# Plano — `specs/relatorio_latex`

Branch de trabalho: `spec/relatorio-latex`, a partir de `planning`, depois das decisões do
`specification.md` §8.

## Organização em `relatorio/`

```
relatorio/
├── analise_primeira_infancia.pdf     # saída final (mesmo caminho de hoje; o site aponta pra cá)
├── inventario_fontes.md / .csv       # gerado — conferência de fontes (§7), não entra no PDF
├── textos_curados.json               # inalterado — lido pelo site e pelo LaTeX
├── controle_revisao.json, curadoria_textos*.docx, specs.md   # inalterados
└── latex/
    ├── relatorio.tex                 # mestre, editado à mão: classe abntex2, \input das partes
    ├── estilo.sty                    # editado à mão: cores, fontes, legendas ABNT, caixas, abertura de capítulo
    ├── pretextual/                   # editado à mão: capa, folha de rosto, siglas
    ├── fontes.bib                    # editado à mão: Fontes (NBR 6023) + campo `variaveis` = fonte_* do analise.py
    ├── fontes/                       # Fraunces (OFL), versionada
    ├── build/
    │   ├── gera_latex.py             # estrutura_eixos.md + textos_curados.json + tabelas_finais → gerado/
    │   ├── tabelas.py                # CSV → longtable ABNT (portado de build_notebook_report.py)
    │   └── inventario_fontes.py      # §7
    ├── gerado/                       # saída do gerador (.tex por capítulo/apêndice) — versionado, diffável
    ├── icones/                       # PDFs gerados dos SVG de website/assets/icons/
    └── _build/                       # latexmk aux + cache de imagens reduzidas — gitignorado
```

Mesmo padrão do `website/`: fonte à mão (`relatorio.tex`, `estilo.sty`, `pretextual/`, `fontes.bib`)
separada da saída do gerador (`gerado/`), que ninguém edita à mão (constituição §4).

Comando único:

```
python relatorio/latex/build/gera_latex.py [--sem-pdf]
```

→ valida `estrutura_eixos.md` (`valida_estrutura`), escreve `gerado/`, reduz imagens para o cache,
roda `latexmk -xelatex` e copia o PDF para `relatorio/analise_primeira_infancia.pdf`.

## Blocos

**Bloco 0 — Aprovação.** Decisões D1-D4 tomadas (2026-09-25); faltam os nomes da equipe; branch `spec/relatorio-latex`.

**Bloco 1 — Inventário de fontes** (independente; útil de imediato).
`inventario_fontes.py` + primeira versão de `fontes.bib` com uma entrada NBR 6023 por fonte
(IBGE Censo 2022/SIDRA, Ripsa/MS, CadÚnico/CTPE, SIM, SINASC, Sinan, SISVAN, EPI/SVS-Rio, PNAD
Contínua, Censo Escolar/INEP, IPS/Data.Rio, camadas geográficas Data.Rio/IBGE). Revisão das
divergências com o usuário antes de mexer em qualquer `fonte:`.

**Bloco 2 — Esqueleto e páginas-amostra.** `relatorio.tex`, `estilo.sty`, capa, folha de rosto,
resumo, listas, sumário, Fontes, **um** capítulo montado à mão (Alimentação — curto e com gráficos,
mapas e pendentes) + um apêndice. Compila; **revisão visual com o usuário** (capa, abertura de
capítulo, página de figuras, tabela) antes de gerar o resto.

**Bloco 3 — Gerador data-driven.** `gera_latex.py` lê `estrutura_eixos.md` e `textos_curados.json`,
gera Introdução, 6 capítulos, Considerações finais; legendas (título e fonte) vindas do inventário
(Bloco 1); caixas de pendente; lorem determinístico onde falta texto; remissões às tabelas; cache de imagens.

**Bloco 4 — Apêndice de tabelas.** `tabelas.py`: porta a seleção/formatação de tabelas de
`build_notebook_report.py` (colunas de %, renomes, `ano` sem separador, escala 0-1 da PNAD) para
`longtable` + `booktabs`, formato pt-BR (1.234,5), Fonte abaixo. Tabelas de 166 bairros em
`longtable`; paisagem só se necessário.

**Bloco 5 — Figuras A4** (D1 = B). Parâmetro nos helpers de `analise.py` (`serie_temporal`,
`grafico_barra*`, `serie_temporal_multipla*`, `grafico_barra_ranking`, `mapa_coropletico_bairros`)
que também grava a variante A4 em `visualizacoes/a4/` e `mapas/a4/` + manifesto (arquivo, título,
fonte, função); `regen_missing_pngs.py` acompanha. Validar com uma execução completa do notebook
(inclui CadÚnico → ambiente `analises_env` com `.env`, feita pelo usuário).

**Bloco 6 — Curadoria e integração.** Chaves novas (`resumo`, `abertura-*`, `achados-*`,
`consideracoes_finais`) no DOCX (`gera_docx_curadoria.py`); `sincroniza_docx.py` passa a regerar o
LaTeX no lugar do HTML do PDF; skill `export_pdf_report` reescrita para o novo pipeline (e o
`build_notebook_report.py` aposentado após a validação); `.gitignore` (`relatorio/latex/_build/`);
`CLAUDE.md`, `README.md` (changelog breve), `specs/roadmap.md`, `specs/tech-stack.md`.

**Bloco 7 — Validação** (`validation.md`) e PDF final.

Ordem: 1 e 2 em paralelo → 3 → 4 → 5 (pode ficar depois da primeira entrega, graças ao fallback) → 6 → 7.

## Riscos

- **Ambiente**: MiKTeX instala pacotes sob demanda e ainda "não checou atualizações"; fixar a lista de
  pacotes usados e documentar em `specs/tech-stack.md`. CI não compila o PDF (sem `tabelas_finais/`), como hoje.
- **Texto curado com caracteres do LaTeX** (`%` é comum: "7,6%") — escape centralizado + teste com
  todas as 58 entradas atuais.
- **Legibilidade das PNGs atuais** (D1 = A ou fallback): fontes internas pequenas nos mapas; medir e
  mostrar nas páginas-amostra do Bloco 2.
- **Tamanho**: 144 MB de mapas no disco → cache reduzido obrigatório; meta < 20 MB.
