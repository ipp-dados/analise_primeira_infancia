# SPEC — Relatório final em LaTeX (`specs/relatorio_latex`)

> Rodada aberta em 2026-09-25 (branch `planning`). Item "Setup LaTeX final report" / "Convert the PDF
> export pipeline to LaTeX" de `specs/roadmap.md` (seção *Other*). Status: **decisões D1-D4 tomadas em 2026-09-25 (§8) — pronta para o Bloco 1.**

## 1. Contexto

O PDF atual (`relatorio/analise_primeira_infancia.pdf`, 137 páginas, 49 MB) sai de
`.claude/skills/export_pdf_report/scripts/build_notebook_report.py` → HTML → Edge headless. Limitações:

- não é um documento: sem capa, folha de rosto, resumo, sumário paginado, listas de ilustrações/tabelas,
  numeração de figuras nem referências; o eixo é um `<h2>`, não um capítulo;
- agrupamento **hardcoded** em Python — não lê `specs/estrutura_eixos.md` (caveat documentado na
  `SKILL.md` do `export_pdf_report`); mover um indicador exige editar código;
- imagens em resolução de tela (mapas a 300 dpi, 31 cm de largura) → PDF pesado e fontes internas
  reduzidas a ~55-65% quando cabem na largura do A4.

Pedido do usuário (2026-09-25):

- cada eixo vira um **capítulo**; **Introdução** em capítulo próprio;
- **capa, resumo e sumário**;
- tabelas **majoritariamente no apêndice**;
- fonte em **LaTeX**, organizada em `relatorio/`, consistente com o site (`website/`) e com
  `relatorio/textos_curados.json`, **atualizável com texto curado novo** como o PDF atual;
- **pt-BR e normas ABNT**; relatório técnico / análise de política pública, não dissertação;
- mapas e gráficos **cabendo no A4**; uso **esparso** de cor e iconografia, tirado do site;
- "Referências" renomeada para **Fontes**, com as fontes de dados;
- uma **tabela de fontes × visualizações/mapas/tabelas** para conferência (fora do relatório).

## 2. Normas de referência

| Norma | Uso aqui |
| :--- | :--- |
| ABNT NBR 10719:2015 (relatório técnico e/ou científico) | Estrutura geral: folha de rosto obrigatória, resumo, sumário, textuais, referências, apêndices |
| NBR 14724 (formatação, por analogia) | A4, margens 3 cm (sup./esq.) e 2 cm (inf./dir.), corpo 12 pt, entrelinha 1,5, citações/notas/legendas menores |
| NBR 6027 (sumário) | Sumário com indicativo numérico, gerado pelo LaTeX |
| NBR 6028 (resumo) | Resumo em parágrafo único, 150-500 palavras, seguido de palavras-chave |
| NBR 6024 (numeração progressiva) | Capítulo = seção primária (1, 2 …), subseção de indicador = secundária (2.1 …) |
| NBR 6023 (referências) | Lista **Fontes** (bases de dados, com órgão, título, URL, data de acesso) |
| NBR 10520 (citações) | Citação autor-data no texto quando o texto curado citar uma fonte (`abntex2cite`, `alf`) |
| IBGE, Normas de apresentação tabular | Tabelas abertas nas laterais, título acima, Fonte abaixo |
| NBR 14724 §5.8 (ilustrações) | Identificação acima ("Gráfico 3 – …", "Mapa 2 – …"), Fonte abaixo; listas separadas de gráficos e de mapas |

Implementação: classe `abntex2` (já instalada no MiKTeX), modelo de relatório técnico, `xelatex` via
`latexmk`.

## 3. Estrutura do documento

**Pré-textuais**
1. Capa — título, Prefeitura/IPP, local e ano; faixa de 11 cores (`spectrum-bar` do site) e azul
   institucional; logo só se o uso estiver autorizado (pendência já registrada no roadmap).
2. Folha de rosto (obrigatória na NBR 10719) — órgão, título, responsáveis, local, ano.
3. Resumo + palavras-chave (texto curado novo, chave `resumo`).
4. Lista de gráficos, Lista de mapas, Lista de tabelas (automáticas).
5. Lista de abreviaturas e siglas (IBGE, SIM, SINASC, Sinan, SISVAN, CadÚnico, AP, CAP, RA, RP, IPS…).
6. Sumário.

**Textuais**
- **1 Introdução** — texto curado `introducao` (já existe, 421 palavras) + seções curtas fixas: os seis
  eixos da política, como ler o relatório, notas sobre população de referência (Ripsa × Censo 2022) e
  supressão de células pequenas do CadÚnico. Notas escritas em linguagem não técnica (constituição §1).
- **2-7 Um capítulo por eixo**, na ordem de `specs/estrutura_eixos.md`:
  - abertura do capítulo: ícone do eixo, "Eixo N", título; texto de abertura (chave nova
    `abertura-<eixo>`); caixa "Principais achados" (chave nova `achados-<eixo>`, mesma do site);
  - uma **seção** por `###` do `.md`: texto curado + gráficos e mapas da subseção, com legenda ABNT e
    remissão à tabela do apêndice ("ver Tabela A.3");
  - indicador `status: pendente` → caixa discreta "Indicador em desenvolvimento" com a `nota` (nunca
    some em silêncio, constituição/`SKILL.md`);
  - seção final "Síntese do eixo" (chave `conclusao-<sid>`, a mesma que o site já lê).
- **8 Considerações finais** — exigida pela NBR 10719 (chave nova `consideracoes_finais`).

**Pós-textuais**
- **Fontes** (no lugar de "Referências") — NBR 6023, uma entrada por base de dados, vinda de
  `relatorio/latex/fontes.bib`.
- **Apêndices A-F** — "APÊNDICE A – Tabelas do eixo Prioridade" etc.; tabelas numeradas (Tabela A.1…),
  em `longtable` quando passam de uma página, paisagem só quando não cabem em retrato.
- Tabelas pequenas (≤ ~8 linhas) que sustentam diretamente o texto podem ficar no corpo — exceção,
  marcada em `estrutura_eixos.md` com uma chave nova (`tabela_no_texto:`), para não virar regra de código.

## 4. Identidade visual (esparsa, tirada do site)

- **Cor**: texto em preto; azul institucional `--ipp-navy #004a80` só em títulos de capítulo, fios
  e caixas; faixa de 11 cores `--c1…--c11` só na capa e na abertura de capítulo. Nenhuma cor nova nos
  dados — gráficos e mapas mantêm a identidade do notebook (decisão já registrada: o PDF segue
  `analise.py`, não o site).
- **Ícones**: os mesmos SVG (Lucide) de `website/assets/icons/`, convertidos para PDF no build —
  eixos (`target`, `handshake`, `users`, `shield-check`, `apple`, `house`), achados (`lightbulb`),
  síntese (`flag`), pendente (`construction`), nota (`info`), fontes (`book-open`). Só nesses lugares.
- **Tipografia**: títulos em Fraunces (a do site; OFL, arquivo versionado em `relatorio/latex/fontes/`),
  corpo em IBM Plex Sans 12 pt (a do site; `plex-otf` já no MiKTeX). Revisável depois das páginas-amostra.
- **Página**: A4 retrato, ABNT, `oneside` (leitura em tela; sem páginas em branco), cabeçalho com o
  título do capítulo, número de página no canto superior direito (abnTeX2).

## 5. Figuras cabendo no A4

Largura útil do A4 com margens ABNT: 16 cm. Metas: gráfico 16 × 8-9 cm, mapa 16 × 11-12 cm, dois por
página quando couber; texto dentro da imagem ≥ 7 pt **no tamanho impresso**. As PNGs atuais têm
título e fonte na própria imagem, o que duplica a legenda ABNT, e o texto delas encolhe para ~55-65%
na largura do A4. Ver decisão D1 (§8).

Independentemente de D1: o build gera um **cache de imagens reduzidas** (gitignorado) na resolução
de impressão (300 dpi na largura final) para o PDF ficar abaixo de ~20 MB (hoje 49 MB).

### 5.1 Desenho das figuras para impressão (pedido do usuário, 2026-09-25)

> "Think about the figures visual design in a printed format and improve readability […] we need more
> clear labels, as we don't have interactivity."

Protótipo aprovado para discussão: `specs/relatorio_latex/prototipo/comparacao_antes_depois.pdf` (antes ×
depois na mesma página A4 com legenda ABNT; scripts ao lado). Diagnóstico das 71 PNGs e 41 mapas atuais,
lidos numa folha de contato:

| Problema na versão de tela | Regra da variante de impressão |
| :--- | :--- |
| Texto encolhe para 50-65% (mapa: legenda ~5 pt, rodapé ~3 pt) | Figura desenhada **no tamanho final** (16 cm de largura; gráfico 5-7 cm de altura, mapa ~9 cm, pequenos múltiplos ~8,5 cm); texto 7-8 pt reais |
| Título e fonte dentro da imagem, duplicando a legenda ABNT | Sem título nem fonte na imagem: título → `\caption` ("Gráfico N –"), fonte e notas → `\fonte{}` abaixo, a partir do manifesto |
| Rótulo de eixo = nome de coluna (`taxa_mortalidade_precoce`, `Valores`, `Total`, `óbitos-gravidez`) | Rótulo por extenso **com unidade**, na horizontal acima do eixo ("Óbitos de 0 a 6 dias por mil nascidos vivos") — um dicionário central `ROTULOS_EIXO` nos helpers, com `ylabel` explícito prevalecendo |
| Número em inglês (`140000`, `7.25`), idade como `0.0` | pt-BR em eixo e rótulo (`140.000`, `7,3`); ano e idade sempre inteiros |
| Sem valores legíveis sem tooltip | **Rótulos diretos seletivos**: série única → primeiro, mínimo/máximo e último valor ("6,4 em 2025"); várias séries → nome + último valor na ponta de cada linha (a legenda continua, abaixo do gráfico); barras → valor (e %, quando parte de um todo) na ponta. Nunca um número em cada ponto |
| Barras de uma só série pintadas com uma cor por categoria (arco-íris) | Uma série = **uma cor**; categorias com rótulo longo → barras horizontais |
| Linhas de "total" misturadas às categorias (ex. linha `Total` de `cadunico_por_faixa_renda_2026.csv` desenhada como faixa) | Linhas de total/subtotal removidas antes de desenhar; o total vai para o texto ou a legenda |
| Espaguete (8-11 séries: CAP, imunobiológicos, subgrupos) | **Pequenos múltiplos**: um painel por série, a série em cor, as demais em cinza ao fundo, mesma escala |
| Eixo y cortado sem aviso, exagerando variações pequenas | Taxas e contagens começam em zero; exceção só com o corte declarado na legenda |
| Paleta pastel pensada para tela (amarelo, verde-água e verde claros não passam em papel; azul acinzentado) | **Paleta de impressão** com o mesmo matiz e ordem do site/notebook, validada pelo validador da skill `dataviz` (luminância, croma, daltonismo, contraste ≥ 3:1 no branco): `#3f76b8 #dc7a45 #0f7d5c #b88a1e #b8527b #5c9a3c #6f64ae #b84f4e` — todos os checks passam |
| Mapa de taxa dominado por bairros com denominador pequeno (1 óbito em 36 nascidos = 28‰) | Escala de cor limitada ao **percentil 95** com "≥ X" no topo — o mesmo recurso que o site já usa nos mapas de violência (`teto`); nota na Fonte. **Decisão D5** (§8): vale para todos os mapas de taxa por bairro? |
| Mapa: fundo saturado (mar azul) gasta tinta e compete com o dado | Mesmo provedor de fundo (convenção da skill `generate_map`), com **véu branco de ~40%** por cima; menos margem de contexto; rosa dos ventos e escala menores, mantidos |
| Fontes misturadas (Palatino nos títulos, DejaVu no resto) | IBM Plex Sans em toda a figura — a mesma do corpo do relatório |
| PNG de gráfico (raster) | Gráficos em **PDF vetorial** (texto nítido, arquivo menor); mapas em PDF com o fundo rasterizado a 300 dpi |

Grade e eixos: só linhas horizontais, finas (0,5 pt), cinza claro, contínuas; sem moldura; marcas de 1,6 pt.
Cores de texto sempre em tons de tinta (nunca a cor da série). Marco temporal (ex. mudança da ficha do
Sinan em 2017) = linha vertical fina + nota curta no próprio gráfico.

Onde isso mora: a variante é gerada pelos **mesmos helpers** de `analise.py` (constituição §2), com um tema
de impressão (`_TEMA_IMPRESSAO`: rcParams, paleta, tamanhos) e um parâmetro/variável global que ativa a
saída extra em `visualizacoes/a4/*.pdf` e `mapas/a4/*.pdf` + manifesto. As versões de tela, o site e o DOCX
não mudam. Casos que pedem forma diferente (pequenos múltiplos no lugar de espaguete) viram um helper novo
(`pequenos_multiplos`) chamado na mesma célula, só para a variante A4 — a lista de casos vai em `tasks.md`.

## 6. Fonte única e atualização

- **Estrutura**: `specs/estrutura_eixos.md`, lido **em tempo de build** com o `parse_estrutura_eixos()`
  já existente. Diferente do PDF atual, editar o `.md` e regerar basta.
- **Texto**: `relatorio/textos_curados.json`, as mesmas chaves que o site lê (nome do arquivo;
  `introducao`; `conclusao-<sid>`) + as chaves novas do §3. O fluxo de curadoria não muda:
  DOCX → `sincroniza_docx.py`/`incorpora_update_docx.py` → JSON → regerar o site **e** o LaTeX.
  As chaves novas ganham bookmark no DOCX de curadoria (`gera_docx_curadoria.py`).
- **Texto ausente** (D4): lorem ipsum determinístico por chave, **como hoje** no site e no PDF atual
  (mesma semente/tamanho de `_lorem(seed)`, para o DOCX continuar detectando o que foi editado). O build
  imprime a lista de chaves ainda em lorem, e o inventário (§7) a registra — o controle fica no
  relatório de build, não no PDF.
- **Consistência com o site**: mesma ordem e numeração de eixos, mesmos rótulos/ícones, mesmos textos,
  mesmas fontes; o link "Relatório final em PDF" do site continua no mesmo caminho.
- **Escape**: o gerador escapa os caracteres especiais do LaTeX no texto curado (`% $ & _ # { } ~ ^ \`)
  e converte aspas retas para aspas tipográficas; o texto curado nunca é reescrito (constituição §5).

## 7. Inventário de fontes (conferência, fora do relatório)

`relatorio/inventario_fontes.md` (+ `.csv`), gerado, com duas visões:

1. **Por fonte**: fonte canônica (variável `fonte_*` de `analise.py` → entrada de `fontes.bib`) →
   gráficos, mapas e tabelas que ela gera, e em que eixo/subseção aparecem.
2. **Por arquivo**: cada PNG/CSV de `visualizacoes/`, `mapas/`, `tabelas_finais/` → fonte, função que o
   gera, eixo/subseção, se entra no relatório.

E uma seção de **alertas**: arquivo no disco que nenhuma subseção usa; referência sem fonte; texto
`fonte:` do `.md` diferente do `fonte_dados` real do `analise.py` (ex. "Epi Rio" × "EPI/SVS-Rio…",
"(não informada no catálogo)"); fonte sem entrada no `fontes.bib`. O inventário **aponta** as
divergências e não corrige nada sozinho — a correção é uma decisão do usuário.

Extração: leitura estática (AST) das chamadas de gráfico/mapa em `analise.py` (`nome_arquivo`,
`titulo`, `fonte_dados` resolvidos contra as atribuições `fonte_* = …`) + `estrutura_eixos.md`. Onde a
leitura estática não resolve (f-strings em laço), um manifesto gravado pelos próprios helpers em tempo
de execução, se D1 = B.

## 8. Decisões (tomadas pelo usuário em 2026-09-25)

- **D1 — Figuras**: (A) reaproveitar as PNGs atuais, reduzidas, com legenda ABNT repetindo o título;
  (B) os helpers de gráfico/mapa de `analise.py` gravam também uma **variante A4** sem título/fonte
  embutidos, no tamanho final, e um manifesto (arquivo, título, fonte); o LaTeX usa a variante quando
  existe e cai na PNG atual quando não existe; (C) recortar a faixa do título no build (frágil).
  Recomendação: **B com o fallback de A**.
  → **Decidido: B com fallback de A.**
- **D2 — Pipeline antigo**: substituir `build_notebook_report.py` + Edge pelo LaTeX no mesmo caminho de
  saída (recomendado; o script antigo fica até a validação e depois sai), ou manter os dois.
  → **Decidido: substituir** (mesmo caminho; `build_notebook_report.py` sai depois da validação).
- **D3 — Autoria na capa/folha de rosto**: só a instituição (Prefeitura do Rio / IPP) ou equipe nomeada;
  uso do logo (autorização ainda pendente, `specs/roadmap.md`).
  → **Decidido: equipe nomeada** (informada em 2026-09-25): Leonardo Aucar, Bianca Medina, Caroline Lima,
  Waleska Marques, Maria Norbert — em `pretextual/folha_rosto.tex` (editado à mão, não gerado), sem funções
  por enquanto. Logo segue condicionado à autorização.
- **D4 — Texto ainda não curado** (resumo, aberturas, sínteses, considerações finais, indicadores sem
  texto): caixa "Texto em curadoria" (recomendado), omitir, ou lorem ipsum como hoje.
  → **Decidido: lorem ipsum como hoje** (ver §6).
- **D5 — Teto de cor nos mapas de taxa por bairro** (§5.1): aplicar o percentil 95 (precedente: mapas de
  violência do site) a todos os mapas de taxa/percentual por bairro na variante de impressão, com nota na
  Fonte; ou manter a escala até o máximo (fiel à tela). *Em aberto.*
- **D6 — Achados do inventário** (Bloco 1, T1.5): o que fazer com os 10 arquivos do relatório gerados por
  chamadas comentadas em `analise.py` e com os 13 gráficos regravados por `regen_missing_pngs.py` sem
  fonte. *Em aberto.*

## 9. Fora do escopo

- Mudar a ordem das seções de `analise.py` (continua ordem de build, `specs/ajuste_eixos` §9.1).
- Mudar a identidade dos gráficos (paleta, tipografia do matplotlib) além do tamanho/título da variante A4.
- O DOCX de curadoria continua sendo gerado como hoje (só ganha as chaves novas).
- Deploy: o PDF segue versionado em `relatorio/` como hoje; o workflow do Pages não muda.
