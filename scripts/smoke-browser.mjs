import { chromium } from 'playwright';import fs from 'node:fs';
const browser=await chromium.launch();const page=await browser.newPage({viewport:{width:1440,height:1000}});fs.mkdirSync('qa/screenshots',{recursive:true});
for(const route of ['','audit/','atlas/','tale/prologue/','atlas/paper/']){await page.goto('http://127.0.0.1:4173/schrodingers_civ/'+route);await page.screenshot({path:'qa/screenshots/'+(route.replaceAll('/','-')||'home')+'desktop.png',fullPage:route===''});console.log(route,await page.title());}
await page.setViewportSize({width:360,height:800});await page.goto('http://127.0.0.1:4173/schrodingers_civ/');await page.screenshot({path:'qa/screenshots/home-phone.png',fullPage:true});await browser.close();
