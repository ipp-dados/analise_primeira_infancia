# -*- coding: utf-8 -*-
"""Build the single consolidated interactive HTML report (relatorio/index.html).

Replaces the old 3-file setup (index.html / lighter_index.html / white_index.html),
which was hand-built by unsaved ad-hoc scripts (see relatorio/specs.md). This script
is the first *persisted* generator: it reads tabelas_finais/*.csv (same source the
PDF pipeline uses) and mapas/*.png, and renders interactive SVG charts via a small
JS engine (lineChart/barChart/groupedBarChart, lifted from the old lighter_index.html
and extended with the "many-series" highlight logic used in analise.py's
serie_temporal_multipla). Per SPEC-visual-identity decision B, this report is
visualization-only: title + source + chart/map + optional data table, no prose/notes
(those stay in the notebook and the PDF).

This is a direct transcription of analise.py's chart call sites as of this branch --
if analise.py's sections, column names, or exported filenames change, this needs
matching edits, same caveat as build_notebook_report.py.

Usage (from project root):
    python .claude/skills/export_pdf_report/scripts/build_html_report.py [out_path]
"""
import base64
import io
import json
import math
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
_counter = [0]

def new_id(prefix):
    _counter[0] += 1
    return f"{prefix}-{_counter[0]}"

def h2(t): parts.append(f"<h2>{t}</h2>")
def h3(t): parts.append(f"<h3>{t}</h3>")
def h4(t): parts.append(f"<h4>{t}</h4>")
def h5(t): parts.append(f"<h5>{t}</h5>")
def h6(t): parts.append(f"<h6>{t}</h6>")

def _out_div(elem_id, fonte):
    src = f'<div class="out-src">{fonte}</div>' if fonte else ""
    return f'<div class="out"><div id="{elem_id}"></div>{src}</div>'

FMT_MAP = {'int': 'v=>fmt(v)', 'pct': 'v=>pct(v)', 'pct1': 'v=>pct(v,1)'}

def line_chart(x, series, opts=None, fonte=None, pair=False):
    """series: list of {label, values, format in FMT_MAP}. Returns the elem id
    (caller wraps in .out / .out-pair). Color/legend/highlight all handled by
    the JS engine itself."""
    elem_id = new_id('c')
    opts = dict(opts or {})
    js_series = []
    for s in series:
        fmt_fn = FMT_MAP.get(s.get('format', 'int'), FMT_MAP['int'])
        js_series.append(
            "{label:%s, values:%s, format:%s}" % (json.dumps(s['label'], ensure_ascii=False), json.dumps(jsvals(s['values'])), fmt_fn)
        )
    scripts.append(
        "lineChart(byId(%s), {x:%s, series:[%s], opts:%s});" % (
            json.dumps(elem_id), json.dumps(jsvals(list(x))), ",".join(js_series), json.dumps(opts)
        )
    )
    parts.append(_out_div(elem_id, fonte))
    return elem_id

def bar_chart(items, fonte=None):
    """items: list of {label, value}."""
    elem_id = new_id('c')
    js_items = [
        "{label:%s, value:%s}" % (json.dumps(str(it['label']), ensure_ascii=False), json.dumps(round(float(it['value']), 4)))
        for it in items
    ]
    scripts.append("barChart(byId(%s), {items:[%s]});" % (json.dumps(elem_id), ",".join(js_items)))
    parts.append(_out_div(elem_id, fonte))
    return elem_id

def grouped_bar_chart(groups, series, opts=None, fonte=None):
    """series: list of {label, values, format}."""
    elem_id = new_id('c')
    opts = dict(opts or {})
    opts.setdefault('table', True)
    js_series = []
    for s in series:
        fmt_fn = FMT_MAP.get(s.get('format', 'int'), FMT_MAP['int'])
        js_series.append(
            "{label:%s, values:%s, format:%s}" % (json.dumps(s['label'], ensure_ascii=False), json.dumps(jsvals(s['values'])), fmt_fn)
        )
    scripts.append(
        "groupedBarChart(byId(%s), {groups:%s, series:[%s], opts:%s});" % (
            json.dumps(elem_id), json.dumps([str(g) for g in groups], ensure_ascii=False), ",".join(js_series), json.dumps(opts)
        )
    )
    parts.append(_out_div(elem_id, fonte))
    return elem_id

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

# ================================================================= HEADER ==

parts.append('<header class="doc-head">')
parts.append('<h1><span class="glyph">\U0001F3DB️</span>Análise Primeira Infância Carioca</h1>')
parts.append('<p class="sub">Visualizações dos indicadores de primeira infância (0 a 6 anos) do município do Rio de Janeiro. Cada gráfico tem a fonte no rodapé e uma opção de ver os dados em tabela; a descrição metodológica completa fica no notebook (<code>analise.py</code>) e no relatório em PDF.</p>')
parts.append('<div class="meta"><span>Instituto Pereira Passos</span><span id="gen-date">—</span></div>')
parts.append('</header>')

# ================================================================== CENSO ==

h2('\U0001F3D8️ Censo 2022')

h3('Por bairro')
df_censo_bairro = read("censo_por_bairro.csv")
top10 = df_censo_bairro.sort_values("0 a 4 anos", ascending=False).head(10)[["bairro", "0 a 4 anos", "Percentual 0 a 4"]]
top10 = top10.rename(columns={"bairro": "Bairro", "0 a 4 anos": "Crianças 0-4", "Percentual 0 a 4": "% do bairro"})
top10["% do bairro"] = top10["% do bairro"].map(lambda v: f"{v:.1f}%".replace(".", ","))
plain_table(top10, fonte="Censo Demográfico 2022 (IBGE/Data.Rio)")

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

h3('População 0-6 por idade/raça/sexo (IBGE SIDRA, 2022)')
FONTE_SIDRA_CENSO = "Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606)"
_ORDEM_IDADE_SIDRA_0_6 = ['Menos de 1 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos', '6 anos']
df_censo_raca = read("censo_sidra_populacao_0_6_raca_2022.csv")
df_censo_raca = df_censo_raca[df_censo_raca["idade"].isin(_ORDEM_IDADE_SIDRA_0_6)].set_index("idade").reindex(_ORDEM_IDADE_SIDRA_0_6).reset_index()
raca_cols = [c for c in df_censo_raca.columns if c not in ("idade", "Total")]
grouped_bar_chart(df_censo_raca["idade"], series_from_cols(df_censo_raca, raca_cols), fonte=FONTE_SIDRA_CENSO)
df_censo_sexo = read("censo_sidra_populacao_0_6_sexo_2022.csv")
df_censo_sexo = df_censo_sexo[df_censo_sexo["idade"].isin(_ORDEM_IDADE_SIDRA_0_6)].set_index("idade").reindex(_ORDEM_IDADE_SIDRA_0_6).reset_index()
sexo_cols = [c for c in df_censo_sexo.columns if c not in ("idade", "Total")]
grouped_bar_chart(df_censo_sexo["idade"], series_from_cols(df_censo_sexo, sexo_cols), fonte=FONTE_SIDRA_CENSO)

# ================================================================ CADUNICO ==

h2('\U0001F5C2️ CadÚnico')
FONTE_CADUNICO = "CadÚnico (extração CTPE)"

h3('Por faixa de renda')
df_renda = read("cadunico_por_faixa_etaria_2026.csv")
df_renda_sem_total = df_renda[df_renda["faixa de renda"] != "Total"]
out_pair(
    lambda: bar_chart([{'label': r["faixa de renda"], 'value': r["Famílias"]} for _, r in df_renda_sem_total.iterrows()], fonte=FONTE_CADUNICO),
    lambda: bar_chart([{'label': r["faixa de renda"], 'value': r["Crianças"]} for _, r in df_renda_sem_total.iterrows()], fonte=FONTE_CADUNICO),
)

h3('Por idade')
df_idade = read("cadunico_por_idade_2026.csv")
df_idade["idade_lbl"] = df_idade["idade"].astype(int).map(lambda i: f"{i} ano" if i == 1 else f"{i} anos")
out_pair(
    lambda: bar_chart([{'label': r["idade_lbl"], 'value': r["Famílias"]} for _, r in df_idade.iterrows()], fonte=FONTE_CADUNICO),
    lambda: bar_chart([{'label': r["idade_lbl"], 'value': r["Crianças"]} for _, r in df_idade.iterrows()], fonte=FONTE_CADUNICO),
)

# ============================================================== DATASUS ===

h2('\U0001F3E5 DataSUS/Tabnet')
FONTE_DATASUS = "DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro"

h3('Nascidos vivos')
df_nv = read("nascidos_vivos_por_ano.csv")
line_chart(df_nv["ano"], [{'label': 'Nascidos vivos', 'values': df_nv['nascidos vivos']}], opts={'height': 220, 'table': True}, fonte=FONTE_DATASUS)

h3('Nascidos abaixo do peso')
df_bp = read("nascidos_abaixo_peso_por_ano.csv")
line_chart(df_bp["ano"], [{'label': '% abaixo do peso', 'values': df_bp['percentual abaixo do peso'], 'format': 'pct1'}], opts={'height': 220, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)

h3('\U0001F4C9 Mortalidade por raça/cor (0-364 dias)')
RACA_LABEL = {"amarela": "Amarela", "branca": "Branca", "indigena": "Indígena", "parda": "Parda", "preta": "Preta", "nao_informado": "Não informado"}
RACAS = list(RACA_LABEL)
df_raca = read("mortalidade_raca_municipio_ano.csv")
line_chart(df_raca["ano"], series_from_cols(df_raca, [f"obitos_{r}" for r in RACAS], {f"obitos_{r}": RACA_LABEL[r] for r in RACAS}), opts={'height': 260, 'table': True}, fonte=FONTE_DATASUS)
line_chart(df_raca["ano"], series_from_cols(df_raca, [f"percentual_{r}" for r in RACAS], {f"percentual_{r}": RACA_LABEL[r] for r in RACAS}, fmt='pct1'), opts={'height': 260, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)

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
_SLUG_SUBGRUPO = {
    '1.1. Reduzível pelas ações de imunização': 'Imunização',
    '1.2.1. Red por at à mulher na gestação': 'Gestação',
    '1.2.2. Red por at à mulher no parto': 'Parto',
    '1.2.3. Red por at ao recém-nascido': 'Recém-nascido',
    '1.3. Red por ações de diag e trat adequado': 'Diagnóstico/tratamento',
    '1.4. Red por ações promoção vinc a atenção': 'Promoção/vinculação',
}
for faixa, faixa_lbl in [('menores de 1 ano', 'Menores de 1 ano'), ('de 1 a 4 anos', 'De 1 a 4 anos'), ('menores de 5 anos', 'Menores de 5 anos')]:
    h5(faixa_lbl)
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
        h6(subgrupo_lbl)
        line_chart(anos, series, opts={'height': 240, 'maxXLabels': 6, 'legendTitle': 'CAP', 'table': True}, fonte=FONTE_EVITAVEIS)

h4('Grupo evitável, por CAP')
GRUPO1_COL = "1. Causas evitáveis"
for faixa, faixa_lbl in [('menores de 1 ano', 'Menores de 1 ano'), ('de 1 a 4 anos', 'De 1 a 4 anos'), ('menores de 5 anos', 'Menores de 5 anos')]:
    h5(faixa_lbl)
    sub = df_grupo_cap_faixa[df_grupo_cap_faixa["faixa_etaria"] == faixa]
    anos = sorted(sub["ano"].unique().tolist())
    caps = sorted(sub["cod_ap_sms"].unique().tolist())
    series_abs, series_pct = [], []
    for cap in caps:
        d = sub[sub["cod_ap_sms"] == cap].set_index("ano")
        series_abs.append({'label': f"CAP {cap}", 'values': [d[GRUPO1_COL].get(a) for a in anos]})
        series_pct.append({'label': f"CAP {cap}", 'values': [d['percentual_evitaveis'].get(a) for a in anos], 'format': 'pct1'})
    line_chart(anos, series_abs, opts={'height': 240, 'maxXLabels': 6, 'table': True}, fonte=FONTE_EVITAVEIS)
    line_chart(anos, series_pct, opts={'height': 240, 'maxXLabels': 6, 'zeroBase': False, 'table': True}, fonte=FONTE_EVITAVEIS)

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

# ==================================================== GRAVIDEZ/PUERPERIO ==

h2('\U0001F930 Gravidez e puerpério')
df_grav = read("obitos_gravidez_por_ano.csv")
line_chart(df_grav["ano"], [{'label': 'Óbitos', 'values': df_grav['óbitos-gravidez']}], opts={'height': 200, 'table': True}, fonte=FONTE_DATASUS)
df_puerp = read("obitos_puerperio_por_ano.csv")
line_chart(df_puerp["ano"], [{'label': 'Óbitos', 'values': df_puerp['óbitos-puerpério']}], opts={'height': 200, 'table': True}, fonte=FONTE_DATASUS)

# ======================================================== NEONATAL ========

h2('\U0001FA7A Mortalidade neonatal')
df_prec = read("mortalidade_neonatal_precoce_por_ano.csv")
line_chart(df_prec["ano"], [{'label': 'Taxa (‰)', 'values': df_prec['taxa_mortalidade_precoce'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)
df_tard = read("mortalidade_neonatal_tardia_por_ano.csv")
line_chart(df_tard["ano"], [{'label': 'Taxa (‰)', 'values': df_tard['taxa_obitos_tardios'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)
df_inf = read("mortalidade_infantil_pos_neonatal_total_por_ano.csv")
line_chart(df_inf["ano"], [{'label': 'Taxa pós-neonatal (‰)', 'values': df_inf['taxa_mortalidade_pos_neonatal'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)
line_chart(df_inf["ano"], [{'label': 'Taxa infantil total (‰)', 'values': df_inf['taxa_mortalidade_infantil'], 'format': 'pct1'}], opts={'height': 200, 'zeroBase': False, 'table': True}, fonte=FONTE_DATASUS)

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

_ORDEM_IDADE_SIDRA_0_5 = ['0 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos']
_ORDEM_IDADE_SIDRA_0_6_EDU = ['0 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos', '6 anos']

def _ordenar_idade(df, ordem):
    return df[df["idade"].isin(ordem)].set_index("idade").reindex(ordem).reset_index()

h3('Frequência escolar 0-5 anos (IBGE SIDRA)')
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

# =================================================================== MAPS ==

h2('\U0001F5FA️ Mapas')

MAP_GROUPS = [
    ("Censo/população", [
        ("mapa_censo_0_4_absoluto.png", "Crianças de 0 a 4 anos, por bairro (Censo 2022)"),
        ("mapa_censo_0_4_percentual.png", "% de crianças de 0 a 4 anos, por bairro (Censo 2022)"),
        ("mapa_censo_0_4_absoluto_ap.png", "Crianças de 0 a 4 anos, por Área de Planejamento"),
        ("mapa_censo_0_4_percentual_ap.png", "% de crianças de 0 a 4 anos, por Área de Planejamento"),
        ("mapa_censo_0_4_absoluto_rp.png", "Crianças de 0 a 4 anos, por Região de Planejamento"),
        ("mapa_censo_0_4_percentual_rp.png", "% de crianças de 0 a 4 anos, por Região de Planejamento"),
    ]),
    ("CadÚnico", [
        ("mapa_cadunico_criancas_bairro_2026.png", "Crianças (0-6 anos) no CadÚnico, por bairro"),
        ("mapa_cadunico_primeira_infancia_bairro_2026.png", "Crianças (0-4 anos) no CadÚnico, por bairro"),
        ("mapa_percentual_cadunico_primeira_infancia_bairro_2026.png", "% de crianças 0-4 anos no CadÚnico sobre o Censo, por bairro"),
    ]),
    ("Natalidade", [
        ("mapa_nascidos_vivos_bairro_2025.png", "Nascidos vivos por bairro (2025)"),
        ("mapa_nascidos_baixo_peso_bairro_2025.png", "Nascidos com baixo peso por bairro (2025)"),
        ("mapa_percentual_baixo_peso_bairro_2025.png", "% de nascidos com baixo peso por bairro (2025)"),
    ]),
    ("Mortalidade por raça/cor", [
        ("mapa_obitos_raca_total_bairro_2025.png", "Óbitos de 0 a 364 dias por bairro (2025)"),
        ("mapa_taxa_obitos_raca_total_bairro_2025.png", "Taxa de mortalidade infantil (0-364 dias) por bairro (2025)"),
    ]),
    ("Gravidez e puerpério", [
        ("mapa_obitos_gravidez_bairro_2025.png", "Óbitos durante a gravidez por bairro (2025)"),
        ("mapa_obitos_puerperio_bairro_2025.png", "Óbitos durante o puerpério por bairro (2025)"),
    ]),
    ("Mortalidade neonatal", [
        ("mapa_obitos_neonatal_precoce_bairro_2025.png", "Óbitos precoces (0-6 dias) por bairro (2025)"),
        ("mapa_taxa_mortalidade_precoce_bairro_2025.png", "Taxa de óbitos precoces por bairro (2025)"),
        ("mapa_obitos_neonatal_tardia_bairro_2025.png", "Óbitos tardios (7-27 dias) por bairro (2025)"),
        ("mapa_taxa_obitos_tardios_bairro_2025.png", "Taxa de óbitos tardios por bairro (2025)"),
        ("mapa_obitos_pos_neonatal_bairro_2025.png", "Óbitos pós-neonatais (28-364 dias) por bairro (2025)"),
        ("mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png", "Taxa de mortalidade pós-neonatal por bairro (2025)"),
        ("mapa_mortalidade_infantil_bairro_2025.png", "Óbitos infantis (0-364 dias) por bairro (2025)"),
        ("mapa_taxa_mortalidade_infantil_bairro_2025.png", "Taxa de mortalidade infantil por bairro (2025)"),
    ]),
    ("Causas evitáveis, por CAP (2025)", [
        ("mapa_obitos_evitaveis_menores_1_ano_cap_2025.png", "Óbitos evitáveis, menores de 1 ano, por CAP"),
        ("mapa_percentual_evitaveis_menores_1_ano_cap_2025.png", "% de óbitos evitáveis, menores de 1 ano, por CAP"),
        ("mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png", "Óbitos evitáveis, de 1 a 4 anos, por CAP"),
        ("mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png", "% de óbitos evitáveis, de 1 a 4 anos, por CAP"),
        ("mapa_obitos_evitaveis_menores_5_anos_cap_2025.png", "Óbitos evitáveis, menores de 5 anos, por CAP"),
        ("mapa_percentual_evitaveis_menores_5_anos_cap_2025.png", "% de óbitos evitáveis, menores de 5 anos, por CAP"),
        ("mapa_obitos_evitaveis_gestacao_menores_1_ano_cap_2025.png", "Óbitos evitáveis - Gestação, menores de 1 ano, por CAP"),
        ("mapa_obitos_evitaveis_parto_menores_1_ano_cap_2025.png", "Óbitos evitáveis - Parto, menores de 1 ano, por CAP"),
    ]),
]

total_expected = sum(len(v) for _, v in MAP_GROUPS)
import os
available = set(os.listdir(MAPAS))
missing = [fn for _, group in MAP_GROUPS for fn, _ in group if fn not in available]
if missing:
    raise SystemExit(f"missing map PNGs: {missing}")

for tema, imgs in MAP_GROUPS:
    h3(tema)
    parts.append('<div class="map-gallery">')
    for fn, caption in imgs:
        parts.append(map_card(fn, caption))
    parts.append('</div>')

footer = '<footer class="doc-foot"><p>Fontes: IBGE (Censo, SIDRA), CTPE/CadÚnico, DATASUS/Tabnet (SINASC, SIM), SISVAN, EPI/SVS-Rio, PNAD Contínua e Censo Escolar/INEP. Elaborado a partir do pipeline documentado em <code>analise.py</code> — Instituto Pereira Passos, Prefeitura da Cidade do Rio de Janeiro.</p></footer>'
parts.append(footer)

# ============================================================== ASSEMBLE ==

gen_date = datetime.date.today().strftime("%d de %B de %Y")
MESES = {"January": "janeiro", "February": "fevereiro", "March": "março", "April": "abril", "May": "maio", "June": "junho",
         "July": "julho", "August": "agosto", "September": "setembro", "October": "outubro", "November": "novembro", "December": "dezembro"}
for en, pt in MESES.items():
    gen_date = gen_date.replace(en, pt)

body = "\n".join(parts).replace('<span id="gen-date">—</span>', f'<span id="gen-date">Atualizado {gen_date}</span>')

CSS = r"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,440;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

  :root{
    --page:        #FDFCFA;
    --surface:     #FFFFFF;
    --surface-2:   #FFFFFF;
    --ink:         #283532;
    --ink-2:       #5E6D68;
    --ink-3:       #98A6A1;
    --hairline:    rgba(20,30,27,0.10);
    --hairline-2:  rgba(20,30,27,0.05);
    --accent:      #58b19c;
    --accent-ink:  #1c2b27;
    --accent-soft: #EAF6F2;
    --shadow:      0 1px 2px rgba(20,30,27,.03), 0 6px 16px -10px rgba(20,30,27,.08);

    --c1: #6a95c8; --c1d:#87aad4;
    --c2: #d28060; --c2d:#d19e8a;
    --c3: #66cca7; --c3d:#89d2b9;
    --c4: #deb254; --c4d:#e0be7b;
    --c5: #ca688d; --c5d:#cc8ea5;
    --c6: #54de54; --c6d:#7be07b;
    --c7: #8177bb; --c7d:#928ad1;
    --c8: #cc6766; --c8d:#d28989;
    --c9: #bc9776; --c9d:#bfad9c;
    --c10:#b67c99; --c10d:#c398b3;
    --c11:#8e9ea4; --c11d:#a5b2b6;
    --c-muted: #c9c9c9; --c-muted-d:#5a6663;

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

  .doc{max-width:860px; margin:0 auto; padding:56px 24px 100px;}

  header.doc-head{margin-bottom:8px;}
  header.doc-head h1{
    font-family:var(--font-display); font-weight:600; font-size:clamp(1.9rem,4.4vw,2.7rem);
    margin:0 0 6px; line-height:1.12; text-wrap:balance; letter-spacing:-.01em;
    display:flex; align-items:center; gap:14px;
  }
  header.doc-head h1 .glyph{font-size:.82em; flex:none;}
  header.doc-head .sub{color:var(--ink-2); font-size:1.02rem; max-width:68ch; margin:0 0 18px;}
  header.doc-head .meta{
    display:flex; flex-wrap:wrap; gap:6px 16px; font-family:var(--font-mono); font-size:.76rem;
    color:var(--ink-3); padding-bottom:28px; border-bottom:1px solid var(--hairline);
  }

  h2{
    font-family:var(--font-display); font-weight:600; font-size:clamp(1.5rem,3vw,1.85rem);
    margin:64px 0 4px; padding-top:28px; border-top:1px solid var(--hairline); line-height:1.2; text-wrap:balance;
  }
  h2:first-of-type{margin-top:40px;}
  h3{
    font-family:var(--font-display); font-weight:600; font-size:1.42rem;
    margin:46px 0 12px; line-height:1.2;
  }
  h4{
    font-family:var(--font-display); font-weight:600; font-size:1.18rem;
    margin:34px 0 10px;
  }
  h5{
    font-family:var(--font-body); font-weight:600; font-size:1.02rem;
    margin:28px 0 8px; color:var(--ink);
  }
  h6{
    font-family:var(--font-body); font-weight:600; font-size:.92rem;
    margin:22px 0 6px; color:var(--ink-2); text-transform:uppercase; letter-spacing:.03em;
  }

  .out{
    margin:12px 0 6px; background:var(--surface); border:1px solid var(--hairline); border-radius:4px;
    box-shadow:var(--shadow); padding:20px 22px 14px;
  }
  .out-pair{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin:12px 0 6px;}

  .map-gallery{display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:18px; margin:12px 0 32px;}
  .map-card{margin:0; background:var(--surface); border:1px solid var(--hairline); border-radius:4px; box-shadow:var(--shadow); overflow:hidden;}
  .map-card img{display:block; width:100%; height:auto;}
  .map-cap{padding:10px 14px; font-size:.82rem; color:var(--ink-2); border-top:1px solid var(--hairline-2);}
  .out-pair > .out{margin:0;}
  .out-src{font-family:var(--font-mono); font-size:.7rem; color:var(--ink-3); margin-top:10px; padding-top:8px; border-top:1px solid var(--hairline-2);}

  .chart-wrap{position:relative;}
  .chart-legend{display:flex; flex-wrap:wrap; gap:5px 14px; margin-bottom:10px;}
  .legend-item{display:flex; align-items:center; gap:6px; font-size:.79rem; color:var(--ink-2); white-space:nowrap;}
  .legend-item i{width:9px; height:9px; border-radius:50%; display:inline-block; flex:none;}
  .chart-svg{width:100%; height:auto; display:block; overflow:visible;}
  .grid-line{stroke:var(--hairline); stroke-width:1;}
  .axis-label{font-family:var(--font-mono); font-size:9px; fill:var(--ink-3);}
  .end-label{font-family:var(--font-mono); font-size:10.5px; font-weight:600; dominant-baseline:middle;}
  .hover-line{stroke:var(--ink-3); stroke-width:1; stroke-dasharray:2 3;}
  .hover-dot{stroke:var(--surface); stroke-width:2;}
  .chart-tooltip{
    position:absolute; top:4px; display:none; pointer-events:none; z-index:5;
    background:var(--surface-2); border:1px solid var(--hairline); border-radius:4px; box-shadow:var(--shadow);
    padding:8px 11px; font-size:.76rem; min-width:104px; max-width:240px;
  }
  .tt-year{font-family:var(--font-mono); color:var(--ink-3); margin-bottom:3px; font-size:.68rem; letter-spacing:.03em;}
  .tt-row{display:flex; align-items:center; gap:6px; color:var(--ink-2); white-space:nowrap; padding:1px 0;}
  .tt-row i{width:7px; height:7px; border-radius:50%; flex:none;}
  .tt-row b{color:var(--ink); font-family:var(--font-mono); font-variant-numeric:tabular-nums;}

  .bar-chart{display:flex; flex-direction:column; gap:8px; min-width:0;}
  .bar-row{display:grid; grid-template-columns:minmax(78px,180px) 1fr auto; gap:10px; align-items:center; min-width:0;}
  .bar-label{font-size:.8rem; color:var(--ink-2); line-height:1.25; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
  .bar-track{height:20px; background:var(--hairline-2); border-radius:3px; overflow:hidden; position:relative; min-width:0;}
  .bar-fill{
    height:100%; border-radius:3px; width:0%; transition:width .9s cubic-bezier(.16,.9,.25,1); min-width:2px;
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

  footer.doc-foot{
    max-width:860px; margin:80px auto 0; padding:24px 24px 60px; border-top:1px solid var(--hairline);
    font-size:.82rem; color:var(--ink-3);
  }
  footer.doc-foot p{max-width:74ch;}

  ::selection{background:var(--accent); color:var(--accent-ink);}

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
        svgEl('stop', {offset:'0%', 'stop-color':cor, 'stop-opacity':.22}, grad);
        svgEl('stop', {offset:'100%', 'stop-color':cor, 'stop-opacity':0}, grad);
        const base = yAt(vMin);
        const area = d + 'L'+validPts[validPts.length-1][0].toFixed(2)+','+base.toFixed(2)+' L'+validPts[0][0].toFixed(2)+','+base.toFixed(2)+' Z';
        svgEl('path', {d:area, fill:'url(#'+gid+')', stroke:'none'}, svg);
      }
      svgEl('path', {d:d, fill:'none', stroke:cor, 'stroke-width':apagada?1.1:2, 'stroke-opacity':apagada?.6:1, 'stroke-linecap':'round', 'stroke-linejoin':'round'}, svg);
      const last = validPts[validPts.length-1];
      if (last && !apagada && opts.endLabels !== false){
        svgEl('circle', {cx:last[0], cy:last[1], r:3.2, fill:cor}, svg);
        if (destacadas.length <= (opts.maxDirectLabels || 8)){
          const t = svgEl('text', {x:last[0]+7, y:last[1], class:'end-label', fill:cor}, svg);
          t.textContent = s.format ? s.format(s.values[s.values.length-1]) : fmtY(s.values[s.values.length-1]);
        }
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
print(f"wrote {OUT_PATH}: {len(doc)} chars, {len(scripts)} charts, {sum(len(v) for _,v in MAP_GROUPS)} maps")
