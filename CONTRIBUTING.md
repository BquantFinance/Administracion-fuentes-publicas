# Contribuir

## Añadir una fuente

1. Copia `templates/source.yaml` a `sources/<sector>/<id>.yaml`. El `id` es kebab-case, empieza por el organismo o siglas y coincide con el nombre del fichero. Ej.: `ine-api-tempus`, `boe-api-sumario`.
2. Rellena solo con información contrastada en la documentación oficial o probada con una llamada real. Si has probado el endpoint, pon la fecha en `verified`. Si no, deja `null`.
3. Sector, acceso, auth, periodicidad y formatos deben estar en `schema/vocab.yaml`. Si falta un valor, propónlo en el mismo PR.
4. Ejecuta:
   ```bash
   pip install -r scripts/requirements.txt
   python scripts/validate.py
   python scripts/build.py
   ```
   y sube también los ficheros generados. El CI falla si no están al día.

## Añadir una receta, una necesidad o una ruta muerta

Los índices de `indices/*.yaml` siguen las mismas reglas que las fichas: solo hechos probados, ids del vocabulario y de
las fichas, castellano en valores. Una receta necesita al menos un `check` que pase con `python scripts/check_recetas.py
--only <id>`; una ruta muerta necesita la fecha de la prueba y, si existe, la sustituta. `validate.py` rechaza
referencias a fichas o identificadores que no existen.

## Criterios de redacción

Las fichas las leen agentes con presupuesto de tokens. Por eso:

- `summary`: qué datos hay y para qué sirven, en una o dos frases. Sin adjetivos, sin historia del organismo.
- `endpoints`: solo los que un desarrollador usa de verdad. Cada uno con un `example` que funcione al copiarlo.
- `quirks`: peculiaridades técnicas del vocabulario cerrado (certificado sin cadena, User-Agent obligatorio, gzip sin cabecera...). Permiten a un agente configurar el cliente HTTP filtrando `catalog.json`. Detalle en `guides/cliente-http.md`.
- `ids`: identificadores que de verdad aparecen en los datos (código INE, NIF, DIR3, CPV, CNAE...), del vocabulario cerrado. Es lo que permite a un agente saber con qué otras fuentes puede cruzar sin abrir el fichero.
- `gotchas`: una frase por trampa. Cabeceras obligatorias, codificaciones, límites, cambios de URL, campos engañosos. Es el campo más valioso del repo.
- Nada que ya esté en otra ficha: usa `related`.
- Castellano en los valores, inglés en las claves. Sin mayúsculas gratuitas, sin markdown dentro de los valores.

## Qué entra y qué no

Entra cualquier fuente cuyo titular sea una Administración pública española y que ofrezca datos reutilizables, aunque sea solo por descarga o consulta web. Se etiqueta `access: portal` o `scraping` cuando no hay API.

No entran fuentes privadas, agregadores de terceros ni servicios de pago, aunque usen datos públicos. Sí entran empresas y fundaciones del sector público estatal cuando publican datos (se indicará en `org`).

## Una fuente que ha cambiado o ha muerto

Abre un issue con la plantilla "Corregir ficha" o envía un PR. Si la fuente ha desaparecido, cambia `status` a `deprecated` y añade en `gotchas` la sustituta si la hay. No borres fichas: sirven de histórico.
