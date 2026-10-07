
(()=>{'use strict';
const $=id=>document.getElementById(id),alpha=Math.exp(-.1)*(-Math.expm1(-.1)/.1)**2*(-Math.expm1(-1))**2;
const F=x=>x/Math.expm1(x),deriv=x=>-.1*x+2*F(.1*x)+2*F(x)-3;
let lo=.01,hi=10;for(let i=0;i<90;i++){const mid=(lo+hi)/2;if(deriv(mid)>0)lo=mid;else hi=mid;}
const xstar=(lo+hi)/2,gamma=Math.exp(-.1*xstar)*(-Math.expm1(-.1*xstar)/(.1*xstar))**2*(-Math.expm1(-xstar))**2/xstar;
const minCount=(n,e)=>Math.ceil(n*n*Math.max(0,alpha-e)/gamma);
function values(){return {n:+$('round8-n').value,e:alpha*Number($('round8-eps').value),r:+$('round8-r').value};}
function update(reset=false){let {n,e,r}=values();const m=n*n,need=minCount(n,e);$('round8-r').max=m;if(reset)r=need;r=Math.max(0,Math.min(m,r));$('round8-r').value=r;
$('round8-n-out').textContent=n;$('round8-eps-out').textContent=e.toFixed(4);$('round8-r-out').textContent=r;$('round8-old').textContent=Math.ceil(m*Math.max(0,alpha-e));$('round8-min').textContent=need;$('round8-full').textContent=m;
const cell=300/n,gap=Math.min(2,cell*.14);let squares='';for(let i=0;i<m;i++){const x=10+(i%n)*cell,y=10+Math.floor(i/n)*cell;squares+=`<rect x="${x}" y="${y}" width="${cell-gap}" height="${cell-gap}" rx="${Math.min(2,cell*.1)}" fill="${i<r?'#0a7166':'#dce4da'}"/>`;}
$('round8-edge-grid').innerHTML=squares;$('round8-edge-grid').setAttribute('aria-label',`${m}の左右ペアのうち${r}ペアに一つずつ容量を配置`);
const capacity=r*gamma/m,lower=Math.max(0,alpha-e),axisMax=Math.max(gamma,alpha+e)+.025,chartWidth=window.innerWidth<=650?340:700,plotRight=chartWidth-30,plotWidth=plotRight-85,X=v=>85+v/axisMax*plotWidth,ok=r>=need;
$('round8-signal-bar').setAttribute('viewBox',`0 0 ${chartWidth} 155`);
$('round8-signal-bar').innerHTML=`<rect x="85" y="31" width="${plotWidth}" height="87" rx="5" fill="#e5eadf"/><rect x="${X(lower)}" y="31" width="${X(alpha+e)-X(lower)}" height="87" fill="#d4c296" opacity=".55"/><text x="12" y="55" font-size="13" fill="#183b40">許容範囲</text><path d="M${X(lower)} 62V39H${X(alpha+e)}V62" stroke="#9a7740" stroke-width="2" fill="none"/><text x="12" y="100" font-size="13" fill="#183b40">作れる範囲</text><rect x="85" y="81" width="${Math.max(0,X(capacity)-85)}" height="25" fill="${ok?'#0a7166':'#ab4f2e'}"/><path d="M${X(alpha)} 26V122" stroke="#183b40" stroke-width="1.5" stroke-dasharray="4 3"/><text x="${X(alpha)}" y="18" text-anchor="middle" font-size="12" fill="#183b40">目標 α</text><text x="85" y="141" font-size="12" fill="#596e6c">0</text><text x="${plotRight}" y="141" text-anchor="end" font-size="12" fill="#596e6c">信号 d/c₀</text>`;
$('round8-signal-bar').setAttribute('aria-label',`信号の許容範囲は${lower.toFixed(5)}から${(alpha+e).toFixed(5)}。${r}容量で作れる範囲は0から${capacity.toFixed(5)}。`);
$('round8-verdict').classList.toggle('inconclusive',!ok);$('round8-verdict').textContent=ok?(need===0?'容量0個でも、許容範囲に入ります。':`${r}個の予算で条件を満たす模型を作れます。最少は${need}個です。`):`${r}個では届きません。少なくともあと${need-r}個必要です。`;
$('round8-live-note').textContent=`許容範囲の下端は ${lower.toFixed(6)}。${r}個での到達上限は ${capacity.toFixed(6)}。${ok?'必要なペアだけに容量を置き、最後のペアを調整して下端に合わせます。':'内部接続や緩和率を変えても、この到達上限を超えられません。'} 定常応答Kはすべて厳密に保存します。`;
}
['round8-n','round8-eps'].forEach(id=>$(id).addEventListener('input',()=>update(true)));$('round8-r').addEventListener('input',()=>update(false));$('round8-min-button').addEventListener('click',()=>update(true));$('round8-below-button').addEventListener('click',()=>{const {n,e}=values();$('round8-r').value=Math.max(0,minCount(n,e)-1);update();});
document.querySelectorAll('[data-round8-eps]').forEach(button=>button.addEventListener('click',()=>{$('round8-eps').value=button.dataset.round8Eps==='signal'?1:Number(button.dataset.round8Eps)/alpha;update(true);}));
$('round8-eps').value=String(.05/alpha);
window.addEventListener('resize',()=>update(false));
window.Round8Lab={alpha,gamma,xstar,minCount,update};update(true);
})();
