# Plano técnico: População de referência

Baseado em `specification.md` (rascunho 1). As partes A-E e as decisões são as da spec. A Parte E tem plano
próprio em `matriculas/plan.md`, e aqui só entra a posição dela na sequência. **Nada é executado antes da
revisão e do ok do usuário.**

## Sequência (população primeiro)

| Bloco | Parte | Conteúdo | Depende de |
|---|---|---|---|
| 1 | A | Função Ripsa, extrato, nota geral A5 | — |
| 2 | A | Série de população infantil (A2) e taxas municipais novas (A3, A4) | 1 |
| 3 | B | Rótulos e notas sub-municipais (B2, B3) | 1 (a nota B3 cita números da Ripsa) |
| 4 | E | Matrículas: Blocos 1-3 de `matriculas/plan.md` (downloads, funções, seção de análise) | 1 |
| 5 | D | Item 7 (percentual de nascidos vivos por bairro), itens do crosswalk sem arquivo, aviso no gerador | 2 (D2 usa A2) |
| 6 | todos | Crosswalk e relatórios: `estrutura_eixos.md`, os três scripts de relatório, regeneração de HTML, PDF e DOCX (inclui o Bloco 4 de `matriculas/plan.md`) | 2-5 |
| 7 | C | Auditoria de faixas (C1) → lista para o usuário → rótulos (C2) → renomeações aprovadas (C3) → nova regeneração | 6 |
| 8 | — | Validação completa, notebook do zero, docs (roadmap, README, constitution, CLAUDE.md), merge | 7 |

A Parte C vem por último porque renomeia arquivos criados nos blocos anteriores. Fazer antes seria renomear
duas vezes.

## Princípios

- **Uma referência por nível**: Ripsa para o município e Censo 2022 abaixo dele. Nenhuma saída mistura as
  duas sem dizer.
- **Somar antes de dividir** (constitution §3), inclusive nas taxas municipais novas.
- **Notebook offline**: extratos versionados em `dados_locais/populacao/` e `dados_locais/educacao/`. A rede
  só é usada se faltar um ano.
- **Notas de curadoria são do usuário**: não são reescritas. O que estiver desatualizado vai para uma lista.
- **Escopo de alteração**: funções novas no topo de `analise.py`; células novas nas seções Censo 2022,
  violência, CadÚnico, nascidos vivos e educação; rótulos e fontes nas saídas sub-municipais; os três
  scripts de relatório; `estrutura_eixos.md`. Nenhum cálculo sub-municipal existente muda (B1).

## Blocos

### Bloco 1: Parte A, base

- `carrega_populacao_ripsa(anos=range(2000, 2026), idades=range(0, 7), caminho_extrato='dados_locais//populacao//ripsa_populacao_rio.csv')`:
  - extrato existe e cobre o pedido → lê e retorna;
  - senão, duas consultas POST ao `popsvs2024br.def` (`Linha=Ano`, `Coluna=Sexo`, uma por idade, ou
    `Coluna=Idade_simples` com filtro de sexo, a escolher pelo que o Tabnet aceitar), mais uma do total de
    todas as idades. Corpo em latin-1, até 5 tentativas com espera, parse do `<PRE>` (`sep=';'`);
  - grava o formato longo `ano, idade, sexo, populacao, data_consulta` (364 linhas), com `idade='total'`
    e `sexo='total'` para o total por ano (26 linhas);
  - confere 26 anos × 7 idades × 2 sexos e que a soma dos sexos bate com o total por idade.
- Helper `populacao_ripsa(df, anos, idade_min, idade_max, sexo='total')` que devolve `ano, populacao` já
  somado, usado por A2, A3, A4 e E.
- Nota A5 (markdown) no início da seção Censo 2022, com a tabela Ripsa × Censo de spec §3.
- Constitution §3: acrescentar `populacao/` à lista de pastas. (Pode ir no Bloco 8, junto com o resto
  das docs.)

### Bloco 2: Parte A, saídas

- **A2**, na seção Censo 2022, depois da evolução 2000/2010/2022:
  `tabelas_finais/populacao_ripsa_0_a_6_por_ano.csv` (`ano`, população de 0 a 6 por idade, `populacao_0_a_5`,
  `populacao_0_a_6`, `populacao_total`, `percentual_0_a_6`) e
  `visualizacoes/populacao_ripsa_0_a_6_por_ano.png` (`serie_temporal` do total 0-6), com
  `fonte_dados='Estimativas populacionais Ripsa/Ministério da Saúde (2000-2025)'`. Se A-D1 mudar, só as
  colunas e o título mudam.
- **A3**, na seção de violência, depois de T1: `tabelas_finais/violencia_familiar_taxa_municipio_ano.csv`
  (`ano`, casos por vínculo, `populacao_0_a_5`, `taxa_por_mil_<vinculo>`) e
  `visualizacoes/violencia_familiar_taxa_municipio_ano.png` (`serie_temporal_multipla` mãe/pai/outros, com a
  marca de 2017 como no G1, se a função permitir; senão só a nota). Usa `taxa_por_mil` já existente.
- **A4**, na seção CadÚnico: uma célula que calcula a razão municipal e grava
  `tabelas_finais/cadunico_razao_populacao_0_a_5_2026.csv` (uma linha: crianças, população Ripsa 2025,
  razão), com a nota das ressalvas. Sem gráfico, porque é um número só; no HTML vira um KPI se o card
  existir, senão uma linha de tabela. Só roda com `.env` (P-A2).

### Bloco 3: Parte B

- Levantar todas as `fonte_dados` e títulos das saídas sub-municipais com população no denominador
  (violência M8-M13 e G8, tabelas `violencia_familiar_taxa_*`) e deixar explícito
  "população de 0 a 4 anos, Censo 2022".
- Nota da ressalva D9 acrescida dos pontos B3 (anos diferentes, subcontagem do Censo).
- `build_html_report.py`: rótulos de fonte dos cards correspondentes (P-B1).

### Bloco 4: Parte E

`matriculas/plan.md` Blocos 1-3, com duas mudanças: a população vem de `populacao_ripsa(...)` (Bloco 1
daqui), e não de uma função própria; e a nota D7 aponta para A5.

### Bloco 5: Parte D

- **D1 (item 7)**, na seção Nascidos vivos, depois do mapa de contagem: calcular por bairro de 2025
  `percentual_nascidos_vivos_municipio = nascidos vivos do bairro ÷ total do município × 100`. O
  denominador inclui "EM BRANCO", depois de conferir P-D1. Tabela gêmea
  `tabelas_finais/tabela_mapa_nascidos_vivos_percentual_2025.csv` e mapa
  `mapas/mapa_percentual_nascidos_vivos_bairro_2025.png` (contínuo, `_CORES_TEMA_MAPA['natalidade']`,
  `fonte_datasus_bairro`).
- **D2**: crosswalk "Crianças até 6 anos (número)" aponta para as saídas de A2.
- **D3**: gráfico do Total por idade da SIDRA 10057 (`grafico_barra`) e tabela, ligados ao item.
- Mortalidade evitável por sexo: `status: pendente` no crosswalk.
- **D4**: aviso no console do `build_html_report.py` e do `build_notebook_report.py` para itens sem
  arquivo e sem status.

### Bloco 6: Crosswalk e relatórios

- `estrutura_eixos.md`: itens novos e atualizados de A2, A3, A4, D1-D3 e E, cada um com a fonte.
- `build_html_report.py`, `build_notebook_report.py`, `regen_missing_pngs.py`: cards e blocos de A2, A3, A4,
  D1, D3 e E (Bloco 4 de `matriculas/plan.md`), incluindo `linhas_referencia` (D8 de E).
- Regenerar HTML, PDF e DOCX pela skill `export_pdf_report` e comparar com o baseline (contagem de cards,
  tamanho, páginas).

### Bloco 7: Parte C

1. **C1**: gerar `auditoria_faixas.md` (fonte → faixa real → data de referência → rótulos e arquivos
   encontrados), varrendo `analise.py`, `tabelas_finais/`, `visualizacoes/`, `mapas/` e os três scripts.
2. **Parar e mostrar ao usuário** a lista de rótulos a corrigir, as renomeações propostas e as notas de
   curadoria afetadas (C-D1).
3. **C2/C3** depois do ok: rótulos em `analise.py` e nos scripts, renomeações com `git rm`/`git add -f`, e
   leitores ajustados.
4. Regenerar os relatórios de novo.

### Bloco 8: Validação e fechamento

- Notebook do zero no `analises_env` (kernel limpo, cwd na raiz) e `validation.md` inteiro.
- Docs: roadmap (itens 6, 7 e Matrículas; B1 (b)/(c) no backlog), README (changelog curto), constitution §3
  (`populacao/`; referência de população por nível como convenção), CLAUDE.md (nova convenção de
  população de referência).
- Merge em `staging_main` só com o ok do usuário.

## Commits

Um por bloco: `SPEC-PopulacaoReferencia: Bloco N (Parte X) -- …`.

## Cuidado registrado

Em 2026-09-24 uma checagem que executou o cabeçalho de `analise.py` fora do notebook rodou células de
análise e regravou 6 saídas rastreadas (ordem de linhas e PNG re-renderizado). Elas foram restauradas com
`git restore`. **Checagens pontuais devem carregar só as funções necessárias via `ast`**, nunca executar
o arquivo por fatia de texto.
