# Especificação — Inclusão dos dados do eixo Proteção (`specs/2026-09-23_inclusao_dados_protecao`)

Branch: `inclusao_dados_protecao`
Status: **rascunho 2 para revisão** — decisões D1, D2/D3b e D4 incorporadas (§9); nenhum código escrito.
Desdobramento: `plan.md` (blocos), `tasks.md` (checklist), `validation.md` (critérios).
Complementa `inventario_dados.md` (formato dos arquivos e decisões da abertura da rodada).
Pasta de dados renomeada para `dados_locais/protecao/` (sem acento).

> **Restrição herdada de `specs/2026-09-08_mortalidade-ap` e `specs/2026-09-22_ajuste_eixos`: só se acrescenta.**
> Nenhuma função, assinatura, constante, célula ou saída já existente é alterada. As únicas
> "edições" em código existente são **chaves novas em dicionários de configuração** (um novo nível
> geográfico `ra`, um novo tema de cor) — mesmo tipo de exceção autorizada para `'cap'`. Ver §7.

---

## 1. Objetivo

Preencher o eixo **🛡️ Proteção**, hoje 100% `pendente` em `specs/estrutura_eixos.md`, com os três
conjuntos de dados de `dados_locais/protecao/`, e levar o resultado a `analise.py`, a
`relatorio/index.html`, ao PDF e ao DOCX de curadoria — **sem quebrar o que já funciona** — e
publicar no GitHub Pages **somente após validação** (§8).

Fora de escopo: itens do catálogo sem dado fornecido (tipificação, recortes <1 ano vs 1-5) —
ficam `pendente` (§6), pois **o usuário tentará extrair os dados faltantes do Tabnet** (ver
abaixo). O item "Territórios com risco a inundação/movimento de massa (SGB)" está
**removido da V1** do relatório (§6, §10). A **taxa de notificações** passa a ser derivada (D1, §5.1 T7).

---

## 2. Fontes (resumo — detalhes em `inventario_dados.md`)

| Fonte | Arquivo | Nível | Período | Natureza |
|---|---|---|---|---|
| Sinan NET / Tabnet | `violencia_familiar/` (7 CSVs por vínculo, extraídos do zip original) | bairro de residência | 2011-2026 | contagem absoluta, 0-5 anos |
| Sinan NET / Tabnet | `notif_viol_ interpes_ autoprovocada_...csv` | bairro de residência | 2018-2026 | contagem absoluta; **só lesão autoprovocada** (40 casos, 33 em 2026 — 2026 é o ano de referência **desta** série, D3b) |
| Data.Rio / IPS 2024 | `violencia_territorial.xlsx` | **Região Administrativa (RA)** | 2024 | 3 taxas, todas as idades |

Achados relevantes já verificados nesta rodada:
- Todos os códigos de bairro do Sinan existem em `limite_bairros_rio.geojson` (`codbairro`) —
  o join numérico do projeto funciona sem casamento por nome.
- Na série de mãe e pai há um salto em 2017 (mãe 600→1514, pai 371→1261) e um vale em 2019-2020:
  possível mudança de ficha/notificação → nota metodológica obrigatória.
- Vínculos **não são exclusivos**: não existe "total de violência familiar" e **não se soma** os
  7 vínculos (dupla contagem). O catálogo pede "< 1 ano / 1-5", mas os arquivos são 0-5 agregado.
- O catálogo (`Fonte: ISP`, nível "R.A. ou bairro", início da série 2014) diverge do dado real
  (Data.Rio/IPS, só RA, só 2024; Sinan desde 2011) → corrigir `fonte`/`nota` em `estrutura_eixos.md`.

---

## 3. ⚠️ Incorporação da Região Administrativa (RA) como nível geográfico

**Precisamos incorporar a RA ao projeto como já foi feito com AP, RP e CAP** — o `violencia_territorial.xlsx`
só existe nesse nível, e as agregações do Sinan por RA (§5, T3) também dependem dele.

### 3.1 Geometria: não há arquivo novo a commitar
`limite_bairros_rio.geojson` já traz `codra` (numérico) e `regiao_adm` (nome). Verificado:
33 RAs (códigos 1-31, 33, 34; **não existe RA 32**), 166 bairros, cada bairro com um `codra`.
A RA é obtida por `dissolve(by='codra')` — o mesmo mecanismo de `'ap'`/`'rp'` em
`mapa_coropletico_bairros` (diferente da CAP, que exigiu geojson próprio). Sem novo arquivo em
`dados_locais/geo/` (que **não** é gitignored).

### 3.2 Chave de junção: `codra` numérico, nunca o nome
Regra do projeto: chave numérica, nunca nome (grafias divergem — o IPS escreve `SÃO CRISTÓVÃO`,
o geojson `SAO CRISTOVAO`; `SANTA TERESA` vs `SANTA TEREZA`). O xlsx traz **numeral romano + nome**;
o numeral é o `codra` (I=1 … XXXIV=34). Verificado: 32 dos 33 `codra` do geojson casam; a única RA
sem dado no IPS é **XXI Paquetá** (aparece "Sem dado" no mapa — comportamento já existente da função).
O nome do xlsx é usado só como verificação cruzada (asserção), não como chave.

### 3.3 O que a RA muda, ponto a ponto (todos aditivos)

| Local | Mudança |
|---|---|
| `analise.py` `_NIVEIS_AGREGACAO` | + `'ra': {'coluna_geo': 'codra', 'tipo': int}` (mesma exceção de `'cap'`; níveis existentes intocados) |
| `analise.py` `mapa_coropletico_bairros` | **nenhuma alteração de código** — `nivel='ra'` funciona via a mesma ramificação `dissolve` de AP/RP; só o docstring ganha a menção |
| `analise.py` `agrega_bairros_por_nivel` | nenhuma — já é genérica via `_NIVEIS_AGREGACAO` (bairro→RA: somar contagens absolutas) |
| `build_html_report.py` | + `"ra"` em `_NIVEL_COL` (`codra`), `_NIVEL_LABEL` (`"RA"`), `_geo_nivel` (ramo dissolve, rótulo = nome da RA a partir de `regiao_adm`) e `_chave_norm` (int). **Esta é a parte que mais facilmente é esquecida**: o HTML tem geometria própria, independente de `analise.py` |
| `.claude/skills/generate_map/SKILL.md` | documentar `nivel='ra'` e a chave `codra` |
| `CLAUDE.md` | uma linha ao lado de AP/CAP: RA (Região Administrativa, 33 no geojson de bairros) **≠** AP **≠** CAP |
| `_RA_PARA_CAP` (já existe) | reaproveitado para agregar RA→CAP no T3/séries por CAP, sem redefinir |

Cuidado de nomenclatura: `'ap'`, `'cap'`, `'rp'` e agora `'ra'` são quatro fronteiras distintas.

### 3.4 Validação específica da RA (vira item de `validation.md`)
- Asserção: 33 RAs dissolvidas; 32 casadas com o xlsx; a diferença é exatamente {21 Paquetá}.
- Asserção: nome romano→número do xlsx ≡ `regiao_adm` normalizado (sem acento) para todas as 32.
- Mapa de RA de teste renderizado e conferido visualmente contra o mapa de bairros.
- Regressão: `nivel='bairro'|'ap'|'rp'|'cap'` geram os mesmos PNGs de antes (checksum, §7.2).

---

## 4. Funções novas em `analise.py` (bloco "Pacotes e Funções Auxiliares")

Toda lógica reutilizável vai lá; as seções de análise só chamam. Nomes seguem o padrão existente
(`carrega_*`, `agrega_*`). Assinaturas são proposta:

| Função | Faz |
|---|---|
| `carrega_sinan_bairro(origem, categoria, anos_validos)` | Lê 1 export Sinan (CSV, latin-1, 6 linhas de metadados), formato largo → longo, remove `Total`, separa `codigo`/`bairro`, **reindexa numa grade bairro × ano completa preenchendo 0** (colunas de ano esparsas) — mesma ideia de `carrega_raca_bairro` |
| `carrega_violencia_familiar(pasta, anos_validos)` | Chama a anterior para os 7 vínculos e devolve um único longo (`vinculo`, `codigo`, `bairro`, `ano`, `casos`); agrupa `outros` = padrasto + irmão(ã) + cônjuge + ex-cônjuge + filho(a) (ver D6 sobre dupla contagem) |
| `carrega_violencia_territorial_ra(caminho)` | Lê o xlsx (pula cabeçalho Data.Rio), extrai `codra` do numeral romano, valida contra `regiao_adm` do geojson, devolve `codra`, `regiao_adm`, 3 taxas; linha "RIO DE JANEIRO" separada como referência municipal |
| `numeral_romano_para_int(s)` | auxiliar do de-para RA |
| `taxa_por_mil(df, col_casos, col_pop)` | recalcula a taxa **depois** de somar numerador e denominador no nível (nunca média de taxas), regra do projeto |
| `carrega_pop_0_4_bairro()` | denominador por `codbairro` a partir de `df_censo['0 a 4 anos']` / `dados_locais/censo/pop_censo_2022_datario.csv` (esse arquivo já traz `codra`) — **reaproveita o que existe, sem nova leitura** (ver D9) |
| `bairro_para_nivel(df, nivel)` | anexa `codra` / `cod_ap_sms` (via `_RA_PARA_CAP`) / `cod_rp` a uma tabela por bairro, a partir do geojson — para agregar contagens (soma de numeradores, nunca média de taxa) |

Além disso, chaves de configuração novas: `'ra'` em `_NIVEIS_AGREGACAO` (§3.3) e um tema de cor
para Proteção em `_CORES_TEMA_MAPA` (proposta: sequencial `OrRd`; `RdPu` já é mortalidade —
decisão D5).

Uma seção nova **"🛡️ Proteção"** de análise é inserida **antes** da seção final "Análise / Relatório"
(markdown-only) — ordem técnica de build, coerente com `specs/2026-09-22_ajuste_eixos`; a apresentação por eixo
continua vindo de `estrutura_eixos.md`.

---

## 5. Lista final proposta de tabelas, gráficos e mapas (para revisão)

Convenções: contagens absolutas → `bins` discretos; taxas → colorbar contínua; todo item cita
`fonte_dados`; anos fechados 2011-2025 (2026 excluído, D3); mapas de bairro usam 2025 (D2);
CSVs em `tabelas_finais/`, PNG em `visualizacoes/`/`mapas/`; cada mapa gera seu gêmeo
`tabela_mapa_*.csv` automaticamente.

**Legenda de origem:** 🅰 pedido do catálogo (item em aberto) · 🅱 item novo proposto por relevância ·
**[?]** depende de decisão (§9).

### 5.1 Tabelas (`tabelas_finais/`)

| ID | Arquivo | Conteúdo | Origem / item em aberto |
|---|---|---|---|
| T1 | `violencia_familiar_por_vinculo_ano.csv` | município × vínculo (mãe, pai, padrasto, irmão(ã), cônjuge, ex-cônjuge, filho(a), + `outros`) × ano 2011-2025 | 🅰 Violência familiar |
| T2 | `violencia_familiar_por_bairro.csv` | bairro (`codbairro`) × {mãe, pai, outros} × ano, grade completa com zeros | 🅰 Violência familiar (base dos mapas) |
| T3 | `violencia_familiar_por_ra.csv` e `violencia_familiar_por_cap.csv` | T2 agregada por `codra` e por CAP (soma de contagens; taxa recalculada após somar casos e população) | 🅱 habilita cruzar com IPS por RA e comparar com Saúde por CAP |
| T4 | `violencia_familiar_outros_detalhe.csv` | composição de "outros" (padrasto, irmão(ã), cônjuge, ex, filho(a)) por ano | 🅱 transparência do agrupamento "outros" |
| T5 | `notif_autoprovocada_por_bairro_ano.csv` | bairro × ano 2018-2026, 2026 marcado como parcial (D3b) | 🅰 Notificações interpessoal/autoprovocada (**parcial**: só autoprovocada) |
| T7 | `violencia_familiar_taxa_por_bairro.csv` | bairro × {mãe, pai, outros}: casos 2025, pop. 0-4 (Censo 2022), **taxa por 1.000** (D1/D9) | 🅰 Taxa de notificações de violência (**com ressalva D9**) |
| T6 | `violencia_territorial_por_ra_2024.csv` | `codra`, `regiao_adm`, taxa de homicídios, homicídios por ação policial, homicídios de jovens negros; linha de referência do município | 🅰 Violência territorial |

### 5.2 Gráficos (`visualizacoes/`)

| ID | Arquivo | Conteúdo | Origem |
|---|---|---|---|
| G1 | `violencia_familiar_serie_vinculos.png` | série temporal 2011-2025: mãe, pai, outros; **anotação de possível quebra em 2017** | 🅰 Violência familiar ("gráfico de linha") |
| G2 | `violencia_familiar_outros_serie.png` | série dos vínculos que compõem "outros" | 🅱 |
| G3 | `violencia_familiar_top_bairros_2025.png` | 10 bairros com mais casos (mãe e pai, barras agrupadas) | 🅱 **[?] pode ser redundante com M1/M2** |
| G4 | `violencia_territorial_taxa_homicidios_ra_2024.png` | barras por RA ordenadas, linha do município | 🅰 Violência territorial |
| G5 | `violencia_territorial_homicidios_acao_policial_ra_2024.png` | idem | 🅰 |
| G6 | `violencia_territorial_homicidios_jovens_negros_ra_2024.png` | idem | 🅰 |
| G7 | `notif_autoprovocada_antes_2026_vs_2026.png` | barras comparando o total 2018-2025 (7 casos) com 2026 (33 casos, ano parcial) e nota sobre a possível mudança de registro administrativo | 🅰 (D3b, pedido do usuário) |
| G8 | `violencia_familiar_taxa_top_bairros_2025.png` | 10 maiores taxas por 1.000 (mãe/pai) | 🅱 **[?] só se as taxas de bairro forem legíveis (D8)** |

O catálogo prevê "gráfico de linha" também para Violência territorial; com **um único ano (2024)**
não existe série — G4-G6 (barras) substituem; registrar em `nota`.

### 5.3 Mapas (`mapas/`)

| ID | Arquivo | Nível / escala | Origem |
|---|---|---|---|
| M1 | `mapa_violencia_familiar_mae_bairro_2025.png` | bairro; contagem, `bins` | 🅰 Violência familiar |
| M2 | `mapa_violencia_familiar_pai_bairro_2025.png` | bairro; contagem, `bins` | 🅰 |
| M3 | `mapa_violencia_familiar_outros_bairro_2025.png` | bairro; contagem, `bins` (**[?] D2:** 2025 ou acumulado 2021-2025 — em 2025 "outros" tem só ~110 casos, ~50 bairros com dado) | 🅰 |
| M7 | `mapa_notif_autoprovocada_bairro_2026.png` | bairro; contagem, `bins`; **2026 como ano de referência** (33 casos, ~20 bairros); legenda/nota: ano parcial + possível mudança de registro | 🅰 (D3b) |
| M8-M10 | `mapa_violencia_familiar_{mae,pai,outros}_taxa_bairro_2025.png` | bairro; **taxa por 1.000 crianças 0-4**, colorbar contínua (convenção: taxa = contínua) | 🅰 Taxa de notificações (D1) — **[?] D8: cortar se redundante com M1-M3** |
| M4 | `mapa_violencia_territorial_taxa_homicidios_ra_2024.png` | **RA**; taxa, colorbar | 🅰 Violência territorial |
| M5 | `mapa_violencia_territorial_homicidios_acao_policial_ra_2024.png` | **RA**; taxa, colorbar | 🅰 |
| M6 | `mapa_violencia_territorial_homicidios_jovens_negros_ra_2024.png` | **RA**; taxa, colorbar | 🅰 |

Total proposto: **7 tabelas (T3 = 2 arquivos → 8 CSVs) + 8 gráficos + 10 mapas** (opcionais/[?]: G3, G8, M8-M10). Mapas M4-M6 dependem 100% da RA (§3). Nenhum mapa de cônjuge/ex/filho(a) individualmente (<20 casos).

### 5.4 Considerados e **não** propostos
- **"Total de violência familiar"** (soma dos vínculos): dupla contagem; o arquivo não traz o total.
- **Dispersão taxa Sinan × taxa IPS por RA**: agora factível com D1, mas o denominador é 0-4 e o IPS é todas as idades — leitura frágil; candidata a rodada futura.
- **Mapas por CAP de violência familiar**: T3 basta; reavaliar se a Saúde pedir.

---

## 6. Cobertura dos itens em aberto do catálogo (eixo Proteção)

| Item do catálogo | Status hoje | Entregas | Status proposto |
|---|---|---|---|
| Violência territorial (ISP → **Data.Rio/IPS**) | pendente | T6, G4-G6, M4-M6 | **implementado** (nota: só 2024, todas as idades, sem série) |
| Violência familiar (<1, 1-5) | pendente | T1-T4, T7, G1-G3, G8, M1-M3 | **implementado parcial** (0-5 agregado; recorte <1/1-5 pendente) |
| Notificações interpessoal/autoprovocada (<1, 1-5) | pendente | T5, G7, M7 | **parcial** (só autoprovocada; interpessoal total e recorte <1/1-5 pendentes) |
| Taxa de notificações de violência (0-6) | pendente | T7, M8-M10 | **implementado com ressalva** (numerador 0-5 ÷ denominador 0-4, Censo 2022 — D9) |
| Crianças que sofrem violência, por tipificação (sexo e idade) | pendente | — | **pendente** (extração Tabnet pelo usuário em andamento; ver nota abaixo) |
| Territórios com risco a inundação/movimento de massa (SGB) | Posterior (Moradia) | — | **REMOVIDO DA V1** — não aparece em HTML/PDF/DOCX nem como cartão `pendente`; pode ser **alterado futuramente** (fonte/escopo/eixo a redefinir). Em `estrutura_eixos.md` a subseção sai da estrutura publicada (ou fica marcada como fora da V1) na implementação, sem apagar a linha do catálogo |

Itens 🅱 (T3, T4, G2, G3, G7) são adicionais e entram em `estrutura_eixos.md` como `### ` extras do
eixo Proteção (ex.: "Violência familiar — composição de 'outros'"), para o parser
(`parse_estrutura_eixos()`) tratar como qualquer subseção.

**Extração Tabnet pelo usuário (dados faltantes):** tipificação por sexo/idade, recorte <1 ano vs 1-5
e, se disponível, o total de notificações de violência interpessoal (hoje só há autoprovocada).
Se chegarem **antes** do início da implementação, o plano os incorpora (novos T/G/M usando os mesmos
carregadores `carrega_sinan_bairro`, que já são genéricos); se chegarem depois, viram rodada
seguinte sem retrabalho. Recomendo pedir exports no **mesmo formato** dos atuais (Sinan NET, bairro
de residência × ano, latin-1) para reaproveitar o carregador.

---

## 7. Impacto nos artefatos e proteção contra regressão

### 7.1 Ordem de trabalho (sem tocar nos geradores até `analise.py` estar validado)
1. Baseline (§7.2). 2. `analise.py`: funções + `'ra'` + seção Proteção → gera CSV/PNG/mapas.
3. `estrutura_eixos.md`: subseções de Proteção `pendente` → arquivos reais.
4. `build_html_report.py` (níveis `ra`, novos blocos SVG, tema de cor). 5. PDF. 6. DOCX
(`gera_docx_curadoria.py`; textos por visualização, `specs/2026-09-22_ajuste_eixos` §7). 7. Skills/docs.
8. Validação → só então §8.

### 7.2 Baseline e comparação
Como `tabelas_finais/`, `visualizacoes/`, `mapas/` são gitignored, a garantia de "sem quebrar" é local:
antes de qualquer edição, gravar checksum (SHA-256) de todas as saídas existentes e o número de
seções/cards/mapas de `relatorio/index.html`, do PDF (páginas) e do DOCX (seções). Após: o diff deve
mostrar **apenas arquivos novos** e o eixo Proteção alterado; qualquer checksum de saída antiga
diferente é regressão (exceto metadados/timestamps, tratados caso a caso).

### 7.3 Pontos de atenção por artefato
- **HTML**: SVG próprio, `_geo_nivel` precisa de `ra`; peso já ~17 MB — até 10 mapas novos somam; usar o
  mesmo pipeline de compressão existente e medir o tamanho antes/depois (limite a definir, D7).
  Eixo Proteção hoje mostra cartões `pendente`; passam a conter conteúdo real. Pills/`h3` de itens
  parciais devem exibir a nota de limitação.
- **PDF**: usa PNGs de `visualizacoes/`/`mapas/` conforme `estrutura_eixos.md` — nova entrada só
  aparece se o arquivo existir (checar `check_maps`/equivalente).
- **DOCX**: cada visualização nova ganha bloco de texto editável; `sincroniza_docx.py` não pode perder
  texto já curado dos outros eixos (testar ida-e-volta: gerar → sincronizar → diff sem mudanças).
- **Textos**: notas obrigatórias — quebra 2017, 2026 excluído por ser parcial, vínculos não
  excludentes, IPS todas as idades/2024, contagem absoluta ≠ risco.

---

## 8. Deploy no GitHub Pages — somente após validação

- O deploy é **manual** (`workflow_dispatch`, `.github/workflows/deploy-relatorio.yml`), publica só
  `relatorio/index.html`. **Nada é disparado nesta rodada até o usuário dar o "ok" explícito.**
- Pré-condições (checklist em `validation.md`): (a) V-regressão §7.2 limpa; (b) `index.html` aberto e
  navegado manualmente em tema claro/escuro, eixo Proteção completo, demais eixos idênticos;
  (c) PDF e DOCX regenerados e conferidos; (d) tamanho do HTML dentro do limite acordado;
  (e) usuário revisou textos/notas; (f) merge para a branch de deploy (a confirmar qual — a branch
  principal é `staging_main`; verificar o que o workflow faz checkout).
- Plano de reversão: o site atual é o último `index.html` commitado; manter a tag/commit anterior
  ao merge para re-disparar o workflow com a versão antiga se algo falhar em produção.

---

## 9. Decisões para revisão

| # | Decisão | Padrão proposto |
|---|---|---|
| D1 | Derivar taxa por 1.000 crianças | **DECIDIDO: sim** — T7, M8-M10, colunas de taxa em T3 |
| D2 | Ano dos mapas de bairro | mãe/pai em 2025; **acumulado 2021-2025 para "outros"** (padrão proposto, não contestado) |
| D3 / D3b | 2026 excluído das séries de vínculo (decidido). Autoprovocada | **DECIDIDO:** gráfico de barras "antes de 2026 × 2026" (G7) e mapa com **2026 como referência** (M7); texto explica a possível mudança de registro administrativo — **hipótese, a confirmar com a fonte (SMS/Sinan) antes de afirmar como fato** |
| D4 | Pasta de dados | **DECIDIDO:** renomeada para `dados_locais/protecao/` (feito). **Zip extraído** para `dados_locais/protecao/violencia_familiar/` (7 CSVs commitados; o `.zip` original segue ignorado pelo `.gitignore` `*.zip`) e lido como CSV comum |
| D5 | Cor do tema Proteção nos mapas/gráficos | **`OrRd`** (novo tema `protecao`). `Purples` foi descartado: no HTML já é o tema `censo` (`_CMAP_TEMA`), embora em `analise.py` `censo` seja `Blues` — divergência preexistente, registrada para a tarefa de documentação (roadmap item 9). Os dois dicionários (`_CORES_TEMA_MAPA` e `_CMAP_TEMA`) recebem a chave nova |
| D6 | "Outros" = padrasto + irmão(ã) + cônjuge + ex-cônjuge + filho(a) soma casos de possíveis mesmas notificações (vínculos não excludentes; a mesma vítima pode ter >1 autor) | Aceitar e **rotular explicitamente** "vínculos não excludentes — soma pode contar uma notificação mais de uma vez"; o mesmo vale para o par mãe/pai (nunca somá-los) |
| D7 | Orçamento de peso do HTML (~17 MB) para os até 10 mapas novos | Medir; limite proposto +2,5 MB |
| D8 | Itens redundantes: G3, G8 (top bairros) e M8-M10 (mapas de taxa vs. contagem) | Gerar tudo, avaliar na revisão visual e cortar o redundante (você já sinalizou essa abordagem) |
| D9 | **Denominador da taxa**: por bairro só há população **0-4** (Censo 2022); o Sinan cobre **0-5** (numerador com 6 idades, denominador com 5) e é de 2025 vs pop. 2022 | (a) padrão: casos 0-5 ÷ pop 0-4, **rotulado "por 1.000 crianças de 0-4 anos (numerador inclui 5 anos)"**, superestima ~20%, mas uniformemente, então o *ranking* entre bairros se preserva; (b) estimar pop 0-5 = 0-4 + 1/5 de 5-9 (mais próximo, porém é estimativa); recomendação: **(a)**, por transparência |

| D10 | Piso de população para taxa de bairro (bairros muito pequenos, ex. Grumari, geram taxas instáveis) — surgiu no `plan.md` | Não suprimir; sinalizar em nota e listar bairros com pop 0-4 < 100 |

---

## 10. Fora de escopo
Novas extrações Tabnet/ISP (a cargo do usuário); tipificação; **SGB/inundação (removido da V1)**; **população por bairro ano a ano** (spec seguinte, `specs/roadmap.md` item 6 — esta rodada usa o denominador 0-4 do Censo 2022 com a ressalva D9 e não o corrige); mapas por CAP; SGB/inundação;
qualquer reorganização física de células de `analise.py`; mudança no workflow de deploy.
