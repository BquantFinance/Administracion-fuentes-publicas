#!/usr/bin/env python3
"""Genera los artefactos derivados a partir de sources/**/*.yaml e indices/*.yaml.

Salidas (no editar a mano):
  catalog.json               todas las fichas y los índices, para carga programática
  sources/<sector>/README.md índice compacto por sector, con las necesidades que resuelve
  indices/README.md          recetas, dónde está cada cosa, identificadores y rutas muertas
  llms.txt                   mapa del repo para agentes
  llms-full.txt              todas las fichas en texto compacto
  README.md                  tablas de productos y sectores entre marcadores AUTO
  guides/servidor-mcp.md     lista de herramientas entre marcadores AUTO, sacada de scripts/mcp_catalogo.py
  mcpb/manifest.json         lista de herramientas del paquete MCPB, de la misma fuente
"""
from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from datetime import date

from common import REPO_RAW, ROOT, load_indices, load_sources, load_vocab

REPO_URL = "https://github.com/BquantFinance/Administracion-fuentes-publicas"


def herramientas_mcp() -> list[dict]:
    """Nombre, firma y descripción de cada @mcp.tool() de scripts/mcp_catalogo.py, leídos sin importar el servidor."""
    tree = ast.parse((ROOT / "scripts" / "mcp_catalogo.py").read_text(encoding="utf-8"))
    out = []
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and any(ast.unparse(d) in ("herramienta", "mcp.tool()") for d in n.decorator_list):
            args = n.args.args
            defaults = [None] * (len(args) - len(n.args.defaults)) + list(n.args.defaults)
            firma = ", ".join(a.arg + (f"={ast.unparse(d)}" if d is not None else "") for a, d in zip(args, defaults))
            doc = " ".join((ast.get_docstring(n) or "").split())
            primera = doc.split(". ")[0].rstrip(".") + "."
            out.append({"name": n.name, "firma": f"{n.name}({firma})", "doc": doc, "resumen": primera})
    return out


def auto(texto: str, marca: str, contenido: str) -> str:
    """Sustituye lo que hay entre <!-- AUTO:marca --> y <!-- /AUTO:marca -->."""
    patron = rf"(<!-- AUTO:{marca} -->).*?(<!-- /AUTO:{marca} -->)"
    if not re.search(patron, texto, flags=re.S):
        raise SystemExit(f"falta el marcador AUTO:{marca}")
    return re.sub(patron, lambda m: f"{m.group(1)}\n{contenido}\n{m.group(2)}", texto, flags=re.S)


def clean(s: dict) -> dict:
    return {k: v for k, v in s.items() if not k.startswith("_")}


def fmt_list(v) -> str:
    return ", ".join(v) if isinstance(v, list) else str(v)


def cell(v) -> str:
    return str(v).replace("|", "\\|") if v is not None else "—"


def render_source_compact(s: dict) -> str:
    """Bloque de texto compacto por fuente para llms-full.txt."""
    lines = [f"## {s['id']}", f"{s['name']} | {s['org']}"]
    lines.append(f"summary: {s['summary'].strip()}")
    for a in s.get("alerts", []) or []:
        lines.append(f"!! {a}")
    lines.append(
        f"access: {fmt_list(s['access'])} | auth: {s['auth']} | formats: {fmt_list(s['formats'])} "
        f"| update: {s['update']} | status: {s['status']} | verified: {s.get('verified') or 'pending'}"
    )
    if s.get("coverage"):
        lines.append(f"coverage: {s['coverage']}")
    for k in ("since", "full", "size", "new"):
        if (s.get("sync") or {}).get(k):
            lines.append(f"sync.{k}: {s['sync'][k]}")
    if s.get("license"):
        lines.append(f"license: {s['license']}")
    lines.append(f"base_url: {s['base_url']}")
    if s.get("docs_url"):
        lines.append(f"docs_url: {s['docs_url']}")
    for e in s.get("endpoints", []) or []:
        line = f"- {e['path']} :: {e['desc']}"
        if e.get("params"):
            line += f" [{e['params']}]"
        lines.append(line)
        if e.get("example"):
            lines.append(f"  ej: {e['example']}")
        if e.get("returns"):
            lines.append(f"  devuelve: {e['returns']}")
    if s.get("rate_limit"):
        lines.append(f"rate_limit: {s['rate_limit']}")
    if s.get("quirks"):
        lines.append(f"quirks: {fmt_list(s['quirks'])}")
    if s.get("ids"):
        lines.append(f"ids: {fmt_list(s['ids'])}")
    for g in s.get("gotchas", []) or []:
        lines.append(f"! {g}")
    for tip in s.get("tips", []) or []:
        lines.append(f"+ {tip}")
    if s.get("related"):
        lines.append(f"related: {fmt_list(s['related'])}")
    return "\n".join(lines)


def render_sector_index(sector: str, title: str, items: list[dict], needs: list[dict]) -> str:
    lines = [
        f"# {title}",
        "",
        f"Sector `{sector}` · {len(items)} fuentes · índice generado por `scripts/build.py`, no editar.",
        "",
    ]
    if needs:
        lines += ["## Dónde está cada cosa", ""]
        for n in needs:
            note = f" ({n['note']})" if n.get("note") else ""
            lines.append(f"- {n['need']} → `{n['source']}`{note}")
        lines.append("")
    lines += [
        "| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for s in items:
        lines.append(
            f"| [{s['id']}]({s['id']}.yaml) | {s['name']} | {fmt_list(s['access'])} | {s['auth']} "
            f"| {fmt_list(s['formats'])} | {s['update']} | {fmt_list(s.get('quirks') or []) or '—'} | {s.get('verified') or '—'} |"
        )
    lines.append("")
    for s in items:
        lines.append(f"- **{s['id']}**: {s['summary'].strip()}")
    lines.append("")
    return "\n".join(lines)


def render_indices_readme(idx: dict, sector_of: dict[str, str], vocab: dict, used_by: dict[str, list[str]]) -> str:
    recetas, dead, idents, needs = idx["recetas"], idx["rutas-muertas"], idx["identificadores"], idx["necesidades"]
    codigos = idx["codigos"]
    lines = [
        "# Índices para agentes",
        "",
        f"Generado por `scripts/build.py` a partir de `indices/*.yaml`, no editar. {len(idx['productos'])} productos, {len(recetas)} recetas, "
        f"{len(needs)} necesidades, {len(idents)} identificadores, {len(codigos)} grupos de códigos, {len(dead)} rutas muertas.",
        "",
        "## Productos que se pueden construir hoy",
        "",
        "Cada uno con las fichas, recetas y código del repo que lo resuelven, cifras medidas, licencia y la trampa que más cuesta.",
        "",
    ]
    for p in idx["productos"]:
        lines += [f"**{p['id']}** · {p['producto']}", f"- para: {p['cliente']}", f"- fichas: {', '.join(p['fuentes'])}"
                  + (f" · recetas: {', '.join(p['recetas'])}" if p.get("recetas") else ""), f"- piezas: {p['piezas']}",
                  f"- frescura: {p['frescura']}" + (f" · volumen: {p['volumen']}" if p.get("volumen") else ""),
                  f"- licencia: {p['licencia']}", f"- trampa: {p['trampa']}", ""]
    lines += [
        "## Recetas por intención",
        "",
        "Procedimientos verificados que encadenan fichas. `python scripts/check_recetas.py` ejecuta las comprobaciones "
        "de cada receta contra los servidores reales (batería de regresión).",
        "",
        "| receta | intención | fichas | verificada |",
        "|---|---|---|---|",
    ]
    for r in recetas:
        srcs = []
        for s in r["steps"]:
            if s["source"] not in srcs:
                srcs.append(s["source"])
        lines.append(f"| `{r['id']}` | {cell(r['intent'])} | {', '.join(srcs)} | {r.get('verified') or 'pendiente'} |")
    lines += ["", "### Pasos", ""]
    for r in recetas:
        lines.append(f"**{r['id']}** · {r['intent']}")
        if r.get("inputs"):
            lines.append(f"- entrada: {', '.join(r['inputs'])}")
        for n, s in enumerate(r["steps"], 1):
            lines.append(f"{n}. `{s['source']}`: {s['do']}")
            if s.get("example"):
                lines.append(f"   ```")
                lines.append(f"   {s['example']}")
                lines.append(f"   ```")
        lines.append(f"- salida: {r['output']}")
        if r.get("note"):
            lines.append(f"- nota: {r['note']}")
        lines.append("")
    lines += ["## Dónde está cada cosa", ""]
    by_sector: dict[str, list[dict]] = defaultdict(list)
    for n in needs:
        by_sector[sector_of.get(n["source"], "sin-fuente")].append(n)
    for sector, title in list(vocab["sector"].items()) + [("sin-fuente", "Sin fuente en el catálogo")]:
        items = by_sector.get(sector)
        if not items:
            continue
        lines.append(f"**{title}**")
        for n in items:
            src = f"`{n['source']}`" if n.get("source") else "ninguna"
            note = f" ({n['note']})" if n.get("note") else ""
            lines.append(f"- {n['need']} → {src}{note}")
        lines.append("")
    lines += [
        "## Identificadores para cruzar datos",
        "",
        "| id | formato | regex | ejemplo | emisor | lo usan |",
        "|---|---|---|---|---|---|",
    ]
    for key, info in idents.items():
        rx = f"`{info['regex']}`" if info.get("regex") else "—"
        lines.append(
            f"| {key} | {cell(info['format'])} | {rx} | {cell(info.get('example'))} | {cell(info.get('issuer'))} | {', '.join(used_by.get(key, [])) or '—'} |"
        )
    lines.append("")
    for key, info in idents.items():
        if info.get("gotcha") or info.get("joins"):
            lines.append(f"**{key}**")
            if info.get("gotcha"):
                lines.append(f"- trampa: {info['gotcha']}")
            for j in info.get("joins") or []:
                lines.append(f"- vía `{j['via']}`: {j['how']}")
            lines.append("")
    lines += [
        "## Códigos que son parámetros",
        "",
        "Valores que una API exige y no se adivinan (ids internos, códigos numéricos, indicativos). Obtenidos con una "
        "llamada real en la fecha indicada; la lista completa se saca con la llamada que cita cada grupo.",
        "",
    ]
    for key, g in codigos.items():
        lines.append(f"**{key}** · `{g['source']}` · {g['use']} (verificado {g['verified']})")
        if g.get("note"):
            lines.append(f"- nota: {g['note']}")
        lines.append("- " + " · ".join(
            f"{e['code']}={e['name']}" + (f" ({e['note']})" if e.get("note") else "") for e in g["entries"]
        ))
        lines.append("")
    lines += [
        "## Rutas muertas",
        "",
        "URLs de documentación antigua que ya no sirven y su sustituta verificada.",
        "",
        "| ruta antigua | estado | sustituta | ficha | nota | comprobada |",
        "|---|---|---|---|---|---|",
    ]
    for d in dead:
        lines.append(
            f"| {cell(d['old'])} | {d['status']} | {cell(d.get('new'))} | `{d['source']}` | {cell(d.get('note'))} | {d['checked']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    vocab = load_vocab()
    sources = load_sources()
    idx = load_indices()
    by_sector: dict[str, list[dict]] = defaultdict(list)
    for s in sources:
        by_sector[s["sector"]].append(s)
    for items in by_sector.values():
        items.sort(key=lambda s: s["id"])
    sector_of = {s["id"]: s["sector"] for s in sources}
    used_by: dict[str, list[str]] = defaultdict(list)
    for s in sources:
        for i in s.get("ids") or []:
            used_by[i].append(s["id"])
    needs_by_sector: dict[str, list[dict]] = defaultdict(list)
    for n in idx["necesidades"]:
        if n.get("source"):
            needs_by_sector[sector_of[n["source"]]].append(n)

    # catalog.json
    identificadores = {k: dict(v, used_by=used_by.get(k, [])) for k, v in idx["identificadores"].items()}
    catalog = {
        "name": "Administración fuentes públicas",
        "description": "Catálogo de fuentes de datos de la Administración pública española, optimizado para agentes.",
        "generated": date.today().isoformat(),
        "repo": REPO_URL,
        "schema": f"{REPO_RAW}/schema/source.schema.json",
        "vocab": f"{REPO_RAW}/schema/vocab.yaml",
        "count": len(sources),
        "sectors": {k: v for k, v in vocab["sector"].items() if k in by_sector},
        "sources": [clean(s) for s in sources],
        "indices": {
            "productos": idx["productos"],
            "recetas": idx["recetas"],
            "necesidades": idx["necesidades"],
            "identificadores": identificadores,
            "rutas_muertas": idx["rutas-muertas"],
            "codigos": idx["codigos"],
        },
    }
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    # índices por sector
    for sector, items in by_sector.items():
        (ROOT / "sources" / sector / "README.md").write_text(
            render_sector_index(sector, vocab["sector"][sector], items, needs_by_sector.get(sector, [])),
            encoding="utf-8",
        )

    # índices agregados
    (ROOT / "indices" / "README.md").write_text(
        render_indices_readme(idx, sector_of, vocab, used_by), encoding="utf-8"
    )

    # tabla de sectores (README) siguiendo el orden del vocabulario
    table = ["| sector | descripción | fuentes |", "|---|---|---|"]
    for sector, title in vocab["sector"].items():
        n = len(by_sector.get(sector, []))
        link = f"[{sector}](sources/{sector}/README.md)" if n else f"`{sector}`"
        table.append(f"| {link} | {title} | {n} |")
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = re.sub(
        r"(<!-- AUTO:sectors -->).*?(<!-- /AUTO:sectors -->)",
        lambda m: f"{m.group(1)}\n{chr(10).join(table)}\n{m.group(2)}",
        readme,
        flags=re.S,
    )
    readme = re.sub(
        r"(<!-- AUTO:count -->).*?(<!-- /AUTO:count -->)",
        lambda m: f"{m.group(1)}{len(sources)}{m.group(2)}",
        readme,
        flags=re.S,
    )
    prod = ["| producto | para quién | fichas | piezas |", "|---|---|---|---|"]
    for p in idx["productos"]:
        prod.append(f"| **{p['id']}** · {cell(p['producto'])} | {cell(p['cliente'])} | {', '.join(p['fuentes'])} | {cell(p['piezas'])} |")
    readme = auto(readme, "productos", "\n".join(prod))
    readme_path.write_text(readme, encoding="utf-8")

    tools = herramientas_mcp()
    guia = ROOT / "guides" / "servidor-mcp.md"
    guia.write_text(auto(guia.read_text(encoding="utf-8"), "herramientas",
                         "\n".join(f"- `{h['firma']}`: {h['doc']}" for h in tools)), encoding="utf-8")
    man_path = ROOT / "mcpb" / "manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8"))
    man["tools"] = [{"name": h["name"], "description": h["resumen"]} for h in tools]
    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # llms.txt
    llms = [
        "# Administración fuentes públicas (España)",
        "",
        "> Datos públicos de España listos para construir productos: dónde está cada dato, cómo pedirlo, qué devuelve, "
        "qué trampas tiene (verificadas con llamadas reales) y código que ya lo trae resuelto. Para agentes y desarrolladores. "
        "Contenido en castellano, claves en inglés.",
        "",
        f"Fuentes: {len(sources)} · Productos: {len(idx['productos'])} · Recetas: {len(idx['recetas'])} · Alcance: Administración General del Estado, Madrid, Cataluña, Andalucía, Comunitat Valenciana y los ayuntamientos de Madrid y Barcelona · Generado: {date.today().isoformat()}",
        "",
        "## Empieza aquí",
        "",
        f"- Con MCP: uvx --from git+{REPO_URL} mcp-catalogo. buscar(texto) mira a la vez fichas, recetas, necesidades, productos e identificadores; ficha(id) da endpoints, ejemplos y trampas. Herramientas: " + ", ".join(h["name"] for h in tools) + f" ({REPO_RAW}/guides/servidor-mcp.md).",
        f"- Sin MCP: este fichero para orientarse y la ficha entera antes de llamar: {REPO_RAW}/sources/<sector>/<id>.yaml (alerts primero, endpoints con example y returns, sync, quirks, gotchas). Todo junto en {REPO_RAW}/catalog.json o en texto en {REPO_RAW}/llms-full.txt.",
        f"- Código: pip install \"fuentes-publicas-mcp @ git+{REPO_URL}\". scripts/clientes trae la sesión HTTP con las CA de FNMT y detección de WAF, clientes CKAN, Socrata, PC-Axis, ArcGIS y OGC sin topes silenciosos, cargadores de BOE, BDNS, INE, SEPE y PLACSP, y el almacén local en Parquet (almacen.py). Proyectos que funcionan en ejemplos/.",
        f"- Recursos: municipios con su código en cada sistema ({REPO_RAW}/datos/municipios.csv), códigos que son parámetros ({REPO_RAW}/indices/codigos.yaml), licencias y datos personales ({REPO_RAW}/guides/reutilizacion.md), almacén local ({REPO_RAW}/guides/almacen.md), cliente HTTP ({REPO_RAW}/guides/cliente-http.md).",
        "",
        "## Qué se puede construir hoy",
        "",
        f"Detalle (frescura, volumen, licencia, trampa) en {REPO_RAW}/indices/productos.yaml.",
        "",
    ]
    for p in idx["productos"]:
        llms.append(f"- {p['id']}: {p['producto']} → {', '.join(p['fuentes'])} · {p['piezas']}")
    llms += [
        "",
        "## Reglas rápidas antes de programar contra una fuente",
        "",
        "- Lee primero `alerts` de la ficha: son trampas silenciosas (datos incompletos, distintos o cero sin error) y cambian la cifra que darías.",
        "- Lee `quirks`, `ids` y `gotchas` de la ficha: son hechos verificados con llamadas reales, no documentación oficial. `quirks` dice cómo configurar el cliente; `ids` con qué otras fuentes se cruza.",
        "- Muchos servidores .gob.es sirven certificados FNMT sin la cadena intermedia; curl y requests fallan hasta añadirla al bundle. Arreglo copiable en la guía Cliente HTTP (`python scripts/fnmt_bundle.py` genera ca-age.pem).",
        "- Envía siempre User-Agent y Accept de navegador; varios sitios (tesoro.es, seg-social.es) devuelven 403 a los valores por defecto de curl y requests.",
        "- Las APIs del BOE exigen Accept explícito (application/json o application/xml) y devuelven los errores siempre en XML.",
        "- Espera ISO-8859-1 en feeds del BOE y CSV del Banco de España; convierte antes de parsear.",
        "- Ninguna fuente verificada documenta límites ni devolvió 429; para descargas masivas, peticiones secuenciales y reintento con espera ante 5xx. El Catastro bloquea la IP tras ráfagas de unas 15 peticiones y rechaza rangos de centros de datos (GitHub Actions incluido); Catastro, REData, datos.gob.es, BNE y FEGA se verifican mejor desde una IP residencial.",
        "- Si una URL que recuerdas falla, busca en la tabla de rutas muertas antes de dar la fuente por perdida.",
        "",
        "## Trampas silenciosas",
        "",
        "Datos incompletos, distintos o a cero sin ningún error; están en `alerts` de cada ficha.",
        "",
    ]
    for s in sorted(sources, key=lambda x: x["id"]):
        for a in s.get("alerts", []) or []:
            llms.append(f"- {s['id']}: {a}")
    llms += [
        "",
        "## Dónde está cada cosa",
        "",
    ]
    for n in idx["necesidades"]:
        src = f"{n['source']}" if n.get("source") else "ninguna"
        note = f" ({n['note']})" if n.get("note") else ""
        llms.append(f"- {n['need']} → {src}{note}")
    llms += ["", "## Recetas por intención", "", f"Pasos, ejemplos y comprobaciones en {REPO_RAW}/indices/recetas.yaml", ""]
    for r in idx["recetas"]:
        srcs = []
        for s in r["steps"]:
            if s["source"] not in srcs:
                srcs.append(s["source"])
        llms.append(f"- {r['id']}: {r['intent']} → {', '.join(srcs)}")
    llms += ["", "## Sectores", ""]
    for sector, title in vocab["sector"].items():
        items = by_sector.get(sector)
        if not items:
            continue
        ids = ", ".join(s["id"] for s in items)
        llms.append(f"- [{title}]({REPO_RAW}/sources/{sector}/README.md): {ids}")
    llms += ["", "## Guías transversales", ""]
    for g in sorted((ROOT / "guides").glob("*.md")):
        title = g.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        llms.append(f"- [{title}]({REPO_RAW}/guides/{g.name})")
    llms += ["", "## Optional", "", f"- [Contribuir]({REPO_RAW}/CONTRIBUTING.md)", f"- [Plantilla de ficha]({REPO_RAW}/templates/source.yaml)", ""]
    (ROOT / "llms.txt").write_text("\n".join(llms), encoding="utf-8")

    # llms-min.txt: entrada ligera (empezar, productos por id, reglas, fichas con alertas y fichas por sector)
    corte = llms.index("## Qué se puede construir hoy")
    mini = llms[:corte]
    mini[4] = mini[4].replace("Generado:", "Entrada ligera; la completa es llms.txt · Generado:")
    mini += ["## Qué se puede construir hoy", "", ", ".join(p["id"] for p in idx["productos"]) + f" (detalle en {REPO_RAW}/indices/productos.yaml).", ""]
    mini += llms[llms.index("## Reglas rápidas antes de programar contra una fuente"): llms.index("## Trampas silenciosas")]
    con_alertas = [s["id"] for s in sorted(sources, key=lambda x: x["id"]) if s.get("alerts")]
    mini += ["## Fichas con trampas silenciosas", "", "Lee sus alerts antes de dar una cifra: " + ", ".join(con_alertas) + ".", ""]
    mini += ["## Fichas por sector", ""]
    for sector, title in vocab["sector"].items():
        items = by_sector.get(sector)
        if items:
            mini.append(f"- {title}: " + ", ".join(s["id"] for s in items))
    mini.append("")
    (ROOT / "llms-min.txt").write_text("\n".join(mini), encoding="utf-8")

    # llms-full.txt
    full = [llms[0], "", llms[2], "", f"Fuentes: {len(sources)} · Generado: {date.today().isoformat()} · Formato: un bloque por fuente; '!!' marca trampas silenciosas (datos incompletos o distintos sin error); '!' marca trampas; '+' marca consejos; 'ej:' es una llamada lista para copiar. Recetas, identificadores y rutas muertas en indices/README.md.", ""]
    for sector, title in vocab["sector"].items():
        items = by_sector.get(sector)
        if not items:
            continue
        full.append(f"# SECTOR {sector}: {title}")
        full.append("")
        for s in items:
            full.append(render_source_compact(s))
            full.append("")
    (ROOT / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")

    print(
        f"build OK: {len(sources)} fuentes, {len(by_sector)} sectores, {len(idx['productos'])} productos, {len(idx['recetas'])} recetas, "
        f"{len(idx['necesidades'])} necesidades, {len(idx['codigos'])} grupos de códigos, {len(idx['rutas-muertas'])} rutas muertas"
    )


if __name__ == "__main__":
    main()
