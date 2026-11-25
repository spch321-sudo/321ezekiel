import json,sys
n=sys.argv[1]
bp=json.load(open('blueprint.json'))['ch'][str(int(n))]
d=json.load(open(f'build/work/c{n}.json',encoding='utf-8'))
ch={k:bp[k] for k in ('n','t','sub','lv','arc','sec')}
ch['serm']={'pts':bp['serm']['pts']}
for k in ('q','truth','mv','card','self','t321','grp','prac','safe'): ch[k]=d[k]
order=['n','t','sub','lv','arc','sec','serm','q','truth','mv','card','self','t321','grp','prac','safe']
json.dump({'ch':{k:ch[k] for k in order},'issues':d['issues']},open(f'ch/{n}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
