# Vivienda y urbanismo

Sector `vivienda-urbanismo` · 1 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Precios de vivienda, transacciones, alquiler (SERPAVI) y suelo → `mivau-precios-vivienda-alquiler`

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [mivau-precios-vivienda-alquiler](mivau-precios-vivienda-alquiler.yaml) | Ministerio de Vivienda – Estadísticas de vivienda (Boletín Online en XLS) y SERPAVI | download, portal | none | xls, xlsx, geojson, shp, zip, pdf, html | quarterly | user-agent-browser, url-drift, overwritten-in-place, static-html, js-rendered | 2026-10-01 |

- **mivau-precios-vivienda-alquiler**: Transacciones de vivienda, valor tasado, parque, vivienda libre y protegida y suelo urbano en XLS trimestrales del Boletín Estadístico Online, y SERPAVI, alquiler de vivienda habitual de fuentes tributarias 2011-2024 por CCAA, provincia, municipio, distrito y sección censal en xlsx y GeoJSON.
