# Tasks: specs/matriculas-censo-escolar

Um commit por bloco. Marcar `[x]` só depois da verificação correspondente em `validation.md`.
IDs D/P são os de `specification.md`, e os blocos são os de `plan.md`.

## Bloco 0: Abertura e decisões

- [x] **T0.1**: Branch `spec/matriculas-censo-escolar` e spec rascunho 1 (2026-09-24, `d8b896c`).
- [x] **T0.2**: D1-D5 aprovadas (usuário, 2026-09-24).
- [x] **T0.3**: Check de 2025 (condição de D4): compatível, spec §3.5. P1-P4 resolvidas (`00e01ce`).
- [x] **T0.4**: Regra `/dados_locais/educacao/inep_microdados/` no `.gitignore`; ZIPs de 2020-2025 em cache.
- [x] **T0.5**: Renomear para `0_a_5` ✅ e D6 no escopo ✅ (usuário, 2026-09-24). Fonte de população levantada e testada (spec §3.6).
- [ ] **T0.6**: Usuário revisa as specs (rascunho 3) e decide D7-D9.
- [ ] **T0.7**: Ok do usuário para implementar.

## Bloco 1: Downloads e P6

- [ ] **T1.1**: Baixar os ZIPs de 2007-2019 no cache.
- [ ] **T1.2**: Tabela por ano (arquivo, encoding, colunas, total 0-5 do Rio) em V1. Parar se faltar coluna.

## Bloco 2: Funções

- [ ] **T2.1**: `carrega_censo_escolar_matriculas(...)`, com regex de arquivo, exceção de URL de 2025, latin-1 e extrato.
- [ ] **T2.2**: `carrega_populacao_ripsa(...)`, com POST no Tabnet, extrato e checagem de anos e idades.
- [ ] **T2.3**: `resume_matriculas_0_a_5(...)`, somando antes de dividir.
- [ ] **T2.4**: Se D8 = (b): `linhas_referencia=None` em `serie_temporal_multipla`, sem mudar gráficos existentes.
- [ ] **T2.5**: Extratos `dados_locais/educacao/inep_matriculas_rio.csv` (76 linhas) e `dados_locais/populacao/ripsa_populacao_rio_0_6_idade_simples.csv` (133 linhas) gerados e versionados.

## Bloco 3: Seção de análise

- [ ] **T3.1**: Markdown com título e nota de método (inclui ressalvas da taxa, Ripsa × Censo e PNE).
- [ ] **T3.2**: Tabela final e os 4 PNG, com `fonte_dados`.
- [ ] **T3.3**: `git rm` de `censo_escolar_matriculas_ate_6anos.csv` e dos dois arquivos `matriculas_0_a_6_*` rastreados; `git add -f` dos novos rastreáveis.
- [ ] **T3.4**: Variável `df_freq_escolar` da célula de matrículas renomeada (`df_matriculas`).

## Bloco 4: Crosswalk e relatórios

- [ ] **T4.1**: `estrutura_eixos.md` atualizado, sem `pendente`; taxa encaixada no catálogo ou como item novo.
- [ ] **T4.2**: `build_html_report.py`, `build_notebook_report.py` e `regen_missing_pngs.py` ajustados (cards e blocos novos).
- [ ] **T4.3**: Chave de curadoria `matriculas_0_a_6_por_ano` migrada, se existir.
- [ ] **T4.4**: HTML, PDF e DOCX regenerados pela skill `export_pdf_report`.

## Bloco 5: Validação e fechamento

- [ ] **T5.1**: Notebook do zero (`analises_env`), V2-V5 ok.
- [ ] **T5.2**: Roadmap (Matrículas feito; mapa por escola no backlog), README (changelog curto) e constitution §3 (pasta `populacao/`).
- [ ] **T5.3**: Revisão do usuário e merge em `staging_main`.
