# -*- coding: utf-8 -*-
"""WEB 經文查詢。用法：python3 scripts/web.py "Ezek 37:14" 或 "Matt 5:3-5"；模組用 web.get(book,ch,v)"""
import json,re,sys,os,functools
D='/home/claude/work/web/json/'
NAMES={'gen':'genesis','exod':'exodus','ex':'exodus','lev':'leviticus','num':'numbers','deut':'deuteronomy','josh':'joshua','judg':'judges','ruth':'ruth','1sam':'1samuel','2sam':'2samuel','1kgs':'1kings','2kgs':'2kings','1chr':'1chronicles','2chr':'2chronicles','ezra':'ezra','neh':'nehemiah','esth':'esther','job':'job','ps':'psalms','prov':'proverbs','eccl':'ecclesiastes','song':'songofsolomon','isa':'isaiah','jer':'jeremiah','lam':'lamentations','ezek':'ezekiel','dan':'daniel','hos':'hosea','joel':'joel','amos':'amos','obad':'obadiah','jonah':'jonah','mic':'micah','nah':'nahum','hab':'habakkuk','zeph':'zephaniah','hag':'haggai','zech':'zechariah','mal':'malachi','matt':'matthew','mark':'mark','luke':'luke','john':'john','acts':'acts','rom':'romans','1cor':'1corinthians','2cor':'2corinthians','gal':'galatians','eph':'ephesians','phil':'philippians','col':'colossians','1thess':'1thessalonians','2thess':'2thessalonians','1tim':'1timothy','2tim':'2timothy','titus':'titus','phlm':'philemon','heb':'hebrews','jas':'james','1pet':'1peter','2pet':'2peter','1john':'1john','2john':'2john','3john':'3john','jude':'jude','rev':'revelation'}
@functools.lru_cache(None)
def book(b):
    b=NAMES.get(b.lower().replace(' ','').replace('.',''),b.lower())
    d=json.load(open(D+b+'.json')); out={}
    for x in d:
        if x.get('type') in ('paragraph text','line text') and 'verseNumber' in x:
            k=(x['chapterNumber'],x['verseNumber']); out[k]=out.get(k,'')+x['value']
    return {k:re.sub(r'\s+',' ',v).strip() for k,v in out.items()}
def get(b,c,v): return book(b).get((c,v))
def main(q):
    m=re.match(r'(\d?\s?[A-Za-z]+)\.?\s+(\d+):(\d+)(?:-(\d+))?$',q.strip())
    if not m: print('格式：Ezek 37:14 或 Matt 5:3-5'); return
    b,c,v1,v2=m.group(1).replace(' ',''),int(m.group(2)),int(m.group(3)),int(m.group(4) or m.group(3))
    for v in range(v1,v2+1): print(f'{c}:{v}',get(b,c,v))
if __name__=='__main__':
    for q in sys.argv[1:]: main(q)
