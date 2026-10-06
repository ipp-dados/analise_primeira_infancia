# SPECIFICATION — Apresentação breve do eixo Inclusão (rodada de 2026-10-06)

Status: planejada e implementada em 2026-10-06 (branch `spec/deck_inclusao`), depois `staging_main` → `demo`.

## 1. Contexto

Pedido do usuário (2026-10-06): "crie uma apresentação nova e breve sobre a seção Inclusão, usando o deck anterior como
referência; não atualize o deck agora". O eixo Inclusão acabou de ganhar dados da extração rotineira do CadÚnico (jul/2026,
`specs/2026-10-06_cadunico_inclusao_moradia`): crianças até 72 meses com deficiência, por tipo e por bairro, e famílias com
BPC por deficiência. Na mesma conversa: o adensamento excessivo fica com o título "mais de 2 pessoas por dormitório"
(decisão do usuário; fecha D11 daquela rodada).

## 2. Decisões

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | **Variante do deck** (`apresentacao/variantes/inclusao.md`), no mesmo pipeline Marp, tema e regras de texto do deck principal (`apresentacao/README.md`) | "usar o deck anterior como referência"; um gerador, uma identidade visual |
| D2 | `apresentacao/apresentacao.md` **não muda** (o slide de Inclusão com o dado pontual fica como está) | "não atualize o deck agora" |
| D3 | Só **acréscimos** no gerador: chaves `incl_*` em `build/numeros.py` (números calculados das tabelas, nunca digitados) e um mapa só do deck em `build/mapas_apresentacao.py` (teto de Tukey e nota dos extremos, regra R7 do deck) | o deck principal sai igual |
| D4 | Breve: 7 slides — capa, o que o eixo mede, números principais, tipos de deficiência, território, BPC, limites e próximos passos, encerramento (8 com ele) | "breve" |
| D5 | Publicado como `apresentacao/apresentacao_primeira_infancia_inclusao.pptx/.pdf` (`--publicar` de uma variante não sobrescreve o deck principal) | entregável versionado, como o deck principal |
| D6 | Texto: "até 72 meses"; BPC dito como benefício **da família**; diferença com o dado pontual de ago/2026 **fora** dos slides (pendente de revisão do usuário) — só na nota do apresentador | regras do deck; ROADMAP |

## 3. Fora do escopo

Atualizar o deck principal; Moradia (só se pedido); site/PDF (não mudam nesta rodada, salvo o fechamento de D11).
