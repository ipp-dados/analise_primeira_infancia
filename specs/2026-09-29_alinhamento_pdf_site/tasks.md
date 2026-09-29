# TASKS — Alinhamento PDF × site

Legenda: [x] feito · [ ] a fazer

## Planejamento (branch `planning`, 2026-09-29)
- [x] P1 Comparar a estrutura do PDF gerado com a do site (capítulos/abas, seções/cartões, figuras)
- [x] P2 Perguntas agrupadas ao usuário → D1-D5
- [x] P3 `specification.md`, `plan.md`, `tasks.md`, `validation.md`; commit e push de `planning`

## B1 — Crosswalk
- [x] T1.1 Mover "Taxa de mortalidade na primeira infância" para depois de "neonatal tardia" (D1), com nota
- [x] T1.2 Tirar "Mortalidade infantil por causas evitáveis, por raça/cor" (D4); E16 em `specs/exclusoes.md`
- [x] T1.3 `motivo:` formal nos itens pendentes (D5)
- [x] T1.4 `tabela_no_texto:` em CadÚnico ÷ população e violência familiar por CAP (D3)
- [x] T1.5 `visualização: cobertura_vacinal_epi_ano.png` (D2); E1 atualizado

## B2 — `analise.py`
- [x] T2.1 Descomentar `cobertura_vacinal_epi_ano`; gerar tela e A4

## B3 — Gerador do PDF
- [x] T3.1 `motivo:` depois de `TEXTO_PENDENTE`
- [x] T3.2 `tabela_no_texto:` no corpo da seção, fora do apêndice

## B4 — Site
- [x] T4.1 `emite_bloco_pendente` lê frase fixa + `motivo:` do crosswalk; build falha sem motivo

## B5 — Regerar e validar
- [x] T5.1 Site, PDF (sem `--publicar`), DOCX
- [x] T5.2 `validation.md` (V1-V8)

## B6 — Fechamento
- [x] T6.1 `controle_revisao.json` (alerta da vacinação resolvido), CHANGELOG, README, ROADMAP, especificação do projeto,
  `relatorio/specs.md`
- [ ] T6.2 Merge `spec/alinhamento-pdf-site` → `planning` → `staging_main`; push
