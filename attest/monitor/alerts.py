"""Alert system for compliance events — webhooks and email notifications.

Triggers alerts on:
- Drift detection (confidence, latency, error rate)
- Risk classification changes
- Compliance posture changes
- Approaching enforcement deadline

Supports:
- Webhook (POST JSON to any URL — Slack, PagerDuty, custom)
- Email (SMTP)
"""

from __future__ import annotations

import json
import smtplib
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum
from typing import Any, Callable


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(str, Enum):
    DRIFT_DETECTED = "drift_detected"
    RISK_LEVEL_CHANGED = "risk_level_changed"
    COMPLIANCE_DEGRADED = "compliance_degraded"
    ERROR_RATE_SPIKE = "error_rate_spike"
    DEADLINE_APPROACHING = "deadline_approaching"
    SYSTEM_REGISTERED = "system_registered"


@dataclass
class Alert:
    alert_type: AlertType
    severity: AlertSeverity
    system_name: str
    system_id: str
    title: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "system_name": self.system_name,
            "system_id": self.system_id,
            "title": self.title,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    def to_slack_block(self) -> dict:
        severity_emoji = {
            AlertSeverity.INFO: "ℹ️",
            AlertSeverity.WARNING: "⚠️",
            AlertSeverity.CRITICAL: "🚨",
        }
        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{severity_emoji[self.severity]} Attest: {self.title}",
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*System:*\n{self.system_name}"},
                        {"type": "mrkdwn", "text": f"*Severity:*\n{self.severity.value.upper()}"},
                    ],
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": self.message},
                },
            ]
        }

    def to_email_html(self) -> str:
        severity_colors = {
            AlertSeverity.INFO: "#6366f1",
            AlertSeverity.WARNING: "#f59e0b",
            AlertSeverity.CRITICAL: "#ef4444",
        }
        color = severity_colors[self.severity]
        return f"""
        <div style="font-family: -apple-system, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: {color}; color: white; padding: 16px 24px; border-radius: 8px 8px 0 0;">
                <h2 style="margin: 0; font-size: 18px;">Attest Compliance Alert</h2>
            </div>
            <div style="background: #1a1f35; color: #e2e8f0; padding: 24px; border: 1px solid #1e293b;
                        border-radius: 0 0 8px 8px;">
                <h3 style="margin: 0 0 8px 0; color: {color};">{self.title}</h3>
                <table style="font-size: 14px; color: #94a3b8; margin-bottom: 16px;">
                    <tr><td style="padding: 4px 16px 4px 0;">System:</td>
                        <td style="color: #e2e8f0;">{self.system_name}</td></tr>
                    <tr><td style="padding: 4px 16px 4px 0;">Severity:</td>
                        <td style="color: {color}; font-weight: 600;">
                            {self.severity.value.upper()}</td></tr>
                    <tr><td style="padding: 4px 16px 4px 0;">Time:</td>
                        <td>{self.timestamp.strftime('%Y-%m-%d %H:%M UTC')}</td></tr>
                </table>
                <p style="margin: 0; font-size: 14px; line-height: 1.6;">{self.message}</p>
                <hr style="border: none; border-top: 1px solid #1e293b; margin: 20px 0;">
                <p style="font-size: 12px; color: #64748b; margin: 0;">
                    Attest — EU AI Act enforcement: August 2, 2026
                </p>
            </div>
        </div>
        """


class WebhookChannel:
    """Send alerts to a webhook URL (Slack, PagerDuty, custom)."""

    def __init__(self, url: str, *, slack_format: bool = False):
        self.url = url
        self.slack_format = slack_format

    def send(self, alert: Alert) -> bool:
        payload = alert.to_slack_block() if self.slack_format else alert.to_dict()
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            self.url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status < 300
        except Exception:
            return False


class EmailChannel:
    """Send alerts via SMTP email."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        from_addr: str,
        to_addrs: list[str],
        *,
        use_tls: bool = True,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_addr = from_addr
        self.to_addrs = to_addrs
        self.use_tls = use_tls

    def send(self, alert: Alert) -> bool:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[Attest {alert.severity.value.upper()}] {alert.title}"
        msg["From"] = self.from_addr
        msg["To"] = ", ".join(self.to_addrs)

        text_body = f"{alert.title}\n\nSystem: {alert.system_name}\n{alert.message}"
        msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(alert.to_email_html(), "html"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.from_addr, self.to_addrs, msg.as_string())
            return True
        except Exception:
            return False


class AlertManager:
    """Central alert manager — routes alerts to configured channels."""

    def __init__(self) -> None:
        self._channels: list[WebhookChannel | EmailChannel] = []
        self._history: list[Alert] = []
        self._filters: list[Callable[[Alert], bool]] = []

    def add_webhook(self, url: str, *, slack: bool = False) -> None:
        self._channels.append(WebhookChannel(url, slack_format=slack))

    def add_email(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        from_addr: str,
        to_addrs: list[str],
    ) -> None:
        self._channels.append(EmailChannel(
            smtp_host, smtp_port, username, password, from_addr, to_addrs,
        ))

    def add_filter(self, fn: Callable[[Alert], bool]) -> None:
        """Only send alerts that pass all filters."""
        self._filters.append(fn)

    def fire(self, alert: Alert) -> int:
        """Send an alert to all channels. Returns number of successful sends."""
        for f in self._filters:
            if not f(alert):
                self._history.append(alert)
                return 0

        self._history.append(alert)
        sent = 0
        for channel in self._channels:
            if channel.send(alert):
                sent += 1
        return sent

    @property
    def history(self) -> list[Alert]:
        return list(self._history)

    def recent(self, n: int = 20) -> list[Alert]:
        return self._history[-n:]


_manager = AlertManager()


def get_alert_manager() -> AlertManager:
    return _manager


def alert_on_drift(system_name: str, system_id: str, drift_report) -> Alert | None:
    """Create and fire an alert from a drift report."""
    if not drift_report.has_drift:
        return None

    from attest.monitor.drift import DriftSeverity

    severity = (
        AlertSeverity.CRITICAL
        if drift_report.overall_severity == DriftSeverity.CRITICAL
        else AlertSeverity.WARNING
    )

    details = []
    for s in drift_report.signals:
        if s.severity != DriftSeverity.NONE:
            details.append(f"• {s.metric}: {s.description}")

    alert = Alert(
        alert_type=AlertType.DRIFT_DETECTED,
        severity=severity,
        system_name=system_name,
        system_id=system_id,
        title=f"Drift detected in {system_name}",
        message="\n".join(details),
        metadata={
            "signals": [
                {"metric": s.metric, "severity": s.severity.value, "p_value": s.p_value}
                for s in drift_report.signals
            ]
        },
    )

    manager = get_alert_manager()
    manager.fire(alert)
    return alert


def alert_on_risk_change(
    system_name: str,
    system_id: str,
    old_level: str,
    new_level: str,
) -> Alert:
    alert = Alert(
        alert_type=AlertType.RISK_LEVEL_CHANGED,
        severity=AlertSeverity.CRITICAL if new_level == "high" else AlertSeverity.WARNING,
        system_name=system_name,
        system_id=system_id,
        title=f"Risk level changed: {system_name}",
        message=f"Risk classification changed from {old_level.upper()} to {new_level.upper()}.",
        metadata={"old_level": old_level, "new_level": new_level},
    )
    get_alert_manager().fire(alert)
    return alert


def check_deadline_alert() -> Alert | None:
    """Fire an alert if the enforcement deadline is approaching."""
    days = (datetime(2026, 8, 2) - datetime.now()).days
    if days > 90:
        return None

    if days <= 30:
        severity = AlertSeverity.CRITICAL
        title = f"EU AI Act enforcement in {days} days"
    elif days <= 60:
        severity = AlertSeverity.WARNING
        title = f"EU AI Act enforcement in {days} days"
    else:
        severity = AlertSeverity.INFO
        title = f"EU AI Act enforcement in {days} days"

    alert = Alert(
        alert_type=AlertType.DEADLINE_APPROACHING,
        severity=severity,
        system_name="all",
        system_id="global",
        title=title,
        message=(
            f"The EU AI Act high-risk system requirements take effect on August 2, 2026. "
            f"You have {days} days remaining to ensure all high-risk AI systems are compliant. "
            f"Non-compliance penalties: up to €15M or 3% of global annual turnover."
        ),
    )
    get_alert_manager().fire(alert)
    return alert
