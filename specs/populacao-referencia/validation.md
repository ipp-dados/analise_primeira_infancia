# Validação: specs/populacao-referencia

Marcar `[x]` com a evidência. Os números de referência vêm da consulta ao Tabnet Ripsa (`popsvs2024br.def`,
Rio de Janeiro, `SMunicípio=3262`) de 2026-09-24. O código deve reproduzi-los enquanto a Ripsa não revisar as
estimativas (P-A1). A validação da Parte E está em `matriculas/validation.md`.

## V0: Fonte e baseline

- [x] Ripsa sem nível bairro: o menor nível do Tabnet é `Município`. *(2026-09-24)*
- [x] O POST automatizado responde (com retry: 2 de 5 consultas tiveram `ConnectionResetError` na primeira tentativa).
- [x] Validação externa: total Ripsa 2024 = 6.729.894 = estimativa municipal IBGE 2024 (Data.Rio).
- [x] Baseline antes do Bloco 1: checksums (md5) de 205 arquivos em `tabelas_finais/`, `visualizacoes/`, `mapas/`, `relatorio/*`, e cópia de `tabelas_finais/`, guardados no scratchpad da sessão. `index.html` 20.903.787 bytes; PDF 127 páginas, 46.293.238 bytes; DOCX 5.946.288 bytes. *(2026-09-24)*

## V1: População Ripsa de referência (Parte A)

Crianças de 0 a 5 anos por sexo e total de todas as idades:

| Ano | 0-5 masc. | 0-5 fem. | 0-5 | 0-4 | Total |
|---|---|---|---|---|---|
| 2000 | 300.757 | 297.565 | 598.322 | 497.379 | 6.312.372 |
| 2005 | 265.900 | 255.528 | 521.428 | 425.282 | 6.503.064 |
| 2010 | 247.131 | 235.539 | 482.670 | 400.636 | 6.605.732 |
| 2011 | 245.956 | 234.692 | 480.648 | 399.485 | 6.622.327 |
| 2015 | 251.718 | 239.963 | 491.681 | 412.521 | 6.724.719 |
| 2017 | 253.205 | 241.440 | 494.645 | 413.393 | 6.756.761 |
| 2020 | 242.549 | 231.773 | 474.322 | 389.268 | 6.770.926 |
| 2021 | 233.744 | 223.536 | 457.280 | 375.330 | 6.757.411 |
| 2022 | 224.774 | 215.133 | 439.907 | 361.163 | 6.742.618 |
| 2023 | 216.447 | 207.292 | 423.739 | 344.963 | 6.735.026 |
| 2024 | 208.258 | 199.279 | 407.537 | 331.402 | 6.729.894 |
| 2025 | 200.890 | 192.183 | 393.073 | 320.791 | 6.730.729 |

A idade simples de 2007-2025 (0-6) está em `matriculas/validation.md` V2.

- [x] O extrato reproduz a tabela acima (e os 26 anos completos). Também reproduz a idade simples de `matriculas/validation.md` V2. *(2026-09-24)*
- [x] Soma dos sexos = total por idade, para todo ano e idade (assert em `carrega_populacao_ripsa`, contra uma 4ª consulta sem filtro de sexo).
- [x] Nota A5 traz a comparação de 2022: total 6.211.223 × 6.742.618; 0-4 310.648 × 361.163; 0-5 379.609 × 439.907. Acrescentado: o Censo por bairro do Data.Rio soma 6.183.971 (total) e 310.157 (0-4), um pouco abaixo do SIDRA.

## V2: Saídas da Parte A

As células foram rodadas numa cópia de rascunho do projeto (só topo + células necessárias); as saídas pré-requisito regravadas lá (`censo_0_a_4_anos_por_ano.csv`, `violencia_familiar_por_vinculo_ano.csv`) saíram idênticas às do repositório, e só as saídas novas foram copiadas.

- [x] A2: tabela 2000-2025 (26 linhas); os gráficos citam a Ripsa; `percentual_0_a_6` = `populacao_0_a_6 / populacao_total` por ano (2025: 469.148 ÷ 6.730.729 = 6,97%). *(2026-09-24)*
- [x] A3: `taxa_por_mil_mae` de 2025 = 4,467 (assert no notebook); 15 linhas (2011-2025); colunas por vínculo, sem soma. *(2026-09-24)*
- [x] A4 viável: conexão com o `.env` atual no `analises_env`; partição `2026-06-12`; 194.138 crianças, 173.768 famílias, idade 0-5. *(2026-09-24)*
- [x] A4: razão = 194.138 ÷ 393.073 = 49,39%, partição `2026-06-12`, 173.768 famílias; uma linha só, nível município. *(2026-09-24)*

## V3: Parte B

- [x] Nenhum valor sub-municipal muda: as 19 CSV regravadas no Bloco 3 (violência por bairro/RA/CAP, taxas, gêmeas de mapa, CadÚnico por bairro) são **byte a byte iguais** ao baseline. *(2026-09-24)*
- [x] Toda saída sub-municipal com população no denominador cita "0 a 4 anos, Censo 2022": PNG (legenda + rodapé), card do HTML (legenda + fonte). Gêmeas CSV: a coluna `pop_0_4` já diz a faixa; a fonte não vai no CSV (schema mantido).

## V4: Parte D

- [x] D1: na gêmea de 2025, soma de `percentual_do_municipio` dos bairros (90,33%) + "EM BRANCO" (9,67%) = 100%; as colunas antigas da gêmea são idênticas ao baseline e o mapa de contagem não foi regravado (a entrada não mudou; uma re-renderização só mudaria bytes pelos tiles). *(2026-09-24)*
- [x] D2/D3: os itens do crosswalk têm arquivo e aparecem no HTML, PDF (p. 5 e 73) e DOCX. *(2026-09-24)*
- [x] D4: o gerador não lista mais nenhum item sem arquivo e sem status ("Itens sem arquivo e sem status: 0").

## V5: Parte C

- [x] `auditoria_faixas.md` cobre todas as fontes (CadÚnico, Censo por bairro e série, SIDRA 9606/10056/10057, Sinan, Ripsa, Censo Escolar, SISVAN, vacinação, PNAD, SIM/SINASC). *(2026-09-24)*
- [x] Renomeações executadas = lista aprovada (21 `git mv`); `grep` sem referência a nomes antigos em `*.py`, `*.json` e `estrutura_eixos.md`. *(2026-09-24)*

## V6: Fechamento

- [ ] Notebook do zero no `analises_env` sem erro, usando só os extratos (sem rede).
- [ ] HTML, PDF e DOCX regenerados; diferenças em relação ao baseline explicadas (cards novos, rótulos).
- [ ] `git status` sem ZIP e sem saída gerada por engano.
