# Plano — `specs/2026-09-28_documentacao`

**Rodada C** do pedido de 2026-09-28 (`specs/2026-09-28_melhorias_site/plan.md`): `ROADMAP.md`, Próximos, **item 6 —
Atualizar a documentação do projeto**, e o pedido de um **documento atualizado que explique o projeto inteiro, como
uma especificação funcional/técnica**. Feita depois da Rodada B (`specs/2026-09-28_organizacao`), que mudou caminhos.
Branch `spec/documentacao`, a partir de `staging_main` (`621d1fe`).

## Entregas

1. `docs/especificacao_projeto.md` (novo): visão geral, escopo (eixos, indicadores, níveis geográficos), fontes,
   requisitos funcionais e não funcionais, arquitetura e fluxo de dados (diagrama), componentes, regras, processos
   (rodadas, curadoria, estrutura, publicação), operação, manutenção do próprio documento, limitações, glossário.
   Formato: Markdown no repositório (decisão do plano aprovado; lê-se no GitHub, com o diagrama Mermaid).
2. Alinhamento dos documentos ao estado real (item 6: nível `ra`, `dados_locais/protecao/`, `carrega_sinan_*`, eixo
   Proteção, relatório LaTeX, e o que as rodadas A e B mudaram): `README.md`, `CLAUDE.md`, `specs/tech-stack.md`,
   `specs/constitution.md`, `relatorio/specs.md` (nota de documento histórico).
3. `.env.example` (citado por README e tech-stack, mas inexistente).

## Regra

Todo número do documento sai de um script (contagens por eixo de `relatorio/curadoria/gera_estrutura_eixos.py`,
níveis geográficos dos geojson, páginas do PDF); todo caminho citado existe. Nada muda em código ou saída.
