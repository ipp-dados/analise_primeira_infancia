# SPECIFICATION — Apresentações breves dos eixos Alimentação e Direito ao Brincar (rodada de 2026-10-06)

Status: implementada em 2026-10-06 (branch `spec/deck_alimentacao_brincar`).

## 1. Contexto

Pedido do usuário (2026-10-06): duas variantes do deck, na estrutura da apresentação de Inclusão
(`specs/2026-10-06_deck_inclusao`), para os eixos **Alimentação** e **Direito ao Brincar**; em Alimentação, slides breves
com um dado pontual recebido como imagem (`apresentacao/variantes/alimentacao_adhoc/`), tomando o título do arquivo como
referência: "Famílias em insegurança alimentar nos Territórios atendidos - Fase de expansão" (mapa de calor por CAP).

## 2. Decisões

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | Variantes `variantes/alimentacao.md` (12 slides, D11) e `variantes/direito_brincar.md` (8 slides), mesma sequência da de Inclusão: capa, o que o eixo mostra (com nota forte de limite da fonte), números/séries, número por bairro antes do percentual, limites e próximos passos, resumo dos indicadores, encerramento | "use a estrutura da apresentação de Inclusão" |
| D2 | `apresentacao.md` e a variante de Inclusão **não mudam** | fora do pedido |
| D3 | Só acréscimos no gerador: chaves `alim_*`/`brin_*` em `build/numeros.py`; mapas só do deck para homicídios por ação policial e de jovens negros (mesmo desenho do de homicídios: teto de Tukey, fonte "Data.Rio" sem o IPS — slide_revision D12); séries SISVAN só do deck | números calculados, nunca digitados |
| D4 | **SISVAN no deck: % recalculado de contagem ÷ total e série até 2025** (2026 é parcial) | duas colunas de % das tabelas têm erro na origem (desnutrição 2023: 3,74% publicado × 5,7% pelas contagens; obesidade 2009: 0,07% × 7,0%); o slide cita o último ano completo |
| D5 | Dado pontual de insegurança alimentar: imagem como recebida (renomeada para `inseguranca_alimentar_territorios_expansao.jpeg`, nome ASCII para `fig:`), título do slide = título do arquivo, kicker "Dado pontual", nota de que mostra só os territórios atendidos; **fonte e data a confirmar** (rodapé e nota do apresentador) | não há metadado na imagem; leitura das CAPs é visual |
| D6 | Gerador: `fig:nome` procura também em `apresentacao/variantes/*/` (imagem pronta de outra equipe, guardada junto da variante) | sem caminho especial no .md |
| D7 | Dado pontual só na apresentação: não entra no crosswalk, no site nem no PDF | constituição §3 (dado pontual nunca vai para o relatório nem para o site final) |
| D8 | Direito ao Brincar: as taxas de ação policial e de jovens negros aparecem como "taxa (Data.Rio)", sem "por 100 mil" | a planilha do Data.Rio não traz a unidade dessas duas; a confirmar na ficha do indicador |
| D9 | Correção no gerador de mapas: a nota de valores extremos só nomeia regiões que existem no mapa (o "998", bairro ignorado do Tabnet, aparecia na lista) | achado no slide de baixo peso; afeta também o deck principal na próxima geração (só o rodapé) |

Revisão pedida pelo usuário (2026-10-06, depois da 1ª versão):
- **D10** — o slide 8 diz que o dado é do programa **Territórios Sociais (IPP/ONU-Habitat)**: kicker, texto e rodapé
  ("Fonte: Territórios Sociais (IPP/ONU-Habitat), fase de expansão"). A data e o método seguem a confirmar.
- **D11** — o slide do dado pontual vira **dois**: o 8 apresenta o dado (fonte, alcance, ressalva); o 9 traz a leitura
  pedida pelo usuário — na CAP 5.3, muitos territórios com insegurança alimentar; na porção leste (CAPs 3.2, 1.0 e 2.2),
  menos territórios, com concentração mais alta (leitura visual do mapa de calor). Total: 12 slides.

## 3. Fora do escopo

Corrigir as colunas de % do SISVAN no `analise.py` (vai para o ROADMAP); atualizar o deck principal; site e PDF.
