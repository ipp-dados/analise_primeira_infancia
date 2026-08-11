# %%
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
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

#carrega variáveis de ambiente
load_dotenv()



# %% [markdown]
# ## Carregamento dos Dados

# %% [markdown]
# ### Cadúnico

# %%
## Cadúnico
# carrega dados cadunico em df

engine = connect_db_ctpe()
df_original = pd.read_sql("SELECT * FROM silver_cadunico_geral WHERE grupo_idade='0-6'", engine)
df =  df_original.copy()
df_original


# calcula indicadores 1 infancia
# exporta resultados

# %%
df_original['id_familia'].nunique()
df_original['grupo_renda_pct'].isna().sum()

# %%
#quantitativos por grupo de renda pct
df_renda = df.groupby(by='grupo_renda_pct').agg({'id_pessoa':'count','id_familia':'nunique'})
df_renda.loc['Total'] = df_renda.sum()
custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
df_renda.reindex(custom_order).head(10)

# %%
#quantitativos por idade
df_idade = df.groupby(by='idade').agg({'id_pessoa':'count','id_familia':'nunique'})
df_idade.head(10)


# %% [markdown]
# ### DataSus

# %%
## DataSus
# le arquivos CSV do datasus
# calcula indicadores primeira infancia
# exporta resultados

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

# %% [markdown]
# ## Análise / Relatório

# %%
