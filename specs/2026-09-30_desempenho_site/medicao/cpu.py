import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome"); ctx=b.new_context(viewport={"width":1400,"height":900}); pg=ctx.new_page()
    cdp=ctx.new_cdp_session(pg); cdp.send("Performance.enable")
    cdp.send("Emulation.setCPUThrottlingRate",{"rate":4})   # celular médio
    fonts=[]
    pg.on("response", lambda r: fonts.append((r.url[:110], r.headers.get("content-length"))) if ("gstatic" in r.url or "googleapis" in r.url) else None)
    pg.add_init_script("""window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>__lt.push(Math.round(e.duration)))).observe({type:'longtask',buffered:true});""")
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(2000)
    m={x["name"]:x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
    print({k:round(m[k]*1000) for k in ["ScriptDuration","LayoutDuration","RecalcStyleDuration","TaskDuration"]}, "nodes",int(m["Nodes"]))
    print("longtasks", pg.evaluate("__lt"))
    print("DCL", round(pg.evaluate("performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd")))
    for f in fonts: print(f)
    b.close()
