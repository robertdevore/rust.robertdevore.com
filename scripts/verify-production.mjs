import assert from 'node:assert/strict';
import {resolve4} from 'node:dns/promises';
import tls from 'node:tls';
import {writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {lessons,origin} from './content.mjs';
const hostname=new URL(origin).hostname;
const dns=await resolve4(hostname);
const certificate=await new Promise((resolve,reject)=>{const socket=tls.connect({host:hostname,port:443,servername:hostname,rejectUnauthorized:true},()=>{const cert=socket.getPeerCertificate();resolve({authorized:socket.authorized,validFrom:cert.valid_from,validTo:cert.valid_to,subjectAltName:cert.subjectaltname});socket.end();});socket.on('error',reject);socket.setTimeout(15000,()=>socket.destroy(new Error('TLS timeout')));});
const routes=['/','/course/','/practice/','/about/',...(await lessons()).map(l=>l.url)];
const checked=[];
for(const route of routes){const response=await fetch(origin+route);assert.equal(response.status,200,route);const html=await response.text();assert.ok(html.includes(`rel="canonical" href="${origin}${route}"`),route);assert.ok(html.includes(`property="og:url" content="${origin}${route}"`));assert.ok(!/python\.robertdevore\.com|localhost|127\.0\.0\.1/.test(html));checked.push(route);}
const discovery=await(await fetch(origin+'/course-index.json')).json();
assert.equal(discovery.lessons.length,28);
for(const item of discovery.lessons){const r=await fetch(item.markdownUrl);assert.equal(r.status,200);assert.match(r.headers.get('content-type'),/text\/markdown/);assert.equal(r.headers.get('x-robots-tag'),'noindex');assert.ok(r.headers.get('link').includes(item.url));assert.equal(createHash('sha256').update(await r.text()).digest('hex'),item.sha256);}
const assets=[];for(const asset of ['/assets/site.css','/assets/site.js','/assets/social.png','/assets/favicon.svg','/search-index.json','/llms.txt','/llms-full.txt','/course-index.json','/assets/showcase/ownership.svg']){const r=await fetch(origin+asset);assert.equal(r.status,200,asset);assets.push({path:asset,type:r.headers.get('content-type'),bytes:(await r.arrayBuffer()).byteLength});}
const sitemap=await (await fetch(origin+'/sitemap.xml')).text();assert.equal((sitemap.match(/<loc>/g)||[]).length,32);assert.ok(!sitemap.includes('python.'));assert.match(await(await fetch(origin+'/robots.txt')).text(),/Allow: \/\nSitemap: https:\/\/rust\.robertdevore\.com\/sitemap.xml/);
const deep=await fetch(origin+'/course/03-ownership',{redirect:'manual'});assert.equal(deep.status,301);assert.ok(new URL(deep.headers.get('location'),origin).pathname.endsWith('/course/03-ownership/'));
assert.equal((await fetch(origin+'/this-page-does-not-exist/')).status,404);
const http=await fetch('http://'+hostname+'/',{redirect:'manual'});assert.ok([301,302,307,308].includes(http.status));assert.ok(new URL(http.headers.get('location'),'http://'+hostname).protocol==='https:');
const report={verifiedAt:new Date().toISOString(),origin,dns,certificate,routes:checked,assets,verifiedMarkdownExports:28,httpsRedirect:http.status,trailingSlashRedirect:deep.status,notFound:404};
await writeFile('docs/production-verification.json',JSON.stringify(report,null,2)+'\n');console.log('Public DNS, certificate, HTTPS redirect, 32 pages, assets, canonicals, sitemap, robots, deep links and 404 verified.');
