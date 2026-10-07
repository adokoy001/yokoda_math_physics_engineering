(()=>{
const packed=document.getElementById('sdp-log-packed'),out=document.getElementById('sdp-log-status'),jsonButton=document.getElementById('download-sdp-log-json');
function bytes(){return Uint8Array.from(atob(packed.textContent.trim()),c=>c.charCodeAt(0))}
function save(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
document.getElementById('download-sdp-log-gzip').addEventListener('click',()=>{save(new Blob([bytes()],{type:'application/gzip'}),'round3_sdp_results.json.gz');out.textContent='元のJSONを含む圧縮ログの保存を開始しました。'});
if(!('DecompressionStream' in window)){jsonButton.disabled=true;out.textContent='このブラウザーではJSONの展開に対応していません。圧縮ログを保存して展開できます。';return}
jsonButton.addEventListener('click',async()=>{jsonButton.disabled=true;out.textContent='実行ログを展開しています…';try{const data=await new Response(new Blob([bytes()]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();save(new Blob([data],{type:'application/json;charset=utf-8'}),'round3_sdp_results.json');out.textContent='全32回分のJSONを展開して、保存を開始しました。'}catch(error){out.textContent='JSONの展開に失敗しました。圧縮ログを保存して展開できます。'}finally{jsonButton.disabled=false}});
})();