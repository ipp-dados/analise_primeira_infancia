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

- [ ] **T1.1** — Renomear o segundo `.to_csv` do CadÚnico:
      `df_bairro_ate_4.to_csv('tabelas_finais/cadunico_por_bairro_ate_4_2026.csv')`
- [ ] **T1.2** — `df_mortalidade_raca_bairro`: adicionar export em `tabelas_finais/mortalidade_raca_bairro_ano.csv`
- [ ] **T1.3** — `df_neonatal_precoce`: adicionar export por bairro-ano em `tabelas_finais/`
- [ ] **T1.4** — `df_neonatal_tardia`: idem
- [ ] **T1.5** — `df_mortalidade_infantil`: idem
- [ ] **T1.6** — `df_obitos_gravidez`: adicionar export por bairro-ano em `tabelas_finais/`
- [ ] **T1.7** — `df_obitos_puerperio`: idem

→ **valida com V1**

---

## Bloco 2 — Componente A: funções auxiliares (`plan.md` §3.4-3.5)

- [ ] **T2.1** — `junta_codbairro_por_bairro(df, df_referencia)` em
      **Limpeza e wrangling de dados** (`plan.md` §3.4)
- [ ] **T2.2** — Aplicar em `df_bairro` (reset do índice primeiro) e garantir que o merge
      existente de `df_bairro_ate_4` com `df_censo` (linha ~905) já traz `codbairro`
- [ ] **T2.3** — Colunas `obitos_total`/`nascidos_total`/`percentual_total` em
      `df_mortalidade_raca_bairro` (`plan.md` §3.5)

→ **valida com V2.1-V2.2**

---

## Bloco 3 — Componente A: 11 indicadores (mapas por bairro)

⚠️ Só inicia após T0.4 confirmado. Ordem sugerida — do mais simples (sem taxa) ao mais
complexo (2 pares de mapas no mesmo dataset):

- [ ] **T3.1** — `cadunico_criancas` (abs) — 1 mapa
- [ ] **T3.2** — `cadunico_primeira_infancia` (abs + %) — 2 mapas
- [ ] **T3.3** — `nascidos_vivos` (abs) — 1 mapa
- [ ] **T3.4** — `nascidos_baixo_peso` (abs + %) — 2 mapas
- [ ] **T3.5** — `obitos_raca_total` (abs + taxa) — 2 mapas
- [ ] **T3.6** — `obitos_neonatal_precoce` (abs + taxa) — 2 mapas
- [ ] **T3.7** — `obitos_neonatal_tardia` (abs + taxa) — 2 mapas
- [ ] **T3.8** — `mortalidade_infantil` (abs + taxa, 0-364) — 2 mapas
- [ ] **T3.9** — `mortalidade_pos_neonatal` (abs + taxa, 28-364, mesmo `df`) — 2 mapas
- [ ] **T3.10** — `obitos_gravidez` (abs, nota de cautela sobre números pequenos) — 1 mapa
- [ ] **T3.11** — `obitos_puerperio` (idem) — 1 mapa

Para cada um: `.describe()` da coluna absoluta → escolher `bins` → `tabela_mapa_*.csv` →
`mapa_coropletico_bairros(...)` (`plan.md` §3.1-3.3). **18 PNGs no total.**

→ **valida com V2.3-V2.8** (rodar após cada 2-3 itens, não só no final — `plan.md` §9)

---

## Bloco 4 — Componente B: IBGE SIDRA (`plan.md` §4)

- [ ] **T4.1** — `carrega_sidra_longo(caminho, coluna_corte)` em **Limpeza e wrangling de
      dados** (`plan.md` §4.1)
- [ ] **T4.2** — Ler as 6 tabelas com corte (raça/sexo) das 9 disponíveis; conferir
      shape/colunas contra o esperado antes de generalizar (V3.1)
- [ ] **T4.3** — 6 tabelas largas em `tabelas_finais/` (`plan.md` §4.2)
- [ ] **T4.4** — 5 gráficos via `grafico_barra_agrupado` (`plan.md` §4.3)
- [ ] **T4.5** — Seção nova no notebook: Censo SIDRA dentro de `🏘️ Censo 2022`; Educação
      SIDRA dentro de `🎓 PNAD Contínua, Censo Escolar e INEP` (`plan.md` §8)

→ **valida com V3**

---

## Bloco 5 — Componente C: mapas de subgrupo (`plan.md` §5)

- [ ] **T5.1** — Dict `subgrupos_componente_c` (gestação/parto → rótulo canônico)
- [ ] **T5.2** — Filtrar `df_evitaveis_cap_faixa` (ano=2025, faixa=`menores de 1 ano`,
      2 subgrupos) → 2 `tabela_mapa_*.csv`
- [ ] **T5.3** — Imprimir `.describe()` por subgrupo **antes** de fixar `bins`
- [ ] **T5.4** — 2 mapas via `mapa_coropletico_bairros(nivel='cap')`

→ **valida com V4**

---

## Bloco 6 — Componente D: séries de subgrupo (`plan.md` §6)

### 6.1 D.1 — Painel municipal, 3 faixas

- [ ] **T6.1.1** — Loop para `< 1 ano` e `1-4 anos` (a de `< 5 anos` já existe, mantida)
- [ ] **T6.1.2** — 2 gráficos novos (`obitos_evitaveis_menores_1_ano_subgrupo_ano.png`,
      `obitos_evitaveis_1_a_4_anos_subgrupo_ano.png`)

### 6.2 D.2a — Matriz completa (6 subgrupos × 3 faixas × CAP)

- [ ] **T6.2.1** — Dict `_SLUG_SUBGRUPO_EVITAVEL` (`plan.md` §6.2)
- [ ] **T6.2.2** — Loop aninhado (subgrupo × faixa) → 18 chamadas `serie_temporal_multipla`
- [ ] **T6.2.3** — Conferir 2-3 amostras contra `df_evitaveis_cap_faixa` filtrado à mão
      (`plan.md` §9)

### 6.3 D.2b — Recorte gestação/parto, `< 1 ano`

- [ ] **T6.3.1** — 2 chamadas `serie_temporal_multipla` (reusa `subgrupos_componente_c` do
      Bloco 5), inseridas logo após os 2 mapas do Componente C

→ **valida com V5**

---

## Bloco 7 — Componente E: raça/cor sem `nao_informado`/1996 (`plan.md` §7)

- [ ] **T7.1** — `rotulos_raca_evitaveis_sem_nao_informado` (dict, exclui `'Não informada'`)
- [ ] **T7.2** — `df_evitaveis_raca_sem_1996` (filtro `ano > 1996`)
- [ ] **T7.3** — Gráfico `obitos_causas_evitaveis_raca_sem_nao_informado_ano.png`
- [ ] **T7.4** — Gráfico `percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano.png`
- [ ] **T7.5** — Célula markdown substituindo o comentário-lembrete da linha 1167, explicando
      a diferença entre a versão original (mantida) e a nova

→ **valida com V6**

---

## Bloco 8 — Documentação e fechamento

- [ ] **T8.1** — README: nova entrada em `## Fontes de dados` (IBGE SIDRA)
- [ ] **T8.2** — README: nova entrada em `## Fluxo de Análise (analise.py)` (Componentes A-E)
- [ ] **T8.3** — README: bloco em `## Recent changes in analise.py`
- [ ] **T8.4** — README: linha nova na `## Update Table`
- [ ] **T8.5** — Sincronizar `analise.ipynb` via `jupytext --sync analise.py`
- [ ] **T8.6** — Rodar `jupyter nbconvert --execute` de ponta a ponta, kernel limpo — 0 erros
      (mesmo processo já usado no início desta sessão)
- [ ] **T8.7** — Conferir visualmente uma amostra dos ~35 PNGs novos (todos os mapas + pelo
      menos 1 de cada tipo de série temporal)
- [ ] **T8.8** — Commit(s) na branch `spec/maps-and-ibge`
- [ ] **T8.9** — Merge em `staging_main` (só após aval do usuário)

→ **valida com V7, V8**

---

## Itens opcionais / segunda rodada

- [ ] Mapas AP/RP para os 11 indicadores do Componente A (registrado em `feature_roadmap.md`)
- [ ] Resolver definitivamente o item T0.4 se a leitura assumida estiver errada — buscar fonte
      de causas evitáveis por bairro (se existir no Tabnet) e refazer o Componente A com o
      cruzamento evitável/não evitável de verdade
- [ ] Atualizar `relatorio/*.html` e regerar o PDF (`skill export_pdf_report`) com os novos
      gráficos/mapas
- [ ] `sidra_frequencia_escola_0_5_sexo_2022` como gráfico próprio (hoje só tabela, `plan.md` §4.3)
