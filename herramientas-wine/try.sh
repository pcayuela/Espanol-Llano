#!/usr/bin/env bash
# uso: try.sh NOMBRE FUENTE [EL_SESO]   -> compila y deja nt_NOMBRE_err.png (barra superior) ; imprime si hay t.exe
S=$(echo /tmp/claude-0/-home-user/*/scratchpad); n=$1; src=$2; seso=${3:-"/home/user/espanol-llano/(6) el seso"}
d=$S/nt/$n; rm -rf "$d"; mkdir -p "$d/t"; cp "$seso" "$d/t/zseso"; cp "$src" "$d/t/$n"
cd $S && timeout 170 bash tc.sh "$d" $S/nt_$n.png >/dev/null 2>&1
ls "$d/t" | grep -c 't.exe' | sed 's/^/exe: /'
convert $S/nt_$n.png -crop 1280x50+0+0 +repage $S/nt_${n}_err.png
