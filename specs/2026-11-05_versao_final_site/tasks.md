# TASKS — Versão final do site (rodada de 2026-11-05)

Legenda: [x] feito · [ ] a fazer. Pedido original: `website_release.md` (raiz). A especificação e o plano completos
(banner, mapa de referência, rodapé, faixa beta, relatório, `main`) vêm no planejamento desta rodada.

## Bloco 1 — Textos
- [x] T1.1 Textos da curadoria de 05/11 (DOCX) conferidos e importados (36; `textos_docx_05_11_revisao.md`)
- [x] T1.2 Textos das 19 abas sem arquivo (17 chaves; `textos_abas_propostos.md`)
- [ ] T1.3 Textos dos eixos (achados, introdução, síntese) — escritos pelo usuário em `relatorio/textos_eixos.md` (9 de 21 importados em 2026-11-05: Prioridade, Inclusão, Família e Cuidados; `relatorio/curadoria/importa_textos_eixos.py`);
      importar e conferir os números citados
- [x] T1.4 **Dividir a Introdução da Visão geral** (pedido do usuário, 2026-11-05): abertura de 1 parágrafo (resumo do
      1º parágrafo atual) no início da aba e, no fim da aba, a seção **"Notas sobre o projeto e metodologia"** com até
      2 parágrafos (resumo dos parágrafos 2 a 4). Chaves: `introducao` (abertura) e `notas_projeto_metodologia`
      (fechamento). Conferir também o capítulo de Introdução do PDF, que lê a mesma chave `introducao`.

## Bloco 2 — Dados faltantes e plano para gestores
- [x] T2.1 Lista de todos os dados faltantes (pedido do usuário, 2026-11-05): `docs/dados_faltantes.csv` — 12 itens: os
      3 `status: pendente` do crosswalk (o aviso de pendência em Prioridade e os dois de Proteção) e 9 lacunas do
      ROADMAP e de `specs/exclusoes.md`
- [x] T2.2 Documento para gestores (Claude Docs, "Diagnóstico da Primeira Infância — dados faltantes e plano de
      entrega"): situação das entregas, tabela dos 12 itens com situação e prioridade editáveis, plano em 3 fases e
      2 portas (sem datas: a definir pelos gestores), pedidos e decisões
- [x] T2.2b Itens 13 a 15 (reunião do eixo Alimentação com a SMS, 2026-11-05) na lista, no documento e no ROADMAP
- [ ] T2.3 Manter a lista e o documento em dia quando um item mudar (pedido feito, dado recebido)
