# PLAN — Nova estrutura (Introdução com panorama + 7 eixos)

Especificação: `specification.md`. Branch de implementação: `spec/nova_estrutura`, a partir de
`staging_main` depois do merge do `planning` (que traz esta pasta e o `estrutura_eixos.md` novo).
Commits: `SPEC-NovaEstrutura: Bloco N -- …`.

**Regra transversal (usuário, 2026-09-28): acrescentar o que falta, nunca remover o que sobra.** Cada bloco
termina com a conferência do Bloco 0 (inventário antes/depois).

## Bloco 0 — Inventário de referência (antes de mexer)
- Guardar, do site atual, a lista de h2/h3/h4/h5, as `seed`s de figura e os ids (inclusive `antigo=`), com um
  script em `scratchpad` que lê `website/index.html` e `website/data/charts.js`.
- Guardar do PDF atual a lista de figuras e tabelas (`relatorio/latex/gerado/capitulos.tex` + `apendices.tex`).
- Capturas de tela do desktop (1440 px) e do celular (390 px) de todas as abas (Playwright, `requirements-dev.txt`).
- Critério de todos os blocos: nenhuma seed, figura ou tabela a menos que no inventário.

## Bloco 1 — Base comum (`relatorio/curadoria/gera_estrutura_eixos.py`)
- `eh_panorama(eixo)`, `eixos_politica(estrutura)` (sem o panorama) e `panorama(estrutura)`.
- `blocos_relatorio()` pula o panorama e gera os blocos de `direito_ao_brincar`.
- `__main__` imprime "Introdução (panorama): N itens" e "Eixos: 7".

## Bloco 2 — PDF (`relatorio/latex/build/gera_latex.py`, `gera_icones.py`)
- Extrair o laço de subseções de `capitulos()` para `secoes_indicadores(subsecoes, nivel, tabs)`, sem mudar a saída
  dos eixos (conferir com diff de `gerado/capitulos.tex`: só muda a ordem e o novo eixo).
- Capítulo Introdução: texto → como_ler → Panorama (subsections) → Os eixos da política (7).
- Apêndice "Tabelas da Introdução"; `\eixo{i}{7}`; `EIXO_META` + ícone de Direito ao Brincar.
- `--eixo N` continua contando só os eixos (1-7); `--eixo 0` = só a Introdução (novo, para iterar).

## Bloco 3 — Site (`website/build/build_site.py`)
- Mover blocos de código (recortar e colar, sem reescrever) para a ordem da `specification.md` §5.1.
- Separar "Nascidos vivos" (série + mapa) dos dois cartões de mortalidade; renomear os cartões que ficam.
- Panorama na Visão geral (`h2_panorama()` capturado no ASSEMBLE); sumário lateral da Visão geral.
- Proteção reorganizada (taxas dentro de Violência familiar; dez maiores taxas junto dos dez maiores em número);
  pendente novo; ids antigos preservados.
- Aba nova Direito ao Brincar; `_EIXO_META`; ícone no sprite; grade de eixos com 7 cartões.
- Barra de abas: 8 abas no desktop (encurtar rótulos se não couber, sem CSS novo).
- `js/navigation.js`: conferir que rotas `#visao-geral/<h3>` do panorama funcionam (o sumário usa `data-alvo`).

## Bloco 4 — Notas de legenda "menores de 5 anos" (observações O1-O4)
- `analise.py`: `Nota: agrega os recortes de menores de 1 ano e de 1 a 4 anos` no `fonte_dados` das 4 chamadas;
  rodar a seção de causas evitáveis por CAP (PNG + A4 + manifesto).
- Site: a mesma nota nas pills "Menores de 5 anos".
- Registrar à curadoria que os textos dos 2 mapas (O3/O4) só falam dos recortes de forma indireta (sem reescrever).

## Bloco 5 — DOCX de curadoria e conferências
- Regenerar `relatorio/curadoria_textos.docx`; rodar `valida_textos_publicados.py`, `confere_textos.py` e
  `inventario_fontes.py`.

## Bloco 6 — Validação, documentação e fechamento
- `validation.md` preenchido (inventário antes/depois, capturas de tela, PDF compilado sem `undefined`).
- Atualizar `docs/especificacao_projeto.md` (eixos: 7 + panorama), `CLAUDE.md` (6 → 7 eixos; Introdução),
  `ROADMAP.md` (rodada em andamento/feita; lacunas: taxa de 1-4 anos, violência geral, efeito do eixo
  transversal), `README.md` (Update Table, 1-3 linhas), `relatorio/specs.md` (histórico do site).
- Regenerar site + PDF (`--publicar` só com o OK do usuário) e fazer o merge em `staging_main`.
