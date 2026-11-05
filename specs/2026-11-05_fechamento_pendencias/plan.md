# PLAN — Fechamento de pendências (2026-11-05)

Ordem pensada para regerar cada produto uma vez só: primeiro o que muda dados/figuras (`analise.py` e pacote), depois
o texto (que cita os números finais), por último site e PDF.

## B1 — SISVAN (R1)
- `primeira_infancia/limpeza.py`: `recalcula_percentuais_sisvan(df, categorias)` → para cada `<cat>_bruto`, grava
  `<cat>_percentual = bruto / total × 100` (float), e avisa quando a coluna da origem diverge mais de 0,1 p.p.
  (registro, não erro). Exportada em `__all__`.
- `analise.py`, seção SISVAN: troca os `convert_numeric_safe` das colunas `_percentual` pela função; as colunas
  derivadas (`Percent. baixo peso total`, `Percent. sobrepeso total`) seguem iguais. Rodar só a seção.
- Conferir os textos `sisvan_*` em `textos_curados.json` e nas notas `nota-curadoria` do `analise.py`.

## B2 — Cores (R6)
- `estilo.py` e `build_site.py` (`_CMAP_TEMA`); comentários. Rodar `analise.py` completo **depois** de B1 e B3
  (uma execução só), com `GERA_VARIANTE_A4`.
- Conferência automática: para cada PNG de mapa em `mapas/` e `mapas/a4/` e cada `fill` dos mapas no site, nenhum
  pixel/cor de polígono com matiz em 190°-250° (azul), exceto o fundo.

## B3 — Mapas de número em Moradia (R2)
- `analise.py`, seção CadÚnico/Moradia: 2 chamadas a `mapa_coropletico_bairros` lendo as `tabela_mapa_*` existentes,
  como as do deck (`apresentacao/build/mapas_apresentacao.py`, só como referência; o deck não muda).
- `specs/estrutura_eixos.md`: `- mapa:` novo antes do de % nos 2 indicadores.
- `build_site.py`: `mapa_svg` dos 2 mapas (classes discretas, `col_agregado` sem cor).

## B4 — ISP (R5)
- Depois do OK do usuário sobre P1: busca por `IPS`/`Índice de Progresso Social` (não por `ips` em minúsculas, que pega
  `chips`, `tips`...) e troca caso a caso, nos arquivos listados em R5.

## B5 — PDF (R3)
- `tabelas.py` e `fontes.bib`; `python relatorio/latex/build/gera_latex.py` (sem `--publicar`); conferir as páginas
  novas em PNG.

## B6 — Textos (R8)
1. Listar as chaves sem texto curado em Inclusão e Moradia (o site de `staging_main` mostra lorem nelas).
2. Rascunhar cada texto com números lidos de `tabelas_finais/` por um script de conferência (no scratchpad), no
   estilo dos textos de Família e Cuidados (vizinhos e do mesmo CadÚnico).
3. Mostrar ao usuário (uma tabela, perguntas agrupadas); aplicar só o aprovado em `textos_curados.json` e
   `controle_revisao.json`.

## B7 — Regerar e conferir
- Site: `python website/build/build_site.py` + `website/build/confere_textos.py`; Playwright desktop e celular nos
  eixos Inclusão, Moradia, Alimentação, Direito ao Brincar e Visão geral (cores).
- PDF: já em B5; regerar depois de B6.

## B8 — Documentação e fechamento
- `ROADMAP.md` (R9), `CLAUDE.md` (cores, decks), `docs/especificacao_projeto.md` (§11), skill `generate_map`
  (cores), `specs/exclusoes.md` (nada sai nesta rodada; só conferir), `validation.md`.
- Commits `SPEC-FechamentoPendencias: Bloco N -- ...`; merge `--no-ff` em `staging_main` com OK do usuário; tag
  `rodada/fechamento_pendencias`. **Sem** merge na `demo` e **sem** deploy.
