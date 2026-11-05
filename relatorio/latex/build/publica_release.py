# -*- coding: utf-8 -*-
"""Publica o relatório em PDF como anexo de uma Release do GitHub (specs/2026-11-05_versao_final_site R7).

O site baixa o PDF de `releases/latest/download/analise_primeira_infancia.pdf`, então um PDF novo só chega aos
leitores depois de uma Release nova com o arquivo anexado sob esse mesmo nome. O PDF não é versionado no git.

    python relatorio/latex/build/publica_release.py v1.0.0                 # ensaio: confere e mostra o que faria
    python relatorio/latex/build/publica_release.py v1.0.0 --gerar         # + gera o PDF (gera_latex.py --publicar)
    python relatorio/latex/build/publica_release.py v1.0.0 --confirmar     # cria a tag e a Release (precisa do OK do usuário)

Pré-requisitos: `gh` instalado e autenticado (`gh auth login`). Antes de publicar, confere: árvore limpa (fora
`website_release.md` e outros não versionados), branch `main`, tag nova, PDF existente e mais novo que os capítulos,
`relatorio/publicacao.json` com `pdf_em_desenvolvimento: false` (só aviso -- uma Release de teste pode sair com a marca).
A tag `vX.Y.Z` é criada pelo próprio `gh release create` no commit atual da `main` (`--target main`).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PDF = RAIZ / "relatorio" / "analise_primeira_infancia.pdf"
CAPITULOS = RAIZ / "relatorio" / "latex"
PUBLICACAO = RAIZ / "relatorio" / "publicacao.json"
BRANCH = "main"


def gh():
    for c in (shutil.which("gh"), r"C:\Program Files\GitHub CLI\gh.exe"):
        if c and Path(c).exists():
            return c
    sys.exit("gh não encontrado: instale (winget install GitHub.cli) e rode `gh auth login`")


def git(*args):
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1 or not args[0].startswith("v"):
        sys.exit(__doc__)
    tag = args[0]
    confirmar, gerar = "--confirmar" in sys.argv, "--gerar" in sys.argv
    erros, avisos = [], []

    exe = gh()
    if subprocess.run([exe, "auth", "status"], capture_output=True).returncode != 0:
        erros.append("gh não autenticado: rode `gh auth login`")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != BRANCH:
        erros.append(f"branch atual é {branch}; a Release sai da {BRANCH}")
    sujos = [l for l in git("status", "--porcelain", "--untracked-files=no").splitlines() if l.strip()]
    if sujos:
        erros.append(f"árvore com alterações não commitadas ({len(sujos)} arquivos)")
    if git("tag", "-l", tag):
        erros.append(f"a tag {tag} já existe")
    if git("rev-parse", "HEAD") != git("rev-parse", f"origin/{BRANCH}"):
        avisos.append(f"HEAD diferente de origin/{BRANCH}: faça o push antes (a tag vai no commit remoto da {BRANCH})")

    if gerar:
        print("gerando o PDF (gera_latex.py --publicar) ...")
        r = subprocess.run([sys.executable, str(RAIZ / "relatorio/latex/build/gera_latex.py"), "--publicar"], cwd=RAIZ)
        if r.returncode != 0:
            sys.exit("gera_latex.py falhou")
    if not PDF.exists():
        erros.append(f"falta {PDF.relative_to(RAIZ)} (rode com --gerar ou gera_latex.py --publicar)")
    else:
        fontes = [p for p in CAPITULOS.rglob("*.tex") if "_build" not in p.parts] + [p for p in CAPITULOS.glob("*.sty")]
        mais_novo = max(fontes, key=lambda p: p.stat().st_mtime)
        if mais_novo.stat().st_mtime > PDF.stat().st_mtime:
            avisos.append(f"o PDF é mais antigo que {mais_novo.relative_to(RAIZ)}: regere com --gerar")
    pub = json.loads(PUBLICACAO.read_text(encoding="utf-8"))
    if pub.get("pdf_em_desenvolvimento"):
        avisos.append("publicacao.json: pdf_em_desenvolvimento = true (o PDF sai com a marca EM DESENVOLVIMENTO)")
    if not pub.get("link_pdf_no_site"):
        avisos.append("publicacao.json: link_pdf_no_site = false -- depois da Release, ligue e regere o site para o botão voltar")

    titulo = f"Relatório {tag}"
    notas = (f"Relatório técnico em PDF da análise de indicadores da primeira infância no Rio de Janeiro ({tag}).\n\n"
             f"O site (https://ipp-dados.github.io/analise_primeira_infancia/) baixa sempre o PDF da última Release.")
    cmd = [exe, "release", "create", tag, str(PDF), "--target", BRANCH, "--title", titulo, "--notes", notas, "--latest"]
    for a in avisos:
        print("AVISO:", a)
    for e in erros:
        print("ERRO:", e)
    if PDF.exists():
        print(f"PDF: {PDF.relative_to(RAIZ)} ({PDF.stat().st_size / 1e6:.1f} MB)")
    print("comando:", " ".join(f'"{c}"' if " " in c else c for c in cmd))
    if erros:
        sys.exit(1)
    if not confirmar:
        print("ensaio: nada publicado (rode de novo com --confirmar, só com o OK do usuário)")
        return
    subprocess.run(cmd, cwd=RAIZ, check=True)
    print("Release publicada. Confira o link do site: releases/latest/download/analise_primeira_infancia.pdf")


if __name__ == "__main__":
    main()
