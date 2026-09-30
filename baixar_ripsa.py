import os
import requests
import pandas as pd
from datetime import date

PASTA = "dados_locais/populacao"
URL_BASE = "https://sistemas.saude.rj.gov.br/tabnetbd/populacao/dados"

os.makedirs(PASTA, exist_ok=True)

dados = []
totais_gerais_lista = []

for ano in range(2000, 2026):

    url = f"{URL_BASE}/populacao_{ano}.csv"
    caminho = os.path.join(PASTA, f"populacao_{ano}.csv")

    print(f"Baixando {ano}...")

    resposta = requests.get(url)
    resposta.raise_for_status()

    with open(caminho, "wb") as arquivo:
        arquivo.write(resposta.content)

    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="latin1",
        dtype={"Idade": str}
    )

    df["Município"] = df["Município"].astype(str).str.zfill(6)
    df["Idade"] = df["Idade"].str.zfill(2)

    # Rio de Janeiro
    df_rio = df[df["Município"] == "330455"].copy()

    # ---------------------------------------------------------
    # População de 0 a 6 anos por sexo
    # ---------------------------------------------------------

    df_idades = df_rio[
        (df_rio["Idade"].isin(["00", "01", "02", "03", "04", "05", "06"]))
        & (df_rio["Sexo"].isin(["M", "F"]))
    ].copy()

    df_idades = df_idades.rename(
        columns={
            "Ano": "ano",
            "Idade": "idade",
            "Sexo": "sexo_original",
            "Populacao": "populacao"
        }
    )

    df_idades["sexo"] = df_idades["sexo_original"].map({
        "M": "masculino",
        "F": "feminino"
    })

    df_idades["idade"] = df_idades["idade"].astype(int)

    dados.append(
        df_idades[
            ["ano", "idade", "sexo", "populacao"]
        ]
    )

    # ---------------------------------------------------------
    # População total do município
    # ---------------------------------------------------------

    total_rio = df_rio["Populacao"].sum()

    totais_gerais_lista.append({
        "ano": ano,
        "idade": "total",
        "sexo": "total",
        "populacao": total_rio
    })

    print(f"OK: {ano}")


# -------------------------------------------------------------
# Junta população de 0 a 6 por sexo
# -------------------------------------------------------------

df_ripsa = pd.concat(dados, ignore_index=True)

# -------------------------------------------------------------
# Junta população total do município
# -------------------------------------------------------------

totais_gerais = pd.DataFrame(totais_gerais_lista)

df_final = pd.concat(
    [
        df_ripsa,
        totais_gerais
    ],
    ignore_index=True
)

df_final["idade"] = df_final["idade"].astype(str)
df_final["data_consulta"] = date.today().isoformat()

df_final = df_final.sort_values(
    ["ano", "sexo", "idade"]
).reset_index(drop=True)


# -------------------------------------------------------------
# Validação
# -------------------------------------------------------------

# Deve haver:
# 26 anos × 7 idades × 2 sexos = 364 registros
# + 26 totais gerais = 390 registros

assert len(df_final) == 390

# Confere 2025: população de 0 a 5 anos = 393.073
teste_2025 = df_final[
    (df_final["ano"] == 2025)
    & (df_final["idade"].isin(["0", "1", "2", "3", "4", "5"]))
]["populacao"].sum()

assert teste_2025 == 393073


# -------------------------------------------------------------
# Salva arquivo final
# -------------------------------------------------------------

arquivo_saida = os.path.join(
    PASTA,
    "ripsa_populacao_rio.csv"
)

df_final.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8"
)

print("\nArquivo criado:")
print(arquivo_saida)

print("\nColunas:")
print(df_final.columns.tolist())

print("\nQuantidade de registros:")
print(len(df_final))

print("\nPopulação 0 a 5 anos em 2025:")
print(teste_2025)

print("\nPrimeiras linhas:")
print(df_final.head(15))