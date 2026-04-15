"""Core model wrapper — the one-line integration point.

Usage:
    # Wrap any callable model/pipeline
    model = attest.wrap(model, name="safety-inspector", purpose="Detect OSHA violations on construction sites")
    result = model(image)  # works exactly as before, but now logged + monitored

    # Decorator form
    @attest.monitor(name="crack-detector", purpose="Detect structural cracks in concrete")
    def detect_cracks(image):
        return cv_model.predict(image)

    # Context manager form
    with attest.track("safety-inspector") as tracker:
        result = model.predict(image)
        tracker.record(input=image, output=result, confidence=result.conf)
"""

from __future__ import annotations

import functools
import time
from contextlib import contextmanager
from typing import Any, Callable

import numpy as np

from attest.sdk.registry import AISystem, InferenceRecord, get_registry


def _extract_shape(obj: Any) -> tuple | None:
    if hasattr(obj, "shape"):
        return tuple(obj.shape)
    if isinstance(obj, (list, tuple)) and len(obj) > 0:
        return (len(obj),)
    return None


def _extract_dtype(obj: Any) -> str | None:
    if hasattr(obj, "dtype"):
        return str(obj.dtype)
    return type(obj).__name__


def _extract_confidence(output: Any) -> float | None:
    """Best-effort extraction of confidence from common output formats."""
    if isinstance(output, dict):
        for key in ("confidence", "conf", "score", "probability", "prob"):
            if key in output:
                val = output[key]
                if isinstance(val, (int, float)):
                    return float(val)
                if hasattr(val, "__iter__"):
                    vals = list(val)
                    if vals and isinstance(vals[0], (int, float)):
                        return float(np.mean(vals))

    if hasattr(output, "conf"):
        conf = getattr(output, "conf")
        if hasattr(conf, "mean"):
            return float(conf.mean())
        if isinstance(conf, (int, float)):
            return float(conf)

    return None


def _summarize_output(output: Any) -> dict[str, Any]:
    summary: dict[str, Any] = {"type": type(output).__name__}
    if isinstance(output, dict):
        summary["keys"] = list(output.keys())[:20]
    elif hasattr(output, "shape"):
        summary["shape"] = tuple(output.shape)
    elif isinstance(output, (list, tuple)):
        summary["length"] = len(output)
    return summary


class WrappedModel:
    """Transparent wrapper that logs every inference call."""

    def __init__(
        self,
        model: Any,
        system: AISystem,
    ) -> None:
        self._model = model
        self._system = system

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        input_shape = _extract_shape(args[0]) if args else None
        input_dtype = _extract_dtype(args[0]) if args else None

        start = time.perf_counter()
        try:
            output = self._model(*args, **kwargs)
        except Exception as e:
            self._system._error_count += 1
            self._system.record_inference(InferenceRecord(
                timestamp=time.time(),
                input_shape=input_shape,
                input_dtype=input_dtype,
                latency_ms=(time.perf_counter() - start) * 1000,
                metadata={"error": str(e)},
            ))
            raise
        elapsed_ms = (time.perf_counter() - start) * 1000

        record = InferenceRecord(
            timestamp=time.time(),
            input_shape=input_shape,
            input_dtype=input_dtype,
            output_shape=_extract_shape(output),
            output_summary=_summarize_output(output),
            confidence=_extract_confidence(output),
            latency_ms=elapsed_ms,
        )
        self._system.record_inference(record)
        return output

    def __getattr__(self, name: str) -> Any:
        return getattr(self._model, name)

    @property
    def attest_system(self) -> AISystem:
        return self._system


def wrap(
    model: Any,
    *,
    name: str,
    purpose: str = "",
    description: str = "",
    model_type: str = "",
    version: str = "",
    tags: dict[str, str] | None = None,
) -> WrappedModel:
    """Wrap a model/callable for automatic compliance logging.

    This is the primary integration point. One line:
        model = attest.wrap(model, name="safety-inspector", purpose="OSHA violation detection")
    """
    framework = ""
    model_cls = type(model).__module__ or ""
    if "torch" in model_cls:
        framework = "pytorch"
    elif "tensorflow" in model_cls or "keras" in model_cls:
        framework = "tensorflow"
    elif "sklearn" in model_cls:
        framework = "scikit-learn"
    elif "ultralytics" in model_cls:
        framework = "ultralytics"
    elif "cv2" in model_cls:
        framework = "opencv"

    if not model_type:
        model_type = type(model).__name__

    registry = get_registry()
    system = registry.register(
        name=name,
        description=description or purpose,
        model_type=model_type,
        framework=framework,
        version=version,
        purpose=purpose,
        tags=tags or {},
    )

    return WrappedModel(model, system)


def monitor(
    *,
    name: str,
    purpose: str = "",
    description: str = "",
    tags: dict[str, str] | None = None,
) -> Callable:
    """Decorator form of wrap — monitors every call to the decorated function."""

    def decorator(fn: Callable) -> Callable:
        registry = get_registry()
        system = registry.register(
            name=name,
            description=description or purpose,
            model_type="function",
            framework="custom",
            purpose=purpose,
            tags=tags or {},
        )

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            input_shape = _extract_shape(args[0]) if args else None
            input_dtype = _extract_dtype(args[0]) if args else None

            start = time.perf_counter()
            try:
                output = fn(*args, **kwargs)
            except Exception as e:
                system._error_count += 1
                system.record_inference(InferenceRecord(
                    timestamp=time.time(),
                    input_shape=input_shape,
                    input_dtype=input_dtype,
                    latency_ms=(time.perf_counter() - start) * 1000,
                    metadata={"error": str(e)},
                ))
                raise
            elapsed_ms = (time.perf_counter() - start) * 1000

            record = InferenceRecord(
                timestamp=time.time(),
                input_shape=input_shape,
                input_dtype=input_dtype,
                output_shape=_extract_shape(output),
                output_summary=_summarize_output(output),
                confidence=_extract_confidence(output),
                latency_ms=elapsed_ms,
            )
            system.record_inference(record)
            return output

        wrapper.attest_system = system  # type: ignore[attr-defined]
        return wrapper

    return decorator


class _Tracker:
    """Manual tracking context for cases where wrap/monitor don't fit."""

    def __init__(self, system: AISystem) -> None:
        self.system = system
        self._start = time.time()

    def record(
        self,
        *,
        input: Any = None,
        output: Any = None,
        confidence: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        record = InferenceRecord(
            timestamp=time.time(),
            input_shape=_extract_shape(input),
            input_dtype=_extract_dtype(input) if input is not None else None,
            output_shape=_extract_shape(output),
            output_summary=_summarize_output(output) if output is not None else None,
            confidence=confidence,
            latency_ms=(time.time() - self._start) * 1000,
            metadata=metadata or {},
        )
        self.system.record_inference(record)
        self._start = time.time()


@contextmanager
def track(
    name: str,
    *,
    purpose: str = "",
    tags: dict[str, str] | None = None,
):
    """Context manager form — for pipelines where wrapping a single model isn't enough."""
    registry = get_registry()
    system = registry.register(
        name=name,
        model_type="pipeline",
        framework="custom",
        purpose=purpose,
        tags=tags or {},
    )
    tracker = _Tracker(system)
    try:
        yield tracker
    finally:
        pass
