# Energía

Sector `energia` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Precios de carburantes por gasolinera → `minetur-precios-carburantes`
- Comercializadoras, cambios de suministrador, bono social, garantías de origen → `cnmc-data`
- Consumo de productos petrolíferos y gas por provincia, balances energéticos → `miteco-energia-estadisticas` (series de CORES en xlsx; el ministerio publica PDF)
- Demanda, generación por tecnología, PVPC y precio spot horarios → `ree-redata` (WAF intermitente; reintentar; ESIOS exige token)
- Precio marginal del mercado diario e intradiario, curvas y programas de casación → `omie-mercado` (ficheros de texto por día; 96 periodos cuarto-horarios en 2026)
- Registro de instalaciones de producción eléctrica y autoconsumo → `miteco-energia-estadisticas` (no localizada descarga abierta; PRETOR da 404)
- Telecomunicaciones (líneas, operadores, audiovisual) → `cnmc-data`

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [cnmc-data](cnmc-data.yaml) | CNMC Data – Estadísticas de energía, telecomunicaciones, audiovisual y postal | api-rest, download, portal | none | csv, json, xml | quarterly | url-drift, js-rendered | 2026-09-30 |
| [minetur-precios-carburantes](minetur-precios-carburantes.yaml) | Geoportal de gasolineras – API REST de precios de carburantes | api-rest | none | json, xml | hourly | — | 2026-09-30 |
| [miteco-energia-estadisticas](miteco-energia-estadisticas.yaml) | MITECO y CORES – Balances energéticos y estadísticas de petróleo y gas | download, portal | none | xlsx, xls, ods, pdf | monthly | overwritten-in-place, url-drift | 2026-09-30 |
| [omie-mercado](omie-mercado.yaml) | OMIE – Resultados del mercado diario e intradiario de electricidad | download | none | csv, txt, zip | daily | latin1, static-html | 2026-09-30 |
| [ree-redata](ree-redata.yaml) | Red Eléctrica – API REData (demanda, generación, precios, intercambios) | api-rest | none | json | daily | waf-intermittent-403, errors-html-or-xml | 2026-09-30 |

- **cnmc-data**: 210 datasets de la CNMC en un CKAN con datastore: electricidad y gas (cuotas de comercializadoras, cambios de suministrador, precios, garantías de origen, bono social), precios provinciales de carburantes, telecomunicaciones, audiovisual, transporte, postal y comercio electrónico.
- **minetur-precios-carburantes**: Precios vigentes de todos los carburantes en 11.491 estaciones terrestres y 148 postes marítimos, con coordenadas, dirección, horario, rótulo y margen, actualizados cada media hora, e histórico diario por fecha. JSON o XML sin autenticación, filtros por CCAA, provincia, municipio y producto.
- **miteco-energia-estadisticas**: Series de CORES en xlsx: consumo mensual de productos petrolíferos por provincia desde 1997, por grupo y total, consumo y existencias de gas, balances anuales y capacidad de refino. Del ministerio, balances y libros de la energía en PDF, coyuntura trimestral y refino mensual en xlsx y ods.
- **omie-mercado**: Precio marginal del mercado diario en España y Portugal (96 periodos cuarto-horarios por día en 2026), programas de casación, curvas de oferta y demanda, ofertas, intradiario de subastas y continuo, capacidades e indisponibilidades. Ficheros de texto con URL fija, sin clave.
- **ree-redata**: API pública sin clave de REData: demanda (evolución, tiempo real, pérdidas), generación por tecnología, balance, emisiones, precios horarios PVPC y spot, intercambios por frontera y red de transporte, por sistema eléctrico. JSON con una serie por concepto. ESIOS exige token.
