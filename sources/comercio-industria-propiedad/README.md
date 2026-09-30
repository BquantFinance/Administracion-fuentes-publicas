# Comercio exterior, industria y propiedad industrial

Sector `comercio-industria-propiedad` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [datacomex](datacomex.yaml) | DataComex – Estadísticas de comercio exterior de España (portal y API con token) | api-rest, portal, download | registration | json, csv, xlsx, html | monthly | session-required, js-rendered | 2026-09-30 |
| [datainvex](datainvex.yaml) | DataInvex – Inversiones exteriores directas | portal | none | html, xlsx | quarterly | viewstate-forms, js-rendered | 2026-09-30 |
| [mincotur-industria-turismo](mincotur-industria-turismo.yaml) | Ministerio de Industria y Turismo – Estadísticas industriales, BADASE y DATAESTUR (API) | api-rest, portal, download | api-key | json, xlsx, csv, html | monthly | viewstate-forms, url-drift | 2026-09-30 |
| [oepm-invenes](oepm-invenes.yaml) | OEPM – Patentes, marcas y diseños (INVENES, Localizador, BOPI) | portal, download | none | html, pdf, xml | daily | waf-blocks-bots, waf-intermittent-403, url-drift | — |

- **datacomex**: Exportaciones e importaciones mensuales de Aduanas por producto TARIC, país y provincia. Portal de consulta interactiva con cuadros de mando y API REST JSON (DatacomexAPI) con token obtenido por usuario y contraseña gratuitos; la descarga masiva también exige iniciar sesión.
- **datainvex**: Flujos y stock de inversión extranjera en España y española en el exterior por país, sector y CCAA, a partir del Registro de Inversiones Exteriores. Aplicación ASP.NET de consulta multidimensional (cubos Inversión Extranjera e Inversión Española) sin API ni ficheros de descarga directa.
- **mincotur-industria-turismo**: Estadísticas de industria (coyuntura, vehículos, cemento, pyme) y base de series BADASE en aplicaciones ASP.NET, más DATAESTUR, plataforma de datos turísticos con 124 conjuntos descargables y una API REST (API-SEGITTUR v2, OpenAPI, clave de API) que reúne FRONTUR, EGATUR, afiliación y AENA.
- **oepm-invenes**: Bases de datos de patentes y modelos de utilidad (INVENES), marcas y nombres comerciales (Localizador), Boletín Oficial de la Propiedad Industrial y estadísticas. El cortafuegos de la OEPM rechazó todas las peticiones desde este entorno (403 con support ID), así que ninguna ruta pudo verificarse.
