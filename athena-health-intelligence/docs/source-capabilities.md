# Source Capabilities Review

## Important caveat on scope

The master spec asks this document to review `PHASE2_SAMSUNG_HEALTH_INTEGRATION.md`
specifically. **That file does not exist in this environment** (see
`docs/audit/AUDIT_REPORT.md` — Phase A is blocked for the same reason). Nothing below is a
review of that document's specific claims; it cannot be, since it was never read. What
follows is an independent capability assessment of Android Health Connect, Samsung Health,
Strava, and SmartHealth, based on their publicly documented behavior, marked
**REQUIRES FURTHER VERIFICATION** wherever this session has no way to confirm something
against a real device, a real Samsung Health account, or the actual Phase 2 document's
assumptions. Once the Phase 2 document is available, re-run this review against its
specific claims and update this table.

Status legend (per spec section 11): `CONFIRMED`, `CONDITIONAL`, `NOT AVAILABLE`,
`REQUIRES USER INPUT`, `REQUIRES DEVICE SUPPORT`, `REQUIRES FURTHER VERIFICATION`.

## Android Health Connect — platform-level facts

| Question | Status | Notes |
|---|---|---|
| Health Connect dependency current | REQUIRES FURTHER VERIFICATION | `androidx.health.connect:connect-client` version pinning must be checked against the current AndroidX release at implementation time, not assumed from training knowledge. |
| Required permissions | CONDITIONAL | Health Connect uses per-record-type runtime permissions (e.g. read `Weight`, read `HeartRate`) declared in the manifest and granted via the Health Connect permissions UI — not a single blanket "health" permission. Each record type ATHENA wants to read needs its own declared + granted permission. |
| Android SDK requirements | REQUIRES FURTHER VERIFICATION | Health Connect has minimum OS/API level requirements that have shifted as it moved from a standalone app to a platform module in newer Android versions; confirm the current minSdk against the target device (a Samsung phone, per this project's context) before scaffolding the companion app. |
| Background execution constraints | CONDITIONAL | Android's background execution limits (Doze, App Standby, foreground service requirements) apply to any scheduled sync; a naive background job is not guaranteed to run promptly. This is exactly why spec section 12 says not to hardcode a 2:00 AM schedule in the first implementation — foreground, user-initiated sync should come first. |
| Scheduled sync feasibility | REQUIRES FURTHER VERIFICATION | Feasible via WorkManager with appropriate constraints, but reliability (especially exact-time firing) is not guaranteed by the OS. Needs on-device testing, which this environment cannot do. |
| Samsung Health → Health Connect sync behavior | REQUIRES FURTHER VERIFICATION | Samsung Health is known to integrate with Health Connect on modern One UI versions, but *which specific record types* sync (and whether third-party ring/wearable apps write into Samsung Health, which then syncs to Health Connect) depends on the specific apps and OS version involved. This project explicitly does not assume this pathway works — see below. |
| Provenance availability via Health Connect | CONFIRMED (at the API level) | Every Health Connect record carries `Metadata` including a data origin (the writing app's package) and device info where the source provided it — this is why `athena/importers/health_connect.py` maps `metadata.dataOrigin`/`metadata.device` into `source_application`/`source_device`. Whether every source app actually populates device info is per-app behavior, not guaranteed. |
| Android permission declaration requirements | CONDITIONAL | Health Connect permissions must be declared in the manifest as an intent filter for the permissions rationale activity, in addition to the standard `<uses-permission>` entries — this is more involved than a typical runtime permission and needs to be built correctly in the (not-yet-started) companion app. |

## "Does SmartHealth automatically write ring data into Samsung Health?"

**Not assumed, not confirmed.** Per spec section 11's explicit instruction — *"Do not
claim SmartHealth automatically writes all ring data into Samsung Health. Treat that
pathway as unconfirmed until tested on the actual device."* — this document takes no
position on whether that pathway works. It is marked `REQUIRES DEVICE SUPPORT` +
`REQUIRES FURTHER VERIFICATION` and should be tested directly once a companion app exists.

## Per-metric availability through Health Connect

| Metric (ATHENA `metric_type`) | Health Connect record type | Status |
|---|---|---|
| `body_weight_kg` | `WeightRecord` | CONFIRMED (record type exists; requires the writing app to populate it and the user to grant the `Weight` read permission) |
| `heart_rate_bpm` | `HeartRateRecord` | CONFIRMED |
| `resting_heart_rate_bpm` | `RestingHeartRateRecord` | CONDITIONAL — distinct record type from `HeartRateRecord`; not yet mapped in `athena/importers/health_connect.py` (only plain heart-rate samples are handled today) |
| `spo2_percent` | `OxygenSaturationRecord` | CONFIRMED |
| `hrv_ms` | `HeartRateVariabilityRmssdRecord` | CONFIRMED, but HRV is watch/ring-dependent — REQUIRES DEVICE SUPPORT |
| `blood_pressure_systolic_mmhg` / `_diastolic_mmhg` | `BloodPressureRecord` | CONFIRMED at the API level; REQUIRES USER INPUT in practice since most consumer wearables don't measure blood pressure directly — this is usually manually logged or comes from a dedicated BP cuff |
| `sleep_session_duration_minutes` + stages | `SleepSessionRecord` (+ `SleepStageRecord`/stage list) | CONFIRMED, REQUIRES DEVICE SUPPORT for stage-level detail (light/deep/REM/awake) — not every device reports all four stages |
| `steps_count` | `StepsRecord` | CONFIRMED |
| `activity_distance_km` / `activity_duration_minutes` | `ExerciseSessionRecord` / `DistanceRecord` | CONDITIONAL — not yet implemented in `athena/importers/health_connect.py`; the record types exist in Health Connect |
| `bmr_kcal` | `BasalMetabolicRateRecord` | CONDITIONAL — exists in Health Connect, not yet mapped in this codebase |
| Body composition (skeletal muscle mass, lean body mass, total body water, visceral fat, biological age) | `BodyFatRecord`, `LeanBodyMassRecord` exist; skeletal muscle mass, total body water, visceral fat rating, and biological age do **not** have dedicated Health Connect record types as of current public documentation | NOT AVAILABLE for the Evolt-specific fields via Health Connect — this is exactly why `athena/importers/evolt.py` exists as a separate structured-JSON/CSV importer rather than assuming Evolt data flows through Health Connect |
| VO2max | `Vo2MaxRecord` | CONFIRMED at API level, REQUIRES DEVICE SUPPORT |

## Strava

Documented, not implemented — see `athena/adapters/strava.py` for the full OAuth flow,
scopes, rate limits, pagination, and dedup considerations (spec section 13). No status
table entry is meaningful here since no code path has been exercised against Strava's real
API from this environment.

## SmartHealth

Per spec section 14, this is capability-discovery only:

| Capability | Status |
|---|---|
| Samsung Health integration | REQUIRES FURTHER VERIFICATION |
| Health Connect integration | REQUIRES FURTHER VERIFICATION |
| CSV export | REQUIRES FURTHER VERIFICATION |
| JSON export | REQUIRES FURTHER VERIFICATION |
| PDF export | REQUIRES FURTHER VERIFICATION |
| Account archive/export | REQUIRES FURTHER VERIFICATION |
| Vendor API | REQUIRES FURTHER VERIFICATION |
| Manual export | REQUIRES FURTHER VERIFICATION |

No private endpoints have been probed, no account credentials have been requested, and no
claim of direct integration is made anywhere in this codebase.
