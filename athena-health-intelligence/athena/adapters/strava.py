"""Strava adapter — INTERFACE ONLY, per master spec section 13.

"Prepare the adapter interface but do not implement OAuth until the
canonical pipeline is stable." Every method below raises
NotImplementedError. No credentials are read, stored, or committed
anywhere in this module or in .env.example.

OAuth flow (for when this is implemented):
    1. Authorization Code flow: redirect user to
       https://www.strava.com/oauth/authorize with client_id, redirect_uri,
       response_type=code, scope=read,activity:read_all.
    2. Exchange the returned `code` at POST https://www.strava.com/oauth/token
       for access_token + refresh_token (refresh_token does not expire;
       access_token expires in ~6 hours).
    3. Store tokens via athena.security.secrets (env-backed) or a future
       encrypted token store — never in Markdown, never in the SQLite DB
       in plaintext, never committed.
    4. Refresh proactively before expiry using the refresh_token.

Required scopes: `read` (public profile) and `activity:read_all` (private
activities) — request the narrowest scope that satisfies the feature.

Token storage: not implemented. athena/security/secrets.py provides
env-var-only access as the intended chokepoint; a persistent encrypted
store (e.g. OS keychain) should replace bare env vars before this adapter
is used interactively, since env vars are process-lifetime only.

Rate limits (Strava's published limits, subject to change — verify
against Strava's developer docs before relying on this): 200 requests
per 15 minutes, 2,000 requests per day, per application. An adapter
implementation must back off on HTTP 429 rather than retry immediately.

Activity pagination: GET /athlete/activities is paginated via `page` and
`per_page` (max 200) query params; there is no cursor, so a long
backfill must page until an empty page is returned.

Activity IDs: Strava activity IDs are per-athlete-per-app stable
integers; store them as source_record_id so re-imports are naturally
idempotent (see athena/deduplication/).

Deduplication against Samsung Health / Health Connect exercise sessions:
Strava activities are frequently the *same* underlying workout also
recorded by a phone or watch and synced to Health Connect. Matching
should use start_time proximity + activity type + duration, similar to
athena/deduplication/strategies.py's TimeWindowValueStrategy, but this is
not implemented — a naive value-tolerance match on distance/duration
across two different GPS/sensor sources would likely produce false
duplicates or false negatives. This needs its own strategy once both
sources are live.
"""

from __future__ import annotations

from datetime import datetime

from athena.importers.base import HealthSourceAdapter, ImportResult
from athena.models.source import SourcePlatform


class StravaAdapter(HealthSourceAdapter):
    source_platform = SourcePlatform.STRAVA

    def authenticate(self) -> None:
        raise NotImplementedError(
            "Strava OAuth is not implemented. See this module's docstring for the "
            "documented flow. No credentials are read or stored by this stub."
        )

    def fetch_records(self, *, start: datetime, end: datetime) -> ImportResult:
        raise NotImplementedError("Strava activity fetching is not implemented — see authenticate().")
