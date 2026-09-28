# Validação — `specs/2026-09-28_melhorias_site`

Escrita antes da implementação; resultados preenchidos no fechamento.

| # | Verificação | Como | Resultado |
|---|---|---|---|
| V1 | Favicon: SVG, `.ico` e `apple-touch-icon` publicados e referenciados | arquivos + `<head>` gerado | |
| V2 | 6 aberturas de eixo no site, no PDF e no DOCX, ≤ 100 palavras, abaixo de "Principais achados" | contagem no HTML, texto do PDF, bookmarks do DOCX | |
| V3 | Nenhum lorem > 150 palavras (site, PDF, DOCX) | script: blocos lorem de cada artefato | |
| V4 | `textos_curados.json` sem alteração; sincronização do DOCX regenerado não muda nenhuma chave | diff + `sincroniza_docx.coleta_edicoes` | |
| V5 | Sem botão "Linhas"; painéis iguais | busca no DOM + capturas | |
| V6 | `index.html` < 300 KB (meta 250 KB) | tamanho | |
| V7 | Bloco 5 sem mudança visual: capturas 1400/390 px iguais pixel a pixel às intermediárias | Playwright + comparação | |
| V8 | `outerHTML` de cada SVG de mapa igual ao intermediário; CSV de cada mapa igual byte a byte | Playwright | |
| V9 | Mudanças visuais dos blocos 1-4 só onde esperado | capturas antes × intermediárias, conferidas à mão | |
| V10 | Textos curados publicados | `valida_textos_publicados.py` | |
| V11 | Site estático: só extensões permitidas, sem `fetch`, orçamento de tamanho | `build_site.py` (avisos) + workflow | |
