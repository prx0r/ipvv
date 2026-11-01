/* standalone multi-view reader — new location, old reader untouched.
   ?work=wid&view=read|compare|literal|critical
   READ = C1 commentary as prose (falls back to L2, then Sanskrit-only).
   Fail-closed: BLOCKED chunks never show English. User versions live in
   localStorage only — paste from your own books, never bundled. */
(function(){
"use strict";
const $ = s => document.querySelector(s);
const esc = s => (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const qs = new URLSearchParams(location.search);
const WID = qs.get('work') || 'bhairavastava';
let VIEW = qs.get('view') || localStorage.getItem('svv-view') || 'read';
if(!['read','compare','literal','critical'].includes(VIEW)) VIEW = 'read';

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
function mdLite(s, bare){
  return (s||'').split(/\n{2,}/).map(p=>{
    p = p.trim(); if(!p) return '';
    const hm = p.match(/^(#{1,3})\s+(.*)$/);
    if(hm) return bare ? `<p>${esc(hm[2])}</p>` : `<div class="vlab">${esc(hm[2])}</div>`;
    const lm = p.match(/^\*\*([^*]+)\*\*\s*(.*)$/s);
    if(lm){
      const body = esc(lm[2]).replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
      return bare ? `<p>${body}</p>`
        : `<div class="c1sec"><div class="vlab">${esc(lm[1]).replace(/\.+$/,'')}</div><div>${body}</div></div>`;
    }
    return `<p>${esc(p).replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>')}</p>`;
  }).join('');
}
async function get(p){
  const r = await fetch(p);
  if(!r.ok) throw 0;
  const ct = r.headers.get('content-type')||'';
  return ct.includes('json') ? r.json() : r.text();
}
function getVar(ch){ try{ return localStorage.getItem(`svv-${WID}-${ch}`) || ''; }catch(e){ return ''; } }
function setVar(ch, v){ try{ localStorage.setItem(`svv-${WID}-${ch}`, v); }catch(e){} }
function go(view){
  VIEW = view;
  try{ localStorage.setItem('svv-view', view); }catch(e){}
  const u = new URL(location.href);
  u.searchParams.set('view', view);
  location.href = u.toString();
}
function devaNum(n){
  const d=['०','१','२','३','४','५','६','७','८','९'];
  return String(n).split('').map(c=>d[+c]||c).join('');
}

let VERSES = [], KAR = {audio:null, timer:null, cur:null};

async function main(){
  let items = null;
  try{
    const L = await get(`/data/layers/${WID}.json`);
    if(L && Array.isArray(L.chunks) && L.chunks.length) items = L.chunks;
  }catch(e){}
  if(!items){
    try{ items = await get(`/data/translations/${WID}.json`); }catch(e){ items = null; }
  }
  if(!items || !items.length){
    $('#view').innerHTML = `<div id="err">Nothing on file for “${esc(WID)}” yet.</div>`;
    return;
  }
  let title = WID.replace(/-/g, ' '), master = '';
  try{
    const idx = await get('/data/works-index.json');
    for(const k of Object.keys(idx||{})){
      if(k === WID || k.endsWith(':'+WID)){ master = k.includes(':') ? k.split(':')[0] : ''; break; }
    }
  }catch(e){}
  const nPass = items.filter(it=>it.gate==='PASS' && (it.l2||it.l1)).length;
  $('#wtitle').textContent = title;
  $('#wsub').textContent = `${master?master+' · ':''}${items.length} passages · ${nPass} with English · Sanskrit always`;
  const labels = [['read','Read'],['compare','Compare'],['literal','Literal'],['critical','Critical']];
  $('#vsw').innerHTML = labels.map(([v,l])=>`<button class="vsw${VIEW===v?' on':''}" data-v="${v}">${l}</button>`).join('');
  document.querySelectorAll('.vsw').forEach(b=>{ b.onclick = ()=>go(b.getAttribute('data-v')); });

  const AUDIODIR = {anuttarastika:'anuttarashtika_trad'};
  const audir = AUDIODIR[WID] || WID;
  let kar = null;
  try{ kar = await get(`/data/karaoke-${WID}.json`); }catch(e){}
  const hasKar = Array.isArray(kar) && kar.length > 0;
  VERSES = items.map((it,ix)=>{
    const raw = cleanSA(it.sanskrit||'');
    const k = hasKar ? kar[ix % kar.length] : null;
    let lines = [];
    if(k && k.words){
      const padas=[[],[],[],[]];
      k.words.forEach(w=>{ (padas[w.pada||0]=padas[w.pada||0]||[]).push(w); });
      lines = padas.filter(p=>p.length).map(p=>({
        words: p.map(w=>({sa: IAST_DEVA.convert(w.w), ro: w.r||'', t0: w.t_on, t1: w.t_off,
          syls: (w.syls||[]).map(s=>({sa: s.d, t0: s.t0, t1: s.t1}))})),
        ro: p.map(w=>esc(w.r||'')).join(' ')
      }));
    } else if(raw){
      lines = [{words: raw.split(/\s+/).filter(Boolean).map(w=>({sa: IAST_DEVA.convert(w), ro: w, t0: null, t1: null})), ro: esc(raw)}];
    }
    const sa = lines.map(l=>`<div class="dline">` + l.words.map(w=>
      (w.syls && w.syls.length
        ? `<span class="kword">` + w.syls.map(s=>
          `<span class="kw"${s.t0!=null?` data-t0="${s.t0}" data-t1="${s.t1}" data-v="${ix}"`:''}>${esc(s.sa)}</span>`
        ).join('') + `</span>`
        : `<span class="kw"${w.t0!=null?` data-t0="${w.t0}" data-t1="${w.t1}" data-v="${ix}"`:''}>${esc(w.sa)}</span>`)
    ).join(' ') + `</div><div class="rline">${l.ro}</div>`).join('');
    const pass = it.gate==='PASS' && (it.l2||it.l1);
    const au = k ? `/audio/${audir}/${k.id||('v'+String(ix+1).padStart(2,'0'))}.mp3` : null;
    return {sa, au, ix, it, pass,
      en1: pass ? cleanEN(it.l1||'') : '',
      en2: pass ? cleanEN(it.l2||it.l1||'') : ''};
  });

  $('#view').innerHTML = VERSES.map((v,ix)=>{
    const vn = devaNum(ix+1);
    const ch = v.it.chunk || ('p'+String(ix+1).padStart(2,'0'));
    const uv = getVar(ch);
    let body = '';
    if(!v.pass){
      body = v.sa;
    } else if(VIEW==='read'){
      // READ is the C1 commentary as prose; L2 when no C1 yet.
      body = (v.it.c1 ? `<div class="readc1">${mdLite(v.it.c1, true)}</div>` : `<div class="en read">${esc(v.en2)}</div}`);
    } else if(VIEW==='compare'){
      body = `<div class="cmp"><div><div class="vlab">L1 · close</div><div class="en">${esc(v.en1||v.en2)}</div></div><div><div class="vlab">L2 · read</div><div class="en">${esc(v.en2)}</div></div></div>`;
    } else if(VIEW==='literal'){
      body = `${v.sa}<div class="vlab">L1 · close</div><div class="en">${esc(v.en1||v.en2)}</div>`;
    } else {
      body = `${v.sa}`
        + `<div class="vlab">L1 · close</div><div class="en">${esc(v.en1||v.en2)}</div>`
        + `<div class="vlab">L2 · read</div><div class="en">${esc(v.en2)}</div>`
        + (v.it.c1?`<div class="vlab">C1 · commentary</div><div class="c1">${mdLite(v.it.c1)}</div>`:'')
        + (v.it.argmap?`<details class="arg"><summary>Argument map</summary><div class="c1">${mdLite(v.it.argmap)}</div></details>`:'')
        + `<div class="prov">gate ${esc(v.it.gate||'?')} · ${esc(v.it.model||'')} · ${esc(v.it.date||'')} · machine-proposed, needs human review</div>`
        + (uv?`<div class="vlab">Your version · this device only</div><div class="en yours">${esc(uv)}</div>`:'')
        + `<div class="varbox" style="display:none"><textarea id="var-${ix}" placeholder="Paste your translation (from your own book)…"></textarea><br><button class="playbtn" data-savevar="${ix}" data-ch="${esc(ch)}">Save on this device</button></div>`
        + `<button class="playbtn addvar" data-ix="${ix}">＋ add your version</button>`;
    }
    return `<div class="verse" data-v="${ix}"><div class="vnum">${vn}</div>${body}<div class="vclose">॥ ${vn} ॥</div></div>`;
  }).join('') + `<div class="rend">❖ ❖ ❖</div>`;

  document.querySelectorAll('.addvar').forEach(b=>{
    b.onclick = (e)=>{ e.stopPropagation(); const box = b.parentElement.querySelector('.varbox'); if(box) box.style.display = box.style.display==='none' ? '' : 'none'; };
  });
  document.querySelectorAll('[data-savevar]').forEach(b=>{
    b.onclick = (e)=>{
      e.stopPropagation();
      const ix = +b.getAttribute('data-savevar'), ch = b.getAttribute('data-ch');
      const ta = document.getElementById(`var-${ix}`);
      if(ta && ta.value.trim()){ setVar(ch, ta.value.trim()); go(VIEW); }
    };
  });
  document.querySelectorAll('.verse').forEach((el,ix)=>{ el.style.cursor='pointer'; el.onclick = ()=>playVerse(ix); });
  const rp = $('#rcPlay'); if(rp) rp.onclick = ()=>{
    let ix = 0;
    KAR.audio.onended = ()=>{ ix++; if(ix < VERSES.length) playVerse(ix); else stopAll(); };
    playVerse(ix);
  };
  const rs = $('#rcStop'); if(rs) rs.onclick = ()=>stopAll();
  const ra = $('#rcRead'); if(ra) ra.onclick = ()=>{
    stopAll();
    speakVerse(0, true);
  };
  KAR.audio = new Audio(); KAR.audio.preload = 'auto';
  window.scrollTo(0,0);
}

function tick(){
  const audio = KAR.audio;
  if(!audio) return;
  const t = audio.currentTime;
  document.querySelectorAll('.kw.on').forEach(w=>w.classList.remove('on'));
  const all = Array.prototype.slice.call(document.querySelectorAll('.kw[data-t0]'));
  for(const w of all){
    if(+w.getAttribute('data-v') !== KAR.cur) continue;
    const t0 = parseFloat(w.getAttribute('data-t0')), t1 = parseFloat(w.getAttribute('data-t1'));
    if(t >= t0 && t <= t1){ w.classList.add('on'); break; }
  }
  if(!audio.paused && !audio.ended) KAR.timer = requestAnimationFrame(tick);
}
function stopAll(){
  if(KAR.timer){ cancelAnimationFrame(KAR.timer); KAR.timer = null; }
  if(KAR.audio){ KAR.audio.pause(); KAR.audio.onended = null; }
  try{ speechSynthesis.cancel(); }catch(e){}
  document.querySelectorAll('.kw.on').forEach(w=>w.classList.remove('on'));
  document.querySelectorAll('.vnow').forEach(v=>v.classList.remove('vnow'));
  const sb = $('#rcStop'); if(sb) sb.style.display='none';
  const pb = $('#rcPlay'); if(pb) pb.style.display='';
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
  const au = VERSES[ix] && VERSES[ix].au;
  const sb = $('#rcStop'); if(sb) sb.style.display='';
  const pb = $('#rcPlay'); if(pb) pb.style.display='none';
  if(au){
    KAR.audio.src = au;
    KAR.audio.play().catch(()=>{ speakVerse(ix, false); });
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
    u.onend = ()=>{ if(advance && ix+1 < VERSES.length) speakVerse(ix+1, true); else stopAll(); };
    speechSynthesis.speak(u);
  }catch(e){}
}
main();
})();
