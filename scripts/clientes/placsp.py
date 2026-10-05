"""PLACSP: feed Atom con CODICE, paginación y campos útiles por entrada (ficha placsp-datos-abiertos).

Uso: python scripts/clientes/placsp.py [paginas]
"""
from __future__ import annotations

import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Iterator

try:
    from ._http import session
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from _http import session

FEED = "https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3.atom"
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "cbc": "urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2",
    "ext": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2",
    "extb": "urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2",
    "at": "http://purl.org/atompub/tombstones/1.0",
}


def _t(el, path: str):
    n = el.find(path, NS)
    return n.text.strip() if n is not None and n.text else None


def _ids(party) -> dict:
    """IDs de una parte por schemeName (DIR3, NIF, ID_PLATAFORMA, ID_OC_PLAT, OTROS)."""
    if party is None:
        return {}
    return {i.get("schemeName"): i.text.strip() for i in party.findall("cac:PartyIdentification/cbc:ID", NS) if i.text}


def nif_normal(nif: str | None) -> str | None:
    """El NIF del adjudicatario llega a veces con guion, puntos, espacios o en minúscula: B-12345678 -> B12345678."""
    return re.sub(r"[\s.\-]", "", nif).upper() or None if nif else None


def es_persona_fisica(nif: str | None) -> bool:
    """DNI o NIE (12345678Z, X1234567L) o NIF enmascarado (***1234**)."""
    return bool(nif) and ("*" in nif or bool(re.fullmatch(r"\d{8}[A-Z]|[XYZ]\d{7}[A-Z]", nif)))


def adjudicaciones(cfs) -> list[dict]:
    """Una fila por TenderResult (uno por lote) y adjudicatario: lote, resultado, fecha, ofertas, pyme, NIF, nombre,
    importes (sin IVA TaxExclusiveAmount, con IVA PayableAmount) y contrato formalizado (id y fecha). Una UTE puede traer
    varios WinningParty en el mismo resultado; la adjudicación del primer lote no es la del contrato entero."""
    out = []
    for tr in cfs.findall("cac:TenderResult", NS):
        base = {
            "lote": _t(tr, "cac:AwardedTenderedProject/cbc:ProcurementProjectLotID"),
            "resultado": _t(tr, "cbc:ResultCode"),
            "fecha_adjudicacion": _t(tr, "cbc:AwardDate"),
            "ofertas": _t(tr, "cbc:ReceivedTenderQuantity"),
            "pyme": _t(tr, "cbc:SMEAwardedIndicator"),
            "importe_sin_iva": _t(tr, "cac:AwardedTenderedProject/cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount"),
            "importe_total": _t(tr, "cac:AwardedTenderedProject/cac:LegalMonetaryTotal/cbc:PayableAmount"),
            "contrato": _t(tr, "cac:Contract/cbc:ID"),  # contrato formalizado, distinto del expediente
            "fecha_contrato": _t(tr, "cac:Contract/cbc:IssueDate"),
        }
        ganadores = tr.findall("cac:WinningParty", NS) or [None]
        for wp in ganadores:
            ident = wp.find("cac:PartyIdentification/cbc:ID", NS) if wp is not None else None
            out.append(dict(base, nif=nif_normal(ident.text) if ident is not None and ident.text else None,
                            nif_esquema=ident.get("schemeName") if ident is not None else None,
                            nombre=_t(wp, "cac:PartyName/cbc:Name") if wp is not None else None))
    return out


def parse_entry(entry) -> dict:
    """Campos clave del CODICE de una entrada: expediente, estado, órgano (DIR3 y NIF), objeto, importes, valor estimado,
    procedimiento, CPV, NUTS, plazo, adjudicaciones por lote y modificaciones (prórrogas, modificados)."""
    cfs = entry.find("ext:ContractFolderStatus", NS)
    if cfs is None:
        return {"id": _t(entry, "a:id"), "title": _t(entry, "a:title"), "updated": _t(entry, "a:updated"), "deleted": True}
    party = cfs.find("ext:LocatedContractingParty/cac:Party", NS)
    ids = _ids(party)
    return {
        "id": _t(entry, "a:id"),
        "updated": _t(entry, "a:updated"),
        "link": entry.find("a:link", NS).get("href") if entry.find("a:link", NS) is not None else None,
        "expediente": _t(cfs, "cbc:ContractFolderID"),
        "estado": _t(cfs, "extb:ContractFolderStatusCode"),
        "organo": _t(party, "cac:PartyName/cbc:Name") if party is not None else None,
        "organo_dir3": ids.get("DIR3"),  # falta en el 29 % del 643: None, no el NIF ni el ID de plataforma (issue 10)
        "organo_nif": nif_normal(ids.get("NIF")),
        "organo_plataforma": ids.get("ID_PLATAFORMA") or ids.get("ID_OC_PLAT"),
        "objeto": _t(cfs, "cac:ProcurementProject/cbc:Name"),
        "tipo": _t(cfs, "cac:ProcurementProject/cbc:TypeCode"),
        "procedimiento": _t(cfs, "cac:TenderingProcess/cbc:ProcedureCode"),
        "importe_sin_iva": _t(cfs, "cac:ProcurementProject/cac:BudgetAmount/cbc:TaxExclusiveAmount"),
        "importe_total": _t(cfs, "cac:ProcurementProject/cac:BudgetAmount/cbc:TotalAmount"),
        "valor_estimado": _t(cfs, "cac:ProcurementProject/cac:BudgetAmount/cbc:EstimatedOverallContractAmount"),
        "cpv": [c.text for c in cfs.findall("cac:ProcurementProject/cac:RequiredCommodityClassification/cbc:ItemClassificationCode", NS)],
        "nuts": _t(cfs, "cac:ProcurementProject/cac:RealizedLocation/cbc:CountrySubentityCode"),
        "plazo_presentacion": _t(cfs, "cac:TenderingProcess/cac:TenderSubmissionDeadlinePeriod/cbc:EndDate"),
        "fecha_publicacion": _t(cfs, "ext:ValidNoticeInfo/ext:AdditionalPublicationStatus/ext:AdditionalPublicationDocumentReference/cbc:IssueDate"),
        "adjudicaciones": adjudicaciones(cfs),
        "modificaciones": [{"n": _t(m, "cbc:ID"), "contrato": _t(m, "cbc:ContractID"), "nota": _t(m, "cbc:Note"),
                            "importe_sin_iva": _t(m, "cac:ContractModificationLegalMonetaryTotal/cbc:TaxExclusiveAmount"),
                            "importe_final_sin_iva": _t(m, "cac:FinalLegalMonetaryTotal/cbc:TaxExclusiveAmount")}
                           for m in cfs.findall("cac:ContractModification", NS)],  # prórrogas y modificados
    }


def parse_feed(contenido: bytes) -> tuple[list[dict], str | None]:
    """Entradas de una página, de la más reciente a la más antigua, y URL de la página anterior (link rel=next).

    Las anulaciones no son entry: llegan como at:deleted-entry (ref = id de la entrada, when, comment type ANULADA).
    Una página de bloqueo del WAF (200 con HTML) se parsea como XML sin entradas: si la raíz no es un feed, ValueError."""
    root = ET.fromstring(contenido)
    if root.tag != "{%s}feed" % NS["a"]:
        raise ValueError(f"PLACSP no devolvió un feed Atom: {contenido[:120]!r}")
    out = [parse_entry(e) for e in root.findall("a:entry", NS)]
    for d in root.findall("at:deleted-entry", NS):
        c = d.find("at:comment", NS)
        out.append({"id": d.get("ref"), "updated": d.get("when"), "deleted": True, "motivo": c.get("type") if c is not None else None})
    out.sort(key=lambda e: datetime.fromisoformat(e["updated"]) if e.get("updated") else datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    nxt = [l.get("href") for l in root.findall("a:link", NS) if l.get("rel") == "next"]
    return out, nxt[0] if nxt else None


def entradas(url: str = FEED, max_paginas: int = 1) -> Iterator[dict]:
    """Recorre el feed y sus páginas anteriores; la vigente trae lo del día y las anteriores pesan 14 a 16 MB."""
    s = session(accept="application/atom+xml, application/xml;q=0.9, */*;q=0.8")
    for _ in range(max_paginas):
        pagina, url = parse_feed(s.get(url, timeout=180, verify=s.verify).content)
        yield from pagina
        if not url:
            return


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    vistos: dict[str, dict] = {}
    for e in entradas(max_paginas=n):
        vistos.setdefault(e["id"], e)  # una entrada por cambio de estado, de la más reciente a la más antigua: vale la primera
    vivos = [e for e in vistos.values() if not e.get("deleted")]
    obras = [e for e in vivos if any(c.startswith("45") for c in e["cpv"]) and e["importe_sin_iva"] and float(e["importe_sin_iva"]) > 1_000_000]
    print(len(vivos), "expedientes,", len(vistos) - len(vivos), "anulados;", len(obras), "obras de más de un millón sin IVA")
    for e in obras[:10]:
        print(e["fecha_publicacion"], e["estado"], e["expediente"], e["organo"], e["importe_sin_iva"])
