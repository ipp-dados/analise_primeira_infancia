# Textos propostos — Inclusão e Moradia (R8)

Proposta para as 11 chaves de Inclusão e Moradia sem texto curado (lorem no site de `staging_main`), incluindo os 2
mapas novos de R2. Estilo: o dos textos curados do CadÚnico em Prioridade e Família e Cuidados. Faixa escrita
"até 72 meses" (regra D10 de `specs/2026-10-06_cadunico_inclusao_moradia`). **Todo número vem das tabelas de
`tabelas_finais/` da execução de 2026-11-05** (silver do CadÚnico, partição de 10/07/2026); a coluna "Conferido em"
diz de onde. Só entram em `relatorio/textos_curados.json` depois do OK do usuário.

## Inclusão

### 1. `cadunico_deficiencia_criancas_0_a_5_2026` — Crianças no CadÚnico com alguma deficiência (texto da tabela)

Das 200.784 crianças até 72 meses inscritas no CadÚnico em julho de 2026, 7.919 têm alguma deficiência registrada, o
que corresponde a 3,9% do total. O dado se refere apenas às crianças cadastradas e depende do que a família declarou
no cadastro: não é uma estimativa da prevalência de deficiência entre todas as crianças da cidade.

Conferido em: `cadunico_deficiencia_criancas_0_a_5_2026.csv` (200.784; 7.919; 3,9%).

### 2. `mapa_percentual_cadunico_criancas_deficiencia_bairro_2026` — mapa de % com deficiência

A proporção de crianças com deficiência varia pouco entre os bairros: quase nove em cada dez ficam entre 3% e 5%,
perto da média do município (3,9%). Entre os bairros com valor próprio, os maiores percentuais estão em Pechincha (6,5%), Itanhangá e Méier (6,0% cada), Padre Miguel (5,3%) e Caju
(5,1%). Pechincha e Méier têm só 25 crianças com deficiência cada; por isso pequenas diferenças no número mudam
bastante o percentual. Os menores valores estão em Manguinhos (2,4%), Cidade de Deus (2,5%) e Acari (2,7%). Em
números absolutos, Campo Grande (446) e Santa Cruz (421) concentram mais crianças com deficiência. Para proteger os
dados, 69 bairros com poucos casos aparecem somados a outros da mesma Região Administrativa e mostram a taxa do
conjunto.

Conferido em: `tabela_mapa_cadunico_deficiencia_bairro_2026.csv` (% e número por bairro; 87% dos 162 bairros entre 3%
e 5%; 69 bairros agregados em 14 conjuntos; um conjunto agregado tem 2,3%, por isso "com valor próprio").

### 3. `cadunico_deficiencia_familias_0_a_5_2026` — Famílias com criança com deficiência (texto da tabela)

São 7.810 famílias com ao menos uma criança até 72 meses com deficiência, 4,4% das 178.838 famílias com crianças
nessa faixa no CadÚnico. Entre as 6.335 famílias com a informação preenchida, 1.530 (24,2%) recebem o Benefício de
Prestação Continuada (BPC) por deficiência; outras 1.475 não têm o dado. O BPC é registrado para a família, por isso
o benefício pode se referir a qualquer membro, não necessariamente à criança.

Conferido em: `cadunico_deficiencia_familias_0_a_5_2026.csv` (7.810; 4,4%; 178.838; 1.530 de 6.335 = 24,2%; 1.475).

### 4. `cadunico_criancas_por_tipo_deficiencia` — Crianças por tipo de deficiência (gráfico)

Os tipos mais registrados são o transtorno mental (3.662 crianças, 46,2% das crianças com deficiência) e a
deficiência mental ou intelectual (3.332, 42,1%), seguidos da deficiência física (2.035, 25,7%) e da síndrome de
Down (359, 4,5%). As deficiências visuais e auditivas somam poucos casos, cada tipo abaixo de 2%. Uma mesma criança
pode ter mais de um tipo registrado, por isso os percentuais não somam 100%.

Conferido em: `cadunico_tipos_deficiencia_0_a_5_2026.csv`.

## Moradia

### 5. `cadunico_criancas_inadequacao_componentes` — Inadequação habitacional por componente (gráfico)

Segundo a aproximação da metodologia da Fundação João Pinheiro, 11.589 crianças até 72 meses do CadÚnico (5,9%) vivem
em domicílio com alguma inadequação habitacional. A maior parte se deve à infraestrutura (9.841 crianças, 5,0%),
sobretudo ao esgoto inadequado (4.676), à água sem canalização ou fora da rede geral (3.584) e ao lixo queimado,
enterrado ou jogado (2.756). Os problemas da própria construção (inadequação edilícia) atingem 2.234 crianças (1,1%):
todos os cômodos usados como dormitório (1.018), piso de terra (859) e ausência de banheiro (627). Um domicílio pode
ter mais de um componente.

Conferido em: `cadunico_moradia_resumo_0_a_5_2026.csv` (11.589; 5,9%; 9.841; 5,0%; 2.234; 1,1%) e
`cadunico_inadequacao_componentes_0_a_5_2026.csv` (componentes).

### 6. `mapa_cadunico_inadequacao_n_bairro_2026` — mapa de número, inadequação (novo)

Em números absolutos, as crianças em domicílios com inadequação habitacional se concentram na Zona Oeste: Santa Cruz
(1.068), Guaratiba (770) e Campo Grande (430) lideram, seguidos da Penha (308), na Zona Norte, e de Paciência (276).
Os quatro primeiros são os únicos bairros com mais de 300 crianças nessa situação. Bairros com menos de 20 casos
aparecem sem cor: estão somados por Região Administrativa ou Área de Planejamento na tabela.

Conferido em: `tabela_mapa_cadunico_inadequacao_bairro_2026.csv` (5 maiores; 4 bairros acima de 300).

### 7. `mapa_percentual_cadunico_inadequacao_bairro_2026` — mapa de %, inadequação

Em proporção, o caso mais destacado é o Alto da Boa Vista, onde 44,1% das crianças do CadÚnico (83 de 188) vivem em
domicílio com inadequação habitacional, mais que o dobro de qualquer outro bairro; por isso ele aparece na cor máxima
e fora da escala. Seguem Vargem Grande (20,8%), Barra de Guaratiba (17,7%), Portuguesa (16,5%) e Penha (15,1%). Santa
Cruz e Guaratiba, que têm os maiores números, ficam em 9,3% e 11,6%, acima da média do município (5,9%).

Conferido em: `tabela_mapa_cadunico_inadequacao_bairro_2026.csv` (% por bairro) e
`cadunico_moradia_resumo_0_a_5_2026.csv` (5,9%).

### 8. `mapa_cadunico_adensamento_n_bairro_2026` — mapa de número, adensamento (novo)

O adensamento excessivo (mais de 2 pessoas por dormitório) é o problema de moradia mais comum entre as crianças do
CadÚnico, e os maiores números estão na Zona Oeste: Santa Cruz (5.681 crianças), Campo Grande (5.249), Guaratiba
(3.661), Bangu (3.053) e Realengo (2.877). Como atinge cerca de metade das crianças cadastradas, o mapa de número
acompanha de perto a distribuição das crianças do CadÚnico pela cidade.

Conferido em: `tabela_mapa_cadunico_adensamento_bairro_2026.csv` (5 maiores) e `cadunico_moradia_resumo_0_a_5_2026.csv`
(51,6%).

### 9. `mapa_percentual_cadunico_adensamento_bairro_2026` — mapa de %, adensamento

Em 2026, 101.477 crianças até 72 meses do CadÚnico (51,6%) vivem em domicílio com mais de 2 pessoas por dormitório.
O percentual é alto em toda a cidade: mesmo os menores valores ficam acima de 30%, como em Todos os Santos (32,3%),
Rocha (33,2%) e Abolição (33,9%). Os maiores estão em Vaz Lobo (61,6%), Glória (57,9%), São Conrado (57,8%), Cacuia
(57,5%) e Sepetiba (56,8%).

Conferido em: `cadunico_moradia_resumo_0_a_5_2026.csv` (101.477; 51,6%) e `tabela_mapa_cadunico_adensamento_bairro_2026.csv`.

### 10. `cadunico_criancas_deficit_componentes` — Déficit habitacional por componente (gráfico)

Pela aproximação da metodologia da Fundação João Pinheiro, 86.393 crianças até 72 meses do CadÚnico (43,2%) vivem em
domicílio em déficit habitacional. Quase todo o déficit vem do ônus excessivo com aluguel, quando famílias com renda
de até 3 salários mínimos gastam mais de 30% dela com aluguel: são 82.081 crianças (41,8%). Os demais componentes
são bem menores: domicílio improvisado (3.436 crianças), rústico (591) e coabitação (588). Um domicílio pode ter mais
de um componente.

Conferido em: `cadunico_moradia_resumo_0_a_5_2026.csv` (86.393; 43,2%) e `cadunico_deficit_componentes_0_a_5_2026.csv`.

### 11. `cadunico_moradia_resumo_0_a_5_2026` — Indicadores agregados de moradia (texto da tabela)

A tabela resume as condições de moradia das crianças até 72 meses do CadÚnico e de suas famílias. Os problemas mais
frequentes são o adensamento excessivo (51,6% das crianças) e o déficit habitacional (43,2%), puxado pelo peso do
aluguel. A inadequação habitacional atinge 5,9%, e a falta de banheiro (0,3%) e de água canalizada (0,6%) é rara.
Entre as famílias, os percentuais são parecidos: 48,0% em adensamento excessivo, 42,5% em déficit e 5,9% em
inadequação.

Conferido em: `cadunico_moradia_resumo_0_a_5_2026.csv`.
