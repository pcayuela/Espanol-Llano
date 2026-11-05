# Programas de alumnos (anonimizados)

Programas hechos con Español Llano por alumnos de un curso de la UCC (2021). Se incluyen los que **compilan y corren** con `sal-1016.exe` bajo Wine (no en Windows). Casi todos son variantes de los ejemplos del manual: la espiral de «Hola Mundo», el reloj, la caja con puntos, el paisaje, el generador de lotería; algunos tienen ideas propias (la rueda con rayos, la cámara, la cara).

## Cómo se anonimizó

- Las carpetas se llaman `alumno-NN`. **El número es al azar**: no sigue el orden de las entregas ni ningún criterio, y la correspondencia con las entregas originales no se guardó en el repositorio.
- Se revisaron los textos de cada programa (cadenas y comentarios) y se reemplazaron los nombres propios que aparecían (en tres programas, un nombre dentro de un texto que se dibuja; ahora dice «Alumno»). Se volvieron a compilar y ejecutar después del cambio.
- Se dejaron afuera dos programas con mensajes personales o de contenido propio de su autor.
- Se conservó el código tal como lo escribió cada alumno, salvo el cambio de arriba y la primera línea (`To run:` pasó a `Para ejecutar:` donde hizo falta). Por eso hay errores de ortografía, mezcla de español e inglés y comentarios en el código.

## Cómo se probó

Cada programa se compiló con una copia de `el seso` con los **dos parches** de [`../ejemplos-2/parches/`](../ejemplos-2/parches/) (`coord` y `elegir`) y se ejecutó 9 segundos en una pantalla virtual; la captura es de ese momento. No se probó cuáles necesitan realmente cada parche; algunos compilan con el `(6) el seso` original y otros no.

Se probaron 46 programas distintos de alumnos: **36 compilan, 10 no** (por rutinas que solo existían en la copia de `el seso` de cada alumno). De los 36 se descartaron 5 más:

- 3 que compilan pero no hacen nada visible: uno termina enseguida porque su rutina principal llama a `apagar` antes de dibujar; otro borra la pantalla en cada vuelta; y otro dibuja solo una línea y no sigue.
- 2 con contenido personal de su autor.

Quedan los 31 de abajo.

| Carpeta | Qué hace |
|---|---|
| [`alumno-01`](alumno-01/) | Fondo celeste con un sol dibujado con texto. |
| [`alumno-02`](alumno-02/) | Caja llena de puntos al azar. |
| [`alumno-03`](alumno-03/) | Triángulo de celdas (variante del de Pascal). |
| [`alumno-04`](alumno-04/) | Espiral de «HOLA MUNDO». |
| [`alumno-05`](alumno-05/) | Espiral de «HOLA MUNDO». |
| [`alumno-06`](alumno-06/) | Espiral de texto con mensaje en la consola. |
| [`alumno-07`](alumno-07/) | Generador de números de sorteo. |
| [`alumno-08`](alumno-08/) | Espiral de «Hola Mundo» con giro a la izquierda. |
| [`alumno-09`](alumno-09/) | Espiral de «¡hola mundo!» con avance en milímetros. |
| [`alumno-10`](alumno-10/) | Espiral de texto con pluma gorda. |
| [`alumno-11`](alumno-11/) | Espiral de texto con pluma delgada. |
| [`alumno-12`](alumno-12/) | Cartel de texto y líneas giratorias. |
| [`alumno-13`](alumno-13/) | Reloj con manecillas animadas. |
| [`alumno-14`](alumno-14/) | Texto con adornos. |
| [`alumno-15`](alumno-15/) | Espiral de texto con saludo. |
| [`alumno-16`](alumno-16/) | Reloj con manecillas. |
| [`alumno-17`](alumno-17/) | Espiral de «HOLA MUNDO» (una letra por vuelta). |
| [`alumno-18`](alumno-18/) | Ilusión óptica de líneas rectas. |
| [`alumno-19`](alumno-19/) | Reloj con segundero. |
| [`alumno-20`](alumno-20/) | Cajas llenas de puntos al azar. |
| [`alumno-21`](alumno-21/) | Texto en espiral. |
| [`alumno-22`](alumno-22/) | Paisaje del desierto. |
| [`alumno-23`](alumno-23/) | Cara dibujada con texto: círculo, letras, sonrisa y nariz. |
| [`alumno-24`](alumno-24/) | Rueda con rayos y texto de neumático. |
| [`alumno-25`](alumno-25/) | Paisaje del desierto (versión en inglés). |
| [`alumno-26`](alumno-26/) | Espiral de «Hola». |
| [`alumno-27`](alumno-27/) | Dibujo de una cámara con texto. |
| [`alumno-28`](alumno-28/) | Ojos dibujados con texto. |
| [`alumno-29`](alumno-29/) | Generador de números de lotería (5 dígitos). |
| [`alumno-30`](alumno-30/) | Espiral de «HOLA MUNDO» con letras medianas. |
| [`alumno-31`](alumno-31/) | Cajas llenas de puntos al azar con rótulo. |
