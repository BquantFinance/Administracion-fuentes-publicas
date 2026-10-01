"""Hace importable scripts/clientes desde un clon del repo; tras pip install se usa fuentes_publicas.clientes."""
import sys
from pathlib import Path

try:
    import fuentes_publicas.clientes  # noqa: F401
    PAQUETE = "fuentes_publicas.clientes"
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    PAQUETE = "clientes"
