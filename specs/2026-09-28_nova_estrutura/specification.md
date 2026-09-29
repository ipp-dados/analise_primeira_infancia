# SPEC — Nova estrutura do site e do PDF (Introdução com panorama + 7 eixos)

Rodada aberta em 2026-09-28 no branch `planning`; implementação em `spec/nova_estrutura`.
Insumos da equipe (nesta pasta):
- `Estrutura relatório e site - eixos atualizados e dados.csv` — indicador → eixo prioritário → eixo
  transversal → cartões do site ("Dado/Visualização", pelos títulos h3/h5 atuais do site);
- `Observações curadoria_textos.txt` — 5 observações de texto.

## 1. Objetivo

Reordenar a apresentação de visualizações e textos, no **site** (`website/`) e no **PDF**
(`relatorio/latex/`), segundo a planilha da equipe. A ordem de construção do `analise.py` não muda
(CLAUDE.md: ordem técnica ≠ ordem de apresentação). A fonte da nova ordem é `specs/estrutura_eixos.md`,
**já atualizado nesta rodada** (2026-09-28, no branch `planning`).

**Regra do usuário (2026-09-28): acrescentar o que falta, nunca remover o que sobra.** Se o site ou o PDF
têm mais dados, cartões, abas ou tabelas do que a planilha lista, eles ficam; a planilha só reordena e
acrescenta. Célula em branco ou "?" na planilha quer dizer "manter o que existe", não "apagar". Remoção só
por entrada nova em `specs/exclusoes.md`, pedida pelo usuário.

## 2. Decisões do usuário (2026-09-28)

| # | Pergunta | Decisão |
|---|---|---|
| D1 | "direito a brincar" como eixo prioritário de Violência territorial | **Criar o 7º eixo, "Direito ao Brincar"** (🧸, depois de Proteção). Grafia "ao Brincar" (a planilha diz "a brincar") confirmada pelo usuário (2026-09-28) |
| D2 | Coluna "Eixo Transversal" | **Só registrar** em `estrutura_eixos.md` (`- eixo transversal: <eixo>`); sem efeito visível no site, PDF ou DOCX nesta rodada |
| D3 | Evitáveis por raça/cor ("?" na planilha, nota de 1996 no .txt) | **Continua pendente**. A nota de 1996 fica registrada no item para quando ele voltar |
| D4 | Regra de conteúdo | Acrescentar o que falta, nunca remover o que sobra (§1) |

## 3. Estrutura-alvo

Ordem publicada (a mesma no site, no PDF e no DOCX de curadoria):

| Ordem | Seção | Site | PDF | Indicadores (itens de `estrutura_eixos.md`) |
|---|---|---|---|---|
| 0 | **Introdução** (panorama, não é eixo) | aba *Visão geral* | cap. *Introdução* | crianças 0-4 (nº e %), 0-6 Ripsa, 0-6 por sexo e por raça/cor, nascidos vivos (nº e %) |
| 1 | Prioridade | aba | cap. | mortalidade neonatal, materna, por raça/cor, evitáveis (faixas, tipo, raça/cor e sexo pendentes), primeira infância; bloco CadÚnico (razão sobre a população, crianças, famílias, renda, sexo, raça/cor) |
| 2 | Inclusão | aba | cap. | só os 3 pendentes de deficiência (CadÚnico) |
| 3 | Família e Cuidados | aba | cap. | educação (frequência geral, por raça/cor, por sexo, PNAD, matrículas, taxa de atendimento), vacinação, CadÚnico por renda e arranjo |
| 4 | Proteção | aba | cap. | violência familiar (vínculo + taxas), "outros", bairros com mais notificações, CAP, autoprovocada, taxa geral (pendente), tipificação (pendente) |
| 5 | **Direito ao Brincar** (novo) | aba | cap. | violência territorial (IPS por RA) |
| 6 | Alimentação | aba | cap. | baixo peso, SISVAN |
| 7 | Moradia | aba | cap. | 3 pendentes |

Resultado da conferência automática (parser + `valida_estrutura`): 51 itens antes e 51 depois; **nenhum
arquivo de visualização, mapa ou tabela saiu**, nenhum entrou; todas as referências existem.

### 3.1 Convenção da Introdução em `estrutura_eixos.md`

O primeiro `##` é `🧭 Introdução`. Os geradores reconhecem o panorama por `chave_eixo(eixo) == "introducao"`
e o tratam à parte:
- não entra na numeração "Eixo N de M" (os eixos continuam de 1 a 7);
- não tem "Principais achados", texto de abertura do eixo nem síntese (`blocos_relatorio` pula o item). O texto
  é a `introducao` curada que já existe, e cada figura tem o seu próprio texto;
- o parser não muda (`##` continua abrindo um "eixo"); a exceção fica nos consumidores, por uma função única
  `eh_panorama(eixo)` em `gera_estrutura_eixos.py`, usada por todos.

## 4. Conferência da planilha e sugestões

Cada ponto em que a atualização se afastou da planilha, ou a completou. Todos já estão aplicados em
`estrutura_eixos.md`, com nota no item; para desfazer um, basta editar o item.

| # | Planilha | Aplicado | Por quê |
|---|---|---|---|
| S1 | Nascidos vivos (nº) aponta só para o cartão de mapas por bairro | série anual `nascidos_vivos_por_ano` **e** mapa vão para a Introdução; os cartões de mortalidade ficam só com mortalidade | o cartão atual "Nascidos vivos e mortalidade infantil por raça/cor" mistura os dois temas; separar é o que a planilha pede, sem perder a série (§1) |
| S2 | Ordem do bloco CadÚnico em Prioridade: razão → famílias por sexo → raça/cor → famílias (nº) → renda → … → crianças (nº) | razão → **crianças (nº)** → famílias (nº) → renda → sexo → raça/cor | a contagem-base (com os mapas por bairro) vem antes dos recortes |
| S3 | "Taxa de mortalidade na primeira infância (<1, 1-4, 0-5)" aponta para o cartão de evitáveis | mantidas as taxas infantil e pós-neonatal (e mapas) no item; a taxa de evitáveis < 5 segue no item de evitáveis | nada sai (§1). **Lacuna**: a taxa de mortalidade de 1 a 4 anos (todas as causas) não existe; fica no ROADMAP |
| S4 | Família e Cuidados: raça/cor → sexo → PNAD → **vacinação** → geral → matrículas → taxa | **geral** → raça/cor → sexo → PNAD → matrículas → taxa → vacinação → CadÚnico arranjo | a vacinação cortava o bloco de educação; o total vem antes dos recortes |
| S5 | Baixo peso (nº) lista também "Estado nutricional (SISVAN)" | SISVAN continua nos seus 4 itens (desnutrição/sobrepeso), logo abaixo do baixo peso | os itens do SISVAN estavam em branco na planilha; o cartão é deles. A ordem no site já é essa |
| S6 | "Taxa de notificações de violência" (Proteção; transversal Direito ao Brincar) sem visualização | vira item **pendente**: "Taxa de notificações de violência (todas as naturezas)". As taxas de violência FAMILIAR foram para "Violência familiar … por vínculo" (taxa municipal + mapas por RA) e para "bairros com mais notificações" (dez maiores taxas + mapas de contagem), como na planilha | nada sai; o pendente registra a lacuna de violência não familiar |
| S7 | "Violência familiar — composição de 'outros'" sem visualização | mantido o gráfico `violencia_familiar_outros_serie` | §1 |
| S8 | Nascidos vivos (%) com "?" | segue sem mapa próprio: percentual no tooltip do mapa e na tabela (D1 revisada de `populacao-referencia`) | já decidido antes |
| S9 | Cartões do site que a planilha não cita: "Bairros com mais crianças de 0 a 4 anos" (tabela top 10), "Evolução da população de 0 a 4 anos, por sexo (Censos 2000-2022)", sub-blocos h4/h5 de evitáveis | ficam, na Introdução (os dois primeiros) e em Prioridade (evitáveis) | §1 |

Consequência a registrar: a aba **Inclusão** fica só com 3 pendentes. É o mesmo caso de Moradia e segue o
padrão existente (cartões "Indicador catalogado, ainda não disponível").

## 5. Mudanças por produto

### 5.1 Site (`website/build/build_site.py`, conteúdo montado em código)

O site não lê a ordem de `estrutura_eixos.md`: os `h2`/`h3` estão em código. É preciso **mover blocos de
código**, sem reescrevê-los, e manter todos os `antigo=` (links antigos) e todas as sementes (`seed`) de texto.

- **Visão geral** passa a ter: Introdução (texto) → **"Panorama da primeira infância carioca"** (cartões
  movidos de Prioridade e de Inclusão, na ordem da §3) → grade de cartões dos eixos (agora 7). O sumário lateral
  da Visão geral lista Introdução, os h3 do panorama e "Eixos".
  - Implementação: hoje o painel da Visão geral é montado no ASSEMBLE, fora do fluxo `h2`/`parts`. Opção
    escolhida: emitir o panorama com um `h2` especial (`h2_panorama()`), capturado no ASSEMBLE e injetado
    no painel `visao-geral`. O `h2` especial não entra em `section_starts`, então não vira aba nem é contado
    como eixo.
  - Cartões movidos para o panorama: "Bairros com mais crianças de 0 a 4 anos", "Crianças de 0 a 4 anos por
    bairro e região", "Evolução da população de 0 a 4 anos, por sexo", "População de 0 a 6 anos por ano
    (Ripsa)", "Crianças de 0 a 6 anos por idade, raça/cor e sexo (Censo 2022)" e um h3 novo **"Nascidos vivos"**
    (série + mapa, tirados dos dois cartões de mortalidade).
- **Prioridade**: neonatal/idade ao óbito → óbitos maternos → "Mortalidade infantil por raça/cor" (renomeado,
  sem a pill "Nascidos vivos") → "Mortalidade infantil por bairro" (a alternância Taxa/Óbitos que ficava no
  cartão "Nascidos vivos e mortalidade infantil por bairro"; mantém `antigo='mapas-2'`) → evitáveis (inteiro,
  pendente por sexo incluído) → bloco CadÚnico (razão → "Crianças e famílias no CadÚnico, por renda e idade"
  com o h4 por bairro → por sexo → por raça/cor).
- **Inclusão**: só os 3 `emite_bloco_pendente` de deficiência.
- **Família e Cuidados**: "Crianças de 0 a 5 anos que frequentam escola/creche (Censo 2022)" → "Taxa de
  frequência … por idade, raça/cor e sexo (Censo 2022)" (vem de Inclusão) → PNAD → matrículas → taxa bruta
  de atendimento → vacinação → "Famílias no CadÚnico … por renda e arranjo familiar" (vem de Inclusão).
- **Proteção**: o h3 "Violência familiar (0 a 5 anos, Sinan)" recebe as h5 de taxa (município e RA) do h3
  "Taxa de notificações…"; h5 "Dez bairros com mais notificações" recebe as dez maiores taxas; "Notificações
  por bairro, em mapa" junto; CAP; autoprovocada; pendente novo "Taxa de notificações de violência (todas as
  naturezas)"; pendente de tipificação. O h3 "Taxa de notificações de violência familiar" deixa de existir como
  h3; o id antigo (`taxa-de-notificações-de-violência-por-1000-crianças` e o slug atual) continua abrindo o
  lugar novo (`antigo=` no h5 de destino, ou um alias).
- **Proteção — como ficou na implementação (2026-09-28)**: em vez de dissolver o h3 "Taxa de notificações…" (o que
  tiraria uma entrada do sumário lateral), a ordem ficou: h3 "Violência familiar (0 a 5 anos, Sinan)" → h3 "Taxa de
  notificações de violência familiar" (município + RA) → **h3 novo "Violência familiar por bairro e CAP (2025)"** (dez
  bairros em número, dez maiores taxas, mapa por bairro, CAP) → autoprovocada → pendentes. Mesmo agrupamento da
  planilha, nenhum id perdido.
- **Direito ao Brincar** (aba nova): h2 `🧸 Direito ao Brincar`, com o h3 de violência territorial (código
  movido de Proteção, com a nota metodológica). `_EIXO_META` ganha `("direito", "Direito ao Brincar", <ícone>)`
  (ícone Lucide a escolher, ex. `toy-brick`/`blocks`, acrescentado ao sprite de ícones), e o mesmo em
  `EIXO_META` do `gera_latex.py`.
- `_FONTES_SECAO`, `achados_<eixo>`, `introducao_<eixo>`, `sintese_<eixo>`: a chave nova é `direito_ao_brincar`
  (lorem até haver texto curado, como nos demais).
- **Barra de abas**: passa de 7 para 8 abas. No desktop (≥ 1100 px), conferir se cabe sem rolagem; se não
  couber, encurtar rótulos ("Família e Cuidados" → "Família", "Direito ao Brincar" → "Brincar") em vez de mudar
  o CSS. É mudança intencional de layout: a regra de desktop pixel-idêntico de `website_mobile` vale para os
  demais elementos, e a comparação por captura de tela deve mostrar diferença só na barra de abas, na Visão geral
  e na ordem dos painéis.

### 5.2 PDF (`relatorio/latex/build/gera_latex.py`, lê `estrutura_eixos.md`)

- `capitulos()`: o eixo panorama vira o **corpo do capítulo Introdução**: texto `introducao` → `como_ler` →
  `\section{Panorama da primeira infância carioca}` com cada indicador como `\subsection` (figuras + textos,
  mesmo código dos eixos, extraído para uma função `secoes_indicadores()`) → `\section{Os eixos da política}`
  (lista dos 7 eixos, sem o panorama).
- Numeração dos eixos e `\eixo{i}{N}` sem o panorama (N = 7).
- Apêndice: "Tabelas da Introdução" antes das tabelas dos eixos.
- `EIXO_META`: entrada para `direito` (ícone gerado por `gera_icones.py`, o mesmo do site).
- `sem_figura`, `EM_LOREM` e o relatório de build continuam funcionando (conferir).

### 5.3 DOCX de curadoria e sincronização (`relatorio/curadoria/`)

- `blocos_relatorio()`: sem achados/introdução/síntese para o panorama; blocos novos para `direito_ao_brincar`.
- `gera_docx_curadoria.py`: o DOCX segue a ordem nova (panorama primeiro, sob "Introdução"); conferir que
  bookmarks e `controle_revisao.json` não dependem da posição do eixo (a chave é pelo nome do arquivo e por
  `chave_eixo`, então não deveria haver impacto).
- `sincroniza_docx.py`, `incorpora_update_docx.py`, `valida_textos_publicados.py`, `inventario_fontes.py`,
  `website/build/confere_textos.py`: rodar e conferir (todos usam `parse_estrutura_eixos`). O campo novo
  `eixo transversal` é ignorado por todos (nenhum lê chaves desconhecidas).

## 6. Observações de texto (`Observações curadoria_textos.txt`): situação

| # | Observação | Situação em 2026-09-28 | Ação na rodada |
|---|---|---|---|
| O1 | Óbitos evitáveis por CAP, menores de 5 anos (série): "agrega os recortes de menores de 1 ano e de 1 a 4 anos" | **Texto: corrigido** ("reúne os óbitos de menores de 1 ano e de 1 a 4 anos"). **Título e legenda da figura: não** ("Óbitos por causas evitáveis, menores de 5 anos, por CAP") | nota na legenda (O5) |
| O2 | Percentual de evitáveis por CAP, menores de 5 anos (série) | **Texto: corrigido** ("reúne as faixas…"). Legenda: não | nota na legenda |
| O3 | Mapa de óbitos evitáveis, menores de 5 anos, CAP 2025 | **Texto: parcial**: fala dos recortes, mas não diz que o menor de 5 agrega os dois. Legenda: não | nota na legenda; sinalizar à curadoria (o texto curado não é reescrito por nós, constituição §5) |
| O4 | Mapa de percentual de evitáveis, menores de 5 anos, CAP 2025 | **Texto: parcial** ("pode ser relacionado aos recortes…"). Legenda: não | idem |
| O5 | Evitáveis por raça/cor: 1996 com distorção por baixa completude | **Não se aplica agora**: o item está pendente (D3); o texto curado `obitos_causas_evitaveis_raca_ano` não cita 1996, e o de `…_sem_nao_informado` começa em 1997 | nota registrada no item de `estrutura_eixos.md` |

Onde fica a nota "agrega os recortes de menores de 1 ano e de 1 a 4 anos":
- `analise.py`: acrescentar `Nota: agrega os recortes de menores de 1 ano e de 1 a 4 anos` ao `fonte_dados` das 4
  chamadas (séries por CAP e mapas por CAP de menores de 5). O `gera_latex.py` já extrai `Nota:` da fonte do
  manifesto A4 para a legenda. Exige rodar as células de causas evitáveis por CAP (DataSUS local, sem banco).
- Site: o mesmo texto no `fonte=`/nota das pills "Menores de 5 anos" (h5 "Por CAP e faixa etária" e "Óbitos
  evitáveis por CAP, em mapa").

## 7. Fora do escopo

- Efeito visual do eixo transversal (D2).
- Extração nova de dados (evitáveis por raça/cor corrigido, por sexo, deficiência, violência geral, taxa de
  1 a 4 anos): segue no ROADMAP.
- Mudar a ordem das seções de `analise.py`.
- A apresentação (`specs/2026-09-28_apresentacao`), que parte desta estrutura quando ela estiver implementada.
