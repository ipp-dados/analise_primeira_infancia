# Roadmap

Estado em 2026-09-28 (fim do dia; curadoria: update 5). Arquivo único do projeto: substitui `specs/roadmap.md` e `website/ROADMAP.md`
(fundidos aqui em 2026-09-25). As decisões e o *porquê* de cada item ficam na pasta da rodada em `specs/`
(`specs/<AAAA-MM-DD>_<nome>/`); aqui fica só o que falta fazer e onde procurar.

Organização: **Em andamento** → **Próximos** (fila priorizada) → **Backlog por tema** → **Concluído** (histórico
resumido). Dentro de cada seção, a ordem é a de prioridade.

---

## Em andamento

-1. **Nova estrutura + apresentação — planejadas em 2026-09-28** (branch `planning`). (a) `specs/2026-09-28_nova_estrutura`:
   Introdução com panorama (população e nascidos vivos) na Visão geral e no capítulo de Introdução do PDF, 7º eixo
   "Direito ao Brincar", reordenação conforme a planilha da equipe; `specs/estrutura_eixos.md` já atualizado (51 itens,
   nenhum arquivo removido). **Não publicar o PDF antes do Bloco 2** (a Introdução viraria "Eixo 1 de 8"). Regra do
   usuário: acrescentar o que falta, nunca remover o que sobra. (b) `specs/2026-09-28_apresentacao`: deck de 30 slides
   em Marp, com fonte única em Markdown e variantes; depende de (a); respostas Q1-Q6 recebidas (PPTX, gestores, textos propostos por nós). Lacunas registradas:
   taxa de mortalidade de 1 a 4 anos, taxa de violência de todas as naturezas, efeito visual do eixo transversal.

0. **Melhorias do site e do relatório — Rodada A implementada em 2026-09-28** (`specs/2026-09-28_melhorias_site`,
   branch `spec/melhorias-site`): favicon novo (monograma "PI", escolhido pelo usuário; alternativas em `website/build/favicon_opcoes/`,
   trocar com `gera_favicon.py`), texto de abertura de cada eixo (`introducao_<eixo>`, lorem até ser curado), lorem ≤ 150
   palavras, pequenos múltiplos só com Painéis, `index.html` 785 → 343 KB sem mudança visual. Mesclada em
   `staging_main` em 2026-09-28; falta o deploy. **Rodada B concluída** no mesmo dia (item 1 de Próximos, fases 1a e
   1b, `specs/2026-09-28_organizacao`). **Rodada C concluída** no mesmo dia (item 6 de Próximos:
   documentação + `docs/especificacao_projeto.md`, `specs/2026-09-28_documentacao`).

1. **Site: exclusões + `improve charts`** — implementado em 2026-09-25 (`specs/2026-09-25_website_graficos`, branch
   `spec/website-graficos`). O push para `staging_main` quebrou o site publicado e foi **revertido em 2026-09-28**
   (commit de rollback `883b4b1`); correções na rodada `specs/2026-09-28_website_bugfix` (mesmo branch: cache das
   folhas de estilo/JS, telas estreitas, textos curados ausentes). Rollback revertido e branch corrigido integrado em
   `staging_main` no mesmo dia (`21cc040`). Falta só o **deploy**, com OK do usuário. Decisões abertas levantadas na
   revisão:
   - mapa de taxa de mortalidade infantil por bairro aparece **duas vezes** no eixo Prioridade (cartão de raça/cor e
     "Total" do cartão neonatal, mesmos valores) — decidir qual fica (site e PDF);
   - unidade dos indicadores do IPS (violência territorial): rotulada "por 100 mil habitantes", convenção do IPS
     Rio, mas a planilha do Data.Rio não traz a unidade — confirmar;
   - curadoria: os 2 textos que tiveram a unidade convertida (`controle_revisao.json`, `ajustes_manuais`, "revisar");
   - série "Não informada" na taxa de mortalidade infantil por raça/cor (`percentual_mortalidade_raca_ano`, site e
     PDF): chega a 89‰ e achata as outras linhas, porque divide óbitos sem raça (SIM) por nascidos sem raça (SINASC),
     o que não é uma taxa comparável. Proposta: tirar essa série do gráfico de taxa e mantê-la no de contagem;
   - base zero nas taxas (decisão P1): variações pequenas, como o baixo peso ao nascer entre 9% e 11%, ficam mais
     achatadas. Rever com a equipe se algum indicador deve ter o eixo cortado, com o corte visível no gráfico.

2. **Curadoria de textos** (contínuo; DOCX `relatorio/curadoria_textos.docx`, controle em
   `relatorio/controle_revisao.json`; updates antigos em `relatorio/textos_updates_antigos/`). Última rodada:
   update 5 (2026-09-28) — 7 textos novos no relatório (causas evitáveis por faixa e por subgrupo em < 1, 1-4 e
   < 5 anos; Censo 0-6 por raça/cor; taxa de frequência escolar por raça/cor e por sexo) e 2 de figuras fora do
   relatório (frequência escolar absoluta, E8), guardados como órfãos.
   - ainda em lorem ipsum: resumo, principais achados e síntese de cada eixo, e textos de figura (46 chaves ao todo no
     total; a lista sai no build: `gera_latex.py` imprime "textos em lorem");
   - alertas abertos para a equipe decidir (não corrigidos no texto): mapa de taxa de mortalidade infantil cita os
     números da taxa pós-neonatal; frase das Considerações finais possivelmente sem "não" ("deve atuar de forma
     isolada"); texto da cobertura vacinal anual pronto, mas a figura está fora do relatório (E1); **novos no
     update 5**: subgrupos < 5 anos cita 198 óbitos por atenção ao recém-nascido em 2006 (a tabela tem 204); taxa de
     frequência escolar por raça/cor e por sexo lê a linha "Total" da tabela SIDRA 10056 como "conjunto de 0 a 6
     anos" (é o total de todas as idades: ~25%, com taxas de 8% a 97% por idade);
   - 2 textos com a unidade convertida depois da base do update 5 (`percentual_mortalidade_raca_ano`,
     `mapa_taxa_obitos_raca_total_bairro_2025`: percentual → por mil) continuam em `ajustes_manuais`, a revisar;
   - nota editorial em aberto no subgrupo 28-364 dias: "opção de texto que junte tudo por conta da repetição".
   - próximo update: baixar a partir do `relatorio/curadoria_textos.docx` atual (o update 5 partiu do update 4 e
     por isso ainda trazia textos já corrigidos depois).

---

## Próximos

1. **Organização do projeto (feat)** — fases **1a e 1b concluídas em 2026-09-28** (`specs/2026-09-28_organizacao`,
   branch `spec/organizacao`; mesmas 431 saídas antes e depois): funções do notebook no pacote `primeira_infancia/`
   (um módulo por tema, `analise.py` de 4.786 para 2.938 linhas), scripts de pipeline da skill do PDF em
   `relatorio/curadoria/`, `requirements.txt` só com as dependências diretas fixadas (+ `requirements-dev.txt`),
   restos de compilação LaTeX removidos. Falta a **fase 1c**, numa rodada própria, com a mesma regra
   ("mesmas saídas antes e depois"):
   - **Pastas de dados e saídas**: reorganizar `dados_locais/`, `tabelas_finais/`, `visualizacoes/` e `mapas/`
     (estrutura por fonte/eixo, nomes, o legado `mapas/tabelas_bairros/` — cujos 3 `.xlsx` versionados são
     regravados a cada execução só com metadados novos —, as variantes `a4/`); atualizar os leitores
     (`website/build/build_site.py`, `relatorio/latex/build/`, `relatorio/curadoria/`, `specs/estrutura_eixos.md`,
     skills, `primeira_infancia/`).
   - Revisitar a decisão de `specs/2026-09-22_ajuste_eixos` §9.1 (não reordenar fisicamente as seções) agora que as
     funções saíram do arquivo — a ordem continua sendo de dependência de dados.
   - Pré-requisito do item 2.

2. **Empacotar scripts reutilizáveis para outros projetos** (depois do item 1) — transformar em pacotes
   instaláveis o que não é específico da primeira infância: mapa coroplético por bairro/AP/RP/RA com fundo
   cartográfico e rodapé, limpeza de exportações do Tabnet, carga do SIDRA, população Ripsa, gráficos com a
   identidade visual, relatório ABNT em LaTeX a partir de um crosswalk `.md`, round-trip de curadoria em DOCX.
   Definir fronteiras, nomes, versionamento e onde publicar (repositório próprio, pip via git).

3. **Estimativa de crianças pequenas por bairro com a Ripsa** (pedido do usuário, 2026-09-24; continuação da
   decisão B1 de `specs/2026-09-24_populacao-referencia`). O Censo 2022 fixo subconta crianças pequenas (0-4:
   310.648 no Censo contra 361.163 na Ripsa em 2022, +16%) e não varia por ano. Estimativa derivada, rotulada
   como tal:
   - **(b)** participação de cada bairro no Censo 2022 × total municipal Ripsa de cada ano, com 0-4 estendido
     para 0-5 pela razão municipal Ripsa; os bairros somam o total Ripsa;
   - **(c)** como (b), com a participação variando no tempo entre os Censos 2010 e 2022 (exige a
     correspondência 160 → 166 bairros).
   Depois recalcular as taxas sub-municipais (violência por bairro/RA/CAP e o % CadÚnico, que depende também do
   item CadÚnico 1) e documentar a mudança de denominador.

4. **Agregar amarela + indígena na frequência escolar por raça/cor** (decidido em 2026-09-25; `specs/exclusoes.md`
   E12) — taxa de frequência escolar por idade e raça/cor do Censo 2022 (`sidra_taxa_frequencia_0_6_raca_2022`):
   os dois grupos são pequenos e chegam a 100% em várias idades. Mesma regra de E5: somar os absolutos
   (frequentam / população) e recalcular a taxa, nunca somar percentuais; aplicar no gráfico de `analise.py`
   (tela e impressão), na tabela do PDF e no site.

5. **Site: versão mobile — implementada em 2026-09-28** (`specs/2026-09-28_website_mobile`, branch
   `spec/website-mobile`), validada no Playwright em 3 motores e 4 tamanhos; o desktop não mudou (conferido pixel a
   pixel). Falta: **teste num iPhone e num Android** (roteiro em `validation.md` V7, com o usuário), merge em
   `staging_main` e deploy. Fica para depois: tablet com alvos de toque de 44 px e texto dos gráficos de viewBox fixo
   entre 9,5 e 11 px (a meta de 44 px / 11 px desta rodada era só do celular).

6. **Atualizar a documentação do projeto — concluído em 2026-09-28** (`specs/2026-09-28_documentacao`): documentos
   alinhados ao estado real e **especificação funcional/técnica** do projeto em `docs/especificacao_projeto.md`.
   Mantê-la em dia a cada rodada (a §11 dela diz o que conferir).

---

## Backlog por tema

### CadÚnico
1. **Geocodificação por bairro oficial** (F1 de `specs/2026-09-23_recortes_cadunico`): o bairro vem do CEP dos
   Correios (`lista_bairros.csv`), que deixa 8,1% das crianças sem bairro e desloca bairros-favela para os
   vizinhos (Maré → Bonsucesso, Rocinha → Gávea; Vila Kennedy/Jabour/Gericinó/Ilha de Guaratiba/Lapa ausentes).
   Refazer por join espacial ou código de bairro do CTPE; só então o mapa "% CadÚnico/Censo" volta ao relatório.
2. **Pedido ao CTPE** (F2): extração com parentesco/responsável familiar (arranjo real), deficiência (3 itens de
   Inclusão) e características do domicílio (2 itens de Moradia).
3. **Filtro de cadastro da silver** (F3): confirmar com o CTPE se `silver_cadunico_geral` já exclui cadastros
   inativos/desatualizados.

### Mortalidade
- Séries temporais comparando subgrupos específicos entre regiões ao longo do tempo.
- Mapas comparando subgrupos específicos entre regiões em 2025.
- Mapas para todos os dados com granularidade até bairro.
- Versões por AP/RP (não só bairro) dos indicadores por bairro de `specs/2026-09-09_maps-and-ibge` (nascidos
  vivos, baixo peso, mortalidade neonatal, óbitos por raça, óbitos gravidez/puerpério) — fora do escopo daquela
  rodada, ver seu §7. Considerar `specs/exclusoes.md` (E4, E9) antes.

### Educação
- Mapa de matrículas por bairro, com as escolas geocodificadas (o arquivo do INEP não traz `codbairro`; ver
  `specs/2026-09-24_populacao-referencia/matriculas/specification.md` §4.4).
- Validar 1 ou 2 anos contra a Sinopse Estatística do INEP (pendência P5 da mesma rodada).

### Outros dados
- Levantar e importar bases pendentes (a detalhar): indicadores do catálogo ainda `pendente` em
  `specs/estrutura_eixos.md` (Moradia, deficiência, violência por tipificação, causas evitáveis por sexo).

### Site (`website/`)
- **Página "Fale Conosco"** (pedido do usuário, 2026-09-24): rota por hash (`#fale-conosco`) como uma aba,
  acessível pela barra de navegação. Formulário exige backend, que o GitHub Pages não tem — `mailto:` + texto
  (estático) ou serviço externo (exige decisão sobre dados pessoais/LGPD).
- **Tirar a faixa "EM DESENVOLVIMENTO / TEMPORÁRIO" do site e a marca d'água do PDF** quando deixarem de ser versão
  de teste — decisão do usuário. Uma chave só: `relatorio/publicacao.json` → `"em_desenvolvimento": false`, depois
  regerar o site e o PDF (`gera_latex.py --publicar`).
- **Confirmar URLs/e-mail reais do rodapé** (Transparência Rio, LGPD, contato; hoje `ascom.ipp@prefeitura.rio`,
  placeholder) — `specs/2026-09-14_relatorio-interativo/tasks.md` T6.2.
- **Logo**: confirmar autorização de uso do logo oficial da Prefeitura/IPP antes do deploy público (T0.4) e pedir
  o SVG oficial à Ascom do IPP (hoje PNG em `srcset`, `specs/2026-09-24_website_refactor` D6).
- **Fontes quase repetidas** na caixa "Fontes desta seção": unificar as constantes `FONTE_*` do gerador (pode
  sair junto com as referências ABNT da rodada em andamento).
- Medir formalmente o contraste do rodapé (WCAG AA; T5.6 — só houve inspeção visual).
- Altura da caixa de texto fora do padrão mapa (240 px com rolagem): revisitar quando os textos reais entrarem.
- **Dados por aba com carregamento tardio** e **outliers de mapa como troca de cor**: medidos e deixados de fora
  (`website_refactor` §4.9); voltam se o orçamento de tamanho estourar.
- Botão "baixar tudo"; persistir estado de collapse (localStorage), se pedido; **tema escuro** (removido na v6.2,
  os tokens em `css/main.css` facilitam voltar).
- **Camada própria de água/costa** nos mapas: hoje o mar vem só do tile (Esri Ocean); necessária apenas se um
  dia for preciso colorir o mar por conta própria (`relatorio/specs.md` v6.4-v6.6).

### Repositório (git)

Decididos em 2026-09-28 para depois (a limpeza de branches mescladas foi feita no mesmo dia, ver Concluído):

- **Tamanho do histórico** — o pack tem ~178 MB, quase tudo binário com muitas versões: o PDF (19 versões, 644 MB
  sem compactar), o antigo `relatorio/index.html` (308 MB) e o DOCX de curadoria (87 MB). **Não reescrever o histórico
  por ora**: mudaria o identificador de todos os commits (clones e a branch da Waleska refeitos; hashes citados no
  `CHANGELOG.md` e nas `specs/`, como o rollback `883b4b1`, deixariam de existir). Primeiro conter o crescimento:
  publicar o PDF como anexo de Release do GitHub em vez de versioná-lo a cada build, ou pôr PDF/DOCX no Git LFS. Se
  o clone um dia atrapalhar, uma limpeza única combinada com a equipe (tag antes, `git filter-repo`, todos reclonam).
- **Papel da `main`** — está 204 commits atrás de `staging_main` (a branch padrão) e nunca recebeu as rodadas.
  Proposta: usá-la como branch de versão e mesclar `staging_main` nela quando `relatorio/publicacao.json` passar para
  a versão final; alternativa: aposentá-la.
- **`waleska-analise-primeira-infancia`** — tem 2 commits de conteúdo que não estão em `staging_main` ("Ajusta análise
  dos resultados da primeira infância", "Ajusta curadoria da primeira infancia", 2026-09-22); confirmar com a autora se
  ainda são necessários antes de mesclar ou apagar.

### Ideias (sem decisão)
- Substituir a visualização HTML por um painel Streamlit.

---

## Concluído

Resumo; detalhes na pasta da rodada.

| Quando | O quê | Onde |
| :-- | :--- | :--- |
| 2026-09-28 | Git: 15 branches já mescladas apagadas (13 `spec/*`, `ajuste_eixos`, `inclusao_dados_protecao`), cada ponto final preservado numa tag `rodada/<nome>`; ficam `main`, `planning`, `staging_main` e a branch da Waleska | `specs/constitution.md` §7 |
| 2026-09-28 | Documentação alinhada ao estado real e especificação funcional/técnica do projeto (`docs/especificacao_projeto.md`); `.env.example` | `specs/2026-09-28_documentacao` |
| 2026-09-28 | Organização do projeto, fases 1a e 1b: pacote `primeira_infancia/`, scripts em `relatorio/curadoria/`, requisitos diretos fixados, 431/431 saídas idênticas | `specs/2026-09-28_organizacao` |
| 2026-09-28 | Rodada A de melhorias: favicon (SVG + `.ico` + apple-touch), abertura de cada eixo, lorem ≤ 150 palavras, só Painéis nos pequenos múltiplos, `index.html` 785 → 343 KB (mapas montados em JS, sprite de ícones) | `specs/2026-09-28_melhorias_site` |
| 2026-09-28 | Curadoria: update 5 incorporado (7 textos novos no site e no PDF, 2 órfãos; controle de revisão recalculado sobre as 5 rodadas; updates antigos em `relatorio/textos_updates_antigos/`; scripts `compara_updates.py` e `valida_textos_publicados.py`) | `relatorio/controle_revisao.json`, skill `export_pdf_report` |
| 2026-09-28 | Site mobile (`css/mobile.css`: gráficos na largura real, "Nesta seção", select, legenda abaixo do mapa, toque) e marca d'água "EM DESENVOLVIMENTO" no PDF ligada à faixa do site (`relatorio/publicacao.json`) | `specs/2026-09-28_website_mobile` |
| 2026-09-28 | Rollback de `staging_main` e correções do site (cache de CSS/JS, telas estreitas, textos curados ausentes); tabelas de conferência texto × figura | `specs/2026-09-28_website_bugfix` |
| 2026-09-25 | Site: exclusões E2-E9 (alternância Taxa ↔ Óbitos), paleta validada, teto P95, unidades nos eixos e taxas por mil com ‰, base zero, pequenos múltiplos, fontes ABNT, textos de achados/síntese; revisão de unidades também na origem (`analise.py`, PDF) | `specs/2026-09-25_website_graficos` |
| 2026-09-25 | Relatório final em LaTeX/ABNT publicado (`relatorio/analise_primeira_infancia.pdf`), validação V1-V20; substitui o PDF por HTML/Edge headless | `specs/2026-09-25_relatorio_latex` |
| 2026-09-25 | Lista de exclusões (E1-E12) aplicada ao PDF e ao `analise.py` | `specs/exclusoes.md` |
| 2026-09-25 | Pastas de `specs/` prefixadas com a data de abertura; roadmaps fundidos neste arquivo | este arquivo, `CLAUDE.md` |
| 2026-09-24 | Site estático em `website/` (abas por eixo, sumário lateral, geometria compartilhada, 1,5 MB) | `specs/2026-09-24_website_refactor` |
| 2026-09-24 | População de referência: Ripsa no município, Censo 2022 rotulado no sub-municipal; auditoria de faixas etárias e 21 renomeações; % de nascidos vivos por bairro; total dobrado dos Censos corrigido | `specs/2026-09-24_populacao-referencia` |
| 2026-09-24 | Matrículas 2007-2025 refeitas dos microdados do INEP, taxa bruta de atendimento e metas do PNE | `specs/2026-09-24_populacao-referencia/matriculas` |
| 2026-09-23 | Recortes do CadÚnico (sexo, raça/cor, renda × arranjo), supressão < 20 | `specs/2026-09-23_recortes_cadunico` |
| 2026-09-23 | Dados de violência e eixo Proteção; nível geográfico `ra` | `specs/2026-09-23_inclusao_dados_protecao` |
| 2026-09-23 | GitHub Pages publicado (deploy manual por `workflow_dispatch`) | `.github/workflows/deploy-relatorio.yml` |
| 2026-09-22 | Relatório reorganizado por eixo da política (crosswalk `specs/estrutura_eixos.md`, DOCX de curadoria) | `specs/2026-09-22_ajuste_eixos` |
| 2026-09-22 | Reorganização de dados/nomes (`dados_locais/` por tema, convenções de saída, 39 órfãos removidos) | `specs/2026-09-22_reorganize-naming` |
| 2026-09-22 | Merge das mudanças da Waleska | `specs/2026-09-22_merge-waleska-changes` |
| 2026-09-14 | Relatório interativo (HTML), todos os mapas em SVG | `specs/2026-09-14_relatorio-interativo`, `relatorio/specs.md` |
| 2026-09-09 | Identidade visual unificada; mapas e dados IBGE | `specs/2026-09-09_visual-identity`, `specs/2026-09-09_maps-and-ibge` |
| 2026-09-08 | Mortalidade por AP/CAP | `specs/2026-09-08_mortalidade-ap` |
