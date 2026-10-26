# Limpeza do repositório e do histórico — validação

## Parte A (2026-10-26)
- [x] `git ls-remote --tags origin 'rodada/*'`: 33 tags, inclusive as 17 novas (16 + `rodada/planning`)
- [x] `git branch -a`: só `staging_main`, `demo`, `main` (local e `origin`)
- [x] `git ls-files mapas tabelas_finais visualizacoes`: só os 3 `.gitkeep`; `git ls-files -ci --exclude-standard` vazio
- [x] Saídas e `revisao_casa_civil/` continuam no disco
- [x] `grep tabelas_bairros analise.py` vazio; as 3 tabelas Excel copiadas para `tabelas_finais/`

## Parte B (2026-10-26)
- [x] `git log --all -- tabelas_finais revisao_casa_civil mapas visualizacoes`: só os `.gitkeep`
- [x] `git rev-list --objects --all | grep cadunico_por_bairro` vazio; nenhum PPTX nem PDF/DOCX de `relatorio/`
- [x] 33 tags; 357 → 346 commits; diferença antiga × nova: `staging_main` só em `apresentacao/` (10 PDF/PPTX) e
      `relatorio/` (7 PDF/DOCX); `demo` também nas saídas ainda rastreadas lá; `main` em 2 PNG
- [x] Hashes citados em `CHANGELOG.md`/`ROADMAP.md`/`specs/`: 32 de 35 resolvem; os 3 restantes são o código IBGE
      `3304557` (não é hash) e `3a258e8`/`101e6bf`, commits que só mexiam em caminhos removidos e sumiram
- [x] Force-push: 3 branches e 33 tags no GitHub; cópia local na história nova, `.git` com 12 MB, PDF/DOCX/decks e
      saídas continuam no disco
- [x] Release `v0.34.0` publicada (20 anexos, tamanhos iguais aos originais); `releases/latest/download/` responde 200
      para o PDF, o PDF da demo e o deck principal; o site publicado linka o PDF da demo na Release
