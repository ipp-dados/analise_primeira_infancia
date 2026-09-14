# -*- coding: utf-8 -*-
"""Build the single consolidated interactive HTML report (relatorio/index.html).

Replaces the old 3-file setup (index.html / lighter_index.html / white_index.html),
which was hand-built by unsaved ad-hoc scripts (see relatorio/specs.md). This script
is the first *persisted* generator: it reads tabelas_finais/*.csv (same source the
PDF pipeline uses) and renders interactive SVG charts via a small JS engine
(lineChart/barChart/groupedBarChart, lifted from the old lighter_index.html and
extended with the "many-series" highlight logic used in analise.py's
serie_temporal_multipla). Per SPEC-visual-identity decision B, this report is
visualization-only: title + source + chart/map + optional data table, no prose/notes
(those stay in the notebook and the PDF). Maps are interleaved in the same position
they appear in analise.py (not grouped in one trailing section), and the page opens
with a persistent navbar linking every h2 section.

This is a direct transcription of analise.py's chart/map call sites, in the same
order they appear there -- if analise.py's sections, column names, exported
filenames, or cell order change, this needs matching edits.

v6 (SPEC-relatorio-interativo) rebuilt the visual identity and interaction model to
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
<defs>/<use>), tracked in SPEC-relatorio-interativo/feature_roadmap.md.

Usage (from project root):
    python .claude/skills/export_pdf_report/scripts/build_html_report.py [out_path]
"""
import base64
import io
import json
import math
import os
import re
import sys
import datetime

import pandas as pd
from PIL import Image

TF = "tabelas_finais"
MAPAS = "mapas"
OUT_PATH = sys.argv[1] if len(sys.argv) > 1 else "relatorio/index.html"

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

FMT_MAP = {'int': 'v=>fmt(v)', 'pct': 'v=>pct(v)', 'pct1': 'v=>pct(v,1)'}

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
    limpos = [remove_outliers_tukey(v) for v in norm]
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

def bar_chart(items, fonte=None, titulo=None):
    norm = _normaliza([it['value'] for it in items])
    limpos = remove_outliers_tukey(norm)
    has_outliers = limpos != norm

    def build(valores):
        elem_id = new_id('c')
        js_items = [
            "{label:%s, value:%s}" % (json.dumps(str(it['label']), ensure_ascii=False), json.dumps(v))
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
    limpos = [remove_outliers_tukey(v) for v in norm]
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

# ------------------------------------------------ SPEC-relatorio-interativo --
# Outliers, option-card (pill selector), CSV download, institutional identity,
# and the SVG choropleth pipeline -- see SPEC-relatorio-interativo/plan.md.

def _esc(s):
    return str(s).replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

def _fmt_ptbr(v, dec=0):
    if v is None:
        return "—"
    s = f"{v:,.{dec}f}"
    s = s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return s

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

def option_card(entries):
    """entries: list de (label, build_fn). build_fn emite exatamente 1 construto
    (pode por sua vez conter um outlier-card). len==1 -> renderiza direto, sem
    coluna de pills (specification.md §3.2)."""
    if len(entries) == 1:
        entries[0][1]()
        return
    panes, pills = [], []
    for i, (label, build_fn) in enumerate(entries):
        start = len(parts)
        build_fn()
        html = "".join(parts[start:]); del parts[start:]
        panes.append(f'<div class="opt-pane"{" hidden" if i else ""}>{html}</div>')
        active = ' data-active="true"' if i == 0 else ''
        pills.append(f'<button type="button" class="pill"{active}>{_esc(label)}</button>')
    parts.append(
        '<div class="option-card">'
        '<div class="pill-col">' + "".join(pills) + '</div>'
        '<div class="opt-panes">' + "".join(panes) + '</div>'
        '</div>'
    )

# ---- institutional logo (embedded once, reused in navbar + footer) --------

def _logo_b64():
    with open("relatorio/assets/ipp-logo.png", "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

LOGO_B64 = _logo_b64()
LOGO_IMG = f'<img src="data:image/png;base64,{LOGO_B64}" alt="Prefeitura do Rio de Janeiro — Instituto Pereira Passos" class="ipp-logo">'

# ---- SVG choropleth pipeline (Bloco 3) -------------------------------------
# Aplicado nesta rodada ao mapa do Censo por bairro (prova de conceito real,
# ver SPEC-relatorio-interativo/tasks.md T3.4) -- os demais ~30 mapas
# continuam como PNG (map_card acima) ate uma rodada de conversao mecanica.

_MAP_W, _MAP_H = 640, 560
_CMAP_TEMA = {'censo': 'Blues', 'natalidade': 'BuGn', 'mortalidade': 'RdPu', 'cadunico': 'YlOrBr'}
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
    return project

def _ring_path(coords, project):
    pts = [project(x, y) for x, y in coords]
    return "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts) + " Z"

def _geom_path_d(geom, project):
    polys = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
    d = []
    for poly in polys:
        d.append(_ring_path(list(poly.exterior.coords), project))
        for interior in poly.interiors:
            d.append(_ring_path(list(interior.coords), project))
    return " ".join(d)

_NIVEL_COL = {"ap": "area_plane", "rp": "cod_rp"}
_NIVEL_LABEL = {"ap": "AP", "rp": "RP", "cap": "CAP"}

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
    raise ValueError(nivel)

def mapa_svg(df, chave_col, valor_col, tema, titulo, legenda_titulo, fonte_dados, bins=None, fmt="int", nivel="bairro"):
    """df: 1 linha por unidade geografica (chave_col identifica a unidade no nivel
    escolhido: codbairro/area_plane/cod_rp/cod_ap_sms). bins: lista de limites
    superiores (contagem absoluta, classes discretas) ou None (percentual/taxa,
    escala continua) -- mesma convencao de mapa_coropletico_bairros em
    analise.py. Emite 1 construto (option_card-compativel) com SVG + legenda +
    tooltip por regiao + toggle de outliers + download CSV."""
    gdf, project, nomes = _geo_nivel(nivel)
    valores = {}
    for _, r in df.iterrows():
        try:
            chave = _chave_norm(r[chave_col], nivel)
        except (ValueError, TypeError):
            continue  # linhas de agregado tipo "Em branco"/"Ignorado" (nao sao uma unidade geografica real)
        valores[chave] = None if pd.isna(r[valor_col]) else float(r[valor_col])
    brutos = list(valores.values())
    limpos = remove_outliers_tukey(brutos)
    limpos_map = dict(zip(valores.keys(), limpos))
    has_outliers = limpos != brutos

    def build(valor_por_regiao):
        elem_id = new_id("m")
        finitos = [v for v in valor_por_regiao.values() if v is not None]
        vmin, vmax = (min(finitos), max(finitos)) if finitos else (0, 1)
        paths, rows = [], []
        for _, row in gdf.iterrows():
            chave = row["_chave"]
            v = valor_por_regiao.get(chave)
            d = _geom_path_d(row.geometry, project)
            if v is None:
                fill = "var(--surface-2)"
            elif bins is not None:
                idx = next((i for i, edge in enumerate(bins) if v <= edge), len(bins))
                fill = _cor_sequencial(tema, (idx + 1) / (len(bins) + 1))
            else:
                frac = (v - vmin) / (vmax - vmin) if vmax > vmin else 0.5
                fill = _cor_sequencial(tema, frac)
            label = nomes.get(chave, str(chave))
            val_txt = _fmt_ptbr(v, 1 if fmt == "pct1" else 0) + ("%" if fmt == "pct1" and v is not None else "")
            paths.append(
                f'<path d="{d}" class="map-region" fill="{fill}" stroke="var(--page)" stroke-width="0.7" '
                f'data-label="{_esc(label)}" data-valor="{_esc(val_txt)}"></path>'
            )
            rows.append((label, v))
        legend_bits = []
        if bins is not None:
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
                legend_bits.append(f'<div class="map-legend-row"><span class="map-legend-sw" style="background:{sw}"></span>{_fmt_ptbr(v, 1)}{"%" if fmt == "pct1" else ""}</div>')
        svg = f'<svg viewBox="0 0 {_MAP_W} {_MAP_H}" class="map-svg" id="{elem_id}">' + "".join(paths) + "</svg>"
        csv = _csv_data_attr([_NIVEL_LABEL.get(nivel, "Bairro"), legenda_titulo or valor_col], rows)
        parts.append(
            f'<div class="out map-svg-card" data-csv="{csv}" data-filename="{_esc(titulo)}.csv">'
            '<button type="button" class="dl-btn" title="Baixar CSV">⭳ CSV</button>'
            f'<div class="chart-subtitle">{_esc(titulo)}</div>'
            '<div class="map-svg-row">'
            f'{svg}'
            f'<div class="map-legend"><div class="eyebrow">{_esc(legenda_titulo or "")}</div>{"".join(legend_bits)}</div>'
            '</div>'
            f'<div class="out-src">{_esc(fonte_dados)}</div>'
            '</div>'
        )
        return elem_id

    if has_outliers:
        with_outliers_toggle(lambda: build(valores), lambda: build(limpos_map), True)
    else:
        build(valores)

# ============================================================ NAVBAR/HEADER ==

parts.append('<div class="topbar-accent"></div>')
parts.append('<nav class="navbar">')
parts.append(
    '<button type="button" class="navbar-burger" id="navbar-burger" aria-expanded="false" aria-controls="navbar-menu">'
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square">'
    '<line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line>'
    '</svg><span class="eyebrow navbar-label">NAVEGAÇÃO</span></button>'
)
parts.append(f'<div class="navbar-logo">{LOGO_IMG}</div>')
parts.append('</nav>')
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

# ================================================================== CENSO ==

h2('\U0001F3D8️ Censo 2022')

h3('Por bairro')
df_censo_bairro = read("censo_por_bairro.csv")
top10 = df_censo_bairro.sort_values("0 a 4 anos", ascending=False).head(10)[["bairro", "0 a 4 anos", "Percentual 0 a 4"]]
top10 = top10.rename(columns={"bairro": "Bairro", "0 a 4 anos": "Crianças 0-4", "Percentual 0 a 4": "% do bairro"})
top10["% do bairro"] = top10["% do bairro"].map(lambda v: f"{v:.1f}%".replace(".", ","))
FONTE_CENSO = "Censo Demográfico 2022 (IBGE/Data.Rio)"
plain_table(top10, fonte=FONTE_CENSO)

h3('População 0-6 por idade/raça/sexo (IBGE SIDRA, 2022)')
FONTE_SIDRA_CENSO = "Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606)"
_ORDEM_IDADE_SIDRA_0_6 = ['Menos de 1 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos', '6 anos']

def _ordenar_idade(df, ordem):
    return df[df["idade"].isin(ordem)].set_index("idade").reindex(ordem).reset_index()

df_censo_raca = _ordenar_idade(read("censo_sidra_populacao_0_6_raca_2022.csv"), _ORDEM_IDADE_SIDRA_0_6)
raca_cols = [c for c in df_censo_raca.columns if c not in ("idade", "Total")]
grouped_bar_chart(df_censo_raca["idade"], series_from_cols(df_censo_raca, raca_cols), fonte=FONTE_SIDRA_CENSO)
df_censo_sexo = _ordenar_idade(read("censo_sidra_populacao_0_6_sexo_2022.csv"), _ORDEM_IDADE_SIDRA_0_6)
sexo_cols = [c for c in df_censo_sexo.columns if c not in ("idade", "Total")]
grouped_bar_chart(df_censo_sexo["idade"], series_from_cols(df_censo_sexo, sexo_cols), fonte=FONTE_SIDRA_CENSO)

h3('Mapas')
mapa_svg(df_censo_bairro, "codbairro", "0 a 4 anos", "censo",
         "Crianças de 0 a 4 anos, por bairro (Censo 2022)", "Crianças 0-4",
         FONTE_CENSO, bins=[1000, 2500, 5000, 10000])
mapa_svg(df_censo_bairro, "codbairro", "Percentual 0 a 4", "censo",
         "% de crianças de 0 a 4 anos, por bairro (Censo 2022)", "% 0-4 anos",
         FONTE_CENSO, fmt='pct1')

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
for _nivel, _info in NIVEIS_PLANEJAMENTO.items():
    df_censo_nivel = _agrega_censo_por_nivel(df_censo_bairro, _nivel)
    mapa_svg(df_censo_nivel, _NIVEL_COL[_nivel], "0 a 4 anos", "censo",
             f"Crianças de 0 a 4 anos, por {_info['nome']} (Censo 2022)", "Crianças 0-4",
             FONTE_CENSO, bins=_info['bins'], nivel=_nivel)
    mapa_svg(df_censo_nivel, _NIVEL_COL[_nivel], "Percentual 0 a 4", "censo",
             f"% de crianças de 0 a 4 anos, por {_info['nome']} (Censo 2022)", "% da população",
             FONTE_CENSO, fmt='pct1', nivel=_nivel)

h3('Série temporal')
df_censo_serie = read("censo_0_a_4_anos_por_ano.csv")
line_chart(df_censo_serie["ano"], [
    {'label': 'Total 0–4 anos', 'values': df_censo_serie['0 a 4 anos']},
    {'label': 'Feminino', 'values': df_censo_serie['Sexo feminino, 0 a 4 anos']},
    {'label': 'Masculino', 'values': df_censo_serie['Sexo masculino, 0 a 4 anos']},
], opts={'height': 230, 'maxXLabels': 3, 'table': True}, fonte="censo_0_a_4_anos_por_ano.csv (Tabela 2974/IBGE)")
line_chart(df_censo_serie["ano"], [
    {'label': 'Percentual 0–4 anos', 'values': df_censo_serie['Percentual 0 a 4 anos'], 'format': 'pct1'},
], opts={'height': 200, 'zeroBase': False, 'maxXLabels': 3, 'table': True}, fonte="censo_0_a_4_anos_por_ano.csv (Tabela 2974/IBGE)")

# ================================================================ CADUNICO ==

h2('\U0001F5C2️ CadÚnico')
FONTE_CADUNICO = "CadÚnico (extração CTPE)"

h3('Por faixa de renda')
df_renda = read("cadunico_por_faixa_etaria_2026.csv")
df_renda_sem_total = df_renda[df_renda["faixa de renda"] != "Total"]
out_pair(
    lambda: bar_chart([{'label': r["faixa de renda"], 'value': r["Crianças"]} for _, r in df_renda_sem_total.iterrows()], fonte=FONTE_CADUNICO, titulo="Crianças"),
    lambda: bar_chart([{'label': r["faixa de renda"], 'value': r["Famílias"]} for _, r in df_renda_sem_total.iterrows()], fonte=FONTE_CADUNICO, titulo="Famílias"),
)

h3('Por idade')
df_idade = read("cadunico_por_idade_2026.csv")
df_idade["idade_lbl"] = df_idade["idade"].astype(int).map(lambda i: f"{i} ano" if i == 1 else f"{i} anos")
out_pair(
    lambda: bar_chart([{'label': r["idade_lbl"], 'value': r["Crianças"]} for _, r in df_idade.iterrows()], fonte=FONTE_CADUNICO, titulo="Crianças"),
    lambda: bar_chart([{'label': r["idade_lbl"], 'value': r["Famílias"]} for _, r in df_idade.iterrows()], fonte=FONTE_CADUNICO, titulo="Famílias"),
)

h3('Mapas')
df_map_cadunico_criancas = read("tabela_mapa_cadunico_criancas_2026.csv")
mapa_svg(df_map_cadunico_criancas, "codbairro", "Crianças", "cadunico",
         "Crianças (0-6 anos) no CadÚnico, por bairro", "Crianças",
         FONTE_CADUNICO, bins=[250, 750, 1500, 3000])
df_map_cadunico_0_4 = read("tabela_mapa_cadunico_primeira_infancia_2026.csv")
mapa_svg(df_map_cadunico_0_4, "codbairro", "Crianças", "cadunico",
         "Crianças (0-4 anos) no CadÚnico, por bairro", "Crianças",
         FONTE_CADUNICO, bins=[200, 500, 1000, 2000])
mapa_svg(df_map_cadunico_0_4, "codbairro", "Percentual Primeira Inf. Cadúnico", "cadunico",
         "% de crianças 0-4 anos no CadÚnico sobre o Censo, por bairro", "% CadÚnico/Censo",
         FONTE_CADUNICO, fmt="pct1")

# ============================================================== DATASUS ===

h2('\U0001F3E5 DataSUS/Tabnet')
FONTE_DATASUS = "DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro"

h3('Nascidos vivos')
df_map_nv = read("tabela_mapa_bairros_nascidos_vivos_bruto.csv")
mapa_svg(df_map_nv, "codigo", "value", "natalidade",
         "Nascidos vivos por bairro (2025)", "Nascidos vivos",
         FONTE_DATASUS, bins=[200, 400, 800, 1500])
df_nv = read("nascidos_vivos_por_ano.csv")
line_chart(df_nv["ano"], [{'label': 'Nascidos vivos', 'values': df_nv['nascidos vivos']}], opts={'height': 220, 'table': True}, fonte=FONTE_DATASUS)

h3('Nascidos abaixo do peso')
df_map_bp = read("tabela_mapa_bairros_nascidos_abaixo_peso.csv")
df_map_bp_2025 = df_map_bp[df_map_bp["ano"] == 2025]
mapa_svg(df_map_bp_2025, "codigo", "Nascidos abaixo peso", "natalidade",
         "Nascidos com baixo peso por bairro (2025)", "Nascidos abaixo do peso",
         FONTE_DATASUS, bins=[15, 30, 60, 120])
mapa_svg(df_map_bp_2025, "codigo", "percentual abaixo do peso", "natalidade",
         "% de nascidos com baixo peso por bairro (2025)", "% baixo peso",
         FONTE_DATASUS, fmt="pct1")
df_bp = read("nascidos_abaixo_peso_por_ano.csv")
line_chart(df_bp["ano"], [{'label': '% abaixo do peso', 'values': df_bp['percentual abaixo do peso'], 'format': 'pct1'}], opts={'height': 220, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)

h3('Mortalidade por raça/cor (0-364 dias)')
RACA_LABEL = {"amarela": "Amarela", "branca": "Branca", "indigena": "Indígena", "parda": "Parda", "preta": "Preta", "nao_informado": "Não informado"}
RACAS = list(RACA_LABEL)
df_raca = read("mortalidade_raca_municipio_ano.csv")
line_chart(df_raca["ano"], series_from_cols(df_raca, [f"obitos_{r}" for r in RACAS], {f"obitos_{r}": RACA_LABEL[r] for r in RACAS}), opts={'height': 260, 'table': True}, fonte=FONTE_DATASUS)
line_chart(df_raca["ano"], series_from_cols(df_raca, [f"percentual_{r}" for r in RACAS], {f"percentual_{r}": RACA_LABEL[r] for r in RACAS}, fmt='pct1'), opts={'height': 260, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)
df_map_raca = read("mortalidade_raca_bairro_ano.csv")
df_map_raca_2025 = df_map_raca[df_map_raca["ano"] == 2025]
mapa_svg(df_map_raca_2025, "codigo", "obitos_total", "mortalidade",
         "Óbitos de 0 a 364 dias por bairro (2025)", "Óbitos",
         FONTE_DATASUS, bins=[2, 5, 10, 20])
mapa_svg(df_map_raca_2025, "codigo", "percentual_total", "mortalidade",
         "Taxa de mortalidade infantil (0-364 dias) por bairro (2025)", "% s/ nascidos vivos",
         FONTE_DATASUS, fmt="pct1")

# ============================================================ EVITAVEIS ===

h2('⛓️ Óbitos por causas evitáveis')
FONTE_EVITAVEIS = "SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro"

h3('Por raça/cor (0-364 dias)')
df_evit_raca = read("mortalidade_causas_evitaveis_raca_municipio_ano.csv")
line_chart(df_evit_raca["ano"], series_from_cols(df_evit_raca, [f"obitos_evitaveis_{r}" for r in RACAS], {f"obitos_evitaveis_{r}": RACA_LABEL[r] for r in RACAS}), opts={'height': 260, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS)
line_chart(df_evit_raca["ano"], series_from_cols(df_evit_raca, [f"percentual_evitaveis_{r}" for r in RACAS], {f"percentual_evitaveis_{r}": RACA_LABEL[r] for r in RACAS}, fmt='pct1'), opts={'height': 260, 'zeroBase': False, 'table': True}, fonte=FONTE_EVITAVEIS)

h4('Sem "não informada" (a partir de 1997)')
RACAS_SEM_NI = [r for r in RACAS if r != "nao_informado"]
df_evit_raca_sem = df_evit_raca[df_evit_raca["ano"] > 1996]
line_chart(df_evit_raca_sem["ano"], series_from_cols(df_evit_raca_sem, [f"obitos_evitaveis_{r}" for r in RACAS_SEM_NI], {f"obitos_evitaveis_{r}": RACA_LABEL[r] for r in RACAS_SEM_NI}), opts={'height': 240, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS)
line_chart(df_evit_raca_sem["ano"], series_from_cols(df_evit_raca_sem, [f"percentual_evitaveis_{r}" for r in RACAS_SEM_NI], {f"percentual_evitaveis_{r}": RACA_LABEL[r] for r in RACAS_SEM_NI}, fmt='pct1'), opts={'height': 240, 'zeroBase': False, 'table': True}, fonte=FONTE_EVITAVEIS)

h3('Por grupo/subgrupo de causa (CID-10)')
for faixa_id, faixa_titulo in [("", "0-364 dias"), ("_0_6", "0-6 dias"), ("_7_27", "7-27 dias"), ("_28_364", "28-364 dias")]:
    h5(faixa_titulo)
    df_g = read(f"mortalidade_causas_evitaveis_grupo{faixa_id}_ano.csv")
    gcols = [c for c in df_g.columns if c != "ano"]
    line_chart(df_g["ano"], series_from_cols(df_g, gcols, {c: clean_causa(c) for c in gcols}), opts={'height': 240, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS)
    df_s = read(f"mortalidade_causas_evitaveis_subgrupo{faixa_id}_ano.csv")
    scols = [c for c in df_s.columns if c != "ano"]
    line_chart(df_s["ano"], series_from_cols(df_s, scols, {c: clean_causa(c) for c in scols}), opts={'height': 280, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS)

h4('Comparação entre faixas etárias (2025)')
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
grouped_bar_chart(faixas_2025, series_2025, fonte=FONTE_EVITAVEIS)

h3('Primeira infância, por Área Programática de Saúde (CAP)')
df_cap_faixa = read("mortalidade_evitaveis_cap_faixa_ano.csv")
df_grupo_cap_faixa = read("mortalidade_evitaveis_grupo_cap_faixa_ano.csv")

h4('Panorama municipal, por subgrupo')
for faixa in ['menores de 1 ano', 'de 1 a 4 anos', 'menores de 5 anos']:
    h5(faixa.capitalize())
    sub = df_cap_faixa[df_cap_faixa["faixa_etaria"] == faixa].groupby(["subgrupo", "ano"], as_index=False)["obitos"].sum()
    subgrupos = list(dict.fromkeys(sub["subgrupo"]))
    anos = sorted(sub["ano"].unique().tolist())
    series = []
    for sg in subgrupos:
        d = sub[sub["subgrupo"] == sg].set_index("ano")["obitos"]
        series.append({'label': clean_causa(sg), 'values': [d.get(a) for a in anos]})
    line_chart(anos, series, opts={'height': 260, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS)

h4('Por CAP e faixa etária')
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
        _entries_cap_faixa.append((
            f"{faixa_lbl} · {subgrupo_lbl}",
            lambda anos=anos, series=series: line_chart(anos, series, opts={'height': 240, 'maxXLabels': 6, 'legendTitle': 'CAP', 'table': True}, fonte=FONTE_EVITAVEIS)
        ))
option_card(_entries_cap_faixa)

h4('Grupo evitável, por CAP')
# 3 faixas, cada uma com o par absoluto+percentual (antes h5 por faixa com 2
# line_chart cada) -- viram 1 chart-card, pill = faixa, cada opcao mostra o
# par lado a lado (out_pair).
GRUPO1_COL = "1. Causas evitáveis"
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
        )
    ))
option_card(_entries_grupo_cap)

h4('Gestação e parto, menores de 1 ano, por CAP')
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
    h5(subgrupo_lbl)
    line_chart(anos, series, opts={'height': 240, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS)

h4('Panorama municipal (< 5 anos) e taxa')
df_menores5_sub = read("obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv")
sgs = list(dict.fromkeys(df_menores5_sub["subgrupo"]))
anos_m5 = sorted(df_menores5_sub["ano"].unique().tolist())
series_m5 = []
for sg in sgs:
    d = df_menores5_sub[df_menores5_sub["subgrupo"] == sg].set_index("ano")["obitos"]
    series_m5.append({'label': clean_causa(sg), 'values': [d.get(a) for a in anos_m5]})
line_chart(anos_m5, series_m5, opts={'height': 260, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS)
df_taxa_m5 = read("taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv")
line_chart(df_taxa_m5["ano"], [{'label': 'Taxa por mil NV', 'values': df_taxa_m5['taxa_por_mil'], 'format': 'pct1'}], opts={'height': 220, 'zeroBase': False, 'table': True}, fonte=FONTE_EVITAVEIS)

h4('Mapas')
FAIXAS_PRIMEIRA_INFANCIA = {
    'menores_1_ano':  {'rotulo': 'menores de 1 ano',   'bins_absoluto': [20, 40, 60, 80]},
    '1_a_4_anos':     {'rotulo': 'de 1 a 4 anos',       'bins_absoluto': [2, 4, 7, 10]},
    'menores_5_anos': {'rotulo': 'menores de 5 anos',   'bins_absoluto': [20, 45, 70, 95]},
}
df_evitaveis_cap_2025 = read("mortalidade_evitaveis_cap_2025.csv")
for sufixo, info in FAIXAS_PRIMEIRA_INFANCIA.items():
    df_faixa_2025 = df_evitaveis_cap_2025[df_evitaveis_cap_2025["faixa_etaria"] == info['rotulo']]
    mapa_svg(df_faixa_2025, "cod_ap_sms", "evitaveis", "mortalidade",
             f"Óbitos por causas evitáveis, {info['rotulo']}, por CAP (2025)", "Óbitos",
             FONTE_EVITAVEIS, bins=info['bins_absoluto'], nivel="cap")
    mapa_svg(df_faixa_2025, "cod_ap_sms", "percentual_evitaveis", "mortalidade",
             f"Percentual de óbitos evitáveis, {info['rotulo']}, por CAP (2025)", "% evitáveis",
             FONTE_EVITAVEIS, fmt="pct1", nivel="cap")
_SUBGRUPOS_COMPONENTE_C = {'gestacao': 'Gestação', 'parto': 'Parto'}
_BINS_SUBGRUPO_COMPONENTE_C = {'gestacao': [10, 20, 30, 40], 'parto': [2, 4, 6, 8]}
for slug, rotulo in _SUBGRUPOS_COMPONENTE_C.items():
    df_subgrupo_2025 = read(f"tabela_mapa_obitos_evitaveis_{slug}_menores_1_ano_cap_2025.csv")
    mapa_svg(df_subgrupo_2025, "cod_ap_sms", "obitos", "mortalidade",
             f"Óbitos evitáveis - {rotulo}, menores de 1 ano, por CAP (2025)", "Óbitos",
             FONTE_EVITAVEIS, bins=_BINS_SUBGRUPO_COMPONENTE_C[slug], nivel="cap")

# ==================================================== GRAVIDEZ/PUERPERIO ==

h2('\U0001F930 Gravidez e puerpério')
df_grav = read("obitos_gravidez_por_ano.csv")
line_chart(df_grav["ano"], [{'label': 'Óbitos', 'values': df_grav['óbitos-gravidez']}], opts={'height': 200, 'table': True}, fonte=FONTE_DATASUS)
df_map_grav = read("obitos_gravidez_bairro_ano.csv")
df_map_grav_2025 = df_map_grav[df_map_grav["ano"] == 2025]
mapa_svg(df_map_grav_2025, "codigo", "óbitos-gravidez", "mortalidade",
         "Óbitos durante a gravidez por bairro (2025)", "Óbitos",
         FONTE_DATASUS, bins=[0, 1])
df_puerp = read("obitos_puerperio_por_ano.csv")
line_chart(df_puerp["ano"], [{'label': 'Óbitos', 'values': df_puerp['óbitos-puerpério']}], opts={'height': 200, 'table': True}, fonte=FONTE_DATASUS)
df_map_puerp = read("obitos_puerperio_bairro_ano.csv")
df_map_puerp_2025 = df_map_puerp[df_map_puerp["ano"] == 2025]
mapa_svg(df_map_puerp_2025, "codigo", "óbitos-puerpério", "mortalidade",
         "Óbitos durante o puerpério por bairro (2025)", "Óbitos",
         FONTE_DATASUS, bins=[0, 1, 2])

# ======================================================== NEONATAL ========

h2('\U0001FA7A Mortalidade neonatal')
h3('Precoce (0-6 dias)')
df_prec = read("mortalidade_neonatal_precoce_por_ano.csv")
line_chart(df_prec["ano"], [{'label': 'Taxa (‰)', 'values': df_prec['taxa_mortalidade_precoce'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)
df_map_neo_prec = read("mortalidade_neonatal_precoce_bairro_ano.csv")
df_map_neo_prec_2025 = df_map_neo_prec[df_map_neo_prec["ano"] == 2025]
mapa_svg(df_map_neo_prec_2025, "codigo", "obitos precoces", "mortalidade",
         "Óbitos precoces (0-6 dias) por bairro (2025)", "Óbitos",
         FONTE_DATASUS, bins=[1, 3, 6, 12])
mapa_svg(df_map_neo_prec_2025, "codigo", "taxa_mortalidade_precoce", "mortalidade",
         "Taxa de óbitos precoces por bairro (2025)", "Taxa por mil NV",
         FONTE_DATASUS, fmt="pct1")

h3('Tardia (7-27 dias)')
df_tard = read("mortalidade_neonatal_tardia_por_ano.csv")
line_chart(df_tard["ano"], [{'label': 'Taxa (‰)', 'values': df_tard['taxa_obitos_tardios'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)
df_map_neo_tard = read("mortalidade_neonatal_tardia_bairro_ano.csv")
df_map_neo_tard_2025 = df_map_neo_tard[df_map_neo_tard["ano"] == 2025]
mapa_svg(df_map_neo_tard_2025, "codigo", "obitos_tardios", "mortalidade",
         "Óbitos tardios (7-27 dias) por bairro (2025)", "Óbitos",
         FONTE_DATASUS, bins=[1, 2, 4, 8])
mapa_svg(df_map_neo_tard_2025, "codigo", "taxa_obitos_tardios", "mortalidade",
         "Taxa de óbitos tardios por bairro (2025)", "Taxa por mil NV",
         FONTE_DATASUS, fmt="pct1")

h3('Pós-neonatal (28-364 dias)')
df_inf = read("mortalidade_infantil_pos_neonatal_total_por_ano.csv")
line_chart(df_inf["ano"], [{'label': 'Taxa pós-neonatal (‰)', 'values': df_inf['taxa_mortalidade_pos_neonatal'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)
df_map_pos_neo = read("mortalidade_infantil_pos_neonatal_total_bairro_ano.csv")
df_map_pos_neo_2025 = df_map_pos_neo[df_map_pos_neo["ano"] == 2025]
mapa_svg(df_map_pos_neo_2025, "codigo", "obitos_28_364", "mortalidade",
         "Óbitos pós-neonatais (28-364 dias) por bairro (2025)", "Óbitos",
         FONTE_DATASUS, bins=[1, 2, 4, 8])
mapa_svg(df_map_pos_neo_2025, "codigo", "taxa_mortalidade_pos_neonatal", "mortalidade",
         "Taxa de mortalidade pós-neonatal por bairro (2025)", "Taxa por mil NV",
         FONTE_DATASUS, fmt="pct1")

h3('Total (0-364 dias)')
line_chart(df_inf["ano"], [{'label': 'Taxa infantil total (‰)', 'values': df_inf['taxa_mortalidade_infantil'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)
mapa_svg(df_map_pos_neo_2025, "codigo", "obitos_0_364", "mortalidade",
         "Óbitos infantis (0-364 dias) por bairro (2025)", "Óbitos",
         FONTE_DATASUS, bins=[2, 5, 10, 20])
mapa_svg(df_map_pos_neo_2025, "codigo", "taxa_mortalidade_infantil", "mortalidade",
         "Taxa de mortalidade infantil por bairro (2025)", "Taxa por mil NV",
         FONTE_DATASUS, fmt="pct1")

# ============================================================== SISVAN ====

h2('\U0001F957 SISVAN')
FONTE_SISVAN = "SISVAN/DATASUS"
df_desn = read("sisvan_desnutricao_por_ano.csv")
line_chart(df_desn["ano"], [{'label': '% baixo peso', 'values': df_desn['Percent. baixo peso total'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_SISVAN)
df_sobre = read("sisvan_sobrepeso_por_ano.csv")
line_chart(df_sobre["ano"], [{'label': '% sobrepeso', 'values': df_sobre['Percent. sobrepeso total'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_SISVAN)
line_chart(df_sobre["ano"], [{'label': '% obesidade', 'values': df_sobre['obesidade_percentual'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_SISVAN)

# ======================================================== VACINACAO =======

h2('\U0001F489 Cobertura vacinal (EPI)')
FONTE_EPI = "EPI/SVS-Rio, cobertura vacinal por imunobiológico"
df_vac = read("cobertura_vacinal_epi_por_ano.csv")
vac_cols = [c for c in df_vac.columns if c != "ano"]
line_chart(df_vac["ano"], series_from_cols(df_vac, vac_cols, fmt='pct1'), opts={'height': 280, 'maxXLabels': 8, 'table': True}, fonte=FONTE_EPI)

df_vac_comp = read("cobertura_vacinal_epi_comparativo_anos.csv")
df_vac_comp_wide = df_vac_comp.pivot(index="ano", columns="imunobiologico", values="cobertura").reset_index()
comp_cols = [c for c in df_vac_comp_wide.columns if c != "ano"]
grouped_bar_chart(df_vac_comp_wide["ano"], series_from_cols(df_vac_comp_wide, comp_cols, fmt='pct1'), opts={'height': 320}, fonte=FONTE_EPI)

# ========================================================= EDUCACAO =======

h2('\U0001F393 Educação')
FONTE_SIDRA_EDU = "Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057)"

h3('Frequência escolar 0-5 anos (IBGE SIDRA)')
_ORDEM_IDADE_SIDRA_0_5 = ['0 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos']
_ORDEM_IDADE_SIDRA_0_6_EDU = ['0 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos', '6 anos']

df_freq_raca = _ordenar_idade(read("sidra_frequencia_escola_0_5_raca_2022.csv"), _ORDEM_IDADE_SIDRA_0_5)
fr_cols = [c for c in df_freq_raca.columns if c not in ("idade", "Total")]
grouped_bar_chart(df_freq_raca["idade"], series_from_cols(df_freq_raca, fr_cols), fonte=FONTE_SIDRA_EDU)
df_freq_sexo = _ordenar_idade(read("sidra_frequencia_escola_0_5_sexo_2022.csv"), _ORDEM_IDADE_SIDRA_0_5)
fs_cols = [c for c in df_freq_sexo.columns if c not in ("idade", "Total")]
grouped_bar_chart(df_freq_sexo["idade"], series_from_cols(df_freq_sexo, fs_cols), fonte=FONTE_SIDRA_EDU)

h3('Taxa de frequência escolar 0-6 anos (IBGE SIDRA)')
df_taxa_raca = _ordenar_idade(read("sidra_taxa_frequencia_0_6_raca_2022.csv"), _ORDEM_IDADE_SIDRA_0_6_EDU)
tr_cols = [c for c in df_taxa_raca.columns if c not in ("idade", "Total")]
grouped_bar_chart(df_taxa_raca["idade"], series_from_cols(df_taxa_raca, tr_cols, fmt='pct1'), fonte=FONTE_SIDRA_EDU)
df_taxa_sexo = _ordenar_idade(read("sidra_taxa_frequencia_0_6_sexo_2022.csv"), _ORDEM_IDADE_SIDRA_0_6_EDU)
ts_cols = [c for c in df_taxa_sexo.columns if c not in ("idade", "Total")]
grouped_bar_chart(df_taxa_sexo["idade"], series_from_cols(df_taxa_sexo, ts_cols, fmt='pct1'), fonte=FONTE_SIDRA_EDU)

h3('Frequência escolar por idade (PNAD Contínua)')
df_pnad = read("frequencia_escolar_pnad_por_idade.csv")
bar_chart([{'label': r["Idade"], 'value': r["Total"] * 100} for _, r in df_pnad.iterrows()], fonte="PNAD Contínua (IBGE)")

h3('Matrículas 0 a 6 anos')
df_mat = read("matriculas_0_a_6_por_ano.csv").sort_values("ano")
line_chart(df_mat["ano"], [{'label': 'Matrículas', 'values': df_mat['matriculas']}], opts={'height': 200, 'table': True}, fonte="Censo Escolar/INEP")

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
        _wrapped.append(
            f'<section class="rsec" id="wrap-{sid}">'
            '<div class="rsec-head">'
            f'<div class="rsec-head-l"><span class="eyebrow rsec-eyebrow">SEÇÃO {i + 1} DE {n_sections}</span>{heading_html}</div>'
            '<button type="button" class="rsec-toggle" aria-expanded="true">'
            '<span class="rsec-toggle-label">RECOLHER</span>'
            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square"><polyline points="6 9 12 15 18 9"></polyline></svg>'
            '</button>'
            '</div>'
            f'<div class="section-body">{body_html}</div>'
            '</section>'
        )
    _wrapped.append(parts[_pre_footer_len])  # rodape, fora de qualquer secao
    parts[:] = _wrapped

# ---- navbar: links para as secoes h2, substitui o antigo Sumario (specification.md §3.6) ----
navbar_links = "".join(
    f'<a href="#{sid}" class="navbar-link">{title}</a>' for level, title, sid in toc if level == 2
)

body = "\n".join(parts).replace('<span id="gen-date">—</span>', f'<span id="gen-date">Atualizado {gen_date}</span>')
body = body.replace('<!--NAVBAR-->', navbar_links)

CSS = r"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,440;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

  :root{
    --page:        #FFFFFF;
    --surface:     #FFFFFF;
    --surface-2:   #F7F8F8;
    --ink:         #1C1E1D;
    --ink-2:       #5B615F;
    --ink-3:       #949B99;
    --hairline:    rgba(20,30,27,0.08);
    --hairline-2:  rgba(20,30,27,0.045);
    --accent:      #2E9678;
    --accent-ink:  #123128;
    --accent-soft: #E9F6F1;
    --shadow:      0 1px 2px rgba(20,30,27,.03), 0 12px 28px -16px rgba(20,30,27,.12);
    --shadow-hover:0 4px 10px rgba(20,30,27,.05), 0 20px 40px -18px rgba(20,30,27,.18);

    --c1: #6a95c8; --c1d:#87aad4;
    --c2: #d28060; --c2d:#d19e8a;
    --c3: #359c78; --c3d:#89d2b9;
    --c4: #deb254; --c4d:#e0be7b;
    --c5: #ca688d; --c5d:#cc8ea5;
    --c6: #4aa64a; --c6d:#7be07b;
    --c7: #8177bb; --c7d:#928ad1;
    --c8: #cc6766; --c8d:#d28989;
    --c9: #bc9776; --c9d:#bfad9c;
    --c10:#b67c99; --c10d:#c398b3;
    --c11:#8e9ea4; --c11d:#a5b2b6;
    --c-muted: #d4d4d4; --c-muted-d:#5a6663;

    --font-display: 'Fraunces', Georgia, 'Times New Roman', serif;
    --font-body: 'IBM Plex Sans', -apple-system, 'Segoe UI', sans-serif;
    --font-mono: 'IBM Plex Mono', ui-monospace, 'SFMono-Regular', Menlo, monospace;
  }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){
      --page:        #14201C;
      --surface:     #1B2925;
      --surface-2:   #21302B;
      --ink:         #EDEEE9;
      --ink-2:       #B7C0BB;
      --ink-3:       #7C8985;
      --hairline:    rgba(255,255,255,0.13);
      --hairline-2:  rgba(255,255,255,0.07);
      --accent:      #88b4aa;
      --accent-ink:  #10201b;
      --accent-soft: #1D302B;
      --shadow:      0 1px 2px rgba(0,0,0,.4), 0 8px 26px -12px rgba(0,0,0,.6);
      --shadow-hover:0 4px 12px rgba(0,0,0,.5), 0 20px 44px -16px rgba(0,0,0,.7);
      --c1:var(--c1d);--c2:var(--c2d);--c3:var(--c3d);--c4:var(--c4d);--c5:var(--c5d);--c6:var(--c6d);--c7:var(--c7d);--c8:var(--c8d);--c9:var(--c9d);--c10:var(--c10d);--c11:var(--c11d);--c-muted:var(--c-muted-d);
    }
  }
  :root[data-theme="dark"]{
    --page:        #14201C;
    --surface:     #1B2925;
    --surface-2:   #21302B;
    --ink:         #EDEEE9;
    --ink-2:       #B7C0BB;
    --ink-3:       #7C8985;
    --hairline:    rgba(255,255,255,0.13);
    --hairline-2:  rgba(255,255,255,0.07);
    --accent:      #88b4aa;
    --accent-ink:  #10201b;
    --accent-soft: #1D302B;
    --shadow:      0 1px 2px rgba(0,0,0,.4), 0 8px 26px -12px rgba(0,0,0,.6);
    --shadow-hover:0 4px 12px rgba(0,0,0,.5), 0 20px 44px -16px rgba(0,0,0,.7);
    --c1:var(--c1d);--c2:var(--c2d);--c3:var(--c3d);--c4:var(--c4d);--c5:var(--c5d);--c6:var(--c6d);--c7:var(--c7d);--c8:var(--c8d);--c9:var(--c9d);--c10:var(--c10d);--c11:var(--c11d);--c-muted:var(--c-muted-d);
  }

  *{box-sizing:border-box;}
  body{
    margin:0; background:var(--page); color:var(--ink);
    font-family:var(--font-body); line-height:1.6; font-size:16px;
    -webkit-font-smoothing:antialiased;
  }
  a{color:var(--accent);}
  code{font-family:var(--font-mono); font-size:.92em; background:var(--hairline-2); padding:.1em .35em; border-radius:3px;}

  .doc{max-width:880px; margin:0 auto; padding:64px 24px 110px;}

  header.doc-head{margin-bottom:8px;}
  header.doc-head h1{
    font-family:var(--font-display); font-weight:600; font-size:clamp(1.9rem,4.4vw,2.7rem);
    margin:0 0 8px; line-height:1.12; text-wrap:balance; letter-spacing:-.01em;
    display:flex; align-items:center; gap:14px;
  }
  header.doc-head h1 .glyph{font-size:.82em; flex:none;}
  header.doc-head .sub{color:var(--ink-2); font-size:1.02rem; max-width:68ch; margin:0 0 18px;}
  header.doc-head .meta{
    display:flex; flex-wrap:wrap; gap:6px 16px; font-family:var(--font-mono); font-size:.76rem;
    color:var(--ink-3); padding-bottom:28px;
  }

  /* ---------- table of contents ---------- */
  .toc{
    background:var(--surface-2); border:1px solid var(--hairline); border-radius:12px;
    padding:22px 26px 20px; margin:0 0 48px;
  }
  .toc-label{
    font-family:var(--font-body); font-weight:600; font-size:.76rem; color:var(--ink-3);
    text-transform:uppercase; letter-spacing:.08em; margin:0 0 12px;
  }
  ul.toc-list{
    list-style:none; margin:0; padding:0; columns:2; column-gap:32px;
  }
  ul.toc-list > li{break-inside:avoid; margin:0 0 10px;}
  ul.toc-list > li > a{
    font-weight:600; color:var(--ink); text-decoration:none; font-size:.92rem;
  }
  ul.toc-list > li > a:hover{color:var(--accent);}
  ul.toc-list ul{list-style:none; margin:5px 0 0; padding:0 0 0 14px; border-left:1px solid var(--hairline);}
  ul.toc-list ul li{margin:4px 0;}
  ul.toc-list ul a{color:var(--ink-2); text-decoration:none; font-size:.82rem;}
  ul.toc-list ul a:hover{color:var(--accent); text-decoration:underline;}

  h2{
    font-family:var(--font-display); font-weight:600; font-size:clamp(1.5rem,3vw,1.85rem);
    margin:68px 0 4px; padding-top:32px; border-top:1px solid var(--hairline); line-height:1.2;
    text-wrap:balance; scroll-margin-top:24px;
  }
  h2:first-of-type{margin-top:0; padding-top:0; border-top:none;}
  h3{
    font-family:var(--font-display); font-weight:600; font-size:1.4rem;
    margin:44px 0 14px; line-height:1.2; scroll-margin-top:24px;
  }
  h4{
    font-family:var(--font-display); font-weight:600; font-size:1.16rem;
    margin:34px 0 12px;
  }
  h5{
    font-family:var(--font-body); font-weight:600; font-size:1rem;
    margin:28px 0 10px; color:var(--ink);
  }
  h6{
    font-family:var(--font-body); font-weight:600; font-size:.88rem;
    margin:22px 0 8px; color:var(--ink-2); text-transform:uppercase; letter-spacing:.03em;
  }

  .out{
    margin:14px 0 8px; background:var(--surface); border:2px solid var(--ink); border-radius:0;
    box-shadow:none; padding:22px 24px 16px;
  }
  .out-pair{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:18px; margin:14px 0 8px;}
  .chart-subtitle{
    font-family:var(--font-body); font-weight:600; font-size:.8rem; color:var(--ink-2);
    text-transform:uppercase; letter-spacing:.05em; margin:0 0 12px;
  }

  /* ---------- maps: floating, no card chrome ---------- */
  .map-gallery{display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:30px; margin:16px 0 36px;}
  .map-card{margin:0; background:transparent; border:none; box-shadow:none;}
  .map-card img{
    display:block; width:100%; height:auto; border-radius:10px;
    box-shadow:var(--shadow); transition:box-shadow .2s ease, transform .2s ease;
  }
  .map-card img:hover{box-shadow:var(--shadow-hover); transform:translateY(-3px);}
  .map-cap{padding:12px 4px 0; font-size:.82rem; color:var(--ink-2); text-align:center;}

  .out-src{font-family:var(--font-mono); font-size:.7rem; color:var(--ink-3); margin-top:10px; padding-top:8px; border-top:1px solid var(--hairline-2);}

  .chart-wrap{position:relative;}
  .chart-legend{display:flex; flex-wrap:wrap; gap:5px 14px; margin-bottom:10px;}
  .legend-item{display:flex; align-items:center; gap:6px; font-size:.79rem; color:var(--ink-2); white-space:nowrap;}
  .legend-item i{width:9px; height:9px; border-radius:50%; display:inline-block; flex:none;}
  .chart-svg{width:100%; height:auto; display:block; overflow:visible;}
  .grid-line{stroke:var(--hairline); stroke-width:1;}
  .axis-label{font-family:var(--font-mono); font-size:9px; fill:var(--ink-3);}
  .end-label{font-family:var(--font-mono); font-size:10.5px; font-weight:600; dominant-baseline:middle;}
  .extreme-label{font-family:var(--font-mono); font-size:8.5px; font-weight:600;}
  .hover-line{stroke:var(--ink-3); stroke-width:1; stroke-dasharray:2 3;}
  .hover-dot{stroke:var(--surface); stroke-width:2;}
  .chart-tooltip{
    position:absolute; top:4px; display:none; pointer-events:none; z-index:5;
    background:var(--surface); border:1px solid var(--hairline); border-radius:6px; box-shadow:var(--shadow-hover);
    padding:8px 11px; font-size:.76rem; min-width:104px; max-width:240px;
  }
  .tt-year{font-family:var(--font-mono); color:var(--ink-3); margin-bottom:3px; font-size:.68rem; letter-spacing:.03em;}
  .tt-row{display:flex; align-items:center; gap:6px; color:var(--ink-2); white-space:nowrap; padding:1px 0;}
  .tt-row i{width:7px; height:7px; border-radius:50%; flex:none;}
  .tt-row b{color:var(--ink); font-family:var(--font-mono); font-variant-numeric:tabular-nums;}

  .bar-chart{display:flex; flex-direction:column; gap:8px; min-width:0;}
  .bar-row{display:grid; grid-template-columns:minmax(78px,180px) 1fr auto; gap:10px; align-items:center; min-width:0;}
  .bar-label{font-size:.8rem; color:var(--ink-2); line-height:1.25; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
  .bar-track{height:20px; background:var(--hairline-2); border-radius:4px; overflow:hidden; position:relative; min-width:0;}
  .bar-fill{
    height:100%; border-radius:4px; width:0%; transition:width .9s cubic-bezier(.16,.9,.25,1); min-width:2px;
  }
  @media (prefers-reduced-motion:reduce){ .bar-fill{transition:none;} }
  .bar-value{
    font-family:var(--font-mono); font-size:.74rem; font-weight:600; color:var(--ink);
    white-space:nowrap; text-align:right; font-variant-numeric:tabular-nums;
  }

  details.data-table{margin-top:12px; font-size:.82rem;}
  details.data-table summary{
    cursor:pointer; color:var(--ink-3); font-family:var(--font-mono); font-size:.72rem; padding:3px 0;
  }
  details.data-table table{width:100%; border-collapse:collapse; margin-top:8px; font-variant-numeric:tabular-nums;}
  details.data-table th, details.data-table td{
    text-align:right; padding:4px 7px; border-bottom:1px solid var(--hairline-2); font-size:.76rem; white-space:nowrap;
  }
  details.data-table th:first-child, details.data-table td:first-child{text-align:left;}
  details.data-table th{color:var(--ink-3); font-weight:500;}
  .table-scroll{overflow-x:auto;}

  table.plain{width:100%; border-collapse:collapse; font-size:.86rem; margin:14px 0;}
  table.plain th, table.plain td{text-align:right; padding:6px 10px; border-bottom:1px solid var(--hairline-2); font-variant-numeric:tabular-nums;}
  table.plain th:first-child, table.plain td:first-child{text-align:left; font-variant-numeric:normal;}
  table.plain th{color:var(--ink-3); font-weight:500; font-size:.78rem;}

  ::selection{background:var(--accent); color:#fff;}

  /* ============ SPEC-relatorio-interativo: identidade institucional ============ */
  :root{ --ipp-navy:#004a80; --ipp-cyan:#00aeef; }

  .topbar-accent{
    height:4px; background:var(--ipp-navy);
    margin-left:calc(50% - 50vw); margin-right:calc(50% - 50vw);
  }
  .navbar{
    display:flex; align-items:center; justify-content:space-between; gap:16px;
    height:56px; padding:0 24px; background:var(--page); border-bottom:2px solid var(--ink);
    margin-left:calc(50% - 50vw); margin-right:calc(50% - 50vw);
    position:sticky; top:0; z-index:20;
  }
  .navbar-burger{display:flex; align-items:center; gap:10px; background:none; border:none; cursor:pointer; color:var(--ink); padding:6px 0;}
  .navbar-label{color:var(--ink); font-weight:600;}
  .navbar-logo{background:var(--ipp-navy); padding:6px 12px; display:flex; align-items:center; flex:none;}
  .navbar-logo .ipp-logo{height:20px; width:auto; display:block;}
  .navbar-menu{
    margin-left:calc(50% - 50vw); margin-right:calc(50% - 50vw);
    background:var(--surface); border-bottom:2px solid var(--ink); box-shadow:var(--shadow-hover);
    position:sticky; top:56px; z-index:19; max-height:70vh; overflow-y:auto;
  }
  .navbar-menu[hidden]{display:none;}
  .navbar-link{
    display:block; max-width:880px; margin:0 auto; padding:10px 24px;
    font-family:var(--font-mono); font-size:.85rem; color:var(--ink); text-decoration:none;
    border-bottom:1px solid var(--hairline);
  }
  .navbar-link:hover{color:var(--accent);}

  .doc-head-row{display:flex; justify-content:space-between; align-items:flex-end; gap:40px; flex-wrap:wrap;}
  .doc-eyebrow{color:var(--accent); font-weight:700; margin-bottom:10px;}
  .doc-head-desc{max-width:420px;}
  header.doc-head .doc-head-desc .meta{display:block; font-family:var(--font-mono); font-size:.72rem; color:var(--ink-3); padding-bottom:0; margin:8px 0 0;}
  .spectrum-bar{display:flex; height:6px; margin-top:24px;}
  .spectrum-bar span{flex:1;}

  /* ---- secoes retrateis, cartao brutalista ---- */
  .rsec{border:2px solid var(--ink); border-radius:0; margin:40px 0; background:var(--surface);}
  .rsec-head{display:flex; align-items:center; justify-content:space-between; gap:16px; padding:16px 22px; border-bottom:2px solid var(--ink);}
  .rsec-head-l{display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;}
  .rsec-head-l h2{margin:0; padding:0; border:none;}
  .rsec-eyebrow{color:var(--accent); font-weight:700;}
  .rsec[data-collapsed="true"] .rsec-eyebrow{color:var(--ink-3); font-weight:400;}
  .rsec-toggle{
    display:flex; align-items:center; gap:8px; background:var(--ink); color:var(--page); border:none; border-radius:0;
    font-family:var(--font-mono); font-size:.72rem; font-weight:600; padding:8px 14px; cursor:pointer; flex:none;
  }
  .rsec[data-collapsed="true"] .rsec-toggle{background:var(--page); color:var(--ink); border:2px solid var(--ink); padding:6px 12px;}
  .section-body{padding:24px 22px 30px;}
  .rsec[data-collapsed="true"] .section-body{display:none;}

  /* ---- seletor de opcoes (pills) ---- */
  .option-card{display:flex; gap:16px; align-items:stretch; margin:14px 0 8px;}
  .pill-col{display:flex; flex-direction:column; gap:8px; width:200px; flex:none; max-height:460px; overflow-y:auto; padding-right:2px;}
  .pill{
    text-align:left; padding:9px 12px; border:2px solid var(--ink); background:var(--page); color:var(--ink); border-radius:0;
    font-family:var(--font-mono); font-size:.72rem; font-weight:600; cursor:pointer;
  }
  .pill[data-active="true"]{background:var(--ink); color:var(--page);}
  .opt-panes{flex:1; min-width:0;}
  .opt-panes .out{margin-top:0;}

  /* ---- outliers ---- */
  .outlier-toolbar{display:flex; justify-content:flex-end; margin-bottom:6px;}
  .outlier-btn{
    display:flex; align-items:center; gap:6px; border:1.5px solid var(--ink); background:var(--page); color:var(--ink); border-radius:0;
    font-family:var(--font-mono); font-size:.68rem; font-weight:600; padding:5px 10px; cursor:pointer;
  }
  .outlier-btn[data-active="true"]{background:var(--ink); color:var(--page);}
  .outlier-x{font-weight:700;}

  /* ---- download CSV ---- */
  .out{position:relative;}
  .dl-btn{
    position:absolute; top:14px; right:14px; z-index:2;
    display:flex; align-items:center; gap:5px; border:1.5px solid var(--ink); background:var(--page); color:var(--ink); border-radius:0;
    font-family:var(--font-mono); font-size:.66rem; font-weight:600; padding:5px 9px; cursor:pointer;
  }
  .dl-btn:hover{background:var(--accent-soft);}

  /* ---- mapas SVG interativos ---- */
  .map-svg-row{display:flex; gap:20px; align-items:flex-start; flex-wrap:wrap;}
  .map-svg{flex:1; min-width:260px; max-width:480px; height:auto;}
  .map-region{transition:filter .15s ease; cursor:pointer;}
  .map-region:hover{filter:brightness(1.08); stroke-width:1.6;}
  .map-legend{width:170px; flex:none;}
  .map-legend-row{display:flex; align-items:center; gap:8px; font-family:var(--font-mono); font-size:.7rem; color:var(--ink-2); margin:4px 0;}
  .map-legend-sw{width:14px; height:14px; border:1px solid var(--ink); flex:none; display:inline-block;}

  /* ---- rodape institucional ---- */
  footer.doc-foot{
    margin-left:calc(50% - 50vw); margin-right:calc(50% - 50vw);
    background:var(--ipp-navy); color:#EAF2F8; padding:36px 24px 24px; margin-top:60px;
  }
  .footer-cols{max-width:880px; margin:0 auto; display:flex; gap:40px; flex-wrap:wrap; padding-bottom:20px;}
  .footer-col{min-width:180px; flex:1;}
  .footer-col-logo{min-width:220px; flex:1.4;}
  .footer-col-logo .ipp-logo{height:24px; width:auto; display:block; margin-bottom:12px;}
  .footer-col-logo p{font-size:.76rem; color:#B9D2E4; max-width:260px; line-height:1.6; margin:0;}
  .footer-col .eyebrow{color:#7FA9C6; margin-bottom:8px;}
  .footer-col > div{font-size:.76rem; color:#DCE9F2; line-height:1.9;}
  .footer-col a{color:#DCE9F2;}
  .footer-col a:hover{color:#fff;}
  .footer-rule{max-width:880px; margin:0 auto; height:1px; background:var(--ipp-cyan); opacity:.4;}
  .footer-credit{max-width:880px; margin:0 auto; padding-top:14px; font-family:var(--font-mono); font-size:.66rem; color:#7FA9C6;}

  @media (max-width:720px){
    .option-card{flex-direction:column;}
    .pill-col{flex-direction:row; flex-wrap:wrap; width:auto; max-height:none;}
    .map-svg-row{flex-direction:column;}
    .map-legend{width:auto;}
  }
  @media (max-width:520px){
    .bar-row{grid-template-columns:70px 1fr auto;}
  }
</style>
"""

ENGINE = r"""
<script>
(function(){
  "use strict";
  function fmt(n, d){ d = d||0; return Number(n).toLocaleString('pt-BR', {minimumFractionDigits:d, maximumFractionDigits:d}); }
  function pct(n, d){ return fmt(n, d==null?1:d) + '%'; }
  const CAT = ['var(--c1)','var(--c2)','var(--c3)','var(--c4)','var(--c5)','var(--c6)','var(--c7)','var(--c8)','var(--c9)','var(--c10)','var(--c11)'];
  const NS = 'http://www.w3.org/2000/svg';
  function svgEl(tag, attrs, parent){
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  let uid = 0;
  function byId(id){ return document.getElementById(id); }

  // limiar acima do qual so as series mais relevantes (top N pelo ultimo valor
  // nao-nulo) ficam coloridas/na legenda; o resto vira uma linha cinza fina,
  // agrupada numa unica entrada "Outras (N)" -- mesma regra de
  // serie_temporal_multipla em analise.py (ver SPEC-visual-identity).
  const LIMIAR_DESTAQUE = 6, N_DESTACADAS = 4;

  function prepararSeries(series){
    series.forEach((s,i)=>{ if (!s.color) s.color = series.length===1 ? 'var(--accent)' : CAT[i%CAT.length]; });
    if (series.length <= LIMIAR_DESTAQUE) return { destacadas: series, apagadas: [] };
    const comFinal = series.map(s=>{
      let v = null;
      for (let i=s.values.length-1; i>=0; i--){ if (s.values[i] != null){ v = s.values[i]; break; } }
      return { s, v: v==null ? -Infinity : v };
    });
    comFinal.sort((a,b)=>b.v-a.v);
    return {
      destacadas: comFinal.slice(0, N_DESTACADAS).map(o=>o.s),
      apagadas: comFinal.slice(N_DESTACADAS).map(o=>o.s),
    };
  }

  // ================= line chart =================
  function lineChart(container, cfg){
    const x = cfg.x, series = cfg.series, opts = cfg.opts || {};
    const { destacadas, apagadas } = prepararSeries(series);
    const W = opts.width || 680, H = opts.height || 250;
    const padL = opts.padL != null ? opts.padL : 38;
    const padR = opts.padR != null ? opts.padR : (opts.endLabels === false ? 14 : 66);
    const padT = 16, padB = 28;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const allVals = [];
    series.forEach(s=>s.values.forEach(v=>{ if (v!=null) allVals.push(v); }));
    let vMin = Math.min.apply(null, allVals), vMax = Math.max.apply(null, allVals);
    if (opts.zeroBase !== false) vMin = Math.min(0, vMin);
    const span = (vMax - vMin) || 1;
    vMax += span * 0.14;
    if (opts.zeroBase === false) vMin -= span * 0.14;
    const n = x.length;
    const xAt = i => padL + (n===1 ? plotW/2 : (plotW * i/(n-1)));
    const yAt = v => padT + plotH - ((v - vMin)/((vMax-vMin)||1))*plotH;
    const fmtY = v => cfg.yFormat ? cfg.yFormat(v) : fmt(v, opts.yDecimals||0);

    const wrap = document.createElement('div'); wrap.className = 'chart-wrap';
    if (series.length > 1){
      const legend = document.createElement('div'); legend.className = 'chart-legend';
      destacadas.forEach(s=>{
        const item = document.createElement('span'); item.className = 'legend-item';
        item.innerHTML = '<i style="background:'+s.color+'"></i>' + s.label;
        legend.appendChild(item);
      });
      if (apagadas.length){
        const item = document.createElement('span'); item.className = 'legend-item';
        item.innerHTML = '<i style="background:var(--c-muted)"></i>Outras ('+apagadas.length+')';
        legend.appendChild(item);
      }
      wrap.appendChild(legend);
    }
    const svg = svgEl('svg', {viewBox:'0 0 '+W+' '+H, class:'chart-svg', preserveAspectRatio:'xMidYMid meet'});
    const gridN = 4;
    for (let i=0;i<=gridN;i++){
      const v = vMin + (vMax-vMin)*i/gridN;
      const y = yAt(v);
      svgEl('line', {x1:padL, x2:W-padR, y1:y, y2:y, class:'grid-line'}, svg);
      svgEl('text', {x:padL-7, y:y+3.5, class:'axis-label', 'text-anchor':'end'}, svg).textContent = fmtY(v);
    }
    const maxLabels = opts.maxXLabels || 7;
    const step = Math.max(1, Math.ceil(n/maxLabels));
    x.forEach((lab,i)=>{
      if (i % step !== 0 && i !== n-1) return;
      svgEl('text', {x:xAt(i), y:H-7, class:'axis-label', 'text-anchor': i===0?'start':(i===n-1?'end':'middle')}, svg).textContent = lab;
    });

    function desenhaSerie(s, apagada){
      const pts = s.values.map((v,i)=> v==null ? null : [xAt(i), yAt(v)]);
      let d = '';
      pts.forEach(p=>{ if (p) d += (d===''?'M':'L') + p[0].toFixed(2) + ',' + p[1].toFixed(2) + ' '; });
      const validPts = pts.filter(Boolean);
      const cor = apagada ? 'var(--c-muted)' : s.color;
      if (!apagada && series.length === 1 && opts.area !== false && validPts.length){
        uid++;
        const gid = 'g'+uid;
        const grad = svgEl('linearGradient', {id:gid, x1:0, y1:0, x2:0, y2:1}, svg);
        svgEl('stop', {offset:'0%', 'stop-color':cor, 'stop-opacity':.18}, grad);
        svgEl('stop', {offset:'100%', 'stop-color':cor, 'stop-opacity':0}, grad);
        const base = yAt(vMin);
        const area = d + 'L'+validPts[validPts.length-1][0].toFixed(2)+','+base.toFixed(2)+' L'+validPts[0][0].toFixed(2)+','+base.toFixed(2)+' Z';
        svgEl('path', {d:area, fill:'url(#'+gid+')', stroke:'none'}, svg);
      }
      svgEl('path', {d:d, fill:'none', stroke:cor, 'stroke-width':apagada?1.1:2, 'stroke-opacity':apagada?.55:1, 'stroke-linecap':'round', 'stroke-linejoin':'round'}, svg);
      const last = validPts[validPts.length-1];
      let lastValidIdx = -1;
      for (let i=s.values.length-1;i>=0;i--){ if (s.values[i]!=null){ lastValidIdx=i; break; } }
      if (last && !apagada && opts.endLabels !== false){
        svgEl('circle', {cx:last[0], cy:last[1], r:3.2, fill:cor}, svg);
        if (destacadas.length <= (opts.maxDirectLabels || 8)){
          const t = svgEl('text', {x:last[0]+7, y:last[1], class:'end-label', fill:cor}, svg);
          t.textContent = s.format ? s.format(s.values[s.values.length-1]) : fmtY(s.values[s.values.length-1]);
        }
      }
      // maximo/minimo fixos, sempre visiveis sem hover (specification.md §3.9) --
      // pula o ponto ja coberto pelo end-label "mais recente" (idx===lastValidIdx) e o
      // primeiro ponto (idx===0, ja visivel por ser onde a linha comeca) -- em series
      // com poucos pontos isso evita rotulo redundante colado no eixo Y. Limiar mais
      // baixo que o end-label (maxExtremeSeries, nao maxDirectLabels): com muitas series
      // no mesmo grafico, maximos/minimos caem em posicoes X arbitrarias e colidem com
      // mais facilidade do que o end-label (que fica sempre no mesmo X, a ultima coluna).
      if (!apagada && opts.extremeLabels !== false && destacadas.length <= (opts.maxExtremeSeries || 4)){
        let iMax=-1, iMin=-1, vMax=-Infinity, vMin=Infinity;
        s.values.forEach((v,i)=>{ if (v!=null){ if (v>vMax){vMax=v;iMax=i;} if (v<vMin){vMin=v;iMin=i;} } });
        [[iMax,-8],[iMin,13]].forEach(([idx,dy])=>{
          if (idx<0 || idx===lastValidIdx || idx===0) return;
          const p = pts[idx]; if (!p) return;
          svgEl('circle', {cx:p[0], cy:p[1], r:2.6, fill:cor}, svg);
          const t = svgEl('text', {x:p[0], y:p[1]+dy, class:'extreme-label', fill:cor, 'text-anchor':'middle'}, svg);
          t.textContent = s.format ? s.format(s.values[idx]) : fmtY(s.values[idx]);
        });
      }
    }
    apagadas.forEach(s=>desenhaSerie(s, true));
    destacadas.forEach(s=>desenhaSerie(s, false));

    const hoverG = svgEl('g', {style:'display:none'}, svg);
    const hoverLine = svgEl('line', {y1:padT, y2:H-padB, class:'hover-line'}, hoverG);
    const hoverDots = series.map(s=>svgEl('circle', {r:3.6, fill:s.color, class:'hover-dot'}, hoverG));
    const tooltip = document.createElement('div'); tooltip.className = 'chart-tooltip';
    const capture = svgEl('rect', {x:padL, y:0, width:Math.max(plotW,1), height:H, fill:'transparent'}, svg);
    capture.style.cursor = 'crosshair';

    function onMove(clientX){
      const rect = svg.getBoundingClientRect();
      const mx = (clientX - rect.left) * (W/rect.width);
      let idx = Math.round((mx-padL)/plotW*(n-1));
      idx = Math.max(0, Math.min(n-1, idx));
      hoverG.style.display = 'block';
      const xp = xAt(idx);
      hoverLine.setAttribute('x1', xp); hoverLine.setAttribute('x2', xp);
      let rows = '';
      series.forEach((s,si)=>{
        const v = s.values[idx];
        hoverDots[si].setAttribute('cx', xp);
        hoverDots[si].setAttribute('cy', v==null ? -9999 : yAt(v));
        if (v != null) rows += '<div class="tt-row"><i style="background:'+s.color+'"></i>'+s.label+': <b>'+(s.format?s.format(v):fmtY(v))+'</b></div>';
      });
      tooltip.innerHTML = '<div class="tt-year">'+x[idx]+'</div>' + rows;
      tooltip.style.display = 'block';
      const leftPct = (xp/W)*100;
      tooltip.style.left = leftPct + '%';
      tooltip.style.transform = leftPct > 60 ? 'translate(-104%,-4%)' : 'translate(6%,-4%)';
    }
    capture.addEventListener('mousemove', e=>onMove(e.clientX));
    capture.addEventListener('touchmove', e=>{ if (e.touches[0]) onMove(e.touches[0].clientX); }, {passive:true});
    capture.addEventListener('mouseleave', ()=>{ hoverG.style.display='none'; tooltip.style.display='none'; });

    wrap.appendChild(svg);
    wrap.appendChild(tooltip);
    container.appendChild(wrap);

    if (opts.table){
      const det = document.createElement('details'); det.className = 'data-table';
      det.innerHTML = '<summary>Ver dados em tabela</summary>';
      const scroll = document.createElement('div'); scroll.className = 'table-scroll';
      const tbl = document.createElement('table');
      let thead = '<tr><th>Ano</th>' + series.map(s=>'<th>'+s.label+'</th>').join('') + '</tr>';
      let rowsHtml = '';
      x.forEach((lab,i)=>{
        rowsHtml += '<tr><td>'+lab+'</td>' + series.map(s=>'<td>'+(s.values[i]==null?'—':(s.format?s.format(s.values[i]):fmtY(s.values[i])))+'</td>').join('') + '</tr>';
      });
      tbl.innerHTML = thead + rowsHtml;
      scroll.appendChild(tbl); det.appendChild(scroll);
      container.appendChild(det);
    }
  }

  // ================= horizontal bar chart =================
  function barChart(container, cfg){
    const items = cfg.items;
    const wrap = document.createElement('div'); wrap.className = 'bar-chart';
    const max = Math.max.apply(null, items.map(it=>it.value)) * 1.06 || 1;
    items.forEach((it,i)=>{
      const row = document.createElement('div'); row.className = 'bar-row';
      const label = document.createElement('div'); label.className = 'bar-label'; label.textContent = it.label; label.title = it.label;
      const track = document.createElement('div'); track.className = 'bar-track';
      const fillWrap = document.createElement('div');
      fillWrap.className = 'bar-fill';
      fillWrap.style.background = it.color || CAT[i%CAT.length];
      track.appendChild(fillWrap);
      const val = document.createElement('span'); val.className = 'bar-value';
      val.textContent = it.format ? it.format(it.value) : fmt(it.value);
      row.appendChild(label); row.appendChild(track); row.appendChild(val);
      wrap.appendChild(row);
      requestAnimationFrame(()=>{ fillWrap.style.width = (it.value/max*100) + '%'; });
    });
    container.appendChild(wrap);
  }

  // ================= grouped vertical bar chart =================
  function groupedBarChart(container, cfg){
    const groups = cfg.groups, series = cfg.series, opts = cfg.opts || {};
    series.forEach((s,i)=>{ if (!s.color) s.color = CAT[i%CAT.length]; });
    const W = opts.width || 760, H = opts.height || 320;
    const padL = 40, padR = 12, padT = 14, padB = 56;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const allVals = [];
    series.forEach(s=>s.values.forEach(v=>{ if (v!=null) allVals.push(v); }));
    const maxV = Math.max.apply(null, allVals) * 1.12;
    const yAt = v => padT + plotH - (v/maxV)*plotH;
    const fmtY = v => cfg.yFormat ? cfg.yFormat(v) : fmt(v, opts.yDecimals||0);

    const wrap = document.createElement('div'); wrap.className = 'chart-wrap';
    const legend = document.createElement('div'); legend.className = 'chart-legend';
    series.forEach(s=>{
      const item = document.createElement('span'); item.className = 'legend-item';
      item.innerHTML = '<i style="background:'+s.color+'"></i>' + s.label;
      legend.appendChild(item);
    });
    wrap.appendChild(legend);

    const svg = svgEl('svg', {viewBox:'0 0 '+W+' '+H, class:'chart-svg'});
    const gridN = 4;
    for (let i=0;i<=gridN;i++){
      const v = maxV*i/gridN;
      const y = yAt(v);
      svgEl('line', {x1:padL, x2:W-padR, y1:y, y2:y, class:'grid-line'}, svg);
      svgEl('text', {x:padL-7, y:y+3.5, class:'axis-label', 'text-anchor':'end'}, svg).textContent = fmtY(v);
    }
    const groupW = plotW / groups.length;
    const barPad = 0.16;
    const innerW = groupW * (1 - 2*barPad);
    const barW = innerW / series.length;
    const tooltip = document.createElement('div'); tooltip.className = 'chart-tooltip';

    groups.forEach((g,gi)=>{
      const gx0 = padL + gi*groupW + groupW*barPad;
      svgEl('text', {x: gx0 + innerW/2, y: H-38, class:'axis-label', 'text-anchor':'middle', 'font-size':10.5}, svg).textContent = g;
      series.forEach((s,si)=>{
        const v = s.values[gi];
        if (v == null) return;
        const bx = gx0 + si*barW;
        const by = yAt(v);
        const bh = Math.max(1, padT+plotH - by);
        const rect = svgEl('rect', {x:bx+0.6, y:by, width:Math.max(1,barW-1.2), height:bh, fill:s.color, rx:1.5}, svg);
        rect.style.cursor = 'pointer';
        rect.addEventListener('mousemove', e=>{
          const r = wrap.getBoundingClientRect();
          tooltip.innerHTML = '<div class="tt-year">'+g+'</div><div class="tt-row"><i style="background:'+s.color+'"></i>'+s.label+': <b>'+(s.format?s.format(v):fmtY(v))+'</b></div>';
          tooltip.style.display = 'block';
          tooltip.style.left = (e.clientX - r.left + 10) + 'px';
          tooltip.style.top = (e.clientY - r.top - 30) + 'px';
          tooltip.style.transform = 'none';
        });
        rect.addEventListener('mouseleave', ()=>{ tooltip.style.display='none'; });
      });
    });

    wrap.appendChild(svg);
    wrap.appendChild(tooltip);
    container.appendChild(wrap);

    if (opts.table){
      const det = document.createElement('details'); det.className = 'data-table';
      det.innerHTML = '<summary>Ver dados em tabela</summary>';
      const scroll = document.createElement('div'); scroll.className = 'table-scroll';
      const tbl = document.createElement('table');
      let thead = '<tr><th></th>' + groups.map(g=>'<th>'+g+'</th>').join('') + '</tr>';
      let rowsHtml = '';
      series.forEach(s=>{
        rowsHtml += '<tr><td>'+s.label+'</td>' + s.values.map(v=>'<td>'+(v==null?'—':(s.format?s.format(v):fmtY(v)))+'</td>').join('') + '</tr>';
      });
      tbl.innerHTML = thead + rowsHtml;
      scroll.appendChild(tbl); det.appendChild(scroll);
      container.appendChild(det);
    }
  }

  // ================= SPEC-relatorio-interativo: controladores estaticos =================
  // (navbar, secoes retrateis, seletor de opcoes, toggle de outliers, download CSV,
  // tooltip de mapa -- tudo delegado/inicializado uma vez no DOMContentLoaded, ja que
  // esses elementos sao HTML estatico gerado em Python, nao criados por lineChart/etc.)

  function initNavbar(){
    const burger = document.getElementById('navbar-burger');
    const menu = document.getElementById('navbar-menu');
    if (!burger || !menu) return;
    burger.addEventListener('click', ()=>{
      const abrindo = menu.hasAttribute('hidden');
      if (abrindo) menu.removeAttribute('hidden'); else menu.setAttribute('hidden','');
      burger.setAttribute('aria-expanded', abrindo ? 'true' : 'false');
    });
    menu.querySelectorAll('a.navbar-link').forEach(a=>{
      a.addEventListener('click', ()=>{ menu.setAttribute('hidden',''); burger.setAttribute('aria-expanded','false'); });
    });
  }

  function initSections(){
    document.querySelectorAll('.rsec').forEach(sec=>{
      const btn = sec.querySelector(':scope > .rsec-head > .rsec-toggle');
      const label = btn && btn.querySelector('.rsec-toggle-label');
      if (!btn) return;
      btn.addEventListener('click', ()=>{
        const colapsando = sec.getAttribute('data-collapsed') !== 'true';
        sec.setAttribute('data-collapsed', colapsando ? 'true' : 'false');
        btn.setAttribute('aria-expanded', colapsando ? 'false' : 'true');
        if (label) label.textContent = colapsando ? 'EXPANDIR' : 'RECOLHER';
      });
    });
  }

  function initPills(){
    document.querySelectorAll('.option-card').forEach(card=>{
      const pills = Array.from(card.querySelectorAll(':scope > .pill-col > .pill'));
      const panes = Array.from(card.querySelectorAll(':scope > .opt-panes > .opt-pane'));
      pills.forEach((pill,i)=>{
        pill.addEventListener('click', ()=>{
          pills.forEach((p,j)=>{ if (j!==i) p.removeAttribute('data-active'); });
          pill.setAttribute('data-active','true');
          panes.forEach((pane,j)=>{ pane.hidden = (j!==i); });
        });
      });
    });
  }

  function initOutliers(){
    document.querySelectorAll('.outlier-card').forEach(card=>{
      const btn = card.querySelector('.outlier-btn');
      const full = card.querySelector(':scope > .outlier-pane[data-variant="full"]');
      const clean = card.querySelector(':scope > .outlier-pane[data-variant="clean"]');
      if (!btn || !full || !clean) return;
      btn.addEventListener('click', ()=>{
        const semOutliers = btn.getAttribute('data-active') !== 'true';
        btn.setAttribute('data-active', semOutliers ? 'true' : 'false');
        full.hidden = semOutliers;
        clean.hidden = !semOutliers;
      });
    });
  }

  function initDownloads(){
    document.addEventListener('click', e=>{
      const btn = e.target.closest('.dl-btn');
      if (!btn) return;
      const card = btn.closest('.out');
      if (!card || !card.dataset.csv) return;
      const blob = new Blob(['﻿' + card.dataset.csv], {type:'text/csv;charset=utf-8;'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = card.dataset.filename || 'dados.csv';
      document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(a.href);
    });
  }

  function initMapTooltips(){
    document.querySelectorAll('.map-svg-card').forEach(card=>{
      const svg = card.querySelector('.map-svg');
      if (!svg) return;
      const tooltip = document.createElement('div'); tooltip.className = 'chart-tooltip';
      tooltip.style.position = 'absolute';
      card.appendChild(tooltip);
      svg.querySelectorAll('.map-region').forEach(path=>{
        path.addEventListener('mousemove', e=>{
          const r = card.getBoundingClientRect();
          tooltip.innerHTML = '<div class="tt-row"><b>'+path.dataset.label+'</b></div><div class="tt-row">'+path.dataset.valor+'</div>';
          tooltip.style.display = 'block';
          tooltip.style.left = (e.clientX - r.left + 12) + 'px';
          tooltip.style.top = (e.clientY - r.top - 34) + 'px';
          tooltip.style.transform = 'none';
        });
        path.addEventListener('mouseleave', ()=>{ tooltip.style.display = 'none'; });
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    initNavbar(); initSections(); initPills(); initOutliers(); initDownloads(); initMapTooltips();
  });

  window.byId = byId; window.lineChart = lineChart; window.barChart = barChart; window.groupedBarChart = groupedBarChart;
  window.fmt = fmt; window.pct = pct;
})();
</script>
"""

RENDER_CALLS = "<script>\n(function(){\n\"use strict\";\n" + "\n".join(scripts) + "\n})();\n</script>"

doc = f"""<title>Primeira Infância Carioca</title>
{CSS}
<div class="doc">
{body}
</div>
{ENGINE}
{RENDER_CALLS}
"""

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(doc)
print(f"wrote {OUT_PATH}: {len(doc)} chars, {len(scripts)} charts, {sum(1 for l,t,s in toc if l==2)} h2 / {sum(1 for l,t,s in toc if l==3)} h3 sections")
