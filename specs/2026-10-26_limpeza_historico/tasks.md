# Limpeza do repositório e do histórico — tarefas

## Parte A (2026-10-26)
- [x] A1 Tags `rodada/*` (16) e branches mescladas apagadas, local e `origin`
- [x] A2 `waleska-analise-primeira-infancia`: avaliada (não mesclável), tag e apagada
- [x] A3 `spec/deck_familia_moradia`: merge de teste (4 conflitos), tag e apagada
- [x] A4 131 saídas fora do rastreio; Excel de `mapas/tabelas_bairros/` → `tabelas_finais/`
- [x] A5 `revisao_casa_civil/` fora do rastreio e no `.gitignore`
- [x] A6 `git gc`; builds e caches locais apagados
- [x] A7 Documentação atualizada
- [x] A8 Push de `staging_main` (`a90a9a8` na história nova)

## Parte B (2026-10-26)
- [x] B1 Decisões (especificação §3)
- [x] B2 Backup: `git bundle --all` em `../backup_analise_primeira_infancia_2026-10-26/` (fora do repositório)
- [x] B3 `git filter-repo` 2.47.0 em clone espelho novo do GitHub (0 forks, 0 PRs, sem proteção de branch)
- [x] B4 Hashes citados trocados nos arquivos atuais a partir de `filter-repo/commit-map` (82 em 37 arquivos; 3 citam
      commits que sumiram e ficaram como estavam) — num commit novo, não no próprio filter-repo (mudaria os hashes de novo)
- [x] B5 Validação (`validation.md`)
- [x] B5b `.gitignore`, link do PDF do site, docs (README, CLAUDE.md, constituição, skill do PDF, especificação do projeto)
- [x] B6 Force-push de todas as branches e tags (pelo usuário, `finalizar_reescrita.sh` no backup); cópia local ressincronizada
- [ ] B6b Pedido ao GitHub Support (cache dos commits antigos `cdfacd2`, `101e6bf`)
- [ ] B7 Release `v0.34.0` com os anexos; avisar a equipe para reclonar; deploy do
      Pages a partir da `demo` (o link do PDF mudou)
- [ ] B8 Apagar o backup depois de validado
