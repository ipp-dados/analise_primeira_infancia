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
**Atualizado na rodada de fidelidade ao mockup — escopo completado, não mais
reduzido.** `_geo_nivel(nivel)` generalizada para os 4 regimes de geometria
que `analise.py` de fato usa (conferidos um a um em `mapa_coropletico_bairros`,
não estimados): `bairro` (166, join direto `codbairro`/`codigo`), `ap`/`rp`
(dissolve do geojson de bairros por `area_plane`/`cod_rp`, mesmas colunas de
`agrega_bairros_por_nivel` em analise.py) e `cap` (geometria própria,
`dados_locais/geo/limite_ap_saude_rio.geojson`, chave `cod_ap_sms` — as 10
CAPs de saúde da SMS-Rio, confirmadas **diferentes** da AP/RP de planejamento
urbano apesar da numeração parecida — checado no código-fonte antes de
implementar, não assumido).
- [x] **T3.1** — Geometria carregada para os 4 níveis: bairro (166), AP (5,
      dissolve), RP (16, dissolve), CAP (10, geojson próprio).
- [x] **T3.2** — `_geom_path_d` trata `MultiPolygon`; confirmado visualmente
      nos 4 níveis (ilhas do bairro, e as formas de AP/RP/CAP) sem polígono
      quebrado.
- [x] **T3.3** — `mapa_svg()` aplica `_CORES_TEMA_MAPA` (4 temas: `censo`,
      `natalidade`, `mortalidade`, `cadunico`), bins discretos ou escala
      contínua conforme o indicador — confirmado visualmente nos 4 temas.
- [x] **T3.4** — **Todos os ~32 mapas convertidos** (não mais 1 de prova de
      conceito): 18 indicadores bairro, 4 Censo AP/RP (absoluto+percentual —
      o denominador "Total" não vem exportado em `censo_por_bairro.csv`,
      recuperado por álgebra exata a partir de `0 a 4 anos`/`Percentual 0 a 4`,
      não por aproximação), 8 mapas CAP-saúde (6 grupo evitável + 2 subgrupo
      gestação/parto, lidos direto de `tabelas_finais/mortalidade_evitaveis_cap_2025.csv`
      e `tabela_mapa_obitos_evitaveis_{gestacao,parto}_menores_1_ano_cap_2025.csv`
      — os mesmos exports que `analise.py` já gera para esses mapas, não uma
      tabela derivada nova). Nenhum PNG de indicador restante;
      `map_card`/`maps_block`/`check_maps` ficam só como fallback morto.
- [x] **T3.5** — Confirmado visualmente nos 4 níveis: sem basemap/UF/labels de
      município vizinho — só polígonos + legenda + footnote de fonte.
- [x] **T3.6** — Tooltip por região implementado e confirmado por inspeção do
      DOM (atributos `data-label`/`data-valor` presentes e corretos em todos
      os 4 níveis); não testado com hover real num navegador interativo.

**Bug real encontrado e corrigido nesta rodada**: `_carrega_bairros_geo`/
`_geo_nivel` usavam a mesma chave de cache (`"bairro"`) para o GeoDataFrame
bruto e para o resultado do nível `'bairro'` — o segundo sobrescrevia o
primeiro, quebrando o dissolve de AP/RP (`TypeError: tuple indices must be
integers`, já que o código tentava indexar uma tupla como se fosse o
GeoDataFrame). Corrigido separando as chaves de cache (`_base_bairro` vs.
`bairro`/`ap`/`rp`/`cap`). Também corrigido: uma linha de agregado
("EM BRANCO", sem `codigo` numérico) numa das tabelas de mapa do DataSUS
quebrava a conversão de chave — `mapa_svg` agora pula silenciosamente
qualquer linha cuja chave não converte para o tipo esperado do nível, em vez
de propagar a exceção.

**Trade-off conhecido, não resolvido nesta rodada**: cada mapa embute sua
geometria SVG como texto, sem compartilhar paths entre instâncias do mesmo
nível — `relatorio/index.html` foi de ~5MB para ~20MB. Registrado em
`feature_roadmap.md` como otimização futura (`<defs>`/`<use>`, ou um mapa
`codigo→d` referenciado por id).

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
- [x] **T5.5** — **Corrigido na rodada de fidelidade ao mockup**: o `.out`
      original (todo chart-card, não só os componentes novos) ainda tinha
      `border-radius:10px` + `box-shadow` — visivelmente diferente do mockup
      aprovado, apesar de `.rsec`/`.option-card`/`.outlier-card` já estarem
      corretos. `.out{border:2px solid var(--ink); border-radius:0;
      box-shadow:none;}` agora vale para **todo** cartão do relatório, sem
      exceção — confirmado visualmente em gráficos, mapas SVG e os cartões
      de opção/outlier.
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

## Bloco 11 — Replanejamento: texto por opção, tema único, outliers só em
taxas, agrupamento (plan.md §10) — **implementado e validado nesta rodada**
- [x] **T11.1** — `option_card` ganha `texto` por opção (`(label, build_fn,
      seed)`, plan.md §10.1). Os 2 grupos já existentes ("Por CAP e faixa
      etária", "Grupo evitável por CAP" — este último fundido com
      "Gestação/parto por CAP" nesta rodada, ver T11.4) também ganharam
      texto, não só os grupos novos. `viz()` (açúcar sintático sobre
      `option_card`, seed=label) criado para os ~25 call sites que não
      precisavam de um seed diferente do label.
- [x] **T11.2** — 3 padrões de CSS (grid) implementados —
      `.option-card-grafico` (texto abaixo, largura total),
      `.option-card-mapa` (texto na 3ª coluna), `.table-with-text` (texto à
      esquerda, tabela à direita, sem pills) — confirmados visualmente nos
      3, incluindo a variante `.option-card-single` (sem pills, 1 opção só).
- [x] **T11.3** — `_lorem(seed, palavras=500)` escrita e usada em todo card —
      **bug real encontrado e corrigido na validação**: 500 palavras sem
      limite de altura estourava o layout (a coluna de texto da Censo
      "Top 10 bairros" ficava ~15 telas mais alta que a tabela ao lado,
      deixando um vão em branco enorme). Corrigido com `.opt-text{max-height:
      240px; overflow-y:auto;}` — a caixa de texto agora tem altura fixa e
      rola internamente, em todo os 3 padrões (não só a tabela).
- [x] **T11.4** — Agrupamento aplicado seção por seção (Censo: tabela
      →padrão C, população raça/sexo→2 pills, mapas→6 pills, série
      temporal→2 pills; CadÚnico: renda/idade→2 pills, mapas→3 pills;
      DataSUS: séries→4 pills, mapas→5 pills; evitáveis: raça→4 pills,
      CID-10→8 pills, panorama-por-subgrupo→3 pills (não estava na proposta
      original de §9, adicionado ao notar o mesmo padrão de repetição),
      "Grupo evitável"+"Gestação/parto"→fundidos em 5 pills, mapas
      CAP→revertido de grade solta para 8 pills; gravidez/puerpério→2+2
      pills; neonatal→4 pills (gráfico) + 8 pills (mapa); SISVAN→3 pills;
      EPI→2 pills; Educação SIDRA→4 pills, PNAD/Matrículas mantidos soltos
      por decisão explícita (fontes diferentes, não um corte comparável,
      mesmo critério de "Comparação entre faixas etárias"). Nenhuma chamada
      solta de `line_chart`/`bar_chart`/`grouped_bar_chart`/`mapa_svg`/
      `plain_table` ficou fora de `option_card`/`viz`/`tabela_com_texto` —
      confirmado por grep (0 resultados para chamada no início de linha).
- [x] **T11.5** — Outliers com gate por formato (`_eh_taxa_ou_percentual`)
      aplicado nas 4 funções. Contagem de outlier-cards caiu de 51 (rodada
      anterior) para 22 — confirmado, só séries/mapas percentual/taxa
      restaram.
- [x] **T11.6** — Bloco CSS de tema escuro removido por completo (`@media
      (prefers-color-scheme: dark)` + `:root[data-theme="dark"]`), `:root`
      ganhou `color-scheme:light` explícito. `grep -c "prefers-color-scheme:
      dark"`/`data-theme="dark"` no HTML gerado = 0/0, confirmado.
- [x] **T11.7** — `.doc{max-width:1200px}` — e os outros 4 lugares que
      hardcodavam `880px` (navbar-link, footer-cols, footer-rule,
      footer-credit) também atualizados para consistência, não previsto
      explicitamente no plan.md original mas necessário para o rodapé/navbar
      não ficarem mais estreitos que o corpo.
- [x] **T11.8** — Geração completa + validação visual (Edge headless,
      screenshot real de ~20000px) confirmando os 3 padrões, o agrupamento,
      tema único e o corpo mais largo. DOM dump + log de console sem erros
      de JavaScript da página (só ruído interno do browser). **Não
      testado**: troca de pill real via clique interativo (mesma limitação
      já registrada em T8.3 — só o estado inicial foi observado).

## Bloco 12 — Ajustes finos pós-mockup: header, navbar, mapas, achados

- [x] **T12.1** — Lorem ipsum reduzido de 500 para 200 palavras
      (`_lorem(seed, palavras=200)`).
- [x] **T12.2** — `.doc-head-row` trocado de `flex;flex-wrap:wrap` para
      `grid;grid-template-columns:1fr 420px` — título e descrição não
      empilham mais mesmo quando a largura combinada excede o container
      (o flex antigo permitia isso via `flex-wrap`). Breakpoint
      `max-width:760px` volta para coluna única.
- [x] **T12.3** — Gap do navbar no topo da página corrigido: `.doc` perdeu
      o `padding-top:64px` (motivo real do gap — navbar/topbar-accent são
      os primeiros filhos de `.doc`, então o padding do container os
      empurrava para baixo do topo real do viewport). O respiro voltou como
      `header.doc-head{padding-top:56px}`, que não afeta a posição do
      navbar (elemento irmão anterior).
- [x] **T12.4** — Mapas: coluna de pills lateral (200px) removida do
      padrão `option-card-mapa`; pills agora ficam numa fileira acima do
      mapa (`grid-template-areas:"pills pills" "map text"`,
      `.option-card-mapa .pill-col{flex-direction:row}`). Mapa ganhou mais
      espaço (`max-width` de 480px → 620px, container com fundo
      `--surface-2` + borda). Breakpoint mobile (≤720px) já empilhava tudo
      em 1 coluna e continua correto sem alteração.
- [x] **T12.5** — Bloco "Principais achados" adicionado ao início de cada
      seção `h2` (dentro de `.section-body`, antes do conteúdo real) —
      fundo cinza claro (`--surface-2`), rótulo eyebrow + 5 bullets
      placeholder (`_lorem_bullets`, 8 palavras cada, seed determinístico
      por seção). Texto ainda é lorem ipsum — fica registrado em
      `feature_roadmap.md` que isso precisa de curadoria real depois.
- [x] **T12.6** — Auditoria de cor do título de seção: o `<h2>` já herdava
      `--ink` (preto) do `body` — não havia regra verde nele. O que
      provavelmente lia como "título verde" era o eyebrow
      (`SEÇÃO N DE M`, cor `--accent`) ficar *inline* com o `<h2>` na mesma
      linha de base (`.rsec-head-l{align-items:baseline}`), sem diferença
      de fonte/tamanho — os dois liam como uma unidade colorida. Corrigido
      reestruturando para empilhado (eyebrow acima, título abaixo, como no
      cabeçalho principal) e adicionando a regra base `.eyebrow{}` que
      faltava (mono, uppercase, letter-spacing, tamanho pequeno) — antes
      cada `.eyebrow` dependia só de classes compostas (`.doc-eyebrow`,
      `.rsec-eyebrow`) para cor, sem tipografia própria, então o rótulo
      "SEÇÃO N DE M" tinha o mesmo tamanho/peso do texto do corpo. `h2`
      também ganhou `color:var(--ink)` explícito por robustez.
- [x] **T12.7** — Grupos de mapas com "muitas" opções (limiar: 6+)
      divididos em 2 subgrupos com um `h5` rotulando cada um: Censo
      (6→3+3, Absoluto/Percentual), Óbitos evitáveis por CAP (8→6+2, por
      faixa etária/por subgrupo gestação-parto), Mortalidade neonatal
      (8→4+4, Óbitos/Taxa). DataSUS (5) e CadÚnico (3) ficaram como
      estavam — não "muitos" o bastante para justificar a divisão.
- [x] **T12.8** — Estilo cartográfico dos mapas SVG alinhado ao padrão dos
      PNG de `mapas/` (`analise.py::mapa_coropletico_bairros`), só sem
      basemap real (decisão via AskUserQuestion: "estilo cartográfico
      apenas, sem tiles reais" — projeção lon/lat simplificada usada nos
      SVGs não é Web Mercator, alinhar tiles reais exigiria re-derivar a
      projeção sem poder validar no browser real). Mudanças: título do
      mapa em serifa (`--font-display`, antes usava a mesma classe sans
      dos gráficos), legenda agora numa caixa com borda/fundo (antes
      flutuava sem chrome), rodapé de 2 linhas "Sistema de referência:
      SIRGAS 2000, UTM - Fuso 23S" + "Fonte: ..." (convenção do PNG,
      `ax.annotate` em `analise.py`), fundo neutro (`--surface-2`) atrás do
      SVG do mapa (contexto visual sem ser um basemap real).
- [x] **T12.9** — Geração completa (17,2MB, 83 gráficos, 9 h2/13 h3) +
      validação visual via Edge headless (header, navbar, seção Censo
      completa incl. achados + os 2 grupos de mapas divididos). DOM dump +
      log sem erros de JS. **Não testado**: clique real em pill (mesma
      limitação de sempre — só o estado inicial renderizado é observável
      sem interação real no browser).

## Bloco 13 — Fundo cartográfico real, rosa dos ventos, escala, legenda
## dentro do mapa, alinhamento da navbar

- [x] **T13.1** — Navbar: `.navbar` (full-bleed) perdeu o `padding:0 24px`
      direto — o padding/flex foi movido pra um `.navbar-inner` novo
      (`max-width:1200px;margin:0 auto;padding:0 24px`), o mesmo padrão
      já usado por `.navbar-link`/`.footer-cols`. Causa raiz do
      desalinhamento: `.navbar` tinha só `padding:24px` fixo a partir da
      viewport (sem `max-width`+`margin:auto`), então em telas >1248px de
      largura o conteúdo do navbar ficava mais perto da borda da tela do
      que o conteúdo de `.doc` (que é 1200px centralizado) — confirmado
      visualmente (screenshot 1400px: burger e eyebrow do header alinham
      na mesma coluna x agora).
- [x] **T13.2** — Rosa dos ventos (seta "N", `_svg_rosa_dos_ventos`) e
      barra de escala (`_svg_barra_escala`) adicionadas a todo mapa SVG,
      desenhadas como `<g>` dentro do próprio SVG (não dependem de
      biblioteca externa). A escala usa `project.scale` (px por grau,
      exposto via atributo na função `project` — refactor mínimo, não
      mudou a assinatura usada em nenhum outro call site) convertido pra
      metros reais (111.320 m/grau) e arredondado pro múltiplo "legível"
      mais próximo (1/2/5 × 10ⁿ), igual convenção de barra de escala
      cartográfica.
- [x] **T13.3** — Fundo cartográfico REAL adicionado (revertendo a decisão
      da rodada anterior de "só estilo, sem tile"): mesmo provedor do PNG
      (`Esri.OceanBasemap`, via `contextily.bounds2img`), buscado 1x por
      bbox único e reamostrado pra caber exatamente no espaço de pixels
      do SVG (mesma bbox/projeção dos polígonos) — resultado aplicado como
      1 classe CSS compartilhada (`map-bg-N`), não 1 cópia de imagem por
      mapa. **Bug real encontrado e corrigido**: zoom 12 (primeira
      tentativa) devolvia um tile placeholder cinza-azulado ("Map data not
      yet available") pra área terrestre do Rio — confirmado por probe
      manual dos tiles (bytes idênticos em zoom 11 e 13, tile de zoom 12
      pra coordenada central do Rio = placeholder). O Ocean Basemap da
      Esri é voltado a contexto oceânico/costeiro; cobertura terrestre em
      alta resolução não acompanha o `max_zoom:13` anunciado pelo
      provedor. Corrigido fixando `zoom=10` (checado manualmente: mostra
      relevo/rodovias reais, igual ao PNG). Apenas **1 fetch único**
      aconteceu na prática — bairro/AP/RP/CAP-saúde acabaram
      arredondando pro mesmo bbox (4 casas decimais), já que todos os 4
      recortes cobrem o mesmo contorno do município, só particionado
      diferente — achado, não assumido de antemão.
- [x] **T13.4** — Legenda movida de coluna lateral (`.map-legend`, 190px)
      pra overlay absoluto DENTRO do mapa (`.map-legend-overlay`, canto
      superior esquerdo, fundo branco 92% opaco com borda — mesma
      convenção do `legend_kwds` do matplotlib em `analise.py`). Área do
      mapa ganhou o espaço todo que a coluna lateral ocupava
      (`.map-svg-frame` max-width 620px → 760px). `.map-region` ganhou
      `fill-opacity:.88` (não mais opaco 100%) pra o fundo aparecer
      sutilmente através dos polígonos, igual ao `alpha=0.82` usado no
      PNG quando `usa_fundo=True`.
- [x] **T13.5** — Geração completa (17,3MB — +~20KB pela imagem de fundo
      compartilhada, negligível frente aos ~17MB de geometria SVG já
      existente) + validação visual via Edge headless (seção Censo →
      Mapas: fundo real com relevo/rodovias visível, rosa dos ventos,
      barra de escala "10 km", legenda dentro do mapa, mapa bem maior).
      DOM dump + log sem erro de JS. **Não testado**: mapas CAP
      especificamente (mesma classe de fundo que bairro/AP/RP, não
      fotografado em separado — risco de regressão específica a eles é
      baixo mas não zero), clique real em pill, breakpoints móveis.

## Bloco 14 — Reversão do fundo real, fontes +20%, contorno só no mapa,
## sombra, alinhamento do topo, mapa menor

- [x] **T14.1** — **Reversão parcial do fundo cartográfico** (T13.3):
      removida a busca de tiles reais (Esri Ocean Basemap via
      `contextily`) — o usuário pediu explicitamente pra nunca usar
      imagem de mapa/satélite representando TERRA nos mapas, e o retalho
      de padding ao redor da cidade mistura terra (municípios vizinhos) e
      água (baía/oceano) sem uma camada de hidrografia disponível pra
      separar os dois — não havia forma seguro de mostrar só o mar em
      azul sem arriscar colorir terra vizinha também. Fundo voltou a ser
      liso neutro (`--surface-2`), sem tile. Função `_basemap_css_class`
      (e toda a máquina de fetch/cache/CSS associada) removida por
      completo — `contextily`/`numpy` deixaram de ser importados pelo
      gerador.
- [x] **T14.2** — Colormap do tema 'censo' trocado de `Blues` pra `Greys`
      — o choropleth do Censo usava tons de azul pra dado de TERRA
      (população por bairro), o que o usuário também pediu pra nunca
      fazer (azul reservado só pro mar, nunca terra/dado). `natalidade`
      (BuGn), `mortalidade` (RdPu) e `cadunico` (YlOrBr) não mudaram —
      não são lidos como azul puro.
- [x] **T14.3** — Botão de remover outliers movido para o mesmo
      nível/lado do botão de download CSV — antes ficava numa barra
      separada ACIMA do card (`.outlier-toolbar` com
      `display:flex;justify-content:flex-end;margin-bottom:6px`); agora é
      `position:absolute;top:14px;right:100px` sobre `.outlier-card`,
      alinhado ao lado esquerdo do `.dl-btn` (`top:14px;right:14px`,
      inalterado).
- [x] **T14.4** — Todas as fontes ~20% maiores: `html{font-size:19.2px}`
      (era o padrão do browser, 16px) escala automaticamente toda
      unidade `rem` do relatório (praticamente tudo). Os poucos rótulos
      SVG com `px` fixo (não herdam de rem) foram escalados a mão:
      `.axis-label` 9→10.8px, `.end-label` 10.5→12.6px, `.extreme-label`
      8.5→10.2px, `.map-scalebar-label` 8→9.6px, `.map-compass-label`
      11→13.2px, e o rótulo inline do eixo X do grafico de barras
      agrupadas (JS) 10.5→12.6.
- [x] **T14.5** — Lorem ipsum reduzido de 200 pra 150 palavras
      (`_lorem(seed, palavras=150)`).
- [x] **T14.6** — Contorno removido de gráficos/tabelas/texto em geral
      (`.out{border:none}`, `.opt-text{border:none}`) — contorno (+ nova
      sombra) agora é exclusivo do cartão de mapa
      (`.out.map-svg-card{border:2px solid var(--ink);box-shadow:var(--shadow)}`)
      e do texto que acompanha um mapa
      (`.option-card-mapa .opt-text{border:2px solid var(--ink);box-shadow:var(--shadow)}`).
- [x] **T14.7** — Mapa e seu texto lado a lado sem vão entre os dois: (a)
      `.option-card-mapa` ganhou `gap:16px 0` (column-gap zerado — antes
      20px) e `align-items:stretch` (era `start`, herdado de
      `.option-card`); (b) `.map-svg-frame` perdeu o `max-width:760px` —
      sem essa trava, o mapa (SVG vetorial, sem imagem raster desde
      T14.1) preenche 100% da coluna "map" do grid, encostando
      diretamente no texto ao lado; (c) `.option-card-mapa .opt-text`
      ganhou `height:100%;max-height:none` (era `max-height:240px`) pra
      acompanhar a altura real do mapa em vez de um limite fixo.
- [x] **T14.8** — Sombra sutil (`var(--shadow)`, já definida no `:root`)
      adicionada ao cartão de mapa, ao texto que acompanha o mapa (ambos
      em T14.6) e ao bloco "Principais achados" (`.key-takeaways`) —
      pedido explicito citando a Page 1 do PDF de referência como
      inspiração visual.
- [x] **T14.9** — Header: `.doc-head-row` trocado de `align-items:end`
      pra `align-items:start` — eyebrow+título (coluna esquerda) e o
      texto de descrição (coluna direita) agora começam na mesma linha
      do topo, em vez de terminarem alinhados na base.
- [x] **T14.10** — Altura dos mapas reduzida ~20% (`_MAP_H` 560→448) —
      checado antes de aplicar que a margem em branco topo+base (~225px
      dos 560px originais, já que a largura é o eixo que limita a escala
      do Rio, mais largo que alto) absorve o corte inteiro sem cortar
      nenhum polígono real.
- [x] **T14.11** — Geração completa (17,15MB, mais rápida que a rodada
      anterior — 5,8s vs ~9-27s, já que não há mais busca de tile por
      rede) + validação visual via Edge headless: header top-alinhado,
      fontes visivelmente maiores, gráfico/tabela sem contorno, mapa
      cinza (não azul) com contorno+sombra encostado no texto (também
      com contorno+sombra), botão de outlier ao lado do CSV. DOM dump +
      log sem erro de JS. **Não testado**: clique real em pill,
      breakpoints móveis, mapas CAP especificamente (mesma lógica de
      fundo neutro que bairro/AP/RP, não fotografados em separado).

## Bloco 15 — Fechamento desta rodada da spec

- [x] **T15.1** — `feature_roadmap.md` atualizado: item de responsividade
      (antes uma linha solta, nunca testada) reescrito como iniciativa
      própria — `mobile_version` — cobrindo o que falta validar de fato
      (breakpoints existem no CSS desde o Bloco 8 mas nunca foram vistos
      numa viewport estreita real: navbar/burger, os 3 padrões de layout
      empilhados, mapa+legenda overlay, tabelas largas).
- [x] **T15.2** — `relatorio/specs.md` fechado até v6.5; `tasks.md` e
      `validation.md` (este arquivo e o par) fechados até Bloco/V14.
- [ ] **T15.3** — **Merge em `staging_main` (só após aval explícito do
      usuário)** — todo o trabalho de código desta spec (Blocos 0-14)
      está implementado e validado visualmente; o que resta em aberto
      (rodapé com URLs reais, autorização do logo, `mobile_version`,
      GitHub Pages) está todo registrado em `feature_roadmap.md` e não
      bloqueia o merge do código em si, só o deploy público específico
      (ver T0.4/T9.4/T9.5, já detalhado nos Blocos anteriores).
