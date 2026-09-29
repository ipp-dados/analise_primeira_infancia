---
# VARIANTE DE EXEMPLO (cópia de apresentacao.md com outro cabeçalho). Fonte única do deck (specs/2026-09-28_apresentacao; estrutura de 33 slides: specs/2026-09-29_slide_revision). Para uma variante: copie este arquivo para variantes/<nome>.md,
# mude este cabeçalho e ligue/desligue blocos; gere com  python apresentacao/build/gera_apresentacao.py variantes/<nome>.md
titulo: Diagnóstico da Primeira Infância Carioca
subtitulo: Um hub de dados para a Política Municipal Integrada da Primeira Infância do Rio de Janeiro
publico: gestores            # gestores | tecnico
secretaria: "Secretaria Municipal de Saúde"   # variante de exemplo: aparece na capa
evento: Apresentação às secretarias municipais
data: outubro de 2026
rodape: Diagnóstico da Primeira Infância Carioca · Instituto Pereira Passos
url_site: https://ipp-dados.github.io/analise_primeira_infancia/
contato: pesquisaeavaliacao.ipp@prefeitura.rio
blocos: [cooperacao, governanca]   # sem o roteiro de demonstração ao vivo
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
Abertura (1 min). Apresentar o IPP e o objetivo da conversa: mostrar o que já temos e pedir ajuda para completar o retrato.
-->

---

<div class="kicker">Parte I · Contexto</div>

# Por que um diagnóstico da primeira infância

<div style="font-size:23px">

- Os primeiros seis anos concentram as maiores oportunidades — e os maiores riscos — do desenvolvimento
- A **Política Municipal Integrada da Primeira Infância Carioca** precisa de um retrato comum da cidade
- Precisamos de um retrato das **especificidades das diferentes partes da cidade**
- Este diagnóstico organiza esse retrato **por eixo da política** e **por território**, do município ao bairro

</div>

<!-- revisar -->

<!--
Mensagem: não é mais um relatório; é uma base comum para planejar e acompanhar a política -- e que mostra a cidade por partes, não só a média.
-->

---

<div class="kicker">Parte I · Contexto</div>

# Um produto vivo, construído com as secretarias

<div class="stats">
<div style="--c:var(--c3)"><b>Vivo</b><span>atualizado a cada nova base de dados e a cada nova necessidade da gestão</span></div>
<div style="--c:var(--c1)"><b>Com vocês</b><span>quem conhece a política na ponta sabe o que medir e como ler cada número</span></div>
<div style="--c:var(--c2)"><b>Aberto</b><span>sugestões de indicadores, bases para compartilhar e correções são bem-vindas</span></div>
</div>

<p class="legenda-grande" style="margin-top:34px; font-size:27px">Este diagnóstico não é um relatório fechado: é um ponto de partida para construirmos juntos.</p>

<!-- revisar -->

<!--
Mensagem central: o projeto é COM as secretarias, não SOBRE elas. Convidar desde já a sugerir indicadores e dados.
-->

---

<div class="kicker">Parte I · Contexto</div>

# O que os registros administrativos não contam sozinhos

- **Foram feitos para outra finalidade**: atender, pagar, notificar — não medir
- **Mudam com o tempo**: nova ficha, novo sistema, nova regra de registro podem parecer mudança real
- **Mostram associação, não causa**: Zika de 2015-2016, recessão (2015-2016) e Covid-19 (2020-2021) atravessam as séries

<!-- revisar -->

---

<div class="kicker">Parte I · Contexto</div>

# Um centro para os dados da primeira infância

<div class="hub">
<div class="col">
<div class="caixa" style="--c:var(--c1)">Censo e estimativas (IBGE, Ripsa/MS)</div>
<div class="caixa" style="--c:var(--c2)">Cadastro Único</div>
<div class="caixa" style="--c:var(--c3)">Saúde: nascimentos, óbitos, violência, nutrição, vacinação</div>
<div class="caixa" style="--c:var(--c4)">Educação: Censo Escolar, PNAD</div>
<div class="caixa" style="--c:var(--c7)">Território: IPS, limites de bairro, AP, RA, CAP</div>
</div>
<div class="seta">→</div>
<div class="centro"><b>Um processamento único</b>aberto, com as mesmas regras para todas as fontes</div>
<div class="seta">→</div>
<div class="col">
<div class="caixa" style="--c:var(--c3)"><b>Site interativo</b> — {{n:n_graficos}} gráficos e {{n:n_mapas}} mapas</div>
<div class="caixa" style="--c:var(--c1)"><b>Relatório em PDF</b> — com todas as tabelas</div>
<div class="caixa" style="--c:var(--c5)"><b>Tabelas e código</b> — abertos no GitHub</div>
</div>
</div>

<!--
Os números de gráficos e mapas saem da estrutura do relatório (estrutura_eixos.md).
-->

---

<!-- se: cooperacao -->
<div class="kicker">Parte I · Chamada</div>

# Para integrar, três acordos simples

<div class="grupo">
<div class="grupo-titulo">Governança de Dados</div>
<div class="stats">
<div style="--c:var(--c1)"><b>Consistência</b><span>o mesmo código de bairro (ou endereço geocodificável) em toda base</span></div>
<div style="--c:var(--c3)"><b>Periodicidade</b><span>uma extração periódica combinada, sempre com o mesmo formato</span></div>
<div style="--c:var(--c2)"><b>Privacidade</b><span>só números agregados; bairros com menos de 20 famílias são somados aos vizinhos da mesma região</span></div>
</div>
</div>

<!-- revisar -->
<!-- /se -->

---

<!-- _class: secao -->
<!-- _footer: '' -->

<div class="kicker">Parte II</div>

# Panorama e método

## Quantas crianças são, onde estão e como medimos

---

<!-- _class: numero -->

<div class="kicker">Parte II · Quantas crianças</div>

<div class="grande">{{n:pop_0_5_ripsa_mil}}</div>

<div class="legenda-grande">crianças de até 72 meses vivem no Rio — <strong>{{n:pct_0_5_ripsa_2025}}</strong> da população em {{n:ano_ripsa}}. E são cada vez menos: eram {{n:pop_0_5_ripsa_2000_mil}} em 2000 ({{n:pct_0_5_ripsa_2000}} da população), <strong>{{n:queda_0_5_ripsa_2000}} a menos</strong>.</div>

<p class="nota">Até 72 meses = 0 a 5 anos completos. É a faixa de todo o painel.</p>

<!-- fonte: Ripsa/Ministério da Saúde, estimativas populacionais 2000-2025 -->

---

<div class="kicker">Parte II · Quantas crianças</div>

# {{n:pop_0_5_ripsa_mil}} na cidade; outra régua no bairro

<div class="stats" style="margin-top:22px">
<div style="--c:var(--c1)"><b>{{n:censo_0_4_2022_mil}}</b><span>0 a 4 anos, <strong>Censo 2022</strong> — a única contagem por bairro, usada nos mapas</span></div>
<div class="destaque" style="--c:var(--c2)"><b>{{n:pop_0_5_ripsa_mil}}</b><span>até 72 meses, <strong>estimativa Ripsa/Ministério da Saúde</strong> ({{n:ano_ripsa}}) — a referência da cidade</span></div>
<div style="--c:var(--c7)"><b>{{n:pop_0_6_ripsa_mil}}</b><span>0 a 6 anos, <strong>estimativa Ripsa</strong> ({{n:ano_ripsa}}) — a faixa da política municipal ("até 6 anos"), com as crianças de 6 anos</span></div>
</div>

<p class="nota" style="font-size:18px; margin-top:26px">O Censo conta menos crianças pequenas do que existem; a estimativa corrige isso, mas só para a cidade inteira. Por isso: taxas <strong>do município</strong> usam a estimativa do mesmo ano; taxas <strong>por bairro ou região</strong> usam o Censo 2022 e servem para comparar territórios entre si. Até 72 meses = 0 a 5 anos completos.</p>

<!-- fonte: Ripsa/Ministério da Saúde, estimativas populacionais; IBGE, Censo Demográfico 2022 -->

---

<div class="kicker">Parte II · Território</div>

# O bairro é a unidade de análise principal

<div class="lado">
<div>

**{{n:n_bairros}} bairros**, agregados quando o dado pede: 5 Áreas de Planejamento, 16 Regiões de Planejamento, 33 Regiões Administrativas.

É no bairro que as diferenças aparecem — e onde a política chega.

</div>

![](fig:apres_censo_0_4_absoluto)

</div>

---

<div class="kicker">Parte II · Território</div>

# Cada fonte tem o seu recorte de território

<div class="dois">
<div>

![](fig:mapa_obitos_evitaveis_menores_5_anos_cap_2025)

<div class="rotulo">Saúde: 10 Áreas Programáticas (CAP) — não são as 5 Áreas de Planejamento</div>
</div>
<div>

![](fig:mapa_violencia_familiar_mae_taxa_ra_2025)

<div class="rotulo">Violência familiar e IPS: 33 Regiões Administrativas</div>
</div>
</div>

---

<!-- _class: numero -->

<div class="kicker">Parte II · Cadastro Único</div>

<div class="grande">{{n:razao_cadunico}}</div>

<div class="legenda-grande">das crianças de até 72 meses da cidade estão no Cadastro Único — <strong>{{n:cadunico_criancas_0_5}}</strong> crianças em <strong>{{n:cadunico_familias}}</strong> famílias. É muito, mas <strong>não é a cidade toda</strong>.</div>

<p class="nota">Até 72 meses = 0 a 5 anos completos.</p>

<!-- fonte: Cadastro Único (extração CTPE, jun/2026); Ripsa/Ministério da Saúde (2025) -->

---

<div class="kicker">Parte II · Onde estão</div>

# As crianças estão na Zona Oeste — e pesam mais nas periferias

<div class="dois">
<div>

![](fig:apres_censo_0_4_absoluto)

<div class="rotulo"><strong>{{n:top3_bairros_0_4}}</strong> lideram em número</div>
</div>
<div>

![](fig:apres_censo_0_4_percentual)

<div class="rotulo">Em proporção da população, favelas e periferias passam à frente da Zona Sul</div>
</div>
</div>

<!-- revisar -->

---

<div class="kicker">Parte II · Quem são</div>

# {{n:pct_negras_0_5_censo}} das crianças de até 72 meses são negras

<div class="fig">

![](fig:censo_sidra_populacao_0_6_raca_2022)

</div>

<!-- fonte: IBGE, Censo Demográfico 2022 (SIDRA 9606), 0 a 5 anos completos (até 72 meses); negras = pretas + pardas -->

---

<div class="kicker">Parte II · Nascimentos</div>

# {{n:nascidos_2025}} crianças nasceram no Rio em 2025

<div class="lado">
<div>

Eram **{{n:nascidos_pico}}** em {{n:nascidos_pico_ano}}. Os nascimentos se concentram na Zona Oeste.

<p class="nota">{{n:nascidos_sem_bairro_2025}} nascidos em 2025 não têm bairro informado e não aparecem no mapa.</p>

</div>

![](fig:mapa_nascidos_vivos_bairro_2025)

</div>

---

<div class="kicker">Parte II · Desigualdade</div>

# Mortalidade infantil: {{n:tmi_2025}} por mil, desigual entre bairros

<div class="lado">
<div>

Óbitos de menores de 1 ano por mil nascidos vivos, 2025.

<p class="nota">Taxa calculada com os nascidos que têm bairro de residência informado. Bairros com poucos nascimentos têm taxas extremas: ficam com a cor máxima e são listados no rodapé, para não apagar as diferenças entre os demais.</p>

</div>

![](fig:apres_taxa_mortalidade_infantil_bairro_2025)

</div>

<!--
Valores extremos: cerca de Tukey (1,5 x intervalo interquartil), a mesma regra do site. Os bairros acima da cerca estão nomeados na nota do rodapé.
-->

---

<div class="kicker">Parte II · Desigualdade</div>

# Onde está a primeira infância do Cadastro Único

<div class="lado">
<div>

Crianças de até 72 meses cadastradas, por bairro.

<p class="nota">Bairro atribuído pelo CEP; bairros com menos de 20 famílias são somados aos vizinhos da mesma região ("Demais bairros da RA").</p>

</div>

![](fig:mapa_cadunico_criancas_bairro_2026)

</div>

---

<!-- _class: secao -->
<!-- _footer: '' -->

<div class="kicker">Parte III</div>

# Os eixos da política

## Destaques por eixo — o resto está no site e no relatório

---

<div class="kicker">Eixo Prioridade</div>

# O cadastro mostra, sobretudo, a primeira infância mais pobre

<div class="lado">
<div>

**{{n:pct_cadunico_pobreza}}** das crianças cadastradas vivem em famílias em pobreza (renda por pessoa de até R$ 218).

Ótimo para planejar a proteção social; enviesado para descrever todas as crianças.

</div>

![](fig:cadunico_familias_por_faixa_renda)

</div>

<!--
R$ 218 por pessoa é a linha de pobreza do Bolsa Família (desde 2023); de R$ 218 a meio salário mínimo é baixa renda.
-->

---

<div class="kicker">Eixo Prioridade</div>

# Óbitos evitáveis de bebês caíram de {{n:evitaveis_0_364_primeiro}} para {{n:evitaveis_0_364_2025}}

<div class="lado largo">
<div>

Menores de 1 ano, {{n:evitaveis_0_364_primeiro_ano}} a 2025.

Ainda assim, **{{n:pct_evitaveis_menores5_2025}}** dos óbitos de menores de 5 anos em 2025 ({{n:evitaveis_menores5_2025}}) eram evitáveis.

</div>

![](fig:obitos_causas_evitaveis_grupo_ano)

</div>

---

<div class="kicker">Eixo Prioridade</div>

# Causas evitáveis por faixa etária

<div class="lado largo baixo">
<div>

Óbitos evitáveis em 2025, por subgrupo de causa, em três idades: **0 a 6 dias**, **7 a 27 dias** e **28 a 364 dias**.

Cada idade pede uma resposta diferente — do pré-natal e do parto ao cuidado do bebê em casa.

</div>

![](fig:obitos_causas_evitaveis_subgrupo_faixa_2025)

</div>

<!-- revisar -->

<!--
Slide novo (slide_revision). As três faixas são as mesmas da mortalidade neonatal precoce, tardia e pós-neonatal.
-->

---

<div class="kicker">Eixo Família e Cuidados</div>

# {{n:atend_0_5}} das crianças de até 72 meses estão matriculadas

<div class="lado">
<div class="stats" style="--n:1; gap:14px; margin:0">
<div style="--c:var(--c1)"><b>{{n:atend_creche}}</b><span>creche (0 a 3 anos) — meta do PNE: 50%</span></div>
<div style="--c:var(--c2)"><b>{{n:atend_pre}}</b><span>pré-escola (4 e 5 anos) — meta do PNE: 100%</span></div>
</div>

![](fig:taxa_atendimento_0_a_5_por_ano)

</div>

<p class="nota">Taxa bruta: {{n:matriculas_0_5}} matrículas em escolas do Rio em 2025 sobre a população estimada da mesma idade.</p>

---

<div class="kicker">Eixo Família e Cuidados</div>

# A rede pública perdeu {{n:queda_publica_desde_pico}} das matrículas de até 72 meses desde {{n:mat_publica_pico_ano}}

<div class="lado largo">
<div>

Rede pública: de **{{n:mat_publica_pico}}** ({{n:mat_publica_pico_ano}}) para **{{n:mat_publica_2025}}** (2025).

Rede privada: caiu para {{n:mat_privada_2021}} na pandemia (2021) e voltou a **{{n:mat_privada_2025}}**.

A pública ainda responde por **{{n:pct_publica_2025}}** das matrículas.

</div>

![](fig:matriculas_0_a_5_rede_por_ano)

</div>

---

<div class="kicker">Eixo Família e Cuidados</div>

# {{n:pct_familias_uma_adulta}} das famílias com crianças no CadÚnico têm uma só adulta

<p class="nota forte" style="margin:0 0 6px"><strong>Atenção:</strong> "uma só adulta" é aproximado pelos adultos (18 anos ou mais) no cadastro — <strong>não é o conceito oficial de família monoparental</strong>.</p>

<div class="dois baixo">
<div>

![](fig:cadunico_familias_por_arranjo)

<div class="rotulo"><strong>{{n:familias_uma_adulta}}</strong> famílias com uma mulher como única adulta; {{n:pct_familias_dois_adultos}} têm um homem e uma mulher</div>
</div>
<div>

![](fig:mapa_percentual_cadunico_familias_uma_adulta_bairro_2026)

<div class="rotulo">{{n:pct_uma_adulta_pobreza}} delas vivem em pobreza</div>
</div>
</div>

---

<div class="kicker">Eixo Proteção</div>

# Violência familiar contra a primeira infância, por vínculo do provável autor

<div class="lado largo">
<div>

Em {{n:vf_ano}}, por mil crianças de até 72 meses: **{{n:vf_taxa_mae_2025}}** com a mãe ({{n:vf_notif_mae_2025}} notificações), **{{n:vf_taxa_pai_2025}}** com o pai ({{n:vf_notif_pai_2025}}) e **{{n:vf_taxa_outros_2025}}** com outros vínculos ({{n:vf_notif_outros_2025}}).

<p class="nota">Os vínculos não se somam: a mesma notificação pode citar mais de um provável autor. Notificação não é caso confirmado; a série muda de patamar em 2017, possivelmente por mudança na ficha.</p>

</div>

![](fig:violencia_familiar_taxa_municipio_ano)

</div>

<!-- revisar -->

---

<div class="kicker">Eixo Proteção</div>

# Notificações por bairro em {{n:vf_ano}}, por vínculo

<div class="dois">
<div>

![](fig:mapa_violencia_familiar_mae_bairro_2025)

<div class="rotulo">Mãe como provável autora</div>
</div>
<div>

![](fig:mapa_violencia_familiar_pai_bairro_2025)

<div class="rotulo">Pai como provável autor</div>
</div>
</div>

<p class="nota">Contagem absoluta: bairros com mais crianças tendem a ter mais notificações. Os mapas não se somam (uma notificação pode citar os dois). Notificação não é caso confirmado.</p>

<!-- revisar -->

<!--
Slide novo (slide_revision D7, revista em 2026-09-29: sem soma de vínculos, que contaria notificações em dobro).
Contagem absoluta -> classes discretas (convenção do projeto). "Outros vínculos" por bairro só existe acumulado em
2021-2025 (poucos casos por ano); a taxa por bairro e por RA está no site.
-->

---

<div class="kicker">Eixo Direito ao Brincar</div>

# O território onde a criança brinca

<div class="lado">
<div>

Homicídios por 100 mil habitantes, por Região Administrativa. A taxa de {{n:ips_homicidios_max_ra}} é um valor extremo e fica com a cor máxima; entre as demais RAs, lidera {{n:ips_homicidios_2a_ra}}.

<p class="nota">Dado da população geral, de todas as idades (IPS 2024) — não é específico de crianças.</p>

</div>

![](fig:apres_violencia_territorial_homicidios_ra_2024)

</div>

---

<div class="kicker">Eixo Alimentação</div>

# 1 em cada 10 bebês nasce com baixo peso

<div class="lado">
<div>

**{{n:baixo_peso_pct_2025}}** dos nascidos vivos em 2025 ({{n:baixo_peso_n_2025}}) tinham menos de 2,5 kg.

<p class="nota">Bairros com poucos nascimentos têm percentuais extremos: ficam com a cor máxima e são listados no rodapé.</p>

</div>

![](fig:apres_baixo_peso_bairro_2025)

</div>

---

<div class="kicker">Parte III · O que falta</div>

# Eixos incompletos

<div class="stats" style="--n:2; margin-top:26px">
<div style="--c:var(--c2)"><b>Inclusão e Moradia</b><span>os dados do Cadastro Único já estão mapeados e em importação</span></div>
<div style="--c:var(--c3)"><b>Direito ao Brincar</b><span>dado incompleto: precisamos do apoio das secretarias para integrar os registros administrativos georreferenciados que já existem</span></div>
</div>

<!-- revisar -->

<!--
Slide novo (slide_revision). Retoma o antigo slide de indicadores pendentes: o que falta e o que as secretarias podem trazer.
-->

---

<div class="kicker">Parte III · O que falta</div>

# Eixos ausentes

<div class="stats" style="--n:2; margin-top:18px">
<div style="--c:var(--c7)"><b>Direito à Cidade</b><span>eixo sem dado público</span></div>
<div style="--c:var(--c5)"><b>Participação</b><span>eixo sem dado público</span></div>
</div>

<div class="conecta"></div>

<div class="solucao"><b>Pesquisa primária</b><span>a solução para os dois eixos: construída em colaboração com as secretarias, cobre o que o registro administrativo não alcança</span></div>

<!-- revisar -->

<!--
Slide novo (slide_revision). Dois eixos distintos, uma mesma solução: pesquisa primária. Convite: quem já coleta algo sobre esses temas? Que pesquisa faria sentido?
-->

---

<div class="kicker">Parte III · Produtos</div>

# Dois produtos, os mesmos dados

<div class="dois">
<div>

![](captura:site_desktop)

<div class="rotulo">Site interativo: abas por eixo, mapas por bairro, tabelas para baixar</div>
</div>
<div style="display:flex; gap:18px; justify-content:center">

![](captura:pdf_capa)

![](captura:pdf_pagina)

</div>
</div>

---

<!-- _class: qr -->

<div class="kicker">Parte III · Acesse agora</div>

# Abra no celular

<div class="lado">
<div>

{{qr:url_site}}

<div class="url">{{url_site}}</div>

</div>
<div>

Funciona no celular e no computador, sem instalar nada.

Cada gráfico tem **tabela** e **CSV** para baixar.

</div>
<div>

![](captura:site_celular)

</div>
</div>

<!-- se: demo -->
<!--
DEMONSTRAÇÃO AO VIVO (3-4 min; se a rede falhar, seguir com este slide):
1. Visão geral: Introdução e panorama (mapa de crianças por bairro; alternar Bairro / AP / RP).
2. Aba Prioridade: mortalidade infantil por bairro -- passar o mouse num bairro (tooltip), alternar Taxa / Óbitos.
3. Um gráfico: "Ver dados em tabela" e baixar o CSV.
4. Aba Inclusão: indicadores "em desenvolvimento" -- gancho para a chamada.
5. Celular: abrir pelo QR code.
-->
<!-- /se -->

---

<!-- _class: encerramento -->
<!-- _footer: '' -->

<div class="kicker">Instituto Pereira Passos</div>

# Obrigado

## Perguntas e sugestões

**{{contato}}** · {{url_site}}

<img class="logo" src="img/ipp-logo.png" alt="Prefeitura do Rio · Instituto Pereira Passos">
