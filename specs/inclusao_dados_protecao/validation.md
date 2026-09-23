# Validação — specs/inclusao_dados_protecao

Marcar `[x]` com a evidência (comando, número, print). Nada é publicado no Pages sem V0-V8 limpos e
"ok" do usuário (V9). Números de referência abaixo foram **verificados sobre os arquivos brutos**
nesta rodada; o código deve reproduzi-los.

## V0 — Baseline (antes de qualquer edição)
- [ ] Checksums SHA-256 de `tabelas_finais/`, `visualizacoes/`, `mapas/`, `relatorio/*` gravados.
- [ ] Contagens: `<h2>/<h3>`, cards, mapas SVG do HTML; páginas do PDF; headings do DOCX; tamanho do HTML (~17 MB).
- [ ] Anotado o que não pôde ser regerado (ex. `cadunico_*` sem `.env`).

## V1 — Nível Região Administrativa
- [ ] `limite_bairros_rio.geojson` → 33 RAs por `dissolve(codra)`, 166 bairros, sem `codra` nulo; RA 32 inexistente.
- [ ] `violencia_territorial.xlsx` → 32 RAs + linha município; casam 32 de 33; **única ausente = 21 Paquetá** (aparece "Sem dado").
- [ ] Numeral romano → `codra` bate com `regiao_adm` normalizado (sem acento/caixa) nas 32 RAs (`SANTA TERESA`≈`SANTA TEREZA` tratado explicitamente e registrado).
- [ ] Município: taxa de homicídios 16,663…, ação policial 5,780…, jovens negros 3,526… (linha "RIO DE JANEIRO").
- [ ] Mapa de teste por RA nítido em `analise.py` e no HTML; rótulo do tooltip = nome da RA.
- [ ] Mapas de `bairro`, `ap`, `rp`, `cap` idênticos ao baseline.

## V2 — Carregadores (números de referência)
Sinan, formato bruto → tabela final:
- [ ] Todo arquivo: linha `Total` removida; nenhuma linha com `codigo` nulo; 6 linhas de metadados lidas (filtro conferido: "Mãe: Sim", "Pai: Sim", …, "Lesão Autoprovocada: Sim").
- [ ] Grade completa: `166 bairros × anos`, zeros onde não havia linha (colunas de ano esparsas — ex. cônjuge só tem 2018-2021 e 2025 no bruto).
- [ ] Soma da grade = linha `Total` do bruto, por ano. Mãe: 324, 464, 429, 564, 452, 600, **1514** (2017), 1265, 868, 734, 805, 1359, 1469, 1515, **1756** (2025), 948 (2026) — total 15.066.
- [ ] Pai 2025 = 1404; padrasto 2025 = 73; irmão(ã) 2025 = 26; cônjuge 2025 = 5; ex-cônjuge 2025 = 3; filho(a) 2025 = 3.
- [ ] `outros` 2025 = 73 + 26 + 5 + 3 + 3 = **110**; `outros` = soma exata dos cinco componentes em todos os anos (T4 fecha com T1).
- [ ] Mãe e pai **nunca** somados em nenhuma tabela.
- [ ] Bairros com caso em 2025: mãe 131, pai 129 (dos 153/155 que aparecem no bruto).
- [ ] Autoprovocada: 40 casos no total; 2018 = 1, 2022 = 2, 2024 = 2, 2025 = 2, 2026 = 33; antes de 2026 = 7; 24 bairros com dado.
- [ ] Todos os `codigo` do Sinan existem em `codbairro` do geojson (0 sem correspondência, 10 bairros do geojson sem nenhum caso — esperado).
- [ ] Denominador: `pop_censo_2022_datario.csv` lido com sep `;`/latin-1; `0 a 4 anos` bate com `df_censo['0 a 4 anos']` em todos os bairros.

## V3 — Saídas de `analise.py`
- [ ] Existem: T1-T7 (T3 = RA e CAP), G1-G8, M1-M10 conforme spec §5 (menos os cortados em D8, já refletidos em todos os artefatos).
- [ ] Nomes seguem convenção (`_anual`, descritivos), tabelas em `tabelas_finais/`, PNG em `visualizacoes/`/`mapas/`, gêmeas `tabela_mapa_*.csv` geradas.
- [ ] Toda visualização/mapa cita `fonte_dados` (Sinan/Tabnet SMS-Rio; Data.Rio/IPS 2024; Censo 2022 para a taxa).
- [ ] Convenção: contagens (M1-M3, M7) com `bins` discretos; taxas (M4-M6, M8-M10) com colorbar contínua.
- [ ] Taxa: recalculada após somar casos e população; conferida à mão em 3 bairros (um grande, um pequeno, um zero) e em 1 RA e 1 CAP (Σcasos/Σpop, não média de taxas).
- [ ] Bairros sem população/sem caso: `NaN`/0 conforme desenho, nunca `inf`; D10: bairros de pop 0-4 < 100 listados.
- [ ] Séries até 2025 (2026 fora), exceto autoprovocada (G7/M7 usam 2026 rotulado como parcial).
- [ ] G1 mostra a anotação de possível quebra em 2017; nenhum gráfico sugere um "total" de violência familiar.
- [ ] `analise.py` roda de ponta a ponta (exceto CadÚnico sem `.env`, como no baseline) sem erro; `jupytext --to notebook` ok.

## V4 — `relatorio/index.html`
- [ ] Eixo Proteção: 5 itens do catálogo tratados (territorial, familiar, notificações, taxa com conteúdo; tipificação `pendente`); <1/1-5 sinalizado pendente onde aplicável.
- [ ] Mapas SVG novos (incl. os 3 por RA) carregam, tooltip com nome, legenda/escala corretas, tema `OrRd`.
- [ ] Claro e escuro conferidos; sem overflow em largura de celular (~375 px).
- [ ] Notas metodológicas visíveis (2017, 2026, vínculos, IPS, D9); hipóteses rotuladas como hipótese.
- [ ] SGB **ausente** de Moradia e de qualquer outro lugar; faixa "EM DESENVOLVIMENTO" preservada.
- [ ] Tamanho: baseline + ≤ 2,5 MB (D7), ou justificativa aprovada.
- [ ] Sem erro de console no navegador.

## V5 — PDF
- [ ] Proteção com gráficos/mapas/tabelas reais; itens pendentes marcados; SGB ausente.
- [ ] Nenhum gráfico/mapa cortado ou sobreposto; páginas = baseline + acréscimo esperado.
- [ ] Apêndice de tabelas inclui as novas.

## V6 — DOCX
- [ ] Todo item novo do `.md` tem heading + espaço de texto; SGB ausente.
- [ ] Ida-e-volta (gerar → sincronizar): eixos não-Proteção sem diferença; texto curado anterior preservado.

## V7 — Regressão global
- [ ] Todos os checksums de V0 idênticos, exceto arquivos novos e artefatos regerados de propósito (HTML/PDF/DOCX).
- [ ] Nos regerados: seções/cards/mapas dos eixos Prioridade, Inclusão, Família, Alimentação, Moradia idênticos (menos a remoção do SGB).
- [ ] `git diff` de `analise.py` contém **só linhas adicionadas**, mais as chaves novas de dicionário e menção no docstring (nenhuma linha antiga removida/alterada).
- [ ] `git status` limpo de arquivos indevidos; `.env`/dados sensíveis não versionados.

## V8 — Consistência entre os 4 artefatos
- [ ] Para cada subseção de Proteção em `estrutura_eixos.md`: presente em HTML, PDF e DOCX com os mesmos arquivos/valores/notas.
- [ ] Valores-chave idênticos nos quatro (ex.: mãe 2025 = 1756; taxa municipal de homicídios = 16,66).
- [ ] Documentação mínima (Bloco 10) atualizada e coerente com o código.

## V9 — Publicação no GitHub Pages (gate)
Pré-requisitos: V0-V8 marcados **e "ok" explícito do usuário**.
- [ ] Merge na branch de deploy conforme T0.4.
- [ ] `workflow_dispatch` concluído com sucesso.
- [ ] Página pública: Proteção completo, demais eixos idênticos, mapas SVG carregam, tema claro/escuro.
- [ ] Commit anterior anotado para reversão.

## Resultado final
_(a preencher ao fechar a rodada: data, commit, o que passou, desvios aceitos, itens levados para a próxima spec.)_
