from playwright.sync_api import sync_playwright
U="http://127.0.0.1:8812/analise_primeira_infancia/"
with sync_playwright() as p:
    # AP/RP: mapas atrás de pills -- clica cada pill de cartão com mapa e passa o mouse
    b=p.chromium.launch(channel="chrome"); pg=b.new_page(viewport={"width":1400,"height":900}); pg.goto(U); pg.wait_for_timeout(500)
    visto={}
    for t in pg.evaluate("Array.from(document.querySelectorAll('.tab-panel')).map(t=>t.id)"):
        pg.evaluate(f"navegacao.ativa({t!r})"); pg.wait_for_timeout(200)
        cards=pg.locator(".tab-panel:not([hidden]) .option-card:has(.map-svg)")
        for ci in range(cards.count()):
            pills=cards.nth(ci).locator(":scope > .pill-col > .pill")
            for pi in range(pills.count()):
                if not pills.nth(pi).is_visible(): continue
                pills.nth(pi).click(); pg.wait_for_timeout(80)
                sv=cards.nth(ci).locator(".opt-pane:not([hidden]) .map-svg").first
                if not sv.count(): continue
                sid=sv.get_attribute("id"); n=pg.evaluate(f"window.MAPAS[{sid!r}].n")
                if n in visto: continue
                sv.locator("use[fill]").nth(2).hover(force=True); pg.wait_for_timeout(80)
                visto[n]=pg.evaluate(f"document.getElementById({sid!r}).closest('.map-svg-card').querySelector('.chart-tooltip').innerText").replace("\n"," | ")
    print("tooltips por nível:",visto); b.close()
    # celular: toque no mapa, rolagem horizontal, erros, em Chrome/Firefox/WebKit
    for nome,bt,kw in [("chrome",p.chromium,{"channel":"chrome"}),("firefox",p.firefox,{}),("webkit",p.webkit,{})]:
        b=bt.launch(**kw); erros=[]
        for vp in [(1400,900,False),(390,844,True),(768,1024,True)]:
            opts={"viewport":{"width":vp[0],"height":vp[1]}}
            if vp[2] and nome!="firefox": opts.update(is_mobile=True, has_touch=True)
            elif vp[2]: opts.update(has_touch=True)
            ctx=b.new_context(**opts); pg=ctx.new_page(); pg.on("pageerror",lambda e:erros.append(str(e)))
            pg.goto(U+"#proteção"); pg.wait_for_timeout(3000)
            larg=pg.evaluate("document.documentElement.scrollWidth - innerWidth")
            desenhados=pg.evaluate("""Array.from(document.querySelectorAll('.tab-panel')).map(p=>p.id.slice(0,4)+':'+p.querySelectorAll('.chart-svg').length+'/'+p.querySelectorAll('.map-svg use').length).join(' ')""")
            tt=""
            if vp[2]:
                u=pg.locator(".tab-panel:not([hidden]) .map-svg use[fill]").nth(5); u.scroll_into_view_if_needed(); u.tap(force=True); pg.wait_for_timeout(150)
                tt=pg.evaluate("Array.from(document.querySelectorAll('.tab-panel:not([hidden]) .map-svg-card .chart-tooltip')).map(t=>t.style.display).filter(d=>d=='block').length")
            print(nome,vp[:2],"scroll-x",larg,"tooltip-toque",tt,"|",desenhados)
            ctx.close()
        print(nome,"erros",erros); b.close()
