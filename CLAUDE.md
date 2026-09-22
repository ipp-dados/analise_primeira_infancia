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

There is no test suite, linter, or build step — `analise.py` is the
deliverable, run cell-by-cell in Jupyter (via Jupytext) or top-to-bottom as a
script. **`analise.py` (the `.py:percent` file) is the source of truth that
gets committed; `analise.ipynb` is a generated artifact** — never hand-edit
the notebook's outputs and expect them to matter, and `*.ipynb` is
gitignored.

Two project skills wrap multi-step regeneration pipelines — prefer them over
reimplementing this logic:
- `generate_map` — produces a choropleth PNG via `mapa_coropletico_bairros` (defined in `analise.py`).
- `export_pdf_report` — regenerates `relatorio/analise_primeira_infancia.pdf` from `analise.py`'s own matplotlib PNGs (`visualizacoes/`) and `tabelas_finais/` tables. Distinct from and NOT related to `relatorio/index.html`'s SVG report — see below.

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
   Cobertura Vacinal EPI, IBGE SIDRA/PNAD/Censo Escolar.
3. A closing "Análise / Relatório" section (markdown notes only, no code
   output) — deliberately omitted from both the HTML and PDF reports.

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
- `relatorio/` — `index.html`, a self-contained interactive HTML report (SVG charts + choropleths, light/dark theme), generated by `.claude/skills/export_pdf_report/scripts/build_html_report.py`. **Distinct pipeline from `analise_primeira_infancia.pdf`** (same skill folder, different script, different visual identity — see the `export_pdf_report` skill's note before touching either). `index.html` is gitignored; the PDF is not.
- `.github/workflows/deploy-relatorio.yml` — manual (`workflow_dispatch`) GitHub Pages deploy of `relatorio/index.html` only (not the PDF).
- `specs/` — the project's spec-driven workflow. `specs/constitution.md` (non-negotiable
  project-wide rules), `specs/tech-stack.md` (what's used and why, including rejected
  alternatives), `specs/roadmap.md` (prioritized/backlog work items), and one directory per
  feature/planning round (`specs/mortalidade-ap`, `specs/maps-and-ibge`, `specs/visual-identity`,
  `specs/relatorio-interativo`, ...), each with `plan.md`, `specification.md`/`specs.md`,
  `tasks.md`, `validation.md`. **Read `specs/constitution.md` first** — check the relevant
  `specs/<round>/` dir and `relatorio/specs.md` (the interactive report's own change history)
  for prior design decisions and *why* before changing related code; several document
  multi-round iteration histories with rejected approaches that shouldn't be re-tried without
  new instruction. Before a risky change or incorporating outside work (e.g. merging another
  branch), open a new `specs/<name>/` round and summarize the plan before executing.
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
