"""Gera a apresentação (specs/2026-09-28_apresentacao) a partir de UM arquivo Markdown.

    python apresentacao/build/gera_apresentacao.py [arquivo.md] [--pptx] [--pdf] [--html] [--png] [--editavel] [--publicar]

Padrão: apresentacao/apresentacao.md; sem opção de formato, gera PPTX + PDF. Saídas em apresentacao/_build/
(gitignored). --publicar copia o PPTX e o PDF para apresentacao/ (versionados). --editavel gera também o PPTX
editável do Marp (experimental; precisa do LibreOffice). --png gera uma imagem por slide (conferência).

O que o pré-processador faz antes do Marp (que não tem variáveis nem condicionais):
  {{campo}}          campo do cabeçalho (frontmatter) do .md
  {{n:chave}}        número calculado de tabelas_finais/ (build/numeros.py); chave inexistente = erro
  {{qr:campo}}       QR code (segno) da URL do campo, como <img>
  fig:nome           figura de visualizacoes/ ou mapas/ (PNG do analise.py), reduzida para _build/img/
  captura:nome       captura de tela gerada pelo gerador (site no desktop/celular, capa do PDF)
  <!-- se: bloco --> ... <!-- /se -->           entra só se `bloco` está na lista `blocos` do cabeçalho
  <!-- se: publico=x --> ... <!-- /se -->      entra só se `publico` do cabeçalho é x
  <!-- se: com_campo --> ... <!-- /se -->      entra só se o campo do cabeçalho está preenchido (ex. com_secretaria)
  <!-- fonte: texto -->                         vira o rodapé do slide ("Fonte: texto")
  <!-- revisar -->                              texto nosso a revisar pela equipe: contado e listado no fim do build
  {{tabela:pendentes}}                          tabela de indicadores pendentes por eixo (estrutura_eixos.md)
Comentários HTML comuns ficam como notas do apresentador (vão para o PPTX).
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from PIL import Image

AQUI = Path(__file__).resolve().parent
APRES = AQUI.parent
RAIZ = APRES.parent
BUILD = APRES / "_build"
IMG = BUILD / "img"
sys.path.insert(0, str(AQUI))
import mapas_apresentacao  # noqa: E402
import numeros  # noqa: E402

LARGURA_MAX = 1800   # px -- figuras reduzidas (as PNGs do analise.py têm até 3.700 px)


def le_md(caminho):
    texto = Path(caminho).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        sys.exit(f"{caminho}: falta o cabeçalho (--- ... ---)")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def condicionais(corpo, meta):
    blocos = set(meta.get("blocos") or [])
    # campo preenchido liga o bloco com_<campo> sozinho (ex. a linha da secretaria na capa)
    blocos |= {f"com_{k}" for k, v in meta.items() if isinstance(v, str) and v.strip()}

    def resolve(m):
        cond, conteudo = m.group(1).strip(), m.group(2)
        if "=" in cond:
            chave, valor = (x.strip() for x in cond.split("=", 1))
            ok = str(meta.get(chave, "")) == valor
        else:
            ok = cond in blocos
        return conteudo if ok else ""

    anterior = None
    while anterior != corpo:   # blocos aninhados: resolve de dentro para fora
        anterior = corpo
        corpo = re.sub(r"<!--\s*se:\s*([^>]*?)\s*-->((?:(?!<!--\s*se:).)*?)<!--\s*/se\s*-->", resolve, corpo, flags=re.S)
    return corpo


_MANIFESTO = None


def pdf_mapa(nome):
    """PDF do mapa: próprio da apresentação (build/mapas_apresentacao.py) ou a versão de impressão do analise.py."""
    if nome in mapas_apresentacao.MAPAS:
        return mapas_apresentacao.gera(nome)[0]
    a4 = RAIZ / "mapas/a4" / f"{nome}.pdf"
    return a4 if a4.exists() else None


def fonte_mapa(nome):
    """Fonte (e nota do teto de cor) do mapa A4, do manifesto gravado pelo analise.py -- vai para o rodapé do slide."""
    global _MANIFESTO
    if nome in mapas_apresentacao.MAPAS:
        return mapas_apresentacao.gera(nome)[1].replace("'", "’")
    if _MANIFESTO is None:
        import pandas as pd
        arq = RAIZ / "visualizacoes/a4/_manifesto.csv"
        _MANIFESTO = ({Path(r.arquivo).stem: r.fonte for r in pd.read_csv(arq).fillna("").itertuples()}
                      if arq.exists() else {})
    f = re.sub(r"\s+", " ", str(_MANIFESTO.get(nome, ""))).strip()
    f = f.replace("; o valor real está na tabela do apêndice", "").replace("'", "’")
    return f.rstrip(".")


def figura(nome):
    """Mapas: a versão de impressão (mapas/a4/<nome>.pdf), que tem o teto de cor no percentil 95 nos mapas contínuos por
    bairro -- o mesmo tratamento de valores extremos do site (pedido do usuário, 2026-09-28: "sempre os mapas sem os
    outliers") -- e não tem título embutido (o título é o do slide). Gráficos: a PNG de tela do analise.py."""
    a4 = pdf_mapa(nome)
    if a4:
        destino = IMG / f"{nome}_a4.png"
        if not destino.exists() or destino.stat().st_mtime < a4.stat().st_mtime:
            import pymupdf
            pag = pymupdf.open(a4)[0]
            pag.get_pixmap(dpi=int(LARGURA_MAX / (pag.rect.width / 72))).save(str(destino))
        return f"img/{destino.name}"
    for pasta, ext in (("mapas", ".jpg"), ("visualizacoes", ".png")):
        origem = RAIZ / pasta / f"{nome}.png"
        if origem.exists():
            destino = IMG / f"{nome}{ext}"
            if not destino.exists() or destino.stat().st_mtime < origem.stat().st_mtime:
                im = Image.open(origem)
                im.thumbnail((LARGURA_MAX, LARGURA_MAX))
                if ext == ".jpg":
                    im.convert("RGB").save(destino, quality=88, optimize=True)
                else:
                    im.save(destino, optimize=True)
            return f"img/{destino.name}"
    raise FileNotFoundError(f"fig:{nome} não existe em mapas/ nem em visualizacoes/")


def qr(url):
    import segno
    destino = IMG / "qr.svg"
    segno.make(url, error="m").save(str(destino), scale=10, border=1, dark="#004a80")
    return f'<img class="qrcode" src="img/{destino.name}" alt="QR code para {url}">'


def tabela_pendentes():
    linhas = ["<table><tr><th>Eixo</th><th>Indicadores</th><th>Sem dado ainda</th><th></th></tr>"]
    for eixo, pend, total in numeros.pendentes_por_eixo():
        larg = 12 * total
        barra = (f'<span class="barra ok" style="width:{12 * (total - pend)}px"></span>'
                 f'<span class="barra" style="width:{12 * pend}px"></span>') if total else ""
        linhas.append(f"<tr><td>{eixo}</td><td>{total}</td><td>{pend or '—'}</td><td style='width:{larg}px'>{barra}</td></tr>")
    return "".join(linhas) + "</table>"


def capturas(url_site):
    """Capturas do site (desktop e celular) e da capa do PDF, para os slides de produtos. Só gera se faltarem."""
    alvos = {"site_desktop": IMG / "captura_site_desktop.png", "site_celular": IMG / "captura_site_celular.png",
             "pdf_capa": IMG / "captura_pdf_capa.png", "pdf_pagina": IMG / "captura_pdf_pagina.png"}
    if not all(p.exists() for p in alvos.values()):
        site = (RAIZ / "website/index.html").as_uri()
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                nav = None
                for canal in ("chrome", "msedge", None):   # Chrome instalado (convenção do projeto), Edge, o do Playwright
                    try:
                        nav = p.chromium.launch(channel=canal) if canal else p.chromium.launch()
                        break
                    except Exception:
                        continue
                if nav is None:
                    raise RuntimeError("nenhum navegador para o Playwright")
                pg = nav.new_page(viewport={"width": 1440, "height": 900})
                pg.goto(site + "#visao-geral"); pg.wait_for_timeout(1200)
                pg.screenshot(path=str(alvos["site_desktop"]))
                pg = nav.new_page(viewport={"width": 390, "height": 780}, device_scale_factor=2)
                pg.goto(site + "#prioridade/mortalidade-infantil-por-bairro"); pg.wait_for_timeout(1500)
                pg.screenshot(path=str(alvos["site_celular"]))
                nav.close()
        except Exception as e:
            print(f"AVISO: capturas do site não geradas ({e})")
        pdf = RAIZ / "relatorio/latex/_build/relatorio.pdf"
        pdf = pdf if pdf.exists() else RAIZ / "relatorio/analise_primeira_infancia.pdf"
        try:
            import pymupdf
            d = pymupdf.open(pdf)
            d[0].get_pixmap(dpi=110).save(str(alvos["pdf_capa"]))
            pag = next((i for i in range(d.page_count) if "Crianças até 4 anos (número)" in d[i].get_text()
                        and i > 10), 14)
            d[pag].get_pixmap(dpi=110).save(str(alvos["pdf_pagina"]))
        except Exception as e:
            print(f"AVISO: capturas do PDF não geradas ({e})")
    return {k: f"img/{v.name}" for k, v in alvos.items()}


def rodape_dos_mapas(corpo):
    """Slide com mapa A4 e sem <!-- fonte: --> própria ganha a fonte do mapa (do manifesto) no rodapé."""
    slides = re.split(r"(?m)^---\s*$", corpo)
    for k, sl in enumerate(slides):
        if "<!-- fonte:" in sl or "_footer" in sl:
            continue
        fontes, notas = [], []   # mesma fonte em dois mapas aparece uma vez; as notas (teto de cor) vão no fim
        for nome in re.findall(r"fig:(\w+)", sl):
            if pdf_mapa(nome):
                base, _, nota = fonte_mapa(nome).partition(". Nota: ")
                if base and base not in fontes:
                    fontes.append(base)
                if nota and nota not in notas:
                    notas.append(nota)
        if fontes:
            texto = "; ".join(fontes) + (". Nota: " + "; ".join(notas) if notas else "")
            slides[k] = sl.rstrip("\n") + f"\n\n<!-- fonte: {texto} -->\n\n"
    return "---".join(slides)


def preprocessa(meta, corpo):
    corpo = condicionais(corpo, meta)
    corpo = rodape_dos_mapas(corpo)
    revisar = len(re.findall(r"<!--\s*revisar\s*-->", corpo))
    corpo = re.sub(r"<!--\s*revisar\s*-->", "", corpo)
    corpo = re.sub(r"<!--\s*fonte:\s*(.*?)\s*-->", lambda m: f"<!-- _footer: 'Fonte: {m.group(1)}' -->", corpo)
    corpo = corpo.replace("{{tabela:pendentes}}", tabela_pendentes())
    corpo = re.sub(r"\{\{n:(\w+)\}\}", lambda m: numeros.valor(m.group(1)), corpo)
    corpo = re.sub(r"\{\{qr:(\w+)\}\}", lambda m: qr(meta[m.group(1)]), corpo)
    caps = None
    if "captura:" in corpo:
        caps = capturas(meta.get("url_site", ""))
        corpo = re.sub(r"captura:(\w+)", lambda m: caps[m.group(1)], corpo)
    corpo = re.sub(r"fig:(\w+)", lambda m: figura(m.group(1)), corpo)

    def campo(m):
        if m.group(1) not in meta:
            raise KeyError(f"{{{{{m.group(1)}}}}}: campo não existe no cabeçalho")
        return str(meta[m.group(1)] or "")
    corpo = re.sub(r"\{\{(\w+)\}\}", campo, corpo)
    sobra = re.findall(r"\{\{[^}]*\}\}", corpo)
    if sobra:
        sys.exit(f"placeholders não resolvidos: {sobra}")
    return corpo, revisar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo", nargs="?", default=str(APRES / "apresentacao.md"))
    for f in ("pptx", "pdf", "html", "png", "editavel", "publicar"):
        ap.add_argument(f"--{f}", action="store_true")
    a = ap.parse_args()
    formatos = [f for f in ("pptx", "pdf", "html", "png") if getattr(a, f)] or ["pptx", "pdf"]

    meta, corpo = le_md(a.arquivo)
    IMG.mkdir(parents=True, exist_ok=True)
    shutil.copytree(RAIZ / "relatorio/latex/fontes", BUILD / "fontes", dirs_exist_ok=True)
    shutil.copy(APRES / "tema/ipp.css", BUILD / "ipp.css")
    shutil.copy(RAIZ / "website/assets/images/ipp-logo.png", IMG / "ipp-logo.png")
    corpo, revisar = preprocessa(meta, corpo)

    cab = {"marp": True, "theme": "ipp", "paginate": True, "size": "16:9", "lang": "pt-BR",
           "title": meta.get("titulo", ""), "footer": meta.get("rodape", "")}
    nome = Path(a.arquivo).stem
    md = BUILD / f"{nome}.md"
    md.write_text("---\n" + yaml.safe_dump(cab, allow_unicode=True, sort_keys=False) + "---\n" + corpo, encoding="utf-8")
    n_slides = len(re.findall(r"^---\s*$", corpo, re.M)) + 1

    npx = shutil.which("npx") or "npx"
    base = [npx, "marp", md.name, "--theme-set", "ipp.css", "--html", "--allow-local-files"]
    saidas = []
    for f in formatos:
        args = {"pptx": ["--pptx"], "pdf": ["--pdf", "--pdf-notes"], "html": ["--html"], "png": ["--images", "png"]}[f]
        destino = BUILD / (f"{nome}.{f}" if f != "png" else f"png/{nome}.png")
        destino.parent.mkdir(exist_ok=True)
        # stdin fechado: sem isso o marp-cli espera o Markdown pela entrada padrão (fica parado quando não é terminal)
        r = subprocess.run(base + args + ["-o", str(destino)], cwd=BUILD, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=900)
        if r.returncode != 0:
            sys.exit(f"marp falhou ({f}):\n{r.stderr[-2000:]}")
        saidas.append(destino)
    if a.editavel:
        destino = BUILD / f"{nome}_editavel.pptx"
        r = subprocess.run(base + ["--pptx", "--pptx-editable", "-o", str(destino)], cwd=BUILD, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=900)
        print("PPTX editável:", destino if r.returncode == 0 else f"falhou ({r.stderr[-500:]})")
    print(f"{n_slides} slides; {revisar} trechos marcados para revisão da equipe")
    for s in saidas:
        print("  ", s.relative_to(RAIZ))
    if a.publicar:
        for s in saidas:
            if s.suffix in (".pptx", ".pdf"):
                shutil.copy(s, APRES / f"apresentacao_primeira_infancia{'' if nome == 'apresentacao' else '_' + nome}{s.suffix}")
        print("publicado em apresentacao/")


if __name__ == "__main__":
    main()
