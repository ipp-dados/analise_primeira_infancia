# PLAN — Apresentação (Marp)

Especificação: `specification.md`. Pré-requisito: `specs/2026-09-28_nova_estrutura` implementada (os slides
21-25 seguem os 7 eixos, e o slide 5 conta os pendentes pela estrutura nova). Os Blocos 1-2 não dependem dela e
podem começar em paralelo. Branch: `spec/apresentacao`; commits `SPEC-Apresentacao: Bloco N -- …`.

## Bloco 0 — Checkpoint com o usuário
- Respostas a Q1-Q6 (`specification.md` §6). Sem resposta, valem os padrões da tabela.

## Bloco 1 — Esqueleto e build
- `apresentacao/` com `package.json` (marp-cli fixado), `.gitignore` de `_build/` e `node_modules/`.
- `gera_apresentacao.py`: frontmatter, `{{campo}}`, `<!-- se: … -->`, `fig:`, QR; chama `npx marp` para
  `--pdf`, `--pptx` e `--html`; `--publicar` copia o PDF.
- `numeros.py`: chaves da §4, cada uma com arquivo, coluna, ano e formato pt-BR; erro se faltar.
- Teste mínimo: um deck de 3 slides com número, figura, bloco condicional e QR.

## Bloco 2 — Tema IPP
- `tema/ipp.css`: tokens do site (`--ipp-navy`, `--ipp-cyan`, `--c1..--c11`), fontes do site, logo, faixa de
  cores; as 10 classes de layout; rodapé de fonte.
- Conferir a legibilidade a 3 m (título ≥ 40 px, número ≥ 120 px a 1280×720).

## Bloco 3 — Deck completo
- Os 30 slides da §4 em `apresentacao/apresentacao.md`.
- R1 (denominador de nascidos vivos) resolvido antes dos slides 18-19.
- R2 (diagrama do hub) em SVG; R3 (mapa de limites) com a skill `generate_map` ou substituição.
- R4: se os mapas cortarem em 16:9, variante de tamanho no `primeira_infancia/impressao.py` (à parte, com o OK do usuário).

## Bloco 4 — Variantes e documentação
- `variantes/exemplo_secretaria.md` (outro público + blocos desligados) gerado sem erro.
- `apresentacao/README.md`: editar, gerar, derivar, publicar.
- `specs/tech-stack.md` (Marp/Node, segno), `CLAUDE.md` (diretório novo), `ROADMAP.md`,
  `docs/especificacao_projeto.md` (produto novo).
- Avaliar uma skill de projeto `build_presentation` (como `build_website`/`export_pdf_report`), se o usuário quiser.

## Bloco 5 — Validação e fechamento
- `validation.md`: 30 slides, 0 placeholders, toda figura com fonte, PDF/PPTX abertos e revisados por captura
  de tela, variante gerada; merge e tag `rodada/apresentacao`.
