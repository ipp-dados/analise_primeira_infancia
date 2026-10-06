# -*- coding: utf-8 -*-
"""### 🗺️ Mapas coropléticos

`mapa_coropletico_bairros` (bairro, AP, RP, RA ou CAP; classes discretas para contagens, colorbar contínua para taxas/percentuais — convenção fixa do projeto) e `agrega_bairros_por_nivel` (soma numerador e denominador por nível antes de recalcular a taxa). Histórico das escolhas de estilo em `.claude/skills/generate_map/SKILL.md`.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import contextily as ctx
import geopandas as gpd
import math
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
from .estilo import (_FONTE_TITULO, _PROVEDORES_FUNDO, _adiciona_rotulos_municipios_vizinhos, _numero_ptbr)
from .impressao import _a4_mapa

__all__ = [
    '_NIVEIS_AGREGACAO',
    '_CAMINHO_GEO_CAP',
    '_RA_PARA_CAP',
    '_adiciona_rosa_dos_ventos',
    'agrega_bairros_por_nivel',
    'mapa_coropletico_bairros',
]


# nível de agregação geográfica: coluna do geojson de bairros usada no dissolve/join, e o tipo para
# comparação (Área de Planejamento e codbairro são numéricos; Região de Planejamento é 'AP.subregião',
# ex. '4.2', e não pode virar número sem perder precisão)
_NIVEIS_AGREGACAO = {
    'bairro': {'coluna_geo': 'codbairro', 'tipo': int},
    'ap':     {'coluna_geo': 'area_plane', 'tipo': int},
    'rp':     {'coluna_geo': 'cod_rp', 'tipo': str},
    'cap':    {'coluna_geo': 'cod_ap_sms', 'tipo': str},
    'ra':     {'coluna_geo': 'codra', 'tipo': int},  # Região Administrativa (33 no geojson de bairros; não existe RA 32)
}

# geojson oficial das 10 CAPs (Coordenadoria de Área Programática de Saúde, SMS-Rio -- não
# aninha no geojson de bairros do IPP, que só traz Área/Região de Planejamento), Data.Rio
# ("Áreas Programáticas da Saúde"); ver specs/2026-09-08_mortalidade-ap/specification.md §4
_CAMINHO_GEO_CAP = 'dados_locais/geo/limite_ap_saude_rio.geojson'

# de-para RA -> CAP, derivado do cruzamento espacial com o polígono oficial acima (não de
# memória -- a versão anterior, escrita à mão, errava Guaratiba e Complexo do Alemão). Não é
# usado pelos mapas desta seção (que usam o geojson oficial direto via nivel='cap'); fica
# documentado para uso futuro, agregando qualquer tabela por bairro/RA até a CAP
_RA_PARA_CAP = {
    1: '1.0', 2: '1.0', 3: '1.0', 7: '1.0', 21: '1.0', 23: '1.0',
    4: '2.1', 5: '2.1', 6: '2.1', 27: '2.1',
    8: '2.2', 9: '2.2',
    10: '3.1', 11: '3.1', 20: '3.1', 29: '3.1', 30: '3.1', 31: '3.1',
    12: '3.2', 13: '3.2', 28: '3.2',
    14: '3.3', 15: '3.3', 22: '3.3', 25: '3.3',
    16: '4.0', 24: '4.0', 34: '4.0',
    17: '5.1', 33: '5.1',
    18: '5.2', 26: '5.2',
    19: '5.3',
}

def _adiciona_rosa_dos_ventos(ax, x=0.94, y=0.90, tamanho=0.05, cor='#262626'):
    """Desenha uma seta 'N' simples (rosa dos ventos) no canto superior direito do mapa."""
    ax.annotate(
        'N', xy=(x, y), xytext=(x, y - tamanho),
        xycoords=ax.transAxes, textcoords=ax.transAxes,
        ha='center', va='center', fontsize=15, fontweight='bold', color=cor,
        arrowprops=dict(arrowstyle='-|>', color=cor, lw=2.0, mutation_scale=24),
        zorder=5,
    )

def agrega_bairros_por_nivel(df, nivel, colunas_soma):
    """Agrega uma tabela por bairro para o nível de Área de Planejamento ('ap') ou Região de
    Planejamento ('rp'), somando `colunas_soma` (ex.: contagens absolutas). Percentuais devem ser
    recalculados depois a partir das colunas somadas (ex.: total de crianças / população total),
    nunca por média simples das linhas por bairro -- bairros têm populações muito desiguais.

    `df` precisa já trazer a coluna administrativa do próprio nível ('area_plane' para 'ap', 'cod_rp'
    para 'rp') -- os exports do Censo/Data.Rio por bairro já vêm com essas colunas nativamente (não
    é preciso buscá-las no geojson de bairros à parte)."""
    coluna_geo, tipo = _NIVEIS_AGREGACAO[nivel]['coluna_geo'], _NIVEIS_AGREGACAO[nivel]['tipo']
    df = df.copy()
    df[coluna_geo] = df[coluna_geo].astype(tipo)
    return df.groupby(coluna_geo, as_index=False)[colunas_soma].sum()

def mapa_coropletico_bairros(df, coluna_valor, titulo, nome_arquivo, chave=None, nivel='bairro', bins=None,
                              cmap='Oranges', legenda_titulo=None, fundo='mapa_oceano_base', alpha=None, fonte_dados=None,
                              caminho_geojson='dados_locais/geo/limite_bairros_rio.geojson',
                              caminho_uf='dados_locais/geo/limite_uf_brasil.geojson',
                              caminho_municipios='dados_locais/geo/limite_municipios_rj.geojson', formato='png', zero_branco=False,
                              teto=None):
    """Gera um mapa coroplético do Rio (limites IPP/Data.Rio, simplificados) e salva em mapas/.

    `nivel`: 'bairro' (padrão) | 'ap' (Área de Planejamento, 5 regiões) | 'rp' (Região de
    Planejamento, 16 regiões) | 'ra' (Região Administrativa, 33 regiões, chave `codra`) -- une (`dissolve`) os polígonos de bairro nesse nível antes do join
    com `df`. `chave` é a coluna de `df` usada no join; se None, usa o nome padrão de cada nível
    ('codbairro', 'area_plane' ou 'cod_rp') -- `df` deve trazer essa coluna já agregada (ver
    `agrega_bairros_por_nivel` para ir de uma tabela por bairro a uma por AP/RP).

    Bairros/regiões sem correspondência em `df` ficam sem preenchimento ('Sem dado'). Se `bins` for
    informado (lista de limites superiores, ex.: [1000, 2500, 5000, 10000]), o mapa usa classes
    discretas com legenda no padrão 'Até X' / 'X a Y' / 'Mais de Z' (estilo de
    `mapas/mapa_referencia.jpeg`); caso contrário, usa uma escala contínua com barra de cores
    (legenda/colorbar sempre dentro da própria área do mapa, não numa coluna externa -- só o título
    fica na margem branca da figura).

    `fundo`: 'mapa' (padrão -- basemap cartográfico via Esri Ocean Basemap: relevo, mar em azul, sem
    nomes de cidade) | None (fundo branco liso, sem contexto geográfico). Com fundo, os limites
    estaduais (UF, fonte IBGE) do entorno são sobrepostos em amarelo tracejado, os municípios
    vizinhos (não Rio de Janeiro) visíveis são rotulados, a vista é ampliada além dos bairros para
    dar contexto (região metropolitana, baía, mar), e o mapa recebe rosa dos ventos + escala gráfica
    (corrigida para a distorção de latitude do Web Mercator).
    `zero_branco` (só com `bins`, contagens absolutas): quando True, valores iguais a 0 ficam brancos, com
    entrada própria '0 (sem casos)' na legenda, em vez de cair na primeira classe ('Até X'). Padrão False
    (comportamento anterior, usado pelos demais mapas).
    `teto` (só escala contínua): limite superior da cor -- valores acima ficam na cor máxima e a colorbar ganha a ponta
    de "acima de" (outlier, ex. Alto da Boa Vista na inadequação habitacional; specs/2026-10-06_cadunico_inclusao_moradia).
    Vai também para a variante A4. None (padrão) = escala até o máximo, como antes; diga no `fonte_dados` quem passou.

    A figura usa proporção larga (~1,46:1, próxima de A4 paisagem) e é exportada a 300 DPI com
    `bbox_inches='tight'`, para que só o título ocupe espaço fora do mapa em si.

    `fonte_dados`: texto curto citando a fonte dos dados temáticos (ex.: 'Censo Demográfico 2022
    (IBGE/Data.Rio)'), exibido no rodapé do mapa junto com o sistema de referência -- SIRGAS 2000
    (dados originais) e, quando `fundo` está ativo, Web Mercator/EPSG:3857 (projeção usada para
    render, a mesma dos basemaps web -- por isso a escala gráfica é corrigida para a latitude, ver
    a skill generate_map).
    """
    info_nivel = _NIVEIS_AGREGACAO[nivel]
    coluna_geo, tipo = info_nivel['coluna_geo'], info_nivel['tipo']
    chave = chave or coluna_geo

    gdf_bairros = gpd.read_file(caminho_geojson)
    gdf_bairros[coluna_geo] = gdf_bairros[coluna_geo].astype(tipo)
    gdf_nivel = gdf_bairros if nivel == 'bairro' else gdf_bairros.dissolve(by=coluna_geo, as_index=False)

    df = df.copy()
    df[chave] = df[chave].astype(tipo)
    gdf = gdf_nivel.merge(df[[chave, coluna_valor]], left_on=coluna_geo, right_on=chave, how='left')
    gdf_a4 = gdf.copy()   # variante de impressão (mesmos dados, desenho próprio)

    # fator de correção do Web Mercator na latitude do Rio (~-23°), para a escala gráfica ficar correta
    # (centroide aproximado só para essa correção, não precisa de precisão métrica -- dispensa reprojeção)
    lat_media = gdf.geometry.centroid.y.mean()
    correcao_mercator = math.cos(math.radians(lat_media))

    usa_fundo = fundo is not None
    if usa_fundo:
        if fundo not in _PROVEDORES_FUNDO:
            raise ValueError(f"fundo inválido: {fundo!r} (use 'mapa' ou None)")
        gdf = gdf.to_crs(epsg=3857)
    alpha = alpha if alpha is not None else (0.82 if usa_fundo else 1.0)
    missing_kwds = ({'color': 'none', 'edgecolor': '#8a8a8a', 'hatch': '///', 'label': 'Sem dado'}
                     if usa_fundo else {'color': '#f0f0f0', 'edgecolor': '#bdbdbd', 'label': 'Sem dado'})

    # figura em formato largo: padding vertical generoso (contexto acima/abaixo do município), mas
    # bem mais enxuto na horizontal -- o contorno dos bairros já é ~1,9:1 (muito mais largo que
    # alto); cortar o excesso de fundo/basemap nas laterais (não os bairros) aproxima a proporção
    # final de uma página A4 paisagem (~1,41:1) sem cortar nenhum dado
    minx, miny, maxx, maxy = gdf.total_bounds
    padx, pady = (maxx - minx) * 0.03, (maxy - miny) * 0.15
    aspecto = (maxx - minx + 2 * padx) / (maxy - miny + 2 * pady)
    altura_fig = 8.5
    _, ax = plt.subplots(figsize=(round(altura_fig * aspecto, 1), altura_fig))

    if bins:
        limite_inferior = min(gdf[coluna_valor].min(), bins[0]) - 1
        limite_superior = max(gdf[coluna_valor].max(), bins[-1])
        limites = [limite_inferior] + list(bins) + [limite_superior]
        rotulos = [f"Até {_numero_ptbr(bins[0])}"]
        rotulos += [f"{_numero_ptbr(bins[i-1]+1)} a {_numero_ptbr(bins[i])}" for i in range(1, len(bins))]
        rotulos.append(f"Mais de {_numero_ptbr(bins[-1])}")
        eh_zero = (gdf[coluna_valor] == 0) if zero_branco else pd.Series(False, index=gdf.index)
        gdf['faixa'] = pd.cut(gdf[coluna_valor].where(~eh_zero), bins=limites, labels=rotulos, ordered=True)
        gdf.plot(
            column='faixa', ax=ax, cmap=cmap, linewidth=0.4, edgecolor='#616161', legend=True, alpha=alpha,
            zorder=2, missing_kwds=missing_kwds,
            legend_kwds={'title': legenda_titulo or coluna_valor, 'loc': 'upper left', 'fontsize': 10,
                         'title_fontsize': 12, 'framealpha': 0.92, 'facecolor': 'white', 'edgecolor': '#c9c9c9',
                         'labelcolor': '#111111'},
        )
        if zero_branco and eh_zero.any():
            # zeros por cima do preenchimento 'Sem dado' (que os cobre com hachura), em branco liso
            gdf[eh_zero].plot(ax=ax, color='white', linewidth=0.4, edgecolor='#616161', zorder=2.5)
            legenda_antiga = ax.get_legend()
            handles_ant = list(legenda_antiga.legend_handles)
            rotulos_ant = [t.get_text() for t in legenda_antiga.get_texts()]
            if not gdf[coluna_valor].isna().any():  # 'Sem dado' só se houver região realmente sem dado
                manter = [i for i, r in enumerate(rotulos_ant) if r != 'Sem dado']
                handles_ant, rotulos_ant = [handles_ant[i] for i in manter], [rotulos_ant[i] for i in manter]
            handles = [Line2D([0], [0], marker='o', linestyle='', markerfacecolor='white', markeredgecolor='#616161', markersize=11)] + handles_ant
            rotulos_leg = ['0 (sem casos)'] + rotulos_ant
            legenda_antiga.remove()
            ax.legend(handles=handles, labels=rotulos_leg, title=legenda_titulo or coluna_valor, loc='upper left', fontsize=10,
                      title_fontsize=12, framealpha=0.92, facecolor='white', edgecolor='#c9c9c9', labelcolor='#111111')
        legenda = ax.get_legend()
        legenda.get_title().set_fontweight('bold')
        for texto in legenda.get_texts():
            texto.set_fontweight('semibold')
    else:
        # colorbar como inset dentro da própria área do mapa (não numa coluna externa) -- mesmo canto
        # que a legenda de classes usaria, já que os dois modos são mutuamente exclusivos numa chamada;
        # deslocada para perto do topo (y0=0,60) para ficar mais sobre a margem de contexto (fora dos
        # bairros) do que sobre os próprios polígonos coloridos. Sem nenhum retângulo/caixa de fundo
        # (nem borda, nem preenchimento) atrás da colorbar -- os rótulos dos ticks e o texto do eixo
        # (rotacionado) ficam FORA da própria cax, então em vez de uma caixa opaca por baixo, cada
        # texto ganha um halo branco (path_effects.withStroke, a mesma técnica dos rótulos de
        # município vizinho) para continuar legível não importa sobre qual parte do mapa a colorbar
        # caia.
        cax_x0, cax_y0, cax_largura, cax_altura = 0.035, 0.60, 0.03, 0.30
        cax = ax.inset_axes([cax_x0, cax_y0, cax_largura, cax_altura])
        gdf.plot(
            column=coluna_valor, ax=ax, cmap=cmap, linewidth=0.4, edgecolor='#616161', legend=True, alpha=alpha,
            zorder=2, missing_kwds=missing_kwds, cax=cax, vmax=teto,
            legend_kwds={'label': legenda_titulo or coluna_valor,
                         **({'extend': 'max'} if teto is not None and gdf[coluna_valor].max() > teto else {})},
        )
        halo = [pe.withStroke(linewidth=3, foreground='white')]
        cax.tick_params(labelsize=9, colors='#111111')
        for rotulo in cax.get_yticklabels():
            rotulo.set_fontweight('semibold')
            rotulo.set_path_effects(halo)
        cax.yaxis.label.set_size(11)
        cax.yaxis.label.set_color('#111111')
        cax.yaxis.label.set_fontweight('bold')
        cax.yaxis.label.set_path_effects(halo)

    if usa_fundo:
        # amplia a vista além dos bairros para dar contexto (região metropolitana, baía, mar)
        ax.set_xlim(minx - padx, maxx + padx)
        ax.set_ylim(miny - pady, maxy + pady)

        gdf_uf = gpd.read_file(caminho_uf).to_crs(epsg=3857)
        gdf_uf.boundary.plot(ax=ax, color='#ffeb3b', linewidth=1.3, linestyle='--', zorder=1)
        ax.set_xlim(minx - padx, maxx + padx)
        ax.set_ylim(miny - pady, maxy + pady)

        ctx.add_basemap(ax, source=_PROVEDORES_FUNDO[fundo], zorder=0, attribution_size=6)

        _adiciona_rosa_dos_ventos(ax)
        ax.add_artist(ScaleBar(
            correcao_mercator, units='m', location='lower right', box_alpha=0.75,
            color='#262626', box_color='white', scale_loc='bottom', border_pad=0.6,
            font_properties={'size': 10},
        ))
        _adiciona_rotulos_municipios_vizinhos(ax, ax.get_xlim(), ax.get_ylim(), caminho_municipios=caminho_municipios)

    # rodapé com sistema de referência (+ projeção de render, quando reprojetado para o basemap) e
    # fonte dos dados -- convenção cartográfica (ver mapas/mapa_referencia.jpeg); sempre presente,
    # com ou sem fundo. Em duas linhas e deslocado um pouco à direita do centro: nem sobre o atributo
    # do basemap do contextily (inferior esquerdo, 2 linhas largas) nem sobre a escala gráfica
    # (inferior direito) -- ambos variam de largura conforme o recorte/nível do mapa
    texto_referencia = ('Sistema de referência: SIRGAS 2000, UTM - Fuso 23S (dados) | Web Mercator EPSG:3857 (mapa)'
                         if usa_fundo else 'Sistema de referência: SIRGAS 2000, UTM - Fuso 23S')
    rodape = texto_referencia if not fonte_dados else f"{texto_referencia}\nFonte: {fonte_dados}"
    ax.annotate(
        rodape, xy=(0.55, 0.012), xycoords='axes fraction', ha='center', va='bottom',
        fontsize=6.5, color='#262626', zorder=6,
        bbox=dict(boxstyle='square,pad=0.35', facecolor='white', alpha=0.8, edgecolor='none'),
    )

    ax.set_title(titulo, fontsize=22, pad=14, fontfamily=_FONTE_TITULO, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f"mapas/{nome_arquivo}.{formato}", dpi=300, bbox_inches='tight', pad_inches=0.15)
    _a4_mapa(gdf_a4, coluna_valor, titulo, nome_arquivo=nome_arquivo, nivel=nivel, bins=bins, cmap=cmap,
             legenda_titulo=legenda_titulo, fonte_dados=fonte_dados, zero_branco=zero_branco,
             caminho_uf=caminho_uf, caminho_municipios=caminho_municipios, teto=teto)
    plt.show()
