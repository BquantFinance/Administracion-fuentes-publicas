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
5. **Ejemplos copiables.** Cada endpoint principal lleva un `example` que funciona al pegarlo. Con claves,
   usar variable de entorno (`$AEMET_KEY`), nunca una clave real.
6. **Vocabulario cerrado.** Sector, acceso, auth, periodicidad, formatos, estado, quirks e ids salen de `schema/vocab.yaml`.
   Si falta un valor, se añade al vocabulario en el mismo commit, no se improvisa.
7. **Castellano en valores, inglés en claves.** Sin markdown dentro de los valores. Sin dos puntos seguidos de
   espacio en valores sin comillas, porque rompe el YAML.
8. **Fuente única de verdad.** Solo se editan `sources/**/*.yaml`, `guides/*.md`, `schema/` y `scripts/`.
   `catalog.json`, `llms.txt`, `llms-full.txt`, los `README.md` de sector y la tabla del README raíz se
   regeneran con `python scripts/build.py` y se suben en el mismo commit.
9. **No borrar fichas.** Una fuente muerta pasa a `status: deprecated` con la sustituta en `gotchas`.
10. **Rendimientos decrecientes.** Si un sector solo tiene portales sin API y datos que ya da el INE, una
    ficha o ninguna. Mejor 50 fichas exactas que 500 aproximadas.

## Flujo de trabajo

```bash
pip install -r scripts/requirements.txt
python scripts/validate.py        # esquema, vocabulario, ids, referencias
python scripts/build.py           # regenera todo lo derivado
python scripts/check_links.py     # informe de URLs (necesita red)
```

Antes de cada commit: validate y build limpios. Commits pequeños por sector o por lote verificado.
Sin subagentes salvo petición expresa: el trabajo es secuencial y de precisión.

## Orden de prioridad

Top-down por impacto: primero las fuentes con API y datos únicos de uso masivo (BOE, INE, AEAT, contratación,
subvenciones, catastro, meteorología, medicamentos), después las de descarga estructurada, al final los portales
sin API. Dentro de cada sector, la misma lógica.

Alcance actual: Administración General del Estado, incluidos organismos independientes adscritos (BdE, CNMV,
CNMC, AIReF) y empresas públicas cuando publican datos únicos (Aena, Puertos del Estado). Fases siguientes,
solo cuando el propietario lo indique: Cortes y Poder Judicial, comunidades autónomas, entidades locales, UE.

## Estado de verificación

Las 67 fichas iniciales se verificaron endpoint a endpoint el 2026-09-30: 63 llevan fecha en `verified` y 4
siguen en `null` (aemet-opendata exige clave de API; fega-beneficiarios-pac, oepm-invenes y el host de datos de
mitma-opendata-movilidad no respondieron desde el entorno de verificación). Al empezar una sesión con red,
re-verificar primero esas cuatro y las fichas en `degraded` o `unknown`; después añadir fuentes nuevas por
impacto. Las verificaciones se hacen con el bundle FNMT y el User-Agent de navegador que describe
`guides/cliente-http.md`.

## Lo que no se hace

- No se añaden agregadores privados, servicios de pago ni datos de terceros sobre datos públicos.
- No se escriben guías largas. Una guía transversal entra solo si condensa algo que afecta a muchas fuentes
  (identificadores, codificaciones, autenticación con certificado).
- No se genera prosa de relleno en README ni en fichas para que "parezca completo".
