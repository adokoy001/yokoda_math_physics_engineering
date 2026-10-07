(function(){'use strict';
document.getElementById('round9-download-size').textContent='40 KB・証明と検算';
document.getElementById('round9-download').addEventListener('click',()=>{
 const raw=atob(document.getElementById('round9-bundle').textContent.trim());
 const bytes=Uint8Array.from(raw,c=>c.charCodeAt(0));
 const url=URL.createObjectURL(new Blob([bytes],{type:'application/zip'}));
 const a=document.createElement('a');a.href=url;a.download='physical-memory-round9-research.zip';a.click();
 setTimeout(()=>URL.revokeObjectURL(url),10000);
});})();