"""Dado pontual do programa Territórios Sociais (IPP) -- domicílios com inadequação habitacional e crianças até 72 meses
(specs/2026-10-08_deck_moradia). Só a variante variantes/moradia.md usa: dado pontual nunca vai para o relatório nem para
o site final (constituição §3), por isso não passa por tabelas_finais/.

Entrada: apresentacao/variantes/moradia/inadequacao_habitacional_criancas_0_a_5_anos_<data>.xlsx (recebida em
2026-10-07; a mais recente pelo nome), um domicílio por linha. Itens edilícios e de entorno: "Sim" = adequado,
"Não" = inadequado, "Não sabe / Não respondeu" fica fora da contagem do item. Condição (critérios do Eixo Urbano):
1 = só inadequação edilícia, 2 = só de infraestrutura no entorno (água, esgoto), 3 = as duas.
"""
from functools import lru_cache
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).resolve().parents[1] / "variantes" / "moradia"

ITENS_EDILICIOS = {"paredes": "Paredes", "piso": "Piso", "chuveiro": "Chuveiro", "vaso": "Vaso sanitário",
                   "pia": "Pia"}
ITENS_ENTORNO = {"agua": "Abastecimento de água", "esgoto": "Esgotamento sanitário"}
DEFICIENCIAS = {"deficiencia_visual": "Visual", "deficiencia_auditiva": "Auditiva",
                "deficiencia_fisica_motora": "Física / motora",
                "deficiencia_mental_intelectual": "Mental / intelectual", "espectro_autista": "Espectro autista",
                "outro_tipo_deficiencia": "Outro tipo"}
CONDICOES = {"Condição 1": "Só edilícia", "Condição 2": "Só entorno (água, esgoto)", "Condição 3": "Edilícia e entorno"}


def arquivo():
    return sorted(PASTA.glob("inadequacao_habitacional_criancas_0_a_5_anos_*.xlsx"))[-1]


@lru_cache(maxsize=1)
def dados():
    d = pd.read_excel(arquivo(), dtype=str)
    d.columns = ["domicilio", "condicao", *d.columns[2:]]
    d["total_criancas_0_a_5"] = pd.to_numeric(d["total_criancas_0_a_5"])
    d["com_deficiencia"] = (d[list(DEFICIENCIAS)] == "Sim").any(axis=1)
    return d


def por_condicao():
    """Domicílios e crianças por condição, na ordem 1-2-3."""
    d = dados()
    t = d.groupby("condicao").agg(domicilios=("domicilio", "size"), criancas=("total_criancas_0_a_5", "sum"),
                                  com_deficiencia=("com_deficiencia", "sum")).reindex(list(CONDICOES))
    t["rotulo"] = [f"{c} — {r}" for c, r in CONDICOES.items()]
    t["pct_domicilios"] = t["domicilios"] / len(d) * 100
    return t.reset_index()


def por_item():
    """Domicílios com cada item inadequado ("Não"), do maior para o menor; um domicílio pode ter vários."""
    d = dados()
    linhas = [(rot, "Entorno" if col in ITENS_ENTORNO else "Edilício", int((d[col] == "Não").sum()))
              for col, rot in {**ITENS_ENTORNO, **ITENS_EDILICIOS}.items()]
    t = pd.DataFrame(linhas, columns=["item", "grupo", "domicilios"]).sort_values("domicilios", ascending=False)
    t["pct_domicilios"] = t["domicilios"] / len(d) * 100
    return t.reset_index(drop=True)


def por_deficiencia():
    """Domicílios com registro de cada tipo de deficiência (não exclusivos), do maior para o menor."""
    d = dados()
    t = pd.DataFrame([(rot, int((d[col] == "Sim").sum())) for col, rot in DEFICIENCIAS.items()],
                     columns=["tipo", "domicilios"]).sort_values("domicilios", ascending=False)
    t["pct_com_deficiencia"] = t["domicilios"] / d["com_deficiencia"].sum() * 100
    return t.reset_index(drop=True)
