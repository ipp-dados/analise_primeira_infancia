"""CSV de tabelas_finais/ -> tabela ABNT/IBGE em LaTeX (longtable + booktabs) para os apêndices.

Regras gerais (specs/relatorio_latex §3, validation V13): tabela aberta nas laterais, título acima,
Fonte abaixo; números em pt-BR (1.234,5); coluna de ano/idade/código sem separador de milhar; percentual
com 1 casa; linhas de total em negrito.

Regras de tamanho (T4.4, decididas pelo usuário em 2026-09-25):
  1. tabela por bairro com coluna `ano` e mais de 100 linhas -> só o ano mais recente (completo: se houver
     `ano_parcial`, o último ano não parcial); o ano vai para o título;
  2. depois disso, mais de `MAX_LINHAS_PDF` linhas -> não é impressa (fica só no formato digital);
  3. tabela por bairro: sem colunas de código e sem `ano` constante, em ordem alfabética; com até
     `MAX_COLUNAS_DUAS` colunas, duas colunas lado a lado em retrato; até `MAX_COLUNAS_DUAS_PAISAGEM`,
     duas colunas em paisagem; mais largas, uma coluna em paisagem.
Ajustes por arquivo (colunas, rótulos, escala) ficam em `AJUSTES` -- o que o Bloco 4 porta de
build_notebook_report.py.
"""
import hashlib
import math
import re
import unicodedata
from pathlib import Path

import pandas as pd

MAX_COLUNAS_RETRATO = 7
MAX_LINHAS_PDF = 200
LIMIAR_ULTIMO_ANO = 100
MAX_COLUNAS_DUAS = 5              # tabela por bairro em duas colunas, página em retrato
MAX_COLUNAS_DUAS_PAISAGEM = 8     # ... ou em paisagem; acima disso, uma coluna só (paisagem)
COLUNAS_CODIGO = re.compile(r"^(codigo|codbairro|codra|cod_ap_sms|cod_rp|area_plane)$", re.I)
COLUNAS_SEM_MILHAR = re.compile(r"^(ano|idade|cod\w*|codigo|cap|ap|rp|ra)$", re.I)
COLUNAS_PCT = re.compile(r"(percent|%|taxa|propor|cobertura)", re.I)
NOTA_SUPRESSAO = ("Nota: -- indica célula suprimida (menos de 20 famílias ou crianças), "
                  "conforme a regra de proteção de dados do Cadastro Único.")

# nome do arquivo -> ajustes (Bloco 4, T4.1; títulos portados de build_notebook_report.py e completados):
#   titulo      título ABNT (o período -- "2006-2025" ou o ano -- é acrescentado sozinho)
#   colunas     colunas a manter, na ordem, pelo nome ORIGINAL do CSV (depois do pivô)
#   renomeia    {nome original: rótulo}
#   pivo        (índice, colunas, valores) -- formato longo -> largo
#   filtro      função df -> df, aplicada antes do pivô
#   ultimo_ano  True: só o ano mais recente (também fora das tabelas por bairro)
#   escala_pct  colunas em fração 0-1 que viram 0-100
_TX = "Taxa (‰)"
_RACAS_OBITOS = {"obitos_parda": "Parda", "obitos_preta": "Preta", "obitos_branca": "Branca",
                 "obitos_amarela": "Amarela", "obitos_indigena": "Indígena", "obitos_nao_informado": "Não informada"}
AJUSTES = {
    # --- Prioridade
    "censo_0_a_4_anos_por_ano.csv": {"titulo": "População de 0 a 4 anos, por sexo, Censos Demográficos",
        "colunas": ["ano", "0 a 4 anos", "Sexo feminino, 0 a 4 anos", "Sexo masculino, 0 a 4 anos", "Total", "Percentual 0 a 4 anos"],
        "renomeia": {"Sexo feminino, 0 a 4 anos": "Meninas", "Sexo masculino, 0 a 4 anos": "Meninos",
                     "Total": "População total", "Percentual 0 a 4 anos": "% 0 a 4 anos"}},
    "censo_por_bairro.csv": {"titulo": "População de 0 a 4 e de 5 a 9 anos, por bairro, Censo Demográfico 2022"},
    "populacao_ripsa_0_a_6_por_ano.csv": {"titulo": "População de 0 a 6 anos, estimativas Ripsa/Ministério da Saúde",
        "colunas": ["ano", "populacao_0_a_5", "populacao_0_a_6", "populacao_total", "percentual_0_a_6"],
        "renomeia": {"populacao_0_a_5": "0 a 5 anos", "populacao_0_a_6": "0 a 6 anos", "populacao_total": "População total",
                     "percentual_0_a_6": "% 0 a 6 anos"}},
    "nascidos_vivos_por_ano.csv": {"titulo": "Nascidos vivos de mães residentes no município"},
    "tabela_mapa_nascidos_vivos_2025.csv": {"titulo": "Nascidos vivos por bairro de residência da mãe",
        "renomeia": {"percentual_do_municipio": "% do município"}},
    "mortalidade_neonatal_precoce_por_ano.csv": {"titulo": "Mortalidade neonatal precoce (0 a 6 dias)",
        "renomeia": {"obitos precoces": "Óbitos", "taxa_mortalidade_precoce": _TX}},
    "mortalidade_neonatal_precoce_bairro_ano.csv": {"titulo": "Mortalidade neonatal precoce (0 a 6 dias), por bairro",
        "renomeia": {"obitos precoces": "Óbitos", "taxa_mortalidade_precoce": _TX}},
    "tabela_mapa_obitos_neonatal_precoce_2025.csv": {"titulo": "Mortalidade neonatal precoce (0 a 6 dias), por bairro",
        "renomeia": {"obitos precoces": "Óbitos", "taxa_mortalidade_precoce": _TX}},
    "mortalidade_neonatal_tardia_por_ano.csv": {"titulo": "Mortalidade neonatal tardia (7 a 27 dias)",
        "renomeia": {"obitos_tardios": "Óbitos", "taxa_obitos_tardios": _TX}},
    "mortalidade_neonatal_tardia_bairro_ano.csv": {"titulo": "Mortalidade neonatal tardia (7 a 27 dias), por bairro",
        "renomeia": {"obitos_tardios": "Óbitos", "taxa_obitos_tardios": _TX}},
    "tabela_mapa_obitos_neonatal_tardia_2025.csv": {"titulo": "Mortalidade neonatal tardia (7 a 27 dias), por bairro",
        "renomeia": {"obitos_tardios": "Óbitos", "taxa_obitos_tardios": _TX}},
    "obitos_gravidez_por_ano.csv": {"titulo": "Óbitos maternos durante a gravidez", "renomeia": {"óbitos-gravidez": "Óbitos"}},
    "obitos_gravidez_bairro_ano.csv": {"titulo": "Óbitos maternos durante a gravidez, por bairro", "renomeia": {"óbitos-gravidez": "Óbitos"}},
    "tabela_mapa_obitos_gravidez_2025.csv": {"titulo": "Óbitos maternos durante a gravidez, por bairro", "renomeia": {"óbitos-gravidez": "Óbitos"}},
    "obitos_puerperio_por_ano.csv": {"titulo": "Óbitos maternos durante o puerpério", "renomeia": {"óbitos-puerpério": "Óbitos"}},
    "obitos_puerperio_bairro_ano.csv": {"titulo": "Óbitos maternos durante o puerpério, por bairro", "renomeia": {"óbitos-puerpério": "Óbitos"}},
    "tabela_mapa_obitos_puerperio_2025.csv": {"titulo": "Óbitos maternos durante o puerpério, por bairro", "renomeia": {"óbitos-puerpério": "Óbitos"}},
    "mortalidade_raca_municipio_ano.csv": {"titulo": "Óbitos de menores de 1 ano, por raça/cor",
        "colunas": ["ano"] + list(_RACAS_OBITOS), "renomeia": _RACAS_OBITOS},
    "mortalidade_raca_bairro_ano.csv": {"titulo": "Óbitos de menores de 1 ano, por raça/cor e bairro",
        "colunas": ["bairro"] + list(_RACAS_OBITOS) + ["obitos_total"], "renomeia": {**_RACAS_OBITOS, "obitos_total": "Total"}},
    "tabela_mapa_obitos_raca_total_2025.csv": {"titulo": "Óbitos de menores de 1 ano, por raça/cor e bairro",
        "colunas": ["bairro"] + list(_RACAS_OBITOS) + ["obitos_total"], "renomeia": {**_RACAS_OBITOS, "obitos_total": "Total"}},
    "mortalidade_evitaveis_cap_2025.csv": {"titulo": "Óbitos por causas evitáveis, por CAP e faixa etária",
        "colunas": ["cod_ap_sms", "faixa_etaria", "evitaveis", "mal_definidas", "demais", "total", "percentual_evitaveis"],
        "renomeia": {"cod_ap_sms": "CAP", "faixa_etaria": "Faixa etária", "mal_definidas": "Mal definidas",
                     "percentual_evitaveis": "% evitáveis"}},
    "taxa_mortalidade_evitaveis_menores_5_municipio_ano.csv": {
        "titulo": "Mortalidade por causas evitáveis de menores de 5 anos", "renomeia": {"taxa_por_mil": _TX}},
    "mortalidade_infantil_pos_neonatal_total_por_ano.csv": {"titulo": "Mortalidade infantil (0 a 364 dias) e pós-neonatal (28 a 364 dias)",
        "renomeia": {"obitos_0_364": "Óbitos 0-364 dias", "obitos_28_364": "Óbitos 28-364 dias",
                     "taxa_mortalidade_infantil": "Taxa infantil (‰)", "taxa_mortalidade_pos_neonatal": "Taxa pós-neonatal (‰)"}},
    "mortalidade_infantil_pos_neonatal_total_bairro_ano.csv": {"titulo": "Mortalidade infantil e pós-neonatal, por bairro",
        "colunas": ["bairro", "obitos_0_364", "obitos_28_364", "nascidos_vivos", "taxa_mortalidade_infantil", "taxa_mortalidade_pos_neonatal"],
        "renomeia": {"obitos_0_364": "Óbitos 0-364 d", "obitos_28_364": "Óbitos 28-364 d",
                     "taxa_mortalidade_infantil": "Taxa infantil (‰)", "taxa_mortalidade_pos_neonatal": "Taxa pós-neonatal (‰)"}},
    "tabela_mapa_mortalidade_infantil_2025.csv": {"titulo": "Mortalidade infantil e pós-neonatal, por bairro",
        "colunas": ["bairro", "obitos_0_364", "obitos_28_364", "nascidos_vivos", "taxa_mortalidade_infantil", "taxa_mortalidade_pos_neonatal"],
        "renomeia": {"obitos_0_364": "Óbitos 0-364 d", "obitos_28_364": "Óbitos 28-364 d",
                     "taxa_mortalidade_infantil": "Taxa infantil (‰)", "taxa_mortalidade_pos_neonatal": "Taxa pós-neonatal (‰)"}},
    "mortalidade_causas_evitaveis_grupo_ano.csv": {"titulo": "Óbitos de menores de 1 ano, por grupo de causa (evitabilidade)"},
    "mortalidade_causas_evitaveis_subgrupo_ano.csv": {"titulo": "Óbitos de menores de 1 ano, por subgrupo de causa evitável"},
    "mortalidade_causas_evitaveis_grupo_0_a_6_dias_ano.csv": {"titulo": "Óbitos de 0 a 6 dias, por grupo de causa (evitabilidade)"},
    "mortalidade_causas_evitaveis_subgrupo_0_a_6_dias_ano.csv": {"titulo": "Óbitos de 0 a 6 dias, por subgrupo de causa evitável"},
    "mortalidade_causas_evitaveis_grupo_7_a_27_dias_ano.csv": {"titulo": "Óbitos de 7 a 27 dias, por grupo de causa (evitabilidade)"},
    "mortalidade_causas_evitaveis_subgrupo_7_a_27_dias_ano.csv": {"titulo": "Óbitos de 7 a 27 dias, por subgrupo de causa evitável"},
    "mortalidade_causas_evitaveis_grupo_28_a_364_dias_ano.csv": {"titulo": "Óbitos de 28 a 364 dias, por grupo de causa (evitabilidade)"},
    "mortalidade_causas_evitaveis_subgrupo_28_a_364_dias_ano.csv": {"titulo": "Óbitos de 28 a 364 dias, por subgrupo de causa evitável"},
    "mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv": {"titulo": "Óbitos de menores de 1 ano por causas evitáveis, por subgrupo e faixa etária",
        "ultimo_ano": True, "pivo": ("subgrupo", "faixa_etaria", "obitos"), "renomeia": {"subgrupo": "Subgrupo"}},
    "obitos_evitaveis_menores_5_subgrupo_municipio_ano.csv": {"titulo": "Óbitos de menores de 5 anos por causas evitáveis, por subgrupo",
        "pivo": ("ano", "subgrupo", "obitos")},
    "mortalidade_evitaveis_subgrupo_cap_2025.csv": {"titulo": "Óbitos por causas evitáveis, por subgrupo, CAP e faixa etária, 2025",
        "renomeia": {"cod_ap_sms": "CAP", "faixa_etaria": "Faixa etária"}},
    # --- Inclusão
    "censo_sidra_populacao_0_6_sexo_2022.csv": {"titulo": "População de 0 a 6 anos, por idade e sexo, Censo Demográfico 2022"},
    "censo_sidra_populacao_0_6_raca_2022.csv": {"titulo": "População de 0 a 6 anos, por idade e cor ou raça, Censo Demográfico 2022"},
    "sidra_frequencia_escola_0_5_raca_2022.csv": {"titulo": "Crianças de 0 a 5 anos que frequentam escola ou creche, por idade e cor ou raça, Censo Demográfico 2022"},
    "sidra_taxa_frequencia_0_6_raca_2022.csv": {"titulo": "Taxa de frequência escolar bruta de 0 a 6 anos (%), por idade e cor ou raça, Censo Demográfico 2022"},
    "sidra_frequencia_escola_0_5_sexo_2022.csv": {"titulo": "Crianças de 0 a 5 anos que frequentam escola ou creche, por idade e sexo, Censo Demográfico 2022"},
    "sidra_taxa_frequencia_0_6_sexo_2022.csv": {"titulo": "Taxa de frequência escolar bruta de 0 a 6 anos (%), por idade e sexo, Censo Demográfico 2022"},
    "cadunico_razao_populacao_0_a_5_2026.csv": {"titulo": "Crianças de 0 a 5 anos no CadÚnico em relação à população do município",
        "colunas": ["criancas_cadunico_0_a_5", "familias_cadunico", "populacao_ripsa_0_a_5", "razao_percentual"],
        "renomeia": {"criancas_cadunico_0_a_5": "Crianças no CadÚnico", "familias_cadunico": "Famílias no CadÚnico",
                     "populacao_ripsa_0_a_5": "População 0 a 5 (Ripsa, 2025)", "razao_percentual": "Razão (%)"}},
    "cadunico_por_sexo_2026.csv": {"titulo": "Crianças de 0 a 5 anos e suas famílias no CadÚnico, por sexo"},
    "tabela_mapa_cadunico_recortes_bairro_2026.csv": {"titulo": "Crianças de 0 a 5 anos e famílias no CadÚnico, por bairro: meninas, crianças negras e famílias com uma só adulta",
        "colunas": ["bairro", "Crianças", "% meninas", "% crianças negras", "Famílias", "% famílias com uma adulta"]},
    "cadunico_por_raca_cor_2026.csv": {"titulo": "Crianças de 0 a 5 anos no CadÚnico, por raça/cor",
        "colunas": ["raça/cor da criança", "Crianças", "% das crianças", "Famílias com ao menos uma"],
        "renomeia": {"raça/cor da criança": "Raça/cor"}},
    "cadunico_familias_por_arranjo_2026.csv": {"titulo": "Famílias com crianças de 0 a 5 anos no CadÚnico, por arranjo familiar"},
    "cadunico_familias_arranjo_renda_2026.csv": {"titulo": "Famílias com crianças de 0 a 5 anos no CadÚnico, por arranjo familiar e renda per capita (% das famílias do arranjo)",
        "pivo": ("arranjo", "faixa de renda per capita", "% no arranjo"), "renomeia": {"arranjo": "Arranjo familiar"}},
    # --- Família e Cuidados
    "cadunico_por_idade_2026.csv": {"titulo": "Crianças de 0 a 5 anos e famílias no CadÚnico, por idade"},
    "cadunico_por_bairro_2026.csv": {"titulo": "Crianças de 0 a 5 anos e famílias no CadÚnico, por bairro"},
    "cadunico_por_bairro_ate_4_2026.csv": {"titulo": "Crianças de 0 a 4 anos e famílias no CadÚnico, por bairro"},
    "tabela_mapa_cadunico_criancas_2026.csv": {"titulo": "Crianças de 0 a 5 anos e famílias no CadÚnico, por bairro (tabela do mapa)"},
    "tabela_mapa_cadunico_criancas_0_a_4_2026.csv": {"titulo": "Crianças de 0 a 4 anos no CadÚnico em relação à população de 0 a 4 anos (Censo 2022), por bairro",
        "colunas": ["bairro", "Primeira Inf. Cadúnico", "0 a 4 anos", "Percentual Primeira Inf. Cadúnico"],
        "renomeia": {"Primeira Inf. Cadúnico": "No CadÚnico", "0 a 4 anos": "População (Censo)",
                     "Percentual Primeira Inf. Cadúnico": "% no CadÚnico"}},
    "cadunico_por_faixa_renda_2026.csv": {"titulo": "Crianças de 0 a 5 anos e famílias no CadÚnico, por faixa de renda per capita",
        "colunas": ["faixa de renda (descrição)", "Crianças", "Famílias"], "renomeia": {"faixa de renda (descrição)": "Faixa de renda"}},
    "frequencia_escolar_pnad_por_idade.csv": {"titulo": "Frequência escolar (%) por idade, PNAD Contínua"},
    "cobertura_vacinal_epi_por_ano.csv": {"titulo": "Cobertura vacinal (%) por imunobiológico"},
    "cobertura_vacinal_epi_comparativo_anos.csv": {"titulo": "Cobertura vacinal (%) por imunobiológico, anos selecionados",
        "pivo": ("imunobiologico", "ano", "cobertura"), "renomeia": {"imunobiologico": "Imunobiológico"}},
    "sidra_frequencia_escola_0_5_total_2022.csv": {"titulo": "Crianças de 0 a 5 anos que frequentam escola ou creche, por idade, Censo Demográfico 2022"},
    "matriculas_0_a_5_por_ano.csv": {"titulo": "Matrículas e taxa bruta de atendimento escolar de 0 a 5 anos",
        "colunas": ["ano", "matriculas_0_a_3", "matriculas_4_a_5", "matriculas", "taxa_atendimento_0_a_3", "taxa_atendimento_4_a_5", "taxa_atendimento_0_a_5"],
        "renomeia": {"matriculas_0_a_3": "Matrículas 0-3", "matriculas_4_a_5": "Matrículas 4-5", "matriculas": "Matrículas 0-5",
                     "taxa_atendimento_0_a_3": "Atendimento 0-3 (%)", "taxa_atendimento_4_a_5": "Atendimento 4-5 (%)",
                     "taxa_atendimento_0_a_5": "Atendimento 0-5 (%)"}},
    # --- Proteção
    "tabela_mapa_violencia_territorial_ra_2024.csv": {"titulo": "Indicadores de violência territorial por Região Administrativa, IPS 2024",
        "colunas": ["regiao_adm", "taxa_homicidios", "homicidios_acao_policial", "homicidios_jovens_negros"],
        "renomeia": {"regiao_adm": "Região Administrativa", "taxa_homicidios": "Taxa de homicídios",
                     "homicidios_acao_policial": "Homicídios por ação policial", "homicidios_jovens_negros": "Homicídios de jovens negros"}},
    "violencia_familiar_por_vinculo_ano.csv": {"titulo": "Notificações de violência familiar contra crianças de 0 a 5 anos, por vínculo do provável autor"},
    "violencia_familiar_por_bairro.csv": {"titulo": "Notificações de violência familiar contra crianças de 0 a 5 anos, por vínculo e bairro"},
    "tabela_mapa_violencia_familiar_mae_2025.csv": {"titulo": "Notificações de violência familiar (autora: mãe), por bairro, 2025"},
    "tabela_mapa_violencia_familiar_pai_2025.csv": {"titulo": "Notificações de violência familiar (autor: pai), por bairro, 2025"},
    "tabela_mapa_violencia_familiar_outros_2021_2025.csv": {"titulo": "Notificações de violência familiar (outros vínculos), por bairro, 2021-2025",
        "renomeia": {"outros_2021_2025": "Outros vínculos"}},
    "violencia_familiar_outros_detalhe.csv": {"titulo": "Notificações de violência familiar: detalhe dos outros vínculos"},
    "violencia_familiar_top_bairros_2025.csv": {"titulo": "Bairros com mais notificações de violência familiar, por vínculo, 2025"},
    "violencia_familiar_por_cap.csv": {"titulo": "Notificações de violência familiar e taxa por mil crianças de 0 a 4 anos, por CAP",
        "ultimo_ano": True, "renomeia": {"cod_ap_sms": "CAP", "pop_0_4": "População 0-4 (Censo)",
        "taxa_por_mil_mae": "Taxa mãe (‰)", "taxa_por_mil_pai": "Taxa pai (‰)", "taxa_por_mil_outros": "Taxa outros (‰)"}},
    "notif_autoprovocada_por_bairro_ano.csv": {"titulo": "Notificações de lesão autoprovocada, 0 a 5 anos, por bairro"},
    "tabela_mapa_notif_autoprovocada_2026.csv": {"titulo": "Notificações de lesão autoprovocada, 0 a 5 anos, por bairro, 2018-2026"},
    "violencia_familiar_taxa_municipio_ano.csv": {"titulo": "Notificações de violência familiar por mil crianças de 0 a 5 anos, por vínculo",
        "renomeia": {"populacao_0_a_5": "População 0-5 (Ripsa)", "taxa_por_mil_mae": "Taxa mãe (‰)",
                     "taxa_por_mil_pai": "Taxa pai (‰)", "taxa_por_mil_outros": "Taxa outros (‰)"}},
    "violencia_familiar_taxa_por_bairro.csv": {"titulo": "Notificações de violência familiar por mil crianças de 0 a 4 anos, por bairro",
        "colunas": ["bairro", "taxa_por_mil_mae_2025", "taxa_por_mil_pai_2025", "taxa_por_mil_outros_2021_2025", "pop_0_4"],
        "renomeia": {"taxa_por_mil_mae_2025": "Mãe, 2025 (‰)", "taxa_por_mil_pai_2025": "Pai, 2025 (‰)",
                     "taxa_por_mil_outros_2021_2025": "Outros, 2021-2025 (‰)", "pop_0_4": "População 0-4 (Censo)"}},
    "violencia_familiar_taxa_top_bairros_2025.csv": {"titulo": "Bairros com as maiores taxas de notificação de violência familiar por mil crianças de 0 a 4 anos, 2025"},
    # --- Alimentação
    "nascidos_abaixo_peso_por_ano.csv": {"titulo": "Nascidos vivos com baixo peso (menos de 2.500 g)",
        "renomeia": {"nascidos abaixo peso": "Nascidos com baixo peso", "percentual abaixo do peso": "% do total"}},
    "sisvan_desnutricao_por_ano.csv": {"titulo": "Estado nutricional (peso para a idade) de crianças de 0 a 5 anos acompanhadas, SISVAN",
        "colunas": ["ano", "total", "peso_muito_baixo_percentual", "peso_baixo_percentual", "peso_adequado_percentual", "peso_elevado_percentual"],
        "renomeia": {"total": "Acompanhadas", "peso_muito_baixo_percentual": "Muito baixo (%)", "peso_baixo_percentual": "Baixo (%)",
                     "peso_adequado_percentual": "Adequado (%)", "peso_elevado_percentual": "Elevado (%)"}},
    "sisvan_sobrepeso_por_ano.csv": {"titulo": "Estado nutricional (IMC para a idade) de crianças de 0 a 5 anos acompanhadas, SISVAN",
        "colunas": ["ano", "total", "magreza_acentuada_percentual", "magreza_percentual", "eutrofia_percentual",
                    "risco sobrepeso_percentual", "sobrepeso_percentual", "obesidade_percentual"],
        "renomeia": {"total": "Acompanhadas", "magreza_acentuada_percentual": "Magreza acentuada (%)", "magreza_percentual": "Magreza (%)",
                     "eutrofia_percentual": "Eutrofia (%)", "risco sobrepeso_percentual": "Risco de sobrepeso (%)",
                     "sobrepeso_percentual": "Sobrepeso (%)", "obesidade_percentual": "Obesidade (%)"}},
}


def esc(s):
    s = str(s)
    trocas = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
              "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(trocas.get(c, c) for c in s)


def num(v, dec):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "--"
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def _sem_acento(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


CODIGOS_ESPECIAIS = {998: "Ilha do Governador (bairro ignorado)", 999: "Bairro ignorado"}
_NOMES = {}


def _nomes_oficiais():
    """codbairro -> nome oficial (dados_locais/geo/limite_bairros_rio.geojson, IPP/Data.Rio)."""
    if not _NOMES:
        import json
        raiz = Path(__file__).resolve().parents[3]
        geo = json.loads((raiz / "dados_locais/geo/limite_bairros_rio.geojson").read_text(encoding="utf-8"))
        _NOMES.update({int(f["properties"]["codbairro"]): f["properties"]["nome"].strip() for f in geo["features"]})
    return _NOMES


def _cabecalho(c):
    """Cabeçalho legível sem renomear à mão: 'peso_baixo_percentual' -> 'Peso baixo (%)',
    'Percentual 0 a 4' -> '% 0 a 4'."""
    s = re.sub(r"^(Percentual|Percent\.)\s+", "% ", str(c).strip())
    pct = bool(re.search(r"(^|_)(percentual|pct)($|_)", s))
    s = re.sub(r"(^|_)(percentual|pct)($|_)", " ", s).replace("_", " ").strip()
    s = _acentua(re.sub(r"\s+", " ", s))
    s = s[:1].upper() + s[1:] if s else s
    return f"{s} (%)" if pct else s


# palavras que chegam sem acento dos CSVs (nomes de coluna e categorias) -- troca palavra inteira
ACENTOS = {
    "obitos": "óbitos", "populacao": "população", "matriculas": "matrículas", "mae": "mãe", "irmao": "irmão",
    "conjuge": "cônjuge", "exconjuge": "ex-cônjuge", "municipio": "município", "raca": "raça",
    "indigena": "indígena", "nao": "não", "particao": "partição", "regiao": "região", "homicidios": "homicídios",
    "razao": "razão", "imunobiologico": "imunobiológico", "criancas": "crianças", "familias": "famílias",
    "vinculo": "vínculo", "etaria": "etária", "evitaveis": "evitáveis", "publica": "pública",
    "pos": "pós", "cadunico": "CadÚnico", "ripsa": "Ripsa", "acao": "ação", "policial": "policial",
    "adm": "administrativa", "cod": "código", "sms": "", "ap": "AP", "notificacoes": "notificações",
}


def _acentua(texto):
    def troca(m):
        p = m.group(0)
        novo = ACENTOS.get(p.lower())
        if novo is None:
            return p
        return novo[:1].upper() + novo[1:] if p[:1].isupper() and novo[:1].islower() else novo
    return re.sub(r"\s+", " ", re.sub(r"[A-Za-z]+", troca, str(texto))).strip()


# ------------------------------------------------------------------ preparação (cacheada)
_PREP = {}


def prepara(caminho):
    """(df, meta) já com as regras de tamanho aplicadas. meta: bairro, ano, suprimido, linhas_orig."""
    caminho = Path(caminho)
    if caminho in _PREP:
        return _PREP[caminho]
    aj = AJUSTES.get(caminho.name, {})
    df = pd.read_csv(caminho)
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed")]
    meta = {"linhas_orig": len(df), "ano": None, "suprimido": False, "periodo": None,
            "bairro": any(str(c).lower() == "bairro" for c in df.columns)}
    if "suprimido" in df.columns:
        meta["suprimido"] = bool(df["suprimido"].astype(bool).any())
        df = df.drop(columns="suprimido")
    if "ano" in df.columns and pd.api.types.is_numeric_dtype(df["ano"]) and df["ano"].nunique() > 1:
        meta["periodo"] = (int(df["ano"].min()), int(df["ano"].max()))
    if aj.get("ultimo_ano") or (meta["bairro"] and "ano" in df.columns and len(df) > LIMIAR_ULTIMO_ANO):
        anos = df.loc[~df["ano_parcial"].astype(bool), "ano"] if "ano_parcial" in df.columns else df["ano"]
        meta["ano"] = int(anos.max())
        df = df[df["ano"] == meta["ano"]].drop(columns="ano")
    if "ano_parcial" in df.columns and meta["ano"] is not None:
        df = df.drop(columns="ano_parcial")
    if aj.get("filtro"):
        df = aj["filtro"](df)
    if aj.get("pivo"):
        idx, col, val = aj["pivo"]
        ordem = list(dict.fromkeys(df[col]))
        df = df.pivot_table(index=idx, columns=col, values=val, aggfunc="sum", sort=False)[ordem].reset_index()
        df.columns = [str(c) for c in df.columns]
    for c in df.columns:     # "86.58%" (texto) -> 86.58 (número), para formatar em pt-BR
        if df[c].dtype == object and df[c].astype(str).str.fullmatch(r"-?\d+(\.\d+)?%").mean() > 0.8:
            df[c] = pd.to_numeric(df[c].astype(str).str.rstrip("%"), errors="coerce")
    for c in aj.get("escala_pct", []):
        df[c] = df[c] * 100
    if meta["bairro"]:
        # nome oficial do bairro pelo código (constituição §3: junção sempre pelo código, nunca pelo nome);
        # o Tabnet traz nomes em caixa alta e sem acento. Códigos sem bairro (998/999, "ignorado") vão ao fim.
        col_cod = next((c for c in df.columns if str(c).lower() in ("codigo", "codbairro")), None)
        col_b = next(c for c in df.columns if str(c).lower() == "bairro")
        df["_fim"] = 0
        if col_cod is not None:
            cods = pd.to_numeric(df[col_cod], errors="coerce")
            oficial = cods.map(_nomes_oficiais())
            df[col_b] = oficial.fillna(cods.map(CODIGOS_ESPECIAIS)).fillna(df[col_b])
            df["_fim"] = (cods.isin(list(CODIGOS_ESPECIAIS)) | oficial.isna()).astype(int)
        df = df.drop(columns=[c for c in df.columns if COLUNAS_CODIGO.match(str(c))])
        if "ano" in df.columns and df["ano"].nunique() == 1:
            meta["ano"] = meta["ano"] or int(df["ano"].iloc[0])
            df = df.drop(columns="ano")
        df = df[[col_b] + [c for c in df.columns if c != col_b]]
        df = (df.assign(_k=df[col_b].map(_sem_acento)).sort_values(["_fim", "_k"], kind="stable")
              .drop(columns=["_k", "_fim"]))
    elif "ano" in df.columns and not aj.get("sem_ordenar"):
        df = df.sort_values("ano", kind="stable")
    if aj.get("colunas"):
        df = df[aj["colunas"]]
    df = df.rename(columns=aj.get("renomeia", {}))
    for c in df.columns:     # categorias em texto sem acento ('mae', 'Nao informado') -> com acento
        if df[c].dtype == object and str(c).lower() != "bairro":
            df[c] = df[c].map(lambda v: _acentua(v) if isinstance(v, str) else v)
    df = df.rename(columns={c: _cabecalho(c) for c in df.columns}).reset_index(drop=True)
    _PREP[caminho] = (df, meta)
    return df, meta


def n_linhas(caminho):
    return len(prepara(caminho)[0])


def cabe_no_pdf(caminho):
    return n_linhas(caminho) <= MAX_LINHAS_PDF


def assinatura(caminho):
    """Mesmo conteúdo impresso = mesma assinatura (ex. série bairro×ano filtrada = tabela do mapa)."""
    df, meta = prepara(caminho)
    if meta["bairro"]:
        # série por bairro filtrada e tabela do mapa diferem às vezes só nas linhas "bairro ignorado":
        # mesmas colunas e mesmo ano contam como a mesma tabela (imprime-se a primeira)
        base = "bairro|" + "|".join(df.columns) + f"|{meta['ano']}"
    else:
        base = df.sort_values(list(df.columns)).to_csv(index=False) + str(meta["ano"])
    return hashlib.md5(base.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------ LaTeX
def _formata_coluna(serie, nome):
    if not pd.api.types.is_numeric_dtype(serie):
        return [esc(v) if not (isinstance(v, float) and math.isnan(v)) else "--" for v in serie], "l"
    if COLUNAS_SEM_MILHAR.match(str(nome).strip()):
        return [str(int(v)) if pd.notna(v) and float(v).is_integer() else (esc(v) if pd.notna(v) else "--") for v in serie], "r"
    inteira = serie.dropna().apply(lambda x: float(x).is_integer()).all()
    dec = 0 if inteira and not COLUNAS_PCT.search(str(nome)) else 1
    return [num(v, dec) for v in serie], "r"


def titulo_padrao(nome_arquivo, titulo_secao):
    base = Path(nome_arquivo).stem
    base = re.sub(r"^tabela_mapa_", "", base)
    return f"{titulo_secao} ({base.replace('_', ' ')})"


def _longtable(colspec, ncols, cab, corpo, titulo, rotulo, tamanho, sep):
    return (rf"{{{tamanho}\setlength{{\tabcolsep}}{{{sep}}}" "\n"
            rf"\begin{{longtable}}{{{colspec}}}" "\n"
            rf"\caption{{{titulo}}}\label{{{rotulo}}}\\" "\n"
            rf"\toprule {cab} \midrule \endfirsthead" "\n"
            rf"\multicolumn{{{ncols}}}{{@{{}}l}}{{\footnotesize\itshape (continuação)}}\\ \toprule {cab} \midrule \endhead" "\n"
            rf"\midrule \multicolumn{{{ncols}}}{{r@{{}}}}{{\footnotesize\itshape (continua)}}\\ \endfoot" "\n"
            r"\bottomrule \endlastfoot" "\n"
            f"{corpo}\n"
            r"\end{longtable}}" "\n")


def tabela_latex(caminho, titulo_secao, fonte_tex, rotulo):
    nome = Path(caminho).name
    aj = AJUSTES.get(nome, {})
    df, meta = prepara(caminho)
    titulo = aj.get("titulo") or titulo_padrao(nome, titulo_secao)
    tem_ano = re.search(r"\b(19|20)\d\d\b", titulo)
    if meta["ano"] and not tem_ano:
        titulo += f", {meta['ano']}"
    elif meta["periodo"] and not tem_ano:
        titulo += f", {meta['periodo'][0]}-{meta['periodo'][1]}"
    titulo = esc(titulo)
    fonte = fonte_tex + (" " + NOTA_SUPRESSAO if meta["suprimido"] else "")

    colunas, specs = [], []
    for c in df.columns:
        vals, al = _formata_coluna(df[c], c)
        colunas.append(vals)
        specs.append(al)
    n, ncol = len(df), len(df.columns)

    def celulas(i):
        cs = [colunas[j][i] for j in range(ncol)]
        if str(cs[0]).strip().lower().startswith("total"):
            cs = [r"\textbf{" + c + "}" for c in cs]
        return cs

    if meta["bairro"] and ncol <= MAX_COLUNAS_DUAS_PAISAGEM and n > 30:
        # duas colunas lado a lado: linhas 1..m à esquerda, m+1..n à direita. Retrato até
        # MAX_COLUNAS_DUAS colunas, paisagem até MAX_COLUNAS_DUAS_PAISAGEM (larguras em cm)
        paisagem = ncol > MAX_COLUNAS_DUAS
        util, vao = (24.5 if paisagem else 16.0), 0.6
        pequeno = paisagem or ncol > 4
        larg_bairro = 2.9 if pequeno else 3.2
        meia_larg = (util - vao) / 2
        larg_num = (meia_larg - larg_bairro) / (ncol - 1) - 0.25     # 0,25 cm = 2 x \tabcolsep
        meia = [rf">{{\raggedright\arraybackslash}}p{{{larg_bairro - 0.25:.2f}cm}}"] + \
               [rf">{{\raggedleft\arraybackslash}}p{{{larg_num:.2f}cm}}"] * (ncol - 1)
        colspec = "@{}" + "".join(meia) + rf"@{{\hspace{{{vao}cm}}}}" + "".join(meia) + "@{}"
        # cabeçalho quebra só em espaço (sem hifenizar "mortali-dade" numa coluna estreita)
        cab1 = " & ".join(r"\hyphenpenalty=10000\exhyphenpenalty=10000\textbf{" + esc(c) + "}" for c in df.columns)
        cab = f"{cab1} & {cab1} " + r"\\"
        m = math.ceil(n / 2)
        linhas = []
        for i in range(m):
            dir_ = celulas(i + m) if i + m < n else [""] * ncol
            linhas.append(" & ".join(celulas(i) + dir_) + r" \\")
        tex = (r"{\renewcommand{\arraystretch}{1.0}" + "\n"
               + _longtable(colspec, 2 * ncol, cab, "\n".join(linhas), titulo, rotulo,
                            r"\scriptsize" if pequeno else r"\footnotesize", "3.5pt") + "}\n")
        if paisagem:
            return r"\begin{landscape}" + "\n" + tex + rf"\vspace{{-6pt}}\fonte{{{fonte}}}" + "\n" + r"\end{landscape}" + "\n"
    else:
        largo = ncol > MAX_COLUNAS_RETRATO
        def cab_celula(c, al):
            txt = r"\textbf{" + esc(c) + "}"
            if al == "r" and len(str(c)) > 12:    # cabeçalho longo quebra numa caixa estreita, alinhada à direita
                larg = "1.8cm" if largo else "2.2cm"
                return rf"\parbox[b]{{{larg}}}{{\raggedleft\hyphenpenalty=10000\exhyphenpenalty=10000 {txt}}}"
            return txt
        cab = " & ".join(cab_celula(c, al) for c, al in zip(df.columns, specs)) + r" \\"
        corpo = "\n".join(" & ".join(celulas(i)) + r" \\" for i in range(n))
        tex = _longtable("@{}" + "".join(specs) + "@{}", ncol, cab, corpo, titulo, rotulo,
                         r"\scriptsize" if largo else r"\small", "3pt" if largo else "5pt")
        if largo:
            tex = r"\begin{landscape}" + "\n" + tex + rf"\vspace{{-6pt}}\fonte{{{fonte}}}" + "\n" + r"\end{landscape}" + "\n"
            return tex
    return tex + rf"\vspace{{-6pt}}\fonte{{{fonte}}}" + "\n"
