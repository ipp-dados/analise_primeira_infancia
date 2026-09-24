# -*- coding: utf-8 -*-
"""Protótipo de layout/tokens (specs/website_refactor Bloco 4) -- NÃO publicado.

Monta website/build/prototype/index.html com pedaços REAIS do site gerado (website/index.html
e data/charts.js): banner, barra de abas, Visão geral, 1 painel de eixo com achados, 4 subseções
(gráficos com pills, mapa com pills, bloco pendente, nota metodológica), caixa de fontes, sumário
lateral. Usa os CSS em rascunho desta pasta (prototype/css/) e os JS reais (js/navigation.js,
js/sidebar.js, js/charts.js). Depois da aprovação, os CSS daqui substituem website/css/ e o
gerador passa a emitir esta estrutura (Blocos 5-6).

    python website/build/prototype/make_prototype.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "website"
OUT = Path(__file__).resolve().parent / "index.html"

html = (SITE / "index.html").read_text(encoding="utf-8")
render = (SITE / "data" / "charts.js").read_text(encoding="utf-8")


def bloco(inicio):
    """Div completo (com divs aninhados) a partir do offset `inicio`."""
    prof = 0
    for m in re.finditer(r"<div\b|</div>", html[inicio:]):
        prof += 1 if m.group() == "<div" else -1
        if prof == 0:
            return html[inicio:inicio + m.end()]
    raise ValueError("div sem fechamento")


def option_cards():
    return [bloco(m.start()) for m in re.finditer(r'<div class="option-card option-card-(?:grafico|mapa)', html)]


def icone(nome):
    svg = (SITE / "assets" / "icons" / f"{nome}.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    svg = re.sub(r'\s*class="[^"]*"', "", svg)
    svg = re.sub(r"\s+", " ", svg).replace("> <", "><")
    return svg.replace("<svg ", '<svg class="icon" aria-hidden="true" focusable="false" ', 1)


def callout(tipo, icone_nome, rotulo, corpo):
    return (f'<div class="callout callout-{tipo}"><span class="callout-icon">{icone(icone_nome)}</span>'
            f'<div class="eyebrow callout-label">{rotulo}</div><div class="callout-body">{corpo}</div></div>')


cards = option_cards()
EIXOS = [  # (id, rótulo curto da aba, título h2, ícone)
    ("visao-geral", "Visão geral", "Visão geral", "layout-dashboard"),
    ("prioridade-sem-secundário", "Prioridade", "Prioridade (sem secundário)", "target"),
    ("inclusão", "Inclusão", "Inclusão", "handshake"),
    ("família-e-cuidados", "Família e Cuidados", "Família e Cuidados", "users"),
    ("proteção", "Proteção", "Proteção", "shield-check"),
    ("alimentação", "Alimentação", "Alimentação", "apple"),
    ("moradia", "Moradia", "Moradia", "house"),
]

# ---- pedaços reais --------------------------------------------------------------------
intro = re.search(r'<p class="lede">(.*?)</p>', html, re.S).group(1)
achados = re.search(r'<div class="key-takeaways">.*?<ul>(.*?)</ul>', html, re.S).group(1)
pendente = re.search(r'<div class="pending-block">.*?<p>(.*?)</p>', html, re.S).group(1)
nota = re.search(r'<div class="pending-block pending-inline">.*?<p>(.*?)</p>', html, re.S)
nota = nota.group(1) if nota else "Nota metodológica de exemplo."
logo = '<img src="../../assets/images/ipp-logo.png" alt="Prefeitura do Rio de Janeiro — Instituto Pereira Passos" class="ipp-logo">'
footer = re.search(r'<footer class="doc-foot">.*?</footer>', html, re.S).group(0).replace("assets/images/", "../../assets/images/")
footer = footer.replace('<div class="footer-cols">', '<div class="container"><div class="footer-cols">', 1)
footer = footer.replace('<div class="footer-rule">', '</div><div class="container"><div class="footer-rule">', 1).replace("</footer>", "</div></footer>")
basemap_css = re.search(r"<style>\.map-bg.*?</style>", html, re.S).group(0).replace("url(assets/", "url(../../assets/")

# subseções do painel Prioridade: (h3, cartão)
SECOES = [
    ("Série temporal", cards[2]),
    ("População de 0 a 6 anos por ano (estimativas Ripsa/MS)", cards[3]),
    ("Mapas", cards[0]),
    ("Nascidos vivos e mortalidade por raça/cor", cards[4]),
]
ids_graficos = set()
for _, c in SECOES:
    ids_graficos.update(re.findall(r'<div id="(c-\d+)"', c))
chamadas = [l for l in render.splitlines() if (m := re.search(r'byId\("(c-\d+)"\)', l)) and m.group(1) in ids_graficos]
fontes = []
for _, c in SECOES:
    for f in re.findall(r'<div class="out-src">(.*?)</div>', c) + re.findall(r"Fonte: (.*?)</div>", c):
        if f not in fontes:
            fontes.append(f)

# ---- montagem ---------------------------------------------------------------------------
tabs = "".join(
    f'<button type="button" role="tab" class="tab" id="tab-{i}" aria-controls="{pid}" aria-selected="false" tabindex="-1">'
    f'{icone(ic)}<span>{rot}</span></button>'
    for i, (pid, rot, _, ic) in enumerate(EIXOS))

def cabecalho(n, titulo, ic):
    return (f'<header class="panel-head"><span class="panel-icon">{icone(ic)}</span><div>'
            f'<div class="eyebrow panel-eyebrow">Eixo {n} de 6</div><h2>{titulo}</h2></div></header>')

cartoes_eixo = "".join(
    f'<a class="eixo-card" href="#{pid}"><span class="panel-icon">{icone(ic)}</span>'
    f'<span class="eyebrow eixo-card-num">Eixo {n}</span><span class="eixo-card-title">{tit}</span>'
    f'<span class="eixo-card-meta">{"10 subseções · 1 pendente" if n == 1 else "(protótipo)"}</span></a>'
    for n, (pid, _, tit, ic) in enumerate(EIXOS[1:], start=1))
paineis = [
    f'<section class="tab-panel" id="visao-geral" role="tabpanel" aria-labelledby="tab-0" hidden>'
    f'<div class="overview-intro"><div class="eyebrow panel-eyebrow">Apresentação</div><h2>Introdução</h2><p class="lede">{intro}</p></div>'
    f'<div class="eyebrow eixo-grid-label">Eixos da política municipal de primeira infância</div>'
    f'<div class="eixo-grid">{cartoes_eixo}</div></section>'
]
corpo = cabecalho(1, EIXOS[1][2], EIXOS[1][3]) + callout("findings", "lightbulb", "Principais achados", f"<ul>{achados}</ul>")
for k, (h3, c) in enumerate(SECOES):
    corpo += f'<h3 id="proto-h3-{k}">{h3}</h3>'
    if k == 1:
        corpo += callout("note", "info", "Nota metodológica", f"<p>{nota}</p>")
    corpo += c
corpo += '<h3 id="proto-h3-pendente">Indicador catalogado (exemplo)</h3>'
corpo += callout("pending", "construction", "Indicador catalogado, ainda não disponível", f"<p>{pendente}</p>")
corpo += callout("sources", "book-open", "Fontes desta seção", "<ul>" + "".join(f"<li>{f}</li>" for f in fontes) + "</ul>")
paineis.append(f'<section class="tab-panel" id="{EIXOS[1][0]}" role="tabpanel" aria-labelledby="tab-1" hidden>{corpo}</section>')
for n, (pid, _, tit, ic) in enumerate(EIXOS[2:], start=2):
    paineis.append(f'<section class="tab-panel" id="{pid}" role="tabpanel" aria-labelledby="tab-{n}" hidden>'
                   f'{cabecalho(n, tit, ic)}<p style="color:var(--ink-3)">(protótipo: o conteúdo desta aba entra no Bloco 5)</p></section>')

navs = ['<nav class="outline-nav" data-panel="visao-geral" hidden>' + "".join(
    f'<a href="#{pid}" data-alvo="{pid}">{tit}</a>' for pid, _, tit, _ in EIXOS[1:]) + "</nav>"]
navs.append(f'<nav class="outline-nav" data-panel="{EIXOS[1][0]}" hidden>' + "".join(
    f'<a href="#{EIXOS[1][0]}/proto-h3-{k}" data-alvo="proto-h3-{k}">{h3}</a>' for k, (h3, _) in enumerate(SECOES))
    + f'<a href="#{EIXOS[1][0]}/proto-h3-pendente" data-alvo="proto-h3-pendente">Indicador catalogado (exemplo)</a></nav>')

espectro = "".join(f'<span style="background:var(--c{i})"></span>' for i in range(1, 12))
doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Protótipo · Primeira Infância Carioca</title>
<link rel="stylesheet" href="css/main.css">
<link rel="stylesheet" href="css/layout.css">
<link rel="stylesheet" href="css/components.css">
{basemap_css}
</head>
<body>
<div class="dev-banner" role="alert">⚠️ EM DESENVOLVIMENTO / TEMPORÁRIO — esta é uma versão de teste do relatório, publicada para validação interna. Conteúdo, dados e layout ainda podem mudar.</div>
<header class="site-banner">
  <div class="container banner-inner">
    <div>
      <span class="banner-logo">{logo}</span>
      <div class="eyebrow banner-eyebrow">Relatório interativo · Instituto Pereira Passos</div>
      <h1>Análise Primeira Infância Carioca</h1>
    </div>
    <div>
      <p class="banner-desc">Indicadores de primeira infância (0 a 6 anos) do município do Rio de Janeiro, organizados pelos eixos da política municipal. Cada gráfico traz a fonte e a opção de baixar os dados; a metodologia completa está no notebook e no relatório em PDF.</p>
      <p class="banner-meta">Atualizado 24 de setembro de 2026</p>
    </div>
  </div>
  <div class="spectrum-bar" aria-hidden="true">{espectro}</div>
</header>
<nav class="tabbar" aria-label="Seções do relatório"><div class="container tabbar-inner" role="tablist">{tabs}</div></nav>
<div class="container page-grid">
<main class="panels">
{"".join(paineis)}
</main>
<aside class="outline" aria-label="Nesta seção"><div class="outline-card">
<div class="outline-head"><span class="eyebrow outline-label">Nesta seção</span><span class="outline-pct">0%</span></div>
<div class="outline-progress" aria-hidden="true"><span></span></div>
{"".join(navs)}
</div></aside>
</div>
{footer}
<script src="../../data/geo.js"></script>
<script src="../../js/charts.js"></script>
<script>
(function(){{
"use strict";
{chr(10).join(chamadas)}
}})();
</script>
<script src="../../js/sidebar.js"></script>
<script src="../../js/navigation.js"></script>
</body>
</html>
"""
OUT.write_text(doc, encoding="utf-8", newline="\n")
print(f"wrote {OUT} ({len(doc):,} chars, {len(chamadas)} gráficos, {len(fontes)} fontes)")
