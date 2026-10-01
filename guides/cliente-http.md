# Cliente HTTP para fuentes de la Administración española

Arreglos verificados con llamadas reales el 2026-09-30. Cada ficha indica en `quirks` cuáles le aplican; este
documento da el arreglo copiable para cada uno. Filtrar `catalog.json` por `quirks` permite configurar el cliente
antes de la primera petición.

En Python todo esto ya está hecho en `scripts/clientes/sesion.py` (instalable con
`pip install "fuentes-publicas-mcp @ git+https://github.com/BquantFinance/Administracion-fuentes-publicas"`):
`sesion()` devuelve una `requests.Session` con las CA de FNMT (genera `ca-age.pem` en `~/.cache/fuentes-publicas` la
primera vez y lo pasa en cada petición aunque `REQUESTS_CA_BUNDLE` esté definido), User-Agent de navegador, reintentos
con espera ante 429, 5xx, cortes y 403 intermitentes, y la excepción `Bloqueado` ante páginas de Incapsula, Akamai,
F5, Anubis o el bloqueo por IP del Catastro, que no reintenta. `texto()` y `json()` resuelven BOM, UTF-8 con cabecera
ISO-8859-15, Latin-1 real y gzip sin anunciar. Encima, `ckan`, `socrata`, `pcaxis`, `arcgis` y `ogc` paginan sin
topes silenciosos.

## tls-chain-incomplete: certificados FNMT sin intermedio

Muchos servidores públicos (airef.es, tesoro.es, registrodelicitadores.gob.es, energia.gob.es, mites.gob.es,
universidades.gob.es, wms.mapama.gob.es, pestadistico.inteligenciadegestion.sanidad.gob.es, buscadorcdi.gob.es) presentan solo el
certificado final, emitido por una CA intermedia de FNMT-RCM (AC Componentes Informáticos, AC Servidores Seguros
Tipo2...), y no envían el intermedio. Los navegadores lo recuperan por AIA; curl, requests, urllib y Node no. Las
raíces FNMT sí están en certifi y en los sistemas, así que basta añadir los intermedios. Nunca desactivar la
verificación.

```bash
B=https://www.sede.fnmt.gob.es/documents/10445900/10526749
: > fnmt-intermedios.pem
for c in AC_Componentes_Informaticos_SHA256 AC_Servidores_Seguros_Tipo1 AC_Servidores_Seguros_Tipo2 \
         AC_Servidores_Seguros_Tipo1_G2 AC_Servidores_Seguros_Tipo2_G2 AC_Servidores_Seguros_Tipo2_G2R \
         AC_Administracion_Publica_SHA256 AC_Sector_Publico AC_Sector_Publico_G2 \
         AC_Raiz_FNMT-RCM-SS AC_Raiz_FNMT-RCM_G2 AC_RAIZ_FNMTRCM_Servidores_Seguros_G2R; do
  curl -sS -o c.cer "$B/$c.cer"
  (openssl x509 -inform DER -in c.cer 2>/dev/null || openssl x509 -in c.cer) >> fnmt-intermedios.pem
done
curl -sS -o c.cer http://www.cert.fnmt.es/certs/ACCOMP.crt && openssl x509 -inform DER -in c.cer >> fnmt-intermedios.pem
cat "$(python3 -c 'import certifi;print(certifi.where())')" fnmt-intermedios.pem > ca-age.pem
curl --cacert ca-age.pem -A "Mozilla/5.0" "https://www.tesoro.es/deuda-publica/estadisticas"
```

```python
import requests
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify="ca-age.pem", timeout=30)
```

O bien `export REQUESTS_CA_BUNDLE=ca-age.pem` y `export SSL_CERT_FILE=ca-age.pem` para todo el proceso. La lista
completa de certificados de FNMT está en https://www.sede.fnmt.gob.es/descargas/certificados-raiz-de-la-fnmt.
`python scripts/fnmt_bundle.py` hace todo esto (certifi, los 12 certificados de la sede, ACCOMP.crt y el contenido de
`EXTRA_CA_BUNDLE` si existe) y deja `ca-age.pem` en la raíz del repo.

Dos trampas verificadas el 2026-09-30:

- Algunos .cer de la sede (Tipo1_G2, Tipo2_G2, Tipo2_G2R) son PEM con una cabecera de texto (Subject, Issuer) delante
  del bloque BEGIN CERTIFICATE; convertirlos como DER produce un bundle que curl rechaza con el error 77. Extraer el
  bloque PEM o dejar que `fnmt_bundle.py` lo haga.
- pestadistico.inteligenciadegestion.sanidad.gob.es firma con una intermedia (AC Componentes Informáticos) que no
  está en la lista de la sede; se obtiene de la extensión AIA del certificado (http://www.cert.fnmt.es/certs/ACCOMP.crt).
  www.cultura.gob.es la usaba en septiembre de 2026 y el 2026-10-01 ya enviaba la cadena completa. Y si `REQUESTS_CA_BUNDLE` o
  `CURL_CA_BUNDLE` están definidos en el entorno (proxies corporativos, sandboxes), `requests.Session` ignora
  `session.verify` y usa esa variable: pasar `verify="ca-age.pem"` en cada petición o apuntar la variable al bundle.

## user-agent-browser

Enviar siempre un User-Agent de navegador. tesoro.es responde 403 al User-Agent por defecto de curl y de
urllib; otros sitios devuelven páginas distintas. `curl -A "Mozilla/5.0"`, `headers={"User-Agent": "Mozilla/5.0"}`.

## accept-header-required

Las APIs del BOE (sumarios, legislación consolidada, BORME) exigen `Accept: application/json` o
`Accept: application/xml`. Sin cabecera, o con `*/*`, responden 400. Los errores llegan siempre en XML aunque se
haya pedido JSON; comprobar el código HTTP antes de parsear.

Variante verificada el 2026-10-01: www.agenciatributaria.es envía una intermedia FNMT firmada con SHA-1 y OpenSSL 3
responde «CA signature digest algorithm too weak»; con el bundle de `fnmt_bundle.py` la cadena se completa con la
intermedia vigente y responde 200.

## gzip-unannounced

La API del Banco de España comprime siempre en gzip, aunque el cliente no lo pida o envíe `Accept-Encoding: identity`.
El 2026-09-30 llegaba sin `Content-Encoding`; el 2026-10-01, con `Content-Encoding: gzip`. `curl --compressed` y
requests lo resuelven; con urllib usar `gzip.decompress(resp.read())` si los dos primeros bytes son `1f 8b`.

## latin1

Feeds RSS del BOE y CSV del Banco de España van en ISO-8859-1. `curl ... | iconv -f ISO-8859-1 -t UTF-8`,
`pd.read_csv(url, encoding="latin-1")`, `resp.content.decode("latin-1")`.

## viewstate-forms

Portal de la CNMV (ASP.NET Web Forms). Para automatizar una búsqueda: GET de la página del formulario, extraer
los campos ocultos `__VIEWSTATE`, `__VIEWSTATEGENERATOR` y `__EVENTVALIDATION`, y reenviarlos en el POST junto
con los campos del formulario (nombres `ctl00$...`). Mantener la sesión de cookies entre GET y POST. Mismo
patrón en DataInvex, BADASE, el Portal Estadístico del SNS y los informes de PRTR-España; en todos ellos la
ficha indica si existe un fichero o API que evite el formulario.

## waf-blocks-bots

Un WAF o una prueba anti-bots rechaza clientes automatizados aunque lleven User-Agent de navegador. El buscador BIEST
del Banco de España (app.bde.es/bie_www) lo hacía el 2026-09-30 con "Request Rejected" y el 2026-10-01 respondió 200
a curl y requests; la vía estable sigue siendo la API y los catálogos CSV de la ficha.

Formas del bloqueo verificadas el 2026-09-30 y sin arreglo lícito desde un script:

- Anubis (Digital.CSIC): la web, las páginas handle y la API REST devuelven 200 con una página "Making sure
  you're not a bot" que exige una prueba de trabajo en JavaScript; el endpoint OAI-PMH queda fuera del filtro.
- F5 con "The requested URL was rejected" y un support ID (OEPM, consultas2.oepm.es): 403 a cualquier cliente,
  con cookies o sin ellas.
- Comprobación de navegador "Voight-Kampff Browser Test" (buscador.recolecta.fecyt.es) y "Checking you are
  not a bot" con código 418 (registros.gbif.es).
- Página de bloqueo de 1,3 MB con 403 (datos.bne.es y las páginas de datos enlazados de bne.es).
- Conexión cerrada tras el TLS, sin respuesta HTTP (www.fega.gob.es) y 403 "Internal Server Error" a todo
  (movilidad-opendata.mitma.es); probablemente bloqueos por origen de red.

En todos los casos la ficha indica la vía alternativa (OAI-PMH, otro organismo, API global) o marca la fuente
como no verificada.

## waf-intermittent-403

El portal de la Seguridad Social (Akamai) responde 403 "Acceso denegado" a una de cada dos o tres peticiones
legítimas, también en las descargas de ficheros, y 200 a la siguiente. Reintentar la misma URL tras 2 a 5
segundos, con las mismas cabeceras (User-Agent y Accept-Language de navegador). No es un límite de ritmo: una
petición aislada también puede recibir el 403.

## session-required

Hacienda (presupuestos de las comunidades autónomas, SGCIEF/PublicacionPresupuestos) devuelve sesion_expirada a
las URL de descarga pedidas directamente; con un cookie jar bastan un GET de inicio.aspx y del formulario y un POST
con sus __VIEWSTATE y __EVENTVALIDATION para recibir el xlsx, sin navegador (verificado el 2026-10-01). REGCON
(convenios colectivos) acepta el POST del formulario con cookie jar; consulta_token_value_id lo rellena el
JavaScript con la hora y no hace falta. La paginación (?pagina=N) y la exportación (?_exportarExcelPublicoXML=1)
dependen de la búsqueda guardada en la sesión: sin la cookie, ?pagina=N devuelve el registro entero sin avisar.

## captcha-required

El Centro de Descargas del CNIG pide un token de reCAPTCHA v3 (preAutorizarDescarga con recaptchaToken) antes de
autorizar cada descarga; sin él, descargaDir responde 403. No hay arreglo lícito desde un script: usar la vía
alternativa que indica la ficha (servicios WFS, WMS o ATOM del mismo organismo) o descargar una vez a mano.

Caso distinto: las descargas GIS de MITECO (`gis.miteco.gob.es/descargas/app/DescargaFichero?f=capa.zip`) usan
ALTCHA, una prueba de trabajo pensada para resolverse en el cliente sin interacción. Se resuelve en código:

```python
import base64, hashlib, json, re, requests
s = requests.Session(); s.headers["User-Agent"] = "Mozilla/5.0"
base = "https://gis.miteco.gob.es/descargas/app/DescargaFichero"
tok = re.search(r'name="__RequestVerificationToken"[^>]*value="([^"]+)"', s.get(base, params={"f": "rn2000.zip"}).text).group(1)
ch = s.get(base, params={"handler": "Altcha"}).json()
n = next(i for i in range(ch["maxnumber"] + 1) if hashlib.sha256((ch["salt"] + str(i)).encode()).hexdigest() == ch["challenge"])
altcha = base64.b64encode(json.dumps({k: ch[k] for k in ("algorithm", "challenge", "salt", "signature")} | {"number": n}).encode()).decode()
r = s.post(base, params={"handler": "Download"}, data={"__RequestVerificationToken": tok, "f": "rn2000.zip", "altcha": altcha}, stream=True)
```

El desafío caduca a los 120 s (`expires` en `salt`), así que pedirlo justo antes del POST; sin el campo altcha el
POST da 400. Verificado el 2026-09-30 y el 2026-10-01 con rn2000.zip (133 MB, entre 0,05 y 0,2 s de cálculo).

## js-rendered

Contenido generado en el navegador. Antes de lanzar un navegador sin cabeza, mirar en las herramientas de red
qué llamadas XHR hace la página: casi siempre devuelven JSON y se pueden replicar con requests. Casos
verificados el 2026-10-01: el buscador del REEC (arise/search, JSON por GET), Portus (portussvr/api, mareas y
último dato), el visor de terremotos del IGN (todos_visualizadores.js con cuatro GeoJSON) y el visor de SERPAVI
(GeoJSON en un blob de Azure cuya carpeta de versión se lee en el JavaScript de la página).

Caso aparte y muy rentable: los portales PC-Axis clonados del INE (INEbase, EDUCAbase de Educación, CULTURAbase
y el portal de criminalidad de Interior) se navegan con JavaScript pero sirven cada tabla en tres formatos con una
URL fija que se deduce del enlace `Tabla.htm?path=...&file=X.px`:

```
https://{host}/{app}/files/_px/es/csv_bdsc{path}{file}?nocab=1   CSV con ; en UTF-8 con BOM
https://{host}/{app}/files/_px/es/px{path}{file}                  PC-Axis
https://{host}/{app}/files/_px/es/xlsx{path}{file}?nocab=1        Excel
```

`{app}` es `EducaJaxiPx` en estadisticas.educacion.gob.es, `CulturaJaxiPx` en estadisticas.cultura.gob.es y
`sec/jaxiPx` en estadisticasdecriminalidad.ses.mir.es. El CSV llega en UTF-8 con BOM aunque Content-Type diga
ISO-8859-15 (decodificado como latin-1 sale «autÃ³noma»; usar utf-8-sig); el px sí va en ISO-8859-15.

## static-html

Lo contrario: el HTML servido ya contiene los enlaces a los ficheros. Un GET más una expresión regular sobre
href, o lxml, bastan. Es el caso de AIReF, Tesoro, AEAT, IGAE, Hacienda local, INE, MITES, SEPE, Seguridad
Social, MAPA, MITECO (calidad del aire, boletín hidrológico), ISCIII, DGT (listados de microdatos) e Interior.
Rascar la página en cada ejecución cuando además tenga url-drift.

## errors-html-or-xml

BOE (errores siempre en XML), INE (404 y 500 en HTML) y BDNS (404 de Tomcat en HTML) no devuelven el error en el
formato pedido. Comprobar el código HTTP antes de parsear y no confiar en Content-Type.

## url-drift y overwritten-in-place

Dos estrategias de caché opuestas. Con url-drift (AIReF, ICO, CNMV, Hacienda local, Seguridad Social, MAPA,
MITECO, ISCIII, SIIU, Puertos del Estado) la URL del fichero cambia en cada publicación, a veces con una marca de
tiempo o un uuid en el nombre: no fijar enlaces, localizarlos en la página cada vez. Con overwritten-in-place
(Tesoro, AEAT, SEPE, CORES) la URL es fija pero el contenido se sustituye: guardar copia fechada si se necesita el
histórico de publicaciones o de revisiones. url-drift también marca las fichas cuyas rutas antiguas (.aspx,
dominios anteriores) han muerto: energia.gob.es, prtr-es.es, mincotur, fomento, universidades.gob.es.

## json-object-or-list

En las APIs del BOE y BORME, `item`, `departamento`, `epigrafe` y `apartado` son un objeto cuando hay un
elemento y una lista cuando hay varios. Normalizar: `x if isinstance(x, list) else [x]`.

## no-weekend-data

El BOE no se publica los domingos (sí los festivos nacionales, con menos secciones) y el BORME tampoco los sábados
ni los festivos; la API devuelve 404 esos días (verificado el 2026-10-01). Al iterar fechas, tratar 404 como día sin
publicación, no como error. Algún día antiguo devuelve 500; reintentar
una vez y saltar.

## soft-errors-200

Errores o consultas sin datos que responden HTTP 200: comprobar el contenido, no solo el código. Casos verificados
el 2026-10-01: AEMET (cuerpo vacío sin clave y estado 404 o 429 dentro del JSON), BOE xml.php con un id inexistente
(raíz `error`), ELI (página de error con title «Error 404»), INE Tempus (`{"status": ...}` en tablas grandes sin filtro),
Idescat y eDatos de Madrid (un código de filtro inexistente se ignora o devuelve vacío), CNIG («Pagina no encontrada»),
MINETUR (id inexistente con lista vacía), Banco de España (`errNum` 404 dentro de la lista en `favoritas`), IVE, IGAE
y Central de Información de Hacienda (HTML con 200) y PLACSP (un ZIP inexistente es un HTML de 521 bytes). Patrón:
validar Content-Type, tamaño mínimo y la clave esperada antes de guardar o parsear.

## datastore-incomplete

En los portales CKAN autonómicos y municipales el datastore (la API de filas) puede no coincidir con el fichero: en la
Comunidad de Madrid el padrón tenía 5.000 de 18.718 filas, en la Junta de Andalucía una tabla 1.000 de 36.260 y en
Barcelona un recurso 1.250 filas para un CSV de 539 MB; en la Generalitat Valenciana las copias del IVE van atrasadas.
Comparar `total` de `datastore_search` con el fichero y, para tablas completas, descargar el recurso original
(`/dataset/{name}/resource/{id}/download`).

## waf-temporary-ban

El WAF bloquea la IP para todo el host durante minutos. datos.madrid.es (Akamai) lo hace tras consultas a
`datastore_search_sql`, cerca de un minuto; el Catastro, tras ráfagas de unas 15 peticiones; PLACSP, el 2026-10-01, entre
20 minutos y tres horas, con 200 y un HTML de 187 bytes en lugar del feed. Espaciar las peticiones,
cachear y no reintentar en bucle: cada intento alarga el bloqueo.

## connection-reset-intermittent

El servidor corta conexiones a ratos (reset o cierre en el saludo TLS) y la misma petición funciona al repetirla:
los hosts de la Generalitat Valenciana (dadesobertes, pegv, bdo, bdt) y MINETUR (carburantes) el 2026-10-01.
Reintentar con espera; en requests, `HTTPAdapter(max_retries=Retry(total=4, backoff_factor=2, allowed_methods=None))`.

## Ritmo de peticiones

Ninguna de las fuentes verificadas documenta límites ni devolvió 429 durante la verificación. Regla prudente
para descargas masivas: peticiones secuenciales por host, reintento con espera exponencial (2, 4, 8 s) ante
5xx y ante cortes de conexión, y cachear en local lo descargado, porque varias fuentes sobreescriben ficheros
en la misma URL (cuadros mensuales del Tesoro) o mueven las rutas (uploads de AIReF, documentos del ICO).

## IP de centros de datos

Varios servidores rechazan rangos de nube (GitHub Actions, entornos de ejecución de agentes) aunque la petición sea
correcta; el mismo cliente funciona desde una IP residencial o corporativa. Verificado el 2026-09-30 desde GitHub Actions
y desde un entorno de verificación: Catastro (cierra la conexión o 403 «Petición HTTP bloqueada»), REData y datos.gob.es
(Incapsula, 403 con HTML), www.bne.es y datos.bne.es (403 con HTML), FEGA (reset o tiempo de espera), inclusion.gob.es
(403 Akamai), ENAIRE (403 del WAF F5), infoelectoral, DGSFP e Instituciones Penitenciarias (reset). Antes de dar una
fuente por caída, probar desde otra red; `verificacion.yml` marca estos casos como `blocked` o `error`, no como `fail`.
