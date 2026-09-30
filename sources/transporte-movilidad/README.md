# Transporte y movilidad

Sector `transporte-movilidad` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aesa-aviacion](aesa-aviacion.yaml) | AESA y Aena – Registro de aeronaves, operadores y tráfico aéreo | portal, download | none | xlsx, pdf, html, csv | monthly | — | — |
| [dgt-datex-trafico](dgt-datex-trafico.yaml) | DGT – Incidencias de tráfico en tiempo real (DATEX II) y cámaras | download, api-rest | none | xml | realtime | — | — |
| [dgt-estadisticas](dgt-estadisticas.yaml) | DGT – Estadísticas de parque, matriculaciones, conductores y siniestralidad | portal, download | none | xlsx, csv, txt, pdf | monthly | — | — |
| [mitma-opendata-movilidad](mitma-opendata-movilidad.yaml) | Ministerio de Transportes – Estudio de movilidad con big data (Open Data) | download | none | csv, zip, shp, geojson | daily | — | — |
| [puertos-estado-datos](puertos-estado-datos.yaml) | Puertos del Estado – Estadísticas portuarias y datos oceanográficos | portal, download, api-rest | none | xlsx, csv, json, pdf | hourly | — | — |

- **aesa-aviacion**: Registro de Matrícula de Aeronaves, operadores y escuelas certificadas, registro de operadores de drones (UAS), estadísticas de tráfico de pasajeros, operaciones y carga por aeropuerto de Aena.
- **dgt-datex-trafico**: Incidencias de tráfico (accidentes, obras, retenciones, meteorología adversa) de la red interurbana en formato DATEX II actualizado cada pocos minutos, más cámaras y paneles. Sin autenticación.
- **dgt-estadisticas**: Parque de vehículos, matriculaciones y transferencias mensuales (con microdatos diarios por vehículo anonimizado), censo de conductores, accidentes con víctimas (microdatos anuales), sanciones. Portal estadístico y descargas.
- **mitma-opendata-movilidad**: Matrices diarias de viajes origen-destino entre distritos, municipios y grandes áreas, por hora, distancia y motivo, estimadas a partir de telefonía móvil desde 2020. Ficheros CSV comprimidos diarios y zonificaciones.
- **puertos-estado-datos**: Tráfico mensual de mercancías, contenedores, pasajeros y buques por autoridad portuaria; red de boyas y mareógrafos con datos de oleaje, viento y nivel del mar en tiempo real e histórico (Portus); predicciones de oleaje.
