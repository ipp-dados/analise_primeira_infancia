# -*- coding: utf-8 -*-
"""### 🖨️ Variante de impressão (relatório PDF)

Cada função de visualização acima grava também uma **variante para o relatório em PDF**
(`specs/2026-09-25_relatorio_latex`, §5.1 e Bloco 5): figura desenhada no tamanho final do A4 (16 cm de largura útil),
sem título nem fonte embutidos (vão para a legenda ABNT do LaTeX), eixo com rótulo por extenso e unidade,
números em pt-BR, rótulos diretos seletivos (sem tooltip no papel), paleta de impressão validada e IBM Plex
Sans (a fonte do corpo do relatório). Séries com mais de `_LIMIAR_DESTAQUE_SERIES` linhas viram pequenos
múltiplos; mapas de taxa por bairro usam teto de cor no percentil 95 (decisão D5).
Gráficos em `visualizacoes/a4/*.pdf` (vetorial), mapas em `mapas/a4/*.pdf`; título, fonte e unidade de cada
figura vão para `visualizacoes/a4/_manifesto.csv`, lido por `relatorio/latex/build/gera_latex.py`.
Desligar com `GERA_VARIANTE_A4 = False`. As PNGs de tela, o site e o DOCX não mudam.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import contextily as ctx
import geopandas as gpd
import math
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import textwrap as _textwrap
from matplotlib import font_manager as _fm
from matplotlib.colors import Normalize as _Normalize
from matplotlib.patches import Patch as _Patch
from matplotlib.ticker import FuncFormatter as _FuncFormatter
from matplotlib.ticker import MaxNLocator as _MaxNLocator
from matplotlib_scalebar.scalebar import ScaleBar
from pathlib import Path
from shapely.geometry import box
from .estilo import (_LIMIAR_DESTAQUE_SERIES, _PROVEDORES_FUNDO, _adiciona_rotulos_municipios_vizinhos, _marca_corte_eixo_y, _numero_ptbr)

__all__ = [
    'GERA_VARIANTE_A4',
    '_PASTA_A4',
    '_MANIFESTO_A4',
    '_CM',
    '_LARGURA_A4',
    '_PALETA_IMPRESSAO',
    '_TINTA',
    '_TINTA2',
    '_TINTA3',
    '_GRADE',
    '_CINZA_CONTEXTO',
    '_PASTA_FONTES',
    '_FAMILIA_IMPRESSAO',
    'ROTULOS_EIXO',
    'ROTULOS_A4_ARQUIVO',
    '_ESCALA_100_A4',
    '_familia_impressao',
    '_rc_impressao',
    '_num_a4',
    '_decimais_a4',
    '_rotulo_a4',
    '_categoria_a4',
    '_eh_total_a4',
    '_rotulo_y_a4',
    '_eixo_x_anos_a4',
    '_ponto_a4',
    '_salva_a4',
    '_a4_seguro',
    '_a4_serie_unica',
    '_espaca_rotulos',
    '_a4_series',
    '_a4_pequenos_multiplos',
    '_a4_barras',
    '_a4_barras_agrupadas',
    '_a4_ranking',
    '_TETO_PERCENTIL_A4',
    '_a4_mapa',
]


GERA_VARIANTE_A4 = True

_PASTA_A4 = {'grafico': 'visualizacoes/a4', 'mapa': 'mapas/a4'}

_MANIFESTO_A4 = 'visualizacoes/a4/_manifesto.csv'

_CM = 1 / 2.54

_LARGURA_A4 = 16 * _CM

# paleta de impressão: mesmos matizes e ordem de _PALETA_CATEGORICA, em tons que passam no validador da skill
# dataviz em fundo branco (luminância, croma, daltonismo, contraste >= 3:1) -- specs/2026-09-25_relatorio_latex §5.1
_PALETA_IMPRESSAO = ['#3f76b8', '#dc7a45', '#0f7d5c', '#b88a1e', '#b8527b', '#5c9a3c', '#6f64ae', '#b84f4e']

_TINTA, _TINTA2, _TINTA3, _GRADE, _CINZA_CONTEXTO = '#16202A', '#3F4B57', '#6B7580', '#DDE2E7', '#C9CFD5'

_PASTA_FONTES = 'relatorio/latex/fontes'

_FAMILIA_IMPRESSAO = None

# rótulo por extenso, com unidade, para a coluna/ylabel que chega às funções de visualização
ROTULOS_EIXO = {
    'taxa_mortalidade_precoce': 'Óbitos de 0 a 6 dias por mil nascidos vivos',
    'taxa_obitos_tardios': 'Óbitos de 7 a 27 dias por mil nascidos vivos',
    'taxa_mortalidade_pos_neonatal': 'Óbitos de 28 a 364 dias por mil nascidos vivos',
    'taxa_mortalidade_infantil': 'Óbitos de menores de 1 ano por mil nascidos vivos',
    'taxa_por_mil': 'Óbitos evitáveis de menores de 5 anos por mil nascidos vivos',
    'nascidos vivos': 'Nascidos vivos por ano',
    'percentual abaixo do peso': '% dos nascidos vivos com menos de 2.500 g',
    'óbitos-gravidez': 'Óbitos maternos durante a gravidez, por ano',
    'óbitos-puerpério': 'Óbitos maternos durante o puerpério, por ano',
    'Percent. baixo peso total': '% das crianças acompanhadas com peso baixo ou muito baixo para a idade',
    'Percent. sobrepeso total': '% das crianças acompanhadas com sobrepeso ou obesidade',
    'obesidade_percentual': '% das crianças acompanhadas com obesidade',
    'populacao_0_a_6': 'Crianças de 0 a 6 anos',
    'percentual_0_a_6': '% da população do município',
    'Percentual 0 a 4 anos': '% da população do município',
    'matriculas': 'Matrículas de crianças de 0 a 5 anos',
    'Óbitos': 'Óbitos por ano',
    'Pessoas': 'Pessoas',
    'Taxa (%)': 'Taxa de frequência escolar bruta (%)',
    'Percentual (%)': '%',
    'Notificações': 'Notificações por ano',
    'notificações': 'Notificações',
}

# ... e por arquivo, quando o mesmo ylabel genérico serve a medidas diferentes
ROTULOS_A4_ARQUIVO = {
    'percentual_mortalidade_raca_ano': 'Óbitos de menores de 1 ano por mil nascidos vivos',
    'pnad_frequencia_escolar_por_idade': '% que frequenta escola ou creche',
    'cadunico_familias_arranjo_renda': '% das famílias do arranjo',
    'taxa_atendimento_0_a_5_por_ano': 'Matrículas por 100 crianças residentes',
}

_ESCALA_100_A4 = {'pnad_frequencia_escolar_por_idade'}   # CSV em fração 0-1

def _familia_impressao():
    """IBM Plex Sans versionada em relatorio/latex/fontes/ (a mesma do corpo do PDF); sans-serif se faltar."""
    global _FAMILIA_IMPRESSAO
    if _FAMILIA_IMPRESSAO is None:
        arquivos = list(Path(_PASTA_FONTES).glob('IBMPlexSans-*.otf'))
        for arq in arquivos:
            _fm.fontManager.addfont(str(arq))
        _FAMILIA_IMPRESSAO = 'IBM Plex Sans' if arquivos else 'sans-serif'
    return _FAMILIA_IMPRESSAO

def _rc_impressao():
    return {
        'font.family': _familia_impressao(), 'font.size': 8, 'text.color': _TINTA, 'axes.labelcolor': _TINTA2,
        'axes.labelsize': 8, 'axes.edgecolor': _TINTA3, 'axes.linewidth': 0.6, 'axes.spines.top': False,
        'axes.spines.right': False, 'axes.spines.left': False, 'axes.grid': True, 'axes.grid.axis': 'y',
        'grid.color': _GRADE, 'grid.linewidth': 0.5, 'grid.alpha': 1.0, 'grid.linestyle': '-',
        'xtick.color': _TINTA3, 'ytick.color': _TINTA3, 'xtick.labelcolor': _TINTA2, 'ytick.labelcolor': _TINTA2,
        'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'ytick.left': False, 'xtick.major.width': 0.6,
        'xtick.major.size': 2.5, 'legend.frameon': False, 'legend.fontsize': 7.5, 'legend.title_fontsize': 7.5,
        'lines.linewidth': 1.6, 'lines.solid_capstyle': 'round', 'pdf.fonttype': 42, 'axes.titlesize': 8,
        'savefig.dpi': 300, 'axes.prop_cycle': plt.cycler(color=_PALETA_IMPRESSAO), 'hatch.linewidth': 0.4,
    }

def _num_a4(v, dec=0):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return '–'
    return f'{v:,.{dec}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def _decimais_a4(valores):
    """0 casas para contagens e valores grandes, 1 para taxas/percentuais pequenos."""
    v = pd.Series(valores).dropna().astype(float)
    if v.empty:
        return 0
    inteiros = (v == v.round()).all()
    return 0 if (inteiros or v.abs().max() >= 100) else 1

def _rotulo_a4(coluna_ou_ylabel, nome_arquivo=None):
    if nome_arquivo in ROTULOS_A4_ARQUIVO:
        return ROTULOS_A4_ARQUIVO[nome_arquivo]
    chave = str(coluna_ou_ylabel)
    if chave in ROTULOS_EIXO:
        return ROTULOS_EIXO[chave]
    texto = chave.replace('_', ' ').strip()
    return texto[:1].upper() + texto[1:]

def _categoria_a4(v):
    """0.0 -> '0'; mantém texto."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)

def _eh_total_a4(v):
    return str(v).strip().lower().startswith(('total', 'subtotal'))

def _rotulo_y_a4(ax, texto):
    """Unidade na horizontal, acima do eixo -- lê-se sem girar a página."""
    ax.set_ylabel('')
    ax.annotate(_textwrap.fill(texto, 95), xy=(0, 1), xycoords='axes fraction', xytext=(0, 8),
                textcoords='offset points', ha='left', va='bottom', fontsize=7.5, color=_TINTA2)

def _eixo_x_anos_a4(ax, xs, rotulo_extra=0):
    xs = sorted(pd.Series(xs).dropna().unique())
    if len(xs) <= 12:
        ax.set_xticks(xs)
    else:
        ax.xaxis.set_major_locator(_MaxNLocator(integer=True, nbins=9))
    ax.set_xlim(xs[0] - 0.5, xs[-1] + 0.5 + rotulo_extra * (xs[-1] - xs[0]))
    if len(xs) > 12:   # a folga à direita é para os rótulos: nenhum ano marcado além do último dado
        ax.set_xticks([t for t in ax.get_xticks() if xs[0] <= t <= xs[-1]])
    ax.xaxis.set_major_formatter(_FuncFormatter(lambda v, _: str(int(v))))

def _ponto_a4(ax, x, y, cor, texto=None, dx=0, dy=0, ha='center', va='center', peso='normal', tamanho=7.5):
    ax.plot([x], [y], 'o', ms=4.0, color=cor, mec='white', mew=1.0, zorder=5, clip_on=False)
    if texto:
        ax.annotate(texto, (x, y), xytext=(dx, dy), textcoords='offset points', ha=ha, va=va,
                    fontsize=tamanho, color=_TINTA, fontweight=peso, zorder=6)

def _salva_a4(fig, nome_arquivo, tipo, titulo, fonte, unidade):
    pasta = Path(_PASTA_A4[tipo])
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / f'{nome_arquivo}.pdf'
    fig.savefig(destino, bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)
    manifesto = Path(_MANIFESTO_A4)
    linha = {'arquivo': destino.as_posix(), 'tipo': tipo, 'titulo': titulo, 'fonte': fonte or '', 'unidade': unidade or ''}
    df_m = pd.read_csv(manifesto) if manifesto.exists() else pd.DataFrame(columns=list(linha))
    df_m = pd.concat([df_m[df_m['arquivo'] != linha['arquivo']], pd.DataFrame([linha])], ignore_index=True)
    manifesto.parent.mkdir(parents=True, exist_ok=True)
    df_m.sort_values('arquivo').to_csv(manifesto, index=False)

def _a4_seguro(funcao):
    """A variante de impressão nunca interrompe o notebook: falha vira aviso (e a figura cai na PNG de tela)."""
    def envelope(*args, **kwargs):
        if not GERA_VARIANTE_A4:
            return
        # seaborn aceita x='ano' quando 'ano' é o índice do DataFrame; aqui a coluna precisa existir
        if args and isinstance(args[0], pd.DataFrame) and not isinstance(args[0], gpd.GeoDataFrame) \
                and any(n is not None and n not in args[0].columns for n in args[0].index.names):
            args = (args[0].reset_index(),) + tuple(args[1:])
        try:
            with plt.rc_context(_rc_impressao()):
                funcao(*args, **kwargs)
        except Exception as erro:  # noqa: BLE001 -- aviso explícito, não silêncio
            print(f'[variante A4] {funcao.__name__} falhou para {kwargs.get("nome_arquivo", "?")}: {erro} '
                  '-- o relatório usa a PNG de tela para esta figura')
    envelope.__name__ = funcao.__name__
    return envelope

# ------------------------------------------------------------------ séries temporais
@_a4_seguro
def _a4_serie_unica(df, tempo, valor, titulo, nome_arquivo, fonte_dados, base_zero=True):
    d = df[[tempo, valor]].dropna().sort_values(tempo)
    x, y = d[tempo].astype(float), d[valor].astype(float)
    dec = _decimais_a4(y)
    fig, ax = plt.subplots(figsize=(_LARGURA_A4, 6.0 * _CM))
    cor = _PALETA_IMPRESSAO[0]
    ax.plot(x, y, color=cor)
    if base_zero:
        ax.set_ylim(0, y.max() * 1.2 if y.max() > 0 else 1)
    else:   # D3/D12 (specs/2026-09-29_pendencias): eixo cortado; a nota já vem em fonte_dados (serie_temporal)
        folga = (y.max() - y.min()) or 1
        ax.set_ylim(y.min() - folga * 0.35, y.max() + folga * 0.35)
        _marca_corte_eixo_y(ax)
    ax.yaxis.set_major_locator(_MaxNLocator(nbins=5, integer=y.max() >= 5))
    ax.yaxis.set_major_formatter(_FuncFormatter(lambda v, _: _num_a4(v, 0 if y.max() >= 5 else 1)))
    _eixo_x_anos_a4(ax, x, rotulo_extra=0.07)
    rotulo = _rotulo_a4(valor, nome_arquivo)
    _rotulo_y_a4(ax, rotulo)
    i_min, i_max = y.idxmin(), y.idxmax()
    marcados = {d.index[0], i_min, i_max}
    for i in marcados - {d.index[-1]}:
        acima = i != i_min or i == i_max
        _ponto_a4(ax, x[i], y[i], cor, _num_a4(y[i], dec), dy=6 if acima else -7, va='bottom' if acima else 'top')
    u = d.index[-1]
    _ponto_a4(ax, x[u], y[u], cor, f'{_num_a4(y[u], dec)}\nem {int(x[u])}', dx=5, ha='left', peso='semibold')
    _salva_a4(fig, nome_arquivo, 'grafico', titulo, fonte_dados, rotulo)

def _espaca_rotulos(valores, separacao):
    """Posições y dos rótulos de fim de linha sem sobreposição (mantém a ordem; desloca o mínimo)."""
    ordem = sorted(range(len(valores)), key=lambda i: valores[i])
    pos = list(valores)
    for k in range(1, len(ordem)):
        a, b = ordem[k - 1], ordem[k]
        if pos[b] - pos[a] < separacao:
            pos[b] = pos[a] + separacao
    return pos

@_a4_seguro
def _a4_series(df, tempo, colunas, titulo, nome_arquivo, ylabel, fonte_dados, linhas_referencia=None, marcos=None):
    itens = [(r, c) for r, c in colunas.items() if c in df.columns]
    if len(itens) > _LIMIAR_DESTAQUE_SERIES:
        return _a4_pequenos_multiplos(df, tempo, itens, titulo, nome_arquivo, ylabel, fonte_dados)
    d = df.sort_values(tempo)
    x = d[tempo].astype(float)
    todos = pd.concat([d[c] for _, c in itens]).astype(float)
    dec = _decimais_a4(todos)
    fig, ax = plt.subplots(figsize=(_LARGURA_A4, 6.8 * _CM))
    maximo = max([todos.max()] + [v for v, _ in (linhas_referencia or [])])   # metas cabem no gráfico
    topo = maximo * 1.15 if maximo > 0 else 1
    ax.set_ylim(0, topo)
    finais = []
    for i, (rotulo, col) in enumerate(itens):
        cor = _PALETA_IMPRESSAO[i % len(_PALETA_IMPRESSAO)]
        s = d[[tempo, col]].dropna()
        ax.plot(s[tempo].astype(float), s[col].astype(float), color=cor, label=rotulo)
        if len(s):
            finais.append((rotulo, cor, float(s[tempo].iloc[-1]), float(s[col].iloc[-1])))
    for valor, rotulo_ref in (linhas_referencia or []):
        ax.axhline(valor, color=_TINTA3, lw=0.6, zorder=0)
        ax.annotate(rotulo_ref, xy=(0, valor), xycoords=('axes fraction', 'data'), xytext=(2, 2),
                    textcoords='offset points', fontsize=6.8, color=_TINTA2, va='bottom')
    for ano, texto in (marcos or {}).items():
        ax.axvline(ano, color=_TINTA3, lw=0.6, zorder=0)
        ax.annotate(_textwrap.fill(texto, 30), xy=(ano, topo), xytext=(3, -2), textcoords='offset points',
                    fontsize=6.8, color=_TINTA2, va='top')
    # rótulos no fim das linhas (nome e último valor); quando as linhas terminam juntas, o rótulo é afastado
    # e ligado ao ponto por um fio fino (em vez de empilhar rótulos soltos)
    ys = _espaca_rotulos([f[3] for f in finais], separacao=topo * 0.075)
    # nomes longos (ex. subgrupos CID-10) no fim da linha alargariam a figura além dos 16 cm e o texto encolheria
    # ao caber na página: nesse caso o fim da linha leva só o valor, e o nome fica na legenda (uma entrada por linha)
    nomes_longos = max((len(str(f[0])) for f in finais), default=0) > 18
    rotulos_fim = [(_num_a4(f[3], dec) if nomes_longos else f'{f[0]}  {_num_a4(f[3], dec)}') for f in finais]
    largura_rot = max((len(r) for r in rotulos_fim), default=10)
    _eixo_x_anos_a4(ax, x, rotulo_extra=min(0.04 + largura_rot * 0.012, 0.35))
    folga = (x.max() - x.min()) * 0.02
    for (rotulo, cor, xf, yf), yr, texto_fim in zip(finais, ys, rotulos_fim):
        ax.plot([xf], [yf], 'o', ms=3.6, color=cor, mec='white', mew=0.9, zorder=5)
        seta = dict(arrowstyle='-', color=_TINTA3, lw=0.4, shrinkA=0, shrinkB=2) if abs(yr - yf) > topo * 0.01 else None
        ax.annotate(texto_fim, xy=(xf, yf), xytext=(xf + folga, yr), textcoords='data',
                    ha='left', va='center', fontsize=7, color=_TINTA, fontweight='semibold',
                    annotation_clip=False, arrowprops=seta)
    ax.yaxis.set_major_formatter(_FuncFormatter(lambda v, _: _num_a4(v, 0 if topo >= 10 else 1)))
    rotulo_y = _rotulo_a4(ylabel, nome_arquivo)
    _rotulo_y_a4(ax, rotulo_y)
    if len(itens) > 1:
        if nomes_longos:
            alcas, rotulos_leg = ax.get_legend_handles_labels()
            ax.legend(alcas, [_textwrap.fill(str(r), 70) for r in rotulos_leg], loc='upper left',
                      bbox_to_anchor=(0, -0.12), ncol=1, handlelength=1.6)
        else:
            ax.legend(loc='upper left', bbox_to_anchor=(0, -0.12), ncol=min(len(itens), 4), handlelength=1.6,
                      columnspacing=1.4)
    _salva_a4(fig, nome_arquivo, 'grafico', titulo, fonte_dados, rotulo_y)

def _a4_pequenos_multiplos(df, tempo, itens, titulo, nome_arquivo, ylabel, fonte_dados):
    """Um painel por série; a série em cor, as demais em cinza ao fundo; mesma escala em todos."""
    n = len(itens)
    ncol = 4 if n <= 8 else (5 if n in (9, 10) else 4)
    nlin = math.ceil(n / ncol)
    d = df.sort_values(tempo)
    x = d[tempo].astype(float)
    todos = pd.concat([d[c] for _, c in itens]).astype(float)
    dec = _decimais_a4(todos)
    topo = todos.max() * 1.18 if todos.max() > 0 else 1
    fig, axs = plt.subplots(nlin, ncol, figsize=(_LARGURA_A4, (1.2 + 3.7 * nlin) * _CM), sharex=True, sharey=True,
                            squeeze=False)
    cor = _PALETA_IMPRESSAO[4]
    anos = sorted(x.unique())
    for k, ax in enumerate(axs.flat):
        if k >= n:
            ax.axis('off')
            continue
        rotulo, col = itens[k]
        for _, outra in itens:
            ax.plot(x, d[outra].astype(float), color=_CINZA_CONTEXTO, lw=0.6, zorder=1)
        s = d[[tempo, col]].dropna()
        ax.plot(s[tempo].astype(float), s[col].astype(float), color=cor, lw=1.4, zorder=3)
        if len(s):
            xf, yf = float(s[tempo].iloc[-1]), float(s[col].iloc[-1])
            ax.plot([xf], [yf], 'o', ms=3.2, color=cor, mec='white', mew=0.8, zorder=4)
            ax.annotate(_num_a4(yf, dec), (xf, yf), xytext=(3, 0), textcoords='offset points', ha='left',
                        va='center', fontsize=6.8, fontweight='semibold', annotation_clip=False)
        ax.set_title(_textwrap.fill(str(rotulo), 26), fontsize=7, fontweight='semibold', loc='left', color=_TINTA, pad=3)
        ax.set_ylim(0, topo)
        ax.set_xticks([anos[0], anos[-1]])
        ax.set_xlim(anos[0] - 0.5, anos[-1] + (anos[-1] - anos[0]) * 0.22)
        ax.tick_params(axis='x', labelsize=6.5)
        ax.tick_params(axis='y', labelsize=6.5)
        ax.xaxis.set_major_formatter(_FuncFormatter(lambda v, _: str(int(v))))
    axs[0, 0].yaxis.set_major_formatter(_FuncFormatter(lambda v, _: _num_a4(v, 0 if topo >= 10 else 1)))
    rotulo_y = _rotulo_a4(ylabel, nome_arquivo)
    fig.text(0, 1.0, f'{rotulo_y}  ·  em cinza, as demais séries', fontsize=7.5, color=_TINTA2, ha='left', va='bottom')
    fig.tight_layout(h_pad=1.0, w_pad=0.5)
    _salva_a4(fig, nome_arquivo, 'grafico', titulo, fonte_dados, rotulo_y)

# ------------------------------------------------------------------ barras
@_a4_seguro
def _a4_barras(df, categoria, valor, titulo, nome_arquivo, fonte_dados):
    d = df[[categoria, valor]].copy()
    d = d[~d[categoria].map(_eh_total_a4)]
    if nome_arquivo in _ESCALA_100_A4:
        d[valor] = d[valor] * 100
    cats = [_categoria_a4(c) for c in d[categoria]]
    vals = d[valor].astype(float).tolist()
    dec = _decimais_a4(vals)
    horizontal = max(len(c) for c in cats) > 12 or len(cats) > 8
    rotulo = _rotulo_a4(valor, nome_arquivo)
    cor = _PALETA_IMPRESSAO[0]
    if horizontal:
        fig, ax = plt.subplots(figsize=(_LARGURA_A4, (1.2 + 0.62 * len(cats)) * _CM))
        pos = list(range(len(cats)))[::-1]
        ax.barh(pos, vals, color=cor, height=0.62)
        ax.set_yticks(pos, [_textwrap.fill(c, 34) for c in cats])
        ax.grid(axis='y', visible=False); ax.grid(axis='x', visible=True)
        ax.tick_params(axis='y', length=0); ax.spines['bottom'].set_visible(False); ax.tick_params(axis='x', length=0)
        for p, v in zip(pos, vals):
            ax.annotate(_num_a4(v, dec), (v, p), xytext=(4, 0), textcoords='offset points', va='center',
                        fontsize=7.5, fontweight='semibold')
        ax.set_xlim(0, max(vals) * 1.18)
        ax.xaxis.set_major_formatter(_FuncFormatter(lambda v, _: _num_a4(v, 0)))
        ax.set_xlabel(rotulo, loc='left')
    else:
        fig, ax = plt.subplots(figsize=(_LARGURA_A4, 6.0 * _CM))
        ax.bar(cats, vals, color=cor, width=0.6)
        for c, v in zip(cats, vals):
            ax.annotate(_num_a4(v, dec), (c, v), xytext=(0, 3), textcoords='offset points', ha='center',
                        va='bottom', fontsize=7.5, fontweight='semibold')
        ax.set_ylim(0, max(vals) * 1.15)
        ax.yaxis.set_major_formatter(_FuncFormatter(lambda v, _: _num_a4(v, 0)))
        ax.tick_params(axis='x', length=0)
        ax.set_xlabel(_rotulo_a4(categoria))
        _rotulo_y_a4(ax, rotulo)
    _salva_a4(fig, nome_arquivo, 'grafico', titulo, fonte_dados, rotulo)

@_a4_seguro
def _a4_barras_agrupadas(df, categoria, valor, agrupador, titulo, nome_arquivo, ylabel, ordem_categoria,
                         ordem_agrupador, fonte_dados):
    d = df[[categoria, agrupador, valor]].copy()
    d = d[~d[categoria].map(_eh_total_a4) & ~d[agrupador].map(_eh_total_a4)]
    cats = list(ordem_categoria) if ordem_categoria is not None else list(dict.fromkeys(d[categoria]))
    grupos = list(ordem_agrupador) if ordem_agrupador is not None else list(dict.fromkeys(d[agrupador]))
    grupos = [g for g in grupos if not _eh_total_a4(g)]
    tab = d.pivot_table(index=categoria, columns=agrupador, values=valor, aggfunc='sum').reindex(index=cats, columns=grupos)
    rotulo = _rotulo_a4(ylabel or valor, nome_arquivo)
    dec = _decimais_a4(tab.values.ravel())
    n_barras = len(cats) * len(grupos)
    rot_cats = [_categoria_a4(c) for c in cats]
    horizontal = max(len(c) for c in rot_cats) > 14
    larg = 0.8 / max(len(grupos), 1)
    if horizontal:
        fig, ax = plt.subplots(figsize=(_LARGURA_A4, (1.6 + 0.3 * n_barras + 0.25 * len(cats)) * _CM))
        base = np.arange(len(cats))[::-1]
        for j, g in enumerate(grupos):
            vals = tab[g].values.astype(float)
            ys = base + (len(grupos) - 1) / 2 * larg - j * larg
            ax.barh(ys, vals, height=larg * 0.9, color=_PALETA_IMPRESSAO[j % 8], label=str(g))
            for yv, v in zip(ys, vals):
                if not np.isnan(v):
                    ax.annotate(_num_a4(v, dec), (v, yv), xytext=(3, 0), textcoords='offset points', va='center', fontsize=6.5)
        ax.set_yticks(base, [_textwrap.fill(c, 30) for c in rot_cats])
        ax.grid(axis='y', visible=False); ax.grid(axis='x', visible=True); ax.tick_params(axis='y', length=0)
        ax.xaxis.set_major_formatter(_FuncFormatter(lambda v, _: _num_a4(v, 0)))
        ax.set_xlim(0, np.nanmax(tab.values) * 1.15)
        ax.set_xlabel(rotulo, loc='left')
        ax.legend(loc='lower right', ncol=1)
    else:
        fig, ax = plt.subplots(figsize=(_LARGURA_A4, 6.8 * _CM))
        base = np.arange(len(cats))
        for j, g in enumerate(grupos):
            vals = tab[g].values.astype(float)
            xs = base - 0.4 + larg / 2 + j * larg
            ax.bar(xs, vals, width=larg * 0.9, color=_PALETA_IMPRESSAO[j % 8], label=str(g))
            if n_barras <= 16:
                for xv, v in zip(xs, vals):
                    if not np.isnan(v):
                        ax.annotate(_num_a4(v, dec), (xv, v), xytext=(0, 2), textcoords='offset points',
                                    ha='center', va='bottom', fontsize=6.3)
        ax.set_xticks(base, [_textwrap.fill(c, 16) for c in rot_cats])
        ax.tick_params(axis='x', length=0)
        ax.set_ylim(0, np.nanmax(tab.values) * 1.15)
        ax.yaxis.set_major_formatter(_FuncFormatter(lambda v, _: _num_a4(v, 0)))
        _rotulo_y_a4(ax, rotulo)
        ax.set_xlabel(_rotulo_a4(categoria))
        longos = max((len(str(g)) for g in grupos), default=0) > 18   # nomes longos: uma entrada por linha
        alcas, rotulos_leg = ax.get_legend_handles_labels()
        ax.legend(alcas, [_textwrap.fill(str(r), 70) for r in rotulos_leg], loc='upper left',
                  bbox_to_anchor=(0, -0.16), ncol=1 if longos else min(len(grupos), 4), handlelength=1.2)
    _salva_a4(fig, nome_arquivo, 'grafico', titulo, fonte_dados, rotulo)

@_a4_seguro
def _a4_ranking(df, categoria, valor, titulo, nome_arquivo, xlabel, linha_referencia, rotulo_referencia, cmap,
                fonte_dados):
    d = df.sort_values(valor, ascending=True)
    vals = d[valor].astype(float).tolist()
    dec = _decimais_a4(vals)
    fig, ax = plt.subplots(figsize=(_LARGURA_A4, (1.0 + 0.5 * len(d)) * _CM))
    pos = list(range(len(d)))
    ax.barh(pos, vals, color=plt.get_cmap(cmap)(0.65), height=0.62)
    ax.set_yticks(pos, [_textwrap.fill(str(c), 34) for c in d[categoria]])
    for p, v in zip(pos, vals):
        ax.annotate(_num_a4(v, dec), (v, p), xytext=(3, 0), textcoords='offset points', va='center', fontsize=7)
    if linha_referencia is not None:
        ax.axvline(linha_referencia, color=_TINTA, lw=0.7)
        ax.annotate(rotulo_referencia or _num_a4(linha_referencia, 1), xy=(linha_referencia, 1.0),
                    xycoords=('data', 'axes fraction'), xytext=(3, 0), textcoords='offset points', fontsize=6.8,
                    color=_TINTA2, va='top')
    ax.grid(axis='y', visible=False); ax.grid(axis='x', visible=True); ax.tick_params(axis='y', length=0)
    ax.set_xlim(0, max(vals) * 1.15)
    ax.xaxis.set_major_formatter(_FuncFormatter(lambda v, _: _num_a4(v, 0)))
    rotulo = _rotulo_a4(xlabel or valor, nome_arquivo)
    ax.set_xlabel(rotulo, loc='left')
    _salva_a4(fig, nome_arquivo, 'grafico', titulo, fonte_dados, rotulo)

# ------------------------------------------------------------------ mapas
_TETO_PERCENTIL_A4 = 0.95   # D5: teto de cor dos mapas contínuos por bairro na impressão

@_a4_seguro
def _a4_mapa(gdf, coluna_valor, titulo, nome_arquivo, nivel, bins, cmap, legenda_titulo, fonte_dados, zero_branco,
             caminho_uf, caminho_municipios, teto=None, piso=None):
    # piso (opcional, specs/2026-10-07_deck_familia_moradia): início da escala contínua quando todos os valores
    # estão numa faixa alta (ex. 63-88%); sem ele a escala começa em zero. Só os mapas do deck usam
    # teto (opcional, specs/2026-09-28_apresentacao): limite explícito da escala contínua -- usado pelos mapas da
    # apresentação (ex. RA Centro como outlier no IPS); sem ele, o comportamento de sempre (percentil 95 por bairro).
    # Com teto >= máximo (Tukey sem outliers, specs/2026-09-29_slide_revision), a escala vai até o máximo, sem o P95
    gdf = gdf.to_crs(epsg=3857) if gdf.crs is not None and gdf.crs.to_epsg() != 3857 else gdf
    minx, miny, maxx, maxy = gdf.total_bounds
    padx, pady = (maxx - minx) * 0.02, (maxy - miny) * 0.06
    aspecto = (maxx - minx + 2 * padx) / (maxy - miny + 2 * pady)
    fig, ax = plt.subplots(figsize=(_LARGURA_A4, _LARGURA_A4 / aspecto))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_xlim(minx - padx, maxx + padx); ax.set_ylim(miny - pady, maxy + pady)
    borda = dict(linewidth=0.25, edgecolor='#5f5f5f')
    sem_dado = dict(color='none', edgecolor='#8a8a8a', hatch='////', linewidth=0.3)
    nota_teto = ''
    rotulo_leg = str(legenda_titulo or coluna_valor)
    if bins:
        eh_zero = (gdf[coluna_valor] == 0) if zero_branco else pd.Series(False, index=gdf.index)
        lim = [min(gdf[coluna_valor].min(), bins[0]) - 1] + list(bins) + [max(gdf[coluna_valor].max(), bins[-1])]
        rot = ([f'Até {_numero_ptbr(bins[0])}'] + [f'{_numero_ptbr(bins[i-1]+1)} a {_numero_ptbr(bins[i])}' for i in range(1, len(bins))]
               + [f'Mais de {_numero_ptbr(bins[-1])}'])
        faixa = pd.cut(gdf[coluna_valor].where(~eh_zero), bins=lim, labels=rot, ordered=True)
        cores = plt.get_cmap(cmap)(np.linspace(0.12, 0.92, len(rot)))
        handles, labels = [], []
        if zero_branco and eh_zero.any():
            gdf[eh_zero].plot(ax=ax, color='white', zorder=2, **borda)
            handles.append(_Patch(facecolor='white', edgecolor='#5f5f5f', linewidth=0.3)); labels.append('0 (sem casos)')
        for i, r in enumerate(rot):
            sel = gdf[faixa == r]
            if len(sel):
                sel.plot(ax=ax, color=cores[i], zorder=2, **borda)
            handles.append(_Patch(facecolor=cores[i], edgecolor='#5f5f5f', linewidth=0.3)); labels.append(r)
        falta = gdf[gdf[coluna_valor].isna()]
        if len(falta):
            falta.plot(ax=ax, zorder=2, **sem_dado)
            handles.append(_Patch(facecolor='white', edgecolor='#8a8a8a', hatch='////', linewidth=0.3)); labels.append('Sem dado')
        leg = ax.legend(handles, labels, title=rotulo_leg, loc='upper left', bbox_to_anchor=(0.012, 0.985),
                        fontsize=7, title_fontsize=7.5, frameon=True, framealpha=0.94, edgecolor='none',
                        handlelength=1.4, handleheight=0.9, borderpad=0.6, labelspacing=0.35, alignment='left')
        leg.get_title().set_fontweight('semibold')
    else:
        valores = gdf[coluna_valor].dropna()
        vmax = float(valores.max()) if len(valores) else 1.0
        if teto is not None and vmax > teto:
            vmax = float(teto)
            nota_teto = f'escala de cor limitada a {_num_a4(vmax, 1)} (valores acima com a cor máxima)'
        elif teto is None and nivel == 'bairro' and len(valores):
            p = float(valores.quantile(_TETO_PERCENTIL_A4))
            if p > 0 and vmax > p * 1.05:
                vmax = p
                nota_teto = f'escala de cor limitada ao percentil {int(_TETO_PERCENTIL_A4 * 100)} ({_num_a4(p, 1)})'
        norma = _Normalize(piso or 0, vmax)
        gdf.plot(column=coluna_valor, ax=ax, cmap=cmap, norm=norma, zorder=2, **borda)
        gdf[gdf[coluna_valor].isna()].plot(ax=ax, zorder=2, **sem_dado)
        cax = ax.inset_axes([0.03, 0.56, 0.022, 0.34])
        cb = fig.colorbar(plt.cm.ScalarMappable(norm=norma, cmap=cmap), cax=cax, extend='max' if nota_teto else 'neither',
                          extendfrac=0.06)
        cb.outline.set_linewidth(0.3)
        cax.tick_params(labelsize=7, length=2, width=0.4, colors=_TINTA)
        halo = [pe.withStroke(linewidth=2.2, foreground='white')]
        cb.set_ticks([t for t in cb.get_ticks() if (piso or 0) <= t <= vmax])
        dec = 0 if vmax >= 10 else 1
        cb.set_ticklabels([_num_a4(t, dec) for t in cb.get_ticks()])
        for t in cax.get_yticklabels():
            t.set_path_effects(halo)
        if nota_teto:
            cax.annotate(f'≥ {_num_a4(vmax, dec)}', xy=(1, 1.07), xycoords='axes fraction', xytext=(3, 0),
                         textcoords='offset points', fontsize=7, va='center', color=_TINTA, path_effects=halo)
        cax.annotate(rotulo_leg.replace('\n', ' '), xy=(0, 1.16), xycoords='axes fraction', fontsize=7.5,
                     fontweight='semibold', va='bottom', ha='left', color=_TINTA, path_effects=halo)
    # contexto: limite estadual, fundo cartográfico reduzido e clareado (menos tinta, mais contraste)
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    gpd.read_file(caminho_uf).to_crs(epsg=3857).clip(box(x0, y0, x1, y1)).boundary.plot(
        ax=ax, color='#d4b106', linewidth=0.7, linestyle=(0, (3, 2)), zorder=1)
    img, ext = ctx.bounds2img(x0, y0, x1, y1, source=_PROVEDORES_FUNDO['mapa_oceano_base'])
    img = (img[..., :3].astype(float) * 0.62 + 255 * 0.38).astype('uint8')
    ax.imshow(img, extent=ext, zorder=0, interpolation='none')   # 'none': sem reamostrar a 300 dpi (PDF ~0,4 MB)
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.annotate('N', xy=(0.965, 0.93), xytext=(0.965, 0.86), xycoords=ax.transAxes, textcoords=ax.transAxes,
                ha='center', va='center', fontsize=8, fontweight='semibold', color=_TINTA,
                arrowprops=dict(arrowstyle='-|>', color=_TINTA, lw=1.0, mutation_scale=10), zorder=5)
    ax.add_artist(ScaleBar(math.cos(math.radians(-22.9)), units='m', location='lower right', box_alpha=0,
                           color=_TINTA, scale_loc='top', border_pad=0.5, width_fraction=0.006, length_fraction=0.16,
                           font_properties={'size': 6.5}))
    _adiciona_rotulos_municipios_vizinhos(ax, ax.get_xlim(), ax.get_ylim(), cor='#5a6570', tamanho=6.5,
                                          caminho_municipios=caminho_municipios)
    for t in ax.texts:
        if t.get_text() != 'N':
            t.set_path_effects([pe.withStroke(linewidth=1.8, foreground='white')])
    ax.annotate('Fundo: Esri, GEBCO, NOAA, National Geographic, DeLorme, NAVTEQ', xy=(0.006, 0.006),
                xycoords='axes fraction', fontsize=4.8, color=_TINTA3, va='bottom')
    ax.axis('off')
    fonte = fonte_dados or ''
    if nota_teto:
        fonte = f'{fonte}. Nota: {nota_teto}; o valor real está na tabela do apêndice'.lstrip('. ')
    _salva_a4(fig, nome_arquivo, 'mapa', titulo, fonte, rotulo_leg.replace('\n', ' '))
