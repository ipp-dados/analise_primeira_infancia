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
    python gera_docx_curadoria.py [<docx_anterior>] [--textos <json de incorpora_update_docx.py>] [--controle <json>]
    (--controle usa relatorio/controle_revisao.json se existir; sem ele, o documento sai sem marcas de status)

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
from docx.shared import Inches, Pt, RGBColor

from gera_estrutura_eixos import _nomes_de_arquivo, parse_estrutura_eixos, valida_estrutura

CAMINHO_SAIDA_PADRAO = "relatorio/curadoria_textos.docx"
CAMINHO_CONTROLE_PADRAO = "relatorio/controle_revisao.json"

# ---- controle de revisão (pedido do usuário, 2026-09-24) ----------------------
# Status de cada bloco de texto, marcado no título (e portanto no Sumário, que é
# um campo TOC dos títulos) e resumido na tabela "Controle de revisão". Fonte:
# relatorio/controle_revisao.json, gerado por incorpora_update_docx.py a partir
# dos arquivos de update (o campo "alertas" é editado à mão).
STATUS_ICONE = {"revisado": "✅", "atualizado": "✏️", "pendente": "⬜", "indicador": "🚧"}
STATUS_ROTULO = {
    "revisado": "Revisado — texto confirmado sem mudança numa rodada posterior",
    "atualizado": "Atualizado — texto novo ou alterado na última rodada em que apareceu (falta uma revisão)",
    "pendente": "Texto a escrever — ainda é o texto provisório (lorem ipsum)",
    "indicador": "Indicador pendente — ainda sem dado no relatório",
}
ICONE_ALERTA = "⚠️"

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


# -------------------------------------------------------- controle de revisão --

def _monta_controle(doc, ancora, linhas, rodada_rotulo):
    """Legenda + contagem + tabela (Eixo | Subseção | Item | Status | Rodada | Observações), inserida
    logo depois do Sumário (no lugar do parágrafo `ancora`), na mesma ordem dos títulos."""
    from collections import Counter
    elementos = []

    def par(texto="", negrito=False, tamanho=None, italico=False):
        p = doc.add_paragraph()
        r = p.add_run(texto)
        r.bold, r.italic = negrito, italico
        if tamanho:
            r.font.size = Pt(tamanho)
        elementos.append(p._p)
        return p

    par("CONTROLE DE REVISÃO", negrito=True)
    rod = ", ".join(rodada_rotulo.values()) or "—"
    par(f"Rodadas de atualização incorporadas: {rod}. O status de cada item aparece no fim do título "
        "(e por isso também no Sumário, depois de “Atualizar campo”).", tamanho=9, italico=True)
    for st in ("revisado", "atualizado", "pendente", "indicador"):
        par(f"{STATUS_ICONE[st]}  {STATUS_ROTULO[st]}", tamanho=9)
    par(f"◐  Subseção com parte dos textos escritos     {ICONE_ALERTA}  Há algo a conferir (ver observação)", tamanho=9)
    c = Counter(l[3] for l in linhas)
    n_obs = sum(1 for l in linhas if l[5] and l[3] != "indicador")
    par("Situação: " + " · ".join(f"{STATUS_ICONE[k]} {c.get(k, 0)}" for k in ("revisado", "atualizado", "pendente", "indicador"))
        + f" · {n_obs} itens com observação", negrito=True, tamanho=9)

    tabela = doc.add_table(rows=1, cols=6)
    tabela.style = doc.styles["Table Grid"]
    for cel, t in zip(tabela.rows[0].cells, ("Eixo", "Subseção", "Item", "Status", "Rodada", "Observações")):
        cel.text = ""
        r = cel.paragraphs[0].add_run(t)
        r.bold = True
        r.font.size = Pt(8)
    for eixo_nome, secao, item, st, rodada, obs in linhas:
        cels = tabela.add_row().cells
        for cel, t in zip(cels, (eixo_nome, secao, item, f"{STATUS_ICONE[st]} {st}", rodada, obs)):
            cel.text = ""
            cel.paragraphs[0].add_run(t).font.size = Pt(8)
    elementos.append(tabela._tbl)
    par("")

    atual = ancora._p
    for el in elementos:
        atual.addnext(el)
        atual = el
    ancora._p.getparent().remove(ancora._p)


# -------------------------------------------------------------- geração ---

def _eh_lorem(texto):
    ws = [w.lower().strip(".,;:") for w in (texto or "").split() if w.strip(".,;:")]
    lorem = set(_LOREM_WORDS)
    return not ws or sum(w in lorem for w in ws) / len(ws) > 0.85


def gera_docx(caminho_saida=CAMINHO_SAIDA_PADRAO, docx_anterior=None, textos_extra=None, controle=None):
    """`textos_extra`: {bookmark_name: texto} que sobrepõe o `docx_anterior` (textos de um arquivo
    de update casados por incorpora_update_docx.py). `controle`: dict de controle_revisao.json."""
    estrutura = parse_estrutura_eixos()
    valida_estrutura(estrutura)

    textos_curados = {}
    if docx_anterior and Path(docx_anterior).exists():
        textos_curados = extrai_textos_por_bookmark(docx_anterior)
    textos_curados.update(textos_extra or {})
    controle = controle or {}
    # "ajustes_manuais" (correções feitas fora de um arquivo de update) vence o status calculado
    ctl_blocos = {**controle.get("blocos", {}), **controle.get("ajustes_manuais", {})}
    ctl_alertas = controle.get("alertas", {})
    ctl_novos = set(controle.get("novos_desde_ultima_rodada", []))
    ctl_notas = {}
    for n in controle.get("notas", []):
        ctl_notas.setdefault(n.get("bookmark"), []).append(n)
    ctl_realocar = {r["bookmark"]: r for r in controle.get("realocar", [])}
    rodada_rotulo = {r["id"]: (r["id"].replace("curadoria_textos_", "").replace("_", " ")
                               + (f" ({r['data']})" if r.get("data") else "")) for r in controle.get("rodadas", [])}
    linhas_controle = []   # (eixo, seção, item, status, rodada, observação)

    def status_de(bname):
        texto = textos_curados.get(bname)
        if not texto or _eh_lorem(texto):
            return "pendente"
        return ctl_blocos.get(bname, {}).get("status", "atualizado")

    def marca(status, bname=None):
        return f"  {STATUS_ICONE[status]}" + (f" {ICONE_ALERTA}" if bname and bname in ctl_alertas else "")

    def paragrafo_aviso(texto, cor, prefixo):
        p = doc.add_paragraph()
        r = p.add_run(f"{prefixo} {texto}")
        r.italic = True
        r.font.size = Pt(9)
        r.font.color.rgb = cor
        return p

    def avisos_do_bloco(bname):
        for a in ctl_alertas.get(bname, []):
            paragrafo_aviso(a, RGBColor(0xB0, 0x3A, 0x2E), ICONE_ALERTA)
        for n in ctl_notas.get(bname, []):
            origem = rodada_rotulo.get(Path(n["origem"]).stem, n["origem"])
            paragrafo_aviso(f"Nota do {origem}, em aberto: “{n['texto']}”", RGBColor(0x1F, 0x4E, 0x79), "📝")

    def registra_linha(eixo_nome, secao, item, bname):
        st = status_de(bname)
        info = ctl_blocos.get(bname, {})
        obs = []
        if bname in ctl_novos and st == "pendente":
            obs.append("item novo (não existia no último arquivo de update)")
        obs += ctl_alertas.get(bname, [])
        obs += [f"nota em aberto: {n['texto']}" for n in ctl_notas.get(bname, [])]
        rodada = rodada_rotulo.get(info.get("rodada"), "—") if st != "pendente" else "—"
        linhas_controle.append((eixo_nome, secao, item, st, rodada, "; ".join(obs)))

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
    # a tabela "Controle de revisão" é montada no fim (precisa de todos os blocos) e movida para cá
    ancora_controle = doc.add_paragraph()

    doc.add_heading("Introdução" + (marca(status_de("introducao"), "introducao") if controle else ""), level=1)
    # Bookmark fixo "introducao": texto curado sobrevive à regeneração e
    # sincroniza_docx.py o leva para HTML/PDF (textos_curados.json).
    p_intro = doc.add_paragraph(textos_curados.get("introducao") or _lorem("introducao-relatorio-docx", 250))
    add_bookmark(p_intro, "introducao", next_id())
    registro_bookmarks["introducao"] = "introducao"
    ids_gerados.add("introducao")
    registra_linha("—", "Introdução", "Introdução", "introducao")
    avisos_do_bloco("introducao")

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
        avisos_do_bloco(bname)
        return bname

    n_imagens = 0

    for eixo in estrutura:
        doc.add_heading(eixo["eixo"], level=1)
        for sub in eixo["subsecoes"]:
            titulo = sub["titulo"]
            campos = sub["campos"]

            if campos.get("status") == "pendente":
                doc.add_heading(titulo + (f"  {STATUS_ICONE['indicador']}" if controle else ""), level=2)
                p = doc.add_paragraph(f'[PENDENTE] {campos.get("nota", "")}')
                p.style = doc.styles["Intense Quote"]
                linhas_controle.append((eixo["eixo"], titulo, "—", "indicador", "—", campos.get("nota", "")))
                continue

            opcoes = [("visualização", nome) for nome in _arquivos_de(campos, "visualização")]
            opcoes += [("mapa", nome) for nome in _arquivos_de(campos, "mapa")]
            id_secao = f"{eixo['eixo']}::{titulo}"
            bname_secao = _bookmark_name(id_secao)

            # status agregado da subseção (marca no H2 => aparece no Sumário)
            bnames = [_bookmark_name(Path(n).stem) for _, n in opcoes] or [bname_secao]
            sts = [status_de(b) for b in bnames]
            if all(x == "revisado" for x in sts):
                st_secao = "revisado"
            elif all(x != "pendente" for x in sts):
                st_secao = "atualizado"
            elif any(x != "pendente" for x in sts):
                st_secao = "parcial"
            else:
                st_secao = "pendente"
            icone_secao = {"parcial": "◐"}.get(st_secao) or STATUS_ICONE[st_secao]
            texto_secao = textos_curados.get(bname_secao)
            tem_texto_secao = bool(opcoes) and bool(texto_secao) and not _eh_lorem(texto_secao)
            alerta_secao = any(b in ctl_alertas for b in bnames) or tem_texto_secao
            marca_h2 = (f"  {icone_secao}" + (f" {ICONE_ALERTA}" if alerta_secao else "")) if controle else ""
            doc.add_heading(titulo + marca_h2, level=2)

            if not opcoes:
                # fonte-only: sem visualização/mapa dedicado em analise.py.
                # Ainda assim ganha 1 bloco de texto curável (specs.md §7).
                bloco_texto(id_secao)
                registra_linha(eixo["eixo"], titulo, "(texto da subseção)", bname_secao)
                continue

            # Texto curado escrito para a subseção inteira (de quando ela não tinha imagem, ou de um
            # arquivo de update em que o texto estava direto sob o H2): fica aqui, sinalizado, em vez
            # de cair no apêndice de órfãos -- a pessoa decide se ele fica, sai ou muda de lugar.
            if tem_texto_secao:
                sugestao = ctl_realocar.get(bname_secao, {}).get(
                    "sugestao", "Conferir se ainda se aplica; se não, mover para a subseção certa ou apagar.")
                paragrafo_aviso("Texto escrito para esta subseção numa versão anterior (hoje ela mostra os "
                                "gráficos abaixo). " + sugestao, RGBColor(0xB0, 0x3A, 0x2E), ICONE_ALERTA)
                bloco_texto(id_secao)
                registra_linha(eixo["eixo"], titulo, "(texto da subseção, versão anterior)", bname_secao)

            for campo, nome in opcoes:
                id_ = Path(nome).stem
                label = id_.replace("_", " ").capitalize()
                b_item = _bookmark_name(id_)
                doc.add_heading(label + (marca(status_de(b_item), b_item) if controle else ""), level=3)
                registra_linha(eixo["eixo"], titulo, label, b_item)
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
    # só texto de verdade vai para o apêndice; lorem órfão (placeholder de item que saiu da estrutura) é descartado
    orfaos = {bname: texto for bname, texto in textos_curados.items()
              if bname not in ids_gerados and not _eh_lorem(texto)}
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

    if controle:
        _monta_controle(doc, ancora_controle, linhas_controle, rodada_rotulo)
    else:
        ancora_controle._p.getparent().remove(ancora_controle._p)

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

    import json
    args = sys.argv[1:]

    def _opcao(nome):
        if nome in args:
            i = args.index(nome)
            v = args[i + 1]
            del args[i:i + 2]
            return v
        return None

    caminho_textos = _opcao("--textos")
    caminho_controle = _opcao("--controle") or (CAMINHO_CONTROLE_PADRAO if Path(CAMINHO_CONTROLE_PADRAO).exists() else None)
    docx_anterior = args[0] if args else None
    textos_extra = None
    if caminho_textos:
        dados = json.loads(Path(caminho_textos).read_text(encoding="utf-8"))
        textos_extra = {bm: v["texto"] for bm, v in dados["textos"].items()}
    controle = json.loads(Path(caminho_controle).read_text(encoding="utf-8")) if caminho_controle else None
    resumo = gera_docx(docx_anterior=docx_anterior, textos_extra=textos_extra, controle=controle)

    print(f"Eixos: {resumo['eixos']}")
    print(f"Subseções: {resumo['subsecoes']}")
    print(f"Imagens embutidas: {resumo['imagens']}")
    print(f"Bookmarks: {resumo['bookmarks']} (órfãos: {resumo['orfaos']})")
    print(f"Gerado: {CAMINHO_SAIDA_PADRAO}")
