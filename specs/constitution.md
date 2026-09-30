# Constitution

Princípios não-negociáveis para trabalhar neste repositório — código,
dados e processo. Convenções de estilo específicas de uma função (paleta de
mapa, posição de legenda etc.) ficam documentadas nas `SKILL.md` e nas specs
de cada rodada, não aqui; isto aqui é o que vale para *qualquer* mudança.

## 1. Idioma e público

- Conteúdo (markdown do notebook, mensagens de commit, texto do relatório,
  este arquivo) é em **pt-BR**. Identificadores de código misturam
  português e inglês (`serie_temporal`, `mapa_coropletico_bairros`,
  `df_censo`) — siga o padrão já usado na vizinhança do código que estiver
  editando, não imponha um idioma único.
- O público final do relatório (`relatorio/`) e do PDF é **não-técnico**
  (gestores, stakeholders da Prefeitura) — título + fonte + dado, sem jargão
  de código nem notas de método do notebook. O notebook (`analise.py`) é o
  único lugar com prosa técnica/metodológica.
- **Changelog breve** (feedback do usuário, 2026-09-22): entradas na "Update
  Table" e em "Notable code changes" do README são 1-3 linhas — o quê e por
  quê, não uma lista exaustiva de sub-itens. Detalhe completo mora na spec
  da rodada (`specs/<AAAA-MM-DD>_<nome>/`), o README só aponta pra lá.

## 2. `analise.py` é a fonte de verdade

- `analise.py` (formato Jupytext `py:percent`) é o artefato versionado.
  `analise.ipynb` é gerado (`jupytext --to notebook`) e está no `.gitignore`
  — nunca edite o `.ipynb` esperando que a mudança persista; edite o `.py` e
  rode `jupytext --sync`.
- Toda função reutilizável de limpeza/wrangling ou de visualização vive no
  pacote **`primeira_infancia/`** (um módulo por tema), importado na seção
  **📦 Pacotes e Funções Auxiliares** no topo do arquivo. Seções de análise
  só **chamam** essas funções — não redefinem lógica de limpeza ou de plot
  inline numa célula de análise. (Até 2026-09-28 as funções ficavam no próprio
  `analise.py`; mudança aprovada pelo usuário em `specs/2026-09-28_organizacao`.)
- Rode o notebook do zero (kernel limpo, top-to-bottom) antes de considerar
  uma mudança validada — já houve bug real (`specs/2026-09-09_maps-and-ibge`) que só
  aparecia fora de uma reexecução de células fora de ordem.

## 3. Convenções de dados que não têm exceção

- **Join por bairro é sempre pelo código numérico** (`codbairro`/`codigo`),
  nunca pelo nome do bairro em string — grafias divergem entre fontes. Ver
  `.claude/skills/generate_map/SKILL.md` para o único caminho documentado de
  fallback por nome.
- **Nunca agregar uma coluna de percentual/taxa por soma ou média direta.**
  Some primeiro os absolutos (numerador e denominador), depois recalcule a
  taxa. (`agrega_bairros_por_nivel` existe exatamente para isso.)
- **Mapas coropléticos:** contagem absoluta sempre em classes discretas
  (`bins`), percentual/taxa sempre em escala contínua (colorbar). Cada nível
  de agregação (bairro/AP/RP/CAP) tem seus próprios `bins` — nunca reaproveitar
  os de outro nível.
- **`ap`** (Área de Planejamento, IPP, 5 regiões) e **`cap`** (Coordenadoria
  de Área Programática de Saúde, SMS-Rio, 10 regiões) são divisões
  administrativas diferentes com códigos de formato parecido — não confundir.
- Toda visualização/mapa cita sua fonte (`fonte_dados` ou equivalente). Não
  adicionar um call site novo sem isso.
- **População de referência por nível** (`specs/2026-09-24_populacao-referencia`, 2026-09-24): taxa **municipal**
  usa as estimativas Ripsa/MS do mesmo ano (`populacao_ripsa`); taxa **sub-municipal** (bairro, AP, RP,
  RA, CAP) usa o Censo 2022, fixo, e diz isso na fonte ou na legenda. Nunca comparar uma com a outra
  sem dizer (o Censo 2022 subconta crianças pequenas). A faixa etária do rótulo é a faixa real do dado
  (`specs/2026-09-24_populacao-referencia/auditoria_faixas.md`), não a do catálogo.
- **Faixa etária padrão: 0 a 5 anos (até 72 meses)** (regra do usuário, 2026-09-29, `specs/2026-09-29_pendencias` D9).
  Toda saída publicada (site, PDF, DOCX, apresentação) trabalha com 0 a 5 anos completos; se uma fonte traz 6 anos,
  eles ficam fora dos gráficos e dos números citados. Quando os 6 anos forem mesmo necessários, **com nota explícita**.
  Títulos do crosswalk que vêm do catálogo ("até 6 anos") dizem "até 72 meses", com o nome do catálogo na `nota` (D18).
  Onde a fonte só tem outra faixa (Censo 2022 por bairro: 0 a 4 anos), o rótulo diz a faixa real.
- **Base zero nos gráficos de taxa/percentual** (decisão P1, `specs/2026-09-25_website_graficos`), com **uma exceção**:
  o percentual de baixo peso ao nascer, de eixo cortado, com a marca de corte desenhada e "eixo não começa em zero"
  na fonte (`specs/2026-09-29_pendencias` D3/D12; `serie_temporal(base_zero=False)`, `eixoCortado` no site). Outra
  exceção só com decisão do usuário.
- **Agregar taxas publicadas** (quando não há numerador e denominador da mesma base): somar taxa × população e dividir
  pela soma da população — nunca média simples. Não dividir contagens de tabelas de bases diferentes (ex.: SIDRA
  10057 ÷ 9606 passa de 100%; `specs/2026-09-29_pendencias` D14).
- **Dado pontual nunca vai para o relatório nem para a versão final do site** (regra do usuário, 2026-09-29,
  `specs/2026-09-29_dados_adhoc` D7). Item com `- dado_pontual:` no crosswalk (extração fora da rotina, ex. CadÚnico
  ago/2026) aparece **só no site em desenvolvimento**: o gerador do PDF o descarta (`sem_dados_pontuais`), a fonte
  dele não entra na lista Fontes (`so_site = {sim}` no `fontes.bib`), e ele é um **bloqueio** da versão final do
  site — com `em_desenvolvimento = false` em `relatorio/publicacao.json`, `build_site.py` para, e o deploy falha se o
  HTML tiver `data-dado-pontual` sem a faixa. Para tirar a faixa, antes substitua o dado pontual pela extração
  automatizada ou retire os blocos (`ROADMAP.md`). Não contornar sem decisão do usuário.
- `dados_locais/` **não é gitignorado** — arquivos colocados ali (inclusive
  camadas geo) são versionados. Confirme com `git status` antes de assumir o
  contrário; não versione dado bruto sensível sem checar antes se deveria
  (ver §6, Privacidade).
- `dados_locais/` é organizado **por tema, uma pasta por fonte, nome em
  snake_case sem espaço/acentuação maiúscula** (`censo/`, `mortalidade/`,
  `sisvan/`, `ibge_sidra/`, `vacinacao/`, `nascidos_vivos/`, `geo/`,
  `tratados/`, `populacao/`, `educacao/`, `protecao/`). Não duplicar o mesmo arquivo em duas pastas temáticas — se um
  dado serve duas seções de análise, ele mora numa pasta só e as duas seções
  leem de lá. `tabelas_finais/`/`visualizacoes/`/`mapas/` seguem uma
  convenção de nome própria — ver `specs/tech-stack.md` (proposta em
  `specs/2026-09-22_reorganize-naming/` até ser aprovada e aplicada).
- ⚠️ **Achado 2026-09-22, ainda não corrigido**: `.gitignore` tem as regras
  de `mapas/`, `tabelas_finais/` e `visualizacoes/*.png` comentadas (`#` no
  início da linha) — na prática essas pastas **estão sendo versionadas**,
  contradizendo a descrição de "artefato gerado" do §4 abaixo. Não rode uma
  regeneração completa nem apague esses arquivos achando que são
  recuperáveis via regeneração até isso ser decidido — confirme com o
  usuário antes.
  **Atualização 2026-09-23 (`specs/2026-09-23_recortes_cadunico`):** o achado acima
  não vale mais. As regras foram reativadas em 2026-09-22 (commit
  `5907196`), então `tabelas_finais/`, `mapas/` e `visualizacoes/` voltaram a
  ser ignorados. Só os arquivos rastreados **antes** disso seguem no git e
  são atualizados quando regenerados; saídas novas não são versionadas (o
  pipeline de relatório as lê do disco local). A cautela de não apagar
  saídas sem regenerá-las continua valendo.

## 4. Não editar artefatos gerados à mão

`visualizacoes/*.png`, `mapas/*.png`, `tabelas_finais/*`, `website/index.html` e
`website/data/*` (antes `relatorio/index.html`, substituído em 2026-09-24 por
`specs/2026-09-24_website_refactor`) e `relatorio/analise_primeira_infancia.pdf` são saídas de
pipeline. (Em `website/`, `css/` e `js/` são fonte editada à mão, não saída — ver
`website/README.md`.) Uma
mudança nesses arquivos que não vier de rodar `analise.py` ou os geradores (`website/build/build_site.py`,
`relatorio/latex/build/`, `relatorio/curadoria/`; até 2026-09-28 parte deles morava em
`.claude/skills/*/scripts/`) será sobrescrita na próxima regeneração e não
deve ser commitada como se fosse a fonte da mudança — edite o gerador, não o
gerado.

## 5. Fluxo de trabalho orientado a spec

- Toda mudança não-trivial (nova seção de análise, nova convenção visual,
  merge de um branch externo, refatoração) ganha uma pasta
  `specs/<AAAA-MM-DD>_<nome-da-rodada>/` (data de abertura da rodada, para
  que `specs/` liste as rodadas em ordem cronológica) **antes** da implementação, com os **quatro**
  documentos do desenvolvimento orientado a spec (regra do usuário, 2026-09-29; antes bastava um
  subconjunto): `specification.md` (o quê e por quê: contexto, decisões, requisitos, fora do escopo),
  `plan.md` (como: levantamento do código, blocos, riscos), `tasks.md` (tarefas numeradas por bloco,
  com caixas marcadas durante a execução) e `validation.md` (critérios de aceite verificáveis,
  preenchidos com o resultado ao fim). O planejamento só termina — e a implementação só começa —
  com os quatro commitados na branch de planejamento. Ver as pastas existentes (`specs/2026-09-08_mortalidade-ap`,
  `specs/2026-09-09_maps-and-ibge`, `specs/2026-09-09_visual-identity`, `specs/2026-09-14_relatorio-interativo`)
  para o formato — não é rígido, mas todo spec documenta contexto, decisões
  tomadas (com o *porquê*) e o que foi validado.
- **Antes de executar uma mudança arriscada ou que envolva reconciliar
  trabalho de terceiros (ex.: incorporar um branch externo), resuma as
  mudanças para o usuário primeiro** — não execute silenciosamente.
- **Specs documentam história — não reescreva decisões passadas.** Se uma
  convenção mudou, registre a mudança como uma nova entrada/rodada (como já
  é feito em `relatorio/specs.md` e no histórico de
  `.claude/skills/generate_map/SKILL.md`), não apague o registro do que foi
  tentado e revertido antes. Isso vale para specs e para o changelog em
  `README.md`.
- Quando a intenção do usuário for ambígua (nomenclatura, escopo, onde um
  arquivo deve morar, o que fazer com conteúdo conflitante), **pergunte** —
  agrupando várias perguntas relacionadas numa única rodada em vez de
  parar a cada dúvida individual — em vez de assumir e seguir em frente.
  As perguntas vão pela ferramenta de pergunta interativa (`AskUserQuestion`,
  até 4 perguntas por chamada, com opções e a recomendada marcada), não
  soltas no texto; se houver mais de 4, fazer rodadas sucessivas agrupadas
  por tema (reforçado pelo usuário em 2026-09-29).

## 6. Privacidade e dados sensíveis

CadÚnico e outras fontes de assistência social contêm dados de população
vulnerável. Nenhuma visualização ou tabela publicada (`relatorio/`, PDF)
deve expor granularidade abaixo do agregado por bairro/AP/RP/CAP definido
nas specs existentes — não adicionar um recorte mais fino (indivíduo,
endereço, faixa etária de 1 em 1 ano em grupos pequenos) sem confirmar
antes que é apropriado.

**Limiar de supressão (aprovado pelo usuário em 2026-09-23, `specs/2026-09-23_recortes_cadunico` §5):**
nenhuma saída publicada (`tabelas_finais/`, o site `website/` (antes `relatorio/index.html`) com os
tooltips e CSV de download, PDF, DOCX) mostra uma contagem de crianças ou
famílias do CadÚnico **menor que 20** abaixo do nível município. O mesmo vale
para o denominador de uma taxa. A célula vira vazia, com a marcação
"suprimido (< 20)", via `suprime_celulas_pequenas` (`primeira_infancia/cadunico.py`), aplicada
*depois* do cálculo e só no que é gravado ou publicado (agregações usam o
dado completo). Grupos pequenos na cidade inteira (ex. raça/cor amarela e
indígena) só aparecem no total do município. Microdados de pessoa ou
família nunca são gravados em disco.

**Agregação no lugar do vazio (pedido do usuário, 2026-09-29, `specs/2026-09-29_privacidade_cadunico`):** por bairro,
a célula pequena não fica vazia — o bairro é somado aos outros bairros pequenos da mesma **Região Administrativa**
("Demais bairros da RA X"); se o conjunto ainda ficar abaixo de 20, aos da mesma **AP**; depois, ao município
("Demais bairros"). Só o que não fecha nem assim fica vazio. Função única: `agrega_bairros_pequenos`
(`primeira_infancia/cadunico.py`), aplicada a toda saída do CadÚnico por bairro, inclusive as versionadas no git.
**Percentual por bairro:** o bairro também entra no conjunto quando o **numerador ou o complemento** (total −
numerador) é menor que 20 — percentual × total publicado devolveria a contagem. Em mapa de percentual, o bairro do
conjunto mostra a taxa do conjunto; em mapa de contagem, fica sem cor, e o total do conjunto está na tabela.
**Histórico:** o commit `cdfacd2` (2026-09-09, antes da regra) tem contagens por bairro abaixo de 20 no GitHub; a
limpeza do histórico está no `ROADMAP.md` e depende de decisão com a equipe (§7).

## 7. Git

- Branch de integração: `staging_main`. Branches de trabalho seguem
  `spec/<nome-curto>` (ex.: `spec/relatorio-interativo`) para rodadas de
  spec, ou um nome descritivo curto para trabalho pontual (ex.: `planning`).
- Depois do merge em `staging_main`, a branch da rodada pode ser apagada (com
  confirmação do usuário) desde que o ponto final fique numa tag anotada
  `rodada/<nome-curto>` (ex.: `rodada/website-mobile`) — assim o nome continua
  apontando para o estado final da rodada. Feito pela primeira vez em
  2026-09-28 (15 branches). Nunca apagar branch de outra pessoa sem perguntar.
- Mensagens de commit em rodadas de spec seguem o padrão
  `SPEC-<Nome>: Bloco N -- descrição curta` (visto no histórico); fora
  desse contexto, uma mensagem direta em português descrevendo o *porquê*
  basta.
- **Branch `demo` — versão de demonstração** (regra do usuário, 2026-09-29, `specs/2026-09-29_demo`): texto
  provisório no lugar do lorem (`website/build/textos_demo.json`), blocos pendentes ocultos, faixa maior com a data
  da V.1 e PDF só até a página impressa 18 com página de aviso. Tudo isso é **exclusivo da `demo`**: não entra em
  `staging_main`, em `main` nem em outra branch. O fluxo é **só de ida** (`staging_main` → `demo`, para atualizar);
  a `demo` nunca é mesclada de volta. O texto provisório nunca vai para o PDF, para `relatorio/textos_curados.json`
  nem para o DOCX de curadoria, que seguem mostrando lorem e pendentes. Enquanto a demonstração estiver no ar, o
  GitHub Pages publica só a partir da `demo`.
- **Direção dos merges** (regra do usuário, 2026-09-29): o trabalho sobe das branches de rodada para a integração, e
  a integração desce para as derivadas. Nunca no sentido contrário:
  - `spec/<nome>` → `staging_main` (merge `--no-ff` ao fim da rodada);
  - `staging_main` → `main` (publicação);
  - `staging_main` → `demo` (para atualizar a demonstração). Depois do merge, regere o site e o PDF na `demo` e
    confira que o build não parou por falta de texto provisório.
  - **Proibido**: `demo` → `staging_main`/`main`/`spec/*`, e `staging_main` ← qualquer branch que tenha a `demo` na
    história. Uma correção feita na `demo` que valha para todos é refeita numa `spec/<nome>` a partir de
    `staging_main` (ou por `cherry-pick` de um commit que não traga nada da demonstração), nunca por merge.
- Nunca force-push, nunca reescreva commits já publicados, nunca pule hooks
  — pedir confirmação explícita antes de qualquer operação destrutiva
  (`reset --hard`, `checkout --`, deletar branch).
