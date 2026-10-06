# VALIDATION — CadÚnico: pipeline novo para Inclusão e Moradia

## Planejamento (2026-10-06)

| Verificação | Resultado |
|---|---|
| Partição das tabelas CadÚnico do CTPE | todas 2026-07-10 |
| `silver_cadunico_geral` com `grupo_idade='0-6'` | **0 linhas** (grupo agora `'0-5'`, A1) |
| Crianças `'0-5'` (geral e pessoas) | 200.784 nas duas; 178.838 famílias |
| Crianças 0-5 com deficiência | 7.919 (4,0%); dado pontual 0-6: 25.995 (A2) |
| Crianças 0-5: inadequação / déficit / adensamento (Sim) | 11.589 / 86.393 / 101.477 |
| Bairros que passam sozinhos (num. e compl. ≥ 20) | deficiência 58%, inadequação 59%, adensamento 89%, déficit 90% |
| Ponte CEP → bairro: cobertura das crianças; código fora da camada oficial | 90,9%; nenhum |

## Implementação

Critérios de aceite; "Resultado" preenchido ao fim.

| # | Critério | Resultado |
|---|---|---|
| V1 | `analise.py` roda do zero sem erro, com a seção CadÚnico não vazia | |
| V2 | Totais do município das tabelas novas batem com o levantamento acima e com `gold_cadunico_indicadores` | |
| V3 | Nenhuma saída por bairro com contagem < 20 (numerador, complemento ou base) fora de conjunto | |
| V4 | Percentuais calculados de absolutos, sem "Não informado"/"Não se aplica" na base; base publicada | |
| V5 | Toda figura nova cita a fonte com a partição (jul/2026) e, nos mapas, a regra de bairros somados | |
| V6 | Mapas de % com escala contínua; join por `codbairro` | |
| V7 | Crosswalk: 6 itens em Inclusão/Moradia, nenhum `pendente`, nenhum `dado_pontual` | |
| V8 | Site de `staging_main`: blocos novos com lorem; sem `data-dado-pontual`; desktop e celular conferidos; orçamento | |
| V9 | `demo`: faixa com 13 de outubro de 2026 e atualização de conteúdo; nota nas abas; build sem lorem/pendente | |
| V10 | PDF da `demo`: página de aviso com a nova data; demais páginas iguais | |
| V11 | Nada da `demo` em `staging_main` (merge só de ida) | |

## Para a rodada de textos (D5)

Textos curados que citam números do CadÚnico de jun/2026 (lista preenchida na implementação).
