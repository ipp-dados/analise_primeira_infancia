# Validation — SPEC-visual-identity

Critérios objetivos por bloco. Um bloco só é marcado `[x]` em `tasks.md`
depois de passar aqui.

## V1 — Módulo de estilo compartilhado
- Novas constantes (`_PALETA_CATEGORICA`, `_CORES_TEMA_MAPA`,
  `_LIMIAR_DESTAQUE_SERIES`, `_N_SERIES_DESTACADAS`, `_COR_SERIE_APAGADA`,
  `_COR_FONTE_RODAPE`) existem em `analise.py` e `_rodape_fonte` roda sem erro
  com `fonte_dados=None` e com uma string.
- As 4 funções aceitam `fonte_dados=None` por padrão (nenhuma chamada
  existente quebra antes do Bloco 3 adicionar o argumento de verdade).
- `serie_temporal_multipla` com >6 colunas produz exatamente
  `_N_SERIES_DESTACADAS` linhas coloridas + 1 entrada de legenda "Outras (N)"
  representando o resto; com ≤6 colunas, comportamento idêntico ao anterior
  (todas coloridas, todas na legenda).

## V2 — Mapas por tema
- Todas as 25 chamadas de `mapa_coropletico_bairros` têm `cmap` explícito
  (nenhuma mais usa o default `'Oranges'`), com o tema batendo a tabela do
  plan.md §2.
- Inspeção visual de pelo menos 1 mapa por tema (4 no total): classe mais
  clara da legenda ainda legível sobre o basemap; classe mais escura não
  satura a ponto de esconder o contorno dos bairros/CAPs.
- Nenhum mapa quebra com `ValueError: Bin edges must be unique` ou `cannot
  convert float NaN to integer` (regressão dos bugs já corrigidos em
  `SPEC-maps-and-ibge` — trocar só o `cmap` não deveria afetar isso, mas
  confirmar).

## V3 — `fonte_dados` nos 73 call sites
- `grep -c "fonte_dados=" analise.py` conta 73 ocorrências (25 mapas + 48
  gráficos) — nenhum call site das 5 funções estilizáveis ficou sem fonte.
- Nenhuma string de fonte foi inventada solta dentro de uma chamada — toda
  vem de uma constante `fonte_*` definida perto de onde os dados da seção
  são carregados (mesmo padrão dos mapas).

## V4 — Notebook completo
- `jupyter nbconvert --to notebook --execute --inplace` a partir de kernel
  limpo termina com **0 células com erro** (mesmo padrão de validação das
  rodadas anteriores).
- Contagem de células de código não caiu (nenhuma célula foi perdida na
  edição em massa dos ~73 call sites).
- Spot-check visual (T5.4) confirma: título serifado + bold, rodapé "Fonte:
  ..." visível, paleta de 11 cores aplicada (não mais o ciclo default do
  matplotlib nem `palette='pastel'` genérico do seaborn).

## V5 — `relatorio/index.html` (consolidado)
- Um único arquivo (`lighter_index.html`/`white_index.html` removidos).
- Abre no navegador sem erro de console; alterna tema claro/escuro sozinho
  conforme `prefers-color-scheme` do SO (sem precisar de toggle manual, a
  menos que os arquivos antigos já tivessem um — nesse caso manter o
  comportamento existente).
- Contém as ~35 visualizações novas de `SPEC-maps-and-ibge` (11 mapas de
  bairro, 2 mapas de subgrupo/CAP, 6 gráficos SIDRA, 22 séries de evitáveis)
  — conferir contagem de elementos de gráfico/mapa na página contra a
  contagem de `savefig`/`mapa_coropletico_bairros` em `analise.py`.
- Nenhuma seção tem texto de nota/metodologia além de título + fonte (B).
- Pelo menos 1 gráfico de cada tipo (linha simples, linha múltipla, barra,
  barra agrupada, mapa) tem a alternância "ver tabela" funcionando.
- Seção "🗺️ Mapas" mostra os mapas agrupados por tema, com as cores novas
  (não mais todos em laranja).

## V6 — PDF
- `pypdf` reporta uma contagem de páginas condizente com o aumento de
  conteúdo (mais alta que a versão anterior, dado ~35 visualizações novas).
- Amostra rasterizada (primeira página, 3-4 páginas do meio, seção de
  mapas, última página) inspecionada visualmente — sem os modos de falha
  conhecidos listados em T7.6.
- `relatorio/analise_primeira_infancia.pdf` reflete o novo estilo (paleta,
  cmap por tema, rodapés de fonte) porque foi gerado **depois** do Bloco 5.

## V7 — Documentação
- `relatorio/specs.md` tem uma entrada "v5" descrevendo a consolidação.
- `README.md` e `feature_roadmap.md` refletem o estado final.
- `tasks.md` só tem T8.5 (merge) em aberto ao final.
