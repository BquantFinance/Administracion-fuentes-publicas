# Respuestas de muestra

Respuestas reales capturadas el 2026-10-01 y recortadas (listas acortadas, texto de documentos reducido a unos párrafos)
para probar los parsers de `scripts/clientes/` sin red: `python scripts/test_clientes.py`. No llevan claves. Los nombres
de personas físicas (beneficiarios de la BDNS, administradores del BORME) están sustituidos por marcadores con el mismo
formato. Codificación original: el CSV de la BDNS va en windows-1252 y el de la Comunidad de Madrid en Latin-1, como los
sirven los servidores; los de PC-Axis en UTF-8 con BOM.

| fichero | llamada de origen |
|---|---|
| boe-sumario-20260930.json | boe/sumario/20260930 (dos números el mismo día; secciones 1, 3, 5A y 5C) |
| boe-sumario-20240102.json | boe/sumario/20240102 (secciones 2A, 4 y 5B) |
| boe-error-404.xml | boe/sumario/20260927 (domingo) |
| boe-documento-BOE-A-2026-20264.xml | diario_boe/xml.php?id=BOE-A-2026-20264 |
| boe-documento-error.xml | diario_boe/xml.php?id=BOE-A-2026-999999 (HTTP 200) |
| boe-lc-normas.json | legislacion-consolidada?from=20260929&to=20260930&limit=3 |
| boe-lc-vacio.json | legislacion-consolidada?from=20260927&to=20260927 |
| boe-lc-metadatos.json | legislacion-consolidada/id/BOE-A-1978-31229/metadatos |
| boe-lc-indice.json | legislacion-consolidada/id/BOE-A-1978-31229/texto/indice |
| boe-lc-bloque-a135.xml | legislacion-consolidada/id/BOE-A-1978-31229/texto/bloque/a135 |
| borme-sumario-20260930.json | borme/sumario/20260930 |
| borme-A-2026-189-28.xml | diario_borme/xml.php?id=BORME-A-2026-189-28 (6 empresas) |
| bdns-convocatorias-busqueda.json | convocatorias/busqueda con fechas del 29 y 30/09/2026 |
| bdns-convocatoria-800000.json | convocatorias?numConv=800000 |
| bdns-concesiones-busqueda.json | concesiones/busqueda del 29/09/2026 (empresa y personas físicas) |
| bdns-ayudasestado-busqueda.json | ayudasestado/busqueda?nifCif=A02066116 |
| bdns-concesiones-exportar.csv | concesiones/exportar?vpd=GE&tipoDoc=csv del 29/09/2026 |
| bdns-error-400.json | convocatorias/busqueda?fechaDesde=2026-09-01 (fecha ISO) |
| bdns-error-404.html | noexiste/busqueda |
| aemet-error-401.json | prediccion/especifica/municipio/diaria/16078 con una clave inválida |
| ine-valores-variable-19-22.json | VALORES_VARIABLEOPERACION/19/22 (cuatro municipios) |
| ine-datos-tabla-29005.json | DATOS_TABLA/29005?nult=2&tip=AM&tv=19:6124 |
| ine-error-volumen.json | DATOS_TABLA/30824?nult=1&tip=AM (sin filtros) |
| datacomex-paises.json | ObtenerPaises |
| datacomex-error-401.json | ObtenerDatos sin token, con Accept application/json |
| saiku-flattened.json | query/q1/result/flattened del cubo 040 Servicio 016 |
| placsp-feed-643.atom | página vigente del feed 643 (dos entradas y una anulación) |
| placsp-sin-dir3-y-prorroga.atom | dos entradas del 643 del 2026-10-05: órgano sin DIR3 (NIF e ID_PLATAFORMA) y contrato con prórroga (ContractModification) |
| ckan-cnmc-datastore-tope.json | datastore_search de la CNMC con limit=50000 (llegan 32.000; tres filas guardadas) |
| ckan-error-404.json | package_show?id=no-existe-xyz en la Comunidad de Madrid |
| ckan-renfe-fl-409.json | package_search?fl=name,title en Renfe (Validation Error) |
| ckan-andalucia-package-show.json | package_show de plantillas-organicas-de-centros-docentes-publicos (url con host interno) |
| ckan-comunidad-madrid-padron.csv | CSV del padrón por sexo de la Comunidad de Madrid (Latin-1, cuatro líneas) |
| socrata-gn9e-3qhr.json | resource/gn9e-3qhr.json?$limit=3 con sus cabeceras x-soda2-fields y x-soda2-types |
| socrata-error-404.json | resource/zzzz-zzzz.json |
| pcaxis-ine-24077.csv | jaxiT3 csv_bdsc de la tabla 24077 (BOM, periodo sin dato como "") |
| pcaxis-cultura-T1FM1001.csv | CulturaJaxiPx csv_bdsc de T1FM1001 |
| arcgis-cobertura-28079.json | cobertura FTTH 2025 de Madrid (FeatureServer, fecha en milisegundos) |
| arcgis-igme-capa.json | descripción de la capa del catálogo sísmico del IGME (objectIdField null, sin paginación) |
| arcgis-igme-sin-paginacion.json | query con resultOffset en esa capa (error con HTTP 200) |
| ogc-sigpac-recintos-tope.json | recintos SIGPAC con limit=1000 (llegan 250; dos features guardadas) |
| sepe-paro-municipios-2026.csv | CSV de datos abiertos del SEPE, título y cabecera más julio y agosto de siete municipios (windows-1252, «<5», códigos de antes de las fusiones) |
| ine-datos-serie-IPC290750.json | DATOS_SERIE del IPC general, variación anual, nult=2 y tip=AM: 2026M08 definitivo y 2026M09 avance |

Faltan, porque necesitan credenciales: el fichero de datos de AEMET (ISO-8859-15) y ObtenerDatos de DataComex.
| bdns-terceros-universidad-de-cadiz.json | terceros?ambito=C&busqueda=universidad de cadiz del 2026-10-05: directorio NIF y nombre con variantes |
