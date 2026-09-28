# -*- coding: utf-8 -*-
"""Funções auxiliares do notebook `analise.py` (limpeza, carga por fonte, gráficos, mapas, variante de
impressão). Pacote criado em specs/2026-09-28_organizacao (fase 1b): antes eram as linhas 1-1897 de
`analise.py`. `from primeira_infancia import *` traz todos os nomes (inclusive os com `_`, usados pelas seções).
"""
from .conexao import *  # noqa: F401,F403
from .limpeza import *  # noqa: F401,F403
from .estilo import *  # noqa: F401,F403
from .impressao import *  # noqa: F401,F403
from .graficos import *  # noqa: F401,F403
from .mapas import *  # noqa: F401,F403
from .protecao import *  # noqa: F401,F403
from .cadunico import *  # noqa: F401,F403
from .populacao import *  # noqa: F401,F403
from .educacao import *  # noqa: F401,F403
from . import conexao, limpeza, estilo, impressao, graficos, mapas, protecao, cadunico, populacao, educacao  # noqa: E402

__all__ = [n for m in (conexao, limpeza, estilo, impressao, graficos, mapas, protecao, cadunico, populacao, educacao) for n in m.__all__]
