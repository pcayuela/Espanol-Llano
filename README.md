# Español Llano — SAL-1016

**SAL-1016** es un compilador y entorno de desarrollo para programar en **Español Llano**, una variante en español del *Plain English* de la Orden Osmosiana. Compila archivos de texto escritos en Español Llano y los convierte en programas ejecutables para Windows/Intel (x86, 32 bits). Se puede recompilar a sí mismo en unos tres segundos.

Es autocontenido: no requiere instalación ni dependencias. Todo el entorno (interfaz, editor, administrador de archivos, procesador de documentos y compilador) está escrito en el propio lenguaje.

## Contenido

| Archivo | Rol |
|---|---|
| `sal-1016.exe` | Ejecutable de Windows. Doble clic para iniciarlo. |
| `(1) el escritorio` | Interfaz de usuario: menúes, pestañas, diálogos. |
| `(2) el administrador de archivos` | Acceso directo al sistema de archivos. |
| `(3) el editor` | Editor de archivos de texto. |
| `(4) el escriba` | Editor de documentos (con el que se produjo el manual). |
| `(5) el compilador` | El compilador. |
| `(6) el seso` | El núcleo: tipos y rutinas de bajo nivel. |
| `lexicon/lexicon` | Lista de palabras usada por el entorno. |
| `documentación/` | Manual, gramática y atajos de teclado. |

### Documentación

- `documentación/instrucciones v2.pdf`: manual «Programación en Español Llano» (120 páginas): visión de conjunto, un programa de ejemplo, glosario e índice.
- `documentación/instrucciones` a `instrucciones v5`: el mismo manual en el formato nativo del entorno (se abre con el escriba). La `v5` es la más reciente.
- `documentación/ebnf`: gramática léxica y sintáctica del lenguaje.
- `documentación/shortcut keys`: atajos de teclado.

## Uso rápido

1. Hacer doble clic en `sal-1016.exe`.
2. Navegar con los menúes alfabéticos (A–Z) de arriba y las pestañas de abajo. No hay barras de desplazamiento: se desplaza manteniendo el clic derecho y arrastrando.
3. Abrir un archivo de texto con el administrador de archivos abre el editor; abrir un documento abre el escriba.

### Compilar el compilador («Bebé SAL»)

1. Copiar los seis archivos `(1)` a `(6)` a un directorio nuevo, por ejemplo `C:\Bebé SAL`.
2. Abrirlos todos (seleccionarlos y presionar ENTER).
3. En el menú **E**, elegir **Ejecutar**.

Cada programa se guarda en su propio directorio. Un archivo sin extensión se toma como código fuente, y el nombre del directorio es el nombre que recibe el `.exe`.

## Importante: no renombrar los archivos

Los archivos de código fuente **no tienen extensión a propósito**: es la convención del compilador. No les agregues `.txt` ni otra extensión. Tampoco conviene convertir su codificación (ISO-8859-1, finales de línea CRLF) sin probar antes que sigan compilando. Por eso los acentos pueden verse mal en GitHub.

## Créditos

Código basado en el trabajo de **The Osmosian Order of Plain English Programmers** / *La Orden Osmosiana de los Programadores en Español Llano* ([www.osmosian.com](http://www.osmosian.com)), con adaptación al español de Pablo Cayuela.
© 2006, 2015, 2017, 2018, según indican los encabezados de los archivos fuente.

Soporte (según el manual): help@osmosian.com
