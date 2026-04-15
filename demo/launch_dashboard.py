"""Launch the Attest dashboard with simulated construction company data.

This populates the registry with realistic AI systems, runs inferences,
classifies risk, and then starts the web dashboard.

Run: python demo/launch_dashboard.py
Then open: http://localhost:8787
"""

import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

import attest
from attest.classify.engine import classify_system
from attest.monitor.alerts import check_deadline_alert, alert_on_drift, get_alert_manager


class SafetyInspectionModel:
    HAZARDS = [
        "no_hard_hat", "no_safety_vest", "missing_guardrail",
        "unsafe_scaffold", "exposed_rebar", "fall_risk",
    ]

    def __init__(self, accuracy=0.91):
        self.accuracy = accuracy
        self._calls = 0

    def __call__(self, image):
        self._calls += 1
        eff_acc = self.accuracy - (0.0003 * max(0, self._calls - 300))
        n = random.randint(0, 4)
        dets = []
        for _ in range(n):
            ok = random.random() < eff_acc
            conf = random.gauss(0.87 if ok else 0.40, 0.10)
            dets.append({
                "class": random.choice(self.HAZARDS),
                "confidence": max(0.05, min(0.99, conf)),
            })
        return {
            "detections": dets,
            "confidence": np.mean([d["confidence"] for d in dets]) if dets else 0.95,
        }


class QualityModel:
    DEFECTS = ["crack_hairline", "crack_structural", "spalling", "corrosion"]

    def __call__(self, image):
        n = random.randint(0, 2)
        defects = [
            {"class": random.choice(self.DEFECTS),
             "confidence": max(0.15, random.gauss(0.80, 0.12)),
             "severity": random.choice(["low", "medium", "high"])}
            for _ in range(n)
        ]
        return {
            "defects": defects,
            "confidence": np.mean([d["confidence"] for d in defects]) if defects else 0.92,
        }


class DocumentParser:
    def __call__(self, text):
        return {
            "permits_found": random.randint(1, 5),
            "violations": random.randint(0, 2),
            "confidence": random.gauss(0.94, 0.03),
        }


def populate():
    print("Populating demo data...")

    safety = attest.wrap(
        SafetyInspectionModel(),
        name="ppe-safety-inspector",
        purpose="Detect PPE violations and safety hazards on construction sites",
        description="YOLOv8-based model detecting hard hats, vests, guardrails, scaffolding issues",
        model_type="YOLOv8-L",
        version="2.4.1",
        tags={"domain": "construction", "deployment": "jetson-orin", "site": "Downtown Tower Project"},
    )

    quality = attest.wrap(
        QualityModel(),
        name="structural-defect-detector",
        purpose="Detect structural defects in concrete and steel for quality assurance",
        description="ResNet50 classifier for crack detection, spalling, and corrosion assessment",
        model_type="ResNet50",
        version="1.7.0",
        tags={"domain": "construction", "deployment": "cloud-gpu", "site": "Bridge Retrofit #42"},
    )

    permits = attest.wrap(
        DocumentParser(),
        name="permit-document-parser",
        purpose="Extract and validate construction permit information from scanned documents",
        description="OCR + NLP pipeline for construction permit compliance verification",
        model_type="LayoutLMv3",
        version="0.9.2",
        tags={"domain": "construction", "deployment": "cloud", "use": "document-processing"},
    )

    print("  Running 500 safety inspections...")
    for _ in range(500):
        img = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        safety(img)

    print("  Running 200 quality inspections...")
    for _ in range(200):
        img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        quality(img)

    print("  Running 150 permit parses...")
    for _ in range(150):
        permits(f"permit document text {random.randint(1000, 9999)}")

    print("  Classifying risk levels...")
    registry = attest.get_registry()
    for system in registry.all_systems():
        result = classify_system(system)
        system.risk_level = result.risk_level
        system.risk_category = result.matched_category.id if result.matched_category else ""
        print(f"    {system.name}: {result.risk_level.value.upper()}")

    print("  Checking for drift...")
    from attest.monitor.drift import detect_drift
    for system in registry.all_systems():
        report = detect_drift(system)
        if report.has_drift:
            alert_on_drift(system.name, system.system_id, report)
            print(f"    ⚠ {system.name}: {report.overall_severity.value} drift")
        else:
            print(f"    ✓ {system.name}: stable")

    deadline_alert = check_deadline_alert()
    if deadline_alert:
        print(f"  📅 {deadline_alert.title}")

    print(f"\nReady: {registry.count} systems, "
          f"{sum(s.total_inferences for s in registry.all_systems()):,} inferences\n")


def main():
    populate()

    print("Starting Attest Dashboard at http://localhost:8787")
    print("Press Ctrl+C to stop\n")

    import uvicorn
    from attest.dashboard.app import app
    uvicorn.run(app, host="0.0.0.0", port=8787, log_level="warning")


if __name__ == "__main__":
    main()
