# PLAN — Versão de demonstração (branch `demo`)

## 1. Levantamento do código (2026-09-29, `staging_main` em `2fccc07`)

- **Lorem no site** (`website/build/build_site.py`): `_lorem` e `_lorem_bullets` (l. ~505/553) são chamados por
  `_texto_analise`/`_texto_seed` (textos de figura, com a precedência do texto curado), por `INTRO_HTML` (l. ~1270),
  pelos achados, pela abertura e pela síntese de cada eixo (l. ~2275-2295, chaves `achados_<eixo>`,
  `introducao_<eixo>`, `sintese_<eixo>`/`conclusao-<sid>`). São 16 pontos de chamada. O HTML atual tem lorem em
  todas as 8 abas.
- **Pendentes no site**: `emite_bloco_pendente(titulo)` (l. ~691) grava o `h3` + `callout callout-pending` e conta
  em `_PENDENTES_SECAO` (cartões da Visão geral, "N pendentes"). São 9 chamadas: 1 em Prioridade, 3 em Inclusão,
  2 em Proteção e 3 em Moradia.
- **Faixa**: string em `build_site.py` (l. ~2351), ligada por `em_desenvolvimento` em `relatorio/publicacao.json`.
  O estilo está em `website/css/layout.css` (`.dev-banner`) e em `css/mobile.css` (l. 98).
- **Link do PDF**: `URL_PDF` fixo em `staging_main` (l. ~2212).
- **PDF**: `relatorio/latex/build/gera_latex.py` → `compila(publicar)` copia `_build/relatorio.pdf` para
  `relatorio/analise_primeira_infancia.pdf`. Hoje tem 161 páginas. A página impressa 18 é a 19ª do arquivo, com o
  "Mapa 1". A marca d'água vem de `gerado/aviso.tex`.
- **Deploy**: `.github/workflows/deploy-relatorio.yml`, com `workflow_dispatch` e o ambiente `github-pages`. A
  branch que pode publicar é definida na regra do ambiente (Settings → Environments → github-pages → Deployment
  branches). O `gh` não está instalado aqui.
- **Leitores de `textos_curados.json`**: site, `gera_latex.py`, `relatorio/curadoria/*` (DOCX, sincronização,
  validação) e `apresentacao/build`. Nenhum deles lê `website/build/textos_demo.json`, porque o arquivo é novo.

## 2. Blocos

### B0 — Planejamento (branch `spec/demo`)
Os quatro documentos, a regra na constituição (§7) e a entrada no `ROADMAP.md`. Merge em `staging_main` (só
documentação, sem código da demonstração). Depois, a branch `demo` sai de `staging_main`.

### B1 — Chave e módulo do site (`demo`)
- `relatorio/publicacao.json` (na `demo`): `"demo": true`, `"lancamento_v1": "2026-10-06"` e os textos da faixa/aviso.
- `website/build/demo.py`: `ATIVO` (lido do JSON), `texto_demo(chave)` (lê `textos_demo.json`; falta de chave →
  erro com a lista das chaves que faltam), `banner_html()`, `URL_PDF_DEMO` e `confere_html(html)` (sem lorem, sem
  `callout-pending`).
- Ganchos em `build_site.py` (poucas linhas, cada uma com `if demo.ATIVO`):
  1. `_lorem`/`_lorem_bullets` → `demo.texto_demo(seed)` (curado continua na frente, porque a troca é dentro do
     fallback);
  2. `emite_bloco_pendente` → retorna sem emitir nem contar;
  3. faixa → `demo.banner_html()`;
  4. `URL_PDF` → `demo.URL_PDF_DEMO`;
  5. fim do build → `demo.confere_html(index_html)`.
- CSS: `.dev-banner.demo` em `layout.css` (fonte ~1rem, padding 16px, 2 linhas: aviso + data em destaque) e a regra
  equivalente em `mobile.css`. A regra existente de `.dev-banner` não muda.

### B2 — Textos provisórios (`demo`)
- Script auxiliar (`website/build/demo.py --lista-chaves`) que roda o build em modo de coleta e lista toda chave que
  cairia em lorem, com o título, a fonte e o caminho da tabela de cada figura.
- O Claude escreve `website/build/textos_demo.json` a partir dos números reais de `tabelas_finais/` (regras D6), eixo
  por eixo. Conferência: nenhuma frase com número que não esteja na tabela, e nenhum juízo ("preocupante",
  "melhorou muito"...).

### B3 — PDF de demonstração (`demo`)
- `relatorio/latex/build/demo_pdf.py`, chamado por `gera_latex.py` só quando `demo` é `true` e depois de `compila`:
  1. localiza a página de corte (legenda "Mapa 1 –" **e** cabeçalho com o número 18; se divergirem, erro);
  2. compila `relatorio/latex/demo_aviso.tex` (1 página, `estilo.sty`, marca d'água; texto de D11 lido do JSON);
  3. monta com PyMuPDF as páginas 1..corte + o aviso, remove links e marcadores para páginas cortadas e grava em
     `_build/relatorio_demo.pdf`;
  4. com `--publicar`, esse arquivo, e não o completo, vai para `relatorio/analise_primeira_infancia.pdf`.
- O texto provisório não entra aqui, porque `gera_latex.py` só lê `textos_curados.json`.

### B4 — Deploy (`demo`)
- No workflow da `demo`, um passo "Confere demonstração": falha com lorem (lista de palavras do gerador) ou
  `callout-pending` em `_site/index.html`.
- Passo manual (usuário/administrador): em Settings → Environments → github-pages, a regra de branches fica só com
  `demo`. Depois, o workflow é disparado a partir da `demo`.

### B5 — Geração, conferência e registro
- `build_site.py`, `gera_latex.py --publicar`, screenshots (desktop, tablet e telefone, com Edge), `confere_textos.py`.
- Conferência de R4 (`git diff staging_main -- relatorio/textos_curados.json relatorio/*.docx relatorio/controle_revisao.json`
  vazio).
- `validation.md` preenchido. `ROADMAP.md` e `CHANGELOG.md` atualizados na `demo` (a entrada da rodada em
  `staging_main` já veio no B0).

## 3. Riscos

- **Conflito no merge `staging_main` → `demo`**: os ganchos ficam em poucas linhas, e o grosso está nos módulos
  próprios. Um texto curado novo na `staging_main` passa na frente do provisório sem conflito. Uma chave nova de
  figura faz o build da `demo` parar (D5), o que é de propósito: é a hora de escrever o texto provisório dela.
- **Merge acidental `demo` → `staging_main`**: levaria a chave `demo: true` e os textos provisórios. Mitigação: a
  regra na constituição e o `demo.py`, que só existe na `demo`. Se `publicacao.json` com `demo` chegar à
  `staging_main` sem o módulo, o build falha com uma mensagem clara.
- **Corte do PDF anda** se o pré-textual crescer: o corte por conteúdo com a conferência dupla (D1) para o build em
  vez de cortar errado.
- **Sumário aponta para páginas que não existem**: é aceito (D2). Os links são removidos, e a página de aviso explica.
- **Tamanho da faixa no celular**: pode empurrar o conteúdo. Conferir no telefone (360 px) que a faixa ocupa no
  máximo 3 linhas.
- **Texto provisório lido como análise oficial**: a faixa diz que os textos são provisórios, e D6 proíbe juízo.
