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
| V1 | % do SISVAN = bruto ÷ total × 100 em todos os anos (conferido por script contra as contagens) | OK — `recalcula_percentuais_sisvan`; origem diverge em 3 casos (desnutrição 2023: 3,74 → 5,72%; sobrepeso total 2009: 8,71 → 15,64%; obesidade 2009: 0,07 → 7,00%) |
| V2 | Textos curados com números do SISVAN batem com os % novos | OK — só o texto de obesidade citava valor errado (frase de 2009 retirada; status "atualizado"); desnutrição e sobrepeso conferidos |
| V3 | 2 mapas de número em Moradia: PNG, A4, `tabela_mapa_*`, site e PDF; classes discretas; bairros agrupados sem cor e com nota | OK — `mapa_cadunico_{inadequacao,adensamento}_n_bairro_2026` (PNG + A4 PDF), crosswalk, site (2 blocos, desktop e celular) e PDF; rodapé próprio (o da taxa não vale para contagem) |
| V4 | Nenhuma entrada de Inclusão/Moradia do crosswalk sem tabela no PDF; fonte do CadÚnico em `fontes.bib` | OK — 9 entradas novas em `AJUSTES`; `mds_cadunico` passa a jul/2026; nota de agregação cita RA ou AP |
| V5 | `grep "IPS\|Índice de Progresso Social"` sem resultados nos arquivos publicados e nos leitores (fora de `specs/` históricos) | OK — restam só 2 menções explicativas (docstring de `protecao.py` e nota do crosswalk: a planilha vem do IPS, a citação é o ISP, como no catálogo da equipe) |
| V6 | Nenhum polígono de mapa em azul (PNG, A4, site); o mar continua azul | OK — todos os mapas usam `_CORES_TEMA_MAPA`; site: fills mais azulados são tons de `Purples` (~250°, violeta), conferidos na imagem |
| V7 | 0 lorem nos eixos Inclusão e Moradia; todo número dos textos novos conferido na tabela de origem | OK — Inclusão e Moradia sem lorem nos blocos de figura e tabela (achados, introdução e síntese dos eixos seguem em lorem: rodada da versão final); 11 textos com "Conferido em"; texto do mapa de deficiência ajustado ("com valor próprio": um conjunto agregado tem 2,3%) |
| V8 | Site regerado: `confere_textos.py` sem erro; desktop e celular conferidos; orçamento de tamanho | OK — `confere_textos.py` (corrigido: status ATENÇÃO faltava na ordem); Edge 1366 e 390 px sem erro de console nem rolagem horizontal; 1,44 MB publicados |
| V9 | PDF regerado sem erro, **não publicado**; `relatorio/analise_primeira_infancia.pdf` não versionado | OK — `gera_latex.py` sem `--publicar` (base Python: o env `analises_env` não tem `svgelements`); 0 referências indefinidas; os 11 textos no capítulo; aviso "sem figura" deixou de contar `tabela_no_texto` |
| V10 | `apresentacao/` sem mudança (`git diff --stat apresentacao/` vazio) | OK — `git diff --stat apresentacao/` vazio |
| V11 | ROADMAP, CLAUDE.md, especificação do projeto e skill `generate_map` atualizados | OK |
