# Sal Monet: el programa de ejemplo del manual, compilado y probado

El manual «Programación en Español Llano» (`documentación/instrucciones v2.pdf`, páginas 13 a 54) construye paso a paso el **Sal Monet**, una aplicación gráfica de menos de 300 líneas. Esta carpeta tiene la versión final armada a partir de esos fragmentos, ya corregida para que compile, y el resultado de probarla.

- `como pintar`: el código fuente (288 líneas). Se llama igual que en el manual, sin el acento. Está en ISO-8859-1 con finales de línea CRLF, como los demás fuentes; no cambiar la codificación ni agregarle extensión.
- `captura-inicio.png`: el programa recién iniciado (reducida a la mitad).
- `captura-error-red.png`: la parte inferior de la pantalla después de escribir una consulta y presionar ENTER.

## Cómo compilarlo

1. Crear un directorio nuevo, por ejemplo `C:\sal-monet`, y copiar adentro `(6) el seso` (renombrado a `el seso`, si se quiere) y `como pintar`. Solo esos dos archivos.
2. Abrir `como pintar` en SAL y elegir **Ejecutar** (menú **E**). El ejecutable queda en el mismo directorio con el nombre del directorio.

## Qué hace el programa (según el manual)

Se escribe el nombre de cualquier persona, lugar o cosa en el cuadro de texto y, con ENTER, el programa le pide una página de imágenes a un buscador (Bing en esta versión; ver «Actualización de 2026»), toma las direcciones, descarga cada imagen y la «pinta» al estilo de Monet sobre un fondo de tonos de gris. Con INICIO, FIN, RE PÁG y AV PÁG se recorren las pinturas. Hay botones **Imprimir** y **Abandonar**, y atajos CTRL-P y CTRL-Q.

## Cambios necesarios respecto al listado del manual

El listado del manual no compila tal cual: es una versión traducida y comentada. Estos son los cambios. Solo dos los exigió el compilador con un error (el color `gris clarísimo` y el encabezado de `hacer un botón`, ver más abajo); las erratas se corrigieron antes de compilar, revisando `el seso` y el contexto, así que no está demostrado que cada una fuera imprescindible:

| Manual | En `como pintar` | Motivo |
|---|---|---|
| `el color gris clarísimo` | `el color gris muy muy claro` | `gris clarísimo` no existe. `el seso` define `gris muy muy claro` (y `el color blanco`, que se usa tal cual). |
| `Para hacer que un botón tenga un punto y un nombre:` | `Para hacer un botón usando un punto y un nombre:` | El encabezado del manual no coincide con las llamadas (`Hacer el botón … usando el punto y …`). |
| `(reponer cursor)` | `(cursor)` | El despachador llama a `manejar un evento (cursor)`. |
| `el botón salir` | `el botón de abandonar` | Errata del manual. |
| `exit` mezclado en rutinas en español (rutinas de INICIO y FIN) | `salir` | Errata del manual; se unificó. |
| `la parte inferior de la pantalla` | `la inferior de la pantalla` | Coherencia con el resto del listado. |
| `… el anterior del trabajo actual es nulo, cloquear.` | se añadió `; salir` | El manual omite el `salir` en la rutina de RE PÁG. |
| `es nula` (en la rutina de AV PÁG) | `es nulo` | Concordancia con `el siguiente`. |
| `en la derecha el texto` | `en la derecha del texto` | Errata del manual. |

Se descartó un comentario del manual (`\ [saltar src=" ]`). Las demás líneas son las del manual.

## Qué se probó

Se compiló con `sal-1016.exe` bajo Wine (Linux, pantalla virtual), con una copia de `el seso`, en **tres intentos**. Los dos primeros fallaron con estos errores del compilador:

1. `No sé cómo 'Elegir [color] entre the color gris clarísimo and [color]'`: el manual escribe `gris clarísimo`, un color que no existe; el correcto es `gris muy muy claro`.
2. `No sé cómo 'Hacer [botón] from/given/with/using [punto] and [string]'`: el encabezado de `hacer un botón`.

El tercero compiló sin errores y generó el ejecutable. Se ejecutó y se comprobó:

| Prueba | Resultado |
|---|---|
| Arranque | Se pinta el fondo en tonos de gris. Abajo aparece `¡Hola, mundo!` en el centro, el cuadro de texto con `_` a la izquierda y los botones **Imprimir** y **Abandonar** a la derecha, como en el diseño del manual. |
| Escribir `sol` | Aparece `sol_` y desaparece el mensaje de estado. |
| RETROCESO y escribir `mar` | `so` + `mar` = `somar_`. |
| ENTER | Muestra `No pude conectarme a url 'http://images.google.com/images?q=somar'.` (prueba hecha con la versión original del manual, antes de la actualización) Se armó la consulta y se intentó leer la URL; falló porque la sesión no tiene acceso a internet. |
| ESC | Borra el texto; queda el `_`. |
| **Imprimir** sin trabajos | No muestra nada (el programa «cloquea», que no se ve). |
| **Abandonar** y CTRL-Q | El programa termina en ambos casos (se comprobó que no queda el proceso). |

## Prueba con imágenes locales (la parte de internet)

Como la sesión no tiene internet, se probó la búsqueda y la pintura con un **servidor local** que imita a Google. Todo está en `prueba-local/`:

- `web/index.html` y tres imágenes (`atardecer.jpg`, `arbol.jpg`, `montana.jpg`). Son dibujos sencillos que generé con ImageMagick, sin contenido de terceros. La página tiene tres `<img src="http://tlocal:8000/...">`.
- `programa/como pintar`: el mismo programa, con **una sola línea distinta**: la dirección pasa de `http://images.google.com/images?q=` a `http://tlocal:8000/?q=`.
- `captura-pintura.png` y `captura-paginas.png`: capturas.

Detalle importante: el programa solo toma las imágenes cuya dirección **empieza con `http://t`** (busca el texto `src="http://t`, como las miniaturas de Google de entonces). Por eso el servidor de prueba se llama `tlocal`, un nombre que hay que agregar al archivo `hosts` (`127.0.0.1 tlocal`).

Cómo repetirlo:

1. Agregar `127.0.0.1 tlocal` al archivo `hosts` (en Linux, `/etc/hosts`; en Windows, `C:\Windows\System32\drivers\etc\hosts`).
2. Servir la carpeta `web`: `python3 -m http.server 8000 --bind 127.0.0.1 --directory web`.
3. Compilar `programa/como pintar` junto con `el seso`, como arriba, y ejecutarlo. Escribir una palabra y presionar ENTER.

Resultados (compilado con `sal-1016.exe` y ejecutado bajo Wine). Una primera tanda se hizo con una versión que usaba nombres en inglés para los colores y el cursor, que resultaron innecesarios; después se repitió el caso principal (`sol` y ENTER) con la versión en español que está en esta carpeta, con el mismo resultado. Las teclas de página y la impresión se probaron solo con la versión anterior:

| Prueba | Resultado |
|---|---|
| Escribir `sol` y ENTER | El servidor recibió `GET /?q=sol`, luego la imagen del atardecer. El programa la «pintó» a pinceladas, encuadrada en un cuadrado de 125 mm, sobre el fondo gris. |
| AV PÁG | Muestra el segundo trabajo (el árbol), que se descarga y se pinta en ese momento (terminó dentro de los 45 s de espera; no se midió el tiempo exacto). |
| AV PÁG otra vez | Tercer trabajo (las montañas). |
| AV PÁG en el último | No cambia (el «cloqueo»). |
| RE PÁG | Vuelve al árbol, al instante y sin nueva descarga. |
| INICIO y FIN | Van al primero (atardecer) y al último (montañas). |
| Peticiones al servidor | Una sola por imagen: las pinturas terminadas no se vuelven a pedir. |
| **Imprimir** con un trabajo cargado, y CTRL-P | El estado muestra `Impreso` y el programa sigue funcionando. No se generó ningún archivo de impresión (la sesión no tiene impresora), así que solo se sabe que la rutina terminó sin error. |

## Actualización de 2026: Google Images ya no sirve

En marzo de 2026 Gerry Rzeppa avisó por correo a la lista de Plain English / Español / Portugués que el Cal Monet dejó de funcionar, porque Google Images ya no devuelve las imágenes como lo hacía desde hace 20 años. El arreglo propuesto son dos líneas, y están aplicadas en [`como pintar`](como%20pintar):

| Dónde | Antes | Ahora |
|---|---|---|
| Al manejar ENTER | `Poner "http://images.google.com/images?q=" en una URL.` | `Poner "https://bing.com/images/search?q=" en una URL.` |
| En las reglas de imagen del escáner | `... comienza con "src=""http://t", interrumpir.` | `... comienza con "src=""https://t", interrumpir.` |

Qué se verificó: el programa modificado **compila** con `sal-1016.exe` bajo Wine y produce el `.exe`. Qué no: no se probó contra Bing, porque no hay internet en esta sesión. Si Bing cambia su página, el filtro `src="https://t` puede dejar de coincidir. El texto de los comentarios dice todavía «reglas de imagen de Google».

La versión local de prueba (`prueba-local/programa/como pintar`) conserva `http://t` y `http://tlocal:8000/`, porque su servidor es `http`.

## Qué no se pudo probar

- **Bing o cualquier buscador real.** La sesión no tiene internet. El cambio a Bing (abajo) se compiló, pero no se probó contra el servicio real. Además, `programa/como pintar` quedó con la versión local (`http://t`), que no se modificó.
- **Una impresión real.** Ver la última fila de la tabla anterior.
- **El comportamiento en Windows.** Todo se probó bajo Wine.
