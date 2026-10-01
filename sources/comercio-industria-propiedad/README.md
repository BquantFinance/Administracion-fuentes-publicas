# Comercio exterior, industria y propiedad industrial

Sector `comercio-industria-propiedad` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Comercio exterior por producto TARIC, país y provincia desde 1995 → `datacomex` (API verificada con cuenta gratuita; códigos de país numéricos, no ISO)
- Inversión extranjera en España y española en el exterior → `datainvex` (aplicación ASP.NET con viewstate; sin API)
- Estadísticas de industria, series BADASE y datos turísticos (DATAESTUR) → `mincotur-industria-turismo` (la API de DATAESTUR respondió sin clave pero con 504 frecuentes; reintentar)
- Patentes, marcas y Boletín de la Propiedad Industrial → `oepm-invenes` (bloqueado por el cortafuegos de la OEPM desde el entorno de verificación)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [datacomex](datacomex.yaml) | DataComex – Estadísticas de comercio exterior de España (portal y API con token) | api-rest, portal, download | registration | json, csv, xlsx, html | monthly | session-required, js-rendered, errors-html-or-xml | 2026-09-30 |
| [datainvex](datainvex.yaml) | DataInvex – Inversiones exteriores directas | portal | none | html, xlsx | quarterly | viewstate-forms, js-rendered, session-required | 2026-10-01 |
| [mincotur-industria-turismo](mincotur-industria-turismo.yaml) | Ministerio de Industria y Turismo – Estadísticas industriales, BADASE y DATAESTUR (API) | api-rest, portal, download | none | xlsx, csv, json, pdf, html | monthly | viewstate-forms, url-drift, overwritten-in-place | 2026-10-01 |
| [oepm-invenes](oepm-invenes.yaml) | OEPM – Patentes, marcas y diseños (INVENES, Localizador, BOPI) | portal, download | none | html, pdf, xml | daily | waf-blocks-bots, waf-intermittent-403, url-drift | — |

- **datacomex**: Exportaciones e importaciones de Aduanas por producto TARIC (2 a 8 dígitos), país y provincia, mensuales y anuales desde 1995, en JSON por API con token gratuito (usuario y contraseña) y en el portal de consulta con cuadros de mando. Definitivos hasta 2023 y provisionales después.
- **datainvex**: Flujos y stock de inversión extranjera en España y española en el exterior por país, sector y CCAA, del Registro de Inversiones Exteriores. Aplicación ASP.NET multidimensional (cubos Inversión Extranjera e Inversión Española); sin API ni descarga directa localizadas; el informe HTML sale por script.
- **mincotur-industria-turismo**: Estadísticas de industria (coyuntura, vehículos, cemento, pyme), cuadro resumen del ministerio y base de series BADASE (ASP.NET), más DATAESTUR, plataforma de datos turísticos con una API REST (API-SEGITTUR v2, OpenAPI, 124 conjuntos en xlsx o csv) que reúne FRONTUR, EGATUR, afiliación y AENA.
- **oepm-invenes**: Bases de datos de patentes y modelos de utilidad (INVENES), marcas y nombres comerciales (Localizador), Boletín Oficial de la Propiedad Industrial y estadísticas. El cortafuegos F5 de la OEPM rechazó desde este entorno todo salvo el índice del Localizador (403 con support ID); sin datos verificados.
