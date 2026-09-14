# Plano técnico — Relatório Interativo (`relatorio/index.html` v6)

Decisões confirmadas (ver `specification.md` §4): A=h2 só, B=Tukey
1.5×IQR pré-computado, C=navbar só h2, D=download por gráfico, E=pills
sempre, F=esta rodada é spec+layout (já entregue — agora entra a
implementação), G=tooltip em mapas dentro do escopo (sem faseamento),
H=tooltip com rótulo+valor em todo ponto, I=máx/mín/recente sempre
visíveis em série temporal, J=GitHub Pages via Actions, K=logo real
(pendência de autorização), L=navy só em linha/rodapé/chip, M=rodapé
enxuto, N=opção A (barra de espectro) + eyebrow consistente entre
header e seções expandidas.

Tudo isto é gerado por `.claude/skills/export_pdf_report/scripts/build_html_report.py`
— não há edição manual do HTML. O motor JS (`lineChart`/`barChart`/
`groupedBarChart`) vive embutido como string de template dentro desse
script (mesmo padrão herdado de `SPEC-visual-identity/plan.md` Bloco 6) —
este plano estende esse mesmo arquivo, não cria um novo pipeline.

## 1. Esquema de dado — chart-card com opções nomeadas

Hoje cada corte de dado vira um `dict` independente que o gerador
transforma em 1 `<div class="out">`. Passa a existir um nível acima,
agrupando N cortes correlatos (mesmo eixo/unidade, diferindo só pela
categoria/CAP/subgrupo selecionado) em **1** chart-card:

```python
{
  "tipo": "line" | "bar" | "grouped_bar" | "map",
  "titulo_base": "Óbitos evitáveis por subgrupo de causa",
  "opcoes": [
    {
      "label": "1 · Imunoprevenção",
      "series": {...},              # mesmo shape que a função de chart já recebe hoje
      "series_sem_outliers": {...},  # mesmo shape, outliers removidos (Bloco 2)
    },
    {"label": "2 · Atenção à gestante", "series": {...}, "series_sem_outliers": {...}},
    ...
  ],
  "fonte_dados": "DataSUS/Tabnet — SIM, óbitos 0–364 dias por causa evitável",
}
```

- Para os casos hoje já de opção única (a maioria dos gráficos do
  relatório), `opcoes` tem 1 item só — o card renderiza sem a coluna de
  pills (nenhuma mudança visual onde não há repetição a resolver).
- `tipo: "map"` carrega, em vez de `series`, a geometria SVG já resolvida
  por opção (Bloco 3) — `paths: [{d, codigo, label, valor, valor_sem_outliers, fill}]`.
- Função nova no gerador, `agrupa_em_chart_card(cortes, criterio_grupo)`,
  substitui as chamadas que hoje emitem N `div.out` soltos — usada nos 4
  pontos identificados em `specification.md` §0.1/§2: CID-10 (~18→1),
  CAP evitáveis (6-8→1), cobertura vacinal por ano, evitáveis por
  subgrupo×CAP.

## 2. Outliers — cercas de Tukey, pré-computadas

```python
def remove_outliers_tukey(valores):
    """valores: list[float|None]. Retorna list[float|None] do mesmo tamanho,
    com outliers substituídos por None (não removidos do array -- mantém o
    eixo temporal/categórico alinhado entre a série com e sem outliers)."""
    finitos = [v for v in valores if v is not None]
    if len(finitos) < 4:          # Tukey não é confiável com poucos pontos
        return list(valores)
    q1, q3 = np.percentile(finitos, [25, 75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [v if (v is None or lo <= v <= hi) else None for v in valores]
```

- Chamada por série/corte individualmente (não por seção inteira) — cada
  `opcoes[i]["series_sem_outliers"]` é `remove_outliers_tukey` aplicado a
  cada série dentro de `opcoes[i]["series"]`.
- Mapas: mesma função aplicada ao array de `valor` por região antes de
  gerar o `fill` da variante sem-outliers (Bloco 3) — os polígonos cujo
  valor virou `None` recebem um `fill` neutro (`var(--surface-2)`) em vez
  de sumir do mapa (a geometria continua lá, só a cor de magnitude some).
- `lineChart`/`barChart`/`groupedBarChart` (motor JS) ganham um 2º array
  opcional por série; o toggle de outliers troca só qual array é lido,
  sem lógica estatística no cliente.

## 3. Mapas — geometria GeoJSON → paths SVG

Novo módulo no gerador (`mapas_svg.py`, ou uma seção nova dentro de
`build_html_report.py` — decidir no Bloco 3 conforme o tamanho real do
código), chamado uma vez por nível (`bairro`/`ap`/`rp`) e reaproveitado
por todo indicador que precisar de mapa naquele nível:

```python
def carrega_geometria_svg(nivel, largura=760, altura=620):
    """Lê dados_locais/geo/limite_bairros_rio.geojson (mesmo arquivo que
    generate_map usa), dissolve por nivel quando != 'bairro' (mesmas
    colunas: area_plane / cod_rp), projeta para um viewBox fixo e devolve
    {codigo: {"d": "M...Z", "label": nome}} -- 1x por nível, cacheado."""
    gdf = geopandas.read_file("dados_locais/geo/limite_bairros_rio.geojson")
    if nivel != "bairro":
        col = {"ap": "area_plane", "rp": "cod_rp"}[nivel]
        gdf = gdf.dissolve(by=col, as_index=False)
    gdf = normaliza_para_viewbox(gdf, largura, altura)   # escala/inverte Y (SVG y cresce p/ baixo)
    return {
        row[_CHAVE[nivel]]: {"d": poligono_para_path_d(row.geometry), "label": row["nome"]}
        for _, row in gdf.iterrows()
    }

def monta_mapa_svg_card(df, coluna_valor, nivel, tema, fonte_dados):
    """df: 1 linha por bairro/AP/RP, já filtrada para a opção ativa.
    tema: chave de _CORES_TEMA_MAPA (specs.md §3.1: natalidade/mortalidade/cadunico/censo).
    Retorna a lista `paths` do esquema do Bloco 1, com fill calculado em
    Python (classificação sequencial, mesma lógica de bins que
    mapa_coropletico_bairros já usa em analise.py -- reaproveitar
    _NIVEIS_AGREGACAO/bins por nível em vez de reimplementar)."""
    geo = carrega_geometria_svg(nivel)
    escala = matplotlib.cm.get_cmap(_CORES_TEMA_MAPA[tema])
    ...
```

- **Sem `contextily`/basemap no SVG** (decisão §3.5 item 6/§7) — só os
  polígonos + tooltip. O footnote de fonte/CRS, título serifado e
  legenda continuam como marcação HTML ao lado do `<svg>`, não dentro
  dele.
- `poligono_para_path_d` precisa lidar com `MultiPolygon` (alguns
  bairros/dissoluções por CAP podem gerar ilhas/múltiplos anéis) —
  concatenar um `d` por anel, mesma técnica que qualquer conversor
  shapely→SVG usa (`M x,y L x,y ... Z` por anel, sem `fill-rule`
  especial necessário pois os anéis de bairro não se sobrepõem).
- Reaproveita a paleta sequencial por tema já definida
  (`_CORES_TEMA_MAPA`, `SPEC-visual-identity/plan.md` §1) — não inventa
  uma nova.

## 4. Motor JS — novos controladores

Adicionados ao template JS embutido em `build_html_report.py` (mesmo
arquivo de `lineChart`/`barChart`/`groupedBarChart`, sem nova
dependência — ver `specification.md` §5):

```js
// seletor de opção por chart-card
function chartOptionSwitcher(cardEl, opcoes, renderFn) {
  let ativa = 0;
  function render() { renderFn(cardEl, opcoes[ativa]); }
  cardEl.querySelectorAll('.pill').forEach((pill, i) => {
    pill.onclick = () => { ativa = i; render(); marcaPillAtiva(cardEl, i); };
  });
  render();
}

// collapse por seção (h2)
function sectionToggle(sectionEl, btnEl) {
  let aberta = true;
  btnEl.onclick = () => {
    aberta = !aberta;
    sectionEl.querySelector('.section-body').hidden = !aberta;
    btnEl.textContent = aberta ? 'RECOLHER' : 'EXPANDIR';
  };
}

// toggle de outliers por chart-card -- troca o array lido, re-renderiza
function outlierToggle(cardEl, renderFn, opcaoAtiva) {
  let semOutliers = false;
  cardEl.querySelector('.outlier-toggle').onclick = () => {
    semOutliers = !semOutliers;
    renderFn(cardEl, opcaoAtiva(), semOutliers);
  };
}

// download CSV -- serializa o array já embutido, sem round-trip de rede
function downloadCsv(filename, headers, rows) {
  const csv = [headers, ...rows].map(r => r.map(csvEscape).join(',')).join('\n');
  const blob = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = filename; a.click();
}
```

- `lineChart` ganha a lógica de rótulo fixo máx/mín/recente
  (`specification.md` §3.9) — 3 linhas de código sobre o array já
  recebido (`Math.max`/`Math.min`/último índice não-nulo), sem precisar
  de dado extra do Python.
- Tooltip de mapa reaproveita a função de tooltip que `lineChart`/
  `barChart` já têm — só troca o alvo do listener de `<circle>`/`<rect>`
  para `<path>` (bairro/CAP), lendo `data-label`/`data-valor` do próprio
  elemento em vez de um array em closure.

## 5. CSS — camada institucional + barra de espectro

Variáveis novas (§3.10, junto das já existentes `--ink`/`--page`/...):

```css
--ipp-navy: #004a80;
--ipp-cyan: #00aeef;
```

- Barra de 4px `background: var(--ipp-navy)` no topo da página (antes da
  navbar).
- Eyebrow do header + eyebrow de seção **expandida**:
  `color: var(--accent-ink); font-weight: 700` (reaproveita `--accent-ink`
  já existente, não é cor nova). Eyebrow de seção **recolhida**: mantém o
  `.eyebrow` padrão (`--ink-3`, peso normal) — é o sinal de estado, não
  uma inconsistência (§3.12).
- Barra de espectro: `<div>` flex com 11 filhos `flex:1`, um `background`
  por `--c1`…`--c11`, 6px de altura, só embaixo do bloco de
  título/descrição (não se repete por seção).
- Chip do logo no navbar: `background: var(--ipp-navy)` em volta do
  `<img>` (o logo é monocromático branco — precisa de fundo escuro).
- Rodapé: `background: var(--ipp-navy)`, tokens de texto claro
  (`#EAF2F8`/`#DCE9F2`/`#7FA9C6`, ver Bloco 6), sem alterar nenhum token
  do corpo do relatório.
- Bordas brutalistas: cartões novos (chart-card, seção, callout de
  achados) usam `border: 2px solid var(--ink); border-radius: 0` em vez
  de `box-shadow: var(--shadow)` — cartões/gráficos já existentes que
  não fazem parte desta rodada não são tocados.

## 6. Rodapé — geração dinâmica

```python
def monta_rodape(data_geracao):
    return {
        "fontes": ["Censo 2022 (IBGE)", "CadÚnico", "DataSUS/Tabnet", "SISVAN · IBGE SIDRA"],
        "links": [
            ("ipp.prefeitura.rio", "https://ipp.prefeitura.rio/"),
            ("Transparência Rio", "https://transparencia.rio/"),   # confirmar URL exata no Bloco 6
            ("LGPD — Proteção de dados", "https://ipp.prefeitura.rio/lgpd/"),  # idem
        ],
        "contato": "ascom.ipp@prefeitura.rio",   # confirmar se é o e-mail certo para este relatório
        "atualizado_em": data_geracao.strftime("%-d de %B de %Y"),  # locale pt-BR
    }
```

- `data_geracao` = `datetime.now()` no momento do build — o rodapé
  sempre reflete a última geração, não uma data hardcoded.
- URLs de Transparência Rio/LGPD e o e-mail de contato do mockup eram
  ilustrativos (copiados do rodapé real do site) — **confirmar os
  corretos para este relatório especificamente antes de finalizar o
  Bloco 6**, não assumir que são os mesmos do site institucional
  principal sem checar.

## 7. Navbar persistente

- Sticky (`position: sticky; top: 0`), substitui o bloco "Sumário" atual
  (que é removido do fluxo da página).
- Hambúrguer abre um painel com os 9 links `h2` (emoji + título,
  `href="#id-da-secao"`) — mesmos `id` que os `h2` já usam hoje (âncoras
  não mudam, só a UI que lista elas).
- Chip do logo institucional (Bloco 5) no lado oposto ao hambúrguer.

## 8. Deploy — GitHub Actions → GitHub Pages

```yaml
# .github/workflows/deploy-relatorio.yml
name: Deploy relatório
on:
  workflow_dispatch: {}
permissions:
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: ${{ steps.deployment.outputs.page_url }} }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: relatorio/   # ou um dir temporário com só index.html, decidir no Bloco 8
      - id: deployment
        uses: actions/deploy-pages@v4
```

- Gatilho `workflow_dispatch` só (manual) nesta primeira versão —
  push-trigger automático fica para depois, se for pedido
  (`specification.md` §5.1 já deixa isso em aberto).
- `path: relatorio/` publicaria também `Page 1.pdf`/`analise_primeira_infancia.pdf`
  junto — **decidir no Bloco 8** se isso é aceitável (ambos já são
  públicos/institucionais) ou se o workflow deve copiar só `index.html`
  para um diretório à parte antes do upload.

## 9. Ordem de execução

Bloco 1 (esquema de dado) → Bloco 2 (outliers) → Bloco 3 (mapas SVG,
maior item de esforço) → Bloco 4 (motor JS) → Bloco 5 (CSS
institucional) → Bloco 6 (rodapé) → Bloco 7 (navbar) → geração completa
+ validação manual (Bloco 8 de `tasks.md`) → Bloco 9 (deploy) → Bloco 10
(documentação/fechamento). Blocos 1-2 e 4-5 podem ser feitos em paralelo
por serem independentes; Bloco 3 é o único que bloqueia Bloco 8
(validação) por completo, então começar cedo.

## 10. Replanejamento — texto por opção, tema único, outliers só em taxas,
agrupamento (specification.md §3.3/§3.13-15/§9)

### 10.1 `option_card`: texto vira parte da opção

Assinatura muda de `entries: list[(label, build_fn)]` para
`entries: list[(label, build_fn, texto)]`. `build_fn` continua emitindo 1
construto (gráfico/mapa); `texto` é uma string (lorem ipsum nesta rodada,
~500 palavras) renderizada num painel próprio, alternado junto com o painel
do gráfico/mapa pelo mesmo índice de opção:

```python
def option_card(entries, padrao):
    """entries: list de (label, build_fn, texto). padrao: 'grafico' | 'mapa'
    -- controla o CSS aplicado (texto abaixo vs. texto na 3a coluna, §3.13).
    Card de opção unica tambem passa por aqui (sem pills visiveis, texto
    ainda renderizado -- so nao ha nada para trocar)."""
    if len(entries) == 1:
        label, build_fn, texto = entries[0]
        build_fn()
        _emite_bloco_texto(texto)  # fora do option-card, mesma posicao visual
        return
    panes, text_panes, pills = [], [], []
    for i, (label, build_fn, texto) in enumerate(entries):
        start = len(parts)
        build_fn()
        html = "".join(parts[start:]); del parts[start:]
        panes.append(f'<div class="opt-pane"{" hidden" if i else ""}>{html}</div>')
        text_panes.append(f'<div class="opt-text"{" hidden" if i else ""}>{_lorem(texto)}</div>')
        pills.append(f'<button type="button" class="pill"{"" if i else " data-active=\"true\""}>{_esc(label)}</button>')
    parts.append(
        f'<div class="option-card option-card-{padrao}">'
        '<div class="pill-col">' + "".join(pills) + '</div>'
        '<div class="opt-panes">' + "".join(panes) + '</div>'
        '<div class="opt-texts">' + "".join(text_panes) + '</div>'
        '</div>'
    )
```

`initPills` (JS) passa a esconder/mostrar 2 elementos por índice (`.opt-pane`
e `.opt-text`), não 1 — mesmo padrão de índice compartilhado, só duplicado.

### 10.2 3 padrões de CSS (grid, não flex simples)

```css
/* padrão A — grafico: pills+grafico numa linha, texto abaixo ocupando tudo */
.option-card-grafico{
  display:grid; grid-template-columns:200px 1fr; grid-template-areas:"pills chart" "text text";
  gap:16px;
}
.option-card-grafico .pill-col{grid-area:pills;}
.option-card-grafico .opt-panes{grid-area:chart;}
.option-card-grafico .opt-texts{grid-area:text;}

/* padrão B — mapa: pills+mapa+texto numa linha so (3 colunas) */
.option-card-mapa{
  display:grid; grid-template-columns:200px 1fr 260px; gap:16px; align-items:start;
}

/* padrão C — tabela: texto | tabela (sem pills nesta rodada) */
.table-with-text{ display:grid; grid-template-columns:260px 1fr; gap:20px; align-items:start; }
```

`.opt-text`/`.table-with-text` usam a mesma tipografia de corpo do
relatório (`--font-body`), não mono — é prosa, não metadado.

### 10.3 Geração de texto (lorem ipsum, ~500 palavras)

```python
import random
_LOREM_WORDS = "lorem ipsum dolor sit amet consectetur adipiscing elit ...".split()  # banco de palavras classico

def _lorem(seed, palavras=500):
    rng = random.Random(seed)  # seed = label da opcao, texto deterministico por opcao (nao muda a cada geracao)
    return " ".join(rng.choice(_LOREM_WORDS) for _ in range(palavras)).capitalize() + "."
```

Determinístico por `seed` (ex. o label da opção) para o texto não mudar
gratuitamente a cada rodada de geração — útil para revisar diffs.

### 10.4 Outliers: gate por formato

```python
def _eh_taxa_ou_percentual(s):
    return s.get('format') in ('pct', 'pct1')

# dentro de line_chart/bar_chart/grouped_bar_chart:
norm = [_normaliza(s['values']) for s in series]
limpos = [remove_outliers_tukey(v) if _eh_taxa_ou_percentual(s) else v for s, v in zip(series, norm)]
```

`mapa_svg` ganha o mesmo gate a partir do parâmetro `fmt` que já recebe
(`fmt='pct1'` → aplica; `fmt='int'`, default → não aplica, nem chama
`remove_outliers_tukey`). Efeito prático: bem menos cards ganham o toggle
de outliers do que na rodada anterior (a maioria dos ~122 chart-renders
eram séries de contagem absoluta).

### 10.5 Tema único: remove o bloco dark inteiro

Apaga `@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){...} }`
e `:root[data-theme="dark"]{...}` do CSS gerado — as variáveis do `:root`
base (hoje "claro") passam a ser as únicas. `color-scheme:light` explícito
no `:root` (novo) evita qualquer resquício de UI nativa escura (scrollbar,
etc.) no navegador do leitor.

### 10.6 Corpo mais largo

`.doc{max-width:880px}` → `.doc{max-width:1200px}` (specification.md §3.15,
R). `.option-card-mapa`'s 3ª coluna (260px) e `.table-with-text`'s 1ª coluna
(260px) foram dimensionadas para caber confortavelmente dentro desse novo
limite junto com um mapa/tabela de tamanho razoável.

### 10.7 Agrupamento (specification.md §9)

Mecânico: para cada linha da tabela de §9, substituir as chamadas
`line_chart`/`bar_chart`/`grouped_bar_chart`/`mapa_svg` soltas (ou os
`h5`/`h6` que hoje as separam) por 1 chamada a `option_card` com as N
opções correspondentes — mesma técnica já usada para "Por CAP e faixa
etária"/"Grupo evitável por CAP", agora aplicada aos ~9 grupos novos
listados na tabela. Cada `build_fn` de opção ganha também seu `texto`
(§10.1) — nesta rodada, `_lorem(label)`.
