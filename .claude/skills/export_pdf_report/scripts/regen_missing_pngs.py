"""Regenerate any visualizacoes/*.png that is missing under its current
nome_arquivo (analise.py sometimes gets partially re-run -- e.g. only the
newest section -- so older sections' PNGs can go stale/missing after a
renaming refactor), using data already exported to tabelas_finais/ (no DB
or raw dados_locais/ dependency needed). Plotting functions are copied
verbatim from analise.py's "Funcoes de visualizacao" section to match the
notebook's visual style exactly (matplotlib/seaborn, same figsize/palette).

Run from the project root (paths below are relative to it). Safe to run
even when nothing is missing -- it always regenerates the ~15 charts it
knows how to build from tabelas_finais/ alone; the 4 CadUnico charts and
everything else are included since tabelas_finais/ already holds their
last-exported data (no DB round-trip needed even for CadUnico).

If analise.py's plotting functions, column names, or CSV schemas change,
this script (and build_notebook_report.py) need matching updates -- treat
it as a snapshot of analise.py's plotting/export contract as of 2026-09-02,
not as a generic tool.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

OUT = "visualizacoes"

# ---- verbatim from analise.py's "Funcoes de visualizacao" ----
def serie_temporal(df, tempo, valor, titulo, nome_arquivo=None, formato='png'):
    nome_arquivo = nome_arquivo or f"{valor}_{tempo}"
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=tempo, y=valor, data=df)
    plt.xlabel(tempo, fontsize=12)
    plt.ylabel(valor, fontsize=12)
    plt.title(titulo, fontsize=14)
    plt.savefig(f"{OUT}/{nome_arquivo}.{formato}")
    plt.close()

def grafico_barra(df, categoria, valor, titulo, nome_arquivo=None, formato='png'):
    nome_arquivo = nome_arquivo or f"{valor}_{categoria}"
    plt.figure(figsize=(10, 6))
    sns.barplot(x=categoria, y=valor, data=df, palette='pastel', hue=categoria)
    plt.xlabel(categoria, fontsize=12)
    plt.ylabel(valor, fontsize=12)
    plt.title(titulo, fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{OUT}/{nome_arquivo}.{formato}")
    plt.close()

print("generating missing PNGs...")

# ---- Censo: two series analise.py never saves (plt.show() only) ----
df_censo_serie = pd.read_csv("tabelas_finais/censo_0_a_4_anos_por_ano.csv")
df_censo_serie['ano'] = df_censo_serie['ano'].astype(str)

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_censo_serie, x='ano', y='0 a 4 anos', label='Total 0 a 4 anos', marker='o', errorbar=None)
sns.lineplot(data=df_censo_serie, x='ano', y='Sexo feminino, 0 a 4 anos', label='Sexo Feminino', marker='o', errorbar=None)
sns.lineplot(data=df_censo_serie, x='ano', y='Sexo masculino, 0 a 4 anos', label='Sexo Masculino', marker='o', errorbar=None)
plt.title('Série Temporal: Crianças 0 a 4 anos', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Valores', fontsize=10)
plt.legend(title='Indicadores', fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{OUT}/censo_0_a_4_serie_total_ano.png")
plt.close()

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_censo_serie, x='ano', y='Percentual 0 a 4 anos', label='Percentual 0 a 4 anos', marker='o', errorbar=None)
plt.title('Série Temporal: Crianças 0 a 4 anos', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Valores', fontsize=12)
plt.legend(title='Indicadores', fontsize=10)
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{OUT}/censo_0_a_4_serie_percentual_ano.png")
plt.close()

# ---- CadÚnico (from already-exported tabelas_finais CSVs, no DB needed) ----
df_renda = pd.read_csv("tabelas_finais/cadunico_por_faixa_etaria_2026.csv")
df_renda = df_renda[df_renda['faixa de renda'] != 'Total']
grafico_barra(df_renda, categoria='faixa de renda', valor='Famílias',
              titulo='CADÚNICO: Famílias c/crianças 0-6 por faixa de renda per capita',
              nome_arquivo='cadunico_familias_por_faixa_renda')
grafico_barra(df_renda, categoria='faixa de renda', valor='Crianças',
              titulo='CADÚNICO: Crianças 0-6 por faixa de renda per capita',
              nome_arquivo='cadunico_criancas_por_faixa_renda')

df_idade = pd.read_csv("tabelas_finais/cadunico_por_idade_2026.csv")
df_idade['idade'] = df_idade['idade'].astype(int)
grafico_barra(df_idade, categoria='idade', valor='Famílias',
              titulo='CADÚNICO: Famílias c/ crianças 0-6 por idade',
              nome_arquivo='cadunico_familias_por_idade')
grafico_barra(df_idade, categoria='idade', valor='Crianças',
              titulo='CADÚNICO: Crianças 0-6 por idade',
              nome_arquivo='cadunico_criancas_por_idade')

# ---- Nascidos vivos / abaixo peso ----
# NB: 'ano' is cast to str before plotting everywhere below, matching the dtype
# these dataframes have in-memory in analise.py (grouped from a melted/string
# 'ano' column). Reading straight from a CSV instead infers int64, which makes
# seaborn treat the x-axis as continuous and emit fractional-year ticks (e.g.
# "2007.5") instead of one tick per year -- str() avoids that regression.
df_vivos_por_ano = pd.read_csv("tabelas_finais/nascidos_vivos_por_ano.csv")
df_vivos_por_ano['ano'] = df_vivos_por_ano['ano'].astype(str)
serie_temporal(df_vivos_por_ano, tempo='ano', valor='nascidos vivos', titulo='Nascidos vivos por ano',
               nome_arquivo='nascidos_vivos_por_ano')

df_baixo_ano = pd.read_csv("tabelas_finais/nascidos_abaixo_peso_por_ano.csv")
df_baixo_ano['ano'] = df_baixo_ano['ano'].astype(str)
serie_temporal(df_baixo_ano, tempo='ano', valor='percentual abaixo do peso', titulo='Percentual Nascidos com baixo peso por ano',
               nome_arquivo='nascidos_abaixo_peso_percentual_por_ano')

# ---- Obitos gravidez / puerperio ----
df_obitos_gravidez_anual = pd.read_csv("tabelas_finais/obitos_gravidez_por_ano.csv")
df_obitos_gravidez_anual['ano'] = df_obitos_gravidez_anual['ano'].astype(str)
serie_temporal(df_obitos_gravidez_anual, 'ano', 'óbitos-gravidez', 'Óbitos durante gravidez por ano',
               nome_arquivo='obitos_gravidez_por_ano')

df_obitos_puerperio_anual = pd.read_csv("tabelas_finais/obitos_puerperio_por_ano.csv")
df_obitos_puerperio_anual['ano'] = df_obitos_puerperio_anual['ano'].astype(str)
serie_temporal(df_obitos_puerperio_anual, 'ano', 'óbitos-puerpério', 'Óbitos durante puerpério por ano',
               nome_arquivo='obitos_puerperio_por_ano')

# ---- SISVAN ----
df_desnutricao = pd.read_csv("tabelas_finais/sisvan_desnutricao_por_ano.csv")
df_desnutricao['ano'] = df_desnutricao['ano'].astype(str)
serie_temporal(df_desnutricao, tempo='ano', valor='Percent. baixo peso total', titulo='Percentual Crianças 0-6 com baixo peso',
               nome_arquivo='sisvan_desnutricao_percentual_por_ano')

df_sobrepeso = pd.read_csv("tabelas_finais/sisvan_sobrepeso_por_ano.csv")
df_sobrepeso['ano'] = df_sobrepeso['ano'].astype(str)
serie_temporal(df_sobrepeso, tempo='ano', valor='Percent. sobrepeso total', titulo='Percentual Crianças 0-6 com sobrepeso i.e. PESO ACIMA + OBESIDADE',
               nome_arquivo='sisvan_sobrepeso_percentual_por_ano')
serie_temporal(df_sobrepeso, tempo='ano', valor='obesidade_percentual', titulo='Percentual Crianças 0-6 com obesidade',
               nome_arquivo='sisvan_obesidade_percentual_por_ano')

# ---- Educacao ----
df_freq_escolar = pd.read_csv("tabelas_finais/frequencia_escolar_pnad_por_idade.csv")
grafico_barra(df=df_freq_escolar, categoria='Idade', valor='Total', titulo="Frequencia escolar por idade",
              nome_arquivo='pnad_frequencia_escolar_por_idade')

df_matriculas = pd.read_csv("tabelas_finais/matriculas_0_a_6_por_ano.csv")
df_matriculas['ano'] = df_matriculas['ano'].astype(str)
serie_temporal(df_matriculas, 'ano', 'matriculas', 'Matrículas de 0 a 6 anos por ano',
               nome_arquivo='matriculas_0_a_6_por_ano')

print("done")
