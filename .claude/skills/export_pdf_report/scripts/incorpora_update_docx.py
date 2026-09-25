# -*- coding: utf-8 -*-
"""Casa os textos de um DOCX de curadoria "de update" (editado fora, tipicamente no Google Docs)
com os bookmarks da estrutura ATUAL de `relatorio/curadoria_textos.docx`.

Por que existe: o round-trip pelo Google Docs apaga os bookmarks OOXML que `sincroniza_docx.py`
usa (ver commit cbae4cd, update 1). E o arquivo de update costuma ter sido baixado de uma versão
anterior da estrutura (títulos de imagem com nomes de arquivo antigos, subseções que mudaram de
conteúdo). Então o casamento é por contexto, nesta ordem:

  1. título do H3 (nome do arquivo da imagem), normalizado (sem acento/pontuação/marcas de status)
     e traduzido pelos renomes conhecidos (`RENOMES`, specs/2026-09-24_populacao-referencia/auditoria_faixas.md B1-B5);
  2. imagem sem título (H3 vazio, comum depois de edição à mão): a posição da imagem dentro do H2;
  3. texto direto sob o H2 (subseção sem imagem): o bookmark `{eixo}::{subseção}` do mesmo H2.

Tudo o que não casa sai num relatório (`nao_casados`) — nunca é descartado em silêncio.

Uso:
    python incorpora_update_docx.py <docx_update> [<docx_update> ...] --saida <json> [--controle relatorio/controle_revisao.json] [--datas AAAA-MM-DD,...]
(updates na ordem cronológica; --controle grava o status por bloco: ver atualiza_controle)
Grava {"textos": {bookmark: {"texto", "origem", "h2", "h3"}}, "nao_casados": [...], "notas": [...]}.
Com vários updates, o último da lista vence quando dois trazem texto para o mesmo bookmark.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gera_docx_curadoria import _LOREM_WORDS, _bookmark_name, extrai_textos_por_bookmark  # noqa: E402

DOCX_ATUAL = "relatorio/curadoria_textos.docx"

# nome antigo (normalizado) -> nome atual (normalizado) -- auditoria_faixas.md, Lista B
RENOMES = [
    (r"\bmapa cadunico primeira infancia bairro 2026\b", "mapa cadunico criancas 0 a 4 bairro 2026"),
    (r"\bmapa percentual cadunico primeira infancia bairro 2026\b", "mapa percentual cadunico 0 a 4 sobre censo bairro 2026"),
    (r"\b(grupo|subgrupo) 0 6 ano\b", r"\1 0 a 6 dias ano"),
    (r"\b(grupo|subgrupo) 7 27 ano\b", r"\1 7 a 27 dias ano"),
    (r"\b(grupo|subgrupo) 28 364 ano\b", r"\1 28 a 364 dias ano"),
]

_LOREM = set(w.lower().strip(".,") for w in _LOREM_WORDS)


def norm(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    for padrao, novo in RENOMES:
        t = re.sub(padrao, novo, t)
    return t


def eh_lorem(texto):
    ws = [w.lower().strip(".,;:") for w in texto.split() if w.strip(".,;:")]
    return bool(ws) and sum(w in _LOREM for w in ws) / len(ws) > 0.85


def _estilo_nivel(p_el):
    st = p_el.find(qn("w:pPr") + "/" + qn("w:pStyle"))
    val = st.get(qn("w:val")) if st is not None else ""
    m = re.match(r"(?:Heading|Ttulo|Titulo|Título)(\d)", val or "")
    return int(m.group(1)) if m else None


def blocos(caminho):
    """Percorre o corpo do DOCX e devolve blocos de texto com contexto (H1, H2, H3, nº da imagem no H2)."""
    doc = Document(caminho)
    h1 = h2 = h3 = ""
    img = -1
    img_do_h3 = None   # nº da 1ª imagem sob o H3 atual; outra imagem sob o mesmo H3 = imagem sem título
    out = []
    for el in doc.element.body.iterchildren():
        if el.tag != qn("w:p"):
            continue
        texto = "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()
        nivel = _estilo_nivel(el)
        if nivel == 1:
            h1, h2, h3, img, img_do_h3 = texto, "", "", -1, None
            continue
        if nivel == 2:
            h2, h3, img, img_do_h3 = texto, "", -1, None
            continue
        if nivel == 3:
            if texto:          # H3 vazio (sobra de edição) não troca o título corrente
                h3, img_do_h3 = texto, None
            continue
        if el.findall(".//" + qn("w:drawing")) or el.findall(".//" + qn("w:pict")):
            img += 1
            if img_do_h3 is None:
                img_do_h3 = img
        if not texto or texto in ("SUMÁRIO",) or texto.startswith(("Tabela de apoio:", "[PENDENTE]", "Clique com o botão direito")):
            continue
        bms = [b.get(qn("w:name")) for b in el.iter(qn("w:bookmarkStart"))]
        out.append(dict(h1=h1, h2=h2, h3=h3, img=img, texto=texto,
                        img_sem_titulo=(img_do_h3 is not None and img != img_do_h3),
                        lorem=eh_lorem(texto), bookmarks=[b for b in bms if b and not b.startswith("_")]))
    return out


def indice_atual(caminho=DOCX_ATUAL):
    """Da estrutura atual: por (h2, h3) e por (h2, nº da imagem) -> bookmark; por h2 -> bookmark da seção."""
    por_h3, por_img, por_h2 = {}, {}, {}
    for b in blocos(caminho):
        if not b["bookmarks"] or norm(b["h1"]) == "textos orfaos":   # apêndice não é estrutura
            continue
        bm = b["bookmarks"][0]
        chave_h2 = norm(b["h2"] or b["h1"])
        if b["img"] >= 0 and b["h3"]:
            por_h3.setdefault((chave_h2, norm(b["h3"])), bm)
            por_h3.setdefault(("*", norm(b["h3"])), bm)   # H3 é único no documento, salvo raras repetições
            por_img[(chave_h2, b["img"])] = bm
        else:
            por_h2[chave_h2] = bm
    return por_h3, por_img, por_h2


def _indice_secoes():
    from gera_estrutura_eixos import parse_estrutura_eixos
    out = {}
    for eixo in parse_estrutura_eixos():
        for sub in eixo["subsecoes"]:
            out[norm(sub["titulo"])] = _bookmark_name(f"{eixo['eixo']}::{sub['titulo']}")
    return out


_SECOES = {}


def casa(caminho_update, indices):
    por_h3, por_img, por_h2 = indices
    textos, nao_casados, notas, realocar = {}, [], [], []
    ultimo_bm_por_img = {}
    vistos = set()   # bookmarks da estrutura atual que existiam neste update (com texto ou lorem)
    for b in blocos(caminho_update):
        chave_h2 = norm(b["h2"] or b["h1"])
        if b["lorem"]:
            k = (por_img.get((chave_h2, b["img"])) if b["img_sem_titulo"] else
                 (por_h3.get((chave_h2, norm(b["h3"]))) or por_h3.get(("*", norm(b["h3"])))) if b["h3"] else por_h2.get(chave_h2))
            if k:
                vistos.add(k)
            continue
        if b["h1"] == "Introdução" and not b["h2"]:
            bm = "introducao"
        elif b["img_sem_titulo"]:
            # imagem sem H3 próprio: vale a posição da imagem dentro do H2
            bm = por_img.get((chave_h2, b["img"]))
        elif b["img"] >= 0 or b["h3"]:
            # H3 com título (com ou sem a imagem -- às vezes a imagem se perde na edição)
            bm = (por_h3.get((chave_h2, norm(b["h3"]))) or por_h3.get(("*", norm(b["h3"])))
                  or (por_img.get((chave_h2, b["img"])) if b["img"] >= 0 else None))
            # vários parágrafos seguidos sob a mesma imagem: mesmo bookmark (juntados abaixo)
        else:
            bm = por_h2.get(chave_h2)
            if not bm and chave_h2 in _SECOES:
                # texto direto sob um H2 que hoje tem imagens: vira "texto da seção" (bookmark da seção),
                # exibido no DOCX com aviso para realocar/conferir -- não some no apêndice de órfãos
                bm = _SECOES[chave_h2]
                realocar.append(dict(bookmark=bm, h2=b["h2"], texto=b["texto"], origem=Path(caminho_update).name))
        # nota editorial (ex. "OPÇÃO DE TEXTO ...:" sem texto depois) -- não é texto de análise
        if b["texto"].rstrip().endswith(":") and len(b["texto"]) < 120 and b["texto"].upper() == b["texto"]:
            notas.append(dict(bookmark=bm, h2=b["h2"], h3=b["h3"], texto=b["texto"], origem=Path(caminho_update).name))
            continue
        if bm:
            vistos.add(bm)
        if not bm:
            nao_casados.append(dict(h1=b["h1"], h2=b["h2"], h3=b["h3"], img=b["img"], texto=b["texto"],
                                    origem=Path(caminho_update).name))
            continue
        if bm in textos and textos[bm]["origem"] == Path(caminho_update).name:
            textos[bm]["texto"] += "\n" + b["texto"]     # parágrafos do mesmo bloco
        else:
            textos[bm] = dict(texto=b["texto"], origem=Path(caminho_update).name, h2=b["h2"], h3=b["h3"])
    return textos, nao_casados, notas, realocar, vistos


def _n(t):
    return " ".join((t or "").split())


def atualiza_controle(caminho, rodadas, por_rodada, vistos_ultima, notas, realocar, bookmarks_atuais):
    """Status por bloco a partir da sequência de rodadas (a mais antiga primeiro):
    - "revisado": o texto aparece em 2+ rodadas e a última não o mudou (confirmado numa nova revisão);
    - "atualizado": texto novo ou alterado na última rodada em que aparece.
    Blocos sem texto curado não entram em `blocos` (o gerador do DOCX os mostra como pendentes).
    `alertas` é editado à mão e preservado entre execuções."""
    anterior = json.loads(Path(caminho).read_text(encoding="utf-8")) if Path(caminho).exists() else {}
    blocos_ = {}
    ids = [r["id"] for r in rodadas]
    todos_bms = set().union(*[set(t) for t in por_rodada.values()]) if por_rodada else set()
    for bm in sorted(todos_bms):
        hist = [rid for rid in ids if bm in por_rodada[rid]]
        textos_ = [_n(por_rodada[rid][bm]["texto"]) for rid in hist]
        mudou_em = hist[0]
        for k in range(1, len(hist)):
            if textos_[k] != textos_[k - 1]:
                mudou_em = hist[k]
        status = "revisado" if (len(hist) >= 2 and mudou_em != hist[-1]) else "atualizado"
        blocos_[bm] = dict(status=status, rodada=mudou_em, historico=hist)
    novos = sorted(bm for bm in bookmarks_atuais if bm not in vistos_ultima and bm != "introducao")
    # sugestões escritas à mão em "realocar" sobrevivem a uma nova execução
    sugestoes = {r["bookmark"]: r["sugestao"] for r in anterior.get("realocar", []) if r.get("sugestao")}
    for r in realocar:
        if r["bookmark"] in sugestoes:
            r["sugestao"] = sugestoes[r["bookmark"]]
    controle = dict(
        _leia=("Controle de revisão dos textos de curadoria (gerado por incorpora_update_docx.py; "
               "'alertas', 'alertas_resolvidos' e 'ajustes_manuais' são editados à mão e preservados). O gerador do DOCX usa este arquivo para marcar "
               "status nos títulos (e portanto no Sumário) e montar a tabela 'Controle de revisão'."),
        rodadas=rodadas, blocos=blocos_, novos_desde_ultima_rodada=novos,
        notas=notas, realocar=realocar, alertas=anterior.get("alertas", {}),
        alertas_resolvidos=anterior.get("alertas_resolvidos", {}),
        # correções aplicadas fora de um arquivo de update: status/rodada que o DOCX mostra até a
        # próxima rodada de update (que recalcula `blocos`; aí vale limpar o que ela já cobrir)
        ajustes_manuais=anterior.get("ajustes_manuais", {}),
    )
    Path(caminho).write_text(json.dumps(controle, ensure_ascii=False, indent=1), encoding="utf-8")
    return controle


def main(argv):
    """incorpora_update_docx.py <update> [<update> ...] --saida <json> [--controle <json>] [--datas d1,d2,...]"""
    def opcao(nome):
        if nome in argv:
            i = argv.index(nome)
            v = argv[i + 1]
            del argv[i:i + 2]
            return v
        return None
    saida = opcao("--saida")
    caminho_controle = opcao("--controle")
    datas = (opcao("--datas") or "").split(",")
    if not saida:
        raise SystemExit(__doc__)
    updates = argv
    indices = indice_atual()
    _SECOES.update(_indice_secoes())
    todos, nao, notas, realocar = {}, [], [], []
    por_rodada, vistos = {}, set()
    for u in updates:
        t, n, nt, rl, vis = casa(u, indices)
        por_rodada[Path(u).stem] = t
        todos.update(t)          # o último update vence
        nao += n
        realocar = rl or realocar
        notas = nt or notas
        vistos = vis
    Path(saida).write_text(json.dumps(dict(textos=todos, nao_casados=nao, notas=notas, realocar=realocar),
                                      ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(todos)} textos casados, {len(nao)} não casados, {len(notas)} notas editoriais, "
          f"{len(realocar)} textos de seção a realocar -> {saida}")
    if caminho_controle:
        rodadas = [dict(id=Path(u).stem, arquivo=Path(u).name, data=(datas[k] if k < len(datas) else ""))
                   for k, u in enumerate(updates)]
        por_h3, por_img, por_h2 = indices
        atuais = set(por_h3.values()) | set(por_img.values()) | set(por_h2.values())
        c = atualiza_controle(caminho_controle, rodadas, por_rodada, vistos, notas, realocar, atuais)
        from collections import Counter
        print(f"controle: {dict(Counter(v['status'] for v in c['blocos'].values()))}, "
              f"{len(c['novos_desde_ultima_rodada'])} itens novos desde a última rodada -> {caminho_controle}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    main(sys.argv[1:])
