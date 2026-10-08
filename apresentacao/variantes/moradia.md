---
# Variante breve: eixo Moradia (specs/2026-10-07_deck_familia_moradia), na estrutura das variantes de Inclusão, Alimentação e
# Direito ao Brincar. Mesmo tema, regras de texto e gerador do deck principal (apresentacao.md, que não muda).
# Gere com  python apresentacao/build/gera_apresentacao.py apresentacao/variantes/moradia.md
# Precisa das tabelas de Moradia da silver do CadÚnico (seção "Inclusão e Moradia" do analise.py) em tabelas_finais/.
titulo: "Moradia: as condições dos domicílios das crianças do Cadastro Único"
subtitulo: Eixo Moradia do Diagnóstico da Primeira Infância Carioca
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
Abertura (30 s). Apresentação curta, só do eixo Moradia: inadequação e déficit habitacional (metodologia da Fundação João
Pinheiro) e adensamento, para as crianças do Cadastro Único; espaço para os dados do programa Territórios Sociais.
-->

---
<div class="kicker">Eixo Moradia</div>

# O que o eixo mostra

<div style="font-size:23px">

- **Inadequação habitacional**: domicílios sem infraestrutura (água, esgoto, lixo, energia) ou com problemas na construção (banheiro, piso, cômodos)
- **Déficit habitacional**: domicílios que precisariam ser repostos ou que pesam demais no orçamento (aluguel, coabitação)
- **Adensamento excessivo**: mais de 2 pessoas por dormitório
- Dados do programa **Territórios Sociais** (a incluir)

</div>

<p class="nota forte" style="margin-top:22px"><strong>Atenção:</strong> só as crianças até 72 meses do <strong>Cadastro Único</strong> (julho de 2026), com as condições do domicílio declaradas no cadastro — não todas as crianças da cidade. Inadequação e déficit seguem a metodologia da <strong>Fundação João Pinheiro</strong> (FJP).</p>

<!-- revisar -->

<!--
Mensagem: o eixo deixou de depender do dado pontual de agosto de 2026 -- sai da extração rotineira do cadastro, como Inclusão.
-->

---
<div class="kicker">Eixo Moradia</div>

# Metade das crianças do cadastro vive em domicílio adensado

<div class="stats" style="--n:3; margin-top:26px">
<div class="destaque" style="--c:var(--c2)"><b>{{n:mor_aden_pct}}</b><span>das crianças em domicílio com mais de 2 pessoas por dormitório ({{n:mor_aden_n}} crianças)</span></div>
<div style="--c:var(--c2)"><b>{{n:mor_deficit_pct}}</b><span>em domicílio em déficit habitacional ({{n:mor_deficit_n}} crianças)</span></div>
<div style="--c:var(--c7)"><b>{{n:mor_inad_pct}}</b><span>em domicílio com inadequação habitacional ({{n:mor_inad_n}} crianças)</span></div>
</div>

<p class="nota" style="margin-top:26px">Os três indicadores se sobrepõem: a mesma criança pode estar em mais de uma situação. Cada percentual considera as crianças com a informação no cadastro.</p>

<!-- fonte: Cadastro Único (extração CTPE, julho de 2026); crianças até 72 meses; metodologia da Fundação João Pinheiro -->

<!-- revisar -->

<!--
Os números do resumo da aba Moradia do site. Em famílias: {{n:mor_aden_fam_pct}} adensadas, {{n:mor_deficit_fam_pct}} em
déficit, {{n:mor_inad_fam_pct}} em inadequação.
-->

---
<div class="kicker">Eixo Moradia · Inadequação habitacional</div>

# O que torna o domicílio inadequado

<div class="lado">
<div>

O componente mais frequente é **{{n:mor_inadcomp1_nome}}** ({{n:mor_inadcomp1_pct}} das crianças), seguido de **{{n:mor_inadcomp2_nome}}** ({{n:mor_inadcomp2_pct}}).

Inadequação de infraestrutura: **{{n:mor_infra_pct}}**; edilícia (construção): **{{n:mor_edil_pct}}**.

<p class="nota">Componentes não exclusivos: um domicílio pode ter mais de um, e as barras não somam o total.</p>

</div>

![](fig:cadunico_criancas_inadequacao_componentes)

</div>

<!-- fonte: Cadastro Único (extração CTPE, julho de 2026); metodologia da Fundação João Pinheiro; componentes não exclusivos -->

<!-- revisar -->

<!--
Saneamento em números absolutos: {{n:mor_banheiro_n}} crianças em domicílio sem banheiro e {{n:mor_agua_n}} sem água
canalizada.
-->

---
<div class="kicker">Eixo Moradia · Déficit habitacional</div>

# {{n:mor_deficit_pct}} das crianças vivem em domicílio em déficit habitacional

<div class="lado">
<div>

O principal componente é **{{n:mor_defcomp1_nome}}** ({{n:mor_defcomp1_pct}} das crianças), seguido de **{{n:mor_defcomp2_nome}}** ({{n:mor_defcomp2_pct}}).

<p class="nota">Déficit habitacional (FJP): domicílios improvisados ou rústicos, coabitação e famílias de baixa renda que gastam 30% ou mais da renda com aluguel. Componentes não exclusivos.</p>

</div>

![](fig:cadunico_criancas_deficit_componentes)

</div>

<!-- fonte: Cadastro Único (extração CTPE, julho de 2026); metodologia da Fundação João Pinheiro; coabitação aproximada -->

<!-- revisar -->

<!--
Leitura para a gestão: o déficit das famílias do cadastro é sobretudo de renda (aluguel), não de construção -- política de
aluguel social e de renda, além de obra. Coabitação é aproximação (o cadastro não identifica todas as famílias do domicílio).
-->

---
<div class="kicker">Eixo Moradia · Território · Número</div>

# Onde estão as crianças em inadequação habitacional: número por bairro

<div class="lado">
<div>

**Número de crianças** em domicílio com inadequação habitacional. Os maiores números estão em {{n:mor_inad_top3_bairros_n}}.

<p class="nota">Bairros com menos de 20 casos ficam sem cor: estão somados aos da mesma Região Administrativa ({{n:mor_inad_n_bairros_somados}} bairros).</p>

</div>

![](fig:apres_cadunico_inadequacao_n_bairro)

</div>

<!-- revisar -->

<!--
O número acompanha o tamanho do cadastro em cada bairro. Para comparar bairros, o próximo slide usa o percentual.
-->

---
<div class="kicker">Eixo Moradia · Território · Percentual</div>

# Percentual de crianças em inadequação habitacional por bairro

<div class="lado">
<div>

**% das crianças cadastradas** do bairro em domicílio com inadequação. A mediana dos bairros é **{{n:mor_inad_mediana_bairros}}**.

O maior percentual é o de {{n:mor_inad_bairro_max}}, um valor atípico (cerca do dobro do segundo, {{n:mor_inad_bairro_2o}}): fica com a cor máxima.

<p class="nota">Bairros com menos de 20 casos mostram o percentual do conjunto dos bairros pequenos da sua Região Administrativa.</p>

</div>

![](fig:apres_cadunico_inadequacao_bairro)

</div>

<!-- revisar -->

<!--
Valor atípico: decisão do usuário de 2026-10-06 (o mesmo tratamento do site e do relatório). Percentual = crianças em
inadequação ÷ crianças com a informação no bairro (mesma base).
-->

---
<div class="kicker">Eixo Moradia · Território · Adensamento</div>

# Adensamento excessivo por bairro

<div class="lado">
<div>

**% das crianças cadastradas** do bairro em domicílio com mais de 2 pessoas por dormitório. A mediana dos bairros é **{{n:mor_aden_mediana_bairros}}**: de {{n:mor_aden_bairro_min}} a {{n:mor_aden_bairro_max}}.

<p class="nota">O adensamento é alto em quase toda a cidade: a diferença entre bairros é menor que a da inadequação.</p>

</div>

![](fig:apres_cadunico_adensamento_bairro)

</div>

<!-- revisar -->

<!--
{{n:mor_aden_n_bairros_sozinhos}} bairros publicados sozinhos; os demais, somados por Região Administrativa (regra de
proteção de dados do Cadastro Único).
-->

---
<div class="kicker">Eixo Moradia · Territórios Sociais</div>

# Dados Territórios Sociais

<div class="grupo" style="margin-top:30px; border-style:dashed; min-height:380px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center">
<div class="grupo-titulo">Espaço reservado</div>

<p class="nota" style="font-size:22px; max-width:820px">Dado do programa <strong>Territórios Sociais</strong> (IPP/ONU-Habitat) sobre moradia nos territórios atendidos — a incluir.</p>
</div>

<!-- revisar -->

<!--
Placeholder pedido pelo usuário (2026-10-07). Quando o dado chegar (imagem pronta, como a de insegurança alimentar da
variante Alimentação): guardar em apresentacao/variantes/moradia_adhoc/ e trocar a caixa por ![](fig:<nome do arquivo>),
com kicker "Dado pontual · Territórios Sociais" e o comentário de rodapé "fonte:". Dado pontual: só na apresentação, nunca no
site nem no relatório (constituição §3).
-->

---
<div class="kicker">Eixo Moradia · Territórios Sociais</div>

# Dados Territórios Sociais

<div class="grupo" style="margin-top:30px; border-style:dashed; min-height:380px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center">
<div class="grupo-titulo">Espaço reservado</div>

<p class="nota" style="font-size:22px; max-width:820px">Leitura do dado do programa <strong>Territórios Sociais</strong> (IPP/ONU-Habitat) — a incluir.</p>
</div>

<!-- revisar -->

<!--
Placeholder pedido pelo usuário (2026-10-07): segundo slide do dado dos Territórios Sociais (na variante Alimentação, o
primeiro apresenta o dado e o segundo traz a leitura).
-->

---
<div class="kicker">Eixo Moradia</div>

# Limites e próximos passos

<div class="dois">
<div>

**Limites**

- Só as crianças do Cadastro Único, com as condições declaradas no cadastro
- Coabitação aproximada: o cadastro não identifica todas as famílias do domicílio
- Bairro pelo CEP: crianças com CEP fora da correspondência ficam só no total da cidade

</div>
<div>

**Próximos passos**

- Incluir os dados dos Territórios Sociais
- Cruzar moradia com renda e composição familiar
- Textos de análise na versão de 13 de outubro de 2026

</div>
</div>

<!-- revisar -->

<!--
Os próximos passos são sugestão do IPP, a revisar com a equipe.
-->

---
<div class="kicker">Eixo Moradia · Resumo</div>

# Resumo dos indicadores

<div style="font-size:19px">

| Indicador (crianças até 72 meses no Cadastro Único) | Crianças | % | % das famílias |
| :-- | --: | --: | --: |
| Adensamento excessivo (mais de 2 pessoas por dormitório) | **{{n:mor_aden_n}}** | {{n:mor_aden_pct}} | {{n:mor_aden_fam_pct}} |
| Déficit habitacional (FJP) | **{{n:mor_deficit_n}}** | {{n:mor_deficit_pct}} | {{n:mor_deficit_fam_pct}} |
| Inadequação habitacional (FJP) | **{{n:mor_inad_n}}** | {{n:mor_inad_pct}} | {{n:mor_inad_fam_pct}} |
| Inadequação de infraestrutura | {{n:mor_infra_n}} | {{n:mor_infra_pct}} | {{n:mor_infra_fam_pct}} |
| Inadequação edilícia | {{n:mor_edil_n}} | {{n:mor_edil_pct}} | {{n:mor_edil_fam_pct}} |
| Domicílio sem banheiro | {{n:mor_banheiro_n}} | {{n:mor_banheiro_pct}} | {{n:mor_banheiro_fam_pct}} |
| Domicílio sem água canalizada | {{n:mor_agua_n}} | {{n:mor_agua_pct}} | {{n:mor_agua_fam_pct}} |

</div>

<!-- fonte: Cadastro Único (extração CTPE, julho de 2026); % sobre as crianças (e as famílias) com a informação; metodologia da Fundação João Pinheiro -->

<!--
Os números do eixo numa só tabela, para consulta. Mesmos valores da tabela da aba Moradia do site.
-->

---
<!-- _class: encerramento -->
<!-- _footer: '' -->

<div class="kicker">Instituto Pereira Passos</div>

# Obrigado

## Perguntas e sugestões

**{{contato}}** · {{url_site}}

<img class="logo" src="img/ipp-logo.png" alt="Prefeitura do Rio · Instituto Pereira Passos">
