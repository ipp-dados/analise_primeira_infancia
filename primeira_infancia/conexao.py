# -*- coding: utf-8 -*-
"""### 🔌 Conexão e utilitários gerais

Conexão com o banco do CTPE (`connect_db_ctpe`, credenciais do `.env`; exige `psycopg` 3 — env `analises_env`) e conversão numérica tolerante.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import os
from sqlalchemy import create_engine

__all__ = [
    'connect_db_ctpe',
    'convert_numeric_safe',
]


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
