# TASKS — Privacidade do CadÚnico

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-09-29)
- [x] P1 Auditoria das tabelas versionadas, do histórico do git e dos percentuais publicados
- [x] P2 Perguntas agrupadas ao usuário → D1-D3
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`; commit e push de `planning`

## B1 — Função
- [x] T1.1 `agrega_bairros_pequenos` em `primeira_infancia/cadunico.py` (RA → AP → município; numerador/complemento)
- [x] T1.2 Teste com dados sintéticos

## B2 — `analise.py`
- [x] T2.1 `cadunico_por_bairro_2026` e `..._ate_4_2026` com conjuntos agregados
- [x] T2.2 Tabelas e mapas de contagem (`tabela_mapa_cadunico_criancas_2026`, `..._0_a_4_2026`)
- [x] T2.3 Recortes (% negras, % uma adulta) com D2; mapas de percentual com a taxa do conjunto
- [x] T2.4 Nota de agregação nos mapas e nas fontes

## B3 — Site
- [x] T3.1 `mapa_svg(col_agregado=...)`: tooltip e CSV com o conjunto
- [x] T3.2 Cartões do CadÚnico usando a coluna

## B4 — Rodar e conferir
- [x] T4.1 Execução completa de `analise.py`
- [x] T4.2 Site, PDF (sem `--publicar`), DOCX, deck
- [x] T4.3 Auditoria automática (R3) e `validation.md`

## B5 — Regra e registro
- [x] T5.1 Constituição §6, `CLAUDE.md`, ROADMAP (histórico, D3), CHANGELOG, README, especificação do projeto
- [x] T5.2 Merge `spec/privacidade-cadunico` → `planning` → `staging_main`; push (2026-09-29)
