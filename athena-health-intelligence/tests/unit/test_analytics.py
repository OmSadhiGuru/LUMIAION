from __future__ import annotations

from datetime import date

import pytest

from athena.analytics.readiness import compute_readiness
from athena.analytics.trends import compute_trend
from athena.analytics.weekly import InvalidWeekFormatError, parse_iso_week, summarize_weekly
from athena.importers.json_importer import JsonImporter


def test_summarize_weekly_computes_average_and_trend(config, db, fixtures_dir):
    result = JsonImporter(config).import_source(fixtures_dir / "records_batch.json")
    for r in result.records:
        db.insert_record(r)

    # 2026-07-22 and 2026-07-25 both fall in ISO week 2026-W30
    year, week = parse_iso_week("2026-W30")
    assert (year, week) == (2026, 30)

    summary = summarize_weekly(db, "2026-W30")
    assert "body_weight_kg" in summary.averages_by_metric
    assert summary.counts_by_metric["body_weight_kg"] == 2
    assert summary.quality_warning_count == 0  # validation hasn't run yet; unverified isn't a warning tier


def test_invalid_week_format_raises():
    with pytest.raises(InvalidWeekFormatError):
        parse_iso_week("not-a-week")


def test_compute_trend_flat_within_threshold():
    trend = compute_trend(80.0, 80.5)
    assert trend.direction == "flat"


def test_compute_trend_up():
    trend = compute_trend(80.0, 85.0)
    assert trend.direction == "up"


def test_compute_trend_insufficient_data():
    trend = compute_trend(None, 80.0)
    assert trend.direction == "insufficient_data"


def test_readiness_scoring_explicitly_not_implemented(config, db):
    with pytest.raises(NotImplementedError):
        compute_readiness(db, date(2026, 7, 29))
