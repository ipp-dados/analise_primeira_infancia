 # Textos propostos — abas sem arquivo próprio (Visão geral e Prioridade)

As 19 abas abaixo não têm arquivo de figura, então o DOCX de curadoria nunca abriu espaço para elas (lacuna conhecida,
`relatorio/specs.md` v7) e o site usava o rótulo da aba como chave do texto. Proposta: **chave própria** para cada uma
(nova coluna "Chave"), trocada em `website/build/build_site.py`. Duas abas do segundo cartão de Prioridade
("Gestação (menores de 1 ano)" e "Parto (menores de 1 ano)") mostram **o mesmo gráfico** que "Menores de 1 ano ·
Gestação/Parto" do primeiro cartão: usam a mesma chave e o mesmo texto (17 textos para 19 abas).

Números conferidos em `tabelas_finais/censo_por_bairro.csv` (+ `area_plane`/`cod_rp`/`rp` do geojson de bairros, mesma
agregação do site: soma das crianças e da população, depois o %) e `tabelas_finais/mortalidade_evitaveis_cap_faixa_ano.csv`.

## Visão geral — Censo 2022, crianças de 0 a 4 anos

### 1. `censo_top10_bairros_0_4` — aba "Top 10 bairros por população 0-4 anos" (tabela)

Os dez bairros com mais crianças de 0 a 4 anos reúnem 103.363 crianças, um terço (33,3%) das 310.157 contadas pelo
Censo 2022 nos bairros da cidade. Campo Grande lidera, com 18.505, seguido de Santa Cruz (16.093), Jacarepaguá
(11.499), Bangu (11.418) e Guaratiba (10.088). Quase todos ficam na Zona Oeste; a Maré (8.553) e a Pavuna (5.892) são
as exceções da Zona Norte. Em vários deles as crianças pequenas também pesam mais na população do bairro, como na Maré
(6,9%), em Guaratiba (6,6%) e em Santa Cruz e Jacarepaguá (6,5% cada).

### 2. `mapa_censo_0_4_absoluto_ap` — aba "Área de Planejamento" (número)

Por Área de Planejamento, as crianças de 0 a 4 anos se concentram nas Zonas Oeste e Norte: a AP 5 (103.779) e a AP 3
(103.747) somam dois terços do total da cidade (33,5% e 33,4%). A AP 4, de Barra da Tijuca e Jacarepaguá, tem 56.651
(18,3%); a AP 2, das Zonas Sul e da Tijuca, 32.281 (10,4%); e a AP 1, do Centro, 13.699 (4,4%).

### 3. `mapa_censo_0_4_absoluto_rp` — aba "Região de Planejamento" (número)

Entre as 16 Regiões de Planejamento, Jacarepaguá tem o maior número de crianças de 0 a 4 anos (37.533), seguida de
Bangu (33.685), Campo Grande (32.782) e Santa Cruz (26.108). As menores são a Ilha do Governador (8.476), Inhaúma
(9.231) e as regiões de Guaratiba e da Tijuca (cerca de 11.200 cada).

### 4. `mapa_censo_0_4_percentual_ap` — aba "Área de Planejamento" (%)

O peso das crianças pequenas na população varia menos entre as Áreas de Planejamento do que o número absoluto. A AP 5
tem a maior participação (5,7% da população), seguida da AP 4 (5,1%), da AP 3 (5,0%) e da AP 1 (4,9%). A AP 2, das
Zonas Sul e da Tijuca, tem a menor: 3,6%.

### 5. `mapa_censo_0_4_percentual_rp` — aba "Região de Planejamento" (%)

Por Região de Planejamento, as maiores participações de crianças de 0 a 4 anos na população estão em Santa Cruz e
Guaratiba (6,3% cada), seguidas de Ramos e Pavuna (5,8% cada). As menores estão na Zona Sul e na Tijuca (3,7% e
3,6%).

## Prioridade — óbitos por causas evitáveis, por CAP (SIM/SVS-Rio, TabWin, 2006 a 2025)

Notas que valem para todas: a contagem é de óbitos de residentes; as linhas são as 10 CAPs; em 2025 as contagens por
CAP são pequenas (em geral abaixo de 20) e variam muito de um ano para o outro.

### 6. `evitaveis_cap_menores_1_gestacao` — "Menores de 1 ano · Gestação" e "Gestação (menores de 1 ano)"

As mortes de bebês reduzíveis pela atenção à mulher na gestação são o maior grupo de causas evitáveis. O total da
cidade subiu de 315 em 2006 para o pico de 389 em 2013 e caiu depois: a média anual passou de 351 óbitos em 2011-2015
para 240 em 2021-2025 (264 em 2025). Em 2025, as CAPs com mais óbitos foram a 4.0 (47), a 5.2 (40) e a 3.3 (39).

### 7. `evitaveis_cap_menores_1_parto` — "Menores de 1 ano · Parto" e "Parto (menores de 1 ano)"

Os óbitos de bebês reduzíveis pela atenção à mulher no parto são menos numerosos: o total da cidade teve o pico de 111
em 2008 e ficou em 67 em 2025, com média anual de 83 em 2011-2015 e 70 em 2021-2025. Em 2025, nenhuma CAP passou de
10 óbitos (3.3, 4.0 e 5.3, com 10 cada), o que pede cautela na comparação entre elas.

### 8. `evitaveis_cap_menores_1_recem_nascido` — "Menores de 1 ano · Recém-nascido"

Os óbitos reduzíveis pela atenção ao recém-nascido tiveram a maior queda entre os grupos: de 195 em 2006 para 55 em
2025, e a média anual caiu de 138 em 2011-2015 para 87 em 2021-2025. Em 2025, a CAP 3.3 teve o maior número (16),
seguida da 4.0 (11) e da 3.1 (8).

### 9. `evitaveis_cap_menores_1_diagnostico` — "Menores de 1 ano · Diagnóstico e tratamento"

Os óbitos de bebês reduzíveis por ações adequadas de diagnóstico e tratamento caíram de 103 em 2006 (pico de 120 em
2007) para 46 em 2025; a média anual passou de 94 em 2011-2015 para 59 em 2021-2025. Em 2025, as CAPs 3.3 (12) e 3.1
(10) tiveram os maiores números.

### 10. `evitaveis_cap_menores_1_promocao` — "Menores de 1 ano · Promoção da saúde"

Os óbitos de bebês reduzíveis por ações de promoção da saúde vinculadas à atenção mudaram pouco ao longo da série: a
média anual foi de 67 em 2011-2015 e de 60 em 2021-2025 (58 em 2025). É o grupo de menores de 1 ano com a menor queda.
Em 2025, a CAP 4.0 teve o maior número (14), seguida das CAPs 3.1 e 5.2 (10 cada).

### 11. `evitaveis_cap_1_a_4_diagnostico` — "De 1 a 4 anos · Diagnóstico e tratamento"

Entre as crianças de 1 a 4 anos, os óbitos reduzíveis por diagnóstico e tratamento adequados são poucos e oscilam: o
total da cidade foi de 54 em 2006 (pico de 63 em 2010) a 29 em 2025, com média anual de 41 em 2011-2015 e 35 em
2021-2025. Em 2025, as CAPs 3.1 e 3.3 tiveram 6 óbitos cada; com números tão pequenos, as diferenças entre CAPs devem
ser lidas com cautela.

### 12. `evitaveis_cap_1_a_4_promocao` — "De 1 a 4 anos · Promoção da saúde"

Os óbitos de crianças de 1 a 4 anos reduzíveis por ações de promoção da saúde ficaram praticamente estáveis: média
anual de 36 em 2011-2015 e de 33 em 2021-2025, com 34 em 2025. Nesse ano, as CAPs 5.1 e 5.3 tiveram 6 óbitos cada e a
4.0, 5. Como são contagens pequenas, a série por CAP serve mais para acompanhar tendências do que para ordenar as
regiões.

### 13. `evitaveis_cap_menores_5_gestacao` — "Menores de 5 anos · Gestação"

Para os menores de 5 anos, a série de óbitos reduzíveis pela atenção à gestação é quase idêntica à dos menores de 1
ano, porque essas mortes acontecem quase sempre no primeiro ano de vida: 318 em 2006, pico de 389 em 2013 e 266 em
2025. Em 2025, as CAPs 4.0 (47), 5.2 (41) e 3.3 (40) tiveram os maiores números.

### 14. `evitaveis_cap_menores_5_parto` — "Menores de 5 anos · Parto"

Como na gestação, os óbitos reduzíveis pela atenção ao parto entre menores de 5 anos praticamente coincidem com os dos
menores de 1 ano: pico de 112 em 2008 e 67 em 2025, com média anual de 83 em 2011-2015 e 70 em 2021-2025. Em 2025, as
CAPs 3.3, 4.0 e 5.3 tiveram 10 óbitos cada.

### 15. `evitaveis_cap_menores_5_recem_nascido` — "Menores de 5 anos · Recém-nascido"

Os óbitos reduzíveis pela atenção ao recém-nascido, entre menores de 5 anos, repetem a série dos menores de 1 ano: de
198 em 2006 para 55 em 2025, a maior queda entre os grupos de causas evitáveis. Em 2025, a CAP 3.3 teve o maior número
(16), seguida da 4.0 (11) e da 3.1 (8).

### 16. `evitaveis_cap_menores_5_diagnostico` — "Menores de 5 anos · Diagnóstico e tratamento"

Somando bebês e crianças de 1 a 4 anos, os óbitos reduzíveis por diagnóstico e tratamento adequados caíram de 157 em
2006 para 75 em 2025; a média anual passou de 134 em 2011-2015 para 94 em 2021-2025. Em 2025, as CAPs 3.3 (18) e 3.1
(16) concentraram os maiores números.

### 17. `evitaveis_cap_menores_5_promocao` — "Menores de 5 anos · Promoção da saúde"

Os óbitos de menores de 5 anos reduzíveis por ações de promoção da saúde variaram pouco: a média anual foi de 103 em
2011-2015 e de 93 em 2021-2025, com 92 em 2025 (pico de 119 em 2010). Em 2025, a CAP 4.0 teve o maior número (19),
seguida das CAPs 5.2 (13) e 3.1 (12).
