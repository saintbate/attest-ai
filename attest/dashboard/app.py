"""Attest Compliance Dashboard — FastAPI web application.

Serves a real-time compliance dashboard for compliance officers.
Reads from the in-memory registry and the SQLite database.

Run: uvicorn attest.dashboard.app:app --reload --port 8787
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from attest.classify.engine import classify_all, classify_system, get_compliance_gap
from attest.monitor.drift import detect_drift, DriftSeverity
from attest.sdk.registry import RiskLevel, get_registry

DASHBOARD_DIR = Path(__file__).parent
TEMPLATE_DIR = DASHBOARD_DIR / "templates"
STATIC_DIR = DASHBOARD_DIR / "static"
SITE_DIR = Path(__file__).parent.parent.parent / "site"

app = FastAPI(title="Attest Compliance Dashboard", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.get("/landing", response_class=HTMLResponse)
async def landing():
    landing_file = SITE_DIR / "index.html"
    if landing_file.exists():
        return HTMLResponse(landing_file.read_text())
    return HTMLResponse("<h1>Landing page not found</h1>", status_code=404)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    registry = get_registry()
    systems = registry.all_systems()

    classifications = []
    for s in systems:
        result = classify_system(s)
        gap = get_compliance_gap(result)
        compliant_count = sum(1 for v in gap.values() if v) if gap else 0
        total_count = len(gap) if gap else 0
        drift = detect_drift(s)
        classifications.append({
            "system": s,
            "classification": result,
            "gap": gap,
            "compliant_count": compliant_count,
            "total_count": total_count,
            "compliance_pct": int(compliant_count / total_count * 100) if total_count else 100,
            "drift": drift,
        })

    high_risk = sum(1 for c in classifications if c["classification"].risk_level == RiskLevel.HIGH)
    total_inferences = sum(s.total_inferences for s in systems)
    drift_alerts = sum(1 for c in classifications if c["drift"].has_drift)

    overall_compliance = 0
    if classifications:
        pcts = [c["compliance_pct"] for c in classifications if c["total_count"] > 0]
        overall_compliance = int(sum(pcts) / len(pcts)) if pcts else 100

    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={
            "systems": classifications,
            "total_systems": len(systems),
            "high_risk": high_risk,
            "total_inferences": total_inferences,
            "drift_alerts": drift_alerts,
            "overall_compliance": overall_compliance,
            "deadline": "August 2, 2026",
            "days_remaining": (datetime(2026, 8, 2) - datetime.now()).days,
        },
    )


@app.get("/system/{system_id}", response_class=HTMLResponse)
async def system_detail(request: Request, system_id: str):
    registry = get_registry()
    system = registry.get(system_id)
    if not system:
        return HTMLResponse("<h1>System not found</h1>", status_code=404)

    classification = classify_system(system)
    gap = get_compliance_gap(classification)
    drift = detect_drift(system)

    recent_inferences = system.inference_log[-50:]
    confidence_timeline = [
        {"ts": r.timestamp, "confidence": r.confidence, "latency": r.latency_ms}
        for r in recent_inferences if r.confidence is not None
    ]

    compliant_count = sum(1 for v in gap.values() if v) if gap else 0
    total_count = len(gap) if gap else 0

    return templates.TemplateResponse(
        name="system_detail.html",
        request=request,
        context={
            "system": system,
            "classification": classification,
            "gap": gap,
            "compliant_count": compliant_count,
            "total_count": total_count,
            "drift": drift,
            "confidence_timeline": json.dumps(confidence_timeline),
        },
    )


@app.get("/api/systems", response_class=JSONResponse)
async def api_systems():
    registry = get_registry()
    systems = registry.all_systems()
    return [{
        "system_id": s.system_id,
        "name": s.name,
        "risk_level": s.risk_level.value,
        "total_inferences": s.total_inferences,
        "error_rate": s.error_rate,
    } for s in systems]


@app.get("/api/system/{system_id}/metrics", response_class=JSONResponse)
async def api_system_metrics(system_id: str):
    registry = get_registry()
    system = registry.get(system_id)
    if not system:
        return JSONResponse({"error": "not found"}, status_code=404)

    records = system.inference_log[-100:]
    return {
        "system_id": system_id,
        "confidence": [
            {"ts": r.timestamp, "value": r.confidence}
            for r in records if r.confidence is not None
        ],
        "latency": [
            {"ts": r.timestamp, "value": r.latency_ms}
            for r in records
        ],
    }
