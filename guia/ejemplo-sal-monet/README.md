# Sal Monet: el programa de ejemplo del manual, compilado y probado

El manual «Programación en Español Llano» (`documentación/instrucciones v2.pdf`, páginas 13 a 54) construye paso a paso el **Sal Monet**, una aplicación gráfica de menos de 300 líneas. Esta carpeta tiene la versión final armada a partir de esos fragmentos, ya corregida para que compile, y el resultado de probarla.

- `como pintar`: el código fuente (288 líneas). Se llama igual que en el manual, sin el acento. Está en ISO-8859-1 con finales de línea CRLF, como los demás fuentes; no cambiar la codificación ni agregarle extensión.
- `captura-inicio.png`: el programa recién iniciado (reducida a la mitad).
- `captura-error-red.png`: la parte inferior de la pantalla después de escribir una consulta y presionar ENTER.

## Cómo compilarlo

1. Crear un directorio nuevo, por ejemplo `C:\sal-monet`, y copiar adentro `(6) el seso` (renombrado a `el seso`, si se quiere) y `como pintar`. Solo esos dos archivos.
2. Abrir `como pintar` en SAL y elegir **Ejecutar** (menú **E**). El ejecutable queda en el mismo directorio con el nombre del directorio.

## Qué hace el programa (según el manual)

Se escribe el nombre de cualquier persona, lugar o cosa en el cuadro de texto y, con ENTER, el programa le pide a Google una página de imágenes, toma las direcciones, descarga cada imagen y la «pinta» al estilo de Monet sobre un fondo de tonos de gris. Con INICIO, FIN, RE PÁG y AV PÁG se recorren las pinturas. Hay botones **Imprimir** y **Abandonar**, y atajos CTRL-P y CTRL-Q.

## Cambios necesarios respecto al listado del manual

El listado del manual no compila tal cual: es una versión traducida y comentada. Estos fueron los cambios, hechos de uno en uno según los errores del compilador y revisando `el seso`:

| Manual | En `como pintar` | Motivo |
|---|---|---|
| `el color blanco` | `the white color` | En `el seso`, los colores solo tienen nombre en inglés. |
| `el color gris clarísimo` | `the lightest gray color` | Ídem. |
| `el color gris muy muy claro` | `the lightest gray color` | Ese color no existe en `el seso`; se usó el mismo gris claro. |
| `Mostrar el cursor flecha.` | `Show the arrow cursor.` | El cursor flecha tiene nombre solo en inglés. |
| `Para hacer que un botón tenga un punto y un nombre:` | `Para hacer un botón usando un punto y un nombre:` | El encabezado del manual no coincide con las llamadas (`Hacer el botón … usando el punto y …`). |
| `(reponer cursor)` | `(cursor)` | El despachador llama a `manejar un evento (cursor)`. |
| `el botón salir` | `el botón de abandonar` | Errata del manual. |
| `exit` mezclado en rutinas en español | `salir` | Errata del manual; se unificó. |
| `la parte inferior de la pantalla` | `la inferior de la pantalla` | Coherencia con el resto del listado. |
| (varias frases) | se añadió `salir` donde el manual lo omitía | Errata del manual. |

Se descartó un comentario del manual (`\ [saltar src=" ]`). Las demás líneas son las del manual.

## Qué se probó

Se compiló con `sal-1016.exe` bajo Wine (Linux, pantalla virtual), con una copia de `el seso`, en **tres intentos**. Los dos primeros fallaron con estos errores del compilador:

1. `No sé cómo 'Elegir [color] entre the color gris clarísimo and [color]'`: faltaban los nombres de colores en inglés.
2. `No sé cómo 'Hacer [botón] from/given/with/using [punto] and [string]'`: el encabezado de `hacer un botón`.

El tercero compiló sin errores y generó el ejecutable. Se ejecutó y se comprobó:

| Prueba | Resultado |
|---|---|
| Arranque | Se pinta el fondo en tonos de gris. Abajo aparece `¡Hola, mundo!` en el centro, el cuadro de texto con `_` a la izquierda y los botones **Imprimir** y **Abandonar** a la derecha, como en el diseño del manual. |
| Escribir `sol` | Aparece `sol_` y desaparece el mensaje de estado. |
| RETROCESO y escribir `mar` | `so` + `mar` = `somar_`. |
| ENTER | Muestra `No pude conectarme a url 'http://images.google.com/images?q=somar'.` Se armó la consulta y se intentó leer la URL; falló porque la sesión no tiene acceso a internet. |
| ESC | Borra el texto; queda el `_`. |
| **Imprimir** sin trabajos | No muestra nada (el programa «cloquea», que no se ve). |
| **Abandonar** y CTRL-Q | El programa termina en ambos casos (se comprobó que no queda el proceso). |

## Qué no se pudo probar

- **La búsqueda de imágenes y la pintura de retratos.** Requieren internet. Además, la dirección que usa el manual (`http://images.google.com/images?q=`) es de 2018 y es probable que Google ya no devuelva páginas con el formato que el programa espera. No se verificó.
- **Las teclas INICIO, FIN, RE PÁG y AV PÁG**, que necesitan trabajos creados.
- **La impresión.**
- **El comportamiento en Windows.** Todo se probó bajo Wine.
