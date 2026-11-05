# PLAN — Versão final do site e do relatório (2026-11-05)

Ordem pensada para regerar cada produto o mínimo de vezes e deixar a publicação por último.

## B3 — Banner e rodapé (R1, R3)
- Baixar a foto do Unsplash (página `wccs6fKUtok`, licença e autor conferidos na página) para
  `website/assets/images/banner-*.{webp,jpg}` em 3 larguras; `website/build/` ganha o passo de redimensionar (Pillow).
- `build_site.py`: `<header class="site-banner">` com a foto de fundo (`<picture>`), camada escura, crédito; CSS em
  `css/layout.css` (desktop) e `css/mobile.css` (celular). Conferir contraste e o orçamento de tamanho.
- Rodapé: conferir cada link (status HTTP) e o texto da coluna da esquerda.

## B4 — Mapa de referência (R2)
- `build_site.py`: função `mapa_referencia_svg()` reaproveitando `_geo_base_bairros()`, `_bounds_project` e o fundo
  cartográfico; camadas `bairro`, `ra`, `ap` como grupos SVG; botões de camada de nomes em `js/charts.js` (mesmo padrão
  das pills); tabela bairro → RA → AP para download.
- PDF: figura A4 estática gerada por um helper novo em `primeira_infancia/mapas.py` (contornos, sem dado), chamada no
  `analise.py` (seção Censo, junto dos mapas de bairro/AP/RP) e citada no capítulo de Introdução.

## B5 — PDF: capítulos em `.tex`, capa e folha de rosto (R5)
1. Gerar o PDF como hoje e guardar a página de referência (PNG das páginas) para comparar.
2. `gera_latex.py --exportar-capitulos`: escreve `relatorio/latex/capitulos/00_introducao.tex` … `08_consideracoes.tex`
   a partir de `gerado/capitulos.tex`, um arquivo por `\chapter`, com cabeçalho de comentário (o que é, como editar).
3. `relatorio.tex` → `\input{capitulos/...}`; `gera_latex.py` deixa de escrever `capitulos.tex` e de ler o JSON de
   textos; continua com figuras, apêndices, resumo, aviso, nocite; checagem: todo `\ref`/`\figura` dos capítulos existe.
4. Comparar o PDF novo com o de referência (mesmo número de páginas e mesmo conteúdo, exceto capa e folha de rosto).
5. Nova `pretextual/capa.tex` e `folha_rosto.tex` (ABNT, identidade IPP); conferir no PNG.

## B6 — Curadoria só do site, sem DOCX (R6)
- Tag `rodada/curadoria_docx` no commit atual; apagar os 4 scripts DOCX; `confere_textos.py` sem DOCX (site × JSON);
  atualizar skill `export_pdf_report` (sai a parte de DOCX; entra "editar os `.tex` de capítulo"), `CLAUDE.md`,
  `docs/especificacao_projeto.md`, `relatorio/` README/notas.

## B7 — Release e Actions (R7, R8)
- `winget install GitHub.cli`; o usuário roda `gh auth login` (`! gh auth login`).
- `relatorio/latex/build/publica_release.py` (ou passo documentado): gera o PDF com `--publicar`, cria tag e Release com
  o PDF e as notas; só roda com confirmação.
- Workflow: `deploy-relatorio.yml` com `on: push: branches: [main]` + `workflow_dispatch`; versões das ações
  atualizadas; novo `confere-site.yml` em PR/push para `staging_main` (checagens de R8, sem gerar nada).

## B8 — Versão final, revisão e teste (R4, R10)
- `publicacao.json` → `false`; regerar site e PDF; conferir que não há dado pontual.
- Revisão de pipelines e documentação (lista de R10); títulos "0 a 5 anos" → "até 72 meses" onde couber.
- Teste completo com Playwright (Edge), desktop 1366 e celular 390: todas as abas, troca de pills, mapas, downloads de
  CSV, links do rodapé e do banner, sem erro de console, sem rolagem horizontal; capturas para o usuário conferir.

## B9 — Publicação (R9) — só com OK explícito do usuário
- Merge `spec/versao_final_site` → `staging_main` (`--no-ff`); tag `rodada/versao_final_site`.
- Merge `staging_main` → `main`; o push na `main` dispara o deploy; conferir o site no ar.
- Release do PDF (B7).
- Constituição §7 e `CLAUDE.md`: `main` = site publicado, `staging_main` = teste, `demo` congelada.
