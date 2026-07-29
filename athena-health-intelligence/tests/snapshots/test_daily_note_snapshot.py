"""Snapshot test: the daily note structure (section headers, measurement
line format) must stay stable since Obsidian references/queries may
depend on it. Timestamps and ids are stripped before comparison since
those are expected to vary.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from athena.analytics.daily import summarize_daily
from athena.exporters.obsidian import write_daily_note
from athena.importers.manual import ManualImporter

SNAPSHOT_PATH = Path(__file__).parent / "daily_note.snapshot.md"


def _normalize(text: str) -> str:
    text = re.sub(r"generated_at: .*", "generated_at: <TIMESTAMP>", text)
    text = re.sub(r"record_ids: \[.*\]", "record_ids: [<IDS>]", text)
    text = re.sub(r"`[0-9a-f-]{36}`", "`<ID>`", text)
    return text


def test_daily_note_matches_snapshot(config, db):
    result = ManualImporter(config).import_record(
        {
            "metric_type": "body_weight_kg",
            "value": 81.2,
            "unit": "kg",
            "start_time": "2026-07-29T07:00:00-04:00",
            "timezone": "America/New_York",
            "measurement_type": "manual",
        }
    )
    for r in result.records:
        r.validation_status = "valid"
        r.confidence = 0.6
        db.insert_record(r)

    summary = summarize_daily(db, date(2026, 7, 29))
    path = write_daily_note(config, summary)

    actual = _normalize(path.read_text())

    if not SNAPSHOT_PATH.exists():
        SNAPSHOT_PATH.write_text(actual, encoding="utf-8")

    expected = _normalize(SNAPSHOT_PATH.read_text())
    assert actual == expected
