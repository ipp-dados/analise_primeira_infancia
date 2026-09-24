# Tasks: specs/populacao-referencia

Um commit por bloco. Marcar `[x]` só depois da verificação correspondente em `validation.md`. As partes e
decisões são as de `specification.md`, e os blocos são os de `plan.md`. As tarefas detalhadas da Parte E
estão em `matriculas/tasks.md`.

## Bloco 0: Abertura e decisões

- [x] **T0.1**: Rodada aberta como `matriculas-censo-escolar` (D1-D9 da Parte E aprovadas, 2026-09-24).
- [x] **T0.2**: Escopo ampliado, branch e pasta renomeadas para `populacao-referencia`, `matriculas/` como subpasta (usuário, 2026-09-24).
- [x] **T0.3**: Levantamento: a Ripsa não tem bairro; inventário de denominadores; diagnóstico do item 7; itens do crosswalk sem arquivo.
- [x] **T0.4**: B1 = opção (a), ordem = população primeiro (usuário, 2026-09-24).
- [x] **T0.5**: A-D1 ✅, A-D2 ✅ (A3, A4), C-D1 ✅, D-D1 ✅ (item 7 reinterpretado: coluna % na gêmea de contagem, sem mapa novo), D-D2 ✅ (usuário, 2026-09-24). A4 viável com o `.env` atual.
- [x] **T0.6**: Ok do usuário para implementar ("ok, implement the spec/populacao-referencia", 2026-09-24).

## Bloco 1: Parte A, base

- [x] **T1.1**: `carrega_populacao_ripsa(...)`, com retry, parse, checagens e extrato `dados_locais/populacao/ripsa_populacao_rio.csv` (390 linhas: 364 + 26 totais; consulta de 2026-09-24).
- [x] **T1.2**: Helper `populacao_ripsa(...)` para faixa, sexo e anos.
- [x] **T1.3**: Nota geral A5 com a tabela Ripsa × Censo (início da seção Censo 2022).
- [x] **T1.4** *(achado)*: `.gitignore` do Bloco 0 tinha a regra `inep_microdados/` colada em `*env` (sem quebra de linha), anulando as duas; separadas.

## Bloco 2: Parte A, saídas

- [x] **T2.1**: A2: `populacao_ripsa_0_a_6_por_ano.csv` (26 linhas) e dois PNG: contagem 0-6 e participação no total (`populacao_ripsa_0_a_6_percentual_por_ano.png`, A-D1 pede os dois).
- [x] **T2.2**: A3: `violencia_familiar_taxa_municipio_ano.csv/.png` (com a marca de 2017, via `serie_temporal_multipla_marcos`).
- [x] **T2.3**: A4: `cadunico_razao_populacao_0_a_5_2026.csv`, partição `2026-06-12` (coluna `data_particao`).

## Bloco 3: Parte B

- [x] **T3.1**: Fontes e títulos sub-municipais explícitos: legendas de M8-M13 ("Censo 2022"), eixo de G8, título/legenda/fonte do mapa % CadÚnico/Censo (só notebook). Os schemas CSV não mudam (sem coluna nova, para não mexer nos leitores). `fonte_sinan_censo` já citava o Censo.
- [x] **T3.2**: Nota D9 acrescida dos pontos B3 (anos diferentes puxam a taxa para baixo; subcontagem puxa para cima; comparar territórios entre si, não com A3). Nota do topo da seção Proteção aponta A3.
- [x] **T3.3**: HTML: legendas dos mapas de taxa, título do top 10 e nota metodológica. PDF (`build_notebook_report.py`): coluna da tabela CAP, títulos das galerias e nota.

## Bloco 4: Parte E

- [x] **T4.1**: `matriculas/tasks.md` Blocos 1-3, com a população vinda da Parte A. Os leitores dos relatórios (ainda com `matriculas_0_a_6`) mudam no Bloco 6.

## Bloco 5: Parte D

- [x] **T5.1**: P-D1: 6.336 de 65.507 nascidos vivos de 2025 (9,7%) sem bairro ("EM BRANCO"); impresso pela célula do mapa.
- [x] **T5.2**: D1: coluna `percentual_do_municipio` na gêmea de nascidos vivos 2025 (bairros somam 90,3%). Ligação no crosswalk: Bloco 6.
- [x] **T5.3**: D3: `sidra_frequencia_escola_0_5_total_2022.csv/.png` (total por idade, 233.509). Ligações de D2/D3 e o `pendente` de mortalidade por sexo: Bloco 6.
- [x] **T5.4**: D4: `itens_sem_arquivo`/`avisa_itens_sem_arquivo` em `gera_estrutura_eixos.py`, chamado pelo validador e pelos dois geradores (HTML e PDF). Antes do Bloco 6 lista exatamente os 4 itens do diagnóstico.

## Bloco 6: Crosswalk e relatórios

- [x] **T6.1**: `estrutura_eixos.md` atualizado (A2, A3, A4, D1-D3, E; mortalidade por sexo `pendente`). 51 subseções, 8 pendentes, 0 itens sem arquivo e sem status.
- [x] **T6.2**: Três scripts atualizados. HTML: `refLines` opcional no `lineChart` (D8) e `col_extra` opcional no `mapa_svg` (tooltip com % do município, D1). `regen_missing_pngs.py`: matrículas 0-5, só se o PNG faltar (o snapshot não tem rodapé de fonte).
- [x] **T6.3**: HTML (option cards 40 → 44; JS validado com `node --check`), PDF (127 → 140 páginas) e DOCX (160 → 171 headings) regenerados. Passo 1 (`regen_missing_pngs.py`) não rodado: todas as referências existem e ele só sobrescreveria PNGs do notebook com o estilo antigo. **Achado:** o texto curado do item "Crianças até 6 anos (número)" (sobre o SIDRA 9606) foi para "Textos órfãos" do DOCX, porque o item passou a ter arquivos; está preservado lá, para o usuário decidir onde fica.

## Bloco 7: Parte C

- [x] **T7.1**: `auditoria_faixas.md` gerado (15 fontes; listas A, B e C; achado do total dobrado na série dos Censos, §2).
- [ ] **T7.2**: Lista de rótulos, renomeações e notas de curadoria afetadas mostrada ao usuário (2026-09-24). **Parado aqui**, aguardando C-D2, C-D3, C-D4.
- [ ] **T7.3**: Rótulos corrigidos e renomeações aprovadas executadas (leitores incluídos).
- [ ] **T7.4**: Relatórios regenerados de novo.

## Bloco 8: Validação e fechamento

- [ ] **T8.1**: Notebook do zero no `analises_env`; `validation.md` completo.
- [ ] **T8.2**: Roadmap, README, constitution e CLAUDE.md atualizados.
- [ ] **T8.3**: Revisão do usuário e merge em `staging_main`.
