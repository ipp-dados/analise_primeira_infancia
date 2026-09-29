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
| V1 | Carga da moradia | 10 categorias; fossa séptica pessoas = 17.149; sem a aba duplicada; cisterna com crianças "não informado"; totais de famílias/pessoas iguais aos da planilha | ✅ 10 categorias; fossa séptica pessoas 17.149; aba duplicada descartada (e duplicata **divergente** dá erro — teste sintético); cisterna com crianças vazias (`criancas_nao_informado`); famílias/pessoas iguais às da planilha |
| V2 | Carga da deficiência | 6 valores do pedido; total 0-6 = 25.995; % BPC 33,3 e 43,1 | ✅ 9.258/3.086 e 16.737/7.214; total 0-6 = 25.995 (10.300 com BPC); % BPC 33,3 · 43,1 · 39,6 |
| V3 | Metadados | manifesto com `is_adhoc: true`, `ref_date: "2026-08"`, `replacement_pending: true`; o texto do aviso vem só dele | ✅ `dados_locais/cadunico/adhoc_2026_08.json` com `is_adhoc`, `ref_date`, `replacement_pending`, `substituicao_prevista` 2026-Q4; o aviso do site e do PDF vem de `aviso_dado_pontual()` (lê o manifesto); o deck repete o texto (sem leitor de manifesto — anotado no slide) |
| V4 | Só acréscimo — site | `website/data/charts.js`: entradas antigas idênticas; HTML fora de Inclusão/Moradia idêntico (exceto contadores); screenshots desktop das outras abas pixel-idênticas | ✅ `data/charts.js` idêntico; `index.html`: só inserções (blocos novos, links do sumário, caixa de fontes de Inclusão e Moradia, que não tinham) + contadores "3 → 4" e "3 → 5 subseções" + hash do CSS. Screenshots 1400 e 1280 px: Família e Cuidados, Proteção, Direito ao Brincar, Alimentação idênticas (0); Visão geral só nos contadores; Prioridade: diferença só na sombra da barra de abas (estado de rolagem, alterna entre 1400 e 1280 de uma execução para outra) |
| V5 | Site — conteúdo | Inclusão e Moradia mantêm os quadros de pendente e ganham os blocos novos, com o aviso "Dado pontual" e a nota da faixa 4-6 | ✅ 3 quadros de pendente em cada eixo mantidos; blocos novos depois deles com o quadro "Dado pontual" (aviso + faixa) |
| V6 | Site — telefone/tablet | cartões e barras sem rolagem horizontal a 375 px e 768 px | ✅ 390 e 768 px: `scrollWidth` = largura da tela nas duas abas; cartões em 2 colunas no celular; sem erro de console |
| V7 | PDF | build sem erro; 3 seções novas com tabela no corpo e quadro de aviso; pendentes inalterados; fonte no inventário | ✅ 167 páginas (antes 161); 3 seções novas com tabela no corpo (retrato) e quadro "Dado pontual"; pendentes inalterados; 0 `undefined`, 12 overfull (iguais); linhas que saíram do texto: só números de página/tabela e a citação do CadÚnico, que vira "(2026a)" (a extração pontual é "(2026b)", mesmo autor e ano — ABNT); fonte no inventário (`mds_cadunico_adhoc`, 4 tabelas ligadas) |
| V8 | Deck | build sem erro; 1 slide novo antes de "Eixos incompletos"; números iguais às CSVs; demais slides inalterados | ✅ 34 slides; slide 29 novo antes de "Eixos incompletos"; números = CSVs (25.995; 33%/43%; 1.425; 2.226); texto dos 33 slides antigos idêntico fora o número da página; 0 anotações no PDF |
| V9 | Faixa 4-6 | nota explícita em todo lugar em que o número sai (site, PDF, deck) | ✅ site (quadro "Dado pontual" em cada item), PDF (quadro), deck (nota do slide) |
| V10 | Roadmap | item de substituição no 4º tri de 2026 com a lista de arquivos do manifesto | ✅ `ROADMAP.md`, Próximas features item 4, com a lista do que apagar/trocar |
| V11 | DOCX de curadoria | exporta sem erro, com as chaves novas | ✅ DOCX regerado (3 itens novos); **achado**: tabelas no corpo não têm bloco de texto no DOCX (já acontecia com `cadunico_razao_populacao_0_a_5_2026`) — no ROADMAP (curadoria) |

**Não feito:** execução completa do `analise.py` do zero (constituição §2) — precisa do banco do CTPE e reescreveria
saídas que esta rodada não pode mudar (D1). A célula nova não depende de nada anterior (só lê `dados_locais/cadunico/`)
e foi rodada isolada; `jupytext --to notebook` e `ast.parse` sem erro.
