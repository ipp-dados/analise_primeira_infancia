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

- [ ] Tamanho de `index.html` + `data/` registrado (as metas são as de V3b).
- [ ] Um `<path id="geo-…">` por região por nível; nenhum `<path d=` dentro de `.map-svg-card`.
- [ ] Capturas dos 5 níveis iguais à baseline.
- [ ] Hover destaca a região, tooltip mostra nome + valor (inclusive "suprimido (< 20)" no CadÚnico),
  toggle de outliers troca o mapa, CSV baixa com as linhas certas — em cada nível.

## V3b: Redução de tamanho (spec §4.9)

Referência: 20,9 MB (V0). Medir depois de cada passo do Bloco 3b.

| Passo | Geometria | Atributos | Outliers | Dados | `index.html` | Site todo (bruto / gzip) |
|---|---|---|---|---|---|---|
| Depois de D2 (Bloco 3) | | | | | | |
| + simplificação (tol = ?) | | | | | | |
| + atributos | | | | | | |
| + outliers como fills | | | | | | |
| + dados por aba | | | | | | |
| **Meta** | ≤ 0,5 MB | ≤ 0,3 MB | ≤ 0,15 MB | ≤ 50 KB iniciais | ≤ 1 MB | ≤ 2 MB |

- [ ] Nenhuma fresta entre vizinhos nem ilha perdida (Paquetá, ilhas da baía) em zoom 200%, 5 níveis.
- [ ] Toggle de outliers do mapa: cores e legenda iguais às da variante "clean" da baseline.
- [ ] Link direto `#<eixo>/<h3>` numa aba ainda não carregada rola para o lugar certo.
- [ ] Gerador imprime o relatório de tamanho sem `AVISO`.

## V4: Protótipo

- [ ] Contraste AA (≥ 4,5:1) de texto sobre cada superfície nova — tabela com os valores.
- [ ] Aprovação do usuário registrada (data e ajustes pedidos).

## V5-V6: Abas, sumário, restyle

- [ ] 7 abas; cada eixo mostra os mesmos h3 e o mesmo nº de `.out` da baseline (tabela da spec §2).
- [ ] Caixa de fontes em cada um dos 6 eixos, sem repetição, com todas as fontes dos cartões do eixo.
- [ ] Nenhum emoji restante em h2, pendentes e notas metodológicas.
- [ ] Barra de abas fica em y=0 depois de rolar; banner some rolando.
- [ ] `#inclusao`, `#inclusao/<id-h3>`, `#<id-h3>` antigo e sem hash abrem no lugar certo; voltar/avançar funciona.
- [ ] Sumário lateral: item ativo acompanha a rolagem; progresso 0% no topo e 100% no fim do painel;
  clique rola e atualiza a URL.

## V7: Integração

- [ ] Workflow: `_site/` contém só `index.html`, `css/`, `js/`, `data/`, `assets/` (conferir com um dry run local
  do passo de cópia).
- [ ] `sincroniza_docx.py` regenera `website/index.html` (rodar com o DOCX atual).
- [ ] `git status` limpo de `relatorio/index.html`; `website/index.html` e `website/data/*` rastreados.

## V8: Navegadores

| Verificação | Chromium | Firefox | WebKit (proxy Safari) | `file://` |
|---|---|---|---|---|
| Carrega sem erro no console | | | | |
| Troca de aba + hash | | | | |
| Barra fixa + sumário lateral | | | | |
| Pills / outliers / CSV | | | | |
| Tooltip de mapa (5 níveis) | | | | |

Safari real não testado (sem macOS nesta máquina) — registrar aqui se alguém testar depois.

## V9: Site estático / GitHub Pages (spec §4.10)

- [ ] `_site/` (montado pelo mesmo passo do workflow) só contém `html css js svg png jpg` + `.nojekyll`; nenhum `.py`.
- [ ] Nenhum `href`/`src` absoluto (`/…`) ou `file:`; nenhum `fetch(`/`XMLHttpRequest` em `js/` e `data/`.
- [ ] Todo caminho relativo resolve para um arquivo existente com a mesma caixa (checagem exata).
- [ ] Roteiro Playwright passa com `_site/` servido num subcaminho (`/<repo>/`).
- [ ] Rotas só por hash: nenhum `history.pushState` com caminho, só com `#`.
- [ ] `404.html` existe e abre.
- [ ] Deploy real (`workflow_dispatch`, com ok do usuário): URL publicada abre, abas, mapas e CSV funcionam.
