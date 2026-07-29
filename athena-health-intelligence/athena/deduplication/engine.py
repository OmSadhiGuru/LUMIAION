"""Deduplication engine.

Never deletes or merges records — duplicates are tagged
(duplicate_status="duplicate", duplicate_of=<original id>) and excluded
from default queries/exports via Database.list_records(exclude_duplicates=True).
The original is left untouched (duplicate_status="unique").
"""

from __future__ import annotations

from athena.database import Database
from athena.deduplication.strategies import DedupStrategy, TimeWindowValueStrategy


def deduplicate(db: Database, *, strategy: DedupStrategy | None = None) -> dict:
    strategy = strategy or TimeWindowValueStrategy()
    all_records = db.list_records()

    by_metric: dict[str, list] = {}
    for r in sorted(all_records, key=lambda r: r.start_time):
        by_metric.setdefault(r.metric_type, []).append(r)

    duplicates_found = 0
    for metric_type, records in by_metric.items():
        confirmed_unique: list = []
        for record in records:
            if record.duplicate_status == "duplicate":
                continue
            match = strategy.find_duplicate(record, confirmed_unique)
            if match is not None:
                db.mark_duplicate(record.id, duplicate_status="duplicate", duplicate_of=match.id)
                duplicates_found += 1
            else:
                if record.duplicate_status != "unique":
                    db.mark_duplicate(record.id, duplicate_status="unique", duplicate_of=None)
                confirmed_unique.append(record)

    return {"records_scanned": len(all_records), "duplicates_found": duplicates_found}
