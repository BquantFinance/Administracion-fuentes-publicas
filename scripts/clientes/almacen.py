"""Almacén local en Parquet, sincronizado día a día y consultable con DuckDB: BOE, BORME, BDNS, PLACSP y carburantes.

No publica nada ni sube datos al repo: cada uno se baja lo que necesita en su carpeta (./almacen o FUENTES_ALMACEN).
Un Parquet por tabla y mes ({dir}/{tabla}/{AAAA-MM}.parquet), deduplicado por clave, y estado.json con lo ya cargado:
repetir sync solo baja lo nuevo y se puede cortar y seguir. Lo que mide cada fuente (desde cuándo, tamaño, tiempo) está
en el campo sync de su ficha.

Datos personales (guides/reutilizacion.md): las personas físicas de la BDNS y los adjudicatarios de PLACSP con DNI, NIE o
NIF enmascarado se guardan sin NIF, nombre ni idPersona (persona_fisica = true), para que los totales cuadren sin
identificar a nadie. Del BORME se guarda el tipo de cada acto y solo el texto de los que no llevan nombres de personas
(constitución, domicilio, capital, objeto, denominación, disolución...).

Tablas: boe (un item del sumario por fila), borme (una empresa de la sección A por fila), bdns (concesiones, minimis y
ayudas de Estado por fecha de alta; en minimis el importe va en ayuda_equivalente), placsp y placsp_adjudicaciones (una
fila por versión de cada expediente y por adjudicatario, updated en UTC; vistas placsp_ultimo (última versión no anulada,
con anulada y anulada_el) y adjudicaciones_ultimo (con
adjudicatarios e importe_compartido: en acuerdos marco el importe del lote se repite en cada adjudicatario) con
el último estado) y carburantes (precio por estación y día).

Uso: python scripts/clientes/almacen.py sync [--fuentes boe,borme,bdns,placsp,carburantes] [--desde AAAA-MM-DD]
                                          [--hasta AAAA-MM-DD] [--minutos N] [--dir almacen]
     python scripts/clientes/almacen.py zip-placsp AAAAMM|AAAA [--feeds 643,1044,1143]   meses fuera de la cadena del feed
     python scripts/clientes/almacen.py sql "select ..."                                 solo lectura
     python scripts/clientes/almacen.py empresa NIF                                      contratos, subvenciones y BORME
     python scripts/clientes/almacen.py estado
Necesita duckdb (pip install duckdb).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import time
import unicodedata
import zipfile
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Iterator

try:
    from . import bdns, boe, placsp
    from .sesion import json as json_r, sesion
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    import bdns
    import boe
    import placsp
    from sesion import json as json_r, sesion


def directorio(d: str | os.PathLike | None = None) -> Path:
    return Path(d or os.environ.get("FUENTES_ALMACEN") or "almacen").resolve()


@dataclass
class Tabla:
    columnas: dict[str, str]  # nombre -> tipo de DuckDB
    clave: tuple[str, ...]
    orden: str  # columna que decide la versión que se queda ante claves repetidas


PRODUCTOS = ("Adblue", "Amoniaco", "Biodiesel", "Bioetanol", "Biogas Natural Comprimido", "Biogas Natural Licuado",
             "Diésel Renovable", "Gas Natural Comprimido", "Gas Natural Licuado", "Gases licuados del petróleo",
             "Gasoleo A", "Gasoleo B", "Gasoleo Premium", "Gasolina 95 E10", "Gasolina 95 E25", "Gasolina 95 E5",
             "Gasolina 95 E5 Premium", "Gasolina 95 E85", "Gasolina 98 E10", "Gasolina 98 E5", "Gasolina Renovable",
             "Hidrogeno", "Metanol")


def _snake(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


V, D, F, B = "VARCHAR", "DATE", "DOUBLE", "BOOLEAN"
TABLAS: dict[str, Tabla] = {
    "boe": Tabla({"fecha": D, "diario_numero": V, "seccion_codigo": V, "seccion_nombre": V, "departamento_codigo": V,
                  "departamento_nombre": V, "epigrafe_nombre": V, "identificador": V, "titulo": V, "url_pdf": V,
                  "pdf_bytes": "BIGINT", "url_html": V, "url_xml": V}, ("identificador",), "fecha"),
    "borme": Tabla({"fecha": D, "documento": V, "provincia": V, "numero": V, "denominacion": V, "registro": V,
                    "actos": "VARCHAR[]", "detalle": V, "capital": F, "datos_registrales": V}, ("documento", "numero"), "fecha"),
    "bdns": Tabla({"coleccion": V, "id": "BIGINT", "cod_concesion": V, "numero_convocatoria": V, "convocatoria": V,
                   "convocante": V, "fecha_concesion": D, "fecha_alta": D, "persona_fisica": B, "nif": V, "beneficiario": V,
                   "id_persona": "BIGINT", "instrumento": V, "importe": F, "ayuda_equivalente": F, "reglamento": V,
                   "objetivo": V, "sector": V, "url_br": V}, ("coleccion", "id"), "fecha_alta"),
    "placsp": Tabla({"feed": V, "id": V, "updated": "TIMESTAMP", "borrado": B, "motivo": V, "expediente": V, "estado": V,
                     "organo": V, "organo_dir3": V, "organo_nif": V, "organo_plataforma": V, "objeto": V, "tipo": V,
                     "procedimiento": V, "importe_sin_iva": F, "importe_total": F, "valor_estimado": F, "cpv": "VARCHAR[]",
                     "nuts": V, "plazo_presentacion": D, "fecha_publicacion": D, "link": V}, ("id", "updated"), "updated"),
    "placsp_adjudicaciones": Tabla({"feed": V, "id": V, "updated": "TIMESTAMP", "n": "INTEGER", "expediente": V,
                                    "organo_nif": V, "organo_dir3": V, "lote": V, "resultado": V, "fecha_adjudicacion": D,
                                    "ofertas": "INTEGER", "pyme": B, "persona_fisica": B, "nif": V, "nombre": V,
                                    "importe_sin_iva": F, "importe_total": F, "contrato": V, "fecha_contrato": D},
                                   ("id", "updated", "n"), "updated"),
    "carburantes": Tabla({"fecha": D, "ideess": V, "rotulo": V, "direccion": V, "cp": V, "localidad": V, "municipio": V,
                          "id_municipio": V, "provincia": V, "id_provincia": V, "id_ccaa": V, "latitud": F, "longitud": F,
                          "margen": V, "horario": V, "tipo_venta": V, **{_snake(p): F for p in PRODUCTOS}},
                         ("fecha", "ideess"), "fecha"),
}


# --- conversión de cada fuente a filas ------------------------------------------------------------------------------

def _fecha(v) -> str | None:
    """AAAAMMDD, AAAA-MM-DD o dd/mm/aaaa a ISO; None si no es una fecha."""
    if not v:
        return None
    s = str(v).strip()
    if m := re.fullmatch(r"(\d{4})(\d{2})(\d{2})", s):
        return "-".join(m.groups())
    if m := re.match(r"(\d{4}-\d{2}-\d{2})", s):
        return m.group(1)
    if m := re.match(r"(\d{2})/(\d{2})/(\d{4})", s):
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    return None


def _num(v) -> float | None:
    """Número con punto decimal (BDNS, PLACSP) o con coma y punto de miles (MINETUR, BORME); '' es None."""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def filas_boe(dia: date) -> dict[str, list[dict]]:
    s = boe.sumario(dia)
    if not s:
        return {}
    cols = TABLAS["boe"].columnas
    filas = []
    for it in boe.items(s):
        f = {k: it.get(k) for k in cols}
        f["fecha"] = _fecha(it.get("fecha")) or dia.isoformat()
        f["diario_numero"] = str(it["diario_numero"]) if it.get("diario_numero") is not None else None
        filas.append(f)
    return {"boe": filas}


# Actos del BORME cuyo texto no lleva nombres de personas; del resto (nombramientos, ceses, revocaciones, socio único,
# situación concursal, fe de erratas...) solo se guarda el tipo.
ACTOS_CON_TEXTO = {"Constitución", "Cambio de domicilio social", "Cambio de objeto social", "Ampliación del objeto social",
                   "Cambio de denominación social", "Modificaciones estatutarias", "Ampliación de capital",
                   "Reducción de capital", "Disolución", "Extinción", "Transformación de sociedad", "Fusión por absorción",
                   "Escisión parcial", "Escisión total", "Cierre provisional hoja registral", "Reapertura hoja registral",
                   "Página web de la sociedad", "Desembolso de dividendos pasivos", "Adaptación Ley 2/95"}


def fila_borme(empresa: dict, fecha: str, documento: str, provincia: str | None) -> dict:
    actos = [a["tipo"] or "Otros" for a in empresa["actos"]]
    partes = [f"{a['tipo']}: {a['texto']}" for a in empresa["actos"] if a["tipo"] in ACTOS_CON_TEXTO and a["texto"]]
    for a in empresa["actos"]:  # el texto concursal lleva juez, administradores e inhabilitados: solo los campos
        c = boe.parse_concursal(a["texto"]) if a["tipo"] == "Situación concursal" else None
        if c:
            partes.append("Situación concursal: " + ", ".join(f"{k} {v}" for k, v in c.items() if v is not None))
    detalle = " | ".join(partes)
    capital = None
    for a in empresa["actos"]:
        if a["tipo"] in ("Ampliación de capital", "Reducción de capital"):
            m = re.search(r"Resultante Suscrito:\s*([\d.,]+)", a["texto"])
        elif a["tipo"] == "Constitución":
            m = re.search(r"Capital:\s*([\d.,]+)", a["texto"])
        else:
            m = None
        if m:
            capital = _num(m.group(1))
    return {"fecha": fecha, "documento": documento, "provincia": provincia, "numero": str(empresa["numero"]),
            "denominacion": empresa["denominacion"], "registro": empresa["registro"], "actos": actos,
            "detalle": detalle or None, "capital": capital, "datos_registrales": empresa["datos_registrales"]}


def filas_borme(dia: date) -> dict[str, list[dict]]:
    s = boe.sumario(dia, "borme")
    if not s:
        return {}
    filas = []
    for it in boe.items(s):
        ident = it["identificador"]
        if ident.startswith("BORME-A") and not ident.endswith("-99"):  # el 99 es el índice alfabético del día
            for e in boe.borme_empresas(ident):
                filas.append(fila_borme(e, _fecha(it.get("fecha")) or dia.isoformat(), ident, it.get("titulo")))
    return {"borme": filas}


def fila_bdns(c: dict, coleccion: str) -> dict:
    nif, nombre = bdns.separar_beneficiario(c.get("beneficiario"))
    nif = placsp.nif_normal(nif)
    fisica = placsp.es_persona_fisica(nif)
    niveles = " ".join(x for x in (c.get("nivel1"), c.get("nivel2"), c.get("nivel3")) if x)
    return {
        "coleccion": coleccion, "id": c.get("id") or c.get("idConcesion"),
        "cod_concesion": c.get("codConcesion") or c.get("codigoConcesion"), "numero_convocatoria": c.get("numeroConvocatoria"),
        "convocatoria": c.get("convocatoria"), "convocante": c.get("convocante") or niveles or None,
        "fecha_concesion": _fecha(c.get("fechaConcesion")), "fecha_alta": _fecha(c.get("fechaAlta") or c.get("fechaRegistro")),
        "persona_fisica": fisica, "nif": None if fisica else nif, "beneficiario": None if fisica else nombre,
        "id_persona": None if fisica else c.get("idPersona"), "instrumento": (c.get("instrumento") or "").strip() or None,
        "importe": _num(c.get("importe")), "ayuda_equivalente": _num(c.get("ayudaEquivalente")),
        "reglamento": c.get("reglamento"), "objetivo": c.get("objetivo"),
        "sector": c.get("sectorActividad") or c.get("sectores"), "url_br": c.get("urlBR"),
    }


def filas_bdns(dia: date) -> dict[str, list[dict]]:
    filas = []
    for col in ("concesiones", "minimis", "ayudasestado"):
        filas += [fila_bdns(c, col) for c in bdns.altas(dia, coleccion=col)]
    return {"bdns": filas}


MINETUR = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestresHist"
_CAMPOS_EESS = {"rotulo": "Rótulo", "direccion": "Dirección", "cp": "C.P.", "localidad": "Localidad", "municipio": "Municipio",
                "id_municipio": "IDMunicipio", "provincia": "Provincia", "id_provincia": "IDProvincia", "id_ccaa": "IDCCAA",
                "margen": "Margen", "horario": "Horario", "tipo_venta": "Tipo Venta"}


def fila_carburante(e: dict, fecha: str) -> dict:
    f = {"fecha": fecha, "ideess": e.get("IDEESS"), "latitud": _num(e.get("Latitud")), "longitud": _num(e.get("Longitud (WGS84)"))}
    f.update({k: (e.get(v) or "").strip() or None for k, v in _CAMPOS_EESS.items()})
    f.update({_snake(p): _num(e.get(f"Precio {p}")) for p in PRODUCTOS})
    return f


def filas_carburantes(dia: date) -> dict[str, list[dict]]:
    r = sesion(accept="application/json").get(f"{MINETUR}/{dia:%d-%m-%Y}", timeout=300)
    datos = json_r(r)
    return {"carburantes": [fila_carburante(e, dia.isoformat()) for e in datos.get("ListaEESSPrecio", [])]}


def _utc(v: str | None) -> str | None:
    """updated llega con milisegundos y desfase (+02:00 en verano, +01:00 en invierno): se guarda en UTC sin zona."""
    if not v:
        return None
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return None


def filas_placsp(entradas: list[dict], feed: str) -> dict[str, list[dict]]:
    exp, adj = [], []
    for e in entradas:
        e = dict(e, updated=_utc(e.get("updated")))
        if e.get("deleted"):
            exp.append({"feed": feed, "id": e["id"], "updated": e.get("updated"), "borrado": True, "motivo": e.get("motivo")})
            continue
        f = {k: e.get(k) for k in ("id", "updated", "link", "expediente", "estado", "organo", "organo_dir3", "organo_nif",
                                   "organo_plataforma", "objeto", "tipo", "procedimiento", "cpv", "nuts")}
        f.update(feed=feed, borrado=False, importe_sin_iva=_num(e.get("importe_sin_iva")), importe_total=_num(e.get("importe_total")),
                 valor_estimado=_num(e.get("valor_estimado")), plazo_presentacion=_fecha(e.get("plazo_presentacion")),
                 fecha_publicacion=_fecha(e.get("fecha_publicacion")))
        exp.append(f)
        for n, a in enumerate(e.get("adjudicaciones") or []):
            fisica = placsp.es_persona_fisica(a["nif"])
            adj.append({"feed": feed, "id": e["id"], "updated": e["updated"], "n": n, "expediente": e.get("expediente"),
                        "organo_nif": e.get("organo_nif"), "organo_dir3": e.get("organo_dir3"), "lote": a["lote"],
                        "resultado": a["resultado"], "fecha_adjudicacion": _fecha(a["fecha_adjudicacion"]),
                        "ofertas": int(a["ofertas"]) if (a["ofertas"] or "").isdigit() else None,
                        "pyme": {"true": True, "false": False}.get((a["pyme"] or "").lower()), "persona_fisica": fisica,
                        "nif": None if fisica else a["nif"], "nombre": None if fisica else a["nombre"],
                        "importe_sin_iva": _num(a["importe_sin_iva"]), "importe_total": _num(a["importe_total"]),
                        "contrato": a.get("contrato"), "fecha_contrato": _fecha(a.get("fecha_contrato"))})
    return {"placsp": exp, "placsp_adjudicaciones": adj}


POR_DIA: dict[str, Callable[[date], dict[str, list[dict]]]] = {
    "boe": filas_boe, "borme": filas_borme, "bdns": filas_bdns, "carburantes": filas_carburantes}
FEEDS = {
    "643": "https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3",
    "1044": "https://contrataciondelestado.es/sindicacion/sindicacion_1044/PlataformasAgregadasSinMenores",
    "1143": "https://contrataciondelestado.es/sindicacion/sindicacion_1143/contratosMenoresPerfilesContratantes",
}
FUENTES = (*POR_DIA, "placsp")


# --- escritura en Parquet --------------------------------------------------------------------------------------------

def _duckdb():
    try:
        import duckdb
    except ImportError as exc:
        raise ImportError("el almacén necesita duckdb: pip install duckdb") from exc
    return duckdb


def existe(dir: str | os.PathLike | None = None) -> Path | None:
    """Carpeta del almacén si ya tiene algo cargado (estado.json), o None."""
    d = directorio(dir)
    return d if (d / "estado.json").exists() else None


def _lit(s: str | Path) -> str:
    return "'" + str(s).replace("'", "''") + "'"


def _mes(tabla: str, fila: dict) -> str | None:
    v = fila.get(TABLAS[tabla].orden)
    return str(v)[:7] if v else None


# 2 (2026-10-05): fecha_publicacion de PLACSP es la del anuncio de licitación (DOC_CN); en la 1 era la del primer
# anuncio, a menudo el de adjudicación. Un almacén de la 1 relee PLACSP en la siguiente sync (las filas nuevas ganan).
ESQUEMA = 2
AVISO_V1 = ("fecha_publicacion de PLACSP de una versión anterior (primer anuncio, a menudo el de adjudicación, no la "
            "licitación): sync o zip-placsp para releer")


class Almacen:
    def __init__(self, dir: str | os.PathLike | None = None):
        self.dir = directorio(dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.ruta_estado = self.dir / "estado.json"
        self.estado = json.loads(self.ruta_estado.read_text()) if self.ruta_estado.exists() else {"version": ESQUEMA}
        if self.estado.get("version", 1) < 2 and self.estado.get("placsp"):
            p = self.estado["placsp"]
            p["zips_por_releer"] = sorted(set(p.get("zips_por_releer", [])) | set(p.pop("zips", [])))
            p.pop("paginas", None)
            print(f"almacén: {AVISO_V1}; ZIP por releer: {', '.join(p['zips_por_releer']) or 'ninguno'}", file=sys.stderr)
        self.estado["version"] = max(self.estado.get("version", 1), ESQUEMA)
        self.buffer: dict[tuple[str, str], list[dict]] = {}
        self.filas_en_buffer = 0

    def guardar_estado(self):
        tmp = self.ruta_estado.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.estado, ensure_ascii=False, indent=1))
        os.replace(tmp, self.ruta_estado)

    def añadir(self, tablas: dict[str, list[dict]]):
        for tabla, filas in tablas.items():
            for f in filas:
                mes = _mes(tabla, f)
                if mes:
                    self.buffer.setdefault((tabla, mes), []).append(f)
                    self.filas_en_buffer += 1

    def volcar(self):
        """Funde lo acumulado con el Parquet de cada mes, se queda con la versión más reciente de cada clave y reemplaza
        el fichero de forma atómica."""
        if not self.buffer:
            return
        con = _duckdb().connect()
        for (tabla, mes), filas in sorted(self.buffer.items()):
            t = TABLAS[tabla]
            destino = self.dir / tabla / f"{mes}.parquet"
            destino.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile("w", suffix=".ndjson", dir=self.dir, delete=False, encoding="utf-8") as fh:
                for f in filas:
                    fh.write(json.dumps({k: f.get(k) for k in t.columnas}, ensure_ascii=False, default=str) + "\n")
                tmp_json = fh.name
            cols = "{" + ", ".join(f"{_lit(k)}: {_lit(v)}" for k, v in t.columnas.items()) + "}"
            nuevo = f"SELECT *, 1 AS _n FROM read_json({_lit(tmp_json)}, format='newline_delimited', columns={cols})"
            origen = (f"SELECT *, 0 AS _n FROM read_parquet({_lit(destino)}) UNION ALL BY NAME {nuevo}"
                      if destino.exists() else nuevo)
            salida = destino.with_suffix(".parquet.tmp")
            con.execute(f"""COPY (SELECT * EXCLUDE (_n) FROM ({origen})
                             QUALIFY row_number() OVER (PARTITION BY {", ".join(t.clave)} ORDER BY {t.orden} DESC NULLS LAST, _n DESC) = 1
                             ORDER BY {t.orden}) TO {_lit(salida)} (FORMAT parquet, COMPRESSION zstd)""")
            os.replace(salida, destino)
            os.unlink(tmp_json)
        con.close()
        self.buffer.clear()
        self.filas_en_buffer = 0

    # --- sincronización ---

    def sync_dias(self, fuente: str, desde: date, hasta: date, fin: float, log=print) -> int:
        """Carga los días pendientes de una fuente en orden; vuelca al cambiar de mes y cada 200.000 filas, y solo
        entonces marca los días como hechos, así que un corte no deja huecos."""
        hechos = set(self.estado.setdefault(fuente, {}).setdefault("dias", []))
        pendientes, n, mes = [], 0, None
        d = desde
        while d <= hasta:
            if d.isoformat() in hechos:
                d += timedelta(days=1)
                continue
            if time.monotonic() > fin:
                log(f"{fuente}: tiempo agotado antes de {d}")
                break
            if mes and d.strftime("%Y-%m") != mes or self.filas_en_buffer > 200_000:
                self._cerrar(fuente, pendientes)
                pendientes = []
            mes = d.strftime("%Y-%m")
            t0 = time.monotonic()
            filas = POR_DIA[fuente](d)
            self.añadir(filas)
            pendientes.append(d.isoformat())
            cuantas = sum(len(v) for v in filas.values())
            n += cuantas
            log(f"{fuente} {d}: {cuantas} filas ({time.monotonic() - t0:.1f} s)")
            d += timedelta(days=1)
        self._cerrar(fuente, pendientes)
        return n

    def _cerrar(self, fuente: str, dias: list[str]):
        self.volcar()
        if dias:
            e = self.estado.setdefault(fuente, {}).setdefault("dias", [])
            e.extend(x for x in dias if x not in e)
            e.sort()
            self.guardar_estado()

    def sync_placsp(self, desde: date, fin: float, feeds=FEEDS, log=print, max_paginas: int | None = None) -> int:
        """Sigue rel=next desde la página vigente de cada feed hasta una instantánea ya cargada o anterior a desde. Las
        instantáneas no cambian de contenido, así que se apuntan como vistas (solo si la cadena se recorrió sin cortes).
        max_paginas acota cada feed: las instantáneas del 643 pesan 14 a 17 MB y desde algunas redes bajan despacio."""
        s = sesion(accept="application/atom+xml, application/xml;q=0.9, */*;q=0.8")
        est = self.estado.setdefault("placsp", {}).setdefault("paginas", {})
        n = 0
        for feed in feeds:
            vistas, nuevas, url, completo = set(est.get(feed, [])), [], FEEDS[feed] + ".atom", False
            leidas = 0
            while url:
                if max_paginas and leidas >= max_paginas:
                    log(f"placsp {feed}: tope de {max_paginas} páginas")
                    break
                if url in vistas:
                    completo = True
                    break
                if time.monotonic() > fin:
                    log(f"placsp {feed}: tiempo agotado")
                    break
                entradas, siguiente = placsp.parse_feed(s.get(url, timeout=300).content)
                leidas += 1
                self.añadir(filas_placsp(entradas, feed))
                n += len(entradas)
                fechas = [e["updated"][:10] for e in entradas if e.get("updated")]
                log(f"placsp {feed} {url.rsplit('/', 1)[1]}: {len(entradas)} entradas {min(fechas, default='')}..{max(fechas, default='')}")
                if url != FEEDS[feed] + ".atom":
                    nuevas.append(url)
                if not siguiente or (fechas and max(fechas) < desde.isoformat()):
                    completo = True
                    break
                url = siguiente
            self.volcar()
            if completo:
                est[feed] = sorted(vistas | set(nuevas))
                self.guardar_estado()
        return n

    def zip_placsp(self, periodo: str, feeds=FEEDS, log=print) -> int:
        """Carga el ZIP mensual (AAAAMM, solo 2025 y 2026) o anual (AAAA) de cada feed. Sin Content-Length ni Range: se baja
        entero a un temporal; un nombre inexistente da 200 con HTML, así que se comprueba que empieza por PK."""
        s = sesion()
        hechos = self.estado.setdefault("placsp", {}).setdefault("zips", [])
        n = 0
        for feed in feeds:
            nombre = f"{feed}_{periodo}"
            if nombre in hechos:
                continue
            with tempfile.NamedTemporaryFile(suffix=".zip", dir=self.dir, delete=False) as fh:
                with s.get(f"{FEEDS[feed]}_{periodo}.zip", stream=True, timeout=600) as r:
                    for trozo in r.iter_content(1 << 20):
                        fh.write(trozo)
                ruta = fh.name
            try:
                if open(ruta, "rb").read(2) != b"PK":
                    log(f"placsp {feed} {periodo}: no hay ZIP (la respuesta no es un ZIP)")
                    continue
                with zipfile.ZipFile(ruta) as z:
                    for miembro in z.namelist():
                        entradas, _ = placsp.parse_feed(z.read(miembro))
                        self.añadir(filas_placsp(entradas, feed))
                        n += len(entradas)
                        if self.filas_en_buffer > 200_000:
                            self.volcar()
                self.volcar()
                hechos.append(nombre)
                por_releer = self.estado["placsp"].get("zips_por_releer", [])
                if nombre in por_releer:
                    por_releer.remove(nombre)
                self.guardar_estado()
                log(f"placsp {feed} {periodo}: {n} entradas")
            finally:
                os.unlink(ruta)
        return n


# --- consulta --------------------------------------------------------------------------------------------------------

def conectar(dir: str | os.PathLike | None = None, solo_lectura: bool = True):
    """DuckDB en memoria con una vista por tabla presente; en solo lectura no puede leer ni escribir fuera del almacén."""
    duckdb = _duckdb()
    d = directorio(dir)
    con = duckdb.connect()
    if solo_lectura:
        con.execute(f"SET allowed_directories=[{_lit(str(d) + os.sep)}]")
        con.execute("SET enable_external_access=false")
        con.execute("SET lock_configuration=true")
    presentes = [t for t in TABLAS if any((d / t).glob("*.parquet"))]
    for t in presentes:
        con.execute(f"CREATE VIEW {t} AS SELECT * FROM read_parquet({_lit(d / t / '*.parquet')}, union_by_name=true)")
    if "placsp" in presentes:
        # Última versión no anulada de cada expediente, con anulada y anulada_el: antes la última fila de una anulada era
        # la de baja (campos vacíos) y desaparecía de cualquier filtro en vez de contar como anulada (sexta tanda)
        con.execute("CREATE VIEW placsp_ultimo AS WITH v AS (SELECT * FROM placsp WHERE NOT coalesce(borrado, false) "
                    "QUALIFY row_number() OVER (PARTITION BY id ORDER BY updated DESC) = 1), "
                    "b AS (SELECT id, max(updated) AS baja, arg_max(motivo, updated) AS motivo_baja FROM placsp "
                    "WHERE borrado GROUP BY id) "
                    "SELECT v.*, coalesce(b.baja >= v.updated, false) AS anulada, "
                    "CASE WHEN b.baja >= v.updated THEN b.baja END AS anulada_el, "
                    "CASE WHEN b.baja >= v.updated THEN b.motivo_baja END AS motivo_baja FROM v LEFT JOIN b USING (id)")
    if "placsp_adjudicaciones" in presentes:
        # acuerdos marco: el importe del lote se repite en cada adjudicatario (agosto de 2026, feed 1044: 521 de 574 lotes
        # con varios; sumar por fila daba 33.302 M€ frente a 9.709 M€ contando cada lote una vez)
        con.execute("CREATE VIEW adjudicaciones_ultimo AS SELECT *, count(*) OVER w AS adjudicatarios, "
                    "(count(*) OVER w > 1 AND min(importe_sin_iva) OVER w = max(importe_sin_iva) OVER w) AS importe_compartido "
                    "FROM (SELECT * FROM placsp_adjudicaciones QUALIFY rank() OVER (PARTITION BY id ORDER BY updated DESC) = 1) "
                    "WINDOW w AS (PARTITION BY id, updated, lote)")
    partes = []
    if "placsp_adjudicaciones" in presentes:
        partes.append("SELECT nif, nombre, 'contrato' AS fuente, coalesce(fecha_adjudicacion, fecha_contrato) AS fecha "
                      "FROM placsp_adjudicaciones WHERE nif IS NOT NULL AND nombre IS NOT NULL AND NOT coalesce(persona_fisica, false)")
    if "bdns" in presentes:
        partes.append("SELECT nif, beneficiario AS nombre, 'ayuda' AS fuente, fecha_concesion AS fecha FROM bdns "
                      "WHERE nif IS NOT NULL AND beneficiario IS NOT NULL AND NOT coalesce(persona_fisica, false)")
    if partes:  # directorio NIF y nombre: el BORME no trae NIF y ninguna fuente abierta lo da por nombre
        con.execute("CREATE VIEW empresas AS SELECT nif, mode(nombre) AS nombre, list(DISTINCT nombre) AS nombres, "
                    "count(*) FILTER (WHERE fuente = 'contrato') AS contratos, count(*) FILTER (WHERE fuente = 'ayuda') AS ayudas, "
                    f"min(fecha) AS primera, max(fecha) AS ultima FROM ({' UNION ALL '.join(partes)}) GROUP BY nif")
    return con


def buscar_empresa(texto: str, dir: str | os.PathLike | None = None, limite: int = 10) -> list[dict]:
    """NIF por nombre (o parte, sin tildes ni forma jurídica) en la vista empresas del almacén: adjudicatarios y
    beneficiarios cargados, sin personas físicas. Exactos primero."""
    con = conectar(dir)
    if not con.execute("SELECT count(*) FROM duckdb_views() WHERE view_name = 'empresas'").fetchone()[0]:
        return []
    clave = _norm_nombre(texto)
    filas = con.execute("SELECT nif, nombre, nombres, contratos, ayudas, primera, ultima FROM empresas").fetchall()
    out = []
    for nif, nombre, nombres, contratos, ayudas, primera, ultima in filas:
        ns = {_norm_nombre(n) for n in nombres or []}
        if nif == texto.upper().strip() or any(clave in n for n in ns):
            out.append({"nif": nif, "nombre": nombre, "contratos": contratos, "ayudas": ayudas,
                        "ultima": str(ultima) if ultima else None, "_exacto": clave in ns})
    out.sort(key=lambda e: (not e.pop("_exacto"), -(e["contratos"] + e["ayudas"])))
    return out[:limite]


def cobertura(dir: str | os.PathLike | None = None) -> dict:
    """Primer y último mes de cada tabla y días cargados por fuente: lo que no está cargado no aparece en las consultas."""
    d = directorio(dir)
    est = json.loads((d / "estado.json").read_text()) if (d / "estado.json").exists() else {}
    out = {}
    for t in TABLAS:
        meses = sorted(p.stem for p in (d / t).glob("*.parquet"))
        if meses:
            out[t] = {"meses": f"{meses[0]}..{meses[-1]}", "ficheros": len(meses)}
    for f in POR_DIA:
        dias = est.get(f, {}).get("dias", [])
        if dias:
            out.setdefault(f, {})["dias_cargados"] = f"{len(dias)} ({dias[0]}..{dias[-1]})"
    if est.get("placsp"):
        out.setdefault("placsp", {})["zips"] = est["placsp"].get("zips", [])
    if "placsp" in out and (est.get("version", 1) < 2 or est.get("placsp", {}).get("zips_por_releer")):
        out["placsp"]["aviso"] = AVISO_V1
    # Las tablas que no se cargan por días (PLACSP por páginas del feed o ZIP) solo decían el mes: un almacén que empieza
    # el 30/09 decía «2026-09..2026-10» y una suma de septiembre salía con un solo día sin aviso.
    sin_dias = [t for t in out if t not in POR_DIA and TABLAS[t].orden and "dias_cargados" not in out[t]]
    if sin_dias:
        try:
            con = _duckdb().connect()
            for t in sin_dias:
                o = TABLAS[t].orden
                mn, mx = con.execute(f"SELECT min({o}), max({o}) FROM read_parquet({_lit(d / t / '*.parquet')}, "
                                     "union_by_name=true)").fetchone()
                if mn:
                    out[t]["desde"], out[t]["hasta"] = str(mn)[:19], str(mx)[:19]
        except Exception:  # noqa: BLE001 - sin duckdb, solo los meses
            pass
    return out


PISTA_VERSIONES = ("placsp y placsp_adjudicaciones tienen una fila por versión (cada cambio de estado) y las bajas como filas "
                   "borrado: para contar o sumar expedientes, placsp_ultimo (una por id, con anulada y anulada_el) y adjudicaciones_ultimo")
PISTA_FEED = ("las tablas de PLACSP juntan las tres sindicaciones: feed '643' son los perfiles alojados, '1044' las plataformas "
              "autonómicas agregadas y '1143' los contratos menores; filtrar por feed")


def sql(consulta: str, dir: str | os.PathLike | None = None, limite: int = 200) -> dict:
    """Ejecuta una consulta de solo lectura y devuelve columnas y filas (fechas como texto)."""
    con = conectar(dir)
    cur = con.execute(consulta)
    cols = [c[0] for c in cur.description] if cur.description else []
    filas = cur.fetchmany(limite + 1)
    out = {"columnas": cols, "filas": [[v if isinstance(v, (int, float, str, bool, list)) or v is None else str(v) for v in f]
                                       for f in filas[:limite]], "truncado": len(filas) > limite}
    pistas = []
    if out["truncado"]:  # sexta tanda: un agente contó constituciones sobre 500 de 626 filas sin mirar truncado
        out["filas_totales"] = con.execute(f"SELECT count(*) FROM ({consulta.strip().rstrip(';')})").fetchone()[0]
        pistas.append("faltan filas: contar o sumar en el propio SQL (count, sum, group by) en vez de traerlas")
    if re.search(r"\bplacsp(_adjudicaciones)?\b", consulta, re.I):  # sexta tanda: sumaban versiones y anuladas
        pistas.append(PISTA_VERSIONES)
    if re.search(r"\b(placsp|placsp_adjudicaciones|placsp_ultimo|adjudicaciones_ultimo)\b", consulta, re.I) \
            and not re.search(r"\bfeed\b", consulta, re.I):  # séptima tanda: 163 obras del 01/10 por 126 al sumar los tres feeds
        pistas.append(PISTA_FEED)
    if pistas:
        out["pista"] = "; ".join(pistas)
    return out


def _norm_nombre(s: str | None) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper()
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    s = re.sub(r"\s+EN LIQUIDACION$", "", s.strip())  # el BORME añade «EN LIQUIDACION» a la denominación
    s = re.sub(r"\b(S ?L ?U?|S ?A ?U?|SOCIEDAD (LIMITADA|ANONIMA)( UNIPERSONAL)?|SLNE|S ?COOP|SCOOP|SLL|SAL|SLP)\s*$", "", s.strip())
    return re.sub(r"\s+", " ", s).strip()


def empresa(nif: str, dir: str | os.PathLike | None = None, nombre: str | None = None, max_filas: int = 10) -> dict:
    """Lo que el almacén local sabe de un NIF: contratos adjudicados (último estado de cada expediente), contratos como
    órgano de contratación, subvenciones y actos del BORME por denominación. Solo cubre lo cargado (ver cobertura)."""
    nif = placsp.nif_normal(nif)
    con = conectar(dir)
    vistas = {r[0] for r in con.execute("SELECT table_name FROM information_schema.tables").fetchall()}
    out: dict = {"nif": nif, "cobertura": cobertura(dir)}

    def filas(q, *p):
        cur = con.execute(q, list(p))
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, [v if isinstance(v, (int, float, str, bool, list)) or v is None else str(v) for v in f]))
                for f in cur.fetchall()]

    if "adjudicaciones_ultimo" in vistas:
        out["contratos"] = filas("""SELECT count(*) AS n,
                                    round(sum(importe_sin_iva) FILTER (WHERE NOT coalesce(importe_compartido, false)), 2) AS importe_sin_iva,
                                    count(*) FILTER (WHERE importe_compartido) AS lotes_compartidos,
                                    round(sum(importe_sin_iva) FILTER (WHERE importe_compartido), 2) AS importe_compartido_sin_iva,
                                    min(fecha_adjudicacion) AS primera, max(fecha_adjudicacion) AS ultima
                                    FROM adjudicaciones_ultimo WHERE nif = ?""", nif)[0]
        out["contratos"]["nota"] = ("importe_compartido_sin_iva: lotes de acuerdos marco cuyo importe se repite en cada "
                                    "adjudicatario; es un techo compartido, no lo adjudicado a esta empresa")
        out["contratos"]["recientes"] = filas(f"""SELECT a.fecha_adjudicacion, a.importe_sin_iva, a.adjudicatarios, a.lote, p.expediente,
                                    p.objeto, p.organo, p.estado, p.link FROM adjudicaciones_ultimo a
                                    JOIN placsp_ultimo p USING (id, updated) WHERE a.nif = ?
                                    ORDER BY a.fecha_adjudicacion DESC NULLS LAST LIMIT {int(max_filas)}""", nif)
        nombre = nombre or next((r["nombre"] for r in filas("SELECT nombre FROM adjudicaciones_ultimo WHERE nif = ? AND nombre IS NOT NULL LIMIT 1", nif)), None)
    if "placsp_ultimo" in vistas:
        out["como_organo"] = filas("""SELECT count(*) AS expedientes, round(sum(importe_sin_iva), 2) AS importe_sin_iva
                                      FROM placsp_ultimo WHERE organo_nif = ? AND NOT anulada""", nif)[0]
    if "bdns" in vistas:
        out["subvenciones"] = filas("""SELECT coleccion, count(*) AS n, round(sum(importe), 2) AS importe,
                                       round(sum(ayuda_equivalente), 2) AS ayuda_equivalente, max(fecha_concesion) AS ultima
                                       FROM bdns WHERE nif = ? GROUP BY coleccion ORDER BY coleccion""", nif)
        nombre = nombre or next((r["beneficiario"] for r in filas("SELECT beneficiario FROM bdns WHERE nif = ? AND beneficiario IS NOT NULL LIMIT 1", nif)), None)
    if "borme" in vistas and nombre:
        clave = _norm_nombre(nombre)
        palabra = max(clave.split(), key=len) if clave else ""
        candidatos = filas("""SELECT fecha, provincia, denominacion, actos, detalle, capital, datos_registrales FROM borme
                              WHERE strip_accents(upper(denominacion)) LIKE ? ORDER BY fecha DESC""", f"%{palabra}%") if palabra else []
        propios = [c for c in candidatos if _norm_nombre(c["denominacion"]) == clave]
        out["borme"] = {"denominacion_buscada": nombre, "actos": propios[:max_filas],
                        "concursos": [c for c in propios if "Situación concursal" in (c["actos"] or [])][:max_filas]}
    return out


# --- línea de órdenes ------------------------------------------------------------------------------------------------

def _dia(s: str | None, defecto: date) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date() if s else defecto


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=None, help="carpeta del almacén (por defecto ./almacen o FUENTES_ALMACEN)")
    sub = ap.add_subparsers(dest="orden", required=True)
    s = sub.add_parser("sync", help="carga lo pendiente hasta ayer")
    s.add_argument("--fuentes", default="boe,borme,bdns,placsp")
    s.add_argument("--desde", help="AAAA-MM-DD; por defecto, ayer")
    s.add_argument("--hasta", help="AAAA-MM-DD; por defecto, ayer")
    s.add_argument("--minutos", type=float, default=0, help="tope de tiempo; 0 sin tope")
    s.add_argument("--paginas", type=int, default=0, help="tope de páginas por feed de PLACSP; 0 sin tope")
    s.add_argument("--feeds", default="643,1044,1143", help="feeds de PLACSP; solo 643 (perfiles alojados) pesa un tercio")
    z = sub.add_parser("zip-placsp", help="carga ZIP mensuales o anuales de PLACSP")
    z.add_argument("periodo", nargs="+", help="AAAAMM (2025 y 2026) o AAAA")
    z.add_argument("--feeds", default="643,1044,1143")
    q = sub.add_parser("sql", help="consulta de solo lectura")
    q.add_argument("consulta")
    q.add_argument("--limite", type=int, default=50)
    e = sub.add_parser("empresa", help="contratos, subvenciones y BORME de un NIF")
    e.add_argument("nif")
    sub.add_parser("estado", help="qué hay cargado")
    a = ap.parse_args(argv)
    try:
        _duckdb()
    except ImportError as exc:
        sys.exit(str(exc))

    if a.orden == "sync":
        ayer = date.today() - timedelta(days=1)
        desde, hasta = _dia(a.desde, ayer), min(_dia(a.hasta, ayer), ayer)
        fin = time.monotonic() + a.minutos * 60 if a.minutos else float("inf")
        alm = Almacen(a.dir)
        for f in [x.strip() for x in a.fuentes.split(",") if x.strip()]:
            if f == "placsp":
                n = alm.sync_placsp(desde, fin, {k: FEEDS[k] for k in a.feeds.split(",")}, max_paginas=a.paginas or None)
            elif f in POR_DIA:
                n = alm.sync_dias(f, desde, hasta, fin)
            else:
                sys.exit(f"fuente desconocida {f}; válidas: {', '.join(FUENTES)}")
            print(f"{f}: {n} filas nuevas")
        print(json.dumps(cobertura(a.dir), ensure_ascii=False, indent=1))
    elif a.orden == "zip-placsp":
        alm = Almacen(a.dir)
        for p in a.periodo:
            alm.zip_placsp(p, {k: FEEDS[k] for k in a.feeds.split(",")})
    elif a.orden == "sql":
        r = sql(a.consulta, a.dir, a.limite)
        print("\t".join(r["columnas"]))
        for f in r["filas"]:
            print("\t".join("" if v is None else str(v) for v in f))
        if r.get("pista"):
            print("pista:", r["pista"], file=sys.stderr)
    elif a.orden == "empresa":
        print(json.dumps(empresa(a.nif, a.dir), ensure_ascii=False, indent=1, default=str))
    elif a.orden == "estado":
        print(json.dumps(cobertura(a.dir), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
