"""Obsidian Markdown exporter.

Every generated note keeps four things visibly separate, per the
ATHENA rule: measurements, derived calculations, ATHENA interpretations,
and data-quality warnings. There are no "ATHENA interpretations" yet
(no readiness scoring, no AI narrative) — that section is omitted
rather than filled with something invented. Every measurement line
carries its record id and validation_status so nothing uncertain reads
as confirmed.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from athena.analytics.daily import DailySummary
from athena.analytics.weekly import WeeklySummary
from athena.config import AthenaConfig
from athena.database import Database
from athena.models.canonical import CanonicalHealthRecord


def _frontmatter(fields: dict) -> str:
    lines = ["---"]
    for k, v in fields.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def _measurement_line(r: CanonicalHealthRecord) -> str:
    status_flag = "" if r.validation_status == "valid" else f" ⚠️ {r.validation_status.upper()}"
    return (
        f"- **{r.metric_type}**: {r.normalized_value} {r.normalized_unit or ''} "
        f"({r.measurement_type}, confidence {r.confidence:.2f}){status_flag} "
        f"— `{r.id}` from `{r.source_platform}`"
    )


def write_daily_note(config: AthenaConfig, summary: DailySummary) -> Path:
    out_dir = config.vault_subdir("05-DAILY-NOTES")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{summary.date.isoformat()}.md"

    record_ids = [r.id for records in summary.records_by_metric.values() for r in records]
    frontmatter = _frontmatter(
        {
            "date": summary.date.isoformat(),
            "type": "athena-daily-note",
            "record_count": summary.total_records,
            "generated_at": datetime.now().isoformat(),
            "record_ids": "[" + ", ".join(record_ids) + "]",
        }
    )

    lines = [frontmatter, "", f"# Daily Note — {summary.date.isoformat()}", ""]

    lines += ["## Measurements", ""]
    if summary.records_by_metric:
        for metric_type in sorted(summary.records_by_metric):
            for r in summary.records_by_metric[metric_type]:
                lines.append(_measurement_line(r))
    else:
        lines.append("_No records for this date._")
    lines.append("")

    lines += ["## Data Quality Warnings", ""]
    if summary.quality_warnings:
        for r in summary.quality_warnings:
            lines.append(f"- **{r.metric_type}** (`{r.id}`): {r.validation_status.upper()}")
            for msg in r.validation_messages:
                lines.append(f"  - {msg}")
    else:
        lines.append("_None._")
    lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_weekly_review(config: AthenaConfig, summary: WeeklySummary) -> Path:
    out_dir = config.vault_subdir("06-WEEKLY-REVIEWS")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{summary.week}.md"

    frontmatter = _frontmatter(
        {
            "week": summary.week,
            "type": "athena-weekly-review",
            "start_date": summary.start_date.isoformat(),
            "end_date": summary.end_date.isoformat(),
            "generated_at": datetime.now().isoformat(),
        }
    )
    lines = [frontmatter, "", f"# Weekly Review — {summary.week}", ""]

    lines += ["## Metric Averages", ""]
    if summary.averages_by_metric:
        lines.append("| Metric | Average | Records | Trend vs. prior week |")
        lines.append("|---|---|---|---|")
        for metric_type in sorted(summary.averages_by_metric):
            trend = summary.trends_by_metric.get(metric_type)
            trend_str = trend.direction if trend else "n/a"
            lines.append(
                f"| {metric_type} | {summary.averages_by_metric[metric_type]} "
                f"| {summary.counts_by_metric[metric_type]} | {trend_str} |"
            )
    else:
        lines.append("_No records for this week._")
    lines.append("")

    lines += ["## Data Quality", "", f"{summary.quality_warning_count} record(s) flagged questionable/invalid this week.", ""]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_body_scan_note(config: AthenaConfig, records: list[CanonicalHealthRecord], scan_id: str) -> Path:
    out_dir = config.vault_subdir("08-BODY-SCANS")
    out_dir.mkdir(parents=True, exist_ok=True)
    scan_date = records[0].start_time.date().isoformat() if records else "unknown-date"
    path = out_dir / f"{scan_date}-{scan_id}.md"

    frontmatter = _frontmatter(
        {
            "scan_id": scan_id,
            "type": "athena-body-scan",
            "source_platform": records[0].source_platform if records else "unknown",
            "generated_at": datetime.now().isoformat(),
        }
    )
    lines = [frontmatter, "", f"# Body Scan — {scan_id}", ""]
    for r in records:
        lines.append(_measurement_line(r))
    lines.append("")
    lines.append(
        "_This note reflects device-estimated values. See the corresponding "
        "17-IMPORT-LOGS/evolt-import-review-*.md file before treating any value here as confirmed._"
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def export_daily_notes_for_all_dates(config: AthenaConfig, db: Database) -> list[Path]:
    """Golden-path entry point for `athena export obsidian`: writes one
    daily note per distinct date present in the database.
    """
    from athena.analytics.daily import summarize_daily

    dates = sorted({r.start_time.date() for r in db.list_records()})
    return [write_daily_note(config, summarize_daily(db, d)) for d in dates]
