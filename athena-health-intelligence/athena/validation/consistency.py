"""Cross-field consistency checks — the checks this project exists for.

These directly implement the ATHENA rule 3.2 examples: skeletal muscle
mass near/above total body weight, lean mass greater than body weight,
implausible total body water, and calorie/macro mismatches. Every
finding is a flag for review, never a silent correction — nothing here
mutates original_value or normalized_value.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena.models.canonical import CanonicalHealthRecord

CALORIE_TOLERANCE_FRACTION = 0.15  # configurable tolerance, per spec section 7
BODY_COMP_TOLERANCE_FRACTION = 0.12


@dataclass
class ConsistencyFinding:
    check: str
    metric_types: list[str] = field(default_factory=list)
    severity: str = "questionable"  # "questionable" | "invalid"
    detail: str = ""

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.check}: {self.detail}"


def check_calorie_reconciliation(
    protein_g: float | None,
    carbohydrate_g: float | None,
    fat_g: float | None,
    total_kcal: float | None,
    tolerance: float = CALORIE_TOLERANCE_FRACTION,
) -> ConsistencyFinding | None:
    if None in (protein_g, carbohydrate_g, fat_g, total_kcal) or total_kcal == 0:
        return None
    computed = protein_g * 4 + carbohydrate_g * 4 + fat_g * 9
    delta = abs(computed - total_kcal) / total_kcal
    if delta > tolerance:
        return ConsistencyFinding(
            check="calorie_reconciliation",
            metric_types=["protein_g", "carbohydrate_g", "fat_g", "calories_kcal"],
            severity="questionable",
            detail=(
                f"macros imply {computed:.0f} kcal but total_kcal is {total_kcal:.0f} "
                f"({delta:.0%} off, tolerance {tolerance:.0%}) — flagged for review, not corrected"
            ),
        )
    return None


def check_sleep_stages(
    session_duration_minutes: float | None,
    stage_minutes: dict[str, float | None],
    tolerance: float = 0.10,
) -> ConsistencyFinding | None:
    known = {k: v for k, v in stage_minutes.items() if v is not None}
    if session_duration_minutes is None or not known:
        return None
    if any(v < 0 for v in known.values()) or session_duration_minutes < 0:
        return ConsistencyFinding(
            check="sleep_stage_negative_duration",
            metric_types=list(known.keys()) + ["sleep_session_duration_minutes"],
            severity="invalid",
            detail="negative sleep duration is not physically possible",
        )
    stage_sum = sum(known.values())
    delta = abs(stage_sum - session_duration_minutes) / max(session_duration_minutes, 1)
    if delta > tolerance:
        return ConsistencyFinding(
            check="sleep_stage_sum_mismatch",
            metric_types=list(known.keys()) + ["sleep_session_duration_minutes"],
            severity="questionable",
            detail=(
                f"sleep stages sum to {stage_sum:.0f} min but session duration is "
                f"{session_duration_minutes:.0f} min ({delta:.0%} off)"
            ),
        )
    return None


def _latest_value(records: list[CanonicalHealthRecord], metric_type: str) -> float | None:
    matches = [r for r in records if r.metric_type == metric_type and isinstance(r.normalized_value, (int, float))]
    if not matches:
        return None
    return matches[-1].normalized_value


def check_body_composition_group(records: list[CanonicalHealthRecord]) -> list[ConsistencyFinding]:
    """Run cross-field checks over one scan's worth of records (records
    sharing a source_record_id / import_batch_id). Order matches the
    ATHENA rule 3.2 examples.
    """
    findings: list[ConsistencyFinding] = []

    weight = _latest_value(records, "body_weight_kg")
    smm = _latest_value(records, "skeletal_muscle_mass_kg")
    lbm = _latest_value(records, "lean_body_mass_kg")
    body_fat_pct = _latest_value(records, "body_fat_percent")
    tbw_pct = _latest_value(records, "total_body_water_percent")

    if weight is not None and smm is not None and smm >= weight:
        findings.append(
            ConsistencyFinding(
                check="skeletal_muscle_exceeds_weight",
                metric_types=["skeletal_muscle_mass_kg", "body_weight_kg"],
                severity="invalid",
                detail=(
                    f"skeletal_muscle_mass_kg ({smm}) is >= body_weight_kg ({weight}) — "
                    f"physiologically impossible, likely field mapping or extraction error"
                ),
            )
        )

    if weight is not None and lbm is not None and lbm > weight:
        findings.append(
            ConsistencyFinding(
                check="lean_mass_exceeds_weight",
                metric_types=["lean_body_mass_kg", "body_weight_kg"],
                severity="invalid",
                detail=f"lean_body_mass_kg ({lbm}) exceeds body_weight_kg ({weight})",
            )
        )

    if smm is not None and lbm is not None and smm > lbm:
        findings.append(
            ConsistencyFinding(
                check="skeletal_muscle_exceeds_lean_mass",
                metric_types=["skeletal_muscle_mass_kg", "lean_body_mass_kg"],
                severity="invalid",
                detail=(
                    f"skeletal_muscle_mass_kg ({smm}) exceeds lean_body_mass_kg ({lbm}) — "
                    f"skeletal muscle is a subset of lean mass; these may be swapped in extraction"
                ),
            )
        )

    if weight is not None and lbm is not None and body_fat_pct is not None:
        implied_fat_mass = weight * (body_fat_pct / 100.0)
        implied_total = lbm + implied_fat_mass
        delta = abs(implied_total - weight) / weight
        if delta > BODY_COMP_TOLERANCE_FRACTION:
            findings.append(
                ConsistencyFinding(
                    check="lean_plus_fat_vs_weight_mismatch",
                    metric_types=["lean_body_mass_kg", "body_fat_percent", "body_weight_kg"],
                    severity="questionable",
                    detail=(
                        f"lean_body_mass_kg ({lbm}) + implied fat mass ({implied_fat_mass:.1f}) = "
                        f"{implied_total:.1f}, which is {delta:.0%} off body_weight_kg ({weight})"
                    ),
                )
            )

    if tbw_pct is not None and not (20 <= tbw_pct <= 80):
        findings.append(
            ConsistencyFinding(
                check="total_body_water_implausible",
                metric_types=["total_body_water_percent"],
                severity="invalid",
                detail=f"total_body_water_percent ({tbw_pct}) is outside physiologically possible range [20, 80]",
            )
        )

    return findings
