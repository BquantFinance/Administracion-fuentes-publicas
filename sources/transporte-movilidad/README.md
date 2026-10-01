# Transporte y movilidad

Sector `transporte-movilidad` · 7 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Datos oceanográficos en tiempo real (oleaje, mareas, boyas) → `puertos-estado-datos` (API interna de Portus sin documentar y sin clave (ubicaciones, mareas previstas, último dato por POST))
- Incidencias de tráfico, detectores, radares, zonas de bajas emisiones, puntos de recarga → `dgt-datex-trafico`
- Matriculaciones, bajas, parque de vehículos y conductores (microdatos) → `dgt-estadisticas` (no localizados microdatos de accidentes, solo tablas; los listados de bajas acaban en 2024-06)
- Matrices origen-destino de movilidad por telefonía móvil → `mitma-opendata-movilidad` (el host de datos respondió 403 desde el entorno de verificación)
- Horarios de trenes (GTFS), estaciones con coordenadas y posiciones en tiempo real → `renfe-datos-abiertos` (GTFS-RT con fallos TLS intermitentes, reintentar; Adif sin portal localizado)
- Tráfico portuario mensual por autoridad portuaria → `puertos-estado-datos`
- Tráfico aéreo mensual por aeropuerto, autopistas de peaje, ferrocarril, licitación y adjudicación de obra → `mitma-boletin-estadistico-online` (XLS con URL fija pero solo el total y 16 aeropuertos, sin otras clases de tráfico; la red completa de Aena en aesa-aviacion)
- Registro de aeronaves y operadores de drones → `aesa-aviacion` (matrículas activas en un PDF de AESA; operadores UAS sin listado público)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aesa-aviacion](aesa-aviacion.yaml) | Aena y AESA – Estadísticas de tráfico aéreo, registro de aeronaves y operadores UAS | download, portal | none | xlsx, xls, pdf, html | monthly | static-html, url-drift, overwritten-in-place | 2026-10-01 |
| [dgt-datex-trafico](dgt-datex-trafico.yaml) | DGT – NAP de tráfico y ficheros DATEX II (incidencias, detectores, cámaras, ZBE) | download | none | xml, rdf | realtime | url-drift, static-html | 2026-10-01 |
| [dgt-estadisticas](dgt-estadisticas.yaml) | DGT en cifras – Parque, matriculaciones, bajas, conductores, siniestralidad y microdatos | download, portal | none | xlsx, txt, zip, pdf, html | daily | latin1, url-drift, tls-chain-incomplete | 2026-10-01 |
| [mitma-boletin-estadistico-online](mitma-boletin-estadistico-online.yaml) | Transportes – Boletín estadístico online (aviación, puertos, carretera, ferrocarril) | download, portal | none | xls, html | monthly | static-html | 2026-10-01 |
| [mitma-opendata-movilidad](mitma-opendata-movilidad.yaml) | Ministerio de Transportes – Estudio de movilidad con big data (Open Data) | download | none | csv, zip, shp, geojson | irregular | waf-blocks-bots | — |
| [puertos-estado-datos](puertos-estado-datos.yaml) | Puertos del Estado – Estadística mensual de tráfico portuario y Portus (oceanografía) | download, portal, api-rest | none | xlsx, pdf, html, json | monthly | js-rendered, url-drift | 2026-10-01 |
| [renfe-datos-abiertos](renfe-datos-abiertos.yaml) | Renfe – Datos abiertos (GTFS, GTFS-RT, estaciones, viajeros) | api-rest, download, feed | none | zip, csv, xlsx, json, protobuf | realtime | latin1 | 2026-10-01 |

- **aesa-aviacion**: Informes mensuales y anuales de tráfico de Aena desde 2004 en Excel y PDF con URL directa (pasajeros, operaciones y mercancía por aeropuerto con variación interanual); cuadros por compañía y destino solo con registro. Aeronaves matriculadas de AESA en un PDF; operadores UAS sin listado público.
- **dgt-datex-trafico**: Ficheros DATEX II públicos sin clave: incidencias en tiempo real (versión 3.7, cada minuto) y 1.952 cámaras en el NAP; en infocar.dgt.es, medidas de unos 5.560 detectores cada minuto, radares, tramos, 47 zonas de bajas emisiones, puntos de recarga eléctrica e incidencias de Cataluña y País Vasco.
- **dgt-estadisticas**: Portal DGT en cifras con 226 productos por tema (tablas y series en xlsx, anuarios en PDF) y microdatos sin registro: matriculaciones diarias y mensuales (MATRABA, ancho fijo, desde 2014), bajas hasta 2024, parque de vehículos anual y mensual por vehículo, censo de conductores y sanciones.
- **mitma-boletin-estadistico-online**: Capítulos del Boletín estadístico del ministerio: licitación y adjudicaciones de obra, aviación civil (total y 16 mayores aeropuertos), Puertos del Estado, mercancías por carretera, autopistas de peaje, ferrocarril, costes de la construcción y visados. Cada tabla en XLS con URL fija por código.
- **mitma-opendata-movilidad**: Matrices diarias de viajes, pernoctaciones y personas entre distritos, municipios y grandes áreas urbanas, estimadas con telefonía móvil desde 2022, en CSV comprimidos con zonificaciones, estudios completos y rutas por carretera. El servidor de datos respondió 403 desde el entorno de verificación.
- **puertos-estado-datos**: Cuadros mensuales de tráfico por autoridad portuaria en xlsx desde 2012 (graneles, mercancía general, contenedores, pasajeros, pesca), anuario y memorias en PDF, y Portus, visor oceanográfico cuya API interna da sin clave mareas previstas y último dato de boyas y mareógrafos.
- **renfe-datos-abiertos**: CKAN con 44 datasets: horarios GTFS de Cercanías y de alta velocidad, larga y media distancia, feeds GTFS-RT (alertas, viajes y posiciones de trenes) en protobuf y JSON, 1.035 estaciones con coordenadas y viajeros por franja horaria y núcleo (año 2018). CC BY 4.0, sin clave.
