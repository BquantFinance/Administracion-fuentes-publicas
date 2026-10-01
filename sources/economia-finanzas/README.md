# Economía, finanzas y mercados

Sector `economia-finanzas` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Euríbor, tipos de interés y de cambio, crédito, balanza de pagos → `bde-estadisticas` (listaSeries con rango=MAX corta en las 1000 observaciones más recientes sin aviso; completar con rango=AAAA)
- Deuda pública por Administración (Protocolo de Déficit Excesivo) → `bde-estadisticas` (capítulo SB_DEUAAPP; histórico también en airef-datos)
- Subastas del Tesoro y deuda del Estado por instrumento y tenedor → `tesoro-estadisticas` (año en curso en 11.xlsx e históricos anuales; el HTML de subastas mezcla decimales con coma y con punto)
- Previsiones macroeconómicas y estimación del PIB en tiempo real → `airef-datos`
- Entidades supervisadas, hechos relevantes e informes financieros de cotizadas → `cnmv-registros` (sin API; formularios ASP.NET, XML mensual de IIC y RSS)
- Líneas ICO y avales por beneficiario → `ico-datos` (no hay datos descargables, solo memoria y cuentas en PDF)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [airef-datos](airef-datos.yaml) | AIReF – Datalab, observatorio de deuda y previsiones | download, portal | none | xlsx, pdf | quarterly | tls-chain-incomplete, static-html, url-drift | 2026-09-30 |
| [bde-estadisticas](bde-estadisticas.yaml) | Banco de España – API de estadísticas y CSV de series | api-rest, download | none | json, csv, xlsx, zip | daily | gzip-unannounced, latin1, soft-errors-200 | 2026-10-01 |
| [cnmv-registros](cnmv-registros.yaml) | CNMV – Registros oficiales, información regulada y estadísticas | portal, feed, download | none | html, xml, pdf, xlsx, rss | realtime | viewstate-forms, static-html, url-drift | 2026-09-30 |
| [ico-datos](ico-datos.yaml) | ICO – Informe anual y cuentas | portal | none | pdf, html | annual | static-html, url-drift | 2026-09-30 |
| [tesoro-estadisticas](tesoro-estadisticas.yaml) | Tesoro Público – Subastas, deuda en circulación y estadísticas mensuales | download, portal | none | xlsx, pdf, html | monthly | user-agent-browser, tls-chain-incomplete, static-html, overwritten-in-place | 2026-10-01 |

- **airef-datos**: Ficheros xlsx de la AIReF: histórico de deuda por Administración, cuadro macro de previsiones, estimación en tiempo real del PIB trimestral (MIPred) y por CCAA, y seguimiento del objetivo de estabilidad. Sin API localizada; los Excel se enlazan desde páginas WordPress.
- **bde-estadisticas**: Unas 12.800 series (tipos de interés y de cambio, euríbor, crédito, deuda pública, balanza de pagos, cuentas financieras) por API JSON, por CSV de cada cuadro del Boletín Estadístico y por ZIP de capítulo. Los códigos de serie se localizan en catálogos CSV.
- **cnmv-registros**: Registros oficiales de entidades supervisadas, información privilegiada (IPP) y otra información relevante (OIR), informes financieros de cotizadas, información pública de IIC en XML mensual, series estadísticas y feeds RSS. Portal ASP.NET sin API pública documentada.
- **ico-datos**: Solo documentos PDF: memoria anual, cuentas anuales consolidadas e información con relevancia prudencial. No publica estadísticas descargables de las Líneas ICO ni de los avales por beneficiario.
- **tesoro-estadisticas**: Subastas de Letras, Bonos y Obligaciones (última por plazo en HTML; año en curso y anterior en 11.xlsx; 2001-2025 en histórico), boletín mensual en 19 cuadros xlsx (circulación, vida media, tenedores, tipos, financiación neta, negociación) e históricos de tipos marginales, medios y efectivos.
