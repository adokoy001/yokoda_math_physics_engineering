
(function(){'use strict';
const $=id=>document.getElementById(id), root=$('round9-kernel');if(!root)return;
function logFactorial(n){let s=0;for(let j=2;j<=n;j++)s+=Math.log(j);return s;}
function constant(k){return Math.exp(k*Math.log(k)+1-k-logFactorial(k-1));}
function density(k,t){if(t===0)return k===1?1:0;return Math.exp(k*Math.log(k)+(k-1)*Math.log(t)-k*t-logFactorial(k-1));}
function survival(k,t){const x=k*t;let term=1,sum=1;for(let j=1;j<k;j++){term*=x/j;sum+=term;}return Math.exp(-x)*sum;}
function values(k,width){const a=1-width/2,b=1+width/2,mu=Math.log(b/a)/(b-a),q=Math.exp(-mu*a)*(-Math.expm1(-mu*(b-a))),p=Math.max(0,survival(k,a)-survival(k,b));return {a,b,mu,q,p,c:constant(k),ratio:p/q};}
function update(){const k=+$('round9-k').value,width=+$('round9-width').value,v=values(k,width);$('round9-k-out').textContent=k;$('round9-width-out').textContent=width.toFixed(2);$('round9-ratio').textContent=v.ratio.toFixed(4);$('round9-constant').textContent=v.c.toFixed(4);
const chart=$('round9-density-chart'),rect=chart.getBoundingClientRect(),W=Math.max(260,Math.min(820,rect.width||760)),H=W<420?275:310,L=39,R=W-12,T=28,B=H-34, ymax=v.c*1.06,X=t=>L+t/2.4*(R-L),Y=y=>B-y/ymax*(B-T);chart.setAttribute('viewBox',`0 0 ${W} ${H}`);
let svg=`<rect x="${X(v.a)}" y="${T}" width="${X(v.b)-X(v.a)}" height="${B-T}" fill="#d8c28b" opacity=".30"/><text x="${X(1)}" y="17" text-anchor="middle" font-size="12" fill="#725b2e">測定窓</text>`;
for(let j=0;j<=4;j++){const y=ymax*j/4;svg+=`<path d="M${L} ${Y(y)}H${R}" stroke="#d8dfd4" stroke-width="1"/><text x="${L-7}" y="${Y(y)+4}" text-anchor="end" font-size="11" fill="#596e6c">${y.toFixed(1)}</text>`;}
const ticks=W<420?[0,1,2]:[0,.5,1,1.5,2];for(const t of ticks)svg+=`<path d="M${X(t)} ${B}v4" stroke="#7a8880"/><text x="${X(t)}" y="${B+19}" text-anchor="middle" font-size="11" fill="#596e6c">${t}</text>`;
svg+=`<path d="M${L} ${T}V${B}H${R}" stroke="#7a8880" fill="none"/><text x="${L}" y="16" font-size="11" fill="#596e6c">密度</text><text x="${R}" y="${H-2}" text-anchor="end" font-size="11" fill="#596e6c">時間 t</text>`;
function path(fn){let p='';for(let j=0;j<=480;j++){const t=2.4*j/480;p+=(j?'L':'M')+X(t).toFixed(2)+' '+Y(fn(t)).toFixed(2);}return p;}
svg+=`<path d="${path(t=>v.c*Math.exp(-t))}" fill="none" stroke="#ab4f2e" stroke-width="2" stroke-dasharray="6 4"/><path d="${path(t=>Math.exp(-t))}" fill="none" stroke="#7a8880" stroke-width="2"/><path d="${path(t=>density(k,t))}" fill="none" stroke="#0a7166" stroke-width="2.6"/><circle cx="${X(1)}" cy="${Y(v.c/Math.E)}" r="3.5" fill="#0a7166"/>`;chart.innerHTML=svg;
chart.setAttribute('aria-label',`${k}段のErlang極限密度。時間${v.a.toFixed(2)}から${v.b.toFixed(2)}の窓内応答は、最適な1状態の${v.ratio.toFixed(4)}倍。普遍上限は${v.c.toFixed(4)}倍。`);
$('round9-readout').textContent=`この窓での極限応答は ${v.p.toFixed(5)}、最適な1状態は ${v.q.toFixed(5)}（率 μ=${v.mu.toFixed(4)}）。上限の ${(100*v.ratio/v.c).toFixed(2)}% まで近づいています。${k===1?'1状態でも、窓に最適な率は幅によって少し変わります。':'窓を狭めると、比は Cₖ に近づきます。'}`;
}
$('round9-k').addEventListener('input',update);$('round9-width').addEventListener('input',update);let frame;window.addEventListener('resize',()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(update);});window.Round9KernelLab={constant,density,survival,values,update};update();
})();
