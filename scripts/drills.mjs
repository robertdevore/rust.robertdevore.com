import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const manifest=JSON.parse(await readFile('drills/manifest.json'));
await mkdir('target/drills',{recursive:true});
const report={toolchain:spawnSync('rustc',['--version'],{encoding:'utf8'}).stdout.trim(),drills:[]};
for(const [name,expected] of Object.entries(manifest)) {
 const result=spawnSync('rustc',['--edition=2024','--error-format=json',`drills/${name}.rs`,'--out-dir','target/drills'],{encoding:'utf8'});
 assert.notEqual(result.status,0,`${name} unexpectedly compiled`);
 const diagnostics=result.stderr.trim().split('\n').map(x=>JSON.parse(x));
 const errors=diagnostics.filter(d=>d.level==='error'&&d.code);
 assert.ok(errors.length>0,`${name} has no coded error`);
 assert.deepEqual([...new Set(errors.map(e=>e.code.code))],[expected],`${name} failed for an unrelated reason`);
 const rendered=diagnostics.map(d=>d.rendered??'').join('');
 if(process.argv.includes('--update')) await writeFile(`drills/expected/${name}.txt`,rendered);
 else assert.equal(rendered,await readFile(`drills/expected/${name}.txt`,'utf8'),`${name}: review snapshot change`);
 report.drills.push({name,expected,verified:true});
}
await writeFile('docs/research/compiler-drills.json',JSON.stringify(report,null,2)+'\n');
console.log(`${report.drills.length} compiler drills verified on ${report.toolchain}`);
