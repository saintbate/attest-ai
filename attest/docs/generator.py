"""Annex IV technical documentation generator.

Generates compliance documentation from runtime data collected by the Attest SDK.
Outputs Markdown that can be converted to PDF for regulatory submission.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from jinja2 import Environment, FileSystemLoader

import attest
from attest.classify.engine import ClassificationResult, classify_system, get_compliance_gap
from attest.sdk.registry import AISystem


TEMPLATE_DIR = Path(__file__).parent / "templates"


@dataclass
class ConfidenceStats:
    mean: float
    std: float
    min: float
    max: float
    below_threshold: int


def _compute_confidence_stats(system: AISystem) -> ConfidenceStats | None:
    confidences = [
        r.confidence for r in system.inference_log if r.confidence is not None
    ]
    if not confidences:
        return None
    arr = np.array(confidences)
    return ConfidenceStats(
        mean=float(arr.mean()),
        std=float(arr.std()),
        min=float(arr.min()),
        max=float(arr.max()),
        below_threshold=int((arr < 0.5).sum()),
    )


@dataclass
class InputStats:
    common_shape: str
    common_dtype: str


def _compute_input_stats(system: AISystem) -> InputStats | None:
    shapes = [r.input_shape for r in system.inference_log if r.input_shape]
    dtypes = [r.input_dtype for r in system.inference_log if r.input_dtype]
    if not shapes and not dtypes:
        return None

    common_shape = "varies"
    if shapes:
        from collections import Counter
        shape_counts = Counter(str(s) for s in shapes)
        common_shape = shape_counts.most_common(1)[0][0]

    common_dtype = "varies"
    if dtypes:
        from collections import Counter
        dtype_counts = Counter(dtypes)
        common_dtype = dtype_counts.most_common(1)[0][0]

    return InputStats(common_shape=common_shape, common_dtype=common_dtype)


def generate_annex_iv(
    system: AISystem,
    classification: ClassificationResult | None = None,
    *,
    provider_name: str = "Provider Name (to be completed)",
    deployment_form: str = "",
    output_path: str | Path | None = None,
) -> str:
    """Generate Annex IV technical documentation for an AI system.

    Returns the rendered Markdown string. Optionally writes to output_path.
    """
    if classification is None:
        classification = classify_system(system)

    now = datetime.now()
    compliance_gap = get_compliance_gap(classification)

    latencies = [r.latency_ms for r in system.inference_log]
    avg_latency = np.mean(latencies) if latencies else 0.0

    timestamps = [r.timestamp for r in system.inference_log]
    if timestamps:
        monitoring_start = datetime.fromtimestamp(min(timestamps)).strftime("%Y-%m-%d %H:%M")
        monitoring_end = datetime.fromtimestamp(max(timestamps)).strftime("%Y-%m-%d %H:%M")
    else:
        monitoring_start = now.strftime("%Y-%m-%d %H:%M")
        monitoring_end = monitoring_start

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        keep_trailing_newline=True,
    )
    template = env.get_template("annex_iv.md.j2")

    rendered = template.render(
        version=attest.__version__,
        generated_at=now.strftime("%Y-%m-%d %H:%M UTC"),
        retention_until=(now + timedelta(days=3652)).strftime("%Y-%m-%d"),
        system=system,
        classification=classification,
        provider_name=provider_name,
        deployment_form=deployment_form,
        registration_date=datetime.fromtimestamp(system.registered_at).strftime("%Y-%m-%d"),
        avg_latency_ms=avg_latency,
        monitoring_start=monitoring_start,
        monitoring_end=monitoring_end,
        confidence_stats=_compute_confidence_stats(system),
        input_stats=_compute_input_stats(system),
        drift_report=None,
        compliance_gap=compliance_gap,
    )

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered)

    return rendered
