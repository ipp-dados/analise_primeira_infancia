# Tasks — SPEC-relatorio-interativo

## Bloco 0 — Decisões
- [x] **T0.1** — Especificação e decisões A-N aprovadas pelo usuário (`specification.md` §4).
- [x] **T0.2** — Branch `spec/relatorio-interativo` criada a partir de `staging_main`.
- [x] **T0.3** — Layout revisado (canvas de design, 3 artboards: Main/States/HeaderOptions) aprovado, opção A do bloco de título escolhida.
- [ ] **T0.4** — **Gate de autorização do logo** (`specification.md` §3.10/§4-K): confirmar
      com alguém do IPP que o uso do brasão/logo oficial da Prefeitura do Rio neste
      relatório está autorizado. Bloqueia o Bloco 9 (deploy público) — não bloqueia o
      desenvolvimento/preview local.

## Bloco 1 — Esquema de dado: chart-card com opções nomeadas (plan.md §1)
- [x] **T1.1** — Implementado como `option_card(entries)` em `build_html_report.py`
      (mais simples que o `agrupa_em_chart_card` esboçado no plan.md: cada opção
      é pré-renderizada pelo Python via as funções de gráfico já existentes —
      `line_chart`/`bar_chart`/`grouped_bar_chart`/`mapa_svg` — e o JS só troca
      qual painel fica visível, sem re-renderizar SVG no cliente. Mais barato de
      implementar corretamente e mantém tooltip/outlier/download funcionando
      "de graça" em cada opção, ao custo de não reduzir o peso do HTML — ver
      nota de escopo abaixo).
- [x] **T1.2** — Aplicada aos 2 casos que, na leitura real do código (não só na
      estimativa do spec), são de fato "parede de gráficos quase idênticos":
      **"Por CAP e faixa etária"** (18 combinações faixa×subgrupo → 1 card,
      confirmado visualmente) e **"Grupo evitável, por CAP"** (3 faixas → 1
      card, cada opção com o par absoluto/percentual). Os outros dois candidatos
      do spec original — "cobertura vacinal por ano" e "evitáveis por
      subgrupo×CAP" — na prática **já eram** 1 gráfico multi-série cada (não uma
      parede de gráficos repetidos); "evitáveis por subgrupo×CAP" é o mesmo caso
      já coberto por "Por CAP e faixa etária" acima. A galeria de mapas do CAP
      (8 PNGs) foi deixada como grade (não virou seletor) — são 8 indicadores
      genuinamente diferentes (não cortes do mesmo indicador), forçar pills ali
      pioraria a comparação lado a lado.
- [x] **T1.3** — Confirmado via screenshot: gráficos de opção única (a maioria)
      renderizam sem coluna de pills.

## Bloco 2 — Outliers: cercas de Tukey pré-computadas (plan.md §2)
- [x] **T2.1** — `remove_outliers_tukey(valores)` escrita (< 4 pontos finitos
      retorna a série inalterada). Não testada com casos sintéticos isolados,
      mas exercitada em massa pela geração real (ver T8.1) — o relatório saiu
      de ~73 para 122 chamadas de render, confirmando que a maioria das séries
      reais tem pelo menos 1 outlier pela regra 1.5×IQR.
- [x] **T2.2** — Aplicada centralmente dentro de `line_chart`/`bar_chart`/
      `grouped_bar_chart`/`mapa_svg` (não precisou editar os ~48+ call sites
      individualmente — as 4 funções são o único ponto de entrada).
- [x] **T2.3** — Implementado como pré-renderização dupla (variante bruta +
      variante limpa, cada uma um gráfico real e independente) + toggle JS de
      visibilidade — ver nota em T1.1 sobre a mudança de abordagem vs. plan.md.
- [x] **T2.4** — Região com valor mascarado usa `fill:var(--surface-2)` — código
      escrito e confirmado no HTML gerado; não clicado interativamente nesta
      rodada (ver T8.3).

## Bloco 3 — Mapas: geometria GeoJSON → paths SVG (plan.md §3, maior esforço)
- [x] **T3.1** — `_carrega_bairros_geo()` escrita e funcionando — **só nível
      bairro nesta rodada** (166 features confirmadas no mapa gerado). Dissolve
      por `area_plane`/`cod_rp` (AP/RP) **não implementado** — escopo
      explicitamente reduzido para caber nesta rodada (ver nota abaixo);
      registrado como follow-up mecânico, não um problema de design.
- [x] **T3.2** — `_geom_path_d` trata `MultiPolygon` (anéis exterior + buracos).
      Testado indiretamente: o mapa renderizado (screenshot) mostra o
      arquipélago/ilhas do Rio corretamente, sem polígono quebrado visível —
      não isolei um bairro insular específico para um teste unitário dedicado.
- [x] **T3.3** — `mapa_svg()` escrita: aplica `_CORES_TEMA_MAPA` (tema `censo`
      → `Blues`), gera bins discretos (contagem) ou escala contínua (%),
      confirmado visualmente com legenda correta em ambos os modos.
- [~] **T3.4** — Aplicado a **1 indicador, nível bairro, tema `censo`** (Censo
      0-4 anos, absoluto + percentual — as 2 variantes do mesmo indicador,
      confirmando os dois modos de legenda). **Não** aplicado aos outros 3 temas
      (natalidade/mortalidade/cadúnico) nem aos níveis AP/RP — ver "Escopo
      reduzido" abaixo. Os ~30 mapas restantes continuam como PNG (`map_card`,
      inalterado).
- [x] **T3.5** — Confirmado visualmente: os 2 mapas SVG não têm basemap, UF, ou
      labels de município vizinho — só polígonos + legenda + footnote de fonte,
      como especificado.
- [x] **T3.6** — Tooltip por região implementado (`initMapTooltips`, lê
      `data-label`/`data-valor` de cada `<path>`) — confirmado por inspeção do
      DOM gerado (atributos presentes e corretos); não testado com hover real
      num navegador interativo nesta rodada.

**Escopo reduzido do Bloco 3 (decisão tomada durante a implementação, não
prevista no plan.md original):** o pipeline geométrico funciona de ponta a
ponta e está provado com um indicador real, mas convertê-lo para os ~30 mapas
restantes (4 temas × 3 níveis × várias faixas etárias) é essencialmente um
trabalho mecânico de call sites, não uma decisão de design nova. Dado o
tamanho da rodada, ficou como próximo passo natural — não fica bloqueado por
nenhuma decisão em aberto, só falta tempo de execução.

## Bloco 4 — Motor JS: novos controladores (plan.md §4)
- [x] **T4.1** — Seletor de opção (`initPills`) — confirmado visualmente
      funcionando (pill ativa destacada, painel correspondente visível) na
      seção "Por CAP e faixa etária".
- [x] **T4.2** — `initSections` (collapse por `h2`) — estrutura HTML confirmada
      (9 `.rsec`, todas sem `data-collapsed` inicial = expandidas por padrão);
      clique não testado interativamente nesta rodada (ver T8.3).
- [x] **T4.3** — `initOutliers` — botões "× Remover outliers" confirmados
      visualmente em todos os gráficos/mapas com outlier detectado.
- [x] **T4.4** — `initDownloads` — botão "⭳ CSV" presente em 126 chart-cards no
      HTML gerado; não clicado/verificado abrindo em planilha nesta rodada.
- [x] **T4.5** — Rótulo fixo de máx/mín/recente — confirmado visualmente em
      várias séries (ex.: picos "568"/"443"/"176" no gráfico de subgrupo × CAP);
      caso de coincidência (recente = extremo) tratado pulando o índice
      repetido — corrigido durante a validação: a 1ª versão também rotulava o
      1º ponto quando ele era um extremo, colidindo com o eixo Y em séries
      curtas (ex.: série de 3 pontos do Censo) — agora pula `idx===0` também,
      não só `idx===lastValidIdx`.
- [x] **T4.6** — Tooltip com rótulo + valor: já existia para linha/barra
      (motor herdado); estendido a mapas SVG nesta rodada (T3.6).

## Bloco 5 — CSS: camada institucional + barra de espectro (plan.md §5)
- [x] **T5.1** — `--ipp-navy`/`--ipp-cyan` adicionadas.
- [x] **T5.2** — Barra de 4px + chip do logo + rodapé navy confirmados
      visualmente; nenhuma outra cor de fundo do corpo do relatório mudou.
- [x] **T5.3** — Eyebrow do header e de seções expandidas em `var(--accent)`
      (não `--accent-ink)` — **bug real encontrado e corrigido durante a
      validação**: `--accent-ink` no tema escuro é quase preto (pensado para
      texto sobre um chip claro, não para texto direto sobre o fundo da
      página) — usá-lo teria deixado o eyebrow ilegível no tema escuro. Trocado
      para `--accent`, que já é a variável usada para links em ambos os temas.
      Confirmado legível no tema escuro (screenshot real, ver T8.6).
- [x] **T5.4** — Barra de espectro confirmada só no topo (1 ocorrência).
- [x] **T5.5** — `.rsec`/`.option-card`/`.outlier-card`/chart-cards novos com
      borda `2px solid var(--ink)`; cartões pré-existentes (`.out` original,
      `.map-card` PNG) não tiveram sua borda alterada.
- [ ] **T5.6** — Contraste do rodapé **não medido formalmente** (sem ferramenta
      de contraste neste ambiente) — inspeção visual do screenshot sugere
      legibilidade adequada, mas fica como pendência real, não confirmada.

## Bloco 6 — Rodapé (plan.md §6)
- [x] **T6.1** — Rodapé com data de geração dinâmica (`gen_date`, mesma variável
      já usada no cabeçalho) — confirmado no HTML gerado.
- [ ] **T6.2** — **Não confirmado** — URLs de Transparência Rio/LGPD e e-mail de
      contato continuam os valores ilustrativos copiados do site institucional
      principal. Pendência real, sinalizada no código (`build_html_report.py`,
      comentário acima de `FOOTER_LINKS`).
- [x] **T6.3** — Rodapé confirmado enxuto no screenshot: logo, fontes, links,
      contato, data — sem endereço/telefone/redes sociais.

## Bloco 7 — Navbar persistente (plan.md §7)
- [x] **T7.1** — Navbar sticky substitui o "Sumário" antigo (removido).
- [x] **T7.2** — 9 links gerados a partir do `toc` (nível `h2`), mesmos `id`
      dos `h2` originais — confirmado por contagem no DOM (9 `.navbar-link`,
      9 `.rsec`, âncoras batendo 1:1).
- [x] **T7.3** — Chip do logo confirmado visualmente no navbar.

## Bloco 8 — Geração completa e validação manual
- [x] **T8.1** — `build_html_report.py` rodado várias vezes durante a
      implementação, sem erro; gerou `relatorio/index.html` (122 chart-renders,
      9 h2 / 21 h3).
- [x] **T8.2** — Aberto via Edge headless (`--headless=new --dump-dom
      --enable-logging=stderr`) — nenhum erro/exceção de JavaScript da página
      encontrado no log (só ruído interno do browser — sync, extensões).
- [~] **T8.3** — Spot-check **estrutural** (contagem de elementos no DOM: 9
      `.rsec`, 2 `.option-card`, 51 `.outlier-card`, 126 `.dl-btn`, 9
      `.navbar-link`) e **visual** (screenshots) confirmam que tudo está
      presente e com o estado inicial correto. **Não testado**: clicar de fato
      numa pill/outlier-toggle/collapse/download e observar a mudança de
      estado em um navegador interativo — headless-screenshot só mostra o
      estado inicial da página. Recomendo um teste manual rápido no navegador
      antes de considerar este bloco 100% fechado.
- [x] **T8.4** — Spot-check visual confirmado via screenshots reais (9 seções
      inspecionadas): barra de espectro só no topo, eyebrow expandida colorida,
      rodapé navy, chip do logo, mapas SVG com legenda correta.
- [ ] **T8.5** — Responsividade em largura estreita **não testada** nesta
      rodada (só validado em 1280px).
- [x] **T8.6** — Tema escuro confirmado (o ambiente de screenshot usa
      `prefers-color-scheme: dark` por padrão — acabou sendo o teste real, e
      foi o que revelou o bug de T5.3). **Tema claro não testado** nesta
      rodada — usa a mesma variável (`--accent`) já validada em produção no
      tema claro antes desta spec, risco considerado baixo mas não confirmado.

## Bloco 9 — Deploy (plan.md §8)
- [ ] **T9.1** — Depende de T0.4 (autorização do logo), ainda em aberto.
- [x] **T9.2** — `.github/workflows/deploy-relatorio.yml` escrito
      (`workflow_dispatch`, `actions/configure-pages` + `upload-pages-artifact`
      + `deploy-pages`).
- [x] **T9.3** — Decidido: só `relatorio/index.html` (copiado para
      `_site/index.html` antes do upload) — não publica `Page 1.pdf` nem o PDF
      de ~50MB.
- [ ] **T9.4** — GitHub Pages **não habilitado** nas configurações do
      repositório — ação manual fora do alcance desta sessão (precisa acesso
      admin ao repo no GitHub).
- [ ] **T9.5** — Deploy **não disparado** — depende de T9.4 e do push desta
      branch para o GitHub.

## Bloco 10 — Documentação e fechamento
- [x] **T10.1** — `relatorio/specs.md` atualizado com a entrada "v6".
- [x] **T10.2** — Não foram necessárias mudanças em `README.md` além do que já
      cobre `build_html_report.py` — o workflow novo em `.github/` é
      autoexplicativo e documentado no próprio arquivo.
- [x] **T10.3** — `feature_roadmap.md` atualizado: itens resolvidos removidos,
      novo item para a conversão dos mapas restantes (Bloco 3) e para T6.2/T5.6.
- [x] **T10.4** — Este arquivo e `validation.md` fechados nesta rodada.
- [ ] **T10.5** — **Merge em `staging_main` (só após aval do usuário)** — e só
      depois de T0.4/T9.4/T9.5 para o deploy público especificamente; o merge
      do código em si não depende desses três.
