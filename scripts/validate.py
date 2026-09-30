#!/usr/bin/env python3
"""Valida todas las fichas: esquema JSON, vocabulario, id/fichero/sector, unicidad y referencias."""
from __future__ import annotations

import json
import sys

from jsonschema import Draft202012Validator

from common import SCHEMA, load_sources, load_vocab


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    vocab = load_vocab()
    sources = load_sources()
    errors: list[str] = []
    ids = {}

    for s in sources:
        path = s.pop("_path")
        dir_sector = s.pop("_dir_sector")
        for err in validator.iter_errors(s):
            loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
            errors.append(f"{path}: {loc}: {err.message}")
        sid = s.get("id", "")
        if sid and path.rsplit("/", 1)[-1] != f"{sid}.yaml":
            errors.append(f"{path}: id '{sid}' no coincide con el nombre del fichero")
        if sid in ids:
            errors.append(f"{path}: id duplicado '{sid}' (también en {ids[sid]})")
        ids[sid] = path
        if s.get("sector") != dir_sector:
            errors.append(f"{path}: sector '{s.get('sector')}' no coincide con la carpeta '{dir_sector}'")
        for field in ("level", "sector", "auth", "update", "status"):
            val = s.get(field)
            if val is not None and val not in vocab[field]:
                errors.append(f"{path}: {field}='{val}' no está en schema/vocab.yaml")
        for a in s.get("access", []):
            if a not in vocab["access"]:
                errors.append(f"{path}: access '{a}' no está en el vocabulario")
        for fmt in s.get("formats", []):
            if fmt not in vocab["formats"]:
                errors.append(f"{path}: formato '{fmt}' no está en el vocabulario")
        summary = s.get("summary", "")
        if summary and summary.strip().endswith(":"):
            errors.append(f"{path}: summary termina en ':'")

    for s in sources:
        for r in s.get("related", []):
            if r not in ids:
                errors.append(f"{s['id']}: related '{r}' no existe")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"\n{len(errors)} error(es) en {len(sources)} fichas", file=sys.stderr)
        return 1
    print(f"OK: {len(sources)} fichas válidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
