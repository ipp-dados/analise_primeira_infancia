# PLAN — Apresentações de Família e Cuidados e de Moradia

- **B1** — `build/numeros.py`: chaves `fam_*` (arranjo, arranjo × pobreza, bairros e APs, matrículas 2019/2021/2022/2025,
  vacinas com `tabela_vacinas()`, fonte única do gráfico) e `mor_*` (resumo, componentes, bairros); o `__main__` lista
  "[falta …]" para chave de tabela ausente.
- **B2** — `build/mapas_apresentacao.py`: mapas `apres_cadunico_uma_adulta_{n_,}bairro`,
  `apres_cadunico_inadequacao_{n_,}bairro`, `apres_cadunico_adensamento_bairro`; gráficos próprios (`desenha`)
  `apres_matriculas_rede_pandemia`, `apres_cobertura_vacinal_metas`, `apres_cadunico_pobreza_arranjo`; opções
  `outliers_fixos` e `piso`.
- **B3** — `primeira_infancia/impressao.py`: `piso` opcional em `_a4_mapa` (padrão: escala em zero, nada muda no analise.py).
- **B4** — `variantes/familia_cuidados.md` e `variantes/moradia.md`.
- **B5** — gerar PNG, conferir, `--publicar` (Família); README do deck; ROADMAP.

Riscos: servidor do mapa de fundo (ArcGIS) instável nesta data — mapas que falham mantêm o PDF anterior; Moradia depende
das silvers do CadÚnico (specification §4).
