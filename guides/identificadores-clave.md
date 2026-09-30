# Identificadores clave para cruzar datos públicos españoles

Los datasets de la Administración no comparten nombres, comparten códigos. Estos son los que hay que conocer.

## Territorio

| clave | formato | quién la emite | dónde se usa | trampa |
|---|---|---|---|---|
| Código INE de municipio | 5 dígitos: provincia (2) + municipio (3). A veces con 6º dígito de control | INE (`ine-codigos-territoriales`) | INE, SEPE, AEMET, DGT, Hacienda local, movilidad MITMA, BDNS | Muchos ficheros lo guardan como entero y pierden el cero inicial (Álava 01). Comprobar si incluye dígito de control |
| Código INE de provincia | 2 dígitos (01 a 52) | INE | Casi todo | Ceuta 51 y Melilla 52 no son provincias en sentido estricto pero se codifican así |
| Código de CCAA | 2 dígitos (01 Andalucía ... 19 Melilla) | INE | Estadísticas | Orden distinto al alfabético y al de Eurostat (NUTS2 usa ES11, ES12...) |
| NUTS 1/2/3 | ES + 1 a 3 caracteres | Eurostat | Datos europeos, fondos UE | NUTS3 = provincia salvo islas y Ceuta/Melilla |
| Sección censal | 10 dígitos: municipio (5) + distrito (2) + sección (3) | INE | Censo, renta por sección (INE Atlas), SERPAVI, movilidad | Las secciones se redibujan cada año; usar la geometría del mismo año que el dato |
| Referencia catastral | 14 caracteres (parcela) o 20 (inmueble) | Catastro (`catastro-ovc`) | Catastro, notarías, registros, SIGPAC rústica | Los códigos de municipio del Catastro son propios, no INE |
| Referencia SIGPAC | provincia:municipio:agregado:zona:polígono:parcela:recinto | FEGA (`mapa-sigpac`) | PAC, agricultura | Comparte polígono y parcela con Catastro en rústica, no el resto |
| Código de estación AEMET (idema) | 4 o 5 caracteres alfanuméricos (3195 Madrid Retiro) | AEMET (`aemet-opendata`) | Climatología | Las predicciones no usan idema, usan código INE de municipio |

## Organizaciones y personas jurídicas

| clave | formato | quién la emite | dónde se usa | trampa |
|---|---|---|---|---|
| NIF | letra + 7 dígitos + control (personas jurídicas: A, B, G, Q, S, P...) | AEAT | Contratación, subvenciones, BORME, registros | La letra inicial indica el tipo de entidad: P ayuntamientos, Q organismos autónomos, S órganos de la AGE, G asociaciones |
| Código DIR3 | letra + 8 dígitos (E00003901) | SGAD (`dir3-directorio`) | FACe, PLACSP, BDNS, transparencia, datos.gob.es | Las unidades cambian con cada reestructuración ministerial; el código antiguo queda extinguido con sucesor |
| Código SIA | 6 o 7 dígitos | SGAD (`pag-administracion-gob-es`) | Sedes electrónicas, BDNS, notificaciones | Identifica el procedimiento, no el organismo |
| Número BDNS | 6 dígitos | IGAE (`bdns-api`) | Convocatorias de subvenciones, extractos en BOE | Es la clave estable de una convocatoria; el título varía |
| Expediente PLACSP | libre, lo asigna cada órgano | Órgano de contratación (`placsp-datos-abiertos`) | Licitaciones | No es único entre organismos; usar el id de la entrada ATOM |
| Código nacional (CN) de medicamento | 6 dígitos | AEMPS (`aemps-cima-api`) | Farmacia, prescripción | Identifica la presentación; el nregistro identifica el medicamento |
| CNAE 2009 | 4 dígitos (a veces letra de sección) | INE | Empresas, empleo, comercio exterior, inversión | CNAE 2025 en transición; las fuentes van cambiando |
| Identificador BOE | BOE-A-AAAA-NNNNN (disposición), BOE-B-... (anuncio), BORME-A-AAAA-NNN-PP | AEBOE (`boe-api-sumario`) | Legislación, anuncios, BORME | En BORME sección A el sufijo PP es el código de provincia |

## Normas para no pelearse con los ficheros

- Codificación: Latin-1 (ISO-8859-1 o 15) en INE antiguo, SEPE, BdE, AEMET; UTF-8 en APIs modernas. Detectar antes de leer.
- Decimales: coma en la mayoría de CSV y JSON administrativos (AEMET, carburantes, BdE). Convertir explícitamente.
- Separador CSV: punto y coma es lo habitual cuando el decimal es coma.
- Fechas: el formato administrativo es DD/MM/AAAA; las APIs modernas usan ISO 8601. AEMET exige el sufijo UTC literal.
- Coordenadas: ETRS89 es el sistema oficial (EPSG:4258 geográficas, 25829/25830/25831 UTM por huso, 32628 en Canarias). Catastro y SIGPAC sirven en UTM; APIs de consumo general en WGS84 (EPSG:4326), que a efectos prácticos coincide con ETRS89.
- Secreto estadístico: el INE marca celdas protegidas con un campo Secreto o con puntos; no interpretar como cero.
- Cero inicial: cualquier código territorial cargado como número pierde el cero de Álava, Albacete, Alicante, Almería, Ávila, Badajoz, Baleares y Barcelona. Cargar como texto siempre.
