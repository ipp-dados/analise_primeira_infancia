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

## V6 — Execução de `analise.py` de ponta a ponta ⏳ pendente

| # | checagem | aceite |
|---|---|---|
| V6.1 | Roda sem erro, kernel limpo, do início ao fim | sem exceção |
| V6.2 | Seção CadÚnico (não tocada pela Waleska) continua funcionando | requer `.env` + Postgres — não disponível nesta sessão |
| V6.3 | Seções de Mortalidade/Censo/SISVAN/Vacinal (tocadas) produzem as tabelas/gráficos esperados, sem os removidos pela curadoria | inspeção de `tabelas_finais/` e `visualizacoes/` após a execução |
| V6.4 | Nenhuma saída **fora** do escopo da Waleska muda (ex.: mapas de raça/cor por bairro, IBGE SIDRA) | `git diff`/comparação de tabelas antes/depois vazio fora do esperado |

Bloqueado por: sem acesso ao Postgres do CadÚnico nem à rede de tiles do `contextily` nesta
sessão (`plan.md` §4). Responsável: rodar numa máquina com `.env` configurado.

---

## V7 — Pipelines de relatório (PDF/HTML) ⏳ pendente

| # | checagem | aceite |
|---|---|---|
| V7.1 | `regen_missing_pngs.py` roda sem erro | sem exceção; `censo_0_a_4_serie_*_ano.png` gerados a partir do CSV restaurado |
| V7.2 | `build_notebook_report.py` roda sem `FileNotFoundError`/`SystemExit` | PDF gerado |
| V7.3 | `build_html_report.py` roda sem `FileNotFoundError` | `relatorio/index.html` gerado |
| V7.4 | Inspeção visual do HTML/PDF gerados | seção "Óbitos por causas evitáveis" sem buraco onde a subseção de raça/cor foi removida; grupo "Mapas" sem título órfão onde grupos inteiros (Gravidez e puerpério, AP/RP do Censo) foram removidos |

Bloqueado por: depende de V6 rodar primeiro (as saídas de `tabelas_finais/`/`visualizacoes/`
precisam existir antes destes scripts rodarem) e, no caso do PDF, do Chrome headless descrito
em `.claude/skills/export_pdf_report/SKILL.md`.

---

## V8 — Regressão fora do escopo

| # | checagem | aceite |
|---|---|---|
| V8.1 | `requirements.txt` inalterado | `git diff` vazio — ✅ passou (não tocado neste branch) |
| V8.2 | Nenhuma função de `📦 Pacotes e Funções Auxiliares` mudou de assinatura | `git diff` do merge só toca células de análise (Censo, Mortalidade, SISVAN, Vacinal), nunca a seção de funções | ✅ passou (inspeção do diff, `plan.md` §2) |
| V8.3 | `mapa_coropletico_bairros`, `agrega_bairros_por_nivel` e as 4 funções de gráfico idênticas | mesmo motivo acima | ✅ passou |
| V8.4 | Saídas de `tabelas_finais/`/`visualizacoes/`/`mapas/` já commitadas não mudam sozinhas | essas pastas são gitignoradas (exceto `.gitkeep`) — nada foi gerado nesta sessão, então não há o que comparar ainda | ⏳ só verificável depois de V6 |

---

## Resumo

| Bloco | Status |
|---|---|
| Merge e integridade estática (V1-V5) | ✅ 100% passou, nesta sessão |
| Execução em runtime (V6-V7) | ⏳ pendente — precisa de ambiente com DB/rede completos |
| Regressão fora do escopo (V8) | ✅ estático passou; dinâmico (V8.4) depende de V6 |

**Nada encontrado até agora contradiz a curadoria da Waleska ou indica que o merge introduziu
um problema novo.** O que falta é confirmação em tempo de execução, não uma dúvida sobre o
conteúdo do merge em si.
