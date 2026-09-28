# Especificação: População de referência (`specs/2026-09-24_populacao-referencia`)

Branch: `spec/populacao-referencia`. Aberta em 2026-09-24 como `spec/matriculas-censo-escolar` e renomeada no
mesmo dia, quando o escopo cresceu (usuário: "can we use ripsa data for the whole project? [...] check if we
can make this a larger reaching spec").
Status: **implementada** (2026-09-24, Blocos 1-8; ver `tasks.md`). Rascunho 2 aprovado; ok para implementar
dado pelo usuário em 2026-09-24; decisões da Parte C (C-D2..C-D4) em `auditoria_faixas.md` §6-7.

> Histórico: rascunho 1 (ampliação, A-E), rascunho 2 (decisões, item 7 reinterpretado, A4 verificada).
Roadmap: itens **6** (população por bairro ano a ano, auditoria de faixas etárias, revisão de nomes) e **7**
(percentual de nascidos vivos por bairro da mãe), e a seção "Matrículas".
Desdobramento: `plan.md`, `tasks.md`, `validation.md` e a subpasta `matriculas/` (Parte E, que já estava
especificada e aprovada antes da ampliação; ver o histórico lá).

---

## 1. Objetivo

Dar ao projeto **uma população de referência explícita e consistente** para todo cálculo que divide por
população, e fechar as lacunas de indicadores ligadas a isso:

| Parte | O quê | Roadmap |
|---|---|---|
| **A** | **Nível município: estimativas Ripsa/MS 2000-2025** (idade simples, sexo) como denominador de toda taxa municipal, mais uma série nova de população infantil ano a ano | 6 |
| **B** | **Níveis bairro/AP/RP/RA/CAP: Censo 2022 como referência fixa**, com rótulos e notas explícitos (decisão B1) | 6 |
| **C** | **Auditoria de faixas etárias entre fontes e revisão de nomes** de tabelas, visualizações e mapas | 6 |
| **D** | **Itens do crosswalk sem arquivo**, incluindo o percentual de nascidos vivos por bairro da mãe | 7 |
| **E** | **Matrículas e taxa de atendimento de 0 a 5 anos** (Censo Escolar/INEP + Ripsa), especificada em `matriculas/` | Matrículas |

**Ordem aprovada (usuário, 2026-09-24): população primeiro.** A Parte A vem antes de tudo, porque E e parte
de D dependem dela. A Parte C vem por último, porque renomeia arquivos criados nas outras partes.

---

## 2. Inventário: onde o projeto usa população hoje (levantamento de 2026-09-24)

| Análise (`analise.py`) | Nível | Denominador atual | Destino nesta spec |
|---|---|---|---|
| Violência familiar, taxa por 1.000 (`~3440-3530`; mapas M8-M13, top 10) | bairro, RA, CAP | Censo 2022, **0-4** (`carrega_pop_0_4_bairro`); numerador Sinan **0-5**, 2025 | **B**: mantém o Censo, com rótulos explícitos. **A**: taxa municipal anual nova (A3) |
| CadÚnico, % de crianças sobre o Censo (`~1557-1590`; mapa só no notebook, fora do relatório pela D6 de `recortes_cadunico`) | bairro | Censo 2022, 0-4; numerador CadÚnico 0-6 (na prática 0-5), 2026 | **B** (inalterado; o mapa continua fora). **A**: razão municipal nova (A4) |
| Censo 2022, crianças de 0-4 e % da população por bairro/AP/RP (`~1102-1275`) | bairro, AP, RP | Censo 2022 | **B**: é a própria descrição do Censo, fica como está |
| Evolução de 0-4 nos Censos 2000/2010/2022 (`~1279-1340`) | município | Censo | Fica. **A** acrescenta a série anual Ripsa ao lado |
| População de 0-6 por raça/cor e sexo (SIDRA 9606, `~1147-1185`) | município | Censo 2022 | Fica: a Ripsa não tem raça/cor |
| Taxa de atendimento de 0-5 (nova) | município | — | **A/E**: Ripsa (D7 de `matriculas/`) |
| Mortalidade infantil, neonatal, materna, baixo peso | bairro, CAP, município | nascidos vivos | Sem mudança: nascidos vivos é o denominador correto |
| Cobertura vacinal, SISVAN, PNAD | município | denominador da própria fonte | Sem mudança |

Nenhuma taxa municipal usa população hoje. Todas as taxas por população são sub-municipais e usam o Censo
2022.

---

## 3. Fonte do nível município: Ripsa/MS

**"População residente: estudo de estimativas populacionais por município, idade e sexo, 2000-2025"**
(Nota Técnica Ripsa nº 01/2025, doi:10.5281/zenodo.17990183; 2ª versão, com 2025). Estimativa em
**1º de julho**, por **município × sexo × idade simples (0-79, 80+)**, revisada depois do Censo 2022 e
ajustada às Projeções do IBGE (revisão 2024). É a base que o Ministério da Saúde usa para os indicadores
municipais.

- **Não tem bairro.** O nível mais fino do Tabnet é `Município`; os outros são Região, UF, Capital, Região
  de Saúde, Macrorregião, Microrregião e RIDE. Não achamos fonte pública de população por bairro × idade
  × ano. O Data.Rio tem o Censo 2022 por bairro e o total municipal por ano sem idade, e o TabNet
  municipal da SMS-Rio não tem tabela de população. Daí a decisão B1.
- **Acesso:** POST no Tabnet `http://tabnet.datasus.gov.br/cgi/tabcgi.exe?ibge/cnv/popsvs2024br.def`,
  `SMunicípio=3262` (330455 Rio de Janeiro), `formato=prn`. **Não usar** `popsvsbr.def`, que é a versão
  2000-2021. O servidor derruba conexões às vezes (`ConnectionResetError` em 2 de 5 consultas no
  levantamento), então a função precisa de retry, e o notebook lê de um extrato versionado.

**Números de referência (consulta de 2026-09-24), Rio de Janeiro:**

| Ano | Total (todas as idades) | 0-4 | 0-5 | % 0-4 no total |
|---|---|---|---|---|
| 2000 | 6.312.372 | 497.379 | 598.322 | 7,9% |
| 2010 | 6.605.732 | 400.636 | 482.670 | 6,1% |
| 2015 | 6.724.719 | 412.521 | 491.681 | 6,1% |
| 2020 | 6.770.926 | 389.268 | 474.322 | 5,7% |
| 2022 | 6.742.618 | 361.163 | 439.907 | 5,4% |
| 2024 | 6.729.894 | 331.402 | 407.537 | 4,9% |
| 2025 | 6.730.729 | 320.791 | 393.073 | 4,8% |

O total de 2024 (6.729.894) bate com a estimativa municipal do IBGE publicada no Data.Rio, o que serve de
validação externa. A série completa (26 anos, idade simples 0-6, sexo) vai para `validation.md`.

**Achado: a Ripsa fica acima do Censo 2022 em todas as idades, não só nas crianças.**

| 2022 | Censo 2022 | Ripsa 2022 | Diferença |
|---|---|---|---|
| Total | 6.211.223 | 6.742.618 | +8,6% |
| 0-4 | 310.648 (SIDRA 9606) | 361.163 | +16,3% |
| 0-5 | 379.609 | 439.907 | +15,9% |
| < 1 ano | 54.337 | 64.701 | +19,1% |

O IBGE corrigiu nas Projeções (revisão 2024) a cobertura incompleta do Censo 2022, e a Ripsa herda essa
correção. Consequências para o projeto:
1. As **participações de 0-4 na população** calculadas com o Censo (7,1% / 5,4% / 4,7% em 2000/2010/2022,
   citadas numa nota de curadoria em `analise.py:1232`) e com a Ripsa (7,9% / 6,1% / 5,4%) **não são
   comparáveis**. Cada número tem que dizer de onde vem. As notas de curadoria são do usuário e não são
   reescritas; entra só uma nota técnica ao lado.
2. **Taxas sub-municipais com o Censo como denominador ficam altas** (denominador subcontado). Isso vai
   para a nota da Parte B.

---

## 4. Partes

### Parte A: população de referência municipal (Ripsa)

- **A1: Função e extrato.** `carrega_populacao_ripsa(anos, idades, por_sexo)` no topo de `analise.py`,
  que substitui a função de mesmo nome planejada em `matriculas/plan.md` e ganha sexo e total. Extrato
  versionado `dados_locais/populacao/ripsa_populacao_rio.csv` com: ano 2000-2025 × idade 0-6 × sexo (364
  linhas), mais o total de todas as idades por ano (26 linhas), com a coluna `data_consulta`. É uma pasta
  nova, `dados_locais/populacao/` (constitution §3: uma pasta por fonte ou tema), com retry no POST.
- **A2: Série de população infantil (nova).** Tabela e gráfico da população de 0-6 anos por ano,
  2000-2025, e da participação no total. Isso preenche o item do crosswalk "Crianças até 6 anos (número)",
  hoje sem arquivo (Parte D). Faixa a exibir: decisão A-D1.
- **A3: Taxa municipal de violência familiar (nova, proposta).** Notificações de 0-5 anos por vínculo
  (mãe, pai, outros) ÷ população Ripsa de 0-5 do mesmo ano × 1.000, de 2011 a 2025. As faixas coincidem (o
  Sinan é 0-5 e a Ripsa tem 0-5 exato), então a ressalva D9 de `inclusao_dados_protecao` não se aplica no
  nível município. Decisão A-D2.
- **A4: Razão municipal CadÚnico/população (nova, proposta).** Crianças de 0-5 no CadÚnico (partição
  2026-06-12: 194.138) ÷ população Ripsa de 0-5 em 2025 (393.073) ≈ 49,4%. Ressalvas: um ano de diferença
  (2026 × 2025); cadastro × estimativa; a faixa "0-6" do CadÚnico é 0-5 completos (auditoria C). Exige
  `.env` e o kernel `analises_env`. Decisão A-D2.
  **Verificado em 2026-09-24:** a conexão com o `.env` atual funciona no `analises_env`. A partição mais
  recente de `ctpe.silver_cadunico_geral` continua `2026-06-12`, com `grupo_idade='0-6'` = **194.138
  crianças, 173.768 famílias, idade 0-5**. Razão = 194.138 ÷ 393.073 = **49,4%**.
- **A5: Nota metodológica geral** (markdown, no início da seção Censo 2022 de `analise.py`, antes de
  qualquer taxa): população de referência por nível (Ripsa no município, Censo 2022 abaixo), diferença
  Ripsa × Censo (tabela de §3), revisões anuais da Ripsa e onde cada uma é usada. As notas de E (D7) e B
  apontam para esta.

### Parte B: níveis sub-municipais (Censo 2022, referência fixa)

**Decisão B1 (usuário, 2026-09-24): opção (a).** O Censo 2022 continua como denominador de bairro, AP, RP,
RA e CAP, **sem** estimativa derivada por ano. As opções (b) (participação do Censo × total Ripsa por ano)
e (c) (participação variando entre 2010 e 2022) ficam registradas e fora do escopo. O trabalho da Parte B
é deixar a referência **explícita**:

- **B2:** toda saída sub-municipal com população no denominador cita na `fonte_dados` e no título ou
  legenda: "população de 0 a 4 anos, Censo 2022". Hoje `fonte_sinan_censo` já cita isso, e a Parte B
  confere os demais (mapas M8-M13, tabelas `violencia_familiar_taxa_*`, `tabela_mapa_*`, cards do HTML).
- **B3:** a nota da seção de violência (ressalva D9) ganha dois pontos: (i) os anos diferentes, com numerador
  2025 ou 2021-2025 contra população 2022, e (ii) o Censo subconta crianças pequenas (§3), então as taxas
  por bairro tendem a ficar mais altas do que com uma estimativa corrigida. Sem mudar nenhum cálculo.
- **B4:** nenhuma taxa sub-municipal nova nesta rodada.

### Parte C: auditoria de faixas etárias e revisão de nomes (roadmap 6)

- **C1: Auditoria (entregável: tabela em `auditoria_faixas.md` nesta pasta).** Para cada fonte, a faixa
  etária real do dado, a data de referência da idade e os rótulos usados em títulos, legendas, nomes de
  arquivo e textos. Já se sabe: CadÚnico `'0-6'` = 0-5 completos (6 anos caem em `'7-14'`); Censo por
  bairro = 0-4; SIDRA 9606 = idade simples 0-6; Sinan = 0-5; Ripsa = idade simples; Censo Escolar = 0-3/4-5
  (Parte E); SISVAN e vacinação a levantar.
- **C2: Padronização de rótulos.** Depois da auditoria, cada título, legenda e texto diz a faixa real
  ("0 a 5 anos", "0 a 4 anos"). "Até 6 anos" ou "0-6" só onde o dado for 0-6 de fato. Não mexe em notas
  de curadoria (texto do usuário); se uma nota de curadoria citar faixa errada, ela entra numa lista para
  o usuário.
- **C3: Revisão de nomes** (`tabelas_finais/`, `visualizacoes/`, `mapas/`): nome ≠ conteúdo, faixa no
  nome ≠ faixa do dado, órfãos, e leitores nos três scripts de relatório. A lista de renomeações vai
  para o usuário aprovar **antes** de executar (decisão C-D1), porque renomear mexe em arquivos rastreados
  e nos leitores.

### Parte D: itens do crosswalk sem arquivo (inclui roadmap 7)

**Rascunho 2: item 7 reinterpretado pelo usuário** ("the percentual por bairro da mae is probably just
the number of nascidos vivos"). O "percentual" do catálogo é a mesma informação que a contagem, só
dividida por uma constante (o total do município no ano). O mapa teria o mesmo desenho do mapa de
contagem que já existe. **Resolução (D1 revisada):** não criar mapa novo. O item do crosswalk passa a
apontar para as saídas de contagem existentes (`mapa_nascidos_vivos_bairro_2025.png`,
`tabela_mapa_nascidos_vivos_2025.csv`), e a gêmea ganha uma coluna `percentual_do_municipio` (nascidos
vivos do bairro ÷ total do município × 100), para a fórmula do catálogo ficar disponível na tabela e no
tooltip do HTML. A proposta original (mapa próprio) fica abaixo como histórico.

**Causa do item 7 (diagnóstico de 2026-09-24, rascunho 1):** o indicador do catálogo "Percentual de nascidos vivos por
bairro de residência da mãe", com metodologia "(nº de nascidos vivos segundo bairro de referência da mãe ÷
nº de nascidos vivos no município) × 100" e visualização em mapa coroplético, **nunca foi implementado**.
Não há código em `analise.py`, e a entrada em `estrutura_eixos.md:44` não lista arquivo. O HTML e o PDF
**pulam em silêncio** itens sem arquivo e sem `status: pendente`, por isso ele não aparecia. Não é título
trocado. (O percentual de **baixo peso** existe e aparece: é outro indicador.) Não depende de população.

Itens do crosswalk sem arquivo e sem `status` (varredura de `estrutura_eixos.md`):

| Item | Eixo | Proposta |
|---|---|---|
| Nascidos vivos por bairro de residência da mãe (percentual) | Prioridade | *(Rascunho 2: substituída pela resolução acima, que liga às saídas de contagem e acrescenta a coluna %.)* Proposta original: **D1: implementar.** Mapa 2025 por bairro, contínuo (percentual); tabela gêmea; divisor = nascidos vivos do município **incluindo** "EM BRANCO" (bairro não informado), para a soma dos bairros não chegar a 100% e isso ficar visível. Decisão D-D1 |
| Crianças até 6 anos (número) | Prioridade | **D2:** preencher com a série da Parte A (A2) |
| Crianças até 6 anos frequentando escola/creche (geral) | Família e Cuidados | **D3:** os CSV da SIDRA 10057 já carregados têm a categoria "Total" (o código a filtra fora dos gráficos por raça e sexo), e as tabelas pivotadas `sidra_frequencia_escola_0_5_*_2022.csv` já trazem a coluna `Total`. Proposta: gráfico de barras do Total por idade (0-5), mais a tabela, ligados ao item. **Faixa real 0-5**: o rótulo "até 6 anos" do item entra na auditoria C |
| Mortalidade infantil por causas evitáveis, por sexo | Prioridade | **Fora do escopo** (não é população). Marcar `status: pendente` para aparecer como pendente, e não sumir |

- **D4:** proposta de guarda no gerador do HTML/PDF para listar no console os itens do crosswalk sem
  arquivo e sem `status`, para isso não se repetir. É só um aviso e não muda a saída. Decisão D-D2.

### Parte E: matrículas e taxa de atendimento (subpasta `matriculas/`)

Especificada e aprovada antes da ampliação (D1-D9 de `matriculas/specification.md`, rascunho 4). O que muda
com a ampliação:
- a função de população passa a ser a da Parte A (A1), e não uma função própria;
- a nota metodológica de D7 aponta para a nota geral A5 e mantém os pontos específicos da taxa (bruta,
  datas, PNE);
- os commits passam a usar o prefixo `SPEC-PopulacaoReferencia: Bloco N (Parte E) -- …`;
- a execução vem **depois** da Parte A.

---

## 5. Decisões

### Aprovadas (usuário, 2026-09-24)

- **Ampliar a spec** e renomear branch e pasta para `populacao-referencia` ✅ (feito: a pasta antiga virou
  `matriculas/`, com o histórico preservado pelo `git mv`).
- **Ordem:** população primeiro ✅.
- **B1:** sub-municipal fica no Censo 2022, opção (a) ✅.
- **Parte E:** todas as decisões de `matriculas/` (D1-D9) seguem valendo.

- **Rascunho 2 (usuário, 2026-09-24):** A-D1 ✅ (0-6 por idade simples) · A-D2 ✅ (A3 e A4) · C-D1 ✅ ·
  D-D1 ✅, **mas o item 7 foi reinterpretado** (Parte D, resolução acima) · D-D2 ✅. A4 foi confirmada
  viável com o `.env` atual.

### Abertas no rascunho 1 (todas decididas no rascunho 2)

| # | Decisão | Proposta |
|---|---|---|
| **A-D1** | Faixa da série de população infantil (A2): 0-5, 0-6 ou as duas. | **0-6 por idade simples** (o catálogo diz "até 6 anos" e a Ripsa tem 0-6 exato), com o total 0-5 na tabela, para bater com as outras taxas. O gráfico mostra o total 0-6 e a participação no total da população. |
| **A-D2** | Taxas municipais novas: A3 (violência familiar por 1.000, 2011-2025) e A4 (razão CadÚnico/população). | **As duas.** A3 é a mais limpa do projeto (mesma faixa e mesmo ano no numerador e no denominador). A4 é um número-resumo forte para o eixo Inclusão, com as ressalvas escritas. Onde entram no crosswalk: A3 em Proteção, A4 em Inclusão. |
| **C-D1** | Renomeações da Parte C. | Executar **só depois** de o usuário aprovar a lista gerada pela auditoria (C1), num bloco próprio. |
| **D-D1** | Item 7: nível e anos. O catálogo pede mapa por bairro. | Mapa de 2025 por bairro, mais tabela gêmea. Sem AP/RP nesta rodada, porque o indicador é participação no total do município e somar por AP é trivial se quiserem depois. |
| **D-D2** | Aviso no gerador para itens sem arquivo (D4). | Sim, só aviso no console. |

---

## 6. Pendências e riscos

- **P-A1: estabilidade e revisões do Tabnet/Ripsa.** Conexão instável (retry), nomes de campo com acento em
  latin-1, código interno `3262`. A Ripsa revisa anualmente, então uma nova consulta pode mudar anos passados.
  Mitigação: extrato versionado com `data_consulta` e checagem de 26 anos × 7 idades × 2 sexos.
- **P-A2: CadÚnico (A4)** exige `.env` e `analises_env`. ✅ Acesso confirmado em 2026-09-24 (partição
  `2026-06-12`). Se a partição mudar antes da implementação, o número muda, e V2 registra a partição usada.
- **P-B1: cards do HTML com rótulo hard-coded.** Os rótulos de fonte nos cards de violência do
  `build_html_report.py` são strings. B2 tem que alterar o gerador também, não só `analise.py`.
- **P-C1: alcance da renomeação.** Arquivos rastreados antes de 2026-09-22 seguem no git (constitution §3,
  atualização de 2026-09-23). Renomear exige `git rm` do antigo e `git add -f` do novo, mais os leitores.
- **P-D1: "EM BRANCO" no denominador** da coluna `percentual_do_municipio`. O denominador é o total do
  município **incluindo** "EM BRANCO", para a soma dos bairros ficar abaixo de 100% quando houver
  nascidos sem bairro. Registrar quantos são em 2025.
- As pendências da Parte E (P1-P7) estão em `matriculas/specification.md` §6.
