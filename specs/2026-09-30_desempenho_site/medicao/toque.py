from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    for port in (8811,8812):
        ctx=b.new_context(viewport={"width":390,"height":844},is_mobile=True,has_touch=True); pg=ctx.new_page()
        pg.goto(f"http://127.0.0.1:{port}/analise_primeira_infancia/#visao-geral"); pg.wait_for_timeout(2500)
        u=pg.locator(".tab-panel:not([hidden]) .map-svg use[fill]").nth(40); u.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        bb=u.bounding_box(); x,y=bb["x"]+bb["width"]/2, bb["y"]+bb["height"]/2
        hit=pg.evaluate(f"(()=>{{const e=document.elementFromPoint({x},{y});return e.tagName+' '+(e.getAttribute('href')||'')}})()")
        pg.touchscreen.tap(x,y); pg.wait_for_timeout(200)
        print(port,"alvo",hit,"tooltips abertos",pg.evaluate("Array.from(document.querySelectorAll('.map-svg-card .chart-tooltip')).filter(t=>t.style.display=='block').map(t=>t.innerText.replace(/\s+/g,' '))"),
              "toque:",pg.evaluate("document.querySelectorAll('use.toque').length"))
        ctx.close()
    b.close()
