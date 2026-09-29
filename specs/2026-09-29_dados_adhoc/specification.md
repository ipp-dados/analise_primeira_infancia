# SPECIFICATION — Dados pontuais do CadÚnico: Moradia e Inclusão (rodada de 2026-09-29)

Status: **planejada em 2026-09-29** (branch `planning`); implementação em `spec/dados-adhoc`. O *como* está em
`plan.md`, as tarefas em `tasks.md`, os critérios de aceite em `validation.md`. Pedido original (genérico, em inglês):
`dados_adhoc.txt`; dado de referência: `Dados Domicílios CADÚNICO.xlsx` (o pedido fala em "CSV", mas é esta planilha).

## 1. Contexto

Os eixos **Moradia** e **Inclusão** estão só com quadros de pendente (site, PDF) e o deck diz que os dados do CadÚnico
"estão em importação". A equipe mandou uma **extração pontual** do CadÚnico (município do Rio, referência **08/2026**),
feita fora do pipeline (não vem do banco CTPE por `connect_db_ctpe`), para entrar **temporariamente** nas três saídas
até a extração automatizada substituí-la (prevista para o 4º trimestre de 2026).

**Moradia** — planilha com 11 abas, uma por filtro, cada uma com famílias, pessoas, crianças de 0-3 e de 4-6 anos:

| Indicador (pedido) | Tipo (pedido) | Abas / categorias |
| :-- | :-- | :-- |
| `domicilio_sem_banheiro` | domiciliar | Tem banheiro = Não |
| `domicilio_sem_agua_encanada` | territorial | Água canalizada = Não |
| `formas_abastecimento_agua` | territorial | Poço ou nascente; Cisterna; Outras formas (a rede geral **não** veio) |
| `formas_escoamento_esgoto` | territorial | Fossa séptica; Fossa rudimentar; Jogado em rio ou mar; Vala a céu aberto; Outra forma (a rede geral **não** veio) |

**Inclusão** — valores só no texto do pedido (sem arquivo): famílias com pessoa com deficiência 210.241; pessoas com
deficiência 401.074; crianças com deficiência de 0-3 anos 9.258 (3.086 com BPC) e de 4-6 anos 16.737 (7.214 com BPC).

Achados na leitura da planilha (tratados em R1):
- A1 — Fossa séptica, pessoas: `'17..149'` (texto) → **17.149** (erro de digitação evidente).
- A2 — Aba "RJ - ESCOAMENTO_FOSSA RUDIMENTA" é **cópia** da de fossa séptica (filtro "Fossa séptica", mesmos valores);
  a fossa rudimentar real está em "RJ - ESCOAMENTO_FOSSARUDIMENTAR". A cópia é descartada.
- A3 — Cisterna: 1.323 famílias e 2.572 pessoas, mas **0 crianças** nas duas faixas — improvável (nas outras categorias
  há ~0,1-0,15 criança de 0-3 por família). Publicado como **não informado**, não como zero.
- A4 — As faixas etárias da extração são 0-3 e **4-6**: incluem os 6 anos, fora da faixa padrão 0 a 5 (D9 de
  `specs/2026-09-29_pendencias`). Ver D1.
- A5 — Os 210.241 são famílias com **qualquer** pessoa com deficiência, não "famílias com criança com deficiência"
  (item do catálogo). Ver D2.
- A6 — Os indicadores de moradia são contagens absolutas no nível **município** (sem recorte sub-municipal): a regra de
  supressão < 20 (constituição §6) não se aplica; nenhuma taxa é calculada além da cobertura do BPC (numerador e
  denominador da mesma extração).

## 2. Decisões do usuário (2026-09-29)

| # | Decisão | Por quê |
| :-- | :--- | :--- |
| D1 | Publicar a faixa **4 a 6 anos** como veio, **com nota explícita** de que inclui os 6 anos (exceção prevista na regra D9); **não mudar nenhum dado ou gráfico existente** — a rodada só **acrescenta** | a extração tem essa faixa; refazer bloquearia a rodada |
| D2 | Famílias (210.241) e pessoas (401.074) com deficiência entram **só como contexto** no bloco das crianças com deficiência; os itens "Famílias no CadÚnico com criança com deficiência" e "por tipo de deficiência" **continuam pendentes** | o número não mede o que o item do catálogo pede |
| D3 | Saídas: **site** (acrescentar os blocos novos **sem substituir os quadros de pendente**), **PDF** e **deck** | pedido do usuário |
| D4 | Aviso **público, em pt-BR, sempre visível** (não só com `em_desenvolvimento`): "Dado pontual do Cadastro Único (referência: agosto de 2026), extraído fora da rotina automatizada; será substituído pela extração automatizada prevista para o 4º trimestre de 2026." | é uma ressalva real sobre o dado, não uma marca de desenvolvimento |

Detalhes decididos na planificação (registrados para revisão):
- **Aditivo também no crosswalk:** os itens pendentes de Moradia e Inclusão ficam como estão; entram itens novos `###`
  com o sufixo "(dado pontual, ago/2026)". Os quadros de pendente continuam dizendo que o indicador depende de extração
  nova — verdade para a extração automatizada.
- **Deck:** um slide **novo** antes de "Eixos incompletos"; o texto deste não muda (D1: só acrescentar).
- **Metadados de rastreio** (pedido, passo 1): `is_adhoc: true`, `ref_date: "2026-08"`, `replacement_pending: true` num
  manifesto versionado junto do dado, lido pelos geradores (fonte única do texto do aviso D4).
- Os achados A1-A3 são corrigidos **no carregamento** (a planilha original fica intacta, versionada como veio).

## 3. Requisitos

**R1 — Camada de dados.** `dados_locais/cadunico/` (pasta nova; o CadÚnico por banco continua sem arquivo) com:
(a) a planilha original renomeada em snake_case (`domicilios_cadunico_2026_08.xlsx`); (b) `deficiencia_cadunico_2026_08.csv`
com os 6 valores do pedido; (c) `adhoc_2026_08.json`, o manifesto (metadados, texto do aviso, notas de faixa e de
qualidade A1-A3). Funções em `primeira_infancia/cadunico.py`: `carrega_moradia_cadunico_adhoc` (identifica a categoria
pelo **filtro** do cabeçalho, não pelo nome da aba; aplica A1-A3; descarta duplicata de filtro) e
`carrega_deficiencia_cadunico_adhoc` (com a cobertura do BPC por faixa). Dado agregado do município: pode ser versionado.

**R2 — `analise.py`.** Célula nova no fim da seção do CadÚnico ("Dados pontuais (ago/2026)"), **sem depender do banco**,
que grava em `tabelas_finais/`: `cadunico_adhoc_moradia_domicilio_2026_08.csv` (sem banheiro, sem água canalizada),
`cadunico_adhoc_moradia_territorio_2026_08.csv` (abastecimento e escoamento por categoria) e
`cadunico_adhoc_deficiencia_2026_08.csv` (0-3, 4-6, total 0-6; com e sem BPC; % BPC). Nenhuma outra célula muda.

**R3 — Crosswalk.** Em `specs/estrutura_eixos.md`, itens novos (fonte "Cadastro Único — extração pontual, referência
08/2026", `tabela_no_texto:`, `- aviso:` com o texto D4 e a nota de faixa D1). Campo novo **`- aviso:`** (texto público,
ao contrário de `- nota:`), mostrado pelo site e pelo PDF abaixo do título do item.

**R4 — Site.** Blocos novos em Inclusão e Moradia, depois dos pendentes: (a) Inclusão: cartões de indicador (crianças
com deficiência 0-3, 4-6; contexto famílias/pessoas) e comparação da **cobertura do BPC** (0-3: 3.086/9.258 = 33,3%;
4-6: 7.214/16.737 = 43,1%) em barras de proporção; (b) Moradia: cartões dos déficits (sem banheiro, sem água canalizada,
esgoto a céu aberto/rio ou mar) e tabela por faixa (famílias, pessoas, 0-3, 4-6) das formas de abastecimento e de
escoamento. Aviso D4 em cada bloco (callout próprio "Dado pontual"). CSS novo em `components.css`/`mobile.css`; nada do
que já existe muda de aparência.

**R5 — PDF.** Os itens novos saem como seção com a tabela no corpo (`tabela_no_texto`) e o aviso num quadro; a fonte
entra no inventário de fontes. Build sem `--publicar`.

**R6 — Deck.** Slide novo com 3-4 números (`{{n:...}}` de `apresentacao/build/numeros.py`, lidos das tabelas de R2) e a
nota do dado pontual. Build sem `--publicar`.

**R7 — Rastreio.** `ROADMAP.md`: item "substituir os dados pontuais do CadÚnico (ago/2026) pela extração automatizada —
4º tri de 2026", apontando para o manifesto e para a lista de arquivos a remover/trocar; a rodada no "Rodada atual".
Registro em `specs/exclusoes.md` não se aplica (nada é excluído).

## 4. Fora do escopo

- Mudar qualquer dado, gráfico, mapa ou texto existente (D1) — inclusive os quadros de pendente e o slide
  "Eixos incompletos".
- Recorte por bairro/AP/RA, série temporal, tipo de deficiência (não vieram na extração).
- Texto curado dos itens novos: sai com o texto provisório (lorem) até a próxima rodada de curadoria, como os demais.
- Publicar (`--publicar`, deploy do site): depende do OK do usuário, como nas outras rodadas.
- A integração automatizada com o banco (é a substituição planejada em R7).

## 5. Ajustes depois do merge (usuário, 2026-09-29)

| # | Pedido | Feito |
| :-- | :--- | :--- |
| D5 | Deck: dividir o slide único em dois, depois do slide 28 | slide 29 **Inclusão** (25.995 crianças com deficiência; BPC 33% de 0 a 3 = 3.086 de 9.258, 43% de 4 a 6 = 7.214 de 16.737) e slide 30 **Moradia** (os 5 destaques do site, só crianças de 0 a 6: sem banheiro 792, sem água canalizada 1.425, vala a céu aberto 2.226, rio ou mar 1.247, fossa rudimentar 1.411; nota "os números não se somam"). Deck com 35 slides |
| D6 | Site: crianças de 0 a 6 e as faixas 0 a 3 / 4 a 6 em destaque; totais (famílias, pessoas) como dado secundário | cartões com o número de crianças de 0 a 6, as duas faixas logo abaixo (`kpi-faixas`) e famílias · pessoas no rodapé do cartão; tabelas de Moradia com "Crianças de 0 a 6 anos" e as faixas primeiro, famílias e pessoas no fim. PDF e CSVs inalterados |
