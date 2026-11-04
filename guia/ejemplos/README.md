# Ejemplos nuevos en Español Llano

Cuatro programas pequeños, compilados con `sal-1016.exe` y ejecutados (bajo Wine). Sirven para ver construcciones distintas de las del Sal Monet del manual: dibujo con tortuga, teclado y sonido, dibujo de líneas con el ratón, y un cuestionario con puntaje.

## De dónde salen

Las ideas vienen de las entregas de un curso de «Fundamentos de Programación» (junio de 2020) que están en la carpeta `Classroom` de la cuenta de UCC del autor del repo. Se revisaron los fuentes de 18 archivos comprimidos con programas de SAL y se compararon contra el Sal Monet de esta carpeta:

- Todas usaban el mismo `el seso` (hash idéntico al de este repo).
- Catorce archivos contenían variantes del Sal Monet, con cambios menores (otros artistas, un botón nuevo, otros textos). No se convirtieron en ejemplos porque no agregan construcciones nuevas.
- Cinco archivos contenían programas distintos (uno de ellos traía también una variante del Monet). Cuatro de sus ideas se rehicieron aquí **desde cero**; el código y los textos son nuevos, y no se copió ni se incluyó ningún trabajo de alumnos ni sus nombres.

| Idea de la entrega | Ejemplo nuevo | Qué cambia |
|---|---|---|
| Un programa de 17 líneas que dibuja con la tortuga | [`rueda`](rueda/) | Misma familia de instrucciones (`Comenzar`, `Girar`, `Mover`, `Escribir`); otra figura, otra palabra y otros ángulos. Es la que más se parece al original. |
| «Mi música»: una rutina por tecla con `Beep` | [`piano`](piano/) | Una sola rutina para sonar (`sonar usando una frecuencia y un nombre`), teclado de piano (blancas abajo, negras arriba), botón **Escala**. |
| «Graficar»: ejes y una recta entre dos puntos | [`graficador`](graficador/) | El estado se lleva con un número (`el paso`) y no con textos; marca los puntos y tiene botón **Borrar**. |
| Cuestionario de tres preguntas con botones | [`cuestionario`](cuestionario/) | Cuatro preguntas sobre Español Llano, tres opciones, puntaje, comentario y botón **Reiniciar**. |

No se rehízo `Formulas` (un ayudante de fórmulas de Física con un botón por fórmula): usa la misma idea de botones y textos que el cuestionario. Tampoco el «adivina el artista» basado en imágenes de internet, que no se puede probar sin red.

## Cómo compilarlos

1. Crear un directorio nuevo (su nombre será el del `.exe`) y copiar adentro **solo** `(6) el seso` y el archivo fuente del ejemplo (el que no tiene extensión, por ejemplo `piano`).
2. Abrir el fuente en SAL y elegir **Ejecutar** (menú **E**).

Los fuentes están en ISO-8859-1 con finales de línea CRLF, como los demás. No les agregues extensión.

## Qué se probó

| Ejemplo | Compilación | Ejecución |
|---|---|---|
| `rueda` | Compiló al primer intento. | Dibuja 36 palabras girando, que se van aclarando; termina con la tecla ESC (no se probó la tecla). |
| `piano` | Falló una vez: «No puedo encontrar el tipo 'nota'». | Las teclas `h` y `w` muestran `LA (440 Hz)` y `DO sostenido (277 Hz)`; una tecla inválida muestra un aviso; **Escala** termina en `DO agudo (523 Hz)`. Bajo Wine con pantalla virtual no hay audio, así que **no se escuchó** ningún sonido: solo se comprobó que la llamada a `Beep` se ejecutó y que el estado cambió. |
| `graficador` | Compiló al primer intento. | Dos clics dibujan los puntos rojos y la recta azul; **Borrar** vuelve al principio. |
| `cuestionario` | Falló dos veces (ver abajo). | Se respondieron las cuatro preguntas: `¡Correcto!`, `Incorrecto` y puntaje final «3 de 4»; un clic extra tras el final no cambia nada; **Reiniciar** vuelve a la pregunta 1; **Abandonar** cierra el programa. |

Todo se probó bajo Wine, no en Windows.

## Errores del compilador que aparecieron

Sirven para escribir en este lenguaje sin repetirlos:

| Mensaje de SAL | Causa | Solución |
|---|---|---|
| `No puedo encontrar el tipo 'nota'` | El nombre de la rutina decía `sonar una nota usando …`. El artículo `una` crea un parámetro del tipo `nota`, que no existe. | No usar `un` / `una` en el nombre de una rutina salvo para parámetros reales: `sonar usando …`. |
| `¡Epa! Necesito un 'es' o un 'son' por ahí, pero todo lo que encontré fue 'a'` | Se definió `El botón a es un botón.`: `a` es un artículo. | Elegir otro nombre (`alfa`, `beta`, `gama`). |
| `Necesito un decisor con las palabras '[número] is/are igual in/into/to [número]'` | Se escribió `Si el número es igual a la clave`. | Para dos números se dice `Si el número es la clave` (y `no es` para lo contrario). |

## Detalles que conviene saber

- `Esperar la tecla escape` (en `rueda`) y los demás comandos de tortuga están definidos en `el seso`; el programa no necesita nada más.
- Los números se unen a un texto con `luego`: `Mostrar "Puntaje: " luego el puntaje en el estado.`
- Para comparar un número con un literal basta `Si el paso es 0, …`.
