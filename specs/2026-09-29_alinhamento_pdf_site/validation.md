# VALIDATION — Alinhamento PDF × site

Critérios de aceite; a coluna "Resultado" é preenchida ao fim (T5.2).

| # | Verificação | Critério | Resultado |
|---|---|---|---|
| V1 | Ordem (D1) | em Prioridade, a ordem das seções do PDF acompanha a dos cartões do site; nenhuma outra seção mudou de lugar | |
| V2 | Vacinação (D2) | `cobertura_vacinal_epi_ano` na tela e no A4; figura na seção do PDF com o texto curado; DOCX com a imagem | |
| V3 | Tabelas no corpo (D3) | as duas tabelas aparecem dentro das seções, formatadas como no apêndice, e não se repetem no apêndice | |
| V4 | Remoção (D4) | seção de causas evitáveis por raça/cor fora do PDF e do DOCX; E16 escrito; SISVAN (número) inalterado | |
| V5 | Pendentes (D5) | todo quadro de pendente, no site e no PDF, com a frase fixa + o motivo formal; nenhuma anotação interna ("Léo", "Posterior", "baixar") publicada | |
| V6 | Estrutura | seções do PDF sem figura, fora as pendentes: só as duas de SISVAN (número) | |
| V7 | Builds | PDF compila, 0 `undefined`, overfull só os já aceitos; site < 1 MB `index.html`; desktop igual fora dos quadros de pendente; `valida_textos_publicados.py` sem frase ausente | |
| V8 | Documentação | exclusões E1/E16, controle de revisão, CHANGELOG, README, ROADMAP, especificação do projeto, `relatorio/specs.md` | |
