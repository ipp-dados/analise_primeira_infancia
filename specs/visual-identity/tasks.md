# Tasks — specs/visual-identity

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
- [x] **T6.1** — Motor JS (`lineChart`/`barChart`/`groupedBarChart`, `fmt`/`pct`/`svgEl`/`byId`)
      e o CSS de tema claro/escuro extraídos de `lighter_index.html` via `Grep` (o arquivo tem
      uma linha de ~3MB com os mapas em base64 que estoura o limite do `Read` — contornado lendo
      só os trechos de código via `Grep -A`).
- [x] **T6.2** — `.claude/skills/export_pdf_report/scripts/build_html_report.py` escrito: lê
      `tabelas_finais/*.csv` direto (sem um blob `DATA` intermediário — cada chamada
      `line_chart`/`bar_chart`/`grouped_bar_chart` já embute os arrays literais na chamada JS),
      resolve os mapas via Pillow (resize + WebP), renderiza 1 `relatorio/index.html`.
      **Achado real ao implementar:** `fmt`/`pct` (usados dentro das funções `format` passadas a
      cada série) não estavam expostos em `window`, só `byId`/`lineChart`/`barChart`/
      `groupedBarChart` — como as chamadas de render ficam num `<script>` (IIFE) separado do
      motor, isso gerava `ReferenceError: fmt is not defined` em todo gráfico com formatação
      customizada. Corrigido expondo `window.fmt`/`window.pct` também.
- [x] **T6.3** — Lógica de destaque portada para `lineChart`: series >6 → top 4 pelo último
      valor não-nulo coloridas (com rótulo/legenda), resto em linha cinza fina sem rótulo, 1
      entrada de legenda "Outras (N)".
- [x] **T6.4** — Seção "🗺️ Mapas" com as **32** imagens reais em `mapas/*.png` (não 25 — a
      estimativa do plan.md contava call sites, não imagens renderizadas; alguns call sites são
      loops que produzem várias imagens), agrupadas em 7 blocos temáticos.
- [x] **T6.5** — Todas as ~73 visualizações (48 gráficos + a cobertura completa de
      specs/maps-and-ibge: SIDRA, evitáveis por CAP/subgrupo, D.1/D.2, raça sem "não informada")
      com só título + fonte + alternância "ver tabela" — sem prosa.
- [x] **T6.6** — Gerado e validado com Chrome headless (`--screenshot`, sem servidor/browser
      interativo disponível neste ambiente): 0 erros de console (2 rodadas, 1 bug real
      encontrado e corrigido — ver T6.2); spot-check visual no topo (Censo, tabela+gráficos),
      meio (evitáveis por CAP, destaque de 10 séries) e final (mapas + rodapé) da página — tema
      escuro automático aplicado corretamente (ambiente sem preferência clara), paleta/fontes
      consistentes com o notebook.
      **Achado real ao implementar:** os gráficos de barra agrupada por idade/raça e
      idade/sexo (SIDRA Censo e SIDRA educação) inicialmente incluíam uma categoria "Total"
      espúria no eixo X — a versão matplotlib evitava isso via `order=_ORDEM_IDADE_SIDRA_0_6`
      (que o `sns.barplot` usa para *filtrar*, não só ordenar); replicado no gerador Python
      filtrando+reordenando pelas mesmas 3 listas de idade que `analise.py` já usa.
- [x] **T6.7** — `relatorio/lighter_index.html` e `relatorio/white_index.html` removidos (local
      only, já fora do git); `relatorio/index.html` agora é o único arquivo, gerado pelo script.

## Bloco 7 — PDF
- [x] **T7.1** — Não necessário: a execução completa do notebook no Bloco 5 já regenerou
      todos os PNGs (74 em `visualizacoes/`, incluindo tudo que `specs/maps-and-ibge` adicionou)
      com o estilo novo — nada para `regen_missing_pngs.py` preencher.
- [x] **T7.2** — `extract_maps.py` **descontinuado** (não atualizado): ele lia um `const MAPS =
      [...]` de um `relatorio/*.html`, mas o novo `relatorio/index.html` (Bloco 6) embute mapas
      como `<img>` direto, sem esse array JS. `build_notebook_report.py` agora resolve/
      redimensiona `mapas/*.png` sozinho (`map_card()`, mesma técnica Pillow/WebP do Bloco 6) —
      elimina a dependência entre os dois scripts.
- [x] **T7.3** — `build_notebook_report.py` atualizado com as seções que faltavam: SIDRA Censo
      (raça/sexo), raça sem "não informada" (Componente E), a subseção inteira de evitáveis por
      CAP (panorama municipal, por subgrupo×CAP×faixa, grupo evitável por CAP, gestação/parto),
      SIDRA educação (4 gráficos), e a galeria de mapas expandida de 5 para as 32 imagens reais
      (7 grupos temáticos, mesmo agrupamento do Bloco 6).
- [x] **T7.4** — Pipeline rodado até o PDF (1ª passada, antes do achado de T7.6 abaixo).
      **Achado real ao implementar:** a primeira tentativa gerou um PDF de 25KB (1 página,
      "ERR_FILE_NOT_FOUND") — a URL `file:///$SCRATCH/...` estava malformada porque `$SCRATCH`
      já é um caminho POSIX (`/c/Users/...`), resultando em 4 barras (`file:////c/Users/...`)
      em vez de `file:///C:/Users/...`. Corrigido convertendo para o caminho Windows via
      `cygpath -m` antes de montar a URL. PDF dessa passada: 95 páginas, ~50MB.
- [x] **T7.5** — `pypdf`/`PyMuPDF` não estavam instalados no ambiente (instalados agora,
      registrar em `requirements.txt` no Bloco 8) — contagem de páginas confirmada (95),
      amostra rasterizada (capa, meio com tabela CAP 10-colunas, mapas, última página/rodapé)
      e inspecionada visualmente.
- [x] **T7.6** — **Achado real ao implementar** (durante a inspeção de T7.5): um dos gráficos
      novos (evitáveis por subgrupo×CAP) mostrava ticks fracionários no eixo de ano ("2007.5",
      "2010.0"...) — o mesmo modo de falha "ano com eixo numérico contínuo" já documentado na
      skill, mas nunca antes visível porque as séries mais antigas (1996-2025) por coincidência
      caem em intervalos redondos no locator automático do matplotlib; as novas (2006-2025) não.
      Bug pré-existente em `serie_temporal`/`serie_temporal_multipla` desde antes desta rodada
      — corrigido com `plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))`
      (preserva o adensamento automático de ticks para séries longas, só proíbe posições
      fracionárias, ao contrário de forçar eixo categórico, que lotaria de rótulos uma série de
      30 anos). Notebook reexecutado do zero para regenerar todos os PNGs afetados (em
      andamento) — HTML e PDF precisam ser regenerados de novo depois, e a amostra revisada
      mais uma vez para confirmar o fix e checar os demais modos de falha conhecidos (milhar em
      `ano`, tabela larga cortada, percentual em escala errada, header/footer do Chrome, tema
      escuro vazando).
- [x] **T7.7** — HTML e PDF regenerados após o fix do eixo de ano (`analise.ipynb` reexecutado
      do zero, 138 células, 0 erros). PDF final: 95 páginas, ~50MB, verificado (contagem de
      páginas + amostra rasterizada incluindo a página antes afetada pelo bug do eixo —
      confirmado corrigido) e copiado para `relatorio/analise_primeira_infancia.pdf`. Este
      arquivo **não** está no `.gitignore` (ao contrário de `relatorio/*.html`) — perguntar ao
      usuário antes de commitar, por ser um binário de ~50MB (dobrou de tamanho em relação à
      versão anterior por causa dos 32 mapas em vez de 5).

## Bloco 8 — Documentação e fechamento
- [x] **T8.1** — `relatorio/specs.md` atualizado com a entrada "v5" (Bloco 6).
- [x] **T8.2** — `README.md` atualizado: "Estrutura do Projeto" (bullet `relatorio/`
      reescrito para o arquivo único), novo bloco "Notable code changes (2026-09-09) —
      identidade visual unificada...", linha `0.16.0` na Update Table.
- [x] **T8.3** — `feature_roadmap.md`: item "Refactor architecture" já estava registrado
      (rodada anterior); adicionado nesta rodada o pedido do usuário de converter o export em
      PDF para LaTeX, para depois desta spec.
- [x] **T8.4** — `tasks.md`/`validation.md` fechados.
- [x] — `requirements.txt`: adicionadas `pymupdf`/`pypdf` (usadas para verificar o PDF —
      instaladas neste ambiente durante o Bloco 7, não estavam registradas antes).
- [ ] **T8.5** — **Merge em `staging_main` (só após aval do usuário)** — nota: este merge e o
      de `spec/maps-and-ibge` (ainda pendente) precisam ser sequenciados; decidir com o
      usuário a ordem antes de mesclar qualquer um dos dois. **Além disso**, o usuário precisa
      decidir se quer commitar o novo `relatorio/analise_primeira_infancia.pdf` (~50MB, não
      ignorado pelo git, dobrou de tamanho por causa dos 32 mapas em vez de 5) — ver
      `export_pdf_report/SKILL.md` §6.
