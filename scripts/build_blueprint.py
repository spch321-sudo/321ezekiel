# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0, 'scripts')
from blueprint_src import CH, ARC_OF, TERRAIN
from tracks_src import TRACKS
from issues_src import ISS00
import wlc

# 各章議題索引（階段 D 才寫全文）：(章, [(標題, 回指/備註)])
IDX = {
 1: ['1:1「三十年」與紀年', '四活物與輪'],
 2: ['吃書卷：甜如蜜與哀號歎息', '先知被差往「悖逆之家」'],
 3: ['守望者與血的責任（回指 ISS00_3）', '七天驚駭與啞口：不診斷先知、不把奇特行動當作要效法的樣式'],
 4: ['側臥三百九十日與四十日', '糞火為何改了'],
 5: ['三分之一、三分之一、三分之一', '「父親要吃兒子」：圍城的慘劇'],
 7: ['「結局到了」與日子：不排時間表'],
 8: ['搭模斯是誰', '殿中暗室與拜日頭'],
 9: ['額上的「記號」與啟 7、9', '神為甚麼讓先知留下哀求'],
 10: ['10 章與 1 章對讀：活物就是基路伯', '火炭撒在城上'],
 11: ['新心新靈的第一次應許', '榮耀離城停在東山'],
 13: ['女先知與符咒', '假先知的辨認（不貼標籤）'],
 14: ['挪亞、但以理、約伯（不用這節斷定別人的禱告無效）', '偶像在心裡'],
 16: ['婚姻與性的意象（回指 ISS00_4；care 最重）', '撒馬利亞與所多瑪的姊妹'],
 17: ['嫩枝與香柏樹（不下定論）', '背約與誓言'],
 18: ['個人責任與「犯罪的，他必死亡」（回指 ISS00_3；不用來責備喪親者、受害者）', '「自做一個新心」'],
 20: ['「不美的律例」與「不能使人活著的惡規」', '為我名的緣故'],
 22: ['站在破口（不把責任壓在單獨一人身上）', '各階層的罪'],
 23: ['兩姊妹的比喻（回指 ISS00_4；care 最重）'],
 24: ['妻子之死（不追問、不勸「要堅強」）', '鍋與流人血的城'],
 28: ['推羅王（回指 ISS00_5）', '伊甸園與基路伯'],
 29: ['尼布甲尼撒與泰爾的工價：預言「未應驗」的問題（並陳）'],
 33: ['守望者再受差遣', '聽道而不行'],
 34: ['牧人（不拿這章攻擊任何教會領袖；回指謙卑）', '我的僕人大衛'],
 36: ['為我名的緣故', '新心新靈與新約（路 22:20；林後 3；約 3）'],
 37: ['枯骨（回指 ISS00_6；care：喪親、重病、長期無望者）', '兩根木杖'],
 38: ['歌革（回指 ISS00_7）'],
 39: ['歌革的結局（回指 ISS00_7）', '七年的柴與七個月的葬埋'],
 40: ['新殿（回指 ISS00_8）'],
 43: ['榮耀歸回（回指 ISS00_8）'],
 44: ['撒督的子孫與利未人'],
 47: ['河水從殿下流出（回指 ISS00_8）', '死海變甜與「不得治好」之地'],
 48: ['城的名字：耶和華的所在（回指 ISS00_8）'],
}

def rng(c, a, z): return f'{c}:{a}--{z}'

ch = {}
for n in range(1, 49):
    t, sub, lv, secs, pts = CH[n]
    ch[str(n)] = dict(
        n=n, t=t, sub='、'.join(sub.split('、')) if '、' in sub else '、'.join(sub),
        lv=lv, arc=ARC_OF[n],
        sec=[[rng(n, a, z), s] for a, z, s in secs],
        serm=dict(pts=[[p, rng(n, a, z), q] for p, a, z, q in pts]))

W = wlc.load('/home/claude/work/morphhb/wlc/Ezek.xml')
tracks = []
for gk, tr, gl, code, root, keys, stops, ins in TRACKS:
    tot = sum(1 for ws in W.values() for w in ws if any(s in keys for s in w[3]))
    tracks.append(dict(gk=gk, tr=tr, gl=gl, code=code, root=root, n=tot,
                       stops=[[f'{c}:{v}', f'「{q}」{m}', 'top' if t else ''] for c, v, q, m, t in stops], ins=ins))

issues = [dict(i, con=[]) for i in ISS00]
issue_index = []
for c in sorted(IDX):
    for k, title in enumerate(IDX[c], 1):
        issue_index.append(dict(id=f'ISS{c:02d}_{k}', t=title, ch=[c]))

bp = dict(ch=ch, terrain=dict(points=[[c + 0.083, h, 0, lab, pos] for c, h, lab, pos in TERRAIN]),
          tracks=tracks, issues=issues, issue_index=issue_index)
json.dump(bp, open('blueprint.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ch', len(ch), 'tracks', [(t['gk'], len(t['stops'])) for t in tracks], 'issues', len(issues), 'index', len(issue_index))
