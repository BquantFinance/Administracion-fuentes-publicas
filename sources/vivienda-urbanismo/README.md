# Vivienda y urbanismo

Sector `vivienda-urbanismo` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Precios de vivienda, transacciones, alquiler (SERPAVI) y suelo → `mivau-precios-vivienda-alquiler` (por municipio, perfil_municipio da las transacciones de los últimos cinco trimestres y el valor tasado (más de 25.000 habitantes) con el código INE ya casado; las tablas solo traen nombres)
- Viviendas turísticas (de uso turístico) de un municipio o una calle, con licencia o anunciadas → `viviendas-uso-turistico` (registros de Cataluña, Madrid, Andalucía y Comunitat Valenciana más el INE (VTE) en todos los municipios; registro e INE dan cifras distintas (Madrid 4.865 inscritas y 10.836 anunciadas); perfil_municipio trae las dos)
- Certificado y etiqueta energética de un edificio o vivienda, letras por municipio → `certificados-eficiencia-energetica` (por parcela en Cataluña y la Comunitat Valenciana (perfil_municipio con la dirección); Madrid y Andalucía solo en descarga y el datastore de Madrid se corta en 1.000 filas)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [certificados-eficiencia-energetica](certificados-eficiencia-energetica.yaml) | Certificados de eficiencia energética de edificios – registros autonómicos | api-rest, ogc, download | none | json, csv, gml, xml, zip, 7z | monthly | datastore-incomplete, user-agent-browser, connection-reset-intermittent, overwritten-in-place | 2026-10-05 |
| [mivau-precios-vivienda-alquiler](mivau-precios-vivienda-alquiler.yaml) | Ministerio de Vivienda – Estadísticas de vivienda (Boletín Online en XLS) y SERPAVI | download, portal | none | xls, xlsx, geojson, shp, zip, pdf, html | quarterly | user-agent-browser, url-drift, overwritten-in-place, static-html, js-rendered | 2026-10-05 |
| [viviendas-uso-turistico](viviendas-uso-turistico.yaml) | Viviendas de uso turístico – registros autonómicos e INE | api-rest, download | none | json, csv | daily | user-agent-browser, connection-reset-intermittent | 2026-10-05 |

- **certificados-eficiencia-energetica**: Certificados de eficiencia energética de los registros de Cataluña, Madrid, Comunitat Valenciana y Andalucía: referencia catastral, letra y valor de energía primaria no renovable y de emisiones, uso y fecha. Por parcela en Cataluña y la Comunitat Valenciana; Madrid y Andalucía, en descarga.
- **mivau-precios-vivienda-alquiler**: Transacciones de vivienda, valor tasado, parque, vivienda libre y protegida y suelo urbano en XLS trimestrales del Boletín Estadístico Online, y SERPAVI, alquiler de vivienda habitual de fuentes tributarias 2011-2024 por CCAA, provincia, municipio, distrito y sección censal en xlsx y GeoJSON.
- **viviendas-uso-turistico**: Viviendas de uso turístico inscritas en los registros de Cataluña, Madrid, Andalucía y Comunitat Valenciana (dirección y, según el caso, referencia catastral, plazas y alta) y las anunciadas en plataformas por municipio según el INE. No miden lo mismo.
