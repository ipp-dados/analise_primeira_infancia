# -*- coding: utf-8 -*-
"""Importa os textos de eixo escritos à mão em `relatorio/textos_eixos.md` para `relatorio/textos_curados.json`.

Cada eixo (`## <emoji> <nome>`) tem três subseções: "Principais achados" -> `achados_<eixo>` (uma frase por linha, sem o
"- "), "Introdução do eixo" -> `introducao_<eixo>` e "Síntese do eixo" -> `sintese_<eixo>` (parágrafos separados por
quebra de linha, como os outros textos curados). Subseção vazia (ou só com o marcador `<!-- texto: ... -->`) não é
importada: o site e o PDF seguem com o lorem. Merge no JSON (nunca apaga chave), e o status vai para
`ajustes_manuais` de `relatorio/controle_revisao.json`. specs/2026-11-05_versao_final_site T1.3.

Uso:  python relatorio/curadoria/importa_textos_eixos.py [--dry-run]
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
MD = RAIZ / "relatorio" / "textos_eixos.md"
JSON_TEXTOS = RAIZ / "relatorio" / "textos_curados.json"
CONTROLE = RAIZ / "relatorio" / "controle_revisao.json"

# mesmo sufixo de chave que chave_eixo() (site e PDF) produz para cada eixo
EIXOS = {"Prioridade": "prioridade", "Inclusão": "inclusao", "Família e Cuidados": "familia_e_cuidados",
         "Proteção": "protecao", "Direito ao Brincar": "direito_ao_brincar", "Alimentação": "alimentacao",
         "Moradia": "moradia"}
SUBSECOES = {"Principais achados": "achados", "Introdução do eixo": "introducao", "Síntese do eixo": "sintese"}


def le_textos(caminho=MD):
    """{chave: texto} das subseções preenchidas."""
    textos, eixo, sub, corpo = {}, None, None, []

    def fecha():
        if eixo and sub:
            linhas = [l.rstrip() for l in corpo if not l.strip().startswith("<!--")]
            if sub == "achados":
                frases = [re.sub(r"^\s*[-•–]\s*", "", l).strip() for l in linhas if l.strip()]
                texto = "\n".join(frases)
            else:
                paragrafos = re.split(r"\n\s*\n", "\n".join(linhas).strip())
                texto = "\n".join(" ".join(p.split()) for p in paragrafos if p.strip())
            if texto:
                textos[f"{sub}_{eixo}"] = texto

    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            fecha()
            nome = re.sub(r"^##\s+\S+\s+", "", linha).strip()
            eixo, sub, corpo = EIXOS.get(nome), None, []
        elif linha.startswith("### "):
            fecha()
            sub, corpo = SUBSECOES.get(linha[4:].strip()), []
        elif linha.strip() == "---":
            fecha()
            sub, corpo = None, []
        elif sub:
            corpo.append(linha)
    fecha()
    return textos


def main():
    textos = le_textos()
    print(f"{len(textos)} textos preenchidos: {', '.join(sorted(textos))}")
    if "--dry-run" in sys.argv:
        return
    atual = json.loads(JSON_TEXTOS.read_text(encoding="utf-8"))
    mudou = {k: v for k, v in textos.items() if atual.get(k) != v}
    atual.update(textos)
    # mesmo formato que o JSON sempre teve (chaves ordenadas, sem quebra no fim)
    JSON_TEXTOS.write_text(json.dumps(atual, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    c = json.loads(CONTROLE.read_text(encoding="utf-8"))
    for k in mudou:
        c["ajustes_manuais"][k] = {
            "status": "atualizado", "rodada": "textos_eixos", "historico": [f"textos_eixos_{date.today().isoformat()}"],
            "obs": "texto de eixo escrito pela coordenação em relatorio/textos_eixos.md (importa_textos_eixos.py)"}
    CONTROLE.write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"gravados no JSON; {len(mudou)} novos ou alterados")


if __name__ == "__main__":
    main()
