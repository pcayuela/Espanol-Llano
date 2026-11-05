# Herramientas para compilar y probar con Wine (Linux)

Tres scripts que se usaron en la sesión en la nube para compilar un fuente con `sal-1016.exe` bajo Wine y mirar el resultado. **Tienen rutas fijas de esa sesión** (prefijo de Wine, carpeta `orig/` con `sal-1016.exe`, pantalla virtual Xvfb `:96`/`:94`): hay que adaptarlas. En Windows no hacen falta: se abre el fuente en SAL y se elige **Ejecutar** (menú **E**).

| Script | Qué hace |
|---|---|
| `tc.sh DIR SALIDA.png` | Abre SAL, abre el primer fuente de `DIR/t/` con el ratón (doble clic en coordenadas fijas) y elige Ejecutar; deja una captura. |
| `try.sh NOMBRE FUENTE [EL_SESO]` | Arma `DIR/t/` con el fuente y una copia de `el seso` (llamada `zseso` para que quede segunda en la lista), llama a `tc.sh` y recorta la barra de error. |
| `runexe.sh DIR EXE SALIDA.png [SEG]` | Ejecuta el `.exe` generado en una pantalla virtual y saca una captura. |

Trampas aprendidas: terminar Wine con `wineserver -k` puede perder cambios de registro recientes (esperar con `wineserver -w`); el fuente debe quedar primero en el listado de archivos; los fuentes deben ser ISO-8859-1 con CRLF y sin extensión.
