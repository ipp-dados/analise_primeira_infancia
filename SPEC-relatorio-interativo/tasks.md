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
- [ ] **T1.1** — Função `agrupa_em_chart_card(cortes, criterio_grupo)` escrita em
      `build_html_report.py`.
- [ ] **T1.2** — Aplicada aos 4 pontos de repetição identificados
      (`specification.md` §0.1/§2): CID-10 (~18 gráficos → 1 card), CAP evitáveis
      (6-8 mapas → 1 card), cobertura vacinal por ano, evitáveis por subgrupo×CAP.
- [ ] **T1.3** — Confirmado que os demais gráficos (opção única) continuam
      renderizando sem a coluna de pills — nenhuma mudança visual onde não havia
      repetição.

## Bloco 2 — Outliers: cercas de Tukey pré-computadas (plan.md §2)
- [ ] **T2.1** — `remove_outliers_tukey(valores)` escrita e testada com dado
      sintético (< 4 pontos, série sem outlier, série com 1-2 outliers óbvios).
- [ ] **T2.2** — Aplicada a toda série dentro de `opcoes[i]["series"]` (gráficos) e ao
      array de `valor` por região (mapas) — gera `series_sem_outliers`/
      `valor_sem_outliers` ao lado do dado bruto.
- [ ] **T2.3** — `lineChart`/`barChart`/`groupedBarChart` (motor JS) ganham o 2º
      array opcional; toggle de outliers no cliente troca só qual array é lido.
- [ ] **T2.4** — Mapas: região cujo valor virou outlier recebe `fill` neutro
      (`var(--surface-2)`) na variante sem-outliers, sem sumir do SVG.

## Bloco 3 — Mapas: geometria GeoJSON → paths SVG (plan.md §3, maior esforço)
- [ ] **T3.1** — `carrega_geometria_svg(nivel)` escrita: lê
      `dados_locais/geo/limite_bairros_rio.geojson`, dissolve por `area_plane`/
      `cod_rp` quando `nivel != 'bairro'`, projeta para viewBox fixo.
- [ ] **T3.2** — `poligono_para_path_d` lida corretamente com `MultiPolygon`
      (ilhas/dissoluções com múltiplos anéis) — testado em pelo menos 1 bairro
      insular e 1 AP dissolvida.
- [ ] **T3.3** — `monta_mapa_svg_card` escrita: aplica a paleta sequencial por tema
      já definida (`_CORES_TEMA_MAPA`), gera `paths` no esquema do Bloco 1.
- [ ] **T3.4** — Aplicada a pelo menos 1 mapa por tema (natalidade/mortalidade/
      cadúnico/censo) e a pelo menos 1 mapa por nível (bairro/AP/RP).
- [ ] **T3.5** — Confirmado visualmente: sem basemap/contexto geográfico (§3.5 item
      6 — só polígonos + tooltip), título/footnote/legenda continuam como HTML ao
      lado do `<svg>`.
- [ ] **T3.6** — Tooltip por região funcionando (reaproveita o controlador do
      Bloco 4) — rótulo (nome do bairro/CAP) + valor formatado pt-BR.

## Bloco 4 — Motor JS: novos controladores (plan.md §4)
- [ ] **T4.1** — `chartOptionSwitcher` (seletor de opção por chart-card, pills
      verticais) escrito e funcionando em pelo menos 1 gráfico e 1 mapa.
- [ ] **T4.2** — `sectionToggle` (collapse por `h2`) escrito — estado inicial
      expandido, sem persistência entre sessões (§3.1).
- [ ] **T4.3** — `outlierToggle` escrito, ligado ao 2º array do Bloco 2.
- [ ] **T4.4** — `downloadCsv` escrito — testado gerando CSV válido (abre sem erro
      em planilha) para 1 gráfico e 1 mapa, respeitando opção ativa + toggle de
      outliers no momento do clique.
- [ ] **T4.5** — `lineChart` ganha rótulo fixo de máximo/mínimo/mais recente
      (§3.9) — testado com série onde os 3 coincidem parcialmente (ex.: mais
      recente = mais alto) para confirmar que não duplica rótulo.
- [ ] **T4.6** — Tooltip com rótulo + valor confirmado em **todo** tipo de marca:
      ponto de linha, barra, região de mapa (§3.8) — não só nos tipos que já
      tinham tooltip antes desta rodada.

## Bloco 5 — CSS: camada institucional + barra de espectro (plan.md §5)
- [ ] **T5.1** — Variáveis `--ipp-navy`/`--ipp-cyan` adicionadas.
- [ ] **T5.2** — Barra de 4px no topo + chip do logo no navbar + rodapé navy —
      nenhuma outra cor de fundo do corpo do relatório alterada.
- [ ] **T5.3** — Eyebrow do header e de seções **expandidas** em `--accent-ink`
      peso 700; seções **recolhidas** continuam no `.eyebrow` padrão (§3.12) —
      conferir visualmente que a diferença de cor bate com o estado de collapse.
- [ ] **T5.4** — Barra de espectro (11 cores) só no bloco de título — confirmado
      que não se repete em nenhum cabeçalho de seção.
- [ ] **T5.5** — Cartões novos (chart-card, seção, callout de achados) com borda
      `2px solid var(--ink)`/`border-radius:0` — cartões pré-existentes fora do
      escopo desta rodada não tocados.
- [ ] **T5.6** — Contraste do texto do rodapé sobre navy checado (WCAG AA) — item
      sinalizado em `specification.md` §8.3.

## Bloco 6 — Rodapé (plan.md §6)
- [ ] **T6.1** — `monta_rodape(data_geracao)` escrita — data sempre derivada do
      momento do build, não hardcoded.
- [ ] **T6.2** — **Confirmar as URLs reais** de Transparência Rio/LGPD e o e-mail
      de contato corretos para este relatório (os do mockup eram ilustrativos,
      copiados do rodapé do site institucional principal — plan.md §6).
- [ ] **T6.3** — Rodapé renderizado com escopo enxuto confirmado (§3.11/§4-M): sem
      endereço/telefone/ícones de redes sociais.

## Bloco 7 — Navbar persistente (plan.md §7)
- [ ] **T7.1** — Navbar sticky substitui o bloco "Sumário" atual.
- [ ] **T7.2** — Painel do hambúrguer lista as 9 seções (emoji + título), âncoras
      batendo com os `id` que os `h2` já usam — nenhum link quebrado.
- [ ] **T7.3** — Chip do logo institucional no navbar (Bloco 5) renderizando ao
      lado do hambúrguer.

## Bloco 8 — Geração completa e validação manual
- [ ] **T8.1** — `build_html_report.py` rodado do zero, gera `relatorio/index.html`
      sem erro.
- [ ] **T8.2** — Aberto em navegador (Chrome headless ou interativo, conforme
      disponibilidade do ambiente) — 0 erros de console.
- [ ] **T8.3** — Spot-check funcional: seletor de opção troca o gráfico/mapa
      exibido em pelo menos 1 instância de cada (CID-10, CAP); toggle de
      outliers muda o array plotado; collapse de pelo menos 2 seções (`h2`)
      funciona nos dois sentidos; download CSV de 1 gráfico e 1 mapa confirmado
      abrindo em planilha.
- [ ] **T8.4** — Spot-check visual: barra de espectro só no topo; eyebrow de seção
      expandida vs. recolhida com cores diferentes conforme §3.12; rodapé navy
      renderizando com o conteúdo do Bloco 6; navbar com o chip do logo.
- [ ] **T8.5** — Responsividade básica: página testada em largura estreita
      (~375-420px) — comportamento do seletor de pills + painel de análise ao
      lado do mapa registrado (mesmo que a solução definitiva fique para depois,
      conforme `specification.md` §8.2, confirmar que nada quebra/overflow
      horizontal grave).
- [ ] **T8.6** — Tema claro/escuro automático (`prefers-color-scheme`) confirmado
      sem regressão — cores institucionais (navy/cyan) e barra de espectro
      legíveis nos dois temas.

## Bloco 9 — Deploy (plan.md §8)
- [ ] **T9.1** — **Confirmar T0.4 (autorização do logo) antes de prosseguir.**
- [ ] **T9.2** — `.github/workflows/deploy-relatorio.yml` escrito
      (`workflow_dispatch`, `actions/upload-pages-artifact` + `actions/deploy-pages`).
- [ ] **T9.3** — Decidido o escopo exato do `path:` publicado (só `index.html`
      vs. `relatorio/` inteiro, incluindo os PDFs) — plan.md §8.
- [ ] **T9.4** — GitHub Pages habilitado nas configurações do repositório
      (Settings → Pages → Source: GitHub Actions) — passo manual, fora do workflow.
- [ ] **T9.5** — Deploy disparado manualmente 1x, URL pública conferida abrindo
      no navegador.

## Bloco 10 — Documentação e fechamento
- [ ] **T10.1** — `relatorio/specs.md` atualizado com a entrada "v6" (este spec).
- [ ] **T10.2** — `README.md` atualizado se a estrutura do projeto mudou
      (workflow novo em `.github/`, módulo `mapas_svg.py` se separado).
- [ ] **T10.3** — `feature_roadmap.md`: remover os itens desta rodada que ficaram
      resolvidos; manter só os deferidos (basemap nos mapas SVG, botão "baixar
      tudo", persistência de collapse — já registrados).
- [ ] **T10.4** — `tasks.md`/`validation.md` fechados.
- [ ] **T10.5** — **Merge em `staging_main` (só após aval do usuário)**.
