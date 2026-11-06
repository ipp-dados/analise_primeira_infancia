"""T8.3 -- teste completo do site (Edge via Playwright), desktop 1366 e celular 390."""
import json, sys, threading, functools, http.server, re
from pathlib import Path
from playwright.sync_api import sync_playwright

SITE = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
class Q(H.func):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=str(SITE)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_port}/index.html"

PERFIS = [("desktop", dict(viewport={"width": 1366, "height": 768})),
          ("celular", dict(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True))]
res = {}
with sync_playwright() as p:
    br = p.chromium.launch(channel="msedge")
    for nome, opts in PERFIS:
        r = res[nome] = {"console": [], "pageerror": [], "reqfail": [], "abas": {}, "downloads": {"ok": 0, "falha": []},
                         "pills": {"cliques": 0, "erros_depois": 0}, "ancoras_quebradas": [], "deeplink": None}
        ctx = br.new_context(accept_downloads=True, **opts); pg = ctx.new_page()
        pg.on("console", lambda m, r=r: r["console"].append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e, r=r: r["pageerror"].append(str(e)))
        pg.on("requestfailed", lambda q, r=r: r["reqfail"].append(f"{q.url} {q.failure}"))
        pg.goto(URL, wait_until="load"); pg.wait_for_timeout(800)
        # ancoras internas
        r["ancoras_quebradas"] = pg.evaluate("""() => [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href'))
            .filter(h => h.length > 1 && !h.includes('/')).filter(h => !document.getElementById(decodeURIComponent(h.slice(1))))""")
        abas = pg.evaluate("() => [...document.querySelectorAll('button[role=tab]')].map(b => [b.id, b.innerText.trim()])")
        for tid, rot in abas:
            pg.click(f"#{tid}") if pg.is_visible(f"#{tid}") else pg.evaluate(f"document.getElementById('{tid}').click()")
            pg.wait_for_timeout(500)
            # rola até o fim para disparar o desenho tardio
            alt = pg.evaluate("document.documentElement.scrollHeight")
            y = 0
            while y < alt:
                y += 700; pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
                alt = pg.evaluate("document.documentElement.scrollHeight")
            pg.wait_for_timeout(1200)
            painel = pg.evaluate(f"document.getElementById('{tid}').getAttribute('aria-controls')")
            info = pg.evaluate("""(pid) => {
              const P = document.getElementById(pid);
              const outs = [...P.querySelectorAll('.out')];
              const vazios = outs.filter(o => { const d = o.querySelector(':scope > div[id]'); const s = o.querySelector('svg.map-svg');
                  if (s) return s.querySelectorAll('use,path').length === 0;
                  return d && d.childElementCount === 0; }).map(o => (o.querySelector('[id]')||{}).id);
              const largos = [...P.querySelectorAll('*')].filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.right > window.innerWidth + 1 && getComputedStyle(e).position !== 'fixed'; })
                  .filter(e => !e.closest('.table-wrap,.tabela-rolagem,[style*="overflow"]')).slice(0, 5).map(e => e.tagName + '.' + e.className);
              return {outs: outs.length, svgs: P.querySelectorAll('svg.chart-svg, .out svg').length, mapas: P.querySelectorAll('svg.map-svg').length,
                      vazios, rolagem_horizontal: document.documentElement.scrollWidth > window.innerWidth, largos,
                      pills: P.querySelectorAll('.pill').length, dl: P.querySelectorAll('.dl-btn').length};
            }""", painel)
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(200)
            pg.screenshot(path=str(OUT / f"{nome}_{painel}.png"), full_page=True)
            # pills: clica todas as que estão visíveis e não ativas
            n_err = len(r["pageerror"]) + len(r["console"])
            pills = pg.locator(f"#{painel} .pill")
            for i in range(pills.count()):
                el = pills.nth(i)
                try:
                    el.scroll_into_view_if_needed(timeout=1500)
                    if el.is_visible(): el.click(timeout=1500); r["pills"]["cliques"] += 1; pg.wait_for_timeout(80)
                except Exception as e: info.setdefault("pill_falha", []).append(str(e)[:80])
            r["pills"]["erros_depois"] += len(r["pageerror"]) + len(r["console"]) - n_err
            # downloads
            dls = pg.locator(f"#{painel} .dl-btn")
            for i in range(dls.count()):
                el = dls.nth(i)
                try:
                    el.scroll_into_view_if_needed(timeout=1500)
                    with pg.expect_download(timeout=4000) as d: el.click(timeout=1500)
                    f = d.value; caminho = f.path(); tam = Path(caminho).stat().st_size
                    linhas = Path(caminho).read_text(encoding="utf-8-sig").count("\n")
                    if tam > 10 and linhas >= 1: r["downloads"]["ok"] += 1
                    else: r["downloads"]["falha"].append(f"{f.suggested_filename} {tam}B")
                except Exception as e: r["downloads"]["falha"].append(f"{painel}#{i}: {str(e)[:90]}")
            r["abas"][rot] = info
        # deep link do SISVAN (achado antigo: título sob a barra fixa)
        alvo = pg.evaluate("() => { const h=[...document.querySelectorAll('h3')].find(h=>/SISVAN/i.test(h.innerText)); return h && h.id; }")
        if alvo:
            pg.goto(URL + "#" + alvo); pg.wait_for_timeout(1500)
            r["deeplink"] = pg.evaluate("""(id) => { const h=document.getElementById(id); const bars=[...document.querySelectorAll('.tabbar, header.sticky, .sticky, .navbar')]
               .filter(b=>['sticky','fixed'].includes(getComputedStyle(b).position)); const fundo=Math.max(0,...bars.map(b=>b.getBoundingClientRect().bottom));
               return {id, topo_titulo: Math.round(h.getBoundingClientRect().top), fundo_barra: Math.round(fundo), visivel: h.getBoundingClientRect().top >= fundo - 2}; }""", alvo)
            pg.screenshot(path=str(OUT / f"{nome}_deeplink_sisvan.png"))
        ctx.close()
    br.close()
srv.shutdown()
(OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
for nome, r in res.items():
    print(f"== {nome}: console {len(r['console'])}, pageerror {len(r['pageerror'])}, reqfail {len(r['reqfail'])}, "
          f"downloads ok {r['downloads']['ok']} falha {len(r['downloads']['falha'])}, pills {r['pills']}, ancoras quebradas {len(r['ancoras_quebradas'])}, deeplink {r['deeplink']}")
    for a, i in r["abas"].items():
        print(f"   {a:22} outs {i['outs']:3} mapas {i['mapas']:2} pills {i['pills']:3} dl {i['dl']:3} vazios {len(i['vazios'])} rolagemH {i['rolagem_horizontal']} largos {i['largos'][:2]} {i.get('pill_falha','')[:1] if i.get('pill_falha') else ''}")
