# Especificação — `specs/2026-09-28_website_mobile`

Faixas: **desktop ≥ 1100 px**, **tablet 720-1099 px**, **celular < 720 px**. Nada abaixo muda o desktop.

## 1. Base

- `html{font-size:17px}` no celular (19,2 px no tablet e no desktop). `h1` do banner com `clamp(1.6rem, 7vw, 2.7rem)`,
  `h2`/`h3` com `clamp` equivalente.
- `--gutter`: 32 px no desktop, 24 px no tablet, 16 px no celular.
- Alvos de toque no celular: `.tab`, `.pill`, `.alterna-btn`, `.dl-btn`, `.outlier-btn`, `summary`, links do sumário e
  do banner com `min-height:44px` (e largura mínima de 44 px). Espaço entre alvos ≥ 8 px.
- Banner no celular: logo com 28 px de altura, eyebrow numa linha (fonte menor), links como 2 pills lado a lado,
  "Atualizado em" abaixo. Faixa amarela com fonte .72rem e padding 8 px. Meta: faixa + banner ≤ 320 px a 390 px.

## 2. Navegação

### 2.1 Abas (M1)
- A fileira continua rolando na horizontal (`overflow-x:auto`, `scroll-snap-type:x proximity`).
- Esmaecimento nas bordas com `mask-image` (degradê de 24 px) só no lado em que ainda há conteúdo: classes
  `.tem-mais-esq`/`.tem-mais-dir` na `.tabbar-inner`, atualizadas no `scroll` (rAF) e no `resize`.
- No `tabchange` e no carregamento, a aba ativa rola para o centro (`scrollIntoView({inline:'center', block:'nearest'})`,
  `behavior:'auto'` com `prefers-reduced-motion`). Sem rolar a página na vertical.
- Altura da barra no celular: 52 px (abas de 44 px).

### 2.2 Sumário e progresso (M2)
- Gerador: além do `<aside class="outline">` (desktop), emite `<div class="outline-mobile">` logo após a barra de abas,
  dentro do mesmo contêiner fixo: botão `Nesta seção: <subseção atual> ▾` (`aria-expanded`, `aria-controls`) e um
  painel com os mesmos links do sumário do painel ativo. Os links são gerados uma vez; `sidebar.js` mostra os do
  painel ativo (mesma lógica de hoje).
- Linha de progresso de 3 px na borda de baixo da barra de abas (tablet e celular), com o mesmo cálculo de
  `sidebar.js`.
- Abrir a lista: painel abaixo da faixa, altura máxima de 60 vh com rolagem; fecha ao escolher um link, ao tocar
  fora, com Esc e ao trocar de aba. O rótulo mostra a subseção ativa (a que o sumário do desktop destaca).
- Altura fixa total no celular (abas + faixa + progresso): ≤ 100 px.
- Desktop: `.outline-mobile{display:none}`; tablet e celular: `.outline{display:none}` (já é assim desde a
  `website_bugfix`).

## 3. Gráficos na largura real (M3)

### 3.1 Largura
- `lineChart`, `groupedBarChart` e `pequenosMultiplos` guardam `cfg` no contêiner (`container._cfg`) e desenham com
  `W = clamp(larguraDoConteiner, 300, 680)` **somente quando a largura do contêiner < 640 px**; acima disso,
  `W = opts.width || 680` como hoje (desktop idêntico).
- Painel oculto (largura 0): usa a largura do ancestral visível mais próximo (`.opt-panes`/`.out`); ao ser mostrado
  (pill, `<select>`, Taxa|Óbitos, Painéis|Linhas, aba), redesenha se a largura mudou.
- `ResizeObserver` nos contêineres, debounce de 150 ms, redesenha só se a largura mudar ≥ 40 px (girar a tela). O
  redesenho troca o conteúdo do contêiner (`replaceChildren`) e mantém o estado (painel de pequenos múltiplos ativo,
  tabela aberta).

### 3.2 Perfil celular (W < 520)
- Fontes do SVG em unidades do viewBox tais que o texto renderizado tenha ≥ 11 px (eixos 11-12 px, rótulos finais
  12-13 px).
- Eixo x: no máximo 4 rótulos (primeiro, último e 2 intermediários); eixo y: 3 intervalos.
- `padR` do rótulo final calculado pela largura do maior valor formatado (hoje fixo em 66).
- Máximo/mínimo (extreme labels) desligados abaixo de 400 px; rótulo final continua até 4 séries.
- Legenda acima do gráfico, quebrando linha (já é assim); "Outras (N)" mantido.
- Barras agrupadas: rótulos do eixo x inclinados já decididos pela largura (regra da `website_bugfix`); valor na
  ponta só se couber (largura da barra ≥ 22 px).
- Barras horizontais (`barChart`, HTML): coluna do rótulo `minmax(90px, 40%)`, rótulo em até 2 linhas.
- Pequenos múltiplos: 1 coluna abaixo de 480 px, 2 colunas de 480 a 719 px.
- Tooltip de linha: por toque (`touchstart`/`touchmove` já existem), preso à largura do cartão, fecha ao tocar fora.

## 4. Pills (M4)
- Gerador: para cada `option-card` com **6 ou mais** opções, emite também um `<select class="pill-select">` com as
  mesmas opções (texto = rótulo da pill), dentro da `.pill-col`. Até 5: nada novo.
- CSS: no celular, `.pill-col` com `<select>` esconde as pills e mostra o select (largura 100%, 44 px, seta própria
  sobre o nativo); no tablet e no desktop, o contrário.
- JS: `change` do select chama `selecionaPill(card, i)`; `selecionaPill` sincroniza o select (valor) e as pills
  (`aria-pressed`), para a alternância Taxa|Óbitos preservar a opção nos dois controles.
- Rótulo acessível: `<label class="visually-hidden">Opção</label>` + `aria-label` com o título da seção.

## 5. Mapas
- Celular: `.map-legend-overlay` sai de cima do mapa e vira bloco abaixo do SVG (`position:static`, largura total,
  itens da legenda em 2 colunas). Tablet e desktop como hoje.
- Barra de escala e rosa dos ventos: tamanho de fonte compensado pela escala do SVG (texto ≥ 10 px renderizado).
- Tooltip por toque: tocar numa região mostra o nome e o valor e destaca a região; tocar em outra troca; tocar fora
  do mapa fecha. Posição: dentro do `.map-svg-card`, limitada às bordas (nunca fora da tela).
- Botões CSV e outliers numa linha própria acima do título, alinhados à direita, com 44 px (hoje ficam absolutos
  sobre o título). Mesmo tratamento nos cartões de gráfico.

## 6. Demais componentes
- `table.plain`: dentro de `.table-scroll` com sombra na borda quando rola; primeira coluna fixa (`position:sticky`).
- Callouts (achados, fontes, nota, pendente): ícone menor (28 px), padding 16 px.
- Conclusões do eixo: padding 20 px.
- Visão geral: grade de eixos em 1 coluna (celular) e 2 (tablet); cartão de introdução com padding 20 px.
- Rodapé: colunas empilhadas.
- `404.html`: mesmo tratamento de banner e fonte.

## 7. Documentação
- `website/README.md`: seção "Telas estreitas" vira "Mobile" (faixas, componentes, como testar).
- Skill `build_website`: retira "Desktop only so far"; passo de verificação em 390×844 e 768×1024.
- `ROADMAP.md`: item 5 dos Próximos → Concluído; `relatorio/specs.md`: v10 do site.
