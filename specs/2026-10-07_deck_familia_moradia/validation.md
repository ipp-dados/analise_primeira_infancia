# VALIDATION — Apresentações de Família e Cuidados e de Moradia

| # | Critério | Resultado |
|---|---|---|
| V1 | Todo número dos slides vem de `{{n:...}}` | OK (Família) — conferidas com as CSVs: 81,2% / 140.976 famílias com uma só adulta; 80% × 54% em pobreza; privada −22% (114.554 → 89.538), pública −2,5% (144.314 → 140.722); vacinas: 4 de 11 na meta em 2025, mediana 69% (2022) → 94%. Moradia: pendente (§4 da specification) |
| V2 | "até 72 meses"; nenhum "0 a 5 anos" fora da nota de equivalência e dos nomes de faixa (creche 0 a 3, pré 4 e 5) | OK |
| V3 | Número antes de percentual nos mapas por bairro; contagem em classes discretas, percentual em escala contínua | OK (Família: slides 6 e 7). A escala do % começa em 60%, dito na legenda, no texto e no rodapé (D6) |
| V4 | Conferência visual (PNG) | OK — 14 slides de Família. Ajustes: escala do mapa de % (D6), gráfico de arranjo × pobreza (D7), texto do slide de vacinas. Moradia: só os 5 slides sem dados (capa, o que o eixo mostra, dois reservados, encerramento) |
| V5 | Deck principal e variantes anteriores sem mudança de fonte | OK — só acréscimos em `numeros.py`/`mapas_apresentacao.py`; `piso` padrão mantém a escala em zero no analise.py |
| V6 | Duração | Família: 14 slides, notas com ~1 a 1,5 min por slide (≈ 15 min) |
