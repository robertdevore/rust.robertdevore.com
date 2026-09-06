import {spawnSync} from 'node:child_process';
import {writeFile,mkdir} from 'node:fs/promises';
import assert from 'node:assert/strict';
const exe=process.platform==='win32'?'target/debug/audit-cli.exe':'target/debug/audit-cli';
const run=(input,args=['-'])=>spawnSync(exe,args,{input,encoding:'utf8'});
for(const [input,output] of [['INFO a\nWARN b\nERROR c','INFO=1 WARN=1 ERROR=1\n'],['','INFO=0 WARN=0 ERROR=0\n'],['INFO café\r\n','INFO=1 WARN=0 ERROR=0\n']]){const r=run(input);assert.equal(r.status,0,r.stderr);assert.equal(r.stdout,output);assert.equal(r.stderr,'');}
for(const input of ['INFO ok\nBOGUS x', 'INFO '+ 'x'.repeat(4096),Buffer.from([73,78,70,79,32,255])]){const r=run(input);assert.equal(r.status,1);assert.equal(r.stdout,'');assert.match(r.stderr,/line [12]:/);}
for(const args of [[],['a','b'],['target/no-such-fixture-23498']]){const r=run('',args);assert.equal(r.status,1);assert.equal(r.stdout,'');assert.match(r.stderr,/audit:/);}
await mkdir('target/cli-fixtures',{recursive:true});
await writeFile('target/cli-fixtures/records.txt','WARN file\n');
assert.equal(run('',['target/cli-fixtures/records.txt']).stdout,'INFO=0 WARN=1 ERROR=0\n');
console.log('10 CLI contract scenarios passed');
