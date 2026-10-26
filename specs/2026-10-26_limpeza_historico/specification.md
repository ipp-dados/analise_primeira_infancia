# Limpeza do repositório e do histórico git — especificação

Rodada aberta em 2026-10-26 a pedido do usuário ("limpar/organizar o git e os arquivos locais"). Duas partes:
**A** (feita nesta data, sem reescrever nada) e **B** (reescrita do histórico — planejada, **depende de acordo com a
equipe** antes de executar; constituição §7).

## 1. Situação encontrada (2026-10-26)

- Repositório **público** (`ipp-dados/analise_primeira_infancia`). `.git` local com 1,5 GB (1,2 GB de objetos soltos),
  pack de 255 MB; GitHub reporta ~740 MB.
- Peso do histórico (em disco, compactado): ~325 MB de PNG (`mapas/`, `visualizacoes/`), ~313 MB de PDF/PPTX/DOCX
  (PDF do relatório com até 48 MB por versão, decks, DOCX de curadoria), ~13 MB do antigo `relatorio/index.html`.
- **Privacidade:** o commit `cdfacd2` (2026-09-09) tem contagens do CadÚnico por bairro de 1 a 19 (`tabelas_finais/`,
  ver `specs/2026-09-29_privacidade_cadunico` D3); o commit `101e6bf` (2026-10-19) publicou `revisao_casa_civil/`
  (revisões externas do PMPIA, uma com nome de pessoa no arquivo).
- 131 saídas (`tabelas_finais/`, `visualizacoes/`, `mapas/`, inclusive `mapas/tabelas_bairros/`) rastreadas apesar
  do `.gitignore` (rastreadas antes de `5907196`) — pastas meio versionadas.
- Branches: 16 mescladas e 2 não mescladas (`spec/deck_familia_moradia`, `waleska-analise-primeira-infancia`).

## 2. Parte A — feito em 2026-10-26

| Decisão | Feito |
| :-- | :-- |
| A1 Branches mescladas | Tag anotada `rodada/<nome>` no ponto final e branch apagada (local e `origin`): `apresentacao`, `cadunico_inclusao_moradia`, `deck_alimentacao_brincar`, `deck_inclusao` (ponta local `114fb49`, à frente da remota), `deck_moradia`, `desempenho_site`, `filtro_residencia_tabnet`, `nova_estrutura`, `alinhamento-pdf-site`, `dados-adhoc`, `dados-adhoc-slides`, `demo` (a `spec/demo`; a branch `demo` fica), `pendencias`, `privacidade-cadunico`, `planning`. Ficam `staging_main`, `demo`, `main` (papel em aberto no `ROADMAP.md`). |
| A2 `waleska-analise-primeira-infancia` | Não mesclável: a ponta tem o `analise.py` com as funções no próprio arquivo (anterior ao pacote `primeira_infancia/`) — mesclar desfaria `specs/2026-09-28_organizacao`. O texto "Análise dos resultados" (`b493216`) não está na ponta da branch nem em `staging_main`; `baixar_ripsa.py` (`36e06fc`) baixa a população de outra fonte (Tabnet SES-RJ) que difere em poucas unidades da usada (`carrega_populacao_ripsa`, Tabnet/DATASUS). Arquivada em `rodada/waleska-analise-primeira-infancia` e apagada (autorização do usuário). |
| A3 `spec/deck_familia_moradia` | A parte de Moradia foi substituída por `spec/deck_moradia` (mesclada em 2026-10-08); a variante **Família e Cuidados** só existe nela. Merge de teste: conflito em `apresentacao/README.md`, `build/numeros.py`, `build/mapas_apresentacao.py`, `variantes/moradia.md`. Arquivada em `rodada/deck_familia_moradia` e apagada (autorização do usuário); retomar numa rodada própria, a partir da tag. |
| A4 Saídas rastreadas | `git rm --cached` nas 131 saídas: ficam no disco, saem dos próximos commits. As 3 tabelas Excel que `analise.py` gravava em `mapas/tabelas_bairros/` passam a ir para `tabelas_finais/` (cópia feita no disco); a célula de setup cria `mapas/` no lugar da subpasta. **Efeito colateral:** quem fizer `pull` desse commit perde essas saídas da cópia local (regeneráveis; as do CadÚnico exigem o banco). |
| A5 `revisao_casa_civil/` | `git rm --cached` + `.gitignore`; fica só local. Continua no histórico até a Parte B. |
| A6 Local | `git gc` (1,5 GB → 688 MB); apagados `apresentacao/node_modules/`, `apresentacao/_build/`, `relatorio/latex/_build/`, `__pycache__/`. |

## 3. Parte B — reescrita do histórico (planejada)

**Objetivo:** tirar do histórico inteiro (todas as branches e tags) (a) o dado do CadÚnico abaixo de 20 e
`revisao_casa_civil/` (privacidade, repositório público) e (b) os binários gerados que incham o clone.

**Caminhos removidos** (`git filter-repo --invert-paths`):
- `revisao_casa_civil/`
- `tabelas_finais/`, `visualizacoes/`, `mapas/` (tudo, menos `.gitkeep`) — após A4 nenhum deles é rastreado;
- `relatorio/index.html`, `relatorio/relatorio.html` (antigos relatórios HTML);
- `relatorio/**/*.pdf|docx` e `apresentacao/*.pdf|pptx` (PDF publicado, DOCX de curadoria e rodadas antigas, decks).

**Teste em cópia (2026-10-26, `git-filter-repo` 2.47.0 num clone espelho):** 688 MB → **12 MB**; 357 → 346 commits
(11 commits só de saídas ficam vazios e somem); 33 tags preservadas e reescritas; `staging_main` mantém `analise.py`,
`primeira_infancia/`, `website/`, `specs/`, `dados_locais/`.

**Decisões pendentes (equipe):**
- B-D1 PDF/PPTX publicados: (recomendado) anexos de uma **Release do GitHub** por versão, com o link no README e no
  site; alternativa: recolocar só a versão atual num commit após a reescrita (o crescimento volta a cada build).
- B-D2 DOCX de curadoria (`curadoria_textos.docx`, `textos_updates_antigos/`): recolocar só a versão atual
  (o fluxo de curadoria os lê do disco) ou guardá-los fora do git (Drive da equipe).
- B-D3 Hashes citados no `CHANGELOG.md`, `ROADMAP.md` e `specs/` (ex.: `883b4b1`, `cdfacd2`, `5907196`): o
  filter-repo reescreve os das mensagens de commit; os do conteúdo dos arquivos são trocados com `--replace-text`
  gerado do `filter-repo/commit-map` (hash antigo abreviado → novo), conferido por amostragem.
- B-D4 Data combinada: ninguém com trabalho não enviado; todos reclonam depois.

## 4. Riscos

- Cópia local antiga que dê push reintroduz o histórico velho — todos reclonam; não mesclar clones antigos.
- O GitHub mantém objetos antigos acessíveis por hash e em `refs/pull/*` (não dá para forçar push nelas): para o dado
  do CadÚnico, pedir ao **GitHub Support** a remoção de dados sensíveis (cache e PRs) após o force-push; verificar
  forks.
- O deploy do Pages sai da `demo`: refazer o deploy depois do force-push.
- O backup espelho anterior à reescrita contém o dado sensível: guardar fora do repositório, com acesso restrito, e
  apagar depois de validado.
