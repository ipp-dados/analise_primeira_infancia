# Plano — `specs/2026-09-28_website_mobile`

Rodada da **versão mobile do site** (`ROADMAP.md`, Próximos, item 5). Aberta em 2026-09-28 como planejamento; o
branch de implementação (`spec/website-mobile`, a partir de `staging_main`) só é criado depois do OK do usuário.

## 1. Ponto de partida (medido em 2026-09-28, `staging_main` 928127a)

A rodada `website_refactor` foi só desktop (§4.8). A `website_bugfix` (2026-09-28) apenas impediu a quebra: abaixo de
1100 px o sumário some, abaixo de 900 px mapa/gráfico e texto empilham, abaixo de 760 px o banner empilha. Medições
com Playwright em 390×844 (celular) e 768×1024 (tablet), aba Prioridade:

| Aspecto | 390 px | 768 px | Meta |
|---|---|---|---|
| Alvos de toque < 44 px | 114 de 114 (abas e pills 38, CSV/outliers 28) | 114 de 114 | 0 |
| Texto dos gráficos (10º percentil da altura renderizada) | **~6 px** | 14 px | ≥ 11 px |
| Legenda do mapa sobre o mapa | **50 % da área** | 12 % | 0 % no celular |
| Tooltip de mapa ao tocar | aparece, mas **sai da tela** | ok | dentro da tela, fecha ao tocar fora |
| Barra de abas | 1038 px de conteúdo em 390, sem indício de rolagem | 1066 em 768 | indício + aba ativa visível |
| Faixa de aviso + banner até o conteúdo | **579 px** (69 % da tela) | 397 px | ≤ 320 px |
| Fonte base | 19,2 px | 19,2 px | 17 px no celular |
| Maior lista de pills | 12 opções (~400 px de altura) | | 1 linha (select) |

## 2. Decisões do usuário (2026-09-28)

| # | Tema | Decisão |
|---|---|---|
| M1 | Abas | **Mantém a fileira de pills** rolando na horizontal, com esmaecimento nas bordas (indica que há mais) e a aba ativa trazida para a vista (`scrollIntoView` no `tabchange`) |
| M2 | Sumário | **Faixa recolhível "Nesta seção ▾"** fixa sob as abas, que abre a lista de subseções, e uma **linha fina de progresso** sob a barra de abas |
| M3 | Gráficos | **Redesenhar na largura real** (`js/charts.js`): fontes legíveis, menos anos no eixo x, legenda acima, pequenos múltiplos em 1-2 colunas; redesenha ao girar/redimensionar |
| M4 | Listas longas de pills | **Até 5 opções**: pills quebrando linha. **6 ou mais**: um `<select>` nativo com o rótulo da opção |

Decididas no plano por serem convenção (o usuário pode vetar no OK):

- Legenda do mapa **abaixo** do mapa no celular (a sobreposição fica só ≥ 720 px).
- Tooltips por toque: tocar mostra, tocar fora ou em outra região troca/fecha; posição presa à tela.
- Alvos de toque ≥ 44 px (WCAG 2.5.5 / Apple HIG) no celular; no desktop os tamanhos não mudam.
- Fonte base 17 px no celular; títulos com `clamp`.
- Banner compacto no celular (logo menor, h1 menor, links numa linha). A faixa amarela "em desenvolvimento" fica
  (é aviso institucional), com fonte menor.

## 3. Princípios da rodada

1. **Desktop intocado.** Toda mudança fica em `@media (max-width: …)` ou atrás de um teste de largura em JS. Na
   validação, capturas a 1400 px antes/depois têm de ser iguais pixel a pixel (exceto a data do banner).
2. **Três faixas**, em vez das 5 regras soltas de hoje: desktop ≥ 1100 px · tablet 720-1099 px · celular < 720 px
   (tokens `--bp-*` documentados em `css/main.css`; media queries não aceitam variáveis, então o valor é repetido e
   comentado).
3. **Sem dados novos, sem `fetch`, sem biblioteca nova.** Só `css/` e `js/` editados à mão + marcação mínima no
   gerador (select das pills, faixa do sumário). Orçamento de tamanho (1 MB / 2 MB) inalterado.
4. **Acessibilidade**: tudo por teclado e leitor de tela como hoje; `<select>` e botões nativos; `aria-expanded` na
   faixa do sumário; `prefers-reduced-motion` respeitado.
5. **Sem dependência de hover** no celular: tudo que hoje é `mousemove` ganha equivalente por toque.

## 4. Abordagem por bloco

| Bloco | Conteúdo | Arquivos |
|---|---|---|
| 1 | Base: faixas de largura, fonte 17 px, gutter, banner compacto, alvos de toque 44 px | `css/main.css`, `layout.css`, `components.css` |
| 2 | Navegação: abas com esmaecimento e aba ativa visível (M1); faixa "Nesta seção ▾" + linha de progresso (M2) | `layout.css`, `js/navigation.js`, `js/sidebar.js`, `build_site.py` (marcação da faixa) |
| 3 | Gráficos na largura real (M3): largura do contêiner, perfil celular (fontes, rótulos, legenda), redesenho com `ResizeObserver`, painel oculto desenhado ao ser mostrado | `js/charts.js` |
| 4 | Pills longas viram `<select>` (M4); Taxa/Óbitos e Painéis/Linhas com 44 px | `build_site.py`, `js/charts.js`, `components.css` |
| 5 | Mapas: legenda abaixo, escala/rosa legíveis, tooltip por toque dentro da tela, botões CSV/outliers numa linha própria | `components.css`, `js/charts.js` |
| 6 | Tabelas, callouts, Visão geral, rodapé, 404 | `components.css`, `layout.css`, `404.html` |
| 7 | Validação (antes/depois, 3 motores, 4 tamanhos, aparelho real) e documentação | `validation.md`, `website/README.md`, skill `build_website`, `ROADMAP.md`, `relatorio/specs.md` |

Detalhe por componente em `specification.md`; tarefas em `tasks.md`; critérios em `validation.md` (escritos antes da
implementação, como na rodada `website_graficos`).

## 5. Riscos

- **Redesenho dos gráficos (M3)** é a parte grande: 87 gráficos criados uma vez no carregamento, muitos em painéis
  ocultos (largura 0). Mitigação: desenhar com a largura do contêiner visível mais próximo e redesenhar quando o
  painel aparece (pill, aba, Taxa|Óbitos) ou quando a largura muda mais que 40 px (debounce). No desktop o caminho
  atual (viewBox fixo 680/760) continua sendo o usado, então o risco de regressão ali é baixo.
- **Barra fixa mais alta** (abas + "Nesta seção" + progresso) come altura útil: meta ≤ 100 px no total no celular;
  a faixa do sumário pode se esconder ao rolar para baixo e voltar ao rolar para cima, se passar disso.
- **`<select>`** muda a aparência entre sistemas (nativo de propósito: acessível e com boa usabilidade no toque).
- **Aparelho real**: o Playwright emula viewport e toque, mas não a rolagem inercial nem o teclado virtual; um teste
  num iPhone e num Android fica com o usuário (V7.x).

## 6. Fora do escopo

PWA/offline, modo escuro, gestos de zoom no mapa (pinch), reordenar conteúdo por eixo, mudar textos, PDF e DOCX.

## 7. Registro da implementação (2026-09-28)

- **`css/mobile.css`** em vez de regras espalhadas: as media queries da `website_bugfix` foram movidas para lá; os
  outros três CSS ficaram só desktop, o que torna a garantia "desktop intocado" fácil de conferir.
- **Uma mudança visível no desktop, de propósito**: rótulos finais de linha a menos de 18 unidades são afastados
  (Meninas 152.221 × Meninos 155.513 saíam um sobre o outro também no desktop). Todo o resto, igual pixel a pixel.
- Largura real: `desenhaLinha`/`desenhaBarras`/`pequenosMultiplos` recebem `ctx` (`null` = caminho do desktop, sem
  mudança); `registra()` guarda a configuração no contêiner e um `ResizeObserver` redesenha quando o painel aparece
  ou a largura muda ≥ 40 px. No tablet os painéis de pequenos múltiplos também vão para a largura real (as células
  têm ~210 px), mesmo com o gráfico-pai no desenho fixo.
- Toque: `pointerleave` só para mouse (o `mouseleave` de compatibilidade fechava o tooltip logo depois do toque);
  `pointer-events:all` no retângulo de captura (o Firefox não acertava `fill="transparent"`).
- Pedidos durante a rodada: GitHub/PDF na mesma linha no celular (rótulo curto) e marca d'água do PDF ligada à faixa
  do site por `relatorio/publicacao.json` (LaTeX: `draftwatermark` 3.3 + nó TikZ para a transparência; o pacote
  `transparent` só funciona no pdfTeX e a chave `alpha` não existe nesta versão).
- Resultados em `validation.md`; falta o teste em aparelho real (V7).
