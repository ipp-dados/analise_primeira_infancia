# SPEC — Site: exclusões e melhoria dos gráficos (`specs/website_graficos`)

> Rodada aberta em 2026-09-25, branch `spec/website-graficos` (a partir de `spec/relatorio-latex`, porque depende
> de `specs/exclusoes.md` e dos helpers novos de `analise.py`). Status: **planejamento — nada implementado.**
> Pedido do usuário: "Move the changes pertaining to the website to a different branch, we will plan those changes
> together with the roadmap feature of improving visualizations. Create the specs for validation before
> implementing." A validação (`validation.md`) foi escrita antes de qualquer código, de propósito.

## 1. Escopo

Duas fontes, planejadas juntas porque mexem nos mesmos gráficos:

**A. Exclusões já decididas** (`specs/exclusoes.md`, 2026-09-25), parte do site — o PDF já aplicou a dele:

| Código | No site | Onde (`website/build/build_site.py`, linhas em 2026-09-25) |
| :-- | :--- | :--- |
| E2 | tirar os subgrupos 1.2.1/1.2.2/1.2.3 das séries e cortes de **1 a 4 anos** | panorama por faixa (~l. 1223-1240), CAP × faixa × subgrupo (`_SLUG_SUBGRUPO`, ~l. 1246-1270) |
| E3 | tirar o subgrupo **1.1** (imunização) de todos os gráficos de subgrupo | séries por faixa (~l. 1190-1205), comparação 2025 (~l. 1206-1217), panorama (~l. 1223-1240), CAP (~l. 1246-1270), menores de 5 (~l. 1326-1335) |
| E4 | tirar os **mapas de óbitos maternos por bairro** (gravidez, puerpério) | ~l. 1136-1146 |
| E5 | **"Amarela e indígena"** numa série só, % recalculado dos absolutos | `RACA_LABEL`/`RACAS` e os 2 gráficos de raça (~l. 1104-1115) |
| E6 | tirar os **mapas de taxa de violência familiar por bairro**; ficam os de RA e a contagem por bairro | ~l. 1720-1732 |
| E7 | tirar **cobertura vacinal, anos selecionados** | ~l. 1550-1556 |
| E8 | tirar **frequência escolar absoluta por raça/cor e por sexo**; fica o total e as taxas | ~l. 1395-1405 |
| E9 | **alternância Taxa ↔ Óbitos** nos mapas de mortalidade por bairro, no lugar de dois cartões | neonatal (~l. 1162-1185) e raça/total (~l. 1117-1128) |

Mantidos por decisão explícita (não mexer): lesão autoprovocada; % de evitáveis por CAP de 1 a 4 anos; séries de
causas evitáveis por faixa; taxas neonatais por bairro.

**B. `improve charts`** (`specs/roadmap.md`, 2026-09-25) — a partir das regras de impressão do PDF
(`specs/relatorio_latex/specification.md` §5.1). Estado de cada item **no site hoje**, conferido no código:

| Item | Estado no site | Proposta |
| :--- | :--- | :--- |
| B1 Rótulos de eixo por extenso, com unidade | eixos sem título; unidade às vezes no nome da série ("Taxa (‰)") | título curto de eixo/unidade a partir do mesmo dicionário do PDF (`ROTULOS_EIXO`, Bloco 5 de `relatorio_latex`) |
| B2 Teto de cor P95 nos mapas de taxa/percentual por bairro | só nos mapas de violência (`teto=`) | todos os mapas contínuos por bairro; legenda "≥ X"; tooltip com o valor real (já é assim) |
| B3 Rótulos diretos seletivos | **já existe**: `endLabels`, `extremeLabels` em `js/charts.js` | revisar os limites (`maxDirectLabels`, `maxExtremeSeries`) e ligar nos gráficos de barras (valor na ponta) |
| B4 Pequenos múltiplos | não existe | nova opção (pill) nos gráficos de 8-11 séries: CAP × ano, imunobiológicos, subgrupos CID |
| B5 Paleta de dados | `--c1…--c11` do site (já mais escuros que o notebook em `--c3`/`--c6`) | validar `--c1…--c8` com o validador da skill `dataviz` contra `--surface`; trocar só os que falham, mantendo a ordem de matizes |
| B6 Fontes com referência completa | caixa "Fontes desta seção" com o texto curto de cada cartão | referência ABNT de `relatorio/latex/fontes.bib` (mesma lista "Fontes" do PDF) |
| B7 Linha `Total` como categoria | a conferir em todos os `bar_chart`/`grouped_bar_chart` | tirar linhas de total/subtotal antes de desenhar |
| B8 Eixo y das taxas | `zeroBase: False` em quase todas as séries de taxa | decidir com a equipe: base zero (regra do PDF) ou manter, com o corte visível |

## 2. Desenho da alternância Taxa ↔ Óbitos (E9)

- Um cartão só, com um **controle segmentado** ("Taxa" | "Óbitos") acima da coluna de pills; as pills (Precoce,
  Tardia, Pós-neonatal, Total) são as mesmas nos dois modos.
- Trocar o modo **mantém a pill selecionada** (Taxa · Tardia → Óbitos · Tardia) e troca o texto junto (cada mapa
  mantém sua própria semente de texto — os textos curados dos mapas de contagem continuam publicados no site).
- Padrão inicial: **Taxa** (é o que o PDF mostra).
- Gerador: `option_card_alternancia([("Taxa", entradas_taxa), ("Óbitos", entradas_obitos)], 'mapa')`, que emite os
  dois `option-card` dentro de um invólucro `.alterna` com o controle; JS novo em `js/charts.js` (~30 linhas), CSS
  em `css/components.css`. Sem mudança no motor de mapas.
- Acessibilidade: botões com `aria-pressed`, alcançáveis por teclado, foco visível (mesmo padrão das pills).
- Estimativa: simples (1 função no gerador, ~30 linhas de JS, ~20 de CSS).

## 3. Decisões para a sessão de planejamento

- **P1** — B8: base zero nas taxas do site ou manter o eixo ajustado?
- **P2** — B4: pequenos múltiplos como pill extra ou como substituto do gráfico de espaguete?
- **P3** — B5: se a validação reprovar cores do site, trocar agora ou só registrar?
- **P4** — ordem: exclusões (A) primeiro e deploy, depois B? (recomendado: A é decidido e pequeno)
- **P5** — B1 depende do dicionário `ROTULOS_EIXO` do Bloco 5 de `relatorio_latex`: esperar por ele ou criar aqui
  e o PDF reaproveitar?

## 4. Fora do escopo

- Mudar a ordem/estrutura das abas (continua fixa no gerador; `specs/estrutura_eixos.md` não é lido pelo site).
- Publicar: deploy só com OK explícito do usuário (skill `build_website`).
