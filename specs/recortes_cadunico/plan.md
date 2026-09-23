# Plano técnico — Novos recortes do CadÚnico

Baseado em `specification.md` (rascunho 2). IDs R1-R3 (recortes), S1-S9 (achados), A1-A8 (correções),
D1-D8 (decisões) e F1-F3 (pendências) são os da spec. **Nada aqui é executado antes da aprovação do
plano.**

Defaults assumidos, **ainda sem resposta do usuário** e fáceis de reverter na revisão: D6 (mapa %
CadÚnico/Censo sai do HTML/PDF), D7 ("0 a 5 anos" só em textos), D8 (renomear o CSV de renda).

## Princípios

- **Recortes novos só acrescentam.** As alterações em código existente ficam restritas às correções
  A1-A8, todas dentro da seção 🗂️ Cadúnico de `analise.py`, do bloco CadÚnico de
  `build_html_report.py` (~1250-1298) e de `build_notebook_report.py` (~500-580), e do leitor em
  `regen_missing_pngs.py:81`.
- **Privacidade antes de gravar.** Toda tabela sub-municipal passa por `suprime_celulas_pequenas`
  *antes* de `to_csv`. O DataFrame sem supressão só existe em memória. Nada de nível pessoa ou
  família é gravado (spec §5).
- **Somar antes de dividir.** Taxas por bairro são recalculadas de numerador e denominador absolutos.
  A supressão acontece depois do cálculo e não entra em nenhuma agregação.

## Descobertas que moldam o plano (verificadas na abertura)

1. **O kernel tem que ser `analises_env`.** No Python base falta `psycopg` 3. Todo run de validação
   usa `C:\Users\13073625755\.conda\envs\analises_env\python.exe` (ou o kernel Jupyter
   correspondente), sempre com cwd na raiz do repo, para o `load_dotenv()` achar o `.env`.
2. **O HTML tem os 3 itens hard-coded como pendentes** (`build_html_report.py:1252-1254`), e o PDF
   também (`build_notebook_report.py:502-504`). Eles ficam no eixo **Inclusão**. As saídas CadÚnico
   existentes estão em **Família e Cuidados** (HTML ~1262). Os cards novos entram no lugar dos
   pendentes, **no eixo Inclusão**, e não junto das saídas antigas.
3. **O HTML monta os mapas SVG a partir das gêmeas `tabela_mapa_*.csv`** (`mapa_svg`) e mostra o
   valor exato no tooltip e no "⭳ CSV". A supressão, portanto, tem que estar na gêmea. Para uma
   célula suprimida, `mapa_svg` recebe `NaN` e hoje rotula como "Sem dado". **É preciso distinguir
   "suprimido (< 20)" de "sem dado"**: nova opção `rotulo_nan` em `mapa_svg`, com default igual ao
   comportamento atual. No PNG (`mapa_coropletico_bairros`), a nota vai em `nota_rodape`/`fonte_dados`,
   sem mudar a função.
4. **O custo de consulta é baixo.** O `SELECT` das famílias com criança devolve ~600-700 mil linhas
   (173.768 famílias × ~3,5 membros), em segundos a poucos minutos. Não precisa de cache em disco, e
   por privacidade não se faz cache.
5. **Ponto de inserção em `analise.py`**: depois da célula dos mapas CadÚnico (~linha 1368) e antes
   de "🏥 DataSus - tabnet". `df_censo`, `df` (com `bairro`) e os aliases de bairro já estão definidos
   nesse ponto.
6. **O join CEP→bairro existente é reaproveitado sem mudar a lógica** (F1 fica fora). A1 só torna
   visível o que ele perde.

## Ordem de execução

```
Bloco 0 (aprovação D6-D8) → Bloco 1 (ambiente + baseline) → Bloco 2 (funções)
  → Bloco 3 (correções A1-A8 nas saídas existentes) → Bloco 4 (R1 sexo) → Bloco 5 (R2 raça/cor)
  → Bloco 6 (R3 arranjo × renda) → Bloco 7 (mapas por bairro) → Bloco 8 (estrutura_eixos.md)
  → Bloco 9 (HTML) ┐
    Bloco 10 (PDF) ├→ Bloco 11 (docs) → Bloco 12 (validação completa + revisão visual)
    Bloco 10b (DOCX)┘
```

Um commit por bloco, com mensagem `recortes_cadunico Bloco N: …`. Deploy no Pages **não** faz parte
desta rodada: é manual e vem depois do ok do usuário.

## Bloco 0 — Aprovação
- O usuário lê `plan.md`, `tasks.md` e `validation.md`.
- Confirmar ou alterar D6, D7 e D8.

## Bloco 1 — Ambiente e baseline (V0)
- Confirmar o kernel `analises_env` (`import psycopg; psycopg.__version__ == '3.3.4'`) e registrar a
  instrução em `README.md`/`CLAUDE.md` no Bloco 11.
- Gravar checksums SHA-256 de `tabelas_finais/`, `visualizacoes/`, `mapas/`, `relatorio/index.html`,
  PDF e DOCX no scratchpad.
- Rodar só a seção CadÚnico (célula de setup, Censo e CadÚnico) e conferir que as 6 tabelas
  `cadunico_*` atuais saem **idênticas** às versionadas. Assim se confirma que a partição do banco
  (2026-06-12) é a mesma que gerou os arquivos. Se não bater, parar e reportar: os números da spec
  §2.3 mudam.

## Bloco 2 — Funções novas (seção 📦, topo de `analise.py`)
Cada função leva docstring em pt-BR explicando o porquê, como as vizinhas.
- `_ROTULOS_RENDA_CADUNICO`: dicionário faixa → rótulo descritivo (A7). Mais
  `_ORDEM_RENDA_CADUNICO` e o agrupamento 3 faixas (`0-218`, `219-810`, `811+`) para os cruzamentos.
- `carrega_cadunico_familias_0_6(engine)`: um único `SELECT` com
  `WHERE id_familia IN (SELECT id_familia FROM ctpe.silver_cadunico_geral WHERE grupo_idade='0-6')`
  e só as colunas necessárias (`id_pessoa`, `id_familia`, `idade`, `sexo`, `raca_cor`,
  `grupo_renda_pct`, `n_pessoas_familia`, `cep`).
- `classifica_arranjo_familiar(df_membros, idade_adulto=18)`: uma linha por família, com
  `n_adultos`, `n_adultas`, `n_criancas_0_5`, `arranjo` (6 categorias da spec §3 R3),
  `grupo_renda_pct` e `composicao_sexo_criancas` (só meninas / só meninos / meninas e meninos).
  Asserções: renda única por família, linhas por família = `n_pessoas_familia`.
- `agrega_cadunico_por_categoria(df, coluna)`: crianças (`count`) e famílias (`nunique`), sem linha
  de total quando as categorias não são exclusivas (parâmetro `exclusivas`).
- `suprime_celulas_pequenas(df, coluna_denominador, colunas, limiar=20)`: devolve uma cópia com
  `colunas` = `NaN` onde denominador < limiar, mais a coluna `suprimido` (bool). Não mexe no df original.

## Bloco 3 — Correções nas saídas existentes (A1-A8)
Dentro da seção 🗂️ Cadúnico. Cada célula alterada ganha um comentário `# recortes_cadunico A<n>`.
- **A1:** conta `df['bairro'].isna()`, acrescenta a linha "Sem bairro identificado (CEP fora da
  lista)" em `cadunico_por_bairro_2026.csv` e reescreve a nota markdown com os números reais.
- **A2:** reescreve a nota do mapa %, citando a causa (bairro do CEP ≠ bairro IPP) e os bairros
  afetados (S2). Mesma nota curta em todos os mapas CadÚnico. **D6** decide se o mapa sai do HTML/PDF.
- **A3:** títulos e legendas "0-6" → "0 a 5 anos" no notebook (`grafico_barra`, `mapa_coropletico_bairros`),
  no HTML (títulos, rótulos das opções `"Crianças 0-6"`) e no PDF. Nomes de arquivo não mudam (D7).
- **A4:** `suprime_celulas_pequenas` antes do `to_csv` de `cadunico_por_bairro_2026`,
  `cadunico_por_bairro_ate_4_2026`, `tabela_mapa_cadunico_criancas_2026` e
  `tabela_mapa_cadunico_primeira_infancia_2026`. No %: denominador = crianças 0-4 no CadÚnico **ou**
  população Censo 0-4 < 20.
- **A5 (D8):** `to_csv('tabelas_finais/cadunico_por_faixa_renda_2026.csv')`, 4 leitores atualizados
  e `git rm` do nome antigo.
- **A6:** notas de "famílias por idade não somam" e do sub-registro no 1º ano.
- **A7:** gráficos de renda com `_ROTULOS_RENDA_CADUNICO`.
- **A8:** nota sobre o filtro de cadastro desconhecido (F3).
- Todas as chamadas corrigidas passam a citar `fonte_cadunico_particao` (D5).

## Bloco 4 — R1 sexo
- `df_familias = classifica_arranjo_familiar(carrega_cadunico_familias_0_6(engine))`, carregado uma
  vez e reusado nos Blocos 4-7.
- `cadunico_por_sexo_2026.csv`: bloco "crianças por sexo" + bloco "famílias por composição de sexo
  das crianças" (exclusivas, Σ = 173.768).
- Gráficos: `cadunico_criancas_por_sexo.png` e `cadunico_familias_por_sexo_criancas.png` (`grafico_barra`).

## Bloco 5 — R2 raça/cor
- `cadunico_por_raca_cor_2026.csv`: crianças por raça/cor (5 + "Negra (preta + parda)") e famílias
  com ≥1 criança da categoria, com a coluna `nota` = "não exclusivas; não somar".
- Gráficos: `cadunico_criancas_por_raca_cor.png` e `cadunico_familias_por_raca_cor.png`. O título do
  segundo diz "famílias com ao menos uma criança…".

## Bloco 6 — R3 arranjo × renda
- `cadunico_familias_por_arranjo_2026.csv`: famílias, crianças e %.
- `cadunico_familias_arranjo_renda_2026.csv`: arranjo × 3 faixas de renda, em contagem e em %
  dentro do arranjo, com a supressão < 20 aplicada.
- Gráficos: `cadunico_familias_por_arranjo.png` (`grafico_barra`) e
  `cadunico_familias_arranjo_renda.png` (`grafico_barra_agrupado`, % dentro do arranjo).
- Célula markdown com a nota metodológica da spec §3 R3 e a inspeção agregada das 713 famílias sem
  adulto (distribuição da idade do membro mais velho).

## Bloco 7 — Mapas por bairro
- Por bairro: crianças, meninas, crianças negras, famílias, famílias "uma adulta". Mesmo alias e
  exclusão de `df_bairro_mapa` e `junta_codbairro_por_bairro(…, df_censo)`.
- Taxas `percentual_meninas`, `percentual_criancas_negras` e `percentual_familias_uma_adulta` (×100),
  depois `suprime_celulas_pequenas`, depois `tabela_mapa_cadunico_recortes_bairro_2026.csv`.
- 3 × `mapa_coropletico_bairros(..., bins=None, cmap=_CORES_TEMA_MAPA['cadunico'], fonte_dados=fonte_cadunico_particao)`,
  com rodapé "Bairros com menos de 20 crianças/famílias suprimidos; bairro atribuído pelo CEP (ver nota)".

## Bloco 8 — `specs/estrutura_eixos.md`
- Trocar `status: pendente` / `nota: Fazer recorte — Léo` das linhas 187-200 por `fonte`,
  `visualização:`, `mapa:`, `tabela:` e `nota:` (proxy de arranjo; famílias não exclusivas).
- Em Família e Cuidados: `cadunico_por_faixa_etaria_2026.csv` → `cadunico_por_faixa_renda_2026.csv`
  (D8). Se D6 for aceita, o mapa % sai da lista.

## Bloco 9 — HTML (`build_html_report.py`)
- Trocar as 3 chamadas `emite_bloco_pendente` (1252-1254) por `option_card`s: R1 (gráfico crianças +
  famílias em `out_pair`, mapa % meninas), R2 (idem + mapa % negras), R3 (arranjo, arranjo × renda,
  mapa % uma adulta). Os textos de nota vêm da spec.
- `mapa_svg`: novo parâmetro opcional `rotulo_nan` para exibir "suprimido (< 20)". O default não
  muda o comportamento dos outros ~30 mapas.
- Bloco CadÚnico de Família e Cuidados: A3 (títulos e rótulos), A5 (leitor), A7 (rótulos de renda),
  D6 (remove a opção "% s/ Censo" do `option_card` de mapas), `FONTE_CADUNICO` com a data da partição.

## Bloco 10 — PDF (`build_notebook_report.py`) e 10b — DOCX
- PDF: trocar os 3 `pending` (502-504) por `chart_block`s e mapas. Aplicar A3, A5, D6 e as notas no
  trecho existente (~515-580).
- DOCX: regenerar com `gera_docx_curadoria.py` (lê o `.md`). Seeds de texto de análise para os
  cards novos seguem o mecanismo `_texto_analise` já existente.
- `regen_missing_pngs.py:81`: leitor renomeado (A5).

## Bloco 11 — Documentação
- `README.md`: changelog de 1-3 linhas (constitution §1).
- `specs/roadmap.md`: item 8 como concluído (1ª leva) e F1-F3 como itens novos de backlog.
- `CLAUDE.md` / `specs/tech-stack.md`: kernel `analises_env` para rodar a seção CadÚnico e a regra
  de supressão < 20 para saídas CadÚnico sub-municipais.
- `specs/constitution.md` §6: o limiar concreto (20) vira regra de projeto. **Pedir ok explícito**
  antes de mexer na constitution.

## Bloco 12 — Validação completa e revisão visual
- Notebook do zero, top-to-bottom, kernel `analises_env` (constitution §2).
- `validation.md` V1-V8 marcados com evidência.
- Revisão visual dos PNG e dos cards HTML. Candidato a corte: o mapa % meninas (baixa variação). A
  decisão fica com o usuário.
