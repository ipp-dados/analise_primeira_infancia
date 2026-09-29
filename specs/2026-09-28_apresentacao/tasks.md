# TASKS — Apresentação

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-09-28)
- [x] P1 Ler `presentation_readme.md`; revisar o roteiro de 30 slides contra a estrutura nova e os dados existentes
- [x] P2 Escolher o gerador (Marp, decisão do usuário) e desenhar o pré-processador e o formato do `.md`
- [x] P3 Roteiro slide a slide com figuras reais e números calculados (`specification.md` §4)
- [x] P4 Lacunas e riscos (R1-R5) e perguntas do checkpoint (Q1-Q6)
- [x] P5 Respostas do usuário a Q1-Q6 (specification.md §6.1)

## Bloco 1 — Esqueleto e build
- [x] T1.1 `apresentacao/` + `package.json` + `.gitignore`
- [x] T1.2 `gera_apresentacao.py` (campos, condicionais, `fig:`, QR, marp-cli, `--publicar`)
- [x] T1.3 `numeros.py` com as chaves da §4
- [x] T1.4 Deck de teste de 3 slides

## Bloco 2 — Tema
- [x] T2.1 `tema/ipp.css` com tokens, logo e 10 layouts
- [x] T2.2 Conferência de legibilidade

## Bloco 3 — Deck
- [x] T3.1 R1: conferir o denominador de nascidos vivos (65.507 × 59.171)
- [x] T3.2 Slides 1-6
- [x] T3.3 Slides 7-20 (R3: mapa de limites)
- [x] T3.4 Slides 21-30 (R2: diagrama do hub, capturas do site e do PDF)
- [x] T3.5 R4: ajuste de mapas para 16:9, se necessário

## Bloco 4 — Variantes e documentação
- [x] T4.1 `variantes/exemplo_secretaria.md`
- [x] T4.2 `apresentacao/README.md`
- [x] T4.3 tech-stack, CLAUDE.md, ROADMAP, especificação do projeto

## Bloco 5 — Fechamento
- [x] T5.1 `validation.md`; revisão visual do PDF e do PPTX
- [ ] T5.2 Merge, tag `rodada/apresentacao`
  - 2026-09-29: merge feito (`40a702d` em `planning`, `ab9f803` em `staging_main`); tag com o OK do usuário
    (`specs/2026-09-29_pendencias` T9.3)
