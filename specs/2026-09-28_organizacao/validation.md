# Validação — `specs/2026-09-28_organizacao`

Escrita antes da implementação; resultados preenchidos no fechamento.

| # | Verificação | Como | Resultado |
|---|---|---|---|
| V1 | Todas as saídas de `analise.py` iguais antes e depois | hash de `tabelas_finais/`, `visualizacoes/`, `mapas/`, `dados_locais/` (PDF sem datas/ID, XLSX por conteúdo) | |
| V2 | Execução depois sem erro nem `[variante A4] … falhou` | log | |
| V3 | Pacote sem import circular; `analise.py` com os mesmos nomes disponíveis para as seções | script de extração + execução | |
| V4 | Site igual (md5 de `index.html`, `data/*`) | `build_site.py` | |
| V5 | LaTeX igual (`gerado/*.tex`) e PDF compilando | `gera_latex.py` | |
| V6 | DOCX de curadoria com os mesmos textos/bookmarks; sincronização sem mudança | `gera_docx_curadoria.py` + `coleta_edicoes` | |
| V7 | Inventário de fontes igual | `inventario_fontes.py` + diff | |
| V8 | `requirements.txt` cobre todo import do código | varredura AST × lista | |
| V9 | `jupytext --to notebook analise.py` funciona | conversão | |
