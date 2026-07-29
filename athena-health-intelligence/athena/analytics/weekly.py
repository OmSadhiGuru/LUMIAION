"""Weekly summary: per-metric averages for an ISO week, plus a trend
against the prior ISO week. Week identifiers use ISO 8601 week format,
e.g. "2026-W31".
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta

from athena.analytics.trends import Trend, compute_trend
from athena.database import Database

_WEEK_RE = re.compile(r"^(?P<year>\d{4})-W(?P<week>\d{2})$")


class InvalidWeekFormatError(ValueError):
    pass


def parse_iso_week(week_str: str) -> tuple[int, int]:
    match = _WEEK_RE.match(week_str.strip())
    if not match:
        raise InvalidWeekFormatError(f"expected ISO week format 'YYYY-Www' (e.g. '2026-W31'), got {week_str!r}")
    return int(match.group("year")), int(match.group("week"))


def iso_week_bounds(year: int, week: int) -> tuple[date, date]:
    start = date.fromisocalendar(year, week, 1)
    end = date.fromisocalendar(year, week, 7)
    return start, end


@dataclass
class WeeklySummary:
    week: str
    start_date: date
    end_date: date
    averages_by_metric: dict[str, float] = field(default_factory=dict)
    counts_by_metric: dict[str, int] = field(default_factory=dict)
    trends_by_metric: dict[str, Trend] = field(default_factory=dict)
    quality_warning_count: int = 0


def _week_average(records, metric_type, start_date, end_date) -> tuple[float | None, int]:
    values = [
        r.normalized_value
        for r in records
        if r.metric_type == metric_type
        and isinstance(r.normalized_value, (int, float))
        and start_date <= r.start_time.date() <= end_date
    ]
    if not values:
        return None, 0
    return sum(values) / len(values), len(values)


def summarize_weekly(db: Database, week_str: str) -> WeeklySummary:
    year, week = parse_iso_week(week_str)
    start_date, end_date = iso_week_bounds(year, week)
    prev_start_date = start_date - timedelta(days=7)
    prev_end_date = end_date - timedelta(days=7)

    all_records = db.list_records(exclude_duplicates=True)
    this_week = [r for r in all_records if start_date <= r.start_time.date() <= end_date]

    metric_types = sorted({r.metric_type for r in this_week})
    summary = WeeklySummary(week=week_str, start_date=start_date, end_date=end_date)

    for metric_type in metric_types:
        avg, count = _week_average(all_records, metric_type, start_date, end_date)
        prev_avg, _ = _week_average(all_records, metric_type, prev_start_date, prev_end_date)
        if avg is not None:
            summary.averages_by_metric[metric_type] = round(avg, 3)
            summary.counts_by_metric[metric_type] = count
            summary.trends_by_metric[metric_type] = compute_trend(prev_avg, avg)

    summary.quality_warning_count = sum(1 for r in this_week if r.validation_status in ("questionable", "invalid"))
    return summary
