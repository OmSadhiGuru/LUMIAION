"""Integration test for the exact golden path from the master spec:

    athena init
    athena import manual
    athena validate
    athena export obsidian
    athena summarize daily 2026-07-29

Runs the real CLI (athena.cli.main) against a tmp_path ATHENA_HOME with
synthetic data only — no real health data, per the spec's testing rules.
"""

from __future__ import annotations

import json

from athena.cli import main


def _run(argv, capsys):
    exit_code = main(argv)
    captured = capsys.readouterr()
    return exit_code, captured.out, captured.err


def test_golden_path_workflow(tmp_path, capsys):
    home = str(tmp_path)

    code, out, _ = _run(["--home", home, "init"], capsys)
    assert code == 0
    assert "Initialized ATHENA" in out

    mapping_path = tmp_path / "weight.json"
    mapping_path.write_text(
        json.dumps(
            {
                "metric_type": "body_weight_kg",
                "value": 81.2,
                "unit": "kg",
                "start_time": "2026-07-29T07:00:00-04:00",
                "timezone": "America/New_York",
                "measurement_type": "manual",
            }
        ),
        encoding="utf-8",
    )
    code, out, _ = _run(["--home", home, "import", "manual", "--from-json", str(mapping_path)], capsys)
    assert code == 0
    assert "records imported: 1" in out

    code, out, _ = _run(["--home", home, "validate"], capsys)
    assert code == 0
    assert "valid: 1" in out

    code, out, _ = _run(["--home", home, "export", "obsidian"], capsys)
    assert code == 0

    daily_note = tmp_path / "vault" / "ATHENA" / "05-DAILY-NOTES" / "2026-07-29.md"
    assert daily_note.exists()
    assert "body_weight_kg" in daily_note.read_text()

    code, out, _ = _run(["--home", home, "summarize", "daily", "2026-07-29"], capsys)
    assert code == 0
    assert "1 record(s) on 2026-07-29" in out

    code, out, _ = _run(["--home", home, "doctor"], capsys)
    assert code == 0
    assert "PASS" in out


def test_records_list_and_show(tmp_path, capsys):
    home = str(tmp_path)
    _run(["--home", home, "init"], capsys)
    mapping_path = tmp_path / "weight.json"
    mapping_path.write_text(
        json.dumps(
            {
                "metric_type": "body_weight_kg",
                "value": 81.2,
                "unit": "kg",
                "start_time": "2026-07-29T07:00:00-04:00",
                "timezone": "America/New_York",
            }
        ),
        encoding="utf-8",
    )
    _run(["--home", home, "import", "manual", "--from-json", str(mapping_path)], capsys)

    code, out, _ = _run(["--home", home, "records", "list"], capsys)
    assert code == 0
    assert "body_weight_kg" in out
    record_id = out.splitlines()[0].split()[0]

    code, out, _ = _run(["--home", home, "records", "show", record_id], capsys)
    assert code == 0
    payload = json.loads(out)
    assert payload["id"] == record_id


def test_evolt_pdf_gives_clean_not_implemented_message(tmp_path, capsys):
    home = str(tmp_path)
    _run(["--home", home, "init"], capsys)
    fake_pdf = tmp_path / "scan.pdf"
    fake_pdf.write_bytes(b"%PDF fake")

    code, _, err = _run(["--home", home, "import", "evolt", str(fake_pdf)], capsys)
    assert code == 2
    assert "Not implemented" in err
