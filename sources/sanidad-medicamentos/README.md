# Sanidad y medicamentos

Sector `sanidad-medicamentos` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Medicamentos, presentaciones, fichas técnicas y problemas de suministro → `aemps-cima-api` (sin precios; precios y financiación en sanidad-nomenclator-facturacion)
- Precios, financiación y aportación de medicamentos (nomenclátor de facturación) → `sanidad-nomenclator-facturacion`
- Ensayos clínicos (REEC) y alertas de seguridad → `aemps-otros-registros` (sin API; el REEC exige sesión)
- Exceso de mortalidad (MoMo), COVID-19, boletines epidemiológicos, gripe → `isciii-cne`
- Hospitales, altas hospitalarias e indicadores del Sistema Nacional de Salud → `sanidad-portal-estadistico` (solo el Catálogo de Hospitales tiene descarga directa)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aemps-cima-api](aemps-cima-api.yaml) | AEMPS CIMA – API REST de medicamentos autorizados y nomenclátor de prescripción | api-rest, download | none | json, xml, pdf, html, zip | daily | user-agent-browser, overwritten-in-place | 2026-10-01 |
| [aemps-otros-registros](aemps-otros-registros.yaml) | AEMPS – Registro Español de Estudios Clínicos (REEC), notas informativas y alertas | portal, feed | none | html, rss, pdf | daily | session-required, js-rendered, waf-blocks-bots | 2026-09-30 |
| [isciii-cne](isciii-cne.yaml) | ISCIII – Centro Nacional de Epidemiología (RENAVE, MoMo, SiVIRA, COVID-19) | download, portal | none | csv, pdf, html | weekly | url-drift, static-html | 2026-09-30 |
| [sanidad-nomenclator-facturacion](sanidad-nomenclator-facturacion.yaml) | Ministerio de Sanidad – Nomenclátor de facturación (medicamentos financiados y precios) | download, portal | none | csv, xls, rdf, html | monthly | static-html, overwritten-in-place | 2026-10-01 |
| [sanidad-portal-estadistico](sanidad-portal-estadistico.yaml) | Ministerio de Sanidad – Portal Estadístico del SNS y Catálogo Nacional de Hospitales | portal, download | none | xlsx, pdf, html | annual | tls-chain-incomplete, viewstate-forms, url-drift | 2026-09-30 |

- **aemps-cima-api**: Los 25.487 medicamentos registrados en España (20.464 autorizados): composición, principios activos, ATC, presentaciones con código nacional, estado, ficha técnica y prospecto en PDF, HTML y secciones, problemas de suministro y registro de cambios. JSON sin autenticación y nomenclátor XML diario.
- **aemps-otros-registros**: Registro Español de Estudios Clínicos (11.926 estudios) con buscador y ficha pública por estudio, notas informativas y alertas de seguridad de medicamentos, productos sanitarios y cosméticos con RSS. Sin API documentada ni descarga masiva; el REEC es una aplicación JavaScript con sesión.
- **isciii-cne**: Vigilancia epidemiológica nacional: exceso de mortalidad diario MoMo en CSV (nacional y CCAA por sexo y edad desde 2015), histórico COVID-19 por provincia, sexo y edad en CSV (2020-2023), boletines semanales, informes anuales RENAVE e informes semanales SiVIRA (gripe, COVID-19, VRS) en PDF.
- **sanidad-nomenclator-facturacion**: Los 20.571 productos del nomenclátor de facturación del SNS (17.209 en alta, el resto de baja o suspendidos): código nacional, laboratorio, principio activo, estado, alta y baja, aportación, PVP con IVA, precio de referencia y agrupación homogénea. CSV, Excel y RDF completos y buscador web.
- **sanidad-portal-estadistico**: Catálogo Nacional de Hospitales en xlsx (849 hospitales con código, camas, municipio, dependencia y complejo), consulta interactiva de cubos del SNS (altas RAE-CMBD, SIAP, recursos, gasto), Indicadores Clave del SNS, Barómetro Sanitario y BDCAP. Solo el catálogo tiene descarga directa.
