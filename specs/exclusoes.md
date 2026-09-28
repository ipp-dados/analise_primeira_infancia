# Lista de exclusões

> Registro único do que foi **tirado** (ou agregado) do relatório PDF, do site e/ou do `analise.py` por decisão
> da equipe — o quê, onde, por quê, quando e como voltar atrás. Editado à mão, como `specs/estrutura_eixos.md`.
> Pedido do usuário (2026-09-25): "keep track of those decisions in a excluded list". A análise que embasou os
> itens E1-E12 está em `specs/2026-09-25_relatorio_latex/sugestoes_omissao.md` (códigos A1-D).
>
> Onde cada produto aplica a exclusão:
> - **PDF e DOCX** — `specs/estrutura_eixos.md` (o arquivo sai da subseção, com uma `nota:`) ou, só para tabelas
>   do apêndice, `SUBSTITUI_NO_PDF` em `relatorio/latex/build/tabelas.py`;
> - **site** — `website/build/build_site.py` (agrupamento fixo no código). Aplicado em 2026-09-25 pela rodada
>   `specs/2026-09-25_website_graficos` (branch `spec/website-graficos`; `_subgrupo_excluido()` no gerador, mesma
>   regra de `analise.py`);
> - **figuras** — `analise.py`, seção de funções auxiliares (`subgrupo_excluido`, `agrupa_racas_raras`); as PNGs
>   só mudam na próxima execução completa do notebook.
>
> Mantido à parte (decisão explícita de **não** excluir): lesão autoprovocada 0-5 anos (sinaliza mudança no
> registro); % de óbitos evitáveis por CAP de 1 a 4 anos; séries de causas evitáveis por faixa etária (0-6, 7-27,
> 28-364 dias); taxas de mortalidade neonatal por bairro (não há versão por CAP/AP/RP — manter o bairro).

| Código | O quê | PDF | Site | `analise.py` | Por quê | Decisão | Como voltar |
| :-- | :--- | :-: | :-: | :-: | :--- | :-- | :--- |
| E1 | 10 arquivos gerados por chamadas **comentadas** em `analise.py` (**arquivos apagados do repositório em 2026-09-25**, a pedido do usuário; os textos curados de 4 deles seguem no apêndice "Textos órfãos" do DOCX) (mapas de óbitos na gravidez, no puerpério, neonatal tardio e pós-neonatal por bairro; `cobertura_vacinal_epi_ano`; 4 gráficos e 1 tabela de causas evitáveis por raça/cor) | sai | — (o site desenha a partir dos CSVs atuais) | — | o PNG no disco é antigo | 2026-09-25 (D6) | descomentar a chamada, rodar o notebook, devolver a linha em `estrutura_eixos.md` |
| E2 | Subgrupos **1.2.1 gestação, 1.2.2 parto e 1.2.3 recém-nascido** em óbitos de **1 a 4 anos** | sai | aplicado | sai | 22, 6 e 4 óbitos em 20 anos na cidade inteira; causa perinatal aos 1-4 anos indica erro de registro ou codificação (A1) | 2026-09-25 | tirar o caso de `subgrupo_excluido()` (`analise.py`) e de `_subgrupo_excluido()` (site) |
| E3 | Subgrupo **1.1 reduzível por imunização**, todas as faixas | sai | aplicado | sai | 0 a 2 óbitos por ano (38 em 30 anos, menores de 1 ano) (A2) | 2026-09-25 | idem E2 |
| E4 | **Mapas de óbitos maternos por bairro** (gravidez e puerpério) | já fora (E1) | aplicado | — | 0 a 3 óbitos por bairro; sem padrão territorial (A4) | 2026-09-25 | devolver as entradas em `build_site.py` |
| E5 | **Raça/cor amarela e indígena** separadas nas séries de óbitos de menores de 1 ano | agrega | aplicado | agrega | 0 a 2 óbitos por ano cada; picos sem significado no gráfico de % (B3). Viram "Amarela e indígena", com o % recalculado a partir dos absolutos (constituição §3) | 2026-09-25 | `agrupa_racas_raras()` sem efeito / reverter no site |
| E6 | **Taxa de violência familiar por bairro** (mapas e colunas de taxa) | sai | aplicado | — | bairros com poucas crianças: Joá 500‰; a taxa fica por RA (B4). A contagem por bairro continua | 2026-09-25 | devolver as linhas `mapa:` e as colunas de taxa |
| E7 | **Cobertura vacinal, anos selecionados** (gráfico e tabela) | sai | aplicado | — | repete 4 anos da série anual (C1) | 2026-09-25 | devolver em `estrutura_eixos.md` e no site |
| E8 | **Frequência escolar em números absolutos por raça/cor e por sexo** (Censo 2022) | sai | aplicado | — | a taxa por idade é o dado comparável (C3); o total absoluto continua | 2026-09-25 | idem E7 |
| E9 | **Mapas de contagem de óbitos por bairro** ao lado do mapa de taxa (neonatal precoce, tardia, pós-neonatal, infantil; raça/cor total) | sai (fica a taxa) | aplicado: **alternância Taxa ↔ Óbitos** no mesmo cartão | — | a contagem reproduz onde nascem mais crianças (C4) | 2026-09-25 | devolver as linhas `mapa:`; no site, desfazer o seletor |
| E10 | **Tabelas repetidas no apêndice do PDF** (bairro/CAP/RA, violência, causas evitáveis, frequência, vacina, CadÚnico) | funde/omite | — | — | mesma informação em várias tabelas | 2026-09-25 | `SUBSTITUI_NO_PDF` em `tabelas.py` |
| E11 | Tabelas com mais de 200 linhas | só digital | — | — | não cabem no papel; bairro × ano vira só o último ano | 2026-09-25 | `MAX_LINHAS_PDF` em `tabelas.py` |
| E12 | **Amarela e indígena** na taxa de frequência escolar por raça/cor (Censo 2022, `sidra_taxa_frequencia_0_6_raca_2022`) | **pendente** | **pendente** | **pendente** | grupos pequenos: taxas de 100% em várias idades (mesmo caso de E5) | 2026-09-25: agregar, **na próxima rodada** | — |
