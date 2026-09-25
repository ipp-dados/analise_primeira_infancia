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
4. **`publicar_teste_pages`** — ✅ concluído: GitHub Pages publicado
   (`workflow_dispatch` de `.github/workflows/deploy-relatorio.yml` já
   disparado; `relatorio/index.html` no ar com a faixa "EM DESENVOLVIMENTO /
   TEMPORÁRIO"). Novas publicações seguem manuais e só após validação
   (ver `specs/inclusao_dados_protecao` §8).
5. **Importar dados de violência** — ✅ concluído:
   `specs/inclusao_dados_protecao` (branch `inclusao_dados_protecao`;
   `dados_locais/protecao/`). Eixo "Proteção" implementado em `analise.py`,
   HTML, PDF e DOCX; nível geográfico `ra` incorporado. Deploy no GitHub
   Pages segue manual, só após validação.
6. **População por bairro, ano a ano (referência fixa)** — spec **seguinte**
   a `inclusao_dados_protecao`. Extrair a população por bairro (idealmente por
   idade simples, 0 a 6 anos) para cada ano, em vez do único ponto do Censo
   2022 (faixa 0-4) usado hoje como denominador. Motivo: as taxas de
   `inclusao_dados_protecao` (D9) misturam numerador 0-5 anos de 2025 com
   denominador 0-4 anos de 2022; uma série anual fixa permite taxas
   consistentes em qualquer ano e recalcular as já existentes. Inclui
   **corrigir os demais problemas** de denominador/cobertura que aparecerem
   (a levantar ao abrir a spec, começando pela lista de ressalvas D9 e pelas
   taxas por bairro que hoje usam o Censo 2022 como referência).
   **Inclui (vindo de `specs/recortes_cadunico`, D7 e D8):**
   - **Auditoria de faixas etárias entre fontes**, junto com o item 7: o que
     cada dado representa de fato. O CadÚnico `'0-6'` são nascidos a partir de
     2020-08-12 (0 a 5 anos completos, idade em ~2026-08-12), e as crianças de
     6 anos caem no grupo `'7-14'`. O Censo usa 0-4, o Sinan 0-5, e assim por
     diante. Só depois padronizar os rótulos "0-6"/"0 a 5"/"até 6 anos" em
     títulos, legendas e textos, e decidir numeradores e denominadores
     compatíveis.
   - **Revisão de nomes** de tabelas (`tabelas_finais/`), visualizações
     (`visualizacoes/`) e mapas (`mapas/`): nome ≠ conteúdo (caso real:
     `cadunico_por_faixa_etaria_2026.csv` continha o recorte por renda,
     renomeado em `recortes_cadunico`), faixa etária no nome ≠ faixa do dado,
     órfãos e leitores nos scripts de relatório.
7. (FIX). **Corrigir `nascidos_vivos_bairro_mae`: faltam mapas e visualizações de percentual.**
  A série por bairro/mãe não gera mapas coropléticos nem gráficos em % (só contagens, se tanto).
  Diagnosticar primeiro (não sei a causa: não abri esse trecho de `analise.py`). Depois seguir
   **Em andamento (2026-09-24):** os itens 6 e 7 foram absorvidos por `specs/populacao-referencia`
   (branch `spec/populacao-referencia`). Diagnóstico do 7: o indicador "percentual de nascidos vivos
   por bairro da mãe" nunca foi implementado e o HTML/PDF pulam itens sem arquivo (spec, Parte D). Nessa
   rodada, o nível município passa a usar a Ripsa/MS e o sub-municipal fica no Censo 2022 (decisão B1 (a)).
   **✅ Concluídos (2026-09-24, `specs/populacao-referencia`):** população Ripsa 2000-2025 como referência
   municipal; rótulos "Censo 2022" explícitos no sub-municipal; auditoria de faixas
   (`specs/populacao-referencia/auditoria_faixas.md`), rótulos com a faixa real e 21 renomeações; item 7
   resolvido como coluna `percentual_do_municipio` na gêmea de contagem; achado e corrigido o total dobrado
   da série dos Censos 2000/2010/2022 (participação de 0-4 anos: 7,6% / 5,8% / 5,0%).
7a. **Ajustar a estimativa de crianças pequenas por bairro com a Ripsa** (pedido do usuário, 2026-09-24;
   é a continuação da decisão B1 de `specs/populacao-referencia`). A Ripsa não tem bairro, então o nível
   sub-municipal ficou no Censo 2022 fixo, que subconta crianças pequenas (0-4: 310.648 no Censo contra
   361.163 na Ripsa em 2022, +16%) e não varia por ano. Construir uma estimativa derivada, rotulada
   como tal:
   - **(b)** participação de cada bairro no Censo 2022 × total municipal Ripsa de cada ano, com 0-4
     estendido para 0-5 pela razão municipal Ripsa; os bairros somam o total Ripsa;
   - **(c)** como (b), mas com a participação variando no tempo entre os Censos 2010 e 2022 (exige a
     correspondência 160 → 166 bairros).
   Depois recalcular as taxas sub-municipais (violência por bairro/RA/CAP e o % CadÚnico, que depende
   também do item 8a) e documentar a mudança de denominador. Pré-requisito: a Parte A de
   `specs/populacao-referencia` concluída.
8. **Extrair novos recortes do CadÚnico** — ✅ 1ª leva concluída:
   `specs/recortes_cadunico` (branch `spec/recortes_cadunico`): sexo, raça/cor,
   renda × arranjo familiar (eixo Inclusão), supressão < 20 e correções nas
   saídas CadÚnico existentes. Pendências dessa rodada viraram os itens 8a-8c
   abaixo. Texto original do item: levantar e extrair recortes
   adicionais além dos já usados em `analise.py` (`tabelas_finais/cadunico_*`:
   por bairro, faixa etária, idade, faixa de renda), a definir ao abrir a
   spec (candidatos: indicadores do catálogo com fonte CadÚnico ainda
   pendentes em `specs/estrutura_eixos.md`, ex. Moradia). Requer `.env`
   com acesso ao banco (`connect_db_ctpe`).
   - **8a. Geocodificação CadÚnico por bairro oficial** (F1 de `recortes_cadunico`):
     o bairro vem do CEP dos Correios (`lista_bairros.csv`), que deixa 8,1% das
     crianças sem bairro e desloca bairros-favela para os vizinhos (Maré →
     Bonsucesso, Rocinha → Gávea; Vila Kennedy/Jabour/Gericinó/Ilha de Guaratiba/
     Lapa ausentes). Refazer por join espacial ou código de bairro do CTPE; só
     então o mapa "% CadÚnico/Censo" pode voltar ao relatório.
   - **8b. Pedido ao CTPE** (F2): extração com parentesco/responsável familiar
     (arranjo real), deficiência (3 itens de Inclusão) e características do
     domicílio (2 itens de Moradia).
   - **8c. Filtro de cadastro da silver** (F3): confirmar com o CTPE se
     `silver_cadunico_geral` já exclui cadastros inativos/desatualizados.
9. **Outros dados faltantes** — levantar e importar bases pendentes além de
   violência (a detalhar; nenhuma listada formalmente ainda além dos itens
   de Matrículas/Mortalidade abaixo).
10. **Atualizar a documentação do projeto** — revisar e alinhar `CLAUDE.md`,
   `README.md`, `CHANGELOG.md`, `specs/tech-stack.md`, `specs/constitution.md`,
   `relatorio/specs.md` e os `SKILL.md` (`generate_map`, `export_pdf_report`)
   ao estado real após `inclusao_dados_protecao` (nível geográfico `ra`,
   `dados_locais/protecao/`, novas funções `carrega_sinan_*`, eixo Proteção
   implementado) e às specs seguintes.

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
- ✅ Update dados de matrículas escolares for years 2021-2025 — feito em `specs/populacao-referencia/matriculas`
  (2026-09-24): série 2007-2025 refeita dos microdados do INEP, 0 a 5 anos, com taxa bruta de atendimento
  (população Ripsa) e metas do PNE.
- Backlog: mapa de matrículas por bairro, com as escolas geocodificadas (o arquivo do INEP não traz
  `codbairro`; ver `specs/populacao-referencia/matriculas/specification.md` §4.4).
- Backlog: validar 1 ou 2 anos contra a Sinopse Estatística do INEP (pendência P5 da mesma spec).

## Relatório interativo (`specs/relatorio-interativo`)
- **`improve charts`** (pedido do usuário, 2026-09-25) — levar para o site (`website/build/build_site.py`,
  `website/js/charts.js`) as melhorias de leitura desenhadas para o PDF em `specs/relatorio_latex` §5.1
  (protótipo em `specs/relatorio_latex/prototipo/`). Fazer **depois do Bloco 5** daquela rodada, para que
  rótulos e paleta venham de uma fonte só:
  - **Rótulos de eixo por extenso, com unidade** — reaproveitar o dicionário `ROTULOS_EIXO` do Bloco 5 em vez
    de nomes de coluna;
  - **Teto de cor no percentil 95 em todos os mapas de taxa/percentual por bairro** — hoje só os mapas de
    violência usam `teto`; alinha o site à decisão D5 do PDF (tooltip continua mostrando o valor real);
  - **Rótulos diretos seletivos** — último valor na ponta de cada linha, valor na ponta das barras; o tooltip
    não existe no celular e não se lê de relance;
  - **Pequenos múltiplos** como opção (pill) nos gráficos de 8-11 séries (CAP × ano, imunobiológicos,
    subgrupos CID) — um painel por série, as demais em cinza ao fundo;
  - **Paleta de dados** — a atual herda do notebook tons que falham em fundo branco (amarelo `#deb254` sem
    contraste 3:1; laranja × verde confundíveis para protanopia; azul `#6a95c8` de croma baixo). A paleta
    validada do PDF (`#3f76b8 #dc7a45 #0f7d5c #b88a1e #b8527b #5c9a3c #6f64ae #b84f4e`) mantém a mesma ordem
    de matizes; rodar o validador da skill `dataviz` contra as superfícies do site antes de trocar;
  - **Fontes com referência completa** — as caixas "Fontes desta seção" passam a mostrar a referência ABNT
    de `relatorio/latex/fontes.bib`, igual à lista "Fontes" do PDF;
  - Conferir se o site repete algum dos problemas achados no protótipo (ex. linha `Total` desenhada como
    categoria em `cadunico_por_faixa_renda_2026.csv`).
- ✅ **Concluído em `specs/website_refactor` (2026-09-24)**: geometria compartilhada via `<use>` + simplificação, site todo 1,5 MB. Registro original:
  **Reduzir o peso de `relatorio/index.html` (~17MB)** — todos os ~32 mapas
  agora são SVG interativo (concluído), mas cada instância embute sua própria
  geometria como texto sem compartilhar paths entre mapas do mesmo nível
  (ex.: os ~20 mapas de bairro repetem os mesmos 166 polígonos). Otimização:
  compartilhar via `<defs>`/`<use>` ou um mapa `codigo→d` referenciado por id
  em vez de inline em cada `<path>` — ver `relatorio/specs.md` v6.1.
- **Confirmar URLs/e-mail reais do rodapé** (Transparência Rio, LGPD, contato) —
  hoje são placeholders copiados do site institucional principal — ver `specs/relatorio-interativo/tasks.md` T6.2
- **Página "Fale Conosco" no site** (pedido do usuário, 2026-09-24) — página/aba própria acessível pela
  barra de navegação; opções (mailto estático × serviço de formulário, LGPD) em `website/ROADMAP.md`.
- **Logo em SVG oficial** — pedir à Ascom do IPP; hoje o PNG oficial é servido em `srcset` (`specs/website_refactor` D6).
- **Confirmar autorização de uso do logo oficial** da Prefeitura do Rio/IPP antes do
  deploy público — ver `specs/relatorio-interativo/tasks.md` T0.4 (bloqueia só o deploy, não o código)
- **Habilitar GitHub Pages** nas configurações do repositório e disparar o primeiro
  deploy — passo manual fora do alcance de uma sessão de código (`specs/relatorio-interativo/tasks.md` T9.4/T9.5)
- Medir formalmente o contraste do rodapé (WCAG AA) — inspeção visual feita, não
  uma medição real (`specs/relatorio-interativo/tasks.md` T5.6)
- **`mobile_version`** — *(2026-09-24: o site mudou para `website/` com abas e sumário lateral; a lista atualizada, por componente, está em `website/ROADMAP.md`. O texto abaixo descreve o layout antigo.)* Versão mobile do relatório ainda não validada de verdade.
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
