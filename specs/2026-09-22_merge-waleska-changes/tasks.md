# Tarefas — Merge das mudanças da Waleska

Ordem de execução. Blocos 0-3 já foram executados (marcados `[x]`) antes destes documentos
existirem — `tasks.md`/`validation.md` foram escritos depois, a pedido do usuário, para trazer
esta spec ao mesmo padrão de documentação das demais (`specs/2026-09-08_mortalidade-ap`,
`specs/2026-09-09_maps-and-ibge`, `specs/2026-09-09_visual-identity`). Blocos 4-5 são o trabalho que falta.

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

- [x] **T1.1** — Criar `specs/2026-09-22_merge-waleska-changes/specs.md` documentando o plano **antes**
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

## Bloco 4 — Validação em runtime ✅ feito

Ambiente montado nesta sessão: `pip install -r requirements.txt` (exceto `pywinpty`,
Windows-only) em `analise_env/`; execução isolada em scratch para não sobrescrever as saídas
reais do projeto (`validation.md` V6).

- [x] **T4.1** — Rodar `analise.py` de ponta a ponta via `jupyter nbconvert --execute
      --allow-errors` — 117/134 células passam; as 17 que falham são todas da seção CadÚnico
      (sem `.env`/Postgres nesta sessão, esperado — `validation.md` V6.2)
- [x] **T4.2** — Conferir que as saídas não tocadas continuam idênticas — ✅
      `mapa_mortalidade_infantil_bairro_2025.png` e afins gerados normalmente (`validation.md` V6.4)
- [x] **T4.3** — **Achado real durante a execução (não previsto no plano)**: uma célula ativa
      sobrevivente da curadoria referenciava `df_percentual_evitaveis_municipio`/
      `rotulos_raca_evitaveis_sem_nao_informado`, ambas só definidas em código que a própria
      Waleska tinha comentado — `NameError` ao rodar de verdade, invisível ao grep estático do
      Bloco 2. Corrigido (commentada, commit `bcdfa08`) e revalidado — `validation.md` V6.5
- [x] **T4.4** — Rodar `regen_missing_pngs.py` + `build_notebook_report.py` — ambos completam
      sem `FileNotFoundError`/`SystemExit` (`validation.md` V7.1-V7.2); render final para PDF
      via Chrome headless **não testado** (fora do escopo desta validação de conteúdo)
- [x] **T4.5** — Rodar `build_html_report.py` — completa sem erro, e confirmado por grep que a
      seção "Óbitos por causas evitáveis" não deixa nenhum título órfão das subseções
      removidas (`validation.md` V7.3-V7.5)
- [x] **T4.6** — `jupytext --sync analise.py` rodado (commit `bcdfa08` já reflete o notebook sincronizado)

→ **validado, ver `validation.md` V6-V8**

---

## Bloco 5 — Fechamento

- [x] **T5.1** — `README.md` atualizado (`## Recent changes`, `## Update Table`) resumindo o
      merge já validado
- [x] **T5.2** — Merge de `specs/2026-09-22_merge-waleska-changes` em `planning`
- [ ] **T5.3** — Decisão do usuário: subir para `staging_main` agora, ou deixar acumulando em
      `planning` junto com outras mudanças da reorganização?
