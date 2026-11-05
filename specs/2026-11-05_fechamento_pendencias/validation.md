# VALIDATION — Fechamento de pendências (2026-11-05)

## Planejamento (2026-11-05)

| Verificação | Resultado |
|---|---|
| Branches locais/remotas | `staging_main` (= origin), `main` (ancestral de `staging_main`), `demo`; sem stash, 1 worktree |
| SISVAN, erro na origem | obesidade 2009: `obesidade_percentual = 0.07` (sem `%`), 1.623 / 23.196 = 7,0% |
| Mapas de número em Moradia | só no deck (`apres_cadunico_inadequacao_n_bairro`, `apres_cadunico_adensamento_n_bairro`); 0 no crosswalk |
| `tabelas.py`, Inclusão/Moradia | nenhuma entrada de deficiência/inadequação/adensamento/déficit |
| Planilha da violência territorial | título "Indicadores do Índice de Progresso Social (IPS) … 2024"; sem menção ao ISP (P1) |
| Azul em mapas | `analise.py`/PDF: `censo` = `Blues`, `natalidade` = `BuGn`; site: `censo` = `Purples`, `natalidade` = `BuGn` |
| Lorem no site de `staging_main` | 83 ocorrências (eixos com chaves sem texto curado) |

## Critérios de aceite

| # | Critério | Resultado |
|---|---|---|
| V1 | % do SISVAN = bruto ÷ total × 100 em todos os anos (conferido por script contra as contagens) | |
| V2 | Textos curados com números do SISVAN batem com os % novos | |
| V3 | 2 mapas de número em Moradia: PNG, A4, `tabela_mapa_*`, site e PDF; classes discretas; bairros agrupados sem cor e com nota | |
| V4 | Nenhuma entrada de Inclusão/Moradia do crosswalk sem tabela no PDF; fonte do CadÚnico em `fontes.bib` | |
| V5 | `grep "IPS\|Índice de Progresso Social"` sem resultados nos arquivos publicados e nos leitores (fora de `specs/` históricos) | |
| V6 | Nenhum polígono de mapa em azul (PNG, A4, site); o mar continua azul | |
| V7 | 0 lorem nos eixos Inclusão e Moradia; todo número dos textos novos conferido na tabela de origem | |
| V8 | Site regerado: `confere_textos.py` sem erro; desktop e celular conferidos; orçamento de tamanho | |
| V9 | PDF regerado sem erro, **não publicado**; `relatorio/analise_primeira_infancia.pdf` não versionado | |
| V10 | `apresentacao/` sem mudança (`git diff --stat apresentacao/` vazio) | |
| V11 | ROADMAP, CLAUDE.md, especificação do projeto e skill `generate_map` atualizados | |
