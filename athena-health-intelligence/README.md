# ATHENA — Health Intelligence Bridge

Local-first, source-traceable health intelligence pipeline for the Alpha Proxima /
LUMIAION ecosystem.

```
Health data file or manual input
        ↓
Validation
        ↓
Canonical ATHENA health schema
        ↓
Local SQLite database
        ↓
Deduplication and provenance
        ↓
Obsidian-compatible Markdown output
```

**Start here:** [`docs/audit/AUDIT_REPORT.md`](docs/audit/AUDIT_REPORT.md) — what actually
exists, what's blocked, and why. Then [`docs/architecture.md`](docs/architecture.md) and
[`docs/data-model.md`](docs/data-model.md) for how it works.

## Quickstart (synthetic data — no real health data required)

```bash
python3 -m venv .venv
./.venv/bin/pip install -e ".[dev]"

export ATHENA_HOME=/tmp/athena-demo   # or any directory you want ATHENA to own
./.venv/bin/athena init
./.venv/bin/athena import manual --from-json tests/fixtures/manual_record.json
./.venv/bin/athena validate
./.venv/bin/athena export obsidian
./.venv/bin/athena summarize daily 2026-07-29
./.venv/bin/athena doctor
```

## Run the tests

```bash
./.venv/bin/pytest -q
```

## Rules this codebase enforces

1. **Never fabricate a health value.** Missing stays missing; uncertain is marked
   uncertain. See `athena/importers/manual.py`'s handling of a null `value`.
2. **Never silently "fix" a suspicious value.** `athena/validation/consistency.py` flags
   skeletal-muscle-mass-exceeds-body-weight and similar patterns; it never corrects them.
3. **Raw source files are immutable.** Every import copies its source into
   `data/raw/<batch_id>/` and hashes it (`athena/security/audit_log.py`); nothing writes
   to that copy again.
4. **Every record carries provenance.** See `docs/data-model.md`.
5. **No medical diagnosis.** `athena/analytics/readiness.py` is an explicit
   `NotImplementedError` stub rather than a fabricated scoring formula.

## What's functional vs. documented-only

See the implementation-status matrix in
[`docs/audit/AUDIT_REPORT.md`](docs/audit/AUDIT_REPORT.md). In short: manual/JSON/CSV/Evolt
(structured) import → validation → SQLite → deduplication → Obsidian export is functional
and tested end-to-end. Samsung Health, SmartHealth, and Strava are not implemented — see
[`docs/source-capabilities.md`](docs/source-capabilities.md) for what's actually confirmed
about each.
