# -*- coding: utf-8 -*-
"""教學講章單課校驗。lesson/NN.json = {"title": "章題——副題", "blocks": [...]}（blocks 格式同 DATA.lesson）。
用法：check_lesson.py NN [NN...] ；通過印「✓ 通過」。--stats 時印字數。"""
import json, re, sys
bp = json.load(open('blueprint.json', encoding='utf-8'))
def han(s): return len(re.findall(r'[一-鿿]', s))
def check(n):
    e = []; w = []
    o = json.load(open(f'lesson/{n:02d}.json', encoding='utf-8')); T = ''.join(json.load(open(f'txt/{n:02d}.json', encoding='utf-8')))
    Tn = re.sub(r'[「」『』，。；：、！？\s（）－—]', '', T)
    c = bp['ch'][str(n)]
    if set(o) != {'title', 'blocks'}: e.append(f'欄位應只有 title/blocks：{sorted(o)}')
    exp_title = f'{c["t"]}——{c["sub"]}'
    if o['title'] != exp_title: e.append(f'title 應為「{exp_title}」')
    B = o['blocks']
    for i, b in enumerate(B):
        if b[0] not in 'hpdsmtn' or len(b[0]) != 1: e.append(f'block {i} 類型 {b[0]}'); 
    hs = [(i, b[1]) for i, b in enumerate(B) if b[0] == 'h']
    nums = '一二三四五六七八九十'
    if len(hs) != 11: e.append(f'h 應 11 個，實 {len(hs)}'); return e, w, {}
    for k, (i, t) in enumerate(hs):
        lab = (nums[k] if k < 10 else '十一')
        if not t.startswith(lab + '、'): e.append(f'第{k+1}個 h 應以「{lab}、」起頭：{t}')
    if not any('原文' in t for _, t in hs[:4]): e.append('一～四節須有一節標題含「原文」')
    for k in range(4):
        if not re.search(r'\d+[:：]?\d*[–\-]\d+|\d+:\d+|\d+章', hs[k][1]) and not re.search(r'\d', hs[k][1]): w.append(f'第{k+1}節標題宜標經文範圍')
    fixed = {4: '五、幾個必須認得的偏差', 5: '六、兩個華人處境的真實問題', 9: '十、結語', 10: '十一、小組討論分享：三個化'}
    for k, t in fixed.items():
        if hs[k][1] != t: e.append(f'h{k+1} 標題應為「{t}」：{hs[k][1]}')
    if not hs[6][1].startswith('七、活出321——'): e.append('七 標題應為「七、活出321——副題」')
    if not hs[7][1].startswith('八、四種心，'): e.append('八 標題應為「八、四種心，副題」')
    if not hs[8][1].startswith('九、這一週，你可以做的幾件事'): e.append('九 標題錯')
    ends = [h[0] for h in hs] + [len(B)]
    def sec(k): return B[ends[k]+1:ends[k+1]]
    ps = lambda k: [b[1] for b in sec(k) if b[0] == 'p']
    p0 = ps(0)
    if not p0 or not p0[0].startswith('弟兄姊妹平安'): e.append('第一節第一段須以「弟兄姊妹平安」起頭')
    p5 = ps(4)
    if len(p5) != 5 or any(not p5[i].startswith(f'第{"一二三四五"[i]}個') for i in range(len(p5))): e.append('五：須剛好 5 段，依序以「第一個」…「第五個」起頭')
    p6 = ps(5)
    if len(p6) != 2 or not (p6[0].startswith('第一個問題') and p6[1].startswith('第二個問題')): e.append('六：須剛好 2 段，以「第一個問題」「第二個問題」起頭')
    p7 = '\n'.join(ps(6))
    for kw in ('耶穌是我的榜樣', '聖經是我的準則', '聖靈是我的引導', '讓耶穌作王', '一切的榮耀', '屬神的體系'):
        if kw not in p7: e.append(f'七：缺「{kw}」')
    p8 = ps(7)
    if len(p8) != 4 or not all(k in p8[i][:12] for i, k in enumerate(['驕傲', '恐懼', '羞恥', '受傷'])): e.append('八：須 4 段，依序驕傲型／恐懼型／羞恥型／受傷型（段首 12 字內含該詞）')
    p9 = ps(8)
    if len(p9) != 9 or any(not p9[i].startswith(f'第{"一二三四五"[i]}，') for i in range(5)) or any(not p9[i].startswith('我宣告') for i in range(5, 9)): e.append('九：須 5 件事（「第一，」…「第五，」）＋4 句「我宣告」共 9 段')
    p10 = ps(9)
    if not p10 or not p10[-1].endswith('奉主耶穌基督的名禱告，阿們。'): e.append('十：末句須為「……奉主耶穌基督的名禱告，阿們。」')
    if len(p10) < 2 or '焦點' not in p10[-2]: e.append('十：倒數第二段須出現「焦點」')
    # 想更深
    ds = [(k, b[1]) for k in range(11) for b in sec(k) if b[0] == 'd']
    if len(ds) != 8: e.append(f'想更深應 8 則，實 {len(ds)}')
    if len({k for k, _ in ds if k < 10}) < 5: e.append('想更深須分散在至少五節')
    for k, d in ds:
        if not (isinstance(d, list) and len(d) == 2): e.append('d 格式 [問, 答]'); continue
        if not d[0].endswith('？') or han(d[0]) < 10: e.append(f'想更深問句須「？」收且≥10 漢字：{d[0][:20]}')
        if not 150 <= han(d[1]) <= 460: e.append(f'想更深回答 {han(d[1])} 漢字（150–460）：{d[0][:14]}')
    # 三個化
    H = sec(10)
    if [b[1] for b in H if b[0] == 's'] != ['第一化　內化（約20分鐘）', '第二化　消化（約35分鐘·主軸）', '第三化　轉化（約25分鐘）', '收尾（5分鐘）']: e.append('十一：s 標題四段須為 第一化　內化（約20分鐘）／第二化　消化（約35分鐘·主軸）／第三化　轉化（約25分鐘）／收尾（5分鐘）')
    qs = [b[1] for b in H if b[0] == 'n']
    if len(qs) != 14: e.append(f'題目應 14 題，實 {len(qs)}')
    for i, q in enumerate(qs, 1):
        if not re.match(rf'{i}\. (★{{1,3}}) ', q): e.append(f'題號/星級格式錯：{q[:12]}')
    groups = []; cur = None
    for b in H:
        if b[0] == 's': cur = [b[1], []]; groups.append(cur)
        elif b[0] == 'n' and cur: cur[1].append(b[1])
    if len(groups) == 4:
        for g in groups[:3]:
            if len(g[1]) < 3 or not any('★★★' in q for q in g[1]): e.append(f'{g[0][:3]} 須≥3 題且含 ★★★')
        ts = [b[1] for b in H if b[0] == 't']
        if ts != ['【看】看見自己', '【聽】聽神說話', '【想】想通關卡', '【講】說出口', '【行】走一步']: e.append('第二化 t 五步須為【看】看見自己／【聽】聽神說話／【想】想通關卡／【講】說出口／【行】走一步')
        if not any('920' in q for q in groups[2][1]): e.append('第三化須有 920 操練題')
        if '【必做】' not in groups[2][1][-1]: e.append('第三化最後一題須含【必做】')
        for gi in range(3):
            ms = []; on = False
            for b in H:
                if b[0] == 's': on = b[1] == groups[gi][0]
                elif on and b[0] == 'm': ms.append(b[1])
            if not any(m.startswith('目的') for m in ms): e.append(f'{groups[gi][0][:3]} 缺「目的：」m')
            if not any(m.startswith('帶領提醒') for m in ms): e.append(f'{groups[gi][0][:3]} 缺「帶領提醒：」m')
    if len([b for b in H if b[0] == 'p']) < 1: e.append('收尾須有 p')
    # 字數
    body = sum(han(b[1]) for k in range(10) for b in sec(k) if b[0] == 'p') + sum(han(h[1]) for h in hs[:10])
    dch = sum(han(d[0]) + han(d[1]) for _, d in ds if isinstance(d, list))
    hua = sum(han(b[1]) for b in H if isinstance(b[1], str))
    tot = body + dch + hua
    if not 4700 <= body <= 5700: e.append(f'講章本體 {body} 漢字（4,700–5,700）')
    if not 7200 <= tot <= 8400: e.append(f'全課 {tot} 漢字（7,200–8,400）')
    # 經文引用警示：「…」≥10字 應見於本章
    for b in B:
        txt = b[1] if isinstance(b[1], str) else ''.join(x for x in b[1] if isinstance(x, str)) if isinstance(b[1], list) else ''
        for m in re.findall(r'「([^」]{10,})」', txt):
            mm = re.sub(r'[「」『』，。；：、！？\s（）－—]', '', m)
            if mm not in Tn: w.append(f'引句不在本章和合本（若引他章請確認逐字）：{m[:22]}')
    if '推羅' in json.dumps(o, ensure_ascii=False): e.append('用了「推羅」（應為泰爾）')
    return e, w, dict(body=body, dch=dch, hua=hua, tot=tot)
if __name__ == '__main__':
    rc = 0
    for a in sys.argv[1:]:
        n = int(a)
        try: e, w, st = check(n)
        except FileNotFoundError: print(n, '缺檔'); rc = 1; continue
        for x in e: print(n, '✗', x)
        for x in w[:6]: print(n, '提醒', x)
        if e: rc = 1
        else: print(n, '✓ 通過', st)
    sys.exit(rc)
