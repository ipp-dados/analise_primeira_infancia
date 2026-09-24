# Plano técnico: Matrículas de 0 a 5 anos (Censo Escolar/INEP)

Baseado em `specification.md` (rascunho 2). IDs D1-D6 (decisões) e P1-P6 (pendências) são os da spec.
**Nada daqui em diante é executado antes de o usuário aprovar este plano.** O check de 2025 (condição de
D4) já foi feito e está em spec §3.5.

## Decisões

- **D1 ✅ 0-5**: `QT_MAT_BAS_0_3 + QT_MAT_BAS_4_5`, com idade na data padrão do Censo (última quarta-feira
  de maio). As colunas `_REF_31_03` de 2025 não são usadas.
- **D2 ✅ reconstruir**: série 2007-2025 inteira a partir dos ZIPs do INEP. Sai de uso
  `dados_locais/educacao/censo_escolar_matriculas_ate_6anos.csv` (`git rm`; o histórico fica no git e
  nesta spec, §3.4).
- **D3 ✅**: creche × pré (0-3 × 4-5) e pública × privada (`TP_DEPENDENCIA` 1-3 × 4).
- **D4 ✅**: 2025 incluído (compatível, §3.5).
- **D5 ✅**: ZIPs em `dados_locais/educacao/inep_microdados/`, gitignorado (regra já adicionada;
  `*.zip` também já era ignorado).
- **D6 (sem resposta)**: taxa de atendimento fora do escopo, vai para o roadmap.
- **Sub-decisão de D1, nome dos arquivos (proposta):** **renomear** `matriculas_0_a_6_por_ano` para
  `matriculas_0_a_5_por_ano`. Um arquivo chamado "0 a 6" com dado de 0-5 engana quem for ler.
  Custo: os dois arquivos antigos (`tabelas_finais/…csv`, `visualizacoes/…png`) estão **rastreados no
  git**, então vão para `git rm` e os novos entram com `git add -f`, mantendo o que já era versionado.
  Os leitores a ajustar são os três scripts de P4 e `estrutura_eixos.md`. Se o usuário preferir manter o
  nome, só os rótulos mudam.

## Princípios

- **Só a seção 🎓 de matrículas muda** (`analise.py:3166-3179`), mais a função nova no topo e as
  referências nos três scripts de relatório e em `estrutura_eixos.md`. A PNAD e o SIDRA logo acima
  não são tocados, exceto para renomear a variável `df_freq_escolar` reaproveitada **na célula de
  matrículas** (spec §2).
- **Uma fonte, uma definição**: todos os anos passam pela mesma função, com as mesmas colunas e a mesma
  data de referência.
- **Notebook roda offline**: o extrato do Rio versionado basta, e a rede só é usada se faltar um ano.

## Blocos

### Bloco 1: Downloads e checagem de 2007-2019 (P6)
- Baixar os 13 ZIPs de 2007-2019 para o cache (~300 MB; usar `curl --retry … -C -`, já que o INEP
  derrubou uma conexão SSL no download de 2025).
- Para cada ano: nome do CSV, encoding, presença de `QT_MAT_BAS_0_3`/`_4_5`/`QT_MAT_INF*`/
  `TP_DEPENDENCIA`, e o total 0-5 do Rio. Registrar numa tabela em `validation.md` V1.
- Se algum ano não tiver as faixas: parar, registrar em P6 e perguntar antes de seguir.

### Bloco 2: Função de carga (topo de `analise.py`, seção 📦)
`carrega_censo_escolar_matriculas(anos, cod_municipio=3304557, pasta_cache='dados_locais//educacao//inep_microdados', caminho_extrato='dados_locais//educacao//inep_matriculas_rio.csv')`:
1. Se o extrato existir e cobrir `anos`, lê o extrato e retorna.
2. Para cada ano faltante: baixa o ZIP se não estiver no cache. A URL de 2025 tem sufixo `_`, então
   há um dicionário de exceções `{2025: 'microdados_censo_escolar_2025_.zip'}`.
3. Localiza o CSV no ZIP por regex (`microdados_ed_basica_<ano>.csv` ou `Tabela_Matricula_<ano>*.csv`,
   ignorando maiúsculas), lê de dentro do ZIP (`sep=';'`, `encoding='latin-1'`, `usecols`), filtra o
   município e agrega por `TP_DEPENDENCIA`.
4. Devolve e grava o extrato: **uma linha por ano × dependência** (19 anos × 4 = 76 linhas), colunas
   `ano, tp_dependencia, dependencia, mat_0_a_3, mat_4_a_5, mat_inf, mat_inf_creche, mat_inf_pre`.
   `mat_inf*` fica como referência, sem ser publicado.

Mais uma função pequena, `resume_matriculas_0_a_5(df_extrato)`, que produz a tabela final por ano:
`ano, matriculas` (0-5; o nome da coluna é mantido porque os leitores usam `matriculas`), `matriculas_0_a_3`,
`matriculas_4_a_5`, `matriculas_publica`, `matriculas_privada`.

### Bloco 3: Seção de análise (`analise.py:3166-3179`)
- Markdown: título "Número de matrículas de 0 a 5 anos (Censo Escolar/INEP, 2007-2025)" e nota de método
  (faixas por escola desde a LGPD; 6 anos misturado com 7-10; data de referência; troca da série antiga
  e o porquê (spec §3.4); vale de 2021; 2025 em tabelas separadas).
- `fonte_matriculas = 'Censo Escolar da Educação Básica (INEP), microdados'`.
- Saídas:
  - `tabelas_finais/matriculas_0_a_5_por_ano.csv` (tabela completa acima);
  - `visualizacoes/matriculas_0_a_5_por_ano.png`: `serie_temporal` do total;
  - `visualizacoes/matriculas_0_a_5_creche_pre_por_ano.png`: `serie_temporal_multipla` (0-3, 4-5);
  - `visualizacoes/matriculas_0_a_5_rede_por_ano.png`: `serie_temporal_multipla` (pública, privada).
- `git rm` do CSV antigo em `dados_locais/educacao/` e `git add` do extrato novo.

### Bloco 4: Crosswalk e relatórios
- `specs/estrutura_eixos.md` (linhas 269-274): título "Matrículas na educação básica de crianças de 0 a
  5 anos", os três PNG e a tabela nova, **sem** `status: pendente`, nota com a definição.
- `build_html_report.py:1415-1416`: arquivo e rótulo, mais os cards das duas séries novas (mesmo
  `option_card`, com `line_chart` de 2 séries).
- `build_notebook_report.py:623-625`: arquivo e rótulo, `chart_block` dos dois PNG novos, tabela com as
  colunas novas.
- `regen_missing_pngs.py:156-159`: arquivo, título e `fonte_dados` (hoje ele não passa fonte).
- Texto de curadoria: `_texto_analise("matriculas_0_a_6_por_ano")` usa a chave antiga. Conferir se
  existe nota de curadoria com essa chave no DOCX/`analise.py` e migrar a chave. **Não escrever texto
  analítico novo** sem pedido, porque a curadoria é do usuário.
- Regenerar HTML, PDF e DOCX pela skill `export_pdf_report`.

### Bloco 5: Validação e fechamento
- Rodar `analise.py` do zero (kernel limpo, `analises_env`) e checar V2-V4.
- Roadmap: marcar "Matrículas" como feito e acrescentar D6 (taxa de atendimento) e o mapa por escola
  geocodificada (spec §4.4). README: entrada curta no changelog.
- Merge em `staging_main` só com o ok do usuário.

## Commits
Um por bloco, `SPEC-MatriculasCensoEscolar: Bloco N -- …`.
