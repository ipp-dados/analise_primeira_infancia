# Validação — `specs/2026-09-28_website_bugfix`

Resultados de 2026-09-28. Os scripts Playwright de captura e auditoria ficaram no scratchpad da sessão; a conferência de
textos é versionada (`website/build/confere_textos.py`).

- [x] V1 `build_site.py` sem `AVISO`; index 0,77 MB, site 1,36 MB; duas execuções seguidas dão o mesmo md5 de
      `index.html` e `data/*`
- [x] V2 Cache: todo `css/`, `js/` e `data/` do `index.html` com `?v=<hash>`. Servido por `http.server` no caminho
      `/analise_primeira_infancia/`: 0 requisições falhas
- [x] V3 Reprodução do bug: HTML novo + CSS/JS de `2e9279b` → botão sem estilo, texto da 1ª pill preso,
      `pm is not defined`. Com as versões nas URLs, esse par não pode mais se formar depois de um deploy
- [x] V4 Pills: 45 cartões, 110 estados (todas as pills, e cada modo Taxa|Óbitos): em cada um, exatamente 1 texto
      visível, o painel certo e o SVG com tamanho > 50 px — 0 falhas
- [x] V5 Alternância Taxa|Óbitos mantém a pill e troca o texto (Óbitos · Tardia → `mapa_obitos_neonatal_tardia_bairro_2025`)
      em Chromium, Firefox e WebKit, por `file://` e por `http.server`; botão ativo `rgb(0, 74, 128)` (azul-marinho)
- [x] V6 Sem erro de JavaScript em nenhuma aba, nas larguras 1400/1000/760/420 px
- [x] V7 Sem rolagem horizontal da página a 420 px em nenhuma das 7 abas (antes: 424-460 px, por causa das URLs das Fontes)
- [x] V8 A ≤ 1100 px, sem sumário/progresso e com o conteúdo na largura toda; a 760 px, pills acima do gráfico e mapa
      com o texto embaixo (texto visível; antes tinha altura 0); a 420 px, banner empilhado e botões acima do título do mapa
- [x] V9 Cores: "Total" laranja × "Meninos" azul × "Meninas" rosa (antes Total = Meninos); eixo x dos Censos mostra
      2000, 2010 e 2022
- [x] V10 Barras de 10 bairros (Proteção): rótulos inclinados, sem sobreposição
- [x] V11 Textos (`conferencia_textos_site.csv`, 121 linhas): **54 OK** (texto do site = JSON = DOCX), **59 PENDENTE**
      (sem texto na curadoria, lorem), **0 ERRO**, **8 NÃO PUBLICADO** com o motivo: E4 (2 mapas), E7 (1),
      raça/cor D6 (4) e `obitos_evitaveis_total_cap_ano`, figura que nunca entrou no site (decisão da equipe).
      Os 3 textos `percentual_evitaveis_cap_*_ano` passaram de não publicados a OK
