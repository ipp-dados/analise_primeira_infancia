# Inventário de fontes

> Gerado por `relatorio/latex/build/inventario_fontes.py` em 25/09/2026 — **não editar à mão**.
> Documento de conferência da equipe (`specs/relatorio_latex` §7); não entra no relatório.
> Cruza `analise.py` (leitura estática), `specs/estrutura_eixos.md` e `relatorio/latex/fontes.bib`.
> A versão em planilha, com todos os campos, é `relatorio/inventario_fontes.csv` (separador `;`).

## Resumo

| | Gráficos | Mapas | Tabelas |
| :--- | ---: | ---: | ---: |
| No disco | 71 | 41 | 88 |
| No relatório (estrutura_eixos.md) | 71 | 40 | 79 |
| Com fonte ligada ao fontes.bib | 71 | 41 | 88 |

## 1. Por fonte

Cada entrada de `fontes.bib` (lista **Fontes** do relatório) e o que ela gera. Só arquivos que entram no relatório; os demais estão na seção 2. Um arquivo com fonte composta (ex. casos do Sinan ÷ população do Censo) aparece em mais de uma fonte.

### Censo Demográfico 2022: população residente, por idade, sexo e cor ou raça

`ibge_censo2022` — INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `censo_sidra_populacao_0_6_raca_2022.png` | Inclusão › Crianças até 6 anos, por raça/cor |
| gráfico | `censo_sidra_populacao_0_6_sexo_2022.png` | Inclusão › Crianças até 6 anos, por sexo |
| gráfico | `sidra_frequencia_escola_0_5_raca_2022.png` | Inclusão › Crianças até 6 anos frequentando escola/creche, por raça/cor |
| gráfico | `sidra_frequencia_escola_0_5_sexo_2022.png` | Inclusão › Crianças até 6 anos frequentando escola/creche, por sexo |
| gráfico | `sidra_frequencia_escola_0_5_total_2022.png` | Família e Cuidados › Crianças até 6 anos frequentando escola/creche (geral) |
| gráfico | `sidra_taxa_frequencia_0_6_raca_2022.png` | Inclusão › Crianças até 6 anos frequentando escola/creche, por raça/cor |
| gráfico | `sidra_taxa_frequencia_0_6_sexo_2022.png` | Inclusão › Crianças até 6 anos frequentando escola/creche, por sexo |
| tabela | `censo_sidra_populacao_0_6_raca_2022.csv` | Inclusão › Crianças até 6 anos, por raça/cor |
| tabela | `censo_sidra_populacao_0_6_sexo_2022.csv` | Inclusão › Crianças até 6 anos, por sexo |
| tabela | `sidra_frequencia_escola_0_5_raca_2022.csv` | Inclusão › Crianças até 6 anos frequentando escola/creche, por raça/cor |
| tabela | `sidra_frequencia_escola_0_5_sexo_2022.csv` | Inclusão › Crianças até 6 anos frequentando escola/creche, por sexo |
| tabela | `sidra_frequencia_escola_0_5_total_2022.csv` | Família e Cuidados › Crianças até 6 anos frequentando escola/creche (geral) |
| tabela | `sidra_taxa_frequencia_0_6_raca_2022.csv` | Inclusão › Crianças até 6 anos frequentando escola/creche, por raça/cor |
| tabela | `sidra_taxa_frequencia_0_6_sexo_2022.csv` | Inclusão › Crianças até 6 anos frequentando escola/creche, por sexo |

### População residente por bairro: Censos Demográficos 2000, 2010 e 2022

`ipp_datario_censo` — INSTITUTO PEREIRA PASSOS  
⚠️ **Conferir:** URL da tabela específica no Data.Rio; confirmar que a série 2000/2010 vem da mesma publicação

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `censo_0_a_4_serie_percentual_ano.png` | Prioridade › Crianças até 4 anos (percentual) |
| gráfico | `censo_0_a_4_serie_total_ano.png` | Prioridade › Crianças até 4 anos (número) |
| gráfico | `violencia_familiar_taxa_top_bairros_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_censo_0_4_absoluto.png` | Prioridade › Crianças até 4 anos (número) |
| mapa | `mapa_censo_0_4_percentual.png` | Prioridade › Crianças até 4 anos (percentual) |
| mapa | `mapa_violencia_familiar_mae_taxa_bairro_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_mae_taxa_ra_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_pai_taxa_bairro_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_pai_taxa_ra_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `censo_0_a_4_anos_por_ano.csv` | Prioridade › Crianças até 4 anos (número) \| Crianças até 4 anos (percentual) |
| tabela | `censo_por_bairro.csv` | Prioridade › Crianças até 4 anos (número) |
| tabela | `violencia_familiar_por_cap.csv` | Proteção › Violência familiar — por CAP |
| tabela | `violencia_familiar_taxa_municipio_ano.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `violencia_familiar_taxa_por_bairro.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `violencia_familiar_taxa_top_bairros_2025.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |

### Estimativas populacionais por município, idade e sexo, 2000-2025 (Ripsa)

`ms_ripsa_populacao` — BRASIL. Ministério da Saúde  
⚠️ **Conferir:** URL exata da tabela consultada por carrega_populacao_ripsa

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `populacao_ripsa_0_a_6_percentual_por_ano.png` | Prioridade › Crianças até 6 anos (número) |
| gráfico | `populacao_ripsa_0_a_6_por_ano.png` | Prioridade › Crianças até 6 anos (número) |
| gráfico | `taxa_atendimento_0_a_5_por_ano.png` | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos |
| gráfico | `violencia_familiar_taxa_municipio_ano.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `cadunico_razao_populacao_0_a_5_2026.csv` | Inclusão › Crianças de 0 a 5 anos no CadÚnico em relação à população do município |
| tabela | `matriculas_0_a_5_por_ano.csv` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos |
| tabela | `populacao_ripsa_0_a_6_por_ano.csv` | Prioridade › Crianças até 6 anos (número) |
| tabela | `violencia_familiar_taxa_municipio_ano.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `violencia_familiar_taxa_por_bairro.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `violencia_familiar_taxa_top_bairros_2025.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |

### Sistema de Informações sobre Mortalidade (SIM): óbitos de residentes no município do Rio de Janeiro

`sms_rio_sim` — RIO DE JANEIRO (RJ). Secretaria Municipal de Saúde  
⚠️ **Conferir:** confirmar se a extração foi no TabNet da SMS-Rio (bairro de residência) ou no DATASUS nacional; URL

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `nascidos_abaixo_peso_percentual_por_ano.png` | Alimentação › Baixo peso ao nascer (percentual) |
| gráfico | `nascidos_vivos_por_ano.png` | Prioridade › Nascidos vivos por bairro de residência da mãe (número) |
| gráfico | `obitos_causas_evitaveis_grupo_0_a_6_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_grupo_28_a_364_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_grupo_7_a_27_dias_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_grupo_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) |
| gráfico | `obitos_causas_evitaveis_raca_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor |
| gráfico | `obitos_causas_evitaveis_raca_sem_nao_informado_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor |
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
| gráfico | `obitos_gravidez_por_ano.png` | Prioridade › Razão de mortalidade materna (durante a gravidez) |
| gráfico | `obitos_puerperio_por_ano.png` | Prioridade › Razão de mortalidade materna (durante puerpério) |
| gráfico | `obitos_raca_ano.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| gráfico | `percentual_evitaveis_cap_1_a_4_anos_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `percentual_evitaveis_cap_menores_1_ano_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `percentual_evitaveis_cap_menores_5_anos_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `percentual_mortalidade_causas_evitaveis_raca_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor |
| gráfico | `percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor |
| gráfico | `percentual_mortalidade_raca_ano.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| gráfico | `taxa_mortalidade_evitaveis_menores_5_ano.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| gráfico | `taxa_mortalidade_infantil_ano.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| gráfico | `taxa_mortalidade_pos_neonatal_ano.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| gráfico | `taxa_mortalidade_precoce_ano.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| gráfico | `taxa_obitos_tardios_ano.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_mortalidade_infantil_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_nascidos_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (número) |
| mapa | `mapa_nascidos_vivos_bairro_2025.png` | Prioridade › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| mapa | `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_gravidez_bairro_2025.png` | Prioridade › Razão de mortalidade materna (durante a gravidez) |
| mapa | `mapa_obitos_neonatal_precoce_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| mapa | `mapa_obitos_neonatal_tardia_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_obitos_pos_neonatal_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_obitos_puerperio_bairro_2025.png` | Prioridade › Razão de mortalidade materna (durante puerpério) |
| mapa | `mapa_obitos_raca_total_bairro_2025.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
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
| tabela | `mortalidade_causas_evitaveis_raca_municipio_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor |
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
| tabela | `obitos_gravidez_bairro_ano.csv` | Prioridade › Razão de mortalidade materna (durante a gravidez) |
| tabela | `obitos_gravidez_por_ano.csv` | Prioridade › Razão de mortalidade materna (durante a gravidez) |
| tabela | `obitos_puerperio_bairro_ano.csv` | Prioridade › Razão de mortalidade materna (durante puerpério) |
| tabela | `obitos_puerperio_por_ano.csv` | Prioridade › Razão de mortalidade materna (durante puerpério) |
| tabela | `tabela_mapa_mortalidade_infantil_2025.csv` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| tabela | `tabela_mapa_obitos_gravidez_2025.csv` | Prioridade › Razão de mortalidade materna (durante a gravidez) |
| tabela | `tabela_mapa_obitos_neonatal_precoce_2025.csv` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| tabela | `tabela_mapa_obitos_neonatal_tardia_2025.csv` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| tabela | `tabela_mapa_obitos_puerperio_2025.csv` | Prioridade › Razão de mortalidade materna (durante puerpério) |
| tabela | `tabela_mapa_obitos_raca_total_2025.csv` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| tabela | `taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |

### Sistema de Informações sobre Nascidos Vivos (SINASC): nascimentos de mães residentes no município do Rio de Janeiro

`sms_rio_sinasc` — RIO DE JANEIRO (RJ). Secretaria Municipal de Saúde  
⚠️ **Conferir:** mesma dúvida do SIM (SMS-Rio ou DATASUS nacional); URL

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `nascidos_abaixo_peso_percentual_por_ano.png` | Alimentação › Baixo peso ao nascer (percentual) |
| gráfico | `nascidos_vivos_por_ano.png` | Prioridade › Nascidos vivos por bairro de residência da mãe (número) |
| gráfico | `obitos_gravidez_por_ano.png` | Prioridade › Razão de mortalidade materna (durante a gravidez) |
| gráfico | `obitos_puerperio_por_ano.png` | Prioridade › Razão de mortalidade materna (durante puerpério) |
| gráfico | `obitos_raca_ano.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| gráfico | `percentual_mortalidade_raca_ano.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| gráfico | `taxa_mortalidade_infantil_ano.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| gráfico | `taxa_mortalidade_pos_neonatal_ano.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| gráfico | `taxa_mortalidade_precoce_ano.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| gráfico | `taxa_obitos_tardios_ano.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_mortalidade_infantil_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_nascidos_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (número) |
| mapa | `mapa_nascidos_vivos_bairro_2025.png` | Prioridade › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| mapa | `mapa_obitos_neonatal_precoce_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| mapa | `mapa_obitos_neonatal_tardia_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_obitos_raca_total_bairro_2025.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
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
| tabela | `nascidos_vivos_por_ano.csv` | Prioridade › Nascidos vivos por bairro de residência da mãe (número) |
| tabela | `tabela_mapa_nascidos_vivos_2025.csv` | Prioridade › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| tabela | `tabela_mapa_obitos_neonatal_precoce_2025.csv` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| tabela | `tabela_mapa_obitos_neonatal_tardia_2025.csv` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |

### Sistema de Informação de Agravos de Notificação (Sinan): notificações de violência interpessoal e autoprovocada

`sms_rio_sinan` — RIO DE JANEIRO (RJ). Secretaria Municipal de Saúde  
⚠️ **Conferir:** URL

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `notif_autoprovocada_antes_2026_vs_2026.png` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| gráfico | `violencia_familiar_outros_serie.png` | Proteção › Violência familiar — composição de "outros" vínculos |
| gráfico | `violencia_familiar_serie_vinculos.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| gráfico | `violencia_familiar_taxa_municipio_ano.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| gráfico | `violencia_familiar_taxa_top_bairros_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| gráfico | `violencia_familiar_top_bairros_2025.png` | Proteção › Violência familiar — bairros com mais notificações (2025) |
| mapa | `mapa_notif_autoprovocada_bairro_2026.png` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| mapa | `mapa_violencia_familiar_mae_bairro_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_mae_taxa_bairro_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_mae_taxa_ra_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_outros_bairro_2021_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_pai_bairro_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_pai_taxa_bairro_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_pai_taxa_ra_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `notif_autoprovocada_por_bairro_ano.csv` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| tabela | `tabela_mapa_notif_autoprovocada_2026.csv` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| tabela | `tabela_mapa_violencia_familiar_mae_2025.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `tabela_mapa_violencia_familiar_outros_2021_2025.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `tabela_mapa_violencia_familiar_pai_2025.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `violencia_familiar_outros_detalhe.csv` | Proteção › Violência familiar — composição de "outros" vínculos |
| tabela | `violencia_familiar_por_bairro.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `violencia_familiar_por_cap.csv` | Proteção › Violência familiar — por CAP |
| tabela | `violencia_familiar_por_vinculo_ano.csv` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| tabela | `violencia_familiar_taxa_municipio_ano.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `violencia_familiar_taxa_por_bairro.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `violencia_familiar_taxa_top_bairros_2025.csv` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| tabela | `violencia_familiar_top_bairros_2025.csv` | Proteção › Violência familiar — bairros com mais notificações (2025) |

### Sistema de Vigilância Alimentar e Nutricional (SISVAN): relatórios públicos de estado nutricional

`ms_sisvan` — BRASIL. Ministério da Saúde

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `sisvan_desnutricao_percentual_por_ano.png` | Alimentação › Desnutrição SISVAN (percentual) |
| gráfico | `sisvan_obesidade_percentual_por_ano.png` | Alimentação › Sobrepeso SISVAN (percentual) |
| gráfico | `sisvan_sobrepeso_percentual_por_ano.png` | Alimentação › Sobrepeso SISVAN (percentual) |
| tabela | `sisvan_desnutricao_por_ano.csv` | Alimentação › Desnutrição SISVAN (número) \| Desnutrição SISVAN (percentual) |
| tabela | `sisvan_sobrepeso_por_ano.csv` | Alimentação › Sobrepeso SISVAN (número) \| Sobrepeso SISVAN (percentual) |

### Cobertura vacinal por imunobiológico, 2016-2026

`sms_rio_epi_vacinal` — RIO DE JANEIRO (RJ). Secretaria Municipal de Saúde. Superintendência de Vigilância em Saúde  
⚠️ **Conferir:** URL do painel e data da extração

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `cobertura_vacinal_epi_ano.png` | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos |
| gráfico | `cobertura_vacinal_epi_comparativo_anos.png` | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos |
| tabela | `cobertura_vacinal_epi_comparativo_anos.csv` | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos |
| tabela | `cobertura_vacinal_epi_por_ano.csv` | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos |

### Cadastro Único para Programas Sociais: base de famílias e pessoas do município do Rio de Janeiro

`mds_cadunico` — BRASIL. Ministério do Desenvolvimento e Assistência Social, Família e Combate à Fome  
⚠️ **Conferir:** nome por extenso do órgão responsável pela extração (CTPE) e forma de citação acordada com o órgão

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `cadunico_criancas_por_faixa_renda.png` | Família e Cuidados › Famílias com crianças até 6 anos no Cadastro Único, por renda |
| gráfico | `cadunico_criancas_por_idade.png` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) |
| gráfico | `cadunico_criancas_por_raca_cor.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| gráfico | `cadunico_criancas_por_sexo.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por sexo |
| gráfico | `cadunico_familias_arranjo_renda.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| gráfico | `cadunico_familias_por_arranjo.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| gráfico | `cadunico_familias_por_faixa_renda.png` | Família e Cuidados › Famílias com crianças até 6 anos no Cadastro Único, por renda |
| gráfico | `cadunico_familias_por_idade.png` | Família e Cuidados › Famílias com crianças até 6 anos no Cadastro Único (número) |
| gráfico | `cadunico_familias_por_raca_cor.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| gráfico | `cadunico_familias_por_sexo_criancas.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por sexo |
| mapa | `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) |
| mapa | `mapa_cadunico_criancas_bairro_2026.png` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) |
| mapa | `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| mapa | `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| tabela | `cadunico_familias_arranjo_renda_2026.csv` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| tabela | `cadunico_familias_por_arranjo_2026.csv` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| tabela | `cadunico_por_bairro_2026.csv` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) \| Famílias com crianças até 6 anos no Cadastro Único (número) |
| tabela | `cadunico_por_bairro_ate_4_2026.csv` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) |
| tabela | `cadunico_por_faixa_renda_2026.csv` | Família e Cuidados › Famílias com crianças até 6 anos no Cadastro Único, por renda |
| tabela | `cadunico_por_idade_2026.csv` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) \| Famílias com crianças até 6 anos no Cadastro Único (número) |
| tabela | `cadunico_por_raca_cor_2026.csv` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| tabela | `cadunico_por_sexo_2026.csv` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por sexo |
| tabela | `cadunico_razao_populacao_0_a_5_2026.csv` | Inclusão › Crianças de 0 a 5 anos no CadÚnico em relação à população do município |
| tabela | `tabela_mapa_cadunico_criancas_0_a_4_2026.csv` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) |
| tabela | `tabela_mapa_cadunico_criancas_2026.csv` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) |
| tabela | `tabela_mapa_cadunico_recortes_bairro_2026.csv` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por sexo \| Famílias no CadÚnico com crianças até 6 anos, por raça/cor \| Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |

### Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua): educação

`ibge_pnadc` — INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA  
⚠️ **Conferir:** número da tabela SIDRA e ano de referência

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `pnad_frequencia_escolar_por_idade.png` | Família e Cuidados › Taxa bruta de frequência escolar da população até 6 anos |
| tabela | `frequencia_escolar_pnad_por_idade.csv` | Família e Cuidados › Taxa bruta de frequência escolar da população até 6 anos |

### Censo Escolar da Educação Básica: microdados, 2007-2025

`inep_censo_escolar` — INSTITUTO NACIONAL DE ESTUDOS E PESQUISAS EDUCACIONAIS ANÍSIO TEIXEIRA

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| gráfico | `matriculas_0_a_5_creche_pre_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `matriculas_0_a_5_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `matriculas_0_a_5_rede_por_ano.png` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos |
| gráfico | `taxa_atendimento_0_a_5_por_ano.png` | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos |
| tabela | `matriculas_0_a_5_por_ano.csv` | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos |

### Índice de Progresso Social do Rio de Janeiro 2024: indicadores por Região Administrativa

`ipp_ips2024` — INSTITUTO PEREIRA PASSOS  
⚠️ **Conferir:** URL do conjunto de dados

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| mapa | `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png` | Proteção › Violência territorial |
| mapa | `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png` | Proteção › Violência territorial |
| mapa | `mapa_violencia_territorial_homicidios_ra_2024.png` | Proteção › Violência territorial |
| tabela | `tabela_mapa_violencia_territorial_ra_2024.csv` | Proteção › Violência territorial |

### Limite de bairros do município do Rio de Janeiro

`ipp_limites_bairros` — INSTITUTO PEREIRA PASSOS  
⚠️ **Conferir:** URL; entradas equivalentes para as CAP (SMS-Rio) e as malhas do IBGE usadas no contexto dos mapas

| Tipo | Arquivo | Eixo › subseção |
| :--- | :--- | :--- |
| mapa | `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) |
| mapa | `mapa_cadunico_criancas_bairro_2026.png` | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) |
| mapa | `mapa_censo_0_4_absoluto.png` | Prioridade › Crianças até 4 anos (número) |
| mapa | `mapa_censo_0_4_percentual.png` | Prioridade › Crianças até 4 anos (percentual) |
| mapa | `mapa_mortalidade_infantil_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_nascidos_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (número) |
| mapa | `mapa_nascidos_vivos_bairro_2025.png` | Prioridade › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) |
| mapa | `mapa_notif_autoprovocada_bairro_2026.png` | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) |
| mapa | `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_obitos_gravidez_bairro_2025.png` | Prioridade › Razão de mortalidade materna (durante a gravidez) |
| mapa | `mapa_obitos_neonatal_precoce_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| mapa | `mapa_obitos_neonatal_tardia_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_obitos_pos_neonatal_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_obitos_puerperio_bairro_2025.png` | Prioridade › Razão de mortalidade materna (durante puerpério) |
| mapa | `mapa_obitos_raca_total_bairro_2025.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| mapa | `mapa_percentual_baixo_peso_bairro_2025.png` | Alimentação › Baixo peso ao nascer (percentual) |
| mapa | `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor |
| mapa | `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar |
| mapa | `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png` | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) |
| mapa | `mapa_taxa_mortalidade_infantil_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png` | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) |
| mapa | `mapa_taxa_mortalidade_precoce_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) |
| mapa | `mapa_taxa_obitos_raca_total_bairro_2025.png` | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) |
| mapa | `mapa_taxa_obitos_tardios_bairro_2025.png` | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) |
| mapa | `mapa_violencia_familiar_mae_bairro_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_mae_taxa_bairro_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_mae_taxa_ra_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_outros_bairro_2021_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_pai_bairro_2025.png` | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) |
| mapa | `mapa_violencia_familiar_pai_taxa_bairro_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_familiar_pai_taxa_ra_2025.png` | Proteção › Taxa de notificações de violência (0 a 6 anos) |
| mapa | `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png` | Proteção › Violência territorial |
| mapa | `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png` | Proteção › Violência territorial |
| mapa | `mapa_violencia_territorial_homicidios_ra_2024.png` | Proteção › Violência territorial |

## 2. Por arquivo

Todos os gráficos, mapas e tabelas no disco. **Fonte (analise.py)** é o `fonte_dados` da chamada que gera o arquivo; para tabelas, a última fonte vista antes do `to_csv` (método *vizinhança* — confira). **Fonte (.md)** é o campo `fonte:` da subseção em `estrutura_eixos.md`.

### Gráficos (71)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `cadunico_criancas_por_faixa_renda.png` | sim | Família e Cuidados › Famílias com crianças até 6 anos no Cadastro Único, por renda | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.1756 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `cadunico_criancas_por_idade.png` | sim | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.1786 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `cadunico_criancas_por_raca_cor.png` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.2023 (chamada) |  |
| `cadunico_criancas_por_sexo.png` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por sexo | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.1991 (chamada) |  |
| `cadunico_familias_arranjo_renda.png` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra_agrupado` l.2086 (chamada) |  |
| `cadunico_familias_por_arranjo.png` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.2079 (chamada) |  |
| `cadunico_familias_por_faixa_renda.png` | sim | Família e Cuidados › Famílias com crianças até 6 anos no Cadastro Único, por renda | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.1747 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `cadunico_familias_por_idade.png` | sim | Família e Cuidados › Famílias com crianças até 6 anos no Cadastro Único (número) | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.1778 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `cadunico_familias_por_raca_cor.png` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.2028 (chamada) |  |
| `cadunico_familias_por_sexo_criancas.png` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por sexo | CadÚnico (extração CTPE, …/…) | Cadastro Único (extração CTPE) | mds_cadunico | `grafico_barra` l.1997 (chamada) |  |
| `censo_0_a_4_serie_percentual_ano.png` | sim | Prioridade › Crianças até 4 anos (percentual) | — | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | — | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `censo_0_a_4_serie_total_ano.png` | sim | Prioridade › Crianças até 4 anos (número) | — | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | — | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `censo_sidra_populacao_0_6_raca_2022.png` | sim | Inclusão › Crianças até 6 anos, por raça/cor | Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.1455 (chamada) |  |
| `censo_sidra_populacao_0_6_sexo_2022.png` | sim | Inclusão › Crianças até 6 anos, por sexo | Censo Demográfico 2022 (IBGE/SIDRA, tabela 9606) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.1464 (chamada) |  |
| `cobertura_vacinal_epi_ano.png` | sim | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos | — | Epi Rio | sms_rio_epi_vacinal | — | chamada comentada em analise.py (arquivo antigo) |
| `cobertura_vacinal_epi_comparativo_anos.png` | sim | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos | EPI/SVS-Rio, cobertura vacinal por imunobiológico | Epi Rio | sms_rio_epi_vacinal | `grafico_barra_agrupado` l.3517 (chamada) |  |
| `matriculas_0_a_5_creche_pre_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal_multipla` l.3679 (chamada) |  |
| `matriculas_0_a_5_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal` l.3675 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `matriculas_0_a_5_rede_por_ano.png` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos | Censo Escolar da Educação Básica (INEP), microdados | Censo Escolar da Educação Básica (INEP), microdados | inep_censo_escolar | `serie_temporal_multipla` l.3686 (chamada) |  |
| `nascidos_abaixo_peso_percentual_por_ano.png` | sim | Alimentação › Baixo peso ao nascer (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2257 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `nascidos_vivos_por_ano.png` | sim | Prioridade › Nascidos vivos por bairro de residência da mãe (número) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (nascidos vivos) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.2198 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `notif_autoprovocada_antes_2026_vs_2026.png` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | Sinan NET/Tabnet (SMS-Rio). 2026 parcial; possível mudança de registro (hipótese) | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `grafico_barra` l.3962 (chamada) |  |
| `obitos_causas_evitaveis_grupo_0_a_6_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2641 (chamada) |  |
| `obitos_causas_evitaveis_grupo_28_a_364_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2739 (chamada) |  |
| `obitos_causas_evitaveis_grupo_7_a_27_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2690 (chamada) |  |
| `obitos_causas_evitaveis_grupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2586 (chamada) |  |
| `obitos_causas_evitaveis_raca_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor | — | DataSUS (SIM) | sms_rio_sim | — | chamada comentada em analise.py (arquivo antigo) |
| `obitos_causas_evitaveis_raca_sem_nao_informado_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor | — | DataSUS (SIM) | sms_rio_sim | — | chamada comentada em analise.py (arquivo antigo) |
| `obitos_causas_evitaveis_subgrupo_0_a_6_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2657 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_28_a_364_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2755 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_7_a_27_dias_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2706 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2602 (chamada) |  |
| `obitos_causas_evitaveis_subgrupo_faixa_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `grafico_barra_agrupado` l.2794 (chamada) |  |
| `obitos_evitaveis_1_a_4_anos_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2879 (chamada) |  |
| `obitos_evitaveis_cap_1_a_4_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.2933 (chamada) |  |
| `obitos_evitaveis_cap_menores_1_ano_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.2933 (chamada) |  |
| `obitos_evitaveis_cap_menores_5_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.2933 (chamada) |  |
| `obitos_evitaveis_menores_1_ano_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2879 (chamada) |  |
| `obitos_evitaveis_menores_5_subgrupo_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `serie_temporal_multipla` l.2837 (chamada) |  |
| `obitos_evitaveis_total_cap_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.2961 (chamada) |  |
| `obitos_gravidez_por_ano.png` | sim | Prioridade › Razão de mortalidade materna (durante a gravidez) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.3134 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `obitos_puerperio_por_ano.png` | sim | Prioridade › Razão de mortalidade materna (durante puerpério) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.3177 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `obitos_raca_ano.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal_multipla` l.2374 (chamada) |  |
| `percentual_evitaveis_cap_1_a_4_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.2945 (chamada) |  |
| `percentual_evitaveis_cap_menores_1_ano_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.2945 (chamada) |  |
| `percentual_evitaveis_cap_menores_5_anos_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal_multipla` l.2945 (chamada) |  |
| `percentual_mortalidade_causas_evitaveis_raca_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor | — | DataSUS (SIM) | sms_rio_sim | — | chamada comentada em analise.py (arquivo antigo) |
| `percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor | — | DataSUS (SIM) | sms_rio_sim | — | chamada comentada em analise.py (arquivo antigo) |
| `percentual_mortalidade_raca_ano.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc | `serie_temporal_multipla` l.2391 (chamada) |  |
| `pnad_frequencia_escolar_por_idade.png` | sim | Família e Cuidados › Taxa bruta de frequência escolar da população até 6 anos | PNAD Contínua (IBGE) | PNAD Contínua | ibge_pnadc | `grafico_barra` l.3631 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `populacao_ripsa_0_a_6_percentual_por_ano.png` | sim | Prioridade › Crianças até 6 anos (número) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `serie_temporal` l.1667 (chamada) |  |
| `populacao_ripsa_0_a_6_por_ano.png` | sim | Prioridade › Crianças até 6 anos (número) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `serie_temporal` l.1663 (chamada) |  |
| `sidra_frequencia_escola_0_5_raca_2022.png` | sim | Inclusão › Crianças até 6 anos frequentando escola/creche, por raça/cor | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.3569 (chamada) |  |
| `sidra_frequencia_escola_0_5_sexo_2022.png` | sim | Inclusão › Crianças até 6 anos frequentando escola/creche, por sexo | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.3578 (chamada) |  |
| `sidra_frequencia_escola_0_5_total_2022.png` | sim | Família e Cuidados › Crianças até 6 anos frequentando escola/creche (geral) | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA, tabela 10057) | ibge_censo2022 | `grafico_barra` l.3594 (chamada) |  |
| `sidra_taxa_frequencia_0_6_raca_2022.png` | sim | Inclusão › Crianças até 6 anos frequentando escola/creche, por raça/cor | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.3599 (chamada) |  |
| `sidra_taxa_frequencia_0_6_sexo_2022.png` | sim | Inclusão › Crianças até 6 anos frequentando escola/creche, por sexo | Censo Demográfico 2022 (IBGE/SIDRA, tabelas 10056/10057) | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `grafico_barra_agrupado` l.3608 (chamada) |  |
| `sisvan_desnutricao_percentual_por_ano.png` | sim | Alimentação › Desnutrição SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.3438 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `sisvan_obesidade_percentual_por_ano.png` | sim | Alimentação › Sobrepeso SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.3462 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `sisvan_sobrepeso_percentual_por_ano.png` | sim | Alimentação › Sobrepeso SISVAN (percentual) | SISVAN/DATASUS | SISVAN | ms_sisvan | `serie_temporal` l.3454 (chamada) | regravado por regen_missing_pngs.py (cópia sem fonte) |
| `taxa_atendimento_0_a_5_por_ano.png` | sim | Família e Cuidados › Taxa bruta de atendimento escolar de 0 a 5 anos | Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | ms_ripsa_populacao, inep_censo_escolar | `serie_temporal_multipla` l.3712 (chamada) |  |
| `taxa_mortalidade_evitaveis_menores_5_ano.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `serie_temporal` l.2849 (chamada) |  |
| `taxa_mortalidade_infantil_ano.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.3397 (chamada) |  |
| `taxa_mortalidade_pos_neonatal_ano.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.3370 (chamada) |  |
| `taxa_mortalidade_precoce_ano.png` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.3233 (chamada) |  |
| `taxa_obitos_tardios_ano.png` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `serie_temporal` l.3287 (chamada) |  |
| `violencia_familiar_outros_serie.png` | sim | Proteção › Violência familiar — composição de "outros" vínculos | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `serie_temporal_multipla` l.3850 (chamada) |  |
| `violencia_familiar_serie_vinculos.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `serie_temporal_multipla_marcos` l.3804 (chamada) |  |
| `violencia_familiar_taxa_municipio_ano.png` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 5 anos: estimativas Ripsa/Ministério da Saúde | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ms_ripsa_populacao, sms_rio_sinan | `serie_temporal_multipla_marcos` l.3831 (chamada) |  |
| `violencia_familiar_taxa_top_bairros_2025.png` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio); bairros com 100+ crianças | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan | `grafico_barra_agrupado` l.4103 (chamada) |  |
| `violencia_familiar_top_bairros_2025.png` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `grafico_barra_agrupado` l.3916 (chamada) |  |

### Mapas (41)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | sim | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.1936 (chamada) |  |
| `mapa_cadunico_criancas_bairro_2026.png` | sim | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.1908 (chamada) |  |
| `mapa_censo_0_4_absoluto.png` | sim | Prioridade › Crianças até 4 anos (número) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo, ipp_limites_bairros | `mapa_coropletico_bairros` l.1498 (chamada) |  |
| `mapa_censo_0_4_percentual.png` | sim | Prioridade › Crianças até 4 anos (percentual) | Censo Demográfico 2022 (IBGE/Data.Rio) | Censo Demográfico 2022 (IBGE) | ipp_datario_censo, ipp_limites_bairros | `mapa_coropletico_bairros` l.1513 (chamada) |  |
| `mapa_mortalidade_infantil_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.3408 (chamada) |  |
| `mapa_nascidos_baixo_peso_bairro_2025.png` | sim | Alimentação › Baixo peso ao nascer (número) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2228 (chamada) |  |
| `mapa_nascidos_vivos_bairro_2025.png` | sim | Prioridade › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (nascidos vivos) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2178 (chamada) |  |
| `mapa_notif_autoprovocada_bairro_2026.png` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3973 (chamada) |  |
| `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.3038 (chamada) |  |
| `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.3038 (chamada) |  |
| `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.3038 (chamada) |  |
| `mapa_obitos_gravidez_bairro_2025.png` | sim | Prioridade › Razão de mortalidade materna (durante a gravidez) | — | DataSUS/Tabnet (SIM) | sms_rio_sim, ipp_limites_bairros | — | chamada comentada em analise.py (arquivo antigo) |
| `mapa_obitos_neonatal_precoce_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.3247 (chamada) |  |
| `mapa_obitos_neonatal_tardia_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | — | chamada comentada em analise.py (arquivo antigo) |
| `mapa_obitos_pos_neonatal_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim, ipp_limites_bairros | — | chamada comentada em analise.py (arquivo antigo) |
| `mapa_obitos_puerperio_bairro_2025.png` | sim | Prioridade › Razão de mortalidade materna (durante puerpério) | — | DataSUS/Tabnet (SIM) | sms_rio_sim, ipp_limites_bairros | — | chamada comentada em analise.py (arquivo antigo) |
| `mapa_obitos_raca_total_bairro_2025.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2411 (chamada) |  |
| `mapa_percentual_baixo_peso_bairro_2025.png` | sim | Alimentação › Baixo peso ao nascer (percentual) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2234 (chamada) |  |
| `mapa_percentual_cadunico_0_a_4_sobre_censo_bairro_2026.png` | não | — | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos; população 0 a 4 anos: Censo 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.1942 (chamada) |  |
| `mapa_percentual_cadunico_criancas_negras_bairro_2026.png` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.2133 (chamada) |  |
| `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | CadÚnico (extração CTPE, …/…). Bairro atribuído pelo CEP (Correios), pode divergir do bairro oficial; bairros com menos de 20 famílias suprimidos | Cadastro Único (extração CTPE) | mds_cadunico, ipp_limites_bairros | `mapa_coropletico_bairros` l.2133 (chamada) |  |
| `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.3048 (chamada) |  |
| `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.3048 (chamada) |  |
| `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | SIM/SVS-Rio (TabWin), óbitos de residentes no município do Rio de Janeiro | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim, ipp_limites_bairros | `mapa_coropletico_bairros` l.3048 (chamada) |  |
| `mapa_taxa_mortalidade_infantil_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.3414 (chamada) |  |
| `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet municipal | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.3386 (chamada) |  |
| `mapa_taxa_mortalidade_precoce_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.3253 (chamada) |  |
| `mapa_taxa_obitos_raca_total_bairro_2025.png` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.2417 (chamada) |  |
| `mapa_taxa_obitos_tardios_bairro_2025.png` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc, ipp_limites_bairros | `mapa_coropletico_bairros` l.3307 (chamada) |  |
| `mapa_violencia_familiar_mae_bairro_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3885 (chamada) |  |
| `mapa_violencia_familiar_mae_taxa_bairro_2025.png` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.4057 (chamada) |  |
| `mapa_violencia_familiar_mae_taxa_ra_2025.png` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.4083 (chamada) |  |
| `mapa_violencia_familiar_outros_bairro_2021_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3897 (chamada) |  |
| `mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.4057 (chamada) |  |
| `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.4083 (chamada) |  |
| `mapa_violencia_familiar_pai_bairro_2025.png` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.3891 (chamada) |  |
| `mapa_violencia_familiar_pai_taxa_bairro_2025.png` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.4057 (chamada) |  |
| `mapa_violencia_familiar_pai_taxa_ra_2025.png` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, sms_rio_sinan, ipp_limites_bairros | `mapa_coropletico_bairros` l.4083 (chamada) |  |
| `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png` | sim | Proteção › Violência territorial | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa | ipp_ips2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.4003 (chamada) |  |
| `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png` | sim | Proteção › Violência territorial | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa | ipp_ips2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.4003 (chamada) |  |
| `mapa_violencia_territorial_homicidios_ra_2024.png` | sim | Proteção › Violência territorial | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa | ipp_ips2024, ipp_limites_bairros | `mapa_coropletico_bairros` l.4003 (chamada) |  |

### Tabelas (88)

| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `cadunico_familias_arranjo_renda_2026.csv` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.2073 (estrutura_eixos.md) |  |
| `cadunico_familias_por_arranjo_2026.csv` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.2048 (estrutura_eixos.md) |  |
| `cadunico_por_bairro_2026.csv` | sim | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) \| Famílias com crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.1839 (estrutura_eixos.md) |  |
| `cadunico_por_bairro_ate_4_2026.csv` | sim | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.1886 (estrutura_eixos.md) |  |
| `cadunico_por_faixa_renda_2026.csv` | sim | Família e Cuidados › Famílias com crianças até 6 anos no Cadastro Único, por renda | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.1738 (estrutura_eixos.md) |  |
| `cadunico_por_idade_2026.csv` | sim | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) \| Famílias com crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.1773 (estrutura_eixos.md) |  |
| `cadunico_por_raca_cor_2026.csv` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por raça/cor | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.2018 (estrutura_eixos.md) |  |
| `cadunico_por_sexo_2026.csv` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por sexo | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.1987 (estrutura_eixos.md) |  |
| `cadunico_razao_populacao_0_a_5_2026.csv` | sim | Inclusão › Crianças de 0 a 5 anos no CadÚnico em relação à população do município | — | Cadastro Único (extração CTPE, jun/2026); população: estimativas Ripsa/Ministério da Saúde (2025) | ms_ripsa_populacao, mds_cadunico | `to_csv` l.1822 (estrutura_eixos.md) |  |
| `censo_0_a_4_anos_por_ano.csv` | sim | Prioridade › Crianças até 4 anos (número) \| Crianças até 4 anos (percentual) | — | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `to_csv` l.1601 (estrutura_eixos.md) |  |
| `censo_por_bairro.csv` | sim | Prioridade › Crianças até 4 anos (número) | — | Censo Demográfico 2022 (IBGE) | ipp_datario_censo | `to_csv` l.1415 (estrutura_eixos.md) |  |
| `censo_sidra_populacao_0_6_raca_2022.csv` | sim | Inclusão › Crianças até 6 anos, por raça/cor | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.1448 (estrutura_eixos.md) |  |
| `censo_sidra_populacao_0_6_sexo_2022.csv` | sim | Inclusão › Crianças até 6 anos, por sexo | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.1449 (estrutura_eixos.md) |  |
| `cobertura_vacinal_epi_comparativo_anos.csv` | sim | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos | — | Epi Rio | sms_rio_epi_vacinal | `to_csv` l.3513 (estrutura_eixos.md) |  |
| `cobertura_vacinal_epi_por_ano.csv` | sim | Família e Cuidados › Cobertura vacinal de rotina em crianças até 2 anos | — | Epi Rio | sms_rio_epi_vacinal | `to_csv` l.3484 (estrutura_eixos.md) |  |
| `frequencia_escolar_pnad_por_idade.csv` | sim | Família e Cuidados › Taxa bruta de frequência escolar da população até 6 anos | — | PNAD Contínua | ibge_pnadc | `to_csv` l.3627 (estrutura_eixos.md) |  |
| `matriculas_0_a_5_por_ano.csv` | sim | Família e Cuidados › Matrículas na educação básica de crianças de 0 a 5 anos \| Taxa bruta de atendimento escolar de 0 a 5 anos | — | Censo Escolar da Educação Básica (INEP), microdados; Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde | ms_ripsa_populacao, inep_censo_escolar | `to_csv` l.3671 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_0_a_6_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2635 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_28_a_364_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2733 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_7_a_27_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2684 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_grupo_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2580 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_raca_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por raça/cor | — | DataSUS (SIM) | sms_rio_sim | — | chamada comentada em analise.py (arquivo antigo) |
| `mortalidade_causas_evitaveis_subgrupo_0_a_6_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2636 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_28_a_364_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2734 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_7_a_27_dias_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2685 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2581 (estrutura_eixos.md) |  |
| `mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2787 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_cap_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.3019 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_cap_faixa_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.2909 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_grupo_cap_faixa_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2925 (estrutura_eixos.md) |  |
| `mortalidade_evitaveis_subgrupo_cap_2025.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.3026 (estrutura_eixos.md) |  |
| `mortalidade_infantil_pos_neonatal_total_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.3359 (estrutura_eixos.md) |  |
| `mortalidade_infantil_pos_neonatal_total_por_ano.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.3366 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_precoce_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.3223 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_precoce_por_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.3229 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_tardia_bairro_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.3277 (estrutura_eixos.md) |  |
| `mortalidade_neonatal_tardia_por_ano.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.3283 (estrutura_eixos.md) |  |
| `mortalidade_raca_bairro_ano.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2349 (estrutura_eixos.md) |  |
| `mortalidade_raca_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2367 (estrutura_eixos.md) |  |
| `nascidos_abaixo_peso_por_ano.csv` | sim | Alimentação › Baixo peso ao nascer (número) \| Baixo peso ao nascer (percentual) | — | DataSUS/Tabnet (`limpeza_tabnet_bairros`) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2253 (estrutura_eixos.md) |  |
| `nascidos_vivos_por_ano.csv` | sim | Prioridade › Nascidos vivos por bairro de residência da mãe (número) | — | DataSUS/Tabnet (nascidos vivos) | sms_rio_sinasc | `to_csv` l.2195 (estrutura_eixos.md) |  |
| `notif_autoprovocada_por_bairro_ano.csv` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3955 (estrutura_eixos.md) |  |
| `obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10) | — | DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis) | sms_rio_sim | `to_csv` l.2829 (estrutura_eixos.md) |  |
| `obitos_gravidez_bairro_ano.csv` | sim | Prioridade › Razão de mortalidade materna (durante a gravidez) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.3124 (estrutura_eixos.md) |  |
| `obitos_gravidez_por_ano.csv` | sim | Prioridade › Razão de mortalidade materna (durante a gravidez) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.3130 (estrutura_eixos.md) |  |
| `obitos_puerperio_bairro_ano.csv` | sim | Prioridade › Razão de mortalidade materna (durante puerpério) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.3167 (estrutura_eixos.md) |  |
| `obitos_puerperio_por_ano.csv` | sim | Prioridade › Razão de mortalidade materna (durante puerpério) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.3173 (estrutura_eixos.md) |  |
| `populacao_ripsa_0_a_6_por_ano.csv` | sim | Prioridade › Crianças até 6 anos (número) | — | Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025) | ms_ripsa_populacao | `to_csv` l.1659 (estrutura_eixos.md) |  |
| `sidra_frequencia_escola_0_5_raca_2022.csv` | sim | Inclusão › Crianças até 6 anos frequentando escola/creche, por raça/cor | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.3559 (estrutura_eixos.md) |  |
| `sidra_frequencia_escola_0_5_sexo_2022.csv` | sim | Inclusão › Crianças até 6 anos frequentando escola/creche, por sexo | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.3560 (estrutura_eixos.md) |  |
| `sidra_frequencia_escola_0_5_total_2022.csv` | sim | Família e Cuidados › Crianças até 6 anos frequentando escola/creche (geral) | — | Censo Demográfico 2022 (IBGE SIDRA, tabela 10057) | ibge_censo2022 | `to_csv` l.3593 (estrutura_eixos.md) |  |
| `sidra_taxa_frequencia_0_6_raca_2022.csv` | sim | Inclusão › Crianças até 6 anos frequentando escola/creche, por raça/cor | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.3561 (estrutura_eixos.md) |  |
| `sidra_taxa_frequencia_0_6_sexo_2022.csv` | sim | Inclusão › Crianças até 6 anos frequentando escola/creche, por sexo | — | Censo Demográfico 2022 (IBGE SIDRA) | ibge_censo2022 | `to_csv` l.3562 (estrutura_eixos.md) |  |
| `sisvan_desnutricao_por_ano.csv` | sim | Alimentação › Desnutrição SISVAN (número) \| Desnutrição SISVAN (percentual) | — | SISVAN | ms_sisvan | `to_csv` l.3437 (estrutura_eixos.md) |  |
| `sisvan_sobrepeso_por_ano.csv` | sim | Alimentação › Sobrepeso SISVAN (número) \| Sobrepeso SISVAN (percentual) | — | SISVAN | ms_sisvan | `to_csv` l.3453 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_criancas_0_a_4_2026.csv` | sim | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.1934 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_criancas_2026.csv` | sim | Família e Cuidados › Crianças até 6 anos no Cadastro Único (número) | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.1907 (estrutura_eixos.md) |  |
| `tabela_mapa_cadunico_recortes_bairro_2026.csv` | sim | Inclusão › Famílias no CadÚnico com crianças até 6 anos, por sexo \| Famílias no CadÚnico com crianças até 6 anos, por raça/cor \| Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar | — | Cadastro Único (extração CTPE) | mds_cadunico | `to_csv` l.2121 (estrutura_eixos.md) |  |
| `tabela_mapa_mortalidade_infantil_2025.csv` | sim | Prioridade › Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos) | — | DataSUS/Tabnet municipal | sms_rio_sim | `to_csv` l.3378 (estrutura_eixos.md) |  |
| `tabela_mapa_nascidos_baixo_peso_2025.csv` | não | — | DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro | — | sms_rio_sim, sms_rio_sinasc | `to_csv` l.2226 (vizinhança) |  |
| `tabela_mapa_nascidos_vivos_2025.csv` | sim | Prioridade › Nascidos vivos por bairro de residência da mãe (número) \| Nascidos vivos por bairro de residência da mãe (percentual) | — | DataSUS/Tabnet (nascidos vivos) | sms_rio_sinasc | `to_csv` l.2176 (estrutura_eixos.md) |  |
| `tabela_mapa_notif_autoprovocada_2026.csv` | sim | Proteção › Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3972 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_gravidez_2025.csv` | sim | Prioridade › Razão de mortalidade materna (durante a gravidez) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.3150 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_neonatal_precoce_2025.csv` | sim | Prioridade › Taxa de mortalidade neonatal precoce (0 a 6 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.3245 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_neonatal_tardia_2025.csv` | sim | Prioridade › Taxa de mortalidade neonatal tardia (7 a 27 dias) | — | DataSUS/Tabnet (SIM/SINASC) | sms_rio_sim, sms_rio_sinasc | `to_csv` l.3299 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_puerperio_2025.csv` | sim | Prioridade › Razão de mortalidade materna (durante puerpério) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.3192 (estrutura_eixos.md) |  |
| `tabela_mapa_obitos_raca_total_2025.csv` | sim | Prioridade › Mortalidade infantil por raça/cor (menores de 1 ano) | — | DataSUS/Tabnet (SIM) | sms_rio_sim | `to_csv` l.2409 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_mae_2025.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3881 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_outros_2021_2025.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3883 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_pai_2025.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3882 (estrutura_eixos.md) |  |
| `tabela_mapa_violencia_familiar_taxa_mae_2025.csv` | não | — | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | — | ipp_ips2024 | `to_csv` l.4056 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_outros_2021_2025.csv` | não | — | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | — | ipp_ips2024 | `to_csv` l.4056 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_pai_2025.csv` | não | — | Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades) | — | ipp_ips2024 | `to_csv` l.4056 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_mae_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.4082 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_outros_2021_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.4082 (vizinhança) |  |
| `tabela_mapa_violencia_familiar_taxa_ra_pai_2025.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos; população 0 a 4 anos: Censo Demográfico 2022 (IBGE/Data.Rio) | — | ipp_datario_censo, sms_rio_sinan | `to_csv` l.4082 (vizinhança) |  |
| `tabela_mapa_violencia_territorial_ra_2024.csv` | sim | Proteção › Violência territorial | — | Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa | ipp_ips2024 | `to_csv` l.3994 (estrutura_eixos.md) |  |
| `taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv` | sim | Prioridade › Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias) | — | DataSUS (SIM, classificação de evitabilidade) | sms_rio_sim | `to_csv` l.2830 (estrutura_eixos.md) |  |
| `violencia_familiar_outros_detalhe.csv` | sim | Proteção › Violência familiar — composição de "outros" vínculos | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3848 (estrutura_eixos.md) |  |
| `violencia_familiar_por_bairro.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3864 (estrutura_eixos.md) |  |
| `violencia_familiar_por_cap.csv` | sim | Proteção › Violência familiar — por CAP | — | Sinan NET/Tabnet (SMS-Rio); população 0 a 4 anos do Censo 2022 | ipp_datario_censo, sms_rio_sinan | `to_csv` l.3939 (estrutura_eixos.md) |  |
| `violencia_familiar_por_ra.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), notificações de residentes no município do Rio de Janeiro, 0 a 5 anos | — | sms_rio_sinan | `to_csv` l.3938 (vizinhança) |  |
| `violencia_familiar_por_vinculo_ano.csv` | sim | Proteção › Violência familiar (0 a 5 anos, por vínculo do provável autor) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3795 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_municipio_ano.csv` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | — | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, ms_ripsa_populacao, sms_rio_sinan | `to_csv` l.3829 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_por_bairro.csv` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | — | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, ms_ripsa_populacao, sms_rio_sinan | `to_csv` l.4037 (estrutura_eixos.md) |  |
| `violencia_familiar_taxa_top_bairros_2025.csv` | sim | Proteção › Taxa de notificações de violência (0 a 6 anos) | — | Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022 | ipp_datario_censo, ms_ripsa_populacao, sms_rio_sinan | `to_csv` l.4102 (estrutura_eixos.md) |  |
| `violencia_familiar_top_bairros_2025.csv` | sim | Proteção › Violência familiar — bairros com mais notificações (2025) | — | Sinan NET/Tabnet (SMS-Rio) | sms_rio_sinan | `to_csv` l.3915 (estrutura_eixos.md) |  |
| `violencia_territorial_por_ra_2024.csv` | não | — | Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos | — | sms_rio_sinan | `to_csv` l.3993 (vizinhança) |  |

## 3. Alertas

Apontados, não corrigidos — cada item pede uma decisão da equipe.

### Gráfico do notebook que regen_missing_pngs.py regrava com uma cópia própria, sem `fonte_dados` (13)

- visualizacoes/cadunico_criancas_por_faixa_renda.png
- visualizacoes/cadunico_criancas_por_idade.png
- visualizacoes/cadunico_familias_por_faixa_renda.png
- visualizacoes/cadunico_familias_por_idade.png
- visualizacoes/matriculas_0_a_5_por_ano.png
- visualizacoes/nascidos_abaixo_peso_percentual_por_ano.png
- visualizacoes/nascidos_vivos_por_ano.png
- visualizacoes/obitos_gravidez_por_ano.png
- visualizacoes/obitos_puerperio_por_ano.png
- visualizacoes/pnad_frequencia_escolar_por_idade.png
- visualizacoes/sisvan_desnutricao_percentual_por_ano.png
- visualizacoes/sisvan_obesidade_percentual_por_ano.png
- visualizacoes/sisvan_sobrepeso_percentual_por_ano.png

### Usado no relatório, mas só regen_missing_pngs.py o gera (não há chamada em analise.py) (2)

- visualizacoes/censo_0_a_4_serie_percentual_ano.png
- visualizacoes/censo_0_a_4_serie_total_ano.png

### Usado no relatório, mas a chamada que o gera está comentada em analise.py (arquivo antigo no disco) (10)

- mapas/mapa_obitos_gravidez_bairro_2025.png
- mapas/mapa_obitos_neonatal_tardia_bairro_2025.png
- mapas/mapa_obitos_pos_neonatal_bairro_2025.png
- mapas/mapa_obitos_puerperio_bairro_2025.png
- tabelas_finais/mortalidade_causas_evitaveis_raca_municipio_ano.csv
- visualizacoes/cobertura_vacinal_epi_ano.png
- visualizacoes/obitos_causas_evitaveis_raca_ano.png
- visualizacoes/obitos_causas_evitaveis_raca_sem_nao_informado_ano.png
- visualizacoes/percentual_mortalidade_causas_evitaveis_raca_ano.png
- visualizacoes/percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano.png

### Informativo: `fonte:` do .md e `fonte_dados` do analise.py citam conjuntos de bases diferentes (13)

- mapas/mapa_mortalidade_infantil_bairro_2025.png — .md: “DataSUS/Tabnet municipal”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- mapas/mapa_nascidos_vivos_bairro_2025.png — .md: “DataSUS/Tabnet (nascidos vivos)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
- mapas/mapa_obitos_raca_total_bairro_2025.png — .md: “DataSUS/Tabnet (SIM)”; analise.py: “DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro”
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

### Arquivo no disco que nenhuma subseção de estrutura_eixos.md usa (10)

- mapas/mapa_percentual_cadunico_0_a_4_sobre_censo_bairro_2026.png
- tabelas_finais/tabela_mapa_nascidos_baixo_peso_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_mae_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_outros_2021_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_pai_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_ra_mae_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_ra_outros_2021_2025.csv
- tabelas_finais/tabela_mapa_violencia_familiar_taxa_ra_pai_2025.csv
- tabelas_finais/violencia_familiar_por_ra.csv
- tabelas_finais/violencia_territorial_por_ra_2024.csv

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
