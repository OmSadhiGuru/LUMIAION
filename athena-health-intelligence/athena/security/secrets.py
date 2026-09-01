"""Secret access: environment variables only, never files or Markdown.

No token storage backend is implemented yet — there is nothing to store
until the Strava OAuth flow is built (see athena/adapters/strava.py,
which is an interface stub, not a working integration). This module
exists now so that when that day comes, secrets are read through one
audited chokepoint instead of `os.environ.get()` calls scattered across
importers.
"""

from __future__ import annotations

import os


class SecretNotFoundError(RuntimeError):
    pass


def get_secret(name: str, *, required: bool = True) -> str | None:
    """Read a secret from the environment. Never reads from a file,
    never logs the value, never accepts a default containing a real value.
    """
    value = os.environ.get(name)
    if value is None or value == "":
        if required:
            raise SecretNotFoundError(
                f"Secret '{name}' is not set. Set it as an environment variable "
                f"(see .env.example) — ATHENA never reads secrets from files or Markdown."
            )
        return None
    return value
