"""Ícones do site (website/assets/icons/*.svg, Lucide, ISC) -> macros TikZ em relatorio/latex/gerado/icones.tex.

Mesmo desenho do site, sem conversor externo no build do LaTeX: cada forma do SVG (path, circle, rect,
line, polyline...) vira um caminho TikZ de retas e curvas de Bézier cúbicas, com o eixo y já invertido
aqui (SVG cresce para baixo, TikZ para cima). Arcos são convertidos em Béziers antes -- o `svg.path` do
TikZ inverte o sentido dos arcos quando o eixo y é espelhado (visto nas páginas-amostra de 2026-09-25).
Uso no LaTeX: \\icone{target} ou \\icone[1.6em]{shield-check}.

Requer `svgelements` (pip). Uso (da raiz do projeto):  python relatorio/latex/build/gera_icones.py
"""
from pathlib import Path

from svgelements import SVG, Arc, Close, CubicBezier, Line, Move, Path as SPath, QuadraticBezier, Shape

RAIZ = Path(__file__).resolve().parents[3]
PASTA = RAIZ / "website/assets/icons"
SAIDA = RAIZ / "relatorio/latex/gerado/icones.tex"
LADO = 24


def p(pt):
    return f"({pt.x:.3f},{LADO - pt.y:.3f})".replace(".000", "")


def caminho_tikz(forma):
    caminho = abs(SPath(forma)) if not isinstance(forma, SPath) else abs(forma)
    partes = []
    for seg in caminho:
        if isinstance(seg, Move):
            partes.append(p(seg.end))
        elif isinstance(seg, Close):
            partes.append("-- cycle")
        elif isinstance(seg, Line):
            partes.append(f"-- {p(seg.end)}")
        elif isinstance(seg, CubicBezier):
            partes.append(f".. controls {p(seg.control1)} and {p(seg.control2)} .. {p(seg.end)}")
        elif isinstance(seg, QuadraticBezier):
            c = seg.control
            c1 = seg.start + (c - seg.start) * (2 / 3)
            c2 = seg.end + (c - seg.end) * (2 / 3)
            partes.append(f".. controls {p(c1)} and {p(c2)} .. {p(seg.end)}")
        elif isinstance(seg, Arc):
            for cub in seg.as_cubic_curves():
                partes.append(f".. controls {p(cub.control1)} and {p(cub.control2)} .. {p(cub.end)}")
    return "\\draw " + " ".join(partes) + ";" if partes else ""


def main():
    linhas = ["% Gerado por relatorio/latex/build/gera_icones.py -- não editar à mão.",
              "% Ícones Lucide (ISC) de website/assets/icons/, os mesmos do site (y já invertido, arcos em Bézier)."]
    for svg in sorted(PASTA.glob("*.svg")):
        doc = SVG.parse(str(svg))
        corpo = " ".join(filter(None, (caminho_tikz(el) for el in doc.elements() if isinstance(el, Shape))))
        linhas.append(f"\\expandafter\\def\\csname icone@{svg.stem}\\endcsname{{{corpo}}}")
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"{len(linhas) - 2} ícones -> {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
