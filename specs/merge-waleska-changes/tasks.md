# Tarefas — Merge das mudanças da Waleska

Ordem de execução. Blocos 0-3 já foram executados (marcados `[x]`) antes destes documentos
existirem — `tasks.md`/`validation.md` foram escritos depois, a pedido do usuário, para trazer
esta spec ao mesmo padrão de documentação das demais (`specs/mortalidade-ap`,
`specs/maps-and-ibge`, `specs/visual-identity`). Blocos 4-5 são o trabalho que falta.

---

## Bloco 0 — Levantamento e decisão

- [x] **T0.1** — Revisar os 4 commits de `origin/waleska-analise-primeira-infancia` (`git log`
      + `git diff` contra `origin/staging_main`) e resumir em `specs.md` antes de tocar em
      qualquer coisa
- [x] **T0.2** — Testar o merge com `--no-commit --no-ff`, confirmar zero conflitos, reverter
      (`git merge --abort`) antes de decidir a estratégia
- [x] **T0.3** — Levantar os riscos de pipelines downstream (grep cruzado contra
      `build_notebook_report.py`/`build_html_report.py`/`regen_missing_pngs.py`)
- [x] **T0.4** — Confirmar com o usuário (`AskUserQuestion`): restaurar o CSV do Censo perdido
      por acidente? **Sim.** Corrigir os scripts de relatório na mesma leva? **Sim.**

---

## Bloco 1 — Merge real

- [x] **T1.1** — Criar `specs/merge-waleska-changes/specs.md` documentando o plano **antes**
      de executar (commit `dc5118d`)
- [x] **T1.2** — `git merge --no-ff origin/waleska-analise-primeira-infancia`, preservando os
      4 commits e a autoria da Waleska (commit `ed964a5`)
- [x] **T1.3** — Confirmar zero conflitos e diff idêntico ao testado no Bloco 0

---

## Bloco 2 — Correções de acompanhamento

- [x] **T2.1** — Restaurar `df_serie_censo.to_csv('tabelas_finais//censo_0_a_4_anos_por_ano.csv')`
      em `analise.py`, logo após o cálculo do percentual (`plan.md` §2)
- [x] **T2.2** — `build_notebook_report.py`: remover a seção "Óbitos por causas evitáveis por
      raça/cor" (`h5` + 2 gráficos + variações sem "não informada")
- [x] **T2.3** — `build_notebook_report.py`: remover `_SLUG_SUBGRUPO_PDF` e o bloco
      `h6('Por CAP e faixa etária, por subgrupo')` (matriz de 18 gráficos)
- [x] **T2.4** — `build_notebook_report.py`: remover `h6('Gestação e parto, menores de 1 ano,
      por CAP')` (2 séries)
- [x] **T2.5** — `build_notebook_report.py`: remover o `chart_block` de
      `cobertura_vacinal_epi_ano.png` (manter a tabela, que ainda tem CSV)
- [x] **T2.6** — `build_notebook_report.py`: `MAP_GROUPS` — remover as 4 entradas AP/RP do
      Censo, o grupo inteiro "Gravidez e puerpério" (as 2 entradas, sem substituto), as 2
      entradas absolutas de neonatal tardia/pós-neonatal (mantidas as de taxa) e as 2 entradas
      de gestação/parto por CAP
- [x] **T2.7** — `build_html_report.py`: remover a seção `h3('Por raça/cor (0-364 dias)')`
      (lê `mortalidade_causas_evitaveis_raca_municipio_ano.csv`, que não existe mais)
- [x] **T2.8** — `build_html_report.py`: remover o grupo de mapas "Por subgrupo (gestação e
      parto)" (lê `tabela_mapa_obitos_evitaveis_{slug}_menores_1_ano_cap_2025.csv`, idem)
- [x] **T2.9** — Verificar com `grep` que nenhuma referência às saídas removidas sobrou em
      nenhum dos 2 scripts (`plan.md` §2, tabela completa)
- [x] **T2.10** — `ast.parse` em `analise.py`, `build_notebook_report.py` e
      `build_html_report.py` — os 3 continuam sintaticamente válidos
- [x] **T2.11** — Commit das correções (`0facf8a`)

---

## Bloco 3 — Validação numérica independente (sem ambiente completo)

- [x] **T3.1** — Instalar só `pandas` (`pip install pandas`, rede HTTPS disponível mesmo sem
      SSH pro GitHub) — suficiente pra reproduzir a lógica de `total_e_percentual_ano`
- [x] **T3.2** — Rodar a versão antiga e a nova da função contra os 3 CSVs reais do Censo
      (2000/2010/2022) e comparar o percentual resultante — `plan.md` §3, resultado: antigo
      751-1.092% (sem sentido), novo 4,75-7,09% (plausível)
- [x] **T3.3** — Registrar o resultado em `plan.md` e `validation.md` com os números exatos

---

## Bloco 4 — Validação em runtime (pendente — precisa de ambiente com DB/rede completos)

- [ ] **T4.1** — Rodar `analise.py` de ponta a ponta (kernel limpo, Jupyter/Jupytext) num
      ambiente com acesso ao Postgres do CadÚnico e rede para os tiles do `contextily`
- [ ] **T4.2** — Conferir que as saídas que **não foram tocadas** pela curadoria continuam
      idênticas (ex.: `mapa_mortalidade_infantil_bairro_2025.png`, mapas de raça/cor por
      bairro, PNADs/SIDRA) — nenhuma regressão fora do escopo da Waleska
- [ ] **T4.3** — Conferir visualmente os gráficos com título/legenda alterados (SISVAN, Censo,
      "Proporção de óbitos evitáveis entre os óbitos" por CAP)
- [ ] **T4.4** — Rodar o skill `export_pdf_report` de ponta a ponta
      (`regen_missing_pngs.py` → `extract_maps.py` → `build_notebook_report.py` → Chrome
      headless) e confirmar que o PDF é gerado sem `FileNotFoundError`/`SystemExit`
- [ ] **T4.5** — Rodar `build_html_report.py` e confirmar que `relatorio/index.html` é gerado
      sem erro, e que a seção "Óbitos por causas evitáveis" não deixa buraco visual onde a
      subseção de raça/cor foi removida
- [ ] **T4.6** — `jupytext --sync analise.py` para atualizar `analise.ipynb`

→ **valida com V6, V7, V8 de `validation.md`**

---

## Bloco 5 — Fechamento

- [ ] **T5.1** — Atualizar `README.md` (`## Recent changes`, `## Update Table`) resumindo o
      merge — só depois do Bloco 4, para descrever o estado validado, não só o pretendido
- [ ] **T5.2** — Merge de `specs/merge-waleska-changes` em `planning` (fast-forward — nenhum
      commit novo em `planning` desde que este branch foi criado)
- [ ] **T5.3** — Decisão do usuário: subir para `staging_main` agora, ou deixar acumulando em
      `planning` junto com outras mudanças da reorganização?
