# Desempenho do site (2026-09-30, branch `spec/desempenho_site`)

Pedido do usuário: (1) menos requisições ao Google Fonts, (2) JavaScript menor ou mais rápido, (3) carregamento mais
rápido. Rodada de teste: medir antes × depois, sem mudar o desktop (captura pixel a pixel, 1400 e 1280 px).

## Diagnóstico (medido, Chrome, 1400 px)

- Rede: 19 requisições, ~990 KB sem gzip (~400 KB com o gzip do Pages). Fontes: 1 CSS do Google + 4 woff2 (141 KB),
  e o CSS do Google vinha por `@import` dentro do `main.css` (cadeia HTML → main.css → Google CSS → woff2).
- **O gargalo não é o download, é o desenho**: 63.886 nós no DOM, 94% em abas ocultas (Prioridade sozinha: 24,7 mil
  elementos); 320 gráficos e 53 mapas (5.344 `<use>`) desenhados no carregamento; 3 listeners por região de mapa
  (~16 mil). Com CPU 4× (celular médio): script 1.115 ms, tarefa longa de 1.022 ms, DOMContentLoaded 1.911 ms.

## Feito

1. **Desenho por aba** (`js/charts.js`: `registra`, `abrePainel`, `preDesenha`, `montaRegioesDe`): gráfico e mapa de
   aba não aberta nascem quando a aba abre (`tabchange`, antes da rolagem ao alvo) ou no tempo ocioso depois do
   `load`, um por vez. Os dados continuam todos no carregamento — por isso o risco R1c da rodada
   `2026-09-24_website_refactor` (link `#eixo/h3` rolando antes de o dado chegar) não se aplica.
2. **Tooltip dos mapas por delegação** (`initMapTooltips`): 3 listeners por `<svg>`; região = `<use>` cujo id está
   em `GEO_NOMES`.
3. **Fontes do próprio site** (pedido do usuário depois da 1ª versão, que só trocou o `@import` por `<link>` +
   `preconnect`): `assets/fonts/*.woff2` — os mesmos arquivos que o Google Fonts entrega ao Chrome, subconjuntos latin
   e latin-ext com o `unicode-range` original, então só baixa o que a página usa — e os `@font-face` no `<style>` do
   `<head>` (fonte `website/build/fontes.css`, gerado por `baixa_fontes.py`). O workflow de deploy passou a aceitar
   `.woff2`. Licença: SIL OFL 1.1 (aviso no `<style>` e no `fontes.css`).
   **Sem `preload`**: medido (6 cargas, 4G simulado), o preload dos 4 woff2 levava a primeira pintura de ~290 para
   ~460 ms (disputava banda com o CSS); sem ele as fontes chegam ~90 ms depois e trocam pelo fallback (`swap`, como antes).

## Resultado (CPU 4× / rede "4G rápido" simulada)

| | antes | depois |
|---|---|---|
| Nós no DOM no carregamento | 63.886 | 10.391 (antes do tempo ocioso) |
| Tempo de script até o load | 1.115 ms | 118 ms |
| Maior tarefa longa | 1.022 ms | ~350 ms (o resto em fatias de ~50 ms) |
| DOMContentLoaded (CPU 4×) | 1.911 ms | 800-1.000 ms |
| DOMContentLoaded (rede) | ~1.240 ms | ~1.090 ms |
| Primeira pintura (mediana de 6) | ~430 ms | ~275 ms |
| Requisições (fontes) | 19 (5, em 2 origens de terceiros) | 18 (4, todas do próprio site) |
| Troca para Prioridade (depois do ocioso) | 158-215 ms | 148 ms |

Validação: capturas de todas as abas a 1400/1280 px idênticas às de antes (as únicas diferenças — sombra da barra
fixa e um trecho da Visão geral a 1280 — também variam entre duas execuções da versão antiga); 5 deep links na
mesma posição; tooltip nos 5 níveis (bairro, AP, RP, RA, CAP) e por toque no celular; CSV de todos os mapas;
Chrome, Firefox e WebKit a 1400, 768 e 390 px sem erro e sem rolagem horizontal. Scripts em `medicao/`.

## Não feito (e por quê)

- **Minificar o JS**: `js/*.js` somam 17 KB com gzip; minificado economizaria ~7 KB e criaria uma etapa de build,
  rejeitada em `2026-09-24_website_refactor` §4.9. O ganho real de JS era o tempo de execução (item 1).
- **Arredondar números de `data/charts.js`** (237 com 16 casas): 1,4 KB com gzip. Não compensa.
- **Tirar uma face** (ex. IBM Plex Mono 600, ou o eixo `opsz` da Fraunces) para ter 3 woff2: muda o desenho no desktop.

## Achado, fora do escopo

- Deep link `#alimentação/estado-nutricional-das-crianças-acompanhadas-sisvan`: o alvo termina a 15 px do topo, sob a
  barra fixa (59 px) — algo acima dele cresce 64 px depois da rolagem. Acontece igual na versão antiga (3 de 3 cargas).
