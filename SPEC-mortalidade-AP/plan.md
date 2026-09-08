# Plano técnico — Óbitos por causas evitáveis por Área Programática

Companion de `specification.md`. Aqui está **como** implementar, com as assinaturas de
função propostas e as decisões de design justificadas.

> **Revisão 2** — incorpora duas decisões do usuário: trabalhar no nível **CAP** com
> geometria oficial, e **nunca alterar código já existente**. A §4 foi reescrita por
> inteiro: a estratégia anterior (acrescentar uma chave em `_NIVEIS_AGREGACAO` e 3 linhas
> em `mapa_coropletico_bairros`) violaria a restrição.

---

## 1. Princípio norteador

O `analise.py` tem uma estrutura explícita, documentada no README e reforçada no commit
`3c14e56`:

> "as seções de análise abaixo apenas *chamam* essas funções, sem redefini-las"

Somado à restrição **"nunca alterar código existente"**, o plano fica: **4 funções novas de
wrangling + 1 função-adaptador de mapa + 1 seção de análise que só orquestra**. Nenhuma
linha existente é editada — nem funções, nem constantes, nem células de análise. Tudo é
acréscimo.

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
- devolve `ano` e `obitos` como `int`; `causa` com `.strip()`.

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

### 3.1 `agrega_grupo_cid(df)`

A planilha não traz o nível "grupo" como linha (spec §2.4). Deriva-se do prefixo do rótulo,
reaproveitando o `padrao_grupo` mental já usado no notebook:

```python
_GRUPOS_CID = {'1': '1. Causas evitáveis',
               '2': '2. Causas mal definidas',
               '3': '3. Demais causas (não claramente evitáveis)'}

def agrega_grupo_cid(df, colunas_chave):
    """Soma os 8 subgrupos CID da planilha nos 3 grupos de primeiro nível ('1.', '2.', '3.').

    A planilha TabWin traz só os subgrupos -- diferente dos arquivos 'segundo causas' usados
    nas seções anteriores, onde grupo e subgrupo são linhas separadas. O grupo sai do primeiro
    caractere do rótulo ('1.2.3. Red por ad...' -> grupo '1').
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

## 4. Camada 3 — Mapas por CAP sem tocar em código existente

Este é o ponto de maior atenção do plano. A restrição do usuário elimina a solução óbvia.

### 4.1 O impasse

`mapa_coropletico_bairros` resolve o nível geográfico por um dicionário no topo do arquivo:

```python
_NIVEIS_AGREGACAO = {
    'bairro': {'coluna_geo': 'codbairro',  'tipo': int},
    'ap':     {'coluna_geo': 'area_plane', 'tipo': int},
    'rp':     {'coluna_geo': 'cod_rp',     'tipo': str},
}
```

O caminho natural seria acrescentar `'cap'` a esse dicionário. Mas isso é **editar uma
constante existente**, e a função precisaria de mais 3 linhas para derivar a coluna — ou
seja, editar a função também. **Proibido.**

### 4.2 A saída: o geojson é parâmetro, e `'rp'` já é genérico

Duas observações destravam o problema **sem tocar em nada**:

1. `mapa_coropletico_bairros` já expõe **`caminho_geojson`** como parâmetro — a geometria
   nunca foi fixa no código.
2. O nível `'rp'` não tem nada de específico de Região de Planejamento: ele significa
   literalmente *"faça o join por uma coluna de texto chamada `cod_rp`"*. O `dissolve` por
   essa coluna, num arquivo que já tem uma feição por valor, é um **no-op**.

Então basta que o geojson de CAP traga uma coluna `cod_rp` com `'1.0'`, `'2.1'`, … `'5.3'`.
Por isso o arquivo salvo em `dados_locais/geo/limite_ap_saude_rio.geojson` tem **duas**
colunas de código (`specification.md` §4.1):

- `cod_ap_sms` — o nome honesto, é o que a documentação e qualquer uso futuro devem ler;
- `cod_rp` — cópia, **alias técnico** que existe só para encaixar no nível `'rp'`.

Já verificado de ponta a ponta (simulando exatamente o que a função faz): `dissolve` devolve
os 10 polígonos válidos, o merge acha os 10 sem nenhum "Sem dado", CRS e `total_bounds`
batem com o limite de bairros.

### 4.3 O adaptador (código novo, não substitui nada)

Para que o alias não vaze para as células de análise, uma função nova, fina, que só
pré-preenche argumentos:

```python
_CAMINHO_GEO_CAP = 'dados_locais/geo/limite_ap_saude_rio.geojson'

def mapa_coropletico_cap(df, coluna_valor, titulo, nome_arquivo, chave='cod_ap_sms', **kwargs):
    """Mapa coroplético por CAP (Área Programática de Saúde da SMS-Rio, 10 unidades).

    Adaptador fino sobre `mapa_coropletico_bairros`, que NÃO é alterada. Duas notas:

    - As CAPs não existem no geojson de bairros do IPP (que traz Área de Planejamento e
      Região de Planejamento). A geometria vem de um arquivo próprio, baixado do Data.Rio
      ('Áreas Programáticas da Saúde', SMS) -- ver SPEC-mortalidade-AP/specification.md §4.
    - Repassa `nivel='rp'` não porque isto seja Região de Planejamento, mas porque esse
      nível é, na prática, "join por uma coluna de texto chamada cod_rp" -- e o geojson de
      CAP traz `cod_rp` como alias de `cod_ap_sms` justamente para encaixar aí. O `dissolve`
      vira no-op (o arquivo já tem uma feição por CAP).

    Cuidado ao usar: `df` precisa da coluna `cod_ap_sms` com os códigos no formato da
    planilha ('1.0', '2.1', ... '5.3') -- sem o prefixo 'AP '.
    """
    df = df.rename(columns={chave: 'cod_rp'})
    return mapa_coropletico_bairros(
        df, coluna_valor=coluna_valor, titulo=titulo, nome_arquivo=nome_arquivo,
        nivel='rp', caminho_geojson=_CAMINHO_GEO_CAP, **kwargs,
    )
```

Cinco linhas efetivas, zero duplicação da lógica cartográfica (bins, colorbar, rosa dos
ventos, escala, rodapé, rótulos de vizinhos — tudo herdado).

### 4.4 Alternativas descartadas

| alternativa | por que não |
|---|---|
| Chave `'cap'` em `_NIVEIS_AGREGACAO` + 3 linhas na função | **viola a restrição**; é a solução mais limpa e fica registrada em `specification.md` §8-D caso o usuário mude de ideia |
| Duplicar `mapa_coropletico_bairros` como `mapa_coropletico_cap` | ~200 linhas copiadas; qualquer ajuste cartográfico futuro teria de ser feito em dois lugares |
| Derivar as CAPs do de-para RA→CAP e dissolver o geojson de bairros | foi a proposta da revisão 1; **errava 5 bairros** (`specification.md` §4.3) e as fronteiras sairiam diferentes das oficiais |
| Renomear `cod_ap_sms` → `cod_rp` e ponto | perderia o nome correto do campo; manter os dois custa 10 valores de texto |

### 4.5 Risco assumido, explicitamente

O alias `cod_rp` num arquivo de CAP é **enganoso para quem abrir o geojson sem contexto**.
Mitigação: o nome honesto `cod_ap_sms` está no mesmo arquivo e é o usado em todas as
tabelas; a docstring do adaptador explica o porquê; e `specification.md` §8-D deixa a
decisão aberta para o usuário reverter para a solução limpa quando quiser.

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
  [py] loop nas 3 faixas -> mapa_coropletico_cap: absoluto (bins) + percentual (contínuo)
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
| 5 | adaptador `mapa_coropletico_cap` + 1 mapa de fumaça | alias `cod_rp` confundir quem ler | docstring + `cod_ap_sms` no mesmo arquivo (§4.5) |
| 6 | escolher `bins` a partir da distribuição | mapa de classe única | V6 |
| 7 | séries temporais | 10 séries acima da paleta de 8 | aceito, precedente da cobertura vacinal |
| 8 | README + Update Table | — | V8 |

**Risco de regressão: zero por construção.** Nenhuma linha existente é editada — a restrição
do usuário, além de ser uma ordem, é também a garantia. O que resta conferir (V9) é só que o
código novo não quebre a execução do arquivo como um todo.

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
