# Apresentação — Diagnóstico da Primeira Infância Carioca

Deck de 33 slides (Marp) gerado a partir de **um arquivo Markdown**: `apresentacao.md`.
Decisões e roteiro em `specs/2026-09-28_apresentacao/`; estrutura atual (33 slides) em
`specs/2026-09-29_slide_revision/`.

## Gerar

```bash
cd apresentacao && npm ci && cd ..                          # uma vez (marp-cli fixado em package.json)
pip install -r requirements-dev.txt                          # segno (QR code) e playwright (capturas do site)
python apresentacao/build/gera_apresentacao.py               # PPTX + PDF em apresentacao/_build/
python apresentacao/build/gera_apresentacao.py --png         # uma imagem por slide, para conferir
python apresentacao/build/gera_apresentacao.py --publicar    # copia PPTX e PDF para apresentacao/ (versionados)
python apresentacao/build/gera_apresentacao.py --editavel    # também um PPTX editável (experimental, LibreOffice)
```

O PPTX padrão tem uma imagem por slide (fiel ao desenho; as notas do apresentador vão junto). O `--editavel` gera
caixas de texto editáveis, mas troca as fontes do tema pelas do sistema: serve de ponto de partida, não de versão final.

## Editar

Tudo em `apresentacao.md`. Slides separados por `---`. Além do Markdown do Marp:

| Escreva | Vira |
|---|---|
| `{{n:chave}}` | número calculado de `tabelas_finais/` (`build/numeros.py`; `python apresentacao/build/numeros.py` lista todos) |
| `{{campo}}` | campo do cabeçalho do arquivo (`titulo`, `data`, `secretaria`, `url_site`...) |
| `![](fig:nome)` | figura do `analise.py`: a versão de impressão (`mapas/a4/`, `visualizacoes/a4/`, sem título embutido) ou, se faltar, a PNG; `fig:apres_*` = mapa só do deck (`build/mapas_apresentacao.py`) |
| `![](captura:site_desktop)` | captura do site ou do PDF (`site_desktop`, `site_celular`, `pdf_capa`, `pdf_pagina`) |
| `{{qr:url_site}}` | QR code da URL |
| `{{tabela:pendentes}}` | tabela de indicadores sem dado por eixo (de `specs/estrutura_eixos.md`) |
| `<!-- se: bloco -->…<!-- /se -->` | só entra se `bloco` está em `blocos:` do cabeçalho; `com_<campo>` liga sozinho quando o campo está preenchido |
| `<!-- fonte: texto -->` | rodapé "Fonte: texto" do slide |
| `<!-- revisar -->` | texto proposto pelo IPP, a revisar pela equipe (o build conta) |
| `<!-- texto livre -->` | nota do apresentador (vai para o PPTX) |

Classes de slide (`<!-- _class: x -->`): `capa`, `secao`, `numero`, `qr`, `encerramento`; blocos HTML `stats`, `lado`,
`dois` (`dois baixo`: figuras mais baixas), `hub`, `kicker`, `nota` (`nota forte`: nota em destaque), `grupo` +
`grupo-titulo` (caixas sob um título comum), `destaque` numa caixa de `stats` (ver `tema/ipp.css`).

Regras do texto (`specs/2026-09-29_slide_revision` §3): "até 72 meses" (nunca "0 a 5 anos" fora da nota de
equivalência), "primeira infância", "Zika de 2015-2016", 393 mil (Ripsa 2025) como população de referência, nenhum
mapa com terra azul, nota explicando todo tratamento de valores extremos.

## Variantes (outro público ou secretaria)

Copie `apresentacao.md` para `variantes/<nome>.md`, mude o cabeçalho (`secretaria`, `publico`, `blocos`, `data`) e
apague ou acrescente slides. Gere com `python apresentacao/build/gera_apresentacao.py variantes/<nome>.md`.
Exemplo: `variantes/exemplo_secretaria.md` (secretaria na capa, sem o roteiro de demonstração). O caminho é a partir da
raiz do repositório: `python apresentacao/build/gera_apresentacao.py apresentacao/variantes/<nome>.md`.

**Variante breve do eixo Inclusão** (`variantes/inclusao.md`, 8 slides, `specs/2026-10-06_deck_inclusao`): números `incl_*`
de `build/numeros.py` e o mapa `apres_cadunico_deficiencia_bairro`; publicada como
`apresentacao_primeira_infancia_inclusao.pptx/.pdf`. Rodapé longo no cabeçalho é seguro (o gerador não quebra mais a
linha do YAML, que fazia o Marp ignorar o tema).
