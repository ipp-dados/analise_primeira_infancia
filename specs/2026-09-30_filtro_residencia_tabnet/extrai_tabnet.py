"""Reextração dos exports por bairro do Tabnet da SMS-Rio (tabnet.rio.rj.gov.br) COM o filtro de município de
residência = Rio de Janeiro (specs/2026-09-30_filtro_residencia_tabnet).

Os arquivos originais foram exportados sem esse filtro: traziam óbitos/nascimentos de não residentes (linha
"EM BRANCO" e parte atribuída a bairros do Rio). Este script refaz cada consulta, grava no mesmo formato
(bairro nas linhas, ano nas colunas, "Total" no fim) e, com --conferir, reproduz a consulta SEM o filtro para
provar que é a mesma consulta dos arquivos originais.

Uso:  python specs/2026-09-30_filtro_residencia_tabnet/extrai_tabnet.py [--conferir] [--gravar]
"""
import argparse
import html
import re
import sys
from pathlib import Path

import pandas as pd
import requests

RAIZ = Path(__file__).resolve().parents[2]
BASE = "http://tabnet.rio.rj.gov.br/cgi-bin/tabnet?"
ANOS = list(range(2006, 2026))

SIM = dict(defn="sim/definicoes/sim_apos2005.def", coluna="Ano_do_Óbito", arq="do{:02d}.dbf",
           resid=("SMunic_Resid", "1"))
SINASC = dict(defn="sinasc/definicoes/sinasc_apos2005.def", coluna="Ano", arq="dn{:02d}.dbf",
              resid=("SMunic_Residencia", "1"), incremento="Nascimentos")
ANOS_RACA_MAE = list(range(2011, 2026))   # raça/cor da mãe só a partir de 2011 no SINASC-Rio
_RACA_MAE = "SRaça/Cor_Mae_(>2010)"

# arquivo -> (sistema, seleções além do município de residência, separador)
CONSULTAS = {
    "mortalidade/obitos_0_364_dias_bairro_2006_2025.csv": ("sim", [("SFaixa_Etária", "1")], ";"),
    "mortalidade/obitos_0_6_dias_bairro_2006_2025.csv": ("sim", [("SFx.Etár.Infantil", "1")], ";"),
    "mortalidade/obitos_7_27_dias_bairro_2006_2025.csv": ("sim", [("SFx.Etár.Infantil", "2")], ";"),
    "mortalidade/obitos_0_364_dias_brancos_bairro_2006_2025.csv": ("sim", [("SFaixa_Etária", "1"), ("SRaça/Cor", "1")], ";"),
    "mortalidade/obitos_0_364_dias_pretos_bairro_2006_2025.csv": ("sim", [("SFaixa_Etária", "1"), ("SRaça/Cor", "2")], ";"),
    "mortalidade/obitos_0_364_dias_amarelos_bairro_2006_2025.csv": ("sim", [("SFaixa_Etária", "1"), ("SRaça/Cor", "3")], ";"),
    "mortalidade/obitos_0_364_dias_pardos_bairro_2006_2025.csv": ("sim", [("SFaixa_Etária", "1"), ("SRaça/Cor", "4")], ";"),
    "mortalidade/obitos_0_364_dias_indigenas_bairro_2006_2025.csv": ("sim", [("SFaixa_Etária", "1"), ("SRaça/Cor", "5")], ";"),
    "mortalidade/obitos_0_364_dias_nao_informado_bairro_2006_2025.csv": ("sim", [("SFaixa_Etária", "1"), ("SRaça/Cor", "6"), ("SRaça/Cor", "7")], ";"),
    "mortalidade/obitos_gravidez_bairro_2006_2025.csv": ("sim", [("SÓbito/Gravidez_", "1")], ","),
    "mortalidade/obitos_puerperio_bairro_2006_2025.csv": ("sim", [("SÓbito/Puerpério_", "1")], ","),   # "Sim até 42 dias"
    "nascidos_vivos/nascidos_vivos_bairros_2006_a_2025.csv": ("sinasc", [], ","),
    "nascidos_vivos/nascidos_vivos_baixo_peso_ao_nascer_bairros_2006_a_2025.csv":
        ("sinasc", [("SPeso_Nascer_500g", str(i)) for i in range(1, 6)], ","),          # 0 a 2.499 g
    "mortalidade/nascidos_vivos_mae_branca_bairro_2011_2025.csv": ("sinasc", [(_RACA_MAE, "1")], ";"),
    "mortalidade/nascidos_vivos_mae_preta_bairro_2011_2025.csv": ("sinasc", [(_RACA_MAE, "2")], ";"),
    "mortalidade/nascidos_vivos_mae_amarela_bairro_2011_2025.csv": ("sinasc", [(_RACA_MAE, "3")], ";"),
    "mortalidade/nascidos_vivos_mae_parda_bairro_2011_2025.csv": ("sinasc", [(_RACA_MAE, "4")], ";"),
    "mortalidade/nascidos_vivos_mae_indigena_bairro_2011_2025.csv": ("sinasc", [(_RACA_MAE, "5")], ";"),
    "mortalidade/nascidos_vivos_mae_nao_informado_bairro_2011_2025.csv": ("sinasc", [(_RACA_MAE, "6")], ";"),
    "mortalidade/nascidos_vivos_mae_ignorado_bairro_2011_2025.csv": ("sinasc", [(_RACA_MAE, "7")], ";"),
}


def _post(defn, campos):
    corpo = "&".join(requests.utils.quote(k.encode("latin1")) + "=" + requests.utils.quote(v.encode("latin1"))
                     for k, v in campos)
    r = requests.post(BASE + defn, data=corpo, timeout=300,
                      headers={"Content-Type": "application/x-www-form-urlencoded"})
    r.raise_for_status()
    return r.content.decode("latin1")


def _tabela(texto):
    """Tabela do TabNet (HTML sem fechamento de TD/TR) -> DataFrame com a 1ª coluna 'rotulo'."""
    cab = re.search(r"<THEAD>(.*?)</THEAD>", texto, re.S | re.I).group(1)
    colunas = [html.unescape(re.sub("<[^>]+>", "", c)).strip() for c in re.split(r"<TH[^>]*>", cab, flags=re.I)[1:]]
    corpo = re.search(r"<TBODY[^>]*>(.*?)(?:</TBODY>|</TABLE>)", texto, re.S | re.I).group(1)
    linhas = []
    for tr in re.split(r"<TR[^>]*>", corpo, flags=re.I)[1:]:
        cel = [html.unescape(re.sub("<[^>]+>", "", c)).strip() for c in re.split(r"<TD[^>]*>", tr, flags=re.I)[1:]]
        if cel:
            linhas.append(cel)
    df = pd.DataFrame(linhas, columns=colunas[:len(linhas[0])])
    df = df.rename(columns={df.columns[0]: "rotulo"})
    for c in df.columns[1:]:
        df[c] = pd.to_numeric(df[c].replace("-", "0").str.replace(".", "", regex=False), errors="coerce").fillna(0).astype(int)
    return df


def consulta(sistema, selecoes, com_residencia=True, anos=ANOS):
    s = SIM if sistema == "sim" else SINASC
    campos = [("Linha", "Bairro_Residencia"), ("Coluna", s["coluna"]), ("Incremento", s.get("incremento", "OBITOS"))]
    campos += [("Arquivos", s["arq"].format(a % 100)) for a in anos]
    if com_residencia:
        campos.append(s["resid"])
    campos += selecoes + [("formato", "table"), ("mostre", "Mostra")]
    return _tabela(_post(s["defn"], campos))


def _anos(rel):
    return ANOS_RACA_MAE if "_2011_2025" in rel else ANOS


def para_formato_original(df, sep):
    """Ordem das linhas do Tabnet (bairros, sem-bairro, Total por último), colunas 2006..2025 + Total."""
    total = df[df["rotulo"] == "TOTAL"]
    corpo = df[df["rotulo"] != "TOTAL"]
    out = pd.concat([corpo, total.assign(rotulo="Total")])
    out = out.rename(columns={"rotulo": "Bairro Residencia"})
    return out


def compara(caminho, sep, novo):
    velho = pd.read_csv(caminho, sep=sep).set_index("Bairro Residencia")
    novo = novo.set_index("Bairro Residencia")
    anos = [c for c in velho.columns if c != "Total"]
    v = velho.loc["Total", anos].astype(int)
    n = novo.loc["Total", [c for c in anos if c in novo.columns]].astype(int)
    return (v - n).abs().sum(), v.to_dict(), n.to_dict()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--conferir", action="store_true", help="reproduz a consulta sem filtro e compara com o arquivo")
    ap.add_argument("--gravar", action="store_true", help="grava os arquivos com o filtro de residência")
    ap.add_argument("--so", nargs="*", help="só estes arquivos (trecho do nome)")
    a = ap.parse_args()
    for rel, (sist, sel, sep) in CONSULTAS.items():
        if a.so and not any(s in rel for s in a.so):
            continue
        caminho = RAIZ / "dados_locais" / rel
        if a.conferir:
            sem = para_formato_original(consulta(sist, sel, com_residencia=False, anos=_anos(rel)), sep)
            dif, v, n = compara(caminho, sep, sem)
            print(f"[sem filtro] {rel}: diferença absoluta total vs arquivo = {dif}  (2025: arquivo {v.get('2025')}, tabnet {n.get('2025')})")
        com = para_formato_original(consulta(sist, sel, com_residencia=True, anos=_anos(rel)), sep)
        tot = com.set_index("Bairro Residencia").loc["Total"]
        semb = [r for r in com["Bairro Residencia"] if not re.match(r"^\d{3} ", r) and r != "Total"]
        print(f"[residentes] {rel}: 2025 = {tot.get('2025')}, linhas sem código de bairro: {semb}")
        if a.gravar:
            com.to_csv(caminho, sep=sep, index=False, lineterminator="\n")
