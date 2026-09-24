# Plano técnico: website_refactor

Baseado em `specification.md` (rascunho 1, D1-D4 aprovadas). **Nada é executado antes do ok do usuário
neste plano.** Um commit por bloco (`SPEC-WebsiteRefactor: Bloco N -- ...`).

## Sequência

| Bloco | Fase do prompt | Conteúdo | Muda a aparência? | Depende de |
|---|---|---|---|---|
| 0 | 1 | Baseline: checksums, contagens, capturas de tela do relatório atual | não | — |
| 1 | 3.1 | Mover o gerador para `website/build/`, saída em `website/index.html` (ainda 1 arquivo) | não | 0 |
| 2 | 3.1 | Extrair CSS, motor JS, render calls e logo para arquivos | não | 1 |
| 3 | 3.1 | Geometria compartilhada dos mapas (D2) + fundo cartográfico em `.jpg` | não | 2 |
| 3b | 3.1 | Redução de tamanho (D5, spec §4.9): simplificação, atributos, variantes de outlier, dados por aba, orçamento | não (salvo tolerância) | 3 |
| 4 | 2 | Protótipo de tokens e layout (página de teste) → **revisão do usuário** | — | 2 |
| 5 | 3.2, 3.5 | Abas, Visão geral, caixa de fontes, ícones; remove navbar/Sumário/retrátil | sim | 4 |
| 6 | 3.3, 3.4 | Sumário lateral com progresso; restyle aplicado a todos os componentes | sim | 5 |
| 7 | 4.3 | Deploy, `sincroniza_docx.py`, remoção de `relatorio/index.html`, docs, `ROADMAP.md` | — | 6 |
| 8 | 4.1, 4.2 | Validação completa (3 motores, `file://` e servidor estático) | — | 7 |

Blocos 1-3 são refatorações **neutras**: a página renderizada tem que ficar igual à baseline. Isso
separa "quebrou na mudança de estrutura" de "quebrou no redesign". O Bloco 4 pode correr em paralelo com o 3.

## Princípios

- **Editar o gerador, não o gerado** (constitution §4). CSS/JS em `website/css` e `website/js` passam a
  ser fonte editada à mão; o gerador só escreve `index.html`, `data/` e `assets/images/basemap-*`.
- **PDF intocado**: nenhum byte de `build_notebook_report.py`, `gera_docx_curadoria.py`, `extract_maps.py`,
  `regen_missing_pngs.py`. `gera_estrutura_eixos.py` só é importado, não editado. A única edição fora de
  `website/` na skill é o destino em `sincroniza_docx.py` (Bloco 7).
- **Caminhos relativos em tudo**, e rodando do root do projeto como hoje (`tabelas_finais/`,
  `dados_locais/geo/`, `relatorio/textos_curados.json` continuam onde estão).
- **Sem dependência nova em runtime**: vanilla HTML/CSS/JS, fontes do Google Fonts como hoje. Ícones
  Lucide copiados como arquivos SVG (sem pacote npm).

## Blocos

### Bloco 0: Baseline

- md5 e tamanho de `relatorio/index.html`; saída do `print` final do gerador (nº de gráficos, h2, h3).
- Contagens do HTML atual: `.out`, `.option-card`, `.map-svg-card`, `.outlier-card`, `data-csv`, h3 por eixo
  (tabela da spec §2).
- Capturas com Edge headless (perfil descartável em scratchpad, regra da SKILL.md): página inteira em
  1440px + recortes de 1 gráfico de linha, 1 barra agrupada, 1 mapa de cada nível (bairro, AP, RP, RA, CAP),
  1 bloco pendente.
- Tudo guardado no scratchpad; resumo em `validation.md` V0.

### Bloco 1: Mover o gerador (neutro)

- `git mv .claude/skills/export_pdf_report/scripts/build_html_report.py website/build/build_site.py`
  (preserva o histórico).
- No topo: `ROOT = Path(__file__).resolve().parents[2]`; `os.chdir(ROOT)` para que os caminhos relativos
  continuem valendo; `sys.path.insert` para `.claude/skills/export_pdf_report/scripts` (import de
  `avisa_itens_sem_arquivo`).
- Saída padrão: `website/index.html`. Docstring atualizada (histórico mantido, nova seção no topo).
- Verificação: rodar com saída em `relatorio/index.html` → md5 igual à baseline, exceto a data de geração
  (se o dia mudou).

### Bloco 2: Extrair CSS/JS/dados (neutro)

- String `CSS` → dividida em `website/css/main.css` (`:root`, reset, tipografia, `h1-h6`),
  `layout.css` (`.doc`, header, rodapé, grades) e `components.css` (resto). Ordem dos `<link>` preserva a
  cascata atual (main → layout → components).
- String `ENGINE` → `website/js/charts.js` (idêntico, IIFE preservada, `window.*` expostos como hoje).
- `RENDER_CALLS` → `website/data/charts.js`, carregado depois de `charts.js`.
- Logo: `relatorio/assets/ipp-logo.png` → `website/assets/images/ipp-logo.png` (`git mv`; nenhum outro
  script usa esse arquivo) e referenciado por `<img src>`, não mais base64. Antes: exceção
  `!/website/assets/**` no `.gitignore` (ver Bloco 7 — `*.png`/`*.svg` são ignorados globalmente).
- `index.html` ganha `<!doctype html>`, `<html lang="pt-BR">`, `<meta charset>`, `<meta viewport>` (hoje o
  documento começa direto em `<title>`).
- Verificação: DOM do `<body>` igual à baseline (normalizando só o `src` do logo); capturas iguais.

### Bloco 3: Geometria compartilhada dos mapas (D2, neutro visualmente)

- `_geo_nivel(nivel)` já projeta cada nível uma vez (`_GEO_CACHE`). Coletar os `d` por
  `(nivel, chave)` e escrever `website/data/geo.js`: uma string com
  `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><path id="geo-bairro-1" d="…"/>…</defs></svg>`
  injetada em `document.body` antes de `data/charts.js` rodar.
- `mapa_svg.build`: trocar `<path d="{d}" …>` por `<use href="#geo-{nivel}-{chave}" class="map-region" fill=… data-label=… data-valor=…>`;
  `stroke`/`stroke-width` passam para o `<use>` (herdados pelo path, que não define nenhum).
- `initMapTooltips` e as regras CSS de `.map-region:hover`: conferir que o alvo do evento é o `<use>` e que
  o hover aplica. Ajustar só se necessário.
- Fundo cartográfico: `_basemap_css_class` grava `website/assets/images/basemap-<n>.jpg` e a regra CSS
  aponta para o arquivo (a regra continua gerada e inline num `<style>` pequeno, ou em `data/basemap.css`).
- Verificação: tamanho registrado; capturas dos 5 níveis de mapa iguais à baseline; hover, tooltip,
  outliers e CSV funcionando em cada nível.

### Bloco 3b: Redução de tamanho (D5)

Cada passo é medido isoladamente (tamanho antes/depois em `validation.md` V3b), para saber quanto cada um rende.
1. **Simplificação**: em `_geo_nivel`, depois de projetar e dissolver, `geometry.simplify(tol, preserve_topology=True)`
   com `tol` em unidades do SVG (começar em 0,3 px e subir enquanto a captura em zoom 200% não mostrar
   fresta nem perder ilha). Paths com comandos relativos e 1 casa decimal.
2. **Atributos**: `stroke`/`stroke-width` para `.map-region` no CSS; `geo.js` exporta também
   `{"<nivel>-<chave>": "<nome>"}`; o tooltip busca o nome pelo `href` do `<use>`; o `<use>` fica com
   `href`, `fill`, `data-valor`.
3. **Outliers dos mapas**: em vez de 2 SVGs, 1 SVG + `data-fill-clean` só nas regiões que mudam de cor e
   legenda alternativa; o toggle troca `fill` e a legenda. Gráficos continuam com 2 painéis (pequenos).
4. **Dados por aba**: `RENDER_CALLS` agrupado pelo h2 corrente → `data/charts-<eixo>.js`; `navigation.js`
   injeta o `<script>` na primeira ativação da aba e só então roda o scroll para um `#<eixo>/<h3>` (R1c).
5. **Orçamento**: função no fim do gerador lista o tamanho de cada arquivo gerado (bruto e gzip) e
   imprime `AVISO` se passar de §4.9.
- Verificação: orçamento de §4.9 cumprido; capturas iguais à baseline (exceto diferença de simplificação
  aprovada por inspeção); toggle de outliers do mapa troca cores e legenda igual à baseline.

### Bloco 4: Protótipo de tokens e layout (fase 2 do prompt)

- Página de teste fora do site publicado (`website/build/prototype.html`, ou scratchpad) que usa os
  `main.css`/`layout.css`/`components.css` em rascunho e **markup real copiado** do `index.html`: banner,
  barra de abas, 1 painel com Principais achados + 2 h3 + 1 gráfico de linha + 1 mapa + 1 pendente + caixa
  de fontes, sumário lateral estático.
- Tokens propostos: raios (6/12/20px), 2 níveis de sombra, escala de espaçamento (4-64px), superfícies de UI
  levemente frias, texto `--ink` com contraste AA medido.
- Capturas em 1440px e 1280px → **o usuário aprova ou pede ajustes antes do Bloco 5**.

### Bloco 5: Abas, Visão geral, fontes, ícones

Gerador (`build_site.py`):
- Coletor de fontes: `_out_div`, `mapa_svg` e `plain_table` registram `fonte` num dicionário por h2
  corrente (`h2()` abre a entrada), preservando a ordem e removendo repetições.
- Montagem (hoje em "envolve cada seção h2"): cada h2 vira `<section class="tab-panel" id="<eixo>"
  role="tabpanel" hidden>` com eyebrow "EIXO N DE 6", Principais achados, corpo, caixa de fontes. Sai o
  botão recolher.
- Painel "Visão geral" (`id="visao-geral"`): Introdução + 6 cartões de eixo (ícone, título, nº de h3,
  nº de pendentes, link `#<eixo>`), calculados de `toc` e das contagens do gerador.
- Barra de abas gerada a partir de `toc` (mesma fonte de dados da navbar antiga). Sai a navbar
  hambúrguer e o Sumário (`<!--NAVBAR-->`, `<!--SUMARIO-->`, `initNavbar`, `initSections`).
- Ícones: `website/assets/icons/<nome>.svg` lidos e embutidos inline (para herdar `currentColor`).
  Mapeamento eixo → ícone num dicionário no gerador; emojis removidos dos h2 (slugs dos ids não mudam —
  hoje o emoji já é descartado por `slugify`); 🚧 e ℹ️ viram ícones.

`js/navigation.js`:
- `activate(eixo, {scrollTo})`: mostra o painel, `aria-selected`, rola para o topo do painel, dispara
  evento `tabchange` (que o sidebar escuta).
- Roteamento por `location.hash` (§4.3 da spec), incluindo resolução de `#<id-h3>` antigo.
- Setas ←/→ na barra de abas; mede a altura da barra e escreve `--nav-h`.

### Bloco 6: Sumário lateral + restyle

- Gerador emite `<aside class="outline">` com uma `<nav>` por painel (h3 do painel; na Visão geral, os
  eixos) e a barra de progresso.
- `js/sidebar.js`: mostra a `<nav>` do painel ativo; `IntersectionObserver` nos h3 do painel ativo
  (`rootMargin` com `--nav-h`); progresso por `scroll` com `requestAnimationFrame`; clique → `scrollIntoView`
  suave + `history.replaceState` para `#<eixo>/<id-h3>`.
- Aplicar os tokens aprovados no Bloco 4 a todos os componentes: `.out`, `.option-card*`, pills,
  `.outlier-card`, `.map-svg-card`, `.key-takeaways`, `.pending-block`, `.table-with-text`, rodapé.
- `scroll-margin-top: calc(var(--nav-h) + 16px)` nos h3.

### Bloco 7: Deploy, integração e documentação

- `.github/workflows/deploy-relatorio.yml`: cópia **explícita** de `index.html 404.html .nojekyll css js data assets`
  para `_site/` (lista de inclusão, não de exclusão — nada de `build/`, `.py`, `README.md`, `ROADMAP.md` vaza
  por esquecimento). Passo de checagem no workflow que falha se `_site/` tiver qualquer extensão fora de
  `html css js svg png jpg` (spec §4.10).
- `website/404.html` e `website/.nojekyll` criados (estáticos, à mão).
- `sincroniza_docx.py`: subprocess passa a rodar `website/build/build_site.py` com destino
  `website/index.html` (edição mínima + mensagem final).
- `git rm relatorio/index.html`; tirar `!/relatorio/index.html` do `.gitignore` (já é uma exceção
  órfã: não existe mais regra `*.html`). **`*.png` e `*.svg` são ignorados globalmente** — sem exceção,
  `website/assets/icons/*.svg` e `website/assets/images/*.png` somem do commit em silêncio (o logo atual
  só está no git porque foi adicionado à força). Adicionar `!/website/assets/**` (antes do Bloco 2, que já
  cria o primeiro arquivo ali) e conferir com `git check-ignore -v` + `git status`.
- Docs: `website/README.md` (gerar, o que é gerado vs. à mão, como testar local), `website/ROADMAP.md`
  (mobile: abas em rolagem horizontal ou menu, sumário lateral vira gaveta/topo, grades de 1 coluna,
  mapas e legenda, alvos de toque, tamanho da fonte base), `relatorio/specs.md` (v8, tabela de
  reversões da spec §6), `export_pdf_report/SKILL.md` (tirar o passo do HTML, apontar para o site),
  `CLAUDE.md`, `specs/tech-stack.md`, `specs/roadmap.md` (fechar "reduzir peso"), README/CHANGELOG
  (entrada curta, constitution §1).
- P1 (skill `build_website`): decidir com o usuário aqui.

### Bloco 8: Validação

- Servidor estático (`python -m http.server` dentro de `website/`) e `file://`.
- Playwright (Chromium, Firefox, WebKit como proxy de Safari) — `pip install playwright` +
  `playwright install` no ambiente de dev, **não** no `requirements.txt` do projeto (ferramenta de
  validação, não do pipeline); confirmar com o usuário antes de instalar.
- Script de verificação no scratchpad: troca de aba, hash e voltar/avançar, âncora antiga, barra fixa em
  y=0 depois de rolar, sumário ativo e progresso, pills, outliers, CSV, tooltip de mapa por nível, zero erro
  no console.
- **Checagem de site estático (spec §4.10)**, script no scratchpad sobre uma cópia de `_site/` montada
  com o mesmo passo do workflow:
  - só extensões permitidas; nenhum `.py`;
  - nenhum `href`/`src` começando com `/` ou `file:`; nenhum `fetch(`/`XMLHttpRequest` nos JS;
  - todo `href`/`src` relativo aponta para um arquivo que existe **com a mesma caixa** (comparação
    exata de nome, porque o Windows não acusa);
  - servir `_site/` **num subcaminho** (`python -m http.server` na pasta-pai, abrindo `/<repo>/`) para
    imitar `<usuario>.github.io/<repo>/`, e rodar o roteiro Playwright ali;
  - `/<repo>/inexistente` → o servidor local não imita o 404 do Pages; conferir só que `404.html` existe e
    abre sozinho.
- **Deploy de verdade** (`workflow_dispatch`) só com ok explícito do usuário — é publicação externa.
  Depois: abrir a URL do Pages e repetir o roteiro Chromium ali.
- Capturas finais por aba (1440px) para o usuário revisar.
