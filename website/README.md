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
| `css/main.css`, `css/layout.css`, `css/components.css` | à mão (tokens em `main.css`) |
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
