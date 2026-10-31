<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>PRATYABHIJNA-WORKBOOK</title><link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Tiro+Devanagari+Sanskrit:ital@0;1&family=Noto+Serif+Devanagari:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/><style>*{box-sizing:border-box}
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
</style></head><body>
<header class="topbar"><div class="topbar-in">
<button class="burger" id="burger" aria-label="menu">☰</button>
<a class="brand" href="/index.html"><span class="deva-brand">स्वातन्त्र्य</span><small>freedom</small></a>
<nav class="topnav" id="topnav"><a href="/translations/index.html" data-sec="translations">Read</a><a href="/recite/index.html" data-sec="recite">Recite</a><a href="/practices/index.html" data-sec="practices">Practise</a><a href="/ipvv/pushing.html" data-sec="ipvv">Enquire</a><a href="/tools/index.html" data-sec="tools">Translate</a><a href="/essays/index.html" data-sec="essays">Write</a></nav>
<span class="topsearch"><input id="q" placeholder="Search…" aria-label="search"/></span>
</div></header>
<div class="shell"><aside class="side" id="sidenav"><details class="mnav" data-mnav="masters" open><summary class="hd">Masters (by works)</summary><div class="sub"><a href="/abhinavagupta/index.html">Abhinavagupta <span class="n">(43)</span></a><a href="/ksemaraja/index.html">Ksemaraja <span class="n">(16)</span></a><a href="/utpaladeva/index.html">Utpaladeva <span class="n">(10)</span></a><a href="/kallata/index.html">Bhatta Kallata <span class="n">(3)</span></a><a href="/bhattanarayana/index.html">Bhattanarayana <span class="n">(2)</span></a><a href="/jayaratha/index.html">Jayaratha <span class="n">(2)</span></a><a href="/somananda/index.html">Somananda <span class="n">(2)</span></a><a href="/vasugupta/index.html">Vasugupta <span class="n">(2)</span></a><a href="/bhutiraja/index.html">Bhutiraja <span class="n">(1)</span></a><a href="/induraja/index.html">Induraja <span class="n">(1)</span></a><a href="/lakshmanagupta/index.html">Lakshmanagupta <span class="n">(1)</span></a><a href="/lalla/index.html">Lalla <span class="n">(1)</span></a><a href="/sambhunatha/index.html">Sambhunatha <span class="n">(1)</span></a><a href="/sivopadhyaya/index.html">Sivopadhyaya <span class="n">(1)</span></a><a href="/yogaraja/index.html">Yogaraja <span class="n">(1)</span></a></div></details><div class="hd">Modern</div><a href="/scholars/index.html">Scholars</a><div class="hd">Library</div><a href="/concepts/index.html">Concepts</a><a href="/translations/index.html">Translations</a><a href="/tools/index.html">Tools</a></aside>
<main><div class="crumbs" id="crumbs"></div><div class="klabel">Workbook</div><h1>PRATYABHIJNA-WORKBOOK</h1><div class="skt"></div><div class="sub">1572 words · vendored research asset</div><div class="sub"><a href="/data/workbooks/PRATYABHIJNA-WORKBOOK.md">source markdown →</a></div><ul>
<li>ATYABHIJÑĀ: RECOGNITION</li>
<li>RECOGNITION-FIRST WORKBOOK</li>
<li>at does it mean to recognize oneself as the Lord?</li>
<li>y does experience seem to contradict it?</li>
<li>y does recognition need memory, imagination, and freedom?</li>
</ul>
<ul>
<li>RPOSE</li>
<li>is workbook gives the Pratyabhijñā (recognition) school a logical entry point. It does</li>
<li>t ask you to accept Kashmir Śaiva metaphysics. It reconstructs the questions the system</li>
<li>ks, the answers it proposes, why each concept is introduced, and where the contested</li>
<li>ferences remain.</li>
<li>epared as part of the Tantrāloka × Ochema research programme · August 2026</li>
</ul>
<hr/>
<ul>
<li>W TO USE THIS WORKBOOK</li>
<li> not read the Īśvarapratyabhijñākārikā as verses to memorize. Read it as one escalating</li>
<li>oblem: *if the self is already unrestricted consciousness, why does it present itself as</li>
<li>bounded, vulnerable, separate person?*</li>
<li> Read one unit at a time. The units are cumulative.</li>
<li> Keep three columns: what the text claims / what Ochema translates / what remains unproven.</li>
<li> Do the checkpoints. The purpose is conceptual control, not memorization.</li>
<li> Treat every modern comparison as an analogue, never an identity.</li>
<li> Return to the kārikā map only after Units 1–6.</li>
</ul>
<ul>
<li>THODOLOGICAL RULE</li>
<li>ver allow a mathematical theorem, neuroscientific model, or contemplative experience to</li>
<li>herit the truth of a metaphysical claim merely because their structures resemble one</li>
<li>other. Translation, analogy, implementation, and identity are four different relations.</li>
</ul>
<hr/>
<ul>
<li>E ONE PROBLEM</li>
<li>self that is already all cannot <i>learn</i> to be what it is; it can only <i>re-cognize</i> it.</li>
<li>erything in the Pratyabhijñā is the working-out of that single insight.</li>
</ul>
<ul>
<li>IT 1 — WHAT IS RECOGNITION?</li>
<li>cognition (pratyabhijñā) is the system&#x27;s name and its whole claim. <i>jñā</i> = to know;</li>
<li>rati-* = &quot;return&quot; / &quot;counter.&quot; Knowing-again.</li>
</ul>
<ul>
<li>1 Re-cognition, not new attainment</li>
<li>e aim is not the acquisition of a new fact but the realization of an identity already</li>
<li>esent. Ratié, quoting Abhinavagupta&#x27;s own gloss, makes it precise:</li>
</ul>
<blockquote>&quot;The aim of the treatise is a recognition, which is not a new knowledge, but the</blockquote>
<blockquote>realization that one already possesses a knowledge.&quot;</blockquote>
<blockquote>— Isabelle Ratié, <i>On reason and scripture in the Pratyabhijñā</i> (2017), p. 121</blockquote>
<ul>
<li>2 The ordinary structure</li>
<li>cognition is what happens when a memory returns: you see a person and know, &quot;this is the</li>
<li>me one.&quot; A synthesis of present perception with a remembered form — not inference, not</li>
<li>velty, but the return of identity.</li>
</ul>
<ul>
<li>3 Recognition has a truth-condition</li>
<li>cognition succeeds only if the identity is <i>true</i>. Confidence, intensity, and</li>
<li>ansformation cannot substitute for veridicality. An experience can be transformative</li>
<li>d yet not be recognition of Śiva. (See the Tantrāloka workbook, Unit 1: the same</li>
<li>arp distinction governs the whole corpus.)</li>
</ul>
<blockquote>&quot;An experience can be psychologically transformative and phenomenologically convincing</blockquote>
<blockquote>without being recognition of Śiva.&quot;</blockquote>
<blockquote>— <i>Tantrāloka Recognition-First Workbook</i>, §1.1</blockquote>
<ul>
<li>ECKPOINT 1</li>
<li>What is the &quot;re-&quot; of re-cognition, and why does it matter?</li>
<li>Why can no intense experience substitute for a <i>true</i> recognition?</li>
</ul>
<ul>
<li>IT 2 — WHY IS RECOGNITION NOT AN INFERENCE?</li>
<li>e distinction blocks a fundamental misreading: that the Pratyabhijñā is a syllogism that</li>
<li>roves* we are Śiva. It is not. It establishes no new fact.</li>
</ul>
<ul>
<li>1 The pointing-out, not the proof</li>
</ul>
<blockquote>&quot;[The inference] merely leads the subject who hears it to pay attention to his or her</blockquote>
<blockquote>own experience... it is equivalent to the act of showing that consists in making</blockquote>
<blockquote>[someone] pay attention [to something by saying] <i>See! See!</i>&quot;</blockquote>
<blockquote>— Ratié, <i>On reason and scripture</i>, pp. 121–122 (quoting the IPVV)</blockquote>
<ul>
<li>2 The prefix <i>prati-</i> carries the force</li>
</ul>
<blockquote>&quot;Abhinavagupta explains that the goal of the treatise is not a cognition but a</blockquote>
<blockquote>re-cognition (praty-abhijñā), where praty- stands for pratīpam, again... It is a</blockquote>
<blockquote>re-cognition because the Self&#x27;s manifestation is not something that did not exist</blockquote>
<blockquote>before, because its manifestation is never interrupted.&quot;</blockquote>
<blockquote>— Ratié, p. 122 (quoting the IPVV)</blockquote>
<ul>
<li>3 The arguments are de-occluding</li>
<li>e arguments do not add to the self; they redirect attention to the self&#x27;s never-</li>
<li>terrupted self-manifestation. They are therapeutic, not productive of a new fact.</li>
</ul>
<ul>
<li>ECKPOINT 2</li>
<li>Why is recognition not an inference?</li>
<li>What does &quot;See! See!&quot; reveal about the function of the arguments?</li>
</ul>
<ul>
<li>IT 3 — WHAT MUST CONSCIOUSNESS BE?</li>
<li>r recognition to be possible, consciousness must have three inseparable features.</li>
</ul>
<ul>
<li>1 Prakāśa — manifestation</li>
<li>nsciousness appears; it is self-luminous. Nothing is known without it. The self is never</li>
<li>sent from awareness.</li>
</ul>
<ul>
<li>2 Vimarśa — reflexive self-knowing</li>
<li>nsciousness does not merely appear; it knows its own appearing. A light that did not</li>
<li>ow its own shining would be a stone, not awareness. The two are inseparable poles.</li>
</ul>
<ul>
<li>3 Svātantrya — creative freedom</li>
</ul>
<blockquote>&quot;Utpaladeva&#x27;s elaborate phenomenological analyses of memory, imagination, perception,</blockquote>
<blockquote>intentionality, etc., all point out the boundless creative freedom (svātantrya) of the</blockquote>
<blockquote>individual&#x27;s consciousness – a freedom which is the essence of the Lord described by the</blockquote>
<blockquote>Śaiva scriptures.&quot;</blockquote>
<blockquote>— Ratié, p. 122</blockquote>
<ul>
<li>e freedom to remember is the freedom by which consciousness manifests a world.</li>
</ul>
<ul>
<li>ECKPOINT 3</li>
<li>Why is luminosity (prakāśa) alone insufficient?</li>
<li>How does memory reveal the creative freedom (svātantrya)?</li>
</ul>
<ul>
<li>IT 4 — HOW DOES LIMITATION ARISE?</li>
<li> the self is unrestricted, how does it appear as a bounded person?</li>
</ul>
<ul>
<li>1 Contraction and misidentification</li>
<li>e limitation is not a change of reality but a misidentification: the unrestricted self is</li>
<li>entified with a bounded &quot;me.&quot; A failure of recognition, not a new entity.</li>
</ul>
<ul>
<li>2 The five kañcukas</li>
<li>lā (limited agency), vidyā (limited knowledge), rāga (attachment), kāla (time), niyati</li>
<li>ecessity) contract infinite capacities into finite experience. The finite subject is a</li>
<li>ntracted configuration of consciousness, not a separate thing.</li>
</ul>
<ul>
<li>3 Not illusion</li>
<li>e world is not dismissed. It is a real manifestation of consciousness. The error is not</li>
<li>at the world exists; it is that it is taken to be outside and other than consciousness.</li>
</ul>
<ul>
<li>ECKPOINT 4</li>
<li>What is the difference between &quot;becoming limited&quot; and &quot;misidentifying oneself as limited&quot;?</li>
<li>Why is the world not dismissed?</li>
</ul>
<ul>
<li>IT 5 — THE A/B/C STRATIFICATION</li>
<li>beration-as-recognition is not a single leap. It stratifies.</li>
</ul>
<ul>
<li>1 A — reflexive presence (established)</li>
<li>nsciousness is always already present to itself. Even before any &quot;I,&quot; there is the sheer</li>
<li>minosity of awareness.</li>
</ul>
<ul>
<li>2 B — ownership (plausible)</li>
<li>is presence is <i>mine</i> — a first-person awareness that owns its states.</li>
</ul>
<ul>
<li>3 C — universalization (the live frontier)</li>
<li>is very consciousness is the Lord&#x27;s — the &quot;I&quot; is not a private subject but the self of</li>
<li>l. Here the argument must work hardest, and the honest doubt lives.</li>
</ul>
<ul>
<li>rella captures the whole stratification in one line:</li>
</ul>
<blockquote>&quot;Recognition... concerns an entity which, invested from the outset with a valid means of</blockquote>
<blockquote>knowledge, is already manifest.&quot;</blockquote>
<blockquote>— Raffaele Torella, <i>Īśvarapratyabhijñākārikā</i> (critical ed.), introduction</blockquote>
<ul>
<li>ECKPOINT 5</li>
<li>What are the three levels, and which is most contested?</li>
<li>Why does the stratification keep the teaching honest?</li>
</ul>
<ul>
<li>IT 6 — WHY CAN RECOGNITION FAIL?</li>
<li>cause consciousness is freedom, no proof can force recognition. This is the nuance that</li>
<li>eps the teaching razor-sharp.</li>
</ul>
<ul>
<li>1 Recognition is not guaranteed</li>
</ul>
<blockquote>&quot;Reason&#x27;s power is ultimately limited by the fact that Recognition is in no way</blockquote>
<blockquote>guaranteed by its use: the most elaborate demonstrations do not necessarily produce the</blockquote>
<blockquote>realization of one&#x27;s identity with Śiva, because in a system that defines consciousness</blockquote>
<blockquote>as an absolute freedom (svātantrya), reason&#x27;s necessity can only be compelling if</blockquote>
<blockquote>consciousness agrees to be compelled.&quot;</blockquote>
<blockquote>— Ratié, p. 133</blockquote>
<ul>
<li>2 The consequence</li>
<li>cognition can be offered, shown, pointed to; it cannot be coerced. The freedom that makes</li>
<li>e self divine is the very freedom that lets it refuse to recognize itself.</li>
</ul>
<ul>
<li>ECKPOINT 6</li>
<li>Why can&#x27;t even the best argument force recognition?</li>
<li>What does the freedom-to-refuse reveal about the premise?</li>
</ul>
<ul>
<li>IT 7 — WHAT CHANGES IN LIBERATION?</li>
<li> the self never ceased to be present and free, liberation cannot add anything.</li>
</ul>
<ul>
<li>1 A correction of identification</li>
<li>beration is not attainment but the correction of a misidentification: the finite &quot;me&quot; was</li>
<li>ver separate from the consciousness through which everything appears.</li>
</ul>
<ul>
<li>2 Completion is dṛḍhavimarśa</li>
<li>e goal is a firm, stable reflective awareness — recognition that <i>holds</i>. Ratié uses the</li>
<li>rm for what reason is <i>for</i>:</li>
</ul>
<blockquote>&quot;They also assign to reason the task of transforming scriptures... into a means of</blockquote>
<blockquote>knowledge expressing a strong realization (dṛḍhavimarśa).&quot;</blockquote>
<blockquote>— Ratié, pp. 132–133</blockquote>
<ul>
<li>3 The lived difference</li>
<li>ough nothing is added, everything is felt differently. The receiver is recognized as the</li>
<li>urce.</li>
</ul>
<ul>
<li>ECKPOINT 7</li>
<li>Why is liberation a correction, not an attainment?</li>
<li>What is dṛḍhavimarśa, and why does it matter?</li>
</ul>
<ul>
<li>IT 8 — WHAT REMAINS UNRESOLVED?</li>
</ul>
<ul>
<li>1 The strongest chain</li>
<li>nifestation is self-showing; self-showing is self-knowing; the self is free; limitation</li>
<li> misidentification; recognition corrects it. Each step textually anchored.</li>
</ul>
<ul>
<li>2 The contested points</li>
<li>e C-level (universalization: is &quot;I am all&quot; established or only plausible?); the contested</li>
<li>adings in the IPVV; the exact force of memory across lives.</li>
</ul>
<ul>
<li>3 What Ochema can contribute</li>
<li>p recognition onto the grid; compare with modern work on for-me-ness and the</li>
<li>flexivism/anonymism debate — as correspondence, never identity.</li>
</ul>
<ul>
<li>4 What Ochema must not claim yet</li>
<li>at cognitive science &quot;proves&quot; recognition, or that the tradition &quot;proves&quot; a cognitive</li>
<li>del.</li>
</ul>
<ul>
<li>5 Final synthesis</li>
<li>cognition is the keystone. It defines the vocabulary (prakāśa, vimarśa, svātantrya) that</li>
<li>ery other workbook depends on. Get it right, and the Spanda, Krama, and Trika workbooks</li>
<li>l have their anchor.</li>
</ul><div class="sub">Sources & corrections: <a href="https://github.com/prx0r/ipvv/edit/master/site/data/workbooks/PRATYABHIJNA-WORKBOOK.md">edit source →</a>. source lives here.</div><div class="pn" id="pnslot"></div></main>
<aside class="toc"><div class="hd">On this page</div><div id="tocbody"></div></aside></div>
<footer><div class="fin"><span>Display only what is formally done.</span><a href="/support/index.html">Support</a><a href="/tools/index.html">Tools</a><a href="/data/person-schema.json">Schema</a><a href="https://github.com/prx0r/ipvv">Source</a><a href="https://github.com/prx0r/ipvv/issues/new">Improve this page</a></div></footer>
<script>window.API="https://ipvv-api.tradesprior.workers.dev";var __IDX__=null;fetch("/data/search-index.json").then(function(r){return r.json()}).then(function(d){__IDX__=d});
var q=document.getElementById("q");
if(q){q.addEventListener("keydown",function(e){if(e.key==="Enter"&&__IDX__){var v=q.value.toLowerCase();var m=__IDX__.filter(function(x){return x.t.toLowerCase().indexOf(v)>-1}).slice(0,1)[0];if(m&&m.u)location.href=m.u}})}
var c=document.getElementById("crumbs");if(c){var p=location.pathname.split("/").filter(Boolean);var h='<a href="/index.html">home</a>';var acc="";p.forEach(function(seg,i){acc+="/"+seg;var last=i===p.length-1;var t=decodeURIComponent(seg).replace(/[-_]/g," ").replace(/\.html$/,"");h+=(last?" › "+t:' › <a href="'+acc+(acc==="/index"?"":".html")+'">'+t+"</a>")});c.innerHTML=h;}</script>
<script>
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
var t=a.textContent.replace(/^›\s*/,'');
a.textContent=t;
if(h===path){a.textContent='› '+t;}
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
</script><script>
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
</script>{varjs}</body></html>