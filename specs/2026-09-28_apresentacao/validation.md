# VALIDATION — Apresentação

Implementação em 2026-09-28, branch `spec/apresentacao` (a partir de `spec/nova_estrutura`).

| Verificação | Resultado |
|---|---|
| Slides | **30** (roteiro da §4 com dois ajustes: os mapas de número e de proporção num slide só; "Próximos passos" e "O que precisamos das secretarias" num slide só) |
| Placeholders não resolvidos | 0 (o build para se sobrar `{{...}}`, figura inexistente ou número inexistente) |
| Números | todos calculados de `tabelas_finais/` por `apresentacao/build/numeros.py` (`python apresentacao/build/numeros.py` lista os valores) |
| R1 — nascidos vivos 65.507 × 59.171 | resolvido: a diferença é o número de nascidos sem bairro informado (6.336 em 2025). O slide 18 usa o total do município e diz quantos ficam fora do mapa; a taxa de mortalidade infantil (slide 19) diz que usa só os nascidos com bairro informado |
| R2 — diagrama do hub | feito em HTML/CSS no slide 3 (sem imagem) |
| R3 — mapa de limites | substituído: o slide 9 compara dois mapas reais (CAP e RA) |
| R4 — mapas em 16:9 | não precisou de variante: mapas e gráficos cabem ao lado do texto (`.lado`) ou em par (`.dois`) |
| Fontes das figuras | as PNGs trazem a fonte; slides só com números têm `<!-- fonte: -->` no rodapé |
| Textos propostos pelo IPP (Q4) | 6 trechos marcados `<!-- revisar -->`: slides 2, 4, 5, 6, 16 e 29 |
| Revisão visual | PNG de cada slide conferida (folhas de contato); ajustes: capa (secretaria vazia, logo branco), largura da tabela de pendentes, slide de educação com o gráfico, link no encerramento |
| PPTX | `apresentacao/apresentacao_primeira_infancia.pptx` (15,8 MB, uma imagem por slide + notas, com o roteiro da demonstração no slide 28) |
| PDF | `apresentacao/apresentacao_primeira_infancia.pdf` (4,5 MB, com notas) |
| PPTX editável (experimental) | gera (`--editavel`), mas com as fontes do sistema no lugar de Fraunces/IBM Plex: títulos longos quebram e sobrepõem. Não publicado; ponto de partida para quem precisar editar no PowerPoint |
| Variante | `variantes/exemplo_secretaria.md` gera sem erro (secretaria na capa, sem notas de demonstração) |
| Problema encontrado | o marp-cli espera o Markdown pela entrada padrão quando ela não é um terminal (o primeiro build ficou parado); corrigido com `stdin=DEVNULL` |
