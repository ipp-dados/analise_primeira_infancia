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
| V1 | Tabelas (`tabelas_finais/*cadunico*`) | nenhuma contagem do CadÚnico de 1 a 19 abaixo do município; nenhum percentual por bairro cujo numerador ou complemento seja < 20 | |
| V2 | Totais | soma dos bairros + conjuntos + sem bairro = total do município, em cada tabela | |
| V3 | Site (`index.html`, `data/*.js`) | mesma checagem de V1 nos tooltips e CSV de download; tooltip do agregado com o nome do conjunto | |
| V4 | Mapas | percentuais: bairros agregados com a taxa do conjunto; contagens: sem cor e marcados; nota no rodapé | |
| V5 | PDF e DOCX | tabelas do apêndice com os conjuntos; nota na fonte | |
| V6 | Outras saídas | saídas fora do CadÚnico idênticas (hash das PNG/CSV) | |
| V7 | Documentação | constituição §6, `CLAUDE.md`, ROADMAP (D3), CHANGELOG, README, especificação do projeto | |
