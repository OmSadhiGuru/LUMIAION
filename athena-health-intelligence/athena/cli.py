"""ATHENA CLI. Golden path:

    athena init
    athena import manual --from-json <mapping.json>
    athena validate
    athena export obsidian
    athena summarize daily 2026-07-29
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime

from athena.analytics.daily import summarize_daily
from athena.analytics.weekly import InvalidWeekFormatError, summarize_weekly
from athena.config import AthenaConfig, load_config
from athena.database import Database
from athena.deduplication.engine import deduplicate
from athena.exporters.json_export import export_records_json, write_export_manifest
from athena.exporters.obsidian import export_daily_notes_for_all_dates, write_daily_note, write_weekly_review
from athena.importers.csv_importer import CsvImporter
from athena.importers.evolt import EvoltImporter
from athena.importers.json_importer import JsonImporter
from athena.importers.manual import ManualImporter
from athena.security.audit_log import AuditLog
from athena.validation.engine import validate_records


def _db(config: AthenaConfig) -> Database:
    db = Database(config.db_path)
    db.init_db()
    return db


def _audit(config: AthenaConfig) -> AuditLog:
    return AuditLog(config.audit_log_path)


def cmd_doctor(args, config: AthenaConfig) -> int:
    ok = True
    print(f"ATHENA_HOME: {config.home}")
    print(f"python: {sys.version.split()[0]}")

    if config.db_path.exists():
        db = Database(config.db_path)
        print(f"database: OK ({config.db_path}), schema_version={db.schema_version()}, records={db.count_records()}")
    else:
        print(f"database: NOT INITIALIZED ({config.db_path}) — run 'athena init'")
        ok = False

    for d in config.required_dirs():
        status = "OK" if d.exists() else "MISSING"
        if status == "MISSING":
            ok = False
        print(f"dir {d}: {status}")

    print("doctor: " + ("PASS" if ok else "ISSUES FOUND"))
    return 0 if ok else 1


def cmd_init(args, config: AthenaConfig) -> int:
    for d in config.required_dirs():
        d.mkdir(parents=True, exist_ok=True)
    db = Database(config.db_path)
    db.init_db()
    _audit(config).record("init", detail={"home": str(config.home)})
    print(f"Initialized ATHENA at {config.home}")
    print(f"  database: {config.db_path} (schema_version={db.schema_version()})")
    print(f"  vault: {config.vault_dir}")
    return 0


def _print_import_result(result) -> int:
    print(f"batch_id: {result.batch_id}")
    print(f"records imported: {len(result.records)}")
    for r in result.records:
        print(f"  {r.id}  {r.metric_type}={r.normalized_value}{r.normalized_unit or ''}  [{r.validation_status}]")
    if result.errors:
        print(f"errors: {len(result.errors)}")
        for e in result.errors:
            print(f"  ! {e}")
    return 0 if result.ok else 1


def cmd_import_manual(args, config: AthenaConfig) -> int:
    if args.from_json:
        with open(args.from_json, "r", encoding="utf-8") as f:
            mapping = json.load(f)
    elif args.json:
        mapping = json.loads(args.json)
    else:
        mapping = {
            "metric_type": input("metric_type: ").strip(),
            "value": input("value: ").strip(),
            "unit": input("unit (blank if none): ").strip() or None,
            "start_time": input("start_time (ISO 8601, e.g. 2026-07-29T07:00:00): ").strip(),
            "timezone": input("timezone (e.g. America/New_York): ").strip() or "UTC",
        }
        try:
            mapping["value"] = float(mapping["value"])
        except ValueError:
            pass

    db = _db(config)
    result = ManualImporter(config).import_record(mapping)
    for r in result.records:
        db.insert_record(r)
    _audit(config).record("import_manual", detail={"batch_id": result.batch_id, "count": len(result.records)})
    return _print_import_result(result)


def cmd_import_json(args, config: AthenaConfig) -> int:
    db = _db(config)
    result = JsonImporter(config).import_source(args.path)
    for r in result.records:
        db.insert_record(r)
    _audit(config).record("import_json", detail={"batch_id": result.batch_id, "count": len(result.records), "source": args.path})
    return _print_import_result(result)


def cmd_import_csv(args, config: AthenaConfig) -> int:
    db = _db(config)
    result = CsvImporter(config).import_source(args.path)
    for r in result.records:
        db.insert_record(r)
    _audit(config).record("import_csv", detail={"batch_id": result.batch_id, "count": len(result.records), "source": args.path})
    return _print_import_result(result)


def cmd_import_evolt(args, config: AthenaConfig) -> int:
    db = _db(config)
    result = EvoltImporter(config).import_source(args.path)
    for r in result.records:
        db.insert_record(r)
    _audit(config).record("import_evolt", detail={"batch_id": result.batch_id, "count": len(result.records), "source": args.path})
    print("NOTE: Evolt values are device-estimated and UNCONFIRMED — see the generated "
          "review file under vault/ATHENA/17-IMPORT-LOGS/ before trusting them.")
    return _print_import_result(result)


def cmd_validate(args, config: AthenaConfig) -> int:
    db = _db(config)
    summary = validate_records(db, batch_id=args.batch)
    _audit(config).record("validate", detail={"batch": args.batch, "summary": summary})
    print("Validation summary:")
    for status, count in summary.items():
        print(f"  {status}: {count}")
    return 0


def cmd_records_list(args, config: AthenaConfig) -> int:
    db = _db(config)
    records = db.list_records(metric_type=args.metric_type, exclude_duplicates=not args.include_duplicates)
    for r in records:
        print(
            f"{r.id}  {r.start_time.isoformat()}  {r.metric_type}={r.normalized_value}{r.normalized_unit or ''}  "
            f"[{r.validation_status}]  dup={r.duplicate_status}"
        )
    print(f"({len(records)} record(s))")
    return 0


def cmd_records_show(args, config: AthenaConfig) -> int:
    db = _db(config)
    record = db.get_record(args.id)
    if record is None:
        print(f"No record with id {args.id}", file=sys.stderr)
        return 1
    print(json.dumps(json.loads(record.model_dump_json()), indent=2, default=str))
    return 0


def cmd_deduplicate(args, config: AthenaConfig) -> int:
    db = _db(config)
    result = deduplicate(db)
    _audit(config).record("deduplicate", detail=result)
    print(f"Scanned {result['records_scanned']} records, found {result['duplicates_found']} duplicate(s).")
    return 0


def cmd_export_obsidian(args, config: AthenaConfig) -> int:
    db = _db(config)
    paths = export_daily_notes_for_all_dates(config, db)
    manifest_path = config.derived_dir / "export_manifest.json"
    write_export_manifest(paths, manifest_path)
    _audit(config).record("export_obsidian", detail={"notes": len(paths)})
    print(f"Wrote {len(paths)} daily note(s) to {config.vault_subdir('05-DAILY-NOTES')}")
    print(f"Export manifest: {manifest_path}")
    return 0


def cmd_summarize_daily(args, config: AthenaConfig) -> int:
    db = _db(config)
    target_date = date.fromisoformat(args.date)
    summary = summarize_daily(db, target_date)
    path = write_daily_note(config, summary)
    print(f"{summary.total_records} record(s) on {target_date.isoformat()}; {len(summary.quality_warnings)} quality warning(s)")
    print(f"Daily note: {path}")
    return 0


def cmd_summarize_weekly(args, config: AthenaConfig) -> int:
    db = _db(config)
    try:
        summary = summarize_weekly(db, args.week)
    except InvalidWeekFormatError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    path = write_weekly_review(config, summary)
    print(f"Week {summary.week}: {len(summary.averages_by_metric)} metric(s) tracked, {summary.quality_warning_count} quality warning(s)")
    print(f"Weekly review: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="athena", description="ATHENA local-first health intelligence CLI")
    parser.add_argument("--home", default=None, help="ATHENA_HOME override (defaults to $ATHENA_HOME or cwd)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="Check environment health").set_defaults(func=cmd_doctor)
    sub.add_parser("init", help="Initialize data dirs, database, and vault").set_defaults(func=cmd_init)

    import_parser = sub.add_parser("import", help="Import health data")
    import_sub = import_parser.add_subparsers(dest="import_command", required=True)

    p = import_sub.add_parser("manual", help="Manually enter one record")
    p.add_argument("--from-json", default=None, help="Path to a JSON file with the record mapping")
    p.add_argument("--json", default=None, help="Inline JSON string with the record mapping")
    p.set_defaults(func=cmd_import_manual)

    p = import_sub.add_parser("json", help="Import a structured JSON file")
    p.add_argument("path")
    p.set_defaults(func=cmd_import_json)

    p = import_sub.add_parser("csv", help="Import a structured CSV file")
    p.add_argument("path")
    p.set_defaults(func=cmd_import_csv)

    p = import_sub.add_parser("evolt", help="Import an Evolt scan (structured JSON/CSV; PDF not supported)")
    p.add_argument("path")
    p.set_defaults(func=cmd_import_evolt)

    p = sub.add_parser("validate", help="Run the validation engine")
    p.add_argument("--batch", default=None, help="Limit validation to one import batch id")
    p.set_defaults(func=cmd_validate)

    records_parser = sub.add_parser("records", help="Inspect canonical records")
    records_sub = records_parser.add_subparsers(dest="records_command", required=True)

    p = records_sub.add_parser("list", help="List records")
    p.add_argument("--metric-type", default=None)
    p.add_argument("--include-duplicates", action="store_true")
    p.set_defaults(func=cmd_records_list)

    p = records_sub.add_parser("show", help="Show one record in full")
    p.add_argument("id")
    p.set_defaults(func=cmd_records_show)

    sub.add_parser("deduplicate", help="Run the deduplication engine").set_defaults(func=cmd_deduplicate)

    export_parser = sub.add_parser("export", help="Export data")
    export_sub = export_parser.add_subparsers(dest="export_command", required=True)
    export_sub.add_parser("obsidian", help="Write Obsidian daily notes for every date in the DB").set_defaults(
        func=cmd_export_obsidian
    )

    summarize_parser = sub.add_parser("summarize", help="Generate summaries")
    summarize_sub = summarize_parser.add_subparsers(dest="summarize_command", required=True)

    p = summarize_sub.add_parser("daily", help="Summarize one date (YYYY-MM-DD)")
    p.add_argument("date")
    p.set_defaults(func=cmd_summarize_daily)

    p = summarize_sub.add_parser("weekly", help="Summarize one ISO week (YYYY-Www)")
    p.add_argument("week")
    p.set_defaults(func=cmd_summarize_weekly)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config(args.home)
    try:
        return args.func(args, config)
    except NotImplementedError as exc:
        print(f"Not implemented: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"File not found: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
