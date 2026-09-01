"""Runtime configuration: where ATHENA's local-first data lives.

Everything resolves from a single ATHENA_HOME root (env var, or the
project directory by default) so `athena doctor` and the test suite can
point at an isolated tmp directory without touching a real vault.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AthenaConfig:
    home: Path

    @property
    def data_dir(self) -> Path:
        return self.home / "data"

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def normalized_dir(self) -> Path:
        return self.data_dir / "normalized"

    @property
    def derived_dir(self) -> Path:
        return self.data_dir / "derived"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "athena.db"

    @property
    def vault_dir(self) -> Path:
        return self.home / "vault" / "ATHENA"

    @property
    def audit_log_path(self) -> Path:
        return self.derived_dir / "audit_log.jsonl"

    def vault_subdir(self, name: str) -> Path:
        return self.vault_dir / name

    def required_dirs(self) -> list[Path]:
        return [
            self.raw_dir,
            self.normalized_dir,
            self.derived_dir,
            self.vault_subdir("05-DAILY-NOTES"),
            self.vault_subdir("06-WEEKLY-REVIEWS"),
            self.vault_subdir("08-BODY-SCANS"),
            self.vault_subdir("12-INSIGHTS"),
            self.vault_subdir("13-ALERTS"),
            self.vault_subdir("14-DASHBOARDS"),
            self.vault_subdir("17-IMPORT-LOGS"),
        ]


def load_config(home: str | Path | None = None) -> AthenaConfig:
    if home is not None:
        resolved = Path(home)
    else:
        env_home = os.environ.get("ATHENA_HOME")
        resolved = Path(env_home) if env_home else Path.cwd()
    return AthenaConfig(home=resolved.resolve())
