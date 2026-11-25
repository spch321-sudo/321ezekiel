# -*- coding: utf-8 -*-
import json,re,hashlib,sys,shutil,os
sys.path.insert(0,'scripts')
from icu_t2s import t2s
R='/home/claude/work/jer_ref/'; O='site/'
data=json.load(open('build/ez_tc.json',encoding='utf-8'))
shell=open('build/shell_ezk.html',encoding='utf-8').read()
sc=json.load(open('build/scmap.json',encoding='utf-8'))
scj=json.dumps(sc,ensure_ascii=False,separators=(',',':'))
assert '<script id="SCMAP"' in shell
shell=re.sub(r'(<script id="SCMAP" type="application/json">).*?(</script>)',lambda m:m.group(1)+scj+m.group(2),shell,flags=re.S)
dj=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
MARK='<script id="DATA" type="application/json">'
assert '@@DATA@@' in shell
i=shell.find('@@DATA@@')
# head 在 DATA 前；原殼 head 結尾含 DATA 開標籤
def build_html(sc_page):
    h=shell
    pre,post=h.split('@@DATA@@')
    pre_end=pre.rfind(MARK)
    assert pre_end>=0 or True
    return pre,post
src=open(R+'index.html',encoding='utf-8').read()
k=src.find('<script id="DATA"'); head_open=src[k:src.find('>',k)+1]
assert head_open==MARK,head_open
pre,post=shell.split('@@DATA@@')
tc=pre+MARK+dj+post
# 簡體頁：head 轉簡 + SCBOOT
BOOT=('<script id="SCBOOT">/* 简体页：一律以简体开启（保留其他存档） */\ntry { var K=\'r321.ezk.v1\', o=JSON.parse(localStorage.getItem(K)||\'null\'); if(!o||typeof o!==\'object\') o={ v:1, last:1, steps:{}, notes:{}, lnote:{}, prac:{}, mem:{}, set:{ fs:1, grk:1, dark:0, role:\'\' }, seen:{} }; o.set=o.set||{}; o.set.sc=1; localStorage.setItem(K,JSON.stringify(o)); } catch(e){}\n</script>\n')
scpage=t2s(pre)+BOOT+MARK+dj+post
for f,t in (('index.html',tc),('sc.html',scpage)): open(O+f,'w',encoding='utf-8').write(t)
# manifest
mf=json.load(open(R+'manifest.webmanifest',encoding='utf-8'))
mf.update(name='以西結書講義',short_name='以西結書講義',description='以西結書全書四十八章：逐節原文解經、講章逐字稿、教學講章、321 生命應用。',id='/321ezekiel/')
json.dump(mf,open(O+'manifest.webmanifest','w',encoding='utf-8'),ensure_ascii=False,indent=2)
me=json.load(open(R+'manifest-en.webmanifest',encoding='utf-8'))
me.update(name='Ezekiel Study Notes',short_name='Ezekiel Notes',description='Ezekiel, all forty-eight chapters: verse-by-verse exposition from the original, sermon manuscripts, teaching lessons and 321 life application.',id='/321ezekiel/en.html')
json.dump(me,open(O+'manifest-en.webmanifest','w',encoding='utf-8'),ensure_ascii=False,indent=2)
# sw
sw=open(R+'sw.js',encoding='utf-8').read()
ver='以西結書-'+hashlib.sha1(tc.encode()).hexdigest()[:12]
sw=sw.replace('耶利米書','以西結書').replace("const V = '以西結書-87214b32552e'",f"const V = '{ver}'")
assert ver in sw and 'PFX = \'以西結書-\'' in sw and '耶利米' not in sw
open(O+'sw.js','w',encoding='utf-8').write(sw)
json.dump({'v':ver},open(O+'version.json','w'),ensure_ascii=False)
open(O+'README.md','w',encoding='utf-8').write('國度321空中團契《321聖經講義》以西結書（四十八章、1,273 節），版本 v1.0。\n\n- 繁體中文：`index.html`（完整）\n- 简体中文：`sc.html`（完整；同一支 App 以简体开启，内嵌繁简对照表一键切换）\n- English：`en.html`\n\n發佈網址：https://spch321-sudo.github.io/321ezekiel/\n\n離線可用的 PWA；iPhone 請先刪除舊的主畫面捷徑再重新「加入主畫面」。\n')
open(O+'.nojekyll','w').close()
print(ver,{f:os.path.getsize(O+f) for f in ('index.html','sc.html')})
