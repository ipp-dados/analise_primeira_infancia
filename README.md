# Análise da Primeira Infância Carioca

Pipeline de dados e relatório sobre a primeira infância (0 a 6 anos) no município do
Rio de Janeiro, produzido pelo **Instituto Pereira Passos (IPP)**, Prefeitura da Cidade
do Rio de Janeiro. Reúne indicadores de população, assistência social, saúde e educação
espalhados por fontes diferentes — Censo, CadÚnico, DataSUS/Tabnet, SISVAN, PNAD, Censo
Escolar — em um único pipeline (`analise.py`) que limpa, cruza e visualiza os dados por
bairro, Área de Planejamento, Região de Planejamento e Área Programática de Saúde.

> ⚠️ **Repositório e relatório em desenvolvimento.** O conteúdo, os dados e a estrutura
> ainda podem mudar — ver o aviso no próprio relatório publicado.

## 🔗 Relatório

| | |
|---|---|
| **Relatório interativo (HTML)** | [ipp-dados.github.io/analise_primeira_infancia](https://ipp-dados.github.io/analise_primeira_infancia/) |
| **Relatório em PDF** | [`relatorio/analise_primeira_infancia.pdf`](relatorio/analise_primeira_infancia.pdf) |
| **Notebook fonte** | [`analise.py`](analise.py) (Jupytext, abre como notebook) |

O relatório HTML é gerado a partir do notebook por
`.claude/skills/export_pdf_report/scripts/build_html_report.py` — mesmos dados, gráficos
interativos (SVG, tooltip, tabela alternativa) em vez de imagens estáticas. O PDF é a
versão para impressão/download, com os gráficos originais do matplotlib.

## Fontes de dados

| Fonte | O que traz | Onde |
|---|---|---|
| **CadÚnico** | Famílias/crianças por renda, idade e bairro | Banco CTPE (camada silver, Siurb) — consulta direta, não é arquivo local |
| **DataSUS/Tabnet** | Nascidos vivos, baixo peso, mortalidade (neonatal, por raça/cor, gravidez/puerpério) por bairro | `dados_locais/mortalidade/`, `dados_locais/nascidos_vivos/` |
| **Censo Demográfico** (IBGE/Data.Rio) | População por bairro e idade, 2000/2010/2022 | `dados_locais/censo/` |
| **IBGE SIDRA** | Censo 2022 por raça/sexo e frequência escolar, nível município | `dados_locais/ibge_sidra/` |
| **SISVAN** | Sobrepeso e desnutrição infantil | `dados_locais/sisvan/` |
| **EPI/SVS-Rio** | Cobertura vacinal | `dados_locais/vacinacao/` |
| **PNAD Contínua / Censo Escolar (INEP)** | Frequência escolar e matrículas | `dados_locais/educacao/` |
| **SIM/SVS-Rio (TabWin)** | Óbitos por causas evitáveis, por Área Programática de Saúde, 2006-2025 | `dados_locais/mortalidade/obitos_causas_evitaveis_primeira_infancia_cap_2006_2025.xlsx` |
| **Data.Rio/IPP, IBGE** | Geometrias de bairro, Área Programática de Saúde, UF e municípios vizinhos | `dados_locais/geo/` |

*OBS: dados brutos completos da versão MVP e do relatório final ficam num Google Drive
compartilhado, acesso restrito — solicitar a leonardoaucar@prefeitura.rio.*

## Estrutura do Projeto
*   `analise.py`: Script principal (sincronizável com Jupytext) que contém extração, limpeza, análise e geração de visualizações; organizado como notebook (células e markdown). Todas as funções de limpeza/wrangling e de visualização ficam centralizadas na seção **Pacotes e Funções Auxiliares**, no topo do notebook.
*   `requirements.txt`: Lista de dependências Python do projeto.
*   `dados_locais/`: Diretório para os dados brutos. Uma pasta por fonte/tema (`censo/`, `mortalidade/`, `sisvan/`, `ibge_sidra/`, `vacinacao/`, `nascidos_vivos/`, `educacao/`, `geo/`).
*   `dados_locais/geo/`: Camadas geográficas de referência, versionadas no git: `limite_bairros_rio.geojson` (limites de bairro do Rio, Data.Rio/IPP, camada `Cartografia/Limites_administrativos`, geometria simplificada, com as colunas de Área/Região de Planejamento usadas nos mapas agregados), `limite_uf_brasil.geojson` (limites dos estados/UF do Brasil, IBGE), `limite_municipios_rj.geojson` (limites e nomes dos 92 municípios do estado do Rio, IBGE, usados para rotular os municípios vizinhos nos mapas com basemap) e `limite_ap_saude_rio.geojson` (as 10 Coordenadorias de Área Programática de Saúde da SMS-Rio, Data.Rio -- não são as 5 Áreas de Planejamento do IPP acima; coluna `cod_ap_sms`).
*   `dados_locais/tratados/`: Saída intermediária de datasets limpos.
*   `tabelas_finais/`: Pasta de saída padronizada (CSV/Excel) para tabelas e agregados gerados pelo pipeline.
*   `visualizacoes/`: Diretório para os gráficos exportados pelo notebook (PNG por padrão; exportação adicional em SVG disponível, mas comentada, em cada função de gráfico). Nomes de arquivo refletem a seção/tema da análise (ex.: `cobertura_vacinal_epi_ano.png`, `cadunico_criancas_por_idade.png`).
*   `mapas/`: Imagens de mapas coropléticos, gerados dentro do próprio `analise.py` com `geopandas`/`contextily` pela função `mapa_coropletico_bairros`: basemap cartográfico (Esri Ocean Basemap), limite estadual sobreposto, municípios vizinhos rotulados, rosa dos ventos, escala gráfica, título em fonte serifada (Palatino Linotype), formato ~1,46:1 (próximo de A4 paisagem) e exportação a 300 DPI. Cobre hoje o Censo (bairro/AP/RP), mortalidade por causas evitáveis por CAP (grupo e subgrupo), e ~20 mapas por bairro no ano mais recente (CadÚnico, nascidos vivos, baixo peso, óbitos por raça, mortalidade neonatal, óbitos gravidez/puerpério) -- cada um com sua tabela-insumo gêmea em `tabelas_finais/tabela_mapa_*.csv`. `mapas/tabelas_bairros/` é o resquício do padrão anterior (Excel), mantido só para `dados_datasus_por_bairro.xlsx` e as tabelas do Censo (`tabela_mapa_0_4_*.xlsx`); nascidos vivos e baixo peso já migraram para o padrão CSV.
*   `relatorio/`: `index.html` autocontido, gerado por
    `.claude/skills/export_pdf_report/scripts/build_html_report.py`, com as visualizações do
    notebook renderizadas de forma interativa (SVG, tooltip, tabela de dados) e todos os mapas
    de `mapas/` (redimensionados/WebP), para compartilhamento com quem não abre o notebook.
    Publicado diretamente no GitHub Pages. Tema claro/escuro automático
    (`prefers-color-scheme`); cada visualização traz só título + fonte + tabela opcional, sem a
    prosa/notas de método do notebook (essas ficam no notebook e no PDF).
*   `specs/`: Constituição do projeto (`constitution.md`), stack técnica (`tech-stack.md`),
    roadmap (`roadmap.md`) e uma subpasta por rodada de planejamento (`plan.md`,
    `specification.md`/`specs.md`, `tasks.md`, `validation.md`) -- histórico completo de
    decisões de design, com o *porquê* por trás de convenções do código.
*   `notebooks/`: Notebook(s) .ipynb sincronizados com `analise.py` via Jupytext (opcional).
*   `.env.example`: Exemplo de variáveis de ambiente necessárias (ex.: credenciais DB).
*   `scripts/`: Utilitários e conversores auxiliares (se presentes).

Pastas de dados/saída (`dados_locais/`, `tabelas_finais/`, `mapas/`, `visualizacoes/`) mantêm um arquivo `.gitkeep` para preservar a estrutura de pastas no git mesmo quando o conteúdo real (dados brutos sensíveis ou saídas geradas) não é versionado.

## Fluxo de Análise (`analise.py`)
O script `analise.py` realiza as seguintes operações, em ordem prática:
1.  **Pacotes e Funções Auxiliares** (topo do notebook): carregamento de pacotes, leitura de configurações (.env) e definição de todas as funções reutilizáveis de limpeza/wrangling (`limpeza_tabnet_bairros`, `carrega_raca_bairro`, `carrega_causas_evitaveis_*`, etc.) e de visualização (`serie_temporal`, `grafico_barra*`, `serie_temporal_multipla`). As seções de análise abaixo só chamam essas funções.
2.  Limpeza SISVAN: processamento de arquivos SISVAN (sobrepeso, desnutrição) e salvamento de saídas intermediárias em `dados_locais/tratados/` e finais em `tabelas_finais/`.
3.  Censo: leitura dos microdados do Censo (2022 e outros anos), cálculo de totais e percentuais por bairro/idade e export para `tabelas_finais/censo_por_bairro.csv`.
4.  CadÚnico: extração via CTPE, análise por faixa de renda, idade e bairro, com export em `tabelas_finais/` (ex.: `cadunico_por_faixa_renda_2026.csv`).
5.  DATASUS (Tabnet) — padrão comum: os arquivos Tabnet são normalizados pela função `limpeza_tabnet_bairros(df, categoria)`, que extrai `codigo` e `bairro`, remove linhas 'Total' e harmoniza nomes de colunas.
6.  Para cada tema do DATASUS (nascidos vivos, baixo peso, mortalidade precoce/tardia, óbitos gravidez/puerpério) são geradas séries temporais e agregações anuais. Nas junções entre tabelas, a chave `codigo` (quando disponível) e `bairro`+`ano` são utilizadas para evitar ambiguidades.
6b. Óbitos por causas evitáveis na primeira infância por CAP: `extrai_planilha_evitaveis_cap` lê a planilha TabWin (10 blocos de 12 linhas por aba) e materializa 6 CSVs fiéis à fonte em `dados_locais/tratados/`; `agrega_grupo_cid` deriva o nível grupo a partir dos 8 subgrupos CID; mapas por CAP usam o nível `'cap'` de `mapa_coropletico_bairros` (geometria em `dados_locais/geo/limite_ap_saude_rio.geojson`, coluna `cod_ap_sms` -- não confundir com o nível `'ap'`, as 5 Áreas de Planejamento do IPP). Além do grupo agregado, dois subgrupos específicos (gestação `1.2.1`, parto `1.2.2`) têm mapa e série temporal próprios por CAP, `< 1 ano`; e uma matriz completa (6 subgrupos evitáveis × 3 faixas etárias × CAP) cobre o cruzamento subgrupo×CAP em série temporal.
6c. IBGE SIDRA: `carrega_sidra_longo(caminho, coluna_corte)` lê as 9 tabelas de `dados_locais/ibge_sidra/` (Censo 2022 e frequência escolar, sempre nível município, sem recorte sub-municipal) e normaliza para formato longo (`idade`, corte de raça/sexo, `valor`); tabelas largas em `tabelas_finais/` e gráficos de barra agrupada por idade × raça/sexo em `visualizacoes/`.
7.  Padronização: nomes de saída e colunas agregadas seguem o padrão `*_anual` e campos de taxa usam nomes descritivos (ex.: `taxa_mortalidade_precoce`). Saídas finais CSV/Excel são escritas em `tabelas_finais/`.
8.  Junção final: múltiplas tabelas DATASUS por bairro são unidas (merge outer) em `dados_datasus_por_bairro.xlsx` (`mapas/tabelas_bairros/`).
8b. Mapas por bairro (cobertura completa): todo indicador com granularidade de bairro -- CadÚnico (via `junta_codbairro_por_bairro`, que resolve nomes de bairro do CadÚnico sem correspondência direta na lista oficial de 166), nascidos vivos, baixo peso, óbitos por raça (coluna total agregada), mortalidade neonatal (precoce/tardia/pós-neonatal/total), óbitos gravidez/puerpério -- gera par `tabelas_finais/tabela_mapa_*.csv` + `mapas/mapa_*.png` (absoluto e, onde já existe denominador, taxa/percentual) para o ano mais recente disponível.
9.  Visualizações: geração de séries temporais e gráficos de barras em `visualizacoes/`, com nomes de arquivo PNG que refletem a seção/tema da análise; exportação adicional em SVG fica disponível (comentada) em cada função de gráfico.

## Como Executar
1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:ipp-dados/analise_primeira_infancia.git
    cd analise_primeira_infancia
    ```
2.  **Crie e ative um ambiente virtual** (recomendado).
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure as variáveis de ambiente**: Crie um arquivo `.env` na raiz do projeto com as credenciais do banco de dados, seguindo o exemplo de `connect_db_ctpe` em `analise.py`.
5.  **Adicione os dados**: Baixe os arquivos de dados do Google Drive e coloque-os na pasta `dados_locais/`.
6.  **Execute a análise**: Utilize o Jupytext para abrir o `analise.py` como um notebook em seu ambiente Jupyter.

## Usando Jupytext
1. Instale `jupytext` em seu ambiente (está em `requirements.txt`).
2. Rode `jupytext --to notebook analise.py` para criar seu `analise.ipynb` ou atualizá-lo a partir do `.py`.
3. Realize as alterações no notebook localmente.
4. Rode `jupytext --sync analise.py` para sincronizar as alterações do notebook de volta no `.py`.
5. Dê commit nas alterações do arquivo `.py`.

## Changelog

Histórico completo em [`CHANGELOG.md`](CHANGELOG.md). Últimas mudanças:

| Versão | Data | Resumo |
| :--- | :--- | :--- |
| 0.19.1 | 2026-09-22 | Revertido o rename de `relatorio/index.html` para `relatorio/relatorio.html` (0.19.0) — de volta a `index.html`. |
| 0.19.0 | 2026-09-22 | Relatório/mapas/tabelas regenerados de verdade; `relatorio/index.html` renomeado para `relatorio/relatorio.html` (deploy continua publicando como `index.html`); primeiro deploy de teste no GitHub Pages; README reestruturado. |
| 0.18.0 | 2026-09-22 | `dados_locais/` reorganizado por tema; convenção de nomes de `tabelas_finais/`/`visualizacoes/`/`mapas/` documentada em `specs/tech-stack.md`. |
| 0.17.0 | 2026-09-22 | Merge da curadoria de `analise.py` da Waleska Marques: bug de agregação do Censo corrigido, ~15 visualizações redundantes removidas. |
| 0.16.0 | 2026-09-09 | Identidade visual unificada; `relatorio/index.html` consolidado num único gerador. |
