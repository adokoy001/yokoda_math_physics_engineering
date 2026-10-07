
function certificatePsi(d,z){d=Math.max(0,d);const u=Math.min(Math.max(0,z),d);return Math.min(u*(2*d-u),(d+u)**2/4)}
function certificateMargin(m,z,d,eta){return Math.max(0,m-eta)**2-certificatePsi(d+eta,z+eta)}
function certificateRadius(m,z,d){if(m<=0||certificateMargin(m,z,d,0)<=0)return 0;let lo=0,hi=m;for(let i=0;i<80;i++){const mid=(lo+hi)/2;if(certificateMargin(m,z,d,mid)>0)lo=mid;else hi=mid}return (lo+hi)/2}
function updateCertificate(){const ids=['m','z','d','eta'];const v=ids.map(x=>parseFloat(document.getElementById('cert-'+x).value));const out=document.getElementById('cert-answer');const rad=document.getElementById('cert-radius');if(v.some(x=>!Number.isFinite(x))||v[3]<0){out.textContent='有限な測定値と、0以上の誤差幅を入力してください。';rad.textContent='';return}const[m,z,d,eta]=v;const left=Math.max(0,m-eta)**2;const right=certificatePsi(d+eta,z+eta);const tolerance=1e-12*Math.max(left,right,Number.MIN_VALUE);const reject=m>eta&&left-right>tolerance;out.textContent=reject?'棄却成立：この誤差区間に合う3状態以下の模型はありません。':'判定保留：この十分条件では3状態以下を棄却できません。';out.style.color=reject?'#08776c':'#885a24';rad.textContent='この集約値で棄却できる誤差幅の上限（厳密には未満）：'+certificateRadius(m,z,d).toPrecision(7)+'。 c² = '+left.toPrecision(5)+'、Ξ = '+right.toPrecision(5)+'。'}
['m','z','d','eta'].forEach(x=>document.getElementById('cert-'+x).addEventListener('input',updateCertificate));updateCertificate();
function saveEmbedded(button,element,name){document.getElementById(button).addEventListener('click',()=>{const a=document.createElement('a');const url=URL.createObjectURL(new Blob([document.getElementById(element).textContent],{type:'text/x-python;charset=utf-8'}));a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)})}
saveEmbedded('download-window-code','window-code','finite_window_verify.py');saveEmbedded('download-figure-code','figure-code','make_finite_window_figure.py');
saveEmbedded('download-algebra-code','algebra-code','cp3_algebraic_certificate.py');
saveEmbedded('download-sdp-exact-code','sdp-exact-code','round3_sdp_exact_certificate.py');
saveEmbedded('download-protocol-code','protocol-code','round3_protocol_verify.py');
saveEmbedded('download-sdp-numeric-code','sdp-numeric-code','round3_sdp_compare.py');
saveEmbedded('download-sharp-code','sharp-code','round4_sharp_certificate.py');
saveEmbedded('download-sdp-primal-code','sdp-primal-code','round4_sdp_primal_exact.py');
