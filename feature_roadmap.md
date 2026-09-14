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

## Relatório interativo (SPEC-relatorio-interativo)
- **Reduzir o peso de `relatorio/index.html` (~20MB)** — todos os ~32 mapas
  agora são SVG interativo (concluído), mas cada instância embute sua própria
  geometria como texto sem compartilhar paths entre mapas do mesmo nível
  (ex.: os ~20 mapas de bairro repetem os mesmos 166 polígonos). Otimização:
  compartilhar via `<defs>`/`<use>` ou um mapa `codigo→d` referenciado por id
  em vez de inline em cada `<path>` — ver `relatorio/specs.md` v6.1.
- **Confirmar URLs/e-mail reais do rodapé** (Transparência Rio, LGPD, contato) —
  hoje são placeholders copiados do site institucional principal — ver tasks.md T6.2
- **Confirmar autorização de uso do logo oficial** da Prefeitura do Rio/IPP antes do
  deploy público — ver tasks.md T0.4 (bloqueia só o deploy, não o código)
- **Habilitar GitHub Pages** nas configurações do repositório e disparar o primeiro
  deploy — passo manual fora do alcance de uma sessão de código (tasks.md T9.4/T9.5)
- Medir formalmente o contraste do rodapé (WCAG AA) — inspeção visual feita, não
  uma medição real (tasks.md T5.6)
- Testar responsividade em telas estreitas (~375-420px) — não testado nesta rodada
- **Bloco "Principais achados" por seção** (callout editorial do mockup) — nunca
  implementado; precisa de texto curado por alguém que analise os dados, não é
  algo para gerar automaticamente a partir das tabelas (ver `relatorio/specs.md` v6.1)
- Botão de "baixar tudo" (fora do escopo — só tem download por gráfico/mapa individual)
- Persistir estado de collapse das seções entre sessões (localStorage), se vier a ser pedido
- Basemap/contexto geográfico (satélite/desenho, UF, municípios vizinhos) nos mapas SVG
  interativos, se vier a ser pedido — não portado do pipeline PNG (`generate_map`), ver
  SPEC-relatorio-interativo/specification.md §7

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
