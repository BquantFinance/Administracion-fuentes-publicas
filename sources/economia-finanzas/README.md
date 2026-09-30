# Economía, finanzas y mercados

Sector `economia-finanzas` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | verificada |
|---|---|---|---|---|---|---|
| [airef-datos](airef-datos.yaml) | AIReF – Datalab, observatorio de deuda y previsiones | download, portal | none | xlsx, pdf | quarterly | 2026-09-30 |
| [bde-estadisticas](bde-estadisticas.yaml) | Banco de España – API de estadísticas y CSV de series | api-rest, download | none | json, csv, xlsx, zip | daily | 2026-09-30 |
| [cnmv-registros](cnmv-registros.yaml) | CNMV – Registros oficiales, información regulada y estadísticas | portal, feed, download | none | html, xml, pdf, xlsx, rss | realtime | 2026-09-30 |
| [ico-datos](ico-datos.yaml) | ICO – Informe anual y cuentas | portal | none | pdf, html | annual | 2026-09-30 |
| [tesoro-estadisticas](tesoro-estadisticas.yaml) | Tesoro Público – Subastas, deuda en circulación y estadísticas mensuales | download, portal | none | xlsx, pdf, html | monthly | 2026-09-30 |

- **airef-datos**: Ficheros xlsx de la AIReF: histórico de deuda por Administración, cuadro macro de previsiones, estimación en tiempo real del PIB trimestral (MIPred) y por CCAA, y seguimiento del objetivo de estabilidad. Sin API; los Excel se enlazan desde páginas WordPress.
- **bde-estadisticas**: Más de 14000 series (tipos de interés y de cambio, euríbor, crédito, deuda pública, balanza de pagos, cuentas financieras) por API JSON, por CSV de cada cuadro del Boletín Estadístico y por ZIP de capítulo. Los códigos de serie se localizan en catálogos CSV.
- **cnmv-registros**: Registros oficiales de entidades supervisadas, información privilegiada (IPP) y otra información relevante (OIR), informes financieros de cotizadas, información pública de IIC en XML mensual, series estadísticas y feeds RSS. Portal ASP.NET sin API pública.
- **ico-datos**: Solo documentos PDF: memoria anual, cuentas anuales consolidadas e información con relevancia prudencial. No publica estadísticas descargables de las Líneas ICO ni de los avales por beneficiario.
- **tesoro-estadisticas**: Resultados de subastas de Letras, Bonos y Obligaciones (tablas HTML por instrumento e histórico en xlsx), boletín mensual en 19 cuadros xlsx (nominal en circulación, vida media, tenedores, vencimientos, negociación) e históricos de tipos marginales, medios y efectivos.
