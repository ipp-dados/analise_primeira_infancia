# PLAN — Dados pontuais do CadÚnico: Moradia e Inclusão

Implementa `specification.md` (R1-R7, D1-D4). Branch de implementação: `spec/dados-adhoc`, a partir de `planning`.
Regra geral da rodada (D1): **só acrescentar** — o diff não pode alterar a saída de nenhum item existente.

## 1. Levantamento (2026-09-29)

| Peça | Situação | Impacto |
| :-- | :-- | :-- |
| `specs/estrutura_eixos.md` | Inclusão: 3 itens pendentes (l. 272-290); Moradia: 3 pendentes (l. 479-497) | itens novos depois dos pendentes; parser (`parse_estrutura_eixos`) aceita chave nova sem mudança |
| `website/build/build_site.py` | seções escritas à mão; Inclusão l. 1750-1756 e Moradia l. 2047-2053 só com `emite_bloco_pendente`; já há `bar_chart`, `plain_table`, `tabela_com_texto`, `callout`, `nota_metodologica` | blocos novos depois das chamadas de pendente; helper novo `cartoes_indicador` + callout "Dado pontual" |
| `website/css/components.css`, `mobile.css` | sem componente de cartão de indicador (KPI) | classes novas (`.kpi-grid`, `.kpi`, `.razao`), sem tocar nas existentes |
| `relatorio/latex/build/gera_latex.py` | `secoes_indicadores` trata pendente, figuras, `tabela_no_texto`, `tabela` | ler `- aviso:` e emitir um quadro (ambiente novo em `estilo.sty`, como `pendente`) |
| `relatorio/latex/build/tabelas.py` | `AJUSTES` por arquivo (rótulos, formato) | entradas para as 3 tabelas novas (cabeçalhos legíveis, % com 1 casa) |
| `relatorio/latex/build/inventario_fontes.py` | inventário a partir do crosswalk/arquivos | conferir que a fonte nova aparece (fonte = "Cadastro Único — extração pontual…") |
| `apresentacao/apresentacao.md` + `build/numeros.py` | slide "Eixos incompletos" (Parte III); números por função `numero` | slide novo antes dele; 4-5 funções novas lendo as CSVs de R2 |
| `relatorio/curadoria/` (DOCX) | exporta textos por chave | chaves novas entram como texto a curar (lorem) — conferir que o export não quebra |
| `primeira_infancia/cadunico.py` | funções do CadÚnico (supressão, agregação) | 2 funções novas; `__all__` |
| `analise.py` | seção CadÚnico precisa de `.env` + psycopg | célula nova independente do banco (só lê `dados_locais/cadunico/`) |

## 2. Blocos

**B1 — Dados e funções (R1).** Criar `dados_locais/cadunico/` com a planilha renomeada, `deficiencia_cadunico_2026_08.csv`
e o manifesto `adhoc_2026_08.json` (`is_adhoc`, `ref_date`, `replacement_pending`, `substituicao_prevista: "2026-Q4"`,
`aviso` (texto D4), `nota_faixa` (D1), `notas_qualidade` A1-A3, lista dos arquivos gerados). Em `cadunico.py`:
- `carrega_moradia_cadunico_adhoc(caminho)`: para cada aba, acha a linha de cabeçalho ("Famílias") e a de valores;
  extrai o filtro ("Tem banheiro = Não", "Forma de escoamento sanitário = …") do texto do cabeçalho; normaliza números
  (`'17..149'` → 17149; falha alto se outro texto não numérico aparecer); descarta filtro repetido com valores iguais
  (A2; se repetido com valores **diferentes**, erro); cisterna com 0 crianças e > 0 famílias → `NaN` + flag (A3,
  regra genérica: crianças = 0 com famílias ≥ 500). Devolve formato longo com `indicador`, `tipo`, `categoria`,
  `familias`, `pessoas_total`, `criancas_0_3`, `criancas_4_6`, e `df.attrs` com o manifesto.
- `carrega_deficiencia_cadunico_adhoc(caminho)`: lê o CSV, acrescenta total 0-6 e `% com BPC` (numerador/denominador
  da mesma extração, 1 casa).
- Conferência sintética rápida (como em `specs/2026-09-29_privacidade_cadunico` T1.2): A1-A3 e o erro de duplicata.

**B2 — `analise.py` (R2).** Célula markdown + código ao fim da seção CadÚnico; grava as 3 CSVs; imprime a checagem
(BPC 33,3% e 43,1%). `jupytext --to notebook` só para conferir a sintaxe; rodar a célula isolada (o resto do notebook
não muda — D1; não é preciso reexecutar tudo, ver Riscos).

**B3 — Crosswalk (R3).** Itens novos:
- Inclusão: "Crianças no CadÚnico com deficiência e acesso ao BPC (dado pontual, ago/2026)".
- Moradia: "Famílias e crianças no CadÚnico em domicílios sem banheiro ou sem água canalizada (dado pontual, ago/2026)"
  e "Famílias e crianças no CadÚnico por forma de abastecimento de água e de escoamento sanitário (dado pontual,
  ago/2026)".
Cada um com `fonte`, `tabela_no_texto`, `tabela`, `aviso`, `nota` (interna: origem, D1-D4). Documentar o campo
`- aviso:` no cabeçalho do crosswalk.

**B4 — Site (R4).** `cartoes_indicador(itens)` (número grande + rótulo + detalhe) e `barras_razao(itens)` (proporção
com numerador/denominador escritos — acessível sem cor); callout `adhoc` com o texto do manifesto (ícone já existente,
p.ex. "info"/"calendar"). Inclusão: cartões + barras BPC + contexto famílias/pessoas (D2) + nota da faixa. Moradia:
cartões dos déficits + `plain_table` das formas por faixa (com o "não informado" de A3). Blocos entram **depois** das
chamadas `emite_bloco_pendente` (D3). Mobile: cartões em 2 colunas no tablet, 1 no telefone.

**B5 — PDF (R5).** Ambiente `aviso` em `estilo.sty`; `secoes_indicadores` emite `\begin{aviso}…\end{aviso}` quando o
item tem `- aviso:`; `AJUSTES` das 3 tabelas; conferir inventário de fontes. `python relatorio/latex/build/gera_latex.py`
(sem `--publicar`).

**B6 — Deck (R6).** Slide "Primeiros números de Inclusão e Moradia" (kicker "Parte III · O que falta" ou "Dado pontual"),
antes de "Eixos incompletos": crianças 0-6 com deficiência (25.995) e cobertura BPC (33% / 43%); crianças de 0-6 em
domicílio sem água canalizada (1.425) e com esgoto em vala a céu aberto (2.226); nota do dado pontual + faixa. Números
por `{{n:...}}`. `python apresentacao/build/gera_apresentacao.py` (sem `--publicar`).

**B7 — Registro (R7).** `ROADMAP.md` (rodada atual + item de substituição no 4º tri com a lista de arquivos do
manifesto), `CHANGELOG.md`/`README.md` (1-3 linhas), `docs/especificacao_projeto.md` (§ fontes: extração pontual;
§11), `CLAUDE.md` (pasta `dados_locais/cadunico/` e campo `aviso`), `validation.md`.

## 3. Riscos

- **"Só acrescentar" verificado por diff:** gerar site/PDF/deck **antes** (na base) e **depois**; comparar
  `website/data/charts.js` e as seções HTML fora de Inclusão/Moradia (devem ser idênticos, exceto contadores da Visão
  geral, que passam a contar os itens novos), e screenshots desktop das outras abas (pixel-idênticas).
- **Contadores da Visão geral / "N subseções":** mudam em Inclusão (3 → 4) e Moradia (3 → 5) — consequência aceita do
  acréscimo; o nº de pendentes não muda.
- **Não reexecutar o notebook inteiro** (precisa do banco; D1 proíbe mudar saídas): a célula nova é independente;
  valido rodando só ela. O constitucional "rodar do zero" fica registrado como não feito nesta rodada, com o motivo.
- **Texto lorem nos itens novos** até a curadoria — igual aos demais itens sem texto curado; listado no ROADMAP.
- **Faixa 4-6 anos** (D1): a nota precisa aparecer em todo lugar em que o número sai (site, PDF, deck, CSV não — CSV
  leva o nome da coluna `criancas_4_6`).
