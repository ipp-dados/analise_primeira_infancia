# Inventário de fontes

> Gerado por `relatorio/latex/build/inventario_fontes.py` em 05/11/2026 — **não editar à mão**.
> Documento de conferência da equipe (`specs/2026-09-25_relatorio_latex` §7); não entra no relatório.
> Cruza `analise.py` (leitura estática), `specs/estrutura_eixos.md` e `relatorio/latex/fontes.bib`.
> A versão em planilha, com todos os campos, é `relatorio/inventario_fontes.csv` (separador `;`).

## Resumo

| | Gráficos | Mapas | Tabelas |
| :--- | ---: | ---: | ---: |
| No disco | 71 | 42 | 101 |
| No relatório (estrutura_eixos.md) | 67 | 34 | 84 |
| Com fonte ligada ao fontes.bib | 70 | 42 | 100 |

## 1. Por fonte

Cada entrada de `fontes.bib` (lista **Fontes** do relatório) e o que ela gera. Só arquivos que entram no relatório; os demais estão na seção 2. Um arquivo com fonte composta (ex. casos do Sinan ÷ população do Censo) aparece em mais de uma fonte.

### Censo Demográfico 2022: população residente, por idade, sexo e cor ou raça

`ibge_censo2022` — Instituto Brasileiro de Geografia e Estatística

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `censo_sidra_populacao_0_6_raca_2022.png` | Introdução › Crianças até 72 meses, por raça/cor |
| gráfico | `censo_sidra_populacao_0_6_sexo_2022.png` | Introdução › Crianças até 72 meses, por sexo |
| gráfico | `sidra_frequencia_escola_0_5_total_2022.png` | Família e Cuidados › Crianças até 72 meses frequentando escola/creche (geral) |
| gráfico | `sidra_taxa_frequencia_0_5_total_2022.png` | Família e Cuidados › Taxa bruta de frequência escolar da população até 72 meses |
| gráfico | `sidra_taxa_frequencia_0_6_raca_2022.png` | Família e Cuidados › Crianças até 72 meses frequentando escola/creche, por raça/cor |
| gráfico | `sidra_taxa_frequencia_0_6_sexo_2022.png` | Família e Cuidados › Crianças até 72 meses frequentando escola/creche, por sexo |
| tabela | `censo_sidra_populacao_0_6_raca_2022.csv` | Introdução › Crianças até 72 meses, por raça/cor |
| tabela | `censo_sidra_populacao_0_6_sexo_2022.csv` | Introdução › Crianças até 72 meses, por sexo |
| tabela | `sidra_frequencia_escola_0_5_total_2022.csv` | Família e Cuidados › Crianças até 72 meses frequentando escola/creche (geral) |
| tabela | `sidra_taxa_frequencia_0_5_total_2022.csv` | Família e Cuidados › Taxa bruta de frequência escolar da população até 72 meses |
| tabela | `sidra_taxa_frequencia_0_6_raca_2022.csv` | Família e Cuidados › Crianças até 72 meses frequentando escola/creche, por raça/cor |
| tabela | `sidra_taxa_frequencia_0_6_sexo_2022.csv` | Família e Cuidados › Crianças até 72 meses frequentando escola/creche, por sexo |

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
| gráfico | `populacao_ripsa_0_a_6_percentual_por_ano.png` | Introdução › Crianças até 72 meses (número) |
| gráfico | `populacao_ripsa_0_a_6_por_ano.png` | Introdução › Crianças até 72 meses (número) |
| gráfico | `taxa_atendimento_0_a_5_por_ano.png` | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos |
| gráfico | `violencia_familiar_taxa_municipio_ano.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `cadunico_razao_populacao_0_a_5_2026.csv` | Prioridade › Crianças de 0 a 5 anos no CadÚnico em relação à população do município |
| tabela | `matriculas_0_a_5_por_ano.csv` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos |
| tabela | `populacao_ripsa_0_a_6_por_ano.csv` | Introdução › Crianças até 72 meses (número) |
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
| gráfico | `cobertura_vacinal_epi_ano.png` | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos |
| tabela | `cobertura_vacinal_epi_por_ano.csv` | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos |

### Cadastro Único para Programas Sociais: base de famílias e pessoas do município do Rio de Janeiro

`mds_cadunico` — Brasil}. Ministério do Desenvolvimento e Assistência Social, Família e Combate à Fome  
⚠️ **Conferir:** nome por extenso do órgão responsável pela extração (CTPE) e forma de citação acordada com o órgão

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `cadunico_criancas_deficit_componentes.png` | Moradia › Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais) |
| gráfico | `cadunico_criancas_inadequacao_componentes.png` | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional |
| gráfico | `cadunico_criancas_por_faixa_renda.png` | Prioridade › Famílias com crianças até 72 meses no Cadastro Único, por renda |
| gráfico | `cadunico_criancas_por_idade.png` | Prioridade › Crianças até 72 meses no Cadastro Único (número) |
| gráfico | `cadunico_criancas_por_raca_cor.png` | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor |
| gráfico | `cadunico_criancas_por_sexo.png` | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por sexo |
| gráfico | `cadunico_criancas_por_tipo_deficiencia.png` | Inclusão › Crianças no CadÚnico por tipo de deficiência |
| gráfico | `cadunico_familias_arranjo_renda.png` | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar |
| gráfico | `cadunico_familias_por_arranjo.png` | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar |
| gráfico | `cadunico_familias_por_faixa_renda.png` | Prioridade › Famílias com crianças até 72 meses no Cadastro Único, por renda |
| gráfico | `cadunico_familias_por_idade.png` | Prioridade › Famílias com crianças até 72 meses no Cadastro Único (número) |
| gráfico | `cadunico_familias_por_raca_cor.png` | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor |
| gráfico | `cadunico_familias_por_sexo_criancas.png` | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por sexo |
| mapa | `mapa_cadunico_adensamento_n_bairro_2026.png` | Moradia › Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (mais de 2 pessoas por dormitório) |
| mapa | `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | Prioridade › Crianças até 72 meses no Cadastro Único (número) |
| mapa | `mapa_cadunico_criancas_bairro_2026.png` | Prioridade › Crianças até 72 meses no Cadastro Único (número) |
| mapa | `mapa_cadunico_inadequacao_n_bairro_2026.png` | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional |
| mapa | `mapa_percentual_cadunico_adensamento_bairro_2026.png` | Moradia › Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (mais de 2 pessoas por dormitório) |
| mapa | `mapa_percentual_cadunico_criancas_deficiencia_bairro_2026.png` | Inclusão › Crianças no CadÚnico com alguma deficiência |
| mapa | `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor |
| mapa | `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar |
| mapa | `mapa_percentual_cadunico_inadequacao_bairro_2026.png` | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional |
| tabela | `cadunico_deficiencia_criancas_0_a_5_2026.csv` | Inclusão › Crianças no CadÚnico com alguma deficiência |
| tabela | `cadunico_deficiencia_familias_0_a_5_2026.csv` | Inclusão › Famílias no CadÚnico com criança com deficiência |
| tabela | `cadunico_deficit_componentes_0_a_5_2026.csv` | Moradia › Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais) |
| tabela | `cadunico_familias_arranjo_renda_2026.csv` | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar |
| tabela | `cadunico_familias_por_arranjo_2026.csv` | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar |
| tabela | `cadunico_inadequacao_componentes_0_a_5_2026.csv` | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional |
| tabela | `cadunico_moradia_resumo_0_a_5_2026.csv` | Moradia › Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais) |
| tabela | `cadunico_por_bairro_2026.csv` | Prioridade › Crianças até 72 meses no Cadastro Único (número) \| Famílias com crianças até 72 meses no Cadastro Único (número) |
| tabela | `cadunico_por_bairro_ate_4_2026.csv` | Prioridade › Crianças até 72 meses no Cadastro Único (número) |
| tabela | `cadunico_por_faixa_renda_2026.csv` | Prioridade › Famílias com crianças até 72 meses no Cadastro Único, por renda |
| tabela | `cadunico_por_idade_2026.csv` | Prioridade › Crianças até 72 meses no Cadastro Único (número) \| Famílias com crianças até 72 meses no Cadastro Único (número) |
| tabela | `cadunico_por_raca_cor_2026.csv` | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor |
| tabela | `cadunico_por_sexo_2026.csv` | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por sexo |
| tabela | `cadunico_razao_populacao_0_a_5_2026.csv` | Prioridade › Crianças de 0 a 5 anos no CadÚnico em relação à população do município |
| tabela | `cadunico_tipos_deficiencia_0_a_5_2026.csv` | Inclusão › Crianças no CadÚnico por tipo de deficiência |
| tabela | `tabela_mapa_cadunico_adensamento_bairro_2026.csv` | Moradia › Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (mais de 2 pessoas por dormitório) |
| tabela | `tabela_mapa_cadunico_criancas_0_a_4_2026.csv` | Prioridade › Crianças até 72 meses no Cadastro Único (número) |
| tabela | `tabela_mapa_cadunico_criancas_2026.csv` | Prioridade › Crianças até 72 meses no Cadastro Único (número) |
| tabela | `tabela_mapa_cadunico_deficiencia_bairro_2026.csv` | Inclusão › Crianças no CadÚnico com alguma deficiência |
| tabela | `tabela_mapa_cadunico_inadequacao_bairro_2026.csv` | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional |
| tabela | `tabela_mapa_cadunico_recortes_bairro_2026.csv` | Prioridade … › Famílias no CadÚnico com crianças até 72 meses, por sexo \| Famílias no CadÚnico com crianças até 72 meses, por raça/cor \| Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar |

### Cadastro Único para Programas Sociais: características dos domicílios e pessoas com deficiência, município do Rio de Janeiro

`mds_cadunico_adhoc` — Brasil}. Ministério do Desenvolvimento e Assistência Social, Família e Combate à Fome  
⚠️ **Conferir:** órgão que fez a extração pontual e forma de citação (specs/2026-09-29_dados_adhoc)

_Nenhum arquivo do relatório._

### Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua): educação

`ibge_pnadc` — Instituto Brasileiro de Geografia e Estatística  
⚠️ **Conferir:** número da tabela SIDRA e ano de referência

_Nenhum arquivo do relatório._

### Censo Escolar da Educação Básica: microdados, 2007-2025

`inep_censo_escolar` — Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `matriculas_0_a_5_creche_pre_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `matriculas_0_a_5_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `matriculas_0_a_5_rede_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `taxa_atendimento_0_a_5_por_ano.png` | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos |
| tabela | `matriculas_0_a_5_por_ano.csv` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos |

### Indicadores de violência territorial por Região Administrativa do município do Rio de Janeiro: 2024

`isp_violencia2024` — Instituto de Segurança Pública do Estado do Rio de Janeiro  
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
| mapa | `mapa_cadunico_adensamento_n_bairro_2026.png` | Moradia › Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (mais de 2 pessoas por dormitório) |
| mapa | `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | Prioridade › Crianças até 72 meses no Cadastro Único (número) |
| mapa | `mapa_cadunico_criancas_bairro_2026.png` | Prioridade › Crianças até 72 meses no Cadastro Único (número) |
| mapa | `mapa_cadunico_inadequacao_n_bairro_2026.png` | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional |
| mapa | `mapa_censo_0_4_absoluto.png` | Introdução › Crianças até 4 anos (número) |
| mapa | `mapa_censo_0_4_percentual.png` | Introdução › Crianças até 4 anos (percentual) |
| mapa | `mapa_nascidos_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (número) |
| mapa | `mapa_nascidos_vivos_bairro_2025.png` | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| mapa | `mapa_notif_autoprovocada_bairro_2026.png` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| mapa | `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (percentual) |
| mapa | `mapa_percentual_cadunico_adensamento_bairro_2026.png` | Moradia › Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (mais de 2 pessoas por dormitório) |
| mapa | `mapa_percentual_cadunico_criancas_deficiencia_bairro_2026.png` | Inclusão › Crianças no CadÚnico com alguma deficiência |
| mapa | `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor |
| mapa | `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar |
| mapa | `mapa_percentual_cadunico_inadequacao_bairro_2026.png` | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional |
| mapa | `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
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

### Gráficos (71)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `cadunico_criancas_deficit_componentes.png` | sim | Moradia › Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais) | CadÚnico (extração CTPE, …/…). Metodologia da Fundação João Pinheiro; componentes não exclusivos | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `grafico_barra` l.1036 (chamada) |  |
| `cadunico_criancas_inadequacao_componentes.png` | sim | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional | CadÚnico (extração CTPE, …/…). Metodologia da Fundação João Pinheiro; componentes não exclusivos | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `grafico_barra` l.1025 (chamada) |  |
| `cadunico_criancas_por_faixa_renda.png` | sim | Prioridade › Famílias com crianças até 72 meses no Cadastro Único, por renda | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.517 (chamada) |  |
| `cadunico_criancas_por_idade.png` | sim | Prioridade › Crianças até 72 meses no Cadastro Único (número) | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.547 (chamada) |  |
| `cadunico_criancas_por_raca_cor.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.809 (chamada) |  |
| `cadunico_criancas_por_sexo.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por sexo | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.777 (chamada) |  |
| `cadunico_criancas_por_tipo_deficiencia.png` | sim | Inclusão › Crianças no CadÚnico por tipo de deficiência | CadÚnico (extração CTPE, …/…). Uma criança pode ter mais de um tipo: as barras não somam | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `grafico_barra` l.980 (chamada) |  |
| `cadunico_familias_arranjo_renda.png` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra_agrupado` l.872 (chamada) |  |
| `cadunico_familias_por_arranjo.png` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.865 (chamada) |  |
| `cadunico_familias_por_faixa_renda.png` | sim | Prioridade › Famílias com crianças até 72 meses no Cadastro Único, por renda | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.508 (chamada) |  |
| `cadunico_familias_por_idade.png` | sim | Prioridade › Famílias com crianças até 72 meses no Cadastro Único (número) | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.539 (chamada) |  |
| `cadunico_familias_por_raca_cor.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.814 (chamada) |  |
| `cadunico_familias_por_sexo_criancas.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por sexo | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.783 (chamada) |  |
| `censo_0_a_4_serie_percentual_ano.png` | sim | Introdução › Crianças até 4 anos (percentual) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `serie_temporal` l.374 (chamada) |  |
| `censo_0_a_4_serie_total_ano.png` | sim | Introdução › Crianças até 4 anos (número) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `serie_temporal_multipla` l.361 (chamada) |  |
| `censo_sidra_populacao_0_6_raca_2022.png` | sim | Introdução › Crianças até 72 meses, por raça/cor | Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.206 (chamada) |  |
| `censo_sidra_populacao_0_6_sexo_2022.png` | sim | Introdução › Crianças até 72 meses, por sexo | Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.219 (chamada) |  |
| `cobertura_vacinal_epi_ano.png` | sim | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos | EPI/SVS-Rio, cobertura vacinal por imunobiológico | Epi Rio | sms_rio_epi_vacinal | `serie_temporal_multipla` l.2541 (chamada) |  |
| `cobertura_vacinal_epi_comparativo_anos.png` | não | — | EPI/SVS-Rio, cobertura vacinal por imunobiológico | — | sms_rio_epi_vacinal | `grafico_barra_agrupado` l.2569 (chamada) |  |
| `matriculas_0_a_5_creche_pre_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal_multipla` l.2757 (chamada) |  |
| `matriculas_0_a_5_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal` l.2753 (chamada) |  |
| `matriculas_0_a_5_rede_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal_multipla` l.2764 (chamada) |  |
| `nascidos_abaixo_peso_percentual_por_ano.png` | sim | Alimentação › Baixo peso ao nascer (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.1266 (chamada) |  |
| `nascidos_vivos_por_ano.png` | sim | Introdução › Nascidos vivos por bairro de residência da mãe (número) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (nascidos vivos) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.1206 (chamada) |  |
| `notif_autoprovocada_antes_2026_vs_2026.png` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | Sinan NET/Tabnet (SMS-Rio). 2026 parcial; possível mudança de registro (hipótese) | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `grafico_barra` l.3041 (chamada) |  |
| `obitos_causas_evitaveis_grupo_0_a_6_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1664 (chamada) |  |
| `obitos_causas_evitaveis_grupo_28_a_364_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1762 (chamada) |  |
| `obitos_causas_evitaveis_grupo_7_a_27_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1713 (chamada) |  |
| `obitos_causas_evitaveis_grupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1609 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_0_a_6_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1680 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_28_a_364_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1778 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_7_a_27_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1729 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1625 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_faixa_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `grafico_barra_agrupado` l.1817 (chamada) |  |
| `obitos_evitaveis_1_a_4_anos_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1910 (chamada) |  |
| `obitos_evitaveis_cap_1_a_4_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1969 (chamada) |  |
| `obitos_evitaveis_cap_menores_1_ano_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1969 (chamada) |  |
| `obitos_evitaveis_cap_menores_5_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1969 (chamada) |  |
| `obitos_evitaveis_menores_1_ano_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1910 (chamada) |  |
| `obitos_evitaveis_menores_5_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.1864 (chamada) |  |
| `obitos_evitaveis_total_cap_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1997 (chamada) |  |
| `obitos_gravidez_por_ano.png` | sim | Prioridade › Óbitos maternos durante a gravidez | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2170 (chamada) |  |
| `obitos_puerperio_por_ano.png` | sim | Prioridade › Óbitos maternos durante o puerpério | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2213 (chamada) |  |
| `obitos_raca_ano.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal_multipla` l.1392 (chamada) |  |
| `percentual_evitaveis_cap_1_a_4_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1981 (chamada) |  |
| `percentual_evitaveis_cap_menores_1_ano_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1981 (chamada) |  |
| `percentual_evitaveis_cap_menores_5_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.1981 (chamada) |  |
| `percentual_mortalidade_raca_ano.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro. Nota: a categoria "Não informada" aparece só no gráfico de óbitos | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal_multipla` l.1413 (chamada) |  |
| `pnad_frequencia_escolar_por_idade.png` | não | — | — | — | — | — |  |
| `populacao_ripsa_0_a_6_percentual_por_ano.png` | sim | Introdução › Crianças até 72 meses (número) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `serie_temporal` l.417 (chamada) |  |
| `populacao_ripsa_0_a_6_por_ano.png` | sim | Introdução › Crianças até 72 meses (número) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `serie_temporal` l.413 (chamada) |  |
| `sidra_frequencia_escola_0_5_raca_2022.png` | não | — | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | — | ibge_censo2022 | `grafico_barra_agrupado` l.2627 (chamada) |  |
| `sidra_frequencia_escola_0_5_sexo_2022.png` | não | — | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | — | ibge_censo2022 | `grafico_barra_agrupado` l.2640 (chamada) |  |
| `sidra_frequencia_escola_0_5_total_2022.png` | sim | Família e Cuidados › Crianças até 72 meses frequentando escola/creche (geral) | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA, tabela 10057) | ibge_censo2022 | `grafico_barra` l.2660 (chamada) |  |
| `sidra_taxa_frequencia_0_5_total_2022.png` | sim | Família e Cuidados › Taxa bruta de frequência escolar da população até 72 meses | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA, tabela 10056) | ibge_censo2022 | `grafico_barra` l.2708 (chamada) |  |
| `sidra_taxa_frequencia_0_6_raca_2022.png` | sim | Família e Cuidados › Crianças até 72 meses frequentando escola/creche, por raça/cor | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057). Nota: amarela e indígena (grupos pequenos) só no total de 0 a 5 anos: …% | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.2669 (chamada) |  |
| `sidra_taxa_frequencia_0_6_sexo_2022.png` | sim | Família e Cuidados › Crianças até 72 meses frequentando escola/creche, por sexo | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.2685 (chamada) |  |
| `sisvan_desnutricao_percentual_por_ano.png` | sim | Alimentação › Desnutrição SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.2490 (chamada) |  |
| `sisvan_obesidade_percentual_por_ano.png` | sim | Alimentação › Sobrepeso SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.2513 (chamada) |  |
| `sisvan_sobrepeso_percentual_por_ano.png` | sim | Alimentação › Sobrepeso SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.2505 (chamada) |  |
| `taxa_atendimento_0_a_5_por_ano.png` | sim | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos | Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | ms_ripsa_populacao, inep_censo_escolar | `serie_temporal_multipla` l.2791 (chamada) |  |
| `taxa_mortalidade_evitaveis_menores_5_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal` l.1880 (chamada) |  |
| `taxa_mortalidade_infantil_ano.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2441 (chamada) |  |
| `taxa_mortalidade_pos_neonatal_ano.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2406 (chamada) |  |
| `taxa_mortalidade_precoce_ano.png` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2269 (chamada) |  |
| `taxa_obitos_tardios_ano.png` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2323 (chamada) |  |
| `violencia_familiar_outros_serie.png` | sim | Proteção › Violência familiar — composição de "outros" vínculos | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `serie_temporal_multipla` l.2929 (chamada) |  |
| `violencia_familiar_serie_vinculos.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan | `serie_temporal_multipla_marcos` l.2883 (chamada) |  |
| `violencia_familiar_taxa_municipio_ano.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 5 anos: estimativas Ripsa/Ministério da Saúde | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ms_ripsa_populacao, sms_rio_sinan | `serie_temporal_multipla_marcos` l.2910 (chamada) |  |
| `violencia_familiar_taxa_top_bairros_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio); bairros com 100+ crianças | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `grafico_barra_agrupado` l.3178 (chamada) |  |
| `violencia_familiar_top_bairros_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan | `grafico_barra_agrupado` l.2995 (chamada) |  |

### Mapas (42)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `mapa_cadunico_adensamento_n_bairro_2026.png` | sim | Moradia › Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (mais de 2 pessoas por dormitório) | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE).… Bairros com menos de 20 casos ficam sem cor: estão somados por RA ou AP na tabela ("Demais bairros da RA/AP …") | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.1079 (chamada) |  |
| `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | sim | Prioridade › Crianças até 72 meses no Cadastro Único (número) | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial. Bairros com menos de 20 crianças ou famílias no CadÚnico ficam sem cor: estão somados por Região Administrativa na tabela ("Demais bairros da RA …") | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.721 (chamada) |  |
| `mapa_cadunico_criancas_bairro_2026.png` | sim | Prioridade › Crianças até 72 meses no Cadastro Único (número) | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial. Bairros com menos de 20 crianças ou famílias no CadÚnico ficam sem cor: estão somados por Região Administrativa na tabela ("Demais bairros da RA …") | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.681 (chamada) |  |
| `mapa_cadunico_inadequacao_n_bairro_2026.png` | sim | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE).… Bairros com menos de 20 casos ficam sem cor: estão somados por RA ou AP na tabela ("Demais bairros da RA/AP …") | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.1079 (chamada) |  |
| `mapa_censo_0_4_absoluto.png` | sim | Introdução › Crianças até 4 anos (número) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo, ipp_limites_bairros | `mapa_coropletico_bairros` l.253 (chamada) |  |
| `mapa_censo_0_4_percentual.png` | sim | Introdução › Crianças até 4 anos (percentual) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo, ipp_limites_bairros | `mapa_coropletico_bairros` l.268 (chamada) |  |
| `mapa_mortalidade_infantil_bairro_2025.png` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2452 (chamada) |  |
| `mapa_nascidos_baixo_peso_bairro_2025.png` | sim | Alimentação › Baixo peso ao nascer (número) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.1236 (chamada) |  |
| `mapa_nascidos_vivos_bairro_2025.png` | sim | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (nascidos vivos) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.1186 (chamada) |  |
| `mapa_notif_autoprovocada_bairro_2026.png` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3052 (chamada) |  |
| `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.2074 (chamada) |  |
| `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.2074 (chamada) |  |
| `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.2074 (chamada) |  |
| `mapa_obitos_neonatal_precoce_bairro_2025.png` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2283 (chamada) |  |
| `mapa_obitos_raca_total_bairro_2025.png` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.1434 (chamada) |  |
| `mapa_percentual_baixo_peso_bairro_2025.png` | sim | Alimentação › Baixo peso ao nascer (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.1242 (chamada) |  |
| `mapa_percentual_cadunico_0_a_4_sobre_censo_bairro_2026.png` | não | — | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; população 0 a 4 anos: Censo 2022 (IBGE/Data.Rio). Bairros com menos de 20 casos (no grupo, no complemento ou no total) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa | — | ipp_datario_censo, mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.727 (chamada) |  |
| `mapa_percentual_cadunico_adensamento_bairro_2026.png` | sim | Moradia › Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (mais de 2 pessoas por dormitório) | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE). Bairros com menos de 20 casos (no grupo, no complemento ou na base) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa. Inadequação: metodologia da Fundação João Pinheiro. Valor atípico, na cor máxima: …; escala de cor até … | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.1091 (chamada) |  |
| `mapa_percentual_cadunico_criancas_deficiencia_bairro_2026.png` | sim | Inclusão › Crianças no CadÚnico com alguma deficiência | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE). Bairros com menos de 20 casos (no grupo, no complemento ou na base) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.997 (chamada) |  |
| `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | sim | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial. Bairros com menos de 20 casos (no grupo, no complemento ou no total) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.920 (chamada) |  |
| `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial. Bairros com menos de 20 casos (no grupo, no complemento ou no total) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.920 (chamada) |  |
| `mapa_percentual_cadunico_inadequacao_bairro_2026.png` | sim | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE). Bairros com menos de 20 casos (no grupo, no complemento ou na base) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa. Inadequação: metodologia da Fundação João Pinheiro. Valor atípico, na cor máxima: …; escala de cor até … | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.1091 (chamada) |  |
| `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.2084 (chamada) |  |
| `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.2084 (chamada) |  |
| `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro… | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.2084 (chamada) |  |
| `mapa_taxa_mortalidade_infantil_bairro_2025.png` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2458 (chamada) |  |
| `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2426 (chamada) |  |
| `mapa_taxa_mortalidade_precoce_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2289 (chamada) |  |
| `mapa_taxa_obitos_raca_total_bairro_2025.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.1440 (chamada) |  |
| `mapa_taxa_obitos_tardios_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2343 (chamada) |  |
| `mapa_violencia_familiar_mae_bairro_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2964 (chamada) |  |
| `mapa_violencia_familiar_mae_taxa_bairro_2025.png` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3132 (chamada) |  |
| `mapa_violencia_familiar_mae_taxa_ra_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3158 (chamada) |  |
| `mapa_violencia_familiar_outros_bairro_2021_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2976 (chamada) |  |
| `mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3132 (chamada) |  |
| `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3158 (chamada) |  |
| `mapa_violencia_familiar_pai_bairro_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.2970 (chamada) |  |
| `mapa_violencia_familiar_pai_taxa_bairro_2025.png` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3132 (chamada) |  |
| `mapa_violencia_familiar_pai_taxa_ra_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3158 (chamada) |  |
| `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png` | sim | Direito ao Brincar › Violência territorial | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa (todas as idades) | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa | isp_violencia2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.3082 (chamada) |  |
| `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png` | sim | Direito ao Brincar › Violência territorial | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa (todas as idades) | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa | isp_violencia2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.3082 (chamada) |  |
| `mapa_violencia_territorial_homicidios_ra_2024.png` | sim | Direito ao Brincar › Violência territorial | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa (todas as idades) | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa | isp_violencia2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.3082 (chamada) |  |

### Tabelas (101)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `cadunico_adhoc_deficiencia_2026_08.csv` | não | — | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE). Bairros com menos de 20 casos (no grupo, no complemento ou na base) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa. Inadequação: metodologia da Fundação João Pinheiro. Valor atípico, na cor máxima: …; escala de cor até … | — | mds_cadunico | `to_csv` l.1141 (vizinhança) |  |
| `cadunico_adhoc_deficiencia_contexto_2026_08.csv` | não | — | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE). Bairros com menos de 20 casos (no grupo, no complemento ou na base) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa. Inadequação: metodologia da Fundação João Pinheiro. Valor atípico, na cor máxima: …; escala de cor até … | — | mds_cadunico | `to_csv` l.1141 (vizinhança) |  |
| `cadunico_adhoc_moradia_domicilio_2026_08.csv` | não | — | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE). Bairros com menos de 20 casos (no grupo, no complemento ou na base) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa. Inadequação: metodologia da Fundação João Pinheiro. Valor atípico, na cor máxima: …; escala de cor até … | — | mds_cadunico | `to_csv` l.1141 (vizinhança) |  |
| `cadunico_adhoc_moradia_territorio_2026_08.csv` | não | — | CadÚnico (extração CTPE, …/…). Bairro pelo CEP da família (correspondência CEP-bairro do CTPE). Bairros com menos de 20 casos (no grupo, no complemento ou na base) mostram a taxa do conjunto dos bairros pequenos da sua Região Administrativa. Inadequação: metodologia da Fundação João Pinheiro. Valor atípico, na cor máxima: …; escala de cor até … | — | mds_cadunico | `to_csv` l.1141 (vizinhança) |  |
| `cadunico_deficiencia_criancas_0_a_5_2026.csv` | sim | Inclusão › Crianças no CadÚnico com alguma deficiência | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.964 (estrutura_eixos.md) |  |
| `cadunico_deficiencia_familias_0_a_5_2026.csv` | sim | Inclusão › Famílias no CadÚnico com criança com deficiência | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.965 (estrutura_eixos.md) |  |
| `cadunico_deficit_componentes_0_a_5_2026.csv` | sim | Moradia › Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais) | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.1016 (estrutura_eixos.md) |  |
| `cadunico_familias_arranjo_renda_2026.csv` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.859 (estrutura_eixos.md) |  |
| `cadunico_familias_por_arranjo_2026.csv` | sim | Família e Cuidados › Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.834 (estrutura_eixos.md) |  |
| `cadunico_inadequacao_componentes_0_a_5_2026.csv` | sim | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.1015 (estrutura_eixos.md) |  |
| `cadunico_moradia_resumo_0_a_5_2026.csv` | sim | Moradia › Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais) | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.1014 (estrutura_eixos.md) |  |
| `cadunico_por_bairro_2026.csv` | sim | Prioridade › Crianças até 72 meses no Cadastro Único (número) \| Famílias com crianças até 72 meses no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.639 (estrutura_eixos.md) |  |
| `cadunico_por_bairro_ate_4_2026.csv` | sim | Prioridade › Crianças até 72 meses no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.714 (estrutura_eixos.md) |  |
| `cadunico_por_faixa_renda_2026.csv` | sim | Prioridade › Famílias com crianças até 72 meses no Cadastro Único, por renda | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.499 (estrutura_eixos.md) |  |
| `cadunico_por_idade_2026.csv` | sim | Prioridade › Crianças até 72 meses no Cadastro Único (número) \| Famílias com crianças até 72 meses no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.534 (estrutura_eixos.md) |  |
| `cadunico_por_raca_cor_2026.csv` | sim | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por raça/cor | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.804 (estrutura_eixos.md) |  |
| `cadunico_por_sexo_2026.csv` | sim | Prioridade › Famílias no CadÚnico com crianças até 72 meses, por sexo | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.773 (estrutura_eixos.md) |  |
| `cadunico_razao_populacao_0_a_5_2026.csv` | sim | Prioridade › Crianças de 0 a 5 anos no CadÚnico em relação à população do município | — | Cadastro Único (extração CTPE, jun/2026); população: estimativas Ripsa/Ministério da Saúde (2025) | ms_ripsa_populacao, mds_cadunico | `to_csv` l.583 (estrutura_eixos.md) |  |
| `cadunico_tipos_deficiencia_0_a_5_2026.csv` | sim | Inclusão › Crianças no CadÚnico por tipo de deficiência | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.966 (estrutura_eixos.md) |  |
| `censo_0_a_4_anos_por_ano.csv` | sim | Introdução › Crianças até 4 anos (número) \| Crianças até 4 anos (percentual) | — | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `to_csv` l.356 (estrutura_eixos.md) |  |
| `censo_por_bairro.csv` | sim | Introdução › Crianças até 4 anos (número) | — | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `to_csv` l.155 (estrutura_eixos.md) |  |
| `censo_sidra_populacao_0_6_raca_2022.csv` | sim | Introdução › Crianças até 72 meses, por raça/cor | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.200 (estrutura_eixos.md) |  |
| `censo_sidra_populacao_0_6_sexo_2022.csv` | sim | Introdução › Crianças até 72 meses, por sexo | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.201 (estrutura_eixos.md) |  |
| `cobertura_vacinal_epi_comparativo_anos.csv` | não | — | EPI/SVS-Rio, cobertura vacinal por imunobiológico | — | sms_rio_epi_vacinal | `to_csv` l.2565 (vizinhança) |  |
| `cobertura_vacinal_epi_por_ano.csv` | sim | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos | — | Epi Rio | sms_rio_epi_vacinal | `to_csv` l.2535 (estrutura_eixos.md) |  |
| `frequencia_escolar_pnad_por_idade.csv` | não | — | — | — | — | — |  |
| `matriculas_0_a_5_por_ano.csv` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos | — | Censo Escolar da Educação Básica (INEP), microdados; Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | ms_ripsa_populacao, inep_censo_escolar | `to_csv` l.2749 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_0_a_6_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1658 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_28_a_364_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1756 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_7_a_27_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1707 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1603 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_0_a_6_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1659 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_28_a_364_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1757 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_7_a_27_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1708 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1604 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1810 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_cap_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.2055 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_cap_faixa_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.1940 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_grupo_cap_faixa_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1956 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_subgrupo_cap_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2062 (estrutura_eixos.md) |  |
| `mortalidade_infantil_pos_neonatal_total_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.2395 (estrutura_eixos.md) |  |
| `mortalidade_infantil_pos_neonatal_total_por_ano.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.2402 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_precoce_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2259 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_precoce_por_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2265 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_tardia_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2313 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_tardia_por_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2319 (estrutura_eixos.md) |  |
| `mortalidade_raca_bairro_ano.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1361 (estrutura_eixos.md) |  |
| `mortalidade_raca_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1384 (estrutura_eixos.md) |  |
| `nascidos_abaixo_peso_por_ano.csv` | sim | Alimentação › Baixo peso ao nascer (número) \| Baixo peso ao nascer (percentual) | — | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.1261 (estrutura_eixos.md) |  |
| `nascidos_vivos_por_ano.csv` | sim | Introdução › Nascidos vivos por bairro de residência da mãe (número) | — | DataSUS/Tabnet (nascidos vivos) | sms_rio_sinasc | `to_csv` l.1203 (estrutura_eixos.md) |  |
| `notif_autoprovocada_por_bairro_ano.csv` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3034 (estrutura_eixos.md) |  |
| `obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.1856 (estrutura_eixos.md) |  |
| `obitos_gravidez_bairro_ano.csv` | sim | Prioridade › Óbitos maternos durante a gravidez | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2160 (estrutura_eixos.md) |  |
| `obitos_gravidez_por_ano.csv` | sim | Prioridade › Óbitos maternos durante a gravidez | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2166 (estrutura_eixos.md) |  |
| `obitos_puerperio_bairro_ano.csv` | sim | Prioridade › Óbitos maternos durante o puerpério | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2203 (estrutura_eixos.md) |  |
| `obitos_puerperio_por_ano.csv` | sim | Prioridade › Óbitos maternos durante o puerpério | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2209 (estrutura_eixos.md) |  |
| `populacao_ripsa_0_a_6_por_ano.csv` | sim | Introdução › Crianças até 72 meses (número) | — | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `to_csv` l.409 (estrutura_eixos.md) |  |
| `sidra_frequencia_escola_0_5_raca_2022.csv` | não | — | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | — | ibge_censo2022 | `to_csv` l.2612 (vizinhança) |  |
| `sidra_frequencia_escola_0_5_sexo_2022.csv` | não | — | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | — | ibge_censo2022 | `to_csv` l.2613 (vizinhança) |  |
| `sidra_frequencia_escola_0_5_total_2022.csv` | sim | Família e Cuidados › Crianças até 72 meses frequentando escola/creche (geral) | — | Censo Demográfico 2022 (IBGE SIDRA, tabela 10057) | ibge_censo2022 | `to_csv` l.2659 (estrutura_eixos.md) |  |
| `sidra_taxa_frequencia_0_5_total_2022.csv` | sim | Família e Cuidados › Taxa bruta de frequência escolar da população até 72 meses | — | Censo Demográfico 2022 (IBGE SIDRA, tabela 10056) | ibge_censo2022 | `to_csv` l.2707 (estrutura_eixos.md) |  |
| `sidra_taxa_frequencia_0_6_raca_2022.csv` | sim | Família e Cuidados › Crianças até 72 meses frequentando escola/creche, por raça/cor | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.2620 (estrutura_eixos.md) |  |
| `sidra_taxa_frequencia_0_6_sexo_2022.csv` | sim | Família e Cuidados › Crianças até 72 meses frequentando escola/creche, por sexo | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.2621 (estrutura_eixos.md) |  |
| `sisvan_desnutricao_por_ano.csv` | sim | Alimentação › Desnutrição SISVAN (número) \| Desnutrição SISVAN (percentual) | — | SISVAN | ms_sisvan | `to_csv` l.2489 (estrutura_eixos.md) |  |
| `sisvan_sobrepeso_por_ano.csv` | sim | Alimentação › Sobrepeso SISVAN (número) \| Sobrepeso SISVAN (percentual) | — | SISVAN | ms_sisvan | `to_csv` l.2504 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_adensamento_bairro_2026.csv` | sim | Moradia › Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (mais de 2 pessoas por dormitório) | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.1062 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_criancas_0_a_4_2026.csv` | sim | Prioridade › Crianças até 72 meses no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.713 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_criancas_2026.csv` | sim | Prioridade › Crianças até 72 meses no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.680 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_deficiencia_bairro_2026.csv` | sim | Inclusão › Crianças no CadÚnico com alguma deficiência | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.996 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_inadequacao_bairro_2026.csv` | sim | Moradia › Crianças no CadÚnico em domicílios com inadequação habitacional | — | Cadastro Único (extração CTPE, jul/2026) | mds_cadunico | `to_csv` l.1062 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_recortes_bairro_2026.csv` | sim | Prioridade … › Famílias no CadÚnico com crianças até 72 meses, por sexo \| Famílias no CadÚnico com crianças até 72 meses, por raça/cor \| Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.908 (estrutura_eixos.md) |  |
| `tabela_mapa_mortalidade_infantil_2025.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.2418 (estrutura_eixos.md) |  |
| `tabela_mapa_nascidos_baixo_peso_2025.csv` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc | `to_csv` l.1234 (vizinhança) |  |
| `tabela_mapa_nascidos_vivos_2025.csv` | sim | Introdução › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) | — | DataSUS/Tabnet (nascidos vivos) | sms_rio_sinasc | `to_csv` l.1184 (estrutura_eixos.md) |  |
| `tabela_mapa_notif_autoprovocada_2026.csv` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3051 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_gravidez_2025.csv` | sim | Prioridade › Óbitos maternos durante a gravidez | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2186 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_neonatal_precoce_2025.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2281 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_neonatal_tardia_2025.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2335 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_puerperio_2025.csv` | sim | Prioridade › Óbitos maternos durante o puerpério | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2228 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_raca_total_2025.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.1432 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_mae_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2960 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_outros_2021_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2962 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_pai_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2961 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_taxa_mae_2025.csv` | não | — | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa (todas as idades) | — | isp_violencia2024 | `to_csv` l.3131 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_outros_2021_2025.csv` | não | — | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa (todas as idades) | — | isp_violencia2024 | `to_csv` l.3131 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_pai_2025.csv` | não | — | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa (todas as idades) | — | isp_violencia2024 | `to_csv` l.3131 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_mae_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.3157 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_outros_2021_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.3157 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_pai_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.3157 (vizinhança) |  |
| `tabela_mapa_violencia_territorial_ra_2024.csv` | sim | Direito ao Brincar › Violência territorial | — | Instituto de Segurança Pública (ISP-RJ), via Data.Rio, 2024, por Região Administrativa | isp_violencia2024 | `to_csv` l.3073 (estrutura_eixos.md) |  |
| `taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.1857 (estrutura_eixos.md) |  |
| `violencia_familiar_outros_detalhe.csv` | sim | Proteção › Violência familiar — composição de "outros" vínculos | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.2927 (estrutura_eixos.md) |  |
| `violencia_familiar_por_bairro.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2943 (estrutura_eixos.md) |  |
| `violencia_familiar_por_cap.csv` | sim | Proteção › Violência familiar — por CAP | — | Sinan NET/Tabnet (SMS-Rio); população 0 a 4 anos do Censo 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.3018 (estrutura_eixos.md) |  |
| `violencia_familiar_por_ra.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | — | sms_rio_sinan | `to_csv` l.3017 (vizinhança) |  |
| `violencia_familiar_por_vinculo_ano.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, ms_ripsa_populacao, sms_rio_sinan | `to_csv` l.2874 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_municipio_ano.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, ms_ripsa_populacao, sms_rio_sinan | `to_csv` l.2908 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_por_bairro.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.3116 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_top_bairros_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.3177 (estrutura_eixos.md) |  |
| `violencia_familiar_top_bairros_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.2994 (estrutura_eixos.md) |  |
| `violencia_territorial_por_ra_2024.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos | — | sms_rio_sinan | `to_csv` l.3072 (vizinhança) |  |

## 3. Alertas

Apontados, não corrigidos — cada item pede uma decisão da equipe.

### Arquivo no disco que nenhuma subseção de estrutura_eixos.md usa (29)

- mapas/mapa_mortalidade_infantil_bairro_2025.png
- mapas/mapa_obitos_neonatal_precoce_bairro_2025.png
- mapas/mapa_obitos_raca_total_bairro_2025.png
- mapas/mapa_percentual_cadunico_0_a_4_sobre_censo_bairro_2026.png
- mapas/mapa_taxa_mortalidade_infantil_bairro_2025.png
- mapas/mapa_violencia_familiar_mae_taxa_bairro_2025.png
- mapas/mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png
- mapas/mapa_violencia_familiar_pai_taxa_bairro_2025.png
- tabelas_finais/cadunico_adhoc_deficiencia_2026_08.csv
- tabelas_finais/cadunico_adhoc_deficiencia_contexto_2026_08.csv
- tabelas_finais/cadunico_adhoc_moradia_domicilio_2026_08.csv
- tabelas_finais/cadunico_adhoc_moradia_territorio_2026_08.csv
- tabelas_finais/cobertura_vacinal_epi_comparativo_anos.csv
- tabelas_finais/frequencia_escolar_pnad_por_idade.csv
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
- visualizacoes/pnad_frequencia_escolar_por_idade.png
- visualizacoes/sidra_frequencia_escola_0_5_raca_2022.png
- visualizacoes/sidra_frequencia_escola_0_5_sexo_2022.png

### Informativo: `fonte:` do .md e `fonte_dados` do analise.py citam conjuntos de bases diferentes (10)

- mapas/mapa_nascidos_vivos_bairro_2025.png — .md: “DataSUS/Tabnet (nascidos vivos)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- mapas/mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png — .md: “DataSUS/Tabnet municipal”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- mapas/mapa_taxa_obitos_raca_total_bairro_2025.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/nascidos_vivos_por_ano.png — .md: “DataSUS/Tabnet (nascidos vivos)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/obitos_gravidez_por_ano.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/obitos_puerperio_por_ano.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/obitos_raca_ano.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/percentual_mortalidade_raca_ano.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro. Nota: a categoria "Não informada" aparece só no gráfico de óbitos”
- visualizacoes/taxa_mortalidade_infantil_ano.png — .md: “DataSUS/Tabnet municipal”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- visualizacoes/taxa_mortalidade_pos_neonatal_ano.png — .md: “DataSUS/Tabnet municipal”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”

### Arquivo no disco que nenhuma chamada ativa de analise.py gera e que o relatório não usa (candidato a limpeza) (2)

- tabelas_finais/frequencia_escolar_pnad_por_idade.csv
- visualizacoes/pnad_frequencia_escolar_por_idade.png

### Entrada de fontes.bib que nenhum arquivo usa (2)

- ibge_pnadc
- mds_cadunico_adhoc

## 4. Referências a confirmar (`conferir` em fontes.bib)

- `ipp_datario_censo`: URL da tabela específica no Data.Rio; confirmar que a série 2000/2010 vem da mesma publicação
- `ms_ripsa_populacao`: URL exata da tabela consultada por carrega_populacao_ripsa
- `sms_rio_sim`: confirmar se a extração foi no TabNet da SMS-Rio (bairro de residência) ou no DATASUS nacional; URL
- `sms_rio_sinasc`: mesma dúvida do SIM (SMS-Rio ou DATASUS nacional); URL
- `sms_rio_sinan`: URL
- `sms_rio_epi_vacinal`: URL do painel e data da extração
- `mds_cadunico`: nome por extenso do órgão responsável pela extração (CTPE) e forma de citação acordada com o órgão
- `mds_cadunico_adhoc`: órgão que fez a extração pontual e forma de citação (specs/2026-09-29_dados_adhoc)
- `ibge_pnadc`: número da tabela SIDRA e ano de referência
- `isp_violencia2024`: URL do conjunto de dados
- `ipp_limites_bairros`: URL; entradas equivalentes para as CAP (SMS-Rio) e as malhas do IBGE usadas no contexto dos mapas
