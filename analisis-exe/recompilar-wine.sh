#!/usr/bin/env bash
# Recompila los seis archivos fuente de SAL con el propio sal-1016.exe (bajo Wine, en Linux)
# y compara el resultado con el original.
#
# Uso:    bash recompilar-wine.sh RUTA/sal-1016.exe RUTA/DIRECTORIO_CON_LOS_FUENTES
# Ej.:    bash analisis-exe/recompilar-wine.sh sal-1016.exe .
#
# Requisitos (Ubuntu/Debian):
#   sudo dpkg --add-architecture i386 && sudo apt-get update
#   sudo apt-get install -y wine wine32:i386 xvfb xdotool imagemagick
#
# Maneja la interfaz de SAL con el raton, en una pantalla virtual de 1280x1024, siguiendo el
# procedimiento del manual: abrir los seis archivos y elegir Ejecutar (menu E).
# Es fragil: depende de las posiciones de los elementos en pantalla. Si falla, ejecutar con
# KEEP=1 para conservar el directorio de trabajo y las capturas (shot_*.png).
set -euo pipefail

EXE=$(realpath "${1:?falta la ruta de sal-1016.exe}")
SRC=$(realpath "${2:?falta el directorio con los fuentes}")
NAME=sal-1016                      # el .exe resultante lleva el nombre del directorio
DISPLAY_NUM=97

WORK=$(mktemp -d)
mkdir -p "$WORK/orig" "$WORK/drive/$NAME" "$WORK/prefix"
cp "$EXE" "$WORK/orig/sal-1016.exe"
n=0
while IFS= read -r -d '' f; do cp "$f" "$WORK/drive/$NAME/"; n=$((n+1)); done \
  < <(find "$SRC" -maxdepth 1 -type f -name '(*' ! -name '*.*' -print0)
[ "$n" -eq 6 ] || { echo "Se esperaban 6 archivos fuente '(N) ...' y hay $n en $SRC" >&2; exit 2; }

export WINEPREFIX="$WORK/prefix" WINEARCH=win32 WINEDEBUG=-all DISPLAY=":$DISPLAY_NUM"
Xvfb ":$DISPLAY_NUM" -screen 0 1280x1024x24 >/dev/null 2>&1 &
XVFB=$!
cleanup() {
  wineserver -k 2>/dev/null || true
  kill "$XVFB" 2>/dev/null || true
  [ "${KEEP:-0}" = 1 ] || rm -rf "$WORK"
}
trap cleanup EXIT
sleep 2

wineboot -i >/dev/null 2>&1
# Unidad D: de Wine apuntando al directorio de trabajo: asi la lista de unidades de SAL
# es siempre c:\, d:\, z:\ y las posiciones de pantalla son las mismas en cualquier maquina.
ln -sfn "$WORK/drive" "$WINEPREFIX/dosdevices/d:"

shot() { import -window root "$WORK/shot_$1.png" 2>/dev/null || true; }
dclick() { xdotool mousemove "$1" "$2" click --repeat 2 --delay 120 1; }

( cd "$WORK/orig" && wine sal-1016.exe >"$WORK/wine.log" 2>&1 & )
for _ in $(seq 1 60); do
  xdotool search --name '^sal-1016$' >/dev/null 2>&1 && break
  sleep 1
done
sleep 15; shot 1_inicio

dclick 110 116; sleep 3            # d:\   (segunda unidad, tras c:\)
dclick 80 92;  sleep 3; shot 2_directorio   # d:\sal-1016\ (unico elemento)
xdotool mousemove 400 400 click 1; sleep 1
xdotool mousemove 30 90 mousedown 1; sleep 0.5
xdotool mousemove 150 150; sleep 0.3
xdotool mousemove 300 214; sleep 0.5
xdotool mouseup 1; sleep 1; shot 3_seleccion   # arrastrar para seleccionar los 6
xdotool key Return; sleep 6; shot 4_abiertos
xdotool mousemove 168 40 click 1; sleep 2        # menu E
xdotool mousemove 230 72 click 1                 # Ejecutar

OUT="$WORK/drive/$NAME/$NAME.exe"
for _ in $(seq 1 120); do [ -s "$OUT" ] && break; sleep 1; done
sleep 3; shot 5_fin
[ -s "$OUT" ] || { echo "No se generó $NAME.exe (ver capturas con KEEP=1)" >&2; exit 3; }

A=$(sha256sum "$EXE" | cut -d' ' -f1)
B=$(sha256sum "$OUT" | cut -d' ' -f1)
echo "original:    $A"
echo "recompilado: $B"
if [ "$A" = "$B" ]; then echo "RESULTADO: idénticos byte a byte"; else echo "RESULTADO: DIFIEREN"; fi
[ "${KEEP:-0}" = 1 ] && echo "Directorio de trabajo conservado: $WORK"
[ "$A" = "$B" ]
