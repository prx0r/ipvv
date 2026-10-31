/* svatantrya app — lab-pattern SPA: one shell, JSON content, zero reloads. */
const API = 'https://ipvv-api.tradesprior.workers.dev';
const $ = s => document.querySelector(s);
const esc = s => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
let LIB = { works: {}, masters: [], sel: null };
let SID = null;
let SPEAK = false;

/* global player: survives route changes, audio keeps playing while you browse */
function playAudio(url, title){
  const p = document.getElementById('player');
  const a = document.getElementById('paudio');
  document.getElementById('ptitle').textContent = title || '—';
  a.src = url; a.play().catch(()=>{});
  p.classList.add('on');
}
document.getElementById('pclose').addEventListener('click', ()=>{
  const a = document.getElementById('paudio');
  a.pause(); a.removeAttribute('src'); a.load();
  document.getElementById('player').classList.remove('on');
});
function listen(text){
  try{
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text.slice(0, 900));
    u.rate = 0.95; speechSynthesis.speak(u);
  }catch(e){}
}
document.getElementById('spk').addEventListener('click', function(){
  SPEAK = !SPEAK;
  this.textContent = SPEAK ? '🔊' : '🔈';
  if(!SPEAK){ try{ speechSynthesis.cancel(); }catch(e){} }
});
/* mic: speak your question */
(function(){
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR) { document.getElementById('mic').style.display='none'; return; }
  const vr = new SR(); vr.lang='en-US'; vr.interimResults=false;
  vr.onresult = e => {
    document.getElementById('askQ').value = e.results[0][0].transcript;
    document.getElementById('ask').requestSubmit();
  };
  vr.onerror = ()=>{};
  document.getElementById('mic').addEventListener('click', ()=>{
    try{ vr.start(); }catch(e){}
  });
})();

async function nav(){
  let mhtml = `<a href="#/practice">practise</a><a href="#/library">library</a>`;
  document.getElementById('menu').innerHTML = mhtml;
  document.querySelectorAll('#menu a[href^="#/"]').forEach(a=>{
    a.addEventListener('click', ()=>{ document.getElementById('menu').classList.remove('open'); });
  });
}
async function showWorks(m, boxSel){
  let w = LIB.works[m];
  if(!w){
    try{ w = await get(`/data/works_${m}.json`); LIB.works[m]=w; }catch(e){ return; }
  }
  if(!LIB.index){
    try{ LIB.index = await get('/data/works-index.json'); }catch(e){ LIB.index = {}; }
  }
  const idx = LIB.index || {};
  const box = document.querySelector(boxSel || '#lib-works');
  if(!box) return;
  box.innerHTML = `<div class="msec">${esc(m)}</div><div class="mgrid">` +
    ((Array.isArray(w)?w:[]).map(x=>{
      const wid = x.id||x.work||m;
      const rec = idx[m+':'+wid] || {};
      const target = rec.translation || wid;
      const hasEn = !!rec.translation;
      const hasSa = !!rec.sanskrit;
      const mark = hasEn ? '' : (hasSa ? ' °' : ' ·');
      return `<a class="mcard" href="#/work/${target}" data-wid="${esc(wid)}">${esc(x.title||x.id||'')}<span class="sub">${mark}</span></a>`;
    }).join('') || '<span class="sub">no works</span>') + `</div>`;
}
async function get(p){
  const r = await fetch(p);
  if(!r.ok) throw 0;
  const ct = r.headers.get('content-type')||'';
  return ct.includes('json') ? r.json() : r.text();
}
const routes = {
  '/': home, '/library': library, '/practice': practices,
};
async function router(){
  const h = location.hash.slice(1) || '/';
  const [path] = h.split('?');
  const bar = document.getElementById('askbar');
  if(bar) bar.style.display = (path === '/' ? 'none' : '');
  const fn = routes[path] || (path.startsWith('/work/') ? work : (path.startsWith('/probe/') ? probe : notfound));
  nav();
  $('#view').innerHTML = '<p style="color:#999">…</p>';
  try { await fn(path); } catch(e){ $('#view').innerHTML = '<p>Could not load. <a href="#/">home</a></p>'; }
  window.scrollTo(0,0);
}
function home(){
  $('#view').innerHTML = `<div id="answer" style="display:none"></div>`;
}
async function library(){
  $('#view').innerHTML = `<div id="libwrap" style="display:flex;gap:1.5rem;align-items:flex-start"><div id="lib-masters" style="min-width:11rem"><div class="msec">Masters</div><div id="lib-mlist"><span class="sub">…</span></div></div><div id="lib-works" style="flex:1;min-width:0"></div></div><div id="answer" style="display:none"></div>`;
  let ms = LIB.masters;
  if(!ms.length){
    try{
      const sec = await get('/data/sections.json');
      ms = ((sec.sections||[]).find(s=>s.id==='masters')||{}).members || [];
      LIB.masters = ms;
    }catch(e){ ms = []; }
  }
  const counts = {};
  await Promise.all(ms.map(async m=>{
    try{ const w = await get(`/data/works_${m}.json`); counts[m]=Array.isArray(w)?w.length:0; LIB.works[m]=w; }catch(e){ counts[m]=0; }
  }));
  const sorted = [...ms].sort((a,b)=>(counts[b]||0)-(counts[a]||0));
  const box = document.getElementById('lib-mlist');
  if(!box) return;
  box.innerHTML = `<div class="mgrid">` + sorted.map(m=>`<a href="#" data-libm="${esc(m)}" class="mcard">${esc(m)} <span class="sub">· ${counts[m]||0}</span></a>`).join('') + `</div>`;
  box.querySelectorAll('[data-libm]').forEach(a=>{
    const open = (e)=>{ if(e) e.preventDefault(); showWorks(a.getAttribute('data-libm'), '#lib-works'); };
    a.addEventListener('click', open);
    a.addEventListener('mouseenter', ()=>{ if(window.matchMedia('(pointer:fine)').matches) showWorks(a.getAttribute('data-libm'), '#lib-works'); });
  });
  if(sorted.length) showWorks(sorted[0], '#lib-works');
}

let KAR = { audio: null, timer: null, cur: null };
// shared ereader: IAST glyphs + cleanSA
/* IAST -> Devanagari, deterministic longest-match. No dependencies. */
const IAST_DEVA = (()=>{
  const VOW={a:'\u0905','\u0101':'\u0906',i:'\u0907','\u012b':'\u0908',u:'\u0909','\u016b':'\u090a','\u1e5b':'\u090b','\u1e5d':'\u090c','\u1e37':'\u090d',e:'\u090f',o:'\u0913',ai:'\u0910',au:'\u0914'};
  const VSN={'\u0101':'\u093e',i:'\u093f','\u012b':'\u0940',u:'\u0941','\u016b':'\u0942','\u1e5b':'\u0943','\u1e5d':'\u0944','\u1e37':'\u0962',e:'\u0947',o:'\u094b',ai:'\u0948',au:'\u094c'};
  const CON={k:'\u0915',kh:'\u0916',g:'\u0917',gh:'\u0918','\u014b':'\u0919',c:'\u091a',ch:'\u091b',j:'\u091c',jh:'\u091d','\u00f1':'\u091e','\u1e6d':'\u091f','\u1e6dh':'\u0920','\u1e0d':'\u0921','\u1e0dh':'\u0922','\u1e47':'\u0923',t:'\u0924',th:'\u0925',d:'\u0926',dh:'\u0927',n:'\u0928',p:'\u092a',ph:'\u092b',b:'\u092c',bh:'\u092d',m:'\u092e',y:'\u092f',r:'\u0930',l:'\u0932',v:'\u0935','\u015b':'\u0936','\u1e63':'\u0937',s:'\u0938',h:'\u0939'};
  const OTH={'\u1e43':'\u0902','\u1e41':'\u0902','\u1e25':'\u0903',"'":'\u093d','\u2019':'\u093d','.':'\u0964','..':'\u0965','|':'\u0964','||':'\u0965',' ':' ','\n':'\n','\u2014':'\u0964'};
  const HAL='\u094d';
  const ALL=Object.keys(CON).concat(Object.keys(VOW)).sort((a,b)=>b.length-a.length);
  function convert(s){
    const tk=[]; let i=0;
    while(i<s.length){
      let hit=null;
      for(const k of ALL){ if(s.startsWith(k,i)){hit=k;break;} }
      if(!hit){ const c=s[i]; tk.push({t:'o',v:(OTH[c]!==undefined?OTH[c]:c)}); i++; continue; }
      if(CON[hit]) tk.push({t:'c',v:CON[hit]});
      else tk.push({t:'v',v:VOW[hit],k:hit});
      i+=hit.length;
    }
    let out='';
    for(let j=0;j<tk.length;j++){
      const t=tk[j];
      if(t.t==='o'){out+=t.v;continue;}
      if(t.t==='v'){out+=t.v;continue;}
      const nx=tk[j+1];
      if(nx&&nx.t==='v'){ if(nx.k==='a'){out+=t.v;} else {out+=t.v+(VSN[nx.k]||'');} j++; }
      else if(nx&&nx.t==='c'){ out+=t.v+HAL; }
      else { out+=t.v+HAL; }
    }
    return out;
  }
  return {convert};
})();
function cleanSA(s){
  return (s||'').replace(/^# Text\s*/,'').replace(/\[[A-Za-z0-9_]+\]/g,'').replace(/\s+/g,' ').trim();
}
function cleanEN(s){
  return (s||'').replace(/^#+\s*[^\n]*\n/,'').replace(/\s*\/\/\s*\S+\s*$/,'').trim();
}

async function work(path){
  const wid = path.split('/')[2];
  let items = await get(`/data/translations/${wid}.json`).catch(()=>null);
  if(!items || !items.length){
    try{
      if(!LIB.index) LIB.index = await get('/data/works-index.json');
      const rec = Object.values(LIB.index||{}).find(r=>r.translation===wid || r.work===wid);
      if(rec && rec.sanskrit){
        const raw = await get(`/data/sanskrit/${rec.sanskrit}`).catch(()=>null);
        if(raw){
          const paras = String(raw).split(/\n{2,}|\n(?=[\u0900-\u097F])/).filter(p=>p.trim()).slice(0,60);
          $('#view').innerHTML = paras.map(p=>{
            const t = cleanSA(p.trim().slice(0,600));
            return `<div class="verse"><div class="dev">${esc(IAST_DEVA.convert(t))}</div><div class="ro">${esc(t)}</div></div>`;
          }).join('') + `<div id="answer" style="display:none"></div>`;
          return;
        }
      }
    }catch(e){}
    $('#view').innerHTML = `<div class="verse"><div class="dev">· · ·</div></div><div id="answer" style="display:none"></div>`;
    return;
  }
  const AUDIODIR = {anuttarastika:'anuttarashtika_trad'};
  const audir = AUDIODIR[wid] || wid;
  let kar = null;
  try{ kar = await get(`/data/karaoke-${wid}.json`); }catch(e){}
  const hasKar = Array.isArray(kar) && kar.length > 0;
  const verses = items.map((it,ix)=>{
    const raw = cleanSA(it.sanskrit||'');
    const k = hasKar ? kar[ix % kar.length] : null;
    let units = [];
    if(k && k.words){
      units = k.words.map(w=>({sa: IAST_DEVA.convert(w.w), ro: w.r||'', t0: w.t_on, t1: w.t_off}));
    } else if(raw){
      units = raw.split(/\s+/).filter(Boolean).map(w=>({sa: IAST_DEVA.convert(w), ro: w, t0: null, t1: null}));
    }
    const dev = `<div class="wline">` + units.map(u=>
      `<span class="wunit"${u.t0!=null?` data-t0="${u.t0}" data-t1="${u.t1}" data-v="${ix}"`:''}><span class="dw">${esc(u.sa)}</span><span class="rw">${esc(u.ro)}</span></span>`
    ).join('') + `</div>`;
    const en = (it.gate==='PASS' && (it.l2||it.l1)) ? `<div class="en">${esc(cleanEN(it.l2||it.l1))}</div>` : '';
    const au = k ? `/audio/${audir}/${k.id||('v'+String(ix+1).padStart(2,'0'))}.mp3` : null;
    return {dev, ro:'', en, au, ix};
  });
  $('#view').innerHTML =
    `<div id="reader">` + verses.map((v,ix)=>`<div class="verse" data-v="${ix}">${v.dev}${v.en}</div>`).join('') + `</div>` +
    `<div id="rcbar"><button id="rcPlay" title="recite">▶</button><button id="rcRead" title="read aloud">🔊</button><button id="rcStop" style="display:none" title="stop">■</button></div>` +
    `<div id="answer" style="display:none"></div>`;
  const audio = new Audio(); audio.preload='auto'; KAR.audio = audio;
  const st = document.createElement('style');
  st.textContent = '#reader{max-width:none}.verse{margin:2rem 0}.verse:first-child{margin-top:.5rem}.wline{line-height:1.4}.wunit{display:inline-block;text-align:center;vertical-align:top;margin:0 .45em .9em 0}.dw{display:block;font-size:1.55rem;line-height:1.4}.rw{display:block;font-size:.78rem;color:#76736e;font-style:normal;letter-spacing:.01em}.en{font-size:1rem;line-height:1.65;max-width:44rem}#rcbar{position:fixed;bottom:4.5rem;left:50%;transform:translateX(-50%);z-index:11;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border:1px solid var(--line);border-radius:999px;padding:.3rem .6rem;display:flex;gap:.2rem;box-shadow:0 4px 16px rgba(0,0,0,.08)}#rcbar button{border:0;background:none;cursor:pointer;font-size:1.1rem;padding:.3rem .6rem;border-radius:999px}#rcbar button:hover{background:#f4f1ea}.wunit.hl{background:#fdf0d5;border-radius:.3em}.wunit.hl .dw{font-weight:500}.vnow{box-shadow:-3px 0 0 var(--gold);padding-left:.8rem}';
  document.head.appendChild(st);
  function tick(){
    const t = audio.currentTime;
    document.querySelectorAll('.wunit.hl').forEach(w=>w.classList.remove('hl'));
    const all = Array.prototype.slice.call(document.querySelectorAll('.wunit[data-t0]'));
    for(const w of all){
      if(+w.getAttribute('data-v') !== KAR.cur) continue;
      const t0 = parseFloat(w.getAttribute('data-t0')), t1 = parseFloat(w.getAttribute('data-t1'));
      if(t >= t0 && t <= t1){ w.classList.add('hl'); break; }
    }
    if(!audio.paused && !audio.ended) KAR.timer = requestAnimationFrame(tick);
  }
  function stopAll(){
    if(KAR.timer){ cancelAnimationFrame(KAR.timer); KAR.timer = null; }
    audio.pause(); audio.onended = null;
    try{ speechSynthesis.cancel(); }catch(e){}
    document.querySelectorAll('.wunit.hl').forEach(w=>w.classList.remove('hl'));
    document.querySelectorAll('.vnow').forEach(v=>v.classList.remove('vnow'));
    const sb = document.getElementById('rcStop'); if(sb) sb.style.display='none';
    const pb = document.getElementById('rcPlay'); if(pb) pb.style.display='';
    KAR.cur = null;
  }
  function markVerse(ix){
    document.querySelectorAll('.vnow').forEach(v=>v.classList.remove('vnow'));
    const blk = document.querySelector(`.verse[data-v="${ix}"]`);
    if(blk){ blk.classList.add('vnow'); blk.scrollIntoView({block:'center',behavior:'smooth'}); }
  }
  function playVerse(ix){
    stopAll();
    KAR.cur = ix;
    markVerse(ix);
    const au = verses[ix] && verses[ix].au;
    const hasAudio = !!au;
    if(hasAudio){
      audio.src = au;
      const sb = document.getElementById('rcStop'); if(sb) sb.style.display='';
      const pb = document.getElementById('rcPlay'); if(pb) pb.style.display='none';
      audio.play().catch(()=>{ speakVerse(ix, false); });
      KAR.timer = requestAnimationFrame(tick);
    } else {
      speakVerse(ix, false);
    }
  }
  function speakVerse(ix, advance){
    try{
      speechSynthesis.cancel();
      const v = document.querySelector(`.verse[data-v="${ix}"]`);
      if(!v) return;
      markVerse(ix);
      const u = new SpeechSynthesisUtterance(v.textContent.slice(0, 1200));
      u.rate = 0.95;
      if(advance){
        u.onend = ()=>{ ix++; if(ix < verses.length) speakVerse(ix, true); else stopAll(); };
      } else {
        u.onend = ()=>{ stopAll(); };
      }
      speechSynthesis.speak(u);
    }catch(e){}
  }
  // tap a verse: hear it (chant if audio exists, spoken otherwise)
  document.querySelectorAll('.verse').forEach((el,ix)=>{
    el.style.cursor = 'pointer';
    el.onclick = ()=>playVerse(ix);
  });
  const mRecite = document.getElementById('rcPlay');
  if(mRecite) mRecite.onclick = ()=>{
    let ix = 0;
    audio.onended = ()=>{ ix++; if(ix >= verses.length){ stopAll(); } else playVerse(ix); };
    playVerse(ix);
  };
  const kstop = document.getElementById('rcStop');
  if(kstop) kstop.onclick = ()=>{ stopAll(); };
  const readAloud = document.getElementById('rcRead');
  if(readAloud) readAloud.onclick = ()=>{
    stopAll();
    speakVerse(0, true);
  };
}

async function practices(){
  $('#view').innerHTML = `<div style="position:relative;margin:0 -1rem"><div style="position:absolute;top:.4rem;left:.8rem;z-index:6"><button class="playbtn" id="labexit" style="background:rgba(255,255,255,.92)">‹ app</button></div><div style="font-family:Inter,system-ui,sans-serif;font-size:.78rem;letter-spacing:.12em;color:var(--mut);padding:.5rem 1rem 0;text-align:center">PRACTISE · the lab, live</div><iframe src="https://body.stonedoorway.com/lab" style="width:100%;height:calc(100dvh - 220px);min-height:420px;border:0;display:block" title="practice lab" allow="autoplay; microphone"></iframe></div><div id="answer" style="display:none"></div>`;
  document.getElementById('labexit').onclick = ()=>{ location.hash = '#/'; };
}








function notfound(){ $('#view').innerHTML = `<h1>—</h1><p><a href="#/">home</a></p>`; }

/* ask box → Worker chat, answer inline */
document.getElementById('ask').addEventListener('submit', async ev=>{
  ev.preventDefault();
  const q = document.getElementById('askQ');
  const msg = (q.value||'').trim();
  if(!msg) return;
  q.value='';
  let box = document.getElementById('answer');
  if(!box){ box = document.createElement('div'); box.id='answer'; document.getElementById('view').appendChild(box); }
  box.style.display='block';
  box.innerHTML = '<div class="who">ASKING</div>…';
  try{
    const work = (location.hash.match(/^#\/(work\/[^/]+|read|recite)/)||[])[1] || 'ipvv';
    const works = work.startsWith('work/') ? work.slice(5) : work==='read' ? 'ipvv' : work;
    const r = await fetch(`${API}/api/chat/${works}`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,session_id:SID})}).then(r=>r.json());
    if(r.session_id) SID = r.session_id;
    box.innerHTML = `<div class="who">ANSWER · ${esc(works)}</div><div>${esc(r.reply||'no answer').slice(0,2000)}</div>` +
      (r.suggestion ? `<span class="follow" id="followq">→ ${esc(r.suggestion)}</span>` : '');
    if(SPEAK && r.reply) listen(r.reply);
    const fq = document.getElementById('followq');
    if(fq) fq.onclick = ()=>{ document.getElementById('askQ').value = r.suggestion; document.getElementById('ask').requestSubmit(); };
  }catch(e){ box.innerHTML = '<div class="who">ERROR</div>'+esc(e.message); }
});
document.getElementById('menuBtn').addEventListener('click', ()=>{
  document.getElementById('menu').classList.toggle('open');
});
window.addEventListener('hashchange', router);
router();
