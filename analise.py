# %% [markdown]
# # 🏛️ Análise Primeira Infância Carioca
#
# Notebook de extração, limpeza e visualização dos indicadores de primeira infância
# (0 a 6 anos) do município do Rio de Janeiro: Censo, CadÚnico, DataSus/Tabnet
# (nascidos vivos, mortalidade, causas evitáveis, cobertura vacinal) e educação
# (PNAD/Censo Escolar).

# %% [markdown]
# ---
# ## 📦 Pacotes e Funções Auxiliares
#
# Imports, conexão com o banco e todas as funções de limpeza/wrangling e de
# visualização reutilizadas ao longo do notebook. Ficam centralizadas aqui para que
# as seções de análise abaixo apenas *chamem* essas funções, sem redefini-las.

# %%
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pathlib import Path
from matplotlib_scalebar.scalebar import ScaleBar
from shapely.geometry import box
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import contextily as ctx
import geopandas as gpd
import pandas as pd
import math
import os

# %% [markdown]
# ### 🔌 Conexão e utilitários gerais

# %%
#conecta ao banco CTPE
def connect_db_ctpe():
    """
    Inicializa o cliente do banco local.

    Returns:
        engine: engine de sqlalchemy
    """
    # cria parâmetros da conexão com banco local
    parameters = {
    "db_name": os.getenv('db_name'),
    "user": os.getenv('user'),
    "password_db": os.getenv('password_db'),
    "host": os.getenv('host'),
    "port": os.getenv('port')
    }
    DB_URL = f"postgresql+psycopg://{parameters['user']}:{parameters['password_db']}@{parameters['host']}:{parameters['port']}/{parameters['db_name']}?client_encoding=utf8"
    engine = create_engine(DB_URL)
    return engine

def convert_numeric_safe(s):
    s_cleaned = s.strip().replace('%','')
    return float(s_cleaned)

# %% [markdown]
# ### 🧹 Limpeza e wrangling de dados

# %%
def limpa_dados_sisvan(colunas, dataset):
    path = Path(f"dados_locais\\{dataset}\\")
    arquivos = [f.name for f in path.iterdir() if f.is_file() and not f.name.startswith('.') and f.name != 'example_file']

    colunas_ajustadas = ['ano']
    for i in colunas:
        if i != 'total':
            colunas_ajustadas.append(i+'_bruto')
            colunas_ajustadas.append(i+'_percentual')
        else:
            colunas_ajustadas.append(i)
    print(colunas_ajustadas)
    df_final = pd.DataFrame(columns=colunas_ajustadas)

    for arquivo in arquivos:
        df = pd.read_excel(f"dados_locais\\{dataset}\\{arquivo}")
        df_infos = df.iloc[[10],5:]
        df_infos.columns = colunas_ajustadas[1:]
        df_infos['ano'] = arquivo[-9:-5]
        df_final = pd.concat([df_final,df_infos])
    df_final.reset_index(inplace=True, drop=True)

    df_final.to_csv(f"dados_locais\\tratados\\{dataset}.csv")

def limpa_dados_datasus(df):
    df = df.melt(id_vars=['Bairro Residencia'])
    return df

def limpeza_tabnet_bairros(df,categoria):
    """Padroniza um export do Tabnet: extrai 'codigo' e 'bairro', remove linhas 'Total'."""
    df.columns = ['bairro','ano',categoria]
    df = df[df['bairro']!='Total']
    df = df[df['ano']!='Total']
    df[['codigo','bairro']] = df.loc[df['bairro']!='EM BRANCO','bairro'].str.split(' ', n=1,expand=True)
    return df

def carrega_raca_bairro(caminho, categoria, anos_validos, sep=';'):
    """Lê um export do Tabnet por bairro e reindexa numa grade bairro x ano completa,
    preenchendo com 0 os anos sem linha no arquivo original (evita contagens incompletas
    em somas/subtrações posteriores)."""
    df = pd.read_csv(caminho, sep=sep)
    df = limpa_dados_datasus(df)
    df = limpeza_tabnet_bairros(df, categoria=categoria)
    df = df.dropna(subset=['codigo', 'bairro'])
    df['ano'] = df['ano'].astype(int)
    grade = df[['codigo', 'bairro']].drop_duplicates().merge(pd.DataFrame({'ano': anos_validos}), how='cross')
    df = grade.merge(df[['codigo', 'bairro', 'ano', categoria]], on=['codigo', 'bairro', 'ano'], how='left')
    df[categoria] = df[categoria].fillna(0)
    df['ano'] = df['ano'].astype(str)
    return df

def carrega_causas_evitaveis_raca(caminho, categoria):
    """Lê um export Tabnet de causas evitáveis por raça/cor (nível município), em formato largo
    (ano nas colunas), e retorna em formato longo (raca, ano, categoria)."""
    df = pd.read_csv(caminho, sep=';', encoding='latin-1')
    df = df.rename(columns={df.columns[0]: 'raca'})
    df['raca'] = df['raca'].str.strip()
    df = df[df['raca'].isin(['Branca','Preta','Amarela','Parda','Indígena','Ignorado'])]
    df = df.drop(columns=['Total'])
    df = df.melt(id_vars=['raca'], var_name='ano', value_name=categoria)
    df[categoria] = df[categoria].replace('-', 0).astype(float)
    mapa_raca = {'Branca':'branca','Preta':'preta','Amarela':'amarela','Parda':'parda',
                 'Indígena':'indigena','Ignorado':'nao_informado'}
    df['raca'] = df['raca'].map(mapa_raca)
    return df

def carrega_causas_evitaveis_categoria(caminho, padrao):
    """Lê um export Tabnet 'segundo causas' (hierarquia grupo/subgrupo/causa, nível município)
    e filtra as linhas cujo rótulo bate com `padrao` (grupo ou subgrupo)."""
    df = pd.read_csv(caminho, sep=';', encoding='latin-1')
    df = df.rename(columns={df.columns[0]: 'causa'})
    df = df[df['causa'].notna()]
    df = df[df['causa'].str.match(padrao)]
    df = df.drop(columns=['Total'])
    df = df.melt(id_vars=['causa'], var_name='ano', value_name='obitos')
    df['obitos'] = df['obitos'].replace('-', 0).astype(float)
    df['ano'] = df['ano'].astype(int)
    return df

def combina_faixas_causa(padrao, arquivos_por_faixa):
    """Aplica `carrega_causas_evitaveis_categoria` a cada faixa etária em `arquivos_por_faixa`
    e soma o resultado por causa/ano (usado para obter o total 0-364 dias)."""
    df_total = None
    for caminho in arquivos_por_faixa.values():
        df_faixa = carrega_causas_evitaveis_categoria(caminho, padrao)
        df_total = df_faixa if df_total is None else pd.concat([df_total, df_faixa])
    return df_total.groupby(['causa','ano'], as_index=False)['obitos'].sum()

def total_e_percentual_ano(df):
    """Agrega um Censo (Tabela 2974/IBGE) por bairro em total e percentual de 0 a 4 anos."""
    df['0 a 4 anos'] = df['Sexo feminino, 0 a 4 anos'] + df['Sexo masculino, 0 a 4 anos']
    df['Total'] = df.iloc[:,9:].sum(axis=1)
    df['Percentual 0 a 4 anos'] = (df['0 a 4 anos']/df['Total'])
    return df[['bairro','0 a 4 anos','Percentual 0 a 4 anos','Sexo feminino, 0 a 4 anos','Sexo masculino, 0 a 4 anos']]

def carrega_cobertura_vacinal(caminho):
    """Lê um export do EPI/SVS-Rio de cobertura vacinal por imunobiológico e ano."""
    df = pd.read_csv(caminho, sep=';')
    df['ano_num'] = pd.to_numeric(df['ANO'], errors='coerce')
    df = df[df['ano_num'].notna()]
    df['ano'] = df['ano_num'].astype(int)
    df['cobertura'] = df['COBERTURA'].str.replace('%','',regex=False).str.replace(',','.',regex=False).astype(float)
    return df[['ano','IMUNO','cobertura']].rename(columns={'IMUNO':'imunobiologico'})

# %% [markdown]
# ### 📈 Funções de visualização
#
# Todas salvam o gráfico em `visualizacoes/` como PNG. A exportação adicional em SVG fica
# disponível, mas comentada, em cada função — descomente a linha `# plt.savefig(...svg...)`
# quando precisar de um formato vetorial.

# %%
def serie_temporal(df,tempo,valor,titulo,nome_arquivo=None, formato='png'):
    nome_arquivo = nome_arquivo or f"{valor}_{tempo}"
    plt.figure(figsize=(12,6))
    sns.lineplot(x=tempo,y=valor,data=df)
    plt.xlabel(tempo,fontsize=12)
    plt.ylabel(valor,fontsize=12)
    plt.title(titulo,fontsize=14)
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}")
    # plt.savefig(f"visualizacoes/{nome_arquivo}.svg")  # descomente para exportar também em SVG
    plt.show()

def grafico_barra(df,categoria,valor,titulo,nome_arquivo=None, formato='png'):
    nome_arquivo = nome_arquivo or f"{valor}_{categoria}"
    plt.figure(figsize=(10,6))
    sns.barplot(x=categoria,y=valor,data=df,palette='pastel',hue=categoria)
    plt.xlabel(categoria,fontsize=12)
    plt.ylabel(valor, fontsize=12)
    plt.title(titulo,fontsize=14)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}")
    # plt.savefig(f"visualizacoes/{nome_arquivo}.svg")  # descomente para exportar também em SVG
    plt.show()

def grafico_barra_agrupado(df,categoria,valor,agrupador,titulo,nome_arquivo,ylabel=None,legend_title=None,ordem_categoria=None,ordem_agrupador=None,rotacao_x=30,figsize=(12,7),formato='png'):
    plt.figure(figsize=figsize)
    sns.barplot(data=df, x=categoria, y=valor, hue=agrupador, order=ordem_categoria, hue_order=ordem_agrupador)
    plt.xlabel(categoria,fontsize=12)
    plt.ylabel(ylabel or valor, fontsize=12)
    plt.title(titulo,fontsize=14)
    plt.xticks(rotation=rotacao_x, ha='right' if rotacao_x else 'center')
    plt.legend(title=legend_title or agrupador, fontsize=9)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}")
    # plt.savefig(f"visualizacoes/{nome_arquivo}.svg")  # descomente para exportar também em SVG
    plt.show()

def serie_temporal_multipla(df,tempo,colunas,titulo,nome_arquivo,ylabel='Valor',legend_title='Cor/Raça',figsize=(12,6),formato='png'):
    plt.figure(figsize=figsize)
    for rotulo,coluna in colunas.items():
        sns.lineplot(x=tempo,y=coluna,data=df,label=rotulo,marker='o',errorbar=None)
    plt.xlabel(tempo,fontsize=12)
    plt.ylabel(ylabel,fontsize=12)
    plt.title(titulo,fontsize=14)
    plt.legend(title=legend_title,fontsize=9)
    plt.grid(True,alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}")
    # plt.savefig(f"visualizacoes/{nome_arquivo}.svg")  # descomente para exportar também em SVG
    plt.show()

def _numero_ptbr(n):
    """Formata um número inteiro com separador de milhar no padrão brasileiro (ex.: 10000 -> '10.000')."""
    return f"{n:,.0f}".replace(",", ".")

# basemap cartográfico/'desenho' (sem satélite -- descartado; ver generate_map skill para o porquê):
# relevo suave, sem rótulos de municípios vizinhos, mar em azul. max_zoom 13 (suficiente na escala do município).
_PROVEDORES_FUNDO = {
    'mapa': ctx.providers.Esri.OceanBasemap,
}

# nível de agregação geográfica: coluna do geojson de bairros usada no dissolve/join, e o tipo para
# comparação (Área de Planejamento e codbairro são numéricos; Região de Planejamento é 'AP.subregião',
# ex. '4.2', e não pode virar número sem perder precisão)
_NIVEIS_AGREGACAO = {
    'bairro': {'coluna_geo': 'codbairro', 'tipo': int},
    'ap':     {'coluna_geo': 'area_plane', 'tipo': int},
    'rp':     {'coluna_geo': 'cod_rp', 'tipo': str},
}

_FONTE_TITULO = 'Palatino Linotype'  # serifada, estilo de publicação acadêmica

# canto reservado para a legenda/colorbar (sempre 'upper left'), em fração dos eixos (0-1) -- um
# rótulo de município vizinho que caia aqui seria sobreposto pela legenda, então é descartado
_ZONA_LEGENDA = (0.0, 0.46, 0.34, 1.0)  # (x0, y0, x1, y1)

def _adiciona_rosa_dos_ventos(ax, x=0.94, y=0.90, tamanho=0.05, cor='#262626'):
    """Desenha uma seta 'N' simples (rosa dos ventos) no canto superior direito do mapa."""
    ax.annotate(
        'N', xy=(x, y), xytext=(x, y - tamanho),
        xycoords=ax.transAxes, textcoords=ax.transAxes,
        ha='center', va='center', fontsize=15, fontweight='bold', color=cor,
        arrowprops=dict(arrowstyle='-|>', color=cor, lw=2.0, mutation_scale=24),
        zorder=5,
    )

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
                              cmap='Oranges', legenda_titulo=None, fundo='mapa', alpha=None, fonte_dados=None,
                              caminho_geojson='dados_locais/geo/limite_bairros_rio.geojson',
                              caminho_uf='dados_locais/geo/limite_uf_brasil.geojson',
                              caminho_municipios='dados_locais/geo/limite_municipios_rj.geojson', formato='png'):
    """Gera um mapa coroplético do Rio (limites IPP/Data.Rio, simplificados) e salva em mapas/.

    `nivel`: 'bairro' (padrão) | 'ap' (Área de Planejamento, 5 regiões) | 'rp' (Região de
    Planejamento, 16 regiões) -- une (`dissolve`) os polígonos de bairro nesse nível antes do join
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
        gdf['faixa'] = pd.cut(gdf[coluna_valor], bins=limites, labels=rotulos, ordered=True)
        gdf.plot(
            column='faixa', ax=ax, cmap=cmap, linewidth=0.4, edgecolor='#616161', legend=True, alpha=alpha,
            zorder=2, missing_kwds=missing_kwds,
            legend_kwds={'title': legenda_titulo or coluna_valor, 'loc': 'upper left', 'fontsize': 10,
                         'title_fontsize': 12, 'framealpha': 0.92, 'facecolor': 'white', 'edgecolor': '#c9c9c9',
                         'labelcolor': '#111111'},
        )
        legenda = ax.get_legend()
        legenda.get_title().set_fontweight('bold')
        for texto in legenda.get_texts():
            texto.set_fontweight('semibold')
    else:
        # colorbar como inset dentro da própria área do mapa (não numa coluna externa) -- mesmo canto
        # que a legenda de classes usaria, já que os dois modos são mutuamente exclusivos numa chamada;
        # deslocada para perto do topo (y0=0,60) para ficar mais sobre a margem de contexto (fora dos
        # bairros) do que sobre os próprios polígonos coloridos. Isso sozinho não bastava: os rótulos
        # dos ticks e o texto do eixo (rotacionado) ficam FORA da própria cax (na margem dela), então
        # não herdam nenhum fundo opaco -- diferente da legenda de classes, que já tem uma caixa
        # branca própria (framealpha/facecolor). Por isso um retângulo branco é desenhado por baixo,
        # cobrindo a barra + ticks + rótulo do eixo, para o texto continuar legível não importa sobre
        # qual parte do mapa a colorbar caia.
        cax_x0, cax_y0, cax_largura, cax_altura = 0.035, 0.60, 0.03, 0.30
        ax.add_patch(plt.Rectangle(
            (cax_x0 - 0.02, cax_y0 - 0.025), 0.175, cax_altura + 0.05,
            transform=ax.transAxes, facecolor='white', edgecolor='#c9c9c9', alpha=0.88, zorder=2.5,
        ))
        cax = ax.inset_axes([cax_x0, cax_y0, cax_largura, cax_altura])
        gdf.plot(
            column=coluna_valor, ax=ax, cmap=cmap, linewidth=0.4, edgecolor='#616161', legend=True, alpha=alpha,
            zorder=2, missing_kwds=missing_kwds, cax=cax,
            legend_kwds={'label': legenda_titulo or coluna_valor},
        )
        cax.tick_params(labelsize=9, colors='#111111')
        for rotulo in cax.get_yticklabels():
            rotulo.set_fontweight('semibold')
        cax.yaxis.label.set_size(11)
        cax.yaxis.label.set_color('#111111')
        cax.yaxis.label.set_fontweight('bold')

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
    texto_referencia = ('Sistema de referência: SIRGAS 2000 (dados) | Web Mercator EPSG:3857 (mapa)'
                         if usa_fundo else 'Sistema de referência: SIRGAS 2000 (EPSG:4326)')
    rodape = texto_referencia if not fonte_dados else f"{texto_referencia}\nFonte: {fonte_dados}"
    ax.annotate(
        rodape, xy=(0.62, 0.012), xycoords='axes fraction', ha='center', va='bottom',
        fontsize=6.5, color='#262626', zorder=6,
        bbox=dict(boxstyle='square,pad=0.35', facecolor='white', alpha=0.8, edgecolor='none'),
    )

    ax.set_title(titulo, fontsize=22, pad=14, fontfamily=_FONTE_TITULO, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f"mapas/{nome_arquivo}.{formato}", dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.show()

# %% [markdown]
# ### ⚙️ Setup

# %%
#carrega variáveis de ambiente
load_dotenv()

#garante que as pastas de saída padrão existam (inclusive a subpasta de tabelas por bairro)
for pasta in ["tabelas_finais", "visualizacoes", "mapas/tabelas_bairros", "dados_locais/tratados"]:
    Path(pasta).mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ### 🧼 Limpeza de dados prévia

# %%
limpa_dados_sisvan(colunas=['magreza_acentuada','magreza','eutrofia','risco sobrepeso','sobrepeso','obesidade','total'], dataset='sobrepeso')
limpa_dados_sisvan(colunas=['peso_muito_baixo','peso_baixo','peso_adequado','peso_elevado','total'], dataset='desnutrição')

# %% [markdown]
# ---
# ## 🧭 Visualização dos Dados (entregáveis dia 12 & 19)

# %% [markdown]
# <p>Para acesso aos dados brutos via Drive: https://drive.google.com/drive/folders/1xOwf72QfaDuJAHuA-Vngl6t5_kzSfGYX?usp=sharing</p>
# <p>OBS: acesso restrito, solicitar a leonardo.aucar@prefeitura.rio</p>

# %% [markdown]
# ### 🏘️ Censo 2022(10/00)

# %% [markdown]
# Dados do Censo IBGE 2022 (agregados DataRio), população por bairro e faixa etária.

# %% [markdown]
# #### Por bairro

# %%
## dados censo
df_censo = pd.read_csv("dados_locais\\censo\\pop_censo_2022_datario.csv", encoding='Latin-1', sep=';')
df_censo.head()

# %%
df_censo['Total'] = df_censo[['0 a 4 anos', '5 a 9 anos',
       '10 a 14 anos', '15 a 19 anos', '20 a 24 anos', '25 a 29 anos',
       '30 a 39 anos', '40 a 49 anos', '50 a 59 anos', '60 a 69 anos',
       '70 anos ou mais']].sum(axis=1)

# %%
print(f'Crianças de 0 a 4 anos em 2022: {df_censo['0 a 4 anos'].sum()}')
print(f'Crianças de 5 a 9 anos em 2022: {df_censo['5 a 9 anos'].sum()}')

# %%
df_censo['Percentual 0 a 4'] = (df_censo['0 a 4 anos']/df_censo['Total'])*100
df_censo['Percentual 5 a 9'] = (df_censo['5 a 9 anos']/df_censo['Total'])*100

# %%
df_censo[['bairro','codbairro','0 a 4 anos','Percentual 0 a 4','5 a 9 anos','Percentual 5 a 9']].sort_values(by='0 a 4 anos',ascending=False).to_csv('tabelas_finais\\censo_por_bairro.csv')

# %%
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False)
#mapa por total de 0 a 4 anos
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).to_excel('mapas/tabelas_bairros/tabela_mapa_0_4_absoluto.xlsx')

# %%
df_censo[['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).head(10)

# %%
# para bairros 'muito grandes' (+100.000 pessoas)
df_censo.loc[df_censo['Total'] > 20000,['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False)
#mapa por percentual dos bairros grandes
df_censo.loc[df_censo['Total'] > 20000,['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).to_excel('mapas/tabelas_bairros/tabela_mapa_grandes_0_4_percentual.xlsx')

# %%
df_censo.loc[df_censo['Total'] > 20000,['bairro','0 a 4 anos','Percentual 0 a 4']].sort_values(by='Percentual 0 a 4',ascending=False).head(20)

# %% [markdown]
# #### 🗺️ Mapa coroplético (bairros)
#
# Mapas coropléticos de crianças de 0 a 4 anos por bairro (Censo 2022), a partir de
# `tabelas_finais/censo_por_bairro.csv`. O join com a geometria dos bairros usa `codbairro`
# (código oficial IPP/Data.Rio), não o nome do bairro -- mais robusto a variações de grafia
# entre fontes. Limites de bairro em `dados_locais/geo/limite_bairros_rio.geojson`
# (Data.Rio, camada `Cartografia/Limites_administrativos`, geometria simplificada).
# Faixas do mapa absoluto seguem o padrão de `mapas/mapa_referencia.jpeg`, para comparação.
#
# Fundo cartográfico/'desenho' via Esri Ocean Basemap (parâmetro `fundo='mapa'` de
# `mapa_coropletico_bairros`, o padrão da função): relevo suave, mar em azul, sem nomes de
# municípios vizinhos. Os limites estaduais (UF, fonte IBGE,
# `dados_locais/geo/limite_uf_brasil.geojson`) do entorno aparecem em amarelo tracejado, a vista é
# ampliada além dos bairros para dar contexto (região metropolitana, baía, mar), e o mapa traz rosa
# dos ventos e escala gráfica. Exportado a 300 DPI, em formato largo.

# %%
df_mapa_censo = pd.read_csv('tabelas_finais\\censo_por_bairro.csv')

fonte_censo = 'Censo Demográfico 2022 (IBGE/Data.Rio)'

mapa_coropletico_bairros(
    df_mapa_censo, coluna_valor='0 a 4 anos',
    titulo='Crianças de 0 a 4 anos de idade, por bairro (Censo 2022)',
    nome_arquivo='mapa_censo_0_4_absoluto',
    bins=[1000, 2500, 5000, 10000],
    legenda_titulo='Crianças 0-4 anos',
    fonte_dados=fonte_censo,
)

# %%
mapa_coropletico_bairros(
    df_mapa_censo, coluna_valor='Percentual 0 a 4',
    titulo='Percentual de crianças de 0 a 4 anos, por bairro (Censo 2022)',
    nome_arquivo='mapa_censo_0_4_percentual',
    legenda_titulo='% da população do bairro',
    fonte_dados=fonte_censo,
)

# %% [markdown]
# #### 🗺️ Versões alternativas: por Área e por Região de Planejamento
#
# Mesmos dados, agregados para os dois níveis de planejamento acima do bairro (`agrega_bairros_por_nivel`
# soma as contagens por bairro; o percentual é recalculado a partir das somas, não pela média das taxas
# por bairro, para não distorcer o resultado entre bairros de tamanhos muito diferentes): as 5 Áreas de
# Planejamento (AP) e as 16 Regiões de Planejamento (RP) do IPP/Data.Rio, ambas já presentes no geojson
# de bairros (`area_plane`, `cod_rp`) e unidas (`dissolve`) por `mapa_coropletico_bairros` via `nivel`.

# %%
# classes discretas por nível -- faixas de valor bem diferentes entre AP (5 regiões grandes) e RP
# (16 regiões menores), então cada nível tem seus próprios limites (não dá pra reaproveitar os do
# bairro); percentuais continuam em escala contínua (não fazem sentido em classes fixas aqui, com só
# 5/16 unidades)
niveis_planejamento = {
    'ap': {'nome': 'Área de Planejamento', 'bins': [25000, 50000, 75000, 100000]},
    'rp': {'nome': 'Região de Planejamento', 'bins': [12000, 18000, 24000, 30000]},
}

for nivel, info in niveis_planejamento.items():
    df_censo_nivel = agrega_bairros_por_nivel(df_censo, nivel, colunas_soma=['0 a 4 anos', 'Total'])
    df_censo_nivel['Percentual 0 a 4'] = (df_censo_nivel['0 a 4 anos'] / df_censo_nivel['Total']) * 100

    mapa_coropletico_bairros(
        df_censo_nivel, coluna_valor='0 a 4 anos', nivel=nivel,
        titulo=f'Crianças de 0 a 4 anos de idade, por {info["nome"]} (Censo 2022)',
        nome_arquivo=f'mapa_censo_0_4_absoluto_{nivel}',
        bins=info['bins'],
        legenda_titulo='Crianças 0-4 anos',
        fonte_dados=fonte_censo,
    )
    mapa_coropletico_bairros(
        df_censo_nivel, coluna_valor='Percentual 0 a 4', nivel=nivel,
        titulo=f'Percentual de crianças de 0 a 4 anos, por {info["nome"]} (Censo 2022)',
        nome_arquivo=f'mapa_censo_0_4_percentual_{nivel}',
        legenda_titulo='% da população',
        fonte_dados=fonte_censo,
    )

# %% [markdown]
# #### Serie temporal censo

# %% [markdown]
# Evolução da população de 0 a 4 anos entre os Censos 2000, 2010 e 2022 (Tabela 2974/IBGE), agregada para o município.

# %%
df_2000 = pd.read_csv('dados_locais\\censo\\tabela 2974_2000.csv', sep=';')
df_2010 = pd.read_csv('dados_locais\\censo\\tabela 2974_2010.csv', sep=';')
df_2022 = pd.read_csv('dados_locais\\censo\\tabela 2974_2022.csv', sep=';')

df_serie_censo = pd.DataFrame(columns=['bairro','ano','0 a 4 anos','Percentual 0 a 4 anos','Sexo feminino, 0 a 4 anos','Sexo masculino, 0 a 4 anos'])
for i in [[df_2000,'2000'],[df_2010,'2010'],[df_2022,'2022']]:
    df = total_e_percentual_ano(i[0])
    df['ano'] = i[1]
    df_serie_censo = pd.concat([df_serie_censo,df])

df_serie_censo=df_serie_censo[['ano','0 a 4 anos', 'Percentual 0 a 4 anos','Sexo feminino, 0 a 4 anos','Sexo masculino, 0 a 4 anos']].groupby(by='ano').sum()
df_serie_censo.to_csv('tabelas_finais//censo_0_a_4_anos_por_ano.csv')

# %%
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_serie_censo, x='ano', y='0 a 4 anos', label='Total 0 a 4 anos', marker='o', errorbar=None)
sns.lineplot(data=df_serie_censo, x='ano', y='Sexo feminino, 0 a 4 anos', label='Sexo Feminino', marker='o', errorbar=None)
sns.lineplot(data=df_serie_censo, x='ano', y='Sexo masculino, 0 a 4 anos', label='Sexo Masculino', marker='o', errorbar=None)
#sns.lineplot(data=df_serie_censo, x='ano', y='Percentual 0 a 4 anos', label='Percentual 0 a 4 anos', marker='o')

# Customize the plot
plt.title('Série Temporal: Crianças 0 a 4 anos', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Valores', fontsize=10)
plt.legend(title='Indicadores', fontsize=10)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# %%
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_serie_censo, x='ano', y='Percentual 0 a 4 anos', label='Percentual 0 a 4 anos', marker='o', errorbar=None)

# Customize the plot
plt.title('Série Temporal: Crianças 0 a 4 anos', fontsize=16)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Valores', fontsize=12)
plt.legend(title='Indicadores', fontsize=10)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

# %% [markdown]
# ##### Pendente: Censo 2022 por idade e raça/cor (0 a 6 anos, cidade toda)

# %% [markdown]
# ### 🗂️ Cadúnico

# %% [markdown]
# Fonte: CadÚnico via banco CTPE (`silver_cadunico_geral`), recorte de crianças 0-6 anos.
#
# > **Nota:** requer conexão ativa com o banco CTPE (credenciais em `.env`) para reproduzir; não roda apenas com os arquivos em `dados_locais/`.

# %% [markdown]
# #### Recorte 0-6 anos

# %%
#Banco CTPE
engine = connect_db_ctpe()
df_original = pd.read_sql("SELECT * FROM silver_cadunico_geral WHERE grupo_idade='0-6'", engine)
df =  df_original.copy()
df_original

# %%
df = df.rename(columns={'id_pessoa':'Crianças','id_familia':'Famílias','grupo_renda_pct':'faixa de renda'})

# %%
df_bairro = pd.read_csv('dados_locais\\lista_bairros.csv', dtype={'cep': str})
df['cep'] = df['cep'].astype(str)

# 2. Faz o JOIN (Merge) trazendo apenas a coluna 'bairros' baseada no 'cep'
df = df.merge(df_bairro[['cep', 'bairro']], on='cep', how='left')

# %% [markdown]
# #### Análise por renda

# %%
#quantitativos por grupo de renda pct
df_renda = df.groupby(by='faixa de renda').agg({'Crianças':'count','Famílias':'nunique'})
df_renda.loc['Total'] = df_renda.sum()
custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
df_renda = df_renda.reindex(custom_order)
df_renda.to_csv('tabelas_finais\\cadunico_por_faixa_etaria_2026.csv')

# %%
df_renda.head(10)

# %%
grafico_barra(df_renda.iloc[:-1,:],categoria='faixa de renda',valor='Famílias',
              titulo='CADÚNICO: Famílias c/crianças 0-6 por faixa de renda per capita',
              nome_arquivo='cadunico_familias_por_faixa_renda')

# %%
grafico_barra(df_renda.iloc[:-1,:],categoria='faixa de renda',valor='Crianças',
              titulo='CADÚNICO: Crianças 0-6 por faixa de renda per capita',
              nome_arquivo='cadunico_criancas_por_faixa_renda')

# %% [markdown]
# #### Análise por idade

# %%
#quantitativos por idade
df #fazer one hot da coluna sexo
df_idade = df.groupby(by='idade').agg({'Crianças':'count','Famílias':'nunique'})#,'sexo_m':'sum','sexo_f':'sum'})
df_idade.to_csv('tabelas_finais\\cadunico_por_idade_2026.csv')
df_idade.head(10)


# %%
grafico_barra(df_idade,categoria='idade',valor='Famílias', titulo='CADÚNICO: Famílias c/ crianças 0-6 por idade',
              nome_arquivo='cadunico_familias_por_idade')

# %%
grafico_barra(df_idade,categoria='idade',valor='Crianças', titulo='CADÚNICO: Crianças 0-6 por idade',
              nome_arquivo='cadunico_criancas_por_idade')

# %% [markdown]
# #### Análise por bairros

# %%
#quantitativos por grupo de renda pct
df_bairro = df.groupby(by=['bairro']).agg({'Crianças':'count','Famílias':'nunique'})
df_bairro.loc['Total'] = df_bairro.sum()
#custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
#df_bairro = df_bairro.reindex(custom_order)
df_bairro.to_csv('tabelas_finais\\cadunico_por_bairro_2026.csv')

# %%
df_bairro.sort_values(by='Crianças', ascending=False).head(10)
# ADICIONAR NOTA SOBRE IDENTIFICACAO DE BAIRROS

# %%
df_bairro.sort_values(by='Primeira Inf. Cadúnico', ascending=True).head(10)

# %%
#quantitativos por grupo de renda pct
df_ate_4 = df[df['idade']<5].copy()
df_bairro_ate_4 = df_ate_4.groupby(by=['bairro']).agg({'Crianças':'count','Famílias':'nunique'})
df_bairro_ate_4.loc['Total'] = df_bairro_ate_4.sum()
#custom_order = ['0-218','219-810','811-1621','1621-3242','3242+','Total']
#df_bairro = df_bairro.reindex(custom_order)
df_bairro_ate_4.to_csv('tabelas_finais\\cadunico_por_bairro_2026.csv')
df_bairro_ate_4 = df_bairro_ate_4.merge(df_censo[['bairro','0 a 4 anos']], on='bairro', how='right')
df_bairro_ate_4['Primeira Inf. Cadúnico'] = df_bairro_ate_4['Crianças']/df_bairro_ate_4['0 a 4 anos']
df_bairro_ate_4.sort_values(by='Crianças', ascending=False).head(10)

# %%
df_bairro[df_bairro['bairro']=='Complexo do Alemão']


# %% [markdown]
# ### 🏥 DataSus - tabnet

# %% [markdown]
# Séries do Datasus/Tabnet (nascidos vivos e óbitos), por bairro de residência, padronizadas pela função `limpeza_tabnet_bairros`.

# %% [markdown]
# #### Nascidos Vivos

# %% [markdown]
# Nascidos vivos totais por bairro (2006-2025).

# %%
#Nascidos vivos
df_vivos = pd.read_csv("dados_locais\\mortalidade\\nascidos_vivos_bairros_2006_a_2025.csv")
df_vivos = limpa_dados_datasus(df_vivos)
df_vivos = limpeza_tabnet_bairros(df_vivos,categoria='nascidos vivos')
df_vivos.head()


# %%
#extracao para mapas
df_vivos[df_vivos['ano']=='2025'].to_excel('mapas/tabelas_bairros/mapa_bairros_nascidos_vivos_bruto.xlsx')

# %%
#agrupamento por ano
df_vivos_por_ano = df_vivos.loc[:,['ano','nascidos vivos']].groupby(by='ano').sum()
df_vivos_por_ano.reset_index(inplace=True)
df_vivos_por_ano.rename({'variable':'ano','value':'nascidos vivos'},axis=1, inplace=True)
print(df_vivos_por_ano.head(25))
df_vivos_por_ano.to_csv('tabelas_finais\\nascidos_vivos_por_ano.csv')

# %%
serie_temporal(df_vivos_por_ano,tempo='ano',valor='nascidos vivos', titulo='Nascidos vivos por ano',
               nome_arquivo='nascidos_vivos_por_ano')

# %% [markdown]
# #### Nascidos abaixo peso

# %% [markdown]
# Nascidos vivos com baixo peso (&lt;2.500g) por bairro, como percentual dos nascidos vivos totais.

# %%
#Nascidos abaixo do peso
df_baixo_peso = pd.read_csv("dados_locais\\mortalidade\\nascidos_vivos_baixo_peso_ao_nascer_bairros_2006_a_2025.csv")
df_baixo_peso = limpa_dados_datasus(df_baixo_peso)
df_baixo_peso = limpeza_tabnet_bairros(df_baixo_peso,categoria='nascidos abaixo peso')
df_baixo_peso.head()

# %%
df_baixo_peso['percentual abaixo do peso'] = (df_baixo_peso['nascidos abaixo peso']/df_vivos['nascidos vivos'])*100
df_baixo_peso[df_baixo_peso['ano']=='2025'].to_excel('mapas/tabelas_bairros/mapa_bairros_nascidos_abaixo_peso.xlsx')

# %%
df_baixo_ano = df_baixo_peso.loc[:,['ano','nascidos abaixo peso']].groupby(by='ano').sum()
df_baixo_ano.reset_index(inplace=True)
df_baixo_ano['percentual abaixo do peso'] = (df_baixo_ano['nascidos abaixo peso']/df_vivos_por_ano['nascidos vivos'])*100
df_baixo_ano.to_csv('tabelas_finais\\nascidos_abaixo_peso_por_ano.csv')
df_baixo_ano.head(25)

# %%
serie_temporal(df_baixo_ano,tempo='ano',valor='percentual abaixo do peso', titulo='Percentual Nascidos com baixo peso por ano',
               nome_arquivo='nascidos_abaixo_peso_percentual_por_ano')

# %% [markdown]
# #### 📉 Mortalidade

# %% [markdown]
# Óbitos até 1 ano de idade: por raça/cor, causas evitáveis, gravidez/puerpério e mortalidade neonatal (precoce, tardia, pós-neonatal e total).

# %% [markdown]
# ##### Óbitos até 1 ano por raça/cor

# %% [markdown]
# Combina os óbitos de menores de 1 ano (0 a 364 dias) por raça/cor (2006-2025) com os nascidos vivos por raça/cor da mãe (2011-2025), ambos por bairro de residência.
#
# Notas:
# - Colunas de ano ausentes nos arquivos do Tabnet indicam total 0 no período e são preenchidas com 0 na limpeza.
# - As categorias `Ignorado` e `Não informado` de nascidos vivos representam a mesma informação ausente, registrada sob nomes diferentes ao longo da série -> somadas em `nascidos_nao_informado`.
# - O percentual de óbitos por raça só é calculável a partir de 2011, quando começa a série de nascidos vivos por raça/cor da mãe.
# - Óbitos e nascidos vivos por raça vêm de consultas independentes do Datasus (óbito de residente x nascimento registrado no bairro) -> em bairros/anos com poucos casos é possível ter óbitos de uma raça sem nascidos vivos correspondentes, gerando percentuais instáveis ou indefinidos (tratados como NaN). Afeta principalmente `indigena`, `amarela` e `nao_informado`, categorias com poucas observações.

# %%
racas = ['amarela','branca','indigena','parda','preta','nao_informado']
arquivos_obitos = {'amarela':'amarelos','branca':'brancos','indigena':'indigenas',
                    'parda':'pardos','preta':'pretos','nao_informado':'nao_informado'}
anos_obitos = list(range(2006, 2026))

df_obitos_raca = None
for raca in racas:
    caminho = f'dados_locais//mortalidade//obitos_0_364_dias_{arquivos_obitos[raca]}_bairro_2006_2025.csv'
    df_raca = carrega_raca_bairro(caminho, categoria=f'obitos_{raca}', anos_validos=anos_obitos)
    df_obitos_raca = df_raca if df_obitos_raca is None else df_obitos_raca.merge(df_raca, on=['codigo','bairro','ano'], how='outer')

colunas_obitos = [f'obitos_{raca}' for raca in racas]
df_obitos_raca[colunas_obitos] = df_obitos_raca[colunas_obitos].fillna(0)
df_obitos_raca.head()

# %%
arquivos_nascidos = {'amarela':'mae_amarela','branca':'mae_branca','indigena':'mae_indigena',
                      'parda':'mae_parda','preta':'mae_preta'}
anos_nascidos = list(range(2011, 2026))

df_nascidos_raca = None
for raca, arquivo in arquivos_nascidos.items():
    caminho = f'dados_locais//mortalidade//nascidos_vivos_{arquivo}_bairro_2011_2025.csv'
    df_raca = carrega_raca_bairro(caminho, categoria=f'nascidos_{raca}', anos_validos=anos_nascidos)
    df_nascidos_raca = df_raca if df_nascidos_raca is None else df_nascidos_raca.merge(df_raca, on=['codigo','bairro','ano'], how='outer')

# 'Ignorado' e 'Não informado' são a mesma mãe sem raça/cor registrada (o Datasus mudou a
# nomenclatura ao longo da série) -> soma em uma única coluna nascidos_nao_informado
for arquivo in ['mae_ignorado','mae_nao_informado']:
    caminho = f'dados_locais//mortalidade//nascidos_vivos_{arquivo}_bairro_2011_2025.csv'
    df_raca = carrega_raca_bairro(caminho, categoria=arquivo, anos_validos=anos_nascidos)
    df_nascidos_raca = df_nascidos_raca.merge(df_raca, on=['codigo','bairro','ano'], how='outer')

colunas_nascidos = [f'nascidos_{raca}' for raca in arquivos_nascidos] + ['mae_ignorado','mae_nao_informado']
df_nascidos_raca[colunas_nascidos] = df_nascidos_raca[colunas_nascidos].fillna(0)
df_nascidos_raca['nascidos_nao_informado'] = df_nascidos_raca['mae_ignorado'] + df_nascidos_raca['mae_nao_informado']
df_nascidos_raca.drop(columns=['mae_ignorado','mae_nao_informado'], inplace=True)
df_nascidos_raca.head()

# %%
df_mortalidade_raca_bairro = df_obitos_raca.merge(df_nascidos_raca, on=['codigo','bairro','ano'], how='outer')

colunas_obitos = [f'obitos_{raca}' for raca in racas]
colunas_nascidos = [f'nascidos_{raca}' for raca in racas]
df_mortalidade_raca_bairro[colunas_obitos] = df_mortalidade_raca_bairro[colunas_obitos].fillna(0)

# nascidos vivos por raça só existe a partir de 2011: mantém NaN antes disso e preenche com 0
# quando o ano está no período coberto mas a combinação bairro/raça não teve registro
periodo_com_nascidos = df_mortalidade_raca_bairro['ano'].astype(int) >= 2011
df_mortalidade_raca_bairro.loc[periodo_com_nascidos, colunas_nascidos] = (
    df_mortalidade_raca_bairro.loc[periodo_com_nascidos, colunas_nascidos].fillna(0)
)

for raca in racas:
    percentual = (df_mortalidade_raca_bairro[f'obitos_{raca}'] / df_mortalidade_raca_bairro[f'nascidos_{raca}']) * 100
    df_mortalidade_raca_bairro[f'percentual_{raca}'] = percentual.replace([float('inf'), -float('inf')], float('nan')).round(2)

df_mortalidade_raca_bairro = df_mortalidade_raca_bairro.sort_values(by=['ano','bairro']).reset_index(drop=True)
df_mortalidade_raca_bairro.to_csv('dados_locais//tratados//mortalidade_raca_bairro_ano.csv', index=False)
df_mortalidade_raca_bairro.head()

# %%
# agrega bairro -> município (todos os bairros pertencem ao município do Rio de Janeiro)
df_mortalidade_raca_municipio = (
    df_mortalidade_raca_bairro.groupby('ano')[colunas_obitos + colunas_nascidos]
    .sum(min_count=1)
    .reset_index()
)
df_mortalidade_raca_municipio['ano'] = df_mortalidade_raca_municipio['ano'].astype(int)
df_mortalidade_raca_municipio.sort_values(by='ano', inplace=True)

for raca in racas:
    percentual = (df_mortalidade_raca_municipio[f'obitos_{raca}'] / df_mortalidade_raca_municipio[f'nascidos_{raca}']) * 100
    df_mortalidade_raca_municipio[f'percentual_{raca}'] = percentual.replace([float('inf'), -float('inf')], float('nan')).round(2)

df_mortalidade_raca_municipio.to_csv('dados_locais//tratados//mortalidade_raca_municipio_ano.csv', index=False)
df_mortalidade_raca_municipio.to_csv('tabelas_finais//mortalidade_raca_municipio_ano.csv', index=False)
df_mortalidade_raca_municipio

# %%
rotulos_raca = {'Amarela':'amarela','Branca':'branca','Indígena':'indigena',
                 'Parda':'parda','Preta':'preta','Não informada':'nao_informado'}

serie_temporal_multipla(
    df_mortalidade_raca_municipio,
    tempo='ano',
    colunas={rotulo: f'obitos_{raca}' for rotulo, raca in rotulos_raca.items()},
    titulo='Óbitos de 0 a 364 dias por raça/cor - Rio de Janeiro (2006-2025)',
    nome_arquivo='obitos_raca_ano',
    ylabel='Óbitos'
)

# %%
# percentual só existe a partir de 2011 (início da série de nascidos vivos por raça/cor da mãe)
df_percentual_raca_municipio = df_mortalidade_raca_municipio[df_mortalidade_raca_municipio['ano'] >= 2011]

serie_temporal_multipla(
    df_percentual_raca_municipio,
    tempo='ano',
    colunas={rotulo: f'percentual_{raca}' for rotulo, raca in rotulos_raca.items()},
    titulo='Percentual de óbitos (0-364 dias) em relação aos nascidos vivos por raça/cor - Rio de Janeiro (2011-2025)',
    nome_arquivo='percentual_mortalidade_raca_ano',
    ylabel='Percentual (%)'
)

# %%
## Retirar não informados do gráfico de percentual

# %% [markdown]
# ##### Óbitos por causas evitáveis por raça/cor

# %% [markdown]
# Óbitos por causas evitáveis (0 a 364 dias, somando as faixas 0-6, 7-27 e 28-364 dias) por raça/cor (1996-2025), comparados aos nascidos vivos por raça/cor da mãe (2011-2025).
#
# Notas:
# - O Datasus só disponibiliza o cruzamento causas evitáveis x raça/cor no nível de município, não por bairro -> esta tabela tem granularidade município-ano (sem versão por bairro, ao contrário da seção anterior).
# - Valores marcados com `-` na fonte indicam 0 ocorrências e são convertidos para 0.
# - Assim como na série geral de óbitos por raça, o percentual só é calculável a partir de 2011.
# - **Atenção:** apesar do nome, este cruzamento por raça/cor não é filtrado só para causas evitáveis — o total por raça aqui fica entre 92% e 103% do total geral de óbitos por raça (seção anterior) na maior parte da série, só caindo mais claramente a partir de 2022. A quebra evitável / mal definida / demais causas só existe nos arquivos "segundo causas" (sem recorte por raça, próxima seção) -> os gráficos `percentual_mortalidade_raca_ano` e `percentual_mortalidade_causas_evitaveis_raca_ano` acabam sendo quase idênticos.
# - A categoria `nao_informado` tem um pico isolado em 1996 (2.136 óbitos, muito acima dos demais anos) por baixa completude do preenchimento de raça/cor no início da série -> não interpretar como aumento real de óbitos.

# %%
faixas_evitaveis = {
    '0_6': 'dados_locais//mortalidade//obitos_causas_evitaveis_0_6_dias_cor_raca_municipio_1996_2025.csv',
    '7_27': 'dados_locais//mortalidade//obitos_causas_evitaveis_7_27_dias_cor_raca_municipio_1996_2025.csv',
    '28_364': 'dados_locais//mortalidade//obitos_causas_evitaveis_28_364_dias_cor_raca_municipio_1996_2025.csv',
}

df_evitaveis_raca = None
for faixa, caminho in faixas_evitaveis.items():
    df_faixa = carrega_causas_evitaveis_raca(caminho, categoria='obitos')
    df_evitaveis_raca = df_faixa if df_evitaveis_raca is None else pd.concat([df_evitaveis_raca, df_faixa])

df_evitaveis_raca = df_evitaveis_raca.groupby(['raca','ano'], as_index=False)['obitos'].sum()

df_evitaveis_raca_municipio = df_evitaveis_raca.pivot(index='ano', columns='raca', values='obitos')
df_evitaveis_raca_municipio.columns = [f'obitos_evitaveis_{c}' for c in df_evitaveis_raca_municipio.columns]
df_evitaveis_raca_municipio = df_evitaveis_raca_municipio.reset_index()
df_evitaveis_raca_municipio['ano'] = df_evitaveis_raca_municipio['ano'].astype(int)
df_evitaveis_raca_municipio.sort_values(by='ano', inplace=True)
df_evitaveis_raca_municipio.head()

# %%
colunas_nascidos_municipio = [f'nascidos_{raca}' for raca in racas]
df_evitaveis_raca_municipio = df_evitaveis_raca_municipio.merge(
    df_mortalidade_raca_municipio[['ano'] + colunas_nascidos_municipio],
    on='ano', how='left'
)

for raca in racas:
    percentual = (df_evitaveis_raca_municipio[f'obitos_evitaveis_{raca}'] / df_evitaveis_raca_municipio[f'nascidos_{raca}']) * 100
    df_evitaveis_raca_municipio[f'percentual_evitaveis_{raca}'] = percentual.replace([float('inf'), -float('inf')], float('nan')).round(2)

df_evitaveis_raca_municipio.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_raca_municipio_ano.csv', index=False)
df_evitaveis_raca_municipio.to_csv('tabelas_finais//mortalidade_causas_evitaveis_raca_municipio_ano.csv', index=False)
df_evitaveis_raca_municipio

# %%
rotulos_raca_evitaveis = {'Amarela':'amarela','Branca':'branca','Indígena':'indigena',
                           'Parda':'parda','Preta':'preta','Não informada':'nao_informado'}

serie_temporal_multipla(
    df_evitaveis_raca_municipio,
    tempo='ano',
    colunas={rotulo: f'obitos_evitaveis_{raca}' for rotulo, raca in rotulos_raca_evitaveis.items()},
    titulo='Óbitos por causas evitáveis (0-364 dias) por raça/cor - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_raca_ano',
    ylabel='Óbitos'
)

# %%
## retirar 1996 do ano acima e colocar nota de rodapé

# %%
# percentual só existe a partir de 2011 (início da série de nascidos vivos por raça/cor da mãe)
df_percentual_evitaveis_municipio = df_evitaveis_raca_municipio[df_evitaveis_raca_municipio['ano'] >= 2011]

serie_temporal_multipla(
    df_percentual_evitaveis_municipio,
    tempo='ano',
    colunas={rotulo: f'percentual_evitaveis_{raca}' for rotulo, raca in rotulos_raca_evitaveis.items()},
    titulo='Percentual de óbitos evitáveis (0-364 dias) em relação aos nascidos vivos por raça/cor - Rio de Janeiro (2011-2025)',
    nome_arquivo='percentual_mortalidade_causas_evitaveis_raca_ano',
    ylabel='Percentual (%)'
)

# %% [markdown]
# ##### Óbitos por causas evitáveis, por grupo de causa (CID-10)

# %% [markdown]
# Usa os arquivos "segundo causas" (não por raça/cor), que classificam cada óbito evitável em uma hierarquia de grupo/subgrupo/causa específica. Soma as três faixas etárias (0-6, 7-27 e 28-364 dias) para obter o total 0-364 dias, no nível de município (1996-2025).
#
# Dois recortes:
# - Grupo (`1.`, `2.`, `3.`): nível mais alto da hierarquia.
# - Subgrupo (`1.1.`, `1.2.1`, `1.2.2`, `1.2.3`, `1.3.`, `1.4.`, `2.`): filhos diretos do grupo `1.` mais o próprio grupo `2.` (que não se divide em subgrupos).
#
# `3. Demais causas (não claramente evitáveis)` não tem subgrupos e por isso só aparece no gráfico de grupo.

# %%
faixas_evitaveis_causa = {
    '0_6': 'dados_locais//mortalidade//obitos_causas_evitaveis_0_6_dias_segundo_causas_municipio_1996_2025.csv',
    '7_27': 'dados_locais//mortalidade//obitos_causas_evitaveis_7_27_dias_segundo_causas_municipio_1996_2025.csv',
    '28_364': 'dados_locais//mortalidade//obitos_causas_evitaveis_28_364_dias_segundo_causas_municipio_1996_2025.csv',
}

# grupo: '1. ', '2. ' ou '3. '; subgrupo: '1.1.', '1.2.1/2/3', '1.3.', '1.4.' ou '2.' (que não se subdivide)
padrao_grupo = r'^[123]\.\s'
padrao_subgrupo = r'^(1\.1\.|1\.2\.[123]|1\.3\.|1\.4\.|2\.)\s'

df_evitaveis_grupo = combina_faixas_causa(padrao_grupo, faixas_evitaveis_causa)
df_evitaveis_subgrupo = combina_faixas_causa(padrao_subgrupo, faixas_evitaveis_causa)

df_evitaveis_grupo_wide = df_evitaveis_grupo.pivot(index='ano', columns='causa', values='obitos').reset_index()
df_evitaveis_subgrupo_wide = df_evitaveis_subgrupo.pivot(index='ano', columns='causa', values='obitos').reset_index()

df_evitaveis_grupo_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_grupo_ano.csv', index=False)
df_evitaveis_subgrupo_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_subgrupo_ano.csv', index=False)
df_evitaveis_grupo_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_grupo_ano.csv', index=False)
df_evitaveis_subgrupo_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_ano.csv', index=False)
df_evitaveis_grupo_wide.head()

# %%
colunas_grupo = {c: c for c in df_evitaveis_grupo_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_grupo_wide,
    tempo='ano',
    colunas=colunas_grupo,
    titulo='Óbitos por causas evitáveis (0-364 dias) por grupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_grupo_ano',
    ylabel='Óbitos',
    legend_title='Grupo',
)

# %%
colunas_subgrupo = {c: c for c in df_evitaveis_subgrupo_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_subgrupo_wide,
    tempo='ano',
    colunas=colunas_subgrupo,
    titulo='Óbitos por causas evitáveis (0-364 dias) por subgrupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7),
)

# %% [markdown]
# ##### Óbitos por causas evitáveis, por grupo de causa e faixa etária

# %% [markdown]
# Mesma classificação de grupo/subgrupo da seção anterior, mas sem somar as três faixas etárias: cada uma (0-6, 7-27 e 28-364 dias) é analisada separadamente, no mesmo recorte usado em Mortalidade Neonatal. Reaproveita `carrega_causas_evitaveis_categoria`, `combina_faixas_causa`, `padrao_grupo`, `padrao_subgrupo` e `faixas_evitaveis_causa`, já definidos acima.

# %% [markdown]
# ###### Precoce (0 a 6 dias)

# %%
df_evitaveis_grupo_0_6 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['0_6'], padrao_grupo)
df_evitaveis_subgrupo_0_6 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['0_6'], padrao_subgrupo)

df_evitaveis_grupo_0_6_wide = df_evitaveis_grupo_0_6.pivot(index='ano', columns='causa', values='obitos').reset_index()
df_evitaveis_subgrupo_0_6_wide = df_evitaveis_subgrupo_0_6.pivot(index='ano', columns='causa', values='obitos').reset_index()

df_evitaveis_grupo_0_6_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_grupo_0_6_ano.csv', index=False)
df_evitaveis_subgrupo_0_6_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_subgrupo_0_6_ano.csv', index=False)
df_evitaveis_grupo_0_6_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_grupo_0_6_ano.csv', index=False)
df_evitaveis_subgrupo_0_6_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_0_6_ano.csv', index=False)
df_evitaveis_grupo_0_6_wide.head()

# %%
colunas_grupo_0_6 = {c: c for c in df_evitaveis_grupo_0_6_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_grupo_0_6_wide,
    tempo='ano',
    colunas=colunas_grupo_0_6,
    titulo='Óbitos por causas evitáveis (0-6 dias) por grupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_grupo_0_6_ano',
    ylabel='Óbitos',
    legend_title='Grupo',
)

# %%
colunas_subgrupo_0_6 = {c: c for c in df_evitaveis_subgrupo_0_6_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_subgrupo_0_6_wide,
    tempo='ano',
    colunas=colunas_subgrupo_0_6,
    titulo='Óbitos por causas evitáveis (0-6 dias) por subgrupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_0_6_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7),
)

# %% [markdown]
# ###### Tardia (7 a 27 dias)

# %%
df_evitaveis_grupo_7_27 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['7_27'], padrao_grupo)
df_evitaveis_subgrupo_7_27 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['7_27'], padrao_subgrupo)

df_evitaveis_grupo_7_27_wide = df_evitaveis_grupo_7_27.pivot(index='ano', columns='causa', values='obitos').reset_index()
df_evitaveis_subgrupo_7_27_wide = df_evitaveis_subgrupo_7_27.pivot(index='ano', columns='causa', values='obitos').reset_index()

df_evitaveis_grupo_7_27_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_grupo_7_27_ano.csv', index=False)
df_evitaveis_subgrupo_7_27_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_subgrupo_7_27_ano.csv', index=False)
df_evitaveis_grupo_7_27_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_grupo_7_27_ano.csv', index=False)
df_evitaveis_subgrupo_7_27_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_7_27_ano.csv', index=False)
df_evitaveis_grupo_7_27_wide.head()

# %%
colunas_grupo_7_27 = {c: c for c in df_evitaveis_grupo_7_27_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_grupo_7_27_wide,
    tempo='ano',
    colunas=colunas_grupo_7_27,
    titulo='Óbitos por causas evitáveis (7-27 dias) por grupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_grupo_7_27_ano',
    ylabel='Óbitos',
    legend_title='Grupo',
)

# %%
colunas_subgrupo_7_27 = {c: c for c in df_evitaveis_subgrupo_7_27_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_subgrupo_7_27_wide,
    tempo='ano',
    colunas=colunas_subgrupo_7_27,
    titulo='Óbitos por causas evitáveis (7-27 dias) por subgrupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_7_27_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7),
)

# %% [markdown]
# ###### Pós-neonatal (28 a 364 dias)

# %%
df_evitaveis_grupo_28_364 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['28_364'], padrao_grupo)
df_evitaveis_subgrupo_28_364 = carrega_causas_evitaveis_categoria(faixas_evitaveis_causa['28_364'], padrao_subgrupo)

df_evitaveis_grupo_28_364_wide = df_evitaveis_grupo_28_364.pivot(index='ano', columns='causa', values='obitos').reset_index()
df_evitaveis_subgrupo_28_364_wide = df_evitaveis_subgrupo_28_364.pivot(index='ano', columns='causa', values='obitos').reset_index()

df_evitaveis_grupo_28_364_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_grupo_28_364_ano.csv', index=False)
df_evitaveis_subgrupo_28_364_wide.to_csv('dados_locais//tratados//mortalidade_causas_evitaveis_subgrupo_28_364_ano.csv', index=False)
df_evitaveis_grupo_28_364_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_grupo_28_364_ano.csv', index=False)
df_evitaveis_subgrupo_28_364_wide.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_28_364_ano.csv', index=False)
df_evitaveis_grupo_28_364_wide.head()

# %%
colunas_grupo_28_364 = {c: c for c in df_evitaveis_grupo_28_364_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_grupo_28_364_wide,
    tempo='ano',
    colunas=colunas_grupo_28_364,
    titulo='Óbitos por causas evitáveis (28-364 dias) por grupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_grupo_28_364_ano',
    ylabel='Óbitos',
    legend_title='Grupo',
)

# %%
colunas_subgrupo_28_364 = {c: c for c in df_evitaveis_subgrupo_28_364_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_evitaveis_subgrupo_28_364_wide,
    tempo='ano',
    colunas=colunas_subgrupo_28_364,
    titulo='Óbitos por causas evitáveis (28-364 dias) por subgrupo - Rio de Janeiro (1996-2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_28_364_ano',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    figsize=(14,7),
)

# %% [markdown]
# ###### Comparação entre faixas etárias (2025)

# %% [markdown]
# Gráfico de barras comparando os 7 subgrupos de causas evitáveis entre as três faixas etárias, no último ano disponível (2025), para evidenciar a mudança de perfil de causas ao longo do primeiro ano de vida.

# %%
faixa_rotulo = {'0_6': '0-6 dias', '7_27': '7-27 dias', '28_364': '28-364 dias'}
tabelas_subgrupo = {'0_6': df_evitaveis_subgrupo_0_6_wide, '7_27': df_evitaveis_subgrupo_7_27_wide, '28_364': df_evitaveis_subgrupo_28_364_wide}

partes_2025 = []
for chave, df_wide in tabelas_subgrupo.items():
    linha_2025 = df_wide[df_wide['ano'] == 2025].melt(id_vars='ano', var_name='subgrupo', value_name='obitos')
    linha_2025['faixa_etaria'] = faixa_rotulo[chave]
    partes_2025.append(linha_2025)

df_subgrupo_2025 = pd.concat(partes_2025, ignore_index=True)
df_subgrupo_2025.to_csv('tabelas_finais//mortalidade_causas_evitaveis_subgrupo_faixa_2025.csv', index=False)
df_subgrupo_2025.head()

# %%
ordem_subgrupo = [c for c in df_evitaveis_subgrupo_0_6_wide.columns if c != 'ano']
ordem_faixa = ['0-6 dias', '7-27 dias', '28-364 dias']

grafico_barra_agrupado(
    df_subgrupo_2025,
    categoria='faixa_etaria',
    valor='obitos',
    agrupador='subgrupo',
    titulo='Óbitos por causas evitáveis por subgrupo e faixa etária - Rio de Janeiro (2025)',
    nome_arquivo='obitos_causas_evitaveis_subgrupo_faixa_2025',
    ylabel='Óbitos',
    legend_title='Subgrupo',
    ordem_categoria=ordem_faixa,
    ordem_agrupador=ordem_subgrupo,
    rotacao_x=0,
)

# %% [markdown]
# #### 📋 Óbitos gravidez e puerpério

# %% [markdown]
# Óbitos maternos durante a gravidez e o puerpério, por bairro de residência (2006-2025).

# %%
df_obitos_gravidez = pd.read_csv('dados_locais\\mortalidade\\obitos_gravidez_bairro_2006_2025.csv')
df_obitos_gravidez = limpa_dados_datasus(df_obitos_gravidez)
df_obitos_gravidez = limpeza_tabnet_bairros(df_obitos_gravidez,categoria='óbitos-gravidez')
df_obitos_gravidez.head()

# %%
#por ano
df_obitos_gravidez_anual = df_obitos_gravidez[['ano','óbitos-gravidez']].groupby(by='ano').sum()
df_obitos_gravidez_anual.to_csv('tabelas_finais//obitos_gravidez_por_ano.csv')
df_obitos_gravidez_anual

# %%
serie_temporal(df_obitos_gravidez_anual,'ano','óbitos-gravidez','Óbitos durante gravidez por ano',
               nome_arquivo='obitos_gravidez_por_ano')

# %%
df_obitos_puerperio = pd.read_csv('dados_locais\\mortalidade\\obitos_puerperio_bairro_2006_2025.csv')
df_obitos_puerperio = limpa_dados_datasus(df_obitos_puerperio)
df_obitos_puerperio = limpeza_tabnet_bairros(df_obitos_puerperio,categoria='óbitos-puerpério')
df_obitos_puerperio.head()

# %%
#por ano
df_obitos_puerperio_anual = df_obitos_puerperio[['ano','óbitos-puerpério']].groupby(by='ano').sum()
df_obitos_puerperio_anual.to_csv('tabelas_finais//obitos_puerperio_por_ano.csv')
df_obitos_puerperio_anual

# %%
serie_temporal(df_obitos_puerperio_anual,'ano','óbitos-puerpério','Óbitos durante puerpério por ano',
               nome_arquivo='obitos_puerperio_por_ano')

# %% [markdown]
# #### 🩺 Mortalidade Neonatal

# %% [markdown]
# Óbitos de menores de 1 ano por faixa etária (precoce, tardia, pós-neonatal e total 0-364 dias), com taxa por 1.000 nascidos vivos.
#
# > **Nota:** Precoce e Tardia comparam com `df_vivos` por *inner join* (bairros sem óbito registrado em algum lado ficam de fora); Pós-neonatal e Total usam uma grade bairro x ano com zeros explícitos, mais robusta. As taxas de Precoce/Tardia podem, por isso, subestimar ligeiramente bairros pequenos.

# %% [markdown]
# ##### Precoce (0 a 6 dias)

# %%
df_neonatal_precoce = pd.read_csv('dados_locais//mortalidade//obitos_0_6_dias_bairro_2006_2025.csv', sep=';')
df_neonatal_precoce = limpa_dados_datasus(df_neonatal_precoce)
df_neonatal_precoce = limpeza_tabnet_bairros(df_neonatal_precoce,categoria='obitos precoces')
df_neonatal_precoce = df_neonatal_precoce.merge(df_vivos, on=['bairro','ano','codigo'])
df_neonatal_precoce['taxa_mortalidade_precoce'] = (df_neonatal_precoce['obitos precoces']/df_neonatal_precoce['nascidos vivos'])*1000
df_neonatal_precoce.head()

# %%
df_neonatal_precoce_anual = df_neonatal_precoce[['ano','obitos precoces','nascidos vivos']].groupby(by='ano').sum()
df_neonatal_precoce_anual['taxa_mortalidade_precoce'] = (df_neonatal_precoce_anual['obitos precoces']/df_neonatal_precoce_anual['nascidos vivos'])*1000
df_neonatal_precoce_anual.to_csv('tabelas_finais//mortalidade_neonatal_precoce_por_ano.csv')
df_neonatal_precoce_anual

# %%
serie_temporal(df_neonatal_precoce_anual,'ano','taxa_mortalidade_precoce','Taxa de óbitos precoces por ano',
               nome_arquivo='taxa_mortalidade_precoce_ano')

# %% [markdown]
# ##### Tardia (7 a 27 dias)

# %%
df_neonatal_tardia = pd.read_csv('dados_locais//mortalidade//obitos_7_27_dias_bairro_2006_2025.csv', sep=';')
df_neonatal_tardia = limpa_dados_datasus(df_neonatal_tardia)
df_neonatal_tardia = limpeza_tabnet_bairros(df_neonatal_tardia,'obitos_tardios')
df_neonatal_tardia = df_neonatal_tardia.merge(df_vivos, on=['bairro','ano','codigo'])
df_neonatal_tardia['taxa_obitos_tardios'] = (df_neonatal_tardia['obitos_tardios']/df_neonatal_tardia['nascidos vivos'])*1000
df_neonatal_tardia.head()

# %%
df_neonatal_tardia_anual = df_neonatal_tardia[['ano','obitos_tardios','nascidos vivos']].groupby(by='ano').sum()
df_neonatal_tardia_anual['taxa_obitos_tardios'] = (df_neonatal_tardia_anual['obitos_tardios']/df_neonatal_tardia_anual['nascidos vivos'])*1000
df_neonatal_tardia_anual.to_csv('tabelas_finais//mortalidade_neonatal_tardia_por_ano.csv')
df_neonatal_tardia_anual

# %%
serie_temporal(df_neonatal_tardia_anual,'ano','taxa_obitos_tardios','Taxa de óbitos tardios por ano',
               nome_arquivo='taxa_obitos_tardios_ano')

# %% [markdown]
# ##### Pós-neonatal (28 a 364 dias)

# %% [markdown]
# Não há arquivo pronto para 28-364 dias (total, sem raça): é derivado por subtração `0-364 - 0-6 - 7-27`, com cada faixa preenchida em uma grade completa bairro x ano (zeros verdadeiros onde o Tabnet omite colunas/linhas de soma zero), para evitar contagens incompletas na subtração.

# %%
anos_infantil = list(range(2006, 2026))

df_nascidos_total = carrega_raca_bairro('dados_locais//mortalidade//nascidos_vivos_bairros_2006_a_2025.csv', categoria='nascidos_vivos', anos_validos=anos_infantil, sep=',')
df_obitos_0_364_total = carrega_raca_bairro('dados_locais//mortalidade//obitos_0_364_dias_bairro_2006_2025.csv', categoria='obitos_0_364', anos_validos=anos_infantil)
df_obitos_0_6_total = carrega_raca_bairro('dados_locais//mortalidade//obitos_0_6_dias_bairro_2006_2025.csv', categoria='obitos_0_6', anos_validos=anos_infantil)
df_obitos_7_27_total = carrega_raca_bairro('dados_locais//mortalidade//obitos_7_27_dias_bairro_2006_2025.csv', categoria='obitos_7_27', anos_validos=anos_infantil)

df_mortalidade_infantil = (
    df_obitos_0_364_total
    .merge(df_obitos_0_6_total, on=['codigo','bairro','ano'], how='outer')
    .merge(df_obitos_7_27_total, on=['codigo','bairro','ano'], how='outer')
    .merge(df_nascidos_total, on=['codigo','bairro','ano'], how='outer')
)

colunas_obitos_faixas = ['obitos_0_364','obitos_0_6','obitos_7_27']
df_mortalidade_infantil[colunas_obitos_faixas] = df_mortalidade_infantil[colunas_obitos_faixas].fillna(0)
df_mortalidade_infantil['nascidos_vivos'] = df_mortalidade_infantil['nascidos_vivos'].fillna(0)

df_mortalidade_infantil['obitos_28_364'] = (
    df_mortalidade_infantil['obitos_0_364'] - df_mortalidade_infantil['obitos_0_6'] - df_mortalidade_infantil['obitos_7_27']
)

df_mortalidade_infantil['taxa_mortalidade_infantil'] = (
    (df_mortalidade_infantil['obitos_0_364'] / df_mortalidade_infantil['nascidos_vivos']) * 1000
).replace([float('inf'), -float('inf')], float('nan'))

df_mortalidade_infantil['taxa_mortalidade_pos_neonatal'] = (
    (df_mortalidade_infantil['obitos_28_364'] / df_mortalidade_infantil['nascidos_vivos']) * 1000
).replace([float('inf'), -float('inf')], float('nan'))

df_mortalidade_infantil.head()

# %%
df_mortalidade_infantil_anual = df_mortalidade_infantil[['ano','obitos_0_364','obitos_28_364','nascidos_vivos']].groupby(by='ano').sum()
df_mortalidade_infantil_anual['taxa_mortalidade_infantil'] = (df_mortalidade_infantil_anual['obitos_0_364']/df_mortalidade_infantil_anual['nascidos_vivos'])*1000
df_mortalidade_infantil_anual['taxa_mortalidade_pos_neonatal'] = (df_mortalidade_infantil_anual['obitos_28_364']/df_mortalidade_infantil_anual['nascidos_vivos'])*1000
df_mortalidade_infantil_anual.to_csv('tabelas_finais//mortalidade_infantil_pos_neonatal_total_por_ano.csv')
df_mortalidade_infantil_anual

# %%
serie_temporal(df_mortalidade_infantil_anual,'ano','taxa_mortalidade_pos_neonatal','Taxa de mortalidade pós-neonatal (28-364 dias) por ano',
               nome_arquivo='taxa_mortalidade_pos_neonatal_ano')

# %% [markdown]
# ##### Total (0 a 364 dias)

# %%
serie_temporal(df_mortalidade_infantil_anual,'ano','taxa_mortalidade_infantil','Taxa de mortalidade infantil (0-364 dias) por ano',
               nome_arquivo='taxa_mortalidade_infantil_ano')

# %% [markdown]
# ### 🥗 DataSus - SISVAN

# %% [markdown]
# Percentual de crianças 0-6 anos com sobrepeso/obesidade e desnutrição, agregado por ano (fonte: SISVAN).

# %%
df_desnutricao = pd.read_csv(r"dados_locais\tratados\desnutrição.csv", index_col=0)
df_desnutricao.tail()

# %%
df_desnutricao['peso_muito_baixo_percentual'] = df_desnutricao['peso_muito_baixo_percentual'].apply(convert_numeric_safe)
df_desnutricao['peso_baixo_percentual'] = df_desnutricao['peso_baixo_percentual'].apply(convert_numeric_safe)
df_desnutricao['Percent. baixo peso total'] = df_desnutricao['peso_muito_baixo_percentual'] + df_desnutricao['peso_baixo_percentual']
df_desnutricao.to_csv('tabelas_finais\\sisvan_desnutricao_por_ano.csv')
serie_temporal(df_desnutricao,tempo='ano',valor='Percent. baixo peso total', titulo='Percentual Crianças 0-6 com baixo peso',
               nome_arquivo='sisvan_desnutricao_percentual_por_ano')

# %%
df_sobrepeso = pd.read_csv(r"dados_locais\tratados\sobrepeso.csv", index_col=0)
df_sobrepeso.head()

# %%
df_sobrepeso['sobrepeso_percentual'] = df_sobrepeso['sobrepeso_percentual'].apply(convert_numeric_safe)
df_sobrepeso['obesidade_percentual'] = df_sobrepeso['obesidade_percentual'].apply(convert_numeric_safe)
df_sobrepeso['Percent. sobrepeso total'] = df_sobrepeso['sobrepeso_percentual'] + df_sobrepeso['obesidade_percentual']
df_sobrepeso.to_csv('tabelas_finais\\sisvan_sobrepeso_por_ano.csv')
serie_temporal(df_sobrepeso,tempo='ano',valor='Percent. sobrepeso total', titulo='Percentual Crianças 0-6 com sobrepeso i.e. PESO ACIMA + OBESIDADE',
               nome_arquivo='sisvan_sobrepeso_percentual_por_ano')

# %%
serie_temporal(df_sobrepeso,tempo='ano',valor='obesidade_percentual', titulo='Percentual Crianças 0-6 com obesidade',
               nome_arquivo='sisvan_obesidade_percentual_por_ano')

# %% [markdown]
# ### 💉 Cobertura Vacinal EPI

# %% [markdown]
# Cobertura vacinal (%) por imunobiológico, série histórica do EPI/SVS-Rio (2016-2026).
#
# Notas:
# - Cobertura acima de 100% é esperada em dados administrativos de vacinação (numerador de doses aplicadas pode incluir população fora do denominador estimado) — não é um erro de cálculo.
# - 2026 é um ano ainda em curso (dados parciais); comparar com cautela contra os anos fechados.

# %%
df_cobertura_vacinal = carrega_cobertura_vacinal('dados_locais//vacinacao//serie_historica_cobertura_vacinal.csv')
df_cobertura_vacinal_wide = df_cobertura_vacinal.pivot(index='ano', columns='imunobiologico', values='cobertura').reset_index()
df_cobertura_vacinal_wide.to_csv('tabelas_finais//cobertura_vacinal_epi_por_ano.csv', index=False)
df_cobertura_vacinal_wide.head()

# %%
colunas_vacinas = {c: c for c in df_cobertura_vacinal_wide.columns if c != 'ano'}
serie_temporal_multipla(
    df_cobertura_vacinal_wide,
    tempo='ano',
    colunas=colunas_vacinas,
    titulo='Cobertura vacinal por imunobiológico - Rio de Janeiro (2016-2026)',
    nome_arquivo='cobertura_vacinal_epi_ano',
    ylabel='Cobertura (%)',
    legend_title='Imunobiológico',
    figsize=(14,7),
)

# %% [markdown]
# Comparativo direto entre quatro anos (2016, 2019, 2022 e 2025) por imunobiológico, para visualizar o impacto da pandemia (queda em 2022) e a recuperação até 2025.

# %%
anos_comparacao = [2016, 2019, 2022, 2025]
ordem_vacinas = [c for c in df_cobertura_vacinal_wide.columns if c != 'ano']

df_cobertura_comparacao = df_cobertura_vacinal[df_cobertura_vacinal['ano'].isin(anos_comparacao)].copy()
df_cobertura_comparacao['ano'] = df_cobertura_comparacao['ano'].astype(str)
df_cobertura_comparacao.to_csv('tabelas_finais//cobertura_vacinal_epi_comparativo_anos.csv', index=False)
df_cobertura_comparacao.head()

# %%
grafico_barra_agrupado(
    df_cobertura_comparacao,
    categoria='ano',
    valor='cobertura',
    agrupador='imunobiologico',
    titulo='Cobertura vacinal por imunobiológico - anos selecionados (2016, 2019, 2022, 2025)',
    nome_arquivo='cobertura_vacinal_epi_comparativo_anos',
    ylabel='Cobertura (%)',
    legend_title='Imunobiológico',
    ordem_categoria=[str(a) for a in anos_comparacao],
    ordem_agrupador=ordem_vacinas,
    rotacao_x=0,
    figsize=(16,7),
)

# %% [markdown]
# ### 🎓 PNAD Contínua, Censo Escolar e INEP

# %% [markdown]
# Frequência escolar (PNAD Contínua) e matrículas (Censo Escolar/INEP) de crianças de 0 a 6 anos.

# %% [markdown]
# #### Taxa de frequência escolar

# %%
df_freq_escolar = pd.read_csv('dados_locais//educacao//pnad_taxa_frequencia_escolar_ate_6_anos.csv', sep=';')
df_freq_escolar = df_freq_escolar[(df_freq_escolar['Idade'] != '0 a 3 anos')
                                  & (df_freq_escolar['Idade'] != '4 a 5 anos')
                                  & (df_freq_escolar['Idade'] != '6 anos')]
df_freq_escolar['Total'] = df_freq_escolar['Total'].str.replace(',','.').astype('Float64')/100
df_freq_escolar.to_csv('tabelas_finais//frequencia_escolar_pnad_por_idade.csv', index=False)
df_freq_escolar

# %%
grafico_barra(df=df_freq_escolar,categoria='Idade',valor='Total',titulo="Frequencia escolar por idade",
              nome_arquivo='pnad_frequencia_escolar_por_idade')

# %% [markdown]
# #### Número de matrículas 0 a 6 anos (complementar 2021-2025)

# %%
df_freq_escolar = pd.read_csv('dados_locais//educacao//censo_escolar_matriculas_ate_6anos.csv')
df_freq_escolar.sort_values('ano', inplace=True)
df_freq_escolar.rename(columns={'f0_': 'matriculas'}, inplace=True)
df_freq_escolar.to_csv('tabelas_finais//matriculas_0_a_6_por_ano.csv', index=False)
df_freq_escolar

# %%
serie_temporal(df_freq_escolar,'ano','matriculas','Matrículas de 0 a 6 anos por ano',
               nome_arquivo='matriculas_0_a_6_por_ano')

# %% [markdown]
# #### Juncao de tabelas por bairro

# %% [markdown]
# Junta nascidos vivos, baixo peso, óbitos de gravidez/puerpério e mortalidade neonatal por bairro-ano.
#
# > **Nota:** não inclui óbitos por raça/cor, causas evitáveis ou cobertura vacinal, que têm granularidades diferentes (raça, ou município-ano).

# %%
lista_dfs = [df_vivos,df_baixo_peso,
             df_obitos_gravidez,df_obitos_puerperio,
             df_neonatal_precoce,df_neonatal_tardia]
df_final = lista_dfs[0].copy()
for i in lista_dfs[1:]:
    df_final = df_final.merge(i,on=['codigo','bairro','ano'],how='outer')
#df_final = df_final[df_final['ano']!='Total']
df_final.drop(columns=['nascidos vivos_x','nascidos vivos_y'],inplace=True)
df_final.to_excel('mapas/tabelas_bairros/dados_datasus_por_bairro.xlsx')
df_final.head()
#pensar testes


# %% [markdown]
# #### Juncao de tabelas municipio

# %% [markdown]
# *(Pendente)* Agregação das tabelas acima ao nível município-ano.

# %% [markdown]
# ---
# ## 📝 Análise / Relatório

# %% [markdown]
# *(Pendente)* Síntese narrativa dos achados.

# %%
###

# %% [markdown]
# ### Demografia e População

# %%
#### Resumo dos achados

#### Fontes de Dados

# %%
#### Dimensão temporal

# %%
#### Recortes de Raça e Gênero

# %%
#### Dimensão geográfica

# %% [markdown]
# ### Assistência Social

# %% [markdown]
# ### Educação

# %% [markdown]
# ### Saúde

# %% [markdown]
# ### Proteção
