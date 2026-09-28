# Sugestões de omissão — relatório e site

> Pedido do usuário (2026-09-25): "look into listing tables/visualizations that could be omitted from the
> analysis (report AND website) without major losses (a suggestion, deaths by 'parto' or 'gravidez' for kids
> over 1 year, as they are likely a input/data register mistake)". **Nada aqui foi aplicado** ao site nem às
> figuras: é uma lista para decisão. Números tirados de `tabelas_finais/` em 2026-09-25 (script de conferência
> na sessão, reproduzível com pandas sobre os CSVs citados).
>
> Separado disto: as **tabelas repetidas do apêndice do PDF** já foram fundidas/omitidas (só no PDF, reversível
> em `SUBSTITUI_NO_PDF`, `relatorio/latex/build/tabelas.py`) — ver o fim deste arquivo.

## A. Dado provavelmente inválido ou irrelevante (recomendo tirar)

| # | O quê | Evidência | Onde aparece | Texto curado afetado |
| :- | :--- | :--- | :--- | :--- |
| A1 | **Causas perinatais em crianças de 1 a 4 anos** — subgrupos 1.2.1 (atenção à mulher na gestação), 1.2.2 (parto) e 1.2.3 (recém-nascido) | 22, 6 e 4 óbitos em **20 anos, na cidade inteira** (2006-2025; `mortalidade_evitaveis_cap_faixa_ano.csv`), menos de 2 por ano. São causas perinatais por definição; aos 1-4 anos indicam sequela registrada como causa básica ou erro de codificação | séries e mapas por subgrupo de 1-4 e de menores de 5 anos (`obitos_evitaveis_1_a_4_anos_subgrupo_ano`, `obitos_evitaveis_menores_5_subgrupo_ano`, tabelas por CAP) | nenhum específico |
| A2 | **Subgrupo 1.1 (reduzível por imunização)** | 38 óbitos de menores de 1 ano em 30 anos (1996-2025), 0 a 2 por ano; 10 em 1-4 anos em 20 anos | legendas e tabelas de subgrupo | nenhum |
| A3 | **Lesão autoprovocada, 0 a 5 anos** | 7 notificações em 8 anos (2018-2025) e 33 em 2026 (ano parcial). Autolesão nessa idade é clinicamente implausível; o salto de 2026 sugere mudança de preenchimento da ficha, como a própria legenda já supõe | gráfico `notif_autoprovocada_antes_2026_vs_2026`, mapa e tabelas `notif_autoprovocada_*` (eixo Proteção) | nenhum |
| A4 | **Óbitos maternos por bairro** (gravidez e puerpério) | em 2025, 107 de 119 bairros com 0 óbito na gravidez e 111 de 135 com 0 no puerpério; máximo de 3. O mapa não mostra padrão, só casos isolados identificáveis | site: mapas `mapa_obitos_gravidez_bairro_2025`, `mapa_obitos_puerperio_bairro_2025` (no PDF já saíram, D6) | 2 textos curados dos mapas (hoje sem figura no PDF) |

## B. Instável por número pequeno (recomendo agregar ou tirar)

| # | O quê | Evidência | Alternativa | Texto curado afetado |
| :- | :--- | :--- | :--- | :--- |
| B1 | **% de óbitos evitáveis por CAP, 1 a 4 anos** | 1 a 39 óbitos por CAP e ano (mediana 6-25); o percentual vai de 0% a 100% na CAP 2.2 e de 11% a 67% na 1.0 | manter só menores de 1 ano e menores de 5; ou média móvel de 5 anos | `percentual_evitaveis_cap_1_a_4_anos_ano`, `mapa_percentual_evitaveis_1_a_4_anos_cap_2025`, `obitos_evitaveis_cap_1_a_4_anos_ano`, `mapa_obitos_evitaveis_1_a_4_anos_cap_2025` |
| B2 | **Taxas de mortalidade neonatal precoce, tardia e pós-neonatal por bairro** | 39 dos 167 bairros com menos de 100 nascidos vivos em 2025 (18 com menos de 50); 54 bairros com 0 óbito precoce. Uma morte num bairro pequeno vira 20-70‰ | manter a taxa infantil (0-364 dias) por bairro, e as faixas neonatais só no município e por CAP; ou taxa de 5 anos acumulados por bairro | `mapa_taxa_mortalidade_precoce_bairro_2025`, `mapa_taxa_obitos_tardios_bairro_2025` (curados); `mapa_taxa_mortalidade_pos_neonatal_bairro_2025` |
| B3 | **Raça/cor amarela e indígena nas séries de óbitos de menores de 1 ano** | 0 a 2 óbitos por ano cada (2018-2025); no gráfico de % geram picos sem significado (indígena 4% em 2016) | juntar em "amarela e indígena" ou manter só na tabela | `obitos_raca_ano`, `percentual_mortalidade_raca_ano` (o texto não precisa mudar) |
| B4 | **Taxa de violência familiar por bairro** | bairros com poucas crianças: Joá com 500‰ (mãe) e 455‰ (pai); o mapa já usa teto P95 na cor, mas a tabela e o tooltip mostram o valor | manter a taxa por RA/CAP, e por bairro só a contagem; ou suprimir taxa com população de 0 a 4 anos abaixo de um limiar | nenhum curado |

## C. Repetido (recomendo tirar do site também)

| # | O quê | Por quê | Texto curado afetado |
| :- | :--- | :--- | :--- |
| C1 | **Cobertura vacinal, anos selecionados** (`cobertura_vacinal_epi_comparativo_anos`) | os 4 anos (2016, 2019, 2022, 2025) já estão na série anual | 1 texto curado — pode ir para a série |
| C2 | **Séries de causas evitáveis por faixa etária** (grupo e subgrupo para 0-6, 7-27 e 28-364 dias; 6 gráficos) | a série total e o recorte por faixa em 2025 (`obitos_causas_evitaveis_subgrupo_faixa_2025`) contam a mesma história | **6 textos curados** — perda real; só tirar se a equipe fundir os textos |
| C3 | **Frequência escolar em números absolutos por raça/cor e por sexo** (Censo 2022) | a taxa por idade é a informação comparável; o absoluto acompanha o tamanho de cada grupo | nenhum |
| C4 | **Mapas de contagem de óbitos por bairro ao lado do mapa de taxa** (precoce, tardia, infantil, raça) | a contagem por bairro reproduz, sobretudo, onde nascem mais crianças | curados: `mapa_obitos_neonatal_precoce_bairro_2025`, `mapa_obitos_raca_total_bairro_2025` |

## D. Não é omissão — nota de qualidade de dado

- SISVAN: desnutrição de 15,5% em 2018 e magreza perto de zero em 2009 destoam da série — manter com nota.
- Violência familiar: quebra de série em 2017 (já anotada no gráfico).
- Óbitos por raça/cor "não informada": 2.136 em 1996 (baixa completude; já anotado no `analise.py`).

## Já aplicado: tabelas repetidas no apêndice do PDF

Só no PDF (o site e o DOCX não mudam). O apêndice caiu de 66 para **43 tabelas** e o relatório de 209 para
**168 páginas**:

- mortalidade por bairro: uma tabela (nascidos vivos, óbitos 0-6, 7-27 e 28-364 dias, total, taxa infantil) no
  lugar de 8 (precoce, tardia, infantil, nascidos, raça × bairro);
- óbitos maternos por bairro: fora (A4);
- causas evitáveis: série total + recorte por faixa em 2025 no lugar das 6 séries por faixa; subgrupo × CAP →
  tabela por CAP;
- violência familiar: uma tabela por bairro (casos e taxas por vínculo) no lugar de por bairro, 3 tabelas de
  mapa, 2 "top 10" e a de CAP; "outros vínculos" dentro da tabela por vínculo; lesão autoprovocada 2025 → a
  do mapa (2018-2026);
- frequência escolar: contagem → taxa; vacina: anos selecionados → série; CadÚnico por bairro → tabela de
  recortes.
