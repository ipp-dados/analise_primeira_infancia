# Tarefas — `specs/2026-09-28_melhorias_site`

- [x] T0.1 Branch `spec/melhorias-site` a partir de `staging_main` (2702ef9); pasta da rodada
- [x] T0.2 Capturas de referência (antes): todas as abas a 1400 px e 390 px

## Bloco 1 — favicon (U1)
- [ ] T1.1 Opções em SVG (`website/build/favicon_opcoes/`), recomendada como padrão
- [ ] T1.2 `website/build/gera_favicon.py`: `.ico` (16/32/48) e `apple-touch-icon.png` (180) a partir do SVG
- [ ] T1.3 `<link>`s no `<head>`; `.ico` no workflow de deploy e no `website/README.md`

## Bloco 2 — abertura do eixo (U2)
- [ ] T2.1 `blocos_relatorio()`: `introducao_<eixo>` depois de `achados_<eixo>`
- [ ] T2.2 Site: parágrafo sob "Principais achados" (+ CSS)
- [ ] T2.3 PDF: parágrafo depois do ambiente `achados`
- [ ] T2.4 DOCX: bloco e bookmark (vem de `blocos_relatorio()`)

## Bloco 3 — lorem ≤ 150 (U3)
- [ ] T3.1 Faixa 100-150 nos três geradores; `resumo`/Introdução/Considerações 150 nos placeholders e em `sincroniza_docx.py`
- [ ] T3.2 `gera_docx`: descartar lorem do DOCX anterior; regenerar `curadoria_textos.docx`
- [ ] T3.3 Conferir: sincronização sem mudança em `textos_curados.json`

## Bloco 4 — só Painéis (U4)
- [ ] T4.1 `js/charts.js` sem controle e sem vista de linhas; CSS `.sm-ctrl` fora

## Bloco 5 — HTML menor (U5)
- [ ] T5.0 Capturas intermediárias (depois dos blocos 1-4) + `outerHTML` dos mapas + CSVs dos mapas
- [ ] T5.1 Mapas em `window.MAPAS` + montagem em `js/charts.js`
- [ ] T5.2 CSV dos mapas no clique
- [ ] T5.3 Sprite de ícones
- [ ] T5.4 Arredondamento em `data/charts.js`

## Fechamento
- [ ] T6.1 PDF (`gera_latex.py --publicar`), DOCX, site regenerados; `valida_textos_publicados.py`
- [ ] T6.2 `validation.md` preenchido
- [ ] T6.3 Docs: `website/README.md`, skills (`build_website`, `export_pdf_report`), `ROADMAP.md`, `CHANGELOG.md`, `README.md`
