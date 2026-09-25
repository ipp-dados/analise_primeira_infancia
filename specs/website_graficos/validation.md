# Validação — `specs/website_graficos`

Escrita **antes** da implementação (pedido do usuário, 2026-09-25). Cada item diz como se verifica; preencher
resultado e data ao fim de cada bloco. Nada conta como validado só porque o gerador rodou sem erro.

## Base (vale para todos os blocos)

- [ ] V0.1 `python website/build/build_site.py` roda sem erro e **sem linha `AVISO`** (orçamento: `index.html`
      ≤ 1 MB, site ≤ 2 MB)
- [ ] V0.2 Duas execuções seguidas dão o mesmo md5 de `index.html` e `data/*` (determinismo)
- [ ] V0.3 `index.html` aberto por `file://` e por `http.server` imitando o Pages (skill `build_website`, passo 2):
      sem erro no console, todas as abas renderizam
- [ ] V0.4 Regras de site estático (`website/README.md`): só html/css/js/svg/png/jpg, caminhos relativos em
      minúsculas, rotas só por hash, sem `fetch`
- [ ] V0.5 Nenhum texto curado some sem registro: lista de sementes de `textos_curados.json` publicadas antes ×
      depois; toda diferença tem um código E* em `specs/exclusoes.md`

## A. Exclusões

- [ ] VA.1 (E2) Nenhum gráfico/pill/tabela de **1 a 4 anos** mostra 1.2.1, 1.2.2 ou 1.2.3 — busca no
      `data/charts.js` pelos rótulos desses subgrupos restrita aos cartões de 1-4 anos; menores de 1 e de 5
      anos continuam mostrando 1.2.x
- [ ] VA.2 (E3) Nenhum gráfico mostra o subgrupo 1.1 — busca por "imunização" em `data/charts.js` = 0
- [ ] VA.3 (E4) Mapas `mapa_obitos_gravidez_bairro_2025` e `mapa_obitos_puerperio_bairro_2025` ausentes; as
      séries municipais de gravidez/puerpério continuam
- [ ] VA.4 (E5) Séries de raça com 5 linhas (Branca, Parda, Preta, Amarela e indígena, Não informada); o % de
      "Amarela e indígena" confere com Σóbitos/Σnascidos × 100 em 3 anos sorteados (não soma de %)
- [ ] VA.5 (E6) Sem mapa de taxa de violência por bairro; mapas de taxa por RA e de contagem por bairro presentes
- [ ] VA.6 (E7, E8) Sem "Comparativo por ano" da vacina; sem frequência absoluta por raça/cor e por sexo; total e
      taxas de frequência presentes
- [ ] VA.7 Mantidos: lesão autoprovocada, % de evitáveis por CAP 1-4 anos, séries por faixa, taxas neonatais por
      bairro — todos presentes

## E9. Alternância Taxa ↔ Óbitos

- [ ] V9.1 Os mapas de mortalidade por bairro (neonatal precoce/tardia/pós-neonatal/total e raça/total) estão em
      **um** cartão cada, com o controle "Taxa | Óbitos"; abre em **Taxa**
- [ ] V9.2 Trocar o modo mantém a pill (Taxa · Tardia → Óbitos · Tardia) e troca o texto junto
- [ ] V9.3 Teclado: Tab chega ao controle, Enter/Espaço troca, foco visível; `aria-pressed` correto
- [ ] V9.4 Tooltip, legenda, download de CSV e botão de outliers funcionam nos dois modos
- [ ] V9.5 Textos curados dos mapas de contagem (`mapa_obitos_neonatal_precoce_bairro_2025`,
      `mapa_obitos_raca_total_bairro_2025`) continuam publicados (modo Óbitos)

## B. Melhoria dos gráficos (cada item só depois da decisão P* correspondente)

- [ ] VB.1 (B1) Todo gráfico de linha/barra tem unidade legível (título de eixo ou rótulo de série); nenhum nome
      de coluna cru (`taxa_mortalidade_precoce`, `Valores`) em texto visível — busca em `data/charts.js`
- [ ] VB.2 (B2) Todo mapa contínuo por bairro usa teto P95; o topo da legenda diz "≥ X"; tooltip mostra o valor
      real acima do teto (conferir 2 bairros acima do P95)
- [ ] VB.3 (B3) Barras com valor na ponta quando ≤ 12 barras; nenhum gráfico com número em todo ponto
- [ ] VB.4 (B4) Pequenos múltiplos: um painel por série, mesma escala, demais séries em cinza; alternar para a
      visão original funciona
- [ ] VB.5 (B5) `node .claude/.../dataviz/scripts/validate_palette.js "<--c1…--c8>" --mode light --surface <--surface>`
      sem FAIL; cores trocadas registradas em `relatorio/specs.md` (histórico da paleta)
- [ ] VB.6 (B6) Toda caixa "Fontes desta seção" traz a referência ABNT da entrada de `fontes.bib`; nenhuma fonte
      do site sem entrada correspondente (reaproveitar `relatorio/latex/build/inventario_fontes.py`)
- [ ] VB.7 (B7) Nenhum gráfico de categorias com linha "Total"/"Subtotal" desenhada como categoria
- [ ] VB.8 (B8) Conforme P1: taxas com base zero, ou o corte do eixo visível no próprio gráfico

## Navegador

- [ ] VN.1 Chrome (DevTools Protocol) e Firefox/WebKit (Playwright): troca de aba + hash, âncoras antigas, barra
      fixa, sumário, pills, alternância, outliers, CSV, tooltip de mapa em cada nível (bairro, AP, RP, RA, CAP)
- [ ] VN.2 Capturas antes × depois dos cartões alterados, guardadas na pasta da rodada
