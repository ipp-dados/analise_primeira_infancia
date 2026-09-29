"""Gráficos só da apresentação (specs/2026-09-29_slide_revision B4): mesmo padrão de `mapas_apresentacao.py` -- desenho
da versão de impressão do analise.py (`primeira_infancia.impressao`, fontes e paleta), gravado em
apresentacao/_build/graficos/, sem tocar em visualizacoes/, no manifesto do relatório nem no site.
Uso no slide: ![](fig:<chave de GRAFICOS>).
"""
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
SAIDA = AQUI.parent / "_build" / "graficos"

GRAFICOS = {
    # D7: a soma dos vínculos em destaque; mãe, pai e outros como linhas secundárias. Taxa da soma = soma dos absolutos
    # ÷ população do mesmo ano (constituição §3), nunca soma das taxas
    "apres_violencia_familiar_total_ano": dict(
        tabela="violencia_familiar_taxa_municipio_ano.csv",
        fonte=("Sinan NET/Tabnet (SMS-Rio), notificações de residentes, até 72 meses (0 a 5 anos); população: estimativas "
               "Ripsa/Ministério da Saúde. Nota: a soma conta uma notificação mais de uma vez quando ela cita mais de um "
               "vínculo; a linha tracejada marca a possível quebra de série de 2017")),
}


def _violencia_familiar_total_ano(cfg, nome):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(RAIZ))
    import primeira_infancia.impressao as imp

    d = pd.read_csv(RAIZ / "tabelas_finais" / cfg["tabela"]).sort_values("ano")
    d["taxa_total"] = (d["mae"] + d["pai"] + d["outros"]) / d["populacao_0_a_5"] * 1000
    linhas = [("Soma dos vínculos", "taxa_total", imp._TINTA, 3.0),
              ("Mãe", "taxa_por_mil_mae", imp._PALETA_IMPRESSAO[1], 1.2),
              ("Pai", "taxa_por_mil_pai", imp._PALETA_IMPRESSAO[0], 1.2),
              ("Outros vínculos", "taxa_por_mil_outros", imp._PALETA_IMPRESSAO[2], 1.2)]
    rc = imp._rc_impressao()
    rc.update({"font.size": 11, "xtick.labelsize": 10.5, "ytick.labelsize": 10.5})
    with plt.rc_context(rc):
        fig, ax = plt.subplots(figsize=(20 * imp._CM, 11.5 * imp._CM))
        topo = d["taxa_total"].max() * 1.15
        ax.set_ylim(0, topo)                                               # base zero (P1)
        ax.axvline(2017, color=imp._TINTA3, lw=0.7, ls="--", zorder=0)
        ax.annotate("possível quebra\nde série (2017)", xy=(2017, topo), xytext=(4, -2), textcoords="offset points",
                    fontsize=9.5, color=imp._TINTA2, va="top")
        finais = []
        for rotulo, col, cor, lw in linhas:
            ax.plot(d["ano"], d[col], color=cor, lw=lw, zorder=4 if lw > 2 else 3)
            finais.append((rotulo, cor, float(d["ano"].iloc[-1]), float(d[col].iloc[-1]), lw > 2))
        ys = imp._espaca_rotulos([f[3] for f in finais], separacao=topo * 0.07)
        imp._eixo_x_anos_a4(ax, d["ano"], rotulo_extra=0.30)
        for (rotulo, cor, xf, yf, forte), yr in zip(finais, ys):
            ax.plot([xf], [yf], "o", ms=5 if forte else 3.8, color=cor, mec="white", mew=1.0, zorder=5)
            seta = dict(arrowstyle="-", color=imp._TINTA3, lw=0.4, shrinkA=0, shrinkB=2) if abs(yr - yf) > topo * .01 else None
            ax.annotate(f"{rotulo}  {imp._num_a4(yf, 1)}", xy=(xf, yf), xytext=(xf + 0.35, yr), textcoords="data",
                        ha="left", va="center", fontsize=11 if forte else 10, color=cor if not forte else imp._TINTA,
                        fontweight="semibold" if forte else "normal", annotation_clip=False, arrowprops=seta)
        ax.yaxis.set_major_formatter(imp._FuncFormatter(lambda v, _: imp._num_a4(v, 0)))
        imp._rotulo_y_a4(ax, "Notificações por 1.000 crianças de até 72 meses")
        SAIDA.mkdir(parents=True, exist_ok=True)
        fig.savefig(SAIDA / f"{nome}.pdf", bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)


_DESENHO = {"apres_violencia_familiar_total_ano": _violencia_familiar_total_ano}


def gera(nome):
    """Gera (se faltar ou estiver velho) o PDF do gráfico; devolve (caminho, fonte para o rodapé)."""
    cfg = GRAFICOS[nome]
    destino = SAIDA / f"{nome}.pdf"
    fresco = max((RAIZ / "tabelas_finais" / cfg["tabela"]).stat().st_mtime, Path(__file__).stat().st_mtime)
    if not destino.exists() or destino.stat().st_mtime < fresco:
        _DESENHO[nome](cfg, nome)
    return destino, cfg["fonte"]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for n in GRAFICOS:
        print(n, *gera(n))
