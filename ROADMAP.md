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

## 000. Rodada atual — Fechamento de pendências (`specs/2026-11-05_fechamento_pendencias`)

Aberta e implementada em 2026-11-05, antes da versão final do site (`website_release.md`). Feito: % do SISVAN recalculado
das contagens; mapas de número em Moradia (PNG, A4, site, PDF); tabelas do CadÚnico de Inclusão e Moradia no PDF; "IPS"
→ ISP-RJ nas citações da violência territorial; mapas sem azul (`censo` → `Purples`, `natalidade` → `Greens`); 11 textos
novos de Inclusão e Moradia (aprovados pelo usuário). Decidido: CadÚnico fica na silver de jul/2026 (a diferença com o
dado pontual de ago/2026 deixa de bloquear); **decks congelados** (não são mais mantidos). Falta: merge em
`staging_main` com OK. **Não** vai para a `demo` nem para deploy.

Ficou para a **rodada da versão final** (achados de 2026-11-05):
1. **DOCX de curadoria de hoje** (`relatorio/curadoria_textos_05_11_26.docx`, volta do Google Docs, sem bookmarks):
   `incorpora_update_docx.py` casa 92 textos (31 de blocos ainda sem texto, 28 editados pela equipe) e deixa 54
   parágrafos com texto real sem casar (CadÚnico por sexo/raça/arranjo, violência territorial, mapas de mortalidade,
   muitos marcados "✏️ aguardando correção"). Vários números estão desatualizados (ex.: 194.138 crianças de jun/2026
   contra 200.784 de jul/2026; 773 óbitos infantis contra 724 nos dados) — conferir cada número antes de incorporar.
2. ~~**Lorem que sobra**~~ — **resolvido em 2026-11-05** (`specs/2026-11-05_versao_final_site` T1.1-T1.4): textos da
   curadoria de 05/11 conferidos, abas sem arquivo com chave e texto próprios, 21 textos de eixo; site e PDF sem lorem.
3. Textos curados com "0 a 5 anos" → "até 72 meses" (D10 de `2026-10-06_cadunico_inclusao_moradia`) e títulos das PNG.

## 0a. Filtro de residência nos exports por bairro do Tabnet (`specs/2026-09-30_filtro_residencia_tabnet`)

Aberta e implementada em 2026-09-30: os 20 exports por bairro do SIM/SINASC (Tabnet SMS-Rio) vinham sem o filtro de
município de residência (entravam não residentes). Reextraídos com `extrai_tabnet.py`; tabelas, site, PDF, deck e 22
textos curados atualizados (mortalidade infantil 2025: 13,1 → 12,3‰; nascidos vivos 65.507 → 58.700). Falta: revisão
dos textos pela equipe (status "atualizado").

## 0b. Desempenho do site (`specs/2026-09-30_desempenho_site`) — concluída em 2026-09-30

Desenho por aba (gráficos e mapas de abas fechadas nascem ao abrir ou no tempo ocioso), tooltip de mapa por delegação,
fontes servidas pelo próprio site. DOM no carregamento 63,9 mil → 10,4 mil nós; primeira pintura ~430 → ~275 ms.
Pendente (achado): deep link de Alimentação/SISVAN termina sob a barra fixa (já acontecia antes).

## 0. Rodada em planejamento — versão de demonstração (`specs/2026-09-29_demo`, branch `spec/demo` → `demo`)

Planejada em 2026-09-29 (D1-D11). É uma branch `demo`, exclusiva e só de ida, com texto provisório no lugar do lorem,
pendentes ocultos, faixa maior com a V.1 prevista para **6/10/2026**, PDF até a página impressa 18 mais o aviso, e o
Pages publicando a partir dela. Falta o OK do usuário para implementar. A troca da branch do ambiente `github-pages` é
manual.

## 1. Rodada atual — pendências (`specs/2026-09-29_pendencias`, branch `spec/pendencias`)

**Implementada em 2026-09-29** (decisões D1-D18, validação V1-V14 em `validation.md`): mapa duplicado fora (E13),
"Não informada" fora da taxa (E14), baixo peso com eixo cortado (única exceção à base zero), **faixa padrão 0 a 5 anos**
(Censo, Ripsa, taxas de frequência do IBGE agregadas por taxa × população; títulos "até 72 meses"; deck com 393 mil),
amarela e indígena só no total (E12), gráfico "PNAD" que era o Censo 2022 substituído (E15), tablet com alvos de 44 px e
gráficos na largura real, unidade do IPS confirmada, Centro como outlier só no deck, rodadas anteriores fechadas.

Falta só o que depende do **OK do usuário**:
1. Publicar o PDF (`gera_latex.py --publicar`; o publicado ainda é o de `specs/2026-09-28_melhorias_site`), fazer o
   deploy do site (`deploy-relatorio.yml`) e publicar o deck (`gera_apresentacao.py --publicar`), ainda com a marca
   "em desenvolvimento".
2. ~~Tags e branches mescladas~~ — feito em 2026-10-26 (`specs/2026-10-26_limpeza_historico`).

## 2. Aguardando equipe/usuário

Não dependem de código; entram no projeto quando chegarem.

- **Pedido ao GitHub Support** (`specs/2026-10-26_limpeza_historico/pedido_github_support.md`, passo a passo e mensagem prontos): remover o
  cache dos commits antigos `cdfacd2` (CadÚnico abaixo de 20) e `101e6bf` (revisões externas), ainda abertos por hash
  no github.com. Depois do 404 nos dois, apagar o backup `../backup_analise_primeira_infancia_2026-10-26/`. Falta também
  avisar a equipe para reclonar.

- **Deck Família e Cuidados** — feito em `spec/deck_familia_moradia` (2026-10-07) e nunca mesclado; arquivado na tag
  `rodada/deck_familia_moradia`. Retomar numa rodada própria se a equipe quiser o deck (conflita com o build atual).

- **Curadoria de textos** (contínuo; DOCX `relatorio/curadoria_textos.docx`, controle em
  `relatorio/controle_revisao.json`; updates antigos em `relatorio/textos_updates_antigos/`). Última rodada:
  update 5 (2026-09-28). Próximo update: baixar a partir do `relatorio/curadoria_textos.docx` atual (o update 5
  partiu do update 4 e por isso ainda trazia textos já corrigidos depois).
  - ainda em lorem ipsum: resumo, principais achados e síntese de cada eixo, abertura de cada eixo
    (`introducao_<eixo>`) e textos de figura (a lista sai no build: `gera_latex.py` imprime "textos em lorem");
  - alertas para a equipe decidir (não corrigidos no texto): mapa de taxa de mortalidade infantil cita os números da
    taxa pós-neonatal; frase das Considerações finais possivelmente sem "não" ("deve atuar de forma isolada"); texto
    da cobertura vacinal anual pronto, mas a figura está fora do relatório (E1); subgrupos < 5 anos cita 198 óbitos
    por atenção ao recém-nascido em 2006 (a tabela tem 204) (o alerta da linha "Total" da SIDRA 10056 foi resolvido
    pela faixa 0 a 5, `specs/2026-09-29_pendencias`);
  - textos marcados `revisar` em `ajustes_manuais`: os 2 com a unidade convertida (2026-09-25) e os 6 ajustados em
    2026-09-29 (faixa 0 a 5, "Não informada", texto herdado do gráfico "PNAD") — lista em
    `specs/2026-09-29_pendencias/validation.md` V13;
  - nota editorial no subgrupo 28-364 dias: "opção de texto que junte tudo por conta da repetição".
  - **tabelas no corpo sem bloco no DOCX** (achado de `specs/2026-09-29_dados_adhoc`): os textos das tabelas
    `tabela_no_texto` (`cadunico_razao_populacao_0_a_5_2026` e as 4 `cadunico_adhoc_*`) saem em lorem no site e no PDF,
    mas `gera_docx_curadoria.py` só cria bloco de texto para figuras — a equipe não tem onde escrevê-los.
- **Apresentação**: os 6 trechos propostos pelo IPP marcados `<!-- revisar -->` em `apresentacao/apresentacao.md`
  (lista em `specs/2026-09-28_apresentacao/validation.md`).
- **Teste do site num iPhone e num Android** (usuário; roteiro em `specs/2026-09-28_website_mobile/validation.md` V7).

## 3. Próximas features

1. **Fontes como referências citáveis e tabelas próprias como fonte de verdade** (pedido do usuário, 2026-11-05;
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
2. **Organização do projeto, fase 1c** (continuação de `specs/2026-09-28_organizacao`; regra: mesmas saídas antes e
   depois):
   - **Pastas de dados e saídas**: reorganizar `dados_locais/`, `tabelas_finais/`, `visualizacoes/` e `mapas/`
     (estrutura por fonte/eixo, nomes, as variantes `a4/`; o legado `mapas/tabelas_bairros/` já foi para
     `tabelas_finais/` em 2026-10-26); atualizar os leitores
     (`website/build/build_site.py`, `relatorio/latex/build/`, `relatorio/curadoria/`, `specs/estrutura_eixos.md`,
     skills, `primeira_infancia/`, `apresentacao/build/`).
   - Revisitar a decisão de `specs/2026-09-22_ajuste_eixos` §9.1 (não reordenar fisicamente as seções) agora que as
     funções saíram do arquivo — a ordem continua sendo de dependência de dados.
   - Pré-requisito do item 4.
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
4. **Empacotar scripts reutilizáveis para outros projetos** (depois do item 2) — transformar em pacotes
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
Retorno da reunião do eixo Alimentação com a SMS (2026-11-05; itens 13 a 15 de `docs/dados_faltantes.csv`):
1. **Baixo peso ao nascer separado da prematuridade**: o baixo peso inclui prematuros; mostrar os dois recortes em
   separado (SINASC). Confirmar o corte: a reunião citou "menores de 36 semanas"; a definição usual é menos de 37
   semanas completas.
2. **Sobrepeso e obesidade pelo IMC por idade e sexo** (SISVAN): a plataforma da SMS classifica pelo IMC por idade
   (idade exata, não faixa) e sexo. Ver se o datalake traz a classificação; se não, calcular a partir de peso e altura
   pelas curvas de referência.
3. **Aleitamento materno por Área de Planejamento**: hoje só há o total do município; a equipe técnica de alimentação e
   nutrição da SMS tem os dados por AP e vai fornecê-los — falta fazer o contato.

### Educação
- Mapa de matrículas por bairro, com as escolas geocodificadas (o arquivo do INEP não traz `codbairro`; ver
  `specs/2026-09-24_populacao-referencia/matriculas/specification.md` §4.4).
- Validar 1 ou 2 anos contra a Sinopse Estatística do INEP (pendência P5 da mesma rodada).

### Outros dados
- Levantar e importar bases pendentes (a detalhar): indicadores do catálogo ainda `pendente` em
  `specs/estrutura_eixos.md` (Moradia, deficiência, violência por tipificação, causas evitáveis por sexo).
- Lacunas registradas pela nova estrutura (`specs/2026-09-28_nova_estrutura`): taxa de mortalidade de 1 a 4 anos,
  taxa de violência de todas as naturezas, efeito visual do eixo transversal.

### PDF (`relatorio/latex/`)
- Legendas a partir do inventário/manifesto e remissões "ver Tabela X.n" (T3.3 de `specs/2026-09-25_relatorio_latex`).

### Site (`website/`)
- **"Até 72 meses" e paleta sem azul no site e no PDF** (`specs/2026-09-29_slide_revision` D1, fora daquela rodada):
  ~~paleta~~ feita em 2026-11-05 (`specs/2026-11-05_fechamento_pendencias` R6: `censo` → `Purples`, `natalidade` →
  `Greens`, no site e no PDF); falta só conferir os títulos que ainda dizem "0 a 5 anos".
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
- **Papel da `main`** — muito atrás de `staging_main` (a branch padrão) e nunca recebeu as rodadas. Proposta: usá-la
  como branch de versão e mesclar `staging_main` nela quando `relatorio/publicacao.json` passar para a versão final;
  alternativa: aposentá-la.

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
