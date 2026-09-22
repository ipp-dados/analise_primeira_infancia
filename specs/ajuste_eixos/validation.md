# Validation — specs/ajuste_eixos

Critérios objetivos por bloco. Um bloco só é marcado `[x]` em `tasks.md`
depois de passar aqui. Nenhum resultado preenchido ainda — este arquivo é
escrito antes da implementação, junto com `plan.md`/`tasks.md`.

## V1 — Crosswalk e `specs/estrutura_eixos.md`
- `specs/estrutura_eixos.md` existe, com exatamente 6 headings `##` (eixos
  ativos, na ordem de `specs.md` §4.3: Prioridade, Inclusão, Família e
  Cuidados, Proteção, Alimentação, Moradia).
- Contagem de subseções (`###`) por eixo bate com o total ativo de
  `specs.md` §4.3 (15/10/7/5/6/4 = 47).
- `valida_estrutura()` roda sem apontar nenhuma referência quebrada (todo
  `visualização`/`mapa`/`tabela` citado existe de fato em
  `visualizacoes/`/`mapas/`/`tabelas_finais/`).
- Todos os 16 indicadores "a reservar" (`specs.md` §4.3) têm
  `status: pendente` + `nota` não-vazia.
- Nenhum dos 18 indicadores descartados (`specs.md` §4.4) aparece em
  `estrutura_eixos.md`, em nenhum eixo.
- "Territórios com risco a inundação" aparece **uma única vez**, em
  Moradia (não duplicado, não também em Proteção).

## V2 — `analise.py`/`analise.ipynb`
- Seção final "Análise / Relatório" tem exatamente 6 subtítulos, nomeados
  igual aos 6 eixos ativos (não mais os 5 antigos por fonte de dado).
- Nota apontando para `specs/estrutura_eixos.md` presente logo após
  "📦 Pacotes e Funções Auxiliares".
- `git diff analise.py` mostra **só mudanças de markdown** — nenhuma célula
  de código (`# %%` sem `[markdown]`) alterada, nenhuma célula movida de
  posição.
- `jupyter nbconvert --to notebook --execute --inplace` a partir de kernel
  limpo termina com **0 células com erro**; contagem de células de código
  idêntica à de antes deste spec (nenhuma célula perdida/duplicada).
- `jupytext --sync analise.py` não reporta divergência entre `.py` e
  `.ipynb` depois de rodado.

## V3 — `relatorio/index.html`
- Exatamente 6 `<h2>`, na ordem dos 6 eixos ativos (confirmar via
  `grep -o '<h2[^>]*>[^<]*'`).
- Nº de blocos "🚧 pendente" no HTML bate com os 16 indicadores "a
  reservar" de V1 (contagem de `emite_bloco_pendente` no código gerado ==
  contagem de `status: pendente` em `estrutura_eixos.md`).
- Nenhuma seção/subseção do catálogo descartado (18 indicadores) aparece no
  HTML gerado.
- Abre sem erro de console (Edge/Chrome headless, `--dump-dom
  --enable-logging=stderr`, sem exceção de JavaScript da própria página).
- Bloco de texto de análise: amostra de 5 blocos, contagem de palavras
  entre 100 e 200 em todos.
- Navbar lista as 6 seções (não 9).

## V4 — PDF
- `pypdf` reporta contagem de páginas coerente com 6 seções + 16 blocos
  pendentes (não comparável 1:1 com a versão anterior por fonte de dado,
  mas sem queda abrupta que sugira conteúdo perdido).
- Amostra rasterizada (capa, 1 seção com conteúdo real — Alimentação —, 1
  seção majoritariamente pendente — Proteção ou Moradia —, última página)
  inspecionada visualmente: selo de pendente legível, nenhuma
  imagem/gráfico quebrado.
- Gerado a partir da mesma `estrutura_eixos.md` final que o HTML (mesma
  execução do skill, não duas rodadas divergentes).

## V5 — DOCX de curadoria
- `relatorio/curadoria_textos.docx` existe, abre no Word (ou LibreOffice)
  sem erro de formato corrompido.
- Contagem de headings nível 1 (eixo) = 6; nível 2 (subseção) = 47 (ativos)
  + pendentes com seu próprio heading também.
- Toda visualização/mapa do catálogo ativo tem pelo menos 1 imagem PNG
  embutida no documento (não um placeholder de imagem quebrada).
- Bookmarks presentes: extrair `word/document.xml` do `.docx` (é um zip) e
  confirmar `<w:bookmarkStart>` em contagem igual à de blocos de texto.
- **Teste de não-destrutividade** (`tasks.md` T5.5): editar 1 texto à mão,
  regenerar, texto editado sobrevive — comparar antes/depois byte a byte
  no parágrafo daquele bookmark específico.
- **Teste de órfão** (`tasks.md` T5.6): remover 1 indicador com texto já
  editado da estrutura, regenerar, texto aparece no apêndice "Textos
  órfãos" em vez de desaparecer.
- Bloco com seletor de opções no HTML (ex. algum indicador com múltiplos
  cortes) aparece no DOCX como múltiplos headings nível 3 + texto próprio
  cada, em sequência — não como 1 heading só com o texto da 1ª opção.

## V6 — Skills (Blocos 6-7)
- Pipeline do Bloco 6 roda de ponta a ponta (5 passos) sem intervenção
  manual entre eles, a partir de um estado limpo.
- **Teste do fluxo real do usuário** (`specs.md` §5.2, `tasks.md` T6.3):
  mover 1 indicador de eixo em `estrutura_eixos.md` à mão, pedir a
  atualização em linguagem natural, confirmar que HTML/PDF/DOCX
  regenerados refletem a mudança (a visualização aparece no novo eixo, não
  mais no antigo, nos 3 artefatos).
- **Teste de sincronização do DOCX** (`tasks.md` T7.4): editar 1 bloco de
  texto no DOCX, pedir sincronização em linguagem natural, confirmar que
  (a) o HTML regenerado mostra o texto novo no bloco certo, (b) o PDF
  idem, (c) `analise.py` ganha a nota markdown correspondente na subseção
  certa, (d) nenhum outro bloco (ainda lorem ipsum) foi alterado nos 3
  artefatos.

## V7 — Documentação
- `requirements.txt` lista `python-docx`.
- `CLAUDE.md` reflete a nota do Bloco 2 (organização de apresentação vs.
  ordem técnica do arquivo).
- `specs/roadmap.md` item 3 marcado concluído.
- `specs/tech-stack.md` documenta a dependência/pipeline de DOCX.
- `relatorio/specs.md` tem uma entrada nova de versão para esta
  reorganização.

## V8 — Consistência entre os 3 artefatos de saída
- HTML, PDF e DOCX gerados na mesma execução do skill (mesmo timestamp de
  `estrutura_eixos.md` usado pelos 3) — mesma contagem de eixos (6), mesma
  contagem de indicadores pendentes destacados (16), mesmos 47 indicadores
  ativos presentes nos 3.
- Nenhum dos 3 artefatos referencia qualquer um dos 18 indicadores
  descartados.

## Resultado final
*(preencher ao concluir a implementação — não preenchido nesta rodada de
planejamento)*
