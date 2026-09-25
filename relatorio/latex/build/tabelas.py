"""CSV de tabelas_finais/ -> tabela ABNT/IBGE em LaTeX (longtable + booktabs) para os apêndices.

Regras gerais (specs/relatorio_latex §3, validation V13): tabela aberta nas laterais, título acima,
Fonte abaixo; números em pt-BR (1.234,5); coluna de ano/idade/código sem separador de milhar; percentual
com 1 casa; linhas de total em negrito.

Regras de tamanho (T4.4, decididas pelo usuário em 2026-09-25):
  1. tabela por bairro com coluna `ano` e mais de 100 linhas -> só o ano mais recente (completo: se houver
     `ano_parcial`, o último ano não parcial); o ano vai para o título;
  2. depois disso, mais de `MAX_LINHAS_PDF` linhas -> não é impressa (fica só no formato digital);
  3. tabela por bairro: sem colunas de código e sem `ano` constante, em ordem alfabética; com até
     `MAX_COLUNAS_DUAS` colunas, duas colunas lado a lado em retrato; até `MAX_COLUNAS_DUAS_PAISAGEM`,
     duas colunas em paisagem; mais largas, uma coluna em paisagem.
Ajustes por arquivo (colunas, rótulos, escala) ficam em `AJUSTES` -- o que o Bloco 4 porta de
build_notebook_report.py.
"""
import hashlib
import math
import re
import unicodedata
from pathlib import Path

import pandas as pd

MAX_COLUNAS_RETRATO = 7
MAX_LINHAS_PDF = 200
LIMIAR_ULTIMO_ANO = 100
MAX_COLUNAS_DUAS = 5              # tabela por bairro em duas colunas, página em retrato
MAX_COLUNAS_DUAS_PAISAGEM = 8     # ... ou em paisagem; acima disso, uma coluna só (paisagem)
COLUNAS_CODIGO = re.compile(r"^(codigo|codbairro|codra|cod_ap_sms|cod_rp|area_plane)$", re.I)
COLUNAS_SEM_MILHAR = re.compile(r"^(ano|idade|cod\w*|codigo|cap|ap|rp|ra)$", re.I)
COLUNAS_PCT = re.compile(r"(percent|%|taxa|propor|cobertura)", re.I)
NOTA_SUPRESSAO = ("Nota: -- indica célula suprimida (menos de 20 famílias ou crianças), "
                  "conforme a regra de proteção de dados do Cadastro Único.")

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


def _sem_acento(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


CODIGOS_ESPECIAIS = {998: "Ilha do Governador (bairro ignorado)", 999: "Bairro ignorado"}
_NOMES = {}


def _nomes_oficiais():
    """codbairro -> nome oficial (dados_locais/geo/limite_bairros_rio.geojson, IPP/Data.Rio)."""
    if not _NOMES:
        import json
        raiz = Path(__file__).resolve().parents[3]
        geo = json.loads((raiz / "dados_locais/geo/limite_bairros_rio.geojson").read_text(encoding="utf-8"))
        _NOMES.update({int(f["properties"]["codbairro"]): f["properties"]["nome"].strip() for f in geo["features"]})
    return _NOMES


def _cabecalho(c):
    """Cabeçalho legível sem renomear à mão: 'peso_baixo_percentual' -> 'Peso baixo (%)',
    'Percentual 0 a 4' -> '% 0 a 4'."""
    s = re.sub(r"^(Percentual|Percent\.)\s+", "% ", str(c).strip())
    pct = bool(re.search(r"(^|_)(percentual|pct)($|_)", s))
    s = re.sub(r"(^|_)(percentual|pct)($|_)", " ", s).replace("_", " ").strip()
    s = re.sub(r"\s+", " ", s)
    s = s[:1].upper() + s[1:] if s else s
    return f"{s} (%)" if pct else s


# ------------------------------------------------------------------ preparação (cacheada)
_PREP = {}


def prepara(caminho):
    """(df, meta) já com as regras de tamanho aplicadas. meta: bairro, ano, suprimido, linhas_orig."""
    caminho = Path(caminho)
    if caminho in _PREP:
        return _PREP[caminho]
    aj = AJUSTES.get(caminho.name, {})
    df = pd.read_csv(caminho)
    df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed")]
    meta = {"linhas_orig": len(df), "ano": None, "suprimido": False,
            "bairro": any(str(c).lower() == "bairro" for c in df.columns)}
    if meta["bairro"] and "ano" in df.columns and len(df) > LIMIAR_ULTIMO_ANO:
        anos = df.loc[~df["ano_parcial"].astype(bool), "ano"] if "ano_parcial" in df.columns else df["ano"]
        meta["ano"] = int(anos.max())
        df = df[df["ano"] == meta["ano"]]
    if "ano_parcial" in df.columns and meta["ano"] is not None:
        df = df.drop(columns="ano_parcial")
    if aj.get("colunas"):
        df = df[aj["colunas"]]
    for c in df.columns:     # "86.58%" (texto) -> 86.58 (número), para formatar em pt-BR
        if df[c].dtype == object and df[c].astype(str).str.fullmatch(r"-?\d+(\.\d+)?%").mean() > 0.8:
            df[c] = pd.to_numeric(df[c].astype(str).str.rstrip("%"), errors="coerce")
    for c in aj.get("escala_pct", []):
        df[c] = df[c] * 100
    if meta["bairro"]:
        if "suprimido" in df.columns:
            meta["suprimido"] = bool(df["suprimido"].astype(bool).any())
            df = df.drop(columns="suprimido")
        # nome oficial do bairro pelo código (constituição §3: junção sempre pelo código, nunca pelo nome);
        # o Tabnet traz nomes em caixa alta e sem acento. Códigos sem bairro (998/999, "ignorado") vão ao fim.
        col_cod = next((c for c in df.columns if str(c).lower() in ("codigo", "codbairro")), None)
        col_b = next(c for c in df.columns if str(c).lower() == "bairro")
        df["_fim"] = 0
        if col_cod is not None:
            cods = pd.to_numeric(df[col_cod], errors="coerce")
            oficial = cods.map(_nomes_oficiais())
            df[col_b] = oficial.fillna(cods.map(CODIGOS_ESPECIAIS)).fillna(df[col_b])
            df["_fim"] = (cods.isin(list(CODIGOS_ESPECIAIS)) | oficial.isna()).astype(int)
        df = df.drop(columns=[c for c in df.columns if COLUNAS_CODIGO.match(str(c))])
        if "ano" in df.columns and df["ano"].nunique() == 1:
            meta["ano"] = meta["ano"] or int(df["ano"].iloc[0])
            df = df.drop(columns="ano")
        df = df[[col_b] + [c for c in df.columns if c != col_b]]
        df = (df.assign(_k=df[col_b].map(_sem_acento)).sort_values(["_fim", "_k"], kind="stable")
              .drop(columns=["_k", "_fim"]))
    elif "ano" in df.columns and not aj.get("sem_ordenar"):
        df = df.sort_values("ano", kind="stable")
    df = df.rename(columns=aj.get("renomeia", {}))
    df = df.rename(columns={c: _cabecalho(c) for c in df.columns}).reset_index(drop=True)
    _PREP[caminho] = (df, meta)
    return df, meta


def n_linhas(caminho):
    return len(prepara(caminho)[0])


def cabe_no_pdf(caminho):
    return n_linhas(caminho) <= MAX_LINHAS_PDF


def assinatura(caminho):
    """Mesmo conteúdo impresso = mesma assinatura (ex. série bairro×ano filtrada = tabela do mapa)."""
    df, meta = prepara(caminho)
    base = df.sort_values(list(df.columns)).to_csv(index=False) + str(meta["ano"])
    return hashlib.md5(base.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------ LaTeX
def _formata_coluna(serie, nome):
    if not pd.api.types.is_numeric_dtype(serie):
        return [esc(v) if not (isinstance(v, float) and math.isnan(v)) else "--" for v in serie], "l"
    if COLUNAS_SEM_MILHAR.match(str(nome).strip()):
        return [str(int(v)) if pd.notna(v) and float(v).is_integer() else (esc(v) if pd.notna(v) else "--") for v in serie], "r"
    inteira = serie.dropna().apply(lambda x: float(x).is_integer()).all()
    dec = 0 if inteira and not COLUNAS_PCT.search(str(nome)) else 1
    return [num(v, dec) for v in serie], "r"


def titulo_padrao(nome_arquivo, titulo_secao):
    base = Path(nome_arquivo).stem
    base = re.sub(r"^tabela_mapa_", "", base)
    return f"{titulo_secao} ({base.replace('_', ' ')})"


def _longtable(colspec, ncols, cab, corpo, titulo, rotulo, tamanho, sep):
    return (rf"{{{tamanho}\setlength{{\tabcolsep}}{{{sep}}}" "\n"
            rf"\begin{{longtable}}{{{colspec}}}" "\n"
            rf"\caption{{{titulo}}}\label{{{rotulo}}}\\" "\n"
            rf"\toprule {cab} \midrule \endfirsthead" "\n"
            rf"\multicolumn{{{ncols}}}{{@{{}}l}}{{\footnotesize\itshape (continuação)}}\\ \toprule {cab} \midrule \endhead" "\n"
            rf"\midrule \multicolumn{{{ncols}}}{{r@{{}}}}{{\footnotesize\itshape (continua)}}\\ \endfoot" "\n"
            r"\bottomrule \endlastfoot" "\n"
            f"{corpo}\n"
            r"\end{longtable}}" "\n")


def tabela_latex(caminho, titulo_secao, fonte_tex, rotulo):
    nome = Path(caminho).name
    aj = AJUSTES.get(nome, {})
    df, meta = prepara(caminho)
    titulo = aj.get("titulo") or titulo_padrao(nome, titulo_secao)
    if meta["ano"] and str(meta["ano"]) not in titulo:
        titulo += f", {meta['ano']}"
    titulo = esc(titulo)
    fonte = fonte_tex + (" " + NOTA_SUPRESSAO if meta["suprimido"] else "")

    colunas, specs = [], []
    for c in df.columns:
        vals, al = _formata_coluna(df[c], c)
        colunas.append(vals)
        specs.append(al)
    n, ncol = len(df), len(df.columns)

    def celulas(i):
        cs = [colunas[j][i] for j in range(ncol)]
        if str(cs[0]).strip().lower().startswith("total"):
            cs = [r"\textbf{" + c + "}" for c in cs]
        return cs

    if meta["bairro"] and ncol <= MAX_COLUNAS_DUAS_PAISAGEM and n > 30:
        # duas colunas lado a lado: linhas 1..m à esquerda, m+1..n à direita. Retrato até
        # MAX_COLUNAS_DUAS colunas, paisagem até MAX_COLUNAS_DUAS_PAISAGEM (larguras em cm)
        paisagem = ncol > MAX_COLUNAS_DUAS
        util, vao = (24.5 if paisagem else 16.0), 0.6
        pequeno = paisagem or ncol > 4
        larg_bairro = 2.9 if pequeno else 3.2
        meia_larg = (util - vao) / 2
        larg_num = (meia_larg - larg_bairro) / (ncol - 1) - 0.25     # 0,25 cm = 2 x \tabcolsep
        meia = [rf">{{\raggedright\arraybackslash}}p{{{larg_bairro - 0.25:.2f}cm}}"] + \
               [rf">{{\raggedleft\arraybackslash}}p{{{larg_num:.2f}cm}}"] * (ncol - 1)
        colspec = "@{}" + "".join(meia) + rf"@{{\hspace{{{vao}cm}}}}" + "".join(meia) + "@{}"
        # cabeçalho quebra só em espaço (sem hifenizar "mortali-dade" numa coluna estreita)
        cab1 = " & ".join(r"\hyphenpenalty=10000\exhyphenpenalty=10000\textbf{" + esc(c) + "}" for c in df.columns)
        cab = f"{cab1} & {cab1} " + r"\\"
        m = math.ceil(n / 2)
        linhas = []
        for i in range(m):
            dir_ = celulas(i + m) if i + m < n else [""] * ncol
            linhas.append(" & ".join(celulas(i) + dir_) + r" \\")
        tex = (r"{\renewcommand{\arraystretch}{1.0}" + "\n"
               + _longtable(colspec, 2 * ncol, cab, "\n".join(linhas), titulo, rotulo,
                            r"\scriptsize" if pequeno else r"\footnotesize", "3.5pt") + "}\n")
        if paisagem:
            return r"\begin{landscape}" + "\n" + tex + rf"\vspace{{-6pt}}\fonte{{{fonte}}}" + "\n" + r"\end{landscape}" + "\n"
    else:
        largo = ncol > MAX_COLUNAS_RETRATO
        cab = " & ".join(r"\textbf{" + esc(c) + "}" for c in df.columns) + r" \\"
        corpo = "\n".join(" & ".join(celulas(i)) + r" \\" for i in range(n))
        tex = _longtable("@{}" + "".join(specs) + "@{}", ncol, cab, corpo, titulo, rotulo,
                         r"\scriptsize" if largo else r"\small", "3pt" if largo else "5pt")
        if largo:
            tex = r"\begin{landscape}" + "\n" + tex + rf"\vspace{{-6pt}}\fonte{{{fonte}}}" + "\n" + r"\end{landscape}" + "\n"
            return tex
    return tex + rf"\vspace{{-6pt}}\fonte{{{fonte}}}" + "\n"
