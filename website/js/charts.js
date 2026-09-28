// charts.js -- motor de graficos, pills, outliers, CSV e tooltips de mapa.
// specs/2026-09-24_website_refactor Bloco 2: extraido da string ENGINE de build_site.py; editado a mao a partir daqui.
(function(){
  "use strict";
  function fmt(n, d){ d = d||0; return Number(n).toLocaleString('pt-BR', {minimumFractionDigits:d, maximumFractionDigits:d}); }
  function pct(n, d){ return fmt(n, d==null?1:d) + '%'; }
  // taxas por mil (mortalidade por mil nascidos vivos, notificações por mil crianças) -- nunca com '%'
  function pm(n, d){ return fmt(n, d==null?1:d) + '‰'; }
  const CAT = ['var(--c1)','var(--c2)','var(--c3)','var(--c4)','var(--c5)','var(--c6)','var(--c7)','var(--c8)','var(--c9)','var(--c10)','var(--c11)'];
  const NS = 'http://www.w3.org/2000/svg';
  function svgEl(tag, attrs, parent){
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  let uid = 0;
  function byId(id){ return document.getElementById(id); }

  // limiar acima do qual so as series mais relevantes (top N pelo ultimo valor
  // nao-nulo) ficam coloridas/na legenda; o resto vira uma linha cinza fina,
  // agrupada numa unica entrada "Outras (N)" -- mesma regra de
  // serie_temporal_multipla em analise.py (ver specs/2026-09-09_visual-identity).
  const LIMIAR_DESTAQUE = 6, N_DESTACADAS = 4;

  // cor padrão pulando as cores fixas já usadas no mesmo gráfico (_COR_ENTIDADE): antes "Total" (1ª, --c1) e
  // "Meninos" (fixa --c1) saíam com a mesma cor (specs/2026-09-28_website_bugfix)
  function coresPadrao(series){
    const usadas = new Set(series.filter(s=>s.color).map(s=>s.color));
    const livres = CAT.filter(c=>!usadas.has(c));
    let k = 0;
    series.forEach(s=>{ if (!s.color) s.color = livres.length ? livres[k++ % livres.length] : CAT[k++ % CAT.length]; });
  }

  function prepararSeries(series){
    if (series.length===1 && !series[0].color) series[0].color = 'var(--accent)';
    coresPadrao(series);
    // painel de pequenos múltiplos: as séries de contexto chegam marcadas (muted) e ficam cinza
    if (series.some(s=>s.muted)) return { destacadas: series.filter(s=>!s.muted), apagadas: series.filter(s=>s.muted) };
    if (series.length <= LIMIAR_DESTAQUE) return { destacadas: series, apagadas: [] };
    const comFinal = series.map(s=>{
      let v = null;
      for (let i=s.values.length-1; i>=0; i--){ if (s.values[i] != null){ v = s.values[i]; break; } }
      return { s, v: v==null ? -Infinity : v };
    });
    comFinal.sort((a,b)=>b.v-a.v);
    return {
      destacadas: comFinal.slice(0, N_DESTACADAS).map(o=>o.s),
      apagadas: comFinal.slice(N_DESTACADAS).map(o=>o.s),
    };
  }

  // ================= line chart =================
  // escala com marcas redondas (1, 2, 2,5, 5 x 10^n): [min, max, nº de intervalos] -- antes o eixo era dividido
  // em 4 partes iguais do intervalo de dados e mostrava marcas como 29, 57, 86, 114
  function escalaRedonda(lo, hi, alvo){
    const bruto = ((hi - lo) || Math.abs(hi) || 1) / alvo;
    const pot = Math.pow(10, Math.floor(Math.log10(bruto)));
    const passo = [1, 2, 2.5, 5, 10].map(m=>m*pot).find(p=>p >= bruto);
    const a = Math.floor(lo / passo + 1e-9) * passo, b = Math.ceil(hi / passo - 1e-9) * passo;
    return [a, b === a ? a + passo : b, Math.max(1, Math.round(((b === a ? a + passo : b) - a) / passo))];
  }

  // título curto da unidade, na horizontal acima do eixo y (B1, mesma regra do PDF)
  function tituloEixo(svg, texto, x, y){
    if (!texto) return;
    svgEl('text', {x:x, y:y, class:'axis-title', 'text-anchor':'start'}, svg).textContent = texto;
  }

  // ctx: null = desenho de desktop (viewBox fixo, escala com o cartão -- inalterado); {mob:true, w} = "largura real"
  // (specs/2026-09-28_website_mobile M3): viewBox = largura do contêiner em px, então 1 unidade = 1 px e as fontes do
  // CSS (.chart-svg--real) saem no tamanho escrito; menos rótulos e paddings medidos pelo texto
  function desenhaLinha(container, cfg, ctx){
    const x = cfg.x, series = cfg.series, opts = cfg.opts || {};
    const mob = !!(ctx && ctx.mob);
    // B4 (specs/2026-09-25_website_graficos, P2): 7 ou mais séries -> pequenos múltiplos, com a visão de linhas ao lado
    if (!opts.painel && opts.multiplos !== false && series.length >= LIMIAR_DESTAQUE + 1) return pequenosMultiplos(container, cfg, ctx);
    const { destacadas, apagadas } = prepararSeries(series);
    const W = mob ? Math.round(Math.max(ctx.w, opts.painel ? 180 : 260)) : (opts.width || 680);
    const H = mob ? Math.round(Math.max(opts.painel ? 140 : 190, Math.min(opts.height || 250, W * (opts.painel ? 0.62 : 0.75)))) : (opts.height || 250);
    let padL = opts.padL != null ? opts.padL : 38;
    let padR = opts.padR != null ? opts.padR : (opts.endLabels === false ? 14 : 66);
    const padT = opts.yLabel ? (mob ? 34 : 30) : 16, padB = mob ? 30 : 28;
    let plotW = W - padL - padR; const plotH = H - padT - padB;
    const allVals = [];
    series.forEach(s=>s.values.forEach(v=>{ if (v!=null) allVals.push(v); }));
    // linhas de referencia opcionais (populacao-referencia D8, metas do PNE): entram na escala
    const refLines = opts.refLines || [];
    refLines.forEach(r=>allVals.push(r.value));
    let vMin = Math.min.apply(null, allVals), vMax = Math.max.apply(null, allVals);
    if (opts.yMax != null) vMax = opts.yMax;
    // B8 (P1): base zero em toda série, taxas inclusive (regra do PDF) -- zeroBase:false só para dados com negativos
    if (opts.zeroBase !== false) vMin = Math.min(0, vMin);
    const span = (vMax - vMin) || 1;
    vMax += span * 0.06;   // folga para o rótulo do máximo
    if (opts.zeroBase === false) vMin -= span * 0.06;
    const esc = escalaRedonda(vMin, vMax, opts.painel ? 2 : (mob ? 3 : 4));
    vMin = esc[0]; vMax = esc[1];
    const gridN = esc[2];
    const n = x.length;
    const xAt = i => padL + (n===1 ? plotW/2 : (plotW * i/(n-1)));
    const yAt = v => padT + plotH - ((v - vMin)/((vMax-vMin)||1))*plotH;
    const passoY = (vMax - vMin) / gridN;
    const decY = opts.yDecimals != null ? opts.yDecimals : (Number.isInteger(Math.round(passoY*1e6)/1e6) ? 0 : 1);
    const fmtY = v => cfg.yFormat ? cfg.yFormat(v) : fmt(v, decY);
    if (mob){
      // largura estimada do texto mono: .axis-label 11,5 px (~6,9 px/caractere), .end-label 13 px (~7,9)
      const rotY = []; for (let i=0;i<=gridN;i++) rotY.push(fmtY(vMin + (vMax-vMin)*i/gridN));
      if (opts.padL == null) padL = Math.max(26, Math.ceil(Math.max.apply(null, rotY.map(t=>String(t).length * 6.9))) + 9);
      const rotuloFinal = s=>{ const v = s.values[s.values.length-1]; return v==null ? '' : String(s.format ? s.format(v) : fmtY(v)); };
      if (opts.padR == null && opts.endLabels !== false){
        const alvo = opts.painel ? destacadas : (destacadas.length <= (opts.maxDirectLabels || 4) ? destacadas : []);
        padR = Math.ceil(Math.max.apply(null, alvo.map(s=>rotuloFinal(s).length * 7.9).concat([0]))) + 14;
      }
      plotW = W - padL - padR;
    }

    const wrap = document.createElement('div'); wrap.className = 'chart-wrap';
    if (series.length > 1 && !opts.painel){
      const legend = document.createElement('div'); legend.className = 'chart-legend';
      destacadas.forEach(s=>{
        const item = document.createElement('span'); item.className = 'legend-item';
        item.innerHTML = '<i style="background:'+s.color+'"></i>' + s.label;
        legend.appendChild(item);
      });
      if (apagadas.length){
        const item = document.createElement('span'); item.className = 'legend-item';
        item.innerHTML = '<i style="background:var(--c-muted)"></i>Outras ('+apagadas.length+')';
        legend.appendChild(item);
      }
      wrap.appendChild(legend);
    }
    const svg = svgEl('svg', {viewBox:'0 0 '+W+' '+H, class:'chart-svg' + (mob ? ' chart-svg--real' : ''), preserveAspectRatio:'xMidYMid meet'});
    tituloEixo(svg, opts.yLabel, 0, mob ? 13 : 12);
    for (let i=0;i<=gridN;i++){
      const v = vMin + (vMax-vMin)*i/gridN;
      const y = yAt(v);
      svgEl('line', {x1:padL, x2:W-padR, y1:y, y2:y, class:'grid-line'}, svg);
      svgEl('text', {x:padL-7, y:y+(mob ? 4 : 3.5), class:'axis-label', 'text-anchor':'end'}, svg).textContent = fmtY(v);
    }
    const maxLabels = mob ? Math.min(opts.maxXLabels || 7, opts.painel ? 3 : (W < 420 ? 4 : 5)) : (opts.maxXLabels || 7);
    const step = Math.max(1, Math.ceil(n/maxLabels));
    x.forEach((lab,i)=>{
      // o último ano sempre aparece; o rótulo regular colado a ele sai (antes "2024" e "2025" se sobrepunham).
      // A distância é medida em unidades do viewBox, não em nº de pontos: com 3 anos (Censos 2000/2010/2022) a regra
      // antiga "< 2 pontos" apagava 2010 (specs/2026-09-28_website_bugfix)
      if (i !== n-1 && (i % step !== 0 || (xAt(n-1) - xAt(i)) < 44)) return;
      svgEl('text', {x:xAt(i), y:H-7, class:'axis-label', 'text-anchor': i===0?'start':(i===n-1?'end':'middle')}, svg).textContent = lab;
    });
    refLines.forEach(r=>{
      const y = yAt(r.value);
      svgEl('line', {x1:padL, x2:W-padR, y1:y, y2:y, stroke:'var(--c-muted)', 'stroke-width':1.1, 'stroke-dasharray':'5 4'}, svg);
      svgEl('text', {x:W-padR, y:y-4, class:'axis-label', 'text-anchor':'end', 'font-style':'italic'}, svg).textContent = r.label;
    });

    function desenhaSerie(s, apagada){
      const pts = s.values.map((v,i)=> v==null ? null : [xAt(i), yAt(v)]);
      let d = '';
      pts.forEach(p=>{ if (p) d += (d===''?'M':'L') + p[0].toFixed(2) + ',' + p[1].toFixed(2) + ' '; });
      const validPts = pts.filter(Boolean);
      const cor = apagada ? 'var(--c-muted)' : s.color;
      if (!apagada && series.length === 1 && opts.area !== false && validPts.length){
        uid++;
        const gid = 'g'+uid;
        const grad = svgEl('linearGradient', {id:gid, x1:0, y1:0, x2:0, y2:1}, svg);
        svgEl('stop', {offset:'0%', 'stop-color':cor, 'stop-opacity':.18}, grad);
        svgEl('stop', {offset:'100%', 'stop-color':cor, 'stop-opacity':0}, grad);
        const base = yAt(vMin);
        const area = d + 'L'+validPts[validPts.length-1][0].toFixed(2)+','+base.toFixed(2)+' L'+validPts[0][0].toFixed(2)+','+base.toFixed(2)+' Z';
        svgEl('path', {d:area, fill:'url(#'+gid+')', stroke:'none'}, svg);
      }
      svgEl('path', {d:d, fill:'none', stroke:cor, 'stroke-width':apagada?1.1:2, 'stroke-opacity':apagada?.55:1, 'stroke-linecap':'round', 'stroke-linejoin':'round'}, svg);
      const last = validPts[validPts.length-1];
      let lastValidIdx = -1;
      for (let i=s.values.length-1;i>=0;i--){ if (s.values[i]!=null){ lastValidIdx=i; break; } }
      if (last && !apagada && opts.endLabels !== false){
        svgEl('circle', {cx:last[0], cy:last[1], r:3.2, fill:cor}, svg);
        // B3: rótulo direto só até 4 séries destacadas (skill dataviz: "<= 4 direct-labeled"); acima, legenda + tooltip
        if (destacadas.length <= (opts.maxDirectLabels || 4)){
          const t = svgEl('text', {x:last[0]+7, y:last[1], class:'end-label', fill:cor}, svg);
          t.textContent = s.format ? s.format(s.values[s.values.length-1]) : fmtY(s.values[s.values.length-1]);
          finais.push({t: t, y: last[1]});
        }
      }
      // maximo/minimo fixos, sempre visiveis sem hover (specification.md §3.9) --
      // pula o ponto ja coberto pelo end-label "mais recente" (idx===lastValidIdx) e o
      // primeiro ponto (idx===0, ja visivel por ser onde a linha comeca) -- em series
      // com poucos pontos isso evita rotulo redundante colado no eixo Y. Limiar mais
      // baixo que o end-label (maxExtremeSeries, nao maxDirectLabels): com muitas series
      // no mesmo grafico, maximos/minimos caem em posicoes X arbitrarias e colidem com
      // mais facilidade do que o end-label (que fica sempre no mesmo X, a ultima coluna).
      if (!apagada && opts.extremeLabels !== false && !(mob && W < 400) && destacadas.length <= (opts.maxExtremeSeries || 2)){
        let iMax=-1, iMin=-1, vMax=-Infinity, vMin=Infinity;
        s.values.forEach((v,i)=>{ if (v!=null){ if (v>vMax){vMax=v;iMax=i;} if (v<vMin){vMin=v;iMin=i;} } });
        [[iMax,-8],[iMin,13]].forEach(([idx,dy])=>{
          if (idx<0 || idx===lastValidIdx || idx===0) return;
          const p = pts[idx]; if (!p) return;
          svgEl('circle', {cx:p[0], cy:p[1], r:2.6, fill:cor}, svg);
          const t = svgEl('text', {x:p[0], y:p[1]+dy, class:'extreme-label', fill:cor, 'text-anchor':'middle'}, svg);
          t.textContent = s.format ? s.format(s.values[idx]) : fmtY(s.values[idx]);
        });
      }
    }
    const finais = [];
    apagadas.forEach(s=>desenhaSerie(s, true));
    destacadas.forEach(s=>desenhaSerie(s, false));
    // rótulos finais com menos de 18 unidades entre si são afastados na vertical (specs/2026-09-28_website_mobile:
    // "152.221" e "155.513" -- Meninas e Meninos -- saíam um sobre o outro, no celular e no desktop)
    if (finais.length > 1){
      finais.sort((a,b)=>a.y-b.y);
      for (let i=1;i<finais.length;i++) if (finais[i].y - finais[i-1].y < 18) finais[i].y = finais[i-1].y + 18;
      const excesso = finais[finais.length-1].y - (H - padB + 4);
      if (excesso > 0) finais.forEach(f=>{ f.y -= excesso; });
      finais.forEach(f=>f.t.setAttribute('y', f.y));
    }

    const hoverG = svgEl('g', {style:'display:none'}, svg);
    const hoverLine = svgEl('line', {y1:padT, y2:H-padB, class:'hover-line'}, hoverG);
    const hoverDots = series.map(s=>svgEl('circle', {r:3.6, fill:s.color, class:'hover-dot'}, hoverG));
    const tooltip = document.createElement('div'); tooltip.className = 'chart-tooltip';
    const capture = svgEl('rect', {x:padL, y:0, width:Math.max(plotW,1), height:H, fill:'transparent'}, svg);
    capture.style.cursor = 'crosshair';
    capture.style.pointerEvents = 'all';   // Firefox não acerta toque/hover em fill="transparent" (specs/2026-09-28_website_mobile)

    function onMove(clientX){
      const rect = svg.getBoundingClientRect();
      const mx = (clientX - rect.left) * (W/rect.width);
      let idx = Math.round((mx-padL)/plotW*(n-1));
      idx = Math.max(0, Math.min(n-1, idx));
      hoverG.style.display = 'block';
      const xp = xAt(idx);
      hoverLine.setAttribute('x1', xp); hoverLine.setAttribute('x2', xp);
      let rows = '';
      series.forEach((s,si)=>{
        const v = s.values[idx];
        hoverDots[si].setAttribute('cx', xp);
        hoverDots[si].setAttribute('cy', v==null ? -9999 : yAt(v));
        if (v != null) rows += '<div class="tt-row"><i style="background:'+s.color+'"></i>'+s.label+': <b>'+(s.format?s.format(v):fmtY(v))+'</b></div>';
      });
      tooltip.innerHTML = '<div class="tt-year">'+x[idx]+'</div>' + rows;
      tooltip.style.display = 'block';
      const leftPct = (xp/W)*100;
      tooltip.style.left = leftPct + '%';
      tooltip.style.transform = leftPct > 60 ? 'translate(-104%,-4%)' : 'translate(6%,-4%)';
    }
    capture.addEventListener('mousemove', e=>onMove(e.clientX));
    capture.addEventListener('touchstart', e=>{ if (e.touches[0]) onMove(e.touches[0].clientX); }, {passive:true});
    capture.addEventListener('touchmove', e=>{ if (e.touches[0]) onMove(e.touches[0].clientX); }, {passive:true});
    wrap._esconde = ()=>{ hoverG.style.display='none'; tooltip.style.display='none'; };
    // sair com o mouse esconde; toque não (depois do toque o navegador dispara um mouseleave de compatibilidade que
    // fechava o tooltip na hora) -- o toque fora do gráfico fecha (initToqueFora)
    capture.addEventListener('pointerleave', e=>{ if (e.pointerType === 'mouse') { hoverG.style.display='none'; tooltip.style.display='none'; } });

    wrap.appendChild(svg);
    wrap.appendChild(tooltip);
    container.appendChild(wrap);

    if (opts.table){
      const det = document.createElement('details'); det.className = 'data-table';
      det.innerHTML = '<summary>Ver dados em tabela</summary>';
      const scroll = document.createElement('div'); scroll.className = 'table-scroll';
      const tbl = document.createElement('table');
      let thead = '<tr><th>Ano</th>' + series.map(s=>'<th>'+s.label+'</th>').join('') + '</tr>';
      let rowsHtml = '';
      x.forEach((lab,i)=>{
        rowsHtml += '<tr><td>'+lab+'</td>' + series.map(s=>'<td>'+(s.values[i]==null?'—':(s.format?s.format(s.values[i]):fmtY(s.values[i])))+'</td>').join('') + '</tr>';
      });
      tbl.innerHTML = thead + rowsHtml;
      scroll.appendChild(tbl); det.appendChild(scroll);
      container.appendChild(det);
    }
  }

  // ================= pequenos múltiplos (B4) =================
  // um painel por série, todos na mesma escala, demais séries em cinza; controle "Painéis | Linhas" troca para o
  // gráfico original (P2: alternância no mesmo cartão, abre em Painéis)
  function pequenosMultiplos(container, cfg, ctx){
    const mob = !!(ctx && ctx.mob);
    const series = cfg.series, opts = cfg.opts || {};
    coresPadrao(series);
    let vMax = -Infinity;
    series.forEach(s=>s.values.forEach(v=>{ if (v!=null && v>vMax) vMax = v; }));
    const ctrl = document.createElement('div'); ctrl.className = 'alterna-ctrl sm-ctrl'; ctrl.setAttribute('role','group'); ctrl.setAttribute('aria-label','Visualização');
    const vistas = [document.createElement('div'), document.createElement('div')];
    vistas[0].className = 'sm-grid';
    if (opts.yLabel){ const t = document.createElement('div'); t.className = 'sm-unidade'; t.textContent = opts.yLabel; container.appendChild(t); }
    // largura real: a célula é medida depois de a grade entrar no DOM; oculta (largura 0), estima pela regra do CSS
    // (1 coluna < 480 px, 2 colunas até 719 px) -- o redesenho ao aparecer corrige
    const alvos = [];
    series.forEach((s,i)=>{
      const cel = document.createElement('div'); cel.className = 'sm-cell';
      const tit = document.createElement('div'); tit.className = 'sm-title'; tit.textContent = s.label;
      const alvo = document.createElement('div');
      cel.appendChild(tit); cel.appendChild(alvo); vistas[0].appendChild(cel);
      alvos.push(alvo);
    });
    // células de ~210 px: no desktop continuam no desenho fixo (300 de viewBox); em tela estreita, largura real sempre
    const reais = mob || TELA_ESTREITA.matches;
    const desenhaPaineis = ()=> series.forEach((s,i)=>{
      const contexto = series.filter((_,j)=>j!==i).map(o=>({label:o.label, values:o.values, format:o.format, muted:true, color:'var(--c-muted)'}));
      let pctx = null;
      if (reais){
        const w = mob ? ctx.w : larguraUtil(container).w, cols = mob ? (w < 480 ? 1 : 2) : Math.max(1, Math.floor((w + 18) / 228));
        pctx = {mob:true, w: alvos[i].clientWidth || (w - 14*(cols-1)) / cols};
      }
      desenhaLinha(alvos[i], {x:cfg.x, series:contexto.concat([{label:s.label, values:s.values, format:s.format, color:s.color}]), yFormat:cfg.yFormat,
        opts:{painel:true, width:300, height:170, padR: mob ? null : 44, maxXLabels:3, area:false, extremeLabels:false, yMax:vMax, yDecimals:opts.yDecimals, zeroBase:opts.zeroBase}}, pctx);
    });
    if (!reais) desenhaPaineis();
    desenhaLinha(vistas[1], {x:cfg.x, series:series, yFormat:cfg.yFormat, opts:Object.assign({}, opts, {multiplos:false, table:false})}, ctx);
    vistas[1].hidden = true;
    ['Painéis','Linhas'].forEach((rot,i)=>{
      const b = document.createElement('button'); b.type = 'button'; b.className = 'alterna-btn'; b.textContent = rot;
      b.setAttribute('aria-pressed', i===0 ? 'true' : 'false');
      b.addEventListener('click', ()=>{
        container._vista = i;   // mantido no redesenho (girar a tela)
        vistas.forEach((v,j)=>{ v.hidden = (j!==i); });
        ctrl.querySelectorAll('.alterna-btn').forEach((o,j)=>o.setAttribute('aria-pressed', j===i ? 'true' : 'false'));
      });
      ctrl.appendChild(b);
    });
    container.appendChild(ctrl); container.appendChild(vistas[0]); container.appendChild(vistas[1]);
    if (reais) desenhaPaineis();
    if (opts.table){
      const tmp = document.createElement('div');
      desenhaLinha(tmp, {x:cfg.x, series:series, yFormat:cfg.yFormat, opts:{multiplos:false, table:true}}, null);
      const det = tmp.querySelector('details.data-table'); if (det) container.appendChild(det);
    }
  }

  // ================= horizontal bar chart =================
  function barChart(container, cfg){
    const items = cfg.items, opts = cfg.opts || {};
    if (opts.yLabel){ const t = document.createElement('div'); t.className = 'bar-unidade'; t.textContent = opts.yLabel; container.appendChild(t); }
    const wrap = document.createElement('div'); wrap.className = 'bar-chart';
    const max = Math.max.apply(null, items.map(it=>it.value)) * 1.06 || 1;
    items.forEach((it,i)=>{
      const row = document.createElement('div'); row.className = 'bar-row';
      const label = document.createElement('div'); label.className = 'bar-label'; label.textContent = it.label; label.title = it.label;
      const track = document.createElement('div'); track.className = 'bar-track';
      const fillWrap = document.createElement('div');
      fillWrap.className = 'bar-fill';
      fillWrap.style.background = it.color || CAT[i%CAT.length];
      track.appendChild(fillWrap);
      const val = document.createElement('span'); val.className = 'bar-value';
      val.textContent = it.format ? it.format(it.value) : fmt(it.value);
      row.appendChild(label); row.appendChild(track); row.appendChild(val);
      wrap.appendChild(row);
      requestAnimationFrame(()=>{ fillWrap.style.width = (it.value/max*100) + '%'; });
    });
    container.appendChild(wrap);
  }

  // ================= grouped vertical bar chart =================
  // ctx como em desenhaLinha: null = desktop (inalterado); {mob:true, w} = largura real
  function desenhaBarras(container, cfg, ctx){
    const groups = cfg.groups, series = cfg.series, opts = cfg.opts || {};
    const mob = !!(ctx && ctx.mob);
    coresPadrao(series);
    const allVals = [];
    series.forEach(s=>s.values.forEach(v=>{ if (v!=null) allVals.push(v); }));
    const esc = escalaRedonda(0, Math.max.apply(null, allVals) * 1.08, mob ? 3 : 4);
    const maxV = esc[1], gridN = esc[2];
    const decY = opts.yDecimals != null ? opts.yDecimals : (Number.isInteger(Math.round(maxV/gridN*1e6)/1e6) ? 0 : 1);
    const fmtY = v => cfg.yFormat ? cfg.yFormat(v) : fmt(v, decY);
    // rótulos do eixo x inclinados quando não cabem na largura do grupo (10 bairros: os nomes se sobrepunham --
    // specs/2026-09-28_website_bugfix); a altura cresce o necessário para a área do gráfico não encolher
    const W = mob ? Math.round(Math.max(ctx.w, 260)) : (opts.width || 760), padR = 12;
    let padL = 40;
    if (mob){ const rotY = []; for (let i=0;i<=gridN;i++) rotY.push(String(fmtY(maxV*i/gridN)));
              padL = Math.max(26, Math.ceil(Math.max.apply(null, rotY.map(t=>t.length * 6.9))) + 9); }
    const larguraCar = mob ? 7.4 : 7.2, fonteGrupo = mob ? 11.5 : 12.6;
    const maxRot = Math.max.apply(null, groups.map(g=>String(g).length));
    const inclina = maxRot * larguraCar > ((W - padL - padR) / groups.length) * 0.95;
    const padB = inclina ? Math.min(150, 26 + maxRot * (mob ? 5 : 5.4)) : 56;
    const H = (mob ? Math.round(Math.max(220, Math.min(opts.height || 320, W * 0.8))) : (opts.height || 320)) + (padB - 56);
    const padT = opts.yLabel ? (mob ? 34 : 30) : 14;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const yAt = v => padT + plotH - (v/maxV)*plotH;

    const wrap = document.createElement('div'); wrap.className = 'chart-wrap';
    const legend = document.createElement('div'); legend.className = 'chart-legend';
    series.forEach(s=>{
      const item = document.createElement('span'); item.className = 'legend-item';
      item.innerHTML = '<i style="background:'+s.color+'"></i>' + s.label;
      legend.appendChild(item);
    });
    wrap.appendChild(legend);

    const svg = svgEl('svg', {viewBox:'0 0 '+W+' '+H, class:'chart-svg' + (mob ? ' chart-svg--real' : '')});
    tituloEixo(svg, opts.yLabel, 0, mob ? 13 : 12);
    for (let i=0;i<=gridN;i++){
      const v = maxV*i/gridN;
      const y = yAt(v);
      svgEl('line', {x1:padL, x2:W-padR, y1:y, y2:y, class:'grid-line'}, svg);
      svgEl('text', {x:padL-7, y:y+3.5, class:'axis-label', 'text-anchor':'end'}, svg).textContent = fmtY(v);
    }
    const groupW = plotW / groups.length;
    const barPad = 0.16;
    const innerW = groupW * (1 - 2*barPad);
    const barW = innerW / series.length;
    // B3: valor na ponta só com poucas barras (<= 12); acima disso, tooltip e tabela. Largura real: só se couber
    const rotulaBarras = groups.length * series.length <= 12 && (!mob || barW >= 22);
    const tooltip = document.createElement('div'); tooltip.className = 'chart-tooltip';

    groups.forEach((g,gi)=>{
      const gx0 = padL + gi*groupW + groupW*barPad;
      const cx = gx0 + innerW/2, ly = H - padB + 16;
      svgEl('text', inclina ? {x: cx, y: ly, class:'axis-label', 'text-anchor':'end', 'font-size':fonteGrupo, transform:'rotate(-35 '+cx+' '+ly+')'}
                            : {x: cx, y: H-38, class:'axis-label', 'text-anchor':'middle', 'font-size':fonteGrupo}, svg).textContent = g;
      series.forEach((s,si)=>{
        const v = s.values[gi];
        if (v == null) return;
        const bx = gx0 + si*barW;
        const by = yAt(v);
        const bh = Math.max(1, padT+plotH - by);
        const rect = svgEl('rect', {x:bx+0.6, y:by, width:Math.max(1,barW-1.2), height:bh, fill:s.color, rx:1.5}, svg);
        if (rotulaBarras) svgEl('text', {x:bx+barW/2, y:by-5, class:'bar-top-label', 'text-anchor':'middle'}, svg).textContent = s.format ? s.format(v) : fmtY(v);
        rect.style.cursor = 'pointer';
        const mostra = e=>{
          const r = wrap.getBoundingClientRect();
          tooltip.innerHTML = '<div class="tt-year">'+g+'</div><div class="tt-row"><i style="background:'+s.color+'"></i>'+s.label+': <b>'+(s.format?s.format(v):fmtY(v))+'</b></div>';
          tooltip.style.display = 'block';
          // preso às bordas do cartão (no celular o tooltip saía da tela)
          tooltip.style.left = Math.max(0, Math.min(e.clientX - r.left + 10, r.width - tooltip.offsetWidth - 4)) + 'px';
          tooltip.style.top = Math.max(0, e.clientY - r.top - 30) + 'px';
          tooltip.style.transform = 'none';
        };
        rect.addEventListener('mousemove', mostra);
        rect.addEventListener('click', mostra);   // toque
        rect.addEventListener('pointerleave', e=>{ if (e.pointerType === 'mouse') tooltip.style.display='none'; });
      });
    });

    wrap.appendChild(svg);
    wrap.appendChild(tooltip);
    wrap._esconde = ()=>{ tooltip.style.display = 'none'; };
    container.appendChild(wrap);

    if (opts.table){
      const det = document.createElement('details'); det.className = 'data-table';
      det.innerHTML = '<summary>Ver dados em tabela</summary>';
      const scroll = document.createElement('div'); scroll.className = 'table-scroll';
      const tbl = document.createElement('table');
      let thead = '<tr><th></th>' + groups.map(g=>'<th>'+g+'</th>').join('') + '</tr>';
      let rowsHtml = '';
      series.forEach(s=>{
        rowsHtml += '<tr><td>'+s.label+'</td>' + s.values.map(v=>'<td>'+(v==null?'—':(s.format?s.format(v):fmtY(v)))+'</td>').join('') + '</tr>';
      });
      tbl.innerHTML = thead + rowsHtml;
      scroll.appendChild(tbl); det.appendChild(scroll);
      container.appendChild(det);
    }
  }

  // ================= specs/2026-09-14_relatorio-interativo: controladores estaticos =================
  // (navbar, secoes retrateis, seletor de opcoes, toggle de outliers, download CSV,
  // tooltip de mapa -- tudo delegado/inicializado uma vez no DOMContentLoaded, ja que
  // esses elementos sao HTML estatico gerado em Python, nao criados por lineChart/etc.)

  // initNavbar/initSections (navbar hambúrguer e seções retráteis) removidos -- substituídos pelas
  // abas (js/navigation.js) e pelo sumário lateral (js/sidebar.js), specs/2026-09-24_website_refactor Bloco 5.

  // o texto de cada opção troca junto com o painel (specification.md §3.13) -- até 2026-09-25 só o painel
  // trocava e o texto ficava sempre no da 1a pill (specs/2026-09-25_website_graficos, V9.2)
  function selecionaPill(card, i){
    const pills = Array.from(card.querySelectorAll(':scope > .pill-col > .pill'));
    const panes = Array.from(card.querySelectorAll(':scope > .opt-panes > .opt-pane'));
    const texts = Array.from(card.querySelectorAll(':scope > .opt-texts > .opt-text'));
    pills.forEach((p,j)=>{
      if (j===i) p.setAttribute('data-active','true'); else p.removeAttribute('data-active');
      p.setAttribute('aria-pressed', j===i ? 'true' : 'false');
    });
    panes.forEach((pane,j)=>{ pane.hidden = (j!==i); });
    if (texts.length === panes.length) texts.forEach((t,j)=>{ t.hidden = (j!==i); });
    // select do celular (6+ opções, specs/2026-09-28_website_mobile M4) acompanha a pill
    const sel = card.querySelector(':scope > .pill-col > .pill-select');
    if (sel && sel.value !== String(i)) sel.value = String(i);
  }
  function pillAtiva(card){
    const pills = Array.from(card.querySelectorAll(':scope > .pill-col > .pill'));
    return Math.max(0, pills.findIndex(p=>p.getAttribute('data-active') === 'true'));
  }

  function initPills(){
    document.querySelectorAll('.option-card').forEach(card=>{
      card.querySelectorAll(':scope > .pill-col > .pill').forEach((pill,i)=>{
        pill.addEventListener('click', ()=>selecionaPill(card, i));
      });
      const sel = card.querySelector(':scope > .pill-col > .pill-select');
      if (sel) sel.addEventListener('change', ()=>selecionaPill(card, Number(sel.value)));
    });
  }

  // alternância Taxa <-> Óbitos (E9, specs/2026-09-25_website_graficos §2): um option-card por modo, mesmas
  // pills na mesma ordem; trocar o modo mantém a pill selecionada
  function initAlternancia(){
    document.querySelectorAll('.alterna').forEach(box=>{
      const botoes = Array.from(box.querySelectorAll(':scope > .alterna-ctrl > .alterna-btn'));
      const modos = Array.from(box.querySelectorAll(':scope > .alterna-modo'));
      botoes.forEach((btn,i)=>{
        btn.addEventListener('click', ()=>{
          const atual = modos.findIndex(m=>!m.hidden);
          if (atual === i) return;
          const cardAtual = modos[atual] && modos[atual].querySelector(':scope > .option-card');
          const cardNovo = modos[i].querySelector(':scope > .option-card');
          if (cardAtual && cardNovo) selecionaPill(cardNovo, pillAtiva(cardAtual));
          modos.forEach((m,j)=>{ m.hidden = (j!==i); });
          botoes.forEach((b,j)=>b.setAttribute('aria-pressed', j===i ? 'true' : 'false'));
        });
      });
    });
  }

  function initOutliers(){
    document.querySelectorAll('.outlier-card').forEach(card=>{
      const btn = card.querySelector('.outlier-btn');
      const full = card.querySelector(':scope > .outlier-pane[data-variant="full"]');
      const clean = card.querySelector(':scope > .outlier-pane[data-variant="clean"]');
      if (!btn || !full || !clean) return;
      btn.addEventListener('click', ()=>{
        const semOutliers = btn.getAttribute('data-active') !== 'true';
        btn.setAttribute('data-active', semOutliers ? 'true' : 'false');
        full.hidden = semOutliers;
        clean.hidden = !semOutliers;
      });
    });
  }

  function initDownloads(){
    document.addEventListener('click', e=>{
      const btn = e.target.closest('.dl-btn');
      if (!btn) return;
      const card = btn.closest('.out');
      if (!card || !card.dataset.csv) return;
      const blob = new Blob(['﻿' + card.dataset.csv], {type:'text/csv;charset=utf-8;'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = card.dataset.filename || 'dados.csv';
      document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(a.href);
    });
  }

  function initMapTooltips(){
    document.querySelectorAll('.map-svg-card').forEach(card=>{
      const svg = card.querySelector('.map-svg');
      if (!svg) return;
      const tooltip = document.createElement('div'); tooltip.className = 'chart-tooltip';
      tooltip.style.position = 'absolute';
      card.appendChild(tooltip);
      // regiões são <use href="#gb12"> etc. (geometria em data/geo.js); nome vem de window.GEO_NOMES
      let tocada = null;
      svg.querySelectorAll('use[href]').forEach(path=>{
        const nome = (window.GEO_NOMES || {})[path.getAttribute('href').slice(1)] || '';
        const mostra = e=>{
          const r = card.getBoundingClientRect();
          tooltip.innerHTML = '<div class="tt-row"><b>'+nome+'</b></div><div class="tt-row">'+path.dataset.v+'</div>';
          tooltip.style.display = 'block';
          // preso às bordas do cartão (no celular o tooltip saía da tela -- specs/2026-09-28_website_mobile §5)
          tooltip.style.left = Math.max(4, Math.min(e.clientX - r.left + 12, r.width - tooltip.offsetWidth - 4)) + 'px';
          tooltip.style.top = Math.max(4, e.clientY - r.top - 34 - (e.pointerType && e.pointerType !== 'mouse' ? 30 : 0)) + 'px';
          tooltip.style.transform = 'none';
        };
        path.addEventListener('mousemove', mostra);
        path.addEventListener('pointerleave', e=>{ if (e.pointerType === 'mouse' && tocada !== path) tooltip.style.display = 'none'; });
        // toque: mostra e destaca a região; tocar em outra troca; tocar fora do mapa fecha (listener global)
        path.addEventListener('pointerup', e=>{
          if (e.pointerType === 'mouse') return;
          if (tocada) tocada.classList.remove('toque');
          tocada = path; path.classList.add('toque'); mostra(e);
        });
      });
      card._esconde = ()=>{ tooltip.style.display = 'none'; if (tocada) { tocada.classList.remove('toque'); tocada = null; } };
    });
  }

  // ================= largura real e redesenho (specs/2026-09-28_website_mobile M3) =================
  // Desktop (>= 1100 px) nunca entra aqui: o desenho de viewBox fixo continua o mesmo, pixel a pixel. Em telas
  // estreitas, contêiner < 640 px -> desenho na largura real. Os gráficos nascem uma vez no carregamento, muitos em
  // painéis ocultos (largura 0): esses são desenhados com uma estimativa e redesenhados quando aparecem (pill, select,
  // aba, Taxa|Óbitos); girar a tela redesenha se a largura mudar >= 40 px.
  const TELA_ESTREITA = window.matchMedia('(max-width:1099.98px)');
  const LIMITE_REAL = 640;
  function larguraUtil(el){
    for (let e = el; e && e !== document.documentElement; e = e.parentElement){
      const w = e.clientWidth;
      if (w > 0){
        if (e === el) return {w: w, visivel: true};
        const cs = getComputedStyle(e);
        return {w: w - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - 28, visivel: false};   // 28 = padding do .out no celular
      }
    }
    return {w: document.documentElement.clientWidth - 60, visivel: false};
  }
  function modoReal(w){ return TELA_ESTREITA.matches && w < LIMITE_REAL; }
  function desenha(c){
    const reg = c._grafico; if (!reg) return;
    const med = larguraUtil(c), mob = modoReal(med.w);
    const tabelaAberta = !!(c.querySelector('details.data-table') || {}).open;
    c.replaceChildren();
    c._w = med.w; c._mob = mob; c._visivel = med.visivel;
    reg.fn(c, reg.cfg, mob ? {mob: true, w: med.w} : null);
    c._reais = mob || !!c.querySelector('.chart-svg--real');
    if (tabelaAberta){ const d = c.querySelector('details.data-table'); if (d) d.open = true; }
    if (c._vista){ const b = c.querySelectorAll('.sm-ctrl .alterna-btn')[c._vista]; if (b) b.click(); }
  }
  const pendentes = new Set(); let timer = null;
  function agendaRedesenho(c){
    pendentes.add(c); clearTimeout(timer);
    timer = setTimeout(()=>{ pendentes.forEach(desenha); pendentes.clear(); }, 150);
  }
  const observador = 'ResizeObserver' in window ? new ResizeObserver(entradas=>{
    entradas.forEach(en=>{
      const c = en.target, w = c.clientWidth;
      if (!w || !c._grafico) return;
      const mob = modoReal(w);
      if (!mob && !c._reais) { c._visivel = true; return; }   // desenho de viewBox fixo: escala sozinho
      if (!c._visivel) { if (Math.abs(w - c._w) > 2 || mob !== c._mob) desenha(c); else c._visivel = true; return; }
      if (mob !== c._mob || Math.abs(w - c._w) >= 40) agendaRedesenho(c);
    });
  }) : null;
  function registra(fn){
    return function(container, cfg){
      container._grafico = {fn: fn, cfg: cfg};
      desenha(container);
      if (observador) observador.observe(container);
    };
  }
  const lineChart = registra(desenhaLinha), groupedBarChart = registra(desenhaBarras);

  // mapas: --map-esc = unidades do viewBox por px na tela; mobile.css usa para manter escala e rosa legíveis
  function atualizaEscalaMapa(svg){
    const w = svg.getBoundingClientRect().width;
    if (w > 0) svg.style.setProperty('--map-esc', (svg.viewBox.baseVal.width / w).toFixed(3));
  }
  function initEscalaMapas(){
    const mapas = document.querySelectorAll('.map-svg');
    if ('ResizeObserver' in window){ const ro = new ResizeObserver(en=>en.forEach(e=>atualizaEscalaMapa(e.target))); mapas.forEach(m=>ro.observe(m)); }
    else mapas.forEach(atualizaEscalaMapa);
  }

  // toque fora de um gráfico/mapa fecha o tooltip dele (no celular não há mouseleave)
  function initToqueFora(){
    document.addEventListener('pointerdown', e=>{
      if (e.pointerType === 'mouse') return;
      document.querySelectorAll('.chart-wrap, .map-svg-card').forEach(el=>{ if (el._esconde && !el.contains(e.target)) el._esconde(); });
    }, {passive: true});
  }

  document.addEventListener('DOMContentLoaded', function(){
    initPills(); initAlternancia(); initOutliers(); initDownloads(); initMapTooltips(); initEscalaMapas(); initToqueFora();
  });

  window.byId = byId; window.lineChart = lineChart; window.barChart = barChart; window.groupedBarChart = groupedBarChart;
  window.fmt = fmt; window.pct = pct; window.pm = pm;
})();
