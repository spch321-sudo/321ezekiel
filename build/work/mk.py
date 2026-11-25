import json,sys
n=sys.argv[1]; mn=int(sys.argv[2]); title=sys.argv[3]
bp=json.load(open('blueprint.json'))
pts=bp['ch'][str(int(n))]['serm']['pts']
bl=[["h",title]]
for l in open(f'build/work/s{n}.txt',encoding='utf-8'):
    l=l.rstrip('\n')
    if not l.strip(): continue
    t,x=l.split(' ',1); bl.append([t,x])
json.dump({"min":mn,"pts":pts,"blocks":bl},open(f'serm/{n}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(sum(len(b[1]) for b in bl[1:]),len(bl))
