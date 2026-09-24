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
| 2007-2019 | | | | | a preencher no Bloco 1 (P6) |
| 2020 | 107.422 | 139.711 | 247.133 | 143.909 | ✅ abertura |
| 2021 | 101.421 | 128.839 | 230.260 | 140.722 | ✅ abertura |
| 2022 | 114.822 | 131.700 | 246.522 | 136.691 | ✅ abertura |
| 2023 | 113.935 | 132.184 | 246.119 | 131.935 | ✅ abertura |
| 2024 | 114.934 | 127.641 | 242.575 | 127.851 | ✅ abertura |
| 2025 | 110.097 | 120.187 | 230.284 | 122.236 | ✅ abertura |

- [ ] 2007-2019 com as colunas de faixa etária (P6).
- [ ] Extrato versionado reproduz a tabela acima (soma sobre as dependências).
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

- [ ] Extrato de população reproduz as linhas acima (e as demais da consulta).
- [ ] `taxa_atendimento_0_a_5 == (matriculas_0_a_3 + matriculas_4_a_5) / (populacao_0_a_3 + populacao_4_a_5)`, e não a média das duas taxas.
- [ ] Nota do notebook traz a comparação com o Censo 2022 (0-5: 379.609 pessoas, taxa 64,9%).

## V3: Saídas

- [ ] `tabelas_finais/matriculas_0_a_5_por_ano.csv`: 19 linhas (2007-2025), `matriculas == matriculas_0_a_3 + matriculas_4_a_5 == matriculas_publica + matriculas_privada`.
- [ ] Os 4 PNG existem e citam a fonte no rodapé (o da taxa cita INEP e Ripsa).
- [ ] Se D8 = (b): gráficos existentes que usam `serie_temporal_multipla` saem idênticos visualmente (sem `linhas_referencia`).
- [ ] Nenhuma referência restante a `matriculas_0_a_6` (`grep -rn` no repo, fora de `specs/` e do histórico).

## V4: Reprodutibilidade

- [ ] Notebook do zero (kernel limpo, `analises_env`, cwd na raiz) roda sem erro, lendo só os extratos (sem rede).
- [ ] Com o extrato de matrículas removido temporariamente, a função reconstrói um extrato idêntico a partir do cache.
- [ ] Com o extrato de população removido temporariamente, a consulta ao Tabnet reconstrói os mesmos valores.
- [ ] `git status` limpo de ZIPs (cache ignorado).

## V5: Relatórios

- [ ] HTML: card de matrículas com 0-5 e os cards novos (creche/pré, rede, taxa); sem "0 a 6"; tamanho e contagem de cards comparados com o baseline.
- [ ] PDF e DOCX regenerados, com a seção de matrículas e a taxa.
