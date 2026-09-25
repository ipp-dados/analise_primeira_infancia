# Tarefas — `specs/2026-09-25_website_graficos`

## Bloco 0 — Planejamento
- [x] T0.1 Spec, plano e validação escritos antes da implementação (2026-09-25)
- [x] T0.2 Sessão com o usuário: P1-P5 (2026-09-25) — P1 base zero; P2 alternância "Painéis | Linhas" no mesmo
      cartão, abrindo em Painéis; P3 trocar agora as cores que reprovarem; P4 tudo nesta sessão, um commit por
      bloco (A primeiro); P5 reaproveitar `ROTULOS_EIXO` de `analise.py` (já existia)

## Bloco 1 — Exclusões
- [x] T1.1 `_subgrupo_excluido()` no gerador (E2, E3) aplicado em todos os cortes de subgrupo
- [x] T1.2 E4 mapas maternos por bairro; E6 mapas de taxa de violência por bairro; E7; E8
- [x] T1.3 E5 "Amarela e indígena" a partir dos absolutos
- [x] T1.4 V0.*, VA.*

## Bloco 2 — Alternância Taxa ↔ Óbitos
- [x] T2.1 `option_card_alternancia` (gerador), JS em `js/charts.js`, CSS em `css/components.css`
- [x] T2.2 Aplicar nos 2 grupos de mapas de mortalidade por bairro
- [x] T2.3 V9.* — de quebra: as pills trocavam só o painel, nunca o texto (bug anterior à rodada), corrigido

## Bloco 3 — Paleta e teto
- [x] T3.1 Validador `dataviz` nas cores do site; P3: `--c1…--c4` trocadas
- [x] T3.2 Teto P95 em todos os mapas contínuos por bairro

## Bloco 4 — Rótulos e totais
- [x] T4.1 Unidades nos eixos (parâmetro `unidade=` → `yLabel`)
- [x] T4.2 Valor na ponta das barras (agrupadas: só com até 12 barras)
- [x] T4.3 Linhas de total fora dos gráficos de categorias (conferido: nenhuma sobrou)
- [x] T4.4 Base zero das taxas (P1), com marcas de eixo redondas

## Bloco 5 — Pequenos múltiplos
- [x] T5.1 `pequenosMultiplos` no motor, automático a partir de 7 séries (P2)

## Bloco 6 — Fontes ABNT
- [x] T6.1 Referência de `fontes.bib` nas caixas de fontes

## Bloco 6b — Textos do relatório
- [x] T6b.1 Site lê `achados_<eixo>` (uma frase por linha) e `sintese_<eixo>` de `textos_curados.json` (§3b)

## Bloco 7 — Navegador e publicação
- [x] T7.1 VN.*; commit do `website/` regenerado; deploy só com OK (não feito)

## Bloco 8 — Revisão de unidades, nomes e títulos (pedido do usuário no meio da rodada, 2026-09-25)
- [x] T8.1 `%` só em percentual; taxas por mil com `‰` (formato `pm1`) — mortalidade neonatal/infantil, evitáveis
      < 5 anos, notificações por mil crianças
- [x] T8.2 Mortalidade infantil por raça/cor por mil nascidos vivos (era por 100), no site e na origem (`analise.py`:
      colunas `taxa_mortalidade_<raça>` e `taxa_mortalidade_infantil_total`; gráfico, mapa e `ROTULOS_A4_ARQUIVO`)
- [x] T8.3 Nomes padronizados: idade ("Menos de 1 ano"), sexo ("Meninas/Meninos"), raça ("Não informada"),
      subgrupos de causa evitável pelo código; cor fixa por entidade (raça/cor, sexo)
- [x] T8.4 Botões CSV/outliers fora da área do conteúdo (4 sobreposições → 0)
- [x] T8.5 Títulos de seção descritivos no site (fim de "Mapas", "Série temporal", "CadÚnico", "SISVAN"…), com
      âncora do id antigo; no PDF, "Razão de mortalidade materna" → "Óbitos maternos…" e violência "0 a 6" → "0 a 5"
- [x] T8.6 Textos curados com a unidade antiga convertidos (2 textos; DOCX → JSON → site/`analise.py`/LaTeX),
      registrados em `relatorio/controle_revisao.json` (`ajustes_manuais`, "revisar")
- [x] T8.7 Eixo y do baixo peso ao nascer ("9, 9, 10, 10" fora de posição) — marcas redondas
- [ ] T8.8 Figuras impressas do PDF regeneradas pela execução completa de `analise.py`
