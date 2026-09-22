# Roadmap

Estado em 2026-09-22. Itens em ordem de prioridade dentro de cada seção;
"Prioridades atuais" é a fila de trabalho imediata, o resto é backlog por
tema (conteúdo herdado de `feature_roadmap.md`, agora fundido aqui).

## Prioridades atuais

1. **Merge das mudanças da Waleska** — ✅ concluído e validado de ponta a
   ponta (`specs/merge-waleska-changes`). Falta só dar merge deste branch
   (`planning`) em `staging_main`, quando o usuário decidir.
2. **Reorganização de dados/nomes** — ✅ concluído: `dados_locais/` por
   tema, convenção de `tabelas_finais/`/`visualizacoes/`/`mapas/`
   documentada em `specs/tech-stack.md`, bug do mapa de nascidos
   vivos/baixo peso preso em dado legado corrigido, 39 arquivos órfãos
   removidos, `relatorio/`, `tabelas_finais/`, `mapas/`, `visualizacoes/`
   regenerados de verdade (exceto CadÚnico, sem `.env` nesta sessão) — ver
   `specs/reorganize-naming/plan.md`.
3. **Reorganizar a estrutura do relatório** — ✅ concluído:
   `relatorio/index.html`, o PDF e um novo DOCX de curadoria de textos
   reorganizados por eixo da política municipal de primeira infância (em
   vez de por fonte de dado), a partir de um crosswalk único e editável à
   mão (`specs/estrutura_eixos.md`) — ver `specs/ajuste_eixos/`. Pendências
   remanescentes já registradas lá, não aqui: reordenação física de
   `analise.py` foi deliberadamente descartada (§9.1); HTML/PDF não leem o
   `.md` em tempo de execução, só o DOCX (`specs.md` §9.3) — mudança de
   agrupamento que afete HTML/PDF exige ajuste manual de código.
4. **`publicar_teste_pages`** — em andamento: repositório está indo a
   público e `relatorio/index.html` ganhou uma faixa fixa "EM
   DESENVOLVIMENTO / TEMPORÁRIO" para permitir publicar antes do item 3
   estar pronto. Falta disparar o `workflow_dispatch` de
   `.github/workflows/deploy-relatorio.yml`.
5. **Importar dados de violência** — ver "Educação e Violência" abaixo;
   `dados_locais/painel_primeira_infancia_cesta_indicadores.xlsx` (eixo
   "Proteção") tem o catálogo de indicadores/fontes a importar.
6. **Outros dados faltantes** — levantar e importar bases pendentes além de
   violência (a detalhar; nenhuma listada formalmente ainda além dos itens
   de Matrículas/Mortalidade abaixo).

## Mortalidade
- Create time series comparing particular subgroups among regions over time
- Create map visualizations comparing particular subgroups among regions in 2025
- Create map visualizations for all data with granularity up to bairro
- AP/RP-level map versions (not just bairro) for the new bairro indicators added in
  `specs/maps-and-ibge` (nascidos vivos, baixo peso, mortalidade neonatal, óbitos por raça,
  óbitos gravidez/puerpério) — deferred out of that spec's scope, see its §7

## Educação e Violência
- Import the data from CSVs
- Create tables and visualizations

## Matrículas
- Update dados de matrículas escolares for years 2021-2025

## Relatório interativo (`specs/relatorio-interativo`)
- **Reduzir o peso de `relatorio/index.html` (~17MB)** — todos os ~32 mapas
  agora são SVG interativo (concluído), mas cada instância embute sua própria
  geometria como texto sem compartilhar paths entre mapas do mesmo nível
  (ex.: os ~20 mapas de bairro repetem os mesmos 166 polígonos). Otimização:
  compartilhar via `<defs>`/`<use>` ou um mapa `codigo→d` referenciado por id
  em vez de inline em cada `<path>` — ver `relatorio/specs.md` v6.1.
- **Confirmar URLs/e-mail reais do rodapé** (Transparência Rio, LGPD, contato) —
  hoje são placeholders copiados do site institucional principal — ver `specs/relatorio-interativo/tasks.md` T6.2
- **Confirmar autorização de uso do logo oficial** da Prefeitura do Rio/IPP antes do
  deploy público — ver `specs/relatorio-interativo/tasks.md` T0.4 (bloqueia só o deploy, não o código)
- **Habilitar GitHub Pages** nas configurações do repositório e disparar o primeiro
  deploy — passo manual fora do alcance de uma sessão de código (`specs/relatorio-interativo/tasks.md` T9.4/T9.5)
- Medir formalmente o contraste do rodapé (WCAG AA) — inspeção visual feita, não
  uma medição real (`specs/relatorio-interativo/tasks.md` T5.6)
- **`mobile_version`** — versão mobile do relatório ainda não validada de verdade.
  O CSS já tem breakpoints (`max-width:720px` e `max-width:520px`) que empilham
  os 3 padrões de layout (gráfico/mapa/tabela) numa coluna só e viram a coluna de
  pills numa fileira horizontal, mas isso nunca foi checado numa viewport estreita
  real (~375-420px) nem via Edge headless — toda validação desta spec até agora
  foi feita a 1400px. Precisa de uma rodada dedicada: screenshot real em
  375/390/420px de largura pra cada um dos 3 padrões de layout + navbar (o burger
  menu nunca foi aberto/testado) + mapa (legenda overlay pode não caber numa tela
  estreita) + tabelas largas (scroll horizontal).
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
- **Camada própria de água/costa pros mapas** — o fundo cartográfico real (Esri Ocean
  Basemap, restaurado na v6.6 após um mal-entendido na v6.5 que o removeu por
  completo) hoje é só o tile do provedor; não há uma camada de hidrografia própria do
  projeto pra separar terra e água com certeza dentro do bbox de contexto ao redor da
  cidade. Não bloqueia nada hoje (o choropleth dos dados nunca usa azul, só o
  basemap), mas seria necessário se algum dia quiser colorir/texturizar
  especificamente o mar por conta própria (sem depender do tile) — ver
  `relatorio/specs.md` v6.4/v6.5/v6.6.

## Other (need to break down later)
- Replace HTML visualization with proper Streamlit panel
- Setup LaTeX final report
- Refactor architecture (after `specs/maps-and-ibge` is completed) — analise.py has grown a lot
  across `specs/mortalidade-ap` and `specs/maps-and-ibge`; revisit whether the single-script
  notebook structure still scales, or whether wrangling/visualization/analysis should split
  into separate modules
- Convert the PDF export pipeline to LaTeX (after `specs/visual-identity` is completed) —
  requested once the current `export_pdf_report` skill's Chrome-headless HTML-to-PDF pipeline
  and the new unified visual identity (`specs/visual-identity`) are both in place
