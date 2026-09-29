# -*- coding: utf-8 -*-
"""Versão de demonstração do site -- EXCLUSIVO da branch `demo` (specs/2026-09-29_demo; constituição §7).

Ligada por `"demo": true` em relatorio/publicacao.json. Com ela:
- texto não curado vem de website/build/textos_demo.json (texto provisório, D5/D6), nunca lorem;
- blocos pendentes não são emitidos (D8);
- a faixa de desenvolvimento é maior e traz a data da V.1 (D3/D11);
- o botão do PDF aponta para o PDF da própria branch (D10);
- o HTML final é conferido: sem lorem e sem quadro pendente (R2/R3).

O arquivo de textos provisórios NÃO é lido pelo PDF, pelo DOCX nem pela sincronização DOCX -> JSON: o texto curado
(relatorio/textos_curados.json) sempre tem precedência e a curadoria continua vendo lorem e pendentes.
"""
import datetime
import html as _html
import json
import re
from pathlib import Path

_PUB = json.loads(Path("relatorio/publicacao.json").read_text(encoding="utf-8"))
ATIVO = bool(_PUB.get("demo"))
_CFG = _PUB.get("demo_textos", {})

_CAMINHO = Path("website/build/textos_demo.json")
_TEXTOS = {k: v for k, v in json.loads(_CAMINHO.read_text(encoding="utf-8")).items() if not k.startswith("_")} \
    if ATIVO and _CAMINHO.exists() else {}
_FALTANDO = []   # chaves pedidas sem texto provisório (o build para no fim, com a lista toda)
_USADAS = set()

URL_PDF_DEMO = "https://raw.githubusercontent.com/ipp-dados/analise_primeira_infancia/demo/relatorio/analise_primeira_infancia.pdf"

_MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
          "novembro", "dezembro"]

def data_v1_extenso():
    d = datetime.date.fromisoformat(_PUB["lancamento_v1"])
    return f"{d.day} de {_MESES[d.month - 1]} de {d.year}"

def _bruto(chave):
    if chave not in _TEXTOS:
        _FALTANDO.append(chave)
        return "[texto provisório ausente]"
    _USADAS.add(chave)
    return _TEXTOS[chave]

def texto(chave):
    """Texto provisório de figura/abertura/síntese, marcado com data-texto-demo (D7)."""
    t = _bruto(chave)
    corpo = "<br><br>".join(_html.escape(p.strip()) for p in t.split("\n") if p.strip())
    return f'<span data-texto-demo="{_html.escape(chave)}">{corpo}</span>'

def itens(chave):
    """Achados do eixo: uma frase por linha."""
    return [f'<span data-texto-demo="{_html.escape(chave)}">{_html.escape(l.strip())}</span>'
            for l in _bruto(chave).split("\n") if l.strip()]

def banner_html():
    return ('<div class="dev-banner dev-banner-demo" role="alert">'
            f'<span class="dev-banner-linha">⚠️ {_html.escape(_CFG["faixa"])}</span>'
            f'<span class="dev-banner-data">Versão 1.0 prevista para {data_v1_extenso()}</span>'
            '</div>')

# palavras distintivas do gerador de lorem (build_site._LOREM_WORDS) -- nenhuma delas é português
_LOREM_RE = re.compile(r"\b(lorem|ipsum|dolor|consectetur|adipiscing|eiusmod|incididunt|labore|dolore|aliqua|"
                       r"exercitation|ullamco|laboris|consequat|reprehenderit|cillum|pariatur|excepteur|cupidatat|"
                       r"proident|officia|deserunt|mollit|laborum|curabitur|porttitor|sollicitudin|vestibulum|"
                       r"faucibus|cubilia|curae|tristique|senectus|egestas)\b", re.I)

def confere(html):
    """Para o build se sobrou chave sem texto provisório, lorem ou quadro pendente (R2/R3)."""
    erros = []
    if _FALTANDO:
        erros.append(f"{len(set(_FALTANDO))} chave(s) sem texto provisório em {_CAMINHO}: "
                     + ", ".join(sorted(set(_FALTANDO))))
    lorem = sorted(set(m.group(0).lower() for m in _LOREM_RE.finditer(html)))
    if lorem:
        erros.append(f"lorem no HTML: {lorem}")
    if "callout-pending" in html:
        erros.append("quadro pendente (callout-pending) no HTML")
    sobra = sorted(set(_TEXTOS) - _USADAS)
    if sobra:
        print(f"AVISO demo: {len(sobra)} texto(s) provisório(s) sem uso (curados agora ou chave antiga): {sobra}")
    if erros:
        raise SystemExit("DEMO BLOQUEADA:\n- " + "\n- ".join(erros))
    print(f"Demo OK: {len(_USADAS)} textos provisórios, sem lorem, sem pendentes.")
