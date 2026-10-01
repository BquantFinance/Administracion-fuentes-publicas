# Instrucciones para agentes que trabajan en este repo

## Qué es esto

Un catálogo de fuentes de datos de la Administración pública española, escrito para que lo consuman agentes de IA
y desarrolladores que construyen encima. No es documentación divulgativa. Es un mapa operativo: qué hay, dónde
está, cómo se llama, qué devuelve, qué falla.

## Objetivo que manda sobre todo lo demás

Máxima utilidad para construir, investigar y desarrollar sobre datos públicos, con el mínimo de tokens.
Cada línea que no ahorre una búsqueda, una prueba fallida o una hora de depuración a quien la lea, sobra.

## Reglas de contenido

1. **Solo lo esencial.** Una fuente entra si un builder la usaría. Un dato entra en la ficha si cambia cómo se
   programa contra la fuente. Historia del organismo, adjetivos, contexto institucional: fuera.
2. **Verificar antes de escribir.** Toda URL, endpoint, parámetro y formato se prueba con una llamada real
   antes de afirmarse. Si responde, `verified` lleva la fecha de hoy. Si no se puede probar, `verified: null`
   y se dice por qué en `gotchas`. Nunca inventar endpoints ni parámetros plausibles. Un intento fallido de
   automatizar no demuestra que no se pueda: se escribe «no localizado» o «no conseguido», con lo probado y la
   fecha, nunca «no existe» o «no es posible», salvo que lo diga la documentación oficial o el propio servidor
   (404, 410, 401).
3. **Las trampas son el valor.** `gotchas` recoge lo que la documentación oficial no dice: cabeceras
   obligatorias, codificaciones, decimales con coma, límites no documentados, ids que no coinciden entre
   organismos, URLs que cambian, datos que parecen cero y son secreto estadístico. Una frase por trampa.
   Las trampas silenciosas (datos incompletos, distintos o a cero sin error) van en `alerts`, tras `summary`, como
   mucho tres por ficha y sin repetirse en `gotchas`: la evaluación del 2026-10-01 mostró que entre las demás se pierden.
4. **`tips` solo si acelera.** Patrón de uso, librería concreta, cruce típico con otra fuente. Máximo seis.
5. **Ejemplos copiables y respuesta descrita.** Cada endpoint principal lleva un `example` que funciona al
   pegarlo y un `returns` con la forma de la respuesta vista en esa llamada (campos clave, tipos, formato de fecha y
   decimal, paginación), nunca copiada de la documentación. Con claves, usar variable de entorno (`$AEMET_KEY`),
   nunca una clave real.
6. **Vocabulario cerrado.** Sector, acceso, auth, periodicidad, formatos, estado, quirks e ids salen de `schema/vocab.yaml`.
   Si falta un valor, se añade al vocabulario en el mismo commit, no se improvisa.
7. **Castellano en valores, inglés en claves.** Sin markdown dentro de los valores. Sin dos puntos seguidos de
   espacio en valores sin comillas, porque rompe el YAML.
8. **Fuente única de verdad.** Solo se editan `sources/**/*.yaml`, `indices/*.yaml`, `guides/*.md`, `schema/`,
   `scripts/` y `evals/` (`datos/municipios.csv` lo genera `python scripts/municipios.py`, con red; `validate.py` lo comprueba), más los ficheros de distribución del servidor MCP (`pyproject.toml`, `server.json`, `glama.json`,
   `Dockerfile`, `mcpb/`) y `.github/`. `catalog.json`, `llms.txt`, `llms-full.txt`, `indices/README.md`, los `README.md` de sector y la
   tabla del README raíz se regeneran con `python scripts/build.py` y se suben en el mismo commit.
9. **No borrar fichas.** Una fuente muerta pasa a `status: deprecated` con la sustituta en `gotchas`.
10. **Rendimientos decrecientes.** Si un sector solo tiene portales sin API y datos que ya da el INE, una
    ficha o ninguna. Mejor 50 fichas exactas que 500 aproximadas.

## Flujo de trabajo

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py        # esquema, vocabulario, ids, referencias
python scripts/build.py           # regenera todo lo derivado
python scripts/check_links.py     # informe de URLs (necesita red)
python scripts/check_recetas.py   # batería de regresión de las recetas (necesita red; --report, --fail)
python scripts/check_ejemplos.py  # ejecuta el example de cada endpoint de las fichas (necesita red; --only, --muestra, --report, --fail)
python scripts/test_clientes.py   # parsers y clientes de scripts/clientes contra las muestras reales, sin red (corre en CI)
python scripts/municipios.py      # regenera datos/municipios.csv (INE, SIGPAC, DIR3, IGN; necesita red, un minuto)
python scripts/fnmt_bundle.py     # genera ca-age.pem (certifi + CA de FNMT) para los hosts con cadena incompleta
python scripts/mcp_catalogo.py    # servidor MCP por stdio sobre catalog.json (guides/servidor-mcp.md); prueba real con test_mcp_catalogo.py, fuera de CI
```

Antes de cada commit: validate y build limpios. Commits pequeños por sector o por lote verificado.
Sin subagentes salvo petición expresa: el trabajo es secuencial y de precisión.

## Índices agregados (`indices/`)

Cinco ficheros que responden a lo que una ficha sola no responde; `validate.py` comprueba que solo citan ids
de fichas y del vocabulario, y `build.py` los vuelca en `indices/README.md`, `llms.txt` y `catalog.json`.

- `recetas.yaml`: procedimiento por intención que encadena fichas. Entra una receta si cruza dos o más fuentes
  o si la vía directa esconde una trampa. Cada paso cita una ficha; cada receta lleva al menos un `check`
  (URL, cabeceras, texto esperado) que `check_recetas.py` ejecuta como regresión. `verified` con fecha solo si
  todos los pasos se probaron; si no, `null` y `note` con lo que falta.
- `necesidades.yaml`: una línea por necesidad habitual con la ficha que la resuelve y la nota que evita el
  desvío típico (FRONTUR es del INE, la EPA no es del SEPE). `source: null` con nota cuando no hay fuente.
- `identificadores.yaml`: una entrada por valor del vocabulario `ids`, con formato, regex, ejemplo, emisor y
  los cruces verificados hacia otras fuentes.
- `rutas-muertas.yaml`: URL antigua que un agente puede recordar, estado observado, sustituta y fecha. Se
  añade una ruta cuando se comprueba que ha muerto, nunca por suposición.
- `codigos.yaml`: valores que una API exige como parámetro y no se adivinan (Id de municipio o provincia del INE
  para `tv`, países de DataComex, estación de AEMET por capital, productos de carburantes, rangos del BOE). Solo
  los de uso frecuente, obtenidos con una llamada real (`verified` obligatorio) y con la llamada que da la lista
  completa en `use`.

## Orden de prioridad

Top-down por impacto: primero las fuentes con API y datos únicos de uso masivo (BOE, INE, AEAT, contratación,
subvenciones, catastro, meteorología, medicamentos), después las de descarga estructurada, al final los portales
sin API. Dentro de cada sector, la misma lógica.

Alcance actual: Administración General del Estado, incluidos organismos independientes adscritos (BdE, CNMV,
CNMC, AIReF) y empresas públicas cuando publican datos únicos (Aena, Puertos del Estado). Desde el 2026-10-01, por
indicación del propietario, también Madrid, Cataluña, Andalucía y Comunitat Valenciana (portal de datos abiertos e
instituto de estadística, level ccaa) y los portales de datos de los ayuntamientos de Madrid y Barcelona (level local).
Fases siguientes, solo cuando el propietario lo indique: resto de comunidades y entidades locales, Cortes y Poder
Judicial, UE.

## Estado de verificación

Auditoría a fondo el 2026-10-01, ficha a ficha y con llamadas reales (agentes por sector que corrigieron fichas y
propusieron cambios en los índices; la sesión principal revisó cada diff, repitió las llamadas dudosas e integró). De
las 95 fichas, 88 llevan `verified` 2026-10-01; datacomex (sin token en el entorno), ree-redata y datos-gob-es-api
(Incapsula) y bne-datos (Cloudflare) siguen en 2026-09-30, y fega-beneficiarios-pac, oepm-invenes y
mitma-opendata-movilidad en `null`. Recetas: 43; desde el entorno el 2026-10-01, 88 de 92 comprobaciones ok (Catastro
sin respuesta tras el proxy, las dos de AEMET omitidas por falta de clave y una de tamaño de la IGAE, que responde a
veces por trozos sin Content-Length; `check_recetas.py` lee ya hasta min_bytes en ese caso). Desde GitHub Actions
(`verificacion.yml`, ejecución del 2026-10-01 sobre 8cc6308): 87 de 89 comprobaciones de recetas ok (MINETUR cortó la
conexión dos veces), ejemplos de las fichas 213 ok de 228 (los fallos eran del analizador de opciones de curl,
corregido después, la exportación de Saiku que necesita sesión, el CKAN de MITECO en despliegue, un 429 de AEMET y dos
cortes de Catastro) y los seis cargadores de `scripts/clientes/` correctos, AEMET incluido con el secreto. Ejecución
manual del mismo día sobre 1db65b2: 92 de 92 recetas, 367 de 379 ejemplos (DATAESTUR 504, DGT lenta, Catastro y dos
ejemplos que leen la cookie de otro paso, que `check_ejemplos.py` ya omite) y los seis cargadores.

Hosts que rechazan o cortan IP de centros de datos (2026-10-01): desde el entorno de agentes, Catastro (403 y error del
proxy), REData, www.ree.es, ESIOS y datos.gob.es (Incapsula), BNE (Cloudflare), FEGA (reset), OEPM (F5),
movilidad-opendata.mitma.es (403), geoserver.iepnb.es (403), sivira.isciii.es, analisis.cis.es y www.inmujer.es
(CONNECT rechazado); con fallos intermitentes, Seguridad Social (Akamai, 403 en la mitad), renfe (TLS), DATAESTUR (504),
indicadores.fecyt.es (TLS) e IECA (reset). Desde GitHub: MINETUR carburantes y Catastro (reset), y antes www.dgt.es y el
nomenclátor de Sanidad (timeout). Del 2026-09-30 siguen pendientes OPI de inclusion.gob.es (Akamai), ENAIRE (F5),
infoelectoral, DGSFP e Instituciones Penitenciarias. Todos se re-verifican desde una IP residencial. ESIOS sigue
pendiente de token. Las verificaciones se hacen con el bundle FNMT y el User-Agent de navegador que describe
`guides/cliente-http.md`. `verificacion.yml` (cron semanal, ejecución manual y push que cambie el propio flujo) ejecuta
recetas, ejemplos de las fichas (`check_ejemplos.py`), cargadores y enlaces, y comenta en el issue de verificación.

## Siguientes pasos, por orden de retorno (2026-10-01)

Diagnóstico honesto tras la primera evaluación (`evals/resultados-2026-09-30.md`): en tareas fáciles con un modelo
potente el catálogo no cambia el acierto; ahorra la mitad de llamadas y evita las fallidas. Las cifras de tokens de
las dos primeras tandas medían el contexto final de cada agente, no el consumo (corregido el 2026-10-01 en `evals/`).
El valor está concentrado en las trampas no deducibles, las rutas muertas y los códigos internos, y solo vale si las
fichas son exactas: la auditoría del 2026-10-01 encontró errores en fichas marcadas como verificadas (exportación de
la BDNS que se queda en 50 filas, BOE en festivos, municipio de SIGPAC que es el del Catastro y no el del INE, CSV de
los portales PC-Axis en UTF-8 y no en Latin-1, descargas que se daban por inexistentes y existen). Orden acordado con
el propietario el 2026-10-01: dejarlo presentable antes de medir (correcciones y auditoría, registros MCP,
verificación, comunidades autónomas) y las evaluaciones al final; todo eso quedó hecho ese día salvo las evaluaciones.

1. **Medir donde importa.** Hecho el 2026-10-01 (`evals/resultados-2026-10-01.md`): tareas difíciles con el modelo por
   defecto y con Sonnet, y entrada ligera. Mismo acierto; con catálogo, la mitad de llamadas y casi ninguna fallida.
   Pendiente, al final: tanda con tokens bien medidos (suma de usage por turno en
   `~/.claude/projects/<proyecto>/<sesión>/subagents/agent-*.jsonl`, no el total del arnés), condición MCP, Haiku,
   tareas con trampas silenciosas y tres repeticiones; Catastro bloqueado.
2. **Distribución antes que más fichas.** Hecho el 2026-10-01 lo instalable: `pipx install git+...` o `uvx` dan el
   comando `mcp-catalogo`, que descarga `catalog.json` si no hay copia local (`guides/servidor-mcp.md`). Preparado el
   mismo día el alta en registros: `server.json` (io.github.BquantFinance/catalogo-fuentes-publicas, validado con
   mcp-publisher), `.github/workflows/publicar-mcp.yml` (al subir una etiqueta vX.Y.Z empaqueta `mcpb/`, lo adjunta a
   una release de GitHub y publica en el registro oficial por OIDC; sin PyPI, que exige 2FA al propietario), `glama.json`,
   `Dockerfile`, alias `fuentes-publicas-mcp`, LICENSE con el texto completo de CC0 (GitHub no detectaba el resumen) y
   bloque de Cursor con botón en la guía. Publicado el 2026-10-01 con la release v0.1.0 (creada desde la web, porque el
   proxy del entorno de agentes no deja subir etiquetas): la entrada del registro oficial está activa y el sha256 del
   .mcpb coincide. Pendiente del propietario: Claim en Glama, imagen de vista previa del repositorio
   (`.github/assets/vista-previa-github.png`) y, si se quiere, cuenta en Smithery y PyPI.
3. **Entrada ligera.** Hecho el 2026-10-01: `build.py` genera `llms-min.txt` (7 KB) y la segunda tanda lo midió.
4. **Código listo, no solo descripciones.** Hecho el 2026-10-01: `scripts/clientes/` con BOE y BORME (`boe.py`), BDNS
   (`bdns.py`), AEMET, INE Tempus, DataComex, PLACSP y Saiku, probados con llamadas reales; `scripts/clientes/muestras/`
   con respuestas reales recortadas y `python scripts/test_clientes.py`, sin red, en CI; `verificacion.yml` ejecuta los
   cargadores contra los servidores cada semana; el 2026-10-01 pasaron los seis desde GitHub, AEMET con el secreto
   (`aemet.py 16078`). Hecho también el 2026-10-01: `sesion.py` (sesión HTTP común con FNMT, User-Agent, reintentos y
   excepción `Bloqueado` ante WAF; `_http.py` queda como compatibilidad y `fnmt_bundle.py` la usa) y clientes genéricos
   `ckan`, `socrata`, `pcaxis`, `arcgis` y `ogc` que paginan sin topes silenciosos, con muestras, pruebas sin red y extra
   de instalación `[clientes]`. Hecho también ese día: campo `alerts` (35 trampas silenciosas movidas desde gotchas
   en 28 fichas; el MCP las devuelve lo primero) y `datos/municipios.csv` con `scripts/municipios.py` (8.132 municipios
   con INE, SIGPAC, DIR3, NIF, NUTS3 y coordenadas; SIGPAC y Catastro numeran distinto que el INE en 4.448 además de
   las 41 capitales con 900) y la herramienta MCP `municipio`. Pendiente: muestras de ObtenerDatos de DataComex y del
   fichero de datos de AEMET (necesitan credenciales) y cargador de Catastro (desde una IP residencial).
5. **Cobertura con demanda real.** Hecho el 2026-10-01: portal de datos e instituto de estadística de Madrid,
   Cataluña (Idescat), Andalucía (IECA) y Comunitat Valenciana (IVE), y portales de los ayuntamientos de Madrid y
   Barcelona (10 fichas, con sus necesidades y códigos). Siguientes comunidades por tamaño solo cuando el propietario lo
   indique.
6. **Mantenimiento con dueño.** Una sesión mensual que corra `verificacion.yml`, arregle lo roto y pase la ronda desde
   una IP residencial para los hosts que bloquean centros de datos (lista en «Estado de verificación»). Sin esto, el
   catálogo caduca; un catálogo con errores es peor que ninguno. Hecho el 2026-10-01: auditoría completa de las 95
   fichas y comprobador de ejemplos (`check_ejemplos.py`) en la verificación semanal. Pendiente: la ronda residencial.
7. **Trampas de la comunidad.** Hecho el 2026-10-01: plantilla de issue «trampa nueva» (`.github/ISSUE_TEMPLATE/trampa.yml`).
   Cada trampa confirmada entra en la ficha con fecha.

Marcar aquí lo hecho con fecha para que la siguiente sesión no lo repita.

## Estado al cierre de la sesión del 2026-10-01 (para retomar)

- Ramas: `main` es la rama por defecto y contiene todo; `claude/vibrant-bell-jwqfvl` es la rama de trabajo de esta
  sesión, idéntica a `main` al cierre. `claude/magical-volta-cjszgk` y `claude/eager-albattani-9me81y` son antiguas y
  se pueden borrar.
- Publicación: release v0.1.0 y entrada `io.github.BquantFinance/catalogo-fuentes-publicas` en el registro oficial de
  MCP. Para otra versión, subir la versión en `server.json`, `pyproject.toml` y `mcpb/manifest.json` y crear la release
  vX.Y.Z desde la web de GitHub; `publicar-mcp.yml` hace el resto.
- CI: `ci.yml` (validate, build y `test_clientes.py` en cada push) y `verificacion.yml` (lunes 06:17 UTC, manual y al
  cambiar el propio flujo; recetas, ejemplos, cargadores y enlaces desde la IP de GitHub; comenta en el issue de
  verificación si algo falla). La clave `AEMET_KEY` está como secreto del repositorio.
- Credenciales fuera del repo: cuenta de DataComex con el correo del propietario (API probada el 2026-09-30); clave de
  AEMET (secreto de GitHub). ESIOS sin token. Nada de esto se escribe en fichas ni commits.
- Evaluación: `evals/tareas.yaml` (20 tareas), `evals/resultados-2026-09-30.md`, `evals/resultados-2026-10-01.md` y
  `evals/consumo.py`, que suma el consumo real por turno desde las transcripciones de los subagentes. No hay ejecutor
  en el repo.
- Imagen y apoyo: logo en `.github/assets/` (claro, oscuro, símbolo y vista previa) y Ko-fi del propietario en
  `.github/FUNDING.yml` y en el README.
- Siguiente trabajo, en este orden: ronda desde una IP residencial para las 7 fichas sin fecha de hoy y los hosts
  bloqueados, y DataComex con token (punto 6); evaluación con tokens bien medidos, condición MCP, Haiku y tres
  repeticiones (punto 1); más comunidades solo cuando lo indique el propietario (punto 5).

## Lo que no se hace

- No se añaden agregadores privados, servicios de pago ni datos de terceros sobre datos públicos.
- No se escriben guías largas. Una guía transversal entra solo si condensa algo que afecta a muchas fuentes
  (identificadores, codificaciones, autenticación con certificado).
- No se genera prosa de relleno en README ni en fichas para que "parezca completo".
