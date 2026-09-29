# Rodada `pendencias` — plano

Aberta em 2026-09-29 a partir de `planning` (reorganização do `ROADMAP.md`, commit `c5c732e`). Objetivo: resolver
todas as pendências que dependem só de nós (seção "Rodada atual" do `ROADMAP.md`). Branch de trabalho:
`spec/pendencias`, criada a partir de `planning`; merge em `planning` e `staging_main` ao fim.

Decisões do usuário (2026-09-29, perguntas agrupadas): ver `ROADMAP.md` → Concluído e a tabela D abaixo.

## D — decisões já tomadas

| # | Decisão | Origem |
| :-- | :--- | :--- |
| D1 | Mapa de taxa de mortalidade infantil por bairro: fica no cartão de **raça/cor**; sai do cartão neonatal | pergunta 2026-09-29 |
| D2 | Série "Não informada" sai do gráfico de **taxa** por raça/cor; fica no de contagem | idem |
| D3 | Base zero mantida em todas as taxas, **exceto baixo peso ao nascer** (eixo cortado, corte visível) | idem |
| D4 | E12: agregar amarela + indígena na taxa de frequência escolar por raça/cor | `specs/exclusoes.md` (2026-09-25) |
| D5 | Extras de tablet da rodada mobile entram nesta rodada | pergunta 2026-09-29 |
| D6 | IPS: unidade "por 100 mil habitantes" confirmada; Centro como outlier só na apresentação | idem |
| D7 | Branch `waleska-analise-primeira-infancia` superada; tag + remoção só com OK do usuário | idem |
| D8 | PDF e deploy do site: preparar tudo, publicar só com OK do usuário | idem |
| D9 | **Faixa padrão do projeto: 0 a 5 anos (até 72 meses).** Onde a idade de 6 anos for necessária, nota explícita. E12 passa a usar os absolutos reais (0-5) | resposta à Q1, 2026-09-29 |
| D10 | Apresentação troca o mapa pelo `mapa_taxa_obitos_raca_total_bairro_2025` | Q2 |
| D11 | Textos curados afetados: ajustamos só o trecho afetado e marcamos `revisar` | Q3 |
| D12 | Eixo cortado: duas barras inclinadas no pé do eixo y **e** nota "eixo não começa em zero" na fonte | Q4 |

## Levantamento (o que o código faz hoje)

- **Mapa duplicado (D1).** Conferido em 2026-09-29: `taxa_mortalidade_infantil` de
  `mortalidade_infantil_pos_neonatal_total_bairro_ano.csv` e `obitos_total / nascidos_total × 1000` de
  `mortalidade_raca_bairro_ano.csv` são **idênticos nos 167 códigos** de 2025 (diferença máxima 7e-15).
  - site: `website/build/build_site.py`, cartão neonatal (`_mapas_neo_taxa` e `_mapas_neo_obitos`, pill "Total" nos dois
    modos: `mapa_taxa_mortalidade_infantil_bairro_2025` e `mapa_mortalidade_infantil_bairro_2025`); o de raça/cor é o
    cartão "Mortalidade infantil por bairro" (`mapa_taxa_obitos_raca_total_bairro_2025`, alternância Taxa/Óbitos);
  - PDF/DOCX: `specs/estrutura_eixos.md`, item "Taxa de mortalidade na primeira infância" (`- mapa:
    mapa_taxa_mortalidade_infantil_bairro_2025.png`);
  - apresentação: `apresentacao/apresentacao.md:336` usa `fig:mapa_taxa_mortalidade_infantil_bairro_2025` (ver Q2);
  - texto curado órfão: `textos_curados.json` → `mapa_taxa_mortalidade_infantil_bairro_2025` (já tinha o alerta "cita
    os números da taxa pós-neonatal").
- **"Não informada" (D2).** `analise.py` §mortalidade por raça: `rotulos_raca` serve aos dois gráficos
  (`obitos_raca_ano` e `percentual_mortalidade_raca_ano`); site: `RACAS` serve aos dois pills do cartão "Mortalidade
  infantil por raça/cor". As tabelas (`mortalidade_raca_municipio_ano.csv`, apêndice do PDF) continuam com a coluna.
  O texto curado de `percentual_mortalidade_raca_ano` comenta a categoria "não informada" (ver Q3).
- **Baixo peso (D3).** Um gráfico só: `nascidos_abaixo_peso_percentual_por_ano` (`analise.py` ~l. 993, `serie_temporal`;
  A4 por `_a4_serie_unica` em `primeira_infancia/impressao.py`, com `set_ylim(0, …)`; site: `line_chart` no eixo
  Alimentação, `build_site.py` ~l. 1990). O JS (`website/js/charts.js` l. 92-96) já aceita `zeroBase:false`, mas sem
  marca de corte. O mapa de percentual já é contínuo e não muda.
- **E12 (D4).** Taxa publicada: `sidra_taxa_frequencia_0_6_raca_2022.csv` (SIDRA 10056, 0-6 anos, só percentuais).
  Absolutos disponíveis: frequentam (SIDRA 10057, **0-5 anos**, `sidra_frequencia_escola_0_5_raca_2022.csv`) e
  população (SIDRA 9606, 0-6, `censo_sidra_populacao_0_6_raca_2022.csv`). Não há numerador absoluto para **6 anos** —
  ver Q1. Consumidores: `analise.py` (~l. 2385, tela + A4), `build_site.py` l. 1750-1755, `tabelas.py` (apêndice).
- **Tablet (D5).** `website/css/mobile.css` já separa tablet (720-1099 px) e celular; faltam alvos de 44 px no tablet
  e texto dos gráficos de viewBox fixo entre 9,5 e 11 px (`specs/2026-09-28_website_mobile`, adiado).

## Blocos

**B0 — Abertura.** Branch `spec/pendencias` a partir de `planning`; `specification.md` (decisões + respostas Q1-Q4),
`tasks.md`, `validation.md`. Linha de base: screenshots do site (desktop ≥ 1100 px, tablet 800 px, celular 390 px,
Playwright) e contagem de figuras/tabelas do PDF (hoje 94 figuras, 43 tabelas).

**B1 — Mapa duplicado (D1).** Tirar a pill "Total" dos dois modos do cartão neonatal no site; tirar o `- mapa:` do
crosswalk com `- nota:` de exclusão; nova linha **E13** em `specs/exclusoes.md` (como voltar). O PNG continua sendo
gerado por `analise.py`; a apresentação troca para o mapa de raça/cor (D10). Texto curado vira órfão (fica no apêndice do DOCX).

**B2 — "Não informada" fora da taxa (D2).** `analise.py`: dicionário próprio para o gráfico de taxa, sem
`nao_informado` (tela e A4); site: lista de séries do pill "Taxa por raça/cor" sem `nao_informado`; nota na fonte/
legenda dizendo que a categoria está só no gráfico de contagem. Linha **E14** em `specs/exclusoes.md`.

**B3 — Eixo cortado no baixo peso (D3, D12).** Parâmetro opcional `base_zero=True` em `serie_temporal` e
`_a4_serie_unica` (padrão inalterado, para o resto ficar idêntico); com `False`, eixo começa perto do mínimo e desenha
a marca de corte (duas barras inclinadas no eixo y). No site, `opts.eixoCortado` no `line_chart` → `zeroBase:false`
+ marca de corte em `js/charts.js`, também nos pequenos múltiplos se o gráfico aparecer neles. Registrar a exceção
à regra P1 em `specs/constitution.md`/`relatorio/specs.md` (onde a P1 está documentada).

**B4 — Faixa 0-5 (D9) e E12 (D4).**
- Regra nova em `specs/constitution.md` (e `CLAUDE.md`, convenção de faixas): faixa padrão 0 a 5 anos (até 72 meses);
  6 anos só com nota. Registrar em `specs/2026-09-24_populacao-referencia/auditoria_faixas.md` como nova entrada.
- Saídas que hoje vão a 6 anos, convertidas para 0-5 (a linha "6 anos" sai do gráfico; fica na tabela bruta quando a
  fonte a traz, com nota): `censo_sidra_populacao_0_6_{raca,sexo}_2022`, `sidra_taxa_frequencia_0_6_{raca,sexo}_2022`,
  a série Ripsa por idade simples (a tabela já traz o total 0-5). **Nomes de arquivo mantidos** (são as chaves do
  texto curado, do crosswalk e da apresentação), como já feito em `percentual_mortalidade_raca_ano`.
- Taxa de frequência por raça/cor e por sexo recalculada dos absolutos: frequentam (SIDRA 10057, 0-5) / população
  (SIDRA 9606, 0-5); "Amarela e indígena" = soma dos absolutos dos dois grupos, recalculada (como E5); o "Total"
  passa a ser 0-5 de verdade (resolve também o alerta da curadoria sobre a linha "Total" da 10056, que era de todas
  as idades). Conferir a taxa recalculada contra a 10056 idade a idade (diferenças esperadas pequenas; registrar).
- Títulos/rótulos "até 6 anos" do crosswalk e do site passam a dizer a faixa real ("0 a 5 anos"), sem mudar a chave
  dos itens; o nome do indicador no catálogo da equipe fica citado na nota.
- Consumidores: `analise.py` (tela + A4), `build_site.py`, `tabelas.py`, `apresentacao/build/numeros.py` (números
  `{{n:...}}` que usem 0-6). Marcar E12 como aplicado em `specs/exclusoes.md`.

**B5 — Tablet (D5).** Só `css/mobile.css` (faixa 720-1099 px) e, para o texto dos gráficos, o redesenho em largura
real de `js/charts.js` já usado no celular. **Desktop pixel a pixel idêntico** (comparação com a linha de base).

**B6 — Documentação das decisões (D6-D7).** Unidade do IPS registrada como confirmada (spec do Proteção / site, sem
ressalva); Centro "só no deck" registrado em `specs/2026-09-28_apresentacao`. Fechamentos: `nova_estrutura` T6.3 e
`apresentacao` T5.2 (merge feito; tags ficam para o OK de D7); nota de fechamento em
`specs/2026-09-25_relatorio_latex/tasks.md` (caixas de trabalho feito; T3.3/T4.3 → backlog do PDF, já no ROADMAP).

**B7 — Regerar e validar.** Rodar as células afetadas de `analise.py` (DataSUS e SIDRA são arquivos locais; não precisa
do banco do CadÚnico), com `GERA_VARIANTE_A4`; `build_site.py`; `gera_latex.py` **sem** `--publicar`; DOCX de
curadoria. Validação em `validation.md`:
- desktop do site idêntico fora dos 4 gráficos/cartões alterados; tablet e celular sem regressão;
- PDF: 94 → 93 figuras (sai 1 mapa), 43 tabelas, nenhuma outra figura a menos;
- faixa 0-5: nenhum gráfico/rótulo publicado com "6 anos" sem nota (busca em site, PDF gerado e deck);
- `analise.py`: as saídas não tocadas continuam idênticas (hash das PNGs/CSVs antes × depois, como na
  `organizacao`);
- textos: lista dos textos curados afetados (Q3) com o status em `controle_revisao.json`.

**B8 — Fechamento.** `CHANGELOG.md`, `docs/especificacao_projeto.md` (§11), `ROADMAP.md`, `CLAUDE.md` se a regra de
base zero mudar lá; merge `spec/pendencias` → `planning` → `staging_main`. **Publicação do PDF, deploy do site, tags e
limpeza de branches só com OK do usuário (D7, D8).**

## Perguntas (respondidas em 2026-09-29)

- Q1 — E12, 6 anos sem numerador absoluto → **D9** (padronizar 0-5 no projeto todo; nota quando precisar de 6).
- Q2 — mapa da apresentação → **D10** (trocar).
- Q3 — textos curados afetados (`percentual_mortalidade_raca_ano`, `sidra_taxa_frequencia_0_6_raca_2022`,
  `nascidos_abaixo_peso_percentual_por_ano`, e agora também os de população e frequência 0-6 que citem 6 anos) → **D11**.
- Q4 — marca de corte → **D12**.
