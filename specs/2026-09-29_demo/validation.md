# VALIDATION — Versão de demonstração (branch `demo`)

Critérios de aceite. A coluna "Resultado" é preenchida ao fim da implementação.

| # | Critério | Como verificar | Resultado |
|---|----------|----------------|-----------|
| V1 | Branch `demo` criada de `staging_main` após o merge do planejamento | `git merge-base --is-ancestor <merge B0> demo` | |
| V2 | Site da `demo` sem lorem | nenhuma palavra distintiva do gerador (`dolor`, `adipiscing`, `eiusmod`, `incididunt`, `consectetur`...) em `website/index.html` e `website/data/*.js` | |
| V3 | Todo texto não curado é provisório e marcado | nº de `data-texto-demo` = nº de chaves de `textos_demo.json` usadas; nenhuma chave curada com `data-texto-demo` | |
| V4 | Textos provisórios dentro de D6 | ≤ 60 palavras por texto de figura, ≤ 3 achados por eixo; números conferidos por amostra (≥ 1 por eixo) contra `tabelas_finais/` | |
| V5 | Pendentes ocultos | 0 `callout-pending`; nenhum dos 9 títulos pendentes no HTML (sumário lateral e cartões inclusive); nenhum "pendente" nos cartões da Visão geral | |
| V6 | Dado pontual continua na `demo` | blocos `data-dado-pontual` de Inclusão e Moradia presentes, com a faixa | |
| V7 | Curadoria intocada | `git diff staging_main demo -- relatorio/textos_curados.json relatorio/curadoria_textos.docx relatorio/controle_revisao.json` vazio; DOCX regerado na `demo` com lorem e pendentes | |
| V8 | PDF da `demo` = páginas até a impressa 18 + aviso | nº de páginas = índice da página do "Mapa 1" + 1; última página com o texto de D11 e "6 de outubro de 2026"; marca d'água em todas | |
| V9 | Sumário completo, sem link quebrado | sumário igual ao da versão completa; nenhum link interno ou marcador para página inexistente (PyMuPDF) | |
| V10 | PDF sem texto provisório | nenhuma frase de `textos_demo.json` no texto extraído do PDF | |
| V11 | PDF das outras branches intacto | em `staging_main`, `gera_latex.py` sem a chave `demo` gera 161 páginas (ou o número vigente), sem página de aviso | |
| V12 | Faixa maior, com a data da V.1 | screenshots: faixa mais alta e com fonte maior que em `staging_main`, "6 de outubro de 2026" visível; no telefone (360 px), ≤ 3 linhas | |
| V13 | Desktop igual fora da faixa | comparação de screenshots desktop (≥ 1100 px) abaixo da faixa, sem diferença fora das áreas de texto e dos pendentes retirados | |
| V14 | Link do PDF aponta para a `demo` | `href` do botão PDF contém `/demo/relatorio/analise_primeira_infancia.pdf` | |
| V15 | Deploy só da `demo` e barrando lorem | regra do ambiente com só `demo`; o passo "Confere demonstração" falha num HTML de teste com lorem | |
| V16 | Regra registrada | constituição §7 com a regra da `demo` (fluxo só de ida, exclusividade) | |
