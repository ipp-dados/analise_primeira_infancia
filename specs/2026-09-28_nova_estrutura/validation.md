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

## Implementação (a preencher)

| Verificação | Critério | Resultado |
|---|---|---|
| Inventário do site, depois × antes | nenhuma seed, figura ou id a menos | |
| Links antigos (`antigo=`, aliases) | todos abrem o lugar novo | |
| Desktop 1440 px | diferença só na barra de abas, na Visão geral e na ordem dos painéis | |
| Barra de abas | 8 abas sem rolagem no desktop | |
| Celular 390 px | Visão geral e aba nova sem rolagem horizontal | |
| PDF | compila; 0 `undefined`; Introdução com Panorama; 7 capítulos de eixo; apêndice da Introdução | |
| Figuras e tabelas do PDF, depois × antes | nenhuma a menos | |
| DOCX de curadoria | ordem nova; `valida_textos_publicados.py` OK | |
| Notas "menores de 5 anos" | nas 4 legendas do PDF e nas pills do site | |
| Tamanho do site | abaixo de 1 MB `index.html` e 2 MB no total (ou aviso justificado) | |
