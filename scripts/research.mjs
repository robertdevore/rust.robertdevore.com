import {mkdir, writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const urls = [
'https://static.rust-lang.org/dist/channel-rust-stable.toml',
'https://blog.rust-lang.org/2026/09/03/Rust-1.98.1/',
'https://blog.rust-lang.org/2026/08/20/Rust-1.98.0/',
'https://rust-lang.org/governance/teams/lang/',
'https://rust-lang.org/governance/teams/library/',
'https://rust-lang.org/governance/teams/compiler/',
'https://rust-lang.org/governance/teams/dev-tools/',
'https://goals.rust-lang.org/2026/goals.html',
'https://goals.rust-lang.org/2026/roadmaps.html',
'https://lang-team.rust-lang.org/design_notes.html',
'https://rustc-dev-guide.rust-lang.org/borrow_check.html',
'https://doc.rust-lang.org/cargo/reference/unstable.html',
'https://doc.rust-lang.org/unstable-book/language-features/const-trait-impl.html',
'https://doc.rust-lang.org/unstable-book/library-features/allocator-api.html',
'https://doc.rust-lang.org/unstable-book/language-features/unsafe-fields.html',
'https://github.com/rust-lang/a-mir-formality',
'https://github.com/rust-lang/trait-system-refactor-initiative',
'https://github.com/rust-lang/lang-team/tree/master/design-meeting-minutes',
'https://rust-lang.github.io/rfcs/3185-static-async-fn-in-trait.html',
'https://doc.rust-lang.org/std/alloc/trait.Allocator.html',
'https://blog.rust-lang.org/2026/08/21/enabling-next-solver-on-nightly/',
'https://blog.rust-lang.org/inside-rust/2026/08/31/program-management-2026-jul-aug/',
'https://goals.rust-lang.org/2026/polonius.html',
'https://bennolossin.github.io/field-projections-designs/',
'https://github.com/rust-lang/goals/issues/734',
'https://github.com/rust-lang/goals/issues/749',
'https://raw.githubusercontent.com/rust-lang/team/main/teams/types.toml',
'https://github.com/rust-lang/miri',
'https://github.com/obi1kenobi/cargo-semver-checks',
'https://developers.cloudflare.com/workers/static-assets/',
'https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/',
'https://developers.cloudflare.com/workers/configuration/routing/custom-domains/'
];
await mkdir('work/research', {recursive:true});
const results = await Promise.all(urls.map(async url=>{
 try { const r=await fetch(url); const body=await r.text(); const text=body.replace(/<script[\s\S]*?<\/script>/g,'').replace(/<style[\s\S]*?<\/style>/g,'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' '); const id=createHash('sha256').update(url).digest('hex').slice(0,12); await writeFile(`work/research/${id}.txt`,text); return {url,status:r.status,checkedAt:new Date().toISOString(),sha256:createHash('sha256').update(body).digest('hex'),local:id};}catch(e){return {url,error:e.message};}
}));
await writeFile('docs/research/source-checks.json',JSON.stringify(results,null,2)+'\n');
console.log(results.map(r=>`${r.status??'ERR'} ${r.url}`).join('\n'));
