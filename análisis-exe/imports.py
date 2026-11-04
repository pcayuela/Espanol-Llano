import struct, sys
d = open(sys.argv[1],'rb').read()
base=0x400000
def rd(rva,n): return d[rva:rva+n]   # file offset == RVA (both alignments 0x1000)
def cstr(rva):
    e=d.index(b'\0',rva); return d[rva:e].decode('latin1')
imp=0x1000; out={}
while True:
    oft,ts,fc,name,ft = struct.unpack('<5I', rd(imp,20))
    if name==0: break
    dll=cstr(name); i=0
    while True:
        thunk=struct.unpack('<I', rd((oft or ft)+4*i,4))[0]
        if thunk==0: break
        fn=cstr((thunk&0x7fffffff)+2) if not thunk&0x80000000 else 'ord%d'%(thunk&0xffff)
        out[base+ft+4*i]=(dll,fn); i+=1
    imp+=20
for k in sorted(out): print('%08x %s!%s'%(k,*out[k]))
