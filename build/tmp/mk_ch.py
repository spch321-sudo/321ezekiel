import json,sys
n=int(sys.argv[1])
bp=json.load(open('blueprint.json',encoding='utf-8'))['ch'][str(n)]
d=json.load(open(f'build/tmp/ch{n:02d}.json',encoding='utf-8'))
c={k:bp[k] for k in ('n','t','sub','lv','arc','sec')}
c['serm']={'pts':bp['serm']['pts']}
c.update(d['ch'])
order=['n','t','sub','lv','arc','sec','serm','q','truth','mv','card','self','t321','grp','prac','safe']
c={k:c[k] for k in order}
json.dump({'ch':c,'issues':d['issues']},open(f'ch/{n:02d}.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
