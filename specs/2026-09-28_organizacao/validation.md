# Validação — `specs/2026-09-28_organizacao`

Escrita antes da implementação; resultados preenchidos no fechamento (2026-09-28). Execuções completas de
`analise.py` no conda env `analises_env` (`MPLBACKEND=Agg`), com o `.env` do CTPE (CadÚnico lido do banco).

| # | Verificação | Como | Resultado |
|---|---|---|---|
| V1 | Todas as saídas de `analise.py` iguais antes e depois | hash de `tabelas_finais/`, `visualizacoes/`, `mapas/`, `dados_locais/` (PDF sem datas/ID, XLSX por conteúdo) | **OK** — 431 de 431 arquivos idênticos, nenhum a mais ou a menos |
| V2 | Execução depois sem erro nem `[variante A4] … falhou` | log | **OK** — exit 0, sem traceback nem falha de variante; log igual ao de antes (fora os números de linha dos avisos) |
| V3 | Pacote sem import circular; `analise.py` com os mesmos nomes disponíveis para as seções | script de extração + comparação do espaço de nomes | **OK** — grafo acíclico (`estilo` na base); 161 nomes, nenhum a mais ou a menos; bytecode, constantes e defaults de toda função iguais (comparação recursiva, sem números de linha) |
| V4 | Site igual (md5 de `index.html`, `data/*`) | `build_site.py` | **OK** — md5 idênticos (os arquivos aparecem modificados só por fim de linha CRLF/LF) |
| V5 | LaTeX igual (`gerado/*.tex`) e PDF compilando | `gera_latex.py` | **OK** — `gerado/` idêntico; PDF compila (0 referências indefinidas) |
| V6 | DOCX de curadoria com os mesmos textos/bookmarks; sincronização sem mudança | `gera_docx_curadoria.py` + `coleta_edicoes` | **OK** — 134 bookmarks com os mesmos textos; sincronização não mudaria nenhuma chave; `valida_textos_publicados.py`: 0 ausentes; `confere_textos.py` roda do novo caminho |
| V7 | Inventário de fontes igual | `inventario_fontes.py` + diff | **OK, depois de um ajuste** — a leitura estática procurava as funções que gravam figuras e as constantes no próprio `analise.py`; passou a ler o pacote antes do notebook (`fonte_notebook()`). Resultado igual ao de antes, fora a coluna/menção de número de linha |
| V8 | `requirements.txt` cobre todo import do código | varredura AST × lista | **OK** — nenhum import externo sem requisito |
| V9 | `jupytext --to notebook analise.py` funciona | conversão | **OK** — 348 células |

Achados durante a implementação:
- O extrator perdia os decoradores `@_a4_seguro` (o AST dá a linha do `def`, não a do decorador): as 6 funções de
  variante A4 sairiam sem a proteção que transforma uma falha da impressão em aviso. Pego pela comparação de V3
  antes da execução completa; corrigido no extrator (`decorator_list`).
- Arquivos soltos removidos (T1.3), todos ignorados pelo git e restos de uma compilação manual com pdfTeX em
  2026-09-25 (o pipeline usa xelatex em `_build/`): `relatorio/latex/relatorio.aux` (32 B),
  `relatorio.fdb_latexmk` (9,8 KB), `relatorio.fls` (12,7 KB), `relatorio.log` (25,6 KB). A pasta
  `.claude/skills/export_pdf_report/scripts/` ficou vazia (só `__pycache__`) e saiu.
- A execução do notebook regrava 3 `.xlsx` versionados em `mapas/tabelas_bairros/` com o mesmo conteúdo (só os
  metadados do zip mudam); foram restaurados, sem commit.
