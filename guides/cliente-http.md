# Cliente HTTP para fuentes de la Administración española

Arreglos verificados con llamadas reales el 2026-09-30. Cada ficha indica en `quirks` cuáles le aplican; este
documento da el arreglo copiable para cada uno. Filtrar `catalog.json` por `quirks` permite configurar el cliente
antes de la primera petición.

## tls-chain-incomplete: certificados FNMT sin intermedio

Muchos servidores públicos (airef.es, tesoro.es, registrodelicitadores.gob.es, energia.gob.es, mites.gob.es,
universidades.gob.es, wms.mapama.gob.es, pestadistico.inteligenciadegestion.sanidad.gob.es) presentan solo el
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
cat "$(python3 -c 'import certifi;print(certifi.where())')" fnmt-intermedios.pem > ca-age.pem
curl --cacert ca-age.pem -A "Mozilla/5.0" "https://www.tesoro.es/deuda-publica/estadisticas"
```

```python
import requests
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, verify="ca-age.pem", timeout=30)
```

O bien `export REQUESTS_CA_BUNDLE=ca-age.pem` y `export SSL_CERT_FILE=ca-age.pem` para todo el proceso. La lista
completa de certificados de FNMT está en https://www.sede.fnmt.gob.es/descargas/certificados-raiz-de-la-fnmt.

## user-agent-browser

Enviar siempre un User-Agent de navegador. tesoro.es responde 403 al User-Agent por defecto de curl y de
urllib; otros sitios devuelven páginas distintas. `curl -A "Mozilla/5.0"`, `headers={"User-Agent": "Mozilla/5.0"}`.

## accept-header-required

Las APIs del BOE (sumarios, legislación consolidada, BORME) exigen `Accept: application/json` o
`Accept: application/xml`. Sin cabecera, o con `*/*`, responden 400. Los errores llegan siempre en XML aunque se
haya pedido JSON; comprobar el código HTTP antes de parsear.

## gzip-unannounced

La API del Banco de España comprime siempre en gzip. Si el cliente no envía `Accept-Encoding`, el cuerpo llega
comprimido sin `Content-Encoding`. `curl --compressed` lo resuelve; requests envía la cabecera por defecto y
descomprime solo; con urllib usar `gzip.decompress(resp.read())` si los dos primeros bytes son `1f 8b`.

## latin1

Feeds RSS del BOE y CSV del Banco de España van en ISO-8859-1. `curl ... | iconv -f ISO-8859-1 -t UTF-8`,
`pd.read_csv(url, encoding="latin-1")`, `resp.content.decode("latin-1")`.

## viewstate-forms

Portal de la CNMV (ASP.NET Web Forms). Para automatizar una búsqueda: GET de la página del formulario, extraer
los campos ocultos `__VIEWSTATE`, `__VIEWSTATEGENERATOR` y `__EVENTVALIDATION`, y reenviarlos en el POST junto
con los campos del formulario (nombres `ctl00$...`). Mantener la sesión de cookies entre GET y POST.

## waf-blocks-bots

El buscador BIEST del Banco de España (app.bde.es/bie_www) rechaza clientes automatizados con "Request
Rejected" aunque lleven User-Agent de navegador. No hay arreglo; usar la API y los catálogos CSV de la ficha.

## waf-intermittent-403

El portal de la Seguridad Social (Akamai) responde 403 "Acceso denegado" a una de cada dos o tres peticiones
legítimas, también en las descargas de ficheros, y 200 a la siguiente. Reintentar la misma URL tras 2 a 5
segundos, con las mismas cabeceras (User-Agent y Accept-Language de navegador). No es un límite de ritmo: una
petición aislada también puede recibir el 403.

## session-required

Hacienda (aplicación de presupuestos de entidades locales, SGCIEF) devuelve "sesión expirada" a cualquier URL de
descarga pedida directamente, incluso con cookies y Referer, porque la sesión se crea en la navegación por el
menú; automatizar con navegador (Playwright). REGCON (convenios colectivos) es más simple: GET del formulario,
conservar cookies y reenviar el token consulta_token_value_id en el POST.

## js-rendered

Contenido generado en el navegador. Antes de lanzar un navegador sin cabeza, mirar en las herramientas de red
qué llamadas XHR hace la página: casi siempre devuelven JSON y se pueden replicar con requests. Ninguna fuente
verificada hasta ahora lo exige.

## static-html

Lo contrario: el HTML servido ya contiene los enlaces a los ficheros. Un GET más una expresión regular sobre
href, o lxml, bastan. Es el caso de AIReF, Tesoro, AEAT, IGAE, Hacienda local, INE, MITES, SEPE y Seguridad
Social. Rascar la página en cada ejecución cuando además tenga url-drift.

## errors-html-or-xml

BOE (errores siempre en XML), INE (404 y 500 en HTML) y BDNS (404 de Tomcat en HTML) no devuelven el error en el
formato pedido. Comprobar el código HTTP antes de parsear y no confiar en Content-Type.

## url-drift y overwritten-in-place

Dos estrategias de caché opuestas. Con url-drift (AIReF, ICO, CNMV, Hacienda local, Seguridad Social) la URL del
fichero cambia en cada publicación: no fijar enlaces, localizarlos en la página cada vez. Con overwritten-in-place
(Tesoro, AEAT, SEPE) la URL es fija pero el contenido se sustituye: guardar copia fechada si se necesita el
histórico de publicaciones o de revisiones.

## json-object-or-list

En las APIs del BOE y BORME, `item`, `departamento`, `epigrafe` y `apartado` son un objeto cuando hay un
elemento y una lista cuando hay varios. Normalizar: `x if isinstance(x, list) else [x]`.

## no-weekend-data

BOE y BORME no se publican domingos ni festivos (BORME tampoco sábados); la API devuelve 404 esos días. Al
iterar fechas, tratar 404 como día sin publicación, no como error. Algún día antiguo devuelve 500; reintentar
una vez y saltar.

## Ritmo de peticiones

Ninguna de las fuentes verificadas documenta límites ni devolvió 429 durante la verificación. Regla prudente
para descargas masivas: peticiones secuenciales por host, reintento con espera exponencial (2, 4, 8 s) ante
5xx y ante cortes de conexión, y cachear en local lo descargado, porque varias fuentes sobreescriben ficheros
en la misma URL (cuadros mensuales del Tesoro) o mueven las rutas (uploads de AIReF, documentos del ICO).
