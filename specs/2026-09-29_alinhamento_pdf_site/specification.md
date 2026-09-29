# SPECIFICATION — Alinhamento PDF × site (rodada de 2026-09-29)

Status: **planejada em 2026-09-29** (branch `planning`); implementação em `spec/alinhamento-pdf-site`. O *como* está
em `plan.md`, as tarefas em `tasks.md`, os critérios de aceite em `validation.md`.

## 1. Contexto

Depois da rodada `specs/2026-09-29_pendencias`, o usuário perguntou se o PDF segue a estrutura nova do site. A
comparação (capítulos e seções do `capitulos.tex` gerado × abas e cartões do `index.html`) mostrou a mesma espinha —
Introdução com panorama e os 7 eixos, na mesma ordem — e quatro divergências reais:

1. **Ordem em Prioridade:** o site abre com o cartão de mortalidade por idade ao óbito (inclui as taxas infantil e
   pós-neonatal); o PDF põe "Taxa de mortalidade na primeira infância" depois dos blocos de causas evitáveis (a
   planilha da equipe de 2026-09-28 apontava o indicador para o cartão de evitáveis).
2. **Cobertura vacinal:** o site mostra a série anual por imunobiológico; no PDF a seção fica sem figura, porque a
   chamada de `cobertura_vacinal_epi_ano` está comentada em `analise.py` (exclusão E1, 2026-09-25: o PNG no disco
   era antigo).
3. **Violência familiar por CAP e CadÚnico ÷ população:** no site, tabelas dentro do cartão; no PDF, as mesmas
   tabelas só no apêndice, e a seção fica vazia.
4. **Causas evitáveis por raça/cor:** seção pendente no PDF (os 4 gráficos saíram em 2026-09-25), ausente no site.

Além disso, os quadros de "indicador pendente" do site mostram as anotações internas do crosswalk ("baixar dados —
Léo", "Posterior", "Posterior (apenas cad)"). O PDF já usa uma frase fixa formal (`TEXTO_PENDENTE` em `gera_latex.py`).

## 2. Decisões do usuário (2026-09-29)

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | **O PDF segue o site** na ordem de Prioridade: "Taxa de mortalidade na primeira infância" logo depois das taxas neonatais precoce e tardia | "adjust the pdf"; substitui, só na ordem, a posição da planilha de 2026-09-28 |
| D2 | **Descomentar** a série de cobertura vacinal (`cobertura_vacinal_epi_ano`) em `analise.py`; a figura volta ao PDF e ao DOCX (o texto curado já existe) | E1 era só "PNG antigo"; o site já desenha a série |
| D3 | **Pôr no relatório** as tabelas de violência familiar por CAP e de CadÚnico ÷ população, **no corpo da seção** (como no site), não só no apêndice | a seção deixa de ficar vazia; mesma leitura nos dois produtos |
| D4 | **Remover** a seção "Mortalidade infantil por causas evitáveis, por raça/cor" do PDF e do DOCX (E16) | seção vazia; o site não a tem. As seções "SISVAN (número)" **ficam** (resposta do usuário) |
| D5 | Quadros de pendente **no site e no PDF**: a frase fixa formal + um **motivo formal por item**, o mesmo texto nos dois | o público não lê anotações internas; o motivo explica o que falta |

## 3. Requisitos

**R1 — Ordem (D1).** No `specs/estrutura_eixos.md`, o item "Taxa de mortalidade na primeira infância" passa para
logo depois de "Taxa de mortalidade neonatal tardia"; o PDF e o DOCX seguem. Nenhum outro item muda de lugar. Nota
no item registrando a mudança.

**R2 — Vacinação (D2).** `analise.py` gera `cobertura_vacinal_epi_ano` (tela e A4); o crosswalk ganha a
`visualização:`; E1 em `specs/exclusoes.md` registra a volta; o alerta "texto pronto, figura fora" em
`relatorio/controle_revisao.json` vai para `alertas_resolvidos`.

**R3 — Tabelas no corpo (D3).** Chave nova e opcional `tabela_no_texto:` no crosswalk (era a tarefa T4.3 de
`specs/2026-09-25_relatorio_latex`, no backlog): o gerador do PDF põe a tabela na seção, com a mesma formatação do
apêndice, e não a repete no apêndice. Usada em `cadunico_razao_populacao_0_a_5_2026.csv` e
`violencia_familiar_por_cap.csv`. O DOCX de curadoria não muda (texto por figura).

**R4 — Remoção (D4).** O item sai do crosswalk; `specs/exclusoes.md` ganha **E16** com as notas que estavam no item
(como voltar, ressalva de 1996). Os dados e os gráficos comentados continuam onde estão.

**R5 — Pendentes (D5).** Campo novo `motivo:` em cada item `status: pendente` do crosswalk (texto público, formal).
PDF: `TEXTO_PENDENTE` + motivo. Site: o mesmo par, lido do crosswalk pelo título (sem texto repetido no gerador). As
`nota:` internas continuam no crosswalk e no DOCX interno.

## 4. Fora do escopo

- Publicar o PDF, o deploy do site e o deck (continuam esperando o OK da rodada `pendencias`).
- Seções "SISVAN (número)" (ficam como estão, D4).
- Reordenar o site ou os outros eixos (a comparação não achou outra divergência de ordem).
