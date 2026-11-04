# Análisis estático de `sal-1016.exe`

Análisis del ejecutable `sal-1016.exe` hecho sin ejecutarlo: cabeceras PE, imports, strings y desensamblado, cotejado con el código fuente (sobre todo `(6) el seso`).

- **SHA-256:** `6062457fe28683d994900459549e7b2c1ea98fc5618feef8e11dcdd64c575264`
- **Tamaño:** 847.872 bytes
- **Herramientas:** `objdump`, `strings`, `file` y dos scripts de Python (incluidos acá).

## Formato del ejecutable

- PE32 para Windows, x86 de 32 bits, subsistema GUI.
- Sin símbolos ni números de línea. Marca de tiempo de compilación en cero (1970).
- Tres secciones: `idata` (imports, `0x401000`), `data` (`0x402000`, ~120 KB) y `code` (`0x420000`, ~700 KB).
- Sin tabla de recursos, sin reubicaciones y sin firma digital. Es el formato mínimo que produce el propio compilador, no el de un linker comercial.
- Punto de entrada en `0x4CE1F4`: prólogo `push ebp / mov ebp,esp`, una llamada a una rutina de inicialización (`0x4B1E24`) y una serie de llamadas a `0xBD29C` que cargan tablas de datos.
- Dentro de `data` está embebida la fuente `osmosian` (ver sus strings de versión y copyright), que el programa carga desde memoria con `AddFontMemResourceEx`.

## Imports de Windows

Nueve DLL, 164 funciones (lista completa en `iat.txt`): `user32`, `kernel32`, `gdi32`, `gdiplus`, `ole32`, `ws2_32`, `winmm`, `shlwapi`, `comdlg32`.

Agrupadas por uso:

- **Interfaz:** ventanas, mensajes, cursores, teclado y ratón.
- **Dibujo y fuentes:** GDI y GDI+ (regiones, polígonos, imágenes).
- **Archivos:** crear, leer, escribir, copiar, mover, borrar, listar; consulta de unidades.
- **Portapapeles e impresión.**
- **Procesos e hilos:** `CreateProcessA`, `CreateThread`, `TerminateProcess`, `LoadLibraryA`, `GetProcAddress`.
- **Red:** solo `WSAStartup` y `WSACleanup` (ver más abajo).
- **Sonido:** `PlaySound`.

## Correspondencia con el código fuente

### Rutinas con ensamblador embebido

En `(6) el seso` hay 64 rutinas cuyo cuerpo son solo líneas `Intel $...` de al menos 8 bytes. **48 aparecen byte por byte en el ejecutable**, por ejemplo:

| Rutina de la fuente | Dirección en el `.exe` |
|---|---|
| `add a byte to a number` | `0x49362F` |
| `add a number to a byte` | `0x4936A7` |
| `add a number to another number` | `0x493723` |
| `bitwise and a byte with a number` | `0x495B6B` |
| `bump a rider` | `0x495BDB` |

Las otras 16 no se encontraron. Hipótesis (no verificada): el compilador no incluye las rutinas que nada usa.

### Llamadas a Windows

| Fuente (`el seso`) | En el `.exe` |
|---|---|
| línea 8138, `To initialize winsock` | `WSAStartup` en `0x4B4F69` |
| línea 5853 | `WSACleanup` en `0x4A98B3` |
| líneas 7635–7636 | `LoadLibraryA("kernel32.dll")` en `0x4B1E59` y `GetProcAddress("HeapSetInformation")` en `0x4B1EA2` |
| línea 13781, `To start a process` | `CreateProcessA` en `0x4C7429` y `CreateThread` en `0x4C7502` |
| línea 13901 | `TerminateProcess` en `0x4C760C` |
| líneas 10541–10557 | `PlaySound` en `0x4BBEE1` |

La rutina de arranque en `0x4B1E24` llama a `DisableProcessWindowsGhosting` y `GetProcessHeap`, y después carga `kernel32`, en el mismo orden que la fuente.

### Red

La fuente tiene una capa de red completa (`socket`, `connect`, `setsockopt`, `getaddrinfo`, `closesocket`). En el ejecutable **solo están `WSAStartup` y `WSACleanup`**. No se importan `socket`, `connect`, `send` ni `recv`, y la cadena `getaddrinfo` no aparece. Es decir, el código de red presente en este ejecutable no abre conexiones. Esto es coherente con que el compilador deje afuera lo que no se alcanza (hipótesis, no verificada).

## Qué se encontró y qué no

- No hay URLs, direcciones IP ni dominios incrustados en los strings. Tampoco claves de registro ni referencias a `cmd` o `powershell`.
- Lo que importa y lo que llama corresponde a lo que describe el manual (entorno gráfico, editor, archivos, impresión, portapapeles y compilador).

## Estructura del programa: arranque y final

El punto de entrada (`0x4CE1F4`) no es una rutina escrita a mano: la genera el compilador. En `(5) el compilador` (rutina `To add and compile the initialize before run and run and finalize after run routine`, línea 49) arma el cuerpo de esa rutina como la concatenación de:

1. `initialize before run.`
2. los inicializadores de los globales,
3. `ejecutar.`,
4. los finalizadores de los globales,
5. `finalize after run.`,
6. `call "kernel32.dll" "ExitProcess" with 0.`

El `.exe` tiene exactamente esa forma (el compilador compila esos tres cuerpos en `To compile the bodies of the routines`, línea 911):

| Paso | En el `.exe` |
|---|---|
| Prólogo | `push ebp / mov ebp,esp` en `0x4CE1F4` |
| `initialize before run` | `call 0x4B1E24`. Es la rutina de arranque vista antes: `DisableProcessWindowsGhosting`, `GetProcessHeap`, `LoadLibraryA("kernel32.dll")` y `GetProcAddress("HeapSetInformation")`. |
| Inicializadores de globales | 153 llamadas directas a rutinas de la biblioteca, sobre todo `0x4BD29C`, `0x4BE290` y `0x4BED04`. |
| `ejecutar` | `call 0x4326FC` (en `0x4CED57`). Es la rutina `Para Ejecutar:` de `(1) el escritorio` (línea 2036). Ver abajo. |
| Finalizadores de globales | 21 llamadas: 15 a `0x4CB714` y una a cada una de `0x4C88BC`, `0x4C8C54`, `0x4C8DD4`, `0x4C9AD4`, `0x4CAAB8` y `0x4CAF84`. |
| `finalize after run` | `call 0x4A9534` (en `0x4CEE58`). |
| `ExitProcess` | `0x4CEE65`, con el código de salida tomado de `0x41F8A8`. Ese dato vale 0. |

### `finalize after run`

La rutina `0x4A9534` llama a las API de cierre en este orden: `CoUninitialize`, `DestroyCursor` (tres veces), `RemoveFontMemResourceEx`, `GdiplusShutdown`, `SelectObject` y `DeleteObject` y `DeleteDC` (lienzo en memoria), `GlobalFree` (impresora), `DestroyWindow` con el bucle `GetMessageA`/`TranslateMessage`/`DispatchMessageA`, y por último `WSACleanup`.

Es el mismo orden en que están definidas las rutinas `To finalize ...` en `(6) el seso` (líneas 5800 a 5853): contexto, cursores, fuentes, GDI+, lienzo en memoria, lienzo de impresora, talker, ventana, winsock. Cada una del `.exe` se corresponde con una de la fuente, y las vacías de la fuente (`finalize the module`, `the mouse`, `the screen`, `the screen canvas`) no emiten llamadas a la API.

### La rutina `ejecutar`

Es `Para Ejecutar:` en `(1) el escritorio` (línea 2036), el programa principal:

```
Start up.
Initialize.
Handle events.
Finalize.
Shut down.
```

(La primera búsqueda no la encontró porque se escribió con mayúscula inicial.) En el `.exe`, la rutina `0x4326FC` llama exactamente a cinco rutinas en ese orden: `0x4C7560` (`Start up`), `0x431FA0` (`Initialize`), `0x42E67C` (`Handle events`), `0x423AE8` (`Finalize`) y `0x4C57D0` (`Shut down`).

- **`Start up`** (`To start up`, `(6) el seso`, línea 13841) inicializa en este orden: com, winsock, gdi+, talker, módulo, colores, pantalla, ventana, fuentes, cursores, ratón, lienzos, contexto y terminal. En el `.exe` las llamadas de `0x4C7560` se corresponden con ese orden. Tres quedaron verificadas por sus llamadas a la API: `CoInitializeEx` (`0x4B3CB7`) en la rutina `0x4B3CA4`, `WSAStartup` (`0x4B4F69`) en `0x4B4F40` y `GdiplusStartup` (`0x4B4374`) en `0x4B4318`.
- **`Shut down`** (`To shut down`, línea 13134) hace lo inverso. En el `.exe` termina llamando a `0x4A98B0`, que es `Finalize winsock` (`WSACleanup`, `0x4A98B3`).

## Fuente embebida y dibujo

### La fuente `osmosian`

- En `(6) el seso`, línea 9998, la fuente está escrita como una cadena hexadecimal (`The osmosian font source is a hex string equal to $00010000...`): 71.624 dígitos hexadecimales, es decir **35.812 bytes**.
- Esos 35.812 bytes aparecen **idénticos** en el `.exe`, en `0x403AD0` (sección `data`).
- Es una fuente TrueType (`sfnt` `0x00010000`) con 11 tablas (`OS/2`, `cmap`, `gasp`, `glyf`, `head`, `hhea`, `hmtx`, `loca`, `maxp`, `name`, `post`), 237 glifos y 2048 unidades por em.
- Su tabla `name` dice: «Osmosian Sloppy © 2005 Relational Systems Corporation 2005. All Rights Reserved.» (versión 1.00, 6 de noviembre de 2005) y, en otra entrada, «Osmosian © 2006 The Osmosian Order. All Rights Reserved.» (versión 3.00). El nombre de familia es `osmosian`.
- La rutina `To initialize the fonts` (línea 8039) la registra llamando a `AddFontMemResourceEx` con la dirección y el largo de esos bytes. En el `.exe` esa llamada está en `0x4B42AE`, y `RemoveFontMemResourceEx` (en `To finalize the fonts`, línea 5814) en `0x4A9683`. La fuente se carga desde memoria: no se instala en el sistema ni se escribe a disco. Quedará disponible para el proceso mientras dure.

Los créditos de esa fuente conviene tenerlos presentes si el repo se hace público: figura una atribución a Relational Systems Corporation en la entrada de 2005.

### Texto y dibujo (GDI)

| Función de Windows | Rutina en la fuente | En el `.exe` |
|---|---|---|
| `CreateFontA` | `convert a font to an hfont` (1362) | `0x4974FD` |
| `TextOutA` | `draw a string at a spot with a color and a font` (5080) | `0x4A5EA9` |
| `GetTextExtentPoint32A` | `get a width given a byte/string and a canvas` (6694, 6708) | `0x4AE201`, `0x4AE3A4` |
| `GetTextMetricsA`, `GetOutlineTextMetricsA` | `get an offset pair ...`, `get an outlinetextmetric given a font` (6464 a 6471) | `0x4ACD1F`, `0x4ACDF8`, `0x4ACE31` |
| `GetCharABCWidthsA` | `create some font widths ...`, `get an abca and an abcc ...` | `0x49B658`, `0x4AB443`, `0x4AB4E0`, `0x4AB5D0` |
| `GetFontData` | `put the actual data of a font into a buffer` (10695) | `0x4BC408`, `0x4BC469` |
| `SetPixelV` | `draw a line / polygon / spot with a color` (4727, 4869, 5016) | `0x4A41A4`, `0x4A4F9A`, `0x4A5C0E` |
| `BeginPaint` / `EndPaint` | `handle any wm-paint with a window` (6870) | `0x4AEFB1`, `0x4AEFD3` |
| `BitBlt` | `extract a picture given a box`, `refresh the screen given a box` | `0x4C08B3` |
| `CreateCompatibleDC` / `CreateCompatibleBitmap` | `initialize the memory canvas` (8053) | `0x4B4395`, `0x4B4405` |
| `GetDC` | `initialize the screen canvas` (8118) | `0x4B4CA7` |

### Una rutina de dibujo, línea por línea

`To draw a spot with a color` (`(6) el seso`, línea 5014) dice:

```
Convert the color to a colorref.
Call "gdi32.dll" "SetPixelV" with the current canvas and the spot's x-coord and the spot's y-coord and the colorref.
```

En el `.exe` es la rutina de `0x4A5BAC` a `0x4A5C17`, y se corresponde con la fuente paso a paso:

| Fuente | Código de máquina |
|---|---|
| (entrada, dos parámetros) | Prólogo `push ebp / mov ebp,esp`. Los parámetros están en `[ebp+8]` (el punto) y `[ebp+0xC]` (el color), y los dos se pasan **por referencia**. |
| `Convert the color to a colorref` | `call 0x496E88`, con el color y la dirección de una variable local (`-4(%ebp)`) para el resultado. |
| `the spot's x-coord` / `y-coord` | Se toma el puntero al punto (`[ebp+8]`): `x` es el campo en el desplazamiento 0 y `y`, en el 4 (`addl $0x4,-0xc(%ebp)`). |
| `Call ... "SetPixelV" with ...` | Se apilan, de derecha a izquierda, el `colorref`, la `y`, la `x` y el lienzo actual (la variable global en `0x40242C`), y se llama a `SetPixelV` en `0x4A5C0E`. |
| (salida) | `mov %ebp,%esp / pop %ebp / ret $8`: la rutina libera los 8 bytes de sus dos parámetros. |

Es una muestra de que el compilador traduce cada oración de la fuente de forma directa, sin optimizar: cada variable pasa por la pila y el orden de las instrucciones sigue el del texto. No se revisó el resto de las rutinas de dibujo con este nivel de detalle.

### Imágenes (GDI+)

- `GdiplusStartup` en `0x4B4374` (`initialize gdi+`, línea 8049) y `GdiplusShutdown` en `0x4A969B`.
- Cargar una imagen desde memoria: `CreateStreamOnHGlobal` (`0x49BB0B`) y `GdipCreateBitmapFromStream` (`0x49BB2D`), en `create a gpbitmap given a buffer` (línea 2019). Las imágenes se leen de un buffer, no de la red.
- Edición: `GdipCloneBitmapAreaI`, `GdipImageRotateFlip` (voltear, espejar y rotar), `GdipDrawImageRectRectI`, `GdipCreateBitmapFromScan0`, `GdipBitmapLockBits` y `GdipBitmapUnlockBits`, y `GdipSetImageAttributesColorMatrix` (escala de grises).

### El «talker»: síntesis de voz

`To initialize a talker` (`(6) el seso`, línea 8121) crea con `CoCreateInstance` el objeto `SpVoice` de la API de voz de Microsoft (SAPI): el identificador de clase `{96749377-3391-11D2-9EE3-00C04F797396}` y el de interfaz `{6C44DF74-72B9-4992-A1EC-EF996E0422D4}`. Las dos cadenas aparecen en el `.exe`. La rutina forma parte de `Start up`, así que el programa pide ese objeto al arrancar.

En la fuente hay rutinas para usarlo (`To speak a string`, `To speak a string and wait`, `To wait until speaking is done`), que respetan la bandera `silent flag`. La palabra `speak` no aparece en los otros cinco archivos, y dentro de `el seso` solo se la menciona en esas rutinas. No se verificó si el ejecutable llega a enlazarlas, ni se probó la voz. `To finalize a talker` libera el objeto (`Call the talker's vtable's release`).

### Impresión

`PrintDlgExA` (`0x4B49BB`, `initialize the printer canvas`), `StartDocA` (`0x494D40`), `StartPage` (`0x495358`), `ResetDCA` (`0x495156`), `EndPage` (`0x4A82C5`) y `EndDoc` (`0x4A6882`). Corresponden a `begin printing`, `begin a sheet`, `end a sheet` y `end printing`.

### Otros

`CoInitializeEx` (`0x4B3CB7`) y `CoCreateInstance` (`0x4B4D47`) están en `initialize com` y `initialize a talker`. `CLSIDFromString` (`0x499ACC`) está en `convert a string to a uuid`. Para qué sirve el «talker», ver la sección siguiente.

### Rutinas de `el seso` que no entran al ejecutable

Los 114 literales ausentes de `el seso` pertenecen a **50 rutinas** (ninguna está enlazada: si lo estuviera, su texto estaría en el `.exe`). Agrupadas por función:

| Grupo | Rutinas (línea en `el seso`) |
|---|---|
| **Sockets** (8) | `create a socket given a host string and a port number` (2199), `destroy a socket` (4262), `get an ip address given a host string` (6404), `get a sockaddr given a host string` (6600), `get some addrinfo routines` (6187), `receive a buffer from a socket` (11928), `send a buffer to a socket` (12901), `put the system's last winsock error into a number` (11475) |
| **HTTP con WinHTTP** (7) | `create the open handle` (2092), `create the connect handle` (1898), `create the request handle` (2175), `send a data string` (12913), `receive the response` (11943), `read a response string` (11850), `destroy a winhttp request` (4273) |
| **URL con WinInet** (2) | `convert a url to a url record` (1737), `read a url into a buffer` (11886) |
| **Correo** (1) | `send an email` (12926): arma un diálogo SMTP (`HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`) |
| **Cifrado** (4) | `create a crypt session with a passphrase string` (1930), `encrypt a buffer given a passphrase string` (5250), `decrypt a buffer given a passphrase string` (4146), `destroy a crypt session` (4181) |
| **CGI y consola** (4) | `initialize the cgi` (7644), `finalize the cgi` (5794), `find a value string given the environment variables and a name` (6035), `read stdin into a buffer` (11869) |
| **Archivos** (5) | `open a file given a path` (9969), `read a file into a buffer` (11780), `write a buffer to a file` (16134), `append a buffer to a file` (221), `read the bible` (11736, lee un archivo `bible.txt`) |
| **Depuración** (7) | `debug a box / a color / a font / a fraction / a line / a pair / a rgb` (2559 a 2647) |
| **Gráficos y texto** (6) | `convert a colorref to a color` (1319), `get a color given a spot` (6277), `extract a picture given a box` (5651), `unmask outside an hrgn` (15831), `get a column# given a row and a spot and a text` (6281), `get a start width and a substring ...` (6631) |
| **Sistema y sonido** (5) | `put the system's date/time into a date/time` (11460), `put the system's last error into a number` (11472), `beep` (380), `buzz` (774), `get a string from the stack` (6651) |
| **Geometría** (1) | `get a rise and a run given a heading` (6488) |

Esto confirma, con otra vía, lo ya visto: en el ejecutable no hay HTTP, sockets, correo ni cifrado. Los 7 literales sueltos de `(3) el editor` y `(5) el compilador` ya se explicaron antes (código comentado).

## Recompilación: el `.exe` se reproduce desde la fuente

Se compilaron los seis archivos fuente de `main` usando el propio `sal-1016.exe` y se comparó el resultado con el original.

- **Entorno:** Wine 9.0 sobre Linux, con una pantalla virtual (Xvfb) y un contenedor aislado en la nube. No se usó Windows.
- **Procedimiento:** los seis archivos, sin extensión y sin cambios, en un directorio llamado `sal-1016`. Se abrió `sal-1016.exe` (el original, desde un directorio aparte), se navegó hasta ese directorio, se seleccionaron los seis archivos, se abrieron con ENTER y se eligió **Ejecutar** en el menú **E**. Es el procedimiento del manual («Bebé SAL»).
- **Resultado:** apareció un `sal-1016.exe` de 847.872 bytes en el directorio, y el programa nuevo se lanzó.

| | SHA-256 |
|---|---|
| Original | `6062457fe28683d994900459549e7b2c1ea98fc5618feef8e11dcdd64c575264` |
| Recompilado | `6062457fe28683d994900459549e7b2c1ea98fc5618feef8e11dcdd64c575264` |

`cmp` no encontró ninguna diferencia entre los dos archivos.

**Repetirlo en Linux.** El procedimiento está automatizado en `recompilar-wine.sh` (en esta carpeta). Con Wine, Xvfb, xdotool e ImageMagick instalados:

```bash
bash analisis-exe/recompilar-wine.sh sal-1016.exe .
```

Maneja SAL con el ratón en una pantalla virtual, abre los seis archivos, elige **Ejecutar** y compara los hashes. En la prueba del 4 de noviembre de 2026 terminó con código 0 y «idénticos byte a byte». Es frágil: depende de las posiciones de pantalla. Para depurar, `KEEP=1` conserva el directorio de trabajo y las capturas.

**Qué demuestra.** Compilar estos seis archivos con SAL produce exactamente el ejecutable del repo. Por lo tanto el `.exe` corresponde a esta fuente, y no hay código en el ejecutable que la fuente no explique. Es la prueba que faltaba para lo que en las secciones anteriores quedaba como hipótesis (por ejemplo, que el compilador deja afuera las rutinas que nadie usa: el resultado reproducido es el mismo programa).

**Límites.**
- El compilador usado es el mismo `.exe` que se verifica. Si ese compilador hiciera algo extra al compilar, se reproduciría a sí mismo igual. Esta prueba confirma la coherencia entre fuente y ejecutable, no la ausencia de comportamiento malicioso. Para eso valen el análisis de imports, strings y rutinas de las secciones anteriores, que no encontraron nada de ese tipo en lo que se revisó.
- Se ejecutó bajo Wine y no en Windows. Que dé el mismo hash indica que el compilador es determinista en ambos casos, pero no se observó el comportamiento del programa en Windows.
- No se observó tráfico de red ni se probaron las demás funciones del programa.

## Red y procesos

### Red

- `WSAStartup` solo se llama desde `Initialize winsock`, que forma parte de `Start up`. `WSACleanup` solo se llama desde `Finalize winsock`, dentro de `Shut down`. Es decir, Winsock se abre al arrancar y se cierra al salir, y nada más lo usa.
- Las rutinas de la fuente que sí usan sockets (`socket`, `connect`, `setsockopt`, `closesocket`, `getaddrinfo`, `inet_ntoa`) no tienen llamada en el `.exe`: no se importan esas funciones y la cadena `getaddrinfo` no aparece. Tampoco hay HTTP ni cifrado (ver *Comparación de strings*).
- `start up the cgi` y `shut down the cgi` (que también inicializan winsock) no son alcanzables desde `Para Ejecutar`.
- `LoadLibraryA` y `GetProcAddress` solo se usan en el arranque, para obtener `HeapSetInformation` de `kernel32.dll`. La variante que carga `ws2_32.dll` para `getaddrinfo` (`To get some addrinfo routines`, línea 6188) no está en el `.exe`.

Conclusión: el código de red que contiene este ejecutable inicializa y cierra Winsock, y no abre conexiones. Está respaldado por imports, strings y el recorrido de llamadas. No se ejecutó el programa, así que no se observó su tráfico real.

### Procesos

El `.exe` crea procesos en un solo caso: ejecutar un programa.

1. **Ejecutar lo que se compiló** (`To handle run`, `(1) el escritorio`, línea 1862): guarda todo, compila el directorio y llama a `Start the current process given the compiler's exe path`.
2. **Ejecutar un `.exe` elegido en el administrador de archivos** (`To handle run given a node`, `(2)`, línea 706): solo si el archivo seleccionado tiene extensión `.exe`; si no, muestra «No sé cómo ejecutar ese tipo de archivo desde aquí.».

Ambos usan `To start a process given a path` (`(6) el seso`, línea 13775), cuya llamada `CreateProcessA` está en `0x4C7429`:

- Falla con un mensaje si ya hay un proceso en ejecución («el proceso ya se está ejecutando»).
- Pasa como directorio de trabajo el directorio del ejecutable.
- Usa los indicadores `67108904`, que en el `.exe` es el dato `0x04000028` (`CREATE_DEFAULT_ERROR_MODE` + `NORMAL_PRIORITY_CLASS` + `DETACHED_PROCESS`, lo mismo que dice el comentario de la fuente). No pasa argumentos de línea de comandos.
- Crea un hilo (`CreateThread`, `0x4C7502`) que espera al proceso con `WaitForSingleObject` y tiempo infinito (`0x496A32`, rutina `To compatibly wait for a process pointer`, línea 1215).
- `TerminateProcess` (`0x4C760C`) está en `To stop a process` (línea 13899). Solo la invoca `Stop the current process` desde `(1) el escritorio` (línea 1931) y siempre sobre el proceso que SAL mismo lanzó.

No hay otras llamadas a `CreateProcessA`, no se arma ninguna línea de comandos y no se invoca `cmd` ni `powershell`.

## Rutinas de archivos

Se cruzaron las llamadas a la API de archivos del `.exe` con las rutinas de `(6) el seso`. El emparejamiento usa dos pistas: el compilador emite las rutinas en el orden de la fuente, y cada grupo de llamadas vecinas (por ejemplo `CreateFileA`, `GetFileSize`, `ReadFile` y `CloseHandle`) coincide con el cuerpo de una sola rutina. Es una correspondencia por orden y vecindad, no una prueba rutina por rutina.

| Operación | Rutina en `(6) el seso` | Llamada en el `.exe` |
|---|---|---|
| Crear directorio | `create a path in the file system (directory)` (2110) | `CreateDirectoryA` `0x49C448` |
| Crear archivo | `create a path in the file system (file)` (2120) | `CreateFileA` `0x49C580` |
| Leer archivo completo | `read a path into a buffer` (11803) | `CreateFileA` `0x4C0264`, `GetFileSize` `0x4C0302`, `ReadFile` `0x4C03F0` |
| Escribir archivo | `write a buffer to a path` (16143) | `CreateFileA` `0x4C84AB`, `WriteFile` `0x4C858C` |
| Duplicar archivo | `duplicate a path to another path in the file system (file)` (5215) | `CopyFileA` `0x4A6757` |
| Renombrar o mover | `rename a path to another path in the file system` (12207) | `MoveFileA` `0x4C221B` |
| Borrar archivo | `destroy a path in the file system (file)` (4248) | `DeleteFileA` `0x4A2AB0` |
| Borrar directorio | `destroy a path in the file system (directory)` (4231) | `RemoveDirectoryA` `0x4A298E` |
| Listar | `get an item from a path (first time)` y `(not first time)` (6426, 6412) | `FindFirstFileA` `0x4ACB27`, `FindNextFileA` `0x4AC94D`, `FindClose` `0x4AC9C1` |
| Atributos | `decide if a path is in the file system`, `... is read-only`, `set a path to read-write mode` | `GetFileAttributesA` `0x49F674`, `0x49F704`, `0x4C55DC`; `SetFileAttributesA` `0x4C5619` |
| Tamaño | `get a size given a path in the file system (file)` (6594) | `GetFileAttributesExA` `0x4AD944` |
| Unidades | `get a drive kind for a path`, `get a drive name for a path` | `GetDriveTypeA` `0x4AC520`, `GetVolumeInformationA` `0x4AC70E` |
| Directorio temporal y ruta del programa | `initialize the module` (8061) | `GetTempPathA` `0x4B4497`, `GetModuleFileNameA` `0x4B45CA` |

Rutinas de la fuente que **no** tienen llamada en el `.exe` (no se incluyen): `open a file given a path`, `read a file into a buffer`, `read stdin into a buffer`, `append a buffer to a file`, `write a buffer to a file`, `write a byte to stdout` y `write a string to stdout`.

### Borrado

- **Archivo:** `DeleteFileA` sobre la ruta.
- **Directorio:** primero borra de forma recursiva cada elemento del directorio (`Loop. Get an item from the path. ... Destroy the other path`) y al final llama a `RemoveDirectoryA`. Es decir, borrar un directorio elimina todo su contenido.
- **Quién lo invoca:** en `(2) el administrador de archivos`, el manejador de la tecla Suprimir (`handle ... (key down - delete key)`, línea 452) elimina los elementos seleccionados en el sistema de archivos. Antes de borrar comprueba que el directorio no sea de solo lectura, que haya algo seleccionado y que el usuario esté seguro (`If the user is not sure, exit.`). No se revisó cómo se implementa esa confirmación.
- **Errores:** si falla una operación, se guarda un mensaje en `el error de e/s` (por ejemplo `Error eliminando archivo '...'`) y el borrado se detiene.

### Pendiente

No se leyeron las rutinas de duplicar, renombrar, copiar y pegar fuera de los puntos citados, ni el código de máquina de cada rutina de archivos más allá de la comprobación de las llamadas a la API.

## Comparación de strings (fuente contra `.exe`)

Se extrajeron los literales de texto de los seis archivos fuente (sin los comentarios) y se buscaron dentro del `.exe`.

- **1.506** literales distintos de 4 o más caracteres.
- **1.385 (92 %)** aparecen en el ejecutable.
- **121** no aparecen: 114 en `(6) el seso`, 6 en `(3) el editor` y 1 en `(5) el compilador`. Ninguno en `(1)`, `(2)` ni `(4)`. La lista completa está en `ausentes.txt`.
- En sentido inverso: de **458** cadenas de texto legible de la sección de datos del `.exe` (8 o más caracteres y 3 o más palabras), **0** carecen de coincidencia en la fuente. Es decir, ese texto está explicado por el código fuente. Quedan fuera del cotejo la fuente `osmosian` embebida y las tablas binarias.

### Qué hay en la fuente y no llegó al ejecutable

Los literales ausentes agrupan funciones que existen en la fuente pero que este ejecutable no incluye:

- **HTTP:** WinHTTP (`WinHttpOpen`, `WinHttpConnect`, `WinHttpSendRequest`, `WinHttpReadData`) y WinInet (`InternetOpenA`, `InternetOpenUrlA`, `InternetReadFile`), con sus mensajes de error.
- **Sockets:** `socket`, `connect`, `setsockopt`, `recv`, `closesocket`, `getaddrinfo`, `inet_ntoa`.
- **Correo:** líneas de protocolo SMTP (`HELO`, `MAIL FROM:`, `RCPT TO:`, `DATA`, `Subject:`, `QUIT`).
- **Cifrado:** `CryptAcquireContextA`, `CryptEncrypt`, `CryptDecrypt` y compañía, más los textos `Passphrase?`, `Encriptando...` y `Desencriptando...`.
- **Consola y entorno CGI:** `AllocConsole`, `GetStdHandle`, `GetEnvironmentVariableA` y `CONTENT_LENGTH`.
- **Otros:** `GetPixel`, `GetLocalTime`, `GetLastError`, `SetFilePointer`, `MessageBeep`.

Esto coincide con el análisis de imports: en el `.exe` solo están `WSAStartup` y `WSACleanup` de la red, y no hay ninguna función de HTTP ni de `advapi32` (cifrado). La explicación más probable es que `el seso` funciona como biblioteca general y el compilador deja afuera el código que ningún programa alcanza. Es una hipótesis: no se verificó recompilando.

### Los 7 literales ausentes fuera de `el seso`

Se revisaron uno por uno y todos corresponden a código comentado o sin llamadores en la fuente:

| Literal ausente | Dónde está | Por qué no llega al `.exe` |
|---|---|---|
| `Passphrase?`, `Passphrase cannot be blank.`, `Desencriptando...` | `(3) el editor`, rutina `To handle decrypt` (línea 262) | En `(1) el escritorio` la línea que despacha ese comando (692) está comentada y marcada `obsolete`, igual que las entradas de menú (864, 870). |
| `Passphrase?`, `Passphrase cannot be blank.`, `Encriptando...` | `(3) el editor`, rutina `To handle encrypt` (línea 273) | Igual: despacho comentado en la línea 695 y entradas de menú comentadas (883, 884), marcadas `obsolete`. |
| `Extrayendo...` | `(3) el editor`, rutinas `handle extract globals` (440), `handle extract routine headers` (458) y `handle extract types` (475) | Sus tres líneas de despacho en `(1) el escritorio` (696 a 698) están comentadas. |
| `En el portapapeles` | `(3) el editor`, usado solo por las rutinas de arriba | Su único uso está en rutinas que no se incluyen. |
| `flag` | `(5) el compilador`, línea 1316, rutina `To compile a literal given a rider (flag)` | Su único llamador (línea 1304) está comentado. |

Como contraste, `handle extract nibble literal`, cuya línea de despacho (699) **no** está comentada, sí aparece en el `.exe` (dos veces). Esto respalda la hipótesis de que el compilador incluye solo las rutinas alcanzables desde el punto de entrada. Sigue siendo una hipótesis: no se verificó recompilando.

## Límites

- **No prueba** que el `.exe` sea el resultado exacto de compilar estos seis archivos. Se cotejó una muestra de rutinas, no todo el ejecutable. Para saberlo habría que recompilar con SAL en Windows y comparar.
- **No es una auditoría completa.** Se leyeron las rutinas de arranque y las llamadas a red, procesos e hilos. Las decenas de miles de líneas restantes de código de máquina no se revisaron.
- El ejecutable no se corrió en ningún momento.

## Archivos de esta carpeta

| Archivo | Contenido |
|---|---|
| `iat.txt` | Dirección de cada import en la tabla de importación y nombre de la función. |
| `sal_annot.asm.gz` | Desensamblado de la sección de código (176.339 líneas), comprimido, con cada llamada a Windows rotulada. |
| `imports.py` | Genera `iat.txt` a partir del `.exe`. |
| `match.py` | Busca las rutinas solo-`Intel` de la fuente dentro del `.exe`. |
| `strcmp.py` | Compara los literales de texto de la fuente con los strings del `.exe`. |
| `ausentes.txt` | Los 121 literales de la fuente que no están en el `.exe`. |
| `recompilar-wine.sh` | Recompila los fuentes con `sal-1016.exe` bajo Wine y compara el resultado. |

## Cómo reproducirlo

Desde la raíz del repo (los scripts reciben las rutas por argumento):

```bash
python3 -I analisis-exe/imports.py sal-1016.exe > iat.txt
```

```bash
python3 -I analisis-exe/match.py sal-1016.exe "(6) el seso"
```

```bash
objdump -D -b binary -mi386 --adjust-vma=0x400000 --start-address=0x420000 --stop-address=0x4CEE74 sal-1016.exe > sal.asm
```

Los desplazamientos de archivo coinciden con las direcciones relativas porque la alineación de sección y de archivo es la misma (`0x1000`).

Para la comparación de strings (regenera `ausentes.txt`):

```bash
python3 -I analisis-exe/strcmp.py sal-1016.exe "(1) el escritorio" "(2) el administrador de archivos" "(3) el editor" "(4) el escriba" "(5) el compilador" "(6) el seso"
```

Para leer el desensamblado comprimido:

```bash
zcat analisis-exe/sal_annot.asm.gz | less
```
