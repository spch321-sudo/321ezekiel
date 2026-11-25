# -*- coding: utf-8 -*-
import json, re, sys
sys.path.insert(0, 'scripts')
import wlc
VC=[28,10,27,17,17,14,27,18,11,22,25,28,23,23,8,63,24,32,14,49,32,31,49,27,17,21,36,26,21,26,18,32,33,31,15,38,28,23,29,49,26,20,27,31,25,24,23,35]
R = re.compile(r'^(\d+):(\d+)--(\d+)$')
def rg(s, n, err):
    m = R.match(s)
    if not m or int(m[1]) != n: err.append(f'{n} 範圍格式錯 {s}'); return None
    return int(m[2]), int(m[3])
def check(bp, txtdir='txt', W=None):
    err = []
    T = {n: json.load(open(f'{txtdir}/{n:02d}.json', encoding='utf-8')) for n in range(1, 49)}
    if sorted(bp['ch'], key=int) != [str(i) for i in range(1, 49)]: err.append('章鍵不全')
    for k, c in bp['ch'].items():
        n = int(k); V = VC[n-1]
        if c['n'] != n: err.append(f'{n} n 不符')
        if len(c['sub'].split('、')) != 3: err.append(f'{n} sub 不是三詞')
        if c['lv'] not in 'ABC': err.append(f'{n} lv')
        if not 4 <= len(c['sec']) <= 7: err.append(f'{n} sec 數量')
        if len(c['serm']['pts']) != 3: err.append(f'{n} pts 數量')
        for name, lst in (('sec', c['sec']), ('pts', [[None, r] for r in [p[1] for p in c['serm']['pts']]])):
            prev = 0
            for item in lst:
                r = rg(item[1] if name == 'pts' else item[0], n, err)
                if not r: continue
                a, z = r
                if a != prev + 1 or z < a: err.append(f'{n} {name} 不連續於 {a}--{z}')
                prev = z
            if prev != V: err.append(f'{n} {name} 未涵蓋全章（止於 {prev}/{V}）')
        for p, r_, q in c['serm']['pts']:
            r = rg(r_, n, err)
            if r and q not in ''.join(T[n][r[0]-1:r[1]]): err.append(f'{n} 引句不在 {r_}：{q}')
    for t in bp['tracks']:
        if not 8 <= len(t['stops']) <= 11: err.append(f"{t['gk']} 停靠點數")
        keys = {'יָדַע':['3045'],'כָּבוֹד':['3519'],'רוּחַ':['7307'],'לֵב':['3820','3824'],'חָיָה':['2421']}[t['gk']]
        for ref, txt, pos in t['stops']:
            c, v = map(int, ref.split(':'))
            m = re.match(r'「(.+?)」', txt)
            if not m or m[1] not in T[c][v-1]: err.append(f"{t['gk']} {ref} 引句不符")
            if W and not any(any(s in keys for s in w[3]) for w in W[(c, v)]): err.append(f"{t['gk']} {ref} 原文無此字")
        if t['n'] < 8: err.append(f"{t['gk']} 次數不足")
    if len(bp['issues']) != 8: err.append('ISS00 不是八條')
    for i in bp['issues']:
        for f in ('id','t','r','ch','why','pos','con','say','care'):
            if f not in i or i[f] in ('', None): 
                if f != 'con': err.append(f"{i.get('id')} 缺 {f}")
        if i['con'] != []: err.append(f"{i['id']} con 非空")
        if len(i['pos']) < 2: err.append(f"{i['id']} pos 少於兩個")
    if not 10 <= len(bp['terrain']['points']) <= 14: err.append('terrain 點數')
    return err
if __name__ == '__main__':
    bp = json.load(open('blueprint.json', encoding='utf-8'))
    W = wlc.load('/home/claude/work/morphhb/wlc/Ezek.xml')
    e = check(bp, W=W)
    print('\n'.join(e) if e else '✓ 通過'); sys.exit(1 if e else 0)
