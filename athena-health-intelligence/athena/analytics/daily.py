"""Daily summary: what was recorded for one date, grouped by metric, with
data-quality issues surfaced separately from clean measurements — never
blended together as if all were equally trustworthy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from athena.database import Database
from athena.models.canonical import CanonicalHealthRecord


@dataclass
class DailySummary:
    date: date
    records_by_metric: dict[str, list[CanonicalHealthRecord]] = field(default_factory=dict)
    quality_warnings: list[CanonicalHealthRecord] = field(default_factory=list)

    @property
    def total_records(self) -> int:
        return sum(len(v) for v in self.records_by_metric.values())


def summarize_daily(db: Database, target_date: date) -> DailySummary:
    # "Daily" means the local wall-clock date each record's own start_time
    # carries — comparing .date() per-record avoids cross-record
    # naive/aware datetime comparison pitfalls entirely.
    records = [r for r in db.list_records(exclude_duplicates=True) if r.start_time.date() == target_date]

    summary = DailySummary(date=target_date)
    for r in records:
        summary.records_by_metric.setdefault(r.metric_type, []).append(r)
        if r.validation_status in ("questionable", "invalid"):
            summary.quality_warnings.append(r)
    return summary
