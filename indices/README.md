# Índices para agentes

Generado por `scripts/build.py` a partir de `indices/*.yaml`, no editar. 41 recetas, 95 necesidades, 19 identificadores, 58 rutas muertas.

## Recetas por intención

Procedimientos verificados que encadenan fichas. `python scripts/check_recetas.py` ejecuta las comprobaciones de cada receta contra los servidores reales (batería de regresión).

| receta | intención | fichas | verificada |
|---|---|---|---|
| `ipc-ultimo-dato` | Último IPC general nacional con variación mensual y anual | ine-api-tempus | 2026-09-30 |
| `localizar-tabla-ine` | Encontrar y descargar una tabla del INE por operación (EPA, padrón, PIB, natalidad) sin conocer su id | ine-api-tempus | 2026-09-30 |
| `municipio-a-codigo-ine` | Código INE de un municipio a partir de su nombre, o la relación completa de municipios | cnig-centro-descargas, ine-codigos-territoriales, catastro-ovc | 2026-09-30 |
| `coordenadas-a-referencia-catastral` | De unas coordenadas a la parcela (recinto SIGPAC y referencia catastral) y a los datos del inmueble | mapa-sigpac, catastro-ovc | 2026-09-30 |
| `parcela-a-red-natura-y-nitratos` | Saber si un recinto agrícola está en Red Natura 2000 o en zona vulnerable a nitratos | mapa-sigpac | 2026-09-30 |
| `empresa-nif-a-ayudas-y-contratos` | Subvenciones, ayudas de investigación y contratos públicos de una empresa o entidad por su NIF | bdns-api, aei-convocatorias, placsp-datos-abiertos, borme-api-sumario | 2026-09-30 |
| `organismo-a-dir3-y-nif` | Código DIR3 y NIF de un organismo público a partir de su nombre, y su jerarquía | face-facturas, dir3-directorio, datos-gob-es-api | 2026-09-30 |
| `boe-sumario-y-texto-consolidado` | Qué se publicó en el BOE un día y cómo pasar de una disposición a su texto y a la norma consolidada | boe-api-sumario, boe-api-legislacion-consolidada, boe-eli | 2026-09-30 |
| `buscar-norma-por-titulo` | Encontrar normas por palabras del título, rango o fecha y seguir sus cambios | boe-api-legislacion-consolidada, boe-feeds | 2026-09-30 |
| `licitaciones-nuevas` | Licitaciones y adjudicaciones publicadas hoy en toda la contratación pública | placsp-datos-abiertos, boe-feeds | 2026-09-30 |
| `subvenciones-convocatorias-recientes` | Convocatorias de subvenciones publicadas en un rango de fechas y su detalle | bdns-api | 2026-09-30 |
| `deuda-publica-por-administracion` | Deuda de un ayuntamiento, de una comunidad autónoma o del Estado | hacienda-ovef, bde-estadisticas, tesoro-estadisticas, airef-datos | 2026-09-30 |
| `irpf-por-municipio` | Renta y declarantes de IRPF por municipio y tramo, todos los ejercicios | aeat-estadisticas | 2026-09-30 |
| `paro-registrado-por-municipio` | Paro registrado y demandantes por municipio, sexo, edad y actividad de un mes | sepe-estadisticas, ine-codigos-territoriales | 2026-09-30 |
| `afiliacion-y-pensiones` | Afiliados a la Seguridad Social por régimen, provincia, CNAE o municipio, y pensiones del mes | segsocial-estadisticas | 2026-09-30 |
| `precio-carburantes-municipio` | Precios de hoy de las gasolineras de un municipio o provincia, y el histórico de un día | minetur-precios-carburantes | 2026-09-30 |
| `incidencias-trafico-tiempo-real` | Incidencias, obras, cortes y velocidades de la red de carreteras en este momento | dgt-datex-trafico | 2026-09-30 |
| `matriculaciones-diarias` | Vehículos matriculados o dados de baja cada día, con marca, modelo y municipio | dgt-estadisticas | 2026-09-30 |
| `calidad-aire-estacion` | Serie horaria o diaria de un contaminante en una estación de calidad del aire | miteco-calidad-aire | 2026-09-30 |
| `embalses-y-caudales` | Reserva de agua de un embalse y caudal diario de un río en una estación de aforo | miteco-saih-boletin-hidrologico | 2026-09-30 |
| `capa-red-natura-2000` | Descargar la capa oficial de Red Natura 2000 u otra capa de biodiversidad | miteco-banco-datos-naturaleza, mapa-sigpac | 2026-09-30 |
| `prediccion-meteo-municipio` | Predicción diaria u horaria de un municipio y observación de la estación más cercana | aemet-opendata | pendiente |
| `medicamento-por-cn-o-nombre` | Datos de un medicamento por código nacional, nombre o principio activo, con ficha técnica y problemas de suministro | aemps-cima-api | 2026-09-30 |
| `exceso-mortalidad-momo` | Defunciones observadas y esperadas por día, ámbito, sexo y edad (MoMo) | isciii-cne | 2026-09-30 |
| `cosecha-oai-publicaciones` | Cosechar publicaciones científicas o patrimonio digital de forma incremental | csic-digital, bne-datos, fecyt-recolecta | 2026-09-30 |
| `tabla-pcaxis-a-csv` | Descargar como CSV una tabla de cualquier portal PC-Axis (INE, EDUCAbase, criminalidad) sin navegador | ine-api-tempus, educacion-estadisticas-ruct, interior-criminalidad | 2026-09-30 |
| `ocurrencias-especie-espana` | Registros de presencia de una especie en España, con recuento y descarga | gbif-es | 2026-09-30 |
| `geologia-y-aguas-subterraneas-punto` | Unidad geológica en un punto y puntos de agua subterránea de una provincia | igme-geologia | 2026-09-30 |
| `buscar-dataset-datos-gob-es` | Localizar un dataset abierto de cualquier Administración y su URL de descarga real | datos-gob-es-api | 2026-09-30 |
| `series-banco-de-espana` | Último dato o serie completa de un indicador del Banco de España (euríbor, tipos, crédito, deuda) | bde-estadisticas | 2026-09-30 |
| `flota-pesquera` | Buques de la flota pesquera por puerto base, caladero y modalidad, y capturas por especie | mapa-pesca | 2026-09-30 |
| `criminalidad-municipio` | Infracciones penales por tipología y trimestre en una comunidad, provincia o municipio de más de 20.000 habitantes | interior-criminalidad | 2026-09-30 |
| `actos-mercantiles-borme` | Constituciones, nombramientos, ceses y disoluciones de sociedades publicados en el BORME | borme-api-sumario, boe-feeds | 2026-09-30 |
| `hospitales-catalogo` | Listado de hospitales con camas, dependencia, complejo y municipio | sanidad-portal-estadistico | 2026-09-30 |
| `dataset-cnmc-a-csv` | Descargar un dataset de la CNMC (energía, telecomunicaciones, postal) como CSV o consultarlo por API | cnmc-data | 2026-09-30 |
| `convenio-colectivo-regcon` | Consultar un convenio colectivo por código, denominación o CNAE en REGCON | mites-estadisticas | 2026-09-30 |
| `deficit-y-ejecucion-presupuestaria` | Déficit mensual de las Administraciones Públicas y ejecución del presupuesto del Estado | igae-ejecucion-presupuestaria, hacienda-ovef | 2026-09-30 |
| `precio-electricidad-horario` | Precio de la electricidad por hora o cuarto de hora (mercado diario, PVPC y spot) y demanda del día | omie-mercado, ree-redata | 2026-09-30 |
| `medicamento-precio-financiado` | Precio de venta, precio de referencia y aportación de un medicamento financiado, con su ficha técnica | sanidad-nomenclator-facturacion, aemps-cima-api | 2026-09-30 |
| `geometria-seccion-censal` | Geometría de las secciones censales, distritos o municipios de un año para mapear datos del INE | ine-cartografia-censal, ine-api-tempus | 2026-09-30 |
| `horarios-tren-gtfs` | Horarios y paradas de Cercanías y de alta velocidad en GTFS, con las coordenadas de las estaciones | renfe-datos-abiertos | 2026-09-30 |

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
3. `ine-api-tempus`: Cambiar js por csv en la URL para obtener CSV (tabulador, ISO-8859-15 con BOM)
   ```
   curl -s "https://servicios.ine.es/wstempus/csv/ES/DATOS_TABLA/24077?nult=1"
   ```
- salida: JSON con una entrada por serie (COD, Nombre, Data) o CSV de la tabla

**municipio-a-codigo-ine** · Código INE de un municipio a partir de su nombre, o la relación completa de municipios
1. `cnig-centro-descargas`: GET del geocoder CartoCiudad find?q={nombre}; devuelve muniCode (INE de 5 dígitos), provinceCode, comunidadAutonomaCode y la geometría; acepta tildes
   ```
   curl -s "https://www.cartociudad.es/geocoder/api/geocoder/find?q=Alcal%C3%A1%20de%20Henares"
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
   curl -s "https://sigpac-hubcloud.es/servicioconsultassigpac/query/refrecinbycoord/4326/-3.9/40.3.json"
   ```
2. `mapa-sigpac`: refcatparcela/{pr}/{mu}/{ag}/{zo}/{po}/{pa}.json devuelve referencia_cat (14 caracteres, parcela)
   ```
   curl -s "https://sigpac-hubcloud.es/servicioconsultassigpac/query/refcatparcela/28/15/0/0/3/9000.json"
   ```
3. `catastro-ovc`: En suelo urbano, Consulta_RCCOOR (XML, pc1+pc2 son los 14 caracteres) y después Consulta_DNPRC?RefCat= para uso, superficie, año y municipio INE; el OVC bloquea la IP tras unas 15 peticiones seguidas (403 Petición HTTP bloqueada durante más de media hora el 30/09/2026)
   ```
   curl -s "https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_RCCOOR?SRS=EPSG:4326&Coordenada_X=-3.6960&Coordenada_Y=40.4185"
   ```
- salida: referencia SIGPAC, referencia catastral de 14 caracteres y datos no protegidos del inmueble

**parcela-a-red-natura-y-nitratos** · Saber si un recinto agrícola está en Red Natura 2000 o en zona vulnerable a nitratos
- entrada: referencia-sigpac
1. `mapa-sigpac`: Obtener los siete códigos del recinto con refrecinbycoord/4326/{lon}/{lat}.json o recinfobypoint
2. `mapa-sigpac`: intersection/red_natura/{pr}/{mu}/{ag}/{zo}/{po}/{pa}/{re}.json devuelve lic_code, lic_name, zepa_code, surface_intersection y surface_tpc; intersection/nitratos igual para zonas vulnerables
   ```
   curl -s "https://sigpac-hubcloud.es/servicioconsultassigpac/intersection/red_natura/28/15/0/0/3/9000/6.json"
   ```
- salida: lista JSON de intersecciones con códigos LIC y ZEPA y superficie afectada

**empresa-nif-a-ayudas-y-contratos** · Subvenciones, ayudas de investigación y contratos públicos de una empresa o entidad por su NIF
- entrada: nif
1. `bdns-api`: concesiones/busqueda?nifCif={NIF}&page=0&pageSize=100 con Accept application/json (con Accept de navegador responde XML); beneficiario trae NIF y nombre en un solo campo, con importe, ayudaEquivalente, numeroConvocatoria y fechaConcesion; el parámetro beneficiario= no existe (400)
   ```
   curl -s -H "Accept: application/json" "https://www.infosubvenciones.es/bdnstrans/api/concesiones/busqueda?page=0&pageSize=100&nifCif=Q1132001G"
   ```
2. `bdns-api`: grandesbeneficiarios, ayudasestado y minimis tienen el mismo patrón de búsqueda (nifCif verificado solo en concesiones); exportación con concesiones/exportar?vpd=GE&tipoDoc=csv y los mismos filtros
3. `aei-convocatorias`: Ayudas de investigación en el CSV completo, filtrar la columna C.I.F. (separador ;, UTF-8 con BOM)
4. `placsp-datos-abiertos`: Contratos en los feeds ATOM y ZIP mensuales; los documentos CODICE llevan cbc:ID con schemeName NIF (adjudicatarios y órganos), filtrar por el valor y comprobar el elemento padre
5. `borme-api-sumario`: Actos societarios solo por nombre y fecha en el XML de cada provincia (receta actos-mercantiles-borme)
- salida: concesiones BDNS (JSON), ayudas AEI (filas CSV) y expedientes PLACSP (XML CODICE)

**organismo-a-dir3-y-nif** · Código DIR3 y NIF de un organismo público a partir de su nombre, y su jerarquía
1. `face-facturas`: relations?fulltext={nombre}&limit=100&page=1; cada item trae oc, og y ut con code (DIR3) y og.identifier con el NIF; relations.csv sin filtro descarga las 50186 relaciones
   ```
   curl -s "https://proveedores.face.gob.es/api/v1/relations?fulltext=Ayuntamiento%20de%20Madrid&limit=100&page=1"
   ```
2. `dir3-directorio`: Jerarquía completa y unidades ausentes de FACe en los xlsx por nivel (AGE 2741, CCAA 2742, EELL 2744); descargar en dos pasos con cookie jar y User-Agent de navegador
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
1. `placsp-datos-abiertos`: GET del feed ATOM vigente (unas 235 entradas, 6 MB); cada entry lleva un documento CODICE con el órgano (cbc:ID schemeName DIR3), CPV, importes (TotalAmount con IVA, TaxExclusiveAmount sin) y estado; link rel=next enlaza la instantánea anterior
   ```
   curl -s "https://contrataciondelestado.es/sindicacion/sindicacion_643/licitacionesPerfilesContratanteCompleto3.atom"
   ```
2. `placsp-datos-abiertos`: Histórico en ZIP mensual por feed (12 a 19 MB) con el mismo XML; PlataformasAgregadasSinMenores.atom para CCAA y EELL y contratosMenoresPerfilesContratantes.atom para menores
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
3. `bdns-api`: Exportación masiva con convocatorias/exportar?vpd=GE&tipoDoc=csv y los mismos filtros (windows-1252; tope de 10000 filas sin aviso)
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
4. `airef-datos`: Histórico de deuda por Administración en Historico_Deuda.xlsx; la URL cambia con cada publicación, localizarla en la página del observatorio de deuda
- salida: xlsx por entidad (Hacienda), CSV por serie (BdE) y cuadros mensuales (Tesoro)

**irpf-por-municipio** · Renta y declarantes de IRPF por municipio y tramo, todos los ejercicios
- entrada: ine-municipio
1. `aeat-estadisticas`: IRPFmunicipios.csv (31 MB, separador ;, decimal coma) con una fila por ejercicio (EJER), tramo (TRAMO) y municipio (MUNI_DEF) y una columna MUNI_n por variable; MUNI_DEF es un código propio, comprobar en la documentación de la estadística la equivalencia con el INE antes de cruzar
   ```
   curl -sO "https://sede.agenciatributaria.gob.es/static_files/Sede/Tema/Estadisticas/Anuario_estadistico/Exportacion/IRPFmunicipios.csv"
   ```
2. `aeat-estadisticas`: Recaudación mensual por figura tributaria en Cuadros_estadisticos_series_es_es.xlsx (URL fija, contenido sobrescrito en cada publicación)
- salida: CSV masivo de todos los ejercicios

**paro-registrado-por-municipio** · Paro registrado y demandantes por municipio, sexo, edad y actividad de un mes
- entrada: ine-municipio
1. `sepe-estadisticas`: La página del mes municipios-20-45/{AAAA}/{mes}.html (2020 en adelante) enlaza un xls por comunidad autónoma en {AAAA}/{mes}_{AAAA}/Muniacteco_20-45_{CCAA}.xls; de 2005 a 2019 en municipios/{AAAA}/{mes}-{AAAA}.html
   ```
   curl -sO -A "Mozilla/5.0" "https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_estadisticos/municipios_20_45/2026/agosto_2026/Muniacteco_20-45_ANDALUCIA.xls"
   ```
2. `sepe-estadisticas`: Los xls son de formato informe, sin código INE (solo nombre del municipio); xlrd no los abre, calamine sí (pandas engine=calamine)
3. `sepe-estadisticas`: Series nacionales y provinciales con URL fija en evolparoseries.xls y paroprovsector.xls
   ```
   curl -sO -A "Mozilla/5.0" "https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_avance/xls/empleo/evolparoseries.xls"
   ```
4. `ine-codigos-territoriales`: Asignar el código INE por nombre y provincia con el diccionario anual
- salida: xls por comunidad con demandantes parados por municipio

**afiliacion-y-pensiones** · Afiliados a la Seguridad Social por régimen, provincia, CNAE o municipio, y pensiones del mes
- entrada: cnae, ine-municipio
1. `segsocial-estadisticas`: GET de la página de la estadística (EST8/EST10/EST290 afiliación media; EST8/EST10/EST305 último día por municipio y CNAE; EST23/EST24 pensiones) con User-Agent y Accept de navegador; extraer los enlaces wcm/connect, que llevan un uuid nuevo en cada publicación
   ```
   curl -sL -A "Mozilla/5.0" -H "Accept: text/html,application/xhtml+xml" "https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST23/EST24" | grep -o 'href="[^"]*wcm/connect[^"]*"'
   ```
2. `segsocial-estadisticas`: Descargar el xlsx con las mismas cabeceras; ante 403 repetir la misma URL tras 2 a 5 segundos (el WAF rechaza una de cada dos o tres peticiones; con Accept */* recibí 403 en 15 intentos seguidos)
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
1. `dgt-estadisticas`: Listado de ficheros en matraba-listados/matriculaciones-automoviles-diario.html (24 diarios del mes) y -mensual.html (desde 2014-12); bajas en bajas-automoviles-diario y -mensual
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
1. `miteco-saih-boletin-hidrologico`: BD-Embalses.zip (Access, 10 MB) con la tabla T_Datos Embalses (AMBITO_NOMBRE, EMBALSE_NOMBRE, FECHA, AGUA_TOTAL, AGUA_ACTUAL, ELECTRICO_FLAG) semanal desde 1988; leer con mdbtools (mdb-export) o un driver ODBC, en la verificación no se consiguió leerlo con librerías Python puras
   ```
   curl -sSL -o BD-Embalses.zip "https://www.miteco.gob.es/content/dam/miteco/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico/Historico-de-embalses/BD-Embalses.zip"
   ```
2. `miteco-saih-boletin-hidrologico`: listado-estaciones-aforo.zip (cuatro CSV con COD_HIDRO, COD_SAIH, UTM huso 30 y municipio) y Anuario-21-22-csv.zip (136 MB, afliq.csv por cuenca con indroea;fecha;altura;caudal diarios)
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
1. `aemet-opendata`: Con clave gratuita en la cabecera api_key, GET prediccion/especifica/municipio/diaria/{INE de 5 dígitos sin dígito de control}; la respuesta es un JSON intermedio (estado, datos) y los datos se descargan con una segunda petición a la URL del campo datos; sin clave llega 200 con cuerpo vacío
   ```
   curl -s -H "api_key: $AEMET_KEY" "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/28079"
   ```
2. `aemet-opendata`: valores/climatologicos/inventarioestaciones/todasestaciones da idema y coordenadas; elegir la más cercana y pedir observacion/convencional/datos/estacion/{idema}
3. `aemet-opendata`: Las 64 rutas y sus parámetros están en AEMET_OpenData_specification.json (OpenAPI 3.0.1), sin clave
   ```
   curl -s "https://opendata.aemet.es/AEMET_OpenData_specification.json"
   ```
- salida: JSON de predicción por día; coma decimal en algunos ficheros de datos
- nota: Sin clave solo se verificaron la especificación y el comportamiento sin autenticación (30/09/2026); las respuestas de datos están pendientes

**medicamento-por-cn-o-nombre** · Datos de un medicamento por código nacional, nombre o principio activo, con ficha técnica y problemas de suministro
- entrada: cn-medicamento
1. `aemps-cima-api`: medicamento?cn={cn} o ?nregistro={nreg} devuelve nregistro, pactivos, atcs, presentaciones (cn, estado), docs (PDF y HTML) y estado; medicamentos?nombre= o ?practiv1= busca (páginas de 200; un cn inexistente responde 204 sin cuerpo)
   ```
   curl -s "https://cima.aemps.es/cima/rest/medicamento?cn=708201"
   ```
2. `aemps-cima-api`: docSegmentado/contenido/1?nregistro={nreg}&seccion=4.1 devuelve una sección de la ficha técnica en HTML; PDF estable en /cima/pdfs/ft/{nreg}/FT_{nreg}.pdf
3. `aemps-cima-api`: psuministro lista los problemas de suministro activos por cn; registroCambios?fecha=dd/mm/aaaa permite sincronizar sin rebajar todo; nomenclátor completo en prescripcion.zip, regenerado a diario
   ```
   curl -s "https://cima.aemps.es/cima/rest/psuministro"
   ```
- salida: JSON del medicamento (solo JSON; Accept XML responde 406)

**exceso-mortalidad-momo** · Defunciones observadas y esperadas por día, ámbito, sexo y edad (MoMo)
- entrada: ccaa
1. `isciii-cne`: momo.isciii.es/public/momo/data es un único CSV de 719 MB (comillas, coma) regenerado a diario; el servidor ignora Range y devuelve el fichero entero con 200, así que leer en streaming y filtrar por ambito (nacional, ccaa), cod_ine_ambito, cod_sexo y cod_gedad
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

**tabla-pcaxis-a-csv** · Descargar como CSV una tabla de cualquier portal PC-Axis (INE, EDUCAbase, criminalidad) sin navegador
1. `ine-api-tempus`: INE, cambiar js por csv en la API (csv/ES/DATOS_TABLA/{id}?nult=n): tabulador, ISO-8859-15 con BOM
   ```
   curl -s "https://servicios.ine.es/wstempus/csv/ES/DATOS_TABLA/24077?nult=12"
   ```
2. `educacion-estadisticas-ruct`: EDUCAbase, del enlace Tabla.htm?path=...&file=X.px deducir EducaJaxiPx/files/_px/es/csv_bdsc{path}{file}?nocab=1 (separador ;, ISO-8859-15, miles con punto)
   ```
   curl -s "https://estadisticas.educacion.gob.es/EducaJaxiPx/files/_px/es/csv_bdsc/no-universitaria/alumnado/matriculado/2024-2025-rd/adultos/l0/adul_01.px?nocab=1"
   ```
3. `interior-criminalidad`: Criminalidad, mismo patrón en sec/jaxiPx/files/_px/es/csv_bdsc{path}{file}?nocab=1 (último trimestre en /DatosBalanceAct/l0/)
   ```
   curl -s "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/09004.px?nocab=1"
   ```
- salida: CSV con la tabla completa; px y xlsx cambiando csv_bdsc por px o xlsx

**ocurrencias-especie-espana** · Registros de presencia de una especie en España, con recuento y descarga
1. `gbif-es`: species/match?name={nombre científico} devuelve usageKey (taxón), rank, matchType y confidence
   ```
   curl -s "https://api.gbif.org/v1/species/match?name=Lynx%20pardinus"
   ```
2. `gbif-es`: occurrence/search?country=ES&taxonKey={usageKey}&limit=300&offset={n} (offset máximo 100000; filtros hasCoordinate, year, gadmGid); occurrence/count con los mismos filtros para el total
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
3. `igme-geologia`: La hoja MAGNA 50 en vectorial y PDF con URL estable por número de hoja (VRF_MAGNA50_{hoja}.zip)
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
2. `bde-estadisticas`: favoritas?idioma=es&series={cod} da el último valor; listaSeries?idioma=es&series={cod}&rango=MAX la serie completa (rangos por frecuencia); la respuesta va siempre en gzip, usar --compressed
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
1. `interior-criminalidad`: Índice del trimestre en sec/dynPx/inebase/index.htm?type=pcaxis&path=/DatosBalanceAnt/{AAAA}{T}/&file=pcaxis (el último en /DatosBalanceAct/)
   ```
   curl -s "https://estadisticasdecriminalidad.ses.mir.es/sec/dynPx/inebase/index.htm?type=pcaxis&path=/DatosBalanceAnt/20262/&file=pcaxis"
   ```
2. `interior-criminalidad`: CSV con jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/09006.px?nocab=1 (municipios; 09005 provincias, 09004 CCAA); cabecera Geografía;Tipología penal;Periodos:;Total, ISO-8859-15, miles con punto y decimales con coma
   ```
   curl -s "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/09006.px?nocab=1"
   ```
- salida: CSV con periodo actual, anterior y variación por tipología

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
1. `sanidad-portal-estadistico`: CNH_{AAAA}.xlsx (9 hojas, 849 hospitales en 2025) con código de hospital, camas, dependencia funcional y código de municipio INE con dígito de control (6 dígitos; quitar el último para cruzar)
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
1. `mites-estadisticas`: GET de consultaPublicaEstatal conservando cookies para obtener consulta_token_value_id; POST del formulario con codigoConvenio, denominacion, cnae2009Pub o cnae2025Pub y el token; el servidor no envía el intermedio FNMT (bundle de la guía)
   ```
   curl -s -c cj -b cj --cacert ca-age.pem "https://expinterweb.mites.gob.es/regcon/pub/consultaPublicaEstatal" | grep -o 'consulta_token_value_id" value="[^"]*"'
   ```
- salida: HTML con la lista de convenios (sin API ni exportación localizada)

**deficit-y-ejecucion-presupuestaria** · Déficit mensual de las Administraciones Públicas y ejecución del presupuesto del Estado
1. `igae-ejecucion-presupuestaria`: Operaciones no financieras mensuales por subsector en M_AACC_{AAAA}.xlsx (URL predecible por año) y serie anual en CAP_Serie.xlsx
   ```
   curl -sO "https://www.igae.pap.hacienda.gob.es/sitios/igae/es-ES/Contabilidad/ContabilidadNacional/Publicaciones/Documents/AACC-M/M_AACC_2026.xlsx"
   ```
2. `igae-ejecucion-presupuestaria`: Ejecución mensual del presupuesto del Estado desde la página imejecucionpresupuesto.aspx (enlaces a xlsx por mes)
3. `hacienda-ovef`: Ejecución trimestral de las entidades locales en un xls por trimestre desde 2017
- salida: xlsx con cuadros por subsector

**precio-electricidad-horario** · Precio de la electricidad por hora o cuarto de hora (mercado diario, PVPC y spot) y demanda del día
1. `omie-mercado`: Precio marginal oficial en marginalpdbc_{AAAAMMDD}.1 (96 periodos cuarto-horarios en 2026; cabecera, filas AAAA;MM;DD;periodo;precio;precio y asterisco final); el fichero del día siguiente se publica por la tarde
   ```
   curl -s "https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_20260929.1"
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
1. `ine-cartografia-censal`: seccionado_{AAAA}.zip del mismo año que el dato (65 MB, shapefile ETRS89 UTM 30); CUSEC es la sección de 10 dígitos, CUDIS el distrito y CUMUN el municipio; disolver por CUMUN para municipios
   ```
   curl -sO "https://www.ine.es/prodyser/cartografia/seccionado_2026.zip"
   ```
2. `ine-api-tempus`: Los datos por sección (Atlas de distribución de renta) o por municipio se cruzan por esos códigos, cargados como texto con ceros a la izquierda
- salida: GeoDataFrame con una fila por sección y los códigos territoriales

**horarios-tren-gtfs** · Horarios y paradas de Cercanías y de alta velocidad en GTFS, con las coordenadas de las estaciones
1. `renfe-datos-abiertos`: GTFS estáticos con URL fija (google_transit.zip para AV, LD y MD; fomento_transit.zip para Cercanías); sin feed_info, la fecha de versión está en last_modified de package_show
   ```
   curl -sO "https://ssl.renfe.com/gtransit/Fichero_AV_LD/google_transit.zip"
   ```
2. `renfe-datos-abiertos`: estaciones.csv (ISO-8859-1, separador ;) con CODIGO, LATITUD y LONGITUD para geolocalizar; los feeds GTFS-RT de gtfsrt.renfe.com no respondieron desde el entorno de verificación
   ```
   curl -sO "https://ssl.renfe.com/ftransit/Fichero_estaciones/estaciones.csv"
   ```
- salida: ZIP GTFS y CSV de estaciones

## Dónde está cada cosa

**Legislación y boletines oficiales**
- Sumario diario del BOE con identificador y URLs de cada disposición → `boe-api-sumario`
- Texto consolidado, vigencia y versiones de una norma → `boe-api-legislacion-consolidada` (incluye normas autonómicas; los boletines autonómicos no están en el catálogo)
- URI estable de una norma para citar o enlazar → `boe-eli`
- Vigilar novedades del BOE, BORME, ayudas o licitaciones sin programar contra la API → `boe-feeds` (RSS en ISO-8859-1)
- Actos societarios inscritos en el Registro Mercantil → `borme-api-sumario` (sin búsqueda por empresa; recorrer días y provincias)

**Economía, finanzas y mercados**
- Euríbor, tipos de interés y de cambio, crédito, balanza de pagos → `bde-estadisticas`
- Deuda pública por Administración (Protocolo de Déficit Excesivo) → `bde-estadisticas` (capítulo SB_DEUAAPP; histórico también en airef-datos)
- Subastas del Tesoro y deuda del Estado por instrumento y tenedor → `tesoro-estadisticas`
- Previsiones macroeconómicas y estimación del PIB en tiempo real → `airef-datos`
- Entidades supervisadas, hechos relevantes e informes financieros de cotizadas → `cnmv-registros` (sin API; formularios ASP.NET, XML mensual de IIC y RSS)
- Líneas ICO y avales por beneficiario → `ico-datos` (no hay datos descargables, solo memoria y cuentas en PDF)

**Hacienda, tributos y presupuestos**
- Renta y declarantes de IRPF por municipio, código postal o tramo → `aeat-estadisticas`
- Recaudación tributaria mensual por figura → `aeat-estadisticas`
- Suministro Inmediato de Información, VERI*FACTU y presentación de modelos → `aeat-servicios-web` (SOAP con certificado electrónico)
- Presupuestos, liquidaciones y deuda viva de ayuntamientos y diputaciones → `hacienda-ovef`
- Tipos de IBI, IAE e IVTM por municipio → `hacienda-ovef` (consulta web con sesión (SGFAL))
- Déficit de las Administraciones Públicas y ejecución del presupuesto del Estado → `igae-ejecucion-presupuestaria`
- Inventario de entes del sector público (INVENTE) → `igae-ejecucion-presupuestaria`

**Estadística oficial**
- Cualquier estadística oficial del INE (IPC, EPA, PIB, padrón, natalidad, empresas) → `ine-api-tempus`
- Códigos INE de municipios, provincias y comunidades → `ine-codigos-territoriales`
- Microdatos de encuestas (EPA, condiciones de vida, presupuestos familiares, censo) → `ine-microdatos`
- Turismo (FRONTUR, EGATUR, ocupación hotelera) → `ine-api-tempus` (las operaciones son del INE; DATAESTUR (mincotur-industria-turismo) las reagrega con API de clave)
- Renta por sección censal (Atlas de distribución de renta) → `ine-api-tempus` (operación del INE; localizar la tabla con TABLAS_OPERACION, no verificada en esta sesión)
- Empresas activas por actividad y tamaño (DIRCE) → `ine-api-tempus`
- Tasa de paro, ocupados y activos (EPA) → `ine-api-tempus` (la EPA es del INE, no del SEPE)
- Salarios → `ine-api-tempus` (Encuesta de Estructura Salarial en el INE; salarios en fuentes tributarias por municipio en aeat-estadisticas (modelo190_salarios))
- Defunciones por causa de muerte → `ine-api-tempus` (estadística del INE; Sanidad solo publica PDF)
- Padrón, nacimientos, defunciones y migraciones → `ine-api-tempus`
- Índice de precios de vivienda y de alquiler → `ine-api-tempus`

**Contratación pública y subvenciones**
- Licitaciones, adjudicaciones y contratos menores de todas las Administraciones → `placsp-datos-abiertos`
- Convocatorias y concesiones de subvenciones, ayudas de Estado, minimis, grandes beneficiarios → `bdns-api`
- Empresas clasificadas para contratar (ROLECE) → `hacienda-registro-licitadores` (solo con certificado electrónico)

**Empleo y Seguridad Social**
- Paro registrado, demandantes y contratos por municipio → `sepe-estadisticas`
- Afiliación a la Seguridad Social por régimen, actividad, provincia y municipio → `segsocial-estadisticas`
- Pensiones contributivas e Ingreso Mínimo Vital → `segsocial-estadisticas`
- Muestra Continua de Vidas Laborales → `segsocial-estadisticas` (no se descarga; se solicita bajo convenio)
- Convenios colectivos (REGCON), huelgas, accidentes de trabajo, regulación de empleo → `mites-estadisticas`
- Extranjeros con autorización de residencia y afiliados extranjeros → `segsocial-estadisticas` (afiliados extranjeros en EST292; las estadísticas de extranjería del Ministerio de Inclusión no están aún en el catálogo)

**Gobierno abierto, transparencia y organización administrativa**
- Catálogo de datasets abiertos de todas las Administraciones → `datos-gob-es-api` (solo metadatos; el fichero vive en el portal del publicador)
- Códigos DIR3 de unidades, entidades y oficinas → `dir3-directorio` (la API relations de face-facturas da DIR3 y NIF sin WAF)
- NIF y relaciones de facturación de un organismo público → `face-facturas`
- Boletín de empleo público y códigos SIA de procedimientos → `pag-administracion-gob-es`
- Altos cargos, retribuciones, agendas y estadísticas de derecho de acceso → `transparencia-portal` (pocas descargas; contratos y subvenciones sin ficheros)

**Territorio, catastro y cartografía**
- Datos de un inmueble o parcela por referencia catastral, dirección o coordenadas → `catastro-ovc` (bloqueo por IP tras ráfagas de unas 15 peticiones)
- Parcelario, edificios y direcciones vectoriales por municipio (INSPIRE) → `catastro-ovc`
- Ortofotos PNOA, modelos del terreno, LiDAR y límites municipales → `cnig-centro-descargas` (descargas con reCAPTCHA; WMS, WMTS y WFS sin restricción)
- Geocodificar una dirección y obtener su código INE → `cnig-centro-descargas` (geocoder CartoCiudad)
- Geometría de secciones censales, distritos y municipios por año → `ine-cartografia-censal` (shapefile anual del INE; los límites municipales oficiales del IGN están tras reCAPTCHA (cnig-centro-descargas))
- Localizar cualquier servicio WMS, WFS o CSW de una Administración → `idee-servicios`

**Meteorología y clima**
- Predicción, observación, climatología, avisos y radar → `aemet-opendata` (clave gratuita obligatoria; el cuerpo vacío con 200 es fallo de autenticación)
- Proyecciones de cambio climático y series centenarias → `aemet-otros-servicios` (sin descarga directa verificada)

**Medio ambiente, agua y biodiversidad**
- Calidad del aire validada por estación y contaminante → `miteco-calidad-aire` (datos anuales validados; el tiempo real lo sirve cada comunidad autónoma, fuera del alcance)
- Emisiones industriales por complejo (PRTR) → `miteco-prtr`
- Reserva de embalses, caudales y estaciones de aforo → `miteco-saih-boletin-hidrologico`
- Red Natura 2000, espacios protegidos, hábitats, humedales, inventario forestal → `miteco-banco-datos-naturaleza` (descargas con desafío ALTCHA (resuelto en la guía); los WMS de mapama están rotos)

**Energía**
- Precios de carburantes por gasolinera → `minetur-precios-carburantes`
- Comercializadoras, cambios de suministrador, bono social, garantías de origen → `cnmc-data`
- Consumo de productos petrolíferos y gas por provincia, balances energéticos → `miteco-energia-estadisticas` (series de CORES en xlsx; el ministerio publica PDF)
- Demanda, generación por tecnología, PVPC y precio spot horarios → `ree-redata` (WAF intermitente; reintentar; ESIOS exige token)
- Precio marginal del mercado diario e intradiario, curvas y programas de casación → `omie-mercado` (ficheros de texto por día; 96 periodos cuarto-horarios en 2026)
- Registro de instalaciones de producción eléctrica y autoconsumo → `miteco-energia-estadisticas` (no localizada descarga abierta; PRETOR da 404)
- Telecomunicaciones (líneas, operadores, audiovisual) → `cnmc-data`

**Sanidad y medicamentos**
- Medicamentos, presentaciones, fichas técnicas y problemas de suministro → `aemps-cima-api` (sin precios; precios y financiación en sanidad-nomenclator-facturacion)
- Precios, financiación y aportación de medicamentos (nomenclátor de facturación) → `sanidad-nomenclator-facturacion`
- Ensayos clínicos (REEC) y alertas de seguridad → `aemps-otros-registros` (sin API; el REEC exige sesión)
- Exceso de mortalidad (MoMo), COVID-19, boletines epidemiológicos, gripe → `isciii-cne`
- Hospitales, altas hospitalarias e indicadores del Sistema Nacional de Salud → `sanidad-portal-estadistico` (solo el Catálogo de Hospitales tiene descarga directa)

**Ciencia e investigación (biología, química, geología, oceanografía)**
- Presencia de especies (ocurrencias, datasets de biodiversidad) → `gbif-es`
- Ayudas de investigación concedidas por la AEI → `aei-convocatorias`
- Publicaciones científicas en acceso abierto → `csic-digital` (OAI-PMH; RECOLECTA (fecyt-recolecta) ya no expone OAI)
- Geología, hidrogeología, puntos de agua y minería → `igme-geologia`
- Terremotos recientes y catálogo sísmico → `ign-sismologia` (tablas HTML; el catálogo solo se descargó desde navegador)

**Agricultura, pesca y alimentación**
- Beneficiarios de la PAC → `fega-beneficiarios-pac` (no verificable el 30/09/2026 (el servidor cierra la conexión); probar bdns-api concesiones con el órgano FEGA)
- Recintos agrícolas, usos del suelo y referencia catastral rústica → `mapa-sigpac`
- Anuario de estadística agraria, precios percibidos y pagados, consumo alimentario → `mapa-estadisticas-agrarias`
- Flota pesquera, capturas y acuicultura → `mapa-pesca` (el identificador de buque es CODIGOBUQUE, no el CFR)

**Transporte y movilidad**
- Datos oceanográficos en tiempo real (oleaje, mareas, boyas) → `puertos-estado-datos` (Portus es una aplicación con API interna no reproducida)
- Incidencias de tráfico, detectores, radares, zonas de bajas emisiones, puntos de recarga → `dgt-datex-trafico`
- Matriculaciones, bajas, parque de vehículos y conductores (microdatos) → `dgt-estadisticas` (no localizados microdatos de accidentes, solo tablas)
- Matrices origen-destino de movilidad por telefonía móvil → `mitma-opendata-movilidad` (el host de datos respondió 403 desde el entorno de verificación)
- Horarios de trenes (GTFS), estaciones con coordenadas y posiciones en tiempo real → `renfe-datos-abiertos` (GTFS-RT no verificado desde el entorno; Adif sin portal localizado)
- Tráfico portuario mensual por autoridad portuaria → `puertos-estado-datos`
- Tráfico aéreo por aeropuerto y registro de aeronaves → `aesa-aviacion` (degradada; sin ficheros verificados)

**Comercio exterior, industria y propiedad industrial**
- Comercio exterior por producto, país y provincia → `datacomex` (API con token de usuario gratuito)
- Inversión extranjera en España y española en el exterior → `datainvex` (aplicación ASP.NET con viewstate; sin API)
- Estadísticas de industria, series BADASE y datos turísticos (DATAESTUR) → `mincotur-industria-turismo`
- Patentes, marcas y Boletín de la Propiedad Industrial → `oepm-invenes` (bloqueado por el cortafuegos de la OEPM desde el entorno de verificación)

**Educación y universidades**
- Alumnado, profesorado y centros no universitarios → `educacion-estadisticas-ruct` (EDUCAbase con el patrón PC-Axis del INE)
- Universidades, matriculados y egresados por titulación, títulos oficiales (RUCT) → `educacion-estadisticas-ruct`

**Justicia, interior y seguridad**
- Criminalidad por tipología, comunidad, provincia y municipio → `interior-criminalidad`

**Cultura y patrimonio**
- Catálogo bibliográfico de la BNE y patrimonio digital (Hispana) → `bne-datos` (datos.bne.es bloqueado desde el entorno; Hispana por OAI-PMH)

**Vivienda y urbanismo**
- Precios de vivienda, transacciones, alquiler (SERPAVI) y suelo → `mivau-precios-vivienda-alquiler`

**Sin fuente en el catálogo**
- Cotizaciones bursátiles y precios de mercado (BME, OMIE) → ninguna (fuera del alcance actual; BME es privado y OMIE no está aún en el catálogo)
- Estadística judicial y sentencias → ninguna (Poder Judicial (CGPJ, CENDOJ) fuera del alcance actual)
- Ayuda oficial al desarrollo y acción exterior → ninguna (sin fuente en el catálogo todavía)

## Identificadores para cruzar datos

| id | formato | regex | ejemplo | emisor | lo usan |
|---|---|---|---|---|---|
| ine-municipio | 5 dígitos, provincia (2) + municipio (3); algunos ficheros añaden un sexto dígito de control | `^\d{5}$` | 28079 | ine-codigos-territoriales | mapa-sigpac, ine-codigos-territoriales, miteco-calidad-aire, aemet-opendata, sanidad-portal-estadistico, catastro-ovc, cnig-centro-descargas, ine-cartografia-censal, dgt-estadisticas, mitma-opendata-movilidad |
| ine-provincia | 2 dígitos, 01 a 52 | `^(0[1-9]|[1-4]\d|5[0-2])$` | 28 | ine-codigos-territoriales | mapa-sigpac, datacomex, minetur-precios-carburantes, miteco-energia-estadisticas, ine-codigos-territoriales, ine-microdatos, dir3-directorio, miteco-calidad-aire, sanidad-portal-estadistico, catastro-ovc, cnig-centro-descargas, ine-cartografia-censal, dgt-estadisticas |
| ccaa | 2 dígitos, 01 Andalucía a 19 Melilla, en el orden del INE | `^(0[1-9]|1\d)$` | 13 | ine-codigos-territoriales | ine-codigos-territoriales, ine-microdatos, isciii-cne, sanidad-portal-estadistico, cnig-centro-descargas, ine-cartografia-censal |
| nuts | ES más 1 a 3 caracteres (ES1, ES11, ES111) | `^ES[1-7]\d{0,2}$` | ES300 | — | ine-cartografia-censal |
| seccion-censal | 10 dígitos, municipio (5) + distrito (2) + sección (3) | `^\d{10}$` | 2807901001 | ine-cartografia-censal | ine-cartografia-censal |
| referencia-catastral | 14 caracteres alfanuméricos (parcela) o 20 (inmueble, con 4 dígitos y 2 letras de control) | `^[0-9A-Z]{14}(\d{4}[A-Z]{2})?$` | 9872023VH5797S0001WX | catastro-ovc | mapa-sigpac, catastro-ovc |
| referencia-sigpac | provincia:municipio:agregado:zona:polígono:parcela:recinto, números separados por dos puntos | `^\d{1,2}:\d{1,3}:\d+:\d+:\d+:\d+:\d+$` | 28:15:0:0:3:9000:6 | mapa-sigpac | mapa-sigpac |
| idema | 4 o 5 caracteres alfanuméricos | `^[0-9A-Z]{4,5}$` | 3195 | aemet-opendata | aemet-opendata |
| nif | DNI (8 dígitos y letra), NIE (X, Y o Z, 7 dígitos y letra) o NIF de persona jurídica (letra, 7 dígitos y control) | `^(\d{8}[A-Z]|[XYZ]\d{7}[A-Z]|[A-HJ-NP-SUVW]\d{7}[0-9A-J])$` | Q1132001G | — | fega-beneficiarios-pac, aei-convocatorias, bdns-api, dir3-directorio, face-facturas |
| dir3 | letra (E, L, A, U, I) y 8 dígitos, o dos letras (LA, EA) y 7 dígitos | `^([A-Z]\d{8}|[A-Z]{2}\d{7})$` | E00003901 | dir3-directorio | placsp-datos-abiertos, datos-gob-es-api, dir3-directorio, face-facturas |
| sia | 6 o 7 dígitos | `^\d{6,7}$` | 200125 | pag-administracion-gob-es | — |
| invente | código numérico del Inventario de Entes del Sector Público | — | — | igae-ejecucion-presupuestaria | bdns-api |
| bdns | 6 dígitos | `^\d{6}$` | 800000 | bdns-api | bdns-api |
| cpv | 8 dígitos, opcionalmente guion y dígito de control | `^\d{8}(-\d)?$` | 45000000-7 | — | placsp-datos-abiertos |
| cnae | sección (letra A a U) o 2 a 4 dígitos (división, grupo, clase) | `^([A-U]|\d{2,4})$` | 4711 | — | mites-estadisticas, segsocial-estadisticas, miteco-prtr |
| codigo-convenio | 14 dígitos | `^\d{14}$` | — | mites-estadisticas | mites-estadisticas |
| cn-medicamento | 6 dígitos | `^\d{6}$` | 708201 | aemps-cima-api | aemps-cima-api, sanidad-nomenclator-facturacion |
| boe-id | BOE-A-AAAA-NNNNN (disposición), BOE-B-AAAA-NNNNN (anuncio), BORME-A-AAAA-NNN-PP (PP código de provincia) | `^(BOE-[ABC]-\d{4}-\d{1,6}|BORME-[ABC]-\d{4}-\d{1,5}(-\d{2})?)$` | BOE-A-1978-31229 | boe-api-sumario | boe-api-legislacion-consolidada, boe-api-sumario, boe-eli, borme-api-sumario |
| eli | URI https://www.boe.es/eli/es/{tipo}/{AAAA}/{MM}/{DD}/{num} con sufijo /con (consolidado) o /dof (publicado) | `^https://www\.boe\.es/eli/es(-[a-z]{2})?/[a-z]+/\d{4}/\d{2}/\d{2}/[^/]+(/(con|dof))?$` | https://www.boe.es/eli/es/lo/2018/12/05/3/con | boe-eli | boe-api-legislacion-consolidada, boe-eli |

**ine-municipio**
- trampa: cargar siempre como texto; como entero pierde el cero inicial de Álava a Barcelona (01 a 08)
- vía `cnig-centro-descargas`: nombre o dirección a código INE con el geocoder CartoCiudad (muniCode)
- vía `catastro-ovc`: código catastral (locat) a INE (loine) con ObtenerMunicipios
- vía `aemet-opendata`: las predicciones por municipio se piden con el INE de 5 dígitos sin dígito de control
- vía `minetur-precios-carburantes`: sin equivalencia; Listados/Municipios usa IDMunicipio propio y solo comparte IDProvincia (INE)
- vía `sanidad-portal-estadistico`: el Catálogo de Hospitales lo guarda con dígito de control (6 dígitos)
- vía `ine-cartografia-censal`: CUMUN en el shapefile de secciones censales; disolver por CUMUN da el contorno municipal del año

**ine-provincia**
- trampa: Ceuta 51 y Melilla 52; el ISO 3166-2 (provincia_iso en los CSV COVID del ISCIII) es otro sistema
- vía `minetur-precios-carburantes`: IDProvincia coincide con el código INE
- vía `dir3-directorio`: catálogo de provincias con idElemento 427

**ccaa**
- trampa: el orden no es alfabético ni el de Eurostat (NUTS2 ES11...)
- vía `isciii-cne`: MoMo usa cod_ine_ambito con este código para ambito ccaa

**nuts**
- trampa: NUTS3 coincide con la provincia salvo islas, Ceuta y Melilla; lo emite Eurostat, no hay fuente en el catálogo

**seccion-censal**
- trampa: las secciones se redibujan cada año; usar la geometría del mismo año que el dato
- vía `ine-cartografia-censal`: geometría anual con CUSEC (sección), CUDIS (distrito) y CUMUN (municipio)
- vía `ine-api-tempus`: renta por sección en el Atlas de distribución de renta (operación del INE)
- vía `mitma-opendata-movilidad`: zonificación por distritos y municipios de los estudios de movilidad (host no verificable)

**referencia-catastral**
- trampa: los códigos de municipio del Catastro son propios, no INE
- vía `catastro-ovc`: coordenadas a referencia con Consulta_RCCOOR; datos del inmueble con Consulta_DNPRC
- vía `mapa-sigpac`: parcela SIGPAC a referencia catastral de 14 caracteres con refcatparcela

**referencia-sigpac**
- trampa: los códigos de provincia y municipio son los del INE; polígono y parcela coinciden con Catastro en rústica, el resto no
- vía `mapa-sigpac`: coordenadas a recinto con refrecinbycoord; recinto a Red Natura o nitratos con intersection

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

**sia**
- trampa: identifica el procedimiento, no el organismo; sin descarga abierta del catálogo SIA

**invente**
- trampa: formato no verificado; consultar en BasesDatos/Invente

**bdns**
- trampa: es la clave estable de la convocatoria; el título varía y los extractos en el BOE lo citan
- vía `bdns-api`: convocatorias?numConv= para el detalle; concesiones/busqueda?numeroConvocatoria= para sus concesiones

**cpv**
- trampa: vocabulario europeo; en CODICE va en cbc:ItemClassificationCode
- vía `boe-feeds`: RSS de anuncios de licitación por división CPV (canal_cpv.php)

**cnae**
- trampa: CNAE 2025 sustituye a CNAE 2009 desde 2026 en Seguridad Social y REGCON; no encadenar series sin recodificar
- vía `segsocial-estadisticas`: afiliación por CNAE a dos dígitos (EST305)
- vía `mites-estadisticas`: REGCON filtra por cnae2009Pub y cnae2025Pub
- vía `miteco-prtr`: inventario de complejos industriales con CNAE

**codigo-convenio**
- trampa: se consulta en REGCON con codigoConvenio; ejemplo no verificado en esta sesión

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
| https://pap.hacienda.gob.es/invente2/ | blocked | https://www.igae.pap.hacienda.gob.es/sitios/igae/es-ES/BasesDatos/Invente/Paginas/inicio.aspx | `igae-ejecucion-presupuestaria` | rechazado por el WAF en la verificación; el 30/09/2026 ni siquiera se estableció la conexión | 2026-09-30 |
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
| https://www.ign.es/resources/sismologia/tproximos/ | 404 | https://www.ign.es/web/ign/portal/ultimos-terremotos/-/ultimos-terremotos/get10dias | `ign-sismologia` | el RSS y el KML de últimos terremotos que colgaban aquí dan 404 (el directorio, 403); www.ign.es/fdsnws no existe | 2026-09-30 |
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
| https://www.mincotur.gob.es/es-es/IndicadoresyEstadisticas/Paginas/Estadisticas.aspx | 404 | https://industria.gob.es/es-es/estadisticas | `mincotur-industria-turismo` | redirige a mintur.gob.es con la misma ruta, que da 404 | 2026-09-30 |
| https://consultas2.oepm.es/InvenesWeb/faces/busquedaInternet.jsp | blocked | — | `oepm-invenes` | F5 rechaza toda petición con 403 y un support ID; ninguna ruta de la OEPM se pudo verificar | 2026-09-30 |
| http://datos.bne.es/ | blocked | https://hispana.mcu.es/oai/oai.cmd | `bne-datos` | 403 con una página de bloqueo de 1,3 MB (también www.bne.es/es/catalogos/datos-enlazados); Hispana sí responde | 2026-09-30 |
| https://hispana.mcu.es/es/oai | 404 | https://hispana.mcu.es/oai/oai.cmd | `bne-datos` | — | 2026-09-30 |
| https://estadisticas.educacion.gob.es/EducaDynPx/educabase/index.htm | redirect | https://estadisticas.educacion.gob.es/EducaDynPx/educabase/index.htm?type=pcaxis&path=/no-universitaria/alumnado/matriculado/2024-2025-rd/adultos&file=pcaxis&l=s0 | `educacion-estadisticas-ruct` | la raíz sin path redirige a un 404 del ministerio; con path completo funciona | 2026-09-30 |
| https://www.universidades.gob.es/ | redirect | https://www.ciencia.gob.es/Ministerio/Estadisticas/SIIU/Estudiantes.html | `educacion-estadisticas-ruct` | — | 2026-09-30 |
| https://www.mivau.gob.es/vivienda/estadisticas | 404 | https://www.mivau.gob.es/el-ministerio/observatorios-y-estadisticas | `mivau-precios-vivienda-alquiler` | los datos siguen en apps.fomento.gob.es, dominio antiguo sin redirección al nuevo | 2026-09-30 |
| https://www.sepe.es/HomeSepe/que-es-el-sepe/estadisticas/datos-estadisticos/municipios/2020/enero-2020.html | 404 | https://www.sepe.es/HomeSepe/que-es-el-sepe/estadisticas/datos-estadisticos/municipios-20-45/2020/enero.html | `sepe-estadisticas` | la ruta municipios/{AAAA}/{mes}-{AAAA}.html solo existe hasta 2019 | 2026-09-30 |
| https://ftpdatos.aemet.es/ | dns | https://opendata.aemet.es/opendata/api | `aemet-otros-servicios` | el FTP histórico de AEMET no resuelve | 2026-09-30 |
| https://app.bde.es/bie_www/ | blocked | https://app.bde.es/bierest/resources/srdatosapp/favoritas?idioma=es&series=D_1NBAF472 | `bde-estadisticas` | el buscador BIEST responde Request Rejected a las consultas automatizadas; la API bierest y los CSV no tienen ese bloqueo | 2026-09-30 |
| https://datos.gob.es/virtuoso/sparql | blocked | https://datos.gob.es/apidata/catalog/dataset.json?_pageSize=100&_page=0 | `datos-gob-es-api` | 403 del WAF en todos los intentos; la API REST pasa con reintentos | 2026-09-30 |
| https://registrodelicitadores.gob.es/rolece/public/consulta_publica | 404 | https://visor.registrodelicitadores.gob.es/ | `hacienda-registro-licitadores` | ya no hay consulta pública sin certificado; solo el visor de certificados y el DEUC | 2026-09-30 |
