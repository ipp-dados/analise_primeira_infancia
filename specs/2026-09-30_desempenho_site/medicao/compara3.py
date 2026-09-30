import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
def shot(b,port,t):
    pg=b.new_page(viewport={"width":1280,"height":900}); pg.goto(f"http://127.0.0.1:{port}/analise_primeira_infancia/#{t}",wait_until="load"); pg.wait_for_timeout(2500)
    im=Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert("RGB"); pg.close(); return im
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    A=[shot(b,8811,"prioridade") for _ in range(3)]; N=[shot(b,8812,"prioridade") for _ in range(3)]
    ref=A[0]
    print("base", [ImageChops.difference(ref,x).getbbox() for x in A[1:]])
    print("novo", [ImageChops.difference(ref,x).getbbox() for x in N])
    print("novo x base-variante", [ImageChops.difference(x,y).getbbox() for x in A for y in N[:1]])
    b.close()
