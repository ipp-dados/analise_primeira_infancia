"""Parser e validador de `specs/estrutura_eixos.md` (Bloco 1 de
`specs/ajuste_eixos/plan.md`).

`specs/estrutura_eixos.md` e' a fonte unica e editavel a mao da organizacao
de `relatorio/index.html`/PDF/DOCX por eixo de politica municipal de
primeira infancia (ver `specs/ajuste_eixos/specs.md` SS5.1 para o formato e
a decisao de projeto). Este modulo faz so duas coisas:

1. `parse_estrutura_eixos()` -- le o `.md` (heading `##` = eixo, `###` =
   subsecao, linha "- chave: valor" = campo) e devolve uma estrutura de
   dados simples.
2. `valida_estrutura()` -- confere que toda `visualizacao`/`mapa`/`tabela`
   referenciada aponta pra um arquivo que existe de fato em
   `visualizacoes/`/`mapas/`/`tabelas_finais/`.

Os Blocos 3/4/5 do plan.md (HTML, PDF, DOCX) reaproveitam este parser em vez
de reimplementa-lo. Este arquivo NAO regenera `estrutura_eixos.md` a partir
do catalogo Excel -- essa classificacao (`classifica_bucket`/`eh_descartado`/
`comeca_com_ok`, specs.md SS4.1/SS4.2/SS4.4) foi um script ad-hoc, rodado uma
unica vez para produzir o `.md` inicial; dali em diante o `.md` e' editado a
mao pelo usuario (specs.md SS5.2) -- reimplementar o classificador aqui
reabriria um caminho de regeneracao automatica que a spec explicitamente nao
quer (specs.md SS5.2, plan.md Bloco 1).
"""

from pathlib import Path

# Diretorios (relativos a raiz do projeto) onde cada tipo de referencia deve
# existir de fato -- usados por valida_estrutura().
_DIRS_POR_CAMPO = {
    "visualização": "visualizacoes",
    "mapa": "mapas",
    "tabela": "tabelas_finais",
}


def parse_estrutura_eixos(caminho="specs/estrutura_eixos.md"):
    """Le `caminho` e devolve:

        list[{"eixo": str, "subsecoes": list[{"titulo": str, "campos": dict}]}]

    Regra de parsing (specs.md SS5.1): heading `##` abre um eixo novo;
    heading `###` abre uma subsecao nova dentro do eixo atual; uma linha
    "- chave: valor" vira um campo da subsecao atual (tudo antes do primeiro
    ':' e' a chave, o resto -- sem espacos nas pontas -- e' o valor). Linhas
    fora de uma subsecao (o bloco de nota no topo do arquivo, linhas em
    branco, blockquotes '>') sao ignoradas.

    Representacao de `campos`: a maioria das chaves ocorre uma vez so por
    subsecao e fica como string simples (`campos["fonte"]`). Algumas chaves
    (`visualização`, `mapa`, `tabela`) podem se repetir dentro da mesma
    subsecao quando um indicador do catalogo tem varios cortes reais em
    `analise.py` (specs.md SS4.5/plan.md Bloco 1) -- nesses casos o valor
    vira uma lista, na ordem em que aparecem no arquivo. Escolha de design:
    a primeira ocorrencia de uma chave fica como string; se a MESMA chave
    aparecer de novo na mesma subsecao, a string vira uma lista de 2 e as
    ocorrencias seguintes so' dao `append` -- assim quem usa `campos.get`
    nao precisa saber de antemao se a chave e' repetivel, so' tratar
    str-ou-list quando for iterar.
    """
    caminho = Path(caminho)
    linhas = caminho.read_text(encoding="utf-8").splitlines()

    estrutura = []
    eixo_atual = None
    subsecao_atual = None

    for linha in linhas:
        bruta = linha.rstrip()
        if bruta.startswith("## "):
            eixo_atual = {"eixo": bruta[3:].strip(), "subsecoes": []}
            estrutura.append(eixo_atual)
            subsecao_atual = None
        elif bruta.startswith("### "):
            if eixo_atual is None:
                raise ValueError(
                    f"Subsecao {bruta!r} encontrada antes de qualquer heading '##' de eixo "
                    f"em {caminho} -- arquivo fora do formato esperado (specs.md SS5.1)."
                )
            subsecao_atual = {"titulo": bruta[4:].strip(), "campos": {}}
            eixo_atual["subsecoes"].append(subsecao_atual)
        elif bruta.lstrip().startswith("- ") and subsecao_atual is not None:
            item = bruta.lstrip()[2:]
            if ":" not in item:
                continue  # linha de lista sem "chave: valor" -- ignorada, nao e' um campo
            chave, valor = item.split(":", 1)
            chave = chave.strip()
            valor = valor.strip()
            campos = subsecao_atual["campos"]
            if chave not in campos:
                campos[chave] = valor
            elif isinstance(campos[chave], list):
                campos[chave].append(valor)
            else:
                campos[chave] = [campos[chave], valor]
        # qualquer outra linha (nota do topo, '>', linha em branco, texto solto) e' ignorada

    return estrutura


def _nomes_de_arquivo(valor):
    """`valor` de um campo visualização/mapa/tabela pode ser uma string
    'nome.ext' ou 'nome.ext (descrição livre)', ou uma lista dessas -- extrai
    só o token do nome de arquivo (primeira "palavra" da string), removendo
    crases se presentes."""
    valores = valor if isinstance(valor, list) else [valor]
    nomes = []
    for v in valores:
        token = v.strip().split()[0] if v.strip() else ""
        nomes.append(token.strip("`"))
    return nomes


def valida_estrutura(estrutura, base_dir="."):
    """Confere que todo valor de 'visualização'/'mapa'/'tabela' referenciado
    em `estrutura` (retorno de parse_estrutura_eixos()) aponta pra um
    arquivo que existe de fato em visualizacoes/mapas/tabelas_finais (dentro
    de `base_dir`). Levanta FileNotFoundError na PRIMEIRA referência quebrada
    encontrada, nomeando o arquivo que sumiu e o indicador (eixo > subseção)
    que o referenciou -- nunca retorna silenciosamente uma lista de erros
    parcial nem segue em frente para gerar um relatório incompleto
    (plan.md Bloco 1: "falha alto, nunca gera relatório silenciosamente
    incompleto por causa de uma referência quebrada")."""
    base = Path(base_dir)
    for eixo in estrutura:
        for sub in eixo["subsecoes"]:
            for campo, pasta in _DIRS_POR_CAMPO.items():
                if campo not in sub["campos"]:
                    continue
                for nome in _nomes_de_arquivo(sub["campos"][campo]):
                    caminho_esperado = base / pasta / nome
                    if not caminho_esperado.exists():
                        raise FileNotFoundError(
                            f"{campo} '{nome}' (referenciado em "
                            f"{eixo['eixo']!r} > {sub['titulo']!r}) não existe em "
                            f"'{pasta}/' -- ver specs/estrutura_eixos.md"
                        )
    return True


def itens_sem_arquivo(estrutura):
    """Subseções sem nenhuma `visualização`/`mapa`/`tabela` e sem `status` -- o HTML e o PDF as pulam
    em silêncio (foi assim que o item "percentual de nascidos vivos por bairro" sumiu do relatório;
    `specs/populacao-referencia` D4). Devolve `[(eixo, título)]`."""
    return [(eixo["eixo"], sub["titulo"])
            for eixo in estrutura for sub in eixo["subsecoes"]
            if not any(c in sub["campos"] for c in _DIRS_POR_CAMPO) and "status" not in sub["campos"]]


def avisa_itens_sem_arquivo(caminho="specs/estrutura_eixos.md"):
    """Só um aviso no console (não muda nenhuma saída): lista os itens de `itens_sem_arquivo`."""
    itens = itens_sem_arquivo(parse_estrutura_eixos(caminho))
    for eixo, titulo in itens:
        print(f"AVISO: item sem arquivo e sem status (não aparece no relatório): {eixo} > {titulo}")
    return itens


if __name__ == "__main__":
    import sys

    # Windows abre stdout no codepage do console (ex. cp1252), que não cobre os
    # emojis dos títulos de eixo -- força UTF-8 para o print funcionar sem
    # exigir `PYTHONIOENCODING=utf-8` do ambiente. reconfigure() existe desde
    # o Python 3.7; em stdout já UTF-8 (Linux/macOS) isto é um no-op.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    estrutura = parse_estrutura_eixos()

    total_subsecoes = sum(len(eixo["subsecoes"]) for eixo in estrutura)
    total_pendentes = sum(
        1
        for eixo in estrutura
        for sub in eixo["subsecoes"]
        if sub["campos"].get("status") == "pendente"
    )

    print(f"Eixos: {len(estrutura)}")
    for eixo in estrutura:
        print(f"  - {eixo['eixo']}: {len(eixo['subsecoes'])} subseções")
    print(f"Total de subseções (indicadores ativos): {total_subsecoes}")
    print(f"Pendentes (status: pendente): {total_pendentes}")
    sem_arquivo = itens_sem_arquivo(estrutura)
    for eixo_sem, titulo_sem in sem_arquivo:
        print(f"AVISO: item sem arquivo e sem status (não aparece no relatório): {eixo_sem} > {titulo_sem}")
    print(f"Itens sem arquivo e sem status: {len(sem_arquivo)}")

    try:
        valida_estrutura(estrutura)
    except FileNotFoundError as erro:
        print(f"ERRO de validação: {erro}")
        raise SystemExit(1)
    else:
        print("Validação: OK -- toda visualização/mapa/tabela referenciada existe.")
