import json,re,sys
han=lambda s:len(re.findall(r'[一-鿿]',s))
L=lambda p:json.load(open(p,encoding='utf-8'))
bp=L('blueprint.json')
D={'ch':[],'txt':{},'blk':{},'serm':{},'issues':list(bp['issues']),'terrain':bp['terrain'],'tracks':bp['tracks'],'lesson':{}}
for n in range(1,49):
    f=f'{n:02d}'
    c=L(f'ch/{f}.json'); D['ch'].append(c['ch']); D['issues']+=c['issues']
    D['txt'][str(n)]=L(f'txt/{f}.json'); D['blk'][str(n)]=L(f'blk/{f}.json'); D['serm'][str(n)]=L(f'serm/{f}.json')
    l=L(f'lesson/{f}.json'); B=l['blocks']; hi=[i for i,b in enumerate(B) if b[0]=='h']; s=hi[10]
    D['lesson'][str(n)]={'no':n,'vol':f'《321以西結書講義》第{n}課·以西結書第{n}章','title':l['title'],
     'chars':sum(han(b[1]) for b in B[:s] if b[0]=='p'),'min':60,'deep':8,
     'dchars':sum(han(b[1][0])+han(b[1][1]) for b in B if b[0]=='d'),
     'tchars':sum(han(b[1]) for b in B[s+1:] if b[0] in 'pstmn'),'blocks':B}

tit={i['id']:i['t'] for i in D['issues']}
CODE=re.compile(r'(?:議題\s?)?(ISS\d\d_\d)(?:「[^」]{1,30}」)?')
def fix(o,key=None):
    if isinstance(o,str):
        if key=='id': return o
        return CODE.sub(lambda m:'議題「'+tit[m.group(1)].replace('「','『').replace('」','』').replace('--','–')+'」',o)
    if isinstance(o,list): return [fix(x) for x in o]
    if isinstance(o,dict): return {k:fix(v,k) for k,v in o.items()}
    return o
D=fix(D)
json.dump(D,open('build/ez_tc.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print({k:len(v) for k,v in D.items()})
