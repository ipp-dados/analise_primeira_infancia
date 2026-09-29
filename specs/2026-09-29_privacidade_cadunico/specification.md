# SPECIFICATION — Privacidade do CadÚnico: agregação de bairros pequenos (rodada de 2026-09-29)

Status: **planejada em 2026-09-29** (branch `planning`); implementação em `spec/privacidade-cadunico`. O *como* está em
`plan.md`, as tarefas em `tasks.md`, os critérios de aceite em `validation.md`.

## 1. Contexto

Pedido do usuário (2026-09-29): garantir que a regra de proteção de dados (constituição §6: nenhuma contagem do
CadÚnico < 20 abaixo do município) vale nas tabelas versionadas no GitHub, **agregando** quando preciso.

Auditoria (2026-09-29, `validation.md` §Planejamento):
- **Versão atual versionada: conforme.** As 4 tabelas por bairro no git (`cadunico_por_bairro_2026`,
  `cadunico_por_bairro_ate_4_2026`, `tabela_mapa_cadunico_criancas_2026`, `tabela_mapa_cadunico_criancas_0_a_4_2026`) não
  têm contagem do CadÚnico entre 1 e 19: os bairros pequenos estão **vazios** (`suprime_celulas_pequenas`).
- **Vazamento por dedução:** o site mostra, por bairro, "% crianças negras" e "% famílias com uma adulta" (tooltip), e
  as tabelas versionadas trazem crianças e famílias por bairro. Percentual × total devolve a contagem: o grupo ou o
  complemento fica abaixo de 20 em **6 bairros** (% negras) e **14** (% uma adulta). Ex.: Leblon, 49 crianças, 35
  negras → 14 não negras.
- **Histórico do git:** o commit `cdfacd2` (2026-09-09, antes da regra de 2026-09-23) tem contagens de 1 a 19 por bairro
  em 4 arquivos (ex.: Argentino 3, Grumari 12), publicado no GitHub.

## 2. Decisões do usuário (2026-09-29)

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | Bairros abaixo do limiar **somados na sua RA** ("Demais bairros da RA X"); se o conjunto ainda ficar < 20, na **AP**; se ainda < 20, no município ("Demais bairros") | em vez de vazio: os totais fecham e o dado não some |
| D2 | Em percentual por bairro, o bairro entra no conjunto agregado também quando o **numerador ou o complemento** (denominador − numerador) é < 20 | percentual × total publicado devolve a contagem |
| D3 | Histórico do git (`cdfacd2`): **só registrar agora**; limpeza (filter-repo + force-push) decidida depois com a equipe | constituição §7: não reescrever histórico sem OK explícito |

Detalhe de implementação decidido na planificação (registrado aqui para revisão):
- **Mapas de percentual:** os bairros de um conjunto aparecem com a **taxa do conjunto** e marcados como agregados
  (tooltip do site: "Demais bairros da RA X"; nota no rodapé do PNG/A4).
- **Mapas de contagem:** os bairros do conjunto ficam **sem cor**, com a marcação "agregado em Demais bairros da RA X"
  — pintar cada um com o total do conjunto exageraria o bairro. O total do conjunto está na tabela.

## 3. Requisitos

**R1 — Função única.** `agrega_bairros_pequenos` em `primeira_infancia/cadunico.py`: recebe a tabela por bairro com
**contagens completas**, as colunas de contagem e os testes (colunas que precisam ser ≥ 20, e pares numerador/
denominador cujo complemento também precisa ser ≥ 20); devolve (a) a **tabela publicada**, com os bairros grandes e uma
linha por conjunto agregado (nome, bairros que o compõem, contagens somadas, taxas recalculadas das somas) e (b) a
**tabela do mapa**, uma linha por bairro, com `agregado_em` (nome do conjunto ou vazio) e as taxas do conjunto nos
bairros agregados. **Sobra que não chega a 20 nem no município** (achado na implementação: 9 bairros de 0 a 4 anos,
21 crianças, entre eles os 5 que o CEP dos Correios não atribui): junta-se ao menor conjunto já formado (e ao seguinte,
se precisar) num único "Demais bairros" — deixá-la vazia abriria a conta Total − publicado = sobra (< 20). Vazio só se
não houver conjunto nenhum.

**R2 — Onde aplica.** Toda saída do CadÚnico por bairro de `analise.py`: `cadunico_por_bairro_2026`,
`cadunico_por_bairro_ate_4_2026`, `tabela_mapa_cadunico_criancas_2026`, `tabela_mapa_cadunico_criancas_0_a_4_2026`,
`tabela_mapa_cadunico_recortes_bairro_2026` e os 5 mapas que saem delas. Localidades sem bairro oficial (6 nomes dos
Correios) formam o conjunto "Localidades sem bairro oficial"; se < 20, vão para "Sem bairro identificado".

**R3 — Site.** Tooltip e CSV de download dos mapas do CadÚnico mostram o conjunto agregado; nenhuma contagem < 20 e
nenhum percentual que devolva contagem < 20 (conferido por script sobre o `index.html`/`data/*.js` gerados).

**R4 — PDF e DOCX.** Tabelas do apêndice com as linhas de conjunto; nota de supressão/agregação na fonte.

**R5 — Regra escrita.** Constituição §6 e `CLAUDE.md`: agregação por RA → AP → município no lugar do vazio; regra do
numerador/complemento em percentuais; o achado do histórico (D3) no `ROADMAP.md` (backlog Repositório).

## 4. Fora do escopo

- Reescrever o histórico do git (D3).
- Outras fontes sensíveis por bairro (Sinan: notificações de violência de 0 a 3 por bairro) — a regra do usuário é do
  CadÚnico; levantado ao usuário ao fim da rodada.
- Geocodificação do CadÚnico (backlog F1).
