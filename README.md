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
1.  **Carregamento de Pacotes e Funções**: Importa as bibliotecas necessárias e define funções auxiliares para conexão com banco de dados, limpeza de dados e geração de gráficos.
2.  **Limpeza de Dados SISVAN**: Processa os dados brutos do SISVAN sobre sobrepeso e desnutrição, limpando-os e salvando-os na pasta `dados_locais/tratados`.
3.  **Análise do Censo 2022**: Carrega e analisa os dados demográficos do Censo 2022 para a população de 0 a 9 anos.
4.  **Análise do CadÚnico**: Conecta-se ao banco de dados do CTPE, extrai dados de crianças de 0 a 6 anos no CadÚnico e gera gráficos por faixa de renda e idade.
5.  **Análise do DATASUS (Tabnet e SISVAN)**: Processa dados de nascidos vivos, baixo peso ao nascer, desnutrição e sobrepeso para gerar séries temporais e indicadores.

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

## Update Table

| Version | Date       | Description         |
| :------ | :--------- | :------------------ |
| 0.1.0   | 2024-08-12 | Versão inicial com extração e tratamento dos dados|
| 0.2.0   | 2024-13-12 | Primeiro Entregável - visualizações por município |
