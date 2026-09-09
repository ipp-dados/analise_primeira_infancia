# Feature Roadmap

## Mortalidade
- Create time series comparing particular subgroups among regions over time
- Create map visualizations comparing particular subgroups among regions in 2025
- Create map visualizations for all data with granularity up to bairro
- AP/RP-level map versions (not just bairro) for the new bairro indicators added in
  SPEC-maps-and-ibge (nascidos vivos, baixo peso, mortalidade neonatal, óbitos por raça,
  óbitos gravidez/puerpério) — deferred out of that spec's scope, see its §7

## Educação e Violência
- Import the data from CSVs
- Create tables and visualizations

## Matrículas
- Update dados de matrículas escolares for years 2021-2025

## Other (need to break down later)
- Replace HTML visualization with proper Streamlit panel
- Setup LaTeX final report
- Refactor architecture (after SPEC-maps-and-ibge is completed) — analise.py has grown a lot
  across SPEC-mortalidade-AP and SPEC-maps-and-ibge; revisit whether the single-script
  notebook structure still scales, or whether wrangling/visualization/analysis should split
  into separate modules
- Convert the PDF export pipeline to LaTeX (after SPEC-visual-identity is completed) —
  requested once the current `export_pdf_report` skill's Chrome-headless HTML-to-PDF pipeline
  and the new unified visual identity (SPEC-visual-identity) are both in place
