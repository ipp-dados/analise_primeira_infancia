# -*- coding: utf-8 -*-
"""Tabela de conferência: texto da curadoria (DOCX / textos_curados.json) x figura publicada no site.

specs/2026-09-28_website_bugfix. Abre website/index.html num Chromium (Playwright, só ambiente de
desenvolvimento -- não está no requirements.txt), percorre cada bloco de texto com `data-seed`
(emitido por build_site.py) e registra a figura que aparece junto dele (aba, seção, modo Taxa|Óbitos,
pill, tipo, título renderizado). Cruza com o texto do DOCX de curadoria (mesma leitura de
sincroniza_docx.coleta_edicoes) e com relatorio/textos_curados.json.

    python website/build/confere_textos.py [saida.csv]

Saída: CSV `;` UTF-8 com BOM (abre direto no Excel pt-BR). Padrão:
specs/2026-09-28_website_bugfix/conferencia_textos_site.csv
"""
import csv
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "export_pdf_report" / "scripts"))

SAIDA = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "specs" / "2026-09-28_website_bugfix" / "conferencia_textos_site.csv"

# lê, para cada bloco de texto, a figura que o acompanha -- o texto de índice i de um option-card é o da pill i
_JS = r"""
() => {
  const txt = e => e ? e.textContent.replace(/\s+/g, ' ').trim() : '';
  const heads = Array.from(document.querySelectorAll('.tab-panel h2, .tab-panel h3, .tab-panel h4'));
  const antes = (el, tag) => { let r = null; for (const h of heads) { if (h.tagName === tag && (h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)) r = h; } return r; };
  const titulos = pane => {
    if (!pane) return '';
    const t = Array.from(pane.querySelectorAll('.map-title, .chart-subtitle, .sm-unidade, .bar-unidade, .axis-title'))
      .filter(e => !e.closest('[hidden]') || e.closest('.outlier-pane'))   // outliers: as duas variantes têm o mesmo título
      .map(txt).filter(Boolean);
    return Array.from(new Set(t)).join(' | ');
  };
  const tipo = pane => !pane ? '' : pane.querySelector('.map-svg') ? 'mapa' : pane.querySelector('table.plain') ? 'tabela'
                    : pane.querySelector('.sm-grid') ? 'gráfico (pequenos múltiplos)' : pane.querySelector('.bar-chart') ? 'gráfico de barras' : 'gráfico';
  return Array.from(document.querySelectorAll('.opt-text[data-seed]')).map(t => {
    const painel = t.closest('.tab-panel');
    const card = t.closest('.option-card, .table-with-text');
    let pane = null, pill = '', modo = '';
    if (card.classList.contains('option-card')) {
      const textos = Array.from(card.querySelectorAll(':scope > .opt-texts > .opt-text'));
      const i = textos.indexOf(t);
      const panes = Array.from(card.querySelectorAll(':scope > .opt-panes > .opt-pane'));
      pane = panes.length ? panes[i] : card.querySelector(':scope > .opt-panes');
      const pills = card.querySelectorAll(':scope > .pill-col > .pill');
      pill = pills.length ? txt(pills[i]) : '';
      const m = card.closest('.alterna-modo');
      if (m) { const box = m.parentElement; const j = Array.from(box.querySelectorAll(':scope > .alterna-modo')).indexOf(m);
               modo = txt(box.querySelectorAll(':scope > .alterna-ctrl > .alterna-btn')[j]); }
    } else pane = card.querySelector(':scope > .opt-panes');
    const tab = document.querySelector('.tab[aria-controls="' + painel.id + '"]');
    return {eixo: txt(tab), secao: txt(antes(t, 'H3')), subsecao: (() => { const h4 = antes(t, 'H4'), h3 = antes(t, 'H3');
              return h4 && h3 && (h3.compareDocumentPosition(h4) & Node.DOCUMENT_POSITION_FOLLOWING) ? txt(h4) : ''; })(),
            modo, pill, tipo: tipo(pane), titulo: titulos(pane), seed: t.dataset.seed, texto: (() => { const d = document.createElement('div');
              d.innerHTML = t.innerHTML.replace(/<br\s*\/?>/gi, '\n'); return d.textContent.replace(/\n{2,}/g, '\n\n').trim(); })()};
  });
}
"""


def _norm(s):
    return re.sub(r"\s+", " ", html.unescape(s or "")).strip()


def extrai_site():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1400, "height": 900})
        pg.goto((ROOT / "website" / "index.html").as_uri())
        pg.wait_for_timeout(800)
        linhas = pg.evaluate(_JS)
        b.close()
    return linhas


def main():
    from sincroniza_docx import coleta_edicoes   # noqa: E402 (caminho acrescentado acima)
    from gera_docx_curadoria import _LOREM_WORDS
    # vocabulário do lorem do site (build_site.py executa tudo no import, por isso lido via ast) + o do DOCX
    import ast
    arvore = ast.parse((ROOT / "website" / "build" / "build_site.py").read_text(encoding="utf-8"))
    no = next(n for n in arvore.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "_LOREM_WORDS")
    vocab = set(_LOREM_WORDS) | set(ast.literal_eval(no.value.func.value).split())   # _LOREM_WORDS = ("...").split()
    eh_lorem = lambda t: bool(t.strip()) and all(w in vocab for w in re.findall(r"[a-zà-ú]+", t.lower()))
    docx, _avisos = coleta_edicoes(ROOT / "relatorio" / "curadoria_textos.docx")
    curados = json.loads((ROOT / "relatorio" / "textos_curados.json").read_text(encoding="utf-8"))
    site = extrai_site()

    usados = set()
    saida = []
    for r in site:
        chaves = r["seed"].split("+")
        usados.update(chaves)
        t_docx = "\n\n".join(docx[k] for k in chaves if k in docx)
        t_json = "\n\n".join(curados[k] for k in chaves if curados.get(k))
        t_site = r["texto"]
        lorem = eh_lorem(t_site)
        if lorem and t_docx:
            status, obs = "ERRO", "texto curado no DOCX não chegou ao site (rodar sincroniza_docx.py)"
        elif lorem:
            status, obs = "PENDENTE", "sem texto na curadoria -- site mostra lorem ipsum"
        elif _norm(t_site) != _norm(t_json):
            status, obs = "ERRO", "texto do site difere de textos_curados.json"
        elif t_docx and _norm(t_docx) != _norm(t_json):
            status, obs = "ATENÇÃO", "DOCX difere do JSON (DOCX editado depois da última sincronização?)"
        else:
            status, obs = "OK", ""
        saida.append({**r, "texto_docx": t_docx, "texto_json": t_json, "texto_site": t_site, "status": status, "observacao": obs,
                      "origem_texto_site": "lorem ipsum" if lorem else "curadoria"})

    # textos curados que não aparecem em nenhum bloco do site, com o motivo conhecido
    motivo = {
        "cobertura_vacinal_epi_comparativo_anos": "figura excluída do site (specs/exclusoes.md, E7)",
        "mapa_obitos_gravidez_bairro_2025": "mapa excluído (specs/exclusoes.md, E4: 0 a 3 óbitos por bairro)",
        "mapa_obitos_puerperio_bairro_2025": "mapa excluído (specs/exclusoes.md, E4: 0 a 3 óbitos por bairro)",
        "obitos_evitaveis_total_cap_ano": "figura nunca publicada no site (o site mostra CAP por faixa etária); "
                                          "está em specs/estrutura_eixos.md -- decidir se entra",
    }
    for k in ("obitos_causas_evitaveis_raca_ano", "obitos_causas_evitaveis_raca_sem_nao_informado_ano",
              "percentual_mortalidade_causas_evitaveis_raca_ano", "percentual_mortalidade_causas_evitaveis_raca_sem_nao_informado_ano"):
        motivo[k] = "gráficos de causas evitáveis por raça/cor removidos em 2026-09-25 (specs/2026-09-25_relatorio_latex D6; estrutura_eixos: pendente)"
    blocos_relatorio = ("introducao", "consideracoes_finais", "resumo")
    for k in sorted(set(curados) | set(docx)):
        if k in usados or k.startswith(("achados_", "sintese_", "conclusao-")) or k in blocos_relatorio:
            continue
        saida.append({"eixo": "", "secao": "", "subsecao": "", "modo": "", "pill": "", "tipo": "", "titulo": "", "seed": k,
                      "texto_docx": docx.get(k, ""), "texto_json": curados.get(k, ""), "texto_site": "",
                      "origem_texto_site": "", "status": "NÃO PUBLICADO",
                      "observacao": motivo.get(k, "texto curado sem figura no site -- investigar")})

    colunas = [("eixo", "Eixo (aba)"), ("secao", "Seção"), ("subsecao", "Subseção"), ("modo", "Modo (Taxa|Óbitos)"),
               ("pill", "Opção (pill)"), ("tipo", "Tipo de figura"), ("titulo", "Título/unidade da figura no site"),
               ("seed", "Chave do texto (arquivo)"), ("status", "Status"), ("observacao", "Observação"),
               ("origem_texto_site", "Origem do texto no site"), ("texto_docx", "Texto na curadoria (DOCX)"),
               ("texto_json", "Texto em textos_curados.json"), ("texto_site", "Texto exibido no site")]
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow([c[1] for c in colunas])
        for r in saida:
            w.writerow([r.get(c[0], "") for c in colunas])
    from collections import Counter
    print(f"{SAIDA}: {len(saida)} linhas", dict(Counter(r['status'] for r in saida)))


if __name__ == "__main__":
    main()
