"""Lanzador del paquete MCPB: ejecuta con uvx el servidor que fija manifest.json (requiere uv instalado)."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

cfg = json.loads((Path(__file__).resolve().parent.parent / "manifest.json").read_text(encoding="utf-8"))["server"]["mcp_config"]
exe = shutil.which(cfg["command"])
if not exe:
    sys.exit("No se encuentra uvx en el PATH; instala uv: https://docs.astral.sh/uv/getting-started/installation/")
sys.exit(subprocess.call([exe, *cfg["args"]]))
