# Validação — `specs/2026-09-28_website_mobile`

Escrita **antes** da implementação; resultados preenchidos em 2026-09-28. Tamanhos: **390×844** (iPhone 12-15),
**360×740** (Android pequeno), **768×1024** (tablet retrato), **1024×768** (tablet paisagem), mais **1400×900** e
**1280×900** (desktop, regressão). Motores: Chromium (canal Chrome), Firefox e WebKit via Playwright, com
`is_mobile`/`has_touch` nos tamanhos de celular. Por `file://` e por `http.server` imitando o Pages. Os scripts
(métricas, interação, captura de desktop) ficaram no scratchpad da sessão; o que cada um mede está descrito no item.

Linha de base (2026-09-28, `staging_main` 928127a, 390 px): 247 alvos < 44 px; texto dos gráficos a 4,6 px (mín.);
legenda cobre 57 % do mapa; botão sobre título em 14 cartões; tooltip sai da tela; 579 px até o conteúdo; 22 px de
rolagem horizontal a 360 px.

## Base
- [x] V0.1 Gerador sem `AVISO`, dentro do orçamento (index 0,79 MB, site 1,40 MB); 2 execuções com o mesmo md5
- [x] V0.2 Sem erro de JavaScript nas 7 abas, nos 4 tamanhos e nos 3 motores
- [x] V0.3 **Desktop**: capturas a 1400 e 1280 px das 7 abas iguais às de antes (diferença de canal ≤ 3 = ruído de
      decodificação do fundo cartográfico, medido entre duas capturas da mesma versão), **exceto uma mudança
      intencional**: os rótulos finais "152.221" (Meninas) e "155.513" (Meninos), antes sobrepostos, agora afastados
      (caixa de ~50×25 px na aba Prioridade)
- [x] V0.4 Regras de site estático mantidas: arquivo novo só `css/mobile.css`; sem `fetch`; `?v=` também nele

## 1. Base
- [x] V1.1 Sem rolagem horizontal da página em nenhum tamanho, aba e motor (antes 22 px a 360 px)
- [x] V1.2 Alvos de toque < 44 px no celular: **0** (antes 247). Links dentro de texto corrido (Fontes) ficam de fora
      (WCAG 2.5.8, exceção de texto)
- [x] V1.3 Faixa de aviso + banner: **272 px** a 390 px (meta ≤ 320; antes 348 → 579 contando a barra). GitHub e PDF
      lado a lado com rótulo curto (pedido do usuário durante a rodada)
- [x] V1.4 Fonte base 17 px no celular; as cores não mudaram (contraste AA da `website_refactor` V4 vale)

## 2. Navegação
- [x] V2.1 Aba ativa inteira visível após tocar, após link com hash e após voltar (3 motores)
- [x] V2.2 Esmaecimento só do lado com mais abas: Visão geral ativa → só à direita; Moradia → só à esquerda
- [x] V2.3 "Nesta seção ▾": rótulo = subseção ativa; abre (`aria-expanded`), lista só do painel ativo, link leva à
      subseção e fecha; fecha ao tocar fora, com Esc e ao trocar de aba (3 motores)
- [x] V2.4 Linha de progresso 0 % no topo e 100 % no fim do painel
- [x] V2.5 Barra fixa (abas + faixa + progresso): **100 px** no celular (106 no tablet)

## 3. Gráficos
- [x] V3.1 Texto dos SVG de gráfico ≥ **11,5 px** (mínimo, não só o 10º percentil) a 390 e 360 px, 3 motores
- [x] V3.2 Rótulos sobrepostos (caixas delimitadoras, texto não rotacionado): **0** nos 4 tamanhos e 3 motores. Para
      isso: rótulos finais afastados 18 unidades; largura do rótulo de grupo das barras recalculada para a fonte do
      celular (os de 7 grupos se sobrepunham)
- [x] V3.3 Girar 390×844 → 844×390 → 390×844: redesenha nas duas larguras, mantém a pill e a tabela aberta
- [x] V3.4 Painel antes oculto (pill, select, Taxa|Óbitos, aba) aparece na largura real (viewBox = px)
- [x] V3.5 Pequenos múltiplos em 1 coluna a 390 px e 2 a 600 px
- [x] V3.6 Tooltip de linha por toque: aparece, fica dentro do cartão, fecha ao tocar fora. Achado: o navegador dispara
      um `mouseleave` de compatibilidade logo depois do toque, que fechava o tooltip na hora (Chromium) — agora só o
      mouse fecha ao sair (`pointerleave` + `pointerType`). No Firefox o retângulo de captura (`fill="transparent"`)
      não recebia toque nem hover — `pointer-events:all`

## 4. Pills
- [x] V4.1 Select em todo cartão com ≥ 6 opções (visível só no celular; pills no tablet e no desktop)
- [x] V4.2 Select troca painel, texto e pill; auditoria da `website_bugfix` no desktop: 45 cartões, 110 estados, 0 falhas
- [x] V4.3 Taxa|Óbitos preserva a opção; select e pills sincronizados (`selecionaPill`)

## 5. Mapas
- [x] V5.1 Legenda abaixo do mapa no celular (0 % sobre o mapa; antes 57 %); sobre o mapa no tablet (13-14 %) e no
      desktop, como antes
- [x] V5.2 Tooltip por toque dentro do cartão e da tela, com a região destacada; tocar fora fecha (3 motores)
- [x] V5.3 Botões CSV/outliers sobre o texto do título: 0 (antes 14)
- [x] V5.4 Escala e rosa dos ventos legíveis (fonte compensada por `--map-esc`, conferido nas capturas)

## 6. Demais componentes
- [x] V6.1 Tabelas largas rolam dentro do cartão com a primeira coluna fixa
- [x] V6.2 Visão geral, callouts, Conclusões, rodapé e 404 sem estouro (V1.1) e com alvos ≥ 44 px (V1.2)

## Marca d'água do PDF (pedido do usuário durante a rodada)
- [x] VW.1 `relatorio/publicacao.json` → `em_desenvolvimento: true`: faixa no site e "EM DESENVOLVIMENTO" em todas as
      157 páginas do PDF (texto extraído de cada página); `false`: sem faixa no site e `gerado/aviso.tex` só com o
      comentário
- [x] VW.2 Nenhuma página com aviso do MuPDF (a capa saía com a marca opaca por falta do recurso de transparência —
      corrigido com o nó TikZ no `\AtBeginDocument`)
- [x] VW.3 Mesmo número de páginas (157); o texto só muda onde a rodada `website_graficos` já tinha mudado títulos e
      o PDF ainda não tinha sido republicado (18 páginas)

## 7. Aparelho real (usuário)
- [ ] V7.1 iPhone (Safari) e Android (Chrome): abrir o link publicado, trocar de aba pela barra, abrir "Nesta
      seção", usar um select de opções, alternar Taxa|Óbitos, tocar num mapa, baixar um CSV, girar a tela
- [ ] V7.2 Rolagem fluida (sem travadas perceptíveis) na aba Prioridade, a mais longa

## Fora da meta (registrado no ROADMAP)
- Tablet (768/1024 px): alvos < 44 px (a meta era só do celular) e texto de gráfico de viewBox fixo entre 9,5 e
  11 px (contêineres ≥ 640 px continuam no desenho do desktop, escalado).
