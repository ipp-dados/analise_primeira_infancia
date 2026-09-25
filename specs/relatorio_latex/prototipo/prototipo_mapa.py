"""Protótipo do mapa de impressão (specs/relatorio_latex, Bloco 5) -- NÃO é código do projeto.
Reaproveita as funções/constantes do topo de analise.py (só defs/imports/constantes, sem rodar análise)."""
import ast, os, subprocess
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

RAIZ = Path(r"C:/Users/13073625755/Documents/GitHub/analise_primeira_infancia")
OUT = Path(__file__).parent
os.chdir(RAIZ)
src = (RAIZ / "analise.py").read_text(encoding="utf-8")
arv = ast.parse(src)
ns = {}
for n in arv.body:
    if n.lineno >= 1300:
        break
    if isinstance(n, (ast.FunctionDef, ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
        exec(compile(ast.Module([n], []), "analise.py", "exec"), ns)
globals().update({k: v for k, v in ns.items() if not k.startswith("__")})

import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.colors import Normalize
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
for peso in ("Regular", "Medium", "SemiBold"):
    fm.fontManager.addfont(subprocess.check_output(["kpsewhich", f"IBMPlexSans-{peso}.otf"], text=True).strip())
plt.rcParams.update({"font.family": "IBM Plex Sans", "pdf.fonttype": 42})

CM = 1 / 2.54
TINTA, TINTA2 = "#16202A", "#3F4B57"


def mapa_impressao(df, coluna_valor, nome, chave, bins=None, cmap="RdPu", legenda_titulo="", teto_pct=None,
                   largura_cm=16.0):
    info = _NIVEIS_AGREGACAO["bairro"]
    col, tipo = info["coluna_geo"], info["tipo"]
    gdf = gpd.read_file("dados_locais/geo/limite_bairros_rio.geojson")
    gdf[col] = gdf[col].astype(tipo)
    df = df.copy(); df[chave] = df[chave].astype(tipo)
    gdf = gdf.merge(df[[chave, coluna_valor]], left_on=col, right_on=chave, how="left").to_crs(epsg=3857)
    corr = math.cos(math.radians(-22.9))
    minx, miny, maxx, maxy = gdf.total_bounds
    padx, pady = (maxx - minx) * 0.02, (maxy - miny) * 0.06     # menos margem de contexto que a versão de tela
    aspecto = (maxx - minx + 2 * padx) / (maxy - miny + 2 * pady)
    fig, ax = plt.subplots(figsize=(largura_cm * CM, largura_cm * CM / aspecto))
    fig.subplots_adjust(0, 0, 1, 1)
    miss = {"color": "none", "edgecolor": "#8a8a8a", "hatch": "////", "linewidth": 0.3}
    borda = dict(linewidth=0.25, edgecolor="#5f5f5f")
    if bins:
        lim = [min(gdf[coluna_valor].min(), bins[0]) - 1] + list(bins) + [max(gdf[coluna_valor].max(), bins[-1])]
        rot = [f"Até {_numero_ptbr(bins[0])}"] + [f"{_numero_ptbr(bins[i-1]+1)} a {_numero_ptbr(bins[i])}" for i in range(1, len(bins))] + [f"Mais de {_numero_ptbr(bins[-1])}"]
        gdf["faixa"] = pd.cut(gdf[coluna_valor], bins=lim, labels=rot, ordered=True)
        cores = plt.get_cmap(cmap)(np.linspace(0.12, 0.92, len(rot)))
        for i, r in enumerate(rot):
            gdf[gdf.faixa == r].plot(ax=ax, color=cores[i], zorder=2, **borda)
        gdf[gdf[coluna_valor].isna()].plot(ax=ax, zorder=2, **miss)
        handles = [Patch(facecolor=cores[i], edgecolor="#5f5f5f", linewidth=0.3) for i in range(len(rot))]
        labels = list(rot)
        if gdf[coluna_valor].isna().any():
            handles.append(Patch(facecolor="white", edgecolor="#8a8a8a", hatch="////", linewidth=0.3)); labels.append("Sem dado")
        leg = ax.legend(handles, labels, title=legenda_titulo, loc="upper left", bbox_to_anchor=(0.012, 0.985),
                        fontsize=7, title_fontsize=7.5, frameon=True, framealpha=0.94, edgecolor="none",
                        handlelength=1.4, handleheight=0.9, borderpad=0.6, labelspacing=0.35, alignment="left")
        leg.get_title().set_fontweight("semibold")
    else:
        vmax = gdf[coluna_valor].quantile(teto_pct) if teto_pct else gdf[coluna_valor].max()
        norm = Normalize(0, vmax)
        gdf.plot(column=coluna_valor, ax=ax, cmap=cmap, norm=norm, zorder=2, missing_kwds=miss, **borda)
        cax = ax.inset_axes([0.03, 0.56, 0.022, 0.36])
        sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        cb = fig.colorbar(sm, cax=cax, extend="max" if teto_pct else "neither", extendfrac=0.06)
        cb.outline.set_linewidth(0.3)
        cax.tick_params(labelsize=7, length=2, width=0.4, colors=TINTA)
        halo = [pe.withStroke(linewidth=2.2, foreground="white")]
        ticks = cb.get_ticks()
        cb.set_ticks([t for t in ticks if t <= vmax])
        labs = [_numero_ptbr(t) for t in cb.get_ticks()]
        if teto_pct:
            labs[-1] = f"{labs[-1]}"
            cax.annotate(f"≥ {_numero_ptbr(vmax)}", xy=(1, 1.07), xycoords="axes fraction", xytext=(3, 0),
                         textcoords="offset points", fontsize=7, va="center", color=TINTA, path_effects=halo)
        cb.set_ticklabels(labs)
        for t in cax.get_yticklabels():
            t.set_path_effects(halo)
        cax.annotate(legenda_titulo, xy=(0, 1.16), xycoords="axes fraction", fontsize=7.5, fontweight="semibold",
                     va="bottom", ha="left", color=TINTA, path_effects=halo)
        gdf[gdf[coluna_valor].isna()].plot(ax=ax, zorder=2, **miss)

    ax.set_xlim(minx - padx, maxx + padx); ax.set_ylim(miny - pady, maxy + pady)
    gpd.read_file("dados_locais/geo/limite_uf_brasil.geojson").to_crs(epsg=3857).boundary.plot(
        ax=ax, color="#d4b106", linewidth=0.7, linestyle=(0, (3, 2)), zorder=1)
    ax.set_xlim(minx - padx, maxx + padx); ax.set_ylim(miny - pady, maxy + pady)
    ctx.add_basemap(ax, source=_PROVEDORES_FUNDO["mapa_oceano_base"], zorder=0, attribution=False)
    # véu branco sobre o fundo: menos tinta no papel e mais contraste para o dado
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color="white", alpha=0.38, zorder=0.5, lw=0))
    ax.annotate("N", xy=(0.965, 0.93), xytext=(0.965, 0.86), xycoords=ax.transAxes, textcoords=ax.transAxes,
                ha="center", va="center", fontsize=8, fontweight="semibold", color=TINTA,
                arrowprops=dict(arrowstyle="-|>", color=TINTA, lw=1.0, mutation_scale=10), zorder=5)
    ax.add_artist(ScaleBar(corr, units="m", location="lower right", box_alpha=0, color=TINTA, scale_loc="top",
                           border_pad=0.5, width_fraction=0.006, length_fraction=0.16, font_properties={"size": 6.5}))
    _adiciona_rotulos_municipios_vizinhos(ax, ax.get_xlim(), ax.get_ylim(), cor="#5a6570", tamanho=6.5)
    for t in ax.texts:
        if t.get_text() not in ("N",):
            t.set_path_effects([pe.withStroke(linewidth=1.8, foreground="white")])
    ax.annotate("Fundo: Esri, GEBCO, NOAA, National Geographic, DeLorme, NAVTEQ", xy=(0.006, 0.006), xycoords="axes fraction",
                fontsize=4.8, color="#6b7580", va="bottom")
    ax.axis("off")
    fig.savefig(OUT / f"{nome}.pdf", dpi=300)
    fig.savefig(OUT / f"{nome}.png", dpi=220)
    plt.close(fig)


df = pd.read_csv("tabelas_finais/tabela_mapa_obitos_neonatal_precoce_2025.csv", dtype={"codigo": str})
df["codigo"] = df["codigo"].astype(int)
mapa_impressao(df, "obitos precoces", "5_mapa_classes", "codigo", bins=[1, 3, 6, 12], cmap="RdPu", legenda_titulo="Óbitos de 0 a 6 dias")
mapa_impressao(df, "taxa_mortalidade_precoce", "6_mapa_taxa", "codigo", cmap="RdPu",
               legenda_titulo="Óbitos por mil nascidos vivos", teto_pct=0.95)
print("ok")
