/* Small, optional enhancements. Every reader and chapter is a real HTML route. */
document.documentElement.classList.add('js');
const menu=document.querySelector('#navigation-dialog');
const opener=document.querySelector('.menu-button');
function openDialog(dialog,button){dialog._opener=button;dialog.showModal();document.body.classList.add('modal-open');button?.setAttribute('aria-expanded','true');}
function closeDialog(dialog){if(dialog.open)dialog.close();}
for(const dialog of document.querySelectorAll('dialog')){
 dialog.addEventListener('keydown',event=>{if(event.key!=='Tab')return;const items=[...dialog.querySelectorAll('a[href],button:not([disabled]),[tabindex="0"]')].filter(el=>el.getClientRects().length);const first=items[0],last=items.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}});
 dialog.addEventListener('click',event=>{const r=dialog.getBoundingClientRect();if(event.target===dialog&&(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom))closeDialog(dialog);});
 dialog.addEventListener('close',()=>{document.body.classList.remove('modal-open');dialog._opener?.setAttribute('aria-expanded','false');dialog._opener?.focus({preventScroll:true});});
}
opener?.addEventListener('click',()=>openDialog(menu,opener));
menu?.querySelector('.close-menu').addEventListener('click',()=>closeDialog(menu));
menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>closeDialog(menu)));
const artwork=document.querySelector('.art-dialog'),artButton=document.querySelector('.art-open');
artButton?.addEventListener('click',()=>openDialog(artwork,artButton));
artwork?.querySelector('.art-close').addEventListener('click',()=>closeDialog(artwork));
const railLinks=[...document.querySelectorAll('.rail a[href^="#"]')];
if(railLinks.length&&'IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting){for(const a of railLinks)a.classList.toggle('active',a.hash==='#'+entry.target.id);}},{rootMargin:'-15% 0px -70% 0px'});railLinks.forEach(a=>{const el=document.getElementById(a.hash.slice(1));if(el)observer.observe(el);});}
const activeChapter=document.querySelector('.rail a[aria-current="page"]');
if(activeChapter){const rail=document.querySelector('.rail');rail.scrollTop=Math.max(0,activeChapter.offsetTop-rail.clientHeight/2);}
for(const viewer of document.querySelectorAll('[data-viewer]')){
 const viewport=viewer.querySelector('.viewer-window'),img=viewport.querySelector('img'),status=viewer.querySelector('[data-scale]');
 let scale=1,x=0,y=0,pan=false,pointers=new Map(),lastPinch=null;
 const update=()=>{x=Math.max(-(scale-1)*viewport.clientWidth/2,Math.min((scale-1)*viewport.clientWidth/2,x));y=Math.max(-(scale-1)*viewport.clientHeight/2,Math.min((scale-1)*viewport.clientHeight/2,y));img.style.transform=`translate(${x}px,${y}px) scale(${scale})`;status.textContent=Math.round(scale*100)+'%';};
 const zoom=f=>{scale=Math.max(1,Math.min(20,scale*f));update();};
 viewer.querySelector('[data-zoom="in"]').onclick=()=>zoom(1.5);
 viewer.querySelector('[data-zoom="out"]').onclick=()=>zoom(1/1.5);
 viewer.querySelector('[data-fit]').onclick=()=>{scale=1;x=y=0;update();};
 viewer.querySelector('[data-pan]').onclick=e=>{pan=!pan;e.currentTarget.setAttribute('aria-pressed',String(pan));viewport.classList.toggle('pan-enabled',pan);};
 const move=dir=>{if(dir==='left')x+=80;if(dir==='right')x-=80;if(dir==='up')y+=80;if(dir==='down')y-=80;update();};
 viewer.querySelectorAll('[data-move]').forEach(b=>b.onclick=()=>move(b.dataset.move));
 viewport.addEventListener('keydown',e=>{if(e.altKey||e.metaKey||e.ctrlKey)return;if(['+','=','-','Home','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){e.preventDefault();if(['+','='].includes(e.key))zoom(1.5);else if(e.key==='-')zoom(1/1.5);else if(e.key==='Home'){scale=1;x=y=0;update();}else move(e.key.replace('Arrow','').toLowerCase());}});
 viewport.addEventListener('pointerdown',e=>{if(!pan)return;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});viewport.setPointerCapture(e.pointerId);});
 viewport.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;const old=pointers.get(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===1){x+=e.clientX-old.x;y+=e.clientY-old.y;}else{const [a,b]=[...pointers.values()];const dist=Math.hypot(a.x-b.x,a.y-b.y);if(lastPinch)scale=Math.max(1,Math.min(20,scale*dist/lastPinch));lastPinch=dist;}update();});
 for(const type of ['pointerup','pointercancel','lostpointercapture'])viewport.addEventListener(type,e=>{pointers.delete(e.pointerId);lastPinch=null;});
 window.addEventListener('resize',update);update();
}
const progress=document.querySelector('.reading-progress span');
if(progress){let scheduled=false;const tick=()=>{progress.style.width=(Math.min(1,window.scrollY/Math.max(1,document.documentElement.scrollHeight-window.innerHeight))*100)+'%';scheduled=false;};window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(tick);}},{passive:true});tick();
 document.addEventListener('keydown',e=>{if(!e.altKey||e.ctrlKey||e.metaKey||e.shiftKey||document.querySelector('dialog[open]')||getSelection()?.toString()||e.target.closest('input,textarea,select,[contenteditable]'))return;const next=e.key==='ArrowRight'?'next':e.key==='ArrowLeft'?'prev':null;const a=next&&document.querySelector(`.chapter-pagination a[rel="${next}"]`);if(a){e.preventDefault();location.assign(a.href);}});
}
