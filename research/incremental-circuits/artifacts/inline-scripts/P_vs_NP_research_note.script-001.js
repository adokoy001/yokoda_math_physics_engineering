
'use strict';
function residualText(x,y){
  const f=z=>Boolean((x||z)&&(y||z));
  const values=[Number(f(0)),Number(f(1))];
  const residual=values[0]===1?'1（定数）':'z';
  const peers=values[0]===1?'この切断では xy=11 だけがこの未来を持ちます。':'xy=00、01、10 と同じ未来です。';
  return `xy=${x}${y} の残余は ${residual}。z=0 なら ${values[0]}、z=1 なら ${values[1]}。${peers}`;
}
function patchModel(i,b){
  const support=[];for(let ell=3;ell>=0;ell--)if((i>>ell)&1)support.push(ell);
  const w=support.length;
  return {i,b,w,extra:w+(b===0?1:0),support,cells:Array.from({length:16},(_,j)=>{
    const mask=(j&i)===i?1:0;
    const before=((j>>3)&1)||((j>>1)&1);
    const after=b===1?(before||mask):(before&&(1-mask));
    const kind=j<i?'past':j===i?'current':mask?'cone':'future';
    return {j,mask,before:Number(before),after:Number(after),kind};
  })};
}
function updateSat(){document.getElementById('sat-result').textContent=residualText(Number(document.getElementById('sat-x').value),Number(document.getElementById('sat-y').value));}
function updatePatch(){
 const i=Number(document.getElementById('patch-i').value),b=Number(document.getElementById('patch-b').value),model=patchModel(i,b);
 const subs=['₀','₁','₂','₃'];const mask=model.support.map(ell=>'z'+subs[ell]).join('∧');
 document.getElementById('patch-i-label').textContent=String(i);
 document.getElementById('patch-result').textContent=`i=${i}=${i.toString(2).padStart(4,'0')}₂。w=${model.w}。マスクは ${mask}。追加は高々${model.extra}ゲート、合計は高々${1+model.extra}ゲート。既読${i}点はすべて保存されます。`;
 const grid=document.getElementById('patch-grid');grid.replaceChildren();
 for(const c of model.cells){
  const el=document.createElement('div');el.className='truthcell '+c.kind;
  const address=document.createElement('span');address.className='address';address.textContent=`${c.j.toString(2).padStart(4,'0')} (${c.j})`;
  const value=document.createElement('span');value.className='value';value.textContent=`${c.before} → ${c.after}`;
  const meaning=document.createElement('span');meaning.className='meaning';meaning.textContent=c.kind==='past'?'既読・保存':c.kind==='current'?'次の位置':c.mask?'未読・a=1':'未読・a=0';
  el.append(address,value,meaning);grid.append(el);
 }
}
if(typeof document!=='undefined'){
 for(const id of ['sat-x','sat-y'])document.getElementById(id).addEventListener('change',updateSat);
 document.getElementById('patch-i').addEventListener('input',updatePatch);
 document.getElementById('patch-b').addEventListener('change',updatePatch);
 const proofButton=document.getElementById('proof-toggle');
 proofButton.addEventListener('click',()=>{const shouldOpen=proofButton.getAttribute('aria-pressed')!=='true';document.querySelectorAll('details.proof').forEach(d=>d.open=shouldOpen);proofButton.setAttribute('aria-pressed',String(shouldOpen));proofButton.textContent=shouldOpen?'証明の詳細をすべて閉じる':'証明の詳細をすべて開く';});
 document.getElementById('print-page').addEventListener('click',()=>window.print());
 let beforePrintStates=[];
 window.addEventListener('beforeprint',()=>{beforePrintStates=Array.from(document.querySelectorAll('details.proof')).map(d=>({el:d,open:d.open}));beforePrintStates.forEach(v=>v.el.open=true);});
 window.addEventListener('afterprint',()=>{beforePrintStates.forEach(v=>v.el.open=v.open);});
 if(window.matchMedia('(max-width:780px)').matches)document.querySelector('.toc').open=false;
 if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{for(const e of entries){if(e.isIntersecting){document.querySelectorAll('.toc a').forEach(a=>a.removeAttribute('aria-current'));const a=document.querySelector('.toc a[href="#'+e.target.id+'"]');if(a)a.setAttribute('aria-current','location');}}},{rootMargin:'-10% 0px -70% 0px'});document.querySelectorAll('section.chapter[id]').forEach(s=>observer.observe(s));}
 updateSat();updatePatch();
}
