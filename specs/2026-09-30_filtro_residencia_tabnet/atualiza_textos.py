"""Atualiza os NÚMEROS dos textos curados afetados pela reextração com filtro de residência
(specs/2026-09-30_filtro_residencia_tabnet): mesma redação, só os valores (e, onde o número novo muda o sentido da
frase, o mínimo de texto para ela continuar verdadeira). Aplica em relatorio/textos_curados.json e na nota de
curadoria correspondente do analise.py; cada trecho antigo precisa existir (senão o script para).

Fora de propósito: `mapa_taxa_mortalidade_infantil_bairro_2025` (alerta aberto, "decisão da equipe"; figura fora
do site e do PDF) -- não é tocado.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
JSON = RAIZ / "relatorio/textos_curados.json"
ANALISE = RAIZ / "analise.py"

TROCAS = {
    "mapa_mortalidade_infantil_bairro_2025": [
        ("registrados 773 óbitos infantis", "registrados 724 óbitos infantis"),
        ("Em 28 dos 167 bairros", "Em 37 dos 167 bairros"),
    ],
    "mapa_obitos_gravidez_bairro_2025": [
        ("O total do mapa é menor que o da série municipal (15 óbitos em 2025) porque 1 registro não tem bairro de "
         "residência informado.", "O total do mapa é o mesmo da série municipal (14 óbitos em 2025)."),
    ],
    "mapa_obitos_neonatal_precoce_bairro_2025": [("os 420 óbitos", "os 333 óbitos")],
    "mapa_obitos_neonatal_tardia_bairro_2025": [("86 bairros não apresentaram", "88 bairros não apresentaram")],
    "mapa_obitos_pos_neonatal_bairro_2025": [("Em 63 dos 167 bairros", "Em 75 dos 167 bairros")],
    "mapa_obitos_puerperio_bairro_2025": [
        ("Foram registrados 31 óbitos distribuídos em 24 bairros", "Foram registrados 29 óbitos distribuídos em 22 bairros"),
        ("O total do mapa é menor que o da série municipal (35 óbitos em 2025) porque 4 registros não têm bairro de "
         "residência informado.", "O total do mapa é o mesmo da série municipal (29 óbitos em 2025)."),
    ],
    "mapa_obitos_raca_total_bairro_2025": [
        ("139 registraram ao menos um óbito e 28 não", "130 registraram ao menos um óbito e 37 não"),
    ],
    "mapa_percentual_baixo_peso_bairro_2025": [("entre 7,4% e 29,4%", "entre 6,7% e 28,6%")],
    "mapa_taxa_mortalidade_pos_neonatal_bairro_2025": [
        ("Cidade Nova (47,62 por mil), Camorim (28,57) e Pitangueiras (26,32)",
         "Cidade Nova (48,78 por mil), Camorim (33,33) e Barra de Guaratiba (20,41)"),
        ("2 em Cidade Nova, 1 em Camorim e 2 em Pitangueiras", "2 em Cidade Nova, 1 em Camorim e 1 em Barra de Guaratiba"),
    ],
    "mapa_taxa_mortalidade_precoce_bairro_2025": [
        ("como Gericinó, com 1 óbito entre 14 nascidos vivos, e Cidade Universitária, com 1 entre 17",
         "como Gericinó, com 1 óbito entre 16 nascidos vivos, e Ribeira, com 1 entre 22"),
    ],
    "mapa_taxa_obitos_raca_total_bairro_2025": [
        ("Em 2025, Cidade Nova e Gericinó apresentaram a maior taxa registrada, de 71,4 óbitos por mil nascidos vivos, "
         "mas com números diferentes de óbitos e nascidos vivos: 3 óbitos entre 42 nascidos vivos em Cidade Nova e 1 "
         "entre 14 em Gericinó. Cidade Universitária apresentou 58,8 por mil, com 1 óbito entre 17 nascidos vivos.",
         "Em 2025, Cidade Nova apresentou a maior taxa registrada, de 73,2 óbitos por mil nascidos vivos, com 3 óbitos "
         "entre 41 nascidos vivos, seguida por Gericinó, com 62,5 por mil (1 óbito entre 16 nascidos vivos). Ribeira "
         "apresentou 45,5 por mil, com 1 óbito entre 22 nascidos vivos."),
    ],
    "mapa_taxa_obitos_tardios_bairro_2025": [
        ("com 1 óbito entre 42 nascidos vivos, e Riachuelo, com 1 entre 66. Dos 161 bairros da tabela, 86 não",
         "com 1 óbito entre 41 nascidos vivos, e Riachuelo, com 1 entre 63. Dos 159 bairros da tabela, 88 não"),
    ],
    "nascidos_abaixo_peso_percentual_por_ano": [
        ("Após permanecer próximo de 10% até 2010", "Após permanecer próximo de 9,5% até 2010"),
        ("chegando ao pico de 10,63% em 2023", "chegando ao pico de 10,39% em 2023"),
        ("com o percentual chegando a 10,26% em 2025", "com o percentual chegando a 10,00% em 2025"),
    ],
    # sem o filtro, 2022-2025 ganhavam os não residentes e a série "subia" em 2022; com residentes a queda continua
    "nascidos_vivos_por_ano": [
        ("Entre os anos de 2020 e 2021, após um período com uma persistente queda acentuada, a série atinge um patamar "
         "muito baixo, período que coincide com o pico da pandemia da COVID-19, apontando que em 2022 a recuperação "
         "aparece como um ajuste estatístico da série.",
         "Entre os anos de 2020 e 2021, após um período com uma persistente queda acentuada, a série atinge um patamar "
         "muito baixo, período que coincide com o pico da pandemia da COVID-19, e a queda continua nos anos seguintes."),
    ],
    "obitos_gravidez_por_ano": [
        ("passou de 78 em 2006 para 15 em 2025, uma redução de aproximadamente 81%",
         "passou de 58 em 2006 para 14 em 2025, uma redução de aproximadamente 76%"),
        ("seguido de aumento para 15 em 2025", "seguido de aumento para 14 em 2025"),
    ],
    "obitos_puerperio_por_ano": [
        ("passaram de 67 em 2006 para 35 em 2025", "passaram de 48 em 2006 para 29 em 2025"),
        ("foram registrados 74 e 109 óbitos", "foram registrados 63 e 79 óbitos"),
        ("com 33 óbitos, seguido de 35 em 2025", "com 25 óbitos, seguido de 29 em 2025"),
    ],
    "obitos_raca_ano": [
        ("passaram de 468 para 272", "passaram de 468 para 253"),
        ("passaram de 373 para 396", "passaram de 373 para 375"),
        ("passaram de 89 para 57", "passaram de 89 para 53"),
        ("de 167 para 47", "de 167 para 42"),
    ],
    "percentual_mortalidade_raca_ano": [
        ("variando de 17,6 a 11,3 e de 19,8 a 14,3", "variando de 17,6 a 11,2 e de 19,7 a 10,2"),
    ],
    "taxa_mortalidade_infantil_ano": [("chegando a 13,03 em 2024 e 13,06 em 2025", "chegando a 12,35 em 2024 e 12,33 em 2025")],
    "taxa_mortalidade_pos_neonatal_ano": [
        ("quando atingiu 3,70 óbitos", "quando atingiu 3,69 óbitos"),
        ("chegando a 4,65 em 2024 e 4,48 em 2025", "chegando a 4,35 em 2024 e 4,24 em 2025"),
    ],
    "taxa_mortalidade_precoce_ano": [
        ("a taxa passou de 7,86 para 6,42", "a taxa passou de 6,86 para 5,68"),
        ("foram registrados 389 óbitos, o menor número da série, seguido de aumento para 420 em 2025",
         "foram registrados 322 óbitos, o menor número da série, seguido de aumento para 333 em 2025"),
    ],
    "taxa_obitos_tardios_ano": [
        ("a taxa passou de 2,70 para 2,60", "a taxa passou de 2,17 para 2,43"),
        ("O maior valor ocorreu em 2020 (3,46), enquanto o menor foi registrado em 2022 (2,29).",
         "O maior valor ocorreu em 2020 (2,79), enquanto o menor foi registrado em 2011 (1,95)."),
        ("os óbitos tardios passaram de 250 para 170", "os óbitos tardios passaram de 178 para 142"),
    ],
}


def aplica(texto, trocas, onde):
    for velho, novo in trocas:
        if velho not in texto:
            sys.exit(f"ERRO: trecho não encontrado em {onde}: {velho[:80]!r}")
        texto = texto.replace(velho, novo)
    return texto


if __name__ == "__main__":
    dados = json.loads(JSON.read_text(encoding="utf-8"))
    fonte = ANALISE.read_text(encoding="utf-8")
    for chave, trocas in TROCAS.items():
        dados[chave] = aplica(dados[chave], trocas, f"textos_curados.json[{chave}]")
        marca = f"<!-- nota-curadoria:{chave} -->"
        if marca in fonte:
            i = fonte.index(marca)
            j = fonte.find("\n# %%", i)
            j = len(fonte) if j < 0 else j
            fonte = fonte[:i] + aplica(fonte[i:j], trocas, f"analise.py[{chave}]") + fonte[j:]
        else:
            print(f"aviso: {chave} sem nota no analise.py")
    JSON.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ANALISE.write_text(fonte, encoding="utf-8")
    print(f"{len(TROCAS)} textos atualizados")
