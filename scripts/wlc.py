#!/usr/bin/env python3
"""WLC (OpenScriptures morphhb) Ezekiel: 逐節詞表與詞根計數。"""
import re, sys, json, collections
import xml.etree.ElementTree as ET
NS = {'o': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
def load(path):
    root = ET.parse(path).getroot()
    verses = {}
    for v in root.iter('{%s}verse' % NS['o']):
        oid = v.get('osisID')
        if not oid or not oid.startswith('Ezek.'): continue
        _, c, n = oid.split('.')
        words = []
        for w in v.iter('{%s}w' % NS['o']):
            lem = (w.get('lemma') or '')
            nums = re.findall(r'(\d+)', lem)
            words.append((''.join(w.itertext()), lem, w.get('morph') or '', nums))
        verses[(int(c), int(n))] = words
    return verses
if __name__ == '__main__':
    v = load('/home/claude/work/morphhb/wlc/Ezek.xml')
    print(len(v), 'verses')
    cnt = collections.Counter()
    for k, ws in v.items():
        for t, lem, m, nums in ws:
            for n in nums: cnt[n] += 1
    for n in ['3045','3519','7307','120','1121','3820','3824','7462','6822','6680','8451']:
        print(n, cnt[n])
