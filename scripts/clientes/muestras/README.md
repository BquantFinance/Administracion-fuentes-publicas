# Respuestas de muestra

Respuestas reales capturadas el 2026-10-01 y recortadas (listas acortadas, texto de documentos reducido a unos párrafos)
para probar los parsers de `scripts/clientes/` sin red: `python scripts/test_clientes.py`. No llevan claves. Los nombres
de personas físicas (beneficiarios de la BDNS, administradores del BORME) están sustituidos por marcadores con el mismo
formato. Codificación original: el CSV de la BDNS va en windows-1252, como lo sirve la API.

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

Faltan, porque necesitan credenciales: el fichero de datos de AEMET (ISO-8859-15) y ObtenerDatos de DataComex.
