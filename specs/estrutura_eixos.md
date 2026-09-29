# Estrutura por Eixos da Política Municipal

> Este arquivo implementa `specs/2026-09-22_ajuste_eixos/specs.md` (Bloco 1 de
> `specs/2026-09-22_ajuste_eixos/plan.md`) — é a fonte única e editável à mão da
> organização de `relatorio/index.html`/PDF/DOCX por eixo de política
> municipal de primeira infância, em vez de por fonte de dado. Formato:
> `##` = eixo, `###` = subseção (um indicador do catálogo
> `dados_locais/painel_primeira_infancia_cesta_indicadores.xlsx`), lista
> `- chave: valor` = campos da subseção. Sem YAML/front matter, de propósito
> (edição manual sem quebrar o parser — ver `parse_estrutura_eixos()` em
> `relatorio/curadoria/gera_estrutura_eixos.py`).
>
> **Convenção de chave repetida**: quando um indicador do catálogo tem mais
> de um corte real em `analise.py` (ex. causas evitáveis por grupo/subgrupo/
> CAP/faixa etária), a subseção lista várias linhas `- visualização: ...`/
> `- mapa: ...`/`- tabela: ...` em sequência — o parser as coleta numa lista,
> não sobrescreve.
>
> **Nova estrutura (`specs/2026-09-28_nova_estrutura`, 2026-09-28)**, a partir da planilha da equipe
> `specs/2026-09-28_nova_estrutura/Estrutura relatório e site - eixos atualizados e dados.csv`:
> - o primeiro `##`, **Introdução**, NÃO é um eixo: é o panorama da primeira infância carioca (população e
>   nascimentos), mostrado na aba *Visão geral* do site e no capítulo *Introdução* do PDF. Os geradores o
>   reconhecem por `chave_eixo(...) == "introducao"` e não o contam como eixo (sem "Eixo N de M", sem achados
>   nem síntese);
> - eixo novo **Direito ao Brincar** (7 eixos no total);
> - campo novo `- eixo transversal: <eixo>` (coluna "Eixo Transversal" da planilha): só registrado aqui, sem
>   efeito no site/PDF/DOCX nesta rodada (decisão do usuário, 2026-09-28).
>
> **Campos novos (`specs/2026-09-29_alinhamento_pdf_site`, 2026-09-29):**
> - `- motivo: <texto>` — **obrigatório em todo item `status: pendente`**: frase pública e formal que o site e o PDF
>   mostram depois da frase fixa do quadro de pendente (`TEXTO_PENDENTE`). Os builds param se faltar. As `- nota:`
>   continuam internas e nunca são publicadas;
> - `- tabela_no_texto: `<arquivo>.csv`` — a tabela (também listada em `- tabela:`) sai no corpo da seção do PDF,
>   com o texto curado da mesma chave, e não no apêndice. Usado quando o site mostra a tabela dentro do cartão.

## 🧭 Introdução

### Crianças até 4 anos (número)
- fonte: Censo Demográfico 2022 (IBGE)
- visualização: `censo_0_a_4_serie_total_ano.png`
- mapa: `mapa_censo_0_4_absoluto.png`
- tabela: `censo_0_a_4_anos_por_ano.csv`
- tabela: `censo_por_bairro.csv`
- nota: movido de Prioridade para a Introdução (specs/2026-09-28_nova_estrutura)

### Crianças até 4 anos (percentual)
- fonte: Censo Demográfico 2022 (IBGE)
- visualização: `censo_0_a_4_serie_percentual_ano.png`
- mapa: `mapa_censo_0_4_percentual.png`
- tabela: `censo_0_a_4_anos_por_ano.csv`
- nota: movido de Prioridade para a Introdução (specs/2026-09-28_nova_estrutura)

### Crianças até 72 meses (número)
- nota: nome no catálogo da equipe: "Crianças até 6 anos (número)"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025)
- visualização: `populacao_ripsa_0_a_6_por_ano.png`
- visualização: `populacao_ripsa_0_a_6_percentual_por_ano.png`
- tabela: `populacao_ripsa_0_a_6_por_ano.csv`
- nota: série anual 2000-2025, nível município, idade simples 0 a 5 (faixa padrão do projeto desde 2026-09-29, specs/2026-09-29_pendencias D9; antes 0 a 6). Estimativa corrigida da subcontagem do Censo 2022: não se compara diretamente com os números do Censo. Ligado em `specs/2026-09-24_populacao-referencia` (A2/D2)
- nota: movido de Prioridade para a Introdução (specs/2026-09-28_nova_estrutura)

### Crianças até 72 meses, por sexo
- nota: nome no catálogo da equipe: "Crianças até 6 anos, por sexo"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Censo Demográfico 2022 (IBGE SIDRA)
- eixo transversal: Proteção
- visualização: `censo_sidra_populacao_0_6_sexo_2022.png`
- tabela: `censo_sidra_populacao_0_6_sexo_2022.csv`
- nota: faixa real 0 a 5 anos (specs/2026-09-29_pendencias D9; a tabela 9606 traz também os 6 anos, fora); a linha de total é de 0 a 5 anos
- nota: movido de Inclusão para a Introdução (specs/2026-09-28_nova_estrutura)

### Crianças até 72 meses, por raça/cor
- nota: nome no catálogo da equipe: "Crianças até 6 anos, por raça/cor"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Censo Demográfico 2022 (IBGE SIDRA)
- eixo transversal: Proteção
- visualização: `censo_sidra_populacao_0_6_raca_2022.png`
- tabela: `censo_sidra_populacao_0_6_raca_2022.csv`
- nota: faixa real 0 a 5 anos (specs/2026-09-29_pendencias D9; a tabela 9606 traz também os 6 anos, fora); a linha de total é de 0 a 5 anos
- nota: movido de Inclusão para a Introdução (specs/2026-09-28_nova_estrutura)

### Nascidos vivos por bairro de residência da mãe (número)
- fonte: DataSUS/Tabnet (nascidos vivos)
- visualização: `nascidos_vivos_por_ano.png`
- mapa: `mapa_nascidos_vivos_bairro_2025.png`
- tabela: `nascidos_vivos_por_ano.csv`
- tabela: `tabela_mapa_nascidos_vivos_2025.csv`
- nota: movido de Prioridade para a Introdução (specs/2026-09-28_nova_estrutura). No site, a série sai do cartão "Nascidos vivos e mortalidade infantil por raça/cor" e o mapa sai do cartão "... por bairro"; os dois cartões de mortalidade ficam só com mortalidade

### Nascidos vivos por bairro de residência da mãe (percentual)
- fonte: DataSUS/Tabnet (nascidos vivos)
- mapa: `mapa_nascidos_vivos_bairro_2025.png`
- tabela: `tabela_mapa_nascidos_vivos_2025.csv`
- nota: mesma informação do mapa de contagem, dividida pelo total do município (coluna `percentual_do_municipio` da tabela; no HTML, no tooltip do mapa). O total inclui os nascidos sem bairro informado (6.336 de 65.507 em 2025), por isso os bairros somam ~90%. Sem mapa próprio (`specs/2026-09-24_populacao-referencia`, D1 revisada)
- nota: movido de Prioridade para a Introdução (specs/2026-09-28_nova_estrutura); a planilha da equipe marca "?" na visualização -- continua sem mapa próprio (D1 revisada)

## 🎯 Prioridade (sem secundário)

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
### Taxa de mortalidade na primeira infância (menores de 1, 1-4, 0-5 anos)
- fonte: DataSUS/Tabnet municipal
- visualização: `taxa_mortalidade_infantil_ano.png`
- visualização: `taxa_mortalidade_pos_neonatal_ano.png`
- mapa: `mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png`
- tabela: `mortalidade_infantil_pos_neonatal_total_por_ano.csv`
- tabela: `mortalidade_infantil_pos_neonatal_total_bairro_ano.csv`
- tabela: `tabela_mapa_mortalidade_infantil_2025.csv`
- nota: posto logo depois das taxas neonatais, na ordem do site (specs/2026-09-29_alinhamento_pdf_site D1); a planilha da equipe de 2026-09-28 o punha no bloco de causas evitáveis

- nota: `mapa_obitos_pos_neonatal_bairro_2025.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
- nota: `mapa_taxa_mortalidade_infantil_bairro_2025.png` fora do relatório (specs/exclusoes.md, E13, 2026-09-29): idêntico ao mapa `mapa_taxa_obitos_raca_total_bairro_2025.png` do item "Mortalidade infantil por raça/cor", que fica
- nota: mapa_mortalidade_infantil_bairro_2025.png fora do relatório (specs/exclusoes.md, E9, 2026-09-25): mapa de contagem ao lado do de taxa; no site vira alternância Taxa/Óbitos
- nota: a planilha da equipe (2026-09-28) aponta este indicador para o cartão "Óbitos por causas evitáveis"; ficam as taxas de menores de 1 ano acima e a taxa de evitáveis de menores de 5 anos (`taxa_mortalidade_evitaveis_menores_5_ano`) no item anterior. A taxa de 1 a 4 anos (todas as causas) ainda não existe (specs/2026-09-28_nova_estrutura §4, S3)
### Óbitos maternos durante a gravidez
- nota: título ajustado em 2026-09-25 (revisão de unidades, specs/2026-09-25_website_graficos): o catálogo pede a razão de mortalidade materna (por 100 mil nascidos vivos), mas o dado publicado é a contagem de óbitos
- fonte: DataSUS/Tabnet (SIM)
- visualização: `obitos_gravidez_por_ano.png`
- tabela: `obitos_gravidez_por_ano.csv`
- tabela: `obitos_gravidez_bairro_ano.csv`
- tabela: `tabela_mapa_obitos_gravidez_2025.csv`

- nota: `mapa_obitos_gravidez_bairro_2025.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
### Óbitos maternos durante o puerpério
- nota: título ajustado em 2026-09-25 (idem): contagem de óbitos, não razão
- fonte: DataSUS/Tabnet (SIM)
- visualização: `obitos_puerperio_por_ano.png`
- tabela: `obitos_puerperio_por_ano.csv`
- tabela: `obitos_puerperio_bairro_ano.csv`
- tabela: `tabela_mapa_obitos_puerperio_2025.csv`

- nota: `mapa_obitos_puerperio_bairro_2025.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
### Mortalidade infantil por raça/cor (menores de 1 ano)
- fonte: DataSUS/Tabnet (SIM)
- eixo transversal: Proteção
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
- nota: as 4 figuras "menores de 5 anos" (série e percentual por CAP, mapas de óbitos e de percentual de 2025) ganham a nota "agrega os recortes de menores de 1 ano e de 1 a 4 anos" na legenda (observação da curadoria, specs/2026-09-28_nova_estrutura §6)

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

### Mortalidade infantil por causas evitáveis, por sexo
- fonte: DataSUS (SIM)
- status: pendente
- motivo: O recorte por sexo ainda não foi extraído do Sistema de Informações sobre Mortalidade (SIM).
- nota: recorte por sexo ainda não extraído do SIM (antes o item sumia do relatório em silêncio, sem arquivo e sem status)

### Crianças de 0 a 5 anos no CadÚnico em relação à população do município
- fonte: Cadastro Único (extração CTPE, jun/2026); população: estimativas Ripsa/Ministério da Saúde (2025)
- tabela: `cadunico_razao_populacao_0_a_5_2026.csv`
- nota: razão municipal (194.138 ÷ 393.073 ≈ 49,4% na partição 2026-06-12). Cadastro de 2026 sobre estimativa de 2025; não é a cobertura exata do cadastro. Item novo da rodada `populacao-referencia` (A4), fora do catálogo original
- nota: movido de Inclusão para Prioridade (specs/2026-09-28_nova_estrutura)
- tabela_no_texto: `cadunico_razao_populacao_0_a_5_2026.csv`

### Crianças até 72 meses no Cadastro Único (número)
- nota: nome no catálogo da equipe: "Crianças até 6 anos no Cadastro Único (número)"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
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
- nota: movido de Família e Cuidados para Prioridade (specs/2026-09-28_nova_estrutura); posto logo depois da razão CadÚnico/população, antes dos recortes de famílias (sugestão S2 da rodada: a contagem-base vem antes dos cortes)

### Famílias com crianças até 72 meses no Cadastro Único (número)
- nota: nome no catálogo da equipe: "Famílias com crianças até 6 anos no Cadastro Único (número)"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_familias_por_idade.png`
- tabela: `cadunico_por_idade_2026.csv`
- tabela: `cadunico_por_bairro_2026.csv`
- nota: faixa real 0 a 5 anos completos (grupo "0-6" do CTPE)
- nota: movido de Família e Cuidados para Prioridade (specs/2026-09-28_nova_estrutura)

### Famílias com crianças até 72 meses no Cadastro Único, por renda
- nota: nome no catálogo da equipe: "Famílias com crianças até 6 anos no Cadastro Único, por renda"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_familias_por_faixa_renda.png`
- visualização: `cadunico_criancas_por_faixa_renda.png`
- tabela: `cadunico_por_faixa_renda_2026.csv`
- nota: movido de Família e Cuidados para Prioridade (specs/2026-09-28_nova_estrutura)

### Famílias no CadÚnico com crianças até 72 meses, por sexo
- nota: nome no catálogo da equipe: "Famílias no CadÚnico com crianças até 6 anos, por sexo"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_criancas_por_sexo.png`
- visualização: `cadunico_familias_por_sexo_criancas.png`
- tabela: `cadunico_por_sexo_2026.csv`
- tabela: `tabela_mapa_cadunico_recortes_bairro_2026.csv`
- nota: sexo da criança; famílias pela composição de sexo das crianças (só meninas / só meninos / ambos); 0 a 5 anos completos; bairros com menos de 20 famílias suprimidos
- nota: movido de Inclusão para Prioridade (specs/2026-09-28_nova_estrutura)

### Famílias no CadÚnico com crianças até 72 meses, por raça/cor
- nota: nome no catálogo da equipe: "Famílias no CadÚnico com crianças até 6 anos, por raça/cor"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Cadastro Único (extração CTPE)
- eixo transversal: Proteção
- visualização: `cadunico_criancas_por_raca_cor.png`
- visualização: `cadunico_familias_por_raca_cor.png`
- mapa: `mapa_percentual_cadunico_criancas_negras_bairro_2026.png`
- tabela: `cadunico_por_raca_cor_2026.csv`
- tabela: `tabela_mapa_cadunico_recortes_bairro_2026.csv`
- nota: raça/cor da criança; famílias com ao menos uma criança da categoria (não somam); por bairro só o % de crianças negras (privacidade); 0 a 5 anos completos
- nota: movido de Inclusão para Prioridade (specs/2026-09-28_nova_estrutura)

## 🤝 Inclusão

### Crianças no CadÚnico com alguma deficiência
- fonte: Cadastro Único
- status: pendente
- motivo: Os dados de deficiência dependem de uma nova extração do Cadastro Único, ainda não disponível.
- nota: baixar dados — Léo

### Famílias no CadÚnico com criança com deficiência
- fonte: Cadastro Único
- status: pendente
- motivo: Os dados de deficiência dependem de uma nova extração do Cadastro Único, ainda não disponível.
- nota: baixar dados — Léo

### Crianças no CadÚnico por tipo de deficiência
- fonte: Cadastro Único
- status: pendente
- motivo: Os dados de deficiência dependem de uma nova extração do Cadastro Único, ainda não disponível.
- nota: baixar dados — Léo

## 👨‍👩‍👧 Família e Cuidados

### Crianças até 72 meses frequentando escola/creche (geral)
- nota: nome no catálogo da equipe: "Crianças até 6 anos frequentando escola/creche (geral)"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Censo Demográfico 2022 (IBGE SIDRA, tabela 10057)
- visualização: `sidra_frequencia_escola_0_5_total_2022.png`
- tabela: `sidra_frequencia_escola_0_5_total_2022.csv`
- nota: faixa real 0 a 5 anos (a tabela 10057 vai só até 5 anos); total de todas as raças e sexos, por idade (`specs/2026-09-24_populacao-referencia`, D3)
- nota: posto no início do bloco de educação, antes dos recortes por raça/cor e sexo (sugestão S4 de specs/2026-09-28_nova_estrutura)

### Crianças até 72 meses frequentando escola/creche, por raça/cor
- nota: nome no catálogo da equipe: "Crianças até 6 anos frequentando escola/creche, por raça/cor"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Censo Demográfico 2022 (IBGE SIDRA)
- eixo transversal: Proteção
- visualização: `sidra_taxa_frequencia_0_6_raca_2022.png`
- tabela: `sidra_taxa_frequencia_0_6_raca_2022.csv`
- nota: faixa real 0 a 5 anos: taxa publicada pelo IBGE (tabela 10056, os 6 anos ficam de fora); total de 0 a 5 anos e "Amarela e indígena" agregados de taxa × população (tabela 9606); amarela e indígena só no total, fora das barras por idade (specs/2026-09-29_pendencias D9, D14, D15; specs/exclusoes.md E12)

- nota: sidra_frequencia_escola_0_5_raca_2022.png, sidra_frequencia_escola_0_5_raca_2022.csv fora do relatório (specs/exclusoes.md, E8, 2026-09-25): número absoluto; fica a taxa por idade
- nota: movido de Inclusão para Família e Cuidados (specs/2026-09-28_nova_estrutura)
### Crianças até 72 meses frequentando escola/creche, por sexo
- nota: nome no catálogo da equipe: "Crianças até 6 anos frequentando escola/creche, por sexo"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Censo Demográfico 2022 (IBGE SIDRA)
- visualização: `sidra_taxa_frequencia_0_6_sexo_2022.png`
- tabela: `sidra_taxa_frequencia_0_6_sexo_2022.csv`
- nota: faixa real 0 a 5 anos: taxa publicada pelo IBGE (tabela 10056, os 6 anos ficam de fora); total de 0 a 5 anos agregado de taxa × população (tabela 9606) (specs/2026-09-29_pendencias D9, D14)

- nota: sidra_frequencia_escola_0_5_sexo_2022.png, sidra_frequencia_escola_0_5_sexo_2022.csv fora do relatório (specs/exclusoes.md, E8, 2026-09-25): número absoluto; fica a taxa por idade
- nota: movido de Inclusão para Família e Cuidados (specs/2026-09-28_nova_estrutura)
### Taxa bruta de frequência escolar da população até 72 meses
- nota: nome no catálogo da equipe: "Taxa bruta de frequência escolar da população até 6 anos"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Censo Demográfico 2022 (IBGE SIDRA, tabela 10056)
- visualização: `sidra_taxa_frequencia_0_5_total_2022.png`
- tabela: `sidra_taxa_frequencia_0_5_total_2022.csv`
- nota: faixa real 0 a 5 anos. Até 2026-09-29 este item usava `pnad_frequencia_escolar_por_idade.png`, rotulado "PNAD Contínua", mas com exatamente a coluna Total da tabela 10056 do Censo 2022: fonte corrigida e duplicata tirada (specs/exclusoes.md E15; specs/2026-09-29_pendencias D16)

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

### Cobertura vacinal de rotina em crianças até 2 anos
- fonte: Epi Rio
- visualização: `cobertura_vacinal_epi_ano.png`
- tabela: `cobertura_vacinal_epi_por_ano.csv`
- nota: posta depois do bloco de educação, que antes ela interrompia (sugestão S4 de specs/2026-09-28_nova_estrutura)
- nota: `cobertura_vacinal_epi_ano.png` de volta em 2026-09-29 (specs/2026-09-29_alinhamento_pdf_site D2): chamada descomentada em analise.py, figura regerada

- nota: `cobertura_vacinal_epi_ano.png` removido do relatório em 2026-09-25 (specs/2026-09-25_relatorio_latex, D6): a chamada que gerava o arquivo está comentada em analise.py, então o PNG no disco é antigo
- nota: cobertura_vacinal_epi_comparativo_anos.png, cobertura_vacinal_epi_comparativo_anos.csv fora do relatório (specs/exclusoes.md, E7, 2026-09-25): repete 4 anos da série anual
### Famílias no CadÚnico com crianças até 72 meses, por renda e arranjo familiar
- nota: nome no catálogo da equipe: "Famílias no CadÚnico com crianças até 6 anos, por renda e arranjo familiar"; título com "até 72 meses" (0 a 5 anos completos, faixa padrão do projeto) desde 2026-09-29 (specs/2026-09-29_pendencias D9, D18; substitui a decisão C-D2 de specs/2026-09-24_populacao-referencia)
- fonte: Cadastro Único (extração CTPE)
- visualização: `cadunico_familias_por_arranjo.png`
- visualização: `cadunico_familias_arranjo_renda.png`
- mapa: `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png`
- tabela: `cadunico_familias_por_arranjo_2026.csv`
- tabela: `cadunico_familias_arranjo_renda_2026.csv`
- tabela: `tabela_mapa_cadunico_recortes_bairro_2026.csv`
- nota: arranjo aproximado pela composição do cadastro (adultos de 18+ por sexo), não é o conceito de monoparental do MDS; renda per capita; 0 a 5 anos completos
- nota: movido de Inclusão para Família e Cuidados (specs/2026-09-28_nova_estrutura)

## 🛡️ Proteção

### Violência familiar (0 a 5 anos, por vínculo do provável autor)
- fonte: Sinan NET/Tabnet (SMS-Rio); município: população 0 a 5 anos das estimativas Ripsa/Ministério da Saúde; RA: população 0 a 4 anos do Censo Demográfico 2022
- visualização: `violencia_familiar_serie_vinculos.png`
- visualização: `violencia_familiar_taxa_municipio_ano.png`
- mapa: `mapa_violencia_familiar_mae_taxa_ra_2025.png`
- mapa: `mapa_violencia_familiar_pai_taxa_ra_2025.png`
- mapa: `mapa_violencia_familiar_outros_taxa_ra_2021_2025.png`
- tabela: `violencia_familiar_por_vinculo_ano.csv`
- tabela: `violencia_familiar_taxa_municipio_ano.csv`
- nota: faixa 0 a 5 anos agregada (recorte menor de 1 ano x 1 a 5 anos pendente). Vínculos não são excludentes e não existe "total": nunca somar mãe + pai. Possível quebra de série em 2017 (hipótese: mudança de ficha/notificação, a confirmar com a fonte). 2026 é ano parcial e fica fora da série. Contagem absoluta não é risco
- nota: município (2011-2025): numerador e denominador com 0 a 5 anos e o mesmo ano (Ripsa), sem ressalva de faixa (`specs/2026-09-24_populacao-referencia`, A3). RA: ressalva de denominador — numerador com 0 a 5 anos (Sinan) e denominador com 0 a 4 anos (Censo 2022), o que superestima a taxa em ~20% de forma uniforme; o Censo 2022 é fixo (subconta crianças pequenas e é de outro ano), então as taxas por território comparam territórios entre si, não com a do município; "outros" usa o acumulado 2021-2025
- nota: nova estrutura (specs/2026-09-28_nova_estrutura): a taxa do município e os mapas de taxa por RA, antes no item "Taxa de notificações de violência familiar", vêm para cá (planilha da equipe); os mapas de contagem por bairro vão para "bairros com mais notificações"

- nota: mapa_violencia_familiar_mae_taxa_bairro_2025.png, mapa_violencia_familiar_pai_taxa_bairro_2025.png, mapa_violencia_familiar_outros_taxa_bairro_2021_2025.png fora do relatório (specs/exclusoes.md, E6, 2026-09-25): taxa por bairro instável (bairros com poucas crianças); fica a taxa por RA
### Violência familiar — composição de "outros" vínculos
- fonte: Sinan NET/Tabnet (SMS-Rio)
- visualização: `violencia_familiar_outros_serie.png`
- tabela: `violencia_familiar_outros_detalhe.csv`
- nota: "outros" = padrasto + irmão(ã) + cônjuge + ex-cônjuge + filho(a); pode contar uma mesma notificação mais de uma vez
- nota: a planilha da equipe (2026-09-28) deixa a visualização em branco; mantido o gráfico que já existia (specs/2026-09-28_nova_estrutura §4)

### Violência familiar — bairros com mais notificações (2025)
- fonte: Sinan NET/Tabnet (SMS-Rio); taxas: população 0 a 4 anos do Censo Demográfico 2022
- visualização: `violencia_familiar_top_bairros_2025.png`
- visualização: `violencia_familiar_taxa_top_bairros_2025.png`
- mapa: `mapa_violencia_familiar_mae_bairro_2025.png`
- mapa: `mapa_violencia_familiar_pai_bairro_2025.png`
- mapa: `mapa_violencia_familiar_outros_bairro_2021_2025.png`
- tabela: `violencia_familiar_top_bairros_2025.csv`
- tabela: `violencia_familiar_taxa_top_bairros_2025.csv`
- tabela: `violencia_familiar_por_bairro.csv`
- tabela: `violencia_familiar_taxa_por_bairro.csv`
- tabela: `tabela_mapa_violencia_familiar_mae_2025.csv`
- tabela: `tabela_mapa_violencia_familiar_pai_2025.csv`
- tabela: `tabela_mapa_violencia_familiar_outros_2021_2025.csv`
- nota: contagem absoluta, ordenada pelo vínculo mãe; bairros populosos lideram. Dez maiores taxas: só bairros com 100 ou mais crianças de 0 a 4 anos (taxa instável abaixo disso)
- nota: nova estrutura (specs/2026-09-28_nova_estrutura): recebe os mapas de contagem por bairro (antes em "Violência familiar ... por vínculo") e o gráfico das dez maiores taxas (antes em "Taxa de notificações")

### Violência familiar — por CAP
- fonte: Sinan NET/Tabnet (SMS-Rio); população 0 a 4 anos do Censo 2022
- tabela: `violencia_familiar_por_cap.csv`
- nota: casos somados por CAP e taxa por 1.000 recalculada depois de somar casos e população (nunca média de taxas)
- tabela_no_texto: `violencia_familiar_por_cap.csv`

### Notificações de violência interpessoal/autoprovocada (menores de 1 ano, 1 a 5 anos)
- fonte: Sinan NET/Tabnet (SMS-Rio)
- visualização: `notif_autoprovocada_antes_2026_vs_2026.png`
- mapa: `mapa_notif_autoprovocada_bairro_2026.png`
- tabela: `notif_autoprovocada_por_bairro_ano.csv`
- tabela: `tabela_mapa_notif_autoprovocada_2026.csv`
- nota: parcial — só lesão autoprovocada (a violência interpessoal total e o recorte menor de 1 ano x 1 a 5 anos estão pendentes). 40 casos em 2018-2026, 33 deles em 2026 (ano parcial, usado como referência desta série); o salto pode refletir mudança de registro administrativo (hipótese, a confirmar com a fonte)

### Taxa de notificações de violência (todas as naturezas)
- fonte: Sinan NET/Tabnet (SMS-Rio)
- eixo transversal: Direito ao Brincar
- status: pendente
- motivo: A taxa de notificações de violência em geral, não apenas familiar, ainda não foi extraída do Sinan.
- nota: a planilha da equipe (2026-09-28) deixa este item sem visualização: as taxas de violência FAMILIAR (antes aqui) foram para "Violência familiar ... por vínculo" e "bairros com mais notificações". Fica pendente a taxa de notificações de violência em geral (não só familiar), que ainda não foi extraída (specs/2026-09-28_nova_estrutura §4)

### Crianças que sofrem violência, por tipificação (sexo e idade)
- fonte: Tabnet municipal
- status: pendente
- motivo: Os dados por tipo de violência, sexo e idade ainda não foram extraídos do Tabnet municipal.
- nota: dado ainda não extraído do Tabnet

## 🧸 Direito ao Brincar

### Violência territorial
- fonte: Data.Rio / Índice de Progresso Social (IPS) 2024, por Região Administrativa
- eixo transversal: Proteção
- mapa: `mapa_violencia_territorial_homicidios_ra_2024.png`
- mapa: `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png`
- mapa: `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png`
- tabela: `tabela_mapa_violencia_territorial_ra_2024.csv`
- nota: dado GERAL da população (todas as idades) — não é específico de crianças (0 a 6 anos) nem de jovens; só 2024 e sem série temporal (apenas mapas, sem barras nem tabela por RA); nível Região Administrativa; RA XXI Paquetá sem dado no IPS. Substitui a fonte "ISP" do catálogo
- nota: movido de Proteção para o eixo novo Direito ao Brincar (planilha da equipe: "direito a brincar"; decisão do usuário de criar o 7º eixo, 2026-09-28, specs/2026-09-28_nova_estrutura)

## 🍽️ Alimentação

### Baixo peso ao nascer (número)
- fonte: DataSUS/Tabnet (`limpeza_tabnet_bairros`)
- mapa: `mapa_nascidos_baixo_peso_bairro_2025.png`
- tabela: `nascidos_abaixo_peso_por_ano.csv`
- nota: a planilha da equipe (2026-09-28) lista aqui também o cartão do SISVAN; ele continua nos itens do SISVAN abaixo (sugestão S5 de specs/2026-09-28_nova_estrutura)

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
- motivo: As características do domicílio dependem de uma nova extração do Cadastro Único, prevista para uma próxima edição.
- nota: Posterior

### Crianças no CadÚnico em domicílios com adensamento habitacional excessivo (acima de 3 por dormitório)
- fonte: Cadastro Único
- status: pendente
- motivo: As características do domicílio dependem de uma nova extração do Cadastro Único, prevista para uma próxima edição.
- nota: Posterior

### Indicadores agregados de moradia (inadequação, saneamento, melhorias habitacionais)
- fonte: (não informada no catálogo)
- status: pendente
- motivo: Previsto para uma próxima edição, a partir do Cadastro Único.
- nota: Posterior (apenas cad)
