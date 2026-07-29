from __future__ import annotations

from pathlib import Path

import pytest

from athena.config import AthenaConfig, load_config
from athena.database import Database

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def config(tmp_path) -> AthenaConfig:
    cfg = load_config(tmp_path)
    for d in cfg.required_dirs():
        d.mkdir(parents=True, exist_ok=True)
    return cfg


@pytest.fixture
def db(config: AthenaConfig) -> Database:
    database = Database(config.db_path)
    database.init_db()
    return database


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR
