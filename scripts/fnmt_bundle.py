#!/usr/bin/env python3
"""Genera ca-age.pem: el bundle de certifi más las CA intermedias y raíces de FNMT-RCM que muchos servidores
.gob.es no envían (quirk tls-chain-incomplete), más el contenido de EXTRA_CA_BUNDLE si está definido (proxies).

Uso: fnmt_bundle.py [--out ca-age.pem]
Después: curl --cacert ca-age.pem ... | requests.get(url, verify="ca-age.pem") | export REQUESTS_CA_BUNDLE=ca-age.pem
"""
from __future__ import annotations

import argparse
import os
import re
import ssl
import sys

import certifi
import requests

from common import ROOT

BASE = "https://www.sede.fnmt.gob.es/documents/10445900/10526749"
CERTS = [
    "AC_Componentes_Informaticos_SHA256",
    "AC_Servidores_Seguros_Tipo1",
    "AC_Servidores_Seguros_Tipo2",
    "AC_Servidores_Seguros_Tipo1_G2",
    "AC_Servidores_Seguros_Tipo2_G2",
    "AC_Servidores_Seguros_Tipo2_G2R",
    "AC_Administracion_Publica_SHA256",
    "AC_Sector_Publico",
    "AC_Sector_Publico_G2",
    "AC_Raiz_FNMT-RCM-SS",
    "AC_Raiz_FNMT-RCM_G2",
    "AC_RAIZ_FNMTRCM_Servidores_Seguros_G2R",
]


PEM_RE = re.compile(rb"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", re.S)


def to_pem(data: bytes) -> str:
    """Devuelve el certificado en PEM; algunos .cer de FNMT son PEM con cabecera de texto (Subject:, Issuer:)."""
    m = PEM_RE.search(data)
    pem = m.group(0).decode("ascii") if m else ssl.DER_cert_to_PEM_cert(data)
    ssl.PEM_cert_to_DER_cert(pem)  # falla si no es un certificado válido
    return pem


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "ca-age.pem"))
    args = ap.parse_args()
    parts = [open(certifi.where(), encoding="ascii").read().rstrip() + "\n"]
    extra = os.environ.get("EXTRA_CA_BUNDLE")
    if extra and os.path.exists(extra):
        parts.append(open(extra, encoding="ascii").read().rstrip() + "\n")
    ok = 0
    for name in CERTS:
        url = f"{BASE}/{name}.cer"
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=40)
            r.raise_for_status()
            parts.append(f"# FNMT {name}\n{to_pem(r.content).rstrip()}\n")
            ok += 1
        except (requests.RequestException, ssl.SSLError, ValueError) as exc:
            print(f"no descargado {name}: {exc}", file=sys.stderr)
    with open(args.out, "w", encoding="ascii") as fh:
        fh.write("".join(parts))
    print(f"{args.out}: certifi + {ok}/{len(CERTS)} certificados FNMT" + (" + EXTRA_CA_BUNDLE" if extra else ""))
    return 0 if ok == len(CERTS) else 1


if __name__ == "__main__":
    sys.exit(main())
