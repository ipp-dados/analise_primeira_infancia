# Validação — specs/recortes_cadunico

Marcar `[x]` com a evidência (comando, número, print). Os números de referência abaixo foram
**verificados no banco CTPE** (`ctpe.silver_cadunico_geral`, partição `2026-06-12`) na abertura da
rodada, em 2026-09-23. O código deve reproduzi-los. Se a partição mudar, os números mudam, e V0
detecta isso.

## V0 — Ambiente e baseline
- [x] Conexão via `.env` ok: 5 chaves presentes, PostgreSQL 15.12, schema `ctpe`, UTF8. *(abertura da rodada)*
- [x] Python base do Anaconda sem `psycopg` 3 → usar `analises_env` (`psycopg 3.3.4`, `geopandas 1.1.4`). *(abertura)*
- [ ] Checksums de `tabelas_finais/`, `visualizacoes/`, `mapas/` e `relatorio/*` gravados, com as contagens do HTML, PDF e DOCX.
- [ ] Seção CadÚnico sem alteração reproduz as 6 tabelas `cadunico_*` versionadas byte a byte (ou com diferença só de float/ordem, justificada).

## V1 — Totais de referência
- [ ] `grupo_idade='0-6'`: **194.138 crianças, 173.768 famílias**; `idade` ∈ {0,…,5}.
- [ ] Por idade: 0 = 11.328; 1 = 27.357; 2 = 33.116; 3 = 37.838; 4 = 41.312; 5 = 43.187.
- [ ] Sexo: F 94.778 / M 99.360 crianças; famílias com ≥1: F 89.463 / M 93.769 (não somar).
- [ ] Composição de sexo exclusiva (só meninas + só meninos + ambos) = 173.768; ambos = 183.232 − 173.768 = **9.464**.
- [ ] Raça/cor crianças: Parda 103.991, Branca 68.200, Preta 20.670, Amarela 1.208, Indígena 69; Negra = **124.661**; sem `NaN`.
- [ ] Renda per capita (crianças/famílias): 0-218 149.426/131.808; 219-810 33.435/30.948; 811-1621 9.742/9.511; 1621-3242 1.374/1.347; 3242+ 161/154.

## V2 — Arranjo familiar (proxy)
- [ ] Linhas por `id_familia` = `n_pessoas_familia` em 100% das famílias (divergências = 0).
- [ ] `grupo_renda_pct` único por família (asserção em `classifica_arranjo_familiar`).
- [ ] Famílias: Uma adulta 141.051; Dois adultos H+M 18.168; Dois adultos outra 6.377; Um adulto homem 3.944; 3+ adultos 3.515; Sem adulto 713. **Σ = 173.768**.
- [ ] Crianças 0-5 por arranjo: 158.437 / 20.042 / 6.932 / 4.147 / 3.834 / 746. **Σ = 194.138**.
- [ ] Arranjo × renda: Σ linhas = famílias do arranjo. Σ colunas = famílias da faixa (131.808 / 30.948 / 11.012 para 811+).
- [ ] Famílias sem adulto: distribuição da idade do membro mais velho registrada (só agregado).

## V3 — Bairro e geocodificação
- [ ] Crianças sem bairro (CEP fora de `lista_bairros.csv`): **15.809 (8,1%)**. Com bairro: 178.329.
- [ ] 178.329 = bairros oficiais + 380 em localidades sem bairro oficial (`_BAIRROS_CADUNICO_SEM_CORRESPONDENCIA`).
- [ ] Linha "Sem bairro identificado" presente em `cadunico_por_bairro_2026.csv`, e a soma de todas as linhas = 194.138.
- [ ] Join por `codbairro` (`junta_codbairro_por_bairro` sem erro). Bairros ausentes do CadÚnico (Vila Kennedy, Jabour, Gericinó, Ilha de Guaratiba, Lapa) aparecem como "Sem dado", não como 0.
- [ ] Taxas por bairro conferidas à mão em 3 bairros (um grande, um pequeno, um perto do limiar): Σ numerador ÷ Σ denominador.
- [ ] Nota de viés CEP→bairro presente nos 3 mapas novos e nos 3 mapas CadÚnico existentes (notebook, HTML, PDF).

## V4 — Privacidade (spec §5)
- [ ] Varredura automática: nenhuma célula sub-municipal < 20 (contagem ou denominador de taxa) em `tabelas_finais/cadunico_*` e `tabelas_finais/tabela_mapa_cadunico_*`.
- [ ] Mesma varredura nos `data-valor` e nos CSV embutidos dos cards CadÚnico de `relatorio/index.html`.
- [ ] Os 10 bairros < 20 crianças do baseline (entre eles Argentino, Campo dos Afonsos, Lagoa, Joá, Urca, Zumbi) aparecem como "suprimido (< 20)" no tooltip, não como "Sem dado".
- [ ] Nenhuma categoria de raça/cor publicada abaixo do nível município. Amarela e Indígena só no total da cidade.
- [ ] Arranjo × renda: nenhuma célula < 20 publicada.
- [ ] Nenhum arquivo novo em `dados_locais/` e nada de nível pessoa ou família gravado em disco (`git status` limpo fora das saídas esperadas).

## V5 — Convenções do projeto
- [ ] Toda visualização e mapa nova ou corrigida cita `fonte_cadunico_particao` (`'CadÚnico (extração CTPE, jun/2026)'`).
- [ ] Mapas de taxa com `bins=None` (colorbar contínua) e `cmap=_CORES_TEMA_MAPA['cadunico']` (`YlOrBr`); HTML com tema `cadunico`.
- [ ] Nenhuma taxa agregada por média ou soma de percentuais.
- [ ] Funções novas na seção 📦; células de análise só chamam essas funções.
- [ ] Nomes: tabelas `cadunico_*_2026.csv`, gêmea `tabela_mapa_cadunico_recortes_bairro_2026.csv`, mapas `mapa_percentual_cadunico_*_bairro_2026.png`.

## V6 — Correções A1-A8
- [ ] A3: nenhum título, legenda ou rótulo publicado diz "0-6" para dados CadÚnico (`grep` no HTML, PDF e notebook). Nomes de arquivo inalterados.
- [ ] A5 (D8): `cadunico_por_faixa_etaria_2026.csv` removido e nenhum leitor aponta para ele (`grep -r`).
- [ ] A2 (D6): se aprovada, o mapa % CadÚnico/Censo está ausente do HTML/PDF e presente no notebook com nota corrigida.
- [ ] A6/A7/A8: notas e rótulos de renda presentes.

## V7 — Relatórios
- [ ] HTML: os 3 itens de Inclusão viram cards reais (sem `emite_bloco_pendente` para eles). O restante do HTML fica idêntico ao baseline (diff estrutural), fora do bloco CadÚnico de Família e Cuidados.
- [ ] `mapa_svg` com `rotulo_nan` default: os outros ~30 mapas SVG ficam byte-idênticos ao baseline.
- [ ] PDF: 3 itens renderizados, mapas legíveis, sem página em branco nova. Contagem de páginas registrada.
- [ ] DOCX: 3 itens com texto semente, eixo Inclusão sem "Fazer recorte — Léo".
- [ ] Tamanho do HTML registrado (antes e depois).

## V8 — Execução completa
- [ ] `analise.py` do zero (kernel limpo, `analises_env`, top-to-bottom) sem erro.
- [ ] `jupytext --sync` ok; `.ipynb` não versionado.
- [ ] Revisão visual com o usuário. Registrar o que foi cortado (ex. mapa % meninas) em todos os artefatos.
