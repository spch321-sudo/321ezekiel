#!/usr/bin/env python3
"""cu89t USFM -> txt/NN.json（和合本繁體逐節，上帝→神、裏→裡、着→著）。用法: parse_usfm.py ezk.usfm txt/"""
import re, sys, json, os
src, out = sys.argv[1], sys.argv[2]
raw = open(src, encoding='utf8').read()
chapters = {}
cur = None
for line in raw.splitlines():
    line = line.rstrip()
    m = re.match(r'\\c (\d+)', line)
    if m:
        cur = int(m.group(1)); chapters[cur] = []; continue
    if cur is None: continue
    # 段落／詩行標記：去掉標記，內容照常處理（詩體每行都要收進該節）
    line = re.sub(r'^\\(p|m|q\d?|b)\b\s*', '', line)
    if line.startswith('\\v '):
        m = re.match(r'\\v (\d+)(?:-(\d+))? ?(.*)', line)
        a, b, t = int(m.group(1)), m.group(2), m.group(3)
        chapters[cur].append([a, int(b) if b else a, t])
    elif line.startswith('\\'):
        continue  # 標題、交叉引用等
    elif chapters[cur] and line:
        chapters[cur][-1][2] += line  # 詩行／續行
# 併節拆開（和合本把兩節併成一行；切點依句號／希伯來文節界核過）
SPLIT = {(16, 56): ('。', 57), (18, 10): ('乃在山上', 11), (39, 26): ('。', 27)}
def split_merged(c, vs):
    out = []
    for a, t in vs:
        if (c, a) in SPLIT:
            key, nxt = SPLIT[(c, a)]
            if key == '。':
                i = t.index('。') + 1
            else:
                i = t.index(key)
            out.append((a, t[:i])); out.append((nxt, t[i:]))
        else:
            out.append((a, t))
    return out
def clean(t):
    t = re.sub(r'\\f .*?\\f\*', '', t)
    t = re.sub(r'\\\+?(add|pn|nd|k|w)\*?', '', t)
    t = re.sub(r'\\\+?[a-z0-9]+\*?', '', t)
    t = t.replace('上帝', '神').replace('裏', '裡').replace('着', '著')
    return re.sub(r'\s+', '', t)
os.makedirs(out, exist_ok=True)
merged = []
for c in sorted(chapters):
    vs = []
    for a, b, t in chapters[c]:
        if b != a: merged.append((c, a, b))
        vs.append((a, clean(t)))
    vs = split_merged(c, vs)
    nums = [a for a, _ in vs]
    assert nums == list(range(1, len(nums) + 1)), (c, nums)
    json.dump([t for _, t in vs], open(f'{out}/{c:02d}.json', 'w', encoding='utf8'), ensure_ascii=False)
counts = [len(chapters[c]) for c in sorted(chapters)]
print('chapters', len(counts), 'verses', sum(counts))
print(counts)
print('merged lines:', merged)
