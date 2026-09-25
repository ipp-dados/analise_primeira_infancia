# Especificação — Mapas por bairro (cobertura completa), IBGE SIDRA e mortalidade por subgrupo evitável

Branch: `spec/maps-and-ibge`
Status: **revisão 2** — decisões do usuário incorporadas (rodada de revisão de `specs.md`
revisão 1). Um item novo segue em aberto (Taxa de Óbitos por raça, §2.5). Nenhum código novo
escrito ainda (além dos pré-requisitos abaixo, já commitados em `staging_main`).

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

Cinco frentes de trabalho, cada uma detalhada em sua própria seção:

- **A.** Todo dado do projeto com granularidade de bairro passa a ter, seguindo o padrão
  estabelecido pelo trabalho mais recente (mortalidade por CAP): uma tabela `.csv` que é o
  insumo literal do mapa, e o `.png` do mapa coroplético em si — **incluindo, agora, uma
  versão de Taxa (não só absoluta) onde já existe denominador** (§2.5).
- **B.** Importar e visualizar os dados do IBGE SIDRA já baixados em
  `dados_locais/IBGE SIDRA/` (Censo 2022 por idade/sexo/raça; frequência escolar 0-6 anos).
- **C.** Dois mapas novos de mortalidade, por **subgrupo** de causa evitável (não o grupo
  agregado já mapeado), na faixa `< 1 ano`, por CAP de Saúde, 2025 — só valor absoluto.
- **D.** Séries temporais de mortalidade por subgrupo evitável: painel municipal por
  subgrupo (3 faixas etárias) e duas variantes por CAP (matriz completa + recorte
  específico).
- **E.** Ajuste nos dois gráficos município-ano de causas evitáveis por raça/cor (0-364
  dias): versão sem a categoria `Não informada` e sem o primeiro ano da série.

E, ao final, uma **reorganização de `analise.py`/notebook** detalhando onde cada entrega
entra e em que ordem.

---

## 2. Componente A — Mapas por bairro (cobertura completa)

### 2.1 Inventário: todo dado com granularidade de bairro hoje em `analise.py`

| Dataset (`df`) | Seção do notebook | Chave de bairro | Export atual | Mapa PNG atual | Dimensão temporal | Colunas abs./% já existentes |
|---|---|---|---|---|---|---|
| `df_censo` (Censo 0-4) | 🏘️ Censo 2022 | `codbairro` | `tabelas_finais/censo_por_bairro.csv` | **Sim** — 6 PNGs (bairro/AP/RP × absoluto/percentual) | Censo 2022 (foto única) | abs `0 a 4 anos` (bins); % `Percentual 0 a 4` (contínua) — **padrão de referência** |
| `df_bairro` (CadÚnico, todas idades) | Análise por bairros (CadÚnico) | nome do bairro (índice; sem `codbairro`/`codigo`) | `tabelas_finais/cadunico_por_bairro_2026.csv` | Não | Extração atual (foto única) | abs `Crianças`, `Famílias`; sem % neste nível |
| `df_bairro_ate_4` (CadÚnico 0-4) | idem | nome do bairro (mesclado ao `df_censo` por nome) | ⚠️ **mesmo nome de arquivo do `df_bairro`** (`cadunico_por_bairro_2026.csv`) — a segunda escrita sobrescreve a primeira; bug real, ver §2.3 | Não | Extração atual | abs `Crianças`; % `Primeira Inf. Cadúnico` (contínua) |
| `df_vivos` (nascidos vivos) | Nascidos Vivos | `codigo` | Só recorte 2025, em **Excel** legado (`mapas/tabelas_bairros/mapa_bairros_nascidos_vivos_bruto.xlsx`) | Não | 2006-2025, `ano=='2025'` selecionável | abs `nascidos vivos` — é o próprio denominador, não gera "taxa" |
| `df_baixo_peso` | Nascidos abaixo peso | `codigo` | Recorte 2025, Excel legado (`mapa_bairros_nascidos_abaixo_peso.xlsx`) | Não | 2006-2025, 2025 selecionável | abs `nascidos abaixo peso`; **já tem** % `percentual abaixo do peso` (vs. nascidos vivos) |
| `df_mortalidade_raca_bairro` | Óbitos até 1 ano por raça/cor | `codigo` | `dados_locais/tratados/mortalidade_raca_bairro_ano.csv` (não em `tabelas_finais/`) | Não | 2006-2025 (nascidos desde 2011), 2025 selecionável | abs `obitos_<raça>` ×6; % `percentual_<raça>` ×6 (por raça); **falta** um total agregado (todas as raças), ver §2.5 |
| `df_neonatal_precoce` | Mortalidade Neonatal → Precoce | `codigo` | Só agregado município (`mortalidade_neonatal_precoce_por_ano.csv`); **sem export por bairro** | Não | 2006-2025, 2025 selecionável | **já tem** taxa `taxa_mortalidade_precoce` (vs. nascidos vivos, contínua) |
| `df_neonatal_tardia` | → Tardia | `codigo` | idem gap, só município | Não | idem | **já tem** taxa `taxa_obitos_tardios` |
| `df_mortalidade_infantil` | → Pós-neonatal/Total | `codigo` | idem gap, só município (`mortalidade_infantil_pos_neonatal_total_por_ano.csv`) | Não | 2006-2025, 2025 selecionável | abs `obitos_0_364`/`obitos_28_364`; **já tem** taxa `taxa_mortalidade_infantil`/`taxa_mortalidade_pos_neonatal` |
| `df_obitos_gravidez`, `df_obitos_puerperio` | 📋 Óbitos gravidez e puerpério | `codigo` | Só agregado município; o frame por bairro existe em memória (usado no merge de `df_final`) mas nunca é exportado | Não | 2006-2025, 2025 selecionável | abs apenas — **contagens por bairro tendem a ser muito pequenas/esparsas**; denominador de taxa não é óbvio (óbito materno, não infantil — ver §2.5) |
| `df_final` (dados_datasus_por_bairro) | Junção de tabelas por bairro | `codigo` | `mapas/tabelas_bairros/dados_datasus_por_bairro.xlsx` | Não (é a junção; cada métrica já está na lista acima) | Multi-indicador, 2006-2025 | — |

**Confirmadamente fora do escopo (só município, sem versão por bairro):** SISVAN
(sobrepeso/desnutrição), Cobertura Vacinal EPI, causas evitáveis "segundo causas"
(grupo/subgrupo, recortes 0-6/7-27/28-364 dias — ver §6, ajuste de raça/cor), causas
evitáveis por CAP (10 unidades, granularidade diferente — já mapeada, ver Componentes C/D),
IBGE SIDRA (município único, ver Componente B), PNAD frequência escolar, matrículas.

### 2.2 Padrão de entrega — ✅ confirmado

Seguindo o padrão do trabalho de mortalidade por CAP (não o padrão antigo em Excel dentro de
`mapas/tabelas_bairros/`), cada indicador acima passa a gerar, para o **ano mais recente
disponível** (2025 nos casos DataSUS/Tabnet; Censo 2022 permanece como está):

- `tabelas_finais/tabela_mapa_<indicador>_<ano>.csv` — a tabela literal usada como `df` na
  chamada de `mapa_coropletico_bairros`.
- `mapas/mapa_<indicador>_<ano>.png` — o mapa em si (absoluto sempre com `bins`, percentual/
  taxa sempre contínuo).

Confirmado: migrar nascidos vivos/baixo peso do padrão Excel/`mapas/tabelas_bairros/` para
CSV/`tabelas_finais/`.

### 2.3 Bugs/lacunas que este componente precisa resolver primeiro

Sem objeção do usuário — seguem como pré-requisito deste branch (bloqueiam a geração dos
mapas pedidos):

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

### 2.5 Novo requisito — Taxa de Óbitos (não só absoluto/percentual) ⚠️ parcialmente em aberto

Pedido do usuário: para os mapas de Componente A, além do valor absoluto, gerar **Taxa de
Óbitos**, com denominador **nascidos vivos** para indicadores de `< 1 ano` e **população**
(Censo) para indicadores de outras faixas etárias.

**O que já está resolvido, sem trabalho novo de denominador:**
- `df_neonatal_precoce`, `df_neonatal_tardia`, `df_mortalidade_infantil` já têm colunas de
  taxa por mil nascidos vivos (todos os indicadores de mortalidade neonatal do projeto são
  `0-364 dias`, ou seja, `< 1 ano` — não existe hoje nenhuma fonte de mortalidade por bairro
  para `1-4 anos`). Os mapas de Componente A para esses três usam essas taxas já calculadas
  como o mapa de escala contínua.
- `df_baixo_peso` já tem `percentual abaixo do peso` (vs. nascidos vivos) — idem.
- `df_mortalidade_raca_bairro` tem taxa por raça, mas **falta um total agregado** (todas as
  raças somadas) — adicionar `obitos_total`/`percentual_total` (óbitos totais ÷ nascidos
  vivos totais, por bairro-ano) para ter uma "taxa de óbitos <1 ano" única no mapa, além das
  6 versões por raça já existentes.

**⚠️ Em aberto — a dicotomia "evitável / não evitável" não existe hoje em nenhuma fonte por
bairro do projeto.** O único arquivo com óbitos por causa evitável desagregados
geograficamente é a planilha TabWin por **CAP** (`specs/2026-09-08_mortalidade-ap`), não por bairro —
`dados_locais/mortalidade/` só tem óbitos **totais** por bairro (`obitos_0_364_dias_bairro_
2006_2025.csv`, sem recorte de causa). Não há, portanto, como calcular "Taxa de óbitos
evitáveis por bairro" vs. "Taxa de óbitos não evitáveis por bairro" com os dados atuais.
Duas leituras possíveis, a confirmar no `plan.md`:
  1. O pedido se refere à mortalidade infantil como um todo (evitável + não evitável já
     somadas, que é exatamente o que `taxa_mortalidade_infantil`/`taxa_obitos_tardios`/
     `taxa_mortalidade_precoce` já representam) — nesse caso, o item já está coberto pelos
     três `df_neonatal_*`/`df_mortalidade_infantil` acima, e "evitável/não evitável" foi só
     uma referência de contexto (à conversa sobre o Componente C), não um novo cruzamento a
     construir.
  2. O pedido é literal e requer uma nova fonte de dados (export do Tabnet com causas
     evitáveis por bairro, se existir) — nesse caso é um item bloqueado até essa fonte
     aparecer, e fica registrado em `feature_roadmap.md` como pendente.
  Esta spec assume a leitura 1 (nenhum dado novo necessário) para efeito de planejamento,
  mas sinaliza explicitamente para confirmação antes do `plan.md` fechar as tarefas.

**`df_obitos_gravidez`/`df_obitos_puerperio` ficam de fora desta rodada de Taxa**: são
óbitos maternos (mulher, durante gravidez/parto), não infantis — nem nascidos vivos nem
população 0-6 anos são um denominador diretamente correto (o denominador apropriado seria
população feminina em idade fértil ou nº de gestações, nenhum disponível por bairro no
projeto hoje). Mantidos só como contagem absoluta, com a nota de cautela sobre números
pequenos já registrada em §2.1.

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
- Local no notebook: ver §7 (reorganização).

---

## 4. Componente C — Mapas de mortalidade por subgrupo evitável (CAP, `< 1 ano`, 2025) — ✅ confirmado

Subgrupos: `1.2.1. Red por at à mulher na gestação` e `1.2.2. Red por at à mulher no parto`
(rótulos canônicos já normalizados em `_ROTULO_PARA_SUBGRUPO`, `analise.py` linhas
173-182). Faixa etária: **`< 1 ano`** (confirmado — causas ligadas a gestação/parto se
concentram no período perinatal). Escala: **só valor absoluto** (confirmado — percentual por
CAP seria muito instável nessas contagens baixas, mesma ressalva já registrada para
`1-4 anos` no notebook atual).

**Diferença em relação aos 6 mapas de CAP já existentes**: aqueles mapeiam o **grupo** `1.
Causas evitáveis` (soma dos 6 subgrupos `1.1`-`1.4`). Estes dois novos mapas são por
**subgrupo individual**, um recorte mais fino que ainda não existe.

Dado já disponível sem processamento novo: `df_evitaveis_cap_faixa` (`cod_ap_sms, causa,
ano, obitos, faixa_etaria` — variável monta em `analise.py` linha 1477) já tem os 8
subgrupos por CAP/ano/faixa etária; basta filtrar `causa` == rótulo canônico do subgrupo,
`faixa_etaria == 'menores de 1 ano'` e `ano == 2025`.

**Entregas** (2 mapas, um por subgrupo):

| arquivo | subgrupo | valor | escala |
|---|---|---|---|
| `mapa_obitos_evitaveis_gestacao_menores_1_ano_cap_2025.png` | `1.2.1. Red por at à mulher na gestação` | óbitos absolutos | discreta (bins a definir pela distribuição real de 2025) |
| `mapa_obitos_evitaveis_parto_menores_1_ano_cap_2025.png` | `1.2.2. Red por at à mulher no parto` | óbitos absolutos | discreta |

Mais os `tabela_mapa_*.csv` correspondentes, no mesmo padrão do Componente A.

---

## 5. Componente D — Séries temporais dos subgrupos evitáveis — ✅ confirmado

### 5.1 Painel municipal, granularidade de subgrupo (3 faixas etárias)

Já existe **parcialmente**: `obitos_evitaveis_menores_5_subgrupo_ano.png` (linha 1442),
série de 8 subgrupos, mas **só para a faixa `< 5 anos`**. Confirmado: gerar a mesma série
para as 3 faixas etárias (`< 1 ano`, `1-4 anos`, `< 5 anos`), usando os 3 CSVs por faixa já
extraídos em `dados_locais/tratados/obitos_evitaveis_<faixa>_causa_cap_2006_2025.csv`,
agregados a município somando as 10 CAPs. Nome de arquivo:
`obitos_evitaveis_<faixa>_subgrupo_ano.png`.

### 5.2 Cada subgrupo evitável, desagregado por CAP — duas variantes

Este cruzamento (subgrupo × CAP) foi **explicitamente marcado fora de escopo** na spec
anterior (`specs/2026-09-08_mortalidade-ap/specification.md` §5.4). Confirmadas **duas** entregas
distintas e complementares:

**D.2a — Matriz completa**: os 6 subgrupos do grupo `1. Causas evitáveis` (`1.1`-`1.4`,
excluindo `2. Causas mal definidas` e `3. Demais causas`), para as **3 faixas etárias**,
cada gráfico com uma linha por CAP (10 séries, `serie_temporal_multipla`, mesmo padrão das
séries de grupo por CAP já existentes). **18 gráficos** (6 subgrupos × 3 faixas). Nome
proposto: `obitos_evitaveis_<slug-subgrupo>_cap_<faixa>_ano.png`.

**D.2b — Recorte específico**: só os 2 subgrupos nominados no Componente C (`1.2.1`,
`1.2.2`), só a faixa **`< 1 ano`**, por CAP — **2 gráficos**, para acompanhar lado a lado os
2 mapas do Componente C (mesmo recorte de dado, em série temporal em vez de foto 2025).
Nome proposto: `obitos_evitaveis_gestacao_cap_menores_1_ano_ano.png` e
`obitos_evitaveis_parto_cap_menores_1_ano_ano.png`.

(D.2b é um subconjunto dos dados de D.2a — não é um cálculo novo, só uma apresentação
separada, publicada junto da seção de mapas do Componente C em vez de junto da matriz
completa.)

---

## 6. Componente E — Ajuste nos gráficos de raça/cor (causas evitáveis, 0-364 dias)

Pedido do usuário, sobre a seção **Óbitos por causas evitáveis por raça/cor** (município-ano,
`analise.py` linha 1105 em diante — note que o código já tem um comentário-lembrete não
implementado, linha 1167: `## retirar 1996 do ano acima e colocar nota de rodapé`).

Criar uma versão adicional de cada um dos dois gráficos, **sem a categoria `nao_informado`**
e **sem o primeiro ano da série** (`1996` — já documentado no notebook, linha 1115, como um
pico isolado de 2.136 óbitos por baixa completude de preenchimento de raça/cor, não um
aumento real):

| gráfico original | nova versão | faixa de anos (nova versão) |
|---|---|---|
| `obitos_causas_evitaveis_raca_ano.png` (`df_evitaveis_raca_municipio`, 1996-2025, 6 raças) | `obitos_causas_evitaveis_raca_sem_nao_informado_ano.png` | 1997-2025, 5 raças (sem `nao_informado`) |
| `percentual_mortalidade_causas_evitaveis_raca_ano.png` (2011-2025, 6 raças) | `percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano.png` | 2011-2025 (já não inclui 1996), 5 raças (sem `nao_informado`) |

Os gráficos originais são mantidos como estão — esta é uma versão adicional, não uma
substituição. `rotulos_raca_evitaveis` (linha 1154) dá origem às duas versões: a nova reusa
o mesmo dicionário menos a chave `'Não informada'`.

---

## 7. Reorganização de `analise.py`/notebook

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
  `##### 🗺️ Mapa coroplético (bairro, 2025)` — absoluto + taxa/percentual quando aplicável
  (Componente A, incluindo §2.5).
- **Óbitos por causas evitáveis por raça/cor** → os dois gráficos do Componente E entram
  logo depois dos dois gráficos originais correspondentes (mesma subseção).
- **📉 Mortalidade → Óbitos por causas evitáveis na primeira infância, por CAP**:
  - `###### Panorama municipal` passa a gerar as 3 faixas etárias, não só `< 5 anos`
    (Componente D.1).
  - Novo `###### Por subgrupo e CAP — séries temporais` entre `Por CAP e faixa etária` e
    `🗺️ Mapas por CAP (2025)`, com a matriz completa (D.2a).
  - `###### 🗺️ Mapas por CAP (2025)` ganha um novo bloco `Mapas por subgrupo (gestação e
    parto, < 1 ano)` após os 6 mapas de grupo já existentes, com os 2 mapas do Componente C
    **e**, logo abaixo, as 2 séries temporais de D.2b (mapa + série lado a lado, mesmo
    recorte de dado).
- **🎓 PNAD Contínua, Censo Escolar e INEP** → novo
  `#### Frequência escolar 0-6 anos (IBGE SIDRA, Censo 2022)`, antes de `Taxa de frequência
  escolar` (PNAD) — como um comparativo mais recente/granular por idade simples, com nota
  explicando a diferença metodológica (Censo vs. PNAD Contínua, a segunda é amostral e
  estadual/nacional).
- **Junção de tabelas por bairro** (`df_final`) → nota atualizando a lista de "não incluídos"
  (hoje já corretamente exclui raça/causas evitáveis/vacinação; permanece assim, já que os
  novos mapas do Componente A usam suas próprias tabelas, não entram no merge geral).

---

## 8. Decisões desta revisão (resolvidas em conversa)

| # | questão | decisão final |
|---|---|---|
| A | Faixa etária dos 2 mapas de subgrupo (Componente C) | **`< 1 ano`** |
| B | Escala dos 2 mapas de subgrupo | **só absoluto** |
| C | Painel municipal por subgrupo (D.1): expandir para as 3 faixas etárias? | **sim** |
| D | Séries subgrupo × CAP (D.2) | **duas variantes**: matriz completa (6 subgrupos × 3 faixas, D.2a) **e** recorte dos 2 subgrupos nominados × `< 1 ano` (D.2b) |
| E | Faixa etária das séries subgrupo × CAP | resolvida junto com D — D.2a cobre as 3 faixas, D.2b só `< 1 ano` |
| F | Padrão de arquivo do Componente A: CSV em `tabelas_finais/` em vez do Excel legado | **sim, migrar** |
| G | Corrigir os bugs/lacunas do §2.3 como parte deste branch? | sem objeção — **sim, corrigir** (pré-requisito direto) |
| H | Mapas por AP/RP para os novos indicadores do Componente A | **fora de escopo, registrado em `feature_roadmap.md`** |
| I | Nome exato dos arquivos `tabela_mapa_*`/`mapa_*` | **usar os nomes propostos** (ajustáveis no `plan.md` se necessário) |
| — | Taxa de Óbitos (novo, Componente A) | **aplica-se ao Componente A** (bairro), não aos mapas de CAP — ver §2.5 para o que já está coberto e o que segue em aberto |
| — | Denominador de Taxa no nível CAP | não se aplica nesta rodada (Taxa é só Componente A/bairro); se algum dia precisar em CAP, agregar dado de bairro existente (nascidos vivos, população Censo) por CAP, mesmo método já usado para AP/RP |
| — | Ajuste raça/cor causas evitáveis (Componente E) | **sim** — versão sem `nao_informado` e sem 1996, para os 2 gráficos citados, mantendo os originais |

### Único item ainda em aberto

**§2.5 — "evitável vs. não evitável" por bairro**: não existe fonte de dados por bairro com
esse recorte de causa hoje no projeto. Esta spec assume que o pedido se refere à mortalidade
infantil como um todo (já coberta pelas taxas de `df_neonatal_precoce`/`df_neonatal_tardia`/
`df_mortalidade_infantil`), não a um cruzamento novo por causa evitável. **Precisa
confirmação antes do `plan.md` fechar as tarefas do Componente A** — se a leitura estiver
errada, é necessário indicar de onde viria o dado de causas evitáveis por bairro.

---

## 9. Fora de escopo

- Mapas por AP/RP para os indicadores novos do Componente A (só bairro; registrado em
  `feature_roadmap.md`, ver §8.H).
- Mapas para os dados do IBGE SIDRA (sem granularidade sub-municipal; ver §3.1).
- Atualização de `relatorio/*.html` e do PDF (`skill export_pdf_report`) — pode virar uma
  etapa seguinte, depois que as tabelas/gráficos existirem.
- Cruzamento subgrupo × CAP para os 8 subgrupos completos (só os 6 "evitáveis", grupo `1.`;
  ver §5.2).
- Taxa por mil nascidos vivos por CAP (mesma limitação já documentada em
  `specs/2026-09-08_mortalidade-ap/specification.md` §5.3 — o denominador só existe a nível município; a
  Taxa deste branch é só Componente A/bairro, ver §8).
- Taxa de óbitos maternos (gravidez/puerpério) por bairro — denominador não é óbvio com os
  dados disponíveis (ver §2.5); mantidos só como contagem absoluta.
- Educação/Violência e Matrículas 2021-2025 (itens já listados separadamente em
  `feature_roadmap.md`, não fazem parte deste branch).
