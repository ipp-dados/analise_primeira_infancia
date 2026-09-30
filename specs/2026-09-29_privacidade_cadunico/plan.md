# Rodada `privacidade_cadunico` — plano

Branch `spec/privacidade-cadunico` a partir de `planning`; merge em `planning` e `staging_main` ao fim, com push.
Decisões D1-D3 em `specification.md`.

## Levantamento

- `analise.py` (seção CadÚnico): `suprime_celulas_pequenas` em l. ~589 (`cadunico_por_bairro_2026`), ~636
  (`..._ate_4_2026`), ~656 (`tabela_mapa_cadunico_criancas_2026` + mapa), ~682 (`..._0_a_4_2026` + 2 mapas), ~870
  (`tabela_mapa_cadunico_recortes_bairro_2026` + 2 mapas). As duas primeiras são por **nome** de bairro dos Correios
  (com "Sem bairro identificado" e "Total"); as três de mapa já têm `codbairro` (`junta_codbairro_por_bairro`).
- RA e AP de cada bairro: `dados_locais/geo/limite_bairros_rio.geojson` (`codra`, `regiao_adm`, `area_plane`).
- Site: `mapa_svg(..., col_suprimido=...)` em `website/build/build_site.py`; os mapas do CadÚnico leem as tabelas de
  mapa. Mapas PNG/A4: `mapa_coropletico_bairros` (`primeira_infancia/mapas.py`).
- PDF: `relatorio/latex/build/tabelas.py` já põe a nota de supressão quando há coluna `suprimido`.

## Blocos

**B1 — Função.** `agrega_bairros_pequenos` (R1) + teste rápido com dados sintéticos (conjuntos RA → AP → município,
complemento, conjunto que não fecha).

**B2 — `analise.py`.** Trocar as 5 chamadas de `suprime_celulas_pequenas` por bairro pela agregação; as tabelas por
nome ganham `codbairro` para achar a RA (mesma normalização de nomes dos mapas). Mapas de percentual com a taxa do
conjunto; mapas de contagem com os agregados sem cor; nota no rodapé.

**B3 — Site.** `mapa_svg` com `col_agregado`: tooltip "Demais bairros da RA X: valor" e CSV com a coluna do conjunto;
cartões do CadÚnico passam a usá-la.

**B4 — Rodar e conferir.** Execução completa de `analise.py` (precisa do banco); site, PDF (sem `--publicar`), DOCX,
deck (números do CadÚnico). Script de auditoria (R3) sobre `tabelas_finais/`, `website/` e o PDF.

**B5 — Regra e registro.** Constituição §6, `CLAUDE.md`, `ROADMAP.md` (histórico, D3), CHANGELOG, README,
especificação do projeto; merge e push.

## Riscos

- Somas por RA mudam os números mostrados em alguns bairros (antes vazios): conferir que os totais fecham com o município.
- Textos curados que citem bairros agora agregados: listar e marcar `revisar`.
