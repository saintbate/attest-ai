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
import hashlib
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable

import numpy as np

from attest.sdk.registry import AISystem, InferenceRecord, InputEvidence, get_registry


_MAX_FILE_HASH_BYTES = 500_000_000


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


def _describe_array_like(obj: Any) -> str:
    dtype = str(getattr(obj, "dtype", "unknown"))
    if hasattr(obj, "mode") and hasattr(obj, "size") and not hasattr(obj, "shape"):
        return f"image/pil/{obj.mode}"
    shape = getattr(obj, "shape", None)
    if shape is not None:
        if len(shape) == 3 and shape[-1] in (1, 3, 4):
            return f"image/array/{dtype}"
        if len(shape) == 4 and shape[-1] in (1, 3, 4):
            return f"video_frames/array/{dtype}"
        return f"array/{dtype}"
    return f"array/{dtype}"


def _hash_input(obj: Any) -> InputEvidence | None:
    """Best-effort SHA-256 of a model input for audit reproducibility.

    Supports numpy arrays, PIL images, torch tensors, bytes-like objects,
    and file paths. Returns None on unsupported types or any error — this
    function must never raise into the wrapped model's inference path.
    """
    if obj is None:
        return None
    try:
        if hasattr(obj, "tobytes") and callable(obj.tobytes):
            data = obj.tobytes()
            return InputEvidence(
                sha256=hashlib.sha256(data).hexdigest(),
                size_bytes=len(data),
                source_type=_describe_array_like(obj),
            )
        if hasattr(obj, "detach") and hasattr(obj, "cpu") and hasattr(obj, "numpy"):
            arr = obj.detach().cpu().numpy()
            data = arr.tobytes()
            return InputEvidence(
                sha256=hashlib.sha256(data).hexdigest(),
                size_bytes=len(data),
                source_type=f"tensor/{arr.dtype}",
            )
        if isinstance(obj, (bytes, bytearray, memoryview)):
            data = bytes(obj)
            return InputEvidence(
                sha256=hashlib.sha256(data).hexdigest(),
                size_bytes=len(data),
                source_type="bytes",
            )
        if isinstance(obj, (str, Path)):
            s = str(obj)
            if len(s) < 4096:
                p = Path(s)
                if p.exists() and p.is_file() and p.stat().st_size <= _MAX_FILE_HASH_BYTES:
                    h = hashlib.sha256()
                    with open(p, "rb") as f:
                        for chunk in iter(lambda: f.read(1 << 20), b""):
                            h.update(chunk)
                    return InputEvidence(
                        sha256=h.hexdigest(),
                        size_bytes=p.stat().st_size,
                        source_type=f"file/{p.suffix.lstrip('.') or 'unknown'}",
                        ref=str(p.resolve()),
                    )
    except Exception:
        return None
    return None


def _attach_evidence_to_last(
    system: AISystem,
    *,
    ref: str | None = None,
    sha256: str | None = None,
    source_type: str | None = None,
    size_bytes: int | None = None,
) -> None:
    """Attach or merge evidence information into the most recent inference record."""
    if not system.inference_log:
        return
    last = system.inference_log[-1]
    if last.input_evidence is None:
        if sha256 is None and ref is None:
            return
        last.input_evidence = InputEvidence(
            sha256=sha256 or "",
            size_bytes=size_bytes,
            source_type=source_type,
            ref=ref,
        )
        return
    if ref is not None:
        last.input_evidence.ref = ref
    if source_type is not None:
        last.input_evidence.source_type = source_type
    if size_bytes is not None:
        last.input_evidence.size_bytes = size_bytes
    if sha256 is not None and not last.input_evidence.sha256:
        last.input_evidence.sha256 = sha256


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
        *,
        hash_input: bool = False,
    ) -> None:
        self._model = model
        self._system = system
        self._hash_input = hash_input

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        first_input = args[0] if args else None
        input_shape = _extract_shape(first_input)
        input_dtype = _extract_dtype(first_input)
        evidence = _hash_input(first_input) if self._hash_input else None

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
                input_evidence=evidence,
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
            input_evidence=evidence,
        )
        self._system.record_inference(record)
        return output

    def __getattr__(self, name: str) -> Any:
        return getattr(self._model, name)

    @property
    def attest_system(self) -> AISystem:
        return self._system

    def log_evidence(
        self,
        *,
        ref: str | None = None,
        sha256: str | None = None,
        source_type: str | None = None,
        size_bytes: int | None = None,
    ) -> None:
        """Attach an evidence reference to the most recent inference record.

        Typical use (camera-based AI, after an alert fires):

            result = model(frame)
            if result.is_alert():
                model.log_evidence(
                    ref="s3://customer-bucket/frames/2026-04-16T14:33:02.123Z.jpg",
                    source_type="image/jpeg",
                )

        Attest never stores or transmits the underlying frame — only the
        reference and (optionally) a SHA-256 that lets an auditor verify
        the frame at audit time.
        """
        _attach_evidence_to_last(
            self._system,
            ref=ref,
            sha256=sha256,
            source_type=source_type,
            size_bytes=size_bytes,
        )


def wrap(
    model: Any,
    *,
    name: str,
    purpose: str = "",
    description: str = "",
    model_type: str = "",
    version: str = "",
    tags: dict[str, str] | None = None,
    hash_input: bool = False,
) -> WrappedModel:
    """Wrap a model/callable for automatic compliance logging.

    This is the primary integration point. One line:
        model = attest.wrap(model, name="safety-inspector", purpose="OSHA violation detection")

    Optional ``hash_input=True`` enables best-effort SHA-256 hashing of each
    inference input for audit reproducibility — useful for camera-based and
    other high-risk AI systems. Hashing runs in-process and adds a small
    (typically <30 ms) per-call latency on typical image sizes. Attest never
    stores the underlying input; only the hash and shape.
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

    return WrappedModel(model, system, hash_input=hash_input)


def monitor(
    *,
    name: str,
    purpose: str = "",
    description: str = "",
    tags: dict[str, str] | None = None,
    hash_input: bool = False,
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
            first_input = args[0] if args else None
            input_shape = _extract_shape(first_input)
            input_dtype = _extract_dtype(first_input)
            evidence = _hash_input(first_input) if hash_input else None

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
                    input_evidence=evidence,
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
                input_evidence=evidence,
            )
            system.record_inference(record)
            return output

        def _log_evidence(
            *,
            ref: str | None = None,
            sha256: str | None = None,
            source_type: str | None = None,
            size_bytes: int | None = None,
        ) -> None:
            _attach_evidence_to_last(
                system,
                ref=ref,
                sha256=sha256,
                source_type=source_type,
                size_bytes=size_bytes,
            )

        wrapper.attest_system = system  # type: ignore[attr-defined]
        wrapper.log_evidence = _log_evidence  # type: ignore[attr-defined]
        return wrapper

    return decorator


class _Tracker:
    """Manual tracking context for cases where wrap/monitor don't fit."""

    def __init__(self, system: AISystem, *, hash_input: bool = False) -> None:
        self.system = system
        self._hash_input = hash_input
        self._start = time.time()

    def record(
        self,
        *,
        input: Any = None,
        output: Any = None,
        confidence: float | None = None,
        metadata: dict[str, Any] | None = None,
        evidence_ref: str | None = None,
    ) -> None:
        evidence = _hash_input(input) if (self._hash_input and input is not None) else None
        if evidence_ref is not None:
            if evidence is None:
                evidence = InputEvidence(sha256="", ref=evidence_ref)
            else:
                evidence.ref = evidence_ref
        record = InferenceRecord(
            timestamp=time.time(),
            input_shape=_extract_shape(input),
            input_dtype=_extract_dtype(input) if input is not None else None,
            output_shape=_extract_shape(output),
            output_summary=_summarize_output(output) if output is not None else None,
            confidence=confidence,
            latency_ms=(time.time() - self._start) * 1000,
            metadata=metadata or {},
            input_evidence=evidence,
        )
        self.system.record_inference(record)
        self._start = time.time()

    def log_evidence(
        self,
        *,
        ref: str | None = None,
        sha256: str | None = None,
        source_type: str | None = None,
        size_bytes: int | None = None,
    ) -> None:
        _attach_evidence_to_last(
            self.system,
            ref=ref,
            sha256=sha256,
            source_type=source_type,
            size_bytes=size_bytes,
        )


@contextmanager
def track(
    name: str,
    *,
    purpose: str = "",
    tags: dict[str, str] | None = None,
    hash_input: bool = False,
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
    tracker = _Tracker(system, hash_input=hash_input)
    try:
        yield tracker
    finally:
        pass
