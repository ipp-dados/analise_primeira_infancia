# -*- coding: utf-8 -*-
"""Extração mecânica das funções auxiliares de `analise.py` para o pacote `primeira_infancia/`
(specs/2026-09-28_organizacao, fase 1b). Rodado uma vez, a partir da raiz, sobre o `analise.py` de `staging_main`
8dbf8c3; fica versionado aqui como registro de como o pacote foi gerado (não é pipeline).

    python specs/2026-09-28_organizacao/extrai_modulos.py [--gravar]

Sem `--gravar`, só relata (módulos, dependências, conferências). Regras:
- cada definição de primeiro nível (def, class, atribuição) das linhas 1-1897 vai inteira, na ordem original, para o
  módulo da subseção em que está (`CORTES`), exceto os nomes de `ESTILO` (camada de estilo, que quebra o ciclo
  gráficos ↔ impressão ↔ mapas) e `_limite_escala_p95` (definida no meio da seção Proteção, vai para `protecao`);
- os comentários logo acima de uma definição vão junto; marcadores `# %%` saem; o texto das células markdown de cada
  subseção vira a docstring do módulo;
- imports: cada módulo importa só os nomes externos que usa (mesma instrução do original) e, dos módulos irmãos, os
  nomes auxiliares que usa (`from .x import ...`); `__all__` lista todo nome definido (inclusive os com `_`, que as
  seções de análise usam), para `from primeira_infancia import *` reproduzir o espaço de nomes de antes;
- falha se o grafo de imports tiver ciclo ou se algum nome usado não for resolvido.
"""
import ast
import builtins
import re
import sys
from pathlib import Path

ORIGEM = Path("analise.py")
DESTINO = Path("primeira_infancia")
FIM_AUXILIARES = 1898   # "### ⚙️ Setup": daqui em diante é o notebook
CORTES = [(36, "conexao"), (64, "limpeza"), (336, "graficos"), (464, "mapas"), (767, "impressao"),
          (1307, "protecao"), (1509, "cadunico"), (1655, "populacao"), (1795, "educacao")]
ESTILO = {"_PALETA_CATEGORICA", "_CORES_TEMA_MAPA", "_LIMIAR_DESTAQUE_SERIES", "_N_SERIES_DESTACADAS",
          "_COR_SERIE_APAGADA", "_COR_FONTE_RODAPE", "_FONTE_TITULO", "_PROVEDORES_FUNDO", "_numero_ptbr",
          "_adiciona_rotulos_municipios_vizinhos", "_ZONA_LEGENDA"}
AVULSAS = {"_limite_escala_p95": "protecao"}
ORDEM = ["conexao", "limpeza", "estilo", "impressao", "graficos", "mapas", "protecao", "cadunico", "populacao", "educacao"]
TITULOS = {"estilo": "Identidade visual compartilhada por gráficos, mapas e variante de impressão: paletas, fonte dos "
                     "títulos, provedores de fundo cartográfico, formatação de números pt-BR e rótulos dos municípios "
                     "vizinhos. Separada em specs/2026-09-28_organizacao para quebrar o ciclo gráficos ↔ impressão ↔ mapas."}

src = ORIGEM.read_text(encoding="utf-8")
linhas = src.split("\n")
arvore = ast.parse(src)


def modulo_da_linha(n):
    m = None
    for ini, nome in CORTES:
        if n >= ini:
            m = nome
    return m


def nomes_definidos(no):
    if isinstance(no, (ast.FunctionDef, ast.ClassDef)):
        return [no.name]
    if isinstance(no, (ast.Assign, ast.AnnAssign)):
        alvos = no.targets if isinstance(no, ast.Assign) else [no.target]
        return [x.id for t in alvos for x in ast.walk(t) if isinstance(x, ast.Name)]
    return []


def nomes_importados(no):
    return [(a.asname or a.name).split(".")[0] for a in no.names]


# 1. imports externos: nome -> instrução de import (texto) que o cria
importa = {}
for no in arvore.body:
    if no.lineno >= FIM_AUXILIARES or not isinstance(no, (ast.Import, ast.ImportFrom)):
        continue
    for a in no.names:
        nome = (a.asname or a.name).split(".")[0]
        if isinstance(no, ast.Import):
            importa[nome] = f"import {a.name}" + (f" as {a.asname}" if a.asname else "")
        else:
            importa[nome] = f"from {no.module} import {a.name}" + (f" as {a.asname}" if a.asname else "")

# 2. definições -> módulo, com o trecho de fonte (comentários logo acima inclusos)
defs = []          # (modulo, nomes, texto, no)
fim_anterior = 0
for no in arvore.body:
    if isinstance(no, (ast.Import, ast.ImportFrom)) and no.lineno < FIM_AUXILIARES:
        fim_anterior = no.end_lineno
        continue
    nomes = nomes_definidos(no)
    avulsa = isinstance(no, ast.FunctionDef) and no.name in AVULSAS
    if no.lineno >= FIM_AUXILIARES and not avulsa:
        continue
    if not nomes and no.lineno < FIM_AUXILIARES:
        # expressão solta (docstring/constante) na região auxiliar: não deve existir
        if not (isinstance(no, ast.Expr) and isinstance(no.value, ast.Constant)):
            sys.exit(f"instrução com efeito na região auxiliar (linha {no.lineno}): {ast.dump(no)[:80]}")
        continue
    # decoradores (@_a4_seguro) ficam acima da linha do def: o trecho começa no primeiro deles
    ini = min([no.lineno] + [d.lineno for d in getattr(no, "decorator_list", [])]) - 1
    if not avulsa:
        # comentários imediatamente acima (sem linha em branco no meio), sem marcadores de célula
        k = ini - 1
        while k > fim_anterior - 1 and linhas[k].startswith("#") and not linhas[k].startswith("# %%"):
            k -= 1
        bloco_com = [l for l in linhas[k + 1:ini] if not l.startswith("# %%")]
        # descarta comentário que é texto de célula markdown (logo após um "# %% [markdown]")
        if k >= 0 and linhas[k].startswith("# %% [markdown]"):
            bloco_com = []
    else:
        bloco_com = []
    texto = "\n".join(bloco_com + linhas[ini:no.end_lineno])
    if avulsa:
        modulo = AVULSAS[no.name]
    elif set(nomes) & ESTILO:
        modulo = "estilo"
    else:
        modulo = modulo_da_linha(no.lineno)
    defs.append((modulo, nomes, texto, no))
    fim_anterior = no.end_lineno

onde = {}
for modulo, nomes, _, _ in defs:
    for n in nomes:
        onde[n] = modulo

# 3. docstring de cada módulo = texto das células markdown da subseção
docs = {m: [] for m in ORDEM}
em_markdown = False
for i, l in enumerate(linhas[:FIM_AUXILIARES - 1], start=1):
    if l.startswith("# %%"):
        em_markdown = l.startswith("# %% [markdown]")
        continue
    if em_markdown and i >= CORTES[0][0]:
        docs[modulo_da_linha(i)].append(re.sub(r"^# ?", "", l))

# 4. nomes usados por módulo
usos = {m: set() for m in ORDEM}
for modulo, nomes, _, no in defs:
    for x in ast.walk(no):
        if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load):
            usos[modulo].add(x.id)
        elif isinstance(x, ast.Attribute):
            pass

dep = {m: {} for m in ORDEM}
externos = {m: set() for m in ORDEM}
for m in ORDEM:
    proprios = {n for mod, nomes, _, _ in defs if mod == m for n in nomes}
    for n in usos[m]:
        if n in proprios:
            continue
        if n in onde:
            dep[m].setdefault(onde[n], set()).add(n)
        elif n in importa:
            externos[m].add(n)

# locais (parâmetros, variáveis) não devem aparecer como não resolvidos: confere só nomes globais livres por função
nao_resolvidos = set()
for modulo, nomes, _, no in defs:
    if not isinstance(no, ast.FunctionDef):
        livres = {x.id for x in ast.walk(no) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)}
        locais = set()
    else:
        locais = {a.arg for a in ast.walk(no) if isinstance(a, ast.arg)}
        locais |= {x.id for x in ast.walk(no) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store)}
        for x in ast.walk(no):
            if isinstance(x, (ast.FunctionDef,)):
                locais.add(x.name)
            if isinstance(x, (ast.Import, ast.ImportFrom)):
                locais |= set(nomes_importados(x))
            if isinstance(x, ast.ExceptHandler) and x.name:
                locais.add(x.name)
        livres = {x.id for x in ast.walk(no) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)}
    for n in livres - locais:
        if n not in onde and n not in importa and not hasattr(builtins, n):
            nao_resolvidos.add((modulo, n))
if nao_resolvidos:
    sys.exit(f"nomes não resolvidos: {sorted(nao_resolvidos)}")

# 5. ciclo?
visitando, feito = set(), []


def visita(m, pilha):
    if m in pilha:
        for a, b in zip(pilha + [m], (pilha + [m])[1:]):
            print(f"  {a} usa de {b}: {sorted(dep[a].get(b, []))}")
        sys.exit(f"ciclo de imports: {' -> '.join(pilha + [m])}")
    if m in feito:
        return
    for d in dep[m]:
        visita(d, pilha + [m])
    feito.append(m)


for m in ORDEM:
    visita(m, [])

for m in ORDEM:
    print(f"{m:10s} {sum(len(n) for mod, n, _, _ in defs if mod == m):3d} nomes | usa {sorted(dep[m]) or '-'} | externos {sorted(externos[m])}")

if "--gravar" not in sys.argv:
    sys.exit(0)

# 6. grava o pacote
DESTINO.mkdir(exist_ok=True)
for m in ORDEM:
    doc = "\n".join(docs.get(m) or []).strip() or TITULOS.get(m, "")
    doc = re.sub(r"\n{3,}", "\n\n", doc).replace('"""', "'''")
    cab = [
        "# -*- coding: utf-8 -*-",
        '"""' + doc + "\n\nExtraído de analise.py sem mudança de código (specs/2026-09-28_organizacao, fase 1b)."
        "\n"'"""',
    ]
    imps = sorted({importa[n] for n in externos[m]}, key=lambda s: (not s.startswith("import"), s))
    cab += imps
    for d in ORDEM:
        if d in dep[m]:
            nomes = sorted(dep[m][d])
            cab.append(f"from .{d} import ({', '.join(nomes)})" if len(", ".join(nomes)) > 80 else f"from .{d} import {', '.join(nomes)}")
    nomes_mod = [n for mod, nomes, _, _ in defs if mod == m for n in nomes]
    corpo = "\n\n".join(t for mod, _, t, _ in defs if mod == m)
    todos = "__all__ = [\n" + "".join(f"    {n!r},\n" for n in dict.fromkeys(nomes_mod)) + "]\n"
    (DESTINO / f"{m}.py").write_text("\n".join(cab) + "\n\n" + todos + "\n\n" + corpo + "\n", encoding="utf-8")

init = ['# -*- coding: utf-8 -*-',
        '"""Funções auxiliares do notebook `analise.py` (limpeza, carga por fonte, gráficos, mapas, variante de',
        'impressão). Pacote criado em specs/2026-09-28_organizacao (fase 1b): antes eram as linhas 1-1897 de',
        '`analise.py`. `from primeira_infancia import *` traz todos os nomes (inclusive os com `_`, usados pelas seções).',
        '"""']
init += [f"from .{m} import *  # noqa: F401,F403" for m in ORDEM]
init += ["from . import " + ", ".join(ORDEM) + "  # noqa: E402", "",
         "__all__ = [n for m in (" + ", ".join(ORDEM) + ") for n in m.__all__]", ""]
(DESTINO / "__init__.py").write_text("\n".join(init), encoding="utf-8")

# 7. analise.py fino: título, célula de pacotes (imports originais + do pacote), notebook a partir do Setup,
#    sem a definição avulsa de _limite_escala_p95
imports_originais = [linhas[no.lineno - 1:no.end_lineno] for no in arvore.body
                     if isinstance(no, (ast.Import, ast.ImportFrom)) and no.lineno < FIM_AUXILIARES]
bloco_imports = "\n".join(l for trecho in imports_originais for l in trecho)
cabecalho = "\n".join(linhas[:8]) + "\n" + """# %% [markdown]
# ---
# ## 📦 Pacotes e Funções Auxiliares
#
# Conexão com o banco e todas as funções de limpeza/wrangling e de visualização reutilizadas ao longo do
# notebook ficam no pacote `primeira_infancia/` (specs/2026-09-28_organizacao), um módulo por tema:
# `conexao` (banco CTPE), `limpeza` (Tabnet/DataSUS, SISVAN, causas evitáveis, SIDRA), `estilo` (paletas,
# fontes, fundo cartográfico), `graficos` (`serie_temporal`, `grafico_barra`, …), `mapas`
# (`mapa_coropletico_bairros`, `agrega_bairros_por_nivel`), `impressao` (variante A4 do relatório PDF,
# `GERA_VARIANTE_A4`), `protecao` (SINAN, violência), `cadunico` (recortes e supressão < 20),
# `populacao` (Ripsa/MS) e `educacao` (Censo Escolar/INEP). As seções abaixo só *chamam* essas funções;
# lógica reutilizável nova vai para o módulo do tema, não para uma célula daqui.

# %%
""" + bloco_imports + "\nfrom primeira_infancia import *  # noqa: F401,F403\n"
resto = linhas[FIM_AUXILIARES - 2:]   # a partir do "# %% [markdown]" que abre o Setup
texto_resto = "\n".join(resto)
avulsa = next(no for no in arvore.body if isinstance(no, ast.FunctionDef) and no.name == "_limite_escala_p95")
trecho = "\n".join(linhas[avulsa.lineno - 1:avulsa.end_lineno]) + "\n\n"
assert texto_resto.count(trecho) == 1
texto_resto = texto_resto.replace(trecho, "", 1)
assert linhas[FIM_AUXILIARES - 2].startswith("# %% [markdown]") and "Setup" in linhas[FIM_AUXILIARES - 1]
ORIGEM.write_text(cabecalho + "\n" + texto_resto, encoding="utf-8")
print("gravado:", sorted(p.name for p in DESTINO.glob("*.py")), "e analise.py")
