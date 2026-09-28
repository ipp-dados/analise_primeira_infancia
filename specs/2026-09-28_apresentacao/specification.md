# SPEC — Apresentação de 30 slides (Marp, fonte única em Markdown)

Rodada aberta em 2026-09-28 no branch `planning`. Insumo: `presentation_readme.md` (nesta pasta).
Implementação em `spec/apresentacao` (o readme sugere `feature/presentation-spec-and-template`; segue-se o
padrão `spec/<nome>` da constituição §7), **depois** de `specs/2026-09-28_nova_estrutura`: a parte temática
dos slides segue a Introdução/panorama e os 7 eixos dessa rodada.

## 1. Objetivo

Deck de 30 slides (45 min) sobre o hub de dados da primeira infância carioca (IPP), com três metas:
1. mostrar a arquitetura de dados, o retrato da cidade, os limites de método e os produtos (site e PDF);
2. chamar as secretarias para compartilhar e integrar dados primários;
3. muito visual: mapas, gráficos, números grandes, pouco texto.

E um **mecanismo de variantes**: uma versão derivada (outro público ou secretaria) sai de editar um único
arquivo Markdown.

## 2. Decisões

| # | Decisão | Por quê |
|---|---|---|
| A1 | **Marp** (`@marp-team/marp-cli`, versão fixada em `apresentacao/package.json`) | Markdown puro com frontmatter; exporta PDF, PPTX e HTML; tema em CSS. Node 24 já instalado. Escolha do usuário (2026-09-28) |
| A2 | Pré-processador em Python (`apresentacao/build/gera_apresentacao.py`) antes do Marp | o Marp não tem condicionais nem variáveis; o projeto já é Python e os números vêm de `tabelas_finais/` |
| A3 | Números dos destaques calculados das tabelas (`{{n:chave}}`), nunca digitados | a mesma regra de "edite o gerador, não o gerado" (constituição §4); o deck se atualiza com os dados |
| A4 | Figuras = PNGs de `visualizacoes/` e `mapas/` (as mesmas do `analise.py`) | uma só fonte visual; o PDF A4 é vetorial, mas o Marp embute melhor PNG |
| A5 | Identidade: azul IPP `#004a80`, ciano `#00aeef`, logo `website/assets/images/ipp-logo.png`, paleta de dados `--c1..--c11` do site | é a identidade já aplicada no site; se houver manual/modelo oficial do IPP (Q1), ele substitui |
| A6 | Idioma pt-BR; títulos de slide como frases de achado ("A cidade tem 469 mil crianças de 0 a 6 anos"), não rótulos | público não técnico (constituição §1) |
| A7 | Saídas em `apresentacao/_build/` (gitignored); só `--publicar` copia `apresentacao/apresentacao_primeira_infancia.pdf` (versionado) | mesmo padrão do PDF do relatório |
| A8 | Regra do usuário: acrescentar o que falta, nunca remover o que sobra | vale para a relação deck × site/PDF: o deck resume, não substitui nada |

## 3. Arquitetura

```
apresentacao/
  apresentacao.md            # fonte única do deck (frontmatter + slides); editar só este arquivo
  variantes/                 # cópias derivadas (ex. secretaria_saude.md), mesmo formato
  tema/ipp.css               # tema Marp (/* @theme ipp */), layouts por classe
  build/gera_apresentacao.py # pré-processa e chama o marp-cli
  build/numeros.py           # chave -> valor formatado pt-BR, calculado de tabelas_finais/
  package.json               # marp-cli fixado; `npm ci` na primeira vez
  README.md                  # como editar, gerar e derivar
  _build/                    # gitignored: .md resolvido, imagens copiadas, QR, PDF/PPTX/HTML
```

### 3.1 Formato de `apresentacao.md`

```markdown
---
marp: true
theme: ipp
paginate: true
titulo: Diagnóstico da Primeira Infância Carioca
subtitulo: Um hub de dados para a política integrada
publico: secretarias            # secretarias | gabinete | tecnico | <nome>
secretaria: ""                  # ex. "Secretaria Municipal de Saúde" -> personaliza capa e chamada
data: 2026-10-XX
blocos: [cooperacao, governanca, demo]   # blocos opcionais ligados
url_site: https://ipp-dados.github.io/analise_primeira_infancia/
---

<!-- _class: capa -->
# {{titulo}}
## {{subtitulo}}
{{secretaria}} · {{data}}

---
<!-- _class: numero -->
# {{n:pop_0_6_ripsa_2025}}
crianças de 0 a 6 anos no Rio ({{n:pct_0_6_ripsa_2025}} da população, 2025)

<!-- se: cooperacao -->
---
...
<!-- /se -->

<!-- se: publico=saude -->
...
<!-- /se -->
```

Regras do pré-processador:
- `{{campo}}` = campo do frontmatter; `{{n:chave}}` = número de `numeros.py`. Chave inexistente = **erro**, e o
  build para (nunca um slide com placeholder).
- `<!-- se: bloco -->…<!-- /se -->` entra se `bloco` está em `blocos`; `se: publico=x` compara com `publico`.
- `![bg right:45%](fig:mapa_censo_0_4_absoluto)` resolve para o PNG em `mapas/` ou `visualizacoes/` e copia para
  `_build/img/`. Figura inexistente = erro.
- `{{qr:url_site}}` gera o QR (biblioteca `segno`, pura Python, dependência nova em `requirements-dev.txt`).
- Variante = copiar `apresentacao.md` para `variantes/<nome>.md` e mudar o frontmatter e os blocos:
  `python apresentacao/build/gera_apresentacao.py variantes/secretaria_saude.md`.

### 3.2 Layouts do tema (classes Marp)

`capa`, `secao` (divisor de parte), `numero` (1 número grande + legenda), `numeros` (3-4 números lado a lado),
`mapa` (mapa em tela cheia à direita + 1-2 frases), `grafico` (gráfico largo + frase de achado), `dois-mapas`,
`lista-curta` (até 4 itens), `qr`, `encerramento`. Rodapé automático com a fonte (`<!-- fonte: … -->` em cada
slide de dado vira o rodapé; sem fonte = aviso no build, constituição §3).

## 4. Roteiro slide a slide (30)

Números entre `{{ }}`: valores atuais calculados em 2026-09-28, só para planejar (o build os recalcula).

### Parte I — Contexto e chamada (1-6)
| # | Título (achado) | Layout | Conteúdo / figura | Fonte |
|---|---|---|---|---|
| 1 | Diagnóstico da Primeira Infância Carioca | capa | logo IPP, faixa de cores do site, secretaria e data (variante) | — |
| 2 | Por que um diagnóstico da primeira infância | lista-curta | apoio à Política Integrada da Primeira Infância; 0-6 anos; nível intramunicipal | texto `introducao` |
| 3 | Um hub único de dados | grafico | diagrama das fontes → `analise.py` → site/PDF (desenho novo, SVG no tema) | inventário de fontes |
| 4 | O que dados secundários não respondem | lista-curta | registro administrativo ≠ pesquisa; Censo esporádico; sem causalidade; Zika/Covid/recessão | texto `introducao` |
| 5 | Chamada: cada secretaria tem um pedaço do retrato | numeros | nº de indicadores pendentes por eixo (Inclusão 3/3, Moradia 3/3, Proteção 2, …) | `estrutura_eixos.md` |
| 6 | Governança e integração | lista-curta | chaves comuns (código de bairro), qualidade das fontes, privacidade (supressão < 20) | constituição §3/§6 |

### Parte II — Panorama e método (7-20)
| # | Título | Layout | Conteúdo / figura |
|---|---|---|---|
| 7 | O território é a unidade de análise | mapa | `mapa_censo_0_4_absoluto` (166 bairros) |
| 8 | Bairro, AP, RP, RA e CAP: recortes diferentes | dois-mapas | bairros × CAP (`mapa_obitos_evitaveis_menores_5_anos_cap_2025` ou mapa só de limites) |
| 9 | Quantas crianças? Duas fontes | numeros | Censo 2022 0-4: {{307.734}}; Ripsa 2025 0-6: {{469.148}} |
| 10 | Por que Ripsa no município e Censo nos bairros | grafico | `populacao_ripsa_0_a_6_por_ano` + nota de subcontagem do Censo |
| 11 | O CadÚnico não é a população | numero | {{49,4%}} das crianças de 0-5 estão no CadÚnico ({{194.138}} de {{393.073}}) |
| 12 | Quem está no CadÚnico | grafico | `cadunico_familias_por_faixa_renda` (viés de renda; não representa a cidade toda) |
| 13 | A primeira infância está diminuindo | grafico | `censo_0_a_4_serie_total_ano` (447 mil em 2000 → 308 mil em 2022) |
| 14 | Crianças são 7% da cidade | numero | {{6,97%}} (Ripsa 2025) + `censo_0_a_4_serie_percentual_ano` |
| 15 | Onde vivem as crianças | mapa | `mapa_censo_0_4_absoluto`: Campo Grande, Santa Cruz e Jacarepaguá lideram |
| 16 | Onde elas pesam mais na população | mapa | `mapa_censo_0_4_percentual` |
| 17 | Quem são: raça/cor e sexo | grafico | `censo_sidra_populacao_0_6_raca_2022` |
| 18 | {{65.507}} nascimentos em 2025 | mapa | `mapa_nascidos_vivos_bairro_2025` |
| 19 | Desigualdade territorial: mortalidade infantil | mapa | `mapa_taxa_mortalidade_infantil_bairro_2025` + {{13,1}} por mil (2025) |
| 20 | Desigualdade: renda e cadastro | mapa | `mapa_cadunico_criancas_bairro_2026` |

### Parte III — Eixos e produtos (21-30)
| # | Título | Layout | Conteúdo |
|---|---|---|---|
| 21 | Prioridade: mortalidade evitável cai, mas concentra-se | grafico | `obitos_causas_evitaveis_grupo_ano` + mapa CAP menores de 5 |
| 22 | Família e Cuidados: {{58,6%}} de atendimento escolar 0-5 | numeros | creche {{43,7%}} (meta PNE 50%), pré {{85,2%}} (meta 100%); `taxa_atendimento_0_a_5_por_ano` |
| 23 | Proteção: violência familiar notificada | grafico | `violencia_familiar_taxa_municipio_ano` + mapa por RA (mãe) |
| 24 | Direito ao Brincar e território | mapa | `mapa_violencia_territorial_homicidios_ra_2024` (população geral, com a ressalva) |
| 25 | Alimentação: 1 em cada 10 nasce com baixo peso | numero | {{10,3%}} (2025) + `mapa_percentual_baixo_peso_bairro_2025`; Inclusão e Moradia: "em construção" → liga à chamada |
| 26 | Dois produtos, os mesmos dados | lista-curta | site interativo + relatório PDF (ABNT); captura das duas capas |
| 27 | Acesse agora | qr | QR de `url_site` + captura do site no celular |
| 28 | Próximos passos de governança | lista-curta | acordos de dados, pontos focais, atualização periódica |
| 29 | O que precisamos das secretarias | numeros | indicadores pendentes por fonte (deficiência, moradia, violência por tipo) |
| 30 | Obrigado · Perguntas | encerramento | contato, GitHub, site |

## 5. Lacunas e riscos identificados

- **R1 — Denominador de nascidos vivos diverge**: `nascidos_vivos_por_ano.csv` dá 65.507 em 2025, e
  `mortalidade_infantil_pos_neonatal_total_por_ano.csv` usa 59.171. É provável que a segunda conte só nascidos
  com bairro informado (ou tenha outra extração). Conferir antes de pôr os dois números no mesmo deck (slides 18
  e 19) e explicar a diferença na nota.
- **R2 — Diagrama do hub (slide 3)**: não existe; é desenho novo (SVG no tema, sem dado).
- **R3 — Mapa só de limites** (bairro × AP × CAP, slide 8): não existe como PNG; pode ser gerado por
  `mapa_coropletico_bairros` (skill `generate_map`) ou trocado por dois mapas de dados já existentes.
- **R4 — Proporção 16:9**: os PNGs foram feitos para a tela do site e para A4; mapas em tela cheia podem precisar
  de uma variante 16:9 (parâmetro de tamanho no `analise.py`, como a variante A4). Avaliar no Bloco 3; não é
  pré-requisito.
- **R5 — Dependência de Node**: `marp-cli` baixa um Chromium para exportar PDF/PPTX. Registrar em
  `specs/tech-stack.md`.

## 6. Perguntas para o checkpoint (fase 1 do readme)

| # | Pergunta | Padrão, se não houver resposta |
|---|---|---|
| Q1 | Há manual de marca ou modelo de slides oficial do IPP/Prefeitura (fontes, capa, contracapa)? | identidade do site (A5) |
| Q2 | Data, local e público da primeira apresentação (quais secretarias)? | `publico: secretarias`, sem secretaria na capa |
| Q3 | Formato de entrega: PDF, PPTX (para edição no PowerPoint) ou os dois? | os dois + HTML |
| Q4 | Quem escreve os textos da chamada e da governança (slides 5, 6, 28, 29)? | rascunho nosso, marcado para revisão |
| Q5 | Pode aparecer número por bairro de CadÚnico e violência em slide (fora do site)? | só mapas já publicados, com a mesma supressão |
| Q6 | Demonstração ao vivo do site no slide 27 ou só QR + captura? | QR + captura (sem depender de rede) |

### 6.1 Respostas do usuário (2026-09-28)

| # | Resposta | Efeito |
|---|---|---|
| Q1 | Não há manual nem modelo oficial | vale A5 (identidade do site) |
| Q2 | Gestores da Prefeitura: pouco conhecimento técnico, grande domínio do tema nas suas áreas | `publico: gestores`; nada de jargão de método (Ripsa, SIDRA, CID-10 aparecem só na fonte do rodapé); os slides de método (9-12) explicam o *efeito* da escolha ("o Censo conta menos crianças pequenas"), não a técnica; sem tom didático sobre o tema em si, que eles dominam |
| Q3 | **PPT** | saída principal `.pptx`. O PPTX padrão do Marp é uma imagem por slide (não editável); como o LibreOffice está instalado, gerar também `--pptx-editable` (experimental) e comparar no Bloco 1. Se o editável sair ruim, avaliar `python-pptx` (1.0.2 já instalado) como gerador alternativo a partir do mesmo `.md`, e decidir com o usuário |
| Q4 | Textos da chamada e da governança: **propor** | rascunho nosso nos slides 2, 4, 5, 6, 28 e 29, marcado com `<!-- revisar -->` e listado em `validation.md` |
| Q5 | Pode número por bairro de CadÚnico e violência | sim, respeitando a supressão < 20 (constituição §6), igual ao site |
| Q6 | Os dois: demonstração ao vivo e QR + captura | slide 27 com QR + captura (plano B sem rede); roteiro de demonstração em notas do apresentador (`<!-- notas -->` do Marp) |

Termo confirmado pelo usuário: **"Direito ao Brincar"**.
