# VALIDATION — Pendências

Critérios de aceite; a coluna "Resultado" é preenchida ao fim da implementação (T8.3).

## Planejamento (2026-09-29)

| Verificação | Resultado |
|---|---|
| Mapas de taxa de mortalidade infantil 2025 (cartão neonatal × raça/cor) | **OK, iguais**: 167 × 167 códigos, diferença máxima 7e-15 |
| Deploy do site depois do merge | **OK**: `deploy-relatorio.yml` em `ab9f803` (2026-09-29 13:00 UTC, sucesso) |
| PDF publicado × estrutura atual | **desatualizado**: último `--publicar` em `17cae4a` (melhorias_site), antes da `nova_estrutura` |

## Implementação

| # | Verificação | Critério | Resultado |
|---|---|---|---|
| V1 | Saídas de `analise.py` não tocadas | hash idêntico antes × depois, fora da lista de saídas alteradas desta rodada | |
| V2 | Mapa duplicado (R1) | site: cartão neonatal com 3 pills nos dois modos; PDF sem `mapa_taxa_mortalidade_infantil_bairro_2025`; E13 escrito | |
| V3 | "Não informada" (R2) | gráfico de taxa com 4 séries no site, na PNG e no A4; contagem com 5; nota presente; E14 escrito | |
| V4 | Eixo cortado (R3) | só o baixo peso com eixo cortado, barras inclinadas e nota nos 3 lugares; nenhum outro gráfico mudou (V1) | |
| V5 | Taxa de frequência 0-5 (R4) | recalculada de 10057 ÷ 9606; diferença para a 10056, idade a idade, registrada; "Amarela e indígena" e "Total" 0-5 presentes | |
| V6 | Faixa 0-5 (R4) | nenhum gráfico, rótulo ou número publicado (site, PDF gerado, deck) com 6 anos sem nota | |
| V7 | Tablet (R5) | 800 e 1024 px: alvos ≥ 44 px, texto dos gráficos entre 9,5 e 11 px, sem rolagem horizontal | |
| V8 | Desktop (R5) | 1440 e 1100 px pixel a pixel iguais à linha de base, fora dos cartões alterados em R1-R4 | |
| V9 | Celular | 390 px sem regressão (capturas antes × depois) | |
| V10 | PDF | compila; 0 `undefined`; 93 figuras (94 − 1 mapa), 43 tabelas, nenhuma outra a menos; overfull só os já aceitos | |
| V11 | Site | inventário: nenhuma seed/figura a menos além de R1; `index.html` < 1 MB, site < 2 MB | |
| V12 | Deck (R7) | compila; slide com o mapa de raça/cor; rótulos 0-5 | |
| V13 | Textos (R8) | trechos ajustados listados; marcados `revisar`; `valida_textos_publicados.py` sem frase ausente | |
| V14 | Documentação (R6, R9, R10) | exclusões E12-E14, constituição, `CLAUDE.md`, CHANGELOG, ROADMAP, especificação do projeto atualizados | |
