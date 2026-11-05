# Textos de eixo propostos — Proteção, Direito ao Brincar, Alimentação e Moradia

Proposta para revisão (T1.3). Mesmo formato de `relatorio/textos_eixos.md`: depois de aprovados, entram lá e são
importados com `relatorio/curadoria/importa_textos_eixos.py`. Cada número foi conferido em `tabelas_finais/`
(execução de 2026-11-05); a linha "Conferido em" de cada eixo diz onde. Frases de interpretação (sem número) estão
marcadas com ◆ no fim da lista de conferência, para você decidir se ficam.

---

## 🛡️ Proteção

### Principais achados

- As notificações de violência familiar contra crianças de 0 a 5 anos cresceram muito desde 2011: em 2025, foram 1.756 envolvendo a mãe e 1.404 envolvendo o pai, contra 324 e 135
- Em 2025, foram 4,5 notificações por mil crianças envolvendo a mãe e 3,6 envolvendo o pai
- A Zona Oeste concentra os registros: a CAP 5.2 tem as maiores taxas (12,1 por mil para a mãe e 10,7 para o pai), e Santíssimo, Bangu e Guaratiba lideram em número
- Entre os "outros vínculos", o padrasto responde por 73 das 110 notificações de 2025
- As notificações de lesão autoprovocada passaram de 7 em oito anos (2018 a 2025) para 33 só em 2026, ainda parcial, o que sugere mudança no registro

### Introdução do eixo

Os dados de proteção vêm das notificações do Sinan, que registram os casos que chegaram aos serviços de saúde. Por isso, medem ao mesmo tempo a ocorrência da violência e a capacidade da rede de identificá-la e notificá-la: um aumento pode refletir mais casos ou mais notificação. O salto observado em 2017 é tratado como possível quebra de série, a confirmar com a fonte. A taxa de notificações de violência de todas as naturezas e a tipificação por sexo e idade ainda não foram extraídas e aparecem como pendentes.

### Síntese do eixo

A violência familiar na primeira infância é notificada sobretudo com a mãe e o pai como prováveis autores, e se concentra no território: a Zona Oeste reúne os maiores números e as maiores taxas. Como as notificações dependem da rede que identifica e registra os casos, as diferenças entre regiões precisam ser lidas também à luz da cobertura dos serviços. O crescimento recente das notificações de lesão autoprovocada pede atenção à qualidade do registro antes de qualquer conclusão sobre o fenômeno.

Conferido em: `violencia_familiar_por_vinculo_ano.csv` (324/135 em 2011; 1.756/1.404 e 73 de 110 em 2025),
`violencia_familiar_taxa_municipio_ano.csv` (4,47 e 3,57 por mil), `violencia_familiar_por_cap.csv` (CAP 5.2: 12,07 e
10,73), `tabela_mapa_violencia_familiar_mae_2025.csv` (Santíssimo 165, Bangu 127, Guaratiba 116),
`notif_autoprovocada_por_bairro_ano.csv` (7 de 2018 a 2025; 33 em 2026). ◆ "dependem da rede que identifica e registra"
e "pede atenção à qualidade do registro" são interpretação.

---

## 🧸 Direito ao Brincar

### Principais achados

- O eixo é representado hoje só pela violência territorial, um indicador de contexto da população geral (todas as idades), de 2024
- A taxa de homicídios varia de 2,8 por 100 mil habitantes (Rocinha) a 76,3 (Centro); sem o Centro, o maior valor é o de Madureira (33,5)
- Os homicídios por ação policial são mais altos na Cidade de Deus (19,6 por 100 mil), na Penha (15,0) e em Irajá (12,9)
- Os homicídios de jovens negros se concentram em Madureira (9,2 por 100 mil), Pavuna (6,8) e Cidade de Deus (6,5)

### Introdução do eixo

O direito ao brincar depende de espaços seguros para a convivência das crianças. Nesta edição, o eixo é tratado a partir da violência territorial, que afeta o uso das ruas, praças e equipamentos públicos pelas famílias. Os dados são do Instituto de Segurança Pública, por Região Administrativa, para 2024, e se referem à população de todas as idades: medem o contexto em que as crianças vivem, não a violência sofrida por elas.

### Síntese do eixo

A violência territorial é muito desigual entre as regiões da cidade e atinge com mais força áreas da Zona Norte e a Cidade de Deus. Para as próximas edições, o eixo precisa de dados próprios da primeira infância, como a oferta e o estado de praças, parques e espaços de brincar, e de uma série histórica da violência territorial.

Conferido em: `tabela_mapa_violencia_territorial_ra_2024.csv` (taxas por RA). ◆ "afeta o uso das ruas, praças e
equipamentos" e a lista do que falta para as próximas edições são interpretação/proposta.

---

## 🍽️ Alimentação

### Principais achados

- O número de nascidos com baixo peso caiu de 7.817 em 2006 para 5.869 em 2025, acompanhando a queda dos nascimentos
- A proporção, porém, ficou estável entre 9,2% e 9,7% até 2021 e subiu para cerca de 10% a partir de 2022 (10,0% em 2025)
- Entre as crianças de 0 a 5 anos acompanhadas pelo SISVAN, 7,5% tinham baixo peso para a idade em 2025
- O excesso de peso (sobrepeso e obesidade) atingiu 16,9% em 2025, abaixo do pico de 21,5% em 2013, mas em alta desde 2021 (12,3%)

### Introdução do eixo

O eixo reúne o peso ao nascer, dos registros de nascidos vivos, e o estado nutricional das crianças de 0 a 5 anos acompanhadas nos serviços de saúde, do SISVAN. O SISVAN cobre só as crianças atendidas e pesadas na rede, não toda a população infantil, e por isso as variações anuais também refletem quem foi acompanhado. A Secretaria Municipal de Saúde recomendou separar a prematuridade do baixo peso ao nascer, classificar o excesso de peso pelo IMC por idade e sexo e incluir o aleitamento materno por Área de Planejamento; esses dados entram nas próximas edições.

### Síntese do eixo

A desnutrição e o excesso de peso convivem na primeira infância carioca. A proporção de baixo peso ao nascer não caiu com os nascimentos e voltou a subir nos últimos anos, o que reforça a atenção ao pré-natal já apontada no eixo Prioridade. O crescimento recente do excesso de peso indica a necessidade de ações de alimentação saudável desde os primeiros anos.

Conferido em: `nascidos_abaixo_peso_por_ano.csv` (7.817 em 2006, 5.869 em 2025; 9,15% a 9,71% até 2021; 10,29%,
10,39%, 9,90% e 10,00% de 2022 a 2025), `sisvan_desnutricao_por_ano.csv` (7,54% em 2025; % recalculado das contagens),
`sisvan_sobrepeso_por_ano.csv` (16,89% em 2025, 21,48% em 2013, 12,30% em 2021). ◆ "reforça a atenção ao pré-natal" e
"ações de alimentação saudável" são interpretação.

---

## 🏠 Moradia

### Principais achados

- Metade das crianças até 72 meses do CadÚnico (51,6%, ou 101.477) vive em domicílio com mais de 2 pessoas por dormitório
- 43,2% (86.393) vivem em domicílio em déficit habitacional, quase todo pelo peso do aluguel: 41,8% estão em famílias de baixa renda que gastam mais de 30% dela com aluguel
- A inadequação da infraestrutura ou da construção atinge 5,9% (11.589), com os maiores números em Santa Cruz (1.068) e Guaratiba (770)
- A falta de banheiro (0,3%) e de água canalizada (0,6%) é rara

### Introdução do eixo

Os dados de moradia vêm do Cadastro Único e cobrem, portanto, as famílias de menor renda, não toda a cidade. A classificação segue a metodologia da Fundação João Pinheiro, adaptada às variáveis do cadastro: o déficit habitacional mede a necessidade de novas moradias (domicílios improvisados, rústicos, coabitação e ônus excessivo com aluguel), e a inadequação mede problemas no domicílio existente (infraestrutura e construção). O adensamento excessivo considera mais de 2 pessoas por dormitório.

### Síntese do eixo

O principal problema habitacional das crianças do CadÚnico não é a precariedade física da casa, que é minoritária, mas o custo do aluguel e a falta de espaço: o adensamento atinge metade delas, e o ônus excessivo com aluguel, mais de quatro em cada dez. Isso aponta para políticas de acesso à moradia e de apoio ao aluguel, além de melhorias habitacionais concentradas nos territórios com mais inadequação, como Santa Cruz e Guaratiba. Os dados das ações de melhoria habitacional do programa Territórios Sociais ainda não foram incorporados.

Conferido em: `cadunico_moradia_resumo_0_a_5_2026.csv` (101.477 e 51,6%; 86.393 e 43,2%; 11.589 e 5,9%; 0,3% e
0,6%), `cadunico_deficit_componentes_0_a_5_2026.csv` (ônus com aluguel 41,8%; renda até 3 salários mínimos),
`tabela_mapa_cadunico_inadequacao_bairro_2026.csv` (Santa Cruz 1.068, Guaratiba 770). ◆ A recomendação de políticas
(acesso à moradia, apoio ao aluguel) é interpretação.
