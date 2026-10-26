# Limpeza do repositório e do histórico — plano

Especificação e decisões: `specification.md`.

1. **Parte A (feita em 2026-10-26):** tags `rodada/*` + branches apagadas; saídas e `revisao_casa_civil/` fora do
   rastreio; `mapas/tabelas_bairros/` → `tabelas_finais/` em `analise.py`; `git gc` e limpeza de builds locais;
   documentação (CLAUDE.md, README, constituição §3, tech-stack, ROADMAP, CHANGELOG).
2. **Parte B (aguarda equipe):** decidir B-D1..B-D4 → anunciar a data → backup espelho → `git filter-repo` num clone
   espelho novo → `--replace-text` dos hashes → validar → force-push de branches e tags → GitHub Support (dados
   sensíveis) → todos reclonam → recolocar/publicar PDF, decks e DOCX conforme B-D1/B-D2 → deploy do Pages.
