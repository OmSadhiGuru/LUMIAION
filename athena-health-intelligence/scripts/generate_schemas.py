#!/usr/bin/env python3
"""Regenerate schemas/canonical-health-record.schema.json from the
pydantic model so it can never drift from athena/models/canonical.py.
Run after any change to CanonicalHealthRecord.
"""

from __future__ import annotations

import json
from pathlib import Path

from athena.models.canonical import CanonicalHealthRecord

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    schema = CanonicalHealthRecord.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = "https://athena.local/schemas/canonical-health-record.schema.json"
    schema["title"] = "ATHENA Canonical Health Record"
    out_path = ROOT / "schemas" / "canonical-health-record.schema.json"
    out_path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
