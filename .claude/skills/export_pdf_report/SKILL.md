---
name: export_pdf_report
description: Build the final report PDF of the primeira-infancia analysis -- an ABNT technical report written in LaTeX (relatorio/latex/, abnTeX2 + xelatex) whose chapters are generated from specs/estrutura_eixos.md and relatorio/textos_curados.json, with print versions of analise.py's own charts/maps (visualizacoes/a4/, mapas/a4/) -- NOT the website/ static site's SVG charts. Use when the user asks for the PDF/report, to regenerate or publish it after the notebook/data/texts change, or to change its structure, look, tables or sources list. Also covers the DOCX curation export (relatorio/curadoria_textos.docx) and syncing hand-edited DOCX text back into the site, the PDF and analise.py -- use it too when the user edits specs/estrutura_eixos.md and asks to "update the report(s)".
---

# Export the report (PDF, LaTeX) and the curation DOCX

The final report is a **LaTeX document** (ABNT NBR 10719 technical report, class `abntex2`, compiled with
`xelatex` via `latexmk`) in `relatorio/latex/`. Design, decisions and history: `specs/2026-09-25_relatorio_latex/`
(read `specification.md` §8 for decisions D1-D6 and §5.1 for the print-figure rules before changing the look).
Exclusions decided by the team (what is left out of the PDF/site and why): `specs/exclusoes.md`.

**History (don't go back without a new decision):** until 2026-09-25 the PDF was an HTML page
(`scripts/build_notebook_report.py`) printed by headless Edge — no cover/abstract/contents, grouping hardcoded
in Python, 49 MB. Replaced by the LaTeX report (`specs/2026-09-25_relatorio_latex`, D2); `build_notebook_report.py` and
`regen_missing_pngs.py` (which re-drew some screen PNGs without a source line) were removed on 2026-09-25, after
the LaTeX PDF passed validation (git history keeps them). Before that, an even older version converted
the site's HTML to PDF — rejected by the user ("keep the visual style of the visualizations used in the
notebook, not the html"). The PDF still uses **the notebook's own figures**, now in their print version.

## What is where

| Path | What | Edited by |
| :--- | :--- | :--- |
| `relatorio/latex/relatorio.tex` | master: class, metadata, order of parts | hand |
| `relatorio/latex/estilo.sty` | fonts, colours, ABNT captions, chapter openers, callout boxes | hand |
| `relatorio/latex/pretextual/` | cover, title page (team names), abbreviations | hand |
| `relatorio/latex/textual/como_ler.tex` | "Como ler este relatório" (facts, not analysis) | hand |
| `relatorio/latex/fontes.bib` | **Fontes** list (NBR 6023) + `padroes` regex linking each `fonte_dados` text to an entry | hand |
| `relatorio/latex/fontes/` | Fraunces + IBM Plex Sans (OFL), used by LaTeX **and** by the print figures | vendored |
| `relatorio/latex/build/gera_latex.py` | generator + compile (chapters, appendix, abstract, icons) | code |
| `relatorio/latex/build/tabelas.py` | CSV → ABNT table; per-table rules (`AJUSTES`), merges (`SUBSTITUI_NO_PDF`), size rules | code |
| `relatorio/latex/build/inventario_fontes.py` | sources inventory (`relatorio/inventario_fontes.md/.csv`) | code |
| `relatorio/latex/build/gera_icones.py` | site's Lucide icons → TikZ macros | code |
| `relatorio/curadoria/` | structure of the eixos (`gera_estrutura_eixos.py`, also imported by the site and LaTeX generators), DOCX curation export/sync/updates, published-text validation — moved out of this skill's `scripts/` in `specs/2026-09-28_organizacao`; the skill only calls them | code |
| `relatorio/latex/gerado/` | generator output (committed, diffable) | **never by hand** |
| `relatorio/latex/_build/` | latexmk aux, image cache, `relatorio.pdf` | gitignored |
| `visualizacoes/a4/`, `mapas/a4/`, `visualizacoes/a4/_manifesto.csv` | print figures + their title/source/unit, written by `analise.py` | gitignored, generated |

## Pipeline

Run everything from the project root.

1. **Figures (print versions).** They come only from a **full run of `analise.py`** (every chart/map
   function also saves `…/a4/<name>.pdf` when `GERA_VARIANTE_A4 = True` — see the "🖨️ Variante de impressão"
   section of the notebook). CadÚnico needs the `analises_env` conda env and `.env`:
   ```
   MPLBACKEND=Agg "<conda>/envs/analises_env/python.exe" -X utf8 analise.py
   ```
   Check the log for `[variante A4] … falhou` lines — a failed print figure falls back to the screen PNG and
   `gera_latex.py` lists every fallback. There is no shortcut script any more: figures come from the notebook.
   A full run also rewrites some tracked outputs (older PNGs/CSVs that are still versioned): check
   `git status` and ask the user before committing them.

2. **Validate the structure.**
   ```
   python relatorio/curadoria/gera_estrutura_eixos.py
   ```
   Fails loudly if any file referenced in `specs/estrutura_eixos.md` is missing. Fix before continuing.

3. **Build the PDF.**
   ```
   python relatorio/latex/build/gera_latex.py              # full document -> relatorio/latex/_build/relatorio.pdf
   python relatorio/latex/build/gera_latex.py --eixo 5     # only eixo 5 in the body (fast iteration on the look)
   python relatorio/latex/build/gera_latex.py --sem-pdf    # only regenerate gerado/*.tex
   python relatorio/latex/build/gera_latex.py --publicar   # full document, then copy to relatorio/analise_primeira_infancia.pdf
   ```
   **`specs/estrutura_eixos.md` is read at build time** — editing it (moving an indicator, renaming a
   subsection, `status: pendente`) is enough for the PDF (unlike the site, whose grouping is still hardcoded).
   The build prints: figures still without a print version, keys still in lorem ipsum, curated texts whose
   figure is not in the report, `undefined` references and overfull boxes > 5 pt.
   `--publicar` replaces the file the site links to — only with the user's OK.

4. **Verify** (`specs/2026-09-25_relatorio_latex/validation.md` has the full list). At least: page count and size
   (budget < 20 MB), rasterize a sample with PyMuPDF and look at it (cover, contents, a chapter opener, a map
   page, an "indicador em desenvolvimento" box, an appendix table, Fontes, last page), and search the extracted
   text for internal notes that must not be published (`specs/`, team names, "baixar dados").

5. **Sources inventory** (for the team, not in the PDF):
   ```
   python relatorio/latex/build/inventario_fontes.py
   ```
   Writes `relatorio/inventario_fontes.md/.csv`: each `fontes.bib` entry → the charts/maps/tables it produces,
   each file → its source, plus alerts (files from commented-out code, sources without a bib entry, `fonte:`
   in the `.md` disagreeing with `fonte_dados`). Alerts are reported, never auto-fixed. A new data source needs
   a `fontes.bib` entry with a `padroes` regex, or it shows up as an alert and without citation.

### Rules that are easy to break

- **Tables**: most go to the appendix; > 200 rows stay digital-only; bairro × year tables print only the latest
  complete year; bairro tables print two-up, alphabetical, with the **official bairro name looked up by code**
  (never by the name string); repeated tables are merged via `SUBSTITUI_NO_PDF`. Per-table titles/columns/pivots
  live in `AJUSTES` — use the **original CSV column names** there.
- **"Indicador em desenvolvimento" boxes print a fixed public sentence** (`TEXTO_PENDENTE`, in
  `relatorio/curadoria/gera_estrutura_eixos.py`) **plus the item's `motivo:`** (formal public reason, required on every
  `status: pendente` item; PDF and site builds fail without it — `specs/2026-09-29_alinhamento_pdf_site` D5). The site
  shows the same pair. The `nota:` lines in `estrutura_eixos.md` are internal team notes and are never printed.
- **`tabela_no_texto:`** puts a table in the section body (portrait unless it really doesn't fit, curated text after
  it) instead of the appendix — use it when the site shows that table inside the card (D3).
- **Figures**: sizes/labels/palette of the print versions are fixed in `analise.py` (`_rc_impressao`,
  `ROTULOS_EIXO`, `_PALETA_IMPRESSAO`, D5 = 95th-percentile colour cap on bairro rate maps). Change them there,
  never by editing PDFs. New unit labels go in `ROTULOS_EIXO`/`ROTULOS_A4_ARQUIVO`.
- **"EM DESENVOLVIMENTO" watermark**: `relatorio/publicacao.json` (`em_desenvolvimento`, `marca_dagua_pdf`) —
  the same switch as the site's yellow strip; the two leave together (`specs/2026-09-28_website_mobile`).
  `gera_latex.py` writes `gerado/aviso.tex` (`\input` in the preamble of `relatorio.tex`): `draftwatermark` 3.3 with
  a TikZ node for transparency — MiKTeX's draftwatermark has no `alpha` key and the `transparent` package is
  pdfTeX-only. The `\AtBeginDocument` TikZ node with the same opacity is required: without it the cover (first page)
  gets the watermark opaque (missing `ExtGState pgf@ca0.16`). Check every page with PyMuPDF warnings after changing it.
- **Escaping**: curated text is escaped by `esc()` (`% $ & _ #`…); never rewrite a curated text to make it compile.
- **LaTeX gotchas already hit**: abnTeX2 already defines `\fonte` and `\nota` (don't redefine); `\nocite{*}`
  pulls abnTeX2's internal option entries (use `gerado/nocite.tex`); BibTeX runs in `_build/`, so the generator
  sets `BIBINPUTS`; a float extension named `log` collides with LaTeX's own log. Shell heredocs in Git Bash
  mangle backslashes — edit `.tex`/`.py` files with the editor or a script file, not inline `sed`/heredoc.

## Curated text (DOCX ↔ site, PDF, analise.py)

Text lives in `relatorio/textos_curados.json`, keyed by figure file stem (`taxa_mortalidade_precoce_ano`),
`introducao`, and — since `specs/2026-09-25_relatorio_latex` Block 6 — the report-level blocks from
`blocos_relatorio()` (`relatorio/curadoria/gera_estrutura_eixos.py`): `resumo`, `achados_<eixo>` (one finding per line),
`introducao_<eixo>` (the eixo's opening text, ≤ 100 words, right below the findings — `specs/2026-09-28_melhorias_site`
U2), `sintese_<eixo>`, `consideracoes_finais` (`<eixo>` = `chave_eixo()`, e.g. `familia_e_cuidados`). Without
curated text the PDF shows deterministic lorem ipsum identical to the site's for the same key (decision D4). The site
reads `achados_`, `introducao_` and `sintese_` (falling back to `conclusao-<sid>`); `resumo` and `consideracoes_finais`
are PDF-only.

**Lorem is capped at 150 words** (range 100-150; `resumo`/Introdução/Considerações finais placeholders 150; eixo
opening 90) in the three generators — site `_lorem`, LaTeX `lorem`, DOCX `_lorem` — since
`specs/2026-09-28_melhorias_site` U3. Changing a placeholder means the old one in the DOCX no longer matches exactly:
`gera_docx` drops the previous DOCX's lorem (`_eh_lorem`) instead of carrying it forward, and
`sincroniza_docx.eh_lorem_ipsum` treats any lorem-like text as placeholder, so an old placeholder never leaks into
`textos_curados.json`. After such a change, regenerate the DOCX and check that the sync changes no key.

6. **Build the DOCX curation export.**
   ```
   python relatorio/curadoria/gera_docx_curadoria.py relatorio/curadoria_textos.docx
   ```
   One heading per eixo/subsection, the (screen) images, one bookmarked text block per image, plus the report
   blocks (Resumo after the Introduction; Principais achados and Síntese at the start/end of each eixo;
   Considerações finais at the end). **Always pass the existing DOCX** so curated text survives (matched by
   bookmark); text whose indicator left the structure goes to a "Textos órfãos" appendix, never lost.
   `relatorio/controle_revisao.json` is loaded automatically (status marks + "Controle de revisão" table).
   After regenerating, check that every non-lorem text of the previous DOCX is still there under the same
   bookmark (`extrai_textos_por_bookmark` on both files).

7. **Sync hand-curated DOCX text back.**
   ```
   python relatorio/curadoria/sincroniza_docx.py relatorio/curadoria_textos.docx
   ```
   Detects genuinely edited blocks (exact comparison with the placeholder each bookmark would get — for the report
   blocks, `placeholder_bloco()`), merges them into `textos_curados.json`, regenerates the site
   (`website/build/build_site.py`) and **the LaTeX report** (`gera_latex.py`, PDF in `_build/`; publish with
   `--publicar`), and updates the curator notes in `analise.py` next to the matching figure (never touches code
   cells). The old second argument (`<pdf_source_out>`) is ignored.

8. **Incorporate an "update" DOCX edited outside Word (Google Docs), with review tracking.** The new file arrives
   as `relatorio/curadoria_textos_update.docx`; past updates live in `relatorio/textos_updates_antigos/`
   (`curadoria_textos_update_<N>.docx`, N = round number, 1-5 so far). `A=relatorio/textos_updates_antigos`:
   ```
   # 1. what did the curator really change? (diff against the update it was based on -- usually the previous one)
   python relatorio/curadoria/compara_updates.py $A/curadoria_textos_update_<N-1>.docx relatorio/curadoria_textos_update.docx
   # 2. review status across ALL rounds (copy the new file to <scratchpad>/curadoria_textos_update_<N>.docx first,
   #    so the round id in controle_revisao.json is the archived name)
   python relatorio/curadoria/incorpora_update_docx.py $A/curadoria_textos_update_1.docx … <scratchpad>/curadoria_textos_update_<N>.docx --saida <scratchpad>/casamento_todos.json --controle relatorio/controle_revisao.json --datas 2026-09-23,…
   # 3. revised matching (only the texts from step 1) -> DOCX -> JSON/site/PDF/analise.py
   python relatorio/curadoria/gera_docx_curadoria.py relatorio/curadoria_textos.docx --textos <scratchpad>/casamento_rev.json
   python relatorio/curadoria/sincroniza_docx.py relatorio/curadoria_textos.docx
   python relatorio/latex/build/gera_latex.py --publicar
   # 4. every curated text on the site and in the PDF (exit 1 if one is missing)
   python relatorio/curadoria/valida_textos_publicados.py
   # 5. archive: relatorio/curadoria_textos_update.docx -> $A/curadoria_textos_update_<N>.docx
   ```
   Google Docs drops bookmarks; the matcher pairs texts by H3 title (with known renames in `RENOMES`), untitled
   images by position, H2-level text by subsection; anything unmatched is reported, never dropped. `alertas` and
   `realocar[].sugestao` in `controle_revisao.json` are hand-edited and preserved. Never edit the user's curated
   text to fix an alert — flag it and let them decide.
   **Don't feed the matcher's `casamento_todos.json` straight into the DOCX** (it re-applies everything already
   decided): it concatenates the text of a figure that left the report (count map, E8 absolute counts) into the
   bookmark of its neighbour (rate map/chart at the same image position), keeps Google Docs duplicated paragraphs
   and brings back texts corrected after the update's base was downloaded. Build `casamento_rev.json`
   (`{"textos": {bookmark: {"texto": …}}}`, bookmark = `_bookmark_name(stem)`) with only the texts
   `compara_updates.py` reports as `NOVO`/`DIFERENTE_DO_JSON`; a text of a figure outside the report goes under its
   own stem and lands in "Textos órfãos". The recomputed `controle_revisao.json` drops the `correcoes` round from
   `rodadas` (re-insert it by hand) and `ajustes_manuais` entries whose corrected text the new update already
   carries should be removed (the computed status then applies). Leftover placeholder words pasted along with the
   text (e.g. a trailing lorem `sunt.`) are not the curator's text: remove them and record it in
   `alertas_resolvidos`.

## Known limitations

- CadÚnico numbers come from the last notebook run against the live DB; nothing here queries it.
- The site's grouping is still hardcoded in `website/build/build_site.py`; a structural edit of
  `estrutura_eixos.md` reaches the PDF and DOCX automatically but the site only by hand (see `build_website`).
- `analise.py`'s final "Análise / Relatório" section is editorial scaffolding and is not published.
- Citations in "Fonte:" lines print corporate authors in capitals (abnTeX2 behaviour); a `fontes.bib` adjustment
  is listed for Block 7 of `specs/2026-09-25_relatorio_latex`.
