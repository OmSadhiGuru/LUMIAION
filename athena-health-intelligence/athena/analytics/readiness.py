"""Readiness scoring is intentionally NOT implemented.

The master spec lists readiness scoring as a planned feature, but no
validated methodology has been defined or reviewed, and ATHENA rule 3.5
("No medical diagnosis") plus rule 3.1 ("never fabricate") make an
off-the-cuff scoring formula (some weighted blend of HRV/sleep/soreness)
exactly the kind of thing this project exists to avoid: a number that
*looks* authoritative but isn't grounded in anything verified.

This stays a stub — raising rather than silently returning a plausible-
looking score — until a real methodology is designed, documented in
docs/data-model.md, and reviewed. Status: NOT STARTED (see
docs/audit/AUDIT_REPORT.md implementation-status matrix).
"""

from __future__ import annotations

from datetime import date

from athena.database import Database


def compute_readiness(db: Database, target_date: date) -> None:
    raise NotImplementedError(
        "Readiness scoring is not implemented. No validated scoring methodology exists yet — "
        "see athena/analytics/readiness.py module docstring and docs/audit/AUDIT_REPORT.md."
    )
