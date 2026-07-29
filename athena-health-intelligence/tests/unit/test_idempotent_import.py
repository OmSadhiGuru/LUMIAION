from __future__ import annotations

from athena.deduplication.engine import deduplicate
from athena.importers.json_importer import JsonImporter


def test_importing_same_file_twice_is_flagged_by_deduplication(config, db, fixtures_dir):
    result1 = JsonImporter(config).import_source(fixtures_dir / "manual_record.json")
    result2 = JsonImporter(config).import_source(fixtures_dir / "manual_record.json")
    for r in result1.records + result2.records:
        db.insert_record(r)

    assert db.count_records() == 2  # nothing is silently dropped or merged at import time

    dedup_result = deduplicate(db)

    assert dedup_result["duplicates_found"] == 1
    unique_records = db.list_records(exclude_duplicates=True)
    assert len(unique_records) == 1
