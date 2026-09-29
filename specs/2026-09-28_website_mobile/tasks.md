# Tarefas — `specs/2026-09-28_website_mobile`

Branch `spec/website-mobile` (criado a partir de `staging_main` depois do OK do plano). Blocos validados juntos e
commitados em 3 partes (site, marca d'água do PDF, documentação); validação em `validation.md`.

## Bloco 0 — Antes de começar
- [x] **T0.1** Capturas de referência (antes): 7 abas × 1400/1024/768/390/360 px, Chromium; guardar fora do git.
- [x] **T0.2** Script de medição (alvos < 44 px, texto do SVG renderizado, sobreposição da legenda, tooltip fora da
      tela, rolagem horizontal, altura até o 1º conteúdo) no scratchpad, reaproveitado em todos os blocos.

## Bloco 1 — Base
- [x] **T1.1** Faixas de largura documentadas no topo de `css/mobile.css` (arquivo novo); media queries da `website_bugfix` movidas para lá.
- [x] **T1.2** Fonte base 17 px, `clamp` nos títulos e gutter no celular.
- [x] **T1.3** Banner e faixa de aviso compactos.
- [x] **T1.4** Alvos de toque de 44 px no celular.

## Bloco 2 — Navegação (M1, M2)
- [x] **T2.1** Abas: esmaecimento nas bordas + aba ativa centralizada (`navigation.js`).
- [x] **T2.2** Gerador: marcação `.outline-mobile` (botão + lista por painel).
- [x] **T2.3** `sidebar.js`: rótulo da subseção ativa, abrir/fechar (toque fora, Esc, link, troca de aba), linha de progresso.
- [x] **T2.4** Altura fixa total ≤ 100 px; se passar, esconder a faixa ao rolar para baixo.

## Bloco 3 — Gráficos na largura real (M3)
- [x] **T3.1** `lineChart`/`groupedBarChart`/`pequenosMultiplos`: largura do contêiner abaixo de 640 px; desktop inalterado.
- [x] **T3.2** Perfil celular (fontes, rótulos x/y, `padR` pelo valor, extremos, pequenos múltiplos 1-2 colunas).
- [x] **T3.3** Redesenho: `ResizeObserver` com debounce, painel oculto desenhado ao aparecer, estado preservado.
- [x] **T3.4** Barras horizontais (rótulo em 2 linhas) e tooltip de linha por toque.

## Bloco 4 — Pills (M4)
- [x] **T4.1** Gerador: `<select class="pill-select">` nos cartões com 6 ou mais opções.
- [x] **T4.2** CSS (select no celular, pills no resto) e JS (`change` → `selecionaPill`, sincronia nos dois sentidos,
      alternância Taxa|Óbitos preserva a opção).

## Bloco 5 — Mapas
- [x] **T5.1** Legenda abaixo do mapa no celular; escala e rosa legíveis.
- [x] **T5.2** Tooltip por toque dentro do cartão; fecha ao tocar fora.
- [x] **T5.3** Botões CSV/outliers numa linha própria (mapas e gráficos).

## Bloco 6 — Demais componentes
- [x] **T6.1** Tabelas com rolagem e primeira coluna fixa; callouts; Conclusões; Visão geral; rodapé; `404.html`.

## Bloco 7 — Validação e documentação
- [x] **T7.1** `validation.md` completo (3 motores × 4 tamanhos + desktop pixel a pixel).
- [ ] **T7.2** Aparelho real (usuário): iPhone e Android, roteiro em V7.
- [x] **T7.3** `website/README.md`, skill `build_website`, `ROADMAP.md`, `relatorio/specs.md` (v10).
- [ ] **T7.4** Merge em `staging_main`; deploy só com OK do usuário.

## Pedidos do usuário durante a rodada
- [x] **TU.1** Banner do celular: GitHub e PDF na mesma linha, com rótulo curto (`.rotulo-curto`).
- [x] **TU.2** Marca d'água "EM DESENVOLVIMENTO" no PDF, removida junto com a faixa do site: chave única
      `relatorio/publicacao.json`; `gera_latex.py` gera `gerado/aviso.tex`; PDF republicado.
