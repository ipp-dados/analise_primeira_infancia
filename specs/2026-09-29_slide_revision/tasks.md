# TASKS — Revisão do deck (30 → 33 slides)

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-09-29)
- [x] P1 Leitura do pedido (`revision_readme.md`) contra o deck atual; pasta renomeada para `2026-09-29_slide_revision`
- [x] P2 Perguntas agrupadas ao usuário → D1-D8
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`
- [x] P4 Commit em `planning`
- [x] P5 Pedido de implementação do usuário (2026-09-29); branch `spec/slide-revision` aberta (sem push)

## B1 — Estrutura e texto
- [x] T1.1 Reordenar slides (§4), remover S06, manter S28 antes do QR
- [x] T1.2 Cabeçalho: `subtitulo`, `contato`
- [x] T1.3 Slides 02, 04, 05, 06, 08, 09, 10, 12, 14, 17, 19, 24, 25, 28 (mudanças do §4)
- [x] T1.4 Slides novos 21, 26, 29, 30 (com `<!-- revisar -->` e notas do apresentador)
- [x] T1.5 Varredura R1-R8 (grep: "0 a 5 anos", "extrema", "infância" sem "primeira", "Zika", "469", "ficam em branco")
- [x] T1.6 `variantes/exemplo_secretaria.md` alinhada

## B2 — Números
- [x] T2.1 Renomear chaves de pobreza; filtro pela faixa `0-218`
- [x] T2.2 `censo_0_5_2022_mil`; vínculos de violência separados (`vf_*_pai/outros_2025`) — a soma (`vf_*_total_2025`) saiu com D9

## B3 — Mapas do deck
- [x] T3.1 `cmap`, `bins`, `outlier` opcionais em `MAPAS`; rampa terracota
- [x] T3.2 Mapas `apres_censo_0_4_*`, `apres_taxa_mortalidade_infantil_bairro_2025`, `apres_baixo_peso_bairro_2025` (o de violência somada saiu com D9: o deck usa os mapas de mãe e pai do relatório)
- [x] T3.3 Conferir cor de todos os mapas do deck (nenhuma terra azul)

## B4 — Gráfico do deck
- [x] T4.1 ~~`graficos_apresentacao.py`~~ retirado com D9; `figura()` usa a versão de impressão dos gráficos (`visualizacoes/a4/`)

## B5 — Tema
- [x] T5.1 `.stats .destaque`, `.grupo`, `.nota.forte` em `tema/ipp.css`

## B6 — Rótulo de renda (projeto)
- [x] T6.1 `cadunico.py` + textos curados (`analise.py`, `textos_curados.json`)
- [x] T6.2 Rodar seção CadÚnico (`analises_env`), site, PDF sem `--publicar`

## B7 — Gerar e registrar
- [x] T7.1 `gera_apresentacao.py --png`; revisão slide a slide; `validation.md`
- [x] T7.2 `apresentacao/README.md`, especificação do projeto, ROADMAP, CHANGELOG
- [x] T7.3 Merge em `planning`/`staging_main`, push e `--publicar` do deck e do PDF (OK do usuário, 2026-09-29; ainda com a marca "em desenvolvimento"); deploy do site pelo `deploy-relatorio.yml` (manual)
- [x] T7.4 D9: sem soma de vínculos; achados corrigidos (legenda do gráfico de raça, fonte "0 a 5 anos" no rodapé, títulos embutidos dos gráficos)
