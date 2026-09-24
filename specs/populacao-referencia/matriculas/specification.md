# Especificação: Matrículas e taxa de atendimento de 0 a 5 anos, Censo Escolar/INEP (`specs/matriculas-censo-escolar`)

Branch: `spec/matriculas-censo-escolar` (a partir de `staging_main`, em 2026-09-24)

> **2026-09-24: esta rodada virou a Parte E de `specs/populacao-referencia`** (branch renomeada para
> `spec/populacao-referencia`, pasta movida para `specs/populacao-referencia/matriculas/`). A função de
> população passa a ser a da Parte A (`carrega_populacao_ripsa`/`populacao_ripsa`), a nota D7 aponta para a
> nota geral A5, e a execução vem depois da Parte A. As decisões D1-D9 abaixo continuam valendo.
Status: **implementada** (2026-09-24, como Parte E de `populacao-referencia`). Rascunho 4: todas as
decisões D1-D9 aprovadas.

Rascunho 3: D1-D5 aprovadas, com o check de 2025 feito (§3.5, compatível).
Renomear os arquivos para `0_a_5` aprovado. **D6 entrou no escopo** (usuário: "you can add to this spec
scope"), o que abriu as decisões D7-D9 sobre o denominador (§3.6, §5). **O usuário revisa as specs antes de
qualquer implementação.** Desdobramento: `plan.md`, `tasks.md`, `validation.md`.

> Histórico: rascunho 1 (abertura), rascunho 2 (D1-D5 e check de 2025), rascunho 3 (renomear, D6 no escopo,
> fonte de população), rascunho 4 (D7-D9 aprovadas).
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
3. Levar o resultado para `tabelas_finais/` e `visualizacoes/` (nomes `matriculas_0_a_5_*`) e, pelo
   crosswalk, para o HTML, o PDF e o DOCX de curadoria.
4. **(D6, no escopo desde o rascunho 3)** Calcular a **taxa bruta de atendimento**: matrículas de 0-3,
   4-5 e 0-5 divididas pela população residente da mesma faixa, por ano (§3.6).

**Fora de escopo:** recorte por bairro, AP ou RP (§4.4).

> Rascunhos 1-2 tinham "cruzamento com população para calcular taxa de atendimento" fora do escopo. O
> usuário incluiu no rascunho 3.

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

### 3.5 Check de 2025 e série 2020-2025 (condição de D4, feito em 2026-09-24)

O ZIP de 2025 (`microdados_censo_escolar_2025_.zip`, pasta interna `microdados_censo_escolar_2025_v2/`)
**mudou de organização**, mas é compatível:

- Em vez de um único `microdados_ed_basica_<ANO>.csv`, vem **uma tabela por tema**: `Tabela_Escola`,
  `Tabela_Matricula`, `Tabela_Turma`, `Tabela_Docente`, `Tabela_Gestor_Escolar` e
  `Tabela_Curso_Tecnico`, todas com sufixo `_2025_V2.csv`. Continua sendo **uma linha por escola**, sem
  dado por aluno. O tamanho maior vem das tabelas de docente, turma e gestor.
- As contagens de matrícula **saíram da tabela de escola** e estão agora na `Tabela_Matricula_2025_V2.csv`
  (263 colunas, com `CO_MUNICIPIO` e `TP_DEPENDENCIA`). `QT_MAT_BAS_0_3`, `QT_MAT_BAS_4_5`, `QT_MAT_INF*`
  existem com o mesmo nome.
- **Encoding latin-1**, apesar de o cabeçalho ser ASCII. Ler como UTF-8 falha no meio do arquivo.
- **Novas colunas `QT_MAT_BAS_*_REF_31_03`**, com a idade em 31 de março (data de corte do CNE). Em 2025,
  0-3 = 119.514 e 4-5 = 122.171, contra 110.097 e 120.187 na data padrão. **Usa-se a data padrão**
  (última quarta-feira de maio, P2), a única que existe em todos os anos. As colunas `_REF_31_03` não
  entram.

Série do Rio (`CO_MUNICIPIO == 3304557`) na data padrão, lida dos ZIPs:

| Ano | Arquivo lido | Escolas | 0-3 | 4-5 | **0-5** | pública 0-5 | `INF` (etapa) |
|---|---|---|---|---|---|---|---|
| 2020 | `microdados_ed_basica_2020.CSV` | 4.235 | 107.422 | 139.711 | **247.133** | 143.909 | 258.749 |
| 2021 | `microdados_ed_basica_2021.csv` | 4.209 | 101.421 | 128.839 | **230.260** | 140.722 | 242.372 |
| 2022 | `microdados_ed_basica_2022.csv` | 4.487 | 114.822 | 131.700 | **246.522** | 136.691 | 258.292 |
| 2023 | `microdados_ed_basica_2023.csv` | 4.198 | 113.935 | 132.184 | **246.119** | 131.935 | 258.120 |
| 2024 | `microdados_ed_basica_2024.csv` | 4.203 | 114.934 | 127.641 | **242.575** | 127.851 | 254.222 |
| 2025 | `Tabela_Matricula_2025_V2.csv` | 3.875 | 110.097 | 120.187 | **230.284** | 122.236 | 241.391 |

"Pública" = `TP_DEPENDENCIA` 1-3 (federal, estadual, municipal). "Escolas" é o número de linhas do
município no arquivo lido. Em 2025 a tabela de matrícula tem menos linhas que a antiga tabela de escola,
então esse número não é comparável entre os dois formatos e não é publicado.

Leituras que vão para a nota do notebook, sem interpretação no relatório:
- **2021 é um vale** (-6,8% sobre 2020). É coerente com a pandemia e aparece também em `INF`.
- **2025 cai 5,1% sobre 2024**, puxado pela pré-escola (4-5: -5,8%). A rede pública de 0-5 cai todo ano
  desde 2020 (143.909 → 122.236, -15%). A privada (total - pública) cai em 2021 (89.538), sobe até 2024
  (114.724) e recua em 2025 (108.048). Desde 2023 a privada é quase metade de 0-5.

### 3.6 Denominador da taxa: população residente de 0-5 anos (levantamento de 2026-09-24)

A única população por idade simples que o projeto tem hoje é a do Censo 2022 (SIDRA 9606,
`dados_locais/ibge_sidra/Censo/`), que cobre só um ano. Para a série anual, a fonte encontrada é:

**Estimativas populacionais da Ripsa/Ministério da Saúde**: "População residente: estudo de estimativas
populacionais por município, idade e sexo, 2000-2025" (Nota Técnica Ripsa nº 01/2025,
doi:10.5281/zenodo.17990183). É revisada depois do Censo 2022 e ajustada às Projeções do IBGE (revisão
2024). Cobre **município × sexo × idade simples (0-79)**, com **1º de julho** de cada ano como data de
referência, de 2000 a 2025. É a base que o Ministério da Saúde usa para os indicadores municipais.

- **Acesso automatizável:** Tabnet `http://tabnet.datasus.gov.br/cgi/tabcgi.exe?ibge/cnv/popsvs2024br.def`
  (o `.def` antigo, `popsvsbr`, é a versão 2000-2021, **não usar**). Um POST com `Linha=Ano`,
  `Coluna=Idade_simples`, `SMunicípio=3262` (330455 Rio de Janeiro), idades 1-7 (menos de 1 a 6 anos),
  arquivos `pop07.dbf`…`pop25.dbf` e `formato=prn` devolve um CSV com `;`. **Testado:**

| Ano | 0-3 | 4-5 | 0-5 | Taxa 0-3 | Taxa 4-5 | Taxa 0-5 |
|---|---|---|---|---|---|---|
| 2020 | 307.006 | 167.316 | 474.322 | 35,0% | 83,5% | 52,1% |
| 2021 | 296.299 | 160.981 | 457.280 | 34,2% | 80,0% | 50,4% |
| 2022 | 282.173 | 157.734 | 439.907 | 40,7% | 83,5% | 56,0% |
| 2023 | 268.654 | 155.085 | 423.739 | 42,4% | 85,2% | 58,1% |
| 2024 | 259.038 | 148.499 | 407.537 | 44,4% | 86,0% | 59,5% |
| 2025 | 251.936 | 141.137 | 393.073 | 43,7% | 85,2% | 58,6% |

(taxas = matrículas de §3.5 ÷ população Ripsa; os dados de 2007-2019 também vieram na mesma consulta)

**Achado: Ripsa e Censo 2022 divergem em 2022.** O Censo 2022 conta **379.609** crianças de 0-5 no Rio
(SIDRA 9606: <1 = 54.337, 1 = 55.996, 2 = 63.010, 3 = 66.801, 4 = 70.504, 5 = 68.961). A Ripsa estima
**439.907** para 2022, 16% a mais, e a diferença maior está em <1 ano (64.701 contra 54.337). Isso é
coerente com o sub-registro de crianças pequenas no Censo 2022, que as Projeções do IBGE (revisão 2024)
corrigem, e a Ripsa herda essa correção. Com o Censo como denominador, a taxa de 2022 seria **64,9%**
(0-3: 47,8%; 4-5: 94,4%) em vez de 56,0%. Ver D7.

**Ressalvas da taxa (vão para a nota de método):**
- É **bruta**. O numerador conta matrículas em escolas do município, incluindo crianças que moram em
  outros municípios (Baixada, Niterói) e estudam no Rio. O denominador são os residentes.
- As datas de referência diferem por cerca de um mês (fim de maio no Censo Escolar, 1º de julho na
  população). O efeito é pequeno e não é corrigido.
- Referência externa de ordem de grandeza: a PNAD (já no notebook) dá cerca de 83% aos 4 anos e 90% aos
  5. A taxa 4-5 Ripsa (80-86%) é coerente com isso.
- O **PNE (Lei 13.005/2014), Meta 1**, prevê 50% de atendimento em creche (0-3) e universalização da
  pré-escola (4-5). É referência natural para leitura, ver D8.

## 4. Proposta

### 4.1 Função de carga (topo de `analise.py`, seção 📦)

Nova `carrega_censo_escolar_matriculas(anos, cod_municipio=3304557, pasta_cache=...)`:

- Baixa o ZIP de cada ano, se ele ainda não estiver no cache local, e lê o CSV de dentro do ZIP
  **sem extrair** (`zipfile` + `pd.read_csv(..., sep=';', encoding='latin-1', usecols=[...])`). O nome
  do CSV varia entre anos (`.CSV`/`.csv`, subpasta), então o arquivo é localizado por padrão e não por
  nome fixo.
- Filtra `CO_MUNICIPIO == cod_municipio` e agrega por dependência. O formato final (uma linha por
  ano × dependência) está em `plan.md` Bloco 2. O formato longo previsto no rascunho 1 foi trocado por
  esse, que é mais simples de somar.
- Só colunas de contagem agregadas por escola: não há dado pessoal, e a §6 da constitution
  (privacidade) não se aplica, mas fica registrado.

### 4.2 Onde os dados moram

- **ZIPs brutos não são versionados.** Juntos passam de 700 MB (só o de 2025 tem 537 MB) e
  `dados_locais/` não é gitignorado. Cache em `dados_locais/educacao/inep_microdados/`, com uma regra
  nova no `.gitignore` (ver D5).
- **Extrato do Rio versionado:** `dados_locais/educacao/inep_matriculas_rio.csv`, 76 linhas
  (19 anos × 4 dependências). Com ele, o notebook roda sem baixar nada; a função só baixa se o
  extrato não cobrir os anos pedidos.

### 4.3 Saídas

- `tabelas_finais/matriculas_0_a_5_por_ano.csv`: série anual 2007-2025 (renomeada de `0_a_6`, aprovado
  no rascunho 3). Traz matrículas, população e taxas; as colunas estão em `plan.md`.
- `visualizacoes/matriculas_0_a_5_por_ano.png`: `serie_temporal` do total de 0-5,
  `fonte_dados='Censo Escolar da Educação Básica (INEP), microdados'`.
- D3: `matriculas_0_a_5_creche_pre_por_ano.png` e `matriculas_0_a_5_rede_por_ano.png`
  (`serie_temporal_multipla`).
- D6: `taxa_atendimento_0_a_5_por_ano.png` (`serie_temporal_multipla` com 0-3, 4-5 e 0-5, em %),
  `fonte_dados` citando INEP e Ripsa/MS.
- População: extrato versionado `dados_locais/populacao/ripsa_populacao_rio_0_6_idade_simples.csv`
  (19 anos × 7 idades), numa pasta temática nova seguindo a constitution §3 (uma pasta por fonte). É
  gerado por uma função que faz o POST no Tabnet e grava o extrato, e depois lê só o extrato.
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

**Registro (usuário, 2026-09-24):** D1 ✅ 0-5 · D2 ✅ reconstruir · D3 ✅ creche × pré e pública × privada ·
D4 ✅, com check de 2025 antes do resto (feito, §3.5) · D5 ✅ · D6 sem resposta, segue a proposta (fora).
**Sub-decisão de D1 (rascunho 3):** renomear para `0_a_5` ✅. **D6 (rascunho 3):** ✅ no escopo.
**D7-D9 (rascunho 4, usuário, 2026-09-24):** D7 ✅ Ripsa, **com nota metodológica** (ver abaixo) ·
D8 ✅ linhas do PNE (b) · D9 ✅ 0-3, 4-5 e 0-5.

**Conteúdo da nota metodológica de D7** (markdown no notebook, perto da taxa; não vai para o relatório,
que é para público não técnico, exceto a linha de fonte no rodapé do gráfico):
1. Denominador: estimativas Ripsa/MS 2000-2025 (Nota Técnica 01/2025), população em 1º de julho, por
   idade simples, ajustada às Projeções do IBGE (revisão 2024), e a data da consulta ao Tabnet.
2. Por que não o Censo 2022: ele conta 379.609 crianças de 0-5 no Rio contra 439.907 da Ripsa (+16%),
   com a maior diferença em menores de 1 ano (sub-registro de crianças pequenas corrigido pelo IBGE).
   Com o Censo, a taxa de 2022 seria 64,9% (0-3: 47,8%; 4-5: 94,4%) em vez de 56,0%, e números do
   Censo 2022 no notebook (SIDRA) não são diretamente comparáveis com a taxa.
3. É uma taxa **bruta**: o numerador inclui não residentes matriculados no Rio, e as datas de
   referência diferem (fim de maio e 1º de julho).
4. Revisões: a Ripsa revisa as estimativas todo ano, então uma nova consulta pode mudar anos passados
   (P7).
5. Diferença com a "taxa bruta de frequência escolar" da PNAD, que já está no notebook: aquela é
   declarada no domicílio, esta é registro administrativo ÷ estimativa.
6. Metas do PNE (Lei 13.005/2014, Meta 1) nas linhas de referência do gráfico.

A tabela abaixo é a proposta original, mantida como histórico.

| # | Decisão | Proposta |
|---|---|---|
| **D1** | **Definição de "até 6 anos"**, já que 6 anos exatos não existe nos dados abertos (§3.2). Opções: (a) **0 a 5 anos** = `QT_MAT_BAS_0_3 + QT_MAT_BAS_4_5`; (b) **educação infantil por etapa** (`QT_MAT_INF`), que inclui crianças mais velhas retidas e exclui 6 anos no fundamental; (c) pedir microdados restritos ao INEP/SEDAP (fora do prazo). | **(a) 0 a 5**, que é a faixa da educação infantil (creche 0-3, pré 4-5) e corresponde à idade, não à etapa. O título passa a "Matrículas de crianças de 0 a 5 anos", e o nome do arquivo `matriculas_0_a_6_por_ano` é mantido ou renomeado (sub-decisão). A etapa (b) pode entrar como série complementar em D3. |
| **D2** | **O que fazer com 2007-2020**, que não bate com a fonte (§3.4). Opções: (a) **reconstruir a série inteira** a partir dos mesmos ZIPs do INEP e aposentar o CSV antigo; (b) juntar o antigo com o novo, com uma nota de quebra; (c) publicar só 2021+. | **(a)**: uma fonte e uma definição só. Os ZIPs de 2007-2020 existem e têm o mesmo formato (verificado pelo tamanho; 2020 lido). O CSV antigo vai para `git rm`, ou fica com uma nota de "não usado", sem apagar o histórico da spec. Alternativa mais barata: começar em 2015 ou 2019, para limitar downloads. |
| **D3** | **Recortes extras** a publicar. Opções: creche × pré (0-3 × 4-5); rede pública × privada; municipal × estadual × federal × privada; nenhum. | **Creche × pré** e **pública × privada**. Os dois são diretos das colunas e relevantes para a política municipal (a rede municipal é ~53% de 0-5 em 2023). |
| **D4** | **Anos**: "2021 em diante" inclui **2025**, que vem num ZIP de 537 MB com URL diferente e talvez outra estrutura (§3.1). | Incluir 2025 **se** o formato for compatível (verificar no Bloco 1). Se não for, publicar até 2024 e registrar 2025 como pendência. |
| **D5** | **Cache dos ZIPs**: `dados_locais/educacao/inep_microdados/` com regra no `.gitignore` (proposta) ou fora do repositório (scratch/`~`). | Dentro do repo, gitignorado, para que o notebook seja autossuficiente. |
| **D6** | **Taxa de atendimento** (matrículas ÷ população de 0-5 anos) nesta rodada? | **Não**: a projeção populacional anual por idade para 2021-2025 é outra fonte e outra discussão. Registrar no roadmap. *(Rascunho 3: usuário incluiu no escopo.)* |

### Decisões abertas (rascunho 3)

| # | Decisão | Proposta |
|---|---|---|
| **D7** | **Denominador da taxa** (§3.6). Opções: (a) **Ripsa/MS 2007-2025**, estimativa anual corrigida para sub-registro; (b) **Censo 2022** só, com taxa de um único ano, 9 pontos mais alta em 0-5 porque o Censo subconta crianças pequenas; (c) Ripsa na série, com o Censo 2022 citado na nota como comparação. | **(c)**: a série usa a Ripsa (anual, mesma base do Ministério da Saúde, corrigida). A nota de método mostra a taxa de 2022 com o Censo (64,9%) e explica a diferença, para ninguém comparar com números do Censo sem saber. |
| **D8** | **Metas do PNE** (50% em creche, 100% em pré-escola) no gráfico da taxa. Opções: (a) só citadas na nota do notebook; (b) linhas de referência no PNG e no HTML, com um parâmetro opcional novo (`linhas_referencia=None`) em `serie_temporal_multipla` e no `line_chart` do HTML. Default `None` não muda nenhum gráfico existente. | **(b)**: é a leitura que o público não técnico precisa ("quanto falta para a meta"), e o parâmetro opcional não afeta os outros gráficos. Se preferir não mexer em funções compartilhadas nesta rodada, fica (a). |
| **D9** | **Faixas da taxa.** Opções: 0-5 só; 0-3, 4-5 e 0-5; também por rede. | **0-3, 4-5 e 0-5** num gráfico só. Taxa por rede não faz sentido, porque a população não se divide por rede; o recorte por rede fica em contagem (D3). |

---

## 6. Pendências e riscos

- **P1: formato de 2025.** ✅ **Resolvida** (§3.5): tabelas separadas, contagens na
  `Tabela_Matricula`, mesmas colunas, latin-1. A função localiza o CSV pelos dois padrões de nome.
- **P2: data de referência da idade.** ✅ **Resolvida** (dicionário de 2025): última quarta-feira de maio de cada ano. Texto original: Pelo dicionário de dados (confirmar no `leia-me/` de cada ZIP),
  a idade é calculada na data de referência do Censo (última quarta-feira de maio). Isso vai para a
  nota de método.
- **P3: escolas paralisadas ou extintas.** ✅ **Resolvida** (2020): escolas com `TP_SITUACAO_FUNCIONAMENTO` 2 ou 3 (331 no Rio) têm 0 matrícula de 0-5, então não é preciso filtrar. Texto original: Verificar se `TP_SITUACAO_FUNCIONAMENTO != 1` tem
  matrícula > 0. Se tiver, decidir o filtro. Em 2023 a soma de `TP_SITUACAO_FUNCIONAMENTO` (4.615 em
  4.198 escolas) mostra que há escolas não ativas no arquivo.
- **P4: pipeline de relatório.** ✅ **Levantada**: `build_html_report.py:1415-1416`, `build_notebook_report.py:623-625` e `regen_missing_pngs.py:156-159` leem `matriculas_0_a_6_por_ano.csv` com o rótulo "0 a 6 anos" hard-coded. Nenhum trata o card como pendente. Texto original: Verificar como `build_html_report.py`, `build_notebook_report.py` e o
  DOCX leem `matriculas_0_a_6_por_ano.*` e se mostram o card como pendente (hard-coded, como
  aconteceu no CadÚnico, ver `specs/recortes_cadunico/plan.md` "Descobertas" item 2).
- **P6: 2007-2019 no formato novo.** A reconstrução da série inteira (D2) supõe que os ZIPs republicados
  de 2007-2019 têm `QT_MAT_BAS_0_3`/`_4_5` (só verificado por tamanho). É checado no Bloco 1, antes de
  qualquer código. Se faltarem as faixas de idade em algum ano, a série começa no primeiro ano com as
  colunas, e isso é registrado aqui.
- **P7: estabilidade do Tabnet.** O POST depende de nomes de campo com acento em latin-1 e do código
  interno `3262` do município. Se o Tabnet mudar, a função falha. Mitigação: extrato versionado
  (o notebook não depende da rede) e validação de que as linhas vêm com 19 anos e 7 idades. A Ripsa
  revisa as estimativas anualmente (nota técnica), então uma nova consulta pode mudar os anos antigos.
  Registrar a data da consulta no extrato (coluna `data_consulta`) e na nota.
- **P5: comparação com números oficiais.** Conferir 1 ou 2 anos contra a Sinopse Estatística do
  INEP (tabela de educação infantil por município) como validação externa.
