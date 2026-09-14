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
- **Reduzir o peso de `relatorio/index.html` (~17MB)** — todos os ~32 mapas
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
- **Bloco "Principais achados" por seção** — layout implementado (v6.3, caixa cinza
  clara + 5 bullets no início de cada `h2`), mas o texto ainda é placeholder (lorem
  ipsum); precisa de texto curado por alguém que analise os dados, não é algo para
  gerar automaticamente a partir das tabelas (ver `relatorio/specs.md` v6.3)
- **Substituir o lorem ipsum dos blocos de análise por texto real** (por opção do
  seletor, não por card — ver v6.2) — nesta rodada o objetivo era só validar o
  layout/espaço reservado, não o conteúdo. Fora do padrão mapa (onde o texto
  acompanha a altura real do mapa, `height:100%`), a caixa de texto tem altura
  fixa (240px) com rolagem interna; revisitar esse limite quando o texto real
  entrar, pode não ser o tamanho certo para prosa de verdade.
- Botão de "baixar tudo" (fora do escopo — só tem download por gráfico/mapa individual)
- Persistir estado de collapse das seções entre sessões (localStorage), se vier a ser pedido
- **Basemap/contexto geográfico real nos mapas SVG** — tentado e revertido na v6.4/v6.5
  (buscava tiles do Esri Ocean Basemap, mas a margem de contexto ao redor da cidade
  mistura terra e água sem uma camada de hidrografia pra separar os dois, e o usuário
  pediu explicitamente pra nunca representar terra com imagem de mapa/satélite). Se
  vier a ser retomado, precisa de uma camada de água/costa própria (não só o bbox da
  cidade) pra colorir/texturizar somente o mar com segurança — ver
  `relatorio/specs.md` v6.4/v6.5.

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
