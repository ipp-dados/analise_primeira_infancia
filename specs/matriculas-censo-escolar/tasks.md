# Tasks: specs/matriculas-censo-escolar

Um commit por bloco. Marcar `[x]` só depois da verificação correspondente em `validation.md`.
IDs D/P são os de `specification.md`, e os blocos são os de `plan.md`.

## Bloco 0: Abertura e decisões
- [x] **T0.1**: Branch `spec/matriculas-censo-escolar` e spec rascunho 1 (2026-09-24, `d8b896c`).
- [x] **T0.2**: D1-D5 aprovadas (usuário, 2026-09-24). D6 sem resposta, segue a proposta.
- [x] **T0.3**: Check de 2025 (condição de D4): compatível, spec §3.5. P1-P4 resolvidas.
- [x] **T0.4**: Regra `/dados_locais/educacao/inep_microdados/` no `.gitignore`; ZIPs de 2020-2025 em cache.
- [ ] **T0.5**: Usuário aprova `plan.md` e a sub-decisão do nome (renomear para `0_a_5`).

## Bloco 1: Downloads e P6
- [ ] **T1.1**: Baixar os ZIPs de 2007-2019 no cache.
- [ ] **T1.2**: Tabela por ano (arquivo, encoding, colunas, total 0-5 do Rio) em V1. Parar se faltar coluna.

## Bloco 2: Funções
- [ ] **T2.1**: `carrega_censo_escolar_matriculas(...)`, com regex de arquivo, exceção de URL de 2025, latin-1 e extrato.
- [ ] **T2.2**: `resume_matriculas_0_a_5(df_extrato)`.
- [ ] **T2.3**: Extrato `dados_locais/educacao/inep_matriculas_rio.csv` gerado (76 linhas) e versionado.

## Bloco 3: Seção de análise
- [ ] **T3.1**: Markdown com título e nota de método.
- [ ] **T3.2**: Tabela final e os 3 PNG, com `fonte_dados`.
- [ ] **T3.3**: `git rm` de `censo_escolar_matriculas_ate_6anos.csv` e dos dois arquivos `matriculas_0_a_6_*` rastreados; `git add -f` dos novos rastreáveis.
- [ ] **T3.4**: Variável `df_freq_escolar` da célula de matrículas renomeada (`df_matriculas`).

## Bloco 4: Crosswalk e relatórios
- [ ] **T4.1**: `estrutura_eixos.md` atualizado, sem `pendente`.
- [ ] **T4.2**: `build_html_report.py`, `build_notebook_report.py` e `regen_missing_pngs.py` ajustados.
- [ ] **T4.3**: Chave de curadoria `matriculas_0_a_6_por_ano` migrada, se existir.
- [ ] **T4.4**: HTML, PDF e DOCX regenerados pela skill `export_pdf_report`.

## Bloco 5: Validação e fechamento
- [ ] **T5.1**: Notebook do zero (`analises_env`), V2-V4 ok.
- [ ] **T5.2**: Roadmap (Matrículas feito; taxa de atendimento e mapa por escola no backlog) e README (changelog curto).
- [ ] **T5.3**: Revisão do usuário e merge em `staging_main`.
