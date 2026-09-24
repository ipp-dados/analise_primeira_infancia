# Tasks: specs/matriculas-censo-escolar

Um commit por bloco. Marcar `[x]` só depois da verificação correspondente em `validation.md`.
IDs D/P são os de `specification.md`, e os blocos são os de `plan.md`.

## Bloco 0: Abertura e decisões

- [x] **T0.1**: Branch `spec/matriculas-censo-escolar` e spec rascunho 1 (2026-09-24, `d8b896c`).
- [x] **T0.2**: D1-D5 aprovadas (usuário, 2026-09-24).
- [x] **T0.3**: Check de 2025 (condição de D4): compatível, spec §3.5. P1-P4 resolvidas (`00e01ce`).
- [x] **T0.4**: Regra `/dados_locais/educacao/inep_microdados/` no `.gitignore`; ZIPs de 2020-2025 em cache.
- [x] **T0.5**: Renomear para `0_a_5` ✅ e D6 no escopo ✅ (usuário, 2026-09-24). Fonte de população levantada e testada (spec §3.6).
- [x] **T0.6**: Usuário revisou as specs e decidiu D7 ✅ Ripsa com nota metodológica, D8 ✅, D9 ✅ (2026-09-24).
- [x] **T0.7**: Ok do usuário para implementar (2026-09-24, como Parte E de `populacao-referencia`).

## Bloco 1: Downloads e P6

- [x] **T1.1**: Baixar os ZIPs de 2007-2019 no cache (2007 precisou de nova tentativa; todos passam em `testzip`).
- [x] **T1.2**: Tabela por ano em V1. Nenhuma coluna faltando.

## Bloco 2: Funções

- [x] **T2.1**: `carrega_censo_escolar_matriculas(...)`, com regex de arquivo, exceção de URL de 2025, latin-1 e extrato.
- [x] **T2.2**: *(substituída pela Parte A de `../`: `carrega_populacao_ripsa`/`populacao_ripsa`.)*
- [x] **T2.3**: `resume_matriculas_0_a_5(...)`, somando antes de dividir.
- [x] **T2.4**: D8: `linhas_referencia=None` em `serie_temporal_multipla`, sem mudar gráficos existentes.
- [x] **T2.5**: Extrato `dados_locais/educacao/inep_matriculas_rio.csv` (76 linhas) versionado; população no extrato da Parte A (`dados_locais/populacao/ripsa_populacao_rio.csv`).

## Bloco 3: Seção de análise

- [x] **T3.1**: Markdown com título e nota de método; nota metodológica de D7 (6 pontos da spec §5) em célula própria.
- [x] **T3.2**: Tabela final e os 4 PNG, com `fonte_dados`.
- [x] **T3.3**: `git rm` de `censo_escolar_matriculas_ate_6anos.csv` e dos dois arquivos `matriculas_0_a_6_*` rastreados; `git add -f` dos novos rastreáveis.
- [x] **T3.4**: Variável `df_freq_escolar` da célula de matrículas renomeada (`df_matriculas`).

## Bloco 4: Crosswalk e relatórios

- [x] **T4.1**: `estrutura_eixos.md` atualizado, sem `pendente`; taxa encaixada no catálogo ou como item novo.
- [x] **T4.2**: `line_chart` do HTML com parâmetro opcional de linhas de referência (D8); `build_html_report.py`, `build_notebook_report.py` e `regen_missing_pngs.py` ajustados (cards e blocos novos).
- [x] **T4.3**: Chave de curadoria `matriculas_0_a_6_por_ano`: não existe em `textos_curados.json` nem em nota de `analise.py`; nada a migrar.
- [x] **T4.4**: HTML, PDF e DOCX regenerados pela skill `export_pdf_report`.

## Bloco 5: Validação e fechamento

- [ ] **T5.1**: Notebook do zero (`analises_env`), V2-V5 ok.
- [ ] **T5.2**: Roadmap (Matrículas feito; mapa por escola no backlog), README (changelog curto) e constitution §3 (pasta `populacao/`).
- [ ] **T5.3**: Revisão do usuário e merge em `staging_main`.
