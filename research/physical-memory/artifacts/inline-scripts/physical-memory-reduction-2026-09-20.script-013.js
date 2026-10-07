(()=>{
'use strict';
const $=id=>document.getElementById(id), all=(s)=>Array.from(document.querySelectorAll(s));
const H=[[2,1,0,1],[1,2,1,0],[0,1,2,1],[1,0,1,2]], F0=[[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]], R=[[1,1,1,1],[1,0,-1,0],[0,1,0,-1]];
const state={heat:0,time:4,hide:false,playing:false,input:0,output:0,h:5.025724834504679,steady:false,mode:'positive',factor:-1,rho:.25,eta:.1,z:.1};
const fmt=(x,n=3)=>Math.abs(x)<.5*10**-n?(0).toFixed(n):x.toFixed(n);
const gram=F=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>F.reduce((v,r)=>v+r[i]*r[j],0)));
const envelope=(d,z)=>{d=Math.max(0,d);z=Math.min(d,Math.max(0,z));return Math.min(Math.sqrt(z*(2*d-z)),(d+z)/2)};
const category=(i,j)=>i===j?'d':(Math.abs(i-j)===2?'z':'m');
function matrix(A,{digits=2,selected=null,categories=false,rows=null}={}){
 let s='<table class="lab-matrix"><thead><tr><th scope="col">'+(rows?'因子':'出力↓')+'</th>';
 for(let j=0;j<4;j++)s+='<th scope="col">B'+(j+1)+'</th>';s+='</tr></thead><tbody>';
 A.forEach((row,i)=>{s+='<tr><th scope="row">'+(rows?rows[i]:'B'+(i+1))+'</th>';row.forEach((v,j)=>{
 let cl=categories?'category-'+category(i,j):v<-1e-10?'negative':Math.abs(v)<1e-10?'zero':'';
 if(selected&&selected[0]===i&&selected[1]===j)cl+=' picked';
 s+='<td class="'+cl+'">'+fmt(v,digits)+'</td>'});s+='</tr>'});return s+'</tbody></table>';
}
function svgBox(w,h,content,label){return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+w+' '+h+'" role="img" aria-label="'+label+'"><title>'+label+'</title>'+content+'</svg>'}
const line=(x1,y1,x2,y2,stroke='#cbd4ca',sw=1,dash='')=>'<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="'+stroke+'" stroke-width="'+sw+'"'+(dash?' stroke-dasharray="'+dash+'"':'')+'/>';
const tx=(x,y,s,extra='')=>'<text x="'+x+'" y="'+y+'" font-size="12" '+extra+'>'+s+'</text>';
function heatTemp(t){return t<=1?.5*(t-4*(-Math.expm1(-t/4))):.5*(1-4*(-Math.expm1(-.25))*Math.exp(-(t-1)/4))}
function heatColor(t){const u=Math.max(0,Math.min(1,t));return 'rgb('+Math.round(207+32*u)+','+Math.round(225-95*u)+','+Math.round(217-140*u)+')'}
function drawHeat(){
 const b=[[58,60],[302,60],[302,270],[58,270]], p=[[180,60],[302,165],[180,270],[58,165]], labels=['I12','I23','I34','I41'];
 let s='';for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){if(Math.abs(i-j)===2){s+=line(...b[i],...b[j],'#bdc8b7',1.5)}else{const mx=(b[i][0]+b[j][0])/2,my=(b[i][1]+b[j][1])/2,cx=mx+.6*(180-mx),cy=my+.6*(165-my);s+='<path d="M '+b[i][0]+' '+b[i][1]+' Q '+cx+' '+cy+' '+b[j][0]+' '+b[j][1]+'" fill="none" stroke="#bdc8b7" stroke-width="1.5"/>'}}
 const adjacent=i=>i===state.heat||(i+1)%4===state.heat, temp=heatTemp(state.time);
 if(!state.hide){for(let i=0;i<4;i++){let on=adjacent(i);s+=line(...p[i],...b[i],on?'#a97749':'#7d9b90',3)+line(...p[i],...b[(i+1)%4],on?'#a97749':'#7d9b90',3)}
 p.forEach(([x,y],i)=>{let v=adjacent(i)?temp:0;s+='<circle cx="'+x+'" cy="'+y+'" r="25" fill="'+heatColor(v)+'" stroke="#496f67" stroke-width="1.5"/>'+tx(x,y-1,labels[i],'text-anchor="middle" style="font-size:14px"')+tx(x,y+17,fmt(v,2),'text-anchor="middle" style="font-size:14px"')})
 }else s+='<rect x="104" y="101" width="152" height="124" rx="10" fill="#e1e8dd"/>'+tx(180,145,'内部は非表示','text-anchor="middle" style="font-size:16px"')+tx(180,179,'応答は同じ','text-anchor="middle" style="font-size:16px"');
 b.forEach(([x,y],i)=>{let v=i===state.heat?Math.min(state.time,1):0;s+='<rect x="'+(x-24)+'" y="'+(y-23)+'" width="48" height="46" rx="5" fill="'+heatColor(v)+'" stroke="'+(i===state.heat?'#a14d2e':'#6b8173')+'" stroke-width="'+(i===state.heat?2.5:1.2)+'"/>'+tx(x,y+5,'B'+(i+1),'text-anchor="middle" style="font-size:16px;font-weight:650"')+tx(x,y+(y<160?-34:43),fmt(v,2)+' K','text-anchor="middle" class="temp-label"')});
 $('heat-diagram').innerHTML='<title>境界と内部の温度差</title>'+s;
 $('heat-time-value').value=fmt(state.time,1)+' s';$('heat-note').textContent=state.hide?'内部を隠しても、熱を蓄える4つの状態は残ります。':state.time<1?'境界B'+(state.heat+1)+'を立ち上げ中。隣接する内部は、まだ追いついていません。':'境界は1 Kに到達。隣接する内部は '+fmt(temp,3)+' K。十分に待つと0.5 Kへ近づきます。';
}
function windowData(h,i,j){const f=4*(-Math.expm1(-.25)),b=f*Math.exp(-.025),e=Math.exp(-h/4),a=b*(1-e)**2,k=i===j?3:-1,v=H[i][j];return {a,k,v,b,first:k*h+v*b*(1-e),second:k*h+v*b*e*(1-e),diff:a*v}}
function drawWindow(){
 const box=$('window-plot'),w=Math.max(250,Math.round(box.getBoundingClientRect().width)),ht=292,L=54,RR=12,T=52,B=45,pw=w-L-RR,ph=ht-T-B,h=state.h,d=windowData(h,state.output,state.input);
 const shift=state.steady?d.k:0,y0=d.k-shift,fun=t=>d.k+.25*d.v*d.b*Math.exp(-t/4)-shift;
 let lo=Math.min(0,y0,fun(2*h)),hi=Math.max(0,y0,fun(0));if(hi-lo<.1){hi+=.12;lo-=.12}const pad=(hi-lo)*.13;lo-=pad;hi+=pad;
 const x=t=>L+t/(2*h)*pw,y=v=>T+(hi-v)/(hi-lo)*ph;
 let s='';for(let n=0;n<4;n++){let v=lo+(hi-lo)*n/3;s+=line(L,y(v),w-RR,y(v),'#dbe1d7')+tx(L-7,y(v)+4,fmt(v,1),'text-anchor="end"')}
 s+='<rect x="'+L+'" y="'+T+'" width="'+pw+'" height="'+ph+'" fill="none" stroke="#b9c8b9"/>';
 for(let n=0;n<2;n++){let t0=n*h,t1=(n+1)*h;let path='M '+x(t0)+' '+y(0);for(let k=0;k<=80;k++){let t=t0+(t1-t0)*k/80;path+=' L '+x(t)+' '+y(fun(t))}path+=' L '+x(t1)+' '+y(0)+' Z';s+='<path d="'+path+'" fill="'+(n===0?'#72a992':'#d4ab76')+'" opacity=".32"/>';s+=tx(x(t0+h/2),T-10,'第'+(n+1)+'窓','text-anchor="middle"')}
 s+=line(x(h),T,x(h),T+ph,'#92a18f',1,'4 4')+line(L,y(y0),w-RR,y(y0),'#88947f',1,'5 4');
 let path='';for(let k=0;k<=160;k++){let t=2*h*k/160;path+=(k?' L ':'M ')+x(t)+' '+y(fun(t))}s+='<path d="'+path+'" fill="none" stroke="#146e63" stroke-width="2.5"/>';
 [0,h,2*h].forEach(v=>{s+=tx(x(v),ht-B+21,fmt(v,1),'text-anchor="'+(v===0?'start':v===2*h?'end':'middle')+'"')});
 s+=tx(L,17,'熱流応答 R（W/K）')+tx(L+pw/2,ht-4,'観測開始からの時間（s）','text-anchor="middle"');
 box.innerHTML=svgBox(w,ht,s,'二窓の積分：B'+(state.input+1)+'入力、B'+(state.output+1)+'出力');
 $('window-value').value=fmt(h,3)+' s';$('area-first').textContent=fmt(d.first-shift*h,3);$('area-second').textContent=fmt(d.second-shift*h,3);$('area-diff').textContent=fmt(d.diff,3)+' J/K';
 $('window-caption').textContent=(state.steady?'定常分を引いても、二窓の差は変わりません。':'熱流は符号付きです。負は、その境界から熱を取り出す向きです。')+' 図の入力・出力選択は次の行列の枠に対応します。';
 $('measured-matrix').innerHTML=matrix(H.map(r=>r.map(v=>d.a*v)),{digits:3,selected:[state.output,state.input]});$('matrix-a').textContent='a = '+fmt(d.a,6)+' J/K';
}
function drawFactor(){const F=state.mode==='positive'?F0:R,chosen=state.factor<0?F:[F[state.factor]],A=gram(chosen);
 $('factor-title').textContent=state.mode==='positive'?'4本の非負ベクトル':'符号を使った3本のベクトル';
 $('factor-vectors').innerHTML=F.map((r,i)=>'<button class="factor-vector" data-factor="'+i+'" aria-pressed="'+(state.factor===i)+'"><span>ベクトル'+(i+1)+'</span>'+r.map(v=>'<span class="'+(v<0?'negative':v===0?'zero':'')+'">'+v+'</span>').join('')+'</button>').join('');
 $('factor-result-title').textContent=state.factor<0?'外積を全部足すと H₀':'ベクトル'+(state.factor+1)+'の外積だけ';$('factor-matrix').innerHTML=matrix(A,{digits:0});
 $('factor-explanation').textContent=state.mode==='positive'?(state.factor<0?'4辺を1本ずつ受け持ちます。どの寄与にも負の数がなく、向かい合う2組は最初から0です。':'選んだ1本は、隣接する2つの境界だけに寄与します。4本全てを足すとH₀です。'):(state.factor<0?'負の寄与を打ち消しに使えるため、3本でH₀を作れます。この分解は3個の物理的な熱容量の構成ではありません。':state.factor===0?'この1本は全ての組に+1を与えます。向かい合う組を0にするには、別のベクトルの負の寄与で消す必要があります。':'向かい合う組に−1が現れます。最初のベクトルの+1を消し、和では0になります。');
}
function drawEnvelope(){const el=$('envelope-plot'),w=Math.max(250,Math.round(el.getBoundingClientRect().width)),h=300,L=52,rr=14,t=23,bb=49,pw=w-L-rr,ph=h-t-bb;
 const x=q=>L+pw*q,y=m=>t+ph*(1-m/1.12);let path='M '+x(0)+' '+y(0);for(let k=1;k<=300;k++){let q=k/300;path+=' L '+x(q)+' '+y(envelope(1,q))}let s='<rect x="'+L+'" y="'+t+'" width="'+pw+'" height="'+ph+'" fill="#f4e9dc"/>';
 s+='<path d="'+path+' L '+x(1)+' '+y(0)+' Z" fill="#dbeadf"/>';
 [0,.2,.6,1].forEach(q=>{s+=line(x(q),t,x(q),t+ph,'#d0d8cd')+tx(x(q),h-bb+20,fmt(q,1),'text-anchor="'+(q===0?'start':q===1?'end':'middle')+'"')});[0,.5,1].forEach(v=>{s+=line(L,y(v),w-rr,y(v),'#d0d8cd')+tx(L-8,y(v)+4,fmt(v,1),'text-anchor="end"')});
 s+='<path d="'+path+'" fill="none" stroke="#126e60" stroke-width="2.5"/>';
 const q=state.rho/(2+state.rho),m=(1+state.rho)/(2+state.rho);s+=line(x(q),y(0),x(q),y(m),'#966440',1,'3 4');s+='<circle cx="'+x(q)+'" cy="'+y(m)+'" r="5.5" fill="#a44c2d" stroke="#fffdf5" stroke-width="2"/>';
 s+=tx(L+9,t+18,'上側：3状態以下では不可能')+tx(L+9,t+ph-19,'下側：この集約値では判定保留')+tx(L,17,'四辺の下限 m / d')+tx(L+pw/2,h-6,'対向成分の上限 z / d','text-anchor="middle"');el.innerHTML=svgBox(w,h,s,'三集約値の境界。選択したH rhoを丸で表示');
 $('envelope-note').textContent='選んだ行列：z/d = '+fmt(q,3)+'、m/d = '+fmt(m,3)+'。'+(state.rho<.5?'丸は境界の上にあり、3状態以下を排除できます。':state.rho===.5?'ρ=0.5で境界へ到達。この行列族では3状態が実際に可能です。':'丸は境界上を動きます。この行列族では3状態が実際に可能です。');
}
function drawRho(){let r=state.rho;$('lab-rho-value').value=fmt(r,2);$('rho-matrix').innerHTML=matrix(H.map(row=>row.map(x=>x+r)),{digits:2,categories:true});$('rho-physical').textContent=r<.5?'4':'3';$('rho-explanation').textContent=r<.5?'全成分を増やしても、まだ4個の内部熱容量が必要です。':'ρが1/2以上になると、3個の内部熱容量で実現できます。';drawEnvelope();}
function attaining(z){if(z<=.2){let a=Math.sqrt(z/2),b=Math.sqrt(1-z/2),c=Math.sqrt(1-2*z);return [[0,a,b,2*a],[2*a,b,a,0],[c,0,0,c]]}if(z===1)return [[1,1,1,1],[0,0,0,0],[0,0,0,0]];
 let scale=Math.sqrt((1-z)/2),rho=2*z/(1-z),h=Math.sqrt(1+rho),q=Math.sqrt(3/8),Q=[[.5,-q,q],[q,-.25,-.75],[q,.75,.25]],rr=[[h,h,h,h],[1,0,-1,0],[0,1,0,-1]];return Q.map(row=>Array.from({length:4},(_,j)=>Math.max(0,scale*row.reduce((v,a,k)=>v+a*rr[k][j],0))));}
function drawAttain(){let z=state.z,F=attaining(z),A=gram(F),m=Math.min(A[0][1],A[1][2],A[2][3],A[3][0]);$('attain-z-value').value=fmt(z,2);$('attain-factor').innerHTML=matrix(F,{digits:3,rows:['f₁','f₂','f₃']});$('attain-note').textContent='表示は丸め値。実際の因子の和では、対角は1、対向成分は '+fmt(z,3)+'、四辺の最小値は '+fmt(m,6)+' = M(1,z)。全て非負です。3行以下で境界を達成しています。';}
function drawNoise(){const e=state.eta,c=1-e,z=e,d=2+e,M=envelope(d,z),margin=c-M,tol=1e-12*Math.max(c,M,Number.MIN_VALUE),reject=margin>tol;
 $('noise-value').value=Math.abs(e-1/6)<1e-14?'1/6 = 0.1667…':fmt(e,4);[['noise-c',c],['noise-z',z],['noise-d',d],['noise-left',c],['noise-right',M]].forEach(([id,v])=>$(id).textContent=fmt(v,3));
 $('noise-left-bar').style.width=(c/1.1*100)+'%';$('noise-right-bar').style.width=(M/1.1*100)+'%';$('noise-verdict').classList.toggle('inconclusive',!reject);$('noise-verdict').textContent=reject?'3状態以下を排除：許した誤差では届きません。':'判定保留：この条件だけでは排除できません。';
 $('noise-detail').textContent='差 c − M = '+fmt(margin,6)+'。'+(reject?'四辺を小さく、対向と対角を大きくしても、3状態の限界を越えています。':'「3状態で十分」という結論ではありません。全成分を使う、より詳しい判定の余地があります。');
}
function drawDistance(){const el=$('distance-plot'),w=Math.max(250,Math.round(el.getBoundingClientRect().width)),h=160,L=26,R=20,x=v=>L+(w-L-R)*v/.22,low=11/62,up=.196676467057347;let s=line(x(0),75,x(.22),75,'#b7c6b7',2)+line(x(low),75,x(up),75,'#0c7166',9);s+='<circle cx="'+x(low)+'" cy="75" r="5" fill="#0c7166"/><circle cx="'+x(up)+'" cy="75" r="5" fill="#faf9f4" stroke="#0c7166" stroke-width="2"/>';
 s+=line(x(low),75,x(low),40,'#6a8e7b')+tx(x(low)-5,25,'下限 11/62','text-anchor="end"')+line(x(up),80,x(up),112,'#6a8e7b')+tx(x(up),134,'上界 約0.1966765','text-anchor="end"');
 s+=tx(x(0),102,'0')+tx(x(.22),102,'0.22','text-anchor="end"')+tx(L,55,'最小値の未決定区間');el.innerHTML=svgBox(w,h,s,'下限と上界の間に残る未決定の距離');}
function openAnchor(){let id=decodeURIComponent(location.hash.slice(1)),el=$(id);if(!el)return;let node=el,changed=false;while(node){if(node.tagName==='DETAILS'&&!node.open){node.open=true;changed=true}node=node.parentElement}if(changed)requestAnimationFrame(()=>el.scrollIntoView({behavior:'auto',block:'start'}));}
$('heat-inputs').addEventListener('click',e=>{const b=e.target.closest('[data-heat]');if(!b)return;state.heat=Number(b.dataset.heat);all('[data-heat]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));drawHeat()});
$('heat-time').addEventListener('input',()=>{state.time=Number($('heat-time').value);drawHeat()});let timer=null;
$('heat-play').addEventListener('click',()=>{state.playing=!state.playing;$('heat-play').textContent=state.playing?'一時停止':'時間を進める';if(!state.playing){clearInterval(timer);return}if(state.time>=16)state.time=0;timer=setInterval(()=>{state.time=Math.min(16,state.time+.1);$('heat-time').value=state.time;drawHeat();if(state.time>=16){clearInterval(timer);state.playing=false;$('heat-play').textContent='最初から再生'}},100)});
$('heat-hide').addEventListener('click',()=>{state.hide=!state.hide;$('heat-hide').setAttribute('aria-pressed',String(state.hide));$('heat-hide').textContent=state.hide?'内部を表示':'内部を隠す';drawHeat()});
['input','output'].forEach(k=>$('measure-'+k).addEventListener('change',()=>{state[k]=Number($('measure-'+k).value);drawWindow()}));
$('window-h').step='any';$('window-h').value=state.h;$('window-h').addEventListener('input',()=>{state.h=Number($('window-h').value);drawWindow()});$('window-optimum').addEventListener('click',()=>{state.h=5.025724834504679;$('window-h').value=state.h;drawWindow()});$('remove-steady').addEventListener('change',()=>{state.steady=$('remove-steady').checked;drawWindow()});
$('factor-modes').addEventListener('click',e=>{const b=e.target.closest('[data-mode]');if(!b)return;state.mode=b.dataset.mode;state.factor=-1;all('[data-mode]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));drawFactor()});$('factor-vectors').addEventListener('click',e=>{const b=e.target.closest('[data-factor]');if(!b)return;state.factor=Number(b.dataset.factor);drawFactor()});$('factor-all').addEventListener('click',()=>{state.factor=-1;drawFactor()});
$('lab-rho').addEventListener('input',()=>{state.rho=Number($('lab-rho').value);drawRho()});all('[data-rho]').forEach(b=>b.addEventListener('click',()=>{state.rho=Number(b.dataset.rho);$('lab-rho').value=state.rho;drawRho()}));$('attain-z').addEventListener('input',()=>{state.z=Number($('attain-z').value);drawAttain()});
$('noise-eta').step='any';$('noise-eta').addEventListener('input',()=>{state.eta=Number($('noise-eta').value);drawNoise()});all('[data-eta]').forEach(b=>b.addEventListener('click',()=>{state.eta=b.dataset.eta==='sixth'?1/6:Number(b.dataset.eta);$('noise-eta').value=state.eta;drawNoise()}));
$('open-all-notes').addEventListener('click',()=>all('.archive').forEach(d=>d.open=true));$('close-all-notes').addEventListener('click',()=>all('.archive').forEach(d=>d.open=false));$('print-reader').addEventListener('click',()=>window.print());window.addEventListener('hashchange',openAnchor);
all('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{const el=$(a.getAttribute('href').slice(1));if(!el)return;let p=el;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}}));
let navQueued=false;function syncNavigation(){navQueued=false;const lessons=all('.lesson');let active=lessons[0];for(const el of lessons)if(el.getBoundingClientRect().top<=innerHeight*.3)active=el;all('.reader-nav a').forEach(a=>a.setAttribute('aria-current',String(a.getAttribute('href')==='#'+active.id)))}window.addEventListener('scroll',()=>{if(!navQueued){navQueued=true;requestAnimationFrame(syncNavigation)}},{passive:true});syncNavigation();
let resizeTimer;if('ResizeObserver'in window){const ro=new ResizeObserver(()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{drawWindow();drawEnvelope();drawDistance()},60)});['window-plot','envelope-plot','distance-plot'].forEach(id=>ro.observe($(id)))}
document.addEventListener('visibilitychange',()=>{if(document.hidden&&state.playing){clearInterval(timer);state.playing=false;$('heat-play').textContent='時間を進める'}});
drawHeat();drawWindow();drawFactor();drawRho();drawAttain();drawNoise();drawDistance();openAnchor();
window.ReaderLab={state,gram,envelope,heatTemp,windowData,attaining};
})();
