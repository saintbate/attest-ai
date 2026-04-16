"""Drift detection for continuous compliance monitoring.

Implements multiple drift detection methods to match the statistical rigor
expected in post-market monitoring per EU AI Act Article 72:

- Kolmogorov–Smirnov (KS) two-sample test: nonparametric distribution test
  for 1D feature streams. Drop-in upgrade from Mann-Whitney U — captures
  distribution shape changes, not just median shifts.
- Maximum Mean Discrepancy (MMD): kernel-based two-sample test that works
  on multivariate feature vectors. State of the art for unsupervised drift
  detection in deep learning (see Greco et al., 2024, "DriftLens";
  Zhao et al., 2026, "DA-MSDL" for industrial MMD applications).
- Mann-Whitney U: retained for backward compatibility.

Detects three kinds of drift on streaming inference data:
1. Confidence drift — distribution of model confidence scores
2. Latency drift — distribution of inference times
3. Error rate drift — proportion of inferences flagged as errors

Important caveat (the "verification tax", Wang 2026, arXiv:2604.12951):
  Detecting statistically significant drift requires sample sizes that
  grow as model error rates shrink. Attest reports effect sizes alongside
  p-values so downstream consumers can judge practical significance, not
  just statistical significance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

import numpy as np
from scipy import stats

from attest.sdk.registry import AISystem, InferenceRecord


class DriftSeverity(str, Enum):
    NONE = "none"
    WARNING = "warning"
    CRITICAL = "critical"


DriftMethod = Literal["ks", "mmd", "mannwhitney"]


@dataclass
class DriftSignal:
    metric: str
    severity: DriftSeverity
    description: str
    baseline_mean: float
    current_mean: float
    method: DriftMethod = "ks"
    p_value: float | None = None
    test_statistic: float | None = None
    effect_size: float | None = None
    percent_change: float = 0.0
    sample_sizes: tuple[int, int] = (0, 0)


@dataclass
class DriftReport:
    system_id: str
    system_name: str
    method: DriftMethod = "ks"
    signals: list[DriftSignal] = field(default_factory=list)
    overall_severity: DriftSeverity = DriftSeverity.NONE

    @property
    def has_drift(self) -> bool:
        return self.overall_severity != DriftSeverity.NONE

    def summary(self) -> str:
        if not self.has_drift:
            return f"No drift detected for '{self.system_name}' (method: {self.method})."
        lines = [
            f"Drift detected for '{self.system_name}' — "
            f"{self.overall_severity.value} (method: {self.method}):"
        ]
        for s in self.signals:
            if s.severity != DriftSeverity.NONE:
                lines.append(f"  • {s.metric}: {s.description}")
        return "\n".join(lines)


def _split_window(
    records: list[InferenceRecord],
    split_ratio: float = 0.5,
) -> tuple[list[InferenceRecord], list[InferenceRecord]]:
    if len(records) < 20:
        return records, records
    split_idx = int(len(records) * split_ratio)
    return records[:split_idx], records[split_idx:]


def _mmd_rbf(x: np.ndarray, y: np.ndarray, gamma: float | None = None) -> float:
    """Squared MMD with RBF kernel between samples x and y.

    Reference: Gretton et al., "A Kernel Two-Sample Test", JMLR 2012.
    gamma defaults to the median heuristic (1 / median pairwise squared distance),
    which is the standard default in practice.
    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    if y.ndim == 1:
        y = y.reshape(-1, 1)

    if gamma is None:
        combined = np.vstack([x, y])
        sq_dists = np.sum((combined[:, None] - combined[None, :]) ** 2, axis=-1)
        median_sq = float(np.median(sq_dists[sq_dists > 0])) if np.any(sq_dists > 0) else 1.0
        gamma = 1.0 / median_sq if median_sq > 0 else 1.0

    def kernel(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        sq = np.sum((a[:, None] - b[None, :]) ** 2, axis=-1)
        return np.exp(-gamma * sq)

    k_xx = kernel(x, x).mean()
    k_yy = kernel(y, y).mean()
    k_xy = kernel(x, y).mean()
    return float(k_xx + k_yy - 2 * k_xy)


def _mmd_permutation_test(
    baseline: np.ndarray,
    current: np.ndarray,
    n_permutations: int = 200,
    rng_seed: int = 0,
) -> tuple[float, float]:
    """Permutation test for MMD. Returns (observed MMD, p-value)."""
    rng = np.random.default_rng(rng_seed)
    observed = _mmd_rbf(baseline, current)
    combined = np.concatenate([baseline, current])
    n_baseline = len(baseline)

    count_at_least = 0
    for _ in range(n_permutations):
        rng.shuffle(combined)
        perm_baseline = combined[:n_baseline]
        perm_current = combined[n_baseline:]
        perm_mmd = _mmd_rbf(perm_baseline, perm_current)
        if perm_mmd >= observed:
            count_at_least += 1

    p_value = (count_at_least + 1) / (n_permutations + 1)
    return observed, p_value


def _cohens_d(baseline: np.ndarray, current: np.ndarray) -> float:
    """Effect size — pooled standard deviation version."""
    n1, n2 = len(baseline), len(current)
    if n1 < 2 or n2 < 2:
        return 0.0
    var1, var2 = baseline.var(ddof=1), current.var(ddof=1)
    pooled = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled == 0:
        return 0.0
    return float((current.mean() - baseline.mean()) / pooled)


def _detect_metric_drift(
    baseline_values: list[float],
    current_values: list[float],
    metric_name: str,
    method: DriftMethod = "ks",
    warning_threshold: float = 0.05,
    critical_threshold: float = 0.01,
) -> DriftSignal:
    if len(baseline_values) < 5 or len(current_values) < 5:
        return DriftSignal(
            metric=metric_name,
            severity=DriftSeverity.NONE,
            description="Insufficient data for drift detection.",
            baseline_mean=float(np.mean(baseline_values)) if baseline_values else 0.0,
            current_mean=float(np.mean(current_values)) if current_values else 0.0,
            method=method,
            sample_sizes=(len(baseline_values), len(current_values)),
        )

    baseline_arr = np.array(baseline_values, dtype=np.float64)
    current_arr = np.array(current_values, dtype=np.float64)
    baseline_mean = float(baseline_arr.mean())
    current_mean = float(current_arr.mean())

    if baseline_mean != 0:
        pct_change = ((current_mean - baseline_mean) / abs(baseline_mean)) * 100
    else:
        pct_change = 0.0

    effect_size = _cohens_d(baseline_arr, current_arr)

    if method == "ks":
        ks_result = stats.ks_2samp(baseline_arr, current_arr, alternative="two-sided")
        p_value = float(ks_result.pvalue)
        test_stat = float(ks_result.statistic)
        test_label = f"KS={test_stat:.3f}"
    elif method == "mmd":
        test_stat, p_value = _mmd_permutation_test(baseline_arr, current_arr)
        test_label = f"MMD²={test_stat:.4f}"
    elif method == "mannwhitney":
        mw_result = stats.mannwhitneyu(
            baseline_arr, current_arr, alternative="two-sided"
        )
        p_value = float(mw_result.pvalue)
        test_stat = float(mw_result.statistic)
        test_label = f"U={test_stat:.0f}"
    else:
        raise ValueError(f"unknown drift method: {method}")

    if p_value < critical_threshold:
        severity = DriftSeverity.CRITICAL
        desc = (
            f"Critical drift: {metric_name} shifted from {baseline_mean:.3f} to "
            f"{current_mean:.3f} ({pct_change:+.1f}%, {test_label}, p={p_value:.4f}, "
            f"Cohen's d={effect_size:+.2f})"
        )
    elif p_value < warning_threshold:
        severity = DriftSeverity.WARNING
        desc = (
            f"Warning: {metric_name} shifted from {baseline_mean:.3f} to "
            f"{current_mean:.3f} ({pct_change:+.1f}%, {test_label}, p={p_value:.4f}, "
            f"Cohen's d={effect_size:+.2f})"
        )
    else:
        severity = DriftSeverity.NONE
        desc = f"{metric_name} stable ({test_label}, p={p_value:.4f})"

    return DriftSignal(
        metric=metric_name,
        severity=severity,
        description=desc,
        baseline_mean=baseline_mean,
        current_mean=current_mean,
        method=method,
        p_value=p_value,
        test_statistic=test_stat,
        effect_size=effect_size,
        percent_change=pct_change,
        sample_sizes=(len(baseline_values), len(current_values)),
    )


def detect_drift(
    system: AISystem,
    *,
    method: DriftMethod = "ks",
) -> DriftReport:
    """Run drift detection across all monitored metrics for an AI system.

    Args:
        system: The AISystem to analyze.
        method: One of "ks" (default, Kolmogorov-Smirnov), "mmd"
            (kernel-based, more sensitive to multivariate shifts), or
            "mannwhitney" (original, shift-in-median only).

    Returns:
        DriftReport with per-metric drift signals, effect sizes, and an
        overall severity level.
    """
    records = system.inference_log
    report = DriftReport(
        system_id=system.system_id,
        system_name=system.name,
        method=method,
    )

    if len(records) < 20:
        return report

    baseline, current = _split_window(records)

    baseline_conf = [r.confidence for r in baseline if r.confidence is not None]
    current_conf = [r.confidence for r in current if r.confidence is not None]
    if baseline_conf and current_conf:
        report.signals.append(
            _detect_metric_drift(baseline_conf, current_conf, "confidence", method=method)
        )

    baseline_lat = [r.latency_ms for r in baseline]
    current_lat = [r.latency_ms for r in current]
    if baseline_lat and current_lat:
        report.signals.append(
            _detect_metric_drift(baseline_lat, current_lat, "latency_ms", method=method)
        )

    def _error_indicators(recs: list[InferenceRecord]) -> list[float]:
        return [1.0 if r.metadata.get("error") else 0.0 for r in recs]

    baseline_err = _error_indicators(baseline)
    current_err = _error_indicators(current)
    if sum(baseline_err) > 0 or sum(current_err) > 0:
        report.signals.append(
            _detect_metric_drift(
                baseline_err, current_err, "error_rate", method=method
            )
        )

    severities = [s.severity for s in report.signals]
    if DriftSeverity.CRITICAL in severities:
        report.overall_severity = DriftSeverity.CRITICAL
    elif DriftSeverity.WARNING in severities:
        report.overall_severity = DriftSeverity.WARNING

    return report
