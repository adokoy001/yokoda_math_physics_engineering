
(function(){'use strict';
const $=id=>document.getElementById(id);if(!$('round10-capacity'))return;
const a=.9,b=1.1,kappa=1,mu=Math.log(b/a)/(b-a);
function q(rate){return Math.exp(-a*rate)*(-Math.expm1(-(b-a)*rate));}
function capacityRate(){let lo=1/b,hi=2/a;for(let j=0;j<100;j++){const mid=(lo+hi)/2,d=1/mid-a+(b-a)/Math.expm1((b-a)*mid);if(d>0)lo=mid;else hi=mid;}return(lo+hi)/2;}
const lambdaC=capacityRate(),G=lambdaC*q(lambdaC),critical=4*kappa/lambdaC;
function survival(shape,x){let sum=1,term=1;for(let j=1;j<shape;j++){term*=x/j;sum+=term;}return Math.exp(-x)*sum;}
function stateBound(k){let best=0;for(let j=1;j<=k;j++){const rate=j*mu,prob=survival(j,a*rate)-survival(j,b*rate);best=Math.max(best,prob);}return kappa*best;}
function oneState(budget){if(!(budget>0))return{value:0,rate:0,capacity:0,spoke:0,direct:kappa};const lambda0=4*kappa/budget,rate=lambda0>=lambdaC?lambdaC:lambda0>mu?lambda0:mu,A=Math.min(kappa,budget*rate/4);return{value:A*q(rate),rate,capacity:4*A/rate,spoke:2*A,direct:Math.max(0,kappa-A)};}
function values(budget,k){const star=oneState(budget),capacityBound=budget*G/4,byStates=stateBound(k);return{budget,k,star,capacityBound,byStates,upper:Math.min(capacityBound,byStates),exact:budget<=critical+1e-12};}
function f(x,n){return x.toFixed(n===undefined?5:n);}
function draw(v){const chart=$('round10-budget-chart'),width=chart.getBoundingClientRect().width,W=Math.max(248,Math.min(840,width||760)),mobile=W<430,H=mobile?300:320,L=mobile?48:55,R=W-12,T=35,B=H-43,ymax=Math.max(.09,v.byStates*1.15),X=x=>L+x/20*(R-L),Y=y=>B-y/ymax*(B-T);chart.setAttribute('viewBox',`0 0 ${W} ${H}`);
let s=`<rect x="${X(0)}" y="${T}" width="${X(critical)-X(0)}" height="${B-T}" fill="#d9e8d1"/><text x="${L}" y="17" font-size="11" fill="#596e6c">観測値 D</text>`;
for(let j=0;j<=4;j++){const y=ymax*j/4;s+=`<path d="M${L} ${Y(y)}H${R}" stroke="#d5ded5"/><text x="${L-7}" y="${Y(y)+4}" text-anchor="end" font-size="11" fill="#596e6c">${f(y,2)}</text>`;}
for(const x of(mobile?[0,5,10,15,20]:[0,2,5,10,15,20]))s+=`<path d="M${X(x)} ${B}v4" stroke="#7b8981"/><text x="${X(x)}" y="${B+19}" text-anchor="middle" font-size="11" fill="#596e6c">${x}</text>`;
s+=`<path d="M${L} ${T}V${B}H${R}" fill="none" stroke="#7b8981"/><text x="${R}" y="${H-3}" text-anchor="end" font-size="11" fill="#596e6c">総容量の上限 B</text>`;
function path(fn){let d='';for(let j=0;j<=400;j++){const budget=j/20;d+=(j?'L':'M')+X(budget).toFixed(2)+' '+Y(fn(budget)).toFixed(2);}return d;}
s+=`<path d="${path(budget=>Math.min(budget*G/4,v.byStates))}" fill="none" stroke="#aa6235" stroke-width="3" stroke-dasharray="6 4"/><path d="${path(budget=>oneState(budget).value)}" fill="none" stroke="#0a7166" stroke-width="2.5"/><path d="M${X(v.budget)} ${T}V${B}" stroke="#73827a" stroke-dasharray="2 4"/><circle cx="${X(v.budget)}" cy="${Y(v.upper)}" r="5" fill="#fffdf8" stroke="#aa6235" stroke-width="2"/><circle cx="${X(v.budget)}" cy="${Y(v.star.value)}" r="3.5" fill="#0a7166"/>`;
chart.innerHTML=s;chart.setAttribute('aria-label',`状態数${v.k}以下。総容量${f(v.budget,2)}の全回路の保証上界は${f(v.upper,6)}、有限1状態の達成値は${f(v.star.value,6)}。総容量${f(critical,5)}以下は二つが一致する。`);
}
function update(){const budget=+$('round10-budget').value,k=+$('round10-k').value,v=values(budget,k);$('round10-budget-out').textContent=f(budget,2);$('round10-k-out').textContent=k;$('round10-upper').textContent=f(v.upper,6);$('round10-lower').textContent=f(v.star.value,6);$('round10-cap-bound').textContent=f(v.capacityBound,6);$('round10-state-bound').textContent=f(v.byStates,6);$('round10-used').textContent=f(v.star.capacity,5);$('round10-spoke').textContent=f(v.star.spoke,5);$('round10-direct').textContent=f(v.star.direct,5);
const status=$('round10-status');status.classList.toggle('round10-open',!v.exact&&k>1);
if(budget===0)status.innerHTML='<strong>総容量ゼロ：過渡核の観測値もゼロ。</strong>内部状態を置かず、直接伝導だけで定常結合κ=1を実現します。';
else if(v.exact)status.innerHTML='<strong>上下が一致：この値が全回路の厳密な最適値です。</strong>状態数の上限を増やしても、同じ総容量では改善できません。有限の1状態で達成しています。';
else if(k===1)status.innerHTML='<strong>k=1では、緑の値が厳密な最適値です。</strong>橙色は二つの一般上界を合わせた値で、緑と一致する場合と差が残る場合があります。1状態の最適化は別途、厳密に解いています。';
else if(budget>=5&&k>=2)status.innerHTML='<strong>この予算では、別掲の2状態例が1状態を上回ります。</strong>2状態の達成値は約0.097555。下の緑線は1状態の値であり、全回路の最適値ではありません。全回路の最適値と橙色の上界の一致は未確定です。';
else status.innerHTML='<strong>ここでは、達成値と保証上界の間に差があります。</strong>1状態よりよい回路が存在するか、上界まで近づけるかは、この二つの式だけでは決まりません。';
$('round10-star-caption').textContent=budget===0?'容量ゼロでは、この内部枝を置かない':'この達成値は1個で作れる';$('round10-star').setAttribute('aria-label',budget===0?'内部容量を置かず、伝導係数1で両端子を直接結ぶ。':`内部容量${f(v.star.capacity,5)}、左右それぞれの伝導係数${f(v.star.spoke,5)}、直接伝導係数${f(v.star.direct,5)}の有限回路。`);
$('round10-design-note').textContent=budget===0?'内部状態なし、直接伝導係数d=1。':'緩和率λ='+f(v.star.rate,5)+'、使用容量 '+f(v.star.capacity,5)+' ≤ 予算 '+f(budget,2)+'。全て有限の部品値です。';draw(v);
}
$('round10-budget').addEventListener('input',update);$('round10-k').addEventListener('input',update);let resizeFrame;window.addEventListener('resize',()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(update);});
$('round10-example-button').addEventListener('click',()=>{$('round10-budget').value='5';$('round10-k').value='2';update();$('round10-lab').scrollIntoView({behavior:'smooth',block:'start'});});
window.Round10Lab={q,capacityRate,stateBound,oneState,values,update,constants:{a,b,kappa,mu,lambdaC,G,critical}};update();
})();
