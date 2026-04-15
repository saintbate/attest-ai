"""Risk classification engine — maps AI systems to EU AI Act risk categories.

Uses a multi-signal approach:
1. Keyword matching against the system's name, description, purpose, and tags
2. Framework/model type heuristics
3. Safety component detection (Annex I route)
4. Confidence scoring based on signal density

This is intentionally rule-based for v1 — deterministic, auditable, no LLM needed.
An LLM-assisted classifier can be layered on top for ambiguous cases.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from attest.classify.categories import (
    ANNEX_III_CATEGORIES,
    CATEGORY_BY_ID,
    SAFETY_COMPONENT_SIGNALS,
    RiskCategory,
)
from attest.sdk.registry import AISystem, RiskLevel


@dataclass
class ClassificationResult:
    system_id: str
    system_name: str
    risk_level: RiskLevel
    matched_category: RiskCategory | None
    confidence: float
    matched_signals: list[str]
    is_safety_component: bool
    rationale: str
    obligations: list[str]


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", " ", text.lower())


def _count_signal_matches(text: str, signals: list[str]) -> list[str]:
    normalized = _normalize(text)
    matched = []
    for signal in signals:
        if _normalize(signal) in normalized:
            matched.append(signal)
    return matched


def classify_system(system: AISystem) -> ClassificationResult:
    """Classify a single AI system against EU AI Act risk categories."""
    corpus = " ".join([
        system.name,
        system.description,
        system.purpose,
        system.model_type,
        " ".join(f"{k} {v}" for k, v in system.tags.items()),
    ])

    is_safety_component = bool(_count_signal_matches(corpus, SAFETY_COMPONENT_SIGNALS))

    best_category: RiskCategory | None = None
    best_matches: list[str] = []
    best_score = 0.0

    for category in ANNEX_III_CATEGORIES:
        matches = _count_signal_matches(corpus, category.signals)
        if not matches:
            continue

        signal_density = len(matches) / len(category.signals)
        raw_score = len(matches) * 0.6 + signal_density * 0.4

        if is_safety_component and category.id == "critical_infrastructure":
            raw_score *= 1.5

        if raw_score > best_score:
            best_score = raw_score
            best_category = category
            best_matches = matches

    if best_category and best_score >= 0.3:
        confidence = min(best_score / 3.0, 1.0)

        if confidence >= 0.5:
            risk_level = RiskLevel.HIGH
        elif confidence >= 0.25:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.LIMITED

        rationale_parts = [
            f"Matched {len(best_matches)} signal(s) in category "
            f"'{best_category.name}' (Area {best_category.area_number}).",
        ]
        if is_safety_component:
            rationale_parts.append(
                "System also identified as a safety component (Annex I route)."
            )
        rationale_parts.append(f"Signals: {', '.join(best_matches)}")

        return ClassificationResult(
            system_id=system.system_id,
            system_name=system.name,
            risk_level=risk_level,
            matched_category=best_category,
            confidence=confidence,
            matched_signals=best_matches,
            is_safety_component=is_safety_component,
            rationale=" ".join(rationale_parts),
            obligations=best_category.obligations,
        )

    return ClassificationResult(
        system_id=system.system_id,
        system_name=system.name,
        risk_level=RiskLevel.MINIMAL if not is_safety_component else RiskLevel.LIMITED,
        matched_category=None,
        confidence=0.8 if not is_safety_component else 0.4,
        matched_signals=[],
        is_safety_component=is_safety_component,
        rationale=(
            "No high-risk signals detected."
            if not is_safety_component
            else "Safety component detected but no specific Annex III category matched. "
            "Manual review recommended."
        ),
        obligations=[],
    )


def classify_all(systems: list[AISystem]) -> list[ClassificationResult]:
    return [classify_system(s) for s in systems]


def get_compliance_gap(result: ClassificationResult) -> dict[str, bool]:
    """Returns a checklist of required compliance items and their status.

    For now, all items start as False (not compliant) — the monitoring
    and documentation modules will flip these as evidence is collected.
    """
    if result.risk_level != RiskLevel.HIGH:
        return {}

    return {
        "risk_management_system": False,
        "data_governance": False,
        "technical_documentation": False,
        "logging_and_records": True,  # Attest provides this automatically
        "transparency_to_deployers": False,
        "human_oversight": False,
        "accuracy_robustness_cybersecurity": False,
        "conformity_assessment": False,
        "eu_declaration_of_conformity": False,
        "post_market_monitoring": False,
    }
