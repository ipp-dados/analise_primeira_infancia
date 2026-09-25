# Estrutura por Eixos da Política Municipal

> Este arquivo implementa `specs/2026-09-22_ajuste_eixos/specs.md` (Bloco 1 de
> `specs/2026-09-22_ajuste_eixos/plan.md`) — é a fonte única e editável à mão da
> organização de `relatorio/index.html`/PDF/DOCX por eixo de política
> municipal de primeira infância, em vez de por fonte de dado. Formato:
> `##` = eixo, `###` = subseção (um indicador do catálogo
> `dados_locais/painel_primeira_infancia_cesta_indicadores.xlsx`), lista
> `- chave: valor` = campos da subseção. Sem YAML/front matter, de propósito
> (edição manual sem quebrar o parser — ver `parse_estrutura_eixos()` em
> `.claude/skills/export_pdf_report/scripts/gera_estrutura_eixos.py`).
>
> **Convenção de chave repetida**: quando um indicador do catálogo tem mais
> de um corte real em `analise.py` (ex. causas evitáveis por grupo/subgrupo/
> CAP/faixa etária), a subseção lista várias linhas `- visualização: ...`/
> `- mapa: ...`/`- tabela: ...` em sequência — o parser as coleta numa lista,
> não sobrescreve.

## 🎯 Prioridade (sem secundário)

### Crianças até 4 anos (número)
- fonte: Censo Demográfico 2022 (IBGE)
- visualização: `censo_0_a_4_serie_total_ano.png`
- mapa: `mapa_censo_0_4_absoluto.png`
- tabela: `censo_0_a_4_anos_por_ano.csv`
- tabela: `censo_por_bairro.csv`

### Crianças até 4 anos (percentual)
- fonte: Censo Demográfico 2022 (IBGE)
- visualização: `censo_0_a_4_serie_percentual_ano.png`
- mapa: `mapa_censo_0_4_percentual.png`
- tabela: `censo_0_a_4_anos_por_ano.csv`

### Crianças até 6 anos (número)
- fonte: Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025)
- visualização: `populacao_ripsa_0_a_6_por_ano.png`
- visualização: `populacao_ripsa_0_a_6_percentual_por_ano.png`
- tabela: `populacao_ripsa_0_a_6_por_ano.csv`
- nota: série anual 2000-2025, nível município, idade simples 0 a 6 (a tabela traz também o total 0 a 5). Estimativa corrigida da subcontagem do Censo 2022: não se compara diretamente com os números do Censo. Ligado em `specs/2026-09-24_populacao-referencia` (A2/D2)

### Nascidos vivos por bairro de residência da mãe (número)
- fonte: DataSUS/Tabnet (nascidos vivos)
- visualização: `nascidos_vivos_por_ano.png`
- mapa: `mapa_nascidos_vivos_bairro_2025.png`
- tabela: `nascidos_vivos_por_ano.csv`
- tabela: `tabela_mapa_nascidos_vivos_2025.csv`

### Nascidos vivos por bairro de residência da mãe (percentual)
- fonte: DataSUS/Tabnet (nascidos vivos)
- mapa: `mapa_nascidos_vivos_bairro_2025.png`
- tabela: `tabela_mapa_nascidos_vivos_2025.csv`
- nota: mesma informação do mapa de contagem, dividida pelo total do município (coluna `percentual_do_municipio` da tabela; no HTML, no tooltip do mapa). O total inclui os nascidos sem bairro informado (6.336 de 65.507 em 2025), por isso os bairros somam ~90%. Sem mapa próprio (`specs/2026-09-24_populacao-referencia`, D1 revisada)

### Taxa de mortalidade neonatal precoce (0 a 6 dias)
- fonte: DataSUS/Tabnet (SIM/SINASC)
- visualização: `taxa_mortalidade_precoce_ano.png`
- mapa: `mapa_taxa_mortalidade_precoce_bairro_2025.png`
- tabela: `mortalidade_neonatal_precoce_por_ano.csv`
- tabela: `mortalidade_neonatal_precoce_bairro_ano.csv`
- tabela: `tabela_mapa_obitos_neonatal_precoce_2025.csv`

- nota: mapa_obitos_neonatal_precoce_bairro_2025.png fora do relatório (specs/exclusoes.md, E9, 2026-09-25): mapa de contagem ao lado do de taxa; no site vira alternância Taxa/Óbitos
### Taxa de mortalidade neonatal tardia (7 a 27 dias)
- fonte: DataSUS/Tabnet (SIM/SINASC)
- visualização: `taxa_obitos_tardios_ano.png`
- mapa: `mapa_taxa_obitos_tardios_bairro_2025.png`
- tabela: `mortalidade_neonatal_tardia_por_ano.csv`
- tabela: `mortalidade_neonatal_tardia_bairro_ano.csv`
- tabela: `tabela_mapa_obitos_neonatal_tardia_2025.csv`

- nota: `mapa_obitos_neonatal_tardia_bairro_2025.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
### Razão de mortalidade materna (durante a gravidez)
- fonte: DataSUS/Tabnet (SIM)
- visualização: `obitos_gravidez_por_ano.png`
- tabela: `obitos_gravidez_por_ano.csv`
- tabela: `obitos_gravidez_bairro_ano.csv`
- tabela: `tabela_mapa_obitos_gravidez_2025.csv`

- nota: `mapa_obitos_gravidez_bairro_2025.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
### Razão de mortalidade materna (durante puerpério)
- fonte: DataSUS/Tabnet (SIM)
- visualização: `obitos_puerperio_por_ano.png`
- tabela: `obitos_puerperio_por_ano.csv`
- tabela: `obitos_puerperio_bairro_ano.csv`
- tabela: `tabela_mapa_obitos_puerperio_2025.csv`

- nota: `mapa_obitos_puerperio_bairro_2025.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
### Mortalidade infantil por raça/cor (menores de 1 ano)
- fonte: DataSUS/Tabnet (SIM)
- visualização: `obitos_raca_ano.png`
- visualização: `percentual_mortalidade_raca_ano.png`
- mapa: `mapa_taxa_obitos_raca_total_bairro_2025.png`
- tabela: `mortalidade_raca_bairro_ano.csv`
- tabela: `mortalidade_raca_municipio_ano.csv`
- tabela: `tabela_mapa_obitos_raca_total_2025.csv`

- nota: mapa_obitos_raca_total_bairro_2025.png fora do relatório (specs/exclusoes.md, E9, 2026-09-25): mapa de contagem ao lado do de taxa; no site vira alternância Taxa/Óbitos
### Mortalidade infantil por causas evitáveis (0 a 6, 7 a 27, 28 a 364 dias)
- fonte: DataSUS (SIM, classificação de evitabilidade)
- visualização: `obitos_evitaveis_total_cap_ano.png`
- visualização: `obitos_evitaveis_cap_menores_1_ano_ano.png`
- visualização: `obitos_evitaveis_cap_1_a_4_anos_ano.png`
- visualização: `obitos_evitaveis_cap_menores_5_anos_ano.png`
- visualização: `percentual_evitaveis_cap_menores_1_ano_ano.png`
- visualização: `percentual_evitaveis_cap_1_a_4_anos_ano.png`
- visualização: `percentual_evitaveis_cap_menores_5_anos_ano.png`
- visualização: `taxa_mortalidade_evitaveis_menores_5_ano.png`
- mapa: `mapa_obitos_evitaveis_menores_1_ano_cap_2025.png`
- mapa: `mapa_obitos_evitaveis_1_a_4_anos_cap_2025.png`
- mapa: `mapa_obitos_evitaveis_menores_5_anos_cap_2025.png`
- mapa: `mapa_percentual_evitaveis_menores_1_ano_cap_2025.png`
- mapa: `mapa_percentual_evitaveis_1_a_4_anos_cap_2025.png`
- mapa: `mapa_percentual_evitaveis_menores_5_anos_cap_2025.png`
- tabela: `mortalidade_evitaveis_cap_faixa_ano.csv`
- tabela: `mortalidade_evitaveis_cap_2025.csv`
- tabela: `taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv`

### Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos)
- fonte: DataSUS/Tabnet municipal
- visualização: `taxa_mortalidade_infantil_ano.png`
- visualização: `taxa_mortalidade_pos_neonatal_ano.png`
- mapa: `mapa_taxa_mortalidade_infantil_bairro_2025.png`
- mapa: `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png`
- tabela: `mortalidade_infantil_pos_neonatal_total_por_ano.csv`
- tabela: `mortalidade_infantil_pos_neonatal_total_bairro_ano.csv`
- tabela: `tabela_mapa_mortalidade_infantil_2025.csv`

- nota: `mapa_obitos_pos_neonatal_bairro_2025.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
- nota: mapa_mortalidade_infantil_bairro_2025.png fora do relatório (specs/exclusoes.md, E9, 2026-09-25): mapa de contagem ao lado do de taxa; no site vira alternância Taxa/Óbitos
### Mortalidade infantil por causas evitáveis, por tipo de causa (grupo/subgrupo CID-10)
- fonte: DataSUS (SIM, grupo/subgrupo CID-10 de causas evitáveis)
- visualização: `obitos_causas_evitaveis_grupo_ano.png`
- visualização: `obitos_causas_evitaveis_subgrupo_ano.png`
- visualização: `obitos_causas_evitaveis_grupo_0_a_6_dias_ano.png`
- visualização: `obitos_causas_evitaveis_subgrupo_0_a_6_dias_ano.png`
- visualização: `obitos_causas_evitaveis_grupo_7_a_27_dias_ano.png`
- visualização: `obitos_causas_evitaveis_subgrupo_7_a_27_dias_ano.png`
- visualização: `obitos_causas_evitaveis_grupo_28_a_364_dias_ano.png`
- visualização: `obitos_causas_evitaveis_subgrupo_28_a_364_dias_ano.png`
- visualização: `obitos_causas_evitaveis_subgrupo_faixa_2025.png`
- visualização: `obitos_evitaveis_menores_1_ano_subgrupo_ano.png`
- visualização: `obitos_evitaveis_1_a_4_anos_subgrupo_ano.png`
- visualização: `obitos_evitaveis_menores_5_subgrupo_ano.png`
- tabela: `mortalidade_causas_evitaveis_grupo_ano.csv`
- tabela: `mortalidade_causas_evitaveis_subgrupo_ano.csv`
- tabela: `mortalidade_causas_evitaveis_grupo_0_a_6_dias_ano.csv`
- tabela: `mortalidade_causas_evitaveis_subgrupo_0_a_6_dias_ano.csv`
- tabela: `mortalidade_causas_evitaveis_grupo_7_a_27_dias_ano.csv`
- tabela: `mortalidade_causas_evitaveis_subgrupo_7_a_27_dias_ano.csv`
- tabela: `mortalidade_causas_evitaveis_grupo_28_a_364_dias_ano.csv`
- tabela: `mortalidade_causas_evitaveis_subgrupo_28_a_364_dias_ano.csv`
- tabela: `mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv`
- tabela: `obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv`
- tabela: `mortalidade_evitaveis_grupo_cap_faixa_ano.csv`
- tabela: `mortalidade_evitaveis_subgrupo_cap_2025.csv`

### Mortalidade infantil por causas evitáveis, por raça/cor
- fonte: DataSUS (SIM)
- status: pendente
- nota: os 4 gráficos (`obitos_causas_evitaveis_raca_ano`, `…_sem_nao_informado_ano`, `percentual_mortalidade_causas_evitaveis_raca_ano`, `…_sem_nao_informado_ano`) e a tabela `mortalidade_causas_evitaveis_raca_municipio_ano.csv` foram removidos do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): as chamadas que os geravam estão comentadas em analise.py, então os arquivos no disco são antigos. Ver também a nota de analise.py: o cruzamento por raça/cor desse arquivo não é filtrado só para causas evitáveis

### Mortalidade infantil por causas evitáveis, por sexo
- fonte: DataSUS (SIM)
- status: pendente
- nota: recorte por sexo ainda não extraído do SIM (antes o item sumia do relatório em silêncio, sem arquivo e sem status)

## 🤝 Inclusão

### Crianças até 6 anos, por sexo
- fonte: Censo Demográfico 2022 (IBGE SIDRA)
- visualização: `censo_sidra_populacao_0_6_sexo_2022.png`
- tabela: `censo_sidra_populacao_0_6_sexo_2022.csv`

### Crianças até 6 anos, por raça/cor
- fonte: Censo Demográfico 2022 (IBGE SIDRA)
- visualização: `censo_sidra_populacao_0_6_raca_2022.png`
- tabela: `censo_sidra_populacao_0_6_raca_2022.csv`

### Crianças até 6 anos frequentando escola/creche, por raça/cor
- fonte: Censo Demográfico 2022 (IBGE SIDRA)
- visualização: `sidra_taxa_frequencia_0_6_raca_2022.png`
- tabela: `sidra_taxa_frequencia_0_6_raca_2022.csv`
- nota: faixa real: frequência de 0 a 5 anos (tabela 10057) e taxa de frequência de 0 a 6 anos (tabela 10056)

- nota: sidra_frequencia_escola_0_5_raca_2022.png, sidra_frequencia_escola_0_5_raca_2022.csv fora do relatório (specs/exclusoes.md, E8, 2026-09-25): número absoluto; fica a taxa por idade
### Crianças até 6 anos frequentando escola/creche, por sexo
- fonte: Censo Demográfico 2022 (IBGE SIDRA)
- visualização: `sidra_taxa_frequencia_0_6_sexo_2022.png`
- tabela: `sidra_taxa_frequencia_0_6_sexo_2022.csv`
- nota: faixa real: frequência de 0 a 5 anos (tabela 10057) e taxa de frequência de 0 a 6 anos (tabela 10056)

- nota: sidra_frequencia_escola_0_5_sexo_2022.png, sidra_frequencia_escola_0_5_sexo_2022.csv fora do relatório (specs/exclusoes.md, E8, 2026-09-25): número absoluto; fica a taxa por idade
### Crianças de 0 a 5 anos no CadÚnico em relação à população do município
- fonte: Cadastro Único (extração CTPE, jun/2026); população: estimativas Ripsa/Ministério da Saúde (2025)
- tabela: `cadunico_razao_populacao_0_a_5_2026.csv`
- nota: razão municipal (194.138 ÷ 393.073 ≈ 49,4% na partição 2026-06-12). Cadastro de 2026 sobre estimativa de 2025; não é a cobertura exata do cadastro. Item novo da rodada `populacao-referencia` (A4), fora do catálogo original

### Famílias no CadÚnico com crianças até 6 anos, por sexo
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_criancas_por_sexo.png`
- visualização: `cadunico_familias_por_sexo_criancas.png`
- tabela: `cadunico_por_sexo_2026.csv`
- tabela: `tabela_mapa_cadunico_recortes_bairro_2026.csv`
- nota: sexo da criança; famílias pela composição de sexo das crianças (só meninas / só meninos / ambos); 0 a 5 anos completos; bairros com menos de 20 famílias suprimidos

### Famílias no CadÚnico com crianças até 6 anos, por raça/cor
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_criancas_por_raca_cor.png`
- visualização: `cadunico_familias_por_raca_cor.png`
- mapa: `mapa_percentual_cadunico_criancas_negras_bairro_2026.png`
- tabela: `cadunico_por_raca_cor_2026.csv`
- tabela: `tabela_mapa_cadunico_recortes_bairro_2026.csv`
- nota: raça/cor da criança; famílias com ao menos uma criança da categoria (não somam); por bairro só o % de crianças negras (privacidade); 0 a 5 anos completos

### Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_familias_por_arranjo.png`
- visualização: `cadunico_familias_arranjo_renda.png`
- mapa: `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png`
- tabela: `cadunico_familias_por_arranjo_2026.csv`
- tabela: `cadunico_familias_arranjo_renda_2026.csv`
- tabela: `tabela_mapa_cadunico_recortes_bairro_2026.csv`
- nota: arranjo aproximado pela composição do cadastro (adultos de 18+ por sexo), não é o conceito de monoparental do MDS; renda per capita; 0 a 5 anos completos

### Crianças no CadÚnico com alguma deficiência
- fonte: Cadastro Único
- status: pendente
- nota: baixar dados — Léo

### Famílias no CadÚnico com criança com deficiência
- fonte: Cadastro Único
- status: pendente
- nota: baixar dados — Léo

### Crianças no CadÚnico por tipo de deficiência
- fonte: Cadastro Único
- status: pendente
- nota: baixar dados — Léo

## 👨‍👩‍👧 Família e Cuidados

### Crianças até 6 anos no Cadastro Único (número)
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_criancas_por_idade.png`
- mapa: `mapa_cadunico_criancas_bairro_2026.png`
- mapa: `mapa_cadunico_criancas_0_a_4_bairro_2026.png`
- tabela: `cadunico_por_idade_2026.csv`
- tabela: `cadunico_por_bairro_2026.csv`
- tabela: `cadunico_por_bairro_ate_4_2026.csv`
- tabela: `tabela_mapa_cadunico_criancas_2026.csv`
- tabela: `tabela_mapa_cadunico_criancas_0_a_4_2026.csv`
- nota: faixa real 0 a 5 anos completos (grupo "0-6" do CTPE); os arquivos `_0_a_4`/`ate_4` são o recorte de 0 a 4 anos

### Famílias com crianças até 6 anos no Cadastro Único (número)
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_familias_por_idade.png`
- tabela: `cadunico_por_idade_2026.csv`
- tabela: `cadunico_por_bairro_2026.csv`
- nota: faixa real 0 a 5 anos completos (grupo "0-6" do CTPE)

### Famílias com crianças até 6 anos no Cadastro Único, por renda
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_familias_por_faixa_renda.png`
- visualização: `cadunico_criancas_por_faixa_renda.png`
- tabela: `cadunico_por_faixa_renda_2026.csv`

### Taxa bruta de frequência escolar da população até 6 anos
- fonte: PNAD Contínua
- visualização: `pnad_frequencia_escolar_por_idade.png`
- tabela: `frequencia_escolar_pnad_por_idade.csv`

### Cobertura vacinal de rotina em crianças até 2 anos
- fonte: Epi Rio
- tabela: `cobertura_vacinal_epi_por_ano.csv`

- nota: `cobertura_vacinal_epi_ano.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
- nota: cobertura_vacinal_epi_comparativo_anos.png, cobertura_vacinal_epi_comparativo_anos.csv fora do relatório (specs/exclusoes.md, E7, 2026-09-25): repete 4 anos da série anual
### Crianças até 6 anos frequentando escola/creche (geral)
- fonte: Censo Demográfico 2022 (IBGE SIDRA, tabela 10057)
- visualização: `sidra_frequencia_escola_0_5_total_2022.png`
- tabela: `sidra_frequencia_escola_0_5_total_2022.csv`
- nota: faixa real 0 a 5 anos (a tabela 10057 vai só até 5 anos); total de todas as raças e sexos, por idade (`specs/2026-09-24_populacao-referencia`, D3)

### Matrículas na educação básica de crianças de 0 a 5 anos
- fonte: Censo Escolar da Educação Básica (INEP), microdados
- visualização: `matriculas_0_a_5_por_ano.png`
- visualização: `matriculas_0_a_5_creche_pre_por_ano.png`
- visualização: `matriculas_0_a_5_rede_por_ano.png`
- tabela: `matriculas_0_a_5_por_ano.csv`
- nota: 0 a 5 anos (`QT_MAT_BAS_0_3` + `QT_MAT_BAS_4_5`), idade na data de referência do Censo Escolar (última quarta-feira de maio); os dados abertos não separam 6 anos de 7-10. Série 2007-2025 refeita dos microdados (a série antiga, "até 6 anos", não batia com a fonte). Catálogo: "crianças até 6 anos" (`specs/2026-09-24_populacao-referencia/matriculas`)

### Taxa bruta de atendimento escolar de 0 a 5 anos
- fonte: Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde
- visualização: `taxa_atendimento_0_a_5_por_ano.png`
- tabela: `matriculas_0_a_5_por_ano.csv`
- nota: matrículas ÷ população residente da mesma faixa (0-3, 4-5, 0-5), 2007-2025; taxa bruta (inclui não residentes matriculados no Rio). Linhas de referência do PNE (50% creche, 100% pré-escola). Item novo da rodada `matriculas-censo-escolar`, fora do catálogo original (o mais próximo, "taxa bruta de frequência escolar", é da PNAD e continua acima)

## 🛡️ Proteção

### Violência territorial
- fonte: Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa
- mapa: `mapa_violencia_territorial_homicidios_ra_2024.png`
- mapa: `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png`
- mapa: `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png`
- tabela: `tabela_mapa_violencia_territorial_ra_2024.csv`
- nota: dado GERAL da população (todas as idades) — não é específico de crianças (0 a 6 anos) nem de jovens; só 2024 e sem série temporal (apenas mapas, sem barras nem tabela por RA); nível Região Administrativa; RA XXI Paquetá sem dado no IPS. Substitui a fonte "ISP" do catálogo

### Violência familiar (0 a 5 anos, por vínculo do provável autor)
- fonte: Sinan NET/Tabnet (SMS-Rio)
- visualização: `violencia_familiar_serie_vinculos.png`
- mapa: `mapa_violencia_familiar_mae_bairro_2025.png`
- mapa: `mapa_violencia_familiar_pai_bairro_2025.png`
- mapa: `mapa_violencia_familiar_outros_bairro_2021_2025.png`
- tabela: `violencia_familiar_por_vinculo_ano.csv`
- tabela: `violencia_familiar_por_bairro.csv`
- tabela: `tabela_mapa_violencia_familiar_mae_2025.csv`
- tabela: `tabela_mapa_violencia_familiar_pai_2025.csv`
- tabela: `tabela_mapa_violencia_familiar_outros_2021_2025.csv`
- nota: faixa 0 a 5 anos agregada (recorte menor de 1 ano x 1 a 5 anos pendente). Vínculos não são excludentes e não existe "total": nunca somar mãe + pai. Possível quebra de série em 2017 (hipótese: mudança de ficha/notificação, a confirmar com a fonte). 2026 é ano parcial e fica fora da série. Contagem absoluta não é risco

### Violência familiar — composição de "outros" vínculos
- fonte: Sinan NET/Tabnet (SMS-Rio)
- visualização: `violencia_familiar_outros_serie.png`
- tabela: `violencia_familiar_outros_detalhe.csv`
- nota: "outros" = padrasto + irmão(ã) + cônjuge + ex-cônjuge + filho(a); pode contar uma mesma notificação mais de uma vez

### Violência familiar — bairros com mais notificações (2025)
- fonte: Sinan NET/Tabnet (SMS-Rio)
- visualização: `violencia_familiar_top_bairros_2025.png`
- tabela: `violencia_familiar_top_bairros_2025.csv`
- nota: contagem absoluta, ordenada pelo vínculo mãe; bairros populosos lideram

### Violência familiar — por CAP
- fonte: Sinan NET/Tabnet (SMS-Rio); população 0 a 4 anos do Censo 2022
- tabela: `violencia_familiar_por_cap.csv`
- nota: casos somados por CAP e taxa por 1.000 recalculada depois de somar casos e população (nunca média de taxas)

### Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos)
- fonte: Sinan NET/Tabnet (SMS-Rio)
- visualização: `notif_autoprovocada_antes_2026_vs_2026.png`
- mapa: `mapa_notif_autoprovocada_bairro_2026.png`
- tabela: `notif_autoprovocada_por_bairro_ano.csv`
- tabela: `tabela_mapa_notif_autoprovocada_2026.csv`
- nota: parcial — só lesão autoprovocada (a violência interpessoal total e o recorte menor de 1 ano x 1 a 5 anos estão pendentes). 40 casos em 2018-2026, 33 deles em 2026 (ano parcial, usado como referência desta série); o salto pode refletir mudança de registro administrativo (hipótese, a confirmar com a fonte)

### Taxa de notificações de violência (0 a 6 anos)
- fonte: Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; bairro/RA/CAP: população 0 a 4 anos do Censo Demográfico 2022
- visualização: `violencia_familiar_taxa_municipio_ano.png`
- visualização: `violencia_familiar_taxa_top_bairros_2025.png`
- mapa: `mapa_violencia_familiar_mae_taxa_ra_2025.png`
- mapa: `mapa_violencia_familiar_pai_taxa_ra_2025.png`
- mapa: `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png`
- tabela: `violencia_familiar_taxa_municipio_ano.csv`
- tabela: `violencia_familiar_taxa_por_bairro.csv`
- tabela: `violencia_familiar_taxa_top_bairros_2025.csv`
- nota: município (2011-2025): numerador e denominador com 0 a 5 anos e o mesmo ano (Ripsa), sem ressalva de faixa (`specs/2026-09-24_populacao-referencia`, A3). Bairro/RA/CAP: ressalva de denominador — numerador com 0 a 5 anos (Sinan) e denominador com 0 a 4 anos (Censo 2022), o que superestima a taxa em ~20% de forma uniforme; o Censo 2022 é fixo (subconta crianças pequenas e é de outro ano), então as taxas por território comparam territórios entre si, não com a do município; "outros" usa o acumulado 2021-2025. Bairros com menos de 100 crianças têm taxa instável: escala de cor limitada ao percentil 95

- nota: mapa_violencia_familiar_mae_taxa_bairro_2025.png, mapa_violencia_familiar_pai_taxa_bairro_2025.png, mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png fora do relatório (specs/exclusoes.md, E6, 2026-09-25): taxa por bairro instável (bairros com poucas crianças); fica a taxa por RA
### Crianças que sofrem violência, por tipificação (sexo e idade)
- fonte: Tabnet municipal
- status: pendente
- nota: dado ainda não extraído do Tabnet

## 🍽️ Alimentação

### Baixo peso ao nascer (número)
- fonte: DataSUS/Tabnet (`limpeza_tabnet_bairros`)
- mapa: `mapa_nascidos_baixo_peso_bairro_2025.png`
- tabela: `nascidos_abaixo_peso_por_ano.csv`

### Baixo peso ao nascer (percentual)
- fonte: DataSUS/Tabnet (`limpeza_tabnet_bairros`)
- visualização: `nascidos_abaixo_peso_percentual_por_ano.png`
- mapa: `mapa_percentual_baixo_peso_bairro_2025.png`
- tabela: `nascidos_abaixo_peso_por_ano.csv`

### Desnutrição SISVAN (número)
- fonte: SISVAN
- nota: faixa real 0 a 5 anos (fase da vida "Criança (de 0 a 5 anos)" do SISVAN)
- tabela: `sisvan_desnutricao_por_ano.csv`

### Desnutrição SISVAN (percentual)
- fonte: SISVAN
- nota: faixa real 0 a 5 anos (fase da vida "Criança (de 0 a 5 anos)" do SISVAN)
- visualização: `sisvan_desnutricao_percentual_por_ano.png`
- tabela: `sisvan_desnutricao_por_ano.csv`

### Sobrepeso SISVAN (número)
- fonte: SISVAN
- nota: faixa real 0 a 5 anos (fase da vida "Criança (de 0 a 5 anos)" do SISVAN)
- tabela: `sisvan_sobrepeso_por_ano.csv`

### Sobrepeso SISVAN (percentual)
- fonte: SISVAN
- nota: faixa real 0 a 5 anos (fase da vida "Criança (de 0 a 5 anos)" do SISVAN)
- visualização: `sisvan_sobrepeso_percentual_por_ano.png`
- visualização: `sisvan_obesidade_percentual_por_ano.png`
- tabela: `sisvan_sobrepeso_por_ano.csv`

## 🏠 Moradia

### Crianças no CadÚnico em domicílios com inadequação habitacional
- fonte: Cadastro Único
- status: pendente
- nota: Posterior

### Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (acima de 3 por dormitório)
- fonte: Cadastro Único
- status: pendente
- nota: Posterior

### Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais)
- fonte: (não informada no catálogo)
- status: pendente
- nota: Posterior (apenas cad)
