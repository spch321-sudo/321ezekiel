import json,sys
n=int(sys.argv[1]); mn=int(sys.argv[2])
bp=json.load(open('blueprint.json',encoding='utf-8'))['ch'][str(n)]
lines=[l.rstrip('\n') for l in open(f'build/tmp/serm{n:02d}.txt',encoding='utf-8') if l.strip()]
blocks=[["h","《"+bp['t']+"》"]]
for l in lines:
    if l.startswith('Q|'): blocks.append(["q",l[2:]])
    else: blocks.append(["p",l])
json.dump({"min":mn,"pts":bp['serm']['pts'],"blocks":blocks},open(f'serm/{n:02d}.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(blocks),sum(len(b[1]) for b in blocks))
