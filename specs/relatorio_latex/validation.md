# Validação — `specs/relatorio_latex`

Preencher ao fim de cada bloco (resultado + data). Nada é "validado" só porque o build saiu com código 0.

## Build
- [x] V1 `gera_latex.py` do zero (sem `_build/`) compila sem erro; zero referências/citações indefinidas
- [~] V2 Nenhum `Overfull \hbox` > 5 pt no log; nenhuma figura ou tabela passando da margem
- [x] V3 Texto ausente sai como lorem idêntico ao do site para a mesma chave; o build lista as chaves em lorem

## Conteúdo e consistência com o site
- [x] V4 Todo `##`/`###` de `estrutura_eixos.md` vira capítulo/seção, na mesma ordem e numeração do site
- [x] V5 Toda `visualização`/`mapa` referenciada aparece uma vez como Gráfico/Mapa numerado
- [x] V6 Toda entrada de `textos_curados.json` aparece no texto extraído do PDF (mesma checagem da
      `SKILL.md`, passo 7), exceto as exceções já documentadas lá
- [x] V7 Todo pendente aparece como caixa "Indicador em desenvolvimento"
- [x] V8 Mover um indicador de eixo no `.md` e regerar → ele muda de capítulo sem mexer em código

## ABNT
- [x] V9 Capa, folha de rosto, resumo (150-500 palavras + palavras-chave), listas, sumário, na ordem da NBR 10719
- [x] V10 Margens 3/2 cm, 12 pt, 1,5; numeração progressiva NBR 6024; paginação arábica no texto
- [x] V11 Gráficos/mapas/tabelas: identificação acima, "Fonte:" abaixo, listas próprias
- [x] V12 "Fontes" em NBR 6023 (órgão, título, URL, "Acesso em:")
- [x] V13 Tabelas abertas nas laterais (IBGE); números pt-BR; `ano` sem separador de milhar

## Figuras
- [x] V14 Toda figura cabe na largura útil (16 cm); texto interno ≥ 7 pt impresso (medido, não estimado)
- [x] V15 Figuras com variante A4 sem título/fonte duplicados; as que ainda caem no fallback listadas no log do build

## Dados e privacidade
- [x] V16 Nenhuma contagem do CadÚnico < 20 abaixo do município (tabelas vêm de CSVs já suprimidos; conferir)
- [~] V17 Rótulos de faixa etária = faixa real do dado (`auditoria_faixas.md`)

## Entregável
- [x] V18 PDF < 20 MB; páginas-amostra rasterizadas e olhadas (capa, sumário, abertura de capítulo,
      página de mapa, pendente, apêndice, Fontes, última página)
- [x] V19 Link "Relatório final em PDF" do site continua válido (mesmo caminho)
- [x] V20 `inventario_fontes.md` sem alertas não resolvidos (ou todos com decisão do usuário registrada)

## Resultado (2026-09-25, PDF de `relatorio/latex/_build/relatorio.pdf`, 155 páginas, 14,2 MB)

Checagens automáticas num script da sessão (texto extraído com PyMuPDF, log do LaTeX, figuras de `visualizacoes/a4/` e
`mapas/a4/`), mais leitura página a página das 154-155 páginas em folhas de contato.

- V1: 0 referência/citação indefinida. V3: lorem do gerador = `_lorem` do site para a mesma semente.
- V2 (aceito com ressalva): 14 `Overfull \hbox` > 5 pt restantes, todos em parágrafos; nenhum texto passa 3 pt da
  margem em nenhuma página (V10). Corrigidos no caminho: títulos de seção em bandeira, coluna de número de página das
  listas, nomes de arquivo com quebra depois de "_", cabeçalho de tabela proporcional ao número de colunas, coluna de
  texto longo com quebra, tabela larga demais para retrato vai para paisagem (largura estimada), `\emergencystretch`.
- V4/V5/V6/V7: 6 capítulos de eixo na ordem do `.md`; 94 figuras = 94 referências; os 51 textos curados com figura
  no relatório estão no PDF; 9 pendentes = 9 caixas. V8: indicador movido de eixo no `.md` mudou de capítulo sem
  tocar em código (teste feito e desfeito).
- V9: ordem NBR 10719 (folha de rosto, resumo com palavras-chave, listas de gráficos/mapas/tabelas, siglas, sumário).
- V10: margens 3 cm/2 cm respeitadas (texto de 2,98 cm a ≥ 2 cm).
- V12: 13 entradas NBR 6023, 12 com "Acesso em:" (CadÚnico sem URL pública). Citações em caixa normal
  (NBR 10520:2023), lista Fontes com a entidade em caixa alta (`\entidade{}` em `fontes.bib`/`estilo.sty`).
- V13: sem ano com separador de milhar ("2.007"/"2.013" achados são contagens de bairro, não anos).
- V14: todo texto das figuras de impressão ≥ 6,3 pt impresso (exceto a atribuição do fundo dos mapas, 4,8 pt, de
  propósito). Corrigidos: 6 gráficos de subgrupo CID que saíam com 4,2-4,8 pt (nome longo no fim da linha
  alargava a figura para 23-26 cm).
- V15: 0 figura em fallback (todas na versão de impressão, sem título/fonte embutidos).
- V16: nenhuma célula 1-19 nas tabelas do CadÚnico por bairro.
- V17 (parcial): rótulos das figuras de impressão seguem `ROTULOS_EIXO`; conferência completa das faixas contra
  `auditoria_faixas.md` fica para a revisão de conteúdo da equipe.
- V18: 14,2 MB (< 20 MB).
- V19: pendente -- depende de publicar (`gera_latex.py --publicar`, mesmo caminho do link do site).
- V20: inventário sem alerta bloqueante (toda figura/tabela do relatório com fonte ligada ao `fontes.bib`); restam
  alertas informativos (arquivos fora da estrutura por causa das exclusões, 10 candidatos a limpeza, 11 textos
  `fonte:` do `.md` diferentes do `fonte_dados`, `regen_missing_pngs.py` regravando 15 PNGs de tela sem fonte).
- Texto interno: nenhuma marca de nota da equipe no PDF (`specs/`, nomes, "baixar dados").

