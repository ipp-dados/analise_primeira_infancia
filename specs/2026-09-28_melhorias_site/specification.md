# Especificação — `specs/2026-09-28_melhorias_site`

Decisões e contexto em `plan.md`. Uma seção por bloco; cada uma diz o que muda, onde, e o critério de aceite
(verificado em `validation.md`).

## 1. Favicon (U1)

- Opções desenhadas em SVG, legíveis a 16 × 16 px, na paleta do IPP (azul `#004a80` / ciano `#00aeef`), sem texto
  pequeno; o usuário escolhe uma. Enquanto não escolhe, fica a recomendada (a primeira da lista em `favicon_opcoes/`).
- Arquivos publicados: `assets/images/favicon.svg` (navegadores modernos), `favicon.ico` na raiz do site (16/32/48,
  navegadores e ferramentas que pedem `/favicon.ico`), `assets/images/apple-touch-icon.png` (180 × 180, fundo
  opaco). `<link>`s no `<head>` gerado com `?v=<md5>`; o `.ico` e o PNG são gerados do SVG por script
  (`website/build/gera_favicon.py`), não à mão.
- Aceite: os três arquivos existem, o `<head>` os referencia, o workflow de deploy aceita `.ico`.

## 2. Texto de abertura do eixo (U2)

- `blocos_relatorio()` (`.claude/skills/export_pdf_report/scripts/gera_estrutura_eixos.py`) ganha, por eixo,
  `introducao_<eixo>` (`rotulo="Introdução do eixo — <título>"`, 90 palavras, 1 linha), **depois** de `achados_<eixo>`.
- Site (`build_site.py`): parágrafo logo abaixo do callout "Principais achados" (`<p class="eixo-intro">`), texto
  curado se houver, senão lorem de 90 palavras com semente `introducao-<sid>` (mesma do PDF).
- PDF (`gera_latex.py`): parágrafo logo depois do ambiente `achados`, antes da primeira seção; entra na lista
  "textos em lorem" do build.
- DOCX (`gera_docx_curadoria.py`): bloco com bookmark `introducao_<eixo>` logo depois de "Principais achados";
  `sincroniza_docx.py` já trata qualquer chave de `blocos_relatorio()`.
- Aceite: 6 aberturas no site, 6 no PDF, 6 bookmarks novos no DOCX; ≤ 100 palavras cada.

## 3. Lorem ≤ 150 palavras (U3)

- `_lorem` (site), `lorem` (LaTeX) e `_lorem` (DOCX): faixa padrão `randint(100, 150)` (semente inalterada).
- `resumo` 250 → 150 (site não tem; LaTeX `texto("resumo", …)`; DOCX `blocos_relatorio`); Introdução 250 → 150 e
  Considerações finais 300 → 150 nos placeholders (hoje curadas — só vale se voltarem a ficar vazias), inclusive a
  comparação de `sincroniza_docx.py`.
- DOCX regenerado com o lorem antigo descartado (`gera_docx(docx_anterior=…)` passa a ignorar texto que
  `_eh_lorem` reconhece), para o placeholder novo entrar e a sincronização não o tomar por edição.
- Aceite: nenhum bloco lorem > 150 palavras no site, no PDF e no DOCX; `textos_curados.json` inalterado; a
  sincronização do DOCX regenerado não muda nenhuma chave.

## 4. Pequenos múltiplos só com Painéis (U4)

- `js/charts.js`, `pequenosMultiplos`: sai o controle `.sm-ctrl` e a vista de linhas (não é mais desenhada); a
  tabela de dados (`opts.table`) continua; `container._vista` deixa de existir. CSS `.sm-ctrl` removido
  (`components.css`, `mobile.css`).
- Aceite: nenhum botão "Linhas" no site; os painéis iguais aos de antes.

## 5. HTML menor (U5)

Nada muda na tela; o DOM depois do JavaScript é o mesmo.

- **Mapas**: `mapa_svg()` deixa de escrever os `<use>` no HTML. Cada `<svg class="map-svg">` sai vazio com
  `data-mapa="<id>"` (e os overlays de rosa dos ventos/escala, que continuam no HTML); os dados vão para
  `window.MAPAS` em `data/charts.js`: nível geográfico, paleta do mapa (lista de cores únicas), índice de cor por
  região, texto do tooltip por região, valor bruto por região (CSV). `js/charts.js` insere os `<use>` na mesma ordem
  e com os mesmos atributos, antes do overlay, no carregamento (todos os mapas, sem esperar a aba — como hoje, que já
  estão no DOM).
- **CSV dos mapas**: gerado no clique a partir de `window.MAPAS` (nomes das regiões de `GEO_NOMES`, valores com a
  mesma formatação pt-BR de `_csv_data_attr`); o `data-csv` sai do HTML dos mapas. CSVs dos gráficos continuam.
- **Ícones**: `icone()` passa a emitir `<svg class="icon" …><use href="#i-<nome>"/></svg>`; um único bloco
  `<svg hidden>` com um `<symbol>` por ícone usado, no início do `<body>`.
- **Números**: floats de `data/charts.js` com no máximo 4 algarismos significativos depois da vírgula que importam
  para o desenho (arredondar a 4 casas decimais; valores exibidos já são formatados com 0-2 casas).
- Aceite: `index.html` < 300 KB (meta 250 KB); capturas de todas as abas a 1400 px e 390 px iguais pixel a pixel às
  capturas feitas depois dos blocos 1-4 (para isolar o bloco 5); `outerHTML` dos SVGs de mapa iguais; CSVs iguais.
