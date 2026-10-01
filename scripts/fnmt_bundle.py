#!/usr/bin/env python3
"""Genera ca-age.pem: el bundle de certifi más las CA intermedias y raíces de FNMT-RCM que muchos servidores
.gob.es no envían (quirk tls-chain-incomplete), más los bundles del entorno (EXTRA_CA_BUNDLE, REQUESTS_CA_BUNDLE,
CURL_CA_BUNDLE, SSL_CERT_FILE) para no romper proxies. La lógica está en clientes/sesion.py, que lo genera solo en
~/.cache/fuentes-publicas si no encuentra ca-age.pem.

Uso: fnmt_bundle.py [--out ca-age.pem]
Después: curl --cacert ca-age.pem ... | requests.get(url, verify="ca-age.pem") | export REQUESTS_CA_BUNDLE=ca-age.pem
"""
from __future__ import annotations

import argparse
import sys

from clientes.sesion import _bundles_entorno, generar_bundle
from common import ROOT


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "ca-age.pem"))
    args = ap.parse_args()
    entorno = _bundles_entorno()
    ruta, ok, total = generar_bundle(args.out)
    print(f"{ruta}: certifi + {ok}/{total} certificados FNMT" + (f" + {', '.join(entorno)}" if entorno else ""))
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
