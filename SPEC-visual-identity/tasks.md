# Tasks — SPEC-visual-identity

## Bloco 0 — Decisões
- [x] **T0.1** — Especificação e decisões A-F aprovadas pelo usuário (`specs.md` §4).
- [x] **T0.2** — Branch `spec/visual-identity` criada a partir de `spec/maps-and-ibge`.

## Bloco 1 — Módulo de estilo compartilhado (`analise.py`)
- [ ] **T1.1** — Adicionar `_PALETA_CATEGORICA`, `_CORES_TEMA_MAPA`,
      `_LIMIAR_DESTAQUE_SERIES`, `_N_SERIES_DESTACADAS`, `_COR_SERIE_APAGADA`,
      `_COR_FONTE_RODAPE`, `_rodape_fonte()` (plan.md §1).
- [ ] **T1.2** — Atualizar `serie_temporal` (fonte_dados, título serifado, DPI 200).
- [ ] **T1.3** — Atualizar `grafico_barra` (paleta do projeto no lugar de `'pastel'`, fonte_dados).
- [ ] **T1.4** — Atualizar `grafico_barra_agrupado` (paleta, fonte_dados).
- [ ] **T1.5** — Atualizar `serie_temporal_multipla` (paleta fixa por posição, lógica de
      destaque acima de 6 séries, `destaques=` opcional, fonte_dados).
- [ ] **T1.6** — Rodar as 4 funções isoladas (fora do notebook completo) num teste rápido
      com dado sintético para confirmar que não quebram antes de tocar os ~73 call sites.

## Bloco 2 — Mapas: `cmap` por tema (25 call sites)
- [ ] **T2.1** — Tema `censo` → `cmap=_CORES_TEMA_MAPA['censo']`: linhas 758, 768, 799, 807.
- [ ] **T2.2** — Tema `cadunico`: linhas 1013, 1033, 1038.
- [ ] **T2.3** — Tema `natalidade`: linhas 1075, 1116, 1121.
- [ ] **T2.4** — Tema `mortalidade`: linhas 1277, 1282, 1852, 1861, 1895, 1959, 1992, 2035,
      2040, 2075, 2080, 2144, 2149, 2166, 2171.
- [ ] **T2.5** — Regenerar os 25 mapas (rodar as células) e checar visualmente contraste da
      classe mais clara de cada rampa (`BuGn`/`RdPu`/`YlOrBr`/`Blues`) sobre o basemap —
      ajustar opacidade/alpha só se algum ficar ilegível.

## Bloco 3 — `fonte_dados` + paleta nos ~48 call sites restantes
Percorrer `analise.py` seção por seção (mesma ordem do notebook), adicionando
`fonte_dados=fonte_<seção>` a cada chamada. Criar uma nova constante `fonte_*`
para seções que ainda não têm uma (SISVAN, PNAD/matrículas, SIDRA educação).
- [ ] **T3.1** — Censo: `grafico_barra_agrupado` (719, 728) → `fonte_censo` (já existe,
      confirmar se cobre também os 2 gráficos SIDRA Censo do Componente B ou se precisam de
      `fonte_sidra_censo` própria).
- [ ] **T3.2** — CadÚnico: `grafico_barra` (914, 919, 935, 939) → `fonte_cadunico`.
- [ ] **T3.3** — Nascidos vivos / baixo peso: `serie_temporal` (1090, 1135) → `fonte_datasus_bairro`.
- [ ] **T3.4** — Óbitos por raça / evitáveis (0-364, subgrupo, grupo etário): `serie_temporal_multipla`
      (1248, 1261, 1344, 1366, 1379, 1392, 1438, 1450, 1485, 1497, 1526, 1538, 1567, 1579,
      1657, 1695, 1751, 1763, 1779, 1815, 1916) e `grafico_barra_agrupado` (1614) →
      `fonte_datasus_bairro` ou `fonte_evitaveis_cap`, conforme a tabela de origem de cada uma
      (checar `df_evitaveis_*` vs `df_mortalidade_raca_bairro` linha a linha).
- [ ] **T3.5** — Gravidez/puerpério/neonatal: `serie_temporal` (1669, 1945, 1979, 2025, 2065,
      2134, 2159) → `fonte_datasus_bairro`/`fonte_evitaveis_cap`.
- [ ] **T3.6** — SISVAN (desnutrição/sobrepeso/obesidade): `serie_temporal` (2192, 2204, 2208)
      → nova `fonte_sisvan` (checar se já existe uma constante equivalente antes de criar).
- [ ] **T3.7** — PNAD/matrículas: `serie_temporal` (2361), `grafico_barra` (2347),
      `grafico_barra_agrupado` (2253, 2299, 2308, 2317, 2326) → `fonte_pnad`/`fonte_matriculas`/
      `fonte_sidra_educacao` conforme a seção.
- [ ] **T3.8** — `serie_temporal_multipla` (2229) → conferir seção e fonte.
- [ ] **T3.9** — Conferir que todo call site das 4 funções (73 no total, mapas incluídos) tem
      `fonte_dados` — `grep -c "fonte_dados=" analise.py` deve bater com a contagem de chamadas.

## Bloco 4 — Destaque de séries com muitas linhas
- [ ] **T4.1** — Identificar todas as `serie_temporal_multipla` com >6 colunas (candidatos
      conhecidos: cobertura vacinal EPI comparativo, as ~18 séries de evitáveis por
      subgrupo×CAP do `SPEC-maps-and-ibge`).
- [ ] **T4.2** — Para cada uma, decidir se o "top 4 pelo valor final" automático faz sentido
      ou se precisa de `destaques=[...]` manual (ex.: cobertura vacinal pode preferir vacinas
      específicas) — registrar a decisão como comentário no call site.
- [ ] **T4.3** — Regenerar e inspecionar visualmente cada gráfico afetado.

## Bloco 5 — Validação completa do notebook
- [ ] **T5.1** — `jupytext --sync` (ou execução direta) para refletir as mudanças de
      `analise.py` no `.ipynb`.
- [ ] **T5.2** — `jupyter nbconvert --to notebook --execute --inplace` a partir de kernel limpo — 0 erros.
- [ ] **T5.3** — Checar `nbformat` por células com `output_type == 'error'` (script já usado nas rodadas anteriores).
- [ ] **T5.4** — Spot-check visual: 1 mapa por tema (4), 1 `serie_temporal_multipla` com
      destaque (1), 1 gráfico de barra simples e 1 agrupado — abrir os PNGs e conferir título
      serifado, rodapé de fonte, paleta correta.

## Bloco 6 — `relatorio/` HTML (consolidação)
- [ ] **T6.1** — Extrair o motor JS (`lineChart`/`barChart`/`groupedBarChart`) e o esqueleto
      de tema claro/escuro de `lighter_index.html`/`white_index.html` para um template
      reaproveitável pelo novo script de build.
- [ ] **T6.2** — Escrever `.claude/skills/export_pdf_report/scripts/build_html_report.py`
      (plan.md §4.2): lê `tabelas_finais/*.csv`, monta o JSON por seção, renderiza 1
      `relatorio/index.html`.
- [ ] **T6.3** — Portar a lógica de destaque de séries (Bloco 4) para o `lineChart` do motor JS.
- [ ] **T6.4** — Adicionar seção "🗺️ Mapas" cobrindo os 25 mapas atuais (WebP ~1400px,
      mesma técnica já usada), agrupados por tema (natalidade/mortalidade/cadunico/censo).
- [ ] **T6.5** — Cada visualização com só título + fonte + alternância "ver tabela" — sem
      prosa/notas de método.
- [ ] **T6.6** — Rodar o script, gerar `relatorio/index.html`, abrir no navegador e conferir:
      tema claro/escuro automático, todas as ~35 visualizações novas presentes, tabela de
      dados funcionando em pelo menos 1 gráfico de cada tipo (linha simples, linha múltipla,
      barra, barra agrupada, mapa).
- [ ] **T6.7** — Remover `relatorio/lighter_index.html` e `relatorio/white_index.html` (arquivos
      antigos, substituídos pelo novo `index.html` consolidado) — local only, já fora do git.

## Bloco 7 — PDF
- [ ] **T7.1** — Rodar `regen_missing_pngs.py`, atualizar se necessário para as funções/
      esquemas de CSV que mudaram no Bloco 1-3.
- [ ] **T7.2** — Atualizar `extract_maps.py` para ler do novo `relatorio/index.html` único.
- [ ] **T7.3** — Atualizar `build_notebook_report.py` com as seções novas de `SPEC-maps-and-ibge`.
- [ ] **T7.4** — Rodar o pipeline completo até o Chrome headless (flags de segurança do
      `--user-data-dir` isolado, `--no-pdf-header-footer`).
- [ ] **T7.5** — Verificar contagem de páginas + rasterizar amostra (primeira, várias do meio,
      seção de mapas, última) e olhar as imagens.
- [ ] **T7.6** — Checar os modos de falha conhecidos da skill (ano com separador de milhar,
      tabela larga cortada, coluna de percentual na escala errada, header/footer do Chrome
      vazando, tema escuro vazando).
- [ ] **T7.7** — Copiar o PDF verificado para `relatorio/analise_primeira_infancia.pdf`.

## Bloco 8 — Documentação e fechamento
- [ ] **T8.1** — Atualizar `relatorio/specs.md` com a v5 (consolidação, script de build
      persistido, remoção da prosa) — seguindo o histórico "v1/v2/v3/v4" já documentado ali.
- [ ] **T8.2** — Atualizar `README.md` (changelog, versão).
- [ ] **T8.3** — Atualizar `feature_roadmap.md` se algo ficar de fora nesta rodada.
- [ ] **T8.4** — Fechar `tasks.md`/`validation.md`.
- [ ] **T8.5** — **Merge em `staging_main` (só após aval do usuário)** — nota: este merge e o
      de `spec/maps-and-ibge` (ainda pendente) precisam ser sequenciados; decidir com o
      usuário a ordem antes de mesclar qualquer um dos dois.
