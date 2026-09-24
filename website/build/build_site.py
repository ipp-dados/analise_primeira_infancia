# -*- coding: utf-8 -*-
"""Build the static website (website/) -- specs/website_refactor.

Moved here from .claude/skills/export_pdf_report/scripts/build_html_report.py
(specs/website_refactor, Bloco 1); the history below predates the move and
still says relatorio/index.html, which was the output path until then.

Usage (from anywhere; paths resolve against the project root):
    python website/build/build_site.py [out_dir]      # default: website/

---- previous docstring ----
Build the single consolidated interactive HTML report (relatorio/index.html).

Note (specs/ajuste_eixos, Bloco 3): the report's 9 h2 sections used to mirror
analise.py's section order (one per data source: Censo, CadUnico, DataSUS/
Tabnet, causas evitaveis, gravidez/puerperio, mortalidade neonatal, SISVAN,
cobertura vacinal, Educacao). As of this round they were regrouped into 6 h2
"eixos da politica municipal" (Prioridade sem secundario, Inclusao, Familia e
Cuidados, Protecao, Alimentacao, Moradia), per specs/estrutura_eixos.md (the
authoritative crosswalk) and specs/ajuste_eixos/specs.md (the decision
record for the classification rules and the 18 discarded indicators). Some
old h2 sections (CadUnico, causas evitaveis, gravidez/puerperio, mortalidade
neonatal, SISVAN, cobertura vacinal) now appear as h3 subsections nested
inside their new eixo, with their own former h3/h4/h5 headings demoted one
level; others (Censo, DataSUS/Tabnet, Educacao) had their content split
across more than one eixo at the h3/pill level -- see specs/estrutura_eixos.md
for the indicator-by-indicator mapping, not this docstring. 16 catalog
indicators with no real analise.py output yet are rendered via
emite_bloco_pendente() (a labeled placeholder, never a silent empty section).

Replaces the old 3-file setup (index.html / lighter_index.html / white_index.html),
which was hand-built by unsaved ad-hoc scripts (see relatorio/specs.md). This script
is the first *persisted* generator: it reads tabelas_finais/*.csv (same source the
PDF pipeline uses) and renders interactive SVG charts via a small JS engine
(lineChart/barChart/groupedBarChart, lifted from the old lighter_index.html and
extended with the "many-series" highlight logic used in analise.py's
serie_temporal_multipla). Per specs/visual-identity decision B, this report is
visualization-only: title + source + chart/map + optional data table, no prose/notes
(those stay in the notebook and the PDF). Maps are interleaved in the same position
they appear in analise.py (not grouped in one trailing section), and the page opens
with a persistent navbar linking every h2 section.

This is a direct transcription of analise.py's chart/map call sites, in the same
order they appear there -- if analise.py's sections, column names, exported
filenames, or cell order change, this needs matching edits.

v6 (specs/relatorio-interativo) rebuilt the visual identity and interaction model to
match a reviewed wireframe/mockup -- brutalist bordered cards (no shadow/radius),
retractable h2 sections, a pill-selector (`option_card`) replacing what used to be a
wall of near-identical repeated charts, an outlier toggle (Tukey fences, applied
centrally in line_chart/bar_chart/grouped_bar_chart/mapa_svg -- not per call site),
per-chart-card CSV download, fixed max/min/most-recent labels on every line chart, and
institutional IPP/Prefeitura-do-Rio colors (navy/cyan) scoped to the navbar/footer
chrome only, never the data palette. Maps are now inline interactive SVG (`mapa_svg()`
-- GeoJSON/dissolve -> paths, tooltip per region) instead of the matplotlib PNGs in
mapas/, covering bairro, AP/RP (dissolved from the bairro geojson, same as
mapa_coropletico_bairros in analise.py) and CAP-saude (a separate geojson, see
`_geo_nivel`) levels; `map_card`/`maps_block`/`check_maps` (the old PNG embedder) are
kept only as a fallback for any future indicator that doesn't fit one of those 4
geometry regimes. Known tradeoff: embedding real SVG geometry per map instance (166
bairro paths, repeated per indicator) makes the output much heavier than the old
base64-PNG version (~20MB vs ~5MB) -- not yet optimized (e.g. sharing paths via
<defs>/<use>), tracked in specs/roadmap.md.

Usage (from project root):
    python .claude/skills/export_pdf_report/scripts/build_html_report.py [out_path]
"""
import base64
import io
import json
import random
import math
import os
import re
import sys
import datetime
from pathlib import Path

# specs/website_refactor Bloco 1: o gerador saiu de .claude/skills/export_pdf_report/scripts/
# (era build_html_report.py). Os caminhos abaixo continuam relativos ao root do projeto
# (tabelas_finais/, dados_locais/geo/, relatorio/textos_curados.json), por isso o chdir;
# gera_estrutura_eixos continua morando na skill do PDF/DOCX e é só importado daqui.
ROOT = Path(__file__).resolve().parents[2]
_OUT_ARG = str(Path(sys.argv[1]).resolve()) if len(sys.argv) > 1 else None   # relativo ao cwd de quem chamou
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "export_pdf_report" / "scripts"))

from gera_estrutura_eixos import avisa_itens_sem_arquivo
# populacao-referencia D4: avisa (sem mudar a saída) itens do crosswalk que o relatório pularia em silêncio
avisa_itens_sem_arquivo()

import pandas as pd
from PIL import Image

TF = "tabelas_finais"
MAPAS = "mapas"
OUT_PATH = _OUT_ARG or "website"   # pasta de saída (specs/website_refactor Bloco 2)

# ---------------------------------------------------------------- helpers --

def read(name, **kw):
    return pd.read_csv(f"{TF}/{name}", encoding="utf-8", **kw)

def clean_causa(label):
    return re.sub(r'^\d[\d.]*\.?\s*', '', str(label))

def jsvals(seq):
    """pandas/numpy -> JSON-safe list (NaN/None -> null, numpy scalars -> float)."""
    out = []
    for v in seq:
        if v is None or (isinstance(v, float) and math.isnan(v)) or pd.isna(v):
            out.append(None)
        elif isinstance(v, str):
            out.append(v)
        else:
            out.append(round(float(v), 4))
    return out

parts = []      # HTML body
scripts = []     # JS statements appended inside the IIFE, in order
toc = []          # (level, title, anchor_id) collected as headings are emitted
_counter = [0]
_slugs = set()

def new_id(prefix):
    _counter[0] += 1
    return f"{prefix}-{_counter[0]}"

def slugify(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE).strip().lower()
    slug = re.sub(r'[\s_]+', '-', text) or 'sec'
    base, i = slug, 2
    while slug in _slugs:
        slug = f"{base}-{i}"
        i += 1
    _slugs.add(slug)
    return slug

section_starts = []  # (index_in_parts, title, sid) -- 1 per h2, used to wrap sections (retratil)

def h2(t):
    sid = slugify(t)
    toc.append((2, t, sid))
    section_starts.append((len(parts), t, sid))
    parts.append(f'<h2 id="{sid}">{t}</h2>')

def h3(t):
    sid = slugify(t)
    toc.append((3, t, sid))
    parts.append(f'<h3 id="{sid}">{t}</h3>')

def h4(t): parts.append(f"<h4>{t}</h4>")
def h5(t): parts.append(f"<h5>{t}</h5>")
def h6(t): parts.append(f"<h6>{t}</h6>")

def _out_div(elem_id, fonte, titulo=None, csv_attr=None, filename=None):
    tit = f'<div class="chart-subtitle">{titulo}</div>' if titulo else ""
    src = f'<div class="out-src">{fonte}</div>' if fonte else ""
    dl = '<button type="button" class="dl-btn" title="Baixar CSV">⭳ CSV</button>' if csv_attr else ""
    attrs = f' data-csv="{csv_attr}" data-filename="{_esc(filename or "dados")}.csv"' if csv_attr else ""
    return f'<div class="out"{attrs}>{dl}{tit}<div id="{elem_id}"></div>{src}</div>'

FMT_MAP = {'int': 'v=>fmt(v)', 'pct': 'v=>pct(v)', 'pct1': 'v=>pct(v,1)',
           # 1 casa decimal sem '%' (taxas por 1.000/100 mil); fora de _eh_taxa_ou_percentual (sem remoção de outliers)
           'dec1': 'v=>fmt(v,1)', 'dec1f': 'v=>fmt(v,1)'}

def _normaliza(vals):
    """pandas/list -> list[float|None], NaN->None (para comparar/filtrar outliers)."""
    out = []
    for v in vals:
        if v is None or (isinstance(v, float) and math.isnan(v)) or pd.isna(v):
            out.append(None)
        else:
            out.append(float(v))
    return out

def line_chart(x, series, opts=None, fonte=None, titulo=None):
    opts = dict(opts or {})
    x_list = list(x)
    norm = [_normaliza(s['values']) for s in series]
    # outliers so em series percentual/taxa -- nao em contagem absoluta (specification.md §3.3, decisao O)
    limpos = [remove_outliers_tukey(v) if _eh_taxa_ou_percentual(s) else v for s, v in zip(series, norm)]
    has_outliers = any(c != n for c, n in zip(limpos, norm))

    def build(valores_por_serie):
        elem_id = new_id('c')
        js_series = []
        for s, vals in zip(series, valores_por_serie):
            fmt_fn = FMT_MAP.get(s.get('format', 'int'), FMT_MAP['int'])
            js_series.append(
                "{label:%s, values:%s, format:%s}" % (json.dumps(s['label'], ensure_ascii=False), json.dumps(vals), fmt_fn)
            )
        scripts.append(
            "lineChart(byId(%s), {x:%s, series:[%s], opts:%s});" % (
                json.dumps(elem_id), json.dumps(jsvals(x_list)), ",".join(js_series), json.dumps(opts)
            )
        )
        csv = _csv_data_attr(["Ano"] + [s['label'] for s in series],
                              [[x_list[i]] + [vv[i] for vv in valores_por_serie] for i in range(len(x_list))])
        parts.append(_out_div(elem_id, fonte, titulo, csv_attr=csv, filename=titulo or (series[0]['label'] if series else 'serie')))
        return elem_id

    if has_outliers:
        with_outliers_toggle(lambda: build(norm), lambda: build(limpos), True)
    else:
        build(norm)

def bar_chart(items, fonte=None, titulo=None, fmt='int'):
    norm = _normaliza([it['value'] for it in items])
    # outliers so em percentual/taxa -- nao em contagem absoluta (specification.md §3.3, decisao O)
    limpos = remove_outliers_tukey(norm) if _eh_taxa_ou_percentual(fmt) else norm
    has_outliers = limpos != norm

    def build(valores):
        elem_id = new_id('c')
        fmt_fn = FMT_MAP.get(fmt, FMT_MAP['int'])
        js_items = [
            "{label:%s, value:%s, format:%s}" % (json.dumps(str(it['label']), ensure_ascii=False), json.dumps(v), fmt_fn)
            for it, v in zip(items, valores) if v is not None
        ]
        scripts.append("barChart(byId(%s), {items:[%s]});" % (json.dumps(elem_id), ",".join(js_items)))
        csv = _csv_data_attr(["Categoria", "Valor"], [(it['label'], v) for it, v in zip(items, valores)])
        parts.append(_out_div(elem_id, fonte, titulo, csv_attr=csv, filename=titulo or 'barras'))
        return elem_id

    if has_outliers:
        with_outliers_toggle(lambda: build(norm), lambda: build(limpos), True)
    else:
        build(norm)

def grouped_bar_chart(groups, series, opts=None, fonte=None, titulo=None):
    opts = dict(opts or {})
    opts.setdefault('table', True)
    groups_list = [str(g) for g in groups]
    norm = [_normaliza(s['values']) for s in series]
    # outliers so em series percentual/taxa -- nao em contagem absoluta (specification.md §3.3, decisao O)
    limpos = [remove_outliers_tukey(v) if _eh_taxa_ou_percentual(s) else v for s, v in zip(series, norm)]
    has_outliers = any(c != n for c, n in zip(limpos, norm))

    def build(valores_por_serie):
        elem_id = new_id('c')
        js_series = []
        for s, vals in zip(series, valores_por_serie):
            fmt_fn = FMT_MAP.get(s.get('format', 'int'), FMT_MAP['int'])
            js_series.append(
                "{label:%s, values:%s, format:%s}" % (json.dumps(s['label'], ensure_ascii=False), json.dumps(vals), fmt_fn)
            )
        scripts.append(
            "groupedBarChart(byId(%s), {groups:%s, series:[%s], opts:%s});" % (
                json.dumps(elem_id), json.dumps(groups_list, ensure_ascii=False), ",".join(js_series), json.dumps(opts)
            )
        )
        csv = _csv_data_attr([""] + groups_list, [[s['label']] + vv for s, vv in zip(series, valores_por_serie)])
        parts.append(_out_div(elem_id, fonte, titulo, csv_attr=csv, filename=titulo or 'barras-agrupadas'))
        return elem_id

    if has_outliers:
        with_outliers_toggle(lambda: build(norm), lambda: build(limpos), True)
    else:
        build(norm)

def out_pair(fn1, fn2):
    """Wrap two chart-producing calls (each appending one .out div) as a side-by-side pair."""
    start = len(parts)
    fn1()
    fn2()
    pair_html = '<div class="out-pair">' + "".join(parts[start:]) + '</div>'
    del parts[start:]
    parts.append(pair_html)

def plain_table(df, fonte=None):
    html = df.to_html(index=False, classes="plain", border=0, na_rep="—", escape=True)
    html = html.replace(' class="dataframe plain"', ' class="plain"')
    src = f'<div class="out-src">{fonte}</div>' if fonte else ""
    parts.append(f'<div class="out"><div class="table-scroll">{html}</div>{src}</div>')

def series_from_cols(df, cols, labels=None, fmt='int'):
    return [{'label': (labels or {}).get(c, c), 'values': df[c].tolist(), 'format': fmt} for c in cols]

# -------------------------------------------------------- map image encode --

def map_card(png_name, caption, max_width=1400):
    img = Image.open(f"{MAPAS}/{png_name}").convert("RGB")
    if img.width > max_width:
        h = int(img.height * max_width / img.width)
        img = img.resize((max_width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=80, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f'<figure class="map-card"><img src="data:image/webp;base64,{b64}" alt="{caption}" loading="lazy"><figcaption class="map-cap">{caption}</figcaption></figure>'

def maps_block(imgs):
    """imgs: list of (filename, caption)."""
    parts.append('<div class="map-gallery">')
    for fn, caption in imgs:
        parts.append(map_card(fn, caption))
    parts.append('</div>')

available_maps = set(os.listdir(MAPAS))

def check_maps(imgs):
    missing = [fn for fn, _ in imgs if fn not in available_maps]
    if missing:
        raise SystemExit(f"missing map PNGs: {missing}")

# ------------------------------------------------ specs/relatorio-interativo --
# Outliers, option-card (pill selector), CSV download, institutional identity,
# and the SVG choropleth pipeline -- see specs/relatorio-interativo/plan.md.

def _esc(s):
    return str(s).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

def _fmt_ptbr(v, dec=0):
    if v is None:
        return "—"
    s = f"{v:,.{dec}f}"
    s = s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return s

# ---- texto de analise: lorem ipsum, por opcao (specs/relatorio-interativo/plan.md §10.3) --
# Placeholder deliberado (specification.md §3.4/§3.13): marca onde o texto real
# vai entrar depois, sem fabricar uma leitura analitica dos dados que ninguem
# validou. Deterministico por `seed` (o label da opcao) para o texto nao mudar
# a cada rodada de geracao -- facilita revisar diffs.
_LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam "
    "quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo "
    "consequat duis aute irure in reprehenderit voluptate velit esse cillum "
    "eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident "
    "sunt culpa qui officia deserunt mollit anim id est laborum curabitur "
    "vitae purus eget nunc porttitor sollicitudin nec eget metus vestibulum "
    "ante primis faucibus orci luctus posuere cubilia curae mauris blandit "
    "aliquet nibh praesent tristique senectus netus fames turpis egestas"
).split()

def _lorem(seed, palavras=None):
    rng = random.Random(seed)
    if palavras is None:
        # specs/ajuste_eixos/specs.md §7: faixa 100-200 palavras por bloco de
        # analise (era um valor fixo de 150 ate a rodada ajuste_eixos) --
        # RNG proprio (nao consome do `rng` de escolha de palavras acima) e
        # deterministico por seed, pra nao mudar a cada regeracao do relatorio.
        palavras = random.Random(f"{seed}-palavras").randint(100, 200)
    corpo = " ".join(rng.choice(_LOREM_WORDS) for _ in range(palavras))
    return corpo[:1].upper() + corpo[1:] + "."

_CAMINHO_TEXTOS_CURADOS = "relatorio/textos_curados.json"

def _carrega_textos_curados():
    p = Path(_CAMINHO_TEXTOS_CURADOS)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

_TEXTOS_CURADOS = _carrega_textos_curados()

def _texto_analise(seed, palavras=None):
    """Texto curado (relatorio/textos_curados.json) se houver, senão lorem.
    Texto curado é escapado e cada quebra de linha do DOCX (1 bookmark = 1
    parágrafo do Word, parágrafos extras viram <w:br/>) vira separação
    visual de parágrafo."""
    curado = _TEXTOS_CURADOS.get(seed)
    if not curado:
        return _lorem(seed, palavras)
    import html as _html
    return "<br><br>".join(_html.escape(t.strip()) for t in curado.split("\n") if t.strip())

def _lorem_bullets(seed, n=5, palavras=8):
    """n frases curtas (placeholder) para o bloco 'principais achados' --
    mesmo gerador deterministico do _lorem, seed derivado por indice."""
    return [_lorem(f"{seed}-kt-{i}", palavras) for i in range(n)]

def _eh_taxa_ou_percentual(s):
    """s: dict de serie ({'label','values','format',...}) ou a string do
    formato direto. Outliers so se aplicam a percentual/taxa, nao a
    contagem absoluta (specification.md §3.3, decisao O)."""
    fmt = s.get('format', 'int') if isinstance(s, dict) else s
    return fmt in ('pct', 'pct1', 'dec1')

def remove_outliers_tukey(valores):
    """valores: list[float|None]. Retorna list[float|None] do mesmo tamanho,
    outliers substituidos por None (mantem o eixo alinhado -- nao remove o
    ponto, so mascara o valor). Cercas de Tukey 1.5xIQR (specification.md §3.3).
    Series com menos de 4 pontos finitos voltam inalteradas (IQR pouco confiavel)."""
    finitos = [v for v in valores if v is not None]
    if len(finitos) < 4:
        return list(valores)
    s = pd.Series(finitos)
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [v if (v is None or (lo <= v <= hi)) else None for v in valores]

def _csv_data_attr(headers, rows):
    """Monta um CSV (pt-BR: ; como separador, , decimal) e devolve como atributo
    HTML data-csv já escapado -- o botao de download so precisa ler o atributo."""
    def cell(v):
        if v is None:
            return ""
        if isinstance(v, float):
            return _fmt_ptbr(v, 2 if v != int(v) else 0)
        return str(v).replace(';', ',')
    lines = [";".join(cell(h) for h in headers)]
    for r in rows:
        lines.append(";".join(cell(c) for c in r))
    return _esc("\n".join(lines))

def with_outliers_toggle(build_full, build_clean, has_outliers):
    """build_full/build_clean: funcoes sem argumento que emitem exatamente 1
    construto (1 chamada a line_chart/bar_chart/... -- 1 div .out) cada. Se
    has_outliers, envolve as duas em um card com toggle; senao so renderiza
    build_full (sem chrome de toggle morto numa serie sem outlier)."""
    if not has_outliers:
        build_full()
        return
    start = len(parts)
    build_full()
    full_html = "".join(parts[start:]); del parts[start:]
    build_clean()
    clean_html = "".join(parts[start:]); del parts[start:]
    parts.append(
        '<div class="outlier-card">'
        '<div class="outlier-toolbar"><button type="button" class="outlier-btn"><span class="outlier-x">×</span> Remover outliers</button></div>'
        f'<div class="outlier-pane" data-variant="full">{full_html}</div>'
        f'<div class="outlier-pane" data-variant="clean" hidden>{clean_html}</div>'
        '</div>'
    )

def option_card(entries, padrao='grafico'):
    """entries: list de (label, build_fn, seed_texto). build_fn emite
    exatamente 1 construto (pode por sua vez conter um outlier-card). Cada
    opcao ganha seu proprio bloco de texto (lorem ipsum, seed=seed_texto --
    determinístico, nao muda a cada geracao), que troca junto quando a pill
    muda (specification.md §3.13). padrao: 'grafico' (texto abaixo, largura
    total) | 'mapa' (texto na 3a coluna, ao lado). len==1 -> sem coluna de
    pills, texto ainda emitido (so nao ha nada para trocar)."""
    if len(entries) == 1:
        label, build_fn, seed = entries[0]
        start = len(parts)
        build_fn()
        html = "".join(parts[start:]); del parts[start:]
        parts.append(
            f'<div class="option-card option-card-{padrao} option-card-single">'
            f'<div class="opt-panes">{html}</div>'
            f'<div class="opt-texts"><div class="opt-text"><div class="opt-text-inner">{_texto_analise(seed)}</div></div></div>'
            '</div>'
        )
        return
    panes, texts, pills = [], [], []
    for i, (label, build_fn, seed) in enumerate(entries):
        start = len(parts)
        build_fn()
        html = "".join(parts[start:]); del parts[start:]
        panes.append(f'<div class="opt-pane"{" hidden" if i else ""}>{html}</div>')
        texts.append(f'<div class="opt-text"{" hidden" if i else ""}><div class="opt-text-inner">{_texto_analise(seed)}</div></div>')
        active = ' data-active="true"' if i == 0 else ''
        pills.append(f'<button type="button" class="pill"{active}>{_esc(label)}</button>')
    parts.append(
        f'<div class="option-card option-card-{padrao}">'
        '<div class="pill-col">' + "".join(pills) + '</div>'
        '<div class="opt-panes">' + "".join(panes) + '</div>'
        '<div class="opt-texts">' + "".join(texts) + '</div>'
        '</div>'
    )

def tabela_com_texto(build_fn, seed):
    """Padrao C (specification.md §3.13): texto a esquerda, tabela a
    direita -- unica ordem invertida em relacao aos padroes grafico/mapa.
    Sem pills nesta rodada (nenhuma tabela do relatorio tem corte
    alternativo ainda)."""
    start = len(parts)
    build_fn()
    html = "".join(parts[start:]); del parts[start:]
    parts.append(
        '<div class="table-with-text">'
        f'<div class="opt-text">{_lorem(seed)}</div>'
        f'<div class="opt-panes">{html}</div>'
        '</div>'
    )

def emite_bloco_pendente(titulo, nota):
    """Subsecao 'a reservar' (catalogo tem o indicador, analise.py ainda nao o
    implementa) -- specs/ajuste_eixos/specs.md §3-E: nunca uma secao vazia sem
    explicacao, sempre com o selo + a razao (Status da planilha). Mesmo
    padrao visual do key-takeaways (--surface-2), com um selo proprio para
    nao ser confundido com 'Principais achados'. Sem bloco de texto lorem --
    nao ha conteudo real a comentar ainda (specs.md §7)."""
    h3(titulo)
    parts.append(
        '<div class="pending-block">'
        '<div class="eyebrow pending-label">🚧 INDICADOR CATALOGADO, AINDA NÃO DISPONÍVEL</div>'
        f'<p>{_esc(nota)}</p>'
        '</div>'
    )

def nota_metodologica(texto):
    """Nota de limitação/qualidade de dado sob o h3 (ex.: quebra de série, denominador). Mesmo visual
    do pending-block, com selo próprio -- não é indicador pendente, é ressalva sobre um dado real."""
    parts.append(
        '<div class="pending-block pending-inline">'
        '<div class="eyebrow pending-label">ℹ️ NOTA METODOLÓGICA</div>'
        f'<p>{_esc(texto)}</p>'
        '</div>'
    )

# ---- institutional logo (embedded once, reused in navbar + footer) --------

# Bloco 2: arquivo em website/assets/images/, não mais base64 embutido.
LOGO_IMG = f'<img src="assets/images/ipp-logo.png" alt="Prefeitura do Rio de Janeiro — Instituto Pereira Passos" class="ipp-logo">'

# ---- SVG choropleth pipeline (Bloco 3) -------------------------------------
# Aplicado nesta rodada ao mapa do Censo por bairro (prova de conceito real,
# ver specs/relatorio-interativo/tasks.md T3.4) -- os demais ~30 mapas
# continuam como PNG (map_card acima) ate uma rodada de conversao mecanica.

# altura reduzida ~20% (560->448, pedido explicito do usuario) -- checado
# antes de aplicar: a altura de conteudo real do mapa (poligonos) e so
# ~335px dentro dos 560px originais (a largura e o eixo que restringe a
# escala, ja que a cidade e bem mais larga que alta), entao os 224px de
# margem em branco (topo+base) absorvem o corte sem cortar poligono algum
_MAP_W, _MAP_H = 640, 448
# 'censo' era 'Blues' (igual analise.py), depois 'Greys' -- agora 'Purples':
# azul e reservado exclusivamente pro mar/agua no fundo do mapa (nunca
# terra/dado), e o usuario pediu uma cor propria em vez de cinza tambem
_CMAP_TEMA = {'censo': 'Purples', 'natalidade': 'BuGn', 'mortalidade': 'RdPu', 'cadunico': 'YlOrBr', 'protecao': 'OrRd'}
_GEO_CACHE = {}

def _bounds_project(gdf, width, height, pad_frac=0.03):
    minx, miny, maxx, maxy = gdf.total_bounds
    cos_lat = math.cos(math.radians((miny + maxy) / 2))
    padx, pady = (maxx - minx) * pad_frac, (maxy - miny) * pad_frac
    minx -= padx; maxx += padx; miny -= pady; maxy += pady
    geo_w, geo_h = (maxx - minx) * cos_lat, (maxy - miny)
    scale = min(width / geo_w, height / geo_h) if geo_w and geo_h else 1
    off_x, off_y = (width - geo_w * scale) / 2, (height - geo_h * scale) / 2
    def project(lon, lat):
        x = (lon - minx) * cos_lat * scale + off_x
        y = height - ((lat - miny) * scale + off_y)
        return x, y
    # expostos para a barra de escala (metros reais) e o fundo cartografico
    # (posicionar o mosaico de tiles no mesmo espaco de pixels dos poligonos)
    project.bounds = (minx, miny, maxx, maxy)
    project.scale = scale  # px por grau ajustado por cos(lat) ~= px por grau de latitude real
    return project

_NIVEL_COL = {"ap": "area_plane", "rp": "cod_rp", "ra": "codra"}
_NIVEL_LABEL = {"ap": "AP", "rp": "RP", "cap": "CAP", "ra": "RA"}

def _geo_base_bairros():
    if "_base_bairro" not in _GEO_CACHE:
        import geopandas as gpd
        gdf = gpd.read_file("dados_locais/geo/limite_bairros_rio.geojson")
        gdf["codbairro"] = gdf["codbairro"].astype(int)
        _GEO_CACHE["_base_bairro"] = gdf
    return _GEO_CACHE["_base_bairro"]

def _geo_nivel(nivel):
    """nivel: 'bairro' | 'ap' | 'rp' | 'cap'. Retorna (gdf, project, nomes) cacheado.
    gdf tem 1 linha por unidade; `nomes` mapeia chave -> rotulo legivel para o
    tooltip. bairro/ap/rp vem do mesmo geojson de bairros (ap/rp via dissolve --
    mesmas colunas area_plane/cod_rp que mapa_coropletico_bairros usa em
    analise.py); cap tem geometria propria (limite_ap_saude_rio.geojson,
    fronteiras de saude da SMS-Rio, DIFERENTES das AP/RP de planejamento
    urbano do IPP apesar da numeracao parecida -- ver analise.py
    _CAMINHO_GEO_CAP)."""
    if nivel in _GEO_CACHE:
        return _GEO_CACHE[nivel]
    if nivel == "bairro":
        base = _geo_base_bairros()
        g = base.copy()
        g["_chave"] = g["codbairro"]
        nomes = dict(zip(g["_chave"], g["nome"]))
    elif nivel == "ra":
        # Região Administrativa: dissolve por codra (33 RAs, não existe a 32); rótulo = nome (regiao_adm)
        base = _geo_base_bairros()
        g = base.dissolve(by="codra", as_index=False)
        g["_chave"] = g["codra"].astype(int)
        nomes = {int(c): str(n).strip().title() for c, n in base.drop_duplicates("codra")[["codra", "regiao_adm"]].values}
    elif nivel in ("ap", "rp"):
        base = _geo_base_bairros()
        col = _NIVEL_COL[nivel]
        g = base.dissolve(by=col, as_index=False)
        g["_chave"] = g[col].astype(str) if nivel == "rp" else g[col].astype(int)
        nomes = {c: f"{_NIVEL_LABEL[nivel]} {c}" for c in g["_chave"]}
    elif nivel == "cap":
        import geopandas as gpd
        g = gpd.read_file("dados_locais/geo/limite_ap_saude_rio.geojson")
        g["_chave"] = g["cod_ap_sms"].astype(float).astype(str)
        nomes = {c: f"CAP {c}" for c in g["_chave"]}
    else:
        raise ValueError(f"nivel desconhecido: {nivel}")
    result = (g, _bounds_project(g, _MAP_W, _MAP_H), nomes)
    _GEO_CACHE[nivel] = result
    return result

# ---- geometria compartilhada (specs/website_refactor Blocos 3/3b) ------------
# Antes: cada mapa (e cada variante "sem outliers") repetia o `d` de todas as
# regiões -- 7.107 <path>, 20 MB. Agora cada região de cada nível vira UM
# <path id="geo-..."> em data/geo.js e o mapa só tem <use href="#geo-..." fill=...>.
# A geometria é simplificada como cobertura (shapely.coverage_simplify: fronteira
# compartilhada simplificada uma vez só, sem fresta entre vizinhos) já no espaço
# de pixels do SVG. Tolerância 0,3 unidade (< meio pixel na largura exibida):
# 1,44 MB -> 0,24 MB nos 5 níveis, nenhum anel (ilha) perdido, área -0,01%.
_GEO_TOL = 0.3
_GEO_DEFS = {}    # nivel -> {chave: (def_id, d)}
_GEO_USADOS = {}  # nivel -> [(def_id, nome, d)] na ordem do geojson, só níveis usados
_GEO_PREFIXO = {"bairro": "b", "ap": "a", "rp": "r", "ra": "x", "cap": "c"}

def _num_svg(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    if s.startswith("0."):
        s = s[1:]
    elif s.startswith("-0."):
        s = "-" + s[2:]
    return "0" if s in ("", "-0", "-") else s

def _path_d_relativo(geom):
    """`d` compacto: M absoluto + l relativo por anel, 1 casa decimal. Deltas
    calculados sobre as coordenadas já arredondadas (sem acúmulo de erro)."""
    polys = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
    aneis = []
    for poly in polys:
        aneis.append(poly.exterior.coords)
        aneis.extend(i.coords for i in poly.interiors)
    out = []
    for coords in aneis:
        pts = [(round(x, 1), round(y, 1)) for x, y in coords][:-1]
        if not pts:
            continue
        pts = [pts[0]] + [p for a, p in zip(pts, pts[1:]) if p != a]
        seg, prev = "", pts[0]
        for p in pts[1:]:
            a, b = _num_svg(round(p[0] - prev[0], 1)), _num_svg(round(p[1] - prev[1], 1))
            prev = p
            seg += (a if (not seg or a.startswith("-")) else " " + a) + (b if b.startswith("-") else "," + b)
        out.append(f"M{_num_svg(pts[0][0])},{_num_svg(pts[0][1])}" + (f"l{seg}" if seg else "") + "z")
    return "".join(out)

def _geo_defs(nivel):
    if nivel not in _GEO_DEFS:
        import numpy as np
        import shapely
        from shapely.ops import transform as _shp_transform
        g, project, nomes = _geo_nivel(nivel)
        px = np.array([_shp_transform(lambda x, y, z=None: project(x, y), geom) for geom in g.geometry.values])
        simp = shapely.coverage_simplify(px, _GEO_TOL)
        defs = {}
        for chave, geom in zip(g["_chave"], simp):
            # id curto (repetido em ~7 mil <use>): g + letra do nível + chave (ex. gb12, gr1_1, gc1_0)
            def_id = "g" + _GEO_PREFIXO[nivel] + re.sub(r"[^0-9A-Za-z]", "_", str(chave))
            defs[chave] = (def_id, _path_d_relativo(geom))
        _GEO_DEFS[nivel] = defs
        _GEO_USADOS[nivel] = [(defs[c][0], str(nomes.get(c, c)), defs[c][1]) for c in g["_chave"]]
    return _GEO_DEFS[nivel]

def _cor_sequencial(tema, frac):
    import matplotlib
    r, g, b, _ = matplotlib.colormaps[_CMAP_TEMA[tema]](0.22 + 0.68 * max(0.0, min(1.0, frac)))
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))

def _chave_norm(v, nivel):
    if nivel == "bairro":
        return int(v)
    if nivel == "ap":
        return int(v)
    if nivel == "rp":
        return str(v)
    if nivel == "cap":
        return str(float(v))
    if nivel == "ra":
        return int(v)
    raise ValueError(nivel)

# ---- fundo cartografico real (Esri Ocean Basemap, mesmo provedor do PNG em
# analise.py) ----
# Restaurado apos uma rodada que removeu isso por preocupacao com terra
# aparecer azul -- esclarecido pelo usuario: o problema era o CHOROPLETH dos
# dados (censo em tons de azul, agora 'Greys') representar TERRA em azul, nao
# o basemap em si. O basemap real pode voltar; so os dados (shapefile
# colorido por valor) nunca usam azul.
_BASEMAP_CACHE = {}   # bbox (arredondado) -> (classe css, b64 jpeg)
_BASEMAP_CSS_RULES = []
_BASEMAP_FILES = {}   # nome do arquivo -> bytes JPEG (gravados em assets/images/ no fim)

def _merc_para_lonlat(mx, my):
    r = 20037508.342789244
    lon = mx / r * 180
    lat = math.degrees(math.atan(math.sinh(my / r * math.pi)))
    return lon, lat

def _basemap_css_class(project):
    """Busca (1x, cacheado por bbox) um mosaico de tiles Esri Ocean Basemap
    cobrindo os limites geograficos de `project` e reamostra pra caber
    EXATAMENTE no espaco de pixels do SVG (mesma bbox/escala usada pelos
    poligonos) -- resultado widthxheight identico a _MAP_W/_MAP_H, aplicado
    como CSS background compartilhado (1 copia do base64, nao 1 por mapa)."""
    minx, miny, maxx, maxy = project.bounds
    key = (round(minx, 4), round(miny, 4), round(maxx, 4), round(maxy, 4))
    if key in _BASEMAP_CACHE:
        return _BASEMAP_CACHE[key][0]
    # specs/website_refactor Bloco 3: JPEG em assets/images/ (antes base64 no <style>), nome
    # derivado da bbox. Se o arquivo já existe em website/, é reaproveitado sem rede -- saída
    # estável entre execuções (antes o JPEG mudava a cada download) e geração offline.
    import hashlib
    arquivo = "basemap-" + hashlib.md5(repr(key).encode()).hexdigest()[:8] + ".jpg"
    class_name = f"map-bg-{len(_BASEMAP_CACHE) + 1}"
    existente = Path("website/assets/images") / arquivo
    if existente.exists():
        _BASEMAP_FILES[arquivo] = existente.read_bytes()
        _BASEMAP_CSS_RULES.append(f'.{class_name}{{background-image:url(assets/images/{arquivo});background-size:100% 100%;}}')
        _BASEMAP_CACHE[key] = (class_name, None)
        return class_name
    try:
        import contextily as ctx
        import numpy as np
        # zoom 10 -- checado manualmente: o Esri Ocean Basemap so tem cobertura real
        # de terreno pra area do Rio ate zoom ~10; zoom 11+ devolve um tile placeholder
        # cinza-azulado com o texto 'Map data not yet available' (bytes identicos em
        # zoom 11 e 13, confirmado por probe manual dos tiles) -- e um basemap voltado
        # a oceano/costa, a cobertura terrestre em alta resolucao nao acompanha
        # o serviço 'Ocean_Basemap' da Esri responde HTTP 500 (2026-09); o sucessor 'Ocean/World_Ocean_Base' tem o mesmo
        # estilo e serve os tiles (mesma solução de _PROVEDORES_FUNDO['mapa_oceano_base'] em analise.py)
        import xyzservices
        fundo_oceano = xyzservices.TileProvider(
            name='Esri.WorldOceanBase',
            url='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
            attribution='Tiles © Esri', max_zoom=13)
        img, ext = ctx.bounds2img(minx, miny, maxx, maxy, zoom=10, source=fundo_oceano, ll=True)
        mx0, mx1, my0, my1 = ext
        lon0, lat0 = _merc_para_lonlat(mx0, my0)
        lon1, lat1 = _merc_para_lonlat(mx1, my1)
        tile_img = Image.fromarray(np.asarray(img)).convert("RGB")
        x0, y1 = project(lon0, lat0)
        x1, y0 = project(lon1, lat1)
        w, h = max(1, round(x1 - x0)), max(1, round(y1 - y0))
        tile_img = tile_img.resize((w, h), Image.LANCZOS)
        canvas = Image.new("RGB", (_MAP_W, _MAP_H), "#eef3f6")
        canvas.paste(tile_img, (round(x0), round(y0)))
        buf = io.BytesIO()
        canvas.save(buf, format="JPEG", quality=72)
        _BASEMAP_FILES[arquivo] = buf.getvalue()
        _BASEMAP_CSS_RULES.append(
            f'.{class_name}{{background-image:url(assets/images/{arquivo});background-size:100% 100%;}}'
        )
    except Exception as exc:
        class_name = ""
        # sem internet/timeout etc -- mapa cai de volta pro fundo neutro
        # (--surface-2 em .map-svg-frame), nao trava a geracao do relatorio inteiro
        print(f"[aviso] fundo cartografico indisponivel para bbox {key}: {exc}", file=sys.stderr)
    _BASEMAP_CACHE[key] = (class_name, None)
    return class_name

def _escala_legivel(distancia_m):
    """Arredonda pra 1/2/5 x 10^n mais proximo -- convencao de barra de escala."""
    if distancia_m <= 0:
        return 100
    exp = math.floor(math.log10(distancia_m))
    base = distancia_m / (10 ** exp)
    nice = 1 if base < 1.5 else 2 if base < 3.5 else 5 if base < 7.5 else 10
    return nice * (10 ** exp)

def _svg_barra_escala(project, x=16, y=None):
    """Barra de escala SVG (canto inferior esquerdo), distancia real calculada a
    partir de project.scale (px por grau ~= px por metro via 111.320m/grau)."""
    y = _MAP_H - 14 if y is None else y
    px_por_m = project.scale / 111320.0
    nice_m = _escala_legivel(110 / px_por_m)
    bar_px = nice_m * px_por_m
    label = f"{nice_m / 1000:.0f} km" if nice_m >= 1000 else f"{nice_m:.0f} m"
    return (
        f'<g class="map-scalebar" transform="translate({x},{y})">'
        f'<rect x="0" y="-4" width="{bar_px:.1f}" height="4" fill="#262626"></rect>'
        f'<rect x="0" y="-4" width="{bar_px:.1f}" height="4" fill="none" stroke="#fff" stroke-width="0.6"></rect>'
        f'<text x="{bar_px / 2:.1f}" y="-8" text-anchor="middle" class="map-scalebar-label">{label}</text>'
        '</g>'
    )

def _svg_rosa_dos_ventos(x=None, y=30):
    """Seta 'N' simples (rosa dos ventos), canto superior direito -- mesma ideia
    de _adiciona_rosa_dos_ventos em analise.py."""
    x = _MAP_W - 30 if x is None else x
    return (
        f'<g class="map-compass" transform="translate({x},{y})">'
        '<path d="M0,-16 L6,6 L0,1.5 L-6,6 Z" fill="#262626" stroke="#fff" stroke-width="0.8"></path>'
        '<text x="0" y="20" text-anchor="middle" class="map-compass-label">N</text>'
        '</g>'
    )

def mapa_svg(df, chave_col, valor_col, tema, titulo, legenda_titulo, fonte_dados, bins=None, fmt="int", nivel="bairro", teto=None, zero_branco=False,
             col_suprimido=None, rotulo_suprimido="suprimido (< 20)", col_extra=None, rotulo_extra=""):
    """`col_extra` (populacao-referencia D1): coluna percentual opcional de `df` mostrada no tooltip ao lado do
    valor, como "1.234 (1,9% do município)" com `rotulo_extra`; None (padrão) não muda nada.
    `teto`: limite superior só da escala de cor contínua (valores acima usam a cor máxima; o tooltip mostra o real).
    `col_suprimido` (specs/recortes_cadunico §5): coluna booleana de `df` marcando regiões suprimidas por
    privacidade (valor já vazio na tabela) -- o tooltip mostra `rotulo_suprimido` em vez de "—" e a legenda
    ganha uma linha própria. None (padrão) = comportamento anterior, usado pelos demais mapas.
    `zero_branco` (só com `bins`): valor 0 vira branco, com linha própria "0 (sem casos)" na legenda.
    df: 1 linha por unidade geografica (chave_col identifica a unidade no nivel
    escolhido: codbairro/area_plane/cod_rp/cod_ap_sms). bins: lista de limites
    superiores (contagem absoluta, classes discretas) ou None (percentual/taxa,
    escala continua) -- mesma convencao de mapa_coropletico_bairros em
    analise.py. Emite 1 construto (option_card-compativel) com SVG + legenda +
    tooltip por regiao + toggle de outliers + download CSV."""
    gdf, project, nomes = _geo_nivel(nivel)
    defs = _geo_defs(nivel)
    valores = {}
    suprimidas = set()
    extras = {}
    for _, r in df.iterrows():
        try:
            chave = _chave_norm(r[chave_col], nivel)
        except (ValueError, TypeError):
            continue  # linhas de agregado tipo "Em branco"/"Ignorado" (nao sao uma unidade geografica real)
        valores[chave] = None if pd.isna(r[valor_col]) else float(r[valor_col])
        if col_extra is not None and not pd.isna(r[col_extra]):
            extras[chave] = float(r[col_extra])
        if col_suprimido is not None and bool(r[col_suprimido]):
            suprimidas.add(chave)
    brutos = list(valores.values())
    # outliers so em percentual/taxa -- nao em contagem absoluta (specification.md §3.3, decisao O)
    limpos = remove_outliers_tukey(brutos) if _eh_taxa_ou_percentual(fmt) else brutos
    limpos_map = dict(zip(valores.keys(), limpos))
    has_outliers = limpos != brutos

    def build(valor_por_regiao):
        elem_id = new_id("m")
        finitos = [v for v in valor_por_regiao.values() if v is not None]
        vmin, vmax = (min(finitos), max(finitos)) if finitos else (0, 1)
        if teto is not None:
            vmax = min(vmax, teto)
        paths, rows = [], []
        for _, row in gdf.iterrows():
            chave = row["_chave"]
            v = valor_por_regiao.get(chave)
            if v is None:
                fill = "var(--surface-2)"
            elif bins is not None and zero_branco and v == 0:
                fill = "#ffffff"
            elif bins is not None:
                idx = next((i for i, edge in enumerate(bins) if v <= edge), len(bins))
                fill = _cor_sequencial(tema, (idx + 1) / (len(bins) + 1))
            else:
                frac = (min(v, vmax) - vmin) / (vmax - vmin) if vmax > vmin else 0.5
                fill = _cor_sequencial(tema, frac)
            label = nomes.get(chave, str(chave))
            val_txt = _fmt_ptbr(v, 1 if fmt in ("pct1", "dec1") else 0) + ("%" if fmt == "pct1" and v is not None else "")
            if v is not None and chave in extras:
                val_txt += f" ({_fmt_ptbr(extras[chave], 1)}% {rotulo_extra})".replace(" )", ")")
            if chave in suprimidas:
                val_txt = rotulo_suprimido
            # geometria em data/geo.js (<path id>), nome da região em window.GEO_NOMES;
            # stroke/fill-opacity no CSS (`.map-svg use`) -- aqui só o que muda por mapa
            paths.append(f'<use href="#{defs[chave][0]}" fill="{fill}" data-v="{_esc(val_txt)}"></use>')
            rows.append((label, v))
        legend_bits = []
        if bins is not None:
            if zero_branco:
                legend_bits.append('<div class="map-legend-row"><span class="map-legend-sw" style="background:#ffffff;border:1px solid var(--ink-3, #888)"></span>0 (sem casos)</div>')
            edges = [None] + bins + [None]
            for i in range(len(bins) + 1):
                lo, hi = edges[i], edges[i + 1]
                lbl = f"Até {_fmt_ptbr(hi)}" if lo is None else (f"Mais de {_fmt_ptbr(lo)}" if hi is None else f"{_fmt_ptbr(lo)} a {_fmt_ptbr(hi)}")
                sw = _cor_sequencial(tema, (i + 1) / (len(bins) + 1))
                legend_bits.append(f'<div class="map-legend-row"><span class="map-legend-sw" style="background:{sw}"></span>{lbl}</div>')
        else:
            steps = 5
            for i in range(steps):
                frac = i / (steps - 1)
                v = vmin + (vmax - vmin) * frac
                sw = _cor_sequencial(tema, frac)
                legend_bits.append(f'<div class="map-legend-row"><span class="map-legend-sw" style="background:{sw}"></span>{"≥ " if teto is not None and i == steps - 1 else ""}{_fmt_ptbr(v, 1)}{"%" if fmt == "pct1" else ""}</div>')
        if suprimidas:
            legend_bits.append('<div class="map-legend-row"><span class="map-legend-sw" style="background:var(--surface-2);border:1px solid var(--ink-3, #888)"></span>'
                               f'Sem dado / {_esc(rotulo_suprimido)}</div>')
        bg_class = _basemap_css_class(project)
        overlay = _svg_rosa_dos_ventos() + _svg_barra_escala(project)
        svg = (
            f'<svg viewBox="0 0 {_MAP_W} {_MAP_H}" class="map-svg {bg_class}" id="{elem_id}">'
            + "".join(paths) + overlay + "</svg>"
        )
        csv = _csv_data_attr([_NIVEL_LABEL.get(nivel, "Bairro"), legenda_titulo or valor_col], rows)
        # estilo cartografico (specification.md §7): fundo real (Esri Ocean Basemap,
        # igual ao PNG) -- azul fica reservado ao mar/basemap, o choropleth dos DADOS
        # (censo etc.) nunca usa azul (Greys/BuGn/RdPu/YlOrBr). Rosa dos ventos + barra
        # de escala, titulo serifado, legenda como overlay DENTRO do mapa + rodape com
        # sistema de referencia (convencao do PNG).
        ref_txt = "Sistema de referência: SIRGAS 2000, UTM - Fuso 23S"
        parts.append(
            f'<div class="out map-svg-card" data-csv="{csv}" data-filename="{_esc(titulo)}.csv">'
            '<button type="button" class="dl-btn" title="Baixar CSV">⭳ CSV</button>'
            f'<div class="map-title">{_esc(titulo)}</div>'
            '<div class="map-svg-frame">'
            f'{svg}'
            f'<div class="map-legend-overlay"><div class="eyebrow map-legend-title">{_esc(legenda_titulo or "")}</div>{"".join(legend_bits)}</div>'
            '</div>'
            f'<div class="map-ref">{ref_txt}<br>Fonte: {_esc(fonte_dados)}</div>'
            '</div>'
        )
        return elem_id

    if has_outliers:
        with_outliers_toggle(lambda: build(valores), lambda: build(limpos_map), True)
    else:
        build(valores)

# ============================================================ NAVBAR/HEADER ==

# Faixa de aviso "em desenvolvimento" -- publicação de teste no GitHub Pages
# (repositório passou a ser público). Remover só quando o relatório for
# considerado pronto para divulgação oficial -- ver specs/roadmap.md
# "publicar_teste_pages".
parts.append(
    '<div class="dev-banner" role="alert">'
    '⚠️ EM DESENVOLVIMENTO / TEMPORÁRIO — esta é uma versão de teste do relatório, '
    'publicada para validação interna. Conteúdo, dados e layout ainda podem mudar.'
    '</div>'
)

parts.append('<div class="topbar-accent"></div>')
parts.append('<nav class="navbar"><div class="navbar-inner">')
parts.append(
    '<button type="button" class="navbar-burger" id="navbar-burger" aria-expanded="false" aria-controls="navbar-menu">'
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square">'
    '<line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line>'
    '</svg><span class="eyebrow navbar-label">NAVEGAÇÃO</span></button>'
)
parts.append(f'<div class="navbar-logo">{LOGO_IMG}</div>')
parts.append('</div></nav>')
parts.append('<div class="navbar-menu" id="navbar-menu" hidden><!--NAVBAR--></div>')

parts.append('<header class="doc-head">')
parts.append('<div class="doc-head-row">')
parts.append('<div class="doc-head-title">')
parts.append('<div class="eyebrow doc-eyebrow">PROJETO · RELATÓRIO INTERATIVO</div>')
parts.append('<h1><span class="glyph">\U0001F3DB️</span>Análise Primeira Infância Carioca</h1>')
parts.append('</div>')
parts.append('<div class="doc-head-desc">')
parts.append('<p class="sub">Visualizações dos indicadores de primeira infância (0 a 6 anos) do município do Rio de Janeiro. Cada gráfico tem a fonte no rodapé e uma opção de ver os dados em tabela; a descrição metodológica completa fica no notebook (<code>analise.py</code>) e no relatório em PDF.</p>')
parts.append('<p class="meta"><span id="gen-date">—</span></p>')
parts.append('</div>')
parts.append('</div>')
parts.append('<div class="spectrum-bar">' + "".join(f'<span style="background:var(--c{i})"></span>' for i in range(1, 12)) + '</div>')
parts.append('</header>')

# ---- sumario + introducao (specs/ajuste_eixos, pedido do usuario) --------
# O Sumario antigo (com ancoras h2+h3) foi removido em specification.md v6
# em favor da navbar persistente (relatorio/specs.md linha ~175); a CSS
# .toc/.toc-list ficou no arquivo sem uso desde entao. Reativada aqui, nao
# reescrita -- convive com a navbar (motivos diferentes: navbar e navegacao
# rapida sempre visivel, Sumario e a abertura formal do documento). Preenchido
# via placeholder (mesmo padrao do <!--NAVBAR-->) porque os ids das secoes so
# existem depois que h2()/h3() rodam mais abaixo no script.
parts.append(
    '<section class="doc-toc" aria-label="Sumário">'
    '<div class="toc">'
    '<div class="toc-label">SUMÁRIO</div>'
    '<ul class="toc-list"><!--SUMARIO--></ul>'
    '</div>'
    '</section>'
)
# Introducao: bloco placeholder (lorem ipsum, 250 palavras fixas -- nao a
# faixa 100-200 dos blocos de analise por visualizacao, specs.md §7; texto
# final e' trabalho de curadoria futura, fora do escopo desta rodada) com
# <h2> real só para herdar a tipografia/first-of-type do CSS -- não passa
# por h2() de proposito (não deve virar seção retrátil, nem entrar na
# navbar/Sumário listando a si mesma).
parts.append(
    '<section class="doc-intro" id="introducao">'
    '<h2>Introdução</h2>'
    # texto curado sob o bookmark "introducao" do DOCX, se já sincronizado
    f'<p class="lede">{_TEXTOS_CURADOS.get("introducao") and _texto_analise("introducao") or _lorem("introducao-relatorio", 250)}</p>'
    '</section>'
)

# ============================================================== PRIORIDADE ==

h2('🎯 Prioridade (sem secundário)')

h3('Por bairro')
df_censo_bairro = read("censo_por_bairro.csv")
top10 = df_censo_bairro.sort_values("0 a 4 anos", ascending=False).head(10)[["bairro", "0 a 4 anos", "Percentual 0 a 4"]]
top10 = top10.rename(columns={"bairro": "Bairro", "0 a 4 anos": "Crianças 0-4", "Percentual 0 a 4": "% do bairro"})
top10["% do bairro"] = top10["% do bairro"].map(lambda v: f"{v:.1f}%".replace(".", ","))
FONTE_CENSO = "Censo Demográfico 2022 (IBGE/Data.Rio)"
tabela_com_texto(lambda: plain_table(top10, fonte=FONTE_CENSO), "Top 10 bairros por população 0-4 anos")

h3('Mapas')

def _agrega_censo_por_nivel(df_bairro, nivel):
    """Agrega censo por bairro para AP/RP, somando o absoluto e recompondo o
    percentual a partir da soma (nao a media das taxas por bairro) -- mesma
    logica de agrega_bairros_por_nivel em analise.py. 'Total' (denominador) nao
    vem exportado em censo_por_bairro.csv; recuperado por algebra exata
    (Total = absoluto / (percentual/100)) a partir das 2 colunas que ja
    existem -- nao e uma aproximacao, e a mesma conta invertida."""
    base = _geo_base_bairros()
    col = _NIVEL_COL[nivel]
    mapa_nivel = dict(zip(base["codbairro"], base[col]))
    d = df_bairro.copy()
    d["_nivel"] = d["codbairro"].map(mapa_nivel)
    d["_total"] = d["0 a 4 anos"] / (d["Percentual 0 a 4"] / 100)
    agg = d.groupby("_nivel", as_index=False)[["0 a 4 anos", "_total"]].sum()
    agg["Percentual 0 a 4"] = agg["0 a 4 anos"] / agg["_total"] * 100
    return agg.rename(columns={"_nivel": col})

NIVEIS_PLANEJAMENTO = {
    'ap': {'nome': 'Área de Planejamento', 'bins': [25000, 50000, 75000, 100000]},
    'rp': {'nome': 'Região de Planejamento', 'bins': [12000, 18000, 24000, 30000]},
}
_entries_mapas_censo_abs = [
    ("Bairro", lambda: mapa_svg(df_censo_bairro, "codbairro", "0 a 4 anos", "censo",
        "Crianças de 0 a 4 anos, por bairro (Censo 2022)", "Crianças 0-4", FONTE_CENSO, bins=[1000, 2500, 5000, 10000]), "mapa_censo_0_4_absoluto"),
]
_entries_mapas_censo_pct = [
    ("Bairro", lambda: mapa_svg(df_censo_bairro, "codbairro", "Percentual 0 a 4", "censo",
        "% de crianças de 0 a 4 anos, por bairro (Censo 2022)", "% 0-4 anos", FONTE_CENSO, fmt='pct1'), "mapa_censo_0_4_percentual"),
]
for _nivel, _info in NIVEIS_PLANEJAMENTO.items():
    df_censo_nivel = _agrega_censo_por_nivel(df_censo_bairro, _nivel)
    _l1 = _info['nome']
    _entries_mapas_censo_abs.append((_l1, lambda df=df_censo_nivel, nivel=_nivel, info=_info: mapa_svg(
        df, _NIVEL_COL[nivel], "0 a 4 anos", "censo",
        f"Crianças de 0 a 4 anos, por {info['nome']} (Censo 2022)", "Crianças 0-4",
        FONTE_CENSO, bins=info['bins'], nivel=nivel), f"{_l1} · Absoluto"))
    _l2 = _info['nome']
    _entries_mapas_censo_pct.append((_l2, lambda df=df_censo_nivel, nivel=_nivel, info=_info: mapa_svg(
        df, _NIVEL_COL[nivel], "Percentual 0 a 4", "censo",
        f"% de crianças de 0 a 4 anos, por {info['nome']} (Censo 2022)", "% da população",
        FONTE_CENSO, fmt='pct1', nivel=nivel), f"{_l2} · %"))
# 6 mapas era demais numa unica fileira de pills -- dividido em 2 grupos
# (Absoluto / %), specification.md §9 revisao
h5('Valores absolutos')
option_card(_entries_mapas_censo_abs, 'mapa')
h5('Percentual')
option_card(_entries_mapas_censo_pct, 'mapa')

h3('Série temporal')
df_censo_serie = read("censo_0_a_4_anos_por_ano.csv")
option_card([
    ("Total/Feminino/Masculino", lambda: line_chart(df_censo_serie["ano"], [
        {'label': 'Total 0–4 anos', 'values': df_censo_serie['0 a 4 anos']},
        {'label': 'Feminino', 'values': df_censo_serie['Sexo feminino, 0 a 4 anos']},
        {'label': 'Masculino', 'values': df_censo_serie['Sexo masculino, 0 a 4 anos']},
    ], opts={'height': 230, 'maxXLabels': 3, 'table': True}, fonte="censo_0_a_4_anos_por_ano.csv (Tabela 2974/IBGE)"), "censo_0_a_4_serie_total_ano"),
    ("% 0-4 anos", lambda: line_chart(df_censo_serie["ano"], [
        {'label': 'Percentual 0–4 anos', 'values': df_censo_serie['Percentual 0 a 4 anos'], 'format': 'pct1'},
    ], opts={'height': 200, 'zeroBase': False, 'maxXLabels': 3, 'table': True}, fonte="censo_0_a_4_anos_por_ano.csv (Tabela 2974/IBGE)"), "censo_0_a_4_serie_percentual_ano"),
], 'grafico')

# populacao-referencia A2/D2: série anual Ripsa (item "Crianças até 6 anos (número)")
h3('População de 0 a 6 anos por ano (estimativas Ripsa/MS)')
nota_metodologica(
    "Estimativas populacionais da Ripsa/Ministério da Saúde, que corrigem a subcontagem de crianças pequenas do Censo 2022 — "
    "por isso os valores ficam acima dos do Censo e não se comparam diretamente com eles. Só existem para o município como um todo."
)
FONTE_RIPSA = "Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025)"
df_pop_ripsa = read("populacao_ripsa_0_a_6_por_ano.csv")
option_card([
    ("0 a 6 anos", lambda: line_chart(df_pop_ripsa["ano"], [{'label': 'População de 0 a 6 anos', 'values': df_pop_ripsa['populacao_0_a_6']}],
        opts={'height': 220, 'maxXLabels': 8, 'table': True}, fonte=FONTE_RIPSA), "populacao_ripsa_0_a_6_por_ano"),
    ("% da população", lambda: line_chart(df_pop_ripsa["ano"], [{'label': '% de 0 a 6 anos na população', 'values': df_pop_ripsa['percentual_0_a_6'], 'format': 'pct1'}],
        opts={'height': 200, 'zeroBase': False, 'maxXLabels': 8, 'table': True}, fonte=FONTE_RIPSA), "populacao_ripsa_0_a_6_percentual_por_ano"),
], 'grafico')

FONTE_DATASUS = "DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro"

RACA_LABEL = {"amarela": "Amarela", "branca": "Branca", "indigena": "Indígena", "parda": "Parda", "preta": "Preta", "nao_informado": "Não informado"}
RACAS = list(RACA_LABEL)
df_nv = read("nascidos_vivos_por_ano.csv")
df_bp = read("nascidos_abaixo_peso_por_ano.csv")
df_raca = read("mortalidade_raca_municipio_ano.csv")

h3('Nascidos vivos e mortalidade por raça/cor')
option_card([
    ("Nascidos vivos", lambda: line_chart(df_nv["ano"], [{'label': 'Nascidos vivos', 'values': df_nv['nascidos vivos']}], opts={'height': 220, 'table': True}, fonte=FONTE_DATASUS), "nascidos_vivos_por_ano"),
    ("Óbitos raça · Absoluto", lambda: line_chart(df_raca["ano"], series_from_cols(df_raca, [f"obitos_{r}" for r in RACAS], {f"obitos_{r}": RACA_LABEL[r] for r in RACAS}), opts={'height': 260, 'table': True}, fonte=FONTE_DATASUS), "obitos_raca_ano"),
    ("Óbitos raça · %", lambda: line_chart(df_raca["ano"], series_from_cols(df_raca, [f"percentual_{r}" for r in RACAS], {f"percentual_{r}": RACA_LABEL[r] for r in RACAS}, fmt='pct1'), opts={'height': 260, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS), "percentual_mortalidade_raca_ano"),
], 'grafico')

h3('Mapas')
df_map_nv = read("tabela_mapa_nascidos_vivos_2025.csv")
df_map_raca_2025 = read("mortalidade_raca_bairro_ano.csv").pipe(lambda d: d[d["ano"] == 2025])
option_card([
    ("Nascidos vivos", lambda: mapa_svg(df_map_nv, "codigo", "nascidos vivos", "natalidade",
        "Nascidos vivos por bairro (2025)", "Nascidos vivos", FONTE_DATASUS, bins=[200, 400, 800, 1500],
        col_extra="percentual_do_municipio", rotulo_extra="do município"), "mapa_nascidos_vivos_bairro_2025"),
    ("Óbitos 0-364 dias", lambda: mapa_svg(df_map_raca_2025, "codigo", "obitos_total", "mortalidade",
        "Óbitos de 0 a 364 dias por bairro (2025)", "Óbitos", FONTE_DATASUS, bins=[2, 5, 10, 20]), "mapa_obitos_raca_total_bairro_2025"),
    ("Taxa mortalidade infantil", lambda: mapa_svg(df_map_raca_2025, "codigo", "percentual_total", "mortalidade",
        "Taxa de mortalidade infantil (0-364 dias) por bairro (2025)", "% s/ nascidos vivos", FONTE_DATASUS, fmt="pct1"), "mapa_taxa_obitos_raca_total_bairro_2025"),
], 'mapa')

h3('Gravidez e puerpério')
df_grav = read("obitos_gravidez_por_ano.csv")
df_puerp = read("obitos_puerperio_por_ano.csv")
option_card([
    ("Gravidez", lambda: line_chart(df_grav["ano"], [{'label': 'Óbitos', 'values': df_grav['óbitos-gravidez']}], opts={'height': 200, 'table': True}, fonte=FONTE_DATASUS), "obitos_gravidez_por_ano"),
    ("Puerpério", lambda: line_chart(df_puerp["ano"], [{'label': 'Óbitos', 'values': df_puerp['óbitos-puerpério']}], opts={'height': 200, 'table': True}, fonte=FONTE_DATASUS), "obitos_puerperio_por_ano"),
], 'grafico')
df_map_grav = read("obitos_gravidez_bairro_ano.csv")
df_map_grav_2025 = df_map_grav[df_map_grav["ano"] == 2025]
df_map_puerp = read("obitos_puerperio_bairro_ano.csv")
df_map_puerp_2025 = df_map_puerp[df_map_puerp["ano"] == 2025]
option_card([
    ("Gravidez", lambda: mapa_svg(df_map_grav_2025, "codigo", "óbitos-gravidez", "mortalidade",
        "Óbitos durante a gravidez por bairro (2025)", "Óbitos", FONTE_DATASUS, bins=[0, 1]), "mapa_obitos_gravidez_bairro_2025"),
    ("Puerpério", lambda: mapa_svg(df_map_puerp_2025, "codigo", "óbitos-puerpério", "mortalidade",
        "Óbitos durante o puerpério por bairro (2025)", "Óbitos", FONTE_DATASUS, bins=[0, 1, 2]), "mapa_obitos_puerperio_bairro_2025"),
], 'mapa')

h3('Mortalidade neonatal')
df_prec = read("mortalidade_neonatal_precoce_por_ano.csv")
df_tard = read("mortalidade_neonatal_tardia_por_ano.csv")
df_inf = read("mortalidade_infantil_pos_neonatal_total_por_ano.csv")
option_card([
    ("Precoce (0-6 dias)", lambda: line_chart(df_prec["ano"], [{'label': 'Taxa (‰)', 'values': df_prec['taxa_mortalidade_precoce'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS), "taxa_mortalidade_precoce_ano"),
    ("Tardia (7-27 dias)", lambda: line_chart(df_tard["ano"], [{'label': 'Taxa (‰)', 'values': df_tard['taxa_obitos_tardios'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS), "taxa_obitos_tardios_ano"),
    ("Pós-neonatal (28-364 dias)", lambda: line_chart(df_inf["ano"], [{'label': 'Taxa pós-neonatal (‰)', 'values': df_inf['taxa_mortalidade_pos_neonatal'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS), "taxa_mortalidade_pos_neonatal_ano"),
    ("Total (0-364 dias)", lambda: line_chart(df_inf["ano"], [{'label': 'Taxa infantil total (‰)', 'values': df_inf['taxa_mortalidade_infantil'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS), "taxa_mortalidade_infantil_ano"),
], 'grafico')

df_map_neo_prec_2025 = read("mortalidade_neonatal_precoce_bairro_ano.csv").pipe(lambda d: d[d["ano"] == 2025])
df_map_neo_tard_2025 = read("mortalidade_neonatal_tardia_bairro_ano.csv").pipe(lambda d: d[d["ano"] == 2025])
df_map_pos_neo_2025 = read("mortalidade_infantil_pos_neonatal_total_bairro_ano.csv").pipe(lambda d: d[d["ano"] == 2025])
# 8 mapas era demais numa unica fileira de pills -- dividido em 2 grupos
# (Óbitos / Taxa), specification.md §9 revisao
h6('Óbitos')
option_card([
    ("Precoce", lambda: mapa_svg(df_map_neo_prec_2025, "codigo", "obitos precoces", "mortalidade",
        "Óbitos precoces (0-6 dias) por bairro (2025)", "Óbitos", FONTE_DATASUS, bins=[1, 3, 6, 12]), "mapa_obitos_neonatal_precoce_bairro_2025"),
    ("Tardia", lambda: mapa_svg(df_map_neo_tard_2025, "codigo", "obitos_tardios", "mortalidade",
        "Óbitos tardios (7-27 dias) por bairro (2025)", "Óbitos", FONTE_DATASUS, bins=[1, 2, 4, 8]), "mapa_obitos_neonatal_tardia_bairro_2025"),
    ("Pós-neonatal", lambda: mapa_svg(df_map_pos_neo_2025, "codigo", "obitos_28_364", "mortalidade",
        "Óbitos pós-neonatais (28-364 dias) por bairro (2025)", "Óbitos", FONTE_DATASUS, bins=[1, 2, 4, 8]), "mapa_obitos_pos_neonatal_bairro_2025"),
    ("Total", lambda: mapa_svg(df_map_pos_neo_2025, "codigo", "obitos_0_364", "mortalidade",
        "Óbitos infantis (0-364 dias) por bairro (2025)", "Óbitos", FONTE_DATASUS, bins=[2, 5, 10, 20]), "mapa_mortalidade_infantil_bairro_2025"),
], 'mapa')
h6('Taxa')
option_card([
    ("Precoce", lambda: mapa_svg(df_map_neo_prec_2025, "codigo", "taxa_mortalidade_precoce", "mortalidade",
        "Taxa de óbitos precoces por bairro (2025)", "Taxa por mil NV", FONTE_DATASUS, fmt="pct1"), "mapa_taxa_mortalidade_precoce_bairro_2025"),
    ("Tardia", lambda: mapa_svg(df_map_neo_tard_2025, "codigo", "taxa_obitos_tardios", "mortalidade",
        "Taxa de óbitos tardios por bairro (2025)", "Taxa por mil NV", FONTE_DATASUS, fmt="pct1"), "mapa_taxa_obitos_tardios_bairro_2025"),
    ("Pós-neonatal", lambda: mapa_svg(df_map_pos_neo_2025, "codigo", "taxa_mortalidade_pos_neonatal", "mortalidade",
        "Taxa de mortalidade pós-neonatal por bairro (2025)", "Taxa por mil NV", FONTE_DATASUS, fmt="pct1"), "mapa_taxa_mortalidade_pos_neonatal_bairro_2025"),
    ("Total", lambda: mapa_svg(df_map_pos_neo_2025, "codigo", "taxa_mortalidade_infantil", "mortalidade",
        "Taxa de mortalidade infantil por bairro (2025)", "Taxa por mil NV", FONTE_DATASUS, fmt="pct1"), "mapa_taxa_mortalidade_infantil_bairro_2025"),
], 'mapa')

h3('Óbitos por causas evitáveis')
FONTE_EVITAVEIS = "SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro"

h4('Por grupo/subgrupo de causa (CID-10)')
_entries_cid10 = []
for faixa_id, faixa_titulo in [("", "0-364 dias"), ("_0_a_6_dias", "0-6 dias"), ("_7_a_27_dias", "7-27 dias"), ("_28_a_364_dias", "28-364 dias")]:
    df_g = read(f"mortalidade_causas_evitaveis_grupo{faixa_id}_ano.csv")
    gcols = [c for c in df_g.columns if c != "ano"]
    _lg = f"{faixa_titulo} · Grupo"
    _seed_g = f"obitos_causas_evitaveis_grupo{faixa_id}_ano"
    _entries_cid10.append((_lg, lambda df=df_g, cols=gcols: line_chart(df["ano"], series_from_cols(df, cols, {c: clean_causa(c) for c in cols}), opts={'height': 240, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS), _seed_g))
    df_s = read(f"mortalidade_causas_evitaveis_subgrupo{faixa_id}_ano.csv")
    scols = [c for c in df_s.columns if c != "ano"]
    _ls = f"{faixa_titulo} · Subgrupo"
    _seed_s = f"obitos_causas_evitaveis_subgrupo{faixa_id}_ano"
    _entries_cid10.append((_ls, lambda df=df_s, cols=scols: line_chart(df["ano"], series_from_cols(df, cols, {c: clean_causa(c) for c in cols}), opts={'height': 280, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS), _seed_s))
option_card(_entries_cid10, 'grafico')

h5('Comparação entre faixas etárias (2025)')
df_faixa2025 = read("mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv")
subgrupos_2025 = list(dict.fromkeys(df_faixa2025["subgrupo"]))
faixas_2025 = ["0-6 dias", "7-27 dias", "28-364 dias"]
series_2025 = []
for sg in subgrupos_2025:
    vals = []
    for fx in faixas_2025:
        row = df_faixa2025[(df_faixa2025["subgrupo"] == sg) & (df_faixa2025["faixa_etaria"] == fx)]
        vals.append(float(row["obitos"].iloc[0]) if len(row) else None)
    series_2025.append({'label': clean_causa(sg), 'values': vals})
# Solo -- nao e um corte comparavel aos outros grupos desta secao (specification.md §9)
option_card([("Comparação entre faixas etárias (2025)", lambda: grouped_bar_chart(faixas_2025, series_2025, fonte=FONTE_EVITAVEIS), "obitos_causas_evitaveis_subgrupo_faixa_2025")], 'grafico')

h4('Primeira infância, por Área Programática de Saúde (CAP)')
df_cap_faixa = read("mortalidade_evitaveis_cap_faixa_ano.csv")
df_grupo_cap_faixa = read("mortalidade_evitaveis_grupo_cap_faixa_ano.csv")

h5('Panorama municipal, por subgrupo')
_SEED_PANORAMA_FAIXA = {
    'menores de 1 ano': 'obitos_evitaveis_menores_1_ano_subgrupo_ano',
    'de 1 a 4 anos': 'obitos_evitaveis_1_a_4_anos_subgrupo_ano',
    'menores de 5 anos': 'obitos_evitaveis_menores_5_subgrupo_ano',
}
_entries_panorama_cap = []
for faixa in ['menores de 1 ano', 'de 1 a 4 anos', 'menores de 5 anos']:
    sub = df_cap_faixa[df_cap_faixa["faixa_etaria"] == faixa].groupby(["subgrupo", "ano"], as_index=False)["obitos"].sum()
    subgrupos = list(dict.fromkeys(sub["subgrupo"]))
    anos = sorted(sub["ano"].unique().tolist())
    series = []
    for sg in subgrupos:
        d = sub[sub["subgrupo"] == sg].set_index("ano")["obitos"]
        series.append({'label': clean_causa(sg), 'values': [d.get(a) for a in anos]})
    _lbl = faixa.capitalize()
    _entries_panorama_cap.append((_lbl, lambda anos=anos, series=series: line_chart(anos, series, opts={'height': 260, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS), _SEED_PANORAMA_FAIXA[faixa]))
option_card(_entries_panorama_cap, 'grafico')

h5('Por CAP e faixa etária')
# 18 combinacoes (3 faixas x 6 subgrupos) -- antes eram 18 line_chart em sequencia
# (h5 por faixa + h6 por subgrupo); viram 1 chart-card com seletor de opcoes
# (specification.md §3.2/§4-E), pill = "faixa · subgrupo".
_SLUG_SUBGRUPO = {
    '1.1. Reduzível pelas ações de imunização': 'Imunização',
    '1.2.1. Red por at à mulher na gestação': 'Gestação',
    '1.2.2. Red por at à mulher no parto': 'Parto',
    '1.2.3. Red por at ao recém-nascido': 'Recém-nascido',
    '1.3. Red por ações de diag e trat adequado': 'Diagnóstico/tratamento',
    '1.4. Red por ações promoção vinc a atenção': 'Promoção/vinculação',
}
_entries_cap_faixa = []
for faixa, faixa_lbl in [('menores de 1 ano', 'Menores de 1 ano'), ('de 1 a 4 anos', 'De 1 a 4 anos'), ('menores de 5 anos', 'Menores de 5 anos')]:
    for subgrupo_full, subgrupo_lbl in _SLUG_SUBGRUPO.items():
        sub = df_cap_faixa[(df_cap_faixa["subgrupo"] == subgrupo_full) & (df_cap_faixa["faixa_etaria"] == faixa)]
        if not len(sub):
            continue
        anos = sorted(sub["ano"].unique().tolist())
        caps = sorted(sub["cod_ap_sms"].unique().tolist())
        series = []
        for cap in caps:
            d = sub[sub["cod_ap_sms"] == cap].set_index("ano")["obitos"]
            series.append({'label': f"CAP {cap}", 'values': [d.get(a) for a in anos]})
        _label = f"{faixa_lbl} · {subgrupo_lbl}"
        _entries_cap_faixa.append((
            _label,
            lambda anos=anos, series=series: line_chart(anos, series, opts={'height': 240, 'maxXLabels': 6, 'legendTitle': 'CAP', 'table': True}, fonte=FONTE_EVITAVEIS),
            _label,
        ))
option_card(_entries_cap_faixa, 'grafico')

h5('Grupo evitável e subgrupos (gestação/parto), por CAP')
# specification.md §9: merge de "Grupo evitável por CAP" (3 faixas, par
# abs+pct) com "Gestação e parto por CAP" (2 subgrupos) num so grupo de 5
# pills -- eram 2 option_card separados numa rodada anterior.
GRUPO1_COL = "1. Causas evitáveis"
# seed: par abs+pct exibido junto (out_pair) num unico card/pill -- so ha 1
# seed por opcao, entao aponta para o arquivo do lado absoluto (primario);
# o lado percentual (percentual_evitaveis_cap_*_ano.png) fica sem seed
# proprio nesta rodada (aproximacao documentada, nao ha 2o slot de seed).
_SEED_GRUPO_CAP_FAIXA = {
    'menores de 1 ano': 'obitos_evitaveis_cap_menores_1_ano_ano',
    'de 1 a 4 anos': 'obitos_evitaveis_cap_1_a_4_anos_ano',
    'menores de 5 anos': 'obitos_evitaveis_cap_menores_5_anos_ano',
}
_entries_grupo_cap = []
for faixa, faixa_lbl in [('menores de 1 ano', 'Menores de 1 ano'), ('de 1 a 4 anos', 'De 1 a 4 anos'), ('menores de 5 anos', 'Menores de 5 anos')]:
    sub = df_grupo_cap_faixa[df_grupo_cap_faixa["faixa_etaria"] == faixa]
    anos = sorted(sub["ano"].unique().tolist())
    caps = sorted(sub["cod_ap_sms"].unique().tolist())
    series_abs, series_pct = [], []
    for cap in caps:
        d = sub[sub["cod_ap_sms"] == cap].set_index("ano")
        series_abs.append({'label': f"CAP {cap}", 'values': [d[GRUPO1_COL].get(a) for a in anos]})
        series_pct.append({'label': f"CAP {cap}", 'values': [d['percentual_evitaveis'].get(a) for a in anos], 'format': 'pct1'})
    _entries_grupo_cap.append((
        faixa_lbl,
        lambda anos=anos, series_abs=series_abs, series_pct=series_pct: out_pair(
            lambda: line_chart(anos, series_abs, opts={'height': 240, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS, titulo="Óbitos (absoluto)"),
            lambda: line_chart(anos, series_pct, opts={'height': 240, 'maxXLabels': 6, 'zeroBase': False, 'table': True}, fonte=FONTE_EVITAVEIS, titulo="% do total evitável"),
        ),
        _SEED_GRUPO_CAP_FAIXA[faixa],
    ))
for subgrupo_full, subgrupo_lbl in [
    ('1.2.1. Red por at à mulher na gestação', 'Gestação'),
    ('1.2.2. Red por at à mulher no parto', 'Parto'),
]:
    sub = df_cap_faixa[(df_cap_faixa["subgrupo"] == subgrupo_full) & (df_cap_faixa["faixa_etaria"] == 'menores de 1 ano')]
    anos = sorted(sub["ano"].unique().tolist())
    caps = sorted(sub["cod_ap_sms"].unique().tolist())
    series = []
    for cap in caps:
        d = sub[sub["cod_ap_sms"] == cap].set_index("ano")["obitos"]
        series.append({'label': f"CAP {cap}", 'values': [d.get(a) for a in anos]})
    _label = f"{subgrupo_lbl} (menores de 1 ano)"
    _entries_grupo_cap.append((
        _label,
        lambda anos=anos, series=series: line_chart(anos, series, opts={'height': 240, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS),
        _label,
    ))
option_card(_entries_grupo_cap, 'grafico')

h5('Panorama municipal (< 5 anos) e taxa')
df_menores5_sub = read("obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv")
sgs = list(dict.fromkeys(df_menores5_sub["subgrupo"]))
anos_m5 = sorted(df_menores5_sub["ano"].unique().tolist())
series_m5 = []
for sg in sgs:
    d = df_menores5_sub[df_menores5_sub["subgrupo"] == sg].set_index("ano")["obitos"]
    series_m5.append({'label': clean_causa(sg), 'values': [d.get(a) for a in anos_m5]})
df_taxa_m5 = read("taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv")
option_card([
    ("Óbitos por subgrupo", lambda: line_chart(anos_m5, series_m5, opts={'height': 260, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS), "obitos_evitaveis_menores_5_subgrupo_ano"),
    ("Taxa por mil NV", lambda: line_chart(df_taxa_m5["ano"], [{'label': 'Taxa por mil NV', 'values': df_taxa_m5['taxa_por_mil'], 'format': 'pct1'}], opts={'height': 220, 'zeroBase': False, 'table': True}, fonte=FONTE_EVITAVEIS), "taxa_mortalidade_evitaveis_menores_5_ano"),
], 'grafico')

h5('Mapas')
# specification.md §9: os 8 mapas por CAP viravam uma grade solta (decisao
# anterior, especifica pra galeria); revertido nesta rodada para pills, como
# o resto do relatorio -- seções mais curtas pesou mais que comparação
# lado a lado (registrado como reversão explícita, não descuido).
FAIXAS_PRIMEIRA_INFANCIA = {
    'menores_1_ano':  {'rotulo': 'menores de 1 ano',   'bins_absoluto': [20, 40, 60, 80]},
    '1_a_4_anos':     {'rotulo': 'de 1 a 4 anos',       'bins_absoluto': [2, 4, 7, 10]},
    'menores_5_anos': {'rotulo': 'menores de 5 anos',   'bins_absoluto': [20, 45, 70, 95]},
}
df_evitaveis_cap_2025 = read("mortalidade_evitaveis_cap_2025.csv")
_entries_mapas_cap_faixa = []
for sufixo, info in FAIXAS_PRIMEIRA_INFANCIA.items():
    df_faixa_2025 = df_evitaveis_cap_2025[df_evitaveis_cap_2025["faixa_etaria"] == info['rotulo']]
    _l1 = f"{info['rotulo']} · Óbitos"
    _entries_mapas_cap_faixa.append((_l1, lambda df=df_faixa_2025, info=info: mapa_svg(
        df, "cod_ap_sms", "evitaveis", "mortalidade",
        f"Óbitos por causas evitáveis, {info['rotulo']}, por CAP (2025)", "Óbitos",
        FONTE_EVITAVEIS, bins=info['bins_absoluto'], nivel="cap"), f"mapa_obitos_evitaveis_{sufixo}_cap_2025"))
    _l2 = f"{info['rotulo']} · %"
    _entries_mapas_cap_faixa.append((_l2, lambda df=df_faixa_2025, info=info: mapa_svg(
        df, "cod_ap_sms", "percentual_evitaveis", "mortalidade",
        f"Percentual de óbitos evitáveis, {info['rotulo']}, por CAP (2025)", "% evitáveis",
        FONTE_EVITAVEIS, fmt="pct1", nivel="cap"), f"mapa_percentual_evitaveis_{sufixo}_cap_2025"))
# mapas de gestação/parto por CAP removidos: merge-waleska-changes descontinuou a
# curadoria desses subgrupos em analise.py (tabela_mapa_obitos_evitaveis_*_menores_1_ano_cap_2025.csv
# não é mais gerada) -- ver specs/merge-waleska-changes/specs.md
option_card(_entries_mapas_cap_faixa, 'mapa')

emite_bloco_pendente("Mortalidade infantil por causas evitáveis, por sexo", "recorte por sexo ainda não extraído do SIM")

# ================================================================ INCLUSAO ==

h2('🤝 Inclusão')

h3('População 0-6 por idade/raça/sexo (IBGE SIDRA, 2022)')
FONTE_SIDRA_CENSO = "Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606)"
_ORDEM_IDADE_SIDRA_0_6 = ['Menos de 1 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos', '6 anos']

def _ordenar_idade(df, ordem):
    return df[df["idade"].isin(ordem)].set_index("idade").reindex(ordem).reset_index()

df_censo_raca = _ordenar_idade(read("censo_sidra_populacao_0_6_raca_2022.csv"), _ORDEM_IDADE_SIDRA_0_6)
raca_cols = [c for c in df_censo_raca.columns if c not in ("idade", "Total")]
df_censo_sexo = _ordenar_idade(read("censo_sidra_populacao_0_6_sexo_2022.csv"), _ORDEM_IDADE_SIDRA_0_6)
sexo_cols = [c for c in df_censo_sexo.columns if c not in ("idade", "Total")]
option_card([
    ("Por raça", lambda: grouped_bar_chart(df_censo_raca["idade"], series_from_cols(df_censo_raca, raca_cols), fonte=FONTE_SIDRA_CENSO), "censo_sidra_populacao_0_6_raca_2022"),
    ("Por sexo", lambda: grouped_bar_chart(df_censo_sexo["idade"], series_from_cols(df_censo_sexo, sexo_cols), fonte=FONTE_SIDRA_CENSO), "censo_sidra_populacao_0_6_sexo_2022"),
], 'grafico')

h3('Frequência e taxa de frequência escolar, por raça/sexo')
FONTE_SIDRA_EDU = "Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057)"
_ORDEM_IDADE_SIDRA_0_5 = ['0 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos']
_ORDEM_IDADE_SIDRA_0_6_EDU = ['0 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos', '6 anos']

df_freq_raca = _ordenar_idade(read("sidra_frequencia_escola_0_5_raca_2022.csv"), _ORDEM_IDADE_SIDRA_0_5)
fr_cols = [c for c in df_freq_raca.columns if c not in ("idade", "Total")]
df_freq_sexo = _ordenar_idade(read("sidra_frequencia_escola_0_5_sexo_2022.csv"), _ORDEM_IDADE_SIDRA_0_5)
fs_cols = [c for c in df_freq_sexo.columns if c not in ("idade", "Total")]
df_taxa_raca = _ordenar_idade(read("sidra_taxa_frequencia_0_6_raca_2022.csv"), _ORDEM_IDADE_SIDRA_0_6_EDU)
tr_cols = [c for c in df_taxa_raca.columns if c not in ("idade", "Total")]
df_taxa_sexo = _ordenar_idade(read("sidra_taxa_frequencia_0_6_sexo_2022.csv"), _ORDEM_IDADE_SIDRA_0_6_EDU)
ts_cols = [c for c in df_taxa_sexo.columns if c not in ("idade", "Total")]
option_card([
    ("Frequência 0-5, por raça", lambda: grouped_bar_chart(df_freq_raca["idade"], series_from_cols(df_freq_raca, fr_cols), fonte=FONTE_SIDRA_EDU), "sidra_frequencia_escola_0_5_raca_2022"),
    ("Frequência 0-5, por sexo", lambda: grouped_bar_chart(df_freq_sexo["idade"], series_from_cols(df_freq_sexo, fs_cols), fonte=FONTE_SIDRA_EDU), "sidra_frequencia_escola_0_5_sexo_2022"),
    ("Taxa 0-6, por raça", lambda: grouped_bar_chart(df_taxa_raca["idade"], series_from_cols(df_taxa_raca, tr_cols, fmt='pct1'), fonte=FONTE_SIDRA_EDU), "sidra_taxa_frequencia_0_6_raca_2022"),
    ("Taxa 0-6, por sexo", lambda: grouped_bar_chart(df_taxa_sexo["idade"], series_from_cols(df_taxa_sexo, ts_cols, fmt='pct1'), fonte=FONTE_SIDRA_EDU), "sidra_taxa_frequencia_0_6_sexo_2022"),
], 'grafico')

# ---- CadÚnico: recortes por sexo, raça/cor, arranjo familiar e renda (specs/recortes_cadunico) ----
FONTE_CADUNICO = "CadÚnico (extração CTPE, jun/2026)"
FONTE_MAPA_CADUNICO = (FONTE_CADUNICO + ". Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; "
                       "bairros com menos de 20 famílias suprimidos")
df_cad_sexo = read("cadunico_por_sexo_2026.csv")
df_cad_raca = read("cadunico_por_raca_cor_2026.csv")
df_cad_arranjo = read("cadunico_familias_por_arranjo_2026.csv")
df_cad_arranjo_renda = read("cadunico_familias_arranjo_renda_2026.csv")
df_cad_recortes_mapa = read("tabela_mapa_cadunico_recortes_bairro_2026.csv")
_ORDEM_RACA_CAD = ["Parda", "Branca", "Preta", "Amarela", "Indígena"]

def _mapa_cadunico_pct(col, titulo, legenda):
    return mapa_svg(df_cad_recortes_mapa, "codbairro", col, "cadunico", titulo, legenda, FONTE_MAPA_CADUNICO,
                    fmt="pct1", col_suprimido="suprimido")

# populacao-referencia A4: razão municipal CadÚnico / população Ripsa
h3("Crianças de 0 a 5 anos no CadÚnico em relação à população do município")
nota_metodologica(
    "Crianças cadastradas no CadÚnico (jun/2026) divididas pela população estimada de 0 a 5 anos do município em 2025 "
    "(Ripsa/Ministério da Saúde). É uma razão entre um cadastro e uma estimativa, com um ano de diferença — não é a cobertura exata do cadastro."
)
_razao_cad = read("cadunico_razao_populacao_0_a_5_2026.csv")
_tab_razao_cad = pd.DataFrame({
    "Crianças de 0 a 5 anos no CadÚnico": _razao_cad["criancas_cadunico_0_a_5"].map(_fmt_ptbr),
    "Famílias": _razao_cad["familias_cadunico"].map(_fmt_ptbr),
    "População de 0 a 5 anos (2025)": _razao_cad["populacao_ripsa_0_a_5"].map(_fmt_ptbr),
    "Crianças no CadÚnico por 100 crianças": _razao_cad["razao_percentual"].map(lambda v: _fmt_ptbr(v, 1) + "%"),
})
tabela_com_texto(lambda: plain_table(_tab_razao_cad, fonte=FONTE_CADUNICO + "; população: estimativas Ripsa/Ministério da Saúde (2025)"),
                 "cadunico_razao_populacao_0_a_5_2026")

h3("Famílias no CadÚnico com crianças até 6 anos, por sexo")
nota_metodologica(
    "Sexo da criança. \"Até 6 anos\" = 0 a 5 anos completos (quem já fez 6 anos não está nesta extração). "
    "As famílias estão classificadas pelo sexo das suas crianças (só meninas, só meninos ou meninas e meninos) — "
    "cada família conta uma vez só."
)
_cs = df_cad_sexo[df_cad_sexo["recorte"] == "Crianças por sexo"]
_cs = _cs[~_cs["categoria"].str.startswith("Total")]
_fs = df_cad_sexo[df_cad_sexo["recorte"] == "Famílias por sexo das crianças"]
_fs = _fs[_fs["categoria"] != "Total"]
option_card([
    ("Crianças e famílias", lambda: out_pair(
        lambda: bar_chart([{'label': r["categoria"], 'value': r["Crianças"]} for _, r in _cs.iterrows()], fonte=FONTE_CADUNICO, titulo="Crianças, por sexo"),
        lambda: bar_chart([{'label': r["categoria"], 'value': r["Famílias"]} for _, r in _fs.iterrows()], fonte=FONTE_CADUNICO, titulo="Famílias, por sexo das crianças"),
    ), "cadunico_criancas_por_sexo"),
], 'grafico')
# mapa % meninas cortado na revisão visual (recortes_cadunico T12.3): ~49% em todo bairro

h3("Famílias no CadÚnico com crianças até 6 anos, por raça/cor")
nota_metodologica(
    "Raça/cor da criança. Uma família com crianças de raça/cor diferentes aparece em mais de uma categoria, por isso as "
    "famílias não somam o total. Negra = preta + parda. Por bairro, só o percentual de crianças negras é publicado "
    "(grupos pequenos, como indígena e amarela, só aparecem no total da cidade)."
)
_rc = df_cad_raca.set_index("raça/cor da criança").loc[_ORDEM_RACA_CAD].reset_index()
option_card([
    ("Crianças e famílias", lambda: out_pair(
        lambda: bar_chart([{'label': r["raça/cor da criança"], 'value': r["Crianças"]} for _, r in _rc.iterrows()], fonte=FONTE_CADUNICO, titulo="Crianças, por raça/cor"),
        lambda: bar_chart([{'label': r["raça/cor da criança"], 'value': r["Famílias com ao menos uma"]} for _, r in _rc.iterrows()], fonte=FONTE_CADUNICO, titulo="Famílias com ao menos uma criança da raça/cor"),
    ), "cadunico_criancas_por_raca_cor"),
], 'grafico')
option_card([
    ("% negras", lambda: _mapa_cadunico_pct("% crianças negras", "% de crianças negras (pretas e pardas) de 0 a 5 anos no CadÚnico, por bairro", "% negras"),
     "mapa_percentual_cadunico_criancas_negras_bairro_2026"),
], 'mapa')

h3("Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar")
nota_metodologica(
    "Arranjo familiar aproximado pela composição do cadastro: número e sexo das pessoas de 18 anos ou mais na família. "
    "\"Uma adulta\" NÃO é o conceito oficial de família monoparental (que depende do parentesco, ausente nesta extração) — "
    "um companheiro que não está no cadastro não aparece. Renda per capita da família; acima de meio salário mínimo "
    "(R$ 810) as faixas estão agrupadas. Células com menos de 20 famílias são suprimidas."
)
_arr = df_cad_arranjo[df_cad_arranjo["arranjo familiar"] != "Total"]
_ordem_arr = _arr["arranjo familiar"].tolist()
_faixas_renda = list(dict.fromkeys(df_cad_arranjo_renda["faixa de renda per capita"]))
_serie_renda = []
for _fx in _faixas_renda:
    _d = df_cad_arranjo_renda[df_cad_arranjo_renda["faixa de renda per capita"] == _fx].set_index("arranjo")["% no arranjo"]
    _serie_renda.append({'label': _fx, 'values': [None if pd.isna(_d.get(a)) else float(_d.get(a)) for a in _ordem_arr], 'format': 'pct1'})
option_card([
    ("Por arranjo", lambda: bar_chart([{'label': r["arranjo familiar"], 'value': r["Famílias"]} for _, r in _arr.iterrows()],
                                      fonte=FONTE_CADUNICO, titulo="Famílias, por arranjo familiar"), "cadunico_familias_por_arranjo"),
    ("Arranjo × renda", lambda: grouped_bar_chart(_ordem_arr, _serie_renda, fonte=FONTE_CADUNICO,
                                                  titulo="% das famílias de cada arranjo, por renda per capita"), "cadunico_familias_arranjo_renda"),
], 'grafico')
option_card([
    ("% uma adulta", lambda: _mapa_cadunico_pct("% famílias com uma adulta", "Famílias com crianças de 0 a 5 anos no CadÚnico: % com uma só adulta, por bairro", "% uma adulta"),
     "mapa_percentual_cadunico_familias_uma_adulta_bairro_2026"),
], 'mapa')

emite_bloco_pendente("Crianças no CadÚnico com alguma deficiência", "baixar dados — Léo")
emite_bloco_pendente("Famílias no CadÚnico com criança com deficiência", "baixar dados — Léo")
emite_bloco_pendente("Crianças no CadÚnico por tipo de deficiência", "baixar dados — Léo")

# ===================================================== FAMILIA E CUIDADOS ==

h2('👨‍👩‍👧 Família e Cuidados')

h3('CadÚnico')

h4('Por faixa de renda e idade')
df_renda = read("cadunico_por_faixa_renda_2026.csv")
df_renda_sem_total = df_renda[df_renda["faixa de renda"] != "Total"].copy()
# recortes_cadunico A7: rótulo descritivo da faixa de renda per capita (coluna gerada por analise.py)
df_renda_sem_total["faixa de renda"] = df_renda_sem_total["faixa de renda (descrição)"]
df_idade = read("cadunico_por_idade_2026.csv")
df_idade["idade_lbl"] = df_idade["idade"].astype(int).map(lambda i: f"{i} ano" if i == 1 else f"{i} anos")
# seed: cada opcao mostra um out_pair (Criancas + Familias lado a lado) sob
# 1 unico bloco de texto/pill -- so ha 1 seed por opcao, entao aponta para o
# arquivo do lado "Criancas" (primeiro do par, aproximacao documentada); o
# lado "Familias" (cadunico_familias_por_faixa_renda.png / _por_idade.png)
# fica sem seed proprio nesta rodada.
option_card([
    ("Por faixa de renda", lambda: out_pair(
        lambda: bar_chart([{'label': r["faixa de renda"], 'value': r["Crianças"]} for _, r in df_renda_sem_total.iterrows()], fonte=FONTE_CADUNICO, titulo="Crianças"),
        lambda: bar_chart([{'label': r["faixa de renda"], 'value': r["Famílias"]} for _, r in df_renda_sem_total.iterrows()], fonte=FONTE_CADUNICO, titulo="Famílias"),
    ), "cadunico_criancas_por_faixa_renda"),
    ("Por idade", lambda: out_pair(
        lambda: bar_chart([{'label': r["idade_lbl"], 'value': r["Crianças"]} for _, r in df_idade.iterrows()], fonte=FONTE_CADUNICO, titulo="Crianças"),
        lambda: bar_chart([{'label': r["idade_lbl"], 'value': r["Famílias"]} for _, r in df_idade.iterrows()], fonte=FONTE_CADUNICO, titulo="Famílias"),
    ), "cadunico_criancas_por_idade"),
], 'grafico')

h4('Mapas')
df_map_cadunico_criancas = read("tabela_mapa_cadunico_criancas_2026.csv")
df_map_cadunico_0_4 = read("tabela_mapa_cadunico_criancas_0_a_4_2026.csv")
option_card([
    ("Crianças 0-5", lambda: mapa_svg(df_map_cadunico_criancas, "codbairro", "Crianças", "cadunico",
        "Crianças (0 a 5 anos) no CadÚnico, por bairro", "Crianças", FONTE_MAPA_CADUNICO, bins=[250, 750, 1500, 3000],
        col_suprimido="suprimido"), "mapa_cadunico_criancas_bairro_2026"),
    ("Crianças 0-4", lambda: mapa_svg(df_map_cadunico_0_4, "codbairro", "Crianças", "cadunico",
        "Crianças (0 a 4 anos) no CadÚnico, por bairro", "Crianças", FONTE_MAPA_CADUNICO, bins=[200, 500, 1000, 2000],
        col_suprimido="suprimido"), "mapa_cadunico_criancas_0_a_4_bairro_2026"),
    # recortes_cadunico D6: mapa "% s/ Censo" retirado do relatório (até 510% por viés CEP -> bairro; fica só no notebook)
], 'mapa')

h3('Cobertura vacinal (EPI)')
FONTE_EPI = "EPI/SVS-Rio, cobertura vacinal por imunobiológico"
df_vac = read("cobertura_vacinal_epi_por_ano.csv")
vac_cols = [c for c in df_vac.columns if c != "ano"]
df_vac_comp = read("cobertura_vacinal_epi_comparativo_anos.csv")
df_vac_comp_wide = df_vac_comp.pivot(index="ano", columns="imunobiologico", values="cobertura").reset_index()
comp_cols = [c for c in df_vac_comp_wide.columns if c != "ano"]
option_card([
    ("Série temporal por imunobiológico", lambda: line_chart(df_vac["ano"], series_from_cols(df_vac, vac_cols, fmt='pct1'), opts={'height': 280, 'maxXLabels': 8, 'table': True}, fonte=FONTE_EPI), "cobertura_vacinal_epi_ano"),
    ("Comparativo por ano", lambda: grouped_bar_chart(df_vac_comp_wide["ano"], series_from_cols(df_vac_comp_wide, comp_cols, fmt='pct1'), opts={'height': 320}, fonte=FONTE_EPI), "cobertura_vacinal_epi_comparativo_anos"),
], 'grafico')

h3('Frequência escolar por idade (PNAD Contínua)')
df_pnad = read("frequencia_escolar_pnad_por_idade.csv")
# PNAD e Matrículas ficam soltos -- indicadores/fontes diferentes entre si,
# nao um corte do mesmo dado (specification.md §9, mesmo criterio ja usado
# para nao forcar pills na "Comparação entre faixas etárias" de evitáveis)
option_card([("Frequência por idade", lambda: bar_chart([{'label': r["Idade"], 'value': r["Total"] * 100} for _, r in df_pnad.iterrows()], fonte="PNAD Contínua (IBGE)", fmt='pct1'), "pnad_frequencia_escolar_por_idade")], 'grafico')

# populacao-referencia D3: total por idade da SIDRA 10057 (item "frequentando escola/creche (geral)")
h3('Crianças de 0 a 5 anos que frequentam escola/creche (Censo 2022)')
df_freq_total = _ordenar_idade(read("sidra_frequencia_escola_0_5_total_2022.csv"), _ORDEM_IDADE_SIDRA_0_5)
option_card([("Por idade", lambda: bar_chart([{'label': r["idade"], 'value': r["Crianças"]} for _, r in df_freq_total.iterrows()],
    fonte=FONTE_SIDRA_EDU), "sidra_frequencia_escola_0_5_total_2022")], 'grafico')

# populacao-referencia Parte E (matriculas/): série 2007-2025 refeita dos microdados do INEP
h3('Matrículas de crianças de 0 a 5 anos (Censo Escolar/INEP)')
nota_metodologica(
    "0 a 5 anos (creche e pré-escola): os dados abertos do INEP não separam as crianças de 6 anos das de 7 a 10. "
    "A série inteira (2007-2025) foi refeita a partir dos microdados do Censo Escolar, com a mesma definição em todos os anos."
)
FONTE_MATRICULAS = "Censo Escolar da Educação Básica (INEP), microdados"
df_mat = read("matriculas_0_a_5_por_ano.csv").sort_values("ano")
option_card([
    ("Total 0 a 5 anos", lambda: line_chart(df_mat["ano"], [{'label': 'Matrículas', 'values': df_mat['matriculas']}],
        opts={'height': 220, 'maxXLabels': 8, 'table': True}, fonte=FONTE_MATRICULAS), "matriculas_0_a_5_por_ano"),
    ("Creche e pré-escola", lambda: line_chart(df_mat["ano"], [
        {'label': '0 a 3 anos (creche)', 'values': df_mat['matriculas_0_a_3']}, {'label': '4 a 5 anos (pré-escola)', 'values': df_mat['matriculas_4_a_5']}],
        opts={'height': 240, 'maxXLabels': 8, 'table': True}, fonte=FONTE_MATRICULAS), "matriculas_0_a_5_creche_pre_por_ano"),
    ("Rede pública e privada", lambda: line_chart(df_mat["ano"], [
        {'label': 'Rede pública', 'values': df_mat['matriculas_publica']}, {'label': 'Rede privada', 'values': df_mat['matriculas_privada']}],
        opts={'height': 240, 'maxXLabels': 8, 'table': True}, fonte=FONTE_MATRICULAS), "matriculas_0_a_5_rede_por_ano"),
], 'grafico')

h3('Taxa bruta de atendimento escolar de 0 a 5 anos')
nota_metodologica(
    "Matrículas em escolas do Rio divididas pela população estimada de residentes da mesma idade (Ripsa/Ministério da Saúde). "
    "É uma taxa bruta: inclui crianças de outros municípios que estudam no Rio. As linhas tracejadas são as metas do Plano Nacional de "
    "Educação (50% em creche e 100% na pré-escola)."
)
option_card([("Por faixa de idade", lambda: line_chart(df_mat["ano"], [
    {'label': '0 a 3 anos (creche)', 'values': df_mat['taxa_atendimento_0_a_3'], 'format': 'pct1'},
    {'label': '4 a 5 anos (pré-escola)', 'values': df_mat['taxa_atendimento_4_a_5'], 'format': 'pct1'},
    {'label': '0 a 5 anos', 'values': df_mat['taxa_atendimento_0_a_5'], 'format': 'pct1'}],
    opts={'height': 280, 'maxXLabels': 8, 'table': True,
          'refLines': [{'value': 50, 'label': 'Meta PNE creche: 50%'}, {'value': 100, 'label': 'Meta PNE pré-escola: 100%'}]},
    fonte="Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde"), "taxa_atendimento_0_a_5_por_ano")], 'grafico')

# ======================================================== PROTECAO ========

h2('🛡️ Proteção')

FONTE_SINAN = "Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos"
FONTE_SINAN_CENSO = "Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio)"
FONTE_IPS = "Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades)"

# ---- Violência territorial (Data.Rio/IPS) ---------------------------------
h3('Violência territorial (Data.Rio/IPS, 2024)')
nota_metodologica(
    "ATENÇÃO: são dados gerais da população, de todas as idades — NÃO são específicos de crianças (0 a 6 anos) nem de jovens; "
    "o indicador \"homicídios de jovens negros\" também se refere à população geral. Um único ano (2024), sem série. "
    "Nível Região Administrativa; a RA XXI Paquetá não tem dado no IPS."
)
df_terr_mapa = read("tabela_mapa_violencia_territorial_ra_2024.csv")
_INDICADORES_TERR = [
    ("taxa_homicidios", "Taxa de homicídios", "violencia_territorial_homicidios_ra_2024", "mapa_violencia_territorial_homicidios_ra_2024"),
    ("homicidios_acao_policial", "Homicídios por ação policial", "violencia_territorial_homicidios_acao_policial_ra_2024", "mapa_violencia_territorial_homicidios_acao_policial_ra_2024"),
    ("homicidios_jovens_negros", "Homicídios de jovens negros", "violencia_territorial_homicidios_jovens_negros_ra_2024", "mapa_violencia_territorial_homicidios_jovens_negros_ra_2024"),
]

option_card([
    (rot, lambda c=col, r=rot: mapa_svg(df_terr_mapa, "codra", c, "protecao", f"{r} por Região Administrativa (2024) — população geral, todas as idades",
                                         "Taxa (IPS), todas as idades, não só crianças", FONTE_IPS, fmt="dec1", nivel="ra"), seed_m)
    for col, rot, _, seed_m in _INDICADORES_TERR
], 'mapa')

# ---- Violência familiar (Sinan) --------------------------------------------
h3('Violência familiar (0 a 5 anos, Sinan)')
nota_metodologica(
    "Faixa 0 a 5 anos agregada (o recorte menor de 1 ano × 1 a 5 anos está pendente). Os vínculos do provável autor NÃO são excludentes "
    "e não existe \"total de violência familiar\": nunca somar mãe + pai; \"outros\" (padrasto + irmão(ã) + cônjuge + ex-cônjuge + filho(a)) "
    "pode contar a mesma notificação mais de uma vez. Possível quebra de série em 2017 (salto de 600 para 1.514 notificações de mãe) — "
    "hipótese de mudança de ficha/notificação, a confirmar com a fonte. 2026 é ano parcial e fica fora da série. Contagem absoluta não é risco."
)
df_vinculo = read("violencia_familiar_por_vinculo_ano.csv")
df_outros = read("violencia_familiar_outros_detalhe.csv")
option_card([
    ("Mãe, pai e outros", lambda: line_chart(df_vinculo["ano"], [
        {'label': 'Mãe', 'values': df_vinculo['mae']}, {'label': 'Pai', 'values': df_vinculo['pai']},
        {'label': 'Outros vínculos', 'values': df_vinculo['outros']}],
        opts={'height': 260, 'maxXLabels': 8, 'table': True}, fonte=FONTE_SINAN), "violencia_familiar_serie_vinculos"),
    ("Composição de \"outros\"", lambda: line_chart(df_outros["ano"], [
        {'label': 'Padrasto', 'values': df_outros['padrasto']}, {'label': 'Irmão(ã)', 'values': df_outros['irmao']},
        {'label': 'Cônjuge', 'values': df_outros['conjuge']}, {'label': 'Ex-cônjuge', 'values': df_outros['exconjuge']},
        {'label': 'Filho(a)', 'values': df_outros['filho']}],
        opts={'height': 260, 'maxXLabels': 8, 'table': True}, fonte=FONTE_SINAN), "violencia_familiar_outros_serie"),
], 'grafico')

h5('Dez bairros com mais notificações (2025)')
df_top_b = read("violencia_familiar_top_bairros_2025.csv")
_bairros_top = list(dict.fromkeys(df_top_b["bairro"]))
_pt = df_top_b.pivot(index="bairro", columns="vinculo", values="notificações").reindex(_bairros_top)
option_card([("Mãe e pai (2025)", lambda: grouped_bar_chart(
    _bairros_top, [{'label': 'Mãe', 'values': _pt['Mãe'].tolist()}, {'label': 'Pai', 'values': _pt['Pai'].tolist()}],
    fonte=FONTE_SINAN, titulo="Dez bairros com mais notificações de violência familiar (2025) — mãe e pai lado a lado, sem soma"),
    "violencia_familiar_top_bairros_2025")], 'grafico')

h5('Mapas por bairro')
df_m_mae = read("tabela_mapa_violencia_familiar_mae_2025.csv")
df_m_pai = read("tabela_mapa_violencia_familiar_pai_2025.csv")
df_m_out = read("tabela_mapa_violencia_familiar_outros_2021_2025.csv")
option_card([
    ("Mãe (2025)", lambda: mapa_svg(df_m_mae, "codbairro", "mae", "protecao", "Notificações de violência familiar por bairro — mãe (2025)",
                                    "Notificações (mãe)", FONTE_SINAN, bins=[5, 15, 30, 60], zero_branco=True), "mapa_violencia_familiar_mae_bairro_2025"),
    ("Pai (2025)", lambda: mapa_svg(df_m_pai, "codbairro", "pai", "protecao", "Notificações de violência familiar por bairro — pai (2025)",
                                    "Notificações (pai)", FONTE_SINAN, bins=[5, 15, 30, 60], zero_branco=True), "mapa_violencia_familiar_pai_bairro_2025"),
    ("Outros (2021-2025)", lambda: mapa_svg(df_m_out, "codbairro", "outros_2021_2025", "protecao",
                                            "Notificações de violência familiar por bairro — outros vínculos (2021-2025, acumulado)",
                                            "Notificações (outros)", FONTE_SINAN, bins=[1, 3, 6, 12], zero_branco=True), "mapa_violencia_familiar_outros_bairro_2021_2025"),
], 'mapa')

h5('Por CAP (2025)')
_COLS_TAB = {'mae': 'Mãe', 'pai': 'Pai', 'outros': 'Outros', 'pop_0_4': 'Crianças 0-4 (Censo 2022)',
             'taxa_por_mil_mae': 'Taxa mãe /1.000', 'taxa_por_mil_pai': 'Taxa pai /1.000', 'taxa_por_mil_outros': 'Taxa outros /1.000'}
df_vf_cap = read("violencia_familiar_por_cap.csv"); df_vf_cap = df_vf_cap[df_vf_cap["ano"] == 2025]
_tab_cap = df_vf_cap[['cod_ap_sms'] + list(_COLS_TAB)].rename(columns={'cod_ap_sms': 'CAP', **_COLS_TAB}).round(1)
for _c in ['Mãe', 'Pai', 'Outros', 'Crianças 0-4 (Censo 2022)']:
    _tab_cap[_c] = _tab_cap[_c].astype(int)
tabela_com_texto(lambda: plain_table(_tab_cap, fonte=FONTE_SINAN_CENSO), "violencia_familiar_por_cap")

# ---- Notificações de lesão autoprovocada -----------------------------------
h3('Notificações de violência interpessoal/autoprovocada (0 a 5 anos, Sinan)')
nota_metodologica(
    "Parcial: o arquivo cobre apenas lesão autoprovocada (a violência interpessoal total e o recorte menor de 1 ano × 1 a 5 anos estão pendentes). "
    "Série muito esparsa: 40 notificações em 2018-2026, 33 delas em 2026 (ano parcial, usado aqui como referência). O salto em 2026 pode refletir "
    "mudança de registro administrativo — hipótese, a confirmar com a fonte (SMS/Sinan)."
)
df_autoprov = read("notif_autoprovocada_por_bairro_ano.csv")
_ap_antes = int(df_autoprov.loc[df_autoprov["ano"] < 2026, "casos"].sum()); _ap_2026 = int(df_autoprov.loc[df_autoprov["ano"] == 2026, "casos"].sum())
option_card([("2018-2025 × 2026", lambda: bar_chart([
    {'label': '2018-2025 (8 anos)', 'value': _ap_antes}, {'label': '2026 (ano parcial)', 'value': _ap_2026}],
    fonte="Sinan NET/Tabnet (SMS-Rio); 2026 parcial", titulo="Lesão autoprovocada notificada, 0 a 5 anos"), "notif_autoprovocada_antes_2026_vs_2026")], 'grafico')
df_m_auto = read("tabela_mapa_notif_autoprovocada_2026.csv")
option_card([("Bairro (2026)", lambda: mapa_svg(df_m_auto, "codbairro", "casos", "protecao",
    "Lesão autoprovocada notificada por bairro (2026, ano parcial)", "Notificações (2026)",
    "Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos", bins=[1, 3], zero_branco=True), "mapa_notif_autoprovocada_bairro_2026")], 'mapa')

# ---- Taxa de notificações ---------------------------------------------------
h3('Taxa de notificações de violência (por 1.000 crianças)')
nota_metodologica(
    "Ressalva de denominador: numerador com crianças de 0 a 5 anos (Sinan) e denominador com 0 a 4 anos (Censo 2022) — a taxa superestima ~20%, "
    "de forma uniforme, então o ranking entre bairros se preserva. \"Outros\" usa o acumulado 2021-2025. Bairros com menos de 100 crianças têm taxa instável: "
    "nos mapas por bairro a escala de cor é limitada ao percentil 95 (o valor real aparece ao passar o mouse). "
    "O denominador por bairro/RA/CAP é a população do Censo 2022, fixa: o Censo subconta crianças pequenas (o que puxa a taxa para cima) e é de 2022, enquanto as notificações são de 2025 (o que puxa para baixo). Por isso as taxas por território servem para comparar territórios entre si, e não com a taxa do município, que usa a estimativa populacional Ripsa/MS do mesmo ano. "
    "Nos mapas de taxa há o botão \"Remover outliers\"."
)
# populacao-referencia A3: taxa municipal com população Ripsa de 0 a 5 anos (mesma faixa e ano do numerador)
h5('Município: notificações por 1.000 crianças de 0 a 5 anos (2011-2025)')
df_vf_taxa_mun = read("violencia_familiar_taxa_municipio_ano.csv")
option_card([("Mãe, pai e outros", lambda: line_chart(df_vf_taxa_mun["ano"], [
    {'label': 'Mãe', 'values': df_vf_taxa_mun['taxa_por_mil_mae'], 'format': 'dec1'},
    {'label': 'Pai', 'values': df_vf_taxa_mun['taxa_por_mil_pai'], 'format': 'dec1'},
    {'label': 'Outros vínculos', 'values': df_vf_taxa_mun['taxa_por_mil_outros'], 'format': 'dec1'}],
    opts={'height': 260, 'maxXLabels': 8, 'table': True, 'yDecimals': 1},
    fonte="Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 5 anos: estimativas Ripsa/Ministério da Saúde"),
    "violencia_familiar_taxa_municipio_ano")], 'grafico')

_mapas_taxa = []
for _nome, _rot, _per in [('mae_2025', 'mãe', '2025'), ('pai_2025', 'pai', '2025'), ('outros_2021_2025', 'outros vínculos', '2021-2025')]:
    _dft = read(f"tabela_mapa_violencia_familiar_taxa_{_nome}.csv")
    _teto = float(_dft["taxa_escala_mapa"].max())
    _mapas_taxa.append((f"{_rot.capitalize()} ({_per})", lambda d=_dft, n=_nome, r=_rot, p=_per, t=_teto: mapa_svg(
        d, "codbairro", f"taxa_por_mil_{n}", "protecao", f"Notificações de violência ({r}) por 1.000 crianças de 0 a 4 anos ({p})",
        "Por 1.000 crianças 0-4 (Censo 2022)", FONTE_SINAN_CENSO, fmt="dec1", teto=t),
        f"mapa_violencia_familiar_{_nome.split('_')[0]}_taxa_bairro_{_nome.split('_', 1)[1]}"))
for _nome, _rot, _per in [('mae_2025', 'mãe', '2025'), ('pai_2025', 'pai', '2025'), ('outros_2021_2025', 'outros vínculos', '2021-2025')]:
    _dfr = read(f"tabela_mapa_violencia_familiar_taxa_ra_{_nome}.csv")
    _mapas_taxa.append((f"{_rot.capitalize()} · RA ({_per})", lambda d=_dfr, n=_nome, r=_rot, p=_per: mapa_svg(
        d, "codra", f"taxa_por_mil_{n}", "protecao", f"Notificações de violência ({r}) por 1.000 crianças de 0 a 4 anos, por RA ({p})",
        "Por 1.000 crianças 0-4 (Censo 2022)", FONTE_SINAN_CENSO, fmt="dec1", nivel="ra"),
        f"mapa_violencia_familiar_{_nome.split('_')[0]}_taxa_ra_{_nome.split('_', 1)[1]}"))
option_card(_mapas_taxa, 'mapa')
h5('Dez maiores taxas (2025, bairros com 100 ou mais crianças de 0 a 4 anos)')
df_top_t = read("violencia_familiar_taxa_top_bairros_2025.csv")
_bairros_t = list(dict.fromkeys(df_top_t["bairro"]))
_ptt = df_top_t.pivot(index="bairro", columns="vinculo", values="taxa por 1.000").reindex(_bairros_t)
option_card([("Mãe e pai (2025)", lambda: grouped_bar_chart(
    _bairros_t, [{'label': 'Mãe', 'values': _ptt['Mãe'].tolist(), 'format': 'dec1f'}, {'label': 'Pai', 'values': _ptt['Pai'].tolist(), 'format': 'dec1f'}],
    fonte=FONTE_SINAN_CENSO, titulo="Dez maiores taxas de notificação por 1.000 crianças de 0 a 4 anos (2025; população: Censo 2022)"),
    "violencia_familiar_taxa_top_bairros_2025")], 'grafico')

emite_bloco_pendente("Crianças que sofrem violência, por tipificação (sexo e idade)", "dado ainda não extraído do Tabnet municipal")

# ====================================================== ALIMENTACAO =======

h2('🍽️ Alimentação')

h3('Baixo peso ao nascer')
option_card([
    ("% abaixo do peso", lambda: line_chart(df_bp["ano"], [{'label': '% abaixo do peso', 'values': df_bp['percentual abaixo do peso'], 'format': 'pct1'}], opts={'height': 220, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS), "nascidos_abaixo_peso_percentual_por_ano"),
], 'grafico')

h3('Mapas')
df_map_bp_2025 = read("tabela_mapa_nascidos_baixo_peso_2025.csv").pipe(lambda d: d[d["ano"] == 2025])
option_card([
    ("Baixo peso · Absoluto", lambda: mapa_svg(df_map_bp_2025, "codigo", "nascidos abaixo peso", "natalidade",
        "Nascidos com baixo peso por bairro (2025)", "Nascidos abaixo do peso", FONTE_DATASUS, bins=[15, 30, 60, 120]), "mapa_nascidos_baixo_peso_bairro_2025"),
    ("Baixo peso · %", lambda: mapa_svg(df_map_bp_2025, "codigo", "percentual abaixo do peso", "natalidade",
        "% de nascidos com baixo peso por bairro (2025)", "% baixo peso", FONTE_DATASUS, fmt="pct1"), "mapa_percentual_baixo_peso_bairro_2025"),
], 'mapa')

h3('SISVAN')
FONTE_SISVAN = "SISVAN/DATASUS"
df_desn = read("sisvan_desnutricao_por_ano.csv")
df_sobre = read("sisvan_sobrepeso_por_ano.csv")
option_card([
    ("Baixo peso", lambda: line_chart(df_desn["ano"], [{'label': '% baixo peso', 'values': df_desn['Percent. baixo peso total'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_SISVAN), "sisvan_desnutricao_percentual_por_ano"),
    ("Sobrepeso", lambda: line_chart(df_sobre["ano"], [{'label': '% sobrepeso', 'values': df_sobre['Percent. sobrepeso total'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_SISVAN), "sisvan_sobrepeso_percentual_por_ano"),
    ("Obesidade", lambda: line_chart(df_sobre["ano"], [{'label': '% obesidade', 'values': df_sobre['obesidade_percentual'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_SISVAN), "sisvan_obesidade_percentual_por_ano"),
], 'grafico')

# =========================================================== MORADIA ======

h2('🏠 Moradia')

emite_bloco_pendente("Crianças no CadÚnico em domicílios com inadequação habitacional", "Posterior")
emite_bloco_pendente("Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (acima de 3 por dormitório)", "Posterior")
emite_bloco_pendente("Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais)", "Posterior (apenas cad)")

# ============================================================== ASSEMBLE ==

gen_date = datetime.date.today().strftime("%d de %B de %Y")
MESES = {"January": "janeiro", "February": "fevereiro", "March": "março", "April": "abril", "May": "maio", "June": "junho",
         "July": "julho", "August": "agosto", "September": "setembro", "October": "outubro", "November": "novembro", "December": "dezembro"}
for en, pt in MESES.items():
    gen_date = gen_date.replace(en, pt)

# ---- rodape institucional (specification.md §3.11/§4-M -- escopo enxuto) ----
# URLs de Transparencia Rio/LGPD e o e-mail de contato sao os do site
# institucional principal, copiados do mockup -- CONFIRMAR se sao os corretos
# para este relatorio especificamente antes do deploy (plan.md §6, T6.2).
FOOTER_FONTES = ["Censo 2022 (IBGE)", "CadÚnico", "DataSUS/Tabnet", "SISVAN · IBGE SIDRA"]
FOOTER_LINKS = [
    ("ipp.prefeitura.rio", "https://ipp.prefeitura.rio/"),
    ("Transparência Rio", "https://transparencia.rio/"),
    ("LGPD — Proteção de dados", "https://ipp.prefeitura.rio/lgpd/"),
]
FOOTER_CONTATO = "ascom.ipp@prefeitura.rio"

_footer_cols = [
    f'<div class="footer-col footer-col-logo">{LOGO_IMG}<p>Relatório produzido a partir da análise de indicadores de primeira infância do Instituto Municipal de Urbanismo Pereira Passos (IPP).</p></div>',
    '<div class="footer-col"><div class="eyebrow">FONTES DE DADOS</div>' + "".join(f'<div>{f}</div>' for f in FOOTER_FONTES) + '</div>',
    '<div class="footer-col"><div class="eyebrow">LINKS</div>' + "".join(f'<div><a href="{url}" target="_blank" rel="noopener">{label} ↗</a></div>' for label, url in FOOTER_LINKS) + '</div>',
    f'<div class="footer-col"><div class="eyebrow">CONTATO</div><div>{FOOTER_CONTATO}</div><div class="eyebrow" style="margin-top:14px;">ATUALIZADO EM</div><div>{gen_date}</div></div>',
]
footer = (
    '<footer class="doc-foot">'
    '<div class="footer-cols">' + "".join(_footer_cols) + '</div>'
    '<div class="footer-rule"></div>'
    '<div class="footer-credit">Instituto Municipal de Urbanismo Pereira Passos — Prefeitura da Cidade do Rio de Janeiro</div>'
    '</footer>'
)
_pre_footer_len = len(parts)   # boundary: conteudo de secao termina aqui; o rodape (a seguir) fica fora de qualquer .rsec
parts.append(footer)

# ---- envolve cada secao h2 num container retratil (specification.md §3.1) ----
if section_starts:
    n_sections = len(section_starts)
    _wrapped = list(parts[:section_starts[0][0]])
    for i, (start, title, sid) in enumerate(section_starts):
        end = section_starts[i + 1][0] if i + 1 < n_sections else _pre_footer_len
        heading_html = parts[start]
        body_html = "".join(parts[start + 1:end])
        takeaways = "".join(f"<li>{b}</li>" for b in _lorem_bullets(sid))
        takeaways_html = (
            '<div class="key-takeaways">'
            '<div class="eyebrow kt-label">PRINCIPAIS ACHADOS</div>'
            f'<ul>{takeaways}</ul>'
            '</div>'
        )
        _wrapped.append(
            f'<section class="rsec" id="wrap-{sid}">'
            '<div class="rsec-head">'
            f'<div class="rsec-head-l"><span class="eyebrow rsec-eyebrow">SEÇÃO {i + 1} DE {n_sections}</span><div class="rsec-head-title">{heading_html}</div></div>'
            '<button type="button" class="rsec-toggle" aria-expanded="true">'
            '<span class="rsec-toggle-label">RECOLHER</span>'
            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square"><polyline points="6 9 12 15 18 9"></polyline></svg>'
            '</button>'
            '</div>'
            f'<div class="section-body">{takeaways_html}{body_html}</div>'
            '</section>'
        )
    _wrapped.append(parts[_pre_footer_len])  # rodape, fora de qualquer secao
    parts[:] = _wrapped

# ---- navbar: links para as secoes h2, substitui o antigo Sumario (specification.md §3.6) ----
navbar_links = "".join(
    f'<a href="#{sid}" class="navbar-link">{title}</a>' for level, title, sid in toc if level == 2
)

# ---- sumario: mesma fonte (toc) da navbar, mas aninhado h2 > h3 (formato
# do Sumario antigo, relatorio/specs.md) -- agrupa cada h3 sob o h2 mais
# recente que o precede em `toc`.
_sumario_grupos = []
for _level, _title, _sid in toc:
    if _level == 2:
        _sumario_grupos.append([(_title, _sid), []])
    elif _level == 3 and _sumario_grupos:
        _sumario_grupos[-1][1].append((_title, _sid))
sumario_html = "".join(
    f'<li><a href="#{sid}">{_esc(title)}</a>'
    + ("<ul>" + "".join(f'<li><a href="#{csid}">{_esc(ctitle)}</a></li>' for ctitle, csid in filhos) + "</ul>" if filhos else "")
    + '</li>'
    for (title, sid), filhos in _sumario_grupos
)

body = "\n".join(parts).replace('<span id="gen-date">—</span>', f'<span id="gen-date">Atualizado {gen_date}</span>')
body = body.replace('<!--NAVBAR-->', navbar_links)
body = body.replace('<!--SUMARIO-->', sumario_html)

# CSS e motor JS agora são arquivos estáticos editados à mão (specs/website_refactor Bloco 2):
# website/css/{main,layout,components}.css e website/js/charts.js. O gerador só os referencia.

# Bloco 2: as chamadas de render (dados embutidos) saem do HTML para data/charts.js,
# carregado depois de js/charts.js (mesma ordem de execução de antes: ENGINE, depois RENDER_CALLS).
RENDER_CALLS_JS = ("// GERADO por website/build/build_site.py -- não editar à mão.\n"
                   "(function(){\n\"use strict\";\n" + "\n".join(scripts) + "\n})();\n")

# regras de fundo cartografico dos mapas, coletadas durante a geracao (1 por
# bbox unico -- bairro/AP/RP compartilham a mesma classe, ja que dissolvem da
# mesma geometria base e tem bounds identicos; CAP tem a sua propria)
BASEMAP_CSS = "<style>" + "".join(_BASEMAP_CSS_RULES) + "</style>" if _BASEMAP_CSS_RULES else ""

doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Primeira Infância Carioca</title>
<link rel="stylesheet" href="css/main.css">
<link rel="stylesheet" href="css/layout.css">
<link rel="stylesheet" href="css/components.css">
{BASEMAP_CSS}
</head>
<body>
<div class="doc">
{body}
</div>
<script src="data/geo.js"></script>
<script src="js/charts.js"></script>
<script src="data/charts.js"></script>
</body>
</html>
"""

# ---- escrita (specs/website_refactor) ----------------------------------------
# OUT_DIR = website/ por padrão. Com outro destino (ex. scratchpad para comparar), os
# arquivos estáticos editados à mão são copiados junto, para a pasta abrir sozinha.
import shutil
SITE_DIR = ROOT / "website"
OUT_DIR = Path(OUT_PATH)
_ESTATICOS = ["css", "js", "assets"]
if OUT_DIR.resolve() != SITE_DIR.resolve():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for nome in _ESTATICOS:
        shutil.copytree(SITE_DIR / nome, OUT_DIR / nome, dirs_exist_ok=True)
(OUT_DIR / "data").mkdir(parents=True, exist_ok=True)
# geometria compartilhada (Blocos 3/3b): injeta um <svg> oculto com <defs> no início do <body>
# e expõe window.GEO_NOMES (id -> nome da região, para o tooltip). Só os níveis usados.
GEO_JS = """// GERADO por website/build/build_site.py -- não editar à mão.
(function(){
"use strict";
var D = __DADOS__;
var NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg'), defs = document.createElementNS(NS, 'defs'), nomes = {};
svg.setAttribute('width', '0'); svg.setAttribute('height', '0'); svg.setAttribute('aria-hidden', 'true');
svg.style.position = 'absolute';
Object.keys(D).forEach(function(n){ D[n].forEach(function(r){
  var p = document.createElementNS(NS, 'path'); p.setAttribute('id', r[0]); p.setAttribute('d', r[2]);
  defs.appendChild(p); nomes[r[0]] = r[1];
}); });
svg.appendChild(defs); document.body.insertBefore(svg, document.body.firstChild);
window.GEO_NOMES = nomes;
})();
""".replace("__DADOS__", json.dumps(_GEO_USADOS, ensure_ascii=False, separators=(",", ":")))

_gerados = {"index.html": doc, "data/charts.js": RENDER_CALLS_JS, "data/geo.js": GEO_JS}
for rel, conteudo in _gerados.items():
    with open(OUT_DIR / rel, "w", encoding="utf-8", newline="\n") as f:
        f.write(conteudo)
(OUT_DIR / "assets" / "images").mkdir(parents=True, exist_ok=True)
for nome, conteudo in _BASEMAP_FILES.items():
    (OUT_DIR / "assets" / "images" / nome).write_bytes(conteudo)
print(f"wrote {OUT_DIR}: {len(scripts)} charts, {sum(1 for l,t,s in toc if l==2)} h2 / {sum(1 for l,t,s in toc if l==3)} h3 sections")

# ---- relatório de tamanho + orçamento (specs/website_refactor §4.9) -----------
# Só avisa, não falha: um estouro é sinal para investigar (ex. geometria voltou a
# ser repetida por mapa), não motivo para travar a geração.
import gzip
ORCAMENTO_INDEX = 1_000_000
ORCAMENTO_SITE = 2_000_000
_PUBLICADOS = ["index.html", "404.html", ".nojekyll", "css", "js", "data", "assets"]   # = lista do workflow de deploy
_tamanhos = []
for nome in _PUBLICADOS:
    alvo = OUT_DIR / nome
    arquivos = [alvo] if alvo.is_file() else (sorted(p for p in alvo.rglob("*") if p.is_file()) if alvo.is_dir() else [])
    for arq in arquivos:
        dados = arq.read_bytes()
        _tamanhos.append((arq.relative_to(OUT_DIR).as_posix(), len(dados), len(gzip.compress(dados))))
for rel, bruto, gz in _tamanhos:
    print(f"  {rel:40s} {bruto:>11,} bytes  (gzip {gz:>9,})")
_total, _total_gz = sum(t[1] for t in _tamanhos), sum(t[2] for t in _tamanhos)
print(f"  {'TOTAL publicado':40s} {_total:>11,} bytes  (gzip {_total_gz:>9,})")
_idx = next((t[1] for t in _tamanhos if t[0] == "index.html"), 0)
if _idx > ORCAMENTO_INDEX:
    print(f"AVISO: index.html com {_idx:,} bytes passa do orçamento de {ORCAMENTO_INDEX:,} (specs/website_refactor §4.9)", file=sys.stderr)
if _total > ORCAMENTO_SITE:
    print(f"AVISO: site publicado com {_total:,} bytes passa do orçamento de {ORCAMENTO_SITE:,} (specs/website_refactor §4.9)", file=sys.stderr)
