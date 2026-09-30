import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
tabs=["visao-geral","prioridade","inclusão","família-e-cuidados","proteção","direito-ao-brincar","alimentação","moradia"]
def shots(b,port,w):
    out={}; erros=[]
    for t in tabs:
        pg=b.new_page(viewport={"width":w,"height":900}); pg.on("pageerror",lambda e:erros.append(str(e)))
        pg.goto(f"http://127.0.0.1:{port}/analise_primeira_infancia/#{t}",wait_until="load"); pg.wait_for_timeout(900)
        pg.add_style_tag(content=".tabbar{visibility:hidden!important;box-shadow:none!important}"); pg.wait_for_timeout(200); pg.evaluate("document.fonts.ready"); out[t]=Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert("RGB"); pg.close()
    return out,erros
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    for w in (1400,1280):
        a,ea=shots(b,8811,w); n,en=shots(b,8812,w)
        for t in tabs:
            if a[t].size!=n[t].size: print(w,t,"TAMANHO",a[t].size,n[t].size); continue
            d=ImageChops.difference(a[t],n[t]); ext=max(x[1] for x in d.getextrema()); bb=d.point(lambda v:255 if v>3 else 0).getbbox()
            print(w,t,"max",ext,"bbox>3",bb)
        print("erros", ea, en)
    b.close()
