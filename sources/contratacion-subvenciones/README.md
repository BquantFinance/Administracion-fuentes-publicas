# Contratación pública y subvenciones

Sector `contratacion-subvenciones` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | verificada |
|---|---|---|---|---|---|---|
| [bdns-api](bdns-api.yaml) | BDNS – Base de Datos Nacional de Subvenciones (API REST) | api-rest, portal, download | none | json, csv, xlsx, pdf | daily | — |
| [hacienda-registro-licitadores](hacienda-registro-licitadores.yaml) | ROLECE – Registro Oficial de Licitadores y Empresas Clasificadas | portal | none | html, pdf | daily | — |
| [placsp-datos-abiertos](placsp-datos-abiertos.yaml) | Plataforma de Contratación del Sector Público – Datos abiertos (ATOM/CODICE) | feed, download | none | atom, xml, zip | realtime | — |

- **bdns-api**: Convocatorias, concesiones y beneficiarios de subvenciones de todas las Administraciones (Estado, CCAA, EELL), ayudas de Estado, minimis, sanciones e inhabilitaciones. API REST pública con paginación y descarga CSV.
- **hacienda-registro-licitadores**: Registro de empresas inscritas para contratar con el sector público, con clasificación de contratistas de obras y servicios por grupos y categorías. Consulta pública por NIF o denominación.
- **placsp-datos-abiertos**: Todas las licitaciones y adjudicaciones publicadas en la Plataforma (Estado, y CCAA y EELL que agregan): feeds ATOM con documentos CODICE (XML basado en UBL) por licitación, más ZIP mensuales históricos.
