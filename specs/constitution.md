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
  da rodada (`specs/<nome>/`), o README só aponta pra lá.

## 2. `analise.py` é a fonte de verdade

- `analise.py` (formato Jupytext `py:percent`) é o artefato versionado.
  `analise.ipynb` é gerado (`jupytext --to notebook`) e está no `.gitignore`
  — nunca edite o `.ipynb` esperando que a mudança persista; edite o `.py` e
  rode `jupytext --sync`.
- Toda função reutilizável de limpeza/wrangling ou de visualização vive na
  seção **📦 Pacotes e Funções Auxiliares**, no topo do arquivo. Seções de
  análise abaixo só **chamam** essas funções — não redefinem lógica de
  limpeza ou de plot inline numa célula de análise.
- Rode o notebook do zero (kernel limpo, top-to-bottom) antes de considerar
  uma mudança validada — já houve bug real (`specs/maps-and-ibge`) que só
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
- **População de referência por nível** (`specs/populacao-referencia`, 2026-09-24): taxa **municipal**
  usa as estimativas Ripsa/MS do mesmo ano (`populacao_ripsa`); taxa **sub-municipal** (bairro, AP, RP,
  RA, CAP) usa o Censo 2022, fixo, e diz isso na fonte ou na legenda. Nunca comparar uma com a outra
  sem dizer (o Censo 2022 subconta crianças pequenas). A faixa etária do rótulo é a faixa real do dado
  (`specs/populacao-referencia/auditoria_faixas.md`), não a do catálogo.
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
  `specs/reorganize-naming/` até ser aprovada e aplicada).
- ⚠️ **Achado 2026-09-22, ainda não corrigido**: `.gitignore` tem as regras
  de `mapas/`, `tabelas_finais/` e `visualizacoes/*.png` comentadas (`#` no
  início da linha) — na prática essas pastas **estão sendo versionadas**,
  contradizendo a descrição de "artefato gerado" do §4 abaixo. Não rode uma
  regeneração completa nem apague esses arquivos achando que são
  recuperáveis via regeneração até isso ser decidido — confirme com o
  usuário antes.
  **Atualização 2026-09-23 (`specs/recortes_cadunico`):** o achado acima
  não vale mais. As regras foram reativadas em 2026-09-22 (commit
  `5907196`), então `tabelas_finais/`, `mapas/` e `visualizacoes/` voltaram a
  ser ignorados. Só os arquivos rastreados **antes** disso seguem no git e
  são atualizados quando regenerados; saídas novas não são versionadas (o
  pipeline de relatório as lê do disco local). A cautela de não apagar
  saídas sem regenerá-las continua valendo.

## 4. Não editar artefatos gerados à mão

`visualizacoes/*.png`, `mapas/*.png`, `tabelas_finais/*`, `relatorio/index.html`
e `relatorio/analise_primeira_infancia.pdf` são saídas de pipeline. Uma
mudança nesses arquivos que não vier de rodar `analise.py` ou os scripts em
`.claude/skills/*/scripts/` será sobrescrita na próxima regeneração e não
deve ser commitada como se fosse a fonte da mudança — edite o gerador, não o
gerado.

## 5. Fluxo de trabalho orientado a spec

- Toda mudança não-trivial (nova seção de análise, nova convenção visual,
  merge de um branch externo, refatoração) ganha uma pasta
  `specs/<nome-da-rodada>/` **antes** da implementação, com o subconjunto
  relevante de `plan.md`, `specification.md`/`specs.md`, `tasks.md`,
  `validation.md`. Ver as pastas existentes (`specs/mortalidade-ap`,
  `specs/maps-and-ibge`, `specs/visual-identity`, `specs/relatorio-interativo`)
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

## 6. Privacidade e dados sensíveis

CadÚnico e outras fontes de assistência social contêm dados de população
vulnerável. Nenhuma visualização ou tabela publicada (`relatorio/`, PDF)
deve expor granularidade abaixo do agregado por bairro/AP/RP/CAP definido
nas specs existentes — não adicionar um recorte mais fino (indivíduo,
endereço, faixa etária de 1 em 1 ano em grupos pequenos) sem confirmar
antes que é apropriado.

**Limiar de supressão (aprovado pelo usuário em 2026-09-23, `specs/recortes_cadunico` §5):**
nenhuma saída publicada (`tabelas_finais/`, `relatorio/index.html` com os
tooltips e CSV de download, PDF, DOCX) mostra uma contagem de crianças ou
famílias do CadÚnico **menor que 20** abaixo do nível município. O mesmo vale
para o denominador de uma taxa. A célula vira vazia, com a marcação
"suprimido (< 20)", via `suprime_celulas_pequenas` em `analise.py`, aplicada
*depois* do cálculo e só no que é gravado ou publicado (agregações usam o
dado completo). Grupos pequenos na cidade inteira (ex. raça/cor amarela e
indígena) só aparecem no total do município. Microdados de pessoa ou
família nunca são gravados em disco.

## 7. Git

- Branch de integração: `staging_main`. Branches de trabalho seguem
  `spec/<nome-curto>` (ex.: `spec/relatorio-interativo`) para rodadas de
  spec, ou um nome descritivo curto para trabalho pontual (ex.: `planning`).
- Mensagens de commit em rodadas de spec seguem o padrão
  `SPEC-<Nome>: Bloco N -- descrição curta` (visto no histórico); fora
  desse contexto, uma mensagem direta em português descrevendo o *porquê*
  basta.
- Nunca force-push, nunca reescreva commits já publicados, nunca pule hooks
  — pedir confirmação explícita antes de qualquer operação destrutiva
  (`reset --hard`, `checkout --`, deletar branch).
