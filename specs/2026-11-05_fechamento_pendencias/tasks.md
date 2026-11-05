# TASKS — Fechamento de pendências (2026-11-05)

Legenda: [x] feito · [ ] a fazer

## Planejamento
- [x] P1 Conferir branches, stash e ROADMAP (trabalho em andamento)
- [x] P2 Perguntas ao usuário → D1-D9
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`
- [ ] P4 OK do usuário no plano e na redação do ISP (ponto aberto P1 da spec)

## B1 — SISVAN
- [ ] T1.1 `recalcula_percentuais_sisvan` em `limpeza.py` (+ `__all__`)
- [ ] T1.2 Seção SISVAN do `analise.py` usa a função
- [ ] T1.3 Conferir/atualizar textos curados e notas `sisvan_*`

## B2 — Cores
- [ ] T2.1 `estilo.py`: `censo` → `Purples`, `natalidade` → `Greens`
- [ ] T2.2 `build_site.py`: `natalidade` → `Greens`; comentários

## B3 — Mapas de número em Moradia
- [ ] T3.1 2 mapas em `analise.py` (classes discretas, A4)
- [ ] T3.2 `estrutura_eixos.md`
- [ ] T3.3 `build_site.py` (`mapa_svg`)

## B4 — ISP
- [ ] T4.1 Trocar citações e rótulos (lista de R5)
- [ ] T4.2 Renomear `fonte_ips`/`FONTE_IPS`

## Execução
- [ ] T5.1 Rodar `analise.py` completo (B1-B4) com variante A4

## B5 — PDF
- [ ] T5.2 `tabelas.py` (Inclusão e Moradia) e `fontes.bib`
- [ ] T5.3 Regerar o PDF (sem publicar) e conferir

## B6 — Textos
- [ ] T6.1 Lista das chaves sem texto em Inclusão e Moradia
- [ ] T6.2 Rascunhos com números conferidos
- [ ] T6.3 Aprovação do usuário
- [ ] T6.4 Aplicar em `textos_curados.json` e `controle_revisao.json`

## B7 — Regerar e conferir
- [ ] T7.1 Site + `confere_textos.py`
- [ ] T7.2 Playwright desktop e celular
- [ ] T7.3 PDF final da rodada (sem publicar)

## B8 — Fechamento
- [ ] T8.1 ROADMAP, CLAUDE.md, `docs/especificacao_projeto.md`, skill `generate_map`
- [ ] T8.2 `validation.md` preenchido
- [ ] T8.3 Merge em `staging_main` e tag `rodada/fechamento_pendencias` (com OK)
