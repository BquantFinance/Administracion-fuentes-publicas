# Contratación pública y subvenciones

Sector `contratacion-subvenciones` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Licitaciones, adjudicaciones y contratos menores de todas las Administraciones → `placsp-datos-abiertos`
- Contratos adjudicados a una empresa por su NIF, o quién gana los contratos de un órgano → `placsp-datos-abiertos` (sin búsqueda por NIF en la plataforma; almacén local con la tabla placsp_adjudicaciones (guides/almacen.md, herramienta almacen_sql))
- Todo lo público de una empresa o entidad por su NIF (ayudas, si es sector público, prohibiciones de contratar) → `bdns-api` (herramienta empresa_nif del MCP o consulta.empresa_nif (BDNS, AEI, Invente y prohibiciones por denominación); contratos y BORME salen solo del almacén local (guides/almacen.md))
- Convocatorias y concesiones de subvenciones, ayudas de Estado, minimis, grandes beneficiarios → `bdns-api`
- Empresas clasificadas para contratar (ROLECE) → `hacienda-registro-licitadores` (solo con certificado electrónico)
- Prohibiciones de contratar vigentes → `hacienda-registro-licitadores` (XML público del visor del ROLECE; el NIF va oculto, cruzar por nombre)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [bdns-api](bdns-api.yaml) | BDNS – Base de Datos Nacional de Subvenciones (API REST) | api-rest, download, portal | none | json, csv, xlsx | daily | latin1, errors-html-or-xml | 2026-10-01 |
| [hacienda-registro-licitadores](hacienda-registro-licitadores.yaml) | ROLECSP – Registro Oficial de Licitadores y Empresas Clasificadas del Sector Público | portal, download | certificate | html, xml, pdf, zip | daily | tls-chain-incomplete, latin1, overwritten-in-place, url-drift | 2026-10-01 |
| [placsp-datos-abiertos](placsp-datos-abiertos.yaml) | Plataforma de Contratación del Sector Público – Sindicación ATOM (CODICE) | feed, download | none | atom, xml, zip, xlsx | daily | soft-errors-200, waf-temporary-ban | 2026-10-01 |

- **bdns-api**: Convocatorias (655000), concesiones, ayudas de Estado, minimis, grandes beneficiarios, sanciones, planes estratégicos y subvenciones a partidos políticos de todas las Administraciones (Estado, CCAA, EELL). API REST JSON paginada sin autenticación y exportación a CSV y xlsx.
- **hacienda-registro-licitadores**: Registro de empresas inscritas para contratar con el sector público y su clasificación. La consulta por empresa exige certificado; sin él solo hay el XML de prohibiciones de contratar vigentes, los esquemas XSD del certificado, el visor de certificados ROLECE y DEUC y el generador del DEUC.
- **placsp-datos-abiertos**: Todas las licitaciones, adjudicaciones y contratos menores publicados en la Plataforma (Estado y perfiles alojados) y los agregados de plataformas autonómicas, como feeds ATOM diarios con el documento CODICE (XML basado en UBL) de cada expediente, y ZIP anuales y mensuales del histórico.
