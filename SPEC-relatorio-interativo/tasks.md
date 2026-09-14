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
