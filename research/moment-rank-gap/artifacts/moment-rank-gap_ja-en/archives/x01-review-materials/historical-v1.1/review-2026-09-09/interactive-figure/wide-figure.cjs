'use strict';

exports.figure = function figure(lang) {
  const ja = lang === 'ja';
  const id = `${ja ? 'ja' : 'en'}-fig-wide`;
  const t = (j, e) => ja ? j : e;
  const title = t('広い総和帯で、成分が生まれてから合流する', 'A wider sum band: components appear, then merge');
  return `<figure class="figure" data-wide-figure data-wide-lang="${ja ? 'ja' : 'en'}" id="${id}">
<div class="figure-head"><span class="figure-num">${t('図 5', 'FIGURE 5')}</span><h4>${title}</h4></div>
<p class="intro">${t('n = 2、s = 1 に固定します。|x₁ + x₂ − 1| ≤ η、x₁(1 − x₁) + x₂(1 − x₂) ≤ δ を満たす集合の道連結成分数です。帯内の数値は成分数を示します。', 'Fix n = 2 and s = 1. The diagram counts path components of the set satisfying |x₁ + x₂ − 1| ≤ η and x₁(1 − x₁) + x₂(1 − x₂) ≤ δ. Numbers inside the band are component counts.')}</p>
<div class="controls">
<div class="control"><label for="${id}-eta">${t('総和の許容幅 η', 'Sum tolerance η')}<output data-wide-value="eta" for="${id}-eta">0.9</output></label><input id="${id}-eta" data-wide-control="eta" type="range" min="0.51" max="0.99" step="0.001" value="0.9"></div>
<div class="control"><label for="${id}-delta">${t('欠損の上限 δ', 'Defect bound δ')}<output data-wide-value="delta" for="${id}-delta">0.1</output></label><input id="${id}-delta" data-wide-control="delta" type="range" min="0" max="0.55" step="0.001" value="0.1"></div>
</div>
<div class="phase-buttons" aria-label="${t('閾値を正確に選択', 'Select exact thresholds')}"><button type="button" data-wide-threshold="k">δ = k</button><button type="button" data-wide-threshold="c">δ = c</button><button type="button" data-wide-threshold="h">δ = h</button><button type="button" data-wide-action="eta-critical">η = 1/√2</button></div>
<div class="chart-box"><svg class="chart-svg" role="img" aria-label="${title}"></svg></div>
<div class="metrics"></div><div class="figure-output" aria-live="polite"></div>
<figcaption>${t('k = η(1 − η) は4成分が新たに現れる閾値、c = (1 − η²)/2 と h = 1/4 は合流の閾値です。閾値ボタンは丸め前の値を選び、等号は変化後の成分数に含めます。η = 1/√2 では c = h で合流が同時に起きます。非常に短い区間の帯内数値は省略されます。', 'At k = η(1 − η), four new components appear; c = (1 − η²)/2 and h = 1/4 are merger thresholds. Threshold buttons select unrounded values, with equality assigned to the state after the transition. At η = 1/√2, c = h and both mergers occur simultaneously. Labels inside very short intervals are omitted.')}</figcaption>
</figure>`;
};
