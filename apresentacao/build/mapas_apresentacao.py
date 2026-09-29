"""Mapas só da apresentação (specs/2026-09-28_apresentacao): o mesmo desenho da versão de impressão do analise.py
(`_a4_mapa`), com um tratamento de valores extremos pedido para o slide. Gravados em apresentacao/_build/mapas/ -- não
tocam em mapas/, no manifesto do relatório nem no site.

Regra de outlier: a mesma do site (cercas de Tukey, 1,5 x IQR, `remove_outliers_tukey` em website/build/build_site.py).
A escala de cor vai até o maior valor que NÃO é outlier; as regiões acima ficam com a cor máxima ("≥ x" na legenda).
Uso no slide: ![](fig:<chave de MAPAS>).
"""
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
SAIDA = AQUI.parent / "_build" / "mapas"

MAPAS = {
    # pedido do usuário (2026-09-28): no slide "O território onde a criança brinca" o Centro enviesava a escala
    "apres_violencia_territorial_homicidios_ra_2024": dict(
        tabela="tabela_mapa_violencia_territorial_ra_2024.csv", coluna="taxa_homicidios", chave="codra", nivel="ra",
        titulo="Taxa de homicídios por RA (2024) — população geral", tema="protecao",
        legenda="Taxa (IPS)\ntodas as idades,\nnão só crianças", rotulo="regiao_adm",
        fonte="Data.Rio / Índice de Progresso Social (IPS), 2024, por Região Administrativa (todas as idades)"),
}


def teto_tukey(valores):
    """Maior valor dentro da cerca superior de Tukey e a lista dos que ficam acima (outliers altos)."""
    v = pd.Series(valores).dropna()
    q1, q3 = v.quantile(0.25), v.quantile(0.75)
    cerca = q3 + 1.5 * (q3 - q1)
    return float(v[v <= cerca].max()), v[v > cerca]


def gera(nome):
    """Gera (se faltar ou estiver velho) o PDF do mapa; devolve (caminho, fonte para o rodapé)."""
    cfg = MAPAS[nome]
    destino = SAIDA / f"{nome}.pdf"
    tabela = RAIZ / "tabelas_finais" / cfg["tabela"]
    df = pd.read_csv(tabela)
    teto, altos = teto_tukey(df[cfg["coluna"]])
    acima = ", ".join(df.loc[altos.index, cfg["rotulo"]].str.title()) if cfg.get("rotulo") else ""
    fonte = cfg["fonte"]
    if len(altos):
        teto_txt = f"{teto:.1f}".replace(".", ",")
        fonte += f". Nota: escala de cor limitada a {teto_txt}" + (f"; {acima} acima, com a cor máxima (outlier)" if acima else "")
    if destino.exists() and destino.stat().st_mtime >= tabela.stat().st_mtime:
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
    imp._a4_mapa(gdf, cfg["coluna"], cfg["titulo"], nome_arquivo=nome, nivel=cfg["nivel"], bins=None,
                 cmap=_CORES_TEMA_MAPA[cfg["tema"]], legenda_titulo=cfg["legenda"], fonte_dados=cfg["fonte"],
                 zero_branco=False, caminho_uf=str(RAIZ / "dados_locais/geo/limite_uf_brasil.geojson"),
                 caminho_municipios=str(RAIZ / "dados_locais/geo/limite_municipios_rj.geojson"),
                 teto=teto if len(altos) else None)
    if not destino.exists():
        raise RuntimeError(f"mapa {nome} não foi gerado (ver aviso acima)")
    return destino, fonte


if __name__ == "__main__":
    for n in MAPAS:
        print(n, *gera(n))
