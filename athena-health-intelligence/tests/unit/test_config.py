from __future__ import annotations

from athena.config import load_config


def test_load_config_defaults_to_cwd_when_no_home_given(monkeypatch, tmp_path):
    monkeypatch.delenv("ATHENA_HOME", raising=False)
    monkeypatch.chdir(tmp_path)
    cfg = load_config()
    assert cfg.home == tmp_path.resolve()


def test_load_config_explicit_home_wins(tmp_path, monkeypatch):
    monkeypatch.setenv("ATHENA_HOME", "/should/not/be/used")
    cfg = load_config(tmp_path)
    assert cfg.home == tmp_path.resolve()


def test_load_config_env_var_used_when_no_explicit_home(tmp_path, monkeypatch):
    monkeypatch.setenv("ATHENA_HOME", str(tmp_path))
    cfg = load_config()
    assert cfg.home == tmp_path.resolve()


def test_required_dirs_include_all_vault_subdirs(tmp_path):
    cfg = load_config(tmp_path)
    dirs = {d.name for d in cfg.required_dirs()}
    assert "raw" in dirs
    assert "05-DAILY-NOTES" in dirs
    assert "17-IMPORT-LOGS" in dirs
