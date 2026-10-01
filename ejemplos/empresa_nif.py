#!/usr/bin/env python3
"""Perfil público de una empresa o entidad por NIF: si es sector público, ayudas (BDNS y AEI) y prohibiciones de
contratar vigentes (fichas bdns-api, aei-convocatorias, igae-ejecucion-presupuestaria y hacienda-registro-licitadores).

Uso: python ejemplos/empresa_nif.py A02066116

Trampas que resuelve: el NIF se filtra con nifCif en cada colección de la BDNS; la AEI exporta todas sus ayudas por
CIF en un CSV con ; y coma decimal; el XML de prohibiciones oculta el NIF y se cruza por denominación sin forma
jurídica; Invente responde 204 sin cuerpo si el NIF no es sector público. Lo que no tiene consulta por NIF (contratos,
BORME, concursos, deudores) sale en la última línea con dónde mirarlo.
"""
import importlib
import sys

import _ruta

consulta = importlib.import_module(f"{_ruta.PAQUETE}.consulta")


def eur(v: float) -> str:
    return f"{v:,.0f}".replace(",", ".") + " €"


def main(nif: str) -> None:
    e = consulta.empresa_nif(nif, 3)
    sp = e["sector_publico"]
    print(f"{e['nif']} {e['nombre'] or '(sin nombre en las fuentes)'}" + (f" · sector público: {sp['FormaJuridica_Descripcion']}, DIR3 {sp['codigoDir3'] or '-'}" if sp else ""))
    s = e["subvenciones"]
    print(f"  BDNS: {s['concesiones']['total']} concesiones" + (f" ({eur(s['concesiones']['importe_total'])})" if "importe_total" in s["concesiones"] else "")
          + f", {s['ayudasestado']['total']} ayudas de Estado, {s['minimis']['total']} minimis")
    for f in s["concesiones"]["filas"][:3]:
        print(f"    {f['fechaConcesion']} {eur(f.get('importe') or 0):>14}  {(f.get('convocatoria') or '')[:80]}")
    print(f"  AEI: {e['aei']['total']} ayudas, {eur(e['aei']['importe_total'])}")
    print(f"  Prohibiciones de contratar vigentes: {len(e['prohibiciones_contratar'])}"
          + "".join(f"\n    {p['autoridad']} hasta {p['fechaFinProhibicion']}: {p['causaProhibicion'][:70]}" for p in e["prohibiciones_contratar"]))
    a = e.get("almacen")
    if a and "contratos" in a:
        c = a["contratos"]
        print(f"  Almacén local: {c['n']} contratos adjudicados ({eur(c['importe_sin_iva'] or 0)} sin IVA)"
              + "".join(f"\n    {r['fecha_adjudicacion']} {eur(r['importe_sin_iva'] or 0):>14}  {(r['organo'] or '')[:30]} | {(r['objeto'] or '')[:50]}" for r in c["recientes"][:3]))
        if a.get("borme"):
            actos = a["borme"]["actos"]
            print(f"  BORME ({a['borme']['denominacion_buscada']}): "
                  + ("; ".join(f"{b['fecha']} {', '.join(b['actos'])}" for b in actos[:5]) if actos else "sin actos en lo cargado"))
    print("  Sin consulta por NIF:")
    for k, v in e["no_cubierto"].items():
        print(f"    {k}: {v}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "A02066116")
