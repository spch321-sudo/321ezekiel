import json,sys,re
n=int(sys.argv[1]); mn=int(sys.argv[2])
bp=json.load(open('../../blueprint.json'))
pts=bp['ch'][str(n)]['serm']['pts']
bl=[]
for ln in open(f'serm{n:02d}.txt',encoding='utf-8').read().split('\n'):
    ln=ln.strip()
    if not ln: continue
    if ln.startswith('# '): bl.append(['h',ln[2:]])
    elif ln.startswith('> '): bl.append(['q',ln[2:]])
    else: bl.append(['p',ln])
json.dump({'min':mn,'pts':pts,'blocks':bl},open(f'../../serm/{n:02d}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
txt=''.join(json.load(open(f'../../txt/{n:02d}.json',encoding='utf-8')))
norm=lambda s:re.sub(r'[，。；：！？、「」『』（）\s—…]','',s)
T=norm(txt)
for b in bl:
    for m in re.findall(r'「([^」]+)」',b[1]):
        if b[0]=='q' and len(norm(m))>6 and norm(m) not in T: print('QUOTE?',m[:40])
c=sum(len(b[1]) for b in bl); q=sum(b[0]=='q' for b in bl)
print(len(bl),c,q)
