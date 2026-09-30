# Transporte y movilidad

Sector `transporte-movilidad` · 6 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Datos oceanográficos en tiempo real (oleaje, mareas, boyas) → `puertos-estado-datos` (Portus es una aplicación con API interna no reproducida)
- Incidencias de tráfico, detectores, radares, zonas de bajas emisiones, puntos de recarga → `dgt-datex-trafico`
- Matriculaciones, bajas, parque de vehículos y conductores (microdatos) → `dgt-estadisticas` (no localizados microdatos de accidentes, solo tablas)
- Matrices origen-destino de movilidad por telefonía móvil → `mitma-opendata-movilidad` (el host de datos respondió 403 desde el entorno de verificación)
- Horarios de trenes (GTFS), estaciones con coordenadas y posiciones en tiempo real → `renfe-datos-abiertos` (GTFS-RT no verificado desde el entorno; Adif sin portal localizado)
- Tráfico portuario mensual por autoridad portuaria → `puertos-estado-datos`
- Tráfico aéreo por aeropuerto y registro de aeronaves → `aesa-aviacion` (degradada; sin ficheros verificados)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aesa-aviacion](aesa-aviacion.yaml) | AESA y Aena – Registro de aeronaves, operadores UAS y estadísticas de tráfico aéreo | portal | registration | html, pdf | monthly | js-rendered, session-required | 2026-09-30 |
| [dgt-datex-trafico](dgt-datex-trafico.yaml) | DGT – NAP de tráfico y ficheros DATEX II (incidencias, detectores, cámaras, ZBE) | download | none | xml, rdf | realtime | url-drift, static-html | 2026-09-30 |
| [dgt-estadisticas](dgt-estadisticas.yaml) | DGT en cifras – Parque, matriculaciones, bajas, conductores, siniestralidad y microdatos | download, portal | none | xlsx, txt, zip, pdf, html | daily | latin1, url-drift, tls-chain-incomplete | 2026-09-30 |
| [mitma-opendata-movilidad](mitma-opendata-movilidad.yaml) | Ministerio de Transportes – Estudio de movilidad con big data (Open Data) | download | none | csv, zip, shp, geojson | daily | waf-blocks-bots | — |
| [puertos-estado-datos](puertos-estado-datos.yaml) | Puertos del Estado – Estadística mensual de tráfico portuario y Portus (oceanografía) | download, portal | none | xlsx, pdf, html, json | monthly | js-rendered, url-drift | 2026-09-30 |
| [renfe-datos-abiertos](renfe-datos-abiertos.yaml) | Renfe – Datos abiertos (GTFS, GTFS-RT, estaciones, viajeros) | api-rest, download, feed | none | zip, csv, xlsx, json, protobuf | realtime | latin1 | 2026-09-30 |

- **aesa-aviacion**: Registro de Matrícula de Aeronaves Civiles y registro de operadores de UAS (trámites en sede con certificado, sin listado abierto localizado) y estadísticas de tráfico de Aena (informes por aeropuerto en una web con sesión y enlaces generados por JavaScript). Sin ficheros descargables verificados.
- **dgt-datex-trafico**: Ficheros DATEX II públicos sin clave: incidencias en tiempo real (versión 3.7, cada minuto) y cámaras en el NAP; en infocar.dgt.es, medidas de 5.569 detectores cada minuto, radares, tramos, zonas de bajas emisiones, puntos de recarga eléctrica e incidencias de Cataluña y Gipuzkoa.
- **dgt-estadisticas**: Portal DGT en cifras con 226 productos por tema (tablas y series en xlsx, anuarios en PDF) y microdatos descargables sin registro: matriculaciones y bajas diarias y mensuales (MATRABA, ancho fijo, desde 2014), parque de vehículos anual y mensual por vehículo, censo de conductores y sanciones.
- **mitma-opendata-movilidad**: Matrices diarias de viajes origen-destino entre distritos, municipios y grandes áreas urbanas, por hora, distancia y motivo, estimadas con telefonía móvil desde 2020, en CSV comprimidos diarios más zonificaciones. El servidor de datos respondió 403 desde este entorno; las páginas del ministerio sí.
- **puertos-estado-datos**: Cuadros resumen mensuales de tráfico por autoridad portuaria en xlsx (mercancías por naturaleza, líquidos, sólidos, mercancía general, contenedores, pesca), memorias anuales en PDF y Portus, aplicación de datos oceanográficos en tiempo real, históricos y predicciones con API interna.
- **renfe-datos-abiertos**: CKAN con 44 datasets: horarios GTFS de Cercanías y de alta velocidad, larga y media distancia, feeds GTFS-RT (alertas, viajes y posiciones de trenes) en protobuf y JSON, 1.036 estaciones con coordenadas, viajeros por franja horaria y núcleo, y puntualidad. CC BY 4.0, sin clave.
