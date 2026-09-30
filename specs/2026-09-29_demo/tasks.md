# TASKS — Versão de demonstração (branch `demo`)

Legenda: [x] feito · [ ] a fazer

## B0 — Planejamento (branch `spec/demo`, 2026-09-29)
- [x] P1 Pedido do usuário; levantamento de lorem, pendentes, faixa, link do PDF, corte do PDF e deploy
- [x] P2 Perguntas agrupadas ao usuário → D1 (página impressa 18), D2 (sumário completo), D3 (faixa só na `demo`),
      D4 (Pages só da `demo`)
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`; regra na constituição (§7); `ROADMAP.md`
- [ ] P4 OK do usuário no plano; merge de `spec/demo` em `staging_main`; criar a branch `demo` a partir dela

## B1 — Chave e módulo do site
- [ ] T1.1 `publicacao.json` (na `demo`): `demo`, `lancamento_v1`, textos da faixa e do aviso
- [ ] T1.2 `website/build/demo.py` (`ATIVO`, `texto_demo`, `banner_html`, `URL_PDF_DEMO`, `confere_html`)
- [ ] T1.3 Ganchos em `build_site.py` (lorem → provisório, pendente oculto, faixa, URL do PDF, conferência final)
- [ ] T1.4 CSS da faixa maior (`layout.css`, `mobile.css`)

## B2 — Textos provisórios
- [ ] T2.1 Lista das chaves que cairiam em lorem (título, fonte, tabela)
- [ ] T2.2 `textos_demo.json`: Visão geral e Introdução
- [ ] T2.3 `textos_demo.json`: Prioridade, Inclusão, Família e Cuidados
- [ ] T2.4 `textos_demo.json`: Proteção, Direito ao Brincar, Alimentação, Moradia
- [ ] T2.5 Revisão: números conferidos com `tabelas_finais/`, sem juízo, tamanho dentro de D6

## B3 — PDF de demonstração
- [ ] T3.1 `relatorio/latex/demo_aviso.tex` (1 página, texto de D11)
- [ ] T3.2 `relatorio/latex/build/demo_pdf.py` (corte com conferência dupla, aviso, links e marcadores)
- [ ] T3.3 Gancho em `gera_latex.py` (`--publicar` copia o PDF de demonstração)

## B4 — Deploy
- [ ] T4.1 Passo "Confere demonstração" no workflow da `demo`
- [ ] T4.2 (usuário) Regra de branches do ambiente `github-pages` → só `demo`
- [ ] T4.3 (usuário, com OK) Disparar o deploy a partir da `demo`

## B5 — Geração, conferência e registro
- [ ] T5.1 Build do site; screenshots desktop/tablet/telefone (Edge); `confere_textos.py`
- [ ] T5.2 `gera_latex.py --publicar`; conferir páginas, sumário, links e aviso
- [ ] T5.3 Conferência de R4 (JSON, DOCX e controle iguais aos da `staging_main`)
- [ ] T5.4 `validation.md`, `ROADMAP.md`, `CHANGELOG.md` (na `demo`)
