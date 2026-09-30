# Rodada: filtro de município de residência nos exports por bairro do Tabnet (2026-09-30)

## Problema

Os exports por bairro do Tabnet da SMS-Rio (`tabnet.rio.rj.gov.br`, SIM e SINASC 2006 em diante) foram gerados
**sem a seleção "Munic Resid = 330455 Rio de Janeiro"**. Sem ela, o Tabnet devolve todo registro da base municipal —
inclusive óbitos e nascimentos de **não residentes** ocorridos no Rio. Parte deles cai em "EM BRANCO" (sem bairro),
parte recebe um código de bairro do Rio.

Achado na conferência do deck (slide 17, mortalidade infantil 13,1‰): em 2025 o arquivo de óbitos de menores de 1 ano
por bairro somava 907 (134 em branco, 773 com bairro), mas o próprio Tabnet dá **724** óbitos de menores de 1 ano
de residentes no Rio, todos com bairro. Nascidos vivos: 65.507 no arquivo contra **58.700** de mães residentes.

## Prova

`extrai_tabnet.py --conferir` refaz cada consulta **sem** o filtro e compara com o arquivo versionado: os 11 arquivos
do SIM batem com diferença zero em todos os anos; os 9 do SINASC com diferença de 0 a 3 nascimentos no total da
série (base de 2025 ainda em revisão). Ou seja, é a mesma consulta, só faltava o filtro.

Não afetados (já filtrados por residência): causas evitáveis por município (segundo causas e por raça/cor — 333/142/249
em 2025, como o Tabnet), a planilha TabWin por CAP (`Munic Resid RJ: 330455` no LOG), SINAN (violência — o cabeçalho
do export traz `Munic. Residência: 330455`), SISVAN. `nascidos_vivos_cor_raca_mae_municipio_2011_2025.csv` também
está sem o filtro, mas não é lido pelo `analise.py` — fica como está (anotado aqui).

## Decisão

Reextrair os 20 arquivos com o filtro, no mesmo formato (bairro × ano, "Total" no fim, mesmo separador), pelo script
desta rodada (`extrai_tabnet.py --gravar`). Nada muda no `analise.py`: os carregadores já descartam "EM BRANCO".
Depois: rodar as seções Setup + Censo + DataSUS/Tabnet do `analise.py` (a do CadÚnico fica de fora para não
reextrair o banco ao vivo), regerar site, PDF e apresentação.

Arquivos (em `dados_locais/`):
- SIM: `mortalidade/obitos_0_364_dias_bairro`, `_0_6_dias_`, `_7_27_dias_`, os 6 de raça/cor (`brancos`, `pretos`,
  `amarelos`, `pardos`, `indigenas`, `nao_informado` = Não informado + Ignorado), `obitos_gravidez_bairro`
  (Óbito/Gravidez = Sim), `obitos_puerperio_bairro` (Óbito/Puerpério = Sim até 42 dias).
- SINASC: `nascidos_vivos/nascidos_vivos_bairros_2006_a_2025`, `..._baixo_peso_ao_nascer_...` (peso 0 a 2.499 g),
  e os 7 de raça/cor da mãe em `mortalidade/nascidos_vivos_mae_*_bairro_2011_2025`.

## Efeito esperado

Números municipais que somam os arquivos por bairro passam a ser de residentes: nascidos vivos, baixo peso,
mortalidade infantil/neonatal por bairro e a taxa municipal "com bairro informado" do deck/site/PDF.

## Também nesta rodada (deck)

Slide 11: legenda do mapa da esquerda passa a dizer o indicador; slide 32: "dados primários" com acento.
