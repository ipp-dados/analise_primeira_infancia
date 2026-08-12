# %%
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pathlib import Path
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

def grafico_barra(df):
    pass

def grafico_serie_temporal(df):
    pass

#carrega variáveis de ambiente
load_dotenv()

# %%
limpa_dados_sisvan(colunas=['magreza_acentuada','magreza','eutrofia','risco sobrepeso','sobrepeso','obesidade','total'], dataset='sobrepeso')
limpa_dados_sisvan(colunas=['peso_muito_baixo','peso_baixo','peso_adequado','peso_elevado','total'], dataset='desnutrição')

# %% [markdown]
# ## Carregamento dos Dados

# %% [markdown]
# <p>Para cesso aos dados brutos via Drive: https://drive.google.com/drive/folders/1xOwf72QfaDuJAHuA-Vngl6t5_kzSfGYX?usp=sharing</p>
# <p>OBS: acesso restrito, solicitar a leonardo.aucar@prefeitura.rio</p>

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
df_renda.reindex(custom_order).head(10)

# %%
#quantitativos por idade
df #fazer one hot da coluna sexo
df_idade = df.groupby(by='idade').agg({'Crianças':'count','Famílias':'nunique'})#,'sexo_m':'sum','sexo_f':'sum'})
df_idade.head(10)


# %% [markdown]
# ### DataSus

# %%
#Nascidos vivos
df_vivos = pd.read_csv(r"dados_locais\nascidos_vivos_bairros_2006_a_2025.csv")
df_vivos = limpa_dados_datasus(df_vivos)
df_total = df_vivos[df_vivos['variable']=='Total']
df_vivos['Percentual'] = (df_vivos['value']/df_total['value'])*100
df_vivos.tail()
# le arquivos CSV do datasus
# calcula indicadores primeira infancia
# exporta resultados

# %%
#Nascidos abaixo do peso
df_baixo_peso = pd.read_csv(r"dados_locais\nascidos_vivos_baixo_peso_ao_nascer_bairros_2006_a_2025.csv")
df_baixo_peso = limpa_dados_datasus(df_baixo_peso)
df_baixo_peso.head()

# %% [markdown]
# ### SISVAN

# %%
df_desnutricao = pd.read_csv(r"dados_locais\tratados\desnutrição.csv", index_col=0)
df_desnutricao.head()

# %%
df_sobrepeso = pd.read_csv(r"dados_locais\tratados\sobrepeso.csv", index_col=0)
df_sobrepeso.head()

# %% [markdown]
# ### Censo 2022(10/00)

# %%
## dados censo
# le arquivos CSV do censo
# calcula indicadores primeira infancia
# exporta resultados

# %% [markdown]
# ### PNAD Contínua e INEP

# %%
# teste

# %% [markdown]
# ## Visualizações

# %%
df_idade.plot()

# %% [markdown]
# ## Análise / Relatório

# %%
