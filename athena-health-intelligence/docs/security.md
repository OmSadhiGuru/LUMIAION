# ATHENA Security

## What is implemented today

- **`.env` exclusion:** `.gitignore` excludes `.env`; only `.env.example` (no real values)
  is committed. `tests/unit/test_strava_adapter.py::test_no_strava_credentials_in_env_example`
  asserts the example file never carries a real value.
- **Secrets read only from environment variables:** `athena/security/secrets.py::get_secret`
  is the only sanctioned way to read a secret. It never reads from a file or from
  Markdown, and raises rather than returning a default containing a real value.
- **No secrets in Markdown:** the Obsidian exporter (`athena/exporters/obsidian.py`) only
  ever writes measurement values, ids, and validation state — it has no code path that
  touches `athena/security/secrets.py`.
- **No tokens in logs:** the audit log (`athena/security/audit_log.py`) records action
  names, target ids, and small JSON `detail` dicts built explicitly by CLI commands — none
  of which include secret values, since none of the current commands handle secrets.
- **Local database:** `data/athena.db` is a local SQLite file, never uploaded anywhere by
  this codebase.
- **Raw-file integrity hashing:** every imported file is copied into `data/raw/<batch_id>/`
  and SHA-256 hashed at import time (`athena/importers/base.py::preserve_raw_file` →
  `athena/security/audit_log.py::compute_sha256`).
- **Export manifest:** `athena export obsidian` and `athena/exporters/json_export.py`
  write a manifest (path, SHA-256, byte size, generation timestamp) alongside any export,
  so a copy can later be checked for tampering or truncation.
- **Audit log:** append-only JSONL at `data/derived/audit_log.jsonl`, one entry per
  CLI-driven action (init, import, validate, deduplicate, export). Never rewritten or
  truncated by this codebase.

## What is explicitly NOT implemented yet

- **Encrypted secret storage.** There is nothing to encrypt yet — Strava OAuth is an
  unimplemented interface (`athena/adapters/strava.py`), so no token exists. When it is
  implemented, plain environment variables (process-lifetime only) should be replaced with
  a persistent encrypted store (e.g. OS keychain) before any interactive use — this is
  called out directly in the Strava adapter's docstring.
- **`athena delete` / backup commands.** No code exists. Design intent below.
- **Encryption at rest for `data/athena.db`.** The database is plaintext SQLite today.

## Deletion command — design intent (not implemented)

A future `athena delete <record-id>` should:
1. Never delete the raw source file in `data/raw/` — the audit trail of *what was
   imported* should survive even if a derived record is removed, per spec 3.3.
2. Tombstone the canonical record (a `deleted_at` column, not a `DELETE FROM`), so
   re-running an import of the same raw file doesn't silently resurrect something the
   user explicitly removed without them knowing why.
3. Log the deletion to the audit log with the actor and reason.
4. Regenerate any Obsidian notes that referenced the deleted record's id, rather than
   leaving a dangling reference.

## Backup plan — design intent (not implemented)

`data/athena.db` is a single SQLite file; `data/raw/` holds immutable source copies. A
backup command should tar `data/` (excluding nothing — raw files are exactly what needs
protecting) plus `vault/ATHENA/` to a user-chosen destination, and should never be wired to
automatically sync to a cloud service by default (see "accidental Obsidian cloud sync"
below) — that decision belongs to the user's Obsidian/OS configuration, not to ATHENA.

## Threats considered

| Threat | Current posture |
|---|---|
| Leaked Git repository | `.gitignore` excludes `.env`, `data/raw/*`, `data/*.db`, and generated vault content (see `athena-health-intelligence/.gitignore`) — only code, schemas, docs, and synthetic test fixtures are committed |
| Stolen phone | Out of scope for this codebase (no mobile app exists yet); the future Android companion app (spec section 12) must not cache decrypted health data outside Health Connect's own storage |
| Compromised OAuth token | N/A today — no OAuth implemented. When Strava is built, see the encrypted-storage note above |
| Accidental Obsidian cloud sync | ATHENA does not control where a user points their Obsidian vault. The generated notes contain measurement values and validation state, which a user syncing their vault to a cloud service should be aware of — this is a user configuration decision to flag, not something ATHENA can prevent |
| Malicious dependency | `pyproject.toml` pins a minimal dependency set (`pydantic` only at runtime); no dependency reaches the network at import time |
| Corrupt import | Every importer collects per-record errors instead of crashing on the first bad row (`ImportResult.errors`); malformed JSON/CSV structure itself still raises loudly rather than being silently skipped — see `tests/unit/test_corrupted_input.py` |
| Duplicate data | Deduplication engine flags rather than silently double-counting in analytics — `athena/deduplication/`, and `Database.list_records(exclude_duplicates=True)` is the default for summaries/exports |
| Incorrect health interpretation | ATHENA does not diagnose (spec 3.5). Readiness scoring is an explicit unimplemented stub rather than a fabricated formula (`athena/analytics/readiness.py`) |
