# VALIDATION — Apresentação breve do eixo Inclusão

| # | Critério | Resultado |
|---|---|---|
| V1 | Todo número dos slides vem de `{{n:incl_*}}` (nenhum digitado) e bate com as tabelas de `tabelas_finais/` | OK — 21 chaves `incl_*`; conferidas com as CSVs (7.919; 3,9%; 7.810; 4,4%; 1.530/6.335 = 24,2%; 1.475 sem informação) |
| V2 | "até 72 meses" em todo o texto; nenhum "0 a 5 anos" fora de nota de equivalência | OK — "até 72 meses" em todo slide; "0 a 5 anos" só na nota de equivalência do slide 2 |
| V3 | Mapa com escala contínua, nota de extremos (Tukey) e de bairros somados; fonte com a partição | OK — escala contínua, Tukey (teto 5,3; 6 bairros nomeados no rodapé), nota de bairros somados por RA |
| V4 | Conferência visual dos slides (PNG) | OK — 8 PNG conferidas. Achado: o tema não era aplicado (rodapé longo quebrado pelo `yaml.safe_dump` -> Marp ignorava o front matter); corrigido no gerador (`width`) |
| V5 | `apresentacao.md` e os PDFs/PPTX do deck principal não mudam | OK — `apresentacao.md` e `apresentacao_primeira_infancia.pdf/.pptx` sem mudança (o rodapé do deck principal é curto: mesmo front matter) |
| V6 | Demo: site regerado sem lorem/pendente; nada da demo em `staging_main` | OK — "Demo OK: 83 textos provisórios, sem lorem, sem pendentes"; site sem mudança de conteúdo nesta rodada; `demo` fora da história de `staging_main` |
