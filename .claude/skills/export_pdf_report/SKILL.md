---
name: export_pdf_report
description: Export a non-technical PDF of the primeira-infancia analysis, using analise.py's own matplotlib/seaborn chart images (visualizacoes/*.png) and tabelas_finais/ data tables -- NOT the relatorio/*.html custom SVG report. Use when the user asks for a PDF export/version of the analysis, report, or notebook, or to regenerate an existing report PDF after the notebook/data changes.
---

# Export PDF report

Produces a print-ready PDF that mirrors `analise.py` section by section
(same titles/order/notes as its markdown cells), but the charts are the
**actual matplotlib/seaborn PNGs the notebook itself produces** in
`visualizacoes/` -- not a re-rendered custom chart engine. This was a
deliberate correction: an earlier version of this skill converted
`relatorio/*.html` (a separate, hand-built report with its own SVG chart
engine, pastel palette and Fraunces/IBM-Plex typography — see
`relatorio/specs.md`) to PDF. The user explicitly rejected that: **"keep
the visual style of the visualizations used in the notebook, not the
html."** Do not go back to converting `relatorio/*.html` — build the
document from `analise.py`'s own outputs instead, as described below.

**Note:** `scripts/build_html_report.py` also lives in this skill's folder
but is a separate pipeline, for `relatorio/relatorio.html` (the interactive
HTML report), not this PDF. As of `specs/relatorio-interativo` (v6,
`relatorio/specs.md`) that report has its own visual identity — brutalist
bordered cards, a pill-selector for cortes that used to repeat as separate
charts, an outlier toggle, per-chart CSV download, and interactive SVG maps
(`mapa_svg()`) replacing most of the old raster `mapas/*.png` — entirely
independent of this skill's matplotlib/PNG-based PDF pipeline. Don't apply
that report's styling conventions here; this PDF intentionally mirrors the
notebook's own matplotlib rendering, per the rejection noted above.

## Pipeline

Run every command from the project root.

1. **Regenerate any stale/missing chart PNGs.**
   `visualizacoes/*.png` is not guaranteed to be complete under its current
   filenames — `analise.py` gets re-run cell-by-cell during development
   (not always top-to-bottom), so older sections' PNGs can lag behind a
   renaming refactor. Check what's missing by diffing the filenames each
   `nome_arquivo=` call in `analise.py` writes against what's actually in
   `visualizacoes/`. As of 2026-09-02 this includes: the 2 Censo series
   (analise.py only ever calls `plt.show()` on those, never `savefig`), 4
   CadÚnico charts, and several DataSus/SISVAN/PNAD charts that were last
   generated under an old filename.
   `scripts/regen_missing_pngs.py` regenerates all of these **from
   `tabelas_finais/` CSVs already on disk — no DB connection or raw
   `dados_locais/` files needed**, including the 4 CadÚnico charts (their
   source CSVs are already exported there). Copies of `analise.py`'s
   `serie_temporal`/`grafico_barra` verbatim, so output is pixel-identical
   in style to what the notebook itself would produce.
   ```
   python .claude/skills/export_pdf_report/scripts/regen_missing_pngs.py
   ```
   If analise.py's plotting functions or exported CSV schemas changed since
   2026-09-02, this script needs matching edits — it's a snapshot of that
   contract, not a generic tool. Read it before trusting it blindly.

2. **Extract the 5 map images.** The choropleth maps in `mapas/` are ~6MB
   PNGs (too big to embed directly at full size); `relatorio/relatorio.html`
   already ships them pre-resized to ~130KB WebP data URIs (see
   `relatorio/specs.md`) — reuse that instead of re-encoding. **Note (v6,
   `specs/relatorio-interativo`):** most maps in `relatorio/relatorio.html` are
   no longer PNG/WebP at all — `build_html_report.py` now renders them as
   inline interactive SVG (`mapa_svg()`), so `extract_maps.py`'s approach
   (pulling a `const MAPS = [...]` JS array out of the HTML) only finds the
   handful of maps still on the old path, if any remain. Check
   `build_html_report.py` for the current map count before relying on this
   step; `extract_maps.py` may need to read straight from `mapas/*.png`
   instead of from the HTML if the JS array it expects is gone.
   ```
   python .claude/skills/export_pdf_report/scripts/extract_maps.py relatorio/relatorio.html <scratchpad>/maps.json
   ```

3. **Build the report HTML.** `scripts/build_notebook_report.py` is a
   direct transcription of `analise.py`'s markdown cells and
   `serie_temporal`/`grafico_barra`/`serie_temporal_multipla` calls: for
   each one it embeds the matching PNG from `visualizacoes/` (base64) plus
   a plain data table sourced from the matching `tabelas_finais/*.csv`.
   ```
   python .claude/skills/export_pdf_report/scripts/build_notebook_report.py <scratchpad>/maps.json <scratchpad>/pdf_source.html
   ```
   If `analise.py` gains/loses a section, or a `tabelas_finais/` filename
   or column name changes, this script needs matching edits — same caveat
   as step 1.

4. **Render to PDF with an isolated headless Chrome.** System Chrome is at
   `C:\Program Files\Google\Chrome\Application\chrome.exe` on this machine.

   **Critical safety rule:** always pass `--headless=new` together with a
   **dedicated, throwaway `--user-data-dir`** (e.g. a fresh folder under
   the scratchpad). Without an isolated `--user-data-dir`, `chrome.exe` can
   attach to the user's real running Chrome instance/profile and pop open a
   **visible window on the user's desktop** — confirmed while building this
   skill, twice: once from a plain `--version` check with no flags at all,
   and the fix (`--headless=new` alone, still sharing the default profile
   dir implicitly) was not sufficient on its own either. Always pass both
   flags together, every invocation, no exceptions.

   ```
   CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
   PROFILE="<scratchpad>/chrome_profile"   # fresh dir, throwaway
   "$CHROME" --headless=new --disable-gpu --no-sandbox \
     --disable-default-apps --no-first-run --disable-sync \
     --user-data-dir="$PROFILE" \
     --print-to-pdf="<scratchpad>/report.pdf" \
     --no-pdf-header-footer \
     --virtual-time-budget=20000 \
     "file:///<scratchpad>/pdf_source.html"
   ```
   **`--no-pdf-header-footer` is the flag that actually suppresses Chrome's
   injected page header/footer** (URL, date, page number). A similarly
   named `--print-to-pdf-no-header` flag does *not* do this — it was tried
   and produced a PDF with visible browser chrome (date top-left, page
   title top-center, `file://...` path + page number at the bottom) on
   every page. Use `--no-pdf-header-footer`, not the other one.

5. **Verify before handing off.** Page count sanity check:
   ```
   python -c "import pypdf; print(len(pypdf.PdfReader('<pdf>').pages))"
   ```
   Then rasterize a broad sample (first page, several mid-document pages
   across different sections, the maps section, the last page) with
   PyMuPDF and actually look at the PNGs — don't just trust a 0 exit code:
   ```
   python -c "
   import fitz
   doc = fitz.open('<pdf>')
   for i in [0, 5, len(doc)//3, len(doc)//2, 2*len(doc)//3, len(doc)-1]:
       doc[i].get_pixmap(dpi=95).save(f'<scratchpad>/check_{i}.png')
   "
   ```
   Known failure modes to specifically check for (all previously hit and
   fixed while building this skill — don't reintroduce them):
   - **Year columns/axes with a thousands separator or fractional ticks**
     (`"2.000"` instead of `"2000"`, or `"2007.5"` tick labels on a chart).
     A column literally named `ano` must never get thousands-grouped, and
     any dataframe read fresh from a CSV needs `df['ano'].astype(str)`
     before plotting a time series with `serie_temporal`, or seaborn
     treats a numeric `ano` as a continuous axis instead of one tick/year.
   - **Wide tables (>6-7 columns) silently clipped/scrollable.** A `<table>`
     wider than the printable page area doesn't wrap in Chrome's print
     output — it just overflows with an inert scrollbar baked into the
     image. `table_html(..., clean_headers=True)` and the `.plain.wide`
     CSS class (table-layout:fixed, wrapping headers, smaller font) handle
     this; use it for anything with many series as columns (subgrupo/CID-10
     tables, cobertura vacinal by imunobiológico).
   - **Percent columns on the wrong scale.** Most `tabelas_finais/*.csv`
     percentage columns are already 0-100. At least one (PNAD frequência
     escolar's `Total`) is a 0-1 fraction — multiply by 100 before treating
     it as a `pct_cols` column, or it prints as `"0,1%"` instead of `"8,0%"`.
   - Browser header/footer leaking onto every page (see step 4's flag note).
   - Dark theme leaking in from the rendering environment's OS setting — the
     doc already forces `<html data-theme="light">` + a `color-scheme`
     meta tag; don't drop those if editing the template.

6. **Place the final file.** Copy the verified PDF to
   `relatorio/analise_primeira_infancia.pdf`. It is **not** in
   `.gitignore` (unlike `relatorio/*.html`, which is) — ask the user before
   committing it if that wasn't already part of the request, since it's a
   ~10-15MB binary regenerated from other tracked/ignored sources.

## Known limitations to mention if relevant

- CadÚnico charts reflect the last saved `tabelas_finais/` export, not a
  live CTPE query (documented in `relatorio/specs.md`); this pipeline
  doesn't touch the DB at all, so it can't refresh them further.
- Some chart end-labels can visually overlap when two series end on close
  values — a cosmetic quirk of the matplotlib defaults `analise.py` uses
  (no custom label collision avoidance), not something to "fix" here since
  the whole point is fidelity to the notebook's own rendering.
- `analise.py` also has two sections with no visual output at all (the
  final bairro/município table joins, "Análise / Relatório") — this
  report omits them, matching `relatorio/*.html`'s precedent.
