# Validação — Mapas por bairro, IBGE SIDRA e mortalidade por subgrupo evitável

Cada checagem tem um **critério de aceite objetivo**. Onde o valor exato não é conhecido
antes de rodar o código real (ex. totais de óbitos por bairro em 2025), o critério é a
propriedade que o resultado precisa satisfazer, não um número fixo — diferente da spec
anterior, aqui a maior parte dos dados-fonte já está em produção havia meses, então o risco
não é "a planilha tem um layout inesperado" (checado uma vez, `V1` da spec anterior), e sim
"a extensão de uma tabela existente introduz uma regressão silenciosa em algo que já
funcionava" — por isso `V8` (regressão) é a seção mais pesada aqui.

---

## V1 — Correções pré-requisito (Bloco 1)

| # | checagem | aceite |
|---|---|---|
| V1.1 | `cadunico_por_bairro_2026.csv` (todas idades) não foi sobrescrito | linhas = nº de bairros únicos em `df_bairro` (incl. `'Total'`); colunas `Crianças`/`Famílias` presentes |
| V1.2 | `cadunico_por_bairro_ate_4_2026.csv` existe, separado | arquivo novo, colunas incluindo `Primeira Inf. Cadúnico` |
| V1.3 | `tabelas_finais/mortalidade_raca_bairro_ano.csv` existe | mesmo nº de linhas que `dados_locais/tratados/mortalidade_raca_bairro_ano.csv` |
| V1.4 | Exports por bairro-ano de neonatal precoce/tardia/mortalidade infantil existem em `tabelas_finais/` | 3 arquivos novos, um por indicador, sem sobrescrever os agregados-município já existentes (`mortalidade_neonatal_precoce_por_ano.csv` etc. continuam idênticos — checar com `git diff` vazio no conteúdo) |
| V1.5 | Exports por bairro-ano de gravidez/puerpério existem | 2 arquivos novos, mesma ressalva de V1.4 sobre os agregados-município |

---

## V2 — Componente A (Blocos 2-3)

| # | checagem | aceite |
|---|---|---|
| V2.1 | `junta_codbairro_por_bairro` não perde bairro nenhum | 0 linhas com `codbairro` nulo em `df_bairro`/`df_bairro_ate_4` após o join (a função levanta erro se sobrar alguma — checagem é "não levantou erro") |
| V2.2 | `obitos_total`/`percentual_total` em `df_mortalidade_raca_bairro` | `obitos_total` = soma das 6 colunas `obitos_<raça>`, célula a célula, para uma amostra de 5 bairros-ano |
| V2.3 | 11 `tabela_mapa_*.csv` existem em `tabelas_finais/` | uma linha por bairro (166, ou 165 se algum bairro tiver 0 registros naquele ano/indicador — conferir contra o total de bairros do dataset fonte, não assumir 166 fixo) |
| V2.4 | 18 PNGs de mapa existem em `mapas/` | nomes batem com a tabela de `plan.md` §3.2 |
| V2.5 | Convenção de escala | toda coluna absoluta usa `bins`; toda coluna de taxa/% usa colorbar contínua (sem `bins`) — checar nos 9 pares |
| V2.6 | `bins` escolhidos após ver os dados | para cada um dos 11 indicadores, ≥ 3 das classes ocupadas (não uma classe única com todos os 166 bairros) |
| V2.7 | Elementos cartográficos | rosa dos ventos, escala gráfica, rodapé SIRGAS 2000, `fonte_dados` preenchido — mesmo padrão dos 6 mapas do Censo (checagem visual em amostra de 3 mapas) |
| V2.8 | Mapas de gravidez/puerpério | nota de cautela sobre números pequenos presente na célula markdown correspondente |

---

## V3 — Componente B: IBGE SIDRA

| # | checagem | aceite |
|---|---|---|
| V3.1 | Layout das 9 tabelas confere com o esperado | uma linha de município (`3304557`), ano `2022`, colunas nomeadas como em `specs.md` §3.1 — se algum arquivo divergir, `carrega_sidra_longo` falha ruidosamente (não silenciosamente) |
| V3.2 | Totais batem (com tolerância) entre o corte "geral" e a soma dos cortes com dimensão | `tabela9606_populacao_geral` (coluna `Total`) ≈ soma de `tabela9606_populacao_raca_cor` pelas 5 raças, por idade — checado: diferença de até ~5 pessoas por idade (ex. `1 ano`: soma das raças 55.991 vs. Total 55.996). **Confirmado como rounding do próprio IBGE** (controle de disclosure em recorte pequeno), não erro de `carrega_sidra_longo`/pivot — os mesmos valores já aparecem divergentes no CSV bruto do SIDRA. Sexo (Homens+Mulheres) bate exato com o Total. |
| V3.3 | Valores `-` viram 0 | nenhum `NaN`/erro de conversão nas 6 tabelas tratadas |
| V3.4 | 6 tabelas em `tabelas_finais/` | existem, formato largo, uma linha por idade (0-6 ou 0-5, + `Total`) |
| V3.5 | 6 gráficos em `visualizacoes/` | existem, eixo x = idade simples (0-6), legenda = raça/sexo (inclui `sidra_frequencia_escola_0_5_sexo_2022`, `plan.md` §4.3) |
| V3.6 | Frequência 0-5 (tabela 10057) vs. taxa 0-6 (tabela 10056) não confundidas | os dois pares de gráficos citam a tabela/ano corretos no título; 10057 é contagem absoluta, 10056 é taxa % — nunca a mesma escala |

---

## V4 — Componente C: mapas de subgrupo

| # | checagem | aceite |
|---|---|---|
| V4.1 | Filtro correto | `causa` == rótulo canônico exato (`1.2.1. Red por at à mulher na gestação` / `1.2.2. Red por at à mulher no parto`, sem o `ad ` redundante do rótulo bruto); `faixa_etaria` == `'menores de 1 ano'`; `ano` == 2025 |
| V4.2 | 2 `tabela_mapa_*.csv` + 2 PNGs existem | nomes conforme `specs.md` §4 |
| V4.3 | Soma das 10 CAPs | bate com o total municipal do subgrupo em 2025, extraído independentemente de `df_evitaveis_subgrupo_mrj` (panorama municipal) |
| V4.4 | Escala | só absoluto, `bins` (nunca colorbar contínua para estes 2 mapas — confirmado em `specs.md` §4) |
| V4.5 | `bins` escolhidos após `.describe()` | não reaproveita os `bins` do grupo agregado (`[20,40,60,80]`) sem antes olhar a distribuição real do subgrupo, que deve ser bem menor |

---

## V5 — Componente D: séries de subgrupo

| # | checagem | aceite |
|---|---|---|
| V5.1 | D.1 — 2 gráficos novos existem | `obitos_evitaveis_menores_1_ano_subgrupo_ano.png`, `obitos_evitaveis_1_a_4_anos_subgrupo_ano.png`; o de `< 5 anos` já existente **não foi alterado** |
| V5.2 | D.1 — soma das faixas | para um ano de amostra, `< 5 anos` == `< 1 ano` + `1-4 anos`, por subgrupo (mesma checagem já feita na fonte, `specs/2026-09-08_mortalidade-ap` V3.1) |
| V5.3 | D.2a — 18 gráficos existem | 6 subgrupos × 3 faixas, nomes conforme `plan.md` §6.2 |
| V5.4 | D.2a — amostra conferida à mão | para 2-3 combinações (subgrupo, faixa, CAP, ano), o valor no gráfico bate com o filtro manual em `df_evitaveis_cap_faixa` |
| V5.5 | D.2a — 10 séries por gráfico | todas as 10 CAPs presentes na legenda de cada um dos 18 (mesmo com valores baixos/zerados) |
| V5.6 | D.2b — 2 gráficos existem | `obitos_evitaveis_gestacao_cap_menores_1_ano_ano.png`, `obitos_evitaveis_parto_cap_menores_1_ano_ano.png` |
| V5.7 | D.2b — subconjunto de D.2a | os valores de D.2b são idênticos aos das séries correspondentes dentro de D.2a (mesmo dado, apresentação separada) |
| V5.8 | D.2b posicionado corretamente | aparece na seção de mapas do Componente C (`###### 🗺️ Mapas por CAP`), não junto da matriz completa D.2a |

---

## V6 — Componente E: raça/cor sem `nao_informado`/1996

| # | checagem | aceite |
|---|---|---|
| V6.1 | 2 gráficos novos existem | `obitos_causas_evitaveis_raca_sem_nao_informado_ano.png`, `percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano.png` |
| V6.2 | Gráficos originais mantidos | `obitos_causas_evitaveis_raca_ano.png` e `percentual_mortalidade_causas_evitaveis_raca_ano.png` continuam sendo gerados, sem alteração |
| V6.3 | `nao_informado` ausente | nenhuma das 5 séries dos 2 gráficos novos usa `obitos_evitaveis_nao_informado`/`percentual_evitaveis_nao_informado` |
| V6.4 | 1996 ausente no gráfico de óbitos | `df_evitaveis_raca_sem_1996['ano'].min() == 1997` |
| V6.5 | Percentual não precisa do filtro de 1996 | `df_percentual_evitaveis_municipio` já começa em 2011 (herdado da célula existente) — confirmar que nenhum ano < 2011 aparece |
| V6.6 | Nota de markdown | explica a diferença entre a versão original e a nova, no lugar do comentário-lembrete da linha 1167 |

---

## V7 — Regressão

| # | checagem | aceite |
|---|---|---|
| V7.1 | Execução ponta a ponta | `jupyter nbconvert --execute --inplace`, kernel limpo, **0 erros** em todas as células (mesmo processo desta sessão) |
| V7.2 | Saídas anteriores ao branch inalteradas | os CSVs de `tabelas_finais/` que já existiam antes deste branch continuam com o mesmo conteúdo (`git diff` vazio, exceto os 2 renomeados/expandidos no Bloco 1) |
| V7.3 | Mapas anteriores | os 6 mapas do Censo e os 6+2 mapas de CAP da spec anterior continuam sendo gerados sem erro |
| V7.4 | Assinaturas de função existentes | `mapa_coropletico_bairros`, `serie_temporal_multipla`, `grafico_barra_agrupado`, `agrega_grupo_cid` — nenhuma mudou de assinatura |
| V7.5 | `_NIVEIS_AGREGACAO` | inalterado — este branch não precisa de nenhuma chave nova (`'bairro'` e `'cap'` já existem) |
| V7.6 | `requirements.txt` | inalterado (nenhuma dependência nova, `plan.md` §10) |

Comando de conferência (nenhuma linha de função existente deve aparecer como removida, só
como contexto de diff; as linhas adicionadas devem ser só `.to_csv`/chamadas novas):

```bash
git diff staging_main -- analise.py | grep "^-" | grep -v "^---"
```

---

## V8 — Documentação e estrutura

| # | checagem | aceite |
|---|---|---|
| V8.1 | Funções no lugar certo | `carrega_sidra_longo`, `junta_codbairro_por_bairro` em `🧹 Limpeza e wrangling de dados`; nenhuma função nova fora de **Pacotes e Funções Auxiliares** |
| V8.2 | Seções de análise só chamam | nenhuma função definida dentro de uma seção de análise (Censo/CadÚnico/DataSUS/etc.) |
| V8.3 | Posição das células novas | confere com a tabela de `plan.md` §8, uma a uma |
| V8.4 | Nomes de arquivo | todos em snake_case, sem acento, refletindo indicador/seção — conferir os ~35 nomes novos contra `plan.md`/`tasks.md` |
| V8.5 | README | os 4 pontos de T8.1-T8.4 atualizados |
| V8.6 | Update Table | linha nova, versão seguinte à última do README |
| V8.7 | Notebook sincronizado | `analise.ipynb` reflete `analise.py` via `jupytext --sync` (sem diff pendente) |
| V8.8 | `specs/2026-09-09_maps-and-ibge/` | decisão do usuário sobre versionar a pasta no commit final (mesmo precedente de `specs/2026-09-08_mortalidade-ap/`, que ficou versionada) |

---

## Script de validação

V2.1, V2.6, V3.1-V3.3, V4.1, V4.3, V5.2, V5.4-V5.5, V5.7, V6.3-V6.5 e V7.1-V7.5 são
automatizáveis (`assert`s inline nas células correspondentes, ou uma célula de checagem ao
fim de cada componente — mesmo espírito da spec anterior). As checagens visuais (V2.7, V3.5,
mapas/gráficos abertos manualmente) e as de documentação (V8) ficam manuais, feitas no
fechamento (`tasks.md` Bloco 8).
