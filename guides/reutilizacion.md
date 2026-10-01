# Reutilización comercial y datos personales

Qué se puede hacer con los datos antes de meterlos en un producto. Las normas se leyeron el 2026-10-01 en la API de
legislación consolidada del BOE (`/datosabiertos/api/legislacion-consolidada/id/{id}/texto/bloque/{bloque}`), salvo el
reglamento europeo, leído en la Oficina de Publicaciones de la UE. Las condiciones de cada sede se leyeron el mismo día y
las cifras salen de llamadas reales. Esta guía no es asesoramiento jurídico. La licencia de cada fuente está en el campo
`license` de su ficha.

## Regla general

- El uso comercial está permitido y es gratuito: la Ley 37/2007 define la reutilización «con fines comerciales o no
  comerciales» (art. 3.1). Solo se cobra el coste marginal, salvo las excepciones del art. 7.2 (organismos que deben
  autofinanciarse, bibliotecas, museos y archivos, sociedades mercantiles públicas).
- En la AGE la modalidad básica es «sin condiciones específicas» (RD 1495/2011, art. 8.1), con las condiciones
  generales del art. 7: no desnaturalizar la información, citar la fuente, mencionar la fecha de la última
  actualización si el original la trae, no sugerir que el organismo participa o patrocina, y conservar los metadatos
  de fecha y condiciones.
- No citar la fuente o la fecha es infracción leve, con multa de 1.000 a 10.000 € en el ámbito de la AGE (Ley 37/2007,
  art. 11.3 y 11.4). Desnaturalizar el sentido de información con licencia es muy grave: de 50.001 a 100.000 €.
- Quien reutiliza responde frente a terceros de los daños que cause el uso (art. 4.7). Los datos pueden corregirse
  después de descargados; la BDNS lo repite en el campo `advertencia` de cada respuesta.
- Comunidades autónomas y ayuntamientos aplican la misma ley con sus condiciones. En los CKAN, cada conjunto declara
  su licencia en `license_id`: filtrar por ese campo antes de usar los datos en un producto.

## Cita literal que pide cada sede

- **BOE y BORME**: «Fuente de los datos: Agencia Estatal Boletín Oficial del Estado» con enlace a https://www.boe.es; en
  obras derivadas, «Basado en datos de la Agencia Estatal Boletín Oficial del Estado». No se puede presentar como
  oficial, y cada texto consolidado reutilizado debe decir que es un texto consolidado de carácter meramente
  informativo (condiciones de reutilización del BOE, licencia tipo del 27 de junio de 2024).
- **AEMET**: «Fuente: AEMET» o «Información elaborada utilizando, entre otras, la obtenida de la Agencia Estatal de
  Meteorología» (nota legal de AEMET).
- **INE**: «Fuente: Sitio web del INE: www.ine.es». Solo autoriza reutilizar lo que tiene al propio INE como fuente
  original, no las tablas de terceros que aloja (aviso legal del INE).
- **Resto de la AGE**: «Fuente: {organismo}» y la fecha de actualización del original.

## Licencias que no son «libre con cita»

Comprobadas con la API el 2026-10-01:

- **CNMC** (`cnmc-data`): CC BY-SA 4.0 en los 214 conjuntos. Lo que se derive se publica con la misma licencia.
- **GBIF** (`gbif-es`): 41.642.680 de las 95.845.920 ocurrencias de España son CC BY-NC 4.0. Para uso comercial, pedir
  `license=CC_BY_4_0&license=CC0_1_0` (54.203.240).
- **Junta de Andalucía** (`junta-andalucia-datos-abiertos`): de 832 conjuntos, 19 son `CC-BY-NC-4.0` y 18 son
  `Consultar-…`, que exigen preguntar a la consejería.

Recogidas en las fichas:

- **PEGV de la Generalitat Valenciana** (`ive-pegv-bancos-datos`): su aviso legal prohíbe comercializar el acceso.
- **Idescat** (`idescat-api`): prohíbe alterar datos, metadatos o enlaces y enmarcar sus páginas.
- **Aena** (`aesa-aviacion`) y **DGT** (`dgt-datex-trafico`): condiciones propias en su aviso legal.

## Datos personales

- Reutilizar datos personales se rige por el RGPD y la LOPDGDD (Ley 37/2007, art. 4.6). Quedan fuera de la
  reutilización si la ponderación de la Ley 19/2013 da prevalencia a la protección de datos, salvo que se anonimicen
  (art. 3.4). La licencia puede prohibir revertir la anonimización cruzando con otras fuentes (art. 8.f).
- **BDNS** (`bdns-api`, RD 130/2019, art. 7.7): la información con datos personales solo se reutiliza para controlar
  la actividad pública, con fines de archivo, de investigación o estadísticos, y anonimizada antes. Las personas
  físicas llegan con el DNI enmascarado (`***8959** NOMBRE`): en un producto, quitar el nombre o descartar esas filas.
- **Catastro** (`catastro-ovc`, TRLCI, art. 51 a 53): nombre, NIF y domicilio del titular, y el valor catastral, son
  datos protegidos. Solo acceden el titular, quien tenga su consentimiento por escrito, los supuestos tasados del
  art. 53 y las administraciones. Los servicios sin certificado ni Cl@ve no los dan.
- **BORME** (`borme-api-sumario`): administradores y apoderados son datos personales; las condiciones del BOE remiten al
  RGPD y a la LOPDGDD.
- **Deudores de la AEAT** (LGT, art. 95 bis): la lista deja de ser accesible a los tres meses y la norma obliga a
  impedir su indexación. No cachearla ni reindexarla.
- **Ayudas de la PAC** (`fega-beneficiarios-pac`, Reglamento (UE) 2021/2116, art. 98.4): no se publica el nombre de
  quien recibe 1.250 € o menos en el año.

## Datos que caducan: copia propia o se pierden

- **BDNS** (RD 130/2019, art. 7.8): las concesiones se retiran solas a los cuatro años naturales siguientes al de
  concesión, y las de personas físicas tras el año siguiente al de concesión. Comprobado el 2026-10-01:
  - `fechaDesde=01/01/2021&fechaHasta=31/12/2021` da `totalElements` 0 (2022 da 1.129.141);
  - el 10/10/2024 hay 0 concesiones con DNI enmascarado de 2.000, y el 10/10/2025, 1.388.
- **PAC**: cada publicación se consulta dos años desde la inicial (Reglamento (UE) 2021/2116, art. 98.4).
- **Deudores de la AEAT**: tres meses desde la publicación, que se hace en el primer semestre con fecha de referencia
  31 de diciembre.

Una copia propia de personas jurídicas no plantea problemas de datos personales. La de personas físicas sigue sujeta al
RGPD y, en la BDNS, a los fines del art. 7.7.
