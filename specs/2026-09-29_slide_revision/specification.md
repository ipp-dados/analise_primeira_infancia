# SPECIFICATION — Revisão do deck (30 → 33 slides)

Rodada aberta em 2026-09-29 (branch `planning`; implementação em `spec/slide-revision`). Pedido original:
`revision_readme.md` (nesta pasta — deck de 32 slides; virou 33 pela decisão D3). A pasta chegou como
`2026-09-20_slide_revision/` e foi renomeada para a data de abertura da rodada (constituição §7).

## 1. Objetivo

Reorganizar e revisar `apresentacao/apresentacao.md` (fonte única do deck Marp, `specs/2026-09-28_apresentacao`)
seguindo as regras globais e a matriz do pedido, com as decisões D1-D8 abaixo. O deck continua sendo gerado por
`apresentacao/build/gera_apresentacao.py`; números por `{{n:...}}` (`build/numeros.py`), nunca digitados à mão.

## 2. Decisões (perguntas agrupadas ao usuário, 2026-09-29)

| # | Tema | Decisão |
|---|---|---|
| D1 | Escopo das regras globais | **Deck + rótulo de renda.** Tudo muda no deck; a troca de rótulos de renda do CadÚnico vale para o projeto todo (é correção factual: R$ 218 per capita é a linha de **pobreza** do Bolsa Família desde 2023; até 1/2 SM é **baixa renda**). "Até 72 meses" e a paleta sem azul no site/PDF vão para o ROADMAP. |
| D2 | Faixa etária | **"até 72 meses"** no lugar de "0 a 5 anos" (igual aos títulos do `estrutura_eixos.md`), com nota explícita "até 72 meses = 0 a 5 anos completos" onde a faixa aparece pela primeira vez e nos slides de número. |
| D3 | Slide original 28 ("Dois produtos") | **Mantido, antes do QR.** O deck passa a ter **33** slides (a matriz do pedido o omitia). |
| D4 | Bullet a remover no novo slide 04 (orig. 05) | **"Nem sempre chegam ao bairro"** (o texto citado no pedido não existe no deck; este é o que contrasta estatística oficial e registro administrativo). |
| D5 | Três caixas do novo slide 09 (orig. 12) | **Censo 2022 0-4 (bairro) · Ripsa 2025 até 72 meses = 393 mil (em destaque) · Censo 2022 0-5 (SIDRA 9606)**. Nenhuma caixa de 0-6 anos; o 469 mil (Ripsa 0-6) sai do deck. |
| D6 | Cor da terra nos mapas | **Rampa terracota** (creme → terracota), só do deck, distinta de `BuGn`/`RdPu`/`YlOrBr`/`Blues` e do `Purples` do site. Nenhum mapa do deck com terra azul. |
| D7 | Violência familiar | Slide 25: título genérico, **soma de todos os vínculos (mãe + pai + outros)** em destaque, vínculos separados como linhas secundárias. Novo slide 26: mapa por bairro 2025 da **soma mãe + pai + outros** (contagem → classes discretas, convenção do projeto). |
| D8 | "Mapa sem outliers" (slides 16 e 28) | **Teto de Tukey** (1,5 × IIQ), igual ao mapa de homicídios do deck e ao site: escala até o maior valor não extremo, extremos com a cor máxima e nomeados na nota do rodapé. |
| D9 | Violência familiar (revisão de D7, usuário, 2026-09-29) | **Sem soma de vínculos** ("não contar em dobro"): a mesma notificação pode citar mais de um provável autor (`2026-09-23_inclusao_dados_protecao` D6). Slide 25: título genérico, mãe, pai e outros com número e taxa próprios, gráfico por vínculo do relatório. Slide 26: mapas de mãe e de pai por bairro (2025) lado a lado, com a nota "os mapas não se somam". |
| D10 | Slide 09 e slide 30 (usuário, 2026-09-29, revisão de D5 e R6) | Slide 09: a 3ª caixa passa a ser a **Ripsa 2025 de 0 a 6 anos (469 mil)** -- a faixa da política municipal, dita "0 a 6 anos" na caixa -- no lugar do Censo 2022 0-5; o 469 mil volta só nessa caixa. Slide 30: Direito à Cidade e Participação são **dois eixos distintos**, e a pesquisa primária é a solução comum aos dois (caixas separadas ligadas a uma caixa única de solução). |

## 3. Regras globais no deck

- R1 "0 a 5 anos" → "até 72 meses" (D2); a nota "até 72 meses = 0 a 5 anos" aparece no mínimo nos slides 08, 09 e 12.
- R2 "extrema pobreza" → "pobreza"; "pobreza/baixa renda" → "baixa renda" (D1: também em `primeira_infancia/cadunico.py`,
  nas tabelas, no site, no PDF e no texto curado que diz "um dos critérios de extrema pobreza").
- R3 Nenhum mapa com terra azul (D6). Afeta ao menos `mapa_censo_0_4_absoluto` e `mapa_censo_0_4_percentual`
  (`Blues` do tema `censo`); conferir todos os `fig:mapa_*` do deck.
- R4 Zika: sempre "Zika de 2015-2016".
- R5 "primeira infância", nunca "infância" solta, em todo texto do deck.
- R6 População de referência: **393 mil** (Ripsa 2025, até 72 meses, `pop_0_5_ripsa_mil`). O 469 mil (0-6) sai.
- R7 Toda figura com valores extremos tratados leva nota explicando o tratamento (D8).
- R8 (achado do planejamento) Textos que dizem "bairros com menos de 20 famílias ficam em branco" estão desatualizados
  desde `2026-09-29_privacidade_cadunico` (agora somados em "Demais bairros da RA …"); corrigir no deck.

## 4. Estrutura nova (33 slides)

| Novo | Origem | Conteúdo / mudança |
|---|---|---|
| 01 | S01 | Subtítulo: "Um hub de dados para a Política Municipal Integrada da Primeira Infância do Rio de Janeiro" |
| 02 | S02 | Bullet 2: "A Política Municipal Integrada da Primeira Infância Carioca precisa de um retrato comum da cidade"; novo bullet 3: "Precisamos de um retrato das especificidades das diferentes partes da cidade" (o antigo bullet 3, "por eixo e por território", fica — confirmar na revisão visual se cabe) |
| 03 | S03 | Sem mudança |
| 04 | S05 | Sai "Nem sempre chegam ao bairro" (D4); "Zika de 2015-2016" |
| 05 | S04 | Título "Um centro para os dados da primeira infância"; caixa central sem o número de indicadores |
| — | S06 | **Removido** (tabela de pendentes; o conteúdo volta nos slides 30-31) |
| 06 | S07 | Cabeçalho "Governança de Dados" agrupando 3 caixas: Consistência (chave comum), Periodicidade (extração combinada), Privacidade (agregados; bairros pequenos somados — R8). Sai a 4ª caixa (Qualidade) |
| 07 | S08 | Seção Parte II, sem mudança |
| 08 | S11 | Número 393 mil "crianças de até 72 meses"; nota do 469/0-6 substituída por "até 72 meses = 0 a 5 anos" |
| 09 | S12 | Título com 393 mil; 3 caixas D5, a central (Ripsa) em destaque; nota de 72 meses |
| 10 | S09 | Título "O bairro é a unidade de análise principal"; mapa em terracota (D6) |
| 11 | S10 | Sem mudança |
| 12 | S13 | "até 72 meses" |
| 13 | S15 | Mapas em terracota (R3) |
| 14 | S16 | Gráfico e texto de 0 a 5 anos / até 72 meses (o PNG atual já é 0-5 — D9 de `2026-09-29_pendencias`; mudar título/texto) |
| 15 | S17 | Sem mudança |
| 16 | S18 | Mortalidade infantil com teto de Tukey + nota (D8) |
| 17 | S19 | "Onde está a primeira infância do Cadastro Único"; nota de privacidade atualizada (R8) |
| 18 | S20 | Seção Parte III, sem mudança |
| 19 | S14 | Kicker "Eixo Prioridade"; "pobreza" / "baixa renda" (R2; número `pct_cadunico_pobreza`) |
| 20 | S21 | Sem mudança |
| 21 | **novo** | "Causas evitáveis por faixa etária": `fig:obitos_causas_evitaveis_subgrupo_faixa_2025` (0-6, 7-27, 28-364 dias, 2025) |
| 22 | S22 | Sem mudança |
| 23 | S23 | Sem mudança |
| 24 | S24 | Nota sobre "família monoparental" reforçada (destaque visual, não mais `nota` discreta); "pobreza" (R2) |
| 25 | S25 | Título genérico; mãe, pai e outros separados, sem soma (D9, que revê D7) |
| 26 | **novo** | "Notificações por bairro em 2025, por vínculo": mapas de mãe e pai lado a lado (D9), com nota "notificação não é caso confirmado" |
| 27 | S26 | Sem mudança |
| 28 | S27 | Baixo peso com teto de Tukey + nota (D8); sai o 2º bloco (Inclusão e Moradia → slide 29); kicker só "Eixo Alimentação" |
| 29 | **novo** | "Eixos incompletos": Inclusão e Moradia (CadÚnico mapeado, em importação); Direito ao Brincar (dado incompleto; apoio das secretarias para integrar registros administrativos georreferenciados) |
| 30 | **novo** | "Eixos ausentes": Direito à Cidade e Participação (sem dado público; soluções colaborativas); pesquisa primária para cobrir o que o registro administrativo não alcança |
| 31 | S28 | "Dois produtos", sem mudança (D3) |
| 32 | S29 | QR, sem mudança |
| 33 | S30 | Contato `pesquisaeavaliacao.ipp@prefeitura.rio` (campo `contato` do cabeçalho) |

## 5. Fora do escopo

- "Até 72 meses" e paleta sem azul no site e no PDF (ROADMAP, D1).
- Números novos digitados à mão: todo número novo vira função em `numeros.py`.
- Mudar a regra de outlier do site (`remove_outliers_tukey`).

## 6. Critérios de aceite

Ver `validation.md`.
