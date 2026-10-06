"""Números dos destaques da apresentação (specs/2026-09-28_apresentacao, A3): calculados de tabelas_finais/ a cada
build, nunca digitados no .md. Uso no slide: {{n:chave}}. Chave inexistente = erro (o build para).

Cada função devolve o texto já formatado em pt-BR. Para acrescentar um número: uma função nova com @numero.
"""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
TF = RAIZ / "tabelas_finais"
sys.path.insert(0, str(RAIZ / "relatorio" / "curadoria"))

_NUMEROS = {}


def numero(f):
    _NUMEROS[f.__name__] = f
    return f


def _csv(nome):
    return pd.read_csv(TF / nome)


def fmt_int(v):
    return f"{int(round(v)):,}".replace(",", ".")


def fmt_dec(v, casas=1):
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(v, casas=1):
    return fmt_dec(v, casas) + "%"


def _ultimo(df, col="ano"):
    return df.sort_values(col).iloc[-1]


# ---------------------------------------------------------------- população
# specs/2026-09-29_pendencias D9/D17: a âncora é 0 a 5 anos (faixa padrão do projeto); 0 a 6 anos só na nota
# "a política fala em até 6 anos" (`pop_0_6_ripsa_mil`)
@numero
def pop_0_6_ripsa_mil():
    return fmt_int(_ultimo(_csv("populacao_ripsa_0_a_6_por_ano.csv"))["populacao_0_a_6"] / 1000) + " mil"


@numero
def pct_0_5_ripsa_2025():
    return fmt_pct(_ultimo(_csv("populacao_ripsa_0_a_6_por_ano.csv"))["percentual_0_a_5"])


def _ripsa_ano(ano):
    d = _csv("populacao_ripsa_0_a_6_por_ano.csv")
    return d[d["ano"] == ano].iloc[0]


@numero
def pop_0_5_ripsa_2000_mil():
    return fmt_int(_ripsa_ano(2000)["populacao_0_a_5"] / 1000) + " mil"


@numero
def pct_0_5_ripsa_2000():
    return fmt_pct(_ripsa_ano(2000)["percentual_0_a_5"])


@numero
def queda_0_5_ripsa_2000():
    """Queda da população de 0 a 5 anos entre 2000 e o último ano da série (mesma fonte, Ripsa)."""
    ult = _ultimo(_csv("populacao_ripsa_0_a_6_por_ano.csv"))
    return fmt_pct((1 - ult["populacao_0_a_5"] / _ripsa_ano(2000)["populacao_0_a_5"]) * 100, 0)


@numero
def pop_0_5_ripsa_mil():
    return fmt_int(_ultimo(_csv("populacao_ripsa_0_a_6_por_ano.csv"))["populacao_0_a_5"] / 1000) + " mil"


@numero
def pop_0_5_ripsa_2025():
    return fmt_int(_ultimo(_csv("populacao_ripsa_0_a_6_por_ano.csv"))["populacao_0_a_5"])


@numero
def ano_ripsa():
    return str(int(_ultimo(_csv("populacao_ripsa_0_a_6_por_ano.csv"))["ano"]))


def _censo(ano):
    d = _csv("censo_0_a_4_anos_por_ano.csv")
    return d[d["ano"] == ano].iloc[0]


@numero
def censo_0_4_2022():
    return fmt_int(_censo(2022)["0 a 4 anos"])


@numero
def censo_0_4_2000_mil():
    return fmt_int(_censo(2000)["0 a 4 anos"] / 1000) + " mil"


@numero
def censo_0_4_2022_mil():
    return fmt_int(_censo(2022)["0 a 4 anos"] / 1000) + " mil"


@numero
def queda_0_4_2000_2022():
    return fmt_pct((1 - _censo(2022)["0 a 4 anos"] / _censo(2000)["0 a 4 anos"]) * 100, 0)


@numero
def pct_0_4_2000():
    return fmt_pct(_censo(2000)["Percentual 0 a 4 anos"])


@numero
def pct_0_4_2022():
    return fmt_pct(_censo(2022)["Percentual 0 a 4 anos"])


@numero
def n_bairros():
    return str(len(_csv("censo_por_bairro.csv")))


def _top_bairros(n=3):
    return _csv("censo_por_bairro.csv").sort_values("0 a 4 anos", ascending=False).head(n)


@numero
def top3_bairros_0_4():
    return ", ".join(_top_bairros()["bairro"].tolist()[:2]) + " e " + _top_bairros()["bairro"].tolist()[2]


@numero
def top1_bairro_0_4_n():
    return fmt_int(_top_bairros(1)["0 a 4 anos"].iloc[0])


@numero
def censo_0_5_2022_mil():
    """Crianças de 0 a 5 anos (até 72 meses) no Censo 2022, SIDRA 9606, linha "Total 0 a 5 anos"."""
    d = _csv("censo_sidra_populacao_0_6_raca_2022.csv").set_index("idade").loc["Total 0 a 5 anos"]
    return fmt_int(d["Total"] / 1000) + " mil"


@numero
def pct_negras_0_5_censo():
    """Pardas + pretas na linha "Total 0 a 5 anos" (specs/2026-09-29_pendencias D9). Antes somava todas as linhas, inclusive
    o "Total" de todas as idades da tabela 9606 -- efeito mínimo (54,3% contra 54,4% corretos), mas errado."""
    d = _csv("censo_sidra_populacao_0_6_raca_2022.csv").set_index("idade").loc["Total 0 a 5 anos"]
    return fmt_pct((d["Parda"] + d["Preta"]) / d["Total"] * 100, 0)


# ---------------------------------------------------------------- nascimentos e mortalidade
@numero
def nascidos_2025():
    return fmt_int(_ultimo(_csv("nascidos_vivos_por_ano.csv"))["nascidos vivos"])


@numero
def nascidos_pico_ano():
    d = _csv("nascidos_vivos_por_ano.csv")
    return str(int(d.loc[d["nascidos vivos"].idxmax(), "ano"]))


@numero
def nascidos_pico():
    return fmt_int(_csv("nascidos_vivos_por_ano.csv")["nascidos vivos"].max())


@numero
def nascidos_sem_bairro_2025():
    d = _csv("mortalidade_infantil_pos_neonatal_total_por_ano.csv")
    n = _ultimo(_csv("nascidos_vivos_por_ano.csv"))["nascidos vivos"]
    return fmt_int(n - _ultimo(d)["nascidos_vivos"])


@numero
def tmi_2025():
    """Taxa de mortalidade infantil por mil nascidos vivos -- nascidos com bairro de residência informado (R1)."""
    return fmt_dec(_ultimo(_csv("mortalidade_infantil_pos_neonatal_total_por_ano.csv"))["taxa_mortalidade_infantil"])


@numero
def evitaveis_0_364_primeiro():
    return fmt_int(_csv("mortalidade_causas_evitaveis_grupo_ano.csv").sort_values("ano").iloc[0]["1. Causas evitáveis"])


@numero
def evitaveis_0_364_2025():
    return fmt_int(_ultimo(_csv("mortalidade_causas_evitaveis_grupo_ano.csv"))["1. Causas evitáveis"])


@numero
def evitaveis_0_364_primeiro_ano():
    return str(int(_csv("mortalidade_causas_evitaveis_grupo_ano.csv")["ano"].min()))


# menores de 1 ano: total e % da MESMA tabela do gráfico do slide (soma das faixas 0-6, 7-27 e 28-364 dias); os de
# menores de 5 anos vêm do extrato por CAP -- listas de evitáveis diferentes, por isso o slide não subtrai uma da outra
def _evitaveis_0_364_2025():
    d = _ultimo(_csv("mortalidade_causas_evitaveis_grupo_ano.csv"))
    return d["1. Causas evitáveis"], d.drop("ano").sum()


@numero
def obitos_0_364_2025():
    return fmt_int(_evitaveis_0_364_2025()[1])


@numero
def pct_evitaveis_0_364_2025():
    ev, total = _evitaveis_0_364_2025()
    return fmt_pct(ev / total * 100, 0)


@numero
def obitos_menores5_2025():
    d = _csv("mortalidade_evitaveis_cap_2025.csv")
    return fmt_int(d[d["faixa_etaria"] == "menores de 5 anos"]["total"].sum())


@numero
def evitaveis_menores5_2025():
    d = _csv("mortalidade_evitaveis_cap_2025.csv")
    return fmt_int(d[d["faixa_etaria"] == "menores de 5 anos"]["evitaveis"].sum())


@numero
def pct_evitaveis_menores5_2025():
    d = _csv("mortalidade_evitaveis_cap_2025.csv")
    d = d[d["faixa_etaria"] == "menores de 5 anos"]
    return fmt_pct(d["evitaveis"].sum() / d["total"].sum() * 100, 0)   # absolutos somados antes (constituição §3)


# ---------------------------------------------------------------- CadÚnico
def _razao_cad():
    return _csv("cadunico_razao_populacao_0_a_5_2026.csv").iloc[0]


@numero
def cadunico_criancas_0_5():
    return fmt_int(_razao_cad()["criancas_cadunico_0_a_5"])


@numero
def cadunico_familias():
    return fmt_int(_razao_cad()["familias_cadunico"])


@numero
def razao_cadunico():
    return fmt_pct(_razao_cad()["razao_percentual"])


# specs/2026-09-29_slide_revision D1: R$ 218 per capita é a linha de POBREZA (Bolsa Família, desde 2023), não de extrema
# pobreza. As faixas são lidas pela chave do CTPE (`0-218`), não pelo rótulo, que é texto de apresentação.
@numero
def pct_cadunico_pobreza():
    d = _csv("cadunico_por_faixa_renda_2026.csv")
    d = d[d["faixa de renda"] != "Total"]
    return fmt_pct(d.loc[d["faixa de renda"] == "0-218", "Crianças"].sum() / d["Crianças"].sum() * 100, 0)


# o gráfico do slide conta famílias; o destaque do texto, crianças -- a nota dá o número de famílias em pobreza
@numero
def familias_pobreza():
    d = _csv("cadunico_por_faixa_renda_2026.csv")
    return fmt_int(d.loc[d["faixa de renda"] == "0-218", "Famílias"].sum())


@numero
def pct_familias_pobreza():
    d = _csv("cadunico_por_faixa_renda_2026.csv")
    d = d[d["faixa de renda"] != "Total"]
    return fmt_pct(d.loc[d["faixa de renda"] == "0-218", "Famílias"].sum() / d["Famílias"].sum() * 100, 0)


def _arranjo(nome):
    d = _csv("cadunico_familias_por_arranjo_2026.csv").set_index("arranjo familiar")
    return d.loc[nome]


@numero
def pct_familias_uma_adulta():
    return fmt_pct(_arranjo("Uma adulta (mulher)")["% das famílias"])


@numero
def familias_uma_adulta():
    return fmt_int(_arranjo("Uma adulta (mulher)")["Famílias"])


@numero
def pct_familias_dois_adultos():
    return fmt_pct(_arranjo("Dois adultos (homem e mulher)")["% das famílias"])


@numero
def pct_uma_adulta_pobreza():
    """% das famílias de uma só adulta na faixa `0-218`. A tabela só grava o rótulo da faixa: o rótulo vem da chave,
    pelo mesmo dicionário que o analise.py usa para gravá-la (`_ROTULOS_RENDA_CADUNICO_3`)."""
    sys.path.insert(0, str(RAIZ))
    from primeira_infancia.cadunico import _ROTULOS_RENDA_CADUNICO_3
    rotulo = _ROTULOS_RENDA_CADUNICO_3["0-218"].replace("\n", " ")
    d = _csv("cadunico_familias_arranjo_renda_2026.csv")
    r = d[(d["arranjo"] == "Uma adulta (mulher)") & (d["faixa de renda per capita"] == rotulo)]
    return fmt_pct(r["% no arranjo"].iloc[0], 0)


# ---------------------------------------------------------------- educação
def _mat_serie():
    return _csv("matriculas_0_a_5_por_ano.csv").sort_values("ano")


@numero
def mat_publica_2025():
    return fmt_int(_mat()["matriculas_publica"])


@numero
def mat_privada_2025():
    return fmt_int(_mat()["matriculas_privada"])


@numero
def mat_publica_pico():
    return fmt_int(_mat_serie()["matriculas_publica"].max())


@numero
def mat_publica_pico_ano():
    d = _mat_serie()
    return str(int(d.loc[d["matriculas_publica"].idxmax(), "ano"]))


@numero
def queda_publica_desde_pico():
    d = _mat_serie()
    return fmt_pct((1 - _mat()["matriculas_publica"] / d["matriculas_publica"].max()) * 100, 0)


@numero
def mat_privada_2021():
    d = _mat_serie()
    return fmt_int(d[d["ano"] == 2021]["matriculas_privada"].iloc[0])


@numero
def pct_publica_2025():
    return fmt_pct(_mat()["matriculas_publica"] / _mat()["matriculas"] * 100, 0)

def _mat():
    return _ultimo(_csv("matriculas_0_a_5_por_ano.csv"))


@numero
def atend_0_5():
    return fmt_pct(_mat()["taxa_atendimento_0_a_5"])


@numero
def atend_creche():
    return fmt_pct(_mat()["taxa_atendimento_0_a_3"])


@numero
def atend_pre():
    return fmt_pct(_mat()["taxa_atendimento_4_a_5"])


@numero
def matriculas_0_5():
    return fmt_int(_mat()["matriculas"])


# ---------------------------------------------------------------- proteção, alimentação
@numero
def vf_notif_mae_2025():
    return fmt_int(_ultimo(_csv("violencia_familiar_taxa_municipio_ano.csv"))["mae"])


@numero
def vf_taxa_mae_2025():
    return fmt_dec(_ultimo(_csv("violencia_familiar_taxa_municipio_ano.csv"))["taxa_por_mil_mae"])


# specs/2026-09-29_slide_revision D7 revista (2026-09-29): os vínculos NÃO se somam -- a mesma notificação pode citar
# mais de um provável autor (specs/2026-09-23_inclusao_dados_protecao D6); cada vínculo com o seu número e a sua taxa.
def _vf_2025():
    return _ultimo(_csv("violencia_familiar_taxa_municipio_ano.csv"))


@numero
def vf_notif_pai_2025():
    return fmt_int(_vf_2025()["pai"])


@numero
def vf_notif_outros_2025():
    return fmt_int(_vf_2025()["outros"])


@numero
def vf_taxa_pai_2025():
    return fmt_dec(_vf_2025()["taxa_por_mil_pai"])


@numero
def vf_taxa_outros_2025():
    return fmt_dec(_vf_2025()["taxa_por_mil_outros"])


# pedido do usuário (2026-09-29): nos slides de Proteção, mãe e pai numa só linha -- a soma dos dois vínculos (uma
# notificação que cite os dois conta duas vezes; o Tabnet não deduplica). O slide diz isso na nota.
@numero
def vf_notif_mae_pai_2025():
    return fmt_int(_vf_2025()["mae"] + _vf_2025()["pai"])


@numero
def vf_taxa_mae_pai_2025():
    d = _vf_2025()
    return fmt_dec((d["mae"] + d["pai"]) / d["populacao_0_a_5"] * 1000)


@numero
def vf_ano():
    return str(int(_vf_2025()["ano"]))


@numero
def baixo_peso_pct_2025():
    return fmt_pct(_ultimo(_csv("nascidos_abaixo_peso_por_ano.csv"))["percentual abaixo do peso"])


@numero
def baixo_peso_n_2025():
    return fmt_int(_ultimo(_csv("nascidos_abaixo_peso_por_ano.csv"))["nascidos abaixo peso"])


@numero
def homicidios_max_ra():
    d = _csv("tabela_mapa_violencia_territorial_ra_2024.csv").dropna(subset=["taxa_homicidios"])
    r = d.loc[d["taxa_homicidios"].idxmax()]
    return f"{fmt_dec(r['taxa_homicidios'], 0)} ({r['regiao_adm'].title()})"


@numero
def homicidios_2a_ra():
    """Maior taxa entre as RAs depois da primeira (o Centro, outlier no mapa do slide)."""
    d = _csv("tabela_mapa_violencia_territorial_ra_2024.csv").dropna(subset=["taxa_homicidios"])
    r = d.sort_values("taxa_homicidios", ascending=False).iloc[1]
    return f"{r['regiao_adm'].title()} ({fmt_dec(r['taxa_homicidios'], 0)})"


@numero
def homicidios_min_ra():
    d = _csv("tabela_mapa_violencia_territorial_ra_2024.csv").dropna(subset=["taxa_homicidios"])
    r = d.loc[d["taxa_homicidios"].idxmin()]
    return f"{fmt_dec(r['taxa_homicidios'], 0)} ({r['regiao_adm'].title()})"


# ---------------------------------------------------------------- o projeto (estrutura_eixos.md)
def _estrutura():
    from gera_estrutura_eixos import _nomes_de_arquivo, eixos_politica, parse_estrutura_eixos
    e = parse_estrutura_eixos(str(RAIZ / "specs/estrutura_eixos.md"))
    return e, eixos_politica, _nomes_de_arquivo


@numero
def n_indicadores():
    e, _, _ = _estrutura()
    return str(sum(len(x["subsecoes"]) for x in e))


@numero
def n_pendentes():
    e, _, _ = _estrutura()
    return str(sum(1 for x in e for s in x["subsecoes"] if s["campos"].get("status") == "pendente"))


@numero
def n_eixos():
    e, eixos_politica, _ = _estrutura()
    return str(len(eixos_politica(e)))


def _conta(campo):
    e, _, nomes = _estrutura()
    return len({n for x in e for s in x["subsecoes"] if campo in s["campos"] for n in nomes(s["campos"][campo])})


@numero
def n_graficos():
    return str(_conta("visualização"))


@numero
def n_mapas():
    return str(_conta("mapa"))


@numero
def n_tabelas():
    return str(_conta("tabela"))


@numero
def n_fontes():
    import re
    return str(len(re.findall(r"^@\w+\{", (RAIZ / "relatorio/latex/fontes.bib").read_text(encoding="utf-8"), re.M)))


def pendentes_por_eixo():
    """[(eixo, pendentes, total)] -- slide da chamada às secretarias."""
    e, eixos_politica, _ = _estrutura()
    from gera_estrutura_eixos import titulo_eixo
    return [(titulo_eixo(x["eixo"]), sum(1 for s in x["subsecoes"] if s["campos"].get("status") == "pendente"),
             len(x["subsecoes"])) for x in eixos_politica(e)]


def valor(chave):
    if chave not in _NUMEROS:
        raise KeyError(f"número '{chave}' não existe em apresentacao/build/numeros.py")
    return _NUMEROS[chave]()


# ---------------------------------------------------------------- dados pontuais do CadÚnico (ref. 08/2026)
# specs/2026-09-29_dados_adhoc: extração pontual, faixas 0-3 e 4-6 (inclui os 6 anos, D1) -- sai com a substituição
# pela extração automatizada (ROADMAP)
def _deficiencia_adhoc():
    return _csv("cadunico_adhoc_deficiencia_2026_08.csv").set_index("Faixa etária")


def _moradia_adhoc(forma):
    d = pd.concat([_csv("cadunico_adhoc_moradia_domicilio_2026_08.csv").rename(columns={"Situação do domicílio": "Forma"}),
                   _csv("cadunico_adhoc_moradia_territorio_2026_08.csv")]).set_index("Forma")
    return d.loc[forma]


@numero
def adhoc_criancas_deficiencia_0_6():
    return fmt_int(_deficiencia_adhoc().loc["Total (0 a 6 anos)", "Crianças com deficiência"])


@numero
def adhoc_bpc_pct_0_3():
    return fmt_pct(_deficiencia_adhoc().loc["0 a 3 anos", "% com BPC"], 0)


@numero
def adhoc_bpc_pct_4_6():
    return fmt_pct(_deficiencia_adhoc().loc["4 a 6 anos", "% com BPC"], 0)


def _criancas_0_6(forma):
    r = _moradia_adhoc(forma)
    return fmt_int(r["Crianças de 0 a 3 anos"] + r["Crianças de 4 a 6 anos"])


@numero
def adhoc_criancas_sem_agua():
    return _criancas_0_6("Sem água canalizada")


@numero
def adhoc_criancas_sem_banheiro():
    return _criancas_0_6("Sem banheiro")


@numero
def adhoc_criancas_vala_ceu_aberto():
    return _criancas_0_6("Vala a céu aberto")


@numero
def adhoc_criancas_rio_mar():
    return _criancas_0_6("Jogado em rio ou mar")


@numero
def adhoc_criancas_fossa_rudimentar():
    return _criancas_0_6("Fossa rudimentar")


@numero
def adhoc_deficiencia_0_3():
    return fmt_int(_deficiencia_adhoc().loc["0 a 3 anos", "Crianças com deficiência"])


@numero
def adhoc_deficiencia_4_6():
    return fmt_int(_deficiencia_adhoc().loc["4 a 6 anos", "Crianças com deficiência"])


@numero
def adhoc_bpc_n_0_3():
    return fmt_int(_deficiencia_adhoc().loc["0 a 3 anos", "Com BPC"])


@numero
def adhoc_bpc_n_4_6():
    return fmt_int(_deficiencia_adhoc().loc["4 a 6 anos", "Com BPC"])


# ---------------------------------------------------------------- Inclusão (silver do CadÚnico, jul/2026)
# specs/2026-10-06_deck_inclusao: só a variante variantes/inclusao.md usa estas chaves; crianças até 72 meses
def _incl_criancas():
    return _csv("cadunico_deficiencia_criancas_0_a_5_2026.csv").set_index("Indicador")


def _incl_familias():
    return _csv("cadunico_deficiencia_familias_0_a_5_2026.csv").set_index("Indicador")


def _incl_tipos():
    return _csv("cadunico_tipos_deficiencia_0_a_5_2026.csv")


def _incl_bairros():
    """Bairros publicados sozinhos (fora dos conjuntos "Demais bairros…" da regra de privacidade)."""
    d = _csv("tabela_mapa_cadunico_deficiencia_bairro_2026.csv")
    return d[d["codbairro"].notna() & d["agregado_em"].isna()]


@numero
def incl_particao():
    """Mês da extração (partição da silver), por extenso: 'julho de 2026'."""
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
             "novembro", "dezembro"]
    d = pd.Timestamp(_csv("cadunico_razao_populacao_0_a_5_2026.csv")["data_particao"].iloc[0])
    return f"{meses[d.month - 1]} de {d.year}"


@numero
def incl_criancas_cadunico():
    return fmt_int(_incl_criancas().iloc[0]["Crianças"])


@numero
def incl_criancas_deficiencia():
    return fmt_int(_incl_criancas().loc["Crianças com deficiência", "Crianças"])


@numero
def incl_pct_criancas_deficiencia():
    return fmt_pct(_incl_criancas().loc["Crianças com deficiência", "%"])


@numero
def incl_familias_deficiencia():
    return fmt_int(_incl_familias().loc["Famílias com criança com deficiência", "Famílias"])


@numero
def incl_pct_familias_deficiencia():
    return fmt_pct(_incl_familias().loc["Famílias com criança com deficiência", "%"])


@numero
def incl_bpc_familias():
    return fmt_int(_incl_familias().loc["Delas, recebem BPC por deficiência", "Famílias"])


@numero
def incl_bpc_base():
    return fmt_int(_incl_familias().loc["Delas, recebem BPC por deficiência", "Base"])


@numero
def incl_pct_bpc():
    return fmt_pct(_incl_familias().loc["Delas, recebem BPC por deficiência", "%"])


@numero
def incl_bpc_sem_info():
    return fmt_int(_incl_familias().loc["Delas, sem informação de BPC", "Famílias"])


@numero
def incl_sem_bpc():
    f = _incl_familias()
    return fmt_int(f.loc["Delas, recebem BPC por deficiência", "Base"] - f.loc["Delas, recebem BPC por deficiência", "Famílias"])


def _incl_tipo(i, campo):
    t = _incl_tipos().iloc[i]
    return {"nome": t["Tipo de deficiência"].lower(), "n": fmt_int(t["Crianças"]),
            "pct": fmt_pct(t["% das crianças com deficiência"], 0)}[campo]


@numero
def incl_tipo1_nome():
    return _incl_tipo(0, "nome")


@numero
def incl_tipo1_pct():
    return _incl_tipo(0, "pct")


@numero
def incl_tipo2_nome():
    return _incl_tipo(1, "nome")


@numero
def incl_tipo2_pct():
    return _incl_tipo(1, "pct")


@numero
def incl_tipo3_nome():
    return _incl_tipo(2, "nome")


@numero
def incl_tipo3_pct():
    return _incl_tipo(2, "pct")


@numero
def incl_mediana_bairros():
    return fmt_pct(_incl_bairros()["% crianças com deficiência"].median())


@numero
def incl_bairro_min():
    b = _incl_bairros().sort_values("% crianças com deficiência").iloc[0]
    return f'{b["bairro"]} ({fmt_pct(b["% crianças com deficiência"])})'


@numero
def incl_bairro_max():
    b = _incl_bairros().sort_values("% crianças com deficiência").iloc[-1]
    return f'{b["bairro"]} ({fmt_pct(b["% crianças com deficiência"])})'


@numero
def incl_n_bairros_sozinhos():
    return fmt_int(len(_incl_bairros()))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for k in _NUMEROS:
        print(f"{k:32s} {valor(k)}")
    print(pendentes_por_eixo())
