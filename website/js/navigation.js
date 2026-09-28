// navigation.js -- barra de abas fixa: troca de painel sem recarregar, estado na URL, teclado.
// specs/2026-09-24_website_refactor §4.3. Editado à mão (não gerado).
//
// URL (só hash -- o GitHub Pages não reescreve caminhos, spec §4.10):
//   (vazio)            -> primeira aba (Visão geral)
//   #<painel>          -> ativa a aba
//   #<painel>/<id-h3>  -> ativa a aba e rola até a subseção
//   #<qualquer-id>     -> link antigo (ex. um h3 do relatório de uma aba só): ativa a aba que contém o id
// Dispara `tabchange` (detail: {id, panel}) no document -- sidebar.js escuta.
(function(){
  "use strict";
  const bar = document.querySelector('.tabbar');
  const tabs = Array.from(document.querySelectorAll('.tabbar [role="tab"]'));
  if (!bar || !tabs.length) return;
  const panelOf = tab => document.getElementById(tab.getAttribute('aria-controls'));
  const reduzMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let ativo = null;

  function navH(){ return bar.getBoundingClientRect().height; }
  function atualizaNavH(){ document.documentElement.style.setProperty('--nav-h', Math.round(navH()) + 'px'); }

  // abas em telas estreitas (specs/2026-09-28_website_mobile M1): a fileira rola na horizontal; esmaecimento só do
  // lado em que ainda há abas (classes lidas por css/mobile.css) e aba ativa centralizada. Se as abas cabem (desktop),
  // nenhuma classe entra e nada rola.
  const fileira = bar.querySelector('.tabbar-inner');
  function atualizaBordas(){
    if (!fileira) return;
    const max = fileira.scrollWidth - fileira.clientWidth;
    fileira.classList.toggle('tem-mais-esq', max > 1 && fileira.scrollLeft > 1);
    fileira.classList.toggle('tem-mais-dir', max > 1 && fileira.scrollLeft < max - 1);
  }
  function centraAba(tab, suave){
    if (!fileira || fileira.scrollWidth <= fileira.clientWidth) return;
    const fr = fileira.getBoundingClientRect(), tr = tab.getBoundingClientRect();
    const esq = fileira.scrollLeft + (tr.left - fr.left) - (fr.width - tr.width) / 2;
    fileira.scrollTo({left: Math.max(0, esq), behavior: (suave && !reduzMovimento) ? 'smooth' : 'auto'});
  }
  if (fileira) {
    let agendado = false;
    fileira.addEventListener('scroll', ()=>{ if (!agendado) { agendado = true; requestAnimationFrame(()=>{ agendado = false; atualizaBordas(); }); } }, {passive: true});
  }

  function rolaPara(y){ window.scrollTo({top: Math.max(0, y), behavior: reduzMovimento ? 'auto' : 'smooth'}); }

  // Topo do painel logo abaixo da barra. Só sobe (se o leitor está no banner, não desce à força).
  function rolaTopoDoPainel(panel){
    const alvo = panel.getBoundingClientRect().top + window.scrollY - navH() - 24;
    if (window.scrollY > alvo) window.scrollTo({top: Math.max(0, alvo), behavior: 'auto'});
  }

  function rolaAte(el){
    rolaPara(el.getBoundingClientRect().top + window.scrollY - navH() - 20);
  }

  function ativa(tab, opts){
    opts = opts || {};
    tabs.forEach(t=>{
      const sel = t === tab;
      t.setAttribute('aria-selected', sel ? 'true' : 'false');
      t.tabIndex = sel ? 0 : -1;
      const p = panelOf(t);
      if (p) p.hidden = !sel;
    });
    const panel = panelOf(tab);
    const mudou = ativo !== tab;
    centraAba(tab, ativo !== null);
    ativo = tab;
    if (mudou) document.dispatchEvent(new CustomEvent('tabchange', {detail: {id: panel.id, panel: panel}}));
    if (opts.alvo) {
      // espera o layout do painel recém-mostrado antes de medir
      requestAnimationFrame(()=> rolaAte(opts.alvo));
    } else if (mudou && opts.rolar !== false) {
      rolaTopoDoPainel(panel);
    }
  }

  function tabDoPainel(panel){ return tabs.find(t => panelOf(t) === panel); }

  function rota(){
    const hash = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (!hash) { ativa(tabs[0], {rolar: false}); return; }
    const [painelId, subId] = hash.split('/');
    // id atual do painel, ou um id antigo listado em data-alias (ex. #prioridade-sem-secundário)
    const direto = tabs.find(t => t.getAttribute('aria-controls') === painelId) || tabs.find(t => {
      const p = panelOf(t);
      return p && (p.dataset.alias || '').split(' ').includes(painelId);
    });
    if (direto) {
      ativa(direto, {alvo: subId ? document.getElementById(subId) : null});
      return;
    }
    // link antigo: id de um elemento dentro de algum painel
    const el = document.getElementById(hash);
    const panel = el && el.closest('.tab-panel');
    const tab = panel && tabDoPainel(panel);
    if (tab) { ativa(tab, {alvo: el}); return; }
    ativa(tabs[0], {rolar: false});
  }

  tabs.forEach((tab, i)=>{
    tab.addEventListener('click', ()=>{
      const id = tab.getAttribute('aria-controls');
      if (location.hash !== '#' + id) history.pushState(null, '', '#' + id);
      ativa(tab);
    });
    tab.addEventListener('keydown', e=>{
      let j = null;
      if (e.key === 'ArrowRight') j = (i + 1) % tabs.length;
      else if (e.key === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') j = 0;
      else if (e.key === 'End') j = tabs.length - 1;
      if (j === null) return;
      e.preventDefault();
      tabs[j].focus();
      tabs[j].click();
    });
  });

  // voltar/avançar e links internos (#painel, #painel/h3) -- os dois eventos, rota() é idempotente
  window.addEventListener('popstate', rota);
  window.addEventListener('hashchange', rota);

  // sombra na barra quando ela gruda no topo
  const sentinela = document.createElement('div');
  sentinela.setAttribute('aria-hidden', 'true');
  bar.parentNode.insertBefore(sentinela, bar);
  new IntersectionObserver(([e])=> bar.classList.toggle('is-stuck', !e.isIntersecting)).observe(sentinela);

  window.addEventListener('resize', ()=>{ atualizaNavH(); atualizaBordas(); if (ativo) centraAba(ativo, false); });
  document.addEventListener('DOMContentLoaded', ()=>{ atualizaNavH(); rota(); atualizaBordas(); });
  // fontes da web mudam a largura das abas depois do DOMContentLoaded
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(()=>{ atualizaNavH(); atualizaBordas(); if (ativo) centraAba(ativo, false); });
  window.navegacao = {ativa: id => { const t = tabs.find(x => x.getAttribute('aria-controls') === id); if (t) t.click(); }, rolaAte: rolaAte};
})();
