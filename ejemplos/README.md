# Ejemplos

Proyectos pequeños que funcionan contra los servidores reales, probados el 2026-10-01. Cada uno resuelve las trampas
de su fuente (lo dice su cabecera) y sirve de punto de partida para un bot, un cron o un agente. Desde un clon del
repo funcionan tal cual; instalado el paquete (`pip install "fuentes-publicas-mcp @ git+https://github.com/BquantFinance/Administracion-fuentes-publicas"`),
también desde cualquier sitio.

| ejemplo | qué hace | fuentes |
|---|---|---|
| `python ejemplos/carburante_cerca.py "Alcalá de Henares" gasoleo 8` | gasolineras más baratas en un radio | MINETUR, municipios |
| `python ejemplos/boe_hoy.py subvención vivienda` | BOE del día filtrado, en Markdown | BOE |
| `python ejemplos/licitaciones.py 72 software` | licitaciones nuevas por CPV y palabra, solo lo no visto | PLACSP |
| `python ejemplos/mi_municipio.py "Alcalá de Henares"` | códigos, padrón, renta y criminalidad de un municipio | INE, Interior, municipios |
| `python ejemplos/subvenciones_empresa.py Q1132001G` | ayudas de una empresa o entidad por NIF, por año y concedente | BDNS |
| `python ejemplos/empresa_nif.py A02066116` | perfil público de un NIF: sector público, BDNS, AEI y prohibiciones de contratar | Invente, BDNS, AEI, ROLECE |

Salida de `mi_municipio.py "Alcalá de Henares"` el 2026-10-01:

```
Alcalá de Henares · Madrid · INE 28005 (con control 280053) · SIGPAC/Catastro 28:5
  DIR3 L01280053 · NIF del ayuntamiento P2800500G · NUTS3 ES300 · capital Alcalá de Henares (40.481793, -3.364867)
  Población (padrón a 2025-01-01): 203.208
  Renta neta media por persona (2023): 15.598 €
  Infracciones penales: enero-junio 2025 4.990, enero-junio 2026 5.697 (acumulado desde enero)
```
