# Hacienda, tributos y presupuestos

Sector `hacienda-presupuestos` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | verificada |
|---|---|---|---|---|---|---|
| [aeat-estadisticas](aeat-estadisticas.yaml) | AEAT – Estadísticas tributarias | portal, download | none | html, xlsx, csv, pdf | monthly | — |
| [aeat-servicios-web](aeat-servicios-web.yaml) | AEAT – Servicios web y trámites automatizables | api-soap | certificate | xml | realtime | — |
| [hacienda-ovef](hacienda-ovef.yaml) | Hacienda – Oficina Virtual de Coordinación Financiera con las EELL y CCAA | portal, download | none | xlsx, csv, pdf | annual | — |
| [igae-ejecucion-presupuestaria](igae-ejecucion-presupuestaria.yaml) | IGAE – Ejecución presupuestaria y contabilidad nacional | portal, download | none | xlsx, pdf, html, csv | monthly | — |

- **aeat-estadisticas**: Estadísticas de declarantes de IRPF, IVA, Sociedades y Patrimonio por tramos, provincia y municipio; informes mensuales de recaudación; ventas, empleo y salarios en fuentes tributarias; comercio exterior.
- **aeat-servicios-web**: Servicios web SOAP para presentar declaraciones, el Suministro Inmediato de Información del IVA (SII), VERI*FACTU, consulta y validación de NIF, y descarga de datos fiscales. Requieren certificado electrónico.
- **hacienda-ovef**: Presupuestos y liquidaciones de todas las entidades locales y CCAA, deuda viva por ayuntamiento, periodo medio de pago, tributos locales (tipos impositivos por municipio), financiación autonómica. Descargas masivas en Excel/CSV.
- **igae-ejecucion-presupuestaria**: Ejecución mensual del presupuesto del Estado y de la Seguridad Social, déficit por Administraciones en contabilidad nacional, Cuenta General del Estado, datos de entidades públicas (INVENTE) y CIMCA de entes locales.
