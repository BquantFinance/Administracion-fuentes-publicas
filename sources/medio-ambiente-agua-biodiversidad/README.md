# Medio ambiente, agua y biodiversidad

Sector `medio-ambiente-agua-biodiversidad` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Calidad del aire validada por estación y contaminante → `miteco-calidad-aire` (datos anuales validados; el tiempo real lo sirve cada comunidad autónoma, fuera del alcance)
- Emisiones industriales por complejo (PRTR) → `miteco-prtr`
- Reserva de embalses, caudales y estaciones de aforo → `miteco-saih-boletin-hidrologico`
- Red Natura 2000, espacios protegidos, hábitats, humedales, inventario forestal → `miteco-banco-datos-naturaleza` (descargas con desafío ALTCHA (resuelto en la guía); los WMS de mapama están rotos)
- Emisiones de gases de efecto invernadero y contaminantes atmosféricos por sector (inventario nacional) → `miteco-inventario-emisiones` (por categoría IPCC; por instalación en miteco-prtr)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [miteco-banco-datos-naturaleza](miteco-banco-datos-naturaleza.yaml) | MITECO – Banco de Datos de la Naturaleza e Inventario del Patrimonio Natural (IEPNB) | download, portal | none | shp, gml, gdb, geojson, kml, xlsx, zip, xml | irregular | captcha-required, url-drift | 2026-09-30 |
| [miteco-calidad-aire](miteco-calidad-aire.yaml) | MITECO – Calidad del aire (datos oficiales validados de estaciones) | download, portal | none | csv, zip, xlsx, xls, pdf | annual | url-drift, static-html | 2026-09-30 |
| [miteco-inventario-emisiones](miteco-inventario-emisiones.yaml) | MITECO – Inventario nacional de emisiones (gases de efecto invernadero y contaminantes) | download | none | xlsx, zip, pdf | annual | static-html, url-drift | 2026-09-30 |
| [miteco-prtr](miteco-prtr.yaml) | PRTR-España – Registro Estatal de Emisiones y Fuentes Contaminantes | download, portal | none | xml, zip, html | annual | viewstate-forms, url-drift | 2026-09-30 |
| [miteco-saih-boletin-hidrologico](miteco-saih-boletin-hidrologico.yaml) | MITECO – Boletín hidrológico, histórico de embalses y anuario de aforos | download, portal | none | csv, zip, pdf, html | weekly | url-drift, js-rendered | 2026-09-30 |

- **miteco-banco-datos-naturaleza**: Capas oficiales de biodiversidad: Red Natura 2000, espacios protegidos, hábitats y especies del artículo 17, humedales Ramsar e IEZH, reservas de la biosfera, Mapa Forestal e Inventario Forestal Nacional. Shapefile y GML en gis.miteco.gob.es (desafío ALTCHA) y GDB, shp y GeoJSON directos del IEPNB.
- **miteco-calidad-aire**: Datos validados de todas las estaciones de las redes autonómicas y locales, un ZIP por año con un CSV por contaminante: horarios (SO2, NO, NO2, NOx, O3, CO, PM10, PM2.5, C6H6), diarios (PM, metales, B(a)P) e irregulares, más metainformación de estaciones con coordenadas y código europeo.
- **miteco-inventario-emisiones**: Serie 1990-2024 de emisiones de gases de efecto invernadero por gas y sector en una tabla resumen xlsx, tablas CRT de la UNFCCC (un xlsx por año en ZIP) con el diccionario de categorías IPCC, e inventario de contaminantes atmosféricos (CLRTAP) por territorio y dominio EMEP. Edición anual.
- **miteco-prtr**: Emisiones anuales a aire, agua y suelo y transferencias de residuos de cada complejo industrial afectado, por sustancia y método, más el inventario de complejos con CNAE, actividad PRTR e IPPC y municipio. Descarga masiva en XML por año (emisiones 2001-2024, residuos 2007-2024) y consultas web.
- **miteco-saih-boletin-hidrologico**: Reserva semanal de cada embalse peninsular de más de 5 hm3 desde 1988 (base Access), boletín hidrológico semanal en PDF, anuario de aforos con series diarias de caudal y nivel por estación desde 1912 (CSV por cuenca) y listado de estaciones. Los SAIH en tiempo real son de cada confederación.
