# SPECIFICATION — Pendências (rodada de 2026-09-29)

Status: **planejada em 2026-09-29** (branch `planning`); implementação em `spec/pendencias`. O *como* está em
`plan.md`, as tarefas em `tasks.md`, os critérios de aceite em `validation.md`.

## 1. Contexto

Depois do merge de `spec/nova_estrutura` e `spec/apresentacao` em `staging_main` e do deploy do site (2026-09-29), o
`ROADMAP.md` foi reorganizado em **A fazer** × **Concluído**. O usuário pediu para resolver nesta rodada todas as
pendências que dependem só de nós: decisões abertas desde `specs/2026-09-25_website_graficos` (mapa duplicado, série
"Não informada", base zero, unidade do IPS), a exclusão E12 ainda não aplicada, os extras de tablet adiados pela
rodada mobile e o fechamento de rodadas anteriores. Numa das respostas, o usuário fixou também a **faixa etária padrão
do projeto** (D9), que passa a valer para todas as saídas.

## 2. Decisões (com o porquê)

As respostas vieram em três rodadas de perguntas agrupadas no planejamento e duas durante a implementação (D14-D18), todas em 2026-09-29.

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | O mapa de taxa de mortalidade infantil por bairro 2025 fica só no cartão de **raça/cor**; sai a pill "Total" (taxa e óbitos) do cartão neonatal e o `- mapa:` do item "Taxa de mortalidade na primeira infância" no PDF | os dois mapas são idênticos nos 167 códigos (conferido); duplicação confunde a leitura |
| D2 | A série "Não informada" sai do gráfico de **taxa** de mortalidade infantil por raça/cor (site, PDF, `analise.py`); fica no de contagem e nas tabelas | óbitos sem raça (SIM) ÷ nascidos sem raça (SINASC) não é taxa comparável; chega a 89‰ e achata as outras séries |
| D3 | Base zero (P1) mantida em todas as taxas, **exceto o percentual de baixo peso ao nascer** | a variação real (9%-11%) some com base zero |
| D4 | E12 aplicado: amarela + indígena agregadas na taxa de frequência escolar por raça/cor | grupos pequenos, taxas de 0% e 100%; mesma regra de E5 (somar absolutos, recalcular) |
| D5 | Extras de tablet (720-1099 px): alvos de toque ≥ 44 px e texto dos gráficos ≥ 11 px, as metas do celular | adiados pela rodada mobile, que só fixou a meta no celular; lá o tablet ficou com alvos < 44 px e texto de gráfico entre 9,5 e 11 px (`specs/2026-09-28_website_mobile/validation.md`, "Fora da meta"). O planejamento desta rodada leu "entre 9,5 e 11 px" como meta; corrigido na implementação |
| D6 | IPS: unidade "por 100 mil habitantes" **confirmada**; o tratamento do Centro como outlier fica **só na apresentação** | convenção do IPS Rio; site e PDF já usam o teto P95 |
| D7 | Branch `waleska-analise-primeira-infancia` **superada** (os 2 commits de 2026-09-22 não serão mesclados); tag + remoção só com OK | o usuário pediu para não apagar agora |
| D8 | PDF e deploy do site: preparar tudo; publicar só com OK do usuário | idem |
| D9 | **Faixa padrão do projeto: 0 a 5 anos (até 72 meses).** Qualquer uso da idade de 6 anos leva nota explícita | padronizar as fontes (CadÚnico, SISVAN, Censo Escolar já são 0-5); E12 só tem numerador absoluto até 5 anos |
| D10 | A apresentação troca `mapa_taxa_mortalidade_infantil_bairro_2025` por `mapa_taxa_obitos_raca_total_bairro_2025` | mesmos valores; mesma figura do site e do PDF |
| D11 | Textos curados afetados: ajustamos só o trecho afetado e marcamos `revisar` em `relatorio/controle_revisao.json` | a equipe revisa no próximo update |
| D12 | Eixo cortado: duas barras inclinadas no pé do eixo y **e** a nota "eixo não começa em zero" na fonte | o corte precisa ser visível e dito por escrito |
| D13 | **Sem cabeçalho `Expires` próprio** no site (pergunta do usuário, 2026-09-29) | conferido no ar: o GitHub Pages já manda `expires` + `Cache-Control: max-age=600`, `ETag` e `Last-Modified` em todo arquivo, sem como configurar (não há `_headers`); o problema real (HTML novo com CSS/JS velhos) já está resolvido pelo `?v=<hash>` de `css/`/`js/`/`data/` (`specs/2026-09-28_website_bugfix`). Resta só `assets/` sem versão: imagem trocada com o mesmo nome pode ficar até 10 min velha, aceitável. `<meta http-equiv="Expires">` não afeta o cache de CSS/JS/imagens nos navegadores atuais |
| D14 | Taxa de frequência escolar: **taxas publicadas do IBGE (SIDRA 10056)** para 0 a 5 anos; grupos agregados e o "Total 0 a 5 anos" = Σ(taxa × população SIDRA 9606) ÷ Σ população | pergunta de 2026-09-29 durante a implementação: frequentam (10057) ÷ população (9606) dá taxas acima de 100% (Amarela 106,9%, homens 100,2% aos 5 anos) e até 10,7 p.p. longe da 10056 — as tabelas vêm de bases diferentes do Censo. Assim, cada grupo continua igual ao publicado pelo IBGE e a agregação soma "absolutos estimados", nunca média simples de taxas |
| D15 | E12: "Amarela e indígena" **só no total 0 a 5 anos** (tabela e nota do gráfico), fora das barras por idade; os dois grupos saem do gráfico por idade | mesmo somados são 89 a 125 crianças por idade (631 no total): 0% aos 0 anos e 100% aos 4 |
| D16 | O gráfico "PNAD Contínua" (`pnad_frequencia_escolar_por_idade`) traz exatamente os números do Censo 2022 (tabela 10056): **fonte corrigida e duplicata tirada** — o item do catálogo passa a usar a taxa total por idade do Censo, 0 a 5 anos (`sidra_taxa_frequencia_0_5_total_2022`), e o texto curado vai junto (marcado `revisar`); E15 em `specs/exclusoes.md` | conferido: 8,04; 30,28; 55,19; 71,99; 82,92; 90,57 = coluna Total da 10056; a regra "acrescentar, nunca remover" (`nova_estrutura`) mantém o item com figura |
| D17 | Apresentação: o número-âncora passa a ser **0 a 5 anos (Ripsa 2025)**; 0 a 6 anos (469 mil) só numa nota ("a política fala em até 6 anos") | D9 prevalece sobre a âncora de 469 mil escolhida em `specs/2026-09-28_apresentacao`; coerência com site e PDF |
| D18 | Subtítulos do crosswalk (títulos do PDF) com "até 6 anos" passam a "**até 72 meses**"; o nome do catálogo fica na `nota` | substitui C-D2 (`specs/2026-09-24_populacao-referencia/auditoria_faixas.md`), que mantinha o nome do catálogo no título |

## 3. Requisitos

**R1 — Mapa duplicado (D1).** Site: cartão neonatal com 3 pills (Precoce, Tardia, Pós-neonatal) nos dois modos. PDF e
DOCX: o item "Taxa de mortalidade na primeira infância" sem o mapa, com `- nota:` de exclusão. `specs/exclusoes.md`
ganha **E13** (o que saiu, por quê, como voltar). O PNG continua sendo gerado por `analise.py`. O texto curado
`mapa_taxa_mortalidade_infantil_bairro_2025` vira órfão (apêndice do DOCX).

**R2 — "Não informada" (D2).** Gráfico de taxa por raça/cor com 4 séries (Branca, Parda, Preta, Amarela e indígena) no
site, no PNG de tela e no A4; a fonte/legenda diz que a categoria está no gráfico de contagem. Gráfico de contagem e
tabelas inalterados. `specs/exclusoes.md` ganha **E14**.

**R3 — Eixo cortado (D3, D12).** Só `nascidos_abaixo_peso_percentual_por_ano`, em três lugares: `analise.py` (tela),
A4 (PDF) e site. Eixo y começa perto do mínimo, com as duas barras inclinadas no pé do eixo e "eixo não começa em
zero" na fonte. O comportamento padrão de todas as funções de gráfico não muda (parâmetro opcional).

**R4 — Faixa 0-5 (D9) e E12 (D4).**
- Regra em `specs/constitution.md` e na convenção de faixas do `CLAUDE.md`.
- As saídas publicadas que hoje vão a 6 anos passam a ir a 5: população do Censo 2022 por sexo e por raça/cor
  (SIDRA 9606), taxa de frequência escolar por sexo e por raça/cor, e a série Ripsa por idade. Onde a fonte traz
  6 anos, a coluna/linha pode ficar na tabela bruta com nota, mas não nos gráficos nem nos números citados.
- Taxa de frequência escolar recalculada dos absolutos: frequentam (SIDRA 10057, 0-5) ÷ população (SIDRA 9606, 0-5),
  por idade, sexo e raça/cor; "Amarela e indígena" = soma dos absolutos dos dois grupos; "Total" = 0 a 5 anos.
- Títulos e rótulos que dizem "até 6 anos" passam a dizer "0 a 5 anos" (crosswalk, site, PDF, deck); o nome do
  indicador no catálogo da equipe fica citado em nota.
- **Nomes de arquivo mantidos** (`*_0_6_*`): são chaves do texto curado, do crosswalk e da apresentação.
- `specs/exclusoes.md`: E12 marcado como aplicado.

**R5 — Tablet (D5).** Na faixa 720-1099 px: alvos de toque ≥ 44 px e texto dos gráficos ≥ 11 px (hoje entre 9,5 e 11). Desktop
(≥ 1100 px) pixel a pixel idêntico, fora dos gráficos alterados por R1-R4; celular sem regressão.

**R6 — Registro (D6, D7).** Unidade do IPS registrada como confirmada; Centro "só no deck" registrado na rodada da
apresentação; D7 no `ROADMAP.md`.

**R7 — Deck (D10).** Slide de mortalidade infantil por bairro com o mapa de raça/cor; deck regerado (sem `--publicar`
até o OK de D8) com os rótulos 0-5 de R4.

**R8 — Textos (D11).** Ajustar só o trecho afetado e marcar `revisar`: `percentual_mortalidade_raca_ano`,
`nascidos_abaixo_peso_percentual_por_ano` (se citar a escala), `sidra_taxa_frequencia_0_6_raca_2022`,
`sidra_taxa_frequencia_0_6_sexo_2022`, `censo_sidra_populacao_0_6_{raca,sexo}_2022` e qualquer outro que cite 6 anos
ou números que mudarem. As notas de curadoria espelhadas em `analise.py` acompanham.

**R9 — Fechamento de rodadas anteriores.** `nova_estrutura` T6.3 e `apresentacao` T5.2 atualizados (merge feito);
nota de fechamento em `specs/2026-09-25_relatorio_latex/tasks.md` (caixas de trabalho feito; T3.3/T4.3 no backlog).
Specs são história: nada é reescrito, só acrescentado.

**R10 — Documentação.** `CHANGELOG.md`, `docs/especificacao_projeto.md` (conferir a §11), `ROADMAP.md`, `CLAUDE.md`
(faixa 0-5; exceção à base zero), `relatorio/specs.md` (exceção à P1 no site).

## 4. Fora do escopo

- Publicar o PDF (`--publicar`), fazer o deploy do site, publicar o deck, criar as tags `rodada/*` e apagar branches —
  só com OK do usuário (D7, D8).
- Itens de "Aguardando equipe/usuário" do `ROADMAP.md` (lorem, alertas de curadoria que não sejam os de R8, os 6
  trechos `revisar` do deck, teste em aparelho real).
- Próximas features (fase 1c, estimativa Ripsa por bairro, empacotamento) e o backlog.
- Recortes do CadÚnico e do SISVAN: já são 0-5 na prática (`auditoria_faixas.md`); só os rótulos mudam, se disserem 6.
- Renomear arquivos `*_0_6_*`.
