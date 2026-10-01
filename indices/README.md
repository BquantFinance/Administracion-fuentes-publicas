# Índices para agentes

Generado por `scripts/build.py` a partir de `indices/*.yaml`, no editar. 43 recetas, 151 necesidades, 21 identificadores, 23 grupos de códigos, 99 rutas muertas.

## Recetas por intención

Procedimientos verificados que encadenan fichas. `python scripts/check_recetas.py` ejecuta las comprobaciones de cada receta contra los servidores reales (batería de regresión).

| receta | intención | fichas | verificada |
|---|---|---|---|
| `ipc-ultimo-dato` | Último IPC general nacional con variación mensual y anual | ine-api-tempus | 2026-09-30 |
| `localizar-tabla-ine` | Encontrar y descargar una tabla del INE por operación (EPA, padrón, PIB, natalidad) sin conocer su id | ine-api-tempus | 2026-09-30 |
| `municipio-a-codigo-ine` | Código INE de un municipio a partir de su nombre, o la relación completa de municipios | cnig-centro-descargas, ine-codigos-territoriales, catastro-ovc | 2026-09-30 |
| `coordenadas-a-referencia-catastral` | De unas coordenadas a la parcela (recinto SIGPAC y referencia catastral) y a los datos del inmueble | mapa-sigpac, catastro-ovc | 2026-10-01 |
| `parcela-a-red-natura-y-nitratos` | Saber si un recinto agrícola está en Red Natura 2000 o en zona vulnerable a nitratos | mapa-sigpac | 2026-10-01 |
| `empresa-nif-a-ayudas-y-contratos` | Subvenciones, ayudas de investigación y contratos públicos de una empresa o entidad por su NIF | bdns-api, aei-convocatorias, placsp-datos-abiertos, borme-api-sumario | 2026-10-01 |
| `organismo-a-dir3-y-nif` | Código DIR3 y NIF de un organismo público a partir de su nombre, y su jerarquía | face-facturas, dir3-directorio, datos-gob-es-api | 2026-09-30 |
| `boe-sumario-y-texto-consolidado` | Qué se publicó en el BOE un día y cómo pasar de una disposición a su texto y a la norma consolidada | boe-api-sumario, boe-api-legislacion-consolidada, boe-eli | 2026-09-30 |
| `buscar-norma-por-titulo` | Encontrar normas por palabras del título, rango o fecha y seguir sus cambios | boe-api-legislacion-consolidada, boe-feeds | 2026-09-30 |
| `licitaciones-nuevas` | Licitaciones y adjudicaciones publicadas hoy en toda la contratación pública | placsp-datos-abiertos, boe-feeds | 2026-09-30 |
| `subvenciones-convocatorias-recientes` | Convocatorias de subvenciones publicadas en un rango de fechas y su detalle | bdns-api | 2026-09-30 |
| `deuda-publica-por-administracion` | Deuda de un ayuntamiento, de una comunidad autónoma o del Estado | hacienda-ovef, bde-estadisticas, tesoro-estadisticas, airef-datos | 2026-10-01 |
| `irpf-por-municipio` | Renta y declarantes de IRPF por municipio y tramo, todos los ejercicios | aeat-estadisticas | 2026-09-30 |
| `paro-registrado-por-municipio` | Paro registrado y demandantes por municipio, sexo, edad y actividad de un mes | sepe-estadisticas, ine-codigos-territoriales | 2026-10-01 |
| `afiliacion-y-pensiones` | Afiliados a la Seguridad Social por régimen, provincia, CNAE o municipio, y pensiones del mes | segsocial-estadisticas | 2026-10-01 |
| `precio-carburantes-municipio` | Precios de hoy de las gasolineras de un municipio o provincia, y el histórico de un día | minetur-precios-carburantes | 2026-09-30 |
| `incidencias-trafico-tiempo-real` | Incidencias, obras, cortes y velocidades de la red de carreteras en este momento | dgt-datex-trafico | 2026-09-30 |
| `matriculaciones-diarias` | Vehículos matriculados o dados de baja cada día, con marca, modelo y municipio | dgt-estadisticas | 2026-10-01 |
| `calidad-aire-estacion` | Serie horaria o diaria de un contaminante en una estación de calidad del aire | miteco-calidad-aire | 2026-09-30 |
| `embalses-y-caudales` | Reserva de agua de un embalse y caudal diario de un río en una estación de aforo | miteco-saih-boletin-hidrologico | 2026-10-01 |
| `capa-red-natura-2000` | Descargar la capa oficial de Red Natura 2000 u otra capa de biodiversidad | miteco-banco-datos-naturaleza, mapa-sigpac | 2026-09-30 |
| `prediccion-meteo-municipio` | Predicción diaria u horaria de un municipio y observación de la estación más cercana | aemet-opendata | 2026-09-30 |
| `medicamento-por-cn-o-nombre` | Datos de un medicamento por código nacional, nombre o principio activo, con ficha técnica y problemas de suministro | aemps-cima-api | 2026-09-30 |
| `exceso-mortalidad-momo` | Defunciones observadas y esperadas por día, ámbito, sexo y edad (MoMo) | isciii-cne | 2026-10-01 |
| `cosecha-oai-publicaciones` | Cosechar publicaciones científicas o patrimonio digital de forma incremental | csic-digital, bne-datos, fecyt-recolecta | 2026-09-30 |
| `tabla-pcaxis-a-csv` | Descargar como CSV una tabla de cualquier portal PC-Axis (INE, EDUCAbase, criminalidad, CULTURAbase) sin navegador | ine-api-tempus, educacion-estadisticas-ruct, interior-criminalidad, cultura-culturabase | 2026-10-01 |
| `ocurrencias-especie-espana` | Registros de presencia de una especie en España, con recuento y descarga | gbif-es | 2026-10-01 |
| `geologia-y-aguas-subterraneas-punto` | Unidad geológica en un punto y puntos de agua subterránea de una provincia | igme-geologia | 2026-10-01 |
| `buscar-dataset-datos-gob-es` | Localizar un dataset abierto de cualquier Administración y su URL de descarga real | datos-gob-es-api | 2026-09-30 |
| `series-banco-de-espana` | Último dato o serie completa de un indicador del Banco de España (euríbor, tipos, crédito, deuda) | bde-estadisticas | 2026-09-30 |
| `flota-pesquera` | Buques de la flota pesquera por puerto base, caladero y modalidad, y capturas por especie | mapa-pesca | 2026-09-30 |
| `criminalidad-municipio` | Infracciones penales por tipología y trimestre en una comunidad, provincia o municipio de más de 20.000 habitantes | interior-criminalidad | 2026-10-01 |
| `actos-mercantiles-borme` | Constituciones, nombramientos, ceses y disoluciones de sociedades publicados en el BORME | borme-api-sumario, boe-feeds | 2026-09-30 |
| `hospitales-catalogo` | Listado de hospitales con camas, dependencia, complejo y municipio | sanidad-portal-estadistico | 2026-10-01 |
| `dataset-cnmc-a-csv` | Descargar un dataset de la CNMC (energía, telecomunicaciones, postal) como CSV o consultarlo por API | cnmc-data | 2026-09-30 |
| `convenio-colectivo-regcon` | Consultar un convenio colectivo por código, denominación o CNAE en REGCON | mites-estadisticas | 2026-10-01 |
| `deficit-y-ejecucion-presupuestaria` | Déficit mensual de las Administraciones Públicas y ejecución del presupuesto del Estado | igae-ejecucion-presupuestaria, hacienda-ovef | 2026-10-01 |
| `precio-electricidad-horario` | Precio de la electricidad por hora o cuarto de hora (mercado diario, PVPC y spot) y demanda del día | omie-mercado, ree-redata | 2026-09-30 |
| `medicamento-precio-financiado` | Precio de venta, precio de referencia y aportación de un medicamento financiado, con su ficha técnica | sanidad-nomenclator-facturacion, aemps-cima-api | 2026-09-30 |
| `geometria-seccion-censal` | Geometría de las secciones censales, distritos o municipios de un año para mapear datos del INE | ine-cartografia-censal, ine-api-tempus | 2026-09-30 |
| `horarios-tren-gtfs` | Horarios y paradas de Cercanías y de alta velocidad en GTFS, con las coordenadas de las estaciones | renfe-datos-abiertos | 2026-10-01 |
| `comercio-exterior-por-producto` | Exportaciones o importaciones de un producto TARIC por país y provincia, mensuales o anuales desde 1995 | datacomex, aeat-estadisticas | 2026-09-30 |
| `poblacion-renta-alquiler-por-municipio` | Población, renta media y precio del alquiler de un municipio con las tablas concretas del INE | ine-api-tempus, ine-cartografia-censal | 2026-09-30 |

### Pasos

**ipc-ultimo-dato** · Último IPC general nacional con variación mensual y anual
1. `ine-api-tempus`: GET DATOS_SERIE/{cod}?nult=1&tip=A con IPC290751 (índice), IPC290752 (variación mensual) e IPC290750 (variación anual); Data[0].Fecha es ISO y T3_TipoDato distingue Avance de Definitivo
   ```
   curl -s "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/IPC290750?nult=1&tip=A"
   ```
2. `ine-api-tempus`: Serie completa con date=19610101:20261231 en vez de nult (sin nult ni date responde 404); las tablas vigentes son 24077 (índice) y 76134 (tasas), comprobables en TABLAS_OPERACION/IPC
- salida: JSON con COD, Nombre y Data (Fecha, T3_Periodo, Anyo, Valor)

**localizar-tabla-ine** · Encontrar y descargar una tabla del INE por operación (EPA, padrón, PIB, natalidad) sin conocer su id
1. `ine-api-tempus`: GET OPERACIONES_DISPONIBLES para el Codigo de la operación (IPC, EPA...) y TABLAS_OPERACION/{Codigo} para sus tablas vigentes con Id y Nombre
   ```
   curl -s "https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/EPA"
   ```
2. `ine-api-tempus`: DATOS_TABLA/{Id}?nult=4&tip=A devuelve todas las series de la tabla; para filtrar, VARIABLES_OPERACION y VALORES_VARIABLEOPERACION dan los pares tv=id_variable:id_valor
3. `ine-api-tempus`: Cambiar js por csv en la URL da la tabla entera en CSV (tabulador, UTF-8 con BOM aunque la cabecera diga ISO-8859-15): ignora nult, y un tv o date con dos puntos da 400
   ```
   curl -s "https://servicios.ine.es/wstempus/csv/ES/DATOS_TABLA/24077?nult=1"
   ```
- salida: JSON con una entrada por serie (COD, Nombre, Data) o CSV de la tabla

**municipio-a-codigo-ine** · Código INE de un municipio a partir de su nombre, o la relación completa de municipios
1. `cnig-centro-descargas`: GET del geocoder CartoCiudad candidates?q={nombre}&limit=1 (464 B) devuelve muniCode (INE de 5 dígitos), provinceCode y comunidadAutonomaCode; find?q= añade la geometría (268 KB) e ignora municipio_filter; acepta tildes
   ```
   curl -s "https://www.cartociudad.es/geocoder/api/geocoder/candidates?q=Alcal%C3%A1%20de%20Henares&limit=1"
   ```
2. `ine-codigos-territoriales`: Relación completa en diccionario{AA}.xlsx con CPRO, CMUN y DC; el código es CPRO+CMUN (5 dígitos, conservar ceros) y DC es el dígito de control que algunos ficheros añaden
   ```
   curl -sO "https://www.ine.es/daco/daco42/codmun/diccionario26.xlsx"
   ```
3. `catastro-ovc`: Equivalencia con el código catastral en ObtenerMunicipios?Provincia={NOMBRE}&Municipio={texto} (loine es el INE, locat el catastral); el OVC bloquea la IP tras ráfagas de unas 15 peticiones
- salida: código INE de municipio (5 dígitos) y de provincia (2)

**coordenadas-a-referencia-catastral** · De unas coordenadas a la parcela (recinto SIGPAC y referencia catastral) y a los datos del inmueble
1. `mapa-sigpac`: refrecinbycoord/4326/{lon}/{lat}.json devuelve la referencia SIGPAC pr:mu:ag:zo:po:pa:re; recinfobypoint añade uso, superficie, pendiente y geometría WKT
   ```
   curl -s --compressed "https://sigpac-hubcloud.es/servicioconsultassigpac/query/refrecinbycoord/4326/-3.9/40.3.json"
   ```
2. `mapa-sigpac`: refcatparcela/{pr}/{mu}/{ag}/{zo}/{po}/{pa}.json devuelve referencia_cat (14 caracteres, a veces 20) repetida una vez por recinto; el municipio SIGPAC es el del Catastro (capitales 900), no el INE
   ```
   curl -s --compressed "https://sigpac-hubcloud.es/servicioconsultassigpac/query/refcatparcela/28/15/0/0/3/9000.json"
   ```
3. `catastro-ovc`: En suelo urbano, Consulta_RCCOOR (XML, pc1+pc2 son los 14 caracteres) y después Consulta_DNPRC?RefCat= para uso, superficie, año y municipio INE; el OVC bloquea la IP tras unas 15 peticiones seguidas (403 Petición HTTP bloqueada durante más de media hora el 30/09/2026)
   ```
   curl -s "https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR?SRS=EPSG:4326&Coordenada_X=-3.6960&Coordenada_Y=40.4185"
   ```
- salida: referencia SIGPAC, referencia catastral de 14 caracteres y datos no protegidos del inmueble

**parcela-a-red-natura-y-nitratos** · Saber si un recinto agrícola está en Red Natura 2000 o en zona vulnerable a nitratos
- entrada: referencia-sigpac
1. `mapa-sigpac`: Obtener los siete códigos del recinto con refrecinbycoord/4326/{lon}/{lat}.json o recinfobypoint
2. `mapa-sigpac`: intersection/red_natura/{pr}/{mu}/{ag}/{zo}/{po}/{pa}/{re}.json devuelve lic_code, lic_name, zepa_code, surface_intersection (m²) y surface_tpc (porcentaje 0-100); intersection/nitratos igual para zonas vulnerables; [] sin intersección; siempre en gzip
   ```
   curl -s --compressed "https://sigpac-hubcloud.es/servicioconsultassigpac/intersection/red_natura/28/15/0/0/3/9000/6.json"
   ```
- salida: lista JSON de intersecciones con códigos LIC y ZEPA y superficie afectada

**empresa-nif-a-ayudas-y-contratos** · Subvenciones, ayudas de investigación y contratos públicos de una empresa o entidad por su NIF
- entrada: nif
1. `bdns-api`: concesiones/busqueda?nifCif={NIF}&page=0&pageSize=100 con Accept application/json (con Accept de navegador responde XML); beneficiario trae NIF y nombre en un solo campo, con importe, ayudaEquivalente, numeroConvocatoria y fechaConcesion; el parámetro beneficiario= no existe (400)
   ```
   curl -s -H "Accept: application/json" "https://www.infosubvenciones.es/bdnstrans/api/concesiones/busqueda?page=0&pageSize=100&nifCif=Q1132001G"
   ```
2. `bdns-api`: grandesbeneficiarios, ayudasestado y minimis tienen el mismo patrón de búsqueda y aceptan nifCif (verificado el 2026-10-01; en ayudasestado beneficiario separa NIF y nombre con guion); exportación con concesiones/exportar?vpd=GE&tipoDoc=csv, los mismos filtros y pageSize (sin él, 50 filas)
3. `aei-convocatorias`: Ayudas de investigación con download-unlimit/All/All/All/All?cif={NIF}, que devuelve solo las filas de ese NIF (separador ;, UTF-8 con BOM); la BDNS no trae la referencia AEI, cruzar por NIF, convocatoria e importe
   ```
   curl -sS -o aei.csv "https://www.aei.gob.es/ayudas-concedidas/buscador-ayudas-concedidas/download-unlimit/All/All/All/All?cif=Q1132001G"
   ```
4. `placsp-datos-abiertos`: Contratos en los feeds ATOM y ZIP mensuales; los documentos CODICE llevan cbc:ID con schemeName NIF (adjudicatarios y órganos), filtrar por el valor y comprobar el elemento padre
5. `borme-api-sumario`: Actos societarios solo por nombre y fecha en el XML de cada provincia (receta actos-mercantiles-borme)
- salida: concesiones BDNS (JSON), ayudas AEI (filas CSV) y expedientes PLACSP (XML CODICE)

**organismo-a-dir3-y-nif** · Código DIR3 y NIF de un organismo público a partir de su nombre, y su jerarquía
1. `face-facturas`: relations?fulltext={nombre}&limit=100&page=1; cada item trae oc, og y ut con code (DIR3) y og.identifier con el NIF (falta en 1 de cada 5); fulltext distingue mayúsculas y tildes y busca subcadenas (Madrid trae Madridejos), así que filtrar por administration.code o buscar por el DIR3; relations.csv omite 27 de las 50187 relaciones
   ```
   curl -s "https://proveedores.face.gob.es/api/v1/relations?fulltext=Ayuntamiento%20de%20Madrid&limit=100&page=1"
   ```
2. `dir3-directorio`: Jerarquía completa y unidades ausentes de FACe en los xlsx por nivel (AGE 2741, CCAA 2742, EELL 2744), foto periódica y solo vigentes; un curl -L con cookie jar y User-Agent de navegador (la primera respuesta fija las cookies TS)
3. `datos-gob-es-api`: Con el DIR3, catalog/dataset/publisher/{dir3}.json lista los datasets que publica ese organismo
- salida: DIR3 (E, L, LA, A, U...), NIF y nombres oficiales

**boe-sumario-y-texto-consolidado** · Qué se publicó en el BOE un día y cómo pasar de una disposición a su texto y a la norma consolidada
- entrada: boe-id, eli
1. `boe-api-sumario`: GET /boe/sumario/{AAAAMMDD} con Accept application/json; recorrer diario, seccion, departamento, epigrafe e item (cada nivel puede ser objeto o lista); cada item trae identificador, titulo y url_pdf, url_html, url_xml
   ```
   curl -s -H "Accept: application/json" "https://www.boe.es/datosabiertos/api/boe/sumario/20240102"
   ```
2. `boe-api-sumario`: Texto completo en xml.php?id={identificador} (raíz documento con metadatos, analisis y texto), sin cabecera Accept
   ```
   curl -s "https://www.boe.es/diario_boe/xml.php?id=BOE-A-2024-87"
   ```
3. `boe-api-legislacion-consolidada`: /id/{identificador}/metadatos da vigencia, estado de consolidación y url_eli; /texto/indice los bloques y /texto/bloque/{id} cada artículo con sus versiones (solo XML)
   ```
   curl -s -H "Accept: application/json" "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-1978-31229/metadatos"
   ```
4. `boe-eli`: La URI ELI más /con devuelve el consolidado vigente en HTML con RDFa; sin sufijo, la versión publicada en el diario
- salida: sumario JSON, XML de cada disposición y consolidado por bloques; 404 los domingos y festivos

**buscar-norma-por-titulo** · Encontrar normas por palabras del título, rango o fecha y seguir sus cambios
- entrada: boe-id
1. `boe-api-legislacion-consolidada`: GET con query (JSON url-encoded con query_string sobre titulo, range sobre fecha_publicacion o fecha_disposicion y sort) y limit; devuelve identificador, titulo, fechas y ámbito de cada norma
   ```
   curl -s -G -H "Accept: application/json" "https://www.boe.es/datosabiertos/api/legislacion-consolidada" --data-urlencode 'query={"query":{"query_string":{"query":"titulo:vivienda"}},"sort":[{"fecha_publicacion":"desc"}]}' --data-urlencode "limit=20"
   ```
2. `boe-api-legislacion-consolidada`: Listado por fecha de última actualización del consolidado con from y to (AAAAMMDD) para detectar normas modificadas; datos-auxiliares/rangos y /materias dan los códigos de filtro
   ```
   curl -s -H "Accept: application/json" "https://www.boe.es/datosabiertos/api/legislacion-consolidada?from=20260901&limit=100"
   ```
3. `boe-feeds`: Para vigilar novedades sin API, RSS diario del BOE por sección (ISO-8859-1)
- salida: lista JSON de normas con identificador BOE; vigencia y url_eli en /id/{id}/metadatos

**licitaciones-nuevas** · Licitaciones y adjudicaciones publicadas hoy en toda la contratación pública
- entrada: dir3, cpv
1. `placsp-datos-abiertos`: GET del feed ATOM vigente, que solo trae lo último (127 entradas y 3,8 MB el 2026-10-01; se regenera una vez al día hacia las 20:15); link rel=next enlaza instantáneas anteriores de 500 entradas y 14 a 17 MB; cada entry lleva el CODICE con órgano (DIR3), CPV, importes y estado, y las anulaciones llegan como at:deleted-entry
   ```
   curl -s "https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3.atom"
   ```
2. `placsp-datos-abiertos`: Histórico en ZIP anuales desde 2012 y mensuales en 2025-2026 (el 643 pesa de 150 a 300 MB al mes; un ZIP inexistente responde 200 con HTML); PlataformasAgregadasSinMenores.atom para CCAA y EELL y contratosMenoresPerfilesContratantes.atom para menores
   ```
   curl -sO "https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3_202508.zip"
   ```
3. `boe-feeds`: Anuncios de licitación publicados en el BOE por división CPV en RSS (canal_cpv.php)
- salida: entradas ATOM con CODICE (XML basado en UBL) por expediente

**subvenciones-convocatorias-recientes** · Convocatorias de subvenciones publicadas en un rango de fechas y su detalle
- entrada: bdns
1. `bdns-api`: convocatorias/busqueda?page=0&pageSize=100&fechaDesde={dd/mm/aaaa}&fechaHasta={dd/mm/aaaa}&order=fechaRecepcion&direccion=desc (tipoAdministracion=C solo estatales); content[] con numeroConvocatoria, descripcion, nivel1 a nivel3 y mrr
   ```
   curl -s "https://www.infosubvenciones.es/bdnstrans/api/convocatorias/busqueda?page=0&pageSize=50&fechaDesde=01/09/2026&fechaHasta=30/09/2026&order=fechaRecepcion&direccion=desc"
   ```
2. `bdns-api`: convocatorias?numConv={numero} da órgano, instrumentos, presupuesto, bases y documentos; codigoBDNS es la clave estable
   ```
   curl -s "https://www.infosubvenciones.es/bdnstrans/api/convocatorias?numConv=800000"
   ```
3. `bdns-api`: Exportación masiva con convocatorias/exportar?vpd=GE&tipoDoc=csv, los mismos filtros y page y pageSize (sin pageSize devuelve 50 filas sin aviso; tope 10000; windows-1252)
- salida: JSON paginado de convocatorias y detalle por número BDNS

**deuda-publica-por-administracion** · Deuda de un ayuntamiento, de una comunidad autónoma o del Estado
1. `hacienda-ovef`: Deuda viva a 31 de diciembre por ayuntamiento en deuda-viva-ayuntamientos-{AAAA}12.xlsx (dipycab y restoeell en la misma carpeta)
   ```
   curl -sO "https://www.hacienda.gob.es/cdi/sist%20financiacion%20y%20deuda/informacioneells/2025/deuda-viva-ayuntamientos-202512.xlsx"
   ```
2. `bde-estadisticas`: Deuda según el Protocolo de Déficit Excesivo por subsector y por comunidad autónoma en el capítulo SB_DEUAAPP.zip del Boletín Estadístico (CSV con 6 filas de cabecera)
   ```
   curl -sO "https://www.bde.es/webbe/es/estadisticas/compartido/datos/zip/SB_DEUAAPP.zip"
   ```
3. `tesoro-estadisticas`: Deuda del Estado por instrumento, vida media, tenedores y vencimientos en los cuadros mensuales {NN}.xlsx (01 nominal en circulación), con User-Agent de navegador
   ```
   curl -sO -A "Mozilla/5.0" "https://www.tesoro.es/sites/default/files/estadisticas/01.xlsx"
   ```
4. `airef-datos`: Ratio de deuda pública total sobre PIB por informe (no por Administración) en Historico_Deuda.xlsx, con el último informe de octubre de 2024; localizar la URL en la página del observatorio de deuda y usar el bundle FNMT
- salida: xlsx por entidad (Hacienda), CSV por serie (BdE) y cuadros mensuales (Tesoro)

**irpf-por-municipio** · Renta y declarantes de IRPF por municipio y tramo, todos los ejercicios
- entrada: ine-municipio
1. `aeat-estadisticas`: IRPFmunicipios.csv (31 MB, separador ;, decimal coma, 2013-2023) con una fila por ejercicio (EJER), tramo (TRAMO) y municipio (MUNI_DEF) y una columna MUNI_n por variable; MUNI_DEF no es el código INE (4 es Albacete, 02003) y la equivalencia está en AyudaCSV_AnuarioMunicipal.pdf; celdas vacías como NULL literal; sin País Vasco ni Navarra
   ```
   curl -sO "https://sede.agenciatributaria.gob.es/static_files/Sede/Tema/Estadisticas/Anuario_estadistico/Exportacion/IRPFmunicipios.csv"
   ```
2. `aeat-estadisticas`: Recaudación mensual por figura tributaria en Cuadros_estadisticos_series_es_es.xlsx (URL fija, contenido sobrescrito en cada publicación)
- salida: CSV masivo de todos los ejercicios

**paro-registrado-por-municipio** · Paro registrado y demandantes por municipio, sexo, edad y actividad de un mes
- entrada: ine-municipio
1. `sepe-estadisticas`: La página del mes municipios/{AAAA}/{mes}.html ({mes}-{AAAA}.html hasta 2019) enlaza ESTADISTICA_MUNICIPIOS.xls, paro y contratos de todos los municipios con código INE (28001.0) por provincia, sexo, edad y sector; el enlace lleva un jcr:{uuid} nuevo cada mes
   ```
   curl -s -A "Mozilla/5.0" "https://www.sepe.es/HomeSepe/que-es-el-sepe/estadisticas/datos-estadisticos/municipios/2026/agosto.html" | grep -o '/HomeSepe/dam/jcr:[^"]*ESTADISTICA_MUNICIPIOS.xls'
   ```
2. `sepe-estadisticas`: Leer con pandas engine=calamine (xlrd falla en parte de los ficheros); «<5» es texto; el desglose por actividad (CNAE) solo existe para capitales y municipios de más de 20.000 habitantes (Municipios_acteco y Muniacteco_20-45)
   ```
   curl -sO -A "Mozilla/5.0" "https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_estadisticos/municipios_20_45/2026/agosto_2026/Muniacteco_20-45_ANDALUCIA.xls"
   ```
3. `sepe-estadisticas`: Series nacionales y provinciales con URL fija en evolparoseries.xls y paroprovsector.xls
   ```
   curl -sO -A "Mozilla/5.0" "https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_avance/xls/empleo/evolparoseries.xls"
   ```
4. `ine-codigos-territoriales`: Nombres y provincia oficiales del municipio con el diccionario anual; en los ficheros por actividad, sin código, cruzar por nombre
- salida: xls con paro y contratos por municipio y código INE

**afiliacion-y-pensiones** · Afiliados a la Seguridad Social por régimen, provincia, CNAE o municipio, y pensiones del mes
- entrada: cnae, ine-municipio
1. `segsocial-estadisticas`: GET de la página de la estadística (EST8/EST10/EST290/EST291 afiliación media; EST8/EST10/EST305 último día; EST23/EST24 pensiones) con User-Agent de navegador; extraer los enlaces wcm/connect, que llevan un uuid nuevo en cada publicación; la afiliación municipal tiene URL fija, descargas/STAT/MUNCNAE{MM}{AA}.xlsx
   ```
   curl -sL -A "Mozilla/5.0" -H "Accept: text/html,application/xhtml+xml" "https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST23/EST24" | grep -o 'href="[^"]*wcm/connect[^"]*"'
   ```
2. `segsocial-estadisticas`: Descargar el xlsx con curl -f o comprobando el Content-Type (el 403 llega como HTML de 708 bytes); el WAF rechaza la mitad de las peticiones con cualquier Accept, repetir la misma URL tras 4 s hasta ocho veces
3. `segsocial-estadisticas`: Pensiones mensuales con nombre {SERIE}{AAAAMM} (PI, IP, JUCOVI, TC, EDPR, TRCA); la afiliación por actividad pasa a CNAE 2025 en 2026
- salida: xlsx con varias hojas y cabeceras combinadas (no leer con header=0)

**precio-carburantes-municipio** · Precios de hoy de las gasolineras de un municipio o provincia, y el histórico de un día
- entrada: ine-provincia
1. `minetur-precios-carburantes`: Listados/Municipios/ devuelve IDMunicipio (código propio, no INE; Madrid 4354, Alcalá de Henares 4280) e IDProvincia en código INE
   ```
   curl -s -H "Accept: application/json" "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/Listados/Municipios/"
   ```
2. `minetur-precios-carburantes`: EstacionesTerrestres/FiltroMunicipio/{IDMunicipio} o FiltroProvincia/{INE2}; ListaEESSPrecio trae Rótulo, Dirección, Latitud, Longitud (WGS84) y un precio por carburante con coma decimal; con Accept de navegador responde XML, pedir application/json
   ```
   curl -s -H "Accept: application/json" "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/FiltroMunicipio/4354"
   ```
3. `minetur-precios-carburantes`: Histórico con EstacionesTerrestresHist/FiltroProvincia/{DD-MM-AAAA}/{INE2}; IDEESS es estable desde 2010 para seguir una estación
- salida: JSON con Fecha y ListaEESSPrecio

**incidencias-trafico-tiempo-real** · Incidencias, obras, cortes y velocidades de la red de carreteras en este momento
1. `dgt-datex-trafico`: nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v37.xml, DATEX II 3.7 con una situation por incidencia; se regenera cada minuto
   ```
   curl -s "https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v37.xml"
   ```
2. `dgt-datex-trafico`: Velocidades e intensidades de 5.569 detectores en MeasuredDataPublication/detectores/content.xml (18,7 MB por minuto, DATEX II 1.0) con sus localizaciones en PredefinedLocationsPublication/detectores; radares fijos en /radares/content.xml
   ```
   curl -s "https://infocar.dgt.es/datex2/dgt/PredefinedLocationsPublication/radares/content.xml"
   ```
3. `dgt-datex-trafico`: Cataluña y Gipuzkoa en sct y dt-gv SituationPublication/all/content.xml; zonas de bajas emisiones y puntos de recarga bajo /datex2/v3/
- salida: XML DATEX II (namespaces distintos por versión; parsear con lxml)

**matriculaciones-diarias** · Vehículos matriculados o dados de baja cada día, con marca, modelo y municipio
- entrada: ine-municipio
1. `dgt-estadisticas`: Listado de ficheros en matraba-listados/matriculaciones-automoviles-diario.html (24 diarios del mes) y -mensual.html (desde 2014-12); bajas en bajas-automoviles-diario y -mensual, detenidas en 2024-06 (diario) y 2024-05 (mensual)
   ```
   curl -s "https://www.dgt.es/menusecundario/dgt-en-cifras/matraba-listados/matriculaciones-automoviles-diario.html" | grep -o 'href="[^"]*export_mat_[^"]*"'
   ```
2. `dgt-estadisticas`: ZIP en /microdatos/salida/{AAAA}/{M}/vehiculos/matriculaciones/export_mat_{AAAAMMDD}.zip (mes sin cero); dentro un txt de ancho fijo en Latin-1 con bastidor enmascarado y municipio INE; el diseño de registro está en PDF en la ficha del producto
   ```
   curl -sSL -o mat.zip "https://www.dgt.es/microdatos/salida/2026/9/vehiculos/matriculaciones/export_mat_20260929.zip"
   ```
3. `dgt-estadisticas`: Parque completo por vehículo en /microdatos/Parque/{AAAA}/parque_consolidado_{AAAA}.zip (1,6 GB en 2025) y mensual desde 2025-03
- salida: txt de ancho fijo por día

**calidad-aire-estacion** · Serie horaria o diaria de un contaminante en una estación de calidad del aire
1. `miteco-calidad-aire`: Metainformacion_{AAAA}.xlsx, hoja Estaciones_{AAAA}, con COD_LOCAL, código europeo, red, latitud, longitud, altitud y tipo de estación; elegir la estación por coordenadas
2. `miteco-calidad-aire`: Datos_HH_{AAAA}.zip (27 MB) trae un CSV por contaminante con una fila por estación y día y columnas H01 a H24 (separador ;, punto decimal, vacío = sin dato); Datos_DD para diarios con D01 a D31
   ```
   curl -sSL -o Datos_HH_2024.zip "https://www.miteco.gob.es/content/dam/miteco/es/calidad-y-evaluacion-ambiental/sgalsi/atm%c3%b3sfera-y-calidad-del-aire/evaluaci%c3%b3n-2024/Datos_HH_2024.zip"
   ```
3. `miteco-calidad-aire`: Cada año tiene su página (datos-oficiales-{AAAA}.html desde 2022) y nombres de fichero distintos; tomar los enlaces de la página en cada ejecución
- salida: CSV anuales por contaminante

**embalses-y-caudales** · Reserva de agua de un embalse y caudal diario de un río en una estación de aforo
1. `miteco-saih-boletin-hidrologico`: BD-Embalses.zip (Access, 10 MB) con una tabla cuyo nombre lleva los años (T_Datos Embalses 1988-2026; listarla con mdb-tables -1) y AMBITO_NOMBRE, EMBALSE_NOMBRE, FECHA, AGUA_TOTAL y AGUA_ACTUAL (texto con coma decimal, hm3) y ELECTRICO_FLAG, semanal desde 1987-10-06; mdb-export -T '%Y-%m-%d' para fechas ISO, o access-parser en Python
   ```
   curl -sSL -o BD-Embalses.zip "https://www.miteco.gob.es/content/dam/miteco/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico/Historico-de-embalses/BD-Embalses.zip"
   ```
2. `miteco-saih-boletin-hidrologico`: listado-estaciones-aforo.zip (cuatro CSV en Latin-1 con COD_HIDRO, COD_SAIH, UTM huso 30 y municipio) y Anuario-21-22-csv.zip (136 MB, afliq.csv por cuenca con indroea;fecha;altura;caudal diarios y afliqe.csv con la reserva validada de embalses)
   ```
   curl -sSL -o estaciones.zip "https://www.miteco.gob.es/content/dam/miteco/es/agua/temas/evaluacion-de-los-recursos-hidricos/sistema-informacion-anuario-aforos/listado-estaciones-aforo.zip"
   ```
3. `miteco-saih-boletin-hidrologico`: Tiempo real solo en el SAIH de cada confederación (enlaces en saih.html), cada uno con su formato
- salida: tabla Access de embalses y CSV de caudales diarios por estación

**capa-red-natura-2000** · Descargar la capa oficial de Red Natura 2000 u otra capa de biodiversidad
1. `miteco-banco-datos-naturaleza`: DescargaFichero?f=rn2000.zip exige resolver un desafío ALTCHA (prueba de trabajo SHA-256) y enviarlo en el POST ?handler=Download; código completo en guides/cliente-http.md; 133 MB con el shapefile PS_Natura2000_2025
   ```
   curl -s "https://gis.miteco.gob.es/descargas/app/DescargaFichero?handler=Altcha"
   ```
2. `miteco-banco-datos-naturaleza`: Descargas directas sin desafío en storage.googleapis.com para IEZH, MFE, hábitats y el resto de capas del IEPNB (lista en iepnb.gob.es/nuestros-datos/descargas)
   ```
   curl -sSL -o IEZH_shp_2025.zip "https://storage.googleapis.com/gestor-doc-portal-iepnb/Ecosistemas/inventario_esp_zonas_humedas/zonas_humedas/IEZH_shp_2025.zip"
   ```
3. `mapa-sigpac`: Para una parcela concreta, intersection/red_natura evita descargar la capa (receta parcela-a-red-natura-y-nitratos)
- salida: ZIP con shapefile o GML

**prediccion-meteo-municipio** · Predicción diaria u horaria de un municipio y observación de la estación más cercana
- entrada: ine-municipio, idema
1. `aemet-opendata`: Con clave gratuita en la cabecera api_key (caduca a los tres meses), GET prediccion/especifica/municipio/diaria/{INE de 5 dígitos sin dígito de control}; la respuesta es un JSON intermedio (estado, datos) y los datos se descargan con una segunda petición a la URL del campo datos, en ISO-8859-15; sin clave llega 200 con cuerpo vacío
   ```
   curl -s -H "api_key: $AEMET_KEY" "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/28079"
   ```
2. `aemet-opendata`: valores/climatologicos/inventarioestaciones/todasestaciones da idema y coordenadas; elegir la más cercana y pedir observacion/convencional/datos/estacion/{idema}
3. `aemet-opendata`: Las 64 rutas y sus parámetros están en AEMET_OpenData_specification.json (OpenAPI 3.0.1), sin clave
   ```
   curl -s "https://opendata.aemet.es/AEMET_OpenData_specification.json"
   ```
- salida: JSON de predicción por día (ficheros en ISO-8859-15); errores con HTTP 200 y estado en el cuerpo; 429 tras unas diez peticiones por minuto

**medicamento-por-cn-o-nombre** · Datos de un medicamento por código nacional, nombre o principio activo, con ficha técnica y problemas de suministro
- entrada: cn-medicamento
1. `aemps-cima-api`: medicamento?cn={cn} o ?nregistro={nreg} devuelve nregistro, pactivos, atcs, presentaciones (cn, estado), docs (PDF y HTML) y estado; medicamentos?nombre= o ?practiv1= busca (páginas de 200; un cn inexistente responde 204 sin cuerpo)
   ```
   curl -s "https://cima.aemps.es/cima/rest/medicamento?cn=708201"
   ```
2. `aemps-cima-api`: docSegmentado/contenido/1?nregistro={nreg}&seccion=4.1 devuelve la sección de la ficha técnica en JSON [{seccion, titulo, contenido, orden}] (HTML solo con Accept text/html); PDF estable en /cima/pdfs/ft/{nreg}/FT_{nreg}.pdf
3. `aemps-cima-api`: psuministro lista los problemas de suministro activos por cn; registroCambios?fecha=dd/mm/aaaa sincroniza sin rebajar todo (sin orden por fecha); nomenclátor completo en prescripcion.zip, regenerado a diario y que exige User-Agent de navegador (403 sin él)
   ```
   curl -s "https://cima.aemps.es/cima/rest/psuministro"
   ```
- salida: JSON del medicamento (solo JSON; Accept XML responde 406)

**exceso-mortalidad-momo** · Defunciones observadas y esperadas por día, ámbito, sexo y edad (MoMo)
- entrada: ccaa
1. `isciii-cne`: momo.isciii.es/public/momo/data es un único CSV de 719 MB (comillas, coma) regenerado a diario; Range no sirve (con desplazamiento pequeño devuelve todo con 200 y con uno grande un 500 de mantenimiento), así que leer en streaming y filtrar por ambito (nacional, ccaa, provincia), cod_ine_ambito, cod_sexo y cod_gedad (all y +65 son agregados)
   ```
   curl -sS "https://momo.isciii.es/public/momo/data" | head -c 2000
   ```
2. `isciii-cne`: Columnas defunciones_observadas, defunciones_estimadas_base, _q01, _q99 y atribuibles a exceso y defecto de temperatura; las últimas semanas se revisan en cada descarga
- salida: CSV diario desde 2015

**cosecha-oai-publicaciones** · Cosechar publicaciones científicas o patrimonio digital de forma incremental
1. `csic-digital`: ?verb=ListRecords&metadataPrefix=oai_dc&from={AAAA-MM-DD} (100 por página, resumptionToken al final del XML); set=com_10261_NN por instituto; 13 formatos (datacite, oai_cerif_openaire, mods, marc)
   ```
   curl -s "https://digital.csic.es/dspace-oai/request?verb=ListRecords&metadataPrefix=oai_dc&from=2026-09-01"
   ```
2. `bne-datos`: Hispana en hispana.mcu.es/oai/oai.cmd con los mismos verbos (10,6 millones de registros, 124 sets, formatos oai_dc, edm, ese y didl)
   ```
   curl -s "https://hispana.mcu.es/oai/oai.cmd?verb=Identify"
   ```
3. `fecyt-recolecta`: RECOLECTA ya no expone OAI-PMH (404 en cuatro rutas el 30/09/2026); cosechar cada repositorio universitario por separado
- salida: XML OAI-PMH paginado con resumptionToken

**tabla-pcaxis-a-csv** · Descargar como CSV una tabla de cualquier portal PC-Axis (INE, EDUCAbase, criminalidad, CULTURAbase) sin navegador
1. `ine-api-tempus`: INE, cambiar js por csv en la API (csv/ES/DATOS_TABLA/{id}): tabla entera, ignora nult; tabulador, UTF-8 con BOM
   ```
   curl -s "https://servicios.ine.es/wstempus/csv/ES/DATOS_TABLA/24077?nult=12"
   ```
2. `educacion-estadisticas-ruct`: EDUCAbase, del enlace Tabla.htm?path=...&file=X.px deducir EducaJaxiPx/files/_px/es/csv_bdsc{path}{file}?nocab=1 (separador ;, UTF-8 con BOM aunque la cabecera diga ISO-8859-15, miles con punto)
   ```
   curl -s "https://estadisticas.educacion.gob.es/EducaJaxiPx/files/_px/es/csv_bdsc/no-universitaria/alumnado/matriculado/2024-2025-rd/adultos/l0/adul_01.px?nocab=1"
   ```
3. `interior-criminalidad`: Criminalidad, mismo patrón en sec/jaxiPx/files/_px/es/csv_bdsc{path}{file}?nocab=1 (todo el año en curso en /DatosBalanceAct/l0/; UTF-8 con BOM)
   ```
   curl -s "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/09004.px?nocab=1"
   ```
4. `cultura-culturabase`: CULTURAbase, mismo patrón en CulturaJaxiPx/files/_px/es/csv_bdsc{path}{file}?nocab=1 (UTF-8 con BOM); la serie vigente de empleo cultural está en /t1/p1f/ y /t1/p1/ solo cubre 2008-2010
   ```
   curl -s "https://estadisticas.cultura.gob.es/CulturaJaxiPx/files/_px/es/csv_bdsc/t1/p1f/M_Anuales/l0/T1FM1001.px?nocab=1"
   ```
- salida: CSV con la tabla completa; px y xlsx cambiando csv_bdsc por px o xlsx

**ocurrencias-especie-espana** · Registros de presencia de una especie en España, con recuento y descarga
1. `gbif-es`: species/match?name={nombre científico} devuelve usageKey (taxón), rank, matchType y confidence
   ```
   curl -s "https://api.gbif.org/v1/species/match?name=Lynx%20pardinus"
   ```
2. `gbif-es`: occurrence/search?country=ES&taxonKey={usageKey}&limit=300&offset={n} (limit mayor se recorta a 300 sin aviso y offset + limit no pasa de 100.001; filtros hasCoordinate, year, gadmGid); para el total, search con limit=0, porque occurrence/count da 400 con hasCoordinate o gadmGid
   ```
   curl -s "https://api.gbif.org/v1/occurrence/count?country=ES&taxonKey=2435261"
   ```
3. `gbif-es`: Más de 100000 registros exige una descarga asíncrona (occurrence/download/request con usuario GBIF gratuito)
- salida: JSON Darwin Core con results, count y endOfRecords

**geologia-y-aguas-subterraneas-punto** · Unidad geológica en un punto y puntos de agua subterránea de una provincia
1. `igme-geologia`: IGME_Geode_50/MapServer/8/query con geometry={lon},{lat}, inSR=4326 y spatialRel=esriSpatialRelIntersects devuelve CODE_UNIO, DESC_UNIT y edades
   ```
   curl -s "https://mapas.igme.es/gis/rest/services/Cartografia_Geologica/IGME_Geode_50/MapServer/8/query?geometry=-3.70,40.42&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=CODE_UNIO,DESC_UNIT,NAME_EDA1&returnGeometry=false&f=json"
   ```
2. `igme-geologia`: BasesDatos/IGME_PuntosAgua/MapServer/0/query?where=Provincia='Madrid'&outFields=*&resultRecordCount={n} (139.697 puntos con acuífero, caudal, profundidad y usos)
   ```
   curl -s "https://mapas.igme.es/gis/rest/services/BasesDatos/IGME_PuntosAgua/MapServer/0/query?where=Provincia%3D%27Madrid%27&outFields=*&resultRecordCount=5&f=json"
   ```
3. `igme-geologia`: La hoja MAGNA 50 por número de hoja en PDF y en VRF_MAGNA50_{hoja}.zip, que es un JPG georreferenciado en ED50, no vectorial; los vectores MAGNA están en el servicio Cartografia_Geologica/IGME_MAGNA_50
- salida: JSON ArcGIS (features[].attributes)

**buscar-dataset-datos-gob-es** · Localizar un dataset abierto de cualquier Administración y su URL de descarga real
- entrada: dir3
1. `datos-gob-es-api`: catalog/dataset/title/{texto}.json?_pageSize=50 o theme/{tema}.json; cada dataset trae distribution[] con accessURL y format; el WAF (Incapsula) responde 403 a la mayoría de las peticiones, reintentar hasta 10 veces con espera
   ```
   curl -s -A "Mozilla/5.0" "https://datos.gob.es/apidata/catalog/dataset/title/paro.json?_pageSize=50"
   ```
2. `datos-gob-es-api`: publisher/{dir3}.json para todos los datasets de un organismo (DIR3 con la receta organismo-a-dir3-y-nif)
3. `datos-gob-es-api`: El fichero vive en el portal del publicador; datos.gob.es solo guarda metadatos y el enlace puede estar muerto, comprobarlo
- salida: JSON Linked Data API (result.items[])

**series-banco-de-espana** · Último dato o serie completa de un indicador del Banco de España (euríbor, tipos, crédito, deuda)
1. `bde-estadisticas`: Código de serie en los catálogos catalogo_{be|tc|ti|si|pb}.csv (ISO-8859-1; nombre, alias, fichero del cuadro, descripción, frecuencia, primera y última observación)
   ```
   curl -sO "https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/catalogo_tc.csv"
   ```
2. `bde-estadisticas`: favoritas?idioma=es&series={cod} da el último valor; listaSeries?idioma=es&series={cod}&rango=MAX la serie, pero MAX devuelve como mucho las 1000 observaciones más recientes sin aviso y en diarias da 412: completar con rango=AAAA; la respuesta va siempre en gzip, usar --compressed
   ```
   curl -s --compressed "https://app.bde.es/bierest/resources/srdatosapp/favoritas?idioma=es&series=D_1NBAF472"
   ```
3. `bde-estadisticas`: CSV del cuadro entero en csv/{cuadro}.csv (nombre en minúsculas, 6 filas de cabecera, fechas en español) o ZIP por capítulo del Boletín
- salida: JSON con serie, fechaValor, valor y metadatos

**flota-pesquera** · Buques de la flota pesquera por puerto base, caladero y modalidad, y capturas por especie
1. `mapa-pesca`: Registro de flota 2006-2025 en un xlsx (15 MB, hoja Datos con AÑO, CODIGOBUQUE, PUERTO BASE, PROVINCIA, CCAA, CALADERO, modalidad, ARQUEO GT, POTENCIA KW, ESLORA, EDAD); el nombre lleva marca de tiempo, localizar el enlace rgfp_bi_excel en la página del registro
   ```
   curl -s "https://www.mapa.gob.es/es/pesca/temas/registro-flota/informacion-sobre-flota-pesquera" | grep -o 'href="[^"]*rgfp_bi_excel[^"]*"'
   ```
2. `mapa-pesca`: Capturas y desembarcos por especie, destino y zona en xlsx en estadistica-capturas-desembarcos (serie 1992-2024)
- salida: xlsx con una fila por buque y año; el identificador es CODIGOBUQUE, no el CFR europeo

**criminalidad-municipio** · Infracciones penales por tipología y trimestre en una comunidad, provincia o municipio de más de 20.000 habitantes
- entrada: ine-municipio
1. `interior-criminalidad`: Índice del trimestre en sec/dynPx/inebase/index.htm?type=pcaxis&path=/DatosBalanceAnt/{AAAA}{T}/&file=pcaxis, que da el path y file reales de sus tablas (todo el año en curso cuelga de /DatosBalanceAct/l0/)
   ```
   curl -s "https://estadisticasdecriminalidad.ses.mir.es/sec/dynPx/inebase/index.htm?type=pcaxis&path=/DatosBalanceAnt/20262/&file=pcaxis"
   ```
2. `interior-criminalidad`: CSV con jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/09006.px?nocab=1 (municipios; 09005 provincias, 09004 CCAA); cabecera Geografía;Tipología penal;Periodos:;Total, UTF-8 con BOM aunque la cabecera diga ISO-8859-15, miles con punto y decimales con coma; desde 2024 el municipio lleva delante su código INE y los balances son acumulados desde enero
   ```
   curl -s "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/09006.px?nocab=1"
   ```
3. `interior-criminalidad`: El balance es acumulado desde enero; un trimestre suelto es el balance menos el anterior del mismo año (09006 menos 09003 para abril-junio), en la misma Geografía y Tipología penal
   ```
   curl -s "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/09003.px?nocab=1"
   ```
- salida: CSV con periodo actual, anterior y variación por tipología; el trimestre suelto, por diferencia

**actos-mercantiles-borme** · Constituciones, nombramientos, ceses y disoluciones de sociedades publicados en el BORME
- entrada: boe-id
1. `borme-api-sumario`: GET /borme/sumario/{AAAAMMDD} con Accept application/json; la sección A trae un item por provincia con identificador BORME-A-AAAA-NNN-PP (PP es el código de provincia)
   ```
   curl -s -H "Accept: application/json" "https://www.boe.es/datosabiertos/api/borme/sumario/20240102"
   ```
2. `borme-api-sumario`: xml.php?id={BORME-A-...} devuelve los actos de la provincia (raíz documento, un par de párrafos por empresa con denominación y actos); no hay búsqueda por empresa, hay que recorrer días y provincias
   ```
   curl -s "https://www.boe.es/diario_borme/xml.php?id=BORME-A-2024-1-01"
   ```
3. `boe-feeds`: RSS diario del BORME para vigilar novedades (ISO-8859-1)
- salida: XML por provincia y día; sin publicación sábados, domingos ni festivos (404)

**hospitales-catalogo** · Listado de hospitales con camas, dependencia, complejo y municipio
- entrada: ine-municipio
1. `sanidad-portal-estadistico`: CNH_{AAAA}.xlsx (9 hojas, 848 hospitales en 2025, todas las celdas como texto) con código de hospital, camas, dependencia funcional y código de municipio INE con dígito de control (6 dígitos; quitar el último para cruzar)
   ```
   curl -sSL -o CNH_2025.xlsx "https://www.sanidad.gob.es/estadEstudios/estadisticas/sisInfSanSNS/ofertaRecursos/hospitales/docs/CNH_2025.xlsx"
   ```
- salida: xlsx

**dataset-cnmc-a-csv** · Descargar un dataset de la CNMC (energía, telecomunicaciones, postal) como CSV o consultarlo por API
1. `cnmc-data`: package_search?q={texto}&rows=1000 (210 datasets) devuelve name, title y resources[] con url y datastore_active
   ```
   curl -s "https://catalogodatos.cnmc.es/api/3/action/package_search?q=comercializadoras&rows=5"
   ```
2. `cnmc-data`: datastore/dump/{resource_id}?format=csv vuelca el recurso entero (coma, primera columna _id); datastore_search?resource_id=&limit= consulta en JSON con campos tipados
   ```
   curl -s "https://catalogodatos.cnmc.es/datastore/dump/522dcc75-b5c4-4c8d-9ec3-c8d8cf66d6b2?format=csv"
   ```
- salida: CSV o JSON del datastore

**convenio-colectivo-regcon** · Consultar un convenio colectivo por código, denominación o CNAE en REGCON
- entrada: codigo-convenio, cnae
1. `mites-estadisticas`: POST a consultaPublicaEstatal con codigoConvenio (14 dígitos), denominacion o idCnaesBusqueda (ids internos del desplegable) y _buscar, con cookie jar; consulta_token_value_id lo rellena el JavaScript y no hace falta; el servidor no envía el intermedio FNMT (bundle de la guía)
   ```
   curl -s --cacert ca-age.pem -c cj -b cj "https://expinterweb.mites.gob.es/regcon/pub/consultaPublicaEstatal" -d "denominacion=hosteleria" -d "_buscar=" | grep -o '[0-9]* - [0-9]*&nbsp;de&nbsp;[0-9]*'
   ```
2. `mites-estadisticas`: ?_exportarExcelPublicoXML=1 con la misma cookie exporta todas las filas de la última búsqueda en SpreadsheetML (ISO-8859-1), leer con ElementTree; ?pagina=N sin la cookie devuelve el registro entero
   ```
   curl -s --cacert ca-age.pem -b cj -o regcon.xls "https://expinterweb.mites.gob.es/regcon/pub/consultaPublicaEstatal?_exportarExcelPublicoXML=1"
   ```
- salida: HTML paginado de 15 filas y exportación SpreadsheetML con todas las filas de la búsqueda

**deficit-y-ejecucion-presupuestaria** · Déficit mensual de las Administraciones Públicas y ejecución del presupuesto del Estado
1. `igae-ejecucion-presupuestaria`: Operaciones no financieras mensuales de la Administración Central, acumuladas desde enero, en M_AACC_{AAAA}.xlsx (URL predecible por año; exige User-Agent de navegador) y serie anual en CAP_Serie.xlsx
   ```
   curl -sO -A "Mozilla/5.0" "https://www.igae.pap.hacienda.gob.es/sitios/igae/es-ES/Contabilidad/ContabilidadNacional/Publicaciones/Documents/AACC-M/M_AACC_2026.xlsx"
   ```
2. `igae-ejecucion-presupuestaria`: Ejecución mensual del presupuesto del Estado desde la página imejecucionpresupuesto.aspx (enlaces a xlsx por mes)
3. `hacienda-ovef`: Ejecución trimestral de las entidades locales, agregada por CCAA y grandes ciudades, un fichero por trimestre desde el 2T de 2013 (xlsx desde 2021q2); nombres con la fecha de publicación, tomar el enlace de la página
- salida: xlsx con cuadros por subsector

**precio-electricidad-horario** · Precio de la electricidad por hora o cuarto de hora (mercado diario, PVPC y spot) y demanda del día
1. `omie-mercado`: Precio marginal oficial en marginalpdbc_{AAAAMMDD}.1 (96 periodos cuarto-horarios desde el 01/10/2025, 92 o 100 en los cambios de hora; cabecera, filas AAAA;MM;DD;periodo;precio;precio y asterisco final); el del día siguiente se publica hacia las 13:50; con parents%5B0%5D= responde 302 y curl sin -L guarda la redirección
   ```
   curl -s "https://www.omie.es/es/file-download?parents=marginalpdbc&filename=marginalpdbc_20260929.1"
   ```
2. `ree-redata`: PVPC y precio spot por hora en mercados/precios-mercados-tiempo-real con time_trunc=hour (hasta tres días por petición); demanda real y prevista en demanda/demanda-tiempo-real; reintentar ante el 403 del WAF
   ```
   curl -s "https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date=2026-09-29T00:00&end_date=2026-09-29T23:59&time_trunc=hour"
   ```
- salida: fichero de texto con 96 precios (OMIE) y JSON con series PVPC (1001) y spot (600) por hora (REData)

**medicamento-precio-financiado** · Precio de venta, precio de referencia y aportación de un medicamento financiado, con su ficha técnica
- entrada: cn-medicamento
1. `sanidad-nomenclator-facturacion`: Descargar el nomenclátor completo (?metodo=nomenclatorExcel, 7 MB, hoja PRODUCTOS) y filtrar por Código Nacional; PVP con IVA, Precio de referencia, Aportación del beneficiario y agrupación homogénea; leer el código como texto
   ```
   curl -s -o nomenclator.xls "https://www.sanidad.gob.es/profesionales/nomenclator.do?metodo=nomenclatorExcel"
   ```
2. `aemps-cima-api`: medicamento?cn={cn} para composición, presentaciones, estado de autorización y ficha técnica; CIMA no trae precios y el nomenclátor no trae los no financiados
   ```
   curl -s "https://cima.aemps.es/cima/rest/medicamento?cn=708201"
   ```
- salida: fila del nomenclátor con precios y financiación más el JSON de CIMA

**geometria-seccion-censal** · Geometría de las secciones censales, distritos o municipios de un año para mapear datos del INE
- entrada: seccion-censal, ine-municipio
1. `ine-cartografia-censal`: seccionado_{AAAA}.zip del mismo año que el dato (65 MB, shapefile ETRS89 UTM 30; en geopandas con la ruta interna zip://seccionado_2026.zip!carpeta/SECC_CE_20260101.shp); CUSEC es la sección de 10 dígitos, CUDIS el distrito y CUMUN el municipio; también por la API OGC del INE (TIPO SECCIONADO)
   ```
   curl -sO "https://www.ine.es/prodyser/cartografia/seccionado_2026.zip"
   ```
2. `ine-api-tempus`: Los datos por sección (Atlas de distribución de renta) o por municipio se cruzan por esos códigos, cargados como texto con ceros a la izquierda
- salida: GeoDataFrame con una fila por sección y los códigos territoriales

**horarios-tren-gtfs** · Horarios y paradas de Cercanías y de alta velocidad en GTFS, con las coordenadas de las estaciones
1. `renfe-datos-abiertos`: GTFS estáticos con URL fija (google_transit.zip para AV, LD y MD; fomento_transit.zip para Cercanías); sin feed_info, la fecha de versión está en last_modified de package_show; las líneas de los .txt van rellenas de espacios y stop_id lleva ceros, leer como texto y recortar
   ```
   curl -sO "https://ssl.renfe.com/gtransit/Fichero_AV_LD/google_transit.zip"
   ```
2. `renfe-datos-abiertos`: estaciones.csv (ISO-8859-1, separador ;) con CODIGO, LATITUD y LONGITUD para geolocalizar; los feeds GTFS-RT de gtfsrt.renfe.com (JSON y protobuf) fallan en el TLS cerca de la mitad de las veces, reintentar
   ```
   curl -sO "https://ssl.renfe.com/ftransit/Fichero_estaciones/estaciones.csv"
   ```
- salida: ZIP GTFS y CSV de estaciones

**comercio-exterior-por-producto** · Exportaciones o importaciones de un producto TARIC por país y provincia, mensuales o anuales desde 1995
- entrada: ine-provincia
1. `datacomex`: Registrarse una vez en datacomex.comercio.es (correo y contraseña, activación por correo) y obtener el token con POST a IniciarSesion; la respuesta es la cadena "token:eyJ...", quitar el prefijo token: y las comillas
   ```
   curl -s -X POST -H "Content-Type: application/json" -d "{\"Usuario\":\"$DATACOMEX_USER\",\"Pass\":\"$DATACOMEX_PASS\"}" "https://comercio.serviciosmin.gob.es/DatacomexAPI/IniciarSesion"
   ```
2. `datacomex`: GET ObtenerDatos con los cinco parámetros (f, pe, pa, ta, pr); pe=ALLM da la serie mensual completa y pe=ALL la anual; pa es el código numérico de país (001 Francia) o ALL; comprobar mensaje en cada fila (provisional, definitivo, error de sintaxis)
   ```
   curl -s -H "Authorization: Bearer $DATACOMEX_TOKEN" "https://comercio.serviciosmin.gob.es/DatacomexAPI/ObtenerDatos?f=E&pe=ALLM&pa=001&ta=2204&pr=ALL"
   ```
3. `aeat-estadisticas`: Para comercio exterior sin registro, la AEAT publica el detalle en MAXIMA_DESAGREGACION_{AAAA}.csv (572 MB, sin cabecera, punto decimal; ficha aeat-estadisticas), la fuente primaria de DataComex
- salida: JSON con Resultados (flujo, periodo, país, provincia, taric, euros y kilos como texto con coma decimal)

**poblacion-renta-alquiler-por-municipio** · Población, renta media y precio del alquiler de un municipio con las tablas concretas del INE
- entrada: ine-municipio
1. `ine-api-tempus`: VALORES_VARIABLEOPERACION/19/22 lista los 8.142 municipios con Codigo INE e Id (Abengibre 02001 es 6124); ese Id es el que admite el filtro tv=19:{id} en cualquier tabla con la variable Municipios
   ```
   curl -s "https://servicios.ine.es/wstempus/js/ES/VALORES_VARIABLEOPERACION/19/22"
   ```
2. `ine-api-tempus`: Padrón por municipio y sexo en DATOS_TABLA/29005?nult=1&tv=19:{id} (sin filtro son 24.414 series y 14 MB); la operación DPOP (Id 22) tiene 65 tablas
   ```
   curl -s "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/29005?nult=1&tv=19:6124&tip=AM"
   ```
3. `ine-api-tempus`: Atlas de distribución de renta (operación ADRH, Id 353): 540 tablas con nombres repetidos, nueve por provincia (30656 Albacete, 30833 Alicante, 30842 Almería); Indicadores de renta media y mediana por municipio, distrito y sección con tv=19:{id}
   ```
   curl -s "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/30656?nult=1&tv=19:6124&tip=AM"
   ```
4. `ine-api-tempus`: Índice de precios de la vivienda en alquiler por municipio de más de 10.000 habitantes en DATOS_TABLA/59060 (operación IPVA, Id 432; el MetaData de cada serie lleva el código INE)
   ```
   curl -s "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/59060?nult=1&tip=AM"
   ```
5. `ine-cartografia-censal`: Geometría de secciones y municipios del mismo año para mapear (CUSEC y CUMUN)
- salida: series JSON con MetaData (variable, nombre y Codigo INE) y Data por año
- nota: Alternativa sin buscar la tabla provincial: la tabla nacional 30824 con tv=19:{Id municipio}&tv=482:284048 (renta neta media por persona; 284052 por hogar) devuelve la serie 2015-2023; sin filtro responde 200 con status de restricciones de volumen. Verificado el 2026-10-01.

## Dónde está cada cosa

**Legislación y boletines oficiales**
- Sumario diario del BOE con identificador y URLs de cada disposición → `boe-api-sumario`
- Texto consolidado, vigencia y versiones de una norma → `boe-api-legislacion-consolidada` (incluye normas autonómicas; los boletines autonómicos no están en el catálogo)
- URI estable de una norma para citar o enlazar → `boe-eli`
- Vigilar novedades del BOE, BORME, ayudas o licitaciones sin programar contra la API → `boe-feeds` (RSS en ISO-8859-1)
- Actos societarios inscritos en el Registro Mercantil → `borme-api-sumario` (sin búsqueda por empresa; recorrer días y provincias, o cargarlo en el almacén local y buscar por denominación (guides/almacen.md))

**Economía, finanzas y mercados**
- Euríbor, tipos de interés y de cambio, crédito, balanza de pagos → `bde-estadisticas` (listaSeries con rango=MAX corta en las 1000 observaciones más recientes sin aviso; completar con rango=AAAA)
- Deuda pública por Administración (Protocolo de Déficit Excesivo) → `bde-estadisticas` (capítulo SB_DEUAAPP; airef-datos solo da la ratio total sobre PIB por informe, no por Administración)
- Subastas del Tesoro y deuda del Estado por instrumento y tenedor → `tesoro-estadisticas` (año en curso en 11.xlsx e históricos anuales; el HTML de subastas mezcla decimales con coma y con punto)
- Previsiones macroeconómicas y estimación del PIB en tiempo real → `airef-datos` (xlsx en wp-content/uploads con rutas que cambian en cada actualización; tomar el enlace de la página)
- Entidades supervisadas, hechos relevantes e informes financieros de cotizadas → `cnmv-registros` (sin API; formularios ASP.NET, XML mensual de IIC y RSS)
- Líneas ICO y avales por beneficiario → `ico-datos` (sin datos por beneficiario ni descargas tabulares; aprobaciones agregadas por canal en tablas HTML)

**Hacienda, tributos y presupuestos**
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

**Estadística oficial**
- Cualquier estadística oficial del INE (IPC, EPA, PIB, padrón, natalidad, empresas) → `ine-api-tempus`
- Códigos INE de municipios, provincias y comunidades → `ine-codigos-territoriales`
- Microdatos de encuestas (EPA, condiciones de vida, presupuestos familiares, censo) → `ine-microdatos`
- Turismo (FRONTUR, EGATUR, ocupación hotelera) → `ine-api-tempus` (las operaciones son del INE; DATAESTUR (mincotur-industria-turismo) las reagrega con una API que no exigió clave y da 504 a menudo)
- Renta por sección censal (Atlas de distribución de renta) → `ine-api-tempus` (operación del INE; localizar la tabla con TABLAS_OPERACION, no verificada en esta sesión)
- Empresas activas por actividad y tamaño (DIRCE) → `ine-api-tempus`
- Tasa de paro, ocupados y activos (EPA) → `ine-api-tempus` (la EPA es del INE, no del SEPE)
- Salarios → `ine-api-tempus` (Encuesta de Estructura Salarial en el INE; salarios en fuentes tributarias por municipio en aeat-estadisticas (modelo190_salarios))
- Pasar un municipio entre códigos INE, SIGPAC o Catastro, DIR3, NIF del ayuntamiento, NUTS3 y coordenadas → `ine-codigos-territoriales` (datos/municipios.csv o la herramienta municipio del MCP; SIGPAC y Catastro numeran distinto que el INE en más de la mitad de los municipios)
- Defunciones por causa de muerte → `ine-api-tempus` (estadística del INE; Sanidad solo publica PDF)
- Padrón, nacimientos, defunciones y migraciones → `ine-api-tempus`
- Índice de precios de vivienda y de alquiler → `ine-api-tempus`
- Población de una entidad singular, núcleo o diseminado (Nomenclátor) → `ine-codigos-territoriales` (POST a nomen2/DescargaTabla por nombre de población (xls o csv), sin clave; la API Tempus no baja del municipio)
- PIB municipal, contabilidad trimestral y defunciones por barrio de la Comunidad de Madrid → `comunidad-madrid-estadistica-api` (no está en el INE; municipios con código INE de 5 dígitos)
- Estadística oficial de Cataluña por municipio, comarca o sección censal (padrón, renta, PIB, afiliación) → `idescat-api` (municipios con 6 dígitos (INE más dígito de control); el INE de 5 se ignora y devuelve todos sin error)
- Ficha resumen de un municipio catalán (población, renta, paro, vivienda) en una llamada → `idescat-api` (EMEX; la población es la del Censo anual, no la del padrón)
- Población por municipio andaluz desde 1996 y estadística propia del IECA → `ieca-api-badea` (los filtros usan ids internos de miembro, no años ni códigos INE)
- Indicadores coyunturales por provincia andaluza (IPC, EPA, paro, PIB) → `ieca-api-badea` (INDEA; cada código fija tipo de dato y base)
- Estadísticas por comarca valenciana (pobreza, empresas, industria, cultivos) → `ive-pegv-bancos-datos` (el INE no publica comarcas; comarcas solo por nombre y agrupación nueva desde 2023)

**Contratación pública y subvenciones**
- Licitaciones, adjudicaciones y contratos menores de todas las Administraciones → `placsp-datos-abiertos`
- Contratos adjudicados a una empresa por su NIF, o quién gana los contratos de un órgano → `placsp-datos-abiertos` (sin búsqueda por NIF en la plataforma; almacén local con la tabla placsp_adjudicaciones (guides/almacen.md, herramienta almacen_sql))
- Todo lo público de una empresa o entidad por su NIF (ayudas, si es sector público, prohibiciones de contratar) → `bdns-api` (herramienta empresa_nif del MCP o consulta.empresa_nif (BDNS, AEI, Invente y prohibiciones por denominación); contratos y BORME salen solo del almacén local (guides/almacen.md))
- Convocatorias y concesiones de subvenciones, ayudas de Estado, minimis, grandes beneficiarios → `bdns-api`
- Empresas clasificadas para contratar (ROLECE) → `hacienda-registro-licitadores` (solo con certificado electrónico)
- Prohibiciones de contratar vigentes → `hacienda-registro-licitadores` (XML público del visor del ROLECE; el NIF va oculto, cruzar por nombre)

**Empleo y Seguridad Social**
- Paro registrado, demandantes y contratos por municipio → `sepe-estadisticas` (ESTADISTICA_MUNICIPIOS.xls con código INE en municipios/{AAAA}/{mes}.html; municipios-20-45 es otra tabla)
- Afiliación a la Seguridad Social por régimen, actividad, provincia y municipio → `segsocial-estadisticas` (municipal en MUNCNAE{MM}{AA}.xlsx con URL fija; «<5» como texto y municipio sin cero inicial)
- Pensiones contributivas e Ingreso Mínimo Vital → `segsocial-estadisticas` (el IMV tiene sección propia con nóminas por CCAA y provincia; no está en otras prestaciones (EST45))
- Muestra Continua de Vidas Laborales → `segsocial-estadisticas` (no se descarga; se solicita bajo convenio)
- Convenios colectivos (REGCON), huelgas, accidentes de trabajo, regulación de empleo → `mites-estadisticas` (REGCON exporta todas las filas de una búsqueda en SpreadsheetML (?_exportarExcelPublicoXML=1))
- Extranjeros con autorización de residencia y afiliados extranjeros → `segsocial-estadisticas` (afiliados extranjeros en EST292; las estadísticas de extranjería del Ministerio de Inclusión no están aún en el catálogo)

**Gobierno abierto, transparencia y organización administrativa**
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

**Territorio, catastro y cartografía**
- Datos de un inmueble o parcela por referencia catastral, dirección o coordenadas → `catastro-ovc` (bloqueo por IP tras ráfagas de unas 15 peticiones)
- Parcelario, edificios y direcciones vectoriales por municipio (INSPIRE) → `catastro-ovc`
- Ortofotos PNOA, modelos del terreno, LiDAR y límites municipales → `cnig-centro-descargas` (descargas con reCAPTCHA; WMS, WMTS y WFS sin restricción)
- Geocodificar una dirección y obtener su código INE → `cnig-centro-descargas` (geocoder CartoCiudad; find ignora municipio_filter y no avisa si el portal no existe, elegir antes con candidates)
- Geometría de secciones censales, distritos y municipios por año → `ine-cartografia-censal` (shapefile anual o API OGC del INE con filtro CQL; límites municipales del IGN sin reCAPTCHA en api-features.ign.es (idee-servicios))
- Localizar cualquier servicio WMS, WFS o CSW de una Administración → `idee-servicios`
- Carreteras y ferrocarril oficiales en vectorial → `idee-servicios` (GeoJSON en api-features.idee.es (roadlink, railwaylink); el WFS transportes de servicios.idee.es solo da GML)
- Ríos, embalses y cuencas en vectorial → `idee-servicios` (GeoJSON en api-features.idee.es (watercourse); el WFS hidrografia da GML)
- Ocupación del suelo SIOSE por polígono → `idee-servicios` (110 millones de polígonos en el WFS ocupacion-suelo; sin count no responde)
- Altitud o modelo digital del terreno de una zona → `idee-servicios` (WCS mdt con GetCoverage y SUBSET devuelve GeoTIFF; WMTS mdt para visualizar)
- Buscar un topónimo → `idee-servicios` (api-features.ign.es/collections/namedplace/items?etiqueta={nombre} en GeoJSON; el geocoder de direcciones está en cnig-centro-descargas)

**Meteorología y clima**
- Predicción, observación, climatología, avisos y radar → `aemet-opendata` (clave gratuita obligatoria; el cuerpo vacío con 200 es fallo de autenticación)
- Proyecciones de cambio climático y series centenarias → `aemet-otros-servicios` (proyecciones AR5 y rejilla diaria de 5 km en tar.gz; desde IP de centro de datos llegaron vacíos)

**Medio ambiente, agua y biodiversidad**
- Calidad del aire validada por estación y contaminante → `miteco-calidad-aire` (datos anuales validados; el tiempo real lo sirve cada comunidad autónoma, fuera del alcance)
- Emisiones industriales por complejo (PRTR) → `miteco-prtr`
- Reserva de embalses, caudales y estaciones de aforo → `miteco-saih-boletin-hidrologico`
- Red Natura 2000, espacios protegidos, hábitats, humedales, inventario forestal → `miteco-banco-datos-naturaleza` (descargas con desafío ALTCHA (resuelto en la guía); los WMS de mapama están rotos)
- Emisiones de gases de efecto invernadero y contaminantes atmosféricos por sector (inventario nacional) → `miteco-inventario-emisiones` (por categoría IPCC; por instalación en miteco-prtr)

**Energía**
- Precios de carburantes por gasolinera → `minetur-precios-carburantes`
- Serie diaria de precios de una gasolinera o de un municipio → `minetur-precios-carburantes` (histórico día a día desde 2007 (EstacionesTerrestresHist, 12 MB al día el nacional); el almacén local lo guarda por estación y día (guides/almacen.md))
- Comercializadoras, cambios de suministrador, bono social, garantías de origen → `cnmc-data`
- Consumo de productos petrolíferos y gas por provincia, balances energéticos → `miteco-energia-estadisticas` (series de CORES en xlsx; el ministerio publica PDF)
- Demanda, generación por tecnología, PVPC y precio spot horarios → `ree-redata` (WAF intermitente; reintentar; ESIOS exige token)
- Precio marginal del mercado diario e intradiario, curvas y programas de casación → `omie-mercado` (ficheros de texto por día; 96 periodos cuarto-horarios en 2026)
- Registro de instalaciones de producción eléctrica y autoconsumo → `miteco-energia-estadisticas` (no localizada descarga abierta; PRETOR da 404)
- Telecomunicaciones (líneas, operadores, audiovisual) → `cnmc-data`

**Sanidad y medicamentos**
- Medicamentos, presentaciones, fichas técnicas y problemas de suministro → `aemps-cima-api` (sin precios; precios y financiación en sanidad-nomenclator-facturacion)
- Precios, financiación y aportación de medicamentos (nomenclátor de facturación) → `sanidad-nomenclator-facturacion`
- Ensayos clínicos (REEC) y alertas de seguridad → `aemps-otros-registros` (sin API documentada; buscador JSON por GET (arise/search), detalle por POST con cookie y alertas en la API REST de WordPress)
- Exceso de mortalidad (MoMo), COVID-19, boletines epidemiológicos, gripe → `isciii-cne`
- Hospitales, altas hospitalarias e indicadores del Sistema Nacional de Salud → `sanidad-portal-estadistico` (Catálogo de Hospitales en xlsx; cubos exportables a CSV por POST de WebForms; Indicadores Clave en JSON (export/data))

**Ciencia e investigación (biología, química, geología, oceanografía)**
- Presencia de especies (ocurrencias, datasets de biodiversidad) → `gbif-es`
- Ayudas de investigación concedidas por la AEI → `aei-convocatorias`
- Publicaciones científicas en acceso abierto → `csic-digital` (OAI-PMH; RECOLECTA (fecyt-recolecta) ya no expone OAI)
- Producción científica española por CCAA y país (Scopus, WoS) y percepción social de la ciencia → `fecyt-recolecta` (CSV y xlsx en indicadores.fecyt.es/data/; icono.fecyt.es ya no resuelve)
- Geología, hidrogeología, puntos de agua y minería → `igme-geologia`
- Terremotos recientes y catálogo sísmico → `ign-sismologia` (GeoJSON de 30 días en el JavaScript del visor (todos_visualizadores.js); catálogo por script imitando al navegador)
- Campañas oceanográficas y datasets del IEO (catálogo de metadatos) → `ieo-datos-oceanograficos` (solo catálogo (CSW y Elasticsearch); los datos se piden en SeaDataNet y erddap.ieo.es no resuelve)

**Agricultura, pesca y alimentación**
- Beneficiarios de la PAC → `fega-beneficiarios-pac` (FEGA cierra la conexión desde IP de centros de datos (30/09 y 01/10/2026); parte de los pagos directos está en bdns-api como convocatorias autonómicas, con cobertura desigual)
- Recintos agrícolas, usos del suelo y referencia catastral rústica → `mapa-sigpac`
- Anuario de estadística agraria, precios percibidos y pagados, consumo alimentario → `mapa-estadisticas-agrarias`
- Flota pesquera, capturas y acuicultura → `mapa-pesca` (el identificador de buque es CODIGOBUQUE, no el CFR)
- Superficie por cultivo y comunidad autónoma (ESYRCE) → `mapa-estadisticas-agrarias` (xlsx anual desde 2022; microdatos solo previa solicitud en sede electrónica)

**Transporte y movilidad**
- Datos oceanográficos en tiempo real (oleaje, mareas, boyas) → `puertos-estado-datos` (API interna de Portus sin documentar y sin clave (ubicaciones, mareas previstas, último dato por POST))
- Incidencias de tráfico, detectores, radares, zonas de bajas emisiones, puntos de recarga → `dgt-datex-trafico`
- Matriculaciones, bajas, parque de vehículos y conductores (microdatos) → `dgt-estadisticas` (no localizados microdatos de accidentes, solo tablas; los listados de bajas acaban en 2024-06)
- Matrices origen-destino de movilidad por telefonía móvil → `mitma-opendata-movilidad` (el host de datos respondió 403 desde el entorno de verificación)
- Horarios de trenes (GTFS), estaciones con coordenadas y posiciones en tiempo real → `renfe-datos-abiertos` (GTFS-RT con fallos TLS intermitentes, reintentar; Adif sin portal localizado)
- Tráfico portuario mensual por autoridad portuaria → `puertos-estado-datos`
- Tráfico aéreo mensual por aeropuerto, autopistas de peaje, ferrocarril, licitación y adjudicación de obra → `mitma-boletin-estadistico-online` (XLS con URL fija pero solo el total y 16 aeropuertos, sin otras clases de tráfico; la red completa de Aena en aesa-aviacion)
- Registro de aeronaves y operadores de drones → `aesa-aviacion` (matrículas activas en un PDF de AESA; operadores UAS sin listado público)

**Comercio exterior, industria y propiedad industrial**
- Comercio exterior por producto TARIC, país y provincia desde 1995 → `datacomex` (API verificada con cuenta gratuita; códigos de país numéricos, no ISO)
- Inversión extranjera en España y española en el exterior → `datainvex` (aplicación ASP.NET con viewstate; sin API)
- Estadísticas de industria, series BADASE y datos turísticos (DATAESTUR) → `mincotur-industria-turismo` (la API de DATAESTUR respondió sin clave pero con 504 frecuentes; reintentar)
- Patentes, marcas y Boletín de la Propiedad Industrial → `oepm-invenes` (bloqueado por el cortafuegos de la OEPM desde el entorno de verificación)

**Educación y universidades**
- Alumnado, profesorado y centros no universitarios → `educacion-estadisticas-ruct` (EDUCAbase con el patrón PC-Axis del INE)
- Universidades, matriculados y egresados por titulación, títulos oficiales (RUCT) → `educacion-estadisticas-ruct`
- Microdatos de PISA, TIMSS o PIAAC de España → `inee-bases-datos` (muestra española en rar o zip con SPSS y Stata; HEAD responde 403, usar GET con Range)

**Justicia, interior y seguridad**
- Criminalidad por tipología, comunidad, provincia y municipio → `interior-criminalidad` (balances acumulados desde enero; código INE de municipio solo desde 2024)
- Detenciones, victimizaciones y hechos esclarecidos por provincia, sexo y edad → `interior-criminalidad` (series anuales PC-Axis 2010-2025 en /Datos2/, /Datos3/ y /Datos4/)

**Cultura y patrimonio**
- Estadísticas culturales (empleo cultural, bibliotecas, museos, cine, bono cultural) → `cultura-culturabase` (PC-Axis con el patrón de descarga del INE; CSV en UTF-8 con BOM aunque la cabecera diga ISO-8859-15)
- Catálogo bibliográfico de la BNE y patrimonio digital (Hispana) → `bne-datos` (datos.bne.es bloqueado desde el entorno; Hispana por OAI-PMH)

**Demografía, migraciones y sociedad**
- Feminicidios por comunidad autónoma, provincia, año y mes → `igualdad-estadisticas-violencia-genero` (API Saiku sin clave; crear consulta MDX y exportar CSV; territorios por nombre, sin código INE)
- Llamadas al 016 por provincia y mes → `igualdad-estadisticas-violencia-genero` (cubo 040 Servicio 016 con medidas de llamadas, WhatsApp, correo y chat)
- Casos activos en VioGén y órdenes de protección → `igualdad-estadisticas-violencia-genero` (cubos 090 y 120; el origen es Interior y el CGPJ)
- Dependencia (SAAD): solicitudes, dictámenes, prestaciones por grado y CCAA, lista de espera → `imserso-dependencia` (xlsx mensual estsisaad_{AAAAMMDD} con URL deducible; la encuesta EDAD es del INE)
- Personas con discapacidad reconocida por provincia, sexo, edad y grado → `imserso-dependencia` (BEDPCD en CSV largo 2019-2024 (bdepcd_2024-1-))
- Pensiones no contributivas por provincia → `imserso-dependencia` (csv y xlsx sobreescritos cada mes; las contributivas están en segsocial-estadisticas)
- Microdatos de un barómetro o encuesta del CIS → `cis-estudios` (MD{n}.zip sin registro desde contentUrl del JSON-LD de la página del estudio; el catálogo es JavaScript con anti-bot, enumerar por sitemap.xml)
- Serie de estimación de voto del CIS → `cis-estudios` (solo PDF {n}_Estimacion.pdf por barómetro; las series web cargan por JavaScript sin API localizada)
- Indicadores de igualdad por sexo (empleo, salarios, poder, salud) → `inmujeres-mujeres-cifras` (un xls por indicador en inmujeres.gob.es aunque el HTML enlace al host antiguo inmujer.es)

**Vivienda y urbanismo**
- Precios de vivienda, transacciones, alquiler (SERPAVI) y suelo → `mivau-precios-vivienda-alquiler`

**Telecomunicaciones y sociedad digital**
- Cobertura de fibra, HFC y 5G por municipio → `mtdfp-cobertura-banda-ancha` (fracciones 0-1 por hogares o por viviendas, no comparables entre bases; la CNMC da líneas, no cobertura)

**Consumo y seguridad alimentaria**
- Alertas alimentarias, registro sanitario de empresas alimentarias y laboratorios → `aesan-alertas-registros` (alertas solo en HTML; sin RSS ni API localizados)

**Sin fuente en el catálogo**
- Si una fuente se puede usar en un producto comercial, cómo citarla y qué hacer con sus datos personales → ninguna (guides/reutilizacion.md, con las normas leídas en el BOE; la licencia de cada fuente está en el campo license de su ficha)
- Cotizaciones bursátiles y precios de mercado (BME, OMIE) → ninguna (BME es privado y queda fuera del alcance; el precio de la electricidad de OMIE está en omie-mercado)
- Deudores con Hacienda de más de 600.000 € (lista del artículo 95 bis LGT) → ninguna (la AEAT la publica en su sede en junio y por ley deja de ser accesible a los tres meses y no debe indexarse; el 01/10/2026 la de 2026 ya daba 404)
- Concursos de acreedores de una empresa por NIF → ninguna (publicidadconcursal.es busca por NIF pero exige resolver un CAPTCHA (no automatizable); los edictos de los juzgados de lo mercantil salen en la sección IV del BOE, sin búsqueda por NIF en la API)
- Estadística judicial y sentencias → ninguna (Poder Judicial (CGPJ, CENDOJ) fuera del alcance actual)
- Ayuda oficial al desarrollo y acción exterior → ninguna (sin fuente en el catálogo todavía)
- Extranjeros con certificado de registro o tarjeta de residencia, autorizaciones y protección internacional → ninguna (Observatorio Permanente de la Inmigración en inclusion.gob.es; el host respondió 403 (Akamai) a IP de centro de datos el 2026-09-30; verificar desde otra red)
- Población empadronada por código postal en la Comunitat Valenciana → ninguna (el IVE la muestra solo en Tableau Public; sin descarga estructurada localizada el 2026-10-01)

## Identificadores para cruzar datos

| id | formato | regex | ejemplo | emisor | lo usan |
|---|---|---|---|---|---|
| ine-municipio | 5 dígitos, provincia (2) + municipio (3); algunos ficheros añaden un sexto dígito de control | `^\d{5}$` | 28079 | ine-codigos-territoriales | cis-estudios, segsocial-estadisticas, sepe-estadisticas, comunidad-madrid-estadistica-api, idescat-api, ieca-api-badea, ine-codigos-territoriales, ive-pegv-bancos-datos, ayuntamiento-madrid-datos-abiertos, comunidad-madrid-datos-abiertos, gencat-dades-obertes, gva-dadesobertes-api, junta-andalucia-datos-abiertos, hacienda-ovef, interior-criminalidad, miteco-calidad-aire, aemet-opendata, sanidad-portal-estadistico, mtdfp-cobertura-banda-ancha, catastro-ovc, cnig-centro-descargas, idee-servicios, ine-cartografia-censal, dgt-estadisticas, mitma-opendata-movilidad, mivau-precios-vivienda-alquiler |
| ine-provincia | 2 dígitos, 01 a 52 | `^(0[1-9]|[1-4]\d|5[0-2])$` | 28 | ine-codigos-territoriales | mapa-sigpac, datacomex, cis-estudios, segsocial-estadisticas, minetur-precios-carburantes, miteco-energia-estadisticas, idescat-api, ieca-api-badea, ine-codigos-territoriales, ine-microdatos, dir3-directorio, gva-dadesobertes-api, aeat-estadisticas, hacienda-ovef, miteco-calidad-aire, aemps-otros-registros, isciii-cne, sanidad-portal-estadistico, mtdfp-cobertura-banda-ancha, catastro-ovc, cnig-centro-descargas, idee-servicios, ine-cartografia-censal, dgt-estadisticas, mivau-precios-vivienda-alquiler |
| ine-entidad-singular | 11 dígitos, municipio INE (5) + entidad colectiva (2) + entidad singular (2) + núcleo o diseminado (2) | `^\d{11}$` | 01001000100 | ine-codigos-territoriales | ine-codigos-territoriales, mtdfp-cobertura-banda-ancha, idee-servicios |
| ccaa | 2 dígitos, 01 Andalucía a 19 Melilla, en el orden del INE | `^(0[1-9]|1\d)$` | 13 | ine-codigos-territoriales | educacion-estadisticas-ruct, ine-codigos-territoriales, ine-microdatos, aeat-estadisticas, aemps-otros-registros, isciii-cne, sanidad-portal-estadistico, mtdfp-cobertura-banda-ancha, cnig-centro-descargas, idee-servicios, ine-cartografia-censal, mivau-precios-vivienda-alquiler |
| nuts | ES más 1 a 3 caracteres (ES1, ES11, ES111) | `^ES[1-7]\d{0,2}$` | ES300 | — | placsp-datos-abiertos, comunidad-madrid-estadistica-api, mtdfp-cobertura-banda-ancha, idee-servicios, ine-cartografia-censal |
| seccion-censal | 10 dígitos, municipio (5) + distrito (2) + sección (3) | `^\d{10}$` | 2807901001 | ine-cartografia-censal | idescat-api, ayuntamiento-barcelona-datos-abiertos, ayuntamiento-madrid-datos-abiertos, ine-cartografia-censal, mivau-precios-vivienda-alquiler |
| referencia-catastral | 14 caracteres alfanuméricos (parcela) o 20 (inmueble, con 4 dígitos y 2 letras de control) | `^[0-9A-Z]{14}(\d{4}[A-Z]{2})?$` | 9872023VH5797S0001WX | catastro-ovc | mapa-sigpac, gva-dadesobertes-api, catastro-ovc, cnig-centro-descargas |
| referencia-sigpac | provincia:municipio:agregado:zona:polígono:parcela:recinto, números separados por dos puntos | `^\d{1,2}:\d{1,3}:\d+:\d+:\d+:\d+:\d+$` | 28:15:0:0:3:9000:6 | mapa-sigpac | mapa-sigpac |
| idema | 4 o 5 caracteres alfanuméricos | `^[0-9A-Z]{4,5}$` | 3195 | aemet-opendata | aemet-opendata |
| nif | DNI (8 dígitos y letra), NIE (X, Y o Z, 7 dígitos y letra) o NIF de persona jurídica (letra, 7 dígitos y control) | `^(\d{8}[A-Z]|[XYZ]\d{7}[A-Z]|[A-HJ-NP-SUVW]\d{7}[0-9A-J])$` | Q1132001G | — | fega-beneficiarios-pac, aei-convocatorias, bdns-api, placsp-datos-abiertos, ayuntamiento-barcelona-datos-abiertos, dir3-directorio, face-facturas, gencat-dades-obertes, gva-dadesobertes-api, junta-andalucia-datos-abiertos, igae-ejecucion-presupuestaria |
| dir3 | letra (E, L, A, U, I) y 8 dígitos, o dos letras (LA, EA) y 7 dígitos | `^([A-Z]\d{8}|[A-Z]{2}\d{7})$` | E00003901 | dir3-directorio | placsp-datos-abiertos, ayuntamiento-madrid-datos-abiertos, datos-gob-es-api, dir3-directorio, face-facturas, gencat-dades-obertes, pag-administracion-gob-es, transparencia-portal, igae-ejecucion-presupuestaria |
| sia | 6 o 7 dígitos | `^\d{6,7}$` | 010170 | pag-administracion-gob-es | pag-administracion-gob-es |
| invente | INV y 8 dígitos, código del Inventario de Entes del Sector Público | `^INV\d{8}$` | INV00000102 | igae-ejecucion-presupuestaria | bdns-api, igae-ejecucion-presupuestaria |
| bdns | 6 dígitos | `^\d{6}$` | 800000 | bdns-api | bdns-api, gencat-dades-obertes |
| cpv | 8 dígitos, opcionalmente guion y dígito de control | `^\d{8}(-\d)?$` | 45000000-7 | — | placsp-datos-abiertos, gva-dadesobertes-api |
| cnae | sección (letra A a U) o 2 a 4 dígitos (división, grupo, clase); algunas fuentes escriben la clase con punto (20.14) | `^([A-U]|\d{2,4}|\d{2}\.\d{1,2})$` | 4711 | — | mites-estadisticas, segsocial-estadisticas, sepe-estadisticas, miteco-prtr |
| codigo-convenio | 14 dígitos | `^\d{14}$` | 42000085011981 | mites-estadisticas | mites-estadisticas |
| cn-medicamento | 6 dígitos | `^\d{6}$` | 708201 | aemps-cima-api | aemps-cima-api, sanidad-nomenclator-facturacion |
| boe-id | BOE-A-AAAA-NNNNN (disposición), BOE-B-AAAA-NNNNN (anuncio), BORME-A-AAAA-NNN-PP (PP código de provincia) | `^(BOE-[ABC]-\d{4}-\d{1,6}|BORME-[ABC]-\d{4}-\d{1,5}(-\d{2})?)$` | BOE-A-1978-31229 | boe-api-sumario | boe-api-legislacion-consolidada, boe-api-sumario, boe-eli, borme-api-sumario |
| eli | URI https://www.boe.es/eli/es/{tipo}/{AAAA}/{MM}/{DD}/{num} con sufijo /con (consolidado) o /dof (publicado) | `^https://www\.boe\.es/eli/es(-[a-z]{2})?/[a-z]+/\d{4}/\d{2}/\d{2}/[^/]+(/(con|dof))?$` | https://www.boe.es/eli/es/lo/2018/12/05/3/con | boe-eli | gencat-dades-obertes, boe-api-legislacion-consolidada, boe-eli |
| referencia-aei | prefijo de convocatoria, año o número y sufijos separados por guiones (PID2022-136883OB-C22, RYC-2008-03681) | `^[A-Z]{2,6}(-[A-Z]{1,4})?-?\d{2,6}(-[0-9A-Z]+)+$` | RYC-2008-03681 | aei-convocatorias | aei-convocatorias, csic-digital |

**ine-municipio**
- trampa: cargar siempre como texto; como entero pierde el cero inicial de Álava a Barcelona (01 a 08)
- vía `cnig-centro-descargas`: nombre o dirección a código INE con el geocoder CartoCiudad (muniCode)
- vía `catastro-ovc`: código catastral (locat) a INE (loine) con ObtenerMunicipios
- vía `aemet-opendata`: las predicciones por municipio se piden con el INE de 5 dígitos sin dígito de control
- vía `minetur-precios-carburantes`: sin equivalencia; Listados/Municipios usa IDMunicipio propio y solo comparte IDProvincia (INE)
- vía `sanidad-portal-estadistico`: el Catálogo de Hospitales lo guarda con dígito de control (6 dígitos)
- vía `ine-cartografia-censal`: CUMUN en el shapefile de secciones censales; disolver por CUMUN da el contorno municipal del año
- vía `interior-criminalidad`: prefijo de 5 dígitos en la columna Geografía de la tabla municipal desde 2024 (antes solo el nombre)
- vía `mivau-precios-vivienda-alquiler`: CUMUN como texto en el xlsx de SERPAVI y CodINE en su GeoJSON municipal (allí CUMUN es entero)
- vía `segsocial-estadisticas`: COD MUNICIPIO de MUNCNAE{MM}{AA}.xlsx, entero sin cero inicial; rellenar a cinco dígitos
- vía `sepe-estadisticas`: código como número (28001.0) en ESTADISTICA_MUNICIPIOS.xls
- vía `ine-api-tempus`: el filtro tv=19 pide el Id interno, no el código (02001 es tv=19:6124); columna ine_tempus_id de datos/municipios.csv
- vía `dir3-directorio`: el ayuntamiento es L01 + INE + dígito de control (L01280796); su NIF no se deduce del código (Vitoria P0106800F), está en datos/municipios.csv

**ine-provincia**
- trampa: Ceuta 51 y Melilla 52; el ISO 3166-2 (provincia_iso en los CSV COVID del ISCIII) es otro sistema
- vía `minetur-precios-carburantes`: IDProvincia coincide con el código INE
- vía `dir3-directorio`: catálogo de provincias con idElemento 427

**ine-entidad-singular**
- trampa: los cinco primeros dígitos son el código INE de municipio; el Nomenclátor del INE lo muestra en tres pares (colectiva, singular, núcleo) tras provincia y municipio
- vía `ine-codigos-territoriales`: búsqueda por nombre en nomen2/tabla.do (POST) con población por sexo, edad o nacionalidad desde 2000; completo en Nacional_{AAAA}.zip
- vía `mtdfp-cobertura-banda-ancha`: columna Código ESP de la hoja ES del fichero de cobertura 2013-2020 (61.818 entidades)
- vía `idee-servicios`: codine en api-features.ign.es/collections/nuc, con polígono y habitantes

**ccaa**
- trampa: el orden no es alfabético ni el de Eurostat (NUTS2 ES11...); Hacienda (deuda viva, parámetro CCAA de CONPREL) numera distinto de 10 a 17 (Extremadura 10, Madrid 12)
- vía `isciii-cne`: MoMo usa cod_ine_ambito con este código para ambito ccaa, como entero sin cero inicial (1, no 01)
- vía `cis-estudios`: CCAA del CIS coincide salvo 7 y 8, intercambiados (7 Castilla-La Mancha, 8 Castilla y León)
- vía `educacion-estadisticas-ruct`: idComunidad del Registro de Centros (01 a 19) y prefijo de la columna territorial de EDUCAbase (01 ANDALUCÍA)
- vía `aemps-otros-registros`: los centros de cada estudio del REEC traen CCAA y provincia del INE como enteros sin cero inicial (9 Cataluña, 8 Barcelona)
- vía `minetur-precios-carburantes`: IDCCAA propio, con 07 y 08 intercambiados respecto al INE; el resto coincide
- vía `ieca-api-badea`: C01 a C18 en BADEA, con C07 Castilla-La Mancha y C08 Castilla y León como en MINETUR

**nuts**
- trampa: NUTS3 coincide con la provincia salvo islas, Ceuta y Melilla; lo emite Eurostat, no hay fuente en el catálogo
- vía `placsp-datos-abiertos`: CountrySubentityCode (NUTS-2021) en RealizedLocation de cada licitación
- vía `idee-servicios`: codnut1 a codnut3 en api-features.ign.es/collections/administrativeunit
- vía `ine-cartografia-censal`: CNUT0 a CNUT3 por sección; concatenados dan el NUTS3 (ES + 2 + 1 + 1 = ES211)
- vía `mtdfp-cobertura-banda-ancha`: campo nuts de las capas ArcGIS de cobertura

**seccion-censal**
- trampa: las secciones se redibujan cada año; usar la geometría del mismo año que el dato
- vía `ine-cartografia-censal`: geometría anual con CUSEC (sección), CUDIS (distrito) y CUMUN (municipio)
- vía `ine-api-tempus`: renta por sección en el Atlas de distribución de renta (operación del INE)
- vía `mitma-opendata-movilidad`: zonificación por distritos y municipios de los estudios de movilidad (host no verificable)
- vía `mivau-precios-vivienda-alquiler`: CUSEC en la hoja Secciones censales del xlsx de SERPAVI (alquiler de 2011 a 2024)

**referencia-catastral**
- trampa: los códigos de municipio del Catastro son propios, no INE
- vía `catastro-ovc`: coordenadas a referencia con Consulta_RCCOOR; datos del inmueble con Consulta_DNPRC
- vía `mapa-sigpac`: parcela SIGPAC a referencia catastral de 14 caracteres con refcatparcela
- vía `cnig-centro-descargas`: refCatastral de 14 caracteres en los portales del geocoder de CartoCiudad

**referencia-sigpac**
- trampa: la provincia es la del INE, pero el municipio es el del Catastro (capitales 900, Madrid 28:900 frente al INE 28079, y otros 4.448 con número distinto); polígono y parcela coinciden con Catastro en rústica
- vía `mapa-sigpac`: coordenadas a recinto con refrecinbycoord; recinto a Red Natura o nitratos con intersection
- vía `ine-codigos-territoriales`: municipio SIGPAC a INE con datos/municipios.csv (columna sigpac), emparejado por nombre con codigossigpac/municipio{pr}.json y contrastado por punto

**idema**
- trampa: las predicciones no usan idema sino el código INE de municipio; inventario en valores/climatologicos/inventarioestaciones

**nif**
- trampa: la letra inicial indica el tipo de entidad (P ayuntamientos, Q organismos autónomos, S órganos de la AGE, G asociaciones); la BDNS ofusca los DNI
- vía `bdns-api`: concesiones/busqueda?nifCif= devuelve las subvenciones del titular
- vía `face-facturas`: relations trae el NIF del órgano gestor (og.identifier) junto a su DIR3
- vía `aei-convocatorias`: columna C.I.F. del CSV de ayudas concedidas
- vía `placsp-datos-abiertos`: cbc:ID con schemeName NIF en los documentos CODICE

**dir3**
- trampa: las unidades cambian con cada reestructuración ministerial; el código antiguo queda extinguido con sucesor
- vía `face-facturas`: nombre a DIR3 y NIF con relations?fulltext=
- vía `datos-gob-es-api`: datasets de un organismo con catalog/dataset/publisher/{dir3}.json
- vía `placsp-datos-abiertos`: cbc:ID con schemeName DIR3 identifica el órgano de contratación
- vía `transparencia-portal`: servicios-buscador/buscar.htm?ente={DIR3} filtra contratos, convenios y retribuciones (admite varios DIR3 separados por coma)

**sia**
- trampa: identifica el procedimiento, no el organismo; es texto con ceros a la izquierda (210 de los 7161 de la AGE), como número deja de cruzar
- vía `pag-administracion-gob-es`: Listado Codigos SIA {nivel}.xlsx del CTT da el DIR3 del departamento y del centro directivo de cada procedimiento

**invente**
- trampa: el listado da fechaAlta en dd/mm/aaaa y la ficha en ISO; 2.057 de 4.801 entes no tienen DIR3
- vía `igae-ejecucion-presupuestaria`: EntidadesSPI_ConFiltros?nif= o ?codDir3= de la API de INVENTE devuelve CodigoInvente
- vía `bdns-api`: codigoInvente en las convocatorias y concesiones (INV00000095 es la AECID)

**bdns**
- trampa: es la clave estable de la convocatoria; el título varía y los extractos en el BOE lo citan
- vía `bdns-api`: convocatorias?numConv= para el detalle; concesiones/busqueda?numeroConvocatoria= para sus concesiones

**cpv**
- trampa: vocabulario europeo; en CODICE va en cbc:ItemClassificationCode
- vía `boe-feeds`: RSS de anuncios de licitación por división CPV (canal_cpv.php)

**cnae**
- trampa: CNAE 2025 sustituye a CNAE 2009 desde 2026 en Seguridad Social y REGCON; no encadenar series sin recodificar
- vía `segsocial-estadisticas`: afiliación por CNAE a dos dígitos (EST305) y en MUNCNAE (COD CNAE como número)
- vía `mites-estadisticas`: REGCON filtra con idCnaesBusqueda, ids internos del desplegable (la división 56 es 28 en CNAE 2009 y 1676 en CNAE 2025)
- vía `miteco-prtr`: CNAE-2009 con punto (20.14) en el inventario de complejos; quitar el punto para cruzar con 4 dígitos
- vía `sepe-estadisticas`: divisiones CNAE como columnas ('00' a '99') en los xls de paro y contratos por actividad

**codigo-convenio**
- trampa: se consulta en REGCON con codigoConvenio; un mismo código agrupa todos los trámites del convenio (31 para la hostelería de Soria)

**cn-medicamento**
- trampa: identifica la presentación; el nregistro identifica el medicamento
- vía `aemps-cima-api`: medicamento?cn= devuelve el nregistro y todas las presentaciones; psuministro lista problemas por cn
- vía `sanidad-nomenclator-facturacion`: precio de venta, precio de referencia, aportación y agrupación homogénea por Código Nacional (solo financiados)

**boe-id**
- trampa: el número no lleva ceros a la izquierda (BOE-A-2024-87)
- vía `boe-api-legislacion-consolidada`: /id/{boe-id}/metadatos devuelve url_eli y vigencia
- vía `boe-api-sumario`: xml.php?id= devuelve el texto completo

**eli**
- trampa: el sufijo cambia la versión, no la norma; sin sufijo equivale a dof
- vía `boe-api-legislacion-consolidada`: url_eli en los metadatos de cada norma

**referencia-aei**
- trampa: una referencia se repite en varias filas o entidades (agrupar antes de sumar importes); la BDNS no la trae
- vía `csic-digital`: dc:relation info:eu-repo/grantAgreement/AEI/{plan}/{referencia}/ de los registros OAI-PMH; normalizar los guiones U+2010

## Códigos que son parámetros

Valores que una API exige y no se adivinan (ids internos, códigos numéricos, indicativos). Obtenidos con una llamada real en la fecha indicada; la lista completa se saca con la llamada que cita cada grupo.

**ine-operaciones** · `ine-api-tempus` · Id o Codigo como {id_o_codigo} en TABLAS_OPERACION, VARIABLES_OPERACION y VALORES_VARIABLEOPERACION; las 112 operaciones con OPERACIONES_DISPONIBLES (verificado 2026-10-01)
- 25=IPC (Índice de Precios de Consumo (IPC)) · 18=IPCA (Índice de Precios de Consumo Armonizado (IPCA)) · 293=EPA (Encuesta de Población Activa (EPA)) · 450=ECP (Estadística Continua de Población) · 72=CP (Cifras de Población) · 22=DPOP (Cifras Oficiales de Población de los Municipios Españoles: Revisión del Padrón Municipal) · 307=MNPN (MNP Estadística de Nacimientos) · 309=MNPD (MNP Estadística de Defunciones) · 424=EMN (Estimación Mensual de Nacimientos) · 23=ECM (Estadística de Defunciones según la Causa de Muerte) · 71=EM (Estadística de Migraciones) · 455=EMCR (Estadística de Migraciones y Cambios de Residencia) · 230=PERE (Estadística del Padrón de la Población Española Residente en el Extranjero) · 15=IPV (Índice de Precios de la Vivienda (IPV)) · 432=IPVA (Índice de Precios de Vivienda en Alquiler) · 40=HPT (Estadística de Hipotecas) · 259=EH (Estadística sobre Ejecuciones Hipotecarias) · 7=ETDP (Estadística de Transmisión de Derechos de la Propiedad) · 125=SM (Estadística de Sociedades Mercantiles) · 13=EPC (Estadística del Procedimiento Concursal) · 26=IPI (Índices de Producción Industrial) · 27=IPRI (Índices de Precios Industriales) · 32=ICM (Índices de Comercio al por Menor) · 303=ETCL (Encuesta Trimestral de Coste Laboral (ETCL)) · 139=EACL (Encuesta Anual de Coste Laboral) · 140=EAES (Encuesta Anual de Estructura Salarial) · 6=ICLA (Índice de Coste Laboral Armonizado) · 155=ECV (Encuesta de Condiciones de Vida (ECV)) · 314=EPF (Encuesta de Presupuestos Familiares (EPF)) · 330=FR (Movimientos Turísticos en Fronteras) · 334=ETR (Encuesta de turismo de residentes) · 238=EOH (Encuesta de Ocupación Hotelera) · 241=EOTR (Encuesta de Ocupación en Alojamientos de Turismo Rural) · 63=IPTR (Índice de Precios de Alojamientos de Turismo Rural) · 237=CNTR2010 (Contabilidad Nacional Trimestral de España: Principales Agregados)

**ine-variables** · `ine-api-tempus` · Filtro tv={variable}:{Id de valor} en DATOS_TABLA; los Id de valor salen de VALORES_VARIABLEOPERACION/{variable}/{operacion} (campo Id, no Codigo) (verificado 2026-10-01)
- 3=Tipo de dato (72 Dato base) · 18=Sexo · 19=Municipios (8.142 valores en la operación 22) · 20=Islas · 34=Tamaño del municipio · 70=Comunidades y Ciudades Autónomas · 115=Provincias · 349=Total Nacional · 762=Grupos ECOICOP (IPC) · 763=Subgrupos ECOICOP (IPC) · 764=Clases ECOICOP (IPC) · 765=Subclases ECOICOP (IPC) · 544=Corrección de efectos (IPC)

**ine-ccaa** · `ine-api-tempus` · code es el código INE de la comunidad; note da el Id del INE para tv=70:{Id} (padrón, IPC y demás operaciones con variable 70) (verificado 2026-10-01)
- 00=Total Nacional (tv=70:16473) · 01=Andalucía (tv=70:8997) · 02=Aragón (tv=70:8998) · 03=Asturias, Principado de (tv=70:8999) · 04=Balears, Illes (tv=70:9000) · 05=Canarias (tv=70:9001) · 06=Cantabria (tv=70:9002) · 07=Castilla y León (tv=70:9003) · 08=Castilla - La Mancha (tv=70:9004) · 09=Cataluña (tv=70:9005) · 10=Comunitat Valenciana (tv=70:9006) · 11=Extremadura (tv=70:9007) · 12=Galicia (tv=70:9008) · 13=Madrid, Comunidad de (tv=70:9009) · 14=Murcia, Región de (tv=70:9010) · 15=Navarra, Comunidad Foral de (tv=70:9011) · 16=País Vasco (tv=70:9012) · 17=Rioja, La (tv=70:9013) · 18=Ceuta (tv=70:9015) · 19=Melilla (tv=70:8995)

**ine-provincias** · `ine-api-tempus` · code es el código INE de la provincia (dos dígitos, también IDProvincia en carburantes e id_prov en DataComex); note da el Id para tv=115:{Id} (verificado 2026-10-01)
- 01=Araba/Álava (tv=115:2) · 02=Albacete (tv=115:3) · 03=Alicante/Alacant (tv=115:4) · 04=Almería (tv=115:5) · 05=Ávila (tv=115:6) · 06=Badajoz (tv=115:7) · 07=Balears, Illes (tv=115:8) · 08=Barcelona (tv=115:9) · 09=Burgos (tv=115:10) · 10=Cáceres (tv=115:11) · 11=Cádiz (tv=115:12) · 12=Castellón/Castelló (tv=115:13) · 13=Ciudad Real (tv=115:14) · 14=Córdoba (tv=115:15) · 15=Coruña, A (tv=115:16) · 16=Cuenca (tv=115:17) · 17=Girona (tv=115:18) · 18=Granada (tv=115:19) · 19=Guadalajara (tv=115:20) · 20=Gipuzkoa (tv=115:21) · 21=Huelva (tv=115:22) · 22=Huesca (tv=115:23) · 23=Jaén (tv=115:24) · 24=León (tv=115:25) · 25=Lleida (tv=115:26) · 26=Rioja, La (tv=115:27) · 27=Lugo (tv=115:28) · 28=Madrid (tv=115:29) · 29=Málaga (tv=115:30) · 30=Murcia (tv=115:31) · 31=Navarra (tv=115:32) · 32=Ourense (tv=115:53) · 33=Asturias (tv=115:33) · 34=Palencia (tv=115:34) · 35=Palmas, Las (tv=115:35) · 36=Pontevedra (tv=115:36) · 37=Salamanca (tv=115:37) · 38=Santa Cruz de Tenerife (tv=115:38) · 39=Cantabria (tv=115:39) · 40=Segovia (tv=115:40) · 41=Sevilla (tv=115:41) · 42=Soria (tv=115:42) · 43=Tarragona (tv=115:43) · 44=Teruel (tv=115:44) · 45=Toledo (tv=115:45) · 46=Valencia/València (tv=115:46) · 47=Valladolid (tv=115:47) · 48=Bizkaia (tv=115:48) · 49=Zamora (tv=115:49) · 50=Zaragoza (tv=115:50) · 51=Ceuta (tv=115:51) · 52=Melilla (tv=115:52)

**datacomex-paises** · `datacomex` · Parámetro pa de ObtenerDatos (3 dígitos, no ISO); los 40 principales destinos de exportación de 2025; la lista completa (292, con marca UE27) la da ObtenerPaises sin token (verificado 2026-10-01)
- nota: 951 y 952 son avituallamiento (combustible y provisiones a buques y aeronaves), no países; la marca UE27 de ObtenerPaises cubre 37 códigos, no sirve para filtrar los 27 Estados
- 001=Francia · 004=Alemania · 010=Portugal · 005=Italia · 006=Reino Unido · 400=Estados Unidos · 003=Países Bajos · 017=Bélgica · 204=Marruecos · 060=Polonia · 052=Turquía · 720=China · 412=México · 039=Suiza · 061=República Checa · 066=Rumanía · 030=Suecia · 009=Grecia · 508=Brasil · 647=Emiratos Árabes Unidos · 007=Irlanda · 732=Japón · 038=Austria · 008=Dinamarca · 064=Hungría · 632=Arabia Saudí · 063=Eslovaquia · 404=Canadá · 208=Argelia · 664=India · 800=Australia · 728=Corea del Sur (Rep. de Corea) · 512=Chile · 220=Egipto · 624=Israel · 388=Sudáfrica · 043=Andorra · 028=Noruega · 951=Avituall.y combust.intercambios comunitarios · 952=Avituallamiento terceros

**aemet-estaciones-capitales** · `aemet-opendata` · Parámetro {idema} en observación por estación y valores climatológicos; una estación por capital de provincia (nombre oficial en name, ciudad en note); las 926 con inventarioestaciones/todasestaciones (verificado 2026-09-30)
- nota: Cuando la capital tiene observatorio y aeropuerto se ha elegido el observatorio urbano salvo Córdoba, Logroño, Bilbao, Burgos, Granada, Málaga, Sevilla, Vitoria y Zaragoza, donde el aeropuerto es la estación de referencia
- 8178D=ALBACETE (Albacete) · 8019=ALICANTE-ELCHE AEROPUERTO (Alicante) · 6297=ALMERÍA (Almería) · 2444=ÁVILA (Ávila) · 4478X=BADAJOZ (Badajoz) · 0201D=BARCELONA, PORT OLÍMPIC (Barcelona) · 1082=BILBAO AEROPUERTO (Bilbao) · 2331=BURGOS AEROPUERTO (Burgos) · 3469A=CÁCERES (Cáceres) · 5973=CÁDIZ (Cádiz) · 8500A=CASTELLÓ - ALMASSORA (Castellón de la Plana) · 4121=CIUDAD REAL (Ciudad Real) · 5402=CÓRDOBA AEROPUERTO (Córdoba) · 1387=A CORUÑA (A Coruña) · 8096=CUENCA (Cuenca) · 0370E=GIRONA (Girona) · 5530E=GRANADA AEROPUERTO (Granada) · 3168D=GUADALAJARA (Guadalajara) · 1024E=DONOSTIA / SAN SEBASTIÁN, IGELDO (Donostia / San Sebastián) · 4605=HUELVA (Huelva) · 9901X=HUESCA (Huesca) · 5270B=JAÉN (Jaén) · 2661=LEÓN, VIRGEN DEL CAMINO (León) · 9771C=LLEIDA (Lleida) · 9170=LOGROÑO, AEROPUERTO (Logroño) · 1518A=LUGO (Lugo) · 3195=MADRID, RETIRO (Madrid) · 6155A=MÁLAGA AEROPUERTO (Málaga) · 7178I=MURCIA (Murcia) · 9262=PAMPLONA (Pamplona) · 1690A=OURENSE (Ourense) · 1249I=OVIEDO (Oviedo) · 2401X=PALENCIA (Palencia) · B228=PALMA, PUERTO (Palma) · C659M=LAS PALMAS DE GRAN CANARIA, PL. DE LA FERIA (Las Palmas de Gran Canaria) · 1484C=PONTEVEDRA (Pontevedra) · 2870=SALAMANCA (Salamanca) · C449C=STA.CRUZ DE TENERIFE (Santa Cruz de Tenerife) · 1111=SANTANDER (Santander) · 2465=SEGOVIA (Segovia) · 5783=SEVILLA AEROPUERTO (Sevilla) · 2030=SORIA (Soria) · 0042Y=TARRAGONA (Tarragona) · 8368U=TERUEL (Teruel) · 3260B=TOLEDO (Toledo) · 8416X=VALENCIA, UPV (Valencia) · 2422=VALLADOLID (Valladolid) · 9091R=VITORIA-GASTEIZ AEROPUERTO (Vitoria-Gasteiz) · 2614=ZAMORA (Zamora) · 9434=ZARAGOZA, AEROPUERTO (Zaragoza) · 5000C=CEUTA (Ceuta) · 6000A=MELILLA (Melilla)

**boe-secciones** · `boe-api-sumario` · Código de seccion en el sumario JSON y parámetro s de los RSS del BOE (boe.php?s=1); vistos en sumarios de 2024 a 2026 (verificado 2026-09-30)
- 1=I. Disposiciones generales · 2A=II. Autoridades y personal. - A. Nombramientos, situaciones e incidencias · 2B=II. Autoridades y personal. - B. Oposiciones y concursos · 3=III. Otras disposiciones · 4=IV. Administración de Justicia · 5A=V. Anuncios. - A. Contratación del Sector Público · 5B=V. Anuncios. - B. Otros anuncios oficiales · 5C=V. Anuncios. - C. Anuncios particulares

**boe-rangos** · `boe-api-legislacion-consolidada` · rango.codigo en el listado y metadatos de legislación consolidada y atributo codigo de rango en el XML de cada disposición; lista de datos-auxiliares/rangos (verificado 2026-09-30)
- 1020=Acuerdo · 1180=Acuerdo Internacional · 1390=Circular · 1070=Constitución · 1510=Decreto · 1480=Decreto Foral Legislativo · 1470=Decreto Legislativo · 1500=Decreto-ley · 1325=Decreto-ley Foral · 1410=Instrucción · 1300=Ley · 1450=Ley Foral · 1290=Ley Orgánica · 1350=Orden · 1340=Real Decreto · 1310=Real Decreto Legislativo · 1320=Real Decreto-ley · 1220=Reglamento · 1370=Resolución

**boe-ambitos** · `boe-api-legislacion-consolidada` · ambito.codigo en legislación consolidada; datos-auxiliares/ambitos (verificado 2026-09-30)
- nota: datos-auxiliares/departamentos devuelve 211 códigos (115 de ministerios históricos) y materias varios miles; secciones y origenes-legislativos responden 404
- 1=Estatal · 2=Autonómico

**carburantes-productos** · `minetur-precios-carburantes` · IDPRODUCTO en FiltroProducto y FiltroProvinciaProducto; en la respuesta cada producto es una clave 'Precio {nombre}' de ListaEESSPrecio; lista con Listados/ProductosPetroliferos (verificado 2026-09-30)
- 1=Gasolina 95 E5 · 23=Gasolina 95 E10 · 24=Gasolina 95 E25 · 25=Gasolina 95 E85 · 20=Gasolina 95 E5 Premium · 3=Gasolina 98 E5 · 21=Gasolina 98 E10 · 4=Gasóleo A habitual · 5=Gasóleo Premium · 6=Gasóleo B · 7=Gasóleo C · 16=Bioetanol · 8=Biodiésel · 17=Gases licuados del petróleo · 18=Gas natural comprimido · 19=Gas natural licuado · 22=Hidrógeno · 9=Fuelóleo bajo índice azufre · 10=Fuelóleo especial · 11=Gasóleo para uso marítimo · 12=Gasolina de aviación · 13=Queroseno de aviación JET_A1 · 14=Queroseno de aviación JET_A2 · 26=Adblue · 27=Diésel renovable · 28=Gasolina renovable · 29=Metanol · 30=Amoniaco · 31=Biogas natural comprimido · 32=Biogas natural licuado

**ree-geo-ids** · `ree-redata` · geo_ids con geo_trunc=electric_system y geo_limit; solo los tres verificados (verificado 2026-09-30)
- nota: Los geo_ids de comunidades autónomas probados el 2026-09-30 no devolvieron datos; no localizada la lista oficial
- 8741=Península · 8742=Canarias · 8743=Baleares

**bde-series** · `bde-estadisticas` · series={code} en favoritas y listaSeries; nombre y frecuencia comprobados en favoritas; lista completa en catalogo_{be|tc|ti|si}.csv (verificado 2026-10-01)
- D_1NBAF472=Euríbor a un año (mensual) · DTCCBCEUSDEUR.B=Dólares estadounidenses por euro (diaria) · DTNPDE2010_P0000P_PS_APU=Deuda PDE del total de AAPP en % del PIB (trimestral) · D_1JA0D000=Paro registrado (mensual desde 1933; MAX solo da las 1000 últimas)

**madrid-distritos** · `ayuntamiento-madrid-datos-abiertos` · COD_DISTRITO como texto en filters del datastore y cod_distrito en la API dinámica; en eDatos del Instituto, 28079_D{2 dígitos} (verificado 2026-10-01)
- nota: lista con datastore_search?resource_id=200076-2-padron-csv&fields=COD_DISTRITO,DESC_DISTRITO&distinct=true
- 1=Centro · 2=Arganzuela · 3=Retiro · 4=Salamanca · 5=Chamartín · 6=Tetuán · 7=Chamberí · 8=Fuencarral-El Pardo · 9=Moncloa-Aravaca · 10=Latina · 11=Carabanchel · 12=Usera · 13=Puente de Vallecas · 14=Moratalaz · 15=Ciudad Lineal · 16=Hortaleza · 17=Villaverde · 18=Villa de Vallecas · 19=Vicálvaro · 20=San Blas-Canillejas · 21=Barajas

**iecm-datasets** · `comunidad-madrid-estadistica-api` · {code} en /statistical-resources/v1.0/datasets/IECM/{code}/~latest.json; el prefijo es la operación; lista completa con datasets.json?limit=1000 y offset (verificado 2026-10-01)
- 054_000001=PIB total y per cápita por rama y municipio · 050_000001=Contabilidad trimestral de la Comunidad de Madrid (oferta) · 012_000032=Nacidos vivos por distrito y barrio de Madrid · 017_000024=Defunciones por distrito y barrio de Madrid · 130_000016=Afiliaciones a la Seguridad Social (mensual)

**idescat-taules** · `idescat-api` · {estadistica}/{nodo}/{tabla} en /taules/v2/{code}/{geo}/data; lista completa navegando desde /taules/v2 (verificado 2026-10-01)
- pmh/446/477=Población por sexo (1998-2025; geo cat, prov, at, com, mun, ac, dis, sec) · pmh/1180/8078=Población por sexo y edad año a año (desde 2014; 2000-2013 en la tabla 1063) · rfdbc/21181/25017=Renta familiar disponible bruta y por habitante (geo cat, at, com, mun) · irpf/4070/3893=IRPF, base imponible y cuota por declarante · afi/8604/8704=Afiliados a la Seguridad Social por residencia y sexo · pibt/21130/24940=PIB trimestral en volumen, oferta, corregido (solo Cataluña)

**idescat-emex** · `idescat-api` · i={code} en /emex/v1/dades.json; todos los ids salen de dades.json?id={municipio de 6 dígitos} (verificado 2026-10-01)
- f171=Población (Censo anual del INE) · f7=Renta familiar disponible bruta por habitante · f242=Paro registrado

**gencat-datasets** · `gencat-dades-obertes` · /resource/{code}.json; lista completa con /api/catalog/v1?domains=analisi.transparenciacatalunya.cat&only=dataset&limit=2000 (verificado 2026-10-01)
- y6fz-g3ff=Registro de entidades jurídicas · ybgg-dgi6=Contratación pública (publicaciones) · s9xt-n979=Concesiones del RAISC · t2h3-cgys=Alojamientos turísticos · n6hn-rmy7=Normativa del DOGC

**ieca-badea-miembros** · `ieca-api-badea` · {alias}={code} en /consulta/{consultaId}; lista completa con /jerarquia/{jerarquiaId}?consultaId={id}&alias={alias} (verificado 2026-10-01)
- 180251=2025 (jerarquía 2 Anual) · 180232=2024 (jerarquía 2 Anual) · 3689=Hombres (jerarquía 22 Sexo) · 3690=Mujeres (jerarquía 22 Sexo)

**indea-indicadores** · `ieca-api-badea` · codIndicador={code} en datosSerie; lista completa con indicadoresList (36 MB) (verificado 2026-10-01)
- IPC2025_COICOP2018n20042=IPC índice general (mensual) · EPAbp2021m2005CNAE2025n22935=EPA tasa de paro (trimestral) · ECPn15972=Población total (trimestral) · CT2024n17646=PIB índice de volumen (trimestral)

**ive-bdt-consultas** · `ive-pegv-bancos-datos` · cons={code} en https://bdt.gva.es/bdt/res_optimo_static.php?cons={code}&idioma=cas&form=csvpunto; lista navegando menuV.php y sel_optimo.php (verificado 2026-10-01)
- C2D3883=Tasa de riesgo de pobreza por comarca (2012-2024) · C1D3402=Indicadores demográficos municipales (2002-2025) · C2V9662=Superficies de cultivo y riego por municipio (2002-2024, 36 MB) · C0D3442=Renta familiar disponible per cápita municipal (2010-2013, miles de euros) · C0D3783=Personal ocupado en la industria por comarca (2008-2024) · C1D4583=Hogares según tamaño por comarca (2014-2020)

**ive-bdo-consultas** · `ive-pegv-bancos-datos` · cons={code} en https://bdo.gva.es/bdo/res_optimo_static.php?cons={code}&idioma=cas&form=csvcoma; se obtiene desde menuV.php?tema={operacion} (verificado 2026-10-01)
- V0308_C1D0355=Empresas activas según tipo por municipio (2017-2025) · V0292_C2D0339=Empresas activas por condición jurídica y tamaño, Comunitat y provincias

**inclasns-ids** · `sanidad-portal-estadistico` · Parámetros areaCode, sex y year de inclasns.sanidad.gob.es/export/data; la lista completa está en los checkbox variableState-{variable}-{id} de main.html (verificado 2026-10-01)
- nota: areaCode no es el código INE (de 30 a 49 sin el 33); los ids de año no son correlativos; nse 71, nsc 79 y nsi 84 son los totales; un año sin dato devuelve data vacío
- 50=España (areaCode) · 30=Andalucía (areaCode; las CCAA siguen el orden del INE de 30 a 49 saltando el 33) · 43=Comunidad de Madrid (areaCode) · 51=Total (sex; 1 hombre, 2 mujer) · 28=Último año disponible (year; responde con el id del año real (92 en esperanza de vida)) · 64=2015 (year) · 89=2020 (year) · 92=2023 (year) · 94=2025 (year)

**aemps-wp-categorias** · `aemps-otros-registros` · categories={code} en www.aemps.gob.es/wp-json/wp/v2/posts; /wp/v2/categories responde 401, el slug sale de class_list y sirve en /category/{slug}/feed/ (verificado 2026-10-01)
- 17=Notas informativas (slug notasinformativas; 1.766 entradas) · 312=Seguridad (slug seguridad-3; 201 entradas (alertas))

## Rutas muertas

URLs de documentación antigua que ya no sirven y su sustituta verificada.

| ruta antigua | estado | sustituta | ficha | nota | comprobada |
|---|---|---|---|---|---|
| https://www.airef.es/es/datalab/ | redirect | https://www.airef.es/es/datalab/datos-economicos/observatorio-de-deuda/ | `airef-datos` | redirige con 301 a /ca/datalab-2/ | 2026-09-30 |
| https://www.airef.es/es/previsiones/ | redirect | https://www.airef.es/es/datalab/previsiones-del-pib-en-tiempo-real/ | `airef-datos` | redirige a las previsiones demográficas de 2018 | 2026-09-30 |
| https://www.cnmv.es/portal/Consultas/Busqueda.aspx | 400 | https://www.cnmv.es/portal/hr/busquedahr.aspx?division=2 | `cnmv-registros` | redirige a la ruta sin .aspx, que responde 400; division 2 es información privilegiada y 3 otra información relevante | 2026-09-30 |
| https://www.cnmv.es/portal/HR/ResultadoBusquedaHR.aspx | 400 | https://www.cnmv.es/portal/hr/busquedahr.aspx?division=3 | `cnmv-registros` | — | 2026-09-30 |
| https://www.cnmv.es/portal/RSS/ | 403 | https://www.cnmv.es/portal/RSS/RSS.asmx/GetDatos?iID=1 | `cnmv-registros` | — | 2026-09-30 |
| https://www.ico.es/web/ico/estadisticas | redirect | — | `ico-datos` | redirige a la portada; el ICO no publica estadísticas descargables | 2026-09-30 |
| https://www.ico.es/web/ico/transparencia | redirect | https://www.ico.es/web/guest/ico/informe-anual | `ico-datos` | — | 2026-09-30 |
| https://www.mites.gob.es/estadisticas/cct/welcome.htm | moved | https://www.mites.gob.es/es/estadisticas/condiciones_trabajo_relac_laborales/CCT/welcome.htm | `mites-estadisticas` | responde 200 con una página de aviso sin datos; igual para /estadisticas/eat/welcome.htm | 2026-09-30 |
| https://administracionelectronica.gob.es/ctt/dir3 | redirect | https://administracionelectronica.gob.es/ctt/verPestanaGeneral.htm?idIniciativa=dir3 | `dir3-directorio` | página de 1,4 KB que redirige por script; /ctt/dir3/descargas va a verPestanaDescargas.htm?idIniciativa=dir3 | 2026-09-30 |
| https://face.gob.es/es/directorio/administraciones | moved | https://proveedores.face.gob.es/api/v1/relations | `face-facturas` | face.gob.es es solo consulta histórica desde el 27/02/2026; la API y el portal viven en proveedores.face.gob.es | 2026-09-30 |
| https://administracion.gob.es/pag_Home/ | redirect | https://administracion.gob.es/ | `pag-administracion-gob-es` | cualquier ruta bajo pag_Home/ redirige o da 404; las nuevas son cortas (/empleopublico/boletin, /ayudas/boletin, /espanaadmon/sia) | 2026-09-30 |
| https://transparencia.gob.es/transparencia/transparencia_Home/index.html | redirect | https://transparencia.gob.es/ | `transparencia-portal` | portal rediseñado; contenidos bajo /publicidad-activa/por-materias/ y /derecho-acceso/ | 2026-09-30 |
| https://www.hacienda.gob.es/es-ES/CDI/Paginas/OVEELL/OVEntidadesLocales.aspx | 404 | https://www.hacienda.gob.es/es-ES/Areas%20Tematicas/Administracion%20Electronica/OVEELL/Paginas/OVEntidadesLocales.aspx | `hacienda-ovef` | — | 2026-09-30 |
| https://www.igae.pap.hacienda.gob.es/sitios/igae/es-ES/Contabilidad/ContabilidadPublica/CPE/EjecucionPresupuestaria/Paginas/imMensualEstado.aspx | 404 | https://www.igae.pap.hacienda.gob.es/sitios/igae/es-ES/Contabilidad/ContabilidadPublica/CPE/EjecucionPresupuestaria/Paginas/imejecucionpresupuesto.aspx | `igae-ejecucion-presupuestaria` | — | 2026-09-30 |
| https://pap.hacienda.gob.es/invente2/ | blocked | https://www.pap.hacienda.gob.es/invente2/pagMenuPrincipalV2.aspx | `igae-ejecucion-presupuestaria` | sin www el proxy recibió 502; con www la raíz /invente2/ da 200 con Acceso Denegado y la API pública está en /Invente2/api | 2026-10-01 |
| https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=resultados&idp=1254734710990 | 404 | https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990 | `ine-codigos-territoriales` | la relación de municipios cuelga de menu=ultiDatos; los xlsx tienen URL fija en daco/daco42/codmun/ | 2026-09-30 |
| https://www.mapama.gob.es/app/descargas/descargafichero.aspx | 404 | https://gis.miteco.gob.es/descargas/app/DescargaFichero | `miteco-banco-datos-naturaleza` | es la URL de los recursos ZIP del catálogo CKAN de MITECO; redirige a descargas-gis-miteco/descargafichero, que da 404 | 2026-09-30 |
| https://www.mapama.gob.es/ | redirect | https://www.miteco.gob.es/ | `miteco-banco-datos-naturaleza` | el dominio antiguo redirige a mapa.gob.es (agricultura); lo ambiental está en miteco.gob.es | 2026-09-30 |
| https://www.miteco.gob.es/es/calidad-y-evaluacion-ambiental/temas/atmosfera-y-calidad-del-aire/calidad-del-aire/evaluacion-datos/datos.html | 404 | https://www.miteco.gob.es/es/calidad-y-evaluacion-ambiental/temas/atmosfera-y-calidad-del-aire/evaluacion-y-datos-de-calidad-del-aire/datos.html | `miteco-calidad-aire` | — | 2026-09-30 |
| https://sig.mapama.gob.es/calidad-aire/ | redirect | https://www.miteco.gob.es/es/calidad-y-evaluacion-ambiental/temas/atmosfera-y-calidad-del-aire/evaluacion-y-datos-de-calidad-del-aire/datos.html | `miteco-calidad-aire` | redirige al índice de visores de mapa.gob.es; igual sig.mapama.gob.es/redes-seguimiento/ | 2026-09-30 |
| https://wms.mapama.gob.es/sig/ | error | https://gis.miteco.gob.es/descargas/app/DescargaFichero | `miteco-banco-datos-naturaleza` | todos los WMS bajo wms.mapama.gob.es/sig/ responden NullReferenceException; descargar la capa o usar sigpac-hubcloud.es para Red Natura | 2026-09-30 |
| http://www.prtr-es.es/ | error | https://prtr-es.miteco.gob.es/ | `miteco-prtr` | 503 el 30/09/2026 y 404 con certificado incorrecto en las pruebas anteriores | 2026-09-30 |
| https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico/historico-de-boletines.html | 404 | https://www.miteco.gob.es/content/dam/miteco/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico/Historico-de-embalses/BD-Embalses.zip | `miteco-saih-boletin-hidrologico` | — | 2026-09-30 |
| https://data.cnmc.es/api/3/action/package_search | 404 | https://catalogodatos.cnmc.es/api/3/action/package_search | `cnmc-data` | — | 2026-09-30 |
| https://energia.gob.es/balances/Balances/Paginas/Balances.aspx | redirect | https://www.miteco.gob.es/es/energia/estrategia-normativa/balances/balances.html | `miteco-energia-estadisticas` | todo energia.gob.es redirige a miteco.gob.es/es/energia; las páginas SharePoint (Paginas/*.aspx) dan 404 allí | 2026-09-30 |
| https://sedeaplicaciones.minetur.gob.es/PRETOR | 404 | — | `miteco-energia-estadisticas` | registro de instalaciones de producción eléctrica; no se localizó sustituto con descarga | 2026-09-30 |
| https://www.aemps.gob.es/informa/ | 403 | https://www.aemps.gob.es/comunicacion/notas-informativas/notas-informativas-aemps/ | `aemps-otros-registros` | el índice da 403 con cualquier User-Agent; cada nota bajo /informa/{slug}/ sí responde | 2026-09-30 |
| https://cne.isciii.es/servicios/renave | 404 | https://cne.isciii.es/servicios/enfermedades-transmisibles/objetivos-boletines | `isciii-cne` | igual /servicios/renave/boletines; los documentos cuelgan de /documents/d/cne/{slug} | 2026-09-30 |
| https://www.sanidad.gob.es/estadEstudios/estadisticas/sisInfSanSNS/home.htm | 404 | https://www.sanidad.gob.es/estadEstudios/estadisticas/sisInfSanSNS/UltDatos.htm | `sanidad-portal-estadistico` | — | 2026-09-30 |
| https://www.sanidad.gob.es/ciudadanos/prestaciones/centrosServiciosSNS/hospitales/home.htm | redirect | https://www.sanidad.gob.es/estadEstudios/estadisticas/sisInfSanSNS/ofertaRecursos/hospitales/home.htm | `sanidad-portal-estadistico` | responde 200 con un meta refresh, no con 30x | 2026-09-30 |
| https://www.aei.gob.es/datos-abiertos | 404 | https://www.aei.gob.es/ayudas-concedidas/buscador-ayudas-concedidas/download-unlimit/All/All/All/All?keys=&area=All | `aei-convocatorias` | — | 2026-09-30 |
| https://digital.csic.es/rest/ | blocked | https://digital.csic.es/dspace-oai/request | `csic-digital` | filtro antibots Anubis (200 con página de prueba de trabajo en JavaScript); el OAI-PMH queda fuera del filtro | 2026-09-30 |
| https://recolecta.fecyt.es/oai | 404 | — | `fecyt-recolecta` | también /oai/request, /oai-pmh y /oai/openaire; cosechar cada repositorio por separado (csic-digital y otros) | 2026-09-30 |
| https://buscador.recolecta.fecyt.es/ | blocked | — | `fecyt-recolecta` | comprobación de navegador Voight-Kampff con 403 | 2026-09-30 |
| https://registros.gbif.es/ | blocked | https://api.gbif.org/v1/occurrence/search?country=ES | `gbif-es` | 418 con página de comprobación antibots; api.gbif.es presenta un certificado que no coincide con el host | 2026-09-30 |
| https://www.ign.es/resources/sismologia/tproximos/ | 404 | https://www.ign.es/web/resources/sismologia/tproximos/todos_visualizadores.js | `ign-sismologia` | el RSS y el KML de últimos terremotos que colgaban aquí dan 404 (el directorio, 403) y www.ign.es/fdsnws da 404; el GeoJSON de 30 días va en el JavaScript del visor | 2026-10-01 |
| https://www.fega.gob.es/ | reset | — | `fega-beneficiarios-pac` | el servidor cierra la conexión tras el TLS con cualquier User-Agent (también fega.gob.es y www.fega.es); las ayudas están en bdns-api y el SIGPAC en mapa-sigpac | 2026-09-30 |
| https://www.mapa.gob.es/es/estadistica/temas/estadisticas-agrarias/economia/precios-percibidos-pagados-salarios/ | 404 | https://www.mapa.gob.es/es/estadistica/temas/estadisticas-agrarias/economia/precios-percibidos-pagados/precios-percibidos-por-los-agricultores-y-ganaderos | `mapa-estadisticas-agrarias` | — | 2026-09-30 |
| https://www.mapa.gob.es/es/pesca/temas/registro-flota/censo-flota-pesquera-operativa/ | 404 | https://www.mapa.gob.es/es/pesca/temas/registro-flota/informacion-sobre-flota-pesquera | `mapa-pesca` | — | 2026-09-30 |
| https://www.mapa.gob.es/es/cartografia-y-sig/ide/descargas/agricultura/sigpac/descarga.aspx | 404 | https://sigpac-hubcloud.es/ | `mapa-sigpac` | redirige a la ruta sin .aspx, que da 404; descargas, WMS, MVT y API en sigpac-hubcloud.es | 2026-09-30 |
| https://infocar.dgt.es/datex2/dgt/SituationPublication/all/content.xml | 404 | https://nap.dgt.es/datex2/v3/dgt/SituationPublication/datex2_v37.xml | `dgt-datex-trafico` | — | 2026-09-30 |
| https://nap.dgt.es/api/3/action/package_search | 403 | https://nap.dgt.es/dataset | `dgt-datex-trafico` | la API CKAN del NAP está cerrada; el catálogo se lee en HTML | 2026-09-30 |
| https://sedeapl.dgt.gob.es/WEB_IEST_CONSULTA/ | redirect | https://www.dgt.es/menusecundario/dgt-en-cifras/ | `dgt-estadisticas` | — | 2026-09-30 |
| https://www.dgt.es/menusecundario/dgt-en-cifras/matraba-listados/transferencias-automoviles-mensual.html | 404 | — | `dgt-estadisticas` | solo existen los listados de matriculaciones y bajas (diario y mensual) | 2026-09-30 |
| https://movilidad-opendata.mitma.es/ | blocked | — | `mitma-opendata-movilidad` | 403 con cuerpo Internal Server Error para cualquier ruta desde el entorno de verificación; posible bloqueo por red | 2026-09-30 |
| https://www.puertos.es/es-es/estadisticas/Paginas/estadistica_mensual.aspx | redirect | https://www.puertos.es/datos/estadisticas/mensuales | `puertos-estado-datos` | todas las rutas SharePoint es-es/estadisticas/Paginas/*.aspx redirigen a /datos/estadisticas/ | 2026-09-30 |
| https://www.mincotur.gob.es/es-es/IndicadoresyEstadisticas/Paginas/Estadisticas.aspx | redirect | https://www.mintur.gob.es/es-es/IndicadoresyEstadisticas/Paginas/Estadisticas.aspx | `mincotur-industria-turismo` | 302 a mintur.gob.es con la misma ruta, que dio 404 el 30/09/2026 y 200 el 01/10/2026; industria en industria.gob.es/es-es/estadisticas | 2026-10-01 |
| https://consultas2.oepm.es/InvenesWeb/faces/busquedaInternet.jsp | blocked | — | `oepm-invenes` | F5 rechaza toda petición con 403 y un support ID; ninguna ruta de la OEPM se pudo verificar | 2026-09-30 |
| http://datos.bne.es/ | blocked | https://hispana.mcu.es/oai/oai.cmd | `bne-datos` | 403 con una página de bloqueo de 1,3 MB (también www.bne.es/es/catalogos/datos-enlazados); Hispana sí responde | 2026-09-30 |
| https://hispana.mcu.es/es/oai | 404 | https://hispana.mcu.es/oai/oai.cmd | `bne-datos` | — | 2026-09-30 |
| https://estadisticas.educacion.gob.es/EducaDynPx/educabase/index.htm | redirect | https://estadisticas.educacion.gob.es/EducaDynPx/educabase/index.htm?type=pcaxis&path=/no-universitaria/alumnado/matriculado/2024-2025-rd/adultos&file=pcaxis&l=s0 | `educacion-estadisticas-ruct` | la raíz sin path redirige a un 404 del ministerio; con path completo funciona | 2026-09-30 |
| https://www.universidades.gob.es/ | redirect | https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU/Estudiantes.html | `educacion-estadisticas-ruct` | — | 2026-09-30 |
| https://www.mivau.gob.es/vivienda/estadisticas | 404 | https://www.mivau.gob.es/el-ministerio/observatorios-y-estadisticas | `mivau-precios-vivienda-alquiler` | los datos siguen en apps.fomento.gob.es, dominio antiguo sin redirección al nuevo | 2026-09-30 |
| https://www.sepe.es/HomeSepe/que-es-el-sepe/estadisticas/datos-estadisticos/municipios/2020/enero-2020.html | 404 | https://www.sepe.es/HomeSepe/que-es-el-sepe/estadisticas/datos-estadisticos/municipios/2020/enero.html | `sepe-estadisticas` | desde 2020 la página del mes es municipios/{AAAA}/{mes}.html; municipios-20-45 es otra tabla (de 20.000 a 45.000 habitantes) | 2026-10-01 |
| https://ftpdatos.aemet.es/ | dns | https://opendata.aemet.es/opendata/api | `aemet-otros-servicios` | el FTP histórico de AEMET no resuelve | 2026-09-30 |
| https://app.bde.es/bie_www/ | blocked | https://app.bde.es/bierest/resources/srdatosapp/favoritas?idioma=es&series=D_1NBAF472 | `bde-estadisticas` | el BIEST respondió Request Rejected a clientes automatizados el 2026-09-30 y 200 el 2026-10-01; la vía estable es la API bierest y los CSV | 2026-10-01 |
| https://datos.gob.es/virtuoso/sparql | blocked | https://datos.gob.es/apidata/catalog/dataset.json?_pageSize=100&_page=0 | `datos-gob-es-api` | 403 del WAF en todos los intentos; la API REST pasa con reintentos | 2026-09-30 |
| https://registrodelicitadores.gob.es/rolece/public/consulta_publica | 404 | https://visor.registrodelicitadores.gob.es/ | `hacienda-registro-licitadores` | ya no hay consulta pública sin certificado; solo el visor de certificados y el DEUC | 2026-09-30 |
| https://extranjeros.inclusion.gob.es/es/ObservatorioPermanenteInmigracion/ | redirect | https://www.inclusion.gob.es/web/migraciones/homees/ObservatorioPermanenteInmigracion/ | `interior-criminalidad` | redirige al portal de migraciones, que respondió 403 (Akamai) desde centro de datos; no hay ficha del OPI hasta verificarlo desde otra red | 2026-09-30 |
| https://imserso.es/el-imserso/documentacion/estadisticas/sistema-autonomia-atencion-dependencia | 404 | https://imserso.es/el-imserso/documentacion/estadisticas/sistema-autonomia-atencion-dependencia-saad | `imserso-dependencia` | 404 con meta refresh a /pagina-no-encontrada; la ruta actual lleva el sufijo -saad | 2026-09-30 |
| https://avancedigital.mineco.gob.es/banda-ancha/cobertura/Paginas/informes-cobertura.aspx | redirect | https://digital.gob.es/telecomunicaciones-infraestructuras-digitales/areas-interes/banda-ancha/informacion-cobertura | `mtdfp-cobertura-banda-ancha` | el portal de avance digital se integró en digital.gob.es; los xlsx cuelgan de /content/dam/portal-mtdfp/ | 2026-09-30 |
| https://estadisticas.educacion.gob.es/EducaDynPx/educabase/index.htm?type=pcaxis&path=/no-universitaria&file=pcaxis | empty | https://estadisticas.educacion.gob.es/EducaDynPx/educabase/index.htm?type=pcaxis&path=/no-universitaria/alumnado/matriculado/series/gen-al-mat&file=pcaxis | `educacion-estadisticas-ruct` | un path incompleto acaba en la 404.html del ministerio con código 200; hay que dar la ruta completa hasta la carpeta de tablas | 2026-09-30 |
| https://www.dgt.es/export/sites/web-DGT/.galleries/downloads/dgt-en-cifras/publicaciones/Parque-vehiculos-Tablas-Estadisticas/Parque-de-vehiculos-Tablas-estadisticas-2025.xlsx | 404 | https://www.dgt.es/export/sites/web-DGT/.galleries/downloads/dgt-en-cifras/publicaciones/Parque-de-vehiculos-Tablas-Estadisticas/Parque-de-vehiculos-Tablas-estadisticas-2025.xlsx | `dgt-estadisticas` | la carpeta pasó de Parque-vehiculos-Tablas-Estadisticas a Parque-de-vehiculos-Tablas-Estadisticas (con de); el nombre del fichero no cambió; las URL de los xlsx salen de la página dgt-en-cifras-detalle/{slug}/ | 2026-09-30 |
| https://www.ign.es/wfs-inspire/hidrografia | 404 | https://servicios.idee.es/wfs-inspire/hidrografia | `idee-servicios` | los WFS temáticos INSPIRE (hidrografía, transportes, ocupación del suelo) viven en servicios.idee.es; www.ign.es solo mantiene ngbe y unidades-administrativas | 2026-09-30 |
| https://www.ign.es/wfs-inspire/transportes | 404 | https://servicios.idee.es/wfs-inspire/transportes | `idee-servicios` | mismo caso que hidrografia | 2026-09-30 |
| https://www.ign.es/wfs-inspire/ocupacion-suelo | 404 | https://servicios.idee.es/wfs-inspire/ocupacion-suelo | `idee-servicios` | respondía 502 el 2026-09-30; en GeoJSON, api-features.idee.es/collections/landcoverunit | 2026-10-01 |
| https://www.ign.es/wms-inspire/hidrografia | 404 | https://servicios.idee.es/wms-inspire/hidrografia | `idee-servicios` | también transportes, ocupacion-suelo y mdt; en www.ign.es quedan ign-base, pnoa-ma y unidades-administrativas | 2026-09-30 |
| https://servicios.idee.es/wmts/mapa-raster | error | https://www.ign.es/wmts/mapa-raster | `idee-servicios` | el 2026-10-01 cerró la conexión sin respuesta; el MTN ráster y la ortofoto (pnoa-ma) siguen en www.ign.es | 2026-10-01 |
| https://www.cis.es/detalle-ficha-estudio?idEstudio=14893 | redirect | https://www.cis.es/es/estudios/barometro-de-septiembre-2026 | `cis-estudios` | redirige al catálogo sin el estudio; la página de cada estudio es /es/estudios/{slug}, enumerable por sitemap.xml | 2026-09-30 |
| https://www.cis.es/catalogo-estudios/resultados-definidos | 404 | https://www.cis.es/es/estudios/catalogo | `cis-estudios` | el catálogo nuevo se renderiza por JavaScript y sus consultas con q= o start= disparan el anti-bot | 2026-09-30 |
| https://www.cis.es/cis/opencms/ES/index.html | 404 | https://www.cis.es/ | `cis-estudios` | portal OpenCms antiguo; 302 a /en/cis/opencms/ES/index.html, que da 404, igual que las rutas 2_bancodedatos/estudios/ver.jsp | 2026-10-01 |
| https://www.inmujeres.gob.es/MujerCifras/ | 403 | https://www.inmujeres.gob.es/MujerCifras/Home.htm | `inmujeres-mujeres-cifras` | la raíz responde Your client is not allowed; las páginas de tema y los xls de /estadisticasweb/ sí | 2026-09-30 |
| https://www.educacionyfp.gob.es/inee/ | redirect | https://www.educacionfpydeportes.gob.es/inee/portada.html | `inee-bases-datos` | también educacion.gob.es/inee; los ficheros llevan /inee/dam/jcr:{uuid}/ y HEAD responde 403 | 2026-09-30 |
| https://www.cartociudad.es/geocoder/api/geocoder/find?q=Calle%20Iglesia%205,%20Madrid&type=portal&id=280790529087&portal=5 | 500 | https://www.cartociudad.es/geocoder/api/geocoder/candidates?q=calle%20iglesia%205,%20madrid&limit=4 | `cnig-centro-descargas` | ejemplo del PDF oficial del geocoder; los id actuales (13.PV.MUN_...) salen de candidates | 2026-10-01 |
| https://datos.madrid.es/egob/catalogo.json | 404 | https://datos.madrid.es/api/3/action/package_search | `ayuntamiento-madrid-datos-abiertos` | la API del portal antiguo murió con la migración a CKAN; los nombres de conjunto conservan el número antiguo | 2026-10-01 |
| https://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.txt | 404 | https://ciudadesabiertas.madrid.es/dynamicAPI/API/query/calair_tiemporeal.json | `ayuntamiento-madrid-datos-abiertos` | también en CSV cambiando la extensión de la consulta | 2026-10-01 |
| https://www.madrid.org/desvan/ | 404 | https://iestadis.edatos.io | `comunidad-madrid-estadistica-api` | las tablas de los bancos Almudena, Baco y Desvan siguen en datos.comunidad.madrid (comunidad-madrid-datos-abiertos) | 2026-10-01 |
| https://www.ine.es/prodyser/microdatos.htm | redirect | https://www.ine.es/dyngs/SER/index.htm?cid=1388 | `ine-microdatos` | meta refresh con 200 | 2026-10-01 |
| https://www.ine.es/daco/daco42/codmun/diccionario20.xlsx | 404 | https://www.ine.es/daco/daco42/codmun/codmun20/20codmun.xlsx | `ine-codigos-territoriales` | la raíz solo sirve 2021-2026; los años anteriores están en codmun{AA}/ | 2026-10-01 |
| https://www.ine.es/ftp/microdatos/epa/dr_EPA_2025.xlsx | 404 | https://www.ine.es/ftp/microdatos/epa/dr_EPA_2021.xlsx | `ine-microdatos` | el diseño de registro va por vigencia (2005, 2021 y 2026), no por año | 2026-10-01 |
| https://registrodelicitadores.gob.es/rolece/static/manuales/Manuales%20de%20Usuario.zip | 404 | https://registrodelicitadores.gob.es/rolece/static/manuales/EsquemasXSD.zip | `hacienda-registro-licitadores` | — | 2026-10-01 |
| https://www.sanidad.gob.es/profesionales/nomenclator.do?metodo=nomenclatorCSV | moved | https://www.sanidad.gob.es/profesionales/nomenclator.do?metodo=buscarProductos&especialidad=%25%25%25&d-4015021-e=1&6578706f7274=1 | `sanidad-nomenclator-facturacion` | devuelve la página HTML con 200; el CSV es la exportación del buscador | 2026-10-01 |
| https://gitlab.cnmc.es/cnmcdata/cnmcdata-api-ejemplos | redirect | https://data.cnmc.es/reutilizadores | `cnmc-data` | 302 a users/sign_in; los ejemplos de la API ya no son públicos | 2026-10-01 |
| https://catalogodatos.cnmc.es/api/3/action/datastore_search?limit=32000&resource_id=c45b35d4-0714-4373-b0ec-3bd71f157098 | 404 | https://catalogodatos.cnmc.es/api/3/action/package_search | `cnmc-data` | ejemplo de la documentación con un recurso retirado (también 8afd824c); localizar el vigente con package_search o package_show | 2026-10-01 |
| https://cbim.mitma.es/ | redirect | https://cibim.transportes.gob.es/ | `mitma-opendata-movilidad` | 301 al dominio nuevo del Centro de Big Data e Inteligencia de Movilidad | 2026-10-01 |
| https://www.seguridadaerea.gob.es/es/ambitos/aeronaves/matriculacion-de-aeronaves | empty | https://www.seguridadaerea.gob.es/es/ambitos/aeronaves/registro-de-matriculas-de-aeronaves-civiles/registro-de-matriculas | `aesa-aviacion` | 200 con una página de error de 2,5 MB, como cualquier ruta inexistente de AESA | 2026-10-01 |
| https://www.adif.es/datos-abiertos | 404 | — | `renfe-datos-abiertos` | no localicé portal de datos abiertos de Adif; data.adif.es no responde | 2026-10-01 |
| https://www.puertos.es/es-es/estadisticas | 403 | https://www.puertos.es/datos/estadisticas/mensuales | `puertos-estado-datos` | 301 a /datos/estadisticas-bk, que responde 403 | 2026-10-01 |
| https://gis.miteco.gob.es/descargas/atom/CategBiodiversidad/downloadservice.xml | 404 | https://gis.miteco.gob.es/descargas/app/DescargaFichero | `miteco-banco-datos-naturaleza` | sigue enlazado desde descargas/biodiversidad.html; la descarga vigente es un POST con desafío ALTCHA | 2026-10-01 |
| https://www.miteco.gob.es/content/dam/miteco/es/calidad-y-evaluacion-ambiental/temas/sistema-espanol-de-inventario-sei-/webtabla-inv-Ed2025.xlsx | redirect | https://www.miteco.gob.es/content/dam/miteco/es/calidad-y-evaluacion-ambiental/temas/sistema-espanol-de-inventario-sei-/webtabla-inv-Ed2026.xlsx | `miteco-inventario-emisiones` | 302 a /es/error/404.html, que responde 200; solo se publica la última edición | 2026-10-01 |
| https://www.hacienda.gob.es/es-ES/CDI/Paginas/ImpuestosTasasEELL/ImpuestosTasasEELL.aspx | 404 | https://serviciostelematicosext.hacienda.gob.es/SGFAL/ConsultaTipos/html/portadaconsultasm.aspx | `hacienda-ovef` | tipos de IBI, IAE, IVTM y otros tributos locales por municipio | 2026-10-01 |
| https://www.dataestur.es/general/frontur/ | redirect | https://www.dataestur.es/viajes-ocio/frontur/ | `mincotur-industria-turismo` | 301 a dataestur.pid.segittur.es, que respondió 403 The request is blocked; igual /general/egatur/ | 2026-10-01 |
| https://www.cultura.gob.es/servicios-a-la-ciudadania/estadisticas/cultura/mc/culturabase/museos.html | redirect | https://www.cultura.gob.es/servicios-a-la-ciudadania/estadisticas/cultura/mc/culturabase/museos-y-colecciones-museograficas.html | `cultura-culturabase` | 302 a /comunes/errores/404.html, que responde 200 | 2026-10-01 |
| https://cnecovid.isciii.es/covid19/resources/casos_hosp_uci_def_sexo_edad_provres_todas_edades.csv | 404 | https://cnecovid.isciii.es/covid19/resources/hosp_uci_def_sexo_edad_provres_todas_edades.csv | `isciii-cne` | el fichero de todas las edades desde el 2022-03-28 no lleva el prefijo casos_ ni la columna num_casos | 2026-10-01 |
| https://www.aemps.gob.es/comunicacion/notas-informativas-productos-sanitarios/feed/ | empty | https://www.aemps.gob.es/category/productossanitarios/feed/ | `aemps-otros-registros` | 200 con 0 items; los feeds de categoría de WordPress (/category/{slug}/feed/) traen 30 | 2026-10-01 |
| https://icono.fecyt.es/ | dns | https://indicadores.fecyt.es/ | `fecyt-recolecta` | NXDOMAIN; los indicadores de FECYT se descargan en indicadores.fecyt.es/data/ | 2026-10-01 |
| https://erddap.ieo.es/ | dns | — | `ieo-datos-oceanograficos` | NXDOMAIN; los datos del IEO se piden en SeaDataNet (csr.seadatanet.org y cdi.seadatanet.org) | 2026-10-01 |
| http://info.igme.es/bdaguas/PointInfo.aspx?id=1623-8-0001 | 404 | https://info.igme.es/BDAguas/ | `igme-geologia` | es el campo URLDetalle de IGME_PuntosAgua; da 404 también por https | 2026-10-01 |
| https://www.ign.es/web/ign/portal/ultimos-terremotos/-/ultimos-terremotos/get5dias | empty | https://www.ign.es/web/resources/sismologia/tproximos/todos_visualizadores.js | `ign-sismologia` | 200 sin tabla; get10dias con el parámetro portlet_dias da N días | 2026-10-01 |
