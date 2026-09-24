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

- [ ] **T3.1**: Fontes e títulos sub-municipais explícitos ("população de 0 a 4 anos, Censo 2022").
- [ ] **T3.2**: Nota D9 acrescida dos pontos B3.
- [ ] **T3.3**: Rótulos de fonte nos cards de violência do HTML.

## Bloco 4: Parte E

- [ ] **T4.1**: `matriculas/tasks.md` Blocos 1-3, com a população vinda da Parte A.

## Bloco 5: Parte D

- [ ] **T5.1**: P-D1: nascidos vivos "EM BRANCO" em 2025 registrados.
- [ ] **T5.2**: D1: coluna `percentual_do_municipio` na gêmea de nascidos vivos 2025; item "(percentual)" do crosswalk ligado ao mapa e à tabela de contagem.
- [ ] **T5.3**: D2 e D3 ligados; mortalidade evitável por sexo marcada `pendente`.
- [ ] **T5.4**: D4: aviso no console dos geradores para itens sem arquivo.

## Bloco 6: Crosswalk e relatórios

- [ ] **T6.1**: `estrutura_eixos.md` atualizado (A2, A3, A4, D1-D3, E).
- [ ] **T6.2**: Três scripts de relatório atualizados, incluindo o Bloco 4 de `matriculas/plan.md`.
- [ ] **T6.3**: HTML, PDF e DOCX regenerados e comparados com o baseline.

## Bloco 7: Parte C

- [ ] **T7.1**: `auditoria_faixas.md` gerado.
- [ ] **T7.2**: Lista de rótulos, renomeações e notas de curadoria afetadas mostrada ao usuário. **Parar.**
- [ ] **T7.3**: Rótulos corrigidos e renomeações aprovadas executadas (leitores incluídos).
- [ ] **T7.4**: Relatórios regenerados de novo.

## Bloco 8: Validação e fechamento

- [ ] **T8.1**: Notebook do zero no `analises_env`; `validation.md` completo.
- [ ] **T8.2**: Roadmap, README, constitution e CLAUDE.md atualizados.
- [ ] **T8.3**: Revisão do usuário e merge em `staging_main`.
