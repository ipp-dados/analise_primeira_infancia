# Repositório para gestão da análise da primeira infância Carioca

## Fontes de dados:
<p>Cadúnico -> dados armazenados em camada silver em banco CTPE no Siurb (fonte original Data Lake Prefeitura, Assistência Social)</p>
<p>Tabnet municipal -> dados disponíveis em nosso google drive para download, fonte original Datasus, tabnet municipal</p>
<p>Censo 2020/10/00 -> dados disponíveis em nosso google drive para download, fonte original IBGE, DataRio</p>
<p></p>
<i>OBS: listagem dos dados da versão MVP e do relatório final disponíveis no Google Drive.</i>

## Estrutura do Projeto
*   `analise.py`: Script principal (e notebook) que contém toda a lógica de extração, tratamento, análise e visualização dos dados.
*   `requirements.txt`: Lista de dependências Python do projeto.
*   `dados_locais/`: Diretório para armazenar os arquivos de dados brutos (CSVs, Excel).
*   `dados_locais/tratados`: Subdiretório onde os dados limpos são salvos.
*   `visualizacoes/`: Diretório onde os gráficos gerados pela análise são salvos.

## Fluxo de Análise (`analise.py`)
O script `analise.py` realiza as seguintes operações:
1.  **Carregamento de Pacotes e Funções**: Importa as bibliotecas necessárias e define funções auxiliares para conexão com banco de dados, limpeza de dados SISVAN e DATASUS, e geração de gráficos (séries temporais e barras).
2.  **Limpeza de Dados SISVAN**: Processa os dados brutos do SISVAN sobre sobrepeso e desnutrição, limpando-os e salvando-os na pasta `dados_locais/tratados`. Gera arquivos CSV na pasta `tabelas_finais` e visualizações de séries temporais.
3.  **Análise do Censo 2022**: Carrega e analisa os dados demográficos do Censo 2022 para a população de 0 a 9 anos por bairro. Calcula totais e percentuais, salvando os resultados em `tabelas_finais/censo_por_bairro.csv` e arquivos Excel para visualização em mapas.
4.  **Série Temporal do Censo (2000, 2010, 2022)**: Integra dados de diferentes anos do Censo para analisar a evolução da população de 0 a 4 anos.
5.  **Análise do CadÚnico**: Conecta-se ao banco de dados do CTPE, extrai dados de crianças de 0 a 6 anos no CadÚnico. Realiza análises por faixa de renda, idade e bairro, gerando gráficos de barras e salvando tabelas em `tabelas_finais/cadunico_por_faixa_etaria_2026.csv`, `tabelas_finais/cadunico_por_idade_2026.csv` e `tabelas_finais/cadunico_por_bairro_2026.csv`. Calcula o indicador "Primeira Inf. Cadúnico" por bairro.
6.  **Análise do DATASUS (Tabnet)**:
    *   **Nascidos Vivos**: Processa dados de nascidos vivos por ano, gerando uma série temporal e salvando em `tabelas_finais/nascidos_vivos_por_ano.csv`.
    *   **Baixo Peso ao Nascer**: Analisa o percentual de nascidos com baixo peso por ano, gerando uma série temporal e salvando em `tabelas_finais/nascidos_abaixo_peso_por_ano.csv`.
    *   **Mortalidade Neonatal**: Analisa a mortalidade neonatal precoce (0-6 dias) e tardia (7-27 dias), calculando as taxas por ano e gerando séries temporais.
    *   **Mortalidade na Gravidez e Puerpério**: Processa e visualiza o número de óbitos durante a gravidez e o puerpério por ano.
7.  **Análise do DATASUS (SISVAN)**:
    *   **Desnutrição**: Processa dados de desnutrição (peso muito baixo e baixo) por ano, gerando séries temporais e salvando em `tabelas_finais/sisvan_desnutricao_por_ano.csv`.
    *   **Sobrepeso e Obesidade**: Processa dados de sobrepeso e obesidade por ano, gerando séries temporais e salvando em `tabelas_finais/sisvan_sobrepeso_por_ano.csv`.
8.  **Análise de Dados de Educação (PNAD, Censo Escolar)**:
    *   **Frequência Escolar**: Analisa e visualiza a taxa de frequência escolar por idade com base nos dados da PNAD.
    *   **Matrículas**: Analisa a série histórica do número de matrículas de crianças de 0 a 6 anos com base no Censo Escolar.

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

---

## Update Table

| Version | Date       | Description         |
| :------ | :--------- | :------------------ |
| 0.1.0   | 2024-08-12 | Versão inicial com extração e tratamento dos dados|
| 0.2.0   | 2024-13-12 | Primeiro Entregável - visualizações por município |
| 0.3.0   | 2026-08-14 | Análise e visualização abrangente dos dados do Censo, CadÚnico, DATASUS e SISVAN |
| 0.4.0   | 2026-08-17 | Inclusão de análises de mortalidade (neonatal, gravidez, puerpério) e educação (frequência, matrículas). |
| 0.4.1   | 2026-08-19 | Normalização das importações Tabnet (função limpeza_tabnet_bairros), padronização do diretório de saída para `tabelas_finais`, inclusão da chave 'codigo' nas junções, renomeação de variáveis agregadas para '*_anual' e campos de taxa mais descritivos, e junção/exportação final dos dados DataSUS por bairro. |
