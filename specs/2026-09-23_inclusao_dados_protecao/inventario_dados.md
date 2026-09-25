# Inventário dos dados — `dados_locais/protecao/`

Levantamento feito na abertura da rodada (nenhum código escrito). Base para `specification.md`.
Pasta ainda **não commitada** (`git status`: untracked) — lembrar que `dados_locais/` não é gitignored.

## 1. `violencia_familiar/` (extraído de `Violência Familiar.zip`; 7 CSVs, Sinan NET / Tabnet municipal)

- Arquivos: `violencia_familiar_{mae,pai,padrasto,irmao(a),conjuge,exconjuge,filho(a)}.csv`
- Cabeçalho de 6 linhas de metadados antes da tabela (filtros: Rio de Janeiro 330455, idade
  0 a 5 anos, "<vínculo>: Sim", período 2007-2026) → `skiprows`/parsing próprio, encoding
  **latin-1**, separador `;`.
- Formato **largo**: `Bairro Resid` = `"<codigo>   <NOME>"` × colunas de ano + `Total`.
  Difere do formato longo de `limpeza_tabnet_bairros` (bairro, ano, valor).
- **Colunas de ano esparsas**: só aparecem anos com pelo menos 1 caso (ex.: `conjuge` tem
  2018-2021, 2025). Precisa reindexar para grade completa (como `carrega_raca_bairro`).
- Linha `Total` no fim (remover). Contagens **absolutas**, sem denominador.
- Escala: `mae` 15.066 casos, `pai` ~ similar; `conjuge`/`exconjuge`/`filho` < 20 (irrelevantes
  para mapa; talvez agregar em "outros").
- 2026 é ano parcial. Sub-notificação/mudança de ficha em 2017 (salto 600→1514 em `mae`) —
  possível quebra de série a documentar.
- Filtro é "vínculo do provável autor com a vítima = Sim"; os vínculos **não são exclusivos
  nem somam o total de violência familiar**.

## 2. `notif_viol_ interpes_ autoprovocada_menor_1, 1-5.csv`

- Mesmo formato Sinan. Filtro real no cabeçalho: **"Lesão Autoprovocada: Sim"** — ou seja,
  apenas autoprovocada, apesar do nome do arquivo ("interpessoal/autoprovocada").
- 40 casos no total (33 em 2026), 24 bairros: muito esparso → mapa por bairro pouco útil;
  série municipal/por CAP mais adequada.
- Não há recorte separado "menor de 1 ano" vs "1 a 5" (catálogo pede os dois); o filtro é
  0-5 agregado.

## 3. `violencia_territorial.xlsx` (Data.Rio, IPS 2024)

- Fonte real: **Data.Rio / Índice de Progresso Social**, não ISP (catálogo diz ISP).
- Nível **Região Administrativa (RA)** + linha "RIO DE JANEIRO", **um único ano (2024)**.
- 3 indicadores: taxa de homicídios, homicídios por ação policial, homicídios de jovens
  negros (taxas, todas as idades — **não é específico de 0-6 anos**).
- Só 32 RAs (faltam RAs sem dado no IPS); nomes com romano + nome, encoding latin-1.
- Não há geojson de RA em `dados_locais/geo/` (só bairros, CAP, UF, municípios). Bairros
  do geojson não trazem RA nativamente (existe `_RA_PARA_CAP` em analise.py, RA → CAP).

## 4. Itens do catálogo Proteção **sem dado** nesta pasta

- "Taxa de notificações de violência (0 a 6 anos)" — precisaria de denominador (população
  0-6 do Censo/nascidos vivos, já existentes em analise.py) ou nova extração.
- "Crianças que sofrem violência, por tipificação (sexo e idade)" — Tabnet municipal, não
  fornecido.
- Recortes separados "menor de 1 ano" vs "1 a 5 anos" — não fornecidos.

## 5. Decisões da abertura da rodada (respostas do usuário)

- **Lacunas**: só o que foi fornecido — taxa 0-6, tipificação e recorte <1/1-5 ficam `pendente`.
- **Territorial (IPS/RA 2024)**: gráfico de barras por RA, sem novo geojson; rotular fonte
  Data.Rio/IPS e avisar que não é específico 0-6.
- **Vínculos**: série temporal comparando vínculos + mapas por bairro para mãe, pai e "outros"
  (padrasto, irmão(ã), cônjuge, ex-cônjuge, filho(a) agregados); se redundante, remover depois.
- **Qualidade**: excluir 2026 (parcial); anotar possível quebra de série em 2017.
