from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome"); pg=b.new_page(viewport={"width":1400,"height":900})
    pg.add_init_script("""
      window.__t={};const wrap=(n)=>{Object.defineProperty(window,n,{configurable:true,set(f){delete window[n];window[n]=function(){const t=performance.now();const r=f.apply(this,arguments);__t[n]=(__t[n]||0)+performance.now()-t;return r};},get(){return undefined}})};
      ['lineChart','barChart','groupedBarChart'].forEach(wrap);
      document.addEventListener('DOMContentLoaded',()=>{__t.dcl0=performance.now()},true);
      window.addEventListener('load',()=>{__t.load=performance.now()});""")
    pg.goto("http://127.0.0.1:8811/analise_primeira_infancia/", wait_until="load"); pg.wait_for_timeout(1000)
    print(pg.evaluate("""()=>{const o={};document.querySelectorAll('.tab-panel').forEach(t=>o[t.id]=[t.querySelectorAll('*').length, t.hidden]);
      o.total=document.querySelectorAll('*').length; o.use=document.querySelectorAll('svg use').length; o.maps=document.querySelectorAll('.map-svg').length;
      o.charts=document.querySelectorAll('.chart-svg').length; o.t=Object.fromEntries(Object.entries(__t).map(([k,v])=>[k,Math.round(v)])); return o}"""))
    b.close()
