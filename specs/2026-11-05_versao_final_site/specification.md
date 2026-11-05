# SPECIFICATION — Versão final do site e do relatório (rodada de 2026-11-05)

Status: **Bloco 1 (textos) e Bloco 2 (dados faltantes) feitos; Blocos 3-9 planejados, aguardando OK do usuário.**
Branch `spec/versao_final_site`. Pedido original: `website_release.md` (raiz). O *como* está em `plan.md`, as tarefas em
`tasks.md`, os critérios de aceite em `validation.md`.

## 1. Contexto

`staging_main` é o ambiente de teste; `main` passa a ser o site publicado. Hoje o GitHub Pages publica a branch `demo`
(constituição §7), com a faixa "em desenvolvimento" no site e a marca d'água no PDF (`relatorio/publicacao.json`).
Antes desta rodada: pendências fechadas (`specs/2026-11-05_fechamento_pendencias`). Nesta rodada, já feito: todos os
textos (site e PDF sem lorem), a lista de dados faltantes (`docs/dados_faltantes.csv`) e o documento de plano para os
gestores (Claude Docs).

## 2. Decisões do usuário (2026-11-05)

| # | Decisão |
| :-- | :-- |
| D1 | **Banner novo** com a foto do Unsplash pedida (criança segurando um livro colorido aberto, `wccs6fKUtok`), com crédito no site |
| D2 | **Mapa de referência da cidade** na Visão geral: bairros, Regiões Administrativas e Áreas de Planejamento, **interativo, com camadas** (bairros em linha fina, RA e AP em linhas mais grossas, rótulos das AP, botões para mostrar os nomes de bairro / RA / AP, nome no hover) |
| D3 | **Rodapé**: sem o e-mail de contato (feito em 2026-11-05); conferir os links que ficam |
| D4 | **Sem a faixa "em desenvolvimento"** no site e sem a marca d'água no PDF (`publicacao.json` → `false`) |
| D5 | **PDF: um `.tex` editável por capítulo**, editado à mão daqui em diante; **o texto fica congelado, os dados continuam gerados** (figuras e tabelas do apêndice saem da execução de `analise.py`) |
| D6 | **Nova capa e nova folha de rosto** do PDF |
| D7 | **Textos de curadoria só do site**: `relatorio/textos_curados.json` alimenta só o site; o PDF passa a ter o próprio texto nos `.tex` (D5) |
| D8 | **Sem DOCX**: os scripts de curadoria em DOCX saem do repositório (ficam no histórico, numa tag); a conferência de números contra os dados fica |
| D9 | **Release do PDF no GitHub**: instalar o `gh` nesta máquina; o PDF é gerado localmente e a Release publicada daqui, com OK do usuário |
| D10 | **Automatizar o GitHub Actions**: deploy do site automático a partir da `main`; corrigir erros e dependências |
| D11 | **Publicação**: `staging_main` → `main`, e a constituição passa a dizer que a `main` é o site publicado |
| D12 | **Revisão final** dos pipelines e da documentação; **teste completo** do site no desktop e no celular |

## 3. Requisitos

**R1 — Banner (D1).** Foto baixada do Unsplash e servida pelo próprio site (regra do site: nenhuma requisição a
terceiros), em versões responsivas (`srcset`, ≤ 200 KB a maior, WebP/JPEG). Crédito visível no banner ou no rodapé, no
formato pedido pela licença do Unsplash ("Foto de <autor> no Unsplash", com links). Título, logo e botões continuam
legíveis (contraste WCAG AA sobre a foto, com camada escura ou recorte). O celular mantém a barra compacta de hoje
(`css/mobile.css`).

**R2 — Mapa de referência (D2).** Novo bloco na Visão geral, logo depois da Introdução, gerado por `build_site.py` a
partir de `dados_locais/geo/limite_bairros_rio.geojson` (RA e AP por `dissolve` de `codra` e `area_plane`, como nos
outros mapas). Mesmo motor SVG e mesmo fundo dos mapas atuais (`data/geo.js`). Sem cor de dado (só contornos; água
azul, terra neutra). Acessível: alternativa em texto (tabela bairro → RA → AP, para download). Entra também no PDF como
figura estática (A4) no capítulo de Introdução.

**R3 — Rodapé (D3).** Links conferidos (Transparência Rio, LGPD, IPP, GitHub, PDF, Base dos Dados); link da Release do
PDF apontando para `releases/latest`.

**R4 — Versão final (D4).** `publicacao.json` → `em_desenvolvimento: false`; o build já bloqueia se sobrar dado
pontual — conferir que não sobra. A faixa amarela e a marca d'água somem juntas.

**R5 — PDF em `.tex` por capítulo (D5, D6, D7).** Exportar uma vez o que `gera_latex.py` gera hoje em
`gerado/capitulos.tex` para `relatorio/latex/capitulos/<nn>_<eixo>.tex` (Introdução + 7 eixos + Considerações finais),
com o texto já resolvido (sem leitura do JSON). `relatorio.tex` passa a fazer `\input` desses arquivos. `gera_latex.py`
deixa de escrever capítulos: continua gerando **figuras** (A4), **tabelas do apêndice**, `resumo.tex`/aviso/fontes e
os rótulos que os capítulos citam; um teste falha se um capítulo citar figura ou tabela que não existe. Nova capa e
folha de rosto em `pretextual/` (identidade IPP, foto do banner ou arte, ABNT).

**R6 — Curadoria só do site, sem DOCX (D7, D8).** Saem `relatorio/curadoria/gera_docx_curadoria.py`,
`sincroniza_docx.py`, `incorpora_update_docx.py`, `compara_updates.py` e as referências nas skills, no `CLAUDE.md` e
na especificação do projeto (tag `rodada/curadoria_docx` antes de apagar). Ficam `textos_curados.json`,
`textos_eixos.md` + `importa_textos_eixos.py` e `website/build/confere_textos.py`, que passa a conferir o texto do site
contra o JSON (sem DOCX). `controle_revisao.json` fica como histórico.

**R7 — Release (D9).** `gh` instalado (winget) e autenticado pelo usuário (`gh auth login`); script ou passo
documentado que gera o PDF, cria a tag `vX.Y.Z` e a Release com o PDF anexado. O link "Relatório final em PDF" do site
aponta para a última Release.

**R8 — GitHub Actions (D10).** Deploy do Pages automático em push na `main` (mais o gatilho manual); conferência do
conteúdo publicado mantida; ações em versões atuais; um job de checagem em PR/push para `staging_main` (site gerado
coerente: sem lorem, sem `data-dado-pontual`, orçamento de tamanho, só tipos de arquivo permitidos).

**R9 — Publicação (D11).** Merge `spec/versao_final_site` → `staging_main` → `main`; Pages passa a publicar a `main`;
a `demo` deixa de ser publicada (fica congelada como registro). Constituição §7 alterada (papel de `main`,
`staging_main` e `demo`).

**R10 — Revisão e teste (D12).** Pipelines (`analise.py`, site, PDF, importação de textos) e documentação
(`CLAUDE.md`, `docs/especificacao_projeto.md`, skills, `README.md`, `ROADMAP.md`) conferidos contra o que existe;
títulos ainda com "0 a 5 anos" passam a "até 72 meses" onde a regra pede; teste completo do site (todas as abas, mapas,
downloads, links, desktop 1366 px e celular 390 px).

## 4. Fora do escopo

Os 6 itens de `docs/dados_faltantes.csv` (os itens 1 e 3 são a próxima rodada) e os 2 pedidos que dependem de dados extras (amamentação e aleitamento materno por AP; serviços públicos em camadas GIS), a fase 1c de organização e a oferta de educação
infantil por bairro (ROADMAP).

## 5. Riscos

- **Congelar o texto do PDF (R5)**: depois da exportação, mudança de número nos dados não atualiza o texto do PDF —
  o teste de rótulos pega figura/tabela sumida, mas não número citado no texto. Mitigação: a conferência de números
  (ROADMAP, Próximas features item 1) passa a ler também os `.tex`.
- **Foto no banner**: peso da página (orçamento de 1 MB no `index.html`, 2 MB no site) e contraste.
- **Deploy automático**: um push na `main` publica na hora; a `main` só recebe merge de `staging_main` com OK.
