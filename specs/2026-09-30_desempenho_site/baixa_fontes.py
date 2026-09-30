"""Baixa as fontes do site (Fraunces, IBM Plex Sans, IBM Plex Mono) do Google Fonts e escreve website/build/fontes.css (o gerador põe no <style> do index.html).

specs/2026-09-30_desempenho_site: o site passa a servir as fontes do próprio domínio (antes: 1 CSS de
fonts.googleapis.com + woff2 de fonts.gstatic.com, duas origens de terceiros). Mesma URL de pedido que o site usava,
mesmo arquivo que o Chrome recebe; só os subconjuntos latin e latin-ext (com o unicode-range do Google, então o
navegador só baixa o que a página usa). Rodar de novo só para trocar pesos/famílias:

    python specs/2026-09-30_desempenho_site/baixa_fontes.py
"""
import pathlib
import re
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parents[2]
URL = ("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,440;9..144,500;9..144,600;9..144,700"
       "&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
SUBCONJUNTOS = ("latin", "latin-ext")
CURTO = {"Fraunces": "fraunces", "IBM Plex Sans": "plex-sans", "IBM Plex Mono": "plex-mono"}

LICENCA = """/* fontes.css -- GERADO por specs/2026-09-30_desempenho_site/baixa_fontes.py (não editar à mão).
   Fontes servidas pelo próprio site (antes Google Fonts). Fraunces (c) The Fraunces Project Authors; IBM Plex Sans e
   IBM Plex Mono (c) IBM Corp. Todas sob a SIL Open Font License 1.1 -- https://openfontlicense.org */
"""


def main():
    css = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": UA})).read().decode()
    pasta = RAIZ / "website" / "assets" / "fonts"
    pasta.mkdir(parents=True, exist_ok=True)
    saida, baixados = [LICENCA], {}
    for sub, bloco in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face \{.*?\})", css, re.S):
        if sub not in SUBCONJUNTOS:
            continue
        fam = re.search(r"font-family: '([^']+)'", bloco).group(1)
        peso = re.search(r"font-weight: ([\d ]+);", bloco).group(1)
        url = re.search(r"url\((\S+?)\)", bloco).group(1)
        # Fraunces e Plex Sans são variáveis (um arquivo para todos os pesos); Plex Mono tem um arquivo por peso
        nome = f"{CURTO[fam]}-{sub}.woff2" if url not in baixados and fam != "IBM Plex Mono" else None
        if fam == "IBM Plex Mono":
            nome = f"{CURTO[fam]}-{peso}-{sub}.woff2"
        nome = baixados.setdefault(url, nome)
        if not (pasta / nome).exists():
            (pasta / nome).write_bytes(urllib.request.urlopen(url).read())
        saida.append(f"/* {sub} */\n" + bloco.replace(f"url({url})", f"url(assets/fonts/{nome})") + "\n")
    (RAIZ / "website" / "build" / "fontes.css").write_text("".join(saida), encoding="utf-8")
    print(len(saida) - 1, "@font-face;", len(set(baixados.values())), "arquivos em", pasta)


if __name__ == "__main__":
    main()
