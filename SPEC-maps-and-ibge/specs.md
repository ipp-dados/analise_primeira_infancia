# Especificação — Mapas por bairro (cobertura completa), IBGE SIDRA e mortalidade por subgrupo evitável (CAP)

Branch: `spec/maps-and-ibge`
Status: **revisão 1** — primeira versão, para revisão do usuário. Nenhum código novo escrito
ainda (além dos pré-requisitos abaixo, já commitados em `staging_main`).

---

## 0. Pré-requisitos já concluídos (nesta sessão, antes da spec)

1. **Ambiente desta máquina atualizado**: o conda env `analises_env` não tinha as
   dependências geoespaciais (`geopandas`, `contextily`, `shapely`, `pyproj`, `pyogrio`,
   `rasterio`, `mapclassify`, `matplotlib-scalebar`, `affine`, `geopy`, `joblib`,
   `mercantile`, `xyzservices`) usadas pelos mapas coropléticos adicionados em outra
   máquina. Instaladas via `pip install -r requirements.txt`.
2. **`analise.ipynb` sincronizado** a partir de `analise.py` (`jupytext --sync`).
3. **Notebook executado do zero, célula a célula** (`jupyter nbconvert --execute`,
   kernel limpo, sem reaproveitar estado). Isso expôs **dois bugs pré-existentes** (de
   14/08, nunca pegos porque só rodavam bem num kernel reexecutado fora de ordem):
   - `df_bairro.sort_values(by='Primeira Inf. Cadúnico', ...)` referenciava uma coluna
     que só existe em `df_bairro_ate_4` (criada depois, mais abaixo).
   - `df_bairro[df_bairro['bairro']=='Complexo do Alemão']` usava `'bairro'` como coluna,
     quando é o índice do `groupby`.
   Corrigidos e commitados em `staging_main` (`4218c7d`). Notebook agora roda limpo,
   0 erros em 114 células, antes de abrir este branch.

Este item não faz parte do escopo de entrega abaixo — é só o estado de partida.

---

## 1. Objetivo

Quatro frentes de trabalho, cada uma detalhada em sua própria seção:

- **A.** Todo dado do projeto com granularidade de bairro passa a ter, seguindo o padrão
  estabelecido pelo trabalho mais recente (mortalidade por CAP): uma tabela `.csv` que é o
  insumo literal do mapa, e o `.png` do mapa coroplético em si.
- **B.** Importar e visualizar os dados do IBGE SIDRA já baixados em
  `dados_locais/IBGE SIDRA/` (Censo 2022 por idade/sexo/raça; frequência escolar 0-6 anos).
- **C.** Dois mapas novos de mortalidade, por **subgrupo** de causa evitável (não o grupo
  agregado já mapeado), no ano mais recente e na menor granularidade geográfica disponível
  para essa fonte (CAP de Saúde).
- **D.** Séries temporais de mortalidade por subgrupo evitável: painel municipal por
  subgrupo, e cada subgrupo desagregado por CAP.

E, ao final, uma **reorganização de `analise.py`/notebook** detalhando onde cada entrega
entra e em que ordem.

---

## 2. Componente A — Mapas por bairro (cobertura completa)

### 2.1 Inventário: todo dado com granularidade de bairro hoje em `analise.py`

| Dataset (`df`) | Seção do notebook | Chave de bairro | Export atual | Mapa PNG atual | Dimensão temporal | Colunas abs./% |
|---|---|---|---|---|---|---|
| `df_censo` (Censo 0-4) | 🏘️ Censo 2022 | `codbairro` | `tabelas_finais/censo_por_bairro.csv` | **Sim** — 6 PNGs (bairro/AP/RP × absoluto/percentual) | Censo 2022 (foto única) | abs `0 a 4 anos` (bins); % `Percentual 0 a 4` (contínua) — **padrão de referência** |
| `df_bairro` (CadÚnico, todas idades) | Análise por bairros (CadÚnico) | nome do bairro (índice; sem `codbairro`/`codigo`) | `tabelas_finais/cadunico_por_bairro_2026.csv` | Não | Extração atual (foto única) | abs `Crianças`, `Famílias`; sem % neste nível |
| `df_bairro_ate_4` (CadÚnico 0-4) | idem | nome do bairro (mesclado ao `df_censo` por nome) | ⚠️ **mesmo nome de arquivo do `df_bairro`** (`cadunico_por_bairro_2026.csv`) — a segunda escrita sobrescreve a primeira; bug real, ver §2.3 | Não | Extração atual | abs `Crianças`; % `Primeira Inf. Cadúnico` (contínua) |
| `df_vivos` (nascidos vivos) | Nascidos Vivos | `codigo` | Só recorte 2025, em **Excel** legado (`mapas/tabelas_bairros/mapa_bairros_nascidos_vivos_bruto.xlsx`) | Não | 2006-2025, `ano=='2025'` selecionável | abs `nascidos vivos` |
| `df_baixo_peso` | Nascidos abaixo peso | `codigo` | Recorte 2025, Excel legado (`mapa_bairros_nascidos_abaixo_peso.xlsx`) | Não | 2006-2025, 2025 selecionável | abs `nascidos abaixo peso`; % `percentual abaixo do peso` |
| `df_mortalidade_raca_bairro` | Óbitos até 1 ano por raça/cor | `codigo` | `dados_locais/tratados/mortalidade_raca_bairro_ano.csv` (não em `tabelas_finais/`) | Não | 2006-2025 (nascidos desde 2011), 2025 selecionável | abs `obitos_<raça>` ×6; % `percentual_<raça>` ×6 |
| `df_neonatal_precoce` | Mortalidade Neonatal → Precoce | `codigo` | Só agregado município (`mortalidade_neonatal_precoce_por_ano.csv`); **sem export por bairro** | Não | 2006-2025, 2025 selecionável | taxa `taxa_mortalidade_precoce` (contínua) |
| `df_neonatal_tardia` | → Tardia | `codigo` | idem gap, só município | Não | idem | taxa `taxa_obitos_tardios` |
| `df_mortalidade_infantil` | → Pós-neonatal/Total | `codigo` | idem gap, só município (`mortalidade_infantil_pos_neonatal_total_por_ano.csv`) | Não | 2006-2025, 2025 selecionável | abs `obitos_0_364`/`obitos_28_364`; taxa `taxa_mortalidade_infantil`/`taxa_mortalidade_pos_neonatal` |
| `df_obitos_gravidez`, `df_obitos_puerperio` | 📋 Óbitos gravidez e puerpério | `codigo` | Só agregado município; o frame por bairro existe em memória (usado no merge de `df_final`) mas nunca é exportado | Não | 2006-2025, 2025 selecionável | abs apenas — **contagens por bairro tendem a ser muito pequenas/esparsas**, precisa nota de cautela |
| `df_final` (dados_datasus_por_bairro) | Junção de tabelas por bairro | `codigo` | `mapas/tabelas_bairros/dados_datasus_por_bairro.xlsx` | Não (é a junção; cada métrica já está na lista acima) | Multi-indicador, 2006-2025 | — |

**Confirmadamente fora do escopo (só município, sem versão por bairro):** SISVAN
(sobrepeso/desnutrição), Cobertura Vacinal EPI, causas evitáveis "segundo causas"
(grupo/subgrupo, recortes 0-6/7-27/28-364 dias), causas evitáveis por raça/cor (a própria
nota do notebook, linha 1111, já registra essa limitação), causas evitáveis por CAP (10
unidades, granularidade diferente — já mapeada, ver Componentes C/D), IBGE SIDRA (município
único, ver Componente B), PNAD frequência escolar, matrículas.

### 2.2 Padrão de entrega proposto

Seguindo o padrão do trabalho de mortalidade por CAP (não o padrão antigo em Excel dentro de
`mapas/tabelas_bairros/`), cada indicador acima passa a gerar, para o **ano mais recente
disponível** (2025 nos casos DataSUS/Tabnet; Censo 2022 permanece como está):

- `tabelas_finais/tabela_mapa_<indicador>_<ano>.csv` — a tabela literal usada como `df` na
  chamada de `mapa_coropletico_bairros` (uma linha por bairro, chave `codigo`/`codbairro` +
  as colunas absoluta(s) e percentual(is) plotadas).
- `mapas/mapa_<indicador>_<ano>.png` — o mapa em si, via `mapa_coropletico_bairros`
  (`nivel='bairro'`, absoluto sempre com `bins`, percentual sempre contínuo — convenção já
  fixa do projeto).

Isso significa **migrar o padrão de saída de Excel/`mapas/tabelas_bairros/` para
CSV/`tabelas_finais/`** para os indicadores que ainda usam o padrão antigo (nascidos vivos,
baixo peso) — decisão a confirmar, ver §7.F.

### 2.3 Bugs/lacunas que este componente precisa resolver primeiro

Achados ao montar o inventário acima (não são deste branch originalmente, mas bloqueiam a
entrega pedida):

1. **Sobrescrita silenciosa**: `df_bairro.to_csv('tabelas_finais/cadunico_por_bairro_2026.csv')`
   (linha 888) e `df_bairro_ate_4.to_csv(...)` mesmo caminho (linha 901) — a segunda apaga a
   primeira. Corrigir com nomes distintos (ex.: `cadunico_por_bairro_2026.csv` /
   `cadunico_por_bairro_ate_4_2026.csv`).
2. **Exports por bairro faltando** para `df_neonatal_precoce`, `df_neonatal_tardia`,
   `df_mortalidade_infantil`, `df_obitos_gravidez`, `df_obitos_puerperio` — hoje só saem
   agregados por município; para gerar `tabela_mapa_*_2025.csv` é preciso adicionar o export
   por bairro (não precisa mexer no agregado município existente).
3. `df_mortalidade_raca_bairro` não tem export em `tabelas_finais/` (só
   `dados_locais/tratados/`) — adicionar, alinhando com o padrão das outras tabelas finais.

### 2.4 Sobre CadÚnico (`df_bairro`/`df_bairro_ate_4`)

Único caso sem `codigo`/`codbairro` nativo — a chave é o nome do bairro. Para mapear, seguir
a recomendação da skill `generate_map`: juntar por nome normalizado contra
`tabelas_finais/censo_por_bairro.csv` (que já tem `codbairro`), confirmar as 166
correspondências, e carregar `codbairro` adiante — nunca inventar um join fuzzy solto.

---

## 3. Componente B — IBGE SIDRA (importação e visualização)

### 3.1 Fonte dos dados

`dados_locais/IBGE SIDRA/` (adicionado em `f48e1b1`, ainda não lido por `analise.py`):

| Pasta/arquivo | Tabela SIDRA | Conteúdo | Nível territorial | Ano |
|---|---|---|---|---|
| `Censo/tabela9606_populacao_geral.csv` | 9606 | População residente por idade (0-6 + total) | Município (linha única: Rio de Janeiro) | 2022 |
| `Censo/tabela9606_populacao_raca_cor.csv` | 9606 | idem, desagregado por cor/raça (Branca/Preta/Amarela/Parda/Indígena) | idem | 2022 |
| `Censo/tabela9606_populacao_sexo.csv` | 9606 | idem, desagregado por sexo | idem | 2022 |
| `Educacao_freq_escolar_ate5/tabela10057_*.csv` (3 arquivos: geral/raça/sexo) | 10057 | Nº de pessoas até 5 anos que frequentavam escola/creche, por idade (0-5 + total) | idem | 2022 |
| `Educacao_freq_escolar_ate6/tabela10056_*.csv` (3 arquivos: geral/raça/sexo) | 10056 | Taxa de frequência escolar bruta (%), por idade (0-6 + total) | idem | 2022 |

**Observação central**: todas as 9 tabelas trazem **uma única linha de município** (Rio de
Janeiro, código `3304557`) — não há recorte por bairro, AP, RP ou CAP nessas exportações do
SIDRA. Portanto **não se aplica** o Componente A (map_table.csv/map.png) a esses dados — a
visualização é por gráfico de barras/comparativo (idade × raça, idade × sexo), como já é
feito hoje para outras fontes só-município do projeto (ex. cobertura vacinal, SISVAN).

### 3.2 Entregas propostas

- Funções de leitura em **Limpeza e wrangling de dados**: um único parser reutilizável para
  o formato longo do SIDRA (colunas fixas `Município`, `Variável`, `Ano`, mais uma dimensão
  de corte — idade/raça/sexo —, `Valor`), já que as 9 tabelas compartilham o mesmo layout de
  export.
- Tabelas tratadas em `tabelas_finais/`:
  - `censo_sidra_populacao_0_6_raca_2022.csv` (largo: idade × raça)
  - `censo_sidra_populacao_0_6_sexo_2022.csv`
  - `sidra_frequencia_escola_0_5_raca_2022.csv` (contagem absoluta, tabela 10057)
  - `sidra_frequencia_escola_0_5_sexo_2022.csv`
  - `sidra_taxa_frequencia_0_6_raca_2022.csv` (taxa %, tabela 10056)
  - `sidra_taxa_frequencia_0_6_sexo_2022.csv`
- Visualizações em `visualizacoes/`: gráficos de barra agrupada (`grafico_barra_agrupado`,
  já existente) — população por idade × raça/sexo; taxa de frequência escolar por idade ×
  raça/sexo. Sem série temporal (um único ano de Censo).
- Local no notebook: ver §6 (reorganização).

---

## 4. Componente C — Mapas de mortalidade por subgrupo evitável (CAP, ano mais recente)

Pedido específico: mapas para os subgrupos `1.2.1. Red por at à mulher na gestação` e
`1.2.2. Red por at à mulher no parto` (rótulos canônicos já normalizados em
`_ROTULO_PARA_SUBGRUPO`, `analise.py` linhas 173-182), no ano mais recente (2025), na menor
granularidade geográfica disponível para essa fonte — CAP de Saúde (10 unidades; a planilha
TabWin não desce a bairro, ver `SPEC-mortalidade-AP/specification.md` §7).

**Diferença em relação aos 6 mapas de CAP já existentes**: aqueles mapeiam o **grupo** `1.
Causas evitáveis` (soma dos 6 subgrupos `1.1`-`1.4`). Estes dois novos mapas são por
**subgrupo individual**, um recorte mais fino que ainda não existe.

Dado já disponível sem processamento novo: `df_evitaveis_cap_faixa` (`cod_ap_sms, causa,
ano, obitos, faixa_etaria` — variável monta em `analise.py` linha 1477) já tem os 8
subgrupos por CAP/ano/faixa etária; basta filtrar `causa` == rótulo canônico do subgrupo e
`ano == 2025`.

**Entregas propostas** (2 mapas, um por subgrupo):

| arquivo | subgrupo | valor | escala |
|---|---|---|---|
| `mapa_obitos_evitaveis_gestacao_cap_2025.png` | `1.2.1. Red por at à mulher na gestação` | óbitos absolutos | discreta (bins a definir pela distribuição real de 2025) |
| `mapa_obitos_evitaveis_parto_cap_2025.png` | `1.2.2. Red por at à mulher no parto` | óbitos absolutos | discreta |

Mais os `tabela_mapa_*.csv` correspondentes, no mesmo padrão do Componente A.

---

## 5. Componente D — Séries temporais dos subgrupos evitáveis

Dois recortes distintos, ambos pedidos:

### 5.1 Painel municipal, granularidade de subgrupo

Já existe **parcialmente**: `obitos_evitaveis_menores_5_subgrupo_ano.png` (linha 1442),
série de 8 subgrupos, mas **só para a faixa `< 5 anos`** — não existe para `< 1 ano` nem
`1-4 anos`. Proposta: gerar a mesma série para as 3 faixas etárias (usando os 3 CSVs por
faixa já extraídos em `dados_locais/tratados/obitos_evitaveis_<faixa>_causa_cap_2006_2025.csv`,
agregados a município somando as 10 CAPs), mantendo o padrão de nome
`obitos_evitaveis_<faixa>_subgrupo_ano.png`.

### 5.2 Cada subgrupo evitável, desagregado por CAP

Este cruzamento (subgrupo × CAP) foi **explicitamente marcado fora de escopo** na spec
anterior (`SPEC-mortalidade-AP/specification.md` §5.4: *"Cruzamento AP × subgrupo CID (10 ×
8 = 80 séries) fica fora do escopo"*) — este branch reintroduz esse pedido, agora restrito
aos subgrupos de causas **evitáveis** (grupo `1.`, os 6 subgrupos `1.1`-`1.4`), não os 8
completos (excluindo `2. Causas mal definidas` e `3. Demais causas`).

Proposta: 6 gráficos (`serie_temporal_multipla`, uma linha por CAP, 10 séries — mesmo padrão
já usado nas séries de grupo por CAP), um por subgrupo, faixa `< 5 anos` (a mais robusta
numericamente — `1-4 anos` já tem nota no notebook sobre instabilidade por contagens muito
baixas, §7.E trata disso).

Nomenclatura proposta: `obitos_evitaveis_<slug-subgrupo>_cap_menores_5_anos_ano.png`, ex.
`obitos_evitaveis_imunizacao_cap_menores_5_anos_ano.png`,
`obitos_evitaveis_gestacao_cap_menores_5_anos_ano.png`, etc.

---

## 6. Reorganização de `analise.py`/notebook

Sem reordenar o notebook inteiro — inserir cada entrega nova ao lado do bloco temático mais
próximo, mesmo princípio já usado nas seções existentes (análise só chama funções definidas
no topo; funções de limpeza/visualização centralizadas em **Pacotes e Funções Auxiliares**).

Novas seções propostas (nome da seção existente → o que entra):

- **🏘️ Censo 2022** → novo `#### 👶 População 0-6 por idade/raça/sexo (IBGE SIDRA, 2022)`,
  logo após a seção `Por bairro` e antes de `🗺️ Mapa coroplético (bairros)` (Componente B,
  parte Censo).
- **Nascidos Vivos**, **Nascidos abaixo peso**, **Óbitos até 1 ano por raça/cor**, **📋
  Óbitos gravidez e puerpério**, **🩺 Mortalidade Neonatal** (cada uma das 4 subseções:
  Precoce/Tardia/Pós-neonatal/Total) → cada uma ganha, ao final, um
  `##### 🗺️ Mapa coroplético (bairro, 2025)` (Componente A).
- **📉 Mortalidade → Óbitos por causas evitáveis na primeira infância, por CAP**:
  - `###### Panorama municipal` passa a gerar as 3 faixas etárias, não só `< 5 anos`
    (Componente D.1).
  - Novo `###### Por subgrupo e CAP — séries temporais` entre `Por CAP e faixa etária` e
    `🗺️ Mapas por CAP (2025)` (Componente D.2).
  - `###### 🗺️ Mapas por CAP (2025)` ganha um novo bloco `Mapas por subgrupo` após os 6
    mapas de grupo já existentes (Componente C).
- **🎓 PNAD Contínua, Censo Escolar e INEP** → novo
  `#### Frequência escolar 0-6 anos (IBGE SIDRA, Censo 2022)`, antes de `Taxa de frequência
  escolar` (PNAD) — como um comparativo mais recente/granular por idade simples, com nota
  explicando a diferença metodológica (Censo vs. PNAD Contínua, a segunda é amostral e
  estadual/nacional).
- **Junção de tabelas por bairro** (`df_final`) → nota atualizando a lista de "não incluídos"
  (hoje já corretamente exclui raça/causas evitáveis/vacinação; permanece assim, já que os
  novos mapas do Componente A usam suas próprias tabelas, não entram no merge geral).

---

## 7. Situação das decisões — abertas para revisão do usuário

| # | questão | proposta desta spec | impacto se ficar sem resposta |
|---|---|---|---|
| A | Faixa etária dos 2 mapas de subgrupo (Componente C) | `< 1 ano` (causas ligadas a gestação/parto concentram-se no período perinatal) | sem decisão, uso `< 1 ano` como padrão |
| B | Escala dos 2 mapas de subgrupo | só absoluto (bins); percentual por CAP tende a ser muito instável nessas contagens baixas — mesma nota já registrada para `1-4 anos` no notebook atual | sem decisão, só absoluto |
| C | Painel municipal por subgrupo (D.1): expandir para as 3 faixas etárias? | sim | sem decisão, mantenho só `< 5 anos` (como já está) |
| D | Séries subgrupo × CAP (D.2): os 6 subgrupos "evitáveis" (1.1-1.4) ou só os 2 do Componente C? | os 6 (mais consistente com "os subgrupos evitáveis", plural) | sem decisão, faço só os 2 mencionados nominalmente |
| E | Faixa etária das séries subgrupo × CAP (D.2) | `< 5 anos` (mais robusta numericamente) | sem decisão, uso `< 5 anos` |
| F | Padrão de arquivo do Componente A: migrar nascidos vivos/baixo peso do Excel legado (`mapas/tabelas_bairros/*.xlsx`) para CSV em `tabelas_finais/`? | sim, migrar (alinhado ao pedido "seguindo o padrão da última atualização") | sem decisão, mantenho os dois padrões coexistindo (Excel legado + CSV novo) |
| G | Corrigir os bugs/lacunas do §2.3 como parte deste branch? | sim — são pré-requisito direto para gerar os `tabela_mapa_*.csv` pedidos | sem decisão, os mapas de nascidos vivos/baixo peso saem sem a comparação `df_bairro`/CadÚnico corrigida |
| H | Mapas por AP/RP (não só bairro) para os novos indicadores do Componente A? | fora de escopo nesta rodada (fica registrado no `feature_roadmap.md` para depois) | sem decisão, só bairro |
| I | Nome exato dos arquivos `tabela_mapa_*`/`mapa_*` (Componente A) — os nomes na tabela §2.2 são só propostas | usar os nomes propostos, ajustáveis no `plan.md` | sem decisão, sigo com os nomes propostos |

Nenhuma delas bloqueia o início do `plan.md` — todas têm uma proposta padrão assumida acima.

---

## 8. Fora de escopo

- Mapas por AP/RP para os indicadores novos do Componente A (só bairro; ver §7.H).
- Mapas para os dados do IBGE SIDRA (sem granularidade sub-municipal; ver §3.1).
- Atualização de `relatorio/*.html` e do PDF (`skill export_pdf_report`) — pode virar uma
  etapa seguinte, depois que as tabelas/gráficos existirem.
- Cruzamento completo subgrupo × CAP para os 8 subgrupos (só os 6 "evitáveis", grupo `1.`;
  ver §7.D).
- Taxa por mil nascidos vivos por CAP para os mapas de subgrupo (mesma limitação já
  documentada em `SPEC-mortalidade-AP/specification.md` §5.3 — o denominador só existe a
  nível município).
- Educação/Violência e Matrículas 2021-2025 (itens já listados separadamente em
  `feature_roadmap.md`, não fazem parte deste branch).
