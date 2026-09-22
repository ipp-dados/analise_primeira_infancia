# -*- coding: utf-8 -*-
"""Build a self-contained, print-ready HTML report that mirrors analise.py
section by section (same order/titles/notes), embedding the *actual*
matplotlib/seaborn PNGs from visualizacoes/ (notebook visual style) --
never a re-rendered/custom chart engine -- plus a plain data table (sourced
from tabelas_finais/) under each chart. Run render_pdf.py on its output to
get the final PDF.

This script is a direct transcription of analise.py's markdown cells and
plotting/export calls as of this branch (specs/visual-identity) -- if
analise.py's sections, column names, or exported filenames change, this
needs matching edits. It is not a generic notebook-to-PDF converter.

Run from the project root:
    python build_notebook_report.py <out.html>

Maps are embedded directly from mapas/*.png (resized/WebP via Pillow, same
technique as build_html_report.py) -- no longer routed through
relatorio/*.html + extract_maps.py, since the consolidated relatorio/relatorio.html
(specs/visual-identity) embeds maps as plain <img> tags, not a `const MAPS = [...]`
JS array extract_maps.py could parse.
"""
import base64
import datetime
import io
import math
import os
import re
import sys

import pandas as pd
from PIL import Image

out_path = sys.argv[1] if len(sys.argv) > 1 else sys.argv[-1]

TF = "tabelas_finais"
VIZ = "visualizacoes"
MAPAS = "mapas"

# ---------------------------------------------------------------- helpers --

def fmt_num(x, dec=0):
    """pt-BR number formatting: '.' thousands, ',' decimal."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    s = f"{x:,.{dec}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")

def img_b64(png_name):
    with open(f"{VIZ}/{png_name}", "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

def chart_block(png_name, src_csv=None):
    b64 = img_b64(png_name)
    src = f'<div class="out-src">{src_csv}</div>' if src_csv else ""
    return f'<div class="out"><img class="chart-img" src="data:image/png;base64,{b64}" alt="{png_name}">{src}</div>'

def map_card(png_name, caption, max_width=1400):
    img = Image.open(f"{MAPAS}/{png_name}").convert("RGB")
    if img.width > max_width:
        h = int(img.height * max_width / img.width)
        img = img.resize((max_width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="WEBP", quality=80, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f'<figure class="map-card"><img src="data:image/webp;base64,{b64}" alt="{caption}"><figcaption class="map-cap">{caption}</figcaption></figure>'

def clean_causa(label):
    """Strip a leading CID-10-style numeric code ('1.2.1 ') from a label."""
    return re.sub(r'^\d[\d.]*\.?\s*', '', str(label))

def table_html(df, dec=0, pct_cols=None, dec_cols=None, rename=None, na="", clean_headers=False):
    """Render a dataframe as a plain HTML table with pt-BR number formatting.

    - Any column literally named 'ano' is rendered as a bare year (no
      thousands separator) regardless of its pandas dtype.
    - pct_cols columns are assumed to already be on a 0-100 scale (not 0-1) --
      multiply by 100 first at the call site if the source column is a
      fraction (e.g. PNAD's 'Total' column was 0-1 in the source CSV).
    - Tables with more than 6 columns get a 'wide' class (smaller font,
      table-layout:fixed, wrapping headers) so long series names don't blow
      out the printable page width -- a fixed-width table with nowrap
      headers silently overflows in Chrome's print output with no visible
      error, just a clipped/unreadable table.
    """
    pct_cols = pct_cols or []
    dec_cols = dec_cols or {}
    df = df.copy()
    for col in df.columns:
        if col.strip().lower() == "ano":
            df[col] = df[col].map(lambda v: str(int(v)) if pd.notna(v) else na)
        elif col in pct_cols:
            d = dec_cols.get(col, 1)
            df[col] = df[col].map(lambda v: (fmt_num(v, d) + "%") if pd.notna(v) else na)
        elif pd.api.types.is_float_dtype(df[col]) or pd.api.types.is_integer_dtype(df[col]):
            d = dec_cols.get(col, dec)
            df[col] = df[col].map(lambda v: fmt_num(v, d) if pd.notna(v) else na)
    if clean_headers:
        df = df.rename(columns={c: clean_causa(c) for c in df.columns if c.strip().lower() != "ano"})
    if rename:
        df = df.rename(columns=rename)
    classes = "plain wide" if len(df.columns) > 6 else "plain"
    html = df.to_html(index=False, classes=classes, border=0, na_rep=na, escape=True)
    html = html.replace(f' class="dataframe {classes}"', f' class="{classes}"')
    return f'<div class="table-scroll">{html}</div>'

def read(name, **kw):
    return pd.read_csv(f"{TF}/{name}", **kw)

def h2(text): return f"<h2>{text}</h2>"
def h3(text): return f"<h3>{text}</h3>"
def h4(text): return f"<h4>{text}</h4>"
def h5(text): return f"<h5>{text}</h5>"
def h6(text): return f"<h6>{text}</h6>"
def p(html): return f'<p class="lede">{html}</p>'
def note(html): return f'<blockquote class="note"><p>{html}</p></blockquote>'
def notes_list(items):
    return '<ul class="notes">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

# ------------------------------------------------------------- page parts --
# Mirrors analise.py section by section: titles/notes are transcribed from
# its markdown cells; each `chart_block` + `table_html` pair corresponds to
# one `serie_temporal`/`grafico_barra`/`serie_temporal_multipla` call there.

parts = []
add = parts.append

add('<header class="doc-head">')
add('<h1><span class="glyph">\U0001F3DB️</span>Análise Primeira Infância Carioca</h1>')
add('<p class="sub">Extração, limpeza e visualização dos indicadores de primeira infância (0 a 6 anos) do município do Rio de Janeiro — Censo, CadÚnico, DataSus/Tabnet (nascidos vivos, mortalidade, causas evitáveis, cobertura vacinal) e educação (PNAD/Censo Escolar).</p>')
add('<div class="meta"><span>Instituto Pereira Passos</span><span id="gen-date">—</span><span>a partir de <code>analise.py</code></span></div>')
add('</header>')

add(h2('\U0001F9ED Visualização dos Dados'))
add(p('Para acesso aos dados brutos via Drive: <a href="https://drive.google.com/drive/folders/1xOwf72QfaDuJAHuA-Vngl6t5_kzSfGYX?usp=sharing">pasta compartilhada</a>.<br>OBS: acesso restrito, solicitar a leonardo.aucar@prefeitura.rio'))

add(h3('\U0001F3D8️ Censo 2022 <span style="opacity:.6">(10/00)</span>'))
add(p('Dados do Censo IBGE 2022 (agregados DataRio), população por bairro e faixa etária.'))
add(h4('Por bairro'))
add(p('Bairros com mais crianças de 0 a 4 anos, por número absoluto e percentual da população local.'))

df_censo_bairro = read("censo_por_bairro.csv")
top10 = df_censo_bairro.sort_values("0 a 4 anos", ascending=False).head(10)[["bairro", "0 a 4 anos", "Percentual 0 a 4"]]
add('<div class="out">' + table_html(top10, pct_cols=["Percentual 0 a 4"], rename={"bairro": "Bairro", "Percentual 0 a 4": "% do bairro"}) + '</div>')

add(h4('Serie temporal censo'))
add(p('Evolução da população de 0 a 4 anos entre os Censos 2000, 2010 e 2022 (Tabela 2974/IBGE), agregada para o município.'))
add(chart_block("censo_0_a_4_serie_total_ano.png", "censo_0_a_4_anos_por_ano.csv"))
df_censo_serie = read("censo_0_a_4_anos_por_ano.csv")
add(table_html(df_censo_serie[["ano", "0 a 4 anos", "Sexo feminino, 0 a 4 anos", "Sexo masculino, 0 a 4 anos"]], rename={"ano": "Ano"}))
add(chart_block("censo_0_a_4_serie_percentual_ano.png", "censo_0_a_4_anos_por_ano.csv"))
add(table_html(df_censo_serie[["ano", "Percentual 0 a 4 anos"]], pct_cols=["Percentual 0 a 4 anos"], rename={"ano": "Ano"}))

add(h4('População 0-6 por idade/raça/sexo (IBGE SIDRA, 2022)'))
add(p('Complementa o Censo por bairro acima com o detalhe por idade simples (0 a 6 anos) e por raça/sexo, direto das tabelas do IBGE SIDRA (Censo 2022, tabela 9606). Só existe no nível município.'))
add(chart_block("censo_sidra_populacao_0_6_raca_2022.png", "censo_sidra_populacao_0_6_raca_2022.csv"))
add(chart_block("censo_sidra_populacao_0_6_sexo_2022.png", "censo_sidra_populacao_0_6_sexo_2022.csv"))

add(h3('\U0001F5C2️ Cadúnico'))
add(p('Fonte: CadÚnico via banco CTPE (<code>silver_cadunico_geral</code>), recorte de crianças 0-6 anos.'))
add(note('<b>Nota:</b> requer conexão ativa com o banco CTPE (credenciais em <code>.env</code>) para reproduzir; não roda apenas com os arquivos em <code>dados_locais/</code>. Os gráficos abaixo refletem o último export salvo em <code>tabelas_finais/</code>.'))

add(h4('Análise por renda'))
add('<div class="out-pair">')
add(chart_block("cadunico_familias_por_faixa_renda.png", "cadunico_por_faixa_etaria_2026.csv"))
add(chart_block("cadunico_criancas_por_faixa_renda.png", "cadunico_por_faixa_etaria_2026.csv"))
add('</div>')
add(table_html(read("cadunico_por_faixa_etaria_2026.csv"), rename={"faixa de renda": "Faixa de renda"}))

add(h4('Análise por idade'))
add('<div class="out-pair">')
add(chart_block("cadunico_familias_por_idade.png", "cadunico_por_idade_2026.csv"))
add(chart_block("cadunico_criancas_por_idade.png", "cadunico_por_idade_2026.csv"))
add('</div>')
df_idade = read("cadunico_por_idade_2026.csv")
df_idade["idade"] = df_idade["idade"].astype(int)
add(table_html(df_idade, rename={"idade": "Idade"}))

add(h3('\U0001F3E5 DataSus - tabnet'))
add(p('Séries do Datasus/Tabnet (nascidos vivos e óbitos), por bairro de residência, padronizadas pela função <code>limpeza_tabnet_bairros</code>.'))

add(h4('Nascidos Vivos'))
add(p('Nascidos vivos totais por bairro (2006-2025).'))
add(chart_block("nascidos_vivos_por_ano.png", "nascidos_vivos_por_ano.csv"))
add(table_html(read("nascidos_vivos_por_ano.csv")[["ano", "nascidos vivos"]], rename={"ano": "Ano"}))

add(h4('Nascidos abaixo peso'))
add(p('Nascidos vivos com baixo peso (&lt;2.500g) por bairro, como percentual dos nascidos vivos totais.'))
add(chart_block("nascidos_abaixo_peso_percentual_por_ano.png", "nascidos_abaixo_peso_por_ano.csv"))
df_bp = read("nascidos_abaixo_peso_por_ano.csv")[["ano", "nascidos abaixo peso", "percentual abaixo do peso"]]
add(table_html(df_bp, pct_cols=["percentual abaixo do peso"], rename={"ano": "Ano", "percentual abaixo do peso": "% abaixo do peso"}))

add(h4('\U0001F4C9 Mortalidade'))
add(p('Óbitos até 1 ano de idade: por raça/cor, causas evitáveis, gravidez/puerpério e mortalidade neonatal (precoce, tardia, pós-neonatal e total).'))

RACA_LABEL = {"amarela": "Amarela", "branca": "Branca", "indigena": "Indígena", "parda": "Parda", "preta": "Preta", "nao_informado": "Não informado"}

add(h5('Óbitos até 1 ano por raça/cor'))
add(p('Combina os óbitos de menores de 1 ano (0 a 364 dias) por raça/cor (2006-2025) com os nascidos vivos por raça/cor da mãe (2011-2025), ambos por bairro de residência.'))
add(notes_list([
    'Colunas de ano ausentes nos arquivos do Tabnet indicam total 0 no período e são preenchidas com 0 na limpeza.',
    'As categorias <code>Ignorado</code> e <code>Não informado</code> de nascidos vivos representam a mesma informação ausente, registrada sob nomes diferentes ao longo da série → somadas em <code>nascidos_nao_informado</code>.',
    'O percentual de óbitos por raça só é calculável a partir de 2011, quando começa a série de nascidos vivos por raça/cor da mãe.',
    'Óbitos e nascidos vivos por raça vêm de consultas independentes do Datasus (óbito de residente x nascimento registrado no bairro) → em bairros/anos com poucos casos é possível ter óbitos de uma raça sem nascidos vivos correspondentes, gerando percentuais instáveis ou indefinidos (tratados como NaN). Afeta principalmente <code>indigena</code>, <code>amarela</code> e <code>nao_informado</code>, categorias com poucas observações.',
]))
df_raca = read("mortalidade_raca_municipio_ano.csv")
add(chart_block("obitos_raca_ano.png", "mortalidade_raca_municipio_ano.csv"))
obitos_cols = [f"obitos_{r}" for r in RACA_LABEL]
add(table_html(df_raca[["ano"] + obitos_cols], rename={"ano": "Ano", **{f"obitos_{r}": lbl for r, lbl in RACA_LABEL.items()}}))
add(chart_block("percentual_mortalidade_raca_ano.png", "mortalidade_raca_municipio_ano.csv"))
pct_cols = [f"percentual_{r}" for r in RACA_LABEL]
add(table_html(df_raca[["ano"] + pct_cols], pct_cols=pct_cols, rename={"ano": "Ano", **{f"percentual_{r}": lbl for r, lbl in RACA_LABEL.items()}}))

add(h5('Óbitos por causas evitáveis, por grupo de causa (CID-10)'))
add(p('Usa os arquivos "segundo causas" (não por raça/cor), que classificam cada óbito evitável em uma hierarquia de grupo/subgrupo/causa específica. Soma as três faixas etárias (0-6, 7-27 e 28-364 dias) para obter o total 0-364 dias, no nível de município (1996-2025).'))
add(notes_list([
    'Grupo (<code>1.</code>, <code>2.</code>, <code>3.</code>): nível mais alto da hierarquia. Subgrupo: filhos diretos do grupo <code>1.</code> mais o próprio grupo <code>2.</code> (que não se divide em subgrupos).',
    '<code>3. Demais causas (não claramente evitáveis)</code> não tem subgrupos e por isso só aparece no gráfico de grupo.',
]))
add(chart_block("obitos_causas_evitaveis_grupo_ano.png", "mortalidade_causas_evitaveis_grupo_ano.csv"))
add(table_html(read("mortalidade_causas_evitaveis_grupo_ano.csv"), rename={"ano": "Ano"}))
add(chart_block("obitos_causas_evitaveis_subgrupo_ano.png", "mortalidade_causas_evitaveis_subgrupo_ano.csv"))
add(table_html(read("mortalidade_causas_evitaveis_subgrupo_ano.csv"), rename={"ano": "Ano"}, clean_headers=True))

add(h5('Óbitos por causas evitáveis, por grupo de causa e faixa etária'))
add(p('Mesma classificação de grupo/subgrupo da seção anterior, mas sem somar as três faixas etárias: cada uma (0-6, 7-27 e 28-364 dias) é analisada separadamente.'))

for faixa_id, faixa_titulo in [("0_6", "Precoce (0 a 6 dias)"), ("7_27", "Tardia (7 a 27 dias)"), ("28_364", "Pós-neonatal (28 a 364 dias)")]:
    add(h6(faixa_titulo))
    add(chart_block(f"obitos_causas_evitaveis_grupo_{faixa_id}_ano.png", f"mortalidade_causas_evitaveis_grupo_{faixa_id}_ano.csv"))
    add(table_html(read(f"mortalidade_causas_evitaveis_grupo_{faixa_id}_ano.csv"), rename={"ano": "Ano"}))
    add(chart_block(f"obitos_causas_evitaveis_subgrupo_{faixa_id}_ano.png", f"mortalidade_causas_evitaveis_subgrupo_{faixa_id}_ano.csv"))
    add(table_html(read(f"mortalidade_causas_evitaveis_subgrupo_{faixa_id}_ano.csv"), rename={"ano": "Ano"}, clean_headers=True))

add(h6('Comparação entre faixas etárias (2025)'))
add(p('Gráfico de barras comparando os subgrupos de causas evitáveis entre as três faixas etárias, no último ano disponível (2025).'))
add(chart_block("obitos_causas_evitaveis_subgrupo_faixa_2025.png", "mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv"))
df_faixa2025 = read("mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv")
df_faixa2025_wide = df_faixa2025.pivot(index="subgrupo", columns="faixa_etaria", values="obitos").reset_index()
ordem_faixa = [c for c in ["0-6 dias", "7-27 dias", "28-364 dias"] if c in df_faixa2025_wide.columns]
df_faixa2025_wide = df_faixa2025_wide[["subgrupo"] + ordem_faixa]
df_faixa2025_wide["subgrupo"] = df_faixa2025_wide["subgrupo"].map(clean_causa)
add(table_html(df_faixa2025_wide, rename={"subgrupo": "Subgrupo"}))

add(h5('Primeira infância, por Área Programática de Saúde (CAP)'))
add(p('Coordenadorias de Área Programática da SMS-Rio (10 unidades) — divisão territorial diferente das 5 Áreas de Planejamento do IPP usadas nos mapas do Censo.'))

df_cap_faixa = read("mortalidade_evitaveis_cap_faixa_ano.csv")
df_grupo_cap_faixa = read("mortalidade_evitaveis_grupo_cap_faixa_ano.csv")
_FAIXAS_CAP = [("menores_1_ano", "menores de 1 ano", "Menores de 1 ano"), ("1_a_4_anos", "de 1 a 4 anos", "De 1 a 4 anos"), ("menores_5_anos", "menores de 5 anos", "Menores de 5 anos")]

def cap_pivot_table(df, value_col, faixa_full, fmt_pct=False):
    sub = df[df["faixa_etaria"] == faixa_full]
    wide = sub.pivot(index="ano", columns="cod_ap_sms", values=value_col).reset_index()
    wide.columns = ["ano"] + [f"CAP {c}" for c in wide.columns[1:]]
    cap_cols = [c for c in wide.columns if c != "ano"]
    return table_html(wide, pct_cols=cap_cols if fmt_pct else [], rename={"ano": "Ano"})

add(h6('Panorama municipal, por subgrupo'))
for sufixo, faixa_full, faixa_lbl in _FAIXAS_CAP:
    add(h6(faixa_lbl))
    fname = "obitos_evitaveis_menores_5_subgrupo_ano.png" if sufixo == "menores_5_anos" else f"obitos_evitaveis_{sufixo}_subgrupo_ano.png"
    add(chart_block(fname, "mortalidade_evitaveis_cap_faixa_ano.csv"))
    sub = df_cap_faixa[df_cap_faixa["faixa_etaria"] == faixa_full].groupby(["subgrupo", "ano"], as_index=False)["obitos"].sum()
    wide = sub.pivot(index="ano", columns="subgrupo", values="obitos").reset_index()
    add(table_html(wide, rename={"ano": "Ano"}, clean_headers=True))

add(h6('Grupo evitável, por CAP'))
for sufixo, faixa_full, faixa_lbl in _FAIXAS_CAP:
    add(p(faixa_lbl))
    if sufixo == "menores_5_anos":
        add(chart_block("obitos_evitaveis_cap_menores_5_anos_ano.png", "mortalidade_evitaveis_grupo_cap_faixa_ano.csv"))
    else:
        add(chart_block(f"obitos_evitaveis_cap_{sufixo}_ano.png", "mortalidade_evitaveis_grupo_cap_faixa_ano.csv"))
    add(cap_pivot_table(df_grupo_cap_faixa, "1. Causas evitáveis", faixa_full))
    add(chart_block(f"percentual_evitaveis_cap_{sufixo}_ano.png", "mortalidade_evitaveis_grupo_cap_faixa_ano.csv"))
    add(cap_pivot_table(df_grupo_cap_faixa, "percentual_evitaveis", faixa_full, fmt_pct=True))
add(chart_block("obitos_evitaveis_total_cap_ano.png", "mortalidade_evitaveis_grupo_cap_faixa_ano.csv"))
add(cap_pivot_table(df_grupo_cap_faixa, "total", "menores de 5 anos"))

add(h6('Panorama municipal (< 5 anos) e taxa'))
add(chart_block("taxa_mortalidade_evitaveis_menores_5_ano.png", "taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv"))
add(table_html(read("taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv"), dec_cols={"taxa_por_mil": 1}, rename={"ano": "Ano", "obitos": "Óbitos", "nascidos_vivos": "Nascidos vivos", "taxa_por_mil": "Taxa (‰)"}))

add(h4('\U0001F4CB Óbitos gravidez e puerpério'))
add(p('Óbitos maternos durante a gravidez e o puerpério, por bairro de residência (2006-2025).'))
add(chart_block("obitos_gravidez_por_ano.png", "obitos_gravidez_por_ano.csv"))
add(table_html(read("obitos_gravidez_por_ano.csv"), rename={"ano": "Ano"}))
add(chart_block("obitos_puerperio_por_ano.png", "obitos_puerperio_por_ano.csv"))
add(table_html(read("obitos_puerperio_por_ano.csv"), rename={"ano": "Ano"}))

add(h4('\U0001FA7A Mortalidade Neonatal'))
add(p('Óbitos de menores de 1 ano por faixa etária (precoce, tardia, pós-neonatal e total 0-364 dias), com taxa por 1.000 nascidos vivos.'))
add(note('<b>Nota:</b> Precoce e Tardia comparam com os nascidos vivos por <i>inner join</i> (bairros sem óbito registrado em algum lado ficam de fora); Pós-neonatal e Total usam uma grade bairro x ano com zeros explícitos, mais robusta.'))

add(h5('Precoce (0 a 6 dias)'))
add(chart_block("taxa_mortalidade_precoce_ano.png", "mortalidade_neonatal_precoce_por_ano.csv"))
add(table_html(read("mortalidade_neonatal_precoce_por_ano.csv"), dec_cols={"taxa_mortalidade_precoce": 1}, rename={"ano": "Ano", "obitos precoces": "Óbitos precoces", "nascidos vivos": "Nascidos vivos", "taxa_mortalidade_precoce": "Taxa (‰)"}))

add(h5('Tardia (7 a 27 dias)'))
add(chart_block("taxa_obitos_tardios_ano.png", "mortalidade_neonatal_tardia_por_ano.csv"))
add(table_html(read("mortalidade_neonatal_tardia_por_ano.csv"), dec_cols={"taxa_obitos_tardios": 1}, rename={"ano": "Ano", "obitos_tardios": "Óbitos tardios", "nascidos vivos": "Nascidos vivos", "taxa_obitos_tardios": "Taxa (‰)"}))

add(h5('Pós-neonatal (28 a 364 dias)'))
add(p('Não há arquivo pronto para 28-364 dias (total, sem raça): é derivado por subtração <code>0-364 - 0-6 - 7-27</code>, numa grade completa bairro x ano.'))
df_infantil = read("mortalidade_infantil_pos_neonatal_total_por_ano.csv")
add(chart_block("taxa_mortalidade_pos_neonatal_ano.png", "mortalidade_infantil_pos_neonatal_total_por_ano.csv"))
add(table_html(df_infantil[["ano", "obitos_28_364", "nascidos_vivos", "taxa_mortalidade_pos_neonatal"]], dec_cols={"taxa_mortalidade_pos_neonatal": 1}, rename={"ano": "Ano", "obitos_28_364": "Óbitos 28-364d", "nascidos_vivos": "Nascidos vivos", "taxa_mortalidade_pos_neonatal": "Taxa (‰)"}))

add(h5('Total (0 a 364 dias)'))
add(chart_block("taxa_mortalidade_infantil_ano.png", "mortalidade_infantil_pos_neonatal_total_por_ano.csv"))
add(table_html(df_infantil[["ano", "obitos_0_364", "nascidos_vivos", "taxa_mortalidade_infantil"]], dec_cols={"taxa_mortalidade_infantil": 1}, rename={"ano": "Ano", "obitos_0_364": "Óbitos 0-364d", "nascidos_vivos": "Nascidos vivos", "taxa_mortalidade_infantil": "Taxa (‰)"}))

add(h3('\U0001F957 DataSus - SISVAN'))
add(p('Percentual de crianças 0-6 anos com sobrepeso/obesidade e desnutrição, agregado por ano (fonte: SISVAN).'))
add(chart_block("sisvan_desnutricao_percentual_por_ano.png", "sisvan_desnutricao_por_ano.csv"))
add(table_html(read("sisvan_desnutricao_por_ano.csv")[["ano", "Percent. baixo peso total"]], pct_cols=["Percent. baixo peso total"], rename={"ano": "Ano"}))
add(chart_block("sisvan_sobrepeso_percentual_por_ano.png", "sisvan_sobrepeso_por_ano.csv"))
add(table_html(read("sisvan_sobrepeso_por_ano.csv")[["ano", "Percent. sobrepeso total"]], pct_cols=["Percent. sobrepeso total"], rename={"ano": "Ano"}))
add(chart_block("sisvan_obesidade_percentual_por_ano.png", "sisvan_sobrepeso_por_ano.csv"))
add(table_html(read("sisvan_sobrepeso_por_ano.csv")[["ano", "obesidade_percentual"]], pct_cols=["obesidade_percentual"], rename={"ano": "Ano", "obesidade_percentual": "% obesidade"}))

add(h3('\U0001F489 Cobertura Vacinal EPI'))
add(p('Cobertura vacinal (%) por imunobiológico, série histórica do EPI/SVS-Rio (2016-2026).'))
add(notes_list([
    'Cobertura acima de 100% é esperada em dados administrativos de vacinação (numerador de doses aplicadas pode incluir população fora do denominador estimado) — não é um erro de cálculo.',
    '2026 é um ano ainda em curso (dados parciais); comparar com cautela contra os anos fechados.',
]))
df_vac = read("cobertura_vacinal_epi_por_ano.csv")
vac_cols = [c for c in df_vac.columns if c != "ano"]
add(table_html(df_vac, pct_cols=vac_cols, rename={"ano": "Ano"}))

add(p('Comparativo direto entre quatro anos (2016, 2019, 2022 e 2025) por imunobiológico, para visualizar o impacto da pandemia (queda em 2022) e a recuperação até 2025.'))
add(chart_block("cobertura_vacinal_epi_comparativo_anos.png", "cobertura_vacinal_epi_comparativo_anos.csv"))
df_vac_comp = read("cobertura_vacinal_epi_comparativo_anos.csv")
df_vac_comp_wide = df_vac_comp.pivot(index="ano", columns="imunobiologico", values="cobertura").reset_index()
vac_comp_cols = [c for c in df_vac_comp_wide.columns if c != "ano"]
add(table_html(df_vac_comp_wide, pct_cols=vac_comp_cols, rename={"ano": "Ano"}))

add(h3('\U0001F393 PNAD Contínua, Censo Escolar e INEP'))
add(p('Frequência escolar (PNAD Contínua) e matrículas (Censo Escolar/INEP) de crianças de 0 a 6 anos.'))

add(h4('Frequência escolar 0-6 anos (IBGE SIDRA, Censo 2022)'))
add(p('Comparativo mais recente e granular (idade simples, por raça/sexo) que a série PNAD abaixo — o Censo é enumeração completa de um único ano (2022), a PNAD Contínua é amostral com série histórica. Não são diretamente comparáveis ano a ano.'))
add(chart_block("sidra_frequencia_escola_0_5_raca_2022.png", "sidra_frequencia_escola_0_5_raca_2022.csv"))
add(chart_block("sidra_frequencia_escola_0_5_sexo_2022.png", "sidra_frequencia_escola_0_5_sexo_2022.csv"))
add(chart_block("sidra_taxa_frequencia_0_6_raca_2022.png", "sidra_taxa_frequencia_0_6_raca_2022.csv"))
add(chart_block("sidra_taxa_frequencia_0_6_sexo_2022.png", "sidra_taxa_frequencia_0_6_sexo_2022.csv"))

add(h4('Taxa de frequência escolar'))
df_freq = read("frequencia_escolar_pnad_por_idade.csv")
add(chart_block("pnad_frequencia_escolar_por_idade.png", "frequencia_escolar_pnad_por_idade.csv"))
df_freq["Total"] = df_freq["Total"] * 100  # source column is a 0-1 fraction, not already 0-100
add(table_html(df_freq, pct_cols=["Total"], dec_cols={"Total": 1}, rename={"Total": "% frequência"}))

add(h4('Número de matrículas 0 a 6 anos <span style="opacity:.6">(complementar 2021-2025)</span>'))
add(chart_block("matriculas_0_a_6_por_ano.png", "matriculas_0_a_6_por_ano.csv"))
add(table_html(read("matriculas_0_a_6_por_ano.csv")[["ano", "matriculas"]], rename={"ano": "Ano", "matriculas": "Matrículas"}))

add(h2('\U0001F5FA️ Mapas'))
add(p('Mapas coropléticos por bairro/CAP, gerados a partir das tabelas exportadas para <code>tabelas_finais/</code>.'))

MAP_GROUPS = [
    ("Censo/população", [
        ("mapa_censo_0_4_absoluto.png", "Crianças de 0 a 4 anos, por bairro (Censo 2022)"),
        ("mapa_censo_0_4_percentual.png", "% de crianças de 0 a 4 anos, por bairro (Censo 2022)"),
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
    ("Mortalidade neonatal", [
        ("mapa_obitos_neonatal_precoce_bairro_2025.png", "Óbitos precoces (0-6 dias) por bairro (2025)"),
        ("mapa_taxa_mortalidade_precoce_bairro_2025.png", "Taxa de óbitos precoces por bairro (2025)"),
        ("mapa_taxa_obitos_tardios_bairro_2025.png", "Taxa de óbitos tardios por bairro (2025)"),
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
    ]),
]

available_maps = set(os.listdir(MAPAS))
missing_maps = [fn for _, group in MAP_GROUPS for fn, _ in group if fn not in available_maps]
if missing_maps:
    raise SystemExit(f"missing map PNGs: {missing_maps}")

for tema, imgs in MAP_GROUPS:
    add(h3(tema))
    add('<div class="map-gallery">')
    for fn, caption in imgs:
        add(map_card(fn, caption))
    add('</div>')

footer = '<footer class="doc-foot"><p>Fontes: IBGE (Censo), CTPE/CadÚnico, Datasus/Tabnet (SINASC, SIM), SISVAN, EPI/SVS-Rio, PNAD Contínua e Censo Escolar/INEP. Elaborado a partir do pipeline documentado em <code>analise.py</code> — Instituto Pereira Passos, Prefeitura da Cidade do Rio de Janeiro. Gráficos gerados pelo próprio notebook (matplotlib/seaborn), a partir das tabelas de <code>tabelas_finais/</code>.</p></footer>'

# ------------------------------------------------------------ full doc -----

gen_date = datetime.date.today().strftime("%d de %B de %Y")
MESES = {"January": "janeiro", "February": "fevereiro", "March": "março", "April": "abril", "May": "maio", "June": "junho",
         "July": "julho", "August": "agosto", "September": "setembro", "October": "outubro", "November": "novembro", "December": "dezembro"}
for en, pt in MESES.items():
    gen_date = gen_date.replace(en, pt)

body = "\n".join(parts).replace('<span id="gen-date">—</span>', f'<span id="gen-date">Atualizado {gen_date}</span>')
body += "\n" + footer

CSS = r"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,440;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
  :root{
    --page:#FFFFFF; --surface:#FFFFFF; --ink:#1A1A1A; --ink-2:#595959; --ink-3:#8C8C8C;
    --hairline:rgba(0,0,0,0.12); --hairline-2:rgba(0,0,0,0.06);
    --note-bg:#F5F5F5; --note-ink:#4D4D4D; --note-border:#B3B3B3;
    --shadow:0 1px 2px rgba(0,0,0,.04), 0 6px 16px -10px rgba(0,0,0,.10);
    --font-display:'Fraunces',Georgia,'Times New Roman',serif;
    --font-body:'IBM Plex Sans',-apple-system,'Segoe UI',sans-serif;
    --font-mono:'IBM Plex Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
  }
  *{box-sizing:border-box;}
  html,body{background:var(--page); color:var(--ink);}
  body{margin:0; font-family:var(--font-body); line-height:1.6; font-size:16px; -webkit-font-smoothing:antialiased;}
  a{color:var(--ink); text-decoration:underline;}
  code{font-family:var(--font-mono); font-size:.92em; background:var(--hairline-2); padding:.1em .35em; border-radius:3px;}
  .doc{max-width:800px; margin:0 auto; padding:40px 24px 80px;}
  header.doc-head{margin-bottom:8px;}
  header.doc-head h1{font-family:var(--font-display); font-weight:600; font-size:2.4rem; margin:0 0 6px; line-height:1.12; display:flex; align-items:center; gap:14px;}
  header.doc-head h1 .glyph{font-size:.82em; flex:none;}
  header.doc-head .sub{color:var(--ink-2); font-size:1.02rem; max-width:64ch; margin:0 0 18px;}
  header.doc-head .meta{display:flex; flex-wrap:wrap; gap:6px 16px; font-family:var(--font-mono); font-size:.76rem; color:var(--ink-3); padding-bottom:24px; border-bottom:1px solid var(--hairline);}
  h2{font-family:var(--font-display); font-weight:600; font-size:1.7rem; margin:56px 0 4px; padding-top:24px; border-top:1px solid var(--hairline); line-height:1.2;}
  h2:first-of-type{margin-top:32px;}
  h3{font-family:var(--font-display); font-weight:600; font-size:1.36rem; margin:40px 0 4px; line-height:1.2;}
  h4{font-family:var(--font-display); font-weight:600; font-size:1.14rem; margin:30px 0 4px;}
  h5{font-family:var(--font-body); font-weight:600; font-size:1rem; margin:24px 0 4px; color:var(--ink);}
  h6{font-family:var(--font-body); font-weight:600; font-size:.9rem; margin:20px 0 4px; color:var(--ink-2); text-transform:uppercase; letter-spacing:.03em;}
  p.lede{color:var(--ink-2); max-width:70ch; margin:6px 0 4px; font-size:.96rem;}
  ul.notes{margin:8px 0 4px; padding-left:1.2em; max-width:70ch; color:var(--ink-2); font-size:.88rem;}
  ul.notes li{margin:4px 0;}
  blockquote.note{margin:12px 0 4px; padding:9px 14px; background:var(--note-bg); border-left:3px solid var(--note-border); border-radius:0 3px 3px 0; max-width:68ch;}
  blockquote.note p{margin:0; font-size:.86rem; color:var(--note-ink); line-height:1.5;}
  blockquote.note b{color:var(--ink);}
  .out{margin:14px 0 6px; background:var(--surface); border:1px solid var(--hairline); border-radius:4px; box-shadow:var(--shadow); padding:14px 16px 12px;}
  .out-pair{display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; margin:14px 0 6px;}
  .out-pair > .out{margin:0;}
  .out-src{font-family:var(--font-mono); font-size:.68rem; color:var(--ink-3); margin-top:8px; padding-top:6px; border-top:1px solid var(--hairline-2);}
  .chart-img{width:100%; height:auto; display:block; border-radius:2px;}
  .table-scroll{overflow-x:auto; margin-top:2px;}
  table.plain{width:100%; border-collapse:collapse; font-size:.74rem; margin:10px 0 18px;}
  table.plain th, table.plain td{text-align:right; padding:4px 8px; border-bottom:1px solid var(--hairline-2); white-space:nowrap; font-variant-numeric:tabular-nums;}
  table.plain th:first-child, table.plain td:first-child{text-align:left; font-variant-numeric:normal;}
  table.plain th{color:var(--ink-3); font-weight:500; font-size:.7rem;}
  table.plain.wide{table-layout:fixed; font-size:.62rem;}
  table.plain.wide th, table.plain.wide td{padding:3px 4px; white-space:normal; word-break:break-word;}
  table.plain.wide th{vertical-align:bottom; line-height:1.25;}
  table.plain.wide th:first-child, table.plain.wide td:first-child{white-space:normal;}
  .map-gallery{display:flex; flex-direction:column; gap:16px; margin:14px 0 6px;}
  .map-card{margin:0 auto; max-width:560px; width:100%; background:var(--surface); border:1px solid var(--hairline); border-radius:4px; box-shadow:var(--shadow); overflow:hidden;}
  .map-card img{display:block; width:100%; height:auto;}
  .map-cap{padding:8px 12px; font-size:.8rem; color:var(--ink-2); border-top:1px solid var(--hairline-2);}
  footer.doc-foot{max-width:800px; margin:56px auto 0; padding:20px 24px 40px; border-top:1px solid var(--hairline); font-size:.8rem; color:var(--ink-3);}
  footer.doc-foot p{max-width:72ch;}

  @media print{
    @page{ size:A4; margin:16mm 14mm 18mm; }
    html,body{ background:#fff !important; }
    .doc{ max-width:100% !important; padding:6px 4px 16px !important; }
    .doc > h2{ break-before:page; }
    .doc > h2:first-of-type{ break-before:auto; }
    .doc > h3{ break-before:page; }
    .doc > h3:first-of-type{ break-before:auto; }
    h3,h4,h5,h6{ break-after:avoid; }
    .out, .out-pair > .out, .map-card{ break-inside:avoid; }
    .out{ box-shadow:none; }
    table.plain{ break-inside:auto; }
    table.plain tr{ break-inside:avoid; }
    a{ color:inherit; text-decoration:none; }
    footer.doc-foot{ break-inside:avoid; }
  }
</style>
"""

doc = f"""<html data-theme="light">
<meta name="color-scheme" content="light">
<title>Primeira Infância Carioca · Notebook</title>
{CSS}
<div class="doc">
{body}
</div>
</html>
"""

with open(out_path, "w", encoding="utf-8") as f:
    f.write(doc)
print("wrote", out_path, len(doc), "chars")
