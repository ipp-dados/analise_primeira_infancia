# Plano técnico: Matrículas e taxa de atendimento de 0 a 5 anos (Censo Escolar/INEP + Ripsa)

Baseado em `specification.md` (rascunho 4). IDs D1-D9 (decisões) e P1-P7 (pendências) são os da spec.
**Nada daqui em diante é executado antes do ok do usuário para implementar** (pedido de 2026-09-24;
decisões D1-D9 já aprovadas). O check de 2025 (condição de D4) já foi feito e está em spec §3.5.

## Decisões

- **D1 ✅ 0-5**: `QT_MAT_BAS_0_3 + QT_MAT_BAS_4_5`, com idade na data padrão do Censo (última quarta-feira
  de maio). As colunas `_REF_31_03` de 2025 não são usadas.
- **D1, nome dos arquivos ✅ renomear**: `matriculas_0_a_6_por_ano` passa a `matriculas_0_a_5_por_ano`. Os
  dois arquivos antigos (`tabelas_finais/…csv`, `visualizacoes/…png`) estão **rastreados no git**, então
  vão para `git rm` e os novos entram com `git add -f`, mantendo o que já era versionado. Os leitores a
  ajustar são os três scripts de P4 e `estrutura_eixos.md`.
- **D2 ✅ reconstruir**: série 2007-2025 inteira a partir dos ZIPs do INEP. Sai de uso
  `dados_locais/educacao/censo_escolar_matriculas_ate_6anos.csv` (`git rm`; o histórico fica no git e
  na spec, §3.4).
- **D3 ✅**: creche × pré (0-3 × 4-5) e pública × privada (`TP_DEPENDENCIA` 1-3 × 4).
- **D4 ✅**: 2025 incluído (compatível, §3.5).
- **D5 ✅**: ZIPs em `dados_locais/educacao/inep_microdados/`, gitignorado (regra já adicionada;
  `*.zip` também já era ignorado).
- **D6 ✅ no escopo**: taxa bruta de atendimento = matrículas ÷ população residente da faixa.
- **D7 ✅ Ripsa, com nota metodológica**: denominador Ripsa/MS na série inteira. A nota tem os 6 pontos
  listados em spec §5 (Ripsa × Censo 2022, taxa bruta, revisões, diferença com a PNAD, PNE).
- **D8 ✅ (b)**: linhas de referência do PNE (50% creche, 100% pré) via parâmetro opcional.
- **D9 ✅**: taxa para 0-3, 4-5 e 0-5, num gráfico só.


## Princípios

- **Só a seção 🎓 de matrículas muda** (`analise.py:3166-3179`), mais as funções novas no topo, as
  referências nos três scripts de relatório e em `estrutura_eixos.md`. A PNAD e o SIDRA logo acima não
  são tocados, exceto para renomear a variável `df_freq_escolar` reaproveitada **na célula de
  matrículas** (spec §2). Única exceção (D8): o parâmetro opcional em `serie_temporal_multipla`
  e no `line_chart` do HTML, com default que não muda nada.
- **Uma fonte, uma definição**: todos os anos passam pela mesma função, com as mesmas colunas e a mesma
  data de referência. O mesmo vale para a população.
- **Somar antes de dividir** (constitution §3): taxa de 0-5 = (mat 0-3 + mat 4-5) ÷ (pop 0-3 + pop 4-5),
  nunca a média das taxas de 0-3 e 4-5.
- **Notebook roda offline**: os extratos versionados bastam, e a rede só é usada se faltar um ano.

## Blocos

### Bloco 1: Downloads e checagem de 2007-2019 (P6)

- Baixar os 13 ZIPs de 2007-2019 para o cache (~300 MB; usar `curl --retry … -C -`, já que o INEP
  derrubou uma conexão SSL no download de 2025).
- Para cada ano: nome do CSV, encoding, presença de `QT_MAT_BAS_0_3`/`_4_5`/`QT_MAT_INF*`/
  `TP_DEPENDENCIA`, e o total 0-5 do Rio. Registrar numa tabela em `validation.md` V1.
- Se algum ano não tiver as faixas: parar, registrar em P6 e perguntar antes de seguir.

### Bloco 2: Funções (topo de `analise.py`, seção 📦)

1. `carrega_censo_escolar_matriculas(anos, cod_municipio=3304557, pasta_cache='dados_locais//educacao//inep_microdados', caminho_extrato='dados_locais//educacao//inep_matriculas_rio.csv')`:
   - se o extrato existir e cobrir `anos`, lê o extrato e retorna;
   - para cada ano faltante, baixa o ZIP se não estiver no cache. A URL de 2025 tem sufixo `_`, então há
     um dicionário de exceções `{2025: 'microdados_censo_escolar_2025_.zip'}`;
   - localiza o CSV no ZIP por regex (`microdados_ed_basica_<ano>.csv` ou `Tabela_Matricula_<ano>*.csv`,
     ignorando maiúsculas), lê de dentro do ZIP (`sep=';'`, `encoding='latin-1'`, `usecols`), filtra o
     município e agrega por `TP_DEPENDENCIA`;
   - grava o extrato com **uma linha por ano × dependência** (19 × 4 = 76 linhas), colunas
     `ano, tp_dependencia, dependencia, mat_0_a_3, mat_4_a_5, mat_inf, mat_inf_creche, mat_inf_pre`.
     `mat_inf*` fica como referência, sem ser publicado.
2. *(2026-09-24: substituído pela Parte A de `../plan.md` Bloco 1; a Parte E só chama `populacao_ripsa(...)`, e o extrato passa a ser `dados_locais/populacao/ripsa_populacao_rio.csv`. Texto original mantido como histórico:)* 2. `carrega_populacao_ripsa(anos, idades=range(0, 7), cod_municipio_tabnet='3262', caminho_extrato='dados_locais//populacao//ripsa_populacao_rio_0_6_idade_simples.csv')`:
   - se o extrato cobrir `anos`, lê o extrato;
   - senão, faz o POST no Tabnet `popsvs2024br.def` (spec §3.6): corpo codificado em latin-1, todos os
     filtros `TODAS_AS_CATEGORIAS__` exceto município e idade, `formato=prn`. Lê o bloco `<PRE>` com
     `sep=';'`, descarta a linha `Total` e a coluna `Total`, e converte para o formato longo;
   - grava o extrato `ano, idade, populacao, data_consulta` (19 × 7 = 133 linhas) e checa que
     vieram todos os anos e idades pedidos (P7).
3. `resume_matriculas_0_a_5(df_matriculas, df_populacao)` produz a tabela final por ano: `ano`,
   `matriculas` (0-5; o nome é mantido porque os leitores usam `matriculas`), `matriculas_0_a_3`,
   `matriculas_4_a_5`, `matriculas_publica`, `matriculas_privada`, `populacao_0_a_3`,
   `populacao_4_a_5`, `populacao_0_a_5`, `taxa_atendimento_0_a_3`, `taxa_atendimento_4_a_5`,
   `taxa_atendimento_0_a_5` (em %, com 1 casa, calculada depois de somar).
4. D8: `linhas_referencia=None` em `serie_temporal_multipla`, uma lista de
   `(valor, rótulo)` desenhada com `axhline` tracejado e cinza e rótulo à direita. Com `None`, não
   desenha nada.

### Bloco 3: Seção de análise (`analise.py:3166-3179`)

- Markdown: título "Matrículas e taxa de atendimento de 0 a 5 anos (Censo Escolar/INEP, 2007-2025)" e
  nota de método: faixas por escola desde a LGPD; 6 anos misturado com 7-10; data de referência; troca
  da série antiga e o porquê (spec §3.4); vale de 2021; 2025 em tabelas separadas; ressalvas da taxa
  bruta; e a **nota metodológica de D7** (spec §5, 6 pontos) numa célula markdown própria, logo acima
  do gráfico da taxa.
- Fontes: `fonte_matriculas = 'Censo Escolar da Educação Básica (INEP), microdados'` e
  `fonte_taxa_atendimento = 'Censo Escolar (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde'`.
- Saídas:
  - `tabelas_finais/matriculas_0_a_5_por_ano.csv` (tabela completa acima);
  - `visualizacoes/matriculas_0_a_5_por_ano.png`: `serie_temporal` do total;
  - `visualizacoes/matriculas_0_a_5_creche_pre_por_ano.png`: `serie_temporal_multipla` (0-3, 4-5);
  - `visualizacoes/matriculas_0_a_5_rede_por_ano.png`: `serie_temporal_multipla` (pública, privada);
  - `visualizacoes/taxa_atendimento_0_a_5_por_ano.png`: `serie_temporal_multipla` (0-3, 4-5, 0-5,
    em %), com as linhas do PNE (D8).
- `git rm` do CSV antigo em `dados_locais/educacao/`; `git add` dos dois extratos novos.

### Bloco 4: Crosswalk e relatórios

- `specs/estrutura_eixos.md` (linhas 269-274): título "Matrículas na educação básica de crianças de 0 a
  5 anos", os três PNG de matrícula e a tabela nova, **sem** `status: pendente`, nota com a definição.
  **Taxa de atendimento:** o catálogo (`painel_primeira_infancia_cesta_indicadores.xlsx`, conferido em
  2026-09-24) **não tem** indicador de atendimento por matrícula. O mais próximo é "Taxa bruta de
  frequência escolar população até 6 anos" (PNAD, domiciliar), que é outro conceito e fica como está.
  A taxa entra como **item novo** no mesmo eixo, logo abaixo das matrículas, com a nota "incluído na
  rodada `matriculas-censo-escolar`, fora do catálogo original".
- `build_html_report.py:1415-1416`: arquivo e rótulo, mais os cards novos (creche/pré, rede, taxa) com
  `option_card` e `line_chart` de várias séries. As linhas do PNE entram no `line_chart` com um parâmetro opcional equivalente (D8).
- `build_notebook_report.py:623-625`: arquivo e rótulo, `chart_block` dos PNG novos, tabela com as
  colunas principais (ano, matrículas 0-5, taxas).
- `regen_missing_pngs.py:156-159`: arquivo, título e `fonte_dados` (hoje ele não passa fonte).
- Texto de curadoria: `_texto_analise("matriculas_0_a_6_por_ano")` usa a chave antiga. Conferir se
  existe nota de curadoria com essa chave no DOCX/`analise.py` e migrar a chave. **Não escrever texto
  analítico novo** sem pedido, porque a curadoria é do usuário.
- Regenerar HTML, PDF e DOCX pela skill `export_pdf_report`.

### Bloco 5: Validação e fechamento

- Rodar `analise.py` do zero (kernel limpo, `analises_env`) e checar V2-V5.
- Roadmap: marcar "Matrículas" como feito e acrescentar ao backlog o mapa por escola geocodificada
  (spec §4.4). README: entrada curta no changelog. Constitution §3: acrescentar `populacao/` à lista de
  pastas de `dados_locais/`.
- Merge em `staging_main` só com o ok do usuário.

## Commits

Um por bloco, `SPEC-MatriculasCensoEscolar: Bloco N -- …`.
