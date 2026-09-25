# Especificação — Relatório Interativo (`relatorio/index.html` v6)

## 0. Contexto

`relatorio/index.html` (ver histórico em `relatorio/specs.md`, v1–v5.1) é hoje
uma página única, longa, sem interatividade além de tooltip ao passar o mouse
em cada gráfico SVG. O usuário anexou um wireframe manuscrito
(`relatorio/Page 1.pdf`) como referência para uma reformulação visual e de
interação. Este spec cobre **só o planejamento** desta rodada — especificação
+ layout revisado. Implementação fica para uma rodada seguinte, após revisão.

### 0.1 Estado atual (levantado nesta rodada)

- 874 linhas, ~3.7MB (dados embutidos como JSON/base64 inline, sem chamada de
  rede em runtime).
- 9 seções `h2` (🏘️ Censo 2022, 🗂️ CadÚnico, 🏥 DataSUS/Tabnet, ⛓️ Óbitos por
  causas evitáveis, 🤰 Gravidez e puerpério, 🩺 Mortalidade neonatal, 🥗
  SISVAN, 💉 Cobertura vacinal (EPI), 🎓 Educação), cada uma com `h3`
  variáveis.
- **Repetição estrutural identificada**: várias subseções emitem uma parede
  de gráficos quase idênticos, um por corte de dado — ex. "Por grupo/subgrupo
  de causa (CID-10)" tem ~18 `div.out` em sequência; as galerias de mapas por
  CAP (`div.map-gallery`) têm 6–8 `div.map-card` lado a lado. É exatamente o
  padrão que o wireframe resolve com o seletor "Option 1/2/3/4".
- Já existe: tooltip via hover nos gráficos SVG, tabela de dados alternativa
  ("ver tabela"), tema claro/escuro automático, sumário no topo com âncoras
  para `h2`/`h3`.
- Não existe hoje: nenhum `<button>`, `<select>` ou `data-*` de estado —
  zero interatividade além do hover. Mapas são PNG/WebP rasterizados
  (`mapas/*.png`, embutidos como `data:` URI), sem geometria vetorial — não
  há hover por bairro/CAP possível sem mudar o pipeline de geração do mapa.
- Motor de gráfico JS próprio: `lineChart`, `barChart`, `groupedBarChart`
  (sem dependência externa) — ver `relatorio/specs.md`.
- Gerador: `.claude/skills/export_pdf_report/scripts/build_html_report.py`
  lê `tabelas_finais/*.csv` e `mapas/*.png` e monta o HTML do zero a cada
  rodada (primeiro gerador persistido do projeto, desde v5).

## 1. Objetivo

1. Reduzir a repetição visual: cortes de dado que hoje viram N gráficos
   viram 1 gráfico + seletor de opções.
2. Adicionar interação sem sair do modelo "arquivo HTML único, sem backend,
   sem build step para o HTML em si" já estabelecido em
   `specs/2026-09-09_visual-identity/specs.md` §4 decisão A — refinado nesta rodada só no
   que diz respeito a **deploy** (§5.1), não à arquitetura do arquivo.
3. Reorganizar o espaço da página para dar lugar de verdade à análise
   textual (hoje o HTML é "só visualização" por decisão de
   `specs/2026-09-09_visual-identity` §2 — isso é revisto aqui, ver §3.4).
4. Adotar um estilo mais "clean/brutalista" — bordas visíveis, blocos
   segmentados, menos dependência de sombra suave — sem abandonar a
   identidade já validada (paleta de 11 cores categóricas, tipografia
   Fraunces/IBM Plex Sans/IBM Plex Mono, tokens de tema claro/escuro).
5. Todo ponto de dado — gráfico ou mapa — mostra rótulo + valor ao passar o
   mouse, sem exceção (§3.5, §3.8). Séries temporais, além disso, marcam
   valor mais alto, mais baixo e mais recente **sem precisar de hover**
   (§3.9).

## 2. Features (do pedido do usuário, mapeadas ao estado atual)

| # | Feature pedida | Onde se aplica hoje | Resolve o quê |
|---|---|---|---|
| 1 | Seções visualmente segmentadas | Todas as 9 `h2` | Hoje é rolagem contínua sem fronteira visual forte entre seções |
| 2 | Estilo clean/brutalista | CSS global (`--shadow` → borda sólida) | Substitui cartões com sombra suave por blocos de borda `2px solid var(--ink)`, cantos retos |
| 3 | Múltiplas opções de gráfico em vez de múltiplos gráficos | CID-10 (~18 gráficos), CAP (6–8 gráficos), cobertura vacinal por ano, evitáveis por subgrupo×CAP | Substitui parede de `div.out` repetidos por 1 chart-card + seletor de pills verticais |
| 4 | Tooltips interativos em gráficos **e mapas** — rótulo + valor em todo ponto | Gráficos já têm; mapas não (raster) | Gráficos: estende o hover atual a todo ponto/barra, sempre com rótulo + valor. Mapas: migra de PNG para SVG vetorial para hover por bairro/CAP — ver §3.5 (maior item de esforço da rodada, mas dentro do escopo, sem faseamento) |
| 5 | Seções retráteis | As 9 `h2` | Collapse/expand independente por seção, só nível `h2` (decisão, §4-A) |
| 6 | Navbar persistente com links para seções principais | Substitui o "Sumário" estático no topo | Sticky, hambúrguer, 9 links (nível `h2` só, decisão §4-C) |
| 7 | Remover outliers (gráficos e mapas) | Qualquer série numérica | Toggle por chart-card; dado pré-computado nas duas versões (decisão §4-B) |
| 8 | Baixar dado completo e filtrado | Qualquer chart-card | Botão de download por gráfico, CSV, respeita opção selecionada + toggle de outliers (decisão §4-D) |

## 3. Decisões de design/arquitetura

### 3.1 Seções retráteis — nível `h2` só

Cada uma das 9 seções principais abre/fecha independente. Subseções (`h3`)
dentro de uma seção aberta ficam sempre visíveis — não há um segundo nível de
collapse. Estado inicial: todas expandidas. Estado de collapse **não é
persistido** entre sessões (sem `localStorage`) — é uma leitura tipicamente
única por visitante; se isso incomodar na prática, é fácil adicionar depois.

### 3.2 Seletor de opções de gráfico/mapa — pills verticais

Pílulas empilhadas verticalmente à esquerda do chart-card, como no
wireframe (`Option 1`/`Option 2`/...). Para os casos com poucas opções
(≤6 — a maioria: cobertura vacinal por ano, mapas por CAP, categorias de
evitabilidade) isso funciona bem sem modificação. Para o caso extremo (CID-10,
até ~18 subgrupos) a coluna de pills fica com `overflow-y:auto` e altura
máxima igual à do chart-card — mantém o padrão visual único do wireframe em
vez de trocar para `<select>` nesses casos, ao custo de precisar rolar a
lista de opções quando ela for longa.

**Atualização desta rodada — ver §3.13**: o seletor de opções passa a existir
em praticamente todo chart-card/map-card do relatório (não só nos 2 casos
convertidos até aqui), como parte do agrupamento de visualizações por seção
(§9). O padrão de pills em si não muda; o que muda é (a) quase toda
visualização agora tem pelo menos 1 pill (mesmo com 1 opção só a estrutura
é reaproveitada, sem coluna de pills visível — regra já existente), e (b)
o texto de análise passa a viver **dentro** de cada opção, não fora do
seletor (§3.13).

### 3.3 Outliers — pré-computados, só para percentuais/taxas

O gerador (`build_html_report.py`) calcula, para cada série numérica **que
seja percentual ou taxa**, a versão com e sem outliers e embute as duas como
JSON. O toggle no cliente só troca qual array o gráfico/mapa lê — sem lógica
estatística em JS.

- **Escopo restringido nesta rodada (decisão nova, §4-O)**: outliers **não**
  são calculados/removidos em números absolutos (contagens — óbitos,
  nascidos vivos, crianças no CadÚnico, etc.). Só se aplica a séries que já
  são percentual/taxa (`format='pct1'` no motor JS — % de óbitos evitáveis,
  taxa de mortalidade por mil, % de crianças no CadÚnico sobre o Censo...).
  Motivo: um valor absoluto "fora da faixa" é frequentemente o dado mais
  relevante da série (um pico real de óbitos num ano, não um erro de
  medição), enquanto uma taxa/percentual anômala tem mais chance de refletir
  um denominador pequeno ou um problema de base de dados (ver o próprio
  aviso do notebook sobre o outlier de >500% no CadÚnico/Censo). Reverte a
  regra genérica "aplica em toda série numérica" da rodada anterior.
- **Regra de outlier** (mantida): cercas de Tukey,
  `[Q1 - 1.5×IQR, Q3 + 1.5×IQR]`, calculada por série/corte individualmente
  (não globalmente por seção).
- Pontos removidos ficam ocultos (não substituídos por interpolação) — a
  série "sem outliers" tem menos pontos, não pontos alterados.
- Mapas: idem — só mapas cuja métrica é percentual/taxa (`fmt='pct1'` em
  `mapa_svg`) ganham o toggle de outliers; mapas de contagem absoluta não.

### 3.4 Espaço para análise textual — reversão parcial da decisão B de `specs/2026-09-09_visual-identity`

`specs/2026-09-09_visual-identity/specs.md` §4 decisão B removeu a prosa/notas de método
do HTML, deixando "só visualização" (título + fonte). Esta rodada reintroduz
espaço textual, mas **redefinido**, não como retorno ao texto integral do
notebook:

- Bloco "Principais achados" por seção (`h2`) — lista curta, editorial, não
  o texto de método completo do notebook. **Ainda não implementado** (gap de
  conteúdo registrado em `relatorio/specs.md` v6.1/`feature_roadmap.md`) —
  continua fora do escopo até existir texto real curado por alguém.
- Bloco de análise por chart-card/map-card/tabela — **decisão tomada nesta
  rodada: o texto muda por opção do seletor**, não fica fixo por card. Ver
  §3.13 para o layout exato (3 padrões) e a implicação técnica de o texto
  virar parte de cada opção, não um elemento externo ao seletor.
- O texto de método completo continua vivendo só no notebook/PDF — este spec
  não reverte isso.
- **Conteúdo placeholder nesta rodada**: todo bloco de análise é preenchido
  com lorem ipsum (~500 palavras cada, texto de preenchimento clássico, sem
  qualquer leitura analítica real) — marca claramente onde o texto de
  verdade vai entrar depois, sem fabricar uma interpretação dos dados que
  ninguém validou (mesmo cuidado do bloco "Principais achados" acima, só que
  aqui preenchido com lorem ipsum em vez de deixado vazio, porque o pedido
  desta rodada é especificamente ver o layout com o espaço de texto ocupado).

### 3.5 Mapas: tooltip por região exige migrar de PNG para SVG — dentro do escopo desta rodada

Os mapas hoje são PNG/WebP estáticos gerados pelo skill `generate_map`
(geopandas + contextily, sem geometria exposta no HTML). Tooltip real por
bairro/CAP (mostrar rótulo + valor ao passar o mouse sobre uma região)
exige que o mapa vire SVG vetorial com um `<path>` por região e dado
embutido — o mesmo padrão de tooltip que os gráficos de linha/barra já
usam, aplicado a polígonos em vez de pontos. **Confirmado com o usuário: é
requisito desta rodada, não fica faseado para depois.** É, de longe, o
item de maior esforço da lista (novo pipeline geométrico), mas entra no
escopo de implementação mesmo assim.

Pipeline proposto, reaproveitando o que `generate_map`/`analise.py` já
resolveram (ver `.claude/skills/generate_map/SKILL.md`):

1. **Geometria fonte**: `dados_locais/geo/limite_bairros_rio.geojson` (166
   bairros, já simplificado para ~19,5k pontos, `EPSG:4326`, chave
   `codbairro`). Para AP/RP, dissolver pelas mesmas colunas que
   `mapa_coropletico_bairros` já usa (`area_plane` — 5 regiões; `cod_rp` —
   16 regiões) em vez de reprojetar/gerar geometria nova.
2. **GeoJSON → paths SVG**: converter os polígonos (já em `EPSG:4326`, ou
   projetados para `EPSG:3857` como o PNG atual faz) para atributos `d` de
   `<path>`, num `viewBox` fixo por nível (bairro/AP/RP) — geopandas expõe
   as coordenadas do polígono simplificado diretamente, sem precisar de
   nenhuma lib JS de projeção cartográfica no cliente.
3. **Dado por região**: cada `<path>` carrega `data-codigo`, `data-label`
   (nome do bairro/CAP) e `data-valor` (+ `data-valor-sem-outliers` quando
   aplicável) — mesma ideia de "dado pré-computado embutido" já usada para
   gráficos (§3.3).
4. **Preenchimento**: mesma escala sequencial por tema já definida em
   `specs/2026-09-09_visual-identity/specs.md` §3.1 (`Teal` natalidade, `RdPu`/`PuRd`
   mortalidade, `YlOrBr` CadÚnico, `Blues` Censo) — calculada em Python no
   gerador e aplicada como `fill` inline por `<path>`, sem reimplementar a
   classificação de bins em JS.
5. **Interação**: reusa o controlador de tooltip do motor de gráfico
   (§3.8) — hover num `<path>` mostra rótulo + valor, igual a um ponto de
   linha ou uma barra.
6. **Legenda, norte, escala, footnote**: elementos textuais/estáticos do
   mapa atual (título serifado, footnote de fonte/CRS, legenda) continuam
   como marcação HTML/SVG simples ao lado do `<svg>` do mapa — só a
   camada de polígonos coloridos muda de raster para vetor. Basemap
   (`contextily`) e camadas de contexto (UF, municípios vizinhos) **não**
   são portados para o SVG — eram um recurso do PNG estático; o mapa
   interativo fica só com os polígonos do município + tooltip, sem fundo
   cartográfico.
7. Efeito colateral bom: SVG embutido como texto é **mais leve e mais
   autocontido** do que PNG em `data:` URI para geometria já simplificada
   deste tamanho — elimina a dependência de arquivo de imagem externo por
   mapa.

### 3.6 Navbar persistente — nível `h2` só

Barra fixa no topo (`position: sticky; top:0`), sempre visível durante a
rolagem. Ícone de hambúrguer abre um painel com as 9 seções (emoji + título),
mesmo nível hoje coberto pelo "Sumário" — que deixa de existir como bloco
solto no topo da página e vira esse menu. Sem os `h3` no menu (ficariam ~35
itens, texto demais para um painel dropdown) — chegar a uma subseção continua
sendo rolar dentro da seção já aberta.

### 3.7 Download de dados — por gráfico

Cada chart-card (gráfico ou mapa) ganha um botão de download próprio, CSV,
respeitando o estado atual daquele card (opção do seletor + toggle de
outliers). Não há botão de "baixar tudo" nesta rodada — arquivo CSV por
card é suficiente dado que `tabelas_finais/*.csv` já existe como fonte bruta
completa para quem quiser os dados sem filtro nenhum.

### 3.8 Tooltip — conteúdo padrão: rótulo + valor, em todo ponto, gráfico ou mapa

Regra única para os dois motores (gráfico e mapa, §3.5): ao passar o mouse
sobre **qualquer** ponto/barra/região, o tooltip mostra rótulo (categoria,
ano, nome do bairro/CAP) + valor formatado (mesma formatação pt-BR já usada
no resto do projeto — separador de milhar `.`, sufixo `%` quando aplicável).
Não é opcional por gráfico — é o comportamento padrão de todo chart-card.

- Gráficos de linha/barra: já é o comportamento hoje (`lineChart`/
  `barChart`/`groupedBarChart` — ver `relatorio/specs.md`); esta rodada
  estende a mesma implementação para as novas variantes com seletor de
  opção (o tooltip segue a série/opção ativa no momento).
- Mapas: novo — cada `<path>` de bairro/CAP (§3.5) recebe o mesmo
  controlador de tooltip, lendo `data-label`/`data-valor` do próprio
  elemento.

### 3.9 Séries temporais — marcação padrão de máximo, mínimo e mais recente

Em todo gráfico de linha (`lineChart`), três pontos ganham rótulo direto
sempre visível — sem precisar de hover — por padrão, por série ativa:

- **Valor mais alto** da série.
- **Valor mais baixo** da série.
- **Valor mais recente** (último ponto no eixo temporal).

Pontos intermediários continuam só com tooltip no hover (§3.8), não rótulo
fixo — marcar todos os pontos por padrão poluiria o gráfico, o que esses
três justamente evitam.

- Quando dois desses três coincidem no mesmo ponto (ex.: o valor mais
  recente também é o mais alto), um único rótulo é mostrado, não duplicado.
- Aplica-se por série visível — no caso de séries com destaque (regra de
  `specs/2026-09-09_visual-identity/specs.md` §3.3, mais de 6 linhas → só as N mais
  relevantes coloridas, resto agrupado em "Outras (N)"), a marcação
  máx/mín/recente vale para as séries coloridas em destaque, não para o
  agregado cinza "Outras".
- Ao trocar a opção ativa no seletor (§3.2), os três rótulos recalculam
  para a série/corte recém-selecionado.
- Não se aplica a `barChart`/`groupedBarChart` (não são séries temporais)
  nem aos mapas (não há "mais recente" num corte espacial de um só ano) —
  só a `lineChart`.

### 3.10 Identidade visual institucional (IPP / Prefeitura do Rio)

Pedido do usuário: aproximar o visual do relatório da identidade
institucional de `ipp.prefeitura.rio`, sem mudar tipografia nem a
funcionalidade já especificada. Cores e composição do logo foram extraídas
diretamente do CSS/HTML publicado do site (não estimadas):

- **Navy institucional** `#004a80` — cor de fundo do rodapé no site real
  (`#wrapper-footer-prefeitura`). Usada aqui como cor institucional
  primária.
- **Família azul/ciano de apoio** — `#4579fb`, `#00aeef`, `#02b1d7`,
  `#00c0f4`, `#008eb6` (botões, estados de hover, destaques pontuais no site
  real).
- **Verde-água** `#0bb975`/`#09b88a`/`#0ab786` — é literalmente a cor padrão
  de link (`a, a:hover { color: #0bb975 }`) do site do IPP. Coincidência
  favorável: já fica muito próxima do `--accent` (`#2E9678`) que o relatório
  já usa — **não precisa mudar** para "conversar" com a identidade
  institucional, é só documentar a proximidade.
- **Logo**: `PREFEITURA [brasão do Rio] RIO | Instituto Pereira Passos`,
  versão monocromática branca (pensada para fundo escuro/colorido) — mesmo
  arquivo usado no cabeçalho do site real.

**Aplicação (subtil, conforme pedido — decisão §4-L)**: fundo do corpo do
relatório continua branco/tinta brutalista, sem alteração. O navy entra em
só dois lugares:
1. Barra de 4px no topo da página, acima da navbar.
2. Rodapé novo (§3.11), fundo sólido navy.
No navbar em si, o logo fica num pequeno chip navy (o logo é
monocromático branco — precisa de fundo escuro para ficar legível sobre a
navbar branca). Nenhuma cor institucional nova entra na paleta categórica
de dados (`--c1`…`--c11`) nem nos estados de interação já especificados
(seletor de opção, toggle de outliers) — isso ficou fora do pedido
("sem mudanças substanciais na funcionalidade").

**Logo — decisão registrada, reverte uma decisão anterior do projeto**:
`relatorio/specs.md` (histórico v2, "Ajustes pontuais em v2") registra que o
projeto **evitou deliberadamente** usar/gerar um logo real do Instituto
Pereira Passos, "para não publicar uma marca institucional não verificada".
Nesta rodada, a pedido direto do usuário, essa decisão é revertida: o logo
real (baixado de `ipp.prefeitura.rio`) é embutido no mockup. **Como esta
sessão não está autenticada com um domínio `@prefeitura.rio`/`@ipp`,
fica registrado aqui como pendência a confirmar antes do deploy público
(§5.1, GitHub Pages torna o arquivo público)**: validar com alguém do IPP
que o uso do brasão/logo oficial neste relatório está autorizado.

### 3.11 Rodapé — novo componente

Rodapé institucional, fundo navy (`#004a80`), texto claro. Escopo
enxuto para o que é relevante a um relatório de dados, não uma réplica do
rodapé completo do site institucional (decisão §4-M):

- Logo (mesmo arquivo do navbar, maior) + uma frase curta de contexto
  ("Relatório produzido a partir da análise de indicadores de primeira
  infância do Instituto Municipal de Urbanismo Pereira Passos (IPP)").
- **Fontes de dados**: lista curta (Censo 2022, CadÚnico, DataSUS/Tabnet,
  SISVAN/SIDRA) — mesma fonte já citada por gráfico (§3.8), aqui como visão
  geral.
- **Links**: `ipp.prefeitura.rio`, Transparência Rio, LGPD (proteção de
  dados) — os três elementos do rodapé real do site que fazem sentido num
  relatório de dados públicos; **omitidos**: endereço físico, telefone,
  ícones de redes sociais (pertencem ao site institucional principal, não a
  este sub-relatório).
- **Contato**: e-mail de contato para o relatório + data de "atualizado em"
  (derivada da data de geração do `build_html_report.py`).
- Tipografia mantida (IBM Plex Sans/Mono) — só a cor de fundo/texto muda
  para o esquema navy.

### 3.12 Bloco de título — "barra de espectro" + consistência nos cabeçalhos de seção

O bloco de título/descrição (topo da página, antes da primeira seção)
ganhou um tratamento específico, escolhido entre 3 opções sketch (ver canvas
de design, artboard `HeaderOptions`):

- **Eyebrow do título** ("PROJETO · RELATÓRIO INTERATIVO") passa de cinza
  neutro (`--ink-3`, o padrão de qualquer legenda mono) para `--accent`
  (o verde já usado em links) + peso 700 — não usa nenhuma cor institucional
  nova, só a que já existe. **Correção feita na implementação**: o plano
  original desta linha dizia `--accent-ink`, mas esse token é escuro demais
  para texto direto sobre o fundo da página no tema escuro (pensado para
  texto sobre um chip claro) — trocado por `--accent` antes mesmo desta
  rodada de remoção do tema escuro (ver `relatorio/specs.md` v6, "bug real
  encontrado e corrigido").
- **Barra de espectro**: uma faixa de 6px logo abaixo do bloco de
  título/descrição, dividida em 11 segmentos iguais, um por cor categórica
  (`--c1`…`--c11`) — assinatura visual única da página (não se repete em
  mais nenhum lugar do relatório), sinalizando "isto contém muitas séries de
  dado diferentes" sem introduzir nenhuma cor nova.
- **Descartadas nesta escolha** (registradas no canvas, não implementadas):
  bloco navy assimétrico atrás da descrição (reabriria a decisão §4-L de
  manter o navy só em linha/rodapé) e moldura com cantos em `--accent`
  (mais "decorada" do que o pedido pedia).

**Consistência nos cabeçalhos de seção (`h2`)** — extensão do mesmo
princípio, não uma cor nova:
- O eyebrow "SEÇÃO N DE 9" de uma seção **expandida** usa o mesmo tratamento
  do eyebrow do título (`--accent-ink`, peso 700) — mesma linguagem visual
  do topo da página aplicada a cada cabeçalho de seção.
- O eyebrow de uma seção **recolhida** continua no cinza padrão (`--ink-3`,
  sem negrito) — a cor faz parte do próprio sinal de estado: expandido =
  destacado, recolhido = neutro. Não é uma inconsistência a corrigir, é a
  hierarquia visual do collapse (§3.1) reforçada pela cor.
- A barra de espectro **não se repete** nos cabeçalhos de seção — fica
  exclusiva do topo da página, como uma "vinheta" única, para não virar um
  padrão repetitivo a cada seção (eram 9 repetições).

### 3.13 Layout de conteúdo — 3 padrões (gráfico, mapa, tabela) + texto por opção

Replanejamento desta rodada, a partir de uma revisão do canvas de design
(`https://claude.ai/code/artifact/6d48c53d-9799-4ac6-be36-a7fa9ca5f64e`)
contra o HTML gerado: o texto de análise não tinha sido implementado (só
existia no mockup) e, ao planejar como implementá-lo, ficou claro que ele
precisa **trocar junto com a opção ativa do seletor** — cada opção passa a
carregar seu próprio texto, não um texto fixo por card. Isso define 3
padrões de layout, um por tipo de conteúdo:

**Padrão A — gráfico (linha/barra/barra agrupada).** Pills à esquerda +
gráfico à direita, na mesma linha (como já é hoje). O texto de análise fica
**abaixo**, ocupando a largura inteira do card (pills + gráfico juntos) —
não só a largura do gráfico. Ao trocar de pill, o gráfico troca **e** o
texto abaixo troca junto (é o texto daquela opção especificamente).

**Padrão B — mapa.** Pills à esquerda + mapa/legenda à direita, igual ao
padrão atual. O texto de análise fica numa coluna **à direita do mapa**
(3ª coluna: pills | mapa+legenda | texto), não abaixo — mesma posição que o
wireframe original já mostrava para mapas. Troca de pill troca o mapa e o
texto lateral juntos.

**Padrão C — tabela (novo, não existia no wireframe nem no HTML atual).**
Texto à **esquerda**, tabela à **direita** — ordem invertida em relação aos
padrões A/B (texto antes do dado, não depois/ao lado). Sem coluna de pills
nesta rodada (as tabelas do relatório hoje — ex. "Top 10 bairros" do Censo —
não têm cortes alternativos; se um caso com opções aparecer depois, adiciona-se
pills à esquerda do texto, mesma lógica dos outros 2 padrões).

**Implicação técnica**: o formato interno de `option_card` muda de
`(label, build_fn)` para `(label, build_fn, texto)` — cada entrada carrega
seu texto. Card de opção única (a maioria, sem pills visíveis) também ganha
texto, só que fixo (1 opção = 1 texto, nada para trocar). O JS de troca de
pill (`initPills`) passa a alternar 2 elementos por opção (painel do
gráfico/mapa + painel de texto), não 1.

**Conteúdo dos textos nesta rodada**: lorem ipsum, ~500 palavras por bloco
(ver §3.4) — texto de preenchimento puro, não uma tentativa de análise real.

### 3.14 Tema único (claro) — remove o tema escuro automático

Decisão nova: `relatorio/index.html` deixa de ter tema escuro automático via
`prefers-color-scheme`. Só o tema claro existe — simplifica a folha de
estilo (remove o bloco `@media (prefers-color-scheme: dark)` e o seletor
`:root[data-theme="dark"]`, que hoje duplicam todas as variáveis de cor) e
elimina uma superfície inteira de teste (a maior parte da validação visual
desta spec até agora só cobriu o tema escuro, por ser o default do ambiente
de screenshot usado — ver `specs/2026-09-14_relatorio-interativo/validation.md` V8).
Paleta categórica de dados (`--c1`…`--c11`), cores institucionais
(`--ipp-navy`/`--ipp-cyan`) e o restante do sistema de tokens continuam os
mesmos valores que já existem para o tema claro — não é uma paleta nova,
só a remoção da variante escura.

### 3.15 Corpo mais largo

`.doc{max-width:880px}` era estreito demais mesmo para o padrão A (pills +
gráfico + texto abaixo, tudo cabendo em 880px deixa pouco espaço para
qualquer um dos três elementos) — mais ainda para o padrão B (3 colunas:
pills + mapa + texto) e o padrão C (texto + tabela lado a lado). Proposta
(default se não houver objeção): `max-width:1200px` — grande o suficiente
para os 3 padrões respirarem, sem virar uma coluna de leitura larga demais
para os blocos de texto corrido (achados, notas). Os elementos de largura
total (navbar, barra de topo, rodapé) já são full-bleed independentemente
deste valor (§3.10), não são afetados.

## 4. Tabela de decisões (formato igual a `specs/2026-09-09_visual-identity/specs.md` §4)

| # | Pergunta | Decisão (confirmada com o usuário nesta rodada) |
|---|---|---|
| A | Nível de collapse das seções retráteis | `h2` só (não `h3`) |
| B | Cálculo do toggle de outliers | Pré-computado no gerador Python, embutido como JSON; regra proposta = cercas de Tukey 1.5×IQR por série (default, sem objeção ainda) |
| C | Profundidade da navbar persistente | Só `h2` (9 links) |
| D | Escopo do botão de download | Por gráfico/mapa individual, CSV |
| E | Seletor de opções (pills vs. dropdown) | Pills verticais sempre, como no wireframe — inclusive para listas longas (CID-10), com rolagem interna na coluna |
| F | Este round entrega implementação ou só spec+layout? | Só spec + layout revisado. Implementação é uma rodada separada, após revisão |
| G | Tooltip em mapas exige migração PNG→SVG? | Sim — e está **dentro do escopo desta rodada** (não faseado), pedido direto do usuário; ver pipeline em §3.5 |
| H | Conteúdo padrão do tooltip | Rótulo + valor em todo ponto/barra/região, gráfico ou mapa — não opcional por card (§3.8) |
| I | Séries temporais: algum rótulo fixo, sem hover? | Sim — valor mais alto, mais baixo e mais recente, sempre visíveis por série ativa (§3.9) |
| J | Hospedagem/deploy | GitHub Pages, via GitHub Actions (`actions/deploy-pages`) — ver §5.1 |
| K | Logo institucional: real ou lockup em texto? | **Logo real** (reverte a decisão anterior de `relatorio/specs.md` que evitava isso) — pendência de confirmar autorização antes do deploy público, ver §3.10 |
| L | Intensidade de aplicação das cores institucionais | Navy só em: barra de 4px no topo + rodapé + chip do logo no navbar. Corpo do relatório e paleta de dados não mudam (§3.10) |
| M | Escopo do conteúdo do rodapé | Enxuto — fontes de dados, 3 links (IPP, Transparência Rio, LGPD), contato, data de atualização. Sem endereço/telefone/redes sociais (§3.11) |
| N | Tratamento do bloco de título/descrição | Opção A ("barra de espectro") — eyebrow em `--accent` + faixa de 6px com as 11 cores categóricas; mesma cor de eyebrow estendida aos cabeçalhos de seção expandidos, por consistência (§3.12) |
| O | Outliers em números absolutos (contagens)? | **Não** — só percentuais/taxas ganham o toggle de outliers a partir de agora (§3.3) |
| P | Texto de análise: fixo por card ou por opção do seletor? | **Por opção** — troca junto com a pill ativa (§3.13) |
| Q | Tema escuro automático? | **Removido** — só tema claro a partir de agora (§3.14) |
| R | Largura do corpo (`.doc`) | `880px` → `1200px` (default, sem objeção ainda) (§3.15) |

## 5. Stack técnica

Mantém a regra de arquitetura já estabelecida em
`specs/2026-09-09_visual-identity/specs.md` (arquivo HTML único, sem passo de build, sem
backend) — nenhuma das features pedidas exige quebrar essa regra. O único
item novo é **onde** o arquivo passa a ser servido (§5.1).

- **JS**: vanilla, sem biblioteca/dependência nova (Alpine.js foi cogitado e
  descartado — não traz benefício suficiente para justificar uma dependência
  externa num arquivo que hoje é zero-dependência). Estende o motor
  existente (`lineChart`/`barChart`/`groupedBarChart`) com:
  - um controlador de seletor de opção por chart-card (fecho JS simples —
    guarda qual opção está ativa, re-renderiza o SVG do card ao clicar numa
    pill);
  - um controlador de collapse por seção (`h2`);
  - um controlador de toggle de outliers por chart-card (troca qual array
    embutido o gráfico lê);
  - uma função de serialização CSV client-side (gera o arquivo a partir do
    JSON já embutido — sem round-trip de rede) para o botão de download.
- **CSS**: sem framework. Camada brutalista nova por cima do sistema de
  variáveis já existente (`--ink`, `--page`, `--surface-2`, `--accent`,
  paleta `--c1`…`--c11`): bordas sólidas `2px solid var(--ink)` no lugar de
  `var(--shadow)` nos cartões novos (chart-card, seção, callout de
  takeaways), `border-radius:0` consistente, tipografia mantida (Fraunces
  display / IBM Plex Sans body / IBM Plex Mono para labels e meta).
- **Geração**: `build_html_report.py` ganha (quando a implementação for
  aprovada): agrupamento de N cortes correlatos em 1 definição de chart-card
  com N séries nomeadas (em vez de N blocos `.out` separados); cálculo da
  variante sem-outliers por série; nenhuma mudança de fonte de dado
  (continua lendo `tabelas_finais/*.csv`).
- **Mapas**: pipeline novo, dentro do escopo desta rodada — geometria
  GeoJSON → paths SVG com dado por região embutido, no lugar do PNG atual
  (detalhado em §3.5). Deixa de depender de `mapas/*.png`/`contextily` no
  lado do HTML; a geração em Python continua usando geopandas (só para ler
  e simplificar a geometria/join, não para renderizar o raster final).
- Sem `package.json`, sem bundler — o arquivo continua sendo gerado por um
  script Python, sem passo de compilação de front-end.

### 5.1 Deploy — GitHub Pages

Pipeline planejado de hospedagem (decisão desta rodada, tabela §4-J):

- **Hospedagem**: GitHub Pages, publicando via **GitHub Actions**
  (`actions/upload-pages-artifact` + `actions/deploy-pages`, o fluxo oficial
  atual do GitHub) — não uma branch `gh-pages` mantida manualmente. O
  workflow copia `relatorio/index.html` para a raiz do artefato de Pages
  como `index.html`; nenhum outro arquivo do repositório (notebook,
  `dados_locais/`, `Tabelas_finais/`, etc.) é publicado.
- **Gatilho**: `workflow_dispatch` (manual) no mínimo; opcionalmente também
  em push para `staging_main` quando `relatorio/index.html` mudar — a
  decidir na implementação, não bloqueia este spec.
- **Por que continua sendo 1 arquivo autocontido, mesmo podendo servir
  vários arquivos estáticos no GitHub Pages**: o site do GitHub Pages para
  este repositório fica em `https://<usuário>.github.io/<repo>/` — qualquer
  asset externo referenciado por caminho relativo/absoluto teria que
  considerar esse prefixo de path. Continuar com tudo embutido (dado, CSS,
  JS, e agora os mapas como SVG inline em vez de PNG — ver §3.5 item 7)
  evita esse problema inteiramente: o arquivo funciona idêntico em
  `file://`, num servidor estático qualquer, ou no Pages, sem nenhuma
  lógica de base-path.
- Sem backend, sem API, sem `.nojekyll`/config adicional além do workflow —
  GitHub Pages serve o HTML exatamente como está.

## 6. Layout revisado (entregável desta rodada)

Wireframe revisado, unindo a estrutura do `relatorio/Page 1.pdf` com o
conteúdo real do relatório atual (seções, textos e paleta de
`relatorio/index.html`), publicado como canvas de design:

**https://claude.ai/code/artifact/6d48c53d-9799-4ac6-be36-a7fa9ca5f64e**

Contém 2 artboards:

- **Main** — barra de acento navy + navbar persistente aberta (com o chip do
  logo institucional), cabeçalho do relatório, uma seção `h2` completa
  expandida (⛓️ Óbitos por causas evitáveis, usada como exemplo por ser o
  caso mais extremo de repetição hoje) mostrando bloco de achados, texto de
  análise, chart-card de gráfico (seletor de categorias CID-10 + toggle de
  outliers + download) e chart-card de mapa (seletor de CAP + toggle de
  outliers + download + painel de análise lateral), a seção seguinte
  mostrada recolhida para dar o ritmo da página, e o rodapé institucional
  (§3.11) ao final.
- **States** — comparação lado a lado do estado recolhido vs. expandido de
  uma seção `h2` (🗂️ CadÚnico), em close-up.

É um mockup estático de revisão (não um protótipo clicável) — serve para
validar estrutura e hierarquia visual antes de qualquer implementação.

## 7. Fora de escopo (registrar no roadmap)

- Implementação em si (rebuild de `relatorio/index.html`) — próxima rodada.
- Basemap/contexto geográfico (satélite ou desenho, UF, municípios
  vizinhos) nos mapas interativos SVG — eram exclusivos do pipeline PNG
  (`generate_map`) e não são portados; o mapa interativo mostra só os
  polígonos do município + tooltip (ver §3.5 item 6).
- Botão de "baixar tudo" (fora do escopo pedido — só download por gráfico).
- Qualquer mudança de conteúdo/dado novo (esta rodada é só
  reestruturação visual e de interação).
- Persistir estado de collapse entre sessões (`localStorage`) — considerar
  depois se for pedido.
- Domínio customizado / HTTPS extra para o GitHub Pages — usa o domínio
  padrão `github.io`.

## 8. Revisão geral e sugestões de melhoria

Pedido do usuário nesta rodada: revisão geral do design, além dos itens
específicos acima. Observações levantadas ao revisar o mockup atualizado:

1. **Autorização do logo é a pendência mais importante** (já registrada em
   §3.10/§4-K) — bloqueia o deploy público (§5.1) até ser confirmada, não só
   o visual. Sugiro resolver isso antes de qualquer outra coisa nesta lista.
2. **Responsividade ainda não especificada.** O layout de seletor de pills
   verticais + painel lateral (gráfico: pills + card; mapa: pills + card +
   painel de análise — três colunas) não foi pensado para telas estreitas.
   Sugestão para a implementação: abaixo de um breakpoint (~720px), as pills
   viram uma faixa horizontal com scroll (em vez de empilhadas na lateral) e
   o painel de análise ao lado do mapa desce para abaixo dele. Vale um
   spec/decisão própria quando a implementação começar — não é parte desta
   rodada, mas fica sinalizado para não ser esquecido.
3. **Contraste do rodapé**: o texto secundário claro sobre navy (usado para
   labels tipo "FONTES DE DADOS") é mais dessaturado que o texto principal —
   vale checar contraste real (WCAG AA) na implementação, não só no mockup.
4. **"Voltar ao topo"**: com o rodapé novo alongando a página (e a navbar já
   ocupando o topo como sticky), um botão fixo de voltar ao topo melhora a
   navegação em seções tardias (ex.: 🎓 Educação, a última).
5. **O `--accent` atual do relatório já "conversa" com a identidade
   institucional** (§3.10 — o verde-água do IPP e o `--accent` do relatório
   são visualmente muito próximos) — não é uma mudança a fazer, é uma boa
   notícia: não há conflito de paleta entre o que já existe e o que está
   sendo adicionado agora.
6. **Chip do logo no navbar é pequeno** (20px de altura) — vale testar
   legibilidade em telas de alta densidade/mobile durante a implementação,
   antes de considerar o tamanho definitivo.
7. **O menu do navbar (§3.6) poderia linkar para o rodapé** (ex.: item
   "Fontes e contato") já que ele passa a concentrar informação que hoje só
   existe implicitamente, espalhada por gráfico — sugestão a avaliar na
   implementação, não é um requisito confirmado nesta rodada.

## 9. Proposta de agrupamento de visualizações por seção

Pedido do usuário: com texto por opção (§3.13) tornando cada card maior,
seções continuarem curtas depende de agrupar cortes correlatos num só
chart-card/map-card com pills, em vez de vários cards em sequência — o
mesmo movimento já feito em 2 casos (§ "Por CAP e faixa etária", "Grupo
evitável por CAP"), agora estendido ao resto do relatório. Levantamento
feito direto em `build_html_report.py` (call sites reais, não estimados).
Alvo por seção: **achados + análise inicial + 1(-2) grupo(s) de gráfico +
1 grupo de mapa** — não necessariamente 1 grupo só quando os cortes não são
comparáveis entre si (mesmo princípio já usado para não forçar pills na
galeria de mapas do CAP, §3.2).

| Seção | Hoje (cards separados) | Proposta de agrupamento |
|---|---|---|
| 🏘️ Censo 2022 | Tabela top 10 + 2 grouped-bar (raça, sexo) + 6 mapas + 2 line charts | Tabela → **padrão C** (texto+tabela). Grupo gráfico "População 0-6" = pills [raça, sexo] (2). Grupo gráfico "Série temporal" = pills [Total/Fem/Masc, % 0-4] (2). Grupo mapa "Censo por nível" = pills [bairro abs, bairro %, AP abs, AP %, RP abs, RP %] (6) |
| 🗂️ CadÚnico | 2 pares bar (renda, idade) + 3 mapas | Grupo gráfico "Por faixa de renda/idade" = pills [Renda, Idade] (2, cada opção já mostra o par Crianças/Famílias). Grupo mapa "Mapas" = pills [Crianças 0-6, Crianças 0-4, % s/ Censo] (3) |
| 🏥 DataSUS/Tabnet | 4 line charts + 5 mapas, em 3 subseções | Grupo gráfico "Séries temporais" = pills [Nascidos vivos, % baixo peso, Óbitos raça abs, Óbitos raça %] (4). Grupo mapa "Mapas" = pills [Nascidos vivos, Baixo peso abs, % baixo peso, Óbitos 0-364, Taxa mortalidade infantil] (5) |
| ⛓️ Óbitos por causas evitáveis | Maior seção: ~14 line charts fora dos 2 grupos já existentes, + 8 mapas soltos | Grupo "Por raça/cor" = pills [Abs, %, Abs sem NI, % sem NI] (4). Grupo "Por grupo/subgrupo CID-10" = pills [8 combinações faixa×corte] (8, já é o padrão do CAP). "Comparação entre faixas" fica solo (1 gráfico, sem par comparável). Grupo "Por CAP e faixa etária" mantido (18, já existe). Grupo "Grupo evitável + gestação/parto, por CAP" = merge de 2 grupos existentes em 1 (3+2=5 pills). Grupo "Panorama <5 anos" = pills [Óbitos por subgrupo, Taxa por mil NV] (2). Grupo mapa "Mapas por CAP" = pills com as 8 opções hoje soltas em sequência |
| 🤰 Gravidez e puerpério | 2 line charts + 2 mapas, soltos | Grupo gráfico = pills [Gravidez, Puerpério] (2). Grupo mapa = pills [Gravidez, Puerpério] (2) |
| 🩺 Mortalidade neonatal | 4 line charts + 8 mapas, em 4 subseções (precoce/tardia/pós/total) | Grupo gráfico "Taxa por fase" = pills [Precoce, Tardia, Pós-neonatal, Total] (4). Grupo mapa "Mapas por fase" = pills [8 combinações fase×abs/taxa] (8) |
| 🥗 SISVAN | 3 line charts soltos | Grupo gráfico = pills [Baixo peso, Sobrepeso, Obesidade] (3) |
| 💉 Cobertura vacinal (EPI) | 1 line (11 séries) + 1 grouped-bar, soltos | Grupo gráfico = pills [Série temporal por imunobiológico, Comparativo por ano] (2) — tipos de gráfico diferentes por opção, o mecanismo já suporta isso |
| 🎓 Educação | 4 grouped-bar (SIDRA) + 1 bar (PNAD) + 1 line (matrículas) | Grupo gráfico "SIDRA frequência/taxa" = pills [Freq. 0-5 raça, Freq. 0-5 sexo, Taxa 0-6 raça, Taxa 0-6 sexo] (4). PNAD e Matrículas ficam soltos — indicadores/fontes diferentes entre si, não um corte do mesmo dado (mesmo critério do item "Comparação entre faixas" acima) |

**Efeito líquido esperado**: as ~14 subseções `h3`/`h4`/`h5`/`h6` hoje usadas
só para separar cortes correlatos (ex. os 4 `h5` de "Por CAP e faixa etária"
já removidos numa rodada anterior) somem, substituídas por pills dentro de
menos grupos maiores — cada `h2` passa a ter uma forma mais previsível
(achados + intro + 1-2 grupos de gráfico + 1 grupo de mapa) em vez de um
número variável de subseções soltas. Título/legenda por opção dentro de um
grupo continuam carregando a informação que os `h5`/`h6` davam (ex. pill
"Menores de 1 ano · Imunização" already carrega os dois níveis que antes
eram `h5`+`h6`).

**Fora desta proposta, por decisão explícita já registrada**: a galeria de
8 mapas do CAP evitável por grupo/subgrupo (§3.2) — mantida como pills
agora (ver tabela acima, linha "Óbitos por causas evitáveis"), revertendo a
decisão anterior de deixá-la como grade solta, já que o objetivo desta
rodada (seções mais curtas) pesa mais que a preocupação original
(comparação lado a lado) — se comparação lado a lado for importante depois,
cabe reavaliar.
