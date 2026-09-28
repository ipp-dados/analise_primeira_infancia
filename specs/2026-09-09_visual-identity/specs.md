# Especificação — Identidade Visual Unificada + Exports HTML/PDF

## 0. Contexto

O projeto hoje produz três saídas a partir da mesma análise, cada uma com uma
identidade visual diferente:

| Saída | Conteúdo hoje | Motor de gráfico | Estilo |
|---|---|---|---|
| `analise.ipynb` / `analise.py` | Todo o código, tabelas, gráficos e texto descritivo | matplotlib/seaborn, sem paleta/tipografia consistente entre funções | Default do seaborn; só os mapas (`mapa_coropletico_bairros`) têm um estilo cartográfico cuidado (serifada no título, footnote de fonte/CRS, legenda com contraste) |
| `relatorio/*.html` (3 arquivos: `index`, `lighter`, `white`) | Espelha o notebook quase 1:1 (mesmos títulos/notas), ~32 gráficos SVG interativos | Motor JS próprio (`lineChart`/`barChart`/`groupedBarChart`), paleta pastel de 11 cores já validada | Interativo (hover, tabela de dados alternativa), tema claro/escuro |
| `relatorio/analise_primeira_infancia.pdf` | Espelha o notebook seção a seção, mas usa os PNGs reais de `visualizacoes/` (não o motor JS) | Os mesmos PNGs matplotlib/seaborn do notebook | Herda o que quer que o notebook tenha |

Desde a última rodada (`specs/2026-09-09_maps-and-ibge`), o notebook ganhou **~35 novos
gráficos/mapas** (11 mapas de bairro, 2 mapas por CAP, 6 gráficos SIDRA, 22
séries temporais de evitáveis) que **não existem ainda em nenhum dos dois
relatórios** — eles ficaram desatualizados. Este spec cobre atualizar os três
outputs e, ao mesmo tempo, unificar a identidade visual entre eles.

## 1. Objetivo

1. Uma identidade visual única — paleta, tipografia, convenção de
   título/fonte/legenda — reconhecível nos três outputs, usando os **mapas
   atuais como referência de qualidade** (título serifado, footnote de fonte
   + sistema de referência, legenda com contraste, halo de texto sobre fundo
   ocupado).
2. Restilizar os gráficos matplotlib/seaborn do próprio notebook (hoje sem
   padrão), não só os relatórios.
3. Atualizar `relatorio/*.html` e o PDF com todo o conteúdo novo de
   `specs/2026-09-09_maps-and-ibge`.
4. Redefinir o papel do HTML: **só visualização**, sem o texto/notas que hoje
   espelham o notebook — ver §5.
5. Dar destaque a séries temporais com muitas linhas, evitando "espaguete"
   ilegível.

## 2. Papel de cada saída (definição operacional)

- **Notebook** (`analise.py`/`.ipynb`): fonte de verdade. Todo o código,
  todas as tabelas, todos os gráficos, todo o texto descritivo/metodológico.
  Público: quem vai auditar/estender a análise.
- **Relatório PDF** (`relatorio/*.pdf`): gráficos + tabelas + descrição,
  fiel à ordem/seções do notebook, mas sem código — para leitura linear,
  impressão, ou quem quer o "notebook sem o Python". Público: leitura
  detalhada por quem não abre o notebook.
- **HTML** (`relatorio/*.html`): **só visualização**, interativo, com opção
  de ver a tabela de dados por trás de cada gráfico. Sem a prosa/notas de
  método que hoje ele copia do notebook — título + fonte bastam, o "porquê"
  fica no PDF/notebook. Público: navegação rápida, apresentação,
  compartilhamento leve.

## 3. Identidade visual

### 3.1 Paleta

- **Mapas coropléticos**: continuam sequenciais de um matiz só por mapa
  (convenção correta para magnitude — ver skill `generate_map`), mas o matiz
  passa a variar **por tema**, em vez de `Oranges` fixo para tudo:

  | Tema | Matiz proposto | Mapas afetados |
  |---|---|---|
  | Natalidade (nascidos vivos, baixo peso) | Verde-azulado suave (`Teal`/`BuGn`) | 3 mapas |
  | Mortalidade (neonatal, gravidez, puerpério, raça, evitáveis/CAP) | Rosa-vinho suave (`RdPu`/`PuRd` dessaturado) | 12 mapas |
  | CadÚnico (renda/vulnerabilidade) | Âmbar suave (`YlOrBr` dessaturado) | 2 mapas |
  | Censo/população | Azul suave (`Blues`) | 6 mapas (já existentes) |

  Cada matiz é dessaturado/aclarado para ficar no mesmo registro "pastel" do
  resto do projeto (não um pastel raso a ponto de perder contraste na
  legenda — mantém o requisito de contraste já resolvido no `generate_map`).
- **Gráficos de barra/linha (notebook + HTML)**: reusar literalmente a
  paleta categórica de 11 cores já validada em `relatorio/lighter_index.html`
  (`--c1`…`--c11`), para que a mesma série tenha a mesma cor no notebook, no
  PDF e no HTML. Hoje só `grafico_barra` usa `palette='pastel'` (paleta
  genérica do seaborn, não a nossa); as outras 3 funções não fixam paleta
  nenhuma.

### 3.2 Tipografia e convenções de gráfico

Estender a convenção dos mapas às 4 funções de plot do notebook
(`serie_temporal`, `serie_temporal_multipla`, `grafico_barra`,
`grafico_barra_agrupado`) e ao motor JS do HTML:
- Título: serifado (`Palatino Linotype`, como os mapas), peso bold.
- Eixos/legendas: sans-serif, tamanho consistente entre funções (hoje varia
  ponto a ponto).
- **Toda visualização passa a ter uma fonte visível** — nova convenção
  `fonte_dados` (mesma ideia do parâmetro que os mapas já têm) virando
  rodapé discreto tipo "Fonte: ...", obrigatório em todo call site.
- **Toda visualização com mais de uma série precisa de legenda**; toda
  visualização com eixo categórico precisa de rótulos legíveis (já é quase
  sempre o caso, mas sem padronização de rotação/tamanho).
- DPI: mapas já salvam a 300 DPI; os outros gráficos hoje usam o default
  (100 DPI, borrado em tela grande/impressão) — subir para um DPI consistente
  (proposta: 200) nos 4 tipos de gráfico do notebook.

### 3.3 Séries temporais com muitas linhas

Vários gráficos hoje têm mais linhas do que se consegue distinguir com
segurança (o próprio `relatorio/specs.md` já registra isso para cobertura
vacinal, "11 séries está fora do que a validação formal de distinguibilidade
cobre"). Candidatos identificados:
- `cobertura_vacinal_epi_comparativo_anos` (11 imunobiológicos)
- As 18 séries de evitáveis por subgrupo × CAP (`specs/2026-09-09_maps-and-ibge` D.2a,
  10 CAPs por gráfico)
- Painéis por raça/cor (5-6 séries) — provavelmente ok sem destaque

Proposta de regra: acima de um limiar (~6 séries), destacar só as N mais
relevantes (maior valor final, ou uma curadoria manual quando fizer sentido
por conteúdo) em cor plena, e desenhar o resto em cinza claro/baixa opacidade
sem entrar na legenda principal (ou agrupadas como "outras"). Aplica-se
tanto ao motor matplotlib (notebook/PDF) quanto ao motor JS (HTML) — mesma
regra, duas implementações.

## 4. Decisões

| # | Pergunta | Proposta (default se não houver objeção) |
|---|---|---|
| A | Consolidar os 3 arquivos HTML (`index`/`lighter`/`white`) em **um único** arquivo com tema claro/escuro automático (`prefers-color-scheme`), em vez de 3 arquivos quase-duplicados de ~4000 linhas cada? | **Sim** — reduz o esforço de manter 3 cópias sincronizadas ao adicionar ~35 visualizações novas, e o motor JS já suporta os dois temas via variáveis CSS. |
| B | Remover a prosa/notas de método do HTML (§2)? | **Sim**, mantendo só título + fonte por gráfico — a descrição completa fica no notebook/PDF. |
| C | Limiar de "muitas séries" para o destaque em §3.3 | **6 séries** por gráfico |
| D | DPI dos gráficos não-mapa | **200** (upgrade de 100, sem chegar aos 300 dos mapas — arquivos menores, ainda nítidos) |
| E | O PDF deve ganhar as ~35 visualizações novas de `specs/2026-09-09_maps-and-ibge` nesta rodada? | **Sim** — é parte do "atualizar HTML e PDF" pedido |
| F | Versionar `relatorio/*.html` no git (hoje ignorado por `*.html` no `.gitignore`)? | Manter como está (não versionado) — fora do escopo pedido, mas registrar no roadmap se quiser revisitar |

## 5. Fora de escopo (registrar no roadmap)

- Substituir o HTML por um painel Streamlit (já no roadmap).
- Qualquer conteúdo novo de dados/mapa (isto é só restyling + export).
- Refatorar `analise.py` em módulos (já no roadmap, rodada separada).

## 6. Branch

`spec/visual-identity`, criada a partir de `spec/maps-and-ibge` (ainda não
mesclada em `staging_main` — merge de `spec/maps-and-ibge` continua pendente
de aprovação, independente desta rodada).
