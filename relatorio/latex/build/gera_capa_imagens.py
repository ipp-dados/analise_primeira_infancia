# -*- coding: utf-8 -*-
"""Imagens da capa, da folha de rosto e do expediente do PDF (specs/2026-11-05_versao_final_site D6).

Referência (pedido do usuário, 2026-11-05): os relatórios técnicos do IPP no Data.Rio ("Panorama da Indústria da
Transformação na Economia Carioca", mar/2026) -- só os elementos principais (bloco institucional, edição mês | ano,
logo, expediente com direção e equipe); cores e tipografia são as do projeto.

Foto (escolhida pelo usuário em 2026-11-10, opção D -- azul): crianças com um globo, EDI Aníbal Machado, 19/10/2026,
de Marcos de Paula / Prefeitura do Rio (uso autorizado pela Prefeitura). A original (~14 MB, nome original
107A2653FP576_EDI_Anibal_Machado_19.10.2026_MARCOS DE PAULA.jpg) fica em relatorio/latex/build/originais/, fora do git; só a imagem tratada (pretextual/capa_foto_azul.jpg) é versionada.
(Até 2026-11-10 a capa usava a foto do banner do site, Compagnons/Unsplash, em duas opções A clara e D azul.)
Logo: website/assets/images/ipp-logo.png (clara, para fundo escuro) e uma versão escura gerada aqui.

Uso:  python relatorio/latex/build/gera_capa_imagens.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parents[3]
SAIDA = RAIZ / "relatorio" / "latex" / "pretextual"
FOTO = RAIZ / "relatorio" / "latex" / "build" / "originais" / "capa_edi_anibal_machado_marcos_de_paula.jpg"

A4 = 21 / 29.7          # largura / altura da página
BASE = 0.85              # corta os 15% de baixo (cabelo de outra criança em primeiro plano; pedido do usuário)


def recorte_retrato(foto):
    """Do alto até BASE da altura, centrado na horizontal, na proporção A4."""
    w, h = foto.size
    y1 = round(h * BASE)
    largura = min(w, round(y1 * A4))
    x0 = (w - largura) // 2
    return foto.crop((x0, 0, x0 + largura, round(largura / A4)))


def main():
    """Estilo do projeto (pedido do usuário, 2026-11-05: "use our style"), com os elementos principais do documento
    técnico do IPP: faixa de foto no alto da capa, logo no pé da capa, da folha de rosto e do expediente."""
    foto = ImageOps.exif_transpose(Image.open(FOTO)).convert("RGB")
    # capa (opção D, escolhida em 2026-11-10): a foto como textura no azul institucional (004A80 escurecido a claro)
    lum = np.asarray(ImageOps.grayscale(recorte_retrato(foto)).resize((1400, round(1400 / A4)), Image.LANCZOS)) / 255
    escuro, claro = np.array([0, 59, 102]), np.array([24, 98, 150])
    Image.fromarray((escuro + (claro - escuro) * lum[..., None]).astype("uint8")).save(
        SAIDA / "capa_foto_azul.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    # logo clara (fundo escuro) e escura (fundo claro), mesma transparência
    logo = Image.open(RAIZ / "website" / "assets" / "images" / "ipp-logo.png").convert("RGBA")
    logo.save(SAIDA / "logo_ipp_clara.png")
    escura = Image.new("RGBA", logo.size, (0x16, 0x20, 0x2A, 0))
    escura.putalpha(logo.getchannel("A"))
    escura.save(SAIDA / "logo_ipp_escura.png")
    for n in ("capa_foto_azul.jpg", "logo_ipp_clara.png", "logo_ipp_escura.png"):
        print(f"{(SAIDA / n).relative_to(RAIZ)}: {(SAIDA / n).stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
