# Validação — `specs/relatorio_latex`

Preencher ao fim de cada bloco (resultado + data). Nada é "validado" só porque o build saiu com código 0.

## Build
- [ ] V1 `gera_latex.py` do zero (sem `_build/`) compila sem erro; zero referências/citações indefinidas
- [ ] V2 Nenhum `Overfull \hbox` > 5 pt no log; nenhuma figura ou tabela passando da margem
- [ ] V3 Texto ausente sai como lorem idêntico ao do site para a mesma chave; o build lista as chaves em lorem

## Conteúdo e consistência com o site
- [ ] V4 Todo `##`/`###` de `estrutura_eixos.md` vira capítulo/seção, na mesma ordem e numeração do site
- [ ] V5 Toda `visualização`/`mapa` referenciada aparece uma vez como Gráfico/Mapa numerado
- [ ] V6 Toda entrada de `textos_curados.json` aparece no texto extraído do PDF (mesma checagem da
      `SKILL.md`, passo 7), exceto as exceções já documentadas lá
- [ ] V7 Todo pendente aparece como caixa "Indicador em desenvolvimento"
- [ ] V8 Mover um indicador de eixo no `.md` e regerar → ele muda de capítulo sem mexer em código

## ABNT
- [ ] V9 Capa, folha de rosto, resumo (150-500 palavras + palavras-chave), listas, sumário, na ordem da NBR 10719
- [ ] V10 Margens 3/2 cm, 12 pt, 1,5; numeração progressiva NBR 6024; paginação arábica no texto
- [ ] V11 Gráficos/mapas/tabelas: identificação acima, "Fonte:" abaixo, listas próprias
- [ ] V12 "Fontes" em NBR 6023 (órgão, título, URL, "Acesso em:")
- [ ] V13 Tabelas abertas nas laterais (IBGE); números pt-BR; `ano` sem separador de milhar

## Figuras
- [ ] V14 Toda figura cabe na largura útil (16 cm); texto interno ≥ 7 pt impresso (medido, não estimado)
- [ ] V15 Figuras com variante A4 sem título/fonte duplicados; as que ainda caem no fallback listadas no log do build

## Dados e privacidade
- [ ] V16 Nenhuma contagem do CadÚnico < 20 abaixo do município (tabelas vêm de CSVs já suprimidos; conferir)
- [ ] V17 Rótulos de faixa etária = faixa real do dado (`auditoria_faixas.md`)

## Entregável
- [ ] V18 PDF < 20 MB; páginas-amostra rasterizadas e olhadas (capa, sumário, abertura de capítulo,
      página de mapa, pendente, apêndice, Fontes, última página)
- [ ] V19 Link "Relatório final em PDF" do site continua válido (mesmo caminho)
- [ ] V20 `inventario_fontes.md` sem alertas não resolvidos (ou todos com decisão do usuário registrada)
