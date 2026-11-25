# -*- coding: utf-8 -*-
"""英文版單位管線。extract / show Pxxx / check Pxxx|all / merge
譯文檔 en/out/Pxxx.txt：每單位 `@@id@@` 單獨一行，下一行起是譯文（可多行）。"""
import json,re,sys,os,glob
sys.path.insert(0,'scripts')
HAN=re.compile(r'[㐀-鿿]'); HEB=re.compile(r'[֐-׿]+')
TAG=re.compile(r'</?([a-zA-Z0-9]+)[^>]*>')
def L(p): return json.load(open(p,encoding='utf-8'))
def skip_path(P,data):
    # P: tuple path
    if P[0]=='txt': return True
    if P[0]=='blk' and P[-1]=='lit': return True
    if P[0]=='ch' and len(P)>=3 and P[2] in ('t','sub','arc','mv'): return True
    if P[0]=='lesson' and len(P)==3 and P[2] in ('title','vol'): return True
    if P[0]=='issues' and len(P)==3 and P[2]=='t' and data['issues'][P[1]]['id'].startswith('ISS00_'): return True
    return False
def walk(o,P,data,out):
    if isinstance(o,str):
        if HAN.search(o) and not skip_path(P,data): out.append(o)
    elif isinstance(o,list):
        for i,x in enumerate(o): walk(x,P+(i,),data,out)
    elif isinstance(o,dict):
        for k,v in o.items(): walk(v,P+(k,),data,out)
def extract(size=13000):
    data=L('build/ez_tc.json'); seq=[]
    for n in range(1,49):
        s=str(n)
        walk(data['ch'][n-1],('ch',n-1),data,seq); walk(data['blk'][s],('blk',s),data,seq)
        walk(data['serm'][s],('serm',s),data,seq); walk(data['lesson'][s],('lesson',s),data,seq)
    for k in ('issues','terrain','tracks'): walk(data[k],(k,),data,seq) if k!='issues' else [walk(x,('issues',i),data,seq) for i,x in enumerate(data['issues'])]
    seen={}; units=[]
    for s in seq:
        if s not in seen: seen[s]=len(units); units.append(s)
    packs=[];cur=[];n=0
    for i,s in enumerate(units):
        cur.append(i); n+=len(HAN.findall(s))
        if n>=size: packs.append(cur); cur=[]; n=0
    if cur:
        if packs and n<size*0.4: packs[-1]+=cur
        else: packs.append(cur)
    json.dump({str(i):s for i,s in enumerate(units)},open('en/units.json','w',encoding='utf-8'),ensure_ascii=False)
    json.dump({f'P{k+1:03d}':v for k,v in enumerate(packs)},open('en/packs.json','w'))
    # in/ 檔
    for k,v in enumerate(packs):
        open(f'en/in/P{k+1:03d}.txt','w',encoding='utf-8').write(''.join(f'@@{i}@@\n{units[i]}\n' for i in v))
    print('單位',len(units),'漢字',sum(len(HAN.findall(s)) for s in units),'包',len(packs))
def parse(path):
    t=open(path,encoding='utf-8').read()
    t=re.sub(r'^## NOTE:.*$\n?','',t,flags=re.M)
    parts=re.split(r'^@@(\d+)@@\n',t,flags=re.M); d={}
    for i in range(1,len(parts),2): d[int(parts[i])]=parts[i+1].rstrip('\n')
    return d
def check_pack(pk,verbose=True):
    units=L('en/units.json'); ids=L('en/packs.json')[pk]; e=[]
    p=f'en/out/{pk}.txt'
    if not os.path.exists(p): return [f'{pk}: 缺檔 {p}']
    d=parse(p)
    extra=set(d)-set(ids); miss=[i for i in ids if i not in d]
    if extra: e.append(f'多餘 id {sorted(extra)[:5]}')
    if miss: e.append(f'缺 id {miss[:8]}（共{len(miss)}）')
    for i in ids:
        if i not in d: continue
        z=units[str(i)]; t=d[i]
        if HAN.search(t): e.append(f'[{i}] 仍有漢字：{HAN.search(t).group(0)} …{t[max(0,HAN.search(t).start()-15):HAN.search(t).start()+15]!r}')
        if '「' in t or '」' in t or '『' in t or '』' in t: e.append(f'[{i}] 殘留「」')
        if re.search(r'ISS\d\d',t): e.append(f'[{i}] 議題代碼外露')
        tz=[(m.group(0)[:2]=='</',m.group(1)) for m in TAG.finditer(z)]; tt=[(m.group(0)[:2]=='</',m.group(1)) for m in TAG.finditer(t)]
        if tz!=tt: e.append(f'[{i}] HTML 標籤不一致：原 {len(tz)} 個、譯 {len(tt)} 個')
        for h in HEB.findall(z):
            if h not in t: e.append(f'[{i}] 希伯來文走樣：{h[:12]}'); break
        for num in re.findall(r'\d+(?::\d+)?',re.sub(r'<[^>]*>','',z)):
            if num not in re.sub(r'<[^>]*>','',t): e.append(f'[{i}] 數字/經節 {num} 不見了'); break
        nz=len(HAN.findall(z))
        if nz>=8 and len(t.split())<nz*0.25: e.append(f'[{i}] 譯文過短（{len(t.split())} 字 vs {nz} 漢字）')
        if '\n' in z and z.count('\n')!=t.count('\n'): e.append(f'[{i}] 換行數不同')
    return e
def fixheb(pk):
    units=L('en/units.json'); p=f'en/out/{pk}.txt'; t=open(p,encoding='utf-8').read()
    parts=re.split(r'^(@@\d+@@\n)',t,flags=re.M); out=[parts[0]]; n=0
    for k in range(1,len(parts),2):
        i=parts[k][2:-3]; body=parts[k+1]; src=HEB.findall(units[i]); got=list(HEB.finditer(body))
        if src and len(src)==len(got):
            it=iter(src); nb=HEB.sub(lambda m:next(it),body)
            n+= nb!=body; body=nb
        out+= [parts[k],body]
    open(p,'w',encoding='utf-8').write(''.join(out)); print('Hebrew 還原單位數',n)
def show(pk): print(open(f'en/in/{pk}.txt',encoding='utf-8').read())
if __name__=='__main__':
    c=sys.argv[1]
    if c=='extract': extract(int(sys.argv[2]) if len(sys.argv)>2 else 13000)
    elif c=='fixheb': fixheb(sys.argv[2])
    elif c=='show': show(sys.argv[2])
    elif c=='check':
        pks=list(L('en/packs.json')) if sys.argv[2]=='all' else sys.argv[2:]
        bad=0
        for pk in pks:
            e=check_pack(pk)
            if e: bad+=1; print(pk,'✗'); [print('  ',x) for x in e[:15]]
            else: print(pk,'✓ 通過')
        sys.exit(1 if bad else 0)
