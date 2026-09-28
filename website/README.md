# Site — Diagnóstico da Primeira Infância Carioca

Site estático (HTML/CSS/JS puros, sem etapa de build no deploy) publicado no GitHub Pages
pelo workflow `.github/workflows/deploy-relatorio.yml`. Histórico e decisões:
`specs/2026-09-24_website_refactor/` (esta estrutura) e `relatorio/specs.md` (versões anteriores, v1-v8).

## Gerar

Da raiz do projeto (ou de qualquer pasta — os caminhos resolvem pelo root):

```bash
python website/build/build_site.py            # escreve em website/
python website/build/build_site.py <pasta>    # escreve em outra pasta (copia css/js/assets junto)
```

Lê `tabelas_finais/*.csv`, `dados_locais/geo/*.geojson` e `relatorio/textos_curados.json`
(texto curado do DOCX, via `.claude/skills/export_pdf_report/scripts/sincroniza_docx.py`, que
também roda este gerador). Imprime o tamanho de cada arquivo publicado e **avisa** se passar do
orçamento (`index.html` ≤ 1 MB, site ≤ 2 MB — spec §4.9). Gerar não precisa de rede: o fundo
cartográfico só é baixado se `assets/images/basemap-<hash>.jpg` ainda não existir.

**O CI não gera o site** (não tem `tabelas_finais/`, que é gitignorado): a saída gerada é
versionada e o deploy só copia. Regerou → confira → commit → dispare o workflow.

## O que é gerado e o que é editado à mão

| Caminho | Origem |
|---|---|
| `index.html` | **gerado** — não editar |
| `data/charts.js` (dados + chamadas dos gráficos) | **gerado** |
| `data/geo.js` (geometria dos mapas, 1 `<path>` por região) | **gerado** |
| `assets/images/basemap-*.jpg`, `assets/images/ipp-logo-<altura>.png` | **gerados** (a partir do tile Esri e de `ipp-logo.png`) |
| `css/main.css`, `css/layout.css`, `css/components.css`, `css/mobile.css` | à mão (tokens em `main.css`; `mobile.css` = telas < 1100 px, carregado por último) |
| `js/charts.js` (motor de gráficos, pills, outliers, CSV, tooltip de mapa) | à mão |
| `js/navigation.js` (abas, URL), `js/sidebar.js` (sumário lateral) | à mão |
| `assets/icons/*.svg` (Lucide, licença ISC), `assets/images/ipp-logo.png` | à mão (fonte) |
| `404.html`, `.nojekyll`, `assets/images/favicon.svg` | à mão |
| `build/` (gerador) | à mão — **não publicado** |

`*.png`/`*.svg` são ignorados globalmente no `.gitignore`; `!/website/assets/**` é a exceção que
mantém os assets do site no git — não remover.

## Convenções dos gráficos (`specs/2026-09-25_website_graficos`)

- **Formato do valor** (`format` da série / `fmt` do mapa): `int` contagem; `pct1` percentual (`%`); `pm1` taxa por
  mil (`‰` — mortalidade por mil nascidos vivos, notificações por mil crianças); `dec1` outra taxa (unidade no
  título). Nunca `pct1` para taxa por mil. `pm1f`/`dec1f` = iguais, sem o botão de outliers.
- **Unidade**: todo `line_chart`/`grouped_bar_chart` recebe `unidade=` (título curto acima do eixo y, por extenso,
  com a unidade); barras horizontais levam a unidade no `titulo`.
- **Nomes**: rótulos equivalentes são padronizados em `_ROTULO_PADRAO` (idade, sexo) e causas evitáveis pelo código
  em `_NOME_CAUSA`; raça/cor e sexo têm cor fixa em `_COR_ENTIDADE`.
- **Títulos de seção** descrevem o indicador (nunca "Mapas"/"Série temporal"); ao renomear um `h3`, passe
  `antigo=` com o id anterior para links compartilhados continuarem funcionando.
- **Fontes**: o texto `fonte=` de cada cartão precisa casar com um `padroes` de `relatorio/latex/fontes.bib`, senão o
  gerador imprime `AVISO` e a caixa de fontes mostra só o texto curto.

## Cache e versões dos arquivos

O `index.html` referencia `css/`, `js/` e `data/` com `?v=<md5 do conteúdo>` (gerado por `_v()` em `build_site.py`).
Sem isso o navegador servia o `index.html` novo com o CSS/JS antigos em cache (2026-09-28: botão Taxa|Óbitos sem
estilo, texto preso na 1ª pill, gráficos sem renderizar — `specs/2026-09-28_website_bugfix`). Arquivo novo em
`css/`/`js/` precisa entrar na lista do `<head>` com `_v()`.

## Conferir textos curados × figuras

`python website/build/confere_textos.py` (Playwright, só desenvolvimento) gera
`specs/2026-09-28_website_bugfix/conferencia_textos_site.csv`: um bloco de texto por linha (aba, seção, modo, pill,
figura exibida, chave, texto do DOCX / do JSON / do site, status OK · PENDENTE (lorem) · ERRO · NÃO PUBLICADO).
Também gera `textos_para_revisao.csv` (uma linha por chave, faltantes primeiro, blocos do relatório incluídos,
colunas em branco "Conferido"/"Comentário" para a revisão manual). Os blocos de texto levam `data-seed` = chave em `relatorio/textos_curados.json`.

## Mobile (`specs/2026-09-28_website_mobile`)

Toda regra de tela estreita fica em **`css/mobile.css`** (carregado por último); `main.css`, `layout.css` e
`components.css` são só desktop. Faixas: **desktop ≥ 1100 px** (nenhuma regra de `mobile.css`), **tablet 720-1099 px**,
**celular < 720 px**; abaixo de 900 px mapa/gráfico e texto empilham. Regra da rodada: o desktop não muda — conferido
por captura pixel a pixel a 1400 e 1280 px antes de cada commit.

| Componente | Tablet e celular | Só celular |
|---|---|---|
| Abas | fileira rola na horizontal, esmaecimento no lado com mais abas, aba ativa centralizada (`js/navigation.js`) | 44 px de altura |
| Sumário | vira a faixa **"Nesta seção ▾"** dentro da barra fixa + linha de progresso de 3 px (`js/sidebar.js`; marcação `.outline-mobile`/`.nav-progress` gerada, oculta no desktop) | |
| Gráficos | contêiner < 640 px → **desenho na largura real** (`js/charts.js`: viewBox = px, fontes ≥ 11 px, menos rótulos, paddings medidos); redesenha ao aparecer (pill, aba, Taxa\|Óbitos) e ao girar a tela | pequenos múltiplos em 1-2 colunas |
| Pills | | cartões com **6+ opções** mostram um `<select>` nativo (`.pill-select`, gerado), sincronizado com as pills |
| Mapas | | legenda **abaixo** do mapa; escala e rosa legíveis (`--map-esc`); tooltip por toque, preso ao cartão |
| Banner | | compacto; GitHub e PDF lado a lado com rótulo curto (`.rotulo-curto`) |
| Alvos de toque | | ≥ 44 px (abas, pills, select, botões, `summary`) |

Tooltips: o mouse continua abrindo por hover e fechando ao sair (`pointerleave` com `pointerType === 'mouse'`); o
toque abre ao tocar e fecha ao tocar fora (o `mouseleave` de compatibilidade do navegador fechava o tooltip na hora).
Testar em 390×844, 360×740, 768×1024 e 1024×768 (Chromium, Firefox, WebKit) e num aparelho real.

## Faixa "EM DESENVOLVIMENTO"

A faixa amarela do topo sai de `relatorio/publicacao.json` (`em_desenvolvimento`), a mesma chave da marca d'água do
PDF (`relatorio/latex/build/gera_latex.py`). Na versão final: `false` e regerar o site e o PDF — as duas saem juntas.

## Testar localmente

- Abrir `website/index.html` direto no navegador funciona (nenhum `fetch`; tudo por `<script src>`).
- Para imitar o GitHub Pages (site servido em `/<repo>/`): `python -m http.server 8000` na pasta
  **acima** de uma cópia chamada `analise_primeira_infancia/` e abrir
  `http://localhost:8000/analise_primeira_infancia/`.

## Regras de site estático (spec §4.10)

Só `html css js svg png jpg` publicados; caminhos sempre relativos e em minúsculas (o Pages
diferencia maiúsculas, o Windows não); rotas só por `#hash` (`#<eixo>`, `#<eixo>/<id-h3>`); nada de
`fetch` para arquivo local; nada de CDN novo (só Google Fonts). O workflow falha se aparecer um tipo
de arquivo fora da lista.
