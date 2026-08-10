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
    "port": 5432
    }
    DB_URL = f"postgresql+psycopg://{parameters['user']}:{parameters['password_db']}@{parameters['host']}:{parameters['port']}/{parameters['db_name']}?client_encoding=utf8"
    engine = create_engine(DB_URL)
    return engine

#checa dados em ctpe
def executar_consulta(client, query):
    """
    Executa uma consulta no BigQuery e salva o resultado em um arquivo Parquet.

    Args:
        client (google.cloud.bigquery.client.Client): O cliente BigQuery.
        query (str): A string da consulta SQL a ser executada.
    """
    df = client.query(query).to_dataframe()
    return df


# %% [markdown]
# ## Carregamento dos Dados

# %% [markdown]
# ### Cadúnico

# %%
## Cadúnico
# carrega dados cadunico em df
# calcula indicadores 1 infancia
# exporta resultados

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
