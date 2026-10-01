# Sanidad y medicamentos

Sector `sanidad-medicamentos` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Medicamentos, presentaciones, fichas técnicas y problemas de suministro → `aemps-cima-api` (sin precios; precios y financiación en sanidad-nomenclator-facturacion)
- Precios, financiación y aportación de medicamentos (nomenclátor de facturación) → `sanidad-nomenclator-facturacion`
- Ensayos clínicos (REEC) y alertas de seguridad → `aemps-otros-registros` (sin API documentada; buscador JSON por GET (arise/search), detalle por POST con cookie y alertas en la API REST de WordPress)
- Exceso de mortalidad (MoMo), COVID-19, boletines epidemiológicos, gripe → `isciii-cne`
- Hospitales, altas hospitalarias e indicadores del Sistema Nacional de Salud → `sanidad-portal-estadistico` (Catálogo de Hospitales en xlsx; cubos exportables a CSV por POST de WebForms; Indicadores Clave en JSON (export/data))

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aemps-cima-api](aemps-cima-api.yaml) | AEMPS CIMA – API REST de medicamentos autorizados y nomenclátor de prescripción | api-rest, download | none | json, xml, pdf, html, zip | daily | user-agent-browser, overwritten-in-place | 2026-10-01 |
| [aemps-otros-registros](aemps-otros-registros.yaml) | AEMPS – Registro Español de Estudios Clínicos (REEC), notas informativas y alertas | api-rest, feed, portal | none | json, rss, html, pdf | daily | session-required, js-rendered, errors-html-or-xml, soft-errors-200 | 2026-10-01 |
| [isciii-cne](isciii-cne.yaml) | ISCIII – Centro Nacional de Epidemiología (RENAVE, MoMo, SiVIRA, COVID-19) | download, portal | none | csv, xlsx, pdf, html | weekly | url-drift, static-html | 2026-10-01 |
| [sanidad-nomenclator-facturacion](sanidad-nomenclator-facturacion.yaml) | Ministerio de Sanidad – Nomenclátor de facturación (medicamentos financiados y precios) | download, portal | none | csv, xls, rdf, html | monthly | static-html, overwritten-in-place | 2026-10-01 |
| [sanidad-portal-estadistico](sanidad-portal-estadistico.yaml) | Ministerio de Sanidad – Portal Estadístico del SNS y Catálogo Nacional de Hospitales | download, portal, api-rest | none | xlsx, csv, json, pdf, html | annual | tls-chain-incomplete, viewstate-forms, latin1, url-drift, soft-errors-200 | 2026-10-01 |

- **aemps-cima-api**: Los 25.487 medicamentos registrados en España (20.464 autorizados): composición, principios activos, ATC, presentaciones con código nacional, estado, ficha técnica y prospecto en PDF, HTML y secciones, problemas de suministro y registro de cambios. JSON sin autenticación y nomenclátor XML diario.
- **aemps-otros-registros**: Registro Español de Estudios Clínicos (11.936 estudios el 1/10/2026) con buscador JSON por GET y detalle por estudio en arrays JSON tras fijar sesión; notas informativas y alertas de seguridad por RSS y API REST de WordPress (5.249 entradas). Sin API documentada ni descarga masiva del REEC.
- **isciii-cne**: Vigilancia epidemiológica: exceso de mortalidad diario MoMo en CSV (nacional, CCAA y provincia por sexo y edad desde 2015), histórico COVID-19 por provincia, sexo y edad en CSV (2020-2023), tablas xlsx del informe semanal SiVIRA (gripe, COVID-19, VRS) y boletines e informes anuales RENAVE en PDF.
- **sanidad-nomenclator-facturacion**: Los 20.571 productos del nomenclátor de facturación del SNS (17.209 en alta, el resto de baja o suspendidos): código nacional, laboratorio, principio activo, estado, alta y baja, aportación, PVP con IVA, precio de referencia y agrupación homogénea. CSV, Excel y RDF completos y buscador web.
- **sanidad-portal-estadistico**: Catálogo Nacional de Hospitales en xlsx (848 hospitales con código, camas, municipio, dependencia, complejo y alta tecnología), cubos de la Consulta Interactiva del SNS (RAE-CMBD, SIAE, SIAP, BDCAP, Barómetro) exportables a CSV por POST e Indicadores Clave del SNS (186) en JSON por GET.
