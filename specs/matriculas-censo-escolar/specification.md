# Especificação: Matrículas de 0 a 6 anos, Censo Escolar/INEP (`specs/matriculas-censo-escolar`)

Branch: `spec/matriculas-censo-escolar` (a partir de `staging_main`, em 2026-09-24)
Status: **rascunho 1**, em planejamento. Decisões D1-D6 (§5) aguardam o usuário. `plan.md`, `tasks.md`
e `validation.md` só serão escritos depois que elas forem aprovadas.
Roadmap: seção "Matrículas" de `specs/roadmap.md` ("Update dados de matrículas escolares for years
2021-2025").

---

## 1. Objetivo

Completar o indicador **"Matrículas na educação básica de crianças até 6 anos"** do eixo 🧒 Prioridade
em `specs/estrutura_eixos.md` (linhas 269-274). Hoje ele está como `status: pendente`, com a nota "até
2020, necessário tratar microdados posteriores". O caminho é:

1. Buscar a quantidade de matrículas de crianças pequenas no **município do Rio de Janeiro**
   (IBGE `3304557`) de **2021 em diante**, direto da fonte original: os microdados do Censo Escolar
   da Educação Básica/INEP
   (<https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar>).
2. Fazer isso de forma reprodutível: uma função no topo de `analise.py` que lê os ZIPs do INEP, em vez
   de um CSV colado à mão sem registro de como foi gerado.
3. Levar o resultado para `tabelas_finais/matriculas_0_a_6_por_ano.csv`,
   `visualizacoes/matriculas_0_a_6_por_ano.png` e, pelo crosswalk, para o HTML, o PDF e o DOCX de
   curadoria.

**Fora de escopo, a princípio:** recorte por bairro, AP ou RP (§4.4) e cruzamento com população para
calcular taxa de atendimento. Esses itens são candidatos a uma rodada seguinte.

---

## 2. Situação atual

- `analise.py:3166-3179` lê `dados_locais/educacao/censo_escolar_matriculas_ate_6anos.csv` (colunas
  `f0_`, `ano`; 2007-2020, 14 linhas), renomeia `f0_` para `matriculas` e plota `serie_temporal`.
  O título da célula é "complementar 2021-2025", mas os anos de 2021 em diante não estão lá.
- **Não há registro de como o CSV foi feito.** O nome de coluna `f0_` é o padrão do BigQuery para uma
  expressão sem alias, o que sugere uma consulta na Base dos Dados sobre a antiga tabela de matrículas
  (nível aluno). O arquivo entrou no commit `343f79f` (2026-08-26, "Update readme and source files
  commited") sem a query. O filtro de idade, a data de referência e as redes incluídas são
  **desconhecidos**.
- Existe uma variável reaproveitada: a célula grava em `df_freq_escolar`, o mesmo nome usado pela
  PNAD logo acima. Isso não quebra nada hoje, mas vale corrigir junto.

---

## 3. Fonte: microdados do Censo Escolar (levantamento de 2026-09-24)

### 3.1 Arquivos disponíveis

URL padrão: `https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_<ANO>.zip`.

| Ano | Tamanho do ZIP | Observação |
|---|---|---|
| 2007 / 2010 / 2015 / 2019 | 21-27 MB | disponível, mesmo formato por escola (verificado pelo tamanho) |
| 2020 | 26,0 MB | **baixado e lido**: `microdados_ed_basica_2020.CSV` (extensão maiúscula, publicado em 2022-09-14) |
| 2021 | 25,9 MB | disponível |
| 2022 | 26,4 MB | disponível |
| 2023 | 32,1 MB | **baixado e lido**: `microdados_ed_basica_2023.csv` (210 MB, 408 colunas, `;`, latin-1) |
| 2024 | 33,8 MB | disponível |
| 2025 | **537 MB** | URL diferente: `microdados_censo_escolar_2025_.zip` (com `_` no fim). O tamanho é 16× maior, então **a estrutura pode ter mudado** e precisa ser verificada (§6, P1). |

### 3.2 Achado principal: não existe mais dado por aluno, só contagem por escola

Desde a adequação à LGPD, o INEP publica **uma linha por escola**, com matrículas já agregadas em
faixas, e republicou os anos anteriores (pelo menos até 2007) nesse formato. Não existe mais um
arquivo de matrículas com a idade de cada aluno. As colunas de idade disponíveis são:

| Coluna | Conteúdo |
|---|---|
| `QT_MAT_BAS_0_3` | matrículas na educação básica, alunos de 0 a 3 anos |
| `QT_MAT_BAS_4_5` | alunos de 4 a 5 anos |
| `QT_MAT_BAS_6_10` | alunos de **6 a 10 anos** |
| `QT_MAT_BAS_11_14`, `_15_17`, `_18_MAIS` | faixas seguintes |
| `QT_MAT_INF`, `QT_MAT_INF_CRE`, `QT_MAT_INF_PRE` | matrículas por **etapa** (educação infantil, creche, pré-escola), de qualquer idade |
| `QT_MAT_BAS_FEM/MASC`, `QT_MAT_BAS_BRANCA/PRETA/PARDA/...` | sexo e raça/cor, **só no total da educação básica**, sem cruzar com idade |

**Consequência:** "0 a 6 anos" exato **não é calculável** com os dados abertos. A faixa de 6 anos está
misturada com 7-10 em `QT_MAT_BAS_6_10`. Por isso a nota em `estrutura_eixos.md` estava pendente. Ver
D1.

### 3.3 Números de referência: Rio de Janeiro (`CO_MUNICIPIO == 3304557`)

| Ano | `0_3` | `4_5` | **0-5** | `INF` (etapa) | `INF_CRE` | `INF_PRE` | CSV histórico ("até 6") |
|---|---|---|---|---|---|---|---|
| 2020 | 107.422 | 139.711 | **247.133** | 258.749 | 115.698 | 143.051 | **205.371** |
| 2023 | 113.935 | 132.184 | **246.119** | 258.120 | 122.762 | 135.358 | (não existe) |

Em 2023 há 4.198 escolas no município. A divisão por dependência administrativa é esta:

| `TP_DEPENDENCIA` | 0-3 | 4-5 | INF |
|---|---|---|---|
| 1 federal | 235 | 269 | 527 |
| 2 estadual | 30 | 85 | 121 |
| 3 municipal | 46.642 | 84.674 | 139.698 |
| 4 privada | 67.028 | 47.156 | 117.774 |

### 3.4 Achado: a série histórica não bate com a fonte original

Em 2020, o ano em que os dois formatos se sobrepõem, o CSV histórico ("até 6 anos") tem **205.371**.
A soma de 0-5 dos microdados atuais dá **247.133**, 42 mil a mais, mesmo **sem** as crianças de 6 anos.
Nenhuma combinação óbvia reproduz o número antigo:

- só rede pública ficaria bem abaixo (em 2023 é ~54% de 0-5, 131.935; 2020 por rede ainda não foi calculado);
- educação infantil (258.749) fica acima;
- a diferença também não é a faixa de 6 anos, que aumentaria o total, não diminuiria.

Hipóteses, nenhuma verificável sem a query original: contagem de alunos distintos em vez de matrículas;
exclusão de alguma modalidade ou etapa; idade calculada em outra data; ou filtro de rede. **Juntar
2007-2020 (CSV antigo) com 2021+ (INEP) numa mesma linha criaria um degrau artificial na série.** Ver D2.

---

## 4. Proposta

### 4.1 Função de carga (topo de `analise.py`, seção 📦)

Nova `carrega_censo_escolar_matriculas(anos, cod_municipio=3304557, pasta_cache=...)`:

- Baixa o ZIP de cada ano, se ele ainda não estiver no cache local, e lê o CSV de dentro do ZIP
  **sem extrair** (`zipfile` + `pd.read_csv(..., sep=';', encoding='latin-1', usecols=[...])`). O nome
  do CSV varia entre anos (`.CSV`/`.csv`, subpasta), então o arquivo é localizado por padrão e não por
  nome fixo.
- Filtra `CO_MUNICIPIO == cod_municipio` e devolve um formato longo com uma linha por
  ano × dependência × coluna de contagem, e colunas `ano`, `dependencia`, `faixa`, `matriculas`.
- Só colunas de contagem agregadas por escola: não há dado pessoal, e a §6 da constitution
  (privacidade) não se aplica, mas fica registrado.

### 4.2 Onde os dados moram

- **ZIPs brutos não são versionados.** Juntos passam de 700 MB (só o de 2025 tem 537 MB) e
  `dados_locais/` não é gitignorado. Cache em `dados_locais/educacao/inep_microdados/`, com uma regra
  nova no `.gitignore` (ver D5).
- **Extrato do Rio versionado:** `dados_locais/educacao/inep_matriculas_rio.csv`, algumas centenas de
  linhas no formato longo acima. Com ele, o notebook roda sem baixar nada; a função só baixa se o
  extrato não cobrir os anos pedidos.

### 4.3 Saídas

- `tabelas_finais/matriculas_0_a_6_por_ano.csv`: série anual, com nome e rótulo conforme D1. O arquivo
  é rastreado desde antes de 2026-09-22 e é lido pelo pipeline de relatório; manter o nome evita mexer
  nos leitores, mas ver D1 sobre o título.
- `visualizacoes/matriculas_0_a_6_por_ano.png`: `serie_temporal`, `fonte_dados='Censo Escolar da
  Educação Básica (INEP), microdados'`.
- Opcional (D3): uma série por creche/pré ou por rede (`serie_temporal_multipla` ou barras agrupadas).
- `specs/estrutura_eixos.md`: tira o `status: pendente` e reescreve a nota com a definição de idade
  adotada.
- Nota de método no notebook (markdown, sem entrar no relatório, que é para público não técnico):
  faixas por escola, data de referência da idade, ausência de dado por aluno e quebra da série (D2).

### 4.4 Recorte territorial (fora de escopo, registrado)

O arquivo por escola traz `NO_BAIRRO`, `CO_CEP` e `CO_DISTRITO`, mas **não traz `codbairro`**. Juntar
por nome de bairro vai contra a constitution §3, e juntar por CEP tem os problemas já documentados no
roadmap item 8a (CadÚnico). Um mapa por bairro exigiria geocodificar as escolas (lat/long via
Data.Rio/SME ou pelo endereço), o que é uma rodada à parte.

---

## 5. Decisões para o usuário

| # | Decisão | Proposta |
|---|---|---|
| **D1** | **Definição de "até 6 anos"**, já que 6 anos exatos não existe nos dados abertos (§3.2). Opções: (a) **0 a 5 anos** = `QT_MAT_BAS_0_3 + QT_MAT_BAS_4_5`; (b) **educação infantil por etapa** (`QT_MAT_INF`), que inclui crianças mais velhas retidas e exclui 6 anos no fundamental; (c) pedir microdados restritos ao INEP/SEDAP (fora do prazo). | **(a) 0 a 5**, que é a faixa da educação infantil (creche 0-3, pré 4-5) e corresponde à idade, não à etapa. O título passa a "Matrículas de crianças de 0 a 5 anos", e o nome do arquivo `matriculas_0_a_6_por_ano` é mantido ou renomeado (sub-decisão). A etapa (b) pode entrar como série complementar em D3. |
| **D2** | **O que fazer com 2007-2020**, que não bate com a fonte (§3.4). Opções: (a) **reconstruir a série inteira** a partir dos mesmos ZIPs do INEP e aposentar o CSV antigo; (b) juntar o antigo com o novo, com uma nota de quebra; (c) publicar só 2021+. | **(a)**: uma fonte e uma definição só. Os ZIPs de 2007-2020 existem e têm o mesmo formato (verificado pelo tamanho; 2020 lido). O CSV antigo vai para `git rm`, ou fica com uma nota de "não usado", sem apagar o histórico da spec. Alternativa mais barata: começar em 2015 ou 2019, para limitar downloads. |
| **D3** | **Recortes extras** a publicar. Opções: creche × pré (0-3 × 4-5); rede pública × privada; municipal × estadual × federal × privada; nenhum. | **Creche × pré** e **pública × privada**. Os dois são diretos das colunas e relevantes para a política municipal (a rede municipal é ~53% de 0-5 em 2023). |
| **D4** | **Anos**: "2021 em diante" inclui **2025**, que vem num ZIP de 537 MB com URL diferente e talvez outra estrutura (§3.1). | Incluir 2025 **se** o formato for compatível (verificar no Bloco 1). Se não for, publicar até 2024 e registrar 2025 como pendência. |
| **D5** | **Cache dos ZIPs**: `dados_locais/educacao/inep_microdados/` com regra no `.gitignore` (proposta) ou fora do repositório (scratch/`~`). | Dentro do repo, gitignorado, para que o notebook seja autossuficiente. |
| **D6** | **Taxa de atendimento** (matrículas ÷ população de 0-5 anos) nesta rodada? | **Não**: a projeção populacional anual por idade para 2021-2025 é outra fonte e outra discussão. Registrar no roadmap. |

---

## 6. Pendências e riscos

- **P1: formato de 2025.** 537 MB contra ~30 MB nos anos anteriores. Pode ser outra organização,
  com várias tabelas ou dado por matrícula de volta. Baixar e inspecionar antes de fechar o plano.
- **P2: data de referência da idade.** Pelo dicionário de dados (confirmar no `leia-me/` de cada ZIP),
  a idade é calculada na data de referência do Censo (última quarta-feira de maio). Isso vai para a
  nota de método.
- **P3: escolas paralisadas ou extintas.** Verificar se `TP_SITUACAO_FUNCIONAMENTO != 1` tem
  matrícula > 0. Se tiver, decidir o filtro. Em 2023 a soma de `TP_SITUACAO_FUNCIONAMENTO` (4.615 em
  4.198 escolas) mostra que há escolas não ativas no arquivo.
- **P4: pipeline de relatório.** Verificar como `build_html_report.py`, `build_notebook_report.py` e o
  DOCX leem `matriculas_0_a_6_por_ano.*` e se mostram o card como pendente (hard-coded, como
  aconteceu no CadÚnico, ver `specs/recortes_cadunico/plan.md` "Descobertas" item 2).
- **P5: comparação com números oficiais.** Conferir 1 ou 2 anos contra a Sinopse Estatística do
  INEP (tabela de educação infantil por município) como validação externa.
