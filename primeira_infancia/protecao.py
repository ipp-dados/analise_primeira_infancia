# -*- coding: utf-8 -*-
"""### 🛡️ Proteção — carregadores e utilitários

Funções do eixo Proteção (violência familiar/autoprovocada — Sinan/Tabnet por bairro;
violência territorial — Data.Rio/IPS por Região Administrativa) e utilitários de taxa e de
agregação geográfica. Ver `specs/2026-09-23_inclusao_dados_protecao/`.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import geopandas as gpd
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import unicodedata
from pathlib import Path
from .estilo import _FONTE_TITULO, _PALETA_CATEGORICA
from .impressao import _a4_ranking, _a4_series
from .graficos import _rodape_fonte
from .mapas import _NIVEIS_AGREGACAO, _RA_PARA_CAP, agrega_bairros_por_nivel

__all__ = [
    '_CAMINHO_GEO_BAIRROS',
    '_VINCULOS_VIOLENCIA_FAMILIAR',
    '_VINCULOS_OUTROS',
    '_ALIAS_RA_IPS',
    '_sem_acento_maiusculo',
    'numeral_romano_para_int',
    '_bairros_referencia',
    'carrega_sinan_bairro',
    'carrega_violencia_familiar',
    'carrega_violencia_territorial_ra',
    'carrega_pop_0_4_bairro',
    'taxa_por_mil',
    'bairro_para_nivel',
    'serie_temporal_multipla_marcos',
    'grafico_barra_ranking',
    'agrega_violencia_familiar_nivel',
    '_limite_escala_p95',
]


_CAMINHO_GEO_BAIRROS = 'dados_locais/geo/limite_bairros_rio.geojson'

# vínculo do provável autor -> arquivo Sinan/Tabnet (violência familiar, 0 a 5 anos)
_VINCULOS_VIOLENCIA_FAMILIAR = {
    'mae': 'violencia_familiar_mae.csv',
    'pai': 'violencia_familiar_pai.csv',
    'padrasto': 'violencia_familiar_padrasto.csv',
    'irmao': 'violencia_familiar_irmao(a).csv',
    'conjuge': 'violencia_familiar_conjuge.csv',
    'exconjuge': 'violencia_familiar_exconjuge.csv',
    'filho': 'violencia_familiar_filho(a).csv',
}

# vínculos agrupados em 'outros' (mãe e pai ficam de fora e nunca são somados entre si)
_VINCULOS_OUTROS = ['padrasto', 'irmao', 'conjuge', 'exconjuge', 'filho']

# grafia do IPS/Data.Rio que difere do geojson de bairros (regiao_adm), só para a checagem cruzada
_ALIAS_RA_IPS = {'SANTA TERESA': 'SANTA TEREZA'}

def _sem_acento_maiusculo(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(texto)) if not unicodedata.combining(c)).upper().strip()

def numeral_romano_para_int(s):
    """Converte um numeral romano (ex.: 'XXXIV') em inteiro (34) -- usado no de-para RA do IPS."""
    valores = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    s = s.strip().upper()
    if not s or any(c not in valores for c in s):
        raise ValueError(f'numeral romano inválido: {s!r}')
    total = 0
    for atual, proximo in zip(s, s[1:] + ' '):
        v = valores[atual]
        total += -v if proximo in valores and valores[proximo] > v else v
    return total

def _bairros_referencia(caminho_geojson=_CAMINHO_GEO_BAIRROS):
    """Tabela dos 166 bairros do geojson (codbairro int, nome, codra int, cod_rp, area_plane)."""
    g = gpd.read_file(caminho_geojson).drop(columns='geometry')
    g['codbairro'] = g['codbairro'].astype(int)
    g['codra'] = g['codra'].astype(int)
    g['regiao_adm'] = g['regiao_adm'].str.strip()  # o geojson traz espaços à direita em algumas RAs
    return g[['codbairro', 'nome', 'regiao_adm', 'codra', 'cod_rp', 'area_plane']].sort_values('codbairro').reset_index(drop=True)

def carrega_sinan_bairro(caminho, categoria, anos_validos):
    """Lê um export Sinan NET/Tabnet por bairro de residência (6 linhas de metadados, latin-1, formato
    largo com colunas de ano esparsas) e devolve o formato longo `codbairro, bairro, ano, <categoria>`
    numa grade completa dos 166 bairros do geojson x `anos_validos`, com 0 onde não havia linha
    (bairro sem caso = 0, não ausente). A linha de filtro do export vai em `df.attrs['filtro']`."""
    with open(caminho, encoding='latin-1') as f:
        filtro = [next(f).strip() for _ in range(6)][4]
    df = pd.read_csv(caminho, sep=';', encoding='latin-1', skiprows=6)
    df = df.rename(columns={df.columns[0]: 'bairro_resid'})
    df = df[df['bairro_resid'] != 'Total']
    df[['codbairro', 'bairro']] = df['bairro_resid'].str.split(n=1, expand=True)
    df['codbairro'] = df['codbairro'].astype(int)
    colunas_ano = [c for c in df.columns if str(c).isdigit()]
    longo = df.melt(id_vars=['codbairro'], value_vars=colunas_ano, var_name='ano', value_name=categoria)
    longo['ano'] = longo['ano'].astype(int)
    ref = _bairros_referencia()
    assert set(longo['codbairro']) <= set(ref['codbairro']), 'código de bairro do Sinan fora do geojson'
    grade = ref[['codbairro', 'nome']].rename(columns={'nome': 'bairro'}).merge(pd.DataFrame({'ano': list(anos_validos)}), how='cross')
    out = grade.merge(longo, on=['codbairro', 'ano'], how='left')
    out[categoria] = out[categoria].fillna(0).astype(int)
    out.attrs['filtro'] = filtro
    return out

def carrega_violencia_familiar(pasta, anos_validos):
    """Lê os 7 exports de violência familiar por vínculo (mãe, pai, padrasto, irmão(ã), cônjuge,
    ex-cônjuge, filho(a)) e devolve um longo `vinculo, codbairro, bairro, ano, casos`. Acrescenta o
    vínculo `outros` (padrasto + irmão(ã) + cônjuge + ex-cônjuge + filho(a)) SEM remover os originais.
    Os vínculos não são excludentes: nunca somar mãe + pai, nem tratar `outros` como total."""
    partes = []
    for vinculo, arquivo in _VINCULOS_VIOLENCIA_FAMILIAR.items():
        d = carrega_sinan_bairro(Path(pasta) / arquivo, 'casos', anos_validos)
        d.insert(0, 'vinculo', vinculo)
        partes.append(d)
    longo = pd.concat(partes, ignore_index=True)
    outros = (longo[longo['vinculo'].isin(_VINCULOS_OUTROS)]
              .groupby(['codbairro', 'bairro', 'ano'], as_index=False)['casos'].sum())
    outros.insert(0, 'vinculo', 'outros')
    return pd.concat([longo, outros], ignore_index=True)

def carrega_violencia_territorial_ra(caminho):
    """Lê `violencia_territorial.xlsx` (Data.Rio/IPS 2024, por Região Administrativa; todas as idades).
    Devolve `codra, regiao_adm, taxa_homicidios, homicidios_acao_policial, homicidios_jovens_negros`
    (32 RAs); a linha 'RIO DE JANEIRO' (referência municipal) vai em `df.attrs['municipio']`.
    A chave é o numeral romano do IPS convertido em `codra`; o nome só serve de checagem cruzada."""
    bruto = pd.read_excel(caminho, header=None)
    linha_cab = next(i for i, v in bruto[1].items() if 'homic' in _sem_acento_maiusculo(v).lower())
    dados = bruto.iloc[linha_cab + 1:, :4].dropna(how='all').copy()
    dados.columns = ['regiao', 'taxa_homicidios', 'homicidios_acao_policial', 'homicidios_jovens_negros']
    cols_num = ['taxa_homicidios', 'homicidios_acao_policial', 'homicidios_jovens_negros']
    dados[cols_num] = dados[cols_num].astype(float)
    eh_municipio = dados['regiao'].str.strip().str.upper() == 'RIO DE JANEIRO'
    municipio = dados[eh_municipio].iloc[0]
    ras = dados[~eh_municipio].copy()
    ras['codra'] = ras['regiao'].str.split().str[0].map(numeral_romano_para_int)
    ras['nome_ips'] = ras['regiao'].str.split(n=1).str[1].map(_sem_acento_maiusculo)
    ref = _bairros_referencia()[['codra', 'regiao_adm']].drop_duplicates('codra')
    ras = ras.merge(ref, on='codra', how='left')
    assert ras['regiao_adm'].notna().all(), 'RA do IPS sem correspondência no geojson'
    esperado = ras['regiao_adm'].map(_sem_acento_maiusculo)
    assert (ras['nome_ips'].map(lambda n: _ALIAS_RA_IPS.get(n, n)) == esperado).all(), 'nome da RA diverge do geojson'
    out = ras[['codra', 'regiao_adm'] + cols_num].sort_values('codra').reset_index(drop=True)
    out.attrs['municipio'] = {c: float(municipio[c]) for c in cols_num}
    return out

def carrega_pop_0_4_bairro(caminho='dados_locais/censo/pop_censo_2022_datario.csv'):
    """População de 0 a 4 anos por bairro (Censo 2022) -- `codbairro, pop_0_4`. Lê o CSV direto,
    sem depender de `df_censo` ter sido calculado antes."""
    d = pd.read_csv(caminho, encoding='latin-1', sep=';')
    return d[['codbairro', '0 a 4 anos']].rename(columns={'0 a 4 anos': 'pop_0_4'}).astype({'codbairro': int})

def taxa_por_mil(df, col_casos, col_pop, nome_taxa='taxa_por_mil'):
    """Taxa por 1.000 = casos / população * 1000. Chamar SEMPRE depois de somar casos e população
    no nível desejado (nunca média de taxas). População 0 ou ausente -> NaN (nunca inf)."""
    df = df.copy()
    pop = df[col_pop].where(df[col_pop] > 0)
    df[nome_taxa] = df[col_casos] / pop * 1000
    return df

def bairro_para_nivel(df, nivel, chave='codbairro'):
    """Anexa a `df` (tabela por bairro) a coluna administrativa do nível: 'ra' -> codra; 'cap' ->
    cod_ap_sms (via `_RA_PARA_CAP` sobre codra); 'rp' -> cod_rp; 'ap' -> area_plane. Serve para
    depois somar contagens com `agrega_bairros_por_nivel` (e só então recalcular taxas)."""
    ref = _bairros_referencia()
    ref['cod_ap_sms'] = ref['codra'].map(_RA_PARA_CAP)
    coluna = _NIVEIS_AGREGACAO[nivel]['coluna_geo']
    if coluna not in ref.columns:
        raise ValueError(f'nível {nivel!r} não suportado por bairro_para_nivel')
    return df.merge(ref[['codbairro', coluna]].rename(columns={'codbairro': chave}), on=chave, how='left')

def serie_temporal_multipla_marcos(df,tempo,colunas,titulo,nome_arquivo,marcos=None,ylabel='Valor',legend_title='Vínculo',figsize=(12,6),formato='png', fonte_dados=None):
    """Como `serie_temporal_multipla` (mesmo estilo/paleta), com linhas verticais tracejadas anotadas
    em `marcos` ({ano: 'texto'}) -- ex.: possível quebra de série. Função à parte para não alterar a
    assinatura da original."""
    plt.figure(figsize=figsize)
    for i,(rotulo,coluna) in enumerate(colunas.items()):
        sns.lineplot(x=tempo,y=coluna,data=df,label=rotulo,marker='o',errorbar=None,
                     color=_PALETA_CATEGORICA[i % len(_PALETA_CATEGORICA)])
    topo = plt.gca().get_ylim()[1]
    for ano,texto in (marcos or {}).items():
        plt.axvline(ano, color='#6b6b6b', linestyle='--', linewidth=1.1, zorder=0)
        plt.annotate(texto, xy=(ano, topo), xytext=(4, -6), textcoords='offset points', ha='left', va='top',
                     fontsize=9, color='#3a3a3a', style='italic')
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xlabel(tempo,fontsize=12)
    plt.ylabel(ylabel,fontsize=12)
    plt.title(titulo,fontsize=15,fontfamily=_FONTE_TITULO,fontweight='bold',pad=12)
    plt.legend(title=legend_title,fontsize=9,loc='upper left')
    plt.grid(True,alpha=0.3)
    _rodape_fonte(fonte_dados)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    _a4_series(df, tempo, colunas, titulo, nome_arquivo=nome_arquivo, ylabel=ylabel, fonte_dados=fonte_dados,
               marcos=marcos)
    plt.show()

def grafico_barra_ranking(df,categoria,valor,titulo,nome_arquivo,xlabel=None,linha_referencia=None,rotulo_referencia=None,cmap='OrRd',figsize=(10,9),formato='png', fonte_dados=None):
    """Barras horizontais ordenadas (maior no topo), com linha vertical opcional de referência (ex.: valor
    do município). Uma cor sequencial só (magnitude), do tema `cmap`."""
    d = df.sort_values(valor, ascending=True)
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(d[categoria].astype(str), d[valor], color=plt.get_cmap(cmap)(0.62))
    if linha_referencia is not None:
        ax.axvline(linha_referencia, color='#262626', linestyle='--', linewidth=1.2)
        ax.annotate(rotulo_referencia or f'{linha_referencia:.1f}', xy=(linha_referencia, 0.02), xycoords=('data','axes fraction'),
                    xytext=(4, 0), textcoords='offset points', ha='left', va='bottom', fontsize=9, color='#262626')
    ax.set_xlabel(xlabel or valor, fontsize=12)
    ax.set_title(titulo, fontsize=15, fontfamily=_FONTE_TITULO, fontweight='bold', pad=12)
    ax.grid(True, axis='x', alpha=0.3)
    ax.set_axisbelow(True)
    _rodape_fonte(fonte_dados)
    plt.tight_layout(rect=(0, 0.03, 1, 1))  # reserva a base para o rodapé de fonte
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    _a4_ranking(df, categoria, valor, titulo, nome_arquivo=nome_arquivo, xlabel=xlabel, linha_referencia=linha_referencia,
                rotulo_referencia=rotulo_referencia, cmap=cmap, fonte_dados=fonte_dados)
    plt.show()

def agrega_violencia_familiar_nivel(df_bairro, df_pop, nivel, vinculos=('mae', 'pai', 'outros')):
    """Agrega a tabela por bairro x ano de violência familiar (colunas `vinculos`) e a população 0-4
    para 'ra' ou 'cap': soma casos e população por ano e SÓ ENTÃO recalcula a taxa por 1.000 de cada
    vínculo (`taxa_por_mil_<vinculo>`), nunca média de taxas de bairro. Não soma vínculos entre si."""
    base = bairro_para_nivel(df_bairro.merge(df_pop, on='codbairro'), nivel)
    partes = []
    for ano, d in base.groupby('ano'):
        a = agrega_bairros_por_nivel(d, nivel, list(vinculos) + ['pop_0_4'])
        a.insert(1, 'ano', ano)
        partes.append(a)
    out = pd.concat(partes, ignore_index=True)
    for v in vinculos:
        out = taxa_por_mil(out, v, 'pop_0_4', f'taxa_por_mil_{v}')
    return out

def _limite_escala_p95(serie):
    """Limite superior da escala de cor: percentil 95 arredondado para cima (múltiplo de 5)."""
    return int(math.ceil(serie.quantile(0.95) / 5) * 5)
