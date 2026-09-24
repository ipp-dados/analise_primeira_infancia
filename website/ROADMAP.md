# Roadmap do site

Pendências do site estático (`website/`). Prioridades e histórico do projeto como um todo ficam em
`specs/roadmap.md`; a rodada que criou esta estrutura é `specs/website_refactor/`.

## Próximo: versão mobile (responsiva)

A rodada `website_refactor` foi só desktop (spec §4.8). O CSS usa grid/flex e variáveis para
que isto mexa em poucas regras. O que falta, por componente:

- **Barra de abas** (`.tabbar`): hoje rola na horizontal sem indicação. Em tela estreita: rolagem
  horizontal com sombra nas bordas e aba ativa trazida para a vista (`scrollIntoView` no
  `tabchange`), ou só ícones + rótulo da ativa, ou um menu (`<select>`/gaveta). Decidir com o usuário.
- **Sumário lateral** (`.outline`): a coluna de 280 px não cabe. Virar uma barra recolhível no topo
  do painel ("Nesta seção ▾") ou uma gaveta; a barra de progresso pode ficar como uma linha fina
  sob a barra de abas.
- **Grade da página** (`.page-grid`): 1 coluna abaixo de ~1100 px; `--gutter` 16 px abaixo de 520 px.
- **Banner**: título em 2 linhas já é fixo; com a fonte de 2,7 rem, "Primeira Infância Carioca"
  quebra de novo em telas < ~420 px — reduzir a fonte do h1 (clamp) em vez de deixar virar 3 linhas.
  Links do banner abaixo do título, não ao lado.
- **Cartões com pills** (`.option-card-grafico`): a coluna de pills de 210 px vira fileira acima do
  gráfico (já existe regra `@media (max-width:720px)`, conferir com o novo layout).
- **Mapa + texto** (`.option-card-mapa`): texto abaixo do mapa, sem a altura presa à do mapa
  (hoje o texto rola por dentro para igualar a altura — em coluna única, deixar crescer).
- **Legenda do mapa** sobre o mapa ocupa muito em tela pequena: mover para baixo do mapa.
- **Tooltips** (gráfico e mapa) dependem de `mousemove`: tratar toque (tap mostra, segundo tap
  ou toque fora esconde).
- **Botões dos cartões** (CSV, outliers) sobrepõem o título em cartões estreitos: ir para uma linha
  própria abaixo do título.
- **Tabelas largas**: já rolam na horizontal (`.table-scroll`); conferir `table.plain`.
- **Alvos de toque**: pills, abas e links do sumário com no mínimo 44×44 px.
- **Fonte base de 19,2 px** (pedido do usuário, v6.5): manter no desktop; avaliar 17-18 px no celular.
- **Validação**: Chrome/Firefox/WebKit em 390×844 e 768×1024 (Playwright), mais um aparelho real.

## Backlog

- **Página "Fale Conosco"** (pedido do usuário, 2026-09-24): página própria, acessível pela barra de
  navegação (item fixo à direita da barra de abas, ou uma aba própria). Formulário exige backend,
  que o GitHub Pages não tem — opções: link `mailto:` + texto (o mais simples, estático), ou
  serviço de formulário externo (exige decisão sobre dados pessoais/LGPD). Confirmar o contato
  certo (hoje o rodapé usa `ascom.ipp@prefeitura.rio`, ainda placeholder — `specs/relatorio-interativo` T6.2).
  Rota por hash (`#fale-conosco`) como uma aba, para não precisar de outra página HTML.
- **Logo em SVG oficial**: substituir `ipp-logo.png` + cópias pelo vetor da Ascom do IPP, se fornecido.
- **Conclusões e "Principais achados"** ainda são lorem ipsum; o DOCX de curadoria não tem bookmark
  para as conclusões (`conclusao-<sid>` em `relatorio/textos_curados.json` funciona à mão).
- **Fontes quase repetidas** na caixa "Fontes desta seção" (mesma base com nota diferente):
  unificar as constantes `FONTE_*` do gerador.
- **Dados por aba com carregamento tardio** e **outliers de mapa como troca de cor**: medidos e
  deixados de fora (spec §4.9); voltam se o orçamento de tamanho estourar.
- **Tema escuro**: removido na v6.2; os tokens em `css/main.css` facilitam voltar.
