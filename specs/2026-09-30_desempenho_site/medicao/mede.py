import sys, json, time, collections
from playwright.sync_api import sync_playwright
url = sys.argv[1]; runs = int(sys.argv[2]) if len(sys.argv) > 2 else 3
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    res = []
    for i in range(runs):
        ctx = b.new_context(viewport={"width":1400,"height":900})
        pg = ctx.new_page()
        cdp = ctx.new_cdp_session(pg)
        cdp.send("Network.enable"); cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        # conexão "4G rápido" simulada, para que o custo de cada requisição apareça
        cdp.send("Network.emulateNetworkConditions", {"offline":False,"latency":40,"downloadThroughput":9_000_000/8,"uploadThroughput":3_000_000/8})
        reqs = []; sizes = {}
        cdp.on("Network.responseReceived", lambda e: reqs.append((e["requestId"], e["response"]["url"], e["type"])))
        cdp.on("Network.loadingFinished", lambda e: sizes.__setitem__(e["requestId"], e["encodedDataLength"]))
        t0 = time.time()
        pg.goto(url, wait_until="load")
        pg.wait_for_timeout(1500)
        m = pg.evaluate("""() => {const n=performance.getEntriesByType('navigation')[0];
          const fcp=performance.getEntriesByName('first-contentful-paint')[0];
          return {dcl:n.domContentLoadedEventEnd, load:n.loadEventEnd, fcp: fcp?fcp.startTime:null,
                  longtasks: 0}}""")
        por = collections.defaultdict(lambda:[0,0]); fontes=[]
        for rid,u,t in reqs:
            por[t][0]+=1; por[t][1]+=sizes.get(rid,0)
            if 'font' in u or 'googleapis' in u: fontes.append(u.split('?')[0][-60:])
        m["req"]={k:(v[0],round(v[1]/1024)) for k,v in por.items()}
        m["total_req"]=len(reqs); m["total_kb"]=round(sum(sizes.values())/1024)
        m["fontes"]=len(fontes)
        res.append(m); ctx.close()
    b.close()
for m in res: print({k:(round(v) if isinstance(v,float) else v) for k,v in m.items()})
