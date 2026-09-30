# Resultados de la evaluación · 2026-09-30

Cinco tareas de `tareas.yaml`, cada una resuelta una vez sin catálogo (A) y una vez con catálogo (B) por el mismo modelo
(agente Claude con Bash, curl y python en un sandbox; en B lee `llms.txt` entero y después solo la ficha, receta o índice que
necesita). Tokens y usos de herramienta son los que reporta el arnés para cada agente; llamadas y fallidas las declara el propio
agente en su informe y se han contrastado con la llamada de referencia de `tareas.yaml`.

| tarea | cond. | correcta | llamadas HTTP | fallidas | tokens | usos de herramienta | segundos |
|---|---|---|---|---|---|---|---|
| ipc-ultimo | A | sí | 9 | 0 | 55.838 | 8 | 103 |
| ipc-ultimo | B | sí | 2 | 0 | 68.209 | 6 | 66 |
| poblacion-abengibre | A | sí | 8 | 2 | 55.979 | 9 | 113 |
| poblacion-abengibre | B | sí | 2 | 0 | 70.554 | 5 | 66 |
| gasolinera-mas-barata | A | sí | 2 | 0 | 50.511 | 5 | 55 |
| gasolinera-mas-barata | B | sí | 2 | 0 | 70.824 | 7 | 78 |
| boe-disposiciones-dia | A | sí | 3 | 0 | 49.256 | 6 | 59 |
| boe-disposiciones-dia | B | sí | 4 | 0 | 71.022 | 9 | 110 |
| direccion-a-codigo-ine | A | sí | 1 | 0 | 46.780 | 3 | 35 |
| direccion-a-codigo-ine | B | sí | 1 | 0 | 65.863 | 5 | 52 |

| total | cond. | correctas | llamadas | fallidas | tokens | usos de herramienta | segundos |
|---|---|---|---|---|---|---|---|
| 5 tareas | A | 5/5 | 23 | 2 | 258.364 | 31 | 365 |
| 5 tareas | B | 5/5 | 11 | 0 | 346.472 | 32 | 372 |

## Notas por tarea

- ipc-ultimo (A): acierta al final, pero 6 de las 9 llamadas fueron a la serie IPC251852 (base 2021, cerrada en diciembre de 2025) que recordaba de memoria
- ipc-ultimo (B): 104,638 de 2026M08 con nult=2 por la trampa documentada; comprobó que septiembre solo tiene avance
- poblacion-abengibre (A): 753 (2025) por la tabla provincial 2855; dos URL de INEbase adivinadas dieron 404
- poblacion-abengibre (B): 753 (2025) con tv=19:6124 de la receta; comprobó vigencia de la tabla
- gasolinera-mas-barata (A): API MINETUR de memoria; 1,735 en Iniesta, coincide con la referencia
- gasolinera-mas-barata (B): 1,735 en Iniesta; leyó ficha, receta y códigos
- boe-disposiciones-dia (A): API del BOE con Accept de memoria; detecta que no hay sección I ese día
- boe-disposiciones-dia (B): sin sección I ese día; lo contrastó con XML, HTML y el día anterior como control
- direccion-a-codigo-ine (A): CartoCiudad de memoria; muniCode 28079, provinceCode 28
- direccion-a-codigo-ine (B): CartoCiudad desde la ficha cnig; leyó llms.txt, la ficha y una receta

## Lectura

- Las cinco tareas son de las fáciles del catálogo (fuentes con API que el modelo ya conoce): el acierto fue 5 de 5 en
  las dos condiciones. La diferencia está en el camino: con catálogo, 11 llamadas HTTP frente a 23, y ninguna fallida
  o inútil frente a 8 (dos 404 por URL adivinadas y seis a una serie del IPC cerrada en 2025 que el modelo recordaba).
- El catálogo costó un 34 % más de tokens (346.472 frente a 258.364) porque cada agente leyó `llms.txt` entero
  (unos 9.000 tokens) más una ficha y una receta. Ese es el coste a recortar: el servidor MCP (`guides/servidor-mcp.md`)
  carga solo la ficha o receta que hace falta y evita el fichero completo.
- No se midieron las tareas donde el catálogo cambia el resultado y no solo el camino (clave de AEMET, CODICE de
  PLACSP, códigos de país de DataComex, bloqueo por IP del Catastro); quedan para la siguiente pasada.
- Una sola ejecución por tarea y condición, mismo modelo y mismo sandbox; con n=5 los totales orientan, no demuestran.
