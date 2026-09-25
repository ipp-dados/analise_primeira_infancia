# Tarefas — `specs/relatorio_latex`

## Bloco 0 — Aprovação
- [x] T0.1 Decisões D1-D4 (`specification.md` §8) registradas neste spec (2026-09-25)
- [x] T0.3 Nomes da equipe para a folha de rosto (2026-09-25; funções não informadas)
- [x] T0.2 Branch `spec/relatorio-latex` a partir de `planning`

## Bloco 1 — Inventário de fontes
- [x] T1.1 `inventario_fontes.py`: AST de `analise.py` (chamadas de gráfico/mapa/`to_csv`, `fonte_*` resolvidos)
- [x] T1.2 Cruzar com `estrutura_eixos.md` (`fonte:`, arquivos por subseção) e com o disco
- [x] T1.3 `relatorio/inventario_fontes.md` + `.csv`: por fonte, por arquivo, alertas
- [x] T1.4 `fontes.bib` (NBR 6023) com campo `variaveis`; alerta de fonte sem entrada
- [ ] T1.5 Revisar alertas com o usuário (não corrigir `fonte:` sem aprovação). Achados de 2026-09-25:
  10 arquivos do relatório vêm de chamadas **comentadas** em `analise.py` (arquivos antigos no disco);
  13 gráficos são regravados por `regen_missing_pngs.py` sem `fonte_dados`; 2 (`censo_0_a_4_serie_*`) só
  existem via esse script; 10 campos `conferir` em `fontes.bib`

## Bloco 2 — Esqueleto e páginas-amostra
- [ ] T2.1 `relatorio.tex` (abntex2, relatório técnico, A4, oneside, 12 pt, 1,5) + `estilo.sty`
- [ ] T2.2 Floats `grafico` e `mapa` (newfloat) com listas próprias; legenda acima, Fonte abaixo
- [ ] T2.3 Fraunces + IBM Plex Sans; cores `--ipp-navy` e `--c1…--c11`
- [ ] T2.4 Ícones Lucide → PDF (svglib ou tradução para TikZ; fallback `fontawesome5`)
- [ ] T2.5 Capa, folha de rosto, resumo, listas, siglas, sumário, Fontes
- [ ] T2.6 Capítulo-amostra (Alimentação) + apêndice-amostra, montados à mão
- [ ] T2.7 Páginas-amostra rasterizadas → revisão do usuário

## Bloco 3 — Gerador
- [ ] T3.1 `gera_latex.py`: `parse_estrutura_eixos()` + `valida_estrutura()` → capítulos em `gerado/`
- [ ] T3.2 Escape LaTeX + aspas tipográficas do texto curado (testar as 58 entradas)
- [ ] T3.3 Legendas a partir do inventário/manifesto; remissões "ver Tabela X.n"
- [ ] T3.4 Caixas: achados, pendente, síntese; texto ausente = lorem determinístico (`_lorem(seed)`) + lista de chaves em lorem no log
- [ ] T3.5 Cache de imagens reduzidas em `_build/` (300 dpi na largura final)
- [ ] T3.6 `latexmk -xelatex` + cópia para `relatorio/analise_primeira_infancia.pdf`

## Bloco 4 — Apêndice de tabelas
- [ ] T4.1 `tabelas.py`: portar seleção/formatação de `build_notebook_report.py`
- [ ] T4.2 `longtable` + `booktabs`, pt-BR, `ano` sem separador, Fonte abaixo
- [ ] T4.3 Chave opcional `tabela_no_texto:` em `estrutura_eixos.md` (+ parser)

## Bloco 5 — Figuras A4 (D1 = B)
- [ ] T5.1 Parâmetro nos helpers de `analise.py`: variante sem título/fonte, tamanho A4, em `visualizacoes/a4/`, `mapas/a4/`
- [ ] T5.2 Manifesto (arquivo, título, fonte, função) gravado pelos helpers
- [ ] T5.3 `regen_missing_pngs.py` acompanha
- [ ] T5.4 Execução completa do notebook pelo usuário (`analises_env` + `.env`)

## Bloco 6 — Curadoria e integração
- [ ] T6.1 Chaves novas no DOCX (`gera_docx_curadoria.py`, preservando o texto já curado)
- [ ] T6.2 `sincroniza_docx.py` regera o LaTeX
- [ ] T6.3 Reescrever `.claude/skills/export_pdf_report/SKILL.md`; aposentar `build_notebook_report.py` após V1-V20
- [ ] T6.4 `.gitignore`, `CLAUDE.md`, `README.md`, `specs/roadmap.md`, `specs/tech-stack.md`

## Bloco 7 — Validação
- [ ] T7.1 Rodar `validation.md` inteiro; PDF final
