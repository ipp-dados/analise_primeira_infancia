# Plano técnico — Óbitos por causas evitáveis por Área Programática

Companion de `specification.md`. Aqui está **como** implementar, com as assinaturas de
função propostas e as decisões de design justificadas.

> **Revisão 3** — o usuário autorizou a exceção pontual que a revisão 2 tinha descartado:
> acrescentar a chave `'cap'` a `_NIVEIS_AGREGACAO`, desde que os códigos/colunas já
> atribuídos a `bairro`/`ap`/`rp` não mudem. A §4 foi reescrita por inteiro — cai o
> adaptador `mapa_coropletico_cap` e o alias `cod_rp` no geojson de CAP (verificados contra
> o código real de `analise.py`: a função `mapa_coropletico_bairros` não precisa de **nenhuma**
> linha nova, só a chave no dicionário).

---

## 1. Princípio norteador

O `analise.py` tem uma estrutura explícita, documentada no README e reforçada no commit
`3c14e56`:

> "as seções de análise abaixo apenas *chamam* essas funções, sem redefini-las"

Somado à restrição **"nunca alterar código existente"**, o plano fica: **4 funções novas de
wrangling + 1 seção de análise que só orquestra**, mais **uma única exceção pontual**
autorizada pelo usuário nesta revisão: uma chave nova (`'cap'`) em `_NIVEIS_AGREGACAO` (§4).
Fora essa chave, nenhuma linha existente é editada — nem funções, nem células de análise.
Tudo o mais é acréscimo, e a própria exceção não pode alterar os códigos/colunas já
atribuídos aos níveis existentes (`bairro`, `ap`, `rp`) — ver §4.1.

---

## 2. Camada 1 — Extração da planilha

### 2.1 `extrai_evitaveis_cap_blocos(caminho, aba)`

Lê uma das abas `<1 ano` / `1-4 anos` / `<5 anos` e devolve formato longo
`cod_ap_sms, causa, ano, obitos`.

```python
def extrai_evitaveis_cap_blocos(caminho, aba, anos=range(2006, 2026)):
    """Lê uma aba 'por CAP' da planilha de causas evitáveis (TabWin) e devolve formato longo.

    A aba é uma pilha de 10 blocos de 12 linhas, um por Área Programática de Saúde: título
    (que carrega o código da CAP), cabeçalho, 8 categorias CID, 'Total' e uma linha em branco.
    A linha 'Total' é descartada -- é recalculável e entraria em dupla contagem em qualquer
    groupby posterior.
    """
```

Design:
- **passo fixo de 12 linhas** (`range(0, len(df), 12)`), não busca por regex de título — o
  layout do TabWin é rígido e o passo fixo falha ruidosamente (`IndexError`) se a planilha
  mudar, o que é preferível a falhar em silêncio. A validação (`validation.md` V1) confirma
  o layout antes de qualquer confiança no resultado;
- a CAP sai do título por `str.split(', AP ')[1].split(',')[0]` — o único lugar da aba que a
  identifica (a planilha escreve `AP 3.1`; guardamos `'3.1'` em `cod_ap_sms`);
- devolve `ano` e `obitos` como `int`; `causa` **não** é só `.strip()` do rótulo bruto —
  é normalizada para o texto de `subgrupo` da tabela em `specification.md` §2.4: 3 dos 8
  rótulos trazem o trecho redundante `ad ` antes de `at` (ex.: `1.2.1. Red por ad at à
  mulher na gestação` → `1.2.1. Red por at à mulher na gestação`); os outros 5 já batem
  com o rótulo bruto. Usa o mesmo dicionário `_ROTULO_PARA_SUBGRUPO` de §3.1.

### 2.2 `extrai_evitaveis_municipio(caminho)`

Lê a aba `Informações gerais` e devolve as **três** tabelas empilhadas nela, como uma tupla
de DataFrames (`por_causa`, `por_cap`, `taxa`). Índices de linha fixos (0-10 / 12-26 / 29-33),
pelo mesmo motivo acima.

Tratamento das linhas ` Ign` e ` Ignorado` da tabela por CAP: `.strip()` + as duas somadas
numa única categoria `Ignorado`. São a mesma informação (CAP de residência não registrada)
sob rótulos diferentes ao longo da série — exatamente o caso já resolvido no notebook para
`mae_ignorado` + `mae_nao_informado` → `nascidos_nao_informado`, então segue-se o mesmo
padrão e a mesma justificativa em comentário.

### 2.3 `extrai_planilha_evitaveis_cap(caminho)` — orquestrador

Chama as duas acima para as 4 abas, escreve os 6 CSVs de §5.1 da spec em
`dados_locais/tratados/` e não devolve nada — assinatura espelhando `limpa_dados_sisvan`,
que também é "roda uma vez, materializa CSV". É essa função que a seção
`🧼 Limpeza de dados prévia` chama.

---

## 3. Camada 2 — Agregação por grupo CID

### 3.0 Princípio: só se trabalha em dois níveis — grupo e subgrupo

A planilha só oferece as 8 linhas `CID Evitav INF` (**subgrupo**) e não traz o nível "grupo"
como linha própria (spec §2.4) — e não há, nesta fonte, um terceiro nível "causa" (a
diferença para os arquivos "segundo causas" já existentes no notebook, que têm os três
níveis grupo/subgrupo/causa, está registrada em `specification.md` linha 28). Por isso todo
código e toda tabela derivada desta planilha carregam **sempre as duas colunas**, `subgrupo`
e `grupo` (esta última derivada da primeira) — nunca uma coluna genérica `causa` solta, e
nunca uma tentativa de desagregar além do subgrupo.

O texto de `subgrupo` usado em qualquer DataFrame é o normalizado da tabela de
`specification.md` §2.4 (coluna "subgrupo"), não o rótulo bruto da planilha — ver §2.1:

```python
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
```

Note que 5 das 8 chaves e valores são idênticos — só as 3 categorias `1.2.*` mudam (o `ad `
redundante é removido). O dicionário existe mesmo assim, com as 8 entradas, para que
`extrai_evitaveis_cap_blocos` e `extrai_evitaveis_municipio` apliquem uma única regra
(`.map(_ROTULO_PARA_SUBGRUPO)`) em vez de tratar 5 casos como "iguais" e 3 como "especiais".

### 3.1 `agrega_grupo_cid(df)`

O grupo se deriva do prefixo do `subgrupo` já normalizado (não do rótulo bruto), reaproveitando
o `padrao_grupo` mental já usado no notebook:

```python
_GRUPOS_CID = {'1': '1. Causas evitáveis',
               '2': '2. Causas mal definidas',
               '3': '3. Demais causas (não claramente evitáveis)'}

def agrega_grupo_cid(df, colunas_chave):
    """Soma os 8 subgrupos CID da planilha nos 3 grupos de primeiro nível ('1.', '2.', '3.').

    A planilha TabWin traz só os subgrupos -- diferente dos arquivos 'segundo causas' usados
    nas seções anteriores, onde grupo e subgrupo são linhas separadas. O grupo sai do primeiro
    caractere do subgrupo já normalizado ('1.2.3. Red por at ao recém-nascido' -> grupo '1').
    """
```

`colunas_chave` permite reusar a mesma função para `['cod_ap_sms','ano']` (por CAP) e para `['ano']`
(município), sem duplicar lógica.

### 3.2 Percentual de evitáveis

Regra do projeto (comentário de `agrega_bairros_por_nivel`): **percentual é sempre
recalculado a partir das somas, nunca média de percentuais**. Aplica-se aqui:

```
percentual_evitaveis = obitos_grupo_1 / obitos_total_da_CAP * 100
```

com `.replace([inf, -inf], nan)` — o mesmo tratamento já usado nas seções de raça/cor para
CAP/ano sem óbito nenhum (denominador 0). Em `1-4 anos` isso acontece de verdade: há CAP/ano
com 0 óbitos totais.

---

## 4. Camada 3 — Mapas por CAP: chave nova em `_NIVEIS_AGREGACAO`

### 4.1 Decisão do usuário: exceção pontual autorizada

A revisão 2 descartou o caminho natural — acrescentar `'cap'` a `_NIVEIS_AGREGACAO` — por
violar a restrição "nunca alterar código existente", e construiu um adaptador
(`mapa_coropletico_cap`) que reaproveitava o nível `'rp'` via um alias `cod_rp` no geojson de
CAP. **O usuário liberou o caminho natural nesta revisão**, com uma condição: os
códigos/colunas já atribuídos aos três níveis existentes (`bairro`, `ap`, `rp`) não podem
mudar. O adaptador e o alias caem por inteiro — não são mais necessários.

`_NIVEIS_AGREGACAO`, hoje (`analise.py:239-243`):

```python
_NIVEIS_AGREGACAO = {
    'bairro': {'coluna_geo': 'codbairro',  'tipo': int},
    'ap':     {'coluna_geo': 'area_plane', 'tipo': int},
    'rp':     {'coluna_geo': 'cod_rp',     'tipo': str},
}
```

Passa a ser, com **uma linha nova** e as três existentes bit-a-bit idênticas:

```python
_NIVEIS_AGREGACAO = {
    'bairro': {'coluna_geo': 'codbairro',  'tipo': int},
    'ap':     {'coluna_geo': 'area_plane', 'tipo': int},
    'rp':     {'coluna_geo': 'cod_rp',     'tipo': str},
    'cap':    {'coluna_geo': 'cod_ap_sms', 'tipo': str},   # NOVO — único acréscimo autorizado
}
```

`tipo=str` pelo mesmo motivo de `'rp'`: os códigos de CAP (`'1.0'`, `'2.1'`, … `'5.3'`) têm
formato `AP.subregião` e perderiam precisão como número.

### 4.2 Por que `mapa_coropletico_bairros` não precisa de nenhuma linha nova

A revisão 2 estimava "mais 3 linhas para derivar a coluna" na função. Conferido contra o
código real (`analise.py:312-357`), essa estimativa era **excessivamente cautelosa**: a
função já é inteiramente genérica sobre `nivel` —

```python
info_nivel = _NIVEIS_AGREGACAO[nivel]
coluna_geo, tipo = info_nivel['coluna_geo'], info_nivel['tipo']
chave = chave or coluna_geo
...
gdf_nivel = gdf_bairros if nivel == 'bairro' else gdf_bairros.dissolve(by=coluna_geo, as_index=False)
```

Não há nenhum `if nivel == 'ap'`/`'rp'` especial: qualquer chave não-`'bairro'` passa pelo
mesmo `dissolve(by=coluna_geo)`, que é **no-op** quando o geojson já tem uma feição por
valor — exatamente o caso do geojson de CAP (10 feições, uma por `cod_ap_sms`, `plan.md` era
`specification.md` §4.2). Chamada direta, sem adaptador:

```python
mapa_coropletico_bairros(
    df, coluna_valor=..., titulo=..., nome_arquivo=...,
    nivel='cap', caminho_geojson='dados_locais/geo/limite_ap_saude_rio.geojson',
)
```

`caminho_geojson` já era parâmetro (não fixo no código) — essa parte da observação da
revisão 2 continua válida, só que agora não precisa de um alias para chegar lá.

A função **fica com zero linhas alteradas**, docstring inclusive — ela não lista `'cap'`
entre os valores de `nivel` (só cita `'bairro'`/`'ap'`/`'rp'`), e não é atualizada para
listar, porque isso seria editar uma linha existente. O significado de `'cap'` fica
documentado aqui e em `specification.md`, não na docstring da função.

### 4.3 O geojson: sem alias

`dados_locais/geo/limite_ap_saude_rio.geojson` só precisa da coluna `cod_ap_sms` — o join
agora usa essa coluna direto (`chave` default = `coluna_geo` = `'cod_ap_sms'`). A coluna
`cod_rp` gravada na revisão 2 como alias técnico não tem mais função; se o arquivo já salvo
ainda a tiver, é inofensiva e pode ser removida numa limpeza futura (não bloqueia nada).

Já verificado de ponta a ponta na revisão 2 (simulando exatamente o que a função faz):
`dissolve` devolve os 10 polígonos válidos, o merge acha os 10 sem nenhum "Sem dado", CRS e
`total_bounds` batem com o limite de bairros — nada disso muda ao trocar `cod_rp` por
`cod_ap_sms` como coluna de join, é o mesmo dado.

### 4.4 Alternativas descartadas

| alternativa | por que não |
|---|---|
| Adaptador `mapa_coropletico_cap` + alias `cod_rp` (plano da revisão 2) | funcionava e não tocava em nada, mas era mais código (função + docstring + geojson com coluna redundante) para o mesmo resultado, uma vez que o usuário autorizou a chave direta |
| Duplicar `mapa_coropletico_bairros` como `mapa_coropletico_cap` | ~200 linhas copiadas; qualquer ajuste cartográfico futuro teria de ser feito em dois lugares |
| Derivar as CAPs do de-para RA→CAP e dissolver o geojson de bairros | foi a proposta da revisão 1; **errava 5 bairros** (`specification.md` §4.3) e as fronteiras sairiam diferentes das oficiais |

### 4.5 Risco assumido, explicitamente

A chave `'cap'` em `_NIVEIS_AGREGACAO` é uma edição real de uma constante que já existia —
tecnicamente fora do "nunca alterar código existente" tomado ao pé da letra, mas dentro do
que o usuário autorizou nesta revisão. Mitigação: a validação (`validation.md` V10.2) confere
mecanicamente que as três chaves antigas ficam bit-a-bit idênticas e que `mapa_coropletico_
bairros` em si (V10.3) não muda nenhuma linha — a exceção fica contida numa única entrada de
dicionário, auditável num `git diff` de uma linha.

### 4.6 De-para RA → CAP: ainda vale a pena?

Sim, mas **não para os mapas** (que usam o polígono oficial). Vale como cross-walk para
agregar tabelas por bairro/RA até a CAP no futuro — por exemplo, cruzar o Censo por bairro
com estes óbitos. Fica como constante nova `_RA_PARA_CAP` (valores corrigidos de
`specification.md` §4.4), **derivada do cruzamento espacial com o polígono oficial**, não
escrita de memória. Não é usada nesta entrega; só documentada.

---

## 5. Camada 4 — Seção de análise (só orquestra)

Estrutura de células, seguindo o padrão markdown-antes-de-código do notebook:

```
##### Óbitos por causas evitáveis na primeira infância, por Área Programática de Saúde (CAP)
  [md] contexto + as 4 notas de interpretação (ver §6)

###### Panorama municipal (< 5 anos)
  [py] lê os 3 CSVs municipais; exporta tabelas_finais/
  [py] serie_temporal_multipla -> 8 subgrupos CID
  [py] serie_temporal        -> taxa por mil NV

###### Por CAP e faixa etária
  [py] empilha as 3 abas -> tabela mestra; agrega_grupo_cid; percentual; exporta
  [py] loop nas 3 faixas -> serie_temporal_multipla (óbitos evitáveis por CAP)
  [py] loop nas 3 faixas -> serie_temporal_multipla (percentual evitáveis por CAP)

###### 🗺️ Mapas por CAP (2025)
  [py] recorte 2025 + exporta mortalidade_evitaveis_cap_2025.csv
  [py] loop nas 3 faixas -> mapa_coropletico_bairros(nivel='cap'): absoluto (bins) + percentual (contínuo)
```

O loop das 3 faixas usa um dict de configuração no mesmo estilo do `niveis_planejamento` já
existente no notebook:

```python
faixas_primeira_infancia = {
    'menores_1_ano':  {'aba': '<1 ano',   'rotulo': 'menores de 1 ano', 'bins': [...]},
    '1_a_4_anos':     {'aba': '1-4 anos', 'rotulo': 'de 1 a 4 anos',    'bins': [...]},
    'menores_5_anos': {'aba': '<5 anos',  'rotulo': 'menores de 5 anos','bins': [...]},
}
```

Os `bins` ficam **em branco no primeiro rascunho** e são preenchidos depois de imprimir a
distribuição de 2025 (`.describe()`), como manda a validação V6 — chutar faixas antes de ver
os dados produziria mapas de classe única.

---

## 6. Notas de markdown a escrever (interpretação)

Toda seção do notebook tem uma célula de notas com as ressalvas de leitura. As desta seção,
todas ancoradas em fatos já verificados:

1. As três faixas são aninhadas: `< 5 anos` = `< 1 ano` + `1-4 anos` (verificado célula a
   célula) — **não somar as três**, seria dupla contagem.
2. 165 óbitos (0,7% da série) não têm CAP de residência registrada, concentrados em 2006-2011;
   **em 2025 são zero**, então os mapas de 2025 cobrem 100% dos óbitos.
3. A planilha só traz subgrupos CID; o grupo `1. Causas evitáveis` é a soma das seis linhas
   `1.*` — diferente dos arquivos "segundo causas" das seções anteriores.
4. `1-4 anos` tem contagens muito baixas (13 a 25 óbitos/ano na cidade inteira, 0 a 3 por CAP);
   percentuais por CAP nessa faixa são instáveis e não devem ser lidos como tendência.
5. Denominador (NV) só existe no nível municipal → sem taxa por mil NV por CAP; os mapas
   absolutos **não são comparáveis entre CAPs sem considerar o tamanho da população** — a CAP
   3.3 tem 29 bairros contra 5 da 5.2.
6. A CAP (SMS, 10 unidades) **não é** a Área de Planejamento do IPP (5 unidades) usada nos
   mapas do Censo deste mesmo notebook — são divisões territoriais diferentes e não devem ser
   comparadas lado a lado sem ressalva.

---

## 7. Ordem de execução e riscos

| # | passo | risco | mitigação |
|---|---|---|---|
| 1 | renomear o xlsx | nenhum (untracked) | — |
| 2 | funções de extração + validação V1-V4 | layout do TabWin diferente do esperado | passo fixo de 12 falha alto; V1 confere antes |
| 3 | CSVs materializados | — | V2/V3 conferem contra os totais da própria planilha |
| 4 | geojson oficial de CAP | ✅ **já feito** — baixado, validado, salvo | V5 |
| 5 | chave `'cap'` em `_NIVEIS_AGREGACAO` + 1 mapa de fumaça | editar uma constante existente | V10.2 confere que as 3 chaves antigas não mudam |
| 6 | escolher `bins` a partir da distribuição | mapa de classe única | V6 |
| 7 | séries temporais | 10 séries acima da paleta de 8 | aceito, precedente da cobertura vacinal |
| 8 | README + Update Table | — | V8 |

**Risco de regressão: quase zero por construção.** Só uma linha de `analise.py` muda uma
constante existente (`_NIVEIS_AGREGACAO`, ganha a chave `'cap'`) — autorizado nesta revisão,
com a garantia mecânica de que as 3 chaves antigas ficam idênticas (V10.2) e nenhuma outra
função existente é tocada (V10.3-V10.4). Fora essa linha, nada existente é editado. O que
resta conferir (V9) é que o código novo não quebre a execução do arquivo como um todo.

---

## 8. Requisitos de ambiente

Nenhuma dependência nova. `openpyxl` (leitura de xlsx) já é usado por `limpa_dados_sisvan` e
já está em `requirements.txt`; `geopandas`/`contextily`/`matplotlib-scalebar` idem.

O `.gitignore` já exclui `*.png` e `/tabelas_finais/*`, então os mapas, gráficos e tabelas
gerados **não** entram no commit — só o código, os CSVs de `dados_locais/tratados/`, o xlsx
renomeado, o geojson de CAP e a documentação. Comportamento igual ao de todas as seções
anteriores.

O geojson novo (`dados_locais/geo/limite_ap_saude_rio.geojson`, 2,57 MB) **entra** no
versionamento, como os outros três de `dados_locais/geo/`. É o maior arquivo do repositório;
se isso incomodar, dá para simplificar a geometria (`.simplify()`) e cair para ~200 KB, ao
custo de bordas ligeiramente menos precisas — na escala do município, imperceptível. Fica
como item opcional em `tasks.md`.
