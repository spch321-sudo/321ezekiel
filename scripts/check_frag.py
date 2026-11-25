# -*- coding: utf-8 -*-
"""單章片段校驗。用法：check_frag.py blk|serm|ch NN [NN...]；通過印「✓ 通過」。"""
import json, sys, re
from pathlib import Path
sys.path.insert(0, 'ref/skill/scripts')
import validate_volume as V
stage = sys.argv[1]; ns = [int(x) for x in sys.argv[2:]]
VC=[28,10,27,17,17,14,27,18,11,22,25,28,23,23,8,63,24,32,14,49,32,31,49,27,17,21,36,26,21,26,18,32,33,31,15,38,28,23,29,49,26,20,27,31,25,24,23,35]
bp = json.load(open('blueprint.json', encoding='utf-8'))
rc = 0
for n in ns:
    V.errs.clear(); V.warns.clear(); extra = []
    f = Path(f'{stage}/{n:02d}.json')
    if not f.exists(): print(n, '缺檔'); rc = 1; continue
    o = json.loads(f.read_text(encoding='utf-8')); T = json.load(open(f'txt/{n:02d}.json', encoding='utf-8'))
    if stage == 'blk':
        V.check_blk(o, n)
        prev = 0
        for b in o:
            if b['a'] != prev + 1: extra.append(f'blk 節號不連續 {prev}→{b["a"]}')
            prev = b['z']
        if prev != VC[n-1]: extra.append(f'blk 未涵蓋全章 止於 {prev}/{VC[n-1]}')
        for b in o:
            if b['grk'].strip() and not re.search(r'[ְ-ֽ]', b['grk']): extra.append(f'blk {b["a"]} 原文無母音點')
            if re.search(r'\bG\d+\b', b['key']): extra.append(f'blk {b["a"]} 舊約字義表出現 G 前綴')
            for fld in ('exp','gram'):
                if re.search(r'推羅', b[fld]): extra.append(f'blk {b["a"]} 用了「推羅」（應為泰爾）')
    elif stage == 'serm':
        # 合併藍圖的 pts
        s = o; exp = bp['ch'][str(n)]['serm']['pts']
        V.check_serm(s, n)
        if s.get('pts') != exp: extra.append('serm.pts 與藍圖不一致（不可改動）')
        txtall = ''.join(T)
        for b in s['blocks']:
            if b[0] == 'q' and b[1].startswith('「') and b[1].endswith('」') and len(b[1]) > 12:
                inner = b[1].strip('「」')
                if re.fullmatch(r'[^，。；！？]*', inner) and inner not in txtall and '經文' in b[1]: pass
    elif stage == 'ch':
        c = o['ch']; V.check_ch(c, f'ch[{n}]')
        if c['n'] != n: extra.append('n 不符')
        for k in ('t','sub','lv','arc','sec'):
            if c[k] != bp['ch'][str(n)][k]: extra.append(f'{k} 與藍圖不一致（不可改動）')
        if c['serm'].get('pts') != bp['ch'][str(n)]['serm']['pts']: extra.append('serm.pts 與藍圖不一致')
        lv = c['lv']; lo, hi = {'A': (12, 16), 'B': (9, 12), 'C': (7, 9)}[lv]
        sf = [x for x in c['safe'] if '檢驗標準' in x]
        if not lo <= len(c['safe']) <= hi * 1 and not lo <= len(sf) <= hi: extra.append(f'safe 條數 {len(c["safe"])} 不在 {lo}–{hi}')
        mvt = c['mv']['t']
        if mvt not in ''.join(T).replace('「','').replace('」','') and mvt.replace('「','').replace('」','') not in ''.join(T).replace('「','').replace('」',''): extra.append('mv.t 不是和合本逐字')
        iss = o['issues']; V.check_issues(iss)
        if not 4 <= len(iss) <= 9: extra.append(f'議題 {len(iss)} 條（4–9）')
        for i in iss:
            if i['ch'][0] != n or not i['id'].startswith(f'ISS{n:02d}_'): extra.append(f'{i["id"]} 歸屬/編號錯')
            if not i['care'].strip(): extra.append(f'{i["id"]} care 空')
    for e in V.errs + extra: print(n, e)
    for w in V.warns: print(n, w)
    if V.errs or extra: rc = 1
    else: print(n, '✓ 通過', f'(提醒 {len(V.warns)})')
sys.exit(rc)
