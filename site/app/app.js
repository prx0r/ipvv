/* svatantrya app — lab-pattern SPA: one shell, JSON content, zero reloads. */
const API = 'https://ipvv-api.tradesprior.workers.dev';
const $ = s => document.querySelector(s);
const esc = s => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const NAV = [
  ['read','/translations','Read'],['recite','/recite','Recite'],['practice','/practices','Practise'],
  ['enquire','/ipvv/pushing.html','Enquire'],['translate','/tools','Translate'],['write','/essays','Write'],
];
const MENU = [
  ['Masters','#/masters'],['Scholars','#/scholars'],['Concepts','#/concepts'],
  ['Pushing','#/pushing'],['About','#/about'],
];
let SID = null;

function nav(cur){
  $('#nav').innerHTML = NAV.map(([k,u,t])=>`<a href="#/${k}" data-k="${k}" class="${k===cur?'on':''}">${t}</a>`).join('');
  $('#menu').innerHTML = MENU.map(([t,u])=>`<a href="${u}">${t}</a>`).join('');
}
async function get(p){
  const r = await fetch(p);
  if(!r.ok) throw 0;
  const ct = r.headers.get('content-type')||'';
  return ct.includes('json') ? r.json() : r.text();
}
const routes = {
  '/': home, '/read': translations, '/recite': recite, '/practice': practices,
  '/enquire': pushing, '/translate': tools, '/write': essays,
  '/masters': masters, '/scholars': scholars, '/concepts': concepts,
};
async function router(){
  const h = location.hash.slice(1) || '/';
  const [path] = h.split('?');
  const fn = routes[path] || (path.startsWith('/work/') ? work : notfound);
  const cur = (NAV.find(([k])=>'/'+k===path)||[])[0] || '';
  nav(cur);
  $('#view').innerHTML = '<p style="color:#999">…</p>';
  try { await fn(path); } catch(e){ $('#view').innerHTML = '<p>Could not load. <a href="#/">home</a></p>'; }
  window.scrollTo(0,0);
}
function home(){
  $('#view').innerHTML = `<h1>svatantrya</h1><div class="sub">freedom · read · recite · practise · enquire · translate · write</div>
  <div class="idx">${NAV.map(([k,u,t])=>`<a href="#/${k}"><b>${t}</b> <small>— ${{read:'the texts',recite:'chants + readout',practice:'112 dhāraṇās',enquire:'hound a text with why',translate:'workbench',write:'working papers'}[k]}</small></a>`).join('')}</div>
  <div id="answer" style="display:none"></div>`;
}
async function translations(){
  const idx = await get('/data/translations.json').catch(()=>null);
  const files = idx || ["kramastotra","bodhapancadasika","spanda","sivasutra","bhairavastava","stavacintamani","tantrasara","paratrimshika","paramarthasara","vbt"];
  $('#view').innerHTML = `<h1>Read</h1><div class="sub">Sanskrit with gate-passed English. Withheld where the gate hasn't passed — fail-closed.</div>
  <div class="idx">${files.map(w=>`<a href="#/work/${w}">${esc(w)}</a>`).join('')}</div><div id="answer" style="display:none"></div>`;
}
async function work(path){
  const wid = path.split('/')[2];
  const items = await get(`/data/translations/${wid}.json`);
  const pass = items.filter(i=>i.gate==='PASS'), held = items.length - pass.length;
  $('#view').innerHTML = `<h1>${esc(wid)}</h1><div class="sub">${pass.length} PASS · ${held} withheld</div>` +
    items.map(it=>`<h2>${esc(it.chunk||'')}</h2><div class="dev">${esc(it.sanskrit||'')}</div>` +
      (it.gate==='PASS'
        ? `<p>${esc(it.l2||it.l1||'')}</p><div class="gate pass">PASS · English shown</div>`
        : `<div class="gate blocked">Withheld — pending review. Sanskrit only, never translated by display.</div>`)).join('') +
    `<div id="answer" style="display:none"></div>`;
}
async function recite(){
  $('#view').innerHTML = `<h1>Recite</h1><div class="sub">Studio chants + four-mode readout. Audio keeps playing while you browse.</div>
  <div class="idx"><a href="#/work/bhairavastava">Bhairavastava — 10 studio chants</a><a href="#/work/anuttarastika">Anuttarāṣṭikā</a></div><div id="answer" style="display:none"></div>`;
}
async function practices(){
  const items = await get('/data/practices.json').catch(()=>[]);
  const list = Array.isArray(items) ? items : [];
  $('#view').innerHTML = `<h1>Practise</h1><div class="sub">112 dhāraṇās · breath-paced · <a href="https://body.stonedoorway.com/lab">open in the Lab ↗</a></div>
  <div class="idx">${list.slice(0,60).map(p=>`<a>${esc(p.title||p.name||p.id)}</a>`).join('')||'<span class="sub">loading…</span>'}</div><div id="answer" style="display:none"></div>`;
}
async function pushing(){
  $('#view').innerHTML = `<h1>Enquire</h1><div class="sub">Hound a text with why. Or ask below — the copilot fires a chain and shows its work.</div>
  <div class="idx"><a href="#/pushing/bodhapancadasika">Bodhapañcadaśikā — 5 sessions (forget → terror → grace → necessity → dissolution)</a><a href="#/pushing/ipvv">IPVV — 12 probes</a><a href="#/pushing/tantraloka">Tantrāloka — 63 probes</a></div><div id="answer" style="display:none"></div>`;
}
async function tools(){
  $('#view').innerHTML = `<h1>Translate</h1><div class="sub">Workbench · variants · witnesses · gates.</div>
  <div class="idx"><a href="#/read">All translations</a><a href="#/concepts">Glossary (100 terms)</a></div><div id="answer" style="display:none"></div>`;
}
async function essays(){
  $('#view').innerHTML = `<h1>Write</h1><div class="sub">Working papers argued from the translations.</div><div id="essays-list">loading…</div><div id="answer" style="display:none"></div>`;
  try{
    const files = ["IPVV-MEMORY-vs-whattheheckismemory","IPVV-buddhist-co-opting","IPVV-felt-to-ground-argument"];
    $('#essays-list').innerHTML = `<div class="idx">${files.map(f=>`<a>${esc(f)}</a>`).join('')}</div>`;
  }catch(e){}
}
async function masters(){
  const secs = await get('/data/sections.json').catch(()=>null);
  const ms = (secs && secs.sections.find(s=>s.id==='masters')) || {members:[]};
  $('#view').innerHTML = `<h1>Masters</h1><div class="sub">By works, most first.</div><div class="idx" id="mlist"></div><div id="answer" style="display:none"></div>`;
  const counts = {};
  await Promise.all(ms.members.slice(0,20).map(async m=>{
    try{ const w = await get(`/data/works_${m}.json`); counts[m]=Array.isArray(w)?w.length:0; }catch(e){ counts[m]=0; }
  }));
  const sorted = [...ms.members].sort((a,b)=>(counts[b]||0)-(counts[a]||0));
  $('#mlist').innerHTML = `<div class="idx">${sorted.map(m=>`<a>${esc(m)} <small>· ${counts[m]||0}</small></a>`).join('')}</div>`;
}
async function scholars(){
  $('#view').innerHTML = `<h1>Scholars</h1><div class="sub">Secondary witnesses — read and cite, host only what is open.</div><div id="answer" style="display:none"></div>`;
}
async function concepts(){
  $('#view').innerHTML = `<h1>Concepts</h1><div class="sub">Glossary with every occurrence linked.</div><div id="answer" style="display:none"></div>`;
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
    const fq = document.getElementById('followq');
    if(fq) fq.onclick = ()=>{ document.getElementById('askQ').value = r.suggestion; document.getElementById('ask').requestSubmit(); };
  }catch(e){ box.innerHTML = '<div class="who">ERROR</div>'+esc(e.message); }
});
document.getElementById('menuBtn').addEventListener('click', ()=>{
  document.getElementById('menu').classList.toggle('open');
});
window.addEventListener('hashchange', router);
router();
