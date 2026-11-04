#!/usr/bin/env python3
"""Genera una copia parcheada de `(6) el seso` SIN tocar el original.
Uso:  python3 aplicar-parches.py "(6) el seso" "el seso parcheado" [coord] [elegir]
  coord   cambia «spot's x» / «spot's y» (y lo mismo con center, start, end, context y line) por x-coord / y-coord, y
          «pair's x» / «difference's y» por x-number / y-number (las líneas
          comentadas con \\ no se tocan). Sin esto, cualquier programa que use rutinas de líneas o
          puntos falla con «No hay 'y' dentro del 'spot'», porque el registro `spot` se define con
          x-coord / y-coord (línea 13450) pero muchas rutinas siguen escribiendo «spot's x» y «spot's y».
  elegir  agrega el encabezado mixto «Para elegir un número entre otro number y un tercer number;»
          (el arreglo que propuso Gerry Rzeppa en 2020) para poder escribir «Elegir un número entre 1 y 9.»
Sin opciones aplica las dos. El archivo es ISO-8859-1 con CRLF; se trabaja en bytes para no alterarlo."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
op = set(sys.argv[3:]) or {"coord", "elegir"}
b = open(src, "rb").read().decode("latin1")
if "coord" in op:
    # Dueños cuyo campo `x`/`y` pasó a llamarse x-coord/y-coord (spot y los registros que lo contienen).
    # Los de tipo `pair` (y `difference`, que es un pair) tienen x-number/y-number. gprect y text no se tocan.
    sufijo = {"spot": "coord", "center": "coord", "start": "coord", "end": "coord", "context": "coord", "line": "coord",
              "pair": "number", "difference": "number"}
    pat = re.compile(r"(\w+)('s) ([xy])\b(?!-)")
    def rep(m):
        a = b.rfind("\n", 0, m.start()) + 1
        if b[a:m.start()].lstrip().startswith("\\") or m.group(1) not in sufijo:
            return m.group(0)
        return "%s%s %s-%s" % (m.group(1), m.group(2), m.group(3), sufijo[m.group(1)])
    b = pat.sub(rep, b)
if "elegir" in op:
    clave = "Para elegir un número entre otro número y un tercer número;"
    assert b.count(clave) == 1, "no encontré el encabezado de referencia"
    b = b.replace(clave, "\\" + clave + "\r\nPara elegir un número entre otro number y un tercer number;")
open(dst, "wb").write(b.encode("latin1"))
print("listo:", dst)
