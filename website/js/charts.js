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

  function prepararSeries(series){
    series.forEach((s,i)=>{ if (!s.color) s.color = series.length===1 ? 'var(--accent)' : CAT[i%CAT.length]; });
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

  function lineChart(container, cfg){
    const x = cfg.x, series = cfg.series, opts = cfg.opts || {};
    // B4 (specs/2026-09-25_website_graficos, P2): 7 ou mais séries -> pequenos múltiplos, com a visão de linhas ao lado
    if (!opts.painel && opts.multiplos !== false && series.length >= LIMIAR_DESTAQUE + 1) return pequenosMultiplos(container, cfg);
    const { destacadas, apagadas } = prepararSeries(series);
    const W = opts.width || 680, H = opts.height || 250;
    const padL = opts.padL != null ? opts.padL : 38;
    const padR = opts.padR != null ? opts.padR : (opts.endLabels === false ? 14 : 66);
    const padT = opts.yLabel ? 30 : 16, padB = 28;
    const plotW = W - padL - padR, plotH = H - padT - padB;
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
    const esc = escalaRedonda(vMin, vMax, opts.painel ? 2 : 4);
    vMin = esc[0]; vMax = esc[1];
    const gridN = esc[2];
    const n = x.length;
    const xAt = i => padL + (n===1 ? plotW/2 : (plotW * i/(n-1)));
    const yAt = v => padT + plotH - ((v - vMin)/((vMax-vMin)||1))*plotH;
    const passoY = (vMax - vMin) / gridN;
    const decY = opts.yDecimals != null ? opts.yDecimals : (Number.isInteger(Math.round(passoY*1e6)/1e6) ? 0 : 1);
    const fmtY = v => cfg.yFormat ? cfg.yFormat(v) : fmt(v, decY);

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
    const svg = svgEl('svg', {viewBox:'0 0 '+W+' '+H, class:'chart-svg', preserveAspectRatio:'xMidYMid meet'});
    tituloEixo(svg, opts.yLabel, 0, 12);
    for (let i=0;i<=gridN;i++){
      const v = vMin + (vMax-vMin)*i/gridN;
      const y = yAt(v);
      svgEl('line', {x1:padL, x2:W-padR, y1:y, y2:y, class:'grid-line'}, svg);
      svgEl('text', {x:padL-7, y:y+3.5, class:'axis-label', 'text-anchor':'end'}, svg).textContent = fmtY(v);
    }
    const maxLabels = opts.maxXLabels || 7;
    const step = Math.max(1, Math.ceil(n/maxLabels));
    x.forEach((lab,i)=>{
      // o último ano sempre aparece; o rótulo regular colado a ele sai (antes "2024" e "2025" se sobrepunham)
      if (i !== n-1 && (i % step !== 0 || (n-1-i) < Math.max(2, step*0.6))) return;
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
        }
      }
      // maximo/minimo fixos, sempre visiveis sem hover (specification.md §3.9) --
      // pula o ponto ja coberto pelo end-label "mais recente" (idx===lastValidIdx) e o
      // primeiro ponto (idx===0, ja visivel por ser onde a linha comeca) -- em series
      // com poucos pontos isso evita rotulo redundante colado no eixo Y. Limiar mais
      // baixo que o end-label (maxExtremeSeries, nao maxDirectLabels): com muitas series
      // no mesmo grafico, maximos/minimos caem em posicoes X arbitrarias e colidem com
      // mais facilidade do que o end-label (que fica sempre no mesmo X, a ultima coluna).
      if (!apagada && opts.extremeLabels !== false && destacadas.length <= (opts.maxExtremeSeries || 2)){
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
    apagadas.forEach(s=>desenhaSerie(s, true));
    destacadas.forEach(s=>desenhaSerie(s, false));

    const hoverG = svgEl('g', {style:'display:none'}, svg);
    const hoverLine = svgEl('line', {y1:padT, y2:H-padB, class:'hover-line'}, hoverG);
    const hoverDots = series.map(s=>svgEl('circle', {r:3.6, fill:s.color, class:'hover-dot'}, hoverG));
    const tooltip = document.createElement('div'); tooltip.className = 'chart-tooltip';
    const capture = svgEl('rect', {x:padL, y:0, width:Math.max(plotW,1), height:H, fill:'transparent'}, svg);
    capture.style.cursor = 'crosshair';

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
    capture.addEventListener('touchmove', e=>{ if (e.touches[0]) onMove(e.touches[0].clientX); }, {passive:true});
    capture.addEventListener('mouseleave', ()=>{ hoverG.style.display='none'; tooltip.style.display='none'; });

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
  function pequenosMultiplos(container, cfg){
    const series = cfg.series, opts = cfg.opts || {};
    series.forEach((s,i)=>{ if (!s.color) s.color = CAT[i%CAT.length]; });
    let vMax = -Infinity;
    series.forEach(s=>s.values.forEach(v=>{ if (v!=null && v>vMax) vMax = v; }));
    const ctrl = document.createElement('div'); ctrl.className = 'alterna-ctrl sm-ctrl'; ctrl.setAttribute('role','group'); ctrl.setAttribute('aria-label','Visualização');
    const vistas = [document.createElement('div'), document.createElement('div')];
    vistas[0].className = 'sm-grid';
    if (opts.yLabel){ const t = document.createElement('div'); t.className = 'sm-unidade'; t.textContent = opts.yLabel; container.appendChild(t); }
    series.forEach((s,i)=>{
      const cel = document.createElement('div'); cel.className = 'sm-cell';
      const tit = document.createElement('div'); tit.className = 'sm-title'; tit.textContent = s.label;
      const alvo = document.createElement('div');
      cel.appendChild(tit); cel.appendChild(alvo); vistas[0].appendChild(cel);
      const contexto = series.filter((_,j)=>j!==i).map(o=>({label:o.label, values:o.values, format:o.format, muted:true, color:'var(--c-muted)'}));
      lineChart(alvo, {x:cfg.x, series:contexto.concat([{label:s.label, values:s.values, format:s.format, color:s.color}]), yFormat:cfg.yFormat,
        opts:{painel:true, width:300, height:170, padR:44, maxXLabels:3, area:false, extremeLabels:false, yMax:vMax, yDecimals:opts.yDecimals, zeroBase:opts.zeroBase}});
    });
    lineChart(vistas[1], {x:cfg.x, series:series, yFormat:cfg.yFormat, opts:Object.assign({}, opts, {multiplos:false, table:false})});
    vistas[1].hidden = true;
    ['Painéis','Linhas'].forEach((rot,i)=>{
      const b = document.createElement('button'); b.type = 'button'; b.className = 'alterna-btn'; b.textContent = rot;
      b.setAttribute('aria-pressed', i===0 ? 'true' : 'false');
      b.addEventListener('click', ()=>{
        vistas.forEach((v,j)=>{ v.hidden = (j!==i); });
        ctrl.querySelectorAll('.alterna-btn').forEach((o,j)=>o.setAttribute('aria-pressed', j===i ? 'true' : 'false'));
      });
      ctrl.appendChild(b);
    });
    container.appendChild(ctrl); container.appendChild(vistas[0]); container.appendChild(vistas[1]);
    if (opts.table){
      const tmp = document.createElement('div');
      lineChart(tmp, {x:cfg.x, series:series, yFormat:cfg.yFormat, opts:{multiplos:false, table:true}});
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
  function groupedBarChart(container, cfg){
    const groups = cfg.groups, series = cfg.series, opts = cfg.opts || {};
    series.forEach((s,i)=>{ if (!s.color) s.color = CAT[i%CAT.length]; });
    const W = opts.width || 760, H = opts.height || 320;
    const padL = 40, padR = 12, padT = opts.yLabel ? 30 : 14, padB = 56;
    // B3: valor na ponta só com poucas barras (<= 12); acima disso, tooltip e tabela
    const rotulaBarras = groups.length * series.length <= 12;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const allVals = [];
    series.forEach(s=>s.values.forEach(v=>{ if (v!=null) allVals.push(v); }));
    const esc = escalaRedonda(0, Math.max.apply(null, allVals) * 1.08, 4);
    const maxV = esc[1], gridN = esc[2];
    const yAt = v => padT + plotH - (v/maxV)*plotH;
    const decY = opts.yDecimals != null ? opts.yDecimals : (Number.isInteger(Math.round(maxV/gridN*1e6)/1e6) ? 0 : 1);
    const fmtY = v => cfg.yFormat ? cfg.yFormat(v) : fmt(v, decY);

    const wrap = document.createElement('div'); wrap.className = 'chart-wrap';
    const legend = document.createElement('div'); legend.className = 'chart-legend';
    series.forEach(s=>{
      const item = document.createElement('span'); item.className = 'legend-item';
      item.innerHTML = '<i style="background:'+s.color+'"></i>' + s.label;
      legend.appendChild(item);
    });
    wrap.appendChild(legend);

    const svg = svgEl('svg', {viewBox:'0 0 '+W+' '+H, class:'chart-svg'});
    tituloEixo(svg, opts.yLabel, 0, 12);
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
    const tooltip = document.createElement('div'); tooltip.className = 'chart-tooltip';

    groups.forEach((g,gi)=>{
      const gx0 = padL + gi*groupW + groupW*barPad;
      svgEl('text', {x: gx0 + innerW/2, y: H-38, class:'axis-label', 'text-anchor':'middle', 'font-size':12.6}, svg).textContent = g;
      series.forEach((s,si)=>{
        const v = s.values[gi];
        if (v == null) return;
        const bx = gx0 + si*barW;
        const by = yAt(v);
        const bh = Math.max(1, padT+plotH - by);
        const rect = svgEl('rect', {x:bx+0.6, y:by, width:Math.max(1,barW-1.2), height:bh, fill:s.color, rx:1.5}, svg);
        if (rotulaBarras) svgEl('text', {x:bx+barW/2, y:by-5, class:'bar-top-label', 'text-anchor':'middle'}, svg).textContent = s.format ? s.format(v) : fmtY(v);
        rect.style.cursor = 'pointer';
        rect.addEventListener('mousemove', e=>{
          const r = wrap.getBoundingClientRect();
          tooltip.innerHTML = '<div class="tt-year">'+g+'</div><div class="tt-row"><i style="background:'+s.color+'"></i>'+s.label+': <b>'+(s.format?s.format(v):fmtY(v))+'</b></div>';
          tooltip.style.display = 'block';
          tooltip.style.left = (e.clientX - r.left + 10) + 'px';
          tooltip.style.top = (e.clientY - r.top - 30) + 'px';
          tooltip.style.transform = 'none';
        });
        rect.addEventListener('mouseleave', ()=>{ tooltip.style.display='none'; });
      });
    });

    wrap.appendChild(svg);
    wrap.appendChild(tooltip);
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
      svg.querySelectorAll('use[href]').forEach(path=>{
        const nome = (window.GEO_NOMES || {})[path.getAttribute('href').slice(1)] || '';
        path.addEventListener('mousemove', e=>{
          const r = card.getBoundingClientRect();
          tooltip.innerHTML = '<div class="tt-row"><b>'+nome+'</b></div><div class="tt-row">'+path.dataset.v+'</div>';
          tooltip.style.display = 'block';
          tooltip.style.left = (e.clientX - r.left + 12) + 'px';
          tooltip.style.top = (e.clientY - r.top - 34) + 'px';
          tooltip.style.transform = 'none';
        });
        path.addEventListener('mouseleave', ()=>{ tooltip.style.display = 'none'; });
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    initPills(); initAlternancia(); initOutliers(); initDownloads(); initMapTooltips();
  });

  window.byId = byId; window.lineChart = lineChart; window.barChart = barChart; window.groupedBarChart = groupedBarChart;
  window.fmt = fmt; window.pct = pct; window.pm = pm;
})();
