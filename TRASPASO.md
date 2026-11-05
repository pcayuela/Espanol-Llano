# Traspaso: todo lo hecho en la sesión en la nube

Documento para retomar el trabajo en una sesión local (la PC de Pablo) sin depender de la conversación original. Contiene el estado del repositorio, lo decidido, lo aprendido y lo que quedó pendiente. Está escrito para que se lo pueda pegar o pedir que lo lea una sesión nueva de Claude.

## 1. Qué es el proyecto

`pcayuela/Espanol-Llano`: el compilador **SAL-1016** (Español Llano, variante en español de Plain English de la Orden Osmosian), adaptado por Pablo Cayuela. Es un compilador y entorno autocontenido: `sal-1016.exe` más seis fuentes (`(1) el escritorio` … `(6) el seso`). Los fuentes están en ISO-8859-1 con CRLF y **sin extensión**; no se debe renombrarlos ni convertirlos.

## 2. Ramas (todo en GitHub; `main` quedó intacto en `1939bde`)

| Rama | Contenido | Commit |
|---|---|---|
| `claude/readme` | README del proyecto (uso, «Bebé SAL»). | `bed6017` |
| `claude/gitattributes` | `.gitattributes` para preservar los bytes de los fuentes. | `a9b3ad9` |
| `claude/analisis-exe` | Análisis estático del `.exe` (formato PE, imports, mapeo contra los fuentes, rutinas ausentes, scripts, `recompilar-wine.sh`). | `cd7b13e` |
| `claude/guia-lenguaje` | Guía del lenguaje, el Sal Monet del manual compilado y probado, y cuatro ejemplos desde cero (`rueda`, `piano`, `graficador`, `cuestionario`); el cambio de Monet a Bing. | `de56951` |
| `claude/ejemplos-bing` | Lo anterior más la nota del intento fallido de probar Bing con un servidor HTTPS local en Wine. | `ac96330` |
| `claude/ejemplos-zips` | `guia/ejemplos-2/`: 9 ejemplos que andan (de Pablo/Elender y de Gerry Rzeppa) y los parches de `el seso`. | `2290bb1` |
| `claude/ejemplos-alumnos` | `guia/ejemplos-alumnos/`: 31 programas de alumnos anonimizados. | `3bb1c51` |
| `claude/traspaso` | Esta rama: contiene todo lo anterior de la línea `guia-lenguaje`→`ejemplos-alumnos`, más este documento y `herramientas-wine/`. | (ver `git log`) |

Los PR que se abrieron al principio se cerraron sin fusionar. **No se fusionó nada en `main`** (decisión de Pablo: «la rama original debe quedar así»). `claude/readme`, `claude/gitattributes` y `claude/analisis-exe` son ramas aparte.

## 3. Decisiones vigentes de Pablo

- `main` no se toca. El repositorio queda público (no privado). «Salnet» no se continúa.
- Nombres en GitHub sin acentos (por eso `herramientas-wine`, `ejemplos-alumnos`).
- No usar la palabra «vive/viven» ni su equivalente en inglés en ningún sentido.
- No desactivar Smart App Control de Windows (si hay que reinstalar, se reinstala).
- Los trabajos de alumnos solo se publican anonimizados y con numeración al azar; el archivo de correspondencia no se guarda en el repositorio.

## 4. Lo comprobado y lo que no

**Comprobado (bajo Wine 9, no en Windows):**
- `sal-1016.exe` se reconstruye desde los fuentes y el `.exe` resultante es idéntico byte a byte (`recompilar-wine.sh`, rama `claude/analisis-exe`). Es el mismo compilador reconstruyéndose a sí mismo; no es una auditoría completa del código de máquina.
- El Sal Monet del manual (288 líneas) compila y pinta con imágenes servidas por un servidor local (`http`).
- Los 4 ejemplos de `guia/ejemplos/`, los 9 de `guia/ejemplos-2/` y los 31 de `guia/ejemplos-alumnos/` compilan y corren.

**No comprobado:**
- Que el Sal Monet con Bing (`https://bing.com/images/search?q=`) funcione: Wine 9 rechaza el certificado de un servidor local (12057 por revocación con una autoridad propia; 12045 con un certificado autofirmado). Hace falta Windows con internet.
- Audio de `piano` (Wine con pantalla virtual no tiene sonido), impresión real, y cualquier prueba en Windows.
- Los `.exe` que venían dentro de los zip del usuario **no se ejecutaron**.

## 5. Hallazgos técnicos útiles

- **Lección de nombres:** un `un/una/el/la` dentro del nombre de una rutina crea un parámetro de ese tipo (`sonar una nota` pide el tipo `nota`). Un nombre como `a` falla (es artículo). Un tipo con el mismo nombre que uno de `el seso` (`contador`, `top`) da «debe estar duplicado».
- **Rutina de entrada:** SAL exige `Para ejecutar:`; con `To run:` dice «Necesito una rutina para 'ejecutar'».
- **Colores y pinceles:** los colores tienen nombre en español (`el color celeste muy muy claro`); los bolígrafos, solo en inglés.
- **Parche `coord`** (`guia/ejemplos-2/parches/aplicar-parches.py`): `spot` se define con `x-coord`/`y-coord` pero muchas rutinas de `el seso` siguen diciendo `spot's x` / `spot's y`; sin el parche, cualquier programa con líneas o puntos da «No hay 'y' dentro del 'spot'».
- **Parche `elegir`:** `Elegir un número entre 1 y 9` falla porque los literales son del tipo inglés `number`; Gerry propuso en 2020 el encabezado mixto `Para elegir un número entre otro number y un tercer number;`.
- Los programas escritos para la CAL en inglés fallan en SAL cuando usan la consola de la CAL (`Write … on the default console`) o definen tipos ya existentes.
- `el seso` de `pinta.zip` (alumnos) es idéntico al del repositorio (`3622dd2d…`); había un dato mío errado de 679.207 bytes, corregido.
- El `.exe` está bloqueado por Smart App Control en la PC de Pablo («reputación binaria malintencionada»); los antivirus no sirven para excluirlo.

## 6. Búsqueda de material en los Drive

- Cuenta UCC (`1022283@ucc.edu.ar`, carpeta Classroom) y Gmail: se revisaron los archivos sin extensión, los comprimidos y las subcarpetas de 2019. Salvo la copia de SAL y los 18 comprimidos con programas de SAL ya usados, todo lo demás es PSeInt/C++.
- Gerry Rzeppa avisó en marzo de 2026 que el Cal Monet con Google Images dejó de funcionar; el arreglo (Bing) está aplicado en `guia/ejemplo-sal-monet/como pintar`.
- Los archivos descargados de alumnos (`ucc/…`, `zz/…`) **quedaron solo en el contenedor de la sesión y se perderán**. No están en GitHub, a propósito.

## 7. Pendiente / decisiones abiertas

1. **Licencia de los ejemplos de Gerry** incluidos en `guia/ejemplos-2/` (`euler`, `arreglo`, `fibonacci`, `triangle`, `horizon`, `fireworks`): no se confirmó. Si hay dudas, retirarlos.
2. **`HAL`, `HAL2`, `HAL3`** (compiladores híbridos de Pablo, en `examples.zip`): no se agregaron; requieren una decisión.
3. **Probar el Monet con Bing en Windows** y, si funciona, agregar la captura.
4. **Rehacer en español** (con código propio) el ejemplo de suma de filas 5×4 de Gerry y/o el arreglo con punteros.
5. 21 programas de los zip y 10 de alumnos no compilan con `el seso` original; si se quiere, se pueden adaptar uno por uno.
6. Decidir si se fusionan las ramas en `main` (hoy no).

## 8. Cómo retomarlo en la PC

```bash
git clone https://github.com/pcayuela/Espanol-Llano.git
cd Espanol-Llano
git checkout claude/traspaso   # trae todo menos analisis-exe, readme y gitattributes
```

- Para compilar en Windows: crear una carpeta nueva (su nombre será el del `.exe`), copiar `(6) el seso` y el fuente, abrir el fuente en SAL y elegir **Ejecutar** (menú **E**).
- Para los programas que lo necesitan, generar la copia parcheada: `python3 guia/ejemplos-2/parches/aplicar-parches.py "(6) el seso" "el seso parcheado"`.
- Para una sesión local de Claude, abrir la carpeta del repositorio y pedirle que lea este archivo.

## 9. Qué se pierde y qué no

- **No se pierde** nada de lo que está en GitHub (las ramas de la tabla de arriba).
- **Se pierde** lo que solo estaba en el contenedor: los archivos de trabajo (descargas de alumnos, el prefijo de Wine, capturas intermedias) y la conversación completa como archivo. Lo útil de eso está resumido aquí; los scripts están en `herramientas-wine/`.
