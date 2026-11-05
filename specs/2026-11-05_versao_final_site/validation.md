# VALIDATION — Versão final do site e do relatório (2026-11-05)

## Feito (Blocos 1 e 2)

| Verificação | Resultado |
|---|---|
| Lorem no site | 0 (`grep -i lorem website/index.html`) |
| Lorem no PDF | 0 ("0 textos em lorem" no `gera_latex.py`) |
| Textos importados | 36 do DOCX de 05/11 (números conferidos), 17 de abas, 2 da Introdução dividida, 21 de eixo |
| Site no navegador | Edge, 1366 e 390 px: sem erro de console, sem rolagem horizontal, em todas as abas |
| Dados faltantes | 8 itens em `docs/dados_faltantes.csv`, iguais ao documento para gestores |

## Critérios de aceite (Blocos 3 a 9)

| # | Critério | Resultado |
|---|---|---|
| V1 | Banner com a foto servida pelo próprio site, crédito visível com links, contraste AA, celular sem quebra | |
| V2 | Mapa de referência: 3 camadas, nomes por botão, nome no hover, tabela para baixar; figura A4 no PDF | |
| V3 | Rodapé sem e-mail; todos os links respondem (HTTP 200/301) | |
| V4 | Sem faixa "em desenvolvimento" no site e sem marca d'água no PDF | |
| V5 | PDF a partir de `capitulos/*.tex`: mesmo conteúdo do PDF de referência (fora capa e folha de rosto); 0 referências indefinidas; checagem de rótulos passa | |
| V6 | Capa e folha de rosto novas conferidas em PNG | |
| V7 | Nenhum script DOCX no repositório; tag `rodada/curadoria_docx` existe; skills e docs sem DOCX; `confere_textos.py` roda | |
| V8 | `gh` instalado e autenticado; Release criada com o PDF; link do site para `releases/latest` funciona | |
| V9 | Deploy automático em push na `main`; checagem em PR/push para `staging_main` passa | |
| V10 | Teste completo (todas as abas, pills, mapas, downloads, links) desktop e celular, com capturas | |
| V11 | Site publicado a partir da `main`; constituição §7 e `CLAUDE.md` atualizados | |
