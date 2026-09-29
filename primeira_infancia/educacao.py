# -*- coding: utf-8 -*-
"""### 🎓 Censo Escolar (INEP) — carregadores

Matrículas de 0 a 5 anos no município, direto dos microdados do Censo Escolar da Educação Básica/INEP
(uma linha por escola, com matrículas agregadas em faixas de idade desde a adequação à LGPD). Ver
`specs/2026-09-24_populacao-referencia/matriculas/`.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import os
import pandas as pd
import re
import requests
import time
import zipfile
from pathlib import Path
from .populacao import populacao_ripsa

__all__ = [
    '_URL_INEP_MICRODADOS',
    '_ZIP_INEP_EXCECOES',
    '_CAMINHO_EXTRATO_INEP',
    '_DEPENDENCIAS_INEP',
    '_COLUNAS_MATRICULA_INEP',
    '_baixa_zip_inep',
    '_le_matriculas_zip_inep',
    'carrega_censo_escolar_matriculas',
    'resume_matriculas_0_a_5',
]


_URL_INEP_MICRODADOS = 'https://download.inep.gov.br/dados_abertos/'

_ZIP_INEP_EXCECOES = {2025: 'microdados_censo_escolar_2025_.zip'}  # 2025 saiu com '_' no fim do nome

_CAMINHO_EXTRATO_INEP = 'dados_locais//educacao//inep_matriculas_rio.csv'

_DEPENDENCIAS_INEP = {1: 'federal', 2: 'estadual', 3: 'municipal', 4: 'privada'}

# contagens por escola: faixas de idade (data padrão do Censo, última quarta-feira de maio) e etapas.
# As colunas '_REF_31_03' de 2025 (idade em 31/03) não são usadas: não existem nos outros anos.
_COLUNAS_MATRICULA_INEP = {'QT_MAT_BAS_0_3': 'mat_0_a_3', 'QT_MAT_BAS_4_5': 'mat_4_a_5', 'QT_MAT_INF': 'mat_inf',
                           'QT_MAT_INF_CRE': 'mat_inf_creche', 'QT_MAT_INF_PRE': 'mat_inf_pre'}

def _baixa_zip_inep(ano, pasta_cache, tentativas=5, espera=10):
    """Baixa o ZIP de microdados do ano para o cache (gitignorado), se ainda não estiver lá."""
    destino = Path(pasta_cache) / f'microdados_censo_escolar_{ano}.zip'
    if destino.exists():
        return destino
    destino.parent.mkdir(parents=True, exist_ok=True)
    url = _URL_INEP_MICRODADOS + _ZIP_INEP_EXCECOES.get(ano, f'microdados_censo_escolar_{ano}.zip')
    for tentativa in range(1, tentativas + 1):
        try:
            with requests.get(url, stream=True, timeout=300) as r:
                r.raise_for_status()
                parcial = destino.with_suffix('.zip.part')
                with open(parcial, 'wb') as f:
                    for bloco in r.iter_content(chunk_size=1 << 20):
                        f.write(bloco)
            parcial.rename(destino)
            return destino
        except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
            if tentativa == tentativas:
                raise
            time.sleep(espera * tentativa)

def _le_matriculas_zip_inep(caminho_zip, ano, cod_municipio):
    """Lê, de dentro do ZIP (sem extrair), o CSV com as contagens de matrícula por escola e devolve as
    somas do município por dependência administrativa. Até 2024 as contagens estão em
    `microdados_ed_basica_<ano>.csv` (.CSV em alguns anos); em 2025, na `Tabela_Matricula_<ano>*.csv`."""
    padrao = re.compile(rf'(microdados_ed_basica_{ano}|tabela_matricula_{ano}[^/]*)\.csv$', re.I)
    with zipfile.ZipFile(caminho_zip) as zf:
        nomes = [n for n in zf.namelist() if padrao.search(n)]
        if len(nomes) != 1:
            raise ValueError(f'{ano}: esperado 1 CSV de matrículas no ZIP, achados {nomes}')
        colunas = ['CO_MUNICIPIO', 'TP_DEPENDENCIA'] + list(_COLUNAS_MATRICULA_INEP)
        with zf.open(nomes[0]) as f:
            df = pd.read_csv(f, sep=';', encoding='latin-1', usecols=lambda c: c in colunas, low_memory=False)
    faltando = set(colunas) - set(df.columns)
    if {'QT_MAT_BAS_0_3', 'QT_MAT_BAS_4_5'} & faltando:
        raise ValueError(f'{ano}: sem as colunas de faixa etária {sorted(faltando)} (P6)')
    df = df[df['CO_MUNICIPIO'] == cod_municipio]
    agregado = (df.groupby('TP_DEPENDENCIA')[[c for c in _COLUNAS_MATRICULA_INEP if c in df.columns]].sum()
                .reindex(list(_DEPENDENCIAS_INEP), fill_value=0).astype(int).rename(columns=_COLUNAS_MATRICULA_INEP))
    agregado = agregado.rename_axis('tp_dependencia').reset_index()
    agregado.insert(0, 'ano', ano)
    agregado.insert(2, 'dependencia', agregado['tp_dependencia'].map(_DEPENDENCIAS_INEP))
    return agregado

def carrega_censo_escolar_matriculas(anos, cod_municipio=3304557, pasta_cache='dados_locais//educacao//inep_microdados',
                                     caminho_extrato=_CAMINHO_EXTRATO_INEP):
    """Matrículas da educação básica no município por ano x dependência administrativa (federal,
    estadual, municipal, privada): `ano, tp_dependencia, dependencia, mat_0_a_3, mat_4_a_5, mat_inf,
    mat_inf_creche, mat_inf_pre` (as colunas `mat_inf*`, por etapa, ficam só como referência).

    Lê o extrato versionado `caminho_extrato` quando ele cobre `anos` (o notebook roda sem rede e sem os
    ZIPs). Senão, baixa os ZIPs faltantes para o cache gitignorado, lê cada ano de dentro do ZIP e
    regrava o extrato. Só contagens agregadas por escola: não há dado pessoal."""
    anos = list(anos)
    extrato = pd.read_csv(caminho_extrato) if os.path.exists(caminho_extrato) else None
    if extrato is not None and set(anos) <= set(extrato['ano']):
        return extrato[extrato['ano'].isin(anos)].reset_index(drop=True)
    ja_lidos = set(extrato['ano']) if extrato is not None else set()
    partes = [extrato] if extrato is not None else []
    for ano in sorted(set(anos) - ja_lidos):
        partes.append(_le_matriculas_zip_inep(_baixa_zip_inep(ano, pasta_cache), ano, cod_municipio))
    out = pd.concat(partes, ignore_index=True).sort_values(['ano', 'tp_dependencia']).reset_index(drop=True)
    assert out.groupby('ano').size().eq(len(_DEPENDENCIAS_INEP)).all(), 'extrato INEP: ano sem as 4 dependências'
    out.to_csv(caminho_extrato, index=False)
    return out[out['ano'].isin(anos)].reset_index(drop=True)

def resume_matriculas_0_a_5(df_matriculas, df_ripsa):
    """Tabela final por ano: matrículas de 0 a 5 anos (total, 0-3, 4-5, pública, privada), população
    Ripsa das mesmas faixas e a taxa bruta de atendimento (%) de cada faixa. A taxa de 0-5 é
    (mat 0-3 + mat 4-5) ÷ (pop 0-3 + pop 4-5), nunca a média das taxas de 0-3 e 4-5."""
    m = df_matriculas.assign(mat_0_a_5=df_matriculas['mat_0_a_3'] + df_matriculas['mat_4_a_5'])
    publica = m['tp_dependencia'].isin([1, 2, 3])
    out = m.groupby('ano').agg(matriculas=('mat_0_a_5', 'sum'), matriculas_0_a_3=('mat_0_a_3', 'sum'),
                               matriculas_4_a_5=('mat_4_a_5', 'sum'))
    out['matriculas_publica'] = m[publica].groupby('ano')['mat_0_a_5'].sum()
    out['matriculas_privada'] = m[~publica].groupby('ano')['mat_0_a_5'].sum()
    for faixa, (ini, fim) in {'0_a_3': (0, 3), '4_a_5': (4, 5), '0_a_5': (0, 5)}.items():
        out[f'populacao_{faixa}'] = populacao_ripsa(df_ripsa, ini, fim).set_index('ano')['populacao']
    for faixa in ['0_a_3', '4_a_5', '0_a_5']:
        numerador = out['matriculas'] if faixa == '0_a_5' else out[f'matriculas_{faixa}']
        out[f'taxa_atendimento_{faixa}'] = (numerador / out[f'populacao_{faixa}'] * 100).round(1)
    return out.reset_index()
