# Tarefas — Mapas por bairro, IBGE SIDRA e mortalidade por subgrupo evitável

Ordem de execução. Cada bloco só começa depois do anterior passar na validação
correspondente (`validation.md`). Referências `plan.md §N` apontam para o design detalhado.

---

## Bloco 0 — Decisões

- [x] **T0.1** — Usuário revisou `specs.md` revisão 1 e respondeu as questões A-I
- [x] **T0.2** — Revisão 2 de `specs.md` incorpora as respostas; commitada (`0eb01ee`)
- [x] **T0.3** — Item H (mapas AP/RP para os novos indicadores) registrado em
      `feature_roadmap.md`, fora de escopo deste branch
- [x] **T0.4** — Confirmado pelo usuário: "Taxa de Óbitos evitável/não evitável" = soma
      evitável + não evitável (mortalidade infantil como um todo), já coberta pelas taxas
      existentes de `df_neonatal_*`/`df_mortalidade_infantil` — nenhum cruzamento novo por
      causa evitável a nível bairro é necessário. Bloco 3 desbloqueado.

---

## Bloco 1 — Correções pré-requisito (`plan.md` §2)

- [x] **T1.1** — Renomeado o segundo `.to_csv` do CadÚnico:
      `df_bairro_ate_4.to_csv('tabelas_finais/cadunico_por_bairro_ate_4_2026.csv')`
- [x] **T1.2** — `df_mortalidade_raca_bairro`: export em `tabelas_finais/mortalidade_raca_bairro_ano.csv`
- [x] **T1.3** — `df_neonatal_precoce`: export por bairro-ano em `tabelas_finais/`
- [x] **T1.4** — `df_neonatal_tardia`: idem
- [x] **T1.5** — `df_mortalidade_infantil`: idem
- [x] **T1.6** — `df_obitos_gravidez`: export por bairro-ano em `tabelas_finais/`
- [x] **T1.7** — `df_obitos_puerperio`: idem

→ **valida com V1**

---

## Bloco 2 — Componente A: funções auxiliares (`plan.md` §3.4-3.5)

- [x] **T2.1** — `junta_codbairro_por_bairro(df, df_referencia)` em
      **Limpeza e wrangling de dados** (`plan.md` §3.4) — também `carrega_sidra_longo`
      (Bloco 4) adicionada no mesmo local
- [x] **T2.2** — Aplicado: `df_bairro_mapa` (nova variável, sem a linha `'Total'`) para
      `df_bairro`; merge existente de `df_bairro_ate_4` com `df_censo` já traz `codbairro`
- [x] **T2.3** — Colunas `obitos_total`/`nascidos_total`/`percentual_total` em
      `df_mortalidade_raca_bairro` (`plan.md` §3.5)

→ **valida com V2.1-V2.2**

---

## Bloco 3 — Componente A: 11 indicadores (mapas por bairro)

⚠️ Só inicia após T0.4 confirmado. Ordem sugerida — do mais simples (sem taxa) ao mais
complexo (2 pares de mapas no mesmo dataset):

- [x] **T3.1** — `cadunico_criancas` (abs) — 1 mapa
- [x] **T3.2** — `cadunico_primeira_infancia` (abs + %) — 2 mapas
- [x] **T3.3** — `nascidos_vivos` (abs) — 1 mapa
- [x] **T3.4** — `nascidos_baixo_peso` (abs + %) — 2 mapas
- [x] **T3.5** — `obitos_raca_total` (abs + taxa) — 2 mapas
- [x] **T3.6** — `obitos_neonatal_precoce` (abs + taxa) — 2 mapas
- [x] **T3.7** — `obitos_neonatal_tardia` (abs + taxa) — 2 mapas
- [x] **T3.8** — `mortalidade_infantil` (abs + taxa, 0-364) — 2 mapas
- [x] **T3.9** — `mortalidade_pos_neonatal` (abs + taxa, 28-364, mesmo `df`) — 2 mapas
- [x] **T3.10** — `obitos_gravidez` (abs, nota de cautela sobre números pequenos) — 1 mapa
- [x] **T3.11** — `obitos_puerperio` (idem) — 1 mapa

Para cada um: `.describe()` da coluna absoluta → escolher `bins` → `tabela_mapa_*.csv` →
`mapa_coropletico_bairros(...)` (`plan.md` §3.1-3.3). **18 PNGs no total — todos gerados.**

Dois achados reais durante a implementação, não previstos no plano original:
- 4 dos 11 indicadores (`nascidos_vivos`, `nascidos_baixo_peso`, `obitos_gravidez`,
  `obitos_puerperio`, mais `obitos_neonatal_precoce`/`obitos_neonatal_tardia` mesmo após
  o merge com `df_vivos`) têm linhas `'EM BRANCO'` (bairro não identificado) que
  `limpeza_tabnet_bairros` deixa com `codigo`/`bairro` = NaN — `mapa_coropletico_bairros`
  falha ao converter NaN para inteiro. Corrigido com `.dropna(subset=['codigo'])` antes de
  cada mapa (não altera `limpeza_tabnet_bairros` em si, só o insumo do mapa).
- `mapa_coropletico_bairros` exige `bins[-1] < valor_maximo_real` (senão o último `limite`
  colide com `bins[-1]` e `pd.cut` rejeita bordas duplicadas) — `obitos_gravidez`/
  `obitos_puerperio` têm contagens tão baixas (max real 2 e 3) que os `bins` propostos em
  `plan.md` (`[1,2,3,5]`) estouravam essa regra; ajustados para `[0,1]`/`[0,1,2]`.

→ **valida com V2.3-V2.8** — notebook rodado do zero após cada correção, 0 erros em 125
células, 35 PNGs em `mapas/` (17 pré-existentes + 18 novos)

---

## Bloco 4 — Componente B: IBGE SIDRA (`plan.md` §4)

- [x] **T4.1** — `carrega_sidra_longo(caminho, coluna_corte)` em **Limpeza e wrangling de
      dados** (`plan.md` §4.1) — feito no Bloco 2
- [x] **T4.2** — Lidas as 6 tabelas com corte (raça/sexo); layout confere com o esperado
- [x] **T4.3** — 6 tabelas largas em `tabelas_finais/` (`plan.md` §4.2)
- [x] **T4.4** — 6 gráficos via `grafico_barra_agrupado` (`plan.md` §4.3) — inclui
      `sidra_frequencia_escola_0_5_sexo_2022.png`
- [x] **T4.5** — Seção nova no notebook: Censo SIDRA dentro de `🏘️ Censo 2022`; Educação
      SIDRA dentro de `🎓 PNAD Contínua, Censo Escolar e INEP` (`plan.md` §8)

Achado: os totais de `tabela9606` (coluna `Total`) têm uma diferença de até ~5 pessoas por
idade em relação à soma das 5 raças -- confirmado como rounding do próprio IBGE (disclosure
control), presente já no CSV bruto do SIDRA, não um bug de `carrega_sidra_longo` (`validation.md`
V3.2). Sexo bate exato.

→ **valida com V3** — notebook rodado do zero, 0 erros (133 células), 6 tabelas + 6 gráficos gerados

---

## Bloco 5 — Componente C: mapas de subgrupo (`plan.md` §5)

- [x] **T5.1** — Dict `subgrupos_componente_c` (gestação/parto → rótulo canônico)
- [x] **T5.2** — Filtrado `df_evitaveis_cap_faixa` (ano=2025, faixa=`menores de 1 ano`,
      2 subgrupos) → 2 `tabela_mapa_*.csv`
- [x] **T5.3** — `.describe()` conferido por subgrupo antes de fixar `bins` (gestação:
      3-47 por CAP, `bins=[10,20,30,40]`; parto: 1-10, `bins=[2,4,6,8]`)
- [x] **T5.4** — 2 mapas via `mapa_coropletico_bairros(nivel='cap')`

Achado: a coluna de subgrupo em `df_evitaveis_cap_faixa` é `'subgrupo'`, não `'causa'` como o
`plan.md` (revisões anteriores) escrevia — corrigido em código e em `plan.md` (`plan.md` §6.3).

→ **valida com V4** — notebook rodado do zero, 0 erros, 2 mapas gerados

---

## Bloco 6 — Componente D: séries de subgrupo (`plan.md` §6)

### 6.1 D.1 — Painel municipal, 3 faixas

- [x] **T6.1.1** — Loop para `< 1 ano` e `1-4 anos` (a de `< 5 anos` já existe, mantida)
- [x] **T6.1.2** — 2 gráficos novos (`obitos_evitaveis_menores_1_ano_subgrupo_ano.png`,
      `obitos_evitaveis_1_a_4_anos_subgrupo_ano.png`)

### 6.2 D.2a — Matriz completa (6 subgrupos × 3 faixas × CAP)

- [x] **T6.2.1** — Dict `_SLUG_SUBGRUPO_EVITAVEL` (`plan.md` §6.2)
- [x] **T6.2.2** — Loop aninhado (subgrupo × faixa) → 18 chamadas `serie_temporal_multipla`
- [x] **T6.2.3** — 18 arquivos conferidos em `visualizacoes/` (contagem exata)

### 6.3 D.2b — Recorte gestação/parto, `< 1 ano`

- [x] **T6.3.1** — 2 chamadas `serie_temporal_multipla` (reusa `subgrupos_componente_c` do
      Bloco 5), inseridas logo após os 2 mapas do Componente C

→ **valida com V5** — notebook rodado do zero, 0 erros (137 células), 22 gráficos novos
(2 + 18 + 2)

→ **valida com V5**

---

## Bloco 7 — Componente E: raça/cor sem `nao_informado`/1996 (`plan.md` §7)

- [x] **T7.1** — `rotulos_raca_evitaveis_sem_nao_informado` (dict, exclui `'Não informada'`)
- [x] **T7.2** — `df_evitaveis_raca_sem_1996` (filtro `ano > 1996`)
- [x] **T7.3** — Gráfico `obitos_causas_evitaveis_raca_sem_nao_informado_ano.png`
- [x] **T7.4** — Gráfico `percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano.png`
- [x] **T7.5** — Célula markdown substituindo o comentário-lembrete da linha 1167, explicando
      a diferença entre a versão original (mantida) e a nova

→ **valida com V6** — notebook rodado do zero, 0 erros (138 células), 2 gráficos novos,
originais mantidos intactos

→ **valida com V6**

---

## Bloco 8 — Documentação e fechamento

- [x] **T8.1** — README: nova entrada em `## Fontes de dados` (IBGE SIDRA)
- [x] **T8.2** — README: nova entrada em `## Fluxo de Análise (analise.py)` (Componentes A-E,
      passos 6b/6c/8b)
- [x] **T8.3** — README: bloco em `## Recent changes in analise.py`
- [x] **T8.4** — README: linha nova na `## Update Table` (0.15.0)
- [x] **T8.5** — `analise.ipynb` sincronizado via `jupytext --sync` a cada bloco (não só no
      fechamento)
- [x] **T8.6** — Notebook já rodado do zero, kernel limpo, ao final de cada bloco (5 execuções
      completas nesta sessão); `analise.py` não mudou desde a última (Bloco 7, 0 erros, 138
      células) — sem necessidade de rerun só para o README
- [x] **T8.7** — Amostra conferida visualmente: 1 mapa por bairro (`mapa_mortalidade_infantil_
      bairro_2025.png`), 1 mapa por CAP/subgrupo (`mapa_obitos_evitaveis_gestacao_menores_1_
      ano_cap_2025.png`), 1 gráfico SIDRA (`censo_sidra_populacao_0_6_raca_2022.png`) — todos
      corretos, convenções cartográficas/gráficas do projeto respeitadas
- [x] **T8.8** — Commits feitos incrementalmente por bloco na branch `spec/maps-and-ibge`
      (`9aac4af`, `18978de`, `178e349`, `75b205e`, + este de fechamento)
- [ ] **T8.9** — Merge em `staging_main` (só após aval do usuário)

→ **valida com V7, V8**

---

## Itens opcionais / segunda rodada

> Revisão: os dois itens de "mapas AP/RP" e "resolver T0.4 se a leitura estiver errada" saíram
> desta lista (o primeiro já vive só em `feature_roadmap.md`, o segundo ficou sem objeto após
> a confirmação em T0.4). O item de `sidra_frequencia_escola_0_5_sexo_2022` foi promovido para
> o Bloco 4 (T4.4) nesta primeira rodada.

- [ ] Atualizar `relatorio/*.html` e regerar o PDF (`skill export_pdf_report`) com os novos
      gráficos/mapas
