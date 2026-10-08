"""Mapas só da apresentação (specs/2026-09-28_apresentacao; specs/2026-09-29_slide_revision B3): o mesmo desenho da
versão de impressão do analise.py (`_a4_mapa`), com as escolhas pedidas para o slide. Gravados em apresentacao/_build/
mapas/ -- não tocam em mapas/, no manifesto do relatório nem no site.

Parâmetros de cada entrada de MAPAS (os opcionais têm padrão):
  tabela, coluna, chave, nivel, titulo, legenda, fonte   obrigatórios
  tema | cmap        cor do tema do projeto (`_CORES_TEMA_MAPA`) ou um cmap próprio ("terracota" = TERRACOTA, abaixo)
  bins              contagens: classes discretas (convenção do projeto); sem bins = escala contínua (taxas e %)
  outlier           escala contínua com teto de Tukey (padrão True); False = escala até o máximo
  zero_branco       zero em branco nas classes discretas ("0 (sem casos)")
  rotulo            coluna com o nome da região para a nota dos outliers (nível bairro: o nome vem do geojson)
  prepara           função df -> df aplicada à tabela antes do mapa (coluna derivada só do deck)
  outliers_fixos    nome da lista de códigos em primeira_infancia.cadunico tratados como valor atípico (no lugar de Tukey)
  piso              início da escala contínua (padrão 0), quando todos os valores estão numa faixa alta

GRAFICOS: séries só da apresentação, no desenho de impressão do analise.py (`_a4_series`); mesma chave `fig:<nome>`.
Com `desenha=f`, a figura é desenhada por f(df, impressao, nome, cfg) no mesmo estilo (`_rc_impressao`).

Regra de outlier: a mesma do site (cercas de Tukey, 1,5 x IQR, `remove_outliers_tukey` em website/build/build_site.py).
A escala de cor vai até o maior valor que NÃO é outlier; as regiões acima ficam com a cor máxima e são nomeadas na nota
do rodapé (R7). Uso no slide: ![](fig:<chave de MAPAS>).
"""
import sys
from pathlib import Path

import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
SAIDA = AQUI.parent / "_build" / "mapas"

# D6: terra nunca em azul no deck. Rampa creme -> terracota, só da apresentação (distinta de BuGn/RdPu/YlOrBr/Blues do
# analise.py e do Purples do site); substitui o `Blues` do tema censo nos mapas de população.
TERRACOTA = LinearSegmentedColormap.from_list("terracota", ["#fbf6ef", "#f1dcc4", "#e3b48f", "#cf8a63", "#a4452c"])
_CMAPS = {"terracota": TERRACOTA}

_FONTE_SINAN = "Sinan NET/Tabnet (SMS-Rio), 0 a 5 anos"


def _vf_mae_pai_bairro_2025(df):
    """Pedido do usuário (2026-09-29): mãe e pai numa só contagem. É a SOMA dos dois vínculos -- a notificação que cita
    os dois conta duas vezes (o Tabnet não permite deduplicar); a nota do slide diz isso."""
    d = df[df["ano"] == 2025].copy()
    d["mae_pai"] = d["mae"] + d["pai"]
    return d


def _vf_mae_pai_municipio(df):
    d = df.copy()
    d["taxa_por_mil_mae_pai"] = (d["mae"] + d["pai"]) / d["populacao_0_a_5"] * 1000
    return d


def _so_bairros_sozinhos(df):
    """Mapas de número: só os bairros publicados sozinhos -- os somados por RA ("Demais bairros…") ficam sem cor."""
    return df[df["codbairro"].notna() & df["agregado_em"].isna()].copy()


_FONTE_CADUNICO_RECORTES = "CadÚnico (extração CTPE); bairro pelo CEP da família"
_FONTE_CADUNICO_SILVER = "CadÚnico (extração CTPE, jul/2026); bairro pelo CEP da família"
_FONTE_CENSO ="IBGE, Censo Demográfico 2022 (Data.Rio), por bairro"
_FONTE_DATASUS = "DATASUS/Tabnet, óbitos e nascimentos de residentes no município do Rio de Janeiro, por bairro (2025)"
MAPAS = {
    # pedido do usuário (2026-09-28): no slide "O território onde a criança brinca" o Centro enviesava a escala
    # slide_revision D12 (2026-09-29): sem menção ao IPS no deck -- legenda e fonte citam só o Data.Rio
    "apres_violencia_territorial_homicidios_ra_2024": dict(
        tabela="tabela_mapa_violencia_territorial_ra_2024.csv", coluna="taxa_homicidios", chave="codra", nivel="ra",
        titulo="Taxa de homicídios por RA (2024) — população geral", tema="protecao",
        legenda="Por 100 mil hab.\ntodas as idades,\nnão só crianças", rotulo="regiao_adm",
        fonte="Data.Rio, 2024, por Região Administrativa (todas as idades)"),
    # specs/2026-10-06_deck_alimentacao_brincar: só a variante variantes/direito_brincar.md; mesmo desenho do mapa acima
    # (teto de Tukey, fonte sem o IPS)
    "apres_violencia_territorial_acao_policial_ra_2024": dict(
        tabela="tabela_mapa_violencia_territorial_ra_2024.csv", coluna="homicidios_acao_policial", chave="codra",
        nivel="ra", titulo="Homicídios por ação policial por RA (2024) — população geral", tema="protecao",
        legenda="Taxa (Data.Rio)\ntodas as idades,\nnão só crianças", rotulo="regiao_adm",
        fonte="Data.Rio, 2024, por Região Administrativa (todas as idades)"),
    "apres_violencia_territorial_jovens_negros_ra_2024": dict(
        tabela="tabela_mapa_violencia_territorial_ra_2024.csv", coluna="homicidios_jovens_negros", chave="codra",
        nivel="ra", titulo="Homicídios de jovens negros por RA (2024)", tema="protecao",
        legenda="Taxa (Data.Rio)\nnão é dado\nde crianças", rotulo="regiao_adm",
        fonte="Data.Rio, 2024, por Região Administrativa"),
    # slide_revision R3/D6: os mapas do Censo em terracota (o tema censo do projeto é Blues)
    "apres_censo_0_4_absoluto": dict(
        tabela="censo_por_bairro.csv", coluna="0 a 4 anos", chave="codbairro", nivel="bairro",
        titulo="Crianças de 0 a 4 anos por bairro (Censo 2022)", cmap="terracota", bins=[1000, 2500, 5000, 10000],
        legenda="Crianças 0-4 anos", fonte=_FONTE_CENSO),
    "apres_censo_0_4_percentual": dict(
        tabela="censo_por_bairro.csv", coluna="Percentual 0 a 4", chave="codbairro", nivel="bairro",
        titulo="Percentual de crianças de 0 a 4 anos por bairro (Censo 2022)", cmap="terracota",
        legenda="% da população\ndo bairro", fonte=_FONTE_CENSO),
    # slide_revision D8: mortalidade infantil e baixo peso com teto de Tukey (antes: percentil 95 da versão A4)
    "apres_taxa_mortalidade_infantil_bairro_2025": dict(
        tabela="tabela_mapa_obitos_raca_total_2025.csv", coluna="taxa_mortalidade_infantil_total", chave="codigo",
        nivel="bairro", titulo="Taxa de mortalidade infantil por bairro (2025)", tema="mortalidade",
        legenda="Óbitos por mil\nnascidos vivos", fonte=_FONTE_DATASUS),
    "apres_baixo_peso_bairro_2025": dict(
        tabela="tabela_mapa_nascidos_baixo_peso_2025.csv", coluna="percentual abaixo do peso", chave="codigo",
        nivel="bairro", titulo="% de nascidos com baixo peso por bairro (2025)", tema="natalidade",
        legenda="% baixo peso", fonte=_FONTE_DATASUS.replace("óbitos e nascimentos", "nascimentos")),
    # pedido do usuário (2026-09-29): um mapa só, mãe + pai somados (no lugar dos dois mapas por vínculo)
    "apres_violencia_familiar_mae_pai_bairro_2025": dict(
        tabela="violencia_familiar_por_bairro.csv", prepara=_vf_mae_pai_bairro_2025, coluna="mae_pai",
        chave="codbairro", nivel="bairro", titulo="Notificações de violência familiar por bairro — mãe ou pai (2025)",
        tema="protecao", bins=[10, 30, 60, 120], zero_branco=True, legenda="Notificações\n(mãe + pai)",
        fonte=_FONTE_SINAN + ", por bairro de residência (2025); soma dos vínculos mãe e pai"),
    # specs/2026-10-06_deck_inclusao: só a variante variantes/inclusao.md; tira as linhas de conjunto ("Demais bairros…",
    # sem codbairro) -- os bairros somados já trazem a taxa do conjunto
    # contagem (classes discretas, convenção do projeto); bairros somados por RA ficam sem cor -- o total do conjunto
    # está na tabela e na nota do slide
    "apres_cadunico_deficiencia_n_bairro": dict(
        tabela="tabela_mapa_cadunico_deficiencia_bairro_2026.csv", prepara=lambda d: d[d["codbairro"].notna()].copy(),
        coluna="Crianças com deficiência", chave="codbairro", nivel="bairro",
        titulo="Crianças até 72 meses com deficiência no CadÚnico, por bairro (número)", tema="cadunico",
        bins=[30, 50, 100, 200], legenda="Crianças com\ndeficiência",
        fonte="CadÚnico (extração CTPE, jul/2026); bairro pelo CEP da família; bairros com menos de 20 casos somados aos "
              "da mesma Região Administrativa ficam sem cor"),
    "apres_cadunico_deficiencia_bairro": dict(
        tabela="tabela_mapa_cadunico_deficiencia_bairro_2026.csv", prepara=lambda d: d[d["codbairro"].notna()].copy(),
        coluna="% crianças com deficiência", chave="codbairro", nivel="bairro",
        titulo="% de crianças até 72 meses com deficiência no CadÚnico, por bairro", tema="cadunico",
        legenda="% com deficiência",
        fonte="CadÚnico (extração CTPE, jul/2026); bairro pelo CEP da família; bairros com menos de 20 casos somados aos "
              "da mesma Região Administrativa"),
    # specs/2026-10-07_deck_familia_moradia: só as variantes variantes/familia_cuidados.md e variantes/moradia.md.
    # Mesmo padrão da de Inclusão: número (classes discretas; bairros somados por RA sem cor) antes do percentual
    "apres_cadunico_uma_adulta_n_bairro": dict(
        tabela="tabela_mapa_cadunico_recortes_bairro_2026.csv", prepara=_so_bairros_sozinhos,
        coluna="Famílias com uma adulta", chave="codbairro", nivel="bairro",
        titulo="Famílias com crianças até 72 meses no CadÚnico com uma só adulta, por bairro (número)",
        tema="cadunico", bins=[250, 500, 1000, 2500], legenda="Famílias com\numa só adulta",
        fonte=_FONTE_CADUNICO_RECORTES + "; bairros com menos de 20 casos somados aos da mesma Região Administrativa "
              "ficam sem cor"),
    "apres_cadunico_uma_adulta_bairro": dict(
        tabela="tabela_mapa_cadunico_recortes_bairro_2026.csv", prepara=lambda d: d[d["codbairro"].notna()].copy(),
        coluna="% famílias com uma adulta", chave="codbairro", nivel="bairro",
        titulo="% das famílias com crianças até 72 meses no CadÚnico com uma só adulta, por bairro", tema="cadunico",
        legenda="% uma só adulta\n(escala a partir de 60%)", piso=60,
        fonte=_FONTE_CADUNICO_RECORTES + "; bairros com menos de 20 casos mostram o percentual do conjunto dos bairros "
              "pequenos da sua Região Administrativa; escala de cor a partir de 60% (todos os bairros entre 60% e 90%)"),
    "apres_cadunico_inadequacao_n_bairro": dict(
        tabela="tabela_mapa_cadunico_inadequacao_bairro_2026.csv", prepara=_so_bairros_sozinhos,
        coluna="Crianças em inadequação habitacional", chave="codbairro", nivel="bairro",
        titulo="Crianças até 72 meses no CadÚnico em domicílio com inadequação habitacional, por bairro (número)",
        tema="cadunico", bins=[25, 50, 100, 250], legenda="Crianças em\ninadequação",
        fonte=_FONTE_CADUNICO_SILVER + "; bairros com menos de 20 casos somados aos da mesma Região Administrativa "
              "ficam sem cor"),
    # outlier fixo (decisão do usuário, 2026-10-06, a mesma do analise.py e do site): só o Alto da Boa Vista sai da escala
    "apres_cadunico_inadequacao_bairro": dict(
        tabela="tabela_mapa_cadunico_inadequacao_bairro_2026.csv", prepara=lambda d: d[d["codbairro"].notna()].copy(),
        coluna="% crianças em inadequação habitacional", chave="codbairro", nivel="bairro",
        titulo="% de crianças até 72 meses no CadÚnico em domicílio com inadequação habitacional, por bairro",
        tema="cadunico", legenda="% inadequação", outliers_fixos="_OUTLIERS_INADEQUACAO_CADUNICO",
        fonte=_FONTE_CADUNICO_SILVER + "; metodologia da Fundação João Pinheiro; bairros com menos de 20 casos mostram "
              "o percentual do conjunto da sua Região Administrativa"),
    "apres_cadunico_adensamento_bairro": dict(
        tabela="tabela_mapa_cadunico_adensamento_bairro_2026.csv", prepara=lambda d: d[d["codbairro"].notna()].copy(),
        coluna="% crianças em adensamento excessivo", chave="codbairro", nivel="bairro",
        titulo="% de crianças até 72 meses no CadÚnico em domicílio com mais de 2 pessoas por dormitório, por bairro",
        tema="cadunico", legenda="% adensamento",
        fonte=_FONTE_CADUNICO_SILVER + "; mais de 2 pessoas por dormitório; bairros com menos de 20 casos mostram o "
              "percentual do conjunto da sua Região Administrativa"),
}

def _sisvan_pct(partes, nome):
    """specs/2026-10-06_deck_alimentacao_brincar: % recalculado de contagem ÷ total (duas colunas de % publicadas têm
    erro na origem: desnutrição 2023, obesidade 2009) e sem 2026, ano parcial -- o slide cita o último ano completo."""
    def f(df):
        d = df[df["ano"] <= 2025].copy()
        d[nome] = d[partes].sum(axis=1) / d["total"] * 100
        return d
    return f


_FONTE_SISVAN = "SISVAN/DATASUS, crianças até 72 meses acompanhadas na atenção básica; % recalculado das contagens"

def _pct_br(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",") + "%"


def _mil_br(v):
    return f"{int(round(v)):,}".replace(",", ".")


def _desenha_matriculas_pandemia(df, imp, nome, cfg):
    """specs/2026-10-07_deck_familia_moradia: matrículas de 0 a 5 anos por rede, 2015-2025, eixo a partir de zero, com
    a faixa da pandemia (2020-2021) e a variação 2019 -> 2021 de cada rede escrita no ponto de 2021."""
    import matplotlib.pyplot as plt
    d = df[df["ano"] >= 2015].sort_values("ano")
    topo = d[["matriculas_publica", "matriculas_privada"]].max().max() * 1.18
    fig, ax = plt.subplots(figsize=(imp._LARGURA_A4, 7.2 * imp._CM))
    ax.axvspan(2019.5, 2021.5, color=imp._GRADE, alpha=0.6, lw=0, zorder=0)
    ax.text(2020.5, topo * 0.98, "pandemia", ha="center", va="top", fontsize=7, color=imp._TINTA2)
    for col, rotulo, cor in (("matriculas_publica", "Rede pública", imp._PALETA_IMPRESSAO[0]),
                             ("matriculas_privada", "Rede privada", imp._PALETA_IMPRESSAO[1])):
        ax.plot(d["ano"], d[col], color=cor, marker="o", ms=3, mec="white", mew=0.6)
        a19, a21 = (float(d.loc[d["ano"] == a, col].iloc[0]) for a in (2019, 2021))
        var = (a21 / a19 - 1) * 100
        ax.annotate(f"{_pct_br(var, 1 if abs(var) < 10 else 0).replace('-', '−')} de 2019 a 2021",
                    xy=(2021, a21), xytext=(0, -9), textcoords="offset points", ha="center", va="top", fontsize=7,
                    color=cor, fontweight="bold")
        fim = d.iloc[-1]
        ax.annotate(f"{rotulo}  {_mil_br(fim[col])}", xy=(fim["ano"], fim[col]), xytext=(5, 0),
                    textcoords="offset points", va="center", fontsize=7, color=imp._TINTA, fontweight="semibold",
                    annotation_clip=False)
    ax.set_ylim(0, topo)
    ax.set_xlim(2014.6, 2025.4)
    ax.set_xticks(range(2015, 2026))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _mil_br(v)))
    ax.set_ylabel("Matrículas")
    imp._salva_a4(fig, nome, "grafico", cfg["titulo"], cfg["fonte"], "Matrículas")


def _desenha_vacinas_metas(df, imp, nome, cfg):
    """specs/2026-10-07_deck_familia_moradia: uma linha por vacina, ordenadas pela cobertura do último ano completo
    (barra verde se atinge a meta do PNI, laranja se não), com o pior ano recente (círculo vazado) e a meta (traço)."""
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    sys.path.insert(0, str(AQUI))
    import numeros
    t = numeros.tabela_vacinas()
    pior, atual = t.attrs["ano_pior"], numeros.VAC_ANO
    cor_ok, cor_baixo = imp._PALETA_IMPRESSAO[2], imp._PALETA_IMPRESSAO[1]
    fig, ax = plt.subplots(figsize=(imp._LARGURA_A4, 8.6 * imp._CM))
    y = list(range(len(t)))
    ax.barh(y, t["atual"], height=0.62, color=[cor_ok if a else cor_baixo for a in t["atinge"]], zorder=2)
    ax.scatter(t["pior"], y, s=26, facecolor="white", edgecolor=imp._TINTA, lw=0.9, zorder=4)
    for i, r in t.iterrows():
        ax.plot([r["meta"]] * 2, [i - 0.42, i + 0.42], color=imp._TINTA, lw=1.4, zorder=5)
        ax.text(max(r["atual"], r["meta"]) + 1.5, i, _pct_br(r["atual"]), va="center", fontsize=7,
                color=imp._TINTA, fontweight="semibold")
    ax.set_yticks(y)
    ax.set_yticklabels(t["vacina"])
    ax.set_xlim(0, 125)
    ax.set_xticks(range(0, 121, 20))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True, color=imp._GRADE, lw=0.5)
    ax.set_xlabel("Cobertura vacinal (%)")
    ax.legend(handles=[Patch(color=cor_ok, label=f"{atual}: atingiu a meta"),
                       Patch(color=cor_baixo, label=f"{atual}: abaixo da meta"),
                       Line2D([], [], color=imp._TINTA, lw=1.4, label="meta do PNI"),
                       Line2D([], [], marker="o", ls="", mfc="white", mec=imp._TINTA, label=f"{pior} (pior ano recente)")],
              loc="upper left", bbox_to_anchor=(0, -0.13), ncol=4, handlelength=1.4, columnspacing=1.2)
    imp._salva_a4(fig, nome, "grafico", cfg["titulo"], cfg["fonte"], "Cobertura vacinal (%)")


def _desenha_pobreza_arranjo(df, imp, nome, cfg):
    """specs/2026-10-07_deck_familia_moradia: % em pobreza (renda por pessoa até R$ 218) por arranjo familiar, uma barra
    por arranjo, com o número de famílias do arranjo. No lugar da versão A4 das barras agrupadas, cuja legenda cobria
    as barras e cuja célula suprimida (< 20) aparecia como 0,0."""
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(RAIZ))
    from primeira_infancia.cadunico import _ROTULOS_RENDA_CADUNICO_3
    pobreza = _ROTULOS_RENDA_CADUNICO_3["0-218"].replace("\n", " ")
    # total do arranjo da tabela de arranjos (a soma das faixas perde as células suprimidas)
    tot = pd.read_csv(RAIZ / "tabelas_finais/cadunico_familias_por_arranjo_2026.csv").set_index("arranjo familiar")["Famílias"]
    d = df[df["faixa de renda per capita"] == pobreza].set_index("arranjo")
    d = d.assign(total=tot).sort_values("% no arranjo")
    fig, ax = plt.subplots(figsize=(imp._LARGURA_A4, 7.0 * imp._CM))
    cores = [imp._PALETA_IMPRESSAO[1] if a == "Uma adulta (mulher)" else imp._CINZA_CONTEXTO for a in d.index]
    y = list(range(len(d)))
    ax.barh(y, d["% no arranjo"], height=0.6, color=cores, zorder=2)
    for i, (a, r) in enumerate(d.iterrows()):
        ax.text(r["% no arranjo"] + 1.5, i, f"{_pct_br(r['% no arranjo'], 0)}  ({_mil_br(r['total'])} famílias)",
                va="center", fontsize=7, color=imp._TINTA,
                fontweight="bold" if a == "Uma adulta (mulher)" else "normal")
    ax.set_yticks(y)
    ax.set_yticklabels(d.index)
    ax.set_xlim(0, 125)
    ax.set_xticks(range(0, 101, 20))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True, color=imp._GRADE, lw=0.5)
    ax.set_xlabel("% das famílias do arranjo em pobreza (renda por pessoa de até R$ 218)")
    imp._salva_a4(fig, nome, "grafico", cfg["titulo"], cfg["fonte"], "% em pobreza")


GRAFICOS = {
    # specs/2026-10-07_deck_familia_moradia: só a variante variantes/familia_cuidados.md
    "apres_cadunico_pobreza_arranjo": dict(
        tabela="cadunico_familias_arranjo_renda_2026.csv", desenha=_desenha_pobreza_arranjo,
        titulo="Famílias com crianças até 72 meses no CadÚnico em pobreza, por arranjo familiar",
        fonte="Cadastro Único (extração CTPE); pobreza: renda por pessoa de até R$ 218"),
    "apres_matriculas_rede_pandemia": dict(
        tabela="matriculas_0_a_5_por_ano.csv", desenha=_desenha_matriculas_pandemia,
        titulo="Matrículas de crianças de 0 a 5 anos, por rede (2015-2025)",
        fonte="Censo Escolar da Educação Básica (INEP), microdados; matrículas em escolas do município do Rio"),
    "apres_cobertura_vacinal_metas": dict(
        tabela="cobertura_vacinal_epi_por_ano.csv", desenha=_desenha_vacinas_metas,
        titulo="Cobertura vacinal por vacina e meta do Programa Nacional de Imunizações",
        fonte="EPI/SVS-Rio, cobertura vacinal por imunobiológico; metas do PNI: 90% para BCG e rotavírus, 95% para as "
              "demais; cobertura acima de 100% é possível (doses aplicadas sobre a população estimada)"),
    # specs/2026-10-06_deck_alimentacao_brincar: só a variante variantes/alimentacao.md
    "apres_sisvan_desnutricao_ano": dict(
        tabela="sisvan_desnutricao_por_ano.csv", tempo="ano", colunas={"Peso baixo ou muito baixo": "pct"},
        prepara=_sisvan_pct(["peso_muito_baixo_bruto", "peso_baixo_bruto"], "pct"),
        titulo="% das crianças acompanhadas com peso baixo ou muito baixo para a idade (SISVAN, 2008-2025)",
        ylabel="% das crianças acompanhadas", fonte=_FONTE_SISVAN + "; peso para a idade"),
    "apres_sisvan_sobrepeso_ano": dict(
        tabela="sisvan_sobrepeso_por_ano.csv", tempo="ano",
        colunas={"Sobrepeso ou obesidade": "pct_excesso", "Obesidade": "pct_obesidade"},
        prepara=lambda df: _sisvan_pct(["obesidade_bruto"], "pct_obesidade")(
            _sisvan_pct(["sobrepeso_bruto", "obesidade_bruto"], "pct_excesso")(df)),
        titulo="% das crianças acompanhadas com sobrepeso ou obesidade (SISVAN, 2008-2025)",
        ylabel="% das crianças acompanhadas", fonte=_FONTE_SISVAN + "; índice de massa corporal para a idade"),
    # pedido do usuário (2026-09-29): uma linha só, mãe + pai somados
    "apres_violencia_familiar_mae_pai_taxa_ano": dict(
        tabela="violencia_familiar_taxa_municipio_ano.csv", prepara=_vf_mae_pai_municipio, tempo="ano",
        colunas={"Mãe ou pai": "taxa_por_mil_mae_pai"}, marcos={2017: "possível quebra de série (2017)"},
        titulo="Notificações de violência familiar com mãe ou pai como provável autor, por 1.000 crianças (2011-2025)",
        ylabel="Notificações por 1.000 crianças",
        fonte=_FONTE_SINAN + "; população 0 a 5 anos: estimativas Ripsa/Ministério da Saúde; soma dos vínculos mãe e pai"),
}


def teto_tukey(valores):
    """Maior valor dentro da cerca superior de Tukey e a lista dos que ficam acima (outliers altos)."""
    v = pd.Series(valores).dropna()
    q1, q3 = v.quantile(0.25), v.quantile(0.75)
    cerca = q3 + 1.5 * (q3 - q1)
    return float(v[v <= cerca].max()), v[v > cerca]


def _num(v):
    return f"{v:.1f}".replace(".", ",")


def _nomes_bairros():
    import geopandas as gpd
    geo = gpd.read_file(RAIZ / "dados_locais/geo/limite_bairros_rio.geojson")
    return dict(zip(geo["codbairro"].astype(int), geo["nome"]))


def gera(nome):
    """Gera (se faltar ou estiver velho) o PDF do mapa ou do gráfico; devolve (caminho, fonte para o rodapé)."""
    if nome in GRAFICOS:
        return gera_grafico(nome)
    cfg = MAPAS[nome]
    destino = SAIDA / f"{nome}.pdf"
    tabela = RAIZ / "tabelas_finais" / cfg["tabela"]
    df = pd.read_csv(tabela)
    if cfg.get("prepara"):
        df = cfg["prepara"](df)
    fonte = cfg["fonte"]
    teto = None
    if cfg.get("outliers_fixos"):
        # bairros escolhidos como valor atípico (lista do pacote, a mesma do analise.py e do site): a escala vai até o
        # maior dos demais e eles ficam na cor máxima, nomeados no rodapé
        sys.path.insert(0, str(RAIZ))
        import primeira_infancia.cadunico as cad
        fixos = df[cfg["chave"]].astype(int).isin(getattr(cad, cfg["outliers_fixos"]))
        teto = float(df.loc[~fixos, cfg["coluna"]].max())
        nomes = _nomes_bairros()
        lista = "; ".join(f"{nomes[int(c)]} ({_num(v)}%)" for c, v in df.loc[fixos, [cfg["chave"], cfg["coluna"]]].values)
        fonte += f". Nota: valor atípico, na cor máxima: {lista}; escala de cor até {_num(teto)}%"
    elif not cfg.get("bins") and cfg.get("outlier", True):
        teto, altos = teto_tukey(df[cfg["coluna"]])
        if len(altos):
            if cfg["nivel"] == "bairro":
                nomes = _nomes_bairros()
                # código fora do geojson (ex. 998, bairro ignorado no Tabnet) não está no mapa: não entra na lista
                # (achado em specs/2026-10-06_deck_alimentacao_brincar)
                regioes = [nomes[int(c)] for c in df.loc[altos.sort_values(ascending=False).index, cfg["chave"]]
                           if int(c) in nomes]
            elif cfg.get("rotulo"):
                regioes = df.loc[altos.sort_values(ascending=False).index, cfg["rotulo"]].str.strip().str.title().tolist()
            else:
                regioes = []
            lista = ", ".join(regioes[:6]) + (f" e mais {len(regioes) - 6}" if len(regioes) > 6 else "")
            fonte += (f". Nota: valores extremos (acima da cerca de Tukey, 1,5 × intervalo interquartil) ficam com a cor "
                      f"máxima; escala limitada a {_num(teto)}" + (f"; acima: {lista}" if lista else ""))
        else:
            teto = float(df[cfg["coluna"]].max())   # sem outlier: escala até o máximo (e não o P95 da versão A4)
    fresco = max(tabela.stat().st_mtime, Path(__file__).stat().st_mtime)
    if destino.exists() and destino.stat().st_mtime >= fresco:
        return destino, fonte
    sys.path.insert(0, str(RAIZ))
    import geopandas as gpd
    import primeira_infancia.impressao as imp
    from primeira_infancia.estilo import _CORES_TEMA_MAPA
    from primeira_infancia.mapas import _NIVEIS_AGREGACAO
    SAIDA.mkdir(parents=True, exist_ok=True)
    imp._PASTA_A4 = {"grafico": str(SAIDA), "mapa": str(SAIDA)}          # nada vai para mapas/a4/
    imp._MANIFESTO_A4 = str(SAIDA / "_manifesto.csv")
    info = _NIVEIS_AGREGACAO[cfg["nivel"]]
    geo = gpd.read_file(RAIZ / "dados_locais/geo/limite_bairros_rio.geojson")
    geo[info["coluna_geo"]] = geo[info["coluna_geo"]].astype(info["tipo"])
    if cfg["nivel"] != "bairro":
        geo = geo.dissolve(by=info["coluna_geo"], as_index=False)
    df[cfg["chave"]] = df[cfg["chave"]].astype(info["tipo"])
    gdf = geo.merge(df[[cfg["chave"], cfg["coluna"]]], left_on=info["coluna_geo"], right_on=cfg["chave"], how="left")
    cmap = _CMAPS.get(cfg.get("cmap"), cfg.get("cmap")) or _CORES_TEMA_MAPA[cfg["tema"]]
    imp._a4_mapa(gdf, cfg["coluna"], cfg["titulo"], nome_arquivo=nome, nivel=cfg["nivel"], bins=cfg.get("bins"),
                 cmap=cmap, legenda_titulo=cfg["legenda"], fonte_dados=cfg["fonte"],
                 zero_branco=cfg.get("zero_branco", False),
                 caminho_uf=str(RAIZ / "dados_locais/geo/limite_uf_brasil.geojson"),
                 caminho_municipios=str(RAIZ / "dados_locais/geo/limite_municipios_rj.geojson"),
                 teto=teto, piso=cfg.get("piso"))
    if not destino.exists():
        raise RuntimeError(f"mapa {nome} não foi gerado (ver aviso acima)")
    return destino, fonte


def gera_grafico(nome):
    cfg = GRAFICOS[nome]
    destino = SAIDA / f"{nome}.pdf"
    tabela = RAIZ / "tabelas_finais" / cfg["tabela"]
    fresco = max(tabela.stat().st_mtime, Path(__file__).stat().st_mtime)
    if destino.exists() and destino.stat().st_mtime >= fresco:
        return destino, cfg["fonte"]
    sys.path.insert(0, str(RAIZ))
    import primeira_infancia.impressao as imp
    SAIDA.mkdir(parents=True, exist_ok=True)
    imp._PASTA_A4 = {"grafico": str(SAIDA), "mapa": str(SAIDA)}          # nada vai para visualizacoes/a4/
    imp._MANIFESTO_A4 = str(SAIDA / "_manifesto.csv")
    df = pd.read_csv(tabela)
    if cfg.get("prepara"):
        df = cfg["prepara"](df)
    if cfg.get("desenha"):
        import matplotlib.pyplot as plt
        with plt.rc_context(imp._rc_impressao()):
            cfg["desenha"](df, imp, nome, cfg)
    else:
        imp._a4_series(df, cfg["tempo"], cfg["colunas"], cfg["titulo"], nome_arquivo=nome, ylabel=cfg["ylabel"],
                       fonte_dados=cfg["fonte"], marcos=cfg.get("marcos"))
    if not destino.exists():
        raise RuntimeError(f"gráfico {nome} não foi gerado (ver aviso acima)")
    return destino, cfg["fonte"]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for n in [*MAPAS, *GRAFICOS]:
        print(n, *gera(n))
