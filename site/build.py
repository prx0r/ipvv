#!/usr/bin/env python3
"""site/build.py — static display site for formally-done translation work.

Same shell for every work. Displays only what formally exists.
Missing layers render greyed (planned), never invented.

Usage: python3 site/build.py [--works ipvv,vbt,tantrasara]
Output: site/dist/ (deploy to Cloudflare Pages, like shivastotravali.pages.dev)
"""
import json, html, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
PATALA = Path("/root/patalacheckpoints")
VOL = Path("/mnt/HC_Volume_106959365/root/projects")

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Tiro+Devanagari+Sanskrit:ital@0;1&family=Noto+Serif+Devanagari:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>"""

CSS = """*{box-sizing:border-box}
:root{--paper:#fff;--card:#fff;--ink:#17140f;--mut:#76736e;--faint:#a9a49c;--line:#e7e3db;--gold:#a86f14;--gold-ink:#7c5410;--sans:'Inter',system-ui,-apple-system,sans-serif;--serif:Georgia,'Cormorant Garamond',serif;--deva:'Tiro Devanagari Sanskrit','Noto Serif Devanagari',serif;
--nav-link:.8rem;--nav-hd:.68rem;--nav-count:.74rem;--nav-gap:.28rem}
html{-webkit-text-size-adjust:100%}
body{font-family:var(--serif);margin:0;background:var(--paper);color:var(--ink);font-size:17px;line-height:1.55;min-height:100vh;display:flex;flex-direction:column}
a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:2px}a:hover{text-decoration-color:var(--gold)}
/* top bar */
.topbar{position:sticky;top:0;z-index:50;background:var(--paper);border-bottom:1px solid var(--line)}
.topbar-in{max-width:1400px;margin:0 auto;display:flex;align-items:center;gap:.9rem;padding:.55rem 1rem}
.brand{color:var(--ink);white-space:nowrap;text-decoration:none;line-height:1.05}.deva-brand{font-family:var(--deva);font-size:1.45rem;line-height:1.25}
.brand small{font-family:var(--sans);font-size:.68rem;color:var(--mut);letter-spacing:.08em;text-transform:uppercase;display:block;line-height:1}
.topnav{display:flex;gap:1.1rem;flex-wrap:nowrap;overflow-x:auto;font-family:var(--sans);font-size:.82rem;scrollbar-width:none}
.topnav::-webkit-scrollbar{display:none}
.topnav a{padding:.4rem .1rem;color:var(--mut);text-decoration:none;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap;border-bottom:2px solid transparent}
.topnav a:hover{color:var(--ink);text-decoration:none}
.topnav a.on{color:var(--ink);font-weight:600;border-bottom-color:var(--gold)}
.topsearch{margin-left:auto;display:flex;gap:.4rem;align-items:center}
.topsearch input{font-family:var(--sans);font-size:.86rem;padding:.45rem .7rem;border:1px solid var(--line);border-radius:999px;background:#fff;min-width:180px;color:var(--ink)}
.topsearch input:focus{outline:none;border-color:var(--mut)}
.burger{display:none;background:none;border:1px solid var(--line);border-radius:.5rem;padding:.35rem .6rem;font-size:1rem;cursor:pointer;color:var(--ink)}
/* shell */
.shell{flex:1;width:100%;max-width:1400px;margin:0 auto;display:grid;grid-template-columns:264px minmax(0,1fr) 228px;gap:2rem;padding:1.5rem 1rem 3rem;align-items:start}
.side{position:sticky;top:64px;max-height:calc(100vh - 84px);overflow:auto;font-family:var(--sans);font-size:var(--nav-link);padding-right:.5rem}
.side .hd{color:var(--faint);font-size:var(--nav-hd);text-transform:uppercase;letter-spacing:.09em;margin:.7rem 0 .2rem;font-weight:400}
.side .hd:first-child{margin-top:0}
.side a{display:block;padding:.28rem .55rem;border-radius:.45rem;color:var(--ink);line-height:1.35;text-decoration:none;font-size:var(--nav-link)}
.side a:hover{background:#f4f1ea;text-decoration:none}
.side a.on{background:#f4f1ea;font-weight:600;color:var(--ink)}
.side .sub a{padding-left:1rem;color:#4a463c;font-size:var(--nav-link)}
.side details.mnav{margin:.9rem 0 .3rem}
.side details.mnav summary{cursor:pointer;list-style:none}
.side details.mnav summary::-webkit-details-marker{display:none}
.side details.mnav summary::after{content:"";display:inline-block;margin-left:.4em;vertical-align:.15em;border-left:.32em solid transparent;border-right:.32em solid transparent;border-top:.42em solid var(--mut);transition:transform .15s}
.side details.mnav[open] summary::after{transform:rotate(180deg)}
.side .n{color:var(--faint);font-size:var(--nav-count);font-family:var(--sans)}
.side details.mnav summary{cursor:pointer;list-style:none;font-size:var(--nav-hd)}
.side .hd{color:var(--faint);font-size:.68rem;text-transform:uppercase;letter-spacing:.09em;margin:.7rem 0 .2rem;font-weight:400}
.side a b,.side b{font-weight:600}
.idx a b,.panel b{font-weight:600}
main{min-width:0;max-width:46rem}
.crumbs{font-family:var(--sans);font-size:.78rem;color:var(--mut);margin-bottom:.6rem}
.crumbs a{color:var(--mut)}
h1{font-weight:500;font-size:34px;letter-spacing:.01em;line-height:1.2;margin:.2rem 0 .4rem}
h2{font-weight:500;font-size:25px;margin:1.6rem 0 .3rem}
.klabel{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mut)}
.sub{color:var(--mut);font-size:15px;margin-bottom:1rem}
.sub a{color:var(--gold-ink)}
.dev{font-family:var(--deva);font-size:23px;line-height:1.75;margin-bottom:3px}
.iast{color:var(--mut);font-size:14px;font-style:italic;margin-bottom:7px}
.en{font-size:15px;max-width:72ch;line-height:1.6}
.skt{white-space:pre-wrap;font-size:1.05rem;font-family:var(--deva)}
.lede{font-size:1.1rem;line-height:1.6;margin-bottom:1rem}
.stats{display:flex;gap:26px;flex-wrap:wrap;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0;margin-bottom:26px;font-size:14px;color:var(--mut)}
.stats b{color:var(--ink);font-weight:600}
/* verse grid */
.verse{display:grid;grid-template-columns:64px 1fr;column-gap:18px;padding:17px 0;border-top:1px solid var(--line)}
.vnum{grid-row:1/4;font-size:12px;color:var(--mut);padding-top:7px;font-variant-numeric:tabular-nums}
/* depth tabs */
.depth{margin:.8rem 0;position:sticky;top:57px;background:var(--paper);padding:.35rem 0;z-index:5;border-bottom:1px solid var(--line)}
.depth button{font-family:var(--sans);font-size:14px;padding:.45rem .9rem;margin:0 .3rem .3rem 0;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.depth button.on{background:var(--ink);color:var(--paper);border-color:var(--ink);font-weight:600}
.depth button.missing{opacity:.45}
/* cards */
.panel{margin:1rem 0;padding:0;border:0;background:none}
.panel.missing{opacity:.6;border-left:2px dashed var(--line);padding-left:1rem}
.idx a{display:flex;gap:10px;color:var(--ink);text-decoration:none;font-size:14px;padding:6px 0;border-bottom:1px solid var(--line);font-family:var(--sans)}
.idx a:hover{text-decoration:underline}
.ev{margin:.5rem 0;padding-left:1rem;position:relative}
.ev .dot{display:none}
.tl{border-left:2px solid var(--ink);margin:1rem 0 1rem .4rem;padding-left:1.1rem}
.hero img{width:100%;border-radius:4px;border:1px solid var(--line)}
.hero .cap{font-family:var(--sans);font-size:.76rem;color:var(--mut);margin-top:.4rem;line-height:1.5}
/* right rail */
.toc{position:sticky;top:64px;max-height:calc(100vh - 84px);overflow:auto;font-family:var(--sans);font-size:.82rem;border-left:1px solid var(--line);padding-left:1rem}
.toc .hd{color:var(--mut);font-size:.7rem;text-transform:uppercase;letter-spacing:.09em;margin-bottom:.4rem}
.toc a{display:block;padding:.2rem 0;color:#4a463c;line-height:1.4;text-decoration:none}
.toc a.on{color:var(--ink);font-weight:600}
/* prev/next + footer */
.pn{display:flex;justify-content:space-between;gap:1rem;margin:2rem 0 0;padding-top:1rem;border-top:1px solid var(--line);font-family:var(--sans);font-size:.88rem}
footer{border-top:1px solid var(--line);background:var(--card);margin-top:auto}
footer .fin{max-width:1400px;margin:0 auto;padding:1.2rem 1rem;font-family:var(--sans);font-size:.8rem;color:var(--mut);display:flex;gap:1.2rem;flex-wrap:wrap}
footer a{color:var(--gold-ink)}
@media(max-width:1100px){.shell{grid-template-columns:240px minmax(0,1fr)}.toc{display:none}}
@media(max-width:800px){
.shell{grid-template-columns:minmax(0,1fr)}
.side{position:fixed;inset:57px auto 0 0;width:min(84vw,320px);background:var(--paper);border-right:1px solid var(--line);z-index:60;padding:1rem;transform:translateX(-105%);transition:transform .2s;max-height:none}
body.navopen .side{transform:none}
.burger{display:block}
.topsearch input{min-width:0;width:110px}
main{max-width:100%}
.depth{top:53px}
.verse{grid-template-columns:1fr}.vnum{grid-row:auto;padding:0 0 4px}.dev{font-size:20px}
}
"""
RECITECSS = """
/* recitation */
.rbar{position:fixed;left:0;right:0;bottom:0;z-index:80;background:#fff;border-top:1px solid var(--line);box-shadow:0 -4px 18px rgba(23,20,15,.08)}
.rbar-in{max-width:1400px;margin:0 auto;display:flex;align-items:center;gap:.6rem;padding:.5rem 1rem;font-family:var(--sans);font-size:.84rem}
.rbar .tbtn{border:1px solid var(--line);background:#fff;border-radius:50%;width:2rem;height:2rem;font-size:.9rem;cursor:pointer;color:var(--ink);flex:none}
.rbar .tbtn.main{background:var(--ink);color:#fff;border-color:var(--ink);width:2.4rem;height:2.4rem;font-size:1rem}
.rbar .tbtn:disabled{opacity:.35;cursor:default}
.rmodes{display:flex;border:1px solid var(--line);border-radius:999px;overflow:hidden;flex:none}
.rmodes button{border:0;background:#fff;padding:.35rem .6rem;font-family:var(--sans);font-size:.74rem;cursor:pointer;color:var(--mut);white-space:nowrap}
.rmodes button.on{background:var(--ink);color:#fff}
.rmodes button:disabled{opacity:.35}
.rlabel{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--mut)}
.rlabel b{color:var(--ink);font-weight:600}
.rsrc{font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:.15rem .5rem;flex:none}
.rsrc.studio{color:var(--gold-ink);border-color:var(--gold)}
.rrate{border:1px solid var(--line);border-radius:.4rem;padding:.25rem .3rem;font-size:.8rem;background:#fff;color:var(--ink)}
.rprog{height:2px;background:var(--line);flex:1;min-width:40px;border-radius:2px;overflow:hidden}
.rprog i{display:block;height:100%;width:0;background:var(--gold)}
.vplay{font-family:var(--sans);font-size:.8rem;border:1px solid var(--line);background:#fff;border-radius:999px;padding:.35rem .8rem;cursor:pointer;color:var(--ink)}
.vplay:hover{border-color:var(--gold);color:var(--gold-ink)}
.vplay.all{background:var(--ink);color:#fff;border-color:var(--ink);font-size:.88rem;padding:.5rem 1.1rem}
article.verse{scroll-margin-top:80px}
article.verse.on{border-left:2px solid var(--gold);background:#fffdf7}
article.verse .w.lit{background:#f4ead3;border-radius:3px}
.pada{margin-bottom:.15rem}
.srcbadge{font-family:var(--sans);font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--gold-ink)}
.recitetools{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;margin:.8rem 0;font-family:var(--sans);font-size:.84rem}
.rnote{font-family:var(--sans);font-size:.78rem;color:var(--mut)}
@media(max-width:800px){.rlabel{display:none}.rmodes button{padding:.35rem .4rem;font-size:.68rem}}
"""
RECITEJS = """<script>
(function(){
"use strict";
var items=[],qi=0,si=0,steps=[],mode="verse",rate=1,playing=false;
var audio=new Audio();audio.preload="auto";
var synth=("speechSynthesis" in window)?window.speechSynthesis:null;
var WT=(window.__WT||{});
function $(s,r){return (r||document).querySelectorAll(s)}
function escT(s){return (s||"").replace(/\s+/g," ").trim()}
function saLines(sa){try{return (sa||"").split(/(?<=[\u0964\u0965])/).map(escT).filter(Boolean)}catch(e){return (sa||"").split(/[\u0964\u0965]+/).map(escT).filter(Boolean)}}
function enChunks(en){var parts=(en||"").split(/(?<=[.!?\u0964\u0965])\s+/).map(escT).filter(Boolean);var out=[],cur="";parts.forEach(function(p){if((cur+" "+p).length>220){if(cur)out.push(cur);cur=p}else{cur=(cur?cur+" ":"")+p}});if(cur)out.push(cur);return out.length?out:[escT(en)].filter(Boolean)}
function collect(){
  items=[];
  Array.prototype.forEach.call(document.querySelectorAll("[data-recite]"),function(el){
    items.push({el:el,id:el.getAttribute("data-id")||"",sa:el.getAttribute("data-sa")||"",
      en:el.getAttribute("data-en")||"",audio:el.getAttribute("data-audio")||"",
      label:el.getAttribute("data-label")||""});
  });
}
function segsFor(id,nlines){
  var w=WT[id];if(!w||!w.segs||!w.segs.length)return null;
  if(w.segs.length>=nlines)return w.segs.slice(0,nlines);
  return null;
}
function buildSteps(it){
  var st=[];
  if(mode==="en"){
    if(!it.en)return st;
    enChunks(it.en).forEach(function(c){st.push({k:"sp",lang:"en",text:c,it:it,part:"en"})});
    return st;
  }
  var lines=(mode==="line")?saLines(it.sa):[escT(it.sa)];
  var segs=(mode==="line"&&it.audio)?segsFor(it.id,lines.length):null;
  lines.forEach(function(ln,i){
    if(it.audio){var s={k:"au",url:it.audio,it:it,part:"sa",line:i};if(segs&&segs[i]){s.t0=segs[i][0];s.t1=segs[i][1]}st.push(s)}
    else if(ln){st.push({k:"sp",lang:"sa",text:ln,it:it,part:"sa",line:i})}
  });
  if(mode!=="sa"&&it.en){enChunks(it.en).forEach(function(c){st.push({k:"sp",lang:"en",text:c,it:it,part:"en"})})}
  return st;
}
function pickVoice(lang){
  if(!synth)return null;
  var vs=synth.getVoices?synth.getVoices():[];
  var pref=lang==="sa"?["sa","hi"]:["en"];
  for(var pi=0;pi<pref.length;pi++){for(var i=0;i<vs.length;i++){if((vs[i].lang||"").toLowerCase().indexOf(pref[pi])===0)return vs[i]}}
  return vs.length?vs[0]:null;
}
function utter(text,lang,done){
  if(!synth){done();return}
  try{synth.cancel()}catch(e){}
  var u=new SpeechSynthesisUtterance(text);u.rate=rate;u.lang=lang==="sa"?"sa-IN":"en-US";
  var v=pickVoice(lang);if(v)u.voice=v;
  u.onend=done;u.onerror=done;
  try{synth.speak(u)}catch(e){done()}
}
function bar(){return document.getElementById("rbar")}
function showBar(){
  if(bar()){bar().style.display="block";return}
  var d=document.createElement("div");d.className="rbar";d.id="rbar";d.style.display="block";
  d.innerHTML='<div class="rbar-in"><button class="tbtn" data-r="prev" title="previous">\u23EE</button><button class="tbtn main" data-r="toggle" title="play/pause">\u23F8</button><button class="tbtn" data-r="next" title="next">\u23ED</button><select class="rrate" data-r="mode" title="recitation mode"><option value="sa">Sanskrit only</option><option value="en">English only</option><option value="verse" selected>Verse: SA \u2192 EN</option><option value="line">Line: SA \u2192 EN</option></select><select class="rrate" data-r="rate" title="speed"><option value="0.75">0.75x</option><option value="1" selected>1x</option><option value="1.15">1.15x</option></select><span class="rsrc" data-r="src">browser voice</span><span class="rlabel" data-r="label"></span><div class="rprog"><i data-r="prog"></i></div><button class="tbtn" data-r="close" title="stop">\u2715</button></div>';
  document.body.appendChild(d);
  d.addEventListener("click",function(e){var b=e.target.closest("[data-r]");if(!b)return;var a=b.getAttribute("data-r");
    if(a==="toggle")toggle();else if(a==="next")next(true);else if(a==="prev")prev();else if(a==="close")stop()});
  d.querySelector('[data-r="mode"]').addEventListener("change",function(e){setMode(e.target.value,true)});
  d.querySelector('[data-r="rate"]').addEventListener("change",function(e){rate=parseFloat(e.target.value)||1});
}
function setLabel(html){var l=document.querySelector('[data-r="label"]');if(l)l.innerHTML=html}
function setSrc(studio){var s=document.querySelector('[data-r="src"]');if(!s)return;s.textContent=studio?"studio chant":"browser voice";s.className="rsrc"+(studio?" studio":"")}
function setProg(f){var pr=document.querySelector('[data-r="prog"]');if(pr)pr.style.width=Math.max(0,Math.min(1,f||0))*100+"%"}
function markItem(it){
  Array.prototype.forEach.call(document.querySelectorAll("article.verse.on"),function(x){x.classList.remove("on")});
  if(it&&it.el&&it.el.scrollIntoView){try{it.el.classList.add("on");it.el.scrollIntoView({block:"center",behavior:"smooth"})}catch(e){}}
}
function clearLit(it){if(!it||!it.el)return;Array.prototype.forEach.call(it.el.querySelectorAll(".w.lit"),function(x){x.classList.remove("lit")})}
function litAt(it,t){
  if(!it||!it.el||!it.el.querySelectorAll)return;
  Array.prototype.forEach.call(it.el.querySelectorAll(".w[data-on]"),function(x){
    var on=parseFloat(x.getAttribute("data-on")),off=parseFloat(x.getAttribute("data-off"));
    if(t>=on&&t<=off)x.classList.add("lit");else x.classList.remove("lit");
  });
}
function playStep(){
  if(!playing)return;
  if(si>=steps.length){next(false);return}
  var s=steps[si],it=s.it;
  markItem(it);clearLit(it);
  setLabel("<b>"+escT(it.label||("verse "+(qi+1)))+"</b> &middot; "+(qi+1)+"/"+items.length+(s.part==="en"?" &middot; English":s.part==="sa"?" &middot; Sanskrit":""));
  if(s.k==="au"){
    setSrc(true);
    try{
      if(audio.getAttribute("src")!==s.url){audio.src=s.url}
      var seek=function(){try{if(s.t0!=null)audio.currentTime=s.t0}catch(e){}try{audio.playbackRate=rate;audio.play()}catch(e){advance()} };
      if(audio.readyState>=1)seek();else{audio.onloadedmetadata=seek}
    }catch(e){advance()}
  }else{
    setSrc(false);setProg(0);
    utter(s.text,s.lang,function(){advance()});
  }
}
audio.addEventListener("timeupdate",function(){
  if(!playing||si>=steps.length)return;
  var s=steps[si];if(s.k!=="au")return;
  if(s.t1!=null&&audio.currentTime>=s.t1){advance();return}
  try{var d=audio.duration||1;var base=(s.t0!=null?s.t0:0),span=((s.t1!=null?s.t1:d)-base)||1;setProg((audio.currentTime-base)/span)}catch(e){}
  litAt(s.it,audio.currentTime);
  var w=WT[s.it.id];if(w&&w.dur&&s.t0==null)setProg(audio.currentTime/w.dur);
});
audio.addEventListener("ended",function(){if(playing)advance()});
audio.addEventListener("error",function(){if(playing){var s=steps[si];if(s&&s.k==="au"){s.k="sp";s.lang="sa";s.text=saLines(s.it.sa)[s.line||0]||s.it.sa;playStep()}}});
function advance(){si++;setProg(0);playStep()}
function next(manual){if(!items.length)return;clearLit(items[qi]);qi++;if(qi>=items.length){stop(true);return}startAt(qi)}
function prev(){if(!items.length)return;clearLit(items[qi]);qi=Math.max(0,qi-1);startAt(qi)}
function startAt(i){
  qi=i;var it=items[qi];
  if(mode==="en"&&!it.en){next(false);return}
  steps=buildSteps(it);si=0;
  if(!steps.length){next(false);return}
  playing=true;showBar();
  var m=document.querySelector('[data-r="mode"]');if(m)m.value=mode;
  playStep();
}
function toggle(){
  if(!items.length)return;
  if(playing){playing=false;try{audio.pause()}catch(e){}try{if(synth)synth.cancel()}catch(e){}var t=document.querySelector('[data-r="toggle"]');if(t)t.innerHTML="\u25B6"}
  else{if(!steps.length){if(qi>=items.length)qi=0;startAt(qi);return}playing=true;playStep();var t2=document.querySelector('[data-r="toggle"]');if(t2)t2.innerHTML="\u23F8"}
}
function stop(done){
  playing=false;steps=[];si=0;
  try{audio.pause()}catch(e){}try{if(synth)synth.cancel()}catch(e){}
  if(items[qi])clearLit(items[qi]);
  Array.prototype.forEach.call(document.querySelectorAll("article.verse.on"),function(x){x.classList.remove("on")});
  setProg(0);
  if(done)setLabel("done &middot; "+items.length+" verses");
  var t=document.querySelector('[data-r="toggle"]');if(t)t.innerHTML="\u25B6";
}
function setMode(m,restart){
  mode=m;
  Array.prototype.forEach.call(document.querySelectorAll("[data-mode]"),function(b){b.classList.toggle("on",b.getAttribute("data-mode")===m)});
  var sel=document.querySelector('[data-r="mode"]');if(sel)sel.value=m;
  if(restart&&playing){stop();startAt(qi)}
}
function pageQueue(){
  collect();
  if(!items.length)return;
  showBar();startAt(0);
}
function init(){
  collect();
  Array.prototype.forEach.call(document.querySelectorAll("[data-mode]"),function(b){
    b.addEventListener("click",function(){setMode(b.getAttribute("data-mode"),playing)});
  });
  Array.prototype.forEach.call(document.querySelectorAll("[data-play-idx]"),function(b){
    b.addEventListener("click",function(){collect();var i=parseInt(b.getAttribute("data-play-idx"),10)||0;showBar();startAt(Math.min(i,items.length-1))});
  });
  Array.prototype.forEach.call(document.querySelectorAll("[data-play-all]"),function(b){
    b.addEventListener("click",function(){pageQueue()});
  });
  if("speechSynthesis" in window){try{speechSynthesis.getVoices()}catch(e){}}
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
window.__recite={setMode:setMode,play:pageQueue};
})();</script>"""
CHATJS = """<script>
(function(){
if(!window.API)return;
var btn=document.createElement('button');
btn.textContent='Ask';
btn.style.cssText='position:fixed;bottom:1rem;right:1rem;z-index:90;background:#1c1a17;color:#fff;border:0;border-radius:999px;padding:.6rem 1.1rem;font-family:Inter,sans-serif;font-size:.84rem;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.15)';
document.body.appendChild(btn);
var work=location.pathname.split('/')[1]||'ipvv';
var works=[work];
// multi-text: add works via ?works=ipvv,tantrasara
var wm=new URLSearchParams(location.search).get('works');
if(wm)works=wm.split(',').map(function(w){return w.trim()}).filter(Boolean);
var workStr=works.join(',');
var panel=document.createElement('div');
panel.style.cssText='position:fixed;bottom:4rem;right:1rem;width:min(90vw,360px);max-height:60vh;background:#fff;border:1px solid #e6ddc9;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.12);display:none;flex-direction:column;z-index:90;font-family:Inter,sans-serif';
panel.innerHTML='<div style="padding:.6rem .8rem;border-bottom:1px solid #e6ddc9;font-weight:600;font-size:.84rem;display:flex;justify-content:space-between;align-items:center"><span>Ask '+works.join(', ')+'</span><button id="voicebtn" style="padding:.2rem .5rem;border:1px solid #e6ddc9;border-radius:.4rem;background:#fff;cursor:pointer;font-size:.78rem">🎤</button></div><div id="chatmsgs" style="flex:1;overflow:auto;padding:.6rem .8rem;font-size:.84rem;min-height:120px"></div><div style="padding:.5rem .8rem;border-top:1px solid #e6ddc9;display:flex;gap:.4rem"><input id="chatin" placeholder="Ask or speak..." style="flex:1;padding:.4rem .6rem;border:1px solid #e6ddc9;border-radius:.4rem;font-size:.84rem"/><button id="chatsend" style="padding:.4rem .7rem;background:#1c1a17;color:#fff;border:0;border-radius:.4rem;cursor:pointer;font-size:.84rem">Send</button></div>';
document.body.appendChild(panel);
btn.onclick=function(){panel.style.display=panel.style.display==='flex'?'none':'flex'};
var sid=null;
function addMsg(role,text){var d=document.createElement('div');d.style.cssText='margin:.4rem 0;'+(role==='user'?'text-align:right':'');d.innerHTML='<b>'+(role==='user'?'You':'Assistant')+':</b> '+text;document.getElementById('chatmsgs').appendChild(d);document.getElementById('chatmsgs').scrollTop=99999}
// voice input
var vr=null;
if('webkitSpeechRecognition' in window||'SpeechRecognition' in window){
  var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  vr=new SR();vr.lang='en-US';vr.interimResults=false;
  vr.onresult=function(e){document.getElementById('chatin').value=e.results[0][0].transcript;document.getElementById('chatsend').click()};
  vr.onerror=function(e){addMsg('assistant','Voice error: '+e.error)};
}
var voicebtn=document.getElementById('voicebtn');
if(voicebtn&&vr){voicebtn.onclick=function(){vr.start();voicebtn.textContent='🔴';vr.onend=function(){voicebtn.textContent='🎤'}}}
document.getElementById('chatsend').onclick=function(){
  var msg=document.getElementById('chatin').value.trim();
  if(!msg)return;
  document.getElementById('chatin').value='';
  addMsg('user',msg);
  fetch(window.API+'/api/chat/'+workStr,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,session_id:sid})})
    .then(r=>r.json()).then(d=>{sid=d.session_id;addMsg('assistant',d.reply);if(d.suggestion){var s=document.createElement('div');s.style.cssText='margin:.4rem 0;font-size:.78rem;color:#7c5410;cursor:pointer;text-decoration:underline';s.textContent='→ '+d.suggestion;s.onclick=function(){document.getElementById('chatin').value=d.suggestion;document.getElementById('chatsend').click()};document.getElementById('chatmsgs').appendChild(s)}})
    .catch(e=>addMsg('assistant','Error: '+e.message));
};
})();
</script>"""
VARJS = """<script>
(function(){
if(!window.API)return;
window.acceptVariant=function(btn){
  var work=btn.getAttribute('data-work');var chunk=btn.getAttribute('data-chunk');
  var userId=prompt('Your profile id:');
  if(!userId){return}
  // fetch variants and accept the first one
  fetch(window.API+'/api/variants/'+work+'/'+chunk).then(r=>r.json()).then(d=>{
    if(!d.variants||!d.variants.length){alert('No variants to accept');return}
    var v=d.variants[0];
    // mark as accepted via a new endpoint
    fetch(window.API+'/api/variants/'+v.id+'/accept',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:userId})})
      .then(r=>r.json()).then(d=>alert('Accepted: '+d.id))
      .catch(e=>alert('Error: '+e.message));
  }).catch(e=>alert('Error: '+e.message));
};
window.saveVariant=function(btn){
  var work=btn.getAttribute('data-work');var chunk=btn.getAttribute('data-chunk');
  var textarea=document.getElementById('variant-text-'+work+'-'+chunk);
  var text=textarea?textarea.value.trim():'';
  if(!text){alert('Enter a translation first');return}
  var userId=prompt('Your profile id (from /api/profile):');
  if(!userId){return}
  fetch(window.API+'/api/variants',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:userId,work:work,chunk:chunk,text:text,style:'owner'})})
    .then(r=>r.json()).then(d=>{alert('Saved: '+d.id);textarea.value=''})
    .catch(e=>alert('Error: '+e.message));
};
window.loadVariants=function(btn){
  var c=btn.parentElement;var work=c.getAttribute('data-work');var chunk=c.getAttribute('data-chunk');
  var list=c.querySelector('.vlist');
  if(list.dataset.loaded){list.style.display=list.style.display==='none'?'block':'none';return}
  list.innerHTML='<i>Loading...</i>';
  fetch(window.API+'/api/variants/'+work+'/'+chunk)
    .then(r=>r.json()).then(d=>{
      if(!d.variants||!d.variants.length){list.innerHTML='<i>No saved variants yet.</i>';list.dataset.loaded='1';return}
      list.innerHTML=d.variants.map(v=>'<div class="panel" style="margin:.3rem 0"><b>'+v.style+'</b> <span style="color:#76736e;font-size:.7rem">'+v.created_at+'</span><div style="margin-top:.3rem;white-space:pre-wrap">'+v.text.slice(0,500)+'</div></div>').join('');
      list.dataset.loaded='1';
    }).catch(e=>{list.innerHTML='<i>Error: '+e.message+'</i>'});
};
})();
</script>"""
SHELLJS = """<script>
(function(){
var b=document.getElementById('burger');
if(b){b.addEventListener('click',function(){document.body.classList.toggle('navopen')});}
// persist masters collapse + sidebar scroll across navigations
try{
document.querySelectorAll('details.mnav').forEach(function(mn,ix){
var key=mn.getAttribute('data-mnav')||('mnav'+ix);
var saved=null;try{saved=localStorage.getItem('mnav_'+key)}catch(e){}
if(saved==='0')mn.removeAttribute('open');else if(saved==='1')mn.setAttribute('open','');
else{var path0=location.pathname;
if((key==='masters'&&/^\/masters\//.test(path0))||(key==='scholars'&&/^\/scholars\//.test(path0)))mn.removeAttribute('open');}
mn.addEventListener('toggle',function(){try{localStorage.setItem('mnav_'+key,mn.open?'1':'0')}catch(e){}});
});
var side=document.getElementById('sidenav');
if(side){
  var sp=localStorage.getItem('sidenav_scroll');
  if(sp)side.scrollTop=parseInt(sp,10)||0;
  side.addEventListener('scroll',function(){localStorage.setItem('sidenav_scroll',side.scrollTop)},{passive:true});
}
}catch(e){}
function initToc(){
var toc=document.getElementById('tocbody');
if(!toc)return;
var hs=document.querySelectorAll('main h2, main h3');var html='';
hs.forEach(function(h,i){if(!h.id){h.id='s'+i}html+='<a href="#'+h.id+'" data-t="'+h.id+'">'+h.textContent.slice(0,60)+'</a>'});
toc.innerHTML=html||'<span style="color:#999">—</span>';
var links=Array.prototype.slice.call(toc.querySelectorAll('a'));
function spy(){var y=window.scrollY+120,cur=null;
hs.forEach(function(h){if(h.getBoundingClientRect().top<120)cur=h.id});
links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+cur)});
if(!cur&&links.length)links[0].classList.add('on');}
window.onscroll=function(){spy()};
spy();}
initToc();
// topnav: dropdown toggle + current-section highlight (re-run after swaps)
function initNav(){
var lb=document.getElementById('libbtn');
if(lb&&!lb.dataset.wired){lb.dataset.wired='1';
lb.addEventListener('click',function(e){e.stopPropagation();
var d=lb.parentElement;var open=d.classList.contains('open');
document.querySelectorAll('.topnav .drop.open').forEach(function(x){x.classList.remove('open')});
if(!open)d.classList.add('open');});
document.addEventListener('click',function(){document.querySelectorAll('.topnav .drop.open').forEach(function(x){x.classList.remove('open')})});}
var sec=(location.pathname.split('/').filter(Boolean)[0]||'').replace(/\.html$/,'');
document.querySelectorAll('#topnav a[data-sec]').forEach(function(a){
var on=a.getAttribute('data-sec')===sec;
a.classList.toggle('on',!!on);
});
var inlib=document.querySelector('#topnav .dropmenu a.on');
var lbb=document.getElementById('libbtn');
if(lbb)lbb.classList.toggle('on',!!inlib);
}
initNav();
// instant nav: same-origin clicks fetch + swap <main>, no full reload
function swapMain(html,url,push){
var doc=new DOMParser().parseFromString(html,'text/html');
var nm=doc.querySelector('main');
if(!nm){location.href=url;return;}
document.querySelector('main').innerHTML=nm.innerHTML;
document.title=doc.title||document.title;
var path=new URL(url,location.origin).pathname;
document.querySelectorAll('#sidenav a').forEach(function(a){
var h=a.getAttribute('href')||'';
var t=a.textContent.replace(/^\u203a\s*/,'');
a.textContent=t;
if(h===path){a.textContent='\u203a '+t;}
});
initToc();
initNav();
if(push!==false){try{history.pushState({u:url},'',url)}catch(e){}}
window.scrollTo(0,0);
}
if(!window.__swapBound){window.__swapBound=true;
document.addEventListener('click',function(e){
var a=e.target.closest?e.target.closest('a'):null;
if(!a||!a.href)return;
if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button!==0)return;
if(a.target==='_blank'||a.hasAttribute('download'))return;
try{if(new URL(a.href).origin!==location.origin)return;}catch(x){return;}
try{if(new URL(a.href).hash)return;}catch(x){return;}
if(a.href===location.href)return;
e.preventDefault();
e.stopImmediatePropagation();
fetch(a.href).then(function(r){if(!r.ok)throw 0;return r.text()}).then(function(h){swapMain(h,a.href,true)}).catch(function(){location.href=a.href});
});
document.addEventListener('click',function(e){
var b=e.target.closest?e.target.closest('.depth button'):null;
if(!b)return;
var d=b.closest('.depth');if(!d)return;
d.querySelectorAll('button').forEach(function(x){x.classList.remove('on')});
b.classList.add('on');
d.querySelectorAll('.tpanel').forEach(function(p){p.style.display=p.dataset.p===b.dataset.p?'block':'none'});
});
window.addEventListener('popstate',function(e){
var u=(e.state&&e.state.u)||location.href;
fetch(u).then(function(r){return r.text()}).then(function(h){swapMain(h,u,false)}).catch(function(){location.href=u});
});
}
})();
</script>"""

TMPL = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>""" + FONTS + """<style>""" + CSS + RECITECSS + """</style></head><body>
<header class="topbar"><div class="topbar-in">
<button class="burger" id="burger" aria-label="menu">☰</button>
<a class="brand" href="/index.html"><span class="deva-brand">स्वातन्त्र्य</span><small>freedom</small></a>
<nav class="topnav" id="topnav"><a href="/translations/index.html" data-sec="translations">Read</a><a href="/recite/index.html" data-sec="recite">Recite</a><a href="/practices/index.html" data-sec="practices">Practise</a><a href="/ipvv/pushing.html" data-sec="ipvv">Enquire</a><a href="/tools/index.html" data-sec="tools">Translate</a><a href="/essays/index.html" data-sec="essays">Write</a></nav>
<span class="topsearch"><input id="q" placeholder="Search…" aria-label="search"/></span>
</div></header>
<div class="shell"><aside class="side" id="sidenav">{sidenav}</aside>
<main><div class="crumbs" id="crumbs"></div><div class="klabel">{kicker}</div><h1>{h1}</h1><div class="skt">{subtitle}</div><div class="sub">{sub}</div>{body}<div class="pn" id="pnslot"></div></main>
{toc}</div>
<footer><div class="fin"><span>Display only what is formally done.</span><a href="/support/index.html">Support</a><a href="/tools/index.html">Tools</a><a href="/data/person-schema.json">Schema</a><a href="https://github.com/prx0r/ipvv">Source</a><a href="https://github.com/prx0r/ipvv/issues/new">Improve this page</a></div></footer>
<script>window.API="https://ipvv-api.tradesprior.workers.dev";var __IDX__=null;fetch("/data/search-index.json").then(function(r){return r.json()}).then(function(d){__IDX__=d});
var q=document.getElementById("q");
if(q){q.addEventListener("keydown",function(e){if(e.key==="Enter"&&__IDX__){var v=q.value.toLowerCase();var m=__IDX__.filter(function(x){return x.t.toLowerCase().indexOf(v)>-1}).slice(0,1)[0];if(m&&m.u)location.href=m.u}})}
var c=document.getElementById("crumbs");if(c){var p=location.pathname.split("/").filter(Boolean);var h='<a href="/index.html">home</a>';var acc="";p.forEach(function(seg,i){acc+="/"+seg;var last=i===p.length-1;var t=decodeURIComponent(seg).replace(/[-_]/g," ").replace(/\.html$/,"");h+=(last?" › "+t:' › <a href="'+acc+(acc==="/index"?"":".html")+'">'+t+"</a>")});c.innerHTML=h;}</script>
""" + SHELLJS + """{recitejs}""" + CHATJS + """{varjs}""" + """</body></html>"""

def tabs(panels):
    btns, divs = [], []
    for i, (name, body, ok) in enumerate(panels):
        cls = "" if ok else "missing"
        on = "on" if i == 0 and ok else ""
        btns.append(f'<button class="{on}{"" if ok else " missing"}" data-p="{i}">{name}{"" if ok else " · soon"}</button>')
        divs.append(f'<div class="panel tpanel {cls}" data-p="{i}" style="display:{"block" if i==0 else "none"}">{body or "<i>not yet formally done — never invented</i>"}</div>')
    js = """<script>document.querySelectorAll('.depth').forEach(function(d){d.querySelectorAll('button').forEach(function(b){b.onclick=function(){d.querySelectorAll('button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');d.querySelectorAll('.tpanel').forEach(function(p){p.style.display=p.dataset.p===b.dataset.p?'block':'none'})}})})</script>"""
    return '<div class="depth" role="tablist">' + "".join(btns) + "</div>" + "".join(divs) + js

def esc(s): return html.escape(str(s or ""))

TOC_ASIDE = '<aside class="toc"><div class="hd">On this page</div><div id="tocbody"></div></aside>'

def TF(tmpl, **kw):
    """Format a template on EXACT {placeholders} only — CSS/JS/content braces pass through untouched."""
    if "toc" not in kw:
        kw["toc"] = TOC_ASIDE
    for k, v in kw.items():
        tmpl = tmpl.replace("{" + k + "}", str(v))
    for k in ("kicker", "subtitle", "recitejs"):
        tmpl = tmpl.replace("{" + k + "}", "")
    for k in ("title", "h1", "sub", "body", "sidenav"):
        if "{" + k + "}" in tmpl:
            raise KeyError("unfilled placeholder in template: {" + k + "}")
    return tmpl

def srclink(path, note=""):
    """Edit-this-page affordance: exact source file on GitHub, or issues link for external/R2 sources."""
    if path.startswith("http"):
        link = f'<a href="{path}">propose a correction →</a>'
    else:
        link = f'<a href="https://github.com/prx0r/ipvv/edit/master/{path}">edit source →</a>'
    extra = f" {esc(note)}" if note else ""
    return f'<div class="sub">Sources & corrections: {link}.{extra}</div>'

def pn(prev_url, prev_label, next_url, next_label):
    l = f'<a href="{prev_url}">← {esc(prev_label)}</a>' if prev_url else "<span></span>"
    r = f'<a href="{next_url}">{esc(next_label)} →</a>' if next_url else "<span></span>"
    return f'<div class="pn">{l}{r}</div>'

def pushing_cards(sub):
    """Q→GEM probe index from vendored volume prose (site/data/pushing/<sub>/)."""
    src = ROOT / "data/pushing" / sub
    dest = DIST / "data/pushing" / sub
    dest.mkdir(parents=True, exist_ok=True)
    cards = []
    if not src.exists():
        return [f"<div class='panel missing'>probes pending — volume path <i>research-library/recognition/pushing-{sub}/</i> not yet vendored</div>"]
    for f in sorted(src.glob("*.md")) + sorted(src.glob("*.txt")):
        raw = f.read_text(encoding="utf-8", errors="replace")
        shutil.copy(f, dest / f.name)
        lines = [l for l in raw.splitlines() if l.strip()][:28]
        title = lines[0].lstrip("# ").strip() if lines else f.stem
        body = "\n".join(lines[1:])[:1100]
        cards.append(f'<div class="panel"><b>{esc(title)}</b> <span class="sub">{esc(f.stem)} · {len(raw.splitlines())} lines</span><div class="en">{esc(body)}{"…" if len(body) == 1100 else ""}</div><div class="sub"><a href="/data/pushing/{sub}/{esc(f.name)}">full probe text →</a></div></div>')
    return cards

def build_ipvv():
    src = sorted((PATALA / "data/published/ipvv").glob("pt-passage-*.json"))
    items = [json.loads(p.read_text()) for p in src]
    out = DIST / "ipvv"; out.mkdir(parents=True, exist_ok=True)
    argdir = ROOT / "data/ipvv/argmaps"
    pmap = {"chunkA":"pilot_V1A","chunkB":"pilot_V1B","chunkC":"pilot_V1C","chunkD":"pilot_V1D",
        "chunkE":"pilot_V1E","chunkF":"pilot_V1F","chunkG":"pilot_V1G","chunkH":"pilot_V1H",
        "chunkI":"pilot_V1I","chunkJ":"pilot_V1J","chunkK":"pilot_V1K","chunkL":"pilot_V1L",
        "chunkM":"pilot_V1M","chunkN":"pilot_V1N","chunkV2-A":"pilot_V2A","chunkV2-B":"pilot_V2B",
        "chunkV2-C":"pilot_V2C","chunkV2-D":"pilot_V2D","chunkV2-E":"pilot_V2E","chunkV2-F":"pilot_V2F",
        "chunkV2-G":"pilot_V2G","chunkV2-H":"pilot_V2H","chunkV2-I":"pilot_V2I","chunkV2-J":"pilot_V2J",
        "chunkV2-K":"pilot_V2K","chunkV2-L":"pilot_V2L","chunkV2-M":"pilot_V2M","chunkV2-N":"pilot_V2N",
        "chunkV2-O":"pilot_V2O","chunkV2-P":"pilot_V2P","chunkV2-Q":"pilot_V2Q","chunkV2-R":"pilot_V2R",
        "chunkV2-S":"pilot_V2S","chunkV3-A":"pilot_V3A","chunkV3-C":"pilot_V3C","chunkV3-D":"pilot_V3D",
        "chunkV3-E":"pilot_V3E","chunkV3-F":"pilot_V3F","chunkV3-G":"pilot_V3G","chunkV3-H":"pilot_V3H",
        "chunkV3-I":"pilot_V3I","chunkV3-J":"pilot_V3J","chunkV3-K":"pilot_V3K","chunkV3-L":"pilot_V3L",
        "chunkV3-M":"pilot_V3M","chunkV3-N":"pilot_V3N","chunkV3-O":"pilot_V3O","chunkV3-P":"pilot_V3P"}
    links = []
    pids = [d["id"].split(":")[-1].replace(".md", "") for d in items]
    for idx, d in enumerate(items):
        pid = pids[idx]
        chunk = (d.get("chunk") or "").replace(".md", "")
        src_txt = (d.get("source") or {}).get("text", "") if isinstance(d.get("source"), dict) else ""
        l2 = d.get("l2_text") or ""
        c1 = d.get("c1") or {}
        c1b = c1.get("body", "") if isinstance(c1, dict) else str(c1)
        # argmap + pilot L2 from R2 cache (full, pristine)
        am, l2p = "", ""
        pp = pmap.get(chunk)
        if pp:
            pa, pl = argdir / f"{pp}_ARGUMENT_MAP.md", argdir / f"{pp}_L2_read.md"
            if pa.exists(): am = pa.read_text()
            if pl.exists(): l2p = pl.read_text()
        if chunk == "chunkV3-B-kriya-dvitiyo-k1-7":
            v3b_extra = ""
            for fn, label in [("pilot_V3B_K6_ARGUMENT_MAP.md", "K6 argmap"),
                              ("pilot_V3B_S7_ARGUMENT_MAP.md", "S7 argmap"),
                              ("pilot_V3B_S9_ARGUMENT_MAP.md", "S9 argmap"),
                              ("pilot_V3B_full_L2.md", "full L2"),
                              ("pilot_V3B_k1_L1_apparatus.md", "k1 L1 apparatus"),
                              ("pilot_V3B_k2-7_L1_apparatus.md", "k2-7 L1 apparatus")]:
                p = argdir / fn
                if p.exists():
                    v3b_extra += f'<hr/><div class="sub">{label} (full)</div><div class="en">{esc(p.read_text())}</div>'
            am = (am + v3b_extra) if am else v3b_extra
        extra_l2 = f'<hr/><div class="sub">Pilot L2 (argument-derived, full)</div><div class="en">{esc(l2p)}</div>' if l2p and l2p.strip() != l2.strip() else ""
        body = tabs([
            ("ORIGINAL", f'<div class="dev">{esc(src_txt)}</div><div class="sub">vol {esc(d.get("vol",""))} · {esc(chunk)} · lines via source.start/end</div>', bool(src_txt)),
            ("READ", f'<div class="en">{esc(l2)}</div>{extra_l2}', bool(l2)),
            ("ARGMAP", f'<div class="en">{esc(am)}</div>', bool(am)),
            ("STUDY", f'<div class="en">{esc(c1b)}</div>', bool(c1b)),
            ("GUIDE", None, False),
            ("CRITICAL", f'<div class="en">immutable {esc(d.get("immutable_id",""))} · T1 chunk <i>sanskritree/{esc(chunk)}.md</i> via <i>tools/fetch.sh</i> · L200 8-section audit per <i>specs/C1_SPEC + l200 spec</i> · L1 apparatus: V3B pilot in <i>samples/</i></div>', True),
        ])
        (out / f"{pid}.html").write_text(TF(TMPL,title=pid, h1=pid, sub="IPVV · " + esc(d.get("vol", "")), sidenav=work_sidenav("ipvv"), body='<div class="recitetools"><button class="vplay" data-play-all>Recite this passage</button><span class="rnote">browser-voice readout · four modes in the player bar</span></div>' + body
            + f'<div data-recite data-id="{pid}" data-label="IPVV · {esc(chunk)}" data-sa="{esc(deva_of(src_txt))}" data-en="{esc(l2[:4000])}" style="display:none"></div>'
            + pn(f"/ipvv/{pids[idx-1]}.html" if idx > 0 else None, pids[idx-1] if idx > 0 else "",
                 f"/ipvv/{pids[idx+1]}.html" if idx < len(pids)-1 else None, pids[idx+1] if idx < len(pids)-1 else ""), recitejs=RECITEJS))
        links.append(f'<a href="/ipvv/{pid}.html">{esc(pid)}</a>')
    (out / "index.html").write_text(TF(TMPL,title="IPVV", h1="Īśvarapratyabhijñāvivṛtivimarśinī",
        sub=f"{len(items)} passages · Sanskrit → READ → STUDY · GUIDE soon", sidenav=work_sidenav("ipvv"),
        body='<div class="idx">' + "".join(links) + "</div>" + srclink("https://github.com/prx0r/ipvv/issues/new", "passages generated from patala corpus (other repo) + R2 pilot cache — corrections welcome here.")))
    # themes: machine-proposed clusters (honestly labeled) + adjudication evidence packet
    try:
        cl = json.loads((PATALA / "data/published/ipvv/clusters.json").read_text())
        cls = cl.get("clusters", [])
        for _f in ("clusters.json", "clusters.report.txt", "adjudication-cl3.json", "essay-cl3.json",
                   "essay-cl3.md", "goldchain-cl3.json", "argument_comparison.json", "index.json",
                   "theme-map-ipvv-v0.json", "theme-discovery-ipvv-v0.json"):
            _s = ROOT / "data/themes" / _f
            if _s.exists():
                (DIST / "data/themes").mkdir(parents=True, exist_ok=True)
                shutil.copy(_s, DIST / "data/themes" / _f)
        def _stat(cid):
            return "adjudication proposed — awaiting review" if cid == "CL-3" else "machine proposal — no editor decision yet"
        tb = "".join(f'<div class="panel"><b>{esc(c.get("cluster_id",""))}</b> · {c.get("size",0)} members · coherence {c.get("coherence","")} · <i>{_stat(c.get("cluster_id",""))}</i><br/>{esc(", ".join(c.get("member_c1_ids",[])[:12]))}</div>' for c in cls)
        tb += '<div class="sub">Evidence packet (machine-readable): <a href="/data/themes/clusters.json">clusters</a> · <a href="/data/themes/clusters.report.txt">editorial report</a> · <a href="/data/themes/adjudication-cl3.json">CL-3 adjudication</a> · <a href="/data/themes/essay-cl3.md">CL-3 essay</a> · <a href="/data/themes/goldchain-cl3.json">CL-3 gold chain</a> · <a href="/data/themes/theme-map-ipvv-v0.json">v0 theme map (63 segments, candidates)</a></div>'
    except Exception as e:
        tb = f"<i>themes pending: {esc(str(e))}</i>"
    (out / "themes.html").write_text(TF(TMPL,title="IPVV themes", h1="Themes", sub="machine-proposed clusters — overlapping, never partition; zero accepted themes yet", sidenav=work_sidenav("ipvv"), body=tb
        + '<div class="sub" style="margin-top:1rem"><a href="/themes/adjudicate.html">Adjudicate clusters →</a> (accept/merge/split — calls Worker API)</div>'))
    # adjudication page
    adj_out = DIST / "themes"; adj_out.mkdir(parents=True, exist_ok=True)
    adj_cards = []
    for c in cls:
        cid = c.get("cluster_id", "")
        members = ", ".join(c.get("member_c1_ids", [])[:8])
        adj_cards.append(f'<div class="panel" data-cluster="{cid}"><b>{cid}</b> · {c.get("size",0)} members · coherence {c.get("coherence","")}<br/><span style="font-size:.8rem;color:#76736e">{esc(members)}</span><br/>'
                        + '<div style="margin-top:.5rem;display:flex;gap:.4rem;flex-wrap:wrap">'
                        + f'<button onclick="decide(&quot;{cid}&quot;,&quot;accept&quot;)" style="padding:.3rem .6rem;border:1px solid var(--line);border-radius:.4rem;background:var(--card);cursor:pointer;font-size:.8rem">Accept</button>'
                        + f'<button onclick="decide(&quot;{cid}&quot;,&quot;reject&quot;)" style="padding:.3rem .6rem;border:1px solid var(--line);border-radius:.4rem;background:var(--card);cursor:pointer;font-size:.8rem">Reject</button>'
                        + f'<button onclick="decide(&quot;{cid}&quot;,&quot;merge&quot;)" style="padding:.3rem .6rem;border:1px solid var(--line);border-radius:.4rem;background:var(--card);cursor:pointer;font-size:.8rem">Merge</button>'
                        + f'<button onclick="decide(&quot;{cid}&quot;,&quot;split&quot;)" style="padding:.3rem .6rem;border:1px solid var(--line);border-radius:.4rem;background:var(--card);cursor:pointer;font-size:.8rem">Split</button>'
                        + '</div><div class="decisions" style="margin-top:.4rem;font-size:.8rem"></div></div>')
    adj_js = """<script>
    function decide(cid, dec) {
      var note = prompt('Note (optional):');
      fetch(window.API+'/api/themes/decide',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cluster_id:cid,decision:dec,note:note})})
        .then(r=>r.json()).then(d=>{alert(cid+' -> '+dec);loadDecisions()})
        .catch(e=>alert('Error: '+e.message));
    }
    function loadDecisions() {
      if(!window.API)return;
      fetch(window.API+'/api/themes/decisions').then(r=>r.json()).then(d=>{
        (d.decisions||[]).forEach(function(dec){
          var el=document.querySelector('[data-cluster="'+dec.cluster_id+'"] .decisions');
          if(el) el.innerHTML='<b>'+dec.decision+'</b> '+dec.created_at+(dec.note?' — '+dec.note:'');
        });
      });
    }
    if(window.API) loadDecisions();
    </script>"""
    adj_body = "".join(adj_cards) + adj_js
    (adj_out / "adjudicate.html").write_text(TF(TMPL,title="Theme adjudication", h1="Theme adjudication",
        kicker="Adjudicate", sub="machine-proposed clusters — accept/merge/split/multi-assign; decisions saved to profile",
        sidenav=work_sidenav("ipvv"), body=adj_body,
        recitejs="", chatjs="", varjs=""))

    # pushing: real Q->GEM probe index (vendored volume prose, fail-closed excerpts)
    pb = ("<h3>IPVV probes</h3>" + "".join(pushing_cards("ipvv"))
          + "<h3>Tantraloka probes</h3><div class='sub'>Abhinavagupta's other magnum opus — same method, different mountain. Full TĀ display section pending; probes live here first.</div>"
          + "".join(pushing_cards("tantraloka"))
          + "<h3>Recognition research dossiers</h3><div class='sub'>The enquiry program behind the probes: transitions with verdicts, agent spec, comparative dossier, reading sequence, provisional Ajaḍapramātṛsiddhi translation.</div>"
          + "".join(pushing_cards("research"))
          + "<h3>Rasa audit</h3><div class='sub'>Quote-validation of the rasa thesis against Dyczkowski's text — attribution corrections (PTv vs TĀ vs footnote), the traceability discipline applied.</div>"
          + "".join(pushing_cards("rasa"))
          + "<h3>Bodhapañcadaśikā probes</h3><div class='sub'>Abhinavagupta's 15-verse doctrinal hymn, pushed as a 5-session arc: forgetting → terror → grace → necessity → dissolution. Same method, new mountain.</div>"
          + "".join(pushing_cards("bodhapancadasika")))
    (out / "pushing.html").write_text(TF(TMPL,title="IPVV pushing", h1="Pushing", sub="Q→GEM deep-dives at varying depth — hound the text with why, the text answers first", sidenav=work_sidenav("ipvv"), body=pb
        + srclink("site/data/pushing/", "probe prose vendored from volume research-library/recognition/; parsed pushing.py records next.")))
    return len(items)

def build_vbt():
    d = json.load(open(VOL / "source-library/tantra/lakshmanjoo/vb_lakshmanjoo.json"))
    vs = d.get("verses", [])
    bd = json.load(open("/root/deitybody/site/frameworks/vbt/body-dharanas.json"))
    seats = {x.get("v"): x for x in bd.get("dharanas", [])}
    out = DIST / "vbt"; out.mkdir(parents=True, exist_ok=True)
    links = []
    nums = [v.get("number") for v in vs[:145]]
    for vi, v in enumerate(vs[:145]):
        n = v.get("number")
        skt, en = v.get("sanskrit", ""), v.get("english", "")
        seat = seats.get(n, {})
        body = tabs([
            ("ORIGINAL", f'<div class="dev">{esc(skt)}</div>', bool(skt)),
            ("READ", f'<div class="en">{esc(en[:2000])}</div>', bool(en)),
            ("GUIDE", None, False),
            ("STUDY", f'<div class="en">attention-seat: {esc(seat.get("locus","—"))} · do: {esc(seat.get("do","—"))}</div>', bool(seat)),
            ("CRITICAL", f'<div class="en">VBT verse {n} · Lakshmanjoo/KSTS</div>', True),
        ])
        (out / f"v{n}.html").write_text(TF(TMPL,title=f"VBT {n}", h1=f"Verse {n}", sub="Vijñānabhairava", sidenav=work_sidenav("vbt"), body='<div class="recitetools"><button class="vplay" data-play-all>Recite this verse</button><span class="rnote">browser-voice readout · four modes in the player bar</span></div>' + body
            + f'<div data-recite data-id="vbt-{n}" data-label="VBT verse {n}" data-sa="{esc(deva_of(skt))}" data-en="{esc(en[:4000])}" style="display:none"></div>'
            + pn(f"/vbt/v{nums[vi-1]}.html" if vi > 0 else None, f"verse {nums[vi-1]}" if vi > 0 else "",
                 f"/vbt/v{nums[vi+1]}.html" if vi < len(nums)-1 else None, f"verse {nums[vi+1]}" if vi < len(nums)-1 else ""), recitejs=RECITEJS))
        links.append(f'<a href="/vbt/v{n}.html">verse {n}</a>')
    (out / "index.html").write_text(TF(TMPL,title="VBT", h1="Vijñānabhairava Tantra",
        sub=f"{len(vs)} verses · catalog of entries, not graded course", sidenav=work_sidenav("vbt"), body='<div class="idx">' + "".join(links) + "</div>" + srclink("https://github.com/prx0r/ipvv/issues/new", "verses from Lakshmanjoo mapping (other repo); seats from deitybody — corrections welcome here.")))
    (out / "themes.html").write_text(TF(TMPL,title="VBT themes", h1="Themes", sub="by upaya/tattva (sanskrithelp mapping)", sidenav=work_sidenav("vbt"),
        body='<div class="panel">Breath · Void/gap · Light · Sound/mantra · Senses · Energy/kundalini · Sexual yoga · Direct recognition. Full mapping: <i>sanskrithelp/data/rag/vijnana-bhairava-mapping.md</i>.</div>'))
    (out / "pushing.html").write_text(TF(TMPL,title="VBT pushing", h1="Pushing", sub="liminal states, goddess, gaps", sidenav=work_sidenav("vbt"),
        body='<div class="panel">Start: V75 edge-of-sleep (para devi prakasate), V24 heart↔12-end, V50 any 12-end. Q→GEM index next.</div>'))
    return len(vs)

def build_tantrasara():
    e0 = json.load(open("/tmp/tantrasara/build/canon/essay0.json"))
    units = e0.get("units", {})
    out = DIST / "tantrasara"; out.mkdir(parents=True, exist_ok=True)
    links = []
    keys = list(units.keys())
    for ki, k in enumerate(keys):
        u = units[k]
        body = tabs([
            ("ORIGINAL", f'<div class="en">span {esc(u.get("text_span",""))} · lines {esc(str(u.get("text_line_range","")))}<br/>{esc(u.get("text",""))}</div>', bool(u.get("text"))),
            ("READ", f'<div class="en">{esc(u.get("plain",""))}</div>', bool(u.get("plain"))),
            ("GUIDE", None, False),
            ("STUDY", f'<div class="en">Q: {esc(u.get("question",""))}</div>', True),
            ("CRITICAL", f'<div class="en">alternates: {esc(str(u.get("alternates",""))[:500])}</div>', True),
        ])
        (out / f"q{k}.html").write_text(TF(TMPL,title=f"TS Q{k}", h1=esc(u.get("question", f"Q{k}")), sub="Tantrasara essay-0", sidenav=work_sidenav("tantrasara"), body=body
            + pn(f"/tantrasara/q{keys[ki-1]}.html" if ki > 0 else None, f"Q{keys[ki-1]}" if ki > 0 else "",
                 f"/tantrasara/q{keys[ki+1]}.html" if ki < len(keys)-1 else None, f"Q{keys[ki+1]}" if ki < len(keys)-1 else "")))
        links.append(f'<a href="/tantrasara/q{k}.html">{esc(u.get("question",""))}</a>')
    (out / "index.html").write_text(TF(TMPL,title="Tantrasara", h1="Tantrasāra",
        sub=f"{len(units)} questions · verbatim → plain · audio pending", sidenav=work_sidenav("tantrasara"), body='<div class="idx">' + "".join(links) + "</div>" + srclink("https://github.com/prx0r/ipvv/issues/new", "essay-0 units from prx0r/tantrasara (other repo) — corrections welcome here.")))
    (out / "themes.html").write_text(TF(TMPL,title="TS themes", h1="Themes", sub="upaya ladder, saktipata, uccara", sidenav=work_sidenav("tantrasara"),
        body='<div class="panel">Next: run ahnika-11 through full pipe, cluster C1s like IPVV.</div>'))
    (out / "pushing.html").write_text(TF(TMPL,title="TS pushing", h1="Pushing", sub="why-questions per ahnika", sidenav=work_sidenav("tantrasara"),
        body='<div class="panel">Q→GEM scaffolds next, same pushing.py extractor.</div>'))
    return len(units)

def work_sidenav(work, active=""):
    """Contextual left sidebar per section. Masters get the full tree."""
    sec = ""
    if work in ("ipvv", "vbt", "tantrasara"):
        sec = ('<div class="hd">This work</div>'
               f'<a href="/{work}/index.html">{"› " if active=="index" else ""}Index</a>'
               f'<a href="/{work}/themes.html">{"› " if active=="themes" else ""}Themes</a>'
               f'<a href="/{work}/pushing.html">{"› " if active=="pushing" else ""}Pushing</a>')
    elif work == "translations":
        sec = '<div class="hd">This section</div><a href="/translations/index.html">All translations</a>'
    elif work == "concepts":
        sec = ('<div class="hd">This section</div><a href="/concepts/index.html">All concepts</a>'
               '<a href="/tools/index.html">Tools</a>')
    elif work in ("scholars", "tools"):
        sec = ""
    return (_masters_nav()
        + sec +
        '<div class="hd">Modern</div><a href="/scholars/index.html">Scholars</a>'
        '<div class="hd">Library</div>'
        '<a href="/concepts/index.html">Concepts</a>'
        '<a href="/translations/index.html">Translations</a>'
        '<a href="/tools/index.html">Tools</a>')

ATmpl = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>""" + FONTS + """<style>""" + CSS + RECITECSS + """</style></head><body>
<header class="topbar"><div class="topbar-in">
<button class="burger" id="burger" aria-label="menu">☰</button>
<a class="brand" href="/index.html"><span class="deva-brand">स्वातन्त्र्य</span><small>freedom</small></a>
<nav class="topnav" id="topnav"><a href="/translations/index.html" data-sec="translations">Read</a><a href="/recite/index.html" data-sec="recite">Recite</a><a href="/practices/index.html" data-sec="practices">Practise</a><a href="/ipvv/pushing.html" data-sec="ipvv">Enquire</a><a href="/tools/index.html" data-sec="tools">Translate</a><a href="/essays/index.html" data-sec="essays">Write</a></nav>
<span class="topsearch"><input id="q" placeholder="Search…" aria-label="search"/></span>
</div></header>
<div class="shell"><aside class="side" id="sidenav">{sidenav}</aside>
<main><div class="crumbs" id="crumbs"></div><div class="klabel">{kicker}</div><h1>{h1}</h1><div class="skt">{subtitle}</div><div class="sub">{sub}</div>{body}<div class="pn" id="pnslot"></div></main>
{toc}</div>
<footer><div class="fin"><span>Display only what is formally done.</span><a href="/support/index.html">Support</a><a href="/tools/index.html">Tools</a><a href="/data/person-schema.json">Schema</a><a href="https://github.com/prx0r/ipvv">Source</a><a href="https://github.com/prx0r/ipvv/issues/new">Improve this page</a></div></footer>
<script>window.API="https://ipvv-api.tradesprior.workers.dev";var __IDX__=null;fetch("/data/search-index.json").then(function(r){return r.json()}).then(function(d){__IDX__=d});
var q=document.getElementById("q");
if(q){q.addEventListener("keydown",function(e){if(e.key==="Enter"&&__IDX__){var v=q.value.toLowerCase();var m=__IDX__.filter(function(x){return x.t.toLowerCase().indexOf(v)>-1}).slice(0,1)[0];if(m&&m.u)location.href=m.u}})}
var c=document.getElementById("crumbs");if(c){var p=location.pathname.split("/").filter(Boolean);var h='<a href="/index.html">home</a>';var acc="";p.forEach(function(seg,i){acc+="/"+seg;var last=i===p.length-1;var t=decodeURIComponent(seg).replace(/[-_]/g," ").replace(/\\.html$/,"");h+=(last?" › "+t:' › <a href="'+acc+(acc==="/index"?"":".html")+'">'+t+"</a>")});c.innerHTML=h;}</script>
""" + SHELLJS + """{recitejs}""" + CHATJS + """{varjs}""" + """</body></html>"""

STATUS_LABEL = {"SOURCE_ONLY": "Sanskrit held", "SOURCE_ONLY_DISPUTED": "Sanskrit held · disputed",
    "SOURCE_PLUS_TRANSLATION": "Sanskrit + English", "SOURCE_PLUS_SCHOLARSHIP": "Sanskrit + scholarship",
    "SOURCE_CHUNKED": "chunked, awaiting T1", "ESSAY0": "essay-0", "PUBLISHED_49": "full display (49)",
    "STOCKPILE": "listed", "LOST": "LOST", "REF_ONLY": "ref-only", "FRAGMENT": "fragments",
    "ATTRIBUTED_DISPUTED": "ascription disputed", "STOCKPILE_UNVERIFIED": "listed · unverified",
    "TEACHER_ONLY": "teacher — no independent works", "SOURCE_HELD": "full Sanskrit held"}

def author_paths(aid):
    a = ROOT / "data/authors" / f"{aid}.json"
    w = ROOT / "data" / f"works_{aid}.json"
    return a, w

def _short_name(n):
    """Nav display name: strip parenthetical epithets ('Ksemaraja (Rajanaka ...)')."""
    return n.split(' (')[0].strip()


def _masters_by_works():
    """Masters sorted by work count desc, then name. Backend order for nav."""
    out = []
    for m in MASTERS:
        try:
            a = json.loads((ROOT / "data/authors" / f"{m}.json").read_text())
            w = json.loads((ROOT / "data" / f"works_{m}.json").read_text())
            out.append((m, _short_name(a.get("name", m)), len(w) if isinstance(w, list) else 0))
        except Exception:
            out.append((m, m, 0))
    out.sort(key=lambda x: (-x[2], x[1]))
    return out


def _masters_chrono():
    """Masters sorted by birth year (nulls last), then name. Backend order for index data."""
    out = []
    for m in MASTERS:
        try:
            a = json.loads((ROOT / "data/authors" / f"{m}.json").read_text())
            b = (a.get("dates") or {}).get("birth")
            out.append((m, a.get("name", m), b if isinstance(b, int) else 9999))
        except Exception:
            out.append((m, m, 9999))
    out.sort(key=lambda x: (x[2], x[1]))
    return out


def _masters_nav(active_mid=""):
    items = "".join(
        f'<a href="/{m}/index.html">{"› " if m == active_mid else ""}{esc(n)} <span class="n">({c})</span></a>'
        for m, n, c in _masters_by_works())
    return ('<details class="mnav" data-mnav="masters" open><summary class="hd">Masters (by works)</summary>'
            '<div class="sub">' + items + '</div></details>')

def sidenav(aid, active=""):
    author = json.loads(author_paths(aid)[0].read_text())
    works = json.loads(author_paths(aid)[1].read_text())
    items = "".join(f'<a href="/{aid}/{w["id"]}.html">{"› " if w["id"]==active else ""}{esc(w["title"])}</a>' for w in works)
    masters = _masters_nav(aid)
    return (masters
        + f'<div class="hd">{esc(author["name"])}</div>'
        f'<a href="/{aid}/index.html">{"› " if active=="bio" else ""}Bio</a>'
        f'<a href="/{aid}/works.html">{"› " if active=="works" else ""}Works map</a>'
        '<div class="hd">Works (canonical list)</div><div class="sub">' + items + "</div>"
        + '<div class="hd">Library</div><a href="/concepts/index.html">Concepts</a>'
        + '<a href="/translations/index.html">Translations</a><a href="/tools/index.html">Tools</a>')

MASTERS = ["abhinavagupta", "somananda", "vasugupta", "kallata", "utpaladeva",
           "lakshmanagupta", "sambhunatha", "ksemaraja", "bhutiraja", "jayaratha",
           "yogaraja", "bhattanarayana", "induraja", "sivopadhyaya", "lalla"]

def build_split(aid, wid):
    """Split a big Sanskrit file into per-section pages. Returns section count."""
    import re
    out = DIST / aid
    if wid == "tantraloka":
        txt = (ROOT / "data/sanskrit/tantraloka.txt").read_text()
        srcfile, srclabel = "site/data/sanskrit/tantraloka.txt", "GRETIL KSTS text, vendored"
        parts = re.split(r"(?m)^(?=:C\d+ )", txt)
        heads = re.findall(r"(?m)^:C\d+ .{0,60}", txt)
    elif wid == "tantrasara":
        txt = (ROOT / "data/sanskrit/tantrasara.txt").read_text()
        srcfile, srclabel = "site/data/sanskrit/tantrasara.txt", "GRETIL KSTS 17 text, vendored"
        parts = re.split(r"(?m)^(?=Tantras.+hnikam)", txt)
        heads = re.findall(r"(?m)^Tantras.+hnikam.*$", txt)
    else:
        return 0
    # first chunk is preamble before section 1 (usually tiny); merge into section 1
    if len(parts) == len(heads) + 1:
        parts[1] = parts[0] + parts[1]; parts = parts[1:]
    n = 0
    for i, (h, p) in enumerate(zip(heads, parts), 1):
        n += 1
        prev = f'<a href="/{aid}/{wid}-{i-1}.html">← {i-1}</a>' if i > 1 else ""
        nxt = f'<a href="/{aid}/{wid}-{i+1}.html">{i+1} →</a>' if i < len(heads) else ""
        nav = f'<div class="nav">{prev} <a href="/{aid}/{wid}.html">all {len(heads)}</a> {nxt}</div>' + srclink(srcfile, srclabel + "; English READ next via pipe.")
        body = nav + tabs([("ORIGINAL", f'<div class="dev skt">{esc(p.strip())}</div>', True),
            ("READ", None, False), ("GUIDE", None, False),
            ("STUDY", f'<div class="en">Section {i} of {len(heads)} — English READ next via pipe.</div>', True),
            ("CRITICAL", f'<div class="en">GRETIL/Mukhabodha; section head: {esc(h.strip()[:80])}</div>', True)]) + nav
        (out / f"{wid}-{i}.html").write_text(TF(ATmpl,title=f"{wid} §{i}", h1=f"Section {i}",
            sub=esc(h.strip()[:80]), sidenav=sidenav(aid, wid), body=body))
    return n

def author_bio_body(aid, author, lin, spine):
    hero = ""
    if author.get("image"):
        im = author["image"]
        hero = (f'<figure style="margin:0 0 1rem"><img src="{esc(im["src"])}" alt="{esc(author["name"])} — related imagery" loading="lazy" style="max-width:100%;border-radius:8px"/>'
                f'<figcaption class="sub">{esc(im["caption"])} Credit: <a href="{esc(im["credit_url"])}">{esc(im["credit"])}</a> · <a href="{esc(im["licence_url"])}">{esc(im["licence"])}</a></figcaption></figure>')
    return (f'<p class="lede">{esc(author["summary"])}</p>' + hero
            + (f'<p>{esc(author["bio"])}</p>' if author.get("bio") else "")
            + lin
            + read_alongside_html(aid))

def read_alongside_html(aid):
    """Modern-scholar cross-links for a master (site/data/read_alongside.json)."""
    try:
        ra = json.loads((ROOT / "data/read_alongside.json").read_text()).get(aid, [])
        sch = {s["id"]: s for s in json.loads((ROOT / "data/scholars.json").read_text())}
        rows = "; ".join(f'<a href="/scholars/{r["scholar"]}.html">{esc(sch[r["scholar"]]["name"])}</a> — {esc(r["why"])}'
                       for r in ra if r["scholar"] in sch)
        return f"<p>Read alongside {rows}.</p>" if rows else ""
    except Exception:
        return ""

def read_with_html(sid):
    """Reverse cross-links: which masters list this scholar as read-alongside."""
    try:
        ra = json.loads((ROOT / "data/read_alongside.json").read_text())
        rows = []
        for aid, rs in ra.items():
            for r in rs:
                if r["scholar"] == sid:
                    try: nm = json.loads((ROOT / "data/authors" / f"{aid}.json").read_text())["name"]
                    except Exception: nm = aid
                    rows.append(f'<div class="ev"><a href="/{aid}/index.html"><b>{esc(nm)}</b></a> — {esc(r["why"])}</div>')
        return f"<h3>Read with</h3>{''.join(rows)}" if rows else ""
    except Exception:
        return ""

def build_author(aid="abhinavagupta"):
    out = DIST / aid; out.mkdir(parents=True, exist_ok=True)
    apath, wpath = author_paths(aid)
    author = json.loads(apath.read_text())
    works = json.loads(wpath.read_text())
    _lin_parts = [f'{esc(l.get("relation","")).rstrip(" :")} {esc(l.get("who",""))}' for l in author.get("lineage", []) if l.get("who")]
    lin = (f'<p>{" · ".join(_lin_parts)}.</p>' if _lin_parts else "")
    spine = {"abhinavagupta": "Raghavan “Abhinavagupta and His Works” 36 + attested extras",
             "utpaladeva": "Wikipedia/BnF/kashmirhope + GRETIL/Mukhabodha holdings",
             "ksemaraja": "Singh/SUNY + Flood 2020 + kashmirhope + ePustakalay/KSTS holdings"}.get(aid, "")
    (out / "index.html").write_text(TF(ATmpl,title=author["name"], h1=esc(author["name"]),
        sub=f'{esc(author["dates"]["flourished"])} · {esc(author.get("place",""))}', sidenav=sidenav(aid, "bio"), toc="",
        body=author_bio_body(aid, author, lin, spine)))
    cats = {}
    for w in works:
        cats.setdefault(w.get("category", "?"), []).append(w)
    blocks = []
    for c, ws in cats.items():
        rows = "".join(
            f'<div class="ev"><span class="dot" style="{"background:#ccc" if w.get("extant") is False else ""}"></span>'
            + f'<b>{esc(w["title"])}</b> — {esc(w.get("date",""))} · {esc(STATUS_LABEL.get(w.get("status",""), w.get("status","")))}'
            + f'<br/><a href="/{aid}/{w["id"]}.html">open →</a></div>' for w in ws)
        blocks.append(f"<h3>{esc(c)}</h3>" + rows)
    n_ext = sum(1 for w in works if w.get("extant") is True)
    n_lost = sum(1 for w in works if w.get("extant") is False)
    n_unk = len(works) - n_ext - n_lost
    (out / "works.html").write_text(TF(ATmpl,title="Works map", h1="Works map",
        sub=f"canonical list: {len(works)} works ({n_ext} extant, {n_lost} lost/ref-only, {n_unk} unverified) — click any title", sidenav=sidenav(aid, "works"),
        body=f'<div class="tl">{"".join(blocks)}</div>'
             f'<div class="sub">Spine: {spine} · <a href="/data/works_{aid}.json">machine-readable JSON</a></div>'
             + srclink(f"site/data/works_{aid}.json", "canonical works list lives here.")))
    for w in works:
        wid = w["id"]
        label = STATUS_LABEL.get(w.get("status", ""), w.get("status", ""))
        meta = f'{esc(w.get("date",""))} · {esc(label)}'
        if w.get("verses") not in (None, ""): meta += f' · {esc(w["verses"])}'
        # pipeline translation link, if ingested (PASS-gated English lives there)
        trlink = ""
        trfile = ROOT / "data/translations" / f"{wid}.json"
        # contentions: falsifiable claims tied to this work (basecamp research objects)
        cfiles = sorted((ROOT / "data/contentions").glob("*.json"))
        clinks = []
        for cf in cfiles:
            try:
                co = json.loads(cf.read_text())
            except Exception:
                continue
            if not isinstance(co, dict):
                continue
            sid = str(co.get("source_id") or co.get("target_question_id") or "")
            if wid not in sid and wid.replace("-", "") not in sid.replace("-", ""):
                continue
            title = co.get("title") or co.get("question") or cf.stem
            fals = ""
            claims = co.get("claims")
            if isinstance(claims, list) and claims and isinstance(claims[0], dict):
                fals = claims[0].get("falsifier", "")
            clinks.append(f'<div class="panel"><b>{esc(str(title)[:90])}</b>'
                         f'<div class="sub">{esc(cf.name)}</div>'
                         f'<div class="en">{esc(str(fals)[:180])}</div>'
                         f'<div class="sub"><a href="/contentions/{esc(cf.stem)}.html">open contention →</a></div></div>')
        contention_block = ("<h3>Contentions</h3>" + "".join(clinks)) if clinks else ""
        if trfile.exists():
            import json as _j
            _items = _j.loads(trfile.read_text())
            _np = sum(1 for _i in _items if _i.get("gate") == "PASS")
            trlink = (f'<div class="panel">Pipeline translation: <b><a href="/translations/{wid}.html">open →</a></b> '
                      f'({_np}/{len(_items)} passages passed the gate; English shows for those only)</div>')
        tf = w.get("text_file")
        sf = w.get("sanskrit_file")
        eds = "".join(f'<div class="sub">▪ {esc(e)}</div>' for e in w.get("editions", []))
        src_note = f'<div class="sub">{esc(w.get("sanskrit_source",""))}</div>' if w.get("sanskrit_source") else ""
        if w.get("sanskrit") == "split-ahnika":
            n = build_split(aid, wid)
            body = (f'<div class="panel">Full Sanskrit in <b>{n} sections</b> — click in. {esc(w.get("note",""))}</div>'
                    + "".join(f'<div class="ev"><a href="/{aid}/{wid}-{i}.html">section {i} →</a></div>' for i in range(1, n + 1)))
        elif sf:
            sp = ROOT / "data/sanskrit" / sf
            txt = sp.read_text() if sp.exists() else ""
            if txt and len(txt) > 500000:
                body = (f'<div class="panel">Full Sanskrit ({len(txt)//1024}KB) — <a href="/data/sanskrit/{sf}"><b>read/download full text →</b></a></div>'
                        + (f'<div class="panel">{esc(w.get("note",""))}</div>' if w.get("note") else "")
                        + tabs([("ORIGINAL (head)", f'<div class="dev skt">{esc(txt[:15000])}\n…[continued in full text]</div>', True),
                            ("READ", None, False), ("GUIDE", None, False),
                            ("STUDY", f'<div class="en">{esc(w["title"])} — English READ next via pipe.</div>', True),
                            ("CRITICAL", f'<div class="en">{esc(w.get("sanskrit_source",""))} · {meta}</div>', True)]))
            else:
                body = tabs([("ORIGINAL", f'<div class="dev skt">{esc(txt)}</div>', bool(txt)),
                    ("READ", None, False), ("GUIDE", None, False),
                    ("STUDY", f'<div class="en">{esc(w["title"])} — full Sanskrit above; English READ next via pipe.</div>', True),
                    ("CRITICAL", f'<div class="en">{esc(w.get("sanskrit_source",""))} · {meta}</div>', True)])
        elif tf:
            p = Path("/root/deitybody/corpus/stotra") / tf
            txt = p.read_text() if p.exists() else ""
            body = tabs([("ORIGINAL", f'<div class="dev">{esc(txt)}</div>', bool(txt)),
                ("READ", None, False), ("GUIDE", None, False),
                ("STUDY", f'<div class="en">{esc(w["title"])} — full Sanskrit above; English READ next via pipe.</div>', True),
                ("CRITICAL", f'<div class="en">deitybody corpus/stotra/{tf} · {meta}{eds}</div>', True)])
        elif w.get("link"):
            thesis = '<div class="panel">Thesis: recognition — the self re-cognises itself as the Lord.</div>' if wid == "ipvv" else ""
            vols = ""
            if wid == "ipvv":
                vols = ('<div class="panel">Full Sanskrit vols (Mukhabodha IAST, CC BY-NC 4.0): '
                        '<a href="/data/sanskrit/ipvv-vol1.txt">Vol 1</a> · '
                        '<a href="/data/sanskrit/ipvv-vol2.txt">Vol 2</a> · '
                        '<a href="/data/sanskrit/ipvv-vol3.txt">Vol 3</a></div>')
            body = (f'<div class="panel">Full display: <b><a href="{w["link"]}">open →</a></b></div>'
                    + vols
                    + (f'<div class="panel">{esc(w["note"])}</div>' if w.get("note") else "")
                    + thesis
                    + (eds if w.get("editions") else ""))
        else:
            note = w.get("note", "")
            sfs = "".join(f'<div class="panel">Sanskrit text: <a href="/data/sanskrit/{f}"><b>{esc(f)} →</b></a></div>' for f in w.get("sanskrit_files", []))
            root = ""
            if w.get("sanskrit_root"):
                root = (f'<div class="panel">Related root text (comm. itself undigitized): '
                        f'<a href="/data/sanskrit/{w["sanskrit_root"]}"><b>{esc(w["sanskrit_root"])} →</b></a></div>')
            if w.get("status") in ("LOST", "REF_ONLY", "FRAGMENT", "ATTRIBUTED_DISPUTED", "SOURCE_ONLY_DISPUTED"):
                why = {"LOST": "references in the tradition", "REF_ONLY": "references in the tradition", "FRAGMENT": "quotations in the tradition", "ATTRIBUTED_DISPUTED": "a disputed ascription — verify before teaching as his", "SOURCE_ONLY_DISPUTED": "a disputed ascription — listed, flagged, never taught as his"}[w.get("status")]
                body = (f'<div class="panel missing"><b>{esc(label)}.</b> No text survives; known only from {esc(why)}.</div>'
                    + (f'<div class="panel">{esc(note)}</div>' if note else "")
                    + eds)
            else:
                body = ((f'<div class="panel">{esc(note)}</div>' if note else "")
                    + sfs + root + eds
                    + f'<div class="panel">Status: {esc(label)}. Next via pipe: cut SOURCE → T1 → L0 → argmap → L2 → L200 → C1.</div>')
        (out / f"{wid}.html").write_text(TF(ATmpl,title=w["title"], h1=esc(w["title"]),
            sub=meta, sidenav=sidenav(aid, wid), body=trlink + contention_block + body + srclink(f"site/data/works_{aid}.json", "canonical entry lives here.")))
    # ship machine-readable data with the site
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    (DIST / "data" / f"author_{aid}.json").write_text(json.dumps(author, ensure_ascii=False, indent=1))
    (DIST / "data" / f"works_{aid}.json").write_text(json.dumps(works, ensure_ascii=False, indent=1))
    import shutil as _sh2
    _sh2.copy(ROOT.parent / "specs/schema/person.json", DIST / "data/person-schema.json")
    # ship ALL held Sanskrit bytes (research/education use; licence in each header)
    sdir = DIST / "data/sanskrit"; sdir.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "data/sanskrit").glob("*.txt"):
        shutil.copy(f, sdir / f.name)
    if (ROOT / "data/roots.json").exists():
        shutil.copy(ROOT / "data/roots.json", DIST / "data/roots.json")
    return len(works)

def ship_translations():
    # ship ingested pipeline translations (PASS-gated English + gate status)
    tdir = DIST / "data/translations"; tdir.mkdir(parents=True, exist_ok=True)
    for f in (ROOT / "data/translations").glob("*.json"):
        shutil.copy(f, tdir / f.name)

def scholar_nav(active=""):
    scholars = sorted(json.loads((ROOT / "data/scholars.json").read_text()), key=lambda s: s.get("name", ""))
    items = "".join(f'<a href="/scholars/{s["id"]}.html">{"› " if s["id"]==active else ""}{esc(s["name"])}</a>' for s in scholars)
    masters = _masters_nav(active if active in MASTERS else "")
    sch = ('<details class="mnav" data-mnav="scholars"><summary class="hd">Scholars</summary>'
           '<div class="sub"><a href="/scholars/index.html">All scholars</a>' + items + "</div></details>")
    return (masters + sch
        + '<div class="hd">Library</div><a href="/concepts/index.html">Concepts</a>'
        + '<a href="/translations/index.html">Translations</a><a href="/tools/index.html">Tools</a>')

ACC_LABEL = {"open": "open access", "login": "free login wall", "metadata": "metadata only — fetch via academia/DOI",
             "print": "print/commercial — cite, never host", "study": "in-repo study material"}

def build_sections():
    """Top-level taxonomy, backend-first: masters chronological by birth, modern alphabetical."""
    import json as _j
    masters = []
    for m, n, y in _masters_chrono():
        ap = ROOT / "data/authors" / f"{m}.json"
        a = _j.loads(ap.read_text())
        masters.append({"id": m, "name": a.get("name", n), "url": f"/{m}/index.html",
                        "birth": a.get("dates", {}).get("birth"), "flourished": a.get("dates", {}).get("flourished", ""),
                        "summary": a.get("summary", "")})
    scholars = sorted(_j.loads((ROOT / "data/scholars.json").read_text()), key=lambda s: s.get("name", ""))
    _border = {m: i for i, (m, _, _) in enumerate(_masters_by_works())}
    masters.sort(key=lambda m: _border.get(m["id"], 999))
    modern = [{"id": s["id"], "name": s["name"], "url": f'/scholars/{s["id"]}.html',
               "affiliation": s.get("affiliation", ""), "summary": s.get("summary", "")} for s in scholars]
    sec = {"sections": [
        {"id": "masters", "title": "Masters", "rule": "premodern author-masters, chronological by birth year (nulls last); undocumented dates flagged, never invented",
         "members": [m["id"] for m in masters]},
        {"id": "modern", "title": "Modern", "rule": "living scholars alphabetical (birth years are private, never asserted) + lineage teachers",
         "members": [m["id"] for m in modern]}]}
    (ROOT / "data/sections.json").write_text(_j.dumps(sec, ensure_ascii=False, indent=1))
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "data/sections.json", DIST / "data/sections.json")
    out = DIST / "masters"; out.mkdir(parents=True, exist_ok=True)
    cards = "".join(
        f'<a href="/{m["id"]}/index.html"><b>{esc(_short_name(m["name"]))}</b> — {esc(str(m["birth"]) if m["birth"] else m["flourished"] or "date unknown")}</a>'
        for m in masters)
    (out / "index.html").write_text(TF(ATmpl,title="Masters", h1="Masters",
        sub="premodern author-masters — click any name, bio loads first",
        sidenav=scholar_nav(""), body=f'<div class="idx">{cards}</div>'
        f'<div class="sub">Order: most works first · full dates on each bio · <a href="/data/sections.json">machine-readable taxonomy</a></div>' + srclink("site/data/authors/", "per-master JSON + person schema; birth years live in dates.birth.")))
    out2 = DIST / "modern"; out2.mkdir(parents=True, exist_ok=True)
    cards = "".join(f'<a href="{m["url"]}"><b>{esc(m["name"])}</b> — {esc(m.get("affiliation",""))}</a>' for m in modern)
    (out2 / "index.html").write_text(TF(ATmpl,title="Modern", h1="Modern",
        sub="living scholars A–Z + lineage teachers — secondary witnesses, linked not hosted",
        sidenav=scholar_nav("index"), body=f'<div class="idx">{cards}</div>'
        f'<div class="sub"><a href="/data/sections.json">machine-readable taxonomy</a></div>' + srclink("site/data/scholars.json", "all bios + bibliographies live here.")))
    return len(masters), len(modern)

def _esc(x): return esc(x)

def build_translations():
    """Pipeline translations: PASS passages display L1/L2 with gate badge;
    BLOCKED passages show Sanskrit + withheld notice (never English-as-translation)."""
    import json as _json
    src = ROOT / "data/translations"
    if not src.exists():
        return 0
    out = DIST / "translations"; out.mkdir(parents=True, exist_ok=True)
    links = []
    for f in sorted(src.glob("*.json")):
        items = _json.loads(f.read_text())
        if not items:
            continue
        wid = f.stem
        n_pass = sum(1 for i in items if i.get("gate") == "PASS")
        blocks, rdis = [], []
        for it in items:
            badge = ("PASS" if it["gate"] == "PASS"
                     else "WITHHELD — pending review (" + ", ".join(it.get("blocking", ["review"])) + ")")
            if it["gate"] == "PASS":
                body = tabs([
                    ("ORIGINAL", f'<div class="dev skt">{esc(it["sanskrit"])}</div>', bool(it["sanskrit"])),
                    ("L1", f'<div class="en">{esc(it.get("l1",""))}</div>', bool(it.get("l1"))),
                    ("READ", f'<div class="en">{esc(it.get("l2",""))}</div>', bool(it.get("l2"))),
                    ("CRITICAL", f'<div class="en">gate: PASS · model {esc(it.get("model",""))} · {esc(it.get("date",""))} · machine-proposed, needs human review before doctrine use</div>', True)])
            else:
                body = (f'<div class="panel"><div class="dev skt">{esc(it["sanskrit"])}</div></div>'
                        f'<div class="panel missing"><b>{badge}.</b> English withheld until the gate passes — fail-closed.</div>')
            blocks.append(f'<h3>{esc(it.get("chunk",""))} · verses {esc(it.get("verses",""))} · {badge.split(" — ")[0]}</h3>' + body)
            _chunk_id = it.get("chunk", "")
            _am = ROOT / "data/argmaps" / wid / f"{_chunk_id}.md"
            _c1 = ROOT / "data/c1" / wid / f"{_chunk_id}.md"
            if _am.exists():
                _amt = _am.read_text(encoding="utf-8", errors="replace")
                blocks.append(f'<div class="panel"><div class="sub"><b>Argument map</b> · {len(_amt.split())} words</div><pre style="white-space:pre-wrap;font-size:.85rem;font-family:var(--serif);color:var(--ink)">{esc(_amt[:3000])}</pre><div class="sub"><a href="/data/argmaps/{wid}/{esc(_chunk_id)}.md">source →</a></div></div>')
            if _c1.exists():
                _c1t = _c1.read_text(encoding="utf-8", errors="replace")
                blocks.append(f'<div class="panel"><div class="sub"><b>C1 commentary</b> · {len(_c1t.split())} words</div><div class="en">{esc(_c1t[:2000])}</div><div class="sub"><a href="/data/c1/{wid}/{esc(_chunk_id)}.md">source →</a></div></div>')
            blocks.append(f'<div class="variant-switcher" data-work="{wid}" data-chunk="{esc(it.get("chunk",""))}" style="margin:.5rem 0;font-family:var(--sans);font-size:.8rem"><button onclick="loadVariants(this)" style="padding:.3rem .7rem;border:1px solid var(--line);border-radius:.4rem;background:var(--card);cursor:pointer">Show variants →</button><div class="vlist" style="margin-top:.4rem"></div><div style="margin-top:.4rem"><input id="variant-text-{wid}-{esc(it.get("chunk",""))}" placeholder="Paste your translation..." style="width:100%;padding:.4rem;border:1px solid var(--line);border-radius:.4rem;font-size:.8rem;margin-top:.3rem"/><button onclick="saveVariant(this)" data-work="{wid}" data-chunk="{esc(it.get("chunk",""))}" style="margin-top:.3rem;padding:.3rem .7rem;border:1px solid var(--line);border-radius:.4rem;background:var(--card);cursor:pointer;font-size:.8rem">Save as variant →</button><div style="margin-top:.3rem"><button onclick="acceptVariant(this)" data-work="{wid}" data-chunk="{esc(it.get("chunk",""))}" style="padding:.3rem .7rem;border:1px solid #2e7d32;border-radius:.4rem;background:#e8f5e9;cursor:pointer;font-size:.8rem;color:#2e7d32">Accept best →</button></div></div></div>')
            en_r = (it.get("l2") or it.get("l1") or "") if it["gate"] == "PASS" else ""
            rdis.append(f'<div data-recite data-id="{wid}-{esc(it.get("chunk",""))}" data-label="{esc(wid)} · {esc(it.get("chunk",""))}" data-sa="{esc(deva_of(it.get("sanskrit","")))}" data-en="{esc(en_r[:4000])}" style="display:none"></div>')
        abase = AUDIO_ALIAS.get(wid, wid)
        chant = f'<div class="recitetools"><a class="vplay all" href="/recite/{abase}.html">Studio chant + recitation →</a></div>' if (ROOT / f"data/audio-{abase}.json").exists() else ""
        (out / f"{wid}.html").write_text(TF(ATmpl,title=f"Translation: {wid}",
            h1=f"Translation: {wid}", kicker="Pipeline translation", sub=f"{n_pass}/{len(items)} passages passed the gate — only those show English",
            sidenav=work_sidenav(""), body=chant + '<div class="recitetools"><button class="vplay" data-play-all>Recite this work</button><span class="rnote">browser-voice readout · four modes in the player bar</span></div>' + f'<div class="stats"><span><b>{len(items)}</b> passages</span><span><b>{n_pass}</b> PASS</span><span><b>{len(items)-n_pass}</b> withheld</span></div>'+"".join(blocks) + "".join(rdis) + srclink("https://github.com/prx0r/ipvv/issues/new", "English derives from R2 batch-t1 drafts (pipeline); corrections welcome here."), recitejs=RECITEJS, varjs=VARJS))
        links.append((wid, n_pass, len(items)))
    (out / "index.html").write_text(TF(ATmpl,title="Translations", h1="Pipeline translations",
        sub="English shows ONLY for gate-PASS passages; the rest stay Sanskrit + status",
        sidenav=work_sidenav(""), body='<div class="idx">'
        + "".join([f'<a href="/translations/{w}.html"><b>{w}</b> — {p}/{n} PASS</a>' for w, p, n in links]) + "</div>" + srclink("tools/ingest_batch.py", "ingest script; sources are R2 batch-t1 drafts.")
        + '<div class="sub">Audit trail: <a href="/data/receipts.jsonl">receipts.jsonl</a> — one machine-readable record per chunk (gates, evidence hash, license, model, date).</div>'))
    return len(links)

def slugify(s):
    import unicodedata as _u
    s = _u.normalize("NFD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "term"

def build_glossary():
    import json as _j
    gl = _j.loads((ROOT / "data/glossary.json").read_text())
    out = DIST / "concepts"; out.mkdir(parents=True, exist_ok=True)
    slugs = [slugify(e["term"]) for e in gl]
    for ei, e in enumerate(gl):
        slug = slugs[ei]
        links = "".join(f'<div class="ev"><a href="/ipvv/{p}.html">IPVV: {esc(p)}</a></div>' for p in e.get("passages", [])[:20])
        (out / f"{slug}.html").write_text(TF(ATmpl,title=e["term"], h1=esc(e["term"]),
            sub="concept · glossary", sidenav=work_sidenav(""),
            body=f'<div class="panel">{esc(e.get("gloss") or "occurrence only — definition pending curation.")}</div>'
                 + (f"<h3>Occurs in</h3>{links}" if links else "<p><i>No linked passages yet.</i></p>")
                 + f'<div class="sub">source: {esc(e.get("source",""))} · <a href="/data/glossary.json">machine-readable glossary</a></div>'
                 + srclink("site/data/glossary.json", "term lives here; mined by tools/build_glossary.py.")
                 + pn(f"/concepts/{slugs[ei-1]}.html" if ei > 0 else None, gl[ei-1]["term"] if ei > 0 else "",
                      f"/concepts/{slugs[ei+1]}.html" if ei < len(gl)-1 else None, gl[ei+1]["term"] if ei < len(gl)-1 else "")))
    idx = "".join(f'<a href="/concepts/{slugify(e["term"])}.html"><b>{esc(e["term"])}</b> — {esc((e.get("gloss") or "")[:90])}</a>' for e in gl)
    (out / "index.html").write_text(TF(ATmpl,title="Concepts", h1="Concepts",
        sub=f"{len(gl)} terms — definitions link to every occurrence", sidenav=work_sidenav(""),
        body='<input id="q" placeholder="filter terms…" style="width:100%;padding:.6rem;font-size:1rem;margin-bottom:.6rem"/>'
             f'<div class="idx" id="terms">{idx}</div>'
             '<script>q.oninput=()=>{const v=q.value.toLowerCase();document.querySelectorAll("#terms a").forEach(a=>a.style.display=a.textContent.toLowerCase().includes(v)?"":"none")}</script>'
             '<div class="sub"><a href="/data/glossary.json">machine-readable glossary</a> · mined from C1 key-terms + curated core</div>' + srclink("tools/build_glossary.py", "miner lives here.")))
    shutil.copy(ROOT / "data/glossary.json", DIST / "data/glossary.json")
    (DIST / "data" / "authors").mkdir(parents=True, exist_ok=True)
    for _af in (ROOT / "data" / "authors").glob("*.json"):
        shutil.copy(_af, DIST / "data" / "authors" / _af.name)
    shutil.copy(ROOT / "data" / "scholars.json", DIST / "data" / "scholars.json")
    return len(gl)

def md_lite(src):
    """Minimal markdown renderer for vendored prose (essays). Escape-first, block rules only."""
    import re as _re
    out, para, lst = [], [], False
    def flush_p():
        nonlocal para
        if para:
            out.append("<p>" + " ".join(para) + "</p>"); para = []
    def flush_l():
        nonlocal lst
        if lst:
            out.append("</ul>"); lst = False
    def inline(s):
        s = esc(s)
        s = _re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = _re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"<i>\1</i>", s)
        s = _re.sub(r"`(.+?)`", r"<code>\1</code>", s)
        return s
    for ln in src.splitlines():
        s = ln.strip()
        if not s:
            flush_p(); flush_l(); continue
        if s.startswith("### "): flush_p(); flush_l(); out.append(f"<h3>{inline(s[4:])}</h3>"); continue
        if s.startswith("## "): flush_p(); flush_l(); out.append(f"<h2>{inline(s[3:])}</h2>"); continue
        if s.startswith("# "): flush_p(); flush_l(); out.append(f"<h1>{inline(s[2:])}</h1>"); continue
        if s in ("---", "***"): flush_p(); flush_l(); out.append("<hr/>"); continue
        if s.startswith("> "): flush_p(); flush_l(); out.append(f"<blockquote>{inline(s[2:])}</blockquote>"); continue
        if s.startswith(("- ", "* ")): flush_p(); 
        if not lst: out.append("<ul>"); lst = True
        out.append(f"<li>{inline(s[2:])}</li>"); continue
        para.append(inline(ln.strip()))
    flush_p(); flush_l()
    return "\n".join(out)

ESSAY_GROUPS = [
 ("Comparative — IPVV against the traditions", ["two-abhinavaguptas-ipvv-tantraloka","spanda-ipvv","krama-ipvv","advaita-ipvv","buddhist-ipvv","rasa-ipvv-abhinavabharati","sivasutra-vb-ipvv"]),
 ("Core proofs — the recognition thesis", ["ultimate-proof-of-recognition","why-recognition-is-felt","nonconstructed-i","felt-to-ground","recognition-and-formal-proofs","recognition-and-nisargadatta","epistemology-of-action","exclusion-individuation","soteriology-of-recognition"]),
 ("Extensions", ["abhinava-extensions","abhinava-vs-utpaladeva","c-razor-ipvv-authority","ontology-soteriology","other-intersubjectivity"]),
]
REVIEWED_ESSAYS = {"advaita-ipvv","buddhist-ipvv","epistemology-of-action","exclusion-individuation","felt-to-ground","ipvv-vs-tantraloka","krama-ipvv","nonconstructed-i","rasa-ipvv-abhinavabharati","recognition-and-formal-proofs","recognition-and-nisargadatta","sivasutra-vb-ipvv","soteriology-of-recognition","spanda-ipvv","two-abhinavaguptas-ipvv-tantraloka","ultimate-proof-of-recognition","why-recognition-is-felt"}

def essay_arg_links(slug):
    """Return HTML linking an essay to its argument packets."""
    try:
        links = json.loads((ROOT / "data/essay-links/links.json").read_text())
        pids = links.get(slug, [])
        if not pids:
            return ""
        rows = "".join(f'<div class="ev"><a href="/arguments/{pid.split(":")[-1]}.html"><b>{esc(pid.split(":")[-1])}</b></a></div>' for pid in pids[:12])
        return f"<h3>Referenced arguments ({len(pids)})</h3>{rows}<div class='sub'><a href='/arguments/index.html'>all arguments →</a></div>"
    except Exception:
        return ""

def arg_essay_links(pid):
    """Return HTML linking an argument packet to essays that reference it."""
    try:
        links = json.loads((ROOT / "data/essay-links/links.json").read_text())
        essays = [slug for slug, pids in links.items() if f"pt:argument:ipvv:{pid}" in pids or pid in [p.split(":")[-1] for p in pids]]
        if not essays:
            return ""
        rows = "".join(f'<div class="ev"><a href="/essays/{slug}.html"><b>{esc(slug)}</b></a></div>' for slug in essays)
        return f"<h3>Referenced by essays ({len(essays)})</h3>{rows}"
    except Exception:
        return ""

def build_essays():
    """Owner's recognition essays (vendored volume prose, displayed as written)."""
    import json as _json
    src = ROOT / "data/essays"
    out = DIST / "essays"; out.mkdir(parents=True, exist_ok=True)
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob("*.md")):
        shutil.copy(f, DIST / "data" / ("essay-" + f.name))
    cards, cardmeta = [], []
    for f in sorted(src.glob("*.md")):
        raw = f.read_text(encoding="utf-8", errors="replace")
        lines = raw.splitlines()
        title = next((l.lstrip("# ").strip() for l in lines if l.startswith("# ")), f.stem)
        stand = next((l.strip().strip("*").strip() for l in lines if l.strip().startswith("*") and len(l.strip()) > 20), "")
        slug = f.stem.lower().replace("essay-", "")
        words = len(raw.split())
        badge = '<span class="srcbadge">peer-reviewed Aug 2026</span>' if slug in REVIEWED_ESSAYS else '<span class="rsrc">working paper</span>'
        (out / f"{slug}.html").write_text(TF(ATmpl, title=title, h1=esc(title),
            kicker="Essay", sub=esc(stand[:220]),
            sidenav=work_sidenav(""), body=f'<div class="sub">{words} words · owner\u2019s working essay, displayed as written · {badge} · <a href="/data/essay-{esc(f.name)}">source markdown</a></div>'
            + essay_arg_links(slug)
            + md_lite(raw)
            + srclink("site/data/essays/" + f.name, "essay source lives here.")))
        cards.append(f'<a href="/essays/{slug}.html"><b>{esc(title)}</b> — {esc(stand[:140])} {"[reviewed]" if slug in REVIEWED_ESSAYS else "[working]"}</a>')
        cardmeta.append((slug, title, stand))
    byslug = {}
    for (slug, title, stand) in cardmeta:
        byslug[slug] = f'<a href="/essays/{slug}.html"><b>{esc(title)}</b> — {esc(stand[:140])} {"[reviewed]" if slug in REVIEWED_ESSAYS else "[working]"}</a>'
    grouped = "".join(f"<h3>{g}</h3>" + '<div class="idx">' + "".join(byslug[s] for s in slugs if s in byslug) + "</div>" for g, slugs in ESSAY_GROUPS)
    (out / "index.html").write_text(TF(ATmpl, title="Essays", h1="Essays",
        kicker="Working papers", sub="the owner\u2019s recognition essays — theses argued from the translations, displayed as written",
        sidenav=work_sidenav(""), body=grouped
        + srclink("site/data/essays/", "essay sources live here.")))
    return len(cards)

def build_pushing_hub():
    """One place for all pushing work: method specs + probe collections + essay link."""
    import json as _json
    out = DIST / "pushing"; out.mkdir(parents=True, exist_ok=True)
    mdest = DIST / "data/pushing-method"; mdest.mkdir(parents=True, exist_ok=True)
    specs = []
    for f in sorted((ROOT.parent / "specs/pushing").glob("*.md")):
        shutil.copy(f, mdest / f.name)
        raw = f.read_text(encoding="utf-8", errors="replace")
        first = next((l.lstrip("# ").strip() for l in raw.splitlines() if l.startswith("# ")), f.stem)
        specs.append(f'<div class="panel"><b>{esc(first)}</b><div class="sub">{esc(f.name)} · {len(raw.split())} words</div><div class="sub"><a href="/data/pushing-method/{esc(f.name)}">read spec →</a></div></div>')
    n_ipvv = len(list((ROOT / "data/pushing/ipvv").glob("*.*")))
    n_ta = len(list((ROOT / "data/pushing/tantraloka").glob("*.*")))
    n_bodha = len(list((ROOT / "data/pushing/bodhapancadasika").glob("*.*")))
    (out / "index.html").write_text(TF(TMPL, title="Pushing", h1="Pushing",
        kicker="Method", sub="hound the text with why until it cannot escape — every probe below is that loop run to an endpoint",
        sidenav=work_sidenav(""), body=
        '<div class="panel"><b>The method in one rule:</b> force the text\u2019s own reasoning to carry the conclusion. Frameworks enter only after the text has spoken. Full procedure in the specs below; the operator instructions in the agent spec.</div>'
        "<h3>How-to and algorithms</h3>" + "".join(specs)
        + f"<h3>Probe collections</h3><div class='idx'><a href='/ipvv/pushing.html'><b>IPVV probes</b> — {n_ipvv} files</a><a href='/ipvv/pushing.html'><b>Tantraloka probes</b> — {n_ta} files</a><a href='/ipvv/pushing.html'><b>Bodhapañcadaśikā probes</b> — {n_bodha} files</a></div>"
        + '<div class="sub">Probes live on the IPVV pushing page (shared method, separate mountains). Essays argued from these cruxes: <a href="/essays/index.html">/essays/</a>.</div>'
        + srclink("https://github.com/prx0r/ipvv/tree/master/specs/pushing", "method specs live here.")))
    return 5 + n_ipvv + n_ta + n_bodha

def build_receipts():
    import hashlib as _h
    import sys as _sys2
    _sys2.path.insert(0, str(ROOT.parent / "tools"))
    from qp_acom import objects as _o
    from qp_acom import receipts as _r
    """Per-chunk audit trail via the vendored qprivately kernel.
    Claim + evidence + versioned gates -> transition() receipt.
    FAIL receipts are first-class: a BLOCKED chunk's receipt records exactly
    what did not pass. Unsigned (proof_level 0); grants/signing are next."""
    import json as _json, sys as _sys
    _sys.path.insert(0, str(ROOT.parent / "tools"))
    from qp_acom import objects as _o
    from qp_acom import receipts as _r
    import qp_gates as _qg
    out = []

    def chunk_receipt(work, chunk, gate, blocking, model, date, src_file,
                      src_lines, lic, imm, has_en, checks):
        asof = date or "2026-10-31"
        src = {"chunk": chunk}
        ev = [
            _o.make_evidence("source_file", src_file or "", "path", asof, src),
            _o.make_evidence("source_lines", src_lines or 0, "line", asof, src),
            _o.make_evidence("source_license", lic or "", "spdx", asof, src),
            _o.make_evidence("immutable_id", imm or "", "id", asof, src),
            _o.make_evidence("gate", gate or "", "verdict", asof, src),
            _o.make_evidence("has_english", bool(has_en), "bool", asof, src),
            _o.make_evidence("gate_checks", checks or {}, "checks", asof, src),
            _o.make_evidence("model", model or "", "model", asof, src),
        ]
        claim = _o.make_claim(f"{work}:{chunk} displays its entitled state",
                              f"translation-display:{work}", "UNKNOWN")
        task = _o.make_task("chunk-display", chunk, {"gate": "decided"})
        run = _o.make_run(task["id"], "pipeline-batch", model or "")
        proposal = {"id": f"{work}:{chunk}", "claim": claim, "target": chunk,
                    "work": work, "gate": gate, "blocking": blocking}
        return _r.transition({"status": "unreviewed"}, proposal, ev,
                             _qg.GATE_IDS, run,
                             transition_type="CHUNK-DISPLAY")

    for f in sorted((ROOT / "data/translations").glob("*.json")):
        for it in _json.loads(f.read_text()):
            out.append(chunk_receipt(
                f.stem, it.get("chunk", "?"), it.get("gate", ""),
                it.get("blocking", []), it.get("model", ""), it.get("date", ""),
                it.get("source_file", ""), it.get("source_lines"),
                it.get("source_license", ""), it.get("immutable_id", ""),
                bool(it.get("l1") or it.get("l2")), it.get("checks", {})))
    for f in sorted((PATALA / "data/published/ipvv").glob("pt-passage-*.json")):
        d = _json.loads(f.read_text())
        out.append(chunk_receipt(
            "ipvv", d.get("chunk", "?"), "PUBLISHED", [], "editor-pipeline",
            "2026-08-11", "patala:published", 0, "mixed-roots",
            d.get("immutable_id", ""), bool((d.get("l2_text") or "").strip()), {}))
    # argument packets (one receipt per packet, via kernel transition())
    for af in sorted((ROOT / "data/arguments").glob("*.json")):
        pkt = _json.loads(af.read_text())
        asof = "2026-10-31"
        src = {"packet": pkt.get("id")}
        ev = [
            _o.make_evidence("packet", pkt.get("id", ""), "id", asof, src),
            _o.make_evidence("work", pkt.get("work_id", ""), "work", asof, src),
            _o.make_evidence("passage", pkt.get("source_passage", ""), "id", asof, src),
            _o.make_evidence("strength", pkt.get("strength", ""), "verdict", asof, src),
            _o.make_evidence("status", pkt.get("status", ""), "verdict", asof, src),
            _o.make_evidence("tension", pkt.get("tension_id") or "", "id", asof, src),
            _o.make_evidence("premises", len(pkt.get("premises", [])), "count", asof, src),
        ]
        claim = _o.make_claim(f"{pkt.get('id','')}: displays its entitled state",
                              f"argument-display:{pkt.get('work_id','')}", "UNKNOWN")
        task = _o.make_task("argument-display", pkt.get("id", ""), {"strength": "decided"})
        run = _o.make_run(task["id"], "pipeline-batch", "")
        proposal = {"id": pkt.get("id", ""), "claim": claim,
                    "target": pkt.get("id", ""), "work": pkt.get("work_id", ""),
                    "gate": "MACHINE_DRAFT", "blocking": []}
        receipt = _r.transition({"status": "unreviewed"}, proposal, ev,
                               ["ipvv/has-immutable-id-v1"], run,
                               transition_type="ARGUMENT-DISPLAY")
        # set the id to include arg prefix
        receipt["id"] = "receipt:arg:" + receipt["id"].split(":")[-1]
        out.append(receipt)
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    with open(DIST / "data/receipts.jsonl", "w", encoding="utf-8") as fh:
        for r in out:
            fh.write(_json.dumps(r, ensure_ascii=False) + "\n")
    return len(out)


def build_corpus():
    """Embeddings-ready corpus: one JSONL, stable ids, gate labels, all layers.
    This file is the input to any embedding run (bge-m3/Qwen3-Embedding + rerank, per nibbanahelp relay)."""
    import json as _json
    recs = []
    for f in sorted((ROOT / "data/translations").glob("*.json")):
        for it in _json.loads(f.read_text()):
            recs.append({"id": f"{f.stem}:{it.get('chunk','')}", "work": f.stem, "ref": str(it.get("verses","")),
                "sa": it.get("sanskrit",""), "en": (it.get("l2") or it.get("l1") or ""),
                "en_gate": it.get("gate",""), "kind": "translation",
                "license": it.get("source_license",""), "source_file": it.get("source_file",""),
                "source_lines": it.get("source_lines"), "immutable_id": it.get("immutable_id",""),
                "checks": it.get("checks",{})})
    for f in sorted((PATALA / "data/published/ipvv").glob("pt-passage-*.json")):
        d = _json.loads(f.read_text())
        src = (d.get("source") or {}).get("text","") if isinstance(d.get("source"),dict) else ""
        recs.append({"id": f"ipvv:{d.get('chunk','')}", "work": "ipvv", "ref": d.get("chunk",""),
            "sa": src, "en": d.get("l2_text",""), "en_gate": "PUBLISHED", "kind": "ipvv-passage",
            "license": "CC BY-NC-SA 4.0", "source_file": "ipvv-vol" + str(d.get("vol",""))[2:3] + ".txt",
            "immutable_id": d.get("immutable_id","")})
        c1 = d.get("c1") or {}
        if isinstance(c1, dict) and c1.get("body"):
            recs.append({"id": f"ipvv-c1:{d.get('chunk','')}", "work": "ipvv", "ref": d.get("chunk",""),
                "sa": "", "en": c1.get("body",""), "en_gate": "PUBLISHED", "kind": "ipvv-c1",
                "license": "CC BY-NC-SA 4.0", "immutable_id": d.get("immutable_id","")})
    for f in sorted((ROOT / "data/essays").glob("ESSAY-*.md")):
        recs.append({"id": f"essay:{f.stem.lower().replace('essay-','')}", "work": "essays", "ref": f.stem,
            "sa": "", "en": f.read_text(encoding="utf-8", errors="replace"), "en_gate": "OWNER", "kind": "essay",
            "license": "CC BY-NC-SA 4.0"})
    for sub in ("ipvv", "tantraloka", "bodhapancadasika"):
        for f in sorted((ROOT / "data/pushing" / sub).glob("*.*")):
            if f.suffix not in (".md", ".txt"): continue
            recs.append({"id": f"pushing:{sub}/{f.name}", "work": "pushing", "ref": f"{sub}/{f.stem}",
                "sa": "", "en": f.read_text(encoding="utf-8", errors="replace")[:6000], "en_gate": "OWNER", "kind": "probe",
                "license": "CC BY-NC-SA 4.0"})
    for af in sorted((ROOT / "data/arguments").glob("*.json")):
        pkt = _json.loads(af.read_text())
        recs.append({"id": pkt.get("id", ""), "work": pkt.get("work_id", ""),
            "ref": pkt.get("source_passage", ""), "sa": pkt.get("sanskrit", ""),
            "en": pkt.get("conclusion", {}).get("text", "") + "\n" + "\n".join(p.get("text", "") for p in pkt.get("premises", [])),
            "en_gate": "MACHINE_DRAFT", "kind": "argument",
            "license": pkt.get("license", ""), "strength": pkt.get("strength", ""),
            "status": pkt.get("status", ""), "tension_id": pkt.get("tension_id"),
            "premises": len(pkt.get("premises", [])),
            "immutable_id": pkt.get("source_passage", "")})
    (DIST / "data/essay-links").mkdir(parents=True, exist_ok=True)
    if (ROOT / "data/essay-links/links.json").exists():
        shutil.copy(ROOT / "data/essay-links/links.json", DIST / "data/essay-links/links.json")
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    with open(DIST / "data/corpus.jsonl", "w", encoding="utf-8") as fh:
        for r in recs:
            fh.write(_json.dumps(r, ensure_ascii=False) + "\n")
    (DIST / "data/styles").mkdir(parents=True, exist_ok=True)
    for f in sorted((ROOT / "data/styles").glob("*.json")):
        shutil.copy(f, DIST / "data/styles" / f.name)
    return len(recs)

def render_asset(sub, title, kind, body_fn, filepat="*.*"):
    """Generic renderer for vendored research assets under site/data/<sub>/."""
    import json as _j
    src = ROOT / "data" / sub
    out = DIST / sub; out.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        (out / "index.html").write_text(TF(TMPL, title=title, h1=title,
            kicker=kind, sub="pending", sidenav=work_sidenav(""),
            body=f"<div class='panel missing'>no {sub} yet</div>"))
        return 0
    cards = []
    for f in sorted(src.glob(filepat)):
        if f.suffix == ".md":
            raw = f.read_text(encoding="utf-8", errors="replace")
            shutil.copy(f, out / f.name)
            first = next((l.lstrip("# ").strip() for l in raw.splitlines() if l.startswith("# ")), f.stem)
            cards.append(f'<div class="panel"><b>{esc(first)}</b><div class="sub">{esc(f.name)} · {len(raw.split())} words</div><div class="sub"><a href="/{sub}/{esc(f.name)}">read →</a></div></div>')
            (out / f.name).write_text(TF(TMPL, title=first, h1=esc(first), kicker=kind,
                sub=f"{len(raw.split())} words · vendored research asset",
                sidenav=work_sidenav(""),
                body=f'<div class="sub"><a href="/data/{sub}/{esc(f.name)}">source markdown →</a></div>' + md_lite(raw)
                + srclink(f"site/data/{sub}/{f.name}", "source lives here.")))
        elif f.suffix == ".json":
            shutil.copy(f, out / f.name)
            try:
                obj = _j.loads(f.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                obj = None
            if isinstance(obj, dict):
                title2 = obj.get("title") or obj.get("question") or obj.get("eo_id") or f.stem
                body = f'<pre style="white-space:pre-wrap;font-size:.85rem">{esc(_j.dumps(obj, ensure_ascii=False, indent=1)[:4000])}</pre>'
            elif isinstance(obj, list):
                title2 = f.stem
                body = f'<div class="sub">{len(obj)} records</div>'
                for o in obj[:8]:
                    if isinstance(o, dict):
                        t = o.get("title") or o.get("question") or o.get("claim") or o.get("question_id") or o.get("id") or "record"
                        body += f'<div class="panel"><b>{esc(str(t)[:90])}</b><div class="sub">{esc(str(o.get("status","")))} · {esc(str(o.get("resolution_level","")))} · {esc(str(o.get("falsifier_status","")))}</div></div>'
                body += f'<div class="sub"><a href="/data/{sub}/{esc(f.name)}">full JSON →</a></div>'
            else:
                title2 = f.stem
                body = f'<div class="sub"><a href="/data/{sub}/{esc(f.name)}">file →</a></div>'
            (out / (f.stem + ".html")).write_text(TF(TMPL, title=title2, h1=esc(str(title2)),
                kicker=kind, sub=f"vendored research asset · {f.name}",
                sidenav=work_sidenav(""),
                body=body + srclink(f"site/data/{sub}/{f.name}", "source lives here.")))
            cards.append(f'<div class="panel"><b>{esc(str(title2)[:90])}</b><div class="sub">{esc(f.name)}</div><div class="sub"><a href="/{sub}/{esc(f.stem)}.html">open →</a> · <a href="/data/{sub}/{esc(f.name)}">json →</a></div></div>')
    (out / "index.html").write_text(TF(TMPL, title=title, h1=title, kicker=kind,
        sub=f"{len(cards)} assets vendored from basecamp",
        sidenav=work_sidenav(""),
        body="".join(cards)))
    return len(cards)

def build_workbooks(): return render_asset("workbooks","Learning workbooks","Workbook",None,"*.md")
def build_contentions(): return render_asset("contentions","Contentions","Contention",None,"*.json")
def build_essay_objects():
    # eo-*/eo.json layout
    src = ROOT / "data/essay-objects"
    out = DIST / "essay-objects"; out.mkdir(parents=True, exist_ok=True)
    cards = []
    for d in sorted(src.glob("eo-*")):
        f = d / "eo.json"
        if not f.exists():
            continue
        obj = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        title = obj.get("title") or obj.get("eo_id") or d.name
        body = (f'<div class="panel"><b>{esc(title)}</b></div>'
                f'<div class="sub">status: {esc(obj.get("status",""))} · question: {esc((obj.get("question") or {}).get("question_id",""))}</div>'
                f'<pre style="white-space:pre-wrap;font-size:.85rem">{esc(json.dumps(obj, ensure_ascii=False, indent=1)[:6000])}</pre>'
                f'<div class="sub"><a href="/data/essay-objects/{esc(d.name)}/eo.json">source json →</a></div>'
                + srclink(f"site/data/essay-objects/{d.name}/eo.json", "source lives here."))
        (out / (d.name + ".html")).write_text(TF(TMPL, title=title, h1=esc(str(title)),
            kicker="Enquiry", sub=f"guided enquiry · {d.name}",
            sidenav=work_sidenav(""), body=body))
        cards.append(f'<div class="panel"><b>{esc(str(title)[:90])}</b><div class="sub">{esc(d.name)}</div><div class="sub"><a href="/essay-objects/{esc(d.name)}.html">open →</a></div></div>')
    (out / "index.html").write_text(TF(TMPL, title="Essay objects", h1="Essay objects", kicker="Enquiry",
        sub=f"{len(cards)} guided enquiries", sidenav=work_sidenav(""),
        body="".join(cards)))
    return len(cards)

def build_ochema_methods():
    src = ROOT / "data/ochema-methods"
    out = DIST / "ochema-methods"; out.mkdir(parents=True, exist_ok=True)
    cards = []
    for f in sorted(src.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix == ".md":
            shutil.copy(f, out / f.name)
            raw = f.read_text(encoding="utf-8", errors="replace")
            first = next((l.lstrip("# ").strip() for l in raw.splitlines() if l.startswith("# ")), f.stem)
            (out / (f.stem + ".html")).write_text(TF(TMPL, title=first, h1=esc(first), kicker="Method",
                sub=f"{len(raw.split())} words · vendored method",
                sidenav=work_sidenav(""),
                body=f'<div class="sub"><a href="/data/ochema-methods/{esc(f.name)}">source markdown →</a></div>' + md_lite(raw)
                + srclink(f"site/data/ochema-methods/{f.name}", "source lives here.")))
            cards.append(f'<div class="panel"><b>{esc(first)}</b><div class="sub">{esc(f.name)}</div><div class="sub"><a href="/ochema-methods/{esc(f.stem)}.html">open →</a></div></div>')
        elif f.suffix in (".json", ".yaml", ".yml"):
            shutil.copy(f, out / f.name)
            try:
                obj = json.loads(f.read_text(encoding="utf-8", errors="replace"))
                body = f'<pre style="white-space:pre-wrap;font-size:.85rem">{esc(json.dumps(obj, ensure_ascii=False, indent=1)[:6000])}</pre>'
            except Exception:
                body = f'<div class="sub"><a href="/data/ochema-methods/{esc(f.name)}">file →</a></div>'
            (out / (f.stem + ".html")).write_text(TF(TMPL, title=f.stem, h1=esc(f.stem), kicker="Method",
                sub=f"vendored method asset · {f.name}",
                sidenav=work_sidenav(""),
                body=body + srclink(f"site/data/ochema-methods/{f.name}", "source lives here.")))
            cards.append(f'<div class="panel"><b>{esc(f.stem)}</b><div class="sub">{esc(f.name)}</div><div class="sub"><a href="/ochema-methods/{esc(f.stem)}.html">open →</a></div></div>')
    (out / "index.html").write_text(TF(TMPL, title="Ochema methods", h1="Ochema methods", kicker="Method",
        sub=f"{len(cards)} method assets", sidenav=work_sidenav(""), body="".join(cards)))
    return len(cards)
def build_source_metaphysics(): return render_asset("source-metaphysics","Source metaphysics","State-of-play",None,"*.json")
def build_information_packets(): return render_asset("information-packets","Information packets","Packet",None,"*")
def build_ochema_methods(): return render_asset("ochema-methods","Ochema methods","Method",None,"*")
def build_philosophers(): return render_asset("philosophers","Philosophers","Research object",None,"*")

def render_text_assets(sub, title, kind, filepat="*.md"):
    src = ROOT / "data" / sub
    out = DIST / sub; out.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        (out / "index.html").write_text(TF(TMPL, title=title, h1=title, kicker=kind,
            sub="pending", sidenav=work_sidenav(""),
            body=f"<div class='panel missing'>no {sub} yet</div>"))
        return 0
    cards = []
    for f in sorted(src.glob(filepat)):
        if f.suffix not in (".md", ".txt"):
            continue
        shutil.copy(f, out / f.name)
        raw = f.read_text(encoding="utf-8", errors="replace")
        first = next((l.lstrip("# ").strip() for l in raw.splitlines() if l.startswith("# ")), f.stem)
        (out / (f.stem + ".html")).write_text(TF(TMPL, title=first, h1=esc(first), kicker=kind,
            sub=f"{len(raw.split())} words · vendored research asset",
            sidenav=work_sidenav(""),
            body=f'<div class="sub"><a href="/data/{sub}/{esc(f.name)}">source →</a></div>' + md_lite(raw)
            + srclink(f"site/data/{sub}/{f.name}", "source lives here.")))
        cards.append(f'<div class="panel"><b>{esc(first)}</b><div class="sub">{esc(f.name)}</div><div class="sub"><a href="/{sub}/{esc(f.stem)}.html">open →</a></div></div>')
    (out / "index.html").write_text(TF(TMPL, title=title, h1=title, kicker=kind,
        sub=f"{len(cards)} assets", sidenav=work_sidenav(""), body="".join(cards)))
    return len(cards)

def build_ratier_chapters(): return render_text_assets("ratie-chapters","Ratie chapters","Chapter","*.md")
def build_torella_volume(): return render_text_assets("torella-volume","Torella volume","Chapter","*.txt")
def build_recognition_framework(): return render_text_assets("recognition-framework","Recognition framework","Framework","*.md")
def render_text_assets2(sub, title, kind, filepat="*"):
    src = ROOT / "data" / sub
    out = DIST / sub; out.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        (out / "index.html").write_text(TF(TMPL, title=title, h1=title, kicker=kind,
            sub="pending", sidenav=work_sidenav(""),
            body=f"<div class='panel missing'>no {sub} yet</div>"))
        return 0
    cards = []
    for f in sorted(src.glob(filepat)):
        if not f.is_file():
            continue
        if f.suffix in (".md", ".txt"):
            shutil.copy(f, out / f.name)
            raw = f.read_text(encoding="utf-8", errors="replace")
            first = next((l.lstrip("# ").strip() for l in raw.splitlines() if l.startswith("# ")), f.stem)
            (out / (f.stem + ".html")).write_text(TF(TMPL, title=first, h1=esc(first), kicker=kind,
                sub=f"{len(raw.split())} words · vendored research asset",
                sidenav=work_sidenav(""),
                body=f'<div class="sub"><a href="/data/{sub}/{esc(f.name)}">source →</a></div>' + md_lite(raw)
                + srclink(f"site/data/{sub}/{f.name}", "source lives here.")))
            cards.append(f'<div class="panel"><b>{esc(first)}</b><div class="sub">{esc(f.name)}</div><div class="sub"><a href="/{sub}/{esc(f.stem)}.html">open →</a></div></div>')
        elif f.suffix in (".json", ".yaml", ".yml"):
            shutil.copy(f, out / f.name)
            try:
                obj = json.loads(f.read_text(encoding="utf-8", errors="replace"))
                body = f'<pre style="white-space:pre-wrap;font-size:.85rem">{esc(json.dumps(obj, ensure_ascii=False, indent=1)[:4000])}</pre>'
            except Exception:
                body = f'<div class="sub"><a href="/data/{sub}/{esc(f.name)}">file →</a></div>'
            (out / (f.stem + ".html")).write_text(TF(TMPL, title=f.stem, h1=esc(f.stem), kicker=kind,
                sub=f"vendored asset · {f.name}", sidenav=work_sidenav(""),
                body=body + srclink(f"site/data/{sub}/{f.name}", "source lives here.")))
            cards.append(f'<div class="panel"><b>{esc(f.stem)}</b><div class="sub">{esc(f.name)}</div><div class="sub"><a href="/{sub}/{esc(f.stem)}.html">open →</a></div></div>')
    (out / "index.html").write_text(TF(TMPL, title=title, h1=title, kicker=kind,
        sub=f"{len(cards)} assets", sidenav=work_sidenav(""), body="".join(cards)))
    return len(cards)

def build_r2_audio_transcripts(): return render_text_assets2("r2-audio-transcripts","R2 audio transcripts","Transcript","*")
def parse_argmap(path):
    """Parse an IPVV argmap markdown into structured fields. Returns None if unparseable."""
    import re as _re
    raw = open(path, encoding="utf-8", errors="replace").read()
    # title
    title = path.stem.replace("pilot_", "").replace("_ARGUMENT_MAP", "").replace("_", " ")
    m = _re.search(r'^# (.+)$', raw, _re.M)
    if m: title = m.group(1).strip()
    # question
    qm = _re.search(r'\*\*The question:\*\*\s*(.+?)(?=\n\n|\n##|\n\*\*)', raw, _re.S)
    question = qm.group(1).strip().replace("\n", " ") if qm else ""
    # what is at issue (thesis)
    issue = ""
    im = _re.search(r'## 1\. What is at issue\s*\n(.+?)(?=## 2)', raw, _re.S)
    if im: issue = im.group(1).strip()[:1500]
    # argument section
    argm = _re.search(r'## 2\. The argument.+?\n(.+?)(?=## 3)', raw, _re.S)
    argument = argm.group(1).strip()[:3000] if argm else ""
    # unresolved
    unm = _re.search(r'## 3\. Unresolved.+?\n(.+?)(?=## 4|\Z)', raw, _re.S)
    unresolved = unm.group(1).strip()[:1000] if unm else ""
    # premises: bolded sub-headers in the argument section
    premises = []
    for pm in _re.finditer(r'\*\*(.+?)(?:\s*\(lines? .+?\))?:\*\*\s*\n(.+?)(?=\n\*\*|\n##|\Z)', argument, _re.S):
        premises.append({"label": pm.group(1).strip(), "text": pm.group(2).strip()[:800]})
    if not premises and argument:
        # fallback: split by double newline
        for chunk in argument.split("\n\n"):
            chunk = chunk.strip()
            if len(chunk) > 80:
                premises.append({"label": "", "text": chunk[:800]})
    return {"title": title, "question": question, "issue": issue,
            "premises": premises, "argument": argument, "unresolved": unresolved}

def build_arguments():
    """ArgumentTruthPackets from argmaps + L2 text. IPVV uses argmaps;
    non-IPVV stotra works derive from L2 prose. All MACHINE_DRAFT."""
    import json as _json, re as _re
    src = ROOT / "data/arguments"; src.mkdir(parents=True, exist_ok=True)
    out = DIST / "arguments"; out.mkdir(parents=True, exist_ok=True)
    (DIST / "data" / "arguments").mkdir(parents=True, exist_ok=True)
    for _af in src.glob("*.json"):
        shutil.copy(_af, DIST / "data" / "arguments" / _af.name)
    # clear old
    for old in src.glob("*.json"):
        old.unlink()
    for old in out.glob("*.html"):
        old.unlink()
    recs = []
    # tension map from pushing-ipvv files
    tension_map = {}
    for pf in (ROOT / "data/pushing/ipvv").glob("*.md"):
        raw = pf.read_text(encoding="utf-8", errors="replace")
        for m in __import__("re").finditer(r'V[123][A-Z](?:-[A-Za-z0-9]+)?', raw):
            key = m.group(0).lower().replace("-", "")
            tension_map.setdefault(key, pf.stem)
    # --- IPVV (argmaps) ---
    pmap = {"chunkA":"pilot_V1A","chunkB":"pilot_V1B","chunkC":"pilot_V1C","chunkD":"pilot_V1D",
        "chunkE":"pilot_V1E","chunkF":"pilot_V1F","chunkG":"pilot_V1G","chunkH":"pilot_V1H",
        "chunkI":"pilot_V1I","chunkJ":"pilot_V1J","chunkK":"pilot_V1K","chunkL":"pilot_V1L",
        "chunkM":"pilot_V1M","chunkN":"pilot_V1N","chunkV2-A":"pilot_V2A","chunkV2-B":"pilot_V2B",
        "chunkV2-C":"pilot_V2C","chunkV2-D":"pilot_V2D","chunkV2-E":"pilot_V2E","chunkV2-F":"pilot_V2F",
        "chunkV2-G":"pilot_V2G","chunkV2-H":"pilot_V2H","chunkV2-I":"pilot_V2I","chunkV2-J":"pilot_V2J",
        "chunkV2-K":"pilot_V2K","chunkV2-L":"pilot_V2L","chunkV2-M":"pilot_V2M","chunkV2-N":"pilot_V2N",
        "chunkV2-O":"pilot_V2O","chunkV2-P":"pilot_V2P","chunkV2-Q":"pilot_V2Q","chunkV2-R":"pilot_V2R",
        "chunkV2-S":"pilot_V2S","chunkV3-A":"pilot_V3A","chunkV3-C":"pilot_V3C","chunkV3-D":"pilot_V3D",
        "chunkV3-E":"pilot_V3E","chunkV3-F":"pilot_V3F","chunkV3-G":"pilot_V3G","chunkV3-H":"pilot_V3H",
        "chunkV3-I":"pilot_V3I","chunkV3-J":"pilot_V3J","chunkV3-K":"pilot_V3K","chunkV3-L":"pilot_V3L",
        "chunkV3-M":"pilot_V3M","chunkV3-N":"pilot_V3N","chunkV3-O":"pilot_V3O","chunkV3-P":"pilot_V3P"}
    pmap_keys_sorted = sorted(pmap.keys(), key=len, reverse=True)
    for d in sorted((PATALA / "data/published/ipvv").glob("pt-passage-*.json")):
        rec = _json.loads(d.read_text())
        chunk = rec.get("chunk", "").replace(".md", "")
        pp = None
        for pk in pmap_keys_sorted:
            if chunk.startswith(pk):
                pp = pmap[pk]
                break
        if chunk.startswith("chunkV3-B"):
            pp = "pilot_V3B"
        am_path = ROOT / "data/ipvv/argmaps" / f"{pp}_ARGUMENT_MAP.md"
        if not am_path.exists():
            continue
        am = parse_argmap(am_path)
        tid = ""
        chunkkey = chunk.lower().replace("-", "").replace("chunk", "")
        for tk, tv in tension_map.items():
            if tk in chunkkey:
                tid = tv
                break
        packet = {
            "id": f"pt:argument:ipvv:{chunk}",
            "work_id": "isvarapratyabhijnavivrtivimarsini",
            "passage_id": rec.get("immutable_id", ""),
            "title": am["title"],
            "kind": "entailment",
            "question": am["question"],
            "issue": am["issue"],
            "premises": [{"text": p["text"], "label": p["label"], "passage_id": rec.get("immutable_id", "")}
                         for p in am["premises"]],
            "inference": "reconstructed from argmap",
            "conclusion": {"text": am["question"], "passage_id": rec.get("immutable_id", "")},
            "unresolved": am["unresolved"],
            "argument_text": am["argument"],
            "tension_id": tid or None,
            "strength": "MACHINE_DRAFT",
            "strength_basis": "extracted from argmap; no human review; premises resolve to passage; no surviving prosecution tested",
            "status": "MACHINE_DRAFT",
            "source_passage": rec.get("immutable_id", ""),
            "sanskrit": (rec.get("source") or {}).get("text", "") if isinstance(rec.get("source"), dict) else "",
            "license": "CC BY-NC-SA 4.0",
        }
        (src / f"ipvv-{chunk}.json").write_text(_json.dumps(packet, ensure_ascii=False, indent=1))
        recs.append(packet)
    # --- Non-IPVV works (from L2 text) ---
    # tension map for non-ipvv works (none yet)
    for tf in sorted((ROOT / "data/translations").glob("*.json")):
        work = tf.stem
        if work == "ipvv" or work.startswith("tantraloka"):
            continue
        items = _json.loads(tf.read_text())
        for it in items:
            if it.get("gate") != "PASS":
                continue
            chunk = it.get("chunk", "?")
            l2 = it.get("l2", "") or it.get("l1", "")
            # extract question from L2 (first sentence or whole)
            first_line = l2.split("\n")[0].strip() if l2 else ""
            # strip markdown headers
            first_line = _re.sub(r'^#+\s*', '', first_line).strip()
            title = f"{work} — {chunk}"
            sa = it.get("sanskrit", "")
            packet = {
                "id": f"pt:argument:{work}:{chunk}",
                "work_id": work,
                "passage_id": f"{work}:{chunk}",
                "title": title,
                "kind": "entailment",
                "question": first_line[:500] if first_line else f"What does {work} {chunk} establish?",
                "issue": f"Derived from L2 text (no argmap). {l2[:500]}",
                "premises": [{"text": sa, "label": "Sanskrit source", "passage_id": f"{work}:{chunk}"}],
                "inference": "derived from L2 prose (no argmap reconstruction)",
                "conclusion": {"text": first_line[:500] if first_line else l2[:300],
                               "passage_id": f"{work}:{chunk}"},
                "unresolved": "",
                "argument_text": l2,
                "tension_id": None,
                "strength": "MACHINE_DRAFT",
                "strength_basis": "derived from L2 prose (no argmap reconstruction); premises = Sanskrit source; no human review",
                "status": "MACHINE_DRAFT",
                "source_passage": f"{work}:{chunk}",
                "sanskrit": sa,
                "license": it.get("source_license", "CC BY-NC-SA 4.0"),
            }
            (src / f"{work}-{chunk}.json").write_text(_json.dumps(packet, ensure_ascii=False, indent=1))
            recs.append(packet)
    # --- tantraloka ahnikas with PASS ---
    for tf in sorted((ROOT / "data/translations").glob("tantraloka-*.json")):
        work = tf.stem
        items = _json.loads(tf.read_text())
        for it in items:
            if it.get("gate") != "PASS":
                continue
            chunk = it.get("chunk", "?")
            l2 = it.get("l2", "") or it.get("l1", "")
            first_line = l2.split("\n")[0].strip() if l2 else ""
            first_line = _re.sub(r'^#+\s*', '', first_line).strip()
            title = f"{work} — {chunk}"
            sa = it.get("sanskrit", "")
            packet = {
                "id": f"pt:argument:{work}:{chunk}",
                "work_id": work,
                "passage_id": f"{work}:{chunk}",
                "title": title,
                "kind": "entailment",
                "question": first_line[:500] if first_line else f"What does {work} {chunk} establish?",
                "issue": f"Derived from L2 text (no argmap). {l2[:500]}",
                "premises": [{"text": sa, "label": "Sanskrit source", "passage_id": f"{work}:{chunk}"}],
                "inference": "derived from L2 prose (no argmap reconstruction)",
                "conclusion": {"text": first_line[:500] if first_line else l2[:300],
                               "passage_id": f"{work}:{chunk}"},
                "unresolved": "",
                "argument_text": l2,
                "tension_id": None,
                "strength": "MACHINE_DRAFT",
                "strength_basis": "derived from L2 prose (no argmap reconstruction); premises = Sanskrit source; no human review",
                "status": "MACHINE_DRAFT",
                "source_passage": f"{work}:{chunk}",
                "sanskrit": sa,
                "license": it.get("source_license", "CC BY-NC-SA 4.0"),
            }
            (src / f"{work}-{chunk}.json").write_text(_json.dumps(packet, ensure_ascii=False, indent=1))
            recs.append(packet)
    # index
    (out / "index.html").write_text(TF(TMPL, title="Arguments", h1="Arguments",
        kicker="Argument truth-packets", sub=f"{len(recs)} packets — conclusion → premises → passage → Sanskrit",
        sidenav=work_sidenav(""), body="<div class='idx'>"
        + "".join(f'<a href="/arguments/{p["id"].split(":")[-1]}.html"><b>{esc(p["title"][:70])}</b> — {esc(p["strength"])}</a>' for p in recs)
        + "</div>" + srclink("site/data/arguments/", "packets live here.")))
    # per-packet pages
    for pkt in recs:
        pid = pkt["id"].split(":")[-1]
        prem = "".join(f'<div class="panel"><b>{esc(p["label"])}</b><div class="en">{esc(p["text"][:1200])}</div></div>' for p in pkt["premises"])
        body = (f'<div class="panel"><b>Question.</b> {esc(pkt["question"])}</div>'
                + f'<div class="panel"><b>Issue.</b> {esc(pkt["issue"][:1200])}</div>'
                + f'<h3>Premises</h3>{prem}'
                + f'<div class="panel"><b>Unresolved.</b> {esc(pkt["unresolved"][:600])}</div>'
                + (f'<div class="sub">Tension: {esc(pkt["tension_id"])}</div>' if pkt["tension_id"] else "")
                + arg_essay_links(pid)
                + f'<div class="sub">Strength: {esc(pkt["strength"])} · Status: {esc(pkt["status"])} · <a href="/data/arguments/{esc(pid)}.json">packet JSON</a></div>'
                + srclink("site/data/arguments/" + pid + ".json", "packet lives here."))
        (out / f"{pid}.html").write_text(TF(TMPL, title=pkt["title"], h1=esc(pkt["title"]),
            kicker="Argument", sub=f'{pkt["strength"]} · {len(pkt["premises"])} premises',
            sidenav=work_sidenav(""), body=body))
    return len(recs)


def build_stylelab():
    out = DIST / "stylelab"; out.mkdir(parents=True, exist_ok=True)
    body = """
    <div class="panel">A3S-style instant preview: paste 3-5 exemplar translations in your target style,
    then a source passage. The model rewrites in that style in seconds — no training, no adapter.
    Training-free aspect-aware steering via prompt conditioning (the A3S pattern, Sep 2026).</div>
    <div class="panel">
      <b>Exemplars (one per line, or separated by ---)</b>
      <textarea id="ex" rows="6" style="width:100%;padding:.5rem;border:1px solid var(--line);border-radius:.4rem;font-family:var(--serif);font-size:.9rem" placeholder="Bhairava-Lord, refuge of the helpless — by mind become Yours, in heart I venerate."></textarea>
      <b style="display:block;margin-top:.6rem">Source passage (Sanskrit or English)</b>
      <textarea id="src" rows="3" style="width:100%;padding:.5rem;border:1px solid var(--line);border-radius:.4rem;font-family:var(--serif);font-size:.9rem" placeholder="tvanmayacittatayā hṛdi vande"></textarea>
      <button onclick="preview()" style="margin-top:.6rem;padding:.5rem 1rem;background:var(--ink);color:var(--paper);border:0;border-radius:.4rem;cursor:pointer;font-size:.9rem">Preview style →</button>
      <div id="preview" style="margin-top:.8rem;padding:.8rem;border:1px solid var(--line);border-radius:.4rem;min-height:60px;background:var(--card)"></div>
    </div>
    <script>
    function preview(){
      var ex=document.getElementById('ex').value.trim();
      var src=document.getElementById('src').value.trim();
      if(!ex||!src){alert('Enter exemplars and source');return}
      var pv=document.getElementById('preview');pv.innerHTML='<i>Generating...</i>';
      fetch(window.API+'/api/style/preview',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({exemplars:ex.split('---').map(s=>s.trim()).filter(Boolean),source:src})})
        .then(r=>r.json()).then(d=>{pv.innerHTML=d.styled||d.error||'No output'})
        .catch(e=>{pv.innerHTML='Error: '+e.message});
    }
    </script>
    """
    (out / "index.html").write_text(TF(TMPL, title="Style lab", h1="Style lab",
        kicker="A3S preview", sub="instant style transfer — paste exemplars, see the style in seconds",
        sidenav=work_sidenav(""), body=body,
        recitejs="", chatjs="", varjs=""))
    return 1

def build_app():
    """Lab-pattern SPA shell (white, single page, zero reloads) + app-ready JSON indexes."""
    import json as _j, shutil as _sh
    src = ROOT / "app"
    if not src.exists():
        return 0
    dest = DIST / "app"; dest.mkdir(parents=True, exist_ok=True)
    for f in src.glob("*.*"):
        _sh.copy(f, dest / f.name)
    works = sorted(f.stem for f in (ROOT / "data/translations").glob("*.json"))
    (DIST / "data" / "translations.json").write_text(_j.dumps(works, ensure_ascii=False))
    pract = []
    for f in sorted((ROOT / "data/practices").glob("*.json")):
        try:
            d = _j.loads(f.read_text(encoding="utf-8"))
            pract.append({"id": d.get("id", f.stem), "title": d.get("name", f.stem),
                          "kind": d.get("kind", ""), "summary": (d.get("summary", "") or "")[:200]})
        except Exception:
            pass
    (DIST / "data" / "practices.json").write_text(_j.dumps(pract, ensure_ascii=False))
    return len(works)

def build_llms_txt():
    """Generate llm.txt (agent-native discovery) + per-work llms.txt."""
    import json as _json
    out = DIST; out.mkdir(parents=True, exist_ok=True)
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    # Root llms.txt
    works = sorted(set(f.stem for f in (ROOT / "data/translations").glob("*.json")))
    lines = [
        "# svatantrya — LLM Discovery File",
        "",
        "> Machine-readable index. All content is freely accessible.",
        "> Source: https://github.com/prx0r/ipvv | Live: https://ipvv-a8u.pages.dev",
        "",
        "## What this site contains",
        "",
        "A complete, auditable translation and commentary pipeline for Trika Śaivism:",
        "- Sanskrit roots (vendored, licensed, CC BY-NC-SA)",
        "- Translations (T1/L1/L2, gate-checked, source-traceable)",
        "- Argument truth-packets (conclusion → premises → passage → Sanskrit)",
        "- C1 passage commentaries (local hermeneutics)",
        "- Themes (machine-proposed clusters, adjudication pending)",
        "- Essays (22 recognition essays, 17 peer-reviewed)",
        "- Scholars (36 bios + bibliographies)",
        "- Recitation (studio chants + browser-voice readout)",
        "- Pushing probes (73 Q→GEM sessions)",
        "- Contentions (16 falsifiable claims with source spans)",
        "",
        "## Data endpoints (machine-readable)",
        "",
        "- /data/corpus.jsonl — 691 records (translations, passages, C1s, essays, arguments, probes)",
        "- /data/receipts.jsonl — 546 audit receipts (qprivately kernel, tamper-checked)",
        "- /data/vectors.json — 691 embeddings (bge-m3, contextual retrieval)",
        "- /data/translations/{work}.json — per-work translation records",
        "- /data/arguments/{id}.json — per-chunk argument truth-packets",
        "- /data/scholars.json — 36 scholar bios + bibliographies",
        "- /data/glossary.json — 100 concepts with occurrences",
        "- /data/authors/{id}.json — 15 master bios + works",
        "- /data/sections.json — taxonomy (Masters vs Modern)",
        "- /data/read_alongside.json — scholar ↔ master cross-links",
        "- /data/essay-links/links.json — essay ↔ argument links",
        "- /data/styles/{id}.json — style cards for translation rendering",
        "",
        "## Per-work data",
        "",
    ]
    for w in works:
        lines.append(f"- /translations/{w}.html — {w} (translation + gate status)")
        lines.append(f"  data: /data/translations/{w}.json")
    lines += [
        "",
        "## API (Cloudflare Worker)",
        "",
        "- POST /api/chat/{work} — RAG chat (per-text or multi-text via comma-separated works)",
        "- POST /api/chat/{work1,work2} — multi-text chat",
        "- GET /api/variants/{work}/{chunk} — list saved variants",
        "- POST /api/variants — save a variant",
        "- POST /api/style/preview — A3S instant style preview",
        "- GET /api/questions/{work} — list stored questions",
        "- GET /api/themes/decisions — list theme adjudication decisions",
        "",
        "## Gate system",
        "",
        "Every translation chunk carries a gate status:",
        "- PASS: English shown (machine-proposed, needs human review)",
        "- BLOCKED: Sanskrit shown, English withheld (fail-closed)",
        "- PUBLISHED: full display (IPVV passages)",
        "",
        "Every chunk has a receipt in /data/receipts.jsonl with gate verdicts,",
        "evidence hashes, source file/line, license, model, and date.",
        "",
        "## License",
        "",
        "Sanskrit roots: CC BY-NC-SA 4.0 (GRETIL/Muktabodha).",
        "Our translations/essays/arguments: CC BY-NC-SA 4.0.",
        "Commercial use requires re-licensing.",
        "",
        "## MCP server",
        "",
        "MCP endpoint: https://ipvv-api.tradesprior.workers.dev/mcp",
        "Tools: get_passage, get_translation, get_argument, search, get_scholar,",
        "       get_work, list_works, get_themes, get_receipts, chat",
        "",
    ]
    (out / "llms.txt").write_text("\n".join(lines))

    # Per-work llms.txt
    for w in works:
        items = _json.loads((ROOT / "data/translations" / f"{w}.json").read_text())
        n_pass = sum(1 for i in items if i.get("gate") == "PASS")
        wlines = [
            f"# {w} — LLM Discovery",
            "",
            f"Work: {w}",
            f"Passages: {len(items)} ({n_pass} PASS, {len(items)-n_pass} BLOCKED)",
            f"Data: /data/translations/{w}.json",
            f"Page: /translations/{w}.html",
            "",
            "## Chunks",
            "",
        ]
        for it in items:
            g = it.get("gate", "")
            wlines.append(f"- {it.get('chunk','')} (verses {it.get('verses','')}) [{g}]")
            if g == "PASS":
                wlines.append(f"  L1: {it.get('l1','')[:120]}")
                wlines.append(f"  L2: {it.get('l2','')[:120]}")
        (out / "llms" / w).mkdir(parents=True, exist_ok=True)
        (out / "llms" / w / "llms.txt").write_text("\n".join(wlines))
    print(f"llms.txt generated: root + {len(works)} per-work")
    return 1

def build_screen():
    out = DIST / "screen"; out.mkdir(parents=True, exist_ok=True)
    body = """
    <div class="panel">Over-the-shoulder screen analysis: capture your screen, ask a question,
    get a spoken answer. Uses Qwen3.8-Omni-Flash vision (1M context, thinking mode).</div>
    <div class="panel">
      <button id="capture" style="padding:.5rem 1rem;background:var(--ink);color:var(--paper);border:0;border-radius:.4rem;cursor:pointer;font-size:.9rem">Capture screen →</button>
      <button id="speak" style="padding:.5rem 1rem;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:.4rem;cursor:pointer;font-size:.9rem;margin-left:.5rem">Speak answer</button>
      <div id="preview" style="margin-top:.8rem;max-width:100%;border:1px solid var(--line);border-radius:.4rem;overflow:hidden"></div>
      <textarea id="q" rows="2" style="width:100%;padding:.5rem;border:1px solid var(--line);border-radius:.4rem;font-family:var(--serif);font-size:.9rem;margin-top:.6rem" placeholder="What do you see? / What does this error mean? / Where do I click?"></textarea>
      <button id="analyze" style="margin-top:.5rem;padding:.5rem 1rem;background:var(--ink);color:var(--paper);border:0;border-radius:.4rem;cursor:pointer;font-size:.9rem">Analyze →</button>
      <div id="result" style="margin-top:.8rem;padding:.8rem;border:1px solid var(--line);border-radius:.4rem;min-height:60px;background:var(--card);white-space:pre-wrap"></div>
    </div>
    <script>
    var imgData=null;
    document.getElementById('capture').onclick=async function(){
      try {
        var stream=await navigator.mediaDevices.getDisplayMedia({video:true});
        var video=document.createElement('video');
        video.srcObject=stream;video.play();
        await new Promise(r=>setTimeout(r,500));
        var canvas=document.createElement('canvas');
        canvas.width=video.videoWidth;canvas.height=video.videoHeight;
        canvas.getContext('2d').drawImage(video,0,0);
        imgData=canvas.toDataURL('image/jpeg',0.8).split(',')[1];
        var preview=document.getElementById('preview');
        preview.innerHTML='<img src="data:image/jpeg;base64,'+imgData+'" style="max-width:100%;display:block"/>';
        stream.getTracks().forEach(t=>t.stop());
      } catch(e){alert('Capture failed: '+e.message)}
    };
    document.getElementById('analyze').onclick=async function(){
      if(!imgData){alert('Capture screen first');return}
      var q=document.getElementById('q').value.trim()||'Describe what you see and explain any errors.';
      var res=document.getElementById('result');res.innerHTML='<i>Analyzing...</i>';
      var r=await fetch(window.API+'/api/screen',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image:imgData,question:q})});
      var d=await r.json();
      res.innerHTML=d.reply||d.error||'No output';
      window._lastReply=d.reply||'';
    };
    document.getElementById('speak').onclick=function(){
      if(window._lastReply){var u=new SpeechSynthesisUtterance(window._lastReply);u.rate=0.95;speechSynthesis.speak(u)}
    };
    </script>
    """
    (out / "index.html").write_text(TF(TMPL, title="Screen", h1="Screen analysis",
        kicker="Over-the-shoulder", sub="capture your screen, ask a question, get a spoken answer",
        sidenav=work_sidenav(""), body=body,
        recitejs="", chatjs="", varjs=""))
    return 1

def build_meditate():
    import json as _json
    out = DIST / "meditate"; out.mkdir(parents=True, exist_ok=True)
    vbt = _json.load(open(VOL / "source-library/tantra/lakshmanjoo/vb_lakshmanjoo.json"))
    vs = vbt.get("verses", [])[:145]
    cards = []
    for v in vs:
        n = v.get("number")
        skt = (v.get("sanskrit", "") or "")[:120]
        en = (v.get("english", "") or "")[:200]
        cards.append(f'<div class="panel"><b>Dharana {n}</b><div class="deva" style="font-size:1.1rem;margin:.4rem 0">{esc(skt)}</div><div class="en" style="font-size:.85rem">{esc(en)}</div><div style="margin-top:.5rem"><button onclick="startMed({n})" style="padding:.3rem .7rem;border:1px solid var(--line);border-radius:.4rem;background:var(--card);cursor:pointer;font-size:.8rem">Practice</button></div></div>')
    med_js = "<script>function startMed(n){alert('Meditation ' + n + ' starting. Close your eyes and breathe.')}function stopMed(){}</script>"
    (out / "index.html").write_text(TF(TMPL, title="Meditation", h1="Meditation",
        kicker="Practice", sub="Vijñānabhairava dhāraṇās as guided practices",
        sidenav=work_sidenav(""), body='<div class="idx">' + "".join(cards) + "</div>" + med_js
        + srclink("https://github.com/prx0r/kashaudio", "chants render here as kashaudio reaches each work."),
        recitejs="", chatjs="", varjs=""))
    return len(vs)

def build_vbt_map():
    """Interactive VBT dhāraṇā map — 112 techniques by upāya category."""
    import json as _json, html as _html
    esc = _html.escape
    vm = _json.loads((ROOT / "data/vbt_map.json").read_text())
    out = DIST / "vbt-map"; out.mkdir(parents=True, exist_ok=True)
    cards = []
    for cat in vm["categories"]:
        cat_name = cat["name"]
        cat_display = cat_name.split(":", 1)[1].strip() if ":" in cat_name else cat_name
        cards.append(f'<h3 style="margin-top:1.5rem">{esc(cat_display)}</h3>')
        for d in cat["dharanas"]:
            dh = d["dh"]
            verse = d["verse"]
            technique = d["technique"]
            trains = d["trains"]
            coord = d["coord"]
            vbt_link = f'/vbt/v{verse}.html' if verse.isdigit() and int(verse) <= 145 else '#'
            cards.append(f'<div class="panel" style="margin:.3rem 0"><div style="display:flex;justify-content:space-between;align-items:start"><div><b>Dhāraṇā {dh}</b> <span class="sub">verse {verse}</span></div><a href="{vbt_link}" style="font-size:.8rem">VBT {verse} →</a></div><div class="en" style="margin-top:.3rem;font-size:.9rem">{esc(technique)}</div><div class="sub" style="margin-top:.2rem">Trains: {esc(trains)}</div><div class="sub">Tāṇtraloka: {esc(coord)}</div></div>')
    upaya_rows = "".join(f'<tr><td><b>{esc(u["name"])}</b></td><td>{u["count"]}</td><td>{esc(u["approach"])}</td><td>{esc(u["tattva"])}</td><td>{esc(u["grace"])}</td></tr>' for u in vm["upayas"])
    upaya_table = f'<table style="width:100%;border-collapse:collapse;font-size:.85rem;margin:1rem 0"><tr style="border-bottom:2px solid var(--ink)"><th style="text-align:left;padding:.4rem">Upāya</th><th style="text-align:left;padding:.4rem">Count</th><th style="text-align:left;padding:.4rem">Approach</th><th style="text-align:left;padding:.4rem">Tattva Range</th><th style="text-align:left;padding:.4rem">Grace</th></tr>{upaya_rows}</table>'
    body = f'<div class="panel"><b>The path:</b> You don\u2019t do all 112. Find the upāya that matches your grace level, pick 2-3 dharanas, master them. When they stop working (the technique becomes the obstacle), move to a higher upaya. — Swami Lakshmanjoo</div>{upaya_table}<h2>112 Dharanas by Category</h2><div class="idx">{"".join(cards)}</div>'
    (out / "index.html").write_text(TF(TMPL, title="VBT Dharana Map", h1="VBT Dharana Map",
        kicker="Interactive", sub="112 techniques by upāya category — each linked to its VBT verse and Tantrāloka coordinate",
        sidenav=work_sidenav(""), body=body,
        recitejs="", chatjs="", varjs=""))
    return len(vm["categories"])

def build_practices():
    """Interactive practice player — VBT dhāraṇās, anapanasati, Ajahn Lee with voice cues."""
    import json as _json
    body_data = _json.loads(open('/tmp/practices_body.json').read())
    out = DIST / "practices"; out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(TF(TMPL, title="Practices", h1="Practices",
        kicker="Interactive", sub="VBT dhāraṇās, ānāpānasati, Ajahn Lee — voice cues, timed steps, audio tones",
        sidenav=work_sidenav(""), body=body_data["body"],
        recitejs="", chatjs="", varjs=""))
    return body_data.get("total", 0)

def build_support():
    out = DIST / "support"; out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(TF(TMPL, title="Support", h1="Support the library",
        kicker="Support", sub="recitation, translation, proof — funded by readers",
        sidenav=work_sidenav(""),
        body='<div class="panel">This library is a free, open record of the Trika masters: Sanskrit held in full, translations gated honestly, recitation growing verse by verse.</div>'
        '<h3>What patronage funds</h3><div class="idx">'
        '<a><b>studio chants</b> — GPU rendering of each short work, verse by verse</a>'
        '<a><b>editions</b> — manuscript comparison behind every translation gate</a>'
        '<a><b>hosting</b> — audio and pages served free, forever</a></div>'
        '<h3>Patreon</h3><div class="panel"><b>Launching soon.</b> A Patreon page is on its way — check back here. Until then, the fastest support is a correction: every page carries an <i>Improve this page</i> link.</div>'
        + srclink("https://github.com/prx0r/ipvv/issues/new", "questions and offers of support land here until Patreon opens.")))
    return 1

def build_tools():
    import json as _j
    out = DIST / "tools"; out.mkdir(parents=True, exist_ok=True)
    entries = []
    for f in (ROOT / "data").glob("works*.json"):
        for w in _j.loads(f.read_text()):
            entries.append({"t": w.get("title", ""), "u": "", "k": "work"})
    for aid in MASTERS:
        ap = ROOT / "data/authors" / f"{aid}.json"
        if ap.exists():
            a = _j.loads(ap.read_text())
            entries.append({"t": a.get("name", aid), "u": f"/{aid}/index.html", "k": "master"})
    for e in _j.loads((ROOT / "data/glossary.json").read_text()):
        import unicodedata as _u
        slug = _u.normalize("NFD", e["term"]).encode("ascii", "ignore").decode()
        import re as _re
        slug = _re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-") or "term"
        entries.append({"t": e["term"], "u": f"/concepts/{slug}.html", "k": "concept"})
    (DIST / "data/search-index.json").write_text(_j.dumps(entries, ensure_ascii=False))
    (out / "index.html").write_text(TF(ATmpl,title="Tools", h1="Tools",
        sub="instant find across masters, works, concepts — runs entirely in your browser",
        sidenav=work_sidenav(""),
        body=('<input id="q" placeholder="search masters, works, concepts…" style="width:100%;padding:.7rem;font-size:1.1rem"/>'
              '<div class="idx" id="hits" style="margin-top:.6rem"></div>'
              '<div class="panel"><b>Verse lookup.</b> Type a passage id (e.g. <i>chunkV2-A-caturtho-vimarsa-aham</i>) — exact matches jump straight to the passage. <input id="v" placeholder="passage id…" style="width:100%;padding:.5rem;margin-top:.4rem"/><div id="vhit" style="margin-top:.4rem"></div></div>'
              '<div class="sub">Index built at deploy time from the same JSON the pages render. No server, no tracking.</div>'
              + srclink("site/build.py", "search index + pages are built here; tools/build_glossary.py mines the glossary.")
              + '<script>let IDX=[];fetch("/data/search-index.json").then(r=>r.json()).then(d=>IDX=d);'
              'q.oninput=()=>{const v=q.value.toLowerCase();const m=v?IDX.filter(e=>e.t.toLowerCase().includes(v)).slice(0,40):[];'
              'hits.innerHTML=m.map(e=>`<a href="${e.u||"/"+e.k+"s/index.html"}"><b>${e.t}</b> <i>${e.k}</i></a>`).join("")||(v?"<i>No matches.</i>":"")};'
              'v.oninput=()=>{const x=v.value.trim();vhit.innerHTML=x?`<a href="/ipvv/${x}.html">Open /ipvv/${x}</a> · <a href="/ipvv/${x.replace(/[^A-Za-z0-9_-]/g,"")}.html">try cleaned</a>`:""};</script>')))
    return 1

def build_scholars():
    out = DIST / "scholars"; out.mkdir(parents=True, exist_ok=True)
    scholars = json.loads((ROOT / "data/scholars.json").read_text())
    links = []
    for s in scholars:
        items = ""
        for it in s.get("items", []):
            acc = ACC_LABEL.get(it.get("access", ""), it.get("access", ""))
            link = f'<a href="{it["link"]}">link →</a>' if it.get("link") else "no public link"
            items += (f'<div class="panel"><b>{esc(it.get("title",""))}</b> {esc(str(it.get("year") or ""))}<br/>'
                      f'<div class="sub">{esc(acc)} · {link}</div>'
                      f'<div class="en">Used for: {esc(it.get("used_for",""))}</div></div>')
        body = (f'<div class="panel">{esc(s.get("summary",""))}</div>'
                + (f'<div class="panel"><b>Bio.</b> {esc(s["bio"])}</div>' if s.get("bio") else "")
                + read_with_html(s["id"])
                + f'<div class="sub">{esc(s.get("affiliation",""))} · status: {esc(s.get("status",""))} · dates: {esc(s.get("dates",{}).get("flourished",""))} — {esc(s.get("dates",{}).get("note",""))}</div>'
                + f'<div class="sub"><a href="/data/scholars.json">machine-readable JSON</a> · <a href="/data/person-schema.json">bio schema</a></div>'
                + items)
        (out / f'{s["id"]}.html').write_text(TF(ATmpl,title=s["name"], h1=esc(s["name"]),
            sub=esc(s.get("affiliation","")), sidenav=scholar_nav(s["id"]), body=body + srclink("site/data/scholars.json", "bio + bibliography live here.")))
        links.append(f'<a href="/scholars/{s["id"]}.html"><b>{esc(s["name"])}</b> — {esc(s.get("affiliation",""))}</a>')
    (out / "index.html").write_text(TF(ATmpl,title="Scholars", h1="Scholars",
        sub="secondary witnesses — read and cite, host only what is open", sidenav=scholar_nav("index"),
        body='<div class="idx">' + "".join(links) + "</div>"
             '<div class="panel">Rule: GREEN (OA/GRETIL/Mukhabodha) ships on site. YELLOW (academia/login, HAL metadata, IRIS) is read-and-cited with links, never hosted. RED (pirated scans, commercial PDFs) never touches the repo.</div>' + srclink("site/data/scholars.json", "all bios + bibliographies live here.")))
    return len(scholars)

def deva_of(s):
    """IAST roman -> Devanagari for the speech synthesizer (display text unchanged)."""
    try:
        from indic_transliteration import sanscript
        from indic_transliteration.sanscript import transliterate
        return transliterate(s or "", sanscript.IAST, sanscript.DEVANAGARI)
    except Exception:
        return s or ""

AUDIO_ALIAS = {"anuttarastika": "anuttarashtika"}
RECITE_TITLES = {"bhairavastava": "Bhairavastava", "anuttarashtika": "Anuttarashtika", "bodhapancadasika": "Bodhapancadasika", "kramastotra": "Kramastotra"}
SYNTH_RECITE = ("bodhapancadasika", "kramastotra")

def build_recite():
    """Studio-chant recitation pages (kashaudio AI renders) + audio shipping.
    English merges from translations JSON, PASS only — BLOCKED verses chant Sanskrit alone."""
    import json as _json
    sfx_dest = DIST / "audio" / "sfx"
    sfx_dest.mkdir(parents=True, exist_ok=True)
    if (ROOT / "static-audio/sfx").exists():
        for sf in (ROOT / "static-audio/sfx").glob("*.wav"):
            shutil.copy(sf, sfx_dest / sf.name)
    for adir in sorted((ROOT / "static-audio").iterdir()):
        if adir.is_dir() and adir.name != "sfx":
            dest = DIST / "audio" / adir.name
            dest.mkdir(parents=True, exist_ok=True)
            for mp3 in adir.glob("*.mp3"):
                shutil.copy(mp3, dest / mp3.name)
    (DIST / "data").mkdir(parents=True, exist_ok=True)
    for aj in sorted((ROOT / "data").glob("audio-*.json")):
        shutil.copy(aj, DIST / "data" / aj.name)
    out = DIST / "recite"; out.mkdir(parents=True, exist_ok=True)
    cards = []
    for aj in sorted((ROOT / "data").glob("audio-*.json")):
        A = _json.loads(aj.read_text()); work = A["work"]
        trmap = {}
        for cand in [work] + [k for k, v in AUDIO_ALIAS.items() if v == work]:
            tp = ROOT / f"data/translations/{cand}.json"
            if tp.exists():
                for it in _json.loads(tp.read_text()):
                    try: vnum = int(str(it.get("verses", "")).split("-")[0])
                    except Exception: continue
                    trmap[vnum] = it
        title = RECITE_TITLES.get(work, work)
        arts, wt, n_en = [], {}, 0
        for i, v in enumerate(A["verses"]):
            t = trmap.get(v["n"], {})
            en = (t.get("l2") or t.get("l1") or "") if t.get("gate") == "PASS" else ""
            if en: n_en += 1
            sa_deva = " ".join(v["padas"])
            byl = {}
            for w in v["words"]: byl.setdefault(w["pada"], []).append(w)
            pdivs, segs = [], []
            for pi in range(len(v["padas"])):
                ws = byl.get(pi, [])
                if ws: segs.append([ws[0]["on"], ws[-1]["off"]])
                spans = " ".join(f'<span class="w" data-on="{w["on"]}" data-off="{w["off"]}">{esc(w["w"])}</span>' for w in ws)
                pdivs.append(f'<div class="pada">{spans or esc(v["padas"][pi])}</div>')
            wt[v["id"]] = {"dur": v.get("dur", 0), "segs": segs}
            iast = "<br/>".join(esc(x) for x in v.get("iast", []) if x)
            eng = f'<div class="eng">{esc(en[:4000])}</div>' if en else '<div class="panel missing"><b>English withheld.</b> This verse has no gate-PASS English yet — the chant stands alone until it passes.</div>'
            badge = "studio chant"
            arts.append(f'<article class="verse" data-recite data-id="{v["id"]}" data-label="{esc(title)} &middot; verse {v["n"]}" data-sa="{esc(sa_deva)}" data-en="{esc(en[:4000])}" data-audio="{v["mp3"]}"><div class="vnum">{v["n"]}<br/><button class="vplay" data-play-idx="{i}">recite</button></div><div>{"".join(pdivs)}<div class="iast">{iast}</div>{eng}<div class="rnote"><span class="srcbadge">{badge}</span> &middot; {esc(v.get("meter",""))} &middot; align {v.get("mms","?")}</div></div></article>')
        mm = sum(v.get("mms", 0) for v in A["verses"]) / max(1, len(A["verses"]))
        en_btn = "" if n_en else "disabled title=\"English withheld on every verse \u2014 gate pending\""
        tools = f'<div class="recitetools"><button class="vplay all" data-play-all>Recite all</button><span class="rmodes"><button data-mode="sa">Sanskrit only</button><button data-mode="en" {en_btn}>English only</button><button data-mode="verse" class="on">Verse SA \u2192 EN</button><button data-mode="line">Line SA \u2192 EN</button></span><span class="rnote">line mode: Sanskrit line-by-line, English follows each verse</span></div>'
        stats = f'<div class="stats"><span><b>{len(A["verses"])}</b> verses</span><span><b>studio chant</b> AI voice</span><span><b>{mm:.2f}</b> mean align</span><span><b>{n_en}/{len(A["verses"])}</b> with English</span></div>'
        wtscript = "<script>window.__WT=" + _json.dumps(wt) + "</script>"
        (out / f"{work}.html").write_text(TF(TMPL, title=f"{title} recitation", h1=title,
            kicker="Recitation \u00b7 studio chant", sub=f"{len(A['verses'])} verses chanted, karaoke-timed · English shows only where the gate passed",
            sidenav=work_sidenav(""), body=stats + tools + "".join(arts) + srclink("https://github.com/prx0r/kashaudio", "chants rendered by the kashaudio pipeline (Vagdhenu AI voice); timings by MMS alignment."),
            recitejs=wtscript + RECITEJS))
        cards.append(("studio", f'<a href="/recite/{work}.html"><b>{esc(title)}</b> &mdash; {len(A["verses"])} verses &middot; studio chant &middot; {n_en} with English</a>'))
    for work in SYNTH_RECITE:
        tp = ROOT / f"data/translations/{work}.json"
        if not tp.exists():
            continue
        title = RECITE_TITLES.get(work, work)
        vitems = []
        for it in _json.loads(tp.read_text()):
            try: vnum = int(str(it.get("verses", "")).strip())
            except Exception: continue
            vitems.append((vnum, it))
        if not vitems:
            continue
        arts, n_en = [], 0
        for i, (vnum, it) in enumerate(vitems):
            en = (it.get("l2") or it.get("l1") or "") if it.get("gate") == "PASS" else ""
            if en: n_en += 1
            sa_roman, sa_deva = it.get("sanskrit", ""), deva_of(it.get("sanskrit", ""))
            eng = f'<div class="eng">{esc(en[:4000])}</div>' if en else '<div class="panel missing"><b>English withheld.</b> This verse has no gate-PASS English yet — the Sanskrit readout stands alone.</div>'
            arts.append(f'<article class="verse" data-recite data-id="{work}-{vnum}" data-label="{esc(title)} verse {vnum}" data-sa="{esc(sa_deva)}" data-en="{esc(en[:4000])}"><div class="vnum">{vnum}<br/><button class="vplay" data-play-idx="{i}">recite</button></div><div><div class="deva">{esc(sa_deva)}</div><div class="iast">{esc(sa_roman)}</div>{eng}<div class="rnote"><span class="rsrc">browser voice</span> — studio chant pending</div></div></article>')
        en_btn = "" if n_en else "disabled"
        tools = f'<div class="recitetools"><button class="vplay all" data-play-all>Recite all</button><span class="rmodes"><button data-mode="sa">Sanskrit only</button><button data-mode="en" {en_btn}>English only</button><button data-mode="verse" class="on">Verse SA to EN</button><button data-mode="line">Line SA to EN</button></span><span class="rnote">line mode: Sanskrit line-by-line, English follows each verse</span></div>'
        stats = f'<div class="stats"><span><b>{len(vitems)}</b> verses</span><span><b>browser-voice readout</b></span><span><b>{n_en}/{len(vitems)}</b> with English</span></div>'
        (out / f"{work}.html").write_text(TF(TMPL, title=f"{title} recitation", h1=title,
            kicker="Recitation - readout", sub=f"{len(vitems)} verses, browser-voice readout — studio chant pending; English shows only where the gate passed",
            sidenav=work_sidenav(""), body=stats + tools + "".join(arts) + srclink("https://github.com/prx0r/kashaudio", "studio chants render here as kashaudio reaches this work."),
            recitejs=RECITEJS))
        cards.append(("synth", f'<a href="/recite/{work}.html"><b>{esc(title)}</b> — {len(vitems)} verses · readout · {n_en} with English</a>'))
    studio_cards = "".join(c for k, c in cards if k == "studio")
    synth_cards = "".join(c for k, c in cards if k == "synth")
    (out / "index.html").write_text(TF(TMPL, title="Recitation", h1="Recitation",
        kicker="Listen", sub="studio chant where rendered · browser-voice readout everywhere else",
        sidenav=work_sidenav(""), body='<h3>Studio chant</h3><div class="idx">' + studio_cards + "</div>"
        + ("<h3>Readout</h3>" + f'<div class="idx">{synth_cards}</div>' if synth_cards else "")
        + '<div class="sub">Every verse and passage page also carries its own <b>Recite</b> button (browser-voice readout, four modes). Studio chant grows as kashaudio renders land — short works first.</div>'
        + srclink("https://github.com/prx0r/kashaudio", "chant pipeline lives here."), recitejs=RECITEJS))
    return len(cards)

def main():
    DIST.mkdir(parents=True, exist_ok=True)
    want = sys.argv[1].split(",") if len(sys.argv) > 1 else ["ipvv", "vbt", "tantrasara", "authors", "scholars", "translations", "concepts", "tools", "sections", "recite", "support", "essays", "pushinghub", "corpus", "receipts", "workbooks", "contentions", "essay-objects", "source-metaphysics", "information-packets", "ochema-methods", "philosophers", "ratier-chapters", "torella-volume", "recognition-framework", "arguments", "stylelab", "llmstxt", "screen", "meditate", "vbtmap", "practices", "app"]
    done = {}
    if "ipvv" in want: done["ipvv"] = build_ipvv()
    if "vbt" in want: done["vbt"] = build_vbt()
    if "tantrasara" in want: done["tantrasara"] = build_tantrasara()
    if "authors" in want:
        for aid in MASTERS: done[aid] = build_author(aid)
    if "scholars" in want: done["scholars"] = build_scholars()
    if "translations" in want: done["translations"] = build_translations()
    if "concepts" in want: done["concepts"] = build_glossary()
    if "tools" in want: done["tools"] = build_tools()
    if "sections" in want: done["sections"] = build_sections()
    if "recite" in want: done["recite"] = build_recite()
    if "support" in want: done["support"] = build_support()
    if "essays" in want: done["essays"] = build_essays()
    if "pushinghub" in want: done["pushinghub"] = build_pushing_hub()
    if "corpus" in want: done["corpus"] = build_corpus()
    if "receipts" in want: done["receipts"] = build_receipts()
    if "workbooks" in want: done["workbooks"] = build_workbooks()
    if "contentions" in want: done["contentions"] = build_contentions()
    if "essay-objects" in want: done["essay-objects"] = build_essay_objects()
    if "source-metaphysics" in want: done["source-metaphysics"] = build_source_metaphysics()
    if "information-packets" in want: done["information-packets"] = build_information_packets()
    if "ochema-methods" in want: done["ochema-methods"] = build_ochema_methods()
    if "philosophers" in want: done["philosophers"] = build_philosophers()
    if "ratier-chapters" in want: done["ratier-chapters"] = build_ratier_chapters()
    if "torella-volume" in want: done["torella-volume"] = build_torella_volume()
    if "recognition-framework" in want: done["recognition-framework"] = build_recognition_framework()
    if "arguments" in want: done["arguments"] = build_arguments()
    if "stylelab" in want: done["stylelab"] = build_stylelab()
    if "screen" in want: done["screen"] = build_screen()
    if "meditate" in want: done["meditate"] = build_meditate()
    if "vbtmap" in want: done["vbtmap"] = build_vbt_map()
    if "practices" in want: done["practices"] = build_practices()
    if "llmstxt" in want: done["llmstxt"] = build_llms_txt()
    if "app" in want: done["app"] = build_app()

    ship_translations()
    shutil.copy(ROOT / "data/latest.json", DIST / "data/latest.json")
    latest = "".join(f'<div class="ev"><b>{esc(i["date"])}</b> — <a href="{esc(i["url"])}">{esc(i["text"][:110])}</a></div>' for i in json.loads((ROOT / "data/latest.json").read_text()))
    masters = "".join(f'<a href="/{m}/index.html"><b>{m}</b> — bio · works map · click-in translations</a>' for m in MASTERS if m in done)
    rest = "".join(f'<a href="/{w}/index.html"><b>{w}</b> — {n} items · Sanskrit → READ → STUDY</a>' for w, n in done.items() if w not in MASTERS and w not in ("scholars", "translations", "concepts", "tools", "sections"))
    sch = '<a href="/scholars/index.html"><b>scholars</b> — secondary witnesses, linked bibliography (read/cite, host only what is open)</a>' if "scholars" in done else ""
    trn = '<a href="/translations/index.html"><b>pipeline translations</b> — English shows ONLY for gate-PASS passages</a>' if "translations" in done else ""
    con = '<a href="/concepts/index.html"><b>concepts</b> — glossary with every occurrence linked</a>' if "concepts" in done else ""
    rec = '<a href="/recite/index.html"><b>recitation</b> — studio chant + four-mode readout</a>' if "recite" in done else ""
    essb = '<a href="/essays/index.html"><b>essays</b> — working papers from the translations</a>' if "essays" in done else ""
    tls = '<a href="/tools/index.html"><b>tools</b> — instant find, verse lookup (in-browser)</a>' if "tools" in done else ""
    sec = '<a href="/masters/index.html"><b>masters</b> — chronological, birth-year order</a><a href="/modern/index.html"><b>modern</b> — living scholars A–Z</a>' if "sections" in done else ""
    lat = '<h3>Latest</h3>' + latest if latest else ""
    (DIST / "index.html").write_text(TF(TMPL,title="Read · recite · ask", h1="Read · recite · ask",
        sub="Sanskrit roots, gate-passed English, studio chant, live questions — display only what is formally done", sidenav=work_sidenav(""),
        body='<div class="idx">'
        + '<a href="/translations/index.html"><b>read</b> — 44 works · Sanskrit → READ · English only where the gate passed</a>'
        + '<a href="/recite/index.html"><b>recite</b> — studio chants + four-mode readout, verse by verse</a>'
        + '<a href="/practices/index.html"><b>practice</b> — 112 dhāraṇās with sound, breath-paced guidance</a>'
        + '<a href="/ipvv/pushing.html"><b>pushing</b> — hound a text with why · or tap Ask below and ask it live</a>'
        + '<a href="/essays/index.html"><b>essays</b> — working papers argued from the translations</a>'
        + "</div>" + lat))
    # full search index: every rendered page, titled (overwrites the partial tools-page index)
    import re as _re2
    try: _part = {e.get("u"): e for e in json.loads((DIST / "data/search-index.json").read_text())}
    except Exception: _part = {}
    _full = []
    for _f in sorted(DIST.rglob("*.html")):
        _u = "/" + _f.relative_to(DIST).as_posix()
        _m = _re2.search(r"<title>(.*?)</title>", _f.read_text(encoding="utf-8", errors="replace"))
        _t = (_m.group(1).split("·")[0].strip() if _m else _f.stem)
        _e = dict(_part.get(_u, {})); _e.update({"t": _t, "u": _u}); _e.setdefault("k", "page")
        _full.append(_e)
    (DIST / "data/search-index.json").write_text(json.dumps(_full, ensure_ascii=False))
    print("built", done)

if __name__ == "__main__":
    main()
