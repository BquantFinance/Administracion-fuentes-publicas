# Vivienda y urbanismo

Sector `vivienda-urbanismo` · 2 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Precios de vivienda, transacciones, alquiler (SERPAVI) y suelo → `mivau-precios-vivienda-alquiler`
- Viviendas turísticas (de uso turístico) de un municipio o una calle, con licencia o anunciadas → `viviendas-uso-turistico` (registros de Cataluña, Madrid, Andalucía y Comunitat Valenciana más el INE (VTE) en todos los municipios; registro e INE dan cifras distintas (Madrid 4.865 inscritas y 10.836 anunciadas); perfil_municipio trae las dos)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [mivau-precios-vivienda-alquiler](mivau-precios-vivienda-alquiler.yaml) | Ministerio de Vivienda – Estadísticas de vivienda (Boletín Online en XLS) y SERPAVI | download, portal | none | xls, xlsx, geojson, shp, zip, pdf, html | quarterly | user-agent-browser, url-drift, overwritten-in-place, static-html, js-rendered | 2026-10-01 |
| [viviendas-uso-turistico](viviendas-uso-turistico.yaml) | Viviendas de uso turístico – registros autonómicos e INE | api-rest, download | none | json, csv | daily | user-agent-browser, connection-reset-intermittent | 2026-10-05 |

- **mivau-precios-vivienda-alquiler**: Transacciones de vivienda, valor tasado, parque, vivienda libre y protegida y suelo urbano en XLS trimestrales del Boletín Estadístico Online, y SERPAVI, alquiler de vivienda habitual de fuentes tributarias 2011-2024 por CCAA, provincia, municipio, distrito y sección censal en xlsx y GeoJSON.
- **viviendas-uso-turistico**: Viviendas de uso turístico inscritas en los registros de Cataluña, Madrid, Andalucía y Comunitat Valenciana (dirección y, según el caso, referencia catastral, plazas y alta) y las anunciadas en plataformas por municipio según el INE. No miden lo mismo.
