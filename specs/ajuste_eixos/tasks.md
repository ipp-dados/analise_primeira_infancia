# Tasks — specs/ajuste_eixos

## Bloco 0 — Decisões
- [x] **T0.1** — `specs.md` revisado e aprovado pelo usuário (decisões A-G, §3).
- [x] **T0.2** — Lista de descarte (18 indicadores) confirmada pelo usuário (§4.4).
- [x] **T0.3** — Branch `planning` já é a branch de trabalho desta rodada (sem
      necessidade de criar `spec/ajuste-eixos` separada, a confirmar se o
      usuário preferir isolar).
- [ ] **T0.4** — Default do risco §9.1 (`plan.md`, topo) — **manter ordem
      técnica de `analise.py`, sem reordenação física de célula** — revisado
      pelo usuário antes de iniciar o Bloco 2. Reverter para reordenação real
      se o usuário discordar aqui.
- [ ] **T0.5** — Local de `specs/estrutura_eixos.md` (raiz de `specs/`) e nome
      final do script/skill do Bloco 1/6 revisados pelo usuário.

## Bloco 1 — Crosswalk completo + `specs/estrutura_eixos.md` (plan.md §1)
- [ ] **T1.1** — Script de classificação (`classifica_bucket`/`eh_descartado`/
      `comeca_com_ok`) escrito e conferido contra os totais já validados em
      `specs.md` §4.3 (47 ativos: 15/10/7/5/6/4 por eixo).
- [ ] **T1.2** — Casamento indicador → arquivo real feito para os 6 eixos
      ativos, um de cada vez, seguindo o método do exemplo "Alimentação"
      (`specs.md` §4.5): **Prioridade (sem secundário)**, **Inclusão**,
      **Família e Cuidados**, **Proteção** (sem arquivo real — só os campos
      `status: pendente` + `nota`), **Moradia** (idem, sem arquivo real).
- [ ] **T1.3** — Confirmado: todo indicador "a reservar" (16, `specs.md` §4.3)
      tem `status: pendente` + `nota` explicando o motivo (reaproveitar a
      coluna `Status` do catálogo como base da nota).
- [ ] **T1.4** — Resolvida a duplicidade "Territórios com risco a inundação"
      (`specs.md` §9.2) — entra uma única vez, em Moradia.
- [ ] **T1.5** — `specs/estrutura_eixos.md` gerado e commitado.
- [ ] **T1.6** — `parse_estrutura_eixos()`/`valida_estrutura()` escritos e
      testados contra o arquivo gerado — `valida_estrutura` não acusa
      nenhuma referência quebrada.

## Bloco 2 — `analise.py`/`analise.ipynb` (plan.md §2)
- [ ] **T2.1** — Seção final "Análise / Relatório" renomeada: 5 subtítulos
      antigos → 6 eixos ativos.
- [ ] **T2.2** — Nota markdown nova após "📦 Pacotes e Funções Auxiliares"
      apontando para `specs/estrutura_eixos.md`.
- [ ] **T2.3** — `CLAUDE.md` atualizado (nota sobre a organização de
      apresentação vs. ordem técnica do arquivo).
- [ ] **T2.4** — `jupytext --sync analise.py` rodado; `analise.ipynb` reflete
      as mudanças de markdown.
- [ ] **T2.5** — Notebook reexecutado do zero (kernel limpo,
      `jupyter nbconvert --to notebook --execute --inplace`) — 0 células com
      erro (confirma que só markdown mudou, nenhuma célula de código foi
      afetada).

## Bloco 3 — `relatorio/index.html` por eixo (plan.md §3)
- [ ] **T3.1** — `build_html_report.py` passa a iterar
      `parse_estrutura_eixos()` em vez das 9 seções hardcoded.
- [ ] **T3.2** — `emite_bloco_pendente` implementado (selo "🚧" + nota,
      mesmo estilo visual do bloco "Principais achados").
- [ ] **T3.3** — Faixa de texto de análise ajustada para 100-200 palavras em
      todo bloco (não mais fixo em 150).
- [ ] **T3.4** — Navbar/sumário lista as 6 seções por eixo.
- [ ] **T3.5** — Geração completa sem erro; contagem de `h2` = 6 (não mais 9).
- [ ] **T3.6** — Inspeção visual: pelo menos 1 seção com conteúdo real
      (Alimentação) e 1 com blocos pendentes (Proteção ou Moradia) — o selo
      de pendente aparece corretamente, sem imagem/gráfico quebrado.

## Bloco 4 — PDF por eixo (plan.md §4)
- [ ] **T4.1** — `build_notebook_report.py` passa a ler a mesma
      `parse_estrutura_eixos()` do Bloco 3.
- [ ] **T4.2** — Equivalente impresso do bloco pendente (parágrafo com
      borda/itálico, já que não há cor de fundo em PDF impresso) implementado.
- [ ] **T4.3** — PDF gerado de ponta a ponta (pipeline Chrome headless já
      existente) — contagem de páginas condizente com o conteúdo (6 seções
      grandes em vez de 9 menores, mesmo total de visualizações).
- [ ] **T4.4** — Amostra rasterizada (capa, 1 seção com conteúdo real, 1 com
      blocos pendentes) inspecionada visualmente.

## Bloco 5 — DOCX de curadoria (plan.md §5)
- [ ] **T5.1** — `python-docx` adicionado a `requirements.txt` e instalado.
- [ ] **T5.2** — `id_bloco()` implementado e conferido: nenhum ID colide
      entre indicadores diferentes (checar duplicata por hash/set).
- [ ] **T5.3** — `gera_docx_curadoria.py` escrito — heading por eixo/
      subseção, imagem PNG real (não SVG) por visualização/mapa, bloco de
      texto lorem ipsum (100-200 palavras) por opção.
- [ ] **T5.4** — Bookmark por bloco de texto implementado
      (`w:bookmarkStart`/`w:bookmarkEnd`) — confirmado abrindo o DOCX gerado
      e inspecionando o XML interno (`docx` é um zip, extrair
      `word/document.xml` e grep pelos IDs).
- [ ] **T5.5** — Regeneração não-destrutiva testada: editar manualmente 1
      bloco de texto no DOCX gerado, rodar o gerador de novo passando o
      arquivo editado como `docx_anterior`, confirmar que o texto editado
      sobrevive e o resto continua lorem ipsum.
- [ ] **T5.6** — Apêndice "Textos órfãos" testado: remover 1 indicador da
      `estrutura_eixos.md` que já tinha texto curado, regenerar, confirmar
      que o texto aparece no apêndice em vez de sumir.
- [ ] **T5.7** — Múltiplas opções no mesmo bloco (ex. um indicador do
      catálogo que hoje tem seletor de pills no HTML) — confirmado que o
      DOCX lista 1 heading + 1 texto por opção, em sequência.

## Bloco 6 — Skill de reestruturação (plan.md §6)
- [x] **T6.1** — `SKILL.md` de `export_pdf_report` atualizado com o pipeline
      de 5 passos (regen PNGs → valida estrutura → HTML → PDF → DOCX).
- [x] **T6.2** — Pipeline executado de ponta a ponta 1x, do zero, sem
      intervenção manual entre os passos (passo 1 produziu um diff
      incidental conhecido em `visualizacoes/*.png`, revertido — não é uma
      falha do pipeline, ver caveat registrado no próprio `SKILL.md`).
- [x] **T6.3** — Teste do fluxo real do usuário (`specs.md` §5.2): editar
      `specs/estrutura_eixos.md` à mão (mover 1 indicador de eixo, renomear
      1 subseção) e regenerar — **resultado real, não o esperado
      originalmente**: a mudança aparece no DOCX (importa
      `parse_estrutura_eixos()` de verdade), mas não no HTML/PDF
      (`relatorio/index.html` saiu byte-idêntico ao anterior) — os dois
      geradores são Python hardcoded, não leem o `.md` em tempo de
      execução. Decisão do usuário registrada em `specs.md` §9.3: manter
      assim, documentar a limitação, tratar mudança de estrutura que afete
      HTML/PDF como ajuste de código manual. Edição de teste revertida
      depois de confirmado (não é uma mudança real de estrutura).

## Bloco 7 — Skill de sincronização do DOCX (plan.md §7)
- [x] **T7.1** — `eh_lorem_ipsum()` implementado e testado — comparação
      exata (não heurística) contra `_lorem(id_)` recalculado on-the-fly;
      0 falsos positivos contra o `.docx` real (100% lorem ipsum hoje).
      Achado durante a implementação: o nome do bookmark gravado no `.docx`
      (`_bookmark_name(id_)`, sanitizado/truncado+hash) não bate byte a
      byte com o `id_` original em 26 dos 84 blocos — corrigido comparando
      contra o `id_` reconstruído (`_mapa_bookmark_para_id`), não contra o
      nome do bookmark diretamente (que teria dado falso positivo e
      gravado a chave errada no JSON).
- [x] **T7.2** — `sincroniza_docx()` escrito — propaga texto real para
      `relatorio/textos_curados.json` (lido por `_texto_analise()` em
      ambos os geradores, Blocos 3-4) e regenera HTML/PDF-source via
      subprocess.
- [x] **T7.3** — Propagação para `analise.py`: nota markdown inserida logo
      após a célula de código que produz o arquivo correspondente ao
      `id_`, localizada por `nome_arquivo=` (2ª fase: `.png`/`.csv`/`.xlsx`
      literal) — busca em duas fases porque um mesmo stem costuma nomear
      tanto uma tabela (`to_csv`, célula anterior) quanto o gráfico
      (`nome_arquivo=`, célula posterior); buscar misturado pegaria a
      célula errada. Idempotente via marcador `<!-- nota-curadoria:ID -->`.
- [x] **T7.4** — Teste de ponta a ponta (feito duas vezes, uma pelo agente
      que implementou e uma independente pela sessão coordenadora, em
      blocos diferentes): editar 1 bookmark numa cópia de teste do `.docx`,
      rodar `sincroniza_docx.py`, confirmar texto no JSON, no HTML
      regenerado, na HTML-fonte do PDF regenerada e como nota markdown em
      `analise.py` — demais blocos (ainda lorem ipsum) inalterados.
      Segunda rodada sobre a mesma edição confirma idempotência (nota
      substituída in-place, não duplicada). Edições de teste revertidas
      (`git restore` + `jupytext --sync`) — nada de teste ficou commitado.
- [x] **T7.5** — `jupytext --sync analise.py` chamado automaticamente por
      `aplica_notas_em_analise()` sempre que uma nota é escrita; confirmado
      sem divergência (`returncode=0`) nos dois testes de ponta a ponta.

## Bloco 8 — Documentação (plan.md §8)
- [x] **T8.1** — `requirements.txt` com `python-docx` (Bloco 5).
- [x] **T8.2** — `CLAUDE.md` atualizado (Bloco 2).
- [x] **T8.3** — `specs/roadmap.md` item 3 marcado concluído, apontando para
      `specs/ajuste_eixos/` (com a ressalva §9.1/§9.3 registrada).
- [x] **T8.4** — `specs/tech-stack.md` com entrada de DOCX/`python-docx`
      (seção "Exportação em PDF/DOCX") e as 2 decisões descartadas
      (reordenar `analise.py`, renderizador genérico guiado pelo `.md`).
- [x] **T8.5** — `relatorio/specs.md` com nova entrada de versão (v7)
      descrevendo a reorganização por eixo, o Sumário/Introdução, e as
      limitações conhecidas da sincronização DOCX.

## Bloco 9 — Geração completa e validação (ver `validation.md`)
- [x] **T9.1** — Sem reexecução nova necessária: os únicos toques em
      `analise.py` desde o T2.5 (Bloco 2) foram edições de TESTE do Bloco 7
      (`sincroniza_docx.py`), todas revertidas via `git restore` +
      `jupytext --sync` logo depois de validadas — `analise.py` commitado
      hoje é byte-a-byte o mesmo validado no T2.5 (0 erros, reexecução
      completa de kernel limpo). Confirmado via `git diff` vazio contra o
      commit do Bloco 2.
- [x] **T9.2** — HTML, PDF (fonte + render) e DOCX regenerados na mesma
      rodada a partir do `estrutura_eixos.md` commitado: 6 eixos em todos
      os 3 (HTML 7 `<h2>`/PDF 8 `<h2>` por causa de Introdução/Apêndice,
      DOCX 7 `<h2 level=1>` — front-matter de cada um, não divergência de
      eixo), 16 pending-block em HTML e PDF, 47 `<h2 level=2>` no DOCX
      (subseções, pendentes incluídas) — tudo batendo.
- [x] **T9.3** — Todos os critérios de `validation.md` (V1-V8) conferidos
      nesta rodada final (ver "Resultado final" em `validation.md`).

## Bloco 10 — Fechamento
- [x] **T10.1** — `validation.md` fechado com o resultado final (V1-V8
      todos passaram; 2 descobertas de escopo registradas com decisão do
      usuário, não reabertas).
- [ ] **T10.2** — Merge em `staging_main` — **só após aval explícito do
      usuário**, como de costume (`specs/constitution.md` §7).
