# %%
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os


# %% [markdown]
# ## Funcões Auxiliares

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


# %% [markdown]
# ### Cadúnico

# %%
#Banco CTPE
engine = connect_db_ctpe()
df_original = pd.read_sql("SELECT * FROM silver_cadunico_geral WHERE grupo_idade='0-6'", engine)
df =  df_original.copy()
df_original

# %%
df = df.rename(columns={'id_pessoa':'Crianças','id_familia':'Famílias','grupo_renda_pct':'faixa de renda'})

# %%
#quantitativos por grupo de renda pct
df_renda = df.groupby(by='faixa de renda').agg({'Crianças':'count','Famílias':'nunique'})
df_renda.loc['Total'] = df_renda.sum()
custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
df_renda = df_renda.reindex(custom_order)
df_renda.head(10)

# %%
grafico_barra(df_renda.iloc[:-1,:],categoria='faixa de renda',valor='Famílias',
              titulo='CADÚNICO: Famílias por faixa de renda per capita',
              formato='png')

# %%
grafico_barra(df_renda.iloc[:-1,:],categoria='faixa de renda',valor='Crianças',
              titulo='CADÚNICO: Crianças por faixa de renda per capita',
              formato='svg')

# %%
#quantitativos por idade
df #fazer one hot da coluna sexo
df_idade = df.groupby(by='idade').agg({'Crianças':'count','Famílias':'nunique'})#,'sexo_m':'sum','sexo_f':'sum'})
df_idade.head(10)


# %%
grafico_barra(df_idade,categoria='idade',valor='Famílias', titulo='CADÚNICO: Famílias por idade')

# %%
grafico_barra(df_idade,categoria='idade',valor='Crianças', titulo='CADÚNICO: Crianças por idade')

# %% [markdown]
# ### DataSus

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
df_baixo_ano.head(25)

# %%
serie_temporal(df_baixo_ano,tempo='ano',valor='percentual abaixo do peso', titulo='Nascidos com baixo peso por ano')

# %% [markdown]
# ### SISVAN

# %%
df_desnutricao = pd.read_csv(r"dados_locais\tratados\desnutrição.csv", index_col=0)
df_desnutricao.head()

# %%
df_desnutricao['peso_muito_baixo_percentual'] = df_desnutricao['peso_muito_baixo_percentual'].apply(convert_numeric_safe)
df_desnutricao['peso_baixo_percentual'] = df_desnutricao['peso_baixo_percentual'].apply(convert_numeric_safe)
df_desnutricao['Percent. baixo peso total'] = df_desnutricao['peso_muito_baixo_percentual'] + df_desnutricao['peso_baixo_percentual']
serie_temporal(df_desnutricao,tempo='ano',valor='Percent. baixo peso total', titulo='Crianças com baixo peso')

# %% [markdown]
#

# %%
df_sobrepeso = pd.read_csv(r"dados_locais\tratados\sobrepeso.csv", index_col=0)
df_sobrepeso.head()

# %%
df_sobrepeso['sobrepeso_percentual'] = df_sobrepeso['sobrepeso_percentual'].apply(convert_numeric_safe)
df_sobrepeso['obesidade_percentual'] = df_sobrepeso['obesidade_percentual'].apply(convert_numeric_safe)
df_sobrepeso['Percent. sobrepeso total'] = df_sobrepeso['sobrepeso_percentual'] + df_sobrepeso['obesidade_percentual']
serie_temporal(df_sobrepeso,tempo='ano',valor='Percent. sobrepeso total', titulo='Crianças com sobrepeso')

# %% [markdown]
# ## Entregaveis Dia 19

# %% [markdown]
# ### Análises por bairros

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
