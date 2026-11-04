#!/usr/bin/env python3
"""Genera una copia parcheada de `(6) el seso` SIN tocar el original.
Uso:  python3 aplicar-parches.py "(6) el seso" "el seso parcheado" [coord] [elegir]
  coord   cambia «'s x» / «'s y» por «'s x-coord» / «'s y-coord» (209 apariciones, 148 líneas; las líneas
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
    pat = re.compile(r"('s) ([xy])\b(?!-)")
    def rep(m):
        a = b.rfind("\n", 0, m.start()) + 1
        return m.group(0) if b[a:m.start()].lstrip().startswith("\\") else "%s %s-coord" % (m.group(1), m.group(2))
    b = pat.sub(rep, b)
if "elegir" in op:
    clave = "Para elegir un número entre otro número y un tercer número;"
    assert b.count(clave) == 1, "no encontré el encabezado de referencia"
    b = b.replace(clave, "\\" + clave + "\r\nPara elegir un número entre otro number y un tercer number;")
open(dst, "wb").write(b.encode("latin1"))
print("listo:", dst)
