# Tarefas — `specs/2026-09-28_website_mobile`

Branch `spec/website-mobile` (criado a partir de `staging_main` depois do OK do plano). Um commit por bloco, com a
validação do bloco preenchida em `validation.md`.

## Bloco 0 — Antes de começar
- [ ] **T0.1** Capturas de referência (antes): 7 abas × 1400/1024/768/390/360 px, Chromium; guardar fora do git.
- [ ] **T0.2** Script de medição (alvos < 44 px, texto do SVG renderizado, sobreposição da legenda, tooltip fora da
      tela, rolagem horizontal, altura até o 1º conteúdo) no scratchpad, reaproveitado em todos os blocos.

## Bloco 1 — Base
- [ ] **T1.1** Faixas de largura documentadas em `css/main.css`; consolidar as media queries da `website_bugfix` nelas.
- [ ] **T1.2** Fonte base 17 px, `clamp` nos títulos e gutter no celular.
- [ ] **T1.3** Banner e faixa de aviso compactos.
- [ ] **T1.4** Alvos de toque de 44 px no celular.

## Bloco 2 — Navegação (M1, M2)
- [ ] **T2.1** Abas: esmaecimento nas bordas + aba ativa centralizada (`navigation.js`).
- [ ] **T2.2** Gerador: marcação `.outline-mobile` (botão + lista por painel).
- [ ] **T2.3** `sidebar.js`: rótulo da subseção ativa, abrir/fechar (toque fora, Esc, link, troca de aba), linha de progresso.
- [ ] **T2.4** Altura fixa total ≤ 100 px; se passar, esconder a faixa ao rolar para baixo.

## Bloco 3 — Gráficos na largura real (M3)
- [ ] **T3.1** `lineChart`/`groupedBarChart`/`pequenosMultiplos`: largura do contêiner abaixo de 640 px; desktop inalterado.
- [ ] **T3.2** Perfil celular (fontes, rótulos x/y, `padR` pelo valor, extremos, pequenos múltiplos 1-2 colunas).
- [ ] **T3.3** Redesenho: `ResizeObserver` com debounce, painel oculto desenhado ao aparecer, estado preservado.
- [ ] **T3.4** Barras horizontais (rótulo em 2 linhas) e tooltip de linha por toque.

## Bloco 4 — Pills (M4)
- [ ] **T4.1** Gerador: `<select class="pill-select">` nos cartões com 6 ou mais opções.
- [ ] **T4.2** CSS (select no celular, pills no resto) e JS (`change` → `selecionaPill`, sincronia nos dois sentidos,
      alternância Taxa|Óbitos preserva a opção).

## Bloco 5 — Mapas
- [ ] **T5.1** Legenda abaixo do mapa no celular; escala e rosa legíveis.
- [ ] **T5.2** Tooltip por toque dentro do cartão; fecha ao tocar fora.
- [ ] **T5.3** Botões CSV/outliers numa linha própria (mapas e gráficos).

## Bloco 6 — Demais componentes
- [ ] **T6.1** Tabelas com rolagem e primeira coluna fixa; callouts; Conclusões; Visão geral; rodapé; `404.html`.

## Bloco 7 — Validação e documentação
- [ ] **T7.1** `validation.md` completo (3 motores × 4 tamanhos + desktop pixel a pixel).
- [ ] **T7.2** Aparelho real (usuário): iPhone e Android, roteiro em V7.
- [ ] **T7.3** `website/README.md`, skill `build_website`, `ROADMAP.md`, `relatorio/specs.md` (v10).
- [ ] **T7.4** Merge em `staging_main`; deploy só com OK do usuário.
