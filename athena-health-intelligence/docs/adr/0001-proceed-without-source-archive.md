# ADR 0001: Proceed with Phases B–E without the Phase 0 archive

## Status
Accepted

## Context
The task instructions referenced `/mnt/data/athena_phase0_complete_vault.tar.gz` and
`/mnt/data/PHASE2_SAMSUNG_HEALTH_INTEGRATION.md` as inputs for a Phase A audit. Neither
file exists in this execution environment (verified via direct filesystem search before
any other work began).

## Decision
Do not fabricate audit findings about the missing archive. Instead:
1. Document the blocker explicitly and honestly in `docs/audit/AUDIT_REPORT.md`.
2. Proceed with Phases B–E (canonical repository, data model, validation engine, first
   vertical slice), which the spec itself designs to run on synthetic test data
   independent of any real vault (spec section 8: "Do not require access to Frederick's
   real private health data for tests").

## Consequences
- The audit report cannot include a real file inventory, data-quality findings about
  actual Evolt scans, or a gap analysis of Genspark's prior work — those sections
  explicitly say so rather than guessing.
- Everything delivered in this PR is genuinely new code with passing tests, not a
  restructuring of inherited work.
- Phase A must be re-run once the archive is actually provided to this repository.
