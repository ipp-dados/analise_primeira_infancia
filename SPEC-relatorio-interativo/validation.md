# Validation — SPEC-relatorio-interativo

Critérios objetivos por bloco, escritos antes da implementação — o alvo, não
o resultado (os critérios abaixo não foram editados após a implementação).

## Status real após a implementação (ver `tasks.md` para o detalhe por bloco)

- **V1-V2 (chart-card, outliers)**: passaram. Aplicado a 2 casos reais de
  repetição (não 4 como o spec original estimava — os outros 2 candidatos
  não eram, na prática, paredes de gráficos repetidos; ver `tasks.md` T1.2).
  Outliers aplicados centralmente, confirmados por geração real (73→122
  chart-renders).
- **V3 (mapas SVG)**: **atualizado numa 2ª rodada** (fidelidade estrita ao
  mockup) — passou por completo, não mais reduzido. Todos os ~32 mapas
  (bairro/AP/RP/CAP-saúde, 4 temas) convertidos, geometria conferida contra
  `analise.py` (não estimada), incluindo a descoberta de que "CAP" usa um
  geojson próprio (`limite_ap_saude_rio.geojson`), diferente da AP/RP de
  planejamento urbano. 2 bugs reais encontrados e corrigidos: colisão de
  chave de cache entre o GeoDataFrame bruto e o resultado do nível `'bairro'`
  (quebrava o dissolve de AP/RP), e uma linha de agregado ("Em branco") numa
  tabela do DataSUS sem `codigo` numérico (quebrava a conversão de chave).
  Trade-off não resolvido: `relatorio/index.html` foi de ~5MB para ~20MB
  (geometria não compartilhada entre instâncias) — ver `feature_roadmap.md`.
- **V4 (motor JS)**: passou por inspeção estrutural do DOM e screenshots reais
  (Edge headless). **Não testado**: clique interativo real (pill/outlier
  toggle/collapse/download) — só o estado inicial foi observado. Um bug real
  foi encontrado e corrigido nesta validação (rótulo de extremo duplicado no
  1º ponto de séries curtas, T4.5).
- **V5 (CSS institucional)**: passou, com 2 bugs reais encontrados e
  corrigidos: `--accent-ink` ilegível no tema escuro (trocado por `--accent`,
  T5.3), e **na 2ª rodada** — o `.out` original (todo chart-card) ainda tinha
  sombra/canto arredondado, destoando visivelmente do mockup apesar dos
  componentes novos já estarem corretos; agora nenhum cartão do relatório
  tem sombra ou canto arredondado. Contraste do rodapé (T5.6) não foi medido
  formalmente.
- **V6 (rodapé)**: estrutura/escopo passaram; URLs e e-mail **não
  confirmados** (T6.2) — continuam placeholders.
- **V7 (navbar)**: passou (contagem 1:1 de links/seções/âncoras no DOM).
- **V8 (geração/validação manual)**: geração e ausência de erro de console
  confirmadas via Edge headless real. Responsividade (T8.5) e tema claro
  (T8.6) não testados nesta rodada — só tema escuro (o default do ambiente
  de screenshot).
- **V9 (deploy)**: workflow escrito e com escopo decidido; **não executado**
  — depende de T0.4 (autorização do logo) e de passos manuais fora do
  alcance desta sessão (habilitar Pages, disparar o Action).
- **V10 (documentação)**: passou — `relatorio/specs.md`, `feature_roadmap.md`,
  `tasks.md` atualizados nesta rodada.

## V0 — Gate de autorização
- `specification.md` T0.4 confirmado: alguém do IPP validou o uso do
  brasão/logo oficial da Prefeitura do Rio. **Sem isso, o Bloco 9 (deploy
  público) não roda** — desenvolvimento e preview local não são
  bloqueados por este item, só a publicação no GitHub Pages.

## V1 — Esquema de dado (chart-card)
- Os 4 pontos de repetição (`specification.md` §0.1/§2) — CID-10, CAP
  evitáveis, cobertura vacinal por ano, evitáveis por subgrupo×CAP —
  cada um vira **exatamente 1** chart-card com N `opcoes`, não mais N
  `div.out` separados.
- Contagem de elementos `.out`/`.map-gallery` na página final é menor que
  a contagem atual (874 linhas / repetições documentadas em
  `specification.md` §0.1) — confirmar com uma contagem antes/depois.
- Gráficos que hoje já são opção única continuam idênticos visualmente
  (sem coluna de pills adicionada onde não havia repetição).

## V2 — Outliers
- `remove_outliers_tukey` com < 4 pontos retorna a série inalterada (não
  filtra nada — regra explícita do plan.md §2).
- Uma série sintética com 1 outlier óbvio (ex.: `[10, 12, 11, 9, 500, 13]`)
  tem exatamente esse ponto substituído por `None` na variante
  sem-outliers; os demais pontos idênticos.
- No relatório gerado: toggle de outliers em pelo menos 1 gráfico e 1
  mapa muda visualmente o que é plotado (não é um botão decorativo).
- Mapa: região filtrada como outlier mostra `fill` neutro na variante
  sem-outliers, sem desaparecer do SVG (geometria continua visível).

## V3 — Mapas SVG
- `carrega_geometria_svg('bairro')` retorna 166 entradas (mesma contagem
  do geojson fonte, `specification.md` §3.5); `'ap'` retorna 5; `'rp'`
  retorna 16.
- Pelo menos 1 bairro/AP com geometria de múltiplos anéis (ilha ou
  dissolução não-contígua) renderiza sem `path` quebrado/vazio.
- Nenhum mapa SVG final tem tile de basemap, overlay de UF, ou label de
  município vizinho (confirmado ausente — eram exclusivos do pipeline
  PNG, `specification.md` §3.5 item 6/§7).
- Hover num `<path>` de bairro/CAP mostra tooltip com nome + valor
  formatado pt-BR — testado em pelo menos 2 regiões por mapa amostrado.
- Preenchimento (`fill`) de cada `<path>` corresponde à paleta sequencial
  do tema certo (`_CORES_TEMA_MAPA` — natalidade=Teal/BuGn,
  mortalidade=RdPu/PuRd, cadunico=YlOrBr, censo=Blues), não a cor de um
  outro tema nem um `Oranges` default esquecido.

## V4 — Motor JS (controladores)
- `chartOptionSwitcher`: clicar em cada pill troca o gráfico/mapa exibido
  e marca a pill ativa (estado visual, não só o dado por trás).
- `sectionToggle`: recolher esconde o corpo da seção (`hidden`), expandir
  mostra de novo — testado nas 9 seções, não só na de exemplo do mockup.
- `outlierToggle` + `downloadCsv`: o CSV baixado depois de ativar o
  toggle de outliers reflete a série filtrada, não a bruta (ordem das
  ações importa — testar clicando outlier-toggle **antes** de baixar).
- `lineChart` com rótulo fixo: série onde o valor mais recente também é o
  mais alto mostra **1** rótulo, não 2 sobrepostos (§3.9, caso de
  coincidência).
- Tooltip com rótulo + valor confirmado em pelo menos 1 instância de
  cada: `lineChart`, `barChart`, `groupedBarChart`, mapa SVG — não só nos
  tipos que já tinham tooltip antes desta rodada.

## V5 — CSS institucional
- Nenhuma cor de fundo do corpo do relatório (fora do header/rodapé/chip
  do logo) mudou de valor em relação ao `relatorio/index.html` atual —
  diff de CSS confirma que só as regras novas (§5 do plan.md) foram
  adicionadas, nada existente foi sobrescrito.
- Eyebrow de toda seção **expandida** está em `--accent-ink`/peso 700;
  eyebrow de toda seção **recolhida** está no `.eyebrow` padrão — as duas
  cores nunca aparecem trocadas (expandida cinza, ou recolhida colorida).
- Barra de espectro (11 cores) aparece **exatamente 1 vez** na página
  (só no bloco de título) — busca por ela no restante do HTML retorna 0.
- Tema escuro (`prefers-color-scheme: dark`) testado: navy/cyan/barra de
  espectro/rodapé continuam legíveis (não é uma paleta pensada só para
  tema claro).

## V6 — Rodapé
- URLs de Transparência Rio, LGPD e e-mail de contato são as reais
  (confirmadas no Bloco 6, T6.2) — não os valores ilustrativos copiados
  do mockup/site institucional principal sem checar.
- Data de "atualizado em" bate com o timestamp real do build (gerar 2x
  em dias diferentes e confirmar que muda).
- Rodapé não contém endereço físico, telefone, nem ícones de redes
  sociais (escopo enxuto confirmado, §3.11/§4-M).
- Contraste de texto claro sobre `--ipp-navy` passa em WCAG AA para
  texto normal (4.5:1) — checar especificamente o tom mais dessaturado
  usado nos labels secundários (`#7FA9C6` no mockup).

## V7 — Navbar
- Os 9 links do hambúrguer levam às âncoras certas — clicar em cada um
  rola para o `h2` correspondente, sem link quebrado (`#` vazio ou
  `id` inexistente).
- Bloco "Sumário" antigo não existe mais na página final (substituído
  pela navbar, não duplicado).

## V8 — Geração e validação manual
- `build_html_report.py` roda do início ao fim sem exceção.
- Console do navegador (Chrome headless `--screenshot` ou interativo,
  conforme disponibilidade do ambiente — mesmo método de
  `SPEC-visual-identity/tasks.md` T6.6) sem erros/warnings novos.
- Largura ~375-420px: nenhum overflow horizontal da página inteira
  (scroll horizontal do `<body>`) — comportamento do seletor de
  pills/painel lateral pode não estar polido ainda (`specification.md`
  §8.2 deixa isso para depois), mas não pode quebrar o layout global.

## V9 — Deploy
- Workflow do GitHub Actions roda sem erro no `workflow_dispatch` manual.
- URL pública do GitHub Pages abre e mostra o relatório correto,
  idêntico ao gerado localmente (sem asset faltando — lembrar que o
  arquivo é autocontido, então "faltando" só aconteceria se o workflow
  publicasse o arquivo errado).
- V0 (gate de autorização do logo) confirmado **antes** deste bloco rodar
  — checar de novo aqui, não só em T0.4/T9.1.

## V10 — Documentação
- `relatorio/specs.md` tem uma entrada "v6" descrevendo esta rodada
  (mesmo padrão das entradas v1-v5.1 já existentes).
- `feature_roadmap.md` reflete o estado final: itens resolvidos
  removidos, deferidos mantidos.
- `tasks.md` só tem T10.5 (merge) em aberto ao final.
