---
# Fonte única do deck (specs/2026-09-28_apresentacao). Para uma variante: copie este arquivo para variantes/<nome>.md,
# mude este cabeçalho e ligue/desligue blocos; gere com  python apresentacao/build/gera_apresentacao.py variantes/<nome>.md
titulo: Diagnóstico da Primeira Infância Carioca
subtitulo: Um hub de dados para a Política Integrada da Primeira Infância
publico: gestores            # gestores | tecnico
secretaria: ""               # ex. "Secretaria Municipal de Saúde" -- aparece na capa e na chamada
evento: Apresentação às secretarias municipais
data: outubro de 2026
rodape: Diagnóstico da Primeira Infância Carioca · Instituto Pereira Passos
url_site: https://ipp-dados.github.io/analise_primeira_infancia/
contato: ascom.ipp@prefeitura.rio
blocos: [cooperacao, governanca, demo]
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

- Os primeiros seis anos concentram as maiores oportunidades — e os maiores riscos — do desenvolvimento
- A **Política Integrada da Primeira Infância** precisa de um retrato comum da cidade, que todas as secretarias leiam do mesmo jeito
- Este diagnóstico organiza esse retrato **por eixo da política** e **por território**, do município ao bairro

<!-- revisar -->

<!--
Mensagem: não é mais um relatório; é uma base comum para planejar e acompanhar a política.
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

# Um só lugar para os dados da primeira infância

<div class="hub">
<div class="col">
<div class="caixa" style="--c:var(--c1)">Censo e estimativas (IBGE, Ripsa/MS)</div>
<div class="caixa" style="--c:var(--c2)">Cadastro Único</div>
<div class="caixa" style="--c:var(--c3)">Saúde: nascimentos, óbitos, violência, nutrição, vacinação</div>
<div class="caixa" style="--c:var(--c4)">Educação: Censo Escolar, PNAD</div>
<div class="caixa" style="--c:var(--c7)">Território: IPS, limites de bairro, AP, RA, CAP</div>
</div>
<div class="seta">→</div>
<div class="centro"><b>{{n:n_indicadores}} indicadores</b>um processamento único e aberto, com as mesmas regras para todas as fontes</div>
<div class="seta">→</div>
<div class="col">
<div class="caixa" style="--c:var(--c3)"><b>Site interativo</b> — {{n:n_graficos}} gráficos e {{n:n_mapas}} mapas</div>
<div class="caixa" style="--c:var(--c1)"><b>Relatório em PDF</b> — com todas as tabelas</div>
<div class="caixa" style="--c:var(--c5)"><b>Tabelas e código</b> — abertos no GitHub</div>
</div>
</div>

<!--
Os números saem da estrutura do relatório (estrutura_eixos.md): indicadores, gráficos e mapas publicados.
-->

---

<div class="kicker">Parte I · Contexto</div>

# O que os registros administrativos não contam sozinhos

- **Foram feitos para outra finalidade**: atender, pagar, notificar — não medir
- **Mudam com o tempo**: nova ficha, novo sistema, nova regra de registro podem parecer mudança real
- **Nem sempre chegam ao bairro**: a maior parte da estatística oficial para no município
- **Mostram associação, não causa**: Zika (2016), recessão (2015-2016) e Covid-19 (2020-2021) atravessam as séries

<!-- revisar -->

---

<!-- se: cooperacao -->
<div class="kicker">Parte I · Chamada</div>

# {{n:n_pendentes}} dos {{n:n_indicadores}} indicadores da política ainda não têm dado

<div class="lado" style="grid-template-columns: 1fr 1.5fr">
<div>

Os dados que faltam **existem** — estão nos sistemas das secretarias.

Com eles, Inclusão e Moradia saem do zero e Proteção fica completa.

</div>
<div>

{{tabela:pendentes}}

</div>
</div>

<!-- revisar -->

---

<div class="kicker">Parte I · Chamada</div>

# Para integrar, quatro acordos simples

<div class="stats" style="--n:4">
<div style="--c:var(--c1)"><b>Chave</b><span>o mesmo código de bairro (ou endereço geocodificável) em toda base</span></div>
<div style="--c:var(--c3)"><b>Ritmo</b><span>uma extração periódica combinada, sempre com o mesmo formato</span></div>
<div style="--c:var(--c2)"><b>Sigilo</b><span>só números agregados; células com menos de 20 famílias ficam em branco</span></div>
<div style="--c:var(--c7)"><b>Qualidade</b><span>um ponto focal que explique mudanças de ficha, sistema ou regra</span></div>
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

<div class="kicker">Parte II · Território</div>

# O bairro é a unidade de análise

<div class="lado">
<div>

**{{n:n_bairros}} bairros**, agregados quando o dado pede: 5 Áreas de Planejamento, 16 Regiões de Planejamento, 33 Regiões Administrativas.

É no bairro que as diferenças aparecem — e onde a política chega.

</div>

![](fig:mapa_censo_0_4_absoluto)

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

<div class="kicker">Parte II · Quantas crianças</div>

<div class="grande">{{n:pop_0_6_ripsa_mil}}</div>

<div class="legenda-grande">crianças de 0 a 6 anos vivem no Rio — <strong>{{n:pct_0_6_ripsa_2025}}</strong> da população em {{n:ano_ripsa}}. E são cada vez menos: eram {{n:pop_0_6_ripsa_2000_mil}} em 2000 ({{n:pct_0_6_ripsa_2000}} da população), <strong>{{n:queda_0_6_ripsa_2000}} a menos</strong>.</div>

<!-- fonte: Ripsa/Ministério da Saúde, estimativas populacionais 2000-2025 -->

---

<div class="kicker">Parte II · Quantas crianças</div>

# {{n:pop_0_6_ripsa_mil}} na cidade; outras réguas no bairro e no cadastro

<div class="stats">
<div style="--c:var(--c2)"><b>{{n:pop_0_6_ripsa_mil}}</b><span>0 a 6 anos, <strong>estimativa Ripsa/Ministério da Saúde</strong> ({{n:ano_ripsa}}) — a faixa da política, só para a cidade inteira</span></div>
<div style="--c:var(--c3)"><b>{{n:pop_0_5_ripsa_mil}}</b><span>0 a 5 anos, mesma estimativa — a base de comparação do Cadastro Único, que vai até 5 anos</span></div>
<div style="--c:var(--c1)"><b>{{n:censo_0_4_2022_mil}}</b><span>0 a 4 anos, <strong>Censo 2022</strong> — a única contagem por bairro, usada nos mapas</span></div>
</div>

<p class="nota" style="font-size:20px; margin-top:22px">O Censo conta menos crianças pequenas do que existem; a estimativa corrige isso, mas só para a cidade inteira. Por isso: taxas <strong>do município</strong> usam a estimativa do mesmo ano; taxas <strong>por bairro ou região</strong> usam o Censo 2022 e servem para comparar territórios entre si.</p>

<!-- fonte: Ripsa/Ministério da Saúde, estimativas populacionais; IBGE, Censo Demográfico 2022 -->

---


<!-- _class: numero -->

<div class="kicker">Parte II · Cadastro Único</div>

<div class="grande">{{n:razao_cadunico}}</div>

<div class="legenda-grande">das crianças de 0 a 5 anos da cidade estão no Cadastro Único — <strong>{{n:cadunico_criancas_0_5}}</strong> crianças em <strong>{{n:cadunico_familias}}</strong> famílias. É muito, mas <strong>não é a cidade toda</strong>.</div>

<!-- fonte: Cadastro Único (extração CTPE, jun/2026); Ripsa/Ministério da Saúde (2025) -->

---

<div class="kicker">Parte II · Cadastro Único</div>

# O cadastro mostra, sobretudo, a infância mais pobre

<div class="lado">
<div>

**{{n:pct_cadunico_extrema_pobreza}}** das crianças cadastradas vivem em famílias em extrema pobreza.

Ótimo para planejar a proteção social; enviesado para descrever todas as crianças.

</div>

![](fig:cadunico_familias_por_faixa_renda)

</div>

---


<div class="kicker">Parte II · Onde estão</div>

# As crianças estão na Zona Oeste — e pesam mais nas periferias

<div class="dois">
<div>

![](fig:mapa_censo_0_4_absoluto)

<div class="rotulo"><strong>{{n:top3_bairros_0_4}}</strong> lideram em número</div>
</div>
<div>

![](fig:mapa_censo_0_4_percentual)

<div class="rotulo">Em proporção da população, favelas e periferias passam à frente da Zona Sul</div>
</div>
</div>

<!-- revisar -->

---

<div class="kicker">Parte II · Quem são</div>

# {{n:pct_negras_0_6_censo}} das crianças de 0 a 6 anos são negras

<div class="fig">

![](fig:censo_sidra_populacao_0_6_raca_2022)

</div>

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

<p class="nota">Taxa calculada com os nascidos que têm bairro de residência informado. Bairros com poucos nascimentos oscilam muito de um ano para outro.</p>

</div>

![](fig:mapa_taxa_mortalidade_infantil_bairro_2025)

</div>

---

<div class="kicker">Parte II · Desigualdade</div>

# Onde está a infância do Cadastro Único

<div class="lado">
<div>

Crianças de 0 a 5 anos cadastradas, por bairro.

<p class="nota">Bairro atribuído pelo CEP; bairros com menos de 20 famílias ficam em branco.</p>

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

# Óbitos evitáveis de bebês caíram de {{n:evitaveis_0_364_primeiro}} para {{n:evitaveis_0_364_2025}}

<div class="lado largo">
<div>

Menores de 1 ano, {{n:evitaveis_0_364_primeiro_ano}} a 2025.

Ainda assim, **{{n:pct_evitaveis_menores5_2025}}** dos óbitos de menores de 5 anos em 2025 ({{n:evitaveis_menores5_2025}}) eram evitáveis.

</div>

![](fig:obitos_causas_evitaveis_grupo_ano)

</div>

---

<div class="kicker">Eixo Família e Cuidados</div>

# {{n:atend_0_5}} das crianças de 0 a 5 anos estão matriculadas

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

# A rede pública perdeu {{n:queda_publica_desde_pico}} das matrículas de 0 a 5 anos desde {{n:mat_publica_pico_ano}}

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

<div class="dois">
<div>

![](fig:cadunico_familias_por_arranjo)

<div class="rotulo"><strong>{{n:familias_uma_adulta}}</strong> famílias com uma mulher como única adulta; {{n:pct_familias_dois_adultos}} têm um homem e uma mulher</div>
</div>
<div>

![](fig:mapa_percentual_cadunico_familias_uma_adulta_bairro_2026)

<div class="rotulo">{{n:pct_uma_adulta_extrema_pobreza}} delas vivem em extrema pobreza</div>
</div>
</div>

<p class="nota">Arranjo aproximado pelos adultos (18 anos ou mais) no cadastro; não é o conceito oficial de família monoparental.</p>

---

<div class="kicker">Eixo Proteção</div>

# Violência familiar: {{n:vf_notif_mae_2025}} notificações com a mãe como provável autora

<div class="lado largo">
<div>

{{n:vf_taxa_mae_2025}} por mil crianças de 0 a 5 anos em 2025.

<p class="nota">Notificação não é caso confirmado; a série muda de patamar em 2017, possivelmente por mudança na ficha.</p>

</div>

![](fig:violencia_familiar_taxa_municipio_ano)

</div>

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

<div class="kicker">Eixo Alimentação · e o que falta</div>

# 1 em cada 10 bebês nasce com baixo peso

<div class="lado">
<div>

**{{n:baixo_peso_pct_2025}}** dos nascidos vivos em 2025 ({{n:baixo_peso_n_2025}}) tinham menos de 2,5 kg.

**Inclusão** e **Moradia** ainda não têm dado: são os eixos que mais dependem das secretarias.

</div>

![](fig:mapa_percentual_baixo_peso_bairro_2025)

</div>

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
