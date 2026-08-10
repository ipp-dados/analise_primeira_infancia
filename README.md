# Repositório para gestão da análise da primeira infância Carioca

## Fontes de dados:
<p>Cadúnico -> dados armazenados em camada silver em banco CTPE no Siurb (fonte original Data Lake Prefeitura, Assistência Social)</p>
<p>Tabnet municipal -> dados disponíveis em nosso google drive para download, fonte original Datasus, tabnet municipal</p>
<p>Censo 2020/10/00 -> dados disponíveis em nosso google drive para download, fonte original IBGE, DataRio</p>
<p></p>
<i>OBS: listagem dos dados da versão MVP e do relatório final disponíveis no Google Drive.</i>

## Fluxo
<p>Dados extraídos do banco local para data_frames por script extracao_cadunico.py</p>
<p>Dados salvos em pasta dados_locais carregados para data_frames no notebook</p>
<p>Gráficos e visualizações salvos em pasta visualizacoes</p>

## Usando Jupytext
<ol>Installe 'jupytext' em seu ambiente (está em requirements.txt)</ol>
<ol>rode 'jupytext --to notebook analise.py' para criar seu arquivo .ipynb ou atualiza-lo a partir do arquivo .py</ol>
<ol>realize as alterações no notebook localmente</ol>
<ol>rode 'jupytext --sync analise.py' para sincronizar as alterações do notebook analise.ipynb no arquivo py</ol>
<ol>dê commit nas alterações do arquivo .py</ol>