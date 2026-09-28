# Plano — `specs/2026-09-28_melhorias_site`

Rodada de **melhorias pequenas do site e do relatório** (pedido do usuário, 2026-09-28). Plano apresentado e aprovado
("ok") na mesma data; branch `spec/melhorias-site`, a partir de `staging_main` (`2702ef9`). É a **Rodada A** de três:

| Rodada | Conteúdo | Branch / pasta |
|---|---|---|
| **A** (esta) | favicon, texto de abertura por eixo, lorem ≤ 150 palavras, só "Painéis" nos pequenos múltiplos, HTML menor | `spec/melhorias-site` · esta pasta |
| B | `ROADMAP.md` Próximos, item 1 (organização do projeto), fases 1a e 1b | `spec/organizacao` · `specs/<data>_organizacao` |
| C | `ROADMAP.md` Próximos, item 6 (documentação) + documento de especificação funcional/técnica do projeto | depois da B, que muda caminhos |

## 1. Ponto de partida (medido em 2026-09-28, `staging_main` 2702ef9)

| Aspecto | Hoje |
|---|---|
| Favicon | `website/assets/images/favicon.svg`: quadrado azul IPP com o ícone "target" do eixo Prioridade; só SVG (sem `.ico`, PNG nem `apple-touch-icon`) |
| Abertura dos eixos | aba/capítulo começa em "Principais achados" e vai direto para as figuras; não há texto de apresentação do eixo |
| Lorem | site, LaTeX e DOCX sorteiam 100-200 palavras por bloco; `resumo` 250 (Introdução e Considerações finais já curadas) |
| Pequenos múltiplos | controle "Painéis \| Linhas" (`js/charts.js`, `pequenosMultiplos`) que desenha as duas vistas |
| `website/index.html` | **771 KB** (127 KB gzip). Mapas SVG inline 335 KB (56 cartões, 114 SVGs com as variantes sem outliers); CSV embutido em `data-csv` 129 KB (88 KB dos mapas); 58 ícones Lucide inline 22 KB. `data/charts.js` 95 KB (241 números com 5+ casas decimais); `data/geo.js` 221 KB, já compacto (1 casa decimal, caminhos relativos) |

## 2. Decisões

Pedidas pelo usuário:

| # | Tema | Decisão |
|---|---|---|
| U1 | Favicon | melhorar; opções geradas nesta rodada para escolha, com as variantes de compatibilidade. **Escolhida: C, monograma "PI"** (2026-09-28) |
| U2 | Abertura | texto de até **100 palavras** no início de cada **eixo** (as 6 abas do site / capítulos do PDF), **abaixo de "Principais achados"**; lorem até ser curado |
| U3 | Lorem | todo bloco lorem com **no máximo 150 palavras**; texto curado não muda |
| U4 | Pequenos múltiplos | ficar **só com Painéis**: sai o botão "Linhas" e a vista de linhas |
| U5 | Tamanho | reduzir o HTML **sem perda de qualidade visual** |

Tomadas no plano (o OK sem ressalvas vale como aprovação das recomendações):

- "Seção principal" = **eixo**, não cada subseção.
- O texto de abertura é um **bloco do relatório** (`blocos_relatorio()`), chave `introducao_<eixo>`: a mesma chave
  no DOCX de curadoria (bookmark novo), em `textos_curados.json`, no site e no PDF — como `achados_`/`sintese_`.
- Faixa do lorem: **100-150** palavras (antes 100-200); `resumo` 250 → 150; abertura do eixo 90 palavras.
- Tamanho: o que muda é **onde** o conteúdo mora, não o que se vê — o DOM depois do JavaScript tem de ser o mesmo.
  Aceito: mapas montados em JS (o site já exige JS para todos os gráficos).

## 3. Princípios

1. **Nenhuma mudança visual fora do pedido.** Capturas a 1400 px e 390 px antes/depois de cada aba: diferenças só
   onde a rodada muda algo (abertura dos eixos, lorem mais curto, cartões de pequenos múltiplos sem o controle,
   favicon). Os blocos de tamanho (U5) têm de sair **pixel a pixel iguais**.
2. **Texto curado intocado**: `relatorio/textos_curados.json` sem nenhuma alteração de valor nesta rodada.
3. **Uma fonte da verdade do lorem por artefato**, mas as três mudam juntas (site = LaTeX, mesmo texto; DOCX, lista
   própria) e a sincronização DOCX → JSON continua reconhecendo o placeholder.
4. **Regras do site estático** (`website/README.md`): sem `fetch`, só html/css/js/svg/png/jpg (+ `.ico`, a acrescentar
   à lista do workflow), caminhos relativos minúsculos, `?v=<md5>` nos recursos.

## 4. Riscos

| Risco | Tratamento |
|---|---|
| Mudar o lorem faz o lorem antigo do DOCX parecer "texto editado" e ele vazar para `textos_curados.json` na próxima sincronização | regenerar `curadoria_textos.docx` descartando o lorem do DOCX anterior (`_eh_lorem`) e conferir que a sincronização não muda nenhuma chave |
| Mapas montados em JS mudarem cor/ordem/tooltip | mesmo `<use>` na mesma ordem e com os mesmos atributos; comparação do `outerHTML` de cada `<svg>` antes/depois no navegador e das capturas |
| CSV gerado no clique diferente do atual | comparar byte a byte, no navegador, o CSV gerado com o `data-csv` antigo de cada mapa |
| Ícones num sprite (`<use>`) perderem estilo (seletor CSS que desce no ícone) | conferir `css/` antes; capturas |
| Workflow de deploy rejeitar `.ico` | incluir a extensão na lista do `.github/workflows/deploy-relatorio.yml` e no `website/README.md` |
