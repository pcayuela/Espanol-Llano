import re, sys
exe=open(sys.argv[1],'rb').read()
src=open(sys.argv[2],'rb').read().decode('latin1')
blocks=re.findall(r'^To ([^\r\n:]+):\r?\n((?:Intel \$[0-9A-Fa-f]+\.[^\r\n]*\r?\n)+)', src, re.M)
ok=bad=0; samples=[]
for name,body in blocks:
    b=bytes.fromhex(''.join(re.findall(r'Intel \$([0-9A-Fa-f]+)\.', body)))
    if len(b)<8: continue
    i=exe.find(b)
    if i>=0:
        ok+=1
        if len(samples)<8: samples.append((name,len(b),hex(0x400000+i)))
    else: bad+=1
print("rutinas solo-Intel (>=8 bytes):",ok+bad,"| halladas literalmente en el exe:",ok,"| no halladas:",bad)
for s in samples: print(s)
