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
   `SPEC-visual-identity/specs.md` §4 decisão A — refinado nesta rodada só no
   que diz respeito a **deploy** (§5.1), não à arquitetura do arquivo.
3. Reorganizar o espaço da página para dar lugar de verdade à análise
   textual (hoje o HTML é "só visualização" por decisão de
   `SPEC-visual-identity` §2 — isso é revisto aqui, ver §3.4).
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

### 3.3 Outliers — pré-computados nas duas versões

O gerador (`build_html_report.py`) calcula, para cada série numérica, a
versão com e sem outliers e embute as duas como JSON. O toggle no cliente só
troca qual array o gráfico/mapa lê — sem lógica estatística em JS.

- **Regra de outlier proposta** (default se não houver objeção): cercas de
  Tukey, `[Q1 - 1.5×IQR, Q3 + 1.5×IQR]`, calculada por série/corte
  individualmente (não globalmente por seção). Mesma regra para gráficos de
  barra/linha e para os valores por bairro/CAP nos mapas.
- Pontos removidos ficam ocultos (não substituídos por interpolação) — a
  série "sem outliers" tem menos pontos, não pontos alterados.

### 3.4 Espaço para análise textual — reversão parcial da decisão B de `SPEC-visual-identity`

`SPEC-visual-identity/specs.md` §4 decisão B removeu a prosa/notas de método
do HTML, deixando "só visualização" (título + fonte). Esta rodada reintroduz
espaço textual, mas **redefinido**, não como retorno ao texto integral do
notebook:

- Bloco "Principais achados" por seção (`h2`) — lista curta, editorial, não
  o texto de método completo do notebook.
- Bloco "Análise" por chart-card — texto curto (2–3 frases) abaixo do
  gráfico, ou ao lado do mapa (ver wireframe, segundo exemplo da seção).
  Fica fixo por chart-card, não muda quando a opção do seletor muda (a menos
  que o texto seja escrito por opção — decisão de conteúdo, não deste spec).
- O texto de método completo continua vivendo só no notebook/PDF — este spec
  não reverte isso, só adiciona os dois blocos curtos acima.

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
   `SPEC-visual-identity/specs.md` §3.1 (`Teal` natalidade, `RdPu`/`PuRd`
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
  `SPEC-visual-identity/specs.md` §3.3, mais de 6 linhas → só as N mais
  relevantes coloridas, resto agrupado em "Outras (N)"), a marcação
  máx/mín/recente vale para as séries coloridas em destaque, não para o
  agregado cinza "Outras".
- Ao trocar a opção ativa no seletor (§3.2), os três rótulos recalculam
  para a série/corte recém-selecionado.
- Não se aplica a `barChart`/`groupedBarChart` (não são séries temporais)
  nem aos mapas (não há "mais recente" num corte espacial de um só ano) —
  só a `lineChart`.

## 4. Tabela de decisões (formato igual a `SPEC-visual-identity/specs.md` §4)

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

## 5. Stack técnica

Mantém a regra de arquitetura já estabelecida em
`SPEC-visual-identity/specs.md` (arquivo HTML único, sem passo de build, sem
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

- **Main** — navbar persistente aberta, cabeçalho do relatório, uma seção
  `h2` completa expandida (⛓️ Óbitos por causas evitáveis, usada como
  exemplo por ser o caso mais extremo de repetição hoje) mostrando bloco de
  achados, texto de análise, chart-card de gráfico (seletor de categorias
  CID-10 + toggle de outliers + download) e chart-card de mapa (seletor de
  CAP + toggle de outliers + download + painel de análise lateral), e a
  seção seguinte mostrada recolhida para dar o ritmo da página.
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
