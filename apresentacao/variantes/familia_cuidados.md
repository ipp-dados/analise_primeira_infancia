---
# Variante breve: eixo Família e Cuidados (specs/2026-10-07_deck_familia_moradia), na estrutura das variantes de Inclusão,
# Alimentação e Direito ao Brincar. Mesmo tema, regras de texto e gerador do deck principal (apresentacao.md, que não muda).
# Gere com  python apresentacao/build/gera_apresentacao.py apresentacao/variantes/familia_cuidados.md
titulo: "Família e Cuidados: quem cuida das crianças e o acesso à creche e à vacina"
subtitulo: Eixo Família e Cuidados do Diagnóstico da Primeira Infância Carioca
publico: gestores
secretaria: ""
evento: Diagnóstico da Primeira Infância Carioca
data: outubro de 2026
rodape: Diagnóstico da Primeira Infância Carioca · Eixo Família e Cuidados · Instituto Pereira Passos
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
Abertura (30 s). Apresentação do eixo Família e Cuidados em cerca de 15 minutos: composição das famílias do Cadastro Único
(o ponto central), educação infantil e vacinação. Um slide de contexto vem do eixo Prioridade.
-->

---
<div class="kicker">Eixo Família e Cuidados</div>

# O que o eixo mostra

<div style="font-size:23px">

- **Quem cuida**: a composição das famílias com crianças até 72 meses no Cadastro Único — e onde elas vivem
- **Educação infantil**: crianças matriculadas em creche e pré-escola, e a mudança entre redes pública e privada na pandemia
- **Vacinação**: cobertura vacinal das crianças em relação às metas nacionais

</div>

<p class="nota forte" style="margin-top:26px"><strong>Atenção:</strong> o Cadastro Único reúne sobretudo famílias de baixa renda. Os dados de composição familiar descrevem as famílias cadastradas — <strong>não todas as famílias da cidade</strong>.</p>

<p class="nota">Até 72 meses = 0 a 5 anos completos, o recorte de primeira infância do Marco Legal.</p>

<!-- revisar -->

<!--
Mensagem (1 min): três perguntas -- quem cuida, onde as crianças passam o dia, se estão protegidas pela vacina. A
composição familiar é o centro da apresentação.
-->

---
<div class="kicker">Contexto · Eixo Prioridade</div>

# Metade das crianças da cidade está no Cadastro Único

<div class="stats" style="--n:3; margin-top:26px">
<div class="destaque" style="--c:var(--c2)"><b>{{n:razao_cadunico}}</b><span>das crianças até 72 meses da cidade estão no cadastro ({{n:pop_0_5_ripsa_mil}} na cidade)</span></div>
<div style="--c:var(--c2)"><b>{{n:cadunico_criancas_0_5}}</b><span>crianças até 72 meses, em {{n:cadunico_familias}} famílias</span></div>
<div style="--c:var(--c7)"><b>{{n:pct_cadunico_pobreza}}</b><span>das crianças cadastradas vivem em famílias em pobreza (renda por pessoa de até R$ 218)</span></div>
</div>

<p class="nota" style="margin-top:26px">O Cadastro Único é a porta de entrada dos programas sociais. Por isso, o que ele mostra sobre as famílias vale para uma parte grande — e a mais vulnerável — da primeira infância carioca.</p>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); população: estimativas Ripsa/Ministério da Saúde (2025) -->

<!-- revisar -->

<!--
Do eixo Prioridade (1 min). Razão = crianças no cadastro ÷ população estimada (Ripsa) da mesma idade. R$ 218 por pessoa é
a linha de pobreza do Bolsa Família (desde 2023).
-->

---
<div class="kicker">Eixo Família e Cuidados · Composição familiar</div>

# {{n:pct_familias_uma_adulta}} das famílias têm uma mulher como única adulta

<div class="lado">
<div class="stats" style="--n:1; gap:14px; margin:0">
<div class="destaque" style="--c:var(--c2)"><b>{{n:familias_uma_adulta}}</b><span>famílias com uma mulher como única adulta, com {{n:fam_criancas_uma_adulta}} crianças ({{n:fam_pct_criancas_uma_adulta}} das cadastradas)</span></div>
<div style="--c:var(--c1)"><b>{{n:pct_familias_dois_adultos}}</b><span>têm um homem e uma mulher; só {{n:fam_pct_um_adulto_homem}} têm um homem como único adulto</span></div>
</div>

![](fig:cadunico_familias_por_arranjo)

</div>

<p class="nota forte" style="margin-top:10px"><strong>Atenção:</strong> "uma só adulta" é aproximado pelos adultos (18 anos ou mais) <strong>registrados no cadastro</strong> — não é o conceito oficial de família monoparental.</p>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); famílias com ao menos uma criança até 72 meses -->

<!-- revisar -->

<!--
O dado mais forte do eixo (1 min 30 s). Em 4 de cada 5 famílias cadastradas com crianças pequenas, o cuidado recai sobre
uma única mulher adulta. Ressalva: a família declara quem mora com ela; um companheiro não registrado não aparece (o
cadastro pode subestimar adultos presentes). Mesmo assim, é o arranjo que a política de cuidados precisa enxergar.
-->

---
<div class="kicker">Eixo Família e Cuidados · Composição familiar e renda</div>

# Famílias com uma só adulta são as mais pobres do cadastro

<div class="lado">
<div>

**{{n:pct_uma_adulta_pobreza}}** das famílias com uma só adulta estão em pobreza ({{n:fam_uma_adulta_pobreza_n}} famílias), contra **{{n:fam_pct_dois_adultos_pobreza}}** das famílias com um homem e uma mulher.

Entre todas as famílias cadastradas em pobreza com crianças até 72 meses, **{{n:fam_pct_uma_adulta_entre_pobres}}** têm uma mulher como única adulta.

</div>

![](fig:apres_cadunico_pobreza_arranjo)

</div>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); pobreza: renda por pessoa de até R$ 218 -->

<!-- revisar -->

<!--
1 min 30 s. Uma renda para sustentar a casa e o cuidado ao mesmo tempo: a sobreposição de pobreza e cuidado solitário é o
recado para a gestão (creche, transferência de renda, rede de apoio).
-->

---
<div class="kicker">Eixo Família e Cuidados · Território · Número</div>

# Onde estão as famílias com uma só adulta: número por bairro

<div class="lado">
<div>

**Número de famílias** cadastradas com crianças até 72 meses e uma só adulta. Os maiores números estão em {{n:fam_uma_adulta_top3_bairros_n}} — bairros com muitas famílias no cadastro.

<p class="nota">Bairros com menos de 20 casos ficam sem cor: estão somados aos da mesma Região Administrativa ({{n:fam_n_bairros_somados}} bairros, {{n:fam_uma_adulta_conjuntos}} famílias).</p>

</div>

![](fig:apres_cadunico_uma_adulta_n_bairro)

</div>

<!-- revisar -->

<!--
1 min. O número acompanha o tamanho do cadastro em cada bairro: a Zona Oeste concentra as famílias. Para comparar bairros,
o próximo slide usa o percentual.
-->

---
<div class="kicker">Eixo Família e Cuidados · Território · Percentual</div>

# Uma só adulta é a regra em toda a cidade — e chega perto de 9 em 10 em favelas

<div class="lado">
<div>

**% das famílias cadastradas** com crianças até 72 meses que têm uma só adulta. Em todas as Áreas de Planejamento fica entre **{{n:fam_uma_adulta_ap_faixa}}**; a mediana dos bairros é {{n:fam_uma_adulta_mediana_bairros}}.

Os maiores percentuais: {{n:fam_uma_adulta_top5_bairros_pct}}.

<p class="nota">Escala de cor a partir de 60%: todos os bairros estão entre {{n:fam_uma_adulta_bairro_min}} e {{n:fam_uma_adulta_bairro_max}}.</p>

</div>

![](fig:apres_cadunico_uma_adulta_bairro)

</div>

<!-- revisar -->

<!--
1 min 30 s. Percentual = famílias com uma só adulta ÷ famílias cadastradas do bairro (mesma base). A diferença entre
regiões é pequena; o que muda é a escala (número) e os bolsões de maior concentração em favelas da Zona Norte (Jacarezinho,
Acari, Maré, Costa Barros) e no Centro (Gamboa). Bairros com menos de 20 casos mostram o percentual do conjunto da sua RA.
-->

---
<div class="kicker">Eixo Família e Cuidados · Educação infantil</div>

# {{n:atend_0_5}} das crianças até 72 meses estão matriculadas

<div class="lado">
<div class="stats" style="--n:1; gap:14px; margin:0">
<div style="--c:var(--c1)"><b>{{n:atend_creche}}</b><span>creche (0 a 3 anos) — meta do PNE: 50%</span></div>
<div style="--c:var(--c2)"><b>{{n:atend_pre}}</b><span>pré-escola (4 e 5 anos) — meta do PNE: 100%</span></div>
</div>

![](fig:taxa_atendimento_0_a_5_por_ano)

</div>

<p class="nota">Taxa bruta: {{n:matriculas_0_5}} matrículas em escolas do Rio em 2025 sobre a população estimada da mesma idade.</p>

<!-- revisar -->

<!--
1 min. Para a família com uma só adulta, a creche é condição para trabalhar. A creche cresceu, mas ainda está abaixo da
meta do Plano Nacional de Educação; a pré-escola, obrigatória, também não chegou a 100%.
-->

---
<div class="kicker">Eixo Família e Cuidados · Educação infantil · Pandemia</div>

# Na pandemia, a rede privada perdeu {{n:fam_queda_privada_2019_2021}} das matrículas; a pública, {{n:fam_queda_publica_2019_2021}}

<div class="lado largo">
<div class="stats" style="--n:1; gap:14px; margin:0">
<div class="destaque" style="--c:var(--c2)"><b>−{{n:fam_perda_privada_2019_2021}}</b><span>matrículas na rede privada de 2019 a 2021 ({{n:fam_mat_privada_2019}} para {{n:mat_privada_2021}})</span></div>
<div style="--c:var(--c1)"><b>−{{n:fam_perda_publica_2019_2021}}</b><span>na rede pública ({{n:fam_mat_publica_2019}} para {{n:fam_mat_publica_2021}})</span></div>
</div>

![](fig:apres_matriculas_rede_pandemia)

</div>

<!-- fonte: Censo Escolar da Educação Básica (INEP), microdados; crianças de 0 a 5 anos matriculadas em escolas do município -->

<!-- revisar -->

<!--
1 min 30 s. O choque da pandemia caiu quase todo sobre a rede privada. Com isso, a rede pública passou de {{n:fam_pct_publica_2019}}
para {{n:fam_pct_publica_2021}} das matrículas em 2021. Cuidado: o Censo Escolar não acompanha a criança -- não dá para dizer quantas
saíram da privada para a pública, só que a privada encolheu e a pública quase não mudou.
-->

---
<div class="kicker">Eixo Família e Cuidados · Educação infantil · Depois da pandemia</div>

# A rede privada voltou em 2022; a pública segue em queda

<div class="stats" style="--n:3; margin-top:26px">
<div style="--c:var(--c2)"><b>+{{n:fam_alta_privada_2021_2022}}</b><span>matrículas na rede privada de 2021 para 2022: voltou a {{n:fam_mat_privada_2022}} e ficou nesse patamar ({{n:mat_privada_2025}} em 2025)</span></div>
<div class="destaque" style="--c:var(--c1)"><b>−{{n:fam_queda_publica_2021_2025}}</b><span>matrículas na rede pública de 2021 a 2025 ({{n:mat_publica_2025}} em 2025)</span></div>
<div style="--c:var(--c7)"><b>−{{n:fam_pop_0_5_queda_2019_2025}}</b><span>crianças até 72 meses na cidade de 2019 a 2025 (estimativa Ripsa): menos crianças explicam parte da queda</span></div>
</div>

<p class="nota" style="margin-top:26px">A rede pública responde hoje por <strong>{{n:pct_publica_2025}}</strong> das matrículas — eram {{n:fam_pct_publica_2019}} em 2019 e {{n:fam_pct_publica_2021}} no auge da pandemia (2021).</p>

<!-- fonte: Censo Escolar da Educação Básica (INEP), microdados; população: estimativas Ripsa/Ministério da Saúde -->

<!-- revisar -->

<!--
1 min. Pergunta para a gestão: a queda da rede pública acompanha só a queda de nascimentos, ou há perda de vagas/demanda
não atendida? A taxa de atendimento (slide anterior) subiu no período -- sinal de que a queda de matrículas é sobretudo
demográfica. Confirmar com a SME antes de afirmar.
-->

---
<div class="kicker">Eixo Família e Cuidados · Vacinação</div>

# Em {{n:fam_vac_ano}}, {{n:fam_vac_n_meta}} das {{n:fam_vac_n}} vacinas atingiram a meta

<div class="lado largo">
<div>

A cobertura se recuperou: a mediana das vacinas foi de **{{n:fam_vac_mediana_pior}}** em {{n:fam_vac_ano_pior}} (o pior ano recente) para **{{n:fam_vac_mediana_atual}}** em {{n:fam_vac_ano}}.

Atingiram a meta: {{n:fam_vac_atingem}}.

<p class="nota">Mais longe da meta: febre amarela, hepatite A e as doses que completam o esquema (2ª dose da tríplice viral, reforço da DTP).</p>

</div>

![](fig:apres_cobertura_vacinal_metas)

</div>

<!-- revisar -->

<!--
1 min 30 s. Barra = cobertura em 2025 (verde: atingiu a meta; laranja: abaixo); traço = meta do PNI (90% BCG e rotavírus,
95% as demais); círculo = 2022. Abaixo da meta: {{n:fam_vac_abaixo}}. 2026 fica fora: ano em curso. Cobertura acima de
100% acontece (doses aplicadas sobre população estimada). Metas a confirmar com a SMS (calendário vigente).
-->

---
<div class="kicker">Eixo Família e Cuidados</div>

# Limites e próximos passos

<div class="dois">
<div>

**Limites**

- Composição familiar só das famílias do Cadastro Único, pelos adultos registrados
- Matrículas e vacinação só para a cidade toda: sem recorte por bairro
- Censo Escolar não acompanha a criança: não mostra trocas de rede

</div>
<div>

**Próximos passos**

- Matrículas e vacinação por território (escola, unidade de saúde)
- Cruzar composição familiar com acesso à creche no Cadastro Único
- Textos de análise na versão de 13 de outubro de 2026

</div>
</div>

<!-- revisar -->

<!--
1 min. Os próximos passos são sugestão do IPP, a revisar com a equipe.
-->

---
<div class="kicker">Eixo Família e Cuidados · Resumo</div>

# Resumo dos indicadores

<div style="font-size:18px">

| Indicador | Número | % | Base do percentual |
| :-- | --: | --: | :-- |
| Crianças até 72 meses no Cadastro Único | {{n:cadunico_criancas_0_5}} | {{n:razao_cadunico}} | crianças até 72 meses da cidade (Ripsa) |
| Famílias com uma mulher como única adulta | **{{n:familias_uma_adulta}}** | {{n:pct_familias_uma_adulta}} | {{n:cadunico_familias}} famílias cadastradas |
| Delas, em pobreza | {{n:fam_uma_adulta_pobreza_n}} | {{n:pct_uma_adulta_pobreza}} | famílias com uma só adulta |
| Taxa de atendimento escolar, 0 a 5 anos (2025) | {{n:matriculas_0_5}} | **{{n:atend_0_5}}** | população estimada da idade |
| Creche (0 a 3) / pré-escola (4 e 5) | — | {{n:atend_creche}} / {{n:atend_pre}} | metas do PNE: 50% / 100% |
| Matrículas na rede privada, 2019 → 2021 | −{{n:fam_perda_privada_2019_2021}} | −{{n:fam_queda_privada_2019_2021}} | matrículas de 2019 |
| Matrículas na rede pública, 2019 → 2021 | −{{n:fam_perda_publica_2019_2021}} | −{{n:fam_queda_publica_2019_2021}} | matrículas de 2019 |
| Vacinas na meta do PNI ({{n:fam_vac_ano}}) | {{n:fam_vac_n_meta}} de {{n:fam_vac_n}} | mediana {{n:fam_vac_mediana_atual}} | cobertura vacinal |

</div>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); Censo Escolar (INEP); estimativas Ripsa/Ministério da Saúde; EPI/SVS-Rio -->

<!--
Os números do eixo numa só tabela, para consulta.
-->

---
<!-- _class: encerramento -->
<!-- _footer: '' -->

<div class="kicker">Instituto Pereira Passos</div>

# Obrigado

## Perguntas e sugestões

**{{contato}}** · {{url_site}}

<img class="logo" src="img/ipp-logo.png" alt="Prefeitura do Rio · Instituto Pereira Passos">
