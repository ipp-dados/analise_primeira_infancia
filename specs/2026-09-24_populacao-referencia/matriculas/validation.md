# Validação: specs/matriculas-censo-escolar

Marcar `[x]` com a evidência (comando, número). Os números de referência foram **lidos dos ZIPs do INEP e
consultados no Tabnet** na abertura da rodada, em 2026-09-24 (spec §3.3, §3.5 e §3.6). O código deve
reproduzi-los exatamente. Para a população, vale "exatamente" enquanto a Ripsa não revisar as estimativas
(P7).

## V0: Fontes

- [x] URLs 2007-2024 no padrão `microdados_censo_escolar_<ANO>.zip`; 2025 em `…_2025_.zip`. *(HTTP 200, 2026-09-24)*
- [x] 2020-2024: contagens em `microdados_ed_basica_<ANO>.csv` (2020 com `.CSV`); 2025 em `Tabela_Matricula_2025_V2.csv`. Todos com `sep=';'` e latin-1.
- [x] Idade na última quarta-feira de maio (dicionário de 2025, `QT_MAT_BAS_0_3`/`_4_5`).
- [x] Escolas não ativas (`TP_SITUACAO_FUNCIONAMENTO` 2/3) sem matrícula de 0-5 (2020: 331 escolas, soma 0).
- [x] Tabnet `popsvs2024br.def` (Ripsa 2000-2025) responde ao POST automatizado, com 19 anos × 7 idades para o Rio (`SMunicípio=3262`). *(2026-09-24)*

## V1: Matrículas de referência, Rio de Janeiro, 0-5 (data padrão)

| Ano | 0-3 | 4-5 | 0-5 | pública 0-5 | Status |
|---|---|---|---|---|---|
| 2007 | 60.997 | 109.653 | 170.650 | 107.599 | ✅ Bloco 1 (2026-09-24) |
| 2008 | 74.455 | 122.449 | 196.904 | 104.919 | ✅ Bloco 1 (2026-09-24) |
| 2009 | 72.318 | 120.806 | 193.124 | 104.076 | ✅ Bloco 1 (2026-09-24) |
| 2010 | 80.325 | 122.525 | 202.850 | 105.600 | ✅ Bloco 1 (2026-09-24) |
| 2011 | 95.636 | 126.796 | 222.432 | 116.243 | ✅ Bloco 1 (2026-09-24) |
| 2012 | 100.517 | 128.006 | 228.523 | 120.029 | ✅ Bloco 1 (2026-09-24) |
| 2013 | 108.859 | 132.871 | 241.730 | 125.616 | ✅ Bloco 1 (2026-09-24) |
| 2014 | 111.591 | 135.689 | 247.280 | 127.060 | ✅ Bloco 1 (2026-09-24) |
| 2015 | 109.873 | 133.303 | 243.176 | 127.291 | ✅ Bloco 1 (2026-09-24) |
| 2016 | 110.358 | 136.664 | 247.022 | 130.762 | ✅ Bloco 1 (2026-09-24) |
| 2017 | 114.609 | 139.032 | 253.641 | 139.031 | ✅ Bloco 1 (2026-09-24) |
| 2018 | 113.789 | 139.729 | 253.518 | 139.935 | ✅ Bloco 1 (2026-09-24) |
| 2019 | 115.723 | 143.145 | 258.868 | 144.314 | ✅ Bloco 1 (2026-09-24) |
| 2020 | 107.422 | 139.711 | 247.133 | 143.909 | ✅ abertura |
| 2021 | 101.421 | 128.839 | 230.260 | 140.722 | ✅ abertura |
| 2022 | 114.822 | 131.700 | 246.522 | 136.691 | ✅ abertura |
| 2023 | 113.935 | 132.184 | 246.119 | 131.935 | ✅ abertura |
| 2024 | 114.934 | 127.641 | 242.575 | 127.851 | ✅ abertura |
| 2025 | 110.097 | 120.187 | 230.284 | 122.236 | ✅ abertura |

- [x] 2007-2019 com as colunas de faixa etária (P6): todos os 19 anos têm `QT_MAT_BAS_0_3/_4_5`, `QT_MAT_INF*` e `TP_DEPENDENCIA`; 2007-2024 em `microdados_ed_basica_<ano>.csv` (2020 `.CSV`), 2025 em `Tabela_Matricula_2025_V2.csv`. *(2026-09-24)*
- [x] Extrato versionado (`inep_matriculas_rio.csv`, 76 linhas) reproduz a tabela acima (soma sobre as dependências); assert de 2020 e 2025 no notebook.
- [ ] Validação externa (P5): 1 ou 2 anos batem com a Sinopse Estatística do INEP (educação infantil por município ou 0-5, se houver).

## V2: População e taxa de referência (Ripsa, consulta de 2026-09-24)

População por idade simples (menos de 1, 1, …, 6 anos), Rio de Janeiro:

| Ano | <1 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 2007 | 79.055 | 80.104 | 81.297 | 82.701 | 84.928 | 88.089 | 91.990 |
| 2010 | 79.749 | 79.756 | 79.779 | 80.190 | 81.162 | 82.034 | 83.018 |
| 2015 | 85.890 | 83.539 | 81.781 | 81.336 | 79.975 | 79.160 | 79.472 |
| 2020 | 72.144 | 76.403 | 79.235 | 79.224 | 82.262 | 85.054 | 82.563 |
| 2022 | 64.701 | 68.604 | 72.424 | 76.444 | 78.990 | 78.744 | 81.625 |
| 2025 | 61.200 | 62.082 | 63.219 | 65.435 | 68.855 | 72.282 | 76.075 |

Taxas de referência 2020-2025: spec §3.6 (ex.: 2025 → 0-3 43,7%, 4-5 85,2%, 0-5 58,6%).

- [x] Extrato de população reproduz as linhas acima (e as demais da consulta).
- [x] `taxa_atendimento_0_a_5 == (matriculas_0_a_3 + matriculas_4_a_5) / (populacao_0_a_3 + populacao_4_a_5)`, e não a média das duas taxas (`resume_matriculas_0_a_5`; 2020-2025 batem com spec §3.6).
- [x] Nota metodológica de D7 presente, com os 6 pontos da spec §5 (inclui Censo 2022: 379.609 pessoas de 0-5, taxa 64,9%).

## V3: Saídas

- [x] `tabelas_finais/matriculas_0_a_5_por_ano.csv`: 19 linhas (2007-2025), `matriculas == matriculas_0_a_3 + matriculas_4_a_5 == matriculas_publica + matriculas_privada` (asserts no notebook).
- [x] Os 4 PNG existem e citam a fonte no rodapé (o da taxa cita INEP e Ripsa).
- [ ] D8: gráficos existentes que usam `serie_temporal_multipla` e `line_chart` saem idênticos visualmente (sem `linhas_referencia`); o da taxa mostra 50% e 100% tracejados.
- [x] Nenhuma referência restante a `matriculas_0_a_6` em código (`grep` em `*.py`, fora de `specs/`).

## V4: Reprodutibilidade

- [ ] Notebook do zero (kernel limpo, `analises_env`, cwd na raiz) roda sem erro, lendo só os extratos (sem rede).
- [x] Com o extrato de matrículas removido, a função reconstruiu o extrato a partir do cache (mesmos valores; a 1ª versão tinha contagens em float, corrigido para int). *(2026-09-24)*
- [ ] Com o extrato de população removido temporariamente, a consulta ao Tabnet reconstrói os mesmos valores.
- [x] `git status` limpo de ZIPs (cache ignorado; regra do `.gitignore` corrigida no Bloco 1 de `populacao-referencia`).

## V5: Relatórios

- [x] HTML: card de matrículas com 0-5 (total, creche/pré, rede) e card da taxa com as metas do PNE; selo "dado desatualizado" removido; option cards 40 → 44 (inclui os cards novos da Parte A e D).
- [x] PDF e DOCX regenerados, com a seção de matrículas e a taxa (PDF p. 74-76).
