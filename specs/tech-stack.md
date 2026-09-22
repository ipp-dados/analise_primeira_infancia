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
  **GitHub Pages**.

## Exportação em PDF

- Pipeline separada (mesma pasta de skill, script diferente:
  `build_notebook_report.py`) monta um HTML espelhando `analise.py` seção a
  seção com os **PNGs reais do matplotlib** (não o motor SVG do relatório
  interativo) e renderiza para PDF via **Chrome headless**
  (`--headless=new` + `--user-data-dir` isolado, obrigatório — ver
  `.claude/skills/export_pdf_report/SKILL.md` para o incidente que motivou
  essa regra).
- Verificação do PDF gerado usa **pypdf** (contagem de páginas) e **PyMuPDF**
  (`fitz`, rasterizar páginas de amostra para inspeção visual).

## O que foi tentado e descartado (não reintroduzir sem motivo novo)

- Basemap de satélite (`Esri.WorldImagery`) — trocado por basemap
  cartográfico por preferência explícita do usuário.
- `CartoDB.Voyager` (exige API key agora) e `OpenStreetMap.Mapnik` (bloqueia
  fetch automatizado) como provedores de tile.
- `geopandas`/`mapclassify` `scheme=` para bins de legenda — não aplica
  formatação de número customizada aos rótulos.
- Relatório em 3 variações estáticas (`index`/`lighter`/`white_index.html`)
  — consolidado num único `index.html` com tema automático.
