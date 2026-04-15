"""Drift detection for continuous compliance monitoring.

Detects three kinds of drift:
1. Confidence drift — are model predictions becoming less certain over time?
2. Latency drift — is the model slowing down (potential data/model issue)?
3. Error rate drift — is the model failing more often?

Uses simple statistical tests suitable for streaming data.
No external dependencies beyond numpy/scipy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np
from scipy import stats

from attest.sdk.registry import AISystem, InferenceRecord


class DriftSeverity(str, Enum):
    NONE = "none"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class DriftSignal:
    metric: str
    severity: DriftSeverity
    description: str
    baseline_mean: float
    current_mean: float
    p_value: float | None = None
    percent_change: float = 0.0


@dataclass
class DriftReport:
    system_id: str
    system_name: str
    signals: list[DriftSignal] = field(default_factory=list)
    overall_severity: DriftSeverity = DriftSeverity.NONE

    @property
    def has_drift(self) -> bool:
        return self.overall_severity != DriftSeverity.NONE

    def summary(self) -> str:
        if not self.has_drift:
            return f"No drift detected for '{self.system_name}'."
        lines = [f"Drift detected for '{self.system_name}' — {self.overall_severity.value}:"]
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


def _detect_metric_drift(
    baseline_values: list[float],
    current_values: list[float],
    metric_name: str,
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
        )

    baseline_arr = np.array(baseline_values)
    current_arr = np.array(current_values)
    baseline_mean = float(baseline_arr.mean())
    current_mean = float(current_arr.mean())

    if baseline_mean != 0:
        pct_change = ((current_mean - baseline_mean) / abs(baseline_mean)) * 100
    else:
        pct_change = 0.0

    stat_result = stats.mannwhitneyu(
        baseline_arr, current_arr, alternative="two-sided"
    )
    p_value = float(stat_result.pvalue)

    if p_value < critical_threshold:
        severity = DriftSeverity.CRITICAL
        desc = (
            f"Critical drift: {metric_name} shifted from {baseline_mean:.3f} to "
            f"{current_mean:.3f} ({pct_change:+.1f}%, p={p_value:.4f})"
        )
    elif p_value < warning_threshold:
        severity = DriftSeverity.WARNING
        desc = (
            f"Warning: {metric_name} shifted from {baseline_mean:.3f} to "
            f"{current_mean:.3f} ({pct_change:+.1f}%, p={p_value:.4f})"
        )
    else:
        severity = DriftSeverity.NONE
        desc = f"{metric_name} stable (p={p_value:.4f})"

    return DriftSignal(
        metric=metric_name,
        severity=severity,
        description=desc,
        baseline_mean=baseline_mean,
        current_mean=current_mean,
        p_value=p_value,
        percent_change=pct_change,
    )


def detect_drift(system: AISystem) -> DriftReport:
    """Run drift detection across all monitored metrics for an AI system."""
    records = system.inference_log
    report = DriftReport(system_id=system.system_id, system_name=system.name)

    if len(records) < 20:
        return report

    baseline, current = _split_window(records)

    baseline_conf = [r.confidence for r in baseline if r.confidence is not None]
    current_conf = [r.confidence for r in current if r.confidence is not None]
    if baseline_conf and current_conf:
        report.signals.append(
            _detect_metric_drift(baseline_conf, current_conf, "confidence")
        )

    baseline_lat = [r.latency_ms for r in baseline]
    current_lat = [r.latency_ms for r in current]
    if baseline_lat and current_lat:
        report.signals.append(
            _detect_metric_drift(baseline_lat, current_lat, "latency_ms")
        )

    def _error_indicators(recs: list[InferenceRecord]) -> list[float]:
        return [1.0 if r.metadata.get("error") else 0.0 for r in recs]

    baseline_err = _error_indicators(baseline)
    current_err = _error_indicators(current)
    if sum(baseline_err) > 0 or sum(current_err) > 0:
        report.signals.append(
            _detect_metric_drift(baseline_err, current_err, "error_rate")
        )

    severities = [s.severity for s in report.signals]
    if DriftSeverity.CRITICAL in severities:
        report.overall_severity = DriftSeverity.CRITICAL
    elif DriftSeverity.WARNING in severities:
        report.overall_severity = DriftSeverity.WARNING

    return report
