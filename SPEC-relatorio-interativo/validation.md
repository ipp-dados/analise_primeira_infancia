# Validation — SPEC-relatorio-interativo

Critérios objetivos por bloco, escritos antes da implementação — o alvo, não
o resultado (os critérios abaixo não foram editados após a implementação).

## Status real após a implementação (ver `tasks.md` para o detalhe por bloco)

- **V1-V2 (chart-card, outliers)**: passaram. Aplicado a 2 casos reais de
  repetição (não 4 como o spec original estimava — os outros 2 candidatos
  não eram, na prática, paredes de gráficos repetidos; ver `tasks.md` T1.2).
  Outliers aplicados centralmente, confirmados por geração real (73→122
  chart-renders).
- **V3 (mapas SVG)**: **atualizado numa 2ª rodada** (fidelidade estrita ao
  mockup) — passou por completo, não mais reduzido. Todos os ~32 mapas
  (bairro/AP/RP/CAP-saúde, 4 temas) convertidos, geometria conferida contra
  `analise.py` (não estimada), incluindo a descoberta de que "CAP" usa um
  geojson próprio (`limite_ap_saude_rio.geojson`), diferente da AP/RP de
  planejamento urbano. 2 bugs reais encontrados e corrigidos: colisão de
  chave de cache entre o GeoDataFrame bruto e o resultado do nível `'bairro'`
  (quebrava o dissolve de AP/RP), e uma linha de agregado ("Em branco") numa
  tabela do DataSUS sem `codigo` numérico (quebrava a conversão de chave).
  Trade-off não resolvido: `relatorio/index.html` foi de ~5MB para ~20MB
  (geometria não compartilhada entre instâncias) — ver `feature_roadmap.md`.
- **V4 (motor JS)**: passou por inspeção estrutural do DOM e screenshots reais
  (Edge headless). **Não testado**: clique interativo real (pill/outlier
  toggle/collapse/download) — só o estado inicial foi observado. Um bug real
  foi encontrado e corrigido nesta validação (rótulo de extremo duplicado no
  1º ponto de séries curtas, T4.5).
- **V5 (CSS institucional)**: passou, com 2 bugs reais encontrados e
  corrigidos: `--accent-ink` ilegível no tema escuro (trocado por `--accent`,
  T5.3), e **na 2ª rodada** — o `.out` original (todo chart-card) ainda tinha
  sombra/canto arredondado, destoando visivelmente do mockup apesar dos
  componentes novos já estarem corretos; agora nenhum cartão do relatório
  tem sombra ou canto arredondado. Contraste do rodapé (T5.6) não foi medido
  formalmente.
- **V6 (rodapé)**: estrutura/escopo passaram; URLs e e-mail **não
  confirmados** (T6.2) — continuam placeholders.
- **V7 (navbar)**: passou (contagem 1:1 de links/seções/âncoras no DOM).
- **V8 (geração/validação manual)**: geração e ausência de erro de console
  confirmadas via Edge headless real. Responsividade (T8.5) e tema claro
  (T8.6) não testados nesta rodada — só tema escuro (o default do ambiente
  de screenshot).
- **V9 (deploy)**: workflow escrito e com escopo decidido; **não executado**
  — depende de T0.4 (autorização do logo) e de passos manuais fora do
  alcance desta sessão (habilitar Pages, disparar o Action).
- **V10 (documentação)**: passou — `relatorio/specs.md`, `feature_roadmap.md`,
  `tasks.md` atualizados nesta rodada.
- **V11 (replanejamento — texto por opção, tema único, outliers só em taxas,
  agrupamento)**: implementado numa rodada seguinte e passou — ver detalhe
  na seção V11 abaixo. 1 bug real encontrado e corrigido (texto sem limite
  de altura estourando o layout).

## V0 — Gate de autorização
- `specification.md` T0.4 confirmado: alguém do IPP validou o uso do
  brasão/logo oficial da Prefeitura do Rio. **Sem isso, o Bloco 9 (deploy
  público) não roda** — desenvolvimento e preview local não são
  bloqueados por este item, só a publicação no GitHub Pages.

## V1 — Esquema de dado (chart-card)
- Os 4 pontos de repetição (`specification.md` §0.1/§2) — CID-10, CAP
  evitáveis, cobertura vacinal por ano, evitáveis por subgrupo×CAP —
  cada um vira **exatamente 1** chart-card com N `opcoes`, não mais N
  `div.out` separados.
- Contagem de elementos `.out`/`.map-gallery` na página final é menor que
  a contagem atual (874 linhas / repetições documentadas em
  `specification.md` §0.1) — confirmar com uma contagem antes/depois.
- Gráficos que hoje já são opção única continuam idênticos visualmente
  (sem coluna de pills adicionada onde não havia repetição).

## V2 — Outliers
- `remove_outliers_tukey` com < 4 pontos retorna a série inalterada (não
  filtra nada — regra explícita do plan.md §2).
- Uma série sintética com 1 outlier óbvio (ex.: `[10, 12, 11, 9, 500, 13]`)
  tem exatamente esse ponto substituído por `None` na variante
  sem-outliers; os demais pontos idênticos.
- No relatório gerado: toggle de outliers em pelo menos 1 gráfico e 1
  mapa muda visualmente o que é plotado (não é um botão decorativo).
- Mapa: região filtrada como outlier mostra `fill` neutro na variante
  sem-outliers, sem desaparecer do SVG (geometria continua visível).

## V3 — Mapas SVG
- `carrega_geometria_svg('bairro')` retorna 166 entradas (mesma contagem
  do geojson fonte, `specification.md` §3.5); `'ap'` retorna 5; `'rp'`
  retorna 16.
- Pelo menos 1 bairro/AP com geometria de múltiplos anéis (ilha ou
  dissolução não-contígua) renderiza sem `path` quebrado/vazio.
- Nenhum mapa SVG final tem tile de basemap, overlay de UF, ou label de
  município vizinho (confirmado ausente — eram exclusivos do pipeline
  PNG, `specification.md` §3.5 item 6/§7).
- Hover num `<path>` de bairro/CAP mostra tooltip com nome + valor
  formatado pt-BR — testado em pelo menos 2 regiões por mapa amostrado.
- Preenchimento (`fill`) de cada `<path>` corresponde à paleta sequencial
  do tema certo (`_CORES_TEMA_MAPA` — natalidade=Teal/BuGn,
  mortalidade=RdPu/PuRd, cadunico=YlOrBr, censo=Blues), não a cor de um
  outro tema nem um `Oranges` default esquecido.

## V4 — Motor JS (controladores)
- `chartOptionSwitcher`: clicar em cada pill troca o gráfico/mapa exibido
  e marca a pill ativa (estado visual, não só o dado por trás).
- `sectionToggle`: recolher esconde o corpo da seção (`hidden`), expandir
  mostra de novo — testado nas 9 seções, não só na de exemplo do mockup.
- `outlierToggle` + `downloadCsv`: o CSV baixado depois de ativar o
  toggle de outliers reflete a série filtrada, não a bruta (ordem das
  ações importa — testar clicando outlier-toggle **antes** de baixar).
- `lineChart` com rótulo fixo: série onde o valor mais recente também é o
  mais alto mostra **1** rótulo, não 2 sobrepostos (§3.9, caso de
  coincidência).
- Tooltip com rótulo + valor confirmado em pelo menos 1 instância de
  cada: `lineChart`, `barChart`, `groupedBarChart`, mapa SVG — não só nos
  tipos que já tinham tooltip antes desta rodada.

## V5 — CSS institucional
- Nenhuma cor de fundo do corpo do relatório (fora do header/rodapé/chip
  do logo) mudou de valor em relação ao `relatorio/index.html` atual —
  diff de CSS confirma que só as regras novas (§5 do plan.md) foram
  adicionadas, nada existente foi sobrescrito.
- Eyebrow de toda seção **expandida** está em `--accent-ink`/peso 700;
  eyebrow de toda seção **recolhida** está no `.eyebrow` padrão — as duas
  cores nunca aparecem trocadas (expandida cinza, ou recolhida colorida).
- Barra de espectro (11 cores) aparece **exatamente 1 vez** na página
  (só no bloco de título) — busca por ela no restante do HTML retorna 0.
- Tema escuro (`prefers-color-scheme: dark`) testado: navy/cyan/barra de
  espectro/rodapé continuam legíveis (não é uma paleta pensada só para
  tema claro).

## V6 — Rodapé
- URLs de Transparência Rio, LGPD e e-mail de contato são as reais
  (confirmadas no Bloco 6, T6.2) — não os valores ilustrativos copiados
  do mockup/site institucional principal sem checar.
- Data de "atualizado em" bate com o timestamp real do build (gerar 2x
  em dias diferentes e confirmar que muda).
- Rodapé não contém endereço físico, telefone, nem ícones de redes
  sociais (escopo enxuto confirmado, §3.11/§4-M).
- Contraste de texto claro sobre `--ipp-navy` passa em WCAG AA para
  texto normal (4.5:1) — checar especificamente o tom mais dessaturado
  usado nos labels secundários (`#7FA9C6` no mockup).

## V7 — Navbar
- Os 9 links do hambúrguer levam às âncoras certas — clicar em cada um
  rola para o `h2` correspondente, sem link quebrado (`#` vazio ou
  `id` inexistente).
- Bloco "Sumário" antigo não existe mais na página final (substituído
  pela navbar, não duplicado).

## V8 — Geração e validação manual
- `build_html_report.py` roda do início ao fim sem exceção.
- Console do navegador (Chrome headless `--screenshot` ou interativo,
  conforme disponibilidade do ambiente — mesmo método de
  `SPEC-visual-identity/tasks.md` T6.6) sem erros/warnings novos.
- Largura ~375-420px: nenhum overflow horizontal da página inteira
  (scroll horizontal do `<body>`) — comportamento do seletor de
  pills/painel lateral pode não estar polido ainda (`specification.md`
  §8.2 deixa isso para depois), mas não pode quebrar o layout global.

## V9 — Deploy
- Workflow do GitHub Actions roda sem erro no `workflow_dispatch` manual.
- URL pública do GitHub Pages abre e mostra o relatório correto,
  idêntico ao gerado localmente (sem asset faltando — lembrar que o
  arquivo é autocontido, então "faltando" só aconteceria se o workflow
  publicasse o arquivo errado).
- V0 (gate de autorização do logo) confirmado **antes** deste bloco rodar
  — checar de novo aqui, não só em T0.4/T9.1.

## V10 — Documentação
- `relatorio/specs.md` tem uma entrada "v6" descrevendo esta rodada
  (mesmo padrão das entradas v1-v5.1 já existentes).
- `feature_roadmap.md` reflete o estado final: itens resolvidos
  removidos, deferidos mantidos.
- `tasks.md` só tem T10.5 (merge) em aberto ao final.

## V11 — Replanejamento: texto por opção, tema único, outliers só em taxas,
agrupamento — **implementado e validado**
- Todo `option_card`/`viz` (novo ou existente) tem texto em toda opção —
  passou (101-125 `.opt-text` no HTML gerado, a depender de como se conta;
  nenhum `.pill` sem `.opt-text` correspondente, mesmo índice).
- Trocar de pill troca **os 2 painéis juntos** (gráfico/mapa E texto) — a
  estrutura HTML/JS garante isso (`initPills` já alternava 2 elementos por
  índice antes desta rodada só teoricamente; agora os 2 elementos existem de
  fato). **Não testado via clique real** — mesma limitação já registrada em
  V4/T8.3.
- Padrão gráfico: texto ocupa a largura de pills+gráfico juntos, abaixo —
  confirmado visualmente (Censo "População 0-6", "Série temporal").
  Padrão mapa: texto é a 3ª coluna, ao lado do mapa — confirmado (Censo
  "Mapas"). Padrão tabela: texto à esquerda, tabela à direita, sem pills —
  confirmado (Censo "Por bairro").
- **Bug real encontrado e corrigido**: sem limite de altura, 500 palavras de
  lorem ipsum numa coluna estreita (260px, padrões mapa/tabela) ficavam
  MUITO mais altas que o gráfico/tabela ao lado, deixando um vão em branco
  enorme (~15 telas, visto no screenshot real). Corrigido com
  `max-height:240px; overflow-y:auto` em `.opt-text` — aplicado a todo
  padrão, não só ao que expôs o bug.
- Nenhum outlier-card aparece em cima de uma série de contagem absoluta —
  confirmado: 22 outlier-cards no HTML final (era 51 antes do gate), e os
  que restaram são todos de séries/mapas `format`/`fmt` percentual/taxa
  (verificado por amostragem visual, não um grep exaustivo de todos os 22).
- CSS gerado não contém `prefers-color-scheme: dark` nem
  `data-theme="dark"` — confirmado, `grep -c` = 0 para ambos.
- `.doc` renderiza a `max-width:1200px` — confirmado (regra presente no CSS
  gerado e largura visível no screenshot).
- Agrupamento: todas as seções da tabela de `specification.md` §9 (mais
  "Panorama municipal, por subgrupo", não previsto na tabela original, mas
  agrupado pelo mesmo critério ao ser notado durante a implementação) viraram
  `option_card`/`viz` — confirmado por grep (0 chamadas soltas de
  `line_chart`/`bar_chart`/`grouped_bar_chart`/`mapa_svg`/`plain_table` no
  início de linha, ou seja, todas passam por um wrapper).
- Console do navegador (Edge headless, DOM dump + log) sem erro de
  JavaScript da página após todas as mudanças deste bloco.

## V12 — Ajustes finos pós-mockup: header, navbar, mapas, achados

- `_lorem(seed, palavras=200)` — confirmado por leitura do código; texto
  visível no screenshot é visivelmente mais curto que antes.
- Header: screenshot real (1400×1200, Edge headless) mostra título "Análise
  Primeira Infância Carioca" à esquerda e o parágrafo de descrição à
  direita, lado a lado, sem empilhar — confirmado visualmente. Grid
  `1fr 420px` não testado abaixo de 760px nesta rodada (herda o breakpoint
  já existente, não alterado).
- Navbar: screenshot mostra a barra de navegação (☰ NAVEGAÇÃO + logo)
  colada no topo do viewport, sem vão acima — confirmado visualmente
  (era o bug reportado: "começa abaixo do início da página").
- Mapas: screenshot da seção Censo → "Mapas" → "Valores absolutos"/
  "Percentual" mostra pills numa fileira horizontal acima do mapa (não
  mais coluna lateral), mapa visivelmente maior, texto como coluna à
  direita — confirmado visualmente para ambos os grupos divididos.
- Bloco "Principais achados": screenshot mostra a caixa cinza clara logo
  abaixo do título "Censo 2022" (antes de "Por bairro"), rótulo
  "PRINCIPAIS ACHADOS" + exatamente 5 bullets — confirmado visualmente e
  por contagem manual dos `<li>` no screenshot.
- Título de seção preto: screenshot confirma "Censo 2022" em preto
  (`--ink`), com o eyebrow "SEÇÃO 1 DE 9" verde (`--accent`) **acima**, em
  linha separada — não mais na mesma linha de base do título. Causa raiz
  documentada em tasks.md T12.6 (eyebrow inline sem diferenciação
  tipográfica lia como parte do título).
- Grupos de mapas divididos: confirmado por leitura do código gerado —
  Censo (2 `option_card` de 3 entradas cada, rotulados "Valores absolutos"/
  "Percentual" via `h5`), CAP evitável e Mortalidade neonatal idem (não
  capturado em screenshot separado nesta rodada, só Censo foi
  fotografado — os outros 2 seguem a mesma função/CSS, risco de regressão
  visual específica a eles é baixo mas não zero).
- Estilo cartográfico: screenshot mostra título do mapa em serifa (Fraunces,
  negrito), legenda numa caixa com borda e título em destaque, rodapé de 2
  linhas "Sistema de referência: SIRGAS 2000, UTM - Fuso 23S" / "Fonte:
  Censo Demográfico 2022 (IBGE/Data.Rio)" abaixo do mapa, fundo cinza claro
  atrás do SVG — confirmado visualmente, sem basemap real (conforme
  decisão).
- Geração: `relatorio/index.html` = 17.234.906 bytes (17,2MB), 83 gráficos,
  9 `h2`/13 `h3` — sem erro na geração (stdout confirma contagens
  esperadas). Console do Edge headless (DOM dump + log) sem erro de
  JavaScript. **Não testado**: clique real em pill (mapas/gráficos) e
  breakpoints móveis (mesma limitação já registrada em rodadas
  anteriores — sem interação real de browser disponível nesta sessão).

## V13 — Fundo cartográfico real, rosa dos ventos, escala, legenda dentro
## do mapa, alinhamento da navbar

- Navbar: screenshot em 1400px de largura mostra "☰ NAVEGAÇÃO" (canto
  esquerdo do navbar) e "PROJETO · RELATÓRIO INTERATIVO" (eyebrow do
  header, logo abaixo) começando na mesma coordenada x — confirmado
  visualmente (era o bug: antes o navbar usava só padding fixo a partir
  da viewport, sem `max-width`+`margin:auto` como `.doc`, desalinhando em
  telas largas).
- Rosa dos ventos e barra de escala: screenshot do mapa "Crianças de 0 a
  4 anos, por bairro" mostra a seta "N" no canto superior direito e uma
  barra rotulada "10 km" no canto inferior esquerdo do mapa — confirmado
  visualmente, presentes em todo mapa (gerados dentro de `build()`,
  chamado por toda invocação de `mapa_svg`).
- Fundo cartográfico real: **bug real encontrado e corrigido durante a
  validação** — a primeira tentativa (zoom 12) mostrava um tile
  placeholder cinza-azulado com o texto "Map data not yet available"
  cobrindo toda a área terrestre do mapa, só a franja litorânea/oceano
  tinha alguma variação de cor. Diagnosticado com um probe manual dos
  tiles (`curl` direto na URL do tile do Esri Ocean Basemap pras
  coordenadas de zoom 11/12/13 do centro do Rio — todos devolviam o mesmo
  placeholder de 14.226 bytes; zoom 8/9/10 devolviam tiles com conteúdo
  real de terreno/relevo, tamanhos diferentes entre si). Corrigido
  fixando `zoom=10`. Novo screenshot confirma relevo/rodovias reais atrás
  dos polígonos, visualmente equivalente ao fundo do PNG de referência
  (`mapas/mapa_censo_0_4_absoluto.png`, comparado lado a lado).
- Legenda dentro do mapa: screenshot confirma a caixa de legenda
  (fundo branco, borda) sobreposta no canto superior esquerdo do próprio
  mapa, não mais numa coluna separada — o mapa ocupa visivelmente mais
  largura do card agora.
- Geração: 17.296.104 bytes (17,3MB) — aumento de ~20KB sobre a rodada
  anterior (imagem de fundo compartilhada, 1 única cópia reaproveitada
  por todos os 44 mapas via classe CSS, confirmado por grep: só existe 1
  `background-image` no HTML gerado). Console do Edge headless (DOM dump
  + log) sem erro de JavaScript. **Não testado**: mapas do nível CAP
  especificamente (reusam a mesma classe de fundo que bairro/AP/RP por
  coincidência de bbox — não fotografados em separado nesta rodada),
  clique real em pill, breakpoints móveis.

## V14 — Reversão do fundo real, fontes +20%, contorno só no mapa, sombra,
## alinhamento do topo, mapa menor

- Fundo dos mapas: `grep -c "background-image"` no HTML gerado = 0
  (confirmado — a máquina de fetch de tile foi removida por completo, não
  só desativada). Screenshot confirma fundo liso neutro atrás dos
  polígonos, sem imagem de satélite/terreno.
- Cor do choropleth do Censo: screenshot mostra a escala "Crianças 0-4"/
  "% 0-4 anos" em tons de cinza (branco → preto), não mais azul —
  confirmado visualmente pros 2 mapas de bairro (absoluto e percentual).
- Botão de outlier ao lado do CSV: screenshot do mapa "% de crianças de 0
  a 4 anos, por bairro" mostra "× Remover outliers" e "⭳ CSV" na mesma
  linha, um ao lado do outro, ambos no canto superior direito do card —
  confirmado visualmente.
- Fontes maiores: comparação visual direta com o screenshot da rodada
  anterior confirma texto perceptivelmente maior no título, eyebrow,
  parágrafos e rótulos do gráfico — sem quebra de layout observada no
  header/navbar/pills nesta largura (1400px).
- Lorem ipsum mais curto: confirmado por leitura do código
  (`_lorem(seed, palavras=150)`); blocos de texto no screenshot são
  visivelmente mais curtos que a rodada anterior.
- Contorno só no mapa: screenshot confirma gráfico de barras
  ("População 0-6 por idade/raça/sexo") e a tabela ("Por bairro") SEM
  nenhuma borda visível, enquanto o cartão de mapa e seu texto pareado
  mantêm um contorno preto de 2px nítido — confirmado visualmente em
  múltiplos exemplos (gráfico de barras, tabela, 2 grupos de mapas do
  Censo).
- Sombra: screenshot mostra uma sombra sutil no cartão de mapa, no texto
  ao lado do mapa e no bloco "Principais achados" — confirmado
  visualmente (mais perceptível no bloco de achados, por ter fundo cinza
  claro contra o branco da página).
- Mapa e texto encostados: screenshot confirma a borda direita do cartão
  de mapa tocando diretamente a borda esquerda do texto pareado, sem vão
  visível entre os dois (era um bug real na primeira tentativa desta
  rodada — o `max-width:760px` do `.map-svg-frame` deixava um vão de
  ~300px antes do texto em telas largas; corrigido removendo o
  `max-width`, novo screenshot confirma o encaixe).
- Alinhamento do topo do header: screenshot confirma o eyebrow "PROJETO ·
  RELATÓRIO INTERATIVO" e o primeiro parágrafo de descrição começando na
  mesma coordenada y — confirmado visualmente.
- Altura do mapa: screenshot confirma um mapa visivelmente mais baixo/
  compacto que a rodada anterior, sem nenhum polígono cortado nas bordas
  — consistente com o cálculo prévio (margem em branco > corte
  aplicado).
- Geração: 17.153.308 bytes (17,15MB, menor que a rodada anterior — texto
  mais curto + sem imagem de fundo), 5,8s (bem mais rápido — sem busca de
  rede). Console do Edge headless (DOM dump + log) sem erro de
  JavaScript. **Não testado**: clique real em pill, breakpoints móveis,
  mapas do nível CAP especificamente fotografados em separado (mesma
  lógica de fundo neutro que bairro/AP/RP, risco de regressão específica
  baixo mas não zero).

## V15 — Fechamento desta rodada da spec

- Código (Blocos 0-14) implementado e validado visualmente em todas as
  rodadas registradas acima — sem erro de JavaScript em nenhuma
  validação via Edge headless.
- Lacunas conhecidas e não resolvidas nesta rodada, todas já registradas
  em `feature_roadmap.md` (não bloqueiam o merge do código): URLs/e-mail
  reais do rodapé, autorização do logo oficial, `mobile_version`
  (breakpoints existem no CSS mas nunca foram vistos numa viewport
  estreita real), habilitar GitHub Pages, texto real substituindo o lorem
  ipsum, peso do arquivo (~17MB de geometria SVG sem compartilhamento).
- Merge em `staging_main`: **gated**, só após aval explícito do usuário
  (mesma regra desde o Bloco 10/T10.5).

## V16 — Fundo real de volta, texto do mapa de verdade limitado à altura

- Fundo real: screenshot confirma relevo/rodovias/água visível atrás dos
  polígonos cinza do Censo (bairro absoluto e uma variante mais abaixo na
  mesma página) — igual ao visual antes da reversão do Bloco 14, agora
  com o esclarecimento correto de que só o CHOROPLETH dos dados (não o
  basemap) tinha o problema de azul-sobre-terra.
- Choropleth ainda em cinza: confirmado nos mesmos 2 screenshots — nenhum
  dado (polígono colorido por valor) aparece em azul; azul só aparece no
  mar/água do basemap real, exatamente a regra pedida ("não usar azul nos
  dados representados no shapefile").
- **Bug real encontrado e corrigido nesta rodada**: `min-height:0` (a
  tentativa anterior de limitar a altura do texto à do mapa) não
  funcionava — confirmado isolando o problema em 2 arquivos HTML mínimos
  fora do gerador (um em CSS Grid, outro em Flexbox, ambos com
  `align-items:stretch`), reproduzindo o mesmo bug nos dois: sem uma
  altura de container definida de fora, o eixo cruzado cresce pro maior
  conteúdo entre os lados, e `min-height:0` não muda isso. A técnica que
  funcionou (confirmada num 3º arquivo de teste antes de aplicar no
  gerador): tirar o texto do cálculo de altura intrínseca do pai via um
  filho `position:absolute`. Screenshot do gerador real após aplicar
  confirma a borda inferior do texto (com scrollbar visível, conteúdo
  cortado) terminando exatamente na mesma linha que a borda inferior do
  mapa — em 2 exemplos diferentes na mesma página.
- Geração: 17.189.574 bytes (17,19MB). Console do Edge headless (DOM dump
  + log) sem erro de JavaScript. **Não testado**: clique real em pill,
  breakpoints móveis, os ~42 mapas restantes fotografados individualmente
  (mesma classe de fundo e mesma técnica CSS que os 2 testados, risco de
  regressão específica baixo mas não zero).

## V17 — Sem contorno no texto do mapa, cor do Censo trocada de cinza pra
## roxo

- Sem contorno no texto do mapa: screenshot confirma a caixa de texto ao
  lado do mapa "Crianças de 0 a 4 anos, por bairro" sem nenhuma borda
  visível — só resta a sombra sutil (`box-shadow`), que continua lá.
- Cor do Censo: screenshot mostra a escala "CRIANÇAS 0-4" e os polígonos
  do mapa em tons de roxo (branco → violeta escuro), não mais cinza —
  confirmado visualmente. Mar/água do fundo cartográfico continua azul
  (a única cor azul na página), sem mudança.
- Mapa e texto continuam encostados e com altura igual (Bloco 16
  preservado — confirmado no mesmo screenshot, scrollbar interna do texto
  terminando na mesma linha da borda inferior do mapa).
- Geração: 17.189.538 bytes (17,19MB, essencialmente igual à rodada
  anterior). Console do Edge headless (DOM dump + log) sem erro de
  JavaScript. **Não testado**: clique real em pill, breakpoints móveis.
