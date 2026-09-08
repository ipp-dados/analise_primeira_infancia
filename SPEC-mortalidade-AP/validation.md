# Validação — Óbitos por causas evitáveis por Área Programática de Saúde (CAP)

> **Revisão 2.** V5 foi reescrita: a geometria agora é oficial, não derivada, e o critério de
> "aninhamento nas Áreas de Planejamento" foi **removido** — o dado oficial mostrou que ele
> não vale (Guaratiba). V10 é nova: prova a restrição de não alterar código existente.

Cada checagem tem um **critério de aceite objetivo**. Os valores esperados abaixo já foram
medidos na planilha e no geojson oficial durante a redação da spec — não são estimativas.

---

## V0 — Arquivo renomeado

| # | checagem | aceite |
|---|---|---|
| V0.1 | O xlsx existe no nome novo | `dados_locais/mortalidade/obitos_causas_evitaveis_primeira_infancia_cap_2006_2025.xlsx` existe |
| V0.2 | O nome antigo sumiu | nenhum arquivo com acento/espaço em `dados_locais/mortalidade/` |
| V0.3 | Está versionado | aparece em `git status` como novo arquivo (não ignorado) |
| V0.4 | Geojson de CAP presente | `dados_locais/geo/limite_ap_saude_rio.geojson` existe, 10 feições, EPSG:4326 |
| V0.5 | Geojson de CAP versionado | não é excluído pelo `.gitignore` |

---

## V1 — Layout da planilha é o esperado

Roda **antes** de confiar em qualquer extração. Se qualquer item falhar, a planilha mudou e
o passo fixo de 12 linhas está inválido.

| # | checagem | aceite |
|---|---|---|
| V1.1 | Abas | exatamente `['Informações gerais', '<1 ano', '1-4 anos', '<5 anos', 'LOGs']` |
| V1.2 | Shape das abas por CAP | `(119, 22)` nas três |
| V1.3 | Shape da aba geral | `(34, 22)` |
| V1.4 | Blocos por aba | 10, nos índices `0, 12, 24, ..., 108` |
| V1.5 | CAPs, na ordem | `['1.0','2.1','2.2','3.1','3.2','3.3','4.0','5.1','5.2','5.3']` |
| V1.6 | Categorias CID por bloco | as mesmas 8, na mesma ordem, nos 30 blocos (10 CAPs × 3 abas) |
| V1.7 | Anos | colunas 1-20 = `2006..2025`; coluna 21 = `Total` |

---

## V2 — Fidelidade da extração à fonte

| # | checagem | aceite |
|---|---|---|
| V2.1 | Nº de linhas por CSV de CAP | 1.600 (10 CAPs × 8 causas × 20 anos), nas três faixas |
| V2.2 | Nenhum `Total` virou registro | `causa` nunca contém `'Total'`; `cod_ap_sms` nunca é `'Total'` |
| V2.3 | Soma da coluna `Total` da planilha = soma dos anos | por linha, em todos os blocos |
| V2.4 | Sem nulos | `obitos.isna().sum() == 0` |
| V2.5 | Tipos | `ano` e `obitos` inteiros; `cod_ap_sms` e `causa` string |
| V2.6 | Total geral `< 5 anos` (10 CAPs, 2006-2025) | **22.784** |
| V2.7 | Total geral `< 1 ano` | soma dos blocos = soma dos totais impressos na planilha |
| V2.8 | Total geral `1-4 anos` | idem |

---

## V3 — Consistência entre as faixas etárias

| # | checagem | aceite |
|---|---|---|
| V3.1 | `< 5 anos` = `< 1 ano` + `1-4 anos`, célula a célula | **0 divergências** em 1.600 células (já verificado na fonte) |
| V3.2 | Faixas não somadas por engano | nenhuma tabela derivada agrega as 3 faixas num total |

---

## V4 — Consistência com a aba `Informações gerais`

| # | checagem | aceite |
|---|---|---|
| V4.1 | Total 2006-2025 por CAP: blocos `< 5 anos` × tabela por CAP da aba 1 | idênticos nas 10 CAPs |
| V4.2 | Totais por CAP esperados | 1.0=1.273 · 2.1=1.110 · 2.2=736 · 3.1=3.211 · 3.2=1.795 · 3.3=3.652 · 4.0=3.278 · 5.1=2.623 · 5.2=2.921 · 5.3=2.185 |
| V4.3 | Total municipal (aba 1) | **22.949** |
| V4.4 | Diferença município − soma das CAPs | **165**, = ` Ign` (82) + ` Ignorado` (83) |
| V4.5 | Diferença em **2025** | **0** (nenhum óbito sem CAP em 2025) |
| V4.6 | Total municipal por ano bate com a soma das 8 causas da aba 1 | em todos os 20 anos |
| V4.7 | Coerência da taxa | `TX ≈ Nº de óbitos / Nº de NV × 1000` (tolerância 0,01); ex. 2006 = 16,4797 |

---

## V5 — Geometria das CAPs (oficial) e adaptador de mapa

Já verificado durante a redação da spec — repetir após instalar o arquivo no projeto.

| # | checagem | aceite |
|---|---|---|
| V5.1 | Nº de feições | **10** |
| V5.2 | Códigos | `1.0, 2.1, 2.2, 3.1, 3.2, 3.3, 4.0, 5.1, 5.2, 5.3` — idênticos aos da planilha, sem o prefixo `AP ` |
| V5.3 | Geometrias válidas | `is_valid.all() == True` (o arquivo original do ArcGIS **não** é; exige `make_valid()`) |
| V5.4 | CRS | EPSG:4326, igual ao limite de bairros |
| V5.5 | `total_bounds` × limite de bairros | iguais até a 4ª casa decimal |
| V5.6 | Bairros cobertos | **166 de 166** dentro de alguma CAP, nenhum órfão |
| V5.7 | RA dividida entre CAPs | **nenhuma** — toda CAP é união exata de RAs |
| V5.8 | Alias | colunas `cod_ap_sms` e `cod_rp` presentes e **idênticas** valor a valor |
| V5.9 | `dissolve` dentro do adaptador | 10 polígonos (no-op), todos válidos |
| V5.10 | Join do dado com a geometria | 10 CAPs com valor, **0** "Sem dado" no mapa de 2025 |
| V5.11 | De-para `_RA_PARA_CAP` | bate 100% com o cruzamento espacial oficial (33 RAs) |

> ❌ **Removido da revisão 1:** "cada CAP cai numa única `area_plane`". O dado oficial mostrou
> que a CAP 5.2 inclui Guaratiba, e o critério deixou de ser prova de correção.

---

## V6 — Mapas

| # | checagem | aceite |
|---|---|---|
| V6.1 | Convenção de escala | absoluto → `bins` discretos; percentual → sem `bins` (colorbar) |
| V6.2 | `bins` escolhidos após ver os dados | ≥ 3 das 5 classes ocupadas em cada mapa absoluto |
| V6.3 | `bins` por faixa etária | faixas diferentes para `< 1 ano` e `1-4 anos` (ordens de grandeza distintas) |
| V6.4 | Elementos cartográficos | rosa dos ventos, escala gráfica, limites de UF, rótulos de municípios vizinhos, rodapé SIRGAS 2000 |
| V6.5 | Fonte no rodapé | `fonte_dados` preenchido nos 6 mapas |
| V6.6 | Arquivos | os 6 PNGs em `mapas/`, 300 DPI |
| V6.7 | Título | cita ano (2025), faixa etária e "Área Programática de Saúde (CAP)" |
| V6.8 | Leitura visual | abrir os 6 e conferir que nenhuma legenda cobre uma CAP inteira |
| V6.9 | Fronteiras | sobrepor ao limite de bairros e conferir que nenhuma CAP corta um bairro ao meio |

---

## V7 — Séries temporais

| # | checagem | aceite |
|---|---|---|
| V7.1 | Arquivos | os 7 PNGs por CAP + 2 municipais em `visualizacoes/` |
| V7.2 | Eixo x | 2006-2025 contínuo, sem buracos |
| V7.3 | 10 séries | as 10 CAPs presentes e na legenda |
| V7.4 | Percentual | valores em 0-100; sem `inf` (CAP/ano com 0 óbitos → `NaN`, gap na linha) |
| V7.5 | Soma das CAPs | por ano, bate com o total municipal menos os `Ignorado` daquele ano |
| V7.6 | Legibilidade | 10 séries, acima da paleta de 8 — conferir visualmente se as linhas são distinguíveis (precedente aceito: cobertura vacinal, 11 séries) |

---

## V8 — Documentação e estrutura

| # | checagem | aceite |
|---|---|---|
| V8.1 | Funções no lugar certo | extração em `🧹 Limpeza e wrangling`; `mapa_coropletico_cap`/`_CAMINHO_GEO_CAP`/`_RA_PARA_CAP` em `📈 Funções de visualização` |
| V8.2 | Seção de análise só chama | nenhuma função definida fora de `📦 Pacotes e Funções Auxiliares` |
| V8.3 | Hierarquia de headings | `#####` para a seção, `######` para as subseções (sem pular nível) |
| V8.4 | Notas de markdown | as 6 notas de `plan.md` §6 presentes |
| V8.5 | Nomes de arquivo | PNGs e CSVs refletem seção/tema, snake_case sem acento |
| V8.6 | README | 4 pontos de T6.1-T6.4 atualizados |
| V8.7 | Update Table | linha nova com versão e resumo |
| V8.8 | Notebook | `analise.ipynb` sincronizado via jupytext |
| V8.9 | Skill | `generate_map/SKILL.md` **não foi alterada** (documenta código existente); qualquer acréscimo é seção nova ao final |

---

## V9 — Regressão

| # | checagem | aceite |
|---|---|---|
| V9.1 | Execução ponta a ponta | `analise.py` roda sem erro do início ao fim |
| V9.2 | Saídas anteriores | os CSVs de `tabelas_finais/` que já existiam continuam idênticos (`git diff` vazio no conteúdo) |
| V9.3 | Mapas anteriores | os 6 mapas do Censo continuam sendo gerados |
| V9.4 | Assinaturas | nenhuma função existente mudou de assinatura |
| V9.5 | Dependências | `requirements.txt` inalterado |

---

## V10 — Restrição: nenhum código existente alterado

A checagem mais importante desta revisão. Objetiva e mecânica:

| # | checagem | aceite |
|---|---|---|
| V10.1 | Diff de `analise.py` | apenas linhas adicionadas; nenhuma linha removida ou modificada |
| V10.2 | `_NIVEIS_AGREGACAO` | idêntico ao de `staging_main` |
| V10.3 | `mapa_coropletico_bairros` | idêntica, docstring inclusive |
| V10.4 | `agrega_bairros_por_nivel`, `serie_temporal*`, `grafico_barra*` | idênticas |
| V10.5 | Células de análise anteriores | nenhuma editada; a seção nova é inserida **entre** células existentes |
| V10.6 | Skills e README | `generate_map/SKILL.md` sem alteração; no README, só acréscimos |

Comando de conferência (lista toda linha removida do arquivo; **aceite: saída vazia**):

```bash
git diff staging_main -- analise.py | grep "^-" | grep -v "^---"
```

---

## Script de validação

As checagens V1-V5 e V10 são todas automatizáveis (V10 por `git diff`). Proposta: um bloco de validação no fim da
seção nova do notebook, com `assert`s comentando o valor esperado — mesmo espírito das notas
de markdown já existentes, e roda junto com a análise.

As checagens visuais (V6.8, V7.6) e as de documentação (V8) ficam manuais.
