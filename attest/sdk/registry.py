"""Global registry of all AI systems discovered and monitored by Attest."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    UNACCEPTABLE = "unacceptable"
    HIGH = "high"
    LIMITED = "limited"
    MINIMAL = "minimal"
    UNCLASSIFIED = "unclassified"


@dataclass
class InputEvidence:
    """Hash-only reference to a model input, captured at inference time.

    Purpose: lets an auditor reproduce *which* input produced a given
    prediction without Attest ever storing the input itself. Important for
    camera-based and other high-risk AI systems where Article 12 logging
    must be reproducible at audit time but the underlying data cannot
    leave the customer's environment.
    """

    sha256: str
    size_bytes: int | None = None
    source_type: str | None = None
    ref: str | None = None
    captured_at: float = field(default_factory=time.time)


@dataclass
class InferenceRecord:
    timestamp: float
    input_shape: tuple | None = None
    input_dtype: str | None = None
    output_shape: tuple | None = None
    output_summary: dict[str, Any] | None = None
    confidence: float | None = None
    latency_ms: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    input_evidence: InputEvidence | None = None


@dataclass
class AISystem:
    """Represents a single registered AI system within the organization."""

    system_id: str
    name: str
    description: str = ""
    model_type: str = ""
    framework: str = ""
    version: str = ""
    purpose: str = ""
    risk_level: RiskLevel = RiskLevel.UNCLASSIFIED
    risk_category: str = ""
    risk_rationale: str = ""
    registered_at: float = field(default_factory=time.time)
    inference_log: list[InferenceRecord] = field(default_factory=list)
    tags: dict[str, str] = field(default_factory=dict)
    human_oversight_required: bool = False
    human_oversight_contact: str = ""
    _total_inferences: int = field(default=0, repr=False)
    _error_count: int = field(default=0, repr=False)

    def record_inference(self, record: InferenceRecord) -> None:
        self.inference_log.append(record)
        self._total_inferences += 1
        if len(self.inference_log) > 10_000:
            self.inference_log = self.inference_log[-5_000:]

    @property
    def total_inferences(self) -> int:
        return self._total_inferences

    @property
    def error_rate(self) -> float:
        if self._total_inferences == 0:
            return 0.0
        return self._error_count / self._total_inferences


class SystemRegistry:
    """Thread-safe global registry of all AI systems."""

    def __init__(self) -> None:
        self._systems: dict[str, AISystem] = {}
        self._lock = threading.Lock()

    def register(
        self,
        name: str,
        *,
        description: str = "",
        model_type: str = "",
        framework: str = "",
        version: str = "",
        purpose: str = "",
        tags: dict[str, str] | None = None,
    ) -> AISystem:
        system_id = f"{name}-{uuid.uuid4().hex[:8]}"
        system = AISystem(
            system_id=system_id,
            name=name,
            description=description,
            model_type=model_type,
            framework=framework,
            version=version,
            purpose=purpose,
            tags=tags or {},
        )
        with self._lock:
            self._systems[system_id] = system
        return system

    def get(self, system_id: str) -> AISystem | None:
        return self._systems.get(system_id)

    def find_by_name(self, name: str) -> list[AISystem]:
        return [s for s in self._systems.values() if s.name == name]

    def all_systems(self) -> list[AISystem]:
        return list(self._systems.values())

    def high_risk_systems(self) -> list[AISystem]:
        return [s for s in self._systems.values() if s.risk_level == RiskLevel.HIGH]

    @property
    def count(self) -> int:
        return len(self._systems)

    def summary(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for s in self._systems.values():
            counts[s.risk_level.value] = counts.get(s.risk_level.value, 0) + 1
        return counts


_registry = SystemRegistry()


def get_registry() -> SystemRegistry:
    return _registry
