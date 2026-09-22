# Tarefas — Óbitos por causas evitáveis por Área Programática de Saúde (CAP)

> **Revisão 3.** Bloco 4 reescrito de novo: o usuário autorizou a exceção pontual que a
> revisão 2 tinha descartado — acrescentar a chave `'cap'` a `_NIVEIS_AGREGACAO`. Cai o
> adaptador `mapa_coropletico_cap` e o alias `cod_rp` no geojson de CAP.
> ⛔ **Regra permanente: nenhuma linha de `analise.py` que já existe pode ser editada — com
> a única exceção da chave `'cap'` em `_NIVEIS_AGREGACAO` (Bloco 4), que não pode alterar os
> códigos/colunas já atribuídos a `bairro`/`ap`/`rp`.**

Ordem de execução. Cada bloco só começa depois do anterior passar na validação
correspondente (`validation.md`).

---

## Bloco 0 — Decisões

- [x] **T0.1** — Usuário revisou a revisão 1 dos documentos
- [x] **T0.2** — Nível **CAP** confirmado; `nivel='ap'` existente permanece intocado
- [x] **T0.3** — Restrição registrada: **nunca alterar código existente**, exceto a chave
      `'cap'` em `_NIVEIS_AGREGACAO` (autorizado na revisão 3, `plan.md` §4.1)
- [x] **T0.4** — Geometria oficial obtida (Data.Rio, "Áreas Programáticas da Saúde")
- [x] **T0.5** — De-para RA→CAP corrigido pelo dado oficial (Guaratiba→5.2, Alemão→3.1)
- [x] **T0.6** — Usuário revisou a revisão 2; revisão 3 liberou a chave `'cap'` direta em
      `_NIVEIS_AGREGACAO` (era o item D) ⛔ *não começar o Bloco 2 antes do aval da revisão 3*
- [ ] **T0.7** — Opcional, não bloqueia (`specification.md` §8): texto da fonte (A), destino
      dos CSVs (B), NV por CAP (C), versionar a spec (E)

---

## Bloco 1 — Arquivo

- [ ] **T1.1** — `mv "dados_locais/mortalidade/Óbitos por causas evitáveis na Primeira Infância.xlsx" "dados_locais/mortalidade/obitos_causas_evitaveis_primeira_infancia_cap_2006_2025.xlsx"`
- [ ] **T1.2** — `git add` do arquivo renomeado (hoje untracked)
- [ ] **T1.3** — Confirmar que o `.gitignore` não exclui `.xlsx` (não exclui — só `.zip`,
      `.png`, `.svg`, `.html`, `.ipynb`)
- [x] **T1.4** — Baixar o geojson oficial das CAPs do Data.Rio e salvar em
      `dados_locais/geo/limite_ap_saude_rio.geojson` (`make_valid`, coluna `cod_ap_sms`) —
      ✅ **feito**. A coluna `cod_rp` gravada como alias na revisão 2 não é mais necessária
      (`plan.md` §4.3) — se ainda estiver no arquivo, é inofensiva; remoção fica opcional
- [ ] **T1.5** — `git add` do geojson novo

→ **valida com V0**

---

## Bloco 2 — Funções de extração (`### 🧹 Limpeza e wrangling de dados`)

- [ ] **T2.1** — `extrai_evitaveis_cap_blocos(caminho, aba, anos)` — 10 blocos × 12 linhas → longo
      `cod_ap_sms, causa, ano, obitos`; descarta linha `Total` e coluna `Total`; normaliza
      `causa` para o texto de `subgrupo` via `_ROTULO_PARA_SUBGRUPO` (`plan.md` §3.0/§2.4 da spec)
- [ ] **T2.2** — `extrai_evitaveis_municipio(caminho)` — 3 tabelas da aba `Informações gerais`;
      ` Ign` + ` Ignorado` somados em `Ignorado`; mesma normalização rótulo→subgrupo na tabela `por_causa`
- [ ] **T2.3** — `extrai_planilha_evitaveis_cap(caminho)` — orquestrador; escreve os 6 CSVs
      em `dados_locais/tratados/`
- [ ] **T2.4** — dict `_ROTULO_PARA_SUBGRUPO` (rótulo bruto → subgrupo normalizado, `plan.md` §3.0)
      + `agrega_grupo_cid(df, colunas_chave)` + dict `_GRUPOS_CID` — sempre as duas colunas,
      `subgrupo` e `grupo`, nunca uma `causa` genérica
- [ ] **T2.5** — Docstrings no estilo do arquivo (pt-BR, explicando o *porquê* das decisões,
      não só o *quê*)

→ **valida com V1, V2, V3, V4**

---

## Bloco 3 — Chamada na limpeza prévia (`### 🧼 Limpeza de dados prévia`)

- [ ] **T3.1** — Adicionar a chamada `extrai_planilha_evitaveis_cap(...)` ao lado das duas
      `limpa_dados_sisvan(...)`
- [ ] **T3.2** — Rodar e conferir que os 6 CSVs aparecem em `dados_locais/tratados/`

---

## Bloco 4 — Mapa por CAP: chave nova em `_NIVEIS_AGREGACAO`

⛔ `mapa_coropletico_bairros` e `agrega_bairros_por_nivel` **não são tocadas** (zero linhas —
`plan.md` §4.2 confere isso contra o código real). A **única** exceção autorizada é a chave
`'cap'` em `_NIVEIS_AGREGACAO`, e mesmo essa não pode alterar as três chaves existentes
(`bairro`, `ap`, `rp`). Ver `plan.md` §4 para o porquê e para as alternativas descartadas.

- [ ] **T4.1** — Acrescentar a chave `'cap': {'coluna_geo': 'cod_ap_sms', 'tipo': str}` a
      `_NIVEIS_AGREGACAO` (`plan.md` §4.1) — única linha nova; `bairro`/`ap`/`rp` bit-a-bit
      idênticas (checar com `git diff`)
- [ ] **T4.2** — Chamar `mapa_coropletico_bairros(..., nivel='cap',
      caminho_geojson='dados_locais/geo/limite_ap_saude_rio.geojson')` direto nas células de
      análise — sem função adaptadora, sem alias
- [ ] **T4.3** — Constante nova `_RA_PARA_CAP` (de-para corrigido), **só documental** nesta
      entrega — não usada pelos mapas
- [ ] **T4.4** — Mapa de fumaça: gerar 1 mapa por CAP e conferir 10 polígonos, 0 "Sem dado"
- [ ] **T4.5** — ❌ **NÃO** editar `.claude/skills/generate_map/SKILL.md` (documenta código
      existente). Em vez disso, se valer a pena, acrescentar uma seção nova ao final sobre o
      nível CAP — decisão do usuário, fora do caminho crítico

→ **valida com V5, V10.2**

---

## Bloco 5 — Seção de análise (`📉 Mortalidade`)

Inserir **depois** de `###### Pós-neonatal...`/`por grupo de causa e faixa etária` e **antes**
de Mortalidade Neonatal.

### 5.1 Panorama municipal (< 5 anos)

- [ ] **T5.1.1** — Célula markdown: título + as 6 notas de `plan.md` §6
- [ ] **T5.1.2** — Ler os 3 CSVs municipais; exportar para `tabelas_finais/`
- [ ] **T5.1.3** — `serie_temporal_multipla` — 8 subgrupos CID, MRJ, < 5 anos
      → `obitos_evitaveis_menores_5_subgrupo_ano.png`
- [ ] **T5.1.4** — `serie_temporal` — taxa por mil NV
      → `taxa_mortalidade_evitaveis_menores_5_ano.png`

### 5.2 Por CAP e faixa etária

- [ ] **T5.2.1** — Dict `faixas_primeira_infancia` (aba, rótulo, bins)
- [ ] **T5.2.2** — Empilhar as 3 abas → `mortalidade_evitaveis_cap_faixa_ano.csv`
      (`dados_locais/tratados/` + `tabelas_finais/`)
- [ ] **T5.2.3** — `agrega_grupo_cid` + percentual → `mortalidade_evitaveis_grupo_cap_faixa_ano.csv`
- [ ] **T5.2.4** — 3 séries temporais de óbitos evitáveis por CAP (uma por faixa)
- [ ] **T5.2.5** — 3 séries temporais de % evitáveis por CAP (uma por faixa)
- [ ] **T5.2.6** — 1 série temporal de óbitos totais por CAP (< 5 anos)

### 5.3 Mapas por CAP (2025)

- [ ] **T5.3.1** — Recorte 2025 → `mortalidade_evitaveis_cap_2025.csv` e
      `mortalidade_evitaveis_subgrupo_cap_2025.csv`
- [ ] **T5.3.2** — Imprimir `.describe()` da distribuição 2025 por faixa **antes** de escolher
      os `bins` (⚠️ não chutar)
- [ ] **T5.3.3** — Preencher os `bins` em `faixas_primeira_infancia`
- [ ] **T5.3.4** — 3 mapas absolutos (classes discretas) via `mapa_coropletico_bairros(nivel='cap')`, um por faixa
- [ ] **T5.3.5** — 3 mapas de percentual (colorbar contínua) via `mapa_coropletico_bairros(nivel='cap')`, um por faixa
- [ ] **T5.3.6** — 🔒 *bloqueado por T0.7-C*: 3 mapas de taxa por mil NV, se o export de
      nascidos vivos por CAP existir

→ **valida com V6, V7**

---

## Bloco 6 — Documentação

- [ ] **T6.1** — README: nova entrada em `## Fontes de dados`
- [ ] **T6.2** — README: nova entrada em `## Fluxo de Análise (analise.py)`
- [ ] **T6.3** — README: bloco em `## Recent changes in analise.py`
- [ ] **T6.4** — README: linha nova na `## Update Table` (próxima versão após 0.8.0)
- [ ] **T6.5** — Sincronizar `analise.ipynb` via jupytext
- [ ] **T6.6** — README: citar a fonte do geojson de CAP (Data.Rio) em `## Fontes de dados`
- [ ] **T6.7** — Mover esta pasta `specs/mortalidade-ap/` para o commit final ou descartá-la
      (decisão do usuário — `relatorio/specs.md` é o precedente de spec versionada)

→ **valida com V8**

---

## Bloco 7 — Fechamento

- [ ] **T7.1** — Rodar `analise.py` de ponta a ponta e confirmar que nenhuma seção anterior
      quebrou (V9)
- [ ] **T7.2** — Conferir os 6 PNGs de mapa e os 7 de série temporal abrindo os arquivos
- [ ] **T7.3** — Commit na branch `spec/mortalidade-ap`
- [ ] **T7.4** — Merge em `staging_main` (só após aval do usuário)

---

## Itens opcionais / segunda rodada

- [ ] Small multiples CAP × subgrupo CID (10 × 8) — hoje fora de escopo
- [ ] Simplificar o geojson de CAP (2,57 MB → ~200 KB) se o tamanho no git incomodar
- [ ] Remover a coluna `cod_rp` do geojson de CAP se ainda estiver lá (não usada desde a revisão 3, `plan.md` §4.3)
- [ ] Atualizar `relatorio/index.html` e derivados com os novos gráficos
- [ ] Regerar o PDF (`skill export_pdf_report`)
- [ ] Mapas por CAP para outros anos além de 2025 (a função já seria genérica — é só um loop)
