# TASKS — Revisão do deck (30 → 33 slides)

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-09-29)
- [x] P1 Leitura do pedido (`revision_readme.md`) contra o deck atual; pasta renomeada para `2026-09-29_slide_revision`
- [x] P2 Perguntas agrupadas ao usuário → D1-D8
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`
- [x] P4 Commit em `planning`
- [ ] P5 Validação do planejamento pelo usuário; push; abrir `spec/slide-revision`

## B1 — Estrutura e texto
- [ ] T1.1 Reordenar slides (§4), remover S06, manter S28 antes do QR
- [ ] T1.2 Cabeçalho: `subtitulo`, `contato`
- [ ] T1.3 Slides 02, 04, 05, 06, 08, 09, 10, 12, 14, 17, 19, 24, 25, 28 (mudanças do §4)
- [ ] T1.4 Slides novos 21, 26, 29, 30 (com `<!-- revisar -->` e notas do apresentador)
- [ ] T1.5 Varredura R1-R8 (grep: "0 a 5 anos", "extrema", "infância" sem "primeira", "Zika", "469", "ficam em branco")
- [ ] T1.6 `variantes/exemplo_secretaria.md` alinhada

## B2 — Números
- [ ] T2.1 Renomear chaves de pobreza; filtro pela faixa `0-218`
- [ ] T2.2 `censo_0_5_2022_mil`, `vf_notif_total_2025`, `vf_taxa_total_2025`

## B3 — Mapas do deck
- [ ] T3.1 `cmap`, `bins`, `outlier` opcionais em `MAPAS`; rampa terracota
- [ ] T3.2 Mapas `apres_censo_0_4_*`, `apres_taxa_mortalidade_infantil_bairro_2025`, `apres_baixo_peso_bairro_2025`, `apres_violencia_familiar_total_bairro_2025`
- [ ] T3.3 Conferir cor de todos os mapas do deck (nenhuma terra azul)

## B4 — Gráfico do deck
- [ ] T4.1 `graficos_apresentacao.py` + `apres_violencia_familiar_total_ano`; `figura()` resolve os dois módulos

## B5 — Tema
- [ ] T5.1 `.stats .destaque`, `.grupo`, `.nota.forte` em `tema/ipp.css`

## B6 — Rótulo de renda (projeto)
- [ ] T6.1 `cadunico.py` + textos curados (`analise.py`, `textos_curados.json`)
- [ ] T6.2 Rodar seção CadÚnico (`analises_env`), site, PDF sem `--publicar`

## B7 — Gerar e registrar
- [ ] T7.1 `gera_apresentacao.py --png`; revisão slide a slide; `validation.md`
- [ ] T7.2 `apresentacao/README.md`, especificação do projeto, ROADMAP, CHANGELOG
- [ ] T7.3 Merge em `planning`/`staging_main`; `--publicar` só com OK do usuário
