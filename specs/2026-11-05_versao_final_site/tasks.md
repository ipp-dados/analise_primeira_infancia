# TASKS — Versão final do site (rodada de 2026-11-05)

Legenda: [x] feito · [ ] a fazer. Pedido original: `initial_prompt.md` (nesta pasta; era `website_release.md` na raiz). A especificação e o plano completos
(banner, mapa de referência, rodapé, faixa beta, relatório, `main`) vêm no planejamento desta rodada.

## Bloco 1 — Textos
- [x] T1.1 Textos da curadoria de 05/11 (DOCX) conferidos e importados (36; `textos_docx_05_11_revisao.md`)
- [x] T1.2 Textos das 19 abas sem arquivo (17 chaves; `textos_abas_propostos.md`)
- [x] T1.3 Textos dos eixos (achados, introdução, síntese) em `relatorio/textos_eixos.md`: 9 escritos pelo usuário (Prioridade, Inclusão, Família e Cuidados; corrigidos contra os dados) e 12 propostos e aprovados (Proteção, Brincar, Alimentação, Moradia; `textos_eixos_propostos.md`); importados com `relatorio/curadoria/importa_textos_eixos.py`. Site e PDF sem lorem;
      importar e conferir os números citados
- [x] T1.4 **Dividir a Introdução da Visão geral** (pedido do usuário, 2026-11-05): abertura de 1 parágrafo (resumo do
      1º parágrafo atual) no início da aba e, no fim da aba, a seção **"Notas sobre o projeto e metodologia"** com até
      2 parágrafos (resumo dos parágrafos 2 a 4). Chaves: `introducao` (abertura) e `notas_projeto_metodologia`
      (fechamento). Conferir também o capítulo de Introdução do PDF, que lê a mesma chave `introducao`.

## Bloco 2 — Dados faltantes e plano para gestores
- [x] T2.1 Lista de todos os dados faltantes (pedido do usuário, 2026-11-05): `docs/dados_faltantes.csv` — 12 itens: os
      3 `status: pendente` do crosswalk (o aviso de pendência em Prioridade e os dois de Proteção) e 9 lacunas do
      ROADMAP e de `specs/exclusoes.md`
- [x] T2.2 Documento para gestores (Claude Docs, "Diagnóstico da Primeira Infância — dados faltantes e plano de
      entrega"): situação das entregas, tabela dos 12 itens com situação e prioridade editáveis, plano em 3 fases e
      2 portas (sem datas: a definir pelos gestores), pedidos e decisões
- [x] T2.2b Itens 13 a 15 (reunião do eixo Alimentação com a SMS, 2026-11-05) na lista, no documento e no ROADMAP
- [ ] T2.3 Manter a lista e o documento em dia quando um item mudar (pedido feito, dado recebido)

## Bloco 3 — Banner e rodapé
- [x] T3.1 Foto do Unsplash (Compagnons, @sigmund, Licença da Unsplash) recortada e comprimida por `website/build/gera_banner.py` (960 px 20 KB, 1600 px 45 KB); crédito com links no banner
- [x] T3.2 Banner novo: foto à direita com máscara (sem emenda), texto e botões legíveis; celular com a foto bem esmaecida e o crédito no alto; site 1,49 MB
- [x] T3.3 E-mail de contato fora do rodapé (2026-11-05)
- [x] T3.4 Links do banner e do rodapé conferidos (HTTP 200); Transparência Rio trocado para transparencia.prefeitura.rio (o antigo estava quebrado); Unsplash responde 401 só a scripts

## Bloco 4 — Mapa de referência
- [x] T4.1 Mapa de referência na Visão geral (`mapa_referencia_html()` em `build_site.py`): bairros, RA e AP como contornos da geometria compartilhada, botões de nomes por camada (`initMapaReferencia` em `js/charts.js`), tooltip do bairro com RA e AP; nomes das RA com acento em todos os mapas de RA (`_NOME_RA`)
- [x] T4.2 CSV bairro → RA → AP no botão do cartão
- [x] T4.3 Figura A4 `mapas/a4/mapa_referencia_bairros_ra_ap.pdf` (`mapa_referencia_a4` em `primeira_infancia/impressao.py`, chamada na seção Censo do `analise.py`); entra no capítulo de Introdução no Bloco 5

## Bloco 5 — PDF em `.tex` por capítulo, capa e folha de rosto
- [x] T5.1 PDF de referência guardado antes da exportação (174 páginas)
- [x] T5.2 `gera_latex.py --exportar-capitulos`: 9 arquivos em `relatorio/latex/capitulos/`, resumo em `pretextual/resumo.tex`, tabelas no corpo em `gerado/tabelas_corpo/`; `relatorio.tex` com `\input{capitulos/...}`; nas execuções normais o script não escreve mais capítulos
- [x] T5.3 `confere_capitulos()`: figuras, tabelas no corpo e rótulos de tabela citados existem (a execução para se faltar algo)
- [x] T5.4 Mesmo texto do PDF de referência (só quebras de linha na Introdução, pelo mapa novo); 174 páginas
- [x] T5.5 Capa, folha de rosto e expediente novos: estilo do projeto com os elementos dos relatórios técnicos do IPP no Data.Rio (bloco institucional, "IPP · NOVEMBRO | 2026", logo; expediente com direção e equipe -- prefeito Eduardo Cavaliere); imagens por `relatorio/latex/build/gera_capa_imagens.py`

## Bloco 6 — Curadoria só do site, sem DOCX
- [x] T6.1 Tag `rodada/curadoria_docx`; apagar os scripts DOCX (+ `valida_textos_publicados.py`, que dependia do fluxo DOCX)
- [x] T6.2 `confere_textos.py` sem DOCX
- [x] T6.3 Skills, `CLAUDE.md`, especificação do projeto

## Bloco 7 — Release e Actions
- [x] T7.1 Instalar o `gh` (v2.103.3, `C:\Program Files\GitHub CLI\gh.exe`; o terminal antigo não tem no PATH) e `gh auth login` (conta leoaucar)
- [x] T7.2 Passo de publicação da Release (`relatorio/latex/build/publica_release.py`: ensaio por padrão, `--gerar`, `--confirmar`)
- [x] T7.3 Deploy automático na `main`; workflow de checagem em `staging_main` (`confere-site.yml`; checagens em `website/build/confere_publicacao.py`)
- [x] T7.4 (D13) `publicacao.json` separado em site/PDF; faixa do site desligada; botão do PDF escondido

## Bloco 8 — Versão final, revisão e teste
- [x] T8.1 `publicacao.json`: site `false`, PDF segue `true`, botão do PDF escondido (D13) -- feito em 031dddc
- [x] T8.2 Revisão de pipelines e documentação; títulos "até 72 meses"
  - [x] 2026-11-06: 4 títulos fora do catálogo "0 a 5 anos" → "até 72 meses" (CadÚnico ÷ população, matrículas,
    taxa de atendimento, violência familiar) no crosswalk, nos `\section` dos capítulos 01/03/04 e em
    `textos_eixos.md` (o site já usava "até 72 meses"); faixa conferida nos dados: CadÚnico com `assert` 0-5,
    INEP `QT_MAT_BAS_0_3`+`_4_5`, Sinan exportado com "menor de 01 ano ... 05 anos", populações Ripsa 0-5.
    Corpo e legendas seguem "0 a 5 anos"; o título da mortalidade (menores de 1, 1-4, 0-5) fica, é recorte etário
  - [x] 2026-11-06: `basemap-f5a7b7b6.jpg` (órfão, idêntico ao usado; bbox antiga do mapa por CAP) removido;
    `build_site.py` apaga `basemap-*.jpg` não usados no build
  - [x] 2026-11-06: Actions nos majors atuais (Node 24): checkout v7, setup-python v7, configure-pages v6,
    upload-pages-artifact v5, deploy-pages v5 -- conferir no próximo run
  - [x] 2026-11-06: `staging_main` local alinhada (fast-forward) com `origin/staging_main`
  - [x] 2026-11-06: números do CadÚnico da partição de junho nas notas internas → partição 2026-07-10 (crosswalk:
    fonte jul/2026 e razão 200.784 ÷ 393.073 ≈ 51,1%; `analise.py`: 16.378 sem bairro, 8,2%). Site e PDF já estavam
    certos; as notas históricas de jun/2026 (grupo `'0-6'`, 713 famílias sem adulto) ficam como registro datado
  - [x] 2026-11-06: documentação conferida contra o que existe (caminhos citados checados um a um). Corrigido: deploy
    descrito como "só manual" (`CLAUDE.md`, `docs/especificacao_projeto.md` §9.4, skill `build_website`) → automático
    na `main` + manual, conferência na `staging_main`, deploy pela `staging_main` até o T9.5; nota da skill
    `generate_map` que citava `relatorio/index.html`/`build_html_report.py`; §12 da especificação (lorem) e data do
    topo; `ROADMAP.md` com esta rodada como atual, rodadas de 09-30 a 10-08 no Concluído, curadoria sem DOCX, papel
    da `main` decidido. `README.md` e `website/README.md` sem pendência (citações antigas são histórico)
  - [x] Pipelines: sem rodar (dados congelados, pedido do usuário em 2026-11-06); `confere_publicacao.py` e
    `confere_textos.py` passam sobre o `website/` versionado. O PDF não foi recompilado: as tabelas do apêndice pegam
    os 4 títulos novos do crosswalk no próximo build
  - [x] 2026-11-06: conferência de todos os números dos 163 textos do site contra `tabelas_finais/` (somente leitura;
    somas por AP/RP/CAP, faixas e taxas recalculadas). Corrigido com OK do usuário: `consideracoes_finais` e cap. 08
    ("não deve atuar de forma isolada"); `mapa_taxa_mortalidade_infantil_bairro_2025` (números antigos → texto do
    PDF); "167 bairros" → 165 (as linhas 998/999 são IGNORADO) em `mapa_mortalidade_infantil_bairro_2025`,
    `mapa_obitos_raca_total_bairro_2025` (37 → 35 sem óbito) e `mapa_obitos_pos_neonatal_bairro_2025` (75 → 73);
    baixo peso por bairro (site e cap. 06: "entre 6,7% e 28,6%" era P10-máximo → quartis 8,7-11,7%, mediana 10,2%,
    4 bairros acima de 20%); `evitaveis_cap_menores_1_gestacao` "total da cidade" → "soma das CAPs". Três dessas
    chaves não aparecem no site (só JSON/PDF). Site regerado uma vez: diferença só nesses textos e na data
- [x] T8.3 Teste completo desktop e celular (2026-11-06; V10, scripts e resultado em `teste_t83/`). Achados menores:
  crédito da foto pouco legível sobre a imagem no desktop; SIDRA e Unsplash só conferíveis à mão (bloqueiam robôs)

## Bloco 9 — Publicação (com OK)
- [x] T9.1 Merge em `staging_main` (5ce5a4f); tag `rodada/versao_final_site` (2026-11-06)
- [x] T9.2 `staging_main` → `main` (fast-forward até 5ce5a4f); deploy conferido pela API (2026-11-06): as 4 primeiras tentativas falharam do lado do GitHub (`deployment_queued` → `deployment_failed`, também pela `staging_main` e com as versões antigas das actions); a 5ª, ~20 min depois, publicou
- [x] T9.3 Release do PDF `v0.35.0` (Latest, PDF ainda EM DESENVOLVIMENTO; botão do site segue desligado); link `releases/latest/download/...` conferido (200, 16,6 MB)
- [x] T9.4 Constituição §7 e `CLAUDE.md` (2026-11-06: `main` = site publicado, `staging_main` = teste, `main` só com merge de `staging_main` e OK; `demo` não é mais publicada; skill `build_website`, especificação §9.4, README/CHANGELOG 0.35.0)
- [x] T9.5 (2026-11-06, ajustes manuais feitos pelo usuário: `main` permitida no ambiente, Pages por "GitHub Actions"; falta só tirar `demo` e `staging_main` das branches permitidas) Trocar a fonte do GitHub Pages da `staging_main` para a `main` (decisão do usuário, 2026-11-05: **por ora o
  site publica pela `staging_main`**, deploy manual -- `gh workflow run deploy-relatorio.yml --ref staging_main`).
  Na hora: incluir `main` nas branches permitidas do ambiente `github-pages` (Settings → Environments), passar
  Settings → Pages → Source para "GitHub Actions" (hoje `legacy` com fonte `demo`), tirar `demo` e `staging_main` das
  permitidas, e conferir o primeiro deploy automático por push na `main`

## Estado em 2026-11-05 (fim da sessão) -- retomar daqui

- Branch `spec/versao_final_site` no `origin`; `staging_main` avançada (fast-forward) até 031dddc; tag
  `rodada/curadoria_docx` no `origin`. `main` intocada (ainda no commit antigo `e6d2a16`).
- **Site publicado** a partir da `staging_main` (decisão do usuário: deploy pela `staging_main` antes do bloco 8) --
  run 42105224110 ok; deployment de 031dddc às 20:38 UTC. github.io não abre da rede do IPP (HTTP 000): conferir de
  outro lugar.
- GitHub Pages: `build_type: legacy` com fonte `demo` + deploys por Actions; o ambiente `github-pages` só aceita
  `demo` e `staging_main` -- no bloco 9, incluir `main` (Settings → Environments) e passar o Pages para "GitHub
  Actions"; a `demo` deixa de ser publicada.
- Actions: avisos de Node 20 em `configure-pages@v5`/`deploy-pages@v4`/`upload-artifact` (ainda funcionam) --
  atualizar quando houver versão nova.
- Capas A e D seguem juntas em `pretextual/capa.tex` (usuário escolhe depois); nomes completos da equipe técnica
  (só Leonardo Nogueira Aucar está completo) ainda pendentes.
- `basemap-*.jpg`: o gerador regrava o fundo do mapa com hash novo a cada build (dois arquivos versionados, um
  sem uso) -- tornar determinístico e apagar o órfão no bloco 8.
- **Próximo: bloco 8** (T8.2 revisão de pipelines/documentação e títulos "até 72 meses"; T8.3 teste completo desktop
  1366 e celular 390 com Playwright/Edge), depois **bloco 9** só com OK (merge, `main`, Release com
  `relatorio/latex/build/publica_release.py vX.Y.Z --gerar` e depois `--confirmar`, constituição §7).

## Estado em 2026-11-06 -- retomar daqui

- Bloco 8 concluído (T8.1-T8.3) na `spec/versao_final_site`; dados e pipeline congelados (nada de `analise.py`). O
  pedido original foi para esta pasta como `initial_prompt.md`.
- Ainda não enviado ao `origin` nem mesclado: **próximo é o bloco 9, só com OK** (T9.1 merge em `staging_main` + tag
  `rodada/versao_final_site`; T9.2 `staging_main` → `main`; T9.3 Release do PDF; T9.4 constituição §7; T9.5 Pages
  pela `main`, com os ajustes manuais nas configurações do GitHub).
- Conferir à mão os links do SIDRA e do Unsplash (bloqueiam robôs) e, se quiser, o contraste do crédito da foto.

## Estado em 2026-11-06 (fim do bloco 9)

- Site publicado pela `main` (5ce5a4f) e PDF na Release `v0.35.0`. A `staging_main` está à frente da `main` só com
  o item do ROADMAP (outro host estático) e duas trocas de versão das actions do Pages (idas e voltas do diagnóstico,
  workflow igual ao da `main`); vão para a `main` na próxima publicação.
- A tag `rodada/versao_final_site` marca d7b9aa5 (fim do T9.4); os commits seguintes são do diagnóstico do deploy.
- Pendente do usuário: tirar `demo` e `staging_main` das branches permitidas do ambiente `github-pages`; conferir o
  site de fora da rede do IPP (github.io bloqueado aqui); clicar os links do SIDRA e do Unsplash.
