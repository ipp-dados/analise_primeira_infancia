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

- [ ] **T2.1**: `css/main.css`, `css/layout.css`, `css/components.css` a partir da string `CSS`.
- [ ] **T2.2**: `js/charts.js` a partir de `ENGINE`; `data/charts.js` a partir de `RENDER_CALLS`.
- [ ] **T2.3**: Logo para `assets/images/` por `<img src>`; `<!doctype>`, `lang`, `charset`, `viewport`.
- [ ] **T2.4**: DOM e capturas iguais à baseline (V2).

## Bloco 3: Geometria compartilhada

- [ ] **T3.1**: `data/geo.js` com `<defs>` por nível; mapas com `<use>`.
- [ ] **T3.2**: Fundo cartográfico em `assets/images/basemap-*.jpg`.
- [ ] **T3.3**: Hover/tooltip/outliers/CSV nos 5 níveis; tamanho < 3 MB; capturas iguais (V3).

## Bloco 3b: Redução de tamanho (D5)

- [ ] **T3b.1**: Simplificação da geometria por nível (tolerância registrada) + paths relativos.
- [ ] **T3b.2**: `stroke` no CSS; nomes das regiões em `geo.js`; `<use>` enxuto.
- [ ] **T3b.3**: Outliers dos mapas como fills alternativos (1 SVG por mapa).
- [ ] **T3b.4**: `data/charts-<eixo>.js` carregado na primeira ativação da aba.
- [ ] **T3b.5**: Relatório de tamanho + aviso de orçamento no gerador; metas de spec §4.9 cumpridas (V3b).

## Bloco 4: Protótipo

- [ ] **T4.1**: Tokens (raio, sombra, espaçamento, superfícies) em rascunho, contraste AA medido.
- [ ] **T4.2**: Página de teste com markup real + capturas 1440/1280px.
- [ ] **T4.3**: Aprovação do usuário (ou rodada de ajustes registrada aqui).

## Bloco 5: Abas e conteúdo

- [ ] **T5.1**: Coletor de fontes por h2 + caixa "FONTES DESTA SEÇÃO".
- [ ] **T5.2**: Painéis de aba, eyebrow "EIXO N DE 6", remoção do toggle retrátil.
- [ ] **T5.3**: Painel Visão geral (Introdução + 6 cartões com contagens do gerador).
- [ ] **T5.4**: Barra de abas gerada; remoção da navbar hambúrguer e do Sumário.
- [ ] **T5.5**: Ícones Lucide em `assets/icons/`, embutidos inline; emojis de h2, 🚧 e ℹ️ substituídos.
- [ ] **T5.6**: `js/navigation.js` (abas, hash, âncora antiga, teclado, `--nav-h`).

## Bloco 6: Sumário lateral e restyle

- [ ] **T6.1**: `<aside class="outline">` gerado por painel.
- [ ] **T6.2**: `js/sidebar.js` (scroll-spy, progresso, clique com URL).
- [ ] **T6.3**: Tokens aprovados aplicados a todos os componentes.

## Bloco 7: Deploy, integração, docs

- [ ] **T7.1**: Workflow de deploy com lista de inclusão + checagem de extensões; `404.html` e `.nojekyll`.
- [ ] **T7.2**: `sincroniza_docx.py` aponta para o novo gerador/destino.
- [ ] **T7.3**: `git rm relatorio/index.html`; `.gitignore` ajustado para `website/`.
- [ ] **T7.4**: `website/README.md` e `website/ROADMAP.md` (mobile).
- [ ] **T7.5**: `relatorio/specs.md` v8, SKILL.md, CLAUDE.md, tech-stack, roadmap, README/CHANGELOG.
- [ ] **T7.6**: P1 — skill `build_website` (decisão do usuário).

## Bloco 8: Validação

- [ ] **T8.1**: Playwright instalado no ambiente de dev (com ok do usuário).
- [ ] **T8.2**: Roteiro de verificação nos 3 motores, `http://` e `file://` (V8).
- [ ] **T8.3**: Checagem de site estático sobre `_site/` servido em subcaminho (V9).
- [ ] **T8.4**: Deploy real no Pages e roteiro Chromium na URL publicada (com ok do usuário).
- [ ] **T8.5**: Capturas finais por aba para revisão do usuário.
- [ ] **T8.6**: Merge em `planning`/`staging_main` (com ok do usuário).
