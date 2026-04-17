"""OSCAL-aligned assessment results output for Attest.

Produces machine-readable compliance evidence in an OSCAL-inspired JSON
format. OSCAL (Open Security Controls Assessment Language) is the NIST
open standard for expressing security and compliance information
(https://pages.nist.gov/OSCAL/).

What this module produces
-------------------------
An Assessment Results Model (AR) document with:
- metadata: document-level provenance (title, version, timestamps, parties)
- import-ap: stub reference to the assessment plan (end-user can swap in
  a real AP if they have one)
- results: one result per AI system, each containing
    - observations: runtime evidence collected by the Attest SDK
    - findings: per-control compliance state derived from the Attest
      compliance gap checklist

Scope & honesty
---------------
This is OSCAL-*aligned*, not a certified, schema-validated OSCAL
document. The JSON follows OSCAL's Assessment Results key names and
structure so it can be ingested by OSCAL tooling with minimal adapter
work, but Attest does not (yet) ship an OSCAL schema validator.

Controls are mapped to EU AI Act Chapter III, Section 2 articles (the
high-risk provider obligations). These control IDs are custom — not part
of NIST catalogs — because no official OSCAL-formatted EU AI Act catalog
exists at the time of writing. When one is published, Attest will switch
to citing it.

References
----------
- NIST OSCAL: https://pages.nist.gov/OSCAL/resources/concepts/layer/assessment/assessment-results/
- EU AI Act full text: Regulation (EU) 2024/1689
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

import attest
from attest.classify.engine import ClassificationResult, classify_system, get_compliance_gap
from attest.sdk.registry import AISystem, RiskLevel


EU_AI_ACT_CONTROLS: dict[str, dict[str, str]] = {
    "eu-ai-act-a9": {
        "title": "Risk management system (Article 9)",
        "gap_key": "risk_management_system",
    },
    "eu-ai-act-a10": {
        "title": "Data and data governance (Article 10)",
        "gap_key": "data_governance",
    },
    "eu-ai-act-a11": {
        "title": "Technical documentation (Article 11, Annex IV)",
        "gap_key": "technical_documentation",
    },
    "eu-ai-act-a12": {
        "title": "Record-keeping / automatic logs (Article 12)",
        "gap_key": "logging_and_records",
    },
    "eu-ai-act-a13": {
        "title": "Transparency and provision of information to deployers (Article 13)",
        "gap_key": "transparency_to_deployers",
    },
    "eu-ai-act-a14": {
        "title": "Human oversight (Article 14)",
        "gap_key": "human_oversight",
    },
    "eu-ai-act-a15": {
        "title": "Accuracy, robustness and cybersecurity (Article 15)",
        "gap_key": "accuracy_robustness_cybersecurity",
    },
    "eu-ai-act-a43": {
        "title": "Conformity assessment (Article 43)",
        "gap_key": "conformity_assessment",
    },
    "eu-ai-act-a47": {
        "title": "EU declaration of conformity (Article 47)",
        "gap_key": "eu_declaration_of_conformity",
    },
    "eu-ai-act-a72": {
        "title": "Post-market monitoring plan (Article 72)",
        "gap_key": "post_market_monitoring",
    },
}


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _prop(name: str, value: str, ns: str = "https://attest.ai/ns/oscal") -> dict[str, str]:
    return {"name": name, "value": value, "ns": ns}


def _inference_stats(system: AISystem) -> dict[str, Any]:
    confidences = [r.confidence for r in system.inference_log if r.confidence is not None]
    latencies = [r.latency_ms for r in system.inference_log]
    total = len(system.inference_log)
    with_hash = sum(
        1 for r in system.inference_log
        if r.input_evidence is not None and r.input_evidence.sha256
    )
    with_ref = sum(
        1 for r in system.inference_log
        if r.input_evidence is not None and r.input_evidence.ref
    )
    return {
        "total_inferences": system.total_inferences,
        "error_rate": round(system.error_rate, 6),
        "mean_confidence": round(float(np.mean(confidences)), 6) if confidences else None,
        "std_confidence": round(float(np.std(confidences)), 6) if confidences else None,
        "mean_latency_ms": round(float(np.mean(latencies)), 3) if latencies else None,
        "p95_latency_ms": round(float(np.percentile(latencies, 95)), 3) if latencies else None,
        "evidence_records": total,
        "evidence_with_hash": with_hash,
        "evidence_with_ref": with_ref,
        "evidence_hash_coverage": round(with_hash / total, 4) if total else 0.0,
        "evidence_ref_coverage": round(with_ref / total, 4) if total else 0.0,
    }


def _build_observations(
    system: AISystem, classification: ClassificationResult
) -> list[dict[str, Any]]:
    stats = _inference_stats(system)
    observations: list[dict[str, Any]] = []

    observations.append({
        "uuid": str(uuid.uuid4()),
        "title": "Automatic inference logging (Article 12)",
        "description": (
            f"Attest SDK recorded {stats['total_inferences']} inference events for "
            f"'{system.name}'. Error rate: {stats['error_rate']:.4%}."
        ),
        "methods": ["TEST"],
        "types": ["monitoring"],
        "collected": _iso_now(),
        "props": [
            _prop("total_inferences", str(stats["total_inferences"])),
            _prop("error_rate", str(stats["error_rate"])),
            _prop("source", "attest.sdk"),
        ],
    })

    if stats["mean_confidence"] is not None:
        observations.append({
            "uuid": str(uuid.uuid4()),
            "title": "Model confidence distribution",
            "description": (
                f"Mean confidence {stats['mean_confidence']:.3f} "
                f"(σ={stats['std_confidence']:.3f}) across "
                f"{stats['total_inferences']} inferences. Supports Article 15 "
                f"accuracy monitoring."
            ),
            "methods": ["TEST"],
            "types": ["finding"],
            "collected": _iso_now(),
            "props": [
                _prop("mean_confidence", str(stats["mean_confidence"])),
                _prop("std_confidence", str(stats["std_confidence"])),
            ],
        })

    if stats["mean_latency_ms"] is not None:
        observations.append({
            "uuid": str(uuid.uuid4()),
            "title": "Inference latency distribution",
            "description": (
                f"Mean latency {stats['mean_latency_ms']:.2f} ms, "
                f"P95 {stats['p95_latency_ms']:.2f} ms. Captured by Attest SDK "
                f"for post-market monitoring (Article 72)."
            ),
            "methods": ["TEST"],
            "types": ["finding"],
            "collected": _iso_now(),
            "props": [
                _prop("mean_latency_ms", str(stats["mean_latency_ms"])),
                _prop("p95_latency_ms", str(stats["p95_latency_ms"])),
            ],
        })

    if stats["evidence_with_hash"] > 0 or stats["evidence_with_ref"] > 0:
        observations.append({
            "uuid": str(uuid.uuid4()),
            "title": "Input evidence linking (Article 12 reproducibility)",
            "description": (
                f"Of {stats['evidence_records']} recorded inferences, "
                f"{stats['evidence_with_hash']} "
                f"({stats['evidence_hash_coverage']:.2%}) have a cryptographic "
                f"input hash and "
                f"{stats['evidence_with_ref']} "
                f"({stats['evidence_ref_coverage']:.2%}) have a customer-supplied "
                f"input reference. This lets an auditor reproduce which input "
                f"produced a given prediction without Attest ever storing the "
                f"underlying data — relevant for camera-based and other "
                f"high-risk AI systems where Article 12 logging must be "
                f"reproducible at audit time."
            ),
            "methods": ["TEST"],
            "types": ["monitoring"],
            "collected": _iso_now(),
            "props": [
                _prop("evidence_hash_coverage", str(stats["evidence_hash_coverage"])),
                _prop("evidence_ref_coverage", str(stats["evidence_ref_coverage"])),
                _prop("evidence_records_total", str(stats["evidence_records"])),
                _prop("source", "attest.sdk/input_evidence"),
            ],
        })

    observations.append({
        "uuid": str(uuid.uuid4()),
        "title": "Risk classification (Article 6, Annex III)",
        "description": (
            f"Rule-based classification assigned risk level "
            f"'{classification.risk_level.value}' "
            f"(category: {classification.matched_category.name if classification.matched_category else 'n/a'}, "
            f"confidence: {classification.confidence:.2f}). "
            f"Manual review by a qualified assessor is recommended before relying "
            f"on this classification for a conformity assessment."
        ),
        "methods": ["EXAMINE"],
        "types": ["risk"],
        "collected": _iso_now(),
        "props": [
            _prop("risk_level", classification.risk_level.value),
            _prop(
                "annex_iii_area",
                str(classification.matched_category.area_number)
                if classification.matched_category
                else "none",
            ),
            _prop("classifier", "attest.classify.engine/rule-based"),
            _prop("classifier_confidence", str(round(classification.confidence, 3))),
        ],
    })

    return observations


def _build_findings(
    system: AISystem,
    classification: ClassificationResult,
    observation_uuids: list[str],
) -> list[dict[str, Any]]:
    gap = get_compliance_gap(classification)
    if not gap:
        return []

    findings: list[dict[str, Any]] = []
    for control_id, control in EU_AI_ACT_CONTROLS.items():
        gap_key = control["gap_key"]
        is_compliant = gap.get(gap_key, False)

        finding = {
            "uuid": str(uuid.uuid4()),
            "title": control["title"],
            "description": (
                f"{'Evidence found' if is_compliant else 'Evidence not yet collected'} "
                f"for '{control['title']}' on system '{system.name}'."
            ),
            "target": {
                "type": "objective-id",
                "target-id": control_id,
                "status": {
                    "state": "satisfied" if is_compliant else "not-satisfied"
                },
            },
            "related-observations": [
                {"observation-uuid": u} for u in observation_uuids
            ],
            "props": [
                _prop("control_id", control_id),
                _prop("evidence_source", "attest"),
            ],
        }
        findings.append(finding)

    return findings


def _build_system_result(system: AISystem) -> dict[str, Any]:
    classification = classify_system(system)
    observations = _build_observations(system, classification)
    obs_uuids = [o["uuid"] for o in observations]
    findings = _build_findings(system, classification, obs_uuids)

    return {
        "uuid": str(uuid.uuid4()),
        "title": f"Compliance assessment for {system.name}",
        "description": (
            f"Runtime compliance evidence for AI system '{system.name}' "
            f"(system_id={system.system_id}), classified as "
            f"'{classification.risk_level.value}' risk under EU AI Act Annex III."
        ),
        "start": datetime.fromtimestamp(system.registered_at, tz=timezone.utc).isoformat(
            timespec="seconds"
        ),
        "end": _iso_now(),
        "props": [
            _prop("system_id", system.system_id),
            _prop("system_name", system.name),
            _prop("risk_level", classification.risk_level.value),
            _prop("framework", system.framework or "unspecified"),
            _prop("model_type", system.model_type or "unspecified"),
        ],
        "observations": observations,
        "findings": findings,
    }


def generate_oscal_assessment_results(
    systems: list[AISystem],
    *,
    provider_name: str = "Provider Name (to be completed)",
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Generate an OSCAL-aligned Assessment Results document for N systems.

    Args:
        systems: The AI systems to include in the assessment.
        provider_name: Organization acting as the provider of these systems
            (appears in the OSCAL metadata as a responsible party).
        output_path: If set, writes the JSON document to this path.

    Returns:
        A dict conforming to OSCAL Assessment Results shape. Top-level key
        is "assessment-results".
    """
    high_risk_systems = [s for s in systems if classify_system(s).risk_level == RiskLevel.HIGH]
    results = [_build_system_result(s) for s in high_risk_systems]

    doc_uuid = str(uuid.uuid4())
    provider_uuid = str(uuid.uuid4())
    tool_uuid = str(uuid.uuid4())

    document = {
        "assessment-results": {
            "uuid": doc_uuid,
            "metadata": {
                "title": "Attest — EU AI Act Compliance Assessment Results",
                "last-modified": _iso_now(),
                "version": attest.__version__,
                "oscal-version": "1.1.2",
                "props": [
                    _prop("regulatory_framework", "EU AI Act (2024/1689)"),
                    _prop("generator", "attest-ai"),
                    _prop("generator_version", attest.__version__),
                ],
                "parties": [
                    {
                        "uuid": provider_uuid,
                        "type": "organization",
                        "name": provider_name,
                        "props": [_prop("role", "provider")],
                    },
                    {
                        "uuid": tool_uuid,
                        "type": "organization",
                        "name": "Attest (Vertical AI LLC)",
                        "props": [_prop("role", "assessor-tool")],
                    },
                ],
                "responsible-parties": [
                    {"role-id": "provider", "party-uuids": [provider_uuid]},
                    {"role-id": "assessor-tool", "party-uuids": [tool_uuid]},
                ],
            },
            "import-ap": {
                "href": "#attest-default-assessment-plan",
                "remarks": (
                    "No external Assessment Plan was imported. Controls were "
                    "derived from EU AI Act Chapter III, Section 2 obligations "
                    "for high-risk systems. Replace this reference with your "
                    "organization's formal AP if one exists."
                ),
            },
            "results": results,
        }
    }

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, indent=2))

    return document
