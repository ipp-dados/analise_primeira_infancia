# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Data analysis project for early-childhood (primeira infância, 0-6 anos) indicators in the
city of Rio de Janeiro, combining Censo (IBGE), CadÚnico, DataSUS/Tabnet, SISVAN, IBGE SIDRA
and cobertura vacinal data. Everything lives in one notebook-as-script,
`analise.py` (2500+ lines, Jupytext `py:percent` format), plus generated
outputs (tables, charts, choropleth maps, an HTML report, a PDF report).

Content and commit messages are in Portuguese (pt-BR); code identifiers mix
Portuguese and English. Match the existing language when editing.

## Commands

```bash
pip install -r requirements.txt          # deps (geopandas/contextily stack, jupytext, etc.)

jupytext --to notebook analise.py        # (re)generate analise.ipynb from the .py source
jupytext --sync analise.py               # sync analise.ipynb <-> analise.py after editing the notebook
```

The CadÚnico section needs the `.env` DB credentials **and** a kernel with
`psycopg` 3 (dev machine: conda env `analises_env`; base Anaconda only has
`psycopg2`). Every sub-municipal CadÚnico output goes through
`suprime_celulas_pequenas` (< 20 families blanked) before it is written —
see `specs/2026-09-23_recortes_cadunico/specification.md` §5. A full run also writes the
print version of every figure used by the PDF report (`GERA_VARIANTE_A4`,
section "🖨️ Variante de impressão"; `visualizacoes/a4/`, `mapas/a4/`).

There is no test suite, linter, or build step — `analise.py` is the
deliverable, run cell-by-cell in Jupyter (via Jupytext) or top-to-bottom as a
script. **`analise.py` (the `.py:percent` file) is the source of truth that
gets committed; `analise.ipynb` is a generated artifact** — never hand-edit
the notebook's outputs and expect them to matter, and `*.ipynb` is
gitignored.

Three project skills wrap multi-step regeneration pipelines — prefer them over
reimplementing this logic:
- `generate_map` — produces a choropleth PNG via `mapa_coropletico_bairros` (defined in `analise.py`).
- `build_website` — regenerates/checks the static site in `website/` (`website/build/build_site.py`) and describes its manual GitHub Pages deploy.
- `export_pdf_report` — builds the final report: an ABNT technical report in LaTeX (`relatorio/latex/`, abnTeX2 + xelatex; `specs/2026-09-25_relatorio_latex`) whose chapters are generated from `specs/estrutura_eixos.md` + `relatorio/textos_curados.json` at build time, with print versions of `analise.py`'s own figures (`visualizacoes/a4/`, `mapas/a4/`) and `tabelas_finais/` tables in the appendix; also the DOCX curation export and the DOCX → site/PDF/`analise.py` text sync. Distinct from and NOT related to the `website/` static site's SVG charts — see below.

## Architecture

### `analise.py` structure (Jupytext `py:percent`, sections marked `# %% [markdown]`)

1. **📦 Pacotes e Funções Auxiliares** (top of file) — imports, DB connection
   (`connect_db_ctpe`, reads `.env`), and **every** reusable
   cleaning/wrangling function (`limpeza_tabnet_bairros`, `carrega_raca_bairro`,
   `carrega_causas_evitaveis_*`, `agrega_grupo_cid`, `carrega_sidra_longo`,
   `junta_codbairro_por_bairro`, `agrega_bairros_por_nivel`, ...) and
   visualization function (`serie_temporal`, `grafico_barra`,
   `grafico_barra_agrupado`, `serie_temporal_multipla`,
   `mapa_coropletico_bairros`). **All new reusable logic goes here, not inline
   in an analysis section below** — sections only call these functions.
2. Analysis sections in source order: Censo 2022, CadÚnico, DataSUS/Tabnet
   (nascidos vivos, baixo peso, mortalidade neonatal, óbitos gravidez/puerpério,
   óbitos por causas evitáveis by CID-10 group/subgroup and by CAP), SISVAN,
   Cobertura Vacinal EPI, IBGE SIDRA/PNAD/Censo Escolar. **This is the
   technical build order (each section's data feeds later joins) and is
   deliberately left unchanged** — see the note below.
3. A closing "Análise / Relatório" section (markdown notes only, no code
   output) — deliberately omitted from both the HTML and PDF reports. Its
   subtitles are the 6 active policy axes (`specs/estrutura_eixos.md`), not
   the source-order sections above.

**Presentation order vs. build order** (`specs/2026-09-22_ajuste_eixos/`): the sections
above are ordered by *data dependency* (a section may read results computed
by an earlier one, e.g. the bairro-level joins near the end of the file read
nascidos vivos/baixo peso/óbitos already computed above) — this order is not
reorganized when the *published* structure changes. The `website/` site,
the PDF, and the DOCX curation export are instead grouped by **eixo da
política municipal de primeira infância** (Prioridade, Inclusão, Família e
Cuidados, Proteção, Alimentação, Moradia), read from `specs/estrutura_eixos.md`
— a hand-editable crosswalk from the indicator catalog
(`dados_locais/painel_primeira_infancia_cesta_indicadores.xlsx`) to the real
visualization/map/table files. To change the published grouping, edit that
`.md` file, not this one's section order (see `specs/2026-09-22_ajuste_eixos/specs.md`
§5 and §9.1 for why cells are not physically moved).

Key conventions enforced throughout, worth checking before adding a new call site:
- **Join key for anything at bairro level is the numeric bairro code**
  (`codbairro` in the geo/Censo layers, `codigo` in DataSUS/Tabnet exports —
  verified to share the same numbering), never the bairro name string (spelling
  varies across sources). See `.claude/skills/generate_map/SKILL.md` for the
  one documented exception path (name-based join, only when no code exists).
- Output naming: aggregated yearly columns end in `_anual`; rate columns get
  descriptive names (`taxa_mortalidade_precoce`), not generic ones.
- Every chart/map call site passes `fonte_dados` (or the chart equivalent) —
  all visualizations cite their source.
- Choropleth convention (`mapa_coropletico_bairros`): **absolute counts always
  use discrete `bins`, percentages/rates always use a continuous colorbar**
  (`bins=None`) — this is fixed project-wide, not a per-map choice.
- **Population denominators by level** (`specs/2026-09-24_populacao-referencia`): municipal rates divide by the
  Ripsa/MS estimate of the same year (`carrega_populacao_ripsa`/`populacao_ripsa`, versioned extract in
  `dados_locais/populacao/`, network only if a year is missing); sub-municipal rates keep the fixed
  Censo 2022 (0-4) and must say so in the source/legend. Labels use the data's real age range (CadÚnico
  `'0-6'` and SISVAN are 0-5; see `auditoria_faixas.md`), not the catalog's "até 6 anos".
- Never aggregate a percentage column by averaging/summing it across bairros
  — sum the absolute numerator/denominator first (`agrega_bairros_por_nivel`),
  then recompute the rate.
- A shared categorical/sequential color palette and serif title typography
  (Palatino Linotype) are reused by all 4 chart functions and by
  `mapa_coropletico_bairros` (`_CORES_TEMA_MAPA` — a sequential cmap per
  subject: `BuGn` natalidade, `RdPu` mortalidade, `YlOrBr` CadÚnico, `Blues`
  censo/população).
- `'ap'` (Área de Planejamento, IPP, 5 regions) and `'cap'` (Coordenadoria de
  Área Programática de Saúde, SMS-Rio, 10 regions) are **different**
  administrative boundaries with similarly-formatted codes — don't conflate
  them; they use different geojson files and columns.
  `'ra'` (Região Administrativa, 33 in the bairro geojson — no RA 32; key `codra`, via `dissolve` like AP/RP,
  no extra geojson) is a third, distinct boundary; join RA data by the numeric `codra`, never by name.

### Directory layout

- `dados_locais/` — raw input data by source (`censo/`, `cadunico/`,
  `mortalidade/`, `sisvan/`, `IBGE SIDRA/`, ...) and `dados_locais/geo/`
  (reference boundary geojsons). **`dados_locais/` is NOT gitignored** —
  files placed there, including geo layers, get committed; verify with `git
  status` before assuming otherwise. `dados_locais/tratados/` holds
  intermediate cleaned outputs.
- `tabelas_finais/` — standardized CSV/Excel output tables from the pipeline (gitignored except `.gitkeep`).
- `visualizacoes/` — exported chart PNGs from `analise.py`, named by section/theme (gitignored except `.gitkeep`).
- `mapas/` — choropleth PNGs from `mapa_coropletico_bairros`, plus each map's twin input table in `tabelas_finais/tabela_mapa_*.csv` (gitignored except `.gitkeep`). `mapas/tabelas_bairros/` is a legacy Excel-based leftover, kept only for two files not yet migrated.
- `website/` — the published static site (GitHub Pages; `specs/2026-09-24_website_refactor`): tabs per eixo, sticky outline, interactive SVG charts/maps. `website/build/build_site.py` (moved from the PDF skill's `build_html_report.py`) generates `index.html`, `data/charts.js`, `data/geo.js` (map geometry, one `<path>` per region, shared by all maps via `<use>`) and `assets/images/basemap-*`/`ipp-logo-*`; `css/` and `js/` are **hand-edited static files**, not generator strings. Generated output is committed (CI has no `tabelas_finais/`, so it only copies). **Distinct pipeline and visual identity from `relatorio/analise_primeira_infancia.pdf`** — don't mix their conventions. Static-site rules (relative lowercase paths, hash-only routes, no `fetch`, only html/css/js/svg/png/jpg published) and the size budget (the generator warns above 1 MB `index.html` / 2 MB site) are in `website/README.md`. `*.png`/`*.svg` are gitignored globally; `!/website/assets/**` keeps the site's assets tracked.
- `relatorio/` — the published PDF (`analise_primeira_infancia.pdf`, copied there only by `gera_latex.py --publicar`), `latex/` (LaTeX source: hand-edited `relatorio.tex`/`estilo.sty`/`pretextual/`/`fontes.bib`, generated `gerado/`, gitignored `_build/`), the sources inventory (`inventario_fontes.md/.csv`, for the team), the DOCX curation export, and `textos_curados.json` (curated text read by the site and the PDF). `relatorio/index.html` no longer exists (replaced by `website/`).
- `ROADMAP.md` (root) — the single roadmap (in progress → prioritized queue → backlog by theme → done); `specs/roadmap.md` and `website/ROADMAP.md` were merged into it on 2026-09-25. Update it when a round opens or closes.
- `specs/exclusoes.md` — hand-edited list of what the team excluded from the PDF/site/figures, why, and how to restore it. Check it before re-adding an indicator.
- `.github/workflows/deploy-relatorio.yml` — manual (`workflow_dispatch`) GitHub Pages deploy of `website/` (explicit include list, excludes `build/`; fails if a non-static file type slips in). Not the PDF.
- `specs/` — the project's spec-driven workflow. `specs/constitution.md` (non-negotiable
  project-wide rules), `specs/tech-stack.md` (what's used and why, including rejected
  alternatives), and one directory per
  feature/planning round (`specs/2026-09-08_mortalidade-ap`, `specs/2026-09-09_maps-and-ibge`, `specs/2026-09-09_visual-identity`,
  `specs/2026-09-14_relatorio-interativo`, ...), each with `plan.md`, `specification.md`/`specs.md`,
  `tasks.md`, `validation.md`. **Read `specs/constitution.md` first** — check the relevant
  `specs/<round>/` dir and `relatorio/specs.md` (the interactive report's own change history)
  for prior design decisions and *why* before changing related code; several document
  multi-round iteration histories with rejected approaches that shouldn't be re-tried without
  new instruction. Before a risky change or incorporating outside work (e.g. merging another
  branch), open a new `specs/<AAAA-MM-DD>_<name>/` round and summarize the plan before executing.
  Round folders are prefixed with the date the round was opened (first commit of its files), so
  `ls specs/` lists them in chronological order; git branches keep the bare name (`spec/<name>`).
- `.claude/skills/` — see Commands above.

### Working with `dados_locais/geo/`

Reference boundary layers for choropleths, all committed to git despite
living under `dados_locais/`:
- `limite_bairros_rio.geojson` — 166 bairros (Data.Rio/IPP), `codbairro` key, carries `area_plane` (AP) and `cod_rp` (RP, keep as string) natively.
- `limite_ap_saude_rio.geojson` — 10 CAP health-district polygons (SMS-Rio), `cod_ap_sms` key.
- `limite_uf_brasil.geojson` — all 27 Brazilian states (IBGE), for context overlay.
- `limite_municipios_rj.geojson` — 92 RJ-state municipalities (IBGE), for neighbor labeling.

See `.claude/skills/generate_map/SKILL.md` for the full iteration history and
reasoning behind the current choropleth styling (basemap provider choice,
legend/colorbar placement, footnote conventions) before changing any of it —
several past "obvious" fixes were tried and reverted for documented reasons.
