# %% [markdown]
# # 🏛️ Análise Primeira Infância Carioca
#
# Notebook de extração, limpeza e visualização dos indicadores de primeira infância
# (0 a 5 anos, até 72 meses -- faixa padrão do projeto, `specs/2026-09-29_pendencias` D9; a política municipal fala
# em "até 6 anos") do município do Rio de Janeiro: Censo, CadÚnico, DataSus/Tabnet
# (nascidos vivos, mortalidade, causas evitáveis, cobertura vacinal) e educação
# (Censo 2022/SIDRA e Censo Escolar/INEP).

# %% [markdown]
# ---
# ## 📦 Pacotes e Funções Auxiliares
#
# Conexão com o banco e todas as funções de limpeza/wrangling e de visualização reutilizadas ao longo do
# notebook ficam no pacote `primeira_infancia/` (specs/2026-09-28_organizacao), um módulo por tema:
# `conexao` (banco CTPE), `limpeza` (Tabnet/DataSUS, SISVAN, causas evitáveis, SIDRA), `estilo` (paletas,
# fontes, fundo cartográfico), `graficos` (`serie_temporal`, `grafico_barra`, …), `mapas`
# (`mapa_coropletico_bairros`, `agrega_bairros_por_nivel`), `impressao` (variante A4 do relatório PDF,
# `GERA_VARIANTE_A4`), `protecao` (SINAN, violência), `cadunico` (recortes e supressão < 20),
# `populacao` (Ripsa/MS) e `educacao` (Censo Escolar/INEP). As seções abaixo só *chamam* essas funções;
# lógica reutilizável nova vai para o módulo do tema, não para uma célula daqui.

# %%
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pathlib import Path
from matplotlib_scalebar.scalebar import ScaleBar
from shapely.geometry import box
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
import contextily as ctx
import xyzservices
import geopandas as gpd
import pandas as pd
import math
import numpy as np
import os
from matplotlib import font_manager as _fm
from matplotlib.ticker import FuncFormatter as _FuncFormatter, MaxNLocator as _MaxNLocator
from matplotlib.colors import Normalize as _Normalize
from matplotlib.patches import Patch as _Patch
import textwrap as _textwrap
import unicodedata
import csv
import re
import time
import urllib.parse
import requests
import zipfile
from primeira_infancia import *  # noqa: F401,F403

# %% [markdown]
# ### ⚙️ Setup

# %%
#carrega variáveis de ambiente
load_dotenv()

#garante que as pastas de saída padrão existam (inclusive a subpasta de tabelas por bairro)
for pasta in ["tabelas_finais", "visualizacoes", "mapas/tabelas_bairros", "dados_locais/tratados"]:
    Path(pasta).mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ### 🧼 Limpeza de dados prévia

# %%
limpa_dados_sisvan(colunas=['magreza_acentuada','magreza','eutrofia','risco sobrepeso','sobrepeso','obesidade','total'], dataset='sobrepeso')
limpa_dados_sisvan(colunas=['peso_muito_baixo','peso_baixo','peso_adequado','peso_elevado','total'], dataset='desnutrição')
extrai_planilha_evitaveis_cap('dados_locais/mortalidade/obitos_causas_evitaveis_primeira_infancia_cap_2006_2025.xlsx')

# %% [markdown]
# > **Nota de organização:** as seções abaixo seguem a ordem técnica de
# > construção dos dados (fonte de dado, na ordem em que cada tabela é
# > extraída/limpa/agregada) — não a ordem de apresentação final. A
# > apresentação em `relatorio/index.html`, no PDF e no DOCX de curadoria é
# > reorganizada por **eixo da política municipal de primeira infância**,
# > definida em `specs/estrutura_eixos.md` (crosswalk e decisões de projeto em
# > `specs/2026-09-22_ajuste_eixos/specs.md`). Editar esse `.md` e pedir a atualização do
# > relatório não exige reordenar nenhuma célula deste notebook.

# %% [markdown]
# ---
# ## 🧭 Visualização dos Dados (entregáveis dia 12 & 19)

# %% [markdown]
# <p>Para acesso aos dados brutos via Drive: https://drive.google.com/drive/folders/1xOwf72QfaDuJAHuA-Vngl6t5_kzSfGYX?usp=sharing</p>
# <p>OBS: acesso restrito, solicitar a leonardo.aucar@prefeitura.rio</p>

# %% [markdown]
# ### 🏘️ Censo 2022(10/00)

# %% [markdown]
# > **Nota metodológica: população de referência** (`specs/2026-09-24_populacao-referencia`, A5). Vale para todo
# > cálculo do notebook que divide por população.
# >
# > | Nível | Denominador | Anos | Onde é usado |
# > |---|---|---|---|
# > | **Município** | Estimativas **Ripsa/Ministério da Saúde** 2000-2025 (Nota Técnica Ripsa nº 01/2025), idade simples e sexo, população em 1º de julho | um por ano | série de população infantil (abaixo), taxa municipal de violência familiar, razão CadÚnico/população, taxa de atendimento escolar (matrículas) |
# > | **Bairro, AP, RP, RA, CAP** | **Censo 2022** (IBGE/Data.Rio), 0 a 4 anos, referência fixa (decisão B1) | só 2022 | taxas de violência familiar por bairro/RA/CAP, % CadÚnico sobre o Censo por bairro |
# >
# > A Ripsa não tem nível bairro (o menor nível do Tabnet é o município) e não há fonte pública de
# > população por bairro × idade × ano; por isso o Censo 2022 fica abaixo do município, sem estimativa
# > derivada por ano.
# >
# > **Ripsa e Censo 2022 não são comparáveis diretamente.** A Ripsa herda das Projeções do IBGE (revisão
# > 2024) a correção da cobertura incompleta do Censo 2022, que subcontou sobretudo as crianças pequenas:
# >
# > | 2022, Rio de Janeiro | Censo 2022 (SIDRA 9606) | Ripsa 2022 | Diferença |
# > |---|---|---|---|
# > | Total (todas as idades) | 6.211.223 | 6.742.618 | +8,6% |
# > | 0 a 4 anos | 310.648 | 361.163 | +16,3% |
# > | 0 a 5 anos | 379.609 | 439.907 | +15,9% |
# > | Menos de 1 ano | 54.337 | 64.701 | +19,1% |
# >
# > (O Censo por bairro do Data.Rio, usado nos mapas, soma 6.183.971 no total e 310.157 de 0 a 4 anos,
# > um pouco abaixo do SIDRA.) Consequências:
# > 1. **Participações na população calculadas com uma e com outra fonte não se comparam.** A participação
# >    de 0 a 4 anos é 7,6% / 5,8% / 5,0% nos Censos 2000/2010/2022 (tabela 2974 por bairro) e 7,9% / 6,1% /
# >    5,4% na Ripsa. Todo número diz de onde vem.
# > 2. **Taxas sub-municipais com o Censo no denominador tendem a ficar mais altas** do que com uma
# >    estimativa corrigida (denominador subcontado).
# > 3. **A Ripsa é revisada todo ano**, então uma consulta nova pode mudar anos passados. O extrato
# >    versionado `dados_locais/populacao/ripsa_populacao_rio.csv` guarda a data da consulta
# >    (`data_consulta`); `carrega_populacao_ripsa` só consulta o Tabnet se o extrato não cobrir os anos
# >    pedidos.

# %% [markdown]
# Dados do Censo IBGE 2022 (agregados DataRio), população por bairro e faixa etária.

# %% [markdown]
# #### Por bairro

# %%
## dados censo
df_censo = pd.read_csv("dados_locais/censo/pop_censo_2022_datario.csv", encoding='Latin-1', sep=';')
df_censo.head()

# %%
df_censo['Total'] = df_censo[['0 a 4 anos', '5 a 9 anos',
       '10 a 14 anos', '15 a 19 anos', '20 a 24 anos', '25 a 29 anos',
       '30 a 39 anos', '40 a 49 anos', '50 a 59 anos', '60 a 69 anos',
       '70 anos ou mais']].sum(axis=1)

# %%
print(f'Crianças de 0 a 4 anos em 2022: {df_censo['0 a 4 anos'].sum()}')
print(f'Crianças de 5 a 9 anos em 2022: {df_censo['5 a 9 anos'].sum()}')

# %%
df_censo['Percentual 0 a 4'] = (df_censo['0 a 4 anos']/df_censo['Total'])*100
df_censo['Percentual 5 a 9'] = (df_censo['5 a 9 anos']/df_censo['Total'])*100

# %%
df_censo[['bairro','codbairro','0 a 4 anos','Percentual 0 a 4','5 a 9 anos','Percentual 5 a 9']].sort_values(by='0 a 4 anos',ascending=False).to_csv('tabelas_finais/censo_por_bairro.csv')

# %%
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False)
#mapa por total de 0 a 4 anos
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).to_excel('mapas/tabelas_bairros/tabela_mapa_0_4_absoluto.xlsx')

# %%
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).head(10)

# %%
# para bairros 'muito grandes' (+100.000 pessoas)
df_censo.loc[df_censo['Total'] > 20000,['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False)
#mapa por percentual dos bairros grandes
df_censo.loc[df_censo['Total'] > 20000,['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).to_excel('mapas/tabelas_bairros/tabela_mapa_grandes_0_4_percentual.xlsx')

# %%
df_censo.loc[df_censo['Total'] > 20000,['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).head(20)

# %% [markdown]
# #### 👶 População de 0 a 5 anos por idade/raça/sexo (IBGE SIDRA, 2022)
#
# Complementa o Censo por bairro acima com o detalhe por idade simples (0 a 5 anos, faixa padrão do projeto --
# `specs/2026-09-29_pendencias` D9; a tabela 9606 traz também os 6 anos, que ficam de fora) e por
# raça/sexo, direto das tabelas do IBGE SIDRA (Censo 2022, tabela 9606). **Só existe no nível
# município** -- as exportações do SIDRA não trazem recorte por bairro/AP/RP/CAP, então não
# há mapa aqui, só tabelas e gráficos comparativos.

# %%
df_censo_sidra_raca = carrega_sidra_longo('dados_locais//ibge_sidra//Censo//tabela9606_populacao_raca_cor.csv', coluna_corte='Cor ou raça')
df_censo_sidra_sexo = carrega_sidra_longo('dados_locais//ibge_sidra//Censo//tabela9606_populacao_sexo.csv', coluna_corte='Sexo')

fonte_sidra_censo = 'Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606)'

# D9 (specs/2026-09-29_pendencias): 0 a 5 anos; a linha "Total" da 9606 (todas as idades) vira o total de 0 a 5 anos.
# Nomes de arquivo mantidos (`_0_6_`): são chaves do texto curado, do crosswalk e da apresentação
_ORDEM_IDADE_SIDRA_0_5_POP = ['Menos de 1 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos']

def _populacao_sidra_0_a_5(df_longo, coluna_corte):
    tabela = (df_longo[df_longo['idade'].isin(_ORDEM_IDADE_SIDRA_0_5_POP)]
              .pivot(index='idade', columns=coluna_corte, values='valor').reindex(_ORDEM_IDADE_SIDRA_0_5_POP))
    tabela.loc['Total 0 a 5 anos'] = tabela.sum()
    tabela.columns.name = None
    return tabela

_populacao_sidra_0_a_5(df_censo_sidra_raca, 'Cor ou raça').to_csv('tabelas_finais//censo_sidra_populacao_0_6_raca_2022.csv')
_populacao_sidra_0_a_5(df_censo_sidra_sexo, 'Sexo').to_csv('tabelas_finais//censo_sidra_populacao_0_6_sexo_2022.csv')
df_censo_sidra_raca.head()

# %%

grafico_barra_agrupado(
    df_censo_sidra_raca[df_censo_sidra_raca['Cor ou raça'] != 'Total'],
    categoria='idade', valor='valor', agrupador='Cor ou raça',
    titulo='População residente de 0 a 5 anos por idade e raça/cor - Rio de Janeiro (Censo 2022)',
    nome_arquivo='censo_sidra_populacao_0_6_raca_2022', ylabel='Pessoas', legend_title='Raça/cor',
    ordem_categoria=_ORDEM_IDADE_SIDRA_0_5_POP, fonte_dados=fonte_sidra_censo,
)

# %% [markdown]
# <!-- nota-curadoria:censo_sidra_populacao_0_6_raca_2022 -->
# **Nota de curadoria:** Os dados do Censo Demográfico 2022 permitem comparar a composição da população de 0 a 5 anos por raça/cor e idade. Entre menores de 1 ano, foram registrados 26.909 crianças brancas, 21.576 pardas e 5.762 pretas. Aos 5 anos, esses números passam para 29.746, 29.837 e 9.252, respectivamente. A comparação entre as idades permite observar mudanças na distribuição dos grupos de raça/cor ao longo da primeira infância. Os dados também possibilitam relacionar essa composição a outros indicadores do relatório que utilizem raça/cor e idade como dimensões de análise.

# %%
grafico_barra_agrupado(
    df_censo_sidra_sexo[df_censo_sidra_sexo['Sexo'] != 'Total'],
    categoria='idade', valor='valor', agrupador='Sexo',
    titulo='População residente de 0 a 5 anos por idade e sexo - Rio de Janeiro (Censo 2022)',
    nome_arquivo='censo_sidra_populacao_0_6_sexo_2022', ylabel='Pessoas', legend_title='Sexo',
    ordem_categoria=_ORDEM_IDADE_SIDRA_0_5_POP, fonte_dados=fonte_sidra_censo,
)

# %% [markdown]
# <!-- nota-curadoria:censo_sidra_populacao_0_6_sexo_2022 -->
# **Nota de curadoria:** Os dados do Censo Demográfico 2022 permitem detalhar a população de crianças de 0 a 5 anos no município do Rio de Janeiro por idade, raça/cor e sexo. A distribuição por idade possibilita observar a composição desse grupo ao longo dos primeiros anos de vida, enquanto os recortes por raça/cor e sexo ampliam a caracterização demográfica da primeira infância. Os dados são apresentados para o conjunto do município e complementam o recorte territorial de crianças de 0 a 4 anos analisado anteriormente. Essa caracterização é importante para contextualizar os indicadores de saúde, educação, proteção social e demais dimensões analisadas no relatório.

# %% [markdown]
# #### 🗺️ Mapa coroplético (bairros)
#
# Mapas coropléticos de crianças de 0 a 4 anos por bairro (Censo 2022), a partir de
# `tabelas_finais/censo_por_bairro.csv`. O join com a geometria dos bairros usa `codbairro`
# (código oficial IPP/Data.Rio), não o nome do bairro -- mais robusto a variações de grafia
# entre fontes. Limites de bairro em `dados_locais/geo/limite_bairros_rio.geojson`
# (Data.Rio, camada `Cartografia/Limites_administrativos`, geometria simplificada).
# Faixas do mapa absoluto seguem o padrão de `mapas/mapa_referencia.jpeg`, para comparação.
#
# Fundo cartográfico/'desenho' via Esri Ocean Basemap (parâmetro `fundo='mapa'` de
# `mapa_coropletico_bairros`, o padrão da função): relevo suave, mar em azul, sem nomes de
# municípios vizinhos. Os limites estaduais (UF, fonte IBGE,
# `dados_locais/geo/limite_uf_brasil.geojson`) do entorno aparecem em amarelo tracejado, a vista é
# ampliada além dos bairros para dar contexto (região metropolitana, baía, mar), e o mapa traz rosa
# dos ventos e escala gráfica. Exportado a 300 DPI, em formato largo.

# %%
df_mapa_censo = pd.read_csv('tabelas_finais/censo_por_bairro.csv')

fonte_censo = 'Censo Demográfico 2022 (IBGE/Data.Rio)'

mapa_coropletico_bairros(
    df_mapa_censo, coluna_valor='0 a 4 anos',
    titulo='Crianças de 0 a 4 anos de idade, por bairro (Censo 2022)',
    nome_arquivo='mapa_censo_0_4_absoluto',
    cmap=_CORES_TEMA_MAPA['censo'],
    bins=[1000, 2500, 5000, 10000],
    legenda_titulo='Crianças 0-4 anos',
    fonte_dados=fonte_censo,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_censo_0_4_absoluto -->
# **Nota de curadoria:** O mapa apresenta a distribuição da população de 0 a 4 anos por bairro no município do Rio de Janeiro, segundo o Censo Demográfico 2022. Por apresentar números absolutos, o mapa pode ser utilizado para comparar a quantidade de crianças entre os diferentes territórios e dimensionar o tamanho desse grupo em cada bairro. A informação também serve como referência para análises que envolvam outros indicadores da primeira infância, permitindo relacionar a quantidade de crianças de cada território a diferentes características demográficas e sociais.

# %%
mapa_coropletico_bairros(
    df_mapa_censo, coluna_valor='Percentual 0 a 4',
    titulo='Percentual de crianças de 0 a 4 anos, por bairro (Censo 2022)',
    nome_arquivo='mapa_censo_0_4_percentual',
    cmap=_CORES_TEMA_MAPA['censo'],
    legenda_titulo='% da população do bairro',
    fonte_dados=fonte_censo,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_censo_0_4_percentual -->
# **Nota de curadoria:** A participação das crianças de 0 a 4 anos na população total do município diminuiu entre os Censos de 2000, 2010 e 2022. A proporção passou de aproximadamente 7,6% em 2000 para 5,8% em 2010 e 5,0% em 2022. O mapa complementa essa tendência ao mostrar diferenças na participação dessa faixa etária entre os bairros. A análise percentual permite comparar territórios de diferentes tamanhos populacionais, evidenciando o peso relativo das crianças de 0 a 4 anos em cada localidade. Esse indicador contribui para caracterizar a estrutura etária do município e contextualizar as demandas relacionadas à primeira infância.

# %% [markdown]
# #### 🗺️ Versões alternativas: por Área e por Região de Planejamento
#
# Mesmos dados, agregados para os dois níveis de planejamento acima do bairro (`agrega_bairros_por_nivel`
# soma as contagens por bairro; o percentual é recalculado a partir das somas, não pela média das taxas
# por bairro, para não distorcer o resultado entre bairros de tamanhos muito diferentes): as 5 Áreas de
# Planejamento (AP) e as 16 Regiões de Planejamento (RP) do IPP/Data.Rio, ambas já presentes no geojson
# de bairros (`area_plane`, `cod_rp`) e unidas (`dissolve`) por `mapa_coropletico_bairros` via `nivel`.

# %%
# classes discretas por nível -- faixas de valor bem diferentes entre AP (5 regiões grandes) e RP
# (16 regiões menores), então cada nível tem seus próprios limites (não dá pra reaproveitar os do
# bairro); percentuais continuam em escala contínua (não fazem sentido em classes fixas aqui, com só
# 5/16 unidades)
""" niveis_planejamento = {
    'ap': {'nome': 'Área de Planejamento', 'bins': [25000, 50000, 75000, 100000]},
    'rp': {'nome': 'Região de Planejamento', 'bins': [12000, 18000, 24000, 30000]},
}

for nivel, info in niveis_planejamento.items():
    df_censo_nivel = agrega_bairros_por_nivel(df_censo, nivel, colunas_soma=['0 a 4 anos', 'Total'])
    df_censo_nivel['Percentual 0 a 4'] = (df_censo_nivel['0 a 4 anos'] / df_censo_nivel['Total']) * 100

    mapa_coropletico_bairros(
        df_censo_nivel, coluna_valor='0 a 4 anos', nivel=nivel,
        titulo=f'Crianças de 0 a 4 anos de idade, por {info["nome"]} (Censo 2022)',
        nome_arquivo=f'mapa_censo_0_4_absoluto_{nivel}',
        cmap=_CORES_TEMA_MAPA['censo'],
        bins=info['bins'],
        legenda_titulo='Crianças 0-4 anos',
        fonte_dados=fonte_censo,
    )
    mapa_coropletico_bairros(
        df_censo_nivel, coluna_valor='Percentual 0 a 4', nivel=nivel,
        titulo=f'Percentual de crianças de 0 a 4 anos, por {info["nome"]} (Censo 2022)',
        nome_arquivo=f'mapa_censo_0_4_percentual_{nivel}',
        cmap=_CORES_TEMA_MAPA['censo'],
        legenda_titulo='% da população',
        fonte_dados=fonte_censo,
    ) """

# %% [markdown]
# #### Serie temporal censo

# %% [markdown]
# Evolução da população de 0 a 4 anos entre os Censos 2000, 2010 e 2022 (Tabela 2974/IBGE), agregada para o município.

# %%
df_2000 = pd.read_csv('dados_locais/censo/tabela 2974_2000.csv', sep=';')
df_2010 = pd.read_csv('dados_locais/censo/tabela 2974_2010.csv', sep=';')
df_2022 = pd.read_csv('dados_locais/censo/tabela 2974_2022.csv', sep=';')

df_serie_censo = pd.DataFrame()

for df_censo_ano, ano in [[df_2000, '2000'], [df_2010, '2010'], [df_2022, '2022']]:
    df = total_e_percentual_ano(df_censo_ano)
    df['ano'] = ano
    df_serie_censo = pd.concat([df_serie_censo, df], ignore_index=True)

df_serie_censo = (
    df_serie_censo
    .groupby(by='ano')[[
        '0 a 4 anos',
        'Total',
        'Sexo feminino, 0 a 4 anos',
        'Sexo masculino, 0 a 4 anos'
    ]]
    .sum()
)

df_serie_censo['Percentual 0 a 4 anos'] = (
    df_serie_censo['0 a 4 anos'] /
    df_serie_censo['Total']
) * 100

df_serie_censo.to_csv('tabelas_finais//censo_0_a_4_anos_por_ano.csv')

# %%
# gravado como censo_0_a_4_serie_total_ano (antes desenhado à mão e nunca salvo: o arquivo só existia via
# regen_missing_pngs.py, sem fonte -- achado do inventário de fontes, specs/2026-09-25_relatorio_latex Bloco 1)
serie_temporal_multipla(
    df_serie_censo, tempo='ano',
    colunas={'Total': '0 a 4 anos', 'Meninas': 'Sexo feminino, 0 a 4 anos', 'Meninos': 'Sexo masculino, 0 a 4 anos'},
    titulo='Evolução da população de 0 a 4 anos — Censos 2000, 2010 e 2022',
    nome_arquivo='censo_0_a_4_serie_total_ano', ylabel='Crianças de 0 a 4 anos', legend_title='',
    fonte_dados=fonte_censo,
)

# %% [markdown]
# <!-- nota-curadoria:censo_0_a_4_serie_total_ano -->
# **Nota de curadoria:** Os dados do Censo Demográfico 2022 permitem dimensionar a população de crianças de 0 a 4 anos no município e observar sua distribuição territorial. A análise combina a série municipal e o mapa por bairro, permitindo visualizar tanto a magnitude da população infantil quanto sua concentração no território. A leitura dos números absolutos é importante para identificar os bairros que concentram maior quantidade de crianças nessa faixa etária, mas deve considerar as diferenças no tamanho da população de cada bairro. Esse indicador contribui para contextualizar os demais resultados do relatório, especialmente aqueles relacionados à saúde, proteção social e educação na primeira infância.

# %%
serie_temporal(
    df_serie_censo, 'ano', 'Percentual 0 a 4 anos',
    titulo='Percentual da população de 0 a 4 anos — Censos 2000, 2010 e 2022',
    nome_arquivo='censo_0_a_4_serie_percentual_ano', fonte_dados=fonte_censo,
)

# %% [markdown]
# <!-- nota-curadoria:censo_0_a_4_serie_percentual_ano -->
# **Nota de curadoria:** A participação das crianças de 0 a 4 anos na população total do município diminuiu entre os Censos de 2000, 2010 e 2022. A proporção passou de aproximadamente 7,6% em 2000 para 5,8% em 2010 e 5,0% em 2022. O mapa complementa essa tendência ao mostrar diferenças na participação dessa faixa etária entre os bairros. A análise percentual permite comparar territórios de diferentes tamanhos populacionais, evidenciando o peso relativo das crianças de 0 a 4 anos em cada localidade. Esse indicador contribui para caracterizar a estrutura etária do município e contextualizar as demandas relacionadas à primeira infância.

# %% [markdown]
# #### 👶 População de 0 a 5 anos por ano (estimativas Ripsa/MS, 2000-2025)
#
# Série anual da população de 0 a 5 anos do município (idade simples; faixa padrão do projeto desde
# `specs/2026-09-29_pendencias` D9 -- antes a série ia a 6 anos) e a participação de 0 a 5 anos no total da população
# (`specs/2026-09-24_populacao-referencia`, A2). Fonte e ressalvas na nota de população de referência, no início
# desta seção: **os valores não se comparam com os dos Censos acima** (a Ripsa corrige a subcontagem do
# Censo 2022). A participação é recalculada da soma (0 a 5 anos ÷ total), nunca média de anos. Nome do arquivo mantido
# (`populacao_ripsa_0_a_6_*`: chave do crosswalk, do texto curado e da apresentação).

# %%
fonte_ripsa = 'Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025)'

df_ripsa = carrega_populacao_ripsa()
df_pop_infantil = (df_ripsa[(df_ripsa['idade'] != 'total') & (df_ripsa['idade'] != '6')]   # D9: 0 a 5 anos
                   .assign(idade=lambda d: 'populacao_idade_' + d['idade'])
                   .pivot_table(index='ano', columns='idade', values='populacao', aggfunc='sum'))
df_pop_infantil.columns.name = None
df_pop_infantil['populacao_0_a_5'] = populacao_ripsa(df_ripsa, 0, 5).set_index('ano')['populacao']
# 0 a 6 anos só como total, para a nota "a política fala em até 6 anos" da apresentação (D17); fora dos gráficos e tabelas
df_pop_infantil['populacao_0_a_6'] = populacao_ripsa(df_ripsa, 0, 6).set_index('ano')['populacao']
df_pop_infantil['populacao_total'] = populacao_ripsa(df_ripsa, None, None).set_index('ano')['populacao']
df_pop_infantil['percentual_0_a_5'] = df_pop_infantil['populacao_0_a_5'] / df_pop_infantil['populacao_total'] * 100
df_pop_infantil = df_pop_infantil.reset_index()
assert len(df_pop_infantil) == 26 and df_pop_infantil.loc[df_pop_infantil['ano'] == 2025, 'populacao_0_a_5'].item() == 393073
df_pop_infantil.to_csv('tabelas_finais//populacao_ripsa_0_a_6_por_ano.csv', index=False)
df_pop_infantil[['ano', 'populacao_0_a_5', 'populacao_total', 'percentual_0_a_5']]

# %%
serie_temporal(df_pop_infantil, 'ano', 'populacao_0_a_5', 'População de 0 a 5 anos por ano (estimativas Ripsa/MS)',
               nome_arquivo='populacao_ripsa_0_a_6_por_ano', fonte_dados=fonte_ripsa)

# %%
serie_temporal(df_pop_infantil, 'ano', 'percentual_0_a_5', 'Participação de 0 a 5 anos na população total (%, estimativas Ripsa/MS)',
               nome_arquivo='populacao_ripsa_0_a_6_percentual_por_ano', fonte_dados=fonte_ripsa)

# %% [markdown]
# ##### Pendente: Censo 2022 por idade e raça/cor (0 a 6 anos, cidade toda)

# %% [markdown]
# ### 🗂️ Cadúnico

# %% [markdown]
# Fonte: CadÚnico via banco CTPE (`silver_cadunico_geral`), recorte de crianças de 0 a 5 anos (grupo `'0-5'` do CTPE;
# `'0-6'` até a partição de jun/2026). Inclusão e Moradia usam as silvers `silver_cadunico_pessoas`/`_familias`
# (subseção própria no fim, `specs/2026-10-06_cadunico_inclusao_moradia`).
#
# > **Nota:** requer conexão ativa com o banco CTPE (credenciais em `.env`) para reproduzir; não roda apenas com os arquivos em `dados_locais/`.
# > O driver é `psycopg` 3 (`requirements.txt`) -- rode com o kernel/env `analises_env`; o Python base do
# > Anaconda só tem `psycopg2` e falha na conexão.
#
# **O que o grupo `'0-6'` representa (verificado no banco em 2026-09-23, `specs/2026-09-23_recortes_cadunico` S3):**
# crianças nascidas a partir de **2020-08-12**, ou seja, **0 a 5 anos completos** (até 72 meses, o recorte
# de primeira infância do Marco Legal). A `idade` da silver é calculada numa data de referência
# (~2026-08-12) posterior à partição (2026-06-12). **Crianças com 6 anos completos NÃO estão aqui** -- caem
# no grupo `'7-14'` do CTPE. Desde a auditoria de faixas etárias (`specs/2026-09-24_populacao-referencia/auditoria_faixas.md`)
# os títulos abaixo dizem "0 a 5 anos"; antes diziam "0-6", o nome do grupo no CTPE. Comparação entre
# fontes (roadmap item 6); outras fontes do projeto usam outros recortes (Censo 0-4, Sinan 0-5...).
#
# **Filtro de cadastro (S9):** a silver não traz `estado_cadastral`/`ativo` (só a bronze); não se sabe se
# ela já exclui cadastros inativos ou desatualizados -- a confirmar com o CTPE. Vale para todos os números
# CadÚnico do projeto.
#
# **Atualização 2026-10-06 (`specs/2026-10-06_cadunico_inclusao_moradia`, A1):** a silver foi refeita na partição
# **2026-07-10** e o grupo passou a se chamar `'0-5'` (mesmas idades, 0 a 5 completos; nascidos de 2020-07-11 a
# 2026-06-30) -- com o nome antigo a seção lia 0 linhas. O nome vem de `_GRUPO_0_5_CADUNICO`. Sobre S9: a bronze da
# mesma partição só tem cadastros `Cadastrado`/`ativo`, e as silvers têm o mesmo nº de pessoas (2.188.165).
#
# **Privacidade:** toda saída CadÚnico abaixo do nível município passa por `suprime_celulas_pequenas`
# (< 20 famílias vira vazio + coluna `suprimido`) antes de ir para `tabelas_finais/`/mapas.

# %% [markdown]
# #### Recorte 0 a 5 anos (grupo `'0-5'` do CTPE)

# %%
fonte_cadunico = 'CadÚnico (extração CTPE)'

#Banco CTPE
engine = connect_db_ctpe()
# a silver de jul/2026 trocou os rótulos das faixas de renda; normaliza para os códigos de sempre
df_original = normaliza_renda_cadunico(
    pd.read_sql(f"SELECT * FROM silver_cadunico_geral WHERE grupo_idade='{_GRUPO_0_5_CADUNICO}'", engine))
assert len(df_original), f"silver_cadunico_geral sem o grupo {_GRUPO_0_5_CADUNICO!r} (o nome do grupo mudou?)"
df =  df_original.copy()
# recortes_cadunico D5: fonte com o mês da extração (a silver guarda uma única partição)
fonte_cadunico_particao = fonte_cadunico_com_particao(df_original['data_particao'].max())
# nota de rodapé dos mapas CadÚnico por bairro (A2/A4)
# (quebra de linha: numa linha só o rodapé invade a atribuição do basemap no canto inferior esquerdo)
# a nota de proteção de dados (bairros pequenos somados por RA) vem em cada mapa, porque muda entre contagem e taxa
# (specs/2026-09-29_privacidade_cadunico)
fonte_mapa_cadunico = f"{fonte_cadunico_particao}.\nBairro atribuído pelo CEP (Correios), pode divergir do bairro oficial"
df_original

# %%
df = df.rename(columns={'id_pessoa':'Crianças','id_familia':'Famílias','grupo_renda_pct':'faixa de renda'})

# %%
df_bairro = pd.read_csv('dados_locais/lista_bairros.csv', dtype={'cep': str})
df['cep'] = df['cep'].astype(str)

# 2. Faz o JOIN (Merge) trazendo apenas a coluna 'bairros' baseada no 'cep'
df = df.merge(df_bairro[['cep', 'bairro']], on='cep', how='left')

# %% [markdown]
# #### Análise por renda

# %%
#quantitativos por grupo de renda pct
df_renda = df.groupby(by='faixa de renda').agg({'Crianças':'count','Famílias':'nunique'})
df_renda.loc['Total'] = df_renda.sum()
custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
df_renda = df_renda.reindex(custom_order)
# recortes_cadunico A5 (D8): o arquivo se chamava cadunico_por_faixa_etaria_2026.csv, mas o conteúdo é por renda
# recortes_cadunico A7: rótulo descritivo da faixa (renda per capita), sem quebra de linha no CSV
df_renda['faixa de renda (descrição)'] = [_ROTULOS_RENDA_CADUNICO.get(f, f).replace('\n', ' ') for f in df_renda.index]
df_renda.to_csv('tabelas_finais/cadunico_por_faixa_renda_2026.csv')

# %%
df_renda.head(10)

# %%
# recortes_cadunico A7: eixo x com o significado da faixa, não só o intervalo em R$
df_renda_grafico = df_renda.iloc[:-1,:].reset_index()
df_renda_grafico['faixa de renda'] = df_renda_grafico['faixa de renda'].map(_ROTULOS_RENDA_CADUNICO)
grafico_barra(df_renda_grafico,categoria='faixa de renda',valor='Famílias',
              titulo='CADÚNICO: Famílias com crianças de 0 a 5 anos, por faixa de renda per capita',
              nome_arquivo='cadunico_familias_por_faixa_renda', fonte_dados=fonte_cadunico_particao)

# %% [markdown]
# <!-- nota-curadoria:cadunico_familias_por_faixa_renda -->
# **Nota de curadoria:** A partir do dado de famílias com crianças de 0 a 5 anos no CadÚnico é possível observar uma distribuição altamente assimétrica, tendo um predomínio absoluto de famílias com renda até R$218, a linha de pobreza do Bolsa Família, isso evidencia que nesse recorte há uma atuação do CadÚnico predominantemente sobre a parcela populacional em situação de extrema vulnerabilidade. No que diz respeito às rendas mais altas a tendência é diminuindo conforme aumenta-se a renda, chegando a patamares estatisticamente irrelevantes.

# %%
grafico_barra(df_renda_grafico,categoria='faixa de renda',valor='Crianças',
              titulo='CADÚNICO: Crianças de 0 a 5 anos, por faixa de renda per capita',
              nome_arquivo='cadunico_criancas_por_faixa_renda', fonte_dados=fonte_cadunico_particao)

# %% [markdown]
# #### Análise por idade
#
# **Leitura (recortes_cadunico A6):** a coluna `Famílias` conta, em cada idade, as famílias com ao menos
# uma criança daquela idade -- uma família com crianças de 1 e 4 anos aparece nas duas barras, então as
# barras **não somam** o total de famílias (Σ = 191.824 contra 173.768 famílias distintas). E há
# **sub-registro no 1º ano** (11.328 crianças com 0 anos contra 43.187 com 5): o recém-nascido entra no
# cadastro com defasagem, então a barra de 0 anos não é uma estimativa de nascimentos.

# %%
#quantitativos por idade
df #fazer one hot da coluna sexo
df_idade = df.groupby(by='idade').agg({'Crianças':'count','Famílias':'nunique'})#,'sexo_m':'sum','sexo_f':'sum'})
df_idade.to_csv('tabelas_finais/cadunico_por_idade_2026.csv')
df_idade.head(10)


# %%
grafico_barra(df_idade,categoria='idade',valor='Famílias', titulo='CADÚNICO: Famílias com crianças de 0 a 5 anos, por idade',
              nome_arquivo='cadunico_familias_por_idade', fonte_dados=fonte_cadunico_particao)

# %% [markdown]
# <!-- nota-curadoria:cadunico_familias_por_idade -->
# **Nota de curadoria:** No recorte por família com crianças de 0 a 5 anos no CadÚnico, à medida que se avança a idade, aumenta-se a quantidade de família com criança naquela idade que está cadastrada no CadÚnico. Seguindo, notoriamente, o mesmo padrão do gráfico das crianças cadastradas no CadÚnico.

# %%
grafico_barra(df_idade,categoria='idade',valor='Crianças', titulo='CADÚNICO: Crianças de 0 a 5 anos, por idade',
              nome_arquivo='cadunico_criancas_por_idade', fonte_dados=fonte_cadunico_particao)

# %% [markdown]
# <!-- nota-curadoria:cadunico_criancas_por_idade -->
# **Nota de curadoria:** A quantidade de crianças no Cadúnico vai crescendo à medida que a idade vai aumentando. Um total de 11.328 crianças de 0 anos estão no CadÚnico, ao passo que quando se trata de crianças de 5 anos o número salta para 43.187 crianças. É importante frisar que esse dado não pode afirmar que os nascimentos estão diminuindo ou aumentando, haja vista o universo utilizado aqui diz respeito apenas às crianças que estão cadastradas no CadÚnico. Diversos podem ser os motivos para esse movimento: momento de inclusão da família no CadÚnico, atualização cadastral, dentre outros.

# %% [markdown]
# #### Razão municipal: crianças de 0 a 5 anos no CadÚnico sobre a população (Ripsa)
#
# Número-resumo do eixo Inclusão (`specs/2026-09-24_populacao-referencia`, A4): crianças do grupo `'0-5'` do CadÚnico
# (na prática **0 a 5 anos completos**, ver a nota de idade no início da seção) ÷ população de 0 a 5 anos
# do município em 2025 (estimativas Ripsa/MS). Ressalvas:
# - **Um ano de diferença:** o cadastro é da partição de 2026 e a estimativa mais recente da Ripsa é de
#   2025 (1º de julho). Como a população de 0 a 5 anos vem caindo (439.907 em 2022, 393.073 em 2025), a
#   razão com a população de 2026 tende a ser um pouco maior.
# - **Registro administrativo × estimativa:** o numerador conta cadastros (inclusive desatualizados, se a
#   silver não os excluir, S9), e o denominador é uma estimativa demográfica. É uma razão, não a cobertura
#   exata do cadastro.
# - Só no nível município. Por bairro, o % CadÚnico/Censo fica só no notebook (mapa mais abaixo, decisão
#   D6 de `recortes_cadunico`).

# %%
fonte_cadunico_ripsa = f'{fonte_cadunico_particao}; população 0 a 5 anos: estimativas Ripsa/Ministério da Saúde (2025)'

_ano_pop_cadunico = 2025
_pop_0_5 = populacao_ripsa(carrega_populacao_ripsa(), 0, 5, anos=[_ano_pop_cadunico])['populacao'].item()
assert df_original['idade'].between(0, 5).all(), f"grupo {_GRUPO_0_5_CADUNICO!r} do CadÚnico fora de 0 a 5 anos"
df_cadunico_razao = pd.DataFrame([{
    'data_particao': str(pd.Timestamp(df_original['data_particao'].max()).date()),
    'criancas_cadunico_0_a_5': len(df_original),
    'familias_cadunico': df_original['id_familia'].nunique(),
    'ano_populacao': _ano_pop_cadunico,
    'populacao_ripsa_0_a_5': _pop_0_5,
    'razao_percentual': len(df_original) / _pop_0_5 * 100,
}])
df_cadunico_razao.to_csv('tabelas_finais/cadunico_razao_populacao_0_a_5_2026.csv', index=False)
df_cadunico_razao

# %% [markdown]
# #### Análise por bairros

# %%
#quantitativos por grupo de renda pct
df_bairro = df.groupby(by=['bairro']).agg({'Crianças':'count','Famílias':'nunique'})
# recortes_cadunico A1: crianças cujo CEP não está em lista_bairros.csv sumiam do groupby em silêncio
_sem_bairro = df[df['bairro'].isna()]
df_bairro.loc[_ROTULO_SEM_BAIRRO_CADUNICO] = [len(_sem_bairro), _sem_bairro['Famílias'].nunique()]
df_bairro.loc['Total'] = df_bairro.sum()
assert df_bairro.loc['Total', 'Crianças'] == len(df), 'tabela por bairro não fecha com o total de crianças'
#custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
#df_bairro = df_bairro.reindex(custom_order)
# o CSV publicado (`cadunico_por_bairro_2026.csv`) sai mais abaixo, depois da normalização dos nomes: a agregação dos
# bairros pequenos precisa do `codbairro` (specs/2026-09-29_privacidade_cadunico); df_bairro em memória segue completo

# %% [markdown]
# **Nota sobre a atribuição de bairro no CadÚnico** (reescrita em `specs/2026-09-23_recortes_cadunico`, A1/A2):
# o CadÚnico não traz bairro; ele é obtido pelo CEP da família em `dados_locais/lista_bairros.csv`
# (bairro dos **Correios**, não o bairro oficial IPP usado em `df_censo`). Três perdas/distorções:
# 1. **15.809 crianças (8,1% de 194.138) têm CEP fora da lista** e ficam sem bairro -- antes sumiam em
#    silêncio do groupby; agora aparecem na linha "Sem bairro identificado" de `cadunico_por_bairro_2026.csv`.
# 2. Dos nomes que casam, 4 são variações de grafia do mesmo bairro oficial (normalizados via
#    `_ALIAS_BAIRRO_CADUNICO`) e 6 são localidades sem bairro oficial (ex. Dendê, Tubiacanga -- Ilha do
#    Governador), juntos **380 crianças** excluídas só dos mapas.
# 3. **O bairro dos Correios não é o bairro oficial:** bairros-favela ficam subcontados e os vizinhos
#    inflados (Maré 3.405 x Bonsucesso 2.936; Jacarezinho 277 x Jacaré 1.409; Rocinha 1.237 x Gávea
#    1.858), e **Vila Kennedy, Jabour, Gericinó, Ilha de Guaratiba e Lapa não aparecem** (os CEPs caem em
#    Bangu, Senador Camará, Guaratiba e Centro) -- ficam "Sem dado" nos mapas. Corrigir exige
#    geocodificação espacial (pendência F1 da spec).

# %%
_ALIAS_BAIRRO_CADUNICO = {
    'Freguesia (Ilha do Governador)': 'Freguesia (Ilha)',
    'Oswaldo Cruz': 'Osvaldo Cruz',
    'São Cristóvão': 'Imperial de São Cristóvão',
    'Turiaçu': 'Turiaçú',
}
_BAIRROS_CADUNICO_SEM_CORRESPONDENCIA = [
    'Dendê', 'Dumas', 'Guarabu', 'Itacolomi', 'Nossa Senhora das Graças', 'Tubiacanga',
]

# versão com codbairro (via df_censo), sem as linhas 'Total' e 'Sem bairro' -- insumo do mapa por bairro (ver Mapas)
df_bairro_mapa = df_bairro.drop(index=['Total', _ROTULO_SEM_BAIRRO_CADUNICO]).reset_index()
df_bairro_mapa['bairro'] = df_bairro_mapa['bairro'].replace(_ALIAS_BAIRRO_CADUNICO)
df_bairro_mapa = df_bairro_mapa[~df_bairro_mapa['bairro'].isin(_BAIRROS_CADUNICO_SEM_CORRESPONDENCIA)]
df_bairro_mapa = junta_codbairro_por_bairro(df_bairro_mapa, df_censo)
assert df_bairro_mapa['codbairro'].is_unique, 'dois nomes dos Correios caíram no mesmo bairro oficial'

# specs/2026-09-29_privacidade_cadunico D1 (constituição §6): bairro com < 20 crianças ou famílias não é publicado sozinho
# nem fica vazio -- é somado com os outros bairros pequenos da mesma RA ("Demais bairros da RA X"; se ainda < 20, da AP;
# depois do município). A mesma agregação serve à tabela por bairro e à do mapa
df_bairro_mapa_pub = agrega_bairros_pequenos(df_bairro_mapa, ['Crianças', 'Famílias'], ['Crianças', 'Famílias'])
tabela_publicada_por_bairro(df_bairro_mapa_pub, {
    'Localidades sem bairro oficial': df_bairro.loc[df_bairro.index.isin(_BAIRROS_CADUNICO_SEM_CORRESPONDENCIA),
                                                    ['Crianças', 'Famílias']].sum().to_dict(),
    _ROTULO_SEM_BAIRRO_CADUNICO: df_bairro.loc[_ROTULO_SEM_BAIRRO_CADUNICO, ['Crianças', 'Famílias']].to_dict(),
    'Total': df_bairro.loc['Total', ['Crianças', 'Famílias']].to_dict(),
}, ['Crianças', 'Famílias']).to_csv('tabelas_finais/cadunico_por_bairro_2026.csv', index=False)
df_bairro_mapa_pub[df_bairro_mapa_pub['bairro'].str.startswith('Demais')]

# %%
df_bairro.sort_values(by='Crianças', ascending=False).head(10)
# ADICIONAR NOTA SOBRE IDENTIFICACAO DE BAIRROS

# %%
#quantitativos por grupo de renda pct
df_ate_4 = df[df['idade']<5].copy()
df_bairro_ate_4 = df_ate_4.groupby(by=['bairro']).agg({'Crianças':'count','Famílias':'nunique'})
df_bairro_ate_4.loc['Total'] = df_bairro_ate_4.sum()
#custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
#df_bairro = df_bairro.reindex(custom_order)
# CSV publicado (`cadunico_por_bairro_ate_4_2026.csv`): sai com o mapa 0-4, da mesma agregação (privacidade_cadunico)
_sem_bairro_ate_4 = df_ate_4[df_ate_4['bairro'].isna()]
_localidades_ate_4 = df_bairro_ate_4.loc[df_bairro_ate_4.index.isin(_BAIRROS_CADUNICO_SEM_CORRESPONDENCIA)].sum()
# mesma normalização/exclusão de nomes sem correspondência oficial que df_bairro_mapa (nota acima) --
# sem isso, o merge 'right' abaixo já dropava essas linhas em silêncio (nenhum erro, só sumia o dado)
df_bairro_ate_4 = df_bairro_ate_4.rename(index=_ALIAS_BAIRRO_CADUNICO).drop(index=_BAIRROS_CADUNICO_SEM_CORRESPONDENCIA, errors='ignore')
df_bairro_ate_4 = df_bairro_ate_4.merge(df_censo[['bairro','codbairro','0 a 4 anos']], on='bairro', how='right')
df_bairro_ate_4['Primeira Inf. Cadúnico'] = df_bairro_ate_4['Crianças']/df_bairro_ate_4['0 a 4 anos']
df_bairro_ate_4.sort_values(by='Crianças', ascending=False).head(10)

# %%
df_bairro_ate_4.sort_values(by='Primeira Inf. Cadúnico', ascending=True).head(10)

# %%
df_bairro.loc[['Complexo do Alemão']]

# %% [markdown]
# #### 🗺️ Mapas por bairro

# %%
# mapa e gêmea (lida pelo site, que mostra o valor no tooltip) saem da mesma agregação (privacidade_cadunico): os bairros
# somados na RA ficam sem cor no mapa de contagem -- o total do conjunto está nas linhas "Demais bairros" da gêmea
df_bairro_mapa_pub.to_csv('tabelas_finais//tabela_mapa_cadunico_criancas_2026.csv', index=False)
mapa_coropletico_bairros(
    df_bairro_mapa_pub[df_bairro_mapa_pub['codbairro'].notna()], coluna_valor='Crianças',
    titulo='Crianças (0 a 5 anos) no CadÚnico, por bairro',
    nome_arquivo='mapa_cadunico_criancas_bairro_2026', chave='codbairro',
    cmap=_CORES_TEMA_MAPA['cadunico'],
    bins=[250, 750, 1500, 3000], legenda_titulo='Crianças', fonte_dados=fonte_mapa_cadunico + '. Bairros com menos de 20 crianças ou famílias no CadÚnico ficam sem cor: estão somados por Região Administrativa na tabela ("Demais bairros da RA …")',
)

# %% [markdown]
# **Nota (reescrita em `specs/2026-09-23_recortes_cadunico`, A2):** o percentual abaixo passa de 100% em 8 bairros
# (Camorim ~510%, Bonsucesso ~341%, Gávea ~313%, Jacaré ~242%, Anil, Ramos, Gardênia Azul, Cidade de
# Deus). A **causa principal é a atribuição de bairro pelo CEP** (nota da seção de bairros acima): o
# numerador usa o bairro dos Correios e o denominador (Censo 2022) o bairro oficial IPP -- crianças de
# Maré, Jacarezinho e Rocinha são contadas em Bonsucesso, Jacaré e Gávea, que ficam acima de 100%, e as
# favelas ficam abaixo. Diferenças de método (registro administrativo x recenseamento) e de data
# (2026 x 2022) contribuem, mas são secundárias. **Por isso este mapa fica só no notebook** e não entra
# no relatório HTML/PDF (decisão D6) até a geocodificação ser refeita (pendência F1).

# %%
df_ate_4_mapa = df_bairro_ate_4[df_bairro_ate_4['bairro'] != 'Total'].copy()
# coluna só para o mapa -- 'Primeira Inf. Cadúnico' é mantida como razão (sem x100), como já
# usada nas células acima; o mapa segue a convenção do projeto de percentual em escala 0-100
# (mesma de 'Percentual 0 a 4' do Censo)
df_ate_4_mapa['Percentual Primeira Inf. Cadúnico'] = df_ate_4_mapa['Primeira Inf. Cadúnico'] * 100
# privacidade_cadunico D1: bairros com < 20 crianças ou famílias no CadÚnico, ou < 20 crianças de 0 a 4 no Censo
# (denominador), somados por RA -> AP -> município; bairro sem nenhuma criança no CadÚnico conta como 0
df_ate_4_mapa[['Crianças', 'Famílias']] = df_ate_4_mapa[['Crianças', 'Famílias']].fillna(0)
df_ate_4_mapa = agrega_bairros_pequenos(
    df_ate_4_mapa.drop(columns=['Primeira Inf. Cadúnico', 'Percentual Primeira Inf. Cadúnico']),
    ['Crianças', 'Famílias', '0 a 4 anos'], ['Crianças', 'Famílias', '0 a 4 anos'],
    taxas={'Primeira Inf. Cadúnico': ('Crianças', '0 a 4 anos', 1),
           'Percentual Primeira Inf. Cadúnico': ('Crianças', '0 a 4 anos', 100)})
df_ate_4_mapa.to_csv('tabelas_finais//tabela_mapa_cadunico_criancas_0_a_4_2026.csv', index=False)
tabela_publicada_por_bairro(df_ate_4_mapa[['bairro', 'codbairro', 'Crianças', 'Famílias', 'agregado_em', 'suprimido',
                                           'bairros agregados']], {
    'Localidades sem bairro oficial': _localidades_ate_4[['Crianças', 'Famílias']].to_dict(),
    _ROTULO_SEM_BAIRRO_CADUNICO: {'Crianças': len(_sem_bairro_ate_4), 'Famílias': _sem_bairro_ate_4['Famílias'].nunique()},
    'Total': {'Crianças': len(df_ate_4), 'Famílias': df_ate_4['Famílias'].nunique()},
}, ['Crianças', 'Famílias']).to_csv('tabelas_finais/cadunico_por_bairro_ate_4_2026.csv', index=False)

mapa_coropletico_bairros(
    df_ate_4_mapa[df_ate_4_mapa['codbairro'].notna()], coluna_valor='Crianças', titulo='Crianças (0-4 anos) no CadÚnico, por bairro',
    nome_arquivo='mapa_cadunico_criancas_0_a_4_bairro_2026', chave='codbairro',
    cmap=_CORES_TEMA_MAPA['cadunico'],
    bins=[200, 500, 1000, 2000], legenda_titulo='Crianças', fonte_dados=fonte_mapa_cadunico + '. Bairros com menos de 20 crianças ou famílias no CadÚnico ficam sem cor: estão somados por Região Administrativa na tabela ("Demais bairros da RA …")',
)
mapa_coropletico_bairros(
    df_ate_4_mapa[df_ate_4_mapa['codbairro'].notna()], coluna_valor='Percentual Primeira Inf. Cadúnico', titulo='% de crianças 0-4 anos no CadÚnico sobre a população 0-4 do Censo 2022, por bairro',
    nome_arquivo='mapa_percentual_cadunico_0_a_4_sobre_censo_bairro_2026', chave='codbairro',
    cmap=_CORES_TEMA_MAPA['cadunico'],
    legenda_titulo='% CadÚnico/Censo 2022', fonte_dados=fonte_mapa_cadunico + '; população 0 a 4 anos: Censo 2022 (IBGE/Data.Rio)'
                                                  + '. Bairros com menos de 20 casos (no grupo, no complemento ou no total) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa',
)

# %% [markdown]
# <!-- nota-curadoria:mapa_cadunico_criancas_0_a_4_bairro_2026 -->
# **Nota de curadoria:** Olhando para a distribuição espacial, pode-se observar que a maior concentração tanto de crianças de 0 a 5 quanto de 0 a 4 anos no CadÚnico está presente nas Zonas Oeste e Norte da cidade. Há alterações absolutas nos intervalos de distribuição quando se olha para os dois mapas, mas o padrão de distribuição geográfica segue praticamente o mesmo. Nos dois mapas, a Zona Oeste apresenta a maior concentração de crianças cadastradas. Já a Zona Sul e parte da extensão litorânea da Barra da Tijuca/Recreio apresentam menores quantitativos. Na Zona Norte e no Centro apresentam-se uma maior fragmentação por terem muitos bairros, favelas e comunidades.

# %% [markdown]
# #### 👨‍👩‍👧 Recortes por família: sexo, raça/cor, arranjo familiar e renda
#
# Indicadores do eixo **Inclusão** (`specs/estrutura_eixos.md`; spec `specs/2026-09-23_recortes_cadunico`). "Crianças
# até 6 anos" é a redação do catálogo (mantida nos subtítulos de `estrutura_eixos.md`, decisão C-D2 de
# `populacao-referencia`); o dado é de **0 a 5 anos completos**, e é isso que os títulos dos gráficos e mapas
# dizem (ver a nota de idade no início da seção). Sexo e raça/cor são atributos **da criança** (D1): uma família com um menino e uma
# menina tem as duas categorias. O arranjo familiar é aproximado pela composição do cadastro (D2), porque
# a silver não tem parentesco com o responsável familiar -- por isso esta célula também lê os adultos das
# famílias, não só as crianças.

# %%
df_membros_cadunico = carrega_cadunico_familias_0_6(engine)
df_familias = classifica_arranjo_familiar(df_membros_cadunico, idade_adulto=18)  # D3: adulto = 18+
# fecha com o recorte de crianças da seção (mesma partição, mesmas famílias)
assert len(df_familias) == df['Famílias'].nunique(), 'nº de famílias diverge do recorte de crianças'
assert df_familias['n_criancas'].sum() == len(df), 'nº de crianças diverge do recorte de crianças'
print(f"{_numero_ptbr(len(df_familias))} famílias, {_numero_ptbr(df_familias['n_criancas'].sum())} crianças, "
      f"{_numero_ptbr(len(df_membros_cadunico))} pessoas no total")

# %% [markdown]
# ##### Por sexo
#
# Duas leituras na mesma tabela: **crianças** por sexo, e **famílias** pela composição de sexo das
# crianças (só meninas / só meninos / meninas e meninos) -- categorias exclusivas, que somam o total de
# famílias. Contar "famílias com ao menos uma menina" e "com ao menos um menino" contaria duas vezes as
# famílias com crianças dos dois sexos.

# %%
df_sexo_criancas = agrega_cadunico_criancas(df, 'sexo', ['Feminino', 'Masculino'])
df_sexo_familias = agrega_cadunico_familias(df_familias, 'composicao_sexo_criancas', _ORDEM_COMPOSICAO_SEXO)
tabela_sexo = pd.concat({'Crianças por sexo': df_sexo_criancas,
                         'Famílias por sexo das crianças': df_sexo_familias}, names=['recorte', 'categoria'])
tabela_sexo = tabela_sexo.astype({c: 'Int64' for c in tabela_sexo.columns if not c.startswith('%')})
tabela_sexo.to_csv('tabelas_finais/cadunico_por_sexo_2026.csv')
tabela_sexo

# %%
grafico_barra(df_sexo_criancas.drop(index='Total (famílias não somam)').rename_axis('sexo da criança').reset_index(),
              categoria='sexo da criança', valor='Crianças',
              titulo='CADÚNICO: Crianças de 0 a 5 anos, por sexo',
              nome_arquivo='cadunico_criancas_por_sexo', fonte_dados=fonte_cadunico_particao)

# %%
grafico_barra(df_sexo_familias.drop(index='Total').rename_axis('sexo das crianças da família').reset_index(),
              categoria='sexo das crianças da família', valor='Famílias',
              titulo='CADÚNICO: Famílias com crianças de 0 a 5 anos, por sexo das crianças',
              nome_arquivo='cadunico_familias_por_sexo_criancas', fonte_dados=fonte_cadunico_particao)

# %% [markdown]
# ##### Por raça/cor
#
# As 5 categorias do CadÚnico, mais o agregado **negra = preta + parda** (convenção IBGE). A coluna de
# famílias conta as famílias com **ao menos uma** criança da categoria -- não somam entre linhas (famílias
# com crianças de raça/cor diferentes aparecem em mais de uma). Amarela e indígena são grupos pequenos na
# cidade (1.208 e 69 crianças) e **nunca aparecem abaixo do nível município** (privacidade, spec §5); por
# bairro só se publica o % de crianças negras.

# %%
df_raca = agrega_cadunico_criancas(df, 'raca_cor', _ORDEM_RACA_CADUNICO)
_negras = df[df['raca_cor'].isin(['Preta', 'Parda'])]
df_raca.loc['Negra (preta + parda)'] = [len(_negras), _negras['Famílias'].nunique(), round(len(_negras) / len(df) * 100, 1)]
df_raca = df_raca.reindex(_ORDEM_RACA_CADUNICO + ['Negra (preta + parda)', 'Total (famílias não somam)'])
df_raca = df_raca.astype({'Crianças': int, 'Famílias com ao menos uma': int}).rename_axis('raça/cor da criança')
df_raca['nota'] = 'famílias não exclusivas entre categorias; não somar'
df_raca.to_csv('tabelas_finais/cadunico_por_raca_cor_2026.csv')
df_raca

# %%
df_raca_grafico = df_raca.loc[_ORDEM_RACA_CADUNICO].reset_index()
grafico_barra(df_raca_grafico, categoria='raça/cor da criança', valor='Crianças',
              titulo='CADÚNICO: Crianças de 0 a 5 anos, por raça/cor',
              nome_arquivo='cadunico_criancas_por_raca_cor', fonte_dados=fonte_cadunico_particao)

# %%
grafico_barra(df_raca_grafico, categoria='raça/cor da criança', valor='Famílias com ao menos uma',
              titulo='CADÚNICO: Famílias com ao menos uma criança de 0 a 5 anos de cada raça/cor',
              nome_arquivo='cadunico_familias_por_raca_cor', fonte_dados=fonte_cadunico_particao)

# %% [markdown]
# ##### Por arranjo familiar e renda
#
# **Arranjo familiar (aproximado):** membros de 18 anos ou mais da família, por sexo. **"Uma adulta
# (mulher)" não é o conceito de família monoparental do MDS**, que depende do parentesco com o responsável
# familiar (campo ausente na extração -- pendência F2). Um companheiro que não está no cadastro não aparece;
# a sub-declaração de cônjuges é um viés conhecido do CadÚnico (reforçado pela regra de renda per capita)
# e provavelmente infla essa categoria. O cadastro de cada família está completo (nº de pessoas na tabela =
# `n_pessoas_familia`, conferido em `classifica_arranjo_familiar`).
#
# **Renda:** faixa de renda per capita da família (`grupo_renda_pct`). No cruzamento com o arranjo, as
# faixas acima de 1/2 salário mínimo se juntam numa só, para não gerar células pequenas; células com menos
# de 20 famílias seriam suprimidas.

# %%
df_arranjo = agrega_cadunico_familias(df_familias, 'arranjo', _ORDEM_ARRANJO_CADUNICO).rename_axis('arranjo familiar')
df_arranjo.to_csv('tabelas_finais/cadunico_familias_por_arranjo_2026.csv')
df_arranjo

# %%
# famílias sem nenhum membro de 18+: inspeção só em agregado (idade do membro mais velho)
df_familias.loc[df_familias['arranjo'] == 'Sem adulto (18+)', 'idade_mais_velho'].value_counts().sort_index()

# %% [markdown]
# **Famílias sem adulto (713, partição jun/2026):** em 554 o membro mais velho tem 16 ou 17 anos -- responsável
# familiar adolescente, permitido pelo CadÚnico a partir de 16 anos. Em 85 o membro mais velho tem até 5 anos
# (cadastro só com a criança), o que indica cadastro incompleto ou inconsistente. As 713 ficam como categoria
# própria, sem descarte; são 0,4% das famílias.

# %%
_renda_3 = df_familias['grupo_renda_pct'].map(_RENDA_CADUNICO_3_FAIXAS)
df_arranjo_renda = (df_familias.assign(renda=_renda_3).groupby(['arranjo', 'renda']).size()
                    .rename('Famílias').reset_index())
assert df_arranjo_renda['Famílias'].sum() == len(df_familias)
df_arranjo_renda['% no arranjo'] = (df_arranjo_renda['Famílias'] /
                                    df_arranjo_renda.groupby('arranjo')['Famílias'].transform('sum') * 100).round(1)
df_arranjo_renda['arranjo'] = pd.Categorical(df_arranjo_renda['arranjo'], _ORDEM_ARRANJO_CADUNICO, ordered=True)
df_arranjo_renda['faixa de renda per capita'] = df_arranjo_renda['renda'].map(_ROTULOS_RENDA_CADUNICO_3).str.replace('\n', ' ')
df_arranjo_renda = df_arranjo_renda.sort_values(['arranjo', 'renda']).drop(columns='renda')
# nível município, mas a regra de célula pequena vale igual (spec §5)
df_arranjo_renda_pub = suprime_celulas_pequenas(df_arranjo_renda, 'Famílias', ['Famílias', '% no arranjo'])
df_arranjo_renda_pub.to_csv('tabelas_finais/cadunico_familias_arranjo_renda_2026.csv', index=False)
df_arranjo_renda_pub

# %%
# rótulos do eixo x em 2 linhas (os nomes de arranjo são longos)
_rotulo_arranjo = {a: a.replace(' (', '\n(') for a in _ORDEM_ARRANJO_CADUNICO}
grafico_barra(df_arranjo.drop(index='Total').rename(index=_rotulo_arranjo).reset_index(),
              categoria='arranjo familiar', valor='Famílias',
              titulo='CADÚNICO: Famílias com crianças de 0 a 5 anos, por arranjo familiar',
              nome_arquivo='cadunico_familias_por_arranjo', fonte_dados=fonte_cadunico_particao)

# %%
_graf_arranjo_renda = df_arranjo_renda_pub.assign(arranjo=df_arranjo_renda_pub['arranjo'].astype(str).map(_rotulo_arranjo))
grafico_barra_agrupado(_graf_arranjo_renda, categoria='arranjo', valor='% no arranjo', agrupador='faixa de renda per capita',
                       titulo='CADÚNICO: Renda per capita das famílias com crianças de 0 a 5 anos, por arranjo familiar',
                       nome_arquivo='cadunico_familias_arranjo_renda', ylabel='% das famílias do arranjo',
                       legend_title='Renda per capita', ordem_categoria=list(_rotulo_arranjo.values()), rotacao_x=0,
                       fonte_dados=fonte_cadunico_particao)

# %% [markdown]
# ##### 🗺️ Mapas por bairro: % de crianças negras e de famílias com uma só adulta
#
# Taxas **internas ao CadÚnico** (numerador e denominador da mesma base e do mesmo bairro atribuído pelo
# CEP), recalculadas a partir das contagens absolutas de cada bairro -- sofrem bem menos com o viés de
# CEP -> bairro do que a razão CadÚnico/Censo, mas o bairro continua sendo o dos Correios (nota acima). Mesma
# normalização de nomes e join por `codbairro` de `df_bairro_mapa`. Bairros com menos de 20 famílias no
# CadÚnico ficam sem cor (supressão, spec §5); escala contínua (convenção de taxas).

# %%
_fam_bairro = atribui_bairro_por_cep(df_familias)
df_recortes_bairro = pd.concat([
    df.groupby('bairro').agg(**{'Crianças': ('Crianças', 'count'),
                                'Meninas': ('sexo', lambda s: (s == 'Feminino').sum()),
                                'Crianças negras': ('raca_cor', lambda s: s.isin(['Preta', 'Parda']).sum())}),
    _fam_bairro.groupby('bairro').agg(**{'Famílias': ('id_familia', 'count'),
                                         'Famílias com uma adulta': ('arranjo', lambda s: (s == 'Uma adulta (mulher)').sum())}),
], axis=1).fillna(0).astype(int).reset_index()
df_recortes_bairro['bairro'] = df_recortes_bairro['bairro'].replace(_ALIAS_BAIRRO_CADUNICO)
df_recortes_bairro = df_recortes_bairro[~df_recortes_bairro['bairro'].isin(_BAIRROS_CADUNICO_SEM_CORRESPONDENCIA)]
df_recortes_bairro = junta_codbairro_por_bairro(df_recortes_bairro, df_censo)
# privacidade_cadunico D1/D2: o percentual publicado × o total publicado devolveria a contagem -- então o bairro entra no
# conjunto da RA também quando o numerador OU o complemento (total - numerador) é < 20. Taxas sempre dos absolutos
# (nunca média de percentuais), recalculadas das somas nos conjuntos
df_recortes_bairro_pub = agrega_bairros_pequenos(
    df_recortes_bairro, ['Crianças', 'Meninas', 'Crianças negras', 'Famílias', 'Famílias com uma adulta'],
    ['Crianças', 'Famílias'],
    pares=[('Meninas', 'Crianças'), ('Crianças negras', 'Crianças'), ('Famílias com uma adulta', 'Famílias')],
    taxas={'% meninas': ('Meninas', 'Crianças', 100), '% crianças negras': ('Crianças negras', 'Crianças', 100),
           '% famílias com uma adulta': ('Famílias com uma adulta', 'Famílias', 100)})
df_recortes_bairro_pub.to_csv('tabelas_finais/tabela_mapa_cadunico_recortes_bairro_2026.csv', index=False)
df_recortes_bairro_pub.sort_values('% famílias com uma adulta', ascending=False).head(10)

# %%
# mapa de % meninas cortado na revisão visual (recortes_cadunico T12.3): ~49% em todo bairro, sem
# informação territorial -- a coluna segue na tabela gêmea
for _coluna, _titulo, _arquivo, _legenda in [
    ('% crianças negras', '% de crianças negras (pretas e pardas) de 0 a 5 anos no CadÚnico, por bairro',
     'mapa_percentual_cadunico_criancas_negras_bairro_2026', '% negras'),
    ('% famílias com uma adulta', 'Famílias com crianças de 0 a 5 anos no CadÚnico: % com uma só adulta, por bairro',
     'mapa_percentual_cadunico_familias_uma_adulta_bairro_2026', '% uma adulta'),
]:
    mapa_coropletico_bairros(
        df_recortes_bairro_pub[df_recortes_bairro_pub['codbairro'].notna()], coluna_valor=_coluna, titulo=_titulo,
        nome_arquivo=_arquivo, chave='codbairro',
        cmap=_CORES_TEMA_MAPA['cadunico'], legenda_titulo=_legenda, fonte_dados=fonte_mapa_cadunico + '. Bairros com menos de 20 casos (no grupo, no complemento ou no total) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa',
    )

# %% [markdown]
# #### ♿🏠 Inclusão e Moradia (silvers de pessoas e famílias, jul/2026)
#
# Eixos **Inclusão** e **Moradia** (`specs/2026-10-06_cadunico_inclusao_moradia`): as silvers novas do CTPE
# (`silver_cadunico_pessoas` e `silver_cadunico_familias`, partição 2026-07-10) trazem deficiência (com o tipo), BPC por
# deficiência e as variáveis de domicílio já classificadas pela metodologia da **Fundação João Pinheiro** (déficit e
# inadequação habitacional, com os componentes) e o adensamento excessivo. Substituem no site o dado pontual de
# ago/2026 (D1; a célula seguinte fica, mas sai do site).
#
# - **Unidade:** crianças de 0 a 5 anos (`faixa_etaria = '0-5'`) e famílias com ao menos uma delas; o domicílio é o da
#   família da criança (D6).
# - **Percentuais** sempre de absolutos, com "Não informado"/"Não se aplica" fora da base (D7); a base sai na tabela.
#   "Não se aplica" na inadequação = domicílio improvisado ou coletivo, que a FJP conta no déficit.
# - **BPC** é atributo da família (`familia_bpc_deficiente`, A3): publicado como famílias com criança com deficiência
#   que recebem BPC por deficiência (de qualquer membro); sem informação fica fora do percentual.
# - **Bairro:** ponte CEP → código oficial do banco (`dim_bridge_ceps_bairros`, D2), join por `codbairro`. Cobre ~90%
#   das crianças; as demais ficam só no total do município. As saídas CadÚnico acima seguem com `lista_bairros.csv`.
# - **Privacidade:** por bairro, `agrega_bairros_pequenos` com o par (casos, base) -- casos e complemento ≥ 20.
# - Totais do município conferidos com `gold_cadunico_indicadores` (recorte `primeira_infancia`) na implementação.

# %%
df_criancas_silver = carrega_criancas_cadunico_silver(engine)
fonte_cadunico_silver = fonte_cadunico_com_particao(df_criancas_silver['data_particao'].max())
# rodapé dos mapas desta subseção: bairro pela ponte do banco (oficial), não pelos Correios como em fonte_mapa_cadunico
# (quebras de linha: numa linha só o rodapé invade a atribuição do basemap)
fonte_mapa_cadunico_silver = (f"{fonte_cadunico_silver}. Bairro pelo CEP da família (correspondência CEP-bairro do CTPE)."
                              "\nBairros com menos de 20 casos (no grupo, no complemento ou na base) mostram a taxa"
                              "\ndo conjunto dos bairros pequenos da sua Região Administrativa")
assert len(df_criancas_silver) == len(df_original), 'silver de pessoas e silver geral divergem no nº de crianças de 0 a 5'
print(f"{_numero_ptbr(len(df_criancas_silver))} crianças, {_numero_ptbr(df_criancas_silver['id_familia'].nunique())} famílias; "
      f"{df_criancas_silver['codbairro'].notna().mean():.1%} com bairro pela ponte")

# %% [markdown]
# ##### Inclusão: crianças com deficiência, tipo e BPC

# %%
df_deficiencia_criancas, df_deficiencia_familias = tabela_deficiencia_cadunico(df_criancas_silver)
df_tipos_deficiencia = tabela_tipos_deficiencia_cadunico(df_criancas_silver)
df_deficiencia_criancas.to_csv('tabelas_finais/cadunico_deficiencia_criancas_0_a_5_2026.csv', index=False)
df_deficiencia_familias.to_csv('tabelas_finais/cadunico_deficiencia_familias_0_a_5_2026.csv', index=False)
df_tipos_deficiencia.to_csv('tabelas_finais/cadunico_tipos_deficiencia_0_a_5_2026.csv', index=False)
print(df_deficiencia_criancas.to_string(index=False), df_deficiencia_familias.to_string(index=False), sep="\n\n")
df_tipos_deficiencia

# %%
# tipos não exclusivos (uma criança pode ter mais de um): as barras não somam o total de crianças com deficiência
grafico_barra(df_tipos_deficiencia.assign(**{'Tipo de deficiência': df_tipos_deficiencia['Tipo de deficiência'].str.replace(' ', '\n', n=1)}),
              categoria='Tipo de deficiência', valor='Crianças',
              titulo='CADÚNICO: Crianças de 0 a 5 anos com deficiência, por tipo',
              nome_arquivo='cadunico_criancas_por_tipo_deficiencia',
              fonte_dados=fonte_cadunico_silver + '. Uma criança pode ter mais de um tipo: as barras não somam')

# %%
_def_bairro = por_bairro_sim_base(df_criancas_silver, 'tem_deficiencia', 'Crianças com deficiência')
df_deficiencia_bairro_pub = agrega_bairros_pequenos(
    _def_bairro, ['Crianças', 'Crianças com deficiência', 'Base (Crianças com deficiência)'], ['Crianças'],
    pares=[('Crianças com deficiência', 'Base (Crianças com deficiência)')],
    taxas={'% crianças com deficiência': ('Crianças com deficiência', 'Base (Crianças com deficiência)', 100)})
df_deficiencia_bairro_pub.to_csv('tabelas_finais/tabela_mapa_cadunico_deficiencia_bairro_2026.csv', index=False)
mapa_coropletico_bairros(
    df_deficiencia_bairro_pub[df_deficiencia_bairro_pub['codbairro'].notna()], coluna_valor='% crianças com deficiência',
    titulo='% de crianças de 0 a 5 anos com deficiência no CadÚnico, por bairro',
    nome_arquivo='mapa_percentual_cadunico_criancas_deficiencia_bairro_2026', chave='codbairro',
    cmap=_CORES_TEMA_MAPA['cadunico'], legenda_titulo='% com deficiência', fonte_dados=fonte_mapa_cadunico_silver)

# %% [markdown]
# ##### Moradia: inadequação, déficit e adensamento (FJP)

# %%
df_moradia_resumo = tabela_moradia_cadunico(df_criancas_silver)
df_inadequacao_componentes = tabela_componentes_fjp(df_criancas_silver, _COMPONENTES_INADEQUACAO_FJP)
df_deficit_componentes = tabela_componentes_fjp(df_criancas_silver, _COMPONENTES_DEFICIT_FJP)
df_moradia_resumo.to_csv('tabelas_finais/cadunico_moradia_resumo_0_a_5_2026.csv', index=False)
df_inadequacao_componentes.to_csv('tabelas_finais/cadunico_inadequacao_componentes_0_a_5_2026.csv', index=False)
df_deficit_componentes.to_csv('tabelas_finais/cadunico_deficit_componentes_0_a_5_2026.csv', index=False)
print(df_moradia_resumo.to_string(index=False), df_inadequacao_componentes.to_string(index=False), sep="\n\n")
df_deficit_componentes

# %%
grafico_barra(df_inadequacao_componentes.assign(Componente=df_inadequacao_componentes['Componente'].str.replace(' ', '\n', n=1)),
              categoria='Componente', valor='Crianças',
              titulo='CADÚNICO: Crianças de 0 a 5 anos em domicílio com inadequação habitacional, por componente',
              nome_arquivo='cadunico_criancas_inadequacao_componentes',
              fonte_dados=fonte_cadunico_silver + '. Metodologia da Fundação João Pinheiro; componentes não exclusivos')

# %%
grafico_barra(df_deficit_componentes.assign(Componente=df_deficit_componentes['Componente'].str.replace(' ', '\n', n=1)),
              categoria='Componente', valor='Crianças',
              titulo='CADÚNICO: Crianças de 0 a 5 anos em domicílio em déficit habitacional, por componente',
              nome_arquivo='cadunico_criancas_deficit_componentes',
              fonte_dados=fonte_cadunico_silver + '. Metodologia da Fundação João Pinheiro; componentes não exclusivos')

# %%
# um mapa (e uma tabela gêmea) por indicador: a agregação dos bairros pequenos depende do par de cada um -- juntos, o
# adensamento (89% dos bairros passam sozinhos) herdaria os conjuntos da inadequação (59%)
for _col, _rot, _titulo, _legenda, _nome in [
    ('fjp_inadequacao', 'Crianças em inadequação habitacional',
     '% de crianças de 0 a 5 anos no CadÚnico em domicílio com inadequação habitacional, por bairro', '% inadequação',
     'inadequacao'),
    ('adensamento_excessivo', 'Crianças em adensamento excessivo',
     '% de crianças de 0 a 5 anos no CadÚnico em domicílio com adensamento excessivo, por bairro', '% adensamento',
     'adensamento'),
]:
    _t = por_bairro_sim_base(df_criancas_silver, _col, _rot)
    _pct = '% ' + _rot[0].lower() + _rot[1:]
    _pub = agrega_bairros_pequenos(_t, ['Crianças', _rot, f'Base ({_rot})'], ['Crianças'], pares=[(_rot, f'Base ({_rot})')],
                                   taxas={_pct: (_rot, f'Base ({_rot})', 100)})
    _pub.to_csv(f'tabelas_finais/tabela_mapa_cadunico_{_nome}_bairro_2026.csv', index=False)
    mapa_coropletico_bairros(
        _pub[_pub['codbairro'].notna()], coluna_valor=_pct, titulo=_titulo,
        nome_arquivo=f'mapa_percentual_cadunico_{_nome}_bairro_2026', chave='codbairro',
        cmap=_CORES_TEMA_MAPA['cadunico'], legenda_titulo=_legenda,
        fonte_dados=fonte_mapa_cadunico_silver + ('.\nInadequação: metodologia da Fundação João Pinheiro'
                                                  if _nome == 'inadequacao' else '.\nMais de 3 pessoas por dormitório'))

# %% [markdown]
# #### 📌 Dados pontuais (ago/2026): moradia e deficiência
#
# > **Fora do site desde 2026-10-06** (`specs/2026-10-06_cadunico_inclusao_moradia` D1): Inclusão e Moradia usam a
# > silver nova (subseção acima). A célula fica pela história e porque o deck (`apresentacao/`) ainda lê estas CSVs.
#
# Extração **pontual** do CadÚnico enviada pela equipe (município do Rio, referência 08/2026), feita fora da rotina —
# não vem do banco CTPE, então esta célula roda sem `.env` (`specs/2026-09-29_dados_adhoc`). Entra só por acréscimo
# (nenhuma outra saída muda) e será substituída pela extração automatizada no 4º trimestre de 2026 (ROADMAP).
# Metadados (`is_adhoc`, `ref_date`, `replacement_pending`) e o aviso público: `dados_locais/cadunico/adhoc_2026_08.json`.
#
# - Faixas da extração: **0 a 3 e 4 a 6 anos** — a de 4 a 6 inclui os 6 anos, fora do padrão 0 a 5 (exceção com nota, D1).
# - Correções na leitura (a planilha fica como veio): fossa séptica, pessoas `'17..149'` → 17.149 (A1); aba
#   "FOSSA RUDIMENTA" era cópia da fossa séptica, descartada (A2); cisterna com 0 crianças e 1.323 famílias → crianças
#   não informadas (A3).
# - Nível município: sem supressão (a regra < 20 vale abaixo do município). Única taxa: % com BPC entre as crianças
#   com deficiência (numerador e denominador da mesma extração).
# - Famílias e pessoas com deficiência são de **todas as idades** (não "famílias com criança com deficiência"): só
#   contexto; os itens do catálogo seguem pendentes (D2).

# %%
df_moradia_adhoc = carrega_moradia_cadunico_adhoc()
df_moradia_adhoc_domicilio, df_moradia_adhoc_territorio = tabelas_cadunico_adhoc(df_moradia_adhoc)
df_deficiencia_adhoc, df_deficiencia_adhoc_contexto = carrega_deficiencia_cadunico_adhoc()
for _df, _nome in [(df_moradia_adhoc_domicilio, 'cadunico_adhoc_moradia_domicilio_2026_08'),
                   (df_moradia_adhoc_territorio, 'cadunico_adhoc_moradia_territorio_2026_08'),
                   (df_deficiencia_adhoc, 'cadunico_adhoc_deficiencia_2026_08'),
                   (df_deficiencia_adhoc_contexto, 'cadunico_adhoc_deficiencia_contexto_2026_08')]:
    _df.to_csv(f'tabelas_finais/{_nome}.csv', index=False)
print(df_moradia_adhoc.attrs['aviso'])
df_deficiencia_adhoc

# %% [markdown]
# ### 🏥 DataSus - tabnet

# %% [markdown]
# Séries do Datasus/Tabnet (nascidos vivos e óbitos), por bairro de residência, padronizadas pela função `limpeza_tabnet_bairros`.

# %% [markdown]
# #### Nascidos Vivos

# %% [markdown]
# Nascidos vivos totais por bairro (2006-2025).

# %%
#Nascidos vivos
df_vivos = pd.read_csv("dados_locais/nascidos_vivos/nascidos_vivos_bairros_2006_a_2025.csv")
df_vivos = limpa_dados_datasus(df_vivos)
df_vivos = limpeza_tabnet_bairros(df_vivos,categoria='nascidos vivos')
df_vivos.head()


# %% [markdown]
# ##### 🗺️ Mapa por bairro (2025)

# %%
fonte_datasus_bairro = 'DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro'

# 'EM BRANCO' (bairro não identificado) fica sem 'codigo' em limpeza_tabnet_bairros -- não
# mapeável, mesmo tratamento de dado incompleto já usado noutras seções ('Ignorado' etc.)
df_vivos_mapa = df_vivos[df_vivos['ano']=='2025'].dropna(subset=['codigo']).copy()
# populacao-referencia D1 (item "percentual de nascidos vivos por bairro de residência da mãe" do catálogo):
# nascidos vivos do bairro ÷ total do município × 100. O total INCLUI 'EM BRANCO' (bairro não informado:
# 3 de 58.700 em 2025, com o filtro de residência -- specs/2026-09-30_filtro_residencia_tabnet; antes, sem o
# filtro, eram 6.336 de 65.507 e a soma dos bairros ficava em ~90%), então a soma fica em ~100%.
# O mapa continua sendo o de contagem -- o percentual é a mesma informação dividida por uma constante.
_total_vivos_2025 = df_vivos.loc[df_vivos['ano']=='2025', 'nascidos vivos'].sum()
_em_branco_2025 = _total_vivos_2025 - df_vivos_mapa['nascidos vivos'].sum()
df_vivos_mapa['percentual_do_municipio'] = df_vivos_mapa['nascidos vivos'] / _total_vivos_2025 * 100
print(f'Nascidos vivos 2025: {_total_vivos_2025} no município, {_em_branco_2025} sem bairro (EM BRANCO); '
      f'soma dos bairros = {df_vivos_mapa["percentual_do_municipio"].sum():.1f}%')
df_vivos_mapa.to_csv('tabelas_finais//tabela_mapa_nascidos_vivos_2025.csv', index=False)

mapa_coropletico_bairros(
    df_vivos_mapa, coluna_valor='nascidos vivos', titulo='Nascidos vivos por bairro (2025)',
    nome_arquivo='mapa_nascidos_vivos_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['natalidade'],
    bins=[200, 400, 800, 1500], legenda_titulo='Nascidos vivos', fonte_dados=fonte_datasus_bairro,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_nascidos_vivos_bairro_2025 -->
# **Nota de curadoria:** Quando se olha para a distribuição espacial desses nascidos vivos pelo território carioca, há uma maior concentração deles na AP5 (Santa Cruz, Campo Grande e Bangu, por exemplo) e AP4 (Jacarepaguá, Barra da Tijuca, Recreio e Taquara, por exemplo). Ao passo que na AP 2, principalmente na Zona Sul há uma quantidade menor. Ficando a AP3 com uma quantidade intermediária.

# %%
#agrupamento por ano
df_vivos_por_ano = df_vivos.loc[:,['ano','nascidos vivos']].groupby(by='ano').sum()
df_vivos_por_ano.reset_index(inplace=True)
df_vivos_por_ano.rename({'variable':'ano','value':'nascidos vivos'},axis=1, inplace=True)
print(df_vivos_por_ano.head(25))
df_vivos_por_ano.to_csv('tabelas_finais/nascidos_vivos_por_ano.csv')

# %%
serie_temporal(df_vivos_por_ano,tempo='ano',valor='nascidos vivos', titulo='Nascidos vivos por ano',
               nome_arquivo='nascidos_vivos_por_ano', fonte_dados=fonte_datasus_bairro)

# %% [markdown]
# <!-- nota-curadoria:nascidos_vivos_por_ano -->
# **Nota de curadoria:** A partir do gráfico de nascidos vivos é possível observar que há uma tendência de queda no número de nascidos vivos na cidade do Rio de Janeiro, com alguns períodos de recuperação. Entre os anos de 2020 e 2021, após um período com uma persistente queda acentuada, a série atinge um patamar muito baixo, período que coincide com o pico da pandemia da COVID-19, e a queda continua nos anos seguintes. Logo, a queda, ainda que não linear, é consistente e aponta para uma redução de cerca de 30% ao longo da série histórica.

# %% [markdown]
# #### Nascidos abaixo peso

# %% [markdown]
# Nascidos vivos com baixo peso (&lt;2.500g) por bairro, como percentual dos nascidos vivos totais.

# %%
#Nascidos abaixo do peso
df_baixo_peso = pd.read_csv("dados_locais/nascidos_vivos/nascidos_vivos_baixo_peso_ao_nascer_bairros_2006_a_2025.csv")
df_baixo_peso = limpa_dados_datasus(df_baixo_peso)
df_baixo_peso = limpeza_tabnet_bairros(df_baixo_peso,categoria='nascidos abaixo peso')
df_baixo_peso.head()

# %%
df_baixo_peso['percentual abaixo do peso'] = (df_baixo_peso['nascidos abaixo peso']/df_vivos['nascidos vivos'])*100

# %% [markdown]
# ##### 🗺️ Mapa por bairro (2025)

# %%
df_baixo_peso_mapa = df_baixo_peso[df_baixo_peso['ano']=='2025'].dropna(subset=['codigo']).copy()
df_baixo_peso_mapa.to_csv('tabelas_finais//tabela_mapa_nascidos_baixo_peso_2025.csv', index=False)

mapa_coropletico_bairros(
    df_baixo_peso_mapa, coluna_valor='nascidos abaixo peso', titulo='Nascidos com baixo peso por bairro (2025)',
    nome_arquivo='mapa_nascidos_baixo_peso_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['natalidade'],
    bins=[15, 30, 60, 120], legenda_titulo='Nascidos abaixo do peso', fonte_dados=fonte_datasus_bairro,
)
mapa_coropletico_bairros(
    df_baixo_peso_mapa, coluna_valor='percentual abaixo do peso', titulo='% de nascidos com baixo peso por bairro (2025)',
    nome_arquivo='mapa_percentual_baixo_peso_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['natalidade'],
    legenda_titulo='% baixo peso', fonte_dados=fonte_datasus_bairro,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_percentual_baixo_peso_bairro_2025 -->
# **Nota de curadoria:** Em 2025, a maior parte dos bairros do Rio de Janeiro apresentou percentuais de nascidos com baixo peso entre 6,7% e 28,6%. Alguns bairros apresentam percentuais mais elevados, chegando a valores acima de 20%. Diferentemente dos números absolutos, o mapa percentual permite comparar melhor os bairros, pois considera a quantidade de nascidos com baixo peso em relação ao total de nascimentos. Valores extremos devem ser analisados com cautela, especialmente em bairros com poucos nascimentos.

# %% [markdown]
# <!-- nota-curadoria:mapa_nascidos_baixo_peso_bairro_2025 -->
# **Nota de curadoria:** A distribuição espacial dos nascidos com baixo peso em 2025 mostra maior concentração em bairros das Zona Oeste e Norte, com destaque para Campo Grande, Santa Cruz, Bangu, Jacarepaguá e Guaratiba. Em contraste, grande parte dos bairros apresenta até 30 registros. Como o mapa utiliza números absolutos, os maiores valores não indicam necessariamente maior incidência, sendo importante compará-los ao total de nascimentos de cada bairro.

# %%
df_baixo_ano = df_baixo_peso.loc[:,['ano','nascidos abaixo peso']].groupby(by='ano').sum()
df_baixo_ano.reset_index(inplace=True)
df_baixo_ano['percentual abaixo do peso'] = (df_baixo_ano['nascidos abaixo peso']/df_vivos_por_ano['nascidos vivos'])*100
df_baixo_ano.to_csv('tabelas_finais/nascidos_abaixo_peso_por_ano.csv')
df_baixo_ano.head(25)

# %%
# D3/D12 (specs/2026-09-29_pendencias): única exceção à base zero -- eixo cortado, com a marca e a nota na fonte
serie_temporal(df_baixo_ano,tempo='ano',valor='percentual abaixo do peso', titulo='Percentual Nascidos com baixo peso por ano',
               nome_arquivo='nascidos_abaixo_peso_percentual_por_ano', fonte_dados=fonte_datasus_bairro, base_zero=False)

# %% [markdown]
# <!-- nota-curadoria:nascidos_abaixo_peso_percentual_por_ano -->
# **Nota de curadoria:** Entre 2006 e 2025, o percentual de nascidos com baixo peso apresentou oscilações moderadas. Após permanecer próximo de 9,5% até 2010, o indicador caiu e atingiu seu menor valor em 2017, com 9,15%. A partir de 2018, observa-se uma tendência de crescimento, chegando ao pico de 10,39% em 2023. Nos anos seguintes houve pequena redução, com o percentual chegando a 10,00% em 2025.

# %% [markdown]
# #### 📉 Mortalidade

# %% [markdown]
# Óbitos até 1 ano de idade: por raça/cor, causas evitáveis, gravidez/puerpério e mortalidade neonatal (precoce, tardia, pós-neonatal e total).

# %% [markdown]
# ##### Óbitos até 1 ano por raça/cor

# %% [markdown]
# Combina os óbitos de menores de 1 ano (0 a 364 dias) por raça/cor (2006-2025) com os nascidos vivos por raça/cor da mãe (2011-2025), ambos por bairro de residência.
#
# Notas:
# - Colunas de ano ausentes nos arquivos do Tabnet indicam total 0 no período e são preenchidas com 0 na limpeza.
# - As categorias `Ignorado` e `Não informado` de nascidos vivos representam a mesma informação ausente, registrada sob nomes diferentes ao longo da série -> somadas em `nascidos_nao_informado`.
# - O percentual de óbitos por raça só é calculável a partir de 2011, quando começa a série de nascidos vivos por raça/cor da mãe.
# - Óbitos e nascidos vivos por raça vêm de consultas independentes do Datasus (óbito de residente x nascimento registrado no bairro) -> em bairros/anos com poucos casos é possível ter óbitos de uma raça sem nascidos vivos correspondentes, gerando percentuais instáveis ou indefinidos (tratados como NaN). Afeta principalmente `indigena`, `amarela` e `nao_informado`, categorias com poucas observações.

# %%
racas = ['amarela','branca','indigena','parda','preta','nao_informado']
arquivos_obitos = {'amarela':'amarelos','branca':'brancos','indigena':'indigenas',
                    'parda':'pardos','preta':'pretos','nao_informado':'nao_informado'}
anos_obitos = list(range(2006, 2026))

df_obitos_raca = None
for raca in racas:
    caminho = f'dados_locais//mortalidade//obitos_0_364_dias_{arquivos_obitos[raca]}_bairro_2006_2025.csv'
    df_raca = carrega_raca_bairro(caminho, categoria=f'obitos_{raca}', anos_validos=anos_obitos)
    df_obitos_raca = df_raca if df_obitos_raca is None else df_obitos_raca.merge(df_raca, on=['codigo','bairro','ano'], how='outer')

colunas_obitos = [f'obitos_{raca}' for raca in racas]
df_obitos_raca[colunas_obitos] = df_obitos_raca[colunas_obitos].fillna(0)
df_obitos_raca.head()

# %%
arquivos_nascidos = {'amarela':'mae_amarela','branca':'mae_branca','indigena':'mae_indigena',
                      'parda':'mae_parda','preta':'mae_preta'}
anos_nascidos = list(range(2011, 2026))

df_nascidos_raca = None
for raca, arquivo in arquivos_nascidos.items():
    caminho = f'dados_locais//mortalidade//nascidos_vivos_{arquivo}_bairro_2011_2025.csv'
    df_raca = carrega_raca_bairro(caminho, categoria=f'nascidos_{raca}', anos_validos=anos_nascidos)
    df_nascidos_raca = df_raca if df_nascidos_raca is None else df_nascidos_raca.merge(df_raca, on=['codigo','bairro','ano'], how='outer')

# 'Ignorado' e 'Não informado' são a mesma mãe sem raça/cor registrada (o Datasus mudou a
# nomenclatura ao longo da série) -> soma em uma única coluna nascidos_nao_informado
for arquivo in ['mae_ignorado','mae_nao_informado']:
    caminho = f'dados_locais//mortalidade//nascidos_vivos_{arquivo}_bairro_2011_2025.csv'
    df_raca = carrega_raca_bairro(caminho, categoria=arquivo, anos_validos=anos_nascidos)
    df_nascidos_raca = df_nascidos_raca.merge(df_raca, on=['codigo','bairro','ano'], how='outer')

colunas_nascidos = [f'nascidos_{raca}' for raca in arquivos_nascidos] + ['mae_ignorado','mae_nao_informado']
df_nascidos_raca[colunas_nascidos] = df_nascidos_raca[colunas_nascidos].fillna(0)
df_nascidos_raca['nascidos_nao_informado'] = df_nascidos_raca['mae_ignorado'] + df_nascidos_raca['mae_nao_informado']
df_nascidos_raca.drop(columns=['mae_ignorado','mae_nao_informado'], inplace=True)
df_nascidos_raca.head()

# %%
df_mortalidade_raca_bairro = df_obitos_raca.merge(df_nascidos_raca, on=['codigo','bairro','ano'], how='outer')

colunas_obitos = [f'obitos_{raca}' for raca in racas]
colunas_nascidos = [f'nascidos_{raca}' for raca in racas]
df_mortalidade_raca_bairro[colunas_obitos] = df_mortalidade_raca_bairro[colunas_obitos].fillna(0)

# nascidos vivos por raça só existe a partir de 2011: mantém NaN antes disso e preenche com 0
# quando o ano está no período coberto mas a combinação bairro/raça não teve registro
periodo_com_nascidos = df_mortalidade_raca_bairro['ano'].astype(int) >= 2011
df_mortalidade_raca_bairro.loc[periodo_com_nascidos, colunas_nascidos] = (
    df_mortalidade_raca_bairro.loc[periodo_com_nascidos, colunas_nascidos].fillna(0)
)

for raca in racas:
    percentual = (df_mortalidade_raca_bairro[f'obitos_{raca}'] / df_mortalidade_raca_bairro[f'nascidos_{raca}']) * 100
    df_mortalidade_raca_bairro[f'percentual_{raca}'] = percentual.replace([float('inf'), -float('inf')], float('nan')).round(2)

# total agregado (todas as raças somadas) -- percentual sempre recalculado a partir das somas,
# nunca média das 6 taxas por raça (mesma regra de agrega_bairros_por_nivel)
df_mortalidade_raca_bairro['obitos_total'] = df_mortalidade_raca_bairro[colunas_obitos].sum(axis=1)
df_mortalidade_raca_bairro['nascidos_total'] = df_mortalidade_raca_bairro[colunas_nascidos].sum(axis=1)
percentual_total = (df_mortalidade_raca_bairro['obitos_total'] / df_mortalidade_raca_bairro['nascidos_total']) * 100
df_mortalidade_raca_bairro['percentual_total'] = percentual_total.replace([float('inf'), -float('inf')], float('nan')).round(2)
# revisão de unidades (specs/2026-09-25_website_graficos): mortalidade infantil se publica por MIL nascidos vivos,
# como as demais taxas do relatório; `percentual_*` (por 100) fica no CSV só para quem já o lê
df_mortalidade_raca_bairro['taxa_mortalidade_infantil_total'] = (df_mortalidade_raca_bairro['percentual_total'] * 10).round(2)

df_mortalidade_raca_bairro = df_mortalidade_raca_bairro.sort_values(by=['ano','bairro']).reset_index(drop=True)
df_mortalidade_raca_bairro.to_csv('dados_locais//tratados//mortalidade_raca_bairro_ano.csv', index=False)
df_mortalidade_raca_bairro.to_csv('tabelas_finais//mortalidade_raca_bairro_ano.csv', index=False)
df_mortalidade_raca_bairro.head()

# %%
# agrega bairro -> município (todos os bairros pertencem ao município do Rio de Janeiro)
df_mortalidade_raca_municipio = (
    df_mortalidade_raca_bairro.groupby('ano')[colunas_obitos + colunas_nascidos]
    .sum(min_count=1)
    .reset_index()
)
df_mortalidade_raca_municipio['ano'] = df_mortalidade_raca_municipio['ano'].astype(int)
df_mortalidade_raca_municipio.sort_values(by='ano', inplace=True)

for raca in racas:
    percentual = (df_mortalidade_raca_municipio[f'obitos_{raca}'] / df_mortalidade_raca_municipio[f'nascidos_{raca}']) * 100
    df_mortalidade_raca_municipio[f'percentual_{raca}'] = percentual.replace([float('inf'), -float('inf')], float('nan')).round(2)

df_mortalidade_raca_municipio = agrupa_racas_raras(df_mortalidade_raca_municipio)   # E5, specs/exclusoes.md
# taxa por mil nascidos vivos (revisão de unidades), recalculada dos absolutos -- inclusive amarela_indigena
for raca in racas + ['amarela_indigena']:
    taxa = df_mortalidade_raca_municipio[f'obitos_{raca}'] / df_mortalidade_raca_municipio[f'nascidos_{raca}'] * 1000
    df_mortalidade_raca_municipio[f'taxa_mortalidade_{raca}'] = taxa.replace([float('inf'), -float('inf')], float('nan')).round(2)
df_mortalidade_raca_municipio.to_csv('dados_locais//tratados//mortalidade_raca_municipio_ano.csv', index=False)
df_mortalidade_raca_municipio.to_csv('tabelas_finais//mortalidade_raca_municipio_ano.csv', index=False)
df_mortalidade_raca_municipio

# %%
# E5 (specs/exclusoes.md): amarela e indígena desenhadas juntas
rotulos_raca = {'Branca':'branca','Parda':'parda','Preta':'preta',
                 'Amarela e indígena':'amarela_indigena','Não informada':'nao_informado'}

serie_temporal_multipla(
    df_mortalidade_raca_municipio,
    tempo='ano',
    colunas={rotulo: f'obitos_{raca}' for rotulo, raca in rotulos_raca.items()},
    titulo='Óbitos de 0 a 364 dias por raça/cor - Rio de Janeiro (2006-2025)',
    nome_arquivo='obitos_raca_ano',
    ylabel='Óbitos', fonte_dados=fonte_datasus_bairro,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_raca_ano -->
# **Nota de curadoria:** A série permite observar mudanças distintas na trajetória dos óbitos segundo raça/cor. Entre 2006 e 2025, os registros para crianças brancas passaram de 468 para 253, enquanto entre crianças pardas passaram de 373 para 375, após oscilações e valores superiores a 500 em alguns anos. Entre crianças pretas, os registros passaram de 89 para 53. A categoria “não informada” também apresentou redução, de 167 para 42, o que altera sua participação na série ao longo do período. Essas diferenças podem ser analisadas em conjunto com os nascidos vivos por raça/cor, disponíveis a partir de 2011, para distinguir composição dos nascimentos e ocorrência dos óbitos.

# %%
# percentual só existe a partir de 2011 (início da série de nascidos vivos por raça/cor da mãe)
df_percentual_raca_municipio = df_mortalidade_raca_municipio[df_mortalidade_raca_municipio['ano'] >= 2011]

# E14 (specs/exclusoes.md, specs/2026-09-29_pendencias D2): "Não informada" fica só no gráfico de óbitos -- óbitos sem
# raça (SIM) ÷ nascidos sem raça (SINASC) não é taxa comparável
rotulos_raca_taxa = {rotulo: raca for rotulo, raca in rotulos_raca.items() if raca != 'nao_informado'}

serie_temporal_multipla(
    df_percentual_raca_municipio,
    tempo='ano',
    colunas={rotulo: f'taxa_mortalidade_{raca}' for rotulo, raca in rotulos_raca_taxa.items()},
    titulo='Taxa de mortalidade infantil (0-364 dias) por raça/cor, por mil nascidos vivos - Rio de Janeiro (2011-2025)',
    nome_arquivo='percentual_mortalidade_raca_ano',   # nome do arquivo mantido (chave do texto curado e do crosswalk)
    ylabel='Óbitos por mil nascidos vivos',
    fonte_dados=f'{fonte_datasus_bairro}. Nota: a categoria "Não informada" aparece só no gráfico de óbitos',
)

# %% [markdown]
# <!-- nota-curadoria:percentual_mortalidade_raca_ano -->
# **Nota de curadoria:** A relação entre óbitos e nascidos vivos evidencia diferenças na mortalidade infantil que não aparecem apenas na contagem absoluta. Entre 2011 e 2025, as taxas de crianças brancas e pardas permaneceram próximas, variando de 17,6 a 11,2 e de 19,7 a 10,2 óbitos por mil nascidos vivos, respectivamente. Para crianças pretas, a taxa variou entre 5,0 e 14,3 por mil, enquanto a categoria amarela e indígena, agrupada por ter poucos registros, apresenta oscilações maiores associadas ao pequeno número de casos. A categoria “não informada” aparece só no gráfico de óbitos: a razão entre óbitos e nascidos sem raça/cor informada não é uma taxa comparável às demais. Essas características devem ser consideradas em comparações entre os grupos e na análise da série histórica.

# %% [markdown]
# ##### 🗺️ Mapa por bairro (2025) — total de óbitos, todas as raças

# %%
df_raca_mapa_2025 = df_mortalidade_raca_bairro[df_mortalidade_raca_bairro['ano'].astype(str) == '2025'].copy()
df_raca_mapa_2025.to_csv('tabelas_finais//tabela_mapa_obitos_raca_total_2025.csv', index=False)

mapa_coropletico_bairros(
    df_raca_mapa_2025, coluna_valor='obitos_total', titulo='Óbitos de 0 a 364 dias por bairro (2025)',
    nome_arquivo='mapa_obitos_raca_total_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['mortalidade'],
    bins=[2, 5, 10, 20], legenda_titulo='Óbitos', fonte_dados=fonte_datasus_bairro,
)
mapa_coropletico_bairros(
    df_raca_mapa_2025, coluna_valor='taxa_mortalidade_infantil_total', titulo='Taxa de mortalidade infantil (0-364 dias) por bairro (2025)',
    nome_arquivo='mapa_taxa_obitos_raca_total_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['mortalidade'],
    legenda_titulo='Óbitos por mil\nnascidos vivos', fonte_dados=fonte_datasus_bairro,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_taxa_obitos_raca_total_bairro_2025 -->
# **Nota de curadoria:** A taxa de mortalidade infantil permite comparar os bairros considerando a relação entre os óbitos e os nascidos vivos de cada território. Em 2025, Cidade Nova apresentou a maior taxa registrada, de 73,2 óbitos por mil nascidos vivos, com 3 óbitos entre 41 nascidos vivos, seguida por Gericinó, com 62,5 por mil (1 óbito entre 16 nascidos vivos). Ribeira apresentou 45,5 por mil, com 1 óbito entre 22 nascidos vivos. A comparação entre taxa, número de óbitos e nascidos vivos permite qualificar a leitura das diferenças territoriais e serve de base para relacionar o indicador a outros recortes da mortalidade infantil.

# %% [markdown]
# <!-- nota-curadoria:mapa_obitos_raca_total_bairro_2025 -->
# **Nota de curadoria:** A distribuição territorial dos óbitos infantis evidencia diferenças na quantidade de registros entre os bairros do município. Em 2025, Santa Cruz concentrou 53 óbitos, seguido por Campo Grande, com 40, e Jacarepaguá, com 32. Dos 167 bairros presentes na tabela, 130 registraram ao menos um óbito e 37 não apresentaram registros. Como o mapa utiliza números absolutos, essas diferenças podem ser relacionadas ao número de nascidos vivos de cada território, permitindo complementar a análise com a taxa de mortalidade infantil e outros recortes demográficos.

# %%
## Retirar não informados do gráfico de percentual

# %% [markdown]
# ##### Óbitos por causas evitáveis por raça/cor

# %% [markdown]
# Óbitos por causas evitáveis (0 a 364 dias, somando as faixas 0-6, 7-27 e 28-364 dias) por raça/cor (1996-2025), comparados aos nascidos vivos por raça/cor da mãe (2011-2025).
#
# Notas:
# - O Datasus só disponibiliza o cruzamento causas evitáveis x raça/cor no nível de município, não por bairro -> esta tabela tem granularidade município-ano (sem versão por bairro, ao contrário da seção anterior).
# - Valores marcados com `-` na fonte indicam 0 ocorrências e são convertidos para 0.
# - Assim como na série geral de óbitos por raça, o percentual só é calculável a partir de 2011.
# - **Atenção:** apesar do nome, este cruzamento por raça/cor não é filtrado só para causas evitáveis — o total por raça aqui fica entre 92% e 103% do total geral de óbitos por raça (seção anterior) na maior parte da série, só caindo mais claramente a partir de 2022. A quebra evitável / mal definida / demais causas só existe nos arquivos "segundo causas" (sem recorte por raça, próxima seção) -> os gráficos `percentual_mortalidade_raca_ano` e `percentual_mortalidade_causas_evitaveis_raca_ano` acabam sendo quase idênticos.
# - A categoria `nao_informado` tem um pico isolado em 1996 (2.136 óbitos, muito acima dos demais anos) por baixa completude do preenchimento de raça/cor no início da série -> não interpretar como aumento real de óbitos.

# %%
# faixas_evitaveis = {
#     '0_6': 'dados_locais//mortalidade//obitos_causas_evitaveis_0_6_dias_cor_raca_municipio_1996_2025.csv',
#     '7_27': 'dados_locais//mortalidade//obitos_causas_evitaveis_7_27_dias_cor_raca_municipio_1996_2025.csv',
#     '28_364': 'dados_locais//mortalidade//obitos_causas_evitaveis_28_364_dias_cor_raca_municipio_1996_2025.csv',
# }

# df_evitaveis_raca = None
# for faixa, caminho in faixas_evitaveis.items():
#     df_faixa = carrega_causas_evitaveis_raca(caminho, categoria='obitos')
#     df_evitaveis_raca = df_faixa if df_evitaveis_raca is None else pd.concat([df_evitaveis_raca, df_faixa])

# df_evitaveis_raca = df_evitaveis_raca.groupby(['raca','ano'], as_index=False)['obitos'].sum()

# df_evitaveis_raca_municipio = df_evitaveis_raca.pivot(index='ano', columns='raca', values='obitos')
# df_evitaveis_raca_municipio.columns = [f'obitos_evitaveis_{c}' for c in df_evitaveis_raca_municipio.columns]
# df_evitaveis_raca_municipio = df_evitaveis_raca_municipio.reset_index()
# df_evitaveis_raca_municipio['ano'] = df_evitaveis_raca_municipio['ano'].astype(int)
# df_evitaveis_raca_municipio.sort_values(by='ano', inplace=True)
# df_evitaveis_raca_municipio.head()

# # %%
# colunas_nascidos_municipio = [f'nascidos_{raca}' for raca in racas]
# df_evitaveis_raca_municipio = df_evitaveis_raca_municipio.merge(
#     df_mortalidade_raca_municipio[['ano'] + colunas_nascidos_municipio],
#     on='ano', how='left'
# )

# for raca in racas:
#     percentual = (df_evitaveis_raca_municipio[f'obitos_evitaveis_{raca}'] / df_evitaveis_raca_municipio[f'nascidos_{raca}']) * 100
#     df_evitaveis_raca_municipio[f'percentual_evitaveis_{raca}'] = percentual.replace([float('inf'), -float('inf')], float('nan')).round(2)

# df_evitaveis_raca_municipio.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_raca_municipio_ano.csv', index=False)
# df_evitaveis_raca_municipio.to_csv('tabelas_finais//mortalidade_causas_evitaveis_raca_municipio_ano.csv', index=False)
# df_evitaveis_raca_municipio

# # %%
# rotulos_raca_evitaveis = {'Amarela':'amarela','Branca':'branca','Indígena':'indigena',
#                            'Parda':'parda','Preta':'preta','Não informada':'nao_informado'}

# # fonte reaproveitada por todas as séries/mapas de óbitos por causas evitáveis desta seção
# # (raça/cor, grupo/subgrupo de causa e, mais adiante, por CAP) -- mesmo sistema de origem (SIM/SVS-Rio)
fonte_evitaveis = 'SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro'

# serie_temporal_multipla(
#     df_evitaveis_raca_municipio,
#     tempo='ano',
#     colunas={rotulo: f'obitos_evitaveis_{raca}' for rotulo, raca in rotulos_raca_evitaveis.items()},
#     titulo='Óbitos por causas evitáveis (0-364 dias) por raça/cor - Rio de Janeiro (1996-2025)',
#     nome_arquivo='obitos_causas_evitaveis_raca_ano',
#     ylabel='Óbitos', fonte_dados=fonte_evitaveis,
# )

# # %% [markdown]
# # **Versão sem `Não informada` e sem 1996:** o gráfico acima mantém as 6 categorias e a série
# # completa (1996-2025) para preservar a fidelidade à fonte. Para leitura de tendência, a
# # versão abaixo remove `nao_informado` (categoria de completude, não uma raça/cor) e o ano de
# # 1996, que tem um pico isolado de 2.136 óbitos "não informado" por baixa completude do
# # preenchimento de raça/cor no início da série (nota acima) -- não é um aumento real de óbitos.

# # %%
# rotulos_raca_evitaveis_sem_nao_informado = {
#     rotulo: raca for rotulo, raca in rotulos_raca_evitaveis.items() if rotulo != 'Não informada'
# }
# df_evitaveis_raca_sem_1996 = df_evitaveis_raca_municipio[df_evitaveis_raca_municipio['ano'] > 1996]

# serie_temporal_multipla(
#     df_evitaveis_raca_sem_1996,
#     tempo='ano',
#     colunas={rotulo: f'obitos_evitaveis_{raca}' for rotulo, raca in rotulos_raca_evitaveis_sem_nao_informado.items()},
#     titulo='Óbitos por causas evitáveis (0-364 dias) por raça/cor, sem "não informada" - Rio de Janeiro (1997-2025)',
#     nome_arquivo='obitos_causas_evitaveis_raca_sem_nao_informado_ano',
#     ylabel='Óbitos', fonte_dados=fonte_evitaveis,
# )

# # %%
# # percentual só existe a partir de 2011 (início da série de nascidos vivos por raça/cor da mãe)
# df_percentual_evitaveis_municipio = df_evitaveis_raca_municipio[df_evitaveis_raca_municipio['ano'] >= 2011]

# serie_temporal_multipla(
#     df_percentual_evitaveis_municipio,
#     tempo='ano',
#     colunas={rotulo: f'percentual_evitaveis_{raca}' for rotulo, raca in rotulos_raca_evitaveis.items()},
#     titulo='Percentual de óbitos evitáveis (0-364 dias) em relação aos nascidos vivos por raça/cor - Rio de Janeiro (2011-2025)',
#     nome_arquivo='percentual_mortalidade_causas_evitaveis_raca_ano',
#     ylabel='Percentual (%)', fonte_dados=fonte_evitaveis,
# )

# %% [markdown]
# **Versão sem `Não informada`:** já não inclui 1996 (a série só começa em 2011).

# %%
# serie_temporal_multipla(
#     df_percentual_evitaveis_municipio,
#     tempo='ano',
#     colunas={rotulo: f'percentual_evitaveis_{raca}' for rotulo, raca in rotulos_raca_evitaveis_sem_nao_informado.items()},
#     titulo='Percentual de óbitos evitáveis (0-364 dias) por raça/cor, sem "não informada" - Rio de Janeiro (2011-2025)',
#     nome_arquivo='percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano',
#     ylabel='Percentual (%)', fonte_dados=fonte_evitaveis,
# )

# %% [markdown]
# ##### Óbitos por causas evitáveis, por grupo de causa (CID-10)

# %% [markdown]
# Usa os arquivos "segundo causas" (não por raça/cor), que classificam cada óbito evitável em uma hierarquia de grupo/subgrupo/causa específica. Soma as três faixas etárias (0-6, 7-27 e 28-364 dias) para obter o total 0-364 dias, no nível de município (1996-2025).
#
# Dois recortes:
# - Grupo (`1.`, `2.`, `3.`): nível mais alto da hierarquia.
# - Subgrupo (`1.1.`, `1.2.1`, `1.2.2`, `1.2.3`, `1.3.`, `1.4.`, `2.`): filhos diretos do grupo `1.` mais o próprio grupo `2.` (que não se divide em subgrupos).
#
# `3. Demais causas (não claramente evitáveis)` não tem subgrupos e por isso só aparece no gráfico de grupo.

# %%
faixas_evitaveis_causa = {
    '0_6': 'dados_locais//mortalidade//obitos_causas_evitaveis_0_6_dias_segundo_causas_municipio_1996_2025.csv',
    '7_27': 'dados_locais//mortalidade//obitos_causas_evitaveis_7_27_dias_segundo_causas_municipio_1996_2025.csv',
    '28_364': 'dados_locais//mortalidade//obitos_causas_evitaveis_28_364_dias_segundo_causas_municipio_1996_2025.csv',
}

# grupo: '1. ', '2. ' ou '3. '; subgrupo: '1.1.', '1.2.1/2/3', '1.3.', '1.4.' ou '2.' (que não se subdivide)
padrao_grupo = r'^[123]\.\s'
padrao_subgrupo = r'^(1\.1\.|1\.2\.[123]|1\.3\.|1\.4\.|2\.)\s'

df_evitaveis_grupo = combina_faixas_causa(padrao_grupo, faixas_evitaveis_causa)
df_evitaveis_subgrupo = combina_faixas_causa(padrao_subgrupo, faixas_evitaveis_causa)

df_evitaveis_grupo_wide = df_evitaveis_grupo.pivot(index='ano', columns='causa', values='obitos').reset_index()
df_evitaveis_subgrupo_wide = df_evitaveis_subgrupo.pivot(index='ano', columns='causa', values='obitos').reset_index()

df_evitaveis_grupo_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_grupo_ano.csv', index=False)
df_evitaveis_subgrupo_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_subgrupo_ano.csv', index=False)
df_evitaveis_grupo_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_grupo_ano.csv', index=False)
df_evitaveis_subgrupo_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_ano.csv', index=False)
df_evitaveis_grupo_wide.head()

# %%
colunas_grupo = {c: c for c in df_evitaveis_grupo_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_grupo_wide,
    tempo='ano',
    colunas=colunas_grupo,
    titulo='Óbitos por causas evitáveis (0-364 dias) por grupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_grupo_ano',
    ylabel='Óbitos',
    legend_title='Grupo', fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_grupo_ano -->
# **Nota de curadoria:** Entre 1996 e 2025, observa-se uma redução expressiva dos óbitos de crianças de 0 a 364 dias por causas evitáveis. O número caiu de cerca de 1,5 mil registros no início da série para 502 em 2025. As causas mal definidas também apresentaram forte redução, chegando a 15 registros, enquanto as demais causas recuaram de forma mais moderada, alcançando 206 óbitos em 2025.

# %%
colunas_subgrupo = {c: c for c in df_evitaveis_subgrupo_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_subgrupo_wide,
    tempo='ano',
    colunas=filtra_colunas_subgrupo(colunas_subgrupo),   # E3, specs/exclusoes.md
    titulo='Óbitos por causas evitáveis (0-364 dias) por subgrupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7), fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_subgrupo_ano -->
# **Nota de curadoria:** Nos subgrupos de causas evitáveis, observa-se redução ao longo da série na maior parte das categorias. Os óbitos reduzíveis por adequada atenção à mulher na gestação permanecem como o principal grupo em 2025, com 263 registros. Também houve queda expressiva nos óbitos relacionados à atenção ao recém-nascido, que passaram de 543 em 1996 para 67 em 2025, enquanto aqueles relacionados à atenção à mulher no parto chegaram a 68 registros.

# %% [markdown]
# ##### Óbitos por causas evitáveis, por grupo de causa e faixa etária

# %% [markdown]
# Mesma classificação de grupo/subgrupo da seção anterior, mas sem somar as três faixas etárias: cada uma (0-6, 7-27 e 28-364 dias) é analisada separadamente, no mesmo recorte usado em Mortalidade Neonatal. Reaproveita `carrega_causas_evitaveis_categoria`, `combina_faixas_causa`, `padrao_grupo`, `padrao_subgrupo` e `faixas_evitaveis_causa`, já definidos acima.

# %% [markdown]
# ###### Precoce (0 a 6 dias)

# %%
df_evitaveis_grupo_0_6 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['0_6'], padrao_grupo)
df_evitaveis_subgrupo_0_6 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['0_6'], padrao_subgrupo)

df_evitaveis_grupo_0_6_wide = df_evitaveis_grupo_0_6.pivot(index='ano', columns='causa', values='obitos').reset_index()
df_evitaveis_subgrupo_0_6_wide = df_evitaveis_subgrupo_0_6.pivot(index='ano', columns='causa', values='obitos').reset_index()

df_evitaveis_grupo_0_6_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_grupo_0_a_6_dias_ano.csv', index=False)
df_evitaveis_subgrupo_0_6_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_subgrupo_0_a_6_dias_ano.csv', index=False)
df_evitaveis_grupo_0_6_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_grupo_0_a_6_dias_ano.csv', index=False)
df_evitaveis_subgrupo_0_6_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_0_a_6_dias_ano.csv', index=False)
df_evitaveis_grupo_0_6_wide.head()

# %%
colunas_grupo_0_6 = {c: c for c in df_evitaveis_grupo_0_6_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_grupo_0_6_wide,
    tempo='ano',
    colunas=colunas_grupo_0_6,
    titulo='Óbitos por causas evitáveis (0-6 dias) por grupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_grupo_0_a_6_dias_ano',
    ylabel='Óbitos',
    legend_title='Grupo', fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_grupo_0_a_6_dias_ano -->
# **Nota de curadoria:** Entre 1996 e 2025, os óbitos de crianças de 0 a 6 dias apresentaram queda expressiva. As causas evitáveis permaneceram como o principal grupo durante toda a série, reduzindo-se para 269 registros em 2025. No mesmo ano, as demais causas somaram 62 óbitos, enquanto as causas mal definidas ficaram em apenas 2 registros.

# %%
colunas_subgrupo_0_6 = {c: c for c in df_evitaveis_subgrupo_0_6_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_subgrupo_0_6_wide,
    tempo='ano',
    colunas=filtra_colunas_subgrupo(colunas_subgrupo_0_6),   # E3
    titulo='Óbitos por causas evitáveis (0-6 dias) por subgrupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_0_a_6_dias_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7), fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_subgrupo_0_a_6_dias_ano -->
# **Nota de curadoria:** Entre 1996 e 2025, os óbitos de crianças de 0 a 6 dias apresentaram redução em praticamente todos os subgrupos. As causas reduzíveis por atenção à mulher na gestação permaneceram como o principal componente, chegando a 183 registros em 2025. Também houve queda importante nos óbitos relacionados à atenção ao recém-nascido e à atenção à mulher no parto, enquanto as causas mal definidas ficaram em apenas 2 registros no final da série.

# %% [markdown]
# ###### Tardia (7 a 27 dias)

# %%
df_evitaveis_grupo_7_27 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['7_27'], padrao_grupo)
df_evitaveis_subgrupo_7_27 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['7_27'], padrao_subgrupo)

df_evitaveis_grupo_7_27_wide = df_evitaveis_grupo_7_27.pivot(index='ano', columns='causa', values='obitos').reset_index()
df_evitaveis_subgrupo_7_27_wide = df_evitaveis_subgrupo_7_27.pivot(index='ano', columns='causa', values='obitos').reset_index()

df_evitaveis_grupo_7_27_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_grupo_7_a_27_dias_ano.csv', index=False)
df_evitaveis_subgrupo_7_27_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_subgrupo_7_a_27_dias_ano.csv', index=False)
df_evitaveis_grupo_7_27_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_grupo_7_a_27_dias_ano.csv', index=False)
df_evitaveis_subgrupo_7_27_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_7_a_27_dias_ano.csv', index=False)
df_evitaveis_grupo_7_27_wide.head()

# %%
colunas_grupo_7_27 = {c: c for c in df_evitaveis_grupo_7_27_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_grupo_7_27_wide,
    tempo='ano',
    colunas=colunas_grupo_7_27,
    titulo='Óbitos por causas evitáveis (7-27 dias) por grupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_grupo_7_a_27_dias_ano',
    ylabel='Óbitos',
    legend_title='Grupo', fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_grupo_7_a_27_dias_ano -->
# **Nota de curadoria:** Entre 1996 e 2025, os óbitos entre 7 e 27 dias de vida apresentaram tendência de queda. As causas evitáveis permaneceram como o principal grupo, passando de níveis próximos a 250-280 registros no início da série para 99 em 2025. As demais causas também diminuíram, chegando a 42 registros, enquanto as causas mal definidas ficaram praticamente zeradas no final do período.

# %%
colunas_subgrupo_7_27 = {c: c for c in df_evitaveis_subgrupo_7_27_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_subgrupo_7_27_wide,
    tempo='ano',
    colunas=filtra_colunas_subgrupo(colunas_subgrupo_7_27),   # E3
    titulo='Óbitos por causas evitáveis (7-27 dias) por subgrupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_7_a_27_dias_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7), fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_subgrupo_7_a_27_dias_ano -->
# **Nota de curadoria:** Entre 1996 e 2025, os óbitos entre 7 e 27 dias de vida apresentaram tendência de queda na maior parte dos subgrupos. A maior queda ocorreu nas causas reduzíveis por adequada atenção ao recém-nascido, que passaram de 157 registros em 1996 para 20 em 2025. Já as causas relacionadas à atenção a mulher na gestação permaneceram como o principal subgrupo no final da série, com 64 óbitos em 2025. Os demais apresentaram valores mais abaixos.

# %% [markdown]
# ###### Pós-neonatal (28 a 364 dias)

# %%
df_evitaveis_grupo_28_364 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['28_364'], padrao_grupo)
df_evitaveis_subgrupo_28_364 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['28_364'], padrao_subgrupo)

df_evitaveis_grupo_28_364_wide = df_evitaveis_grupo_28_364.pivot(index='ano', columns='causa', values='obitos').reset_index()
df_evitaveis_subgrupo_28_364_wide = df_evitaveis_subgrupo_28_364.pivot(index='ano', columns='causa', values='obitos').reset_index()

df_evitaveis_grupo_28_364_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_grupo_28_a_364_dias_ano.csv', index=False)
df_evitaveis_subgrupo_28_364_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_subgrupo_28_a_364_dias_ano.csv', index=False)
df_evitaveis_grupo_28_364_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_grupo_28_a_364_dias_ano.csv', index=False)
df_evitaveis_subgrupo_28_364_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_28_a_364_dias_ano.csv', index=False)
df_evitaveis_grupo_28_364_wide.head()

# %%
colunas_grupo_28_364 = {c: c for c in df_evitaveis_grupo_28_364_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_grupo_28_364_wide,
    tempo='ano',
    colunas=colunas_grupo_28_364,
    titulo='Óbitos por causas evitáveis (28-364 dias) por grupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_grupo_28_a_364_dias_ano',
    ylabel='Óbitos',
    legend_title='Grupo', fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_grupo_28_a_364_dias_ano -->
# **Nota de curadoria:** Entre 1996 e 2025, os óbitos entre 28 e 364 dias apresentaram tendência de redução. As causas evitáveis permaneceram como o principal grupo, passando de 461 registros em 1996 para 134 em 2025. As demais causas também diminuíram, chegando a 102 óbitos, enquanto as causas mal definidas apresentaram a maior redução proporcional, passando de 108 para 13 registros.

# %%
colunas_subgrupo_28_364 = {c: c for c in df_evitaveis_subgrupo_28_364_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_subgrupo_28_364_wide,
    tempo='ano',
    colunas=filtra_colunas_subgrupo(colunas_subgrupo_28_364),   # E3
    titulo='Óbitos por causas evitáveis (28-364 dias) por subgrupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_28_a_364_dias_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7), fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_subgrupo_28_a_364_dias_ano -->
# **Nota de curadoria:** Entre 1996 e 2025, os óbitos entre 28 e 364 dias apresentaram queda na maior parte dos subgrupos. O principal destaque é a redução dos óbitos reduzíveis por ações de diagnóstico e tratamento adequado, que saíram de patamares muito elevados no início da série e chegaram a 43 registros em 2025. No final do período, os maiores valores ficaram em ações de promoção vinculadas às ações de atenção, com 56 óbitos, seguidas por diagnóstico e tratamento adequado, enquanto os demais subgrupos apresentaram números mais baixos.

# %% [markdown]
# ###### Comparação entre faixas etárias (2025)

# %% [markdown]
# Gráfico de barras comparando os 7 subgrupos de causas evitáveis entre as três faixas etárias, no último ano disponível (2025), para evidenciar a mudança de perfil de causas ao longo do primeiro ano de vida.

# %%
faixa_rotulo = {'0_6': '0-6 dias', '7_27': '7-27 dias', '28_364': '28-364 dias'}
tabelas_subgrupo = {'0_6': df_evitaveis_subgrupo_0_6_wide, '7_27': df_evitaveis_subgrupo_7_27_wide, '28_364': df_evitaveis_subgrupo_28_364_wide}

partes_2025 = []
for chave, df_wide in tabelas_subgrupo.items():
    linha_2025 = df_wide[df_wide['ano'] == 2025].melt(id_vars='ano', var_name='subgrupo', value_name='obitos')
    linha_2025['faixa_etaria'] = faixa_rotulo[chave]
    partes_2025.append(linha_2025)

df_subgrupo_2025 = pd.concat(partes_2025, ignore_index=True)
df_subgrupo_2025.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv', index=False)
df_subgrupo_2025.head()

# %%
ordem_subgrupo = [c for c in df_evitaveis_subgrupo_0_6_wide.columns if c != 'ano']
ordem_faixa = ['0-6 dias', '7-27 dias', '28-364 dias']

grafico_barra_agrupado(
    df_subgrupo_2025,
    categoria='faixa_etaria',
    valor='obitos',
    agrupador='subgrupo',
    titulo='Óbitos por causas evitáveis por subgrupo e faixa etária - Rio de Janeiro (2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_faixa_2025',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    ordem_categoria=ordem_faixa,
    ordem_agrupador=ordem_subgrupo,
    rotacao_x=0, fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_causas_evitaveis_subgrupo_faixa_2025 -->
# **Nota de curadoria:** Em 2025, a distribuição das causas evitáveis varia de forma importante entre as faixas etárias. Nos primeiros dias de vida, predominam os óbitos relacionados à atenção à mulher na gestação, com 183 registros entre 0 e 6 dias e 64 entre 7 e 27 dias. Já entre 28 e 364 dias, ganham maior peso as causas reduzíveis por ações de promoção vinculadas às ações de atenção, com 56 óbitos, e por diagnóstico e tratamento adequado, com 43 registros. O gráfico evidencia, portanto, uma mudança no perfil das causas evitáveis conforme a idade da criança: no período neonatal, destacam-se fatores ligados à gestação, parto e atenção ao recém-nascido, enquanto após os 28 aumentam relativamente às causas relacionadas à promoção, diagnóstico e tratamento.

# %% [markdown]
# ##### Óbitos por causas evitáveis na primeira infância, por Área Programática de Saúde (CAP)

# %% [markdown]
# Primeira vez no notebook com óbitos por causas evitáveis desagregados por **Área Programática de Saúde (CAP)** -- as 10 Coordenadorias de Área Programática da SMS-Rio (`cod_ap_sms`, geometria oficial em `dados_locais/geo/limite_ap_saude_rio.geojson`), que **não são** as 5 Áreas de Planejamento do IPP (`nivel='ap'`) usadas nos mapas do Censo acima. Fonte: planilha `obitos_causas_evitaveis_primeira_infancia_cap_2006_2025.xlsx`, exportada do TabWin/SIM municipal (SIM/SVS-Rio, óbitos de residentes no município do Rio de Janeiro), 2006-2025, em três faixas etárias: `< 1 ano`, `1-4 anos` e `< 5 anos`.
#
# Notas de leitura:
# 1. As três faixas são aninhadas: `< 5 anos` = `< 1 ano` + `1-4 anos` (verificado célula a célula, 0 divergências) -- **não somar as três**, seria dupla contagem.
# 2. 165 óbitos (0,7% da série) não têm CAP de residência registrada, concentrados em 2006-2011; **em 2025 são zero**, então os mapas de 2025 cobrem 100% dos óbitos.
# 3. A planilha só traz subgrupos CID; o grupo `1. Causas evitáveis` é a soma das seis linhas `1.*` -- diferente dos arquivos "segundo causas" das seções anteriores, onde grupo e subgrupo são linhas separadas.
# 4. `1-4 anos` tem contagens muito baixas (13 a 25 óbitos/ano na cidade inteira, 0 a 3 por CAP); percentuais por CAP nessa faixa são instáveis e não devem ser lidos como tendência.
# 5. O denominador (nascidos vivos) só existe no nível municipal -> sem taxa por mil NV por CAP; os mapas absolutos **não são comparáveis entre CAPs sem considerar o tamanho da população** -- a CAP 3.3 tem 29 bairros contra 5 da 5.2.
# 6. A CAP (SMS, 10 unidades) **não é** a Área de Planejamento do IPP (5 unidades) usada nos mapas do Censo deste mesmo notebook -- são divisões territoriais diferentes e não devem ser comparadas lado a lado sem ressalva.

# %% [markdown]
# ###### Panorama municipal (< 5 anos)

# %%
df_evitaveis_subgrupo_mrj = pd.read_csv('dados_locais//tratados//obitos_evitaveis_menores_5_causa_municipio_2006_2025.csv')
df_taxa_evitaveis_cap_mrj = pd.read_csv('dados_locais//tratados//taxa_mortalidade_evitaveis_menores_5_municipio_2006_2025.csv')

df_evitaveis_subgrupo_mrj.to_csv('tabelas_finais//obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv', index=False)
df_taxa_evitaveis_cap_mrj.to_csv('tabelas_finais//taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv', index=False)
df_taxa_evitaveis_cap_mrj.head()

# %%
df_evitaveis_subgrupo_mrj_wide = df_evitaveis_subgrupo_mrj.pivot(index='ano', columns='subgrupo', values='obitos').reset_index()
colunas_subgrupo_evitaveis_cap = {c: c for c in df_evitaveis_subgrupo_mrj_wide.columns if c != 'ano'}

serie_temporal_multipla(
    df_evitaveis_subgrupo_mrj_wide,
    tempo='ano',
    colunas=filtra_colunas_subgrupo(colunas_subgrupo_evitaveis_cap),   # E3
    titulo='Óbitos por causas evitáveis (< 5 anos) por subgrupo - Rio de Janeiro (2006-2025)',
    nome_arquivo='obitos_evitaveis_menores_5_subgrupo_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7), fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_evitaveis_menores_5_subgrupo_ano -->
# **Nota de curadoria:** Entre 2006 e 2025, os óbitos de menores de 5 anos apresentaram tendência geral de redução. As demais causas não claramente evitáveis permaneceram entre os principais componentes, chegando a 277 registros em 2025. Entre as causas evitáveis, destacam-se aquelas relacionadas à atenção à mulher na gestação, que atingiram 266 óbitos em 2025. Também houve redução importante nos óbitos relacionados à atenção ao recém-nascido, que passaram de 198 em 2006 para 55 em 2025, enquanto as causas mal definidas recuaram para 22 registros.

# %%
serie_temporal(
    df_taxa_evitaveis_cap_mrj, 'ano', 'taxa_por_mil',
    'Taxa de mortalidade por causas evitáveis (< 5 anos), por mil nascidos vivos - Rio de Janeiro (2006-2025)',
    nome_arquivo='taxa_mortalidade_evitaveis_menores_5_ano', fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:taxa_mortalidade_evitaveis_menores_5_ano -->
# **Nota de curadoria:** A taxa relaciona os óbitos por causas evitáveis ao número de nascidos vivos, permitindo acompanhar a ocorrência do indicador ao longo do tempo. Em 2006, foram registrados 1.353 óbitos e taxa de 16,48 por mil nascidos vivos. Em 2025, foram 856 óbitos e 14,58 por mil, enquanto o menor valor da série ocorreu em 2014, com 13,10 por mil. A trajetória apresenta oscilações, inclusive nos anos mais recentes, quando a taxa passou de 14,28 em 2022 para 14,97 em 2023, 14,28 em 2024 e 14,58 em 2025. A série permite acompanhar conjuntamente a ocorrência dos óbitos e sua relação com os nascidos vivos.

# %% [markdown]
# ###### Panorama municipal, por subgrupo — demais faixas etárias
#
# A série acima (subgrupo CID, `< 5 anos`) já vem pronta da aba `Informações gerais` da
# planilha. Para `< 1 ano` e `1-4 anos` (que não têm essa aba própria), soma-se as 10 CAPs
# dos CSVs já extraídos por faixa -- mesmo total, caminho diferente.

# %%
faixas_evitaveis_municipio_extra = {
    'menores_1_ano': 'menores de 1 ano',
    '1_a_4_anos':    'de 1 a 4 anos',
}

for sufixo, rotulo in faixas_evitaveis_municipio_extra.items():
    df_municipio_faixa = (
        pd.read_csv(f'dados_locais//tratados//obitos_evitaveis_{sufixo}_causa_cap_2006_2025.csv')
        .groupby(['subgrupo', 'ano'], as_index=False)['obitos'].sum()
    )
    df_municipio_faixa_wide = df_municipio_faixa.pivot(index='ano', columns='subgrupo', values='obitos').reset_index()

    serie_temporal_multipla(
        df_municipio_faixa_wide,
        tempo='ano',
        colunas=filtra_colunas_subgrupo({c: c for c in df_municipio_faixa_wide.columns if c != 'ano'}, rotulo),   # E2/E3
        titulo=f'Óbitos por causas evitáveis ({rotulo}) por subgrupo - Rio de Janeiro (2006-2025)',
        nome_arquivo=f'obitos_evitaveis_{sufixo}_subgrupo_ano',
        ylabel='Óbitos', legend_title='Subgrupo', figsize=(14,7), fonte_dados=fonte_evitaveis,
    )

# %% [markdown]
# ###### Por CAP e faixa etária

# %%
# bins definidos depois de ver a distribuição de 2025 por faixa (célula 'Mapas por CAP' abaixo)
# -- contagens uma ordem de grandeza menores em '1-4 anos' que em '< 1 ano'/'< 5 anos', então
# cada faixa tem seus próprios limites de classe (não dá pra reaproveitar entre faixas)
faixas_primeira_infancia = {
    'menores_1_ano':  {'rotulo': 'menores de 1 ano',   'bins_absoluto': [20, 40, 60, 80]},
    '1_a_4_anos':     {'rotulo': 'de 1 a 4 anos',       'bins_absoluto': [2, 4, 7, 10]},
    'menores_5_anos': {'rotulo': 'menores de 5 anos',   'bins_absoluto': [20, 45, 70, 95]},
}

partes_evitaveis_cap = []
for sufixo, info in faixas_primeira_infancia.items():
    df_bloco = pd.read_csv(f'dados_locais//tratados//obitos_evitaveis_{sufixo}_causa_cap_2006_2025.csv')
    df_bloco['faixa_etaria'] = info['rotulo']
    partes_evitaveis_cap.append(df_bloco)

df_evitaveis_cap_faixa = pd.concat(partes_evitaveis_cap, ignore_index=True)
df_evitaveis_cap_faixa.to_csv('dados_locais//tratados//mortalidade_evitaveis_cap_faixa_ano.csv', index=False)
df_evitaveis_cap_faixa.to_csv('tabelas_finais//mortalidade_evitaveis_cap_faixa_ano.csv', index=False)
df_evitaveis_cap_faixa.head()

# %%
df_evitaveis_grupo_cap_faixa = agrega_grupo_cid(df_evitaveis_cap_faixa, ['cod_ap_sms', 'ano', 'faixa_etaria'])

df_grupo_cap_faixa_wide = df_evitaveis_grupo_cap_faixa.pivot_table(
    index=['cod_ap_sms', 'ano', 'faixa_etaria'], columns='grupo', values='obitos', aggfunc='sum'
).reset_index()

colunas_grupo_cap = list(_GRUPOS_CID.values())
df_grupo_cap_faixa_wide['total'] = df_grupo_cap_faixa_wide[colunas_grupo_cap].sum(axis=1)
percentual_evitaveis_cap = df_grupo_cap_faixa_wide[_GRUPOS_CID['1']] / df_grupo_cap_faixa_wide['total'] * 100
df_grupo_cap_faixa_wide['percentual_evitaveis'] = percentual_evitaveis_cap.replace([float('inf'), -float('inf')], float('nan')).round(2)

df_grupo_cap_faixa_wide.to_csv('dados_locais//tratados//mortalidade_evitaveis_grupo_cap_faixa_ano.csv', index=False)
df_grupo_cap_faixa_wide.to_csv('tabelas_finais//mortalidade_evitaveis_grupo_cap_faixa_ano.csv', index=False)
df_grupo_cap_faixa_wide.head()

# %%
# nota de legenda das figuras de menores de 5 anos (observação da curadoria, specs/2026-09-28_nova_estrutura §6): o
# recorte soma os de menores de 1 ano e de 1 a 4 anos
def fonte_evitaveis_faixa(sufixo):
    return fonte_evitaveis + ('. Nota: agrega os recortes de menores de 1 ano e de 1 a 4 anos' if sufixo == 'menores_5_anos' else '')

for sufixo, info in faixas_primeira_infancia.items():
    df_faixa_grupo = df_grupo_cap_faixa_wide[df_grupo_cap_faixa_wide['faixa_etaria'] == info['rotulo']]

    df_obitos_evitaveis_wide = df_faixa_grupo.pivot(index='ano', columns='cod_ap_sms', values=_GRUPOS_CID['1']).reset_index()
    serie_temporal_multipla(
        df_obitos_evitaveis_wide,
        tempo='ano',
        colunas={c: c for c in df_obitos_evitaveis_wide.columns if c != 'ano'},
        titulo=f'Óbitos por causas evitáveis, {info["rotulo"]}, por CAP - Rio de Janeiro (2006-2025)',
        nome_arquivo=f'obitos_evitaveis_cap_{sufixo}_ano',
        ylabel='Óbitos',
        legend_title='CAP',
        figsize=(14,7), fonte_dados=fonte_evitaveis_faixa(sufixo),
    )

    df_percentual_evitaveis_wide = df_faixa_grupo.pivot(index='ano', columns='cod_ap_sms', values='percentual_evitaveis').reset_index()
    serie_temporal_multipla(
        df_percentual_evitaveis_wide,
        tempo='ano',
        colunas={c: c for c in df_percentual_evitaveis_wide.columns if c != 'ano'},
        titulo=f'Percentual de óbitos evitáveis, {info["rotulo"]}, por CAP - Rio de Janeiro (2006-2025)',
        nome_arquivo=f'percentual_evitaveis_cap_{sufixo}_ano',
        ylabel='Percentual (%)',
        legend_title='CAP',
        figsize=(14,7), fonte_dados=fonte_evitaveis_faixa(sufixo),
    )

# %%
df_total_menores_5_cap_wide = (
    df_grupo_cap_faixa_wide[df_grupo_cap_faixa_wide['faixa_etaria'] == 'menores de 5 anos']
    .pivot(index='ano', columns='cod_ap_sms', values='total').reset_index()
)
serie_temporal_multipla(
    df_total_menores_5_cap_wide,
    tempo='ano',
    colunas={c: c for c in df_total_menores_5_cap_wide.columns if c != 'ano'},
    titulo='Total de óbitos (todas as causas), menores de 5 anos, por CAP - Rio de Janeiro (2006-2025)',
    nome_arquivo='obitos_evitaveis_total_cap_ano',
    ylabel='Óbitos',
    legend_title='CAP',
    figsize=(14,7), fonte_dados=fonte_evitaveis,
)

# %% [markdown]
# <!-- nota-curadoria:obitos_evitaveis_total_cap_ano -->
# **Nota de curadoria:** A série permite acompanhar a evolução dos óbitos de menores de 5 anos nas diferentes Áreas Programáticas de Saúde (CAP) e comparar como esses registros variam entre os territórios ao longo do tempo. No conjunto das CAPs, os óbitos passaram de 1.311 em 2006 para 856 em 2025, com redução ao longo da série, embora tenha ocorrido aumento entre 2024 e 2025, de 819 para 856 registros. A distribuição territorial também apresenta diferenças importantes em 2025, com 150 óbitos na CAP 4.0 e 131 na CAP 3.3. Esses dados podem ser relacionados à composição das causas e ao percentual de óbitos evitáveis em cada CAP.

# %% [markdown]
# ###### Por subgrupo e CAP — séries temporais
#
# Cruzamento subgrupo × CAP: os 6 subgrupos do grupo `1. Causas evitáveis` (`1.1`-`1.4`,
# sem `2. Causas mal definidas`/`3. Demais causas`), para as 3 faixas etárias, uma linha por
# CAP em cada gráfico (18 gráficos). Contagens muito baixas nalgumas combinações (ex.
# `1.2.1`/`1-4 anos`/CAP pequena) geram linhas quase todas em zero -- mesma ressalva já feita
# para `1-4 anos` em geral.

# %%
# _SLUG_SUBGRUPO_EVITAVEL = {
#     '1.1. Reduzível pelas ações de imunização':   'imunizacao',
#     '1.2.1. Red por at à mulher na gestação':     'gestacao',
#     '1.2.2. Red por at à mulher no parto':        'parto',
#     '1.2.3. Red por at ao recém-nascido':         'recem_nascido',
#     '1.3. Red por ações de diag e trat adequado': 'diagnostico_tratamento',
#     '1.4. Red por ações promoção vinc a atenção': 'promocao_vinculacao',
# }

# for subgrupo, slug in _SLUG_SUBGRUPO_EVITAVEL.items():
#     for sufixo, info in faixas_primeira_infancia.items():
#         df_serie_subgrupo_cap = df_evitaveis_cap_faixa[
#             (df_evitaveis_cap_faixa['subgrupo'] == subgrupo) & (df_evitaveis_cap_faixa['faixa_etaria'] == info['rotulo'])
#         ].pivot(index='ano', columns='cod_ap_sms', values='obitos').reset_index()

#         serie_temporal_multipla(
#             df_serie_subgrupo_cap,
#             tempo='ano',
#             colunas={c: c for c in df_serie_subgrupo_cap.columns if c != 'ano'},
#             titulo=f'Óbitos evitáveis - {subgrupo.split(". ",1)[1]}, {info["rotulo"]}, por CAP (2006-2025)',
#             nome_arquivo=f'obitos_evitaveis_{slug}_cap_{sufixo}_ano',
#             ylabel='Óbitos', legend_title='CAP', figsize=(14,7), fonte_dados=fonte_evitaveis,
#         )

# %% [markdown]
# ###### 🗺️ Mapas por CAP (2025)

# %%
df_evitaveis_cap_2025 = df_grupo_cap_faixa_wide[df_grupo_cap_faixa_wide['ano'] == 2025].copy()
df_evitaveis_cap_2025 = df_evitaveis_cap_2025.rename(columns={
    _GRUPOS_CID['1']: 'evitaveis', _GRUPOS_CID['2']: 'mal_definidas', _GRUPOS_CID['3']: 'demais',
})
df_evitaveis_cap_2025.to_csv('dados_locais//tratados//mortalidade_evitaveis_cap_2025.csv', index=False)
df_evitaveis_cap_2025.to_csv('tabelas_finais//mortalidade_evitaveis_cap_2025.csv', index=False)

df_evitaveis_subgrupo_cap_2025 = df_evitaveis_cap_faixa[df_evitaveis_cap_faixa['ano'] == 2025]
df_evitaveis_subgrupo_cap_2025_wide = df_evitaveis_subgrupo_cap_2025.pivot_table(
    index=['cod_ap_sms', 'faixa_etaria'], columns='subgrupo', values='obitos', aggfunc='sum'
).reset_index()
df_evitaveis_subgrupo_cap_2025_wide.to_csv('dados_locais//tratados//mortalidade_evitaveis_subgrupo_cap_2025.csv', index=False)
df_evitaveis_subgrupo_cap_2025_wide.to_csv('tabelas_finais//mortalidade_evitaveis_subgrupo_cap_2025.csv', index=False)

# distribuição de 2025 por faixa, impressa antes de usar os bins acima -- os limites de
# 'faixas_primeira_infancia' já foram escolhidos a partir desta mesma distribuição
for sufixo, info in faixas_primeira_infancia.items():
    print(info['rotulo'])
    print(df_evitaveis_cap_2025.loc[df_evitaveis_cap_2025['faixa_etaria'] == info['rotulo'], 'evitaveis'].describe())

# %%
for sufixo, info in faixas_primeira_infancia.items():
    df_faixa_2025 = df_evitaveis_cap_2025[df_evitaveis_cap_2025['faixa_etaria'] == info['rotulo']]

    mapa_coropletico_bairros(
        df_faixa_2025, coluna_valor='evitaveis', nivel='cap',
        titulo=f'Óbitos por causas evitáveis, {info["rotulo"]}, por CAP - Rio de Janeiro (2025)',
        nome_arquivo=f'mapa_obitos_evitaveis_{sufixo}_cap_2025',
        cmap=_CORES_TEMA_MAPA['mortalidade'],
        bins=info['bins_absoluto'],
        legenda_titulo='Óbitos',
        caminho_geojson=_CAMINHO_GEO_CAP,
        fonte_dados=fonte_evitaveis_faixa(sufixo),
    )
    mapa_coropletico_bairros(
        df_faixa_2025, coluna_valor='percentual_evitaveis', nivel='cap',
        titulo=f'Proporção de óbitos evitáveis entre os óbitos, {info["rotulo"]}, por CAP - Rio de Janeiro (2025)',
        nome_arquivo=f'mapa_percentual_evitaveis_{sufixo}_cap_2025',
        cmap=_CORES_TEMA_MAPA['mortalidade'],
        legenda_titulo='% dos óbitos',
        caminho_geojson=_CAMINHO_GEO_CAP,
        fonte_dados=fonte_evitaveis_faixa(sufixo),
    )

# %% [markdown]
# ###### 🗺️ Mapas por subgrupo (gestação e parto, menores de 1 ano, 2025)
#
# Recorte mais fino que os mapas de grupo acima -- em vez do grupo `1. Causas evitáveis`
# (soma dos 6 subgrupos), estes dois mapeiam só um subgrupo cada, na faixa `< 1 ano` (onde
# causas ligadas a gestação/parto se concentram).

# %%
# subgrupos_componente_c = {
#     'gestacao': '1.2.1. Red por at à mulher na gestação',
#     'parto':    '1.2.2. Red por at à mulher no parto',
# }
# bins_subgrupo_componente_c = {
#     'gestacao': [10, 20, 30, 40],
#     'parto':    [2, 4, 6, 8],
# }

# for slug, subgrupo in subgrupos_componente_c.items():
#     df_subgrupo_2025 = df_evitaveis_cap_faixa[
#         (df_evitaveis_cap_faixa['ano'] == 2025)
#         & (df_evitaveis_cap_faixa['faixa_etaria'] == 'menores de 1 ano')
#         & (df_evitaveis_cap_faixa['subgrupo'] == subgrupo)
#     ]
#     df_subgrupo_2025.to_csv(f'tabelas_finais//tabela_mapa_obitos_evitaveis_{slug}_menores_1_ano_cap_2025.csv', index=False)

#     mapa_coropletico_bairros(
#         df_subgrupo_2025, coluna_valor='obitos', nivel='cap',
#         titulo=f'Óbitos evitáveis - {subgrupo.split(". ",1)[1]}, menores de 1 ano, por CAP (2025)',
#         nome_arquivo=f'mapa_obitos_evitaveis_{slug}_menores_1_ano_cap_2025',
#         cmap=_CORES_TEMA_MAPA['mortalidade'],
#         bins=bins_subgrupo_componente_c[slug],
#         legenda_titulo='Óbitos', caminho_geojson=_CAMINHO_GEO_CAP, fonte_dados=fonte_evitaveis,
#     )

# %% [markdown]
# ###### Séries temporais — gestação e parto, menores de 1 ano, por CAP
#
# Mesmo recorte dos 2 mapas acima, em série temporal (2006-2025) em vez de foto de 2025 --
# subconjunto da matriz completa da seção "Por subgrupo e CAP" acima, não um cálculo novo.

# %%
# for slug in ('gestacao', 'parto'):
#     df_serie_componente_c = df_evitaveis_cap_faixa[
#         (df_evitaveis_cap_faixa['subgrupo'] == subgrupos_componente_c[slug])
#         & (df_evitaveis_cap_faixa['faixa_etaria'] == 'menores de 1 ano')
#     ].pivot(index='ano', columns='cod_ap_sms', values='obitos').reset_index()

#     serie_temporal_multipla(
#         df_serie_componente_c,
#         tempo='ano',
#         colunas={c: c for c in df_serie_componente_c.columns if c != 'ano'},
#         titulo=f'Óbitos evitáveis - {subgrupos_componente_c[slug].split(". ",1)[1]}, menores de 1 ano, por CAP (2006-2025)',
#         nome_arquivo=f'obitos_evitaveis_{slug}_cap_menores_1_ano_ano',
#         ylabel='Óbitos', legend_title='CAP', figsize=(14,7), fonte_dados=fonte_evitaveis,
#     )

# %% [markdown]
# #### 📋 Óbitos gravidez e puerpério

# %% [markdown]
# Óbitos maternos durante a gravidez e o puerpério, por bairro de residência (2006-2025).

# %%
df_obitos_gravidez = pd.read_csv('dados_locais/mortalidade/obitos_gravidez_bairro_2006_2025.csv')
df_obitos_gravidez = limpa_dados_datasus(df_obitos_gravidez)
df_obitos_gravidez = limpeza_tabnet_bairros(df_obitos_gravidez,categoria='óbitos-gravidez')
df_obitos_gravidez.to_csv('tabelas_finais//obitos_gravidez_bairro_ano.csv', index=False)
df_obitos_gravidez.head()

# %%
#por ano
df_obitos_gravidez_anual = df_obitos_gravidez[['ano','óbitos-gravidez']].groupby(by='ano').sum()
df_obitos_gravidez_anual.to_csv('tabelas_finais//obitos_gravidez_por_ano.csv')
df_obitos_gravidez_anual

# %%
serie_temporal(df_obitos_gravidez_anual,'ano','óbitos-gravidez','Óbitos durante gravidez por ano',
               nome_arquivo='obitos_gravidez_por_ano', fonte_dados=fonte_datasus_bairro)

# %% [markdown]
# <!-- nota-curadoria:obitos_gravidez_por_ano -->
# **Nota de curadoria:** A série histórica permite acompanhar a variação dos óbitos ocorridos durante a gravidez no município entre 2006 e 2025. O número de registros passou de 58 em 2006 para 14 em 2025, uma redução de aproximadamente 76%, embora a trajetória apresente oscilações ao longo do período. Em 2024 foram registrados 4 óbitos, seguido de aumento para 14 em 2025. Por se tratar de número absoluto de óbitos, o indicador permite acompanhar a evolução temporal do evento, mas não representa, isoladamente, uma medida de risco. A série pode servir de base para comparações com outros indicadores de mortalidade materna.

# %% [markdown]
# ##### 🗺️ Mapa por bairro (2025)
#
# **Nota:** contagens muito pequenas por bairro (a maioria com 0 óbitos em 2025) -- leia como
# indicador de onde há registro do evento, não como comparação robusta de magnitude entre
# bairros.

# %%
df_obitos_gravidez_mapa = df_obitos_gravidez[df_obitos_gravidez['ano'].astype(str) == '2025'].dropna(subset=['codigo']).copy()
df_obitos_gravidez_mapa.to_csv('tabelas_finais//tabela_mapa_obitos_gravidez_2025.csv', index=False)

# mapa_coropletico_bairros(
#     df_obitos_gravidez_mapa, coluna_valor='óbitos-gravidez', titulo='Óbitos durante a gravidez por bairro (2025)',
#     nome_arquivo='mapa_obitos_gravidez_bairro_2025', chave='codigo',
#     cmap=_CORES_TEMA_MAPA['mortalidade'],
#     bins=[0, 1], legenda_titulo='Óbitos', fonte_dados=fonte_datasus_bairro,
# )

# %% [markdown]
# <!-- nota-curadoria:mapa_obitos_gravidez_bairro_2025 -->
# **Nota de curadoria:** A distribuição territorial dos óbitos durante a gravidez permite identificar os bairros com registros do evento em 2025. Foram registrados 14 óbitos em 12 bairros, com dois registros em Vigário Geral e Rocinha. O total do mapa é o mesmo da série municipal (14 óbitos em 2025). Como são números absolutos e contagens pequenas, o mapa pode ser utilizado como referência territorial e relacionado a outros indicadores, como nascidos vivos, população e características demográficas, para ampliar a análise da mortalidade materna.

# %%
df_obitos_puerperio = pd.read_csv('dados_locais/mortalidade/obitos_puerperio_bairro_2006_2025.csv')
df_obitos_puerperio = limpa_dados_datasus(df_obitos_puerperio)
df_obitos_puerperio = limpeza_tabnet_bairros(df_obitos_puerperio,categoria='óbitos-puerpério')
df_obitos_puerperio.to_csv('tabelas_finais//obitos_puerperio_bairro_ano.csv', index=False)
df_obitos_puerperio.head()

# %%
#por ano
df_obitos_puerperio_anual = df_obitos_puerperio[['ano','óbitos-puerpério']].groupby(by='ano').sum()
df_obitos_puerperio_anual.to_csv('tabelas_finais//obitos_puerperio_por_ano.csv')
df_obitos_puerperio_anual

# %%
serie_temporal(df_obitos_puerperio_anual,'ano','óbitos-puerpério','Óbitos durante puerpério por ano',
               nome_arquivo='obitos_puerperio_por_ano', fonte_dados=fonte_datasus_bairro)

# %% [markdown]
# <!-- nota-curadoria:obitos_puerperio_por_ano -->
# **Nota de curadoria:** A série histórica permite acompanhar a variação dos óbitos ocorridos durante o puerpério entre 2006 e 2025. Os registros passaram de 48 em 2006 para 29 em 2025, com oscilações ao longo do período. Destaca-se o aumento observado em 2020 e 2021, quando foram registrados 63 e 79 óbitos, respectivamente, seguido de redução nos anos posteriores. Em 2024 ocorreu o menor número da série, com 25 óbitos, seguido de 29 em 2025. A série pode ser utilizada para comparações temporais com outros indicadores de mortalidade materna.

# %% [markdown]
# ##### 🗺️ Mapa por bairro (2025)
#
# **Nota:** mesma ressalva do mapa de óbitos na gravidez acima -- contagens muito pequenas
# por bairro.

# %%
df_obitos_puerperio_mapa = df_obitos_puerperio[df_obitos_puerperio['ano'].astype(str) == '2025'].dropna(subset=['codigo']).copy()
df_obitos_puerperio_mapa.to_csv('tabelas_finais//tabela_mapa_obitos_puerperio_2025.csv', index=False)

# mapa_coropletico_bairros(
#     df_obitos_puerperio_mapa, coluna_valor='óbitos-puerpério', titulo='Óbitos durante o puerpério por bairro (2025)',
#     nome_arquivo='mapa_obitos_puerperio_bairro_2025', chave='codigo',
#     cmap=_CORES_TEMA_MAPA['mortalidade'],
#     bins=[0, 1, 2], legenda_titulo='Óbitos', fonte_dados=fonte_datasus_bairro,
# )

# %% [markdown]
# <!-- nota-curadoria:mapa_obitos_puerperio_bairro_2025 -->
# **Nota de curadoria:** A distribuição territorial dos óbitos durante o puerpério permite identificar os bairros com registros do evento em 2025. Foram registrados 29 óbitos distribuídos em 22 bairros, com maior número em Senador Camará, que apresentou 3 registros. Jacarepaguá, Bangu, Pavuna, Guaratiba e Complexo do Alemão registraram 2 óbitos cada, enquanto os demais bairros com ocorrência apresentaram 1 registro. O total do mapa é o mesmo da série municipal (29 óbitos em 2025). Como são números absolutos, o mapa pode ser relacionado a outros indicadores, como nascidos vivos e características demográficas, para ampliar a análise territorial da mortalidade materna.

# %% [markdown]
# #### 🩺 Mortalidade Neonatal


# %% [markdown]
# Óbitos de menores de 1 ano por faixa etária (precoce, tardia, pós-neonatal e total 0-364 dias), com taxa por 1.000 nascidos vivos.
#
# > **Nota:** Precoce e Tardia comparam com `df_vivos` por *inner join* (bairros sem óbito registrado em algum lado ficam de fora); Pós-neonatal e Total usam uma grade bairro x ano com zeros explícitos, mais robusta. As taxas de Precoce/Tardia podem, por isso, subestimar ligeiramente bairros pequenos.

# %% [markdown]
# ##### Precoce (0 a 6 dias)

# %%
df_neonatal_precoce = pd.read_csv('dados_locais//mortalidade//obitos_0_6_dias_bairro_2006_2025.csv', sep=';')
df_neonatal_precoce = limpa_dados_datasus(df_neonatal_precoce)
df_neonatal_precoce = limpeza_tabnet_bairros(df_neonatal_precoce,categoria='obitos precoces')
df_neonatal_precoce = df_neonatal_precoce.merge(df_vivos, on=['bairro','ano','codigo'])
df_neonatal_precoce['taxa_mortalidade_precoce'] = (df_neonatal_precoce['obitos precoces']/df_neonatal_precoce['nascidos vivos'])*1000
df_neonatal_precoce.to_csv('tabelas_finais//mortalidade_neonatal_precoce_bairro_ano.csv', index=False)
df_neonatal_precoce.head()

# %%
df_neonatal_precoce_anual = df_neonatal_precoce[['ano','obitos precoces','nascidos vivos']].groupby(by='ano').sum()
df_neonatal_precoce_anual['taxa_mortalidade_precoce'] = (df_neonatal_precoce_anual['obitos precoces']/df_neonatal_precoce_anual['nascidos vivos'])*1000
df_neonatal_precoce_anual.to_csv('tabelas_finais//mortalidade_neonatal_precoce_por_ano.csv')
df_neonatal_precoce_anual

# %%
serie_temporal(df_neonatal_precoce_anual,'ano','taxa_mortalidade_precoce','Taxa de óbitos precoces por ano',
               nome_arquivo='taxa_mortalidade_precoce_ano', fonte_dados=fonte_datasus_bairro)

# %% [markdown]
# <!-- nota-curadoria:taxa_mortalidade_precoce_ano -->
# **Nota de curadoria:** A série histórica permite analisar a evolução da mortalidade neonatal precoce em relação ao número de nascidos vivos no município. Entre 2006 e 2025, a taxa passou de 6,86 para 5,68 óbitos por mil nascidos vivos, embora tenha apresentado oscilações ao longo do período. Em 2024, foram registrados 322 óbitos, o menor número da série, seguido de aumento para 333 em 2025. A leitura conjunta da taxa e dos números absolutos permite distinguir mudanças na ocorrência dos óbitos de variações relacionadas ao número de nascidos vivos, servindo como base para comparações temporais e para o cruzamento com outros indicadores de mortalidade infantil.

# %% [markdown]
# ###### 🗺️ Mapa por bairro (2025)

# %%
df_neonatal_precoce_mapa = df_neonatal_precoce[df_neonatal_precoce['ano'].astype(str) == '2025'].dropna(subset=['codigo']).copy()
df_neonatal_precoce_mapa.to_csv('tabelas_finais//tabela_mapa_obitos_neonatal_precoce_2025.csv', index=False)

mapa_coropletico_bairros(
    df_neonatal_precoce_mapa, coluna_valor='obitos precoces', titulo='Óbitos precoces (0-6 dias) por bairro (2025)',
    nome_arquivo='mapa_obitos_neonatal_precoce_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['mortalidade'],
    bins=[1, 3, 6, 12], legenda_titulo='Óbitos', fonte_dados=fonte_datasus_bairro,
)
mapa_coropletico_bairros(
    df_neonatal_precoce_mapa, coluna_valor='taxa_mortalidade_precoce', titulo='Taxa de óbitos precoces (0-6 dias) por bairro (2025)',
    nome_arquivo='mapa_taxa_mortalidade_precoce_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['mortalidade'],
    legenda_titulo='Taxa por mil NV', fonte_dados=fonte_datasus_bairro,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_taxa_mortalidade_precoce_bairro_2025 -->
# **Nota de curadoria:** A taxa de mortalidade neonatal precoce permite comparar os bairros considerando o número de nascidos vivos de cada território, evitando a interpretação baseada apenas na quantidade de óbitos. Em 2025, alguns bairros apresentam taxas elevadas associadas a poucos registros de óbitos e a um número reduzido de nascidos vivos, como Gericinó, com 1 óbito entre 16 nascidos vivos, e Ribeira, com 1 entre 22. Por isso, a leitura territorial da taxa deve considerar também o número absoluto de óbitos e o tamanho do denominador. Esses dados podem servir de base para comparar os territórios e aprofundar a análise em conjunto com outros indicadores.

# %% [markdown]
# <!-- nota-curadoria:mapa_obitos_neonatal_precoce_bairro_2025 -->
# **Nota de curadoria:** A distribuição dos óbitos neonatais precoces por bairro permite identificar como os 333 óbitos registrados em 2025 estão distribuídos territorialmente. Por apresentar números absolutos, o mapa possibilita comparar a quantidade de óbitos entre os bairros e reconhecer onde esses registros estão mais concentrados. A informação pode ser utilizada como base para cruzamentos com o número de nascidos vivos, relacionando a ocorrência dos óbitos ao tamanho da população exposta. O recorte territorial também pode ser relacionado a outros indicadores de mortalidade infantil e características demográficas dos bairros, ampliando a análise do fenômeno.

# %% [markdown]
# ##### Tardia (7 a 27 dias)

# %%
df_neonatal_tardia = pd.read_csv('dados_locais//mortalidade//obitos_7_27_dias_bairro_2006_2025.csv', sep=';')
df_neonatal_tardia = limpa_dados_datasus(df_neonatal_tardia)
df_neonatal_tardia = limpeza_tabnet_bairros(df_neonatal_tardia,'obitos_tardios')
df_neonatal_tardia = df_neonatal_tardia.merge(df_vivos, on=['bairro','ano','codigo'])
df_neonatal_tardia['taxa_obitos_tardios'] = (df_neonatal_tardia['obitos_tardios']/df_neonatal_tardia['nascidos vivos'])*1000
df_neonatal_tardia.to_csv('tabelas_finais//mortalidade_neonatal_tardia_bairro_ano.csv', index=False)
df_neonatal_tardia.head()

# %%
df_neonatal_tardia_anual = df_neonatal_tardia[['ano','obitos_tardios','nascidos vivos']].groupby(by='ano').sum()
df_neonatal_tardia_anual['taxa_obitos_tardios'] = (df_neonatal_tardia_anual['obitos_tardios']/df_neonatal_tardia_anual['nascidos vivos'])*1000
df_neonatal_tardia_anual.to_csv('tabelas_finais//mortalidade_neonatal_tardia_por_ano.csv')
df_neonatal_tardia_anual

# %%
serie_temporal(df_neonatal_tardia_anual,'ano','taxa_obitos_tardios','Taxa de óbitos tardios por ano',
               nome_arquivo='taxa_obitos_tardios_ano', fonte_dados=fonte_datasus_bairro)

# %% [markdown]
# <!-- nota-curadoria:taxa_obitos_tardios_ano -->
# **Nota de curadoria:** A série histórica permite acompanhar a evolução da mortalidade neonatal tardia em relação ao número de nascidos vivos. Entre 2006 e 2025, a taxa passou de 2,17 para 2,43 óbitos por mil nascidos vivos, com oscilações ao longo do período. O maior valor ocorreu em 2020 (2,79), enquanto o menor foi registrado em 2011 (1,95). No mesmo período, os óbitos tardios passaram de 178 para 142. A leitura conjunta desses indicadores permite diferenciar a variação no número de óbitos da variação proporcional em relação aos nascidos vivos e serve de base para comparações temporais com outros indicadores de mortalidade infantil.

# %% [markdown]
# ###### 🗺️ Mapa por bairro (2025)

# %%
df_neonatal_tardia_mapa = df_neonatal_tardia[df_neonatal_tardia['ano'].astype(str) == '2025'].dropna(subset=['codigo']).copy()
df_neonatal_tardia_mapa.to_csv('tabelas_finais//tabela_mapa_obitos_neonatal_tardia_2025.csv', index=False)

# mapa_coropletico_bairros(
#     df_neonatal_tardia_mapa, coluna_valor='obitos_tardios', titulo='Óbitos tardios (7-27 dias) por bairro (2025)',
#     nome_arquivo='mapa_obitos_neonatal_tardia_bairro_2025', chave='codigo',
#     cmap=_CORES_TEMA_MAPA['mortalidade'],
#     bins=[1, 2, 4, 8], legenda_titulo='Óbitos', fonte_dados=fonte_datasus_bairro,
# )
mapa_coropletico_bairros(
    df_neonatal_tardia_mapa, coluna_valor='taxa_obitos_tardios', titulo='Taxa de óbitos tardios (7-27 dias) por bairro (2025)',
    nome_arquivo='mapa_taxa_obitos_tardios_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['mortalidade'],
    legenda_titulo='Taxa por mil NV', fonte_dados=fonte_datasus_bairro,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_taxa_obitos_tardios_bairro_2025 -->
# **Nota de curadoria:** A taxa de mortalidade neonatal tardia permite comparar os bairros considerando o número de nascidos vivos de cada território. Em 2025, alguns bairros apresentam taxas elevadas mesmo com apenas um óbito, como Cidade Nova, com 1 óbito entre 41 nascidos vivos, e Riachuelo, com 1 entre 63. Dos 159 bairros da tabela, 88 não registraram óbitos tardios. Por isso, a leitura da taxa deve considerar conjuntamente o número de óbitos e o número de nascidos vivos, especialmente nos territórios com menor número de nascimentos. O indicador pode servir de base para comparações territoriais e cruzamentos com outros dados de mortalidade infantil.

# %% [markdown]
# <!-- nota-curadoria:mapa_obitos_neonatal_tardia_bairro_2025 -->
# **Nota de curadoria:** A distribuição territorial dos óbitos neonatais tardios permite identificar como os registros de 2025 se concentram entre os bairros. Na base utilizada para o mapa, 88 bairros não apresentaram registros, enquanto os maiores números ocorreram em Santa Cruz e Campo Grande, com 12 óbitos cada, e Jacarepaguá, com 8. Como se trata de números absolutos, a quantidade de óbitos deve ser interpretada em conjunto com o número de nascidos vivos de cada território. Essa informação pode servir de base para comparar a distribuição dos registros com as respectivas taxas e com outros indicadores de mortalidade neonatal.

# %% [markdown]
# ##### Pós-neonatal (28 a 364 dias)

# %% [markdown]
# Não há arquivo pronto para 28-364 dias (total, sem raça): é derivado por subtração `0-364 - 0-6 - 7-27`, com cada faixa preenchida em uma grade completa bairro x ano (zeros verdadeiros onde o Tabnet omite colunas/linhas de soma zero), para evitar contagens incompletas na subtração.

# %%
anos_infantil = list(range(2006, 2026))

df_nascidos_total = carrega_raca_bairro('dados_locais//nascidos_vivos//nascidos_vivos_bairros_2006_a_2025.csv', categoria='nascidos_vivos', anos_validos=anos_infantil, sep=',')
df_obitos_0_364_total = carrega_raca_bairro('dados_locais//mortalidade//obitos_0_364_dias_bairro_2006_2025.csv', categoria='obitos_0_364', anos_validos=anos_infantil)
df_obitos_0_6_total = carrega_raca_bairro('dados_locais//mortalidade//obitos_0_6_dias_bairro_2006_2025.csv', categoria='obitos_0_6', anos_validos=anos_infantil)
df_obitos_7_27_total = carrega_raca_bairro('dados_locais//mortalidade//obitos_7_27_dias_bairro_2006_2025.csv', categoria='obitos_7_27', anos_validos=anos_infantil)

df_mortalidade_infantil = (
    df_obitos_0_364_total
    .merge(df_obitos_0_6_total, on=['codigo','bairro','ano'], how='outer')
    .merge(df_obitos_7_27_total, on=['codigo','bairro','ano'], how='outer')
    .merge(df_nascidos_total, on=['codigo','bairro','ano'], how='outer')
)

colunas_obitos_faixas = ['obitos_0_364','obitos_0_6','obitos_7_27']
df_mortalidade_infantil[colunas_obitos_faixas] = df_mortalidade_infantil[colunas_obitos_faixas].fillna(0)
df_mortalidade_infantil['nascidos_vivos'] = df_mortalidade_infantil['nascidos_vivos'].fillna(0)

df_mortalidade_infantil['obitos_28_364'] = (
    df_mortalidade_infantil['obitos_0_364'] - df_mortalidade_infantil['obitos_0_6'] - df_mortalidade_infantil['obitos_7_27']
)

df_mortalidade_infantil['taxa_mortalidade_infantil'] = (
    (df_mortalidade_infantil['obitos_0_364'] / df_mortalidade_infantil['nascidos_vivos']) * 1000
).replace([float('inf'), -float('inf')], float('nan'))

df_mortalidade_infantil['taxa_mortalidade_pos_neonatal'] = (
    (df_mortalidade_infantil['obitos_28_364'] / df_mortalidade_infantil['nascidos_vivos']) * 1000
).replace([float('inf'), -float('inf')], float('nan'))

df_mortalidade_infantil.to_csv('tabelas_finais//mortalidade_infantil_pos_neonatal_total_bairro_ano.csv', index=False)
df_mortalidade_infantil.head()

# %%
df_mortalidade_infantil_anual = df_mortalidade_infantil[['ano','obitos_0_364','obitos_28_364','nascidos_vivos']].groupby(by='ano').sum()
df_mortalidade_infantil_anual['taxa_mortalidade_infantil'] = (df_mortalidade_infantil_anual['obitos_0_364']/df_mortalidade_infantil_anual['nascidos_vivos'])*1000
df_mortalidade_infantil_anual['taxa_mortalidade_pos_neonatal'] = (df_mortalidade_infantil_anual['obitos_28_364']/df_mortalidade_infantil_anual['nascidos_vivos'])*1000
df_mortalidade_infantil_anual.to_csv('tabelas_finais//mortalidade_infantil_pos_neonatal_total_por_ano.csv')
df_mortalidade_infantil_anual

# %%
serie_temporal(df_mortalidade_infantil_anual,'ano','taxa_mortalidade_pos_neonatal','Taxa de mortalidade pós-neonatal (28-364 dias) por ano',
               nome_arquivo='taxa_mortalidade_pos_neonatal_ano', fonte_dados=fonte_datasus_bairro)

# %% [markdown]
# <!-- nota-curadoria:taxa_mortalidade_pos_neonatal_ano -->
# **Nota de curadoria:** Ao longo da série, o indicador apresenta oscilações, com valores mais elevados no início do período e redução até 2020, quando atingiu 3,69 óbitos por mil nascidos vivos. A partir de 2021, observa-se retomada dos valores, chegando a 4,35 em 2024 e 4,24 em 2025. A comparação entre os anos permite identificar mudanças no comportamento desse componente da mortalidade infantil e verificar como sua trajetória se relaciona às variações observadas na taxa de mortalidade infantil total.

# %% [markdown]
# ###### 🗺️ Mapa por bairro (2025)

# %%
df_mortalidade_infantil_mapa = df_mortalidade_infantil[df_mortalidade_infantil['ano'].astype(str) == '2025'].copy()
df_mortalidade_infantil_mapa.to_csv('tabelas_finais//tabela_mapa_mortalidade_infantil_2025.csv', index=False)

# mapa_coropletico_bairros(
#     df_mortalidade_infantil_mapa, coluna_valor='obitos_28_364', titulo='Óbitos pós-neonatais (28-364 dias) por bairro (2025)',
#     nome_arquivo='mapa_obitos_pos_neonatal_bairro_2025', chave='codigo',
#     cmap=_CORES_TEMA_MAPA['mortalidade'],
#     bins=[1, 2, 4, 8], legenda_titulo='Óbitos', fonte_dados=fonte_datasus_bairro,
# )
mapa_coropletico_bairros(
    df_mortalidade_infantil_mapa, coluna_valor='taxa_mortalidade_pos_neonatal', titulo='Taxa de mortalidade pós-neonatal (28-364 dias) por bairro (2025)',
    nome_arquivo='mapa_taxa_mortalidade_pos_neonatal_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['mortalidade'],
    legenda_titulo='Taxa por mil NV', fonte_dados=fonte_datasus_bairro,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_taxa_mortalidade_pos_neonatal_bairro_2025 -->
# **Nota de curadoria:** A taxa permite comparar os bairros considerando o número de nascidos vivos de cada território. Em 2025, os maiores valores ocorreram em Cidade Nova (48,78 por mil), Camorim (33,33) e Barra de Guaratiba (20,41). Esses valores correspondem a poucos registros de óbitos: 2 em Cidade Nova, 1 em Camorim e 1 em Barra de Guaratiba. A leitura conjunta da taxa com o número de óbitos e de nascidos vivos é importante para contextualizar as diferenças entre os territórios, especialmente nos bairros com menor número de nascimentos.

# %% [markdown]
# ##### Total (0 a 364 dias)

# %%
serie_temporal(df_mortalidade_infantil_anual,'ano','taxa_mortalidade_infantil','Taxa de mortalidade infantil (0-364 dias) por ano',
               nome_arquivo='taxa_mortalidade_infantil_ano', fonte_dados=fonte_datasus_bairro)

# %% [markdown]
# <!-- nota-curadoria:taxa_mortalidade_infantil_ano -->
# **Nota de curadoria:** A série histórica apresenta oscilações entre 2006 e 2025, com redução até 2017, quando atingiu 11,26 óbitos por mil nascidos vivos. A partir de 2018, observa-se uma retomada gradual, chegando a 12,35 em 2024 e 12,33 em 2025. A comparação ao longo do período permite identificar mudanças no comportamento do indicador e relacioná-las às variações no número de óbitos e de nascidos vivos. A trajetória também pode ser analisada em conjunto com os diferentes componentes da mortalidade na primeira infância.

# %% [markdown]
# ###### 🗺️ Mapa por bairro (2025)

# %%
mapa_coropletico_bairros(
    df_mortalidade_infantil_mapa, coluna_valor='obitos_0_364', titulo='Óbitos infantis (0-364 dias) por bairro (2025)',
    nome_arquivo='mapa_mortalidade_infantil_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['mortalidade'],
    bins=[2, 5, 10, 20], legenda_titulo='Óbitos', fonte_dados=fonte_datasus_bairro,
)
mapa_coropletico_bairros(
    df_mortalidade_infantil_mapa, coluna_valor='taxa_mortalidade_infantil', titulo='Taxa de mortalidade infantil (0-364 dias) por bairro (2025)',
    nome_arquivo='mapa_taxa_mortalidade_infantil_bairro_2025', chave='codigo',
    cmap=_CORES_TEMA_MAPA['mortalidade'],
    legenda_titulo='Taxa por mil NV', fonte_dados=fonte_datasus_bairro,
)

# %% [markdown]
# <!-- nota-curadoria:mapa_mortalidade_infantil_bairro_2025 -->
# **Nota de curadoria:** Em 2025, foram registrados 724 óbitos infantis nos bairros analisados. Santa Cruz concentrou 53 registros, seguida por Campo Grande, com 40, e Jacarepaguá, com 32. Em 37 dos 167 bairros não houve registro de óbitos. Como os números variam também conforme o tamanho da população de nascidos vivos, a comparação entre os bairros ganha contexto quando relacionada à respectiva taxa de mortalidade infantil.

# %% [markdown]
# <!-- nota-curadoria:mapa_taxa_mortalidade_infantil_bairro_2025 -->
# **Nota de curadoria:** Em 2025, alguns bairros apresentaram taxas elevadas mesmo com poucos registros de óbitos. Em Cidade Nova, foram 2 óbitos entre 42 nascidos vivos, resultando em 47,62 óbitos por mil nascidos vivos. Em Camorim, 1 óbito entre 35 nascidos vivos correspondeu a 28,57 por mil, enquanto em Pitangueiras foram 2 óbitos entre 76 nascidos vivos, com taxa de 26,32 por mil. Esses exemplos mostram como o número de nascidos vivos influencia a taxa e reforçam a importância de analisá-la junto aos valores absolutos.

# %% [markdown]
# ### 🥗 DataSus - SISVAN

# %% [markdown]
# Percentual de crianças de 0 a 5 anos (fase da vida "Criança (de 0 a 5 anos)" do SISVAN) com sobrepeso/obesidade e desnutrição, agregado por ano (fonte: SISVAN).

# %%
fonte_sisvan = 'SISVAN/DATASUS'

df_desnutricao = pd.read_csv("dados_locais/tratados/desnutrição.csv", index_col=0)
df_desnutricao.tail()

# %%
df_desnutricao['peso_muito_baixo_percentual'] = df_desnutricao['peso_muito_baixo_percentual'].apply(convert_numeric_safe)
df_desnutricao['peso_baixo_percentual'] = df_desnutricao['peso_baixo_percentual'].apply(convert_numeric_safe)
df_desnutricao['Percent. baixo peso total'] = df_desnutricao['peso_muito_baixo_percentual'] + df_desnutricao['peso_baixo_percentual']
df_desnutricao.to_csv('tabelas_finais/sisvan_desnutricao_por_ano.csv')
serie_temporal(df_desnutricao,tempo='ano',valor='Percent. baixo peso total', titulo='Percentual de crianças de 0 a 5 anos com baixo peso - SISVAN',
               nome_arquivo='sisvan_desnutricao_percentual_por_ano', fonte_dados=fonte_sisvan)

# %% [markdown]
# <!-- nota-curadoria:sisvan_desnutricao_percentual_por_ano -->
# **Nota de curadoria:** Ao longo da série, o percentual de crianças com baixo peso para a idade (desnutrição) apresentou oscilações, permanecendo na maior parte dos anos entre 3% e 7%. O principal destaque ocorreu em 2018, quando o indicador atingiu 15,5%, valor muito acima dos outros anos. Após esse pico, o percentual retorna a níveis mais próximos do padrão da série, chegando a 7,5% em 2025. O valor de 2018 se destaca como um ponto fora do comportamento geral e merece atenção ao ser analisado.

# %%
df_sobrepeso = pd.read_csv("dados_locais/tratados/sobrepeso.csv", index_col=0)
df_sobrepeso.head()

# %%
df_sobrepeso['sobrepeso_percentual'] = df_sobrepeso['sobrepeso_percentual'].apply(convert_numeric_safe)
df_sobrepeso['obesidade_percentual'] = df_sobrepeso['obesidade_percentual'].apply(convert_numeric_safe)
df_sobrepeso['Percent. sobrepeso total'] = df_sobrepeso['sobrepeso_percentual'] + df_sobrepeso['obesidade_percentual']
df_sobrepeso.to_csv('tabelas_finais/sisvan_sobrepeso_por_ano.csv')
serie_temporal(df_sobrepeso,tempo='ano',valor='Percent. sobrepeso total', titulo='Percentual de crianças de 0 a 5 anos com sobrepeso e obesidade - SISVAN',
               nome_arquivo='sisvan_sobrepeso_percentual_por_ano', fonte_dados=fonte_sisvan)

# %% [markdown]
# <!-- nota-curadoria:sisvan_sobrepeso_percentual_por_ano -->
# **Nota de curadoria:** O percentual de crianças com sobrepeso apresentou oscilações ao longo da série. O indicador cresce até atingir seu maior valor em 2013, com 21,48%, e depois passa a apresentar redução, chegando a 12,30% em 2021. A partir de 2022, observa-se nova elevação, alcançando 16,89% em 2025.

# %%
serie_temporal(df_sobrepeso,tempo='ano',valor='obesidade_percentual', titulo='Percentual de crianças de 0 a 5 anos com obesidade - SISVAN',
               nome_arquivo='sisvan_obesidade_percentual_por_ano', fonte_dados=fonte_sisvan)

# %% [markdown]
# <!-- nota-curadoria:sisvan_obesidade_percentual_por_ano -->
# **Nota de curadoria:** O percentual de crianças com obesidade, semelhante ao com sobrepeso, também apresentou oscilações ao longo da série. Após crescimento entre 2008 e 2013, o indicador atingiu seu maior valor em 2013, com 11,36%. Nos anos seguintes houve tendência de redução, chegando a 5,36% em 2020. A partir de 2022, os valores permaneceram relativamente estáveis, com leve aumento recente, alcançando 7,34% em 2025. O valor de 2009, de 0,07%, aparece muito abaixo do restante da série e deve ser interpretado com cautela.

# %% [markdown]
# ### 💉 Cobertura Vacinal EPI

# %% [markdown]
# Cobertura vacinal (%) por imunobiológico, série histórica do EPI/SVS-Rio (2016-2026).
#
# Notas:
# - Cobertura acima de 100% é esperada em dados administrativos de vacinação (numerador de doses aplicadas pode incluir população fora do denominador estimado) — não é um erro de cálculo.
# - 2026 é um ano ainda em curso (dados parciais); comparar com cautela contra os anos fechados.

# %%
fonte_cobertura_vacinal = 'EPI/SVS-Rio, cobertura vacinal por imunobiológico'

df_cobertura_vacinal = carrega_cobertura_vacinal('dados_locais//vacinacao//serie_historica_cobertura_vacinal.csv')
df_cobertura_vacinal_wide = df_cobertura_vacinal.pivot(index='ano', columns='imunobiologico', values='cobertura').reset_index()
df_cobertura_vacinal_wide.to_csv('tabelas_finais//cobertura_vacinal_epi_por_ano.csv', index=False)
df_cobertura_vacinal_wide.head()

# %%
# De volta em 2026-09-29 (specs/2026-09-29_alinhamento_pdf_site D2; antes comentada, E1): o site já desenhava a série
colunas_vacinas = {c: c for c in df_cobertura_vacinal_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_cobertura_vacinal_wide,
    tempo='ano',
    colunas=colunas_vacinas,
    titulo='Cobertura vacinal por imunobiológico - Rio de Janeiro (2016-2026)',
    nome_arquivo='cobertura_vacinal_epi_ano',
    ylabel='Cobertura (%)',
    legend_title='Imunobiológico',
    figsize=(14,7), fonte_dados=fonte_cobertura_vacinal,
)

# %% [markdown]
# <!-- nota-curadoria:cobertura_vacinal_epi_ano -->
# **Nota de curadoria:** A evolução da cobertura vacinal na cidade do Rio de Janeiro traz uma trajetória com uma elevada cobertura para grande parte dos imunizantes até 2018, momento que se inicia uma redução entre os anos de 2019 e 2022. A partir de 2023 observa-se recuperação das coberturas, especialmente para pneumocócica 10-valente, poliomielite, meningocócica C, rotavírus e primeira dose da tríplice viral. Entretanto, a recuperação não é homogênea entre os imunizantes, permanecendo níveis baixos em vacinas como DTP de primeiro reforço, hepatite A e segunda dose da tríplice viral, chamando atenção para o cuidado com as doses de reforço.

# %% [markdown]
# Comparativo da cobertura vacinal por imunobiológico nos anos de 2016, 2019, 2022 e 2025.

# %%
anos_comparacao = [2016, 2019, 2022, 2025]
ordem_vacinas = [c for c in df_cobertura_vacinal_wide.columns if c != 'ano']

df_cobertura_comparacao = df_cobertura_vacinal[df_cobertura_vacinal['ano'].isin(anos_comparacao)].copy()
df_cobertura_comparacao['ano'] = df_cobertura_comparacao['ano'].astype(str)
df_cobertura_comparacao.to_csv('tabelas_finais//cobertura_vacinal_epi_comparativo_anos.csv', index=False)
df_cobertura_comparacao.head()

# %%
grafico_barra_agrupado(
    df_cobertura_comparacao,
    categoria='ano',
    valor='cobertura',
    agrupador='imunobiologico',
    titulo='Cobertura vacinal por imunobiológico - anos selecionados (2016, 2019, 2022, 2025)',
    nome_arquivo='cobertura_vacinal_epi_comparativo_anos',
    ylabel='Cobertura (%)',
    legend_title='Imunobiológico',
    ordem_categoria=[str(a) for a in anos_comparacao],
    ordem_agrupador=ordem_vacinas,
    rotacao_x=0,
    figsize=(16,7), fonte_dados=fonte_cobertura_vacinal,
)

# %% [markdown]
# <!-- nota-curadoria:cobertura_vacinal_epi_comparativo_anos -->
# **Nota de curadoria:** A cobertura vacinal no município do Rio de Janeiro quando analisada comparando-se os anos apresenta uma trajetória marcada por um patamar relativamente elevado e heterogêneo no início da série, uma redução generalizada que atinge seu ponto mais baixo em 2022e e uma recuperação observada a partir de 2023, ficando mais evidente em 2025. Entretanto, a recuperação não é uniforme entre os imunobiológicos, permanecendo baixas em coberturas de algumas doses de reforço/esquema vacinal.

# %% [markdown]
# ### 🎓 PNAD Contínua, Censo Escolar e INEP

# %% [markdown]
# Frequência e taxa de frequência escolar (Censo 2022, IBGE/SIDRA) e matrículas (Censo Escolar/INEP), 0 a 5 anos.

# %% [markdown]
# #### Frequência escolar e taxa de frequência de 0 a 5 anos (IBGE SIDRA, Censo 2022)
#
# Idade simples, por raça/cor e sexo. Faixa 0 a 5 anos (`specs/2026-09-29_pendencias` D9): a tabela 10056 (taxa) vai
# até 6 anos, que fica de fora. **Taxa (D14):** a publicada pelo IBGE (10056) para cada grupo e idade; os agregados --
# "Total 0 a 5 anos" e "Amarela e indígena" (E12/D15) -- somam taxa × população (9606) e dividem pela população. Não
# se divide frequentam (10057) por população (9606): as tabelas vêm de bases diferentes do Censo e a razão passa de
# 100% em alguns grupos. Até 2026-09-29 havia aqui também um gráfico rotulado "PNAD Contínua" que trazia, na verdade,
# a coluna Total da 10056 (D16, E15) -- substituído pela taxa total por idade abaixo.

# %%
fonte_sidra_educacao = 'Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057)'

df_sidra_freq_raca = carrega_sidra_longo('dados_locais//ibge_sidra//Educacao_freq_escolar_ate5//tabela10057_frequencia_escola_raca_cor.csv', coluna_corte='Cor ou raça')
df_sidra_freq_sexo = carrega_sidra_longo('dados_locais//ibge_sidra//Educacao_freq_escolar_ate5//tabela10057_frequencia_escola_sexo.csv', coluna_corte='Sexo')
df_sidra_taxa_raca = carrega_sidra_longo('dados_locais//ibge_sidra//Educacao_freq_escolar_ate6//tabela10056_taxa_frequencia_raca_cor.csv', coluna_corte='Cor ou raça')
df_sidra_taxa_sexo = carrega_sidra_longo('dados_locais//ibge_sidra//Educacao_freq_escolar_ate6//tabela10056_taxa_frequencia_sexo.csv', coluna_corte='Sexo')

df_sidra_freq_raca.pivot(index='idade', columns='Cor ou raça', values='valor').to_csv('tabelas_finais//sidra_frequencia_escola_0_5_raca_2022.csv')
df_sidra_freq_sexo.pivot(index='idade', columns='Sexo', values='valor').to_csv('tabelas_finais//sidra_frequencia_escola_0_5_sexo_2022.csv')
# D14/D15: taxa 0 a 5 anos, com "Total 0 a 5 anos" e "Amarela e indígena" agregados de taxa × população (9606).
# Nomes de arquivo mantidos (`_0_6_`: chaves do texto curado, do crosswalk e do site)
df_taxa_freq_raca = taxa_frequencia_0_a_5(df_sidra_taxa_raca, df_censo_sidra_raca, 'Cor ou raça',
                                          agrupa={'Amarela e indígena': ['Amarela', 'Indígena']})
df_taxa_freq_sexo = taxa_frequencia_0_a_5(df_sidra_taxa_sexo, df_censo_sidra_sexo, 'Sexo')
assert (df_taxa_freq_raca.drop(columns='idade').max() <= 100).all() and (df_taxa_freq_sexo.drop(columns='idade').max() <= 100).all()
df_taxa_freq_raca.to_csv('tabelas_finais//sidra_taxa_frequencia_0_6_raca_2022.csv', index=False)
df_taxa_freq_sexo.to_csv('tabelas_finais//sidra_taxa_frequencia_0_6_sexo_2022.csv', index=False)
df_taxa_freq_raca

# %%
_ORDEM_IDADE_SIDRA_0_5 = ['0 ano', '1 ano', '2 anos', '3 anos', '4 anos', '5 anos']

grafico_barra_agrupado(
    df_sidra_freq_raca[df_sidra_freq_raca['Cor ou raça'] != 'Total'],
    categoria='idade', valor='valor', agrupador='Cor ou raça',
    titulo='Crianças de até 5 anos que frequentam escola/creche, por idade e raça/cor - Rio de Janeiro (Censo 2022)',
    nome_arquivo='sidra_frequencia_escola_0_5_raca_2022', ylabel='Pessoas', legend_title='Raça/cor',
    ordem_categoria=_ORDEM_IDADE_SIDRA_0_5, fonte_dados=fonte_sidra_educacao,
)

# %% [markdown]
# <!-- nota-curadoria:sidra_frequencia_escola_0_5_raca_2022 -->
# **Nota de curadoria:** Os dados do Censo Demográfico 2022 permitem analisar a frequência à escola/creche entre crianças de 0 a 5 anos, considerando idade e raça/cor. O número de crianças frequentando escola/creche aumenta conforme a idade, passando de 4.358 entre crianças de 0 ano para 66.163 aos 5 anos. No total do recorte, foram registradas 233.509 crianças, sendo 104.981 brancas, 96.352 pardas e 31.757 pretas. A organização dos dados por idade e raça/cor permite comparar a participação dos diferentes grupos ao longo da primeira infância e relacionar esse indicador a outros recortes educacionais e demográficos.

# %%
grafico_barra_agrupado(
    df_sidra_freq_sexo[df_sidra_freq_sexo['Sexo'] != 'Total'],
    categoria='idade', valor='valor', agrupador='Sexo',
    titulo='Crianças de até 5 anos que frequentam escola/creche, por idade e sexo - Rio de Janeiro (Censo 2022)',
    nome_arquivo='sidra_frequencia_escola_0_5_sexo_2022', ylabel='Pessoas', legend_title='Sexo',
    ordem_categoria=_ORDEM_IDADE_SIDRA_0_5, fonte_dados=fonte_sidra_educacao,
)

# %% [markdown]
# <!-- nota-curadoria:sidra_frequencia_escola_0_5_sexo_2022 -->
# **Nota de curadoria:** Os dados do Censo Demográfico 2022 permitem analisar a frequência à escola/creche entre crianças de 0 a 5 anos segundo sexo e idade. O número de crianças frequentando aumenta ao longo das idades, passando de 4.358 aos 0 anos para 66.163 aos 5 anos. No total, foram registradas 120.304 crianças do sexo masculino e 113.205 do sexo feminino. A comparação por idade permite observar diferenças entre os sexos ao longo da primeira infância e relacionar esse recorte ao número total de crianças frequentando escola/creche. Os dados também podem ser analisados junto às taxas de frequência escolar por sexo.

# %%
# populacao-referencia D3: item do catálogo "Crianças até 6 anos frequentando escola/creche (geral)" --
# o total (todas as raças e sexos) por idade. A tabela 10057 vai só até 5 anos (faixa real 0 a 5).
df_sidra_freq_total = df_sidra_freq_sexo[df_sidra_freq_sexo['Sexo'] == 'Total'].copy()
df_sidra_freq_total = (df_sidra_freq_total[df_sidra_freq_total['idade'] != 'Total'][['idade', 'valor']]
                       .rename(columns={'valor': 'Crianças'}))
assert df_sidra_freq_total['Crianças'].sum() == 233509
df_sidra_freq_total.to_csv('tabelas_finais//sidra_frequencia_escola_0_5_total_2022.csv', index=False)
grafico_barra(df_sidra_freq_total, categoria='idade', valor='Crianças',
              titulo='Crianças de 0 a 5 anos que frequentam escola/creche, por idade - Rio de Janeiro (Censo 2022)',
              nome_arquivo='sidra_frequencia_escola_0_5_total_2022', fonte_dados=fonte_sidra_educacao)

# %%
# D15: amarela e indígena (89 a 125 crianças por idade, somadas) fora das barras por idade; o agregado de 0 a 5 anos
# vai na nota da fonte e na tabela
_taxa_amarela_indigena = df_taxa_freq_raca.set_index('idade').loc['Total 0 a 5 anos', 'Amarela e indígena']
_taxa_amarela_indigena_txt = f'{_taxa_amarela_indigena:.1f}'.replace('.', ',')
grafico_barra_agrupado(
    df_taxa_freq_raca[df_taxa_freq_raca['idade'] != 'Total 0 a 5 anos']
        .melt(id_vars='idade', value_vars=['Branca', 'Parda', 'Preta'], var_name='Cor ou raça', value_name='valor'),
    categoria='idade', valor='valor', agrupador='Cor ou raça',
    titulo='Taxa de frequência escolar bruta (0 a 5 anos), por idade e raça/cor - Rio de Janeiro (Censo 2022)',
    nome_arquivo='sidra_taxa_frequencia_0_6_raca_2022', ylabel='Taxa (%)', legend_title='Raça/cor',
    ordem_categoria=_ORDEM_IDADE_SIDRA_0_5,
    fonte_dados=f'{fonte_sidra_educacao}. Nota: amarela e indígena (grupos pequenos) só no total de 0 a 5 anos: '
                f'{_taxa_amarela_indigena_txt}%',
)

# %% [markdown]
# <!-- nota-curadoria:sidra_taxa_frequencia_0_6_raca_2022 -->
# **Nota de curadoria:** A taxa de frequência escolar bruta aumenta conforme a idade, passando de 8,04% entre crianças de 0 ano para 90,57% aos 5 anos. No conjunto de 0 a 5 anos, a taxa foi de 59,30%, com diferenças entre os grupos de raça/cor: 62,26% entre crianças pretas, 59,10% entre pardas e 58,70% entre brancas. A comparação por idade permite analisar como a frequência escolar se modifica ao longo da primeira infância e como esse comportamento varia entre os grupos de raça/cor. Os dados podem ser relacionados ao número absoluto de crianças frequentando escola/creche para complementar a análise.

# %%
grafico_barra_agrupado(
    df_taxa_freq_sexo[df_taxa_freq_sexo['idade'] != 'Total 0 a 5 anos']
        .melt(id_vars='idade', value_vars=['Homens', 'Mulheres'], var_name='Sexo', value_name='valor'),
    categoria='idade', valor='valor', agrupador='Sexo',
    titulo='Taxa de frequência escolar bruta (0 a 5 anos), por idade e sexo - Rio de Janeiro (Censo 2022)',
    nome_arquivo='sidra_taxa_frequencia_0_6_sexo_2022', ylabel='Taxa (%)', legend_title='Sexo',
    ordem_categoria=_ORDEM_IDADE_SIDRA_0_5, fonte_dados=fonte_sidra_educacao,
)

# %% [markdown]
# <!-- nota-curadoria:sidra_taxa_frequencia_0_6_sexo_2022 -->
# **Nota de curadoria:** A taxa de frequência escolar bruta aumenta conforme a idade, passando de 8,04% aos 0 anos para 90,57% aos 5 anos. No conjunto de 0 a 5 anos, a taxa foi de 59,81% entre os meninos e 58,78% entre as meninas. A diferença entre os sexos varia ao longo das idades: aos 4 anos, a taxa foi de 82,51% entre meninos e 83,35% entre meninas, enquanto aos 5 anos foi de 91,56% entre meninos e 89,49% entre meninas. A comparação por idade e sexo permite analisar como a frequência escolar se modifica ao longo da primeira infância.

# %% [markdown]
# #### Taxa de frequência escolar por idade (total, Censo 2022)
#
# D16 (`specs/2026-09-29_pendencias`, E15): substitui o gráfico "PNAD Contínua" (`pnad_frequencia_escolar_por_idade`,
# lido de `dados_locais/educacao/pnad_taxa_frequencia_escolar_ate_6_anos.csv`), que trazia exatamente a coluna Total
# da tabela 10056 do Censo 2022 com a fonte errada. Mesmo dado, fonte certa, 0 a 5 anos.

# %%
df_taxa_freq_total = (df_taxa_freq_sexo[['idade', 'Total']].rename(columns={'Total': 'Taxa (%)'}))
df_taxa_freq_total.to_csv('tabelas_finais//sidra_taxa_frequencia_0_5_total_2022.csv', index=False)
grafico_barra(df=df_taxa_freq_total[df_taxa_freq_total['idade'] != 'Total 0 a 5 anos'], categoria='idade', valor='Taxa (%)',
              titulo='Taxa de frequência escolar bruta por idade, 0 a 5 anos - Rio de Janeiro (Censo 2022)',
              nome_arquivo='sidra_taxa_frequencia_0_5_total_2022', fonte_dados=fonte_sidra_educacao)

# %% [markdown]
# <!-- nota-curadoria:sidra_taxa_frequencia_0_5_total_2022 -->
# **Nota de curadoria:** A frequência escolar na primeira infância apresenta uma trajetória de crescimento acelerado à medida que a idade da criança vai aumentando. Esse movimento pode ser explicado pela necessidade de retorno dos pais, em especial das mães, ao mercado de trabalho e garantia do direito constitucional ao desenvolvimento para as crianças. A partir dos 4 anos, quando há a obrigatoriedade legal da pré-escola a taxa sobe para cerca de 83%, atingindo 90% aos 5 anos. A despeito do alto percentual, é um ponto de atenção ter uma déficit de 17% e 10% de crianças em idade escolar obrigatória que não a estejam frequentando.

# %% [markdown]
# #### Matrículas e taxa de atendimento de 0 a 5 anos (Censo Escolar/INEP, 2007-2025)
#
# **Nota de método** (`specs/2026-09-24_populacao-referencia/matriculas/`):
# - **Fonte:** microdados do Censo Escolar da Educação Básica (INEP), município do Rio de Janeiro
#   (`CO_MUNICIPIO` 3304557), lidos dos ZIPs originais por `carrega_censo_escolar_matriculas`. O extrato
#   `dados_locais/educacao/inep_matriculas_rio.csv` (ano × dependência) deixa o notebook rodar sem os ZIPs.
# - **Só contagens por escola:** desde a adequação à LGPD o INEP publica uma linha por escola, com as
#   matrículas já agregadas em faixas de idade (e republicou os anos anteriores nesse formato). Não há dado
#   por aluno.
# - **0 a 5 anos, não 0 a 6:** a faixa de 6 anos vem misturada com 7-10 (`QT_MAT_BAS_6_10`), então "até 6
#   anos" exato não é calculável com os dados abertos. Usa-se 0-3 + 4-5 (`QT_MAT_BAS_0_3` + `QT_MAT_BAS_4_5`),
#   a faixa da educação infantil (creche e pré-escola) por idade, não por etapa.
# - **Idade na data de referência do Censo Escolar** (última quarta-feira de maio). As colunas de 2025 com
#   idade em 31/03 (`_REF_31_03`) não entram, porque não existem nos outros anos.
# - **Troca da série antiga:** o CSV anterior (`censo_escolar_matriculas_ate_6anos.csv`, 2007-2020, sem
#   registro de como foi gerado) tinha 205.371 em 2020, contra 247.133 de 0-5 nos microdados. Nenhuma
#   combinação óbvia reproduz o número antigo, e juntar as duas séries criaria um degrau artificial; por
#   isso a série inteira foi reconstruída da mesma fonte.
# - **2021 é um vale** (pandemia), e **2025 vem em tabelas separadas** no ZIP (`Tabela_Matricula`), com as
#   mesmas colunas. Escolas paralisadas/extintas não têm matrícula de 0-5 (conferido em 2020).
# - Pública = federal + estadual + municipal (`TP_DEPENDENCIA` 1-3); privada = 4.

# %%
fonte_matriculas = 'Censo Escolar da Educação Básica (INEP), microdados'
fonte_taxa_atendimento = 'Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde'

df_matriculas_rede = carrega_censo_escolar_matriculas(range(2007, 2026))
df_matriculas = resume_matriculas_0_a_5(df_matriculas_rede, carrega_populacao_ripsa())
assert len(df_matriculas) == 19
assert (df_matriculas['matriculas'] == df_matriculas['matriculas_0_a_3'] + df_matriculas['matriculas_4_a_5']).all()
assert (df_matriculas['matriculas'] == df_matriculas['matriculas_publica'] + df_matriculas['matriculas_privada']).all()
assert df_matriculas.set_index('ano').loc[[2020, 2025], 'matriculas'].tolist() == [247133, 230284]
df_matriculas.to_csv('tabelas_finais//matriculas_0_a_5_por_ano.csv', index=False)
df_matriculas

# %%
serie_temporal(df_matriculas, 'ano', 'matriculas', 'Matrículas de crianças de 0 a 5 anos por ano',
               nome_arquivo='matriculas_0_a_5_por_ano', fonte_dados=fonte_matriculas)

# %%
serie_temporal_multipla(
    df_matriculas, tempo='ano', colunas={'0 a 3 anos (creche)': 'matriculas_0_a_3', '4 a 5 anos (pré-escola)': 'matriculas_4_a_5'},
    titulo='Matrículas de crianças de 0 a 5 anos, por faixa de idade', nome_arquivo='matriculas_0_a_5_creche_pre_por_ano',
    ylabel='Matrículas', legend_title='Faixa de idade', fonte_dados=fonte_matriculas,
)

# %%
serie_temporal_multipla(
    df_matriculas, tempo='ano', colunas={'Rede pública': 'matriculas_publica', 'Rede privada': 'matriculas_privada'},
    titulo='Matrículas de crianças de 0 a 5 anos, por rede', nome_arquivo='matriculas_0_a_5_rede_por_ano',
    ylabel='Matrículas', legend_title='Rede', fonte_dados=fonte_matriculas,
)

# %% [markdown]
# **Nota metodológica da taxa de atendimento** (decisão D7 de `matriculas/`; a nota geral de população de
# referência está no início da seção Censo 2022):
# 1. **Denominador:** estimativas Ripsa/MS 2000-2025 (Nota Técnica Ripsa nº 01/2025), população em 1º de
#    julho, por idade simples, ajustada às Projeções do IBGE (revisão 2024); consulta ao Tabnet de
#    2026-09-24 (coluna `data_consulta` do extrato).
# 2. **Por que não o Censo 2022:** ele conta 379.609 crianças de 0-5 no Rio contra 439.907 da Ripsa (+16%),
#    com a maior diferença em menores de 1 ano (sub-registro de crianças pequenas, corrigido pelo IBGE). Com
#    o Censo, a taxa de 2022 seria **64,9%** (0-3: 47,8%; 4-5: 94,4%) em vez de 56,0%; números do Censo 2022
#    no notebook (SIDRA) não se comparam diretamente com esta taxa.
# 3. **Taxa bruta:** o numerador conta matrículas em escolas do município, inclusive de crianças que moram
#    em outros municípios; o denominador são os residentes. As datas de referência diferem (fim de maio e 1º
#    de julho).
# 4. **Revisões:** a Ripsa revisa as estimativas todo ano, então uma consulta nova pode mudar anos passados.
# 5. **Diferença com a taxa de frequência do Censo 2022** (acima; até 2026-09-29 rotulada "PNAD" por engano, D16): aquela
#    é declarada no domicílio; esta é registro administrativo ÷ estimativa. Ordem de grandeza coerente (~83% aos 4 anos
#    e ~91% aos 5).
# 6. **Metas do PNE** (Lei 13.005/2014, Meta 1): 50% de atendimento em creche (0-3) e universalização da
#    pré-escola (4-5), como linhas de referência no gráfico.

# %%
serie_temporal_multipla(
    df_matriculas, tempo='ano',
    colunas={'0 a 3 anos (creche)': 'taxa_atendimento_0_a_3', '4 a 5 anos (pré-escola)': 'taxa_atendimento_4_a_5',
             '0 a 5 anos': 'taxa_atendimento_0_a_5'},
    titulo='Taxa bruta de atendimento escolar de 0 a 5 anos (%)', nome_arquivo='taxa_atendimento_0_a_5_por_ano',
    ylabel='Matrículas por 100 crianças residentes', legend_title='Faixa de idade', fonte_dados=fonte_taxa_atendimento,
    linhas_referencia=[(50, 'Meta PNE creche: 50%'), (100, 'Meta PNE pré-escola: 100%')],
)

# %% [markdown]
# #### Juncao de tabelas por bairro

# %% [markdown]
# Junta nascidos vivos, baixo peso, óbitos de gravidez/puerpério e mortalidade neonatal por bairro-ano.
#
# > **Nota:** não inclui óbitos por raça/cor, causas evitáveis ou cobertura vacinal, que têm granularidades diferentes (raça, ou município-ano).

# %%
lista_dfs = [df_vivos,df_baixo_peso,
             df_obitos_gravidez,df_obitos_puerperio,
             df_neonatal_precoce,df_neonatal_tardia]
df_final = lista_dfs[0].copy()
for i in lista_dfs[1:]:
    df_final = df_final.merge(i,on=['codigo','bairro','ano'],how='outer')
#df_final = df_final[df_final['ano']!='Total']
df_final.drop(columns=['nascidos vivos_x','nascidos vivos_y'],inplace=True)
df_final.to_excel('mapas/tabelas_bairros/dados_datasus_por_bairro.xlsx')
df_final.head()
#pensar testes


# %% [markdown]
# #### Juncao de tabelas municipio

# %% [markdown]
# *(Pendente)* Agregação das tabelas acima ao nível município-ano.

# %% [markdown]
# ---
# ## 🛡️ Proteção
#
# Violência contra crianças de 0 a 5 anos (Sinan NET/Tabnet, por bairro de residência) e violência
# territorial (Data.Rio/IPS, por Região Administrativa). Especificação: `specs/2026-09-23_inclusao_dados_protecao/`.
#
# > **Leitura dos dados — avisos que valem para toda a seção**
# > - Os **vínculos** (mãe, pai, padrasto...) **não são excludentes** e não existe "total de violência
# >   familiar": a mesma notificação pode citar mais de um provável autor. **Nunca somar mãe + pai.**
# >   `outros` = padrasto + irmão(ã) + cônjuge + ex-cônjuge + filho(a) e pode contar uma notificação mais de uma vez.
# > - **2026 é ano parcial** e fica fora das séries de violência familiar (2011-2025). Na lesão autoprovocada,
# >   2026 é o ano de referência (33 dos 40 casos da série).
# > - Possível **quebra de série em 2017** (salto de mães 600 → 1.514 e pais 371 → 1.261): *hipótese* de mudança
# >   de ficha/notificação, **a confirmar com a fonte**.
# > - Contagem absoluta **não é risco**: bairros populosos concentram mais casos. A taxa por 1.000 crianças usa
# >   numerador 0-5 anos e denominador 0-4 anos (Censo 2022) — superestima ~20%, de modo uniforme. No município, a
# >   taxa usa a população de 0 a 5 anos da Ripsa/MS do mesmo ano (A3), sem essa ressalva.
# > - Violência territorial (IPS): dado da **população geral (todas as idades), NÃO específico de crianças nem de jovens**; só 2024.

# %% [markdown]
# ### Violência familiar por vínculo do provável autor

# %%
fonte_sinan = 'Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos'
fonte_sinan_censo = 'Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio)'
fonte_ips = 'Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades)'

ANOS_VF = list(range(2011, 2026))  # 2026 é ano parcial: fora das séries de violência familiar
df_vf = carrega_violencia_familiar('dados_locais/protecao/violencia_familiar', range(2011, 2027))
df_vf_fechado = df_vf[df_vf['ano'].isin(ANOS_VF)]

_tot = df_vf.groupby(['vinculo', 'ano'])['casos'].sum()
assert _tot['mae'].loc[2011:2025].sum() + _tot['mae'][2026] == 15066          # total do bruto (mãe)
assert (_tot['mae'][2017], _tot['mae'][2025], _tot['pai'][2025]) == (1514, 1756, 1404)
assert (_tot['outros'] == df_vf[df_vf['vinculo'].isin(_VINCULOS_OUTROS)].groupby('ano')['casos'].sum()).all()
assert df_vf.groupby('vinculo')['codbairro'].nunique().eq(166).all()          # grade completa, com zeros

# %% [markdown]
# ##### T1 · Município x vínculo x ano

# %%
ordem_vinculos = ['mae', 'pai', 'padrasto', 'irmao', 'conjuge', 'exconjuge', 'filho', 'outros']
df_vf_vinculo_ano = (df_vf_fechado.pivot_table(index='ano', columns='vinculo', values='casos', aggfunc='sum')
                     [ordem_vinculos].reset_index())
df_vf_vinculo_ano.columns.name = None
df_vf_vinculo_ano.to_csv('tabelas_finais/violencia_familiar_por_vinculo_ano.csv', index=False)
df_vf_vinculo_ano

# %% [markdown]
# ##### G1 · Série temporal por vínculo (mãe, pai e outros)
#
# > Os vínculos não se somam. A linha tracejada em 2017 marca a **possível** quebra de série (hipótese, a confirmar).

# %%
serie_temporal_multipla_marcos(
    df_vf_vinculo_ano, tempo='ano', colunas={'Mãe': 'mae', 'Pai': 'pai', 'Outros vínculos': 'outros'},
    titulo='Notificações de violência familiar contra crianças de 0 a 5 anos, por vínculo (2011-2025)',
    nome_arquivo='violencia_familiar_serie_vinculos', marcos={2017: 'possível quebra de série (2017)'},
    ylabel='Notificações', legend_title='Vínculo do provável autor', fonte_dados=fonte_sinan,
)

# %% [markdown]
# ##### A3 · Taxa municipal por 1.000 crianças de 0 a 5 anos, por vínculo (2011-2025)
#
# > Notificações de cada vínculo ÷ população de **0 a 5 anos** do mesmo ano (estimativas Ripsa/MS) × 1.000
# > (`specs/2026-09-24_populacao-referencia`, A3). No município, numerador e denominador têm a mesma faixa (0-5) e o
# > mesmo ano, então a ressalva D9 (numerador 0-5 sobre população 0-4 do Censo) **não se aplica aqui**; ela
# > vale só para as taxas por bairro/RA/CAP mais abaixo. Os vínculos seguem sem soma entre si, e a possível
# > quebra de série de 2017 vale também para a taxa. Fonte da população: nota no início da seção Censo 2022.

# %%
fonte_sinan_ripsa = 'Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 5 anos: estimativas Ripsa/Ministério da Saúde'

df_vf_taxa_municipio = df_vf_vinculo_ano[['ano', 'mae', 'pai', 'outros']].merge(
    populacao_ripsa(carrega_populacao_ripsa(), 0, 5, anos=ANOS_VF).rename(columns={'populacao': 'populacao_0_a_5'}), on='ano')
for _v in ['mae', 'pai', 'outros']:
    df_vf_taxa_municipio = taxa_por_mil(df_vf_taxa_municipio, _v, 'populacao_0_a_5', f'taxa_por_mil_{_v}')
assert len(df_vf_taxa_municipio) == len(ANOS_VF)
assert round(df_vf_taxa_municipio.loc[df_vf_taxa_municipio['ano'] == 2025, 'taxa_por_mil_mae'].item(), 2) == round(1756 / 393073 * 1000, 2)
df_vf_taxa_municipio.to_csv('tabelas_finais/violencia_familiar_taxa_municipio_ano.csv', index=False)

serie_temporal_multipla_marcos(
    df_vf_taxa_municipio, tempo='ano',
    colunas={'Mãe': 'taxa_por_mil_mae', 'Pai': 'taxa_por_mil_pai', 'Outros vínculos': 'taxa_por_mil_outros'},
    titulo='Notificações de violência familiar por 1.000 crianças de 0 a 5 anos, por vínculo (2011-2025)',
    nome_arquivo='violencia_familiar_taxa_municipio_ano', marcos={2017: 'possível quebra de série (2017)'},
    ylabel='Notificações por 1.000 crianças', legend_title='Vínculo do provável autor', fonte_dados=fonte_sinan_ripsa,
)
df_vf_taxa_municipio.round(2)

# %% [markdown]
# ##### T4 e G2 · Composição de "outros"

# %%
componentes_outros = ['padrasto', 'irmao', 'conjuge', 'exconjuge', 'filho']
df_vf_outros_detalhe = df_vf_vinculo_ano[['ano'] + componentes_outros + ['outros']].copy()
assert (df_vf_outros_detalhe[componentes_outros].sum(axis=1) == df_vf_outros_detalhe['outros']).all()
assert df_vf_outros_detalhe.loc[df_vf_outros_detalhe['ano'] == 2025, 'outros'].item() == 110
df_vf_outros_detalhe.to_csv('tabelas_finais/violencia_familiar_outros_detalhe.csv', index=False)

serie_temporal_multipla(
    df_vf_outros_detalhe, tempo='ano',
    colunas={'Padrasto': 'padrasto', 'Irmão(ã)': 'irmao', 'Cônjuge': 'conjuge', 'Ex-cônjuge': 'exconjuge', 'Filho(a)': 'filho'},
    titulo='Vínculos agrupados em "outros" (2011-2025)', nome_arquivo='violencia_familiar_outros_serie',
    ylabel='Notificações', legend_title='Vínculo', fonte_dados=fonte_sinan,
)

# %% [markdown]
# ##### T2 · Por bairro (mãe, pai, outros) x ano

# %%
df_vf_bairro = (df_vf_fechado[df_vf_fechado['vinculo'].isin(['mae', 'pai', 'outros'])]
                .pivot_table(index=['codbairro', 'bairro', 'ano'], columns='vinculo', values='casos').reset_index())
df_vf_bairro.columns.name = None
df_vf_bairro.to_csv('tabelas_finais/violencia_familiar_por_bairro.csv', index=False)
assert df_vf_bairro.groupby('ano')['mae'].sum().loc[2025] == 1756
df_vf_bairro.head()

# %% [markdown]
# ##### 🗺️ Mapas por bairro (M1 mãe 2025, M2 pai 2025, M3 "outros" acumulado 2021-2025)
#
# Contagens absolutas → classes discretas. Mãe e pai em 2025; "outros" tem só ~110 casos em 2025, então usa o
# acumulado 2021-2025.

# %%
df_vf_2025 = df_vf_bairro[df_vf_bairro['ano'] == 2025]
df_vf_outros_acum = (df_vf_bairro[df_vf_bairro['ano'].between(2021, 2025)]
                     .groupby(['codbairro', 'bairro'], as_index=False)['outros'].sum()
                     .rename(columns={'outros': 'outros_2021_2025'}))
assert df_vf_outros_acum['outros_2021_2025'].sum() == df_vf_outros_detalhe[df_vf_outros_detalhe['ano'].between(2021, 2025)]['outros'].sum()

df_vf_2025[['codbairro', 'bairro', 'mae']].to_csv('tabelas_finais/tabela_mapa_violencia_familiar_mae_2025.csv', index=False)
df_vf_2025[['codbairro', 'bairro', 'pai']].to_csv('tabelas_finais/tabela_mapa_violencia_familiar_pai_2025.csv', index=False)
df_vf_outros_acum.to_csv('tabelas_finais/tabela_mapa_violencia_familiar_outros_2021_2025.csv', index=False)

mapa_coropletico_bairros(
    df_vf_2025, coluna_valor='mae', chave='codbairro', bins=[5, 15, 30, 60],
    titulo='Notificações de violência familiar por bairro — mãe (2025)',
    nome_arquivo='mapa_violencia_familiar_mae_bairro_2025', cmap=_CORES_TEMA_MAPA['protecao'], fundo='mapa_oceano_base', zero_branco=True,
    legenda_titulo='Notificações (mãe)', fonte_dados=fonte_sinan,
)
mapa_coropletico_bairros(
    df_vf_2025, coluna_valor='pai', chave='codbairro', bins=[5, 15, 30, 60],
    titulo='Notificações de violência familiar por bairro — pai (2025)',
    nome_arquivo='mapa_violencia_familiar_pai_bairro_2025', cmap=_CORES_TEMA_MAPA['protecao'], fundo='mapa_oceano_base', zero_branco=True,
    legenda_titulo='Notificações (pai)', fonte_dados=fonte_sinan,
)
mapa_coropletico_bairros(
    df_vf_outros_acum, coluna_valor='outros_2021_2025', chave='codbairro', bins=[1, 3, 6, 12],
    titulo='Notificações de violência familiar por bairro — outros vínculos (2021-2025)',
    nome_arquivo='mapa_violencia_familiar_outros_bairro_2021_2025', cmap=_CORES_TEMA_MAPA['protecao'], fundo='mapa_oceano_base', zero_branco=True,
    legenda_titulo='Notificações (outros,\nacumulado 5 anos)', fonte_dados=fonte_sinan,
)

# %% [markdown]
# ##### G3 · Dez bairros com mais notificações (mãe e pai, 2025)
#
# > Ordenado pelo vínculo mãe; mãe e pai aparecem lado a lado, **sem soma**. Contagem absoluta — bairros populosos lideram.

# %%
top10_mae = df_vf_2025.nlargest(10, 'mae')['codbairro']
df_top_bairros = (df_vf_2025[df_vf_2025['codbairro'].isin(top10_mae)]
                  .sort_values('mae', ascending=False)
                  .melt(id_vars=['codbairro', 'bairro'], value_vars=['mae', 'pai'], var_name='vinculo', value_name='notificações'))
df_top_bairros['vinculo'] = df_top_bairros['vinculo'].map({'mae': 'Mãe', 'pai': 'Pai'})
df_top_bairros.to_csv('tabelas_finais/violencia_familiar_top_bairros_2025.csv', index=False)
grafico_barra_agrupado(
    df_top_bairros, categoria='bairro', valor='notificações', agrupador='vinculo',
    titulo='Dez bairros com mais notificações de violência familiar (2025)',
    nome_arquivo='violencia_familiar_top_bairros_2025', ylabel='Notificações', legend_title='Vínculo',
    ordem_categoria=list(df_top_bairros['bairro'].drop_duplicates()), ordem_agrupador=['Mãe', 'Pai'],
    fonte_dados=fonte_sinan,
)

# %% [markdown]
# ##### T3 · Por Região Administrativa e por CAP (casos somados; taxa recalculada depois de somar)

# %%
df_pop_04 = carrega_pop_0_4_bairro()
if 'df_censo' in globals():  # denominador confere com o Censo já carregado na seção Censo 2022
    assert (df_pop_04.set_index('codbairro')['pop_0_4']
            == df_censo.set_index('codbairro')['0 a 4 anos'].reindex(df_pop_04['codbairro'])).all()

df_vf_ra = agrega_violencia_familiar_nivel(df_vf_bairro, df_pop_04, 'ra')
df_vf_ra = df_vf_ra.merge(_bairros_referencia()[['codra', 'regiao_adm']].drop_duplicates('codra'), on='codra', how='left')
df_vf_cap = agrega_violencia_familiar_nivel(df_vf_bairro, df_pop_04, 'cap')
for _df in (df_vf_ra, df_vf_cap):
    assert _df[_df['ano'] == 2025]['mae'].sum() == 1756 and _df[_df['ano'] == 2025]['pop_0_4'].sum() == df_pop_04['pop_0_4'].sum()
df_vf_ra.to_csv('tabelas_finais/violencia_familiar_por_ra.csv', index=False)
df_vf_cap.to_csv('tabelas_finais/violencia_familiar_por_cap.csv', index=False)
df_vf_cap[df_vf_cap['ano'] == 2025]

# %% [markdown]
# ### Notificações de lesão autoprovocada (0 a 5 anos)
#
# > O arquivo cobre **apenas lesão autoprovocada** (não a violência interpessoal total) e não separa menores de 1 ano
# > de 1 a 5 anos. Série muito esparsa: 40 casos em 2018-2026, 33 deles em 2026 (ano parcial). O salto em 2026 pode
# > refletir mudança de registro administrativo — **hipótese, a confirmar com a fonte (SMS/Sinan)**.

# %%
df_autoprov = carrega_sinan_bairro('dados_locais/protecao/notif_viol_ interpes_ autoprovocada_menor_1, 1-5.csv',
                                   'casos', range(2018, 2027))
assert 'Autoprov' in df_autoprov.attrs['filtro']
assert df_autoprov['casos'].sum() == 40 and df_autoprov.loc[df_autoprov['ano'] == 2026, 'casos'].sum() == 33
df_autoprov['ano_parcial'] = df_autoprov['ano'] == 2026
df_autoprov.to_csv('tabelas_finais/notif_autoprovocada_por_bairro_ano.csv', index=False)

df_autoprov_periodos = pd.DataFrame({
    'período': ['2018-2025 (8 anos)', '2026 (ano parcial)'],
    'notificações': [df_autoprov.loc[~df_autoprov['ano_parcial'], 'casos'].sum(), df_autoprov.loc[df_autoprov['ano_parcial'], 'casos'].sum()],
})
assert df_autoprov_periodos['notificações'].tolist() == [7, 33]
grafico_barra(df_autoprov_periodos, 'período', 'notificações',
              'Lesão autoprovocada notificada, 0 a 5 anos: 2018-2025 x 2026',
              nome_arquivo='notif_autoprovocada_antes_2026_vs_2026',
              fonte_dados='Sinan NET/Tabnet (SMS-Rio). 2026 parcial; possível mudança de registro (hipótese)')

# %% [markdown]
# ##### 🗺️ Mapa por bairro (M7 · 2026, ano de referência desta série)

# %%
df_autoprov_2026 = df_autoprov[df_autoprov['ano'] == 2026][['codbairro', 'bairro', 'casos']]
df_autoprov_2026.to_csv('tabelas_finais/tabela_mapa_notif_autoprovocada_2026.csv', index=False)
mapa_coropletico_bairros(
    df_autoprov_2026, coluna_valor='casos', chave='codbairro', bins=[1, 3],
    titulo='Lesão autoprovocada notificada por bairro (2026, ano parcial)',
    nome_arquivo='mapa_notif_autoprovocada_bairro_2026', cmap=_CORES_TEMA_MAPA['protecao'], fundo='mapa_oceano_base', zero_branco=True,
    legenda_titulo='Notificações\n(2026, parcial)', fonte_dados='Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos',
)

# %% [markdown]
# ### Violência territorial por Região Administrativa (Data.Rio/IPS, 2024)
#
# > **Dado geral da população, NÃO específico de crianças ou jovens:** um único ano (2024) e todas as idades.
# > A RA XXI Paquetá não tem dado no IPS ("Sem dado" nos mapas).

# %%
df_terr = carrega_violencia_territorial_ra('dados_locais/protecao/violencia_territorial.xlsx')
terr_municipio = df_terr.attrs['municipio']
assert len(df_terr) == 32 and set(_bairros_referencia()['codra']) - set(df_terr['codra']) == {21}
assert round(terr_municipio['taxa_homicidios'], 3) == 16.663
df_terr_saida = pd.concat([df_terr, pd.DataFrame([{'codra': None, 'regiao_adm': 'MUNICÍPIO DO RIO DE JANEIRO', **terr_municipio}])],
                          ignore_index=True)
df_terr_saida.to_csv('tabelas_finais/violencia_territorial_por_ra_2024.csv', index=False)
df_terr.to_csv('tabelas_finais/tabela_mapa_violencia_territorial_ra_2024.csv', index=False)

indicadores_territoriais = {
    'taxa_homicidios': ('Taxa de homicídios', 'homicidios'),
    'homicidios_acao_policial': ('Homicídios por ação policial', 'homicidios_acao_policial'),
    'homicidios_jovens_negros': ('Homicídios de jovens negros', 'homicidios_jovens_negros'),
}
# só mapas (índice/taxa -> colorbar contínua); sem gráficos de barra por RA. Dado da população geral, não infantil
for coluna, (rotulo, sufixo) in indicadores_territoriais.items():
    mapa_coropletico_bairros(
        df_terr, coluna_valor=coluna, chave='codra', nivel='ra',
        titulo=f'{rotulo} por RA (2024) — população geral', nome_arquivo=f'mapa_violencia_territorial_{sufixo}_ra_2024',
        cmap=_CORES_TEMA_MAPA['protecao'], fundo='mapa_oceano_base',
        legenda_titulo='Taxa (IPS)\ntodas as idades,\nnão só crianças', fonte_dados=fonte_ips,
    )

# %% [markdown]
# ### Taxa de notificações de violência familiar por 1.000 crianças
#
# > **Ressalva D9:** numerador com crianças de 0 a 5 anos (Sinan) e denominador com 0 a 4 anos (Censo 2022) — a taxa
# > superestima ~20%, de forma uniforme, então o *ranking* entre bairros se preserva. "Outros" usa o acumulado
# > 2021-2025 (numerador) sobre a mesma população. Bairros com poucas crianças geram taxas instáveis (D10): a escala
# > de cor é limitada ao percentil 95 (valores maiores aparecem com a cor máxima); a tabela guarda o valor real.
# >
# > **População de referência (`specs/2026-09-24_populacao-referencia`, B3):** o denominador por bairro, RA e CAP é **fixo no
# > Censo 2022** (decisão B1), porque não há população por bairro × idade × ano.
# > - **Anos diferentes:** o numerador é de 2025 (mãe, pai) ou 2021-2025 (outros), e a população é de 2022. A
# >   população de 0 a 5 anos do município caiu ~11% entre 2022 e 2025 (Ripsa: 439.907 → 393.073), então a população
# >   de 2022 tende a ser maior que a de 2025, o que puxa a taxa para baixo.
# > - **O Censo 2022 subconta crianças pequenas:** no município, 0-4 anos soma 310.648 no Censo contra 361.163 na
# >   Ripsa (+16%; nota no início da seção Censo 2022). Com o denominador subcontado, a taxa por bairro tende a ficar
# >   **mais alta** do que ficaria com uma estimativa corrigida.
# > - Os dois efeitos vão em sentidos opostos e não se anulam de forma exata; por isso as taxas por bairro servem para
# >   comparar territórios entre si, não para comparar com a taxa municipal (A3), que usa a Ripsa. Nenhum cálculo muda.

# %%
df_vf_taxa_bairro = (df_vf_2025[['codbairro', 'bairro', 'mae', 'pai']]
                     .rename(columns={'mae': 'casos_mae_2025', 'pai': 'casos_pai_2025'})
                     .merge(df_vf_outros_acum.rename(columns={'outros_2021_2025': 'casos_outros_2021_2025'}), on=['codbairro', 'bairro'])
                     .merge(df_pop_04, on='codbairro'))
for _nome, _casos in [('mae_2025', 'casos_mae_2025'), ('pai_2025', 'casos_pai_2025'), ('outros_2021_2025', 'casos_outros_2021_2025')]:
    df_vf_taxa_bairro = taxa_por_mil(df_vf_taxa_bairro, _casos, 'pop_0_4', f'taxa_por_mil_{_nome}')
assert not np.isinf(df_vf_taxa_bairro.select_dtypes('number')).any().any()
df_vf_taxa_bairro.to_csv('tabelas_finais/violencia_familiar_taxa_por_bairro.csv', index=False)

# D10: bairros com poucas crianças de 0 a 4 anos, sinalizados (não suprimidos)
bairros_pop_pequena = df_vf_taxa_bairro[df_vf_taxa_bairro['pop_0_4'] < 100][['bairro', 'pop_0_4']]
print('Bairros com menos de 100 crianças de 0 a 4 anos (taxa instável):', bairros_pop_pequena.values.tolist())

# %% [markdown]
# ##### 🗺️ Mapas de taxa por bairro (M8-M10) — colorbar contínua (taxa)

# %%
for _nome, _rotulo, _periodo in [('mae_2025', 'mãe', '2025'), ('pai_2025', 'pai', '2025'), ('outros_2021_2025', 'outros vínculos', '2021-2025')]:
    _col = f'taxa_por_mil_{_nome}'
    _lim = _limite_escala_p95(df_vf_taxa_bairro[_col])
    _mapa = df_vf_taxa_bairro[['codbairro', 'bairro', 'pop_0_4', _col]].copy()
    _mapa['taxa_escala_mapa'] = _mapa[_col].clip(upper=_lim)
    _mapa.to_csv(f'tabelas_finais/tabela_mapa_violencia_familiar_taxa_{_nome}.csv', index=False)
    mapa_coropletico_bairros(
        _mapa, coluna_valor='taxa_escala_mapa', chave='codbairro',
        titulo=f'Notificações de violência ({_rotulo}) por 1.000 crianças de 0 a 4 anos ({_periodo})',
        nome_arquivo=f'mapa_violencia_familiar_{_nome.split("_")[0]}_taxa_bairro_{_nome.split("_", 1)[1]}',
        cmap=_CORES_TEMA_MAPA['protecao'], fundo='mapa_oceano_base', legenda_titulo=f'Notificações por\n1.000 crianças 0-4\n(Censo 2022; escala até {_lim})',
        fonte_dados=fonte_sinan_censo,
    )

# %% [markdown]
# ##### 🗺️ Mapas de taxa por Região Administrativa (M11-M13) — colorbar contínua
#
# Casos somados por RA e taxa recalculada sobre a população 0-4 da RA (nunca média de taxas de bairro).

# %%
_ra_2025 = df_vf_ra[df_vf_ra['ano'] == 2025][['codra', 'regiao_adm', 'pop_0_4', 'mae', 'pai']]
_ra_outros = (df_vf_ra[df_vf_ra['ano'].between(2021, 2025)].groupby('codra', as_index=False)['outros'].sum()
              .rename(columns={'outros': 'outros_2021_2025'}))
df_vf_taxa_ra = _ra_2025.merge(_ra_outros, on='codra')
for _nome, _casos in [('mae_2025', 'mae'), ('pai_2025', 'pai'), ('outros_2021_2025', 'outros_2021_2025')]:
    df_vf_taxa_ra = taxa_por_mil(df_vf_taxa_ra, _casos, 'pop_0_4', f'taxa_por_mil_{_nome}')
assert not np.isinf(df_vf_taxa_ra.select_dtypes('number')).any().any()

for _nome, _rotulo, _periodo in [('mae_2025', 'mãe', '2025'), ('pai_2025', 'pai', '2025'), ('outros_2021_2025', 'outros vínculos', '2021-2025')]:
    _col = f'taxa_por_mil_{_nome}'
    _mapa_ra = df_vf_taxa_ra[['codra', 'regiao_adm', 'pop_0_4', _col]].copy()
    _mapa_ra.to_csv(f'tabelas_finais/tabela_mapa_violencia_familiar_taxa_ra_{_nome}.csv', index=False)
    mapa_coropletico_bairros(
        _mapa_ra, coluna_valor=_col, chave='codra', nivel='ra',
        titulo=f'Notificações de violência ({_rotulo}) por 1.000 crianças de 0 a 4 anos, por RA ({_periodo})',
        nome_arquivo=f'mapa_violencia_familiar_{_nome.split("_")[0]}_taxa_ra_{_nome.split("_", 1)[1]}',
        cmap=_CORES_TEMA_MAPA['protecao'], fundo='mapa_oceano_base',
        legenda_titulo='Notificações por\n1.000 crianças 0-4\n(Censo 2022)', fonte_dados=fonte_sinan_censo,
    )

# %% [markdown]
# ##### G8 · Dez maiores taxas (mãe e pai, 2025)
#
# > Só bairros com 100 ou mais crianças de 0 a 4 anos (taxa estável); mãe e pai lado a lado, sem soma.

# %%
_est = df_vf_taxa_bairro[df_vf_taxa_bairro['pop_0_4'] >= 100]
top10_taxa = _est.nlargest(10, 'taxa_por_mil_mae_2025')
df_top_taxa = (top10_taxa[['bairro', 'taxa_por_mil_mae_2025', 'taxa_por_mil_pai_2025']]
               .rename(columns={'taxa_por_mil_mae_2025': 'Mãe', 'taxa_por_mil_pai_2025': 'Pai'})
               .melt(id_vars='bairro', var_name='vinculo', value_name='taxa por 1.000'))
df_top_taxa.to_csv('tabelas_finais/violencia_familiar_taxa_top_bairros_2025.csv', index=False)
grafico_barra_agrupado(
    df_top_taxa, categoria='bairro', valor='taxa por 1.000', agrupador='vinculo',
    titulo='Dez maiores taxas de notificação por 1.000 crianças de 0 a 4 anos (2025)',
    nome_arquivo='violencia_familiar_taxa_top_bairros_2025', ylabel='Notificações por 1.000 crianças\nde 0 a 4 anos (Censo 2022)',
    legend_title='Vínculo', ordem_categoria=list(top10_taxa['bairro']), ordem_agrupador=['Mãe', 'Pai'],
    fonte_dados=fonte_sinan_censo + '; bairros com 100+ crianças',
)

# %% [markdown]
# ---
# ## 📝 Análise / Relatório
#
# *(Pendente)* Síntese narrativa dos achados, organizada pelos 6 eixos ativos
# da política municipal de primeira infância (`specs/estrutura_eixos.md`,
# `specs/2026-09-22_ajuste_eixos/specs.md`) — substitui os 5 subtítulos antigos por
# fonte de dado (Demografia e População, Assistência Social, Educação,
# Saúde, Proteção).

# %% [markdown]
# *(Pendente)* Síntese narrativa dos achados.

# %%
###

# %% [markdown]
# ### 🎯 Prioridade (sem secundário)

# %%
#### Resumo dos achados

#### Fontes de Dados

# %%
#### Dimensão temporal

# %%
#### Recortes de Raça e Gênero

# %%
#### Dimensão geográfica

# %% [markdown]
# ### 🤝 Inclusão

# %% [markdown]
# ### 👨‍👩‍👧 Família e Cuidados

# %% [markdown]
# ### 🛡️ Proteção

# %% [markdown]
# ### 🍽️ Alimentação

# %% [markdown]
# ### 🏠 Moradia
