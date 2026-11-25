# -*- coding: utf-8 -*-
"""合併英文版 DATA → build/ez_en.json"""
import json,re,sys,glob
sys.path.insert(0,'scripts')
import en_units as U, web
HAN=U.HAN
L=U.L
data=L('build/ez_tc.json'); units=L('en/units.json'); canon=L('en/canon.json'); packs=L('en/packs.json')
tr={}
for pk in packs:
    d=U.parse(f'en/out/{pk}.txt')
    for i,t in d.items(): tr[units[str(i)]]=t
assert len(tr)==len(units),(len(tr),len(units))
import os
if os.path.exists('en/delta_units.json'):
    du=L('en/delta_units.json'); dp=L('en/delta_packs.json')
    for pk in dp:
        d=U.parse(f'en/out/{pk}.txt')
        for i,t in d.items(): tr[du[i]]=t
def web_ref(n,a,z): return [web.get('ezek',n,v) for v in range(a,z+1)]
def rep(o,P):
    if isinstance(o,str):
        if HAN.search(o) and not U.skip_path(P,data):
            if o not in tr and o.replace('蹚','趟') in tr: return tr[o.replace('蹚','趟')]
            assert o in tr,('未譯',P,o[:30]); return tr[o]
        return o
    if isinstance(o,list): return [rep(x,P+(i,)) for i,x in enumerate(o)]
    if isinstance(o,dict): return {k:rep(v,P+(k,)) for k,v in o.items()}
    return o
out={}
# ch
chs=[]
for n,c in enumerate(data['ch'],1):
    s=str(n); nc={}
    for k,v in c.items():
        if k in('t','sub'): nc[k]=canon[k][s]
        elif k=='arc': nc[k]=canon['arc'][v]
        elif k=='mv':
            m=re.match(r'以西結書(\d+):(\d+)(?:--(\d+))?$',v['r']); assert m,v['r']
            a=int(m.group(2)); z=int(m.group(3) or a)
            nc[k]={'t':' '.join(web_ref(n,a,z)),'r':f'Ezek {n}:{a}'+(f'--{z}' if z!=a else '')}
        else: nc[k]=rep(v,('ch',n-1,k))
    chs.append(nc)
out['ch']=chs
out['txt']={}
for s,v in data['txt'].items():
    n=int(s); vs=[web.get('ezek',n,i) for i in range(1,len(v)+1)]
    assert all(vs),('WEB缺節',n); out['txt'][s]=vs
out['blk']={}
for s,bl in data['blk'].items():
    n=int(s); nb=[]
    for b in bl:
        x={}
        for k,v in b.items():
            if k=='lit': x[k]='<blockquote><p>“'+' '.join(web_ref(n,b['a'],b['z']))+'”</p></blockquote>'
            else: x[k]=rep(v,('blk',s,len(nb),k))
        nb.append(x)
    out['blk'][s]=nb
out['serm']={s:rep(v,('serm',s)) for s,v in data['serm'].items()}
iss=[]
for i,x in enumerate(data['issues']):
    y=rep(x,('issues',i))
    if x['id'].startswith('ISS00_'): y['t']=canon['iss'][x['id']] if x['id'] in canon['iss'] else None; assert y['t'],x['id']
    iss.append(y)
out['issues']=iss
out['terrain']=rep(data['terrain'],('terrain',)); out['tracks']=rep(data['tracks'],('tracks',))
wc=lambda s:len(re.findall(r"[A-Za-z0-9’'\-]+",re.sub(r'<[^>]*>',' ',s)))
out['lesson']={}
for s,l in data['lesson'].items():
    n=int(s); B=rep(l['blocks'],('lesson',s,'blocks'))
    hi=[i for i,b in enumerate(B) if b[0]=='h']; st=hi[10]
    ch=out['ch'][n-1]
    out['lesson'][s]={'no':n,'vol':f'Study Notes on Ezekiel 321, Lesson {n} · Ezekiel Chapter {n}','title':f"{ch['t']}—{ch['sub']}",
      'chars':sum(wc(b[1]) for b in B[:st] if b[0]=='p'),'min':l['min'],'deep':l['deep'],
      'dchars':sum(wc(b[1][0])+wc(b[1][1]) for b in B if b[0]=='d'),
      'tchars':sum(wc(b[1]) for b in B[st+1:] if b[0] in 'pstmn'),'blocks':B}
js=json.dumps(out,ensure_ascii=False)
bad=HAN.findall(js); print('殘留漢字',len(bad),''.join(bad[:30]))
assert not bad
json.dump(out,open('build/ez_en.json','w',encoding='utf-8'),ensure_ascii=False)
print('ok',len(js))
