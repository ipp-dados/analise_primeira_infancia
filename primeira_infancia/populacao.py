# -*- coding: utf-8 -*-
"""### 👥 População de referência (Ripsa/MS) — carregadores

Estimativas populacionais Ripsa/Ministério da Saúde 2000-2025 (Nota Técnica Ripsa nº 01/2025), por
município, sexo e idade simples, via Tabnet (`popsvs2024br.def`). É o denominador de **toda taxa
municipal** do projeto; abaixo do município (bairro, AP, RP, RA, CAP) o denominador continua sendo o
Censo 2022 (decisão B1). Ver `specs/2026-09-24_populacao-referencia/` e a nota geral no início da seção Censo 2022.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import csv
import os
import pandas as pd
import re
import requests
import time
import urllib.parse
from pathlib import Path

__all__ = [
    '_URL_TABNET_RIPSA',
    '_CAMINHO_EXTRATO_RIPSA',
    '_FILTROS_TABNET_RIPSA',
    '_SEXOS_TABNET_RIPSA',
    '_consulta_tabnet_ripsa',
    'carrega_populacao_ripsa',
    'populacao_ripsa',
]


# Tabnet da Ripsa, versão 2000-2025 (NÃO usar `popsvsbr.def`, que é a versão antiga 2000-2021)
_URL_TABNET_RIPSA = 'http://tabnet.datasus.gov.br/cgi/tabcgi.exe?ibge/cnv/popsvs2024br.def'

_CAMINHO_EXTRATO_RIPSA = 'dados_locais//populacao//ripsa_populacao_rio.csv'

# todos os filtros do formulário do Tabnet; os não usados vão como 'TODAS_AS_CATEGORIAS__'
_FILTROS_TABNET_RIPSA = ['SRegião', 'SUnidade_da_Federação', 'SMunicípio', 'SCapital', 'SRegião_de_Saúde_(CIR)',
                         'SMacrorregião_de_Saúde', 'SMicrorregião_IBGE', 'SRegião_Metropolitana_-_RIDE',
                         'SMacrorregião_PNDR', 'SAmazônia_Legal', 'SSemiárido', 'SFaixa_de_Fronteira',
                         'SZona_de_Fronteira', 'SMunicípio_de_extrema_pobreza', 'SSexo', 'SFaixa_Etária_1',
                         'SFaixa_Etária_2', 'SIdade_simples']

_SEXOS_TABNET_RIPSA = {'masculino': '1', 'feminino': '2'}

def _consulta_tabnet_ripsa(anos, idades=None, sexo=None, cod_municipio_tabnet='3262', tentativas=5, espera=5):
    """Um POST no Tabnet da Ripsa: linha = ano; coluna = idade simples (se `idades`) ou só o total.
    Devolve um DataFrame indexado por ano, com uma coluna por idade (0, 1, ...) ou a coluna 'total'.

    O corpo vai em latin-1 (os nomes de campo têm acento). O servidor derruba conexões às vezes
    (`ConnectionResetError` em 2 de 5 consultas no levantamento), por isso as `tentativas`. O código
    '3262' é o código interno do Tabnet para 330455 Rio de Janeiro."""
    campos = [('Linha', 'Ano'), ('Coluna', 'Idade_simples' if idades is not None else '--Não-Ativa--'),
              ('Incremento', 'População_residente')]
    campos += [('Arquivos', f'pop{a % 100:02d}.dbf') for a in anos]
    for filtro in _FILTROS_TABNET_RIPSA:
        if filtro == 'SMunicípio':
            campos.append((filtro, cod_municipio_tabnet))
        elif filtro == 'SSexo' and sexo is not None:
            campos.append((filtro, _SEXOS_TABNET_RIPSA[sexo]))
        elif filtro == 'SIdade_simples' and idades is not None:
            campos += [(filtro, str(i + 1)) for i in idades]  # opção 1 = 'Menos que 1 ano de idade'
        else:
            campos.append((filtro, 'TODAS_AS_CATEGORIAS__'))
    campos += [('formato', 'prn'), ('mostre', 'Mostra')]
    corpo = urllib.parse.urlencode(campos, encoding='latin-1')

    for tentativa in range(1, tentativas + 1):
        try:
            r = requests.post(_URL_TABNET_RIPSA, data=corpo, timeout=120,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'})
            r.raise_for_status()
            break
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
            if tentativa == tentativas:
                raise
            time.sleep(espera * tentativa)
    texto = r.content.decode('latin-1')
    bloco = re.search(r'<PRE>(.*?)</PRE>', texto, re.S | re.I)
    if bloco is None:
        raise ValueError('resposta do Tabnet sem bloco <PRE> (formulário mudou?)')
    # leitor com aspas: o cabeçalho traz entidades HTML ('Popula&ccedil;&atilde;o') com ';' dentro das aspas
    linhas = [l.strip() for l in bloco.group(1).splitlines() if l.strip().startswith('"')]
    tabela = list(csv.reader(linhas, delimiter=';', quotechar='"'))
    df = pd.DataFrame(tabela[1:], columns=tabela[0])
    df = df[df.iloc[:, 0] != 'Total'].rename(columns={df.columns[0]: 'ano'})
    df['ano'] = df['ano'].astype(int)
    df = df.set_index('ano').replace('-', '0').astype(int)
    if idades is not None:
        df = df.drop(columns='Total')
        df.columns = list(idades)
    else:
        df.columns = ['total']
    return df

def carrega_populacao_ripsa(anos=range(2000, 2026), idades=range(0, 7), caminho_extrato=_CAMINHO_EXTRATO_RIPSA,
                            cod_municipio_tabnet='3262'):
    """População residente do município do Rio de Janeiro, estimativas Ripsa/MS (1º de julho de cada ano),
    em formato longo `ano, idade, sexo, populacao, data_consulta`:
    - idade simples em `idades` (0 = menos de 1 ano) x sexo ('masculino'/'feminino');
    - mais uma linha por ano com o total de todas as idades (`idade='total'`, `sexo='total'`).

    Lê o extrato versionado `caminho_extrato` quando ele cobre `anos` e `idades` (o notebook roda sem
    rede). Senão, consulta o Tabnet, confere a grade (anos x idades x 2 sexos) e que a soma dos sexos
    bate com o total por idade, e regrava o extrato com a data da consulta -- a Ripsa revisa as
    estimativas todo ano, então uma consulta nova pode mudar anos passados."""
    anos, idades = list(anos), list(idades)
    if os.path.exists(caminho_extrato):
        ext = pd.read_csv(caminho_extrato, dtype={'idade': str, 'sexo': str})
        idades_ext = {int(i) for i in ext['idade'] if i != 'total'}
        if set(anos) <= set(ext['ano']) and set(idades) <= idades_ext:
            manter = ext['ano'].isin(anos) & (ext['idade'].isin([str(i) for i in idades]) | (ext['idade'] == 'total'))
            return ext[manter].reset_index(drop=True)
        anos = sorted(set(anos) | set(ext['ano']))
        idades = sorted(set(idades) | idades_ext)

    partes = []
    for sexo in _SEXOS_TABNET_RIPSA:
        largo = _consulta_tabnet_ripsa(anos, idades, sexo, cod_municipio_tabnet)
        longo = largo.reset_index().melt(id_vars='ano', var_name='idade', value_name='populacao')
        longo.insert(2, 'sexo', sexo)
        partes.append(longo)
    por_sexo = pd.concat(partes, ignore_index=True)
    total_idade = _consulta_tabnet_ripsa(anos, idades, None, cod_municipio_tabnet)
    total_geral = _consulta_tabnet_ripsa(anos, None, None, cod_municipio_tabnet)

    assert len(por_sexo) == len(anos) * len(idades) * 2 and set(por_sexo['ano']) == set(anos), \
        'Ripsa: grade incompleta (anos x idades x sexos)'
    soma_sexos = por_sexo.pivot_table(index='ano', columns='idade', values='populacao', aggfunc='sum')
    assert (soma_sexos.reindex(index=total_idade.index, columns=total_idade.columns) == total_idade).all().all(), \
        'Ripsa: soma dos sexos diferente do total por idade'

    total = total_geral.reset_index().rename(columns={'total': 'populacao'})
    total['idade'], total['sexo'] = 'total', 'total'
    out = pd.concat([por_sexo, total[['ano', 'idade', 'sexo', 'populacao']]], ignore_index=True)
    out['idade'] = out['idade'].astype(str)
    out['data_consulta'] = pd.Timestamp.today().date().isoformat()
    out = out.sort_values(['ano', 'sexo', 'idade']).reset_index(drop=True)
    Path(caminho_extrato).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(caminho_extrato, index=False)
    return out

def populacao_ripsa(df_ripsa, idade_min=0, idade_max=5, sexo='total', anos=None):
    """Soma a população do longo de `carrega_populacao_ripsa` numa faixa etária (idades inteiras,
    inclusive) e devolve `ano, populacao`. `idade_min=None` e `idade_max=None` -> total de todas as
    idades. `sexo='total'` soma masculino + feminino."""
    d = df_ripsa
    if idade_min is None and idade_max is None:
        d = d[d['idade'] == 'total']
    else:
        d = d[d['idade'] != 'total']
        idade = d['idade'].astype(int)
        d = d[(idade >= idade_min) & (idade <= idade_max)]
        if sexo != 'total':
            d = d[d['sexo'] == sexo]
    if anos is not None:
        d = d[d['ano'].isin(list(anos))]
    return d.groupby('ano', as_index=False)['populacao'].sum()
