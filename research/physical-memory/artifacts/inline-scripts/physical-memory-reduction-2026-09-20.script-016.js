(()=>{'use strict';
 const $=id=>document.getElementById(id), alpha=Math.exp(-.1)*(-Math.expm1(-.1)/.1)**2*(-Math.expm1(-1))**2;
 const bound=(n,e,b)=>n*n*Math.max(0,alpha-e)/(1+n*b);
 function update(){
  const n=+$('theory-n').value,e=+$('theory-eps').value,b=+$('theory-static').value,lower=bound(n,e,b);
  $('theory-n-out').textContent=n;$('theory-eps-out').textContent=e.toFixed(3);$('theory-static-out').textContent=b.toFixed(3);
  $('theory-linear').textContent=2*n-1;$('theory-exact').textContent=n*n;
  $('theory-lower').textContent=lower>0?Math.ceil(lower-1e-10)+'個以上':'判定保留';
  $('theory-note').textContent=lower>0?`α ≈ ${alpha.toFixed(6)}。この測定からの下界は ${lower.toFixed(3)}。${b===0?'定常応答を厳密保存すると、同じ条件のままn²に比例して増えます。':'定常の交差結合に追加の幅を許すと、この下界は弱まります。'}通常次数は全応答の厳密再現に対する値で、この集団測定だけから推定した次数ではありません。`:'許容誤差が集団信号以上になり、この測定から正の下界は出せません。';
  const maxN=60,maxY=3600,X=k=>48+(k-2)/58*376,Y=v=>250-v/maxY*210;
  const path=fn=>Array.from({length:59},(_,i)=>`${i?'L':'M'}${X(i+2).toFixed(2)},${Y(fn(i+2)).toFixed(2)}`).join(' ');
  $('theory-plot').innerHTML=`<svg viewBox="0 0 460 294" aria-hidden="true"><text x="48" y="19" font-size="12">内部状態数</text>${[0,1200,2400,3600].map(v=>`<path d="M48 ${Y(v)}H424" stroke="#d5ded5"/><text x="40" y="${Y(v)+4}" text-anchor="end" font-size="11">${v}</text>`).join('')}<path d="${path(k=>k*k)}" fill="none" stroke="#a98a47" stroke-width="2" stroke-dasharray="5 4"/><path d="${path(k=>bound(k,e,b))}" fill="none" stroke="#0a7166" stroke-width="3"/><path d="${path(k=>2*k-1)}" fill="none" stroke="#ab4f2e" stroke-width="2"/><path d="M${X(n)} 35V250" stroke="#667c71" stroke-dasharray="2 4"/><circle cx="${X(n)}" cy="${Y(lower)}" r="4" fill="#0a7166"/>${[2,20,40,60].map(v=>`<text x="${X(v)}" y="269" text-anchor="middle" font-size="11">${v}</text>`).join('')}<text x="235" y="288" text-anchor="middle" font-size="12">各側の境界数 n</text></svg>`;
 }
 for(const id of ['theory-n','theory-eps','theory-static'])$(id).addEventListener('input',update);
 window.Round7Lab={alpha,bound};update();
})();
