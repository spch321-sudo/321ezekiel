import sys,re
from playwright.sync_api import sync_playwright
errs=[]; han=re.compile(r'[一-鿿]'); hanhits=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':900})
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)[:200]))
    pg.on('console',lambda m:errs.append('CONSOLE '+m.text[:200]) if m.type=='error' and 'Failed to load' not in m.text else None)
    pg.goto('http://localhost:8765/en.html'); pg.wait_for_timeout(2500)
    for t in ('I will preach','I lead a group','I read'):
        if pg.get_by_text(t).count():
            try: pg.get_by_text(t).first.click(timeout=800)
            except Exception: pass
    pg.wait_for_timeout(400)
    seen=[]
    def snap(label):
        t=pg.inner_text('body').replace('繁','').replace('简',''); seen.append((label,len(t)))
        m=han.search(t)
        if m: hanhits.append((label,t[max(0,m.start()-30):m.start()+30]))
    print(pg.evaluate("document.documentElement.lang"), pg.title())
    for tab in ('Text','Course','Tools','Me','Today'):
        loc=pg.locator('nav button, .tabbar button, button').filter(has_text=tab)
        if loc.count():
            try: loc.last.click(timeout=800); pg.wait_for_timeout(300); snap('tab '+tab)
            except Exception as e: errs.append('tab '+tab)
        else: errs.append('no tab '+tab)
    for ch in (1,2,8,11,16,18,24,28,34,36,37,38,43,47,48):
        pg.evaluate(f"go('course',{ch})"); pg.wait_for_timeout(250); snap(f'course {ch}')
        btns=pg.locator('.subtabs button, .tabs button, .seg button')
        n=btns.count()
        for i in range(n):
            try: btns.nth(i).click(timeout=600); pg.wait_for_timeout(100); snap(f'  {ch}/sub{i}')
            except Exception: pass
    for sub in ('search','tracks','issues','map','review','safeall'):
        pg.evaluate(f"go('tools',0,'{sub}')"); pg.wait_for_timeout(400); snap('tool '+sub)
    for ch in (1,28,48):
        pg.evaluate(f"go('text',{ch})"); pg.wait_for_timeout(300); snap(f'text {ch}')
    print('頁數',len(seen),'短頁',[s for s in seen if s[1]<300][:6])
    print('Han hits',hanhits[:8]); print('ERRS',errs[:12])
    b.close()
