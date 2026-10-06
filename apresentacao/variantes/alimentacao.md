---
# Variante breve: eixo Alimentação (specs/2026-10-06_deck_alimentacao_brincar), na estrutura da variante Inclusão
# (variantes/inclusao.md). Mesmo tema, regras de texto e gerador do deck principal (apresentacao.md, que não muda).
# Gere com  python apresentacao/build/gera_apresentacao.py apresentacao/variantes/alimentacao.md
titulo: "Alimentação: peso ao nascer e estado nutricional das crianças"
subtitulo: Eixo Alimentação do Diagnóstico da Primeira Infância Carioca
publico: gestores
secretaria: ""
evento: Diagnóstico da Primeira Infância Carioca
data: outubro de 2026
rodape: Diagnóstico da Primeira Infância Carioca · Eixo Alimentação · Instituto Pereira Passos
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
Abertura (30 s). Apresentação curta, só do eixo Alimentação: peso ao nascer, estado nutricional das crianças acompanhadas
pela saúde e um dado pontual sobre insegurança alimentar.
-->

---
<div class="kicker">Eixo Alimentação</div>

# O que o eixo mostra

<div style="font-size:23px">

- **Baixo peso ao nascer**: bebês nascidos com menos de 2,5 kg, na cidade e por bairro (DataSUS, nascidos vivos)
- **Desnutrição, sobrepeso e obesidade** das crianças até 72 meses acompanhadas pela atenção básica (SISVAN)
- Um **dado pontual** sobre famílias em insegurança alimentar nos territórios atendidos

</div>

<p class="nota forte" style="margin-top:26px"><strong>Atenção:</strong> o SISVAN reúne as crianças <strong>pesadas e medidas nos serviços de saúde</strong> — não todas as crianças da cidade. Os percentuais descrevem as crianças acompanhadas.</p>

<p class="nota">Até 72 meses = 0 a 5 anos completos, o recorte de primeira infância do Marco Legal.</p>

<!-- revisar -->

<!--
Mensagem: o eixo combina um indicador de nascimento (todos os nascidos vivos) com o acompanhamento nutricional da atenção
básica. São bases diferentes: não somar nem comparar diretamente.
-->

---
<div class="kicker">Eixo Alimentação · Nascimento</div>

# 1 em cada 10 bebês nasce com baixo peso

<div class="lado">
<div>

**{{n:baixo_peso_pct_2025}}** dos nascidos vivos em {{n:alim_bp_ano}} ({{n:baixo_peso_n_2025}} bebês) tinham menos de 2,5 kg.

O percentual oscila pouco: {{n:alim_bp_pct_ini}} em {{n:alim_bp_ano_ini}}, mínimo de {{n:alim_bp_min}} e pico de {{n:alim_bp_pico}}.

<p class="nota">O eixo do gráfico não começa em zero, para mostrar a variação.</p>

</div>

![](fig:nascidos_abaixo_peso_percentual_por_ano)

</div>

<!-- revisar -->

<!--
Baixo peso ao nascer é indicador de saúde da gestação (pré-natal, nutrição da gestante, prematuridade), por isso entra no
eixo Alimentação. Série estável em torno de 9-10%.
-->

---
<div class="kicker">Eixo Alimentação · Território · Número</div>

# Onde nascem os bebês com baixo peso: número por bairro

<div class="lado">
<div>

**Número de nascidos** com baixo peso em {{n:alim_bp_ano}}. Os maiores números estão em {{n:alim_bp_top3_bairros_n}} — bairros com muitos nascimentos.

<p class="nota">O número acompanha o total de nascimentos do bairro. Para comparar bairros, o próximo slide usa o percentual.</p>

</div>

![](fig:mapa_nascidos_baixo_peso_bairro_2025)

</div>

<!-- revisar -->

<!--
Contagem absoluta -> classes discretas (convenção do projeto).
-->

---
<div class="kicker">Eixo Alimentação · Território · Percentual</div>

# Percentual de nascidos com baixo peso por bairro

<div class="lado">
<div>

**% dos nascidos vivos** do bairro com menos de 2,5 kg — não o número de bebês.

A mediana dos bairros é **{{n:alim_bp_mediana_bairros}}**, perto da média da cidade ({{n:baixo_peso_pct_2025}}).

<p class="nota">Bairros com poucos nascimentos têm percentuais extremos: ficam com a cor máxima e são listados no rodapé.</p>

</div>

![](fig:apres_baixo_peso_bairro_2025)

</div>

<!-- revisar -->

<!--
Percentual = nascidos com baixo peso ÷ nascidos vivos do bairro (mesma base). Em bairro com poucos nascimentos, um ou dois
casos mudam muito o percentual: não ler os extremos como prioridade sem olhar o número.
-->

---
<div class="kicker">Eixo Alimentação · Estado nutricional</div>

# {{n:alim_desnut_pct}} das crianças acompanhadas têm peso baixo para a idade

<div class="lado">
<div>

Em {{n:alim_sisvan_ano}}, **{{n:alim_desnut_n}}** das {{n:alim_sisvan_total}} crianças até 72 meses acompanhadas pelo SISVAN tinham peso baixo ou muito baixo para a idade ({{n:alim_desnut_muito_baixo_pct}} com peso muito baixo).

<p class="nota">O pico de {{n:alim_desnut_pico}} foge do comportamento da série e deve ser lido com cautela.</p>

</div>

![](fig:apres_sisvan_desnutricao_ano)

</div>

<!-- revisar -->

<!--
Indicador peso-para-idade do SISVAN. 2026 é ano parcial: fica fora do gráfico do deck. Percentuais recalculados das
contagens (o site mostra 2023 como 3,7%, erro da coluna de % da origem; pelas contagens, 5,7%). O número de crianças acompanhadas cresceu muito
desde 2008 (cobertura do sistema), o que também mexe nos percentuais.
-->

---
<div class="kicker">Eixo Alimentação · Estado nutricional</div>

# {{n:alim_sobrepeso_pct}} das crianças acompanhadas têm sobrepeso ou obesidade

<div class="lado">
<div>

Em {{n:alim_sisvan_ano}}, **{{n:alim_sobrepeso_n}}** crianças acompanhadas tinham sobrepeso ou obesidade: {{n:alim_sobrepeso_pct}}, mais que o dobro do percentual com peso baixo para a idade ({{n:alim_desnut_pct}}).

Delas, **{{n:alim_obesidade_n}}** com obesidade ({{n:alim_obesidade_pct}}). Outras {{n:alim_risco_sobrepeso_pct}} estão em risco de sobrepeso.

</div>

![](fig:apres_sisvan_sobrepeso_ano)

</div>

<!-- revisar -->

<!--
Leitura para a gestão: entre as crianças acompanhadas, o excesso de peso já pesa mais que o baixo peso para a idade.
Percentuais recalculados das contagens (o site mostra a obesidade de 2009 como 0,07%, erro da coluna de % da origem).
-->

---
<div class="kicker">Eixo Alimentação · Dado pontual · Territórios Sociais</div>

# Famílias em insegurança alimentar nos territórios atendidos — fase de expansão

<div class="lado baixo">
<div>

Dado do programa **Territórios Sociais** (IPP/ONU-Habitat): concentração das famílias em insegurança alimentar **nos territórios atendidos pelo programa**, na fase de expansão.

O mapa mostra os limites das Coordenadorias de Área Programática de Saúde (CAP).

<p class="nota">Dado pontual: mostra só os territórios do programa, não a cidade inteira — áreas sem cor não significam ausência de insegurança alimentar.</p>

</div>

![](fig:inseguranca_alimentar_territorios_expansao)

</div>

<!-- fonte: Territórios Sociais (IPP/ONU-Habitat), fase de expansão; dado pontual; mapa de calor -->

<!-- revisar -->

<!--
Dado ad hoc (apresentacao/variantes/alimentacao_adhoc/). Só nesta apresentação: dado pontual não vai para o relatório nem
para a versão final do site (constitution §3). Fonte: Territórios Sociais (IPP/ONU-Habitat), informada pelo usuário em
2026-10-06. Confirmar com a equipe: data, o que é "fase de expansão" e como foi medida a insegurança alimentar (escala,
ex. EBIA). A leitura do próximo slide é visual (mapa de calor, sem números).
-->

---
<div class="kicker">Eixo Alimentação · Dado pontual · Territórios Sociais</div>

# CAP 5.3: muitos territórios; leste: menos territórios, concentração mais alta

<div class="lado baixo">
<div>

Na **CAP 5.3** há **muitos territórios** com insegurança alimentar.

Na **porção leste** da cidade (CAPs 3.2, 1.0 e 2.2) há **menos territórios** com o problema, mas com **concentração mais alta** de famílias em insegurança alimentar.

<p class="nota">Leitura visual do mapa de calor (sem números), só nos territórios do programa.</p>

</div>

![](fig:inseguranca_alimentar_territorios_expansao)

</div>

<!-- fonte: Territórios Sociais (IPP/ONU-Habitat), fase de expansão; dado pontual; mapa de calor -->

<!-- revisar -->

<!--
Leitura pedida pelo usuário (2026-10-06): espalhamento na CAP 5.3 (muitos focos) × poucos focos, mais intensos, a leste
(o ponto mais alto, em amarelo, fica entre as CAPs 3.2 e 1.0).
-->

---
<div class="kicker">Eixo Alimentação</div>

# Limites e próximos passos

<div class="dois">
<div>

**Limites**

- SISVAN: só as crianças acompanhadas na atenção básica; a cobertura cresceu ao longo da série
- Sem dado de consumo alimentar nem de insegurança alimentar para a cidade toda
- Baixo peso ao nascer por bairro: percentuais instáveis onde há poucos nascimentos

</div>
<div>

**Próximos passos**

- SISVAN por bairro ou por CAP, para ver o estado nutricional no território
- Insegurança alimentar com fonte rotineira (ex. Cadastro Único), no lugar do dado pontual
- Textos de análise na versão de 13 de outubro de 2026

</div>
</div>

<!-- revisar -->

<!--
Achado interno (não falar): duas colunas de % publicadas do SISVAN têm erro na origem (desnutrição 2023, obesidade 2009);
os números deste deck são recalculados de contagem ÷ total. Pendente de correção no analise.py (ROADMAP).
-->

---
<div class="kicker">Eixo Alimentação · Resumo</div>

# Resumo dos indicadores

<div style="font-size:19px">

| Indicador | Número | % | Base do percentual |
| :-- | --: | --: | :-- |
| Nascidos com baixo peso ({{n:alim_bp_ano}}) | **{{n:baixo_peso_n_2025}}** | {{n:baixo_peso_pct_2025}} | nascidos vivos |
| Mediana dos bairros, baixo peso ao nascer | — | {{n:alim_bp_mediana_bairros}} | nascidos vivos do bairro |
| Crianças acompanhadas pelo SISVAN ({{n:alim_sisvan_ano}}) | {{n:alim_sisvan_total}} | — | — |
| Peso baixo ou muito baixo para a idade | **{{n:alim_desnut_n}}** | {{n:alim_desnut_pct}} | crianças acompanhadas |
| Sobrepeso ou obesidade | **{{n:alim_sobrepeso_n}}** | {{n:alim_sobrepeso_pct}} | crianças acompanhadas |
| Delas, obesidade | {{n:alim_obesidade_n}} | {{n:alim_obesidade_pct}} | crianças acompanhadas |
| Risco de sobrepeso | — | {{n:alim_risco_sobrepeso_pct}} | crianças acompanhadas |

</div>

<!-- fonte: DATASUS/Tabnet, nascidos vivos de residentes ({{n:alim_bp_ano}}); SISVAN/DATASUS, crianças até 72 meses acompanhadas ({{n:alim_sisvan_ano}}) -->

<!--
Os números do eixo numa só tabela, para consulta. O dado pontual de insegurança alimentar não entra: não tem números.
-->

---
<!-- _class: encerramento -->
<!-- _footer: '' -->

<div class="kicker">Instituto Pereira Passos</div>

# Obrigado

## Perguntas e sugestões

**{{contato}}** · {{url_site}}

<img class="logo" src="img/ipp-logo.png" alt="Prefeitura do Rio · Instituto Pereira Passos">
