# Tarefas — `specs/website_graficos`

## Bloco 0 — Planejamento
- [x] T0.1 Spec, plano e validação escritos antes da implementação (2026-09-25)
- [ ] T0.2 Sessão com o usuário: P1-P5

## Bloco 1 — Exclusões
- [ ] T1.1 `_subgrupo_excluido()` no gerador (E2, E3) aplicado em todos os cortes de subgrupo
- [ ] T1.2 E4 mapas maternos por bairro; E6 mapas de taxa de violência por bairro; E7; E8
- [ ] T1.3 E5 "Amarela e indígena" a partir dos absolutos
- [ ] T1.4 V0.*, VA.*

## Bloco 2 — Alternância Taxa ↔ Óbitos
- [ ] T2.1 `option_card_alternancia` (gerador), JS em `js/charts.js`, CSS em `css/components.css`
- [ ] T2.2 Aplicar nos 2 grupos de mapas de mortalidade por bairro
- [ ] T2.3 V9.*

## Bloco 3 — Paleta e teto
- [ ] T3.1 Validador `dataviz` nas cores do site; decisão P3
- [ ] T3.2 Teto P95 em todos os mapas contínuos por bairro

## Bloco 4 — Rótulos e totais
- [ ] T4.1 Unidades nos eixos (P5)
- [ ] T4.2 Valor na ponta das barras
- [ ] T4.3 Linhas de total fora dos gráficos de categorias
- [ ] T4.4 Base zero das taxas (P1)

## Bloco 5 — Pequenos múltiplos
- [ ] T5.1 Tipo novo no motor de gráficos; aplicar nos gráficos de 8-11 séries (P2)

## Bloco 6 — Fontes ABNT
- [ ] T6.1 Referência de `fontes.bib` nas caixas de fontes

## Bloco 6b — Textos do relatório
- [ ] T6b.1 Site lê `achados_<eixo>` (uma frase por linha) e `sintese_<eixo>` de `textos_curados.json` (§3b)

## Bloco 7 — Navegador e publicação
- [ ] T7.1 VN.*; commit do `website/` regenerado; deploy só com OK
