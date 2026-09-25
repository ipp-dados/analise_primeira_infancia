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

## 9. Fora do escopo

- Mudar a ordem das seções de `analise.py` (continua ordem de build, `specs/ajuste_eixos` §9.1).
- Mudar a identidade dos gráficos (paleta, tipografia do matplotlib) além do tamanho/título da variante A4.
- O DOCX de curadoria continua sendo gerado como hoje (só ganha as chaves novas).
- Deploy: o PDF segue versionado em `relatorio/` como hoje; o workflow do Pages não muda.
