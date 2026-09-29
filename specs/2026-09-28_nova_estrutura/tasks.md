# TASKS — Nova estrutura

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-09-28)
- [x] T0.1 Ler a planilha da equipe e as observações de texto; cruzar com `estrutura_eixos.md` e com o site
- [x] T0.2 Perguntas ao usuário (D1-D3) e a regra D4 (acrescentar, nunca remover)
- [x] T0.3 Atualizar `specs/estrutura_eixos.md` (Introdução + 7 eixos, notas por item, campo `eixo transversal`)
- [x] T0.4 Conferir: 51 → 51 itens, nenhum arquivo a mais ou a menos, `valida_estrutura` OK
- [x] T0.5 Conferir as observações do .txt nos textos curados (`specification.md` §6)
- [x] T0.6 Escrever specification/plan/tasks/validation
- [x] T0.7 Commit no `planning` (4e7e254); merge em `staging_main` ao fim da rodada

## Bloco 0 — Inventário
- [x] T0a Script de inventário do site (h2-h5, seeds, ids) e do PDF (figuras, tabelas)
- [x] T0b Capturas de tela de referência (desktop 1440, celular 390)

## Bloco 1 — Base comum
- [x] T1.1 `eh_panorama`, `eixos_politica`, `panorama` em `gera_estrutura_eixos.py`
- [x] T1.2 `blocos_relatorio` sem o panorama; blocos de `direito_ao_brincar`

## Bloco 2 — PDF
- [x] T2.1 `secoes_indicadores()` extraída (diff sem mudança nos eixos)
- [x] T2.2 Capítulo Introdução com o Panorama; "Os eixos da política" com 7
- [x] T2.3 Apêndice "Tabelas da Introdução"
- [x] T2.4 Ícone e `EIXO_META` de Direito ao Brincar; `--eixo 0`
- [x] T2.5 Compilar (`--sem-pdf` e completo); 0 `undefined`, overfull ≤ o de antes

## Bloco 3 — Site
- [x] T3.1 Panorama na Visão geral (cartões de Censo, Ripsa, SIDRA sexo/raça, Nascidos vivos)
- [x] T3.2 Separar Nascidos vivos dos cartões de mortalidade; renomear os cartões
- [x] T3.3 Prioridade reordenada (mortalidade → evitáveis → CadÚnico)
- [x] T3.4 Inclusão só com pendentes; Família e Cuidados reordenada (educação → vacinação → CadÚnico arranjo)
- [x] T3.5 Proteção reorganizada + pendente "todas as naturezas"; ids antigos preservados
- [x] T3.6 Aba Direito ao Brincar (h2, ícone, `_EIXO_META`, grade de eixos)
- [x] T3.7 Barra de abas com 8 abas no desktop; sumário lateral da Visão geral
- [x] T3.8 Inventário depois = antes (+ Nascidos vivos h3, + pendente, + aba)

## Bloco 4 — Notas "menores de 5 anos"
- [x] T4.1 `analise.py`: nota no `fonte_dados` das 4 chamadas; rodar a seção
- [x] T4.2 Site: nota nas pills "Menores de 5 anos"
- [x] T4.3 Aviso à curadoria sobre os textos O3/O4 (na mensagem ao usuário e em specification.md §6)

## Bloco 5 — DOCX e conferências
- [x] T5.1 Regenerar o DOCX de curadoria na ordem nova
- [x] T5.2 `valida_textos_publicados.py`, `confere_textos.py`, `inventario_fontes.py` sem erro

## Bloco 6 — Fechamento
- [x] T6.1 `validation.md`
- [x] T6.2 Documentação (especificação do projeto, CLAUDE.md, ROADMAP, README, relatorio/specs.md)
- [ ] T6.3 Regenerar site e PDF; publicar com o OK do usuário; merge; tag `rodada/nova_estrutura`
  - 2026-09-29: merge em `planning`/`staging_main` feito (`ab9f803`) e site publicado; PDF e tag seguem em
    `specs/2026-09-29_pendencias` (T9.3, com OK do usuário)
