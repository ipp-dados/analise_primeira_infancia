# -*- coding: utf-8 -*-
"""Build a self-contained, print-ready HTML report that mirrors analise.py's
outputs -- charts (actual matplotlib/seaborn PNGs from visualizacoes/,
notebook visual style, never a re-rendered custom chart engine) and maps
(mapas/*.png) -- but organized by eixo da política municipal de primeira
infância (specs/estrutura_eixos.md), not by data source. Run render_pdf.py
on its output to get the final PDF.

Data tables that back a chart already shown in the body are moved to a
single appendix at the end of the document (specs/ajuste_eixos/plan.md,
Bloco 4) -- the body reads as narrative + charts + maps, numbers live in
one reference section, each linked by a "Tabela N" anchor.

This script is a direct transcription of analise.py's markdown cells and
plotting/export calls as of this branch (specs/ajuste_eixos) -- if
analise.py's sections, column names, or exported filenames change, this
needs matching edits. It is not a generic notebook-to-PDF converter.

Run from the project root:
    python build_notebook_report.py <out.html>

Maps are embedded directly from mapas/*.png (resized/WebP via Pillow, same
technique as build_html_report.py) -- no longer routed through
relatorio/*.html + extract_maps.py, since the consolidated relatorio/index.html
(specs/visual-identity) embeds maps as plain <img> tags, not a `const MAPS = [...]`
JS array extract_maps.py could parse.
"""
import base64
import datetime
import html
import io
import json
import math
import os
import random
import re
import sys
from pathlib import Path

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
    html_out = df.to_html(index=False, classes=classes, border=0, na_rep=na, escape=True)
    html_out = html_out.replace(f' class="dataframe {classes}"', f' class="{classes}"')
    return f'<div class="table-scroll">{html_out}</div>'

def read(name, **kw):
    return pd.read_csv(f"{TF}/{name}", **kw)

_toc = []      # (level, title, anchor_id) collected as h2()/h3() are called -- feeds the Sumário
_slugs = set()

def _slugify(text):
    """Same algorithm as build_html_report.py's slugify() -- kept in sync
    deliberately so the two generators' anchor ids read consistently, even
    though this file has no shared import with that one (each generator is
    a standalone snapshot per CLAUDE.md's convention)."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE).strip().lower()
    slug = re.sub(r'[\s_]+', '-', text) or 'sec'
    base, i = slug, 2
    while slug in _slugs:
        slug = f"{base}-{i}"
        i += 1
    _slugs.add(slug)
    return slug

def h2(text):
    sid = _slugify(text)
    _toc.append((2, text, sid))
    return f'<h2 id="{sid}">{text}</h2>'

def h3(text):
    sid = _slugify(text)
    _toc.append((3, text, sid))
    return f'<h3 id="{sid}">{text}</h3>'

def h4(text): return f"<h4>{text}</h4>"
def h5(text): return f"<h5>{text}</h5>"
def h6(text): return f"<h6>{text}</h6>"
def p(html_str): return f'<p class="lede">{html_str}</p>'
def note(html_str): return f'<blockquote class="note"><p>{html_str}</p></blockquote>'
def notes_list(items):
    return '<ul class="notes">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def _esc(text):
    return html.escape(str(text))

# ---- introducao: lorem ipsum placeholder, mesmo gerador/lista de palavras
# de build_html_report.py (specs/ajuste_eixos/specs.md §7 -- texto final é
# trabalho de curadoria futura, nao fabricado aqui) -- mantido em sincronia
# manualmente, mesma razao do _slugify acima.
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
        palavras = random.Random(f"{seed}-palavras").randint(100, 200)
    corpo = " ".join(rng.choice(_LOREM_WORDS) for _ in range(palavras))
    return corpo[:1].upper() + corpo[1:] + "."

# ---- textos curados: cada bloco de analise por grafico/mapa passa pelo
# helper abaixo em vez de chamar _lorem diretamente, para que um futuro
# script de sincronizacao (specs/ajuste_eixos/plan.md Bloco 7) possa injetar
# texto editado a mao (originado no DOCX de curadoria, relatorio/
# curadoria_textos.docx) sem precisar tocar este gerador de novo -- este
# gerador so LE relatorio/textos_curados.json, nunca escreve nele.
_CAMINHO_TEXTOS_CURADOS = "relatorio/textos_curados.json"

def _carrega_textos_curados():
    """{seed: texto} de edições humanas já sincronizadas de volta do DOCX de
    curadoria -- arquivo pode não existir ainda (nenhuma curadoria feita),
    nesse caso {} e tudo cai no lorem ipsum determinístico. Escrito por um
    script futuro de sincronização (specs/ajuste_eixos/plan.md Bloco 7), não
    por este gerador -- este gerador só LÊ."""
    p = Path(_CAMINHO_TEXTOS_CURADOS)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

_TEXTOS_CURADOS = _carrega_textos_curados()

def _texto_analise(seed, palavras=None):
    return _TEXTOS_CURADOS.get(seed) or _lorem(seed, palavras)

def pending(titulo, nota):
    """Placeholder for a catalog indicator not yet implemented in analise.py
    (specs/estrutura_eixos.md, status: pendente) -- always labeled with the
    reason, never a silently empty section. Mirrors build_html_report.py's
    emite_bloco_pendente(), adapted to this file's plain-HTML (no CSS
    variable parity needed beyond reusing --note-bg/--note-border)."""
    return f'<h4>{_esc(titulo)}</h4><div class="pending-block"><p><b>\U0001F6A7 Indicador catalogado, ainda não disponível.</b> {_esc(nota)}</p></div>'

# ---------------------------------------------------- appendix table registry --
# Tables that back a chart already shown in the body move here instead of
# sitting inline (specs/ajuste_eixos/plan.md, Bloco 4-B); a small numbered
# registry keeps insertion order == the (newly reorganized) body's reading
# order, since we register each table at the same call site it used to be
# rendered inline.

_apendice = []  # list of (n, titulo, table_html_str)

def registra_tabela(titulo, table_html_str):
    n = len(_apendice) + 1
    _apendice.append((n, titulo, table_html_str))
    return f'<p class="tbl-ref">\U0001F4CE Ver <a href="#tbl-{n}">Tabela {n}</a> no apêndice.</p>'

# ------------------------------------------------------------- page parts --
# Reorganized by eixo da política municipal (specs/estrutura_eixos.md,
# specs/ajuste_eixos/plan.md Bloco 4) instead of by data source. Titles/notes
# under each indicator are transcribed verbatim from analise.py's markdown
# cells (same wording as the pre-reorg version of this file); only the
# grouping/heading nesting changed, plus table extraction to the appendix
# (see registra_tabela above) and new `pending()` placeholders for catalog
# indicators without real data yet.

parts = []
add = parts.append

add('<header class="doc-head">')
add('<h1><span class="glyph">\U0001F3DB️</span>Análise Primeira Infância Carioca</h1>')
add('<p class="sub">Extração, limpeza e visualização dos indicadores de primeira infância (0 a 6 anos) do município do Rio de Janeiro — Censo, CadÚnico, DataSus/Tabnet (nascidos vivos, mortalidade, causas evitáveis, cobertura vacinal) e educação (PNAD/Censo Escolar), organizados por eixo da política municipal.</p>')
add('<div class="meta"><span>Instituto Pereira Passos</span><span id="gen-date">—</span><span>a partir de <code>analise.py</code></span></div>')
add('</header>')

# ---- sumario (pedido do usuario, specs/ajuste_eixos) ----------------------
# Preenchido no fim (ver "full doc" abaixo), depois que todos os h2()/h3()
# ja rodaram e _toc esta completo -- mesmo motivo do placeholder <!--NAVBAR-->
# em build_html_report.py.
add('<div class="toc"><div class="toc-label">SUMÁRIO</div><ul class="toc-list"><!--SUMARIO--></ul></div>')

# ---- introducao: bloco placeholder de 250 palavras (lorem ipsum) ---------
# Nao usa a faixa 100-200 dos blocos de analise por visualizacao do HTML
# (specs.md §7, nao existem la) -- pedido do usuario foi especificamente
# "250 words" fixas para a introducao do relatorio como um todo.
add(h2('Introdução'))
add(p(_lorem("introducao-relatorio-pdf", 250)))

add(p('Para acesso aos dados brutos via Drive: <a href="https://drive.google.com/drive/folders/1xOwf72QfaDuJAHuA-Vngl6t5_kzSfGYX?usp=sharing">pasta compartilhada</a>.<br>OBS: acesso restrito, solicitar a leonardo.aucar@prefeitura.rio'))

# =====================================================================
# 1. Prioridade (sem secundário)
# =====================================================================
add(h2('\U0001F3AF Prioridade (sem secundário)'))

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
add(p(_texto_analise("censo_0_a_4_serie_total_ano")))
df_censo_serie = read("censo_0_a_4_anos_por_ano.csv")
add(registra_tabela("População de 0 a 4 anos, por ano (Censo)", table_html(df_censo_serie[["ano", "0 a 4 anos", "Sexo feminino, 0 a 4 anos", "Sexo masculino, 0 a 4 anos"]], rename={"ano": "Ano"})))
add(chart_block("censo_0_a_4_serie_percentual_ano.png", "censo_0_a_4_anos_por_ano.csv"))
add(p(_texto_analise("censo_0_a_4_serie_percentual_ano")))
add(registra_tabela("Percentual da população de 0 a 4 anos, por ano (Censo)", table_html(df_censo_serie[["ano", "Percentual 0 a 4 anos"]], pct_cols=["Percentual 0 a 4 anos"], rename={"ano": "Ano"})))

add(h3('\U0001F3E5 Nascidos Vivos'))
add(p('Nascidos vivos totais por bairro (2006-2025).'))
add(chart_block("nascidos_vivos_por_ano.png", "nascidos_vivos_por_ano.csv"))
add(p(_texto_analise("nascidos_vivos_por_ano")))
add(registra_tabela("Nascidos vivos por ano", table_html(read("nascidos_vivos_por_ano.csv")[["ano", "nascidos vivos"]], rename={"ano": "Ano"})))

add(h3('\U0001F4C9 Mortalidade'))
add(p('Óbitos até 1 ano de idade: por raça/cor, causas evitáveis, gravidez/puerpério e mortalidade neonatal (precoce, tardia, pós-neonatal e total).'))

RACA_LABEL = {"amarela": "Amarela", "branca": "Branca", "indigena": "Indígena", "parda": "Parda", "preta": "Preta", "nao_informado": "Não informado"}

add(h4('Óbitos até 1 ano por raça/cor'))
add(p('Combina os óbitos de menores de 1 ano (0 a 364 dias) por raça/cor (2006-2025) com os nascidos vivos por raça/cor da mãe (2011-2025), ambos por bairro de residência.'))
add(notes_list([
    'Colunas de ano ausentes nos arquivos do Tabnet indicam total 0 no período e são preenchidas com 0 na limpeza.',
    'As categorias <code>Ignorado</code> e <code>Não informado</code> de nascidos vivos representam a mesma informação ausente, registrada sob nomes diferentes ao longo da série → somadas em <code>nascidos_nao_informado</code>.',
    'O percentual de óbitos por raça só é calculável a partir de 2011, quando começa a série de nascidos vivos por raça/cor da mãe.',
    'Óbitos e nascidos vivos por raça vêm de consultas independentes do Datasus (óbito de residente x nascimento registrado no bairro) → em bairros/anos com poucos casos é possível ter óbitos de uma raça sem nascidos vivos correspondentes, gerando percentuais instáveis ou indefinidos (tratados como NaN). Afeta principalmente <code>indigena</code>, <code>amarela</code> e <code>nao_informado</code>, categorias com poucas observações.',
]))
df_raca = read("mortalidade_raca_municipio_ano.csv")
add(chart_block("obitos_raca_ano.png", "mortalidade_raca_municipio_ano.csv"))
add(p(_texto_analise("obitos_raca_ano")))
obitos_cols = [f"obitos_{r}" for r in RACA_LABEL]
add(registra_tabela("Óbitos até 1 ano por raça/cor, por ano", table_html(df_raca[["ano"] + obitos_cols], rename={"ano": "Ano", **{f"obitos_{r}": lbl for r, lbl in RACA_LABEL.items()}})))
add(chart_block("percentual_mortalidade_raca_ano.png", "mortalidade_raca_municipio_ano.csv"))
add(p(_texto_analise("percentual_mortalidade_raca_ano")))
pct_cols = [f"percentual_{r}" for r in RACA_LABEL]
add(registra_tabela("Percentual de óbitos até 1 ano por raça/cor, por ano", table_html(df_raca[["ano"] + pct_cols], pct_cols=pct_cols, rename={"ano": "Ano", **{f"percentual_{r}": lbl for r, lbl in RACA_LABEL.items()}})))

add(h4('Óbitos por causas evitáveis, por grupo de causa (CID-10)'))
add(p('Usa os arquivos "segundo causas" (não por raça/cor), que classificam cada óbito evitável em uma hierarquia de grupo/subgrupo/causa específica. Soma as três faixas etárias (0-6, 7-27 e 28-364 dias) para obter o total 0-364 dias, no nível de município (1996-2025).'))
add(notes_list([
    'Grupo (<code>1.</code>, <code>2.</code>, <code>3.</code>): nível mais alto da hierarquia. Subgrupo: filhos diretos do grupo <code>1.</code> mais o próprio grupo <code>2.</code> (que não se divide em subgrupos).',
    '<code>3. Demais causas (não claramente evitáveis)</code> não tem subgrupos e por isso só aparece no gráfico de grupo.',
]))
add(chart_block("obitos_causas_evitaveis_grupo_ano.png", "mortalidade_causas_evitaveis_grupo_ano.csv"))
add(p(_texto_analise("obitos_causas_evitaveis_grupo_ano")))
add(registra_tabela("Óbitos por causas evitáveis, por grupo de causa e ano", table_html(read("mortalidade_causas_evitaveis_grupo_ano.csv"), rename={"ano": "Ano"})))
add(chart_block("obitos_causas_evitaveis_subgrupo_ano.png", "mortalidade_causas_evitaveis_subgrupo_ano.csv"))
add(p(_texto_analise("obitos_causas_evitaveis_subgrupo_ano")))
add(registra_tabela("Óbitos por causas evitáveis, por subgrupo de causa e ano", table_html(read("mortalidade_causas_evitaveis_subgrupo_ano.csv"), rename={"ano": "Ano"}, clean_headers=True)))

add(h4('Óbitos por causas evitáveis, por grupo de causa e faixa etária'))
add(p('Mesma classificação de grupo/subgrupo da seção anterior, mas sem somar as três faixas etárias: cada uma (0-6, 7-27 e 28-364 dias) é analisada separadamente.'))

for faixa_id, faixa_titulo in [("0_6", "Precoce (0 a 6 dias)"), ("7_27", "Tardia (7 a 27 dias)"), ("28_364", "Pós-neonatal (28 a 364 dias)")]:
    add(h5(faixa_titulo))
    add(chart_block(f"obitos_causas_evitaveis_grupo_{faixa_id}_ano.png", f"mortalidade_causas_evitaveis_grupo_{faixa_id}_ano.csv"))
    add(p(_texto_analise(f"obitos_causas_evitaveis_grupo_{faixa_id}_ano")))
    add(registra_tabela(f"Óbitos por causas evitáveis, por grupo — {faixa_titulo}", table_html(read(f"mortalidade_causas_evitaveis_grupo_{faixa_id}_ano.csv"), rename={"ano": "Ano"})))
    add(chart_block(f"obitos_causas_evitaveis_subgrupo_{faixa_id}_ano.png", f"mortalidade_causas_evitaveis_subgrupo_{faixa_id}_ano.csv"))
    add(p(_texto_analise(f"obitos_causas_evitaveis_subgrupo_{faixa_id}_ano")))
    add(registra_tabela(f"Óbitos por causas evitáveis, por subgrupo — {faixa_titulo}", table_html(read(f"mortalidade_causas_evitaveis_subgrupo_{faixa_id}_ano.csv"), rename={"ano": "Ano"}, clean_headers=True)))

add(h5('Comparação entre faixas etárias (2025)'))
add(p('Gráfico de barras comparando os subgrupos de causas evitáveis entre as três faixas etárias, no último ano disponível (2025).'))
add(chart_block("obitos_causas_evitaveis_subgrupo_faixa_2025.png", "mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv"))
add(p(_texto_analise("obitos_causas_evitaveis_subgrupo_faixa_2025")))
df_faixa2025 = read("mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv")
df_faixa2025_wide = df_faixa2025.pivot(index="subgrupo", columns="faixa_etaria", values="obitos").reset_index()
ordem_faixa = [c for c in ["0-6 dias", "7-27 dias", "28-364 dias"] if c in df_faixa2025_wide.columns]
df_faixa2025_wide = df_faixa2025_wide[["subgrupo"] + ordem_faixa]
df_faixa2025_wide["subgrupo"] = df_faixa2025_wide["subgrupo"].map(clean_causa)
add(registra_tabela("Óbitos por causas evitáveis, por subgrupo e faixa etária (2025)", table_html(df_faixa2025_wide, rename={"subgrupo": "Subgrupo"})))

add(h4('Primeira infância, por Área Programática de Saúde (CAP)'))
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

add(h5('Panorama municipal, por subgrupo'))
for sufixo, faixa_full, faixa_lbl in _FAIXAS_CAP:
    add(h6(faixa_lbl))
    fname = "obitos_evitaveis_menores_5_subgrupo_ano.png" if sufixo == "menores_5_anos" else f"obitos_evitaveis_{sufixo}_subgrupo_ano.png"
    add(chart_block(fname, "mortalidade_evitaveis_cap_faixa_ano.csv"))
    add(p(_texto_analise(Path(fname).stem)))
    sub = df_cap_faixa[df_cap_faixa["faixa_etaria"] == faixa_full].groupby(["subgrupo", "ano"], as_index=False)["obitos"].sum()
    wide = sub.pivot(index="ano", columns="subgrupo", values="obitos").reset_index()
    add(registra_tabela(f"Óbitos evitáveis por subgrupo, panorama municipal — {faixa_lbl}", table_html(wide, rename={"ano": "Ano"}, clean_headers=True)))

add(h5('Grupo evitável, por CAP'))
for sufixo, faixa_full, faixa_lbl in _FAIXAS_CAP:
    add(p(faixa_lbl))
    if sufixo == "menores_5_anos":
        add(chart_block("obitos_evitaveis_cap_menores_5_anos_ano.png", "mortalidade_evitaveis_grupo_cap_faixa_ano.csv"))
        add(p(_texto_analise("obitos_evitaveis_cap_menores_5_anos_ano")))
    else:
        add(chart_block(f"obitos_evitaveis_cap_{sufixo}_ano.png", "mortalidade_evitaveis_grupo_cap_faixa_ano.csv"))
        add(p(_texto_analise(f"obitos_evitaveis_cap_{sufixo}_ano")))
    add(registra_tabela(f"Óbitos evitáveis (grupo), por CAP — {faixa_lbl}", cap_pivot_table(df_grupo_cap_faixa, "1. Causas evitáveis", faixa_full)))
    add(chart_block(f"percentual_evitaveis_cap_{sufixo}_ano.png", "mortalidade_evitaveis_grupo_cap_faixa_ano.csv"))
    add(p(_texto_analise(f"percentual_evitaveis_cap_{sufixo}_ano")))
    add(registra_tabela(f"% de óbitos evitáveis, por CAP — {faixa_lbl}", cap_pivot_table(df_grupo_cap_faixa, "percentual_evitaveis", faixa_full, fmt_pct=True)))
add(chart_block("obitos_evitaveis_total_cap_ano.png", "mortalidade_evitaveis_grupo_cap_faixa_ano.csv"))
add(p(_texto_analise("obitos_evitaveis_total_cap_ano")))
add(registra_tabela("Óbitos evitáveis totais, por CAP (menores de 5 anos)", cap_pivot_table(df_grupo_cap_faixa, "total", "menores de 5 anos")))

add(h5('Panorama municipal (< 5 anos) e taxa'))
add(chart_block("taxa_mortalidade_evitaveis_menores_5_ano.png", "taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv"))
add(p(_texto_analise("taxa_mortalidade_evitaveis_menores_5_ano")))
add(registra_tabela("Taxa de mortalidade por causas evitáveis, menores de 5 anos", table_html(read("taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv"), dec_cols={"taxa_por_mil": 1}, rename={"ano": "Ano", "obitos": "Óbitos", "nascidos_vivos": "Nascidos vivos", "taxa_por_mil": "Taxa (‰)"})))

add(h4('\U0001F4CB Óbitos gravidez e puerpério'))
add(p('Óbitos maternos durante a gravidez e o puerpério, por bairro de residência (2006-2025).'))
add(chart_block("obitos_gravidez_por_ano.png", "obitos_gravidez_por_ano.csv"))
add(p(_texto_analise("obitos_gravidez_por_ano")))
add(registra_tabela("Óbitos durante a gravidez, por ano", table_html(read("obitos_gravidez_por_ano.csv"), rename={"ano": "Ano"})))
add(chart_block("obitos_puerperio_por_ano.png", "obitos_puerperio_por_ano.csv"))
add(p(_texto_analise("obitos_puerperio_por_ano")))
add(registra_tabela("Óbitos durante o puerpério, por ano", table_html(read("obitos_puerperio_por_ano.csv"), rename={"ano": "Ano"})))

add(h4('\U0001FA7A Mortalidade Neonatal'))
add(p('Óbitos de menores de 1 ano por faixa etária (precoce, tardia, pós-neonatal e total 0-364 dias), com taxa por 1.000 nascidos vivos.'))
add(note('<b>Nota:</b> Precoce e Tardia comparam com os nascidos vivos por <i>inner join</i> (bairros sem óbito registrado em algum lado ficam de fora); Pós-neonatal e Total usam uma grade bairro x ano com zeros explícitos, mais robusta.'))

add(h5('Precoce (0 a 6 dias)'))
add(chart_block("taxa_mortalidade_precoce_ano.png", "mortalidade_neonatal_precoce_por_ano.csv"))
add(p(_texto_analise("taxa_mortalidade_precoce_ano")))
add(registra_tabela("Mortalidade neonatal precoce (0 a 6 dias), por ano", table_html(read("mortalidade_neonatal_precoce_por_ano.csv"), dec_cols={"taxa_mortalidade_precoce": 1}, rename={"ano": "Ano", "obitos precoces": "Óbitos precoces", "nascidos vivos": "Nascidos vivos", "taxa_mortalidade_precoce": "Taxa (‰)"})))

add(h5('Tardia (7 a 27 dias)'))
add(chart_block("taxa_obitos_tardios_ano.png", "mortalidade_neonatal_tardia_por_ano.csv"))
add(p(_texto_analise("taxa_obitos_tardios_ano")))
add(registra_tabela("Mortalidade neonatal tardia (7 a 27 dias), por ano", table_html(read("mortalidade_neonatal_tardia_por_ano.csv"), dec_cols={"taxa_obitos_tardios": 1}, rename={"ano": "Ano", "obitos_tardios": "Óbitos tardios", "nascidos vivos": "Nascidos vivos", "taxa_obitos_tardios": "Taxa (‰)"})))

add(h5('Pós-neonatal (28 a 364 dias)'))
add(p('Não há arquivo pronto para 28-364 dias (total, sem raça): é derivado por subtração <code>0-364 - 0-6 - 7-27</code>, numa grade completa bairro x ano.'))
df_infantil = read("mortalidade_infantil_pos_neonatal_total_por_ano.csv")
add(chart_block("taxa_mortalidade_pos_neonatal_ano.png", "mortalidade_infantil_pos_neonatal_total_por_ano.csv"))
add(p(_texto_analise("taxa_mortalidade_pos_neonatal_ano")))
add(registra_tabela("Mortalidade pós-neonatal (28 a 364 dias), por ano", table_html(df_infantil[["ano", "obitos_28_364", "nascidos_vivos", "taxa_mortalidade_pos_neonatal"]], dec_cols={"taxa_mortalidade_pos_neonatal": 1}, rename={"ano": "Ano", "obitos_28_364": "Óbitos 28-364d", "nascidos_vivos": "Nascidos vivos", "taxa_mortalidade_pos_neonatal": "Taxa (‰)"})))

add(h5('Total (0 a 364 dias)'))
add(chart_block("taxa_mortalidade_infantil_ano.png", "mortalidade_infantil_pos_neonatal_total_por_ano.csv"))
add(p(_texto_analise("taxa_mortalidade_infantil_ano")))
add(registra_tabela("Mortalidade total (0 a 364 dias), por ano", table_html(df_infantil[["ano", "obitos_0_364", "nascidos_vivos", "taxa_mortalidade_infantil"]], dec_cols={"taxa_mortalidade_infantil": 1}, rename={"ano": "Ano", "obitos_0_364": "Óbitos 0-364d", "nascidos_vivos": "Nascidos vivos", "taxa_mortalidade_infantil": "Taxa (‰)"})))

add(h3('\U0001F5FA️ Mapas'))
add(p('Mapas coropléticos por bairro/CAP, gerados a partir das tabelas exportadas para <code>tabelas_finais/</code>.'))

MAP_GROUPS_PRIORIDADE = [
    ("Censo/população", [
        ("mapa_censo_0_4_absoluto.png", "Crianças de 0 a 4 anos, por bairro (Censo 2022)"),
        ("mapa_censo_0_4_percentual.png", "% de crianças de 0 a 4 anos, por bairro (Censo 2022)"),
    ]),
    ("Natalidade", [
        ("mapa_nascidos_vivos_bairro_2025.png", "Nascidos vivos por bairro (2025)"),
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

def emit_map_gallery(groups):
    available_maps = set(os.listdir(MAPAS))
    missing_maps = [fn for _, imgs in groups for fn, _ in imgs if fn not in available_maps]
    if missing_maps:
        raise SystemExit(f"missing map PNGs: {missing_maps}")
    for tema, imgs in groups:
        add(h4(tema))
        add('<div class="map-gallery">')
        for fn, caption in imgs:
            add(map_card(fn, caption))
            add(p(_texto_analise(Path(fn).stem)))
        add('</div>')

emit_map_gallery(MAP_GROUPS_PRIORIDADE)

# =====================================================================
# 2. Inclusão
# =====================================================================
add(h2('\U0001F91D Inclusão'))

add(h3('População 0-6 por idade/raça/sexo (IBGE SIDRA, 2022)'))
add(p('Complementa o Censo por bairro do eixo Prioridade com o detalhe por idade simples (0 a 6 anos) e por raça/sexo, direto das tabelas do IBGE SIDRA (Censo 2022, tabela 9606). Só existe no nível município.'))
add(chart_block("censo_sidra_populacao_0_6_raca_2022.png", "censo_sidra_populacao_0_6_raca_2022.csv"))
add(p(_texto_analise("censo_sidra_populacao_0_6_raca_2022")))
add(chart_block("censo_sidra_populacao_0_6_sexo_2022.png", "censo_sidra_populacao_0_6_sexo_2022.csv"))
add(p(_texto_analise("censo_sidra_populacao_0_6_sexo_2022")))

add(h3('Frequência escolar 0-6 anos (IBGE SIDRA, Censo 2022)'))
add(p('Comparativo mais recente e granular (idade simples, por raça/sexo) que a série PNAD do eixo Família e Cuidados — o Censo é enumeração completa de um único ano (2022), a PNAD Contínua é amostral com série histórica. Não são diretamente comparáveis ano a ano.'))
add(chart_block("sidra_frequencia_escola_0_5_raca_2022.png", "sidra_frequencia_escola_0_5_raca_2022.csv"))
add(p(_texto_analise("sidra_frequencia_escola_0_5_raca_2022")))
add(chart_block("sidra_frequencia_escola_0_5_sexo_2022.png", "sidra_frequencia_escola_0_5_sexo_2022.csv"))
add(p(_texto_analise("sidra_frequencia_escola_0_5_sexo_2022")))
add(chart_block("sidra_taxa_frequencia_0_6_raca_2022.png", "sidra_taxa_frequencia_0_6_raca_2022.csv"))
add(p(_texto_analise("sidra_taxa_frequencia_0_6_raca_2022")))
add(chart_block("sidra_taxa_frequencia_0_6_sexo_2022.png", "sidra_taxa_frequencia_0_6_sexo_2022.csv"))
add(p(_texto_analise("sidra_taxa_frequencia_0_6_sexo_2022")))

add(h3('\U0001F5C2️ CadÚnico'))
add(pending("Famílias no CadÚnico com crianças até 6 anos, por sexo", "Fazer recorte — Léo"))
add(pending("Famílias no CadÚnico com crianças até 6 anos, por raça/cor", "Fazer recorte — Léo"))
add(pending("Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar", "Fazer recorte — Léo"))
add(pending("Crianças no CadÚnico com alguma deficiência", "baixar dados — Léo"))
add(pending("Famílias no CadÚnico com criança com deficiência", "baixar dados — Léo"))
add(pending("Crianças no CadÚnico por tipo de deficiência", "baixar dados — Léo"))

# =====================================================================
# 3. Família e Cuidados
# =====================================================================
add(h2('\U0001F468‍\U0001F469‍\U0001F467 Família e Cuidados'))

add(h3('\U0001F5C2️ Cadúnico'))
add(p('Fonte: CadÚnico via banco CTPE (<code>silver_cadunico_geral</code>), recorte de crianças 0-6 anos.'))
add(note('<b>Nota:</b> requer conexão ativa com o banco CTPE (credenciais em <code>.env</code>) para reproduzir; não roda apenas com os arquivos em <code>dados_locais/</code>. Os gráficos abaixo refletem o último export salvo em <code>tabelas_finais/</code>.'))

add(h4('Análise por renda'))
add('<div class="out-pair">')
add(chart_block("cadunico_familias_por_faixa_renda.png", "cadunico_por_faixa_etaria_2026.csv"))
add(chart_block("cadunico_criancas_por_faixa_renda.png", "cadunico_por_faixa_etaria_2026.csv"))
add('</div>')
# Par compartilha uma unica tabela no apendice (registra_tabela chamado uma
# vez abaixo) -- por isso tambem compartilha UM bloco de texto, com seed
# combinado dos dois stems (specs/ajuste_eixos/specs.md §7). Caso
# PDF-only: nao existe um bookmark equivalente no DOCX de curadoria (que
# ainda trata os dois arquivos separadamente), so este texto combinado.
add(p(_texto_analise("cadunico_familias_por_faixa_renda_cadunico_criancas_por_faixa_renda")))
add(registra_tabela("CadÚnico por faixa de renda", table_html(read("cadunico_por_faixa_etaria_2026.csv"), rename={"faixa de renda": "Faixa de renda"})))

add(h4('Análise por idade'))
add('<div class="out-pair">')
add(chart_block("cadunico_familias_por_idade.png", "cadunico_por_idade_2026.csv"))
add(chart_block("cadunico_criancas_por_idade.png", "cadunico_por_idade_2026.csv"))
add('</div>')
# Mesmo caso do par acima: um bloco de texto compartilhado, PDF-only.
add(p(_texto_analise("cadunico_familias_por_idade_cadunico_criancas_por_idade")))
df_idade = read("cadunico_por_idade_2026.csv")
df_idade["idade"] = df_idade["idade"].astype(int)
add(registra_tabela("CadÚnico por idade", table_html(df_idade, rename={"idade": "Idade"})))

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
add(p(_texto_analise("cobertura_vacinal_epi_comparativo_anos")))
df_vac_comp = read("cobertura_vacinal_epi_comparativo_anos.csv")
df_vac_comp_wide = df_vac_comp.pivot(index="ano", columns="imunobiologico", values="cobertura").reset_index()
vac_comp_cols = [c for c in df_vac_comp_wide.columns if c != "ano"]
add(registra_tabela("Cobertura vacinal, comparativo entre anos", table_html(df_vac_comp_wide, pct_cols=vac_comp_cols, rename={"ano": "Ano"})))

add(h3('\U0001F393 PNAD Contínua e INEP'))
add(h4('Taxa de frequência escolar'))
df_freq = read("frequencia_escolar_pnad_por_idade.csv")
add(chart_block("pnad_frequencia_escolar_por_idade.png", "frequencia_escolar_pnad_por_idade.csv"))
add(p(_texto_analise("pnad_frequencia_escolar_por_idade")))
df_freq["Total"] = df_freq["Total"] * 100  # source column is a 0-1 fraction, not already 0-100
add(registra_tabela("Taxa de frequência escolar (PNAD Contínua), por idade", table_html(df_freq, pct_cols=["Total"], dec_cols={"Total": 1}, rename={"Total": "% frequência"})))

add(h4('Número de matrículas 0 a 6 anos <span style="opacity:.6">(complementar 2021-2025)</span>'))
add(chart_block("matriculas_0_a_6_por_ano.png", "matriculas_0_a_6_por_ano.csv"))
add(p(_texto_analise("matriculas_0_a_6_por_ano")))
add(registra_tabela("Matrículas na educação básica, 0 a 6 anos, por ano", table_html(read("matriculas_0_a_6_por_ano.csv")[["ano", "matriculas"]], rename={"ano": "Ano", "matriculas": "Matrículas"})))
add('<div class="pending-block pending-inline"><p><b>\U0001F6A7 Dado desatualizado.</b> até 2020, necessário tratar microdados posteriores.</p></div>')

add(h3('\U0001F5FA️ Mapas'))
MAP_GROUPS_FAMILIA = [
    ("CadÚnico", [
        ("mapa_cadunico_criancas_bairro_2026.png", "Crianças (0-6 anos) no CadÚnico, por bairro"),
        ("mapa_cadunico_primeira_infancia_bairro_2026.png", "Crianças (0-4 anos) no CadÚnico, por bairro"),
        ("mapa_percentual_cadunico_primeira_infancia_bairro_2026.png", "% de crianças 0-4 anos no CadÚnico sobre o Censo, por bairro"),
    ]),
]
emit_map_gallery(MAP_GROUPS_FAMILIA)

# =====================================================================
# 4. Proteção
# =====================================================================
add(h2('\U0001F6E1️ Proteção'))
add(h3('\U0001F6A7 Indicadores catalogados'))
add(pending("Violência territorial", 'dado catalogado, ainda não importado para `analise.py` (Incorporar no relatório — ver `specs/roadmap.md`, "Educação e Violência")'))
add(pending("Violência familiar (menores de 1 ano, 1 a 5 anos)", "dado catalogado, ainda não importado para `analise.py` (Incorporar no relatório)"))
add(pending("Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos)", "dado catalogado, ainda não importado para `analise.py` (Incorporar no relatório)"))
add(pending("Taxa de notificações de violência (0 a 6 anos)", "dado catalogado, ainda não importado para `analise.py` (Incorporar no relatório)"))
add(pending("Crianças que sofrem violência, por tipificação (sexo e idade)", "dado catalogado, ainda não importado para `analise.py` (Incorporar no relatório)"))

# =====================================================================
# 5. Alimentação
# =====================================================================
add(h2('\U0001F37D️ Alimentação'))

add(h3('\U0001F3E5 Nascidos abaixo peso'))
add(p('Nascidos vivos com baixo peso (&lt;2.500g) por bairro, como percentual dos nascidos vivos totais.'))
add(chart_block("nascidos_abaixo_peso_percentual_por_ano.png", "nascidos_abaixo_peso_por_ano.csv"))
add(p(_texto_analise("nascidos_abaixo_peso_percentual_por_ano")))
df_bp = read("nascidos_abaixo_peso_por_ano.csv")[["ano", "nascidos abaixo peso", "percentual abaixo do peso"]]
add(registra_tabela("Nascidos abaixo do peso, por ano", table_html(df_bp, pct_cols=["percentual abaixo do peso"], rename={"ano": "Ano", "percentual abaixo do peso": "% abaixo do peso"})))

add(h3('\U0001F957 DataSus - SISVAN'))
add(p('Percentual de crianças 0-6 anos com sobrepeso/obesidade e desnutrição, agregado por ano (fonte: SISVAN).'))
add(chart_block("sisvan_desnutricao_percentual_por_ano.png", "sisvan_desnutricao_por_ano.csv"))
add(p(_texto_analise("sisvan_desnutricao_percentual_por_ano")))
add(registra_tabela("Desnutrição SISVAN, por ano", table_html(read("sisvan_desnutricao_por_ano.csv")[["ano", "Percent. baixo peso total"]], pct_cols=["Percent. baixo peso total"], rename={"ano": "Ano"})))
add(chart_block("sisvan_sobrepeso_percentual_por_ano.png", "sisvan_sobrepeso_por_ano.csv"))
add(p(_texto_analise("sisvan_sobrepeso_percentual_por_ano")))
add(registra_tabela("Sobrepeso SISVAN, por ano", table_html(read("sisvan_sobrepeso_por_ano.csv")[["ano", "Percent. sobrepeso total"]], pct_cols=["Percent. sobrepeso total"], rename={"ano": "Ano"})))
add(chart_block("sisvan_obesidade_percentual_por_ano.png", "sisvan_sobrepeso_por_ano.csv"))
add(p(_texto_analise("sisvan_obesidade_percentual_por_ano")))
add(registra_tabela("Obesidade SISVAN, por ano", table_html(read("sisvan_sobrepeso_por_ano.csv")[["ano", "obesidade_percentual"]], pct_cols=["obesidade_percentual"], rename={"ano": "Ano", "obesidade_percentual": "% obesidade"})))

add(h3('\U0001F5FA️ Mapas'))
MAP_GROUPS_ALIMENTACAO = [
    ("Baixo peso ao nascer", [
        ("mapa_nascidos_baixo_peso_bairro_2025.png", "Nascidos com baixo peso por bairro (2025)"),
        ("mapa_percentual_baixo_peso_bairro_2025.png", "% de nascidos com baixo peso por bairro (2025)"),
    ]),
]
emit_map_gallery(MAP_GROUPS_ALIMENTACAO)

# =====================================================================
# 6. Moradia
# =====================================================================
add(h2('\U0001F3E0 Moradia'))
add(h3('\U0001F6A7 Indicadores catalogados'))
add(pending("Crianças no CadÚnico em domicílios com inadequação habitacional", "Posterior"))
add(pending("Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (acima de 3 por dormitório)", "Posterior"))
add(pending("Territórios com risco a inundação e/ou movimento de massa", 'Posterior (Eixo/fonte de dado do catálogo é "Proteção", mas a Política Municipal Prioritária é "Moradia" — entra só aqui, por specs/ajuste_eixos/specs.md §9.2/§4.3)'))
add(pending("Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais)", "Posterior (apenas cad)"))

# =====================================================================
# Apêndice — tabelas de dados (specs/ajuste_eixos/plan.md, Bloco 4-B)
# =====================================================================
add(h2('\U0001F4CE Apêndice — Tabelas de dados'))
add(p('Tabelas de apoio a cada gráfico já exibido no corpo do relatório, na mesma ordem em que os gráficos aparecem.'))
for n, titulo, tbl in _apendice:
    add(f'<h4 id="tbl-{n}">Tabela {n} — {_esc(titulo)}</h4>' + tbl)

footer = '<footer class="doc-foot"><p>Fontes: IBGE (Censo), CTPE/CadÚnico, Datasus/Tabnet (SINASC, SIM), SISVAN, EPI/SVS-Rio, PNAD Contínua e Censo Escolar/INEP. Elaborado a partir do pipeline documentado em <code>analise.py</code> — Instituto Pereira Passos, Prefeitura da Cidade do Rio de Janeiro. Gráficos gerados pelo próprio notebook (matplotlib/seaborn), a partir das tabelas de <code>tabelas_finais/</code>.</p></footer>'

# ------------------------------------------------------------ full doc -----

gen_date = datetime.date.today().strftime("%d de %B de %Y")
MESES = {"January": "janeiro", "February": "fevereiro", "March": "março", "April": "abril", "May": "maio", "June": "junho",
         "July": "julho", "August": "agosto", "September": "setembro", "October": "outubro", "November": "novembro", "December": "dezembro"}
for en, pt in MESES.items():
    gen_date = gen_date.replace(en, pt)

# ---- sumario: agrupa cada h3 sob o h2 mais recente que o precede em _toc,
# mesma logica de build_html_report.py (mantida em sincronia manualmente).
_sumario_grupos = []
for _level, _title, _sid in _toc:
    if _level == 2:
        _sumario_grupos.append([(_title, _sid), []])
    elif _level == 3 and _sumario_grupos:
        _sumario_grupos[-1][1].append((_title, _sid))
sumario_html = "".join(
    f'<li><a href="#{sid}">{_esc(re.sub(r"<[^>]+>", "", title))}</a>'
    + ("<ul>" + "".join(f'<li><a href="#{csid}">{_esc(re.sub(r"<[^>]+>", "", ctitle))}</a></li>' for ctitle, csid in filhos) + "</ul>" if filhos else "")
    + '</li>'
    for (title, sid), filhos in _sumario_grupos
)

body = "\n".join(parts).replace('<span id="gen-date">—</span>', f'<span id="gen-date">Atualizado {gen_date}</span>')
body = body.replace('<!--SUMARIO-->', sumario_html)
body += "\n" + footer

CSS = r"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,440;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
  :root{
    --page:#FFFFFF; --surface:#FFFFFF; --ink:#1A1A1A; --ink-2:#595959; --ink-3:#8C8C8C;
    --hairline:rgba(0,0,0,0.12); --hairline-2:rgba(0,0,0,0.06);
    --note-bg:#F5F5F5; --note-ink:#4D4D4D; --note-border:#B3B3B3;
    --pending-bg:#F2EFE9; --pending-border:#B08D57;
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
  .toc{background:var(--surface); border:1px solid var(--hairline); border-radius:4px; box-shadow:var(--shadow); padding:16px 20px 14px; margin:20px 0 8px;}
  .toc-label{font-family:var(--font-body); font-weight:600; font-size:.72rem; color:var(--ink-3); text-transform:uppercase; letter-spacing:.07em; margin:0 0 10px;}
  ul.toc-list{list-style:none; margin:0; padding:0; columns:2; column-gap:28px;}
  ul.toc-list > li{break-inside:avoid; margin:0 0 8px;}
  ul.toc-list > li > a{font-weight:600; color:var(--ink); text-decoration:none; font-size:.86rem;}
  ul.toc-list ul{list-style:none; margin:4px 0 0; padding:0 0 0 12px; border-left:1px solid var(--hairline-2);}
  ul.toc-list ul li{margin:3px 0;}
  ul.toc-list ul a{color:var(--ink-2); text-decoration:none; font-size:.76rem;}
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
  .pending-block{margin:8px 0 20px; padding:9px 14px; background:var(--pending-bg); border-left:3px solid var(--pending-border); border-radius:0 3px 3px 0; max-width:68ch;}
  .pending-block p{margin:0; font-size:.86rem; color:var(--note-ink); line-height:1.5;}
  .pending-block b{color:var(--ink);}
  .pending-block.pending-inline{margin:8px 0 4px;}
  .tbl-ref{margin:4px 0 18px; font-size:.78rem; color:var(--ink-3);}
  .tbl-ref a{color:var(--ink-3);}
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
    .out, .out-pair > .out, .map-card, .toc{ break-inside:avoid; }
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
