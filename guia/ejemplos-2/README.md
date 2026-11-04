# Ejemplos 2: material de los cuatro archivos `.zip`

Se revisó lo que llegó en `ejemplos.zip`, `examples.zip`, `sample.zip` y `the_golden_key.zip`, más el programa suelto `desierto.txt`. Aquí quedan los programas que **compilaron y corrieron** con `sal-1016.exe` bajo Wine, y los parches mínimos de `el seso` que hicieron falta. Todo se probó bajo Wine, no en Windows.

## Qué hay aquí

| Carpeta | Qué es | Estado |
|---|---|---|
| [`sorteo/`](sorteo/) | Sorteo de lotería de 5 dígitos en la consola. Es el fuente de Pablo (traducción de un ejemplo en inglés de la Orden Osmosian). | Compila y corre con el parche `elegir`. Muestra `Generador de números de lotería`, cinco dígitos (por ejemplo `54384`) y `Presione la tecla Escape para salir`. |
| [`desierto/`](desierto/) | Paisaje del desierto: cielo con degradé, sol, pájaros y arena con degradé. Reescrito a partir de `desierto.txt`. | Compila y corre con el parche `coord`. Captura en la carpeta. |
| [`parches/`](parches/) | `aplicar-parches.py`: genera una copia parcheada de `(6) el seso` sin tocar el original. | Reproduce byte a byte la copia que se usó en las pruebas. |

Cómo usarlo: `python3 parches/aplicar-parches.py "(6) el seso" "el seso parcheado" coord` (o `elegir`, o ninguna opción para los dos parches), y compilar con esa copia en lugar de la original. El `(6) el seso` del repositorio no se modificó.

## Los dos parches

**`coord`.** El registro `spot` se define con `x-coord` e `y-coord` (línea 13450 de `(6) el seso`), pero 209 lugares del archivo (148 líneas) siguen escribiendo `'s x` y `'s y`. En español `y` es «and», y de todos modos el campo ya no se llama así. Cualquier programa que mueva líneas o puntos falla con `No hay 'x' dentro del 'spot'` o `No hay 'y' dentro del 'spot'`. Varias entregas del curso (2021) traen copias de `el seso` retocadas a mano para esquivar esto, cada una arreglando solo algunas líneas. El parche las cambia todas de una vez (las líneas comentadas con `\` no se tocan).

**`elegir`.** Con el `el seso` original, `Elegir un número entre 1 y 9.` falla con `No sé cómo 'Elegir [número] entre [number] and [number]'`: el compilador trata los literales como del tipo inglés `number`, y `número` no se convierte en `number`. Gerry Rzeppa lo explicó por correo en noviembre de 2020 y propuso un encabezado mixto, que es lo que agrega este parche: `Para elegir un número entre otro number y un tercer number;`.

## Qué cambió en `desierto`

El `desierto.txt` original no compilaba. Primer error: `No sé cómo 'Elegir [punto] in/into/to the mitad superior de [ratio] from/given/with/using [caja]'`. Es el sol, y venía de un `el seso` con encabezados mixtos agregados a mano. Para que compile con el `el seso` del repositorio más el parche `coord`:

| Antes | Ahora | Motivo |
|---|---|---|
| `Usar el bolígrafo azul cielo claro.` | `Usar el color celeste muy muy claro.` | Los bolígrafos tienen nombre en inglés; los colores sí tienen nombre en español (`celeste`, `amarillo`, `naranja`, con `muy muy claro`). |
| `Imaginar una línea en medio de una caja de la pantalla.` | `Imagine a line across the middle of the screen's box.` | El encabezado en español solo existe en una copia retocada de `el seso`. |
| `Dibujar la línea`, `Mover la línea hacia arriba 1 píxel`, `Si la línea está arriba de …` | versión en inglés (`Draw the line`, `Move the line up 1 pixel`, `If the line is above …`) | La línea imaginada se llama `line`, no `línea`. |
| `Oscurecer el color actual en 3 porcentaje` | `… sobre 3 porcentaje` | El encabezado original dice `sobre`. |
| `1/4 de pulgada`, `1 pulgada` | `6 mm`, `25 mm` | `pulgada` no es una unidad. |
| `Hacer un punto … de ancho`, `Centrar el punto en el lugar`, `Dibujar el punto con …` | `Make a dot … wide`, `Center the dot on the spot`, `Draw the dot with …` | Esos encabezados solo existen en inglés. |
| `Elegir un lugar …`, `Mover al lugar` | `Pick a spot …`, `Move to the spot` | El punto elegido se llama `spot`. |
| `Dibujar un cuarto de círculo …`, `Dar la vuelta`, `Mover … en cualquier dirección` | `Draw a quarter circle …`, `Turn around`, `Move the spot about … in any direction` | Solo en inglés, o con otra preposición. |

El resultado es un programa mezclado, no totalmente en español: `el seso` no tiene todavía encabezados en español para todo lo gráfico.

## Qué había en los zip y qué no se agregó

- **`ejemplos.zip`** (unos 160 fuentes de texto): programas de Pablo (`sorteo`, `simulator`, pruebas de `Hola Mundo`, la carpeta `Lizbeth`) y la carpeta `ucc2021`, con entregas de alumnos de dos cátedras. **No se publican las entregas de alumnos ni sus nombres.** Las que se miraron son mayormente traducciones de los ejemplos del manual (Sal Monet, el desierto, `pollock`, las cajas rellenas, el reloj, la ilusión óptica), no ideas nuevas. Hay también un `.csv` de una encuesta, que no se abrió ni se publica. Unas 90 copias de `el seso`: 68 son idénticas a la del repositorio y el resto son variantes retocadas a mano (por ejemplo con `x-coord`, o con encabezados mixtos, o una versión más antigua, SAL-1003).
- **`examples.zip`**: casi todo es Plain English en inglés (Project Euler, primos, fuegos artificiales, `pollock`, un arreglo con punteros), además de los experimentos de Pablo con compiladores híbridos (`HAL`, `HAL2`, `HAL3`) y varios `.exe`. `nuevo euler` (una mezcla de español e inglés, código de Gerry) compiló con el `el seso` original y mostró `The answer is: 233168`, que es la respuesta correcta; no se agregó porque el código es de Gerry. Los `HAL` no se agregaron: son compiladores completos y requieren una decisión aparte.
- **`sample.zip`**: es el Cal Monet en inglés (el original del que sale `guia/ejemplo-sal-monet/`), con su `.exe`. No se agregó. Usa Google Images, que ya no funciona (ver el README de ese ejemplo).
- **`the_golden_key.zip`**: el `cal-4400` (compilador en inglés de la Orden Osmosian), un libro en PDF y un `bible.txt`. No es Español Llano y es material de terceros: no se agregó.
- **Los `.exe` que venían en los zip no se ejecutaron.** Todo lo que se probó se compiló desde su fuente.
