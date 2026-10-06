---
# Variante breve: eixo Direito ao Brincar (specs/2026-10-06_deck_alimentacao_brincar), na estrutura da variante Inclusão
# (variantes/inclusao.md). Mesmo tema, regras de texto e gerador do deck principal (apresentacao.md, que não muda).
# Gere com  python apresentacao/build/gera_apresentacao.py apresentacao/variantes/direito_brincar.md
titulo: "Direito ao Brincar: o território onde a criança vive"
subtitulo: Eixo Direito ao Brincar do Diagnóstico da Primeira Infância Carioca
publico: gestores
secretaria: ""
evento: Diagnóstico da Primeira Infância Carioca
data: outubro de 2026
rodape: Diagnóstico da Primeira Infância Carioca · Eixo Direito ao Brincar · Instituto Pereira Passos
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
Abertura (30 s). Apresentação curta, só do eixo Direito ao Brincar: hoje, o único dado do eixo é a violência no território.
-->

---
<div class="kicker">Eixo Direito ao Brincar</div>

# O que o eixo mostra

<div style="font-size:23px">

- A **violência no território** onde a criança vive e brinca, por Região Administrativa (RA)
- Três taxas de 2024: **homicídios**, **homicídios por ação policial** e **homicídios de jovens negros**
- O que falta para medir o direito ao brincar: espaços, equipamentos e programas

</div>

<p class="nota forte" style="margin-top:26px"><strong>Atenção:</strong> as três taxas são da <strong>população geral, de todas as idades</strong> — não são dados de crianças. Descrevem o ambiente em que as crianças crescem.</p>

<p class="nota">Um único ano (2024), sem série histórica; a RA de Paquetá não tem dado.</p>

<!-- revisar -->

<!--
Mensagem: o eixo é novo (7º eixo, 2026-09-28) e ainda tem um só indicador. A apresentação mostra o que há e pede apoio para o
que falta.
-->

---
<div class="kicker">Eixo Direito ao Brincar · Território</div>

# Homicídios: {{n:brin_homicidios_mun}} por 100 mil habitantes na cidade

<div class="lado">
<div>

Taxa de homicídios por RA em 2024. **{{n:brin_homicidios_acima}} das {{n:brin_n_ras}} RAs** com dado ficam acima da taxa da cidade.

A taxa de {{n:homicidios_max_ra}} é um valor extremo e fica com a cor máxima; entre as demais RAs, lidera {{n:homicidios_2a_ra}}.

<p class="nota">Dado da população geral, de todas as idades — não é específico de crianças.</p>

</div>

![](fig:apres_violencia_territorial_homicidios_ra_2024)

</div>

<!-- revisar -->

<!--
Mesmo mapa do slide "O território onde a criança brinca" do deck principal (teto de Tukey; o Centro fica com a cor máxima).
-->

---
<div class="kicker">Eixo Direito ao Brincar · Território</div>

# Homicídios por ação policial

<div class="lado">
<div>

Taxa da cidade: **{{n:brin_policial_mun}}**. A maior é a de **{{n:brin_policial_max}}**; {{n:brin_policial_acima}} RAs ficam acima da taxa da cidade e {{n:brin_policial_zero}} não registraram nenhum caso em 2024.

<p class="nota">Dado da população geral, de todas as idades — não é específico de crianças.</p>

</div>

![](fig:apres_violencia_territorial_acao_policial_ra_2024)

</div>

<!-- revisar -->

<!--
Taxa publicada pelo Data.Rio (indicador do Índice de Progresso Social, não citado no deck -- slide_revision D12). Unidade
da taxa a confirmar na ficha do indicador antes de dizer "por 100 mil".
-->

---
<div class="kicker">Eixo Direito ao Brincar · Território</div>

# Homicídios de jovens negros

<div class="lado">
<div>

Taxa da cidade: **{{n:brin_jovens_negros_mun}}**. A maior é a de **{{n:brin_jovens_negros_max}}**; {{n:brin_jovens_negros_acima}} RAs ficam acima da taxa da cidade.

<p class="nota">Não é dado de crianças: indica a violência letal no território em que elas crescem.</p>

</div>

![](fig:apres_violencia_territorial_jovens_negros_ra_2024)

</div>

<!-- revisar -->

<!--
Mesma fonte e mesma ressalva de unidade do slide anterior.
-->

---
<div class="kicker">Eixo Direito ao Brincar · O que falta</div>

# Limites e próximos passos

<div class="dois">
<div>

**Limites**

- Um só indicador, de violência, e da população geral
- Só 2024, por Região Administrativa: sem série nem detalhe por bairro
- Nada ainda sobre espaços e oportunidades de brincar

</div>
<div>

**Próximos passos**

- Integrar os registros administrativos georreferenciados que já existem nas secretarias: praças, parques, áreas de lazer, equipamentos culturais e esportivos, programas para a primeira infância
- Violência contra crianças por tipo, sexo e idade (Tabnet municipal)
- Textos de análise na versão de 13 de outubro de 2026

</div>
</div>

<p class="nota forte" style="margin-top:20px">Precisamos do apoio das secretarias para completar o eixo.</p>

<!-- revisar -->

<!--
Mesmo pedido do slide "Eixos incompletos" do deck principal. Os itens de equipamentos são sugestão do IPP, a revisar com a
equipe (o catálogo de indicadores ainda não os lista).
-->

---
<div class="kicker">Eixo Direito ao Brincar · Resumo</div>

# Resumo dos indicadores

<div style="font-size:21px">

| Indicador (2024, população geral) | Taxa da cidade | Maior taxa (RA) | RAs acima da cidade |
| :-- | --: | :-- | --: |
| Homicídios (por 100 mil hab.) | **{{n:brin_homicidios_mun}}** | {{n:brin_homicidios_max}} | {{n:brin_homicidios_acima}} de {{n:brin_n_ras}} |
| Homicídios por ação policial | **{{n:brin_policial_mun}}** | {{n:brin_policial_max}} | {{n:brin_policial_acima}} de {{n:brin_n_ras}} |
| Homicídios de jovens negros | **{{n:brin_jovens_negros_mun}}** | {{n:brin_jovens_negros_max}} | {{n:brin_jovens_negros_acima}} de {{n:brin_n_ras}} |

</div>

<!-- fonte: Data.Rio, 2024, por Região Administrativa (todas as idades); RA de Paquetá sem dado -->

<!--
Os números do eixo numa só tabela, para consulta. Mesmos valores da tabela do site.
-->

---
<!-- _class: encerramento -->
<!-- _footer: '' -->

<div class="kicker">Instituto Pereira Passos</div>

# Obrigado

## Perguntas e sugestões

**{{contato}}** · {{url_site}}

<img class="logo" src="img/ipp-logo.png" alt="Prefeitura do Rio · Instituto Pereira Passos">
