/* Small, optional enhancements. Every reader and chapter is a real HTML route. */
let taleTick=()=>{};
document.documentElement.classList.add('js');
const menu=document.querySelector('#navigation-dialog');
const opener=document.querySelector('.menu-button');
function openDialog(dialog,button){dialog._opener=button;dialog.showModal();document.body.classList.add('modal-open');button?.setAttribute('aria-expanded','true');}
function closeDialog(dialog){if(dialog.open)dialog.close();}
function wireDialog(dialog){if(dialog._wired)return;dialog._wired=true;
 dialog.addEventListener('keydown',event=>{if(event.key!=='Tab')return;const items=[...dialog.querySelectorAll('a[href],button:not([disabled]),[tabindex="0"]')].filter(el=>el.getClientRects().length);const first=items[0],last=items.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}});
 dialog.addEventListener('click',event=>{const r=dialog.getBoundingClientRect();if(event.target===dialog&&(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom))closeDialog(dialog);});
 dialog.addEventListener('close',()=>{document.body.classList.remove('modal-open');dialog._opener?.setAttribute('aria-expanded','false');dialog._opener?.focus({preventScroll:true});});
}
document.querySelectorAll('dialog').forEach(wireDialog);
opener?.addEventListener('click',()=>openDialog(menu,opener));
menu?.querySelector('.close-menu').addEventListener('click',()=>closeDialog(menu));
menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>closeDialog(menu)));
const railLinks=[...document.querySelectorAll('.rail a[href^="#"]')];
if(railLinks.length&&'IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting){for(const a of railLinks)a.classList.toggle('active',a.hash==='#'+entry.target.id);}},{rootMargin:'-15% 0px -70% 0px'});railLinks.forEach(a=>{const el=document.getElementById(a.hash.slice(1));if(el)observer.observe(el);});}
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
let progressEl=document.querySelector('.reading-progress span');
{let scheduled=false;
 const tick=()=>{if(progressEl)progressEl.style.width=(Math.min(1,window.scrollY/Math.max(1,document.documentElement.scrollHeight-window.innerHeight))*100)+'%';scheduled=false;};
 window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(tick);}},{passive:true});
 taleTick=tick;
 document.addEventListener('keydown',e=>{if(!e.altKey||e.ctrlKey||e.metaKey||e.shiftKey||document.querySelector('dialog[open]')||getSelection()?.toString()||e.target.closest('input,textarea,select,[contenteditable]'))return;const next=e.key==='ArrowRight'?'next':e.key==='ArrowLeft'?'prev':null;const a=next&&document.querySelector(`.chapter-pagination a[rel="${next}"]`);if(a){e.preventDefault();go(a.href);}});
}

/* Tale soundtrack. The player is emitted outside #page-shell, so the chapter
   swap below never touches it: one <audio> element serves the whole read and the
   sound is continuous across chapter turns. Storage carries the position across
   a hard load — a reload, landing on a chapter directly, or leaving and coming
   back. Nothing is emitted at all unless src/assets/audio/ has files. */
const taleBtn=document.querySelector('.tale-audio'),taleEl=document.querySelector('.tale-audio-el');
if(taleBtn&&taleEl){
 const tracks=JSON.parse(taleBtn.dataset.tracks||'[]'),KEY='tale-audio',REST=3000,GRACE=600000;
 // Two tiers of memory. sessionStorage is the same-tab record: a reload or a
 // direct landing resumes exactly, intent included. localStorage is the wider
 // one -- close the tab, wander off, come back within GRACE (ten minutes) and
 // the place is still held. Only the position crosses that gap, never the
 // intent: a fresh document carries no user gesture, so a browser would refuse
 // to play anyway. The star waits to be pressed, then picks up where it was.
 const readSession=()=>{try{return JSON.parse(sessionStorage.getItem(KEY))||{};}catch{return {};}};
 const readLocal=()=>{try{const v=JSON.parse(localStorage.getItem(KEY));
  return v&&Number.isFinite(v.ts)&&Date.now()-v.ts<=GRACE?{i:v.i,t:v.t}:{};}catch{return {};}};
 const inTab=readSession(),prior=Number.isInteger(inTab.i)?inTab:readLocal();
 let index=Number.isInteger(prior.i)&&tracks[prior.i]?prior.i:0;
 // wantPlaying is the reader's intent, which outlives the element's paused state:
 // during the rest between the last track and the first the audio is paused, but
 // the star must stay lit and the loop must still resume.
 let wantPlaying=false,restTimer=null;
 const save=()=>{const at={i:index,t:taleEl.currentTime};
  try{sessionStorage.setItem(KEY,JSON.stringify({...at,playing:wantPlaying}));}catch{}
  try{localStorage.setItem(KEY,JSON.stringify({...at,ts:Date.now()}));}catch{}};
 const reflect=()=>{taleBtn.setAttribute('aria-pressed',String(wantPlaying));taleBtn.setAttribute('aria-label',wantPlaying?'Pause background music':'Play background music');};
 // Light the star on intent, but drop it again if the browser refuses to play,
 // so the control never claims sound that is not happening.
 const start=()=>{wantPlaying=true;reflect();return taleEl.play().then(reflect,()=>{wantPlaying=false;reflect();});};
 const stop=()=>{wantPlaying=false;clearTimeout(restTimer);taleEl.pause();reflect();};
 taleEl.volume=0.4;          // background bed, not foreground; adjust to taste
 taleEl.loop=false;          // the ended handler owns looping, so it can rest
 const resuming=!!prior.playing,seek=prior.t>0?prior.t:0;
 // A reader who never presses play pays nothing. One returning to a held
 // position pays for metadata only, so currentTime is already set when they
 // press -- without it the track would sound from zero before seeking.
 taleEl.preload=resuming?'auto':seek?'metadata':'none';
 if(tracks[index]&&taleEl.getAttribute('src')!==tracks[index])taleEl.src=tracks[index];
 const seekThen=after=>taleEl.addEventListener('loadedmetadata',()=>{if(seek&&seek<taleEl.duration)taleEl.currentTime=seek;after&&after();},{once:true});
 taleBtn.addEventListener('click',()=>{wantPlaying?stop():start();save();});
 taleEl.addEventListener('ended',()=>{
  const wrapped=index+1>=tracks.length;
  index=(index+1)%tracks.length;
  taleEl.src=tracks[index];save();
  // The playlist loops with a short rest: after the last track the first returns
  // three seconds later rather than snapping straight back.
  if(wrapped)restTimer=setTimeout(()=>{if(wantPlaying)taleEl.play().then(reflect,reflect);},REST);
  else taleEl.play().then(reflect,reflect);
 });
 addEventListener('pagehide',save);
 setInterval(save,4000);
 if(resuming){seek?seekThen(start):start();}else if(seek){seekThen();}
 reflect();
}

/* Seamless chapter turns. A full page load destroys the <audio> element and its
   buffer, which is why restoring the position alone still left a gap — and on
   Safari and Firefox often refused to resume at all, there being no user gesture
   in the new document. Chapter-to-chapter links are therefore swapped in place:
   only <main> and the rail are replaced, the player is untouched, and the sound
   never stops. Every other link stays a real navigation, so leaving the tale
   tears the document down and the music ends, which is the intended behaviour.
   With JS off, or on any failure, these are ordinary links. */
const CHAPTER=/\/tale\/[^/]+\/$/;
const onChapter=()=>document.body.classList.contains('chapter-page');
const isChapterUrl=u=>{try{const x=new URL(u,location.href);return x.origin===location.origin&&CHAPTER.test(x.pathname);}catch{return false;}};
let navigating=false;
async function go(href,push=true){
 if(!onChapter()||!isChapterUrl(href)||navigating){location.assign(href);return;}
 navigating=true;
 try{
  const res=await fetch(href,{credentials:'same-origin'});
  if(!res.ok)throw new Error('fetch');
  const doc=new DOMParser().parseFromString(await res.text(),'text/html');
  const next=doc.querySelector('main#main'),cur=document.querySelector('main#main');
  if(!next||!cur)throw new Error('shape');
  cur.replaceChildren(...next.childNodes);
  const rail=document.querySelector('.rail'),nextRail=doc.querySelector('.rail');
  if(rail&&nextRail)rail.replaceChildren(...nextRail.childNodes);
  document.title=doc.title;
  if(push)history.pushState({tale:1},'',href);
  scrollTo(0,0);
  mountChapter();
  cur.focus({preventScroll:true});
 }catch{location.assign(href);}
 finally{navigating=false;}
}
document.addEventListener('click',e=>{
 if(e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
 const a=e.target.closest('a[href]');
 if(!a||a.target||a.hasAttribute('download')||!onChapter()||!isChapterUrl(a.href))return;
 e.preventDefault();go(a.href);
});
addEventListener('popstate',()=>{if(onChapter()&&isChapterUrl(location.href))go(location.href,false);else location.reload();});

/* Re-run the bindings that live inside the swapped region. Everything else --
   the menu dialog, the rail observer, the atlas viewer -- is bound once and is
   either outside <main> or absent from chapter pages. */
function mountChapter(){
 const artwork=document.querySelector('.art-dialog'),artButton=document.querySelector('.art-open');
 if(artwork){wireDialog(artwork);artwork.querySelector('.art-close')?.addEventListener('click',()=>closeDialog(artwork));}
 if(artButton&&artwork)artButton.addEventListener('click',()=>openDialog(artwork,artButton));
 progressEl=document.querySelector('.reading-progress span');
 const active=document.querySelector('.rail a[aria-current="page"]'),rail=document.querySelector('.rail');
 if(active&&rail)rail.scrollTop=Math.max(0,active.offsetTop-rail.clientHeight/2);
 taleTick();
}
mountChapter();
