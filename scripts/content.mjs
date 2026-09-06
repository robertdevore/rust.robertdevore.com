import {readFile,readdir} from 'node:fs/promises';
export const origin='https://rust.robertdevore.com';
export const stages=[
 {name:'Learn the foundations',label:'01 / Foundations',description:'From the first executable to ownership, data modeling, and a working event counter.'},
 {name:'Build reliable programs',label:'02 / Application design',description:'Borrowed interfaces, purposeful traits, bounded input, and tests that matter.'},
 {name:'Understand concurrent work',label:'03 / Concurrency',description:'Shared state, threads, synchronization, futures, and the runtime underneath async.'},
 {name:'Reason about the boundaries',label:'04 / Systems practice',description:'Pinning, unsafe invariants, performance evidence, and the Rust being developed today.'},
 {name:'Ship and maintain',label:'05 / Production',description:'Install the finished tool, review its contracts, and build a sustainable release workflow.'}
];
export async function lessons(){return Promise.all((await readdir('content/lessons')).filter(f=>f.endsWith('.md')).sort().map(async(file,index)=>{const raw=await readFile(`content/lessons/${file}`,'utf8');const split=raw.indexOf('\n---\n');if(split<0)throw Error(`Missing metadata separator: ${file}`);const meta=JSON.parse(raw.slice(0,split));return {...meta,number:index+1,slug:file.replace('.md',''),url:`/course/${file.replace('.md','')}/`,body:raw.slice(split+5)};}));}
