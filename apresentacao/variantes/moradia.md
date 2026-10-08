---
# Variante: eixo Moradia + dado pontual do Territórios Sociais (specs/2026-10-08_deck_moradia), na estrutura das
# variantes breves (variantes/inclusao.md). Mesmo tema, regras de texto e gerador do deck principal.
# Dado pontual (apresentacao/variantes/moradia/, build/territorios_sociais.py) só nesta apresentação (constituição §3).
# Gere com  python apresentacao/build/gera_apresentacao.py apresentacao/variantes/moradia.md
titulo: "Moradia: crianças em domicílios inadequados"
subtitulo: Eixo Moradia do Diagnóstico da Primeira Infância Carioca e dado do programa Territórios Sociais
publico: gestores
secretaria: ""
evento: Diagnóstico da Primeira Infância Carioca
data: outubro de 2026
rodape: Diagnóstico da Primeira Infância Carioca · Eixo Moradia · Instituto Pereira Passos
url_site: https://ipp-dados.github.io/analise_primeira_infancia/
contato: pesquisaeavaliacao.ipp@prefeitura.rio
blocos: []
---

<!-- _class: capa -->
<!-- _paginate: false -->
<!-- _footer: '' -->

<div class="kicker">Instituto Pereira Passos · {{evento}}</div>

# {{titulo}}

## {{subtitulo}}

<!-- se: com_secretaria -->
**{{secretaria}}**
<!-- /se -->

{{data}}

<img class="logo" src="img/ipp-logo.png" alt="Prefeitura do Rio · Instituto Pereira Passos">

<!--
Abertura (30 s). Duas partes: (1) o eixo Moradia do diagnóstico, com o Cadastro Único da cidade inteira; (2) um dado
pontual do programa Territórios Sociais sobre domicílios com inadequação habitacional e crianças até 72 meses.
-->

---
<div class="kicker">Eixo Moradia</div>

# O que esta apresentação mostra

<div class="dois">
<div>

**1. Cadastro Único — a cidade**

- Crianças até 72 meses em domicílios com **inadequação habitacional** (critério da Fundação João Pinheiro; extração e cálculo do IPP)
- **Adensamento excessivo** e **déficit habitacional**
- Onde estão: **número** e **percentual** por bairro

</div>
<div>

**2. Territórios Sociais — dado pontual**

- Domicílios **visitados pelo programa** com inadequação habitacional e crianças até 72 meses
- Por **condição** (edilícia, entorno ou as duas) e por item
- Domicílios com **registro de deficiência**

</div>
</div>

<p class="nota forte" style="margin-top:22px"><strong>Atenção:</strong> as duas partes usam bases e critérios diferentes (Fundação João Pinheiro × critérios do Eixo Urbano do programa). Os números não se somam nem se comparam diretamente.</p>

<p class="nota">Até 72 meses = 0 a 5 anos completos, o recorte de primeira infância do Marco Legal.</p>

<!-- revisar -->

---
<div class="kicker">Eixo Moradia · Conceitos</div>

# Conceitos usados nesta apresentação

<div class="conceitos">
<div style="--c:var(--c2)">
<h3>Fundação João Pinheiro (FJP)</h3>
<p class="sub">Parte 1 · critério da FJP, referência nacional; extração do Cadastro Único e cálculo do IPP</p>
<p><b>Inadequação habitacional</b> — a casa precisa de melhoria: <strong>infraestrutura</strong> (água, esgoto, lixo, energia) ou <strong>edilícia</strong> (sem banheiro, piso de terra, todos os cômodos como dormitório).</p>
<p><b>Déficit habitacional</b> — falta uma moradia: domicílio improvisado ou rústico, coabitação ou aluguel acima de 30% da renda.</p>
<p><b>Adensamento excessivo</b> — mais de 2 pessoas por dormitório.</p>
</div>
<div style="--c:var(--c4)">
<h3>Territórios Sociais</h3>
<p class="sub">Partes 2 e 3 · programa do IPP com a ONU-Habitat, nas áreas de menor desenvolvimento social</p>
<p><b>Critérios do Eixo Urbano</b> (do programa Territórios Sociais) — três condições de inadequação:</p>
<p><b>1</b> · só <strong>edilícia</strong>: paredes, piso, chuveiro, vaso, pia</p>
<p><b>2</b> · só <strong>entorno</strong>: sem água ou esgoto adequados</p>
<p><b>3</b> · as <strong>duas</strong></p>
</div>
</div>

<p class="nota" style="margin-top:12px">Até 72 meses = 0 a 5 anos completos, o recorte de primeira infância do Marco Legal. Os critérios da FJP e do Eixo Urbano são diferentes: os números das duas partes não se comparam diretamente.</p>

<!-- revisar -->

<!--
Slide de glossário pedido pelo usuário (2026-10-08), antes da Parte 1. Ônus excessivo com aluguel: definição da FJP
(renda familiar de até 3 salários mínimos e aluguel acima de 30% da renda) — o CTPE aplica a sua aproximação no
Cadastro Único; confirmar a redação com a equipe.
-->

---
<!-- _class: secao -->
<!-- _footer: '' -->

<div class="kicker">Parte 1</div>

# Moradia no Cadastro Único

## Crianças até 72 meses das famílias cadastradas, na cidade inteira

---
<div class="kicker">Eixo Moradia · Inadequação habitacional</div>

# {{n:mora_inad_n}} crianças cadastradas vivem em domicílio inadequado

<div class="stats" style="--n:3; margin-top:26px">
<div class="destaque" style="--c:var(--c2)"><b>{{n:mora_inad_n}}</b><span>crianças até 72 meses em domicílios com inadequação habitacional — {{n:mora_inad_pct}} das {{n:mora_criancas_base}} cadastradas</span></div>
<div style="--c:var(--c2)"><b>{{n:mora_infra_n}}</b><span>com inadequação de <strong>infraestrutura</strong> (água, esgoto, lixo, energia) — {{n:mora_infra_pct}}</span></div>
<div style="--c:var(--c3)"><b>{{n:mora_edil_n}}</b><span>com inadequação <strong>edilícia</strong> (banheiro, cômodos, piso) — {{n:mora_edil_pct}}</span></div>
</div>

<p class="nota" style="margin-top:26px">Uma criança pode estar nos dois grupos. São {{n:mora_inad_familias}} famílias. Critério da Fundação João Pinheiro; extração e cálculo do IPP.</p>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); critério da Fundação João Pinheiro, extração e cálculo do IPP; crianças até 72 meses -->

<!-- revisar -->

<!--
A infraestrutura (o entorno do domicílio) pesa muito mais que a construção em si: 5,0% × 1,1%.
-->

---
<div class="kicker">Eixo Moradia · Inadequação habitacional</div>

# Esgoto e água são as falhas mais comuns

<div class="lado">
<div>

O esgoto inadequado (fossa rudimentar, vala, rio ou mar) e a água sem canalização ou fora da rede geral lideram os componentes.

<p class="nota">Componentes não exclusivos: um domicílio pode ter mais de um.</p>

</div>

![](fig:cadunico_criancas_inadequacao_componentes)

</div>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); critério da Fundação João Pinheiro, extração e cálculo do IPP; componentes não exclusivos -->

<!-- revisar -->

---
<div class="kicker">Eixo Moradia · Território · Número</div>

# Onde estão as crianças em domicílio inadequado: número por bairro

<div class="lado">
<div>

**Número de crianças** até 72 meses em domicílio com inadequação. Os maiores números estão em {{n:mora_inad_top3_bairros_n}}.

<p class="nota">Bairros com menos de 20 casos ficam sem cor: estão somados aos da mesma Região Administrativa ({{n:mora_inad_n_bairros_somados}} bairros, {{n:mora_inad_criancas_conjuntos}} crianças, na tabela do site).</p>

</div>

![](fig:apres_cadunico_inadequacao_n_bairro)

</div>

<!-- revisar -->

<!--
Mapa de número: novo, pedido para esta apresentação (2026-10-08); vai também para o site (ROADMAP). Contagem -> classes
discretas (convenção do projeto). O número mostra onde está o volume de crianças — onde a ação alcança mais gente.
-->

---
<div class="kicker">Eixo Moradia · Território · Percentual</div>

# Entre as crianças do Cadastro Único: % em domicílio inadequado, por bairro

<div class="lado baixo">
<div>

<p class="nota forte" style="margin-top:0"><strong>Universo do Cadastro Único:</strong> % das crianças <strong>cadastradas</strong> que moram no bairro — não representa todas as crianças do bairro.</p>

A mediana dos bairros é **{{n:mora_inad_mediana_bairros}}**, perto da média das crianças cadastradas da cidade ({{n:mora_inad_pct}}).

<p class="nota">Extremos com a cor máxima, listados no rodapé.</p>

</div>

![](fig:apres_cadunico_inadequacao_bairro)

</div>

<!-- revisar -->

<!--
O percentual mostra onde o problema é mais frequente entre as crianças cadastradas do bairro; o número (slide anterior),
onde está o volume. A zona oeste (Santa Cruz, Guaratiba, Campo Grande) aparece nos dois.
-->

---
<div class="kicker">Eixo Moradia · Adensamento e déficit</div>

# Metade das crianças cadastradas vive em casa adensada

<div class="stats" style="--n:3; margin-top:26px">
<div class="destaque" style="--c:var(--c2)"><b>{{n:mora_adens_pct}}</b><span>das crianças ({{n:mora_adens_n}}) em domicílio com <strong>mais de 2 pessoas por dormitório</strong></span></div>
<div style="--c:var(--c3)"><b>{{n:mora_deficit_pct}}</b><span>das crianças ({{n:mora_deficit_n}}) em família no <strong>déficit habitacional</strong> (FJP)</span></div>
<div style="--c:var(--c3)"><b>{{n:mora_aluguel_pct}}</b><span>das crianças em família com <strong>ônus excessivo com aluguel</strong> — o principal componente do déficit</span></div>
</div>

<p class="nota" style="margin-top:26px">Sem banheiro: {{n:mora_banheiro_pct}} das crianças; sem água canalizada: {{n:mora_agua_pct}}.</p>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); critério da Fundação João Pinheiro, extração e cálculo do IPP; crianças até 72 meses -->

<!-- revisar -->

<!--
O problema mais comum das famílias cadastradas não é a casa precária, é a casa cheia e o aluguel caro. Adensamento: limite
de densidade da FJP (mais de 2 por dormitório; o catálogo da equipe dizia "acima de 3" — decisão de 2026-10-06).
-->

---
<div class="kicker">Eixo Moradia · Déficit habitacional</div>

# O aluguel pesa mais que a precariedade da casa

<div class="lado">
<div>

**{{n:mora_aluguel_n}}** crianças vivem em famílias que gastam parte excessiva da renda com aluguel.

Domicílio improvisado, domicílio rústico e coabitação somam bem menos.

</div>

![](fig:cadunico_criancas_deficit_componentes)

</div>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); critério da Fundação João Pinheiro, extração e cálculo do IPP; componentes não exclusivos -->

<!-- revisar -->

---
<div class="kicker">Eixo Moradia · Território · Número</div>

# Crianças em casa adensada: número por bairro

<div class="lado">
<div>

**Número de crianças** até 72 meses em domicílio com mais de 2 pessoas por dormitório. Os maiores números: {{n:mora_adens_top3_bairros_n}}.

<p class="nota">Bairros com menos de 20 casos ficam sem cor: estão somados aos da mesma Região Administrativa ({{n:mora_adens_n_bairros_somados}} bairros, {{n:mora_adens_criancas_conjuntos}} crianças).</p>

</div>

![](fig:apres_cadunico_adensamento_n_bairro)

</div>

<!-- revisar -->

---
<div class="kicker">Eixo Moradia · Território · Percentual</div>

# Entre as crianças do Cadastro Único: % em casa adensada, por bairro

<div class="lado baixo">
<div>

<p class="nota forte" style="margin-top:0"><strong>Universo do Cadastro Único:</strong> % das crianças <strong>cadastradas</strong> que moram no bairro em domicílio com mais de 2 pessoas por dormitório — não representa todas as crianças do bairro.</p>

A mediana dos bairros é **{{n:mora_adens_mediana_bairros}}**: o adensamento é comum em quase toda a cidade.

<p class="nota">Extremos com a cor máxima, listados no rodapé.</p>

</div>

![](fig:apres_cadunico_adensamento_bairro)

</div>

<!-- revisar -->

---
<!-- _class: secao -->
<!-- _footer: '' -->

<div class="kicker">Parte 2 · Dado pontual</div>

# Territórios Sociais

## Domicílios visitados pelo programa com inadequação habitacional e crianças até 72 meses

---
<div class="kicker">Territórios Sociais · O programa e o dado</div>

# Um levantamento casa a casa, nas áreas mais vulneráveis

<div class="dois">
<div>

**O programa**

- Do **Instituto Pereira Passos**, com a ONU-Habitat: visita as famílias nas áreas de menor Índice de Desenvolvimento Social da cidade e as encaminha aos serviços
- O diagnóstico das visitas orienta ações de melhoria habitacional, como o **Casa Carioca** (Ação Comunitária)

</div>
<div>

**As condições (critérios do Eixo Urbano)**

- **Condição 1** — só inadequação **edilícia**: paredes, piso, chuveiro, vaso sanitário, pia
- **Condição 2** — só **entorno** sem infraestrutura adequada: abastecimento de água, esgotamento sanitário
- **Condição 3** — as **duas** inadequações

</div>
</div>

<p class="nota forte" style="margin-top:20px"><strong>Dado pontual:</strong> só os domicílios visitados pelo programa — não a cidade inteira.</p>

<!-- fonte: Territórios Sociais (IPP/ONU-Habitat); Prefeitura do Rio -->

<!-- revisar -->

<!--
Confirmar com a equipe do programa: período das visitas, quais fases/territórios entram na planilha e a relação exata
com o Casa Carioca (o Casa Carioca usa o diagnóstico do Territórios Sociais para escolher as casas — fonte: parecer social
do Casa Carioca, Ação Comunitária).
-->

---
<div class="kicker">Territórios Sociais · Primeira infância</div>

# {{n:ts_domicilios}} domicílios inadequados com crianças até 72 meses

<div class="stats" style="--n:3; margin-top:26px">
<div style="--c:var(--c3)"><b>{{n:ts_cond1_n}}</b><span><strong>Condição 1</strong> — só edilícia ({{n:ts_cond1_pct}}; {{n:ts_cond1_criancas}} crianças)</span></div>
<div class="destaque" style="--c:var(--c2)"><b>{{n:ts_cond2_n}}</b><span><strong>Condição 2</strong> — só entorno: água ou esgoto ({{n:ts_cond2_pct}}; {{n:ts_cond2_criancas}} crianças)</span></div>
<div style="--c:var(--c2)"><b>{{n:ts_cond3_n}}</b><span><strong>Condição 3</strong> — edilícia e entorno ({{n:ts_cond3_pct}}; {{n:ts_cond3_criancas}} crianças)</span></div>
</div>

<p class="nota" style="margin-top:26px">São <strong>{{n:ts_criancas}} crianças</strong> até 72 meses; {{n:ts_pct_uma_crianca}} dos domicílios têm uma só.</p>

<!-- fonte: Territórios Sociais (IPP), dado pontual; domicílios com inadequação habitacional e crianças até 72 meses -->

<!-- revisar -->

<!--
A planilha diz "0 a 5" (o roteiro da reunião dizia 0 a 6): o recorte do deck é até 72 meses, o padrão do projeto.
-->

---
<div class="kicker">Territórios Sociais · Primeira infância</div>

# O entorno define a inadequação: {{n:ts_entorno_pct}} dos domicílios inadequados não têm água ou esgoto adequados

<div class="lado">
<div>

Dos {{n:ts_domicilios}} domicílios **já classificados como inadequados** com crianças, **{{n:ts_entorno_n}}** (condições 2 e 3) têm problema de água ou esgoto no entorno — que não se resolve só com obra dentro da casa.

<p class="nota">A Condição 1 (só edilícia) é a que a melhoria dentro da casa alcança diretamente.</p>

</div>

![](fig:apres_ts_condicao)

</div>

<!-- revisar -->

<!--
Leitura para a gestão: a maior parte do problema nesses domicílios depende de saneamento (rede de água e esgoto), não só
de reforma. Mesma direção do Cadastro Único (infraestrutura 5,0% × edilícia 1,1%), em base diferente.
-->

---
<div class="kicker">Territórios Sociais · Primeira infância</div>

# Esgoto: o item inadequado em {{n:ts_esgoto_pct}} dos domicílios com crianças

<div class="lado">
<div>

Esgotamento sanitário ({{n:ts_esgoto_n}}) e abastecimento de água ({{n:ts_agua_n}}) lideram. Dentro da casa, os mais comuns são **pia** ({{n:ts_pia_pct}}) e **piso** ({{n:ts_piso_pct}}).

<p class="nota">Itens não exclusivos: um domicílio pode ter mais de um. "Não sabe / não respondeu" fica fora da contagem.</p>

</div>

![](fig:apres_ts_itens)

</div>

<!-- revisar -->

<!--
Piso inadequado e falta de pia pesam na primeira infância: a criança pequena passa o dia no chão, e sem pia a higiene
das mãos e dos alimentos fica mais difícil.
-->

---
<!-- _class: secao -->
<!-- _footer: '' -->

<div class="kicker">Parte 3 · Novo recorte</div>

# Territórios Sociais e deficiência

## Domicílios inadequados com crianças até 72 meses e registro de deficiência ou transtorno

---
<div class="kicker">Territórios Sociais · Primeira infância e deficiência</div>

# {{n:ts_def_domicilios}} domicílios inadequados com crianças e registro de deficiência

<div class="stats" style="--n:3; margin-top:26px">
<div style="--c:var(--c3)"><b>{{n:ts_cond1_def}}</b><span><strong>Condição 1</strong> — só edilícia</span></div>
<div class="destaque" style="--c:var(--c2)"><b>{{n:ts_cond2_def}}</b><span><strong>Condição 2</strong> — só entorno</span></div>
<div style="--c:var(--c2)"><b>{{n:ts_cond3_def}}</b><span><strong>Condição 3</strong> — edilícia e entorno</span></div>
</div>

<p class="nota" style="margin-top:26px">{{n:ts_def_pct}} dos {{n:ts_domicilios}} domicílios com crianças até 72 meses têm registro de deficiência ou transtorno.</p>

<!-- fonte: Territórios Sociais (IPP), dado pontual; domicílios com inadequação habitacional e crianças até 72 meses -->

<!-- revisar -->

<!--
CONFIRMAR com a equipe: a deficiência registrada é da criança ou de qualquer morador do domicílio? A planilha traz os
campos no nível do domicílio. Até confirmar, o texto diz "domicílio com registro de deficiência".
-->

---
<div class="kicker">Territórios Sociais · Primeira infância e deficiência</div>

# Espectro autista é o registro mais comum

<div class="lado">
<div>

O tipo mais registrado é **{{n:ts_def_tipo1_nome}}**: {{n:ts_def_tipo1_n}} domicílios, {{n:ts_def_tipo1_pct}} dos que têm registro de deficiência.

Em {{n:ts_def_mais_de_um}} domicílios há mais de um tipo registrado.

<p class="nota">Tipos não exclusivos. Números pequenos: ler como ordem de grandeza.</p>

</div>

![](fig:apres_ts_deficiencia_tipo)

</div>

<!-- revisar -->

<!--
Visual (6) e auditiva (11) têm menos de 20 domicílios: sem recorte territorial não identificam ninguém, mas não publicar
esses números por território (regra de privacidade do projeto, contagem mínima de 20).
-->

---
<div class="kicker">Territórios Sociais · Primeira infância e deficiência · Território</div>

# Criança com TEA: concentração em Santa Cruz

Domicílios do programa com **criança até 72 meses com transtorno do espectro autista (TEA)**: aglomerado em **Santa Cruz**; os demais, na zona norte, no Centro e em Guaratiba.

<p style="text-align:center; margin:4px 0 0"><img src="fig:mapa_moradia_ts" style="max-height:395px"></p>

<!-- fonte: Territórios Sociais (IPP); mapa da Coordenadoria de Pesquisa, Avaliação e Políticas Públicas (IPP), base Data.Rio; dado pontual -->

<!-- revisar -->

<!--
Mapa recebido pronto da equipe do programa (2026-10-08, apresentacao/variantes/moradia/mapa_moradia_ts.jpeg). Um ponto por
domicílio. Leitura visual: aglomerado em Santa Cruz; pontos na zona norte (Inhaúma, Méier, Tijuca), Centro, Guaratiba e
zona sul (favelas). O título da imagem diz "0 a 5 anos" (= até 72 meses).
-->

---
<div class="kicker">Eixo Moradia · Método</div>

# Limites e próximos passos

<div class="dois" style="font-size:19px">
<div>

**Limites**

- **Cadastro Único**: informação declarada pelas famílias de baixa renda cadastradas — não é amostra da população; bairro aproximado pelo CEP
- **Critério da FJP** aplicado ao cadastro com aproximações (ex.: ônus com aluguel pela renda declarada); "não informado" fica fora da base
- **Territórios Sociais**: só os domicílios visitados nas áreas de menor IDS; critérios do Eixo Urbano, diferentes dos da FJP
- **Deficiência** registrada no domicílio; números pequenos por tipo
- Bases e datas diferentes: não somar nem comparar diretamente

</div>
<div>

**Próximos passos**

- **Harmonizar critérios**: aplicar o critério da FJP aos domicílios do Territórios Sociais, para comparar as duas bases
- **Cruzar** Territórios Sociais e Cadastro Único pelas famílias em comum
- **Dimensionar o universo** além do cadastro com o Censo 2022 (saneamento e características dos domicílios)
- **Medir a cobertura das ações de mitigação** do Casa Carioca entre os domicílios inadequados com crianças
- Recortes territoriais sempre com a regra de privacidade (mínimo de 20 casos)

</div>
</div>

<!-- revisar -->

<!--
Revisto a pedido do usuário (2026-10-08): limites e próximos passos do ponto de vista metodológico, sem itens do roadmap
do site e sem menção ao total geral do programa (essa planilha não existirá).
-->

---
<div class="kicker">Eixo Moradia · Resumo</div>

# Resumo dos indicadores

<div style="font-size:18px">

| Indicador | Número | % | Base do percentual |
| :-- | --: | --: | :-- |
| **Cadastro Único** — crianças em inadequação habitacional | **{{n:mora_inad_n}}** | {{n:mora_inad_pct}} | crianças cadastradas |
| Inadequação de infraestrutura | {{n:mora_infra_n}} | {{n:mora_infra_pct}} | crianças cadastradas |
| Inadequação edilícia | {{n:mora_edil_n}} | {{n:mora_edil_pct}} | crianças cadastradas |
| Adensamento excessivo (mais de 2 por dormitório) | **{{n:mora_adens_n}}** | {{n:mora_adens_pct}} | crianças cadastradas |
| Déficit habitacional (FJP) | {{n:mora_deficit_n}} | {{n:mora_deficit_pct}} | crianças cadastradas |
| **Territórios Sociais** — domicílios inadequados com crianças | **{{n:ts_domicilios}}** | — | — |
| Condição 1 / 2 / 3 | {{n:ts_cond1_n}} / {{n:ts_cond2_n}} / {{n:ts_cond3_n}} | {{n:ts_cond1_pct}} / {{n:ts_cond2_pct}} / {{n:ts_cond3_pct}} | domicílios com crianças |
| Com registro de deficiência | **{{n:ts_def_domicilios}}** | {{n:ts_def_pct}} | domicílios com crianças |

</div>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}), critério da Fundação João Pinheiro, extração e cálculo do IPP; Territórios Sociais (IPP), dado pontual -->

---
<!-- _class: encerramento -->
<!-- _footer: '' -->

<div class="kicker">Instituto Pereira Passos</div>

# Obrigado

## Perguntas e sugestões

**{{contato}}** · {{url_site}}

<img class="logo" src="img/ipp-logo.png" alt="Prefeitura do Rio · Instituto Pereira Passos">
