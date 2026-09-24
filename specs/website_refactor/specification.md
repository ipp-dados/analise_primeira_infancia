# Especificação: website_refactor

Pedido original: `prompt_html_review.md` (nesta pasta). Rodada aberta em 2026-09-24, branch
`spec/website-refactor`. **Rascunho 2, decisões D1-D4 aprovadas e D5 (redução de tamanho) pedida pelo usuário (2026-09-24); nada é
implementado antes do ok neste documento e em `plan.md`.**

## 1. Objetivo

Separar o site HTML do pipeline do PDF e reorganizá-lo como um site estático modular em `website/`,
publicável no GitHub Pages, com nova navegação (abas por eixo, barra fixa, sumário lateral com
progresso) e visual mais suave. O PDF não muda nesta rodada.

## 2. Estado atual (levantamento, 2026-09-24)

- **Gerador**: `.claude/skills/export_pdf_report/scripts/build_html_report.py` (2.625 linhas) escreve
  um único `relatorio/index.html` (20,9 MB) com tudo embutido: CSS (~430 linhas, string `CSS`), motor JS
  (~400 linhas, string `ENGINE`), chamadas de render com os dados (0,11 MB), logo IPP e fundo cartográfico
  em base64 (0,13 MB).
- **Peso**: 96% do arquivo (20,1 MB) são `<path>` de mapa — 7.171 tags, porque a geometria de cada nível
  (166 bairros, AP, RP, RA, CAP) é repetida em cada mapa e em cada variante "sem outliers". Registrado
  como pendência desde a v6.1 (`relatorio/specs.md`, `specs/roadmap.md`).
- **Estrutura da página**: faixa "EM DESENVOLVIMENTO" → barra de acento → navbar hambúrguer (links h2)
  → cabeçalho (título, descrição, data, barra de espectro) → Sumário (h2 > h3) → Introdução → 6 seções
  `.rsec` retráteis (cada uma abre com "Principais achados") → rodapé institucional.

| Eixo (h2) | h3 | cartões `.out` | mapas | pendentes | MB |
|---|---|---|---|---|---|
| 🎯 Prioridade (sem secundário) | 10 | 246 | 35 | 1 | 13,4 |
| 🤝 Inclusão | 9 | 44 | 4 | 3 | 1,2 |
| 👨‍👩‍👧 Família e Cuidados | 6 | 52 | 2 | 0 | 0,6 |
| 🛡️ Proteção | 5 | 76 | 20 | 1 | 4,6 |
| 🍽️ Alimentação | 3 | 33 | 3 | 0 | 0,9 |
| 🏠 Moradia | 3 | 0 | 1 | 3 | 0,2 |

  (Contagens incluem as variantes de pill e de outlier, por isso são maiores que o número de indicadores.)

- **Motor de gráficos**: SVG com `viewBox` fixo; `getBoundingClientRect` só no hover (tooltip). Renderizar
  dentro de um painel `hidden` já funciona (os painéis de pill fazem isso hoje) — as abas não exigem
  mudar o motor.
- **Acoplamentos com outros scripts**: `sincroniza_docx.py` roda o gerador via subprocess com destino
  `relatorio/index.html`; `build_notebook_report.py` e `gera_docx_curadoria.py` só *citam* o gerador em
  comentários e copiam `_lorem`/`slugify`, sem importá-lo. Os três leem `relatorio/textos_curados.json`.
  O gerador importa `avisa_itens_sem_arquivo` de `gera_estrutura_eixos.py`.
- **Deploy**: `.github/workflows/deploy-relatorio.yml` (manual) copia só `relatorio/index.html` para
  `_site/`. O CI não tem `tabelas_finais/` (gitignorado), então **não pode rodar o gerador** — a saída
  gerada precisa continuar versionada.

## 3. Decisões (aprovadas em 2026-09-24)

- **D1 — Local do gerador**: move para `website/build/build_site.py` e escreve em `website/`.
  `relatorio/index.html` deixa de ser gerado e sai do git (e sai também a exceção `!/relatorio/index.html`
  do `.gitignore`). O workflow de deploy e `sincroniza_docx.py` passam a apontar para `website/`. A skill
  `export_pdf_report` fica só com PDF e DOCX.
- **D2 — Peso dos mapas**: a geometria de cada nível é escrita **uma vez**, em arquivo compartilhado
  (`website/data/geo.js`), e cada mapa guarda só o que muda por indicador. Deve continuar abrindo em
  `file://` (sem `fetch`). Ver §4.6 para o mecanismo.
- **D3 — Abas**: "Visão geral" (Introdução + visão dos eixos) + 6 abas de eixo. Aba ativa na URL.
- **D4 — Visual**: restyle da interface (cantos arredondados, sombras suaves, cores de UI mais suaves,
  ícones SVG). Mantém Fraunces (títulos) e IBM Plex (corpo/mono), os acentos institucionais navy/ciano,
  a paleta de dados (11 cores) e os `cmap` dos mapas.
- **D5 — Redução de tamanho** (pedido do usuário, 2026-09-24): orçamento explícito para os arquivos do
  site, com técnicas além de D2 — ver §4.9.
- **D6 — Ajustes pedidos na revisão do protótipo** (Bloco 4, 2026-09-24; protótipo aprovado com ajustes):
  - **Conclusões por eixo**: bloco de 100-200 palavras (lorem até haver texto curado) no fim de cada
    painel de eixo, antes da caixa de fontes; não na Visão geral. Visualmente distinto (cartão azul
    institucional escuro com faixa ciano), com h3 "Conclusões" que entra no sumário lateral. Seed
    `conclusao-<sid>` em `relatorio/textos_curados.json`; o DOCX de curadoria ainda não tem bookmark
    para ele (fora do escopo: `gera_docx_curadoria.py` não muda nesta rodada).
  - **Banner sem a descrição**: no lugar, links para o repositório no GitHub, para o relatório final em
    PDF e a data de atualização. O PDF (~48 MB) não é publicado no Pages; o link aponta para o arquivo
    versionado no GitHub (`blob/staging_main/relatorio/analise_primeira_infancia.pdf`).
  - **Logo em resolução maior**: não existe SVG oficial publicado (o site do IPP usa um PNG de 212×77;
    o nosso original tem 1723×310). O borrado vinha da redução de 14× no navegador. Solução: logo
    exibido maior (40 px no banner, 32 px no rodapé) com cópias reduzidas em Lanczos para 1×/2×/3×
    (`srcset`), geradas pelo build a partir do original. Vetorizar o brasão por conta própria foi
    descartado (publicaria uma marca oficial alterada); se a Ascom do IPP fornecer o SVG, ele substitui.
  - **Página "Fale Conosco"** na barra de navegação: registrada em `website/ROADMAP.md` e
    `specs/roadmap.md` (fora desta rodada).
  - **Título**: "Diagnóstico da Primeira Infância Carioca", sempre em 2 linhas
    ("Diagnóstico da" / "Primeira Infância Carioca"); `<title>` na mesma forma em 1 linha.

## 4. Requisitos

### 4.1 Estrutura de diretórios

```
website/
├── index.html              # GERADO — conteúdo (markup), linka css/js/data
├── css/
│   ├── main.css            # tokens (cores, raios, sombras, espaçamento), reset, tipografia
│   ├── layout.css          # grade da página, faixa fixa, coluna lateral
│   └── components.css      # banner, abas, cartões, callouts, pills, gráficos, mapas, rodapé
├── js/
│   ├── charts.js           # motor atual (lineChart/barChart/groupedBarChart, pills, outliers, CSV, tooltips)
│   ├── navigation.js       # troca de aba, estado na URL, faixa fixa
│   └── sidebar.js          # sumário lateral, scroll-spy, progresso
├── data/                   # GERADO
│   ├── charts-<eixo>.js    # chamadas de render + dados, 1 por aba (antes RENDER_CALLS inline; §4.9)
│   └── geo.js              # geometria compartilhada dos mapas (D2)
├── assets/
│   ├── icons/              # SVG (fonte; o gerador os embute inline)
│   └── images/             # ipp-logo.png, basemap-*.jpg (GERADO)
├── build/                  # NÃO publicado
│   └── build_site.py       # gerador (ex-build_html_report.py)
├── 404.html                # página de erro estática (§4.10)
├── .nojekyll               # vazio; desliga o Jekyll se o modo de deploy mudar (§4.10)
├── README.md               # como gerar, o que é gerado vs. editado à mão
└── ROADMAP.md              # pendências da versão mobile (fase 4)
```

- Arquivos em `css/`, `js/` (exceto `data/`) e `assets/icons/` são **editados à mão** — deixam de ser
  strings Python. `index.html`, `data/*` e `assets/images/basemap-*.jpg` são **gerados** (constitution §4:
  editar o gerador, não o gerado).
- `charts.js` é um quarto arquivo JS além dos dois do prompt: o motor de gráficos precisa de um lugar
  próprio e não é navegação nem sidebar.
- Todos os caminhos são relativos (`css/main.css`, não `/css/main.css`) — funciona no subcaminho do
  GitHub Pages (`<usuario>.github.io/<repo>/`) e em `file://`.

### 4.2 Cabeçalho (banner)

- Conteúdo: logo IPP, título ("Análise Primeira Infância Carioca"), descrição curta, data de atualização.
  O ícone 🏛️ do título sai (o logo cumpre esse papel).
- Rola normalmente com a página (não é fixo). A faixa "EM DESENVOLVIMENTO" continua acima do banner
  enquanto `publicar_teste_pages` não for encerrado (`specs/roadmap.md`).
- A barra de espectro (11 cores de dados) pode ficar como detalhe decorativo do banner.

### 4.3 Barra de abas (fixa)

- Logo abaixo do banner, `position: sticky; top: 0`. Altura exposta como variável CSS (`--nav-h`) para
  o scroll-spy e o `scroll-margin-top` dos títulos.
- 7 botões: Visão geral + 6 eixos, cada um com ícone SVG + nome. Semântica ARIA de abas (`role="tablist"`,
  `tab`, `tabpanel`, `aria-selected`, setas ←/→ entre abas).
- Clicar troca o painel ativo sem recarregar (painéis inativos com `hidden`) e rola para o topo do
  painel (logo abaixo da barra).
- **URL**: `#<eixo>` ativa a aba (ex. `#inclusao`); `#<eixo>/<id-h3>` ativa e rola até a subseção.
  Voltar/avançar do navegador funciona (`hashchange`). Âncora antiga `#<id-h3>` (links já compartilhados)
  é resolvida para a aba que contém o h3. Sem hash → Visão geral.
- Substitui a navbar hambúrguer e o Sumário (v6/v7). O toggle recolher/expandir das seções sai — cada aba
  já mostra uma seção só.

### 4.4 Conteúdo e cartões

- Painel de eixo: eyebrow "EIXO N DE 6" + título h2 → "Principais achados" → h3s e cartões como hoje →
  **caixa de fontes** (§4.5).
- Cartões com `border-radius` e sombra suave em vez da borda preta de 2px (reverte v6.1; ver §6).
- Comportamento de gráfico/mapa inalterado: pills, outliers, CSV, tooltip, rótulos de extremo, texto de
  análise por opção.
- Painel "Visão geral": Introdução (texto atual, curado ou lorem) + 6 cartões de eixo (ícone, nome,
  número de subseções e de indicadores pendentes, link para a aba). Números calculados pelo gerador a
  partir do que ele emite — nenhum texto novo inventado.

### 4.5 Caixa de fontes por seção

- Ao fim de cada painel de eixo, callout "FONTES DESTA SEÇÃO" no mesmo estilo de "Principais achados".
- Conteúdo: lista **deduplicada** das strings de fonte realmente usadas pelos cartões daquele eixo
  (`fonte`/`fonte_dados` passados a `_out_div`, `mapa_svg`, `plain_table`), na ordem em que aparecem.
  Coletada pelo gerador, não escrita à mão.
- Fontes quase iguais (ex. mesma base com nota diferente) aparecem separadas nesta rodada; unificar
  exigiria editar as constantes `FONTE_*`, o que fica para uma revisão de conteúdo.

### 4.6 Mapas (D2)

- `data/geo.js` define, uma vez por nível (`bairro`, `ap`, `rp`, `ra`, `cap`), um `<path id="geo-<nivel>-<chave>">`
  dentro de um `<svg>` oculto de `<defs>`, injetado no carregamento.
- Cada mapa passa a ter `<use href="#geo-<nivel>-<chave>" fill="…" data-label="…" data-valor="…">` por
  região. Cores, legenda, tooltip, rosa dos ventos, escala e outliers continuam calculados em Python pela
  mesma lógica de `mapa_svg` — muda só onde a geometria mora.
- Por que `<use>` e não desenhar em JS: mantém toda a lógica de cor em Python (sem reescrever
  `_cor_sequencial`/bins/teto em JS) e deixa a saída visualmente idêntica. É um refinamento da opção
  aprovada em D2 (mesmo resultado: geometria única, abre em `file://`).
- O fundo cartográfico sai do base64 embutido para `assets/images/basemap-<bbox>.jpg`, referenciado por CSS.
- Metas de tamanho: ver §4.9.

### 4.7 Sumário lateral com progresso

- Coluna à direita do conteúdo, `position: sticky; top: var(--nav-h)`.
- Mostra os h3 da aba ativa (Visão geral: os 6 eixos). Item ativo = h3 visível mais alto
  (`IntersectionObserver`, com margem para a barra fixa). Clique rola suavemente até o h3 e atualiza a URL
  (`#<eixo>/<id-h3>`).
- Barra de progresso = fração rolada do painel ativo (0% no topo do painel, 100% no fim da caixa de fontes).
- Troca de conteúdo junto com a aba.

### 4.8 Layout e visual

- Container de até ~1440px: grade `minmax(0, 1fr) 280px` (conteúdo + sumário). Os gráficos escalam pelo
  `viewBox`; conferir que nenhum fica ilegível com a coluna de conteúdo mais estreita que os 1200px atuais.
- Tokens novos em `main.css`: `--radius-sm/md/lg`, `--shadow-1/2`, escala de espaçamento, superfícies de UI
  mais suaves. `--c1..--c11` (dados) e cores dos mapas não mudam.
- Ícones: conjunto Lucide (licença ISC), um por eixo + Visão geral + pendente (substitui 🚧) + nota
  metodológica (substitui ℹ️) + fontes. Emojis saem dos títulos h2.
- Contraste de texto AA (4,5:1) nos tokens novos.
- CSS com Grid/Flexbox e variáveis, sem regras mobile nesta rodada — só não impedir a próxima.

### 4.9 Redução de tamanho dos arquivos (pedido do usuário, 2026-09-24)

Requisito próprio, além da deduplicação de D2. Medido sobre o `relatorio/index.html` atual:

| Contribuinte | Hoje | Depois de D2 | Técnica adicional | Meta |
|---|---|---|---|---|
| Geometria dos mapas | 20,1 MB (7.107 paths) | 1,35 MB (218 paths únicos, 1 casa decimal) | Simplificação Douglas-Peucker (`shapely.simplify`, tolerância ~0,3 px do SVG, `preserve_topology=True`) + comandos relativos (`l dx,dy`) | ≤ 0,5 MB |
| Atributos por região (`fill`, `stroke`, `data-label`) | 0,83 MB | ~0,6 MB | `stroke`/`stroke-width` na classe CSS; nome da região mora uma vez em `geo.js` (JS busca pelo `href`), o `<use>` só guarda `fill` + `data-valor` | ≤ 0,3 MB |
| Variantes "sem outliers" (painel duplicado inteiro) | 6,4 MB | ~0,5 MB | Mapas: a variante guarda só a lista de `fill` alternativos, aplicada pelo toggle; gráficos continuam pré-renderizados (pequenos) | ≤ 0,15 MB |
| Fundo cartográfico | 0,13 MB (base64) | 0,10 MB (`.jpg`) | JPEG qualidade ~70, largura máxima = largura exibida × 2 | ≤ 0,1 MB |
| Dados dos gráficos (`data/charts.js`) | 0,11 MB | igual | Números com no máximo 4 algarismos significativos quando a fonte já é arredondada; um arquivo por aba (`data/charts-<eixo>.js`), carregado por `<script>` injetado na primeira ativação (funciona em `file://`) | ≤ 0,15 MB no total, ≤ 50 KB na carga inicial |
| CSS/JS escritos à mão | ~0,03 MB | igual | Sem minificação (continuam legíveis, sem etapa de build) — o gzip do Pages resolve | — |

- **Orçamento**: `index.html` ≤ 1 MB; todo o `website/` publicado ≤ 2 MB sem compressão (hoje 20,9 MB, redução
  ≥ 90%). Medir também o tamanho com gzip (o GitHub Pages comprime HTML/CSS/JS na entrega).
- **Sem perda visível**: a simplificação não pode abrir frestas entre bairros vizinhos nem sumir com
  polígonos pequenos (ilhas, Paquetá). Validar por comparação de captura em 1440px e em zoom 200% dos cinco níveis.
- **Carga por aba**: só os dados da aba aberta (e da Visão geral) entram na carga inicial; as outras
  abas carregam na primeira vez que forem abertas. A geometria (`geo.js`) carrega uma vez, porque é
  compartilhada.
- **Guarda contra regressão**: o gerador imprime o tamanho de cada arquivo gerado e **avisa** (não falha)
  se o orçamento for ultrapassado.
- Escopo: só os arquivos do site. PDF (46 MB) e DOCX (5,9 MB) ficam fora (cerca do prompt, §4.11).

**Resultado medido (Blocos 3/3b, 2026-09-24)** — site publicado **1.330.860 bytes** (gzip 310.059), contra
20,9 MB: **−93,6%**. `index.html` 866.816 bytes, `data/geo.js` 248.221, `data/charts.js` 109.451, CSS+JS
45.111, basemap 23.524, logo 37.737. Orçamento total (≤ 1 MB / ≤ 2 MB) cumprido.

Decisões tomadas com os números na mão (a tabela acima era estimativa):
- **Simplificação**: `coverage_simplify` com tolerância 0,3 (não Douglas-Peucker por polígono, que abriria
  frestas entre vizinhos — a camada de bairros nem é uma cobertura perfeita). 1,44 → 0,24 MB, 0 anéis
  perdidos, área −0,01%. Ids curtos (`#gb12`) em vez de `#geo-bairro-12`.
- **Outliers dos mapas como fills alternativos: não feito.** As variantes "sem outliers" custam 0,21 MB
  (≈ 30 KB com gzip) depois da deduplicação; reescrever o toggle, que funciona, para economizar isso não
  compensa o risco.
- **Dados por aba com carregamento tardio: não feito.** Todos os dados de gráfico somam 109 KB (17 KB com
  gzip); o carregamento tardio traria o risco R1c (rolagem antes do script da aba chegar) por quase nada.
  Se os dados crescerem muito, o gerador avisa pelo orçamento e a ideia volta.
- Atributos por região ficaram em 0,44 MB (acima da estimativa de 0,3), dentro do orçamento total.
- **Basemap**: arquivo nomeado pela bbox e reaproveitado se já existir — a saída ficou determinística
  (antes o JPEG mudava a cada download) e a geração roda sem rede.

### 4.10 Formato final: site estático compatível com GitHub Pages (requisito, 2026-09-24)

O GitHub Pages só serve arquivos; não roda código no servidor nem reescreve rotas. O que é publicado
tem que cumprir tudo abaixo:

- **Só arquivos estáticos publicados**: `.html`, `.css`, `.js`, `.svg`, `.png`, `.jpg`. Nenhum `.py`, nenhum
  endpoint, nenhuma variável de ambiente, nenhum banco. O gerador Python roda **só na máquina de dev**; a
  saída é versionada e o workflow apenas copia (o CI não tem `tabelas_finais/` para gerar nada).
- **Sem etapa de build no deploy**: nem Jekyll, nem bundler, nem npm. O workflow usa
  `upload-pages-artifact` + `deploy-pages` (não passa pelo Jekyll); mesmo assim `website/.nojekyll` é
  publicado, para o caso de alguém trocar para deploy "a partir de branch" (o Jekyll ignoraria pastas com `_`).
- **Rotas só por hash** (`#inclusao`, `#inclusao/<h3>`), nunca por caminho (`/inclusao`): o Pages não tem
  fallback para uma SPA, e um caminho inexistente dá 404.
- **Caminhos relativos e com a mesma caixa (maiúsculas/minúsculas)**: o site roda no subcaminho `/<repo>/`,
  então nada de `/css/...` absoluto. O Pages diferencia maiúsculas de minúsculas e o Windows não — um
  `Logo.png` vs `logo.png` passa local e quebra publicado. Convenção: todo nome de arquivo em minúsculas,
  sem espaço nem acento.
- **Dependências externas só via HTTPS**, só as que já existem (Google Fonts). Nada de CDN novo.
- **Sem `fetch`/XHR para arquivos locais** — tudo por `<script src>`/`<link>`/`<img>`, que funciona
  igual no Pages e em `file://`.
- **Limites**: arquivo < 100 MB (limite do git), site < 1 GB, e o orçamento de §4.9 bem abaixo disso.
- **Entrada**: `index.html` na raiz do artefato publicado; `404.html` simples, com link de volta para
  `index.html` (o Pages usa esse arquivo automaticamente).

### 4.11 Fora de escopo

- PDF: `build_notebook_report.py` e o layout do PDF não mudam. `gera_docx_curadoria.py` também não.
- Layout mobile (vai para `website/ROADMAP.md`).
- Conteúdo: textos de análise, "Principais achados" e Introdução continuam como estão (lorem ou curado).
- Agrupamento por eixo: o gerador continua com o agrupamento fixo em código (não passa a ler
  `specs/estrutura_eixos.md` em tempo de execução — decisão de `specs/ajuste_eixos` §9.3 mantida).
- Tema escuro (removido na v6.2, continua fora).

## 5. Riscos

- **R1 — Mudança no motor dos mapas (D2)**: um `<use>` herda `fill` mas o hover/tooltip precisam
  continuar funcionando (evento chega no `<use>`, não no `<path>` do `<defs>`). Validar hover, tooltip,
  toggle de outliers e CSV em mapas dos 5 níveis.
- **R1b — Simplificação de geometria (§4.9)**: tolerância alta demais abre frestas entre vizinhos ou
  apaga ilhas. Simplificar a camada **dissolvida por nível** com `preserve_topology=True` e conferir pela
  captura em zoom; se aparecer fresta, baixar a tolerância antes de aceitar.
- **R1c — Dados carregados por aba**: um link direto para `#<eixo>/<h3>` tem que esperar o script da aba
  carregar antes de rolar (a rolagem roda no `onload` do script).
- **R2 — Safari**: não há Safari nesta máquina (Windows). Proxy: WebKit do Playwright. Registrar em
  `validation.md` que Safari real não foi testado.
- **R3 — Links antigos**: a URL publicada hoje é a raiz do Pages; ela continua a mesma (o site novo é
  publicado na raiz). Âncoras antigas de h3 são resolvidas (§4.3).
- **R4 — Documentação espalhada**: CLAUDE.md, `specs/tech-stack.md`, `specs/roadmap.md`, `relatorio/specs.md`,
  SKILL.md de `export_pdf_report`, README e comentários do próprio gerador citam `relatorio/index.html` e
  `build_html_report.py`. Atualizar todos no último bloco; registros históricos em specs antigas não são
  reescritos (constitution §5).

## 6. Decisões anteriores revertidas (registrar como v8 em `relatorio/specs.md`)

| Antes | Onde foi decidido | Agora |
|---|---|---|
| Cartões brutalistas (borda 2px preta, sem raio) | v6/v6.1 | Cantos arredondados + sombra |
| Navbar hambúrguer com links h2 | v6 | Barra de abas fixa |
| Sumário no topo (h2 > h3) | v7 | Sumário lateral da aba ativa |
| Seções retráteis | v6 | Abas (uma seção por vez) |
| Emojis nos títulos de seção | v2 | Ícones SVG |
| Um arquivo HTML autocontido | v5 | Site estático com arquivos separados |
| `relatorio/index.html` versionado e publicado | v5.1 | `website/` versionado e publicado |

## 7. Pendências

- **P1**: Criar uma skill própria (`.claude/skills/build_website/`) com o passo a passo de geração, ou
  deixar só em `website/README.md`? Proposta: skill fina que aponta para o README. A confirmar no Bloco 7.
- **P2**: Autorização do logo IPP e placeholders do rodapé continuam pendentes (`specs/relatorio-interativo`
  T0.4/T6.2) — não bloqueiam esta rodada.
