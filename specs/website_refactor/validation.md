# Validação: specs/website_refactor

Marcar `[x]` com a evidência (comando, número, captura). Capturas e checksums ficam no scratchpad da
sessão; aqui só o resumo.

## V0: Baseline (antes do Bloco 1)

- [x] Levantamento (2026-09-24): `relatorio/index.html` 20,9 MB; 7.171 `<path>` de mapa = 20,1 MB (96%);
  base64 0,13 MB; render calls 0,11 MB; 6 h2 / 36 h3 / 44 `.option-card` / 100 `.out` / 8 blocos pendentes.
- [x] md5 do versionado `77cd7ed1…`; regerado hoje `21d94030…` — diferença só no JPEG do fundo cartográfico (baixado de novo a cada execução). Comparações seguintes mascaram `base64,…`. `print`: 20.917.880 chars, 97 charts, 6 h2 / 36 h3.
- [x] DOM renderizado (`--dump-dom`, Chrome headless, 21,7 MB, 156 `<svg>`) e captura 1440×2400 do topo guardados no scratchpad. Capturas por componente: feitas por bloco, isolando o cartão com CSS injetado numa cópia da página.

## V1: Gerador movido

- [x] `build_site.py out.html` rodado de outra pasta: md5 mascarado `4689bcd2…` = baseline.
- [x] `build_notebook_report.py`, `gera_docx_curadoria.py`: `git diff` vazio.

## V2: Arquivos separados

- [x] Markup de `.doc` idêntico à baseline (20.632.907 chars), só com o `src` do logo normalizado; `js/charts.js` = antigo `ENGINE` e `data/charts.js` = antigo `RENDER_CALLS`, byte a byte.
- [x] Estilos computados + caixas (sonda injetada, Chrome headless 1440px, 17.644 elementos fora de `<svg>`): **0 diferenças** com o `<!doctype>` removido — a divisão do CSS em 3 arquivos preserva a cascata.
- [x] Com o `<!doctype>` (modo padrão; antes a página rodava em *quirks mode*): única mudança é `line-height` herdado em `<table>` (quirks não herda fonte em tabela) → tabelas um pouco mais altas, +124 px na página inteira; larguras 0 diferenças. Intencional.
- [ ] Zero erro no console (verificar com Playwright, Bloco 8).

## V3: Geometria compartilhada

- [x] Tamanho registrado (V3b).
- [x] 230 `<path id>` em `<defs>` (bairro 166, AP 5, RP 16, RA 33, CAP 10 — só níveis usados); 0 `<path d=` de região dentro dos cartões; 7.107 `<use>`, 0 `href` sem alvo.
- [x] Captura do 1º mapa de cada nível (cartão isolado, 820×760): 1 a 24 pixels com diferença > 40/255 por mapa (0,00%) — bordas simplificadas. Inspeção visual a 1× e 2×: sem fresta, sem ilha perdida.
- [x] Sonda funcional (Chrome headless): tooltip mostra nome + valor nos 5 níveis; toggle de outliers de mapa troca os painéis e a variante limpa resolve a geometria; 0 erros de JS. CSV: `data-csv` gerado em Python, igual à baseline. Hover visual e "suprimido (< 20)": conferir no roteiro Playwright (Bloco 8).

## V3b: Redução de tamanho (spec §4.9)

Referência: 20,9 MB (V0). Medir depois de cada passo do Bloco 3b.

| Passo | Geometria | Atributos | Outliers | Dados | `index.html` | Site todo (bruto / gzip) |
|---|---|---|---|---|---|---|
| Depois de D2 (Bloco 3, sem simplificar) | 1,35 MB | ~0,5 MB | ~0,5 MB | 109 KB | ~2,4 MB | ~3,9 MB |
| + simplificação (tol = 0,3) + atributos + ids curtos | 0,25 MB | 0,44 MB | 0,21 MB | 109 KB | 0,87 MB | **1,33 MB / 0,31 MB** |
| + outliers como fills | não feito (spec §4.9) | | | | | |
| + dados por aba | não feito (spec §4.9) | | | | | |
| **Meta** | ≤ 0,5 MB | ≤ 0,3 MB | ≤ 0,15 MB | ≤ 50 KB iniciais | ≤ 1 MB | ≤ 2 MB |

- [x] Nenhuma fresta entre vizinhos nem ilha perdida: 0 anéis perdidos nos 5 níveis (contagem), área −0,01%, capturas em 1× e 2×.
- [x] Toggle de outliers do mapa: mesma estrutura de 2 painéis da baseline (T3b.3 não feito).
- [~] Não se aplica (dados por aba não feito).
- [x] Gerador imprime o relatório de tamanho sem `AVISO`; duas execuções seguidas dão md5 idêntico (`index.html`, `data/*.js`).

## V4: Protótipo

- [x] Contraste AA (≥ 4,5:1), WCAG 2.x:

  | Texto | Fundo | Razão |
  |---|---|---|
  | `--ink` #16202A | surface / page | 16,5 / 15,1 |
  | `--ink-2` #3F4B57 | surface / page / surface-3 | 8,9 / 8,2 / 7,7 |
  | `--ink-3` #5B6773 | surface / page / surface-2 / surface-3 | 5,8 / 5,3 / 5,4 / 5,0 |
  | `--accent` #0A5A99 | surface / page / accent-soft | 7,2 / 6,6 / 6,2 |
  | `--accent-ink` #073F6C | accent-soft | 9,4 |
  | `--warn` #8A4B06 | warn-soft | 6,2 |
  | branco | ipp-navy / accent | 9,2 / 7,2 |
  | *antes:* `--ink-3` #949B99 / acento #2E9678 | branco | *2,8 / 3,7 — falhavam* |
- [x] Comportamento no protótipo (Chrome via DevTools Protocol, 1440×900, reduced motion): barra de abas em y=0 depois de rolar; `--nav-h` medido (59 px); clique na aba muda o hash; sumário acompanha a rolagem (37% → 100%, subseção certa ativa); clique no sumário leva o h3 a 20 px abaixo da barra e grava `#<painel>/<h3>`; 0 erros no console. Achado e corrigido: na Visão geral o sumário marcava "Moradia" (links para painéis ocultos entravam no scroll-spy); e o salto nativo do navegador para `#<painel>` deixava o topo sob a barra (`scroll-margin-top` no painel).
- [ ] Aprovação do usuário registrada (data e ajustes pedidos).

## V5-V6: Abas, sumário, restyle

- [x] 7 abas; por eixo, h3 (sem contar "Conclusões"), `.out`, mapas, pills, CSV, outlier-cards e blocos de texto **idênticos à baseline** nos 6 eixos (contagem sobre o HTML gerado).
- [x] Caixa de fontes nos 5 eixos com cartões (Prioridade 5, Inclusão 5, Família 7, Proteção 6, Alimentação 2 fontes); Moradia não tem cartão de dado, então não tem caixa. Fontes quase iguais aparecem separadas (spec §4.5).
- [x] Nenhum emoji no texto de `<main>` nem nas abas (regex de faixas de emoji sobre `innerText`). A faixa "EM DESENVOLVIMENTO" mantém ⚠️ de propósito.
- [x] Barra de abas em y=0 depois de rolar; banner some rolando (Chrome, DevTools Protocol).
- [x] `#inclusão` (topo do painel a 83 px, sob a barra de 59), `#família-e-cuidados/cadúnico` e `#violência-territorial-…` antigo (h3 a 79 px), `#introducao` → Visão geral, hash inexistente → Visão geral, sem hash → Visão geral; voltar/avançar entre abas funciona.
- [x] Sumário lateral: item ativo acompanha a rolagem (terço superior da área visível); 0% no topo, 100% no fim com "Conclusões" ativo; clique rola e grava `#<painel>/<h3>`.

- [x] Título em 2 linhas (altura do h1 / line-height = 2); logo carrega a cópia de 40 px exibida a 40 px; 0 erros de console.
- [x] Mapas AP/RP/RA sem furinhos (captura do mapa AP) depois de `_fecha_frestas`.

## V7: Integração

- [x] Dry run local dos passos do workflow: `_site/` com 34 arquivos, 1,5 MB, só tipos permitidos; teste negativo (um `.py` plantado) detectado pela checagem.
- [x] `sincroniza_docx.regenera_html()` regenera `website/index.html` com md5 idêntico ao build direto (só a função de regeneração; a sincronização completa mexe em `analise.py` e não foi rodada).
- [x] `relatorio/index.html` removido do git (`git rm`), exceção do `.gitignore` retirada; `git check-ignore` não ignora nada em `website/` (index, 404, .nojekyll, data, assets).

## V8: Navegadores

Playwright, 1440×900, `reduced_motion`; site servido por `python -m http.server` em
`/analise_primeira_infancia/` (imita o Pages) e também aberto por `file://`. Build final (md5 `5732d55f…`).

| Verificação | Chromium (Chrome 153) | Firefox 155 | WebKit 26.6 (proxy Safari) | `file://` (3 motores) |
|---|---|---|---|---|
| Carrega sem erro no console | ✅ 0 erros | ✅ 0 | ✅ 0 | ✅ |
| Abre na Visão geral; clique na aba muda painel e hash | ✅ | ✅ | ✅ | ✅ |
| Barra de abas em y=0 depois de rolar; sumário com item ativo e % | ✅ | ✅ | ✅ | — |
| Rota profunda `#família-e-cuidados/cadúnico` (h3 a 79 px) e âncora antiga | ✅ | ✅ | ✅ | — |
| Voltar/avançar; seta → na barra de abas | ✅ | ✅ | ✅ | — |
| Pills / outliers / download CSV (34 linhas, `;`) | ✅ | ✅ | ✅ | — |
| Tooltip de mapa nos 5 níveis (bairro, AP, RP, RA, CAP) | ✅ | ✅ | ✅ | ✅ mapa resolve `<use>` |
| 97 gráficos renderizados | ✅ | ✅ | ✅ | ✅ |
| `404.html` com CSS (base no subcaminho) | ✅ | ✅ | ✅ | — |

Safari real não testado (sem macOS nesta máquina) — registrar aqui se alguém testar depois.

## V9: Site estático / GitHub Pages (spec §4.10)

- [x] Cópia montada com os mesmos comandos do workflow: 35 arquivos, só `html css js svg png jpg` + `.nojekyll`; nenhum `.py`/`.md`.
- [x] Nenhum `href`/`src`/`url()` absoluto ou `file:`; nenhum `fetch(`/`XMLHttpRequest`; domínios externos só os esperados (Google Fonts, GitHub, IPP, Transparência Rio).
- [x] 23 referências locais resolvem com a **mesma caixa** (checagem por `os.listdir`, não pelo sistema de arquivos do Windows).
- [x] Roteiro Playwright passa com o site num subcaminho (V8).
- [x] Rotas só por hash (`pushState` só com `#`).
- [x] `404.html` existe, abre e carrega o CSS a partir da raiz do site.
- [ ] Deploy real (`workflow_dispatch`) — **aguarda ok do usuário** (publicação externa).
