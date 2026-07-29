from __future__ import annotations

import pytest

from athena.importers.evolt import EvoltImporter


def test_valid_scan_imports_all_mapped_fields(config, fixtures_dir):
    result = EvoltImporter(config).import_source(fixtures_dir / "evolt_scan_valid.json")
    assert result.ok
    assert len(result.records) == 8
    assert all(r.source_platform == "evolt" for r in result.records)
    assert all(r.measurement_type == "device_estimated" for r in result.records)
    assert all(r.source_record_id == "scan-valid-001" for r in result.records)


def test_suspicious_scan_flags_impossible_values(config, fixtures_dir):
    result = EvoltImporter(config).import_source(fixtures_dir / "evolt_scan_suspicious.json")
    assert result.ok
    smm = next(r for r in result.records if r.metric_type == "skeletal_muscle_mass_kg")
    weight = next(r for r in result.records if r.metric_type == "body_weight_kg")
    assert smm.validation_status == "invalid"
    assert weight.validation_status == "invalid"


def test_unmapped_field_still_imported_and_flagged(config, fixtures_dir):
    result = EvoltImporter(config).import_source(fixtures_dir / "evolt_scan_suspicious.json")
    unmapped = next(r for r in result.records if r.metric_type.startswith("evolt_unmapped__"))
    assert unmapped.extraction_method == "structured_json"
    assert any("unrecognized" in m.lower() for m in unmapped.validation_messages)


def test_review_file_generated(config, fixtures_dir):
    EvoltImporter(config).import_source(fixtures_dir / "evolt_scan_valid.json")
    review_files = list((config.vault_subdir("17-IMPORT-LOGS")).glob("evolt-import-review-*.md"))
    assert len(review_files) == 1
    content = review_files[0].read_text()
    assert "UNCONFIRMED" in content
    assert "skeletal_muscle_mass_kg" in content


def test_pdf_raises_not_implemented(config, tmp_path):
    fake_pdf = tmp_path / "scan.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake")
    with pytest.raises(NotImplementedError):
        EvoltImporter(config).import_source(fake_pdf)
