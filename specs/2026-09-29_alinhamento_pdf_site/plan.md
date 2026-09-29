# Rodada `alinhamento_pdf_site` — plano

Branch `spec/alinhamento-pdf-site` a partir de `planning`; merge em `planning` e `staging_main` ao fim, com push.
Decisões D1-D5 em `specification.md`.

## Levantamento

- **Comparação** (script em scratchpad, 2026-09-29): 9 capítulos do PDF (Introdução, 7 eixos, Considerações finais)
  × 9 `h2` do site (Introdução, Panorama, 7 eixos) — mesma ordem. Seções do PDF sem figura e sem `status: pendente`:
  CadÚnico ÷ população, cobertura vacinal, violência familiar por CAP, SISVAN desnutrição (número), SISVAN sobrepeso
  (número).
- **Pendentes:** PDF — `gera_latex.py` l. 218-223 (ignora a `nota:`, imprime `TEXTO_PENDENTE`); site —
  `emite_bloco_pendente(titulo, nota)` com a nota escrita à mão em 8 chamadas (`build_site.py` l. 1624, 1732-1734,
  1964-1965, 2029-2031). Os títulos do site são os mesmos do crosswalk nesses 8 itens.
- **Vacinação:** chamada comentada em `analise.py` (~l. 2282-2292); site já lê `cobertura_vacinal_epi_por_ano.csv`.
- **Tabelas:** `tabelas.tabela_latex(caminho, titulo_secao, fonte_tex, rotulo)` já monta uma tabela isolada; o
  apêndice é montado em `gera_latex.py` (~l. 231-332).

## Blocos

**B1 — Crosswalk (D1, D4, D5).** Mover o item de taxa de mortalidade; tirar o item de causas evitáveis por raça/cor
(E16); `motivo:` nos pendentes; `tabela_no_texto:` nos dois itens de D3; `visualização:` da vacinação.

**B2 — `analise.py` (D2).** Descomentar a chamada da vacinação; rodar só a seção (DataSUS/EPI locais) com a variante
A4 — sem rodar o notebook inteiro (o resto não muda).

**B3 — Gerador do PDF (D3, D5).** `gera_latex.py`: `motivo:` depois de `TEXTO_PENDENTE`; `tabela_no_texto:` na seção
via `tabelas.tabela_latex`, fora do apêndice. Parser (`gera_estrutura_eixos.py`) aceita as chaves novas.

**B4 — Site (D5).** `emite_bloco_pendente(titulo)` lê o `motivo:` do crosswalk pelo título; falha no build se o item
não existir ou não tiver motivo (nunca volta a anotação interna).

**B5 — Regerar e validar.** Site, PDF (sem `--publicar`), DOCX; comparação de estrutura de novo; `validation.md`.

**B6 — Fechamento.** `specs/exclusoes.md` (E1, E16), `relatorio/controle_revisao.json`, CHANGELOG, README, ROADMAP
(T4.3 sai do backlog do PDF), `docs/especificacao_projeto.md`, `relatorio/specs.md`; merge e push.

## Riscos

- Tabela no corpo muito larga ou longa: as duas têm 1 e 10 linhas; conferir no PDF.
- Série de vacinação com muitos imunobiológicos: `serie_temporal_multipla` já destaca 4 e apaga o resto (≥ 7 séries).
