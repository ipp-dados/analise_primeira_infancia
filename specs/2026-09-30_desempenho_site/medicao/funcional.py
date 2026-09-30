from playwright.sync_api import sync_playwright
BASE="http://127.0.0.1:{}/analise_primeira_infancia/"
def links(pg):
    return pg.evaluate("""()=>Array.from(document.querySelectorAll('.tab-panel h3[id]')).filter((h,i)=>i%9==0).map(h=>h.closest('.tab-panel').id+'/'+h.id)""")
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    pg=b.new_page(viewport={"width":1400,"height":900}); pg.goto(BASE.format(8811)); L=links(pg); pg.close()
    # 1. deep links: mesma posição de rolagem
    difs=[]
    for l in L:
        ys=[]
        for port in (8811,8812):
            pg=b.new_page(viewport={"width":1400,"height":900}); pg.goto(BASE.format(port)+"#"+l, wait_until="load"); pg.wait_for_timeout(1800)
            ys.append(pg.evaluate("scrollY")); pg.close()
        if abs(ys[0]-ys[1])>2: difs.append((l,ys))
    print("deep links testados",len(L),"diferentes",difs)
    # 2. tooltip de mapa em cada nível + csv, em todas as abas, na versão nova
    pg=b.new_page(viewport={"width":1400,"height":900}); erros=[]; pg.on("pageerror",lambda e:erros.append(str(e)))
    pg.goto(BASE.format(8812)); pg.wait_for_timeout(800)
    visto=set(); tabs=pg.evaluate("Array.from(document.querySelectorAll('.tab-panel')).map(t=>t.id)")
    for t in tabs:
        pg.evaluate(f"navegacao.ativa({t!r})"); pg.wait_for_timeout(300)
        for i,info in enumerate(pg.evaluate("""()=>Array.from(document.querySelectorAll('.tab-panel:not([hidden]) .map-svg')).map(s=>[s.id, (window.MAPAS[s.id]||{}).n, s.querySelectorAll('use').length, !!s.closest('.map-svg-card').dataset.csv, s.getBoundingClientRect().width>0])""")):
            sid,nivel,nuse,csv,vis=info
            if not csv or nuse==0: print("PROBLEMA",t,info)
            if nivel in visto or not vis: continue
            u=pg.locator(f"#{sid} use[fill]").nth(3); u.scroll_into_view_if_needed(); u.hover(force=True); pg.wait_for_timeout(100)
            tt=pg.evaluate(f"(()=>{{const t=document.getElementById({sid!r}).closest('.map-svg-card').querySelector('.chart-tooltip');return [t.style.display,t.innerText]}})()")
            pg.mouse.move(2,2); pg.wait_for_timeout(100)
            fecha=pg.evaluate(f"document.getElementById({sid!r}).closest('.map-svg-card').querySelector('.chart-tooltip').style.display")
            print(t,nivel,"tooltip",tt,"depois de sair:",fecha); visto.add(nivel)
    print("níveis",visto,"erros",erros)
    # 3. custo da troca de aba com CPU 4x
    pg2=b.new_page(viewport={"width":1400,"height":900}); cdp=pg2.context.new_cdp_session(pg2); cdp.send("Emulation.setCPUThrottlingRate",{"rate":4})
    for port in (8811,8812):
        pg2.goto(BASE.format(port)); pg2.wait_for_timeout(6000)
        for t in ["prioridade","família-e-cuidados","proteção"]:
            ms=pg2.evaluate(f"(()=>{{const t0=performance.now();navegacao.ativa({t!r});document.body.offsetHeight;return Math.round(performance.now()-t0)}})()")
            print(port,"troca para",t,ms,"ms")
    b.close()
