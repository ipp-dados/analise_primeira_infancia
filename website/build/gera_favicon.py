# -*- coding: utf-8 -*-
"""Favicon do site a partir de um SVG de `website/build/favicon_opcoes/` (specs/2026-09-28_melhorias_site U1).

    python website/build/gera_favicon.py [<opcao>]      (padrão: a_adulto_crianca)

Grava:
- `website/assets/images/favicon.svg` -- navegadores modernos (<link rel="icon" type="image/svg+xml">);
- `website/favicon.ico` -- 16, 32 e 48 px, para navegadores/ferramentas que pedem /favicon.ico;
- `website/assets/images/apple-touch-icon.png` -- 180 px, quadrado sem cantos arredondados (o iOS arredonda).
O `.ico` e o PNG são rasterizados pelo Chrome instalado (Playwright, `channel="chrome"`, só em desenvolvimento, como
`confere_textos.py`) e montados com Pillow. Trocar de opção = rodar de novo com outro nome e regenerar o site
(`build_site.py` põe `?v=<md5>` nos três links).
"""
import io
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parents[2]
OPCOES = RAIZ / "website" / "build" / "favicon_opcoes"
SITE = RAIZ / "website"


def rasteriza(svg, tamanho, pagina):
    pagina.set_viewport_size({"width": tamanho, "height": tamanho})
    svg = re.sub(r"<svg ", f'<svg width="{tamanho}" height="{tamanho}" ', svg, count=1)
    pagina.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
    return Image.open(io.BytesIO(pagina.screenshot(omit_background=True))).convert("RGBA")


def main(opcao="a_adulto_crianca"):
    svg = (OPCOES / f"{opcao}.svg").read_text(encoding="utf-8")
    (SITE / "assets" / "images" / "favicon.svg").write_text(svg, encoding="utf-8")
    # apple-touch-icon: fundo até a borda (o sistema aplica a máscara arredondada)
    svg_quadrado = re.sub(r'(<rect [^>]*?)\s+rx="[^"]*"', r"\1", svg, count=1)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(device_scale_factor=1)
        icones = [rasteriza(svg, t, pg) for t in (16, 32, 48)]
        toque = rasteriza(svg_quadrado, 180, pg)
        b.close()
    icones[-1].save(SITE / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)],
                    append_images=icones[:-1])
    toque.convert("RGB").save(SITE / "assets" / "images" / "apple-touch-icon.png", optimize=True)
    for f in (SITE / "assets" / "images" / "favicon.svg", SITE / "favicon.ico",
              SITE / "assets" / "images" / "apple-touch-icon.png"):
        print(f"{f.relative_to(RAIZ)}  {f.stat().st_size:,} bytes")


if __name__ == "__main__":
    main(*sys.argv[1:2])
