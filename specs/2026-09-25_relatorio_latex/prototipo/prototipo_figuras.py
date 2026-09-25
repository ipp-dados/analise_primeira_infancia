"""Protótipo do tema de impressão (specs/2026-09-25_relatorio_latex, Bloco 5) -- NÃO é código do projeto.
Desenha 4 formas representativas no tamanho final do A4 (16 cm de largura útil), a partir de tabelas_finais/."""
import subprocess
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.ticker import FuncFormatter, MaxNLocator
import pandas as pd

RAIZ = Path(r"C:/Users/13073625755/Documents/GitHub/analise_primeira_infancia")
OUT = Path(__file__).parent
TF = RAIZ / "tabelas_finais"

for peso in ("Regular", "Medium", "SemiBold"):
    fm.fontManager.addfont(subprocess.check_output(["kpsewhich", f"IBMPlexSans-{peso}.otf"], text=True).strip())

CM = 1 / 2.54
LARGURA = 16 * CM
TINTA, TINTA2, TINTA3, GRADE = "#16202A", "#3F4B57", "#6B7580", "#DDE2E7"
PALETA = ["#3f76b8", "#dc7a45", "#0f7d5c", "#b88a1e", "#b8527b", "#5c9a3c", "#6f64ae", "#b84f4e"]
CINZA_CONTEXTO = "#C9CFD5"

plt.rcParams.update({
    "font.family": "IBM Plex Sans", "font.size": 8, "text.color": TINTA,
    "axes.labelcolor": TINTA2, "axes.labelsize": 8, "axes.edgecolor": TINTA3, "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRADE, "grid.linewidth": 0.5,
    "xtick.color": TINTA3, "ytick.color": TINTA3, "xtick.labelcolor": TINTA2, "ytick.labelcolor": TINTA2,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "ytick.left": False, "xtick.major.width": 0.6,
    "xtick.major.size": 2.5, "legend.frameon": False, "legend.fontsize": 7.5,
    "lines.linewidth": 1.6, "lines.solid_capstyle": "round",
    "pdf.fonttype": 42, "savefig.dpi": 300,
})


def num(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_eixo(dec=0):
    return FuncFormatter(lambda v, _: num(v, dec))


def rotulo_y(ax, texto):
    """Unidade do eixo na horizontal, acima do eixo -- lê-se sem girar a página."""
    ax.set_ylabel("")
    ax.annotate(texto, xy=(0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points",
                ha="left", va="bottom", fontsize=7.5, color=TINTA2)


def marca_ponto(ax, x, y, texto, cor, dx=4, dy=0, ha="left", va="center", peso="semibold"):
    ax.plot([x], [y], "o", ms=4.2, color=cor, mec="white", mew=1.0, zorder=5)
    ax.annotate(texto, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va,
                fontsize=7.5, color=TINTA, fontweight=peso)


def salva(fig, nome):
    fig.savefig(OUT / f"{nome}.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / f"{nome}.png", bbox_inches="tight", pad_inches=0.02, dpi=200)
    plt.close(fig)


# 1. Série única: taxa de mortalidade neonatal precoce ------------------------------------------
df = pd.read_csv(TF / "mortalidade_neonatal_precoce_por_ano.csv")
fig, ax = plt.subplots(figsize=(LARGURA, 6.2 * CM))
ax.plot(df.ano, df.taxa_mortalidade_precoce, color=PALETA[0])
ax.set_ylim(0, df.taxa_mortalidade_precoce.max() * 1.18)
ax.yaxis.set_major_formatter(fmt_eixo(0))
ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
ax.set_xlim(df.ano.min() - 0.5, df.ano.max() + 1.6)
rotulo_y(ax, "Óbitos de 0 a 6 dias por mil nascidos vivos")
i_max, i_min = df.taxa_mortalidade_precoce.idxmax(), df.taxa_mortalidade_precoce.idxmin()
for i, va, dy in [(0, "bottom", 5), (i_min, "top", -6)]:
    r = df.loc[i]
    marca_ponto(ax, r.ano, r.taxa_mortalidade_precoce, num(r.taxa_mortalidade_precoce, 1), PALETA[0], dx=0, dy=dy, ha="center", va=va, peso="normal")
u = df.iloc[-1]
marca_ponto(ax, u.ano, u.taxa_mortalidade_precoce, f"{num(u.taxa_mortalidade_precoce, 1)}\nem {int(u.ano)}", PALETA[0], dx=5)
salva(fig, "1_serie_unica")

# 2. Várias séries: notificações de violência familiar por vínculo, com marco ---------------------
df = pd.read_csv(TF / "violencia_familiar_por_vinculo_ano.csv")
df["outros vínculos"] = df[["padrasto", "irmao", "conjuge", "exconjuge", "filho", "outros"]].sum(axis=1)
series = [("mae", "Mãe", PALETA[0]), ("pai", "Pai", PALETA[1]), ("outros vínculos", "Outros vínculos", PALETA[2])]
fig, ax = plt.subplots(figsize=(LARGURA, 6.8 * CM))
for col, rot, cor in series:
    ax.plot(df.ano, df[col], color=cor, label=rot)
    u = df.iloc[-1]
    marca_ponto(ax, u.ano, u[col], f"{rot}  {num(u[col])}", cor, dx=5)
ax.axvline(2017, color=TINTA3, lw=0.6, zorder=0)
ax.annotate("2017: mudança na ficha de\nnotificação (possível quebra de série)", (2017, ax.get_ylim()[1] * 0.97),
            xytext=(4, 0), textcoords="offset points", fontsize=7, color=TINTA2, va="top")
ax.set_ylim(0, None)
ax.set_xlim(df.ano.min() - 0.5, df.ano.max() + 3.2)
ax.yaxis.set_major_formatter(fmt_eixo(0))
ax.xaxis.set_major_locator(plt.FixedLocator(range(2011, 2026, 2)))
rotulo_y(ax, "Notificações por ano, crianças de 0 a 5 anos")
ax.legend(loc="upper left", bbox_to_anchor=(0, -0.13), ncol=3, handlelength=1.6, columnspacing=1.6)
salva(fig, "2_series_multiplas")

# 3. Barras categóricas: CadÚnico por faixa de renda (horizontal, um só matiz, valor na ponta) ---------
df = pd.read_csv(TF / "cadunico_por_faixa_renda_2026.csv")
df = df[~df["faixa de renda"].astype(str).str.lower().str.startswith("total")]
df = df.iloc[::-1]
total = df["Crianças"].sum()
fig, ax = plt.subplots(figsize=(LARGURA, 5.2 * CM))
ax.barh(df["faixa de renda (descrição)"], df["Crianças"], color=PALETA[0], height=0.62)
ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True)
ax.xaxis.set_major_formatter(fmt_eixo(0)); ax.tick_params(axis="y", length=0)
ax.spines["bottom"].set_visible(False); ax.tick_params(axis="x", length=0)
for y, v in enumerate(df["Crianças"]):
    ax.annotate(f"{num(v)}  ({num(100 * v / total, 1)}%)", (v, y), xytext=(4, 0), textcoords="offset points",
                va="center", fontsize=7.5, color=TINTA, fontweight="semibold")
ax.set_xlim(0, df["Crianças"].max() * 1.28)
ax.set_xlabel("Crianças de 0 a 5 anos no CadÚnico (jun/2026)", loc="left")
salva(fig, "3_barras_categoricas")

# 4. Pequenos múltiplos: óbitos evitáveis < 1 ano por CAP (cada painel destaca uma CAP) -------------
df = pd.read_csv(TF / "mortalidade_evitaveis_cap_faixa_ano.csv")
df = df[df.faixa_etaria == "menores de 1 ano"].groupby(["cod_ap_sms", "ano"], as_index=False).obitos.sum()
caps = sorted(df.cod_ap_sms.unique())
fig, axs = plt.subplots(2, 5, figsize=(LARGURA, 8.4 * CM), sharex=True, sharey=True)
for ax, cap in zip(axs.flat, caps):
    for outra in caps:
        d = df[df.cod_ap_sms == outra]
        ax.plot(d.ano, d.obitos, color=CINZA_CONTEXTO, lw=0.7, zorder=1)
    d = df[df.cod_ap_sms == cap]
    ax.plot(d.ano, d.obitos, color=PALETA[4], lw=1.5, zorder=3)
    u = d.iloc[-1]
    ax.plot([u.ano], [u.obitos], "o", ms=3.4, color=PALETA[4], mec="white", mew=0.8, zorder=4)
    ax.annotate(num(u.obitos), (u.ano, u.obitos), xytext=(3.5, 0), textcoords="offset points", ha="left", va="center", fontsize=7, fontweight="semibold")
    ax.set_xlim(2005, 2031)
    ax.set_title(f"CAP {cap:.1f}".replace(".", "."), fontsize=8, fontweight="semibold", loc="left", color=TINTA, pad=3)
    ax.xaxis.set_major_locator(plt.FixedLocator([2006, 2015, 2025]))
    ax.tick_params(axis="x", labelsize=6.8)
    ax.set_ylim(0, df.obitos.max() * 1.15)
axs[0, 0].yaxis.set_major_formatter(fmt_eixo(0))
fig.text(0, 1.0, "Óbitos por causas evitáveis de menores de 1 ano, por CAP de residência  ·  em cinza, as demais CAP",
         fontsize=7.5, color=TINTA2, ha="left", va="bottom")
fig.tight_layout(h_pad=1.2, w_pad=0.6)
salva(fig, "4_pequenos_multiplos")
print("ok", sorted(p.name for p in OUT.glob("*.pdf")))
