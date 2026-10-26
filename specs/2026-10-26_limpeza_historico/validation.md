# Limpeza do repositório e do histórico — validação

## Parte A (2026-10-26)
- [x] `git ls-remote --tags origin 'rodada/*'`: 33 tags, inclusive as 17 novas (16 + `rodada/planning`)
- [x] `git branch -a`: só `staging_main`, `demo`, `main` (local e `origin`)
- [x] `git ls-files mapas tabelas_finais visualizacoes`: só os 3 `.gitkeep`; `git ls-files -ci --exclude-standard` vazio
- [x] Saídas e `revisao_casa_civil/` continuam no disco
- [x] `grep tabelas_bairros analise.py` vazio; as 3 tabelas Excel copiadas para `tabelas_finais/`

## Parte B (a fazer)
- [ ] `git log --all -- tabelas_finais revisao_casa_civil` vazio no repositório reescrito
- [ ] Nenhum blob com contagem do CadÚnico de `cdfacd2`: `git rev-list --objects --all | grep cadunico_por_bairro` vazio
- [ ] Mesmo número de tags; `staging_main` reescrita com árvore igual à antiga fora dos caminhos removidos
      (`git diff --stat <antiga> <nova>` só lista caminhos removidos)
- [ ] Hashes citados em `CHANGELOG.md`/`specs/` resolvem com `git cat-file -e` (amostra de 10)
- [ ] Clone novo do GitHub: tamanho ~12-20 MB; site da `demo` publicado; `build_site.py` e `gera_latex.py` rodam
