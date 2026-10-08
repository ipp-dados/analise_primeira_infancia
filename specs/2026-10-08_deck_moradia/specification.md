# SPECIFICATION — Apresentação de Moradia com dado pontual do Territórios Sociais (rodada de 2026-10-08)

Status: implementada e publicada em 2026-10-08 (branch `spec/deck_moradia`; `apresentacao/apresentacao_primeira_infancia_moradia.pptx/.pdf`).

## 1. Contexto

Pedido do usuário (2026-10-08): um deck variante de **Moradia** (20 a 25 slides) com os dados do eixo Moradia seguidos de
um dado pontual do programa **Territórios Sociais**. Recebidos em `apresentacao/variantes/moradia/`:
- `Levantamento de Dados - Casa Carioca e Primeira Infância.pdf` — roteiro da reunião com a Ação Comunitária (06/10/2026):
  análise geral, recorte da primeira infância, primeira infância e deficiência, ações de mitigação e 3 mapas;
- `inadequacao_habitacional_criancas_0_a_5_anos_2026-10-07.xlsx` — um domicílio por linha (4.794), só domicílios com
  inadequação e crianças de 0 a 5 anos: condição (critérios do Eixo Urbano), 7 itens, nº de crianças, 6 tipos de deficiência;
- `stakeholder.md` — ordem pedida pela apresentadora: total geral → por condição → crianças até 5 anos → deficiência por tipo;
  "Gustavo está tentando fazer um mapa".

Também pedido: mapas de **número de crianças** (não só %) para os mapas do eixo Moradia, no deck agora e no site depois
(ROADMAP 000c).

## 2. Decisões

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | Variante `variantes/moradia.md`, 23 slides: Parte 1 (Cadastro Único, a cidade: inadequação, componentes, número e % por bairro; adensamento e déficit, número e % por bairro) e Parte 2 (Territórios Sociais: o programa e as condições, total geral, domicílios com crianças por condição, itens, deficiência por condição e tipo, mapa), limites e próximos passos, resumo, encerramento | ordem do `stakeholder.md` e do roteiro; limite de 25 slides |
| D2 | Mapas de número só do deck (`apres_cadunico_inadequacao_n_bairro`, `apres_cadunico_adensamento_n_bairro`; classes discretas, bairros somados por RA sem cor, como em Inclusão) e versões de % do deck (sem linhas "Demais bairros…", teto de Tukey) | convenção do projeto; site fica para depois (ROADMAP) |
| D3 | Dado pontual lido direto da planilha por `build/territorios_sociais.py` (não passa por `tabelas_finais/`); números `ts_*` em `build/numeros.py`, gráficos de barras `apres_ts_*` em `build/mapas_apresentacao.py` (`tipo="barras"`, desenho `_a4_barras`) | constituição §3: dado pontual só no deck |
| D4 | Itens: "Sim" = adequado, "Não" = inadequado; "Não sabe / Não respondeu" fora da contagem do item | conferido: Condição 1 só tem "Não" em itens edilícios, Condição 2 só em água/esgoto |
| D5 | Recorte "até 72 meses" (a planilha é 0 a 5; o roteiro dizia 0 a 6) | padrão do projeto (D9 de 2026-09-29_pendencias) |
| D6 | Deficiência como "domicílio com registro de deficiência" até a equipe confirmar se é da criança | campos no nível do domicílio |
| D7 | Total geral do programa e mapa da equipe: slides com "a receber" / "mapa em elaboração" (marcados `revisar`) | não vieram na planilha |
| D8 | Ações de mitigação (itens 1.2, 2.2, 3.2 do roteiro) fora do deck, citadas em próximos passos | não há dado |
| D9 | A planilha (microdado por domicílio, com deficiência) **não é versionada** (decisão do usuário, 2026-10-08; `.gitignore`); o roteiro em PDF e o `stakeholder.md` (nomes de pessoas) também ficam fora. O mapa recebido é versionado (o build precisa dele) | dado sensível; o deck só publica agregados |

Revisão pedida pelo usuário (2026-10-08, depois da 1ª versão):
- **D10** — sem "a receber": sai o slide do total geral do programa; próximos passos só citam incluir as ações de mitigação.
- **D11** — slide de **conceitos** antes da Parte 1 (FJP, Cadastro Único, inadequação, déficit, adensamento, Territórios
  Sociais, critérios do Eixo Urbano, Casa Carioca); classe `.conceitos` no tema.
- **D12** — mapa recebido da equipe (`variantes/moradia/mapa_moradia_ts.jpeg`, domicílios com criança até 72 meses com TEA)
  no lugar do slide "mapa em elaboração", depois do slide de tipos de deficiência (o usuário o levou para antes do bloco
  e depois o devolveu); transição (classe `secao`) "Parte 3 · Novo recorte — Territórios Sociais e deficiência".
- **D16** — slide de conceitos simplificado: duas colunas, uma por fonte (FJP: inadequação, déficit, adensamento;
  Territórios Sociais: critérios do Eixo Urbano, do programa); sem Cadastro Único nem Casa Carioca.
- **D13** — título do slide do entorno: os 73% são dos domicílios **já inadequados**; o padrão da inadequação vem do entorno.
- **D14** — "critério da Fundação João Pinheiro; extração e cálculo do IPP" no texto, nos rodapés e nas fontes dos mapas.
- **D15** — mapas de %: título, legenda e nota forte dizem que o % é do universo do Cadastro Único, não de todas as
  crianças do bairro.
- Total: 24 slides.

## 3. Fora do escopo

Mapas de número no site/PDF (ROADMAP 000c).
