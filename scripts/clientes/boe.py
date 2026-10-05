"""BOE y BORME: Accept obligatorio, árbol del sumario variable, errores en XML y 404 sin boletín (fichas boe-api-sumario,
boe-api-legislacion-consolidada y borme-api-sumario).

Uso: python scripts/clientes/boe.py [AAAAMMDD]
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from typing import Iterator

try:
    from ._http import session
except ImportError:  # ejecutado por ruta
    sys.path.insert(0, os.path.dirname(__file__))
    from _http import session

API = "https://www.boe.es/datosabiertos/api"
LC = f"{API}/legislacion-consolidada"
_NIVELES = {"diario": ("numero",), "seccion": ("codigo", "nombre"), "departamento": ("codigo", "nombre"), "epigrafe": ("nombre",), "apartado": ("nombre",)}
# Tipos de acto vistos en 109 XML de provincia de la sección A (julio a septiembre de 2026); uno que falte queda dentro del anterior
ACTOS_BORME = (
    "Constitución", "Nombramientos", "Ceses/Dimisiones", "Revocaciones", "Reelecciones", "Otros conceptos",
    "Declaración de unipersonalidad", "Sociedad unipersonal", "Pérdida del carácter de unipersonalidad",
    "Cambio de identidad del socio único", "Cambio de domicilio social", "Cambio de objeto social", "Ampliación del objeto social",
    "Cambio de denominación social", "Modificaciones estatutarias", "Ampliación de capital", "Reducción de capital",
    "Disolución", "Extinción", "Transformación de sociedad", "Fusión por absorción", "Escisión parcial", "Situación concursal",
    "Cancelaciones de oficio de nombramientos", "Reapertura hoja registral", "Cierre provisional hoja registral",
    "Página web de la sociedad", "Fe de erratas", "Escisión total", "Desembolso de dividendos pasivos", "Modificación de poderes",
    "Empresario Individual", "Adaptación Ley 2/95", "Articulo 378.5 del Reglamento del Registro Mercantil",
)
# Un acto empieza tras «. » o tras «.- » (así encadena el BORME las resoluciones concursales: sin el guion opcional, el
# segundo «Situación concursal» de una empresa quedaba dentro del texto del primero; BORME-A-2026-189-28, 2026-10-05)
_ACTO_RE = re.compile(r"(?:^|(?<=\.)-?\s+)(" + "|".join(re.escape(a) for a in ACTOS_BORME) + r")(?=[.:\s])")


def _aaaammdd(fecha) -> str:
    return fecha.strftime("%Y%m%d") if isinstance(fecha, date) else str(fecha).replace("-", "")


def _get(url: str, accept: str = "application/json", params=None, intentos: int = 2):
    """GET con Accept explícito (sin él, 400); reintenta una vez los 500 que dan algunos días antiguos."""
    s = session(accept=accept)
    for n in range(intentos):
        r = s.get(url, params=params, timeout=90, verify=s.verify)
        if r.status_code < 500 or n + 1 == intentos:
            return r
        time.sleep(3)


def error_api(cuerpo: str | bytes) -> str:
    """Los errores de la API llegan siempre en XML (response/status/code y text), aunque se pida JSON."""
    try:
        root = ET.fromstring(cuerpo)
        return f"{root.findtext('status/code')} {root.findtext('status/text')}"
    except ET.ParseError:
        return str(cuerpo)[:120]


def sumario(fecha, diario: str = "boe") -> dict | None:
    """data.sumario del día (diario boe o borme); None si no hay boletín (404: el BOE no sale los domingos, el BORME
    tampoco sábados ni festivos). Lanza RuntimeError con otros códigos, como el 500 de algunos días antiguos."""
    r = _get(f"{API}/{diario}/sumario/{_aaaammdd(fecha)}")
    if r.status_code == 404:
        return None
    if r.status_code != 200:
        raise RuntimeError(f"{diario.upper()} {_aaaammdd(fecha)}: {error_api(r.content)}")
    return r.json()["data"]["sumario"]


def items(sumario: dict) -> Iterator[dict]:
    """Aplana el sumario: un dict por disposición o anuncio con diario, sección, departamento y epígrafe.

    No supone niveles fijos: un día puede traer dos diarios (ordinario y extraordinario), cualquier nivel es objeto
    si tiene un elemento y lista si tiene varios, y hay nodos texto intermedios (departamento.texto en las secciones
    4 y 5C, seccion.texto en extraordinarios). En el BORME la sección C cuelga de apartado.
    """
    fecha = sumario.get("metadatos", {}).get("fecha_publicacion")

    def walk(nodo, ctx):
        for clave, valor in nodo.items():
            hijos = valor if isinstance(valor, list) else [valor]
            if clave == "item":
                for it in hijos:
                    pdf = it.get("url_pdf") or {}
                    yield dict(ctx, fecha=fecha, identificador=it["identificador"], titulo=it.get("titulo"), control=it.get("control"),
                               url_pdf=pdf.get("texto"), pdf_bytes=int(pdf["szBytes"]) if pdf.get("szBytes") else None,
                               url_html=it.get("url_html"), url_xml=it.get("url_xml"))
            elif clave in _NIVELES:
                for h in hijos:
                    yield from walk(h, dict(ctx, **{f"{clave}_{c}": h.get(c) for c in _NIVELES[clave]}))
            elif clave == "texto" and isinstance(valor, (dict, list)):
                for h in hijos:
                    yield from walk(h, ctx)

    yield from walk(sumario, {})


def sumarios(desde, hasta, diario: str = "boe") -> Iterator[tuple[date, dict]]:
    """Recorre días; salta los que no tienen boletín y avisa por stderr de los que fallan (500 en fechas antiguas)."""
    d = desde if isinstance(desde, date) else datetime.strptime(_aaaammdd(desde), "%Y%m%d").date()
    fin = hasta if isinstance(hasta, date) else datetime.strptime(_aaaammdd(hasta), "%Y%m%d").date()
    while d <= fin:
        try:
            s = sumario(d, diario)
            if s:
                yield d, s
        except RuntimeError as exc:
            print(f"aviso: {exc}", file=sys.stderr)
        d += timedelta(days=1)


def parse_documento(root: ET.Element) -> dict:
    """XML de xml.php: metadatos planos (los atributos codigo como <campo>_codigo), materias, referencias y texto plano."""
    meta = {}
    for el in root.find("metadatos"):
        valor = el[0].text if len(el) else el.text  # url_epub anida un url_epub
        meta[el.tag] = (valor or "").strip() or None
        if el.get("codigo") is not None:
            meta[f"{el.tag}_codigo"] = el.get("codigo")
    def refs(tipo: str) -> list[dict]:
        return [{"id": r.get("referencia"), "relacion": r.findtext("palabra"), "relacion_codigo": r.find("palabra").get("codigo") if r.find("palabra") is not None else None,
                 "texto": r.findtext("texto")} for r in root.iterfind(f"analisis/referencias/{tipo}es/{tipo}")]

    texto = root.find("texto")
    return {
        **meta,
        "materias": [m.text for m in root.iterfind("analisis/materias/materia")],
        "anteriores": refs("anterior"),
        "posteriores": refs("posterior"),
        "texto": "\n".join(t.strip() for t in texto.itertext() if t.strip()) if texto is not None else "",
    }


def documento(identificador: str) -> dict:
    """Disposición o anuncio por id (BOE-A, BOE-B, BORME-A, BORME-C). Un id inexistente da 200 con <error>: KeyError."""
    url = "https://www.boe.es/diario_borme/xml.php" if identificador.startswith("BORME") else "https://www.boe.es/diario_boe/xml.php"
    r = _get(url, accept="application/xml", params={"id": identificador})
    root = ET.fromstring(r.content)
    if root.tag == "error":
        raise KeyError(f"{identificador}: {root.findtext('descripcion')}")
    return parse_documento(root)


def normas(desde=None, hasta=None, query: dict | None = None, lote: int = 1000) -> Iterator[dict]:
    """Legislación consolidada: por fecha de última actualización (desde/hasta) o por query (query_string con campo,
    p. ej. titulo:vivienda; range con gte y lte en AAAAMMDD). Pagina con offset; sin resultados data es "", no []."""
    offset = 0
    while True:
        params = {"offset": offset, "limit": lote}
        if desde:
            params["from"] = _aaaammdd(desde)
        if hasta:
            params["to"] = _aaaammdd(hasta)
        if query:
            params["query"] = json.dumps(query, ensure_ascii=False)
        r = _get(LC, params=params)
        if r.status_code != 200:
            raise RuntimeError(f"legislación consolidada: {error_api(r.content)}")
        data = r.json()["data"] or []
        yield from data
        if len(data) < lote:
            return
        offset += lote


def metadatos(identificador: str) -> dict | None:
    """Vigencia, estado de consolidación y url_eli; None si la disposición no tiene texto consolidado (404)."""
    r = _get(f"{LC}/id/{identificador}/metadatos")
    if r.status_code == 404:
        return None
    if r.status_code != 200:
        raise RuntimeError(f"{identificador}: {error_api(r.content)}")
    return r.json()["data"][0]


def indice(identificador: str) -> list[dict]:
    """Bloques del consolidado (id, titulo, fecha_actualizacion, url); el id se pasa a bloque()."""
    r = _get(f"{LC}/id/{identificador}/texto/indice")
    if r.status_code != 200:
        raise RuntimeError(f"{identificador}: {error_api(r.content)}")
    data = r.json()["data"]
    b = (data[0] if isinstance(data, list) else data)["bloque"]
    return b if isinstance(b, list) else [b]


def parse_bloque(root: ET.Element) -> list[dict]:
    """Versiones de un bloque (solo XML): id_norma que la introdujo, fechas AAAAMMDD y texto plano."""
    return [dict(v.attrib, texto="\n".join(t.strip() for t in v.itertext() if t.strip())) for v in root.iterfind("data/bloque/version")]


def version_vigente(versiones: list[dict], fecha=None) -> dict | None:
    """La versión con fecha_vigencia más reciente que no sea posterior a fecha (hoy por defecto)."""
    tope = _aaaammdd(fecha or date.today())
    validas = [v for v in versiones if (v.get("fecha_vigencia") or v.get("fecha_publicacion") or "") <= tope]
    return max(validas, key=lambda v: v.get("fecha_vigencia") or v.get("fecha_publicacion") or "", default=None)


def bloque(identificador: str, id_bloque: str) -> list[dict]:
    """Un bloque (preambulo, a1, da1...) con todas sus versiones; con Accept application/json responde 400."""
    r = _get(f"{LC}/id/{identificador}/texto/bloque/{id_bloque}", accept="application/xml")
    if r.status_code != 200:
        raise RuntimeError(f"{identificador}/{id_bloque}: {error_api(r.content)}")
    return parse_bloque(ET.fromstring(r.content))


def parse_borme_a(root: ET.Element) -> list[dict]:
    """Sección A del BORME: cada empresa es un p.articulo (número - denominación) y un p.parrafo con los actos y los
    datos registrales al final. Devuelve número, denominación, registro (si viene entre paréntesis), actos y datos."""
    out, actual = [], None
    for p in root.find("texto"):
        txt = "".join(p.itertext()).strip()
        if p.get("class") == "articulo":
            num, _, nombre = txt.partition(" - ")
            m = re.match(r"(.*?)\s*\(R\.M\. ([^)]*)\)\.?$", nombre)
            nombre, registro = (m.group(1), m.group(2)) if m else (nombre, None)
            if nombre.endswith(".") and not re.search(r"\b[A-Z]\.[A-Z]\.$", nombre):  # el punto final es del BORME, salvo en S.L. o S.A.
                nombre = nombre[:-1]
            actual = {"numero": int(num) if num.isdigit() else num, "denominacion": nombre.strip(), "registro": registro, "actos": [], "datos_registrales": None}
            out.append(actual)
        elif p.get("class") == "parrafo" and actual is not None:
            cuerpo, _, datos = txt.partition("Datos registrales.")
            actual["datos_registrales"] = datos.strip().rstrip(".") or None
            cortes = list(_ACTO_RE.finditer(cuerpo))
            previo = cuerpo[: cortes[0].start() if cortes else len(cuerpo)].strip(" .")
            if previo:  # acto que no está en ACTOS_BORME: se conserva con tipo None
                actual["actos"].append({"tipo": None, "texto": previo})
            for i, m in enumerate(cortes):
                fin = cortes[i + 1].start() if i + 1 < len(cortes) else len(cuerpo)
                actual["actos"].append({"tipo": m.group(1), "texto": cuerpo[m.end():fin].strip(" .:")})
    return out


def parse_concursal(texto: str | None) -> dict | None:
    """Acto «Situación concursal» del BORME a campos, sin los nombres que trae (juez, administradores concursales e
    inhabilitados son datos personales): procedimiento, firme, fecha de la resolución (AAAA-MM-DD), resolución (Auto de
    declaración de concurso, de apertura de la fase de liquidación, de conclusión, sentencia de calificación...), clase
    (Voluntario o Necesario), calificación (Culpable o Fortuito) y juzgado."""
    if not texto:
        return None
    m = re.search(r"Fecha de resolución (\d{1,2})/(\d{1,2})/(\d{4})\.\s*([^.]+)\.", texto)
    proc = re.search(r"Procedimiento concursal ([^.\s]+)", texto)
    juz = re.search(r"Juzgado:\s*(?:num\. \d+ )?(.*?)\.\s*(?:Juez|Resoluciones|Administrador|$)", texto)
    clase = re.search(r"\b(Voluntario|Necesario)\b", texto)
    calif = re.search(r"\b(Culpable|Fortuito)\b", texto)
    firme = re.search(r"FIRME: (SI|SÍ|No)", texto, re.I)
    return {"procedimiento": proc.group(1) if proc else None,
            "fecha_resolucion": f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else None,
            "resolucion": m.group(4).strip() if m else None, "clase": clase.group(1) if clase else None,
            "calificacion": calif.group(1) if calif else None,
            "firme": None if not firme else firme.group(1).upper() in ("SI", "SÍ"),
            "juzgado": juz.group(1).strip() if juz else None}


def borme_empresas(identificador: str) -> list[dict]:
    """Empresas y actos de un BORME-A-AAAA-NNN-PP (PP provincia). El sufijo 99 es el índice alfabético del día, no una provincia."""
    r = _get("https://www.boe.es/diario_borme/xml.php", accept="application/xml", params={"id": identificador})
    root = ET.fromstring(r.content)
    if root.tag == "error":
        raise KeyError(f"{identificador}: {root.findtext('descripcion')}")
    return parse_borme_a(root)


if __name__ == "__main__":
    dia = sys.argv[1] if len(sys.argv) > 1 else date.today().strftime("%Y%m%d")
    s = sumario(dia)
    if s is None:
        sys.exit(f"{dia}: sin BOE (domingo)")
    todos = list(items(s))
    print(dia, len(todos), "items;", sum(1 for i in todos if i["seccion_codigo"] == "1"), "en la sección I")
    for i in todos[:3]:
        print(" ", i["identificador"], i["seccion_codigo"], (i.get("departamento_nombre") or "")[:40], "|", i["titulo"][:80])
    m = metadatos("BOE-A-1978-31229")
    art = version_vigente(bloque("BOE-A-1978-31229", "a135"))
    print("Constitución:", m["estado_consolidacion"]["texto"], m["url_eli"], "| art. 135 vigente desde", art["fecha_vigencia"], "por", art["id_norma"])
    b = sumario(dia, "borme")
    if b:
        madrid = next((i["identificador"] for i in items(b) if i["identificador"].startswith("BORME-A") and i["identificador"].endswith("-28")), None)
        if madrid:
            emp = borme_empresas(madrid)
            print("BORME Madrid:", len(emp), "empresas;", sum(1 for e in emp for a in e["actos"] if a["tipo"] == "Constitución"), "constituciones")
