# VALIDATION — Nova estrutura

## Planejamento (2026-09-28)

| Verificação | Resultado |
|---|---|
| `parse_estrutura_eixos` no arquivo novo | 8 `##`: Introdução (7 itens), Prioridade (16), Inclusão (3), Família e Cuidados (8), Proteção (7), Direito ao Brincar (1), Alimentação (6), Moradia (3) |
| Itens antes × depois | 51 × 51 |
| Arquivos (visualização/mapa/tabela) removidos | nenhum |
| Arquivos acrescentados | nenhum (só redistribuição) |
| `valida_estrutura` | OK: toda referência existe |
| Observações do .txt | O1/O2 corrigidas no texto; O3/O4 parciais; nenhuma na legenda; O5 não se aplica (item pendente) — `specification.md` §6 |

⚠️ Enquanto o Bloco 2 não estiver implementado, um build do PDF a partir deste `estrutura_eixos.md` trataria a
Introdução como "Eixo 1 de 8". Não publicar o PDF entre o merge do planejamento e o Bloco 2.

## Implementação (2026-09-28, branch `spec/nova_estrutura`)

| Verificação | Critério | Resultado |
|---|---|---|
| Inventário do site, depois × antes | nenhuma seed, figura ou id a menos | **OK**: 113 × 113 seeds, iguais; ids a menos só os numéricos automáticos (`c-N`/`m-N`, renumerados); ids antigos dos cartões renomeados mantidos como âncora |
| Links antigos | abrem o lugar novo | **OK**: `#prioridade/mapas` abre a Visão geral (cartão mudou de aba; `navigation.js`) |
| Desktop 1440 px | diferença só na barra de abas, na Visão geral e na ordem | **OK** (capturas antes/depois conferidas; topo da Visão geral igual, sumário com os h3 do panorama) |
| Barra de abas | 8 abas sem rolagem no desktop | **OK** em 1100, 1150, 1279, 1280, 1440 px (rótulo curto "Família"/"Brincar" e espaço 4 px abaixo de 1280) |
| Celular 390 px | sem rolagem horizontal | **OK** (largura da página 390; barra de abas rola, como antes) |
| PDF | compila; 0 `undefined`; Introdução com Panorama; 7 capítulos de eixo; apêndice da Introdução | **OK**: 158 páginas; overfull > 5 pt: 14, os mesmos já aceitos em `2026-09-25_relatorio_latex` (cabeçalhos de tabela do apêndice) |
| Figuras e tabelas do PDF, depois × antes | nenhuma a menos | **OK**: 94 × 94 figuras e 43 × 43 tabelas, os mesmos arquivos; pendentes 9 → 10 (item novo) |
| DOCX de curadoria | ordem nova; textos preservados | **OK**: 77 × 77 textos curados, nenhum perdido ou alterado; 94 imagens |
| Textos publicados | frases curadas no site e no PDF | **OK**: `valida_textos_publicados.py` (PDF de `_build`): 0 textos com frase ausente |
| Notas "menores de 5 anos" | 4 legendas do PDF e pills do site | **OK**: 4 legendas no PDF; 11 ocorrências no site (séries, pills por subgrupo e mapas de menores de 5) |
| Tamanho do site | < 1 MB `index.html`, < 2 MB total | **OK**: `index.html` 347 KB; total 1,06 MB |

Não publicado: `relatorio/analise_primeira_infancia.pdf` (só com `--publicar`, a pedido do usuário) e o deploy do site.
