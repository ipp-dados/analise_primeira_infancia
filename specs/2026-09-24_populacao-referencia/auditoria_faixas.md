# Auditoria de faixas etárias (Parte C, C1)

Levantamento de 2026-09-24, depois dos Blocos 1-6. Varredura de `analise.py`, `tabelas_finais/`,
`visualizacoes/`, `mapas/`, `specs/estrutura_eixos.md`, dos três scripts de relatório e do HTML gerado.
**Nada desta lista foi executado.** Pela decisão C-D1, rótulos (C2) e renomeações (C3) só entram depois
do ok do usuário (§5).

## 1. Fonte → faixa real → data de referência → rótulos em uso

| Fonte | Faixa real do dado | Data de referência da idade | Rótulos em uso (títulos, legendas, arquivos) | Situação |
|---|---|---|---|---|
| **CadÚnico** (`silver_cadunico_geral`, grupo `'0-6'`) | **0 a 5 anos completos** (nascidos a partir de 2020-08-12; 6 anos caem em `'7-14'`) | idade calculada ~2026-08-12; partição 2026-06-12 | "0-6", "até 6 anos", "(0-6 anos)" em 8 títulos de gráfico, 1 título de mapa, 4 subtítulos do crosswalk/HTML | ❌ rótulo ≠ dado (C2) |
| **CadÚnico, recorte `idade < 5`** | 0 a 4 anos | idem | "(0-4 anos)", mas arquivos `*_primeira_infancia_*` | ⚠️ rótulo certo, **nome de arquivo ≠ conteúdo** (C3) |
| **Censo 2022 por bairro** (Data.Rio) | 0 a 4 anos (grupo quinquenal) | 31/07/2022 | "0 a 4 anos", `*_0_4_*` | ✅ |
| **Censo 2000/2010/2022, série** (tabela 2974 por bairro) | 0 a 4 anos | 01/08/2000, 31/07/2010, 31/07/2022 | "0 a 4 anos", `censo_0_a_4_*` | ✅ rótulo; ❌ **bug no total** (§2) |
| **SIDRA 9606** (Censo 2022) | idade simples 0 a 6 | 31/07/2022 | "0 a 6 anos", `censo_sidra_populacao_0_6_*` | ✅ |
| **SIDRA 10057** (frequência escolar) | 0 a 5 anos | 31/07/2022 | "até 5 anos" / "0 a 5 anos", `sidra_frequencia_escola_0_5_*`; crosswalk "até 6 anos" | ⚠️ títulos ok; subtítulos do crosswalk dizem "até 6" |
| **SIDRA 10056** (taxa de frequência) | 0 a 6 anos | 31/07/2022 | "(0-6 anos)", `sidra_taxa_frequencia_0_6_*` | ✅ |
| **PNAD Contínua** (frequência escolar) | idade simples 0 a 6 (e 0-3, 4-5) | data da entrevista | título "Frequencia escolar por idade" (sem faixa, sem acento) | ⚠️ falta a faixa no título; recorte geográfico a confirmar (o notebook diz estadual/nacional) |
| **Sinan** (violência, autoprovocada) | 0 a 5 anos | idade na notificação | "0 a 5 anos" em títulos e fontes; crosswalk "Taxa de notificações de violência **(0 a 6 anos)**" | ⚠️ só o subtítulo do crosswalk/HTML está errado |
| **Sinan ÷ Censo** (taxa por bairro/RA/CAP) | numerador 0-5, denominador 0-4 | notificação × 31/07/2022 | explícito desde o Bloco 3 | ✅ (ressalva D9 documentada) |
| **Ripsa/MS** | idade simples 0-79, 80+ (extrato: 0 a 6) | 1º de julho | "0 a 6", "0 a 5" conforme a coluna | ✅ |
| **Censo Escolar/INEP** | 0-3 e 4-5 (6 anos misturado com 7-10) | última quarta-feira de maio | "0 a 5 anos", `matriculas_0_a_5_*` | ✅ (Parte E) |
| **SISVAN** | "Criança (de 0 a 5 anos)" (cabeçalho dos relatórios) | data do acompanhamento | "0 a 6 anos" em 3 títulos de gráfico; nota "crianças 0-6 anos"; crosswalk sem faixa | ❌ rótulo ≠ dado (C2) |
| **Cobertura vacinal (EPI Rio)** | coorte-alvo de cada vacina (menores de 1 ano, 1 ano...) | ano de aplicação | "rotina em crianças até 2 anos" (painel da SMS) | ✅ (rótulo da fonte) |
| **SIM/SINASC, mortalidade** | dias (0-6, 7-27, 28-364) e anos (<1, 1-4, <5) | óbito | títulos certos ("0-6 dias"); arquivos `*_0_6_ano`, `*_7_27_ano`, `*_28_364_ano` | ⚠️ **nome ambíguo**: `0_6` lê-se como "0 a 6 anos" (C3) |

## 2. Achado fora de rótulo: total dobrado na série dos Censos

`total_e_percentual_ano` (topo de `analise.py`) cria a coluna `'0 a 4 anos'` **antes** de somar
`df.iloc[:, 9:]`, então a faixa de 0 a 4 anos entra duas vezes no `Total`. Conferido com os totais oficiais
do IBGE para o Rio:

| Ano | `Total` no notebook | Total sem a dupla contagem | Total oficial (IBGE) | % 0-4 publicado | % 0-4 correto |
|---|---|---|---|---|---|
| 2000 | 6.305.209 | 5.857.904 | 5.857.904 | 7,1% | **7,6%** |
| 2010 | 6.684.478 | 6.320.446 | 6.320.446 | 5,4% | **5,8%** |
| 2022 | 6.479.557 | 6.171.823 | (tabela 2974 por bairro) | 4,7% | **5,0%** |

Afeta `tabelas_finais/censo_0_a_4_anos_por_ano.csv` (colunas `Total` e `Percentual 0 a 4 anos`), o gráfico
de percentual do notebook, o card "% 0-4 anos" do HTML, o PNG `censo_0_a_4_serie_percentual_ano.png`, a
nota de curadoria de `mapa_censo_0_4_percentual` (texto do usuário, cita 7,1% / 5,4% / 4,7%) e a nota A5
deste bloco (que repete os mesmos números). As contagens de 0 a 4 anos não mudam.

**Correção proposta:** calcular `Total` antes de criar a coluna `'0 a 4 anos'` (uma linha), regenerar a
tabela, o PNG e o HTML/PDF, e corrigir os números da nota A5. A nota de curadoria fica para o usuário.

## 3. Lista A: rótulos a corrigir (C2)

Só títulos, legendas e textos de código/relatório. Notas de curadoria ficam na lista C.

| # | Onde | Hoje | Proposta |
|---|---|---|---|
| A1 | `analise.py`, 4 gráficos CadÚnico por renda e idade | "CADÚNICO: … crianças 0-6 …" | "… crianças de 0 a 5 anos …" |
| A2 | `analise.py`, 6 gráficos CadÚnico por sexo, raça/cor, arranjo | "… crianças até 6 anos …" | "… crianças de 0 a 5 anos …" |
| A3 | `analise.py` e HTML, mapa CadÚnico por bairro | "Crianças (0-6 anos) no CadÚnico, por bairro" | "Crianças (0 a 5 anos) no CadÚnico, por bairro" |
| A4 | `analise.py` e HTML/PDF, mapas CadÚnico de raça/cor e arranjo | "… até 6 anos no CadÚnico …" | "… de 0 a 5 anos no CadÚnico …" |
| A5 | HTML/PDF, subtítulos "Famílias no CadÚnico com crianças até 6 anos, por …" (3) | "até 6 anos" | "de 0 a 5 anos" (ver decisão C-D2) |
| A6 | `analise.py`, 3 gráficos SISVAN + nota da seção | "0 a 6 anos" / "0-6 anos" | "0 a 5 anos" |
| A7 | `analise.py`, PNAD | "Frequencia escolar por idade" | "Frequência escolar por idade, 0 a 6 anos (PNAD Contínua)" |
| A8 | crosswalk e HTML/PDF, "Taxa de notificações de violência (0 a 6 anos)" | "(0 a 6 anos)" | "(0 a 5 anos)" |
| A9 | `analise.py`, markdown da seção CadÚnico ("recorte de crianças 0-6 anos", "Recorte 0-6 anos") | "0-6" | "0 a 5 anos (grupo `'0-6'` do CTPE)" |

## 4. Lista B: renomeações propostas (C3)

Todos os arquivos abaixo estão rastreados no git (P-C1): `git mv`/`git rm` + `git add -f`, e os leitores
ajustados.

| # | Hoje | Proposta | Leitores |
|---|---|---|---|
| B1 | `mapas/mapa_cadunico_primeira_infancia_bairro_2026.png` | `mapa_cadunico_criancas_0_a_4_bairro_2026.png` | `analise.py`, HTML, PDF, crosswalk, `relatorio/textos_curados.json` (chave de texto curado: migrar) |
| B2 | `tabelas_finais/tabela_mapa_cadunico_primeira_infancia_2026.csv` | `tabela_mapa_cadunico_criancas_0_a_4_2026.csv` | `analise.py`, HTML, crosswalk |
| B3 | `mapas/mapa_percentual_cadunico_primeira_infancia_bairro_2026.png` (só notebook) | `mapa_percentual_cadunico_0_a_4_sobre_censo_bairro_2026.png` | `analise.py` |
| B4 | `*_causas_evitaveis_{grupo,subgrupo}_0_6_ano.*` (2 CSV em `tabelas_finais/`, 2 em `dados_locais/tratados/`, 2 PNG) | `…_0_a_6_dias_ano.*` | `analise.py`, crosswalk |
| B5 | idem `_7_27_ano` e `_28_364_ano` (8 CSV, 4 PNG) | `…_7_a_27_dias_ano`, `…_28_a_364_dias_ano` (mesmo padrão de B4) | `analise.py`, crosswalk |

Sem renomeação proposta (nome = conteúdo): `censo_sidra_populacao_0_6_*`, `sidra_taxa_frequencia_0_6_*`,
`sidra_frequencia_escola_0_5_*`, `populacao_ripsa_0_a_6_*`, `matriculas_0_a_5_*`, `censo_0_a_4_*`,
`cadunico_por_bairro_ate_4_2026.csv`. O padrão de nome mistura `0_6` e `0_a_6`; unificar tudo seria uma
renomeação ampla sem ganho de clareza, por isso fica fora.

## 5. Lista C: notas de curadoria afetadas (texto do usuário, não editado)

| Chave | Problema |
|---|---|
| `mapa_censo_0_4_percentual` | cita 7,1% / 5,4% / 4,7% (bug do §2; corretos 7,6% / 5,8% / 5,0%, Censo) |
| `cadunico_familias_por_idade` | "crianças até 6 anos no CadÚnico" (dado: 0 a 5) |
| `mapa_cadunico_primeira_infancia_bairro_2026` | "crianças de 0 a 6 quanto 0 a 4 no CadÚnico" (dado: 0 a 5 e 0 a 4) |
| DOCX, "Textos órfãos" | texto curado do item "Crianças até 6 anos (número)" (sobre o SIDRA 9606, por idade, raça/cor e sexo) saiu do item no Bloco 6, porque o item passou a apontar para a série Ripsa. Parece pertencer aos itens de Inclusão "Crianças até 6 anos, por sexo / por raça/cor" |

## 6. Decisões para o usuário

| # | Decisão | Proposta |
|---|---|---|
| **C-D1** (aprovada) | Executar C2/C3 só depois de ver as listas | — |
| **C-D2** | Os subtítulos do crosswalk que vêm do catálogo ("Famílias no CadÚnico com crianças até 6 anos…", "Crianças até 6 anos frequentando escola/creche") mudam para a faixa real, ou ficam com o nome do catálogo e a faixa real vai na nota? | Mudar os títulos de gráfico/mapa (lista A) e **manter o nome do catálogo nos subtítulos do crosswalk**, com a faixa real na `nota` — o catálogo é o vocabulário da política |
| **C-D3** | Corrigir o bug do total da série dos Censos (§2) nesta rodada | Sim; muda o percentual publicado (não as contagens) |
| **C-D4** | Renomeações B1-B5 | B1-B3 sim (nome diz "primeira infância", conteúdo é 0-4); B4-B5 sim (ambiguidade dias × anos) |

## 7. Execução (C2/C3, 2026-09-24)

Decisões do usuário (2026-09-24): **C-D2 ✅** (subtítulos do crosswalk com o nome do catálogo, faixa real na
`nota`; títulos de gráfico e mapa com a faixa real), **C-D3 ✅** (corrigir o total da série dos Censos),
**C-D4 ✅** (renomeações B1-B5).

- **§2:** `total_e_percentual_ano` soma o `Total` antes de criar `'0 a 4 anos'`. `censo_0_a_4_anos_por_ano.csv`
  muda só em `Total` e `Percentual 0 a 4 anos` (7,64% / 5,76% / 4,99%); contagens iguais. Nota A5 corrigida. O
  PNG `censo_0_a_4_serie_percentual_ano.png` (gerado só por `regen_missing_pngs.py`) foi regenerado isolado.
- **Lista A:** A1-A4, A6, A7 e A9 aplicadas em `analise.py` e nos dois geradores; A5 e A8 ficam com o nome do
  catálogo (C-D2), com a faixa real na `nota` do crosswalk (CadÚnico, SIDRA 10056/10057, SISVAN). PNG
  regenerados: 10 gráficos e 5 mapas do CadÚnico, 3 do SISVAN, 1 da PNAD. Todas as CSV regravadas são
  iguais às anteriores, exceto a da série dos Censos.
- **Lista B:** 21 arquivos rastreados com `git mv` (3 do CadÚnico, 18 de mortalidade), leitores em
  `analise.py`, crosswalk e geradores (inclusive os sufixos montados em f-string nos dois geradores), e a
  chave de `relatorio/textos_curados.json`. No DOCX, os 8 bookmarks das imagens renomeadas foram migrados
  para os nomes novos (texto preservado; "Textos órfãos" continua com 6 itens).
- **Lista C:** notas de curadoria não editadas; ficam com o usuário.
