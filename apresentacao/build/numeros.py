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


@numero
def pct_cadunico_extrema_pobreza():
    d = _csv("cadunico_por_faixa_renda_2026.csv")
    d = d[d["faixa de renda"] != "Total"]
    return fmt_pct(d.iloc[0]["Crianças"] / d["Crianças"].sum() * 100, 0)


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
def pct_uma_adulta_extrema_pobreza():
    d = _csv("cadunico_familias_arranjo_renda_2026.csv")
    r = d[(d["arranjo"] == "Uma adulta (mulher)") & (d["faixa de renda per capita"].str.startswith("Extrema"))]
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


@numero
def baixo_peso_pct_2025():
    return fmt_pct(_ultimo(_csv("nascidos_abaixo_peso_por_ano.csv"))["percentual abaixo do peso"])


@numero
def baixo_peso_n_2025():
    return fmt_int(_ultimo(_csv("nascidos_abaixo_peso_por_ano.csv"))["nascidos abaixo peso"])


@numero
def ips_homicidios_max_ra():
    d = _csv("tabela_mapa_violencia_territorial_ra_2024.csv").dropna(subset=["taxa_homicidios"])
    r = d.loc[d["taxa_homicidios"].idxmax()]
    return f"{fmt_dec(r['taxa_homicidios'], 0)} ({r['regiao_adm'].title()})"


@numero
def ips_homicidios_2a_ra():
    """Maior taxa entre as RAs depois da primeira (o Centro, outlier no mapa do slide)."""
    d = _csv("tabela_mapa_violencia_territorial_ra_2024.csv").dropna(subset=["taxa_homicidios"])
    r = d.sort_values("taxa_homicidios", ascending=False).iloc[1]
    return f"{r['regiao_adm'].title()} ({fmt_dec(r['taxa_homicidios'], 0)})"


@numero
def ips_homicidios_min_ra():
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


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for k in _NUMEROS:
        print(f"{k:32s} {valor(k)}")
    print(pendentes_por_eixo())
