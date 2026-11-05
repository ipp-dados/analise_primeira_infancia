---
name: export_pdf_report
description: Build the final report PDF of the primeira-infancia analysis -- an ABNT technical report written in LaTeX (relatorio/latex/, abnTeX2 + xelatex). Since 2026-11-05 its chapters are hand-edited .tex files (relatorio/latex/capitulos/) while the data they cite -- print versions of analise.py's own charts/maps (visualizacoes/a4/, mapas/a4/), in-body tables and appendix tables from tabelas_finais/ -- is still generated. NOT the website/ static site's SVG charts. Use when the user asks for the PDF/report, to edit its text, cover or structure, to regenerate or publish it after the notebook/data change, or to change its tables or sources list.
---

# Export the report (PDF, LaTeX)

The final report is a **LaTeX document** (ABNT NBR 10719 technical report, class `abntex2`, compiled with
`xelatex` via `latexmk`) in `relatorio/latex/`. Design, decisions and history: `specs/2026-09-25_relatorio_latex/`
(read `specification.md` §8 for decisions D1-D6 and §5.1 for the print-figure rules before changing the look);
the switch to hand-edited chapters, the new cover/title/staff pages and the end of the DOCX curation:
`specs/2026-11-05_versao_final_site` (R5, R6, D5-D8). Exclusions decided by the team: `specs/exclusoes.md`.

**History (don't go back without a new decision):** until 2026-09-25 the PDF was an HTML page printed by headless
Edge; replaced by LaTeX (`specs/2026-09-25_relatorio_latex`, D2). Until 2026-11-05 the chapters were generated from
`specs/estrutura_eixos.md` + `relatorio/textos_curados.json` and the text was curated in a DOCX round-tripped through
Google Docs; since then **the text is written directly in the `.tex` chapters** and `textos_curados.json` is the
**site's** text only. The DOCX scripts were removed (git tag `rodada/curadoria_docx` keeps them).

## What is where

| Path | What | Edited by |
| :--- | :--- | :--- |
| `relatorio/latex/relatorio.tex` | master: class, metadata (`\autor`, `\preambulo`), order of parts, `\input` of each chapter | hand |
| `relatorio/latex/capitulos/NN_<eixo>.tex` | **the 9 chapters** (Introdução, 7 eixos, Considerações finais): text, sections, `\figura{…}`, `\input{gerado/tabelas_corpo/…}`, `\vertabelas{\ref{tab:…}}` | **hand** |
| `relatorio/latex/pretextual/` | `capa.tex` (two options A/D under evaluation), `folha_rosto.tex`, `expediente.tex` (direção + equipe técnica), `resumo.tex` (one page), `siglas.tex`; images by `build/gera_capa_imagens.py` | hand |
| `relatorio/latex/textual/como_ler.tex` | "Como ler este relatório" (facts, not analysis) | hand |
| `relatorio/latex/estilo.sty` | fonts, colours, ABNT captions, chapter openers, callout boxes, `\figura` | hand |
| `relatorio/latex/fontes.bib` | **Fontes** list (NBR 6023) + `padroes` regex linking each `fonte_dados` text to an entry | hand |
| `relatorio/latex/fontes/` | Fraunces + IBM Plex Sans (OFL), used by LaTeX **and** by the print figures | vendored |
| `relatorio/latex/build/gera_latex.py` | builds the generated parts (appendix, in-body tables, nocite, watermark switch, icons), **checks the chapters**, compiles | code |
| `relatorio/latex/build/tabelas.py` | CSV → ABNT table; per-table rules (`AJUSTES`), merges (`SUBSTITUI_NO_PDF`), size rules | code |
| `relatorio/latex/build/gera_capa_imagens.py` | cover photo (faint / navy texture) and the dark/light IPP logo PNGs | code |
| `relatorio/latex/build/inventario_fontes.py` | sources inventory (`relatorio/inventario_fontes.md/.csv`) | code |
| `relatorio/latex/gerado/` | generator output: `apendices.tex`, `tabelas_corpo/*.tex`, `nocite.tex`, `aviso.tex`, `icones.tex` | **never by hand** |
| `relatorio/latex/_build/` | latexmk aux, image cache, `relatorio.pdf` | gitignored |
| `visualizacoes/a4/`, `mapas/a4/`, `visualizacoes/a4/_manifesto.csv` | print figures + their title/source/unit, written by `analise.py` | gitignored, generated |

## Pipeline

Run everything from the project root.

1. **Figures (print versions).** They come only from a **full run of `analise.py`** (every chart/map function also
   saves `…/a4/<name>.pdf` when `GERA_VARIANTE_A4 = True`). CadÚnico needs the `analises_env` conda env and `.env`:
   ```
   MPLBACKEND=Agg "<conda>/envs/analises_env/python.exe" -X utf8 analise.py
   ```
   Check the log for `[variante A4] … falhou` lines (a failed print figure falls back to the screen PNG).

2. **Build the PDF.** `gera_latex.py` needs the **base Python** (the conda env lacks `svgelements`, used for the icons).
   ```
   python relatorio/latex/build/gera_latex.py              # full document -> relatorio/latex/_build/relatorio.pdf
   python relatorio/latex/build/gera_latex.py --sem-pdf    # only regenerate gerado/*.tex and run the checks
   python relatorio/latex/build/gera_latex.py --publicar   # full document, then copy to relatorio/analise_primeira_infancia.pdf
   ```
   It still reads `specs/estrutura_eixos.md` to build the **appendix tables, the in-body tables and their labels**,
   then **checks the chapters**: every `\figura` file, every `\input{gerado/…}` and every `\ref{tab:…}` they cite must
   exist, or the build stops with the list. It prints `undefined` references and overfull boxes > 5 pt.
   `--exportar-capitulos` was the one-time export (2026-11-05); it refuses to overwrite the chapters
   (`--forcar` would discard the hand edits -- never without the user's explicit OK).
   `--publicar` replaces the local `relatorio/analise_primeira_infancia.pdf` — only with the user's OK. That file is
   gitignored: readers get it from a **GitHub Release** (the site links to
   `releases/latest/download/analise_primeira_infancia.pdf`), so publishing = `--publicar` + a new Release with the PDF
   attached under the same file name. Never commit the PDF.

3. **Verify.** Page count and size (budget < 20 MB); rasterize a sample with PyMuPDF and look at it (covers, title
   page, staff page, summary on one page, contents, a chapter opener, a map page, an appendix table, Fontes, last page);
   search the extracted text for internal notes that must not be published (`specs/`, "baixar dados").

4. **Sources inventory** (for the team, not in the PDF): `python relatorio/latex/build/inventario_fontes.py`.
   A new data source needs a `fontes.bib` entry with a `padroes` regex, or it shows up as an alert and without
   citation. (Known issue, ROADMAP: it attributes sources by "neighbourhood" in `analise.py` and can mislabel a table.)

## Editing the report

- **Text**: edit the chapter `.tex` directly. Each file starts with a comment explaining what is hand-made and what is
  generated. A number typed in the text does **not** update when the data changes — after a data refresh, re-check the
  numbers cited in the chapters against `tabelas_finais/` (the planned number check, ROADMAP "Próximas features" 2,
  should also read the `.tex`). Shell heredocs mangle backslashes: edit `.tex` files with the editor or a script file.
- **New indicator in the PDF**: add it to `specs/estrutura_eixos.md` (so its tables reach the appendix with a label),
  run `--sem-pdf`, then add the `\section`, the `\figura{…}` (copy an existing one: type, PDF path, caption, source
  line with `\citeonline`, label) and the `\vertabelas{Tabela~\ref{tab:…}}` line to the chapter.
- **Indicators without data are not published** (user's decision, 2026-11-05): no "em desenvolvimento" box in the PDF
  or the site; they stay `status: pendente` in the crosswalk and in `docs/dados_faltantes.csv` / ROADMAP.
- **Cover**: two options (A light, D navy) are both in `capa.tex` until the user chooses; delete the other then. Both
  show an "EM DESENVOLVIMENTO" label while `relatorio/publicacao.json` says so (`\ifemdesenvolvimento`, written by
  `gera_latex.py` into `gerado/aviso.tex`) — the page watermark is hidden under the cover photo.
- **Staff page** (`expediente.tex`): names and positions given by the user; the mayor since 2026-03-20 is Eduardo
  Cavaliere. Keep `\autor` in `relatorio.tex` in sync with the technical team.

### Rules that are easy to break

- **Tables**: most go to the appendix; > 200 rows stay digital-only; bairro × year tables print only the latest
  complete year; bairro tables print two-up, alphabetical, with the **official bairro name looked up by code**;
  repeated tables are merged via `SUBSTITUI_NO_PDF`. Per-table titles/columns/pivots live in `AJUSTES` — use the
  **original CSV column names** there. `tabela_no_texto:` in the crosswalk sends a table to
  `gerado/tabelas_corpo/<stem>.tex` for an `\input` in the chapter instead of the appendix.
- **Figures**: sizes/labels/palette of the print versions are fixed in `primeira_infancia/impressao.py`
  (`_rc_impressao`, `ROTULOS_EIXO`, `_PALETA_IMPRESSAO`, 95th-percentile colour cap on bairro rate maps). Change them
  there, never by editing PDFs. No map paints land blue (blue is water only).
- **"EM DESENVOLVIMENTO" watermark**: `relatorio/publicacao.json` (`em_desenvolvimento`, `marca_dagua_pdf`) — the same
  switch as the site's yellow strip; the two leave together. `gerado/aviso.tex` uses `draftwatermark` 3.3 with a TikZ
  node for transparency (MiKTeX has no `alpha` key; `transparent` is pdfTeX-only) and an `\AtBeginDocument` TikZ node
  with the same opacity (without it the first page gets an opaque mark).
- **LaTeX gotchas already hit**: abnTeX2 already defines `\fonte` and `\nota`; `\nocite{*}` pulls abnTeX2's internal
  entries (use `gerado/nocite.tex`); BibTeX runs in `_build/` (the generator sets `BIBINPUTS`); a float extension named
  `log` collides with LaTeX's log; TikZ `remember picture` needs two passes (latexmk does it); in a TikZ node, put the
  font in `font={…}` — a size switch inside the node text resets after `\\`; `\vspace*` right after a
  `tikzpicture` needs a `\par` first.

## Known limitations

- CadÚnico numbers come from the last notebook run against the live DB; nothing here queries it.
- The site's grouping is hardcoded in `website/build/build_site.py`; a structural edit of `estrutura_eixos.md` reaches
  the PDF's appendix automatically, the chapters and the site only by hand.
- `analise.py`'s final "Análise / Relatório" section is editorial scaffolding and is not published.
