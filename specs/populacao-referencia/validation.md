# Validação: specs/populacao-referencia

Marcar `[x]` com a evidência. Os números de referência vêm da consulta ao Tabnet Ripsa (`popsvs2024br.def`,
Rio de Janeiro, `SMunicípio=3262`) de 2026-09-24. O código deve reproduzi-los enquanto a Ripsa não revisar as
estimativas (P-A1). A validação da Parte E está em `matriculas/validation.md`.

## V0: Fonte e baseline

- [x] Ripsa sem nível bairro: o menor nível do Tabnet é `Município`. *(2026-09-24)*
- [x] O POST automatizado responde (com retry: 2 de 5 consultas tiveram `ConnectionResetError` na primeira tentativa).
- [x] Validação externa: total Ripsa 2024 = 6.729.894 = estimativa municipal IBGE 2024 (Data.Rio).
- [ ] Baseline antes do Bloco 1: checksums de `tabelas_finais/`, `visualizacoes/`, `mapas/`, `relatorio/*`, e contagens do HTML (cards, mapas SVG, tamanho), páginas do PDF e headings do DOCX.

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

- [ ] O extrato reproduz a tabela acima (e os 26 anos completos).
- [ ] Soma dos sexos = total por idade, para todo ano e idade.
- [ ] Nota A5 traz a comparação de 2022: total 6.211.223 × 6.742.618; 0-4 310.648 × 361.163; 0-5 379.609 × 439.907.

## V2: Saídas da Parte A

- [ ] A2: tabela 2000-2025 (26 linhas); o gráfico cita a Ripsa; o `percentual_0_a_6` é recalculado da soma, e não a média.
- [ ] A3: `taxa_por_mil_mae` de 2025 = 1.756 ÷ 393.073 × 1.000 ≈ 4,47; 15 anos (2011-2025); vínculos não somados entre si.
- [x] A4 viável: conexão com o `.env` atual no `analises_env`; partição `2026-06-12`; 194.138 crianças, 173.768 famílias, idade 0-5. *(2026-09-24)*
- [ ] A4: razão = 194.138 ÷ 393.073 ≈ 49,4% (ou os números da partição vigente, registrada); nenhuma contagem sub-municipal nova gravada.

## V3: Parte B

- [ ] Nenhum valor sub-municipal muda: tabelas `violencia_familiar_taxa_*`, `violencia_familiar_por_ra/cap` e gêmeas de mapa idênticas ao baseline, exceto por mudança de rótulo ou coluna de texto.
- [ ] Toda saída sub-municipal com população no denominador cita "0 a 4 anos, Censo 2022" (PNG, gêmea, card do HTML).

## V4: Parte D

- [ ] D1: na gêmea de 2025, soma de `percentual_do_municipio` dos bairros + "EM BRANCO" = 100%; o mapa de contagem é idêntico ao baseline.
- [ ] D2/D3: os itens do crosswalk têm arquivo e aparecem no HTML, PDF e DOCX.
- [ ] D4: o gerador não lista mais nenhum item sem arquivo e sem status.

## V5: Parte C

- [ ] `auditoria_faixas.md` cobre todas as fontes (CadÚnico, Censo por bairro, SIDRA, Sinan, Ripsa, Censo Escolar, SISVAN, vacinação, PNAD).
- [ ] Renomeações executadas = lista aprovada; `grep` sem referência a nomes antigos fora de `specs/`.

## V6: Fechamento

- [ ] Notebook do zero no `analises_env` sem erro, usando só os extratos (sem rede).
- [ ] HTML, PDF e DOCX regenerados; diferenças em relação ao baseline explicadas (cards novos, rótulos).
- [ ] `git status` sem ZIP e sem saída gerada por engano.
