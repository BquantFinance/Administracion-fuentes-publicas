# Contratación pública y subvenciones

Sector `contratacion-subvenciones` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [bdns-api](bdns-api.yaml) | BDNS – Base de Datos Nacional de Subvenciones (API REST) | api-rest, download, portal | none | json, csv, xlsx | daily | latin1, errors-html-or-xml | 2026-09-30 |
| [hacienda-registro-licitadores](hacienda-registro-licitadores.yaml) | ROLECSP – Registro Oficial de Licitadores y Empresas Clasificadas del Sector Público | portal | certificate | html, xml, pdf | daily | tls-chain-incomplete | 2026-09-30 |
| [placsp-datos-abiertos](placsp-datos-abiertos.yaml) | Plataforma de Contratación del Sector Público – Sindicación ATOM (CODICE) | feed, download | none | atom, xml, zip | realtime | — | 2026-09-30 |

- **bdns-api**: Convocatorias (655000), concesiones, ayudas de Estado, minimis, grandes beneficiarios, sanciones, planes estratégicos y subvenciones a partidos políticos de todas las Administraciones (Estado, CCAA, EELL). API REST JSON paginada sin autenticación y exportación a CSV y xlsx.
- **hacienda-registro-licitadores**: Registro de empresas inscritas para contratar con el sector público y su clasificación. No hay consulta pública abierta: el acceso exige certificado electrónico y AutoFirma. Solo son públicos el visor de certificados ROLECE y DEUC en XML y el generador del DEUC.
- **placsp-datos-abiertos**: Todas las licitaciones, adjudicaciones y contratos menores publicados en la Plataforma (Estado y perfiles alojados) y los agregados de plataformas autonómicas, como feeds ATOM con el documento CODICE (XML basado en UBL) de cada expediente y ZIP mensuales del histórico.
