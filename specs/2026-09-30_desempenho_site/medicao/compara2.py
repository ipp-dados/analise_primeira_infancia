import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
def shot(b,port,t):
    pg=b.new_page(viewport={"width":1280,"height":900}); pg.goto(f"http://127.0.0.1:{port}/analise_primeira_infancia/#{t}",wait_until="load"); pg.wait_for_timeout(1500)
    im=Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert("RGB"); pg.close(); return im
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    for t in ["prioridade","família-e-cuidados"]:
        a1=shot(b,8811,t); a2=shot(b,8811,t); n=shot(b,8812,t)
        print(t,"base x base",ImageChops.difference(a1,a2).getbbox(),"base x novo",ImageChops.difference(a1,n).getbbox())
        d=ImageChops.difference(a1,n).getbbox()
        if d:
            y=d[1]; a1.crop((0,y-60,1280,y+200)).save(f"{t[:5]}_base.png"); n.crop((0,y-60,1280,y+200)).save(f"{t[:5]}_novo.png")
    b.close()
