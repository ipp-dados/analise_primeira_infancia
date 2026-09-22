# Validação — Merge das mudanças da Waleska

Cada checagem tem um critério de aceite objetivo. As marcadas **✅ passou** já foram executadas
nesta sessão (comandos reproduzidos abaixo); as marcadas **⏳ pendente** precisam de um
ambiente com acesso ao Postgres do CadÚnico e/ou rede para tiles do `contextily`, indisponíveis
aqui — ver `plan.md` §4.

---

## V1 — Merge sem conflitos

| # | checagem | aceite | resultado |
|---|---|---|---|
| V1.1 | `git merge --no-commit --no-ff origin/waleska-analise-primeira-infancia` a partir do HEAD pré-merge | sem marcadores `<<<<<<<`/`=======`/`>>>>>>>` | ✅ passou — `grep -c` retornou 0 |
| V1.2 | Diff do merge de teste == diff de Waleska contra sua própria base | `+206 -191` em `analise.py`, idêntico nas duas medições | ✅ passou |
| V1.3 | Merge real (`--no-ff`, sem `--no-commit`) reproduz o mesmo resultado | mesmo diff, commit `ed964a5` criado | ✅ passou |

Comando:
```bash
git merge --no-commit --no-ff origin/waleska-analise-primeira-infancia
grep -c "^<<<<<<<\|^=======\|^>>>>>>>" analise.py   # 0
git diff --stat HEAD -- analise.py                   # +206 -191
git merge --abort
```

---

## V2 — Integridade sintática

| # | checagem | aceite | resultado |
|---|---|---|---|
| V2.1 | `analise.py` é Python válido após o merge | `ast.parse` sem exceção | ✅ passou |
| V2.2 | `build_notebook_report.py` válido após as correções | idem | ✅ passou |
| V2.3 | `build_html_report.py` válido após as correções | idem | ✅ passou |

```bash
python3 -c "import ast; [ast.parse(open(f, encoding='utf-8').read()) for f in [
    'analise.py',
    '.claude/skills/export_pdf_report/scripts/build_notebook_report.py',
    '.claude/skills/export_pdf_report/scripts/build_html_report.py']]"
```

---

## V3 — Nenhuma referência solta a saída removida

| # | checagem | aceite | resultado |
|---|---|---|---|
| V3.1 | `build_notebook_report.py` não referencia mais nenhuma das saídas da tabela de `plan.md` §2 | grep vazio | ✅ passou |
| V3.2 | `build_html_report.py` idem | grep vazio (só o comentário explicativo que cita os nomes) | ✅ passou |
| V3.3 | `regen_missing_pngs.py` não foi afetado (não gera nada removido pela Waleska) | grep confirma que só referencia `censo_0_a_4_anos_por_ano.csv`, já restaurado | ✅ passou |

```bash
grep -n "obitos_causas_evitaveis_raca\|mortalidade_causas_evitaveis_raca_municipio_ano\|_SLUG_SUBGRUPO_PDF\|cobertura_vacinal_epi_ano.png\|mapa_censo_0_4_.*_ap.png\|mapa_censo_0_4_.*_rp.png\|mapa_obitos_gravidez_bairro_2025\|mapa_obitos_puerperio_bairro_2025\|mapa_obitos_neonatal_tardia_bairro_2025\|mapa_obitos_pos_neonatal_bairro_2025\|mapa_obitos_evitaveis_gestacao\|mapa_obitos_evitaveis_parto" \
  .claude/skills/export_pdf_report/scripts/build_notebook_report.py   # vazio

grep -n "mortalidade_causas_evitaveis_raca_municipio_ano\|tabela_mapa_obitos_evitaveis_.*_menores_1_ano_cap_2025\|_SUBGRUPOS_COMPONENTE_C\|_entries_mapas_cap_subgrupo" \
  .claude/skills/export_pdf_report/scripts/build_html_report.py       # só o comentário explicativo
```

---

## V4 — Bug de cálculo do Censo, confirmado numericamente

| # | checagem | aceite | resultado |
|---|---|---|---|
| V4.1 | Percentual "antigo" (soma de percentuais por bairro) está fora da faixa 0-100% | > 100% em todos os 3 anos | ✅ passou — 1.091,84% / 837,37% / 751,97% (2000/2010/2022) |
| V4.2 | Percentual "novo" (recalculado dos totais somados) está numa faixa plausível | 0-100%, decrescente ao longo dos censos (consistente com envelhecimento populacional) | ✅ passou — 7,09% / 5,45% / 4,75% |
| V4.3 | A correção não é cosmética | diferença de ordem de grandeza (>100x) entre antigo e novo | ✅ passou |

Comando e código completo em `plan.md` §3. Dados de entrada:
`dados_locais/censo/tabela 2974_{2000,2010,2022}.csv` (não gitignorados, usados como estão).

---

## V5 — CSV do Censo restaurado

| # | checagem | aceite | resultado |
|---|---|---|---|
| V5.1 | Linha `to_csv` presente em `analise.py` | `grep -n "censo_0_a_4_anos_por_ano.csv" analise.py` encontra a chamada | ✅ passou |
| V5.2 | Posição no código | depois do cálculo de `Percentual 0 a 4 anos`, antes da primeira célula de gráfico (`# %%`) | ✅ passou (inspeção manual) |
| V5.3 | Colunas exportadas batem com o que os 3 scripts consumidores esperam (`ano`, `0 a 4 anos`, `Sexo feminino, 0 a 4 anos`, `Sexo masculino, 0 a 4 anos`, `Percentual 0 a 4 anos`) | presentes (mais `Total`, coluna extra inofensiva) | ✅ passou (inspeção manual do código de `regen_missing_pngs.py`) |

---

## V6 — Execução de `analise.py` de ponta a ponta ✅ passou

Ambiente montado: `analise_env/` (venv já existente) com `pip install -r requirements.txt`
(exceto `pywinpty`, dependência Windows-only irrelevante em Linux — não instala, e não é usado
por `analise.py`). `analise.py` convertido para notebook e executado via
`jupyter nbconvert --execute --allow-errors` numa cópia isolada em scratch (inputs de
`dados_locais/` linkados como leitura; saídas em `tabelas_finais/`/`mapas/`/`visualizacoes/`
**locais ao scratch**, para não sobrescrever as saídas reais já commitadas/geradas do projeto).

Dois ajustes só-de-ambiente, sem tocar `analise.py` de verdade — o projeto assume Windows
(paths com `\`, que não funcionam como separador no Linux): substituídos por `/` numa cópia
temporária só para rodar aqui. **Não são bugs do merge da Waleska nem foram commitados.**

| # | checagem | aceite | resultado |
|---|---|---|---|
| V6.1 | Roda sem erro, kernel limpo, do início ao fim | sem exceção | ⚠️ ver V6.2 |
| V6.2 | Seção CadÚnico (não tocada pela Waleska) | requer `.env` + Postgres | **Confirmado que falha só por falta de `.env`/DB** (não existe `.env` no projeto) — `ValueError` na primeira célula que usa `engine`, cascata de `NameError`/`KeyError` nas ~17 células seguintes da seção CadÚnico, todas dependentes da query. Nenhuma delas foi tocada por Waleska. Comportamento idêntico ao documentado em `.claude/skills/export_pdf_report/SKILL.md` ("não roda apenas com os arquivos em `dados_locais/`") |
| V6.3 | Seções de Mortalidade/Censo/SISVAN/Vacinal/SIDRA (tocadas) | tabelas/gráficos esperados, sem os removidos pela curadoria | ✅ **117 de 134 células rodam sem erro** — as 17 que falham são só CadÚnico (V6.2). Confirmado por inspeção de arquivo: as ~10 saídas removidas pela curadoria (tabela `plan.md` §2) **não existem**; as saídas mantidas/restauradas **existem** — ver lista completa abaixo |
| V6.4 | Nenhuma saída fora do escopo muda | mapas/tabelas não tocadas continuam sendo geradas | ✅ `mapa_mortalidade_infantil_bairro_2025.png`, mapas de raça/cor, IBGE SIDRA etc. gerados normalmente |
| V6.5 | **Novo, achado durante a execução**: nenhuma célula ativa referencia uma variável só definida numa célula comentada pela curadoria | 0 `NameError` fora da cascata do CadÚnico | ❌ **falhou na primeira tentativa** — achado real: o commit "Ajusta curadoria da mortalidade evitável" comentou 3 das 4 chamadas `serie_temporal_multipla` de "óbitos evitáveis por raça/cor sem não informada", deixando a 4ª ativa referenciando `df_percentual_evitaveis_municipio`/`rotulos_raca_evitaveis_sem_nao_informado`, ambas só definidas nas linhas comentadas. **Corrigido** (comentada também, commit `bcdfa08`) — reexecutado, ✅ passou |

Confirmação por arquivo (rodado após o fix do V6.5):

```
=== não deveriam existir (removidas pela curadoria) ===
ok, absent: tabelas_finais/mortalidade_causas_evitaveis_raca_municipio_ano.csv
ok, absent: visualizacoes/obitos_causas_evitaveis_raca_ano.png
ok, absent: visualizacoes/cobertura_vacinal_epi_ano.png
ok, absent: mapas/mapa_censo_0_4_absoluto_ap.png
ok, absent: mapas/mapa_censo_0_4_percentual_rp.png
ok, absent: mapas/mapa_obitos_gravidez_bairro_2025.png
ok, absent: mapas/mapa_obitos_puerperio_bairro_2025.png
ok, absent: mapas/mapa_obitos_neonatal_tardia_bairro_2025.png
ok, absent: mapas/mapa_obitos_pos_neonatal_bairro_2025.png
ok, absent: tabelas_finais/tabela_mapa_obitos_evitaveis_gestacao_menores_1_ano_cap_2025.csv

=== deveriam existir (mantidas/restauradas) ===
ok, present: tabelas_finais/censo_0_a_4_anos_por_ano.csv
ok, present: mapas/mapa_censo_0_4_absoluto.png
ok, present: mapas/mapa_censo_0_4_percentual.png
ok, present: visualizacoes/cobertura_vacinal_epi_comparativo_anos.png
ok, present: mapas/mapa_taxa_obitos_tardios_bairro_2025.png
ok, present: mapas/mapa_taxa_mortalidade_pos_neonatal_bairro_2025.png
ok, present: mapas/mapa_mortalidade_infantil_bairro_2025.png
```

---

## V7 — Pipelines de relatório (PDF/HTML) ✅ passou

Rodado com as saídas frescas de V6 (mais os artefatos legados de CadÚnico e um CSV legado
de nascidos vivos, ambos copiados do `tabelas_finais/`/`mapas/`/`visualizacoes/` reais do
projeto, já que a seção CadÚnico não pôde ser regerada nesta sessão — mesmo princípio
documentado no `SKILL.md`, "reflete o último export salvo").

| # | checagem | aceite | resultado |
|---|---|---|---|
| V7.1 | `regen_missing_pngs.py` roda até onde não depende de CadÚnico | `censo_0_a_4_serie_*_ano.png` gerados a partir do CSV restaurado | ✅ passou (falha só ao chegar na parte de CadÚnico, mesma causa de V6.2) |
| V7.2 | `build_notebook_report.py` roda sem `FileNotFoundError`/`SystemExit` | HTML fonte do PDF gerado | ✅ passou — `wrote pdf_source.html 14996765 chars` |
| V7.3 | `build_html_report.py` roda sem `FileNotFoundError` | `index.html` gerado | ✅ passou — `wrote index.html: 15678100 chars, 77 charts, 9 h2 / 12 h3 sections` |
| V7.4 | Conteúdo gerado não tem as seções removidas | grep no HTML final | ✅ passou — `"Óbitos por causas evitáveis por raça/cor"`, `"Por CAP e faixa etária, por subgrupo"`, `"Gestação e parto, menores de 1 ano"` (PDF) e `"Por raça/cor (0-364 dias)"`, `"Por subgrupo (gestação e parto)"` (HTML): **0 ocorrências**, nenhuma |
| V7.5 | Conteúdo gerado ainda tem as seções mantidas | grep no HTML final | ✅ passou — `"Óbitos por causas evitáveis, por grupo de causa (CID-10)"` e `"Grupo evitável, por CAP"` presentes |

Não testado: renderização para PDF de fato via Chrome headless (passo separado do
`SKILL.md`, precisa do Chrome/Windows descrito lá — fora do escopo desta validação, que é
sobre o **conteúdo** gerado pelos scripts Python, não sobre o passo de impressão).

---

## V8 — Regressão fora do escopo

| # | checagem | aceite | resultado |
|---|---|---|---|
| V8.1 | `requirements.txt` inalterado | `git diff` vazio | ✅ passou |
| V8.2 | Nenhuma função de `📦 Pacotes e Funções Auxiliares` mudou de assinatura | `git diff` do merge só toca células de análise | ✅ passou |
| V8.3 | `mapa_coropletico_bairros`, `agrega_bairros_por_nivel` e as 4 funções de gráfico idênticas | mesmo motivo acima | ✅ passou |
| V8.4 | Saídas de `tabelas_finais/`/`visualizacoes/`/`mapas/` já commitadas não mudam sozinhas | pastas gitignoradas — a execução desta sessão rodou isolada em scratch, sem tocar as saídas reais do projeto | ✅ passou por construção (V6 rodou num diretório separado, não sobrescreveu nada real) |
| V8.5 | Ambiente Linux consegue rodar o projeto (achado incidental, não pedido, registrado por transparência) | `pip install -r requirements.txt` falha (`pywinpty`, Windows-only) | ⚠️ **não corrigido** — instalado sem esse pacote para esta validação; se o time quiser rodar em Linux/CI no futuro, vale marcar `pywinpty` com `sys_platform == 'win32'` em `requirements.txt` (não feito aqui — fora do pedido original, só observado) |

---

## Resumo

| Bloco | Status |
|---|---|
| Merge e integridade estática (V1-V5) | ✅ 100% passou |
| Execução em runtime (V6-V7) | ✅ 100% passou (CadÚnico à parte — sem DB nesta sessão, esperado e documentado, fora do escopo da Waleska) |
| Regressão fora do escopo (V8) | ✅ passou (V8.5 é um achado incidental sobre portabilidade Linux, não uma regressão do merge) |

**Um bug real foi encontrado e corrigido durante a execução (V6.5)**: uma célula ativa
sobrevivente referenciava variáveis só definidas em código que a própria curadoria da Waleska
tinha comentado — só aparece rodando o notebook de verdade, não em grep estático. Corrigido
(commit `bcdfa08`) e revalidado. Fora esse achado (já corrigido), nada mais contradiz a
curadoria da Waleska ou indica que o merge introduziu um problema novo — **merge validado de
ponta a ponta**, pronto para o Bloco 5 (`tasks.md`).
