# Especificação — Novos recortes do CadÚnico (`specs/recortes_cadunico`)

Branch: `spec/recortes_cadunico` (a partir de `planning`)
Status: **implementado** (2026-09-23, Blocos 1-12; ver `tasks.md`/`validation.md`). D1-D6 e D8 aprovadas
pelo usuário; D7 adiada para a auditoria de faixas etárias do roadmap item 6 (§8). Abertos: revisão visual
com o usuário (T12.3), limiar na constitution (T11.4, só com ok), merge (T12.4).

> **Desvios registrados na implementação:** (1) A4: os PNG dos mapas de contagem **também** passaram a ser
> desenhados a partir da tabela suprimida, não só a gêmea CSV, para o PNG e o HTML mostrarem os mesmos bairros
> sem cor (o plano previa o PNG inalterado); (2) os Blocos 4-7 viraram um commit só, porque foram testados
> juntos (mesma carga do banco); (3) `regen_missing_pngs.py` só regenera os 4 PNG CadÚnico se estiverem
> faltando, porque a cópia de `grafico_barra` dele não tem os rótulos de renda nem o rodapé de fonte; (4) a nova
> tabela `cadunico_por_faixa_renda_2026.csv` e as saídas novas **não são versionadas**: `.gitignore` ignora
> `tabelas_finais/`, `mapas/` e `visualizacoes/` desde 2026-09-22, e só os arquivos já rastreados antes seguem
> no git. O aviso da constitution §3 sobre regras comentadas está desatualizado.
Roadmap: item 8 de `specs/roadmap.md` (itens 6 e 7 ficam para a rodada seguinte).
Desdobramento: `plan.md` (blocos), `tasks.md` (checklist), `validation.md` (critérios).

> **Escopo de alteração.** Os recortes novos (R1-R3) **só acrescentam**: funções, células e saídas
> novas. As saídas CadÚnico **existentes** podem ser corrigidas, porque o usuário pediu a revisão
> delas ("review other visualizations extracted from Cadunico as sanity checks and to improve when
> necessary"). Mesmo assim, cada correção fica listada em §6 (A1-A8) com o porquê, e nada fora da
> seção 🗂️ Cadúnico, das saídas `cadunico_*` e dos trechos CadÚnico dos scripts de relatório é tocado.

---

## 1. Objetivo

1. Tirar do `status: pendente` três indicadores do eixo **🤝 Inclusão** em
   `specs/estrutura_eixos.md` (linhas 187-200):

   | # | Indicador do catálogo |
   |---|---|
   | R1 | Famílias no CadÚnico com crianças até 6 anos, **por sexo** |
   | R2 | Famílias no CadÚnico com crianças até 6 anos, **por raça/cor** |
   | R3 | Famílias no CadÚnico com crianças até 6 anos, **por renda e arranjo familiar** |

2. **Revisar as saídas CadÚnico já publicadas** (4 gráficos, 3 mapas, 6 tabelas) e corrigir o que
   estiver errado ou enganoso (§6).
3. Levar tudo a `analise.py`, `tabelas_finais/`, `visualizacoes/` e `mapas/`, e pelo crosswalk a
   `relatorio/index.html`, ao PDF e ao DOCX de curadoria. O deploy no Pages continua manual e só vem
   após validação.

**Fora de escopo:** os três itens de deficiência (linhas 202-215) e os dois de Moradia com fonte
CadÚnico (inadequação habitacional, adensamento). **Esses campos não existem nas tabelas acessíveis**
(§2.2), então os itens continuam `pendente` até uma extração nova no CTPE (pendência F2, §9).

---

## 2. Fonte: banco CTPE (levantamento de 2026-09-23)

### 2.1 Conexão: ✅ funciona com os parâmetros do `.env`

- `connect_db_ctpe()` (`analise.py:40`) lê `db_name`, `user`, `password_db`, `host` e `port` do `.env`.
  As 5 chaves estão presentes e a conexão abre: PostgreSQL 15.12, schema `ctpe`, `server_encoding` e
  `client_encoding` UTF8.
- ⚠️ **Ambiente Python:** o driver é `psycopg` 3 (`postgresql+psycopg://`, `requirements.txt`:
  `psycopg==3.3.4`). O Python base do Anaconda (`C:\ProgramData\anaconda3`) **não tem** `psycopg` 3,
  só `psycopg2`, e falha com `ModuleNotFoundError`. O env certo é o **`analises_env`** (conda), que
  tem `psycopg 3.3.4` e `geopandas 1.1.4`. O kernel do Jupyter precisa ser esse env.
- `load_dotenv()` sem argumento (`analise.py:920`) acha o `.env` porque o notebook roda da raiz do
  repo. Um script rodado de outra pasta **não** acha o `.env`: aconteceu no teste desta rodada, e a
  URL saiu com `port=None`.
- **Encoding: ok.** O `Ind�gena`/`N�o` do primeiro teste era só o console do Windows (cp1252). Com
  `stdout` em UTF-8 os valores vêm certos (`Indígena`), e os CSV de `tabelas_finais/` estão em UTF-8.

### 2.2 Tabelas e campos disponíveis

| Tabela | Linhas | Partição | Uso |
|---|---|---|---|
| `ctpe.silver_cadunico_geral` | ~2,18 mi pessoas (todas as idades) | **só `2026-06-12`** | já usada por `analise.py:1209` (filtro `grupo_idade='0-6'`) |
| `ctpe.bronze_cadunico` | 2,17-2,18 mi por partição | `2026-05-08`, `2026-06-12` | não usada |

Campos da **silver** (18): `id_pessoa`, `id_familia`, `raca_cor`, `sexo`, `valor_renda_media`,
`data_nascimento`, `n_pessoas_familia`, `cep`, `risco_inseguranca_alimentar`,
`trabalho_infantil_pessoa`, `familia_com_trabalho_infantil`, `data_particao`, `idade`,
`grupo_idade`, `renda_pct`, `grupo_renda_pct`, `valor_renda_familiar`, `grupo_renda_familiar`.

Campos **só na bronze**: `id_membro_familia`, `estado_cadastral`, `identidade_genero`,
`transgenero`, `data_cadastro`, `data_ultima_atualizacao`, `risco_violacao_direitos`,
`despesa_aluguel`, `despesa_medicamentos`, `familia_indigena`, `familia_quilombola`, `ativo`, ...

**Não existem em nenhuma das duas tabelas:** relação de parentesco com o responsável familiar
(RF), um identificador de quem é o RF, deficiência ou tipo de deficiência, e características do
domicílio (material, cômodos, dormitórios, saneamento).

### 2.3 Números de referência: recorte `grupo_idade='0-6'` da silver, partição 2026-06-12

194.138 crianças em 173.768 famílias. **Idades 0 a 5 (§6, S3).**

| Dimensão | Categoria | Crianças | Famílias com ≥1 criança da categoria |
|---|---|---:|---:|
| sexo | Feminino | 94.778 | 89.463 |
| | Masculino | 99.360 | 93.769 |
| raça/cor | Parda | 103.991 | 96.016 |
| | Branca | 68.200 | 63.845 |
| | Preta | 20.670 | 19.452 |
| | Amarela | 1.208 | 1.193 |
| | Indígena | 69 | 64 |
| renda per capita (`grupo_renda_pct`) | 0-218 | 149.426 | 131.808 |
| | 219-810 | 33.435 | 30.948 |
| | 811-1621 | 9.742 | 9.511 |
| | 1621-3242 | 1.374 | 1.347 |
| | 3242+ | 161 | 154 |

Também existe `grupo_renda_familiar` (renda **total** da família). A análise usa só a per capita,
que é o critério de elegibilidade dos programas: R$ 218 é a linha de extrema pobreza e R$ 810,50 é
½ salário mínimo de 2026.

**Famílias não são exclusivas entre categorias da criança.** Uma família com um menino e uma menina
aparece nas duas linhas: 89.463 + 93.769 = 183.232, acima das 173.768 famílias. É a mesma armadilha
dos vínculos em `inclusao_dados_protecao`, e nunca se soma essas linhas.

---

## 3. Recortes (decisões D1-D3 aprovadas)

### R1 — por sexo (D1: atributo da criança)

- Crianças por sexo.
- Famílias por **composição de sexo das crianças**, em categorias exclusivas que somam 173.768: só
  meninas, só meninos, meninas e meninos. Isso responde a "famílias por sexo" sem dupla contagem.
- Bairro: % de meninas entre as crianças, em mapa de taxa com escala contínua (D4). É um mapa de
  baixa variação esperada (~49% em toda parte), candidato a corte na revisão visual (Bloco 12).

### R2 — por raça/cor (D1: atributo da criança)

- Crianças por raça/cor, nas 5 categorias do CadÚnico, mais o agregado **negra = preta + parda**
  (convenção IBGE).
- Famílias com ≥1 criança de cada raça/cor. São **não exclusivas**: o rótulo e a nota avisam, e não
  há linha de total somado. O total de famílias (173.768) aparece à parte.
- Bairro: **só "% de crianças negras"** (taxa, escala contínua). Nenhuma categoria de raça/cor é
  publicada por bairro (D4, §5).

### R3 — por renda e arranjo familiar (D2: proxy; D3: adulto = 18+)

**Arranjo familiar: proxy pela composição etária do cadastro.** Não existe campo de parentesco, mas a
silver traz **todas** as pessoas de cada `id_familia`, com idade e sexo. Pegando as famílias com
≥1 criança 0-5 e contando os membros de 18 anos ou mais por sexo:

| Arranjo (proxy) | Famílias | % | Crianças 0-5 |
|---|---:|---:|---:|
| Uma adulta (mulher) | 141.051 | 81,2% | 158.437 |
| Dois adultos (homem e mulher) | 18.168 | 10,5% | 20.042 |
| Dois adultos (outra composição) | 6.377 | 3,7% | 6.932 |
| Um adulto (homem) | 3.944 | 2,3% | 4.147 |
| Três ou mais adultos | 3.515 | 2,0% | 3.834 |
| Sem adulto (18+) | 713 | 0,4% | 746 |

O cadastro de cada família está completo: o número de linhas por `id_familia` bate com
`n_pessoas_familia` em 100% das 173.768 famílias. As categorias são exclusivas, então somam.

**Nota metodológica obrigatória** (notebook, HTML, PDF e DOCX):
- "Uma adulta" **não** é "família monoparental feminina" no conceito do MDS, que usa parentesco com o
  RF. É uma aproximação pela composição do cadastro.
- Um companheiro que não está no cadastro não aparece. A sub-declaração de cônjuges é um viés
  conhecido do CadÚnico, reforçado pelas regras de renda per capita, e provavelmente infla a categoria
  "Uma adulta".
- As 713 famílias sem nenhum membro de 18+ são inspecionadas em agregado (idade do membro mais velho)
  e ficam como categoria própria. Não são descartadas.

**Renda:** o cruzamento é arranjo × `grupo_renda_pct` (valor único por família, conferido em
validação), em contagem e em % dentro de cada arranjo. Para evitar células pequenas, as faixas acima
de ½ SM se juntam numa só no cruzamento: fica **0-218 / 219-810 / 811+** (§5).

Bairro: % de famílias com "Uma adulta" (taxa, escala contínua).

---

## 4. Implementação em `analise.py`: esboço, detalhado em `plan.md`

- **Funções novas** na seção 📦 (regra do projeto):
  - `carrega_cadunico_familias_0_6(engine)`: `SELECT` de todas as pessoas das famílias com ≥1
    criança `grupo_idade='0-6'`, filtrado no SQL. O `df_original` atual só traz as crianças, e o
    arranjo precisa dos adultos.
  - `classifica_arranjo_familiar(df_membros, idade_adulto=18)`: uma linha por família, com arranjo e renda.
  - `agrega_cadunico_por_categoria(df, coluna)`: crianças (`count`) e famílias (`nunique`) por categoria.
  - `suprime_celulas_pequenas(df, coluna_denominador, colunas, limiar=20)`: aplica a regra de privacidade de §5.
- **Células novas** na seção 🗂️ Cadúnico, depois de "🗺️ Mapas por bairro" (`df_censo` e o join
  CEP→bairro já existem ali).
- **Saídas novas**, com nomes em `specs/tech-stack.md`. Toda chamada cita `fonte_cadunico_particao` (D5):
  - tabelas: `cadunico_por_sexo_2026.csv`, `cadunico_por_raca_cor_2026.csv`,
    `cadunico_familias_por_arranjo_2026.csv`, `cadunico_familias_arranjo_renda_2026.csv`,
    `tabela_mapa_cadunico_recortes_bairro_2026.csv` (gêmea dos 3 mapas, já suprimida)
  - gráficos: `cadunico_criancas_por_sexo.png`, `cadunico_familias_por_sexo_criancas.png`,
    `cadunico_criancas_por_raca_cor.png`, `cadunico_familias_por_raca_cor.png`,
    `cadunico_familias_por_arranjo.png`, `cadunico_familias_arranjo_renda.png`
  - mapas (bairro, taxa, `_CORES_TEMA_MAPA['cadunico']`, `bins=None`):
    `mapa_percentual_cadunico_meninas_bairro_2026.png`,
    `mapa_percentual_cadunico_criancas_negras_bairro_2026.png`,
    `mapa_percentual_cadunico_familias_uma_adulta_bairro_2026.png`
- **Crosswalk:** as três entradas de `specs/estrutura_eixos.md` recebem `visualização:`, `tabela:`,
  `mapa:` e `nota:`, e a `fonte` vira "Cadastro Único (extração CTPE)". HTML e PDF têm esses itens
  *escritos à mão* como `emite_bloco_pendente`/`pending` (`build_html_report.py:1252-1254`,
  `build_notebook_report.py:502-504`), e os blocos são **substituídos** pelos cards reais. O DOCX
  herda do `.md`.

---

## 5. Recorte territorial e privacidade (constitution §6; D4 aprovada)

> **Nota de privacidade (pedida pelo usuário).** O CadÚnico descreve população vulnerável. Nesta
> rodada, **nenhuma saída publicada** mostra uma contagem de crianças ou famílias abaixo de **20** em
> nível sub-municipal. Saída publicada inclui `tabelas_finais/`, que está versionado (constitution
> §3, `.gitignore` comentado), mais o HTML (tooltips e botão "⭳ CSV") e o PDF. Os bairros abaixo do
> limiar aparecem como **"suprimido (< 20)"** em tabela e sem cor em mapa, com nota de rodapé. Os
> microdados só existem em memória durante a execução: nada de nível pessoa ou família é gravado em
> disco, nem em `dados_locais/tratados/`. A regra vale também para as saídas CadÚnico **já
> existentes** (A4), não só para as novas.

- **Limiar:** denominador < 20 (crianças ou famílias, conforme a taxa). Em mapas de contagem, célula < 20.
- **Raça/cor por bairro:** só o agregado "% negra". Amarela (1.208 na cidade) e Indígena (69) nunca
  aparecem abaixo do nível município.
- **Cruzamentos no nível município** (arranjo × renda, raça × família): faixas de renda acima de
  ½ SM se juntam (§3 R3). Qualquer célula que ainda fique < 20 é suprimida com a mesma marcação.
- **Níveis:** só bairro nesta rodada, como as saídas CadÚnico existentes. AP/RP/RA ficam para depois.
  Se entrarem, é via `agrega_bairros_por_nivel`: soma dos absolutos e depois a taxa, **somando também
  os bairros suprimidos**, porque a supressão é de publicação e não de cálculo.
- **Viés de geocodificação (S1/S2 abaixo):** as taxas novas são **internas ao CadÚnico** (numerador e
  denominador da mesma base e do mesmo bairro atribuído), então sofrem bem menos com o viés de
  CEP→bairro do que a razão CadÚnico/Censo. O viés continua existindo e vai na nota do mapa.

---

## 6. Revisão de sanidade das saídas CadÚnico existentes

Feita em 2026-09-23 sobre `tabelas_finais/cadunico_*`, a partir de `analise.py:1194-1368` e de um
reprocessamento do join no banco.

| # | Achado | Evidência | Gravidade |
|---|---|---|---|
| S1 | **8,1% das crianças somem no join CEP→bairro, em silêncio.** A nota do notebook fala só em 380 crianças excluídas, de 178.329 | 194.138 crianças no banco × 178.329 na tabela por bairro. 15.809 têm CEP (todo CEP tem 8 dígitos) sem linha em `dados_locais/lista_bairros.csv` (25.535 CEPs, nenhum duplicado). Os prefixos são da cidade (235xx, 230xx, 218xx, ...) | alta |
| S2 | **O bairro do CEP (Correios) ≠ o bairro oficial (IPP).** Bairros-favela ficam subcontados e os vizinhos, inflados | % CadÚnico/Censo 0-4 > 100% em 8 bairros: Camorim 510%, Bonsucesso 341%, Gávea 313%, Jacaré 242%, Anil 169%, ... Maré tem só 3.405 crianças contra Bonsucesso 2.936, Jacarezinho 277 contra Jacaré 1.409, Rocinha 1.237 contra Gávea 1.858. **Vila Kennedy, Jabour, Gericinó, Ilha de Guaratiba e Lapa não aparecem**: os CEPs caem em Bangu, Senador Camará, Guaratiba e Centro. A nota atual do mapa culpa a "metodologia de contagem diferente", mas a causa principal é essa | alta (mapas por bairro) |
| S3 | O rótulo diz **"0-6 anos", mas os dados vão de 0 a 5** (`idade` ∈ {0..5}, sem 6) | `cadunico_por_idade_2026.csv`. Verificado no banco: `grupo_idade='0-6'` = nascidos entre **2020-08-12** e 2026-06-05. A `idade` é calculada numa data de referência **~2026-08-12**, e não na partição (2026-06-12): a idade recalculada na partição fica 1 ano abaixo em parte das crianças. As crianças com **6 anos** caem no grupo **`'7-14'`** (idade 6-8 nesse grupo), ou seja, o rótulo upstream também engana. Pelo Marco Legal (até 72 meses), 0-5 completos é o recorte da primeira infância, mas **outras fontes do projeto usam outros recortes** (Censo 0-4, etc.). Ver D7 | média |
| S4 | **Células pequenas publicadas.** 10 bairros têm < 20 crianças e 6 têm < 10 (Argentino 3, Campo dos Afonsos 4, Lagoa 5, Joá 6, Urca 6, Zumbi 7). O HTML mostra o valor exato no tooltip e no CSV | `cadunico_por_bairro_2026.csv`, `tabela_mapa_*` | média (privacidade) |
| S5 | `cadunico_por_faixa_etaria_2026.csv` contém o recorte **por renda**, não por faixa etária | `analise.py:1232`, lido por `build_html_report.py:1267`, `build_notebook_report.py:520,521,529`, `regen_missing_pngs.py:81` | baixa (nome) |
| S6 | "Famílias por idade" **não soma** o total de famílias: uma família com 2 crianças de idades diferentes conta 2 vezes. Nada no gráfico avisa | Σ famílias por idade = 191.824 > 173.768 | baixa |
| S7 | Sub-registro no 1º ano: idade 0 tem 11.328 crianças contra 43.187 com 5 anos. É esperado (defasagem de cadastro do recém-nascido), mas não está anotado | `cadunico_por_idade_2026.csv` | baixa (nota) |
| S8 | Faixas de renda com rótulo só numérico ("0-218"), sem o significado para o público não técnico | gráficos de renda | baixa (legibilidade) |
| S9 | Não se sabe se a silver já filtra cadastros ativos ou atualizados: `estado_cadastral`/`ativo` só existem na bronze | §2.2 | a confirmar com o CTPE (F3) |

### Correções propostas (A = ação nesta rodada)

| # | Corrige | Ação |
|---|---|---|
| A1 | S1 | Tabela por bairro ganha a linha explícita **"Sem bairro identificado (CEP fora da lista)"**. A nota do notebook é reescrita com os números reais (15.809 sem CEP na lista + 380 em localidades sem bairro oficial) e o HTML/PDF citam a cobertura (~91,6%). Enriquecer `lista_bairros.csv` fica fora (F1) |
| A2 | S2 | A nota do mapa % CadÚnico/Censo é reescrita com a causa real e a lista dos bairros afetados. Todos os mapas CadÚnico por bairro recebem a nota de viés de geocodificação. **D6** decide se o mapa % CadÚnico/Censo continua no relatório publicado |
| A3 | S3 | **Adiada (D7).** Os títulos e rótulos existentes **não** mudam nesta rodada. A definição de idade vai para a auditoria de faixas etárias entre fontes do roadmap item 6. Nesta rodada, só: (i) uma nota no notebook com a definição real (nascidos a partir de 2020-08-12; idade em ~2026-08-12; 6 anos no grupo `'7-14'`); (ii) as saídas **novas** usam a redação do catálogo ("crianças até 6 anos") com a nota "idades de 0 a 5 anos completos" |
| A4 | S4 | `suprime_celulas_pequenas` (limiar 20) aplicada às tabelas e gêmeas de mapa **existentes** (`cadunico_por_bairro_2026`, `cadunico_por_bairro_ate_4_2026`, `tabela_mapa_cadunico_*`) antes de gravar. O PNG de contagem não muda (a menor classe já é < 200/250), mas o tooltip e o CSV do HTML passam a mostrar "suprimido" |
| A5 | S5 | Renomear para `cadunico_por_faixa_renda_2026.csv` e atualizar os 4 leitores, o crosswalk e o `README.md:74`. O arquivo antigo é removido do versionamento (**D8**). Verificado em 2026-09-23 (`grep` no repo): **todos** os usos do nome antigo leem o conteúdo de renda, e nenhuma visualização precisa de uma tabela CadÚnico por faixa etária com esse nome. O recorte por idade simples já está em `cadunico_por_idade_2026.csv`. Se uma tabela CadÚnico por faixa etária for necessária no futuro (ex. 0-3 creche × 4-5 pré-escola), ela nasce com nome próprio, dentro da revisão de nomes do roadmap item 6 |
| A6 | S6, S7 | Nota no notebook e texto no HTML/PDF: "famílias por idade não somam" e o sub-registro no 1º ano. Os gráficos não mudam |
| A7 | S8 | Rótulos descritivos nas faixas de renda: "Extrema pobreza (até R$ 218)", "Pobreza/baixa renda (R$ 218-810)", "½ a 1 SM", "1 a 2 SM", "acima de 2 SM" per capita. Um dicionário único `_ROTULOS_RENDA_CADUNICO` é reusado nos gráficos novos e nos existentes |
| A8 | S9 | Só registro: nota no notebook e pendência F3. Nenhuma mudança de número |

---

## 7. Validação: resumo, detalhes em `validation.md`

- Totais batem com §2.3. Arranjo: Σ famílias = 173.768 e Σ crianças = 194.138. Sexo exclusivo: Σ = 173.768.
- Bairro: Σ crianças com bairro + "sem bairro identificado" + localidades sem bairro oficial = 194.138.
- Nenhuma saída publicada tem contagem sub-municipal < 20 (varredura automática nos CSV e no HTML).
- Notebook rodado do zero no kernel `analises_env` (constitution §2).
- HTML, PDF e DOCX regenerados. Os 3 itens aparecem no eixo Inclusão, e o resto do relatório fica
  idêntico ao baseline, fora das saídas CadÚnico corrigidas.

---

## 8. Decisões

| # | Pergunta | Decisão |
|---|---|---|
| D1 | "Por sexo" e "por raça/cor" como atributo **da criança** | ✅ **Sim** (usuário, 2026-09-23) |
| D2 | Arranjo familiar pelo proxy de composição | ✅ **Sim.** Pedido ao CTPE de extração com parentesco/RF registrado como F2 |
| D3 | Idade de corte de "adulto" | ✅ **18 anos** |
| D4 | Recorte territorial e privacidade | ✅ **Ok**: bairro para sexo e arranjo (taxa), raça só como "% negra" por bairro, supressão < 20, **com nota de privacidade** (§5) |
| D5 | Data da partição na fonte | ✅ **Sim**: `fonte_cadunico_particao = 'CadÚnico (extração CTPE, jun/2026)'` nas chamadas novas. As corrigidas em A1-A7 passam a usá-la também, e `fonte_cadunico` fica definida como está |
| D6 | O mapa "% crianças 0-4 no CadÚnico sobre o Censo" (valores até 510% por viés de CEP, S2) continua no **relatório publicado**? | ✅ **Sai do HTML e do PDF** até o F1 ser resolvido. Continua no notebook, com nota corrigida (usuário, 2026-09-23) |
| D7 | Corrigir "0-6" → "0 a 5 anos" nos textos? | ⏸️ **Adiada** (usuário, 2026-09-23): "precisamos ter certeza do que o dado representa. CadÚnico é 0 a 6 (nossa extração), mas Censo e outros dados podem não ser". A definição real do CadÚnico está verificada (S3), mas a padronização de rótulos de idade é feita **junto com os itens 6 e 7 do roadmap**, numa auditoria de faixas etárias entre todas as fontes. Nesta rodada: nota de definição + redação do catálogo nas saídas novas (A3) |
| D8 | Renomear `cadunico_por_faixa_etaria_2026.csv` → `cadunico_por_faixa_renda_2026.csv` | ✅ **Sim** (usuário, 2026-09-23), condicionado a checar se o original ainda serve a outra visualização. Checado: não serve (A5). A revisão geral de nomes (tabelas, visualizações, mapas) entrou no roadmap item 6 |

---

## 9. Pendências fora desta rodada

- **F1:** a geocodificação CEP→bairro precisa ser refeita, idealmente por coordenada ou CEP
  georreferenciado + join espacial com `limite_bairros_rio.geojson`, ou por um código de bairro
  fornecido pelo CTPE. Isso resolve S1 e S2 de verdade. Candidato ao roadmap.
- **F2:** pedido ao CTPE de uma extração com parentesco/RF (arranjo real), deficiência (3 itens de
  Inclusão) e características do domicílio (2 itens de Moradia).
- **F3:** confirmar com o CTPE o filtro de cadastro (ativo, atualizado em ≤ 24 meses) aplicado na silver.
