# Validação — `specs/2026-09-28_melhorias_site`

Escrita antes da implementação; resultados preenchidos no fechamento (2026-09-28). Capturas com Playwright (Chrome
instalado, `channel="chrome"`), todas as abas, página inteira, a 1400 px e 390 px: **antes** (`staging_main`
2702ef9), **intermediárias** (blocos 1-4 prontos) e **finais** (bloco 5 pronto).

| # | Verificação | Como | Resultado |
|---|---|---|---|
| V1 | Favicon: SVG, `.ico` e `apple-touch-icon` publicados e referenciados | arquivos + `<head>` gerado | **OK** — `assets/images/favicon.svg` (opção A, 477 B), `favicon.ico` (16/32/48, 2,2 KB), `assets/images/apple-touch-icon.png` (180 px, 2,8 KB); três `<link>` com `?v=`; `.ico` aceito no workflow e no relatório de tamanho |
| V2 | 6 aberturas de eixo no site, no PDF e no DOCX, ≤ 100 palavras, abaixo de "Principais achados" | contagem no HTML, texto do PDF, bookmarks do DOCX | **OK** — 6 × 90 palavras no site, o mesmo texto nas 6 no PDF, 6 bookmarks `introducao_<eixo>` novos no DOCX; posição conferida na captura (logo abaixo do callout) |
| V3 | Nenhum lorem > 150 palavras (site, PDF, DOCX) | script: blocos lorem de cada artefato | **OK** — máximo 150 no site (93 blocos), 143 no PDF, 150 no DOCX (57 blocos) |
| V4 | `textos_curados.json` sem alteração; sincronização do DOCX regenerado não muda nenhuma chave | diff + `sincroniza_docx.coleta_edicoes` | **OK** — JSON idêntico; 77 blocos curados do DOCX anterior intactos; `coleta_edicoes` do DOCX novo: 0 diferenças com o JSON |
| V5 | Sem botão "Linhas"; painéis iguais | busca no DOM + capturas | **OK** — 0 botões "Linhas"; os cartões de pequenos múltiplos perdem só a linha do controle |
| V6 | `index.html` < 300 KB (meta 250 KB) | tamanho | **Parcial** — 785 → **343 KB** (−56 %; gzip 128 → 66 KB); total publicado 1.393 → 1.052 KB. O que resta: legendas dos mapas (35 KB), CSV dos gráficos (42 KB), sumários desktop + celular (27 KB), textos. Mover o CSV dos gráficos para o JS só trocaria bytes de arquivo, sem reduzir o site; ficou de fora |
| V7 | Bloco 5 sem mudança visual: capturas 1400/390 px iguais pixel a pixel às intermediárias | Playwright + comparação | **OK** — 1400 px: 6 abas idênticas; Proteção com 1.228 px de diferença ≤ 3/255 (mapas por RA com camadas semitransparentes; `outerHTML` idêntico, é composição da GPU). 390 px: diferenças só em y 268-389 (barra fixa "Nesta seção"), que também aparecem entre duas capturas do mesmo build |
| V8 | `outerHTML` de cada SVG de mapa igual ao intermediário; CSV de cada mapa igual byte a byte | Playwright | **OK** — 56/56 SVGs com `outerHTML` idêntico; 56/56 CSVs idênticos; tooltip conferido (região → nome + valor) |
| V9 | Mudanças visuais dos blocos 1-4 só onde esperado | capturas antes × intermediárias, conferidas à mão | **OK** — aberturas dos eixos, lorem mais curto (páginas mais baixas), controle de pequenos múltiplos removido |
| V10 | Textos curados publicados | `valida_textos_publicados.py` | **OK** — 0 ausentes |
| V11 | Site estático: só extensões permitidas, sem `fetch`, orçamento de tamanho | `build_site.py` (avisos) + workflow | **OK** — sem `AVISO`; duas gerações seguidas com md5 idênticos; nenhum erro de JS no console |

Notas:
- Arredondar os floats longos de `data/charts.js` (4 casas, só quando o valor exibido não muda) foi implementado e
  **revertido**: mudava o antialiasing de algumas linhas (subpixel) por ~3 KB. Ficou só `2000.0` → `2000`.
- Uma captura de 1400 px saiu com a fonte web ainda carregando (diferença em todo texto); refeita, bateu. Vale para a
  próxima rodada: esperar `document.fonts.ready` antes de capturar.
