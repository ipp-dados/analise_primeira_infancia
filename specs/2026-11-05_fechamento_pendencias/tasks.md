# TASKS — Fechamento de pendências (2026-11-05)

Legenda: [x] feito · [ ] a fazer

## Planejamento
- [x] P1 Conferir branches, stash e ROADMAP (trabalho em andamento)
- [x] P2 Perguntas ao usuário → D1-D9
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`
- [x] P4 OK do usuário no plano e na redação do ISP (ponto aberto P1 da spec)

## B1 — SISVAN
- [x] T1.1 `recalcula_percentuais_sisvan` em `limpeza.py` (+ `__all__`)
- [x] T1.2 Seção SISVAN do `analise.py` usa a função
- [x] T1.3 Conferir/atualizar textos curados e notas `sisvan_*`

## B2 — Cores
- [x] T2.1 `estilo.py`: `censo` → `Purples`, `natalidade` → `Greens`
- [x] T2.2 `build_site.py`: `natalidade` → `Greens`; comentários

## B3 — Mapas de número em Moradia
- [x] T3.1 2 mapas em `analise.py` (classes discretas, A4)
- [x] T3.2 `estrutura_eixos.md`
- [x] T3.3 `build_site.py` (`mapa_svg`)

## B4 — ISP
- [x] T4.1 Trocar citações e rótulos (lista de R5)
- [x] T4.2 Renomear `fonte_ips`/`FONTE_IPS`

## Execução
- [x] T5.1 Rodar `analise.py` completo (B1-B4) com variante A4

## B5 — PDF
- [x] T5.2 `tabelas.py` (Inclusão e Moradia) e `fontes.bib`
- [x] T5.3 Regerar o PDF (sem publicar) e conferir

## B6 — Textos
- [x] T6.1 Lista das chaves sem texto em Inclusão e Moradia
- [x] T6.2 Rascunhos com números conferidos
- [x] T6.3 Aprovação do usuário
- [x] T6.4 Aplicar em `textos_curados.json` e `controle_revisao.json`

## B7 — Regerar e conferir
- [x] T7.1 Site + `confere_textos.py`
- [x] T7.2 Playwright desktop e celular
- [x] T7.3 PDF final da rodada (sem publicar)

## B8 — Fechamento
- [x] T8.1 ROADMAP, CLAUDE.md, `docs/especificacao_projeto.md`, skill `generate_map`
- [x] T8.2 `validation.md` preenchido
- [ ] T8.3 Merge em `staging_main` e tag `rodada/fechamento_pendencias` (com OK)
