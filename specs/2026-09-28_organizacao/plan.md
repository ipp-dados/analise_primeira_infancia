# Plano — `specs/2026-09-28_organizacao`

**Rodada B** do pedido de 2026-09-28 (`specs/2026-09-28_melhorias_site/plan.md`): `ROADMAP.md`, Próximos, **item 1 —
Organização do projeto**, fases **1a** e **1b** (aprovadas pelo usuário; a **1c**, reorganizar as pastas de dados e
saídas, fica para uma rodada própria). Branch `spec/organizacao`, a partir de `staging_main` (`8dbf8c3`). Execução
completa do notebook contra o banco do CadÚnico autorizada pelo usuário (consultas só de leitura).

## 1. Regra da rodada

É refatoração: **mesmas saídas antes e depois**. Uma execução completa de `analise.py` antes de mexer (referência) e
outra depois; hash de todo arquivo gravado em `tabelas_finais/`, `visualizacoes/`, `mapas/` e `dados_locais/` (PDF sem
datas de criação/ID; XLSX pelo conteúdo das planilhas). Os geradores que dependem dos scripts movidos (site, LaTeX,
DOCX, inventário de fontes) também têm de produzir o mesmo resultado.

## 2. Ponto de partida

| Aspecto | Hoje |
|---|---|
| `analise.py` | 4.786 linhas; linhas 1-1897 são imports + 160 nomes auxiliares (funções e constantes) em 9 subseções; 1 função auxiliar perdida na seção Proteção (`_limite_escala_p95`) |
| Dependências entre as subseções | gráficos ↔ impressão ↔ mapas formam um ciclo (constantes de estilo e ajudantes de mapa usados pela variante de impressão, que por sua vez é chamada pelos gráficos e mapas) |
| Scripts de pipeline | `.claude/skills/export_pdf_report/scripts/*.py` (estrutura dos eixos, DOCX de curadoria, sincronização, updates, validação) importados por `website/build/`, `relatorio/latex/build/` via `sys.path` apontando para dentro da skill |
| `requirements.txt` | `pip freeze` de 130 pacotes (inclui toda a pilha do Jupyter e dependências transitivas); `playwright` (usado em desenvolvimento) não está listado |
| Arquivos soltos | `relatorio/latex/relatorio.aux/.fdb_latexmk/.fls/.log` fora de `_build/` (de uma compilação manual antiga) |

## 3. Fases

**1a — arrumação sem mudar código de análise**
1. Scripts de pipeline saem da skill para `relatorio/curadoria/` (`git mv`, histórico preservado); `sys.path` e caminhos
   atualizados nos importadores; a skill passa a só chamá-los.
2. `requirements.txt` com as dependências diretas (importadas pelo código ou necessárias para rodar/abrir o notebook),
   versões fixadas nas do ambiente atual; `requirements-dev.txt` com as de desenvolvimento (Playwright). Documentar o
   ambiente do CadÚnico (`psycopg` 3, env `analises_env`).
3. Apagar os arquivos soltos, olhando cada um antes e registrando o que saiu (`validation.md`).

**1b — `analise.py` em módulos**
1. Pacote `primeira_infancia/` na raiz, um módulo por subseção auxiliar, com a camada de estilo separada para quebrar o
   ciclo: `conexao`, `limpeza`, `estilo`, `impressao`, `graficos`, `mapas`, `protecao`, `cadunico`, `populacao`,
   `educacao`. O texto das células markdown de cada subseção vira a docstring do módulo.
2. Extração **mecânica** (script, AST): cada definição vai inteira, sem reescrever corpo nenhum; os imports entre
   módulos são calculados pelos nomes que cada definição usa. `__all__` exporta todos os nomes (inclusive os com `_`,
   que as seções usam), e `analise.py` faz `from primeira_infancia import *` — as seções de análise não mudam.
3. `analise.py` continua Jupytext `py:percent`, com a mesma ordem de seções (a decisão de `specs/2026-09-22_ajuste_eixos`
   §9.1, de não reordenar fisicamente, continua válida: a ordem é de dependência de dados).

## 4. Riscos

| Risco | Tratamento |
|---|---|
| Nome usado por uma função que só existia no escopo do notebook | conferido antes (AST): nenhuma função auxiliar usa nomes definidos no corpo |
| Estado global (`GERA_VARIANTE_A4`, `_FAMILIA_IMPRESSAO`) reatribuído pelo notebook e não visto pelo módulo | conferido: nenhuma seção reatribui nome auxiliar; `_FAMILIA_IMPRESSAO` só é escrito dentro do próprio módulo |
| Import circular | camada `estilo` na base; o grafo de imports é verificado acíclico pelo script de extração |
| Ferramentas que leem `analise.py` estaticamente (`inventario_fontes.py`, `sincroniza_docx.py`) | inventário regenerado e comparado; notas de curadoria continuam nas seções |
| Saída não determinística entre execuções (tiles do mapa de fundo, metadados) | arquivos que diferirem são investigados um a um; se a diferença também aparece entre duas execuções do código antigo, é ruído |
