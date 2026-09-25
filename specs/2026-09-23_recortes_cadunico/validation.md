# Validação — specs/2026-09-23_recortes_cadunico

Marcar `[x]` com a evidência (comando, número, print). Os números de referência abaixo foram
**verificados no banco CTPE** (`ctpe.silver_cadunico_geral`, partição `2026-06-12`) na abertura da
rodada, em 2026-09-23. O código deve reproduzi-los. Se a partição mudar, os números mudam, e V0
detecta isso.

## V0 — Ambiente e baseline
- [x] Conexão via `.env` ok: 5 chaves presentes, PostgreSQL 15.12, schema `ctpe`, UTF8. *(abertura da rodada)*
- [x] Python base do Anaconda sem `psycopg` 3 → usar `analises_env` (`psycopg 3.3.4`, `geopandas 1.1.4`). *(abertura)*
- [x] Checksums de `tabelas_finais/`, `visualizacoes/`, `mapas/` e `relatorio/*` gravados, com as contagens do HTML, PDF e DOCX. *(2026-09-23: 180 arquivos em `scratchpad/baseline/sha256.txt`; HTML 20.331.573 bytes, 7 `<h2`, 24 `<h3`, 65 `map-svg-card`; PDF 44,3 MB; DOCX 5,7 MB)*
- [x] Seção CadÚnico sem alteração reproduz as 6 tabelas `cadunico_*` versionadas byte a byte (ou com diferença só de float/ordem, justificada). *(2026-09-23: `analise.py` linhas 1-1369 no `analises_env`, **6/6 idênticas** (`cmp`). Efeito colateral fora do escopo: `dados_locais/tratados/{sobrepeso,desnutrição}.csv` mudam de **ordem de linhas** a cada execução, porque `limpa_dados_sisvan` usa `Path.iterdir()`, cuja ordem depende do SO. Nenhum valor muda, e os arquivos foram restaurados. Os PNG também mudam de bytes ao ser re-renderizados, sem mudança visual.)*

## V1 — Totais de referência
- [x] `grupo_idade='0-6'`: **194.138 crianças, 173.768 famílias**; `idade` ∈ {0,…,5}; `data_nascimento` de 2020-08-12 a 2026-06-05.
- [x] Definição de idade verificada (2026-09-23): crianças de 6 anos estão no grupo `'7-14'` (idade 6-8, nascidos de 2017-08-13 a 2020-08-11), e a `idade` é calculada em ~2026-08-12, não na partição. Nota no notebook (A3).
- [x] Por idade: 0 = 11.328; 1 = 27.357; 2 = 33.116; 3 = 37.838; 4 = 41.312; 5 = 43.187.
- [x] Sexo: F 94.778 / M 99.360 crianças; famílias com ≥1: F 89.463 / M 93.769 (não somar).
- [x] Composição de sexo exclusiva (só meninas + só meninos + ambos) = 173.768; ambos = 183.232 − 173.768 = **9.464**.
- [x] Raça/cor crianças: Parda 103.991, Branca 68.200, Preta 20.670, Amarela 1.208, Indígena 69; Negra = **124.661**; sem `NaN`.
- [x] Renda per capita (crianças/famílias): 0-218 149.426/131.808; 219-810 33.435/30.948; 811-1621 9.742/9.511; 1621-3242 1.374/1.347; 3242+ 161/154.

## V2 — Arranjo familiar (proxy)
*Evidência (2026-09-23): asserções de `classifica_arranjo_familiar` e da célula de carga passaram (173.768 famílias, 194.138 crianças, 521.993 pessoas); tabelas `cadunico_familias_por_arranjo_2026.csv` e `..._arranjo_renda_2026.csv` batem com os números abaixo. Sem adulto: 554 com o membro mais velho de 16-17 anos, 85 só com crianças de até 5 anos (nota no notebook).*
- [x] Linhas por `id_familia` = `n_pessoas_familia` em 100% das famílias (divergências = 0).
- [x] `grupo_renda_pct` único por família (asserção em `classifica_arranjo_familiar`).
- [x] Famílias: Uma adulta 141.051; Dois adultos H+M 18.168; Dois adultos outra 6.377; Um adulto homem 3.944; 3+ adultos 3.515; Sem adulto 713. **Σ = 173.768**.
- [x] Crianças 0-5 por arranjo: 158.437 / 20.042 / 6.932 / 4.147 / 3.834 / 746. **Σ = 194.138**.
- [x] Arranjo × renda: Σ linhas = famílias do arranjo. Σ colunas = famílias da faixa (131.808 / 30.948 / 11.012 para 811+).
- [x] Famílias sem adulto: distribuição da idade do membro mais velho registrada (só agregado).

## V3 — Bairro e geocodificação
*Evidência: `assert` do total por bairro = 194.138 (linha "Sem bairro identificado" = 15.809 crianças / 14.159 famílias). Conferência à mão: Bangu 3.763/7.705 = 48,8% meninas; Rocinha 915/1.125 = 81,3% uma adulta; Copacabana 877/1.127 = 77,8%.*
- [x] Crianças sem bairro (CEP fora de `lista_bairros.csv`): **15.809 (8,1%)**. Com bairro: 178.329.
- [x] 178.329 = bairros oficiais + 380 em localidades sem bairro oficial (`_BAIRROS_CADUNICO_SEM_CORRESPONDENCIA`).
- [x] Linha "Sem bairro identificado" presente em `cadunico_por_bairro_2026.csv`, e a soma de todas as linhas = 194.138.
- [x] Join por `codbairro` (`junta_codbairro_por_bairro` sem erro). Bairros ausentes do CadÚnico (Vila Kennedy, Jabour, Gericinó, Ilha de Guaratiba, Lapa) aparecem como "Sem dado", não como 0.
- [x] Taxas por bairro conferidas à mão em 3 bairros (um grande, um pequeno, um perto do limiar): Σ numerador ÷ Σ denominador.
- [x] Nota de viés CEP→bairro presente nos 3 mapas novos e nos 3 mapas CadÚnico existentes (notebook, HTML, PDF).

## V4 — Privacidade (spec §5)
*Evidência: varredura automática sem nenhuma célula < 20 visível nos CSV `cadunico_*`/`tabela_mapa_cadunico_*` nem nos `data-valor` dos 8 mapas CadÚnico do HTML; 89 tooltips "suprimido (< 20)"; 10 bairros suprimidos no mapa 0-6 e 11 no 0-4 (Praia da Bandeira sai pelo denominador do Censo); arranjo × renda: 1 célula suprimida (Sem adulto × acima de 1/2 SM, 7 famílias).*
- [x] Varredura automática: nenhuma célula sub-municipal < 20 (contagem ou denominador de taxa) em `tabelas_finais/cadunico_*` e `tabelas_finais/tabela_mapa_cadunico_*`.
- [x] Mesma varredura nos `data-valor` e nos CSV embutidos dos cards CadÚnico de `relatorio/index.html`.
- [x] Os 10 bairros < 20 crianças do baseline (entre eles Argentino, Campo dos Afonsos, Lagoa, Joá, Urca, Zumbi) aparecem como "suprimido (< 20)" no tooltip, não como "Sem dado".
- [x] Nenhuma categoria de raça/cor publicada abaixo do nível município. Amarela e Indígena só no total da cidade.
- [x] Arranjo × renda: nenhuma célula < 20 publicada.
- [x] Nenhum arquivo novo em `dados_locais/` e nada de nível pessoa ou família gravado em disco (`git status` limpo fora das saídas esperadas).

## V5 — Convenções do projeto
- [x] Toda visualização e mapa nova ou corrigida cita `fonte_cadunico_particao` (`'CadÚnico (extração CTPE, jun/2026)'`).
- [x] Mapas de taxa com `bins=None` (colorbar contínua) e `cmap=_CORES_TEMA_MAPA['cadunico']` (`YlOrBr`); HTML com tema `cadunico`.
- [x] Nenhuma taxa agregada por média ou soma de percentuais.
- [x] Funções novas na seção 📦; células de análise só chamam essas funções.
- [x] Nomes: tabelas `cadunico_*_2026.csv`, gêmea `tabela_mapa_cadunico_recortes_bairro_2026.csv`, mapas `mapa_percentual_cadunico_*_bairro_2026.png`.

## V6 — Correções A1-A8
- [x] A3 (D7 adiada): títulos existentes **inalterados** (diff). Nota de definição de idade presente no notebook. Saídas novas com "até 6 anos" + nota "0 a 5 anos completos".
- [x] A5 (D8): `cadunico_por_faixa_etaria_2026.csv` removido e nenhum leitor aponta para ele (`grep -r`, incluindo `README.md`).
- [x] A2 (D6, aprovada): o mapa % CadÚnico/Censo está ausente do HTML/PDF e presente no notebook com nota corrigida.
- [x] A6/A7/A8: notas e rótulos de renda presentes.

## V7 — Relatórios
*Evidência: HTML 20.331.573 → 21.478.148 bytes; `<h3` 24 → 27; `map-svg-card` 65 → 69; os 40 títulos de mapa não CadÚnico ficam byte-idênticos ao baseline (commit 9091d97). Removido: "% ... CadÚnico sobre o Censo"; adicionados os 3 mapas de taxa. Gráficos novos renderizados no DOM (Edge headless `--dump-dom`). PDF 122 → 129 páginas, sem página em branco, páginas novas e apêndice inspecionados. DOCX: 49 subseções, 104 imagens, 112 bookmarks (1 órfão = texto do mapa removido).*
- [x] HTML: os 3 itens de Inclusão viram cards reais (sem `emite_bloco_pendente` para eles). O restante do HTML fica idêntico ao baseline (diff estrutural), fora do bloco CadÚnico de Família e Cuidados.
- [x] `mapa_svg` com `rotulo_nan` default: os outros ~30 mapas SVG ficam byte-idênticos ao baseline.
- [x] PDF: 3 itens renderizados, mapas legíveis, sem página em branco nova. Contagem de páginas registrada.
- [x] DOCX: 3 itens com texto semente, eixo Inclusão sem "Fazer recorte — Léo".
- [x] Tamanho do HTML registrado (antes e depois).

## V8 — Execução completa
*Evidência: `analise.py` inteiro no `analises_env` (runner com `load_dotenv(".env")` explícito), exit 0 em ~3 min; saídas CadÚnico versionadas idênticas às commitadas; `jupytext --to notebook` ok. Ruído fora do escopo: `limpa_dados_sisvan` muda a ordem das linhas de `dados_locais/tratados/*.csv` e `sisvan_*_por_ano.csv` a cada execução (ordem de `Path.iterdir()`), revertido.*
- [x] `analise.py` do zero (kernel limpo, `analises_env`, top-to-bottom) sem erro.
- [x] `jupytext --sync` ok; `.ipynb` não versionado.
- [x] Revisão visual com o usuário. Registrar o que foi cortado (ex. mapa % meninas) em todos os artefatos. *(2026-09-23: mapa % meninas cortado. HTML 67 `map-svg-card`, PDF 128 páginas sem o mapa, DOCX 103 imagens; 2º bookmark órfão = texto do mapa cortado.)*
