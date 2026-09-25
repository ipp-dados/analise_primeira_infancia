"""Gera o relatório final em LaTeX e compila o PDF (specs/relatorio_latex, Blocos 2-4).

Lê, em tempo de build (nada de agrupamento fixo no código):
  - specs/estrutura_eixos.md      -> capítulos (## eixo) e seções (### indicador), na ordem do arquivo;
  - relatorio/textos_curados.json -> texto de cada figura (chave = nome do arquivo sem extensão), a
                                     introdução, o resumo, as sínteses e as considerações finais;
                                     sem texto curado, lorem determinístico idêntico ao do site (D4);
  - inventário de fontes          -> título e fonte de cada figura (inventario_fontes.coleta());
  - tabelas_finais/*.csv          -> apêndices (tabelas.py).

Escreve relatorio/latex/gerado/*.tex (não editar à mão), reduz as imagens para o cache em _build/,
roda latexmk -xelatex (PDF em relatorio/latex/_build/relatorio.pdf; com --publicar, copiado para
relatorio/analise_primeira_infancia.pdf -- specs/relatorio_latex D2: só depois da validação).

Uso (da raiz do projeto):  python relatorio/latex/build/gera_latex.py [--sem-pdf] [--eixo N] [--publicar]
  --sem-pdf   só gera os .tex (sem compilar)
  --eixo N    só o eixo N (1-6) no corpo -- para iterar no visual sem compilar o documento inteiro
  --publicar  copia o PDF para relatorio/analise_primeira_infancia.pdf (padrão: fica em relatorio/latex/_build/)
"""
import argparse
import json
import random
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

from PIL import Image

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
LATEX = RAIZ / "relatorio/latex"
GERADO = LATEX / "gerado"
CACHE = LATEX / "_build/img"
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(RAIZ / ".claude/skills/export_pdf_report/scripts"))
from gera_estrutura_eixos import parse_estrutura_eixos, valida_estrutura  # noqa: E402
import inventario_fontes  # noqa: E402
import tabelas  # noqa: E402

TEXTOS = json.loads((RAIZ / "relatorio/textos_curados.json").read_text(encoding="utf-8"))

# rótulo curto e ícone por eixo -- os mesmos do site (website/build/build_site.py, _EIXO_META)
EIXO_META = [("prioridade", "target"), ("inclus", "handshake"), ("fam", "users"),
             ("prote", "shield-check"), ("aliment", "apple"), ("moradia", "house")]
PALAVRAS_CHAVE = "Primeira infância. Indicadores sociais. Políticas públicas. Rio de Janeiro (RJ)."


# ------------------------------------------------------------------ texto: lorem idêntico ao do site
_LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam "
    "quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo "
    "consequat duis aute irure in reprehenderit voluptate velit esse cillum "
    "eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident "
    "sunt culpa qui officia deserunt mollit anim id est laborum curabitur "
    "vitae purus eget nunc porttitor sollicitudin nec eget metus vestibulum "
    "ante primis faucibus orci luctus posuere cubilia curae mauris blandit "
    "aliquet nibh praesent tristique senectus netus fames turpis egestas"
).split()


def lorem(seed, palavras=None):
    """Cópia de _lorem() de website/build/build_site.py -- mantida igual de propósito (mesma semente,
    mesmo texto), para o DOCX de curadoria continuar reconhecendo o que ainda é placeholder."""
    rng = random.Random(seed)
    if palavras is None:
        palavras = random.Random(f"{seed}-palavras").randint(100, 200)
    corpo = " ".join(rng.choice(_LOREM_WORDS) for _ in range(palavras))
    return corpo[:1].upper() + corpo[1:] + "."


EM_LOREM = []   # chaves ainda sem texto curado (relatório de build)


def texto(seed, palavras=None, lorem_seed=None):
    curado = TEXTOS.get(seed)
    if curado:
        return "\n\n".join(esc(p.strip()) for p in curado.split("\n") if p.strip())
    EM_LOREM.append(seed)
    return esc(lorem(lorem_seed or seed, palavras))


def esc(s):
    """Escapa o texto curado para LaTeX sem reescrevê-lo (constituição §5)."""
    s = str(s)
    trocas = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
              "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    s = "".join(trocas.get(c, c) for c in s)
    s = re.sub(r'"([^"]*)"', r"“\1”", s)          # aspas retas -> tipográficas
    s = s.replace("<", r"\textless{}").replace(">", r"\textgreater{}")
    return s


def slug_site(titulo):
    """Mesmo slugify do site (id do painel = semente de conclusao-<sid>)."""
    t = re.sub(r"[^\w\s-]", "", titulo, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s_]+", "-", t) or "sec"


def rotulo_label(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def titulo_eixo(bruto):
    """'🎯 Prioridade (sem secundário)' -> 'Prioridade' (mesmo h2 do site)."""
    t = re.sub(r"^[^\wÀ-ÿ]+", "", bruto).strip()
    return re.sub(r"\s*\(sem secundário\)$", "", t)


def lista(v):
    if not v:
        return []
    return [x.strip().strip("`").strip() for x in ([v] if isinstance(v, str) else v)]


# ------------------------------------------------------------------ figuras
def caminho_figura(nome, tipo):
    """Variante A4 (PDF vetorial, Bloco 5) se existir; senão a PNG atual reduzida para o cache."""
    pasta = "visualizacoes" if tipo == "grafico" else "mapas"
    stem = Path(nome).stem
    a4 = RAIZ / pasta / "a4" / f"{stem}.pdf"
    if a4.exists():
        return a4, True
    origem = RAIZ / pasta / nome
    CACHE.mkdir(parents=True, exist_ok=True)
    ext = ".jpg" if tipo == "mapa" else ".png"
    destino = CACHE / f"{stem}{ext}"
    if not destino.exists() or destino.stat().st_mtime < origem.stat().st_mtime:
        im = Image.open(origem)
        im.thumbnail((1900, 1900))                       # 16 cm a 300 dpi
        if ext == ".jpg":
            im.convert("RGB").save(destino, quality=88, optimize=True)
        else:
            im.save(destino, optimize=True)
    return destino, False


FALLBACK = []   # figuras ainda sem variante A4
ROTULO_POR_ASSINATURA = {}   # conteúdo impresso da tabela -> \label da primeira ocorrência


def legenda_fonte(info, tipo):
    chaves = [c for c in (info.get("chaves_bib") or "").split(", ") if c and c != "ipp_limites_bairros"]
    partes = [rf"\citeonline{{{c}}}" for c in chaves]
    base = "Elaboração IPP com dados de " + "; ".join(partes) + "." if partes else "Elaboração IPP."
    if tipo == "mapa":
        base += r" Limites de bairros: \citeonline{ipp_limites_bairros}. Sistema de referência SIRGAS 2000."
    return base


def legenda_titulo(info, titulo_secao, nome):
    t = (info.get("titulo") or "").strip()
    if not t or "…" in t or "\x00" in t:
        t = titulo_secao
    t = re.sub(r"\s*[-–]\s*Rio de Janeiro\b", "", t)       # o relatório inteiro é sobre o município
    return esc(t[:1].upper() + t[1:])


def bloco_figura(nome, tipo, info, titulo_secao):
    caminho, a4 = caminho_figura(nome, tipo)
    if not a4:
        FALLBACK.append(nome)
    rel = Path(caminho).resolve().relative_to(LATEX.resolve()) if LATEX.resolve() in Path(caminho).resolve().parents \
        else Path("../..") / Path(caminho).resolve().relative_to(RAIZ.resolve())
    rotulo = f"{'graf' if tipo == 'grafico' else 'mapa'}:{rotulo_label(Path(nome).stem)}"
    return (rf"\figura{{{tipo}}}{{{rel.as_posix()}}}{{{legenda_titulo(info, titulo_secao, nome)}}}"
            rf"{{{legenda_fonte(info, tipo)}}}{{{rotulo}}}")


# ------------------------------------------------------------------ montagem
def capitulos(estrutura, info_por_arquivo, so_eixo=None):
    tex = []
    tex.append(r"\chapter{Introdução}\label{cap:introducao}")
    intro = TEXTOS.get("introducao")
    tex.append(texto("introducao", 250, lorem_seed="introducao-relatorio") if intro else esc(lorem("introducao-relatorio", 250)))
    tex.append(r"\input{textual/como_ler}")
    tex.append(r"\section{Os eixos da política}")
    tex.append(r"\begin{itemize}")
    for i, eixo in enumerate(estrutura, 1):
        n_sub = len(eixo["subsecoes"])
        n_pend = sum(1 for s in eixo["subsecoes"] if (s["campos"].get("status") or "").strip() == "pendente")
        tex.append(rf"\item \textbf{{Eixo {i} --- {esc(titulo_eixo(eixo['eixo']))}}} (Capítulo~\ref{{cap:eixo-{i}}}): "
                   rf"{n_sub} indicadores" + (f", {n_pend} em desenvolvimento" if n_pend else "") + ".")
    tex.append(r"\end{itemize}")

    tabelas_por_eixo = []
    for i, eixo in enumerate(estrutura, 1):
        titulo = titulo_eixo(eixo["eixo"])
        sid = slug_site(titulo)
        icone = next((ic for pre, ic in EIXO_META if sid.startswith(pre)), "layout-dashboard")
        tabs_eixo = []
        tabelas_por_eixo.append((titulo, tabs_eixo))
        if so_eixo and i != so_eixo:
            continue
        tex.append(rf"\eixo{{{i}}}{{{len(estrutura)}}}{{{icone}}}")
        tex.append(rf"\chapter{{{esc(titulo)}}}\label{{cap:eixo-{i}}}")
        tex.append(r"\begin{achados}\begin{itemize}")
        for k in range(5):     # mesmo placeholder do site (_lorem_bullets)
            tex.append(r"\item " + esc(lorem(f"{sid}-kt-{k}", 8)))
        tex.append(r"\end{itemize}\end{achados}")
        for sub in eixo["subsecoes"]:
            c = sub["campos"]
            tex.append(rf"\section{{{esc(sub['titulo'])}}}")
            if (c.get("status") or "").strip() == "pendente":
                notas = lista(c.get("nota"))
                tex.append(r"\begin{pendente}" + esc(" ".join(notas) or "Indicador catalogado, ainda sem dado disponível.")
                           + r"\end{pendente}")
                continue
            for campo, tipo in (("visualização", "grafico"), ("mapa", "mapa")):
                for nome in lista(c.get(campo)):
                    info = info_por_arquivo.get(("visualizacoes" if tipo == "grafico" else "mapas") + "/" + nome, {})
                    tex.append(bloco_figura(nome, tipo, info, sub["titulo"]))
                    tex.append(texto(Path(nome).stem))
            refs = []
            for nome in lista(c.get("tabela")):
                if nome in tabelas.SUBSTITUI_NO_PDF:          # tabela repetida: remete à que a cobre, ou sai
                    nome = tabelas.SUBSTITUI_NO_PDF[nome]
                    if nome is None:
                        continue
                caminho = RAIZ / "tabelas_finais" / nome
                if not tabelas.cabe_no_pdf(caminho):
                    if nome not in [t for t, _ in tabs_eixo]:
                        tabs_eixo.append((nome, sub["titulo"]))
                    refs.append(r"\texttt{" + esc(nome) + "} (formato digital)")
                    continue
                # mesma tabela impressa (ex. série bairro×ano filtrada = tabela do mapa) sai uma vez só
                sig = tabelas.assinatura(caminho)
                if sig not in ROTULO_POR_ASSINATURA:
                    ROTULO_POR_ASSINATURA[sig] = f"tab:{rotulo_label(Path(nome).stem)}"
                    tabs_eixo.append((nome, sub["titulo"]))
                ref = rf"Tabela~\ref{{{ROTULO_POR_ASSINATURA[sig]}}}"
                if ref not in refs:
                    refs.append(ref)
            if refs:
                tex.append(r"\vertabelas{" + ", ".join(refs) + rf"; ver Apêndice~\ref{{ap:eixo-{i}}}}}")
        tex.append(r"\section{Síntese do eixo}")
        tex.append(rf"\begin{{sintese}}{{{esc(titulo)}}}" + texto(f"conclusao-{sid}") + r"\end{sintese}")

    tex.append(r"\chapter{Considerações finais}\label{cap:consideracoes}")
    tex.append(texto("consideracoes_finais", 300))
    return "\n\n".join(tex) + "\n", tabelas_por_eixo


def apendices(tabelas_por_eixo, info_por_arquivo):
    tex = [r"\begin{apendicesenv}", r"\partapendices"]
    for i, (titulo, tabs) in enumerate(tabelas_por_eixo, 1):
        tex.append(rf"\chapter{{Tabelas do eixo {esc(titulo)}}}\label{{ap:eixo-{i}}}")
        if not tabs:
            tex.append("Este eixo não tem tabelas de dados nesta edição.")
        digitais = []
        for nome, titulo_secao in tabs:
            caminho = RAIZ / "tabelas_finais" / nome
            if not tabelas.cabe_no_pdf(caminho):
                digitais.append((nome, titulo_secao, tabelas.n_linhas(caminho)))
                continue
            info = info_por_arquivo.get("tabelas_finais/" + nome, {})
            tex.append(tabelas.tabela_latex(caminho, titulo_secao,
                                            legenda_fonte(info, "tabela"), f"tab:{rotulo_label(Path(nome).stem)}"))
        if digitais:   # T4.4: tabelas longas demais para o papel ficam só no formato digital
            tex.append(r"\section*{Tabelas disponíveis em formato digital}")
            tex.append(rf"As tabelas abaixo têm mais de {tabelas.MAX_LINHAS_PDF} linhas e não são impressas; estão em "
                       r"\texttt{tabelas\_finais/} no repositório do projeto.")
            tex.append(r"\begin{itemize}" + "".join(
                rf"\item \texttt{{{esc(n)}}} --- {esc(s)} ({tabelas.num(l, 0)} linhas)" for n, s, l in digitais)
                + r"\end{itemize}")
    tex.append(r"\end{apendicesenv}")
    return "\n\n".join(tex) + "\n"


def resumo():
    return (r"\setlength{\absparsep}{18pt}" "\n" r"\begin{resumo}" "\n" + texto("resumo", 250) + "\n\n"
            r"\noindent\textbf{Palavras-chave}: " + PALAVRAS_CHAVE + "\n" r"\end{resumo}" "\n")


def compila(publicar=False):
    cmd = ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
           "-outdir=_build", "relatorio.tex"]
    import os
    env = dict(os.environ, BIBINPUTS=str(LATEX) + os.pathsep, TEXINPUTS=str(LATEX) + os.pathsep)
    r = subprocess.run(cmd, cwd=LATEX, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    log = (LATEX / "_build/relatorio.log")
    if r.returncode != 0:
        erros = [l for l in log.read_text(encoding="utf-8", errors="replace").splitlines() if l.startswith(("!", "./", "gerado"))]
        print("\n".join(erros[:30]) or r.stdout[-3000:])
        sys.exit("latexmk falhou -- ver relatorio/latex/_build/relatorio.log")
    texto_log = log.read_text(encoding="utf-8", errors="replace")
    indef = len(re.findall(r"undefined", texto_log, re.I))
    overfull = re.findall(r"Overfull \\hbox \((\d+\.\d+)pt", texto_log)
    grandes = [o for o in overfull if float(o) > 5]
    destino = "relatorio/latex/_build/relatorio.pdf"
    if publicar:   # só o documento inteiro substitui o PDF publicado (o site aponta para ele)
        shutil.copy(LATEX / "_build/relatorio.pdf", RAIZ / "relatorio/analise_primeira_infancia.pdf")
        destino = "relatorio/analise_primeira_infancia.pdf"
    print(f"PDF: {destino}  |  avisos 'undefined': {indef}  |  "
          f"overfull > 5pt: {len(grandes)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sem-pdf", action="store_true")
    ap.add_argument("--eixo", type=int)
    ap.add_argument("--publicar", action="store_true",
                    help="copia o PDF para relatorio/analise_primeira_infancia.pdf (só com o documento inteiro)")
    args = ap.parse_args()

    estrutura = parse_estrutura_eixos(str(RAIZ / "specs/estrutura_eixos.md"))
    valida_estrutura(estrutura, base_dir=str(RAIZ))
    linhas, _, _ = inventario_fontes.coleta()
    info = {l["arquivo"]: l for l in linhas}

    GERADO.mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(AQUI / "gera_icones.py")], check=True, cwd=RAIZ, capture_output=True)
    corpo, tabs = capitulos(estrutura, info, args.eixo)
    (GERADO / "capitulos.tex").write_text("% Gerado por gera_latex.py -- não editar à mão.\n" + corpo, encoding="utf-8")
    (GERADO / "apendices.tex").write_text("% Gerado por gera_latex.py -- não editar à mão.\n"
                                           + apendices(tabs if not args.eixo else [t if k == args.eixo - 1 else (t[0], [])
                                                                                    for k, t in enumerate(tabs)], info),
                                           encoding="utf-8")
    chaves = re.findall(r"^@\w+\{(\w+),", (LATEX / "fontes.bib").read_text(encoding="utf-8"), re.M)
    (GERADO / "nocite.tex").write_text("% Gerado por gera_latex.py.\n\\nocite{" + ",".join(chaves) + "}\n",
                                       encoding="utf-8")
    (GERADO / "resumo.tex").write_text("% Gerado por gera_latex.py -- não editar à mão.\n" + resumo(), encoding="utf-8")
    print(f"{len(estrutura)} eixos; {len(FALLBACK)} figuras ainda sem variante A4 (usando a PNG de tela); "
          f"{len(EM_LOREM)} textos em lorem: {', '.join(EM_LOREM[:8])}{' …' if len(EM_LOREM) > 8 else ''}")
    usados = {Path(n).stem for e in estrutura for s in e["subsecoes"] for f in ("visualização", "mapa")
              for n in lista(s["campos"].get(f))}
    sem_figura = sorted(k for k in TEXTOS if k not in usados and k != "introducao" and not k.startswith(("conclusao-", "resumo", "consideracoes")))
    if sem_figura:
        print(f"Textos curados sem figura no relatório ({len(sem_figura)}): {', '.join(sem_figura)}")
    if not args.sem_pdf:
        compila(publicar=args.publicar and not args.eixo)


if __name__ == "__main__":
    main()
