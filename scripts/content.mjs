import {readFile,readdir} from 'node:fs/promises';
export const origin='https://rust.robertdevore.com';
export const stages=[
 {name:'Learn the foundations',label:'01 / Foundations',description:'Write your first program, learn ownership, and build an event counter.'},
 {name:'Build reliable programs',label:'02 / Application design',description:'Design functions that borrow data, handle errors, limit input, and test the results.'},
 {name:'Understand concurrent work',label:'03 / Concurrency',description:'Share data safely, coordinate threads, and learn how futures and runtimes work.'},
 {name:'Work with systems code',label:'04 / Systems practice',description:'Understand pinning and unsafe code, measure performance, and follow work on Rust.'},
 {name:'Ship and maintain',label:'05 / Production',description:'Install your tool, check its public API, and learn how to release updates.'}
];
export async function lessons(){return Promise.all((await readdir('content/lessons')).filter(f=>f.endsWith('.md')).sort().map(async(file,index)=>{const raw=await readFile(`content/lessons/${file}`,'utf8');const split=raw.indexOf('\n---\n');if(split<0)throw Error(`Missing metadata separator: ${file}`);const meta=JSON.parse(raw.slice(0,split));return {...meta,number:index+1,slug:file.replace('.md',''),url:`/course/${file.replace('.md','')}/`,body:raw.slice(split+5)};}));}
