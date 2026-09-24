# Validação: specs/matriculas-censo-escolar

Marcar `[x]` com a evidência (comando, número). Os números de referência foram **lidos dos ZIPs do INEP**
na abertura da rodada, em 2026-09-24 (spec §3.3 e §3.5). O código deve reproduzi-los exatamente.

## V0: Fonte
- [x] URLs 2007-2024 no padrão `microdados_censo_escolar_<ANO>.zip`; 2025 em `…_2025_.zip`. *(HTTP 200, 2026-09-24)*
- [x] 2020-2024: contagens em `microdados_ed_basica_<ANO>.csv` (2020 com `.CSV`); 2025 em `Tabela_Matricula_2025_V2.csv`. Todos com `sep=';'` e latin-1.
- [x] Idade na última quarta-feira de maio (dicionário de 2025, `QT_MAT_BAS_0_3`/`_4_5`).
- [x] Escolas não ativas (`TP_SITUACAO_FUNCIONAMENTO` 2/3) sem matrícula de 0-5 (2020: 331 escolas, soma 0).

## V1: Totais de referência, Rio de Janeiro, 0-5 (data padrão)

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

## V2: Saídas
- [ ] `tabelas_finais/matriculas_0_a_5_por_ano.csv`: 19 linhas (2007-2025), `matriculas == matriculas_0_a_3 + matriculas_4_a_5 == matriculas_publica + matriculas_privada`.
- [ ] Os 3 PNG existem e citam a fonte no rodapé.
- [ ] Nenhuma referência restante a `matriculas_0_a_6` (`grep -rn` no repo, fora de `specs/` e do histórico).

## V3: Reprodutibilidade
- [ ] Notebook do zero (kernel limpo, `analises_env`, cwd na raiz) roda sem erro, lendo só o extrato (sem rede).
- [ ] Com o extrato removido temporariamente, a função reconstrói um extrato idêntico a partir do cache.
- [ ] `git status` limpo de ZIPs (cache ignorado).

## V4: Relatórios
- [ ] HTML: card de matrículas com 0-5 e os dois cards novos; sem "0 a 6"; tamanho e contagem de cards comparados com o baseline.
- [ ] PDF e DOCX regenerados, com a seção de matrículas atualizada.
