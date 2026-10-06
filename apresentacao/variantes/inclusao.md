---
# Variante breve: eixo Inclusão (specs/2026-10-06_deck_inclusao). Mesmo tema, regras de texto e gerador do deck principal
# (apresentacao.md, que não muda). Gere com  python apresentacao/build/gera_apresentacao.py variantes/inclusao.md
titulo: "Inclusão: crianças com deficiência no Cadastro Único"
subtitulo: Eixo Inclusão do Diagnóstico da Primeira Infância Carioca
publico: gestores
secretaria: ""
evento: Diagnóstico da Primeira Infância Carioca
data: outubro de 2026
rodape: Diagnóstico da Primeira Infância Carioca · Eixo Inclusão · Instituto Pereira Passos
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
Abertura (30 s). Apresentação curta, só do eixo Inclusão, com os dados novos do Cadastro Único.
-->

---
<div class="kicker">Eixo Inclusão</div>

# O que o eixo mostra

<div style="font-size:23px">

- Quantas crianças até 72 meses com deficiência estão no **Cadastro Único**, de que tipo e em que bairros
- Quantas famílias com essas crianças recebem o **Benefício de Prestação Continuada (BPC)**
- Dados da **extração rotineira** do Cadastro Único ({{n:incl_particao}}), que substitui o dado pontual usado antes

</div>

<p class="nota forte" style="margin-top:26px"><strong>Atenção:</strong> o Cadastro Único reúne sobretudo famílias de baixa renda e registra a deficiência declarada no cadastro. Os números descrevem as crianças cadastradas — <strong>não são a prevalência de deficiência na cidade</strong>.</p>

<p class="nota">Até 72 meses = 0 a 5 anos completos, o recorte de primeira infância do Marco Legal.</p>

<!-- revisar -->

<!--
Mensagem: o eixo deixou de depender de uma extração pontual; agora sai da mesma base que alimenta o resto do diagnóstico e será atualizado a cada nova extração.
-->

---
<div class="kicker">Eixo Inclusão</div>

# {{n:incl_criancas_deficiencia}} crianças até 72 meses com deficiência no Cadastro Único

<div class="stats" style="--n:3; margin-top:26px">
<div class="destaque" style="--c:var(--c2)"><b>{{n:incl_criancas_deficiencia}}</b><span>crianças até 72 meses com deficiência — {{n:incl_pct_criancas_deficiencia}} das {{n:incl_criancas_cadunico}} cadastradas</span></div>
<div style="--c:var(--c2)"><b>{{n:incl_familias_deficiencia}}</b><span>famílias com ao menos uma criança com deficiência ({{n:incl_pct_familias_deficiencia}} das famílias com crianças até 72 meses)</span></div>
<div style="--c:var(--c2)"><b>{{n:incl_pct_bpc}}</b><span>das famílias com a informação recebem o BPC por deficiência</span></div>
</div>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}) -->

<!-- revisar -->

<!--
Os três números da aba Inclusão do site. Famílias e crianças quase coincidem: em geral, uma criança com deficiência por família.
-->

---
<div class="kicker">Eixo Inclusão</div>

# Tipos de deficiência registrados

<div class="lado">
<div>

Os tipos mais registrados são **{{n:incl_tipo1_nome}}** ({{n:incl_tipo1_pct}} das crianças com deficiência), **deficiência {{n:incl_tipo2_nome}}** ({{n:incl_tipo2_pct}}) e **{{n:incl_tipo3_nome}}** ({{n:incl_tipo3_pct}}).

<p class="nota">Uma criança pode ter mais de um tipo registrado: as barras não somam o total de crianças com deficiência.</p>

</div>

![](fig:cadunico_criancas_por_tipo_deficiencia)

</div>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); crianças até 72 meses com deficiência -->

<!-- revisar -->

<!--
Surdez, cegueira e baixa visão são grupos pequenos na cidade: aparecem só no total do município, nunca por bairro (regra de proteção de dados do Cadastro Único).
-->

---
<div class="kicker">Eixo Inclusão · Território · Número</div>

# Onde estão as crianças com deficiência: número por bairro

<div class="lado">
<div>

**Número de crianças** até 72 meses com deficiência no cadastro. Os maiores números estão em {{n:incl_top3_bairros_n}} — bairros com muitas crianças cadastradas.

<p class="nota">Bairros com menos de 20 casos ficam sem cor: estão somados aos da mesma Região Administrativa ({{n:incl_n_bairros_somados}} bairros, {{n:incl_criancas_conjuntos}} crianças, na tabela do site).</p>

</div>

![](fig:apres_cadunico_deficiencia_n_bairro)

</div>

<!-- revisar -->

<!--
O número acompanha o tamanho do bairro e do cadastro: a Zona Oeste concentra crianças cadastradas. Para comparar bairros, o próximo slide usa o percentual.
-->

---
<div class="kicker">Eixo Inclusão · Território · Percentual</div>

# Percentual de crianças com deficiência por bairro

<div class="lado">
<div>

**% das crianças cadastradas** (até 72 meses) que têm deficiência, em cada bairro — não o número de crianças.

A mediana dos bairros é **{{n:incl_mediana_bairros}}**: de {{n:incl_bairro_min}} a {{n:incl_bairro_max}}.

<p class="nota">Bairros com menos de 20 casos mostram o percentual do conjunto dos bairros pequenos da sua Região Administrativa.</p>

</div>

![](fig:apres_cadunico_deficiencia_bairro)

</div>

<!-- revisar -->

<!--
Percentual = crianças com deficiência ÷ crianças cadastradas do bairro (mesma base). Cautela: o registro depende de diagnóstico e de acesso ao cadastro; diferenças pequenas entre bairros não são conclusivas. Bairro atribuído pelo CEP da família (correspondência CEP-bairro do CTPE); crianças com CEP fora da correspondência entram só no total do município.
-->

---
<div class="kicker">Eixo Inclusão · Proteção social</div>

# {{n:incl_pct_bpc}} das famílias com criança com deficiência recebem o BPC

<div class="stats" style="--n:3; margin-top:26px">
<div class="destaque" style="--c:var(--c2)"><b>{{n:incl_bpc_familias}}</b><span>famílias recebem o BPC por deficiência</span></div>
<div style="--c:var(--c3)"><b>{{n:incl_sem_bpc}}</b><span>famílias não recebem</span></div>
<div style="--c:var(--c7)"><b>{{n:incl_bpc_sem_info}}</b><span>famílias sem a informação no cadastro</span></div>
</div>

<p class="nota" style="margin-top:26px">O BPC por deficiência é registrado para a <strong>família</strong>, não para a criança: o benefício pode ser de outro membro. O percentual considera as {{n:incl_bpc_base}} famílias com a informação.</p>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); famílias com ao menos uma criança até 72 meses com deficiência -->

<!-- revisar -->

<!--
Leitura para a gestão: a maior parte das famílias com criança com deficiência não recebe o BPC por deficiência. Elegibilidade (renda, avaliação) não está no cadastro -- não dá para dizer quantas teriam direito.
-->

---
<div class="kicker">Eixo Inclusão</div>

# Limites e próximos passos

<div class="dois">
<div>

**Limites**

- Só as crianças do Cadastro Único, com a deficiência declarada no cadastro
- BPC registrado para a família, não para a criança
- Bairro pelo CEP: crianças com CEP fora da correspondência ficam só no total da cidade

</div>
<div>

**Próximos passos**

- Cuidados e ajudas recebidos pelas crianças com deficiência (dado já disponível no cadastro)
- Cruzar deficiência com renda e moradia das famílias
- Textos de análise na versão de 13 de outubro de 2026

</div>
</div>

<!-- revisar -->

<!--
Interno (não falar sem a revisão do usuário): a extração pontual de agosto de 2026 tinha 25.995 crianças de 0 a 6 anos com deficiência; a extração rotineira tem 7.919 de 0 a 5. A faixa de 6 anos não explica a diferença -- pendente de revisão (ROADMAP).
-->

---
<div class="kicker">Eixo Inclusão · Resumo</div>

# Resumo dos indicadores

<div style="font-size:19px">

| Indicador | Número | % | Base do percentual |
| :-- | --: | --: | :-- |
| Crianças até 72 meses no Cadastro Único | {{n:incl_criancas_cadunico}} | — | — |
| Crianças com deficiência | **{{n:incl_criancas_deficiencia}}** | {{n:incl_pct_criancas_deficiencia}} | crianças cadastradas |
| Tipo mais registrado: {{n:incl_tipo1_nome}} | {{n:incl_tipo1_n}} | {{n:incl_tipo1_pct}} | crianças com deficiência |
| Deficiência {{n:incl_tipo2_nome}} | {{n:incl_tipo2_n}} | {{n:incl_tipo2_pct}} | crianças com deficiência |
| Deficiência {{n:incl_tipo3_nome}} | {{n:incl_tipo3_n}} | {{n:incl_tipo3_pct}} | crianças com deficiência |
| Famílias com criança com deficiência | **{{n:incl_familias_deficiencia}}** | {{n:incl_pct_familias_deficiencia}} | {{n:incl_familias_cadunico}} famílias com criança até 72 meses |
| Recebem o BPC por deficiência | **{{n:incl_bpc_familias}}** | {{n:incl_pct_bpc}} | {{n:incl_bpc_base}} famílias com a informação |
| Não recebem o BPC | {{n:incl_sem_bpc}} | {{n:incl_pct_sem_bpc}} | {{n:incl_bpc_base}} famílias com a informação |
| Sem informação de BPC | {{n:incl_bpc_sem_info}} | — | — |

</div>

<!-- fonte: Cadastro Único (extração CTPE, {{n:incl_particao}}); tipos não exclusivos (uma criança pode ter mais de um) -->

<!--
Os números do eixo numa só tabela, para consulta. Mesmos valores das tabelas da aba Inclusão do site.
-->

---
<!-- _class: encerramento -->
<!-- _footer: '' -->

<div class="kicker">Instituto Pereira Passos</div>

# Obrigado

## Perguntas e sugestões

**{{contato}}** · {{url_site}}

<img class="logo" src="img/ipp-logo.png" alt="Prefeitura do Rio · Instituto Pereira Passos">
