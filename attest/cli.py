"""Attest CLI — manage AI system compliance from the command line.

Commands:
    attest inventory    — list all registered AI systems
    attest classify     — run risk classification on all systems
    attest docs         — generate Annex IV documentation
    attest monitor      — run drift detection
    attest status       — compliance dashboard overview
    attest persist      — flush in-memory data to database
    attest alerts       — configure and test alert channels
    attest serve        — launch the compliance dashboard
"""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from attest.classify.engine import classify_all, classify_system, get_compliance_gap
from attest.docs.generator import generate_annex_iv
from attest.monitor.drift import detect_drift, DriftSeverity
from attest.sdk.registry import RiskLevel, get_registry
from attest.store.db import init_db, save_system, save_inference_batch, save_document

console = Console()


@click.group()
@click.version_option(package_name="attest-ai")
def main():
    """Attest — EU AI Act compliance for AI systems."""
    pass


@main.command()
def inventory():
    """List all registered AI systems."""
    registry = get_registry()
    systems = registry.all_systems()

    if not systems:
        console.print("[yellow]No AI systems registered. Wrap your models with attest.wrap() first.[/yellow]")
        return

    table = Table(title=f"AI System Inventory ({len(systems)} systems)")
    table.add_column("Name", style="cyan")
    table.add_column("ID", style="dim")
    table.add_column("Type", style="green")
    table.add_column("Framework")
    table.add_column("Risk Level")
    table.add_column("Inferences", justify="right")
    table.add_column("Error Rate", justify="right")

    for s in systems:
        risk_style = {
            RiskLevel.HIGH: "bold red",
            RiskLevel.LIMITED: "yellow",
            RiskLevel.MINIMAL: "green",
            RiskLevel.UNCLASSIFIED: "dim",
        }.get(s.risk_level, "")

        table.add_row(
            s.name,
            s.system_id,
            s.model_type,
            s.framework,
            f"[{risk_style}]{s.risk_level.value}[/{risk_style}]",
            str(s.total_inferences),
            f"{s.error_rate:.1%}",
        )

    console.print(table)


@main.command()
def classify():
    """Run EU AI Act risk classification on all registered systems."""
    registry = get_registry()
    systems = registry.all_systems()

    if not systems:
        console.print("[yellow]No AI systems registered.[/yellow]")
        return

    results = classify_all(systems)

    for result in results:
        system = registry.get(result.system_id)
        if system:
            system.risk_level = result.risk_level
            system.risk_category = (
                result.matched_category.id if result.matched_category else ""
            )
            system.risk_rationale = result.rationale

        risk_style = "bold red" if result.risk_level == RiskLevel.HIGH else "green"
        panel_content = (
            f"[{risk_style}]Risk Level: {result.risk_level.value.upper()}[/{risk_style}]\n"
            f"Category: {result.matched_category.name if result.matched_category else 'N/A'}\n"
            f"Confidence: {result.confidence:.0%}\n"
            f"Safety Component: {'Yes' if result.is_safety_component else 'No'}\n\n"
            f"Rationale: {result.rationale}\n"
        )

        if result.obligations:
            panel_content += "\nObligations:\n"
            for ob in result.obligations:
                panel_content += f"  • {ob}\n"

        gap = get_compliance_gap(result)
        if gap:
            panel_content += "\nCompliance Gap:\n"
            compliant = sum(1 for v in gap.values() if v)
            total = len(gap)
            panel_content += f"  {compliant}/{total} requirements met\n"
            for item, status in gap.items():
                icon = "[green]✓[/green]" if status else "[red]✗[/red]"
                panel_content += f"  {icon} {item.replace('_', ' ').title()}\n"

        console.print(Panel(panel_content, title=f"[bold]{result.system_name}[/bold]"))


@main.command()
@click.option("--output", "-o", type=click.Path(), help="Output directory for docs")
@click.option("--provider", default="", help="Provider/company name for documentation")
def docs(output: str | None, provider: str):
    """Generate Annex IV technical documentation for all high-risk systems."""
    registry = get_registry()
    systems = registry.all_systems()

    if not systems:
        console.print("[yellow]No AI systems registered.[/yellow]")
        return

    output_dir = Path(output) if output else Path("attest_docs")
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    for system in systems:
        result = classify_system(system)
        if result.risk_level in (RiskLevel.HIGH, RiskLevel.LIMITED):
            doc_path = output_dir / f"{system.name}_{system.system_id}_annex_iv.md"
            doc = generate_annex_iv(
                system,
                result,
                provider_name=provider or "Provider Name (to be completed)",
                output_path=doc_path,
            )
            generated += 1
            console.print(f"[green]Generated:[/green] {doc_path}")

    if generated == 0:
        console.print("[yellow]No high-risk or limited-risk systems found. No docs generated.[/yellow]")
    else:
        console.print(f"\n[bold green]{generated} document(s) generated in {output_dir}/[/bold green]")


@main.command(name="monitor")
def monitor_cmd():
    """Run drift detection on all registered systems."""
    registry = get_registry()
    systems = registry.all_systems()

    if not systems:
        console.print("[yellow]No AI systems registered.[/yellow]")
        return

    for system in systems:
        report = detect_drift(system)

        if not report.has_drift:
            console.print(f"[green]✓[/green] {system.name}: No drift detected")
            continue

        severity_style = (
            "bold red" if report.overall_severity == DriftSeverity.CRITICAL else "yellow"
        )
        console.print(
            f"[{severity_style}]⚠ {system.name}: "
            f"{report.overall_severity.value.upper()} drift detected[/{severity_style}]"
        )
        for signal in report.signals:
            if signal.severity != DriftSeverity.NONE:
                console.print(f"  • {signal.description}")


@main.command()
def status():
    """Show compliance dashboard overview."""
    registry = get_registry()
    systems = registry.all_systems()

    if not systems:
        console.print(Panel(
            "[yellow]No AI systems registered yet.[/yellow]\n\n"
            "Get started:\n"
            "  1. Import attest in your code\n"
            "  2. Wrap your model: model = attest.wrap(model, name='...', purpose='...')\n"
            "  3. Run your application normally\n"
            "  4. Come back here to see compliance status",
            title="[bold]Attest Compliance Dashboard[/bold]",
        ))
        return

    summary = registry.summary()
    total = registry.count
    high_risk = summary.get("high", 0)
    total_inferences = sum(s.total_inferences for s in systems)

    results = classify_all(systems)
    gaps = [get_compliance_gap(r) for r in results if r.risk_level == RiskLevel.HIGH]

    all_items = {}
    for gap in gaps:
        for item, status in gap.items():
            if item not in all_items:
                all_items[item] = {"compliant": 0, "total": 0}
            all_items[item]["total"] += 1
            if status:
                all_items[item]["compliant"] += 1

    overview = (
        f"[bold]AI Systems:[/bold] {total}\n"
        f"[bold red]High Risk:[/bold red] {high_risk}\n"
        f"[bold]Total Inferences Logged:[/bold] {total_inferences:,}\n"
    )
    console.print(Panel(overview, title="[bold]Attest Compliance Dashboard[/bold]"))

    if all_items:
        table = Table(title="Compliance Requirements (High-Risk Systems)")
        table.add_column("Requirement")
        table.add_column("Compliant", justify="center")
        table.add_column("Status")

        for item, counts in all_items.items():
            label = item.replace("_", " ").title()
            ratio = f"{counts['compliant']}/{counts['total']}"
            if counts["compliant"] == counts["total"]:
                status_icon = "[green]✓ Complete[/green]"
            elif counts["compliant"] > 0:
                status_icon = "[yellow]◐ Partial[/yellow]"
            else:
                status_icon = "[red]✗ Missing[/red]"
            table.add_row(label, ratio, status_icon)

        console.print(table)

    console.print("\n[dim]Enforcement deadline: August 2, 2026 — "
                  "ensure all high-risk systems are fully compliant.[/dim]")


@main.command()
@click.option("--db", type=click.Path(), default="attest_compliance.db", help="Database path")
def persist(db: str):
    """Flush in-memory registry data to the compliance database."""
    db_path = Path(db)
    init_db(db_path)

    registry = get_registry()
    systems = registry.all_systems()

    if not systems:
        console.print("[yellow]No systems to persist.[/yellow]")
        return

    for system in systems:
        save_system(system, db_path)
        saved = save_inference_batch(system.system_id, system.inference_log, db_path)
        console.print(f"[green]Persisted:[/green] {system.name} ({saved} inference records)")

    console.print(f"\n[bold green]Data saved to {db_path}[/bold green]")


@main.command()
@click.option("--webhook", help="Webhook URL to add (Slack, PagerDuty, custom)")
@click.option("--slack", is_flag=True, help="Format webhook payload for Slack")
@click.option("--test", is_flag=True, help="Send a test alert to all configured channels")
def alerts(webhook: str | None, slack: bool, test: bool):
    """Configure and test alert channels."""
    from attest.monitor.alerts import (
        Alert, AlertSeverity, AlertType, get_alert_manager, check_deadline_alert,
    )

    manager = get_alert_manager()

    if webhook:
        manager.add_webhook(webhook, slack=slack)
        console.print(f"[green]Added webhook:[/green] {webhook} {'(Slack format)' if slack else ''}")

    if test:
        test_alert = Alert(
            alert_type=AlertType.DRIFT_DETECTED,
            severity=AlertSeverity.WARNING,
            system_name="test-system",
            system_id="test-001",
            title="Test Alert from Attest",
            message="This is a test alert to verify your notification channels are working.",
        )
        sent = manager.fire(test_alert)
        if sent > 0:
            console.print(f"[green]Test alert sent to {sent} channel(s)[/green]")
        else:
            console.print("[yellow]No channels configured or all sends failed.[/yellow]")

    deadline = check_deadline_alert()
    if deadline:
        console.print(f"\n[bold yellow]{deadline.title}[/bold yellow]")
        console.print(f"[dim]{deadline.message}[/dim]")

    history = manager.recent(10)
    if history:
        console.print(f"\n[bold]Recent Alerts ({len(history)})[/bold]")
        for a in history:
            sev_style = {"critical": "bold red", "warning": "yellow", "info": "cyan"}.get(
                a.severity.value, ""
            )
            console.print(
                f"  [{sev_style}]{a.severity.value.upper()}[/{sev_style}] "
                f"{a.title} — {a.system_name}"
            )


@main.command()
@click.option("--host", default="0.0.0.0", help="Host to bind")
@click.option("--port", default=8787, help="Port to bind")
def serve(host: str, port: int):
    """Launch the Attest compliance dashboard."""
    import uvicorn
    from attest.dashboard.app import app

    console.print(f"[bold]Starting Attest Dashboard at http://localhost:{port}[/bold]")
    uvicorn.run(app, host=host, port=port, log_level="warning")
