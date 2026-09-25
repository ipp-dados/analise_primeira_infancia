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
- [x] T1.5 (= D6, 2026-09-25: arquivos antigos tirados do relatório) Revisar alertas com o usuário (não corrigir `fonte:` sem aprovação). Achados de 2026-09-25:
  10 arquivos do relatório vêm de chamadas **comentadas** em `analise.py` (arquivos antigos no disco);
  13 gráficos são regravados por `regen_missing_pngs.py` sem `fonte_dados`; 2 (`censo_0_a_4_serie_*`) só
  existem via esse script; 10 campos `conferir` em `fontes.bib`

## Bloco 2 — Esqueleto e páginas-amostra
- [x] T2.1 `relatorio.tex` (abntex2, relatório técnico, A4, oneside, 12 pt, 1,5) + `estilo.sty`
- [x] T2.2 Floats `grafico` e `mapa` (newfloat) com listas próprias; legenda acima, Fonte abaixo
- [x] T2.3 Fraunces + IBM Plex Sans; cores `--ipp-navy` e `--c1…--c11`
- [x] T2.4 Ícones Lucide → PDF (svglib ou tradução para TikZ; fallback `fontawesome5`)
- [x] T2.5 Capa, folha de rosto, resumo, listas, siglas, sumário, Fontes
- [x] T2.6 Capítulo-amostra: em vez de montar à mão, o gerador já saiu (Bloco 3 adiantado); `--eixo N` compila só um eixo
- [ ] T2.7 Páginas-amostra rasterizadas → revisão do usuário. Primeiro build completo (2026-09-25): 1.156 páginas, das
  quais ~1.040 são 9 tabelas bairro×ano em formato longo (2.400-4.800 linhas) → ver T4.4

## Bloco 3 — Gerador
- [x] T3.1 `gera_latex.py`: `parse_estrutura_eixos()` + `valida_estrutura()` → capítulos em `gerado/`
- [x] T3.2 Escape LaTeX + aspas tipográficas do texto curado (testar as 58 entradas)
- [ ] T3.3 Legendas a partir do inventário/manifesto; remissões "ver Tabela X.n"
- [x] T3.4 Caixas: achados, pendente, síntese; texto ausente = lorem determinístico (`_lorem(seed)`) + lista de chaves em lorem no log
- [x] T3.5 Cache de imagens reduzidas em `_build/` (300 dpi na largura final)
- [ ] T3.6 `latexmk -xelatex` + cópia para `relatorio/analise_primeira_infancia.pdf`

## Bloco 4 — Apêndice de tabelas
- [ ] T4.1 `tabelas.py`: portar seleção/formatação de `build_notebook_report.py`
- [ ] T4.2 `longtable` + `booktabs`, pt-BR, `ano` sem separador, Fonte abaixo
- [x] T4.4 Regras de tamanho das tabelas (decididas pelo usuário em 2026-09-25), em `tabelas.py`:
  (1) tabela por bairro com `ano` e mais de 100 linhas -> só o ano mais recente completo (respeita `ano_parcial`);
  (2) mais de 200 linhas -> só formato digital, listada no fim do apêndice; (3) tabela por bairro em duas colunas
  (retrato até 5 colunas, paisagem até 8), sem colunas de código, em ordem alfabética, **nome oficial do bairro
  pelo código** (geojson IPP; 998/999 = "bairro ignorado", no fim); tabela repetida (série filtrada = tabela do
  mapa) impressa uma vez só. Resultado: **245 páginas** (corpo até a p. 114; 74 tabelas em 130 páginas de
  apêndice; 2 tabelas de CAP só digitais). Maiores restantes, para o T4.1: raça/cor por bairro (14 colunas, 7 p.),
  violência familiar por CAP e óbitos evitáveis por subgrupo (formato longo, pedem pivô), CadÚnico arranjo × renda.
- [x] T4.1 Ajustes por tabela (`AJUSTES` em `tabelas.py`): títulos ABNT com período automático, acentos
  (`ACENTOS`), pivôs (subgrupo × ano, arranjo × renda, vacina × ano), colunas selecionadas; quase-duplicatas por
  bairro (mesmas colunas e ano). 209 páginas
- [x] T4.5 Tabelas repetidas fundidas/omitidas no PDF (pedido do usuário, 2026-09-25; `SUBSTITUI_NO_PDF`):
  **168 páginas, 43 tabelas**. Auditoria de omissões para relatório E site em `sugestoes_omissao.md` (A-D),
  aguardando decisão
- [x] T4.6 Exclusões decididas pelo usuário (2026-09-25), registradas em `specs/exclusoes.md` (E1-E11): PDF/DOCX via
  `estrutura_eixos.md` (E6-E9), tabelas (E3, E5, E6), `analise.py` (`subgrupo_excluido`, `agrupa_racas_raras`,
  E2/E3/E5 -- PNGs mudam na próxima execução completa). **159 páginas.** Parte do site foi para
  `specs/website_graficos` (branch `spec/website-graficos`), a pedido do usuário
- [ ] T4.3 Chave opcional `tabela_no_texto:` em `estrutura_eixos.md` (+ parser)

## Bloco 5 — Figuras A4 (D1 = B)
- [x] T5.0 Protótipo e regras de desenho para impressão (`specification.md` §5.1; `prototipo/`) — 2026-09-25
- [ ] T5.1 Parâmetro nos helpers de `analise.py`: variante sem título/fonte, tamanho A4, em `visualizacoes/a4/`, `mapas/a4/` (PDF)
- [ ] T5.1a `_TEMA_IMPRESSAO` (Plex Sans, paleta de impressão validada, grade/eixos) + formatação pt-BR
- [ ] T5.1b `ROTULOS_EIXO` (coluna → rótulo com unidade) e rótulos diretos seletivos por tipo de helper
- [ ] T5.1c Barras: uma cor por série, horizontais com rótulo longo, remoção de linhas de total
- [ ] T5.1d Helper `pequenos_multiplos` para os casos de espaguete (CAP × ano, imunobiológicos, subgrupos CID)
- [ ] T5.1e Mapas: tamanho final, legenda 7-7,5 pt, véu no fundo, teto P95 se D5 aprovar
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
