import {chromium} from '@playwright/test';
import {readFile} from 'node:fs/promises';
await import('./howl.mjs');
const browser=await chromium.launch(process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{});
try{const page=await browser.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});const svg=await readFile('showcase/rust-course.svg','utf8');await page.setContent(`<html><head><style>body{margin:0}svg{display:block}</style></head><body>${svg}</body></html>`);await page.evaluate(()=>document.fonts.ready);await page.locator('svg').screenshot({path:'assets/social.png'});}finally{await browser.close();}
console.log('Rasterized the verified Howl social card to assets/social.png.');
