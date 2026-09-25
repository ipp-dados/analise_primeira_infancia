# Plano — `specs/2026-09-25_website_graficos`

Proposta para a sessão de planejamento com o usuário (decisões P1-P5 em `specification.md` §3). Cada bloco fecha
com os itens correspondentes de `validation.md` e um commit `SPEC-WebsiteGraficos: Bloco N -- ...`.

- **Bloco 0 — Planejamento.** Decidir P1-P5; ajustar esta ordem.
- **Bloco 1 — Exclusões (A).** E2-E8 em `build_site.py`, com um helper `_subgrupo_excluido()` igual ao
  `subgrupo_excluido()` de `analise.py` (mesma regra, citando `specs/exclusoes.md`) e o agrupamento E5 a partir
  dos absolutos. Validação VA.*, V0.*.
- **Bloco 2 — Alternância Taxa ↔ Óbitos (E9).** `option_card_alternancia` no gerador, JS e CSS à mão.
  Validação V9.*.
- **Bloco 3 — Paleta e teto (B5, B2).** Rodar o validador; trocar só o que reprovar (P3). Teto P95 nos mapas
  contínuos por bairro. VB.2, VB.5.
- **Bloco 4 — Rótulos e totais (B1, B3, B7, B8).** Depende de P1 e P5. VB.1, VB.3, VB.7, VB.8.
- **Bloco 5 — Pequenos múltiplos (B4).** Novo tipo de gráfico no motor (`js/charts.js`); P2. VB.4.
- **Bloco 6 — Fontes ABNT (B6).** Do `fontes.bib` para as caixas do site. VB.6.
- **Bloco 7 — Navegador e publicação.** VN.*; deploy só com OK explícito.

Atualizar ao fechar: `specs/exclusoes.md` (coluna Site: "planejado" → "aplicado"), `specs/roadmap.md`
(`improve charts`), `website/README.md`/`website/ROADMAP.md` se algo de uso mudar, `relatorio/specs.md` (histórico
do site).
