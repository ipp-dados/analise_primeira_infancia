# Critérios de moradia do CadÚnico: déficit, inadequação (Fundação João Pinheiro) e adensamento

Como os indicadores de moradia do eixo **Moradia** são classificados. A classificação **não é feita neste projeto**: vem
pronta da silver `ctpe.silver_cadunico_familias` (banco do CTPE), calculada pelo ETL do CadÚnico — repositório
`Analise_cad_unico`, `src/cadunico_etl/moradia.py` (commit `11c4e8a`, 2026-10-06), regras na spec
`specs/2026-10-06_disability-housing/spec.md` §5 e em `docs/dicionario_dados.md` daquele repositório. Este projeto só lê as
colunas `fjp_*` e `adensamento_excessivo` e conta as crianças até 72 meses (0 a 5 anos completos) de cada família
(`specs/2026-10-06_cadunico_inclusao_moradia`). A mesma tabela, em formato aberto: `docs/criterios_fjp_cadunico.csv`.

**Referência:** Fundação João Pinheiro, *Metodologia do Déficit Habitacional e da Inadequação de Domicílios no Brasil
2016–2019* (v2.1, 2021), Quadros 3, 9 e 11. A FJP calcula com a PNAD Contínua; o CadÚnico não tem todas as variáveis da
PNAD, então os indicadores são uma **aproximação alinhada à FJP**, não a estimativa oficial de déficit ou inadequação.

## Valores de cada indicador

Cada indicador vale, por família (e, para as crianças, pela família em que vivem):
- **Sim** — o domicílio se enquadra na regra;
- **Não** — não se enquadra;
- **Não se aplica** — o domicílio está fora do universo da regra (ex.: inadequação só vale para domicílio urbano,
  permanente e não rústico);
- **Não informado** — falta um dado necessário à regra (campo vazio, rótulo fora do domínio conhecido ou 0 dormitórios).

Os indicadores-síntese (déficit, inadequação, infraestrutura, edilícia) valem **Sim** se algum componente é Sim, **Não**
se todos são Não ou Não se aplica, **Não se aplica** se todos são Não se aplica, e **Não informado** nos demais casos.
**Neste projeto os percentuais usam só Sim e Não na base** (Não se aplica e Não informado ficam fora; a base sai em cada
tabela) e os componentes não são exclusivos — um domicílio pode estar em mais de um, e as barras não somam.

## 1. Déficit habitacional

Domicílios que precisam ser repostos ou acrescentados ao estoque. Universo: todos os domicílios, salvo indicação.

| Componente | Regra (é déficit quando…) | Fidelidade à FJP |
| :-- | :-- | :-- |
| Domicílio improvisado | espécie do domicílio = particular improvisado | Igual (a própria FJP usa o CadÚnico nesse componente) |
| Domicílio rústico | só domicílio particular permanente: parede de taipa não revestida, madeira aproveitada, palha ou outro material | FJP: parede que não é de alvenaria nem madeira aparelhada. "Outro material" é grande e entra |
| Coabitação | 2 ou mais famílias no domicílio **e** mais de 2 pessoas por dormitório | **Aproximação**: a FJP identifica núcleos familiares conviventes pelo parentesco (PNAD); o CadÚnico só tem o número de famílias no domicílio |
| Ônus excessivo com aluguel | só domicílio urbano e permanente: renda familiar de até 3 salários mínimos (R$ 4.863 em 2026) **e** aluguel acima de 30% da renda familiar | A FJP usa a renda do **domicílio**; aqui é a da **família** |
| **Déficit (síntese)** | algum dos quatro acima | Indicador "ao menos um", não soma |

## 2. Inadequação de domicílios

Domicílios que não precisam ser repostos, mas têm carências. **Universo (FJP): domicílios urbanos, particulares
permanentes e não rústicos**; fora dele, "Não se aplica" (é o caso dos improvisados, coletivos, rústicos e rurais).

| Componente | Grupo | Regra (é inadequado quando…) |
| :-- | :-- | :-- |
| Iluminação não elétrica | Infraestrutura | iluminação a óleo, querosene ou gás, vela ou outra forma (elétrica sem medidor **não** é inadequada) |
| Água | Infraestrutura | sem água canalizada **ou** abastecimento por poço ou nascente, cisterna ou outra forma (fora da rede geral) |
| Esgoto | Infraestrutura | fossa rudimentar, vala a céu aberto, direto para rio, lago ou mar, ou outra forma (rede coletora ou fossa séptica são adequadas) |
| Lixo | Infraestrutura | queimado ou enterrado na propriedade, jogado em terreno baldio ou logradouro, ou em rio, lago ou mar ("tem outro destino" **não** é inadequado) |
| Banheiro | Edilícia | sem banheiro (o CadÚnico não diz se o banheiro é exclusivo, como pede a FJP) |
| Cômodos | Edilícia | todos os cômodos do domicílio são usados como dormitório |
| Piso | Edilícia | piso de terra |
| **Inadequação de infraestrutura** | Síntese | algum componente de infraestrutura |
| **Inadequação edilícia** | Síntese | algum componente edilício |
| **Inadequação (síntese)** | Síntese | algum dos sete componentes |

## 3. Adensamento excessivo (complementar, não é componente da FJP)

| Indicador | Regra |
| :-- | :-- |
| Adensamento excessivo | **mais de 2 pessoas por dormitório** (pessoas no domicílio ÷ dormitórios), em qualquer domicílio |

O limite de 2 é o de densidade que a FJP usa na coabitação. **O catálogo de indicadores da equipe diz "acima de 3 por
dormitório"** (o critério da FJP para adensamento de domicílio próprio): a diferença foi levada ao usuário
(`specs/2026-10-06_cadunico_inclusao_moradia` D11). Os títulos do site dizem o que o dado mede (mais de 2).

## 4. Resultado para as crianças até 72 meses (partição de 10/07/2026)

| Indicador | Crianças | Base (Sim + Não) | % |
| :-- | --: | --: | --: |
| Inadequação habitacional | 11.589 | 195.910 | 5,9 |
| Inadequação de infraestrutura | 9.841 | 195.622 | 5,0 |
| Inadequação edilícia | 2.234 | 195.910 | 1,1 |
| Déficit habitacional | 86.393 | 200.108 | 43,2 |
| — ônus excessivo com aluguel | 82.081 | 196.503 | 41,8 |
| Adensamento excessivo (mais de 2 por dormitório) | 101.477 | 196.655 | 51,6 |

Valores das tabelas `cadunico_moradia_resumo_0_a_5_2026.csv` e `cadunico_*_componentes_0_a_5_2026.csv` (`tabelas_finais/`),
conferidos com `ctpe.gold_cadunico_indicadores`. Os números mudam a cada nova partição do CadÚnico; as regras, só com uma
nova versão do ETL do CTPE.
