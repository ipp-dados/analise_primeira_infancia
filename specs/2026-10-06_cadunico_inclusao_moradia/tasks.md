# TASKS — CadÚnico: pipeline novo para Inclusão e Moradia

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-10-06)
- [x] P1 Levantamento do banco (tabelas, partições, categorias, tamanho das células por bairro, ponte CEP → bairro)
- [x] P2 Perguntas ao usuário → D1-D4; escopo proposto (D3, §3-§4 da spec)
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`; commit em `planning`

## B1 — Pacote (`primeira_infancia/cadunico.py`)
- [x] T1.1 `carrega_criancas_cadunico_silver` (ponte, só colunas usadas; famílias derivadas das crianças, sem carregador próprio)
- [x] T1.2 `sim_base` e tabelas (deficiência, tipos, moradia-resumo, componentes FJP), `por_bairro_sim_base`
- [x] T1.3 Constantes de rótulos/ordem; `__all__`
- [x] T1.4 Conferência com `gold_cadunico_indicadores` (município)

## B2 — `analise.py`
- [x] T2.1 Filtro `'0-6'` → `'0-5'` (seção e `carrega_cadunico_familias_0_6`); notas da seção
- [x] T2.2 Subseção nova: CSVs, 3 gráficos, 3 mapas + gêmeas (privacidade)
- [x] T2.3 Nota na célula do dado pontual (fora do site, D1)
- [x] T2.4 Execução completa (kernel limpo); saídas e variante A4 conferidas

## B3 — Crosswalk
- [x] T3.1 Inclusão: R1-R3; Moradia: R4-R6; itens pontuais removidos

## B4 — Site (`staging_main`)
- [x] T4.1 Inclusão e Moradia em `build_site.py` (cartões, gráficos, mapas, tabelas); blocos pontuais fora
- [x] T4.2 Regerar; conferir navegador (desktop/celular), lorem nas chaves novas, sem `data-dado-pontual`, orçamento

## B5 — Documentação e integração
- [x] T5.1 ROADMAP, `specs/exclusoes.md`, `docs/especificacao_projeto.md`, CHANGELOG/README
- [x] T5.2 `validation.md` preenchido; merge `--no-ff` em `staging_main`

## B6 — Demo
- [x] T6.1 Merge `staging_main` → `demo`
- [x] T6.2 `publicacao.json`: `lancamento_v1 = 2026-10-13`, faixa com próxima atualização de conteúdo e textos, nota das abas
- [x] T6.3 `demo.py`: nota nas abas Inclusão e Moradia
- [x] T6.4 `textos_demo.json`: chaves novas; números CadÚnico atualizados
- [x] T6.5 Regerar site da demo (conferência passa) e o aviso do PDF (só a página de aviso, D9)
