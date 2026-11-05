# -*- coding: utf-8 -*-
"""Gera as imagens do banner do site a partir da foto do Unsplash (specs/2026-11-05_versao_final_site R1).

Foto: "Criança segurando aberto um livro colorido com ilustrações", de Compagnons (@sigmund), Licença da Unsplash
(uso gratuito, crédito pedido): https://unsplash.com/pt-br/fotografias/crianca-segurando-aberto-um-livro-colorido-com-ilustracoes-wccs6fKUtok

O site serve a imagem do próprio domínio (regra do site: nenhuma requisição a terceiros) e só publica .jpg/.png
(lista do workflow de deploy), por isso: recorte horizontal na faixa do livro e das mãos, duas larguras em JPEG
progressivo. A foto original é baixada uma vez para `website/build/_cache/` (fora do git) quando falta.

Uso:  python website/build/gera_banner.py
"""
import urllib.request
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).resolve().parent
CACHE = AQUI / "_cache" / "unsplash_wccs6fKUtok.jpg"
SAIDA = AQUI.parent / "assets" / "images"
URL_CDN = "https://images.unsplash.com/photo-1765223085025-0405fcfbb338?fm=jpg&q=85&w=3000&fit=max"

# faixa vertical (fração da altura) com o livro e as mãos; proporção 3:1 para caber no banner largo
FAIXA = (0.26, 0.76)
LARGURAS = (960, 1600)


def main():
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(URL_CDN, headers={"User-Agent": "analise-primeira-infancia/gera_banner"})
        CACHE.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    foto = Image.open(CACHE).convert("RGB")
    w, h = foto.size
    faixa = foto.crop((0, int(h * FAIXA[0]), w, int(h * FAIXA[1])))
    for largura in LARGURAS:
        altura = round(faixa.height * largura / faixa.width)
        destino = SAIDA / f"banner-foto-{largura}.jpg"
        faixa.resize((largura, altura), Image.LANCZOS).save(destino, "JPEG", quality=72, optimize=True, progressive=True)
        print(f"{destino.relative_to(AQUI.parents[1])}: {largura}x{altura}, {destino.stat().st_size // 1024} KB")


def gera_capa_pdf():
    """Mesma foto na capa do relatório em PDF (specs/2026-11-05_versao_final_site R5/D6): faixa um pouco mais alta,
    2400 px de largura (impressão A4 a ~290 dpi), JPEG q80."""
    foto = Image.open(CACHE).convert("RGB")
    w, h = foto.size
    faixa = foto.crop((0, int(h * 0.08), w, int(h * 0.92)))   # proporção ~1,79:1 -> 11,8 cm de altura em 21 cm (cobre a faixa de 11,5 cm)
    destino = AQUI.parents[1] / "relatorio" / "latex" / "pretextual" / "capa_foto.jpg"
    faixa.resize((2400, round(faixa.height * 2400 / faixa.width)), Image.LANCZOS).save(
        destino, "JPEG", quality=80, optimize=True, progressive=True)
    print(f"{destino.relative_to(AQUI.parents[1])}: {destino.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
    gera_capa_pdf()
