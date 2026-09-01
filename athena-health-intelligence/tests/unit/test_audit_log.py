from __future__ import annotations

from athena.security.audit_log import AuditLog, compute_sha256


def test_audit_log_appends_entries(tmp_path):
    log = AuditLog(tmp_path / "audit_log.jsonl")
    log.record("import_manual", target_id="rec-1", detail={"count": 1})
    log.record("validate", detail={"summary": {"valid": 1}})

    entries = log.read_all()
    assert len(entries) == 2
    assert entries[0]["action"] == "import_manual"
    assert entries[0]["target_id"] == "rec-1"
    assert entries[1]["action"] == "validate"


def test_audit_log_is_append_only_across_instances(tmp_path):
    path = tmp_path / "audit_log.jsonl"
    AuditLog(path).record("first")
    AuditLog(path).record("second")
    assert len(AuditLog(path).read_all()) == 2


def test_compute_sha256_matches_known_hash(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("athena", encoding="utf-8")
    import hashlib

    expected = hashlib.sha256(b"athena").hexdigest()
    assert compute_sha256(f) == expected


def test_compute_sha256_differs_for_different_content(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("one", encoding="utf-8")
    f2.write_text("two", encoding="utf-8")
    assert compute_sha256(f1) != compute_sha256(f2)
