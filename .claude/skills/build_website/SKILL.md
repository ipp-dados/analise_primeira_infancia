---
name: build_website
description: Regenerate, check and prepare the deploy of the static website in website/ (GitHub Pages) -- the tabbed interactive report with SVG charts/maps, built by website/build/build_site.py from tabelas_finais/ and dados_locais/geo/. Use when the user asks to update/regenerate/rebuild the site (or "the HTML report", "the interactive report", "o site", "relatório interativo"), after analise.py outputs or specs/estrutura_eixos.md change, when changing the site's look (css/), behavior (js/) or structure, or before publishing it. NOT for the PDF or the DOCX -- those are the export_pdf_report skill.
---

# Build website

Thin wrapper: the full reference is `website/README.md` (what is generated vs. hand-edited,
local testing, static-site rules) and the design history is `specs/2026-09-24_website_refactor/` +
`relatorio/specs.md` (v8). Read those before changing structure or styling — several
"obvious" alternatives were measured and rejected there (per-polygon simplification,
lazy per-tab data, tracing the IPP logo, translucent tab bar).

## Regenerate

From the project root:

```
python website/build/build_site.py
```

- Reads `tabelas_finais/*.csv`, `dados_locais/geo/*.geojson`, `relatorio/textos_curados.json`.
  CadÚnico numbers are whatever the last `analise.py` run exported (no DB access here).
- Writes `website/index.html`, `website/data/charts.js`, `website/data/geo.js` and generated images
  in `website/assets/images/` (`basemap-*.jpg` only if missing — offline and deterministic;
  `ipp-logo-<altura>.png` from `ipp-logo.png`).
- Maps (`specs/2026-09-28_melhorias_site` U5): the HTML carries each map's `<svg>` empty (compass and scale
  bar in `window.MAPAS_OVERLAYS`); the regions (`<use>`, colour, tooltip) and the map's download CSV live in `window.MAPAS` (`data/charts.js`)
  and `js/charts.js` (`montaMapas`) inserts them on load, in the region order of `window.GEO_IDS` (`data/geo.js`).
  Icons are a `<symbol>` sprite at the top of `<body>`, one `<use>` per icon. Before that round `index.html` was
  785 KB; after, ~345 KB — a change that grows it back by hundreds of KB is a regression.
- Favicon: `python website/build/gera_favicon.py [<opção>]` (options in `website/build/favicon_opcoes/`) writes
  `assets/images/favicon.svg`, `favicon.ico` (site root) and `assets/images/apple-touch-icon.png`; rebuild the site
  afterwards (the `<link>`s carry `?v=<md5>`).
- Prints every published file's size (raw and gzip). **An `AVISO` line means the size budget
  (index ≤ 1 MB, site ≤ 2 MB) was exceeded** — investigate (usually map geometry being inlined per
  map again) instead of publishing.
- Two consecutive runs must give identical `index.html`/`data/*` md5s.
- If the user edited `specs/estrutura_eixos.md` to move an indicator between eixos, the generator
  does NOT read that file — relocate the h2/h3 block in `build_site.py` by hand (see the
  `export_pdf_report` skill's caveat, same rule for both generators).
- Text curated in the DOCX reaches the site through
  `relatorio/curadoria/sincroniza_docx.py`, which also reruns this generator.

## Edit

- `website/css/*.css` and `website/js/*.js` are hand-edited source — edit them directly, never
  as strings in the generator. `index.html` and `data/` are generated — never hand-edit.
- Tokens (colors, radii, shadows, spacing) live in `css/main.css`; text contrast must stay WCAG AA
  (table in `specs/2026-09-24_website_refactor/validation.md` V4). Data palette `--c1..--c11` and the map
  colormaps are fixed project conventions — don't restyle them with the UI (`--c1..--c4` were changed once, on
  2026-09-25, because they failed the `dataviz` validator — `relatorio/specs.md` v9; re-run the validator before
  any palette change). Chart conventions (value formats — `pm1` for per-mil rates, never `%` —, `unidade=`,
  label/colour standardisation, `h3(..., antigo=)`) are in `website/README.md`.
- New icons: add a Lucide SVG to `website/assets/icons/` (keep the ISC license comment); `icone(nome)` puts it in
  the sprite once and emits a `<use>` (don't select inside an icon from CSS: the drawing is in a shadow tree).
- Small multiples (7+ series) show only the panels ("Painéis"); the "Linhas" toggle was removed on 2026-09-28
  (`specs/2026-09-28_melhorias_site` U4).
- Each eixo tab opens with "Principais achados" (`achados_<eixo>`) and, right below it, the eixo's opening text
  (`introducao_<eixo>`, ≤ 100 words) — both report blocks shared with the PDF and the DOCX.
- **Mobile** (`specs/2026-09-28_website_mobile`): every narrow-screen rule lives in `css/mobile.css` (loaded last;
  desktop ≥ 1100 px / tablet 720-1099 / phone < 720). The desktop must not change: before committing, compare
  full-page screenshots of all tabs at 1400 and 1280 px against the previous build (channel difference ≤ 3 is basemap
  decode noise). Charts in containers < 640 px on narrow screens are redrawn at their real width by `js/charts.js`
  (`desenhaLinha`/`desenhaBarras` with a `ctx`; `ctx = null` is the untouched desktop path) — keep new chart options
  working in both paths. Details and component table: `website/README.md` → "Mobile".
- The yellow "EM DESENVOLVIMENTO" strip is driven by `relatorio/publicacao.json` (`em_desenvolvimento`), the same
  switch as the PDF watermark — flip it there, never by editing the banner markup.
- Asset URLs carry `?v=<md5>` (`_v()` in the generator) so browsers never mix a new `index.html` with cached CSS/JS;
  a new file in `css/`/`js/` must be added to the `<head>` with `_v()`.

## Verify before publishing

1. Open `website/index.html` directly (file://) — no console errors, all tabs render — at desktop width and at
   390×844 / 768×1024 with touch emulation (Playwright `is_mobile`/`has_touch`): no horizontal scroll, touch targets
   ≥ 44 px on phones, chart text ≥ 11 px, map legend below the map, tooltips open on tap and close on tap outside.
2. Imitate GitHub Pages: copy the published set (`index.html 404.html .nojekyll css js data assets`)
   into `<tmp>/analise_primeira_infancia/`, run `python -m http.server` in `<tmp>` and open
   `http://127.0.0.1:<port>/analise_primeira_infancia/`.
3. Static-site rules (`website/README.md`): only html/css/js/svg/png/jpg; relative lowercase paths
   that match on-disk case exactly; hash-only routes; no `fetch`.
4. Browser check: Chrome via DevTools Protocol (`websocket-client` is installed) or Playwright
   (Chromium via `channel="chrome"`, Firefox, WebKit — dev environment only: `requirements-dev.txt`). Cover tab switch + hash, old anchors, sticky bar, outline, pills, outliers,
   CSV download and a map tooltip at each level (bairro, AP, RP, RA, CAP).

## Publish

- Commit the regenerated `website/` output (CI cannot generate: `tabelas_finais/` is gitignored).
- Deploy is `.github/workflows/deploy-relatorio.yml`, **manual** (`workflow_dispatch`, Actions tab →
  "Deploy relatório" → Run workflow, on the default branch `staging_main`). It copies an explicit file
  list and fails if a non-static file type is present. Publishing is external and visible — only
  with the user's explicit OK.
