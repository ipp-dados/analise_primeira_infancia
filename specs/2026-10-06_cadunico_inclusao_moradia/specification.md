# SPECIFICATION — CadÚnico: pipeline novo para Inclusão e Moradia (rodada de 2026-10-06)

Status: **planejada em 2026-10-06** (branch `planning`); implementação em `spec/cadunico_inclusao_moradia`, depois
`staging_main` → `demo`. O *como* está em `plan.md`, as tarefas em `tasks.md`, os critérios de aceite em
`validation.md`.

## 1. Contexto

Pedido do usuário (2026-10-06): o banco CTPE tem a **bronze do CadÚnico atualizada** e duas tabelas **silver novas**
que trazem os dados de **Inclusão** (deficiência e assistência social) e de **Moradia**. Atualizar as duas seções com
esses dados, "corrigindo o pipeline"; figuras e mapas novos ganham blocos de lorem (texto curado vem na próxima
rodada); levar tudo para a `demo` com texto provisório; na `demo`, data prevista da V.1 passa a **13/10/2026**
(anunciada como atualização de conteúdo e texto) no site e no PDF, com a marca de que Inclusão e Moradia tiveram o
pipeline refeito. **O relatório (PDF) não é atualizado agora** — só o aviso do PDF da `demo`.

Levantamento no banco (2026-10-06, só agregados; nenhum microdado gravado):

| Tabela (`ctpe.`) | Linhas | Partição | Uso |
| :-- | --: | :-- | :-- |
| `bronze_cadunico` | 2.188.165 | 2026-07-10 | todos `Cadastrado`/`ativo` — responde à dúvida S9 (filtro de cadastro) |
| `silver_cadunico_geral` | 2.188.165 | 2026-07-10 | usada hoje pela seção CadÚnico |
| `silver_cadunico_pessoas` (**nova**) | 2.188.165 | 2026-07-10 | pessoa: `faixa_etaria` (`'0-5'`), deficiência por tipo, ajudas recebidas |
| `silver_cadunico_familias` (**nova**) | 1.118.753 | 2026-07-10 | família: déficit e inadequação (FJP) com componentes, adensamento, BPC, domicílio |
| `gold_cadunico_indicadores` | 10.654 | 2026-07-10 | só município (sem bairro) — não serve para os mapas; usado só como conferência |
| `dim_bridge_ceps_bairros` | 25.535 | — | CEP → `codigo_bairro` (código **oficial** IPP, 164 bairros, sem CEP ambíguo) |

Achados:
- **A1 — o pipeline atual está quebrado.** A `silver_cadunico_geral` foi refeita: o grupo `'0-6'` virou **`'0-5'`**
  (idades 0 a 5). `WHERE grupo_idade='0-6'` (seção CadÚnico e `carrega_cadunico_familias_0_6`) devolve **0 linhas**.
  Com o filtro corrigido: 200.784 crianças em 178.838 famílias (antes 194.019 / 173.680, partição de jun/2026).
- **A2 — o dado pontual não bate com a silver.** Extração pontual ago/2026: 25.995 crianças de 0 a 6 anos com
  deficiência; silver jul/2026: **7.919 de 0 a 5**. A diferença de faixa (6 anos) não explica 3×. Não se publica um ao
  lado do outro (D1); a origem da diferença fica registrada para a equipe (ROADMAP).
- **A3 — BPC é atributo da família** (`familia_bpc_deficiente`), não da criança, e vem vazio em parte das famílias
  (1.490 das 7.919 crianças com deficiência). Publica-se como famílias, com "não informado" fora do percentual.
- **A4 — "Não informado" e "Não se aplica"** aparecem nas variáveis FJP/adensamento. "Não se aplica" na inadequação é o
  domicílio improvisado/coletivo (já contado no déficit, metodologia FJP). Os dois ficam **fora do denominador** (como
  "Não informada" em E14, `specs/2026-09-29_pendencias`), e a base de cada percentual é publicada.
- **A5 — tamanho das células por bairro** (ponte do banco, numerador e complemento ≥ 20): passam sozinhos 58% dos
  bairros na deficiência, 59% na inadequação, 89% no adensamento e 90% no déficit. Os demais entram nos conjuntos por
  RA (`agrega_bairros_pequenos`), como nos mapas atuais.
- **A6 — a ponte do banco** cobre 90,9% das crianças (lista dos Correios: 92,1%), mas dá o código oficial (join por
  código, constituição §3) e põe no bairro certo Vila Kennedy, Lapa, Jabour, Gericinó, Ilha de Guaratiba e Complexo do
  Alemão — os casos da nota A2 de `recortes_cadunico`.

## 2. Decisões do usuário (2026-10-06)

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | Os itens **dado pontual** (ago/2026) de Inclusão e Moradia **saem** do crosswalk e do site, substituídos pelos itens da silver. Arquivos, carregadores e a célula de `analise.py` **ficam** (história; o deck ainda os lê) | a extração rotineira chegou; números incompatíveis lado a lado (A2) confundiriam; tira o bloqueio da versão final do site |
| D2 | Bairro das saídas **novas** pela ponte do banco (`dim_bridge_ceps_bairros`, código oficial). As saídas CadÚnico já existentes seguem com `lista_bairros.csv`; trocar todas fica no ROADMAP | join por código (constituição §3) sem mexer agora em mapas e textos já curados |
| D3 | Escopo **enxuto**, proposto nesta rodada (§3), com cortes registrados (§4) | pedido do usuário: avaliar se parte do dado é excessiva para esta etapa |
| D4 | `demo`: faixa com "Versão 1.0 prevista para 13 de outubro de 2026" e menção à próxima atualização de conteúdo e textos; **nota nas abas Inclusão e Moradia** ("dados atualizados: pipeline do CadÚnico refeito, jul/2026"); aviso do PDF da `demo` com a nova data | escolha do usuário |

Decididas na planificação (para revisão):
- **D5** — Corrigir o filtro `'0-6'` → `'0-5'` na seção CadÚnico inteira (A1): sem isso nada do CadÚnico roda. Os números
  das saídas existentes mudam para a partição de jul/2026; textos curados que citam números antigos ficam para a rodada
  de textos (lista em `validation.md`). Nomes de arquivo `*_0_6_*` mantidos (convenção da constituição).
- **D6** — Unidade: **crianças de 0 a 5 anos** (`faixa_etaria = '0-5'`, faixa padrão) e **famílias com ao menos uma
  criança de 0 a 5**. Atributos do domicílio vêm da família da criança.
- **D7** — Percentual sempre de absolutos, com "Não informado"/"Não se aplica" fora da base (A4); por bairro, só depois
  de `agrega_bairros_pequenos` com pares (numerador, base) — complemento também ≥ 20.
- **D8** — Textos: figuras/tabelas novas ficam em lorem em `staging_main` (automático: sem texto curado); na `demo`,
  texto provisório descritivo em `website/build/textos_demo.json`. Textos provisórios da `demo` que citam números do
  CadÚnico antigo são atualizados para jul/2026 (são provisórios e descritivos; não é curadoria).
- **D9** — PDF: não regerado em `staging_main`. Na `demo`, só a página de aviso muda (data); as 18 páginas impressas
  ficam como estão.

Decididas depois da implementação (usuário, 2026-10-06):
- **D10** — **"até 72 meses"** no lugar de "0 a 5 anos" em todo texto escrito do site (títulos, sumário, cartões, notas,
  títulos de gráfico e mapa, rótulos de tabela da silver nova), em todas as abas; os títulos renomeados guardam o id
  antigo (`antigo=`). Ficam: "0 a 4 anos" (Censo por bairro), "menores de 5 anos" (mortalidade), faixas em dias, chaves de
  dado, as notas que explicam a faixa ("até 72 meses (0 a 5 anos completos)") e os **textos curados** (rodada de textos).
  As PNG de outras seções (PDF, deck) ficam para a atualização do relatório.
- **D11** — critérios FJP explicados e exportados (`docs/criterios_fjp_cadunico.md`/`.csv`), a partir do ETL do CTPE
  (`Analise_cad_unico`, `src/cadunico_etl/moradia.py`). Rótulos ajustados à regra real (sem banheiro, não "exclusivo";
  todos os cômodos como dormitório; iluminação não elétrica; piso de terra). **Adensamento**: o CTPE usa **mais de 2
  pessoas por dormitório**; o catálogo diz "acima de 3". O site diz o que o dado mede (mais de 2). **Decidido pelo usuário
  (2026-10-06): fica mais de 2, também como título.**

## 3. Requisitos — escopo proposto

Todas as saídas: fonte `fonte_cadunico_com_particao` (jul/2026), nível município ou bairro (ponte), privacidade §6.

**Inclusão** (substitui os 3 pendentes e o item pontual de BPC):
- **R1 — Crianças no CadÚnico com alguma deficiência:** tabela no texto (crianças de 0 a 5, com deficiência, %) e
  **mapa de % por bairro** (escala contínua). Cartões no site.
- **R2 — Famílias no CadÚnico com criança com deficiência:** tabela no texto (famílias com criança de 0 a 5, com criança
  com deficiência, %; dessas, com BPC por deficiência, sem BPC, não informado, % com BPC entre as informadas — A3).
- **R3 — Crianças no CadÚnico por tipo de deficiência:** gráfico de barras e tabela (8 tipos; uma criança pode ter mais
  de um tipo — as barras não somam; nota).

**Moradia** (substitui os 3 pendentes e os 2 itens pontuais):
- **R4 — Crianças em domicílios com inadequação habitacional (FJP):** gráfico de barras dos componentes (água, esgoto,
  lixo, energia, banheiro, cômodos, piso; mais os totais infraestrutura/edilícia) e **mapa de % por bairro**.
- **R5 — Adensamento excessivo (mais de 3 pessoas por dormitório):** **mapa de % por bairro**; valor do município nos
  cartões e na tabela de R6.
- **R6 — Indicadores agregados de moradia:** tabela-resumo no texto (crianças e famílias: inadequação, infraestrutura,
  edilícia, déficit habitacional, adensamento, sem banheiro, sem água canalizada; número, base, %) e gráfico de barras
  dos componentes do **déficit** (improvisado, rústico, coabitação, ônus excessivo com aluguel).

Total: 3 gráficos, 3 mapas (+ tabelas gêmeas), 4 tabelas. Saídas existentes que não são de Inclusão/Moradia: só A1/D5.

**R7 — `demo`** (só lá, constituição §7): D4; textos provisórios para as chaves novas; build da `demo` sem lorem e sem
pendente; PDF da `demo` com a página de aviso nova.

## 4. Fora do escopo

- **Cortado por excesso nesta etapa** (ROADMAP, backlog): ajudas recebidas pela pessoa com deficiência
  (`ajuda_*`, fora do catálogo); formas de abastecimento de água e escoamento (o detalhe do dado pontual — os
  componentes FJP de água/esgoto cobrem o indicador); mapa do déficit (90% ônus de aluguel — repete renda);
  mapas por componente; recortes por idade, raça/cor ou renda das novas variáveis; cruzamento deficiência × moradia.
- Trocar a atribuição de bairro das saídas CadÚnico existentes (D2) e o deck (`apresentacao/`, ainda com o dado pontual).
- Texto curado (próxima rodada), PDF de `staging_main`, publicação (push/deploy: pendentes do ROADMAP §00, com OK).
- Investigar a diferença A2 (com a equipe que fez a extração pontual).
