# TASKS — Dados pontuais do CadÚnico: Moradia e Inclusão

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-09-29)
- [x] P1 Leitura do pedido (`dados_adhoc.txt`) e da planilha; achados A1-A6
- [x] P2 Perguntas agrupadas ao usuário → D1-D4
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`; commit de `planning`

## B1 — Dados e funções
- [ ] T1.1 `dados_locais/cadunico/`: planilha renomeada, `deficiencia_cadunico_2026_08.csv`, manifesto `adhoc_2026_08.json`
- [ ] T1.2 `carrega_moradia_cadunico_adhoc` (filtro pelo cabeçalho, A1-A3, duplicata) em `primeira_infancia/cadunico.py`
- [ ] T1.3 `carrega_deficiencia_cadunico_adhoc` (total 0-6, % BPC); `__all__`
- [ ] T1.4 Conferência sintética (A1, A2, A3, duplicata divergente → erro)

## B2 — `analise.py`
- [ ] T2.1 Célula "Dados pontuais (ago/2026)" ao fim da seção CadÚnico, gravando as 3 CSVs
- [ ] T2.2 Rodar a célula isolada; `jupytext --to notebook` sem erro

## B3 — Crosswalk
- [ ] T3.1 Itens novos em Inclusão (1) e Moradia (2), com `aviso:`
- [ ] T3.2 Documentar o campo `- aviso:` no cabeçalho de `specs/estrutura_eixos.md`

## B4 — Site
- [ ] T4.1 Geração de referência (antes) para a comparação
- [ ] T4.2 Helpers `cartoes_indicador`, `barras_razao`, callout "Dado pontual"
- [ ] T4.3 Blocos de Inclusão e Moradia (depois dos pendentes)
- [ ] T4.4 CSS novo (`components.css`, `mobile.css`)
- [ ] T4.5 Build + `confere_textos.py`; screenshots desktop/telefone

## B5 — PDF
- [ ] T5.1 Ambiente `aviso` (`estilo.sty`) e leitura de `- aviso:` em `secoes_indicadores`
- [ ] T5.2 `AJUSTES` das 3 tabelas; inventário de fontes
- [ ] T5.3 Build sem `--publicar`; conferir as páginas novas

## B6 — Deck
- [ ] T6.1 Funções em `apresentacao/build/numeros.py`
- [ ] T6.2 Slide novo antes de "Eixos incompletos"; build sem `--publicar`

## B7 — Registro
- [ ] T7.1 `ROADMAP.md` (rodada atual; substituição no 4º tri de 2026)
- [ ] T7.2 `CHANGELOG.md`, `README.md`, `docs/especificacao_projeto.md`, `CLAUDE.md`
- [ ] T7.3 `validation.md` preenchido; DOCX de curadoria regerado sem erro
