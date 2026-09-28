# Especificação — Merge das mudanças da Waleska

Ver `plan.md` para a estratégia técnica e a validação numérica independente do bug de cálculo,
`tasks.md` para o checklist de execução e `validation.md` para os critérios de aceite.

## Contexto

`origin/waleska-analise-primeira-infancia` é uma revisão de `analise.py` feita
por Waleska Marques: remoção de visualizações redundantes/pouco interessantes
e pequenas correções de curadoria (títulos, rótulos, um bug de cálculo). O
branch parte de `3a258e8` (o `staging_main` de antes das rodadas
`specs/2026-09-09_maps-and-ibge`, `specs/2026-09-09_visual-identity` e `specs/2026-09-14_relatorio-interativo`),
então está **muito atrasado** em relação ao nosso branch atual — mas toca só
`analise.py`, e só em regiões que não colidem com o que fizemos depois (ver
"Teste de merge" abaixo).

4 commits, só em `analise.py`:

| Commit | Mensagem | Linhas |
|---|---|---|
| f3477c9 | Ajusta curadoria do Censo | +28 -14 |
| 4da8409 | Ajusta curadoria da mortalidade evitável | +149 -149 |
| c555e2c | Ajusta curadoria da seção de Saúde | +40 -39 |
| 6461a12 | Corrige fonte das causas evitáveis | +1 -1 |

## Resumo por commit

### 1. Ajusta curadoria do Censo (f3477c9)

- **Corrige um bug real de agregação**: `total_e_percentual_ano` passa a
  devolver também a coluna `Total`; a série temporal do Censo (2000/2010/2022)
  deixa de somar a coluna `Percentual 0 a 4 anos` diretamente por ano (média
  de percentuais por bairro — viola a convenção do projeto, ver
  `specs/constitution.md` §3) e passa a somar os absolutos primeiro e
  recalcular o percentual depois. Correção legítima e consistente com o resto
  do projeto.
- Remove os 4 mapas de Censo por AP/RP (`niveis_planejamento`, absoluto e
  percentual × AP/RP) — bloco inteiro comentado, não apagado.
- Melhora títulos/labels dos 2 gráficos de série temporal do Censo (mais
  descritivos, unidade explícita no eixo).
- **Efeito colateral (não mencionado na mensagem do commit): a linha
  `df_serie_censo.to_csv('tabelas_finais//censo_0_a_4_anos_por_ano.csv')`
  desaparece** — parece um esquecimento da reescrita do bloco de agregação,
  não uma remoção intencional (ver "Riscos" abaixo).

### 2. Ajusta curadoria da mortalidade evitável (4da8409)

Maior commit, todo por comentário de blocos (não exclusão de código — dá pra
reverter fácil se algo for indesejado):

- Remove a análise de óbitos evitáveis por raça/cor no município inteira
  (pipeline `df_evitaveis_raca_municipio` + 3 gráficos: absoluto, absoluto
  sem "não informada", percentual). Justificativa implícita: provavelmente
  redundante com a análise de mortalidade geral por raça/cor já existente
  (o próprio notebook já nota, `analise.py:1373`, que "os gráficos
  `percentual_mortalidade_raca_ano` e `percentual_mortalidade_causas_evitaveis_raca_ano`
  acabam sendo quase idênticos").
- Remove a matriz de séries temporais subgrupo × CAP × faixa etária (18
  gráficos).
- Remove os 2 mapas e as 2 séries temporais de gestação/parto por CAP
  (componente C).
- Remove o mapa de contagem absoluta de óbitos durante a gravidez por bairro
  e o de puerpério por bairro (mantém as séries temporais desses, que não
  foram tocadas).
- Remove os mapas de contagem absoluta de óbitos neonatais tardios e
  pós-neonatais por bairro — **mantém os mapas de taxa** (`taxa_obitos_tardios`,
  `taxa_mortalidade_pos_neonatal`) logo abaixo, intocados. Padrão consistente:
  quando existe uma versão em taxa, a contagem absoluta correspondente é
  considerada redundante e removida.
- Ajusta título/legenda do mapa de percentual de óbitos evitáveis por CAP
  para deixar claro que é proporção **entre os óbitos totais** (não entre
  nascidos vivos): "Percentual de óbitos evitáveis" → "Proporção de óbitos
  evitáveis entre os óbitos"; legenda "% evitáveis" → "% dos óbitos". Melhora
  de precisão, não uma mudança de cálculo.
- **Bug introduzido e corrigido no próprio branch**: o comentário do bloco de
  raça/cor engloba também a linha `fonte_evitaveis = '...'`, usada por várias
  chamadas mais abaixo que **não** foram comentadas (mapas de CAP, etc.) —
  isso quebraria essas chamadas com `NameError`. Corrigido no commit seguinte.

### 3. Ajusta curadoria da seção de Saúde (c555e2c)

- Melhora títulos dos 3 gráficos de SISVAN (desnutrição/sobrepeso/obesidade):
  mais descritivos, citam a fonte no próprio título.
- Remove o gráfico principal de cobertura vacinal por imunobiológico
  (série 2016-2026, `cobertura_vacinal_epi_ano`) — mantém o comparativo entre
  os 4 anos (2016/2019/2022/2025), que cobre o mesmo dado de forma mais
  direta segundo a nova nota de markdown.

### 4. Corrige fonte das causas evitáveis (6461a12)

Descomenta só a linha `fonte_evitaveis = '...'` que tinha sido comentada por
engano no commit 2 (ver acima) — sem isso, todo call site de mapa/série de
causas evitáveis por CAP que ainda está ativo (não removido pela curadoria)
quebraria com `NameError: name 'fonte_evitaveis' is not defined`.

## Teste de merge

`git merge --no-commit --no-ff origin/waleska-analise-primeira-infancia` a
partir do HEAD atual (`planning`, já com a reorganização de specs) — **merge
automático limpo, zero conflitos**, diff idêntico ao diff de Waleska contra
sua própria base (+206/-191 em `analise.py`). `ast.parse` confirma que o
arquivo resultante é Python válido. Testado e revertido (`git merge --abort`)
antes de decidir a estratégia final — nada foi commitado ainda.

Apesar do branch estar muito atrasado, as mudanças de `specs/2026-09-09_maps-and-ibge`
+ `specs/2026-09-09_visual-identity` + `specs/2026-09-14_relatorio-interativo` não tocam as mesmas
linhas que Waleska editou (elas mexeram principalmente em
`mapa_coropletico_bairros`, no módulo de estilo compartilhado e em código
novo — Waleska mexeu em call sites de seções específicas de análise já
existentes na base antiga). Um merge real (preservando os 4 commits e a
autoria dela) é viável sem reconciliação manual linha a linha.

## Riscos encontrados — pipelines downstream que quebram

`analise.py` não é o único lugar que conhece os nomes de arquivo que ele
gera. Os scripts do skill `export_pdf_report`
(`build_notebook_report.py`, `build_html_report.py`,
`regen_missing_pngs.py`) referenciam, por nome, PNGs/CSVs específicos —
e **vários deixam de ser gerados** pela curadoria da Waleska:

| Arquivo que para de ser gerado | Referenciado em |
|---|---|
| `tabelas_finais/censo_0_a_4_anos_por_ano.csv` (perdido por acidente, não por decisão de curadoria) | `build_notebook_report.py`, `build_html_report.py`, `regen_missing_pngs.py` |
| `mortalidade_causas_evitaveis_raca_municipio_ano.csv` + os 4 PNGs de óbitos evitáveis por raça/cor | `build_notebook_report.py`, `build_html_report.py` |
| `mapa_obitos_evitaveis_gestacao_menores_1_ano_cap_2025.png` / `..._parto_...` | `build_notebook_report.py` (galeria de mapas) |
| `mapa_obitos_gravidez_bairro_2025.png`, `mapa_obitos_puerperio_bairro_2025.png`, `mapa_obitos_neonatal_tardia_bairro_2025.png`, `mapa_obitos_pos_neonatal_bairro_2025.png` (contagens absolutas) | `build_notebook_report.py` (galeria de mapas) |
| `mapa_censo_0_4_percentual_ap.png` / `_rp.png` (e provavelmente os dois `_absoluto_ap/rp`, mesmo bloco) | `build_notebook_report.py` (galeria de mapas) |
| `cobertura_vacinal_epi_ano.png` | `build_notebook_report.py` |

Isso não quebra `analise.py` em si (o próprio notebook roda sem erro — as
seções removidas simplesmente não existem mais). Quebra **a próxima vez que
alguém rodar o skill `export_pdf_report`** (`build_notebook_report.py` vai
tentar abrir um PNG/CSV que não existe mais e falhar, ou `build_html_report.py`
vai fazer o mesmo para a seção de raça/cor evitáveis) — o próprio `SKILL.md`
já avisa que esses scripts são "uma foto de um contrato", não algo genérico,
e pede pra serem lidos/atualizados quando `analise.py` muda. É exatamente
esse o caso agora.

`relatorio/index.html` (gerado por `build_html_report.py`) e o PDF
(`analise_primeira_infancia.pdf`, gerado por `build_notebook_report.py`) só
quebram **quando regenerados** — os arquivos já commitados/publicados hoje
não mudam sozinhos.

## Proposta

1. Fazer o merge de verdade (`git merge origin/waleska-analise-primeira-infancia`,
   preservando os 4 commits e a autoria da Waleska) neste branch,
   `specs/2026-09-22_merge-waleska-changes` (criado a partir de `planning`).
2. Restaurar a linha `df_serie_censo.to_csv(...)` que sumiu por acidente —
   claramente não fazia parte da curadoria pretendida.
3. Para os PNGs/CSVs que pararam de ser gerados **de propósito**: atualizar
   `build_notebook_report.py` (e `build_html_report.py` onde aplicável) para
   parar de referenciá-los, evitando quebrar a próxima geração de
   relatório/PDF — em vez de deixar como dívida técnica silenciosa.
4. Rodar o notebook do zero (ou pelo menos as seções tocadas) pra confirmar
   que não há mais nenhuma referência solta às variáveis/arquivos removidos.

## Execução

Itens 1-3 feitos neste branch:

- **Merge real**: `git merge origin/waleska-analise-primeira-infancia`
  (commit `ed964a5`), preservando os 4 commits/autoria da Waleska. Sem
  conflitos, igual ao teste prévio.
- **CSV do Censo restaurado**: `df_serie_censo.to_csv('tabelas_finais//censo_0_a_4_anos_por_ano.csv')`
  de volta em `analise.py`, logo após o cálculo do percentual (commit `0facf8a`).
- **Scripts de relatório corrigidos** (commit `0facf8a`): removidas de
  `build_notebook_report.py` e `build_html_report.py` todas as referências a
  saídas que a curadoria descontinuou (tabela no spec acima) — verificado por
  grep que não sobra nenhuma, e `ast.parse` confirma que os 3 arquivos
  (`analise.py` + os 2 scripts) continuam sintaticamente válidos.

**Item 4 pendente** — não rodei o notebook de ponta a ponta (precisa da
conexão com o Postgres do CadÚnico e acesso de rede para os tiles do
`contextily`, indisponíveis nesta sessão). O que foi verificado sem executar:
`ast.parse` em todos os arquivos tocados e uma auditoria por `grep` de que
nenhum nome de arquivo/variável removido ainda é referenciado em
`analise.py` ou nos scripts de relatório. **Recomendado antes de dar o merge
por definitivamente validado**: rodar `analise.py` do zero (kernel limpo) e,
depois, o skill `export_pdf_report` de ponta a ponta, para confirmar em
tempo de execução (não só estaticamente) que nada quebrou.
