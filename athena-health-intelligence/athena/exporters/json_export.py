"""JSON export of canonical records, plus an export manifest (per
docs/security.md) so a copied export can be checked for tampering or
truncation after the fact.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from athena.database import Database


def export_records_json(db: Database, out_path: str | Path, **filters) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    records = db.list_records(**filters)
    payload = [json.loads(r.model_dump_json()) for r in records]
    out_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return out_path


def write_export_manifest(exported_paths: list[Path], manifest_path: str | Path) -> Path:
    manifest_path = Path(manifest_path)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    entries = []
    for p in exported_paths:
        p = Path(p)
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        entries.append({"path": str(p), "sha256": digest, "bytes": p.stat().st_size})
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": entries,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path
