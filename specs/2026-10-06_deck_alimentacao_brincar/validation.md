# VALIDATION — Apresentações breves de Alimentação e Direito ao Brincar

| # | Critério | Resultado |
|---|---|---|
| V1 | Todo número dos slides vem de `{{n:...}}` (nenhum digitado) | OK — 18 chaves `alim_*`, 11 `brin_*` (+ `baixo_peso_*`, `homicidios_*` já existentes); conferidas com as CSVs (5.869 / 10,0%; SISVAN 2025: 16.215 de 215.132 = 7,5%, 36.062 = 16,9%, 15.674 = 7,3%; homicídios 16,7, ação policial 5,8, jovens negros 3,5) |
| V2 | "até 72 meses"; nenhum "0 a 5 anos" fora da nota de equivalência | OK |
| V3 | Número antes de percentual nos mapas por bairro; contagem em classes discretas, percentual em escala contínua com Tukey | OK — slides 4 e 5 de Alimentação |
| V4 | Conferência visual (PNG) | OK — 11 + 8 slides. Ajustes: imagem do dado pontual passava do rodapé (`lado baixo`); SISVAN da versão A4 ia até 2026 parcial e com os dois % errados (séries só do deck); frase de comparação número × % reescrita |
| V5 | Deck principal e variante de Inclusão sem mudança de fonte; pré-processam sem erro | OK — `apresentacao.md` e `variantes/inclusao.md` não mudaram; únicas diferenças na próxima geração: rodapé do mapa de baixo peso sem "998" |
| V6 | Dado pontual fora do site e do PDF | OK — não está no crosswalk |
