# -*- coding: utf-8 -*-
"""Mostra o que um DOCX de update (Google Docs) mudou DE VERDADE em relação ao update anterior em que ele foi
baseado, e como cada texto mudado está hoje em `relatorio/textos_curados.json`.

Por que existe (update 5, 2026-09-28): o curador baixa o update anterior, edita e devolve. O casamento de
`incorpora_update_docx.py` sobre o arquivo inteiro reapresenta tudo o que já foi decidido em rodadas anteriores
(regressões de textos corrigidos depois, parágrafos duplicados pelo Google Docs, texto de mapa de contagem colado
no bookmark do mapa de taxa vizinho porque a figura de contagem saiu do relatório). Comparar com o update-base
isola só o que o curador escreveu nesta rodada.

Uso:
    python compara_updates.py <update_base.docx> <update_novo.docx>

Para cada figura (H3) cujo texto mudou entre os dois arquivos imprime o status em relação ao JSON:
  IGUAL_AO_JSON      -- já incorporado (nada a fazer);
  NOVO               -- chave sem texto curado ainda;
  DIFERENTE_DO_JSON  -- texto novo diferente do curado (decidir: rodada nova ou regressão?).
Títulos que mudaram só de acento (o curador corrigindo o nome do arquivo no H3) são listados à parte: o H3 do
DOCX é o nome do arquivo e não aparece no site nem no PDF.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from incorpora_update_docx import blocos, eh_lorem  # noqa: E402

JSON = "relatorio/textos_curados.json"


def n(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", t)).strip()


def ws(t):
    return " ".join((t or "").split())


def textos_por_h3(caminho):
    out = {}
    for b in blocos(caminho):
        if not b["h3"] or eh_lorem(b["texto"]) or b["texto"].startswith(("Tabela de apoio", "📝")):
            continue
        out.setdefault(n(b["h3"]), []).append(b["texto"].strip())
    return {k: "\n".join(v) for k, v in out.items()}


def main(base, novo):
    cur = json.loads(Path(JSON).read_text(encoding="utf-8"))
    por_stem = {n(k.replace("_", " ")): k for k in cur}
    t_base, t_novo = textos_por_h3(base), textos_por_h3(novo)
    mudados = 0
    for h3, texto in t_novo.items():
        if ws(t_base.get(h3)) == ws(texto):
            continue
        mudados += 1
        chave = por_stem.get(h3)
        if chave and ws(cur[chave]) == ws(texto):
            print(f"IGUAL_AO_JSON      | {h3} | {chave}")
            continue
        print(f"{'NOVO' if not chave else 'DIFERENTE_DO_JSON':18s} | {h3} | {chave}\n    novo: {ws(texto)}")
        if chave:
            print(f"    json: {ws(cur[chave])}")
    print(f"\n{mudados} figura(s) com texto mudado em relação a {Path(base).name}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
