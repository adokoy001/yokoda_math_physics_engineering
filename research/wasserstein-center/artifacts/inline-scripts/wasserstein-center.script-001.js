
'use strict';
/* Pure numerical and SVG routines. The same code is embedded in the HTML. */
const MathNote = (() => {
  const C={ink:'#182c3b',muted:'#64757c',line:'#d9dfdc',teal:'#087e83',orange:'#bd502e',purple:'#77659a',paper:'#fffdf8'};
  const fmt=(x,n=4)=>Number(x).toFixed(n);
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function params(mu,s){
    const M=mu*(1-mu),v=M*s;
    if(s===0) return {mu,s,M,v,k:0,L:Infinity,a:0,b:1,xm:mu,xp:mu,xL:mu,xR:mu,r2:0};
    if(s===1) return {mu,s,M,v,k:1,L:0,a:1-mu,b:1-mu,xm:0,xp:1,xL:.5,xR:.5,r2:0};
    const L=-Math.log(s),k=2/(2+L),a=v/(mu*mu+v),b=(1-mu)**2/((1-mu)**2+v);
    return {mu,s,M,v,L,k,a,b,xm:(1-k)*mu,xp:mu+k*(1-mu),xL:mu+k*(v-mu*mu)/(2*mu),xR:mu+k*((1-mu)**2-v)/(2*(1-mu)),r2:v*(L/(2+L))};
  }
  function fc(u,t){
    if(t.s===0) return t.mu;
    if(t.s===1) return u<1-t.mu?0:1;
    if(u<t.a) return t.xm;
    if(u>t.b) return t.xp;
    return t.mu+t.k*Math.sqrt(t.v)*(2*u-1)/(2*Math.sqrt(u*(1-u)));
  }
  function centerParts(t){
    if(t.s===0) return [[[0,t.mu],[1,t.mu]]];
    if(t.s===1) return [[[0,0],[1-t.mu,0]],[[1-t.mu,1],[1,1]]];
    return [[[0,t.xm],[t.a,t.xm]],Array.from({length:151},(_,i)=>{const u=t.a+(t.b-t.a)*i/150;const x=t.mu+t.k*Math.sqrt(t.v)*(2*u-1)/(2*Math.sqrt(u*(1-u)));return [u,x];}),[[t.b,t.xp],[1,t.xp]]];
  }
  function witness(t,kind='two'){
    if(t.s===0) return [{x:t.mu,w:1}];
    if(t.s===1) return [{x:0,w:1-t.mu},{x:1,w:t.mu}];
    if(kind==='three'){
      const D=t.M-t.v,c=(D/(1-t.mu)+1-D/t.mu)/2;
      return [{x:0,w:1-t.mu-D/c},{x:c,w:D/(c*(1-c))},{x:1,w:t.mu-D/(1-c)}];
    }
    const p=(t.a+t.b)/2;
    return [{x:t.mu-Math.sqrt(t.v*(1-p)/p),w:p},{x:t.mu+Math.sqrt(t.v*p/(1-p)),w:1-p}];
  }
  function discreteParts(law){let u=0;return law.map(d=>{const out=[[u,d.x],[u+d.w,d.x]];u+=d.w;return out;});}
  const path=(arr,X,Y)=>arr.map((p,i)=>(i?'L':'M')+fmt(X(p[0]),2)+','+fmt(Y(p[1]),2)).join(' ');
  const txt=(x,y,s,extra='')=>`<text x="${x}" y="${y}" ${extra}>${esc(s)}</text>`;
  function axes(w,h,ymax=1,ylabel='値 x',xlabel='下からの割合 u'){
    const l=55,r=w-22,top=34,bot=h-46,X=u=>l+(r-l)*u,Y=x=>bot-(bot-top)*x/ymax;
    let out='';
    for(let i=0;i<=4;i++){
      const u=i/4;
      out+=`<path d="M${l} ${Y(u*ymax)}H${r}" stroke="${C.line}"/>`+txt(l-10,Y(u*ymax)+4,fmt(u*ymax,ymax<.1?3:2),'text-anchor="end"');
      out+=txt(X(u),bot+23,fmt(u,2),'text-anchor="middle"');
    }
    out+=txt(l,17,ylabel,`fill="${C.ink}"`)+txt(r,h-4,xlabel,'text-anchor="end"');
    return {X,Y,out,l,r,top,bot};
  }
  function quantile(t,kind='two',hero=false){
    const w=620,h=350,{X,Y,out}=axes(w,h),parts=centerParts(t);
    let lines='';
    if(hero){
      for(let i=0;i<=8;i++){
        const p=t.a+(t.b-t.a)*i/8;
        const lo=t.mu-Math.sqrt(t.v*(1-p)/p),hi=t.mu+Math.sqrt(t.v*p/(1-p));
        lines+=`<path d="${path([[0,lo],[p,lo],[p,hi],[1,hi]],X,Y)}" fill="none" stroke="${C.ink}" stroke-width="1.3" opacity=".16"/>`;
      }
    } else {
      const wp=discreteParts(witness(t,kind));
      wp.forEach((p,i)=>{
        lines+=`<path d="${path(p,X,Y)}" fill="none" stroke="${C.orange}" stroke-width="2.4" stroke-dasharray="8 5"/>`;
        if(i) lines+=`<path d="${path([wp[i-1][1],p[0]],X,Y)}" stroke="${C.orange}" stroke-width="1.4" stroke-dasharray="2 5"/>`;
      });
    }
    parts.forEach((p,i)=>{
      if(i) lines+=`<path d="${path([parts[i-1].at(-1),p[0]],X,Y)}" stroke="${C.teal}" stroke-width="1.3" stroke-dasharray="2 5"/>`;
      lines+=`<path d="${path(p,X,Y)}" fill="none" stroke="${C.teal}" stroke-width="4" stroke-linecap="round"/>`;
    });
    return `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${hero?'平均0.5・分散0.125の二点入力族と最適中心の分位関数':'最適中心と最遠入力の分位関数。数値は続く表に掲載'}" xmlns="http://www.w3.org/2000/svg"><g font-family="system-ui,sans-serif" font-size="12" fill="${C.muted}">${out}${lines}</g></svg>`;
  }
  function radius(t){
    const w=620,h=350,max=.4*Math.sqrt(t.M),{X,Y,out}=axes(w,h,max,'最悪の W₂ 誤差 R','分散 / 最大分散  s');
    const ps=Array.from({length:301},(_,i)=>{const s=i/300;return [s,Math.sqrt(params(t.mu,s).r2)];});
    const line=path(ps,X,Y),area=line+` L${X(1)} ${Y(0)} L${X(0)} ${Y(0)} Z`;
    return `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="平均を固定し、分散を変えたときの最適半径。分散が0と最大値では半径0" xmlns="http://www.w3.org/2000/svg"><g font-family="system-ui,sans-serif" font-size="12" fill="${C.muted}">${out}<path d="${area}" fill="${C.teal}" opacity=".07"/><path d="${line}" fill="none" stroke="${C.teal}" stroke-width="3"/><path d="M${X(t.s)} ${Y(0)}V${Y(Math.sqrt(t.r2))}" stroke="${C.orange}" stroke-dasharray="4 4"/><circle cx="${X(t.s)}" cy="${Y(Math.sqrt(t.r2))}" r="6" fill="${C.orange}" stroke="${C.paper}" stroke-width="2"/></g></svg>`;
  }
  function envelope(){
    const t=params(.5,.5),w=650,h=300,{X,Y,out}=axes(w,h,.27,'積分分位 K(u)','下からの割合 u');
    const H=u=>Math.min(t.mu*u,(1-t.mu)*(1-u),Math.sqrt(t.v*u*(1-u)));
    let lines='';
    const curves=[{fn:u=>t.mu*u,col:C.purple},{fn:u=>(1-t.mu)*(1-u),col:C.orange},{fn:u=>Math.sqrt(t.v*u*(1-u)),col:'#7d9daa'}];
    const pts=fn=>Array.from({length:201},(_,i)=>[i/200,Math.min(.27,fn(i/200))]);
    curves.forEach(o=>{const p=Array.from({length:401},(_,i)=>[i/400,o.fn(i/400)]).filter(p=>p[1]<=.27);lines+=`<path d="${path(p,X,Y)}" fill="none" stroke="${o.col}" stroke-width="1.5" stroke-dasharray="5 5"/>`;});
    for(const p of [.36,.5,.64]){
      const lo=-Math.sqrt(t.v*(1-p)/p),hi=Math.sqrt(t.v*p/(1-p));
      lines+=`<path d="${path([[0,0],[p,-p*lo],[1,0]],X,Y)}" fill="none" stroke="${C.ink}" stroke-width="1.3" opacity=".3"/>`;
    }
    lines+=`<path d="${path(pts(H),X,Y)}" fill="none" stroke="${C.teal}" stroke-width="4"/>`;
    return `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="3つの上界の最小値が包絡Hになる。μ=0.5、v=0.125。3つの二点分布の積分分位はすべてH以下" xmlns="http://www.w3.org/2000/svg"><g font-family="system-ui,sans-serif" font-size="12" fill="${C.muted}">${out}${lines}</g></svg>`;
  }
  function state(t){
    let rows;
    if(t.s===0) rows=[['一点の確率',fmt(t.mu),'100%']];
    else rows=[['左の点の確率',fmt(t.xm),fmt(100*t.a,2)+'%'],['連続部分の確率',t.s===1?'なし':fmt(t.xL)+' 〜 '+fmt(t.xR),fmt(100*(t.b-t.a),2)+'%'],['右の点の確率',fmt(t.xp),fmt(100*(1-t.b),2)+'%']];
    const table=rows.map(row=>'<tr>'+row.map((s,i)=>i?`<td>${esc(s)}</td>`:`<th scope="row">${esc(s)}</th>`).join('')+'</tr>').join('');
    const masses=t.s===0?[1,0,0]:[t.a,t.b-t.a,1-t.b];
    const bar=masses.map((p,i)=>`<span class="mass-${i}" style="width:${p*100}%">${p>.12?fmt(p*100,1)+'%':''}</span>`).join('');
    const note=t.s===0?'分散が0なら、すべての値が平均と一致します。入力も中心も一点分布で、誤差は0です。':t.s===1?'最大分散では、入力は0と1だけを取る分布に一意に決まります。中心も同じ分布で、誤差は0です。':'分位図の水平な部分は点に集中する確率、中央の増加部分は連続成分です。点線の縦の跳びの間には、中心の確率はありません。';
    return {table,bar,note,mu:fmt(t.mu,2),s:fmt(t.s,2),v:fmt(t.v,6),k:fmt(t.k,6),r:fmt(Math.sqrt(t.r2),6),r2:fmt(t.r2,6),cv:fmt(t.k*t.v,6)};
  }
  return {params,fc,centerParts,witness,quantile,radius,envelope,state,fmt};
})();
if(typeof module!=='undefined'&&module.exports) module.exports=MathNote;

(() => {
  const byId=id=>document.getElementById(id);
  const mu=byId('mu'),share=byId('share');
  let timer;
  function update(announce=true){
    const t=MathNote.params(Number(mu.value),Number(share.value)),s=MathNote.state(t);
    const kind=document.querySelector('input[name="witness"]:checked').value;
    for(const [id,key] of [['mu-out','mu'],['share-out','s'],['v-out','v'],['r-out','r'],['cv-out','cv'],['k-out','k']])byId(id).textContent=s[key];
    mu.setAttribute('aria-valuetext','平均 '+s.mu);
    share.setAttribute('aria-valuetext','最大分散の '+MathNote.fmt(t.s*100,0)+'%、分散 '+s.v);
    byId('quantile-chart').innerHTML=MathNote.quantile(t,kind);
    byId('radius-chart').innerHTML=MathNote.radius(t);
    byId('center-table').innerHTML=s.table;
    byId('mass-bar').innerHTML=s.bar;
    byId('quantile-caption').textContent=s.note;
    if(announce){clearTimeout(timer);timer=setTimeout(()=>{byId('live-state').textContent='平均 '+s.mu+'、分散 '+s.v+'。最悪の距離は '+s.r+'。中心の分散は '+s.cv+'。';},180);}
  }
  mu.disabled=false;share.disabled=false;
  mu.addEventListener('input',()=>update());share.addEventListener('input',()=>update());
  document.querySelectorAll('input[name="witness"]').forEach(input=>{input.disabled=false;input.addEventListener('change',()=>update());});
  update(false);
  const print=byId('print-page');print.disabled=false;
  let oldDetails=null;
  function openForPrint(){if(oldDetails===null){oldDetails=Array.from(document.querySelectorAll('details')).map(el=>[el,el.open]);oldDetails.forEach(([el])=>el.open=true);}}
  function restoreDetails(){if(oldDetails){oldDetails.forEach(([el,opened])=>el.open=opened);oldDetails=null;}}
  window.addEventListener('beforeprint',openForPrint);window.addEventListener('afterprint',restoreDetails);
  print.addEventListener('click',()=>{openForPrint();window.print();});
})();
