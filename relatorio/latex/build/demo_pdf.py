# -*- coding: utf-8 -*-
"""PDF de demonstração -- EXCLUSIVO da branch `demo` (specs/2026-09-29_demo D1/D2/D11; constituição §7).

Chamado por gera_latex.py depois de compilar o relatório inteiro, só com `"demo": true` em relatorio/publicacao.json:
1. acha a página de corte: a que tem a legenda "Mapa 1 –" E o número impresso 18 no cabeçalho (se divergirem, erro --
   o corte nunca anda em silêncio);
2. compila relatorio/latex/demo_aviso.tex (1 página; texto de publicacao.json -> gerado/demo_aviso.tex);
3. junta as páginas 1..corte + o aviso; o sumário fica completo (D2), mas links e marcadores para páginas cortadas saem.
Saída: relatorio/latex/_build/relatorio_demo.pdf. O texto provisório do site (textos_demo.json) não entra aqui.
"""
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pymupdf

AQUI = Path(__file__).resolve().parent
LATEX = AQUI.parent
RAIZ = LATEX.parents[1]
PAGINA_IMPRESSA = 18
LEGENDA_CORTE = "Mapa 1 –"
_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
          "novembro", "dezembro"]


def config():
    pub = json.loads((RAIZ / "relatorio/publicacao.json").read_text(encoding="utf-8"))
    return pub if pub.get("demo") else None


def _data_extenso(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} de {_MESES[d.month - 1]} de {d.year}"


def _esc(s):
    return re.sub(r"([&%$#_{}])", r"\\\1", s)


def pagina_corte(doc):
    """Índice (0-based) da última página mantida."""
    # só páginas do corpo: as listas de gráficos/mapas e o sumário (linhas pontilhadas) também citam "Mapa 1 –" e "18"
    corpo = [(i, p.get_text()) for i, p in enumerate(doc)]
    corpo = [(i, t) for i, t in corpo if ". . ." not in t]
    por_legenda = [i for i, t in corpo if LEGENDA_CORTE in t]
    # cabeçalho do abnTeX2: número impresso numa linha própria nas primeiras linhas da página
    por_numero = [i for i, t in corpo if str(PAGINA_IMPRESSA) in [l.strip() for l in t.splitlines()[:4]]]
    if not por_legenda or not por_numero or por_legenda[0] != por_numero[0]:
        sys.exit(f"demo_pdf: corte ambíguo -- '{LEGENDA_CORTE}' na(s) página(s) {[i + 1 for i in por_legenda]}, "
                 f"número impresso {PAGINA_IMPRESSA} na(s) {[i + 1 for i in por_numero]}. Revise D1 de specs/2026-09-29_demo.")
    return por_legenda[0]


def compila_aviso(pub):
    t = pub["demo_textos"]
    texto = _esc(t["aviso_pdf"].format(data=_data_extenso(pub["lancamento_v1"])))
    (LATEX / "gerado/demo_aviso.tex").write_text(
        "% Gerado por build/demo_pdf.py a partir de relatorio/publicacao.json -- não editar à mão.\n"
        f"\\newcommand{{\\demotitulo}}{{{_esc(t['aviso_pdf_titulo'])}}}\n\\newcommand{{\\demotexto}}{{{texto}}}\n",
        encoding="utf-8")
    env = dict(os.environ, TEXINPUTS=str(LATEX) + os.pathsep)
    r = subprocess.run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-outdir=_build",
                        "demo_aviso.tex"], cwd=LATEX, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    if r.returncode != 0:
        sys.exit("demo_pdf: latexmk falhou em demo_aviso.tex -- ver relatorio/latex/_build/demo_aviso.log")
    return LATEX / "_build/demo_aviso.pdf"


def monta(pub):
    doc = pymupdf.open(LATEX / "_build/relatorio.pdf")
    ultima = pagina_corte(doc)
    n = ultima + 1
    toc = [e for e in doc.get_toc(simple=True) if 0 < e[2] <= n]   # marcadores só para páginas mantidas (destino por número de página: o destino nomeado se perde no select)
    doc.select(list(range(n)))
    removidos = 0
    for p in doc:   # sumário e listas completos (D2), mas sem link para página que não existe mais
        for l in p.get_links():
            if l.get("kind") in (pymupdf.LINK_GOTO, pymupdf.LINK_NAMED) and not (0 <= l.get("page", -1) < n):
                p.delete_link(l)
                removidos += 1
    aviso = pymupdf.open(compila_aviso(pub))
    doc.insert_pdf(aviso)
    toc.append([1, pub["demo_textos"]["aviso_pdf_titulo"], n + 1])
    doc.set_toc(toc)
    saida = LATEX / "_build/relatorio_demo.pdf"
    doc.save(saida, garbage=3, deflate=True)
    print(f"PDF de demonstração: páginas 1-{n} (impressa {PAGINA_IMPRESSA}) + aviso = {n + 1} páginas; "
          f"{removidos} links para páginas cortadas removidos")
    return saida
