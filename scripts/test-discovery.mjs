import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {lessons,origin} from './content.mjs';
const course=await lessons(),index=JSON.parse(await readFile('dist/course-index.json','utf8'));
assert.equal(index.lessons.length,course.length);const full=await readFile('dist/llms-full.txt','utf8');const headers=await readFile('dist/_headers','utf8');const redirects=await readFile('dist/_redirects','utf8');
for(const l of course){
 const html=await readFile(`dist${l.url}index.html`,'utf8');const data=JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
 const page=data['@graph'].find(x=>x['@id']===origin+l.url+'#webpage');assert.ok(page['@type'].includes('LearningResource'));assert.equal(page.name,l.title);assert.equal(page.url,origin+l.url);
 const bc=data['@graph'].find(x=>x['@type']==='BreadcrumbList');assert.deepEqual(bc.itemListElement.map(x=>x.position),[1,2,3]);assert.equal(bc.itemListElement.at(-1).item,origin+l.url);
 for(const id of Object.values(l.headingIds||{}))assert.ok(html.includes(`id="${id}"`),'renamed heading lost its existing URL');
 const item=index.lessons.find(x=>x.id===l.slug),markdown=await readFile(`dist/lessons/${l.slug}.md`,'utf8');assert.equal(item.sha256,createHash('sha256').update(markdown).digest('hex'));assert.ok(!markdown.includes('{{'));assert.ok(full.includes(markdown));assert.ok(markdown.includes(`Canonical: ${origin}${l.url}`));assert.ok(headers.includes(`Link: <${origin}${l.url}>; rel="canonical"`));assert.ok(redirects.includes(`${l.url.slice(0,-1)} ${l.url} 301`));
 if(l.example)assert.ok(markdown.includes(await readFile(`examples/${l.example}.rs`,'utf8')),'source omitted from Markdown');
 if(l.drill)assert.ok(markdown.includes(await readFile(`drills/expected/${l.drill}.txt`,'utf8')),'diagnostic omitted');
}
for(const route of ['/','/course/','/about/','/practice/']){const html=await readFile(`dist${route}index.html`,'utf8');assert.ok(JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1])['@graph'].some(x=>x['@type']==='WebSite'));}
assert.ok(!index.lessons.some(x=>JSON.stringify(x).includes('localhost')));
console.log('Structured data, canonical breadcrumbs, 28 source-complete Markdown exports, index hashes and permanent redirect contracts verified.');

const home=await readFile('dist/index.html','utf8'),launch=await readFile('dist/assets/rust-course-launch.png');
assert.equal(launch.subarray(1,4).toString(),'PNG');
for(const [name,value] of [['width',launch.readUInt32BE(16)],['height',launch.readUInt32BE(20)]])assert.ok(home.includes(`property="og:image:${name}" content="${value}"`));
assert.ok(home.includes(`property="og:image" content="${origin}/assets/rust-course-launch.png"`));
assert.ok(home.includes(`name="twitter:image" content="${origin}/assets/rust-course-launch.png"`));
assert.ok((await readFile('dist/course/index.html','utf8')).includes(`property="og:image" content="${origin}/assets/social.png"`));
console.log('Homepage share image dimensions, X metadata and preserved section URLs verified.');
