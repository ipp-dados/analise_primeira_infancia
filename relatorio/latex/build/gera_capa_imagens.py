# -*- coding: utf-8 -*-
"""Imagens da capa, da folha de rosto e do expediente do PDF (specs/2026-11-05_versao_final_site D6).

Referência (pedido do usuário, 2026-11-05): os relatórios técnicos do IPP no Data.Rio ("Panorama da Indústria da
Transformação na Economia Carioca", mar/2026) -- só os elementos principais (bloco institucional, edição mês | ano,
logo, expediente com direção e equipe); cores e tipografia são as do projeto.

Foto: "Criança segurando aberto um livro colorido com ilustrações", de Compagnons (@sigmund), Licença da Unsplash
(a mesma do banner do site; a original fica em website/build/_cache/, baixada por website/build/gera_banner.py).
Logo: website/assets/images/ipp-logo.png (clara, para fundo escuro) e uma versão escura gerada aqui.

Uso:  python relatorio/latex/build/gera_capa_imagens.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parents[3]
SAIDA = RAIZ / "relatorio" / "latex" / "pretextual"
sys.path.insert(0, str(RAIZ / "website" / "build"))
import gera_banner  # noqa: E402  (mesma foto e mesmo cache do banner)

A4 = 21 / 29.7          # largura / altura da página
CENTRO_X = 0.55          # centro horizontal do recorte (livro e mãos)


def recorte_retrato(foto):
    w, h = foto.size
    largura = round(h * A4)
    x0 = min(max(0, round(w * CENTRO_X - largura / 2)), w - largura)
    return foto.crop((x0, 0, x0 + largura, h))


def main():
    """Estilo do projeto (pedido do usuário, 2026-11-05: "use our style"), com os elementos principais do documento
    técnico do IPP: faixa de foto no alto da capa, logo no pé da capa, da folha de rosto e do expediente."""
    if not gera_banner.CACHE.exists():
        gera_banner.main()            # baixa a original para o cache
    foto = Image.open(gera_banner.CACHE).convert("RGB")
    w, h = foto.size
    faixa = foto.crop((0, int(h * 0.08), w, int(h * 0.92)))   # ~1,79:1 -> 11,8 cm de altura em 21 cm
    faixa.resize((2400, round(faixa.height * 2400 / faixa.width)), Image.LANCZOS).save(
        SAIDA / "capa_foto.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    # logo clara (fundo escuro) e escura (fundo claro), mesma transparência
    logo = Image.open(RAIZ / "website" / "assets" / "images" / "ipp-logo.png").convert("RGBA")
    logo.save(SAIDA / "logo_ipp_clara.png")
    escura = Image.new("RGBA", logo.size, (0x16, 0x20, 0x2A, 0))
    escura.putalpha(logo.getchannel("A"))
    escura.save(SAIDA / "logo_ipp_escura.png")
    for n in ("capa_foto.jpg", "logo_ipp_clara.png", "logo_ipp_escura.png"):
        print(f"{(SAIDA / n).relative_to(RAIZ)}: {(SAIDA / n).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
