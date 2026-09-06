import {readFile,readdir,stat} from 'node:fs/promises';
import assert from 'node:assert/strict';
import path from 'node:path';
import {lessons,origin} from './content.mjs';
const course=await lessons();assert.equal(course.length,28);
const files=[];async function walk(dir){for(const f of await readdir(dir)){const p=path.join(dir,f);if((await stat(p)).isDirectory())await walk(p);else files.push(p);}}await walk('dist');
let links=0;
for(const file of files.filter(f=>f.endsWith('.html'))){const html=await readFile(file,'utf8');assert.match(html,/<html lang="en">/);assert.equal((html.match(/<h1[ >]/g)||[]).length,1,file);assert.match(html,/<link rel="canonical" href="https:\/\/rust\.robertdevore\.com\//);assert.ok(!/python\.robertdevore\.com|localhost|127\.0\.0\.1|\{\{/.test(html),`leaked placeholder or wrong domain: ${file}`);assert.ok(!/(?:src|href)="http:\/\//.test(html),`mixed content ${file}`);
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);assert.equal(new Set(ids).size,ids.length,`duplicate IDs ${file}`);
for(const match of html.matchAll(/(?:href|src)="([^"<>]+)"/g)){let href=match[1].replaceAll('&amp;','&');if(href.startsWith(origin))href=href.slice(origin.length);if(href.startsWith('#')){assert.ok(ids.includes(href.slice(1)),`missing anchor ${href} in ${file}`);continue;}if(!href.startsWith('/'))continue;const [url,fragment]=href.split('#');const target=path.join('dist',url.endsWith('/')?url+'index.html':url);assert.ok(files.includes(target),`${file} missing ${href}`);if(fragment&&target.endsWith('.html')){assert.ok((await readFile(target,'utf8')).includes(`id="${fragment}"`),`missing fragment ${href}`);}links++;}}
for(const l of course){assert.ok(l.body.includes('## Exercise')||l.body.includes('## Your extension')||l.body.includes('## Cancellation exercise'),`missing exercise ${l.slug}`);assert.ok(l.body.includes('<details>'),`missing solution ${l.slug}`);assert.ok(l.body.split(/\s+/).length>350,`thin lesson ${l.slug}`);}
const sitemap=await readFile('dist/sitemap.xml','utf8');assert.equal((sitemap.match(/<loc>/g)||[]).length,32);assert.ok(!sitemap.includes('/404'));
const index=JSON.parse(await readFile('dist/search-index.json'));assert.equal(index.length,28);
console.log(`32 public pages + 404, 28 lesson contracts, metadata, anchors, and ${links} local links verified.`);
