# Instrucciones para agentes que trabajan en este repo

## Objetivo

Una aceleradora de startups de datos públicos (decisión del propietario, 2026-10-01): que un fundador, un desarrollador
o su agente pase de la idea a un producto sobre datos públicos españoles lo antes posible. Eso pide cuatro cosas, y todo
lo que entra en el repo sirve a alguna:

1. Encontrar el dato: fichas exactas, `buscar` en el MCP, índices.
2. Traerlo resuelto: clientes, herramientas MCP que devuelven datos, almacén local, ejemplos que funcionan.
3. Saber si se puede vender: licencia de cada fuente, `guides/reutilizacion.md`.
4. Mantenerlo al día: campo `sync` de las fichas, filtros por fecha de alta, descarga condicional.

`indices/productos.yaml` dice qué se puede construir hoy y con qué piezas; es la portada del README. Criterio para
añadir algo: ahorra tiempo o errores a quien construye, y si es una herramienta o un índice nuevo, se mide (evals/)
antes de darlo por bueno. Mejor pocas piezas que funcionan que muchas a medias.

## Reglas de contenido

1. **Solo lo esencial.** Una fuente entra si alguien construiría sobre ella. Un dato entra en la ficha si cambia cómo
   se programa contra la fuente. Historia del organismo, adjetivos y contexto institucional, fuera.
2. **Verificar antes de escribir.** Toda URL, endpoint, parámetro, formato y cifra se prueba con una llamada real. Si
   responde, `verified` lleva la fecha; si no se puede probar, `verified: null` y el motivo en `gotchas`. Nunca inventar
   endpoints ni parámetros plausibles. Un intento fallido se escribe «no localizado» o «no conseguido», con lo probado
   y la fecha; «no existe» solo si lo dice la documentación oficial o el servidor (404, 410, 401).
3. **Las trampas son el valor.** `gotchas`, una frase por trampa: cabeceras, codificaciones, decimales con coma, límites
   no documentados, ids que no coinciden, URLs que cambian. Las trampas silenciosas (datos incompletos, distintos o a
   cero sin error) van en `alerts`, como mucho tres por ficha y sin repetirse en `gotchas`, y cada una dice la operación
   exacta con un ejemplo de números comprobados: la evaluación del 2026-10-01 mostró que una alerta que solo describe
   no cambia el resultado y la explícita sí.
4. **`tips` solo si acelera**, como mucho seis. Histórico y sincronización van en `sync` (since, full, size, new), solo
   con medidas propias y la muestra dicha si la cifra es estimada.
5. **Ejemplos copiables y respuesta descrita.** Cada endpoint principal lleva `example` que funciona al pegarlo y
   `returns` con la forma vista en esa llamada. Con claves, variable de entorno (`$AEMET_KEY`), nunca la clave.
6. **Vocabulario cerrado** (`schema/vocab.yaml`) para sector, acceso, auth, periodicidad, formatos, estado, quirks e ids;
   si falta un valor, se añade en el mismo commit.
7. **Castellano en valores, inglés en claves.** Sin markdown dentro de los valores ni dos puntos seguidos de espacio en
   valores sin comillas.
8. **Fuente única de verdad.** Se editan `sources/**/*.yaml`, `indices/*.yaml`, `guides/*.md`, `schema/`, `scripts/`,
   `evals/`, `ejemplos/`, `plugins/`, `.claude-plugin/`, `.github/`, la cabecera del README y los ficheros de
   distribución (`pyproject.toml`, `server.json`, `glama.json`, `Dockerfile`, `mcpb/`). `python scripts/build.py`
   regenera y se sube en el mismo commit: `catalog.json`, `llms-min.txt`, `llms.txt`, `llms-full.txt`,
   `indices/README.md`, los README de sector, las tablas AUTO del README, la lista de herramientas de
   `guides/servidor-mcp.md` y de `mcpb/manifest.json` (sacadas de las docstrings de `scripts/mcp_catalogo.py`).
   `datos/municipios.csv` lo genera `python scripts/municipios.py`.
9. **No borrar fichas.** Una fuente muerta pasa a `status: deprecated` con la sustituta en `gotchas`.
10. **Rendimientos decrecientes.** Mejor 50 fichas exactas que 500 aproximadas; un sector sin API y con datos que ya da
    el INE, una ficha o ninguna.
11. **Superficie pequeña y respuestas compactas.** Antes de una herramienta MCP nueva, ver si cabe en una existente
    (`buscar` cubre fichas, recetas, necesidades, productos e identificadores; `ficha(id)` da el detalle de todos). Las
    definiciones se pagan en cada turno (13 herramientas, unos 1.550 tokens el 2026-10-01) y las respuestas en cada
    llamada: JSON sin sangría ni copia estructurada, tablas en columnas, sin campos que repiten lo ya sabido y textos
    largos cortados. `test_mcp_catalogo.py` falla si se pasan los presupuestos de tamaño. El contenido sigue en
    castellano: en prosa el inglés ahorraba un 8 a 15 % de tokens, menos que el formato, y las fichas citan literales
    de la fuente que no se traducen.

## Flujo de trabajo

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py        # esquema, vocabulario, ids, referencias (sale con 1 si falla; no encadenar con | tail)
python scripts/build.py           # regenera todo lo derivado
python scripts/test_clientes.py   # parsers y clientes contra muestras reales, sin red (CI)
python scripts/test_mcp_catalogo.py  # el servidor MCP por stdio llamando a todas las herramientas (red; fuera de CI)
python scripts/check_recetas.py   # comprobaciones de las recetas (red; --only, --report, --fail)
python scripts/check_ejemplos.py  # example de cada endpoint de las fichas (red; --only, --report, --fail)
python scripts/check_links.py     # informe de URLs (red)
python scripts/municipios.py      # regenera datos/municipios.csv (red, un par de minutos)
python scripts/fnmt_bundle.py     # ca-age.pem con las CA de FNMT para los hosts con cadena incompleta
```

Antes de cada commit, validate y build limpios. Commits pequeños por lote verificado, en castellano. Sin subagentes
salvo petición expresa o para evaluaciones.

## Índices (`indices/`)

`validate.py` comprueba que solo citan ids de fichas, recetas y vocabulario.

- `productos.yaml`: qué se puede construir hoy, para quién, con qué fichas, recetas y código, frescura, volumen medido,
  licencia y la trampa principal. Solo productos cuyas piezas existen y funcionan.
- `recetas.yaml`: procedimiento que cruza dos o más fuentes o esquiva una trampa; cada paso cita una ficha y cada
  receta lleva al menos un `check` que `check_recetas.py` ejecuta.
- `necesidades.yaml`: una línea por necesidad habitual con la ficha que la resuelve y la nota que evita el desvío.
- `identificadores.yaml`: formato, regex, ejemplo, emisor y cruces verificados de cada id del vocabulario.
- `rutas-muertas.yaml`: URL antigua comprobada como muerta, estado, sustituta y fecha.
- `codigos.yaml`: valores que una API exige y no se adivinan, obtenidos con una llamada real.

## Alcance

AGE con organismos independientes (BdE, CNMV, CNMC, AIReF) y empresas públicas con datos únicos (Aena, Puertos);
Madrid, Cataluña, Andalucía y Comunitat Valenciana (portal e instituto de estadística) y los ayuntamientos de Madrid y
Barcelona. Desde el 2026-10-05 (propietario): entran también comunidades y ayuntamientos que aporte la comunidad si
llegan verificados con llamadas reales, con alertas explícitas y validate y build limpios (issues 4 y 6). Cortes, Poder
Judicial o UE, solo cuando lo indique el propietario.

## Estado (2026-10-01)

- **Catálogo**: 95 fichas, 88 verificadas el 2026-10-01. En 2026-09-30 siguen datacomex (sin token), ree-redata y
  datos-gob-es-api (Incapsula) y bne-datos (Cloudflare); en `null`, fega-beneficiarios-pac, oepm-invenes y
  mitma-opendata-movilidad. 43 recetas, 12 productos.
- **Hosts que rechazan IP de centros de datos**: Catastro, REData, www.ree.es, ESIOS, datos.gob.es, BNE, FEGA, OEPM,
  movilidad-opendata.mitma.es, geoserver.iepnb.es, sivira.isciii.es, analisis.cis.es y www.inmujer.es; intermitentes
  Seguridad Social, renfe, DATAESTUR, indicadores.fecyt.es e IECA; desde GitHub, MINETUR y Catastro. PLACSP
  (contrataciondelestado.es y contrataciondelsectorpublico.gob.es) bloqueó el 2026-10-01 esta IP y la de GitHub con 200
  y la página de su WAF en atom y ZIP, al menos de 17:24 a 17:42 UTC; a las 16:57 y a las 19:46 servía el feed (temporal). Se re-verifican
  desde una IP residencial (pendiente). Verificación desde GitHub del 2026-10-01: sobre 42998e7, recetas 88 de 93
  (Catastro, MINETUR, DGT y un corte de GBIF) y ejemplos de fichas 368 de 380 (429 de AEMET, 504 de DATAESTUR); sobre
  5b79d2d, recetas 91 de 93 (MINETUR) y ejemplos 367 de 380 (CIMA con un 500 y un timeout, 10 de 10 al repetir; DATAESTUR), y los cargadores
  de PLACSP daban 0 sin error por el WAF (ahora lanzan Bloqueado). El 2026-10-05, a mano sobre f4bfeab (el cron de los
  lunes 06:17 no se disparó; sin ninguna ejecución schedule hasta entonces): recetas 92 de 93 (429 de AEMET), ejemplos
  364 de 380 (timeouts del IECA y cortes de la Junta de Andalucía) y cargadores bien salvo ckan.py, porque la Comunidad
  de Madrid sacó padron_por_sexo del datastore el 04/10 (corregido).
- **Evaluación** (`evals/`): con Haiku y trampas silenciosas, acierto 3 de 21 sin catálogo, 10 con ficheros y 13 con
  MCP, con un 30 % y un 43 % menos de tokens de entrada. Cuarta tanda (2026-10-05): con `perfil_municipio`, `coyuntura`
  y `empresa_nif`, 8 de 8 frente a 4 de 8 sin ellas, un 75 % menos de tokens y un tercio del tiempo. Sin medir aún:
  productos y almacén.
- **Publicación**: releases v0.1.0 a v0.3.0 y entrada `io.github.BquantFinance/catalogo-fuentes-publicas` en el registro
  oficial de MCP. Para otra versión, subir la versión en `server.json`, `pyproject.toml` y `mcpb/manifest.json` (y en
  los dos ficheros del plugin) y crear la release vX.Y.Z desde la web; `publicar-mcp.yml` empaqueta, adjunta y publica.
  v0.4.0 y v0.5.0 (respuestas compactas) publicadas el 2026-10-01 (registro oficial, sha256 del .mcpb coincide). 0.6.0
  publicada el 2026-10-05 con la etiqueta `0.6.0`, sin v, sobre 92b68dc (registro, sha256 e instalación desde la etiqueta
  comprobados); un primer intento sobre 46911a0 falló porque los ficheros seguían en 0.5.0: la versión se sube en main
  antes de crear la release, que usa el código de la etiqueta. v0.7.0 (radar, directorio NIF y nombre, SIGPAC en
  ubicaciones, PR 5 de seguridad) publicada el 2026-10-05 sobre f9bcc8a: registro, sha256 y `pip install ...@v0.7.0` con
  `fuentes-radar` comprobados; es la versión que instala la plantilla ejemplos/radar/radar-workflow.yml.
- **CI**: `ci.yml` (validate, build al día y `test_clientes.py` en cada push) y `verificacion.yml` (lunes 06:17 UTC,
  manual y al cambiar el flujo: recetas, ejemplos de fichas, cargadores, ejemplos y enlaces desde la IP de GitHub;
  comenta en el issue de verificación si algo falla). Secreto `AEMET_KEY` en el repositorio.
- **Credenciales fuera del repo**: cuenta de DataComex con el correo del propietario y clave de AEMET (secreto de
  GitHub); ESIOS sin token. Nunca en fichas ni commits.
- **Ramas**: `main` por defecto; `claude/vibrant-bell-jwqfvl` de trabajo, igual que main.

## Siguiente

1. Medir lo que falta (productos y almacén) con y sin las piezas; lo que no ahorre tiempo o errores, se quita. Hecho el
   2026-10-05 para `perfil_municipio`, `coyuntura` y `empresa_nif` (se quedan).
2. Ronda desde una IP residencial para los hosts bloqueados (necesita al propietario).
3. Productos nuevos solo con piezas que ya funcionen; fuentes nuevas solo si desbloquean un producto.

## Lo que no se hace

- Datos alojados en el repo ni releases de datos: el almacén es local y `almacen/` está en `.gitignore`.
- Agregadores privados, servicios de pago o datos de terceros sobre datos públicos.
- Guías largas: una guía entra solo si condensa algo que afecta a muchas fuentes.
- Prosa de relleno en README o fichas para que parezca completo.
