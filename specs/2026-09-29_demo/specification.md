# SPECIFICATION — Versão de demonstração (branch `demo`)

Rodada aberta em 2026-09-29. Planejamento na branch `spec/demo`; implementação na branch nova **`demo`**.

## 1. Contexto

O site (`website/`) e o PDF (`relatorio/analise_primeira_infancia.pdf`) ainda têm **57 textos em lorem ipsum**
(textos de figura, achados, aberturas e sínteses de eixo) e **9 quadros "pendente"** (indicadores sem dado:
1 em Prioridade, 3 em Inclusão, 2 em Proteção, 3 em Moradia). A curadoria dos textos continua com a equipe
(DOCX → `relatorio/textos_curados.json`), e a V.1 deve sair em **6 de outubro de 2026**.

Até lá, o usuário quer publicar uma **versão de demonstração** que se leia bem por quem não é da equipe: sem lorem, sem
quadros de pendência, com um PDF curto e um aviso claro de que a versão final vem aí. Tudo isso **sem mexer** no que
a equipe cura (JSON, DOCX), no PDF das outras branches e no `staging_main`.

## 2. Pedido do usuário (2026-09-29)

1. Uma branch nova de demonstração.
2. O GitHub Pages passa a publicar a partir dela.
3. Todo lorem ipsum do site é substituído por um **texto provisório gerado pelo Claude**, curto e descritivo da
   visualização.
4. O bloco de conteúdo ou visualização que ainda falta fica **oculto** nessa versão.
5. Essas mudanças são **exclusivas da branch `demo`** (regra registrada na constituição).
6. O texto provisório **não vai para o relatório** (PDF).
7. O texto provisório **não substitui o texto curado**: o JSON e o DOCX continuam mostrando os textos pendentes e o
   lorem.
8. O PDF dessa branch vai **só até a página 18**, sem alterar o PDF de nenhuma outra branch.
9. Depois da página 18, o PDF diz que é só uma demonstração e pede para aguardar a versão final (**previsão: 6 de
   outubro de 2026**).
10. A faixa "em desenvolvimento" do site fica **maior** e mostra a data prevista da V.1.

## 3. Decisões

- **D1 — Onde o PDF para**: na **página impressa 18**, que hoje é a 19ª do arquivo e termina no *Mapa 1 — Crianças de 0 a
  4 anos, por bairro (Censo 2022)*. O corte é localizado pelo **conteúdo** (a página com a legenda "Mapa 1"), com
  conferência pelo número impresso 18. Assim ele não anda se o pré-textual mudar de tamanho. Se as duas referências
  divergirem, o build para.
  *Por quê*: é a escolha do usuário, e a demonstração termina num mapa, não no meio de uma seção.
- **D2 — Sumário do PDF de demonstração**: o sumário fica **completo**, com todos os capítulos e as páginas da versão
  inteira, e a página de aviso explica por que as páginas depois da 18 não estão ali. Os links internos e os
  marcadores que apontam para páginas cortadas são removidos, para não haver link quebrado.
  *Por quê*: é a escolha do usuário. O leitor vê tudo o que vem na V.1, e o LaTeX não muda nada na `demo`.
- **D3 — Faixa maior e data da V.1 só na `demo`**: `staging_main` continua com a faixa atual.
- **D4 — GitHub Pages só a partir da `demo`** enquanto a demonstração estiver no ar: a regra de branches do ambiente
  `github-pages` passa de `staging_main` para `demo`. Na V.1 volta para `staging_main` (ou `main`). A troca é feita
  nas configurações do repositório (o `gh` não está instalado nesta máquina); fica como passo manual do usuário ou de
  quem administra o repositório.
- **D5 — Texto provisório num arquivo próprio, só na `demo`**: `website/build/textos_demo.json`, com as mesmas chaves de
  `relatorio/textos_curados.json`. O site usa, nesta ordem: **texto curado**, depois **texto provisório**, e **nunca**
  lorem na `demo`. O build para se sobrar uma chave sem nenhum dos dois. O arquivo **não** é lido pelo gerador do PDF,
  pela exportação do DOCX nem pela sincronização DOCX → JSON, e nunca entra em `textos_curados.json`.
  *Por quê*: é o requisito 7. Quando a equipe curar uma chave, o texto curado aparece sozinho, porque tem precedência.
- **D6 — Como o texto provisório é escrito**: o Claude escreve os textos uma vez, na implementação (não há chamada de
  API no build), a partir do título, da fonte e dos números reais de cada visualização (`tabelas_finais/`). São 1 a
  3 frases (até cerca de 60 palavras) que **descrevem** o que o gráfico ou o mapa mostra (recorte, período, unidade,
  valor mais recente, tendência visível), **sem interpretação de política** nem juízo que a equipe não validou.
  Nos achados, até 3 itens por eixo. Na síntese do eixo, 2 a 3 frases.
  *Por quê*: descritivo e curto, como pediu o usuário. A leitura analítica fica para a curadoria.
- **D7 — Marca do texto provisório**: não tem rótulo visual (a faixa já diz que é demonstração). Leva o atributo
  `data-texto-demo` no HTML, para que as conferências automáticas separem o provisório do curado.
- **D8 — O que fica oculto**: todo bloco `emite_bloco_pendente` (quadro "pendente" e o título `h3` dele) e as entradas
  correspondentes no sumário lateral e nos cartões da Visão geral (a contagem "N pendentes" some). Os blocos de
  **dado pontual** (ago/2026) **continuam**: são dado real, e a `demo` tem a faixa de desenvolvimento, então a regra D7
  de `specs/2026-09-29_dados_adhoc` já permite. Nenhum eixo fica vazio: todos têm ao menos 2 subseções com dado.
- **D9 — Separação das branches**: o código da demonstração fica isolado em módulos próprios
  (`website/build/demo.py`, `relatorio/latex/build/demo_pdf.py`), com poucos pontos de gancho em `build_site.py` e
  `gera_latex.py`, ligados por uma chave `demo` em `relatorio/publicacao.json`. Isso diminui o conflito quando
  `staging_main` for mesclada na `demo`.
  **Fluxo só de ida**: `staging_main` → `demo` (merge para atualizar a demonstração). A `demo` **nunca** é mesclada em
  `staging_main` nem em `main`.
- **D10 — Link do PDF no site**: na `demo`, o botão "PDF" aponta para o PDF da própria branch
  (`raw.githubusercontent.com/.../demo/relatorio/analise_primeira_infancia.pdf`).
- **D11 — Textos da faixa e da página de aviso** (propostos; o usuário pode ajustar na revisão):
  - Faixa: **"⚠️ VERSÃO DE DEMONSTRAÇÃO — em desenvolvimento. Os textos são provisórios e alguns indicadores ainda
    não aparecem. Versão 1.0 prevista para 6 de outubro de 2026."**
  - Página final do PDF: título "Versão de demonstração" e o texto *"Este documento é uma demonstração e termina aqui.
    Os capítulos listados no sumário (eixos da Política Integrada da Primeira Infância, considerações finais e
    apêndices) estarão na versão final do relatório, prevista para 6 de outubro de 2026. Aguarde a versão final."*
  - A data fica numa chave só (`lancamento_v1: "2026-10-06"` em `publicacao.json` da `demo`), usada pelo site e pelo
    PDF.

- **D12 — Introdução resumida na demo** (pedido do usuário, 2026-09-29, depois da implementação): no site da `demo`, o
  texto curado `introducao` (421 palavras) é substituído por um resumo em duas partes de ~1/3 cada, em `textos_demo.json`.
  `introducao_demo` (141 palavras) fica como Introdução e `conclusao_introducao_demo` (142 palavras) vai para um box
  "Conclusões", no formato do dos eixos, no fim do panorama, antes das fontes. Saem as referências faltantes: "(ref.)"
  sai; "(ref. email)" vira "pelo contato no rodapé desta página"; "(ref. github)" vira "no GitHub (link no topo desta
  página)"; "ao fim desse documento… todas as tabelas" vira "cada gráfico, mapa e tabela permite baixar os dados". É
  a **única exceção** à precedência do texto curado (D5), e só no site da `demo`: `textos_curados.json`, o DOCX e o PDF
  continuam com o texto integral.

## 4. Requisitos

- **R1** A branch `demo` existe, criada de `staging_main` depois do merge desta rodada de planejamento.
- **R2** O site da `demo` tem **zero** lorem: nenhuma das palavras do gerador `_LOREM_WORDS` fora de outro contexto, e
  todo texto não curado tem `data-texto-demo`.
- **R3** O site da `demo` não tem `callout-pending` nem título de indicador pendente, nem no sumário lateral nem nos
  cartões.
- **R4** `relatorio/textos_curados.json`, `relatorio/curadoria_textos.docx` e `relatorio/controle_revisao.json` ficam
  **byte a byte iguais** aos de `staging_main` no ponto da criação da `demo`. O DOCX regerado na `demo` continua com
  o lorem e os pendentes.
- **R5** O PDF publicado na `demo` tem as páginas 1 até a página impressa 18 da versão completa, **mais uma** página de
  aviso (D11), com marca d'água, sumário completo e nenhum link interno quebrado. Não contém texto provisório.
- **R6** O PDF de `staging_main` e de qualquer outra branch não muda (o `gera_latex.py --publicar` sem a chave `demo`
  produz o mesmo documento de antes).
- **R7** A faixa da `demo` é visivelmente maior (fonte e altura) no desktop e no celular e traz a data da V.1. O restante
  do layout no desktop continua igual (comparação de screenshots, como manda `specs/2026-09-28_website_mobile`).
- **R8** O deploy só publica a partir da `demo` (D4). O workflow da `demo` falha se o HTML tiver lorem ou
  `callout-pending`.
- **R9** A constituição registra que tudo isso é exclusivo da branch `demo` e que o fluxo é só de ida.

## 5. Fora do escopo

- A apresentação (`apresentacao/`): não muda.
- Escrever texto curado: o texto provisório não é curadoria, e nada dele volta para o DOCX.
- A versão final (V.1): tirar a faixa e voltar o Pages para `staging_main`/`main` é outra rodada.
- Mudanças em `analise.py` ou nos dados.
