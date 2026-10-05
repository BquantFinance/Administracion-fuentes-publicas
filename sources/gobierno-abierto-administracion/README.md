# Gobierno abierto, transparencia y organización administrativa

Sector `gobierno-abierto-administracion` · 12 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Catálogo de datasets abiertos de todas las Administraciones → `datos-gob-es-api` (solo metadatos; el fichero vive en el portal del publicador)
- Códigos DIR3 de unidades, entidades y oficinas → `dir3-directorio` (la API relations de face-facturas da DIR3 y NIF sin WAF)
- NIF y relaciones de facturación de un organismo público → `face-facturas`
- Boletín de empleo público y códigos SIA de procedimientos → `pag-administracion-gob-es`
- Altos cargos, retribuciones, agendas y estadísticas de derecho de acceso → `transparencia-portal` (retribuciones, contratos y convenios se exportan a xlsx en servicios-buscador (2000 filas como máximo); subvenciones en bdns-api)
- Datos abiertos de la Comunidad de Madrid (calidad del aire, padrón, centros, registros) por API → `comunidad-madrid-datos-abiertos` (CKAN; el datastore puede tener menos filas que el CSV (5000 de 18718 en el padrón); descargar el recurso)
- Padrón de la ciudad de Madrid por distrito, barrio, sección censal y edad → `ayuntamiento-madrid-datos-abiertos` (CSV mensual del conjunto 200076-0-padron; la API dinámica se quedó en 2023)
- Calidad del aire y tráfico en tiempo real de la ciudad de Madrid → `ayuntamiento-madrid-datos-abiertos` (calair_tiemporeal e informo pm.xml; las horas aún no medidas llegan como 0 con validación N)
- Accidentes de tráfico de la ciudad de Madrid → `ayuntamiento-madrid-datos-abiertos` (un CSV por año en 300228-0; una fila por persona, agrupar por num_expediente)
- GTFS del Consorcio de Transportes de Madrid → `comunidad-madrid-datos-abiertos` (el conjunto enlaza a ArcGIS; el ZIP sale de /sharing/rest/content/items/{id}/data)
- Registro de entidades, contratación o subvenciones (RAISC) de la Generalitat de Catalunya → `gencat-dades-obertes` (Socrata; sin $limit corta a 1000 filas; buscar en catalán; el RAISC trae codi_bdns)
- Población de Barcelona por barrio o sección censal del último año → `ayuntamiento-barcelona-datos-abiertos` (padrón municipal, no cifra oficial; el Idescat por sección acaba en 2022; solo el datastore es automatizable)
- Disposiciones del BOJA por fecha con sumario y PDF → `junta-andalucia-datos-abiertos` (API v0 aparte del CKAN; ordenar por dateUTC y trocear por día)
- Datos abiertos de la Junta de Andalucía y filas de sus CSV por API → `junta-andalucia-datos-abiertos` (cambiar el host interno de los recursos subidos por www.juntadeandalucia.es)
- Datos abiertos de la Generalitat Valenciana (contratos, ERTE, turismo, cultura) por API → `gva-dadesobertes-api` (CKAN con datastore; el órgano real va en origen_datos, no en organization)
- Contratos adjudicados por la Generalitat Valenciana, incluidos los menores → `gva-dadesobertes-api` (un conjunto por año (eco-gvo-contratos-AAAA); importes con coma decimal; URL_LICITACION enlaza con PLACSP)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [ayuntamiento-barcelona-datos-abiertos](ayuntamiento-barcelona-datos-abiertos.yaml) | Ayuntamiento de Barcelona – Open Data BCN (API CKAN y DataStore) | api-rest, download | none | json, csv, xml, geojson, gpkg, shp, zip | daily | captcha-required, datastore-incomplete | 2026-10-01 |
| [ayuntamiento-madrid-datos-abiertos](ayuntamiento-madrid-datos-abiertos.yaml) | Ayuntamiento de Madrid – Portal de datos abiertos (API CKAN y API dinámica) | api-rest, download, feed | none | json, csv, xml, xlsx, xls, zip, txt, kml, shp, ttl, atom | realtime | waf-intermittent-403, url-drift, overwritten-in-place, waf-temporary-ban | 2026-10-01 |
| [comunidad-madrid-datos-abiertos](comunidad-madrid-datos-abiertos.yaml) | Comunidad de Madrid – Catálogo de datos abiertos (API CKAN) | api-rest, download | none | json, csv, zip, ttl, rdf | daily | latin1, overwritten-in-place, datastore-incomplete | 2026-10-05 |
| [datos-gob-es-api](datos-gob-es-api.yaml) | datos.gob.es – Catálogo nacional de datos abiertos (API) | api-rest, sparql, portal | none | json, xml, csv, rdf | daily | waf-intermittent-403, errors-html-or-xml, static-html | 2026-09-30 |
| [dir3-directorio](dir3-directorio.yaml) | DIR3 – Directorio Común de Unidades Orgánicas y Oficinas | download, portal | none | xlsx, pdf | irregular | session-required, user-agent-browser, static-html | 2026-10-01 |
| [face-facturas](face-facturas.yaml) | FACe – Facturas electrónicas al sector público y directorio DIR3 | api-rest, api-soap, download | none | json, csv, xml | realtime | user-agent-browser | 2026-10-01 |
| [gencat-dades-obertes](gencat-dades-obertes.yaml) | Generalitat de Catalunya – Dades obertes (API Socrata SODA) | api-rest, download | none | json, csv, geojson | daily | — | 2026-10-01 |
| [gva-dadesobertes-api](gva-dadesobertes-api.yaml) | GVA – Portal de datos abiertos de la Generalitat Valenciana (API CKAN) | api-rest, download | none | json, csv, rdf, ttl, jsonld | daily | overwritten-in-place, datastore-incomplete, connection-reset-intermittent | 2026-10-01 |
| [jcyl-datos-abiertos](jcyl-datos-abiertos.yaml) | Junta de Castilla y León – Portal de datos abiertos | download, portal | none | csv, xls, json, xml, shp, kml, rdf | daily | static-html, latin1 | 2026-10-05 |
| [junta-andalucia-datos-abiertos](junta-andalucia-datos-abiertos.yaml) | Junta de Andalucía – Portal de datos abiertos (API CKAN y API v0 con BOJA) | api-rest, download | none | json, csv, xls, xlsx, ods, kml, rdf, txt | daily | latin1, datastore-incomplete | 2026-10-01 |
| [pag-administracion-gob-es](pag-administracion-gob-es.yaml) | Punto de Acceso General – Trámites, SIA, empleo público y ayudas | portal, download | none | html, pdf, xlsx | weekly | static-html, url-drift, user-agent-browser, session-required | 2026-10-01 |
| [transparencia-portal](transparencia-portal.yaml) | Portal de la Transparencia de la AGE | portal, download | none | html, xlsx, ods, zip, pdf | monthly | static-html, url-drift | 2026-10-01 |

- **ayuntamiento-barcelona-datos-abiertos**: 555 datasets del Ayuntamiento de Barcelona (padrón por sección censal desde 1997, accidentes de la Guardia Urbana, movilidad, vivienda, IBI, subvenciones, presupuesto) sobre CKAN 2.6. La API de acciones y el DataStore (búsqueda y SQL) responden sin clave; las descargas pasan por un reto anti-bot.
- **ayuntamiento-madrid-datos-abiertos**: 673 conjuntos del Ayuntamiento en CKAN 2.9.11: padrón mensual por sección y edad, accidentes, censo de locales, presupuestos, calidad del aire y tráfico en tiempo real. API JSON, datastore con filtros, DCAT, feed Atom y una API dinámica con filtros por campo en ciudadesabiertas.madrid.es.
- **comunidad-madrid-datos-abiertos**: CKAN 2.9 con 177 conjuntos de las consejerías (calidad del aire diaria, polen, centros educativos, farmacias, registros, GTFS del Consorcio, elecciones autonómicas) y 2086 tablas del Instituto de Estadística (bancos Almudena municipal, Baco y Desvan). API JSON, datastore y DCAT sin clave.
- **datos-gob-es-api**: Catálogo federado de los datasets abiertos de todas las Administraciones (Estado, CCAA, EELL, universidades) con metadatos DCAT-AP, distribuciones con URL de descarga y publicador identificado por código DIR3. API REST JSON paginada; el endpoint SPARQL no respondió desde este entorno.
- **dir3-directorio**: Inventario oficial de unidades orgánicas, entidades y oficinas de todas las Administraciones con código DIR3, jerarquía, NIF y estado. Descarga pública en xlsx por nivel (foto periódica, no diaria) más catálogos auxiliares; es la clave de FACe, PLACSP, BDNS y datos.gob.es.
- **face-facturas**: Punto general de entrada de facturas electrónicas: API pública JSON y CSV con las 50000 relaciones oficina contable, órgano gestor y unidad tramitadora (DIR3 y NIF) de las Administraciones adheridas, y servicios SOAP con certificado para presentar y consultar facturas.
- **gencat-dades-obertes**: Unos 1.100 datasets de la Generalitat en Socrata (registro de entidades, contratación pública, subvenciones RAISC, alojamientos turísticos, meteorología XEMA, embalses, normativa del DOGC). API SODA con consultas SoQL en servidor, salida JSON, CSV y GeoJSON y exportación completa, sin clave.
- **gva-dadesobertes-api**: Catálogo CKAN de la Generalitat Valenciana (1310 conjuntos de la GVA, el Institut Cartogràfic Valencià y la Universidad de Alicante): contratos, ERTE, turismo, cultura, cartografía. API JSON con datastore para consultar filas de los CSV, volcado CSV y DCAT-AP, sin autenticación.
- **jcyl-datos-abiertos**: Catálogo de datos abiertos de la Junta de Castilla y León: 840 conjuntos descargables por URL directa (.csv, .xls, .json) y CSV del catálogo completo regenerado a diario. Sin API; la estadística autonómica (SIE, app SAS) tampoco.
- **junta-andalucia-datos-abiertos**: Catálogo CKAN 2.10 de la Junta de Andalucía (832 conjuntos de 72 organismos, 260 del IECA): presupuestos, tesorería, educación, medio ambiente, cultura. API JSON con datastore en 173 recursos y una API v0 aparte con OpenAPI (BOJA desde 1979, RPT, agenda, subvenciones), sin autenticación.
- **pag-administracion-gob-es**: Portal ciudadano de la AGE: boletín semanal de empleo público y quincenal de ayudas y becas en PDF, buscadores de trámites, empleo, becas y oficinas y directorio de sedes electrónicas, sin API localizada. Los códigos SIA de procedimientos se descargan en xlsx por nivel desde el área pública del CTT.
- **transparencia-portal**: Publicidad activa de la AGE: buscador con exportación a xlsx de contratos (835607, menores incluidos), convenios, retribuciones y actividad privada de altos cargos, filtrable por DIR3, y estadísticas del derecho de acceso y resoluciones denegatorias en xlsx y ods. Sin API localizada.
