# Justicia, interior y seguridad

Sector `justicia-interior-seguridad` · 1 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Criminalidad por tipología, comunidad, provincia y municipio → `interior-criminalidad` (balances acumulados desde enero; código INE de municipio solo desde 2024)
- Detenciones, victimizaciones y hechos esclarecidos por provincia, sexo y edad → `interior-criminalidad` (series anuales PC-Axis 2010-2025 en /Datos2/, /Datos3/ y /Datos4/)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [interior-criminalidad](interior-criminalidad.yaml) | Ministerio del Interior – Portal Estadístico de Criminalidad (balances y series anuales) | download, portal | none | csv, px, xlsx, html | quarterly | latin1, js-rendered, static-html, errors-html-or-xml, url-drift | 2026-10-01 |

- **interior-criminalidad**: Balances trimestrales acumulados de infracciones penales por tipología (CCAA, provincia, isla y municipio) desde 2016, con comparación interanual, y series anuales 2010-2025 de hechos conocidos, esclarecidos, detenciones y victimizaciones por CCAA y provincia; PC-Axis con descarga CSV, px y xlsx.
