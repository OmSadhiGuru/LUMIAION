from __future__ import annotations

from datetime import datetime, timezone

import pytest

from athena.adapters.strava import StravaAdapter


def test_strava_authenticate_not_implemented():
    with pytest.raises(NotImplementedError):
        StravaAdapter().authenticate()


def test_strava_fetch_records_not_implemented():
    with pytest.raises(NotImplementedError):
        StravaAdapter().fetch_records(start=datetime.now(timezone.utc), end=datetime.now(timezone.utc))


def test_no_strava_credentials_in_env_example():
    from pathlib import Path

    env_example = Path(__file__).resolve().parents[2] / ".env.example"
    content = env_example.read_text()
    for line in content.splitlines():
        if line.startswith("STRAVA_") and "=" in line:
            assert line.split("=", 1)[1].strip() == "", f"unexpected value committed for {line}"
