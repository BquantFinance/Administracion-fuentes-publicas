# Energía

Sector `energia` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [cnmc-data](cnmc-data.yaml) | CNMC Data – Estadísticas de energía, telecomunicaciones, audiovisual y postal | api-rest, download, portal | none | csv, json, xml | quarterly | — | 2026-09-30 |
| [minetur-precios-carburantes](minetur-precios-carburantes.yaml) | Geoportal de gasolineras – API REST de precios de carburantes | api-rest | none | json, xml | hourly | — | 2026-09-30 |
| [miteco-energia-estadisticas](miteco-energia-estadisticas.yaml) | MITECO y CORES – Balances energéticos y estadísticas de petróleo y gas | download, portal | none | xlsx, xls, ods, pdf | monthly | overwritten-in-place, url-drift | 2026-09-30 |

- **cnmc-data**: 210 datasets de la CNMC en un CKAN con datastore: electricidad y gas (cuotas de comercializadoras, cambios de suministrador, precios, garantías de origen, bono social), precios provinciales de carburantes, telecomunicaciones, audiovisual, transporte, postal y comercio electrónico.
- **minetur-precios-carburantes**: Precios vigentes de todos los carburantes en 11.491 estaciones terrestres y 148 postes marítimos, con coordenadas, dirección, horario, rótulo y margen, actualizados cada media hora, e histórico diario por fecha. JSON o XML sin autenticación, filtros por CCAA, provincia, municipio y producto.
- **miteco-energia-estadisticas**: Series de CORES en xlsx: consumo mensual de productos petrolíferos por provincia desde 1997, por grupo y total, consumo y existencias de gas, balances anuales y capacidad de refino. Del ministerio, balances y libros de la energía en PDF, coyuntura trimestral y refino mensual en xlsx y ods.
