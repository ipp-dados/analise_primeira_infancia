# %% [markdown]
# ## Pacotes e Funcões Auxiliares

# %%
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os


# %%
#conecta ao banco CTPE
def connect_db_ctpe():
    """
    Inicializa o cliente do banco local.

    Returns:
        engine: engine de sqlalchemy
    """
    # cria parâmetros da conexão com banco local
    parameters = {
    "db_name": os.getenv('db_name'),
    "user": os.getenv('user'),
    "password_db": os.getenv('password_db'),
    "host": os.getenv('host'),
    "port": os.getenv('port')
    }
    DB_URL = f"postgresql+psycopg://{parameters['user']}:{parameters['password_db']}@{parameters['host']}:{parameters['port']}/{parameters['db_name']}?client_encoding=utf8"
    engine = create_engine(DB_URL)
    return engine

def convert_numeric_safe(s):
    s_cleaned = s.strip().replace('%','')
    return float(s_cleaned)

def limpa_dados_sisvan(colunas, dataset):
    path = Path(f"dados_locais\\{dataset}\\")
    arquivos = [f.name for f in path.iterdir() if f.is_file() and f.name != 'example_file']
    
    colunas_ajustadas = ['ano']
    for i in colunas:
        if i != 'total':
            colunas_ajustadas.append(i+'_bruto')
            colunas_ajustadas.append(i+'_percentual')
        else:
            colunas_ajustadas.append(i)
    print(colunas_ajustadas)
    df_final = pd.DataFrame(columns=colunas_ajustadas)

    for arquivo in arquivos:
        df = pd.read_excel(f"dados_locais\\{dataset}\\{arquivo}")
        df_infos = df.iloc[[10],5:]
        df_infos.columns = colunas_ajustadas[1:]
        df_infos['ano'] = arquivo[-9:-5]
        df_final = pd.concat([df_final,df_infos])
    df_final.reset_index(inplace=True, drop=True)
    
    df_final.to_csv(f"dados_locais\\tratados\\{dataset}.csv")

def limpa_dados_datasus(df):
    df = df.melt(id_vars=['Bairro Residencia'])
    return df

def serie_temporal(df,tempo,valor,titulo, formato='png'):
    plt.figure(figsize=(12,6))
    sns.lineplot(x=tempo,y=valor,data=df)
    plt.xlabel(tempo,fontsize=12)
    plt.ylabel(valor,fontsize=12)
    plt.title(titulo,fontsize=14)
    plt.savefig(f"visualizacoes/{valor}_{tempo}.{formato}")
    plt.title(titulo)

def grafico_barra(df,categoria,valor,titulo, formato='png'):
    plt.figure(figsize=(10,6))
    sns.barplot(x=categoria,y=valor,data=df,palette='pastel',hue=categoria)
    plt.xlabel(categoria,fontsize=12)
    plt.ylabel(valor, fontsize=12)
    plt.title(titulo,fontsize=14)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{valor}_{categoria}.{formato}")
    plt.show()

#carrega variáveis de ambiente
load_dotenv()

# %%
limpa_dados_sisvan(colunas=['magreza_acentuada','magreza','eutrofia','risco sobrepeso','sobrepeso','obesidade','total'], dataset='sobrepeso')
limpa_dados_sisvan(colunas=['peso_muito_baixo','peso_baixo','peso_adequado','peso_elevado','total'], dataset='desnutrição')

# %% [markdown]
# ## Visualização dos Dados (entregável dia 12)

# %% [markdown]
# <p>Para cesso aos dados brutos via Drive: https://drive.google.com/drive/folders/1xOwf72QfaDuJAHuA-Vngl6t5_kzSfGYX?usp=sharing</p>
# <p>OBS: acesso restrito, solicitar a leonardo.aucar@prefeitura.rio</p>

# %% [markdown]
# ### Censo 2022(10/00)

# %%
## dados censo
df_censo = pd.read_csv("dados_locais\\pop_censo_2022_datario.csv", encoding='Latin-1', sep=';')
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
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4','5 a 9 anos','Percentual 5 a 9']].sort_values(by='0 a 4 anos',ascending=False).to_csv('Tabelas_finais\\censo_por_bairro.csv')

# %%
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False)
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).to_excel('tabela_mapa_0_4_absoluto.xlsx')
#mapa por total de 0 a 4 anos

# %%
# para bairros 'muito grandes' (+100.000 pessoas)
df_censo.loc[df_censo['Total'] > 20000,['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False)
df_censo.loc[df_censo['Total'] > 20000,['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).to_excel('tabela_mapa_grandes_0_4_percentual.xlsx')
#mapa por percentual dos bairros grandes

# %% [markdown]
# #### Serie temporal censo

# %%
df_2000 = pd.read_csv('dados_locais\\tabela 2974_2000.csv', sep=';')
df_2010 = pd.read_csv('dados_locais\\tabela 2974_2010.csv', sep=';')
df_2022 = pd.read_csv('dados_locais\\tabela 2974_2022.csv', sep=';')

def total_e_percentual_ano(df):
    df['0 a 4 anos'] = df['Sexo feminino, 0 a 4 anos'] + df['Sexo masculino, 0 a 4 anos']
    df['Total'] = df.iloc[:,9:].sum(axis=1)
    df['Percentual 0 a 4 anos'] = (df['0 a 4 anos']/df['Total'])
    return df[['bairro','0 a 4 anos','Percentual 0 a 4 anos','Sexo feminino, 0 a 4 anos','Sexo masculino, 0 a 4 anos']]

df_serie_censo = pd.DataFrame(columns=['bairro','ano','0 a 4 anos','Percentual 0 a 4 anos','Sexo feminino, 0 a 4 anos','Sexo masculino, 0 a 4 anos'])
for i in [[df_2000,'2000'],[df_2010,'2010'],[df_2022,'2022']]:
    df = total_e_percentual_ano(i[0])
    df['ano'] = i[1]
    df_serie_censo = pd.concat([df_serie_censo,df])

df_serie_censo[['ano','0 a 4 anos', 'Percentual 0 a 4 anos','Sexo feminino, 0 a 4 anos','Sexo masculino, 0 a 4 anos']].groupby(by='ano').sum()

# %%
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_serie_censo, x='ano', y='0 a 4 anos', label='Total 0 a 4 anos', marker='o')
sns.lineplot(data=df_serie_censo, x='ano', y='Sexo feminino, 0 a 4 anos', label='Sexo Feminino', marker='o')
sns.lineplot(data=df_serie_censo, x='ano', y='Sexo masculino, 0 a 4 anos', label='Sexo Masculino', marker='o')
#sns.lineplot(data=df_serie_censo, x='ano', y='Percentual 0 a 4 anos', label='Percentual 0 a 4 anos', marker='o')

# Customize the plot
plt.title('Série Temporal: Crianças 0 a 4 anos', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Valores', fontsize=12)
plt.legend(title='Indicadores', fontsize=10)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# %%
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_serie_censo, x='ano', y='Percentual 0 a 4 anos', label='Percentual 0 a 4 anos', marker='o')

# Customize the plot
plt.title('Série Temporal: Crianças 0 a 4 anos', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Valores', fontsize=12)
plt.legend(title='Indicadores', fontsize=10)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# %% [markdown]
# ### Cadúnico

# %% [markdown]
# #### Recorte 0-6 anos

# %%
#Banco CTPE
engine = connect_db_ctpe()
df_original = pd.read_sql("SELECT * FROM silver_cadunico_geral WHERE grupo_idade='0-6'", engine)
df =  df_original.copy()
df_original

# %%
df = df.rename(columns={'id_pessoa':'Crianças','id_familia':'Famílias','grupo_renda_pct':'faixa de renda'})

# %%
df_bairro = pd.read_csv('dados_locais\\lista_bairros.csv', dtype={'cep': str})
df['cep'] = df['cep'].astype(str)

# 2. Faz o JOIN (Merge) trazendo apenas a coluna 'bairros' baseada no 'cep'
df = df.merge(df_bairro[['cep', 'bairro']], on='cep', how='left')

# %%
#quantitativos por grupo de renda pct
df_renda = df.groupby(by='faixa de renda').agg({'Crianças':'count','Famílias':'nunique'})
df_renda.loc['Total'] = df_renda.sum()
custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
df_renda = df_renda.reindex(custom_order)
df_renda.head(10)
df_renda.to_csv('Tabelas_finais\\cadunico_por_faixa_etaria_2026.csv')

# %%
grafico_barra(df_renda.iloc[:-1,:],categoria='faixa de renda',valor='Famílias',
              titulo='CADÚNICO: Famílias c/crianças 0-6 por faixa de renda per capita',
              formato='png')

# %%
grafico_barra(df_renda.iloc[:-1,:],categoria='faixa de renda',valor='Crianças',
              titulo='CADÚNICO: Crianças 0-6 por faixa de renda per capita',
              formato='png')

# %%
#quantitativos por idade
df #fazer one hot da coluna sexo
df_idade = df.groupby(by='idade').agg({'Crianças':'count','Famílias':'nunique'})#,'sexo_m':'sum','sexo_f':'sum'})
df_idade.to_csv('Tabelas_finais\\cadunico_por_idade_2026.csv')
df_idade.head(10)


# %%
grafico_barra(df_idade,categoria='idade',valor='Famílias', titulo='CADÚNICO: Famílias c/ crianças 0-6 por idade')

# %%
grafico_barra(df_idade,categoria='idade',valor='Crianças', titulo='CADÚNICO: Crianças 0-6 por idade')

# %% [markdown]
# #### Análise por bairros

# %%
#quantitativos por grupo de renda pct
df_bairro = df.groupby(by=['bairro']).agg({'Crianças':'count','Famílias':'nunique'})
df_bairro.loc['Total'] = df_bairro.sum()
#custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
#df_bairro = df_bairro.reindex(custom_order)
df_bairro.to_csv('Tabelas_finais\\cadunico_por_bairro_2026.csv')

# %%
df_bairro.sort_values(by='Crianças', ascending=False).head(10)
# ADICIONAR NOTA SOBRE IDENTIFICACAO DE BAIRROS

# %%
df_bairro.sort_values(by='Primeira Inf. Cadúnico', ascending=True).head(10)

# %%
#quantitativos por grupo de renda pct
df_ate_4 = df[df['idade']<5].copy()
df_bairro_ate_4 = df_ate_4.groupby(by=['bairro']).agg({'Crianças':'count','Famílias':'nunique'})
df_bairro_ate_4.loc['Total'] = df_bairro_ate_4.sum()
#custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
#df_bairro = df_bairro.reindex(custom_order)
df_bairro_ate_4.to_csv('Tabelas_finais\\cadunico_por_bairro_2026.csv')
df_bairro_ate_4 = df_bairro_ate_4.merge(df_censo[['bairro','0 a 4 anos']], on='bairro', how='right')
df_bairro_ate_4['Primeira Inf. Cadúnico'] = df_bairro_ate_4['Crianças']/df_bairro_ate_4['0 a 4 anos']
df_bairro_ate_4.sort_values(by='Crianças', ascending=False).head(10)

# %%
df_bairro[df_bairro['bairro']=='Complexo do Alemão']

# %% [markdown]
# ### DataSus - tabnet

# %%
#Nascidos vivos
df_vivos = pd.read_csv(r"dados_locais\nascidos_vivos_bairros_2006_a_2025.csv")
df_vivos = limpa_dados_datasus(df_vivos)
df_vivos.head()


# %%
#df_total = df_vivos[df_vivos['variable']=='Total']
#df_total.head()
#df_vivos['Percentual'] = (df_vivos['value']/df_total['value'])*100
# le arquivos CSV do datasus
# calcula indicadores primeira infancia
# exporta resultados

# %%
df_vivos_por_ano = df_vivos.loc[:,['variable','value']].groupby(by='variable').sum()
df_vivos_por_ano.drop(index='Total',inplace=True)
df_vivos_por_ano.reset_index(inplace=True)
df_vivos_por_ano.rename({'variable':'ano','value':'Nascidos vivos'},axis=1, inplace=True)
df_vivos_por_ano.head(25)
df_vivos_por_ano.to_csv('Tabelas_finais\\nascidos_vivos_por_ano.csv')

# %%
serie_temporal(df_vivos_por_ano,tempo='ano',valor='Nascidos vivos', titulo='Nascidos vivos por ano')

# %%
#Nascidos abaixo do peso
df_baixo_peso = pd.read_csv(r"dados_locais\nascidos_vivos_baixo_peso_ao_nascer_bairros_2006_a_2025.csv")
df_baixo_peso = limpa_dados_datasus(df_baixo_peso)
df_baixo_peso.head()

# %%
df_baixo_ano = df_baixo_peso.loc[:,['variable','value']].groupby(by='variable').sum()
df_baixo_ano.drop(index='Total',inplace=True)
df_baixo_ano.reset_index(inplace=True)
df_baixo_ano.rename({'variable':'ano','value':'Nascidos abaixo peso'},axis=1, inplace=True)
df_baixo_ano['percentual abaixo do peso'] = (df_baixo_ano['Nascidos abaixo peso']/df_vivos_por_ano['Nascidos vivos'])*100
df_baixo_ano.to_csv('Tabelas_finais\\nascidos_abaixo_peso_por_ano.csv')
df_baixo_ano.head(25)

# %%
serie_temporal(df_baixo_ano,tempo='ano',valor='percentual abaixo do peso', titulo='Percentual Nascidos com baixo peso por ano')

# %% [markdown]
# ### DataSus - SISVAN

# %%
df_desnutricao = pd.read_csv(r"dados_locais\tratados\desnutrição.csv", index_col=0)
df_desnutricao.tail()

# %%
df_desnutricao['peso_muito_baixo_percentual'] = df_desnutricao['peso_muito_baixo_percentual'].apply(convert_numeric_safe)
df_desnutricao['peso_baixo_percentual'] = df_desnutricao['peso_baixo_percentual'].apply(convert_numeric_safe)
df_desnutricao['Percent. baixo peso total'] = df_desnutricao['peso_muito_baixo_percentual'] + df_desnutricao['peso_baixo_percentual']
df_desnutricao.to_csv('Tabelas_finais\\sisvan_desnutricao_por_ano.csv')
serie_temporal(df_desnutricao,tempo='ano',valor='Percent. baixo peso total', titulo='Percentual Crianças 0-6 com baixo peso')

# %%
df_sobrepeso = pd.read_csv(r"dados_locais\tratados\sobrepeso.csv", index_col=0)
df_sobrepeso.head()

# %%
df_sobrepeso['sobrepeso_percentual'] = df_sobrepeso['sobrepeso_percentual'].apply(convert_numeric_safe)
df_sobrepeso['obesidade_percentual'] = df_sobrepeso['obesidade_percentual'].apply(convert_numeric_safe)
df_sobrepeso['Percent. sobrepeso total'] = df_sobrepeso['sobrepeso_percentual'] + df_sobrepeso['obesidade_percentual']
df_sobrepeso.to_csv('Tabelas_finais\\sisvan_sobrepeso_por_ano.csv')
serie_temporal(df_sobrepeso,tempo='ano',valor='Percent. sobrepeso total', titulo='Percentual Crianças 0-6 com sobrepeso i.e. PESO ACIMA + OBESIDADE')

# %%
serie_temporal(df_sobrepeso,tempo='ano',valor='obesidade_percentual', titulo='Percentual Crianças 0-6 com obesidade')

# %% [markdown]
# ## Entregaveis Dia 19

# %% [markdown]
# ### Análises por bairros

# %%
# Censo 2022
# Tabnet
# Cadunico

# %% [markdown]
# ### Série Histórica Censo

# %%

# %% [markdown]
# ### Dados datasus faltantes

# %%

# %% [markdown]
# ### PNAD Contínua e INEP

# %%
# teste

# %% [markdown]
# ## Entregáveis posteriores

# %% [markdown]
# ## Análise / Relatório

# %%
