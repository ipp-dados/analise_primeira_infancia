# Tech Stack

Inventário do que o projeto usa e para quê — para decidir com o que é
consistente estender, e o que evitar reintroduzir (ver histórico de opções
descartadas nas `SKILL.md` e nas specs por rodada).

## Linguagem e execução

- **Python 3**, sem gerenciador de ambiente próprio além de `venv`/`pip` —
  `requirements.txt` na raiz, `analise_env/` é o ambiente local (gitignorado).
- **Jupytext** (`py:percent`, `jupytext.toml`) mantém `analise.py` como
  fonte versionada e sincronizável com `analise.ipynb` (gerado, gitignorado).
  Rodado interativamente via **JupyterLab/Jupyter Notebook** (`ipykernel`).
- Sem framework de testes, linter ou CI de qualidade de código configurado.
  Validação é manual: reexecutar o notebook do zero e inspecionar
  saídas/gráficos (ver `specs/*/validation.md` de cada rodada para o que foi
  checado).

## Dados e banco

- **CadÚnico** vem de um banco **PostgreSQL** (camada silver, CTPE/Siurb),
  acessado via **SQLAlchemy** + **psycopg** (`connect_db_ctpe` em `analise.py`).
  Credenciais em `.env` (`python-dotenv`), nunca commitadas — ver `.env.example`.
- Demais fontes (Tabnet/DataSUS, Censo/IBGE, SISVAN, IBGE SIDRA, planilha
  TabWin de óbitos por causas evitáveis) são arquivos estáticos em
  `dados_locais/`, sem conexão de rede em tempo de análise.
- **pandas** para toda a manipulação tabular; **openpyxl** para ler/escrever
  Excel (`.xlsx`); saídas finais em CSV e Excel em `tabelas_finais/`.

### Convenção de nomes (`dados_locais/` · `tabelas_finais/` · `visualizacoes/` · `mapas/`)

Formalizada em 2026-09-22 a partir do padrão que já era maioria — ver
`specs/reorganize-naming/plan.md` para o levantamento completo (achados,
arquivos órfãos removidos, um bug real de dado congelado que motivou isto).

- `dados_locais/`: uma pasta por fonte, tema, snake_case sem espaço/acento
  maiúsculo (`censo/`, `mortalidade/`, `sisvan/`, `ibge_sidra/`,
  `vacinacao/`, `nascidos_vivos/`, `geo/`). Um dado nunca mora em duas
  pastas — se duas seções de análise usam o mesmo arquivo, as duas leem da
  mesma pasta.
- `tabelas_finais/`/`visualizacoes/`/`mapas/`: `{tema}_{indicador}[_{corte}]_{granularidade_ou_ano}.{ext}`.
  `tema` normalmente repete o nome da pasta de origem em `dados_locais/`.
  `corte` (opcional): `raca`, `sexo`, `subgrupo`, `cap`. Sufixo de
  granularidade: `_por_ano` (série município), `_bairro_ano` (série por
  bairro), `_{ANO}` (corte transversal — mapas, prefixo `tabela_mapa_`
  reservado pro par CSV↔PNG de cada mapa).
- **O nome do PNG reaproveita o nome do CSV correspondente** sempre que os
  dois existem pro mesmo indicador — é o mecanismo de rastreio entre as
  três pastas, não uma tabela de mapeamento separada pra manter em dia.
- Exceção documentada, não é dívida técnica: `mapas/tabelas_bairros/*.xlsx`
  é o resquício intencional do padrão anterior (Excel), mantido só pra 2
  tabelas que não migraram — ver README.

## Geoespacial (mapas)

- **geopandas** + **shapely** + **pyproj** + **pyogrio** para ler/manipular
  os GeoJSON de `dados_locais/geo/` e fazer os joins/dissolves por
  bairro/AP/RP/CAP.
- **contextily** (+ `xyzservices`, `mercantile`, `rasterio`, `affine`,
  `geopy`, `joblib`) busca os tiles do basemap (`Esri.OceanBasemap` — ver
  `.claude/skills/generate_map/SKILL.md` para o porquê desse provedor
  específico e os alternativos já testados/descartados). Precisa de rede
  no momento do render; sem `fundo`, a função roda 100% offline.
- **matplotlib-scalebar** para a escala gráfica (com correção de distorção
  de latitude do Web Mercator).
- **mapclassify** é dependência soft (a classificação de bins é manual via
  `pd.cut`, não via `scheme=` do geopandas — ver o SKILL.md acima para o
  motivo: `scheme=` não respeita a formatação pt-BR do rótulo da legenda).

## Visualização (notebook/PDF)

- **matplotlib** + **seaborn** para todos os gráficos do notebook
  (`serie_temporal`, `grafico_barra`, `grafico_barra_agrupado`,
  `serie_temporal_multipla`) e para os mapas coropléticos. Estilo
  compartilhado: paleta categórica de 11 cores, título serifado (Palatino
  Linotype), rodapé de fonte, DPI 200 (gráficos) / 300 (mapas) — ver
  `specs/visual-identity/`.
- Export padrão em PNG (`visualizacoes/`, `mapas/`); export SVG existe mas
  fica comentado por padrão em cada função de plot.

## Relatório interativo (`relatorio/index.html`)

- **HTML/CSS/JS vanilla**, um único arquivo autocontido — sem framework, sem
  passo de build, sem dependência externa além de uma fonte via Google
  Fonts. Gerado por `.claude/skills/export_pdf_report/scripts/build_html_report.py`
  (Python puro), que lê `tabelas_finais/*.csv` e os GeoJSON de
  `dados_locais/geo/` e emite gráficos/mapas como **SVG inline** (motor de
  chart próprio: `lineChart`/`barChart`/`groupedBarChart`, mapas via
  `mapa_svg()`), não como imagem raster.
- Tema claro/escuro automático via `prefers-color-scheme`, sem JS de
  detecção de tema.
- Deploy: **GitHub Actions** (`.github/workflows/deploy-relatorio.yml`,
  disparo manual `workflow_dispatch`) publica `relatorio/index.html` no
  **GitHub Pages** (copiado para `_site/index.html`, nome exigido na raiz
  do site pelo Pages).

## Exportação em PDF/DOCX

- Pipeline separada (mesma pasta de skill, script diferente:
  `build_notebook_report.py`) monta um HTML espelhando `analise.py` (por
  eixo da política municipal, `specs/ajuste_eixos/`) com os **PNGs reais do
  matplotlib** (não o motor SVG do relatório interativo) e renderiza para
  PDF via **Chrome headless** (`--headless=new` + `--user-data-dir`
  isolado, obrigatório — ver `.claude/skills/export_pdf_report/SKILL.md`
  para o incidente que motivou essa regra). Chrome não está garantido no
  ambiente de desenvolvimento — **Edge** (mesmo motor Chromium, mesmas
  flags) é o fallback documentado no `SKILL.md`. O `file://` da URL de
  entrada precisa da forma com letra de unidade do Windows
  (`file:///C:/...`) — a forma POSIX do Git Bash (`/c/...`) gera um PDF
  quase vazio sem erro nenhum (achado registrado no `SKILL.md`).
- Verificação do PDF gerado usa **pypdf** (contagem de páginas) e **PyMuPDF**
  (`fitz`, rasterizar páginas de amostra para inspeção visual).
- **DOCX de curadoria** (`specs/ajuste_eixos/` Bloco 5): `python-docx`
  (`requirements.txt`) gera `relatorio/curadoria_textos.docx` — 1 heading
  por eixo/subseção, imagens reais redimensionadas (Pillow, JPEG em
  memória — nunca embute o PNG original de `mapas/`, ~6MB cada), 1
  parágrafo de texto de análise por visualização/mapa, cada um com um
  bookmark OOXML (`w:bookmarkStart`/`w:bookmarkEnd`, via `docx.oxml` —
  `python-docx` não tem API de alto nível pra isso) nomeado por um ID
  estável (nome de arquivo sem extensão). Sumário do DOCX usa um **campo
  `TOC` nativo do Word** (não uma lista estática) — o usuário atualiza
  clicando "Atualizar campo"/F9 conforme edita o documento.
- **Sincronização de texto curado** (`specs/ajuste_eixos/` Bloco 7,
  `sincroniza_docx.py`): texto editado à mão no DOCX vira a fonte de
  `relatorio/textos_curados.json` (`{seed: texto}`, seed = mesmo nome de
  arquivo), lido por `build_html_report.py`/`build_notebook_report.py` via
  um pequeno helper (`_texto_analise(seed)`) antes de cair no lorem ipsum
  determinístico — por isso os seeds de texto do HTML/PDF foram alinhados
  a nomes de arquivo reais (não ao rótulo legível da opção) nessa rodada.

## O que foi tentado e descartado (não reintroduzir sem motivo novo)

- Basemap de satélite (`Esri.WorldImagery`) — trocado por basemap
  cartográfico por preferência explícita do usuário.
- `CartoDB.Voyager` (exige API key agora) e `OpenStreetMap.Mapnik` (bloqueia
  fetch automatizado) como provedores de tile.
- `geopandas`/`mapclassify` `scheme=` para bins de legenda — não aplica
  formatação de número customizada aos rótulos.
- Relatório em 3 variações estáticas (`index`/`lighter`/`white_index.html`)
  — consolidado num único `index.html` com tema automático.
- Reordenar fisicamente as células de `analise.py` por eixo da política
  municipal (`specs/ajuste_eixos/plan.md` §9.1) — mantida a ordem técnica
  de construção do dado; só a apresentação (HTML/PDF/DOCX) é reorganizada.
- Reescrever `build_html_report.py`/`build_notebook_report.py` como
  renderizadores genéricos guiados por `specs/estrutura_eixos.md`
  (`parse_estrutura_eixos()` de verdade, não só os seeds de texto) — maior
  risco/custo do que o ganho, decisão do usuário registrada em
  `specs/ajuste_eixos/specs.md` §9.3; os dois continuam Python hardcoded,
  reorganizados fisicamente à mão quando o `.md` muda de agrupamento.

## Inclusão dos dados de Proteção (`specs/inclusao_dados_protecao`)

- Nível geográfico **RA** (`codra`) por `dissolve` do geojson de bairros (sem arquivo novo). Tema de cor `protecao` = `OrRd`
  (`Purples` descartado: já é `censo` no HTML).
- Fonte Sinan NET/Tabnet (CSV latin-1 com 6 linhas de metadados, formato largo) lida por `carrega_sinan_bairro`; IPS/Data.Rio por RA (xlsx).
- Fundo cartográfico: `Esri.OceanBasemap` (serviço `Ocean_Basemap`) fora do ar em 2026-09; usar `World_Ocean_Base` (`fundo='mapa_oceano_base'`).
