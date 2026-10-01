# Hacienda, tributos y presupuestos

Sector `hacienda-presupuestos` · 6 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Renta y declarantes de IRPF por municipio, código postal o tramo → `aeat-estadisticas`
- Recaudación tributaria mensual por figura → `aeat-estadisticas`
- Suministro Inmediato de Información, VERI*FACTU y presentación de modelos → `aeat-servicios-web` (SOAP con certificado electrónico)
- Presupuestos, liquidaciones y deuda viva de ayuntamientos y diputaciones → `hacienda-ovef` (CONPREL da presupuestos y liquidaciones por entidad desde 2002 con descarga directa (DescargaFichero))
- Presupuestos de las comunidades autónomas → `hacienda-ovef` (SGCIEF/PublicacionPresupuestos; xlsx tras un GET y un POST con __VIEWSTATE, sin navegador)
- Tipos de IBI, IAE e IVTM por municipio → `hacienda-ovef` (consulta web con sesión (SGFAL))
- Déficit de las Administraciones Públicas y ejecución del presupuesto del Estado → `igae-ejecucion-presupuestaria`
- Inventario de entes del sector público (INVENTE) → `igae-ejecucion-presupuestaria`
- Presupuestos Generales del Estado por capítulos, políticas y programas (aprobados o proyecto) → `sepg-presupuestos-generales-estado` (presupuesto, no ejecución; la ejecución está en igae-ejecucion-presupuestaria)
- Periodo medio de pago a proveedores de todas las AAPP y financiación extraordinaria de las CCAA (FLA) → `hacienda-central-informacion`
- Calendario de publicación de las estadísticas de Hacienda, IGAE y AEAT → `hacienda-central-informacion`

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aeat-estadisticas](aeat-estadisticas.yaml) | AEAT – Estadísticas tributarias y descarga masiva | download, portal | none | csv, xlsx, html, pdf | monthly | static-html, overwritten-in-place, url-drift | 2026-10-01 |
| [aeat-servicios-web](aeat-servicios-web.yaml) | AEAT – Servicios web SII y VERI*FACTU | api-soap | certificate | xml | realtime | tls-chain-incomplete | 2026-10-01 |
| [hacienda-central-informacion](hacienda-central-informacion.yaml) | Hacienda – Central de Información (calendario, periodo medio de pago, financiación CCAA) | download, portal | none | xlsx, xls, html, pdf | monthly | static-html, overwritten-in-place, soft-errors-200 | 2026-10-01 |
| [hacienda-ovef](hacienda-ovef.yaml) | Hacienda – Entidades locales, presupuestos, deuda viva, financiación y tributos | download, portal | none | xlsx, xls, zip, pdf | monthly | static-html, session-required, viewstate-forms, url-drift | 2026-10-01 |
| [igae-ejecucion-presupuestaria](igae-ejecucion-presupuestaria.yaml) | IGAE – Ejecución presupuestaria y contabilidad nacional | download, api-rest, portal | none | xlsx, xls, pdf, html, json | monthly | static-html, user-agent-browser, overwritten-in-place, soft-errors-200 | 2026-10-01 |
| [sepg-presupuestos-generales-estado](sepg-presupuestos-generales-estado.yaml) | Secretaría de Estado de Presupuestos y Gastos – Presupuestos Generales del Estado en xlsx | download | none | xlsx, pdf | annual | static-html, user-agent-browser | 2026-10-01 |

- **aeat-estadisticas**: Estadísticas de declarantes de IRPF (nacional, por municipio y por código postal), IVA, Sociedades y Patrimonio, recaudación mensual y anual, ventas, empleo y salarios en fuentes tributarias y comercio exterior. CSV masivos del anuario, series de recaudación en xlsx y CSV de comercio exterior.
- **aeat-servicios-web**: Servicios web SOAP con certificado electrónico para el Suministro Inmediato de Información del IVA (SII), los sistemas de facturación VERI*FACTU y la presentación de modelos. WSDL y XSD públicos, entorno de pruebas con host propio y portal de desarrolladores separado de la sede.
- **hacienda-central-informacion**: Portal de publicaciones económico-financieras de Hacienda e IGAE con catálogo de informes y ficheros de URL estable: calendario de publicaciones, periodo medio de pago a proveedores de las AAPP (mensual desde 2014, series e informes de CCAA y EELL) y mecanismos de financiación de CCAA desde 2012.
- **hacienda-ovef**: Entidades locales: deuda viva por ayuntamiento, entregas a cuenta mensuales, ejecución trimestral, estabilidad, presupuestos y liquidaciones por entidad desde 2002 (CONPREL), periodo medio de pago y tipos impositivos municipales. Ficheros xlsx, xls y Access por año, trimestre o mes.
- **igae-ejecucion-presupuestaria**: Déficit y operaciones no financieras de las AAPP en contabilidad nacional (mensual por subsector y CCAA, series trimestrales y anuales desde 1995), ejecución mensual del presupuesto del Estado en caja, cuentas anuales de las AAPP e inventario de entes públicos (INVENTE) con API REST en JSON.
- **sepg-presupuestos-generales-estado**: Estadísticas de los Presupuestos Generales del Estado por ejercicio (2014 a 2025, proyectos con sufijo P): cinco libros xlsx por año (consolidados, Estado, Seguridad Social, organismos autónomos, resto de entes) con los cuadros de ingresos y gastos por capítulos, políticas y programas, más su PDF.
