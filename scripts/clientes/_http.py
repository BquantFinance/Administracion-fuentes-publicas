"""Compatibilidad: los cargadores usan session(); la implementación está en sesion.py."""
from __future__ import annotations

try:
    from .sesion import ACCEPT, UA, bundle, sesion  # noqa: F401  (reexportados)
except ImportError:
    from sesion import ACCEPT, UA, bundle, sesion  # noqa: F401


def session(accept: str = "application/json, */*;q=0.8"):
    return sesion(accept=accept)
