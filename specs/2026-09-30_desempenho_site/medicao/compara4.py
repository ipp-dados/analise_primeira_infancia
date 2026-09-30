import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
def shot(b,port,t):
    pg=b.new_page(viewport={"width":1280,"height":900}); pg.goto(f"http://127.0.0.1:{port}/analise_primeira_infancia/#{t}",wait_until="load"); pg.wait_for_timeout(900)
    pg.add_style_tag(content=".tabbar{visibility:hidden!important;box-shadow:none!important}"); pg.wait_for_timeout(200)
    im=Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert("RGB"); pg.close(); return im
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    for t in ["visao-geral","alimentação"]:
        A=[shot(b,8811,t) for _ in range(3)]; N=[shot(b,8812,t) for _ in range(3)]
        f=lambda x,y: ImageChops.difference(x,y).point(lambda v:255 if v>3 else 0).getbbox()
        print(t,"base×base",[f(A[0],x) for x in A[1:]],"novo×novo",[f(N[0],x) for x in N[1:]],"base×novo",[f(a,n) for a,n in zip(A,N)])
    b.close()
