// sidebar.js -- sumário da aba ativa: subseção atual destacada e barra de progresso.
// specs/2026-09-24_website_refactor §4.7. Editado à mão (não gerado).
//
// Marcação (gerada): <aside class="outline"> (desktop) com um <nav class="outline-nav" data-panel="<id>"> por painel;
// cada <a href="#<painel>/<id-h3>" data-alvo="<id-h3>">. Escuta `tabchange` de navigation.js.
// Subseção ativa = último h3 cujo topo já passou da barra fixa (medido no scroll, com rAF --
// mais previsível que IntersectionObserver para seções de alturas muito diferentes).
//
// Mobile (specs/2026-09-28_website_mobile M2): as mesmas listas aparecem também em .outline-mobile (faixa
// "Nesta seção ▾" dentro da barra fixa, visível < 1100 px) e o progresso também vai para .nav-progress. Os dois
// conjuntos (desktop e mobile) são atualizados juntos; o CSS decide qual aparece.
(function(){
  "use strict";
  const outline = document.querySelector('.outline');
  const mobile = document.querySelector('.outline-mobile');
  if (!outline && !mobile) return;
  const navs = Array.from(document.querySelectorAll('.outline .outline-nav, .outline-mobile .outline-nav'));
  const barras = Array.from(document.querySelectorAll('.outline-progress span, .nav-progress span'));
  const pctEl = outline && outline.querySelector('.outline-pct');
  const botao = mobile && mobile.querySelector('.outline-mobile-btn');
  const lista = mobile && mobile.querySelector('.outline-mobile-lista');
  const atualEl = mobile && mobile.querySelector('.outline-mobile-atual');
  const reduzMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let painel = null, itens = [], agendado = false;

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
    barras.forEach(b => { b.style.width = (pct * 100).toFixed(1) + '%'; });
    if (pctEl) pctEl.textContent = Math.round(pct * 100) + '%';
    // subseção ativa: último h3 que já chegou ao terço superior da área visível (abaixo da barra);
    // no fim do painel, o último item (a subseção final pode ser curta demais para subir até lá)
    const linha = topoBarra + (window.innerHeight - topoBarra) * 0.3;
    let ativo = -1;
    const posicoes = itens.length ? itens[0].map(it => it.alvo.getBoundingClientRect().top) : [];
    posicoes.forEach((top, i)=>{ if (top <= linha) ativo = i; });
    if (pct >= 0.99 && posicoes.length) ativo = posicoes.length - 1;
    itens.forEach(grupo => grupo.forEach((it, i)=>{
      if (i === ativo) it.link.setAttribute('aria-current', 'true'); else it.link.removeAttribute('aria-current');
      it.link.classList.toggle('is-past', i < ativo);
    }));
    // faixa mobile: nome da subseção atual (antes da primeira, o título do painel)
    if (atualEl) {
      const h2 = painel.querySelector('h2');
      const texto = ativo >= 0 && itens[0] ? itens[0][ativo].link.textContent : (h2 ? h2.textContent : '');
      if (atualEl.textContent !== texto) atualEl.textContent = texto;
    }
  }
  function agenda(){ if (!agendado) { agendado = true; requestAnimationFrame(atualiza); } }

  // ---- faixa mobile: abrir/fechar ----
  function abre(aberta){
    if (!botao || !lista) return;
    botao.setAttribute('aria-expanded', aberta ? 'true' : 'false');
    lista.hidden = !aberta;
  }
  if (botao) {
    botao.addEventListener('click', ()=> abre(lista.hidden));
    // toque/clique fora fecha; Esc fecha e devolve o foco ao botão
    document.addEventListener('click', e=>{ if (!lista.hidden && !mobile.contains(e.target)) abre(false); });
    document.addEventListener('keydown', e=>{ if (e.key === 'Escape' && !lista.hidden) { abre(false); botao.focus(); } });
  }

  document.addEventListener('tabchange', e=>{
    painel = e.detail.panel;
    abre(false);
    // um grupo de itens por sumário (desktop e mobile), na mesma ordem
    const doPainel = navs.filter(n => n.dataset.panel === painel.id);
    navs.forEach(n => { n.hidden = !doPainel.includes(n); });
    // só subseções do painel entram no destaque por rolagem; links para outras abas
    // (Visão geral lista os eixos) apontam para painéis ocultos e não têm posição
    itens = doPainel.map(nav => Array.from(nav.querySelectorAll('a[data-alvo]'))
      .map(link => ({link: link, alvo: document.getElementById(link.dataset.alvo)}))
      .filter(it => it.alvo && painel.contains(it.alvo)));
    agenda();
  });

  document.addEventListener('click', e=>{
    const link = e.target.closest('.outline a[data-alvo], .outline-mobile a[data-alvo]');
    if (!link) return;
    const alvo = document.getElementById(link.dataset.alvo);
    if (!alvo) return;
    e.preventDefault();
    abre(false);
    // aba (Visão geral lista os eixos): delega a troca de aba para navigation.js
    if (alvo.classList.contains('tab-panel')) { if (window.navegacao) window.navegacao.ativa(alvo.id); return; }
    history.replaceState(null, '', link.getAttribute('href'));
    const y = alvo.getBoundingClientRect().top + window.scrollY - navH() - 20;
    window.scrollTo({top: Math.max(0, y), behavior: reduzMovimento ? 'auto' : 'smooth'});
  });

  window.addEventListener('scroll', agenda, {passive: true});
  window.addEventListener('resize', agenda);
})();
