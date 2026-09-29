# Análise da Primeira Infância Carioca

Pipeline de dados e relatório sobre a primeira infância (0 a 6 anos) no município do
Rio de Janeiro, produzido pelo **Instituto Pereira Passos (IPP)**, Prefeitura da Cidade
do Rio de Janeiro. Reúne indicadores de população, assistência social, saúde e educação
espalhados por fontes diferentes — Censo, CadÚnico, DataSUS/Tabnet, SINAN, SISVAN, PNAD, Censo
Escolar, IPS — em um único pipeline (`analise.py` + pacote `primeira_infancia/`) que limpa, cruza e
visualiza os dados por bairro, Área e Região de Planejamento, Região Administrativa e Área Programática
de Saúde, organizados em um panorama (população e nascimentos) e nos 7 eixos da política municipal de primeira infância.

📘 **Especificação funcional e técnica do projeto** (o que entrega, dados, arquitetura, regras, processos):
[`docs/especificacao_projeto.md`](docs/especificacao_projeto.md).

> ⚠️ **Repositório e relatório em desenvolvimento.** O conteúdo, os dados e a estrutura
> ainda podem mudar — ver o aviso no próprio relatório publicado.

## 🔗 Relatório

| | |
|---|---|
| **Site (relatório interativo)** | [ipp-dados.github.io/analise_primeira_infancia](https://ipp-dados.github.io/analise_primeira_infancia/) |
| **Relatório em PDF** | [`relatorio/analise_primeira_infancia.pdf`](relatorio/analise_primeira_infancia.pdf) |
| **Apresentação (30 slides)** | [`apresentacao/apresentacao_primeira_infancia.pptx`](apresentacao/apresentacao_primeira_infancia.pptx) · [PDF](apresentacao/apresentacao_primeira_infancia.pdf) — como gerar: [`apresentacao/README.md`](apresentacao/README.md) |
| **Notebook fonte** | [`analise.py`](analise.py) (Jupytext, abre como notebook) |

O site é gerado a partir das saídas do notebook por `website/build/build_site.py` (ver
[`website/README.md`](website/README.md)) — mesmos dados, gráficos interativos (SVG, tooltip,
tabela alternativa, CSV), organizado em abas por eixo da política municipal. O PDF é um relatório
técnico ABNT em LaTeX (`relatorio/latex/`), com as figuras do próprio notebook na versão de impressão e
todas as tabelas no apêndice.

## Fontes de dados

| Fonte | O que traz | Onde |
|---|---|---|
| **CadÚnico** | Famílias/crianças por renda, idade, sexo, raça/cor, arranjo familiar e bairro | Banco CTPE (camada silver, Siurb) — consulta direta, não é arquivo local |
| **DataSUS/Tabnet** | Nascidos vivos, baixo peso, mortalidade (neonatal, por raça/cor, gravidez/puerpério) por bairro | `dados_locais/mortalidade/`, `dados_locais/nascidos_vivos/` |
| **Censo Demográfico** (IBGE/Data.Rio) | População por bairro e idade, 2000/2010/2022 | `dados_locais/censo/` |
| **IBGE SIDRA** | Censo 2022 por raça/sexo e frequência escolar, nível município | `dados_locais/ibge_sidra/` |
| **SISVAN** | Sobrepeso e desnutrição infantil | `dados_locais/sisvan/` |
| **EPI/SVS-Rio** | Cobertura vacinal | `dados_locais/vacinacao/` |
| **PNAD Contínua / Censo Escolar (INEP, microdados)** | Frequência escolar, matrículas 0-5 anos e taxa de atendimento | `dados_locais/educacao/` |
| **Ripsa/Ministério da Saúde** | População por idade e sexo, 2000-2025 (denominador das taxas municipais) | `dados_locais/populacao/` |
| **SINAN (SMS-Rio)** | Notificações de violência familiar e autoprovocada, por bairro | `dados_locais/protecao/` |
| **IPS 2024 (IPP)** | Violência territorial por Região Administrativa | `dados_locais/protecao/` |
| **SIM/SVS-Rio (TabWin)** | Óbitos por causas evitáveis, por Área Programática de Saúde, 2006-2025 | `dados_locais/mortalidade/obitos_causas_evitaveis_primeira_infancia_cap_2006_2025.xlsx` |
| **Data.Rio/IPP, IBGE** | Geometrias de bairro, Área Programática de Saúde, UF e municípios vizinhos | `dados_locais/geo/` |

*OBS: dados brutos completos da versão MVP e do relatório final ficam num Google Drive
compartilhado, acesso restrito — solicitar a leonardoaucar@prefeitura.rio.*

## Estrutura do Projeto
*   `analise.py`: Script principal (sincronizável com Jupytext) que contém extração, limpeza, análise e geração de visualizações; organizado como notebook (células e markdown). Todas as funções de limpeza/wrangling e de visualização ficam no pacote `primeira_infancia/` (um módulo por tema: conexão, limpeza, estilo, gráficos, mapas, variante de impressão, Proteção, CadÚnico, população, educação), importado no topo do notebook.
*   `primeira_infancia/`: funções reutilizáveis do notebook, um módulo por tema (`specs/2026-09-28_organizacao`).
*   `requirements.txt`: dependências diretas, com versões fixadas; `requirements-dev.txt`: só desenvolvimento (Playwright).
*   `dados_locais/`: Diretório para os dados brutos. Uma pasta por fonte/tema (`censo/`, `mortalidade/`, `sisvan/`, `ibge_sidra/`, `vacinacao/`, `nascidos_vivos/`, `educacao/`, `populacao/`, `protecao/`, `geo/`).
*   `dados_locais/geo/`: Camadas geográficas de referência, versionadas no git: `limite_bairros_rio.geojson` (limites de bairro do Rio, Data.Rio/IPP, camada `Cartografia/Limites_administrativos`, geometria simplificada, com as colunas de Área/Região de Planejamento usadas nos mapas agregados), `limite_uf_brasil.geojson` (limites dos estados/UF do Brasil, IBGE), `limite_municipios_rj.geojson` (limites e nomes dos 92 municípios do estado do Rio, IBGE, usados para rotular os municípios vizinhos nos mapas com basemap) e `limite_ap_saude_rio.geojson` (as 10 Coordenadorias de Área Programática de Saúde da SMS-Rio, Data.Rio -- não são as 5 Áreas de Planejamento do IPP acima; coluna `cod_ap_sms`).
*   `dados_locais/tratados/`: Saída intermediária de datasets limpos.
*   `tabelas_finais/`: Pasta de saída padronizada (CSV/Excel) para tabelas e agregados gerados pelo pipeline.
*   `visualizacoes/`: Diretório para os gráficos exportados pelo notebook (PNG por padrão; exportação adicional em SVG disponível, mas comentada, em cada função de gráfico). Nomes de arquivo refletem a seção/tema da análise (ex.: `cobertura_vacinal_epi_ano.png`, `cadunico_criancas_por_idade.png`).
*   `mapas/`: Imagens de mapas coropléticos, gerados dentro do próprio `analise.py` com `geopandas`/`contextily` pela função `mapa_coropletico_bairros`: basemap cartográfico (Esri Ocean Basemap), limite estadual sobreposto, municípios vizinhos rotulados, rosa dos ventos, escala gráfica, título em fonte serifada (Palatino Linotype), formato ~1,46:1 (próximo de A4 paisagem) e exportação a 300 DPI. Cobre hoje o Censo (bairro/AP/RP), mortalidade por causas evitáveis por CAP (grupo e subgrupo), e ~20 mapas por bairro no ano mais recente (CadÚnico, nascidos vivos, baixo peso, óbitos por raça, mortalidade neonatal, óbitos gravidez/puerpério) -- cada um com sua tabela-insumo gêmea em `tabelas_finais/tabela_mapa_*.csv`. `mapas/tabelas_bairros/` é o resquício do padrão anterior (Excel), mantido só para `dados_datasus_por_bairro.xlsx` e as tabelas do Censo (`tabela_mapa_0_4_*.xlsx`); nascidos vivos e baixo peso já migraram para o padrão CSV.
*   `website/`: o site estático publicado no GitHub Pages (HTML/CSS/JS, sem build no deploy) —
    abas por eixo, sumário lateral, gráficos e mapas SVG interativos. `website/build/build_site.py`
    gera `index.html` e `data/`; CSS e JS são editados à mão. Detalhes em
    [`website/README.md`](website/README.md) (inclusive a versão mobile), pendências em
    [`ROADMAP.md`](ROADMAP.md).
*   `relatorio/`: relatório em PDF (`analise_primeira_infancia.pdf`), DOCX de curadoria de textos,
    `controle_revisao.json` (status de revisão de cada texto), `textos_updates_antigos/` (rodadas de
    curadoria devolvidas pelo Google Docs, `curadoria_textos_update_<N>.docx`) e `textos_curados.json`
    (texto curado lido pelo site e pelo PDF); `latex/` (fonte do relatório ABNT e gerador) e `curadoria/`
    (estrutura dos eixos, exportação/sincronização do DOCX, validação dos textos publicados). O antigo
    `relatorio/index.html` foi substituído por `website/` (`specs/2026-09-24_website_refactor`).
*   `ROADMAP.md`: o que está em andamento, a fila priorizada, o backlog por tema e o histórico resumido.
*   `specs/`: Constituição do projeto (`constitution.md`), stack técnica (`tech-stack.md`),
    lista de exclusões (`exclusoes.md`) e uma subpasta por rodada de planejamento (`<AAAA-MM-DD>_<nome>/`, pela data de abertura,
    com `plan.md`, `specification.md`/`specs.md`, `tasks.md`, `validation.md`) -- histórico completo de
    decisões de design, com o *porquê* por trás de convenções do código.
*   `docs/`: especificação funcional e técnica do projeto (`especificacao_projeto.md`).
*   `.env.example`: modelo do `.env` (credenciais do banco do CTPE, usadas só pela seção CadÚnico).
*   `.claude/skills/`: instruções operacionais para o assistente (mapas, site, PDF/curadoria).

Pastas de dados/saída (`dados_locais/`, `tabelas_finais/`, `mapas/`, `visualizacoes/`) mantêm um arquivo `.gitkeep` para preservar a estrutura de pastas no git mesmo quando o conteúdo real (dados brutos sensíveis ou saídas geradas) não é versionado.

## Fluxo de Análise (`analise.py`)
O script `analise.py` realiza as seguintes operações, em ordem prática:
1.  **Pacotes e Funções Auxiliares** (topo do notebook): carregamento de pacotes e `from primeira_infancia import *`, que traz todas as funções reutilizáveis de limpeza/wrangling (`limpeza_tabnet_bairros`, `carrega_raca_bairro`, `carrega_causas_evitaveis_*`, etc.) e de visualização (`serie_temporal`, `grafico_barra*`, `serie_temporal_multipla`). As seções de análise abaixo só chamam essas funções.
2.  Limpeza SISVAN: processamento de arquivos SISVAN (sobrepeso, desnutrição) e salvamento de saídas intermediárias em `dados_locais/tratados/` e finais em `tabelas_finais/`.
3.  Censo: leitura dos microdados do Censo (2022 e outros anos), cálculo de totais e percentuais por bairro/idade e export para `tabelas_finais/censo_por_bairro.csv`.
4.  CadÚnico: extração via CTPE, análise por faixa de renda, idade e bairro, com export em `tabelas_finais/` (ex.: `cadunico_por_faixa_renda_2026.csv`).
5.  DATASUS (Tabnet) — padrão comum: os arquivos Tabnet são normalizados pela função `limpeza_tabnet_bairros(df, categoria)`, que extrai `codigo` e `bairro`, remove linhas 'Total' e harmoniza nomes de colunas.
6.  Para cada tema do DATASUS (nascidos vivos, baixo peso, mortalidade precoce/tardia, óbitos gravidez/puerpério) são geradas séries temporais e agregações anuais. Nas junções entre tabelas, a chave `codigo` (quando disponível) e `bairro`+`ano` são utilizadas para evitar ambiguidades.
6b. Óbitos por causas evitáveis na primeira infância por CAP: `extrai_planilha_evitaveis_cap` lê a planilha TabWin (10 blocos de 12 linhas por aba) e materializa 6 CSVs fiéis à fonte em `dados_locais/tratados/`; `agrega_grupo_cid` deriva o nível grupo a partir dos 8 subgrupos CID; mapas por CAP usam o nível `'cap'` de `mapa_coropletico_bairros` (geometria em `dados_locais/geo/limite_ap_saude_rio.geojson`, coluna `cod_ap_sms` -- não confundir com o nível `'ap'`, as 5 Áreas de Planejamento do IPP). Além do grupo agregado, dois subgrupos específicos (gestação `1.2.1`, parto `1.2.2`) têm mapa e série temporal próprios por CAP, `< 1 ano`; e uma matriz completa (6 subgrupos evitáveis × 3 faixas etárias × CAP) cobre o cruzamento subgrupo×CAP em série temporal.
6c. IBGE SIDRA: `carrega_sidra_longo(caminho, coluna_corte)` lê as 9 tabelas de `dados_locais/ibge_sidra/` (Censo 2022 e frequência escolar, sempre nível município, sem recorte sub-municipal) e normaliza para formato longo (`idade`, corte de raça/sexo, `valor`); tabelas largas em `tabelas_finais/` e gráficos de barra agrupada por idade × raça/sexo em `visualizacoes/`.
7.  Padronização: nomes de saída e colunas agregadas seguem o padrão `*_anual` e campos de taxa usam nomes descritivos (ex.: `taxa_mortalidade_precoce`). Saídas finais CSV/Excel são escritas em `tabelas_finais/`.
8.  Junção final: múltiplas tabelas DATASUS por bairro são unidas (merge outer) em `dados_datasus_por_bairro.xlsx` (`mapas/tabelas_bairros/`).
8a. Proteção: violência familiar (SINAN) por vínculo do provável autor, bairro, CAP e RA, notificações de lesão
    autoprovocada, violência territorial por RA (IPS 2024) e taxas por 1.000 crianças de 0 a 4 anos (Censo 2022).
8b. População de referência e educação: estimativas Ripsa/MS 2000-2025 (denominador de toda taxa municipal) e
    matrículas de 0 a 5 anos a partir dos microdados do Censo Escolar (INEP), com a taxa bruta de atendimento.
8c. Mapas por bairro (cobertura completa): todo indicador com granularidade de bairro -- CadÚnico (via `junta_codbairro_por_bairro`, que resolve nomes de bairro do CadÚnico sem correspondência direta na lista oficial de 166), nascidos vivos, baixo peso, óbitos por raça (coluna total agregada), mortalidade neonatal (precoce/tardia/pós-neonatal/total), óbitos gravidez/puerpério -- gera par `tabelas_finais/tabela_mapa_*.csv` + `mapas/mapa_*.png` (absoluto e, onde já existe denominador, taxa/percentual) para o ano mais recente disponível.
9.  Visualizações: geração de séries temporais e gráficos de barras em `visualizacoes/`, com nomes de arquivo PNG que refletem a seção/tema da análise; exportação adicional em SVG fica disponível (comentada) em cada função de gráfico. Cada gráfico e mapa grava também a versão de impressão usada no PDF (`visualizacoes/a4/`, `mapas/a4/`).

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
4.  **Configure as variáveis de ambiente**: copie `.env.example` para `.env` e preencha as credenciais do banco (lidas por `connect_db_ctpe` em `primeira_infancia/conexao.py`). A seção CadÚnico usa o driver `psycopg` 3 (`requirements.txt`) — o kernel precisa ter esse pacote (no ambiente de desenvolvimento, o conda env `analises_env`; o Python base do Anaconda só tem `psycopg2`).
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
| 0.30.1 | 2026-09-29 | PDF alinhado ao site: ordem de Prioridade, cobertura vacinal de volta, tabelas no corpo da seção, seção vazia fora; quadros de pendente com texto formal no site e no PDF (`specs/2026-09-29_alinhamento_pdf_site`). |
| 0.30.0 | 2026-09-29 | Faixa padrão 0 a 5 anos (até 72 meses) em site, PDF e deck; mapa duplicado, série "Não informada" e gráfico "PNAD" (era o Censo 2022) fora; amarela e indígena só no total; baixo peso com eixo cortado; tablet com alvos de 44 px (`specs/2026-09-29_pendencias`). |
| 0.29.0 | 2026-09-28 | Apresentação de 30 slides para gestores (Marp, gerada de `apresentacao/apresentacao.md` com números calculados das tabelas e variantes por público); mapas dos slides sem distorção por valores extremos (`specs/2026-09-28_apresentacao`). |
| 0.28.0 | 2026-09-28 | Nova estrutura do site e do PDF: panorama da primeira infância (população e nascimentos) na Visão geral e no capítulo de Introdução, 7º eixo "Direito ao Brincar", indicadores reordenados pela planilha da equipe sem remover nenhum conteúdo; nota "agrega os recortes" nas figuras de menores de 5 anos (`specs/2026-09-28_nova_estrutura`). |
| 0.27.1 | 2026-09-28 | Especificação funcional e técnica do projeto (`docs/especificacao_projeto.md`), documentação alinhada ao estado real, `.env.example` (`specs/2026-09-28_documentacao`). |
| 0.27.0 | 2026-09-28 | Funções do notebook no pacote `primeira_infancia/` (um módulo por tema), scripts de curadoria em `relatorio/curadoria/`, requisitos diretos fixados + `requirements-dev.txt`; mesmas saídas antes e depois (`specs/2026-09-28_organizacao`). |
| 0.26.0 | 2026-09-28 | Favicon novo; texto de abertura em cada eixo (site, PDF, DOCX); lorem ≤ 150 palavras; pequenos múltiplos só com Painéis; `index.html` 785 → 343 KB sem mudança visual (`specs/2026-09-28_melhorias_site`). |
| 0.25.1 | 2026-09-28 | Curadoria: update 5 incorporado (7 textos novos no site e no PDF, 2 de figuras fora do relatório guardados como órfãos), controle de revisão recalculado, updates antigos em `relatorio/textos_updates_antigos/` e validação dos textos publicados (`valida_textos_publicados.py`). |
| 0.25.0 | 2026-09-28 | Site com versão mobile (`css/mobile.css`, gráficos redesenhados na largura real, "Nesta seção" recolhível, select para listas longas, legenda do mapa abaixo) sem mudar o desktop; marca d'água "EM DESENVOLVIMENTO" no PDF, ligada à faixa do site por `relatorio/publicacao.json` (`specs/2026-09-28_website_mobile`). |
| 0.24.0 | 2026-09-28 | Rodada de gráficos do site (exclusões, Taxa ↔ Óbitos, unidades, paleta) e correções depois do rollback: cache de CSS/JS versionado, telas estreitas, textos curados ausentes; tabelas de conferência texto × figura (`specs/2026-09-25_website_graficos`, `specs/2026-09-28_website_bugfix`). |
| 0.23.0 | 2026-09-25 | Relatório final em LaTeX/ABNT (capa, resumo, sumário, capítulo por eixo, apêndice de tabelas, Fontes), gerado de `estrutura_eixos.md`; figuras em versão de impressão pelo `analise.py`; lista de exclusões (`specs/2026-09-25_relatorio_latex`, `specs/exclusoes.md`). |
| 0.22.0 | 2026-09-24 | Site reestruturado em `website/` (arquivos separados, abas por eixo, sumário lateral, novo visual, título "Diagnóstico da Primeira Infância Carioca") e 20,9 MB → 1,5 MB (`specs/2026-09-24_website_refactor`). |
| 0.21.0 | 2026-09-24 | População de referência: Ripsa/MS no município (taxas municipais novas) e Censo 2022 explícito abaixo dele; matrículas 0-5 refeitas dos microdados do INEP, com taxa de atendimento; auditoria de faixas etárias e correção do total dos Censos (`specs/2026-09-24_populacao-referencia`). |
| 0.20.0 | 2026-09-23 | CadÚnico: recortes por sexo, raça/cor e arranjo familiar × renda (eixo Inclusão), supressão de células < 20 e correções nas saídas existentes (`specs/2026-09-23_recortes_cadunico`). |
| 0.19.1 | 2026-09-22 | Revertido o rename de `relatorio/index.html` para `relatorio/relatorio.html` (0.19.0) — de volta a `index.html`. |
| 0.19.0 | 2026-09-22 | Relatório/mapas/tabelas regenerados de verdade; `relatorio/index.html` renomeado para `relatorio/relatorio.html` (deploy continua publicando como `index.html`); primeiro deploy de teste no GitHub Pages; README reestruturado. |
| 0.18.0 | 2026-09-22 | `dados_locais/` reorganizado por tema; convenção de nomes de `tabelas_finais/`/`visualizacoes/`/`mapas/` documentada em `specs/tech-stack.md`. |
| 0.17.0 | 2026-09-22 | Merge da curadoria de `analise.py` da Waleska Marques: bug de agregação do Censo corrigido, ~15 visualizações redundantes removidas. |
| 0.16.0 | 2026-09-09 | Identidade visual unificada; `relatorio/index.html` consolidado num único gerador. |
