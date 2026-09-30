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

GRAFICOS: séries só da apresentação, no desenho de impressão do analise.py (`_a4_series`); mesma chave `fig:<nome>`.

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
}

GRAFICOS = {
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
    if not cfg.get("bins") and cfg.get("outlier", True):
        teto, altos = teto_tukey(df[cfg["coluna"]])
        if len(altos):
            if cfg["nivel"] == "bairro":
                nomes = _nomes_bairros()
                regioes = [nomes.get(int(c), str(c)) for c in df.loc[altos.sort_values(ascending=False).index, cfg["chave"]]]
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
                 teto=teto)
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
    imp._a4_series(df, cfg["tempo"], cfg["colunas"], cfg["titulo"], nome_arquivo=nome, ylabel=cfg["ylabel"],
                   fonte_dados=cfg["fonte"], marcos=cfg.get("marcos"))
    if not destino.exists():
        raise RuntimeError(f"gráfico {nome} não foi gerado (ver aviso acima)")
    return destino, cfg["fonte"]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for n in [*MAPAS, *GRAFICOS]:
        print(n, *gera(n))
