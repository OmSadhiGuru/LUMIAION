# ADR 0002: Provenance fields are flat on CanonicalHealthRecord, not nested

## Status
Accepted

## Context
The master spec's own `CanonicalHealthRecord` class definition (section 6) lists
provenance fields (`source_platform`, `source_application`, `source_record_id`, etc.)
directly on the model rather than as a nested `Provenance` object, even though
`athena/models/provenance.py` is also a listed file in the target repository structure.

## Decision
Keep `CanonicalHealthRecord` fields flat, matching the spec's literal class definition.
`athena/models/provenance.py` provides a `Provenance` container and `build_provenance()`
factory that importers can use to construct the provenance-related keyword arguments in
one place, then spread them into `CanonicalHealthRecord(**provenance.as_kwargs(), ...)` —
but the canonical storage shape itself stays flat.

## Consequences
- Every provenance field is a first-class SQLite column (see `athena/database.py`),
  queryable directly (`WHERE source_platform = 'evolt' AND validation_status =
  'questionable'`) without JSON path expressions into a nested blob.
- `provenance.py` exists and is used, but as a builder/helper, not as the storage shape —
  satisfying both the literal model spec and the "every canonical record must preserve
  provenance" requirement (spec 3.4).
