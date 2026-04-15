"""Persistent storage for compliance evidence.

Uses SQLite for the MVP — simple, zero-config, file-based.
10-year retention requirement means we need reliable, long-lived storage.
"""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

from attest.sdk.registry import AISystem, InferenceRecord


DEFAULT_DB_PATH = Path("attest_compliance.db")


def _get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: Path = DEFAULT_DB_PATH) -> None:
    conn = _get_connection(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS ai_systems (
            system_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            model_type TEXT DEFAULT '',
            framework TEXT DEFAULT '',
            version TEXT DEFAULT '',
            purpose TEXT DEFAULT '',
            risk_level TEXT DEFAULT 'unclassified',
            risk_category TEXT DEFAULT '',
            risk_rationale TEXT DEFAULT '',
            is_safety_component INTEGER DEFAULT 0,
            human_oversight_required INTEGER DEFAULT 0,
            human_oversight_contact TEXT DEFAULT '',
            tags TEXT DEFAULT '{}',
            registered_at REAL NOT NULL,
            updated_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS inference_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system_id TEXT NOT NULL REFERENCES ai_systems(system_id),
            timestamp REAL NOT NULL,
            input_shape TEXT,
            input_dtype TEXT,
            output_shape TEXT,
            output_summary TEXT,
            confidence REAL,
            latency_ms REAL DEFAULT 0,
            metadata TEXT DEFAULT '{}',
            created_at REAL NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_inference_system
            ON inference_log(system_id, timestamp);

        CREATE TABLE IF NOT EXISTS classification_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system_id TEXT NOT NULL REFERENCES ai_systems(system_id),
            risk_level TEXT NOT NULL,
            category_id TEXT,
            confidence REAL,
            matched_signals TEXT,
            rationale TEXT,
            classified_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS drift_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system_id TEXT NOT NULL REFERENCES ai_systems(system_id),
            severity TEXT NOT NULL,
            signals TEXT NOT NULL,
            summary TEXT,
            detected_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            system_id TEXT NOT NULL REFERENCES ai_systems(system_id),
            doc_type TEXT NOT NULL DEFAULT 'annex_iv',
            content TEXT NOT NULL,
            generated_at REAL NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def save_system(system: AISystem, db_path: Path = DEFAULT_DB_PATH) -> None:
    conn = _get_connection(db_path)
    now = time.time()
    conn.execute(
        """INSERT OR REPLACE INTO ai_systems
        (system_id, name, description, model_type, framework, version,
         purpose, risk_level, risk_category, risk_rationale,
         human_oversight_required, human_oversight_contact,
         tags, registered_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            system.system_id, system.name, system.description,
            system.model_type, system.framework, system.version,
            system.purpose, system.risk_level.value,
            system.risk_category, system.risk_rationale,
            int(system.human_oversight_required),
            system.human_oversight_contact,
            json.dumps(system.tags),
            system.registered_at, now,
        ),
    )
    conn.commit()
    conn.close()


def save_inference_batch(
    system_id: str,
    records: list[InferenceRecord],
    db_path: Path = DEFAULT_DB_PATH,
) -> int:
    if not records:
        return 0
    conn = _get_connection(db_path)
    now = time.time()
    rows = [
        (
            system_id, r.timestamp,
            str(r.input_shape) if r.input_shape else None,
            r.input_dtype,
            str(r.output_shape) if r.output_shape else None,
            json.dumps(r.output_summary) if r.output_summary else None,
            r.confidence, r.latency_ms,
            json.dumps(r.metadata) if r.metadata else "{}",
            now,
        )
        for r in records
    ]
    conn.executemany(
        """INSERT INTO inference_log
        (system_id, timestamp, input_shape, input_dtype, output_shape,
         output_summary, confidence, latency_ms, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()
    count = len(rows)
    conn.close()
    return count


def save_document(
    system_id: str,
    content: str,
    doc_type: str = "annex_iv",
    db_path: Path = DEFAULT_DB_PATH,
) -> None:
    conn = _get_connection(db_path)
    conn.execute(
        "INSERT INTO documents (system_id, doc_type, content, generated_at) VALUES (?, ?, ?, ?)",
        (system_id, doc_type, content, time.time()),
    )
    conn.commit()
    conn.close()


def get_system_count(db_path: Path = DEFAULT_DB_PATH) -> int:
    conn = _get_connection(db_path)
    row = conn.execute("SELECT COUNT(*) FROM ai_systems").fetchone()
    conn.close()
    return row[0] if row else 0


def get_inference_count(system_id: str, db_path: Path = DEFAULT_DB_PATH) -> int:
    conn = _get_connection(db_path)
    row = conn.execute(
        "SELECT COUNT(*) FROM inference_log WHERE system_id = ?", (system_id,)
    ).fetchone()
    conn.close()
    return row[0] if row else 0
