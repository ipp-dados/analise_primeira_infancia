# PLAN — Apresentação breve do eixo Inclusão

- **B1** — `apresentacao/build/numeros.py`: funções `@numero` `incl_*` a partir de `cadunico_deficiencia_criancas_0_a_5_2026.csv`,
  `cadunico_deficiencia_familias_0_a_5_2026.csv`, `cadunico_tipos_deficiencia_0_a_5_2026.csv` e
  `tabela_mapa_cadunico_deficiencia_bairro_2026.csv` (mediana e extremos só dos bairros publicados sozinhos).
- **B2** — `apresentacao/build/mapas_apresentacao.py`: `apres_cadunico_deficiencia_bairro` (tema cadunico, escala contínua,
  Tukey; `prepara` tira as linhas de conjunto "Demais bairros…", que não têm `codbairro`).
- **B3** — `apresentacao/variantes/inclusao.md`: cabeçalho do deck principal com título do eixo; slides de D4; figuras
  `fig:cadunico_criancas_por_tipo_deficiencia` (versão A4) e `fig:apres_cadunico_deficiencia_bairro`.
- **B4** — gerar PNG para conferir, PPTX/PDF, `--publicar`; conferir que `apresentacao.md` gera igual (sem chave quebrada).
- **B5** — fechar D11 da rodada anterior (adensamento "mais de 2": ROADMAP, `docs/criterios_fjp_cadunico.*`, crosswalk);
  README do deck (variante nova); ROADMAP; merge `staging_main` → `demo`, regerar site da demo; push.

Riscos: marp/Chromium no build (já usado no deck principal); mapa com muitos bairros em conjunto (58% sozinhos) — a nota
do slide diz que bairros pequenos estão somados por RA.
