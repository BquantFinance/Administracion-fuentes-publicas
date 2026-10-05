#!/usr/bin/env python3
"""Valida las fichas (esquema JSON, vocabulario, id/fichero/sector, unicidad, referencias) y los índices de indices/."""
from __future__ import annotations

import ast
import json
import re
import sys

from jsonschema import Draft202012Validator

from common import INDEX_FILES, ROOT, SCHEMA, comandos_paquete, herramientas_mcp, load_indices, load_sources, load_vocab

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
URL_RE = re.compile(r"^https?://\S+$")
DEAD_STATUS = {"404", "400", "403", "500", "503", "redirect", "moved", "reset", "blocked", "dns", "error", "empty"}
CHECK_KEYS = {"url", "method", "headers", "status", "contains", "min_bytes", "read_bytes", "retries", "fnmt"}
CLIENTES = ROOT / "scripts" / "clientes"
CODE_MAX = 600  # caracteres del bloque code en JSON compacto, lo que paga ficha() en cada llamada


def nombres_modulo(nombre: str) -> set[str] | None:
    """Funciones, clases y variables de primer nivel de scripts/clientes/<nombre>.py, sin importarlo; None si no existe."""
    path = CLIENTES / f"{nombre}.py"
    if not path.is_file() or nombre.startswith("_"):
        return None
    out = set()
    for n in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out.add(n.name)
        elif isinstance(n, ast.Assign):
            out |= {t.id for t in n.targets if isinstance(t, ast.Name)}
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            out.add(n.target.id)
    return out


def partir_use(linea: str) -> tuple[str, str]:
    """«llamada: qué devuelve» partido en el primer «: » fuera de paréntesis, corchetes, llaves y comillas (una llamada
    puede llevar un dict: ckan.filas('gva', rid, filters={'a': 1}))."""
    nivel, comilla = 0, None
    for i, ch in enumerate(linea):
        if comilla:
            comilla = None if ch == comilla else comilla
        elif ch in "'\"":
            comilla = ch
        elif ch in "([{":
            nivel += 1
        elif ch in ")]}":
            nivel -= 1
        elif ch == ":" and nivel == 0 and linea[i + 1:i + 2] == " ":
            return linea[:i], linea[i + 2:].strip()
    return linea, ""


def validate_code(path: str, code: dict, herramientas: set[str], comandos: set[str]) -> list[str]:
    """code de una ficha: módulo que existe, cada use con una llamada a una función que existe en su módulo (o una
    orden del paquete) y una descripción, mcp solo con herramientas del servidor y el bloque entero en CODE_MAX."""
    errors = []
    w = f"{path}: code"
    modulo = str(code.get("module", "")).rsplit(".", 1)[-1]
    if nombres_modulo(modulo) is None:
        errors.append(f"{w}: module {code.get('module')} no está en scripts/clientes")
    for linea in code.get("use") or []:
        llamada, que = partir_use(linea)
        if not que:
            errors.append(f"{w}: use sin «llamada: qué devuelve»: {linea[:60]}")
        if llamada.split(" ", 1)[0] in comandos:
            continue
        try:
            arbol = ast.parse(llamada, mode="eval")
        except SyntaxError:
            errors.append(f"{w}: use no es una llamada de Python ni una orden de {sorted(comandos)}: {llamada[:60]}")
            continue
        refs = [(n.value.id, n.attr) for n in ast.walk(arbol)
                if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)]
        if not isinstance(arbol.body, (ast.Call, ast.Subscript)) or not refs:
            errors.append(f"{w}: use debe empezar por modulo.funcion(...): {llamada[:60]}")
        for mod, attr in refs:
            nombres = nombres_modulo(mod)
            if nombres is None:
                errors.append(f"{w}: {mod} no es un módulo de scripts/clientes ({llamada[:60]})")
            elif attr not in nombres:
                errors.append(f"{w}: {mod}.{attr} no existe en scripts/clientes/{mod}.py")
    for h in code.get("mcp") or []:
        if h not in herramientas:
            errors.append(f"{w}: mcp '{h}' no es una herramienta de mcp_catalogo.py ({', '.join(sorted(herramientas))})")
    largo = len(json.dumps(code, ensure_ascii=False, separators=(",", ":")))
    if largo > CODE_MAX:
        errors.append(f"{w}: {largo} caracteres en JSON (máximo {CODE_MAX})")
    return errors


def _str(errors: list[str], where: str, obj: dict, key: str, max_len: int, required: bool = True) -> None:
    val = obj.get(key)
    if val is None:
        if required:
            errors.append(f"{where}: falta '{key}'")
        return
    if not isinstance(val, str) or not val.strip():
        errors.append(f"{where}: '{key}' debe ser texto no vacío")
    elif len(val) > max_len:
        errors.append(f"{where}: '{key}' supera {max_len} caracteres ({len(val)})")


def validate_municipios() -> list[str]:
    """datos/municipios.csv (generado por scripts/municipios.py): columnas fijas, ine único de 5 dígitos, formatos."""
    import csv
    import re
    path = ROOT / "datos" / "municipios.csv"
    if not path.exists():
        return []
    cols = ["ine", "dc", "nombre", "cpro", "ccaa", "provincia", "nuts3", "ine_tempus_id", "sigpac", "sigpac_cruce", "dir3", "nif",
            "lat", "lon", "nucleo"]
    with path.open(encoding="utf-8", newline="") as fh:
        filas = list(csv.DictReader(fh))
    errores = [] if filas and list(filas[0]) == cols else [f"{path.name}: columnas distintas de {cols}"]
    vistos = set()
    for f in filas:
        w = f"{path.name}: {f.get('ine')}"
        if not re.fullmatch(r"\d{5}", f.get("ine") or "") or f["ine"] in vistos or f["ine"][:2] != f.get("cpro"):
            errores.append(f"{w}: ine inválido, repetido o de otra provincia")
        vistos.add(f.get("ine"))
        if f.get("sigpac") and not re.fullmatch(rf"{int(f['cpro'])}:\d{{1,3}}", f["sigpac"]):
            errores.append(f"{w}: sigpac '{f['sigpac']}' no es provincia:municipio")
        if f.get("dir3") and f["dir3"] != f"L01{f['ine']}{f['dc']}":
            errores.append(f"{w}: dir3 '{f['dir3']}' no es L01 + ine + dc")
    if len(filas) < 8000:
        errores.append(f"{path.name}: solo {len(filas)} municipios")
    return errores[:20]


def validate_indices(ids: set[str], vocab: dict) -> list[str]:
    errors: list[str] = []
    idx = load_indices()
    vocab_ids = set(vocab["ids"])

    # recetas
    seen: set[str] = set()
    for r in idx["recetas"]:
        rid = r.get("id", "?")
        w = f"indices/recetas.yaml [{rid}]"
        if not isinstance(rid, str) or not ID_RE.match(rid):
            errors.append(f"{w}: id inválido")
        if rid in seen:
            errors.append(f"{w}: id duplicado")
        seen.add(rid)
        _str(errors, w, r, "intent", 160)
        _str(errors, w, r, "output", 220)
        _str(errors, w, r, "note", 300, required=False)
        for i in r.get("inputs") or []:
            if i not in vocab_ids:
                errors.append(f"{w}: input '{i}' no está en vocab ids")
        steps = r.get("steps") or []
        if not steps:
            errors.append(f"{w}: sin steps")
        for n, s in enumerate(steps, 1):
            sw = f"{w} paso {n}"
            if s.get("source") not in ids:
                errors.append(f"{sw}: source '{s.get('source')}' no es una ficha")
            _str(errors, sw, s, "do", 400)
            _str(errors, sw, s, "example", 600, required=False)
            _str(errors, sw, s, "note", 220, required=False)
        checks = r.get("checks") or []
        if not checks:
            errors.append(f"{w}: sin checks")
        for n, c in enumerate(checks, 1):
            cw = f"{w} check {n}"
            extra = set(c) - CHECK_KEYS
            if extra:
                errors.append(f"{cw}: claves no admitidas {sorted(extra)}")
            if not URL_RE.match(str(c.get("url", ""))):
                errors.append(f"{cw}: url inválida")
            if c.get("method", "GET") not in ("GET", "HEAD", "POST"):
                errors.append(f"{cw}: method inválido")
            for k in ("status", "min_bytes", "read_bytes", "retries"):
                if k in c and not isinstance(c[k], int):
                    errors.append(f"{cw}: '{k}' debe ser entero")
            if "headers" in c and not isinstance(c["headers"], dict):
                errors.append(f"{cw}: headers debe ser un mapa")
            if "contains" in c and not isinstance(c["contains"], str):
                errors.append(f"{cw}: contains debe ser texto")
        ver = r.get("verified", "missing")
        if ver == "missing":
            errors.append(f"{w}: falta 'verified'")
        elif ver is not None and not (isinstance(ver, str) and DATE_RE.match(ver)):
            errors.append(f"{w}: verified debe ser AAAA-MM-DD o null")
        elif ver is None and not r.get("note"):
            errors.append(f"{w}: verified null exige note con lo que falta por probar")

    # rutas muertas
    olds: set[str] = set()
    for d in idx["rutas-muertas"]:
        old = d.get("old", "?")
        w = f"indices/rutas-muertas.yaml [{old}]"
        if not URL_RE.match(str(old)):
            errors.append(f"{w}: old inválida")
        if old in olds:
            errors.append(f"{w}: old duplicada")
        olds.add(old)
        if str(d.get("status")) not in DEAD_STATUS:
            errors.append(f"{w}: status '{d.get('status')}' no está en {sorted(DEAD_STATUS)}")
        if d.get("new") is not None and not URL_RE.match(str(d["new"])):
            errors.append(f"{w}: new debe ser URL o null")
        if d.get("source") not in ids:
            errors.append(f"{w}: source '{d.get('source')}' no es una ficha")
        _str(errors, w, d, "note", 300, required=False)
        if not (isinstance(d.get("checked"), str) and DATE_RE.match(d["checked"])):
            errors.append(f"{w}: checked debe ser AAAA-MM-DD")

    # identificadores
    idents = idx["identificadores"]
    if set(idents) != vocab_ids:
        errors.append(
            f"indices/identificadores.yaml: claves distintas del vocabulario ids; faltan {sorted(vocab_ids - set(idents))}, sobran {sorted(set(idents) - vocab_ids)}"
        )
    for key, info in idents.items():
        w = f"indices/identificadores.yaml [{key}]"
        _str(errors, w, info, "format", 220)
        _str(errors, w, info, "gotcha", 300, required=False)
        rx = info.get("regex")
        if rx is not None:
            try:
                compiled = re.compile(rx)
            except re.error as exc:
                errors.append(f"{w}: regex no compila ({exc})")
                compiled = None
            ex = info.get("example")
            if compiled and ex is not None and not compiled.fullmatch(str(ex)):
                errors.append(f"{w}: example '{ex}' no cumple la regex")
        if info.get("issuer") is not None and info["issuer"] not in ids:
            errors.append(f"{w}: issuer '{info['issuer']}' no es una ficha")
        for j in info.get("joins") or []:
            if j.get("via") not in ids:
                errors.append(f"{w}: join via '{j.get('via')}' no es una ficha")
            _str(errors, w, j, "how", 220)

    # necesidades
    needs: set[str] = set()
    for n in idx["necesidades"]:
        need = n.get("need", "?")
        w = f"indices/necesidades.yaml [{need[:40]}]"
        _str(errors, w, n, "need", 160)
        if need in needs:
            errors.append(f"{w}: need duplicada")
        needs.add(need)
        src = n.get("source", "missing")
        if src == "missing":
            errors.append(f"{w}: falta 'source' (null si no hay fuente)")
        elif src is not None and src not in ids:
            errors.append(f"{w}: source '{src}' no es una ficha")
        elif src is None and not n.get("note"):
            errors.append(f"{w}: source null exige note")
        _str(errors, w, n, "note", 300, required=False)

    # productos
    receta_ids = {r.get("id") for r in idx["recetas"]}
    pids: set[str] = set()
    for p in idx["productos"]:
        pid = p.get("id", "?")
        w = f"indices/productos.yaml [{pid}]"
        if not isinstance(pid, str) or not ID_RE.match(pid):
            errors.append(f"{w}: id inválido")
        if pid in pids:
            errors.append(f"{w}: id duplicado")
        pids.add(pid)
        for k, n in (("producto", 160), ("cliente", 160), ("piezas", 300), ("frescura", 200), ("licencia", 200), ("trampa", 240)):
            _str(errors, w, p, k, n)
        _str(errors, w, p, "volumen", 200, required=False)
        if not p.get("fuentes"):
            errors.append(f"{w}: sin fuentes")
        for s in p.get("fuentes") or []:
            if s not in ids:
                errors.append(f"{w}: fuente '{s}' no es una ficha")
        for r in p.get("recetas") or []:
            if r not in receta_ids:
                errors.append(f"{w}: receta '{r}' no existe")
        if not (isinstance(p.get("verified"), str) and DATE_RE.match(p["verified"])):
            errors.append(f"{w}: verified debe ser AAAA-MM-DD (solo entran productos con piezas probadas)")

    # codigos
    for key, g in (idx["codigos"] or {}).items():
        w = f"indices/codigos.yaml [{key}]"
        if not isinstance(key, str) or not ID_RE.match(key):
            errors.append(f"{w}: clave inválida")
        if g.get("source") not in ids:
            errors.append(f"{w}: source '{g.get('source')}' no es una ficha")
        _str(errors, w, g, "use", 300)
        _str(errors, w, g, "note", 300, required=False)
        ver = g.get("verified")
        if not (isinstance(ver, str) and DATE_RE.match(ver)):
            errors.append(f"{w}: verified debe ser AAAA-MM-DD (los códigos se obtienen con una llamada real)")
        entries = g.get("entries") or []
        if not entries:
            errors.append(f"{w}: sin entries")
        codes: set[str] = set()
        for e in entries:
            code = str(e.get("code", "")).strip()
            if not code:
                errors.append(f"{w}: entrada sin code")
            if code in codes:
                errors.append(f"{w}: code duplicado {code}")
            codes.add(code)
            _str(errors, w, e, "name", 120)
            _str(errors, w, e, "note", 160, required=False)
    return errors


def main() -> int:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    vocab = load_vocab()
    sources = load_sources()
    errors: list[str] = []
    ids = {}
    herramientas = {h["name"] for h in herramientas_mcp()}
    comandos = comandos_paquete()

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
        for q in s.get("quirks", []) or []:
            if q not in vocab["quirks"]:
                errors.append(f"{path}: quirk '{q}' no está en el vocabulario")
        for i in s.get("ids", []) or []:
            if i not in vocab["ids"]:
                errors.append(f"{path}: id '{i}' no está en el vocabulario ids")
        summary = s.get("summary", "")
        if summary and summary.strip().endswith(":"):
            errors.append(f"{path}: summary termina en ':'")
        if isinstance(s.get("code"), dict):
            errors += validate_code(path, s["code"], herramientas, comandos)

    for s in sources:
        for r in s.get("related", []):
            if r not in ids:
                errors.append(f"{s['id']}: related '{r}' no existe")

    n_idx = 0
    try:
        errors += validate_indices(set(ids), vocab)
        n_idx = len(INDEX_FILES)
    except Exception as exc:  # fichero ausente o YAML roto
        errors.append(f"indices/: no se pudieron cargar los índices ({exc})")

    errors += validate_municipios()

    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"\n{len(errors)} error(es) en {len(sources)} fichas", file=sys.stderr)
        return 1
    print(f"OK: {len(sources)} fichas y {n_idx} índices válidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
