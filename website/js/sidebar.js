// sidebar.js -- sumário lateral da aba ativa: subseção atual destacada e barra de progresso.
// specs/website_refactor §4.7. Editado à mão (não gerado).
//
// Marcação (gerada): <aside class="outline"> com um <nav class="outline-nav" data-panel="<id>">
// por painel; cada <a href="#<painel>/<id-h3>" data-alvo="<id-h3>">. Escuta `tabchange` de navigation.js.
// Subseção ativa = último h3 cujo topo já passou da barra fixa (medido no scroll, com rAF --
// mais previsível que IntersectionObserver para seções de alturas muito diferentes).
(function(){
  "use strict";
  const outline = document.querySelector('.outline');
  if (!outline) return;
  const navs = Array.from(outline.querySelectorAll('.outline-nav'));
  const barra = outline.querySelector('.outline-progress span');
  const pctEl = outline.querySelector('.outline-pct');
  const reduzMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let painel = null, nav = null, itens = [], agendado = false;

  function navH(){
    const v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h'));
    return isNaN(v) ? 64 : v;
  }

  function atualiza(){
    agendado = false;
    if (!painel) return;
    const topoBarra = navH();
    // progresso: 0% com o topo do painel sob a barra, 100% com o fim do painel no pé da tela
    const r = painel.getBoundingClientRect();
    const inicio = r.top - topoBarra - 24, fim = r.bottom - window.innerHeight;
    let pct = fim - inicio <= 0 ? 1 : (0 - inicio) / (fim - inicio);
    pct = Math.max(0, Math.min(1, pct));
    if (barra) barra.style.width = (pct * 100).toFixed(1) + '%';
    if (pctEl) pctEl.textContent = Math.round(pct * 100) + '%';
    // subseção ativa
    let ativo = -1;
    itens.forEach((it, i)=>{ if (it.alvo.getBoundingClientRect().top - topoBarra - 90 <= 0) ativo = i; });
    if (pct >= 0.999 && itens.length) ativo = itens.length - 1;
    itens.forEach((it, i)=>{
      if (i === ativo) it.link.setAttribute('aria-current', 'true'); else it.link.removeAttribute('aria-current');
      it.link.classList.toggle('is-past', i < ativo);
    });
  }
  function agenda(){ if (!agendado) { agendado = true; requestAnimationFrame(atualiza); } }

  document.addEventListener('tabchange', e=>{
    painel = e.detail.panel;
    nav = navs.find(n => n.dataset.panel === painel.id) || null;
    navs.forEach(n => { n.hidden = n !== nav; });
    // só subseções do painel entram no destaque por rolagem; links para outras abas
    // (Visão geral lista os eixos) apontam para painéis ocultos e não têm posição
    itens = nav ? Array.from(nav.querySelectorAll('a[data-alvo]'))
      .map(link => ({link: link, alvo: document.getElementById(link.dataset.alvo)}))
      .filter(it => it.alvo && painel.contains(it.alvo)) : [];
    agenda();
  });

  outline.addEventListener('click', e=>{
    const link = e.target.closest('a[data-alvo]');
    if (!link) return;
    const alvo = document.getElementById(link.dataset.alvo);
    if (!alvo) return;
    e.preventDefault();
    // aba (Visão geral lista os eixos): delega a troca de aba para navigation.js
    if (alvo.classList.contains('tab-panel')) { if (window.navegacao) window.navegacao.ativa(alvo.id); return; }
    history.replaceState(null, '', link.getAttribute('href'));
    const y = alvo.getBoundingClientRect().top + window.scrollY - navH() - 20;
    window.scrollTo({top: Math.max(0, y), behavior: reduzMovimento ? 'auto' : 'smooth'});
  });

  window.addEventListener('scroll', agenda, {passive: true});
  window.addEventListener('resize', agenda);
})();
