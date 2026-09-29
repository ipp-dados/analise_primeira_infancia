# -*- coding: utf-8 -*-
"""### 🗂️ CadÚnico — carregadores, recortes e privacidade

Recortes por sexo, raça/cor e arranjo familiar × renda das famílias com crianças na primeira
infância, e a regra de supressão de células pequenas aplicada a toda saída CadÚnico
sub-municipal. Ver `specs/2026-09-23_recortes_cadunico/`.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import numpy as np
import pandas as pd

__all__ = [
    '_ORDEM_RENDA_CADUNICO',
    '_ROTULOS_RENDA_CADUNICO',
    '_RENDA_CADUNICO_3_FAIXAS',
    '_ROTULOS_RENDA_CADUNICO_3',
    '_ORDEM_ARRANJO_CADUNICO',
    '_ORDEM_COMPOSICAO_SEXO',
    '_ORDEM_RACA_CADUNICO',
    '_LIMIAR_SUPRESSAO_CADUNICO',
    '_ROTULO_SEM_BAIRRO_CADUNICO',
    '_MESES_PTBR',
    'fonte_cadunico_com_particao',
    'carrega_cadunico_familias_0_6',
    'classifica_arranjo_familiar',
    'agrega_cadunico_familias',
    'agrega_cadunico_criancas',
    'atribui_bairro_por_cep',
    'suprime_celulas_pequenas',
    '_regioes_dos_bairros',
    'agrega_bairros_pequenos',
    'tabela_publicada_por_bairro',
]


# faixas de renda per capita do CTPE (`grupo_renda_pct`) -> rótulo para público não técnico.
# R$ 218 = linha de pobreza do Bolsa Família (desde 2023; specs/2026-09-29_slide_revision D1); até R$ 810,50
# (1/2 SM) = baixa renda do CadÚnico. R$ 810,50 = 1/2 salário mínimo de 2026 (R$ 1.621)
_ORDEM_RENDA_CADUNICO = ['0-218', '219-810', '811-1621', '1621-3242', '3242+']

_ROTULOS_RENDA_CADUNICO = {
    '0-218': 'Pobreza\n(até R$ 218)',
    '219-810': 'Baixa renda\n(R$ 218 a 810)',
    '811-1621': '1/2 a 1 SM\n(R$ 810 a 1.621)',
    '1621-3242': '1 a 2 SM\n(R$ 1.621 a 3.242)',
    '3242+': 'Acima de 2 SM\n(mais de R$ 3.242)',
}

# nos cruzamentos (arranjo x renda) as faixas acima de 1/2 SM se juntam -- evita células pequenas
_RENDA_CADUNICO_3_FAIXAS = {'0-218': '0-218', '219-810': '219-810',
                            '811-1621': '811+', '1621-3242': '811+', '3242+': '811+'}

_ROTULOS_RENDA_CADUNICO_3 = {'0-218': _ROTULOS_RENDA_CADUNICO['0-218'],
                             '219-810': _ROTULOS_RENDA_CADUNICO['219-810'],
                             '811+': 'Acima de 1/2 SM\n(mais de R$ 810)'}

_ORDEM_ARRANJO_CADUNICO = ['Uma adulta (mulher)', 'Dois adultos (homem e mulher)', 'Dois adultos (outra composição)',
                           'Um adulto (homem)', 'Três ou mais adultos', 'Sem adulto (18+)']

_ORDEM_COMPOSICAO_SEXO = ['Só meninas', 'Só meninos', 'Meninas e meninos']

_ORDEM_RACA_CADUNICO = ['Parda', 'Branca', 'Preta', 'Amarela', 'Indígena']

_LIMIAR_SUPRESSAO_CADUNICO = 20  # spec recortes_cadunico §5: nenhuma célula sub-municipal < 20 publicada

_ROTULO_SEM_BAIRRO_CADUNICO = 'Sem bairro identificado (CEP fora da lista)'

_MESES_PTBR = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

def fonte_cadunico_com_particao(data_particao):
    """Texto de fonte das saídas CadÚnico com o mês da extração (ex. 'CadÚnico (extração CTPE,
    jun/2026)') -- a silver só guarda uma partição, então a data é a única pista de quando o
    retrato foi tirado."""
    data = pd.Timestamp(data_particao)
    return f"CadÚnico (extração CTPE, {_MESES_PTBR[data.month - 1]}/{data.year})"

def carrega_cadunico_familias_0_6(engine):
    """Todas as pessoas (de qualquer idade) das famílias com ao menos uma criança do grupo '0-6'.

    O `df_original` da seção CadÚnico traz só as crianças; o arranjo familiar precisa dos adultos
    da mesma família. O filtro é feito no SQL (subconsulta por `id_familia`) e só as colunas usadas
    são lidas. Microdado: fica só em memória, nunca é gravado em disco (spec §5)."""
    consulta = """
        SELECT id_pessoa, id_familia, idade, grupo_idade, sexo, raca_cor, grupo_renda_pct,
               n_pessoas_familia, cep, data_particao
        FROM silver_cadunico_geral
        WHERE id_familia IN (SELECT id_familia FROM silver_cadunico_geral WHERE grupo_idade = '0-6')
    """
    return pd.read_sql(consulta, engine)

def classifica_arranjo_familiar(df_membros, idade_adulto=18):
    """Uma linha por família, com o arranjo familiar *aproximado* pela composição do cadastro.

    A silver não tem parentesco com o responsável familiar, então o arranjo é inferido contando
    os membros com `idade_adulto`+ anos e o sexo deles: 'Uma adulta (mulher)' NÃO é o conceito de
    família monoparental do MDS (que usa parentesco) -- um companheiro fora do cadastro não aparece
    (spec §3 R3). Também devolve a composição de sexo das crianças (categorias exclusivas),
    a faixa de renda per capita e o CEP das crianças (endereço da família).

    Asserções: a renda per capita é única por família e o nº de linhas por família bate com
    `n_pessoas_familia` (cadastro completo) -- se falharem, o proxy deixa de valer."""
    d = df_membros.copy()
    d['adulto'] = d['idade'] >= idade_adulto
    d['adulta'] = d['adulto'] & (d['sexo'] == 'Feminino')
    d['adulto_h'] = d['adulto'] & (d['sexo'] == 'Masculino')
    d['crianca'] = d['grupo_idade'] == '0-6'
    d['menina'] = d['crianca'] & (d['sexo'] == 'Feminino')
    d['menino'] = d['crianca'] & (d['sexo'] == 'Masculino')

    assert d.groupby('id_familia')['grupo_renda_pct'].nunique(dropna=False).max() == 1, \
        'grupo_renda_pct não é único por família'
    tamanho = d.groupby('id_familia').agg(n_linhas=('id_pessoa', 'count'), n_pessoas=('n_pessoas_familia', 'max'))
    assert (tamanho['n_linhas'] == tamanho['n_pessoas']).all(), \
        'cadastro incompleto: nº de membros na tabela != n_pessoas_familia'

    fam = d.groupby('id_familia').agg(
        n_adultos=('adulto', 'sum'), n_adultas=('adulta', 'sum'), n_adultos_h=('adulto_h', 'sum'),
        n_criancas=('crianca', 'sum'), n_meninas=('menina', 'sum'), n_meninos=('menino', 'sum'),
        idade_mais_velho=('idade', 'max'), grupo_renda_pct=('grupo_renda_pct', 'first'),
    )
    fam['cep'] = d[d['crianca']].groupby('id_familia')['cep'].first().astype(str)

    def _arranjo(r):
        if r.n_adultos == 0:
            return 'Sem adulto (18+)'
        if r.n_adultos == 1:
            return 'Uma adulta (mulher)' if r.n_adultas == 1 else 'Um adulto (homem)'
        if r.n_adultos == 2:
            return 'Dois adultos (homem e mulher)' if (r.n_adultas == 1 and r.n_adultos_h == 1) else 'Dois adultos (outra composição)'
        return 'Três ou mais adultos'
    fam['arranjo'] = fam.apply(_arranjo, axis=1)
    fam['composicao_sexo_criancas'] = np.select(
        [fam['n_meninos'] == 0, fam['n_meninas'] == 0], ['Só meninas', 'Só meninos'], default='Meninas e meninos')
    return fam.reset_index()

def agrega_cadunico_familias(df_familias, coluna, ordem):
    """Famílias, crianças (soma de `n_criancas`) e % de famílias por uma categoria EXCLUSIVA da
    família (arranjo, composição de sexo) -- como cada família está numa categoria só, as linhas
    somam e a linha 'Total' é válida."""
    t = (df_familias.groupby(coluna).agg(**{'Famílias': ('id_familia', 'count'), 'Crianças': ('n_criancas', 'sum')})
         .reindex(ordem).fillna(0).astype(int))
    t['% das famílias'] = (t['Famílias'] / t['Famílias'].sum() * 100).round(1)
    t.loc['Total'] = [t['Famílias'].sum(), t['Crianças'].sum(), 100.0]
    return t.astype({'Famílias': int, 'Crianças': int})

def agrega_cadunico_criancas(df_criancas, coluna, ordem, col_crianca='Crianças', col_familia='Famílias'):
    """Crianças (`count`) e famílias com ao menos uma criança da categoria (`nunique`) por um
    atributo DA CRIANÇA (sexo, raça/cor). As famílias NÃO são exclusivas entre categorias (uma
    família com um menino e uma menina conta nas duas), por isso não há linha de total somado --
    o total de famílias vai numa linha própria, calculado sobre a base inteira."""
    t = (df_criancas.groupby(coluna).agg(**{'Crianças': (col_crianca, 'count'), 'Famílias com ao menos uma': (col_familia, 'nunique')})
         .reindex(ordem).fillna(0).astype(int))
    t['% das crianças'] = (t['Crianças'] / len(df_criancas) * 100).round(1)
    t.loc['Total (famílias não somam)'] = [len(df_criancas), df_criancas[col_familia].nunique(), 100.0]
    return t.astype({'Crianças': int, 'Famílias com ao menos uma': int})

def atribui_bairro_por_cep(df, caminho='dados_locais/lista_bairros.csv'):
    """Mesmo join CEP -> nome de bairro da seção CadÚnico (`lista_bairros.csv`, bairro dos
    Correios), empacotado para reuso nos recortes novos. CEPs fora da lista ficam com `bairro`
    NaN (~8% das crianças, ver nota A1 da seção) -- o bairro dos Correios nem sempre é o bairro
    oficial IPP (viés documentado na nota A2)."""
    ref = pd.read_csv(caminho, dtype={'cep': str})
    out = df.copy()
    out['cep'] = out['cep'].astype(str)
    return out.merge(ref[['cep', 'bairro']], on='cep', how='left')

def suprime_celulas_pequenas(df, colunas_denominador, colunas, limiar=_LIMIAR_SUPRESSAO_CADUNICO):
    """Regra de privacidade do CadÚnico (spec recortes_cadunico §5): devolve uma CÓPIA com
    `colunas` = NaN nas linhas em que qualquer coluna de `colunas_denominador` for < `limiar`, e
    a coluna booleana `suprimido`. Usar só no que é publicado (CSV, mapa, relatório) -- cálculos e
    agregações usam sempre o dado sem supressão."""
    if isinstance(colunas_denominador, str):
        colunas_denominador = [colunas_denominador]
    out = df.copy()
    inteiras = [c for c in colunas if pd.api.types.is_integer_dtype(out[c])]
    mascara = (out[colunas_denominador] < limiar).any(axis=1)
    out.loc[mascara, colunas] = np.nan
    out[inteiras] = out[inteiras].astype('Int64')  # contagens seguem inteiras (vazio, não '15809.0')
    out['suprimido'] = mascara
    return out


# ------------------------------------------------------------------ agregação de bairros pequenos
_MINUSCULAS_NOME = {'da', 'das', 'de', 'do', 'dos', 'e'}


def _nome_ra(bruto):
    """'BARRA DA TIJUCA         ' -> 'Barra da Tijuca' (campo `regiao_adm` da camada de bairros)."""
    palavras = str(bruto).strip().lower().split()
    return ' '.join(p if (i and p in _MINUSCULAS_NOME) else p[:1].upper() + p[1:] for i, p in enumerate(palavras))


def _regioes_dos_bairros(caminho='dados_locais/geo/limite_bairros_rio.geojson'):
    """codbairro -> (codra, nome da RA, AP), da camada oficial de bairros (sem geometria)."""
    import json
    feats = json.load(open(caminho, encoding='utf-8'))['features']
    return pd.DataFrame([{'codbairro': int(f['properties']['codbairro']), 'codra': int(f['properties']['codra']),
                          'ra': _nome_ra(f['properties']['regiao_adm']), 'ap': str(f['properties']['area_plane']).strip()}
                         for f in feats])


def agrega_bairros_pequenos(df, contagens, minimos, pares=(), taxas=None, limiar=_LIMIAR_SUPRESSAO_CADUNICO,
                            nome='bairro', regioes=None):
    """Regra de privacidade do CadÚnico por agregação (specs/2026-09-29_privacidade_cadunico, D1/D2): em vez de deixar
    vazio o bairro pequeno, soma-o com os outros bairros pequenos da mesma RA ("Demais bairros da RA X"); se o conjunto
    ainda não passa no teste, com os da mesma AP; depois, no município ("Demais bairros"). Conjunto que não passa nem
    assim fica vazio (último recurso).

    `df`: uma linha por bairro, com `codbairro` e as contagens COMPLETAS (sem supressão). Um bairro (ou conjunto) passa
    quando toda coluna de `minimos` é >= `limiar` e, para cada par (numerador, denominador) de `pares`, o numerador e o
    complemento (denominador - numerador) também são -- senão o percentual publicado devolveria uma contagem pequena.
    `taxas`: {coluna: (numerador, denominador, fator)} recalculadas das somas (nunca média de percentuais).

    Devolve uma cópia com: as linhas dos bairros (os agregados com `contagens` vazias, as `taxas` do conjunto e
    `agregado_em` = nome do conjunto) e, no fim, uma linha por conjunto (`nome` = nome do conjunto, `codbairro` vazio,
    `bairros agregados`, contagens somadas e taxas). A coluna booleana `suprimido` marca o que ficou vazio.
    Usar só no que é gravado ou publicado -- cálculos usam o dado completo."""
    regioes = _regioes_dos_bairros() if regioes is None else regioes
    taxas = taxas or {}
    base = df.copy()
    base['codbairro'] = base['codbairro'].astype(int)
    for col, (num, den, fator) in taxas.items():   # taxa de cada bairro, dos absolutos
        base[col] = base[num] / base[den].where(base[den] > 0) * fator
    base = base.merge(regioes, on='codbairro', how='left', validate='many_to_one')
    if base['codra'].isna().any():
        raise ValueError(f"bairros sem RA na camada oficial: {sorted(base.loc[base['codra'].isna(), nome])}")

    def passa(linha):
        return (all(linha[c] >= limiar for c in minimos)
                and all(linha[n] >= limiar and linha[d] - linha[n] >= limiar for n, d in pares))

    base['agregado_em'] = None
    pendentes = base.index[~base.apply(passa, axis=1)]
    conjuntos = []   # (rótulo, índices)
    for nivel, rotulo in (('codra', lambda g: f"Demais bairros da RA {g['ra'].iloc[0]}"),
                          ('ap', lambda g: f"Demais bairros da AP {g['ap'].iloc[0]}"),
                          (None, lambda g: 'Demais bairros')):
        restantes = []
        grupos = [base.loc[pendentes]] if nivel is None else [g for _, g in base.loc[pendentes].groupby(nivel)]
        for g in grupos:
            if len(g) == 0:
                continue
            if passa(g[contagens].sum()):
                conjuntos.append((rotulo(g), list(g.index)))
            else:
                restantes += list(g.index)
        pendentes = restantes
    # sobra que não passa nem no município: junta aos conjuntos já formados, do menor para o maior, num único "Demais
    # bairros" -- deixar vazio abriria a conta Total - publicado = sobra (< 20)
    while pendentes and conjuntos:
        menor = min(range(len(conjuntos)), key=lambda k: base.loc[conjuntos[k][1], minimos[0]].sum())
        _, idx = conjuntos.pop(menor)
        pendentes = pendentes + idx
        if passa(base.loc[pendentes, contagens].sum()):
            conjuntos.append(('Demais bairros', pendentes))
            pendentes = []

    out = base.drop(columns=['codra', 'ra', 'ap'])
    out['suprimido'] = False
    linhas_conjunto = []
    for rotulo, idx in conjuntos:
        soma = out.loc[idx, contagens].sum()
        linha = {nome: rotulo, 'codbairro': pd.NA, 'bairros agregados': ', '.join(sorted(out.loc[idx, nome])),
                 **soma.to_dict(), 'agregado_em': None, 'suprimido': False}
        for col, (num, den, fator) in taxas.items():
            linha[col] = soma[num] / soma[den] * fator if soma[den] else np.nan
            out.loc[idx, col] = linha[col]
        out.loc[idx, contagens] = np.nan
        out.loc[idx, 'agregado_em'] = rotulo
        linhas_conjunto.append(linha)
    if pendentes:   # nem no município: vazio
        out.loc[pendentes, contagens + list(taxas)] = np.nan
        out.loc[pendentes, 'suprimido'] = True
    out = pd.concat([out, pd.DataFrame(linhas_conjunto)], ignore_index=True)
    out['codbairro'] = out['codbairro'].astype('Int64')
    for c in contagens:
        out[c] = out[c].round().astype('Int64')
    return out


def tabela_publicada_por_bairro(agregada, extras, contagens, nome='bairro', limiar=_LIMIAR_SUPRESSAO_CADUNICO,
                                rotulo_localidades='Localidades sem bairro oficial',
                                rotulo_sem_bairro=_ROTULO_SEM_BAIRRO_CADUNICO):
    """Tabela publicada por bairro = saída de `agrega_bairros_pequenos` + linhas extras, na ordem de `extras`
    ({rótulo: {coluna: contagem}}, ex. localidades dos Correios sem bairro oficial, "Sem bairro identificado",
    "Total"). A linha de localidades que não passa no limiar é somada à de "Sem bairro identificado" (não se publica
    um conjunto pequeno). "Total" é o município (sem limiar)."""
    extras = {k: dict(v) for k, v in extras.items()}
    loc = extras.get(rotulo_localidades)
    if loc is not None and any(loc[c] < limiar for c in contagens) and rotulo_sem_bairro in extras:
        for c in contagens:
            extras[rotulo_sem_bairro][c] += loc[c]
        extras[rotulo_sem_bairro]['bairros agregados'] = rotulo_localidades
        del extras[rotulo_localidades]
    linhas = [{nome: k, **v} for k, v in extras.items()]
    out = pd.concat([agregada, pd.DataFrame(linhas)], ignore_index=True)
    for c in contagens:
        out[c] = out[c].astype('Int64')
    return out

