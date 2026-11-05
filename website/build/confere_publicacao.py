# -*- coding: utf-8 -*-
"""Confere o site já gerado antes de publicar (specs/2026-11-05_versao_final_site R8). Só lê arquivos; não gera nada.

Roda no GitHub Actions (deploy na `main` e checagem em `staging_main`) e localmente. Só biblioteca padrão.

    python website/build/confere_publicacao.py [pasta]

`pasta` é o site como vai ao ar (padrão: monta a lista de inclusão a partir de `website/`, a mesma do deploy).
Falha (saída 1) se:
  - aparece arquivo de tipo fora da lista permitida (site estático: html/css/js/svg/png/jpg/ico/woff2);
  - passa do orçamento (index.html > 1 MB ou site > 2 MB; website/README.md);
  - sobrou texto provisório (lorem ipsum) em index.html;
  - há dado pontual (`data-dado-pontual`) sem a faixa EM DESENVOLVIMENTO (constituição §3);
  - algum JS usa `fetch(` (o site abre por file:// e não faz requisições).
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SITE = RAIZ / "website"
# a mesma lista de inclusão de .github/workflows/deploy-relatorio.yml
INCLUI = ["index.html", "404.html", ".nojekyll", "favicon.ico", "css", "js", "data", "assets"]
PERMITIDOS = {".html", ".css", ".js", ".svg", ".png", ".jpg", ".ico", ".woff2"}
LIMITE_INDEX = 1_000_000
LIMITE_SITE = 2_000_000
# palavras do lorem do gerador que não existem em português (build_site._LOREM_WORDS)
LOREM = re.compile(r"\b(consectetur|adipiscing|eiusmod|incididunt|exercitation|ullamco)\b", re.I)


def arquivos(pasta=None):
    if pasta:
        base = Path(pasta)
        return base, [p for p in base.rglob("*") if p.is_file()]
    lista = []
    for nome in INCLUI:
        p = SITE / nome
        lista += [x for x in p.rglob("*") if x.is_file()] if p.is_dir() else [p]
    return SITE, lista


def main():
    base, lista = arquivos(sys.argv[1] if len(sys.argv) > 1 else None)
    erros = []
    faltam = [p for p in lista if not p.exists()]
    erros += [f"falta {p.relative_to(base)}" for p in faltam]
    lista = [p for p in lista if p.exists()]

    fora = [p for p in lista if p.name != ".nojekyll" and p.suffix.lower() not in PERMITIDOS]
    erros += [f"tipo de arquivo não permitido: {p.relative_to(base)}" for p in fora]

    index = base / "index.html"
    total = sum(p.stat().st_size for p in lista)
    if index.exists() and index.stat().st_size > LIMITE_INDEX:
        erros.append(f"index.html com {index.stat().st_size:,} bytes (limite {LIMITE_INDEX:,})")
    if total > LIMITE_SITE:
        erros.append(f"site com {total:,} bytes (limite {LIMITE_SITE:,})")

    html = index.read_text(encoding="utf-8") if index.exists() else ""
    achados = sorted(set(m.lower() for m in LOREM.findall(html)))
    if achados:
        erros.append(f"texto provisório (lorem) em index.html: {', '.join(achados)}")
    dev = 'class="dev-banner"' in html
    if "data-dado-pontual" in html and not dev:
        erros.append("dado pontual na versão final (sem a faixa EM DESENVOLVIMENTO) -- constituição §3")

    for js in (p for p in lista if p.suffix == ".js"):
        if "fetch(" in js.read_text(encoding="utf-8", errors="replace"):
            erros.append(f"{js.relative_to(base)} usa fetch( -- o site não faz requisições")

    print(f"{len(lista)} arquivos, {total:,} bytes; index.html {index.stat().st_size if index.exists() else 0:,} bytes; "
          f"faixa EM DESENVOLVIMENTO: {'sim' if dev else 'não'}")
    if erros:
        print("ERROS:")
        for e in erros:
            print("  -", e)
        sys.exit(1)
    print("Conteúdo OK")


if __name__ == "__main__":
    main()
