# Repositório para gestão da análise da primeira infância Carioca

## Fontes de dados:
<p>Cadúnico -> dados armazenados em camada silver em banco CTPE no Siurb (fonte original Data Lake Prefeitura, Assistência Social)</p>
<p>Tabnet municipal -> dados disponíveis em nosso google drive para download, fonte original Datasus, tabnet municipal</p>
<p>Censo 2020/10/00 -> dados disponíveis em nosso google drive para download, fonte original IBGE, DataRio</p>
<p></p>
<i>OBS: listagem dos dados da versão MVP e do relatório final disponíveis no Google Drive.</i>

## Estrutura do Projeto
*   `analise.py`: Script principal (sincronizável com Jupytext) que contém extração, limpeza, análise e geração de visualizações; organizado como notebook (células e markdown).
*   `requirements.txt`: Lista de dependências Python do projeto.
*   `dados_locais/`: Diretório para os dados brutos. Subpastas por fonte (ex.: `nascidos_vivos/`, `mortalidade/`, `sisvan/`, `cadunico/`).
*   `dados_locais/tratados/`: Saída intermediária de datasets limpos.
*   `tabelas_finais/`: Pasta de saída padronizada (CSV/Excel) para tabelas e agregados gerados pelo pipeline.
*   `visualizacoes/`: Diretório para gráficos e imagens exportadas.
*   `notebooks/`: Notebook(s) .ipynb sincronizados com `analise.py` via Jupytext (opcional).
*   `.env.example`: Exemplo de variáveis de ambiente necessárias (ex.: credenciais DB).
*   `scripts/`: Utilitários e conversores auxiliares (se presentes).

## Fluxo de Análise (`analise.py`)
O script `analise.py` realiza as seguintes operações, em ordem prática:
1.  Carregamento de pacotes e leitura de configurações (.env). Define helpers reutilizáveis (limpeza, agregação, gráficos, conexão CTPE).
2.  Limpeza SISVAN: processamento de arquivos SISVAN (sobrepeso, desnutrição) e salvamento de saídas intermediárias em `dados_locais/tratados/` e finais em `tabelas_finais/`.
3.  Censo: leitura dos microdados do Censo (2022 e outros anos), cálculo de totais e percentuais por bairro/idade e export para `tabelas_finais/censo_por_bairro.csv`.
4.  CadÚnico: extração via CTPE, análise por faixa de renda, idade e bairro, com export em `tabelas_finais/` (ex.: `cadunico_por_faixa_etaria_2026.csv`).
5.  DATASUS (Tabnet) — padrão comum: os arquivos Tabnet são normalizados pela função `limpeza_tabnet_bairros(df, categoria)`, que extrai `codigo` e `bairro`, remove linhas 'Total' e harmoniza nomes de colunas.
6.  Para cada tema do DATASUS (nascidos vivos, baixo peso, mortalidade precoce/tardia, óbitos gravidez/puerpério) são geradas séries temporais e agregações anuais. Nas junções entre tabelas, a chave `codigo` (quando disponível) e `bairro`+`ano` são utilizadas para evitar ambiguidades.
7.  Padronização: nomes de saída e colunas agregadas seguem o padrão `*_anual` e campos de taxa usam nomes descritivos (ex.: `taxa_mortalidade_precoce`). Saídas finais CSV/Excel são escritas em `tabelas_finais/`.
8.  Junção final: múltiplas tabelas DATASUS por bairro são unidas (merge outer) em `dados_datasus_por_bairro.xlsx` para facilitar análises espaciais e export para mapas.
9.  Visualizações: geração de séries temporais, gráficos de barras e mapas (quando aplicável) em `visualizacoes/`.

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
