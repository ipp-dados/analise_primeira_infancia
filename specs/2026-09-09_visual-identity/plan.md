# Plano técnico — Identidade Visual Unificada + Exports HTML/PDF

Decisões confirmadas (ver `specs.md` §4): A=sim (1 HTML só), B=sim (só
visualização, sem prosa), C=6 séries, D=200 DPI, E=sim (PDF ganha o
conteúdo novo), F=sim (manter `*.html` fora do git).

## 1. Módulo de estilo compartilhado (`analise.py`)

Novas constantes, adicionadas logo após `_FONTE_TITULO`/`_ZONA_LEGENDA`
(linha ~401-405, já usadas por `mapa_coropletico_bairros`; ficam acessíveis
também às 4 funções de plot de série/barra, que são chamadas só depois,
nunca definidas-e-executadas na mesma célula):

```python
# paleta categórica de 11 cores -- mesmos hex do motor JS de relatorio/index.html
# (--c1..--c11), para a mesma série ter a mesma cor no notebook, no PDF e no HTML.
_PALETA_CATEGORICA = ['#6a95c8', '#d28060', '#66cca7', '#deb254', '#ca688d',
                       '#54de54', '#8177bb', '#cc6766', '#bc9776', '#b67c99', '#8e9ea4']

# matiz sequencial por tema, usado por mapa_coropletico_bairros no lugar do
# 'Oranges' fixo -- mesma lógica "um matiz só por mapa" (magnitude), variando
# o matiz conforme o assunto (ver specs.md §3.1)
_CORES_TEMA_MAPA = {
    'natalidade': 'BuGn',    # nascidos vivos, baixo peso
    'mortalidade': 'RdPu',   # óbitos (neonatal, gravidez, puerpério, raça, evitáveis/CAP)
    'cadunico': 'YlOrBr',    # CadÚnico
    'censo': 'Blues',        # Censo/população
}

_LIMIAR_DESTAQUE_SERIES = 6  # acima disso, serie_temporal_multipla destaca só as mais relevantes
_N_SERIES_DESTACADAS = 4
_COR_SERIE_APAGADA = '#c9c9c9'

_COR_FONTE_RODAPE = '#5E6D68'  # mesmo tom neutro do --ink-2 do relatorio HTML

def _rodape_fonte(fonte_dados):
    """Desenha 'Fonte: ...' discreto no canto inferior direito da figura -- mesma ideia do
    footnote dos mapas, aplicada aos gráficos de série/barra. No-op se fonte_dados for None
    (mantém compatibilidade com qualquer chamada residual sem o parâmetro)."""
    if fonte_dados:
        plt.figtext(0.99, 0.01, f'Fonte: {fonte_dados}', ha='right', va='bottom',
                    fontsize=7, style='italic', color=_COR_FONTE_RODAPE)
```

### 1.1 `serie_temporal` -- adiciona `fonte_dados`, título serifado, rodapé, DPI 200

```python
def serie_temporal(df,tempo,valor,titulo,nome_arquivo=None, formato='png', fonte_dados=None):
    nome_arquivo = nome_arquivo or f"{valor}_{tempo}"
    plt.figure(figsize=(12,6))
    sns.lineplot(x=tempo,y=valor,data=df, color=_PALETA_CATEGORICA[0], marker='o')
    plt.xlabel(tempo,fontsize=12)
    plt.ylabel(valor,fontsize=12)
    plt.title(titulo,fontsize=15,fontfamily=_FONTE_TITULO,fontweight='bold',pad=12)
    plt.grid(True,alpha=0.25)
    _rodape_fonte(fonte_dados)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    plt.show()
```

### 1.2 `grafico_barra` -- troca `palette='pastel'` (genérico do seaborn) pela paleta do projeto

```python
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
    plt.show()
```
(`legend=False` porque `hue=categoria` já colore cada barra por ela mesma --
uma legenda redundante repetindo os rótulos do eixo X não agrega, mas os
rótulos do eixo X continuam sendo a "legenda" exigida por specs.md §3.2.)

### 1.3 `grafico_barra_agrupado` -- aplica a paleta ao `hue`

```python
def grafico_barra_agrupado(df,categoria,valor,agrupador,titulo,nome_arquivo,ylabel=None,legend_title=None,ordem_categoria=None,ordem_agrupador=None,rotacao_x=30,figsize=(12,7),formato='png', fonte_dados=None):
    plt.figure(figsize=figsize)
    sns.barplot(data=df, x=categoria, y=valor, hue=agrupador, order=ordem_categoria,
                hue_order=ordem_agrupador, palette=_PALETA_CATEGORICA)
    plt.xlabel(categoria,fontsize=12)
    plt.ylabel(ylabel or valor, fontsize=12)
    plt.title(titulo,fontsize=15,fontfamily=_FONTE_TITULO,fontweight='bold',pad=12)
    plt.xticks(rotation=rotacao_x, ha='right' if rotacao_x else 'center')
    plt.legend(title=legend_title or agrupador, fontsize=9)
    _rodape_fonte(fonte_dados)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    plt.show()
```

### 1.4 `serie_temporal_multipla` -- paleta fixa por posição + destaque acima do limiar

```python
def serie_temporal_multipla(df,tempo,colunas,titulo,nome_arquivo,ylabel='Valor',legend_title='Cor/Raça',figsize=(12,6),formato='png', fonte_dados=None, destaques=None):
    plt.figure(figsize=figsize)
    itens = list(colunas.items())
    if len(itens) > _LIMIAR_DESTAQUE_SERIES:
        if destaques is None:
            # top _N_SERIES_DESTACADAS pelo último valor não-nulo de cada série
            def _valor_final(coluna):
                serie = df[coluna].dropna()
                return serie.iloc[-1] if len(serie) else float('-inf')
            destaques = sorted((r for r,_ in itens), key=lambda r: _valor_final(dict(itens)[r]), reverse=True)[:_N_SERIES_DESTACADAS]
        cor_idx = 0
        for rotulo, coluna in itens:
            if rotulo in destaques:
                sns.lineplot(x=tempo,y=coluna,data=df,label=rotulo,marker='o',errorbar=None,
                             color=_PALETA_CATEGORICA[cor_idx % len(_PALETA_CATEGORICA)], linewidth=2.2, zorder=3)
                cor_idx += 1
            else:
                sns.lineplot(x=tempo,y=coluna,data=df,marker=None,errorbar=None,legend=False,
                             color=_COR_SERIE_APAGADA, alpha=0.6, linewidth=1.1, zorder=1)
        plt.plot([],[],color=_COR_SERIE_APAGADA,alpha=0.6,linewidth=1.1,
                 label=f'Outras ({len(itens)-len(destaques)})')
    else:
        for i,(rotulo,coluna) in enumerate(itens):
            sns.lineplot(x=tempo,y=coluna,data=df,label=rotulo,marker='o',errorbar=None,
                         color=_PALETA_CATEGORICA[i % len(_PALETA_CATEGORICA)])
    plt.xlabel(tempo,fontsize=12)
    plt.ylabel(ylabel,fontsize=12)
    plt.title(titulo,fontsize=15,fontfamily=_FONTE_TITULO,fontweight='bold',pad=12)
    plt.legend(title=legend_title,fontsize=9)
    plt.grid(True,alpha=0.3)
    _rodape_fonte(fonte_dados)
    plt.tight_layout()
    plt.savefig(f"visualizacoes/{nome_arquivo}.{formato}", dpi=200, bbox_inches='tight')
    plt.show()
```

`destaques` (lista de rótulos) permite curadoria manual quando o "top N pelo
valor final" não for a escolha certa (ex.: cobertura vacinal pode preferir
destacar vacinas específicas em vez das 4 com maior cobertura em 2025).
Decidir caso a caso durante o Bloco 4 (abaixo), olhando cada gráfico
renderizado.

## 2. Mapas -- `cmap` por tema (25 call sites)

`mapa_coropletico_bairros` já aceita `cmap` (default `'Oranges'`, nunca
sobrescrito em nenhuma chamada hoje). Adiciona `cmap=_CORES_TEMA_MAPA['...']`
em cada uma das 25 chamadas:

| Tema | Linhas (chamadas) | Indicadores |
|---|---|---|
| `censo` | 758, 768, 799, 807 | Censo 0-4 anos (bairro/AP/RP, abs+%) |
| `cadunico` | 1013, 1033, 1038 | CadÚnico crianças/primeira infância |
| `natalidade` | 1075, 1116, 1121 | Nascidos vivos, baixo peso |
| `mortalidade` | 1277, 1282, 1852, 1861, 1895, 1959, 1992, 2035, 2040, 2075, 2080, 2144, 2149, 2166, 2171 | Óbitos por raça, evitáveis/CAP (geral + subgrupo), gravidez, puerpério, neonatal precoce/tardia/pós/total |

Depois de gerar os 25 mapas com o novo `cmap`, verificar visualmente (Bloco
5) se a classe mais clara de cada tema ainda tem contraste suficiente sobre
o basemap -- `BuGn`/`Blues`/`YlOrBr`/`RdPu` são rampas ColorBrewer
sequenciais, mas a tonalidade mais clara de cada uma pode precisar de um
`vmin`/ajuste de opacidade se ficar ilegível (mesmo tipo de ajuste iterativo
documentado na skill `generate_map`).

## 3. Rodapé de fonte + paleta nos ~48 call sites restantes

`serie_temporal` (13), `serie_temporal_multipla` (22), `grafico_barra` (5) e
`grafico_barra_agrupado` (8) ainda não passam `fonte_dados` (parâmetro novo,
§1). Cada chamada ganha `fonte_dados=fonte_<seção>` reaproveitando a
constante já definida na seção (`fonte_censo`, `fonte_cadunico`,
`fonte_datasus_bairro`, `fonte_evitaveis_cap`) quando a chamada está dentro
do escopo dessa seção; para seções sem uma constante `fonte_*` ainda
(SISVAN, PNAD/matrículas, SIDRA educação) definir uma nova constante no
mesmo padrão, ao lado dos dados sendo carregados -- não inventar o texto na
própria chamada do gráfico. Isto é levantado célula a célula no Bloco 3
(abaixo), organizado pelas mesmas seções de `analise.py`.

## 4. `relatorio/` -- consolidar em 1 HTML, remover prosa, cobrir conteúdo novo

### 4.1 Problema com o processo atual

`relatorio/specs.md` já documenta que os 3 arquivos HTML foram montados por
"scripts Python ad-hoc" (não versionados) que embutem os dados de
`tabelas_finais/*.csv` como JSON inline. Sem esses scripts salvos, cada
atualização até hoje foi uma edição direta dos milhares de linhas do HTML --
inviável para adicionar ~35 visualizações novas e ainda reduzir para 1
arquivo.

### 4.2 Decisão de arquitetura para esta rodada

Persistir um script de build real (novo:
`.claude/skills/export_pdf_report/scripts/build_html_report.py`, ao lado do
script irmão que já monta o PDF) que:
1. Lê `tabelas_finais/*.csv` (mesma fonte que o PDF já usa) e monta um único
   dicionário `{ secao: [ {tipo, titulo, fonte, dados...} ] }`.
2. Reaproveita o motor JS existente (`lineChart`/`barChart`/`groupedBarChart`
   -- extraído do `lighter_index.html` atual para dentro do script/template)
   -- **sem reescrever o motor de gráfico**, só o pipeline de geração.
3. Renderiza **um** `relatorio/index.html`, tema claro/escuro automático via
   `prefers-color-scheme` (a base de variáveis CSS já existe nos 3 arquivos
   atuais -- reaproveitar, não reinventar).
4. Cada visualização vem só com **título + fonte + o gráfico/mapa +
   alternância "ver tabela"** -- sem as notas de markdown que hoje
   acompanham cada seção (removidas, por B em `specs.md`).
5. Nova seção "🗺️ Mapas" cobre os ~25 mapas atuais (hoje só 5 estavam
   embutidos) -- mesma técnica de redimensionar para WebP ~1400px já usada
   em `lighter_index.html`/`white_index.html`.
6. Séries com >6 linhas (§1.4) recebem o mesmo tratamento de destaque no
   motor JS -- portar a lógica de `_N_SERIES_DESTACADAS`/cinza-apagado para
   `lineChart`.

`index.html` e `lighter_index.html`/`white_index.html` (as 2 variantes
antigas) são removidos do diretório depois que o novo `index.html`
consolidado estiver validado -- ficam só como histórico no git (arquivo
ignorado, então nem isso; a remoção é só local).

## 5. PDF -- `export_pdf_report`

Reexecutar o pipeline já documentado na skill (`regen_missing_pngs.py` →
`extract_maps.py` → `build_notebook_report.py` → Chrome headless), com dois
ajustes:
- `extract_maps.py` deve ler os mapas do novo `relatorio/index.html`
  consolidado (só 1 arquivo agora, não mais `white_index.html`).
- `build_notebook_report.py` precisa de novas entradas de seção para os ~35
  gráficos/mapas de `specs/2026-09-09_maps-and-ibge` que ainda não estão no template
  (ele é "uma transcrição direta das células de `analise.py`" -- precisa
  acompanhar as células novas).
- Estilo herdado automaticamente do notebook: como o PDF usa os PNGs reais
  de `visualizacoes/`/`mapas/`, os Blocos 1-2 (paleta, DPI, cmap por tema,
  rodapé de fonte) aparecem no PDF sem trabalho extra -- só precisa rodar
  DEPOIS que analise.py estiver com o novo estilo.

## 6. Ordem de execução

Blocos 1-2 (analise.py) → Bloco 3 (rodapés/paleta nos call sites restantes)
→ validação completa do notebook (0 erros) → Bloco 4 (HTML) → Bloco 5 (PDF)
→ documentação → merge (gated).
