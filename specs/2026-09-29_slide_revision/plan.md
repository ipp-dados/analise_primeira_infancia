# PLAN — Revisão do deck (30 → 33 slides)

Branch de implementação: `spec/slide-revision` (a partir de `planning`), merge em `planning` e depois `staging_main`.
Decisões D1-D8 e a estrutura nova em `specification.md`.

## Blocos

### B1 — Estrutura e texto (`apresentacao/apresentacao.md`)
Reordenar os slides pela tabela do §4 da especificação (mover blocos inteiros entre `---`, com notas do apresentador
e `<!-- revisar -->`), remover S06, criar 21, 26, 29 e 30, e aplicar R1-R8. Cabeçalho: `subtitulo` e `contato` novos.
O bloco `<!-- se: cooperacao -->` passa a envolver só o novo slide 06. Os slides novos 29-30 levam `<!-- revisar -->`
(texto proposto pelo IPP a partir do pedido). Por último, alinhar `variantes/exemplo_secretaria.md` à mesma estrutura.

### B2 — Números (`apresentacao/build/numeros.py`)
- `pct_cadunico_extrema_pobreza` → `pct_cadunico_pobreza`; `pct_uma_adulta_extrema_pobreza` → `pct_uma_adulta_pobreza`
  (hoje filtra `startswith("Extrema")`; passa a filtrar pela chave da faixa `0-218`, não pelo rótulo).
- Novos: `censo_0_5_2022_mil` (SIDRA 9606, linha "Total 0 a 5 anos"), `vf_notif_total_2025` e `vf_taxa_total_2025`
  (mãe + pai + outros somados antes de dividir pela população — constituição §3), `vf_notif_bairros_2025` se o slide 26 citar.
- `pop_0_6_ripsa_mil` deixa de ser usado pelo deck (fica disponível).

### B3 — Mapas do deck (`apresentacao/build/mapas_apresentacao.py`)
Estender `MAPAS` com parâmetros opcionais: `cmap` (sobrepõe o tema), `bins` (contagens em classes discretas),
`outlier` (liga o teto de Tukey; hoje sempre ligado). Rampa terracota definida uma vez no módulo
(`LinearSegmentedColormap`, creme → terracota, ~#f6efe6 → #a4452c), sem tocar em `primeira_infancia/estilo.py` (D1).
Mapas novos (todos `apres_*`, em `apresentacao/_build/mapas/`):
| chave | tabela | trato |
|---|---|---|
| `apres_censo_0_4_absoluto` | `tabela_mapa_censo_*` (contagem) | terracota, `bins` |
| `apres_censo_0_4_percentual` | idem (%) | terracota, contínuo |
| `apres_taxa_mortalidade_infantil_bairro_2025` | tabela do `mapa_taxa_obitos_raca_total_bairro_2025` | tema, Tukey |
| `apres_baixo_peso_bairro_2025` | tabela do `mapa_percentual_baixo_peso_bairro_2025` | tema, Tukey |
| `apres_violencia_familiar_total_bairro_2025` | `violencia_familiar_por_bairro.csv`, ano 2025, mãe + pai + outros | `OrRd`, `bins` |
Conferir os demais `fig:mapa_*` do deck (CAP evitáveis `RdPu`, RA violência `OrRd`, nascidos/baixo peso `BuGn`,
CadÚnico `YlOrBr`): nenhum azul puro; `BuGn` termina em verde-azulado, que o pedido admite ("teal accents") — registrar
em `validation.md` e trocar se a revisão visual achar azul.

### B4 — Gráfico do deck (novo `apresentacao/build/graficos_apresentacao.py`)
Mesmo padrão de `mapas_apresentacao.py`: `GRAFICOS = {"apres_violencia_familiar_total_ano": ...}` gerado com
`serie_temporal_multipla`/versão A4 do pacote em `_build/graficos/`, linha "Total (mãe + pai + outros)" em destaque e
os três vínculos em linhas finas; base zero (P1). `gera_apresentacao.figura()` resolve `apres_*` nos dois módulos.

### B5 — Tema (`apresentacao/tema/ipp.css`)
- `.stats .destaque` (caixa central do slide 09: borda/fundo mais fortes, número maior).
- `.grupo` com título ("Governança de Dados") envolvendo as 3 caixas do slide 06.
- `.nota.forte` (callout da família monoparental, slide 24).

### B6 — Rótulo de renda no projeto (D1)
`primeira_infancia/cadunico.py` (`_ROTULOS_RENDA_CADUNICO` e o comentário da linha de R$ 218), texto curado de
`analise.py` (l. ~504) e `relatorio/textos_curados.json`, rodar a seção CadÚnico do `analise.py` (conda
`analises_env` + `.env`) para regravar as tabelas/figuras, reconstruir site (skill `build_website`) e PDF
(skill `export_pdf_report`, sem `--publicar`). Sem acesso ao banco: renomear os rótulos nas tabelas já gravadas
não é aceito — registrar como pendente e seguir com o deck.

### B7 — Gerar, conferir, documentar
`gera_apresentacao.py --png`, revisão slide a slide (V1-V10), `apresentacao/README.md` (33 slides),
`docs/especificacao_projeto.md`, ROADMAP (item "72 meses + paleta sem azul no site/PDF"), CHANGELOG.
`--publicar` só com o OK do usuário.

## Riscos
- Slide 02 com 4 bullets e slide 09 com 3 caixas podem estourar a altura: ajustar fonte só no slide (`style`).
- `outros` por bairro em um único ano tem contagens muito pequenas; é SINAN (fora da regra de < 20 do CadÚnico), mas
  a soma no mapa reduz o problema — nota de rodapé "notificação não é caso confirmado".
- O PNG do pedido pode ter sido revisado numa versão antiga (o deck já usa 393 mil e o gráfico de raça já é 0-5):
  checar cada item contra o deck atual, não contra o pedido.
