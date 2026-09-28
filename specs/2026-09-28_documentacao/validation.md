# Validação — `specs/2026-09-28_documentacao`

| # | Verificação | Como | Resultado |
|---|---|---|---|
| V1 | Todo caminho citado nos documentos existe | varredura dos trechos entre crases de `docs/especificacao_projeto.md`, README, CLAUDE.md, tech-stack, constituição, `website/README.md` e skills, resolvendo caminhos relativos pela pasta do contexto | **OK** — um erro real corrigido (`dados_locais/cadunico/` e `IBGE SIDRA/` no CLAUDE.md, pastas que não existem); o que sobra são menções históricas explícitas (`relatorio/index.html`, "não existe mais"), o arquivo transitório `relatorio/curadoria_textos_update.docx`, `_site/` do CI e o ambiente local `analise_env/` |
| V2 | Números do documento conferem com a fonte | script sobre `specs/estrutura_eixos.md` (51 indicadores, 9 pendentes, 63 gráficos, 31 mapas, 85 tabelas), geojson (166 bairros, 5 AP, 16 RP, 33 RA, 10 CAP), `fontes.bib` (13), PDF (157 páginas), `tabelas_finais/` (87 CSV) | **OK** |
| V3 | Pontos do item 6 do ROADMAP cobertos | nível `ra`, `dados_locais/protecao/`, `carrega_sinan_*`, eixo Proteção, relatório LaTeX | **OK** — README, CLAUDE.md e especificação |
| V4 | Nenhuma mudança de código nem de saída | `git diff --stat` | **OK** — só documentação e `.env.example` |
