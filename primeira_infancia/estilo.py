# -*- coding: utf-8 -*-
"""Identidade visual compartilhada por gráficos, mapas e variante de impressão -- mesma paleta/rodapé de fonte usados no site e no PDF (ver specs/2026-09-09_visual-identity): paletas, fonte dos títulos, provedores de fundo cartográfico, formatação de números pt-BR e rótulos dos municípios vizinhos. Separada em specs/2026-09-28_organizacao para quebrar o ciclo gráficos ↔ impressão ↔ mapas.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import contextily as ctx
import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import xyzservices
from shapely.geometry import box

__all__ = [
    '_PALETA_CATEGORICA',
    '_NOTA_EIXO_CORTADO',
    '_marca_corte_eixo_y',
    '_CORES_TEMA_MAPA',
    '_LIMIAR_DESTAQUE_SERIES',
    '_N_SERIES_DESTACADAS',
    '_COR_SERIE_APAGADA',
    '_COR_FONTE_RODAPE',
    '_numero_ptbr',
    '_PROVEDORES_FUNDO',
    '_FONTE_TITULO',
    '_ZONA_LEGENDA',
    '_adiciona_rotulos_municipios_vizinhos',
]


# paleta categórica de 11 cores -- mesmos hex do motor JS de relatorio/index.html (--c1..--c11),
# para a mesma série ter a mesma cor no notebook, no PDF e no HTML.
_PALETA_CATEGORICA = ['#6a95c8', '#d28060', '#66cca7', '#deb254', '#ca688d',
                       '#54de54', '#8177bb', '#cc6766', '#bc9776', '#b67c99', '#8e9ea4']

# matiz sequencial por tema, usado por mapa_coropletico_bairros no lugar de um cmap fixo --
# mesma lógica "um matiz só por mapa" (magnitude), variando o matiz conforme o assunto.
_CORES_TEMA_MAPA = {
    'natalidade': 'BuGn',    # nascidos vivos, baixo peso
    'mortalidade': 'RdPu',   # óbitos (neonatal, gravidez, puerpério, raça, evitáveis/CAP)
    'cadunico': 'YlOrBr',    # CadÚnico
    'censo': 'Blues',        # Censo/população
    'protecao': 'OrRd',      # violência/notificações (eixo Proteção)
}

_LIMIAR_DESTAQUE_SERIES = 6  # acima disso, serie_temporal_multipla destaca só as mais relevantes

_N_SERIES_DESTACADAS = 4

_COR_SERIE_APAGADA = '#c9c9c9'

_COR_FONTE_RODAPE = '#5E6D68'

def _numero_ptbr(n):
    """Formata um número inteiro com separador de milhar no padrão brasileiro (ex.: 10000 -> '10.000')."""
    return f"{n:,.0f}".replace(",", ".")

# basemap cartográfico/'desenho' (sem satélite -- descartado; ver generate_map skill para o porquê):
# relevo suave, sem rótulos de municípios vizinhos, mar em azul. max_zoom 13 (suficiente na escala do município).
_PROVEDORES_FUNDO = {
    'mapa': ctx.providers.Esri.OceanBasemap,
}

# o serviço 'Ocean_Basemap' da Esri (provedor de 'mapa') passou a responder HTTP 500 em 2026-09; o sucessor
# 'Ocean/World_Ocean_Base' tem o mesmo estilo (relevo suave, mar azul, sem rótulos) e serve os tiles.
# Chave nova (não altera 'mapa'): use fundo='mapa_oceano_base' enquanto o serviço antigo estiver fora do ar.
# 2026-09-25 (specs/2026-09-25_relatorio_latex, aprovado pelo usuário após comparação lado a lado): 'mapa_oceano_base' passou a
# ser o padrão de mapa_coropletico_bairros -- mesmo estilo; 'mapa' continua disponível se o serviço antigo voltar.
_PROVEDORES_FUNDO['mapa_oceano_base'] = xyzservices.TileProvider(
    name='Esri.WorldOceanBase',
    url='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
    attribution='Tiles © Esri — Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri',
    max_zoom=13,
)

_FONTE_TITULO = 'Palatino Linotype'  # serifada, estilo de publicação acadêmica

# canto reservado para a legenda/colorbar (sempre 'upper left'), em fração dos eixos (0-1) -- um
# rótulo de município vizinho que caia aqui seria sobreposto pela legenda, então é descartado
_ZONA_LEGENDA = (0.0, 0.46, 0.34, 1.0)  # (x0, y0, x1, y1)

def _adiciona_rotulos_municipios_vizinhos(ax, xlim, ylim, cor='#262626', tamanho=10, margem=0.02,
                                           caminho_municipios='dados_locais/geo/limite_municipios_rj.geojson'):
    """Rotula os municípios vizinhos (não Rio de Janeiro) visíveis na área do mapa.

    Usa o ponto representativo do FRAGMENTO recortado pela janela (garante que o rótulo fique dentro
    da parte de fato visível do município, não fora do mapa) -- mas descarta fragmentos cujo ponto
    fica perto demais da borda (`margem`), que é o caso de um município que só encosta numa pontinha
    do canto do mapa (ex.: Rio Claro, cujo pedaço visível é um triângulo minúsculo no canto) e cujo
    rótulo sairia cortado pela borda da figura. Também descarta quem cairia sobre a legenda/colorbar
    (sempre no canto superior esquerdo -- `_ZONA_LEGENDA`).
    """
    gdf_mun = gpd.read_file(caminho_municipios).to_crs(epsg=3857)
    gdf_mun = gdf_mun[gdf_mun['nome'] != 'Rio de Janeiro'].copy()
    janela = box(xlim[0], ylim[0], xlim[1], ylim[1])
    gdf_mun = gdf_mun[gdf_mun.intersects(janela)].copy()
    gdf_mun['ponto'] = gdf_mun.intersection(janela).apply(lambda g: g.representative_point())

    largura, altura = xlim[1] - xlim[0], ylim[1] - ylim[0]
    x0, x1 = xlim[0] + largura * margem, xlim[1] - largura * margem
    y0, y1 = ylim[0] + altura * margem, ylim[1] - altura * margem
    lx0, ly0, lx1, ly1 = _ZONA_LEGENDA

    def _visivel(p):
        if not (x0 <= p.x <= x1 and y0 <= p.y <= y1):
            return False
        xf, yf = (p.x - xlim[0]) / largura, (p.y - ylim[0]) / altura
        return not (lx0 <= xf <= lx1 and ly0 <= yf <= ly1)

    gdf_visiveis = gdf_mun[gdf_mun['ponto'].apply(_visivel)]
    for _, row in gdf_visiveis.iterrows():
        ponto = row['ponto']
        ax.annotate(
            row['nome'], xy=(ponto.x, ponto.y), ha='center', va='center',
            fontsize=tamanho, color=cor, fontweight='medium', zorder=4,
            path_effects=[pe.withStroke(linewidth=2.5, foreground='white')],
        )


# ------------------------------------------------------------------ eixo y cortado (specs/2026-09-29_pendencias D3/D12)
# Única exceção à base zero (P1): percentual de baixo peso ao nascer. O corte é desenhado (duas barras inclinadas no pé
# do eixo y) e dito por escrito na fonte, no gráfico de tela, na variante A4 (PDF) e no site (js/charts.js).
_NOTA_EIXO_CORTADO = 'Nota: eixo não começa em zero'

def _marca_corte_eixo_y(ax, cor='#5a6570', tamanho=0.018):
    """Duas barras inclinadas sobre a base do eixo y, em coordenadas do eixo (independe da escala dos dados)."""
    fundo = ax.get_facecolor()
    ax.add_patch(mpatches.Rectangle(
        (-tamanho, -tamanho * 0.2), tamanho * 2.2, tamanho * 2.4, transform=ax.transAxes, facecolor=fundo,
        edgecolor='none', clip_on=False, zorder=5))
    for dy in (0, tamanho):
        ax.plot([-tamanho, tamanho], [dy - tamanho * 0.3, dy + tamanho * 0.9], transform=ax.transAxes, color=cor,
                linewidth=1.0, clip_on=False, zorder=6, solid_capstyle='round')
