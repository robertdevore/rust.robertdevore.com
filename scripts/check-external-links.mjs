import {readFile,writeFile} from 'node:fs/promises';
import {lessons} from './content.mjs';
const text=(await lessons()).map(x=>x.body).join('\n')+await readFile('content/about.md','utf8');
const urls=[...new Set([...text.matchAll(/\]\((https:\/\/[^)]+)\)/g)].map(x=>x[1]))].filter(u=>!u.includes('github.com/robertdevore/rust.robertdevore.com'));
const results=[];let index=0;
await Promise.all(Array.from({length:5},async()=>{while(index<urls.length){const url=urls[index++];try{const r=await fetch(url,{signal:AbortSignal.timeout(30000)});await r.arrayBuffer();results.push({url,status:r.status,finalUrl:r.url});}catch(e){results.push({url,error:e.message});}}}));
await writeFile('docs/research/lesson-links.json',JSON.stringify({checkedAt:new Date().toISOString(),results},null,2)+'\n');
const failed=results.filter(r=>r.status!==200);console.log(JSON.stringify({checked:results.length,failed},null,2));if(failed.length)process.exitCode=1;
