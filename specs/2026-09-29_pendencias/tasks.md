# TASKS — Pendências

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-09-29)
- [x] P1 Reorganizar o `ROADMAP.md` (A fazer × Concluído) e conferir o que ainda estava em andamento (deploy já feito;
  PDF publicado anterior à nova estrutura; caixas antigas de `relatorio_latex`)
- [x] P2 Perguntas agrupadas ao usuário (3 rodadas) → D1-D12
- [x] P3 Levantamento do código de cada item (`plan.md`); mapas duplicados conferidos (167 × 167, iguais)
- [x] P4 Constituição: perguntas pela ferramenta interativa (§5); os 4 documentos obrigatórios antes de implementar (§5)
- [x] P5 `specification.md`, `plan.md`, `tasks.md`, `validation.md`; commit e push de `planning`

## B0 — Abertura e linha de base
- [ ] T0.1 Branch `spec/pendencias` a partir de `planning`
- [ ] T0.2 Hash de todas as saídas de `tabelas_finais/`, `visualizacoes/` (inclui `a4/`) e `mapas/` (inclui `a4/`)
- [ ] T0.3 Capturas do site (Playwright): desktop 1440 e 1100, tablet 800 e 1024, celular 390 — todas as abas
- [ ] T0.4 Inventário do PDF (figuras, tabelas, páginas) e do site (seeds, ids) — script da `nova_estrutura`

## B1 — Mapa duplicado (D1, R1)
- [ ] T1.1 `build_site.py`: tirar a pill "Total" de `_mapas_neo_obitos` e `_mapas_neo_taxa`
- [ ] T1.2 `specs/estrutura_eixos.md`: tirar `mapa_taxa_mortalidade_infantil_bairro_2025.png` com `- nota:` (E13)
- [ ] T1.3 `specs/exclusoes.md`: linha E13
- [ ] T1.4 Deck: `apresentacao.md` → `fig:mapa_taxa_obitos_raca_total_bairro_2025` (D10)

## B2 — "Não informada" fora da taxa (D2, R2)
- [ ] T2.1 `analise.py`: rótulos próprios do gráfico de taxa, sem `nao_informado`; nota na fonte
- [ ] T2.2 `build_site.py`: séries do pill "Taxa por raça/cor" sem `nao_informado`; nota na fonte
- [ ] T2.3 `specs/exclusoes.md`: linha E14

## B3 — Eixo cortado no baixo peso (D3, D12, R3)
- [ ] T3.1 `primeira_infancia/graficos.py`: `serie_temporal(..., base_zero=True)`; com `False`, eixo ajustado +
  marca de corte + nota na fonte
- [ ] T3.2 `primeira_infancia/impressao.py`: o mesmo em `_a4_serie_unica` (e no caminho que a chama)
- [ ] T3.3 `website/js/charts.js`: `opts.eixoCortado` → `zeroBase:false` + marca de corte; `build_site.py` passa a
  opção e a nota só no gráfico de baixo peso
- [ ] T3.4 `analise.py`: chamada do baixo peso com `base_zero=False`
- [ ] T3.5 Registrar a exceção à P1 (`relatorio/specs.md`, `CLAUDE.md`)

## B4 — Faixa 0-5 (D9, D4, R4)
- [ ] T4.1 Regra da faixa 0-5 em `specs/constitution.md` e `CLAUDE.md`; nova entrada em `auditoria_faixas.md`
- [ ] T4.2 Função em `primeira_infancia/` (tema educação/população): taxa de frequência por idade × corte a partir de
  10057 ÷ 9606, com "Amarela e indígena" e "Total" 0-5
- [ ] T4.3 `analise.py`: população 0-5 por sexo e raça/cor; taxa de frequência recalculada; gráficos (tela + A4) sem
  6 anos; conferência contra a 10056 idade a idade (registrar em `validation.md`)
- [ ] T4.4 Série Ripsa por idade: gráficos e números em 0-5
- [ ] T4.5 `build_site.py`, `relatorio/latex/build/tabelas.py`, `apresentacao/build/numeros.py`: ler as tabelas novas;
  rótulos "0 a 5 anos"
- [ ] T4.6 `specs/estrutura_eixos.md`: títulos "até 6 anos" → "0 a 5 anos" (chaves mantidas), nota com o nome do
  catálogo
- [ ] T4.7 Varredura de "6 anos"/"0-6"/"até 6" em site, PDF gerado, deck, `analise.py` (títulos): nota ou correção
- [ ] T4.8 `specs/exclusoes.md`: E12 aplicado

## B5 — Tablet (D5, R5)
- [ ] T5.1 `css/mobile.css` (720-1099 px): alvos ≥ 44 px (pills, abas, botões CSV/outlier, sumário, rodapé)
- [ ] T5.2 `js/charts.js`: redesenho em largura real também no tablet, com texto entre 9,5 e 11 px
- [ ] T5.3 Comparar o desktop pixel a pixel com T0.3

## B6 — Registro e fechamentos (D6, D7, R6, R9)
- [ ] T6.1 Unidade do IPS confirmada (spec do Proteção, sem ressalva no site/PDF se houver)
- [ ] T6.2 Centro só no deck: nota em `specs/2026-09-28_apresentacao`
- [ ] T6.3 `nova_estrutura` T6.3, `apresentacao` T5.2; nota de fechamento em `relatorio_latex/tasks.md`

## B7 — Textos (D11, R8)
- [ ] T7.1 Ajustar os trechos afetados em `relatorio/textos_curados.json` e nas notas espelhadas de `analise.py`
- [ ] T7.2 Marcar `revisar` em `relatorio/controle_revisao.json`

## B8 — Regerar e validar
- [ ] T8.1 Rodar as células afetadas de `analise.py` (com `GERA_VARIANTE_A4`)
- [ ] T8.2 `build_site.py`; `gera_latex.py` (sem `--publicar`); DOCX de curadoria; deck (sem `--publicar`)
- [ ] T8.3 Preencher `validation.md` (V1-V14)

## B9 — Fechamento
- [ ] T9.1 `CHANGELOG.md`, `docs/especificacao_projeto.md` (§11), `ROADMAP.md`
- [ ] T9.2 Merge `spec/pendencias` → `planning` → `staging_main`; push
- [ ] T9.3 Com OK do usuário: `gera_latex.py --publicar`, deploy do site, deck `--publicar`, tags `rodada/*`,
  limpeza de branches (D7, D8)
