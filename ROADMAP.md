# Roadmap

Estado em 2026-11-05 (pendências fechadas em `specs/2026-11-05_fechamento_pendencias`; próxima: versão final do site). Arquivo único do projeto: substitui
`specs/roadmap.md` e `website/ROADMAP.md` (fundidos aqui em 2026-09-25). As decisões e o *porquê* de cada item ficam
na pasta da rodada em `specs/` (`specs/<AAAA-MM-DD>_<nome>/`); aqui fica só o que falta fazer, onde procurar e o
histórico resumido.

Organização em duas partes:
- **A fazer** — (1) **Rodada atual**, (2) **Aguardando equipe/usuário** (depende de terceiros, não de código),
  (3) **Próximas features** (fila priorizada), (4) **Backlog por tema**. Dentro de cada seção, a ordem é a de prioridade.
- **Concluído** — histórico resumido, do mais recente ao mais antigo.

---

# A fazer

## 1. Rodada atual — Versão final do site (`specs/2026-11-05_versao_final_site`, branch `spec/versao_final_site`)

Aberta em 2026-11-05 (pedido em `specs/2026-11-05_versao_final_site/initial_prompt.md`). **Dados e pipeline congelados** nesta rodada: só
textos, documentação e configuração. Feito (blocos 1-7): textos do site e do PDF conferidos contra os dados, sem lorem
(curadoria de 05/11 incorporada); banner com foto (crédito Unsplash) e rodapé com links conferidos; mapa de referência
da cidade (vizinhos, RA/AP) na Introdução; PDF com um `.tex` editável por capítulo, capa e folha de rosto novas;
curadoria só do site, em JSON (fim do DOCX, tag `rodada/curadoria_docx`); `publica_release.py` e Actions (deploy na
`main`, conferência na `staging_main`); site sem a faixa EM DESENVOLVIMENTO, publicado por ora pela `staging_main`.

Em andamento — bloco 8: revisão de pipelines e documentação, títulos "até 72 meses" (feito em 2026-11-06), teste
completo desktop 1366 px e celular 390 px. Falta com OK — bloco 9: merge em `staging_main` e `main`, Release do PDF,
constituição §7, Pages pela `main` (ajustes manuais nas configurações do GitHub).

Fica para depois da rodada (exige rodar o pipeline):
- títulos das figuras PNG ainda com "0 a 5 anos" (D10 de `specs/2026-10-06_cadunico_inclusao_moradia`);
- deep link de Alimentação/SISVAN termina sob a barra fixa (achado de `specs/2026-09-30_desempenho_site`) — conferir
  no teste do bloco 8.

## 2. Aguardando equipe/usuário

Não dependem de código; entram no projeto quando chegarem.

- **Pedido ao GitHub Support** (`specs/2026-10-26_limpeza_historico/pedido_github_support.md`, passo a passo e mensagem prontos): remover o
  cache dos commits antigos `cdfacd2` (CadÚnico abaixo de 20) e `101e6bf` (revisões externas), ainda abertos por hash
  no github.com. Depois do 404 nos dois, apagar o backup `../backup_analise_primeira_infancia_2026-10-26/`. Falta também
  avisar a equipe para reclonar.

- **Deck Família e Cuidados** — feito em `spec/deck_familia_moradia` (2026-10-07) e nunca mesclado; arquivado na tag
  `rodada/deck_familia_moradia`. Retomar numa rodada própria se a equipe quiser o deck (conflita com o build atual).

- **Curadoria de textos** (contínuo; sem DOCX desde 2026-11-05, tag `rodada/curadoria_docx`): textos do site em
  `relatorio/textos_curados.json` (eixos em `relatorio/textos_eixos.md`, importados por
  `relatorio/curadoria/importa_textos_eixos.py`), texto do PDF editado à mão em `relatorio/latex/capitulos/*.tex`;
  controle em `relatorio/controle_revisao.json`. Sem lorem desde 2026-11-05. Alertas antigos ainda abertos:
  - alertas para a equipe decidir (não corrigidos no texto): mapa de taxa de mortalidade infantil cita os números da
    taxa pós-neonatal; frase das Considerações finais possivelmente sem "não" ("deve atuar de forma isolada"); texto
    da cobertura vacinal anual pronto, mas a figura está fora do relatório (E1); subgrupos < 5 anos cita 198 óbitos
    por atenção ao recém-nascido em 2006 (a tabela tem 204) (o alerta da linha "Total" da SIDRA 10056 foi resolvido
    pela faixa 0 a 5, `specs/2026-09-29_pendencias`);
  - textos marcados `revisar` em `ajustes_manuais`: os 2 com a unidade convertida (2026-09-25) e os 6 ajustados em
    2026-09-29 (faixa 0 a 5, "Não informada", texto herdado do gráfico "PNAD") — lista em
    `specs/2026-09-29_pendencias/validation.md` V13;
  - nota editorial no subgrupo 28-364 dias: "opção de texto que junte tudo por conta da repetição".
- **Apresentação**: os 6 trechos propostos pelo IPP marcados `<!-- revisar -->` em `apresentacao/apresentacao.md`
  (lista em `specs/2026-09-28_apresentacao/validation.md`).
- **Teste do site num iPhone e num Android** (usuário; roteiro em `specs/2026-09-28_website_mobile/validation.md` V7).

## 3. Próximas features

1. **Próxima rodada (spec própria, logo depois da versão final): itens 1 e 3 de `docs/dados_faltantes.csv`**
   (prioridade definida pelo usuário em 2026-11-05):
   - **Item 1 — população de crianças por bairro.** **Estimativa de crianças pequenas por bairro com a Ripsa** (pedido do usuário, 2026-09-24; continuação da
     decisão B1 de `specs/2026-09-24_populacao-referencia`). O Censo 2022 fixo subconta crianças pequenas (0-4:
     310.648 no Censo contra 361.163 na Ripsa em 2022, +16%) e não varia por ano. Estimativa derivada, rotulada
     como tal:
     - **(b)** participação de cada bairro no Censo 2022 × total municipal Ripsa de cada ano, com 0-4 estendido
       para 0-5 pela razão municipal Ripsa; os bairros somam o total Ripsa;
     - **(c)** como (b), com a participação variando no tempo entre os Censos 2010 e 2022 (exige a
       correspondência 160 → 166 bairros).
     Depois recalcular as taxas sub-municipais (violência por bairro/RA/CAP e o % CadÚnico, que depende também do
     item CadÚnico 1) e documentar a mudança de denominador.
   - **Item 3 — cadastros considerados no CadÚnico** (F3, Backlog > CadÚnico item 3): confirmar com o CTPE se a
     silver já exclui cadastros inativos ou desatualizados e, se não, aplicar o filtro e refazer as saídas.
2. **Fontes como referências citáveis e tabelas próprias como fonte de verdade** (pedido do usuário, 2026-11-05;
   antes da fase 1c):
   - Toda tabela e fonte de dados usada (Censo, CadÚnico/CTPE, Tabnet, SISVAN, SIDRA, INEP, Ripsa, Sinan, ISP/Data.Rio,
     cobertura vacinal…) vira uma **referência bibliográfica** citável ao fim do projeto: entrada única (autor/órgão,
     título, ano, data de extração, URL/consulta) em `relatorio/latex/fontes.bib`, reaproveitada pelo site e pelo PDF;
     partir de `relatorio/inventario_fontes.*`.
   - As **tabelas desenvolvidas pelo projeto** (`tabelas_finais/`) também ganham referência própria e ficam prontas para
     **conferir os textos contra elas** como fonte de verdade: cada número citado num texto curado aponta para a
     tabela/célula de origem e é checado por script (estende `website/build/confere_textos.py`).
   - Achado (2026-11-05): `relatorio/latex/build/inventario_fontes.py` atribui fonte por "vizinhança" no `analise.py` e
     dá ISP a 3 tabelas de violência familiar (Sinan) fora do relatório (`tabela_mapa_violencia_familiar_taxa_*`).
3. **Organização do projeto, fase 1c** (continuação de `specs/2026-09-28_organizacao`; regra: mesmas saídas antes e
   depois):
   - **Pastas de dados e saídas**: reorganizar `dados_locais/`, `tabelas_finais/`, `visualizacoes/` e `mapas/`
     (estrutura por fonte/eixo, nomes, as variantes `a4/`; o legado `mapas/tabelas_bairros/` já foi para
     `tabelas_finais/` em 2026-10-26); atualizar os leitores
     (`website/build/build_site.py`, `relatorio/latex/build/`, `relatorio/curadoria/`, `specs/estrutura_eixos.md`,
     skills, `primeira_infancia/`, `apresentacao/build/`).
   - Revisitar a decisão de `specs/2026-09-22_ajuste_eixos` §9.1 (não reordenar fisicamente as seções) agora que as
     funções saíram do arquivo — a ordem continua sendo de dependência de dados.
   - Pré-requisito do item 4.
4. **Empacotar scripts reutilizáveis para outros projetos** (depois do item 3) — transformar em pacotes
   instaláveis o que não é específico da primeira infância: mapa coroplético por bairro/AP/RP/RA com fundo
   cartográfico e rodapé, limpeza de exportações do Tabnet, carga do SIDRA, população Ripsa, gráficos com a
   identidade visual, relatório ABNT em LaTeX a partir de um crosswalk `.md`, round-trip de curadoria em DOCX,
   deck Marp com números calculados. Definir fronteiras, nomes, versionamento e onde publicar (repositório
   próprio, pip via git).
5. **Substituir os dados pontuais do CadÚnico (ref. 08/2026) pela extração automatizada — site feito em 2026-10-06**
   (`specs/2026-10-06_cadunico_inclusao_moradia` D1: Inclusão e Moradia usam as silvers novas; nenhum bloco de dado pontual no site, o bloqueio da versão final
   saiu). Falta o deck e, depois dele, apagar os arquivos listados abaixo. Texto original do item:
   **Bloqueia a versão final do site** (regra D7, constituição §3: sem a faixa "em desenvolvimento" o build e o deploy
   param enquanto houver dado pontual; no PDF ele nunca entra)
   (`specs/2026-09-29_dados_adhoc`, implementada em 2026-09-29 na branch `spec/dados-adhoc`). Hoje Inclusão e Moradia
   mostram, por acréscimo, uma extração pontual (fora do banco CTPE) com o aviso "Dado pontual". Ao substituir:
   levar as mesmas medidas para `analise.py` a partir do banco (com faixa 0 a 5 anos), recalcular, e apagar
   `dados_locais/cadunico/` (planilha, CSV e manifesto `adhoc_2026_08.json` — a lista de tabelas geradas está nele),
   as funções `*_cadunico_adhoc` de `primeira_infancia/cadunico.py`, a célula "📌 Dados pontuais" do `analise.py`, os
   3 itens "(dado pontual, ago/2026)" de `specs/estrutura_eixos.md`, os blocos marcados `dados_adhoc` em
   `website/build/build_site.py`, o slide "Primeiros números de Inclusão e Moradia" do deck, as entradas
   `cadunico_adhoc_*` de `relatorio/latex/build/tabelas.py` e `mds_cadunico_adhoc` de `fontes.bib` (com a
   exclusão `(?!…extração pontual)` do padrão de `mds_cadunico`). Os itens pendentes de Inclusão e Moradia saem de
   pendente quando o dado automatizado cobrir o que o catálogo pede (famílias **com criança** com deficiência, tipo de
   deficiência, inadequação e adensamento).
6. ~~**Tirar a menção ao IPS do site e do relatório**~~ — **feito em 2026-11-05** (citar o ISP — `specs/2026-11-05_fechamento_pendencias` D5; pedido do usuário, 2026-09-29; no deck já feito — D12 de
   `specs/2026-09-29_slide_revision`): na violência territorial (Direito ao Brincar), a fonte passa a citar só o
   Data.Rio, como no deck — `fonte:` em `specs/estrutura_eixos.md`, `fonte_dados` dos 3 mapas em `analise.py` (e as
   versões A4), o texto no `website/build/build_site.py`, a entrada/`padroes` em `relatorio/latex/fontes.bib` e os
   textos curados que citem o IPS (decisão da equipe); depois regerar site, PDF e DOCX.
7. **Skill de mapas exportável** (pedido do usuário, 2026-11-05): transformar a skill `generate_map`
   (`.claude/skills/generate_map/SKILL.md`) numa skill autocontida e exportável para outros projetos -- mapa
   coroplético por bairro/AP/RP/RA/CAP com fundo cartográfico, rosa dos ventos, escala, vizinhos e rodapé, versão de
   tela (PNG) e de impressão (A4/PDF) e mapa de referência só com contornos (como `mapa_referencia_a4` e o mapa da
   Visão geral do site). Inclui o código (hoje em `primeira_infancia/mapas.py` e `impressao.py`), as camadas de
   `dados_locais/geo/` necessárias ou instruções para obtê-las, as convenções do projeto (classes discretas para
   contagem, escala contínua para taxa, sem azul em terra) e um empacotamento para instalar (plugin/skill do Claude
   Code e pacote Python). Anda junto com o item 4 (empacotar scripts reutilizáveis).

## 4. Backlog por tema

### CadÚnico
1. **Geocodificação por bairro oficial** (F1 de `specs/2026-09-23_recortes_cadunico`): o bairro vem do CEP dos
   Correios (`lista_bairros.csv`), que deixa 8,1% das crianças sem bairro e desloca bairros-favela para os
   vizinhos (Maré → Bonsucesso, Rocinha → Gávea; Vila Kennedy/Jabour/Gericinó/Ilha de Guaratiba/Lapa ausentes).
   Refazer por join espacial ou código de bairro do CTPE; só então o mapa "% CadÚnico/Censo" volta ao relatório.
   **2026-10-06:** o CTPE tem a ponte `dim_bridge_ceps_bairros` (CEP → código oficial); já usada nas saídas novas de
   Inclusão e Moradia (`specs/2026-10-06_cadunico_inclusao_moradia` D2). Falta levar as saídas CadÚnico antigas para ela (muda mapas e textos curados).
2. **Pedido ao CTPE** (F2): extração com parentesco/responsável familiar (arranjo real). Deficiência e domicílio
   chegaram nas silvers novas (2026-10-06, `specs/2026-10-06_cadunico_inclusao_moradia`).
3. **Filtro de cadastro da silver** (F3): confirmar com o CTPE se `silver_cadunico_geral` já exclui cadastros
   inativos/desatualizados. **2026-10-06:** a bronze da mesma partição só tem `Cadastrado`/`ativo`, com o mesmo nº de
   pessoas das silvers — confirmar com o CTPE se é filtro da carga.
4. **Cortados por excesso em 2026-10-06** (`specs/exclusoes.md` E17-E19): ajudas recebidas pela pessoa com
   deficiência; formas de abastecimento e escoamento; mapa do déficit e mapas por componente; recortes por idade,
   raça/cor ou renda das variáveis novas.

### Mortalidade
- Séries temporais comparando subgrupos específicos entre regiões ao longo do tempo.
- Mapas comparando subgrupos específicos entre regiões em 2025.
- Mapas para todos os dados com granularidade até bairro.
- Versões por AP/RP (não só bairro) dos indicadores por bairro de `specs/2026-09-09_maps-and-ibge` (nascidos
  vivos, baixo peso, mortalidade neonatal, óbitos por raça, óbitos gravidez/puerpério) — fora do escopo daquela
  rodada, ver seu §7. Considerar `specs/exclusoes.md` (E4, E9) antes.

### Alimentação
Retorno da reunião do eixo Alimentação com a SMS (2026-11-05; itens 5 e 6 de `docs/dados_faltantes.csv`; o item 3 abaixo depende de dados extras):
1. **Baixo peso ao nascer separado da prematuridade**: o baixo peso inclui prematuros; mostrar os dois recortes em
   separado (SINASC). Confirmar o corte: a reunião citou "menores de 36 semanas"; a definição usual é menos de 37
   semanas completas.
2. **Sobrepeso e obesidade pelo IMC por idade e sexo** (SISVAN): a plataforma da SMS classifica pelo IMC por idade
   (idade exata, não faixa) e sexo. Ver se o datalake traz a classificação; se não, calcular a partir de peso e altura
   pelas curvas de referência.
3. ⚠️ **Depende de dados extras** (fora da lista de dados faltantes) — **Amamentação e aleitamento materno por Área de Planejamento** (exclusivo e continuado; pedido do usuário, 2026-11-05): hoje só há o total do município; a equipe técnica de alimentação e
   nutrição da SMS tem os dados por AP e vai fornecê-los — falta fazer o contato.

### Educação
- **Oferta de educação infantil por bairro × crianças e nascimentos** (pedido do usuário, 2026-11-05; amplia o item
  abaixo): por bairro, **matrículas** (creche 0-3 e pré-escola 4-5) e
  **número de creches e pré-escolas** (estabelecimentos do Censo Escolar com essas etapas) comparados ao **número de
  crianças** (Censo 2022 ou a estimativa anual por bairro, Próximas features item 3) e aos **nascimentos** (SINASC,
  nascidos vivos por bairro de residência da mãe — indica a demanda dos próximos anos). Saídas: mapas e tabela de
  matrículas e de creches por mil crianças e por mil nascidos vivos, com a mesma regra de taxa (somar numerador e
  denominador antes de agregar por AP/RP/RA). Depende da geocodificação das escolas (abaixo); eixo Família e Cuidados.
- Mapa de matrículas por bairro, com as escolas geocodificadas (o arquivo do INEP não traz `codbairro`; ver
  `specs/2026-09-24_populacao-referencia/matriculas/specification.md` §4.4).
- Validar 1 ou 2 anos contra a Sinopse Estatística do INEP (pendência P5 da mesma rodada).

### Outros dados
- ⚠️ **Depende de dados extras** (fora da lista de dados faltantes) — **Serviços públicos em camadas GIS** (pedido do usuário, 2026-11-05): localização de
  creches e escolas, unidades de saúde, CRAS, praças e espaços de brincar como camadas sobre os mapas do site (e do PDF), para
  comparar a oferta de serviços com a demanda (crianças, nascimentos, CadÚnico). **Depende de acesso a dados externos**
  (secretarias responsáveis e IPP/Data.Rio); usar a camada de bairros oficial e o código do bairro como chave.
- Levantar e importar bases pendentes (a detalhar): indicadores do catálogo ainda `pendente` em
  `specs/estrutura_eixos.md` (Moradia, deficiência, violência por tipificação, causas evitáveis por sexo).
- Lacunas registradas pela nova estrutura (`specs/2026-09-28_nova_estrutura`): taxa de mortalidade de 1 a 4 anos,
  taxa de violência de todas as naturezas, efeito visual do eixo transversal.

### PDF (`relatorio/latex/`)
- Legendas a partir do inventário/manifesto e remissões "ver Tabela X.n" (T3.3 de `specs/2026-09-25_relatorio_latex`).

### Site (`website/`)
- **"Até 72 meses" e paleta sem azul no site e no PDF** (`specs/2026-09-29_slide_revision` D1, fora daquela rodada):
  ~~paleta~~ feita em 2026-11-05 (`specs/2026-11-05_fechamento_pendencias` R6: `censo` → `Purples`, `natalidade` →
  `Greens`, no site e no PDF); títulos das seções conferidos em 2026-11-06 (`specs/2026-11-05_versao_final_site`
  T8.2); faltam só os títulos dentro das figuras PNG (exige rodar o pipeline).
- **Página "Fale Conosco"** (pedido do usuário, 2026-09-24): rota por hash (`#fale-conosco`) como uma aba,
  acessível pela barra de navegação. Formulário exige backend, que o GitHub Pages não tem — `mailto:` + texto
  (estático) ou serviço externo (exige decisão sobre dados pessoais/LGPD).
- **Tirar a marca d'água do PDF e religar o botão do PDF no site** com a Release do relatório final — decisão do
  usuário (2026-11-05: o site saiu da fase de teste antes do PDF). `relatorio/publicacao.json` →
  `"pdf_em_desenvolvimento": false` e `"link_pdf_no_site": true`, `gera_latex.py --publicar`, Release
  (`publica_release.py`), regerar o site.
- **Logo**: confirmar autorização de uso do logo oficial da Prefeitura/IPP antes do deploy público (T0.4) e pedir
  o SVG oficial à Ascom do IPP (hoje PNG em `srcset`, `specs/2026-09-24_website_refactor` D6).
- **Fontes quase repetidas** na caixa "Fontes desta seção": unificar as constantes `FONTE_*` do gerador.
- Medir formalmente o contraste do rodapé (WCAG AA; T5.6 — só houve inspeção visual).
- Altura da caixa de texto fora do padrão mapa (240 px com rolagem): revisitar quando os textos reais entrarem.
- **Dados por aba com carregamento tardio** e **outliers de mapa como troca de cor**: medidos e deixados de fora
  (`website_refactor` §4.9); voltam se o orçamento de tamanho estourar.
- Botão "baixar tudo"; persistir estado de collapse (localStorage), se pedido; **tema escuro** (removido na v6.2,
  os tokens em `css/main.css` facilitam voltar).
- **Camada própria de água/costa** nos mapas: hoje o mar vem só do tile (Esri Ocean); necessária apenas se um
  dia for preciso colorir o mar por conta própria (`relatorio/specs.md` v6.4-v6.6).

### Repositório (git)
- *Dado do CadÚnico abaixo de 20 no histórico* e *tamanho do histórico*: resolvidos em 2026-10-26 pela reescrita do
  histórico (`specs/2026-10-26_limpeza_historico`, Parte B); PDF, decks e DOCX de curadoria agora vão para a Release do GitHub.
- **Papel da `main`** — decidido em `specs/2026-11-05_versao_final_site` (R8): `main` é o site publicado e
  `staging_main` o ambiente de teste; a `main` só recebe merge de `staging_main` com OK (bloco 9, constituição §7).

### Ideias (sem decisão)
- Substituir a visualização HTML por um painel Streamlit.

---

# Concluído

Resumo; detalhes na pasta da rodada.

| Quando | O quê | Onde |
| :-- | :--- | :--- |
| 2026-11-05 | Fechamento de pendências: SISVAN recalculado das contagens, mapas de número em Moradia, tabelas do CadÚnico no PDF, IPS → ISP, mapas sem azul, 11 textos de Inclusão e Moradia, decks congelados | `specs/2026-11-05_fechamento_pendencias` |
| 2026-10-26 | Histórico do git reescrito (`git filter-repo`): sem o dado do CadÚnico abaixo de 20, `revisao_casa_civil/`, saídas e binários gerados (~740 MB → ~12 MB); hashes citados atualizados; PDF, decks e DOCX na Release do GitHub; link do PDF no site para a última Release | `specs/2026-10-26_limpeza_historico` |
| 2026-10-26 | Limpeza do repositório: 17 branches arquivadas em tags `rodada/*` e apagadas (inclusive `deck_familia_moradia` e a da Waleska, não mescláveis); 131 saídas e `revisao_casa_civil/` fora do git; Excel de `mapas/tabelas_bairros/` em `tabelas_finais/`; `git gc`; reescrita do histórico planejada | `specs/2026-10-26_limpeza_historico` |
| 2026-10-08 | Decks breves de Inclusão, Alimentação e Direito ao Brincar e Moradia (congelados desde 2026-11-05) | tags `rodada/deck_inclusao`, `rodada/deck_alimentacao_brincar`, `rodada/deck_moradia` |
| 2026-10-06 | CadÚnico de Inclusão e Moradia pelas silvers de pessoas/famílias; dados pontuais de ago/2026 fora do site | `specs/2026-10-06_cadunico_inclusao_moradia` |
| 2026-09-30 | Filtro de residência nos 20 exports por bairro do Tabnet (mortalidade infantil 2025: 13,1 → 12,3‰; nascidos vivos 65.507 → 58.700); textos revistos na versão final | `specs/2026-09-30_filtro_residencia_tabnet` |
| 2026-09-30 | Desempenho do site: desenho por aba, tooltip por delegação, fontes próprias (DOM 63,9 mil → 10,4 mil nós; primeira pintura ~430 → ~275 ms) | `specs/2026-09-30_desempenho_site` |
| 2026-09-29 | Versão de demonstração (branch `demo`, só de ida; Pages publicou dela até 2026-11-05) | `specs/2026-09-29_demo` |
| 2026-09-29 | Revisão do deck: 30 → 33 slides, "até 72 meses", 393 mil, mapas sem azul (terracota) e com teto de Tukey, violência familiar por vínculo (sem soma), eixos incompletos/ausentes; faixas de renda do CadÚnico corrigidas para "Pobreza"/"Baixa renda" em todo o projeto | `specs/2026-09-29_slide_revision` |
| 2026-09-29 | PDF alinhado ao site (ordem de Prioridade, vacinação de volta, tabelas no corpo com `tabela_no_texto:`, seção vazia fora — E16); quadros de pendente formais com `motivo:` | `specs/2026-09-29_alinhamento_pdf_site` |
| 2026-09-29 | Pendências: faixa padrão 0 a 5 anos (até 72 meses), exclusões E12-E15, eixo cortado no baixo peso, tablet com as metas do celular, decisões registradas; correção do esquema do banco do CadÚnico | `specs/2026-09-29_pendencias` |
| 2026-09-29 | Decisões de pendências (escopo da rodada atual, mapa duplicado, série "Não informada", base zero, unidade do IPS, Centro só no deck, branch da Waleska superada); regra de perguntas agrupadas pela ferramenta interativa na constituição | este arquivo, `specs/constitution.md` §5 |
| 2026-09-29 | Merge de `spec/nova_estrutura` e `spec/apresentacao` em `planning` e `staging_main` (`149a87f`) e deploy do site | `.github/workflows/deploy-relatorio.yml` |
| 2026-09-28 | Apresentação: deck de 30 slides em Marp com fonte única em Markdown, números calculados de `tabelas_finais/`, variantes por secretaria, PPTX e PDF em `apresentacao/`; mapas com teto P95, Centro como outlier no IPS | `specs/2026-09-28_apresentacao` |
| 2026-09-28 | Nova estrutura: panorama na Introdução (Visão geral no site), 7º eixo Direito ao Brincar, reordenação conforme a planilha da equipe (site, PDF, DOCX); 94 × 94 figuras e 43 × 43 tabelas mantidas | `specs/2026-09-28_nova_estrutura` |
| 2026-09-28 | Git: 15 branches já mescladas apagadas (13 `spec/*`, `ajuste_eixos`, `inclusao_dados_protecao`), cada ponto final preservado numa tag `rodada/<nome>` | `specs/constitution.md` §7 |
| 2026-09-28 | Documentação alinhada ao estado real e especificação funcional/técnica do projeto (`docs/especificacao_projeto.md` e `.docx`); `.env.example` | `specs/2026-09-28_documentacao` |
| 2026-09-28 | Organização do projeto, fases 1a e 1b: pacote `primeira_infancia/`, scripts em `relatorio/curadoria/`, requisitos diretos fixados, 431/431 saídas idênticas | `specs/2026-09-28_organizacao` |
| 2026-09-28 | Rodada A de melhorias: favicon (SVG + `.ico` + apple-touch), abertura de cada eixo, lorem ≤ 150 palavras, só Painéis nos pequenos múltiplos, `index.html` 785 → 343 KB (mapas montados em JS, sprite de ícones); deploy feito | `specs/2026-09-28_melhorias_site` |
| 2026-09-28 | Curadoria: update 5 incorporado (7 textos novos no site e no PDF, 2 órfãos; controle de revisão recalculado sobre as 5 rodadas; updates antigos em `relatorio/textos_updates_antigos/`; scripts `compara_updates.py` e `valida_textos_publicados.py`) | `relatorio/controle_revisao.json`, skill `export_pdf_report` |
| 2026-09-28 | Site mobile (`css/mobile.css`: gráficos na largura real, "Nesta seção", select, legenda abaixo do mapa, toque), mesclado e publicado; marca d'água "EM DESENVOLVIMENTO" no PDF ligada à faixa do site (`relatorio/publicacao.json`) | `specs/2026-09-28_website_mobile` |
| 2026-09-28 | Rollback de `staging_main` e correções do site (cache de CSS/JS, telas estreitas, textos curados ausentes); tabelas de conferência texto × figura; branch corrigido integrado (`66471ff`) | `specs/2026-09-28_website_bugfix` |
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
