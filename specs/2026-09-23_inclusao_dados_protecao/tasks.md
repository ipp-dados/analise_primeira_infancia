# Tasks — specs/2026-09-23_inclusao_dados_protecao

Um commit por bloco. Marcar `[x]` só com a verificação correspondente de `validation.md` feita.
IDs T/G/M (tabelas/gráficos/mapas) e D (decisões) são os de `specification.md`.

## Bloco 0 — Aprovação e decisões
- [ ] **T0.1** — Usuário leu `specification.md`, `plan.md`, `tasks.md`, `validation.md`.
- [ ] **T0.2** — Decisões confirmadas ou alteradas: D2, D5 (`OrRd`), D6, D7 (+2,5 MB), D8, D9 (opção a), D10.
- [ ] **T0.3** — Definido se os exports Tabnet extras (tipificação, <1/1-5, interpessoal) entram
      antes do Bloco 3 ou ficam para a rodada seguinte.
- [ ] **T0.4** — Confirmado qual branch o workflow de Pages publica (`staging_main`?) e o fluxo de merge
      (`inclusao_dados_protecao` → `planning`/`staging_main`).

## Bloco 1 — Baseline de regressão (V0)
- [x] **T1.1** — Checksum SHA-256 de tudo em `tabelas_finais/`, `visualizacoes/`, `mapas/`,
      `relatorio/index.html`, PDF e DOCX, salvo no scratchpad.
- [x] **T1.2** — Contagens: `<h2>/<h3>`/cards/mapas SVG do HTML; páginas do PDF; headings do DOCX;
      tamanho do `index.html`.
- [x] **T1.3** — Registrado em `validation.md` V0 o estado (commit, o que não pôde ser regerado, ex. CadÚnico sem `.env`).

## Bloco 2 — Nível RA
- [x] **T2.1** — `'ra'` em `_NIVEIS_AGREGACAO` (`analise.py`) + menção no docstring de `mapa_coropletico_bairros`; **nenhuma outra linha alterada**.
- [x] **T2.2** — HTML: `_NIVEL_COL`, `_NIVEL_LABEL`, ramo próprio em `_geo_nivel` (nome via `regiao_adm`), `_chave_norm`.
- [x] **T2.3** — Mapa de teste por RA renderizado em `analise.py` e no HTML; asserções 33/32/{21} (V1).
- [ ] **T2.4** — Regressão rápida: um mapa de cada nível existente (`bairro`, `ap`, `rp`, `cap`) idêntico ao baseline.

## Bloco 3 — Funções (topo de `analise.py`)
- [x] **T3.1** — `numeral_romano_para_int` + `carrega_violencia_territorial_ra` (cabeçalho localizado por texto; asserção de nome).
- [x] **T3.2** — `carrega_sinan_bairro` (metadados de 6 linhas, latin-1, remove `Total`, grade sobre os 166 bairros, zeros).
- [x] **T3.3** — `carrega_violencia_familiar` (7 vínculos + `outros`; nunca somar mãe+pai).
- [x] **T3.4** — `carrega_pop_0_4_bairro` (lê `pop_censo_2022_datario.csv`; asserção contra `df_censo`).
- [x] **T3.5** — `taxa_por_mil` e `bairro_para_nivel` (CAP via `_RA_PARA_CAP`).
- [x] **T3.6** — Tema `protecao` em `_CORES_TEMA_MAPA` (`OrRd`).
- [x] **T3.7** — Script de verificação no scratchpad reproduz os números de V2 (totais por vínculo/ano, 32 RAs, etc.).

## Bloco 4 — Seção "🛡️ Proteção" em `analise.py` (inserida antes de "Análise / Relatório")
- [x] **T4.0** — Célula markdown de abertura da seção (padrão emoji/`##` do arquivo).
- [x] **T4.1** — 4a: T1, T2, T3 (RA e CAP), T4 → `tabelas_finais/`.
- [x] **T4.2** — 4a: G1 (com anotação 2017), G2, G3 → `visualizacoes/`.
- [x] **T4.3** — 4a: M1, M2, M3 (`bins`; limites calibrados e registrados) → `mapas/` + `tabela_mapa_*.csv`.
- [x] **T4.4** — 4b: T5, G7 (2018-2025 × 2026), M7 (2026).
- [x] **T4.5** — 4c: T6, G4-G6, M4-M6 (`nivel='ra'`, `chave='codra'`, contínuo).
- [x] **T4.6** — 4d: T7, M8-M10, G8; rótulos D9; bairros de pop 0-4 < 100 listados (D10).
- [x] **T4.7** — Todas as chamadas com `fonte_dados`; convenções bins × contínuo; nada de média de taxa entre bairros.
- [ ] **T4.8** — Corte D8: revisar G3, G8, M8-M10 com o usuário; remover o redundante (e as linhas correspondentes nos blocos 5-8).
- [x] **T4.9** — Rodada completa de `analise.py`/`jupytext` sem erro; `analise.ipynb` sincronizado (gitignored).

## Bloco 5 — `specs/estrutura_eixos.md`
- [x] **T5.1** — Subseções de Proteção com arquivos reais, `fonte` corrigida e `nota` de limitação.
- [x] **T5.2** — Subseções 🅱 adicionadas (composição "outros", top bairros, taxas RA/CAP).
- [x] **T5.3** — Tipificação e recorte <1/1-5 mantidos `pendente`.
- [x] **T5.4** — SGB/inundação removido da estrutura publicada (fora da V1).
- [x] **T5.5** — `parse_estrutura_eixos()` roda; contagens por eixo conferidas; `gera_estrutura_eixos.py` **não** re-executado.

## Bloco 6 — HTML
- [x] **T6.1** — `_CMAP_TEMA['protecao']='OrRd'`.
- [x] **T6.2** — Proteção: blocos reais (`h3`, `option_card`, `mapa_svg`, tabelas) substituem os 5 `emite_bloco_pendente`; pendentes só para tipificação e <1/1-5.
- [x] **T6.3** — Bloco SGB removido de Moradia.
- [x] **T6.4** — Notas metodológicas (2017, 2026, vínculos, IPS, D9) no lugar do texto de análise padrão.
- [x] **T6.5** — Tamanho do HTML medido; dentro de D7 ou compressão aplicada.
- [ ] **T6.6** — Aberto e navegado em tema claro/escuro (V4).

## Bloco 7 — PDF
- [x] **T7.1** — Proteção com `chart_block`/`emit_map_gallery` (`MAP_GROUPS_PROTECAO`)/`registra_tabela`; SGB removido.
- [x] **T7.2** — PDF regenerado via skill `export_pdf_report`; páginas e quebras conferidas (V5).

## Bloco 8 — DOCX
- [x] **T8.1** — Edições manuais do DOCX atual sincronizadas (`sincroniza_docx.py`) **antes** de regenerar.
- [x] **T8.2** — `gera_docx_curadoria.py` regenerado; blocos de texto para cada visualização nova.
- [x] **T8.3** — Ida-e-volta (gerar → sincronizar) sem diff nos eixos não-Proteção (V6).

## Bloco 9 — Textos e notas
- [ ] **T9.1** — Seis notas do plano (§Bloco 9) redigidas, com hipóteses marcadas como tal.
- [ ] **T9.2** — Usuário revisou e aprovou os textos (via DOCX).
- [ ] **T9.3** — Aprovados propagados a HTML/PDF/`analise.py` (`sincroniza_docx.py`).

## Bloco 10 — Documentação mínima
- [ ] **T10.1** — `specs/roadmap.md` (item 5 concluído), `specs/tech-stack.md`, `relatorio/specs.md`, `CHANGELOG.md`.
- [x] **T10.2** — `.claude/skills/generate_map/SKILL.md` (`nivel='ra'`, `codra`) e `CLAUDE.md` (uma linha RA≠AP≠CAP).

## Bloco 11 — Validação final
- [ ] **T11.1** — `validation.md` V0-V8 executado; resultados anotados.
- [ ] **T11.2** — Diff contra baseline: só adições + eixo Proteção + remoção do SGB.
- [ ] **T11.3** — Usuário revisou HTML/PDF/DOCX e deu "ok" de validação.

## Bloco 12 — Publicação no GitHub Pages (gated)
- [ ] **T12.1** — **"Ok" explícito do usuário** para publicar. *Sem isso, parar aqui.*
- [ ] **T12.2** — Merge para a branch de deploy conforme T0.4.
- [ ] **T12.3** — `workflow_dispatch` de `deploy-relatorio.yml`.
- [ ] **T12.4** — Página publicada conferida (V9); commit de reversão anotado.
- [ ] **T12.5** — `specs/roadmap.md` atualizado com o resultado; itens seguintes (população ano a ano, CadÚnico, documentação) intactos.
