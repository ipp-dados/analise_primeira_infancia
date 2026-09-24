---
name: export_pdf_report
description: Export a non-technical PDF of the primeira-infancia analysis, using analise.py's own matplotlib/seaborn chart images (visualizacoes/*.png) and tabelas_finais/ data tables -- NOT the website/ static site's custom SVG charts. Use when the user asks for a PDF export/version of the analysis, report, or notebook, or to regenerate an existing report PDF after the notebook/data changes. Also covers regenerating the website (website/build/build_site.py, step 3) and the DOCX curation export (relatorio/curadoria_textos.docx) from the same structural source (specs/estrutura_eixos.md) -- use this skill too when the user edits that file and asks to "update the report(s)", or when someone has hand-edited analysis text in the DOCX and asks to sync/propagate it back into the website, PDF, or analise.py.
---

# Export PDF report

Produces a print-ready PDF that mirrors `analise.py`'s outputs section by
section, but the charts are the **actual matplotlib/seaborn PNGs the
notebook itself produces** in `visualizacoes/` -- not a re-rendered custom
chart engine. This was a deliberate correction: an earlier version of this
skill converted `relatorio/*.html` (a separate, hand-built report with its
own SVG chart engine, pastel palette and Fraunces/IBM-Plex typography — see
`relatorio/specs.md`) to PDF. The user explicitly rejected that: **"keep
the visual style of the visualizations used in the notebook, not the
html."** Do not go back to converting `relatorio/*.html` — build the PDF
from `analise.py`'s own outputs instead, as described below.

**Note (updated 2026-09-24, `specs/website_refactor`):** the interactive HTML report no longer
lives in this skill. Its generator (formerly `scripts/build_html_report.py`) moved to
`website/build/build_site.py` and now produces the static site in `website/` (tabs per eixo, sticky
outline, SVG charts/maps, hand-edited `css/`/`js/`) — see `website/README.md`. It is still entirely
independent of this skill's matplotlib/PNG-based PDF pipeline: don't apply the site's styling
conventions to the PDF, or vice versa; the rejection noted above still stands. It still imports
`avisa_itens_sem_arquivo` from `scripts/gera_estrutura_eixos.py` and reads
`relatorio/textos_curados.json`, and `scripts/sincroniza_docx.py` still regenerates it (step 6).
**What changed as of `specs/ajuste_eixos`:** both used
to be organized independently (9 sections each, mirroring `analise.py`'s
data-source order, hardcoded per script) — both were manually regrouped
into the 6 eixo sections described by `specs/estrutura_eixos.md` (see
`specs/ajuste_eixos/specs.md` for the crosswalk/decisions), but **neither
actually reads that file at runtime** — see the important caveat below
before assuming an `.md` edit alone regenerates them correctly.

## `specs/estrutura_eixos.md`: source of truth for grouping — but only *live* for the DOCX

A hand-editable Markdown file (root of `specs/`, not inside
`specs/ajuste_eixos/`) — `##` per eixo, `###` per indicator subsection, a
flat `- chave: valor` list per subsection (`fonte`/`visualização`/`mapa`/
`tabela`/`status`/`nota`; repeatable keys become a list). **This is the
file the user edits by hand** to reorganize the reports (move an
indicator to another eixo, rename a subsection, mark something pendente)
— per the explicit request in `specs/ajuste_eixos/specs.md` §5.2: *"whenever
i may want to change the structure of the report, i want to be able to
just change the .md file and ask for the update."*

**Important, discovered while validating this skill (2026-09, Bloco 6):**
that promise is only fully automatic for `gera_docx_curadoria.py`, which
genuinely imports and calls `parse_estrutura_eixos()` at generation time —
edit the `.md`, rerun step 5 below, done. `website/build/build_site.py` (ex-`build_html_report.py`) and
`build_notebook_report.py` do **not** import or read the `.md` at all —
their grouping is hardcoded Python, physically reorganized once (Blocos
3-4) to match the `.md` as it existed then. Regenerating them after an
`.md`-only edit reproduces the *old* grouping byte-for-byte (confirmed
empirically: moving an indicator between eixos and renaming a subsection
in the `.md`, then rerunning step 3, produced a byte-identical
site output). Decided with the user not to rewrite these two
into fully data-driven renderers (a much larger, riskier change touching
already-verified working code) — so when a user's `.md` edit changes
HTML/PDF *grouping* (which eixo a chart/map lives under — a rename that
doesn't move anything, or a `status: pendente` flip, has no HTML/PDF code
to touch), the fix is a **manual code change**: find the moved
content's h2/h3/h4 block in `website/build/build_site.py`
(and the equivalent in `build_notebook_report.py`) and relocate it under
the new eixo's heading, same method used to build Blocos 3-4 originally —
then run the pipeline. Tell the user this explicitly rather than silently
claiming the `.md` edit alone was enough for all three artifacts.

`scripts/gera_estrutura_eixos.py` owns `parse_estrutura_eixos()` (the
parser — only `gera_docx_curadoria.py` actually imports it, per the caveat
above; `website/build/build_site.py`/`build_notebook_report.py` only reference the
`.md` in comments) and `valida_estrutura()` (fails loud, naming the missing
file, if any `visualização`/`mapa`/`tabela` reference doesn't exist on disk
— never lets a generator run against a broken reference silently, and
worth running against the `.md` regardless of which artifact you're
touching). It does **not** regenerate `specs/estrutura_eixos.md` from the
original Excel catalog (`dados_locais/painel_primeira_infancia_cesta_indicadores.xlsx`)
— that classification (which eixo a catalog indicator belongs to, which 18
were discarded) was a one-time script run to produce the initial file;
from then on the `.md` is the source of truth, edited by hand, never
re-derived from the spreadsheet again (`specs/ajuste_eixos/specs.md` §5.2).

## Pipeline

Run every command from the project root. Steps 3-5 are independent of each
other once step 1-2 are done — regenerate only the artifact(s) the request
actually needs (e.g. "just update the PDF" skips steps 3 and 5), but
**always run 1-2 first** regardless of which artifact(s) you're targeting.
Step 6 (DOCX text sync) is only relevant once someone has actually curated
text in the DOCX — most regeneration requests never need it.

1. **Regenerate any stale/missing chart PNGs.**
   `visualizacoes/*.png` is not guaranteed to be complete/current under its
   current filenames — `analise.py` gets re-run cell-by-cell during
   development (not always top-to-bottom), so older sections' PNGs can lag
   behind a renaming refactor or a data update.
   `scripts/regen_missing_pngs.py` regenerates a known list of charts
   **from `tabelas_finais/` CSVs already on disk — no DB connection or raw
   `dados_locais/` files needed.** Copies of `analise.py`'s
   `serie_temporal`/`grafico_barra` verbatim, so output is pixel-identical
   in style to what the notebook itself would produce.
   ```
   python .claude/skills/export_pdf_report/scripts/regen_missing_pngs.py
   ```
   **Caution observed in practice:** this script regenerates its whole
   fixed list unconditionally, not just files that are actually missing —
   running it can silently produce a handful of `git diff`-visible PNG
   changes even when nothing upstream changed (e.g. from matplotlib
   rendering drift between environments/versions), not necessarily a
   real content update. Check `git status`/`git diff --stat` on
   `visualizacoes/` right after running it, and don't fold those changes
   into an unrelated commit (e.g. a structure-reorg commit) without
   noticing — confirm with the user whether an incidental regen diff
   should be kept or reverted before committing it. If `analise.py`'s
   plotting functions or exported CSV schemas changed since this script
   was last touched, it needs matching edits — it's a snapshot of that
   contract, not a generic tool. Read it before trusting it blindly.

2. **Validate `specs/estrutura_eixos.md` against the real files.**
   ```
   python .claude/skills/export_pdf_report/scripts/gera_estrutura_eixos.py
   ```
   Prints the eixo/subsection/pendente counts and exits non-zero with a
   clear "file X referenced by Y doesn't exist" error if anything is
   broken (e.g. the user renamed a PNG on disk but not in the `.md`, or a
   copy-paste typo in a filename). **Stop here and fix the `.md` (or the
   missing file) if this fails** — never proceed to steps 3-5 against a
   broken structure.

3. **Build the website (`website/`).** Not part of this skill anymore (`specs/website_refactor`):
   ```
   python website/build/build_site.py
   ```
   Writes `website/index.html`, `website/data/*` and generated images; prints file sizes and warns
   above the size budget. Groups ~130 chart/map cards into the 6 eixo tabs; catalog indicators marked
   `status: pendente` render via `emite_bloco_pendente()`. The generated output is committed and
   deployed as-is by `.github/workflows/deploy-relatorio.yml` — details in `website/README.md`.

4. **Build the PDF.**
   1. Build the PDF's source HTML (embeds real PNGs from `visualizacoes/`/
      `mapas/`, resized; groups the same 47 indicators into the same 6
      eixos, with chart-paired data tables moved to a final "Apêndice"
      section instead of sitting inline — `specs/ajuste_eixos/plan.md`
      Bloco 4):
      ```
      python .claude/skills/export_pdf_report/scripts/build_notebook_report.py <scratchpad>/pdf_source.html
      ```
      (Single positional arg. Older docs/comments in this codebase may
      reference a 2-arg `extract_maps.py`-based invocation — that pipeline
      was removed when maps moved to plain `<img>`/PNG embedding; ignore
      any mention of `extract_maps.py` for this step — the file itself was
      deleted in the 2026-09-24 cleanup.)
   2. **Render to PDF with an isolated headless browser.** Use whichever
      Chromium-based browser is actually installed on this machine — check
      both, in order:
      ```
      CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
      EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
      ```
      Chrome is not guaranteed to be present (confirmed absent on at least
      one dev machine this skill was used on, 2026-09) — fall back to Edge
      at the path above if Chrome doesn't exist; both are Chromium and
      accept the same flags below.

      **Critical safety rule, applies to either browser:** always pass
      `--headless=new` together with a **dedicated, throwaway
      `--user-data-dir`** (e.g. a fresh folder under the scratchpad).
      Without an isolated `--user-data-dir`, the browser can attach to the
      user's real running instance/profile and pop open a **visible
      window on the user's desktop** — confirmed while building this
      skill, twice: once from a plain `--version` check with no flags at
      all, and `--headless=new` alone (still sharing the default profile
      dir implicitly) was not sufficient either. Always pass both flags
      together, every invocation, no exceptions.

      **The `file://` URL must use the Windows drive-letter form**
      (`file:///C:/Users/...`), not the POSIX/Git-Bash form the shell
      itself uses (`/c/Users/...`) — passing the latter silently produces
      a near-empty 1-page PDF with no error (confirmed while validating
      this skill, 2026-09) instead of failing loudly. Convert the path
      before building the URL if your working shell is Git Bash/MSYS.

      ```
      BROWSER="$EDGE"   # or "$CHROME", whichever exists
      PROFILE="<scratchpad>/chrome_profile"   # fresh dir, throwaway
      "$BROWSER" --headless=new --disable-gpu --no-sandbox \
        --disable-default-apps --no-first-run --disable-sync \
        --user-data-dir="$PROFILE" \
        --print-to-pdf="<scratchpad>/report.pdf" \
        --no-pdf-header-footer \
        --virtual-time-budget=60000 \
        "file:///C:/path/to/<scratchpad>/pdf_source.html"
      ```
      **`--no-pdf-header-footer` is the flag that actually suppresses the
      browser's injected page header/footer** (URL, date, page number). A
      similarly named `--print-to-pdf-no-header` flag does *not* do this —
      it was tried and produced a PDF with visible browser chrome on every
      page. Use `--no-pdf-header-footer`, not the other one.
      `--virtual-time-budget=60000` (60s) has been sufficient for the full
      ~78-page, ~14MB source HTML; a much shorter budget is not
      necessarily the cause if you still get a tiny/broken PDF — check the
      `file://` path form above first, that has been the actual repeat
      cause of a "renders but comes out wrong" result.
   3. **Verify before handing off.** Page count sanity check:
      ```
      python -c "import pypdf; print(len(pypdf.PdfReader('<pdf>').pages))"
      ```
      Then rasterize a broad sample (first page, several mid-document
      pages across different eixos, a mostly-pendente eixo like Proteção
      or Moradia, the Apêndice, the last page) with PyMuPDF and actually
      look at the PNGs — don't just trust a 0 exit code:
      ```
      python -c "
      import fitz
      doc = fitz.open('<pdf>')
      for i in [0, 5, len(doc)//3, len(doc)//2, 2*len(doc)//3, len(doc)-1]:
          doc[i].get_pixmap(dpi=95).save(f'<scratchpad>/check_{i}.png')
      "
      ```
      Known failure modes to specifically check for (all previously hit
      and fixed while building this skill — don't reintroduce them):
      - **Year columns/axes with a thousands separator or fractional
        ticks** (`"2.000"` instead of `"2000"`, or `"2007.5"` tick
        labels). A column literally named `ano` must never get
        thousands-grouped, and any dataframe read fresh from a CSV needs
        `df['ano'].astype(str)` before plotting a time series, or
        seaborn treats a numeric `ano` as a continuous axis instead of
        one tick/year.
      - **Wide tables (>6-7 columns) silently clipped/scrollable.** A
        `<table>` wider than the printable page area doesn't wrap in
        print output — it just overflows with an inert scrollbar baked
        into the image. `table_html(..., clean_headers=True)` and the
        `.plain.wide` CSS class handle this.
      - **Percent columns on the wrong scale.** Most `tabelas_finais/*.csv`
        percentage columns are already 0-100. At least one (PNAD
        frequência escolar's `Total`) is a 0-1 fraction — multiply by 100
        before treating it as a `pct_cols` column.
      - Browser header/footer leaking onto every page (see the flag note
        above).
      - Dark theme leaking in from the rendering environment's OS setting
        — the doc forces `<html data-theme="light">` + a `color-scheme`
        meta tag; don't drop those if editing the template.
      - A near-empty 1-2 page PDF despite a 0 exit code — see the
        `file://` path-form note above; this is the most likely cause,
        check it before anything else.
   4. **Place the final file.** Copy the verified PDF to
      `relatorio/analise_primeira_infancia.pdf`. It is **not** in
      `.gitignore` (unlike most of `relatorio/*.html`) — ask the user
      before committing it if that wasn't already part of the request,
      since it's a ~25-30MB binary regenerated from other tracked/ignored
      sources.

5. **Build the DOCX curation export.**
   ```
   python .claude/skills/export_pdf_report/scripts/gera_docx_curadoria.py [<docx_anterior>]
   ```
   Writes `relatorio/curadoria_textos.docx` (hardcoded output path) — 1
   heading per eixo/subsection, real (resized) images per
   visualização/mapa, one bookmarked placeholder text block per
   image/option for a human to edit outside the notebook. **Pass the
   existing `relatorio/curadoria_textos.docx` itself as `<docx_anterior>`
   when regenerating after a structure edit**, so already hand-edited text
   survives (matched by a stable per-image bookmark ID) and any text whose
   underlying indicator got removed/renamed lands in a "Textos órfãos"
   appendix instead of silently vanishing — never regenerate this file
   from scratch (omitting `<docx_anterior>`) once real curation has begun,
   or edited text is lost. See `specs/ajuste_eixos/plan.md` Bloco 5 for
   the bookmark/ID design if extending this script.

6. **Sync hand-curated DOCX text back into HTML/PDF/`analise.py`.** Once
   someone has actually edited placeholder text in
   `relatorio/curadoria_textos.docx` (replacing lorem ipsum with real
   analysis), run:
   ```
   python .claude/skills/export_pdf_report/scripts/sincroniza_docx.py relatorio/curadoria_textos.docx [<pdf_source_out>]
   ```
   Detects which bookmarks genuinely changed (exact comparison against the
   deterministic lorem ipsum that bookmark's ID would still produce — not
   a heuristic), writes them to `relatorio/textos_curados.json` (which
   `website/build/build_site.py`/`build_notebook_report.py` both read via
   `_texto_analise(seed)` before falling back to lorem — this is *why*
   Bloco 3/4's seeds were aligned to real filenames instead of pill
   labels, see `specs/ajuste_eixos/specs.md` §9.3), regenerates
   `website/` (the site) and the PDF's source HTML, and inserts/updates a
   markdown note in `analise.py` right after the code cell that produces
   the matching chart/table (idempotent — a marker comment prevents
   duplicate notes on repeat runs; never touches a code cell). This script
   does **not** render the final PDF binary — run step 4.2-4.4 above
   afterward if you want `relatorio/analise_primeira_infancia.pdf`
   updated too. One identifier gap is known and accepted (not a bug):
   the ~24 HTML pill options with no single backing file (granular cuts
   the catalog crosswalk doesn't enumerate) — curated text for those needs manual
   placement. (The 2 PDF "out_pair" CadÚnico cases used to be a second gap; since
   2026-09-24 `_texto_par` joins the curated texts of both files.) Since 2026-09-24 this
   script only runs `jupytext --sync` if `analise.ipynb` already exists (it's a disposable copy).

7. **Incorporate an "update" DOCX edited outside Word (Google Docs), with review tracking.**
   Files like `relatorio/curadoria_textos_update_N.docx` come back **without bookmarks** (the
   Google Docs round trip drops them) and are often based on an older structure (old filenames,
   subsections that changed). Don't copy texts by hand — run, with ALL update files in
   chronological order:
   ```
   python .claude/skills/export_pdf_report/scripts/incorpora_update_docx.py relatorio/curadoria_textos_update_1.docx relatorio/curadoria_textos_update_2.docx --saida <scratchpad>/casamento.json --controle relatorio/controle_revisao.json --datas 2026-09-23,2026-09-24
   python .claude/skills/export_pdf_report/scripts/gera_docx_curadoria.py relatorio/curadoria_textos.docx --textos <scratchpad>/casamento.json
   python .claude/skills/export_pdf_report/scripts/sincroniza_docx.py relatorio/curadoria_textos.docx <scratchpad>/pdf/pdf_source.html   # create <scratchpad>/pdf first
   ```
   then render the PDF (step 4.2-4.4). The matcher pairs texts by H3 title (normalized, with the
   known file renames in `RENOMES`), untitled images by position inside the H2, and H2-level text
   by subsection; anything unmatched is reported, never dropped. `relatorio/controle_revisao.json`
   records per block `revisado` (confirmed unchanged in a later round) / `atualizado` (new or
   changed in its last round), items new since the last update, editorial notes and relocation
   cases; its `alertas` field (and `realocar[].sugestao`) is **hand-edited and preserved**. The DOCX
   generator reads it to put a status mark at the end of each H2/H3 (so the Word Sumário doubles
   as a checklist) and a "Controle de revisão" table right after the Sumário. Never edit the
   user's curated text to fix an alert — flag it and let them decide (constitution).
   Verify: every matched text is under its bookmark in the new DOCX, no previously curated text
   lost, and (after rendering) every `textos_curados.json` entry appears in the PDF text —
   except section-level texts of subsections that have charts, which intentionally aren't published.

## Known limitations to mention if relevant

- CadÚnico charts reflect the last saved `tabelas_finais/` export, not a
  live CTPE query; steps 3-5 above don't touch the DB at all, so they
  can't refresh CadÚnico data further (only `analise.py` itself can, via
  step 1's caveat above not applying to CadÚnico specifically — it needs a
  real notebook re-run against the live DB).
- Some chart end-labels can visually overlap when two series end on close
  values — a cosmetic quirk of the matplotlib defaults `analise.py` uses,
  not something to "fix" here since the whole point of the PDF/DOCX is
  fidelity to the notebook's own rendering.
- `analise.py` has a final "Análise / Relatório" section (markdown notes
  only, no code output) that all three artifacts deliberately omit —
  it's editorial scaffolding for a future narrative synthesis by eixo, not
  publishable content yet.
- 16 catalog indicators (`specs/estrutura_eixos.md`, `status: pendente`)
  have no real chart/map yet — all three artifacts show them as a labeled
  placeholder, never a silently missing/empty section. Importing the
  underlying data for these is tracked in `specs/roadmap.md`, not this
  skill's job.
