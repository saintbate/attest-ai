"""Demo: Construction Safety Inspection AI — Full Compliance Flow

Simulates a construction company using AI for safety inspections.
Shows the complete Attest integration:
  1. One-line model wrapping
  2. Automatic risk classification
  3. Continuous monitoring with drift detection
  4. Annex IV documentation generation

Run: python demo/construction_safety.py
"""

import random
import sys
import time
from pathlib import Path

import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table

sys.path.insert(0, str(Path(__file__).parent.parent))

import attest
from attest.classify.engine import classify_system, get_compliance_gap
from attest.docs.generator import generate_annex_iv
from attest.monitor.drift import detect_drift, DriftSeverity

console = Console()


# --- Simulated construction safety CV model ---

class SafetyInspectionModel:
    """Simulates a YOLOv8-style model trained to detect construction hazards."""

    HAZARD_CLASSES = [
        "no_hard_hat", "no_safety_vest", "missing_guardrail",
        "unsafe_scaffold", "exposed_rebar", "electrical_hazard",
        "fall_risk", "blocked_exit", "no_ppe", "crane_proximity",
    ]

    def __init__(self, accuracy: float = 0.92):
        self.accuracy = accuracy
        self._call_count = 0

    def __call__(self, image: np.ndarray) -> dict:
        self._call_count += 1

        # Simulate accuracy degradation over time (drift scenario)
        effective_accuracy = self.accuracy
        if self._call_count > 150:
            effective_accuracy -= 0.08  # model starts degrading

        num_detections = random.randint(0, 4)
        detections = []
        for _ in range(num_detections):
            is_correct = random.random() < effective_accuracy
            hazard = random.choice(self.HAZARD_CLASSES)
            conf = random.gauss(0.85 if is_correct else 0.45, 0.12)
            conf = max(0.01, min(0.99, conf))
            detections.append({
                "class": hazard,
                "confidence": conf,
                "bbox": [
                    random.randint(0, 600),
                    random.randint(0, 400),
                    random.randint(50, 200),
                    random.randint(50, 200),
                ],
            })

        return {
            "detections": detections,
            "confidence": np.mean([d["confidence"] for d in detections]) if detections else 0.95,
            "image_size": tuple(image.shape[:2]),
            "processing_time_ms": random.gauss(45, 8),
        }

    def predict(self, image: np.ndarray) -> dict:
        return self(image)


class QualityInspectionModel:
    """Simulates a model that detects structural defects (cracks, spalling, corrosion)."""

    DEFECT_CLASSES = [
        "crack_hairline", "crack_structural", "spalling",
        "corrosion", "delamination", "water_damage",
    ]

    def __call__(self, image: np.ndarray) -> dict:
        num_defects = random.randint(0, 3)
        defects = []
        for _ in range(num_defects):
            defects.append({
                "class": random.choice(self.DEFECT_CLASSES),
                "confidence": max(0.1, random.gauss(0.78, 0.15)),
                "severity": random.choice(["low", "medium", "high"]),
            })

        return {
            "defects": defects,
            "confidence": np.mean([d["confidence"] for d in defects]) if defects else 0.90,
            "structural_risk": "high" if any(
                d["class"] == "crack_structural" and d["severity"] == "high" for d in defects
            ) else "normal",
        }


def run_demo():
    console.print(Panel(
        "[bold]Attest Demo: Construction Safety AI Compliance[/bold]\n\n"
        "Simulates a construction company running two AI inspection systems.\n"
        "Shows automatic risk classification, continuous monitoring,\n"
        "drift detection, and Annex IV documentation generation.",
        border_style="blue",
    ))
    console.print()

    # --- Step 1: Wrap models with Attest (one-line integration) ---
    console.print("[bold cyan]Step 1: Register AI Systems (one-line integration)[/bold cyan]")
    console.print()

    safety_model = SafetyInspectionModel(accuracy=0.92)
    quality_model = QualityInspectionModel()

    # THE ONE LINE — this is the entire integration:
    safety_ai = attest.wrap(
        safety_model,
        name="safety-inspector",
        purpose="Detect OSHA safety violations on construction sites using computer vision",
        description="YOLOv8-based hazard detection for construction site safety compliance",
        model_type="YOLOv8",
        version="2.1.0",
        tags={"domain": "construction", "deployment": "edge-device", "site": "Project Alpha"},
    )

    quality_ai = attest.wrap(
        quality_model,
        name="quality-inspector",
        purpose="Detect structural defects in concrete and steel for quality control",
        description="CNN-based defect detection for structural integrity assessment",
        model_type="ResNet50",
        version="1.3.0",
        tags={"domain": "construction", "deployment": "cloud", "site": "Project Alpha"},
    )

    console.print("  [green]✓[/green] safety-inspector registered (YOLOv8 hazard detection)")
    console.print("  [green]✓[/green] quality-inspector registered (ResNet50 defect detection)")
    console.print()

    # --- Step 2: Simulate inference (normal operation) ---
    console.print("[bold cyan]Step 2: Simulate 200 site inspections[/bold cyan]")
    console.print()

    with Progress() as progress:
        task = progress.add_task("Running inspections...", total=200)
        for i in range(200):
            image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
            safety_ai(image)
            if i % 3 == 0:
                quality_ai(image)
            progress.advance(task)
            time.sleep(0.005)

    console.print(f"  [green]✓[/green] {safety_ai.attest_system.total_inferences} safety inspections logged")
    console.print(f"  [green]✓[/green] {quality_ai.attest_system.total_inferences} quality inspections logged")
    console.print()

    # --- Step 3: Automatic risk classification ---
    console.print("[bold cyan]Step 3: EU AI Act Risk Classification[/bold cyan]")
    console.print()

    registry = attest.get_registry()
    for system in registry.all_systems():
        result = classify_system(system)
        system.risk_level = result.risk_level
        system.risk_category = result.matched_category.id if result.matched_category else ""

        risk_style = "bold red" if result.risk_level.value == "high" else "green"
        console.print(f"  [{risk_style}]■[/{risk_style}] {system.name}: "
                       f"[{risk_style}]{result.risk_level.value.upper()}[/{risk_style}]")
        console.print(f"    Category: {result.matched_category.name if result.matched_category else 'N/A'}")
        console.print(f"    Confidence: {result.confidence:.0%}")
        if result.matched_signals:
            console.print(f"    Signals: {', '.join(result.matched_signals[:5])}")
        console.print()

    # --- Step 4: Drift detection ---
    console.print("[bold cyan]Step 4: Drift Detection[/bold cyan]")
    console.print()

    for system in registry.all_systems():
        report = detect_drift(system)
        if report.has_drift:
            sev_style = "bold red" if report.overall_severity == DriftSeverity.CRITICAL else "yellow"
            console.print(f"  [{sev_style}]⚠[/{sev_style}] {system.name}: "
                           f"{report.overall_severity.value}")
            for signal in report.signals:
                if signal.severity != DriftSeverity.NONE:
                    console.print(f"    {signal.description}")
        else:
            console.print(f"  [green]✓[/green] {system.name}: stable")
    console.print()

    # --- Step 5: Compliance gap analysis ---
    console.print("[bold cyan]Step 5: Compliance Gap Analysis[/bold cyan]")
    console.print()

    for system in registry.all_systems():
        result = classify_system(system)
        gap = get_compliance_gap(result)
        if not gap:
            console.print(f"  [green]✓[/green] {system.name}: no high-risk obligations")
            continue

        compliant = sum(1 for v in gap.values() if v)
        total = len(gap)

        table = Table(title=f"{system.name} — {compliant}/{total} requirements met")
        table.add_column("Requirement", style="cyan")
        table.add_column("Status", justify="center")

        for item, status in gap.items():
            icon = "[green]✓[/green]" if status else "[red]✗[/red]"
            table.add_row(item.replace("_", " ").title(), icon)
        console.print(table)
        console.print()

    # --- Step 6: Generate Annex IV documentation ---
    console.print("[bold cyan]Step 6: Generate Annex IV Technical Documentation[/bold cyan]")
    console.print()

    output_dir = Path("attest_docs")
    output_dir.mkdir(exist_ok=True)

    for system in registry.all_systems():
        result = classify_system(system)
        if result.risk_level.value == "high":
            doc_path = output_dir / f"{system.name}_annex_iv.md"
            generate_annex_iv(
                system,
                result,
                provider_name="BuildSafe AI Corp.",
                deployment_form="Edge device (Jetson Orin) + Cloud dashboard",
                output_path=doc_path,
            )
            console.print(f"  [green]✓[/green] Generated: {doc_path}")

    console.print()

    # --- Summary ---
    console.print(Panel(
        "[bold green]Demo Complete[/bold green]\n\n"
        f"AI Systems Discovered: {registry.count}\n"
        f"High-Risk Systems: {len(registry.high_risk_systems())}\n"
        f"Total Inferences Logged: "
        f"{sum(s.total_inferences for s in registry.all_systems()):,}\n"
        f"Documents Generated: {len(list(output_dir.glob('*.md')))}\n\n"
        "In a real deployment, this entire flow is automatic.\n"
        "The construction company just wraps their model and Attest handles the rest.\n\n"
        "[dim]Enforcement deadline: August 2, 2026[/dim]",
        title="[bold]Compliance Summary[/bold]",
        border_style="green",
    ))


if __name__ == "__main__":
    run_demo()
