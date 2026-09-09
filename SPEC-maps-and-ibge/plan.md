# Plano técnico — Mapas por bairro, IBGE SIDRA e mortalidade por subgrupo evitável

Companion de `specs.md` (revisão 2). Aqui está **como** implementar: nomes de arquivo,
assinaturas de função, colunas exatas e a ordem em que cada peça depende da anterior.

---

## 1. Princípio norteador

Diferente da spec anterior (`SPEC-mortalidade-AP`), **não há restrição de "nunca alterar
código existente"** — o usuário já autorizou corrigir os dois bugs de ordenação (feito, fora
deste branch) e pediu explicitamente para corrigir as lacunas de export do Componente A
(`specs.md` §2.3/§8.G). Mesmo assim, o princípio de menor intervenção continua valendo:

- **Reaproveitar `mapa_coropletico_bairros` e `_NIVEIS_AGREGACAO` como estão** — todo o
  Componente A usa `nivel='bairro'` (já suportado, nenhuma chave nova). O Componente C usa
  `nivel='cap'` (já existe, criado na spec anterior).
- **Extensão, não reescrita**: cada dataset do Componente A ganha `.to_csv(...)` +
  `mapa_coropletico_bairros(...)` novos ao final da sua seção já existente — nenhuma célula
  de limpeza/wrangling anterior muda de comportamento, só passa a exportar mais uma tabela.
- Seções de análise só chamam funções definidas em **Pacotes e Funções Auxiliares** — só 3
  funções novas de verdade neste plano: o parser genérico do SIDRA (§4.1), o agregador de
  raça total (§3.5) e o join CadÚnico→`codbairro` (§3.4). O resto é reuso direto do que já
  existe (`mapa_coropletico_bairros`, `serie_temporal_multipla`, `grafico_barra_agrupado`,
  `agrega_grupo_cid`).

---

## 2. Camada 0 — Correções pré-requisito (`specs.md` §2.3)

Bloqueiam qualquer export novo do Componente A — sem elas, o CSV de CadÚnico continua sendo
sobrescrito e as tabelas de mortalidade neonatal/gravidez/puerpério/raça não têm onde ancorar
o merge por `codigo`.

| # | correção | onde |
|---|---|---|
| 2.1 | `df_bairro.to_csv('tabelas_finais/cadunico_por_bairro_2026.csv')` mantém o nome; `df_bairro_ate_4.to_csv(...)` passa a `tabelas_finais/cadunico_por_bairro_ate_4_2026.csv` | linha ~901 |
| 2.2 | `df_mortalidade_raca_bairro.to_csv(...)` ganha uma segunda linha `.to_csv('tabelas_finais/mortalidade_raca_bairro_ano.csv', index=False)` (mantém o export existente em `dados_locais/tratados/`) | linha ~1054 |
| 2.3 | `df_neonatal_precoce`, `df_neonatal_tardia`, `df_mortalidade_infantil` ganham, cada um, um export por bairro-ano em `tabelas_finais/` (nome: `<indicador>_bairro_ano.csv`) — **além** do agregado município que já existe, não no lugar dele | linhas ~1648/1669/1719 |
| 2.4 | `df_obitos_gravidez`/`df_obitos_puerperio` ganham export por bairro-ano em `tabelas_finais/` (`obitos_gravidez_bairro_ano.csv`/`obitos_puerperio_bairro_ano.csv`) — hoje só existe o agregado município | linhas ~1603/1619 |

---

## 3. Camada 1 — Componente A (mapas por bairro, cobertura completa)

### 3.1 Padrão comum a todo item da tabela abaixo

Para cada dataset, ao final da seção já existente:

```python
df_mapa = df_<dataset>[df_<dataset>['ano'] == <ano_mais_recente>][['codigo', <colunas>]].copy()
df_mapa.to_csv('tabelas_finais/tabela_mapa_<indicador>_<ano>.csv', index=False)

mapa_coropletico_bairros(
    df_mapa, coluna_valor='<coluna_absoluta>', titulo='...', nome_arquivo='mapa_<indicador>_<ano>',
    chave='codigo', bins=[...],  # definidos após ver .describe() da distribuição real
    legenda_titulo='...', fonte_dados='...',
)
# + uma segunda chamada sem bins para a coluna de taxa/percentual, quando existir
```

Igual ao padrão já usado nos 6 mapas do Censo e nos 6 mapas de CAP — nenhuma variação de
assinatura.

### 3.2 Tabela de indicadores (Componente A)

| indicador (slug) | `df` fonte | ano | coluna absoluta (bins) | coluna taxa/% (contínua) | pré-requisito §2 |
|---|---|---|---|---|---|
| `cadunico_criancas` | `df_bairro` | extração atual | `Crianças` | — (sem % neste nível) | 3.4 (join `codbairro`) |
| `cadunico_primeira_infancia` | `df_bairro_ate_4` | extração atual | `Crianças` | `Primeira Inf. Cadúnico` | 3.4 |
| `nascidos_vivos` | `df_vivos` | 2025 | `nascidos vivos` | — (é o próprio denominador) | — |
| `nascidos_baixo_peso` | `df_baixo_peso` | 2025 | `nascidos abaixo peso` | `percentual abaixo do peso` | — |
| `obitos_raca_total` | `df_mortalidade_raca_bairro` | 2025 | `obitos_total` (nova, §3.5) | `percentual_total` (nova, §3.5) | 3.5, 2.2 |
| `obitos_neonatal_precoce` | `df_neonatal_precoce` | 2025 | `obitos_0_6` | `taxa_mortalidade_precoce` | 2.3 |
| `obitos_neonatal_tardia` | `df_neonatal_tardia` | 2025 | `obitos_7_27` | `taxa_obitos_tardios` | 2.3 |
| `mortalidade_infantil` | `df_mortalidade_infantil` | 2025 | `obitos_0_364` | `taxa_mortalidade_infantil` | 2.3 |
| `mortalidade_pos_neonatal` | `df_mortalidade_infantil` | 2025 | `obitos_28_364` | `taxa_mortalidade_pos_neonatal` | 2.3 |
| `obitos_gravidez` | `df_obitos_gravidez` | 2025 | `óbitos-gravidez` | — (denominador não definido, `specs.md` §2.5/§9) | 2.4 |
| `obitos_puerperio` | `df_obitos_puerperio` | 2025 | `óbitos-puerpério` | — (idem) | 2.4 |

11 indicadores, até 18 PNGs (9 com par abs+taxa, 2 só absoluto). `mortalidade_infantil` e
`mortalidade_pos_neonatal` reaproveitam o mesmo `df_mortalidade_infantil` já carregado — não
é uma leitura de dado nova, só duas chamadas de mapa a mais na mesma célula.

Censo (`df_censo`) **não entra nesta tabela** — já está feito (6 PNGs, padrão de
referência), só citado no inventário de `specs.md` §2.1.

### 3.3 Bins

Mesma regra da spec anterior: **nunca chutar antes de ver a distribuição real.** Para cada
indicador acima, antes de escolher `bins`, imprimir `df_mapa['<coluna_absoluta>'].describe()`
— com 166 bairros (vs. 10 CAPs), a variância é maior e outliers (ex. bairros com poucos
nascimentos vs. Barra da Tijuca/Campo Grande) podem exigir uma classe extra em relação ao
padrão de 4 bins do Censo/CAP.

### 3.4 `junta_codbairro_por_bairro(df, df_referencia=df_censo)`

Única peça nova de wrangling deste componente, para resolver o caso do CadÚnico (a única
fonte sem `codigo`/`codbairro` nativo — `specs.md` §2.4):

```python
def junta_codbairro_por_bairro(df, df_referencia):
    """Junta `codbairro` a uma tabela cuja única chave de bairro é o nome (string).

    Usa `df_referencia` (por padrão `df_censo`, que já tem `codbairro` confiável) como
    fonte da correspondência nome -> código. Levanta um erro se sobrar alguma linha sem
    match, em vez de silenciosamente dropar bairros -- um join fuzzy solto já foi descartado
    como opção (skill `generate_map`).
    """
    resultado = df.merge(df_referencia[['bairro', 'codbairro']], on='bairro', how='left')
    sem_match = resultado[resultado['codbairro'].isna()]
    if len(sem_match) > 0:
        raise ValueError(f"{len(sem_match)} bairros sem correspondência: {sem_match['bairro'].unique()}")
    return resultado
```

Chamada para `df_bairro` (reset o índice para expor `bairro` como coluna primeiro, já que
hoje é o índice do `groupby`) e para `df_bairro_ate_4` (já tem `bairro` como coluna, do merge
existente com `df_censo` na linha ~905 — só precisa que esse merge **também** traga
`codbairro`, não seja preciso um segundo join).

### 3.5 Coluna "total" em `df_mortalidade_raca_bairro`

```python
colunas_obitos_raca = [f'obitos_{r}' for r in racas]
colunas_nascidos_raca = [f'nascidos_{r}' for r in racas]  # já existem, ver linha ~1029

df_mortalidade_raca_bairro['obitos_total'] = df_mortalidade_raca_bairro[colunas_obitos_raca].sum(axis=1)
df_mortalidade_raca_bairro['nascidos_total'] = df_mortalidade_raca_bairro[colunas_nascidos_raca].sum(axis=1)
percentual_total = (df_mortalidade_raca_bairro['obitos_total'] / df_mortalidade_raca_bairro['nascidos_total']) * 100
df_mortalidade_raca_bairro['percentual_total'] = percentual_total.replace([float('inf'), -float('inf')], float('nan')).round(2)
```

Mesmo padrão de tratamento de `inf`/`nan` já usado nas 6 colunas por raça — só soma todas
antes de dividir, nunca média das 6 taxas por raça (mesma regra de `agrega_bairros_por_nivel`
para percentuais).

---

## 4. Camada 2 — Componente B (IBGE SIDRA)

### 4.1 `carrega_sidra_longo(caminho, coluna_corte)`

Parser único para as 9 tabelas — todas compartilham o layout longo do SIDRA (uma linha por
combinação de dimensões, coluna `Valor` no fim):

```python
def carrega_sidra_longo(caminho, coluna_corte):
    """Lê um export longo do IBGE SIDRA (uma linha de município, dimensões em colunas) e
    devolve só as colunas relevantes: idade, `coluna_corte` (raça/sexo/None) e valor.

    As 9 tabelas de `dados_locais/IBGE SIDRA/` trazem sempre Rio de Janeiro (código
    3304557), 2022, e uma coluna de idade (`Idade`/`Grupo de idade`, nome varia entre as
    tabelas 9606 e 10056/10057) -- normalizado aqui para 'idade'. `Valor == '-'` (0
    ocorrências, mesma convenção já usada nos arquivos Tabnet do projeto) é convertido para 0.
    """
    df = pd.read_csv(caminho)
    coluna_idade = 'Idade' if 'Idade' in df.columns else 'Grupo de idade'
    df = df.rename(columns={coluna_idade: 'idade'})
    df['valor'] = df['Valor'].replace('-', 0).astype(float)
    colunas = ['idade', 'valor'] + ([coluna_corte] if coluna_corte else [])
    return df[colunas]
```

Chamado 6 vezes (uma por arquivo `*_raca_cor.csv`/`*_sexo.csv`; os 3 `*_geral.csv` são o
corte `Total` já contido nos outros dois — não precisam de leitura separada, `coluna_corte=None`
extrai só a linha `Total` de qualquer um dos dois arquivos com corte).

### 4.2 Tabelas tratadas

| arquivo em `tabelas_finais/` | fonte | formato |
|---|---|---|
| `censo_sidra_populacao_0_6_raca_2022.csv` | `Censo/tabela9606_populacao_raca_cor.csv` | largo: `idade` × 6 colunas de raça |
| `censo_sidra_populacao_0_6_sexo_2022.csv` | `Censo/tabela9606_populacao_sexo.csv` | largo: `idade` × (Total/Homens/Mulheres) |
| `sidra_frequencia_escola_0_5_raca_2022.csv` | `Educacao_freq_escolar_ate5/tabela10057_frequencia_escola_raca_cor.csv` | largo, contagem absoluta |
| `sidra_frequencia_escola_0_5_sexo_2022.csv` | idem `_sexo.csv` | largo, contagem absoluta |
| `sidra_taxa_frequencia_0_6_raca_2022.csv` | `Educacao_freq_escolar_ate6/tabela10056_taxa_frequencia_raca_cor.csv` | largo, taxa % |
| `sidra_taxa_frequencia_0_6_sexo_2022.csv` | idem `_sexo.csv` | largo, taxa % |

`.pivot(index='idade', columns=coluna_corte, values='valor')` em cada uma — mesmo padrão já
usado em `df_evitaveis_subgrupo_mrj_wide` (linha 1435).

### 4.3 Visualizações

`grafico_barra_agrupado` (já existe, usado hoje no comparativo de cobertura vacinal
2016/2019/2022/2025) — eixo `idade` (0 a 6), grupos = raça ou sexo:

| arquivo | dado |
|---|---|
| `censo_sidra_populacao_0_6_raca_2022.png` | população por idade simples × raça |
| `censo_sidra_populacao_0_6_sexo_2022.png` | população por idade simples × sexo |
| `sidra_frequencia_escola_0_5_raca_2022.png` | nº que frequenta escola/creche por idade × raça |
| `sidra_taxa_frequencia_0_6_raca_2022.png` | taxa de frequência (%) por idade × raça |
| `sidra_taxa_frequencia_0_6_sexo_2022.png` | taxa de frequência (%) por idade × sexo |

(`sidra_frequencia_escola_0_5_sexo_2022` fica só como tabela — o gráfico por sexo já é
melhor representado pela taxa %, que normaliza a diferença de tamanho de população entre os
grupos; a contagem absoluta por sexo é redundante com a taxa por sexo já no gráfico acima.)

---

## 5. Camada 3 — Componente C (mapas de subgrupo, CAP, `< 1 ano`, 2025)

Reaproveita `df_evitaveis_cap_faixa` (já existe, linha 1477) e `mapa_coropletico_bairros(nivel='cap')`
(já existe, sem nenhuma alteração):

```python
subgrupos_componente_c = {
    'gestacao': '1.2.1. Red por at à mulher na gestação',
    'parto':    '1.2.2. Red por at à mulher no parto',
}

for slug, subgrupo in subgrupos_componente_c.items():
    df_subgrupo_2025 = df_evitaveis_cap_faixa[
        (df_evitaveis_cap_faixa['ano'] == 2025)
        & (df_evitaveis_cap_faixa['faixa_etaria'] == 'menores de 1 ano')
        & (df_evitaveis_cap_faixa['causa'] == subgrupo)
    ]
    df_subgrupo_2025.to_csv(f'tabelas_finais/tabela_mapa_obitos_evitaveis_{slug}_menores_1_ano_cap_2025.csv', index=False)

    mapa_coropletico_bairros(
        df_subgrupo_2025, coluna_valor='obitos', nivel='cap',
        titulo=f'Óbitos evitáveis - {subgrupo.split(". ",1)[1]}, menores de 1 ano, por CAP (2025)',
        nome_arquivo=f'mapa_obitos_evitaveis_{slug}_menores_1_ano_cap_2025',
        bins=[...],  # ver contagem real antes de fixar -- provavelmente 0-poucos por CAP
        legenda_titulo='Óbitos', caminho_geojson=_CAMINHO_GEO_CAP, fonte_dados=fonte_evitaveis_cap,
    )
```

`bins` aqui provavelmente precisam de classes bem menores que os mapas de grupo já
existentes (`[20,40,60,80]` para o grupo inteiro) — um único subgrupo específico, numa única
faixa etária, por CAP, deve ter contagens de dígito único na maioria das CAPs. Conferir com
`.describe()` antes de fixar, mesma regra de §3.3.

---

## 6. Camada 4 — Componente D (séries de subgrupo evitável)

### 6.1 D.1 — Painel municipal, 3 faixas etárias

Generaliza o que hoje só existe para `< 5 anos` (linha 1435-1447). Precisa de um total
municipal por faixa — soma as 10 CAPs dos CSVs já extraídos por `extrai_planilha_evitaveis_cap`
(`obitos_evitaveis_<faixa>_causa_cap_2006_2025.csv`), já que a planilha TabWin só tem o
recorte município completo (`< 5 anos`) pronto na aba `Informações gerais`:

```python
for sufixo, info in faixas_primeira_infancia.items():
    df_municipio_faixa = (
        pd.read_csv(f'dados_locais/tratados/obitos_evitaveis_{sufixo}_causa_cap_2006_2025.csv')
        .groupby(['causa', 'ano'], as_index=False)['obitos'].sum()
    )
    df_wide = df_municipio_faixa.pivot(index='ano', columns='causa', values='obitos').reset_index()
    serie_temporal_multipla(
        df_wide, tempo='ano', colunas={c: c for c in df_wide.columns if c != 'ano'},
        titulo=f'Óbitos por causas evitáveis ({info["rotulo"]}) por subgrupo - Rio de Janeiro (2006-2025)',
        nome_arquivo=f'obitos_evitaveis_{sufixo}_subgrupo_ano', ylabel='Óbitos', legend_title='Subgrupo',
        figsize=(14,7),
    )
```

A célula existente para `< 5 anos` (que lê `obitos_evitaveis_menores_5_causa_municipio_2006_2025.csv`
direto, sem precisar somar CAPs) é **mantida como está** — os dois caminhos chegam ao mesmo
resultado para essa faixa (verificação cruzada, não retrabalho); o loop acima só cobre as
duas faixas que faltam (`< 1 ano`, `1-4 anos`).

### 6.2 D.2a — Matriz completa (6 subgrupos × 3 faixas × CAP)

```python
_SLUG_SUBGRUPO_EVITAVEL = {
    '1.1. Reduzível pelas ações de imunização':   'imunizacao',
    '1.2.1. Red por at à mulher na gestação':     'gestacao',
    '1.2.2. Red por at à mulher no parto':        'parto',
    '1.2.3. Red por at ao recém-nascido':         'recem_nascido',
    '1.3. Red por ações de diag e trat adequado': 'diagnostico_tratamento',
    '1.4. Red por ações promoção vinc a atenção': 'promocao_vinculacao',
}

for subgrupo, slug in _SLUG_SUBGRUPO_EVITAVEL.items():
    for sufixo, info in faixas_primeira_infancia.items():
        df_serie = df_evitaveis_cap_faixa[
            (df_evitaveis_cap_faixa['causa'] == subgrupo) & (df_evitaveis_cap_faixa['faixa_etaria'] == info['rotulo'])
        ].pivot(index='ano', columns='cod_ap_sms', values='obitos').reset_index()

        serie_temporal_multipla(
            df_serie, tempo='ano', colunas={c: c for c in df_serie.columns if c != 'ano'},
            titulo=f'Óbitos evitáveis - {subgrupo.split(". ",1)[1]}, {info["rotulo"]}, por CAP (2006-2025)',
            nome_arquivo=f'obitos_evitaveis_{slug}_cap_{sufixo}_ano', ylabel='Óbitos', legend_title='CAP',
            figsize=(14,7),
        )
```

18 chamadas (6 × 3), um único loop aninhado — nenhuma lógica nova além do que
`serie_temporal_multipla` já faz para os 6 gráficos de grupo×CAP existentes (linha 1499-1524).
Contagens muito baixas nalgumas combinações (ex. `1.2.1`/`1-4 anos`/CAP pequena) vão gerar
linhas quase todas em zero — aceitável, mesma ressalva já registrada no notebook para
`1-4 anos` em geral (nota 4, `specs.md`/spec anterior).

### 6.3 D.2b — Recorte gestação/parto, `< 1 ano`

Subconjunto de D.2a — mesma fonte, só filtra os 2 subgrupos do Componente C e a faixa
`< 1 ano`, publicado ao lado dos 2 mapas de `mapas/` (não recalcula nada):

```python
for slug in ('gestacao', 'parto'):
    df_serie = df_evitaveis_cap_faixa[
        (df_evitaveis_cap_faixa['causa'] == subgrupos_componente_c[slug])
        & (df_evitaveis_cap_faixa['faixa_etaria'] == 'menores de 1 ano')
    ].pivot(index='ano', columns='cod_ap_sms', values='obitos').reset_index()

    serie_temporal_multipla(
        df_serie, tempo='ano', colunas={c: c for c in df_serie.columns if c != 'ano'},
        titulo=f'Óbitos evitáveis - {subgrupos_componente_c[slug].split(". ",1)[1]}, menores de 1 ano, por CAP (2006-2025)',
        nome_arquivo=f'obitos_evitaveis_{slug}_cap_menores_1_ano_ano', ylabel='Óbitos', legend_title='CAP',
        figsize=(14,7),
    )
```

Reaproveita `subgrupos_componente_c` já definido em §5 — mesma seção de análise, célula logo
após os 2 mapas.

---

## 7. Camada 5 — Componente E (raça/cor, sem `nao_informado`/1996)

Duas células novas, logo após as duas já existentes (linhas 1157-1180), reusando
`df_evitaveis_raca_municipio` já calculado:

```python
rotulos_raca_evitaveis_sem_nao_informado = {
    r: c for r, c in rotulos_raca_evitaveis.items() if r != 'Não informada'
}

df_evitaveis_raca_sem_1996 = df_evitaveis_raca_municipio[df_evitaveis_raca_municipio['ano'] > 1996]

serie_temporal_multipla(
    df_evitaveis_raca_sem_1996, tempo='ano',
    colunas={rotulo: f'obitos_evitaveis_{raca}' for rotulo, raca in rotulos_raca_evitaveis_sem_nao_informado.items()},
    titulo='Óbitos por causas evitáveis (0-364 dias) por raça/cor, sem "não informada" - Rio de Janeiro (1997-2025)',
    nome_arquivo='obitos_causas_evitaveis_raca_sem_nao_informado_ano', ylabel='Óbitos',
)
```

E a mesma ideia para o percentual, a partir de `df_percentual_evitaveis_municipio` (já filtra
`ano >= 2011`, não precisa do corte de 1996 — só remove `nao_informado` das colunas):

```python
serie_temporal_multipla(
    df_percentual_evitaveis_municipio, tempo='ano',
    colunas={rotulo: f'percentual_evitaveis_{raca}' for rotulo, raca in rotulos_raca_evitaveis_sem_nao_informado.items()},
    titulo='Percentual de óbitos evitáveis (0-364 dias) por raça/cor, sem "não informada" - Rio de Janeiro (2011-2025)',
    nome_arquivo='percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano', ylabel='Percentual (%)',
)
```

O comentário-lembrete não implementado na linha 1167 (`## retirar 1996 do ano acima e
colocar nota de rodapé`) é substituído por uma nota de markdown explicando que o gráfico
original (com 1996 e `nao_informado`) é mantido para completude da série, e a versão nova é
a recomendada para leitura de tendência.

---

## 8. Reorganização (posição exata de cada célula nova)

Ver `specs.md` §7 para a visão geral; aqui, a posição **relativa a células específicas já
existentes** de `analise.py`, para orientar o `tasks.md`:

| entrega | inserir depois de | inserir antes de |
|---|---|---|
| B (SIDRA Censo) | `#### Por bairro` (Censo), linha ~672 | `#### 🗺️ Mapa coroplético (bairros)`, linha ~674 |
| A: CadÚnico (2 indicadores) | célula `df_bairro[df_bairro['bairro']=='Complexo do Alemão']` corrigida (pré-requisito, já em `staging_main`) | `### 🏥 DataSus - tabnet`, linha ~914 |
| A: nascidos vivos | fim de `#### Nascidos Vivos`, linha ~948 | `#### Nascidos abaixo peso`, linha ~950 |
| A: baixo peso | fim de `#### Nascidos abaixo peso`, linha ~976 | `#### 📉 Mortalidade`, linha ~978 |
| A: óbitos raça | fim de `##### Óbitos até 1 ano por raça/cor`, linha ~1103 | `##### Óbitos por causas evitáveis por raça/cor`, linha ~1105 |
| E (raça/cor evitáveis) | célula `percentual_mortalidade_causas_evitaveis_raca_ano` (linha ~1180) | `##### Óbitos por causas evitáveis, por grupo de causa (CID-10)`, linha ~1183 |
| D.1 (3 faixas) | célula `taxa_mortalidade_evitaveis_menores_5_ano` (linha ~1454) | `###### Por CAP e faixa etária`, linha ~1457 |
| D.2a (matriz completa) | fim de `###### Por CAP e faixa etária` (após o loop de 3 faixas existente, linha ~1524) | `df_total_menores_5_cap_wide`/série de total, linha ~1526 |
| C (2 mapas) + D.2b (2 séries) | fim do loop de mapas de CAP existente, linha ~1586 | `#### 📋 Óbitos gravidez e puerpério`, linha ~1589 |
| A: gravidez/puerpério | fim de cada subseção correspondente, linhas ~1608/~1624 | próxima subseção |
| A: neonatal precoce/tardia/mortalidade infantil | fim de cada subseção correspondente, linhas ~1654/~1675/~1732 | próxima subseção |
| B (SIDRA Educação) | `#### Taxa de frequência escolar` (PNAD), antes da célula de leitura, linha ~1833 | célula de leitura PNAD |

---

## 9. Ordem de execução e riscos

| # | passo | risco | mitigação |
|---|---|---|---|
| 1 | Camada 0 (bugs/exports faltando, §2) | export com nome errado quebra um merge mais abaixo | rodar e conferir `tabelas_finais/` antes de seguir |
| 2 | Componente A — funções auxiliares (§3.4, §3.5) | join de nome de bairro perde alguma linha | `junta_codbairro_por_bairro` levanta erro em vez de dropar silenciosamente |
| 3 | Componente A — 11 indicadores, 1 de cada vez | bins ruins (classe única) | `.describe()` antes de cada `bins`, mesma regra da spec anterior |
| 4 | Componente B — parser + 6 tabelas + 5 gráficos | layout SIDRA diferente do esperado nas 9 tabelas | conferir shape/colunas de cada CSV antes de generalizar o parser (V3.1) |
| 5 | Componente C — 2 mapas | contagens tão baixas que o mapa vira quase todo "classe 1" | aceitar — é o resultado real; documentar em nota de markdown, mesmo padrão de `1-4 anos` |
| 6 | Componente D — D.1, D.2a, D.2b | 18 gráficos gerados errado por erro no loop | conferir 2-3 amostras manualmente contra `df_evitaveis_cap_faixa` filtrado à mão |
| 7 | Componente E — 2 gráficos | esquecer de manter os originais | ambos ficam no notebook, nomes de arquivo diferentes |
| 8 | README + Update Table + jupytext sync | — | checklist único no fim (`tasks.md` Bloco 8) |
| 9 | Execução ponta a ponta + commit | qualquer célula anterior quebrada por engano | `jupyter nbconvert --execute` limpo, 0 erros (mesmo processo já usado nesta sessão) |

Risco geral: **maior que a spec anterior**, porque aqui há edição real de código já em
produção (Camada 0) e ~30 novos artefatos (mapas + séries + tabelas), não uma seção
isolada nova. Mitigação principal: seguir a ordem acima estritamente (cada camada só começa
com a anterior validada) e rodar o notebook completo a cada 2-3 indicadores do Componente A,
não só no final.

---

## 10. Requisitos de ambiente

Nenhuma dependência nova além do que já foi instalado nesta sessão (`geopandas`,
`contextily`, etc. — ver `specs.md` §0). `pandas.read_csv` já lida com os 9 arquivos do SIDRA
sem parser especial além de `carrega_sidra_longo`.
