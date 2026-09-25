"""Inventário de fontes × gráficos/mapas/tabelas (specs/relatorio_latex, Bloco 1).

Gera relatorio/inventario_fontes.md e relatorio/inventario_fontes.csv -- documento de conferência
para a equipe, NÃO entra no PDF. Cruza três coisas:

1. analise.py, lido estaticamente (AST, sem executar nada): cada chamada de um helper que grava
   figura (qualquer função com `savefig` no corpo), cada `plt.savefig` solto e cada `.to_csv` em
   tabelas_finais/ -- com `nome_arquivo`, `titulo` e `fonte_dados` resolvidos contra as
   atribuições de string anteriores (`fonte_* = ...`) e contra os laços `for` sobre listas literais;
2. specs/estrutura_eixos.md (eixo, subseção e texto `fonte:` de cada arquivo usado no relatório);
3. relatorio/latex/fontes.bib (campo `padroes`, que liga cada texto de fonte a uma referência ABNT).

Só aponta divergências; não corrige nada (constituição §5 -- a correção é decisão da equipe).

Uso (da raiz do projeto):  python relatorio/latex/build/inventario_fontes.py
"""
import ast
import csv
import itertools
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / ".claude/skills/export_pdf_report/scripts"))
from gera_estrutura_eixos import parse_estrutura_eixos  # noqa: E402

ANALISE = RAIZ / "analise.py"
BIB = RAIZ / "relatorio/latex/fontes.bib"
SAIDA_MD = RAIZ / "relatorio/inventario_fontes.md"
SAIDA_CSV = RAIZ / "relatorio/inventario_fontes.csv"
PASTAS = {"visualizacoes": "gráfico", "mapas": "mapa", "tabelas_finais": "tabela"}

CORINGA = "\x00"          # trecho que a leitura estática não resolve (vira `.+` na busca no disco)
MAX_COMBINACOES = 400      # teto de expansão de laços aninhados


# ---------------------------------------------------------------------------------------------
# Avaliação estática de expressões de string
# ---------------------------------------------------------------------------------------------
def avalia(no, env):
    """Lista de valores possíveis (str) de uma expressão; CORINGA onde não resolve."""
    if isinstance(no, ast.Constant):
        return [no.value if isinstance(no.value, str) else str(no.value)]
    if isinstance(no, ast.Name):
        return env.get(no.id, [CORINGA])
    if isinstance(no, ast.JoinedStr):
        partes = []
        for v in no.values:
            if isinstance(v, ast.Constant):
                partes.append([v.value])
            elif isinstance(v, ast.FormattedValue):
                partes.append(avalia(v.value, env))
        return _produto(partes)
    if isinstance(no, ast.BinOp) and isinstance(no.op, ast.Add):
        return _produto([avalia(no.left, env), avalia(no.right, env)])
    if isinstance(no, ast.BoolOp) and isinstance(no.op, ast.Or):
        return avalia(no.values[-1], env)
    if isinstance(no, ast.Call) and isinstance(no.func, ast.Name) and no.func.id in env.get("__funcoes__", {}):
        params, retorno = env["__funcoes__"][no.func.id]
        local = dict(env)
        for p, a in zip(params, no.args):
            local[p] = avalia(a, env)
        return avalia(retorno, local)
    return [CORINGA]


def _produto(partes):
    saida = ["".join(c) for c in itertools.islice(itertools.product(*partes), MAX_COMBINACOES)]
    return list(dict.fromkeys(saida)) or [CORINGA]


def valores_iteraveis(no, env):
    """Para `for alvo in <no>`: lista de elementos (cada um str ou tupla de str), ou None."""
    if isinstance(no, ast.Name) and no.id in env.get("__listas__", {}):
        return env["__listas__"][no.id]
    if isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute) and no.func.attr == "items":
        base = no.func.value
        if isinstance(base, ast.Name) and base.id in env.get("__dicts__", {}):
            return env["__dicts__"][base.id]
    if isinstance(no, (ast.List, ast.Tuple)):
        elems = []
        for e in no.elts:
            if isinstance(e, (ast.Tuple, ast.List)):
                elems.append(tuple(avalia(x, env)[0] for x in e.elts))
            else:
                elems.append(avalia(e, env)[0])
        return elems
    if isinstance(no, ast.Dict):
        return [(avalia(k, env)[0], avalia(v, env)[0]) for k, v in zip(no.keys, no.values) if k is not None]
    return None


def liga_alvo(alvo, elem, env):
    if isinstance(alvo, ast.Name):
        env[alvo.id] = [elem if isinstance(elem, str) else CORINGA]
    elif isinstance(alvo, (ast.Tuple, ast.List)):
        itens = elem if isinstance(elem, tuple) else ()
        for i, sub in enumerate(alvo.elts):
            liga_alvo(sub, itens[i] if i < len(itens) else CORINGA, env)


# ---------------------------------------------------------------------------------------------
# Leitura de analise.py
# ---------------------------------------------------------------------------------------------
def funcoes_simples(arvore):
    """{nome: (params, expr)} das funções de topo cujo último comando é `return <expr>` de texto."""
    out = {}
    for no in arvore.body:
        if isinstance(no, ast.FunctionDef) and no.body and isinstance(no.body[-1], ast.Return) and no.body[-1].value is not None:
            if isinstance(no.body[-1].value, (ast.JoinedStr, ast.Constant, ast.BinOp)):
                out[no.name] = ([a.arg for a in no.args.args], no.body[-1].value)
    return out


def helpers_que_gravam(arvore):
    """{nome_funcao: info} para toda função de topo que chama savefig (pasta, parâmetros, default)."""
    helpers = {}
    for no in arvore.body:
        if not isinstance(no, ast.FunctionDef):
            continue
        saves = [n for n in ast.walk(no) if isinstance(n, ast.Call) and getattr(n.func, "attr", None) == "savefig"]
        if not saves:
            continue
        caminho = ast.unparse(saves[0].args[0]) if saves[0].args else ""
        pasta = next((p for p in PASTAS if p in caminho), "visualizacoes")
        params = [a.arg for a in no.args.args]
        defaults = dict(zip(params[len(params) - len(no.args.defaults):], no.args.defaults))
        padrao_nome = None
        for n in ast.walk(no):   # `nome_arquivo = nome_arquivo or f"{valor}_{tempo}"`
            if (isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "nome_arquivo"
                    and isinstance(n.value, ast.BoolOp)):
                padrao_nome = n.value.values[-1]
        helpers[no.name] = dict(pasta=pasta, params=params, defaults=defaults, padrao_nome=padrao_nome, linha=no.lineno)
    return helpers


class Leitor(ast.NodeVisitor):
    def __init__(self, helpers):
        self.helpers = helpers
        self.env = {"__listas__": {}, "__dicts__": {}, "__funcoes__": {}}
        self.registros = []          # dicts: tipo, padroes (lista de str com CORINGA), titulo, fonte, funcao, linha, metodo
        self.fonte_vigente = None    # última fonte vista (para tabelas e savefig soltos)
        self.titulo_vigente = None

    # atribuições de string / listas literais
    def visit_Assign(self, no):
        valor = no.value
        for alvo in no.targets:
            if isinstance(alvo, ast.Name):
                if isinstance(valor, (ast.List, ast.Tuple)):
                    elems = valores_iteraveis(valor, self.env)
                    if elems is not None:
                        self.env["__listas__"][alvo.id] = elems
                elif isinstance(valor, ast.Dict):
                    self.env["__dicts__"][alvo.id] = valores_iteraveis(valor, self.env)
                vals = avalia(valor, self.env)
                if vals != [CORINGA]:
                    self.env[alvo.id] = vals
                else:
                    self.env.pop(alvo.id, None)
                if alvo.id.startswith("fonte") and vals != [CORINGA]:
                    self.fonte_vigente = vals[0]
        self.generic_visit(no)

    def visit_For(self, no):
        elems = valores_iteraveis(no.iter, self.env)
        if not elems:
            liga_alvo(no.target, CORINGA, self.env)
            for s in no.body:
                self.visit(s)
            return
        # visita o corpo uma vez com cada alvo ligado a TODOS os valores (union), o que expande os padrões
        nomes = {}
        for elem in elems:
            tmp = {}
            liga_alvo(no.target, elem, tmp)
            for k, v in tmp.items():
                nomes.setdefault(k, [])
                nomes[k] += [x for x in v if x not in nomes[k]]
        self._laco_combinado = getattr(self, "_laco_combinado", [])
        self._laco_combinado.append((no.target, elems))
        for k, v in nomes.items():
            self.env[k] = v
        for s in no.body:
            self.visit(s)
        self._laco_combinado.pop()

    def visit_Call(self, no):
        nome = no.func.id if isinstance(no.func, ast.Name) else getattr(no.func, "attr", None)
        if nome in self.helpers:
            self._helper(no, nome)
        elif nome == "savefig" and no.args:
            self._registra("solto", avalia(no.args[0], self.env), self.titulo_vigente, self.fonte_vigente,
                           "plt.savefig", no.lineno, "vizinhança")
        elif nome == "title" and no.args:
            self.titulo_vigente = avalia(no.args[0], self.env)[0]
        elif nome == "to_csv" and no.args:
            caminhos = avalia(no.args[0], self.env)
            if any("tabelas_finais" in c for c in caminhos):
                self._registra("tabela", caminhos, None, self.fonte_vigente, "to_csv", no.lineno, "vizinhança")
        self.generic_visit(no)

    def _helper(self, no, nome):
        h = self.helpers[nome]
        ligados = {}
        for i, a in enumerate(no.args):
            if i < len(h["params"]):
                ligados[h["params"][i]] = a
        for kw in no.keywords:
            if kw.arg:
                ligados[kw.arg] = kw.value
        env_local = dict(self.env)
        for p, expr in ligados.items():
            env_local[p] = avalia(expr, self.env)
        if "nome_arquivo" in ligados:
            nomes = env_local["nome_arquivo"]
        elif h["padrao_nome"] is not None:
            nomes = avalia(h["padrao_nome"], env_local)
        else:
            nomes = [CORINGA]
        titulo = env_local.get("titulo", [None])[0]
        fonte = env_local.get("fonte_dados", [None])[0] if "fonte_dados" in ligados else None
        if fonte:
            self.fonte_vigente = fonte
        caminhos = [f"{h['pasta']}/{n}.png" for n in nomes]
        self._registra("figura", caminhos, titulo, fonte, nome, no.lineno, "chamada" if fonte else "sem fonte_dados")

    def _registra(self, tipo, caminhos, titulo, fonte, funcao, linha, metodo):
        self.registros.append(dict(tipo=tipo, caminhos=[c.replace("//", "/") for c in caminhos], titulo=titulo,
                                   fonte=fonte, funcao=funcao, linha=linha, metodo=metodo))


def padrao_para_regex(caminho):
    partes = [re.escape(p) for p in caminho.split(CORINGA)]
    return re.compile("^" + ".+".join(partes) + "$")


# ---------------------------------------------------------------------------------------------
# fontes.bib e estrutura_eixos.md
# ---------------------------------------------------------------------------------------------
def le_bib():
    texto = BIB.read_text(encoding="utf-8")
    entradas = {}
    for m in re.finditer(r"@\w+\{(\w+),(.*?)\n\}", texto, re.S):
        chave, corpo = m.group(1), m.group(2)
        campos = {k.lower(): v.strip() for k, v in re.findall(r"^\s*(\w+)\s*=\s*\{(.*)\},?\s*$", corpo, re.M)}
        padroes = [re.compile(p.strip(), re.I) for p in campos.get("padroes", "").split("||") if p.strip()]
        entradas[chave] = dict(titulo=campos.get("title", "").strip("{}"), padroes=padroes,
                               conferir=campos.get("conferir"), autor=re.sub(r"\\entidade\{([^}]*)\}", r"\1", campos.get("author", "")).strip("{}"))
    return entradas


def chaves_da_fonte(texto, bib):
    if not texto:
        return []
    return [k for k, e in bib.items() if any(p.search(texto) for p in e["padroes"])]


def mapa_estrutura():
    """arquivo -> lista de (eixo, subseção, fonte do .md, campo)."""
    usos = defaultdict(list)
    for eixo in parse_estrutura_eixos(str(RAIZ / "specs/estrutura_eixos.md")):
        for sub in eixo["subsecoes"]:
            campos = sub["campos"]
            for campo in ("visualização", "mapa", "tabela"):
                vals = campos.get(campo) or []
                for v in ([vals] if isinstance(vals, str) else vals):
                    arq = v.strip().strip("`").strip()
                    if arq:
                        usos[arq].append((eixo["eixo"], sub["titulo"], campos.get("fonte"), campo))
    return usos


# ---------------------------------------------------------------------------------------------
def coleta():
    """(linhas, alertas, bib): uma linha por arquivo no disco -- também usada por gera_latex.py."""
    arvore = ast.parse(ANALISE.read_text(encoding="utf-8"))
    helpers = helpers_que_gravam(arvore)
    leitor = Leitor(helpers)
    leitor.env["__funcoes__"] = funcoes_simples(arvore)
    for no in arvore.body:
        if not isinstance(no, ast.FunctionDef):   # corpo das funções não é chamada; só o topo
            leitor.visit(no)

    comentados = set(re.findall(r"^#.*nome_arquivo\s*=\s*['\"]([\w\-]+)['\"]", ANALISE.read_text(encoding="utf-8"), re.M))
    comentados |= {Path(c).name for c in re.findall(r"^#.*to_csv\(['\"]([^'\"]+)['\"]", ANALISE.read_text(encoding="utf-8"), re.M)}
    regen = RAIZ / ".claude/skills/export_pdf_report/scripts/regen_missing_pngs.py"
    regen_txt = regen.read_text(encoding="utf-8") if regen.exists() else ""
    regravados = set(re.findall(r"nome_arquivo=['\"]([\w\-]+)['\"]", regen_txt)) | set(re.findall(r"\{OUT\}/([\w\-]+)\.png", regen_txt))
    bib = le_bib()
    usos = mapa_estrutura()
    disco = {f"{p}/{f.name}": PASTAS[p] for p in PASTAS for f in (RAIZ / p).glob("*")
             if f.suffix in (".png", ".csv")}

    # arquivo no disco -> registros de analise.py que o geram
    origem = defaultdict(list)
    padroes_sem_arquivo = []
    for r in leitor.registros:
        achou = False
        for c in r["caminhos"]:
            rx = padrao_para_regex(c)
            for arq in disco:
                if rx.match(arq):
                    origem[arq].append(r)
                    achou = True
        if not achou:
            padroes_sem_arquivo.append(r)

    linhas, alertas = [], defaultdict(list)
    for arq, tipo in sorted(disco.items(), key=lambda kv: (kv[1], kv[0])):
        nome = arq.split("/", 1)[1]
        regs = origem.get(arq, [])
        r = next((x for x in regs if x["fonte"]), regs[0] if regs else None)
        fonte_py = r["fonte"] if r else None
        uso = usos.get(nome, [])
        fonte_md = "; ".join(dict.fromkeys(u[2] or "" for u in uso)) or None
        if tipo == "tabela" and fonte_md:
            fonte_py, metodo = None, "estrutura_eixos.md"
        else:
            metodo = (r or {}).get("metodo") or ("estrutura_eixos.md" if fonte_md else "")
        fonte_ok = fonte_py and CORINGA not in fonte_py
        chaves = (chaves_da_fonte(fonte_py, bib) if fonte_py else []) or chaves_da_fonte(fonte_md, bib)
        if tipo == "mapa" and "ipp_limites_bairros" not in chaves:
            chaves.append("ipp_limites_bairros")   # todo mapa usa a malha de bairros (IPP/Data.Rio)
        stem = Path(nome).stem
        linhas.append(dict(
            arquivo=arq, tipo=tipo,
            eixo=" | ".join(dict.fromkeys(u[0] for u in uso)), subsecao=" | ".join(dict.fromkeys(u[1] for u in uso)),
            no_relatorio="sim" if uso else "não",
            titulo=(r or {}).get("titulo") or "", fonte_analise=(fonte_py or "").replace(CORINGA, "…"),
            fonte_estrutura=fonte_md or "", chaves_bib=", ".join(chaves),
            funcao=(r or {}).get("funcao") or "", linha=(r or {}).get("linha") or "",
            metodo_fonte=metodo,
            observacao="; ".join(x for x in [
                "chamada comentada em analise.py (arquivo antigo)" if not regs and (stem in comentados or nome in comentados) else "",
                "regravado por regen_missing_pngs.py (cópia sem fonte)" if stem in regravados and tipo != "tabela" else ""] if x),
        ))
        if not regs and (stem in comentados or nome in comentados) and uso:
            alertas["Usado no relatório, mas a chamada que o gera está comentada em analise.py (arquivo antigo no disco)"].append(arq)
        elif not regs and stem in regravados and uso:
            alertas["Usado no relatório, mas só regen_missing_pngs.py o gera (não há chamada em analise.py)"].append(arq)
        if regs and stem in regravados and tipo != "tabela":
            alertas["Gráfico do notebook que regen_missing_pngs.py regrava com uma cópia própria, sem `fonte_dados`"].append(arq)
        if not regs and not uso:
            alertas["Arquivo no disco que nenhuma chamada ativa de analise.py gera e que o relatório não usa (candidato a limpeza)"].append(arq)
        if not uso:
            alertas["Arquivo no disco que nenhuma subseção de estrutura_eixos.md usa"].append(arq)
        if uso and not chaves:
            alertas["Arquivo do relatório sem fonte ligada a uma entrada de fontes.bib"].append(
                f"{arq} — analise.py: {fonte_py or '(sem fonte_dados)'}; .md: {fonte_md or '(sem fonte:)'}")
        if uso and fonte_ok and fonte_md:
            ch_py, ch_md = set(chaves_da_fonte(fonte_py, bib)), set(chaves_da_fonte(fonte_md, bib))
            if ch_md and ch_py and not (ch_md & ch_py):
                alertas["`fonte:` do .md aponta para base diferente do `fonte_dados` do analise.py"].append(
                    f"{arq} — .md: “{fonte_md}” → {sorted(ch_md)}; analise.py: “{fonte_py}” → {sorted(ch_py)}")
        if tipo != "tabela" and regs and all(not x["fonte"] for x in regs):
            alertas["Figura gerada sem `fonte_dados` (constituição §3: toda visualização cita a fonte)"].append(
                f"{arq} — {r['funcao']}, linha {r['linha']}")
        if tipo != "tabela" and fonte_ok and fonte_md and not (set(chaves_da_fonte(fonte_md, bib)) >= set(chaves_da_fonte(fonte_py, bib))):
            alertas["Informativo: `fonte:` do .md e `fonte_dados` do analise.py citam conjuntos de bases diferentes"].append(
                f"{arq} — .md: “{fonte_md}”; analise.py: “{fonte_py}”")
    for nome, lst in usos.items():
        if not any(l["arquivo"].endswith("/" + nome) for l in linhas):
            alertas["Referência em estrutura_eixos.md sem arquivo no disco"].append(nome)
    for r in padroes_sem_arquivo:
        alertas["Saída de analise.py sem arquivo correspondente no disco (não gerada nesta máquina?)"].append(
            f"{r['caminhos'][0].replace(CORINGA, '*')} — {r['funcao']}, linha {r['linha']}")
    for k, e in bib.items():
        if not any(k in l["chaves_bib"].split(", ") for l in linhas):
            alertas["Entrada de fontes.bib que nenhum arquivo usa"].append(k)
    textos_md = {u[2] for us in usos.values() for u in us if u[2]}
    for t in sorted(textos_md):
        if not chaves_da_fonte(t, bib):
            alertas["Texto `fonte:` de estrutura_eixos.md que não casa com nenhuma entrada de fontes.bib"].append(t)

    return linhas, alertas, bib


def main():
    linhas, alertas, bib = coleta()
    escreve_csv(linhas)
    escreve_md(linhas, alertas, bib)
    print(f"{len(linhas)} arquivos ({sum(l['no_relatorio'] == 'sim' for l in linhas)} no relatório), "
          f"{sum(len(v) for v in alertas.values())} alertas em {len(alertas)} tipos -> {SAIDA_MD.relative_to(RAIZ)}")


def escreve_csv(linhas):
    with SAIDA_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(linhas)


def _md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def escreve_md(linhas, alertas, bib):
    out = [
        "# Inventário de fontes",
        "",
        f"> Gerado por `relatorio/latex/build/inventario_fontes.py` em {date.today():%d/%m/%Y} — **não editar à mão**.",
        "> Documento de conferência da equipe (`specs/relatorio_latex` §7); não entra no relatório.",
        "> Cruza `analise.py` (leitura estática), `specs/estrutura_eixos.md` e `relatorio/latex/fontes.bib`.",
        "> A versão em planilha, com todos os campos, é `relatorio/inventario_fontes.csv` (separador `;`).",
        "",
        "## Resumo",
        "",
        "| | Gráficos | Mapas | Tabelas |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for rotulo, filtro in [("No disco", lambda l: True), ("No relatório (estrutura_eixos.md)", lambda l: l["no_relatorio"] == "sim"),
                           ("Com fonte ligada ao fontes.bib", lambda l: bool(l["chaves_bib"]))]:
        cont = [sum(1 for l in linhas if l["tipo"] == t and filtro(l)) for t in ("gráfico", "mapa", "tabela")]
        out.append(f"| {rotulo} | {cont[0]} | {cont[1]} | {cont[2]} |")

    out += ["", "## 1. Por fonte", "",
            "Cada entrada de `fontes.bib` (lista **Fontes** do relatório) e o que ela gera. Só arquivos que entram "
            "no relatório; os demais estão na seção 2. Um arquivo com fonte composta (ex. casos do Sinan ÷ população "
            "do Censo) aparece em mais de uma fonte.", ""]
    for chave, e in bib.items():
        doc = [l for l in linhas if chave in l["chaves_bib"].split(", ") and l["no_relatorio"] == "sim"]
        out.append(f"### {e['titulo']}")
        out.append("")
        out.append(f"`{chave}` — {e['autor']}" + (f"  \n⚠️ **Conferir:** {e['conferir']}" if e["conferir"] else ""))
        out.append("")
        if not doc:
            out += ["_Nenhum arquivo do relatório._", ""]
            continue
        out += ["| Tipo | Arquivo | Eixo › subseção |", "| :--- | :--- | :--- |"]
        for l in sorted(doc, key=lambda l: (l["tipo"], l["arquivo"])):
            out.append(f"| {l['tipo']} | `{l['arquivo'].split('/', 1)[1]}` | {_md(_eixo_curto(l['eixo']))} › {_md(l['subsecao'])} |")
        out.append("")

    out += ["## 2. Por arquivo", "",
            "Todos os gráficos, mapas e tabelas no disco. **Fonte (analise.py)** é o `fonte_dados` da chamada que "
            "gera o arquivo; para tabelas, a última fonte vista antes do `to_csv` (método *vizinhança* — confira). "
            "**Fonte (.md)** é o campo `fonte:` da subseção em `estrutura_eixos.md`.", ""]
    for tipo in ("gráfico", "mapa", "tabela"):
        sel = [l for l in linhas if l["tipo"] == tipo]
        out += [f"### {tipo.capitalize()}s ({len(sel)})", "",
                "| Arquivo | No relatório | Eixo › subseção | Fonte (analise.py) | Fonte (.md) | Fontes.bib | Origem | Observação |",
                "| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |"]
        for l in sel:
            origem = f"`{l['funcao']}` l.{l['linha']} ({l['metodo_fonte']})" if l["funcao"] else "—"
            out.append(f"| `{l['arquivo'].split('/', 1)[1]}` | {l['no_relatorio']} | "
                       f"{_md(_eixo_curto(l['eixo']) + ' › ' + l['subsecao']) if l['eixo'] else '—'} | "
                       f"{_md(l['fonte_analise']) or '—'} | {_md(l['fonte_estrutura']) or '—'} | {l['chaves_bib'] or '—'} | {origem} | {l['observacao'] or ''} |")
        out.append("")

    out += ["## 3. Alertas", "", "Apontados, não corrigidos — cada item pede uma decisão da equipe.", ""]
    if not alertas:
        out.append("Nenhum.")
    for titulo, itens in alertas.items():
        out += [f"### {titulo} ({len(itens)})", ""] + [f"- {_md(i)}" for i in sorted(set(itens))] + [""]
    pend = [(k, e["conferir"]) for k, e in bib.items() if e["conferir"]]
    out += ["## 4. Referências a confirmar (`conferir` em fontes.bib)", ""] + [f"- `{k}`: {c}" for k, c in pend] + [""]
    SAIDA_MD.write_text("\n".join(out), encoding="utf-8")


def _eixo_curto(eixo):
    return re.sub(r"^[^\wÀ-ÿ]+", "", eixo.split(" | ")[0]).split(" (")[0] + (" …" if " | " in eixo else "")


if __name__ == "__main__":
    main()
