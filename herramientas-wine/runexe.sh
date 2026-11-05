#!/usr/bin/env bash
# uso: runexe.sh DIR_t EXE OUT.png [SEG] [TECLAS...]
S=$(echo /tmp/claude-0/-home-user/*/scratchpad); export WINEPREFIX=$S/wine/prefix WINEARCH=win32 WINEDEBUG=-all DISPLAY=:94
D=$1; E=$2; O=$3; W=${4:-10}; shift 4 2>/dev/null
Xvfb :94 -screen 0 1280x1024x24 >/dev/null 2>&1 & XV=$!; sleep 2
(cd "$D" && wine "$E" >/dev/null 2>&1 &); sleep $W
for k in "$@"; do xdotool key "$k"; sleep 1; done; sleep 2
import -window root "$O"; wineserver -k 2>/dev/null; kill $XV 2>/dev/null
