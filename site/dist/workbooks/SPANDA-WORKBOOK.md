<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>SPANDA-WORKBOOK · Trika Library</title><link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Tiro+Devanagari+Sanskrit:ital@0;1&family=Noto+Serif+Devanagari:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/><style>*{box-sizing:border-box}
:root{--paper:#fff;--card:#fff;--ink:#17140f;--mut:#76736e;--faint:#a9a49c;--line:#e7e3db;--gold:#a86f14;--gold-ink:#7c5410;--sans:'Inter',system-ui,-apple-system,sans-serif;--serif:Georgia,'Cormorant Garamond',serif;--deva:'Tiro Devanagari Sanskrit','Noto Serif Devanagari',serif}
html{-webkit-text-size-adjust:100%}
body{font-family:var(--serif);margin:0;background:var(--paper);color:var(--ink);font-size:17px;line-height:1.55;min-height:100vh;display:flex;flex-direction:column}
a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:2px}a:hover{text-decoration-color:var(--gold)}
/* top bar */
.topbar{position:sticky;top:0;z-index:50;background:var(--paper);border-bottom:1px solid var(--line)}
.topbar-in{max-width:1400px;margin:0 auto;display:flex;align-items:center;gap:.9rem;padding:.55rem 1rem}
.brand{color:var(--ink);white-space:nowrap;text-decoration:none;line-height:1.05}.deva-brand{font-family:var(--deva);font-size:1.45rem;line-height:1.25}
.brand small{font-family:var(--sans);font-size:.68rem;color:var(--mut);letter-spacing:.08em;text-transform:uppercase;display:block;line-height:1}
.topnav{display:flex;gap:.15rem;flex-wrap:wrap;font-family:var(--sans);font-size:.86rem}
.topnav a{padding:.4rem .6rem;border-radius:.5rem;color:var(--ink);text-decoration:none}
.topnav a:hover{background:#f4f1ea;text-decoration:none}
.topsearch{margin-left:auto;display:flex;gap:.4rem;align-items:center}
.topsearch input{font-family:var(--sans);font-size:.86rem;padding:.45rem .7rem;border:1px solid var(--line);border-radius:999px;background:#fff;min-width:180px;color:var(--ink)}
.topsearch input:focus{outline:none;border-color:var(--mut)}
.burger{display:none;background:none;border:1px solid var(--line);border-radius:.5rem;padding:.35rem .6rem;font-size:1rem;cursor:pointer;color:var(--ink)}
/* shell */
.shell{flex:1;width:100%;max-width:1400px;margin:0 auto;display:grid;grid-template-columns:264px minmax(0,1fr) 228px;gap:2rem;padding:1.5rem 1rem 3rem;align-items:start}
.side{position:sticky;top:64px;max-height:calc(100vh - 84px);overflow:auto;font-family:var(--sans);font-size:.86rem;padding-right:.5rem}
.side .hd{color:var(--mut);font-size:.7rem;text-transform:uppercase;letter-spacing:.09em;margin:.9rem 0 .3rem}
.side .hd:first-child{margin-top:0}
.side a{display:block;padding:.28rem .55rem;border-radius:.45rem;color:var(--ink);line-height:1.35;text-decoration:none}
.side a:hover{background:#f4f1ea}
.side a.on{background:#f4f1ea;font-weight:600;color:var(--ink)}
.side .sub a{padding-left:1rem;color:#4a463c}
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
.panel{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:1rem 1.2rem;margin:.7rem 0}
.panel.missing{opacity:.55;border-style:dashed}
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
<a class="brand" href="/index.html"><span class="deva-brand">स्वातन्त्र्य</span><small>freedom · trika library</small></a>
<nav class="topnav"><a href="/support/index.html">Support</a><a href="/stylelab/index.html">Style lab</a><a href="/arguments/index.html">Arguments</a><a href="/pushing/index.html">Pushing</a><a href="/essays/index.html">Essays</a><a href="/recite/index.html">Recite</a><a href="/masters/index.html">Masters</a><a href="/modern/index.html">Modern</a><a href="/concepts/index.html">Concepts</a><a href="/translations/index.html">Translations</a><a href="/tools/index.html">Tools</a></nav>
<span class="topsearch"><input id="q" placeholder="Search…" aria-label="search"/></span>
</div></header>
<div class="shell"><aside class="side" id="sidenav"><div class="hd">Masters (chronological)</div><a href="/bhattanarayana/index.html">Bhattanarayana</a><a href="/vasugupta/index.html">Vasugupta</a><a href="/kallata/index.html">Bhatta Kallata</a><a href="/somananda/index.html">Somananda</a><a href="/utpaladeva/index.html">Utpaladeva (Utpalacarya)</a><a href="/bhutiraja/index.html">Bhutiraja (Bhuti)</a><a href="/induraja/index.html">Induraja</a><a href="/sambhunatha/index.html">Sambhunatha</a><a href="/lakshmanagupta/index.html">Lakshmanagupta</a><a href="/abhinavagupta/index.html">› Abhinavagupta</a><a href="/ksemaraja/index.html">Ksemaraja (Rajanaka Ksemaraja)</a><a href="/jayaratha/index.html">Jayaratha (Rajanaka)</a><a href="/lalla/index.html">Lalla (Lal Ded, Lalleshvari)</a><a href="/sivopadhyaya/index.html">Sivopadhyaya</a><a href="/yogaraja/index.html">Yogaraja</a><div class="hd">Abhinavagupta</div><a href="/abhinavagupta/index.html">Bio</a><a href="/abhinavagupta/works.html">Works map</a><div class="hd">Works (canonical list)</div><div class="sub"><a href="/abhinavagupta/bodhapanacadasika.html">Bodhapañcadaśikā (Prabodhapañcadaśikā)</a><a href="/abhinavagupta/anuttarastika.html">Anuttarāṣṭikā</a><a href="/abhinavagupta/bhairavastava.html">Bhairavastava (Īśvarastava)</a><a href="/abhinavagupta/kramastotra.html">Kramastotra</a><a href="/abhinavagupta/paramarthacarca.html">Paramārthacarcā</a><a href="/abhinavagupta/paramarthadvadasika.html">Paramārthadvādaśikā (Advayadvādaśikā)</a><a href="/abhinavagupta/mahopadesavimsatika.html">Mahopadeśaviṃśatikā</a><a href="/abhinavagupta/anubhavanivedana.html">Anubhavanivedana</a><a href="/abhinavagupta/sivasaktyavinabhava.html">Śivaśaktyavinābhāvastotra</a><a href="/abhinavagupta/laghviprakriya.html">Laghvīprakriyā</a><a href="/abhinavagupta/dehastha.html">Dehasthadevatācakrastotra</a><a href="/abhinavagupta/paryantapancasika.html">Paryantapañcāśikā</a><a href="/abhinavagupta/rahasyapancadasika.html">Rahasyapañcadaśikā</a><a href="/abhinavagupta/paramarthasamgraha.html">Paramārthasaṃgraha</a><a href="/abhinavagupta/anuttarasataka.html">Anuttaraśataka</a><a href="/abhinavagupta/prakaranastotra.html">Prakaraṇastotra</a><a href="/abhinavagupta/tantraloka.html">Tantrāloka</a><a href="/abhinavagupta/tantrasara.html">Tantrasāra</a><a href="/abhinavagupta/tantroccaya.html">Tantroccaya</a><a href="/abhinavagupta/tantravatadhanika.html">Tantravaṭadhānikā (Seed of Tantra)</a><a href="/abhinavagupta/mvv.html">Mālinīvijayavārttika (Mālinīślokavārttika)</a><a href="/abhinavagupta/purvapancika.html">Pūrvapañcikā (comm. on Purvasastra/Malinivijaya)</a><a href="/abhinavagupta/ptv.html">Parātrīśikāvivaraṇa (long)</a><a href="/abhinavagupta/ptlaghu.html">Parātrīśikālaghuvṛtti (+ Anuttaratrimśikā laghuvṛtti)</a><a href="/abhinavagupta/devistotravivarana.html">Devīstotra­vivaraṇa</a><a href="/abhinavagupta/tattvadhvaprakasika.html">Tattvādhvaprakāśikā</a><a href="/abhinavagupta/ipv.html">Īśvarapratyabhijñāvimarśinī (laghvī)</a><a href="/abhinavagupta/ipvv.html">Īśvarapratyabhijñāvivṛtivimarśinī (bṛhatī)</a><a href="/abhinavagupta/sivadrstyalocana.html">Śivadṛṣṭyālocana</a><a href="/abhinavagupta/kathamukhatilaka.html">Kathāmukhatilaka</a><a href="/abhinavagupta/bhedavadavidarana.html">Bhedavādavidāraṇa</a><a href="/abhinavagupta/paramarthasara.html">Paramārthasāra</a><a href="/abhinavagupta/gitarthasamgraha.html">Bhagavadgītārthasaṃgraha</a><a href="/abhinavagupta/abhinavabharati.html">Abhinavabhāratī (Nāṭyaśāstravivṛti)</a><a href="/abhinavagupta/dhvanyalokalocana.html">Dhvanyālokalocana</a><a href="/abhinavagupta/kavyakautukavivarana.html">Kāvyakautukavivaraṇa (on Bhatta Tauta)</a><a href="/abhinavagupta/ghatakarpara.html">Ghaṭakarparakulakavivṛti</a><a href="/abhinavagupta/natyalocana.html">Nāṭyalocana</a><a href="/abhinavagupta/kramakeli.html">Kramakeli</a><a href="/abhinavagupta/prakirnakavivarana.html">Prakīrṇakavivaraṇa</a><a href="/abhinavagupta/padarthapravesa.html">Padārthapraveśanirṇayaṭīkā</a><a href="/abhinavagupta/prakaranavivarana.html">Prakaraṇavivaraṇa</a><a href="/abhinavagupta/parapravesika.html">Parāpraveśikā</a></div><div class="hd">Library</div><a href="/concepts/index.html">Concepts</a><a href="/translations/index.html">Translations</a><a href="/tools/index.html">Tools</a></aside>
<main><div class="crumbs" id="crumbs"></div><div class="klabel">Workbook</div><h1>SPANDA-WORKBOOK</h1><div class="skt"></div><div class="sub">1448 words · vendored research asset</div><div class="sub"><a href="/data/workbooks/SPANDA-WORKBOOK.md">source markdown →</a></div><ul>
<li>ANDA: THE PULSE</li>
<li>PULSE-FIRST WORKBOOK</li>
<li>at is the vibration that is already everything?</li>
<li>y does the world seem still and separate when it is a throb?</li>
<li>y does the pulse need the body, the breath, and the senses?</li>
</ul>
<ul>
<li>RPOSE</li>
<li>is workbook gives the Spandakārikā a logical entry point. It does not ask you to accept</li>
<li>shmir Śaiva metaphysics. It reconstructs the questions the system asks, the answers it</li>
<li>oposes, why each concept is introduced, and where the contested inferences remain.</li>
<li>epared as part of the Tantrāloka × Ochema research programme · August 2026</li>
</ul>
<hr/>
<ul>
<li>W TO USE THIS WORKBOOK</li>
<li> not read the Spandakārikā as verses to memorize. Read it as one escalating problem:</li>
<li>f reality is a single pulsing consciousness, why does it present itself as a still world</li>
<li> separate things, observed by a separate &quot;me&quot;?*</li>
<li> Read one unit at a time. The units are cumulative.</li>
<li> Keep three columns: what the text claims / what Ochema translates / what remains unproven.</li>
<li> Do the checkpoints. Conceptual control, not memorization.</li>
<li> Treat every modern comparison as an analogue, never an identity.</li>
<li> Return to the kārikā map only after Units 1–5.</li>
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
<li>reality that merely <i>shines</i> would be a lamp, not awareness. To be consciousness, it must</li>
<li>hrob* — and that throb is both the world&#x27;s manifestation and its self-knowing.</li>
</ul>
<ul>
<li>IT 1 — WHAT IS THE PULSE?</li>
<li>e tradition&#x27;s own term-policy is decisive: spanda = &quot;the pulse,&quot; never &quot;vibration,&quot;</li>
<li>ich risks sounding mechanical. It is the self-moving activity of consciousness itself.</li>
</ul>
<ul>
<li>1 The source of the wheel of energies</li>
<li>e root verse names the absolute as the pulse&#x27;s source:</li>
</ul>
<blockquote>taṃ śakticakravibhavaprabhavaṃ śaṃkaraṃ stumaḥ —</blockquote>
<blockquote>&quot;we praise Śaṅkara, the source of the Wheel of Energies.&quot;</blockquote>
<blockquote>— Spandakārikā 1.1 (the dossier&#x27;s anchor rendering)</blockquote>
<ul>
<li>2 Not a thing that vibrates</li>
<li>anda is not a substance that shakes. It is the very life of awareness — the movement by</li>
<li>ich consciousness knows and manifests at once. It is constitutive, not accidental.</li>
</ul>
<ul>
<li>3 The hidden pulse driving the triad</li>
</ul>
<blockquote>yataḥ kāraṇavargo &#x27;yaṃ vimūḍho &#x27;mūḍhavat svayam | sahāntareṇa cakreṇa</blockquote>
<blockquote>pravṛttisthitisaṃhṛtīḥ —</blockquote>
<blockquote>&quot;the host of causes, bewildered-as-if-not, by the inner wheel achieves creation,</blockquote>
<blockquote>maintenance, dissolution.&quot;</blockquote>
<blockquote>— Spandakārikā 1.6 (the hidden pulse driving the triad — the report&#x27;s A-thesis in the</blockquote>
<blockquote>Spanda&#x27;s form)</blockquote>
<ul>
<li>e world&#x27;s apparent stillness is the hidden pulse working unnoticed.</li>
</ul>
<ul>
<li>ECKPOINT 1</li>
<li>Why &quot;pulse&quot; and not &quot;vibration&quot;?</li>
<li>What does kārikā 1.6 reveal about the relation of the pulse to the visible world?</li>
</ul>
<ul>
<li>IT 2 — WHY DOES IT FEEL STILL?</li>
<li> reality is a single throb, why does experience present a still world of separate,</li>
<li>lid things?</li>
</ul>
<ul>
<li>1 The perceiver&#x27;s contraction</li>
<li>e world does not appear pulsing because the perceiver is contracted. The individual soul,</li>
<li>sorbed in its own standpoint, loses the felt sense of the pulse. It is not that the pulse</li>
<li>ops; it is that the perceiver stops being open to it.</li>
</ul>
<ul>
<li>2 Not an illusion of the world, but a limit of the perceiver</li>
<li>anda does not say the world is unreal. It says the world&#x27;s pulsing nature is overlooked</li>
<li> a contracted view. The stillness is a misperception of a throb, not proof that reality</li>
<li> still.</li>
</ul>
<ul>
<li>3 The caution</li>
<li>at experience has a temporal flow is a datum. That this flow is the absolute&#x27;s own</li>
<li>gnition-sequence is the metaphysical claim.</li>
</ul>
<ul>
<li>ECKPOINT 2</li>
<li>When the world seems still, what has changed — the world or the perceiver?</li>
<li>Why is &quot;spanda = energy&quot; a category error under the methodological rule?</li>
</ul>
<ul>
<li>IT 3 — WHAT IS CONSCIOUSNESS, IF IT PULSES?</li>
</ul>
<ul>
<li>1 Manifestation is self-showing (prakāśa)</li>
<li>nsciousness appears. Nothing is known without it.</li>
</ul>
<ul>
<li>2 Self-knowing is the pulse&#x27;s return (vimarśa)</li>
<li>nsciousness knows its own appearing. The pulse is the name for the inseparability of the</li>
<li>o: to manifest IS to know oneself manifesting.</li>
</ul>
<ul>
<li>3 The perceiver never deviates</li>
<li>e subject is not destroyed in liberation; it is recognized as having always been the</li>
<li>lse. The apparent &quot;fall&quot; into a bounded self was a misrecognition, not a departure of</li>
<li>ality from itself.</li>
</ul>
<ul>
<li>4 The integrated picture</li>
<li>nsciousness = activity that knows itself = spanda. Every cognition is a pulse: the</li>
<li>aching out toward an object and the taking it back into the self.</li>
</ul>
<ul>
<li>ECKPOINT 3</li>
<li>What is vimarśa, and why is it the pulse&#x27;s &quot;return&quot;?</li>
<li>How can cognition and manifestation be the same movement?</li>
</ul>
<ul>
<li>IT 4 — HOW DOES THE WORLD ARISE?</li>
</ul>
<ul>
<li>1 The wheel of powers (śakticakra)</li>
<li>ery faculty — perception, memory, imagination, agency — is a spoke of the wheel whose</li>
<li>urce is Śiva. The many powers are not separate things; they are the one consciousness</li>
<li>ving through its self-expressions.</li>
</ul>
<ul>
<li>2 The dissolution of the subject/object split</li>
<li>ere is not a &quot;me&quot; and a &quot;world&quot; with powers in between. There is one wheel, one source,</li>
<li>d its spokes are the apparent actors and objects. The finite self is a spoke that has</li>
<li>rgotten it belongs to the wheel.</li>
</ul>
<ul>
<li>3 World as self-articulation</li>
<li>e world is the shape the pulse takes in its self-knowing — the dynamism-pole of</li>
<li>nifestation, complementing the recognition-pole of Pratyabhijñā.</li>
</ul>
<ul>
<li>ECKPOINT 4</li>
<li>What is the śakticakra, and what is its source?</li>
<li>How does the wheel dissolve the subject/object split?</li>
</ul>
<ul>
<li>IT 5 — HOW DOES THE BODY AND BREATH FIT?</li>
<li>e pulse is not only metaphysical; it is felt as the body&#x27;s life and breath.</li>
</ul>
<ul>
<li>1 The pulse in the body</li>
<li>anda is the very life of the body — the breath, the heartbeat, the flow of sensation.</li>
<li>e body is not a cage around the pulse; it is one of the pulse&#x27;s own articulations.</li>
</ul>
<ul>
<li>2 Breath and sensation as access</li>
<li> attending to the body&#x27;s own pulsing, the yogi recovers the felt sense of spanda that</li>
<li>dinary perception overlooks. The body is a doorway to the pulse, not a barrier.</li>
</ul>
<ul>
<li>3 The caution</li>
<li>at the body &quot;feels alive&quot; is a datum. That this aliveness is the absolute&#x27;s own</li>
<li>lf-movement is the metaphysical claim.</li>
</ul>
<ul>
<li>ECKPOINT 5</li>
<li>Why is the body a doorway, not a barrier?</li>
<li>What practice-gate does the body offer, and what must not be inferred from it?</li>
</ul>
<ul>
<li>IT 6 — WHAT CHANGES IN LIBERATION?</li>
</ul>
<ul>
<li>1 Before and after</li>
<li>fore recognition, the perceiver feels bounded, separate, still. After, it recognizes</li>
<li>self as the pulse. Nothing is added; a mistaken identification is corrected.</li>
</ul>
<ul>
<li>2 Liberation as recognition, not escape</li>
<li>anda aligns with Pratyabhijñā: liberation is not leaving the world but recognizing the</li>
<li>er-present dynamic self-nature. The wheel never left its hub.</li>
</ul>
<ul>
<li>3 The lived difference</li>
<li>ough nothing is added, everything is felt differently — the world experienced as the</li>
<li>lse&#x27;s own body.</li>
</ul>
<ul>
<li>ECKPOINT 6</li>
<li>Why can&#x27;t liberation be the acquisition of a new state?</li>
<li>How does Spanda&#x27;s liberation relate to recognition?</li>
</ul>
<ul>
<li>IT 7 — WHY THE FOUR COMMENTARIES?</li>
</ul>
<ul>
<li>1 One verse, four depths</li>
<li>e Spandakārikā survives with four commentaries (Vṛtti, Vivṛti, Nirṇaya, Saṃdoha),</li>
<li>ited together by Dyczkowski. The same stanza is read at four levels: the gloss, the</li>
<li>ctrinal unfolding, the analytical determination, and the concentrated summary.</li>
</ul>
<ul>
<li>2 The reading method</li>
<li>beginner reads the gloss; a scholar the analysis; a practitioner the summary as a</li>
<li>ditation. This is the workbook&#x27;s three-depth display applied to the primary text itself.</li>
</ul>
<ul>
<li>3 What remains contested</li>
<li>w far the pulse is an actual felt process vs a structural description; the relation of</li>
<li>anda to the Śivasūtra&#x27;s authorship; the divergences of the four commentaries.</li>
</ul>
<ul>
<li>IT 8 — WHAT REMAINS UNRESOLVED?</li>
</ul>
<ul>
<li>1 The strongest Spanda chain</li>
<li>nifestation is self-showing; self-showing is self-knowing; self-knowing is the pulse; the</li>
<li>lse is the absolute.</li>
</ul>
<ul>
<li>2 The contested jump</li>
<li>at the felt aliveness of the body is the absolute&#x27;s own self-movement is the metaphysical</li>
<li>ap — the tradition&#x27;s claim, not an established fact.</li>
</ul>
<ul>
<li>3 What Ochema can contribute</li>
<li>p the pulse onto the dynamism pole; compare with modern self-organization and active</li>
<li>ference — as correspondence, never identity.</li>
</ul>
<ul>
<li>4 What Ochema must not claim yet</li>
<li>at physics &quot;proves&quot; spanda, or that spanda &quot;proves&quot; a physics.</li>
</ul>
<ul>
<li>5 Final synthesis</li>
<li>anda gives the system its energy: the pulse that both manifests and knows. It connects</li>
<li>e precision of Pratyabhijñā (recognition) to the process-ontology of Krama (sequence).</li>
<li>e Krama&#x27;s own signature captures it in one image:</li>
</ul>
<blockquote>spandāspandaparispandamakarandamahotpalam —</blockquote>
<blockquote>&quot;the great lotus of the nectar that is the pulse, the pulse&#x27;s rest, the pulse&#x27;s</blockquote>
<blockquote>outpouring.&quot;</blockquote>
<blockquote>— Mahārthamañjarī 2 (the Krama reading of the pulse-triple)</blockquote><div class="sub">Sources & corrections: <a href="https://github.com/prx0r/ipvv/edit/master/site/data/workbooks/SPANDA-WORKBOOK.md">edit source →</a>. source lives here.</div><div class="pn" id="pnslot"></div></main>
<aside class="toc"><div class="hd">On this page</div><div id="tocbody"></div></aside></div>
<footer><div class="fin"><span>Trika Library — display only what is formally done.</span><a href="/support/index.html">Support</a><a href="/tools/index.html">Tools</a><a href="/data/person-schema.json">Schema</a><a href="https://github.com/prx0r/ipvv">Source</a><a href="https://github.com/prx0r/ipvv/issues/new">Improve this page</a></div></footer>
<script>window.API="https://ipvv-api.tradesprior.workers.dev";var __IDX__=null;fetch("/data/search-index.json").then(function(r){return r.json()}).then(function(d){__IDX__=d});
var q=document.getElementById("q");
if(q){q.addEventListener("keydown",function(e){if(e.key==="Enter"&&__IDX__){var v=q.value.toLowerCase();var m=__IDX__.filter(function(x){return x.t.toLowerCase().indexOf(v)>-1}).slice(0,1)[0];if(m&&m.u)location.href=m.u}})}
var c=document.getElementById("crumbs");if(c){var p=location.pathname.split("/").filter(Boolean);var h='<a href="/index.html">home</a>';var acc="";p.forEach(function(seg,i){acc+="/"+seg;var last=i===p.length-1;var t=decodeURIComponent(seg).replace(/[-_]/g," ").replace(/\.html$/,"");h+=(last?" › "+t:' › <a href="'+acc+(acc==="/index"?"":".html")+'">'+t+"</a>")});c.innerHTML=h;}</script>
<script>
(function(){
var b=document.getElementById('burger');
if(b){b.addEventListener('click',function(){document.body.classList.toggle('navopen')});}
var toc=document.getElementById('tocbody');
if(toc){var hs=document.querySelectorAll('main h2, main h3');var html='';
hs.forEach(function(h,i){if(!h.id){h.id='s'+i}html+='<a href="#'+h.id+'" data-t="'+h.id+'">'+h.textContent.slice(0,60)+'</a>'});
toc.innerHTML=html||'<span style="color:#999">—</span>';
var links=Array.prototype.slice.call(toc.querySelectorAll('a'));
function spy(){var y=window.scrollY+120,cur=null;
hs.forEach(function(h){if(h.getBoundingClientRect().top<120)cur=h.id});
links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+cur)});
if(!cur&&links.length)links[0].classList.add('on');}
window.addEventListener('scroll',spy,{passive:true});spy();}
})();
</script><script>
(function(){
if(!window.API)return;
var btn=document.createElement('button');
btn.textContent='Ask';
btn.style.cssText='position:fixed;bottom:1rem;right:1rem;z-index:90;background:#1c1a17;color:#fff;border:0;border-radius:999px;padding:.6rem 1.1rem;font-family:Inter,sans-serif;font-size:.84rem;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.15)';
document.body.appendChild(btn);
var panel=document.createElement('div');
panel.style.cssText='position:fixed;bottom:4rem;right:1rem;width:min(90vw,360px);max-height:60vh;background:#fff;border:1px solid #e6ddc9;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.12);display:none;flex-direction:column;z-index:90;font-family:Inter,sans-serif';
panel.innerHTML='<div style="padding:.6rem .8rem;border-bottom:1px solid #e6ddc9;font-weight:600;font-size:.84rem">Ask '+works.join(', ')+'</div><div id="chatmsgs" style="flex:1;overflow:auto;padding:.6rem .8rem;font-size:.84rem;min-height:120px"></div><div style="padding:.5rem .8rem;border-top:1px solid #e6ddc9;display:flex;gap:.4rem"><input id="chatin" placeholder="Ask..." style="flex:1;padding:.4rem .6rem;border:1px solid #e6ddc9;border-radius:.4rem;font-size:.84rem"/><button id="chatsend" style="padding:.4rem .7rem;background:#1c1a17;color:#fff;border:0;border-radius:.4rem;cursor:pointer;font-size:.84rem">Send</button></div>';
document.body.appendChild(panel);
btn.onclick=function(){panel.style.display=panel.style.display==='flex'?'none':'flex'};
var work=location.pathname.split('/')[1]||'ipvv';
var works=[work];
// multi-text: add works via ?works=ipvv,tantrasara
var wm=new URLSearchParams(location.search).get('works');
if(wm)works=wm.split(',').map(function(w){return w.trim()}).filter(Boolean);
var workStr=works.join(',');
var sid=null;
function addMsg(role,text){var d=document.createElement('div');d.style.cssText='margin:.4rem 0;'+(role==='user'?'text-align:right':'');d.innerHTML='<b>'+(role==='user'?'You':'Assistant')+':</b> '+text;document.getElementById('chatmsgs').appendChild(d);document.getElementById('chatmsgs').scrollTop=99999}
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