# Especificação — Relatório Visual (`relatorio/`)

## Objetivo

Páginas HTML autocontidas que apresentam os indicadores de `analise.py` de forma
visual, para compartilhar com quem não vai abrir o notebook (planilha de
stakeholders, apresentação, etc.). Sem build step, sem backend: cada arquivo é
um único `.html` que roda abrindo direto no navegador (`file://`) ou por um
servidor estático qualquer.

## Histórico e decisões (processo iterativo)

### v1 (descontinuada) — relatório executivo curado

Pedido inicial: exportar a análise como página web "mais atraente
visualmente... focada em visuais, não em código... para stakeholders não
técnicos".

Abordagem: um dashboard estilo "relatório institucional" — banda de capa,
tira de KPIs em destaque, paleta de marca própria (verde-azulado + latão),
~15 gráficos *selecionados* (não todos), com narrativa e *callouts* escritos
especificamente para o relatório.

**Descontinuada** a pedido do usuário: "mantenha as visualizações mais
próximas do formato e estrutura originais do notebook, não omita
visualizações [...] quero um notebook com visual melhor, não um site
totalmente diferente."

### v2 — relatório fiel ao notebook (`index.html`)

- Reestruturado para seguir exatamente a ordem, os títulos (com os mesmos
  emojis) e as notas de markdown de `analise.py`.
- **Todas** as visualizações do notebook incluídas (~32 gráficos), nenhuma
  seção resumida ou omitida — inclusive as duas séries temporais do Censo que
  no notebook nunca chegam a ser exportadas em PNG (só `plt.show()`).
- Removida a "casca" de site: sem banda de capa, sem tira de KPIs, sem
  numeração de figuras/legendas, sem rodapé com grade de fontes — passou a
  ser um documento contínuo, seção após seção.
- Mantido o que valia a pena melhorar em relação a um PNG estático: gráficos
  SVG nativos, tooltip ao passar o mouse, legenda, rótulo direto no fim da
  linha/barra, tabela de dados alternativa (acessibilidade), tema claro/escuro.
- Cores dos gráficos: paleta categórica validada (8 matizes do skill de
  dataviz do workspace) para séries de até 8; estendida pragmaticamente até
  11 (cobertura vacinal), apoiada em rótulo direto + legenda + tooltip +
  tabela, já que 11 séries está fora do que a validação formal de
  distinguibilidade cobre.

### Ajustes pontuais em v2

- Iconografia revisada para tom mais sério: emojis com referência a morte,
  crianças ou dinheiro trocados (ex.: `⚰️→📉` Mortalidade, `💰→🗂️` Cadúnico) e,
  depois, `⚖️→🥗` (SISVAN — ícone de nutrição mais específico que "balança").
- Ícone do título trocado para 🏛️ (instituição), a pedido do usuário — sem
  usar/gerar um logo real do Instituto Pereira Passos, para não publicar uma
  marca institucional não verificada.
- Gráficos de barra do Cadúnico (por faixa de renda e por idade): valores
  passaram a ser arredondados e abreviados (`149.426` → `"149 mil"`) e o
  rótulo do valor ganhou coluna própria no grid da linha — antes ficava
  posicionado de forma absoluta e podia ultrapassar a caixa do gráfico.

### v3 — `lighter_index.html` (tema claro + paleta pastel + mapas)

- Fundo mais claro; as 11 cores categóricas + a cor de destaque recalculadas
  para tons pastel (mesma ordem de matiz, luminosidade/saturação ajustadas
  por fórmula HSL) — mantidas nos modos claro e escuro.
- Nova seção "🗺️ Mapas": os 5 PNGs coropléticos de `mapas/`, redimensionados
  de ~5000×3500px/~6MB para 1400px de largura em WebP (~130KB cada) e
  embutidos como `data:` URI direto na página.

### v4 — `white_index.html` (fundo branco + texto cinza)

- Parte da mesma base do `lighter_index.html` (mesmo conteúdo, mesma seção de
  mapas).
- *Tokens* de interface (fundo, superfícies, texto, linhas divisórias, caixas
  de nota) trocados para branco puro / cinza neutro, sem o matiz esverdeado
  do tema padrão.
- Cores dos gráficos mantidas em pastel, sem alteração — pedido explícito do
  usuário.

## Arquitetura técnica

- Um arquivo HTML autocontido por variante — sem dependência de rede além da
  fonte (Google Fonts).
- Dados extraídos das tabelas geradas por `analise.py` (pasta
  `tabelas_finais/`) via scripts Python ad-hoc, embutidos como JSON inline no
  `<script>` da página (nenhuma chamada de API em tempo de execução).
- Motor de gráficos em JavaScript puro (sem biblioteca externa), com três
  funções reaproveitadas em todas as seções:
  - `lineChart` — série(s) temporal(is); hover com crosshair, legenda quando
    há mais de uma série, rótulo direto no fim da linha, tabela de dados
    opcional.
  - `barChart` — barras horizontais de série única.
  - `groupedBarChart` — barras verticais agrupadas (comparativo de cobertura
    vacinal por ano, causas evitáveis por subgrupo × faixa etária).
- Tema claro/escuro via variáveis CSS, respeitando os três estados do tema do
  visualizador (`data-theme="light"`/`"dark"` e `prefers-color-scheme`, sem
  *stamp*).

## Arquivos

| Arquivo | Tema | Paleta dos gráficos | Seção de mapas |
| :--- | :--- | :--- | :--- |
| `index.html` | Padrão (pedra) | Plena | Não |
| `lighter_index.html` | Claro | Pastel | Sim |
| `white_index.html` | Branco/cinza neutro | Pastel | Sim |

## Limitações conhecidas

- CadÚnico (por faixa de renda/idade) depende de uma consulta ao banco CTPE
  que não pode ser reexecutada neste ambiente; os números refletem o último
  export salvo em `tabelas_finais/`.
- `relatorio/*.html` não está versionado no git: o `.gitignore` do projeto
  tem uma regra genérica `*.html` que os exclui — pendente decisão do usuário
  sobre versionar ou manter só local/artefato.
- Algumas seções de `analise.py` sem saída visual (funções auxiliares,
  junção de tabelas por bairro) não têm equivalente no relatório, por não
  gerarem gráfico algum no notebook.
