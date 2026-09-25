# Validação — `specs/2026-09-25_website_graficos`

Escrita **antes** da implementação (pedido do usuário, 2026-09-25). Cada item diz como se verifica; preencher
resultado e data ao fim de cada bloco. Nada conta como validado só porque o gerador rodou sem erro.

Resultados de 2026-09-25. Scripts de conferência (Playwright/regex) ficaram no scratchpad da sessão; o que cada um
mede está descrito no item.

## Base (vale para todos os blocos)

- [x] V0.1 `python website/build/build_site.py` roda sem erro e **sem linha `AVISO`** (orçamento: `index.html`
      ≤ 1 MB, site ≤ 2 MB) — index 0,77 MB, site 1,35 MB (antes 0,76/1,47 MB)
- [x] V0.2 Duas execuções seguidas dão o mesmo md5 de `index.html` e `data/*` (determinismo)
- [x] V0.3 `index.html` aberto por `file://` e por `http.server` imitando o Pages (skill `build_website`, passo 2):
      sem erro no console, todas as abas renderizam — Chromium, Firefox e WebKit
- [x] V0.4 Regras de site estático (`website/README.md`): só html/css/js/svg/png/jpg, caminhos relativos em
      minúsculas, rotas só por hash, sem `fetch` — nenhum arquivo novo publicado; JS novo sem `fetch`
- [x] V0.5 Nenhum texto curado some sem registro: 59 sementes publicadas antes, 56 depois; saíram
      `cobertura_vacinal_epi_comparativo_anos` (E7), `mapa_obitos_gravidez_bairro_2025` e
      `mapa_obitos_puerperio_bairro_2025` (E4)

## A. Exclusões

- [x] VA.1 (E2) Nenhum gráfico/pill/tabela de **1 a 4 anos** mostra 1.2.1, 1.2.2 ou 1.2.3 — pill → id do gráfico →
      chamada em `data/charts.js`: 4 falhas antes, 0 depois; menores de 1 e de 5 anos mantêm Gestação/Parto/Recém-nascido
- [x] VA.2 (E3) Nenhum gráfico mostra o subgrupo 1.1 — "imuniza" em `data/charts.js` = 0 (a única ocorrência no
      `index.html` é "imunizantes", no texto curado da cobertura vacinal)
- [x] VA.3 (E4) Mapas `mapa_obitos_gravidez_bairro_2025` e `mapa_obitos_puerperio_bairro_2025` ausentes; as
      séries municipais de gravidez/puerpério continuam
- [x] VA.4 (E5) Séries de raça com 5 linhas (Branca, Parda, Preta, Amarela e indígena, Não informada); a taxa de
      "Amarela e indígena" confere com Σóbitos/Σnascidos em 2016, 2020 e 2024 (2024: 0,54 por 100 = 5,4‰; a soma
      de percentuais daria 0,70). Depois do Bloco 8 a taxa é por mil (ver VB.1)
- [x] VA.5 (E6) Sem mapa de taxa de violência por bairro; mapas de taxa por RA e de contagem por bairro presentes
- [x] VA.6 (E7, E8) Sem "Comparativo por ano" da vacina; sem frequência absoluta por raça/cor e por sexo; total e
      taxas de frequência presentes
- [x] VA.7 Mantidos: lesão autoprovocada, % de evitáveis por CAP 1-4 anos, séries por faixa, taxas neonatais por
      bairro — todos presentes

## E9. Alternância Taxa ↔ Óbitos

- [x] V9.1 Os mapas de mortalidade por bairro (neonatal precoce/tardia/pós-neonatal/total e raça/total) estão em
      **um** cartão cada, com o controle "Taxa | Óbitos"; abre em **Taxa**
- [x] V9.2 Trocar o modo mantém a pill (Taxa · Tardia → Óbitos · Tardia; Pós-neonatal idem) e troca o texto junto
- [x] V9.3 Teclado: Tab chega ao controle, Enter/Espaço troca, foco visível; `aria-pressed` correto
- [x] V9.4 Tooltip, legenda, download de CSV e botão de outliers funcionam nos dois modos
- [x] V9.5 Textos curados dos mapas de contagem (`mapa_obitos_neonatal_precoce_bairro_2025`,
      `mapa_obitos_raca_total_bairro_2025`) continuam publicados (modo Óbitos)

## B. Melhoria dos gráficos (cada item só depois da decisão P* correspondente)

- [x] VB.1 (B1) Todo gráfico de linha/barra agrupada tem título de unidade no eixo (0 sem `yLabel`); as 9 barras
      horizontais têm a unidade no subtítulo; nenhum rótulo de série cru. Taxas por mil com `‰` (0 com `%`)
- [x] VB.2 (B2) Todo mapa contínuo por bairro usa teto P95; o topo da legenda diz "≥ X" quando algum bairro passa do
      teto; tooltip mostra o valor real (inalterado)
- [x] VB.3 (B3) Barras agrupadas com valor na ponta quando ≤ 12 barras; rótulo direto de linha só até 4 séries,
      máximo/mínimo só até 2
- [x] VB.4 (B4) Pequenos múltiplos: um painel por série, mesma escala, demais séries em cinza; "Linhas" volta à
      visão original (vacinas, CAP × ano, subgrupos)
- [x] VB.5 (B5) Validador: antes FAIL em claridade (c4), croma (c1) e daltonismo (c2↔c3, ΔE 3,4 protan); depois sem
      FAIL, um WARN c5↔c6 ΔE 8,0 (limite; há legenda e rótulo direto). Troca registrada em `css/main.css` e em
      `relatorio/specs.md` (v9)
- [x] VB.6 (B6) Toda caixa "Fontes desta seção" traz a referência ABNT da entrada de `fontes.bib`; o gerador avisa
      fonte sem entrada — nenhuma hoje
- [x] VB.7 (B7) Nenhum gráfico de categorias com linha "Total"/"Subtotal" desenhada como categoria
- [x] VB.8 (B8) P1: taxas com base zero, marcas redondas (o eixo do baixo peso ao nascer mostrava "9, 9, 10, 10")

## Textos do relatório

- [x] VT.1 Com `achados_protecao`/`sintese_protecao` preenchidos (teste, JSON restaurado depois), o site mostra as
      duas frases na caixa "Principais achados" e a síntese em "Conclusões"; sem eles, o placeholder de hoje

## Navegador

- [x] VN.1 Chromium (canal Chrome), Firefox e WebKit via Playwright, por `file://` e por `http.server` imitando o
      Pages: troca de aba + hash, âncoras antigas (`#prioridade/mapas-2`, `#mapas-3`, `#sisvan`,
      `#prioridade-sem-secundário`), pills, alternância, tooltip de mapa em bairro/AP/RP/RA/CAP; nenhum botão sobre
      legenda/eixo/título (4 casos antes, 0 depois)
- [x] VN.2 Capturas antes × depois no scratchpad da sessão (não versionadas: PNG é ignorado no git fora de
      `website/assets/`)
