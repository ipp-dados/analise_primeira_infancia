"""Diagrama Mermaid de docs/especificacao_projeto.md em PNG, na vertical (para caber no A4 do DOCX).
Uso: python docs/build/diagrama_png.py <pasta_tmp>/diagrama.png"""
import re, sys, pathlib
from playwright.sync_api import sync_playwright
md = pathlib.Path('docs/especificacao_projeto.md').read_text(encoding='utf-8')
bloco = re.search(r"```mermaid\n(.*?)```", md, re.S).group(1).replace('flowchart LR', 'flowchart TB')
html = """<!doctype html><html><head><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script></head>
<body style="margin:0;background:#fff"><pre class="mermaid">""" + bloco + """</pre>
<script>mermaid.initialize({startOnLoad:true, theme:'base', flowchart:{htmlLabels:true, curve:'basis'},
 themeVariables:{fontFamily:'Arial', fontSize:'15px', primaryColor:'#e6eef6', primaryBorderColor:'#004a80',
 primaryTextColor:'#1b2a38', lineColor:'#4a6f8f', clusterBkg:'#f6f8fa', clusterBorder:'#9fb4c7'}});</script></body></html>"""
out = pathlib.Path(sys.argv[1])
(out.parent / 'diagrama.html').write_text(html, encoding='utf-8')
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome'); pg = b.new_page(device_scale_factor=2, viewport={'width': 1600, 'height': 900})
    pg.goto((out.parent / 'diagrama.html').resolve().as_uri()); pg.wait_for_selector('pre.mermaid svg', timeout=20000)
    pg.locator('pre.mermaid svg').screenshot(path=str(out)); b.close()
print('ok', out)
