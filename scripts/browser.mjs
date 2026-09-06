import {chromium,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {lessons} from './content.mjs';
const base=process.env.SITE_URL||'http://localhost:4173';
const course=await lessons();
const browser=await chromium.launch(process.env.BROWSER_CHANNEL ? {channel:process.env.BROWSER_CHANNEL} : {});const context=await browser.newContext({viewport:{width:1440,height:1000}});const page=await context.newPage();const errors=[];const failed=[];
page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('requestfailed',r=>failed.push(r.url()));
const checked=[];
try{
for(const route of ['/', '/course/', '/practice/', '/about/',...course.map(l=>l.url)]){const r=await page.goto(base+route);assert.equal(r.status(),200,route);await page.locator('h1').waitFor();assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://rust.robertdevore.com'+route);await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),{message:`horizontal overflow ${route}`}).toBe(true);checked.push(route);}
await page.goto(base+'/');await mkdir('work/qa',{recursive:true});await page.screenshot({path:'work/qa/home-desktop.png',fullPage:true});
await page.keyboard.press('/');await page.locator('#search-input').fill('borrowing');await page.locator('#search-results a').first().waitFor();assert.ok(await page.locator('#search-results a').count()>0);await page.keyboard.press('Escape');await expect(page.locator('#search-dialog')).not.toBeVisible();
await page.goto(base+course[2].url);await page.locator('[data-complete]').click();await page.reload();assert.equal(await page.locator('[data-complete]').getAttribute('aria-pressed'),'true');await page.locator('[data-complete]').click();
await page.locator('details').first().locator('summary').click();assert.equal(await page.locator('details').first().getAttribute('open'),'');await page.reload();assert.equal(await page.locator('h1').textContent(),course[2].title);
const accessibility=[];
for(const route of ['/', '/course/', course[2].url, '/about/']){await page.goto(base+route);const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();accessibility.push({route,violations:result.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))});}
await page.setViewportSize({width:390,height:844});await page.goto(base+'/');await page.screenshot({path:'work/qa/home-mobile.png',fullPage:true});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
for(const l of course){await page.goto(base+l.url);await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),{message:`mobile overflow ${l.url}`}).toBe(true);}
await page.goto(base+course[2].url);await page.locator('.menu-toggle').click();assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'true');await page.keyboard.press('Escape');await expect(page.locator('.menu-toggle')).toHaveAttribute('aria-expanded','false');await page.screenshot({path:'work/qa/lesson-mobile.png',fullPage:true});
await writeFile('work/qa/browser.json',JSON.stringify({base,checked,accessibility,errors,failed,checkedAt:new Date().toISOString()},null,2));
assert.deepEqual(errors,[],'browser console errors');assert.deepEqual(failed,[],'failed requests');assert.ok(accessibility.every(a=>a.violations.length===0),JSON.stringify(accessibility));
console.log(`${checked.length} desktop routes, 28 mobile lessons, search, progress, deep refresh, menus and accessibility passed.`);
}finally{await browser.close();}
