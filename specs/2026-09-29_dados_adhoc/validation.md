# VALIDATION — Dados pontuais do CadÚnico: Moradia e Inclusão

## Planejamento (2026-09-29)

| Verificação | Resultado |
|---|---|
| Planilha de referência: 11 abas, uma por filtro, 4 medidas cada | lida; 10 filtros distintos + 1 aba duplicada (A2) |
| Valores não numéricos | 1: fossa séptica, pessoas `'17..149'` (A1) |
| Crianças zeradas com famílias > 0 | 1: cisterna, 1.323 famílias, 0 crianças nas duas faixas (A3) |
| Cobertura BPC do pedido | 3.086 / 9.258 = 33,33%; 7.214 / 16.737 = 43,10% — confere com o pedido |
| Faixa etária | 0-3 e 4-6 (inclui 6 anos) — exceção com nota (D1) |

## Implementação

Critérios de aceite; "Resultado" preenchido ao fim (T7.3).

| # | Verificação | Critério | Resultado |
|---|---|---|---|
| V1 | Carga da moradia | 10 categorias; fossa séptica pessoas = 17.149; sem a aba duplicada; cisterna com crianças "não informado"; totais de famílias/pessoas iguais aos da planilha | |
| V2 | Carga da deficiência | 6 valores do pedido; total 0-6 = 25.995; % BPC 33,3 e 43,1 | |
| V3 | Metadados | manifesto com `is_adhoc: true`, `ref_date: "2026-08"`, `replacement_pending: true`; o texto do aviso vem só dele | |
| V4 | Só acréscimo — site | `website/data/charts.js`: entradas antigas idênticas; HTML fora de Inclusão/Moradia idêntico (exceto contadores); screenshots desktop das outras abas pixel-idênticas | |
| V5 | Site — conteúdo | Inclusão e Moradia mantêm os quadros de pendente e ganham os blocos novos, com o aviso "Dado pontual" e a nota da faixa 4-6 | |
| V6 | Site — telefone/tablet | cartões e barras sem rolagem horizontal a 375 px e 768 px | |
| V7 | PDF | build sem erro; 3 seções novas com tabela no corpo e quadro de aviso; pendentes inalterados; fonte no inventário | |
| V8 | Deck | build sem erro; 1 slide novo antes de "Eixos incompletos"; números iguais às CSVs; demais slides inalterados | |
| V9 | Faixa 4-6 | nota explícita em todo lugar em que o número sai (site, PDF, deck) | |
| V10 | Roadmap | item de substituição no 4º tri de 2026 com a lista de arquivos do manifesto | |
| V11 | DOCX de curadoria | exporta sem erro, com as chaves novas | |
