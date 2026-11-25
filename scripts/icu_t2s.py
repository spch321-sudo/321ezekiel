import ctypes,array
_i=ctypes.CDLL('libicui18n.so.74')
def _u16(s):
    a=array.array('H',s.encode('utf-16-le')); return (ctypes.c_uint16*(len(a)+1))(*a,0), len(a)
_i.utrans_openU_74.restype=ctypes.c_void_p
_e=ctypes.c_int(0); _id,_n=_u16('Traditional-Simplified')
_t=_i.utrans_openU_74(_id,_n,0,None,0,None,ctypes.byref(_e)); assert _e.value<=0,_e.value
_t=ctypes.c_void_p(_t)
def t2s(s):
    out=[]
    for k in range(0,len(s),8000):
        c=s[k:k+8000]; a=array.array('H',c.encode('utf-16-le')); n=len(a); cap=n*3+64
        arr=(ctypes.c_uint16*cap)(*a); lim=ctypes.c_int32(n); e=ctypes.c_int(0)
        tl=ctypes.c_int32(n)
        _i.utrans_transUChars_74(_t,arr,ctypes.byref(tl),cap,0,ctypes.byref(lim),ctypes.byref(e))
        assert e.value<=0,e.value
        out.append(bytes(memoryview(arr).cast('B')[:tl.value*2]).decode('utf-16-le'))
    return ''.join(out)
if __name__=='__main__': print(t2s('耶和華的榮光充滿了殿，計畫甚好，畫記號，著手，唱著唱著，乾旱，繸，後來'))
