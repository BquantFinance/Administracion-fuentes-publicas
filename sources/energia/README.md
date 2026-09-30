# Energía

Sector `energia` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | verificada |
|---|---|---|---|---|---|---|
| [cnmc-data](cnmc-data.yaml) | CNMC Data – Estadísticas de energía, telecomunicaciones y audiovisual | portal, download, api-rest | none | csv, xlsx, json | quarterly | — |
| [minetur-precios-carburantes](minetur-precios-carburantes.yaml) | Geoportal de gasolineras – API de precios de carburantes | api-rest | none | json, xml | daily | — |
| [miteco-energia-estadisticas](miteco-energia-estadisticas.yaml) | MITECO – Balances energéticos, hidrocarburos y registro de instalaciones | portal, download | none | xlsx, pdf, csv | monthly | — |

- **cnmc-data**: Portal de datos abiertos de la CNMC: mercado eléctrico y gasista (comercializadoras, cambios de suministrador, precios, autoconsumo), telecomunicaciones (líneas, ingresos, cuotas por operador), audiovisual y postal. Descarga por indicador con API CKAN.
- **minetur-precios-carburantes**: Precios diarios de todos los carburantes en todas las estaciones de servicio de España con coordenadas, dirección, horario y rótulo. API REST JSON sin autenticación, también histórico por fecha.
- **miteco-energia-estadisticas**: Balances energéticos anuales, estadísticas de hidrocarburos (consumo de productos petrolíferos y gas por provincia, vía CORES), registro administrativo de instalaciones de producción eléctrica, autoconsumo y planes energéticos.
