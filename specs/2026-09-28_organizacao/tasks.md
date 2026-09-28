# Tarefas — `specs/2026-09-28_organizacao`

- [x] T0.1 Branch `spec/organizacao` a partir de `staging_main` (8dbf8c3); pasta da rodada
- [x] T0.2 Execução de referência de `analise.py` (antes) + hash de todas as saídas

## Fase 1a
- [ ] T1.1 `relatorio/curadoria/`: scripts de pipeline da skill `export_pdf_report` (`git mv`), importadores atualizados
- [ ] T1.2 `requirements.txt` (dependências diretas, versões fixadas) + `requirements-dev.txt`
- [ ] T1.3 Arquivos soltos removidos (registrados em `validation.md`)

## Fase 1b
- [ ] T2.1 Script de extração (AST) → pacote `primeira_infancia/`
- [ ] T2.2 `analise.py` fino: imports + `from primeira_infancia import *` + seções inalteradas
- [ ] T2.3 Execução completa (depois) + comparação de hashes

## Fechamento
- [ ] T3.1 Site, LaTeX, DOCX e inventário de fontes regenerados iguais
- [ ] T3.2 `validation.md`; docs (`CLAUDE.md`, `README.md`, skills, `specs/tech-stack.md`, `ROADMAP.md`, `CHANGELOG.md`)
