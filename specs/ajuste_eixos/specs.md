# Especificação — Reorganização por Eixos da Política Municipal (`specs/ajuste_eixos`)

## 0. Contexto

O projeto hoje organiza tudo (`analise.py`, `relatorio/index.html`, o PDF) por
**fonte de dado**: Censo 2022, CadÚnico, DataSUS/Tabnet (nascidos vivos, baixo
peso, mortalidade — raça, causas evitáveis, gravidez/puerpério, neonatal),
SISVAN, Cobertura Vacinal EPI, IBGE SIDRA/PNAD/Censo Escolar — 9 seções `h2`
em `index.html`, na mesma ordem em `analise.py`. Isso é reconhecido como
pendência no roadmap: `specs/roadmap.md` já lista "Reorganizar a estrutura do
relatório... ainda sem spec próprio" como prioridade 3. Esta rodada formaliza
esse spec.

O pedido desta rodada muda o eixo de organização de "fonte de dado" para
**eixo da política municipal de primeira infância** — usando como fonte de
verdade uma planilha de planejamento já existente,
`dados_locais/painel_primeira_infancia_cesta_indicadores.xlsx` (catálogo de
65 indicadores, mantido por quem coordena o painel, não gerado por
`analise.py`).

### 0.1 Estado atual (levantado nesta rodada)

- **`analise.py`**: ~2500 linhas, `py:percent`, funções auxiliares no topo,
  9 blocos de análise em sequência (ver `CLAUDE.md`). A seção final "Análise
  / Relatório" (só markdown, sem código, deliberadamente fora do HTML/PDF)
  já tem 5 subtítulos-esqueleto — `Demografia e População`, `Assistência
  Social`, `Educação`, `Saúde`, `Proteção` — que antecipam uma síntese por
  eixo, mas nunca foram preenchidos.
- **`relatorio/index.html`** (v6.7, ver `relatorio/specs.md`): 9 `h2` na
  mesma ordem de `analise.py`, ~126 chart-cards/map-cards, seletor de opções
  (pills) já usado para agrupar cortes correlatos, bloco de texto de
  análise por opção em lorem ipsum (150 palavras/bloco, decisão v6.5).
- **PDF** (`.claude/skills/export_pdf_report`): espelha `analise.py`
  seção a seção com os PNGs reais do matplotlib — pipeline independente do
  HTML (motor SVG vs. PNG), mesma ordem de conteúdo.
- **DOCX**: não existe hoje. `python-docx` não está em `requirements.txt`.
- **Catálogo** (`painel_primeira_infancia_cesta_indicadores.xlsx`): 3 abas —
  `Indicadores` (65 linhas, 17 colunas — a fonte relevante aqui), `Visão
  geral` (5 eixos de fonte de dado, pergunta-chave e indicadores-chave por
  eixo) e `Esqueleto dos painéis` (notas soltas sobre um painel futuro
  "5 painéis, um por eixo" — não é o que esta rodada implementa, ver §9).

## 1. Objetivo

1. Reorganizar **todas** as visualizações, tabelas e mapas hoje existentes
   segundo as colunas `Eixo da Política Municipal Prioritário`/`Secundário`
   do catálogo, não mais por fonte de dado.
2. Produzir um **documento de estrutura** (`.md`) que é a fonte única e
   **editável pelo usuário** dessa organização — hierarquia de eixos,
   subseções, fontes de dado, visualizações e mapas de cada uma. Editar esse
   arquivo e pedir "atualiza" deve bastar para propagar a mudança de
   estrutura para `analise.py`/`analise.ipynb`, `relatorio/index.html` e o
   PDF, sem precisar reexplicar o pedido (§5).
3. Reorganizar `analise.py`/`analise.ipynb` segundo essa estrutura (não só
   os relatórios de saída — ver risco em §9.1).
4. Reorganizar `relatorio/index.html` segundo a mesma estrutura.
5. Um relatório final em PDF com a mesma estrutura (mesmo conteúdo do HTML,
   sem a interatividade).
6. Toda subseção que representa uma visualização ganha um bloco de texto de
   100–200 palavras — hoje isso já existe como lorem ipsum no HTML (150
   palavras, v6.5); passa a ser o padrão explícito também no PDF e no novo
   DOCX (§7).
7. Um novo **DOCX de curadoria**: lista todas as visualizações/mapas
   (organizados pela nova estrutura) cada um seguido do seu bloco de texto
   placeholder, para edição manual fora do notebook.
8. Esse DOCX é editado à mão pelo usuário com o texto final; o texto final
   volta para o notebook/HTML/PDF — precisa de um skill dedicado (§8).
9. Bloco com múltiplas visualizações/mapas (padrão já existente de seletor
   de opções no HTML, v6.2): cada opção mantém seu **próprio** bloco de
   texto, que troca junto com a seleção — já é o comportamento do HTML;
   o DOCX precisa do equivalente (um bloco de texto por opção, não um só
   por card, ver §7).

## 2. O catálogo `painel_primeira_infancia_cesta_indicadores.xlsx`

### 2.1 A aba `Indicadores` (65 linhas)

Colunas relevantes: `Indicador`, `entregaveis` (data), `Status`, `Eixo`
(fonte de dado — População/Assistência Social/Educação/Proteção/Saúde, já
usado hoje), `Eixo da Política Municipal Prioritário`, `Eixo da Política
Municipal Secundário`, `Fonte`, `Nível de desagregação`, `Forma de
visualização` (x2).

### 2.2 Duas taxonomias, nenhuma com exatamente "5 eixos"

Levantamento feito nesta rodada (valores não-vazios):

| Coluna | Valores distintos | Observação |
|---|---|---|
| `Eixo` (já em uso) | Saúde (21), Assistência Social (13), População (7), Educação (5), Proteção (4), 15 em branco | 5 valores — bate com a aba `Visão geral` e com a organização atual de `analise.py` |
| `Eixo da Política Municipal Prioritário` | Prioridade (35!), Proteção (7), Alimentação (6), Inclusão (6), Direito ao Brincar (4), Moradia (4), Direito à cidade (2), Participação (1) | 8 valores, mais da metade das linhas caem em "Prioridade" — um valor genérico, não um eixo de política real |
| `Eixo da Política Municipal Secundário` | Família e Cuidados (13, incl. 1 grafia alternativa "Famílias e cuidados"), Inclusão/Famílias e cuidados (5, tag composta), Inclusão (2), Prioridade (1), 40 em branco | Maioria em branco; usado nesta rodada só como fallback (§3) |

Decidido com o usuário (ver §3): a estrutura desta rodada usa a coluna
**Prioritário**, com fallback para a **Secundário** quando o valor
primário é o genérico "Prioridade" — não a coluna `Eixo` nem uma redução
artificial a 5 categorias.

## 3. Decisões desta rodada

| # | Pergunta | Decisão (confirmada com o usuário) |
|---|---|---|
| A | Qual taxonomia define a estrutura de topo? | `Eixo da Política Municipal Prioritário` (8 valores reais) — não a coluna `Eixo`, não reduzida a 5. Citação do usuário: "use 8 eixos, add sections for missing data, but highlight them, some of them may be removed later" |
| B | O que fazer com as 35 linhas tagueadas só "Prioridade" (54% do catálogo)? | Usar a coluna **Secundário** como fallback nessas linhas — se ela tiver valor, o indicador migra para lá; se também estiver vazia, fica no bucket residual "Prioridade (sem secundário)" |
| C | Normalização de grafia/tags compostas (feita nesta rodada, não perguntada — documentar para revisão) | "Famílias e cuidados" (1) tratado como a mesma categoria de "Família e Cuidados" (13) → bucket único, 8 linhas. Tag composta "Inclusão / Famílias e cuidados" (5) tratada como pertencendo a **Inclusão** (por ordem de menção), com nota de referência cruzada para Família e Cuidados |
| D | Bucket residual "Prioridade (sem secundário)" (20 indicadores, 31% do catálogo) | Mantido como um eixo próprio nesta rodada, não redistribuído por adivinhação — o usuário sinalizou que "alguns podem ser removidos depois", então fica marcado como candidato a reclassificação futura, não uma seção definitiva |
| E | Reservar espaço para indicadores do catálogo ainda não implementados em `analise.py`? | Sim, mas não para os que já têm `entregaveis` real — na prática, os indicadores até "Número de famílias no CadÚnico por renda e arranjo familiar" (33ª linha do catálogo). Os que vêm depois (violência/proteção, recortes por raça/sexo em Educação, deficiência no CadÚnico, moradia, risco ambiental) ganham seção reservada e **destacada como pendente**, não uma seção vazia sem aviso |
| F | Regra E é perfeita? | Não — cruzando com a coluna `Status` aparecem exceções reais à posição no catálogo (§4.2); a regra final passou a usar `Status` diretamente, não a posição (ver §4.2) |
| G | Descarte de indicadores inviáveis/desnecessários (revisão feita pelo usuário sobre a lista de não-implementados, ver §4.4) | 18 dos 65 indicadores do catálogo descartados nesta rodada — 3 eixos (Direito ao Brincar, Direito à cidade, Participação) ficam sem nenhum indicador restante e são **removidos da estrutura** (§4.3/§4.4) |

## 4. Estrutura proposta: 6 eixos ativos (3 descartados por completo)

### 4.1 Regra de classificação

```
bucket(indicador):
  p = Eixo da Política Municipal Prioritário
  s = Eixo da Política Municipal Secundário
  se p vazio:            sem classificação (não deve ocorrer nas 65 linhas — confirmar se aparecer)
  se p != "Prioridade":   bucket = p                         (Proteção, Alimentação, Inclusão,
                                                                Direito ao Brincar, Moradia,
                                                                Direito à cidade, Participação)
  se p == "Prioridade":
    se s vazio:           bucket = "Prioridade (sem secundário)"
    senão:                bucket = normaliza(s)              (→ Família e Cuidados, ou Inclusão)
```

`normaliza(s)`: `"Famílias e cuidados"` → `Família e Cuidados`;
`"Inclusão / Famílias e cuidados"` → `Inclusão` (+ referência cruzada);
demais valores usados como estão.

### 4.2 Regra de status: `Status` da planilha, não a posição no catálogo

A regra E (§3) originalmente usava a posição no catálogo (indicadores até o
33º, "renda e arranjo familiar") como proxy de "já implementado". Cruzando
com a coluna `Status` apareceram exceções reais — a posição não é
confiável sozinha:

| Indicador | Posição | `Status` | Tratamento correto |
|---|---|---|---|
| SCFV 0 a 6 anos georreferenciado | antes do corte | vazio | Não implementado, apesar de estar "antes" |
| Matrículas na educação básica 0-6 | antes do corte | "até 2020, tratar microdados posteriores" | Parcialmente implementado (`matriculas_0_a_6_por_ano.png` existe, só até 2020) — placeholder de "atualização pendente" |
| Famílias CadÚnico por sexo/raça/renda+arranjo (3 indicadores) | antes do corte | "Fazer recorte - Léo" | Não implementado, apesar de estar "antes" |
| Crianças 0-6 frequentando escola/creche (geral, por raça, por sexo) | depois do corte | "ok" | **Já implementado** (`sidra_frequencia_escola_0_5_raca_2022.png`, `..._sexo_2022.png`, tabelas SIDRA/PNAD correspondentes), apesar de estar "depois" |

**Correção adotada**: a regra final usa `Status` diretamente —
`implementado` = a célula `Status` começa com "ok" (case-insensitive);
qualquer outro valor (vazio, "Posterior", "Fazer recorte...", "Não
dispomos de dados", "Incorporar no relatório", etc.) = ainda não
implementado. Mais confiável que a posição e é exatamente essa coluna que
o usuário usou para decidir os descartes do §4.4.

### 4.3 Os 6 eixos ativos, contagem e status de implementação

Depois do descarte de 18 indicadores (§4.4), 3 dos 9 buckets (Direito ao
Brincar, Direito à cidade, Participação) ficam **sem nenhum indicador
restante** e saem da estrutura por completo — não é mais "9 eixos", são
**6 eixos ativos**:

| Eixo | Ativos | Implementado | A reservar/destacar | (Descartados) |
|---|---:|---:|---:|---:|
| Prioridade (sem secundário) | 15 | 15 | 0 | 5 |
| Inclusão | 10 | 4 | 6 | 3 |
| Família e Cuidados | 7 | 6 | 1 | 1 |
| Proteção | 5 | 0 | 5 | 2 |
| Alimentação | 6 | 6 | 0 | 0 |
| Moradia | 4 | 0 | 4 | 0 |
| ~~Direito ao Brincar~~ | 0 | — | — | 4 (removido) |
| ~~Direito à cidade~~ | 0 | — | — | 2 (removido) |
| ~~Participação~~ | 0 | — | — | 1 (removido) |
| **Total** | **47** | **31** | **16** | **18** |

Conteúdo de cada eixo ativo (indicadores do catálogo, já sem os
descartados; visualização/tabela/mapa específico de `analise.py` por
indicador é trabalho de `tasks.md` — §4.5 mostra o método com um eixo já
resolvido por completo):

- **Prioridade (sem secundário)** (15, todos já implementados) — número/
  percentual de crianças até 4/6 anos (Censo), nascidos vivos por bairro
  (número e %), crianças e famílias no CadÚnico (recorte geral e por
  renda), taxas de mortalidade neonatal (precoce/tardia), mortalidade
  infantil por raça/cor e por causas evitáveis (geral, por tipo de causa,
  por raça, por sexo), taxa de mortalidade na primeira infância. **Núcleo
  de indicadores de sobrevivência/existência básica** sem uma bandeira de
  política mais específica no catálogo — nome de working title, a revisar.
- **Inclusão** (10: 4 implementados, 6 a reservar) — crianças até 6 por
  sexo/raça (Censo, implementado), crianças frequentando escola/creche por
  raça/sexo (implementado), famílias no CadÚnico por sexo/raça/renda+
  arranjo (3, a reservar — "Fazer recorte"), crianças/famílias no
  CadÚnico com deficiência (3, a reservar — "baixar dados").
- **Família e Cuidados** (7: 6 implementados, 1 a reservar) — taxa bruta de
  frequência escolar 0-6, cobertura vacinal de rotina <2 anos
  (implementados); matrículas na educação básica 0-6 (a reservar —
  atualização pendente pós-2020, ver §4.2).
- **Proteção** (5, nenhum implementado) — violência territorial, violência
  familiar, notificações de violência interpessoal/autoprovocada, taxa de
  notificações 0-6, crianças que sofrem violência por tipificação. Próximo
  eixo de dado a importar (`specs/roadmap.md`, item "Educação e Violência").
- **Alimentação** (6, 100% implementado) — baixo peso ao nascer (número e
  %), desnutrição SISVAN (número e %), sobrepeso SISVAN (número e %).
- **Moradia** (4, nenhum implementado, todos "Posterior") — crianças no
  CadÚnico em domicílios com inadequação habitacional / adensamento
  excessivo, territórios com risco a inundação/movimento de massa
  (checar se é o mesmo indicador que aparece com `Eixo` fonte-de-dado
  "Proteção" mas política "Moradia" — não é uma duplicata de linha, é a
  mesma linha com as duas colunas divergentes; confirmar que só entra uma
  vez na implementação), indicadores agregados de moradia.

## 4.4 Indicadores descartados nesta rodada (18 de 65)

Registro histórico da revisão feita pelo usuário sobre a lista de
indicadores ainda não implementados — descartados = **não entram na
estrutura nova em nenhuma forma** (nem seção reservada/destacada). Mantido
aqui em vez de simplesmente removido do catálogo de trabalho, por §5 da
constitution (specs documentam histórico, não reescrevem decisões).

| Eixo original | Indicador | Motivo (`Status`/`Observação` da planilha) |
|---|---|---|
| Prioridade (sem secundário) | Taxa de Mortalidade Infantil (TMI) | "ok / já coberto por outro item" — redundante |
| Prioridade (sem secundário) | Taxa de Mortalidade na Infância (TMM5, <5 anos) | idem — redundante |
| Prioridade (sem secundário) | Razão de Mortalidade Materna (geral) | idem — já coberto por "gravidez" + "puerpério", ambos implementados |
| Prioridade (sem secundário) | Nascimentos pelo nº de consultas de pré-natal | "Posterior" |
| Prioridade (sem secundário) | SCFV 0 a 6 anos georreferenciado | Status vazio, sem justificativa registrada |
| Inclusão | Crianças com TEA, atendimento SMPD/SME/SMAS/SMS/SMTR | "Não há cruzamento de registros administrativos" |
| Inclusão | Crianças com neurodivergência, atendimento SMPD/SME/SMAS/SMS/SMTR | idem |
| Inclusão | Distribuição de famílias indígenas/quilombolas no CadÚnico | "Posterior" |
| Proteção | Crianças que sofrem acidentes em casa | dado só parcialmente coberto via violência interpessoal/autoprovocada por local |
| Proteção | Crianças com medida protetiva / % acompanhadas | "Não dispomos de dados" |
| Direito ao Brincar | Nº de praças com parquinho infantil | "Não dispomos de dados" |
| Direito ao Brincar | Nº de super parques com espaço para 1ª infância | idem |
| Direito ao Brincar | % crianças a X min de área de brincar / déficit de espaços | idem |
| Direito ao Brincar | % crianças com acesso regular a espaço de brincar | idem |
| Direito à cidade | Acesso a equipamento público cultural | "Não dispomos de dados" |
| Direito à cidade | Acesso a equipamento público de esporte e lazer | idem |
| Participação | Crianças escutadas / processos de participação infantil (SUBPAR) | "Não dispomos de dados" — único indicador do eixo, que fica sem nenhum conteúdo |
| Família e Cuidados | Crianças em atendimento SMPD/SME/SMAS/SMS/SMTR | "Não há cruzamento de registros administrativos" |

**Efeito colateral direto**: como o único indicador de cada um foi
descartado, os eixos **Direito ao Brincar**, **Direito à cidade** e
**Participação** somem da estrutura nesta rodada — não como "seção vazia
destacada" (regra E), mas removidos por completo. Se dado novo viabilizar
algum deles no futuro, é uma reintrodução de eixo, não um preenchimento de
placeholder (registrar como nova decisão nessa rodada futura, não reabrir
esta).

## 4.5 Exemplo detalhado — eixo "Alimentação" (método a repetir nos outros)

Serve de modelo para o crosswalk completo (feito em `tasks.md`, não aqui):

| Indicador do catálogo | Seção atual em `analise.py` | Visualizações | Tabelas | Mapas |
|---|---|---|---|---|
| Baixo peso ao nascer (nº) | DataSUS/Tabnet → Nascidos abaixo peso | (dado bruto na série, sem PNG próprio de contagem) | `nascidos_abaixo_peso_por_ano.csv` | `mapa_nascidos_baixo_peso_bairro_2025.png` |
| Baixo peso ao nascer (%) | idem | `nascidos_abaixo_peso_percentual_por_ano.png` | idem | `mapa_percentual_baixo_peso_bairro_2025.png` |
| Desnutrição SISVAN (nº e %) | SISVAN | `sisvan_desnutricao_percentual_por_ano.png` | `sisvan_desnutricao_por_ano.csv` | — |
| Sobrepeso/obesidade SISVAN (nº e %) | SISVAN | `sisvan_sobrepeso_percentual_por_ano.png`, `sisvan_obesidade_percentual_por_ano.png` | `sisvan_sobrepeso_por_ano.csv` | — |

O novo eixo "🍽️ Alimentação" herda essas duas seções inteiras (DataSUS
"Nascidos abaixo peso" + SISVAN completo), sem quebrar nenhuma visualização
em pedaços menores.

## 5. Documento vivo de estrutura (`specs/estrutura_eixos.md`)

### 5.1 Papel e formato

Arquivo **novo**, produzido durante a implementação desta spec (não nesta
rodada) — vive em `specs/estrutura_eixos.md` (raiz de `specs/`, ao lado de
`roadmap.md`/`tech-stack.md`, não dentro de `specs/ajuste_eixos/`), porque é
um documento vivo que sobrevive a esta rodada, não um artefato histórico de
uma spec só — **decisão a confirmar na revisão**, fácil de mudar de lugar.

Formato: um heading `##` por eixo, `###` por subseção, e uma lista com
formato fixo por item de conteúdo —

```markdown
## 🍽️ Alimentação

### Baixo peso ao nascer
- fonte: DataSUS/Tabnet (`limpeza_tabnet_bairros`)
- visualização: `nascidos_abaixo_peso_percentual_por_ano.png` (série temporal, %)
- mapa: `mapa_percentual_baixo_peso_bairro_2025.png`
- tabela: `nascidos_abaixo_peso_por_ano.csv`
```

Esse formato (heading + lista com chaves fixas `fonte`/`visualização`/
`mapa`/`tabela`) é deliberado: precisa ser confortável para o usuário editar
à mão (mover uma entrada de eixo, renomear uma seção, apagar uma linha) **e**
simples o bastante para um script parsear de forma confiável (heading →
seção, lista → itens, chave antes de `:` → campo) sem precisar de front
matter YAML nem de um formato mais rígido que atrapalhe a edição manual.

### 5.2 Fluxo de atualização

Pedido explícito do usuário nesta rodada: **"whenever i may want to change
the structure of the report, i want to be able to just change the .md file
and ask for the update."** Ou seja, depois que a reorganização inicial
existir:

1. Usuário edita `specs/estrutura_eixos.md` diretamente (reordena uma
   subseção, move uma visualização de eixo, renomeia um título).
2. Usuário pede a atualização (linguagem natural, ex. "atualiza o relatório
   com a nova estrutura").
3. Um skill (§8) relê o `.md`, valida que toda visualização/mapa/tabela
   referenciada ainda existe em `tabelas_finais/`/`visualizacoes/`/`mapas/`,
   e regenera `relatorio/index.html` + o PDF na nova ordem/agrupamento.
   Reordenar `analise.py`/`analise.ipynb` para bater com o `.md` é decisão
   em aberto — ver risco §9.1 (mover células tem custo/risco diferente de
   regenerar um HTML).
4. Texto já curado no DOCX (§6.4) que corresponda a uma visualização movida
   **acompanha a visualização**, não fica para trás — exige um identificador
   estável por visualização (não a posição/ordem), ver §8.

## 6. Impacto nos artefatos

### 6.1 `analise.py` / `analise.ipynb`

Pedido explícito do usuário: reorganizar também o notebook, não só os
relatórios de saída. **Risco real, sinalizado em §9.1**: `CLAUDE.md` hoje
documenta a ordem atual de `analise.py` como parte da arquitetura ("Analysis
sections in source order: Censo 2022, CadÚnico, DataSUS/Tabnet [...]") e
várias seções têm dependência de execução sequencial dentro do arquivo (ex.
"Juncao de tabelas por bairro", no fim do arquivo, lê resultados de nascidos
vivos/baixo peso/óbitos calculados em seções anteriores). Mover células
fisicamente por eixo pode quebrar essa ordem de dependência se não for feito
com cuidado. `CLAUDE.md` precisa ser atualizado para descrever a nova
organização quando isto for implementado (não apagar a descrição antiga sem
registrar a mudança, por §5 da constitution).

### 6.2 `relatorio/index.html`

Reorganizado para navbar/sumário e seções `h2` por eixo em vez de por fonte
de dado. Mecanismo de seletor de opções (pills) e texto por opção (v6.2)
já existentes são reaproveitados sem mudança de motor — só a fonte de
agrupamento passa a ser `estrutura_eixos.md` em vez da ordem fixa hoje
hardcoded em `build_html_report.py`.

### 6.3 PDF (`analise_primeira_infancia.pdf`)

Mesma estrutura por eixo, sem interatividade (pills viram, por exemplo,
subtítulos sequenciais em vez de seletor) — `build_notebook_report.py`
passa a ler a mesma fonte de estrutura que o HTML.

### 6.4 Novo: DOCX de curadoria de texto

Arquivo novo, ex. `relatorio/curadoria_textos.docx` — um documento Word
simples (heading por eixo/subseção, imagem de cada visualização/mapa
embutida, seguida do bloco de texto placeholder daquela visualização/opção)
gerado por script (`python-docx`, não está em `requirements.txt` ainda —
precisa ser adicionado). Objetivo: alguém edita o texto placeholder direto
no Word, sem tocar em código/HTML.

**Requisito de regeneração não-destrutiva** (implicação de arquitetura, não
levantada explicitamente pelo usuário mas necessária para o fluxo do §5.2
funcionar): se o DOCX for regenerado do zero a cada atualização de
estrutura, texto já escrito à mão se perde. O gerador precisa reconhecer
texto já editado (via um identificador estável por bloco, §8) e preservá-lo,
só adicionando placeholder para visualizações genuinamente novas — mesmo
princípio de "não sobrescrever o que foi curado" que os blocos de "Principais
achados" do HTML já registram como pendência editorial em
`relatorio/specs.md`.

## 7. Blocos de texto por visualização

- Todo item de conteúdo (gráfico, mapa ou tabela) que hoje aparece como uma
  subseção ganha um bloco de texto de análise — convenção já existente no
  HTML (150 palavras, `relatorio/specs.md` v6.5); **esta rodada ajusta a
  faixa para 100–200 palavras**, pedido explícito do usuário, e essa faixa
  passa a valer uniformemente em HTML, PDF e DOCX (substitui o número fixo
  "150" anterior — registrar como nova convenção, não apagar o registro
  antigo, por §5 da constitution).
- Cards com seletor de opções (pills): **cada opção mantém seu próprio
  bloco de texto**, que troca junto com a opção ativa — já é o
  comportamento do HTML (v6.2); o DOCX precisa do equivalente estático
  (todas as opções de um mesmo bloco aparecem em sequência no documento,
  cada uma com seu próprio texto rotulado, já que o Word não tem alternância
  interativa).
- Conteúdo ainda é lorem ipsum nesta fase — nenhuma leitura analítica real é
  fabricada a partir dos dados (mesmo cuidado já registrado em
  `relatorio/specs.md` para o bloco "Principais achados").

## 8. Skills necessários

Dois skills novos ou a estender, ambos como pendência de implementação
(fora do escopo de escrever só esta spec):

1. **Skill de reestruturação** — lê `specs/estrutura_eixos.md`, valida
   referências contra `tabelas_finais/`/`visualizacoes/`/`mapas/`, e
   regenera `relatorio/index.html` + PDF na nova ordem/agrupamento (e,
   dependendo da decisão do risco §9.1, também reordena `analise.py`).
   Provável extensão de `.claude/skills/export_pdf_report/` (já concentra
   os dois geradores de relatório) em vez de um skill totalmente novo.
2. **Skill de sincronização do DOCX** — lê o DOCX editado pelo usuário,
   identifica quais blocos de texto mudaram (por identificador estável, não
   por posição/texto literal), e escreve o texto final de volta nos lugares
   correspondentes do notebook (markdown), HTML e PDF. Precisa de um
   identificador único e estável por visualização/opção (proposta: reusar o
   nome de arquivo do PNG/CSV já existente, que já é único no projeto por
   convenção de `specs/tech-stack.md` — evita inventar um esquema de ID
   novo).

## 9. Riscos e decisões em aberto (confirmar antes do `plan.md`)

### 9.1 Reordenar `analise.py` fisicamente é o maior risco da rodada

Mover ~2500 linhas de células por eixo, em vez de manter a ordem técnica
atual (que respeita dependências de dado entre seções — ver §6.1), é uma
mudança de alto risco/alto custo de revisão. Duas alternativas a pesar no
`plan.md`, não decididas aqui:

- **(a) Reordenar de fato** as células de `analise.py` por eixo — atende o
  pedido literalmente, mas exige reexecutar o notebook do zero (regra da
  constitution) e revisar manualmente toda dependência entre seções antes
  de considerar validado.
- **(b) Manter a ordem técnica atual** (funções → Censo → CadÚnico → ... →
  junções finais, que é a ordem de construção do dado) e adicionar só uma
  marcação leve por seção (comentário/`# Eixo:` no markdown) que os
  geradores de relatório (HTML/PDF/DOCX) usam para **reordenar a
  apresentação**, sem mover nenhuma célula. Risco bem menor, mas não
  cumpre "reorganizar analise.py" tão literalmente quanto o pedido original.

### 9.2 Outras pendências

- Onde exatamente mora `specs/estrutura_eixos.md` (§5.1) — proposta na
  raiz de `specs/`, a confirmar.
- Nome/formato final do eixo "Prioridade (sem secundário)" (15
  indicadores ativos após o descarte do §4.4, todos já implementados) —
  bucket residual, não uma categoria de política real; nome de working
  title.
- ~~Eixo "Participação" tem 1 indicador só...~~ — **resolvido**: o usuário
  descartou esse indicador (§4.4), o eixo sai da estrutura por completo.
- Duplicidade aparente: "Territórios com risco a inundação" tem `Eixo`
  (fonte de dado) = Proteção mas `Eixo da Política Municipal Prioritário`
  = Moradia — é a mesma linha do catálogo com as duas colunas divergentes,
  não duas linhas duplicadas; ainda assim, checar na implementação que só
  entra uma vez (em Moradia, pela regra §3-A) e não é replicado por engano
  em Proteção.
- `python-docx` precisa ser adicionado a `requirements.txt`.

## 10. Fora de escopo desta rodada

- Implementação em si (reorganizar `analise.py`, regenerar HTML/PDF, criar o
  DOCX, construir os 2 skills) — fica para `plan.md`/`tasks.md`, após
  revisão desta spec.
- Importar dados novos para os eixos ativos ainda sem nenhuma implementação
  (Proteção, Moradia) — esta rodada só define onde essas seções vão morar e
  como ficam destacadas como pendentes; importar os dados em si é o item já
  registrado em `specs/roadmap.md` ("Educação e Violência", "Outros dados
  faltantes"). Direito ao Brincar, Direito à cidade e Participação não
  entram aqui — foram descartados por completo nesta rodada (§4.4), não
  ficam como pendência de importação.
- Escrever o texto final de qualquer bloco de análise — continua lorem
  ipsum até a curadoria manual via DOCX acontecer.
- O painel/dashboard mencionado na aba "Esqueleto dos painéis" do catálogo
  (filtro territorial, KPIs por eixo, etc.) — é uma ideia de produto
  diferente (um painel interativo tipo Streamlit, já listado em
  `specs/roadmap.md` "Other"), não o que este spec cobre.
