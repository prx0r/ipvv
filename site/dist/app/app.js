/* svatantrya app — lab-pattern SPA: one shell, JSON content, zero reloads. */
const API = 'https://ipvv-api.tradesprior.workers.dev';
const $ = s => document.querySelector(s);
const esc = s => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const NAV = [
  ['practice','/practices','Practise'],['library','/library','Library'],
];
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

async function nav(cur){
  let mhtml = `<div class="msec">Menu</div>` +
    NAV.map(([k,u,t])=>`<a href="#/${k}" data-k="${k}" class="${k===cur?'on':''}">${t}</a>`).join('');
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
  '/': home, '/library': library,
  '/read': translations, '/recite': recite, '/practice': practices,
  '/enquire': pushing, '/translate': tools, '/write': essays,
  '/masters': masters, '/scholars': scholars, '/concepts': concepts,
};
async function router(){
  const h = location.hash.slice(1) || '/';
  const [path] = h.split('?');
  // restore shell chrome (practices/lab hides it)
  ['top','askbar'].forEach(id=>{ const el=document.getElementById(id); if(el) el.style.display=''; });
  const mb = document.getElementById('menuBtn');
  if(mb) mb.style.display = (path === '/practice') ? 'none' : '';
  const fn = routes[path] || (path.startsWith('/work/') ? work : (path.startsWith('/probe/') ? probe : notfound));
  const cur = (NAV.find(([k])=>'/'+k===path)||[])[0] || '';
  nav(cur);
  $('#view').innerHTML = '<p style="color:#999">…</p>';
  try { await fn(path); } catch(e){ $('#view').innerHTML = '<p>Could not load. <a href="#/">home</a></p>'; }
  window.scrollTo(0,0);
}
function home(){
  $('#view').innerHTML = `<h1>svatantrya</h1><div class="sub">freedom</div>
  <div class="idx"><a href="#/practice"><b>practise</b> <small>— the lab, live</small></a><a href="#/library"><b>library</b> <small>— masters · works · read</small></a></div>
  <div id="answer" style="display:none"></div>`;
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
async function translations(){
  const idx = await get('/data/translations.json').catch(()=>null);
  const files = idx || ["kramastotra","bodhapancadasika","spanda","sivasutra","bhairavastava","stavacintamani","tantrasara","paratrimshika","paramarthasara","vbt"];
  $('#view').innerHTML = `<h1>Read</h1><div class="sub">Sanskrit with gate-passed English. Withheld where the gate hasn't passed — fail-closed.</div>
  <div class="idx">${files.map(w=>`<a href="#/work/${w}">${esc(w)}</a>`).join('')}</div><div id="answer" style="display:none"></div>`;
}
let KAR = { audio: null, timer: null, cur: null };
function stopKaraoke(){
  if(KAR.timer){ cancelAnimationFrame(KAR.timer); KAR.timer = null; }
  if(KAR.audio){ KAR.audio.pause(); }
  document.querySelectorAll('.kw.on').forEach(w=>w.classList.remove('on'));
  const b = document.getElementById('kstop');
  if(b) b.style.display='none';
}
async function work(path){
  const wid = path.split('/')[2];
  let items = await get(`/data/translations/${wid}.json`).catch(()=>null);
  if(!items || !items.length){
    // fallback: Sanskrit root via works-index (fail-closed: Sanskrit only, no English)
    try{
      if(!LIB.index) LIB.index = await get('/data/works-index.json');
      const rec = Object.values(LIB.index||{}).find(r=>r.translation===wid || r.work===wid);
      if(rec && rec.sanskrit){
        const raw = await get(`/data/sanskrit/${rec.sanskrit}`).catch(()=>null);
        if(raw){
          const paras = String(raw).split(/\n{2,}|\n(?=[\u0900-\u097F])/).filter(p=>p.trim()).slice(0,60);
          $('#view').innerHTML = `<h1>${esc(rec.title||wid)}</h1><div class="sub">Sanskrit root · translation in progress — English withheld until the gate passes.</div>` +
            paras.map(p=>`<div class="dev">${esc(p.trim().slice(0,600))}</div>`).join('') +
            `<div id="answer" style="display:none"></div>`;
          return;
        }
      }
    }catch(e){}
    $('#view').innerHTML = `<h1>${esc(wid)}</h1><div class="sub">Not yet on the site — Sanskrit root not vendored, translation not started.</div><div id="answer" style="display:none"></div>`;
    return;
  }
  const AUDIODIR = {anuttarastika:'anuttarashtika_trad'};
  const audir = AUDIODIR[wid] || wid;
  let kar = null;
  try{ kar = await get(`/data/karaoke-${wid}.json`); }catch(e){}
  const hasKar = Array.isArray(kar) && kar.length > 0;
  const pass = items.filter(i=>i.gate==='PASS'), held = items.length - pass.length;
  let mode = 'both';
  try{ mode = localStorage.getItem('readmode') || 'both'; }catch(e){}
  const modes = [['sa','SA'],['en','EN'],['both','SA+EN']];
  let html = `<h1>${esc(wid)}</h1><div class="sub">${pass.length} PASS · ${held} withheld${hasKar ? ' · karaoke ready' : ''}</div>`;
  html += `<div id="modebar" style="margin-bottom:1rem"><button class="playbtn" id="mRecite">▶ recite</button> <button class="playbtn" id="readAloud" title="read aloud">🔊 read aloud</button> ` +
    modes.map(([m,l])=>`<button class="playbtn" data-mode="${m}" ${m===mode?'style="border-color:var(--gold)"':''}>${l}</button>`).join(' ') +
    ` <button class="playbtn" id="kstop" style="display:none">■ stop</button></div><div id="kv"></div>`;
  html += items.map((it,ix)=>{
    const k = hasKar ? kar[ix % kar.length] : null;
    let saHtml = `<div class="dev rl-sa">${esc(it.sanskrit||'')}</div>`;
    let roHtml = '';
    if(k && k.words){
      const padas=[[],[],[],[]];
      k.words.forEach(w=>{ (padas[w.pada||0]=padas[w.pada||0]||[]).push(w); });
      saHtml = padas.filter(p=>p.length).map(p=>`<div class="dev rl-sa">${p.map(w=>`<span class="kw" data-t0="${w.t_on}" data-t1="${w.t_off}" data-v="${ix}">${esc(w.w)}</span>`).join(' ')}</div>`).join('');
      const rline = padas.filter(p=>p.length).map(p=>p.map(w=>esc(w.r||'')).join(' ')).join(' / ');
      if(rline.trim()) roHtml = `<div class="iast rl-ro">${rline}</div>`;
    }
    return `<div class="vblock" data-v="${ix}"><div style="display:flex;align-items:baseline;gap:.5rem"><h2 style="margin:0">${esc(it.chunk||'')}</h2>${k?`<button class="playbtn" data-kplay="${ix}" data-au="/audio/${audir}/${k.id||('v'+String(ix+1).padStart(2,'0'))}.mp3">▶</button>`:''}</div>${saHtml}${roHtml}` +
    (it.gate==='PASS'
      ? `<div class="rl-en"><p>${esc(it.l2||it.l1||'')}</p><div class="gate pass">PASS · English shown</div></div>`
      : `<div class="rl-en gate blocked">Withheld — pending review. Sanskrit only, never translated by display.</div>`) + `</div>`;
  }).join('');
  html += `<div id="answer" style="display:none"></div>`;
  $('#view').innerHTML = html;
  const applyMode = (m)=>{
    mode = m;
    try{ localStorage.setItem('readmode', m); }catch(e){}
    document.querySelectorAll('#modebar [data-mode]').forEach(b=>{
      if(b.getAttribute('data-mode')===m) b.style.borderColor='var(--gold)'; else b.style.borderColor='';
    });
    const showSa = (m==='sa'||m==='both'), showEn = (m==='en'||m==='both'), showRo = (m!=='en');
    document.querySelectorAll('.rl-sa').forEach(el=>el.style.display=showSa?'':'none');
    document.querySelectorAll('.rl-ro').forEach(el=>el.style.display=showRo?'':'none');
    document.querySelectorAll('.rl-en').forEach(el=>el.style.display=showEn?'':'none');
  };
  document.querySelectorAll('#modebar [data-mode]').forEach(b=>{
    b.onclick = ()=>{ stopKaraoke(); KAR.cur=null; applyMode(b.getAttribute('data-mode')); };
  });
  applyMode(mode);
  if(!hasKar) return;
  const audio = new Audio(); audio.preload='auto'; KAR.audio = audio;
  const st = document.createElement('style');
  st.textContent = '.kw{transition:background .15s;border-radius:.2em;padding:0 .1em}.kw.on{background:#fdf0d5}.iast{color:#76736e;font-size:14px;font-style:italic;margin-bottom:7px}';
  document.head.appendChild(st);
  function tick(){
    const t = audio.currentTime;
    document.querySelectorAll('.kw.on').forEach(w=>w.classList.remove('on'));
    const all = Array.prototype.slice.call(document.querySelectorAll('.kw'));
    for(const w of all){
      if(+w.getAttribute('data-v') !== KAR.cur) continue;
      const t0 = parseFloat(w.getAttribute('data-t0')), t1 = parseFloat(w.getAttribute('data-t1'));
      if(t >= t0 && t <= t1){ w.classList.add('on'); break; }
    }
    if(!audio.paused && !audio.ended) KAR.timer = requestAnimationFrame(tick);
  }
  function playVerse(ix){
    if(KAR.timer){ cancelAnimationFrame(KAR.timer); KAR.timer = null; }
    audio.pause();
    document.querySelectorAll('.kw.on').forEach(w=>w.classList.remove('on'));
    const btn = document.querySelector(`[data-kplay="${ix}"]`);
    if(!btn) return;
    audio.src = btn.getAttribute('data-au');
    KAR.cur = ix;
    const sb = document.getElementById('kstop'); if(sb) sb.style.display='';
    audio.play().catch(()=>{});
    KAR.timer = requestAnimationFrame(tick);
    const blk = document.querySelector(`.vblock[data-v="${ix}"]`);
    if(blk) blk.scrollIntoView({block:'center',behavior:'smooth'});
  }
  document.querySelectorAll('[data-kplay]').forEach(b=>{ b.onclick = ()=>playVerse(+b.getAttribute('data-kplay')); });
  const mRecite = document.getElementById('mRecite');
  if(mRecite) mRecite.onclick = ()=>{
    let ix = 0;
    const total = document.querySelectorAll('[data-kplay]').length;
    audio.onended = ()=>{ ix++; if(ix >= total){ const sb=document.getElementById('kstop'); if(sb) sb.style.display='none'; KAR.cur=null; } else playVerse(ix); };
    playVerse(ix);
  };
  const kstop = document.getElementById('kstop');
  if(kstop) kstop.onclick = ()=>{ audio.onended=null; stopKaraoke(); KAR.cur=null; };
  const readAloud = document.getElementById('readAloud');
  if(readAloud) readAloud.onclick = ()=>{
    stopKaraoke(); KAR.cur=null;
    try{
      speechSynthesis.cancel();
      const parts = [];
      document.querySelectorAll('.vblock').forEach(v=>{
        const sa = Array.prototype.map.call(v.querySelectorAll('.rl-sa'), e=>e.textContent).join(' ');
        const en = Array.prototype.map.call(v.querySelectorAll('.rl-en'), e=>e.textContent).join(' ');
        if(sa) parts.push(sa);
        if(en && mode !== 'sa') parts.push(en.slice(0, 400));
      });
      const u = new SpeechSynthesisUtterance(parts.join(' ').slice(0, 4000));
      u.rate = 0.95; speechSynthesis.speak(u);
    }catch(e){}
  };
}
async function recite(){
  let works = [];
  try{
    const idx = await get('/data/translations.json');
    works = idx.filter(w=>['bhairavastava','anuttarastika','stavacintamani','sivastotravali'].includes(w));
  }catch(e){}
  let html = `<h1>Recite</h1><div class="sub">Studio chants. Audio keeps playing while you browse.</div>`;
  for(const w of works){
    try{
      const au = await get(`/data/audio-${w}.json`).catch(()=>null);
      if(!au || !au.verses) continue;
      html += `<h2>${esc(w)}</h2>`;
      au.verses.slice(0,12).forEach((v,i)=>{
        const id = v.id || `${w}_${i+1}`;
        html += `<button class="playbtn" data-au="/audio/${w}/${id}.mp3" data-t="${esc(w)} v${v.n||i+1}">▶ v${v.n||i+1}</button>`;
      });
    }catch(e){}
  }
  $('#view').innerHTML = html + `<div id="answer" style="display:none"></div>`;
  document.querySelectorAll('#view .playbtn[data-au]').forEach(b=>{
    b.onclick = ()=>playAudio(b.getAttribute('data-au'), b.getAttribute('data-t'));
  });
}
async function practices(){
  $('#view').innerHTML = `<div style="position:relative;margin:0 -1rem"><div style="position:absolute;top:.4rem;left:.8rem;z-index:6"><button class="playbtn" id="labexit" style="background:rgba(255,255,255,.92)">‹ app</button></div><div style="font-family:Inter,system-ui,sans-serif;font-size:.78rem;letter-spacing:.12em;color:var(--mut);padding:.5rem 1rem 0;text-align:center">PRACTISE · the lab, live</div><iframe src="https://body.stonedoorway.com/lab" style="width:100%;height:calc(100dvh - 220px);min-height:420px;border:0;display:block" title="practice lab" allow="autoplay; microphone"></iframe></div><div id="answer" style="display:none"></div>`;
  document.getElementById('labexit').onclick = ()=>{ location.hash = '#/'; };
}
async function pushing(){
  let items = [];
  try{
    const c = await (await fetch('/data/corpus.jsonl')).text();
    items = c.split('\n').filter(Boolean).map(l=>{ try{return JSON.parse(l)}catch(e){return null} }).filter(r=>r && r.kind==='probe');
  }catch(e){}
  const byWork = {};
  items.forEach(r=>{ const w=(r.work||'pushing').replace('pushing:',''); (byWork[w]=byWork[w]||[]).push(r); });
  const groups = Object.keys(byWork).sort();
  $('#view').innerHTML = `<h1>Enquire</h1><div class="sub">Hound a text with why. Or ask below — the copilot fires a chain and shows its work.</div>` +
    (groups.length ? groups.map(g=>`<h2>${esc(g)}</h2><div class="idx">${byWork[g].slice(0,30).map(r=>`<a href="#/probe/${esc(r.id.replace(/^pushing:/,''))}">${esc((r.ref||r.id).split('/').pop().replace(/\.md$/,'').replace(/[-_]/g,' ').slice(0,80))}</a>`).join('')}</div>`).join('') :
    `<div class="idx"><a href="#/pushing/bodhapancadasika">Bodhapañcadaśikā — 5 sessions</a><a href="#/pushing/ipvv">IPVV — 12 probes</a><a href="#/pushing/tantraloka">Tantrāloka — 63 probes</a></div>`) +
    `<div id="answer" style="display:none"></div>`;
}
function mdBasic(src){
  let h = esc(src);
  h = h.replace(/^###### (.*)$/gm,'<h6>$1</h6>').replace(/^##### (.*)$/gm,'<h5>$1</h5>').replace(/^#### (.*)$/gm,'<h4>$1</h4>').replace(/^### (.*)$/gm,'<h3>$1</h3>').replace(/^## (.*)$/gm,'<h2>$1</h2>').replace(/^# (.*)$/gm,'<h1>$1</h1>');
  h = h.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/^&gt; (.*)$/gm,'<blockquote>$1</blockquote>');
  h = h.split('\n\n').map(p=>/^\s*<(h\d|blockquote|ul|ol|li|div|pre)/.test(p)?p:'<p>'+p.replace(/\n/g,'<br>')+'</p>').join('\n');
  return h;
}
async function probe(path){
  const id = path.split('/').slice(2).join('/');
  const recs = [];
  try{
    const c = await (await fetch('/data/corpus.jsonl')).text();
    c.split('\n').filter(Boolean).forEach(l=>{ try{ const r=JSON.parse(l); if(r.kind==='probe'&&(r.id==='pushing:'+id||r.id===id)) recs.push(r); }catch(e){} });
  }catch(e){}
  let body = '', title = id.split('/').pop().replace(/\.md$/,'').replace(/[-_]/g,' ');
  if(recs.length){ body = mdBasic((recs[0].en||'').slice(0,12000)); }
  else {
    try{ const t = await get('/data/pushing/'+id); body = mdBasic(t.slice(0,12000)); }
    catch(e){ body = '<p>Probe not found.</p>'; }
  }
  $('#view').innerHTML = `<div class="sub"><a href="#/enquire">← enquire</a> · owner voice, not scripture</div><h1>${esc(title.slice(0,80))}</h1><div class="gate pass">OWNER · pushing probe</div>${body}<div id="answer" style="display:none"></div>`;
  window.scrollTo(0,0);
}
async function tools(){
  $('#view').innerHTML = `<h1>Translate</h1><div class="sub">Workbench · variants · witnesses · gates.</div>
  <div class="idx"><a href="#/read">All translations</a><a href="#/concepts">Glossary (100 terms)</a></div><div id="answer" style="display:none"></div>`;
}
async function essays(){
  $('#view').innerHTML = `<h1>Write</h1><div class="sub">Working papers argued from the translations. Tap to read.</div><div id="essays-list">loading…</div><div id="essay-body"></div><div id="answer" style="display:none"></div>`;
  try{
    let files = null;
    try{ files = await get('/data/essays.json'); }catch(e){}
    if(!Array.isArray(files)) files = ["IPVV-MEMORY-vs-whattheheckismemory","IPVV-buddhist-co-opting","IPVV-felt-to-ground-argument","IPVV-recognition-formulations-vs-mepit","IPVV-internal-arc-vimarsas"];
    $('#essays-list').innerHTML = `<div class="idx">${files.map(f=>{ const n = typeof f==='string'?f:(f.id||f.file||''); return `<a href="#" data-essay="${esc(n)}">${esc(n.replace(/[-_]/g,' ').slice(0,60))}</a>`; }).join('')}</div>`;
    document.querySelectorAll('#essays-list [data-essay]').forEach(a=>{
      a.onclick = async (e)=>{ e.preventDefault();
        const n = a.getAttribute('data-essay');
        const eb = document.getElementById('essay-body');
        eb.innerHTML = '<p style="color:#999">…</p>';
        for(const u of [`/data/essay-${n}.md`,`/data/essay-ESSAY-${n}.md`,`/data/pushing/ipvv/${n}.md`]){
          try{ const t = await get(u); eb.innerHTML = mdBasic(t.slice(0,15000)); eb.scrollIntoView({block:'start'}); return; }
          catch(err){}
        }
        eb.innerHTML = '<p>Essay text not published yet.</p>';
      };
    });
  }catch(e){ const el=document.getElementById('essays-list'); if(el) el.innerHTML='<p>Could not load.</p>'; }
}
async function masters(){
  const secs = await get('/data/sections.json').catch(()=>null);
  const ms = ((secs && secs.sections.find(s=>s.id==='masters')) || {members:[]}).members || [];
  $('#view').innerHTML = `<h1>Masters</h1><div class="sub">Tap a name to see their works. By works, most first.</div><div id="mlist">loading…</div><div id="answer" style="display:none"></div>`;
  const counts = {}, cache = {};
  await Promise.all(ms.slice(0,25).map(async m=>{
    try{ const w = await get(`/data/works_${m}.json`); counts[m]=Array.isArray(w)?w.length:0; cache[m]=w; }catch(e){ counts[m]=0; }
  }));
  const sorted = [...ms].sort((a,b)=>(counts[b]||0)-(counts[a]||0));
  const box = document.getElementById('mlist');
  box.innerHTML = sorted.map(m=>`<div><a href="#" data-m="${esc(m)}"><b>${esc(m)}</b> <span class="sub">· ${counts[m]||0}</span></a><div class="mw" id="mw-${esc(m)}" style="display:none;margin:.2rem 0 .6rem 1rem"></div></div>`).join('');
  box.querySelectorAll('[data-m]').forEach(a=>{
    a.onclick = (e)=>{ e.preventDefault();
      const m = a.getAttribute('data-m');
      const d = document.getElementById('mw-'+m);
      if(!d) return;
      const open = d.style.display !== 'none';
      box.querySelectorAll('.mw').forEach(x=>x.style.display='none');
      if(open) return;
      const w = cache[m]||[];
      d.innerHTML = (Array.isArray(w)?w:[]).map(x=>`<div><a href="#/work/${esc(x.id||x.work||m)}">${esc(x.title||x.id||'')}</a></div>`).join('') || '<span class="sub">no works listed</span>';
      d.style.display='';
    };
  });
}
async function scholars(){
  $('#view').innerHTML = `<h1>Scholars</h1><div class="sub">Secondary witnesses — read and cite, host only what is open. Tap a name for bio.</div><div id="slist">loading…</div><div id="answer" style="display:none"></div>`;
  try{
    const ss = await get('/data/scholars.json');
    const list = Array.isArray(ss) ? ss : [];
    const box = document.getElementById('slist');
    box.innerHTML = list.map((s,i)=>`<div><a href="#" data-s="${i}"><b>${esc(s.name||s.id)}</b></a> <span class="sub">· ${esc(s.affiliation||'')}</span><div class="sb" id="sb-${i}" style="display:none;margin:.2rem 0 .6rem 1rem"></div></div>`).join('');
    box.querySelectorAll('[data-s]').forEach(a=>{
      a.onclick = (e)=>{ e.preventDefault();
        const i = +a.getAttribute('data-s');
        const d = document.getElementById('sb-'+i);
        if(!d) return;
        const open = d.style.display !== 'none';
        box.querySelectorAll('.sb').forEach(x=>x.style.display='none');
        if(open) return;
        const s = list[i]||{};
        d.innerHTML = `<p>${esc(s.bio||s.summary||'No bio on file.')}</p>`;
        d.style.display='';
      };
    });
  }catch(e){ document.getElementById('slist').innerHTML = '<p>Could not load.</p>'; }
}
async function concepts(){
  $('#view').innerHTML = `<h1>Concepts</h1><div class="sub">Glossary with every occurrence linked. Tap a term.</div><div id="clist">loading…</div><div id="answer" style="display:none"></div>`;
  try{
    const g = await get('/data/glossary.json');
    const list = Array.isArray(g) ? g : [];
    const box = document.getElementById('clist');
    box.innerHTML = list.map((t,i)=>`<div><a href="#" data-t="${i}"><b>${esc(t.term||t.id)}</b></a><div class="cb" id="cb-${i}" style="display:none;margin:.2rem 0 .6rem 1rem"></div></div>`).join('');
    box.querySelectorAll('[data-t]').forEach(a=>{
      a.onclick = (e)=>{ e.preventDefault();
        const i = +a.getAttribute('data-t');
        const d = document.getElementById('cb-'+i);
        if(!d) return;
        const open = d.style.display !== 'none';
        box.querySelectorAll('.cb').forEach(x=>x.style.display='none');
        if(open) return;
        const t = list[i]||{};
        d.innerHTML = `<p>${esc(t.gloss||t.definition||'')}</p>` +
          (t.passages && t.passages.length ? `<div class="sub">${t.passages.length} occurrence${t.passages.length>1?'s':''}: ${t.passages.slice(0,6).map(p=>esc(p)).join(', ')}</div>` : '');
        d.style.display='';
      };
    });
  }catch(e){ document.getElementById('clist').innerHTML = '<p>Could not load.</p>'; }
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
