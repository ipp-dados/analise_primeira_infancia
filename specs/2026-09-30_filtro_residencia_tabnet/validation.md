# Validação — filtro de residência nos exports do Tabnet (2026-09-30)

| # | Conferência | Resultado |
|---|---|---|
| V1 | `extrai_tabnet.py --conferir`: consulta SEM filtro reproduz os arquivos antigos | 11 do SIM: diferença 0 em todos os anos (puerpério = "Sim até 42 dias"); 9 do SINASC: 0 a 3 nascimentos na série inteira (base 2025 em revisão) |
| V2 | Totais 2025 com filtro × Tabnet público (residentes no Rio) | óbitos < 1 ano 724 (0-6 d 333, 7-27 d 142, 28-364 d 249) = Tabnet; nascidos vivos 58.700; baixo peso 5.869 |
| V3 | Outras fontes já filtradas (não reextraídas) | causas evitáveis municipais (333/141/249 em 2025), TabWin por CAP (LOG: `Munic Resid RJ: 330455`), SINAN (cabeçalho `Munic. Residência: 330455`), SISVAN |
| V4 | `analise.py`: Setup + Censo + DataSUS/Tabnet (linhas 1-423 e 946-2272; CadÚnico fora para não reextrair o banco) | sem erro; 21 tabelas mudaram, todas de nascidos/baixo peso/mortalidade infantil, neonatal, materna e por raça/cor; figuras A4 regeneradas |
| V5 | Números novos (2025) | mortalidade infantil 12,33‰ (antes 13,06), pós-neonatal 4,24, precoce 5,68, tardia 2,43; baixo peso 10,0% (10,26%); nascidos 58.700 (65.507), pico 90.303 em 2015 (antes 94.588 em 2009); sem bairro 3 (6.336) |
| V6 | Textos curados (`atualiza_textos.py`): 22 textos, só números (e 1 frase: a "recuperação de 2022" dos nascidos era efeito da extração) | JSON + nota do `analise.py`; `controle_revisao.json` com status "atualizado" (histórico `residencia_2026-09-30`); `mapa_taxa_mortalidade_infantil_bairro_2025` não tocado (alerta aberto, fora do site e do PDF) |
| V7 | Site regenerado | determinístico (2 builds, mesmos md5); sem AVISO de tamanho; Chrome sem erro de console; achado "12,3 óbitos por mil"; nenhum 13,06/65.507/94.588/10,26% |
| V8 | PDF (`gera_latex.py --publicar`) | 0 `undefined`; texto extraído sem 65.507/13,06/10,26%/94.588; tem 58.700, 12,33, 10,00%, 90.303 |
| V9 | Deck | slide 14: 58.700, pico 90.303 (2015), 3 sem bairro; slide 17: 12,3‰; slide 28: 10,0%; slide 11 com o indicador de cada mapa; slide 32 "dados primários" |
