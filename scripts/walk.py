import sys,re
from playwright.sync_api import sync_playwright
name=sys.argv[1] if len(sys.argv)>1 else 'index.html'
errs=[]; han=re.compile(r'[一-鿿]')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':900})
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)[:200]))
    pg.on('console',lambda m:errs.append('CONSOLE '+m.text[:200]) if m.type=='error' and 'Failed to load' not in m.text else None)
    pg.goto('http://localhost:8765/'+name); pg.wait_for_timeout(2500)
    pg.get_by_text('我要講道').first.click() if pg.get_by_text('我要講道').count() else None
    pg.wait_for_timeout(500)
    def body(): return pg.inner_text('body')
    seen=[]
    def snap(label):
        t=body(); seen.append((label,len(t)))
    for tab in ('經文','課程','工具','我的','今日'):
        pg.locator('nav button, .tabbar button, button').filter(has_text=tab).last.click(); pg.wait_for_timeout(300); snap('tab '+tab)
    for ch in (1,2,8,18,24,28,34,37,38,43,47,48):
        pg.evaluate(f"go('course',{ch})"); pg.wait_for_timeout(250); snap(f'course {ch}')
        for t in ('卡片','核心','小組','講章','講義','操練','把關'):
            loc=pg.get_by_text(t,exact=True)
            if loc.count():
                try: loc.first.click(timeout=800); pg.wait_for_timeout(120); snap(f'  {ch}/{t}')
                except Exception as e: errs.append(f'click {ch}/{t} {str(e)[:60]}')
            else: errs.append(f'缺分頁 {ch}/{t}')
    for sub in ('search','tracks','issues','map','review','safeall'):
        pg.evaluate(f"go('tools',0,'{sub}')"); pg.wait_for_timeout(400); snap('tool '+sub)
    pg.evaluate("go('text',37)"); snap('text 37')
    print([s for s in seen if s[1]<300])
    print('頁數',len(seen),'ERRS',errs[:12])
    b.close()
