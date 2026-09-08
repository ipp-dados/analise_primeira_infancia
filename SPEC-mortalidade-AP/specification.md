# Especificação — Óbitos por causas evitáveis na primeira infância, por Área Programática de Saúde (CAP)

Branch: `spec/mortalidade-ap`
Status: **revisão 2** — decisões do usuário incorporadas; nenhum código escrito ainda

> **Restrição do usuário (vale para tudo abaixo): NUNCA alterar código já existente.**
> Nenhuma função, assinatura, constante ou célula atual de `analise.py` é modificada.
> Só se acrescenta código novo. Ver `plan.md` §4 para a consequência de design disso.

---

## 1. Objetivo

Incorporar ao `analise.py` uma nova fonte de dados — a planilha `Óbitos por causas
evitáveis na Primeira Infância.xlsx`, exportada do TabWin/SIM municipal — que traz, pela
primeira vez no projeto, óbitos por **causas evitáveis (CID-10) desagregados por Área
Programática de Saúde (CAP)** e por três faixas etárias da primeira infância.

Até hoje o recorte de causas evitáveis existente no notebook é **só municipal** (arquivos
`obitos_causas_evitaveis_*_segundo_causas_municipio_1996_2025.csv`) e por faixas de dias
(0-6, 7-27, 28-364). Esta planilha é complementar, não substituta:

| | recorte existente | planilha nova |
|---|---|---|
| Granularidade geográfica | município | **10 CAPs (AP de Saúde)** + município |
| Faixa etária | 0-6, 7-27, 28-364 dias (< 1 ano) | **< 1 ano, 1-4 anos, < 5 anos** |
| Período | 1996-2025 | 2006-2025 |
| Causas | grupo / subgrupo / causa (hierarquia completa) | 8 subgrupos + Total |
| Denominador (NV) | por bairro/raça | só município (linha `Nº de NV`) |

Entregas pedidas: CSVs extraídos da planilha, tabelas derivadas, **mapas por CAP para 2025**
e **séries temporais por CAP**, sempre separando `< 1 ano` / `1-4 anos` / `< 5 anos`.

---

## 2. Fonte de dados

### 2.1 Arquivo e renomeação

Nome atual (com acentos, espaços e maiúsculas — fora do padrão do projeto):

```
dados_locais/mortalidade/Óbitos por causas evitáveis na Primeira Infância.xlsx
```

Nome proposto, seguindo a convenção dos demais arquivos de `dados_locais/mortalidade/`
(snake_case, sem acento, recorte + nível geográfico + período):

```
dados_locais/mortalidade/obitos_causas_evitaveis_primeira_infancia_cap_2006_2025.xlsx
```

A renomeação é feita com `git mv`/`mv` (o arquivo ainda é untracked, então é um `mv` simples
seguido de `git add`).

### 2.2 Origem (aba `LOGs`)

A aba `LOGs` documenta as quatro consultas TabWin que geraram a planilha:

- `DEF=C:\Sivitais\tabdow\OBITO2 MRJ.def`, `PATH=c:\sivitais\simw\dados\*.dbf`
- LOG 1 — Linha `CID Evitav INF` × Coluna `Ano do Óbito` (MRJ, < 5 anos)
- LOG 2 — Linha `AP Resid06` × Coluna `Ano do Óbito` (MRJ, < 5 anos)
- LOG 3 — `CID Evitav INF` × ano, `< 1 ano`
- LOG 4 — `CID Evitav INF` × ano, `1 a 4 anos`
- Bases: `DORJOR2006..2024.DBF` + `OCRJ2025_07082026.DBF` + `ORRJ2025_07082026.DBF`;
  1.347.029 registros processados.

**Fonte a citar nos mapas/gráficos:** `SIM/SVS-Rio (TabWin), óbitos de residentes no
município do Rio de Janeiro`. ⚠️ *A confirmar com o usuário o texto institucional exato.*

### 2.3 Estrutura interna da planilha

Cinco abas. Colunas de dados sempre `2006..2025` (colunas 1-20) + `Total` (coluna 21).

**Aba 1 — `Informações gerais`** (município inteiro, < 5 anos). Três tabelas empilhadas:

| linhas | tabela | linha-chave | conteúdo |
|---|---|---|---|
| 0-10 | Óbitos por causa | `CID Evitav INF` | 8 subgrupos CID + `Total` |
| 12-26 | Óbitos por CAP | `AP Resid06` | ` Ign`, 10 CAPs, ` Ignorado`, `Total` |
| 29-33 | Taxa de mortalidade | — | `Nº de óbitos`, `Nº de NV`, `TX` |

**Abas 2-4 — `<1 ano`, `1-4 anos`, `<5 anos`.** Formato idêntico entre si: **10 blocos de
12 linhas**, um por CAP, na ordem `1.0, 2.1, 2.2, 3.1, 3.2, 3.3, 4.0, 5.1, 5.2, 5.3`.
Cada bloco:

```
linha +0 : título  "... , AP 3.1, 2006-2025"      <- carrega o código da CAP
linha +1 : cabeçalho  "CID Evitav INF" | 2006 | ... | 2025 | Total
linha +2..+9 : as 8 categorias CID (sempre as mesmas, nesta ordem)
linha +10: "Total"
linha +11: em branco
```

**Aba 5 — `LOGs`**: metadados da consulta, não vira CSV (só é citada nesta especificação).

### 2.4 As 8 categorias CID (`CID Evitav INF`)

Mesma taxonomia já usada no notebook (Malta et al., lista de causas evitáveis), em rótulos
abreviados pelo TabWin:

| # | rótulo na planilha | grupo |
|---|---|---|
| 1 | `1.1. Reduzível pelas ações de imunização` | 1. Evitáveis |
| 2 | `1.2.1. Red por ad at à mulher na gestação` | 1. Evitáveis |
| 3 | `1.2.2. Red por ad at à mulher no parto` | 1. Evitáveis |
| 4 | `1.2.3. Red por ad at ao recém-nascido` | 1. Evitáveis |
| 5 | `1.3. Red por ações de diag e trat adequado` | 1. Evitáveis |
| 6 | `1.4. Red por ações promoção vinc a atenção` | 1. Evitáveis |
| 7 | `2. Causas mal definidas` | 2. Mal definidas |
| 8 | `3. Demais causas (não claramente evitáveis)` | 3. Demais |

⚠️ Note que a planilha **não traz o nível "grupo"** (`1.`, `2.`, `3.`) como linha própria —
o grupo `1.` é obtido somando as seis linhas `1.*`. Isso difere dos arquivos "segundo
causas" já usados no notebook, onde grupo e subgrupo aparecem como linhas separadas.

### 2.5 Consistências já verificadas na fonte

Verificadas antes de escrever esta spec (script ad-hoc, resultados abaixo):

- ✅ `<5 anos` = `<1 ano` + `1-4 anos` **célula a célula**, para as 10 CAPs, 8 causas e 20 anos
  (0 divergências em 1.600 células).
- ✅ Para cada CAP, o total 2006-2025 dos blocos da aba `<5 anos` bate exatamente com a
  tabela por CAP da aba `Informações gerais` (10 de 10 CAPs).
- ✅ A diferença entre o total municipal (aba 1, 22.949) e a soma das 10 CAPs (22.784) é
  **exatamente** a soma das linhas ` Ign` (82) + ` Ignorado` (83) = 165 óbitos sem CAP de
  residência registrada. Concentra-se no início da série (42 em 2006) e **é zero em 2025**.

Consequência para as entregas: em **2025 os mapas por CAP cobrem 100% dos óbitos** — não há
resíduo "sem CAP". A nota de rodapé sobre CAP ignorada só é necessária nas séries temporais.

---

## 3. Nomenclatura: CAP (decidido)

✅ **Decidido pelo usuário:** trabalhar no nível **CAP** (Coordenadoria de Área Programática
da SMS-Rio), as 10 unidades da planilha.

O termo "AP" já está ocupado no projeto: `analise.py` usa `nivel='ap'` para as **5 Áreas de
Planejamento do IPP** (`area_plane`). Para não criar ambiguidade:

| conceito | 5 unidades | 10 unidades |
|---|---|---|
| nome | Área de Planejamento (IPP) | **Coordenadoria de Área Programática (CAP/SMS)** |
| no código | `nivel='ap'` (existente, **intocado**) | sufixo `_cap` nos nomes de arquivo/variável |
| no geojson | `area_plane` (limite de bairros) | `cod_ap_sms` (arquivo novo, §4) |

Nos títulos de gráficos e mapas: **"Área Programática de Saúde (CAP)"** na primeira menção,
"CAP" depois. Nos nomes de arquivo, sufixo `_cap` (ex.: `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png`).

---

## 4. Geometria oficial das CAPs ✅ obtida

⚠️ **Esta seção substitui integralmente a versão anterior, que derivava as CAPs de um
de-para RA→CAP escrito à mão. Esse de-para tinha dois erros** — ver §4.3.

### 4.1 Fonte

Baixado do portal oficial **Data.Rio / IPP-PCRJ**, dataset *"Áreas Programáticas da Saúde"*
(Áreas Programáticas da Secretaria Municipal de Saúde — AP SMS):

- Página: <https://www.data.rio/datasets/b7b11fe05c984d4c9824c6081fcd57e2_0/about>
- Download: `https://hub.arcgis.com/api/v3/datasets/b7b11fe05c984d4c9824c6081fcd57e2_0/downloads/data?format=geojson&spatialRefId=4326`

Salvo em **`dados_locais/geo/limite_ap_saude_rio.geojson`** (2,57 MB, EPSG:4326, 10 feições).

Tratamento aplicado na gravação (só dados, nenhum código do projeto tocado):
- `make_valid()` — o arquivo original vem com geometrias inválidas (auto-interseções);
- coluna `cod_ap_sms` = `COD_AP_SMS` sem o prefixo `"AP "` → `'1.0'`, `'2.1'`, … `'5.3'`,
  **exatamente os códigos usados na planilha** (join direto, sem normalização);
- coluna `cod_rp` = cópia de `cod_ap_sms` — **alias técnico** exigido pela reutilização da
  função de mapa existente sem alterá-la; a justificativa está em `plan.md` §4;
- descartados `OBJECTID`, `GlobalID`, `Shape__Area`, `Shape__Length` (metadados do ArcGIS).

### 4.2 Conferência contra o limite de bairros

| checagem | resultado |
|---|---|
| Nº de feições | **10**, códigos idênticos aos da planilha |
| Bairros dentro de alguma CAP | **166 de 166**, nenhum órfão |
| RA dividida entre duas CAPs | **nenhuma** — toda CAP é união exata de RAs |
| `total_bounds` × limite de bairros | iguais até a 4ª casa decimal |
| CRS | EPSG:4326 nos dois arquivos |

### 4.3 O que o dado oficial corrigiu

O de-para RA→CAP que eu havia proposto na versão anterior desta spec errava **duas** RAs:

| RA | eu havia proposto | **oficial** | tinha sido sinalizado? |
|---|---|---|---|
| 26 Guaratiba (4 bairros) | 5.3 | **5.2** | sim, marcado como incerto |
| 29 Complexo do Alemão | 3.2 | **3.1** | ❌ **não** — eu tinha como certo |
| 20 Ilha do Governador | 3.1 | 3.1 ✅ | sim, marcado como incerto |

Total: 5 bairros classificados errado. Como o dado da planilha já vem agregado por CAP,
**nenhum número muda** — mas o desenho das fronteiras mudaria, e a CAP 3.1 apareceria menor
do que é. Foi o motivo de buscar a fonte oficial.

### 4.4 De-para RA → CAP (corrigido)

Mantido **como documentação e para uso futuro** (agregar qualquer tabela por bairro/RA até a
CAP), agora derivado do cruzamento espacial com o polígono oficial, não de memória:

| CAP | RAs (código) |
|---|---|
| 1.0 | 1 Portuária, 2 Centro, 3 Rio Comprido, 7 São Cristóvão, 21 Paquetá, 23 Santa Teresa |
| 2.1 | 4 Botafogo, 5 Copacabana, 6 Lagoa, 27 Rocinha |
| 2.2 | 8 Tijuca, 9 Vila Isabel |
| 3.1 | 10 Ramos, 11 Penha, 20 Ilha do Governador, **29 Complexo do Alemão**, 30 Maré, 31 Vigário Geral |
| 3.2 | 12 Inhaúma, 13 Méier, 28 Jacarezinho |
| 3.3 | 14 Irajá, 15 Madureira, 22 Anchieta, 25 Pavuna |
| 4.0 | 16 Jacarepaguá, 24 Barra da Tijuca, 34 Cidade de Deus |
| 5.1 | 17 Bangu, 33 Realengo |
| 5.2 | 18 Campo Grande, **26 Guaratiba** |
| 5.3 | 19 Santa Cruz |

> Nota: as CAPs **não** aninham dentro das Áreas de Planejamento do IPP como eu havia afirmado
> na versão anterior — Guaratiba pertence à Área de Planejamento 5 e à CAP 5.2, o que continua
> coerente, mas a checagem de aninhamento deixou de ser prova de nada e foi retirada da
> validação (`validation.md` V5).

---

## 5. Entregas

### 5.1 CSVs extraídos da planilha (fiéis à fonte, sem cálculo)

Em `dados_locais/tratados/`, nomes em snake_case; formato **longo** (tidy), consistente com
o que as funções de plotagem do notebook consomem:

| arquivo | colunas | linhas |
|---|---|---|
| `obitos_evitaveis_menores_5_causa_municipio_2006_2025.csv` | `causa, ano, obitos` | 8 × 20 = 160 |
| `obitos_evitaveis_menores_5_cap_municipio_2006_2025.csv` | `cod_ap_sms, ano, obitos` | 12 × 20 = 240 |
| `taxa_mortalidade_evitaveis_menores_5_municipio_2006_2025.csv` | `ano, obitos, nascidos_vivos, taxa_por_mil` | 20 |
| `obitos_evitaveis_menores_1_ano_causa_cap_2006_2025.csv` | `cod_ap_sms, causa, ano, obitos` | 10 × 8 × 20 = 1.600 |
| `obitos_evitaveis_1_a_4_anos_causa_cap_2006_2025.csv` | idem | 1.600 |
| `obitos_evitaveis_menores_5_anos_causa_cap_2006_2025.csv` | idem | 1.600 |

Regras de extração:
- linhas `Total` **não** viram registro (são recalculáveis e evitam dupla contagem);
  as linhas ` Ign` / ` Ignorado` da tabela por CAP **são** mantidas, com `cod_ap_sms` normalizado
  para `Ignorado` (as duas somadas), por serem informação real de completude;
- coluna `Total` da planilha descartada (recalculável);
- `ano` como inteiro, `obitos` como inteiro (a fonte não tem `-`, mas o `.replace('-', 0)`
  já usado no projeto é mantido por segurança).

### 5.2 Tabelas derivadas (`dados_locais/tratados/` + `tabelas_finais/`)

| arquivo | conteúdo |
|---|---|
| `mortalidade_evitaveis_cap_faixa_ano.csv` | **tabela mestra**: `cod_ap_sms, faixa_etaria, ano, causa, obitos` — as 3 abas empilhadas |
| `mortalidade_evitaveis_grupo_cap_faixa_ano.csv` | agregado no nível **grupo** (`1.`, `2.`, `3.`), largo por grupo |
| `mortalidade_evitaveis_cap_2025.csv` | recorte 2025: `cod_ap_sms, faixa_etaria, evitaveis, mal_definidas, demais, total, percentual_evitaveis` — é o insumo dos mapas |
| `mortalidade_evitaveis_subgrupo_cap_2025.csv` | recorte 2025 por subgrupo CID, largo (`cod_ap_sms` × 8 causas), por faixa |

### 5.3 Mapas por CAP — ano de 2025 (`mapas/`)

Seguindo a convenção fixa do projeto (skill `generate_map`): **contagem absoluta → classes
discretas**; **percentual → colorbar contínua**. Seis mapas, dois por faixa etária:

| arquivo | valor | escala |
|---|---|---|
| `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | nº de óbitos por causas evitáveis (grupo `1.`) | discreta |
| `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | idem | discreta |
| `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | idem | discreta |
| `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png` | % dos óbitos da AP classificados como evitáveis | contínua |
| `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png` | idem | contínua |
| `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png` | idem | contínua |

Os `bins` das versões absolutas serão definidos **depois de ver a distribuição de 2025**
(faixas diferentes por faixa etária — `1-4 anos` tem contagens uma ordem de grandeza
menores que `< 1 ano`), do mesmo jeito que `niveis_planejamento` já faz hoje.

> **Limitação:** não é possível gerar mapa de **taxa por mil nascidos vivos** por CAP —
> a planilha só traz `Nº de NV` no nível municipal (aba 1, linha 32). Ficaria disponível se
> o usuário exportar do Tabnet os nascidos vivos por CAP de residência. Registrado em
> `tasks.md` como item opcional/bloqueado.

### 5.4 Séries temporais por CAP, 2006-2025 (`visualizacoes/`)

Usando `serie_temporal_multipla` (uma linha por CAP, 10 séries):

| arquivo | conteúdo |
|---|---|
| `obitos_evitaveis_cap_menores_1_ano_ano.png` | óbitos evitáveis (grupo `1.`), `< 1 ano` |
| `obitos_evitaveis_cap_1_a_4_anos_ano.png` | idem, `1-4 anos` |
| `obitos_evitaveis_cap_menores_5_anos_ano.png` | idem, `< 5 anos` |
| `percentual_evitaveis_cap_menores_1_ano_ano.png` | % evitáveis sobre o total de óbitos da AP |
| `percentual_evitaveis_cap_1_a_4_anos_ano.png` | idem |
| `percentual_evitaveis_cap_menores_5_anos_ano.png` | idem |
| `obitos_evitaveis_total_cap_ano.png` | total de óbitos (todas as causas) por CAP, `< 5 anos` |

E, do nível municipal (aba 1), duas séries que hoje não existem no notebook nesse recorte:

| arquivo | conteúdo |
|---|---|
| `obitos_evitaveis_menores_5_subgrupo_ano.png` | 8 subgrupos CID, MRJ, `< 5 anos` |
| `taxa_mortalidade_evitaveis_menores_5_ano.png` | TX por mil NV, MRJ, `< 5 anos` |

> **Nota de legibilidade:** 10 séries num gráfico está acima das 8 cores da paleta categórica
> validada — o mesmo caso já aceito no projeto para cobertura vacinal (11 séries). Mantido,
> apoiado em legenda + tabela CSV correspondente.
>
> ⚠️ Cruzamento **AP × subgrupo CID** (10 × 8 = 80 séries) fica **fora do escopo**: só faz
> sentido como small multiples ou como gráfico por CAP sob demanda. Os dados ficam disponíveis
> em `mortalidade_evitaveis_cap_faixa_ano.csv` para quem quiser.

---

## 6. Onde isso entra no `analise.py`

Seção nova, **dentro de `🏥 DataSus - tabnet` → `📉 Mortalidade`**, depois de
`##### Óbitos por causas evitáveis, por grupo de causa e faixa etária` e antes de
`Mortalidade Neonatal`:

```
##### Óbitos por causas evitáveis na primeira infância, por Área Programática de Saúde (CAP)
###### Panorama municipal (< 5 anos)
###### Por CAP e faixa etária — séries temporais
###### 🗺️ Mapas por CAP (2025)
```

As funções de leitura/limpeza vão para **`### 🧹 Limpeza e wrangling de dados`** (topo do
notebook), e o novo nível `'cap'` para junto de `_NIVEIS_AGREGACAO` em
**`### 📈 Funções de visualização`** — respeitando a regra do projeto de que as seções de
análise só *chamam* funções, nunca as definem.

A extração da planilha → CSVs entra em **`### 🧼 Limpeza de dados prévia`**, ao lado das
duas chamadas `limpa_dados_sisvan(...)` — mesmo padrão de "roda uma vez, materializa CSV".

---

## 7. Fora de escopo

- Recorte por **raça/cor** cruzado com CAP (não existe na planilha).
- Recorte por **bairro** (a planilha para em CAP).
- Taxa por mil NV **por CAP** (falta o denominador — ver 5.3).
- Atualização de `relatorio/*.html` e do PDF (`skill export_pdf_report`) — pode virar um
  segundo passo depois que os gráficos existirem.
- Alteração das seções de causas evitáveis já existentes (0-6/7-27/28-364 dias): permanecem
  como estão, esta é uma seção **adicional**.

---

## 8. Situação das decisões

### ✅ Resolvidas nesta rodada

| # | questão | decisão |
|---|---|---|
| 1 | Nomenclatura `cap` × `ap` | **CAP**, com `nivel='ap'` existente intocado (§3) |
| 2 | Guaratiba / Ilha do Governador | resolvido pelo **dado oficial**: Guaratiba → 5.2, Ilha do Governador → 3.1, Complexo do Alemão → 3.1 (§4.3) |
| 3 | Geometria das CAPs | baixada do Data.Rio, salva em `dados_locais/geo/limite_ap_saude_rio.geojson` (§4.1) |
| 4 | Alterar código existente | **proibido** — ver `plan.md` §4 |

### ⚠️ Ainda em aberto

| # | questão | impacto se ficar sem resposta |
|---|---|---|
| A | **Texto institucional da fonte** para o rodapé dos mapas (§2.2) | uso `SIM/SVS-Rio (TabWin) — óbitos de residentes no município do Rio de Janeiro` |
| B | **Destino dos CSVs extraídos**: `dados_locais/tratados/` (proposto, mesmo destino de `limpa_dados_sisvan`) ou `dados_locais/mortalidade/` | sigo com `tratados/` |
| C | **Nascidos vivos por CAP**: existe export do Tabnet? | sem ele, não há mapa de taxa por mil NV — só contagem absoluta e % de evitáveis (§5.3) |
| D | **Alias `cod_rp` no geojson de CAP** (`plan.md` §4.2): aceitável como está, ou prefere autorizar as 3 linhas em `mapa_coropletico_bairros`? | sigo com o alias, que respeita a restrição de não mudar código |
| E | `SPEC-mortalidade-AP/` entra no commit final? (precedente: `relatorio/specs.md` é versionado) | mantenho versionado |

Nenhuma delas bloqueia o início da implementação — A, B, D e E têm padrão assumido, e C só
adiciona 3 mapas opcionais.
