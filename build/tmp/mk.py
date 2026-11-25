import json,sys,re
n=int(sys.argv[1]); mn=int(sys.argv[2])
bp=json.load(open('/home/claude/321ezekiel/blueprint.json'))
pts=bp['ch'][str(n)]['serm']['pts']
T=json.load(open(f'/home/claude/321ezekiel/txt/{n:02d}.json'))
txt=''.join(T)
blocks=[]
for l in open(f'/home/claude/321ezekiel/build/tmp/s{n}.txt',encoding='utf-8'):
    l=l.rstrip('\n')
    if not l.strip(): continue
    if l.startswith('# '): blocks.append(['h',l[2:]])
    elif l.startswith('q|'): blocks.append(['q',l[2:]])
    else: blocks.append(['p',l])
tot=sum(len(b[1]) for b in blocks)
print('blocks',len(blocks),'chars',tot)
norm=lambda s:re.sub(r'[「」『』]','',s)
for b in blocks:
    if b[0]=='q':
        inner=norm(b[1]).rstrip('。，；')
        if inner not in norm(txt): print('QUOTE?',b[1])
json.dump({'min':mn,'pts':pts,'blocks':blocks},open(f'/home/claude/321ezekiel/serm/{n:02d}.json','w'),ensure_ascii=False,indent=1)
