# Tasks — specs/recortes_cadunico

Um commit por bloco. Marcar `[x]` só depois da verificação correspondente em `validation.md`.
IDs R/S/A/D/F são os de `specification.md`, e os blocos são os de `plan.md`.

## Bloco 0 — Aprovação e decisões
- [x] **T0.1** — Spec rascunho 1 revisada e D1-D5 aprovadas (usuário, 2026-09-23).
- [x] **T0.2** — Revisão de sanidade das saídas CadÚnico existentes incorporada à spec (§6).
- [x] **T0.3** — Usuário leu `plan.md`, `tasks.md` e `validation.md`.
- [x] **T0.4** — D6 ✅ (mapa % fora do HTML/PDF), D8 ✅ (renomear; checado que nenhum outro uso precisa do nome antigo), D7 ⏸️ adiada para o roadmap item 6 (auditoria de faixas etárias entre fontes).

## Bloco 1 — Ambiente e baseline (V0)
- [x] **T1.1** — Kernel `analises_env` confirmado (`psycopg` 3.3.4) e cwd na raiz do repo.
- [x] **T1.2** — Checksums SHA-256 de `tabelas_finais/`, `visualizacoes/`, `mapas/`, `relatorio/*` salvos no scratchpad.
- [x] **T1.3** — Contagens do HTML (`<h2>/<h3>`, cards, mapas SVG, tamanho), páginas do PDF e headings do DOCX.
- [x] **T1.4** — Seção CadÚnico rodada sem alteração. As 6 tabelas `cadunico_*` saem idênticas às versionadas (mesma partição). Se não saírem: parar e reportar.

## Bloco 2 — Funções (topo de `analise.py`)
- [x] **T2.1** — `_ROTULOS_RENDA_CADUNICO`, `_ORDEM_RENDA_CADUNICO` e o agrupamento de 3 faixas.
- [x] **T2.2** — `carrega_cadunico_familias_0_6(engine)`: filtro no SQL, só as colunas necessárias.
- [x] **T2.3** — `classifica_arranjo_familiar(df_membros, idade_adulto=18)` com asserções (renda única por família; linhas = `n_pessoas_familia`).
- [x] **T2.4** — `agrega_cadunico_por_categoria(df, coluna, exclusivas)`.
- [x] **T2.5** — `suprime_celulas_pequenas(df, coluna_denominador, colunas, limiar=20)`, testada à mão num df de 3 linhas.

## Bloco 3 — Correções nas saídas existentes
- [x] **T3.1** — A1: linha "Sem bairro identificado" + nota reescrita com os números reais.
- [x] **T3.2** — A2: nota do mapa % reescrita (causa CEP→bairro, bairros afetados) + nota curta nos 3 mapas CadÚnico.
- [x] **T3.3** — A3 (D7 adiada): **títulos existentes intocados**. Só a nota markdown com a definição real de idade CadÚnico (nascidos ≥ 2020-08-12, idade em ~2026-08-12, 6 anos no grupo `'7-14'`).
- [x] **T3.4** — A4: supressão < 20 nas 2 tabelas por bairro e nas 2 gêmeas de mapa.
- [x] **T3.5** — A5: `cadunico_por_faixa_renda_2026.csv` + `git rm` do nome antigo; `README.md:74` atualizado (leitores nos Blocos 9-10, mesmo PR).
- [x] **T3.6** — A6 + A8: notas (famílias por idade não somam, sub-registro no 1º ano, filtro de cadastro).
- [x] **T3.7** — A7: rótulos descritivos nos 2 gráficos de renda.
- [x] **T3.8** — `fonte_cadunico_particao` nas chamadas corrigidas.

## Bloco 4 — R1 sexo
- [x] **T4.1** — `df_familias` carregado uma vez (Blocos 4-7).
- [x] **T4.2** — `cadunico_por_sexo_2026.csv` (crianças por sexo + famílias por composição, Σ = 173.768).
- [x] **T4.3** — `cadunico_criancas_por_sexo.png`, `cadunico_familias_por_sexo_criancas.png`.

## Bloco 5 — R2 raça/cor
- [x] **T5.1** — `cadunico_por_raca_cor_2026.csv` (5 categorias + "Negra"; famílias não exclusivas, com nota).
- [x] **T5.2** — `cadunico_criancas_por_raca_cor.png`, `cadunico_familias_por_raca_cor.png`.

## Bloco 6 — R3 arranjo × renda
- [x] **T6.1** — `cadunico_familias_por_arranjo_2026.csv`.
- [x] **T6.2** — `cadunico_familias_arranjo_renda_2026.csv` (3 faixas, contagem e %, supressão < 20).
- [x] **T6.3** — `cadunico_familias_por_arranjo.png`, `cadunico_familias_arranjo_renda.png`.
- [x] **T6.4** — Célula markdown com a nota metodológica + inspeção agregada das famílias sem adulto.

## Bloco 7 — Mapas por bairro
- [x] **T7.1** — Tabela por bairro (join por `codbairro` via `junta_codbairro_por_bairro`), 3 taxas recalculadas de absolutos.
- [x] **T7.2** — Supressão < 20 → `tabela_mapa_cadunico_recortes_bairro_2026.csv`.
- [x] **T7.3** — 3 mapas de taxa (`bins=None`, `cadunico`, fonte + rodapé de supressão e geocodificação).

## Bloco 8 — Crosswalk
- [x] **T8.1** — As 3 entradas de Inclusão preenchidas em `specs/estrutura_eixos.md`.
- [x] **T8.2** — Família e Cuidados: CSV renomeado (D8) e mapa % retirado (D6), se aprovados.

## Bloco 9 — HTML
- [x] **T9.1** — 3 `emite_bloco_pendente` → `option_card`s reais no eixo Inclusão.
- [x] **T9.2** — `mapa_svg(rotulo_nan=…)` com default inalterado; tooltip "suprimido (< 20)".
- [x] **T9.3** — Bloco CadÚnico existente: A5, A7, D6, fonte com partição (títulos de idade intocados, D7).
- [x] **T9.4** — HTML regenerado; o diff estrutural contra o baseline mostra só as mudanças esperadas.

## Bloco 10 — PDF e DOCX
- [ ] **T10.1** — PDF: 3 `pending` → blocos reais; A5, D6 e notas no trecho existente.
- [ ] **T10.2** — `regen_missing_pngs.py`: leitor renomeado.
- [ ] **T10.3** — PDF e DOCX regenerados (skill `export_pdf_report`).

## Bloco 11 — Documentação
- [ ] **T11.1** — `README.md`: changelog curto.
- [ ] **T11.2** — `specs/roadmap.md`: item 8 (1ª leva) concluído, F1-F3 no backlog.
- [ ] **T11.3** — `CLAUDE.md`/`specs/tech-stack.md`: kernel `analises_env` e regra de supressão CadÚnico.
- [ ] **T11.4** — `specs/constitution.md` §6: limiar 20. **Só com ok explícito do usuário.**

## Bloco 12 — Validação e revisão
- [ ] **T12.1** — Notebook do zero, top-to-bottom, no `analises_env`, sem erro.
- [ ] **T12.2** — `validation.md` V1-V8 com evidência.
- [ ] **T12.3** — Revisão visual com o usuário (candidato a corte: mapa % meninas).
- [ ] **T12.4** — Merge em `planning` só depois do ok do usuário. Deploy no Pages fica fora desta rodada.
