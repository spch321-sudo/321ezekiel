# -*- coding: utf-8 -*-
"""移植 Jeremiah 英文外殼 → Ezekiel（en.html 的外殼）。每項替換斷言找到。"""
import json,re
R='/home/claude/work/'
shell=open(R+'jer_en_shell.html',encoding='utf-8').read()
def sub(old,new,cnt=None,regex=False):
    global shell
    c=len(re.findall(old,shell,re.S)) if regex else shell.count(old)
    assert c>0 and (cnt is None or c==cnt),f'替換失敗 {old[:50]!r} 找到{c}'
    shell=re.sub(old,lambda m:new,shell,flags=re.S) if regex else shell.replace(old,new)
    print('✓',c,old[:40].replace('\n',' '))
ARCS=[["Call",1,3,"Call: glory comes to the land of exile — the vision by the Chebar, the son of man stands up, the watchman and the tongue stuck to the roof of the mouth"],
["Siege",4,7,"Siege: the siege and the end — Jerusalem on a brick, the shaved head and the three parts, prophesy to the mountains, the end has come"],
["Departure",8,11,"Departure: abominations in the temple and the departure of glory — the dark rooms in the temple, the mark on the forehead, glory leaves the threshold, the promise of a new heart"],
["Hope",12,19,"Hope: false hope and personal responsibility — the exile’s baggage, false prophets and the whitewashed wall, idols in the heart, the soul who sins shall die, turn and live"],
["Charge",20,24,"Charge: the charge from history and the end of the city — for the sake of my name, the sword drawn, standing in the breach, the boiling pot, the death of the prophet’s wife"],
["Nations",25,32,"Nations: the nations — the neighbors’ gloating, the walls of Tyre and the king of Tyre, Egypt, the nations in the pit"],
["Life",33,39,"Life: new life and hope — the watchman sent again, God himself the shepherd, a new heart and a new spirit, the dry bones live, the coming of Gog"],
["Return",40,48,"Return: the new temple and the return of glory — the man with the measuring rod, glory fills the house, the river from under the threshold, Yahweh Is There"]]
sub(r'const ARCS = \[.*?\];   /\* eight movements','const ARCS = '+json.dumps(ARCS,ensure_ascii=False)+';   /* eight movements',1,True)
sub("const LASTCH = 52;","const LASTCH = 48;",1)
sub("const KEY = 'r321.jer.v1.en';","const KEY = 'r321.ezk.v1.en';",1)
sub("K='r321.jer.v1'","K='r321.ezk.v1'")
sub("app: 'jer', pfx: 'xz-jer-'","app: 'ezk', pfx: 'xz-ezk-'",1)
sub('window.GX_BOOK = {"zh": "耶利米書", "en": "Jeremiah", "slug": "jer"};','window.GX_BOOK = {"zh": "以西結書", "en": "Ezekiel", "slug": "ezk"};',1)
sub("app: 'jer-en',","app: 'ezk-en',",1)
sub("(EN ? 'jer' : '321-Jeremiah')","(EN ? 'ezk' : '321-Ezekiel')",1)
sub("(EN ? 'jer-' : '321-Jeremiah-')","(EN ? 'ezk-' : '321-Ezekiel-')",2)
sub('fifty-two','forty-eight'); sub('1,364','1,273')
sub("const BOOK = T('耶利米書', 'Jeremiah');","const BOOK = T('以西結書', 'Ezekiel');",1)
sub("const chLabel = n => T('耶利米書' + n + '章', 'Jeremiah ' + n);","const chLabel = n => T('以西結書' + n + '章', 'Ezekiel ' + n);",1)
# map
MAPH='''    <div class="card"><p style="margin:0 0 10px"><b>Call</b> (1–3)　<b>1:28</b> the appearance of the glory of Yahweh　→　<b>2:2</b> the Spirit entered me　→　<b>3:17</b> I have made you a watchman</p>
    <p style="margin:0 0 10px"><b>Siege</b> (4–7)　<b>4:1</b> Jerusalem on a brick　→　<b>5:5</b> this is Jerusalem　→　<b>7:2</b> the end has come</p>
    <p style="margin:0 0 10px"><b>Departure</b> (8–11)　<b>8:3</b> he took me by a lock of my hair　→　<b>9:4</b> a mark on the foreheads　→　<b>10:18</b> the glory departs from the threshold　→　<b>11:19</b> a heart of flesh</p>
    <p style="margin:0 0 10px"><b>Hope</b> (12–19)　<b>13:10</b> whitewash on a flimsy wall　→　<b>16:6</b> live　→　<b>18:23</b> do I have any pleasure in the death of the wicked?　→　<b>18:32</b> turn, and live</p>
    <p style="margin:0 0 10px"><b>Charge</b> (20–24)　<b>20:9</b> for the sake of my name　→　<b>22:30</b> stand in the breach　→　<b>24:16</b> the desire of your eyes taken away</p>
    <p style="margin:0 0 10px"><b>Nations</b> (25–32)　<b>28:2</b> your heart is proud, and you say, “I am a god”　→　<b>29:6</b> they will know that I am Yahweh　→　<b>32:27</b> the mighty who went down to Sheol</p>
    <p style="margin:0 0 10px"><b>Life</b> (33–39)　<b>33:11</b> turn back; why will you die?　→　<b>34:15</b> I myself will be the shepherd of my sheep　→　<b>36:26</b> a new heart and a new spirit　→　<b>37:14</b> you shall live</p>
    <p style="margin:0"><b>Return</b> (40–48)　<b>43:5</b> the glory of Yahweh filled the house　→　<b>47:9</b> everything will live　→　<b>48:35</b> Yahweh Is There</p></div>
    <div class="card"><p class="eyebrow">The book’s axis · six turning points</p>
    <table><tr><th>Turning point</th><th>Text</th></tr>
    <tr><td><b>① Glory comes to the land of exile: the heavens opened, and I saw visions of God</b></td><td>1:1; 1:28</td></tr><tr><td><b>② The glory departs: the temple abandoned, the city judged</b></td><td>8:3; 10:18; 11:23</td></tr><tr><td><b>③ The watchman and the individual: the one who sins shall die; the one who turns shall live</b></td><td>3:17; 18:32; 33:7</td></tr><tr><td><b>④ God himself as shepherd: he seeks, brings out and feeds</b></td><td>34:11; 34:15</td></tr><tr><td><b>⑤ A new heart and spirit, and the dry bones: you shall live</b></td><td>36:26–27; 37:14</td></tr><tr><td><b>⑥ The glory returns: the temple, the river, and Yahweh Is There</b></td><td>43:5; 47:9; 48:35</td></tr></table></div>`;'''
sub(r'    <div class="card"><p style="margin:0 0 10px"><b>Call</b> \(chapter 1\).*?<td>32:15; 36:32</td></tr></table></div>`;',MAPH,1,True)
sub('From uprooting and tearing down, to building and planting.','From the glory departing, to Yahweh Is There.',1)
sub('In eight movements the whole book follows one line: God will uproot and tear down in order to build and plant; the prophet stands between judgment and hope and speaks through tears; and in the end God writes the new covenant on the human heart.','In eight movements the whole book follows one line: the glory of God departs, and returns; for the sake of his own name he makes people know that he is Yahweh; he himself becomes their shepherd, gives a new heart and a new spirit, makes dry bones live, and at last gives the city a name: “Yahweh Is There.”',1)
# Xiaozhi rules
lines=shell.split('\n')
def fl(s):
    k=[x for x,l in enumerate(lines) if s in l]; assert len(k)==1,(s,k); return k[0]
lines[fl("'3. Disputes are not adjudicated")]="    '3. Disputes are not adjudicated: on the vision of the new temple (chapters 40–48: literal, symbolic, or both), Gog and Magog (chapters 38–39), the king of Tyre and Satan (chapter 28), the prophet\\'s sign-acts and his silence, the arrangements for Levites and sacrifices in the new temple (chapters 44–46), and personal responsibility and the sins of the generations (chapter 18) — always state first what all sides agree on, then present the main positions, and only then the position of these notes; never adjudicate, and never make political judgments.',"
b=fl("Do not judge people, do not get entangled in politics"); c=fl("If they come about their own sin")
new=["    'Do not judge people, do not get entangled in politics, do not pass verdicts on particular churches or people. Ezekiel is not a timetable and not a footnote to modern politics — its focus is: the glory of God departs, and returns; for the sake of his own name he makes people know that he is Yahweh; he himself becomes the shepherd, gives a new heart and a new spirit, makes dry bones live, and at last gives the city a name: “Yahweh Is There.”',",
"    'The end times and prophecy: Gog and Magog (chapters 38–39) and the vision of the new temple (chapters 40–48) — do not count days, do not draw timetables, do not identify any modern nation, people or person as a fulfilment; what calls people to turn today and to trust the Lord who himself is the shepherd is the original meaning.',",
"    'The marriage and sexual imagery of chapters 16 and 23: speak first of God\\'s grief, never enlarge the picture, and never tell a wounded person \"this picture is about you\"; protect those present who have been hurt or whose marriages have broken.',",
"    'Chapter 18 (\"the soul who sins shall die\") and chapter 24 (the death of the prophet\\'s wife): never use \"personal responsibility\" to answer bereavement, suffering or what happened to a child, and never hint that suffering is because of one\\'s own sin; stay with them and listen first, then gently point to the Lord who himself is the shepherd and who makes dry bones live.',",
"    'The watchman of chapters 3 and 33: never use it to produce fear or guilt in pastors or anyone, and never require anyone to carry a burden for another\\'s salvation that they cannot carry; the watchman\\'s charge is to speak, not to guarantee the result.',",
"    'Despair and self-harm: if someone says life feels meaningless or they want to disappear, stay with them gently and take it seriously; never say \"just have faith\" and never answer with passages of judgment; encourage them to contact someone they trust and their pastor right away. In Taiwan they can call the 1925 mental-health hotline, or 119 in an emergency; elsewhere, their local crisis line and emergency number.',"]
lines[b:c]=new
shell='\n'.join(lines)
sub('[Four rules specific to Jeremiah]','[Four rules specific to Ezekiel]',1)
sub('"Jeremiah does not deal with this directly."','"Ezekiel does not deal with this directly."',1)
sub('321 Jeremiah: Exposition and Sermons','321 Ezekiel: Exposition and Sermons')
sub('321 Jeremiah Study Notes','321 Ezekiel Study Notes')
sub('Jeremiah Study Notes','Ezekiel Study Notes')
# 殘留的 Jeremiah 逐處檢視：先全換，再例外還原
keep={"jeremiah: 'Jeremiah'":"@@K1@@","Isaiah Jeremiah Lamentations":"@@K2@@"}
for k,v in keep.items(): assert k in shell; shell=shell.replace(k,v)
left=[m.start() for m in re.finditer('Jeremiah',shell)]
print('剩',len(left))
for p in left[:80]: print('  ',repr(shell[max(0,p-60):p+80]))
open('build/shell_ezk_en_pre.html','w',encoding='utf-8').write(shell)

# ---- 第二段：逐處換成 Ezekiel
shell=open('build/shell_ezk_en_pre.html',encoding='utf-8').read()
sub('n === 24 && ch >= 1 && ch <= 52','n === 26 && ch >= 1 && ch <= 48',1)
sub('r.n === 24 && r.ch >= 1 && r.ch <= 52','r.n === 26 && r.ch >= 1 && r.ch <= 48',1)
sub('"t":"Jeremiah","a":["Jer","Je"]','"t":"@@B1@@","a":["Jer","Je"]',1)
sub('["Jeremiah",24]','["@@B1@@",24]',1)
sub('Jeremiah','Ezekiel')
sub('@@B1@@','Jeremiah'); sub('@@K1@@',"jeremiah: 'Jeremiah'",1); sub('@@K2@@','Isaiah Jeremiah Lamentations',1)
sub('耶利米書','以西結書'); sub('耶利米书','以西结书')
sub("setTitle('Ecc ' + n","setTitle('Ezek ' + n",2)
sub('Twelve Lessons','Forty-Eight Lessons',1)
open('build/shell_ezk_en.html','w',encoding='utf-8').write(shell)
rest=[(m.group(0),shell[max(0,m.start()-50):m.end()+50]) for m in re.finditer(r'Jeremiah|\bjer\b|Anathoth|Baruch|Josiah|Hananiah|Septuagint|seventy years|Babylon',shell)]
print('剩',len(rest))
for r in rest: print(repr(r[1]))
