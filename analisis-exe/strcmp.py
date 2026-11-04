"""Compara los literales de texto de la fuente con los strings del .exe.

Uso: python3 -I strcmp.py sal-1016.exe fuente1 fuente2 ...
Escribe 'ausentes.txt' (literales de la fuente que no estan en el .exe) junto al script.
"""
import re, sys, os, collections

exe = open(sys.argv[1], 'rb').read()
files = sys.argv[2:]
outdir = os.path.dirname(os.path.abspath(__file__))

def literals(text):
    """Literales "..." fuera de comentarios (EBNF: un backslash fuera de string abre un comentario hasta el fin de linea)."""
    out, i, n, instr, cur = [], 0, len(text), False, []
    while i < n:
        c = text[i]
        if instr:
            if c == '"':
                if i + 1 < n and text[i + 1] == '"':
                    cur.append('"'); i += 2; continue
                out.append(''.join(cur)); instr, cur = False, []
            elif c == '\n':
                instr, cur = False, []
            else:
                cur.append(c)
        else:
            if c == '"':
                instr = True
            elif c == '\\':
                while i < n and text[i] != '\n':
                    i += 1
                continue
        i += 1
    return out

lits = collections.OrderedDict()
for f in files:
    t = open(f, 'rb').read().decode('latin1').replace('\r', '')
    for s in literals(t):
        lits.setdefault(s, set()).add(os.path.basename(f)[:3])

cand = [s for s in lits if len(s) >= 4 and s.strip()]
present = {s for s in cand if s.encode('latin1') in exe}
absent = [s for s in cand if s not in present]
print("literales distintos (>=4 car.):", len(cand),
      "| presentes en el exe:", len(present), "| ausentes:", len(absent))
byf = collections.defaultdict(lambda: [0, 0])
for s in cand:
    for f in lits[s]:
        byf[f][0 if s in present else 1] += 1
print("por archivo (presentes, ausentes):", dict(byf))
open(os.path.join(outdir, 'ausentes.txt'), 'w').write('\n'.join(absent) + '\n')

# Texto legible en la seccion data del exe (0x2000..0x2000+0x1d8ac) sin coincidencia en la fuente
srcall = ''.join(open(f, 'rb').read().decode('latin1') for f in files)
runs = re.findall(rb'[\x20-\x7e\xa0-\xff]{8,}', exe[0x2000:0x2000 + 0x1d8ac])
pat = re.compile(r"^[A-Za-z\xc0-\xff¿¡][A-Za-z\xc0-\xff0-9 ,.'¿?¡!:;()/-]*$")
txt = [r.decode('latin1') for r in runs if pat.match(r.decode('latin1')) and r.count(b' ') >= 2]
extra = [s for s in txt if s not in srcall]
print("cadenas de texto legible (>=8 car., >=3 palabras):", len(txt),
      "| sin coincidencia en la fuente:", len(extra))
