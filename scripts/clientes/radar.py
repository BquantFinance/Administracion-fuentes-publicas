#!/usr/bin/env python3
"""Radar: lo nuevo de cada día en licitaciones (PLACSP), convocatorias de ayudas (BDNS), BOE y sociedades recién
constituidas (BORME), filtrado por un radar.yaml y recordando lo ya visto. Pensado para un cron de GitHub Actions
(plantilla en ejemplos/radar/): cada mañana un issue, un RSS y un JSON con solo lo nuevo, sin servidores.

Uso: fuentes-radar radar.yaml [--estado radar/estado.json] [--salida radar] [--dias 3]
     python scripts/clientes/radar.py ejemplos/radar/radar.yaml

Trampas que resuelve: el feed de PLACSP repite cada expediente en cada cambio de estado (vale el primero visto) y la
página de bloqueo de su WAF se lanza como error, no como cero; la BDNS sin pageSize se queda en 50; el BOE no sale los
domingos (404); el BORME A de cada provincia es un documento aparte y su número 99 es el índice; los nombres de
administradores y socios del BORME son datos personales y no se publican (solo el acto de constitución).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import unicodedata
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

try:
    from . import bdns, boe, placsp
    from .almacen import FEEDS
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    import bdns
    import boe
    import placsp
    from almacen import FEEDS

FUENTES = ("licitaciones", "ayudas", "boe", "sociedades", "concursos")
MAX_VISTOS = 20000  # por fuente; los más antiguos se olvidan
MAX_RSS = 200


def norm(s: str | None) -> str:
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def casa(texto: str | None, palabras: list[str] | None) -> bool:
    """Sin palabras, todo casa; con palabras, basta una, sin tildes ni mayúsculas («subvención» casa «subvenciones»)."""
    return not palabras or any(norm(p) in norm(texto) for p in palabras)


def _lista(cfg: dict, clave: str) -> list[str]:
    v = cfg.get(clave) or []
    return [str(x) for x in (v if isinstance(v, list) else [v])]


def filtrar_licitaciones(entradas: list[dict], cfg: dict) -> list[dict]:
    """La más reciente de cada expediente (el feed va de nuevo a antiguo), sin anulaciones, por estado (PUB por defecto:
    en plazo), prefijo CPV, NUTS, importe mínimo sin IVA y palabras en el objeto o el órgano."""
    ultimas: dict[str, dict] = {}
    for e in entradas:
        ultimas.setdefault(e["id"], e)
    estados = _lista(cfg, "estados") or ["PUB"]
    cpv, nuts, palabras = _lista(cfg, "cpv"), _lista(cfg, "nuts"), _lista(cfg, "palabras")
    minimo = float(cfg.get("importe_min") or 0)
    out = []
    for e in ultimas.values():
        if e.get("deleted") or (estados != ["*"] and e.get("estado") not in estados):
            continue
        if cpv and not any(c.startswith(p) for c in e.get("cpv") or [] for p in cpv):
            continue
        if nuts and not any((e.get("nuts") or "").startswith(n) for n in nuts):
            continue
        importe = float(e["importe_sin_iva"]) if e.get("importe_sin_iva") else None
        if minimo and (importe is None or importe < minimo):
            continue
        if not casa(f"{e.get('objeto')} {e.get('organo')}", palabras):
            continue
        out.append({"fuente": "licitaciones", "id": e["id"], "fecha": (e.get("fecha_publicacion") or e.get("updated") or "")[:10],
                    "titulo": e.get("objeto"), "detalle": f"{e.get('organo') or ''} · CPV {','.join(e.get('cpv') or [])[:40]}"
                    + (f" · plazo {e['plazo_presentacion']}" if e.get("plazo_presentacion") else ""),
                    "importe": importe, "url": e.get("link")})
    return sorted(out, key=lambda x: x["importe"] or 0, reverse=True)


def filtrar_ayudas(convocatorias: list[dict], cfg: dict) -> list[dict]:
    """Convocatorias de la BDNS por palabras en la descripción u órgano y por nivel (ESTADO, AUTONOMICA, LOCAL, OTROS)."""
    niveles, palabras = [n.upper() for n in _lista(cfg, "nivel")], _lista(cfg, "palabras")
    out = []
    for c in convocatorias:
        organo = " ".join(x for x in (c.get("nivel1"), c.get("nivel2"), c.get("nivel3")) if x)
        if niveles and (c.get("nivel1") or "").upper() not in niveles:
            continue
        if not casa(f"{c.get('descripcion')} {organo}", palabras):
            continue
        num = c.get("numeroConvocatoria")
        out.append({"fuente": "ayudas", "id": str(num), "fecha": c.get("fechaRecepcion"), "titulo": c.get("descripcion"),
                    "detalle": organo, "importe": None,
                    "url": f"https://www.infosubvenciones.es/bdnstrans/GE/es/convocatorias/{num}"})
    return out


def filtrar_boe(items: list[dict], cfg: dict) -> list[dict]:
    """Items del sumario por sección (1, 2A, 2B, 3, 4, 5A...), departamento y palabras en el título."""
    secciones, deps, palabras = _lista(cfg, "secciones"), _lista(cfg, "departamentos"), _lista(cfg, "palabras")
    out = []
    for i in items:
        if secciones and str(i.get("seccion_codigo")) not in secciones:
            continue
        if deps and not casa(i.get("departamento_nombre"), deps):
            continue
        if not casa(i.get("titulo"), palabras):
            continue
        out.append({"fuente": "boe", "id": i["identificador"], "fecha": i.get("fecha"), "titulo": i.get("titulo"),
                    "detalle": i.get("departamento_nombre"), "importe": None, "url": i.get("url_html")})
    return out


def filtrar_sociedades(empresas: list[dict], cfg: dict) -> list[dict]:
    """Constituciones del BORME A ({provincia, documento, fecha, empresa de boe.parse_borme_a}) por palabras en el objeto
    social y capital mínimo. Solo el texto del acto de constitución: nada de nombramientos ni socios (datos personales)."""
    palabras, minimo = _lista(cfg, "palabras"), float(cfg.get("capital_min") or 0)
    out = []
    for x in empresas:
        e = x["empresa"]
        cons = next((a["texto"] for a in e["actos"] if a["tipo"] == "Constitución"), None)
        if cons is None or not casa(cons, palabras):
            continue
        capital = None
        if "Capital:" in cons:
            cifra = cons.split("Capital:")[1].split("Euros")[0].strip().rstrip(".")
            try:
                capital = float(cifra.replace(".", "").replace(",", "."))
            except ValueError:
                pass
        if minimo and (capital is None or capital < minimo):
            continue
        out.append({"fuente": "sociedades", "id": f"{x['documento']}#{e['numero']}", "fecha": x.get("fecha"),
                    "titulo": e["denominacion"], "detalle": f"{x.get('provincia') or ''} · {cons[:300]}", "importe": capital,
                    "url": f"https://www.boe.es/diario_borme/txt.php?id={x['documento']}"})
    return out


def _clave_empresa(s: str | None) -> str:
    try:
        from .almacen import _norm_nombre
    except ImportError:
        from almacen import _norm_nombre
    return _norm_nombre(s)


def filtrar_concursos(empresas: list[dict], cfg: dict, nombres: list[str] | None = None) -> list[dict]:
    """Actos «Situación concursal» del BORME A ({provincia, documento, fecha, empresa}) de las empresas vigiladas (nombres
    ya resueltos; sin lista, todas) y por palabras en la resolución (declaración, liquidación, conclusión, calificación).
    Solo los campos de boe.parse_concursal: sin juez, administradores ni inhabilitados."""
    claves = {_clave_empresa(n) for n in nombres or []}
    resol = _lista(cfg, "resoluciones")
    out = []
    for x in empresas:
        e = x["empresa"]
        if claves and _clave_empresa(e["denominacion"]) not in claves:
            continue
        for a in e["actos"]:
            c = boe.parse_concursal(a["texto"]) if a["tipo"] == "Situación concursal" else None
            if not c or not casa(c.get("resolucion"), resol):
                continue
            out.append({"fuente": "concursos", "id": f"{x['documento']}#{e['numero']}#{c['procedimiento']}#{c['resolucion']}",
                        "fecha": c.get("fecha_resolucion"), "titulo": e["denominacion"],
                        "detalle": " · ".join(str(v) for v in (x.get("provincia"), c.get("resolucion"), c.get("clase"),
                                              c.get("calificacion"), f"procedimiento {c.get('procedimiento')}",
                                              f"resolución {c.get('fecha_resolucion')}", c.get("juzgado")) if v),
                        "importe": None, "url": f"https://www.boe.es/diario_borme/txt.php?id={x['documento']}"})
    return out


def vigiladas(cfg: dict, log=print) -> list[str]:
    """Nombres de las empresas de concursos.empresas; un NIF se traduce a sus nombres con el directorio de la BDNS."""
    import re
    nombres = []
    for v in _lista(cfg, "empresas"):
        if re.fullmatch(r"[A-Za-z]\d{7}[0-9A-Za-z]", v.strip()):
            hallados = [n for e in bdns.terceros(v.strip().upper())["empresas"] for n in e["nombres"]]
            if not hallados:
                log(f"concursos: sin nombre para el NIF {v} en la BDNS; ponlo por su denominación")
            nombres += hallados
        else:
            nombres.append(v)
    return nombres


def _dias(desde: date, hasta: date) -> list[date]:
    return [desde + timedelta(days=i) for i in range((hasta - desde).days + 1)]


def recoger(cfg: dict, desde: date, hasta: date, log=print, errores: dict | None = None) -> list[dict]:
    """Llama a las fuentes configuradas y devuelve los candidatos filtrados (sin quitar aún lo ya visto). Con errores (un
    dict), una fuente que falla (PLACSP bloqueado, BDNS caída) se anota ahí y las demás siguen; sin él, el error sube."""
    out: list[dict] = []

    def aparte(fuentes: tuple, fn) -> None:
        if errores is None:
            return fn()
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            for f in fuentes:
                errores.setdefault(f, f"{type(exc).__name__}: {str(exc)[:200]}")
            log(f"{', '.join(fuentes)}: {type(exc).__name__}: {str(exc)[:200]}")

    def licitaciones() -> None:
        c = cfg["licitaciones"] or {}
        entradas = []
        for feed in _lista(c, "feeds") or ["643", "1044"]:
            entradas += list(placsp.entradas(FEEDS[feed] + ".atom", max_paginas=int(c.get("paginas") or 1)))
        out.extend(filtrar_licitaciones(entradas, c))
        log(f"licitaciones: {len(entradas)} entradas leídas")

    def ayudas() -> None:
        c = cfg["ayudas"] or {}
        convs = list(bdns.buscar("convocatorias", fechaDesde=bdns.fecha_bdns(desde), fechaHasta=bdns.fecha_bdns(hasta),
                                 order="fechaRecepcion", direccion="desc"))
        out.extend(filtrar_ayudas(convs, c))
        log(f"ayudas: {len(convs)} convocatorias desde {desde}")

    if "licitaciones" in cfg:
        aparte(("licitaciones",), licitaciones)
    if "ayudas" in cfg:
        aparte(("ayudas",), ayudas)
    nombres: list[str] = []
    if "concursos" in cfg:
        aparte(("concursos",), lambda: nombres.extend(vigiladas(cfg["concursos"] or {}, log)))
    for dia in _dias(desde, hasta) if ("boe" in cfg or "sociedades" in cfg or "concursos" in cfg) else []:
        if "boe" in cfg:
            aparte(("boe",), lambda dia=dia: out.extend(filtrar_boe(list(boe.items(s)), cfg["boe"] or {})
                                                        if (s := boe.sumario(dia)) else []))
        borme = tuple(b for b in ("sociedades", "concursos") if b in cfg)
        if borme:
            aparte(borme, lambda dia=dia: out.extend(_borme_dia(cfg, dia, nombres)))
    return out


def _borme_dia(cfg: dict, dia: date, nombres: list[str]) -> list[dict]:
    """Constituciones y concursos de un día del BORME A, con una sola descarga por provincia para los dos bloques."""
    out: list[dict] = []
    if "sociedades" in cfg or "concursos" in cfg:
        s = boe.sumario(dia, "borme")
        # si uno de los dos bloques no filtra provincias, se bajan todas
        prov = [_lista(cfg[b] or {}, "provincias") for b in ("sociedades", "concursos") if b in cfg]
        provincias = [] if any(not p for p in prov) else [norm(x) for p in prov for x in p]
        empresas = []
        for it in boe.items(s) if s else []:
            ident = it["identificador"]
            if not ident.startswith("BORME-A") or ident.endswith("-99"):  # el 99 es el índice alfabético
                continue
            if provincias and ident.rsplit("-", 1)[1] not in provincias and norm(it.get("titulo")) not in provincias:
                continue
            empresas += [{"documento": ident, "provincia": it.get("titulo"), "fecha": dia.isoformat(), "empresa": e}
                         for e in boe.borme_empresas(ident)]
        for b, f in (("sociedades", filtrar_sociedades), ("concursos", None)):
            if b not in cfg:
                continue
            c = cfg[b] or {}
            propias = [x for x in empresas if not _lista(c, "provincias") or
                       x["documento"].rsplit("-", 1)[1] in _lista(c, "provincias") or norm(x["provincia"]) in [norm(p) for p in _lista(c, "provincias")]]
            out += f(propias, c) if f else filtrar_concursos(propias, c, nombres)
    return out


def rss(items: list[dict], titulo: str) -> str:
    ahora = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    partes = [f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{escape(titulo)}</title>'
              f"<link>https://github.com/BquantFinance/Administracion-fuentes-publicas</link>"
              f"<description>Radar de datos públicos</description><lastBuildDate>{ahora}</lastBuildDate>"]
    for i in items:
        desc = escape(" · ".join(x for x in (i.get("detalle"), f"{i['importe']:,.2f} €" if i.get("importe") else None) if x))
        titulo_item = escape(("[" + i["fuente"] + "] " + (i.get("titulo") or ""))[:300])
        partes.append(f"<item><title>{titulo_item}</title>"
                      f"<link>{escape(i.get('url') or '')}</link><guid isPermaLink=\"false\">{escape(i['fuente'] + ':' + i['id'])}</guid>"
                      f"<description>{desc}</description></item>")
    return "".join(partes) + "</channel></rss>\n"


def markdown(nuevos: list[dict], fecha: date, errores: dict | None = None) -> str:
    aviso = "".join(f"- {f}: {e}\n" for f, e in (errores or {}).items())
    aviso = f"\n## Fuentes con error (se reintentan en la próxima ejecución)\n\n{aviso}" if aviso else ""
    if not nuevos:
        return f"Radar {fecha}: nada nuevo.\n{aviso}"
    lineas = [f"Radar {fecha}: {len(nuevos)} novedades.\n"]
    for f in FUENTES:
        grupo = [i for i in nuevos if i["fuente"] == f]
        if grupo:
            lineas.append(f"\n## {f.capitalize()} ({len(grupo)})\n")
            for i in grupo[:100]:
                importe = f" · {i['importe']:,.0f} €" if i.get("importe") else ""
                lineas.append(f"- [{(i.get('titulo') or '')[:160]}]({i.get('url') or ''}){importe}  \n  {(i.get('detalle') or '')[:240]}")
            if len(grupo) > 100:
                lineas.append(f"- … y {len(grupo) - 100} más en ultimo.json")
    return "\n".join(lineas) + "\n" + aviso


def ejecutar(cfg: dict, estado_path: Path, salida: Path, dias: int = 3, hoy: date | None = None, log=print) -> dict:
    hoy = hoy or date.today()
    estado = json.loads(estado_path.read_text(encoding="utf-8")) if estado_path.is_file() else {}
    ultima = date.fromisoformat(estado["ultima"]) if estado.get("ultima") else None
    desde = max(ultima, hoy - timedelta(days=dias)) if ultima else hoy - timedelta(days=dias)
    errores: dict = {}
    candidatos = recoger(cfg, desde, hoy, log, errores)
    vistos = {f: set(estado.get("vistos", {}).get(f, [])) for f in FUENTES}
    nuevos = [i for i in candidatos if i["id"] not in vistos[i["fuente"]]]
    nuevos = list({(i["fuente"], i["id"]): i for i in nuevos}.values())
    for i in nuevos:
        vistos[i["fuente"]].add(i["id"])
    recientes = (nuevos + estado.get("recientes", []))[:MAX_RSS]
    # con una fuente caída no se avanza la fecha: la próxima pasada vuelve a cubrir esos días (lo visto no se repite)
    estado = {"ultima": (estado.get("ultima") if errores and ultima else hoy.isoformat()),
              "vistos": {f: sorted(v)[-MAX_VISTOS:] for f, v in vistos.items() if v}, "recientes": recientes}
    salida.mkdir(parents=True, exist_ok=True)
    estado_path.parent.mkdir(parents=True, exist_ok=True)
    estado_path.write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")
    resumen = {"fecha": hoy.isoformat(), "desde": desde.isoformat(), "nuevos": len(nuevos),
               "por_fuente": {f: sum(1 for i in nuevos if i["fuente"] == f) for f in FUENTES if f in cfg},
               "errores": errores, "items": nuevos}
    (salida / "ultimo.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1), encoding="utf-8")
    (salida / "ultimo.md").write_text(markdown(nuevos, hoy, errores), encoding="utf-8")
    (salida / "feed.xml").write_text(rss(recientes, cfg.get("titulo") or "Radar de datos públicos"), encoding="utf-8")
    return resumen


def main(argv: list[str] | None = None) -> int:
    import yaml
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("config", help="radar.yaml con los bloques licitaciones, ayudas, boe y sociedades")
    p.add_argument("--estado", default="radar/estado.json", help="lo ya visto (se sube al repositorio en el workflow)")
    p.add_argument("--salida", default="radar", help="carpeta para ultimo.md, ultimo.json y feed.xml")
    p.add_argument("--dias", type=int, default=3, help="días hacia atrás en la primera ejecución o tras un hueco")
    a = p.parse_args(argv)
    cfg = yaml.safe_load(Path(a.config).read_text(encoding="utf-8")) or {}
    t0 = time.monotonic()
    r = ejecutar(cfg, Path(a.estado), Path(a.salida), a.dias, log=lambda m: print(m, file=sys.stderr, flush=True))
    print(Path(a.salida, "ultimo.md").read_text(encoding="utf-8"))
    # el resumen va al final de stdout: un tail del log lo conserva (en stderr salía antes del informe)
    print(f"radar: {r['nuevos']} nuevos {r['por_fuente']} en {time.monotonic() - t0:.0f} s"
          + (f"; con error {sorted(r['errores'])}" if r["errores"] else ""))
    configuradas = [f for f in FUENTES if f in cfg]
    return 1 if configuradas and set(configuradas) <= set(r["errores"]) else 0  # solo si fallan todas


if __name__ == "__main__":
    sys.exit(main())
