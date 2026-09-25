# Plano técnico — Inclusão dos dados do eixo Proteção

Baseado em `specification.md` (rascunho 2). IDs de entrega (T1-T7, G1-G8, M1-M10) e decisões
(D1-D9) são os da spec. **Nada aqui é executado antes da aprovação da spec e do plano.**

Defaults assumidos por este plano, **sem objeção do usuário até agora** (fáceis de reverter na
revisão): D2 (mãe/pai 2025; "outros" acumulado 2021-2025), D5 (`OrRd`), D6 (rotular vínculos não
excludentes), D7 (+2,5 MB no HTML), D8 (gerar tudo, cortar o redundante na revisão visual),
D9 opção (a) (casos 0-5 ÷ pop 0-4, rotulado).

## Princípio: só se acrescenta

Nenhuma função, assinatura, célula ou saída existente é alterada. Exceções permitidas, todas
*chaves novas em dicionários de configuração*: `'ra'` em `_NIVEIS_AGREGACAO`, tema `protecao` em
`_CORES_TEMA_MAPA` (`analise.py`) e em `_CMAP_TEMA` (`build_html_report.py`), `"ra"` em
`_NIVEL_COL`/`_NIVEL_LABEL`/`_geo_nivel`/`_chave_norm` (HTML). Onde os scripts de HTML/PDF têm o
eixo Proteção *escrito à mão* como blocos `pendente`, esses blocos são **substituídos** (única
alteração de conteúdo existente; é o objetivo da rodada) e o bloco SGB em Moradia é **removido da V1**.

## Descobertas que moldam o plano (verificadas nesta rodada)

1. **HTML e PDF não leem `estrutura_eixos.md`** — `build_html_report.py` (linhas ~1298-1305) e
   `build_notebook_report.py` (~585-595) têm o eixo Proteção hard-coded como 5 chamadas
   `emite_bloco_pendente`/`pending`. Só `gera_docx_curadoria.py` lê o `.md`. Logo: cada mudança no
   eixo exige editar `.md` **e** os dois scripts (limite já documentado em `ajuste_eixos` §9.3).
2. **O bloco SGB aparece duas vezes** por script (Moradia: HTML ~1340, PDF ~635) e no `.md`.
   Remoção da V1 = 3 lugares + o DOCX (que herda do `.md`).
3. **HTML monta os próprios mapas SVG** a partir de `tabelas_finais/tabela_mapa_*.csv`
   (`mapa_svg`) — não usa os PNG de `mapas/`. Cada mapa novo precisa de (i) a tabela-gêmea gerada
   por `analise.py` e (ii) uma chamada `mapa_svg` no HTML. O PDF, ao contrário, usa os PNG.
4. **Paleta divergente preexistente**: `censo` = `Blues` (analise.py) × `Purples` (HTML). Não
   corrigir aqui (fora de escopo); só evitar colisão com o tema novo e registrar (roadmap item 9).
5. **Ponto de inserção em `analise.py`**: depois da última célula de análise ("Junção de tabelas
   município", ~linha 2512) e **antes** de "📝 Análise / Relatório" (~2516). Ordem técnica de
   build; a apresentação por eixo vem do `.md`.
6. **Denominador**: `dados_locais/censo/pop_censo_2022_datario.csv` (sep `;`, latin-1) já traz
   `codbairro`, `codra`, `0 a 4 anos`. A função lê esse CSV direto — não depende de `df_censo`
   ter sido calculado numa célula anterior — e uma asserção confere que iguala `df_censo['0 a 4 anos']`.
7. **CadÚnico não é regenerável sem `.env`** (banco). A nova seção **não depende** dele; a
   regressão compara os `cadunico_*` existentes sem regerá-los.

## Ordem de execução

```
Bloco 0 (aprovação) → Bloco 1 (baseline) → Bloco 2 (nível RA) → Bloco 3 (funções) → Bloco 4 (seção Proteção)
   → Bloco 5 (estrutura_eixos.md) → Bloco 6 (HTML) ┐
                                    Bloco 7 (PDF)  ├→ Bloco 9 (textos) → Bloco 10 (docs) → Bloco 11 (validação) → Bloco 12 (deploy, gated)
                                    Bloco 8 (DOCX) ┘
```

Blocos 6, 7 e 8 dependem só do 5 e podem ser feitos em qualquer ordem. **Um commit por bloco**
(mensagens `inclusao_dados_protecao Bloco N: …`, como em `ajuste_eixos`).

## Bloco 0 — Aprovação e decisões abertas
- Usuário lê `specification.md`, `plan.md`, `tasks.md`, `validation.md`.
- Confirmar/alterar D2, D5, D6, D7, D8, D9; confirmar o que muda se os dados Tabnet extras
  (tipificação, <1/1-5, interpessoal) chegarem antes da implementação (spec §6).
- Decidir **quando** os exports Tabnet extras entram: antes do Bloco 3 (incorporados) ou rodada seguinte.

## Bloco 1 — Baseline de regressão
Antes de qualquer edição de código (saídas são gitignored, então a garantia é local):
```python
# scratch (scratchpad da sessão, não versionado)
import hashlib, pathlib, json
raiz = pathlib.Path('.')
pastas = ['tabelas_finais', 'visualizacoes', 'mapas']
base = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for d in pastas for p in raiz.joinpath(d).rglob('*') if p.is_file()}
# + relatorio/index.html, relatorio/analise_primeira_infancia.pdf, relatorio/curadoria_textos.docx
# + contagens: nº de <h2>/<h3>/cards/mapas SVG do HTML; nº de páginas do PDF; nº de headings do DOCX
json.dump(base, open('<scratchpad>/baseline_saidas.json', 'w'))
```
Também registrar tamanho do `index.html` (limite D7) e o comando/estado usado para gerar cada artefato.
Resultado vai para `validation.md` (V0).

## Bloco 2 — Nível geográfico RA (spec §3)
`analise.py` (só o dicionário + docstring):
```python
_NIVEIS_AGREGACAO = {
    'bairro': ..., 'ap': ..., 'rp': ..., 'cap': ...,      # intocados
    'ra':     {'coluna_geo': 'codra', 'tipo': int},         # NOVO
}
```
`mapa_coropletico_bairros` já faz `dissolve(by=coluna_geo)` para qualquer nível ≠ bairro: **sem
mudança de código**, só menção no docstring. Em `build_html_report.py`: `_NIVEL_COL['ra']='codra'`,
`_NIVEL_LABEL['ra']='RA'`, ramo `dissolve` em `_geo_nivel` com rótulos vindos de `regiao_adm`
(nome), `_chave_norm(v,'ra')=int(v)`. Cuidado: `_geo_nivel` hoje trata `ap`/`rp` num só `elif`
(`nomes = "AP/RP {c}"`); `ra` precisa de ramo próprio para usar o nome da RA.

Checagem: mapa de teste por RA (valor = nº de bairros) renderizado nos dois geradores; asserções
33 RAs, 32 casadas com IPS, diferença = {21}.

## Bloco 3 — Funções novas (topo de `analise.py`)
Ver spec §4. Ordem: `numeral_romano_para_int` → `carrega_violencia_territorial_ra` →
`carrega_sinan_bairro` → `carrega_violencia_familiar` → `carrega_pop_0_4_bairro` →
`taxa_por_mil` → `bairro_para_nivel`. Detalhes de implementação:

- `carrega_sinan_bairro(caminho, categoria, anos_validos)`: `pd.read_csv(caminho, sep=';',
  encoding='latin-1', skiprows=6)` (cabeçalho de metadados tem 6 linhas; validar lendo a linha
  de filtro, ex. `"Mãe: Sim"`, e devolvê-la em `df.attrs['filtro']` para conferência);
  remover linha `Total`; `Bairro Resid` → `codigo` (int) + `bairro` (`str.split(n=1)`, atenção a
  espaços múltiplos: `"1        SAUDE"`); `melt` ano; **grade** bairro × `anos_validos` com 0
  (mesmo padrão de `carrega_raca_bairro`); reindexar sobre os **166 bairros do geojson**, não só
  os que aparecem no arquivo (bairro sem caso = 0, não ausente). `anos_validos` = `range(2011, 2026)`
  para vínculos e `2018-2026` para autoprovocada (D3b).
- `carrega_violencia_familiar(pasta, anos_validos)`: 7 arquivos → longo (`vinculo`, `codbairro`,
  `bairro`, `ano`, `casos`); `outros` = padrasto + irmão(ã) + cônjuge + ex-cônjuge + filho(a),
  **mantendo também** cada vínculo original (T4). Nunca somar mãe + pai.
- `carrega_violencia_territorial_ra(caminho)`: `pd.read_excel(header=None, skiprows=...)` —
  localizar a linha de cabeçalho pelo texto "Taxa de homicídios" em vez de por posição fixa;
  `codra = numeral_romano_para_int(primeira palavra)`; linha "RIO DE JANEIRO" vai para
  `df.attrs['municipio']`; asserção de nome contra `regiao_adm` normalizado (`unicodedata` NFKD, sem dependência nova).
  Nomes com encoding: abrir com o motor padrão do Excel (o mojibake visto era só do terminal).
- `taxa_por_mil`: `casos / pop * 1000`, recalculada após `groupby().sum()` de casos e pop.
- `bairro_para_nivel`: CAP via `_RA_PARA_CAP` (já existe) sobre `codra`; RP/AP via colunas do geojson.

Sem suíte de testes no projeto: cada função ganha **asserções inline na própria célula** e um
script de verificação no scratchpad (não versionado) que reproduz os números de `validation.md` V2.

## Bloco 4 — Seção "🛡️ Proteção" em `analise.py`
Uma célula markdown de abertura (`# %% [markdown]`, mesma convenção emoji/`##` das demais) e
sub-blocos. Toda chamada cita `fonte_dados`; contagem → `bins`, taxa → contínuo; saídas seguem
`_anual`/nomes descritivos.

- **4a Violência familiar** — T1, T2, T3 (RA e CAP), T4; G1, G2, G3; M1, M2, M3.
  Séries usam `serie_temporal_multipla` (mãe, pai, outros) com anotação do salto de 2017.
  `bins` dos mapas: derivados dos quantis dos dados (2025: mãe máx 165, pai máx 132 por bairro; "outros"
  acumulado 2021-2025 tem máx bem menor) — **calibrar ao ver a distribuição**, registrando
  os limites escolhidos no `.md` (mapas anteriores usam `[15, 30, 60, 120]`, etc.).
- **4b Autoprovocada** — T5; G7 (barras: total 2018-2025 × 2026 parcial); M7 (2026). Nota de
  hipótese sobre o registro administrativo, sem afirmar causa.
- **4c Violência territorial** — T6; G4, G5, G6 (`grafico_barra`, ordenado, linha do município);
  M4, M5, M6 (`nivel='ra'`, `chave='codra'`, contínuo, `_CORES_TEMA_MAPA['protecao']`).
- **4d Taxa** — T7; M8, M9, M10 (contínuo, bairros); G8 (top taxas, opcional); rótulo D9 em título/legenda:
  "por 1.000 crianças de 0 a 4 anos (numerador inclui 5 anos)".
- Arredondamento/`NaN`: bairros com pop 0-4 = 0 ou ausente → `NaN`, não 0 nem inf.
- **Bairros com poucos habitantes** (pop 0-4 muito pequena) geram taxas instáveis: definir na
  revisão um piso (ex. suprimir/hachurar taxa quando pop < N) — decisão D10 abaixo.

**D10 (nova, do plano)**: piso de população para taxa de bairro (Grumari, Paquetá etc.). Proposta:
não suprimir, mas sinalizar em nota e listar os bairros de pop 0-4 < 100 no rodapé/tabela.

Cada célula termina imprimindo/validando totais (`assert`), como as seções existentes fazem.

## Bloco 5 — `specs/estrutura_eixos.md`
- Reescrever as subseções de 🛡️ Proteção: `status: pendente` → arquivos reais
  (`- visualização/mapa/tabela:` repetidos), `fonte` corrigida (Data.Rio/IPS, Sinan), `nota` com as
  limitações (só 2024/todas as idades; 0-5 agregado; só autoprovocada; taxa D9).
- Novas subseções 🅱 (composição de "outros", top bairros, taxas por RA/CAP) como `### ` extras.
- Itens sem dado (tipificação; recorte <1/1-5) permanecem `status: pendente`.
- **SGB/inundação**: removido da estrutura publicada (subseção sai do eixo Moradia; comentário
  `<!-- fora da V1 -->` mantém o rastro, se o parser tolerar; senão fica só no `.md` de specs).
- Rodar `parse_estrutura_eixos()` e conferir: nenhuma subseção perdida, contagens por eixo.
- **Não** regenerar o `.md` a partir do catálogo com `gera_estrutura_eixos.py` (sobrescreveria edições manuais).

## Bloco 6 — `relatorio/index.html`
- `_CMAP_TEMA['protecao']='OrRd'`; suporte `ra` (Bloco 2).
- Substituir as 5 chamadas `emite_bloco_pendente` de Proteção por blocos reais no padrão existente:
  `h3` por indicador + `option_card` (`line_chart`/`bar_chart`/`grouped_bar_chart`, `mapa_svg`,
  `plain_table`/`tabela_com_texto`), com `fonte` em todos. Itens sem dado ficam
  `emite_bloco_pendente` (tipificação; recorte <1/1-5).
- Remover o `emite_bloco_pendente` do SGB em Moradia.
- Notas metodológicas (2017, 2026, vínculos, IPS, D9) como texto de apoio no `h3`, na mesma
  posição em que os demais eixos colocam `_texto_analise`.
- Medir tamanho antes/depois (D7); se estourar, aplicar a mesma compressão dos mapas atuais
  (basemap WebP, geometrias simplificadas — ver `relatorio/specs.md`).
- Confirmar que a faixa "EM DESENVOLVIMENTO / TEMPORÁRIO" segue no lugar (não é escopo remover).

## Bloco 7 — PDF (`build_notebook_report.py`)
Mesma substituição: Proteção usa `chart_block`, `emit_map_gallery` (novo `MAP_GROUPS_PROTECAO`) e
`registra_tabela` para os PNG/CSV reais; SGB removido de Moradia; apêndice de tabelas recebe as novas.
Regerar via skill `export_pdf_report`; conferir contagem de páginas e ausência de quebra em
gráficos/mapas novos.

## Bloco 8 — DOCX de curadoria
- **Antes** de regenerar: propagar edições manuais existentes do DOCX (`sincroniza_docx.py`, passo 6 da
  skill) para não perder texto curado.
- Regenerar com `gera_docx_curadoria.py` (lê o `.md`); depois testar ida-e-volta:
  gerar → sincronizar → diff vazio nos eixos não-Proteção.
- Cada visualização/mapa novo ganha bloco de texto editável.

## Bloco 9 — Textos e notas
Redigir (pt-BR, tom não-técnico, mesmo padrão dos textos existentes) e submeter à revisão do usuário:
1. quebra de série 2017 (possível mudança de ficha/notificação — **hipótese**);
2. 2026 parcial e excluído (exceto autoprovocada, onde é a referência);
3. vínculos não excludentes / não somar;
4. IPS: Data.Rio, 2024, todas as idades, sem série;
5. contagem absoluta ≠ risco; taxa D9 com sua ressalva;
6. hipótese de mudança de registro administrativo em 2026 (autoprovocada) **a confirmar com a fonte**.

## Bloco 10 — Documentação mínima da rodada
`specs/roadmap.md` (item 5 concluído), `specs/tech-stack.md` (nível RA, OrRd, Sinan),
`relatorio/specs.md` (histórico), `.claude/skills/generate_map/SKILL.md` (`nivel='ra'`, `codra`),
`CLAUDE.md` (uma linha RA≠AP≠CAP), `CHANGELOG.md`. A revisão ampla é o roadmap item 9 (outra rodada).

## Bloco 11 — Validação final
Executar todo `validation.md`; usuário revisa o HTML no navegador (claro/escuro) e os textos.

## Bloco 12 — Publicação no GitHub Pages (gated)
Só após V-final aprovada **e "ok" explícito do usuário**:
1. Merge para a branch que o workflow publica (confirmar; principal é `staging_main`, trabalho em `planning`);
2. `workflow_dispatch` de `.github/workflows/deploy-relatorio.yml`;
3. Conferir a página publicada (Proteção completo, demais eixos idênticos, mapas SVG carregam);
4. Reversão: re-disparar o workflow no commit anterior ao merge.

## Riscos
| Risco | Mitigação |
|---|---|
| Regressão silenciosa em saídas antigas | Baseline por checksum (Bloco 1), diff só de adições |
| HTML/PDF divergirem do `.md` (não o leem) | Checklist V8 cruza `.md` × HTML × PDF × DOCX por indicador |
| Mapas de contagem enganam (bairros populosos) | Taxa T7/M8-M10 ao lado; nota "contagem ≠ risco" |
| Taxa D9 mal interpretada | Rótulo explícito em título/legenda/nota |
| Peso do HTML | Medir por bloco; corte D8 |
| `.md` sobrescrito por `gera_estrutura_eixos.py` | Não rodar; documentar no plano e nas tarefas |
| DOCX perder texto curado | Sincronizar antes de regenerar (Bloco 8) |
| Dados Tabnet extras chegarem no meio | Carregadores genéricos; novo lote = tarefas T4.x adicionais |
