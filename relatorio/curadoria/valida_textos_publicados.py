# -*- coding: utf-8 -*-
"""Confere se cada texto de `relatorio/textos_curados.json` está publicado no site (`website/index.html`) e no PDF,
frase a frase. Rodar depois de `sincroniza_docx.py` / `gera_latex.py --publicar` (update 5, 2026-09-28).

Uso:
    python valida_textos_publicados.py [<pdf>]        (padrão: relatorio/analise_primeira_infancia.pdf)

A comparação ignora espaços, hífens e aspas tipográficas e procura as palavras de cada frase EM ORDEM, tolerando
o que o PDF intercala num parágrafo partido entre páginas (marca d'água, cabeçalho, uma figura inteira com os
rótulos dos eixos) e até 2 palavras partidas na quebra de página ("magni-" | cabeçalho | "tude"). Uma frase que
ainda falhe deve ser conferida à mão (abrir a página) antes de ser tratada como ausente.

Ausências esperadas (não são erro, saem marcadas como "esperado"):
- textos de figuras fora do relatório (órfãos: `gera_latex.py` lista em "Textos curados sem figura no relatório");
- `resumo` e `consideracoes_finais` no site (só PDF, specs/2026-09-25_website_graficos §3b);
- `obitos_evitaveis_total_cap_ano` no site (figura nunca publicada no site; specs/2026-09-28_website_bugfix).
Saída != 0 se algum texto que deveria estar publicado faltar.
"""
import html
import json
import re
import sys
import unicodedata
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
import pymupdf  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gera_estrutura_eixos import blocos_relatorio, parse_estrutura_eixos  # noqa: E402

JSON = "relatorio/textos_curados.json"
SITE = "website/index.html"
SO_PDF = {"resumo", "consideracoes_finais", "obitos_evitaveis_total_cap_ano"}


def n(t):
    t = unicodedata.normalize("NFKC", t or "")
    for a, b in [("­", ""), ("“", '"'), ("”", '"'), ("’", "'"), ("–", "-"), ("—", "-")]:
        t = t.replace(a, b)
    return re.sub(r"[\s\-]+", "", t).lower()


def frase_presente(frase, alvo, janela=8000):
    ws = [n(w) for w in frase.split() if n(w)]
    if not ws:
        return True
    inicio, resto = "".join(ws[:3]), ws[3:]
    pos = alvo.find(inicio)
    while pos >= 0:
        p, falhas = pos + len(inicio), 0
        for w in resto:
            q = alvo.find(w, p)
            if q < 0 or q - p > (janela if len(w) > 3 else 60):
                falhas += 1
                if falhas > 2:
                    break
                continue
            p = q + len(w)
        if falhas <= 2:
            return True
        pos = alvo.find(inicio, pos + 1)
    # início da frase partido pela quebra de página ("A distribuição" | figura | "por idade..."): confere o resto
    return len(ws) > 8 and frase_presente(" ".join(frase.split()[3:]), alvo, janela)


def cobertura(texto, alvo):
    frases = [f for f in re.split(r"(?<=[.!?])\s+", texto) if len(f.strip()) > 25]
    return sum(frase_presente(f, alvo) for f in frases), len(frases)


def chaves_no_relatorio():
    estrutura = parse_estrutura_eixos()
    chaves = {"introducao"} | set(blocos_relatorio(estrutura))
    for eixo in estrutura:
        for sub in eixo["subsecoes"]:
            if sub["campos"].get("status") == "pendente":
                continue
            for campo in ("visualização", "mapa"):
                v = sub["campos"].get(campo)
                for x in (v if isinstance(v, list) else [v] if v else []):
                    chaves.add(Path(re.sub(r"[`\s]", "", x)).stem)
    return chaves


def main(pdf):
    cur = json.loads(Path(JSON).read_text(encoding="utf-8"))
    site = n(html.unescape(re.sub(r"<[^>]+>", " ", Path(SITE).read_text(encoding="utf-8"))))
    txt_pdf = n(" ".join(p.get_text() for p in pymupdf.open(pdf)))
    no_rel = chaves_no_relatorio()
    erros = 0
    for k in sorted(cur):
        if not cur[k].strip():
            continue
        s, p = cobertura(cur[k], site), cobertura(cur[k], txt_pdf)
        publicado = k in no_rel or k.startswith(("conclusao-",))
        falta_site = publicado and k not in SO_PDF and s[0] < s[1]
        falta_pdf = publicado and p[0] < p[1]
        if not publicado:
            obs = "esperado: figura fora do relatório (órfão)"
        elif falta_site or falta_pdf:
            obs = "FALTA -- conferir à mão"
            erros += 1
        else:
            obs = "ok" + (" (site: só PDF, esperado)" if k in SO_PDF and s[0] < s[1] else "")
        print(f"{k:66s} site {s[0]:>2}/{s[1]:<2} pdf {p[0]:>2}/{p[1]:<2} {obs}")
    print(f"\n{erros} texto(s) com frase ausente no site ou no PDF")
    return erros


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else "relatorio/analise_primeira_infancia.pdf") else 0)
