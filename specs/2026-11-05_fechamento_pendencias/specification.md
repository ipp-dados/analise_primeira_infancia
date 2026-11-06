# SPECIFICATION — Fechamento de pendências antes da versão final do site (rodada de 2026-11-05)

Status: **em planejamento (2026-11-05)**, branch `spec/fechamento_pendencias`. O *como* está em `plan.md`, as tarefas
em `tasks.md`, os critérios de aceite em `validation.md`. Só se implementa depois do OK do usuário.

## 1. Contexto

O usuário pediu a versão final do site (`website_release.md`, na raiz; desde 2026-11-06 em `specs/2026-11-05_versao_final_site/initial_prompt.md`). Primeiro passo do
pedido: "conferir as branches; se houver trabalho em andamento, terminar antes". Branches: nenhuma além de
`staging_main`, `main` (ancestral de `staging_main`) e `demo`; sem stash. O `ROADMAP.md`, porém, tinha itens abertos
das rodadas `2026-10-06_cadunico_inclusao_moradia`, `2026-10-06_deck_alimentacao_brincar` e `2026-10-08_deck_moradia`.
Esta rodada fecha esses itens. A rodada da versão final vem **depois**, numa spec própria.

## 2. Decisões do usuário (2026-11-05)

| # | Decisão | Origem |
| :-- | :-- | :-- |
| D1 | **Corrigir o % do SISVAN** em `analise.py`: recalcular todos os % a partir de contagem ÷ total | ROADMAP 000b.3 |
| D2 | **Mapas de número de crianças por bairro no eixo Moradia** (inadequação e adensamento), ao lado dos mapas de %; site e PDF | ROADMAP 000c.3 |
| D3 | **Tabelas do CadÚnico (Inclusão e Moradia) no PDF**: entradas em `relatorio/latex/build/tabelas.py` e fonte em `fontes.bib` | ROADMAP 000.2 |
| D4 | **CadÚnico: fica a extração atual do projeto (silver de jul/2026)**. A diferença com o dado pontual de ago/2026 (25.995 × 7.919 crianças com deficiência, A2 da rodada de 10-06) deixa de bloquear | resposta do usuário |
| D5 | **"IPS" → "ISP"** nas citações da violência territorial (homicídios, homicídios por ação policial, homicídios de jovens negros, por RA, 2024). O indicador continua publicado | resposta do usuário |
| D6 | **Nenhum mapa com azul, só a água**: tema `censo` `Blues` → `Purples` (como o site já usa) e tema `natalidade` `BuGn` → `Greens`, no `analise.py`/PDF **e** no site | resposta do usuário |
| D7 | **Decks deixam de ser mantidos**: `apresentacao/` fica congelado como está (sem regerar, sem apagar). Saem do ROADMAP os itens só de deck (000.3, 000b.1-2, 000c.1-2) | resposta do usuário |
| D8 | **Textos das chaves novas do CadÚnico antes da versão final**: proposta de texto curado para cada figura/tabela de Inclusão e Moradia ainda em lorem (e para os 2 mapas novos de D2), aprovada pelo usuário antes de entrar em `textos_curados.json` | resposta do usuário |
| D9 | **Organização fase 1c fica para depois da versão final** (ROADMAP §3.1 continua na fila) | resposta do usuário |

## 3. Requisitos

**R1 — SISVAN (D1).** As colunas `*_percentual` de `dados_locais/tratados/desnutrição.csv` e `sobrepeso.csv` têm
erro na origem (ex.: obesidade 2009 = `0.07`, sem `%`, contra 7,0% pelas contagens; desnutrição 2023 = 3,74% contra
5,7%). Os % publicados passam a ser **`<categoria>_bruto / total × 100`**, numa função do pacote
(`primeira_infancia/limpeza.py`), nunca lendo a coluna `_percentual` da origem. Mesmos nomes de arquivo e de coluna
de saída (`tabelas_finais/sisvan_*`, `visualizacoes/sisvan_*`), para não quebrar o site, o PDF e o crosswalk. Os
textos curados com números do SISVAN são conferidos e, se mudarem, reescritos com a mesma redação (status
"atualizado" em `controle_revisao.json`).

**R2 — Mapas de número em Moradia (D2).** Dois mapas novos em `analise.py`, via `mapa_coropletico_bairros`, com
**classes discretas** (contagem, convenção do projeto) e o tema `cadunico`:
`mapa_cadunico_inadequacao_n_bairro_2026` e `mapa_cadunico_adensamento_n_bairro_2026`. Leem as tabelas de mapa que
já existem (`tabela_mapa_cadunico_inadequacao_bairro_2026.csv`, `..._adensamento_...`), já protegidas
(`agrega_bairros_pequenos`). Bairros somados ao grupo "Demais bairros da RA X" ficam **sem cor** com essa nota na fonte
(como no deck). Classes de partida iguais às do deck (`[40, 75, 150, 300]` e `[150, 400, 800, 1600]`), conferidas com
os dados. Variante A4 gerada junto (`GERA_VARIANTE_A4`). Entram em `specs/estrutura_eixos.md` **antes** do mapa de %
de cada indicador (número antes do percentual, como em Inclusão), no site (`mapa_svg`) e no PDF.

**R3 — Tabelas do CadÚnico no PDF (D3).** Toda tabela de Inclusão e Moradia listada no crosswalk ganha entrada em
`tabelas.py` (título, colunas, renomeação, no padrão das de 10-06) e a fonte "CadÚnico, extração CTPE, jul/2026" ganha
entrada em `fontes.bib`. O PDF é **regerado e conferido**, mas **não publicado** (a publicação é da rodada da versão
final, com Release).

**R4 — CadÚnico jul/2026 (D4).** Nenhum dado novo é extraído. O ROADMAP registra A2 como "decidido: silver de
jul/2026". Nenhum item `dado_pontual` volta a ser publicado.

**R5 — ISP (D5).** Todas as citações e rótulos "IPS"/"Índice de Progresso Social" da violência territorial passam a
citar o ISP: `analise.py` (`fonte_ips`, legenda `Taxa (IPS)`, markdown), `build_site.py` (`FONTE_IPS`, título h3,
nota da RA XXI), `tabelas.py`, `fontes.bib`, `specs/estrutura_eixos.md`, `textos_curados.json`,
`relatorio/inventario_fontes.*`, `docs/especificacao_projeto.md`, comentários e docstrings de
`primeira_infancia/protecao.py`. Redação proposta: **"Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por
Região Administrativa (todas as idades)"**. Identificadores de código (`fonte_ips`, `FONTE_IPS`) mudam para `*_isp`.
**Ponto aberto P1:** a planilha (`dados_locais/protecao/violencia_territorial.xlsx`) se intitula "Indicadores do Índice
de Progresso Social (IPS) … 2024" e não cita o ISP; a redação acima supõe que o ISP é a fonte primária dos homicídios
do IPS Rio. O usuário confirma a redação antes da implementação.

**R6 — Cores dos mapas (D6).** `_CORES_TEMA_MAPA` (`primeira_infancia/estilo.py`): `censo` → `Purples`,
`natalidade` → `Greens`. `_CMAP_TEMA` (`website/build/build_site.py`): `natalidade` → `Greens` (`censo` já é
`Purples`). Nenhum outro mapa (site, PNG, A4) usa matiz azul em terra; o azul fica só no fundo (mar). Gráficos de
linha/barra **não** mudam (a paleta categórica não é de mapa). Os comentários que justificam a cor antiga são
atualizados, e o SKILL `generate_map` e o `CLAUDE.md` registram a regra.

**R7 — Decks (D7).** `apresentacao/` não é tocado. `ROADMAP.md`, `CLAUDE.md` e `docs/especificacao_projeto.md`
registram que os decks não são mais mantidos (congelados em 2026-11-05).

**R8 — Textos (D8).** Para cada figura, mapa e tabela de Inclusão e Moradia sem texto curado (lorem no site de
`staging_main`), e para os 2 mapas de R2: uma proposta de texto no estilo dos textos curados vizinhos (mesmo
tamanho, mesma forma de citar números, faixa "até 72 meses"/"0 a 5 anos" conforme a regra D9/D10 das rodadas
anteriores), **com cada número conferido na tabela de origem** em `tabelas_finais/`. As propostas vão ao usuário
agrupadas (uma tabela: chave, texto proposto, números e onde foram conferidos); só entram em `textos_curados.json`
depois do OK. Depois disso, nenhum lorem nos eixos Inclusão e Moradia.

**R9 — ROADMAP.** Cabeçalho com a data atual; seções 000/000b/000c/00 fechadas ou movidas (o que depende da equipe
fica em "Aguardando equipe/usuário"); fase 1c continua em §3; linha nova em "Concluído".

## 4. Fora do escopo

- A versão final do site (banner, introdução, mapa de referência, rodapé, faixa beta, testes, `main`) — próxima rodada.
- Publicar o PDF (Release) e fazer deploy.
- Fase 1c da organização (D9).
- Pendências que dependem da equipe: pedido ao GitHub Support, reclonar, apagar o backup (rodada de 10-26).
- Novo DOCX de curadoria `relatorio/curadoria_textos_05_11_26.docx`: será lido na rodada da versão final. (Ele ainda
  traz "acima de 3 por dormitório" e os 🚧 de Inclusão/Moradia, vindos de uma exportação anterior.)

## 5. Riscos

- **CadÚnico precisa do banco**: R2 só lê tabelas que já estão em `tabelas_finais/`, sem consultar o banco. Se uma
  tabela de mapa não estiver no disco, a seção CadÚnico roda no `analises_env` com o `.env`.
- **Novos % do SISVAN mudam textos e talvez o eixo** dos gráficos (zero na base, P1); conferir visualmente.
- **Trocar cores muda todas as PNG** de Censo e natalidade; o desktop do site muda **só** nas cores dos mapas (a regra
  "pixel-idêntico" do mobile vale para layout, não para esta troca pedida).
