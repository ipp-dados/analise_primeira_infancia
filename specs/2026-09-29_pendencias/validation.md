# VALIDATION — Pendências

Critérios de aceite; a coluna "Resultado" é preenchida ao fim da implementação (T8.3).

## Planejamento (2026-09-29)

| Verificação | Resultado |
|---|---|
| Mapas de taxa de mortalidade infantil 2025 (cartão neonatal × raça/cor) | **OK, iguais**: 167 × 167 códigos, diferença máxima 7e-15 |
| Deploy do site depois do merge | **OK**: `deploy-relatorio.yml` em `ab9f803` (2026-09-29 13:00 UTC, sucesso) |
| PDF publicado × estrutura atual | **desatualizado**: último `--publicar` em `17cae4a` (melhorias_site), antes da `nova_estrutura` |
| Cabeçalhos de cache do site no ar (D13) | **OK, nada a fazer**: `/`, `css/main.css?v=…`, `assets/images/ipp-logo.png`, `favicon.ico` com `expires`, `Cache-Control: max-age=600`, `ETag`, `Last-Modified` (curl, 2026-09-29) |

## Implementação

| # | Verificação | Critério | Resultado |
|---|---|---|---|
| V1 | Saídas de `analise.py` não tocadas | hash idêntico antes × depois, fora da lista de saídas alteradas desta rodada || **OK** para PNG e CSV (bytes): execução completa antes × depois (`analise_env`), 302 → 305 arquivos; mudaram só os previstos — 8 PNG (população Censo raça/sexo, Ripsa × 2, baixo peso, taxa por raça/cor, taxa de frequência raça/sexo) e 5 CSV; 3 novos (`sidra_taxa_frequencia_0_5_total_2022` CSV/PNG/A4). As PDFs A4 e os `.xlsx` têm data de criação embutida e mudam a cada execução — não comparáveis por bytes (as PDFs de antes não foram guardadas); mesmo código e dados das PNG idênticas |
| V2 | Mapa duplicado (R1) | site: cartão neonatal com 3 pills nos dois modos; PDF sem `mapa_taxa_mortalidade_infantil_bairro_2025`; E13 escrito || **OK**: seeds do site 113 → 111 (saíram `mapa_taxa_mortalidade_infantil_bairro_2025` e `mapa_mortalidade_infantil_bairro_2025`; `pnad_…` trocado por `sidra_taxa_frequencia_0_5_total_2022`, E15); PDF sem o mapa; E13 escrito |
| V3 | "Não informada" (R2) | gráfico de taxa com 4 séries no site, na PNG e no A4; contagem com 5; nota presente; E14 escrito || **OK**: 4 séries na taxa (site, PNG, A4), 5 na contagem; nota na fonte e na legenda do PDF (manifesto A4); E14 escrito |
| V4 | Eixo cortado (R3) | só o baixo peso com eixo cortado, barras inclinadas e nota nos 3 lugares; nenhum outro gráfico mudou (V1) || **OK**: marca de corte e nota na PNG de tela, no A4 (legenda do PDF) e no site (`eixoCortado`); nenhum outro gráfico mudou (V1) |
| V5 | Taxa de frequência 0-5 (R4) | recalculada dos absolutos (plano); diferença para a 10056, idade a idade, registrada; "Amarela e indígena" e "Total" 0-5 presentes || **Método trocado (D14)**: 10057 ÷ 9606 passava de 100% (Amarela 106,9%, homens 100,2% aos 5 anos) e ficava até 10,7 p.p. longe da 10056 (preta 3 anos) — as tabelas vêm de bases diferentes. Adotado: taxa publicada (10056) por grupo e idade, agregados por taxa × população (9606): total 0-5 = 59,30%; amarela e indígena 62,82% (só no total, D15); nenhum valor > 100% (assert em `analise.py`) |
| V6 | Faixa 0-5 (R4) | nenhum gráfico, rótulo ou número publicado (site, PDF gerado, deck) com 6 anos sem nota || **OK**: PDF gerado sem "6 anos" fora de nota (capa, folha de rosto e "Como ler" corrigidas); site: 3 menções, todas notas explicativas (CadÚnico e INEP); deck: só a nota de 469 mil (D17); textos curados: nenhuma |
| V7 | Tablet (R5) | 768, 800 e 1024 px: alvos ≥ 44 px, texto dos gráficos ≥ 11 px, sem rolagem horizontal || **OK** em 768, 800 e 1024 px, 8 abas: 0 alvos < 44 px, menor texto de gráfico 11 px (antes 9,5), 0 px de rolagem horizontal |
| V8 | Desktop (R5) | 1440 e 1100 px pixel a pixel iguais à linha de base, fora dos cartões alterados em R1-R4 || **OK**: 1440 e 1100 px iguais nas abas sem mudança de conteúdo (Inclusão, Moradia, Proteção), fora a sombra da barra de abas (estado de rolagem na captura); nas demais, só os cartões alterados (Direito ao Brincar: nota do IPS "0 a 5 anos") |
| V9 | Celular | 390 px sem regressão (capturas antes × depois) || **OK**: 390 px — Inclusão, Moradia e Proteção pixel a pixel iguais; demais só onde o conteúdo mudou; 0 alvos < 44 px, texto ≥ 11,5 px, sem rolagem horizontal |
| V10 | PDF | compila; 0 `undefined`; 93 figuras (94 − 1 mapa), 43 tabelas, nenhuma outra a menos; overfull só os já aceitos || **OK**: compila; 0 `undefined`; 158 páginas; 94 → 93 figuras (saíram o mapa duplicado e o "PNAD", entrou a taxa total do Censo); 43 × 43 tabelas; overfull > 5 pt: 14, os já aceitos; não publicado (`--publicar` só com OK) |
| V11 | Site | inventário: nenhuma seed/figura a menos além de R1; `index.html` < 1 MB, site < 2 MB || **OK**: `index.html` 347 KB; site 1,07 MB; seeds conforme V2 |
| V12 | Deck (R7) | compila; slide com o mapa de raça/cor; rótulos 0-5 || **OK**: 30 slides, 6 trechos `revisar` (os mesmos); âncora 393 mil (0 a 5, Ripsa 2025) com nota de 469 mil; mapa de raça/cor no slide de mortalidade; "54% das crianças de 0 a 5 anos são negras"; não publicado |
| V13 | Textos (R8) | trechos ajustados listados; marcados `revisar`; `valida_textos_publicados.py` sem frase ausente || **OK**: ajustados e marcados `revisar` — `percentual_mortalidade_raca_ano`, `sidra_taxa_frequencia_0_6_raca_2022`, `sidra_taxa_frequencia_0_6_sexo_2022`, `censo_sidra_populacao_0_6_raca_2022`, `censo_sidra_populacao_0_6_sexo_2022`, `sidra_taxa_frequencia_0_5_total_2022` (herdado do "PNAD"); `nascidos_abaixo_peso_percentual_por_ano` não cita a escala, ficou igual; 2 alertas da 10056 resolvidos; `valida_textos_publicados.py`: 0 frases ausentes; DOCX: 51 subseções, 93 imagens, 0 bookmarks órfãos |
| V14 | Documentação (R6, R9, R10) | exclusões E12-E14, constituição, `CLAUDE.md`, CHANGELOG, ROADMAP, especificação do projeto atualizados || **OK**: `specs/exclusoes.md` E12 (aplicado), E13-E15; constituição §3 (faixa 0-5, base zero, agregação de taxas publicadas) e §5; `CLAUDE.md`; `relatorio/specs.md` v12; `auditoria_faixas.md` §8; CHANGELOG, README, ROADMAP, `docs/especificacao_projeto.md` |

## Achados e efeitos colaterais da execução (2026-09-29)

- **Banco do CadÚnico:** a tabela `silver_cadunico_geral` saiu do esquema `ctpe` (hoje em `public`); a consulta de
  `carrega_cadunico_familias_0_6` (`primeira_infancia/cadunico.py`) dava erro e foi corrigida para o nome sem esquema,
  como a consulta principal de `analise.py`. O banco também tem **extração nova**: as saídas do CadÚnico versionadas
  mudam um pouco (ex.: 11.328 → 11.254 crianças de 0 ano) — atualização de dado, não desta rodada.
- **Fundo cartográfico do site:** `basemap-04b5f5ec.jpg` → `basemap-f5a7b7b6.jpg`, **mesmos bytes**; o nome vem da
  bbox arredondada a 4 casas, que mudou na 4ª casa neste ambiente. O antigo, sem referência, foi apagado.
- **Gráficos e mapas de causas evitáveis por CAP:** versões versionadas diferem das de hoje só por renderização
  (2 px de largura, mesmo conteúdo) — ambiente diferente do da rodada `nova_estrutura`.
- **Ambiente:** instalados, fixados em `requirements*.txt`, `matplotlib-scalebar` no `analises_env`, `svgelements` e
  `playwright` no Anaconda base, e `npm ci` em `apresentacao/` (sem `node_modules`, o `npx marp` buscava um pacote
  inexistente). O Chrome não está instalado: capturas com o Edge (`channel="msedge"`).
- **Heredoc do Git Bash** come barras invertidas em scripts Python inline (duas viram uma): scripts com regex foram
  escritos em arquivo.
