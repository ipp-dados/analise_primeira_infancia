"""CSV de tabelas_finais/ -> tabela ABNT/IBGE em LaTeX (longtable + booktabs) para os apêndices.

Regras gerais (specs/relatorio_latex §3, validation V13): tabela aberta nas laterais, título acima,
Fonte abaixo; números em pt-BR (1.234,5); coluna de ano/idade/código sem separador de milhar; percentual
com 1 casa; linhas de total em negrito. Ajustes por arquivo (colunas, rótulos, escala) ficam em
`AJUSTES` -- é o que o Bloco 4 porta de build_notebook_report.py.
"""
import math
import re
from pathlib import Path

import pandas as pd

MAX_COLUNAS_RETRATO = 7
COLUNAS_SEM_MILHAR = re.compile(r"^(ano|idade|cod\w*|codigo|cod_ap_sms|codbairro|codra|cap|ap|rp|ra)$", re.I)
COLUNAS_PCT = re.compile(r"(percent|%|taxa|propor|cobertura)", re.I)

# nome do arquivo -> {"titulo":..., "colunas": [...], "renomeia": {...}, "escala_pct": [...]}
AJUSTES = {}


def esc(s):
    s = str(s)
    trocas = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
              "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(trocas.get(c, c) for c in s)


def num(v, dec):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "--"
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def _formata_coluna(serie, nome):
    if not pd.api.types.is_numeric_dtype(serie):
        return [esc(v) if not (isinstance(v, float) and math.isnan(v)) else "--" for v in serie], "l"
    if COLUNAS_SEM_MILHAR.match(str(nome).strip()):
        return [str(int(v)) if pd.notna(v) and float(v).is_integer() else (esc(v) if pd.notna(v) else "--") for v in serie], "r"
    inteira = serie.dropna().apply(lambda x: float(x).is_integer()).all()
    dec = 0 if inteira and not COLUNAS_PCT.search(str(nome)) else 1
    return [num(v, dec) for v in serie], "r"


def _cabecalho(c):
    """Cabeçalho legível sem renomear à mão: 'peso_baixo_percentual' -> 'Peso baixo (%)'."""
    s = str(c).strip()
    pct = bool(re.search(r"(^|_)(percentual|pct)($|_)", s))
    s = re.sub(r"(^|_)(percentual|pct)($|_)", " ", s).replace("_", " ").strip()
    s = re.sub(r"\s+", " ", s)
    s = s[:1].upper() + s[1:] if s else s
    return f"{s} (%)" if pct else s


def titulo_padrao(nome_arquivo, titulo_secao):
    base = Path(nome_arquivo).stem
    base = re.sub(r"^tabela_mapa_", "", base)
    return f"{titulo_secao} ({base.replace('_', ' ')})"


def tabela_latex(caminho, titulo_secao, fonte_tex, rotulo):
    nome = Path(caminho).name
    aj = AJUSTES.get(nome, {})
    df = pd.read_csv(caminho)
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed")]
    if aj.get("colunas"):
        df = df[aj["colunas"]]
    for c in aj.get("escala_pct", []):
        df[c] = df[c] * 100
    for c in df.columns:     # "86.58%" (texto) -> 86.58 (número), para formatar em pt-BR
        if df[c].dtype == object and df[c].astype(str).str.fullmatch(r"-?\d+(\.\d+)?%").mean() > 0.8:
            df[c] = pd.to_numeric(df[c].astype(str).str.rstrip("%"), errors="coerce")
    if "ano" in df.columns and not aj.get("sem_ordenar"):
        df = df.sort_values("ano", kind="stable")
    df = df.rename(columns=aj.get("renomeia", {}))
    df = df.rename(columns={c: _cabecalho(c) for c in df.columns})
    titulo = esc(aj.get("titulo") or titulo_padrao(nome, titulo_secao))

    colunas, specs = [], []
    for c in df.columns:
        vals, al = _formata_coluna(df[c], c)
        colunas.append(vals)
        specs.append(al)
    largo = len(df.columns) > MAX_COLUNAS_RETRATO
    cab = " & ".join(r"\textbf{" + esc(c) + "}" for c in df.columns) + r" \\"
    linhas = []
    for i in range(len(df)):
        celulas = [colunas[j][i] for j in range(len(df.columns))]
        if str(celulas[0]).strip().lower().startswith("total"):
            celulas = [r"\textbf{" + c + "}" for c in celulas]
        linhas.append(" & ".join(celulas) + r" \\")
    colspec = "@{}" + "".join(specs) + "@{}"
    corpo = "\n".join(linhas)
    tamanho = r"\scriptsize" if largo else r"\small"
    tex = (rf"{{{tamanho}\setlength{{\tabcolsep}}{{{'3pt' if largo else '5pt'}}}" "\n"
           rf"\begin{{longtable}}{{{colspec}}}" "\n"
           rf"\caption{{{titulo}}}\label{{{rotulo}}}\\" "\n"
           rf"\toprule {cab} \midrule \endfirsthead" "\n"
           rf"\multicolumn{{{len(df.columns)}}}{{@{{}}l}}{{\footnotesize\itshape (continuação)}}\\ \toprule {cab} \midrule \endhead" "\n"
           rf"\midrule \multicolumn{{{len(df.columns)}}}{{r@{{}}}}{{\footnotesize\itshape (continua)}}\\ \endfoot" "\n"
           r"\bottomrule \endlastfoot" "\n"
           f"{corpo}\n"
           r"\end{longtable}}" "\n"
           rf"\vspace{{-6pt}}\fonte{{{fonte_tex}}}" "\n")
    if largo:
        tex = r"\begin{landscape}" + "\n" + tex + r"\end{landscape}" + "\n"
    return tex
