# SPECIFICATION — Apresentações de Família e Cuidados e de Moradia (rodada de 2026-10-07)

Status: implementada em 2026-10-07 (branch `spec/deck_familia_moradia`). Família e Cuidados publicada; Moradia escrita,
**não gerada** (falta a fonte de dados, §4).

## 1. Contexto

Pedido do usuário (2026-10-07): mais duas variantes do deck, na estrutura das de Alimentação e Direito ao Brincar
(`specs/2026-10-06_deck_alimentacao_brincar`), para **Família e Cuidados** e **Moradia**.
- Moradia: dois slides reservados para "Dados Territórios Sociais".
- Família e Cuidados: destacar a mudança das matrículas em 2020/2021 entre redes privada e pública; tornar a cobertura
  vacinal mais fácil de ler e comparar; dar grande peso à composição familiar (e ao seu aspecto geográfico); trazer do
  eixo Prioridade o que couber; 12 a 15 slides (até 15 min), com capa e encerramento.

## 2. Decisões

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | `variantes/familia_cuidados.md` (14 slides) e `variantes/moradia.md` (13 slides), na sequência das variantes anteriores: capa, o que o eixo mostra (nota forte do limite da fonte), números e gráficos, número por bairro antes do percentual, limites e próximos passos, resumo, encerramento | "use a mesma estrutura" |
| D2 | Família: composição familiar em 4 slides (arranjo; arranjo × pobreza; número por bairro; % por bairro) | "alta importância" à composição familiar e à geografia |
| D3 | Do eixo Prioridade, um slide de contexto: razão CadÚnico/população (49%), crianças e famílias no cadastro, % em pobreza | dá a escala do cadastro antes da composição familiar; mortalidade não cabe no tema |
| D4 | Matrículas na pandemia: gráfico só do deck (2015-2025, eixo a partir de zero, faixa da pandemia, variação 2019→2021 escrita em cada rede) + slide "depois da pandemia" (volta da privada, queda da pública, queda da população de 0 a 5) | destacar 2020/2021; a nota do apresentador diz que o Censo Escolar não acompanha a criança (não mostra troca de rede) |
| D5 | Vacinação: gráfico só do deck, uma linha por vacina ordenada pela cobertura de 2025 (último ano completo; 2026 em curso), cor pela meta do PNI (90% BCG e rotavírus, 95% demais), traço da meta e círculo do pior ano recente (2022, menor mediana entre 2019 e 2024) | o gráfico de 11 linhas e o de barras por ano eram difíceis de comparar; metas a confirmar com a SMS (`revisar`) |
| D6 | % de famílias com uma só adulta por bairro com escala a partir de 60% (parâmetro novo `piso` em `_a4_mapa`, padrão 0) e o aviso na legenda, no texto e no rodapé | todos os bairros entre 63% e 88%: com a escala em zero, o mapa saía de uma cor só |
| D7 | Arranjo × pobreza: gráfico só do deck (% em pobreza por arranjo, uma barra cada, com o total de famílias) | a versão A4 das barras agrupadas tinha legenda sobre as barras e mostrava a célula suprimida (< 20) como 0,0 |
| D8 | Moradia: mapa de % de inadequação com o valor atípico fixo da decisão de 2026-10-06 (Alto da Boa Vista; opção `outliers_fixos` lendo `_OUTLIERS_INADEQUACAO_CADUNICO`), não Tukey | mesmo tratamento do analise.py e do site |
| D9 | Moradia: dois slides "Dados Territórios Sociais" com caixa "Espaço reservado"; a nota do apresentador diz como trocar pela imagem (pasta `variantes/moradia_adhoc/`, como em Alimentação) | pedido do usuário; dado pontual só no deck (constituição §3) |
| D10 | Só acréscimos no gerador: chaves `fam_*`/`mor_*` em `build/numeros.py`; mapas e gráficos `apres_*` em `build/mapas_apresentacao.py` (opção `desenha` para gráfico próprio); `piso` opcional em `primeira_infancia/impressao.py` | deck principal e variantes anteriores saem iguais |

## 3. Fora do escopo

Deck principal e outras variantes; site e PDF.

## 4. Bloqueio — dados de Moradia (2026-10-07)

As tabelas de Moradia (`cadunico_moradia_resumo_0_a_5_2026.csv`, `cadunico_*_componentes_0_a_5_2026.csv`,
`tabela_mapa_cadunico_{inadequacao,adensamento}_bairro_2026.csv`) e as figuras de componentes não estão em
`tabelas_finais/`/`visualizacoes/`, e o `analise.py` não as gera hoje: o banco do CTPE voltou a ter só
`bronze_cadunico` e `silver_cadunico_geral` (partição 2026-06-12, grupo `'0-6'`). As silvers
`silver_cadunico_pessoas`/`_familias` (partição 2026-07-10) não existem mais, e o `analise.py` para no `assert` do grupo
`'0-5'` (linha 466). Os mesmos arquivos de Inclusão também faltam. A variante `moradia.md` gera assim que as tabelas
voltarem (`python apresentacao/build/numeros.py` lista as chaves `mor_*` com "[falta …]" até lá).
