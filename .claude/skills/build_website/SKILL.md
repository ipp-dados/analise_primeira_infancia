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
- Prints every published file's size (raw and gzip). **An `AVISO` line means the size budget
  (index ≤ 1 MB, site ≤ 2 MB) was exceeded** — investigate (usually map geometry being inlined per
  map again) instead of publishing.
- Two consecutive runs must give identical `index.html`/`data/*` md5s.
- If the user edited `specs/estrutura_eixos.md` to move an indicator between eixos, the generator
  does NOT read that file — relocate the h2/h3 block in `build_site.py` by hand (see the
  `export_pdf_report` skill's caveat, same rule for both generators).
- Text curated in the DOCX reaches the site through
  `.claude/skills/export_pdf_report/scripts/sincroniza_docx.py`, which also reruns this generator.

## Edit

- `website/css/*.css` and `website/js/*.js` are hand-edited source — edit them directly, never
  as strings in the generator. `index.html` and `data/` are generated — never hand-edit.
- Tokens (colors, radii, shadows, spacing) live in `css/main.css`; text contrast must stay WCAG AA
  (table in `specs/2026-09-24_website_refactor/validation.md` V4). Data palette `--c1..--c11` and the map
  colormaps are fixed project conventions — don't restyle them with the UI (`--c1..--c4` were changed once, on
  2026-09-25, because they failed the `dataviz` validator — `relatorio/specs.md` v9; re-run the validator before
  any palette change). Chart conventions (value formats — `pm1` for per-mil rates, never `%` —, `unidade=`,
  label/colour standardisation, `h3(..., antigo=)`) are in `website/README.md`.
- New icons: add a Lucide SVG to `website/assets/icons/` (keep the ISC license comment); the
  generator inlines it with `icone(nome)`.
- Desktop only so far; mobile work is listed in `ROADMAP.md` (root, "Próximos" → versão mobile).

## Verify before publishing

1. Open `website/index.html` directly (file://) — no console errors, all tabs render.
2. Imitate GitHub Pages: copy the published set (`index.html 404.html .nojekyll css js data assets`)
   into `<tmp>/analise_primeira_infancia/`, run `python -m http.server` in `<tmp>` and open
   `http://127.0.0.1:<port>/analise_primeira_infancia/`.
3. Static-site rules (`website/README.md`): only html/css/js/svg/png/jpg; relative lowercase paths
   that match on-disk case exactly; hash-only routes; no `fetch`.
4. Browser check: Chrome via DevTools Protocol (`websocket-client` is installed) or Playwright
   (Chromium via `channel="chrome"`, Firefox, WebKit — dev environment only, not in
   `requirements.txt`). Cover tab switch + hash, old anchors, sticky bar, outline, pills, outliers,
   CSV download and a map tooltip at each level (bairro, AP, RP, RA, CAP).

## Publish

- Commit the regenerated `website/` output (CI cannot generate: `tabelas_finais/` is gitignored).
- Deploy is `.github/workflows/deploy-relatorio.yml`, **manual** (`workflow_dispatch`, Actions tab →
  "Deploy relatório" → Run workflow, on the default branch `staging_main`). It copies an explicit file
  list and fails if a non-static file type is present. Publishing is external and visible — only
  with the user's explicit OK.
