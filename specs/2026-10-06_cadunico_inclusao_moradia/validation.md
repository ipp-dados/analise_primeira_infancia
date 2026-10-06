# VALIDATION — CadÚnico: pipeline novo para Inclusão e Moradia

## Planejamento (2026-10-06)

| Verificação | Resultado |
|---|---|
| Partição das tabelas CadÚnico do CTPE | todas 2026-07-10 |
| `silver_cadunico_geral` com `grupo_idade='0-6'` | **0 linhas** (grupo agora `'0-5'`, A1) |
| Crianças `'0-5'` (geral e pessoas) | 200.784 nas duas; 178.838 famílias |
| Crianças 0-5 com deficiência | 7.919 (4,0%); dado pontual 0-6: 25.995 (A2) |
| Crianças 0-5: inadequação / déficit / adensamento (Sim) | 11.589 / 86.393 / 101.477 |
| Bairros que passam sozinhos (num. e compl. ≥ 20) | deficiência 58%, inadequação 59%, adensamento 89%, déficit 90% |
| Ponte CEP → bairro: cobertura das crianças; código fora da camada oficial | 90,9%; nenhum |

## Implementação

Critérios de aceite; "Resultado" preenchido ao fim.

| # | Critério | Resultado |
|---|---|---|
| V1 | `analise.py` roda do zero sem erro, com a seção CadÚnico não vazia | OK — `python analise.py` (analises_env, MPLBACKEND=Agg) exit 0; 1ª execução parou em mais 2 mudanças da silver (achados A7/A8 abaixo), corrigidas |
| V2 | Totais do município das tabelas novas batem com o levantamento acima e com `gold_cadunico_indicadores` | OK — 200.784 crianças/178.838 famílias; deficiência 7.919; déficit 86.393/75.681; inadequação 11.589/10.266; adensamento 101.477/84.035 = `gold_cadunico_indicadores` |
| V3 | Nenhuma saída por bairro com contagem < 20 (numerador, complemento ou base) fora de conjunto | OK — deficiência: 69 bairros em 14 conjuntos; inadequação: 67 em 11; adensamento: 18 em 4; 0 suprimidos |
| V4 | Percentuais calculados de absolutos, sem "Não informado"/"Não se aplica" na base; base publicada | OK — `sim_base` (só Sim/Não na base); colunas `Base` nas CSVs |
| V5 | Toda figura nova cita a fonte com a partição (jul/2026) e, nos mapas, a regra de bairros somados | OK — fonte "CadÚnico (extração CTPE, jul/2026)"; rodapé dos mapas em 3 linhas (a 1ª versão invadia a atribuição do basemap) |
| V6 | Mapas de % com escala contínua; join por `codbairro` | OK — `bins=None`; `codbairro` da ponte, nomes da camada oficial |
| V7 | Crosswalk: 6 itens em Inclusão/Moradia, nenhum `pendente`, nenhum `dado_pontual` | OK — 3 + 3 itens, sem `status: pendente` nem `dado_pontual`; `gera_latex.py --sem-pdf` aceita o crosswalk (exit 0, `gerado/` restaurado: PDF fora da rodada) |
| V8 | Site de `staging_main`: blocos novos com lorem; sem `data-dado-pontual`; desktop e celular conferidos; orçamento | OK — 6 seções, lorem nos textos novos, 0 `data-dado-pontual`, 1,43 MB publicados (gzip 720 KB); desktop conferido em captura. Celular: captura headless corta a largura em todas as abas (inclusive as não alteradas) — blocos novos usam só componentes já cobertos por `mobile.css` |
| V9 | `demo`: faixa com 13 de outubro de 2026 e atualização de conteúdo; nota nas abas; build sem lorem/pendente | |
| V10 | PDF da `demo`: página de aviso com a nova data; demais páginas iguais | |
| V11 | Nada da `demo` em `staging_main` (merge só de ida) | |

## Para a rodada de textos (D5)

Textos curados que citam números do CadÚnico de jun/2026 (status a revisar):
- `cadunico_criancas_por_idade`: 11.328 crianças de 0 anos → **15.415**; 43.187 de 5 anos → **43.242** (jul/2026).
- Textos provisórios da `demo` com números do CadÚnico: atualizados na própria `demo` (D8).
- Notas técnicas de `analise.py` com números de jun/2026 (famílias sem adulto 713, CEPs fora da lista 15.809, nota de
  curadoria por idade) ficam como registro datado; a rodada de textos revisa.

## Achados da implementação

- **A7** — faixas de renda (`grupo_renda_pct`) com rótulos novos (`'até 218'`, `'218,01 a 810'`…): o gráfico de renda saía
  vazio. `normaliza_renda_cadunico` devolve os códigos de sempre e para em faixa desconhecida.
- **A8** — `id_pessoa` deixou de ser chave (150.691 distintos em 200.784 crianças; 1 vazio na tabela): a conferência de
  tamanho de família contava `id_pessoa`; passou a contar linhas. Contagens de crianças não mudam (nenhum vazio entre elas).
- **A9** — Alto da Boa Vista: 44,1% das crianças em inadequação (83 de 188), passa sozinho na regra de privacidade; é
  dado, não erro.
