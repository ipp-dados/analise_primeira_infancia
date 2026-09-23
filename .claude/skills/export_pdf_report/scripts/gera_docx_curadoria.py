"""Gera `relatorio/curadoria_textos.docx` (Bloco 5 de `specs/ajuste_eixos/plan.md`).

Documento Word para curadoria de textos de análise fora do notebook/HTML:
abre com um Sumário (campo TOC nativo do Word, sob controle do usuário --
ele mesmo pede "Atualizar campo" no Word conforme edita o documento) e uma
Introdução (placeholder de 250 palavras, mesmo princípio do HTML/PDF), 1
heading nível 1 por eixo, 1 heading nível 2 por subseção
(`specs/estrutura_eixos.md`, pendentes incluídas), e para cada subseção
não-pendente 1 "opção" por visualização/mapa real (heading nível 3 +
imagem PNG real, redimensionada, + 1 parágrafo de texto placeholder).
Subseções sem visualização/mapa dedicado (`fonte`-only) ainda ganham 1
bloco de texto, sem imagem.

Cada parágrafo de texto carrega um bookmark OOXML (`w:bookmarkStart`/
`w:bookmarkEnd`) nomeado a partir de um ID estável (nome do arquivo de
imagem sem extensão, ou `"{eixo}::{subseção}"` quando não há arquivo) --
permite regenerar o documento "por cima" de si mesmo sem perder texto já
editado à mão (`gera_docx(docx_anterior=...)`), e permite ao futuro skill de
sincronização (Bloco 7 do plano) extrair `{bookmark: texto}` de volta.

Reaproveita `parse_estrutura_eixos()`/`valida_estrutura()`/`_nomes_de_arquivo()`
de `gera_estrutura_eixos.py` (mesma pasta) -- não reimplementa o parsing do
`.md`. Independente de `build_html_report.py`/`build_notebook_report.py`
(nenhum import compartilhado além do parser acima), por convenção deste
projeto de manter cada gerador de relatório autocontido (`CLAUDE.md`).

Como os demais scripts desta pasta, espera ser executado com o diretório de
trabalho na raiz do projeto (`specs/estrutura_eixos.md`, `visualizacoes/`,
`mapas/`, `relatorio/` são todos caminhos relativos a ela).

CLI:
    python gera_docx_curadoria.py [<docx_anterior>]

Sem argumento: gera do zero (todo texto placeholder, sem apêndice de
órfãos). Com argumento: lê `<docx_anterior>` para preservar texto já
editado à mão e mover blocos removidos da estrutura para o apêndice "Textos
órfãos" em vez de descartá-los. Destino sempre `relatorio/curadoria_textos.docx`
(hardcoded, mesma convenção dos scripts irmãos desta pasta).
"""

import hashlib
import io
import random
import re
import sys
from pathlib import Path

from PIL import Image
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches

from gera_estrutura_eixos import _nomes_de_arquivo, parse_estrutura_eixos, valida_estrutura

CAMINHO_SAIDA_PADRAO = "relatorio/curadoria_textos.docx"

_DIR_POR_CAMPO = {"visualização": "visualizacoes", "mapa": "mapas"}

# Largura máxima / qualidade JPEG na reamostragem das imagens antes de
# embutir no .docx -- mapas/*.png chegam a ~6MB cada (CLAUDE.md); embutir
# ~130 imagens sem redimensionar deixaria o documento gigante.
_LARGURA_MAX_PX = 1000
_QUALIDADE_JPEG = 82

# Constraints de nome de bookmark OOXML: só [A-Za-z0-9_], precisa começar
# com letra, versões antigas do Word truncam por volta de 40 caracteres.
_BOOKMARK_MAXLEN = 40
_BOOKMARK_TRUNC = 32


# ------------------------------------------------------------ lorem ipsum --
# Copiado literalmente de build_html_report.py (_LOREM_WORDS/_lorem) --
# specs/ajuste_eixos/specs.md §7 pede o MESMO vocabulário/algoritmo
# determinístico nos 3 artefatos (HTML/PDF/DOCX). Não importado de lá de
# propósito -- este script é autocontido (ver docstring acima).
_LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam "
    "quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo "
    "consequat duis aute irure dolor in reprehenderit voluptate velit esse "
    "cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat "
    "non proident sunt culpa qui officia deserunt mollit anim id est laborum "
    "sed ut perspiciatis unde omnis iste natus error voluptatem accusantium "
    "doloremque laudantium totam rem aperiam eaque ipsa quae ab illo inventore "
    "veritatis quasi architecto beatae vitae dicta explicabo nemo ipsam "
    "quia voluptas aspernatur aut odit fugit consequuntur magni dolores eos "
    "qui ratione sequi nesciunt neque porro quisquam dolorem adipisci numquam "
    "eius modi tempora incidunt magnam quaerat minima veniam nostrum "
    "exercitationem ullam corporis suscipit laboriosam nisi aliquid ex ea "
    "commodi consequatur autem vel eum iure reprehenderit qui in ea "
    "voluptate esse quam nihil molestiae illum facere possimus omnis dolor "
    "assumenda repellendus temporibus autem quibusdam et aut officiis "
    "debitis rerum necessitatibus saepe eveniet voluptates repudiandae "
    "recusandae itaque earum rerum hic tenetur a sapiente delectus reiciendis "
    "voluptatibus maiores alias perferendis doloribus asperiores repellat "
    "curabitur pretium tincidunt lacus felis euismod semper porta massa "
    "sagittis nunc vitae mauris fringilla vestibulum ante ipsum primis "
    "faucibus orci luctus posuere cubilia curae mus donec pede justo "
    "fringilla vel aliquet nec vulputate eget arcu in enim justo rhoncus ut "
    "imperdiet a venenatis vitae justo nullam dictum felis eu pede mollis "
    "pretium integer tincidunt cras dapibus vivamus elementum semper nisi "
    "aenean vulputate eleifend tellus aenean leo ligula porttitor eu "
    "consequat vitae eleifend ac enim aliquam lorem ante dapibus nec "
    "condimentum quam curabitur vel hendrerit libero pellentesque habitant "
    "morbi tristique senectus et netus malesuada fames ac turpis egestas "
    "proin pharetra nonummy pede mauris viverra diam vitae quam suspendisse "
    "potenti nullam porttitor lacus at turpis donec posuere metus vitae "
    "ipsum aliquam nunc praesent augue eget arcu dictum varius duis at "
    "consectetuer lorem donec massa sapien faucibus et molestie ac feugiat "
    "sed lectus vestibulum mauris malesuada fringilla est ullamcorper "
    "eget nulla facilisi etiam dignissim diam quis enim lobortis scelerisque "
    "fermentum dui aliquet nibh praesent tristique senectus netus fames turpis egestas"
).split()


def _lorem(seed, palavras=None):
    rng = random.Random(seed)
    if palavras is None:
        palavras = random.Random(f"{seed}-palavras").randint(100, 200)
    corpo = " ".join(rng.choice(_LOREM_WORDS) for _ in range(palavras))
    return corpo[:1].upper() + corpo[1:] + "."


# --------------------------------------------------------------- bookmarks --

def add_bookmark(paragraph, bookmark_name, bookmark_id):
    """Envolve TODO o parágrafo `paragraph` num bookmark OOXML nomeado
    `bookmark_name` (bookmarkStart antes de qualquer run, bookmarkEnd depois
    de todas) -- nunca um bookmark span multiplos paragrafos, o que mantem a
    extração (`extrai_textos_por_bookmark`) trivial: 1 bookmark = 1 texto."""
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), str(bookmark_id))
    start.set(qn('w:name'), bookmark_name)
    paragraph._p.insert(0, start)
    end = OxmlElement('w:bookmarkEnd')
    end.set(qn('w:id'), str(bookmark_id))
    paragraph._p.append(end)


def add_toc_field(paragraph):
    """Insere um campo `TOC` nativo do Word no parágrafo `paragraph` --
    diferente de uma lista estática (HTML/PDF deste projeto usam uma,
    construída a partir do `toc`/`_toc` de cada gerador), um campo de
    verdade fica sob controle do usuário: à medida que ele edita o .docx
    (renomeia um heading, apaga uma subseção, promove um H3 pendente depois
    de implementado), basta clicar com o botão direito e "Atualizar campo"
    (ou F9) para o sumário refletir a estrutura atual do documento, sem
    precisar regenerar nada por script. python-docx não roda o campo (só o
    Word calcula os títulos + números de página), por isso o texto inicial
    é só um aviso -- vira um sumário de verdade na primeira abertura no
    Word (ver `_forca_atualizacao_de_campos` abaixo)."""
    run = paragraph.add_run()

    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')
    run._r.append(fld_begin)

    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = 'TOC \\o "1-3" \\h \\z \\u'
    run._r.append(instr)

    fld_sep = OxmlElement('w:fldChar')
    fld_sep.set(qn('w:fldCharType'), 'separate')
    run._r.append(fld_sep)

    placeholder = OxmlElement('w:t')
    placeholder.text = (
        "Clique com o botão direito neste texto e escolha “Atualizar "
        "campo” (ou selecione tudo com Ctrl+A e pressione F9) para "
        "gerar o sumário a partir dos títulos deste documento."
    )
    run._r.append(placeholder)

    fld_end = OxmlElement('w:fldChar')
    fld_end.set(qn('w:fldCharType'), 'end')
    run._r.append(fld_end)


def _forca_atualizacao_de_campos(document):
    """Seta `<w:updateFields w:val="true"/>` em settings.xml -- pede ao Word
    pra recalcular todos os campos (o TOC acima incluído) na abertura do
    arquivo, em vez de depender só do usuário lembrar de atualizar
    manualmente. Best-effort: numa versão de python-docx sem `.settings`
    isso só deixa de forçar, não quebra a geração (o campo ainda funciona
    manualmente)."""
    try:
        settings = document.settings.element
        update_fields = OxmlElement('w:updateFields')
        update_fields.set(qn('w:val'), 'true')
        settings.append(update_fields)
    except AttributeError:
        pass


def extrai_textos_por_bookmark(caminho_docx):
    """Retorna {bookmark_name: texto_do_paragrafo} lendo um .docx já gerado."""
    doc = Document(caminho_docx)
    out = {}
    for paragraph in doc.paragraphs:
        p_xml = paragraph._p
        starts = p_xml.findall(qn('w:bookmarkStart'))
        for s in starts:
            name = s.get(qn('w:name'))
            if name:
                out[name] = paragraph.text
    return out


def _bookmark_name(id_):
    """Sanitiza `id_` (string livre -- nome de arquivo sem extensão, ou
    'eixo::subseção') para um nome de bookmark OOXML válido: só
    [A-Za-z0-9_], começa com letra, <= 40 chars (versões antigas do Word
    truncam por aí). Quando o resultado sanitizado passaria de 40 chars,
    trunca pra ~32 e acrescenta um hash de 8 hex do ID ORIGINAL (não do
    sanitizado) -- assim duas strings bem diferentes que colapsam pro mesmo
    prefixo sanitizado ainda saem com sufixos diferentes."""
    limpo = re.sub(r"[^A-Za-z0-9_]", "", id_)
    if not limpo or not limpo[0].isalpha():
        limpo = "b_" + limpo
    if len(limpo) > _BOOKMARK_MAXLEN:
        sufixo = hashlib.sha1(id_.encode("utf-8")).hexdigest()[:8]
        limpo = limpo[:_BOOKMARK_TRUNC] + "_" + sufixo
    return limpo


# ------------------------------------------------------------------ imagem --

def _imagem_redimensionada(caminho):
    """Abre `caminho` (PNG real de visualizacoes/ ou mapas/), redimensiona
    para no máximo `_LARGURA_MAX_PX` de largura e reencoda como JPEG
    (qualidade `_QUALIDADE_JPEG`) num BytesIO em memória -- mapas/*.png
    chegam a ~6MB cada; sem isso, ~130 imagens deixariam o .docx enorme.
    JPEG (não WebP -- Word não embute WebP de forma confiável)."""
    img = Image.open(caminho).convert("RGB")
    if img.width > _LARGURA_MAX_PX:
        altura = int(img.height * _LARGURA_MAX_PX / img.width)
        img = img.resize((_LARGURA_MAX_PX, altura), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=_QUALIDADE_JPEG)
    buf.seek(0)
    return buf


def _arquivos_de(campos, chave):
    """campos.get(chave) pode ser ausente, string ou lista (convenção de
    parse_estrutura_eixos()) -- normaliza pra lista de nomes de arquivo,
    reaproveitando _nomes_de_arquivo() de gera_estrutura_eixos.py."""
    valor = campos.get(chave)
    if valor is None:
        return []
    return _nomes_de_arquivo(valor)


# -------------------------------------------------------------- geração ---

def gera_docx(caminho_saida=CAMINHO_SAIDA_PADRAO, docx_anterior=None):
    estrutura = parse_estrutura_eixos()
    valida_estrutura(estrutura)

    textos_curados = {}
    if docx_anterior and Path(docx_anterior).exists():
        textos_curados = extrai_textos_por_bookmark(docx_anterior)

    ids_gerados = set()          # bookmark names emitidos nesta rodada (conteúdo real)
    registro_bookmarks = {}      # bookmark_name -> id_ original (detecção de colisão)
    _contador = [0]

    def next_id():
        _contador[0] += 1
        return _contador[0]

    doc = Document()

    # ---- sumario + introducao (pedido do usuario, specs/ajuste_eixos) -----
    # Sumario = campo TOC nativo do Word (add_toc_field), nao uma lista
    # estatica -- "para controle do usuario": ele mesmo pede a atualizacao
    # no Word conforme edita o documento, sem depender de regerar via
    # script. Mesmo lugar/ordem do HTML e do PDF (Sumario antes,
    # Introducao logo depois, ambos antes do primeiro eixo).
    # "Sumário" NÃO usa add_heading (estilo Heading N) de propósito: o campo
    # TOC abaixo varre os níveis 1-3 do documento inteiro, e um heading real
    # aqui apareceria listado dentro do próprio sumário, apontando pra si
    # mesmo (mesmo motivo pelo qual build_html_report.py também não usa
    # h2() pra isso).
    rotulo = doc.add_paragraph()
    rotulo.add_run("SUMÁRIO").bold = True
    add_toc_field(doc.add_paragraph())

    doc.add_heading("Introdução", level=1)
    # Bookmark fixo "introducao": texto curado sobrevive à regeneração e
    # sincroniza_docx.py o leva para HTML/PDF (textos_curados.json).
    p_intro = doc.add_paragraph(textos_curados.get("introducao") or _lorem("introducao-relatorio-docx", 250))
    add_bookmark(p_intro, "introducao", next_id())
    registro_bookmarks["introducao"] = "introducao"
    ids_gerados.add("introducao")

    def bloco_texto(id_):
        """Escreve 1 parágrafo de texto (curado, se já existir, senão lorem
        ipsum determinístico) com bookmark nomeado a partir de `id_`, e
        devolve o bookmark_name usado."""
        bname = _bookmark_name(id_)
        if bname in registro_bookmarks and registro_bookmarks[bname] != id_:
            raise ValueError(
                f"Colisão de bookmark: {bname!r} gerado tanto para "
                f"{registro_bookmarks[bname]!r} quanto para {id_!r} -- "
                "IDs deveriam ser únicos no projeto (specs/tech-stack.md)."
            )
        registro_bookmarks[bname] = id_
        ids_gerados.add(bname)
        texto = textos_curados.get(bname) or _lorem(id_)
        p = doc.add_paragraph(texto)
        add_bookmark(p, bname, next_id())
        return bname

    n_imagens = 0

    for eixo in estrutura:
        doc.add_heading(eixo["eixo"], level=1)
        for sub in eixo["subsecoes"]:
            titulo = sub["titulo"]
            campos = sub["campos"]
            doc.add_heading(titulo, level=2)

            if campos.get("status") == "pendente":
                p = doc.add_paragraph(f'[PENDENTE] {campos.get("nota", "")}')
                p.style = doc.styles["Intense Quote"]
                continue

            opcoes = [("visualização", nome) for nome in _arquivos_de(campos, "visualização")]
            opcoes += [("mapa", nome) for nome in _arquivos_de(campos, "mapa")]

            if not opcoes:
                # fonte-only: sem visualização/mapa dedicado em analise.py.
                # Ainda assim ganha 1 bloco de texto curável (specs.md §7).
                bloco_texto(f"{eixo['eixo']}::{titulo}")
                continue

            for campo, nome in opcoes:
                id_ = Path(nome).stem
                label = id_.replace("_", " ").capitalize()
                doc.add_heading(label, level=3)
                pasta = _DIR_POR_CAMPO[campo]
                stream = _imagem_redimensionada(Path(pasta) / nome)
                doc.add_picture(stream, width=Inches(5.5))
                n_imagens += 1
                bloco_texto(id_)

            tabelas = _arquivos_de(campos, "tabela")
            if tabelas:
                p = doc.add_paragraph()
                nomes_fmt = ", ".join(f"`{t}`" for t in tabelas)
                run = p.add_run(f"Tabela de apoio: {nomes_fmt}")
                run.italic = True

    # Blocos cujo bookmark existia no docx_anterior mas não foi regenerado
    # nesta rodada (indicador removido/renomeado na estrutura) -- preservados
    # num apêndice em vez de descartados (plan.md §5.2).
    orfaos = {bname: texto for bname, texto in textos_curados.items() if bname not in ids_gerados}
    if orfaos:
        doc.add_heading("Textos órfãos", level=1)
        for bname, texto in orfaos.items():
            # O rótulo (nome do bookmark original) fica num parágrafo à
            # parte, SEM bookmark -- só o parágrafo de texto carrega o
            # bookmark (mesmo padrão de "heading não-bookmarked + texto
            # bookmarked" usado nos blocos normais acima). Isso é o que
            # garante round-trip correto: uma extração futura recupera o
            # TEXTO do órfão sob o bookmark_name original, não o rótulo --
            # e por isso o órfão sobrevive intacto a uma nova rodada de
            # regeneração enquanto continuar fora da estrutura.
            rotulo = doc.add_paragraph()
            rotulo.add_run(bname).bold = True
            p = doc.add_paragraph(texto)
            add_bookmark(p, bname, next_id())

    _forca_atualizacao_de_campos(doc)

    Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
    doc.save(caminho_saida)

    return {
        "doc": doc,
        "eixos": len(estrutura),
        "subsecoes": sum(len(e["subsecoes"]) for e in estrutura),
        "imagens": n_imagens,
        "bookmarks": len(registro_bookmarks) + len(orfaos),
        "orfaos": len(orfaos),
    }


if __name__ == "__main__":
    # Windows abre stdout no codepage do console (ex. cp1252), que não cobre
    # os emojis dos títulos de eixo -- força UTF-8 (mesma solução usada em
    # gera_estrutura_eixos.py).
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    docx_anterior = sys.argv[1] if len(sys.argv) > 1 else None
    resumo = gera_docx(docx_anterior=docx_anterior)

    print(f"Eixos: {resumo['eixos']}")
    print(f"Subseções: {resumo['subsecoes']}")
    print(f"Imagens embutidas: {resumo['imagens']}")
    print(f"Bookmarks: {resumo['bookmarks']} (órfãos: {resumo['orfaos']})")
    print(f"Gerado: {CAMINHO_SAIDA_PADRAO}")
