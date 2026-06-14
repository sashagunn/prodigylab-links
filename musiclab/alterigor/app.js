/* ============================================================
   42.0 FM — ALTER IGOR   ·   single-file station engine
   Radio wave and dance are the same phenomenon.
   ============================================================ */
(() => {
'use strict';
const $ = (s) => document.querySelector(s);
const clamp = (v,a,b)=>Math.max(a,Math.min(b,v));
const lerp = (a,b,t)=>a+(b-a)*t;

/* ---------- frequency map ---------- */
const MINF=40.8, MAXF=43.9, TOL=0.16, PXMHZ=300;
const FREQS=[
  {key:'42.0',c:42.0,name:'CARRIER',el:'carrier'},
  {key:'41.2',c:41.2,name:'TRANSMISSIONS',el:'tx'},
  {key:'42.8',c:42.8,name:'THE TRANSMITTER',el:'tw'},
  {key:'43.5',c:43.5,name:'THE LINEAGE',el:'ln'},
];

/* ---------- release data (real ALTER IGOR catalogue) ---------- */
/* SIDE A — the album "42.0 FM" (42.0 FM Records, rel. 06.26.26) + singles */
const SIDE_A=[
  {idx:'01',t:'Searching…',file:'a_01.mp3',rec:'recovered 06.26.26',sig:'pre-signal',tag:'intro'},
  {idx:'02',t:'Ближе',file:'a_02.mp3',rec:'recovered 06.26.26',sig:'contemporary',tag:'neo-soul'},
  {idx:'03',t:'Бёдра',file:'a_03.mp3',rec:'recovered 06.26.26',sig:'hip rotation',tag:'acid jazz'},
  {idx:'04',t:'Атмосфера',file:'a_04.mp3',rec:'recovered 06.26.26',sig:'atmosphere',tag:'neo-soul'},
  {idx:'05',t:'SMSки',file:'a_05.mp3',rec:'recovered 06.26.26',sig:'two-step body',tag:'jazz hip-hop'},
  {idx:'06',t:'Волны',file:'a_06.mp3',rec:'recovered 06.26.26',sig:'wave',tag:'neo-soul'},
  {idx:'07',t:'Свет',file:'a_07.mp3',rec:'recovered 06.26.26',sig:'light',tag:'acid jazz'},
  {idx:'08',t:'PLEASE TURN CASSETTE OVER',file:'a_08.mp3',rec:'end of side a',sig:'flip cue',tag:'↺ side b',flip:true},
  {idx:'—',t:'Рядом',file:'a_09.mp3',rec:'single',sig:'closeness',tag:'single'},
  {idx:'—',t:'Касания',file:'a_10.mp3',rec:'single',sig:'contemporary',tag:'single'},
];
/* SIDE B — the dance album: speed-garage reworks (flip the cassette) */
const SIDE_B=[
  {idx:'01',t:'42 — Speed Garage Club Rework',file:'b_01.mp3',rec:'intercepted',sig:'underground rave',tag:'speed garage'},
  {idx:'02',t:'Ближе — Speed Garage Rework',file:'b_02.mp3',rec:'intercepted',sig:'4×4 body',tag:'speed garage'},
  {idx:'03',t:'Бёдра — Speed Garage Rework',file:'b_03.mp3',rec:'intercepted',sig:'baile',tag:'speed garage'},
  {idx:'04',t:'Атмосфера — Speed Garage Rework',file:'b_04.mp3',rec:'intercepted',sig:'warehouse',tag:'speed garage'},
  {idx:'05',t:'SMSки — Garage Warehouse Cut',file:'b_05.mp3',rec:'intercepted',sig:'4×4',tag:'uk garage'},
  {idx:'06',t:'City Lights — Speed Garage Rework',file:'b_06.mp3',rec:'intercepted',sig:'rave',tag:'speed garage'},
  {idx:'07',t:'Soul Dance — Speed Garage Rework',file:'b_07.mp3',rec:'intercepted',sig:'club soul',tag:'speed garage'},
  {idx:'08',t:'Февральский Огонь — UK Speed Garage',file:'b_08.mp3',rec:'intercepted',sig:'rave',tag:'uk speed garage'},
];

/* HyperFollow smart links (one link → all platforms) */
const LK={
  album:'https://distrokid.com/hyperfollow/alterigor1/420-fm?ref=release',
  ryadom:'https://distrokid.com/hyperfollow/alterigor1/0oPVs9g91aW?ref=release',
  kasaniya:'https://distrokid.com/hyperfollow/alterigor1/h1CIK8JfRMP?ref=release',
};
/* official release covers (DistroKid imgix) */
const CV={
  album:'https://distrokid.imgix.net/http%3A%2F%2Fgather.fandalism.com%2F12876335--81AA0432-5ACA-48D1-A903207FA211BC3F--0--1664959--Coverside1.png?fm=jpg&q=75&w=800&s=2496759fe0a69e8f542e7fb8f588311b',
  kasaniya:'https://distrokid.imgix.net/http%3A%2F%2Fgather.fandalism.com%2F12876335--AC7B0E39-C96E-4603-91011E5D36FE8F40--0--1841649--.png?fm=jpg&q=75&w=800&s=a791e443f226659240aa361e8195c4fb',
  ryadom:'https://distrokid.imgix.net/http%3A%2F%2Fgather.fandalism.com%2F12876335--EB497DC1-3058-4713-B14A2A94901E43AA--0--1998142--.png?fm=jpg&q=75&w=800&s=3fdebc52346011eededcbcf9819000d1',
};
const pad2=n=>String(n).padStart(2,'0');
SIDE_A.forEach((t,i)=>{ t.link = t.t==='Рядом'?LK.ryadom : t.t==='Касания'?LK.kasaniya : LK.album;
  t.cover = t.t==='Рядом'?CV.ryadom : t.t==='Касания'?CV.kasaniya : CV.album;
  t.vid = 'v_'+pad2(i+1)+'.mp4'; });
SIDE_B.forEach((t,i)=>{ t.link = LK.album; t.cover = CV.album; t.vid = 'v_'+pad2((i%8)+1)+'.mp4'; });

const LINEAGE=[
  {no:'01',h:'THE DRUM',tag:'FIRST NETWORK',desc:'The drum was the first network. Africa — message carried between villages by skin and hand. Before the wire, the rhythm.',vis:'./visuals/ln_drum.jpg'},
  {no:'02',h:'THE BALLROOM',tag:'COURTSHIP, ENCODED',desc:'The frame as a transmission protocol. Desire, packetised. Every step a handshake. Restraint as bandwidth.',vis:'./visuals/ln_ballroom.jpg'},
  {no:'03',h:'THE CONTEMPORARY',tag:'',desc:'The present frame. Signal shaped by contrast, form, and intention. Urban rhythm. Clean lines. Culture in motion.',vis:'./visuals/ln_contemporary.jpg'},
  {no:'04',h:'THE FLOOR',tag:'NIGHTCLUB',desc:'The floor holds the frequency. Bodies in motion. Bass as architecture. Light as language. The dancefloor was the first internet.',vis:'./visuals/ln_floor.jpg'},
  {no:'05',h:'THE STAGE',tag:'ALL-STAR SCENE',desc:'Where icons converge. Maximum attention. Collective memory in real time. Energy as a unifying force. Legends aren’t announced, they’re received.',vis:'./visuals/ln_stage.jpg'},
  {no:'∞',h:'42.0 FM',tag:'SIGNAL RECEIVED',desc:'And now — 42.0 FM. The current point of a very old signal. You are receiving it.',final:true,vis:'./visuals/blizhe-poster.jpg'},
];

/* ============================================================
   STATE
   ============================================================ */
const S={
  tuning:42.0, target:42.0, strength:0, locked:null, lastLocked:'42.0',
  side:'A', started:false, lastMove:performance.now(),
  freqsTuned: new Set(['42.0']),
  listenerId:null, visit:0, unlocked:{sideB:false,origin:false}
};

/* memory */
try{
  const raw=JSON.parse(localStorage.getItem('fm42')||'{}');
  S.visit=(raw.visit||0)+1;
  S.listenerId=raw.listenerId||('0x'+Math.floor(Math.random()*0xFFF).toString(16).toUpperCase().padStart(3,'0'));
  S.unlocked=raw.unlocked||S.unlocked;
}catch(e){ S.listenerId='0x'+Math.floor(Math.random()*0xFFF).toString(16).toUpperCase().padStart(3,'0'); S.visit=1; }
function save(){ try{localStorage.setItem('fm42',JSON.stringify({visit:S.visit,listenerId:S.listenerId,unlocked:S.unlocked}));}catch(e){} }
save();
$('#lid').textContent=S.listenerId;
$('#visit').textContent= S.visit>1 ? ('return visit · '+S.visit) : 'first contact';

/* ============================================================
   AUDIO — ether noise (WebAudio) + track previews (native)
   ============================================================ */
let actx, noiseGain, noiseSrc, musicGain, audioOn=false;
let currentTrack=null;
let muted=false;
function applyMute(){ [currentTrack,bed,carrierTrk,sting].forEach(a=>{ if(a) a.muted=muted; }); }
function initAudio(){
  if(audioOn) return; audioOn=true;
  try{
    actx=new (window.AudioContext||window.webkitAudioContext)();
    const len=actx.sampleRate*2, buf=actx.createBuffer(1,len,actx.sampleRate), d=buf.getChannelData(0);
    for(let i=0;i<len;i++) d[i]=(Math.random()*2-1)*0.6;
    noiseSrc=actx.createBufferSource(); noiseSrc.buffer=buf; noiseSrc.loop=true;
    const bp=actx.createBiquadFilter(); bp.type='bandpass'; bp.frequency.value=1600; bp.Q.value=0.6;
    noiseGain=actx.createGain(); noiseGain.gain.value=0;
    noiseSrc.connect(bp); bp.connect(noiseGain); noiseGain.connect(actx.destination);
    noiseSrc.start();
  }catch(e){}
}
function playTrack(file){
  if(!file) return;
  try{
    if(currentTrack){ currentTrack.pause(); currentTrack=null; }
    const a=new Audio('./audio/'+file); a.volume=0; a.loop=true;
    a.play().then(()=>{ let v=0; const f=setInterval(()=>{ v=Math.min(.55,v+.05); a.volume=v; if(v>=.55)clearInterval(f);},60); }).catch(()=>{});
    currentTrack=a;
  }catch(e){}
}
function stopTrack(){ if(currentTrack){ const a=currentTrack; let v=a.volume; const f=setInterval(()=>{v=Math.max(0,v-.08);a.volume=v;if(v<=0){a.pause();clearInterval(f);}},50); currentTrack=null; } }

/* ambient bed — live layer by local time of day (Phase 9) */
let bed=null, bedBase=0.16;
function timeOfDay(){ const h=new Date().getHours();
  if(h>=5&&h<11) return 'dawn'; if(h>=11&&h<19) return 'day'; return 'night'; }
function startBed(){
  const tod=timeOfDay();
  S.night = tod==='night';
  bedBase = tod==='night'?0.12 : tod==='dawn'?0.07 : 0.1;
  try{
    bed=new Audio('./audio/bed_'+tod+'.mp3'); bed.loop=true; bed.volume=0; bed.muted=muted;
    bed.play().then(()=>{ let v=0; const f=setInterval(()=>{ v=Math.min(bedBase,v+0.01); bed.volume=v; if(v>=bedBase)clearInterval(f);},80); }).catch(()=>{});
  }catch(e){}
}
function duckBed(to){ if(bed) bed.volume=lerp(bed.volume,to,0.08); }
let sting=null;
function playSting(){ try{ if(!sting){ sting=new Audio('./audio/sting.mp3'); sting.volume=0.6; } sting.muted=muted; sting.currentTime=0; sting.play().catch(()=>{}); }catch(e){} }

/* ============================================================
   BUILD UI
   ============================================================ */
/* dial ticks */
const band=$('#band');
for(let f=MINF; f<=MAXF+0.001; f+=0.1){
  const x=(f-MINF)*PXMHZ, major=Math.abs(f-Math.round(f))<0.001;
  const t=document.createElement('div'); t.className='tick '+(major?'major':'minor'); t.style.left=x+'px';
  if(major){ const l=document.createElement('div'); l.className='lab'; l.textContent=f.toFixed(0); t.appendChild(l);}
  band.appendChild(t);
}
FREQS.forEach(fr=>{ const m=document.createElement('div'); m.className='stnmark'; m.style.left=((fr.c-MINF)*PXMHZ)+'px'; m.textContent=fr.key; band.appendChild(m); });

/* body video element (BLIZHE) — driven by signalStrength in frame loop */
const bodyvid=$('#bodyvid');

/* CARRIER signal dust — light amber particles reacting to tuning */
let dust=null;
function initDust(){
  const cv=$('#cdust'); if(!cv) return;
  const ctx=cv.getContext('2d'); const dpr=Math.min(devicePixelRatio,1.5);
  let W=0,H=0; const parts=[];
  function resize(){ W=cv.width=cv.clientWidth*dpr; H=cv.height=cv.clientHeight*dpr; }
  resize(); window.addEventListener('resize',resize);
  const N=innerWidth<640?32:64;
  for(let i=0;i<N;i++) parts.push({x:Math.random(),y:Math.random(),r:Math.random()*1.6+0.4,s:Math.random()*0.0006+0.0002,d:Math.random()*6.28});
  dust={ step(strength,onCarrier){
    ctx.clearRect(0,0,W,H);
    if(!onCarrier) return;
    const a=0.1+strength*0.5;
    for(const p of parts){ p.y-=p.s*(0.5+strength); p.x+=Math.sin(p.d+p.y*6)*0.0003;
      if(p.y<-0.02){ p.y=1.02; p.x=Math.random(); }
      ctx.beginPath(); ctx.arc(p.x*W,p.y*H,p.r*dpr,0,6.28);
      ctx.fillStyle='rgba(232,176,75,'+(a*(0.4+p.r/2)).toFixed(3)+')'; ctx.fill(); }
  }};
}

/* platform icons (monochrome, tint with accent on hover) */
const PLAT=[
  ['Spotify','<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="currentColor"/><path d="M5.8 9.2c4-1.1 8.3-.8 11.8 1.1M6.4 12.7c3.3-.9 6.7-.6 9.6 1.1M7 15.9c2.5-.6 5-.4 7.2.9" stroke="#0b0b0d" stroke-width="1.5" fill="none" stroke-linecap="round"/></svg>'],
  ['Apple Music','<svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5.5" fill="currentColor"/><path d="M10 15.2V8.4l5-1.1v6" stroke="#0b0b0d" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="8.6" cy="15.4" r="1.8" fill="#0b0b0d"/><circle cx="14.6" cy="14.1" r="1.8" fill="#0b0b0d"/></svg>'],
  ['YouTube','<svg viewBox="0 0 24 24"><rect x="2" y="5.5" width="20" height="13" rx="4" fill="currentColor"/><path d="M10 9.2l5.2 2.8L10 14.8z" fill="#0b0b0d"/></svg>'],
  ['SoundCloud','<svg viewBox="0 0 24 24" fill="currentColor"><rect x="3" y="11" width="1.7" height="6" rx=".8"/><rect x="6" y="9" width="1.7" height="8" rx=".8"/><rect x="9" y="7" width="1.7" height="10" rx=".8"/><rect x="12" y="9.5" width="1.7" height="7.5" rx=".8"/><path d="M15.2 8.2a5 5 0 0 1 4.8 5.3 3.6 3.6 0 0 1-3.6 3.5h-1.2z"/></svg>'],
  ['Yandex Music','<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="currentColor"/><path d="M13.2 6.5h1.6v11h-1.6v-4.3c-3 0-5-1.2-5-3.4 0-1.9 1.5-3.3 4.4-3.3zm0 1.4c-1.8 0-2.7.8-2.7 1.9 0 1.2 1 1.8 2.7 1.8z" fill="#0b0b0d"/></svg>'],
];
function platHTML(url){ const u=url||'#';
  return PLAT.map(p=>`<a class="plat" href="${u}" target="_blank" rel="noopener" title="${p[0]} — via HyperFollow" aria-label="${p[0]}" onclick="event.stopPropagation()">${p[1]}</a>`).join(''); }

/* transmissions grid */
function renderTX(){
  const data = S.side==='A'?SIDE_A:SIDE_B;
  const g=$('#txgrid'); g.innerHTML='';
  data.forEach((tr,i)=>{
    const row=document.createElement('div'); row.className='tx-row'+(tr.flip?' flip-row':''); row.dataset.idx=tr.idx;
    if(tr.flip){
      row.innerHTML=`<div class="tx-cover" style="background-image:url('${tr.cover}')"><span class="num">↺</span></div>
        <div><div class="ttl">${tr.t}</div>
        <div class="meta" style="opacity:1;height:auto;margin-top:5px">END OF SIDE A · CLICK TO FLIP THE CASSETTE</div></div>
        <div class="tag">${tr.tag}</div>`;
      row.addEventListener('click',flipCassette);
    } else {
      row.innerHTML=`<div class="tx-cover" style="background-image:url('${tr.cover}')"><span class="num">${tr.idx}</span><span class="eq"><i></i><i></i><i></i></span></div>
        <div><div class="ttl">${tr.t}</div>
        <div class="meta">RECOVERED ${tr.rec} · ORIGIN 42.0 FM · SIGNATURE ${tr.sig}</div>
        <div class="links">${platHTML(tr.link)}</div></div>
        <div class="tag">${tr.tag}</div>`;
      row.addEventListener('mouseenter',()=>selectIntercept(i));
      row.addEventListener('click',()=>selectIntercept(i));
    }
    g.appendChild(row);
  });
  const p=$('#txprog'); p.innerHTML=''; for(let i=0;i<data.length;i++){ const b=document.createElement('i'); p.appendChild(b);}
}
let focusedIdx=-1, albumOn=false;
function curData(){ return S.side==='A'?SIDE_A:SIDE_B; }
function nextRealIdx(i){
  const data=curData();
  for(let k=0;k<data.length;k++){ i=(i+1)%data.length; if(!data[i].flip) return i; }
  return 0;
}
function highlightRow(i){
  const rows=[...document.querySelectorAll('.tx-row')];
  rows.forEach(r=>r.classList.remove('foc'));
  const row=rows[i];
  if(row){ row.classList.add('foc','recovering'); setTimeout(()=>row.classList.remove('recovering'),900);
    try{ row.scrollIntoView({block:'nearest',behavior:'smooth'}); }catch(e){} }
  const bars=$('#txprog').children;
  for(let j=0;j<bars.length;j++) bars[j].classList.toggle('on', j<=i);
  const data=curData(), tr=data[i], np=$('#txnowttl');
  if(np && tr) np.textContent = tr.t + (tr.tag ? (' · '+tr.tag) : '');
  const npv=$('#npvid');
  if(npv && tr && tr.vid){ const src='./visuals/'+tr.vid;
    if(npv.getAttribute('src')!==src) npv.setAttribute('src',src); }
}
/* play one intercept; when it ends, auto-advance to the next (album mode) */
function playIntercept(i){
  const data=curData();
  if(i<0||i>=data.length) i=0;
  if(data[i] && data[i].flip) i=nextRealIdx(i);
  focusedIdx=i; highlightRow(i);
  const tr=data[i]; if(!tr||!tr.file) return;
  stopTrack();
  const a=new Audio('./audio/'+tr.file); a._file=tr.file; a.loop=false; a.volume=0; a.muted=muted;
  a.addEventListener('ended',()=>{ if(albumOn) playIntercept(nextRealIdx(focusedIdx)); });
  a.play().catch(()=>{});           // volume is ramped by manageMusic (radio mix)
  currentTrack=a;
}
/* hover / click an intercept — hijack the playhead there, keep auto-advance */
function selectIntercept(i){ if(!S.started) return; albumOn=true; playIntercept(i); }

/* lineage */
const lt=$('#lntrack');
LINEAGE.forEach(s=>{ const d=document.createElement('div'); d.className='ln-slide'+(s.final?' final':'');
  const img = s.vis ? `<img src="${s.vis}" alt="" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">` : '';
  const slotStyle = s.vis ? ' style="display:none"' : '';
  const tag = s.tag ? ` <span class="ln-tag">/ ${s.tag}</span>` : '';
  d.innerHTML=`<div class="ln-meta">
      <div class="sectlabel">43.5 · the lineage · ${s.no}</div>
      <h3 class="ln-title">${s.h}${tag}</h3>
      <div class="ln-sub">${s.desc}</div>
    </div>
    <div class="ln-vis">${img}<div class="slot"${slotStyle}>[ ${s.h} — visual slot ]</div></div>`;
  lt.appendChild(d); });

/* ============================================================
   INPUT — tuning
   ============================================================ */
function nudge(d){ S.target=clamp(S.target+d,MINF,MAXF); S.lastMove=performance.now(); hideHint(); }
const lnStage=$('#lntrack');
function inLineage(t){ return S.locked==='43.5' && t && t.closest && t.closest('#ln'); }
window.addEventListener('wheel',e=>{ if(!S.started)return; e.preventDefault();
  if(inLineage(e.target)){ lnStage.scrollLeft += (Math.abs(e.deltaY)>Math.abs(e.deltaX)?e.deltaY:e.deltaX)*1.1; return; }
  nudge(e.deltaY*0.0009); },{passive:false});
function lnGo(dir){ if(lnStage) lnStage.scrollBy({left:dir*lnStage.clientWidth,behavior:'smooth'}); }
const _lp=$('#lnPrev'), _ln=$('#lnNext');
if(_lp) _lp.addEventListener('click',e=>{ e.stopPropagation(); lnGo(-1); });
if(_ln) _ln.addEventListener('click',e=>{ e.stopPropagation(); lnGo(1); });
window.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'){nudge(0.03);} else if(e.key==='ArrowLeft'){nudge(-0.03);}
  origCode(e);
});
let dragging=false,lastX=0;
function down(x){ if(!S.started)return; dragging=true; lastX=x; }
function move(x){ if(!dragging)return; nudge(-(x-lastX)*0.0042); lastX=x; }
function up(){ dragging=false; }
window.addEventListener('mousedown',e=>down(e.clientX));
window.addEventListener('mousemove',e=>move(e.clientX));
window.addEventListener('mouseup',up);
window.addEventListener('touchstart',e=>down(e.touches[0].clientX),{passive:true});
window.addEventListener('touchmove',e=>{ if(dragging){e.preventDefault();} move(e.touches[0].clientX); },{passive:false});
window.addEventListener('touchend',up);

let hintHidden=false;
function hideHint(){ if(hintHidden)return; hintHidden=true; gsap.to('#dialhint',{opacity:0,duration:.6}); }

/* ============================================================
   RENDER LOOP
   ============================================================ */
const root=document.documentElement;
const layers={}; FREQS.forEach(f=>layers[f.key]=$('#'+f.el));
const barsEl=$('#bars'); for(let i=0;i<7;i++) barsEl.appendChild(document.createElement('i'));
let whisperShown=false;

function frame(now){
  S.tuning=lerp(S.tuning,S.target,0.12);
  /* proximity per freq */
  let best=null,bestP=0;
  FREQS.forEach(f=>{
    const p=clamp(1-Math.abs(S.tuning-f.c)/TOL,0,1);
    layers[f.key].style.opacity=Math.pow(p,0.8).toFixed(3);
    layers[f.key].classList.toggle('live',p>0.5);
    if(p>bestP){bestP=p;best=f;}
  });
  const locked = bestP>0.02 ? best : null;
  S.strength=bestP; S.locked=locked?locked.key:null;
  if(locked){ S.lastLocked=locked.key; S.freqsTuned.add(locked.key); }

  root.style.setProperty('--strength',S.strength.toFixed(3));
  root.style.setProperty('--noise',(1-S.strength).toFixed(3));

  /* HUD */
  $('#freqVal').textContent=S.tuning.toFixed(1)+' MHz';
  $('#freqName').textContent= locked? locked.name : '· · · scanning · · ·';
  const lit=Math.round(S.strength*7);
  for(let i=0;i<7;i++) barsEl.children[i].classList.toggle('on',i<lit);

  /* dial position */
  band.style.transform='translateX('+(window.innerWidth/2-(S.tuning-MINF)*PXMHZ)+'px)';

  /* body video resolves from static as the carrier locks in */
  if(bodyvid){
    const st=S.strength;
    bodyvid.style.filter='contrast('+(1.02+st*0.3).toFixed(2)+') brightness('+(0.58+st*0.45).toFixed(2)+') blur('+((1-st)*5).toFixed(1)+'px)';
    const sil=$('#silhouette'); if(sil) sil.style.opacity=(0.3+st*0.7).toFixed(2);
  }
  // headline glitch resolve: RGB split shrinks to zero as you lock 42.0
  root.style.setProperty('--gl', (S.locked==='42.0'?(1-S.strength):0.85).toFixed(3));
  // carrier signal dust reacts to tuning
  if(dust) dust.step(S.strength, S.locked==='42.0');

  /* ether noise gain — very subtle, and gone entirely near a station */
  if(noiseGain){
    const target=muted?0:Math.pow(Math.max(0,1-S.strength*1.5),2)*0.05;
    noiseGain.gain.value=lerp(noiseGain.gain.value,target,0.12);
  }

  /* transmitter is now the album tower art (static image + CSS wavefronts) */

  /* dead-frequency whisper */
  const idle=now-S.lastMove;
  if(!locked && idle>6000 && !whisperShown && S.started){ showWhisper(); }
  if(locked || idle<6000){ whisperShown=false; $('#whisper').style.opacity=0; }

  /* track preview when a transmission is focused & locked */
  manageMusic();

  requestAnimationFrame(frame);
}

function manageMusic(){
  // continuous radio: the station never stops — only its loudness/clarity changes
  // with how well you're tuned. Loudest on 41.2 (the playlist), present everywhere else.
  if(currentTrack){
    let base = S.locked==='41.2'?0.6 : S.locked==='42.0'?0.45 : (S.locked?0.32:0.18);
    base *= (0.55+S.strength*0.45);
    currentTrack.volume = muted?0:lerp(currentTrack.volume, base, 0.06);
  }
  // ambient bed sits faintly underneath; rises a touch in the dead air
  duckBed(S.locked ? 0.03 : 0.08);
  // the now-playing monitor only runs while the playlist (41.2) is on screen
  const npv=$('#npvid');
  if(npv){ if(S.locked==='41.2'){ if(npv.paused && npv.getAttribute('src')) npv.play().catch(()=>{}); }
           else if(!npv.paused){ npv.pause(); } }
}

const WHISPERS={
  '42.0':'you came in on the carrier. most people never hear it.',
  '41.2':'the intercept you just touched — it was addressed to no one. now it has you.',
  '42.8':'the tower felt you stop. it is listening back.',
  '43.5':'you stood inside the lineage. the drum remembers your weight.',
};
function showWhisper(){
  whisperShown=true;
  const w=$('#whisper'); w.textContent=WHISPERS[S.lastLocked]||'the static is not empty. it is waiting.';
  w.style.opacity=1;
}

/* ============================================================
   CARRIER intro (gsap)
   ============================================================ */
function intro(){
  const tl=gsap.timeline();
  if(S.visit>1){
    $('#c1').textContent='You came back.';
    $('#c2').textContent='The signal never stopped — listener '+S.listenerId+'.';
  }
  tl.set([ '#c1','#c2','#c3'],{opacity:0,y:14})
    .to('#carrier',{opacity:1,duration:.6})
    .to('#c1',{opacity:1,y:0,duration:1.1},'+=0.4')
    .to('#c2',{opacity:1,y:0,duration:1.1},'+=1.2')
    .to('#c3',{opacity:.9,y:0,duration:1.4},'+=0.8')
    .add(()=>{ gsap.to('#dialhint',{opacity:1,duration:.8}); },'+=0.6');
}

/* ============================================================
   CASSETTE — Side A / Side B
   ============================================================ */
function flipCassette(){
  $('#cassette').classList.toggle('flip');
  S.side = S.side==='A'?'B':'A';
  document.body.classList.toggle('sideB', S.side==='B');
  $('#cassidehint').textContent = S.side==='A'?'Side A':'Side B';
  if(S.side==='B'){ S.unlocked.sideB=true; save(); }
  stopTrack(); focusedIdx=-1; renderTX();
  playSting();
  albumOn=true; playIntercept(0);   // restart the station on the flipped side
  flash(S.side==='B'?'PLEASE TURN CASSETTE OVER · SIDE B':'SIDE A');
}
$('#cassette').addEventListener('click',flipCassette);
function flash(txt){
  const w=$('#whisper'); w.textContent=txt; w.style.opacity=1;
  setTimeout(()=>{ if(!whisperShown) w.style.opacity=0; },1400);
}

/* ============================================================
   420 origin code
   ============================================================ */
let codeBuf='';
function origCode(e){
  if(/^[0-9]$/.test(e.key)){ codeBuf=(codeBuf+e.key).slice(-3); if(codeBuf==='420'){ openOrigin(); } }
}
function openOrigin(){ S.unlocked.origin=true; save(); $('#origin').classList.add('show'); }
$('#originX').addEventListener('click',()=>$('#origin').classList.remove('show'));

/* ============================================================
   THREE.JS — THE TRANSMITTER
   ============================================================ */
const tw={ready:false};
function initTransmitter(){
  if(tw.ready||typeof THREE==='undefined')return;
  const canvas=$('#twcanvas');
  const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.6));
  const scene=new THREE.Scene();
  scene.fog=new THREE.FogExp2(0x070708,0.045);
  const cam=new THREE.PerspectiveCamera(56,1,0.1,120); cam.position.set(0,2.6,11.5);
  const mobile=innerWidth<640;
  const accent=new THREE.Color(0xE8B04B);

  // soft radial glow sprite texture
  const gtex=(()=>{ const c=document.createElement('canvas'); c.width=c.height=64; const g=c.getContext('2d');
    const grd=g.createRadialGradient(32,32,0,32,32,32);
    grd.addColorStop(0,'rgba(255,231,178,1)'); grd.addColorStop(.3,'rgba(232,176,75,.55)'); grd.addColorStop(1,'rgba(232,176,75,0)');
    g.fillStyle=grd; g.fillRect(0,0,64,64); const t=new THREE.Texture(c); t.needsUpdate=true; return t; })();
  const add=THREE.AdditiveBlending;

  // atmosphere glow behind the tower
  const atmo=new THREE.Sprite(new THREE.SpriteMaterial({map:gtex,color:accent,transparent:true,opacity:.28,blending:add,depthWrite:false}));
  atmo.scale.set(19,28,1); atmo.position.set(0,2.2,-1); scene.add(atmo);
  // soft light pool on the floor — fills the lower frame
  const pool=new THREE.Mesh(new THREE.CircleGeometry(17,48),
    new THREE.MeshBasicMaterial({map:gtex,color:accent,transparent:true,opacity:.22,blending:add,depthWrite:false}));
  pool.rotation.x=-Math.PI/2; pool.position.y=-1.98; scene.add(pool);

  // tower: glowing pillar + light beam + beacon
  const towerG=new THREE.Group(); scene.add(towerG);
  const pillar=new THREE.Mesh(new THREE.CylinderGeometry(0.035,0.07,6.4,12),
    new THREE.MeshBasicMaterial({color:accent,transparent:true,opacity:.85,blending:add,depthWrite:false}));
  pillar.position.y=1.2; towerG.add(pillar);
  const beam=new THREE.Mesh(new THREE.CylinderGeometry(0.012,0.75,12,20,1,true),
    new THREE.MeshBasicMaterial({color:accent,transparent:true,opacity:.12,blending:add,side:THREE.DoubleSide,depthWrite:false}));
  beam.position.y=3.6; towerG.add(beam);
  const beacon=new THREE.Sprite(new THREE.SpriteMaterial({map:gtex,color:0xffe7b2,transparent:true,opacity:1,blending:add,depthWrite:false}));
  beacon.scale.set(1.3,1.3,1); beacon.position.y=4.5; towerG.add(beacon);

  // radar rings on the ground (fill the frame)
  const rings=[]; const RN=mobile?6:10;
  for(let i=0;i<RN;i++){
    const r=new THREE.Mesh(new THREE.RingGeometry(1,1.045,96),
      new THREE.MeshBasicMaterial({color:accent,transparent:true,opacity:0,side:THREE.DoubleSide,blending:add,depthWrite:false}));
    r.rotation.x=-Math.PI/2; r.position.y=-2; r.userData.phase=i/RN; scene.add(r); rings.push(r);
  }
  // faint radar spokes
  const spokes=new THREE.Group(); spokes.position.y=-1.99; scene.add(spokes);
  const SK=mobile?6:12;
  for(let i=0;i<SK;i++){ const a=(i/SK)*Math.PI*2;
    const sg=new THREE.Mesh(new THREE.PlaneGeometry(17,0.012),
      new THREE.MeshBasicMaterial({color:accent,transparent:true,opacity:.05,blending:add,depthWrite:false}));
    sg.rotation.x=-Math.PI/2; sg.rotation.z=a; sg.position.set(Math.cos(a)*8.5,0,Math.sin(a)*8.5); spokes.add(sg); }

  // signal-dust particles drifting up
  const pc=mobile?140:420;
  const pg=new THREE.BufferGeometry(); const pos=new Float32Array(pc*3); const spd=new Float32Array(pc);
  for(let i=0;i<pc;i++){ const ang=Math.random()*Math.PI*2, rad=Math.random()*12;
    pos[i*3]=Math.cos(ang)*rad; pos[i*3+1]=Math.random()*12-2.5; pos[i*3+2]=Math.sin(ang)*rad; spd[i]=0.004+Math.random()*0.012; }
  pg.setAttribute('position',new THREE.BufferAttribute(pos,3));
  const pm=new THREE.PointsMaterial({map:gtex,color:accent,size:mobile?0.3:0.36,sizeAttenuation:true,transparent:true,opacity:.6,blending:add,depthWrite:false});
  const particles=new THREE.Points(pg,pm); scene.add(particles);

  // track nodes as glowing sprites riding the wavefronts
  const nodes=[]; const NN=mobile?6:10;
  for(let i=0;i<NN;i++){
    const n=new THREE.Sprite(new THREE.SpriteMaterial({map:gtex,color:accent,transparent:true,opacity:.9,blending:add,depthWrite:false}));
    n.scale.set(0.55,0.55,1); n.userData={a:(i/NN)*Math.PI*2,rad:2.5+Math.random()*7,sp:0.15+Math.random()*0.25};
    scene.add(n); nodes.push(n);
  }

  function resize(){ const w=canvas.clientWidth||innerWidth,h=canvas.clientHeight||innerHeight;
    renderer.setSize(w,h,false); cam.aspect=w/h; cam.updateProjectionMatrix(); }
  resize(); window.addEventListener('resize',resize);

  let t=0;
  tw.render=(strength,active)=>{
    t+=0.016;
    const k=0.4+strength*0.6;
    beacon.material.opacity=(0.5+0.5*Math.abs(Math.sin(t*2.4)))*k;
    pillar.material.opacity=0.45+strength*0.45;
    beam.material.opacity=0.06+strength*0.12;
    atmo.material.opacity=0.16+strength*0.24;
    rings.forEach(r=>{ const ph=(r.userData.phase+t*(0.05+strength*0.15))%1; const sc=0.4+ph*15;
      r.scale.set(sc,sc,sc); r.material.opacity=(1-ph)*(1-ph)*0.6*k; });
    const p=pg.attributes.position.array;
    for(let i=0;i<pc;i++){ p[i*3+1]+=spd[i]*(0.6+strength); if(p[i*3+1]>9.5) p[i*3+1]=-2.5; }
    pg.attributes.position.needsUpdate=true;
    pm.opacity=0.3+strength*0.5;
    pool.material.opacity=0.12+strength*0.2;
    nodes.forEach(n=>{ n.userData.a+=n.userData.sp*0.006*(0.5+strength);
      n.position.set(Math.cos(n.userData.a)*n.userData.rad,-1.9+Math.sin(t*0.8+n.userData.a)*0.25,Math.sin(n.userData.a)*n.userData.rad);
      n.material.opacity=0.4+strength*0.6; });
    spokes.rotation.y=t*0.04;
    const ang=t*0.06;
    cam.position.set(Math.sin(ang)*11.5, 2.5+Math.sin(t*0.3)*0.3, Math.cos(ang)*11.5);
    cam.lookAt(0,1.7,0);
    renderer.render(scene,cam);
  };
  tw.ready=true;
}

/* ============================================================
   CALLSIGN
   ============================================================ */
let geoLoc='UNKNOWN ORIGIN';
fetch('https://ipapi.co/json/').then(r=>r.json()).then(j=>{
  if(j&&j.city){ geoLoc=(j.city+', '+(j.region_code||j.country_code||'')).toUpperCase(); }
}).catch(()=>{});

/* mute toggle — silences tracks, bed, carrier & ether noise */
const SP_ON='<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor" stroke="none"/><path d="M16.5 8.5a5 5 0 0 1 0 7"/><path d="M18.9 6.2a8 8 0 0 1 0 11.6"/></svg>';
const SP_OFF='<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor" stroke="none"/><line x1="16.5" y1="9.5" x2="21.5" y2="14.5"/><line x1="21.5" y1="9.5" x2="16.5" y2="14.5"/></svg>';
const muteBtn=$('#mute');
function renderMute(){ if(muteBtn){ muteBtn.innerHTML=muted?SP_OFF:SP_ON; muteBtn.classList.toggle('off',muted); muteBtn.setAttribute('title', muted?'sound off — click to unmute':'mute'); } }
renderMute();
if(muteBtn) muteBtn.addEventListener('click',e=>{ e.stopPropagation(); muted=!muted; applyMute(); renderMute(); });

$('#decode').addEventListener('click',openCard);
function openCard(){
  const now=new Date();
  $('#cardId').textContent=S.listenerId;
  $('#cardLoc').textContent=geoLoc;
  $('#cardTime').textContent=now.toTimeString().slice(0,5);
  $('#cardFreqs').textContent=S.freqsTuned.size+' / 4';
  $('#cardSide').textContent=S.side;
  $('#modal').classList.add('show'); $('#mclose').classList.add('show');
}
function closeCard(){ $('#modal').classList.remove('show'); $('#mclose').classList.remove('show'); }
$('#mclose').addEventListener('click',closeCard);
$('#modal').addEventListener('click',e=>{ if(e.target.id==='modal') closeCard(); });
$('#saveImg').addEventListener('click',()=>{
  if(typeof html2canvas==='undefined')return;
  html2canvas($('#card'),{backgroundColor:null,scale:2}).then(cv=>{
    const a=document.createElement('a'); a.download='42fm-callsign-'+S.listenerId+'.png'; a.href=cv.toDataURL(); a.click();
  });
});
$('#shareBtn').addEventListener('click',()=>{
  const txt='I tuned into 42.0 FM. Listener '+S.listenerId+'. Now part of the signal.';
  if(navigator.share){ navigator.share({title:'42.0 FM — ALTER IGOR',text:txt,url:location.href}).catch(()=>{}); }
  else { navigator.clipboard?.writeText(txt+' '+location.href); flash('copied to clipboard'); }
});

/* ============================================================
   GATE / START
   ============================================================ */
$('#gate').addEventListener('click',start,{once:true});
let carrierTrk=null;
function start(){
  S.started=true;
  initAudio();
  startBed();
  if(bodyvid){ bodyvid.play().catch(()=>{}); }
  initDust();
  $('#gate').classList.add('hidden');
  setTimeout(()=>{ const g=$('#gate'); if(g) g.remove(); },1200);
  renderTX();
  albumOn=true; playIntercept(0);   // continuous radio, starts on "Searching…"
  intro();
}

/* ============================================================
   PRELOADER — reveal gate once assets are warm (cap 4s)
   ============================================================ */
(function preload(){
  const pf=$('#pfill'), pp=$('#ppct'), pre=$('#pre');
  let p=0, done=false;
  const tick=setInterval(()=>{ p=Math.min(96,p+Math.random()*16); if(pf)pf.style.width=p+'%'; if(pp)pp.textContent=Math.round(p)+'%'; },180);
  function finish(){ if(done)return; done=true; clearInterval(tick);
    if(pf)pf.style.width='100%'; if(pp)pp.textContent='100%';
    setTimeout(()=>{ if(pre){ pre.style.opacity='0'; setTimeout(()=>pre.remove(),900);} },350); }
  const minWait=setTimeout(()=>{}, 1100);
  let ready=false;
  const fontsP = (document.fonts&&document.fonts.ready)?document.fonts.ready:Promise.resolve();
  fontsP.then(()=>{ ready=true; });
  // finish on window load (min 1.1s) or hard cap 4s
  const cap=setTimeout(finish,4000);
  window.addEventListener('load',()=>setTimeout(finish,1100));
  if(document.readyState==='complete') setTimeout(finish,1200);
})();

/* respect reduced motion: pause heavy bits */
if(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches){
  document.addEventListener('DOMContentLoaded',()=>{ const v=$('#bodyvid'); if(v){ v.removeAttribute('autoplay'); } });
}

requestAnimationFrame(frame);
})();
