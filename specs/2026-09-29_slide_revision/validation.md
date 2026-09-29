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
| V1 | Estrutura | 33 slides na ordem do §4 da especificação; S06 ausente; `--png` gera 33 imagens || ✅ 33 slides na ordem do §4; S06 ausente; `--png` gera 33 imagens (2026-09-29) |
| V2 | Textos fixos | subtítulo, bullets do slide 02, título do 05 ("centro"), "Governança de Dados" com Consistência/Periodicidade/Privacidade, "principal" no 10, contato novo — exatamente como no pedido || ✅ subtítulo, bullets 2-3 do slide 02 (o antigo bullet 3 coube, fonte 23 px), "Um centro para os dados…", "Governança de Dados" com as 3 caixas, "principal" no 10, contato novo |
| V3 | Regras R1-R6 | grep no `.md` e no texto dos PNG: 0 "0 a 5 anos" fora da nota de equivalência, 0 "extrema pobreza", 0 "pobreza/baixa renda", 0 "Zika (2016)", 0 "469", 0 "infância" sem "primeira" antes || ✅ no `_build/apresentacao.md`: 0 "extrema pobreza", 0 "pobreza/baixa", 0 "Zika (2016)", 0 "469", 0 "ficam em branco", 0 "infância" sem "primeira". "0 a 5 anos" só nas notas de equivalência; nas fontes vindas do manifesto do relatório o deck troca por "até 72 meses" (`fonte_mapa`); os gráficos do deck vêm da versão de impressão, sem título embutido. Resta a legenda "0 a 5 anos" da série total no gráfico de atendimento escolar (slide 22), um rótulo de dado ao lado de "0 a 3" e "4 a 5" |
| V4 | Números | todo número novo vem de `numeros.py`; `vf_taxa_total_2025` = soma dos absolutos ÷ população; `censo_0_5_2022_mil` confere com a SIDRA 9606 || ✅ números novos em `numeros.py`; vínculos da violência sem soma (D9): mãe 1.756 (4,5 por mil), pai 1.404 (3,6), outros 110 (0,3); `censo_0_5_2022_mil` = 379.609 (SIDRA 9606, "Total 0 a 5 anos") → 380 mil; pobreza pela chave `0-218` (77%; uma adulta 80%) |
| V5 | Mapas | nenhuma terra azul; contagens com classes discretas, taxas/% contínuas; slides 16 e 28 com teto de Tukey e nota nomeando os extremos || ✅ Censo em terracota (absoluto em classes, % contínuo com Tukey: Grumari, Campo dos Afonsos); mortalidade (teto 32,8; 7 bairros nomeados) e baixo peso (teto 15,9; 4 nomeados) com Tukey; violência em classes (`OrRd`). `BuGn` (nascidos, baixo peso) termina em verde-azulado — aceito como "teal accent", sem terra azul na revisão visual. `_a4_mapa`: com teto explícito o P95 não é mais aplicado |
| V6 | Slide 25/26 | título sem "mãe"; ~~soma em destaque~~ vínculos separados, sem soma (D9); mapas 2025 de mãe e pai; nota "notificação não é caso confirmado" | ✅ título "Violência familiar contra a primeira infância, por vínculo do provável autor"; taxas 4,5 (mãe), 3,6 (pai), 0,3 (outros) por mil; gráfico por vínculo do relatório (versão de impressão); slide 26 com os mapas de mãe e pai e a nota "os mapas não se somam". A primeira implementação (soma, 3.270) foi retirada a pedido do usuário |
| V7 | Destaques | caixa central do slide 09 e nota monoparental do slide 24 visivelmente destacadas; nenhum slide com texto cortado ou sobreposto || ✅ caixa Ripsa destacada (borda e sombra, número maior); nota monoparental em caixa destacada acima das figuras (abaixo delas encostava no rodapé de 2 linhas); caixas de "Governança" cabem na moldura (fonte 42 px). Legenda do gráfico de raça (slide 14) que cobria a barra "Parda" de 5 anos: corrigida no deck (gráficos passam a vir da versão de impressão, `visualizacoes/a4/`) e na origem (`grafico_barra_agrupado` com a legenda fora da área do gráfico) |
| V8 | Rótulo de renda (D1) | `cadunico.py`, tabelas, site (`index.html`, `data/charts.js`), PDF e textos curados sem "Extrema pobreza"/"Pobreza/baixa renda"; demais saídas idênticas || ✅ `cadunico.py`, tabelas (`analise.py` completo no `analises_env`), site (`index.html`, `data/charts.js`) e PDF (`gerado/*.tex`, sem `--publicar`) sem "Extrema pobreza"/"Pobreza/baixa renda"; diff por palavra do site e do LaTeX só com os rótulos e o texto curado |
| V9 | Variante | `variantes/exemplo_secretaria.md` gera sem erro com a nova estrutura || ✅ `variantes/exemplo_secretaria.md` = deck novo com o cabeçalho da variante; gera 33 slides sem erro |
| V10 | Documentação | `apresentacao/README.md` (33 slides), especificação do projeto, ROADMAP (72 meses + paleta no site/PDF), CHANGELOG || ✅ `apresentacao/README.md`, `docs/especificacao_projeto.md` (33 slides, RF21-RF22), ROADMAP (feito + "72 meses e paleta no site/PDF" + legenda do gráfico de raça), CHANGELOG |
