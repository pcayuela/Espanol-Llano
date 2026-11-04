# Guía rápida de Español Llano

Esta guía explica cómo se **escribe** un programa en Español Llano, el lenguaje que compila SAL-1016. Para saber cómo usar SAL (abrirlo, compilar, ejecutar) ver el manual en `documentación/` y el `README.md`.

**De dónde sale lo que dice la guía.** Está armada con el manual «Programación en Español Llano» (`documentación/instrucciones v2.pdf`), la gramática (`documentación/ebnf`) y el código fuente de SAL, que está escrito en el propio lenguaje. Los ejemplos que vienen del manual se indican como tales. Los demás se tomaron del código fuente de `(6) el seso`. Esta guía es un resumen: el manual y el código siguen siendo la referencia.

## 1. La idea

Español Llano busca que el código se lea como una oración normal. El compilador no usa una gramática compleja: reconoce cinco tipos de oraciones y se guía por palabras clave (artículos, verbos, conjunciones y preposiciones).

```
Para ejecutar:
Poner en marcha.
Inicializar nuestras cosas.
Manejar eventos.
Finalizar nuestras cosas.
Apagar.
```

(Ejemplo del manual. `Poner en marcha` y `Apagar` están definidas en `el seso`.)

El compilador acepta las palabras clave en español y en inglés. El propio código de SAL mezcla ambos idiomas, y muchas rutinas tienen un encabezado en cada idioma:

```
Para agregar un byte a otro byte;
To add a byte to another byte:
```

(De `(6) el seso`.) Los dos encabezados definen la misma rutina.

## 2. Los cinco tipos de oraciones

| Tipo | Cómo empieza | Qué hace |
|---|---|---|
| Definición de tipo | `Un` / `Una` / `Algún` / `Alguna` | Define un tipo de dato |
| Definición de variable global | `El` / `La` / `Lo` / `Los` / `Las` | Define una variable global |
| Encabezado de rutina | `Para` | Define una rutina |
| Condicional | `Si` o `Cuando` | Ejecuta algo solo si se cumple una condición |
| Imperativo | cualquier otra palabra | Ordena hacer algo |

## 3. Nombres y artículos

- Lo que sigue a `un`, `una`, `otro`, `otra`, `algún`, `alguna` o `el`, `la`, `lo`, `los`, `las` se toma como un **nombre**, hasta encontrar un verbo simple (`es`, `son`, `puede`, `hace`), una conjunción (`y`, `e`, `o`, `u`), una preposición (`sobre`, `bajo`, `entre`, `hasta`), un texto literal, o un signo de puntuación.
- No se da nombre a las variables: se las nombra con un artículo y el nombre de su tipo. «Un evento» crea una variable local de tipo evento, y después se la cita como «el evento». Si hace falta una segunda del mismo tipo se dice «otro evento» o «el segundo evento».
- El resto de las palabras son solo palabras. Las excepciones son los operadores (`más`, `menos`, `veces`, `dividido por`, `luego`), las palabras `llamada` e `igual`, y los imperativos reservados `lazo`, `interrumpir`, `salir`, `repetir` y `diga`.

## 4. Reglas del lenguaje

Según el manual:

- No distingue mayúsculas de minúsculas.
- El orden de las definiciones no importa.
- **No hay `si` anidados.** Cada condicional entra en una línea.
- **No hay lazos anidados.** Se divide el código en rutinas.
- No hay objetos, ni números reales, ni ecuaciones. Las fracciones se manejan con razones (`335/113`).
- El código es procedimental, y cada declaración termina en punto.

## 5. Comentarios

Hay tres clases:

| Clase | Sintaxis | Para qué |
|---|---|---|
| Comentario simple | `\ texto hasta el fin de línea` | Anotaciones. El editor los muestra en celeste. |
| Observación | `[texto]` en una sola línea | Notas permanentes entre el código, por ejemplo `Llamar a "kernel32.dll" "Beep" con 220 [hertz] y 200 [ms].` |
| Calificador | `(texto)` en un encabezado de rutina | **No es un comentario común:** forma parte del nombre de la rutina y cambia cuál se llama. Ej.: `Para manejar un evento (refrescar):` |

## 6. Tipos de datos

Seis tipos primitivos incorporados:

| Tipo | Tamaño | Notas |
|---|---|---|
| Byte | 8 bits | De 0 a 255 |
| Wyrd | 16 bits | De -32768 a +32767 |
| Número | 32 bits | De -2147483648 a +2147483647 |
| Puntero | 32 bits | La dirección 0 es `nulo` (`nil`) |
| Bandera | 32 bits, usa 1 | `sí` o `no` |
| Registro | variable | Se le agregan campos |

Además hay:

- **Subtipos:** `Un conteo es un número.` `Un nombre es una cadena.`
- **Unidades de medida:** `Un centímetro es 10 milímetros.` `Una hora es 60 minutos.`
- **Registros:** agregan campos al registro base.

  ```
  Un elemento tiene
  una clase, una ruta, un directorio, un designador, una extensión,
  un tamaño, un win32finddata y un handle.
  ```
  (Del manual, glosario de archivos. La gramática usa `has` / `tiene`.)
- **Punteros:** `Un puntero de byte es un puntero a un byte.`
- **Cosas:** tipos dinámicos (consola, evento, imagen, texto, etc.). Quien los define se hace cargo de su memoria: normalmente una rutina `crear` que reserva memoria (`asignar memoria para ...`) y otra `destruir` que la libera (`desasignar ...`).

Las **cadenas** y las **subcadenas** son registros integrados. Muchos servicios de Windows piden cadenas terminadas en nulo: antes de llamarlos se usa `null terminate` sobre la cadena.

## 7. Variables globales

Empiezan con un artículo definido:

```
Un segundo es 1000 milisegundos.
El byte copyright es un byte igual a 169.
La pantalla tiene un cuadro, una altura de píxel y un ancho de píxel.
```

(La primera y la segunda son de `(6) el seso`; la tercera, del manual.) Las variables **locales** se crean dentro de una rutina con «un ...», y los **parámetros** con las mismas palabras en el encabezado. Se pasan siempre por referencia.

## 8. Rutinas

Cada rutina tiene un encabezado, que dice qué hace y qué parámetros usa, y un cuerpo con una o más declaraciones. Hay tres clases:

| Clase | Encabezado | Devuelve |
|---|---|---|
| Procedimiento | `Para algo:` | nada |
| Decisor | `Para decidir si algo:` | «sí» o «no» |
| Función | `Para poner el nombre de un tipo en un tipo:` | un valor calculado |

- Un encabezado puede terminar en `:` (y entonces sigue el cuerpo) o en `;`. Con `;` se declaran **frases alternativas** que hacen lo mismo, y la última lleva `:`.
- Hay que separar las palabras con espacios, también en los encabezados: el manual avisa de no olvidar los que preceden a «en» y «marcha» en `poner en marcha`.
- La rutina `Para ejecutar:` es el programa principal.
- Los decisores se usan dentro de un `si`: `Si el evento está modificado, manejar el evento (atajo); salir.`

## 9. Declaraciones

### Condicionales

```
SI esto, hacer esto; hacer esto; hacer esto.
```

- Después de la coma van los imperativos, separados por **punto y coma**. El primer **punto** termina la declaración.
- Las palabras negativas se descartan y se invierte la respuesta: «el punto no está en la caja» se resuelve preguntando si el punto está en la caja, y se invierte el resultado.

```
Si el número es mayor que 3, diga "Eso es mucho"; salir.
```

### Imperativos reservados

| Español | Inglés | Qué hace |
|---|---|---|
| `lazo` | `loop` | Inicio de un lazo |
| `interrumpir` | `break` | Sale del lazo |
| `repetir` | `repeat` | Vuelve al inicio del lazo |
| `salir` | `exit` | Sale de la rutina |
| `diga` | `say` | Devuelve «sí» o «no» desde un decisor |
| `privatizar` | `privatize` | Hace privado (una copia local) un parámetro, para poder modificarlo sin alterar el original. Ej.: `Privatizar la caja.` |

Los lazos no tienen condición de cabecera: se escriben con `lazo`, se sale con `interrumpir` y se vuelve con `repetir`:

```
Para manejar eventos:
Esperar un evento.
Si el evento es nulo, salir.
Manejar el evento.
Repetir.
```

(Del manual.) Algunas operaciones comunes se escriben como verbos, según el manual: `agregar esto a eso`, `restar esto de eso`, `multiplicar esto por eso`, `dividir esto por eso`.

### Llamar a Windows

```
Llamar "ole32.dll" "CoInitializeEx" con 0 y 2 [coinit_aparthreaded].
```

(Del manual; es una rutina de `(6) el seso`.) El código real de SAL lo escribe casi siempre en inglés, y esa forma también muestra cómo recibir un valor:

```
Call "kernel32.dll" "GetModuleHandleA" with 0 returning the module's handle.
```

La gramática (`ebnf`) lo define como `call "dll" "función" [with expresión {and expresión}] [returning término]`. Así `el seso` accede a las funciones de Windows.

### Código de máquina

```
Intel $8B8508000000.  \ mov eax,[ebp+8]
```

(De `(6) el seso`.) Inserta bytes de código de máquina x86 tal cual. Se usa en las rutinas más básicas, como sumar bytes.

## 10. Literales y expresiones

| Literal | Ejemplo |
|---|---|
| Número | `0`, `-2147483648` |
| Razón | `335/113`, `-19601/13860` |
| Mixto | `1-1/2`, `3-3/4` |
| Cadena | `"hola"`, con comillas dobles duplicadas para incluir una: `"dijo ""hola"""` |
| Nibble (hexadecimal) | `$8B85` |
| Bandera | `sí`, `no` |
| Puntero | `nulo` |

- **Operadores infijos:** `más`, `menos`, `veces`, `dividido por`, y `luego` (concatena cadenas). Ejemplo de `(6) el seso`, escrito en inglés: `Put "Error eliminando archivo '" then the path then "'." into el error de e/s.`
- **Razones entre términos:** `la altura / el ancho`, con espacios alrededor de la barra.
- **Forzar el tipo:** el manual lo escribe `el puntero AS A NÚMERO`. Casi no hace falta usarlo.
- **Signo:** `+ x` y `- x` llevan un espacio después del signo.

## 11. Posesivos

Se usa para entrar a los campos de un registro y para llamar a funciones de acceso:

```
el campo del registro
la altura de una caja
la longitud de una cadena
```

Hay tres posesivos especiales: `el objetivo de un puntero` (lo apuntado), `la magnitud de algo` (tamaño en bytes) y `el paradero de algo` (su dirección). En la gramática aparecen con `'s` en inglés (`the path's first`).

## 12. Errores

Las rutinas que acceden al sistema (archivos, red) no devuelven un código de error: dejan un texto en la variable global `el error de e/s`. Quien llama debe comprobar después de cada llamada que esté en blanco:

```
Destroy the nodette's path in the file system.
If el error de e/s is not blank, exit.
```

(De `(2) el administrador de archivos`, en inglés.)

## 13. Estructura de un proyecto

- Cada programa va en **su propio directorio**, con una copia de `el seso`.
- Los archivos fuente **no llevan extensión**: SAL solo compila archivos sin extensión. El orden y los nombres no importan.
- El `.exe` resultante se guarda en el mismo directorio y toma el nombre del directorio.
- Para compilar y ejecutar: abrir un archivo fuente en el editor de SAL y usar `Ejecutar` (menú **E**). `Detener` (menú **D**) corta un programa que quedó en un lazo eterno.

### Codificación de los archivos

Los fuentes de SAL están en **ISO-8859-1** (no UTF-8) con finales de línea CRLF. Si se guarda un archivo fuente en UTF-8, SAL lo muestra con los acentos rotos (`número` aparece como `nÃºmero`). Para escribir código propio con acentos hay que guardarlo en ISO-8859-1, o evitar los acentos.

### Programa mínimo

Un archivo fuente, con `el seso` en el mismo directorio:

```
Para ejecutar:
Poner en marcha.
Apagar.
```

Compila y se ejecuta, pero no hace nada visible. Este programa se compiló con `sal-1016.exe` (bajo Wine) copiándolo junto a `el seso`: SAL informó `500 ms` de compilación y generó un ejecutable de Windows de 32 bits de 102.400 bytes, que arrancó y terminó sin mostrar nada. El manual lo desarrolla hasta un programa completo (el «Sal Monet»), añadiendo una estructura de eventos, atajos de teclado y dibujo.

### Un programa de prueba que compila

Este programa se compiló con SAL (junto a una copia de `el seso`) y probó varias construcciones de esta guía: subtipo, global con `igual a`, registro con `tiene`, decisor con `diga`, condicional, lazo con `interrumpir` y `repetir`, y posesivo:

```
Para ejecutar:
Poner en marcha.
Probar definiciones.
Contar hasta el tope.
Probar posesivos.
Apagar.

Un contrapunto es un número.

El tope es un número igual a 10.

Una tarjeta tiene un nombre y un contrapunto.

Para decidir si un contrapunto es grande:
Si el contrapunto es mayor que 5, diga sí.
Diga no.

Para probar definiciones:
Poner 3 en un contrapunto.
Si el contrapunto es grande, salir.

Para contar hasta el tope:
Poner 0 en un contrapunto.
Lazo.
Si el contrapunto es mayor que el tope, interrumpir.
Agregar 1 al contrapunto.
Repetir.

Para probar posesivos:
Poner "hola" en el nombre de una tarjeta.
```

Lo que enseñaron los intentos que fallaron:

- **Un nombre de tipo que ya existe en `el seso` da error.** Con `Un contador es un número.` SAL respondió «Creo que he visto este tipo 'contador' en algún lugar previo; debe estar duplicado», porque `el seso` ya define `contador`. Conviene buscar el nombre en `el seso` antes de usarlo.
- **`Crear una X` solo existe para las «cosas»** (tipos dinámicos). Con un registro simple, SAL respondió «No sé cómo 'Crear [tarjeta]'», porque nadie definió una rutina `crear` para ese tipo.
- **El artículo `un` / `una` dentro del nombre de una rutina crea un parámetro.** `Para sonar una nota usando …` dio «No puedo encontrar el tipo 'nota'». Se corrige con `Para sonar usando una frecuencia y un nombre:`.
- **Los artículos no sirven como nombres.** `El botón a es un botón.` dio «¡Epa! Necesito un 'es' o un 'son' por ahí, pero todo lo que encontré fue 'a'». Hay que usar otro nombre (`alfa`).
- **Para comparar dos números se escribe `es`, sin «igual a».** `Si el número es la clave, …`; con «igual a» SAL pide un decisor que no existe.
- **Los mensajes de error aparecen en la barra superior**, en rojo, con el nombre del archivo, y se descartan con el botón «Bueno» o con ESC.

### Más ejemplos

En `guia/ejemplos/` hay cuatro programas nuevos y probados: una rueda de texto con la tortuga, un piano de teclado, un graficador de rectas y un cuestionario con puntaje. Su `README.md` explica de dónde salen las ideas, cómo compilarlos y qué se probó.

### Un programa completo: el Sal Monet

El manual desarrolla un programa gráfico completo, el **Sal Monet**. La versión final, corregida para que compile, está en `guia/ejemplo-sal-monet/` junto con el informe de la prueba: compila y se ejecuta (fondo pintado, estado, botones, cuadro de texto, teclado). Su parte de internet se probó con un servidor local: busca, descarga, «pinta» las imágenes y se navega entre ellas con AV PÁG, RE PÁG, INICIO y FIN. El listado del manual no compila tal cual; lo que hubo que cambiar está en esa carpeta. Dos cosas útiles de lo aprendido:

- **Muchos nombres de `el seso` existen en español y en inglés** (`el color blanco` y `the white color`; `Mostrar el cursor flecha` y `Show the arrow cursor`) y se pueden mezclar con el resto del código. El manual escribe `el color gris clarísimo`, que no existe: el nombre correcto es `el color gris muy muy claro`. Ante un error «No sé cómo…», conviene buscar el nombre en `el seso`, que mezcla los dos idiomas.
- **El encabezado de una rutina tiene que coincidir con la frase con que se la llama.** El manual define `hacer que un botón tenga un punto y un nombre` y la llama con `hacer el botón … usando el punto y …`; el compilador rechaza esa discrepancia.

## 14. Equivalencias español – inglés

| Español | Inglés |
|---|---|
| `para` | `to` |
| `si` | `if` |
| `sí` / `no` | `yes` / `no` |
| `nulo` | `nil` |
| `igual a` | `equal to` |
| `llamada` | `called` |
| `lazo` | `loop` |
| `interrumpir` | `break` |
| `repetir` | `repeat` |
| `salir` | `exit` |
| `diga` | `say` |
| `privatizar` | `privatize` |
| `llamar` | `call` |
| `más` / `menos` / `veces` | `plus` / `minus` / `times` |
| `dividido por` | `divided by` |
| `luego` | `then` |

## 15. Qué no cubre esta guía

- El glosario completo del manual (unas 60 páginas): el catálogo de tipos, rutinas y variables que ofrece `el seso`. Está en el PDF.
- La gramática formal: `documentación/ebnf`.
- El detalle de dibujo, impresión, documentos y consola.
- Además de los tres programas de arriba, se compiló y se probó el **Sal Monet** completo del manual (ver `guia/ejemplo-sal-monet/`), incluida la búsqueda y pintura de imágenes con un servidor local. No se probó con un buscador real ni con una impresora real. Desde 2026 el ejemplo usa Bing en lugar de Google Images (Google dejó de servir las imágenes); ver la sección «Actualización de 2026» de ese README.
- Los ejemplos sueltos no se compilaron uno por uno. Se compilaron tres programas completos: el programa mínimo y la estructura de eventos del manual (`Para ejecutar` con `inicializar`, `manejar eventos`, `finalizar` y un manejador de evento), además del programa de prueba de la sección 13. Ninguno se *ejecutó* más allá de comprobar que el compilador lo aceptara y que el programa generado arrancara. Los fragmentos cortos del resto de la guía están tomados del manual o del código fuente y pueden necesitar las definiciones de `el seso` para compilar.
