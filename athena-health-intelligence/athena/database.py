"""SQLite persistence for canonical health records.

Schema versioning uses PRAGMA user_version rather than a migrations
framework — there is exactly one schema so far (SCHEMA_VERSION = 1).
When a second version exists, add a numbered _migrate_to_N function and
apply them in order in `_migrate()`. This keeps the "clear schema
version strategy" the spec asks for without pulling in a migrations
dependency for a single-table database.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

from athena.models.canonical import CanonicalHealthRecord

SCHEMA_VERSION = 1

_LIST_FIELDS = {"validation_messages", "transformations", "tags"}
_JSON_VALUE_FIELDS = {"original_value", "normalized_value"}

_CREATE_RECORDS_TABLE = """
CREATE TABLE IF NOT EXISTS canonical_records (
    id TEXT PRIMARY KEY,
    metric_type TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    timezone TEXT NOT NULL,
    original_value TEXT,
    original_value_type TEXT NOT NULL,
    original_unit TEXT,
    normalized_value TEXT,
    normalized_value_type TEXT NOT NULL,
    normalized_unit TEXT,
    source_platform TEXT NOT NULL,
    source_application TEXT,
    source_device TEXT,
    source_record_id TEXT,
    extraction_method TEXT NOT NULL,
    measurement_type TEXT NOT NULL,
    validation_status TEXT NOT NULL,
    confidence REAL NOT NULL,
    validation_messages TEXT NOT NULL,
    raw_source_path TEXT,
    imported_at TEXT NOT NULL,
    transformation_version TEXT NOT NULL,
    transformations TEXT NOT NULL,
    duplicate_status TEXT,
    duplicate_of TEXT,
    tags TEXT NOT NULL,
    import_batch_id TEXT
);
"""

_CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_records_metric_type ON canonical_records(metric_type);",
    "CREATE INDEX IF NOT EXISTS idx_records_start_time ON canonical_records(start_time);",
    "CREATE INDEX IF NOT EXISTS idx_records_batch ON canonical_records(import_batch_id);",
]


def _encode_value(value):
    """original_value/normalized_value are float | str | dict | None.
    Store the JSON text plus a type tag so decoding is lossless
    (e.g. the string "12" and the float 12.0 must round-trip distinctly).
    """
    if value is None:
        return None, "null"
    if isinstance(value, bool):
        return json.dumps(value), "bool"
    if isinstance(value, (int, float)):
        return json.dumps(value), "number"
    if isinstance(value, dict):
        return json.dumps(value), "dict"
    return json.dumps(value), "str"


def _decode_value(text, value_type):
    if value_type == "null" or text is None:
        return None
    return json.loads(text)


class Database:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(_CREATE_RECORDS_TABLE)
            for stmt in _CREATE_INDEXES:
                conn.execute(stmt)
            current_version = conn.execute("PRAGMA user_version").fetchone()[0]
            if current_version < SCHEMA_VERSION:
                conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")

    def schema_version(self) -> int:
        with self._connect() as conn:
            return conn.execute("PRAGMA user_version").fetchone()[0]

    def insert_record(self, record: CanonicalHealthRecord) -> None:
        ov_text, ov_type = _encode_value(record.original_value)
        nv_text, nv_type = _encode_value(record.normalized_value)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO canonical_records (
                    id, metric_type, start_time, end_time, timezone,
                    original_value, original_value_type, original_unit,
                    normalized_value, normalized_value_type, normalized_unit,
                    source_platform, source_application, source_device, source_record_id,
                    extraction_method, measurement_type, validation_status, confidence,
                    validation_messages, raw_source_path, imported_at,
                    transformation_version, transformations,
                    duplicate_status, duplicate_of, tags, import_batch_id
                ) VALUES (?,?,?,?,?, ?,?,?, ?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?, ?,?, ?,?,?,?)
                """,
                (
                    record.id,
                    record.metric_type,
                    record.start_time.isoformat(),
                    record.end_time.isoformat() if record.end_time else None,
                    record.timezone,
                    ov_text,
                    ov_type,
                    record.original_unit,
                    nv_text,
                    nv_type,
                    record.normalized_unit,
                    record.source_platform,
                    record.source_application,
                    record.source_device,
                    record.source_record_id,
                    record.extraction_method,
                    record.measurement_type,
                    record.validation_status,
                    record.confidence,
                    json.dumps(record.validation_messages),
                    record.raw_source_path,
                    record.imported_at.isoformat(),
                    record.transformation_version,
                    json.dumps(record.transformations),
                    record.duplicate_status,
                    record.duplicate_of,
                    json.dumps(record.tags),
                    record.import_batch_id,
                ),
            )

    def _row_to_record(self, row: sqlite3.Row) -> CanonicalHealthRecord:
        data = dict(row)
        original_value = _decode_value(data.pop("original_value"), data.pop("original_value_type"))
        normalized_value = _decode_value(data.pop("normalized_value"), data.pop("normalized_value_type"))
        return CanonicalHealthRecord(
            **{
                **data,
                "original_value": original_value,
                "normalized_value": normalized_value,
                "validation_messages": json.loads(data["validation_messages"]),
                "transformations": json.loads(data["transformations"]),
                "tags": json.loads(data["tags"]),
            }
        )

    def get_record(self, record_id: str) -> CanonicalHealthRecord | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM canonical_records WHERE id = ?", (record_id,)).fetchone()
            return self._row_to_record(row) if row else None

    def list_records(
        self,
        *,
        metric_type: str | None = None,
        import_batch_id: str | None = None,
        source_record_id: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        exclude_duplicates: bool = False,
    ) -> list[CanonicalHealthRecord]:
        clauses = []
        params: list = []
        if metric_type is not None:
            clauses.append("metric_type = ?")
            params.append(metric_type)
        if import_batch_id is not None:
            clauses.append("import_batch_id = ?")
            params.append(import_batch_id)
        if source_record_id is not None:
            clauses.append("source_record_id = ?")
            params.append(source_record_id)
        if start_date is not None:
            clauses.append("start_time >= ?")
            params.append(start_date.isoformat())
        if end_date is not None:
            clauses.append("start_time <= ?")
            params.append(end_date.isoformat())
        if exclude_duplicates:
            clauses.append("(duplicate_status IS NULL OR duplicate_status != 'duplicate')")
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM canonical_records {where} ORDER BY start_time ASC", params
            ).fetchall()
            return [self._row_to_record(r) for r in rows]

    def update_validation(
        self, record_id: str, *, validation_status: str, confidence: float, validation_messages: list[str]
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE canonical_records SET validation_status = ?, confidence = ?, validation_messages = ? WHERE id = ?",
                (validation_status, confidence, json.dumps(validation_messages), record_id),
            )

    def mark_duplicate(self, record_id: str, *, duplicate_status: str, duplicate_of: str | None) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE canonical_records SET duplicate_status = ?, duplicate_of = ? WHERE id = ?",
                (duplicate_status, duplicate_of, record_id),
            )

    def count_records(self) -> int:
        with self._connect() as conn:
            return conn.execute("SELECT COUNT(*) FROM canonical_records").fetchone()[0]
