# Repositório para gestão da análise da primeira infância Carioca

## Fontes de dados:
<p>Cadúnico -> dados armazenados em camada silver em banco CTPE no Siurb (fonte original Data Lake Prefeitura, Assistência Social)</p>
<p>Tabnet municipal -> dados disponíveis em nosso google drive para download, fonte original Datasus, tabnet municipal</p>
<p>Censo 2020/10/00 -> dados disponíveis em nosso google drive para download, fonte original IBGE, DataRio</p>
<p></p>
<i>OBS: listagem dos dados da versão MVP e do relatório final disponíveis no Google Drive.</i>

## Estrutura do Projeto
*   `analise.py`: Script principal (sincronizável com Jupytext) que contém extração, limpeza, análise e geração de visualizações; organizado como notebook (células e markdown). Todas as funções de limpeza/wrangling e de visualização ficam centralizadas na seção **Pacotes e Funções Auxiliares**, no topo do notebook.
*   `requirements.txt`: Lista de dependências Python do projeto.
*   `dados_locais/`: Diretório para os dados brutos. Subpastas por fonte (ex.: `nascidos_vivos/`, `mortalidade/`, `sisvan/`, `cadunico/`).
*   `dados_locais/tratados/`: Saída intermediária de datasets limpos.
*   `tabelas_finais/`: Pasta de saída padronizada (CSV/Excel) para tabelas e agregados gerados pelo pipeline.
*   `visualizacoes/`: Diretório para os gráficos exportados pelo notebook (PNG por padrão; exportação adicional em SVG disponível, mas comentada, em cada função de gráfico). Nomes de arquivo refletem a seção/tema da análise (ex.: `cobertura_vacinal_epi_ano.png`, `cadunico_criancas_por_idade.png`).
*   `mapas/`: Imagens de mapas (gerados externamente, ex. QGIS) e a subpasta `mapas/tabelas_bairros/`, destino único das tabelas por bairro em Excel usadas para gerar mapas (ex.: `dados_datasus_por_bairro.xlsx`, `mapa_bairros_nascidos_vivos_bruto.xlsx`).
*   `relatorio/`: Páginas HTML autocontidas com os gráficos do notebook renderizados de forma interativa (SVG, tooltip, tabela de dados), para compartilhamento com quem não abre o notebook. Três versões, mesmo conteúdo e mesma ordem de `analise.py`, variando só o tema visual:
    *   `relatorio/index.html`: tema padrão (fundo em tom de pedra, paleta de cores plena nos gráficos).
    *   `relatorio/lighter_index.html`: tema mais claro e paleta pastel nos gráficos, com uma seção adicional de mapas coropléticos por bairro (imagens de `mapas/`, redimensionadas e incorporadas na própria página).
    *   `relatorio/white_index.html`: mesma base do `lighter_index.html`, mas com fundo branco puro e texto em tons de cinza neutro (sem matiz de cor no texto/fundo); os gráficos mantêm a paleta pastel.
*   `notebooks/`: Notebook(s) .ipynb sincronizados com `analise.py` via Jupytext (opcional).
*   `.env.example`: Exemplo de variáveis de ambiente necessárias (ex.: credenciais DB).
*   `scripts/`: Utilitários e conversores auxiliares (se presentes).

Pastas de dados/saída (`dados_locais/`, `tabelas_finais/`, `mapas/`, `visualizacoes/`) mantêm um arquivo `.gitkeep` para preservar a estrutura de pastas no git mesmo quando o conteúdo real (dados brutos sensíveis ou saídas geradas) não é versionado.

## Fluxo de Análise (`analise.py`)
O script `analise.py` realiza as seguintes operações, em ordem prática:
1.  **Pacotes e Funções Auxiliares** (topo do notebook): carregamento de pacotes, leitura de configurações (.env) e definição de todas as funções reutilizáveis de limpeza/wrangling (`limpeza_tabnet_bairros`, `carrega_raca_bairro`, `carrega_causas_evitaveis_*`, etc.) e de visualização (`serie_temporal`, `grafico_barra*`, `serie_temporal_multipla`). As seções de análise abaixo só chamam essas funções.
2.  Limpeza SISVAN: processamento de arquivos SISVAN (sobrepeso, desnutrição) e salvamento de saídas intermediárias em `dados_locais/tratados/` e finais em `tabelas_finais/`.
3.  Censo: leitura dos microdados do Censo (2022 e outros anos), cálculo de totais e percentuais por bairro/idade e export para `tabelas_finais/censo_por_bairro.csv`.
4.  CadÚnico: extração via CTPE, análise por faixa de renda, idade e bairro, com export em `tabelas_finais/` (ex.: `cadunico_por_faixa_etaria_2026.csv`).
5.  DATASUS (Tabnet) — padrão comum: os arquivos Tabnet são normalizados pela função `limpeza_tabnet_bairros(df, categoria)`, que extrai `codigo` e `bairro`, remove linhas 'Total' e harmoniza nomes de colunas.
6.  Para cada tema do DATASUS (nascidos vivos, baixo peso, mortalidade precoce/tardia, óbitos gravidez/puerpério) são geradas séries temporais e agregações anuais. Nas junções entre tabelas, a chave `codigo` (quando disponível) e `bairro`+`ano` são utilizadas para evitar ambiguidades.
7.  Padronização: nomes de saída e colunas agregadas seguem o padrão `*_anual` e campos de taxa usam nomes descritivos (ex.: `taxa_mortalidade_precoce`). Saídas finais CSV/Excel são escritas em `tabelas_finais/`.
8.  Junção final: múltiplas tabelas DATASUS por bairro são unidas (merge outer) em `dados_datasus_por_bairro.xlsx`. Esta e as demais tabelas por bairro em Excel (nascidos vivos, baixo peso, Censo 0-4 anos) são sempre exportadas em `mapas/tabelas_bairros/`, para facilitar análises espaciais e export para mapas.
9.  Visualizações: geração de séries temporais e gráficos de barras em `visualizacoes/`, com nomes de arquivo PNG que refletem a seção/tema da análise; exportação adicional em SVG fica disponível (comentada) em cada função de gráfico.

## Como Executar
1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
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
<ol>
<li>Instale 'jupytext' em seu ambiente (está em requirements.txt)</li>
<li>rode 'jupytext --to notebook analise.py' para criar seu arquivo .ipynb ou atualiza-lo a partir do arquivo .py</li>
<li>realize as alterações no notebook localmente</li>
<li>rode 'jupytext --sync analise.py' para sincronizar as alterações do notebook analise.ipynb no arquivo py</li>
<li>dê commit nas alterações do arquivo .py</li>
</ol>

---

## Recent changes in analise.py

Notable code changes (2026-08-17..2026-08-19):
- Added preprocessing markdown cells and additional data-cleaning steps for clarity in the analysis flow.
- Introduced function limpeza_tabnet_bairros(df, categoria) to standardize Tabnet imports and extract a numeric 'codigo' plus 'bairro'.
- Normalized output folders to lowercase `tabelas_finais` (previously `Tabelas_finais`).
- Updated merges to include the new 'codigo' key, avoided relying on 'Total' rows, and renamed several aggregated variables to '*_anual' and rate columns to descriptive names (e.g., `taxa_mortalidade_precoce`, `taxa_obitos_tardios`).
- Added final join of multiple DataSUS tables per bairro and export to `dados_datasus_por_bairro.xlsx`.

These changes improve consistency of column names, make merges more robust by using 'codigo', and standardize output paths.

Notable code changes (2026-08-25):
- Mortalidade infantil por raça/cor: óbitos até 1 ano por bairro e município, com percentual em relação aos nascidos vivos por raça/cor da mãe.
- Óbitos por causas evitáveis: recortes por raça/cor e por grupo/subgrupo CID-10 (total e nos recortes 0-6, 7-27 e 28-364 dias), com comparativo de subgrupos entre faixas etárias em 2025.
- Mortalidade Neonatal: novas taxas pós-neonatal e total (0-364 dias), derivadas por subtração numa grade bairro x ano com zeros explícitos.
- Cobertura Vacinal EPI: série histórica por imunobiológico e comparativo entre 2016/2019/2022/2025 (novos dados em `dados_locais/vacinacao/`).
- Correção dos caminhos de nascidos_vivos/baixo_peso que apontavam para pasta inexistente, quebrando as taxas Precoce/Tardia e a junção final.
- Exportação para `tabelas_finais/` de todas as tabelas usadas em gráficos, e revisão do markdown do notebook com notas sobre limitações dos dados (ex.: causas evitáveis por raça não filtra apenas o grupo evitável).

Notable code changes (2026-08-26) — reorganização do notebook:
- Todas as funções de limpeza/wrangling (`limpeza_tabnet_bairros`, `carrega_raca_bairro`, `carrega_causas_evitaveis_raca`, `carrega_causas_evitaveis_categoria`, `combina_faixas_causa`, `total_e_percentual_ano`, `carrega_cobertura_vacinal`) e de visualização (`serie_temporal`, `grafico_barra`, `grafico_barra_agrupado`, `serie_temporal_multipla`) foram movidas para a seção **Pacotes e Funções Auxiliares**, no topo do notebook; `combina_faixas_causa` foi generalizada para receber o dicionário de arquivos por faixa como parâmetro.
- Seções do notebook receberam divisórias (`---`) e emojis nos títulos para facilitar a navegação visual; o nível de heading de "Limpeza de dados prévia" foi corrigido (H3, antes pulava de H2 para H4).
- `serie_temporal` e `grafico_barra` passaram a aceitar `nome_arquivo` explícito (como `grafico_barra_agrupado`/`serie_temporal_multipla` já faziam); todos os PNGs exportados em `visualizacoes/` foram renomeados para refletir a seção/tema (ex.: `óbitos-gravidez_ano.png` → `obitos_gravidez_por_ano.png`, `Total_Idade.png` → `pnad_frequencia_escolar_por_idade.png`).
- Exportação em SVG deixou de ser automática: cada função de gráfico agora salva só PNG por padrão, com uma linha `plt.savefig(...svg...)` comentada para habilitar o formato vetorial quando necessário.
- As 5 tabelas por bairro em Excel (`tabela_mapa_0_4_absoluto`, `tabela_mapa_grandes_0_4_percentual`, `mapa_bairros_nascidos_vivos_bruto`, `mapa_bairros_nascidos_abaixo_peso`, `dados_datasus_por_bairro`) passaram a ser sempre exportadas em `mapas/tabelas_bairros/` (antes iam para `tabelas_finais/` ou para a raiz do projeto); uma célula de setup garante que a pasta exista.
- Corrigido resíduo de `Tabelas_finais\` (maiúsculo) em alguns exports de CSV, padronizando para `tabelas_finais\`.
- Os arquivos-dummy usados para manter a estrutura de pastas no git (`exemplo`, `example_file`, `example`) foram renomeados para `.gitkeep`, com as exceções correspondentes adicionadas ao `.gitignore`.

Notable code changes (2026-08-26) — relatório visual em `relatorio/`:
- Novo `relatorio/index.html`: página HTML autocontida (sem dependências externas além da fonte via Google Fonts) que replica `analise.py` seção por seção — mesmos títulos, mesmas notas de markdown, mesma ordem — substituindo os PNGs do matplotlib por gráficos SVG interativos (legenda, tooltip ao passar o mouse, tabela de dados alternativa) construídos a partir das tabelas em `tabelas_finais/`.
- Novo `relatorio/lighter_index.html`: mesma página em tema mais claro e paleta pastel nos gráficos, acrescida de uma seção "Mapas" com os 5 mapas coropléticos de `mapas/` (redimensionados e comprimidos para a página, ~130 KB cada em vez dos ~6 MB originais).
- Ícone da seção SISVAN trocado de ⚖️ para 🥗 (nutrição), refletido também em `analise.py`.
- Nos gráficos de barra do CadÚnico (por faixa de renda e por idade), os valores passaram a ser arredondados e abreviados (ex.: `149.426` → `149 mil`) e o rótulo do valor ganhou uma coluna própria no layout, para nunca ultrapassar a caixa do gráfico.
- Novo `relatorio/white_index.html`: mesma base do `lighter_index.html` (mesmo conteúdo, mesma seção de mapas), mas com fundo branco puro e texto em cinza neutro (sem o matiz esverdeado do tema padrão); os gráficos continuam na paleta pastel.

---

## Update Table

| Version | Date       | Description         |
| :------ | :--------- | :------------------ |
| 0.1.0   | 2024-08-12 | Versão inicial com extração e tratamento dos dados|
| 0.2.0   | 2024-13-12 | Primeiro Entregável - visualizações por município |
| 0.3.0   | 2026-08-14 | Análise e visualização abrangente dos dados do Censo, CadÚnico, DATASUS e SISVAN |
| 0.4.0   | 2026-08-17 | Inclusão de análises de mortalidade (neonatal, gravidez, puerpério) e educação (frequência, matrículas). |
| 0.4.1   | 2026-08-19 | Normalização das importações Tabnet (função limpeza_tabnet_bairros), padronização do diretório de saída para `tabelas_finais`, inclusão da chave 'codigo' nas junções, renomeação de variáveis agregadas para '*_anual' e campos de taxa mais descritivos, e junção/exportação final dos dados DataSUS por bairro. |
| 0.5.0   | 2026-08-25 | Mortalidade infantil por raça/cor, óbitos por causas evitáveis (CID-10, por faixa etária), novas taxas de mortalidade neonatal (pós-neonatal e total), cobertura vacinal EPI (série histórica e comparativo entre anos), correção de caminhos de nascidos_vivos/baixo_peso e exportação padronizada para `tabelas_finais/`. |
| 0.6.0   | 2026-08-26 | Reorganização do notebook: funções de limpeza/wrangling e de visualização centralizadas em Pacotes e Funções Auxiliares, seções com divisórias/emojis para navegação visual, PNGs renomeados por seção/tema, exportação em SVG comentada por padrão, tabelas por bairro em Excel sempre em `mapas/tabelas_bairros/`, e arquivos-dummy de estrutura de pastas trocados por `.gitkeep`. |
| 0.7.0   | 2026-08-26 | Novo relatório visual em `relatorio/`: `index.html` replica `analise.py` seção por seção com gráficos SVG interativos; `lighter_index.html` é a mesma página em tema claro e paleta pastel, com uma seção adicional de mapas coropléticos por bairro. Ícone da seção SISVAN trocado para 🥗; valores dos gráficos de barra do CadÚnico arredondados/abreviados e sempre dentro da caixa do gráfico. |
| 0.8.0   | 2026-08-26 | Novo `relatorio/white_index.html`: mesmo conteúdo do `lighter_index.html`, com fundo branco puro e texto em cinza neutro; gráficos continuam na paleta pastel. |
