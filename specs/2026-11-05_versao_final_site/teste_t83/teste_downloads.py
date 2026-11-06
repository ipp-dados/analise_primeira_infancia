import sys, threading, functools, http.server, json
from pathlib import Path
from playwright.sync_api import sync_playwright
SITE=Path(sys.argv[1]); OUT=Path(sys.argv[2])
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(Q,directory=str(SITE))); threading.Thread(target=srv.serve_forever,daemon=True).start()
URL=f"http://127.0.0.1:{srv.server_port}/index.html"
res={"visiveis_ok":0,"ocultos_ok":0,"falhas":[],"motivo_oculto":{}}
with sync_playwright() as p:
    br=p.chromium.launch(channel="msedge"); ctx=br.new_context(accept_downloads=True,viewport={"width":1366,"height":768}); pg=ctx.new_page()
    pg.goto(URL); pg.wait_for_timeout(800)
    for tid in pg.evaluate("()=>[...document.querySelectorAll('button[role=tab]')].map(b=>b.id)"):
        pg.click(f"#{tid}"); pg.wait_for_timeout(400)
        painel=pg.evaluate(f"document.getElementById('{tid}').getAttribute('aria-controls')")
        n=pg.locator(f"#{painel} .dl-btn").count()
        for i in range(n):
            el=pg.locator(f"#{painel} .dl-btn").nth(i)
            vis=el.is_visible()
            if not vis:
                why=el.evaluate("b=>{let e=b;while(e&&e!==document.body){const s=getComputedStyle(e);if(s.display==='none'||e.hidden)return (e.className||e.tagName)+'';e=e.parentElement;}return '?'}")
                res["motivo_oculto"][why]=res["motivo_oculto"].get(why,0)+1
            try:
                with pg.expect_download(timeout=4000) as d:
                    if vis: el.scroll_into_view_if_needed(); el.click()
                    else: el.evaluate("b=>b.click()")
                pth=d.value.path(); txt=Path(pth).read_text(encoding="utf-8-sig")
                ok=len(txt)>10 and txt.count("\n")>=1 and "," in txt.splitlines()[0] or ";" in txt.splitlines()[0]
                if ok: res["visiveis_ok" if vis else "ocultos_ok"]+=1
                else: res["falhas"].append(f"{painel}#{i} {d.value.suggested_filename} vazio")
            except Exception as e: res["falhas"].append(f"{painel}#{i} {str(e)[:80]}")
    br.close()
srv.shutdown(); print(json.dumps(res,ensure_ascii=False,indent=1))
