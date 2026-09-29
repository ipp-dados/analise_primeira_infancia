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
| Textos propostos pelo IPP (Q4) | 6 trechos marcados `<!-- revisar -->`: slides 2, 3, 5, 6, 7 e 17 |
| Revisão visual | PNG de cada slide conferida (folhas de contato); ajustes: capa (secretaria vazia, logo branco), largura da tabela de pendentes, slide de educação com o gráfico, link no encerramento |
| PPTX | `apresentacao/apresentacao_primeira_infancia.pptx` (15,8 MB, uma imagem por slide + notas, com o roteiro da demonstração no slide 28) |
| PDF | `apresentacao/apresentacao_primeira_infancia.pdf` (4,5 MB, com notas) |
| PPTX editável (experimental) | gera (`--editavel`), mas com as fontes do sistema no lugar de Fraunces/IBM Plex: títulos longos quebram e sobrepõem. Não publicado; ponto de partida para quem precisar editar no PowerPoint |
| Variante | `variantes/exemplo_secretaria.md` gera sem erro (secretaria na capa, sem notas de demonstração) |
| Problema encontrado | o marp-cli espera o Markdown pela entrada padrão quando ela não é um terminal (o primeiro build ficou parado); corrigido com `stdin=DEVNULL` |

## Revisão do usuário (2026-09-28)

- Saiu o slide "O que precisamos das secretarias" (com os próximos passos). Entrou, como slide 3, "Um produto vivo,
  construído com as secretarias": o projeto é feito **com** elas (vivo, com o conhecimento de quem está na ponta,
  aberto a sugestões e a dados compartilhados). Continua com 30 slides; a variante de exemplo recebeu a mesma troca.

## Revisão do usuário 2 (2026-09-28)

- **Mapas sem outliers**: todo `fig:` de mapa usa agora a versão de impressão (`mapas/a4/<nome>.pdf`, rasterizada),
  que tem o teto de cor no percentil 95 nos mapas contínuos por bairro (mesmo tratamento do site e do PDF, D5) e não
  tem título embutido. A fonte e a nota do teto saem do manifesto A4 para o rodapé do slide (fonte repetida aparece
  uma vez). Os mapas de contagem (classes discretas) não têm teto, como no site. Exemplo do efeito: a mortalidade
  infantil por bairro (slide 18) deixa de ficar quase toda clara por causa de poucos bairros extremos.
- **Slides novos** (eixo Família e Cuidados): matrículas por rede, pública × privada (slide 23), e arranjo familiar
  no CadÚnico, adultos por família (slide 24, gráfico + mapa de % com uma só adulta).
- **Continua com 30 slides**: "Na cidade, estimativa do ano; no bairro, o Censo" virou a nota do slide "Quantas
  crianças?" (sai o gráfico da série Ripsa); "Há menos crianças pequenas a cada Censo" virou a legenda do "469 mil"
  (sai o gráfico dos Censos). Os dois gráficos seguem no site e no relatório.
- Observação: no mapa de % de famílias com uma só adulta quase todos os bairros ficam na cor mais escura; não é
  outlier, é o dado: a proporção é alta (cerca de 80%) em toda a cidade.

## Revisão do usuário 3 (2026-09-28)

- **Centro como outlier no mapa do IPS** (slide 26): mapa próprio da apresentação (`apresentacao/build/mapas_apresentacao.py`,
  gravado só em `apresentacao/_build/mapas/`), com a regra de outlier do site (cercas de Tukey 1,5 x IQR): a escala vai
  até o maior valor não outlier (Madureira, 33,5) e o Centro (76, acima da cerca de 46,9) fica com a cor máxima, dito
  no rodapé e no texto. Para isso, `_a4_mapa` (`primeira_infancia/impressao.py`) ganhou o parâmetro opcional `teto=`;
  sem ele, nada muda nos mapas do relatório. Site e PDF do relatório continuam com o mapa de sempre.
- **População padronizada**: um número-âncora, **469 mil** crianças de 0 a 6 anos (Ripsa 2025, a faixa da política),
  sempre em "mil". O slide dele vem antes do das réguas e a tendência usa a mesma fonte (699 mil em 2000 → 469 mil em
  2025, −33%), em vez de misturar com o Censo de 0 a 4 anos. O slide seguinte explica as outras duas réguas, no mesmo
  formato: 393 mil (0 a 5 anos, base do CadÚnico) e 308 mil (0 a 4 anos, Censo 2022, a única por bairro).
