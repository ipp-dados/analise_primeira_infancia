# -*- coding: utf-8 -*-
"""Sincroniza `relatorio/curadoria_textos.docx` já curado (texto real
escrito por um humano sobre o placeholder lorem ipsum) com o resto do
pipeline -- Bloco 7 de `specs/ajuste_eixos/plan.md`.

Lê os bookmarks do `.docx`, decide quais parágrafos foram genuinamente
editados (texto difere do lorem ipsum determinístico que `_lorem` geraria
hoje para aquele bloco) e propaga o texto editado para:

  (a) `relatorio/textos_curados.json` -- merge, nunca substitui o arquivo
      inteiro (`atualiza_textos_curados`);
  (b) `relatorio/index.html`, regenerado via subprocess
      (`build_html_report.py` lê o JSON no import, por isso subprocess, não
      import direto -- ver nota em `regenera_html`);
  (c) a HTML-fonte do PDF, regenerada via subprocess (`build_notebook_report.py`,
      mesma razão);
  (d) uma nota markdown nova/atualizada em `analise.py`, logo após a célula
      de código que produz o arquivo correspondente ao bloco -- a parte de
      maior risco desta tarefa, ver `sincroniza_nota_analise`.

Reaproveita de `gera_docx_curadoria.py` (mesma pasta, NÃO modificado por
este script): `extrai_textos_por_bookmark`, `_lorem`, `_bookmark_name` e
`_arquivos_de`. Reaproveita de `gera_estrutura_eixos.py`:
`parse_estrutura_eixos`.

## Por que não basta comparar `_lorem(nome_do_bookmark)` contra o texto

O nome do bookmark gravado no `.docx` é `_bookmark_name(id_)`
(`gera_docx_curadoria.py`), que SANITIZA `id_` (só `[A-Za-z0-9_]`, começa
com letra) e, quando o resultado passaria de 40 caracteres, TRUNCA para 32
e acrescenta um hash de 8 hex do `id_` ORIGINAL. Só quando `id_` já é um
identificador Python-like curto (a maioria dos nomes de arquivo deste
projeto) o nome do bookmark bate com `id_` byte a byte. Quando não bate
(confirmado empiricamente: 26 dos 84 bookmarks reais de
`relatorio/curadoria_textos.docx`, todos por causa só do truncamento -- nome
de arquivo comprido, não edição real), comparar `_lorem(nome_do_bookmark)`
direto contra o texto do parágrafo dá **falso positivo** (acha que foi
editado, e o pior: gravaria a chave errada no JSON -- HTML/PDF fazem
`_texto_analise(Path(arquivo).stem)`, ou seja, esperam o `id_` completo, não
a versão truncada+hash).

A correção: `_mapa_bookmark_para_id` reconstrói `{bookmark_name: id_
original}` reencenando a MESMA enumeração que `gera_docx_curadoria.gera_docx()`
faz sobre `parse_estrutura_eixos()` (sem escrever nenhum `.docx`) e aplicando
`_bookmark_name()` (a mesma função, importada, nunca reimplementada) a cada
candidato -- é determinística, então isso é reversão exata, não heurística.

CLI:
    python sincroniza_docx.py <caminho_docx> [<pdf_source_out>]

Sem o 2º argumento, a HTML-fonte do PDF é escrita num arquivo temporário
fora do repositório (este script não é responsável pelo passo final de
renderização do PDF via browser headless -- isso continua manual, ver
`SKILL.md`); passe um caminho explícito para inspecionar o resultado.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))  # same-folder imports, como os scripts irmãos
from gera_docx_curadoria import _arquivos_de, _bookmark_name, _lorem, extrai_textos_por_bookmark
from gera_estrutura_eixos import parse_estrutura_eixos

# scripts/ -> export_pdf_report/ -> skills/ -> .claude/ -> raiz do projeto
_RAIZ = Path(__file__).resolve().parents[4]

_CAMINHO_JSON_RELATIVO = "relatorio/textos_curados.json"
_CAMINHO_ANALISE_RELATIVO = "analise.py"

# Onde procurar o arquivo real correspondente a um `id_` (stem) -- na ordem
# em que `gera_docx_curadoria.py` também os associa (visualização, mapa,
# tabela); usado só para decidir se um `id_` tem "âncora de código" em
# analise.py (bloco fallback "{eixo}::{subseção}" não tem nenhum arquivo).
_DIRS_ARQUIVO = [("visualizacoes", ".png"), ("mapas", ".png"), ("tabelas_finais", ".csv")]


# --------------------------------------------------------- 1. detecção -----

def eh_lorem_ipsum(seed, texto):
    """True se `texto` e' exatamente o lorem ipsum determinístico que
    `_lorem(seed)` geraria hoje -- comparação exata (não heurística), já que
    `_lorem` é 100% determinístico por seed. `seed` aqui é sempre o `id_`
    ORIGINAL (não o nome sanitizado do bookmark) -- ver `_mapa_bookmark_para_id`."""
    if seed == "introducao":  # bookmark fixo, lorem de 250 palavras (gera_docx_curadoria.py)
        return texto == _lorem("introducao-relatorio-docx", 250)
    return texto == _lorem(seed)


def _ids_originais_conhecidos():
    """Enumera todo `id_` que `gera_docx_curadoria.gera_docx()` usaria como
    seed de bookmark/lorem hoje, reencenando sua própria lógica de
    enumeração sobre `parse_estrutura_eixos()` -- sem gerar nenhum `.docx`.
    Blocos `status: pendente` não entram (não geram bookmark no gerador:
    viram só um parágrafo `[PENDENTE]` sem `bloco_texto()`)."""
    estrutura = parse_estrutura_eixos()
    ids = {"introducao"}  # bookmark fixo da Introdução (fora da estrutura)
    for eixo in estrutura:
        for sub in eixo["subsecoes"]:
            campos = sub["campos"]
            if campos.get("status") == "pendente":
                continue
            nomes = _arquivos_de(campos, "visualização") + _arquivos_de(campos, "mapa")
            if not nomes:
                ids.add(f"{eixo['eixo']}::{sub['titulo']}")
            else:
                for nome in nomes:
                    ids.add(Path(nome).stem)
    return ids


def _mapa_bookmark_para_id():
    """{bookmark_name: id_original}, invertendo `_bookmark_name` por força
    bruta sobre todo `id_` conhecido hoje em `specs/estrutura_eixos.md`
    (determinístico, então isso é exato, não uma adivinhação). Um bookmark
    do `.docx` ausente deste mapa (estrutura mudou desde a geração do
    `.docx`, ou é um bookmark do apêndice "Textos órfãos") fica de fora --
    tratado à parte por `coleta_edicoes`."""
    return {_bookmark_name(id_): id_ for id_ in _ids_originais_conhecidos()}


def coleta_edicoes(caminho_docx):
    """Lê `caminho_docx` e devolve `(edicoes, avisos)`:
    - `edicoes`: {id_original: texto} só para blocos genuinamente editados
      (texto difere do lorem ipsum determinístico esperado).
    - `avisos`: lista de strings, 1 por bookmark do .docx que não bate com
      nenhum `id_` conhecido da estrutura atual (best-effort: tratado como
      se o próprio nome do bookmark já fosse o `id_`, o que só é correto
      quando esse nome não passou por truncamento -- ver docstring do
      módulo) -- nunca interrompe a sincronização, só reportado."""
    textos = extrai_textos_por_bookmark(caminho_docx)
    mapa = _mapa_bookmark_para_id()

    edicoes = {}
    avisos = []
    for bname, texto in textos.items():
        id_ = mapa.get(bname)
        if id_ is None:
            avisos.append(
                f"bookmark {bname!r} não corresponde a nenhum indicador de "
                "specs/estrutura_eixos.md hoje (estrutura mudou desde a "
                "geração deste .docx, ou é um bookmark do apêndice 'Textos "
                "órfãos'); tratando o próprio nome do bookmark como id_ "
                "(pode estar truncado/hasheado se o nome original passava "
                "de 40 caracteres -- resultado best-effort)."
            )
            id_ = bname
        if not eh_lorem_ipsum(id_, texto):
            edicoes[id_] = texto
    return edicoes, avisos


# ------------------------------------------------- 2. JSON compartilhado ---

def atualiza_textos_curados(edicoes, raiz=_RAIZ):
    """`edicoes`: {seed: texto}. Faz merge com o que já existe no JSON
    (nunca substitui o arquivo inteiro) -- um bookmark que não está
    presente nesta rodada de sincronização não deve perder uma curadoria já
    registrada anteriormente."""
    p = raiz / _CAMINHO_JSON_RELATIVO
    atual = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    atual.update(edicoes)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(atual, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return atual


# --------------------------------------------- 3. regeneração HTML / PDF ---

def regenera_html(raiz=_RAIZ):
    """Roda `build_html_report.py` como subprocess (não import direto -- o
    módulo carrega `_TEXTOS_CURADOS` uma vez, no import, então um import
    dentro do mesmo processo Python não veria o JSON recém-escrito).
    Invocação e cwd espelham exatamente `SKILL.md` ("rode a partir da raiz
    do projeto")."""
    destino = "relatorio/index.html"
    subprocess.run(
        [sys.executable, ".claude/skills/export_pdf_report/scripts/build_html_report.py", destino],
        cwd=str(raiz), check=True, capture_output=True, text=True,
    )
    return raiz / destino


def regenera_pdf_source(raiz=_RAIZ, destino_relativo=None):
    """Idem, para a HTML-fonte do PDF (`build_notebook_report.py`). Sem
    `destino_relativo`, escreve num arquivo temporário FORA do repositório
    -- este script não é responsável pelo passo de renderização para PDF
    via browser headless (isso continua manual, `SKILL.md`), só precisa
    confirmar que a fonte HTML do PDF também reflete o texto novo."""
    if destino_relativo is None:
        caminho_absoluto = Path(tempfile.gettempdir()) / "sincroniza_docx_pdf_source.html"
        subprocess.run(
            [sys.executable, str((raiz / ".claude/skills/export_pdf_report/scripts/build_notebook_report.py")),
             str(caminho_absoluto)],
            cwd=str(raiz), check=True, capture_output=True, text=True,
        )
        return caminho_absoluto
    subprocess.run(
        [sys.executable, ".claude/skills/export_pdf_report/scripts/build_notebook_report.py", destino_relativo],
        cwd=str(raiz), check=True, capture_output=True, text=True,
    )
    return raiz / destino_relativo


# ------------------------------------------- 4. nota markdown em analise.py -

def _arquivo_real_para_seed(seed, raiz=_RAIZ):
    """Path do arquivo real (visualizacoes/mapas/tabelas_finais) cujo stem
    é `seed`, ou None -- distingue um `id_` de arquivo real de um fallback
    '{eixo}::{subseção}' (sem código-âncora em analise.py, nada a fazer)."""
    for pasta, ext in _DIRS_ARQUIVO:
        candidato = raiz / pasta / f"{seed}{ext}"
        if candidato.exists():
            return candidato
    return None


def _tipo_marcador_celula(linha):
    """'codigo' | 'markdown' | None (linha não é um marcador `# %%` de jupytext
    py:percent -- só as duas formas exatas existem hoje em analise.py, sem
    metadata extra na linha)."""
    s = linha.rstrip("\n").rstrip("\r")
    if s == "# %%":
        return "codigo"
    if s == "# %% [markdown]":
        return "markdown"
    return None


def _formata_bloco_nota(seed, texto):
    """Uma célula markdown nova, no formato exato pedido:
        # %% [markdown]
        # <!-- nota-curadoria:SEED -->
        # **Nota de curadoria:** TEXTO
    seguida de uma linha em branco (mesma convenção de espaçamento entre
    células já usada em todo o arquivo). `texto` é colapsado numa única
    linha lógica (quebras de linha do parágrafo do .docx viram espaço) --
    jupytext py:percent não tem problema com uma linha de comentário longa,
    e evita ter que prefixar `# ` em múltiplas linhas."""
    texto_limpo = " ".join(texto.split())
    return (
        "# %% [markdown]\n"
        f"# <!-- nota-curadoria:{seed} -->\n"
        f"# **Nota de curadoria:** {texto_limpo}\n"
        "\n"
    )


def sincroniza_nota_analise(linhas, seed, texto):
    """Insere ou atualiza (in-place, em `linhas` -- list[str] com quebras de
    linha preservadas) a nota markdown de curadoria para `seed` em
    `analise.py`. Devolve True se algo mudou, False se `seed` não foi
    encontrado em nenhum lugar do arquivo (nunca levanta exceção por isso --
    o chamador decide como reportar). Levanta ValueError só no caso
    defensivo de uma estrutura de células inconsistente (marcador de
    curadoria encontrado fora de uma célula markdown), para nunca corromper
    o arquivo tentando adivinhar."""
    marcador = f"# <!-- nota-curadoria:{seed} -->"

    # 1) já existe uma nota para este seed? substitui só essa célula, in-place.
    for i, linha in enumerate(linhas):
        if linha.rstrip("\n").rstrip("\r") == marcador:
            j = i - 1
            while j >= 0 and _tipo_marcador_celula(linhas[j]) is None:
                j -= 1
            if j < 0 or _tipo_marcador_celula(linhas[j]) != "markdown":
                raise ValueError(
                    f"Marcador de curadoria de {seed!r} encontrado fora de uma "
                    "célula markdown esperada -- abortando para não corromper analise.py."
                )
            inicio = j
            k = i + 1
            while k < len(linhas) and _tipo_marcador_celula(linhas[k]) is None:
                k += 1
            fim = k
            linhas[inicio:fim] = _formata_bloco_nota(seed, texto).splitlines(keepends=True)
            return True

    # 2) não existe ainda -- localiza a célula de código que produz o arquivo `seed`.
    # `nome_arquivo=` nunca carrega a extensão em analise.py (a extensão é
    # acrescentada só na hora de salvar); to_csv/to_excel já carregam a
    # extensão literal no caminho. As duas convenções são tentadas em DUAS
    # FASES, não misturadas numa lista só: um mesmo stem costuma nomear TANTO
    # a tabela em tabelas_finais/ (`to_csv('tabelas_finais/{seed}.csv')`,
    # cell mais cedo no arquivo) QUANTO o gráfico em visualizacoes/
    # (`nome_arquivo='{seed}'`, cell separada, mais tarde) -- gera_docx_curadoria.py
    # só cria bookmark a partir de uma imagem (visualização/mapa), nunca de
    # uma tabela sozinha, então a célula de PLOTAGEM é sempre a âncora certa;
    # buscar as duas convenções misturadas na ordem em que aparecem no
    # arquivo pegaria a célula de exportação da tabela por engano sempre que
    # ela vier antes (caso comum, confirmado com 'nascidos_vivos_por_ano').
    fases = (
        [f"nome_arquivo='{seed}'", f'nome_arquivo="{seed}"'],
        [f"{seed}.png", f"{seed}.csv", f"{seed}.xlsx"],
    )
    idx_match = None
    for padroes in fases:
        for i, linha in enumerate(linhas):
            if any(p in linha for p in padroes):
                idx_match = i
                break
        if idx_match is not None:
            break
    if idx_match is None:
        return False

    inicio = idx_match
    while inicio >= 0 and _tipo_marcador_celula(linhas[inicio]) != "codigo":
        inicio -= 1
    if inicio < 0:
        raise ValueError(f"Não encontrei início de célula de código antes da ocorrência de {seed!r}.")

    fim = idx_match + 1
    while fim < len(linhas) and _tipo_marcador_celula(linhas[fim]) is None:
        fim += 1

    bloco = _formata_bloco_nota(seed, texto).splitlines(keepends=True)
    linhas[fim:fim] = bloco
    return True


def aplica_notas_em_analise(edicoes, raiz=_RAIZ):
    """`edicoes`: {seed: texto}. Aplica `sincroniza_nota_analise` para todo
    seed com arquivo real correspondente (`_arquivo_real_para_seed`);
    fallbacks '{eixo}::{subseção}' são pulados de propósito (sem
    código-âncora, nada a fazer em analise.py). Só grava o arquivo e roda
    `jupytext --sync` se algo de fato mudou. Devolve um dict-resumo."""
    caminho_analise = raiz / _CAMINHO_ANALISE_RELATIVO
    linhas = caminho_analise.read_text(encoding="utf-8").splitlines(keepends=True)

    atualizados, pulados_fallback, nao_encontrados = [], [], []
    mudou = False
    for seed, texto in edicoes.items():
        if "::" in seed and _arquivo_real_para_seed(seed, raiz=raiz) is None:
            pulados_fallback.append(seed)
            continue
        if _arquivo_real_para_seed(seed, raiz=raiz) is None:
            nao_encontrados.append(seed)
            continue
        try:
            if sincroniza_nota_analise(linhas, seed, texto):
                atualizados.append(seed)
                mudou = True
            else:
                nao_encontrados.append(seed)
        except ValueError as erro:
            nao_encontrados.append(f"{seed} (erro: {erro})")

    jupytext_ok = None
    if mudou:
        caminho_analise.write_text("".join(linhas), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, "-m", "jupytext", "--sync", str(caminho_analise)],
            cwd=str(raiz), capture_output=True, text=True,
        )
        jupytext_ok = {"returncode": r.returncode, "stdout": r.stdout, "stderr": r.stderr}

    return {
        "atualizados": atualizados,
        "pulados_fallback": pulados_fallback,
        "nao_encontrados": nao_encontrados,
        "jupytext": jupytext_ok,
    }


# ------------------------------------------------------------- orquestração -

def sincroniza(caminho_docx, raiz=_RAIZ, pdf_source_out=None, aplica_analise=True):
    edicoes, avisos = coleta_edicoes(caminho_docx)

    resultado = {
        "editados": sorted(edicoes),
        "avisos": avisos,
        "json_atualizado": False,
        "html_ok": False,
        "pdf_source_ok": False,
        "pdf_source_path": None,
        "analise": None,
    }
    if not edicoes:
        return resultado

    atualiza_textos_curados(edicoes, raiz=raiz)
    resultado["json_atualizado"] = True

    regenera_html(raiz=raiz)
    resultado["html_ok"] = True

    caminho_pdf_source = regenera_pdf_source(raiz=raiz, destino_relativo=pdf_source_out)
    resultado["pdf_source_ok"] = True
    resultado["pdf_source_path"] = str(caminho_pdf_source)

    if aplica_analise:
        resultado["analise"] = aplica_notas_em_analise(edicoes, raiz=raiz)

    return resultado


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    if len(sys.argv) < 2:
        print("uso: python sincroniza_docx.py <caminho_docx> [<pdf_source_out>]")
        raise SystemExit(1)

    caminho_docx_arg = sys.argv[1]
    pdf_source_out_arg = sys.argv[2] if len(sys.argv) > 2 else None

    res = sincroniza(caminho_docx_arg, pdf_source_out=pdf_source_out_arg)

    print(f"Blocos editados detectados: {len(res['editados'])}")
    for seed in res["editados"]:
        print(f"  - {seed}")
    for aviso in res["avisos"]:
        print(f"AVISO: {aviso}")

    if not res["editados"]:
        print("Nada a sincronizar (todo bookmark ainda é lorem ipsum).")
        raise SystemExit(0)

    print(f"JSON atualizado: {res['json_atualizado']} ({_CAMINHO_JSON_RELATIVO})")
    print(f"HTML regenerado: {res['html_ok']} (relatorio/index.html)")
    print(f"HTML-fonte do PDF regenerada: {res['pdf_source_ok']} -> {res['pdf_source_path']}")

    if res["analise"]:
        a = res["analise"]
        print(f"analise.py -- notas atualizadas: {a['atualizados']}")
        print(f"analise.py -- fallback sem âncora (esperado, pulado): {a['pulados_fallback']}")
        print(f"analise.py -- não encontrados (reportar): {a['nao_encontrados']}")
        if a["jupytext"]:
            print(f"jupytext --sync: returncode={a['jupytext']['returncode']}")
            print(a["jupytext"]["stdout"])
            if a["jupytext"]["stderr"]:
                print("stderr:", a["jupytext"]["stderr"])
