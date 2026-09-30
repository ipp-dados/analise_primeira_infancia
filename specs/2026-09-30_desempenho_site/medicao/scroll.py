from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(channel="chrome")
    for port in (8811,8812):
      for t in ["prioridade","família-e-cuidados","proteção"]:
        pg=b.new_page(viewport={"width":1280,"height":900}); pg.goto(f"http://127.0.0.1:{port}/analise_primeira_infancia/#{t}",wait_until="load"); pg.wait_for_timeout(1500)
        print(port,t,pg.evaluate("[scrollY, document.documentElement.scrollHeight, document.querySelector('.tabbar').classList.contains('is-stuck')]")); pg.close()
    b.close()
