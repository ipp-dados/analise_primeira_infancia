# Tasks — SPEC-visual-identity

## Bloco 0 — Decisões
- [x] **T0.1** — Especificação e decisões A-F aprovadas pelo usuário (`specs.md` §4).
- [x] **T0.2** — Branch `spec/visual-identity` criada a partir de `spec/maps-and-ibge`.

## Bloco 1 — Módulo de estilo compartilhado (`analise.py`)
- [x] **T1.1** — Adicionadas `_PALETA_CATEGORICA`, `_CORES_TEMA_MAPA`,
      `_LIMIAR_DESTAQUE_SERIES`, `_N_SERIES_DESTACADAS`, `_COR_SERIE_APAGADA`,
      `_COR_FONTE_RODAPE`, `_rodape_fonte()` (plan.md §1).
- [x] **T1.2** — `serie_temporal` atualizada (fonte_dados, título serifado, DPI 200).
- [x] **T1.3** — `grafico_barra` atualizada (paleta do projeto no lugar de `'pastel'`, fonte_dados).
- [x] **T1.4** — `grafico_barra_agrupado` atualizada (paleta, fonte_dados).
- [x] **T1.5** — `serie_temporal_multipla` atualizada (paleta fixa por posição, lógica de
      destaque acima de 6 séries, `destaques=` opcional, fonte_dados).
- [x] **T1.6** — As 4 funções testadas isoladas com dado sintético (série simples, barra,
      barra agrupada, múltipla com ≤6 e com >6 séries) — todas geraram PNG válido; o caso
      >6 séries confirmado visualmente (4 linhas coloridas + "Outras (N)" em cinza).

## Bloco 2 — Mapas: `cmap` por tema (25 call sites)
- [x] **T2.1** — Tema `censo`: 4 call sites (Censo 0-4 anos bairro/AP/RP, abs+%).
- [x] **T2.2** — Tema `cadunico`: 3 call sites.
- [x] **T2.3** — Tema `natalidade`: 3 call sites.
- [x] **T2.4** — Tema `mortalidade`: 15 call sites.
- [x] **T2.5** — Confirmado por script que as 25 chamadas têm `cmap=_CORES_TEMA_MAPA[...]`
      (4+3+3+15=25, nenhuma sobrou no default `'Oranges'`). Inspeção visual do contraste sobre
      o basemap fica para o spot-check do Bloco 5 (depois da execução completa do notebook).

## Bloco 3 — `fonte_dados` + paleta nos ~48 call sites restantes
- [x] **T3.1** — Censo: `grafico_barra_agrupado` (SIDRA raça/sexo) → nova `fonte_sidra_censo`
      (distinta de `fonte_censo`, que é Data.Rio, não IBGE/SIDRA).
- [x] **T3.2** — CadÚnico: `grafico_barra` (4 chamadas, renda/idade) → `fonte_cadunico`
      (definição movida para o início da seção CadÚnico, antes do 1º uso).
- [x] **T3.3** — Nascidos vivos / baixo peso: `serie_temporal` (2) → `fonte_datasus_bairro`.
- [x] **T3.4** — Óbitos por raça / evitáveis (raça, grupo, subgrupo, 0-364/0-6/7-27/28-364,
      comparação por faixa, CAP, subgrupo×CAP): confirmado que raça/cor vem do Tabnet
      (`fonte_datasus_bairro`) e que grupo/subgrupo/CAP vêm do SIM/SVS-Rio TabWin — a
      constante `fonte_evitaveis_cap` (definida tarde demais, só na subseção CAP) foi
      **renomeada para `fonte_evitaveis`, movida para antes do 1º uso** (linha ~1414, antes da
      subseção de raça) e reaproveitada em todos os ~24 call sites evitáveis (séries + os 3
      mapas que já a usavam).
- [x] **T3.5** — Gravidez/puerpério/neonatal: `serie_temporal` (6) → `fonte_datasus_bairro`.
- [x] **T3.6** — SISVAN: nova `fonte_sisvan`; 3 `serie_temporal`.
- [x] **T3.7** — Cobertura vacinal: nova `fonte_cobertura_vacinal`; 1 `serie_temporal_multipla`
      + 1 `grafico_barra_agrupado`. SIDRA educação: nova `fonte_sidra_educacao`; 4
      `grafico_barra_agrupado`. PNAD: nova `fonte_pnad`; 1 `grafico_barra`. Matrículas: nova
      `fonte_matriculas`; 1 `serie_temporal`.
- [x] **T3.8** — Confirmado (fazia parte do levantamento acima).
- [x] **T3.9** — `grep -c "fonte_dados=" analise.py` = 78 = 5 assinaturas de função (`=None`
      nos 4 defs de gráfico + 1 no de mapa) + 73 call sites reais (25 mapas + 48 gráficos).
      Verificação programática confirmou 0 call sites sem `fonte_dados`.

## Bloco 4 — Destaque de séries com muitas linhas
- [x] **T4.1** — >6 séries confirmadas em: 4 gráficos "subgrupo" evitáveis (7 séries: 6
      subgrupos + `2.`), 2 "menores_5/extra" subgrupo (7 séries), ~27 gráficos "por CAP" (10
      séries), 1 cobertura vacinal (11 séries). Painéis por raça/cor ficaram em 6 séries — não
      disparam o destaque, como previsto no plan.md.
- [x] **T4.2** — Decisão: manter o destaque **automático** (top 4 pelo valor final) em todos os
      casos, inclusive cobertura vacinal. Motivo levantado ao checar os dados via um script
      Python solto: os nomes de coluna de `cobertura_vacinal_epi_por_ano.csv` apareciam com
      mojibake (`TR�PLICE VIRAL D1` etc.) mesmo lendo com `encoding='utf-8'` explícito — mas
      **isso era um artefato do meu script de diagnóstico** (não especificava o mesmo encoding
      que `carrega_cobertura_vacinal` usa em `analise.py`), confirmado no spot-check visual do
      Bloco 5: o gráfico real mostra "TRÍPLICE VIRAL D1" corretamente acentuado na legenda. Não
      era um risco real, mas a decisão de manter o automático continua válida por si só (top-4
      evidencia os imunobiológicos com maior cobertura corrente, sem curadoria arbitrária).
- [x] **T4.3** — Confirmado no Bloco 5: `obitos_causas_evitaveis_subgrupo_ano.png` (7 séries) e
      `cobertura_vacinal_epi_ano.png` (11 séries) renderizam corretamente com 4 linhas
      destacadas + "Outras (N)" em cinza.

## Bloco 5 — Validação completa do notebook
- [x] **T5.1** — `jupytext --sync` rodado (2x — ver nota abaixo).
- [x] **T5.2** — `jupyter nbconvert --to notebook --execute --inplace` a partir de kernel limpo — 0 erros, 138 células de código.
      **Achado real ao implementar:** a 1ª tentativa (executada com o processo indevidamente
      auto-desanexado do rastreamento do harness — ver nota) rodou sobre uma `analise.py`
      corrompida por um erro meu: um `Edit` do Bloco 3 removeu a linha `fonte_evitaveis_cap =
      '...'` junto com o marcador de célula `# %%` que a precedia, fundindo silenciosamente a
      célula de código seguinte (que definia `faixas_primeira_infancia`, `df_evitaveis_cap_faixa`
      etc.) dentro da célula de markdown anterior — o código virou comentário e nunca executou,
      causando `NameError: name 'df_evitaveis_cap_faixa' is not defined` mais adiante. Corrigido
      restaurando o `# %%` no lugar certo; varredura automática confirmou que nenhum outro
      `Edit` desta rodada cometeu o mesmo erro. Re-executado do zero com sucesso (138 células,
      0 erros, ordem cronológica de geração dos PNGs consistente com a ordem do arquivo).
- [x] **T5.3** — Script `nbformat` confirmou 0 células com `output_type == 'error'`.
- [x] **T5.4** — Spot-check visual: mapas dos 4 temas (censo=Blues, cadúnico=YlOrBr,
      natalidade=BuGn, mortalidade=RdPu) corretos; `obitos_causas_evitaveis_subgrupo_ano.png`
      (7 séries) e `cobertura_vacinal_epi_ano.png` (11 séries) com destaque automático
      funcionando; `cadunico_familias_por_idade.png` (barra simples) e
      `censo_sidra_populacao_0_6_raca_2022.png` (barra agrupada) com paleta/título/fonte
      corretos.

## Bloco 6 — `relatorio/` HTML (consolidação)
- [ ] **T6.1** — Extrair o motor JS (`lineChart`/`barChart`/`groupedBarChart`) e o esqueleto
      de tema claro/escuro de `lighter_index.html`/`white_index.html` para um template
      reaproveitável pelo novo script de build.
- [ ] **T6.2** — Escrever `.claude/skills/export_pdf_report/scripts/build_html_report.py`
      (plan.md §4.2): lê `tabelas_finais/*.csv`, monta o JSON por seção, renderiza 1
      `relatorio/index.html`.
- [ ] **T6.3** — Portar a lógica de destaque de séries (Bloco 4) para o `lineChart` do motor JS.
- [ ] **T6.4** — Adicionar seção "🗺️ Mapas" cobrindo os 25 mapas atuais (WebP ~1400px,
      mesma técnica já usada), agrupados por tema (natalidade/mortalidade/cadunico/censo).
- [ ] **T6.5** — Cada visualização com só título + fonte + alternância "ver tabela" — sem
      prosa/notas de método.
- [ ] **T6.6** — Rodar o script, gerar `relatorio/index.html`, abrir no navegador e conferir:
      tema claro/escuro automático, todas as ~35 visualizações novas presentes, tabela de
      dados funcionando em pelo menos 1 gráfico de cada tipo (linha simples, linha múltipla,
      barra, barra agrupada, mapa).
- [ ] **T6.7** — Remover `relatorio/lighter_index.html` e `relatorio/white_index.html` (arquivos
      antigos, substituídos pelo novo `index.html` consolidado) — local only, já fora do git.

## Bloco 7 — PDF
- [ ] **T7.1** — Rodar `regen_missing_pngs.py`, atualizar se necessário para as funções/
      esquemas de CSV que mudaram no Bloco 1-3.
- [ ] **T7.2** — Atualizar `extract_maps.py` para ler do novo `relatorio/index.html` único.
- [ ] **T7.3** — Atualizar `build_notebook_report.py` com as seções novas de `SPEC-maps-and-ibge`.
- [ ] **T7.4** — Rodar o pipeline completo até o Chrome headless (flags de segurança do
      `--user-data-dir` isolado, `--no-pdf-header-footer`).
- [ ] **T7.5** — Verificar contagem de páginas + rasterizar amostra (primeira, várias do meio,
      seção de mapas, última) e olhar as imagens.
- [ ] **T7.6** — Checar os modos de falha conhecidos da skill (ano com separador de milhar,
      tabela larga cortada, coluna de percentual na escala errada, header/footer do Chrome
      vazando, tema escuro vazando).
- [ ] **T7.7** — Copiar o PDF verificado para `relatorio/analise_primeira_infancia.pdf`.

## Bloco 8 — Documentação e fechamento
- [ ] **T8.1** — Atualizar `relatorio/specs.md` com a v5 (consolidação, script de build
      persistido, remoção da prosa) — seguindo o histórico "v1/v2/v3/v4" já documentado ali.
- [ ] **T8.2** — Atualizar `README.md` (changelog, versão).
- [ ] **T8.3** — Atualizar `feature_roadmap.md` se algo ficar de fora nesta rodada.
- [ ] **T8.4** — Fechar `tasks.md`/`validation.md`.
- [ ] **T8.5** — **Merge em `staging_main` (só após aval do usuário)** — nota: este merge e o
      de `spec/maps-and-ibge` (ainda pendente) precisam ser sequenciados; decidir com o
      usuário a ordem antes de mesclar qualquer um dos dois.
