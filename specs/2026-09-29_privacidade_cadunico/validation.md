# VALIDATION — Privacidade do CadÚnico

## Planejamento (2026-09-29)

| Verificação | Resultado |
|---|---|
| Tabelas do CadÚnico por bairro versionadas (HEAD) | **conformes**: 0 contagens de 1 a 19 nas 4 tabelas; bairros pequenos vazios |
| Histórico do git | **não conforme**: `cdfacd2` (2026-09-09) com 20-22 contagens de 1 a 19 por bairro em `cadunico_por_bairro_2026`, `cadunico_por_bairro_ate_4_2026`, `tabela_mapa_cadunico_criancas_2026`, `tabela_mapa_cadunico_primeira_infancia_2026` — registrado (D3) |
| Percentuais publicados × totais publicados | **não conforme**: numerador ou complemento < 20 em 6 bairros (% negras) e 14 (% uma adulta) |
| Primeira varredura (falso alarme) | os "valores < 20" em `tabela_mapa_cadunico_criancas_0_a_4_2026` eram a razão CadÚnico/Censo (0,07 = 7%) e a população do Censo — não contagens do CadÚnico |

## Implementação

Critérios de aceite; "Resultado" preenchido ao fim (T4.3).

| # | Verificação | Critério | Resultado |
|---|---|---|---|
| V1 | Tabelas (`tabelas_finais/*cadunico*`) | nenhuma contagem do CadÚnico de 1 a 19 abaixo do município; nenhum percentual por bairro cujo numerador ou complemento seja < 20 |  **OK**: 5 tabelas por bairro — 0 contagens de 1 a 19, 0 complementos < 20, 0 bairros agregados com contagem; conjuntos: 3 (todas as idades), 2 (0-4), 5 (recortes: RA Lagoa, RA Ilha do Governador, AP 1, AP 2, AP 3) |
| V2 | Totais | soma dos bairros + conjuntos + sem bairro = total do município, em cada tabela |  **OK**: `cadunico_por_bairro_2026` e `..._ate_4_2026`: bairros + conjuntos + localidades + sem bairro = Total. Achado na implementação: 9 bairros de 0 a 4 (21 crianças) não fechavam 20 nem no município e ficavam vazios — Total − publicado revelaria 21; corrigido juntando a sobra ao menor conjunto (teste sintético cobre o caso) |
| V3 | Site (`index.html`, `data/*.js`) | mesma checagem de V1 nos tooltips e CSV de download; tooltip do agregado com o nome do conjunto |  **OK**: 4 mapas do CadÚnico no `data/charts.js` — menor contagem publicada 20/21, 0 abaixo de 20; tooltips "somado em Demais bairros da RA …" (10 e 16 nos de contagem) e taxa "(Demais bairros …)" (25 em cada de percentual); nota do mapa no site atualizada |
| V4 | Mapas | percentuais: bairros agregados com a taxa do conjunto; contagens: sem cor e marcados; nota no rodapé |  **OK**: PNG/A4 — percentuais com a taxa do conjunto, contagens sem cor; nota nova no rodapé (a antiga "… famílias suprimidos" saiu de `fonte_mapa_cadunico`) |
| V5 | PDF e DOCX | tabelas do apêndice com os conjuntos; nota na fonte |  **OK**: 3 tabelas do apêndice com as linhas "Demais bairros …" e a nota de agregação na fonte (bairros agregados não aparecem em linha própria); PDF compila, 0 `undefined`, 14 overfull; `valida_textos_publicados.py` sem frase ausente; nenhum texto curado cita bairro agregado |
| V6 | Outras saídas | saídas fora do CadÚnico idênticas (hash das PNG/CSV) |  **OK**: mudaram só as 5 tabelas e os 5 mapas do CadÚnico por bairro e o manifesto A4 (legendas); nenhuma outra PNG/CSV |
| V7 | Documentação | constituição §6, `CLAUDE.md`, ROADMAP (D3), CHANGELOG, README, especificação do projeto |  **OK**: constituição §6 (agregação, numerador/complemento, histórico), `CLAUDE.md`, ROADMAP (histórico `cdfacd2` no backlog Repositório), CHANGELOG, README, especificação do projeto (RF5, RNF2) |
