(() => {
 'use strict';
 const $ = id => document.getElementById(id);
 const num = id => Number($(id).value);
 const put = (id, s) => { $(id).textContent = s; };
 const pct = (x, digits=0) => (100*x).toFixed(digits) + '%';
 const fmt = (x,d=4) => x.toFixed(d);
 const teal='#087f80',dark='#006668',ink='#193135',muted='#576a6d',warm='#ae6339';
 const text = (x,y,s,cls='chart-label',extra='') => `<text x="${x}" y="${y}" class="${cls}" ${extra}>${s}</text>`;
 const line = (x1,y1,x2,y2,extra='') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" ${extra}/>`;
 const title = s => `<title>${s}</title>`;
 let cycleState=0;
 const cycleCoords=[[100,76],[300,76],[300,266],[100,266]];
 function drawCycle(reset=true){
  if(reset)cycleState=0;
  const e=num('epsilon'),d=num('spread'),g=num('gamma'),gain=e*d,q=e*(2+d),safe=g+1e-12>=gain;
  put('epsilon-out',fmt(e,2));put('spread-out',fmt(d,2));put('gamma-out',fmt(g));put('margin-critical',fmt(gain));
  $('cycle-step').disabled=safe;
  const arrowColor=safe?'#a5b5ad':teal,stroke=`stroke="${arrowColor}" stroke-width="2.5" ${safe?'stroke-dasharray="7 5"':''} marker-end="url(#cycle-arrow)"`;
  let s=title(`各変更の利益は${fmt(gain)}、閾値は${fmt(g)}。${safe?'全変更が閾値以下。':'４つの変更を繰り返せる。'}`);
  s+=`<defs><marker id="cycle-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7" fill="${arrowColor}"/></marker></defs>`;
  s+=line(162,76,230,76,stroke)+line(300,115,300,221,stroke)+line(238,266,170,266,stroke)+line(100,227,100,121,stroke);
  s+=text(200,23,`i : +${fmt(gain)}`,'chart-label','text-anchor="middle"');
  s+=text(312,164,"j",'chart-label')+text(312,185,`+${fmt(gain)}`,'chart-label');
  s+=text(200,328,`i : +${fmt(gain)}`,'chart-label','text-anchor="middle"');
  s+=text(88,164,"j",'chart-label','text-anchor="end"')+text(88,185,`+${fmt(gain)}`,'chart-label','text-anchor="end"');
  const states=['00','10','11','01'];
  cycleCoords.forEach(([x,y],idx)=>{const even=idx%2===0;
   s+=`<rect x="${x-60}" y="${y-37}" width="120" height="74" rx="12" fill="${cycleState===idx?'#e6f4ef':'#f7f9f5'}" stroke="${cycleState===idx?teal:'#c3d2ca'}" stroke-width="${cycleState===idx?3:1.3}"/>`;
   s+=text(x,y-10,states[idx],'chart-value','text-anchor="middle"');
   s+=text(x,y+10,`h = ${even?'+':'−'}${fmt(e,2)}`,'chart-label','text-anchor="middle" style="font-size:14px"');
   s+=text(x,y+27,`Φ = ${even?'0':fmt(q)}`,'chart-label','text-anchor="middle" style="font-size:14px"');
  });
  s+=text(200,372,`aᵢ = 1　　aⱼ = ${fmt(1+d,2)}`,'chart-label','text-anchor="middle" style="font-size:15px"');
  $('cycle-svg').innerHTML=s;
  $('cycle-status').classList.toggle('safe',safe);
  put('cycle-status',safe?`保証あり：γ ≥ γ*。等号でも安全です。この４状態例では、利益 ${fmt(gain)} が閾値を厳密に超えないため、矢印は進めません。`:`循環する反例を構成可能：各手の利益 ${fmt(gain)} > γ = ${fmt(g)}。自分にとっての改善を４回続けると、元の状態に戻ります。`);
 }
 ['epsilon','spread','gamma'].forEach(id=>$(id).addEventListener('input',()=>drawCycle()));
 $('set-boundary').addEventListener('click',()=>{$('gamma').value=fmt(num('epsilon')*num('spread'));drawCycle();});
 $('cycle-step').addEventListener('click',()=>{cycleState=(cycleState+1)%4;drawCycle(false);});
 const schedules=[[1,2,3],[1,4,5],[2,4,5],[3,4,5]];
 const pairValue=(i,j)=>schedules.filter(a=>a.includes(i)&&a.includes(j)).length/4;
 function drawAudit(changed='query-target'){
  let i=num('query-target'),j=num('other-target');
  if(i===j){if(changed==='query-target'){j=i%5+1;$('other-target').value=j;}else{i=j%5+1;$('query-target').value=i;}}
  put('attack-rule',`対象 ${i} を観察 → 監査なしなら ${i} を攻撃 ／ 監査ありなら ${j} を攻撃`);
  let rows='',count=0;
  schedules.forEach(a=>{const inspected=a.includes(i),attack=inspected?j:i,hit=a.includes(attack);if(hit)count++;
   const dots=[1,2,3,4,5].map(x=>`<span class="target-dot ${a.includes(x)?'on':''} ${x===attack?'attacked':''}" title="対象${x}：${a.includes(x)?'監査あり':'監査なし'}${x===attack?'、攻撃先':''}">${x}</span>`).join('');
   rows+=`<tr><td><div class="target-dots" aria-label="監査対象 ${a.join('・')}。攻撃先 ${attack}">${dots}</div></td><td>${inspected?'あり':'なし'}</td><td>対象 ${attack}</td><td><span class="${hit?'detected-label':'miss-label'}">${hit?'● 検出':'− 回避'}</span></td></tr>`;
  });
  $('schedule-rows').innerHTML=rows;put('attack-value',pct(count/4));put('attack-count',`４予定中${count}予定で検出`);
  let grid='<table class="pair-table" aria-label="攻撃ペア別の検出率。行は観察対象、列は監査あり時の攻撃対象"><thead><tr><th>i / j</th>';
  for(let y=1;y<=5;y++)grid+=`<th scope="col">${y}</th>`;grid+='</tr></thead><tbody>';
  for(let x=1;x<=5;x++){grid+=`<tr><th scope="row">${x}</th>`;for(let y=1;y<=5;y++){
   grid+=x===y?'<td>—</td>':`<td><button type="button" data-i="${x}" data-j="${y}" class="${pairValue(x,y)>.25?'high':''} ${x===i&&y===j?'selected':''}" aria-label="${x}を観察、監査ありなら${y}を攻撃：検出率${pct(pairValue(x,y))}" aria-pressed="${x===i&&y===j}">${pct(pairValue(x,y))}</button></td>`;
  }grid+='</tr>';}
  $('pair-grid').innerHTML=grid+'</tbody></table>';
 }
 ['query-target','other-target'].forEach(id=>$(id).addEventListener('change',()=>drawAudit(id)));
 $('pair-grid').addEventListener('click',ev=>{const b=ev.target.closest('button[data-i]');if(!b)return;$('query-target').value=b.dataset.i;$('other-target').value=b.dataset.j;drawAudit();});
 function drawSupport(){
  const m=num('support-count'),vals=[0,0,0,.25,.25,.25,.25,.25,.25,.3];put('support-count-out',m);
  let s=title('５対象・３監査の厳密な最適値。１〜３種類は０％、４〜９種類は25％、10種類は30％。');
  const x=i=>90+64*i,y=v=>268-v*650;
  for(const t of [0,.1,.2,.3])s+=line(57,y(t),744,y(t),'class="chart-grid"')+text(61,y(t)+6,pct(t),'chart-label','text-anchor="end" style="font-size:23px"');
  s+=text(57,25,'最適検出率','chart-label','style="font-size:24px"');
  vals.forEach((v,idx)=>{const active=idx+1===m;
   s+=`<rect x="${x(idx)-22}" y="${y(v)}" width="44" height="${v?268-y(v):3}" rx="4" fill="${idx===9?ink:teal}" opacity="${active?1:.35}"/>`;
   if(active)s+=`<rect x="${x(idx)-27}" y="${y(v)-7}" width="54" height="${268-y(v)+15}" rx="7" fill="none" stroke="${ink}" stroke-width="1.6"/>`;
   if([1,5,9].includes(idx))s+=text(x(idx),y(v)-16,pct(v),'chart-value','text-anchor="middle" style="font-size:27px"');
   s+=text(x(idx),294,idx+1,'chart-label',`text-anchor="middle" style="font-weight:${active?800:400};font-size:25px"`);
  });
  s+=text(420,328,'パターン数の上限 m','chart-label','text-anchor="middle" style="font-size:24px"');$('support-chart').innerHTML=s;
  const msg=m<=3?`${m}種類まででは 0％。どの予定を選んでも、１ビットの観察を使って検出を避ける攻撃が存在します。`:m<=9?`${m}種類までなら最適値は25％。４種類の構成で達成でき、全10種類のうち１つでも欠けると25％が上界です。`:'全10種類を使えると30％。10予定を一様に選ぶことで、どの対象ペアも30％の確率で同時に監査されます。';
  put('support-comment',msg);$('support-comment').classList.toggle('safe',m>=4);
 }
 $('support-count').addEventListener('input',drawSupport);
 const capped=(n,rho)=>(n-3)*(n-4+2*rho)/(n*n-3*n-2);
 function drawCap(){
  const n=num('target-count'),f=num('cap-fraction')/100,N=n*(n-1)/2,r=n-2,rho=f/N,T=capped(n,rho),F=1-4/n+rho,alpha=(n-2)*(n-3)/(n*(n-1));
  put('target-count-out',n);put('cap-fraction-out',pct(f));put('cap-model',`${n}対象のうち ${n-2} 対象を監査 ／ 全 ${N} 予定 ／ 指定予定の上限 ρ = ${pct(rho,3)}（一様分布では ${pct(1/N,3)}）`);
  put('cap-value',pct(T,2));put('cap-fair',pct(F,2));put('cap-gap',`制約なしの最適値 ${pct(alpha,2)}。個別監査率を自由にする改善幅は ${((T-F)*100).toFixed(2)} ポイント。`);
  const x=t=>65+570*t,y=v=>277-(v/(Math.ceil((alpha+.025)*10)/10))*226;
  const ymax=Math.ceil((alpha+.025)*10)/10;
  let s=title(`${n}対象の監査。確率上限の割合が${pct(f)}のとき、最適値${pct(T,2)}、個別監査率均一なら${pct(F,2)}。`);
  for(let tick=0;tick<=Math.round(ymax*10);tick++){const v=tick/10;s+=line(65,y(v),635,y(v),'class="chart-grid"')+text(55,y(v)+6,pct(v),'chart-label','text-anchor="end" style="font-size:21px"');}
  s+=text(65,26,'最適検出率','chart-label','style="font-size:23px"');
  for(const t of [0,.25,.5,.75,1])s+=text(x(t),306,pct(t),'chart-label','text-anchor="middle" style="font-size:22px"');
  s+=`<path d="M${x(0)},${y(capped(n,0))} L${x(1)},${y(alpha)} L${x(0)},${y(1-4/n)} Z" fill="#e9f3ec"/>`;
  s+=line(x(0),y(capped(n,0)),x(1),y(alpha),`stroke="${teal}" stroke-width="3.5"`);
  s+=line(x(0),y(1-4/n),x(1),y(alpha),`stroke="${warm}" stroke-width="2.6" stroke-dasharray="7 5"`);
  s+=line(x(f),48,x(f),277,'stroke="#6b8079" stroke-width="1" stroke-dasharray="3 5"');
  s+=`<circle cx="${x(f)}" cy="${y(T)}" r="6.5" fill="${teal}" stroke="white" stroke-width="2"/><rect x="${x(f)-4.5}" y="${y(F)-4.5}" width="9" height="9" fill="${warm}" stroke="white" stroke-width="1.3"/>`;
  s+=text(350,341,'指定予定の上限 / 一様分布での確率','chart-label','text-anchor="middle" style="font-size:21px"');$('cap-chart').innerHTML=s;
  const u=(1-rho-T)/(2*r),v=2*T/(r*(r-1));
  const groups=[['指定ペア {1,2}',1,rho],['{1,2} と R の間',2*r,u],['R 内部のペア',r*(r-1)/2,v]];
  $('weight-groups').innerHTML=groups.map(([label,count,w])=>`<div class="weight-row"><div>${label}<small>${count}予定 × 各 ${pct(w,3)}</small></div><div class="weight-bar" role="img" aria-label="総確率 ${pct(count*w,3)}"><span style="width:${100*count*w}%"></span></div><strong>${pct(count*w,2)}</strong></div>`).join('');
  const all=[];for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)all.push({e:[i,j],w:i===1&&j===2?rho:(i<=2||j<=2)?u:v});
  const rates=all.map(({e})=>all.reduce((s,z)=>s+(e.every(i=>!z.e.includes(i))?z.w:0),0));
  const min=Math.min(...rates),total=all.reduce((s,z)=>s+z.w,0);
  put('cap-check',`図の確率を全${N}ペアについて直接集計：総確率 ${pct(total,2)}、最小同時監査率 ${pct(min,2)}。理論値 ${pct(T,2)} と一致。`);
 }
 ['target-count','cap-fraction'].forEach(id=>$(id).addEventListener('input',drawCap));
 const pairs=[[1,2],[3,4],[1,5],[2,3],[4,5],[3,5],[2,5],[2,4],[1,4],[1,3]];
 const adjacent=(a,b)=>a.every(x=>!b.includes(x));let restricted=0;
 function drawGraph(){
  const center=[260,224];const pos=pairs.map((_,i)=>{const a=-Math.PI/2+2*Math.PI*(i%5)/5,rad=i<5?175:85;return[center[0]+rad*Math.cos(a),center[1]+rad*Math.sin(a)];});
  const isNeigh=i=>adjacent(pairs[i],pairs[restricted]);
  let s=title(`未監査ペア${pairs[restricted].join('')}を使用しない最適分布。隣接頂点は各1/12、その他は各1/8。`);
  for(let i=0;i<10;i++)for(let j=i+1;j<10;j++)if(adjacent(pairs[i],pairs[j]))s+=line(...pos[i],...pos[j],`stroke="${i===restricted||j===restricted?teal:'#cbd7d0'}" stroke-width="${i===restricted||j===restricted?3:1.7}"`);
  pairs.forEach((p,i)=>{const[x,y]=pos[i],sel=i===restricted,nei=isNeigh(i),fill=sel?'#fff':nei?dark:'#e1e9e1',st=sel?warm:nei?dark:'#839a8e';
   s+=`<g class="p-node" tabindex="0" role="button" data-node="${i}" aria-label="未監査ペア${p.join('')}を使用しない場合を見る" aria-pressed="${sel}"><circle cx="${x}" cy="${y}" r="26" fill="${fill}" stroke="${st}" stroke-width="${sel?3:1.8}"/><text x="${x}" y="${y+6}" text-anchor="middle" font-size="19" font-weight="700" fill="${nei?'white':ink}">${p.join('')}</text></g>`;
  });
  $('petersen').innerHTML=s;put('graph-selected',`指定ペア ${pairs[restricted].join('')}`);
 }
 function selectGraph(ev){const el=ev.target.closest('[data-node]');if(!el)return;if(ev.type==='keydown'&&!['Enter',' '].includes(ev.key))return;if(ev.type==='keydown')ev.preventDefault();restricted=Number(el.dataset.node);drawGraph();if(ev.type==='keydown')$('petersen').querySelector(`[data-node="${restricted}"]`).focus();}
 $('petersen').addEventListener('click',selectGraph);$('petersen').addEventListener('keydown',selectGraph);
 const proofs=()=>[...document.querySelectorAll('details.proof-block')];
 $('expand-proofs').addEventListener('click',()=>proofs().forEach(e=>e.open=true));
 $('collapse-proofs').addEventListener('click',()=>proofs().forEach(e=>e.open=false));
 let printStates=[];
 addEventListener('beforeprint',()=>{printStates=proofs().map(e=>e.open);proofs().forEach(e=>e.open=true);});
 addEventListener('afterprint',()=>{proofs().forEach((e,i)=>e.open=printStates[i]||false);});
 $('print-page').addEventListener('click',()=>window.print());
 function openAnchor(){const hash=decodeURIComponent(location.hash.slice(1));if(!hash)return;const target=document.getElementById(hash);if(!target)return;let p=target;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}if(hash.startsWith('proof-'))requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}
 addEventListener('hashchange',openAnchor);
 drawCycle();drawAudit();drawSupport();drawCap();drawGraph();openAnchor();
})();
