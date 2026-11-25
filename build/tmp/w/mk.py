import json,sys,re
n=int(sys.argv[1]); mn=int(sys.argv[2]); title=sys.argv[3]
bp=json.load(open('blueprint.json'))
pts=bp['ch'][str(n)]['serm']['pts']
T=''.join(json.load(open(f'txt/{n:02d}.json')))
norm=lambda s:re.sub(r'[「」『』\s]','',s)
TN=norm(T)
bl=[['h','《'+title+'》']]
for ln in open(f'build/tmp/w/s{n}.txt',encoding='utf-8'):
    ln=ln.strip()
    if not ln: continue
    if ln.startswith('Q '): bl.append(['q',ln[2:]])
    else: bl.append(['p',ln])
for b in bl:
    if b[0]=='q':
        parts=[x for x in re.split(r'[，。；！？：、…]',norm(b[1])) if len(x)>=8]
        bad=[x for x in parts if x not in TN]
        if bad: print('NOTVERBATIM?',b[1][:40],bad[:2])
json.dump({'min':mn,'pts':pts,'blocks':bl},open(f'serm/{n:02d}.json','w'),ensure_ascii=False,indent=1)
c=sum(len(b[1]) for b in bl); print(n,'blocks',len(bl),'chars',c,'q',sum(b[0]=='q' for b in bl))
