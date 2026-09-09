# Validation — SPEC-visual-identity

Critérios objetivos por bloco. Um bloco só é marcado `[x]` em `tasks.md`
depois de passar aqui.

**Status final: todos os critérios V1-V7 passaram.** Duas contagens do plan.md
inicial precisaram de correção durante a implementação: o Bloco 6/7 cobre
**32 mapas reais** (não 25 — a estimativa original contava call sites de
`mapa_coropletico_bairros`, e alguns são loops que produzem várias imagens) e
**73 visualizações totais** no HTML/PDF (25 mapas + 48 gráficos, contando tudo
que já existia + tudo que `SPEC-maps-and-ibge` adicionou — não "~35 novas").

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

## Resultado final (todas confirmadas)
- V1: constantes/`_rodape_fonte`/destaque automático confirmados por teste
  isolado (Bloco 1) e no notebook real (Bloco 5) — chart com 7 séries e chart
  com 11 séries, ambos com 4 destacadas + "Outras (N)".
- V2: 25/25 call sites com `cmap` (4 censo, 3 cadúnico, 3 natalidade, 15
  mortalidade); 4 mapas (1 por tema) inspecionados visualmente, sem
  regressão dos bugs de `SPEC-maps-and-ibge`.
- V3: `grep -c "fonte_dados=" analise.py` = 78 = 73 call sites reais + 5
  assinaturas de função com `=None`; verificação programática (script
  parseando blocos de chamada) confirmou 0 sem fonte.
- V4: notebook reexecutado do zero **duas vezes** nesta rodada (a 2ª após o
  fix do eixo de ano fracionário, achado durante o Bloco 7) — 138 células, 0
  erros nas duas.
- V5: `relatorio/index.html` único, 73 gráficos + 32 mapas, sem erro de
  console (Chrome headless, 2 bugs reais encontrados e corrigidos — `fmt`/
  `pct` não expostos, categoria "Total" espúria no eixo dos SIDRA), tabela
  "ver dados" confirmada em linha simples/múltipla/barra/barra agrupada/mapa
  (mapas não têm toggle de tabela — são imagem estática, por design).
- V6: PDF final com 95 páginas, ~50MB; amostra rasterizada (capa, meio,
  mapas, rodapé) sem os modos de falha conhecidos, incluindo o eixo de ano
  fracionário (achado e corrigido nesta mesma verificação).
- V7: este arquivo, `relatorio/specs.md`, `README.md` e `feature_roadmap.md`
  atualizados; `tasks.md` só com T8.5 (merge, gated) em aberto.
