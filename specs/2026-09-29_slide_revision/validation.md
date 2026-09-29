# VALIDATION — Revisão do deck (30 → 33 slides)

## Planejamento (2026-09-29)

| Verificação | Resultado |
|---|---|
| Matriz do pedido × deck atual | a matriz omite S28 ("Dois produtos") → mantido (D3), deck com **33** slides |
| Bullet do slide 04 citado no pedido | **não existe** no deck; removido "Nem sempre chegam ao bairro" (D4) |
| Slide 09 (orig. 12) "manter 3 caixas" | o slide tem **2** caixas; a 3ª é o Censo 2022 0-5 (D5) |
| 393 × 469 mil | o deck já usa 393 mil (Ripsa 2025, 0-5) nos slides 11-12; o 469 mil (Ripsa 0-6) aparece só na nota do slide 11 |
| Gráfico de raça "0-6 → 0-5" | o PNG `censo_sidra_populacao_0_6_raca_2022` **já é 0-5** (D9 de `2026-09-29_pendencias`); muda só o texto. Achado: a legenda cobre a barra "Parda" de 5 anos |
| "Extrema pobreza" | R$ 218 é a linha de pobreza desde 2023 → rótulo errado em 11 arquivos (código, tabelas, site, PDF, texto curado) — D1 |
| Nota "menos de 20 famílias ficam em branco" | desatualizada desde `2026-09-29_privacidade_cadunico` (slides orig. 07 e 19) — R8 |
| Paletas dos mapas do deck | `Blues` (Censo) viola a regra; `BuGn` (nascidos, baixo peso) termina em verde-azulado — admitido como "teal accent", conferir na revisão visual |

## Implementação

Critérios de aceite; "Resultado" preenchido ao fim (T7.1).

| # | Verificação | Critério | Resultado |
|---|---|---|---|
| V1 | Estrutura | 33 slides na ordem do §4 da especificação; S06 ausente; `--png` gera 33 imagens | |
| V2 | Textos fixos | subtítulo, bullets do slide 02, título do 05 ("centro"), "Governança de Dados" com Consistência/Periodicidade/Privacidade, "principal" no 10, contato novo — exatamente como no pedido | |
| V3 | Regras R1-R6 | grep no `.md` e no texto dos PNG: 0 "0 a 5 anos" fora da nota de equivalência, 0 "extrema pobreza", 0 "pobreza/baixa renda", 0 "Zika (2016)", 0 "469", 0 "infância" sem "primeira" antes | |
| V4 | Números | todo número novo vem de `numeros.py`; `vf_taxa_total_2025` = soma dos absolutos ÷ população; `censo_0_5_2022_mil` confere com a SIDRA 9606 | |
| V5 | Mapas | nenhuma terra azul; contagens com classes discretas, taxas/% contínuas; slides 16 e 28 com teto de Tukey e nota nomeando os extremos | |
| V6 | Slide 25/26 | título sem "mãe"; soma em destaque e vínculos separados visíveis; mapa 2025 soma mãe + pai + outros; nota "notificação não é caso confirmado" | |
| V7 | Destaques | caixa central do slide 09 e nota monoparental do slide 24 visivelmente destacadas; nenhum slide com texto cortado ou sobreposto | |
| V8 | Rótulo de renda (D1) | `cadunico.py`, tabelas, site (`index.html`, `data/charts.js`), PDF e textos curados sem "Extrema pobreza"/"Pobreza/baixa renda"; demais saídas idênticas | |
| V9 | Variante | `variantes/exemplo_secretaria.md` gera sem erro com a nova estrutura | |
| V10 | Documentação | `apresentacao/README.md` (33 slides), especificação do projeto, ROADMAP (72 meses + paleta no site/PDF), CHANGELOG | |
