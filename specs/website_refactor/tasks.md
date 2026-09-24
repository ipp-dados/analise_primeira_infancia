# Tasks: specs/website_refactor

Um commit por bloco. Marcar `[x]` só depois da verificação correspondente em `validation.md`. Decisões em
`specification.md` §3, blocos em `plan.md`.

## Bloco 0: Abertura e baseline

- [x] **T0.1**: Pedido lido (`prompt_html_review.md`), levantamento do gerador e do HTML atual (spec §2).
- [x] **T0.2**: D1-D4 aprovadas pelo usuário (2026-09-24): gerador em `website/build/`, geometria
  compartilhada, Visão geral + 6 abas, restyle mantendo fontes.
- [x] **T0.3**: Branch `spec/website-refactor` criada a partir de `planning`.
- [x] **T0.4**: Ok do usuário em `specification.md` + `plan.md` ("ok, move ahead", 2026-09-24).
- [x] **T0.5**: Baseline (checksums, contagens, DOM renderizado, captura) — V0. Playwright ausente: fica para o checkpoint do Bloco 4.

## Bloco 1: Mover o gerador

- [x] **T1.1**: `git mv` para `website/build/build_site.py`.
- [x] **T1.2**: `ROOT`/`chdir`, `sys.path` para `gera_estrutura_eixos`, saída padrão `website/index.html`; caminho de saída relativo ao cwd de quem chama. `sincroniza_docx.py` já aponta para o novo script (destino muda no Bloco 7).
- [x] **T1.3**: Saída byte-idêntica à baseline (V1).

## Bloco 2: Extrair CSS/JS/dados

- [x] **T2.1**: `css/main.css`, `css/layout.css`, `css/components.css` a partir da string `CSS`.
- [x] **T2.2**: `js/charts.js` a partir de `ENGINE`; `data/charts.js` a partir de `RENDER_CALLS`.
- [x] **T2.3**: Logo para `assets/images/` por `<img src>`; `<!doctype>`, `lang`, `charset`, `viewport`.
- [x] **T2.4**: DOM e estilos iguais à baseline (V2). Argumento do gerador passou a ser a *pasta* de saída (copia `css/js/assets` quando não é `website/`); `sincroniza_docx.py` já chama sem argumento. `index.html`/`data/` gerados só entram no git no Bloco 3b (evita mais uma cópia de 20 MB no histórico).

## Bloco 3: Geometria compartilhada

- [x] **T3.1**: `data/geo.js` com `<defs>` por nível (230 paths, só níveis usados); mapas com `<use>` (7.107).
- [x] **T3.2**: Fundo cartográfico em `assets/images/basemap-<hash da bbox>.jpg`, reaproveitado se existir (saída determinística, geração offline).
- [x] **T3.3**: Hover/tooltip/outliers nos 5 níveis; capturas iguais (V3). CSV não muda (gerado em Python, sem geometria).

## Bloco 3b: Redução de tamanho (D5)

- [x] **T3b.1**: `coverage_simplify`, tolerância 0,3; paths relativos com 1 casa decimal.
- [x] **T3b.2**: `stroke` no CSS; nomes em `window.GEO_NOMES`; ids curtos (`#gb12`).
- [~] **T3b.3**: **Não feito, por decisão medida** (spec §4.9): variantes custam 0,21 MB / ~30 KB gzip.
- [~] **T3b.4**: **Não feito, por decisão medida** (spec §4.9): dados somam 109 KB / 17 KB gzip.
- [x] **T3b.5**: Relatório de tamanho (bruto e gzip) + `AVISO` de orçamento no gerador; 1,33 MB publicado (V3b).
- [x] **T3b.6** *(achado)*: AP/RP/RA dissolvidos têm furinhos brancos (anéis internos minúsculos que sobram do dissolve de bairros que não fecham perfeitamente) — já existiam na baseline. Corrigido no Bloco 6 (`_fecha_frestas`): furo que nenhuma outra região cobre é preenchido, enclave real fica. Anéis: AP 629→135, RP 505→145, RA 448→164, bairro 302→298, CAP 144→140.

## Bloco 4: Protótipo

- [x] **T4.1**: Tokens em `website/build/prototype/css/` (raios 8/14/20, 2 sombras, espaçamento 4-64, fundo `#F3F5F8` + cartões brancos, acento azul IPP `#0A5A99`); contraste AA medido (V4).
- [x] **T4.2**: `website/build/prototype/make_prototype.py` → `prototype/index.html` com pedaços reais (9 gráficos, mapa com pills, pendente, nota, fontes). `js/navigation.js` e `js/sidebar.js` já escritos (reais) e usados pelo protótipo; ícones Lucide em `assets/icons/`. Capturas via DevTools Protocol (script no scratchpad; a captura por linha de comando do Chrome não serve para página rolada).
- [x] **T4.3**: Aprovado com ajustes (2026-09-24) — conclusões por eixo, banner com links (GitHub, PDF, data) no lugar da descrição, logo em resolução maior, "Fale Conosco" no roadmap, título "Diagnóstico da Primeira Infância Carioca" em 2 linhas (spec D6). Rótulo curto na aba ("Prioridade"), título completo no h2.

## Bloco 5: Abas e conteúdo

- [x] **T5.1**: Coletor de fontes por h2 + caixa "FONTES DESTA SEÇÃO".
- [x] **T5.2**: Painéis de aba, eyebrow "EIXO N DE 6", remoção do toggle retrátil.
- [x] **T5.3**: Painel Visão geral (Introdução + 6 cartões com contagens do gerador).
- [x] **T5.4**: Barra de abas gerada; remoção da navbar hambúrguer e do Sumário.
- [x] **T5.5**: Ícones Lucide em `assets/icons/`, embutidos inline; emojis de h2, 🚧 e ℹ️ substituídos.
- [x] **T5.6**: `js/navigation.js` (abas, hash, âncora antiga, teclado, `--nav-h`).

## Bloco 6: Sumário lateral e restyle

- [x] **T6.1**: `<aside class="outline">` gerado por painel.
- [x] **T6.2**: `js/sidebar.js` (scroll-spy, progresso, clique com URL).
- [x] **T6.3**: Tokens aprovados aplicados a todos os componentes (CSS do protótipo promovido a `website/css/`).
- [x] **T6.4** *(D6)*: Conclusões por eixo, banner com links, logo com `srcset` (40/32 px), título em 2 linhas. `initNavbar`/`initSections` removidos de `js/charts.js`.

## Bloco 7: Deploy, integração, docs

- [x] **T7.1**: Workflow de deploy com lista de inclusão + checagem de extensões; `404.html` e `.nojekyll`.
- [x] **T7.2**: `sincroniza_docx.py` aponta para o novo gerador/destino (feito já nos Blocos 1-2, para cada commit continuar funcionando).
- [x] **T7.3**: `git rm relatorio/index.html`; `.gitignore` ajustado para `website/`.
- [x] **T7.4**: `website/README.md` e `website/ROADMAP.md` (mobile).
- [x] **T7.5**: `relatorio/specs.md` v8, SKILL.md (descrição + passo 3), CLAUDE.md, constitution §4/§6, tech-stack, roadmap (peso ✅, Fale Conosco, logo SVG, mobile → `website/ROADMAP.md`), README (0.22.0) e CHANGELOG. Comentários dos scripts do PDF que citam `build_html_report.py` ficam como estão (fora do escopo, registro histórico).
- [ ] **T7.6**: P1 — skill `build_website` (decisão do usuário).

## Bloco 8: Validação

- [x] **T8.1**: Playwright 1.x + Firefox 155 + WebKit 26.6 no Python base (ok do usuário, 2026-09-24); Chromium = Chrome instalado (`channel="chrome"`). Fora do `requirements.txt`.
- [x] **T8.2**: Roteiro nos 3 motores, `http://` em subcaminho e `file://` (V8). Achados e corrigidos: fundo translúcido da barra de abas deixava o texto de baixo aparecer (Firefox) → opaco; `favicon.ico` inexistente gerava 404 no console → `assets/images/favicon.svg`; `404.html` só acertava a base em `*.github.io` → usa o 1º segmento do caminho.
- [x] **T8.3**: Checagem de site estático sobre a cópia publicada (V9): 35 arquivos, 23 referências locais, sem problemas.
- [ ] **T8.4**: Deploy real no Pages e roteiro Chromium na URL publicada (com ok do usuário).
- [x] **T8.5**: Capturas por motor no scratchpad; revisão final do usuário abrindo `website/index.html`.
- [x] **T8.7** *(pedido no Bloco 8)*: logo do IPP (banner e rodapé) vira link para `ipp.prefeitura.rio`.
- [x] **T8.8** *(ajustes finais)*: "(sem secundário)" removido do site (id `prioridade` + alias do antigo); logo 34/28 px; PDF com download direto; Base dos Dados no rodapé. Conferido no navegador (texto, rotas nova e antiga, alturas, links), 0 erros.
- [ ] **T8.6**: Merge em `planning`/`staging_main` (com ok do usuário).
