# -*- coding: utf-8 -*-
"""壓出每章素材總表 build/brief/NN.md（寫作者唯一素材來源）。"""
import json, sys, os
sys.path.insert(0, 'scripts')
import wlc
bp = json.load(open('blueprint.json', encoding='utf-8'))
W = wlc.load('/home/claude/work/morphhb/wlc/Ezek.xml')
os.makedirs('build/brief', exist_ok=True)
THREAD = '神的榮耀離開，又歸回；祂為自己的名，叫人知道祂是耶和華；祂親自作牧人、賜新心新靈、使枯骨復活，最後以「耶和華的所在」為這城的名。'
GUARD = ['不排末世時間表、不算日子；不指名現代國家；不給任何現在的人貼標籤。',
 '語法／解釋爭議先陳列各家立場，再給本講義判斷。經文一律和合本（見下方逐節經文，引用必須逐字）。',
 '果效是忍耐與更愛主，不是恐慌。次序：先讓經文講完，321 才在末端自然接上。',
 '碰到性暴力、喪親、重病、自傷、長期無望：`care` 必須先保護讀者（不追問、不勸「要堅強」、不放大畫面）。']
for n in range(1, 49):
    c = bp['ch'][str(n)]
    t = json.load(open(f'txt/{n:02d}.json', encoding='utf-8'))
    L = [f'# 以西結書 {n} 章素材總表', '', f'章題：{c["t"]}　副題：{c["sub"]}　等級：{c["lv"]}　弧段：{c["arc"]}', '',
         '## 全卷的一條線', THREAD, '', '## 守則'] + [f'- {g}' for g in GUARD]
    L += ['', '## 前後章', f'- 上一章：{bp["ch"][str(n-1)]["t"] if n>1 else "—"}', f'- 下一章：{bp["ch"][str(n+1)]["t"] if n<48 else "—"}']
    L += ['', '## 藍圖：分段', *[f'- {r}　{s}' for r, s in c['sec']], '', '## 藍圖：講章三點（點題／範圍／引句，已定案）',
          *[f'- {p}　{r}　「{q}」' for p, r, q in c['serm']['pts']]]
    L += ['', '## 和合本逐節（引用必須逐字）']
    L += [f'{i}　{v}' for i, v in enumerate(t, 1)]
    L += ['', '## 希伯來文（WLC，逐節；詞｜Strong 號）']
    for i in range(1, len(t) + 1):
        ws = W.get((n, i), [])
        L.append(f'{i}　' + '　'.join(f'{w[0]}[{"+".join("H"+s for s in w[3])}]' for w in ws))
    st = [(t_['gk'], s) for t_ in bp['tracks'] for s in t_['stops'] if s[0].split(':')[0] == str(n)]
    if st:
        L += ['', '## 本章在字軌上的停靠點'] + [f'- {g} {s[0]} {s[1]}' for g, s in st]
    L += ['', '## 全卷立場（ISS00，本章 say 要回指的）']
    for i in bp['issues']:
        if i['ch'][0] <= n <= i['ch'][1]:
            L += [f'- {i["id"]} {i["t"]}（{i["r"]}）：{i["say"]}']
    ix = [x for x in bp['issue_index'] if x['ch'][0] == n]
    L += ['', '## 本章議題索引（階段 D 寫全文）'] + ([f'- {x["id"]} {x["t"]}' for x in ix] or ['- （無；若需要可自補 1–2 條，id 依序）'])
    open(f'build/brief/{n:02d}.md', 'w', encoding='utf-8').write('\n'.join(L))
print('ok 48')
