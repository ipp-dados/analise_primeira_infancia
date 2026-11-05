# TASKS — Versão final do site (rodada de 2026-11-05)

Legenda: [x] feito · [ ] a fazer. Pedido original: `website_release.md` (raiz). A especificação e o plano completos
(banner, mapa de referência, rodapé, faixa beta, relatório, `main`) vêm no planejamento desta rodada.

## Bloco 1 — Textos
- [x] T1.1 Textos da curadoria de 05/11 (DOCX) conferidos e importados (36; `textos_docx_05_11_revisao.md`)
- [x] T1.2 Textos das 19 abas sem arquivo (17 chaves; `textos_abas_propostos.md`)
- [x] T1.3 Textos dos eixos (achados, introdução, síntese) em `relatorio/textos_eixos.md`: 9 escritos pelo usuário (Prioridade, Inclusão, Família e Cuidados; corrigidos contra os dados) e 12 propostos e aprovados (Proteção, Brincar, Alimentação, Moradia; `textos_eixos_propostos.md`); importados com `relatorio/curadoria/importa_textos_eixos.py`. Site e PDF sem lorem;
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

## Bloco 3 — Banner e rodapé
- [x] T3.1 Foto do Unsplash (Compagnons, @sigmund, Licença da Unsplash) recortada e comprimida por `website/build/gera_banner.py` (960 px 20 KB, 1600 px 45 KB); crédito com links no banner
- [x] T3.2 Banner novo: foto à direita com máscara (sem emenda), texto e botões legíveis; celular com a foto bem esmaecida e o crédito no alto; site 1,49 MB
- [x] T3.3 E-mail de contato fora do rodapé (2026-11-05)
- [x] T3.4 Links do banner e do rodapé conferidos (HTTP 200); Transparência Rio trocado para transparencia.prefeitura.rio (o antigo estava quebrado); Unsplash responde 401 só a scripts

## Bloco 4 — Mapa de referência
- [x] T4.1 Mapa de referência na Visão geral (`mapa_referencia_html()` em `build_site.py`): bairros, RA e AP como contornos da geometria compartilhada, botões de nomes por camada (`initMapaReferencia` em `js/charts.js`), tooltip do bairro com RA e AP; nomes das RA com acento em todos os mapas de RA (`_NOME_RA`)
- [x] T4.2 CSV bairro → RA → AP no botão do cartão
- [x] T4.3 Figura A4 `mapas/a4/mapa_referencia_bairros_ra_ap.pdf` (`mapa_referencia_a4` em `primeira_infancia/impressao.py`, chamada na seção Censo do `analise.py`); entra no capítulo de Introdução no Bloco 5

## Bloco 5 — PDF em `.tex` por capítulo, capa e folha de rosto
- [ ] T5.1 PDF de referência (PNG das páginas)
- [ ] T5.2 Exportar `capitulos/*.tex`; `relatorio.tex` com `\input`; `gera_latex.py` sem capítulos nem JSON de textos
- [ ] T5.3 Checagem de rótulos (figuras/tabelas citadas existem)
- [ ] T5.4 Comparar com o PDF de referência
- [ ] T5.5 Nova capa e folha de rosto

## Bloco 6 — Curadoria só do site, sem DOCX
- [ ] T6.1 Tag `rodada/curadoria_docx`; apagar os scripts DOCX
- [ ] T6.2 `confere_textos.py` sem DOCX
- [ ] T6.3 Skills, `CLAUDE.md`, especificação do projeto

## Bloco 7 — Release e Actions
- [ ] T7.1 Instalar o `gh`; o usuário faz `gh auth login`
- [ ] T7.2 Passo de publicação da Release
- [ ] T7.3 Deploy automático na `main`; workflow de checagem em `staging_main`

## Bloco 8 — Versão final, revisão e teste
- [ ] T8.1 `publicacao.json` → `false`; regerar site e PDF
- [ ] T8.2 Revisão de pipelines e documentação; títulos "até 72 meses"
- [ ] T8.3 Teste completo desktop e celular

## Bloco 9 — Publicação (com OK)
- [ ] T9.1 Merge em `staging_main`; tag `rodada/versao_final_site`
- [ ] T9.2 `staging_main` → `main`; deploy conferido
- [ ] T9.3 Release do PDF
- [ ] T9.4 Constituição §7 e `CLAUDE.md`
