import {readFile,writeFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const render=process.argv.includes('--render');
const manifest=JSON.parse(await readFile('howl.json','utf8'));
const inputs=['howl.json',...new Set(manifest.cards.flatMap(c=>[c.file,c.font_file,c.background_image].filter(Boolean)))];
if(render){for(const args of [['validate'],['render','--out','showcase']]){const r=spawnSync(process.env.HOWL_BIN||'howl',args,{stdio:'inherit'});if(r.error)throw r.error;if(r.status!==0)process.exit(r.status||1);}}
const outputs=(await readdir('showcase')).filter(f=>/\.(svg|html|md)$/.test(f)).map(f=>'showcase/'+f);
async function hashes(files){return Object.fromEntries(await Promise.all(files.map(async f=>[f,createHash('sha256').update(await readFile(f)).digest('hex')])));}
const receipt={howlVersion:'1.1.0',inputs:await hashes(inputs),outputs:await hashes(outputs)};
if(render)await writeFile('showcase/manifest-lock.json',JSON.stringify(receipt,null,2)+'\n');
else assert.deepEqual(receipt,JSON.parse(await readFile('showcase/manifest-lock.json','utf8')),'Howl source/artifact drift: run npm run render:howl with Howl 1.1.0.');
console.log('Howl source and artifact hashes verified.');
