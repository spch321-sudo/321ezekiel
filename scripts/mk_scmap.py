# -*- coding: utf-8 -*-
"""從本卷內容 + 外殼推導 SCMAP，並以 ICU 逐字驗證。輸出 build/scmap.json"""
import json,re,collections,sys
sys.path.insert(0,'scripts')
from icu_t2s import t2s
KEEP=set('繸')
han=re.compile(r'[㐀-鿿豈-﫿]')
def leaves(o,out):
    if isinstance(o,str): out.append(o)
    elif isinstance(o,list):
        for x in o: leaves(x,out)
    elif isinstance(o,dict):
        for v in o.values(): leaves(v,out)
def corpus_fields(data,shell):
    f=[]; leaves(data,f)
    sh=re.sub(r'<script id="SCMAP".*?</script>','',shell,flags=re.S)
    f+= re.split(r'(?<=[\n。！？])',sh)   # 外殼切成句，避免單一巨串
    return [x for x in f if han.search(x)]
def convert_fields(fields):
    SEP='\u0001'
    out=[]; buf=[]; n=0
    res=[]
    for x in fields:
        buf.append(x); n+=len(x)
        if n>6000: res+=t2s(SEP.join(buf)).split(SEP); buf=[]; n=0
    if buf: res+=t2s(SEP.join(buf)).split(SEP)
    assert len(res)==len(fields)
    return res
def build(fields):
    conv=convert_fields(fields)
    for a,b in zip(fields,conv): assert len(a)==len(b),(a[:20],b[:20])
    T='\u0001'.join(fields); S='\u0001'.join(conv)
    # KEEP
    S=''.join(c if c not in KEEP else c for c in S)
    S=list(S)
    for i,c in enumerate(T):
        if c in KEEP: S[i]=c
    S=''.join(S)
    cnt=collections.defaultdict(collections.Counter)
    for a,b in zip(T,S):
        if han.match(a): cnt[a][b]+=1
    dflt={c:cn.most_common(1)[0][0] for c,cn in cnt.items()}
    m_tc=''.join(c for c in sorted(dflt) if dflt[c]!=c); m_sc=''.join(dflt[c] for c in sorted(dflt) if dflt[c]!=c)
    # 偏離位置 → 詞組
    phr={}
    dev=[i for i,a in enumerate(T) if han.match(a) and S[i]!=dflt[a]]
    # 預建 n-gram 索引
    for i in dev:
        for L in range(2,9):
            key=T[i:i+L]
            if '\u0001' in key: break
            occ=[m.start() for m in re.finditer(re.escape(key),T)] if key not in phr else None
            if key in phr:
                if phr[key]==S[i:i+L]: break
                continue
            outs={S[o:o+L] for o in occ}
            if len(outs)==1:
                phr[key]=outs.pop(); break
        else:
            raise SystemExit(f'無法為偏離字建詞組：{T[max(0,i-5):i+8]!r}')
    return T,S,m_tc,m_sc,dict(phr),dflt
def apply(T,m_tc,m_sc,phr):
    cm=dict(zip(m_tc,m_sc)); heads=collections.defaultdict(list)
    for k in phr: heads[k[0]].append(k)
    for h in heads: heads[h].sort(key=len,reverse=True)
    out=[];i=0
    while i<len(T):
        c=T[i]
        for k in heads.get(c,()):
            if T.startswith(k,i): out.append(phr[k]); i+=len(k); break
        else: out.append(cm.get(c,c)); i+=1
    return ''.join(out)
def apply2(T,m_tc,m_sc,phr):
    cm=dict(zip(m_tc,m_sc)); heads=collections.defaultdict(list)
    for k in phr: heads[k[0]].append(k)
    for h in heads: heads[h].sort(key=len,reverse=True)
    out=[];starts=[];i=0
    while i<len(T):
        c=T[i]
        for k in heads.get(c,()):
            if T.startswith(k,i): out.append(phr[k]); starts+=[i]*len(k); i+=len(k); break
        else: out.append(cm.get(c,c)); starts.append(i); i+=1
    return ''.join(out),starts
def make(data,shell):
    fields=corpus_fields(data,shell)
    T,S,m_tc,m_sc,phr,d=build(fields)
    for rnd in range(200):
        got,starts=apply2(T,m_tc,m_sc,phr)
        bad=next((i for i,(a,b) in enumerate(zip(got,S)) if a!=b),None)
        if bad is None: break
        st=starts[bad]; ok=False
        for lf in range(0,5):
            s0=st-lf
            if s0<0: break
            for L in range(bad-s0+1,bad-s0+9):
                key=T[s0:s0+L]
                if '\u0001' in key: break
                outs={S[o.start():o.start()+L] for o in re.finditer(re.escape(key),T)}
                if len(outs)==1 and key not in phr: phr[key]=outs.pop(); ok=True; break
            if ok: break
        if not ok: raise SystemExit(f'修補失敗 {T[max(0,bad-6):bad+8]!r}')
    got,_=apply2(T,m_tc,m_sc,phr)
    assert got==S,'驗證失敗：詞組＋逐字 ≠ ICU'
    print(f'SCMAP：逐字 {len(m_tc)}、詞組 {len(phr)}，與 ICU 逐字相同（{len(T)} 字）')
    return {'m':[m_tc,m_sc],'p':[[k,v] for k,v in sorted(phr.items())]}
if __name__=='__main__':
    data=json.load(open('build/ez_tc.json',encoding='utf-8')); shell=open('build/shell_ezk.html',encoding='utf-8').read()
    json.dump(make(data,shell),open('build/scmap.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
