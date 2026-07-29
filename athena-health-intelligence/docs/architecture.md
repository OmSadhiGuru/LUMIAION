# ATHENA Architecture

## Pipeline

```
Health data file or manual input
        ↓
Importer (manual / json / csv / evolt / health_connect)
        ↓  — preserves raw source file immutably in data/raw/
Validation (ranges → consistency → anomalies)
        ↓  — flags, never silently corrects
Canonical ATHENA health schema (CanonicalHealthRecord)
        ↓
SQLite (data/athena.db)
        ↓
Deduplication (flag-only, never deletes)
        ↓
Obsidian-compatible Markdown export (vault/ATHENA/)
```

This is the same pipeline described in the master spec, section 2. It runs end-to-end
today via `athena init && athena import manual && athena validate && athena export
obsidian && athena summarize daily <date>` (see `tests/integration/test_cli_workflow.py`).

## Package layout

```
athena/
├── cli.py            — argparse-based CLI, one function per subcommand
├── config.py          — AthenaConfig: resolves ATHENA_HOME to data/vault paths
├── database.py         — SQLite persistence for CanonicalHealthRecord
├── models/              — CanonicalHealthRecord, provenance, metric registry, vocab
├── importers/            — file/manual-entry importers (Importer ABC)
├── adapters/               — pull-based external API adapters (HealthSourceAdapter ABC);
│                              currently only the Strava interface stub
├── validation/              — ranges.py, consistency.py, anomalies.py, engine.py
├── deduplication/            — engine.py + pluggable strategies.py
├── analytics/                  — daily.py, weekly.py, trends.py, readiness.py (stub)
├── exporters/                   — obsidian.py, json_export.py
└── security/                     — secrets.py (env-only), audit_log.py (JSONL + hashing)
```

`Importer` (file/manual input) and `HealthSourceAdapter` (pull-based external API) are
deliberately separate base classes in `athena/importers/base.py` — an importer reads
something local and finishes; an adapter authenticates and can be called repeatedly. Only
`StravaAdapter` uses the latter today, and it is unimplemented (see
`athena/adapters/strava.py`).

## Design decisions and why

- **Provenance fields are flat on `CanonicalHealthRecord`, not nested.** This matches the
  master spec's literal class definition and means every provenance field is a real SQLite
  column that can be filtered on directly, rather than requiring JSON path queries into a
  nested blob. See `docs/data-model.md`.
- **Validation is a separate, deterministic pass, not a pydantic validator on the model.**
  `CanonicalHealthRecord` only enforces structural validity (types, required fields).
  Physiological plausibility lives in `athena/validation/` and runs as an explicit step
  (`athena validate`) so a record can exist in an "unverified" or "questionable" state
  without ever being rejected outright — per spec 3.1, "if a value is uncertain, mark it
  as uncertain," not "refuse to store it."
- **Confidence is a coarse, capped score, not a statistical model.** See
  `athena/validation/engine.py`'s module docstring for the exact rule. The intent is that
  adding a new check can only make ATHENA more conservative, never less.
- **Deduplication tags, never deletes or merges.** `duplicate_status`/`duplicate_of` are
  set; the underlying record is untouched. Default queries exclude duplicates
  (`exclude_duplicates=True`) but nothing is destroyed, matching spec 3.3's "raw source
  data must be immutable" spirit extended to derived records too.
- **Readiness scoring is an explicit stub, not a placeholder formula.**
  `athena/analytics/readiness.py` raises `NotImplementedError` with an explanation rather
  than shipping a plausible-looking weighted score with no validated basis — see its
  module docstring and spec rule 3.5 ("no medical diagnosis").

## What is genuinely not built yet

See `docs/audit/AUDIT_REPORT.md`'s implementation-status matrix for the authoritative,
per-component list. In short: Samsung Health and SmartHealth connectors (no code), Strava
OAuth (interface only), Evolt PDF extraction (interface only, raises on `.pdf`), Health
Connect (parses a documented shape but untested against a real device export), encryption,
backup/deletion commands, and the Android companion app.
