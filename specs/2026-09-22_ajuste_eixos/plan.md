# Plano técnico — Reorganização por Eixos da Política Municipal

Baseado nas decisões confirmadas em `specs.md` (§3 A-G) e na estrutura de 6
eixos ativos do §4.3/§4.4. Resolve aqui as duas decisões que `specs.md`
deixou em aberto (§9), como **padrão desta rodada, sem objeção do usuário
até agora** — fácil de reverter se o usuário discordar na revisão deste
plano:

- **§9.1 (reordenar `analise.py` fisicamente vs. marcação leve)**: escolhida
  a opção **(b)** — manter a ordem técnica atual das células (respeitando
  as dependências de dado entre seções) e reorganizar só a **apresentação**
  (HTML/PDF/DOCX) via `specs/estrutura_eixos.md`. Motivo: mover ~2500 linhas
  de célula por eixo é o maior risco identificado no spec, para um ganho
  que a apresentação reorganizada já entrega (ver Bloco 2 para o que
  "reorganizar analise.py" passa a significar concretamente).
- **§9.2 (local de `specs/estrutura_eixos.md`)**: confirmado na raiz de
  `specs/`, ao lado de `roadmap.md`/`tech-stack.md`.

## Ordem de execução

Bloco 1 (crosswalk + `estrutura_eixos.md`) é pré-requisito de tudo que
segue — nenhum gerador pode reorganizar nada sem essa fonte de verdade.
Blocos 2 e 3-4 podem correr em paralelo depois disso; Bloco 5 (DOCX) depende
do Bloco 3 (mesma fonte de imagens/textos); Blocos 6-7 (skills) só fazem
sentido depois que os geradores dos Blocos 3-5 existem de verdade (um skill
não é escrito antes do script que ele invoca).

```
Bloco 1 → Bloco 2 ─┐
        → Bloco 3 ─┼→ Bloco 5 → Bloco 6 → Bloco 7 → Bloco 8 → Bloco 9 → Bloco 10
        → Bloco 4 ─┘
```

## Bloco 1 — Crosswalk completo + `specs/estrutura_eixos.md`

Script novo, ad-hoc (roda uma vez para gerar o arquivo, que depois vira
editável à mão — não é reexecutado automaticamente): lê o catálogo, aplica
as regras de bucket (`specs.md` §4.1) e descarte (§4.4), e cruza cada
indicador sobrevivente com o(s) arquivo(s) reais que já existem em
`visualizacoes/`/`mapas/`/`tabelas_finais/`.

```python
# scripts/gera_estrutura_eixos.py (local definitivo a decidir no Bloco 1 —
# candidato: dentro de .claude/skills/export_pdf_report/scripts/, junto dos
# outros geradores, já que vira parte do mesmo pipeline de reestruturação)

import pandas as pd, re
from pathlib import Path

BUCKETS_ORDEM = ["Prioridade (sem secundário)", "Inclusão", "Família e Cuidados",
                 "Proteção", "Alimentação", "Moradia"]

DESCARTE = { ... }  # as 18 strings exatas de specs.md §4.4, para excluir do crosswalk

def carrega_catalogo():
    df = pd.read_excel("dados_locais/painel_primeira_infancia_cesta_indicadores.xlsx",
                        sheet_name="Indicadores")
    df["bucket"] = df.apply(classifica_bucket, axis=1)   # regra §4.1
    df = df[~df["Indicador"].apply(eh_descartado)]        # regra §4.4
    df["implementado"] = df["Status"].apply(comeca_com_ok)  # regra §4.2 corrigida
    return df

def casa_com_arquivos(indicador_texto, catalogos_de_arquivo):
    """Faz o casamento indicador -> arquivo(s) reais. Primeira tentativa:
    correspondência por palavra-chave (nome do indicador normalizado vs.
    nome de arquivo em visualizacoes/mapas/tabelas_finais, já convencionado
    por specs/tech-stack.md). Indicadores sem casamento claro (a maioria dos
    cortes granulares -- por CAP, por subgrupo CID-10, por faixa etária --
    que o catálogo não lista um a um) exigem revisão manual linha por linha,
    usando o exemplo do Bloco "Alimentação" (specs.md §4.5) como método."""
    ...
```

- **Isto não é um matching 100% automático** — o catálogo tem 47 indicadores
  ativos, mas `analise.py` produz ~130 visualizações/mapas reais (muitos
  cortes granulares — por CAP, por subgrupo CID-10, por faixa etária — que
  o catálogo não desdobra um a um). O script resolve o que der por
  correspondência de texto; o resto é preenchido manualmente linha por
  linha, seguindo o método do exemplo "Alimentação" já resolvido em
  `specs.md` §4.5 (repetir para os outros 5 eixos ativos: Prioridade,
  Inclusão, Família e Cuidados, Proteção, Moradia).
- Saída: `specs/estrutura_eixos.md`, no formato definido em `specs.md`
  §5.1 (heading `##` por eixo, `###` por subseção, lista com chaves fixas
  `fonte`/`visualização`/`mapa`/`tabela`). Indicadores "a reservar" (16, do
  §4.3) entram com uma chave extra `status: pendente` (ver Bloco 3 para o
  que essa chave dispara na renderização):

```markdown
## 🛡️ Proteção

### Violência territorial
- fonte: ISP
- status: pendente
- nota: dado catalogado, ainda não importado para `analise.py` (ver `specs/roadmap.md`, "Educação e Violência")
```

- Parser do `.md` (reaproveitado pelos Blocos 3/4/5 — escrito uma vez, não
  reimplementado por gerador):

```python
def parse_estrutura_eixos(caminho="specs/estrutura_eixos.md"):
    """Retorna list[{"eixo": str, "subsecoes": list[{"titulo": str, "campos": dict}]}]
    Regra de parsing: heading ## = novo eixo; heading ### = nova subseção
    dentro do eixo atual; linha "- chave: valor" = campo da subseção atual.
    Sem YAML/front matter -- só Markdown puro, para o usuário editar à mão
    sem quebrar o parser (chave antes de ':' é tudo que importa)."""
    ...

def valida_estrutura(estrutura):
    """Confere que todo valor de 'visualização'/'mapa'/'tabela' referenciado
    aponta pra um arquivo que existe de fato em visualizacoes/mapas/
    tabelas_finais -- roda antes de qualquer geração, falha alto (erro
    explícito com o nome do arquivo que sumiu), nunca gera um relatório
    silenciosamente incompleto por causa de uma referência quebrada."""
    ...
```

## Bloco 2 — `analise.py`/`analise.ipynb`: o que "reorganizar" significa aqui

Dado o default (b) do topo deste arquivo, **não há reordenação física de
células**. O que muda de fato em `analise.py`:

1. A seção final "Análise / Relatório" (hoje só stub, 5 subtítulos —
   `CLAUDE.md`/`analise.py` linha ~2516) é **renomeada** para os 6 eixos
   ativos (Prioridade, Inclusão, Família e Cuidados, Proteção, Alimentação,
   Moradia), substituindo os 5 subtítulos antigos (Demografia e População,
   Assistência Social, Educação, Saúde, Proteção) — essa seção continua só
   markdown/notas, sem código, e continua fora do HTML/PDF (convenção já
   documentada em `CLAUDE.md`, não muda).
2. Um bloco de nota markdown novo, logo após a seção "📦 Pacotes e Funções
   Auxiliares", apontando para `specs/estrutura_eixos.md` como a
   organização "oficial" de apresentação — deixa explícito no próprio
   notebook por que a ordem das seções abaixo (por fonte de dado) não bate
   com a ordem do relatório publicado (por eixo de política), em vez de
   deixar essa discrepância implícita.
3. `CLAUDE.md` (seção "`analise.py` structure") ganha uma nota equivalente,
   sem apagar a descrição da ordem técnica atual (que continua verdadeira e
   é a ordem real do arquivo) — só documentando que a apresentação final
   segue outro critério, definido em `specs/estrutura_eixos.md`.
4. `jupytext --sync analise.py` depois de qualquer edição de célula
   markdown, como sempre.

**Fora deste bloco**: nenhuma função de limpeza/wrangling/visualização
muda de posição ou de assinatura — este bloco é só edição de texto
markdown, risco mínimo.

## Bloco 3 — `relatorio/index.html`: agrupamento por eixo

`build_html_report.py` para de iterar as 9 seções hardcoded por fonte de
dado; passa a iterar `parse_estrutura_eixos()` (Bloco 1):

```python
estrutura = parse_estrutura_eixos()
for eixo in estrutura:                       # 6 h2, na ordem de specs.md §4.3
    abre_secao_h2(eixo["eixo"])
    for sub in eixo["subsecoes"]:
        campos = sub["campos"]
        if campos.get("status") == "pendente":
            emite_bloco_pendente(sub["titulo"], campos.get("nota", ""))  # novo
            continue
        # já existente: option_card/viz/tabela_com_texto, só que agora
        # disparado pela leitura do .md em vez de uma chamada hardcoded
        emite_conteudo(campos)
    fecha_secao_h2()
```

- **`emite_bloco_pendente`** (componente novo): mesmo estilo visual do
  bloco "Principais achados" (`--surface-2`, já existente), com um selo
  "🚧 Indicador catalogado, ainda não disponível" + a `nota` do `.md` — não
  é uma seção vazia sem explicação (decisão E do spec), nem finge ter dado
  que não existe.
- Faixa de texto por visualização ajustada de 150 para **100-200 palavras**
  (`specs.md` §7) — `_lorem(seed, palavras=random.Random(seed).randint(100,200))`
  ou um valor fixo no meio da faixa (150 continua sendo um valor válido
  dentro dela); decidir no Bloco 3 qual dos dois é mais simples de manter
  determinístico entre gerações.
- Cards com seletor de opções continuam com 1 texto por opção (já é o
  comportamento, `specs.md` §7 só confirma que nada muda aqui).
- Navbar/sumário passa a listar as 6 seções por eixo (era 9 por fonte de
  dado) — mesmo componente, fonte de dado diferente.

## Bloco 4 — PDF (`build_notebook_report.py`)

Mesma mudança de fonte de agrupamento (`parse_estrutura_eixos()` em vez da
ordem hardcoded que hoje espelha `analise.py` seção a seção). Diferença
real do HTML: pills viram subtítulos sequenciais (sem interatividade, já é
como o PDF trata opções hoje onde existem) e `emite_bloco_pendente` vira um
parágrafo com o mesmo selo, sem CSS de destaque (PDF é impresso, sem cor de
fundo `--surface-2` — usar borda/itálico como equivalente impresso).

## Bloco 5 — DOCX de curadoria (`relatorio/curadoria_textos.docx`)

Script novo (`gera_docx_curadoria.py`, mesma pasta de skill), usando
`python-docx` (adicionar a `requirements.txt`):

```python
from docx import Document
from docx.shared import Inches

def gera_docx(estrutura, caminho_saida="relatorio/curadoria_textos.docx"):
    doc = Document()
    for eixo in estrutura:
        doc.add_heading(eixo["eixo"], level=1)
        for sub in eixo["subsecoes"]:
            doc.add_heading(sub["titulo"], level=2)
            campos = sub["campos"]
            if campos.get("status") == "pendente":
                doc.add_paragraph(f'[PENDENTE] {campos.get("nota","")}', style="Intense Quote")
                continue
            for opcao in sub.get("opcoes", [_opcao_unica(campos)]):
                if opcao.get("label"):
                    doc.add_heading(opcao["label"], level=3)  # 1 heading por opção do seletor
                if opcao.get("imagem"):
                    doc.add_picture(opcao["imagem"], width=Inches(5.5))  # PNG real, não SVG
                doc.add_paragraph(texto_atual(eixo, sub, opcao))  # ver ID estável abaixo
    doc.save(caminho_saida)
```

- **Imagens**: DOCX usa os PNGs reais de `visualizacoes/`/`mapas/` (mesma
  fonte do PDF), não o motor SVG do HTML — não existe `mapa_svg()` fora do
  navegador.
- **Múltiplas opções no mesmo bloco → 1 heading + 1 bloco de texto por
  opção**, em sequência no documento (Word não tem alternância
  interativa) — atende `specs.md` §1 item 9 diretamente.

### 5.1 ID estável por bloco (pré-requisito do Bloco 7, decidido aqui)

```python
def id_bloco(eixo_titulo, subsecao_titulo, opcao_label=None):
    """ID estável = nome do arquivo de imagem/tabela já único no projeto
    (specs/tech-stack.md já garante isso), com fallback pro título da
    subseção+opção quando não há arquivo (ex.: bloco 'pendente' sem imagem).
    Nunca usa a ORDEM/posição no documento como parte do ID -- é exatamente
    o que quebraria ao mover uma visualização de eixo (specs.md §5.2)."""
    return campos.get("visualização") or campos.get("mapa") or campos.get("tabela") \
        or f"{eixo_titulo}::{subsecao_titulo}::{opcao_label or ''}"
```

Cada parágrafo de texto no DOCX carrega esse ID como um **bookmark**
invisível (`docx.oxml`, `w:bookmarkStart`/`w:bookmarkEnd` — recurso nativo
do formato, não visível ao usuário editando no Word) — é o que permite o
Bloco 7 encontrar "qual texto é este" depois que o usuário reordenou/editou
o documento livremente.

### 5.2 Regeneração não-destrutiva

```python
def gera_docx(estrutura, caminho_saida, docx_anterior=None):
    textos_curados = {}
    if docx_anterior and Path(docx_anterior).exists():
        textos_curados = extrai_textos_por_bookmark(docx_anterior)  # {id_bloco: texto}
    ...
    for opcao in ...:
        id_ = id_bloco(...)
        texto = textos_curados.get(id_) or _lorem(id_)  # preserva o que já foi editado
        _paragrafo_com_bookmark(doc, id_, texto)
```

- Roda sobre o próprio arquivo existente como `docx_anterior` (regenerar
  "por cima" de si mesmo) — texto lorem ipsum nunca sobrescreve texto já
  editado; só blocos genuinamente novos (ID nunca visto antes) recebem
  lorem ipsum.
- Bloco cujo ID desapareceu da nova `estrutura` (visualização removida/
  descartada) — o texto curado correspondente é **preservado num apêndice
  "Textos órfãos"** ao final do documento, não descartado silenciosamente
  (pode ter sido um descarte por engano, ou o texto servir em outro lugar).

## Bloco 6 — Skill de reestruturação

Estende `.claude/skills/export_pdf_report/` (já concentra os geradores de
relatório) em vez de criar um skill novo do zero — mesma pasta, scripts
novos (`gera_estrutura_eixos.py` do Bloco 1, `gera_docx_curadoria.py` do
Bloco 5), e os dois scripts existentes (`build_html_report.py`,
`build_notebook_report.py`) editados para ler `parse_estrutura_eixos()`.

Pipeline do skill, versão atualizada do `SKILL.md`:

1. `python .claude/skills/export_pdf_report/scripts/regen_missing_pngs.py`
   (já existe, sem mudança).
2. Validar `specs/estrutura_eixos.md` contra os arquivos reais
   (`valida_estrutura`, Bloco 1) — falha aqui pára o pipeline com um erro
   claro, em vez de gerar um relatório com um link quebrado.
3. `build_html_report.py` → `relatorio/index.html`.
4. `build_notebook_report.py` → PDF (pipeline Chrome headless já existente,
   sem mudança de motor).
5. `gera_docx_curadoria.py` → `relatorio/curadoria_textos.docx` (passando o
   arquivo anterior, se existir, para a regeneração não-destrutiva do
   Bloco 5.2).

## Bloco 7 — Skill de sincronização do DOCX

Skill novo (ou uma segunda "receita" dentro do mesmo `export_pdf_report/`
— decidir nome final no Bloco 7 conforme o tamanho real do código):

```python
def sincroniza_docx(caminho_docx="relatorio/curadoria_textos.docx"):
    textos = extrai_textos_por_bookmark(caminho_docx)   # {id_bloco: texto}
    for id_, texto in textos.items():
        if eh_lorem_ipsum(texto):      # heurística simples: hash contra o lorem
            continue                    # não foi editado, nada a propagar
        escreve_texto_no_html(id_, texto)      # rebuild pontual do bloco correspondente
        escreve_texto_no_pdf_source(id_, texto)
        # notebook: texto final vira uma nota markdown na subseção
        # correspondente de analise.py, localizada pelo mesmo id_ (nome de
        # arquivo) -- não sobrescreve nenhuma célula de código
```

- `eh_lorem_ipsum`: já que `_lorem(seed, ...)` é determinístico (Bloco 5.2
  do plan de `relatorio-interativo`, reaproveitado aqui), basta comparar o
  texto atual contra `_lorem(id_)` gerado on-the-fly — igual = "ainda não
  editado", diferente = "usuário escreveu texto real, propagar".
- Escrever no notebook (`analise.py`) é o único ponto deste bloco que toca
  o arquivo fonte de verdade do projeto — inserir a nota markdown na
  subseção certa exige localizar o cabeçalho markdown correspondente ao
  `id_` (nome de arquivo já aparece como comentário/variável perto de cada
  `nome_arquivo=` na célula de código, ponto de ancoragem já existente,
  sem precisar inventar um novo).

## Bloco 8 — Documentação

- `requirements.txt`: `python-docx` adicionado.
- `CLAUDE.md`: nota do Bloco 2 item 3.
- `specs/roadmap.md`: item 3 ("Reorganizar a estrutura do relatório...")
  marcado concluído, apontando para este spec.
- `specs/tech-stack.md`: entrada nova descrevendo `python-docx`/DOCX no
  inventário de stack (seção "Exportação em PDF" vira "Exportação em
  PDF/DOCX", ou seção própria).
- `relatorio/specs.md`: nova entrada de versão do HTML descrevendo a
  reorganização por eixo (mesmo padrão histórico do arquivo).

## Bloco 9 — Geração completa e validação

Ver `validation.md` para os critérios objetivos por bloco. Ordem de
execução da validação: Bloco 1 (estrutura + crosswalk revisado) → Bloco 2
(notebook reexecutado do zero) → Blocos 3-5 (os 3 artefatos de saída,
gerados a partir da mesma `estrutura_eixos.md`) → Blocos 6-7 (skills
exercidos de ponta a ponta: editar o `.md`, pedir atualização, editar o
DOCX, pedir sincronização) → Bloco 8 (checagem de documentação).

## Bloco 10 — Fechamento

Merge em `staging_main` só após aval explícito do usuário, como de
costume — não implica em nenhuma ação além do já estabelecido em
`specs/constitution.md` §7.
