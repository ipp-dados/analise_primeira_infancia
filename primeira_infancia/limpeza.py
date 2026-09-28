# -*- coding: utf-8 -*-
"""### 🧹 Limpeza e wrangling de dados

Limpeza das exportações do Tabnet/DataSUS (código numérico do bairro como chave), SISVAN, óbitos por causas evitáveis (raça/cor, grupo/subgrupo CID-10, CAP), cobertura vacinal e tabelas do SIDRA em formato longo.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import pandas as pd
from pathlib import Path

__all__ = [
    'limpa_dados_sisvan',
    'limpa_dados_datasus',
    'limpeza_tabnet_bairros',
    'carrega_raca_bairro',
    'carrega_causas_evitaveis_raca',
    'carrega_causas_evitaveis_categoria',
    'combina_faixas_causa',
    'total_e_percentual_ano',
    'carrega_cobertura_vacinal',
    '_ROTULO_PARA_SUBGRUPO',
    '_GRUPOS_CID',
    'extrai_evitaveis_cap_blocos',
    'extrai_evitaveis_municipio',
    'extrai_planilha_evitaveis_cap',
    'agrega_grupo_cid',
    'subgrupo_excluido',
    'filtra_colunas_subgrupo',
    'agrupa_racas_raras',
    'junta_codbairro_por_bairro',
    'carrega_sidra_longo',
]


def limpa_dados_sisvan(colunas, dataset):
    path = Path(f"dados_locais/sisvan/{dataset}/")
    arquivos = [f.name for f in path.iterdir() if f.is_file() and not f.name.startswith('.') and f.name != 'example_file']

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
        df = pd.read_excel(f"dados_locais/sisvan/{dataset}/{arquivo}")
        df_infos = df.iloc[[10],5:]
        df_infos.columns = colunas_ajustadas[1:]
        df_infos['ano'] = arquivo[-9:-5]
        df_final = pd.concat([df_final,df_infos])
    df_final.reset_index(inplace=True, drop=True)

    df_final.to_csv(f"dados_locais/tratados/{dataset}.csv")

def limpa_dados_datasus(df):
    df = df.melt(id_vars=['Bairro Residencia'])
    return df

def limpeza_tabnet_bairros(df,categoria):
    """Padroniza um export do Tabnet: extrai 'codigo' e 'bairro', remove linhas 'Total'."""
    df.columns = ['bairro','ano',categoria]
    df = df[df['bairro']!='Total']
    df = df[df['ano']!='Total']
    df[['codigo','bairro']] = df.loc[df['bairro']!='EM BRANCO','bairro'].str.split(' ', n=1,expand=True)
    return df

def carrega_raca_bairro(caminho, categoria, anos_validos, sep=';'):
    """Lê um export do Tabnet por bairro e reindexa numa grade bairro x ano completa,
    preenchendo com 0 os anos sem linha no arquivo original (evita contagens incompletas
    em somas/subtrações posteriores)."""
    df = pd.read_csv(caminho, sep=sep)
    df = limpa_dados_datasus(df)
    df = limpeza_tabnet_bairros(df, categoria=categoria)
    df = df.dropna(subset=['codigo', 'bairro'])
    df['ano'] = df['ano'].astype(int)
    grade = df[['codigo', 'bairro']].drop_duplicates().merge(pd.DataFrame({'ano': anos_validos}), how='cross')
    df = grade.merge(df[['codigo', 'bairro', 'ano', categoria]], on=['codigo', 'bairro', 'ano'], how='left')
    df[categoria] = df[categoria].fillna(0)
    df['ano'] = df['ano'].astype(str)
    return df

def carrega_causas_evitaveis_raca(caminho, categoria):
    """Lê um export Tabnet de causas evitáveis por raça/cor (nível município), em formato largo
    (ano nas colunas), e retorna em formato longo (raca, ano, categoria)."""
    df = pd.read_csv(caminho, sep=';', encoding='latin-1')
    df = df.rename(columns={df.columns[0]: 'raca'})
    df['raca'] = df['raca'].str.strip()
    df = df[df['raca'].isin(['Branca','Preta','Amarela','Parda','Indígena','Ignorado'])]
    df = df.drop(columns=['Total'])
    df = df.melt(id_vars=['raca'], var_name='ano', value_name=categoria)
    df[categoria] = df[categoria].replace('-', 0).astype(float)
    mapa_raca = {'Branca':'branca','Preta':'preta','Amarela':'amarela','Parda':'parda',
                 'Indígena':'indigena','Ignorado':'nao_informado'}
    df['raca'] = df['raca'].map(mapa_raca)
    return df

def carrega_causas_evitaveis_categoria(caminho, padrao):
    """Lê um export Tabnet 'segundo causas' (hierarquia grupo/subgrupo/causa, nível município)
    e filtra as linhas cujo rótulo bate com `padrao` (grupo ou subgrupo)."""
    df = pd.read_csv(caminho, sep=';', encoding='latin-1')
    df = df.rename(columns={df.columns[0]: 'causa'})
    df = df[df['causa'].notna()]
    df = df[df['causa'].str.match(padrao)]
    df = df.drop(columns=['Total'])
    df = df.melt(id_vars=['causa'], var_name='ano', value_name='obitos')
    df['obitos'] = df['obitos'].replace('-', 0).astype(float)
    df['ano'] = df['ano'].astype(int)
    return df

def combina_faixas_causa(padrao, arquivos_por_faixa):
    """Aplica `carrega_causas_evitaveis_categoria` a cada faixa etária em `arquivos_por_faixa`
    e soma o resultado por causa/ano (usado para obter o total 0-364 dias)."""
    df_total = None
    for caminho in arquivos_por_faixa.values():
        df_faixa = carrega_causas_evitaveis_categoria(caminho, padrao)
        df_total = df_faixa if df_total is None else pd.concat([df_total, df_faixa])
    return df_total.groupby(['causa','ano'], as_index=False)['obitos'].sum()

def total_e_percentual_ano(df):
    """Agrega um Censo (Tabela 2974/IBGE) por bairro em total e percentual de 0 a 4 anos.

    O `Total` é somado ANTES de criar a coluna '0 a 4 anos' -- na ordem inversa, a faixa de 0 a 4 anos
    entrava duas vezes no total (populacao-referencia, auditoria de faixas §2; com a correção, os totais
    de 2000 e 2010 batem com o IBGE: 5.857.904 e 6.320.446)."""
    df['Total'] = df.iloc[:,9:].sum(axis=1)
    df['0 a 4 anos'] = df['Sexo feminino, 0 a 4 anos'] + df['Sexo masculino, 0 a 4 anos']
    df['Percentual 0 a 4 anos'] = (df['0 a 4 anos']/df['Total'])
    return df[['bairro','0 a 4 anos','Total','Percentual 0 a 4 anos','Sexo feminino, 0 a 4 anos','Sexo masculino, 0 a 4 anos']]

def carrega_cobertura_vacinal(caminho):
    """Lê um export do EPI/SVS-Rio de cobertura vacinal por imunobiológico e ano."""
    df = pd.read_csv(caminho, sep=';')
    df['ano_num'] = pd.to_numeric(df['ANO'], errors='coerce')
    df = df[df['ano_num'].notna()]
    df['ano'] = df['ano_num'].astype(int)
    df['cobertura'] = df['COBERTURA'].str.replace('%','',regex=False).str.replace(',','.',regex=False).astype(float)
    return df[['ano','IMUNO','cobertura']].rename(columns={'IMUNO':'imunobiologico'})

# a planilha TabWin de causas evitáveis por CAP só traz os 8 subgrupos CID (nunca o nível
# 'grupo' como linha própria, e nunca um terceiro nível 'causa' -- ver specs/2026-09-08_mortalidade-ap/
# specification.md §2.4); o rótulo bruto de 3 das 8 categorias ('1.2.*') traz um trecho 'ad '
# redundante que não aparece no texto de subgrupo canônico -- este dicionário normaliza os 8
# rótulos possíveis para esse texto canônico, usado em toda tabela derivada desta planilha
_ROTULO_PARA_SUBGRUPO = {
    '1.1. Reduzível pelas ações de imunização':    '1.1. Reduzível pelas ações de imunização',
    '1.2.1. Red por ad at à mulher na gestação':   '1.2.1. Red por at à mulher na gestação',
    '1.2.2. Red por ad at à mulher no parto':      '1.2.2. Red por at à mulher no parto',
    '1.2.3. Red por ad at ao recém-nascido':       '1.2.3. Red por at ao recém-nascido',
    '1.3. Red por ações de diag e trat adequado':  '1.3. Red por ações de diag e trat adequado',
    '1.4. Red por ações promoção vinc a atenção':  '1.4. Red por ações promoção vinc a atenção',
    '2. Causas mal definidas':                     '2. Causas mal definidas',
    '3. Demais causas (não claramente evitáveis)': '3. Demais causas (não claramente evitáveis)',
}

_GRUPOS_CID = {'1': '1. Causas evitáveis',
               '2': '2. Causas mal definidas',
               '3': '3. Demais causas (não claramente evitáveis)'}

def extrai_evitaveis_cap_blocos(caminho, aba, anos=range(2006, 2026)):
    """Lê uma aba 'por CAP' (`<1 ano` / `1-4 anos` / `<5 anos`) da planilha de causas evitáveis
    na primeira infância (TabWin) e devolve formato longo `cod_ap_sms, subgrupo, ano, obitos`.

    A aba é uma pilha de 10 blocos de 12 linhas, um por Área Programática de Saúde (CAP):
    título (carrega o código da CAP, ex. 'AP 3.1'), cabeçalho, 8 categorias CID, 'Total' e uma
    linha em branco. Passo fixo de 12 linhas (não busca por regex de título) -- o layout do
    TabWin é rígido e um passo fixo falha ruidosamente (IndexError) se a planilha mudar, o que
    é preferível a falhar em silêncio. A linha 'Total' é descartada -- é recalculável e
    entraria em dupla contagem em qualquer groupby posterior.
    """
    df = pd.read_excel(caminho, sheet_name=aba, header=None)
    registros = []
    for inicio in range(0, len(df), 12):
        cod_ap_sms = df.iloc[inicio, 0].split(', AP ')[1].split(',')[0]
        for linha in range(inicio + 2, inicio + 10):
            subgrupo = _ROTULO_PARA_SUBGRUPO[df.iloc[linha, 0].strip()]
            for ano, obitos in zip(anos, df.iloc[linha, 1:21]):
                registros.append((cod_ap_sms, subgrupo, ano, int(obitos)))
    return pd.DataFrame(registros, columns=['cod_ap_sms', 'subgrupo', 'ano', 'obitos'])

def extrai_evitaveis_municipio(caminho):
    """Lê a aba 'Informações gerais' (nível município, < 5 anos) da planilha de causas
    evitáveis na primeira infância e devolve as três tabelas empilhadas nela, como uma tupla
    de DataFrames `(por_subgrupo, por_cap, taxa)`. Índices de linha fixos (2-9 / 14-25 /
    31-33), pelo mesmo motivo de `extrai_evitaveis_cap_blocos`.

    As linhas ' Ign' e ' Ignorado' da tabela por CAP (CAP de residência não registrada, sob
    dois rótulos diferentes ao longo da série) são somadas numa única categoria 'Ignorado' --
    o mesmo padrão já usado no notebook para `mae_ignorado` + `mae_nao_informado`.
    """
    df = pd.read_excel(caminho, sheet_name='Informações gerais', header=None)
    anos = list(range(2006, 2026))

    registros_subgrupo = []
    for linha in range(2, 10):
        subgrupo = _ROTULO_PARA_SUBGRUPO[df.iloc[linha, 0].strip()]
        for ano, obitos in zip(anos, df.iloc[linha, 1:21]):
            registros_subgrupo.append((subgrupo, ano, int(obitos)))
    por_subgrupo = pd.DataFrame(registros_subgrupo, columns=['subgrupo', 'ano', 'obitos'])

    registros_cap = []
    for linha in range(14, 26):
        cod_ap_sms = df.iloc[linha, 0].strip()
        cod_ap_sms = 'Ignorado' if cod_ap_sms in ('Ign', 'Ignorado') else cod_ap_sms
        for ano, obitos in zip(anos, df.iloc[linha, 1:21]):
            registros_cap.append((cod_ap_sms, ano, int(obitos)))
    por_cap = pd.DataFrame(registros_cap, columns=['cod_ap_sms', 'ano', 'obitos'])
    por_cap = por_cap.groupby(['cod_ap_sms', 'ano'], as_index=False)['obitos'].sum()

    registros_taxa = list(zip(anos, df.iloc[31, 1:21], df.iloc[32, 1:21], df.iloc[33, 1:21]))
    taxa = pd.DataFrame(registros_taxa, columns=['ano', 'obitos', 'nascidos_vivos', 'taxa_por_mil'])
    taxa['obitos'] = taxa['obitos'].astype(int)
    taxa['nascidos_vivos'] = taxa['nascidos_vivos'].astype(int)
    taxa['taxa_por_mil'] = taxa['taxa_por_mil'].astype(float)

    return por_subgrupo, por_cap, taxa

def extrai_planilha_evitaveis_cap(caminho):
    """Extrai a planilha de causas evitáveis na primeira infância por CAP (TabWin) e
    materializa os 6 CSVs 'fiéis à fonte' (sem cálculo) em `dados_locais/tratados/` -- mesmo
    padrão de `limpa_dados_sisvan`: roda uma vez, materializa CSV, não devolve nada."""
    por_subgrupo, por_cap_municipio, taxa = extrai_evitaveis_municipio(caminho)
    por_subgrupo.to_csv('dados_locais//tratados//obitos_evitaveis_menores_5_causa_municipio_2006_2025.csv', index=False)
    por_cap_municipio.to_csv('dados_locais//tratados//obitos_evitaveis_menores_5_cap_municipio_2006_2025.csv', index=False)
    taxa.to_csv('dados_locais//tratados//taxa_mortalidade_evitaveis_menores_5_municipio_2006_2025.csv', index=False)

    abas_por_sufixo = {'menores_1_ano': '<1 ano', '1_a_4_anos': '1-4 anos', 'menores_5_anos': '<5 anos'}
    for sufixo, aba in abas_por_sufixo.items():
        df_bloco = extrai_evitaveis_cap_blocos(caminho, aba)
        df_bloco.to_csv(f'dados_locais//tratados//obitos_evitaveis_{sufixo}_causa_cap_2006_2025.csv', index=False)

def agrega_grupo_cid(df, colunas_chave):
    """Soma os 8 subgrupos CID (coluna 'subgrupo') de uma tabela extraída da planilha de
    causas evitáveis na primeira infância nos 3 grupos de primeiro nível ('1.', '2.', '3.'),
    devolvendo uma coluna 'grupo' no lugar de 'subgrupo'. A planilha TabWin traz só os
    subgrupos -- diferente dos arquivos 'segundo causas' usados nas seções anteriores, onde
    grupo e subgrupo são linhas separadas -- então o grupo sai do primeiro caractere do
    subgrupo já normalizado ('1.2.3. Red por at ao recém-nascido' -> grupo '1').

    `colunas_chave` permite reusar a função para `['cod_ap_sms','ano','faixa_etaria']` (por
    CAP) ou `['ano']` (município), sem duplicar lógica."""
    df = df.copy()
    df['grupo'] = df['subgrupo'].str[0].map(_GRUPOS_CID)
    return df.groupby(colunas_chave + ['grupo'], as_index=False)['obitos'].sum()

def subgrupo_excluido(subgrupo, faixa=None):
    """Subgrupos de causa evitável que ficam fora dos gráficos por decisão da equipe (specs/exclusoes.md):
    E3 -- 1.1 (reduzível por imunização), em todas as faixas: 0 a 2 óbitos por ano;
    E2 -- 1.2.x (gestação, parto, recém-nascido) em '1 a 4 anos': causa perinatal nessa idade é quase
    sempre erro de registro/codificação (22, 6 e 4 óbitos em 20 anos). Os CSVs continuam completos;
    só o que é desenhado muda."""
    s = str(subgrupo).strip()
    if s.startswith('1.1'):
        return True
    return faixa is not None and '1 a 4' in str(faixa) and s.startswith('1.2')

def filtra_colunas_subgrupo(colunas, faixa=None):
    """{rótulo: coluna} de `serie_temporal_multipla` sem os subgrupos de `subgrupo_excluido`."""
    return {rotulo: col for rotulo, col in colunas.items() if not subgrupo_excluido(rotulo, faixa)}

def agrupa_racas_raras(df):
    """E5 (specs/exclusoes.md): amarela e indígena somam 0 a 2 óbitos de menores de 1 ano por ano cada e geram
    picos sem significado no percentual -- viram 'amarela_indigena', com o percentual recalculado a partir dos
    absolutos somados (nunca somando percentuais, constituição §3). Acrescenta colunas, não remove nenhuma."""
    df = df.copy()
    df['obitos_amarela_indigena'] = df['obitos_amarela'] + df['obitos_indigena']
    if {'nascidos_amarela', 'nascidos_indigena'} <= set(df.columns):
        df['nascidos_amarela_indigena'] = df['nascidos_amarela'] + df['nascidos_indigena']
        pct = df['obitos_amarela_indigena'] / df['nascidos_amarela_indigena'] * 100
        df['percentual_amarela_indigena'] = pct.replace([float('inf'), -float('inf')], float('nan')).round(2)
    return df

def junta_codbairro_por_bairro(df, df_referencia):
    """Junta `codbairro` a uma tabela cuja única chave de bairro é o nome (string) -- caso do
    CadÚnico, a única fonte do projeto sem `codigo`/`codbairro` nativo. Usa `df_referencia`
    (ex. `df_censo`, que já tem `codbairro` confiável) como fonte da correspondência
    nome -> código. Levanta erro se sobrar alguma linha sem match, em vez de silenciosamente
    dropar bairros -- um join fuzzy solto foi descartado como opção (skill `generate_map`)."""
    resultado = df.merge(df_referencia[['bairro', 'codbairro']], on='bairro', how='left')
    sem_match = resultado[resultado['codbairro'].isna()]
    if len(sem_match) > 0:
        raise ValueError(f"{len(sem_match)} bairros sem correspondência: {sorted(sem_match['bairro'].unique())}")
    return resultado

def carrega_sidra_longo(caminho, coluna_corte=None):
    """Lê um export longo do IBGE SIDRA (uma linha de município, dimensões em colunas) e
    devolve só as colunas relevantes: idade, `coluna_corte` (raça/sexo, se houver) e valor.

    As tabelas de `dados_locais/ibge_sidra/` trazem sempre Rio de Janeiro (código 3304557),
    2022, e uma coluna de idade (`Idade` na tabela 9606, `Grupo de idade` nas 10056/10057) --
    normalizada aqui para 'idade'. `Valor == '-'` (0 ocorrências, mesma convenção já usada nos
    arquivos Tabnet do projeto) é convertido para 0."""
    df = pd.read_csv(caminho)
    coluna_idade = 'Idade' if 'Idade' in df.columns else 'Grupo de idade'
    df = df.rename(columns={coluna_idade: 'idade'})
    df['valor'] = df['Valor'].replace('-', 0).astype(float)
    colunas = ['idade', 'valor'] + ([coluna_corte] if coluna_corte else [])
    return df[colunas]
