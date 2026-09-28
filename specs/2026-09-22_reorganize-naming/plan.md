# Plano — Convenção de nomes (dados_locais / tabelas_finais / visualizacoes / mapas)

**Não executado ainda** — proposta para revisão antes de mexer em ~150 arquivos versionados
e nos 3 scripts de relatório.

## Achado principal: bug real, não só estética

`build_html_report.py` lê **tabelas legadas e paradas no tempo** para 2 dos mapas de
Natalidade, em vez das tabelas que `analise.py` gera hoje:

| Mapa | Lê hoje (legado, parado) | `analise.py` gera hoje | Diferença de schema |
|---|---|---|---|
| Nascidos vivos | `tabela_mapa_bairros_nascidos_vivos_bruto.csv` | `tabela_mapa_nascidos_vivos_2025.csv` | coluna `value` (legado) vs `nascidos vivos` (atual); legado não tem coluna `ano` |
| Baixo peso | `tabela_mapa_bairros_nascidos_abaixo_peso.csv` | `tabela_mapa_nascidos_baixo_peso_2025.csv` | coluna `Nascidos abaixo peso` (legado, maiúscula) vs `nascidos abaixo peso` (atual, minúscula) |

Nenhum código de `analise.py` escreve mais os dois arquivos legados (confirmado por grep —
zero ocorrências do nome). Ambos têm a mesma data de disco que o resto do lote gerado em
09/09 — ou seja, congelados desde então; a próxima vez que os dados de nascidos vivos forem
atualizados (novo ano, correção na fonte), **esses dois mapas do relatório não vão refletir a
mudança**, e ninguém vai perceber porque o script não dá erro. É exatamente o tipo de
divergência silenciosa que motivou o pedido de "manter convenção consistente pra rastrear o
que é parte do quê".

## Inventário: arquivos confirmados órfãos (não gerados por nada hoje)

Verificado por busca de cada nome-base em `analise.py` + `build_notebook_report.py` +
`build_html_report.py` + `regen_missing_pngs.py` (cuidado: descontados falsos positivos de
nomes montados por f-string/loop, ex. `obitos_evitaveis_cap_{sufixo}_ano` — esses **são**
gerados, só não aparecem como string literal).

**`tabelas_finais/`** (5):
- `tabela_mapa_bairros_nascidos_vivos_bruto.csv`, `tabela_mapa_bairros_nascidos_abaixo_peso.csv` — legado, ver bug acima (substituir referência, não só apagar)
- `censo_por_bairro_2022.csv` — duplicata órfã de `censo_por_bairro.csv` (o nome ativo)
- `agregados_saude_datasus.xlsx`, `tabnet_nascidos_vivos_e_abaixo_peso_por_ano.csv` — Excel/CSV legados, sem call site

**`visualizacoes/`** (21):
- 18 PNGs da matriz subgrupo×CAP removida pela curadoria da Waleska (`obitos_evitaveis_{imunizacao,gestacao,parto,recem_nascido,diagnostico_tratamento,promocao_vinculacao}_cap_{1_a_4_anos,menores_1_ano,menores_5_anos}_ano.png`) — já esperado, `specs/2026-09-22_merge-waleska-changes`
- `taxa_ano.png` — nome genérico, zero referência, de 09/09
- `percentual abaixo nascidos vivos abaixo do peso_ano.png`, `percentual nascidos vivos abaixo do peso_ano.png` — **espaço literal no nome**, de 09/09

**`mapas/`** (11):
- 6 PNGs do Censo AP/RP e 2 de gestação/parto por CAP, removidos pela curadoria da Waleska — esperado
- `Nasc abaixo do peso abs.png`, `Nasc abaixo do peso proporção.png`, `Nº absoluto crianças de 0 a 4.png`, `Nº nasc vivos absoluto.png`, `Proporção crianças de 0 a 4.png` — **5 arquivos com espaço/maiúscula/acento**, claramente pré-`mapa_coropletico_bairros` (nomes "de leitura", não de código), de 09/09

**Achado à parte, não bloqueia nada**: `mapas/mapa_referencia.jpeg` (a imagem QGIS externa que
`generate_map/SKILL.md`, o README e um comentário em `analise.py` citam como referência do
estilo de legenda) **não existe no repositório**. Não impede nada tecnicamente (é só citada em
prosa), mas as 3 citações ficam órfãs. Não é parte deste plano — só registro.

**Fora de escopo, intencional**: `mapas/tabelas_bairros/*.xlsx` — README já documenta isso
como o "resquício do padrão anterior", mantido de propósito para 2 tabelas que não migraram.
Não mexer sem pedido à parte.

## Convenção proposta

Já existe um padrão dominante — a proposta é **formalizar o que já é maioria**, não inventar
algo novo, e só re-nomear o que quebra o padrão:

```
{tema}_{indicador}[_{corte}]_{granularidade_ou_ano}.{ext}
```

- `tema`: mesmo nome da pasta de `dados_locais/` de origem quando fizer sentido
  (`censo`, `mortalidade`, `sisvan`, `cadunico`, `vacinacao`, `sidra`) — já é o padrão em
  ~90% dos arquivos atuais.
- `indicador`: o que a coluna de valor mede (`nascidos_vivos`, `obitos_evitaveis`,
  `frequencia_escolar`).
- `corte`: opcional — `raca`, `sexo`, `subgrupo`, `cap`.
- Sufixo de granularidade: `_por_ano` (série temporal município), `_bairro_ano` (série por
  bairro), `_{ANO}` (corte transversal de um ano — mapas). `tabela_mapa_` como prefixo continua
  reservado para o par CSV↔PNG de cada mapa (já é a convenção, ex.
  `tabela_mapa_nascidos_vivos_2025.csv` ↔ `mapa_nascidos_vivos_bairro_2025.png`).
- **Nome do PNG em `visualizacoes/`/`mapas/` reaproveita o nome do CSV em `tabelas_finais/`**
  sempre que os dois existem para o mesmo indicador (já é o caso na maioria) — é o mecanismo
  de rastreio pedido, não uma tabela de mapeamento à parte pra manter sincronizada.

## Ação proposta (aguardando aprovação)

1. **Corrigir o bug** (prioridade real, não cosmética): trocar as 2 leituras em
   `build_html_report.py` para os arquivos/colunas atuais (`tabela_mapa_nascidos_vivos_2025.csv`
   col. `nascidos vivos`; `tabela_mapa_nascidos_baixo_peso_2025.csv` col. `nascidos abaixo peso`,
   já filtrado a 2025 no caso de nascidos vivos, filtro por `ano==2025` já existe pro baixo peso).
2. **Apagar os órfãos confirmados** (36 arquivos, listados acima) — zero call site, zero risco.
3. **Não renomear em massa** o resto — já segue a convenção proposta na prática. Só os 2 pares
   legado↔atual do item 1 precisam de decisão (manter os 2 nomes com o legado aposentado, como
   proposto, em vez de inventar um terceiro nome para ambos).
4. Documentar a convenção em `specs/tech-stack.md` (não em `constitution.md` — é uma convenção
   de projeto, não uma regra de processo).

## Execução — ✅ concluída (2026-09-22)

Usuário aprovou os itens 1-2. Feito, nesta ordem:

1. `build_html_report.py` corrigido (tabelas/colunas atuais).
2. 39 arquivos órfãos removidos (5 "de leitura" incluídos — sem objeção).
3. Convenção documentada em `specs/tech-stack.md` (item 4), não em
   `constitution.md`.
4. `.gitignore` corrigido à parte (linhas de `mapas/`/`tabelas_finais/`/
   `visualizacoes/` estavam comentadas, virando texto solto em vez de regra).
5. `relatorio/`, `mapas/`, `tabelas_finais/`, `visualizacoes/`,
   `dados_locais/tratados/` regenerados de verdade (CadÚnico no último
   estado salvo). PDF renderizado via Chromium/Playwright e verificado por
   amostragem de páginas antes de substituir o arquivo.
