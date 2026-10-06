# PLAN — CadÚnico: pipeline novo para Inclusão e Moradia

## Levantamento do código

- `primeira_infancia/cadunico.py`: carregadores (`carrega_cadunico_familias_0_6`, filtro `'0-6'`), privacidade
  (`agrega_bairros_pequenos`, `tabela_publicada_por_bairro`), dado pontual (`carrega_*_adhoc`). Saídas por bairro usam
  `codbairro` + nome (`bairro`) e as colunas `agregado_em`/`suprimido` lidas pelo site.
- `analise.py`, seção 🗂️ Cadúnico (linhas ~424-944): `df_original` por `grupo_idade='0-6'`; célula de dado pontual no fim.
- `specs/estrutura_eixos.md`: Inclusão (3 pendentes + 1 pontual) e Moradia (3 pendentes + 2 pontuais).
- `website/build/build_site.py`: seções escritas à mão (`h2`/`h3`, `emite_bloco_pendente`, `cartoes_indicador`,
  `bar_chart`, `mapa_svg(..., col_suprimido, col_agregado)`, `tabela_com_texto`, `aviso_dado_pontual`). Lorem automático
  para chave sem texto curado.
- `demo`: `relatorio/publicacao.json` (`lancamento_v1`, `demo_textos`), `website/build/demo.py` (faixa, textos, conferência),
  `website/build/textos_demo.json`, `relatorio/latex/build/demo_pdf.py` (aviso + páginas 1-18).

## Blocos

**B1 — Pacote.** Em `cadunico.py`:
- `carrega_criancas_cadunico_silver(engine)`: uma linha por criança `'0-5'` (pessoas ⨝ famílias ⨝ ponte), só as colunas
  usadas (deficiência, BPC, FJP, adensamento, banheiro, água, `codbairro`). Em memória; nunca gravado.
- `carrega_familias_cadunico_silver(engine)`: famílias com criança `'0-5'` (`familia_com_crianca_0_5='Sim'`), com flag
  "tem criança com deficiência" (subconsulta em pessoas) e `codbairro`.
- `indicador_sim_base(serie)`: (sim, base, %) com "Não informado"/"Não se aplica"/nulo fora da base (D7).
- `tabela_moradia_cadunico(...)`, `tabela_deficiencia_cadunico(...)`, `tabela_tipos_deficiencia(...)`,
  `tabela_componentes_fjp(...)`, `por_bairro_sim_base(df, indicadores)` (contagens por `codbairro` para
  `agrega_bairros_pequenos`, com nome oficial do geojson). Constantes de rótulo/ordem. `__all__`.
- Conferência: totais do município batem com `gold_cadunico_indicadores` (recorte `primeira_infancia`) onde houver.

**B2 — `analise.py`.**
- A1/D5: `'0-6'` → `'0-5'` no `SELECT` de `df_original` e em `carrega_cadunico_familias_0_6`; notas da seção
  atualizadas (grupo `'0-5'`, partição jul/2026, S9 respondida pela bronze).
- Subseção nova "♿🏠 Inclusão e Moradia (silver, jul/2026)" antes da célula de dado pontual: chama B1, grava as CSVs,
  3 gráficos (`grafico_barra`), 3 mapas (`mapa_coropletico_bairros`, `bins=None`, `_CORES_TEMA_MAPA['cadunico']`) e
  as tabelas gêmeas. Célula do dado pontual mantida (D1), com nota de que saiu do site.
- `jupytext --to notebook` e execução completa (`jupyter nbconvert --execute`, kernel `analises_env`, cópia em scratch
  se preciso); variante A4 sai junto.

**B3 — Crosswalk.** Inclusão e Moradia: 6 itens com `visualização/mapa/tabela/tabela_no_texto` (R1-R6), sem `status:
pendente`; itens pontuais removidos (D1); `nota` com a rodada. Título dos itens = catálogo ("até 72 meses" onde couber).

**B4 — Site (`staging_main`).** Em `build_site.py`: Inclusão e Moradia reescritas com os blocos novos (cartões, barras,
mapas com `col_agregado`, tabelas com texto); sai o código dos blocos pontuais dessas abas. Regerar, conferir no
navegador (desktop e celular), tamanho do site, nenhum `data-dado-pontual`.

**B5 — Documentação.** ROADMAP (rodada, cortes §4, A2, D2, deck), `specs/exclusoes.md` (cortes), `docs/especificacao_projeto.md`
(fontes CadÚnico: silver nova e ponte), CHANGELOG/README breve, `CLAUDE.md` se a regra de bairro mudar de texto.
Merge `--no-ff` em `staging_main`.

**B6 — Demo.** `staging_main` → `demo` (merge). Na `demo`: `lancamento_v1 = 2026-10-13`; texto da faixa (próxima
atualização de conteúdo e textos); nota nas abas Inclusão e Moradia via `demo.py` (chave em `demo_textos`); textos
provisórios das chaves novas e números do CadÚnico atualizados em `textos_demo.json`; `build_site.py` (conferência da
demo passa); `demo_pdf.py` para refazer o aviso. Sem push (ROADMAP §00).

## Riscos

- Execução completa do notebook é longa e depende do banco: rodar em segundo plano; erro fora do CadÚnico é reportado,
  não contornado.
- Números novos mudam textos curados de Prioridade/Família (D5): lorem não volta (texto curado tem precedência), mas o
  texto fica desatualizado até a rodada de textos — listado em `validation.md`.
- Mapa de deficiência com ~40% dos bairros em conjuntos (A5): aceito, como nos mapas atuais; se ficar ilegível, cai o
  mapa e fica a tabela (decisão registrada).
- Merge na `demo`: conflitos esperados em `index.html`/`charts.js` gerados — resolver regerando, não à mão.
