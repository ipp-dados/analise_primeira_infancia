# -*- coding: utf-8 -*-
"""### 📈 Funções de visualização

Todas salvam o gráfico em `visualizacoes/` como PNG. A exportação adicional em SVG fica
disponível, mas comentada, em cada função — descomente a linha `# plt.savefig(...svg...)`
quando precisar de um formato vetorial.

Extraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b).
"""
import matplotlib.pyplot as plt
import seaborn as sns
from .estilo import (_COR_FONTE_RODAPE, _COR_SERIE_APAGADA, _FONTE_TITULO, _LIMIAR_DESTAQUE_SERIES, _N_SERIES_DESTACADAS, _PALETA_CATEGORICA)
from .impressao import _a4_barras, _a4_barras_agrupadas, _a4_serie_unica, _a4_series

__all__ = [
    '_rodape_fonte',
    'serie_temporal',
    'grafico_barra',
    'grafico_barra_agrupado',
    'serie_temporal_multipla',
]


def _rodape_fonte(fonte_dados):
    """Desenha 'Fonte: ...' discreto no canto inferior direito da figura -- mesma ideia do
    footnote dos mapas, aplicada aos gráficos de série/barra. No-op se fonte_dados for None."""
    if fonte_dados:
        plt.figtext(0.99, 0.01, f'Fonte: {fonte_dados}', ha='right', va='bottom',
                    fontsize=7, style='italic', color=_COR_FONTE_RODAPE)

def serie_temporal(df,tempo,valor,titulo,nome_arquivo=None, formato='png', fonte_dados=None):
    nome_arquivo = nome_arquivo or f"{valor}_{tempo}"
    plt.figure(figsize=(12,6))
    sns.lineplot(x=tempo,y=valor,data=df, color=_PALETA_CATEGORICA[0], marker='o')
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xlabel(tempo,fontsize=12)
    plt.ylabel(valor,fontsize=12)
    plt.title(titulo,fontsize=15,fontfamily=_FONTE_TITULO,fontweight='bold',pad=12)
    plt.grid(True,alpha=0.25)
    _rodape_fonte(fonte_dados)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    _a4_serie_unica(df, tempo, valor, titulo, nome_arquivo=nome_arquivo, fonte_dados=fonte_dados)
    # plt.savefig(f"visualizacoes/{nome_arquivo}.svg")  # descomente para exportar também em SVG
    plt.show()

def grafico_barra(df,categoria,valor,titulo,nome_arquivo=None, formato='png', fonte_dados=None):
    nome_arquivo = nome_arquivo or f"{valor}_{categoria}"
    plt.figure(figsize=(10,6))
    sns.barplot(x=categoria,y=valor,data=df,palette=_PALETA_CATEGORICA,hue=categoria,legend=False)
    plt.xlabel(categoria,fontsize=12)
    plt.ylabel(valor, fontsize=12)
    plt.title(titulo,fontsize=15,fontfamily=_FONTE_TITULO,fontweight='bold',pad=12)
    _rodape_fonte(fonte_dados)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    _a4_barras(df, categoria, valor, titulo, nome_arquivo=nome_arquivo, fonte_dados=fonte_dados)
    # plt.savefig(f"visualizacoes/{nome_arquivo}.svg")  # descomente para exportar também em SVG
    plt.show()

def grafico_barra_agrupado(df,categoria,valor,agrupador,titulo,nome_arquivo,ylabel=None,legend_title=None,ordem_categoria=None,ordem_agrupador=None,rotacao_x=30,figsize=(12,7),formato='png', fonte_dados=None):
    plt.figure(figsize=figsize)
    sns.barplot(data=df, x=categoria, y=valor, hue=agrupador, order=ordem_categoria, hue_order=ordem_agrupador, palette=_PALETA_CATEGORICA)
    plt.xlabel(categoria,fontsize=12)
    plt.ylabel(ylabel or valor, fontsize=12)
    plt.title(titulo,fontsize=15,fontfamily=_FONTE_TITULO,fontweight='bold',pad=12)
    plt.xticks(rotation=rotacao_x, ha='right' if rotacao_x else 'center')
    plt.legend(title=legend_title or agrupador, fontsize=9)
    _rodape_fonte(fonte_dados)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    _a4_barras_agrupadas(df, categoria, valor, agrupador, titulo, nome_arquivo=nome_arquivo, ylabel=ylabel,
                         ordem_categoria=ordem_categoria, ordem_agrupador=ordem_agrupador, fonte_dados=fonte_dados)
    # plt.savefig(f"visualizacoes/{nome_arquivo}.svg")  # descomente para exportar também em SVG
    plt.show()

def serie_temporal_multipla(df,tempo,colunas,titulo,nome_arquivo,ylabel='Valor',legend_title='Cor/Raça',figsize=(12,6),formato='png', fonte_dados=None, destaques=None, linhas_referencia=None):
    """`linhas_referencia`: lista opcional de `(valor, rótulo)` desenhada como linha horizontal tracejada
    cinza, com o rótulo à direita (ex.: metas do PNE). `None` (padrão) não desenha nada."""
    plt.figure(figsize=figsize)
    itens = list(colunas.items())
    if len(itens) > _LIMIAR_DESTAQUE_SERIES:
        mapa_colunas = dict(itens)
        if destaques is None:
            def _valor_final(coluna):
                serie = df[coluna].dropna()
                return serie.iloc[-1] if len(serie) else float('-inf')
            destaques = sorted((r for r, _ in itens), key=lambda r: _valor_final(mapa_colunas[r]), reverse=True)[:_N_SERIES_DESTACADAS]
        cor_idx = 0
        for rotulo,coluna in itens:
            if rotulo in destaques:
                sns.lineplot(x=tempo,y=coluna,data=df,label=rotulo,marker='o',errorbar=None,
                             color=_PALETA_CATEGORICA[cor_idx % len(_PALETA_CATEGORICA)], linewidth=2.2, zorder=3)
                cor_idx += 1
            else:
                sns.lineplot(x=tempo,y=coluna,data=df,marker=None,errorbar=None,legend=False,
                             color=_COR_SERIE_APAGADA, alpha=0.6, linewidth=1.1, zorder=1)
        plt.plot([],[],color=_COR_SERIE_APAGADA,alpha=0.6,linewidth=1.1,
                 label=f'Outras ({len(itens) - len(destaques)})')
    else:
        for i,(rotulo,coluna) in enumerate(itens):
            sns.lineplot(x=tempo,y=coluna,data=df,label=rotulo,marker='o',errorbar=None,
                         color=_PALETA_CATEGORICA[i % len(_PALETA_CATEGORICA)])
    for valor, rotulo_ref in (linhas_referencia or []):
        plt.axhline(valor, color='#6b6b6b', linestyle='--', linewidth=1.1, zorder=0)
        plt.annotate(rotulo_ref, xy=(1, valor), xycoords=('axes fraction', 'data'), xytext=(-4, 3),
                     textcoords='offset points', ha='right', va='bottom', fontsize=9, color='#3a3a3a', style='italic')
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xlabel(tempo,fontsize=12)
    plt.ylabel(ylabel,fontsize=12)
    plt.title(titulo,fontsize=15,fontfamily=_FONTE_TITULO,fontweight='bold',pad=12)
    plt.legend(title=legend_title,fontsize=9)
    plt.grid(True,alpha=0.3)
    _rodape_fonte(fonte_dados)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    _a4_series(df, tempo, colunas, titulo, nome_arquivo=nome_arquivo, ylabel=ylabel, fonte_dados=fonte_dados,
               linhas_referencia=linhas_referencia)
    # plt.savefig(f"visualizacoes/{nome_arquivo}.svg")  # descomente para exportar também em SVG
    plt.show()
