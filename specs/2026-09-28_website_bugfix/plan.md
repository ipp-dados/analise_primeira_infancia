# Plano — `specs/2026-09-28_website_bugfix`

Aberta em 2026-09-28, no branch `spec/website-graficos` (correção da rodada `specs/2026-09-25_website_graficos`).

## Contexto

O push da rodada `website_graficos` para `staging_main` (7af4bbc) deixou o site com bugs relatados pelo usuário:

1. botão Taxa | Óbitos fora do estilo do site;
2. textos da curadoria que não aparecem;
3. ao trocar de mapa/gráfico, o texto não troca junto;
4. o layout quebra ao reduzir a largura (sugestão: esconder o sumário/barra de progresso);
5. vários gráficos/mapas não aparecem direito.

**Rollback**: `staging_main` voltou à árvore de `2e9279b` num commit novo (`883b4b1`), sem reescrever o histórico
(push normal, sem `--force`). Para reintegrar este branch: `git revert 883b4b1` em `staging_main` (ou no branch)
antes do merge — senão o merge vê os commits da rodada como já integrados e mantém a árvore antiga.

## Diagnóstico

| # | Causa | Evidência |
|---|---|---|
| 1, 3, 5 | **Cache**: `index.html` novo com `css/`/`js/` antigos. As URLs não tinham versão, e o navegador ou o cache do Pages servia o `charts.js` e o `components.css` da versão anterior. | Reproduzido: HTML atual + CSS/JS de `2e9279b` → botão cinza sem estilo, texto preso em "Precoce" com o mapa "Tardia", erro `pm is not defined` (a função `pm` é nova) que interrompe `data/charts.js` e deixa os gráficos seguintes sem renderizar. Com CSS/JS atuais, 110 trocas de pill em 45 cartões: 0 falhas. |
| 1 | Mesmo com o CSS certo, o controle segmentado cinza (estilo iOS) não era linguagem do site. | Captura antes/depois. |
| 2 | (a) Par absoluto + percentual por CAP passava só a chave do absoluto: os 3 textos `percentual_evitaveis_cap_*_ano`, curados, nunca apareceram. (b) `tabela_com_texto` sempre gerava lorem, mesmo havendo texto curado (hoje nenhuma das 3 tabelas tem texto curado). | `conferencia_textos_site.csv` |
| 4 | Sem regra responsiva para o grid conteúdo + sumário (coluna fixa de 280 px) nem para o banner. A 760 px, um gráfico ficava com ~90 px; título do mapa com uma palavra por linha; texto do mapa empilhado com altura 0 (filho absoluto); URLs das Fontes estouravam 420 px. | Capturas a 1000/760/420 px |
| extra | Cor padrão repetia cor fixa ("Total" e "Meninos" ambos `--c1`); regra do último rótulo do eixo x apagava 2010 em séries de 3 Censos; nomes de bairro sobrepostos nas barras verticais de 10 grupos. | Capturas |

## Correções

- `build_site.py`: `?v=<md5 8>` em todo `css/`/`js/`/`data/` do `<head>` (`_v()`; CRLF normalizado → mesmo hash no
  Windows e no Linux); `data-seed` em cada bloco de texto; tupla de chaves no par CAP; `tabela_com_texto` com
  `_texto_seed`.
- `css/layout.css`: ≤ 1100 px sem sumário lateral (e sem barra de progresso), conteúdo em largura total; ≤ 760 px banner
  empilhado, gutter 18 px.
- `css/components.css`: Taxa|Óbitos (e Painéis|Linhas) com a forma das pills e o azul-marinho das abas no ativo; foco
  visível; ≤ 900 px mapa/gráfico e texto empilhados (texto do mapa volta ao fluxo); ≤ 720 px botões acima do título
  do mapa; quebra de URLs nas caixas de fonte; grade de eixos em 2 colunas ≤ 1100 px e 1 coluna ≤ 720 px.
- `js/charts.js`: `coresPadrao` pula cores fixas já usadas; distância do último rótulo do eixo x em unidades do
  viewBox; rótulos inclinados (-35°) nas barras verticais quando não cabem.
- `website/build/confere_textos.py` (novo, dev): gera a tabela de conferência texto × figura.

Fora de escopo (continuam no ROADMAP): versão mobile de verdade (texto dos SVG fica pequeno a 420 px), 59 blocos
ainda em lorem (curadoria), decisões abertas da rodada `website_graficos`.
