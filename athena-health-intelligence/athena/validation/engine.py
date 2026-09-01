"""Validation orchestration: deterministic checks only, run before any
AI interpretation (per ATHENA rule "Implement deterministic validation
before any AI interpretation" — there is no AI interpretation step in
this codebase yet, so this is the only validation ATHENA performs).

Confidence is a coarse, explainable score — not a statistical model:
    1.0 baseline for measured values with no findings
    0.8 baseline for device_estimated / calculated with no findings
    0.5 for manual/unverified with no findings
    any "questionable" finding caps confidence at 0.4
    any "invalid" finding caps confidence at 0.1
The cap-based approach means adding a new check can only ever make
confidence more conservative, never less — a change here cannot
silently make ATHENA more trusting of bad data.
"""

from __future__ import annotations

from itertools import groupby

from athena.database import Database
from athena.models.canonical import CanonicalHealthRecord
from athena.validation.anomalies import check_anomaly
from athena.validation.consistency import check_body_composition_group, check_calorie_reconciliation, check_sleep_stages
from athena.validation.ranges import check_range

_BASELINE_BY_MEASUREMENT_TYPE = {
    "measured": 1.0,
    "device_estimated": 0.8,
    "calculated": 0.8,
    "manual": 0.6,
    "inferred": 0.4,
    "unverified": 0.3,
}


def _apply_finding(record: CanonicalHealthRecord, severity: str, detail: str) -> None:
    record.validation_messages.append(f"[{severity.upper()}] {detail}")
    severity_rank = {"valid": 0, "unverified": 1, "questionable": 2, "invalid": 3}
    if severity_rank.get(severity, 0) > severity_rank.get(record.validation_status, 0):
        record.validation_status = severity


def validate_record(
    record: CanonicalHealthRecord,
    *,
    recent_values: list[float] | None = None,
) -> CanonicalHealthRecord:
    """Run range + anomaly checks on a single record in isolation. Group
    (cross-field) checks are run separately by validate_records because
    they need sibling records. Mutates and returns the same record.
    """
    record.validation_status = "valid"

    range_result = check_range(record.metric_type, record.normalized_value)
    if range_result is not None:
        _apply_finding(record, range_result.severity, range_result.detail)

    if recent_values and isinstance(record.normalized_value, (int, float)):
        anomaly = check_anomaly(record.metric_type, record.normalized_value, recent_values)
        if anomaly is not None:
            _apply_finding(record, anomaly.severity, anomaly.detail)

    baseline = _BASELINE_BY_MEASUREMENT_TYPE.get(record.measurement_type, 0.3)
    if record.validation_status == "invalid":
        record.confidence = min(record.confidence, 0.1) if record.confidence else 0.1
    elif record.validation_status == "questionable":
        record.confidence = 0.4
    elif record.validation_status == "valid":
        record.confidence = baseline
    else:
        record.confidence = min(baseline, 0.5)

    return record


def _apply_group_findings(records: list[CanonicalHealthRecord], findings) -> None:
    for finding in findings:
        for record in records:
            if record.metric_type in finding.metric_types:
                _apply_finding(record, finding.severity, finding.detail)
                if finding.severity == "invalid":
                    record.confidence = 0.1
                elif finding.severity == "questionable" and record.confidence > 0.4:
                    record.confidence = 0.4


def validate_records(db: Database, *, batch_id: str | None = None) -> dict:
    """Validate every record in the database (or just one import batch),
    including cross-field checks within each import batch, then persist
    the results. Returns a summary count by validation_status.
    """
    records = db.list_records(import_batch_id=batch_id) if batch_id else db.list_records()

    history_by_metric: dict[str, list[float]] = {}
    for r in sorted(records, key=lambda r: r.start_time):
        recent = history_by_metric.get(r.metric_type, [])
        validate_record(r, recent_values=recent[-10:] if recent else None)
        if isinstance(r.normalized_value, (int, float)):
            recent.append(r.normalized_value)
            history_by_metric[r.metric_type] = recent

    records_sorted = sorted(records, key=lambda r: r.import_batch_id or "")
    for group_batch_id, group_iter in groupby(records_sorted, key=lambda r: r.import_batch_id):
        if not group_batch_id:
            continue
        group = list(group_iter)

        body_findings = check_body_composition_group(group)
        _apply_group_findings(group, body_findings)

        by_metric = {r.metric_type: r.normalized_value for r in group}
        calorie_finding = check_calorie_reconciliation(
            by_metric.get("protein_g"), by_metric.get("carbohydrate_g"), by_metric.get("fat_g"), by_metric.get("calories_kcal")
        )
        if calorie_finding:
            _apply_group_findings(group, [calorie_finding])

        sleep_finding = check_sleep_stages(
            by_metric.get("sleep_session_duration_minutes"),
            {
                "sleep_stage_light_minutes": by_metric.get("sleep_stage_light_minutes"),
                "sleep_stage_deep_minutes": by_metric.get("sleep_stage_deep_minutes"),
                "sleep_stage_rem_minutes": by_metric.get("sleep_stage_rem_minutes"),
                "sleep_stage_awake_minutes": by_metric.get("sleep_stage_awake_minutes"),
            },
        )
        if sleep_finding:
            _apply_group_findings(group, [sleep_finding])

    summary = {"valid": 0, "questionable": 0, "invalid": 0, "unverified": 0}
    for r in records:
        summary[r.validation_status] = summary.get(r.validation_status, 0) + 1
        db.update_validation(
            r.id,
            validation_status=r.validation_status,
            confidence=r.confidence,
            validation_messages=r.validation_messages,
        )
    return summary
