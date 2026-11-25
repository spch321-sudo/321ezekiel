# -*- coding: utf-8 -*-
"""移植 321耶利米書 外殼 → 以西結書（繁/简）。每項替換都斷言找到。"""
import json,re,hashlib,sys,os
from PIL import Image,ImageFilter
R='/home/claude/work/jer_ref/'; O='site/'
os.makedirs(O,exist_ok=True)
# ---- icons
im=Image.open('assets/cover.png').convert('RGB')
for s in (32,64,120,152,167,180,192,512,1024):
    t=im.resize((s,s),Image.LANCZOS)
    if s<=192: t=t.filter(ImageFilter.UnsharpMask(radius=1,percent=60,threshold=2))
    t.save(f'{O}icon-{s}.png')
im.resize((64,64),Image.LANCZOS).save(O+'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
for f in ('coread.js','peerjs.min.js','xz2.js','404.html'):
    open(O+f,'wb').write(open(R+f,'rb').read())
# ---- shell
h=open(R+'index.html',encoding='utf-8').read()
i=h.find('<script id="DATA"');j=h.find('</script>',i)
head,tail=h[:i],h[j:]
shell=head+'@@DATA@@'+tail
n_ok=0
def sub(old,new,cnt=None,regex=False):
    global shell
    c=len(re.findall(old,shell,re.S)) if regex else shell.count(old)
    assert c>0 and (cnt is None or c==cnt),f'替換失敗 {old[:40]!r} 找到{c}'
    shell=re.sub(old,lambda m:new,shell,flags=re.S) if regex else shell.replace(old,new)
    print('✓',c,old[:30].replace('\n',' '))
# arcs
ARCS=[["召",1,3,"召：榮耀臨到被擄之地——迦巴魯河邊的異象，人子站起來，守望者與口舌貼住上膛"],
["圍",4,7,"圍：圍困與結局——磚上的耶路撒冷，剃頭髮與三分，對山說預言，結局到了"],
["離",8,11,"離：殿中的穢行與榮耀離去——殿中的暗室，額上的記號，榮耀離開殿，新心的應許"],
["望",12,19,"望：假盼望與個人的責任——流亡的行裝，假先知與抹灰的牆，偶像在心裡，犯罪的必死，回頭而存活"],
["控",20,24,"控：歷史的控訴與城的結局——為我名的緣故，刀出了鞘，站在破口，煮肉的鍋，妻子之死"],
["列",25,32,"列：列國——四鄰的幸災樂禍，泰爾的城牆與泰爾王，埃及，陰府的列國"],
["生",33,39,"生：重生與盼望——守望者再受差遣，親自作牧人，新心新靈，枯骨復活，歌革的來臨"],
["歸",40,48,"歸：新殿與榮耀歸回——度量的人，榮耀充滿了殿，殿下流出的水，耶和華的所在"]]
sub(r'const ARCS = \[.*?\];   /\* 八段','const ARCS = '+json.dumps(ARCS,ensure_ascii=False)+';   /* 八段',1,True)
sub("const LASTCH = 52;","const LASTCH = 48;",1)
sub("const KEY = 'r321.jer.v1';","const KEY = 'r321.ezk.v1';",1)
sub("K='r321.jer.v1'","K='r321.ezk.v1'") if "K='r321.jer.v1'" in shell else None
sub("app: 'jer', pfx: 'xz-jer-'","app: 'ezk', pfx: 'xz-ezk-'",1)
sub('window.GX_BOOK = {"zh": "耶利米書", "en": "Jeremiah", "slug": "jer"};','window.GX_BOOK = {"zh": "以西結書", "en": "Ezekiel", "slug": "ezk"};',1)
sub("'Currently reading: Jeremiah '","'Currently reading: Ezekiel '",1)
sub('1,364','1,273')
sub('五十二','四十八')
# 地形圖
MAPH=("""    <div class="card"><p style="margin:0 0 10px"><b>召</b>（1–3 章）　<b>1:28</b> 耶和華榮耀的形像　→　<b>2:2</b> 靈就進入我裡面　→　<b>3:17</b> 立你作守望的人</p>
    <p style="margin:0 0 10px"><b>圍</b>（4–7 章）　<b>4:1</b> 磚上的耶路撒冷　→　<b>5:5</b> 這就是耶路撒冷　→　<b>7:2</b> 結局到了</p>
    <p style="margin:0 0 10px"><b>離</b>（8–11 章）　<b>8:3</b> 抓住我的一綹頭髮　→　<b>9:4</b> 畫記號在額上　→　<b>10:18</b> 榮耀從殿的門檻出去　→　<b>11:19</b> 賜給他們肉心</p>
    <p style="margin:0 0 10px"><b>望</b>（12–19 章）　<b>13:10</b> 未泡透的灰抹牆　→　<b>16:6</b> 仍可存活　→　<b>18:23</b> 豈是我喜悅的嗎　→　<b>18:32</b> 回頭而存活</p>
    <p style="margin:0 0 10px"><b>控</b>（20–24 章）　<b>20:9</b> 為我名的緣故　→　<b>22:30</b> 站在破口　→　<b>24:16</b> 眼目所喜愛的忽然取去</p>
    <p style="margin:0 0 10px"><b>列</b>（25–32 章）　<b>28:2</b> 心裡高傲，說我是神　→　<b>29:6</b> 就知道我是耶和華　→　<b>32:27</b> 下到陰間的勇士</p>
    <p style="margin:0 0 10px"><b>生</b>（33–39 章）　<b>33:11</b> 轉回吧，何必死亡　→　<b>34:15</b> 我必親自作我羊的牧人　→　<b>36:26</b> 新心新靈　→　<b>37:14</b> 你們就要活了</p>
    <p style="margin:0"><b>歸</b>（40–48 章）　<b>43:5</b> 榮光充滿了殿　→　<b>47:9</b> 百物都必生活　→　<b>48:35</b> 耶和華的所在</p></div>
    <div class="card"><p class="eyebrow">全卷主軸 · 六個轉折</p>
    <table><tr><th>轉折</th><th>經文</th></tr>
    <tr><td><b>① 榮耀臨到被擄之地：天開了，看見神的異象</b></td><td>1:1；1:28</td></tr><tr><td><b>② 榮耀離開：殿被丟棄，城被審判</b></td><td>8:3；10:18；11:23</td></tr><tr><td><b>③ 守望與個人：犯罪的必死，回頭的存活</b></td><td>3:17；18:32；33:7</td></tr><tr><td><b>④ 親自作牧人：祂親自尋找、領出、牧養</b></td><td>34:11；34:15</td></tr><tr><td><b>⑤ 新心新靈與枯骨復活：你們就要活了</b></td><td>36:26–27；37:14</td></tr><tr><td><b>⑥ 榮耀歸回：殿、河與耶和華的所在</b></td><td>43:5；47:9；48:35</td></tr></table></div>`;""")
sub(r'    <div class="card"><p style="margin:0 0 10px"><b>召</b>（1 章）.*?<td>32:15；36:32</td></tr></table></div>`;',MAPH,1,True)
sub('從拔出、拆毀，到建立、栽植。','從榮耀離開，到耶和華的所在。',1)
sub('全卷八段，一條線：神要拔出、拆毀，為要建立、栽植；先知站在審判與盼望之間含淚說話，最後神把新約寫在人心上。','全卷八段，一條線：神的榮耀離開，又歸回；祂為自己的名，叫人知道祂是耶和華；祂親自作牧人、賜新心新靈、使枯骨復活，最後以「耶和華的所在」為這城的名。',1)
sub('從「我已曉得你」，走到「寫在他們心上」','從「耶和華榮耀的形像」，走到「耶和華的所在」',1)
# 小智守則
lines=shell.split('\n')
def find_line(s):
    k=[x for x,l in enumerate(lines) if s in l]; assert len(k)==1,(s,k); return k[0]
a=find_line("'三、爭議不裁決：遇到耶利米書的成書")
lines[a]="    '三、爭議不裁決：遇到以西結書的殿的異象（四十至四十八章是字面、象徵或兩者並有）、歌革與瑪各（三十八、三十九章）、泰爾王與撒但（二十八章）、先知的象徵行動與啞口、利未人與祭祀在新殿的安排（四十四至四十六章）、個人責任與世代的罪（十八章）這幾類問題，一律先講「兩邊都同意的」，再並陳各家立場，最後才說本講義的立場；絕不裁決，也絕不作政治判斷。',"
b=find_line("不論斷人、不捲入政治、不評斷特定教會或人物。耶利米書")
c=find_line("若對方為自己的罪而來")
new=["    '不論斷人、不捲入政治、不評斷特定教會或人物。以西結書不是時間表，也不是現代政治的註腳——全卷的焦點是：神的榮耀離開，又歸回；祂為自己的名，叫人知道祂是耶和華；祂親自作牧人、賜新心新靈、使枯骨復活，最後以「耶和華的所在」為這城的名。',",
"    '末世與預言：歌革與瑪各（三十八、三十九章）與新殿的異象（四十至四十八章），不算日子、不排時間表、不指認任何現代國家、民族或人物是預言的應驗；叫人今天就回頭、就信靠那位親自作牧人的主，才是原意。',",
"    '十六章、二十三章的婚姻與性的比喻：先講神的心痛，不放大畫面，不對受傷的人說「這比喻在說你」；先保護在場曾受傷害或婚姻破碎的弟兄姊妹。',",
"    '十八章「犯罪的，他必死亡」與二十四章妻子之死：不用「個人責任」去回答喪親、受苦與孩子的遭遇，不暗示受苦是因為自己的罪；先陪伴、先聽，再慢慢指向那位親自作牧人、使枯骨復活的主。',",
"    '三章、三十三章的守望者：不用它給牧者或任何人製造恐懼與愧疚，也不要求人為他人的得救背負自己背不起的責任；守望的託付是說出話，不是保證結果。',",
"    '絕望與自傷：遇到說「活著沒意思」「想消失」的人，先溫柔陪伴、認真看待，不用經文勸他「要有信心」，也不用審判的經文回應他；鼓勵他立刻聯絡信任的人與牧者；在台灣可撥安心專線 1925，緊急狀況撥 119。',"]
lines[b:c]=new
shell='\n'.join(lines)
sub('像一位陪讀的屬靈朋友','像一位陪讀的屬靈朋友')
sub('【耶利米書專屬的四條規矩】','【以西結書專屬的四條規矩】',1)
# 名稱（長的在前）
sub('321耶利米書解經與講章','321以西結書解經與講章')
sub('321耶利米書講義','321以西結書講義')
sub('耶利米書講義','以西結書講義')
sub('耶利米書','以西結書')
sub('耶利米书','以西结书',1)
# 殘留檢查
left=re.findall(r'耶利米|Jeremiah(?! Lam)|\bjer\b(?!\|lam)|耶路撒冷哭泣|拔出、拆毀',shell.replace("isaiah: 'Isaiah', jeremiah: 'Jeremiah'",'').replace('Isaiah Jeremiah Lamentations',''))
print('殘留',left)
assert not left,left
open('build/shell_ezk.html','w',encoding='utf-8').write(shell)
