# Plano técnico — Merge das mudanças da Waleska

Companion de `specs.md` (o resumo dos 4 commits e dos riscos encontrados). Aqui está **como**
o merge foi/será executado, as decisões de estratégia e a validação numérica independente do
único bug de cálculo em jogo.

---

## 1. Estratégia de merge escolhida

Três opções foram consideradas:

| opção | prós | contras | escolhida? |
|---|---|---|---|
| `git merge --no-ff` (real, preservando os 4 commits + autoria da Waleska) | histórico completo e auditável; `git blame` continua apontando pra autora certa; reversível com `git revert` de um único commit de merge | nenhum, dado que o teste `--no-commit` não achou conflito | ✅ sim |
| Cherry-pick commit a commit | mesmo resultado, mais granular | mais passos manuais pro mesmo resultado, sem ganho já que não há conflito | não |
| Squash num commit só | histórico mais enxuto | perde a autoria/mensagens individuais da Waleska sem necessidade | não |

Decisão: merge real. O branch de origem (`origin/waleska-analise-primeira-infancia`) parte de
um commit antigo (`3a258e8`, antes de `specs/maps-and-ibge`/`specs/visual-identity`/
`specs/relatorio-interativo`), mas como as regiões de `analise.py` que ela editou não se
sobrepõem às que essas três rodadas tocaram, o merge de 3 pontas do git resolve sozinho — ver
`specs.md` §Teste de merge para a confirmação (`--no-commit --no-ff`, zero conflitos, revertido
antes de decidir).

Executado: commit `ed964a5` neste branch (`specs/merge-waleska-changes`, criado a partir de
`planning`).

---

## 2. Mapeamento de correções — o que quebrava e o que foi feito

`specs.md` já lista a tabela de saídas que pararam de ser geradas e onde eram referenciadas.
Aqui está a ação tomada para cada uma, por arquivo:

| Saída removida/perdida | Causa | Ação | Onde |
|---|---|---|---|
| `tabelas_finais/censo_0_a_4_anos_por_ano.csv` | Esquecimento na reescrita do bloco de agregação (commit 1) | `.to_csv(...)` restaurado em `analise.py`, logo após o cálculo do percentual corrigido | `analise.py` |
| `mortalidade_causas_evitaveis_raca_municipio_ano.csv` + 4 PNGs de raça/cor | Removido de propósito (commit 2) | Seção "Óbitos por causas evitáveis por raça/cor" removida de ambos os builders | `build_notebook_report.py`, `build_html_report.py` |
| 18 PNGs da matriz subgrupo×CAP×faixa | Removido de propósito (commit 2) | Bloco `h6('Por CAP e faixa etária, por subgrupo')` + dict `_SLUG_SUBGRUPO_PDF` removidos | `build_notebook_report.py` (não afeta `build_html_report.py`, que deriva o equivalente direto do CSV compartilhado, ainda gerado) |
| Mapas + séries de gestação/parto por CAP | Removido de propósito (commit 2) | Bloco `h6('Gestação e parto...')` removido; 2 entradas de mapa removidas de `MAP_GROUPS` | `build_notebook_report.py` |
| CSV `tabela_mapa_obitos_evitaveis_{slug}_menores_1_ano_cap_2025.csv` (gestação/parto) | Removido de propósito, mesmo commit | Grupo de mapas "Por subgrupo (gestação e parto)" removido (`_SUBGRUPOS_COMPONENTE_C` e dependências) | `build_html_report.py` |
| Mapas absolutos de gravidez/puerpério por bairro | Removido de propósito (commit 2) | Grupo `("Gravidez e puerpério", [...])` removido inteiro de `MAP_GROUPS` (as duas entradas do grupo foram removidas) | `build_notebook_report.py` |
| Mapas absolutos de neonatal tardia/pós-neonatal por bairro | Removido de propósito, taxa mantida (commit 2) | As 2 entradas absolutas removidas do grupo `"Mortalidade neonatal"`; entradas de taxa mantidas | `build_notebook_report.py` |
| 4 mapas AP/RP do Censo (absoluto+percentual × ap+rp) | Removido de propósito (commit 1) | 4 entradas removidas do grupo `"Censo/população"` | `build_notebook_report.py` |
| PNG principal de cobertura vacinal (`cobertura_vacinal_epi_ano.png`) | Removido de propósito, comparativo mantido (commit 3) | `chart_block(...)` removido; tabela (`table_html`, do CSV que continua sendo exportado) mantida | `build_notebook_report.py` |

Princípio seguido: **remover só a referência à saída que parou de existir**, nunca a seção
inteira quando parte dela ainda é válida (ex.: cobertura vacinal mantém a tabela; mortalidade
neonatal mantém os mapas de taxa) — evita perder conteúdo que a curadoria da Waleska não pediu
para remover.

---

## 3. Validação numérica independente do bug de cálculo (Censo)

`specs.md` afirma que a versão antiga do `total_e_percentual_ano` produzia um "percentual"
sem sentido (soma de percentuais por bairro, não percentual recalculado dos totais). Em vez de
confiar só na leitura do diff, a lógica das duas versões foi replicada em pandas e rodada
contra os 3 CSVs reais do Censo (`dados_locais/censo/tabela 2974_{2000,2010,2022}.csv`):

| Ano | Bairros | % antigo (soma de percentuais por bairro) | % novo (recalculado dos totais somados) |
|---|---|---|---|
| 2000 | 158 | **1.091,84%** | **7,09%** |
| 2010 | 160 | **837,37%** | **5,45%** |
| 2022 | 166 | **751,97%** | **4,75%** |

O valor antigo é literalmente sem sentido (>100%, cresce com o número de bairros — é uma soma,
não uma média nem um percentual). O valor novo é plausível e consistente com uma tendência de
queda na participação de crianças de 0-4 anos na população total ao longo dos censos — direção
esperada dado o envelhecimento populacional do município. **Confirma objetivamente que o
commit 1 da Waleska corrige um bug real**, não é uma mudança cosmética.

Comando usado (reprodutível, só precisa de `pandas`):

```python
import pandas as pd

def total_e_percentual_ano_old(df):
    df = df.copy()
    df['0 a 4 anos'] = df['Sexo feminino, 0 a 4 anos'] + df['Sexo masculino, 0 a 4 anos']
    df['Total'] = df.iloc[:, 9:].sum(axis=1)
    df['Percentual 0 a 4 anos'] = df['0 a 4 anos'] / df['Total']
    return df

for ano, path in [('2000', 'dados_locais/censo/tabela 2974_2000.csv'),
                   ('2010', 'dados_locais/censo/tabela 2974_2010.csv'),
                   ('2022', 'dados_locais/censo/tabela 2974_2022.csv')]:
    df = total_e_percentual_ano_old(pd.read_csv(path, sep=';'))
    pct_old_bug = df['Percentual 0 a 4 anos'].sum() * 100                       # bug: soma de fração por bairro
    pct_new_fix = (df['0 a 4 anos'].sum() / df['Total'].sum()) * 100            # correto: recalcula dos totais
    print(ano, pct_old_bug, pct_new_fix)
```

---

## 4. O que este ambiente não conseguiu validar em tempo de execução

- **Sem conexão com o Postgres do CadÚnico** (`connect_db_ctpe`) — não dá pra rodar
  `analise.py` de ponta a ponta nesta sessão, já que a seção CadÚnico vem antes da seção de
  Mortalidade (onde as mudanças da Waleska estão) na ordem do notebook.
- **`geopandas`/`contextily` não instalados no ambiente local** (`analise_env/` incompleto) —
  não tentado instalar por serem pesados (dependem de GDAL) e não serem necessários pra validar
  o que mudou (nenhuma mudança da Waleska mexe em mapas ou geometria, só em quais mapas são
  chamados).
- **`pandas` foi instalado sob demanda** (`pip install pandas`, rede via HTTPS disponível
  mesmo sem acesso SSH ao GitHub) só para a validação numérica da §3 — suficiente pra essa
  checagem pontual, insuficiente pra rodar o notebook inteiro.

Ver `validation.md` para a lista completa de checagens, incluindo as que ficam pendentes de um
ambiente com banco/rede.

---

## 5. Próximos passos

1. Rodar `analise.py` de ponta a ponta (kernel limpo) num ambiente com acesso ao Postgres —
   confirma em runtime o que hoje só foi confirmado estaticamente (`ast.parse` + grep).
2. Rodar o skill `export_pdf_report` de ponta a ponta — confirma que
   `build_notebook_report.py`/`build_html_report.py` realmente geram o PDF/HTML sem
   `FileNotFoundError`/`SystemExit`.
3. Merge de `specs/merge-waleska-changes` em `planning` (fast-forward, `planning` não andou
   desde que este branch foi criado).
4. Decisão do usuário sobre subir `planning`/o resultado deste merge para `staging_main`.
