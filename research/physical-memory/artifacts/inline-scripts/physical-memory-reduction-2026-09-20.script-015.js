
(function(){
'use strict';
const $=id=>document.getElementById(id), H=[[2,1,0,1],[1,2,1,0],[0,1,2,1],[1,0,1,2]],F0=[[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]];
function factor(r,positive){
 if(positive&&r===0)return null;
 if(r<.5||(positive&&r===.5)){const a=(Math.sqrt(1+r)-1)/2;return F0.map(row=>row.map(v=>v+a))}
 const h=Math.sqrt(1+r),q=Math.sqrt(3/8);
 const F=[[h/2-q,h/2+q,h/2+q,h/2-q],[q*h-.25,q*h-.75,q*h+.25,q*h+.75],[q*h+.75,q*h+.25,q*h-.75,q*h-.25]];
 return F.map(row=>row.map(v=>Math.abs(v)<1e-14?0:v));
}
function table(A,rowLabels){return '<table class="lab-matrix"><thead><tr><th></th>'+[1,2,3,4].map(i=>'<th>B'+i+'</th>').join('')+'</tr></thead><tbody>'+A.map((row,i)=>'<tr><th>'+rowLabels[i]+'</th>'+row.map(v=>'<td class="'+(v===0?'zero':'')+'">'+v.toFixed(3)+'</td>').join('')+'</tr>').join('')+'</tbody></table>'}
function drawPositive(){const r=Number($('lab-rho').value),strict=$('require-positive').checked,F=factor(r,strict);
 $('positive-ordinary').textContent=r<.5?'4':'3';$('positive-strict').textContent=r===0?'不可能':r<=.5?'4':'3';
 $('positive-factor').innerHTML=F?table(F,F.map((_,i)=>'f'+(i+1))):'';
 $('positive-coupling-note').textContent=!F?'ρ=0は行列にゼロ成分があるため、すべて正の因子では何本使っても厳密に表せません。':r===.5?(strict?'境界ρ=0.5。正の結合だけで厳密に表すには4個必要です。表示はその4行因子です。':'境界ρ=0.5。3行で厳密に表せますが、表示した因子には4つのゼロがあります。'):(strict?'全成分が正の':'ゼロを許す')+F.length+'行因子を表示しています。';
}
let sensorMode='raw';
function sensorData(mode){const theta=1,T=.1,h=1,a=theta*Math.exp(-T/theta)*(-Math.expm1(-h/theta))**2;return H.map(row=>row.map(v=>mode==='raw'?a*v:0))}
function drawSensor(){const raw=sensorMode==='raw';$('sensor-matrix').innerHTML=table(sensorData(sensorMode),['B1','B2','B3','B4']);
 $('sensor-verdict').textContent=raw?'見かけの判定：4状態以上':'二窓差は0：内部状態を要求しない';$('sensor-verdict').classList.toggle('inconclusive',raw);
 $('sensor-note').textContent=raw?'実際の内部容量は0個です。観測にはセンサーの動特性が含まれ、物体の真の熱流を使うという判定の前提を満たしていません。':sensorMode==='true'?'立上りの後では真の熱流は一定。等しい長さの二窓で差を取ると0になります。':'既知の一次遅れを端点値で補正すると、解析的に二窓差は0へ戻ります。この表示には雑音を加えていません。';
 document.querySelectorAll('[data-sensor]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.sensor===sensorMode)));
}
$('require-positive').addEventListener('change',drawPositive);$('lab-rho').addEventListener('input',drawPositive);document.querySelectorAll('[data-rho]').forEach(b=>b.addEventListener('click',drawPositive));
$('sensor-modes').addEventListener('click',e=>{const b=e.target.closest('[data-sensor]');if(!b)return;sensorMode=b.dataset.sensor;drawSensor()});
drawPositive();drawSensor();window.Round6Lab={factor,sensorData,drawPositive};
})();
(function(){
'use strict';
const $=id=>document.getElementById(id),keys=['L','D','m','M','z'];
function certificate(L,D,m,M,z){
 const a=[L,D,m,M,z];if(a.some(v=>!Number.isFinite(v))||L<0||D<=0||m<0||M<m||L>D||z<0||m>D)return {kind:'invalid'};
 const scale=Math.max(...a),tol=1e-10;[L,D,m,M,z]=a.map(v=>v/scale);
 const zc=Math.min(z,D),psi=Math.min(zc*(2*D-zc),(D+zc)**2/4);
 if(m*m-psi>tol)return {kind:'three',reject:true,margin:(m-Math.sqrt(psi))*scale};
 if(!(z>tol&&m-z>tol&&L-M>tol&&m*m-D*z>tol))return {kind:'outside',reject:false};
 const A=Math.max(L,z+m*m/z-D),U=(m*m-D*z)/(D-z),V=Math.min(M,m*z*(D-z)/(m*m-D*z)),R=Math.min(M,2*D*z*m/(z*z+m*m));
 if(!(U>0&&U<=z+tol&&A<=D+tol&&R>=m-tol&&V>=m-tol&&A-R>tol))return {kind:'outside',reject:false};
 const P=(A*(U-V)**2+2*(A-R)*U*V)/((A-R)*(A+R)),gap=L-M-P;
 return {kind:'five',reject:gap>tol,margin:gap*scale,projectedNorm:P*scale,A:A*scale,U:U*scale,V:V*scale,R:R*scale};
}
function draw(){const a=keys.map(k=>Number($('five-'+k).value)),empty=keys.some(k=>$('five-'+k).value.trim()===''),r=empty?{kind:'invalid'}:certificate(...a);const o=$('five-verdict');o.classList.toggle('inconclusive',!r.reject);
 o.textContent=r.kind==='invalid'?'入力を確認：有限で整合した上下限が必要です。':r.reject?'棄却成立：この区間に合う3状態以下の模型はありません。':'判定保留：この条件では3状態以下を排除できません。';
 $('five-detail').textContent=r.kind==='three'?'三集約式だけで棄却できます。余裕 m−M(D,z) = '+r.margin.toPrecision(6):r.kind==='five'?'五値条件：射影ノルムの上限 P = '+r.projectedNorm.toPrecision(7)+'、残る辺の矛盾余裕 L−M−P = '+r.margin.toPrecision(7)+'。':r.kind==='outside'?'三集約式では保留です。現在の値は、実装した五値条件の適用範囲に入りません。':'0≤L≤D、0≤m≤M、m≤D、z≥0を確認してください。';
 return r;
}
function preset(value){if(value==='correlation'){[1,1,.5,.5,0].forEach((v,i)=>$('five-'+keys[i]).value=v)}else{const e=value==='bound'?11/62:Number(value);[2-e,2+e,1-e,1+e,e].forEach((v,i)=>$('five-'+keys[i]).value=v)}draw()}
keys.forEach(k=>$('five-'+k).addEventListener('input',draw));document.querySelectorAll('[data-five]').forEach(b=>b.addEventListener('click',()=>preset(b.dataset.five)));
function noiseFull(){const e=ReaderLab.state.eta,ok=e<=11/62;const el=$('full-noise-verdict');el.textContent=ok?'全成分を使う追加保証でも棄却成立（η≤11/62）。':'11/62までの追加保証では判定保留。';el.classList.toggle('inconclusive',!ok)}
$('noise-eta').addEventListener('input',noiseFull);document.querySelectorAll('[data-eta]').forEach(b=>b.addEventListener('click',noiseFull));
draw();noiseFull();window.FiveBoundsLab={certificate,preset,draw};
})();

document.querySelectorAll('[data-round6-download]').forEach(button=>button.addEventListener('click',()=>{const data=document.getElementById(button.dataset.round6Download).textContent;const url=URL.createObjectURL(new Blob([data],{type:'text/x-python;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=button.dataset.filename;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}));

