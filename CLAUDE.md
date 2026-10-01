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
   `scripts/` y `evals/`. `catalog.json`, `llms.txt`, `llms-full.txt`, `indices/README.md`, los `README.md` de sector y la
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
CNMC, AIReF) y empresas públicas cuando publican datos únicos (Aena, Puertos del Estado). Fases siguientes,
solo cuando el propietario lo indique: Cortes y Poder Judicial, comunidades autónomas, entidades locales, UE.

## Estado de verificación

85 fichas verificadas endpoint a endpoint el 2026-09-30 (82 con fecha en `verified`; `null` en fega-beneficiarios-pac,
oepm-invenes y mitma-opendata-movilidad, que no respondieron desde el entorno). Las 43 recetas se comprobaron ese día
desde GitHub Actions (`verificacion.yml`, 87 de 89 comprobaciones ok; Catastro cerró la conexión y datos.gob.es estaba
en mantenimiento). Hosts que rechazan IP de centros de datos, verificados desde GitHub y desde el entorno: Catastro,
REData y datos.gob.es (Incapsula), BNE, FEGA, OPI de inclusion.gob.es (Akamai), ENAIRE (F5), infoelectoral, DGSFP e
Instituciones Penitenciarias; se re-verifican desde una IP residencial. ESIOS sigue pendiente de token. Al empezar una
sesión con red, re-verificar primero esas fuentes y las fichas en `degraded` o `unknown`; después añadir fuentes nuevas
por impacto. Las verificaciones se hacen con el bundle FNMT y el User-Agent de navegador que describe
`guides/cliente-http.md`. `verificacion.yml` (cron semanal y ejecución manual) solo corre desde la rama por defecto del
repositorio.

## Siguientes pasos, por orden de retorno (2026-10-01)

Diagnóstico honesto tras la primera evaluación (`evals/resultados-2026-09-30.md`): en tareas fáciles con un modelo
potente el catálogo no cambia el acierto; ahorra la mitad de llamadas y evita las fallidas. Las cifras de tokens de
las dos primeras tandas medían el contexto final de cada agente, no el consumo (corregido el 2026-10-01 en `evals/`).
El valor está concentrado en las trampas no deducibles, las rutas muertas y los códigos internos, y solo vale si las
fichas son exactas: la auditoría del 2026-10-01 encontró errores en fichas marcadas como verificadas (exportación de
la BDNS que se queda en 50 filas, BOE en festivos, nivel1 de la BDNS). Orden acordado con el propietario el
2026-10-01: dejarlo presentable antes de medir (correcciones y auditoría, registros MCP, verificación, comunidades
autónomas) y las evaluaciones al final.

1. **Medir donde importa.** Hecho el 2026-10-01 (`evals/resultados-2026-10-01.md`): tareas difíciles con el modelo por
   defecto y con Sonnet, y entrada ligera. Mismo acierto; con catálogo, la mitad de llamadas y casi ninguna fallida.
   Pendiente, al final: tanda con tokens bien medidos (suma de usage por turno en
   `~/.claude/projects/<proyecto>/<sesión>/subagents/agent-*.jsonl`, no el total del arnés), condición MCP, Haiku,
   tareas con trampas silenciosas y tres repeticiones; Catastro bloqueado.
2. **Distribución antes que más fichas.** Hecho el 2026-10-01 lo instalable: `pipx install git+...` o `uvx` dan el
   comando `mcp-catalogo`, que descarga `catalog.json` si no hay copia local (`guides/servidor-mcp.md`). Pendiente: alta
   en los registros de MCP (Smithery, Glama, registro oficial) y bloque de configuración para Cursor.
3. **Entrada ligera.** Hecho el 2026-10-01: `build.py` genera `llms-min.txt` (7 KB) y la segunda tanda lo midió.
4. **Código listo, no solo descripciones.** Hecho el 2026-10-01: `scripts/clientes/` con BOE y BORME (`boe.py`), BDNS
   (`bdns.py`), AEMET, INE Tempus, DataComex, PLACSP y Saiku, probados con llamadas reales; `scripts/clientes/muestras/`
   con respuestas reales recortadas y `python scripts/test_clientes.py`, sin red, en CI; `verificacion.yml` ejecuta los
   cargadores contra los servidores cada semana. Pendiente: muestras de ObtenerDatos de DataComex y del fichero de datos
   de AEMET (necesitan credenciales) y cargador de Catastro (desde una IP residencial).
5. **Cobertura con demanda real.** Comunidades autónomas por tamaño (Madrid, Cataluña, Andalucía, Comunidad
   Valenciana) y los portales de datos de Madrid y Barcelona, que tienen API; antes que el resto de la AGE.
6. **Mantenimiento con dueño.** Una sesión mensual que corra `verificacion.yml`, arregle lo roto y pase la ronda desde
   una IP residencial para los hosts que bloquean centros de datos (lista en «Estado de verificación»). Sin esto, el
   catálogo caduca; un catálogo con errores es peor que ninguno.
7. **Trampas de la comunidad.** Hecho el 2026-10-01: plantilla de issue «trampa nueva» (`.github/ISSUE_TEMPLATE/trampa.yml`).
   Cada trampa confirmada entra en la ficha con fecha.

Marcar aquí lo hecho con fecha para que la siguiente sesión no lo repita.

## Estado al cierre de la sesión del 2026-10-01 (para retomar)

- Ramas: `main` es la rama por defecto y contiene todo; `claude/magical-volta-cjszgk` es la rama de trabajo de la
  sesión anterior, idéntica a `main` al cierre. Las siguientes sesiones pueden trabajar directamente en `main` o en una
  rama nueva; `claude/eager-albattani-9me81y` es antigua y se puede borrar.
- CI: `ci.yml` (validate y build en cada push) y `verificacion.yml` (lunes 06:17 UTC y manual; recetas y enlaces
  desde la IP de GitHub; abre un issue si algo falla). La clave `AEMET_KEY` está como secreto del repositorio.
- Credenciales fuera del repo: cuenta de DataComex con el correo del propietario (API probada); clave de AEMET
  (secreto de GitHub). ESIOS sin token. Nada de esto se escribe en fichas ni commits.
- Evaluación: `evals/tareas.yaml` (20 tareas), `evals/resultados-2026-09-30.md` y `evals/resultados-2026-10-01.md`.
  Las ejecuciones se hicieron con subagentes del propio arnés (tokens y usos de herramienta del arnés); no hay
  ejecutor en el repo.
- `scripts/clientes/`: boe, bdns, ine_tempus, placsp y saiku probados el 2026-10-01 con llamadas reales desde el
  entorno; aemet (rehecho: sin clave fallaba con KeyError y dependía del Content-Type) se prueba con el secreto en
  `verificacion.yml`; datacomex sin probar de nuevo (sin credenciales en el entorno). Corregidos ese día: placsp
  ignoraba las anulaciones (at:deleted-entry) e ine_tempus.ultimo_valor devolvía el periodo más antiguo.
- Hallazgos de la evaluación ya volcados en fichas: catálogos de DataComex (ObtenerPaises, ObtenerTarics...), tabla
  nacional 30824 del Atlas con filtros tv, item de la sección 5C del BOE bajo departamento.texto, regeneración
  diaria del feed de PLACSP y buscador JSF como vía para lo publicado hoy.
- Siguiente trabajo, en este orden (acordado el 2026-10-01): auditoría a fondo de las fichas de uso masivo; alta del MCP
  en registros y configuración para Cursor (punto 2); verificación y ronda desde IP residencial (punto 6); comunidades
  autónomas por tamaño y portales de Madrid y Barcelona (punto 5); evaluación con tokens bien medidos (punto 1).

## Lo que no se hace

- No se añaden agregadores privados, servicios de pago ni datos de terceros sobre datos públicos.
- No se escriben guías largas. Una guía transversal entra solo si condensa algo que afecta a muchas fuentes
  (identificadores, codificaciones, autenticación con certificado).
- No se genera prosa de relleno en README ni en fichas para que "parezca completo".
