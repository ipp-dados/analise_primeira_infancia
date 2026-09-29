# Inventário de fontes

> Gerado por `relatorio/latex/build/inventario_fontes.py` em 28/09/2026 — **não editar à mão**.
> Documento de conferência da equipe (`specs/2026-09-25_relatorio_latex` §7); não entra no relatório.
> Cruza `analise.py` (leitura estática), `specs/estrutura_eixos.md` e `relatorio/latex/fontes.bib`.
> A versão em planilha, com todos os campos, é `relatorio/inventario_fontes.csv` (separador `;`).

## Resumo

| | Gráficos | Mapas | Tabelas |
| :--- | ---: | ---: | ---: |
| No disco | 66 | 37 | 87 |
| No relatório (estrutura_eixos.md) | 63 | 30 | 75 |
| Com fonte ligada ao fontes.bib | 66 | 37 | 87 |

## 1. Por fonte

Cada entrada de `fontes.bib` (lista **Fontes** do relatório) e o que ela gera. Só arquivos que entram no relatório; os demais estão na seção 2. Um arquivo com fonte composta (ex. casos do Sinan ÷ população do Censo) aparece em mais de uma fonte.

### Censo Demográfico 2022: população residente, por idade, sexo e cor ou raça

`ibge_censo2022` — Instituto Brasileiro de Geografia e Estatística

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `censo_sidra_populacao_0_6_raca_2022.png` | Introdução › Crianças até 6 anos, por raça/cor |
| gráfico | `censo_sidra_populacao_0_6_sexo_2022.png` | Introdução › Crianças até 6 anos, por sexo |
| gráfico | `sidra_frequencia_escola_0_5_total_2022.png` | Família e Cuidados › Crianças até 6 anos frequentando escola/creche (geral) |
| gráfico | `sidra_taxa_frequencia_0_6_raca_2022.png` | Família e Cuidados › Crianças até 6 anos frequentando escola/creche, por raça/cor |
| gráfico | `sidra_taxa_frequencia_0_6_sexo_2022.png` | Família e Cuidados › Crianças até 6 anos frequentando escola/creche, por sexo |
| tabela | `censo_sidra_populacao_0_6_raca_2022.csv` | Introdução › Crianças até 6 anos, por raça/cor |
| tabela | `censo_sidra_populacao_0_6_sexo_2022.csv` | Introdução › Crianças até 6 anos, por sexo |
| tabela | `sidra_frequencia_escola_0_5_total_2022.csv` | Família e Cuidados › Crianças até 6 anos frequentando escola/creche (geral) |
| tabela | `sidra_taxa_frequencia_0_6_raca_2022.csv` | Família e Cuidados › Crianças até 6 anos frequentando escola/creche, por raça/cor |
| tabela | `sidra_taxa_frequencia_0_6_sexo_2022.csv` | Família e Cuidados › Crianças até 6 anos frequentando escola/creche, por sexo |

### População residente por bairro: Censos Demográficos 2000, 2010 e 2022

`ipp_datario_censo` — Instituto Pereira Passos  
⚠️ **Conferir:** URL da tabela específica no Data.Rio; confirmar que a série 2000/2010 vem da mesma publicação

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `censo_0_a_4_serie_percentual_ano.png` | Introdução › Crianças até 4 anos (percentual) |
| gráfico | `censo_0_a_4_serie_total_ano.png` | Introdução › Crianças até 4 anos (número) |
| gráfico | `violencia_familiar_taxa_top_bairros_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_censo_0_4_absoluto.png` | Introdução › Crianças até 4 anos (número) |
| mapa | `mapa_censo_0_4_percentual.png` | Introdução › Crianças até 4 anos (percentual) |
| mapa | `mapa_violencia_familiar_mae_taxa_ra_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_pai_taxa_ra_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `censo_0_a_4_anos_por_ano.csv` | Introdução › Crianças até 4 anos (número) \| Crianças até 4 anos (percentual) |
| tabela | `censo_por_bairro.csv` | Introdução › Crianças até 4 anos (número) |
| tabela | `tabela_mapa_violencia_familiar_mae_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `tabela_mapa_violencia_familiar_outros_2021_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `tabela_mapa_violencia_familiar_pai_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `violencia_familiar_por_bairro.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `violencia_familiar_por_cap.csv` | Proteção › Violência familiar — por CAP |
| tabela | `violencia_familiar_por_vinculo_ano.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `violencia_familiar_taxa_municipio_ano.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `violencia_familiar_taxa_por_bairro.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `violencia_familiar_taxa_top_bairros_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `violencia_familiar_top_bairros_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |

### Estimativas populacionais por município, idade e sexo, 2000-2025 (Ripsa)

`ms_ripsa_populacao` — Brasil}. Ministério da Saúde  
⚠️ **Conferir:** URL exata da tabela consultada por carrega_populacao_ripsa

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `populacao_ripsa_0_a_6_percentual_por_ano.png` | Introdução › Crianças até 6 anos (número) |
| gráfico | `populacao_ripsa_0_a_6_por_ano.png` | Introdução › Crianças até 6 anos (número) |
| gráfico | `taxa_atendimento_0_a_5_por_ano.png` | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos |
| gráfico | `violencia_familiar_taxa_municipio_ano.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `cadunico_razao_populacao_0_a_5_2026.csv` | Prioridade › Crianças de 0 a 5 anos no CadÚnico em relação à população do município |
| tabela | `matriculas_0_a_5_por_ano.csv` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos |
| tabela | `populacao_ripsa_0_a_6_por_ano.csv` | Introdução › Crianças até 6 anos (número) |
| tabela | `violencia_familiar_por_vinculo_ano.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `violencia_familiar_taxa_municipio_ano.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |

### Sistema de Informações sobre Mortalidade (SIM): óbitos de residentes no município do Rio de Janeiro

`sms_rio_sim` — Rio de Janeiro (RJ)}. Secretaria Municipal de Saúde  
⚠️ **Conferir:** confirmar se a extração foi no TabNet da SMS-Rio (bairro de residência) ou no DATASUS nacional; URL

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `nascidos_abaixo_peso_percentual_por_ano.png` | Alimentação › Baixo peso ao nascer (percentual) |
| gráfico | `nascidos_vivos_por_ano.png` | Introdução › Nascidos vivos por bairro de residência da mãe (número) |
| gráfico | `obitos_causas_evitaveis_grupo_0_a_6_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_grupo_28_a_364_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_grupo_7_a_27_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_grupo_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_subgrupo_0_a_6_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_subgrupo_28_a_364_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_subgrupo_7_a_27_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_subgrupo_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_subgrupo_faixa_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_evitaveis_1_a_4_anos_subgrupo_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_evitaveis_cap_1_a_4_anos_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `obitos_evitaveis_cap_menores_1_ano_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `obitos_evitaveis_cap_menores_5_anos_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `obitos_evitaveis_menores_1_ano_subgrupo_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_evitaveis_menores_5_subgrupo_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_evitaveis_total_cap_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `obitos_gravidez_por_ano.png` | Prioridade › Óbitos maternos durante a gravidez |
| gráfico | `obitos_puerperio_por_ano.png` | Prioridade › Óbitos maternos durante o puerpério |
| gráfico | `obitos_raca_ano.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| gráfico | `percentual_evitaveis_cap_1_a_4_anos_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `percentual_evitaveis_cap_menores_1_ano_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `percentual_evitaveis_cap_menores_5_anos_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `percentual_mortalidade_raca_ano.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| gráfico | `taxa_mortalidade_evitaveis_menores_5_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `taxa_mortalidade_infantil_ano.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| gráfico | `taxa_mortalidade_pos_neonatal_ano.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| gráfico | `taxa_mortalidade_precoce_ano.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| gráfico | `taxa_obitos_tardios_ano.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_nascidos_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (número) |
| mapa | `mapa_nascidos_vivos_bairro_2025.png` | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| mapa | `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (percentual) |
| mapa | `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_taxa_mortalidade_infantil_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_taxa_mortalidade_precoce_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| mapa | `mapa_taxa_obitos_raca_total_bairro_2025.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| mapa | `mapa_taxa_obitos_tardios_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| tabela | `mortalidade_causas_evitaveis_grupo_0_a_6_dias_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_causas_evitaveis_grupo_28_a_364_dias_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_causas_evitaveis_grupo_7_a_27_dias_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_causas_evitaveis_grupo_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_causas_evitaveis_subgrupo_0_a_6_dias_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_causas_evitaveis_subgrupo_28_a_364_dias_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_causas_evitaveis_subgrupo_7_a_27_dias_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_causas_evitaveis_subgrupo_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_evitaveis_cap_2025.csv` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| tabela | `mortalidade_evitaveis_cap_faixa_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| tabela | `mortalidade_evitaveis_grupo_cap_faixa_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_evitaveis_subgrupo_cap_2025.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `mortalidade_infantil_pos_neonatal_total_bairro_ano.csv` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| tabela | `mortalidade_infantil_pos_neonatal_total_por_ano.csv` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| tabela | `mortalidade_neonatal_precoce_bairro_ano.csv` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| tabela | `mortalidade_neonatal_precoce_por_ano.csv` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| tabela | `mortalidade_neonatal_tardia_bairro_ano.csv` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| tabela | `mortalidade_neonatal_tardia_por_ano.csv` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| tabela | `mortalidade_raca_bairro_ano.csv` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| tabela | `mortalidade_raca_municipio_ano.csv` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| tabela | `nascidos_abaixo_peso_por_ano.csv` | Alimentação › Baixo peso ao nascer (número) \| Baixo peso ao nascer (percentual) |
| tabela | `obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| tabela | `obitos_gravidez_bairro_ano.csv` | Prioridade › Óbitos maternos durante a gravidez |
| tabela | `obitos_gravidez_por_ano.csv` | Prioridade › Óbitos maternos durante a gravidez |
| tabela | `obitos_puerperio_bairro_ano.csv` | Prioridade › Óbitos maternos durante o puerpério |
| tabela | `obitos_puerperio_por_ano.csv` | Prioridade › Óbitos maternos durante o puerpério |
| tabela | `tabela_mapa_mortalidade_infantil_2025.csv` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| tabela | `tabela_mapa_obitos_gravidez_2025.csv` | Prioridade › Óbitos maternos durante a gravidez |
| tabela | `tabela_mapa_obitos_neonatal_precoce_2025.csv` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| tabela | `tabela_mapa_obitos_neonatal_tardia_2025.csv` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| tabela | `tabela_mapa_obitos_puerperio_2025.csv` | Prioridade › Óbitos maternos durante o puerpério |
| tabela | `tabela_mapa_obitos_raca_total_2025.csv` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| tabela | `taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |

### Sistema de Informações sobre Nascidos Vivos (SINASC): nascimentos de mães residentes no município do Rio de Janeiro

`sms_rio_sinasc` — Rio de Janeiro (RJ)}. Secretaria Municipal de Saúde  
⚠️ **Conferir:** mesma dúvida do SIM (SMS-Rio ou DATASUS nacional); URL

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `nascidos_abaixo_peso_percentual_por_ano.png` | Alimentação › Baixo peso ao nascer (percentual) |
| gráfico | `nascidos_vivos_por_ano.png` | Introdução › Nascidos vivos por bairro de residência da mãe (número) |
| gráfico | `obitos_gravidez_por_ano.png` | Prioridade › Óbitos maternos durante a gravidez |
| gráfico | `obitos_puerperio_por_ano.png` | Prioridade › Óbitos maternos durante o puerpério |
| gráfico | `obitos_raca_ano.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| gráfico | `percentual_mortalidade_raca_ano.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| gráfico | `taxa_mortalidade_infantil_ano.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| gráfico | `taxa_mortalidade_pos_neonatal_ano.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| gráfico | `taxa_mortalidade_precoce_ano.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| gráfico | `taxa_obitos_tardios_ano.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_nascidos_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (número) |
| mapa | `mapa_nascidos_vivos_bairro_2025.png` | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| mapa | `mapa_percentual_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (percentual) |
| mapa | `mapa_taxa_mortalidade_infantil_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_taxa_mortalidade_precoce_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| mapa | `mapa_taxa_obitos_raca_total_bairro_2025.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| mapa | `mapa_taxa_obitos_tardios_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| tabela | `mortalidade_neonatal_precoce_bairro_ano.csv` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| tabela | `mortalidade_neonatal_precoce_por_ano.csv` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| tabela | `mortalidade_neonatal_tardia_bairro_ano.csv` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| tabela | `mortalidade_neonatal_tardia_por_ano.csv` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| tabela | `nascidos_abaixo_peso_por_ano.csv` | Alimentação › Baixo peso ao nascer (número) \| Baixo peso ao nascer (percentual) |
| tabela | `nascidos_vivos_por_ano.csv` | Introdução › Nascidos vivos por bairro de residência da mãe (número) |
| tabela | `tabela_mapa_nascidos_vivos_2025.csv` | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| tabela | `tabela_mapa_obitos_neonatal_precoce_2025.csv` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| tabela | `tabela_mapa_obitos_neonatal_tardia_2025.csv` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |

### Sistema de Informação de Agravos de Notificação (Sinan): notificações de violência interpessoal e autoprovocada

`sms_rio_sinan` — Rio de Janeiro (RJ)}. Secretaria Municipal de Saúde  
⚠️ **Conferir:** URL

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `notif_autoprovocada_antes_2026_vs_2026.png` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| gráfico | `violencia_familiar_outros_serie.png` | Proteção › Violência familiar — composição de "outros" vínculos |
| gráfico | `violencia_familiar_serie_vinculos.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| gráfico | `violencia_familiar_taxa_municipio_ano.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| gráfico | `violencia_familiar_taxa_top_bairros_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| gráfico | `violencia_familiar_top_bairros_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_notif_autoprovocada_bairro_2026.png` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| mapa | `mapa_violencia_familiar_mae_bairro_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_violencia_familiar_mae_taxa_ra_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_outros_bairro_2021_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_pai_bairro_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_violencia_familiar_pai_taxa_ra_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `notif_autoprovocada_por_bairro_ano.csv` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| tabela | `tabela_mapa_notif_autoprovocada_2026.csv` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| tabela | `tabela_mapa_violencia_familiar_mae_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `tabela_mapa_violencia_familiar_outros_2021_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `tabela_mapa_violencia_familiar_pai_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `violencia_familiar_outros_detalhe.csv` | Proteção › Violência familiar — composição de "outros" vínculos |
| tabela | `violencia_familiar_por_bairro.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `violencia_familiar_por_cap.csv` | Proteção › Violência familiar — por CAP |
| tabela | `violencia_familiar_por_vinculo_ano.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `violencia_familiar_taxa_municipio_ano.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `violencia_familiar_taxa_por_bairro.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `violencia_familiar_taxa_top_bairros_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| tabela | `violencia_familiar_top_bairros_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |

### Sistema de Vigilância Alimentar e Nutricional (SISVAN): relatórios públicos de estado nutricional

`ms_sisvan` — Brasil}. Ministério da Saúde

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `sisvan_desnutricao_percentual_por_ano.png` | Alimentação › Desnutrição SISVAN (percentual) |
| gráfico | `sisvan_obesidade_percentual_por_ano.png` | Alimentação › Sobrepeso SISVAN (percentual) |
| gráfico | `sisvan_sobrepeso_percentual_por_ano.png` | Alimentação › Sobrepeso SISVAN (percentual) |
| tabela | `sisvan_desnutricao_por_ano.csv` | Alimentação › Desnutrição SISVAN (número) \| Desnutrição SISVAN (percentual) |
| tabela | `sisvan_sobrepeso_por_ano.csv` | Alimentação › Sobrepeso SISVAN (número) \| Sobrepeso SISVAN (percentual) |

### Cobertura vacinal por imunobiológico, 2016-2026

`sms_rio_epi_vacinal` — Rio de Janeiro (RJ)}. Secretaria Municipal de Saúde. Superintendência de Vigilância em Saúde  
⚠️ **Conferir:** URL do painel e data da extração

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| tabela | `cobertura_vacinal_epi_por_ano.csv` | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos |

### Cadastro Único para Programas Sociais: base de famílias e pessoas do município do Rio de Janeiro

`mds_cadunico` — Brasil}. Ministério do Desenvolvimento e Assistência Social, Família e Combate à Fome  
⚠️ **Conferir:** nome por extenso do órgão responsável pela extração (CTPE) e forma de citação acordada com o órgão

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `cadunico_criancas_por_faixa_renda.png` | Prioridade › Famílias com crianças até 6 anos no Cadastro Único, por renda |
| gráfico | `cadunico_criancas_por_idade.png` | Prioridade › Crianças até 6 anos no Cadastro Único (número) |
| gráfico | `cadunico_criancas_por_raca_cor.png` | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| gráfico | `cadunico_criancas_por_sexo.png` | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por sexo |
| gráfico | `cadunico_familias_arranjo_renda.png` | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| gráfico | `cadunico_familias_por_arranjo.png` | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| gráfico | `cadunico_familias_por_faixa_renda.png` | Prioridade › Famílias com crianças até 6 anos no Cadastro Único, por renda |
| gráfico | `cadunico_familias_por_idade.png` | Prioridade › Famílias com crianças até 6 anos no Cadastro Único (número) |
| gráfico | `cadunico_familias_por_raca_cor.png` | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| gráfico | `cadunico_familias_por_sexo_criancas.png` | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por sexo |
| mapa | `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | Prioridade › Crianças até 6 anos no Cadastro Único (número) |
| mapa | `mapa_cadunico_criancas_bairro_2026.png` | Prioridade › Crianças até 6 anos no Cadastro Único (número) |
| mapa | `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| mapa | `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| tabela | `cadunico_familias_arranjo_renda_2026.csv` | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| tabela | `cadunico_familias_por_arranjo_2026.csv` | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| tabela | `cadunico_por_bairro_2026.csv` | Prioridade › Crianças até 6 anos no Cadastro Único (número) \| Famílias com crianças até 6 anos no Cadastro Único (número) |
| tabela | `cadunico_por_bairro_ate_4_2026.csv` | Prioridade › Crianças até 6 anos no Cadastro Único (número) |
| tabela | `cadunico_por_faixa_renda_2026.csv` | Prioridade › Famílias com crianças até 6 anos no Cadastro Único, por renda |
| tabela | `cadunico_por_idade_2026.csv` | Prioridade › Crianças até 6 anos no Cadastro Único (número) \| Famílias com crianças até 6 anos no Cadastro Único (número) |
| tabela | `cadunico_por_raca_cor_2026.csv` | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| tabela | `cadunico_por_sexo_2026.csv` | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por sexo |
| tabela | `cadunico_razao_populacao_0_a_5_2026.csv` | Prioridade › Crianças de 0 a 5 anos no CadÚnico em relação à população do município |
| tabela | `tabela_mapa_cadunico_criancas_0_a_4_2026.csv` | Prioridade › Crianças até 6 anos no Cadastro Único (número) |
| tabela | `tabela_mapa_cadunico_criancas_2026.csv` | Prioridade › Crianças até 6 anos no Cadastro Único (número) |
| tabela | `tabela_mapa_cadunico_recortes_bairro_2026.csv` | Prioridade … › Famílias no CadÚnico com crianças até 6 anos, por sexo \| Famílias no CadÚnico com crianças até 6 anos, por raça/cor \| Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |

### Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua): educação

`ibge_pnadc` — Instituto Brasileiro de Geografia e Estatística  
⚠️ **Conferir:** número da tabela SIDRA e ano de referência

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `pnad_frequencia_escolar_por_idade.png` | Família e Cuidados › Taxa bruta de frequência escolar da população até 6 anos |
| tabela | `frequencia_escolar_pnad_por_idade.csv` | Família e Cuidados › Taxa bruta de frequência escolar da população até 6 anos |

### Censo Escolar da Educação Básica: microdados, 2007-2025

`inep_censo_escolar` — Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `matriculas_0_a_5_creche_pre_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `matriculas_0_a_5_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `matriculas_0_a_5_rede_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `taxa_atendimento_0_a_5_por_ano.png` | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos |
| tabela | `matriculas_0_a_5_por_ano.csv` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos |

### Índice de Progresso Social do Rio de Janeiro 2024: indicadores por Região Administrativa

`ipp_ips2024` — Instituto Pereira Passos  
⚠️ **Conferir:** URL do conjunto de dados

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| mapa | `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png` | Direito ao Brincar › Violência territorial |
| mapa | `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png` | Direito ao Brincar › Violência territorial |
| mapa | `mapa_violencia_territorial_homicidios_ra_2024.png` | Direito ao Brincar › Violência territorial |
| tabela | `tabela_mapa_violencia_territorial_ra_2024.csv` | Direito ao Brincar › Violência territorial |

### Limite de bairros do município do Rio de Janeiro

`ipp_limites_bairros` — Instituto Pereira Passos  
⚠️ **Conferir:** URL; entradas equivalentes para as CAP (SMS-Rio) e as malhas do IBGE usadas no contexto dos mapas

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| mapa | `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | Prioridade › Crianças até 6 anos no Cadastro Único (número) |
| mapa | `mapa_cadunico_criancas_bairro_2026.png` | Prioridade › Crianças até 6 anos no Cadastro Único (número) |
| mapa | `mapa_censo_0_4_absoluto.png` | Introdução › Crianças até 4 anos (número) |
| mapa | `mapa_censo_0_4_percentual.png` | Introdução › Crianças até 4 anos (percentual) |
| mapa | `mapa_nascidos_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (número) |
| mapa | `mapa_nascidos_vivos_bairro_2025.png` | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| mapa | `mapa_notif_autoprovocada_bairro_2026.png` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| mapa | `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (percentual) |
| mapa | `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| mapa | `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| mapa | `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_taxa_mortalidade_infantil_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_taxa_mortalidade_precoce_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| mapa | `mapa_taxa_obitos_raca_total_bairro_2025.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| mapa | `mapa_taxa_obitos_tardios_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_violencia_familiar_mae_bairro_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_violencia_familiar_mae_taxa_ra_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_outros_bairro_2021_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_pai_bairro_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_violencia_familiar_pai_taxa_ra_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png` | Direito ao Brincar › Violência territorial |
| mapa | `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png` | Direito ao Brincar › Violência territorial |
| mapa | `mapa_violencia_territorial_homicidios_ra_2024.png` | Direito ao Brincar › Violência territorial |

## 2. Por arquivo

Todos os gráficos, mapas e tabelas no disco. **Fonte (analise.py)** é o `fonte_dados` da chamada que gera o arquivo; para tabelas, a última fonte vista antes do `to_csv` (método *vizinhança* — confira). **Fonte (.md)** é o campo `fonte:` da subseção em `estrutura_eixos.md`.

### Gráficos (66)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `cadunico_criancas_por_faixa_renda.png` | sim | Prioridade › Famílias com crianças até 6 anos no Cadastro Único, por renda | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.492 (chamada) |  |
| `cadunico_criancas_por_idade.png` | sim | Prioridade › Crianças até 6 anos no Cadastro Único (número) | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.522 (chamada) |  |
| `cadunico_criancas_por_raca_cor.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.759 (chamada) |  |
| `cadunico_criancas_por_sexo.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por sexo | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.727 (chamada) |  |
| `cadunico_familias_arranjo_renda.png` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra_agrupado` l.822 (chamada) |  |
| `cadunico_familias_por_arranjo.png` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.815 (chamada) |  |
| `cadunico_familias_por_faixa_renda.png` | sim | Prioridade › Famílias com crianças até 6 anos no Cadastro Único, por renda | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.483 (chamada) |  |
| `cadunico_familias_por_idade.png` | sim | Prioridade › Famílias com crianças até 6 anos no Cadastro Único (número) | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.514 (chamada) |  |
| `cadunico_familias_por_raca_cor.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.764 (chamada) |  |
| `cadunico_familias_por_sexo_criancas.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por sexo | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.733 (chamada) |  |
| `censo_0_a_4_serie_percentual_ano.png` | sim | Introdução › Crianças até 4 anos (percentual) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `serie_temporal` l.362 (chamada) |  |
| `censo_0_a_4_serie_total_ano.png` | sim | Introdução › Crianças até 4 anos (número) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `serie_temporal_multipla` l.349 (chamada) |  |
| `censo_sidra_populacao_0_6_raca_2022.png` | sim | Introdução › Crianças até 6 anos, por raça/cor | Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.194 (chamada) |  |
| `censo_sidra_populacao_0_6_sexo_2022.png` | sim | Introdução › Crianças até 6 anos, por sexo | Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.207 (chamada) |  |
| `cobertura_vacinal_epi_comparativo_anos.png` | não | — | EPI/SVS-Rio, cobertura vacinal por imunobiológico | — | sms_rio_epi_vacinal | `grafico_barra_agrupado` l.2291 (chamada) |  |
| `matriculas_0_a_5_creche_pre_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal_multipla` l.2469 (chamada) |  |
| `matriculas_0_a_5_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal` l.2465 (chamada) |  |
| `matriculas_0_a_5_rede_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal_multipla` l.2476 (chamada) |  |
| `nascidos_abaixo_peso_percentual_por_ano.png` | sim | Alimentação › Baixo peso ao nascer (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.993 (chamada) |  |
| `nascidos_vivos_por_ano.png` | sim | Introdução › Nascidos vivos por bairro de residência da mãe (número) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (nascidos vivos) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.934 (chamada) |  |
| `notif_autoprovocada_antes_2026_vs_2026.png` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | Sinan NET/Tabnet (SMS-Rio). 2026 parcial; possível mudança de registro (hipótese) | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `grafico_barra` l.2752 (chamada) |  |
| `obitos_causas_evitaveis_grupo_0_a_6_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1386 (chamada) |  |
| `obitos_causas_evitaveis_grupo_28_a_364_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1484 (chamada) |  |
| `obitos_causas_evitaveis_grupo_7_a_27_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1435 (chamada) |  |
| `obitos_causas_evitaveis_grupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1331 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_0_a_6_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1402 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_28_a_364_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1500 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_7_a_27_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1451 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1347 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_faixa_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `grafico_barra_agrupado` l.1539 (chamada) |  |
| `obitos_evitaveis_1_a_4_anos_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1632 (chamada) |  |
| `obitos_evitaveis_cap_1_a_4_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1691 (chamada) |  |
| `obitos_evitaveis_cap_menores_1_ano_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1691 (chamada) |  |
| `obitos_evitaveis_cap_menores_5_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1691 (chamada) |  |
| `obitos_evitaveis_menores_1_ano_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1632 (chamada) |  |
| `obitos_evitaveis_menores_5_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1586 (chamada) |  |
| `obitos_evitaveis_total_cap_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1719 (chamada) |  |
| `obitos_gravidez_por_ano.png` | sim | Prioridade › Óbitos maternos durante a gravidez | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.1892 (chamada) |  |
| `obitos_puerperio_por_ano.png` | sim | Prioridade › Óbitos maternos durante o puerpério | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.1935 (chamada) |  |
| `obitos_raca_ano.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal_multipla` l.1119 (chamada) |  |
| `percentual_evitaveis_cap_1_a_4_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1703 (chamada) |  |
| `percentual_evitaveis_cap_menores_1_ano_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1703 (chamada) |  |
| `percentual_evitaveis_cap_menores_5_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1703 (chamada) |  |
| `percentual_mortalidade_raca_ano.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal_multipla` l.1136 (chamada) |  |
| `pnad_frequencia_escolar_por_idade.png` | sim | Família e Cuidados › Taxa bruta de frequência escolar da população até 6 anos | PNAD Contínua (IBGE) | PNAD Contínua | ibge_pnadc | `grafico_barra` l.2421 (chamada) |  |
| `populacao_ripsa_0_a_6_percentual_por_ano.png` | sim | Introdução › Crianças até 6 anos (número) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `serie_temporal` l.403 (chamada) |  |
| `populacao_ripsa_0_a_6_por_ano.png` | sim | Introdução › Crianças até 6 anos (número) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `serie_temporal` l.399 (chamada) |  |
| `sidra_frequencia_escola_0_5_raca_2022.png` | não | — | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | — | ibge_censo2022 | `grafico_barra_agrupado` l.2343 (chamada) |  |
| `sidra_frequencia_escola_0_5_sexo_2022.png` | não | — | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | — | ibge_censo2022 | `grafico_barra_agrupado` l.2356 (chamada) |  |
| `sidra_frequencia_escola_0_5_total_2022.png` | sim | Família e Cuidados › Crianças até 6 anos frequentando escola/creche (geral) | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA, tabela 10057) | ibge_censo2022 | `grafico_barra` l.2376 (chamada) |  |
| `sidra_taxa_frequencia_0_6_raca_2022.png` | sim | Família e Cuidados › Crianças até 6 anos frequentando escola/creche, por raça/cor | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.2381 (chamada) |  |
| `sidra_taxa_frequencia_0_6_sexo_2022.png` | sim | Família e Cuidados › Crianças até 6 anos frequentando escola/creche, por sexo | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.2394 (chamada) |  |
| `sisvan_desnutricao_percentual_por_ano.png` | sim | Alimentação › Desnutrição SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.2212 (chamada) |  |
| `sisvan_obesidade_percentual_por_ano.png` | sim | Alimentação › Sobrepeso SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.2236 (chamada) |  |
| `sisvan_sobrepeso_percentual_por_ano.png` | sim | Alimentação › Sobrepeso SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.2228 (chamada) |  |
| `taxa_atendimento_0_a_5_por_ano.png` | sim | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos | Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | ms_ripsa_populacao, inep_censo_escolar | `serie_temporal_multipla` l.2502 (chamada) |  |
| `taxa_mortalidade_evitaveis_menores_5_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal` l.1602 (chamada) |  |
| `taxa_mortalidade_infantil_ano.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2163 (chamada) |  |
| `taxa_mortalidade_pos_neonatal_ano.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2128 (chamada) |  |
| `taxa_mortalidade_precoce_ano.png` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.1991 (chamada) |  |
| `taxa_obitos_tardios_ano.png` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2045 (chamada) |  |
| `violencia_familiar_outros_serie.png` | sim | Proteção › Violência familiar — composição de "outros" vínculos | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `serie_temporal_multipla` l.2640 (chamada) |  |
| `violencia_familiar_serie_vinculos.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan | `serie_temporal_multipla_marcos` l.2594 (chamada) |  |
| `violencia_familiar_taxa_municipio_ano.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 5 anos: estimativas Ripsa/Ministério da Saúde | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ms_ripsa_populacao, sms_rio_sinan | `serie_temporal_multipla_marcos` l.2621 (chamada) |  |
| `violencia_familiar_taxa_top_bairros_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio); bairros com 100+ crianças | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `grafico_barra_agrupado` l.2889 (chamada) |  |
| `violencia_familiar_top_bairros_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan | `grafico_barra_agrupado` l.2706 (chamada) |  |

### Mapas (37)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | sim | Prioridade › Crianças até 6 anos no Cadastro Único (número) | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.672 (chamada) |  |
| `mapa_cadunico_criancas_bairro_2026.png` | sim | Prioridade › Crianças até 6 anos no Cadastro Único (número) | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.644 (chamada) |  |
| `mapa_censo_0_4_absoluto.png` | sim | Introdução › Crianças até 4 anos (número) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo, ipp_limites_bairros | `mapa_coropletico_bairros` l.241 (chamada) |  |
| `mapa_censo_0_4_percentual.png` | sim | Introdução › Crianças até 4 anos (percentual) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo, ipp_limites_bairros | `mapa_coropletico_bairros` l.256 (chamada) |  |
| `mapa_mortalidade_infantil_bairro_2025.png` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2174 (chamada) |  |
| `mapa_nascidos_baixo_peso_bairro_2025.png` | sim | Alimentação › Baixo peso ao nascer (número) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.964 (chamada) |  |
| `mapa_nascidos_vivos_bairro_2025.png` | sim | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (nascidos vivos) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.914 (chamada) |  |
| `mapa_notif_autoprovocada_bairro_2026.png` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2763 (chamada) |  |
| `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.1796 (chamada) |  |
| `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.1796 (chamada) |  |
| `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.1796 (chamada) |  |
| `mapa_obitos_neonatal_precoce_bairro_2025.png` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2005 (chamada) |  |
| `mapa_obitos_raca_total_bairro_2025.png` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.1156 (chamada) |  |
| `mapa_percentual_baixo_peso_bairro_2025.png` | sim | Alimentação › Baixo peso ao nascer (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.970 (chamada) |  |
| `mapa_percentual_cadunico_0_a_4_sobre_censo_bairro_2026.png` | não | — | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos; população 0 a 4 anos: Censo 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.678 (chamada) |  |
| `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.869 (chamada) |  |
| `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.869 (chamada) |  |
| `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.1806 (chamada) |  |
| `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.1806 (chamada) |  |
| `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.1806 (chamada) |  |
| `mapa_taxa_mortalidade_infantil_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2180 (chamada) |  |
| `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2148 (chamada) |  |
| `mapa_taxa_mortalidade_precoce_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2011 (chamada) |  |
| `mapa_taxa_obitos_raca_total_bairro_2025.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.1162 (chamada) |  |
| `mapa_taxa_obitos_tardios_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2065 (chamada) |  |
| `mapa_violencia_familiar_mae_bairro_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2675 (chamada) |  |
| `mapa_violencia_familiar_mae_taxa_bairro_2025.png` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2843 (chamada) |  |
| `mapa_violencia_familiar_mae_taxa_ra_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2869 (chamada) |  |
| `mapa_violencia_familiar_outros_bairro_2021_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2687 (chamada) |  |
| `mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2843 (chamada) |  |
| `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2869 (chamada) |  |
| `mapa_violencia_familiar_pai_bairro_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2681 (chamada) |  |
| `mapa_violencia_familiar_pai_taxa_bairro_2025.png` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2843 (chamada) |  |
| `mapa_violencia_familiar_pai_taxa_ra_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2869 (chamada) |  |
| `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png` | sim | Direito ao Brincar › Violência territorial | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa | ipp_ips2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.2793 (chamada) |  |
| `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png` | sim | Direito ao Brincar › Violência territorial | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa | ipp_ips2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.2793 (chamada) |  |
| `mapa_violencia_territorial_homicidios_ra_2024.png` | sim | Direito ao Brincar › Violência territorial | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa | ipp_ips2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.2793 (chamada) |  |

### Tabelas (87)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `cadunico_familias_arranjo_renda_2026.csv` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.809 (estrutura_eixos.md) |  |
| `cadunico_familias_por_arranjo_2026.csv` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.784 (estrutura_eixos.md) |  |
| `cadunico_por_bairro_2026.csv` | sim | Prioridade › Crianças até 6 anos no Cadastro Único (número) \| Famílias com crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.575 (estrutura_eixos.md) |  |
| `cadunico_por_bairro_ate_4_2026.csv` | sim | Prioridade › Crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.622 (estrutura_eixos.md) |  |
| `cadunico_por_faixa_renda_2026.csv` | sim | Prioridade › Famílias com crianças até 6 anos no Cadastro Único, por renda | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.474 (estrutura_eixos.md) |  |
| `cadunico_por_idade_2026.csv` | sim | Prioridade › Crianças até 6 anos no Cadastro Único (número) \| Famílias com crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.509 (estrutura_eixos.md) |  |
| `cadunico_por_raca_cor_2026.csv` | sim | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por raça/cor | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.754 (estrutura_eixos.md) |  |
| `cadunico_por_sexo_2026.csv` | sim | Prioridade › Famílias no CadÚnico com crianças até 6 anos, por sexo | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.723 (estrutura_eixos.md) |  |
| `cadunico_razao_populacao_0_a_5_2026.csv` | sim | Prioridade › Crianças de 0 a 5 anos no CadÚnico em relação à população do município | — | Cadastro Único (extração CTPE, jun/2026); população: estimativas Ripsa/Ministério da Saúde (2025) | ms_ripsa_populacao, mds_cadunico | `to_csv` l.558 (estrutura_eixos.md) |  |
| `censo_0_a_4_anos_por_ano.csv` | sim | Introdução › Crianças até 4 anos (número) \| Crianças até 4 anos (percentual) | — | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `to_csv` l.344 (estrutura_eixos.md) |  |
| `censo_por_bairro.csv` | sim | Introdução › Crianças até 4 anos (número) | — | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `to_csv` l.154 (estrutura_eixos.md) |  |
| `censo_sidra_populacao_0_6_raca_2022.csv` | sim | Introdução › Crianças até 6 anos, por raça/cor | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.187 (estrutura_eixos.md) |  |
| `censo_sidra_populacao_0_6_sexo_2022.csv` | sim | Introdução › Crianças até 6 anos, por sexo | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.188 (estrutura_eixos.md) |  |
| `cobertura_vacinal_epi_comparativo_anos.csv` | não | — | EPI/SVS-Rio, cobertura vacinal por imunobiológico | — | sms_rio_epi_vacinal | `to_csv` l.2287 (vizinhança) |  |
| `cobertura_vacinal_epi_por_ano.csv` | sim | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos | — | Epi Rio | sms_rio_epi_vacinal | `to_csv` l.2258 (estrutura_eixos.md) |  |
| `frequencia_escolar_pnad_por_idade.csv` | sim | Família e Cuidados › Taxa bruta de frequência escolar da população até 6 anos | — | PNAD Contínua | ibge_pnadc | `to_csv` l.2417 (estrutura_eixos.md) |  |
| `matriculas_0_a_5_por_ano.csv` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos | — | Censo Escolar da Educação Básica (INEP), microdados; Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | ms_ripsa_populacao, inep_censo_escolar | `to_csv` l.2461 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_0_a_6_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1380 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_28_a_364_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1478 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_7_a_27_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1429 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1325 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_0_a_6_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1381 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_28_a_364_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1479 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_7_a_27_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1430 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1326 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1532 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_cap_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.1777 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_cap_faixa_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.1662 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_grupo_cap_faixa_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1678 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_subgrupo_cap_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1784 (estrutura_eixos.md) |  |
| `mortalidade_infantil_pos_neonatal_total_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.2117 (estrutura_eixos.md) |  |
| `mortalidade_infantil_pos_neonatal_total_por_ano.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.2124 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_precoce_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.1981 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_precoce_por_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.1987 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_tardia_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2035 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_tardia_por_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2041 (estrutura_eixos.md) |  |
| `mortalidade_raca_bairro_ano.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1088 (estrutura_eixos.md) |  |
| `mortalidade_raca_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1111 (estrutura_eixos.md) |  |
| `nascidos_abaixo_peso_por_ano.csv` | sim | Alimentação › Baixo peso ao nascer (número) \| Baixo peso ao nascer (percentual) | — | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.989 (estrutura_eixos.md) |  |
| `nascidos_vivos_por_ano.csv` | sim | Introdução › Nascidos vivos por bairro de residência da mãe (número) | — | DataSUS/Tabnet (nascidos vivos) | sms_rio_sinasc | `to_csv` l.931 (estrutura_eixos.md) |  |
| `notif_autoprovocada_por_bairro_ano.csv` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.2745 (estrutura_eixos.md) |  |
| `obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1578 (estrutura_eixos.md) |  |
| `obitos_gravidez_bairro_ano.csv` | sim | Prioridade › Óbitos maternos durante a gravidez | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1882 (estrutura_eixos.md) |  |
| `obitos_gravidez_por_ano.csv` | sim | Prioridade › Óbitos maternos durante a gravidez | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1888 (estrutura_eixos.md) |  |
| `obitos_puerperio_bairro_ano.csv` | sim | Prioridade › Óbitos maternos durante o puerpério | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1925 (estrutura_eixos.md) |  |
| `obitos_puerperio_por_ano.csv` | sim | Prioridade › Óbitos maternos durante o puerpério | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1931 (estrutura_eixos.md) |  |
| `populacao_ripsa_0_a_6_por_ano.csv` | sim | Introdução › Crianças até 6 anos (número) | — | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `to_csv` l.395 (estrutura_eixos.md) |  |
| `sidra_frequencia_escola_0_5_raca_2022.csv` | não | — | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | — | ibge_censo2022 | `to_csv` l.2333 (vizinhança) |  |
| `sidra_frequencia_escola_0_5_sexo_2022.csv` | não | — | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | — | ibge_censo2022 | `to_csv` l.2334 (vizinhança) |  |
| `sidra_frequencia_escola_0_5_total_2022.csv` | sim | Família e Cuidados › Crianças até 6 anos frequentando escola/creche (geral) | — | Censo Demográfico 2022 (IBGE SIDRA, tabela 10057) | ibge_censo2022 | `to_csv` l.2375 (estrutura_eixos.md) |  |
| `sidra_taxa_frequencia_0_6_raca_2022.csv` | sim | Família e Cuidados › Crianças até 6 anos frequentando escola/creche, por raça/cor | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.2335 (estrutura_eixos.md) |  |
| `sidra_taxa_frequencia_0_6_sexo_2022.csv` | sim | Família e Cuidados › Crianças até 6 anos frequentando escola/creche, por sexo | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.2336 (estrutura_eixos.md) |  |
| `sisvan_desnutricao_por_ano.csv` | sim | Alimentação › Desnutrição SISVAN (número) \| Desnutrição SISVAN (percentual) | — | SISVAN | ms_sisvan | `to_csv` l.2211 (estrutura_eixos.md) |  |
| `sisvan_sobrepeso_por_ano.csv` | sim | Alimentação › Sobrepeso SISVAN (número) \| Sobrepeso SISVAN (percentual) | — | SISVAN | ms_sisvan | `to_csv` l.2227 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_criancas_0_a_4_2026.csv` | sim | Prioridade › Crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.670 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_criancas_2026.csv` | sim | Prioridade › Crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.643 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_recortes_bairro_2026.csv` | sim | Prioridade … › Famílias no CadÚnico com crianças até 6 anos, por sexo \| Famílias no CadÚnico com crianças até 6 anos, por raça/cor \| Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.857 (estrutura_eixos.md) |  |
| `tabela_mapa_mortalidade_infantil_2025.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.2140 (estrutura_eixos.md) |  |
| `tabela_mapa_nascidos_baixo_peso_2025.csv` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc | `to_csv` l.962 (vizinhança) |  |
| `tabela_mapa_nascidos_vivos_2025.csv` | sim | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) | — | DataSUS/Tabnet (nascidos vivos) | sms_rio_sinasc | `to_csv` l.912 (estrutura_eixos.md) |  |
| `tabela_mapa_notif_autoprovocada_2026.csv` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.2762 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_gravidez_2025.csv` | sim | Prioridade › Óbitos maternos durante a gravidez | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1908 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_neonatal_precoce_2025.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2003 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_neonatal_tardia_2025.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2057 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_puerperio_2025.csv` | sim | Prioridade › Óbitos maternos durante o puerpério | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1950 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_raca_total_2025.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1154 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_mae_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2671 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_outros_2021_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2673 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_pai_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2672 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_taxa_mae_2025.csv` | não | — | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | — | ipp_ips2024 | `to_csv` l.2842 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_outros_2021_2025.csv` | não | — | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | — | ipp_ips2024 | `to_csv` l.2842 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_pai_2025.csv` | não | — | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | — | ipp_ips2024 | `to_csv` l.2842 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_mae_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2868 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_outros_2021_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2868 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_pai_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2868 (vizinhança) |  |
| `tabela_mapa_violencia_territorial_ra_2024.csv` | sim | Direito ao Brincar › Violência territorial | — | Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa | ipp_ips2024 | `to_csv` l.2784 (estrutura_eixos.md) |  |
| `taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.1579 (estrutura_eixos.md) |  |
| `violencia_familiar_outros_detalhe.csv` | sim | Proteção › Violência familiar — composição de "outros" vínculos | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.2638 (estrutura_eixos.md) |  |
| `violencia_familiar_por_bairro.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2654 (estrutura_eixos.md) |  |
| `violencia_familiar_por_cap.csv` | sim | Proteção › Violência familiar — por CAP | — | Sinan NET/Tabnet (SMS-Rio); população 0 a 4 anos do Censo 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2729 (estrutura_eixos.md) |  |
| `violencia_familiar_por_ra.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | — | sms_rio_sinan | `to_csv` l.2728 (vizinhança) |  |
| `violencia_familiar_por_vinculo_ano.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, ms_ripsa_populacao, sms_rio_sinan | `to_csv` l.2585 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_municipio_ano.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, ms_ripsa_populacao, sms_rio_sinan | `to_csv` l.2619 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_por_bairro.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2827 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_top_bairros_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2888 (estrutura_eixos.md) |  |
| `violencia_familiar_top_bairros_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2705 (estrutura_eixos.md) |  |
| `violencia_territorial_por_ra_2024.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos | — | sms_rio_sinan | `to_csv` l.2783 (vizinhança) |  |

## 3. Alertas

Apontados, não corrigidos — cada item pede uma decisão da equipe.

### Arquivo no disco que nenhuma subseção de estrutura_eixos.md usa (22)

- mapas/mapa_mortalidade_infantil_bairro_2025.png
- mapas/mapa_obitos_neonatal_precoce_bairro_2025.png
- mapas/mapa_obitos_raca_total_bairro_2025.png
- mapas/mapa_percentual_cadunico_0_a_4_sobre_censo_bairro_2026.png
- mapas/mapa_violencia_familiar_mae_taxa_bairro_2025.png
- mapas/mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png
- mapas/mapa_violencia_familiar_pai_taxa_bairro_2025.png
- tabelas_finais/cobertura_vacinal_epi_comparativo_anos.csv
- tabelas_finais/sidra_frequencia_escola_0_5_raca_2022.csv
- tabelas_finais/sidra_frequencia_escola_0_5_sexo_2022.csv
- tabelas_finais/tabela_mapa_nascidos_baixo_peso_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_mae_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_outros_2021_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_pai_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_ra_mae_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_ra_outros_2021_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_ra_pai_2025.csv
- tabelas_finais/violencia_familiar_por_ra.csv
- tabelas_finais/violencia_territorial_por_ra_2024.csv
- visualizacoes/cobertura_vacinal_epi_comparativo_anos.png
- visualizacoes/sidra_frequencia_escola_0_5_raca_2022.png
- visualizacoes/sidra_frequencia_escola_0_5_sexo_2022.png

### Informativo: `fonte:` do .md e `fonte_dados` do analise.py citam conjuntos de bases diferentes (11)

- mapas/mapa_nascidos_vivos_bairro_2025.png — .md: “DataSUS/Tabnet (nascidos vivos)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- mapas/mapa_taxa_mortalidade_infantil_bairro_2025.png — .md: “DataSUS/Tabnet municipal”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- mapas/mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png — .md: “DataSUS/Tabnet municipal”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- mapas/mapa_taxa_obitos_raca_total_bairro_2025.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/nascidos_vivos_por_ano.png — .md: “DataSUS/Tabnet (nascidos vivos)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/obitos_gravidez_por_ano.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/obitos_puerperio_por_ano.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/obitos_raca_ano.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/percentual_mortalidade_raca_ano.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/taxa_mortalidade_infantil_ano.png — .md: “DataSUS/Tabnet municipal”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/taxa_mortalidade_pos_neonatal_ano.png — .md: “DataSUS/Tabnet municipal”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”

## 4. Referências a confirmar (`conferir` em fontes.bib)

- `ipp_datario_censo`: URL da tabela específica no Data.Rio; confirmar que a série 2000/2010 vem da mesma publicação
- `ms_ripsa_populacao`: URL exata da tabela consultada por carrega_populacao_ripsa
- `sms_rio_sim`: confirmar se a extração foi no TabNet da SMS-Rio (bairro de residência) ou no DATASUS nacional; URL
- `sms_rio_sinasc`: mesma dúvida do SIM (SMS-Rio ou DATASUS nacional); URL
- `sms_rio_sinan`: URL
- `sms_rio_epi_vacinal`: URL do painel e data da extração
- `mds_cadunico`: nome por extenso do órgão responsável pela extração (CTPE) e forma de citação acordada com o órgão
- `ibge_pnadc`: número da tabela SIDRA e ano de referência
- `ipp_ips2024`: URL do conjunto de dados
- `ipp_limites_bairros`: URL; entradas equivalentes para as CAP (SMS-Rio) e as malhas do IBGE usadas no contexto dos mapas
