# Ejemplos 2: material de los cuatro archivos `.zip`

Se revisó lo que llegó en `ejemplos.zip`, `examples.zip`, `sample.zip` y `the_golden_key.zip`, más el programa suelto `desierto.txt`. Aquí quedan los programas que **compilaron y corrieron** con `sal-1016.exe` bajo Wine, y los parches mínimos de `el seso` que hicieron falta. Todo se probó bajo Wine, no en Windows.

## Qué hay aquí

Todos compilan con `sal-1016.exe` y corren (bajo Wine). «Parche» indica qué copia de `el seso` hace falta (ver más abajo); «original» es el `(6) el seso` del repositorio sin tocar.

| Carpeta | Qué es | `el seso` | Captura |
|---|---|---|---|
| [`sorteo/`](sorteo/) | Sorteo de lotería de 5 dígitos en la consola (fuente de Pablo, traducción de un ejemplo en inglés de la Orden Osmosian). | parche `elegir` | `sorteo/captura.png` |
| [`desierto/`](desierto/) | Paisaje del desierto: cielo y arena con degradé, sol y pájaros. Reescrito a partir de `desierto.txt`. | parche `coord` | `desierto/captura.png` |
| [`holamundo-espiral/`](holamundo-espiral/) | Tres variantes de la espiral de «Hola Mundo» (`testing_1`, `prueba_elender`, `prueba_elender2`; la última dice «¡Hola che!» y tiene los encabezados `Para girar izquierda …` y `Para correr …`). | original | una captura por variante |
| [`euler/`](euler/) | Problema 1 de Project Euler (suma de múltiplos de 3 o 5 menores que 1000). Muestra `The answer is: 233168`, que es correcto. Mezcla español e inglés. | original | `euler/captura.png` |
| [`arreglo/`](arreglo/) | Un arreglo de 100 números hecho con punteros (`principalvector`). Escribe los valores 1, 33 y 0 leídos del arreglo. | original | `arreglo/captura.png` |
| [`fibonacci/`](fibonacci/) | Imprime la serie de Fibonacci en la consola. | original | `fibonacci/captura.png` |
| [`triangle/`](triangle/) | Triángulo de Pascal dibujado con hexágonos. | parche `coord` | `triangle/captura.png` |
| [`horizon/`](horizon/) | El paisaje del desierto en su versión original en inglés (`Hor`). | parche `coord` | `horizon/captura.png` |
| [`fireworks/`](fireworks/) | Fuegos artificiales: al hacer clic en «FIREWORKS» del menú, aparecen estallidos sobre la silueta de una ciudad. | parche `coord` | `fireworks/captura.png` (después del clic) |
| [`parches/`](parches/) | `aplicar-parches.py`: genera una copia parcheada de `(6) el seso` sin tocar el original. | | |

**Procedencia.** `sorteo`, `desierto` y `holamundo-espiral` son de Pablo y su colaborador Elender. `euler`, `arreglo`, `fibonacci`, `triangle`, `horizon` y `fireworks` son ejemplos en inglés de la Orden Osmosian (Gerry Rzeppa) que Pablo reunió; se incluyen con el nombre del fuente original y un único cambio: la primera línea `To run:` pasó a `Para ejecutar:`, porque SAL exige esa rutina de entrada y sin ella dice `Necesito una rutina para 'ejecutar'`. Si hay alguna duda sobre la licencia de esos seis, conviene retirarlos.

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

Se probaron 33 fuentes de `examples.zip` y de `ejemplos.zip` (adaptados con `Para ejecutar`), con el `el seso` original y, si fallaban, con los parches: **9 compilaron y corrieron, 21 no compilaron y 3 eran duplicados exactos de otros.** Además se probaron aparte `sorteo` y `desierto`. Los que no compilan:

| Programa | Error |
|---|---|
| `p7`, `p7G`, `p8`, `primes`, `primesgen`, `pg` (Project Euler, primos) | `No sé cómo 'Write [string] at/on the default console'`: usan la consola de la CAL, que SAL no define. |
| `eulerGRZ`, `p2` | `No sé cómo 'Read [string]'`. |
| `peuler`, `newP1euler` | `Creo que he visto este tipo 'top' en algún lugar previo; debe estar duplicado`: definen un tipo que ya existe en `el seso`. |
| `pollock` | `No sé cómo 'convert [letter] in/into/to [string]'`. |
| `preu` | `Ya sé cómo 'quit'`: redefine una rutina que ya existe. |
| `E1`, `ej1-1`, `ej2-1`, `simple sentences`, `simulator`, `pruebo`, `Lizbeth/loteria` | Faltan rutinas auxiliares que en la versión completa están en el mismo archivo, o usan otro `el seso`. |
| `pruebacastellano` | `No sé cómo 'Bip'`. |

No se agregó:

- **Entregas de alumnos (`ucc2021`, otras carpetas de `ejemplos.zip`).** No se publican ni sus programas ni sus nombres. Las que se miraron son mayormente traducciones de los ejemplos del manual. Hay también un `.csv` de una encuesta, que no se abrió.
- **`HAL`, `HAL2`, `HAL3`** (compiladores híbridos de Pablo): requieren una decisión aparte.
- **`sample.zip`**: es el Cal Monet en inglés (el original de `guia/ejemplo-sal-monet/`).
- **`the_golden_key.zip`**: el `cal-4400` (compilador en inglés), un PDF y `bible.txt`; no es Español Llano.
- **Los `.exe` de los zip no se ejecutaron.** Todo lo probado se compiló desde su fuente.
