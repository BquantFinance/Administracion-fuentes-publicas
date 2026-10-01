# Economía, finanzas y mercados

Sector `economia-finanzas` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Euríbor, tipos de interés y de cambio, crédito, balanza de pagos → `bde-estadisticas` (listaSeries con rango=MAX corta en las 1000 observaciones más recientes sin aviso; completar con rango=AAAA)
- Deuda pública por Administración (Protocolo de Déficit Excesivo) → `bde-estadisticas` (capítulo SB_DEUAAPP; airef-datos solo da la ratio total sobre PIB por informe, no por Administración)
- Subastas del Tesoro y deuda del Estado por instrumento y tenedor → `tesoro-estadisticas` (año en curso en 11.xlsx e históricos anuales; el HTML de subastas mezcla decimales con coma y con punto)
- Previsiones macroeconómicas y estimación del PIB en tiempo real → `airef-datos` (xlsx en wp-content/uploads con rutas que cambian en cada actualización; tomar el enlace de la página)
- Entidades supervisadas, hechos relevantes e informes financieros de cotizadas → `cnmv-registros` (sin API; formularios ASP.NET, XML mensual de IIC y RSS)
- Líneas ICO y avales por beneficiario → `ico-datos` (sin datos por beneficiario ni descargas tabulares; aprobaciones agregadas por canal en tablas HTML)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [airef-datos](airef-datos.yaml) | AIReF – Datalab, observatorio de deuda y previsiones | download, portal | none | xlsx, pdf | quarterly | tls-chain-incomplete, static-html, url-drift | 2026-10-01 |
| [bde-estadisticas](bde-estadisticas.yaml) | Banco de España – API de estadísticas y CSV de series | api-rest, download | none | json, csv, xlsx, zip | daily | gzip-unannounced, latin1, soft-errors-200 | 2026-10-01 |
| [cnmv-registros](cnmv-registros.yaml) | CNMV – Registros oficiales, información regulada y estadísticas | portal, feed, download | none | html, xml, pdf, xlsx, rss | realtime | viewstate-forms, static-html, url-drift | 2026-10-01 |
| [ico-datos](ico-datos.yaml) | ICO – Informe anual y cuentas | portal, scraping | none | pdf, html | annual | static-html, url-drift | 2026-10-01 |
| [tesoro-estadisticas](tesoro-estadisticas.yaml) | Tesoro Público – Subastas, deuda en circulación y estadísticas mensuales | download, portal | none | xlsx, pdf, html | monthly | user-agent-browser, tls-chain-incomplete, static-html, overwritten-in-place | 2026-10-01 |

- **airef-datos**: Ficheros xlsx de la AIReF: ratio de deuda pública sobre PIB por informe, cuadro macro de previsiones, estimación en tiempo real del PIB trimestral (MIPred) y PIB trimestral por CCAA (METCAP); seguimiento del objetivo de estabilidad solo en PDF. Sin API localizada; Excel enlazados desde WordPress.
- **bde-estadisticas**: Unas 12.800 series (tipos de interés y de cambio, euríbor, crédito, deuda pública, balanza de pagos, cuentas financieras) por API JSON, por CSV de cada cuadro del Boletín Estadístico y por ZIP de capítulo. Los códigos de serie se localizan en catálogos CSV.
- **cnmv-registros**: Registros oficiales de entidades supervisadas, información privilegiada (IP) y otra información relevante (OIR), informes financieros de cotizadas, información pública de IIC en XML mensual, series estadísticas y feeds RSS. Portal ASP.NET sin API pública documentada.
- **ico-datos**: Memoria, cuentas anuales consolidadas e información con relevancia prudencial en PDF, y una página con tablas HTML de aprobaciones por canal (mediación, financiación directa, avales, capital), magnitudes y ratios. Sin descargas tabulares ni datos por beneficiario.
- **tesoro-estadisticas**: Subastas de Letras, Bonos y Obligaciones (última por plazo en HTML; año en curso y anterior en 11.xlsx; 2001-2025 en histórico), boletín mensual en 19 cuadros xlsx (circulación, vida media, tenedores, tipos, financiación neta, negociación) e históricos de tipos marginales, medios y efectivos.
