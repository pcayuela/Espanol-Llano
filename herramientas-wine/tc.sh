#!/usr/bin/env bash
# uso: tc.sh DIR_CON_t  (contiene t/'el seso' y t/pruebas)  -> compila 'pruebas' con SAL en Wine y deja capturas
set -u
D=$(realpath "$1"); OUT=$2
export WINEPREFIX=/tmp/claude-0/-home-user/2e45a95c-2ddf-5edd-ac16-4195469918dd/scratchpad/wine/prefix WINEARCH=win32 WINEDEBUG=-all DISPLAY=:96
Xvfb :96 -screen 0 1280x1024x24 >/dev/null 2>&1 & XV=$!
sleep 2
ln -sfn "$D" "$WINEPREFIX/dosdevices/d:"
( cd /tmp/claude-0/-home-user/2e45a95c-2ddf-5edd-ac16-4195469918dd/scratchpad/wine/orig && wine sal-1016.exe >/dev/null 2>&1 & )
for _ in $(seq 1 60); do xdotool search --name '^sal-1016$' >/dev/null 2>&1 && break; sleep 1; done; sleep 15
dc(){ xdotool mousemove $1 $2 click --repeat 2 --delay 120 1; }
dc 110 116; sleep 3; dc 60 92; sleep 3; dc 100 116; sleep 4
xdotool mousemove 168 40 click 1; sleep 2; xdotool mousemove 230 72 click 1; sleep 15
import -window root "$OUT"
ls -la "$D/t" | grep -c 'exe' ; ls "$D/t"
wineserver -k 2>/dev/null; kill $XV 2>/dev/null
