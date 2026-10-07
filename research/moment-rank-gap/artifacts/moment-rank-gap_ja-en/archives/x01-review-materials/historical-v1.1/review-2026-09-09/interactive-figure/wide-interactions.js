(() => {
  'use strict';
  const figures = [...document.querySelectorAll('[data-wide-figure]')];
  if (!figures.length) return;
  const state = { eta: 0.9, delta: 0.1, criticalEta: false };
  const fmt = x => Number(x.toFixed(6)).toString();
  const thresholds = () => ({
    k: state.eta * (1 - state.eta),
    // The symbolic η = 1/√2 preset has c = h exactly; no epsilon comparisons.
    c: state.criticalEta ? 0.25 : (1 - state.eta * state.eta) / 2,
    h: 0.25
  });
  const count = (d, q) => {
    if (d < q.k) return 2;
    if (d < Math.min(q.c, q.h)) return 6;
    if (d >= Math.max(q.c, q.h)) return 1;
    return q.c < q.h ? 4 : 2;
  };
  const tag = (name, attrs, body = '') => `<${name} ${Object.entries(attrs).map(([k, v]) => `${k}="${v}"`).join(' ')}>${body}</${name}>`;
  const text = (x, y, label, extra = {}) => tag('text', { x, y, ...extra }, label);
  const line = (x1, y1, x2, y2, extra = {}) => tag('line', { x1, y1, x2, y2, ...extra });

  function draw(f) {
    const ja = f.dataset.wideLang === 'ja', t = (j, e) => ja ? j : e;
    const q = thresholds(), width = Math.max(280, Math.round(f.clientWidth || 760));
    const left = 22, right = width - 22, X = d => left + d / 0.55 * (right - left);
    const svg = f.querySelector('svg');
    svg.setAttribute('viewBox', `0 0 ${width} 191`);
    const stops = [...new Set([0, q.k, q.c, q.h, 0.55])].sort((a, b) => a - b);
    const colors = { 1: '#146b61', 2: '#d4e9df', 4: '#ddb979', 6: '#f1dbb3' };
    let html = tag('title', {}, t('広い総和帯の道連結成分数', 'Path-component counts for a wider sum band'));
    for (let i = 1; i < stops.length; i++) {
      const a = stops[i - 1], b = stops[i], n = count((a + b) / 2, q), w = X(b) - X(a);
      html += tag('rect', { x: X(a), y: 42, width: w, height: 44, fill: colors[n] },
        tag('title', {}, `${fmt(a)} ≤ δ &lt; ${fmt(b)}: ${n} ${t('成分', n === 1 ? 'component' : 'components')}`));
      if (w > 26) html += text((X(a) + X(b)) / 2, 70, n, { 'text-anchor': 'middle', class: 'value', style: `font-size:16px;fill:${n === 1 ? '#fff' : '#182927'}` });
    }
    for (const tick of (width < 400 ? [0, 0.2, 0.4, 0.55] : [0, 0.1, 0.2, 0.3, 0.4, 0.55])) {
      html += line(X(tick), 87, X(tick), 93, { class: 'axis' });
      html += text(X(tick), 111, fmt(tick), { 'text-anchor': 'middle' });
    }
    ['k', 'c', 'h'].forEach((name, i) => {
      const y = 131 + i * 23;
      html += line(X(q[name]), 87, X(q[name]), y - 12, { stroke: 'var(--slate)', 'stroke-width': 1, 'stroke-dasharray': '2 3' });
      html += text(X(q[name]), y, name, { 'text-anchor': 'middle', class: 'value' });
    });
    html += line(X(state.delta), 29, X(state.delta), 92, { stroke: 'var(--ink)', 'stroke-width': 2 });
    html += tag('circle', { cx: X(state.delta), cy: 27, r: 3.5, fill: 'var(--ink)' });
    html += text(Math.min(right - 44, Math.max(left + 44, X(state.delta))), 15, `δ = ${fmt(state.delta)}`, { 'text-anchor': 'middle', class: 'value' });
    svg.innerHTML = html;
    f.querySelector('[data-wide-value="eta"]').textContent = state.criticalEta ? '1/√2' : fmt(state.eta);
    f.querySelector('[data-wide-value="delta"]').textContent = fmt(state.delta);
    f.querySelector('[data-wide-control="eta"]').value = String(state.eta);
    f.querySelector('[data-wide-control="delta"]').value = String(state.delta);
    f.querySelectorAll('[data-wide-threshold]').forEach(button => {
      const name = button.dataset.wideThreshold;
      button.setAttribute('aria-pressed', String(state.delta === q[name]));
      button.setAttribute('aria-label', t(`δ を閾値 ${name} = ${fmt(q[name])} に設定`, `Set δ to threshold ${name} = ${fmt(q[name])}`));
    });
    f.querySelector('[data-wide-action="eta-critical"]').setAttribute('aria-pressed', String(state.criticalEta));
    const n = count(state.delta, q);
    f.querySelector('.metrics').innerHTML = [['k', q.k], ['c', q.c], ['h', q.h]].map(([name, value]) => `<span>${name}<b>${fmt(value)}</b></span>`).join('');
    const order = q.c === q.h ? 'c = h' : q.c < q.h ? 'c < h' : 'h < c';
    const sequence = q.c === q.h ? '2 → 6 → 1' : q.c < q.h ? '2 → 6 → 4 → 1' : '2 → 6 → 2 → 1';
    f.querySelector('.figure-output').textContent = t(
      `現在は ${n} 成分です。${order}：δ を増やすと ${sequence} と変化します。`,
      `Currently ${n} path component${n === 1 ? '' : 's'}. ${order}: as δ increases, the count follows ${sequence}.`
    );
  }
  const redraw = () => figures.forEach(draw);
  for (const f of figures) {
    f.querySelectorAll('[data-wide-control]').forEach(input => input.addEventListener('input', () => {
      const value = Number(input.value);
      if (!Number.isFinite(value)) return;
      if (input.dataset.wideControl === 'eta') {
        state.eta = Math.max(0.51, Math.min(0.99, value)); state.criticalEta = false;
      } else state.delta = Math.max(0, Math.min(0.55, value));
      redraw();
    }));
    f.querySelectorAll('[data-wide-threshold]').forEach(button => button.addEventListener('click', () => {
      state.delta = thresholds()[button.dataset.wideThreshold]; redraw();
    }));
    f.querySelector('[data-wide-action="eta-critical"]').addEventListener('click', () => {
      state.eta = Math.SQRT1_2; state.criticalEta = true; redraw();
    });
  }
  document.querySelectorAll('[data-set-lang]').forEach(button => button.addEventListener('click', () => requestAnimationFrame(redraw)));
  let queued = false;
  window.addEventListener('resize', () => {
    if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; redraw(); }); }
  });
  redraw();
})();
