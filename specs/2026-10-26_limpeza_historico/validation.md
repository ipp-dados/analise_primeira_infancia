# Limpeza do repositório e do histórico — validação

## Parte A (2026-10-26)
- [x] `git ls-remote --tags origin 'rodada/*'`: 33 tags, inclusive as 17 novas (16 + `rodada/planning`)
- [x] `git branch -a`: só `staging_main`, `demo`, `main` (local e `origin`)
- [x] `git ls-files mapas tabelas_finais visualizacoes`: só os 3 `.gitkeep`; `git ls-files -ci --exclude-standard` vazio
- [x] Saídas e `revisao_casa_civil/` continuam no disco
- [x] `grep tabelas_bairros analise.py` vazio; as 3 tabelas Excel copiadas para `tabelas_finais/`

## Parte B (a fazer)
- [x] `git log --all -- tabelas_finais revisao_casa_civil mapas visualizacoes`: só os `.gitkeep`
- [x] `git rev-list --objects --all | grep cadunico_por_bairro` vazio; nenhum PPTX nem PDF/DOCX de `relatorio/`
- [x] 33 tags; 357 → 346 commits; diferença antiga × nova: `staging_main` só em `apresentacao/` (10 PDF/PPTX) e
      `relatorio/` (7 PDF/DOCX); `demo` também nas saídas ainda rastreadas lá; `main` em 2 PNG
- [ ] Hashes citados em `CHANGELOG.md`/`specs/` resolvem com `git cat-file -e` (amostra de 10)
- [ ] Clone novo do GitHub: tamanho ~12-20 MB; site da `demo` publicado; `build_site.py` e `gera_latex.py` rodam
