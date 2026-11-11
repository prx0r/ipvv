import {handleScholar} from './scholar-workspace.js';

let cachedVectors = null;
let cachedPushIndex = null;

async function getPushIndex(env) {
  if (cachedPushIndex) return cachedPushIndex;
  try {
    const resp = await fetch('https://ipvv-a8u.pages.dev/data/pushing/INDEX.json');
    if (!resp.ok) return null;
    cachedPushIndex = await resp.json();
    return cachedPushIndex;
  } catch (e) { return null; }
}

async function dashscopeChat(env, messages, maxTokens = 512, signal) {
  const apiKey = env.DASHSCOPE_API_KEY;
  if (!apiKey) throw new Error('no dashscope key');
  const resp = await fetch('https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions', {
    method: 'POST',
    ...(signal?{signal}:{}),
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'qwen3.8-omni-flash',
      messages,
      max_tokens: maxTokens,
      reasoning_effort: 'medium',
    }),
  });
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`dashscope ${resp.status}: ${err.slice(0, 200)}`);
  }
  const data = await resp.json();
  return data.choices?.[0]?.message?.content || '';
}

async function getVectors(env) {
  if (cachedVectors) return cachedVectors;
  try {
    const resp = await fetch('https://ipvv-a8u.pages.dev/data/vectors.json?v=' + Date.now());
    if (!resp.ok) return null;
    cachedVectors = await resp.json();
    return cachedVectors;
  } catch (e) {
    return null;
  }
}

function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) + 1e-8);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // allow-list: configured origin + the reading front-ends (public data, no credentials)
    const reqOrigin = request.headers.get('Origin') || '';
    const allowed = new Set([env.CORS_ORIGIN || '', 'https://svatantrya.net', 'https://svread.pages.dev', 'https://ipvv-a8u.pages.dev'].filter(Boolean));
    // Caller origins we will return an OAuth flow to: the allow-list plus
    // any *.svread.pages.dev branch alias plus local dev servers.
    const returnableOrigin = (o) => {
      if (!o || typeof o !== 'string') return '';
      try {
        const u = new URL(o);
        if (allowed.has(u.origin)) return u.origin;
        if (u.protocol === 'https:' && /\.svread\.pages\.dev$/.test(u.hostname)) return u.origin;
        if ((u.hostname === 'localhost' || u.hostname === '127.0.0.1')) return u.origin;
      } catch (e) { /* not a URL */ }
      return '';
    };
    const cors = {
      'Access-Control-Allow-Origin': allowed.has(reqOrigin) ? reqOrigin : (env.CORS_ORIGIN || '*'),
      'Access-Control-Allow-Credentials': 'true',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: cors });
    }

    const path = url.pathname;

    // Account sessions are cross-origin between the reader and the worker.
    // Reject unexpected browser origins and never sign with an empty secret.
    if (path.startsWith('/api/auth/')) {
      if (reqOrigin && !allowed.has(reqOrigin)) return json({error:'origin not allowed'}, 403, cors);
      if (typeof env.SESSION_SECRET !== 'string' || env.SESSION_SECRET.length < 32)
        return json({error:'authentication temporarily unavailable'}, 503, cors);
    }

    // POST /api/profile
    if (path === '/api/profile' && request.method === 'POST') {
      const { email } = await request.json();
      if (!email) return json({ error: 'email required' }, 400, cors);
      const id = 'u:' + btoa(email).replace(/=/g, '');
      await env.DB.prepare('INSERT OR IGNORE INTO profiles (id, email) VALUES (?, ?)').bind(id, email).run();
      return json({ id, email }, 200, cors);
    }

    // POST /api/variants
    if (path === '/api/variants' && request.method === 'POST') {
      const { user_id, work, chunk, text, style } = await request.json();
      if (!user_id || !work || !chunk || !text) return json({ error: 'missing fields' }, 400, cors);
      const id = 'v:' + crypto.randomUUID();
      await env.DB.prepare('INSERT INTO variants (id, user_id, work, chunk, text, style) VALUES (?, ?, ?, ?, ?, ?)')
        .bind(id, user_id, work, chunk, text, style || 'owner').run();
      return json({ id }, 200, cors);
    }

    // GET /api/variants/:work/:chunk
    const vm = path.match(/^\/api\/variants\/([^/]+)\/([^/]+)$/);
    if (vm && request.method === 'GET') {
      const [, work, chunk] = vm;
      const { results } = await env.DB.prepare('SELECT * FROM variants WHERE work = ? AND chunk = ? ORDER BY created_at DESC')
        .bind(work, chunk).all();
      return json({ variants: results }, 200, cors);
    }

    // POST /api/bookmarks
    if (path === '/api/bookmarks' && request.method === 'POST') {
      const { user_id, work, chunk } = await request.json();
      if (!user_id || !work || !chunk) return json({ error: 'missing fields' }, 400, cors);
      const id = 'b:' + crypto.randomUUID();
      await env.DB.prepare('INSERT OR IGNORE INTO bookmarks (id, user_id, work, chunk) VALUES (?, ?, ?, ?)')
        .bind(id, user_id, work, chunk).run();
      return json({ id }, 200, cors);
    }

    // GET /api/bookmarks/:user_id
    const bm = path.match(/^\/api\/bookmarks\/([^/]+)$/);
    if (bm && request.method === 'GET') {
      const [, userId] = bm;
      const { results } = await env.DB.prepare('SELECT * FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC')
        .bind(userId).all();
      return json({ bookmarks: results }, 200, cors);
    }

    // GET /api/debug/vectors — check vector loading
    if (path === '/api/debug/vectors' && request.method === 'GET') {
      const vecs = await getVectors(env);
      if (!vecs) return json({ error: 'vectors not loaded' }, 500, cors);
      const bh = vecs.filter(v => v.work === 'bhairavastava');
      return json({ total: vecs.length, bh: bh.length, sample: bh[0] ? { id: bh[0].id, en: (bh[0].en||'').slice(0,100) } : null }, 200, cors);
    }

    // POST /api/chat/:work — RAG chat
    const cm = path.match(/^\/api\/chat\/([^/]+)$/);
    if (cm && request.method === 'POST') {
      const [, workParam] = cm;
      const works = workParam.split(',').map(w => w.trim()).filter(Boolean);
      const { session_id, message, user_id } = await request.json();
      if (!message) return json({ error: 'message required' }, 400, cors);

      let sid = session_id;
      if (!sid) {
        sid = 's:' + crypto.randomUUID();
        await env.DB.prepare('INSERT INTO chat_sessions (id, user_id, work) VALUES (?, ?, ?)')
          .bind(sid, user_id || null, works[0]).run();
      }
      await env.DB.prepare('INSERT INTO chat_messages (id, session_id, role, content) VALUES (?, ?, ?, ?)')
        .bind('m:' + crypto.randomUUID(), sid, 'user', message).run();

      let reply = '';
      let retrievedIds = '[]';
      let retrievedGates = '[]';
      try {
        const qEmb = await env.AI.run('@cf/baai/bge-m3', { text: ['query: ' + message] });
        const qVec = qEmb.data[0];

        const vecs = await getVectors(env);
        if (!vecs) throw new Error('vectors not loaded');

        const gateWeight = { 'PUBLISHED': 1.0, 'PASS': 0.9, 'OWNER': 0.7, 'BLOCKED': 0.0 };
        const candidates = vecs
          .filter(v => works.includes(v.work) && (v.gate === 'PASS' || v.gate === 'PUBLISHED' || v.gate === 'OWNER'))
          .map(v => ({ ...v, score: cosine(qVec, v.vec) * (gateWeight[v.gate] || 0.5) }))
          .sort((a, b) => b.score - a.score)
          .slice(0, 20);

        // Template match: best pushing probe (chain context for Qwen)
        let chainCtx = '';
        try {
          const probes = vecs.filter(v => v.kind === 'probe');
          let best = null;
          for (const p of probes) {
            const s = cosine(qVec, p.vec);
            if (!best || s > best.score) best = { ...p, score: s };
          }
          if (best && best.score > 0.35) {
            chainCtx = `\n\nPrior enquiry on this question:\n[${best.id}] ${(best.en || '').slice(0, 800)}`;
          }
        } catch (e) { /* template match is best-effort */ }
        // Recorded hound verdicts (pushing INDEX): if the user asks something
        // a hound already asked, bring its verdict in as prior enquiry.
        try {
          const pidx = await getPushIndex(env);
          if (pidx && Array.isArray(pidx.records)) {
            const fold2 = s => (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
            const stop2 = new Set('what,which,who,whom,whose,when,where,why,does,doing,done,have,this,that,these,those,with,from,your,their,about,there,would,could,there,their,them,they,then,than,also,into,doesn,don,about,there,is,are,was,were,the,a,an,and,of,to,in,for,is,it,as,at,by,be,on,that,this'.split(','));
            const qt = new Set(fold2(message).split(/[^a-z]+/).filter(w => w.length >= 5 && !stop2.has(w)));
            let bestV = null;
            const flat = [];
            for (const r of pidx.records) for (const q of (r.questions || [])) flat.push({ r, q });
            for (const { r, q } of flat) {
              const qt2 = new Set(fold2(q.q || '').split(/[^a-z]+/).filter(w => w.length >= 5 && !stop2.has(w)));
              let n = 0; for (const t of qt) if (qt2.has(t)) n++;
              if (r.file && works.some(w => r.file.toLowerCase().includes(String(w).toLowerCase()))) n += 3;
              if (n >= 4 && (!bestV || n > bestV.n)) bestV = { n, r, q };
            }
            if (bestV) {
              chainCtx += `\n\nPrior hound verdict [pushing:${bestV.r.file}#${bestV.q.id}]: Q: ${bestV.q.q} / Verdict: ${bestV.q.verdict || 'open'} (commentary from a pushing session, not scripture)`;
            }
          }
        } catch (e) { /* verdict match is best-effort */ }

        // Diverse pick: best 1-2 per work, then rerank
        const byWork = {};
        for (const c of candidates) { (byWork[c.work] = byWork[c.work] || []).push(c); }
        let diverse = [];
        Object.values(byWork).forEach(arr => { diverse = diverse.concat(arr.slice(0, 4)); });
        diverse.sort((a, b) => b.score - a.score);
        let top = diverse.slice(0, 5);
        if (diverse.length > 5) {
          const ctxs = diverse.map(c => ({ text: (c.en || c.sa || '').slice(0, 500) || 'passage' }));
          const rerank = await env.AI.run('@cf/baai/bge-reranker-base', {
            query: message,
            contexts: ctxs,
          });
          const scores = rerank.results || rerank.data || [];
          diverse.forEach((c, i) => {
            c.rerank = (scores[i] && (scores[i].score || scores[i])) || c.score;
          });
          top = diverse.sort((a, b) => b.rerank - a.rerank).slice(0, 5);
        }

        // Graph traversal: follow argument packet edges
        const argPackets = vecs.filter(v => v.kind === 'argument');
        const gathered = new Set(top.map(t => t.id));
        // Lexical fallback: a distinctive query term in IAST or plain spelling
        // must hit records containing it, diacritics aside (bge can miss
        // samayajnam vs samayajñam). Gated the same as everything else.
        try {
          const fold = s => (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
          const stop = new Set(('what','which','who','whom','whose','when','where','why','does','doing','done','have','this','that','these','those','with','from','your','their','about','there','would','could','there','their','them','they','then','than','also','into','doesn','don','about').split(','));
          // work names never discriminate (the works filter already scopes by work);
          // matching them only lets 'bhairavastava' hit every 'bhairava' in the text
          const workToks = new Set(works.flatMap(w => fold(w).split(/[^a-z]+/).filter(Boolean)));
          const toks = [...new Set(fold(message).split(/[^a-z]+/).filter(w => w.length >= 5 && !stop.has(w) && ![...workToks].some(k => k && (w === k || w.includes(k)))))];
          if (toks.length) {
            const scored = [];
            for (const v of vecs) {
              if (!works.includes(v.work)) continue;
              if (!(v.gate === 'PASS' || v.gate === 'PUBLISHED' || v.gate === 'OWNER')) continue;
              const hay = fold((v.l3 || '') + ' ' + (v.en || '') + ' ' + (v.sa || ''));
              const hw = new Set(hay.split(/[^a-z]+/).filter(w => w.length >= 5));
              let n = 0;
              for (const t of toks) {
                for (const w of hw) { if (w.includes(t) || t.includes(w)) { n++; break; } }
              }
              if (n > 0) scored.push({ v, n });
            }
            scored.sort((a, b) => (b.n - a.n));
            for (const s of scored.slice(0, 5)) gathered.add(s.v.id);
          }
        } catch (e) { /* lexical fallback is best-effort */ }
        top.forEach(t => {
          argPackets.forEach(a => {
            if (a.ref === t.id || a.id.includes(t.id)) gathered.add(a.id);
          });
        });
        top.forEach(t => {
          argPackets.forEach(a => {
            if (a.tension_id && gathered.has(a.id)) {
              argPackets.forEach(a2 => {
                if (a2.tension_id === a.tension_id && a2.id !== a.id) gathered.add(a2.id);
              });
            }
          });
        });
        // Work-matched pushing sessions ride along as prior enquiry: a hound
        // session that names this work is relevant even when cosine is shy.
        // (Gated like everything else; cited as commentary, never as source.)
        try {
          const wprobes = vecs.filter(v => v.kind === 'probe' && works.some(w => (v.id || '').toLowerCase().includes(String(w).toLowerCase())));
          const wscored = wprobes.map(p => ({ p, s: cosine(qVec, p.vec) }));
          wscored.sort((a, b) => b.s - a.s);
          for (const w of wscored.slice(0, 2)) gathered.add(w.p.id);
        } catch (e) { /* work-matched probes are best-effort */ }

        const gatheredRecs = vecs.filter(v => gathered.has(v.id));
        // Direct references: if the question names chunk ids, include those
        // records — similarity alone can miss an explicitly named verse.
        try {
          const want = [...new Set((message.match(/[a-z0-9]+(?:-[a-z]+\d+(?:-v\d+)?)/gi) || []).map(s => s.toLowerCase()))].slice(0, 4);
          const norm = id => String(id || '').toLowerCase().split(/[:/]/).pop().replace(/\.(note|md)$/, '');
          if (want.length) {
            for (const v of vecs) {
              if (!works.includes(v.work)) continue;
              if (!(v.gate === 'PASS' || v.gate === 'PUBLISHED' || v.gate === 'OWNER')) continue;
              const cid = norm(v.id);
              if (cid && want.some(w => w === cid || w.endsWith(cid) || cid.endsWith(w))) gathered.add(v.id);
            }
            for (const t of [...gathered]) {
              for (const a of argPackets) {
                if (a.ref === t || a.id.includes(t)) gathered.add(a.id);
              }
            }
          }
        } catch (e) { /* direct-reference is best-effort */ }
        const contextRecs = vecs.filter(v => gathered.has(v.id));
        retrievedIds = JSON.stringify(contextRecs.map(t => t.id));
        retrievedGates = JSON.stringify(contextRecs.map(t => t.gate));
        const context = contextRecs.map(t => { const txt = t.l3 || t.en || t.sa || ''; return `[${t.id}] (work: ${t.work}, gate: ${t.gate}${t.l3 ? ', final translation' : ''}) ${txt}`; }).join('\n\n');
        const prompt = `You are a Trika Śaivism scholar answering inside a scripture reader. Never say 'the passages you've given me', 'supplied text', or anything that reveals retrieval; just answer.\n\nAnswer using ONLY the provided passages. Cite records by their [id] exactly as written (e.g. [bhairavastava:bh-p07]) — never by bare § numbers, never invent ids. If the answer is not in the passages: first, say what the passages DO establish that bears on it (one sentence, cited). Then, if it is stable background knowledge \u2014 authorship, dates, well-known figures, plain Sanskrit glosses, general Trika context \u2014 answer briefly from general knowledge, marked plainly as 'From general knowledge, not these verses:' and closed with 'Verify it against the texts.'. Never present general knowledge as coming from the passages. Never translate or interpret a verse whose English is withheld (gated/BLOCKED): for those, say the translation is not published here and stop. If the passages partly address it, say what they do establish and mark the remainder open \u2014 never fill gaps. Colophon verses (dates, authorship, composition circumstances) answer who/when questions — weigh them when present. Match Sanskrit terms across transliteration variants (\u00f1/n, \u015b/s, \u1e63/s, \u1e43/m, \u0101/a, \u012b/i, \u016b/u, \u1e25/h): a passage mentioning the term counts as addressing it even when the spelling differs.\n\nGate labels indicate trust level (PUBLISHED > PASS > OWNER). OWNER records are prior enquiries, not scripture — cite them as experienced commentary, never as source text.\n\nWrite as long as the question needs and no longer: plain speech, no academic jargon, no invented terms, no padding. No headers, no bold section labels, no bullet lists — plain sentences, then citations on their own final line. Never name the KIND of record you are using \u2014 no 'the C1', 'the NOTE', 'the commentary', 'the gloss', 'the argument', 'the pushing record', 'the note says'. Write as if you know the text directly ('Verse 1 bows with...'). The bracket citations carry all provenance; prose must contain zero source-talk. Reason step by step from the passages when the question is a why/how question; quote the key Sanskrit or English phrase you are standing on.\n\nPassages:\n${context}${chainCtx}\n\nQuestion: ${message}`;
        // Primary: Qwen3.8-Omni-Flash via DashScope. Fallback: deepseek via Workers AI.
        try {
          reply = await dashscopeChat(env, [{ role: 'user', content: prompt }], 512);
        } catch (qe) {
          const gen = await env.AI.run('@cf/deepseek-ai/deepseek-v4-flash', {
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 512,
          });
          const deep = gen && gen.choices && gen.choices[0] && gen.choices[0].message;
          reply = (deep && deep.content) || gen.response || (gen.result && gen.result.response) || 'No answer (both models failed).';
        }
      } catch (e) {
        reply = `RAG error: ${e.message}. Vectors: ${cachedVectors ? cachedVectors.length : 'none'}.`;
      }

      await env.DB.prepare('INSERT INTO chat_messages (id, session_id, role, content) VALUES (?, ?, ?, ?)')
        .bind('m:' + crypto.randomUUID(), sid, 'assistant', reply).run();
      // store question record with reply (for pushing corpus growth)
      try {
        const qid = 'q:' + crypto.randomUUID();
        await env.DB.prepare('INSERT INTO questions (id, session_id, work, message, reply, retrieved_ids, gate_labels) VALUES (?, ?, ?, ?, ?, ?, ?)')
          .bind(qid, sid, works[0], message, reply, retrievedIds, retrievedGates).run();
      } catch (e) { /* question storage is best-effort */ }
      // proactive follow-up suggestion
      let suggestion = '';
      try {
        const followup = await dashscopeChat(env, [{ role: 'user', content: `Given this Q&A about ${works.join(', ')}:\nQ: ${message}\nA: ${reply.slice(0,300)}\n\nSuggest one follow-up question in plain speech that the retrieved passages could answer or that opens their hardest unresolved tension. No scholar names, no academic jargon, just the question. Nothing else.` }], 64);
        if (followup && followup.length > 5 && followup.length < 300) suggestion = followup.trim();
      } catch (e) { /* proactive is best-effort */ }
      return json({ session_id: sid, reply, suggestion }, 200, cors);
    }

    // GET /api/chat/:session_id/history
    const ch = path.match(/^\/api\/chat\/([^/]+)\/history$/);
    if (ch && request.method === 'GET') {
      const [, sid] = ch;
      const { results } = await env.DB.prepare('SELECT role, content, created_at FROM chat_messages WHERE session_id = ? ORDER BY created_at')
        .bind(sid).all();
      return json({ messages: results }, 200, cors);
    }


    // POST /api/themes/decide — accept/reject/merge/split a cluster
    const td = path.match(/^\/api\/themes\/decide$/);
    if (td && request.method === 'POST') {
      const { cluster_id, decision, user_id, note } = await request.json();
      if (!cluster_id || !decision) return json({ error: 'cluster_id and decision required' }, 400, cors);
      const id = 'td:' + crypto.randomUUID();
      // store in a simple key-value via D1 (we'll use a decisions table)
      await env.DB.prepare('CREATE TABLE IF NOT EXISTS theme_decisions (id TEXT PRIMARY KEY, cluster_id TEXT, decision TEXT, user_id TEXT, note TEXT, created_at TEXT)').run();
      await env.DB.prepare('INSERT INTO theme_decisions (id, cluster_id, decision, user_id, note) VALUES (?, ?, ?, ?, ?)')
        .bind(id, cluster_id, decision, user_id || null, note || null).run();
      return json({ id, cluster_id, decision }, 200, cors);
    }

    // GET /api/themes/decisions — list all decisions
    if (path === '/api/themes/decisions' && request.method === 'GET') {
      await env.DB.prepare('CREATE TABLE IF NOT EXISTS theme_decisions (id TEXT PRIMARY KEY, cluster_id TEXT, decision TEXT, user_id TEXT, note TEXT, created_at TEXT)').run();
      const { results } = await env.DB.prepare('SELECT * FROM theme_decisions ORDER BY created_at DESC').all();
      return json({ decisions: results }, 200, cors);
    }

    // POST /api/style/preview — A3S-style instant preview (prompt-based, free-tier)
    if (path === '/api/style/preview' && request.method === 'POST') {
      const { exemplars, source, model } = await request.json();
      if (!exemplars || !source) return json({ error: 'exemplars and source required' }, 400, cors);
      const ex = Array.isArray(exemplars) ? exemplars.join('\n---\n') : exemplars;
      const prompt = `You are a style transfer engine. Given these example translations in the target style:\n\n${ex}\n\nRewrite the following Sanskrit passage in the same style. Preserve meaning exactly. Only change register/diction.\n\nSource (Sanskrit): ${source}\n\nStyled translation:`;
      try {
        let styled = '';
        try {
          styled = await dashscopeChat(env, [{ role: 'user', content: prompt }], 512);
        } catch (e2) {
          const gen = await env.AI.run(model || '@cf/deepseek-ai/deepseek-v4-flash', {
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 512,
          });
          styled = gen.response || gen.result?.response || gen.choices?.[0]?.message?.content || '';
        }
        return json({ styled, model: 'qwen3.8-omni-flash' }, 200, cors);
      } catch (e) {
        return json({ error: e.message }, 500, cors);
      }
    }

    // POST /api/c2/render — C2 styled rendition, grounded on the canonical packet.
    // implements skills/render-c2: PASS-only, meaning locked to L1/L2/C1, style is diction only.
    if (path === '/api/c2/render' && request.method === 'POST') {
      const { work, chunk, style, model } = await request.json();
      const st = String(style || '').trim().slice(0, 60);
      if (!work || !chunk || !st) return json({ error: 'work, chunk and style (1-60 chars) required' }, 400, cors);
      if (!/^[a-zA-Z0-9 _-]+$/.test(work) || !/^[a-zA-Z0-9 _-]+$/.test(chunk)) return json({ error: 'bad work/chunk' }, 400, cors);
      let packet = null;
      try {
        const lr = await fetch('https://ipvv-a8u.pages.dev/data/layers/' + work + '.json');
        if (!lr.ok) return json({ error: 'work not on file: ' + work }, 404, cors);
        const layers = await lr.json();
        packet = (layers.chunks || []).find(c => c.chunk === chunk);
      } catch (e) {
        return json({ error: 'canonical fetch failed: ' + e.message }, 502, cors);
      }
      if (!packet) return json({ error: 'chunk not on file: ' + chunk }, 404, cors);
      if (packet.gate !== 'PASS') return json({ error: 'English withheld — gate ' + (packet.gate || 'BLOCKED') }, 422, cors);
      // claim skeleton: structured arguments packet where the build ships one
      let argBlock = '', openBlock = '';
      try {
        const ar = await fetch('https://ipvv-a8u.pages.dev/data/arguments/' + work + '-' + chunk + '.json');
        if (ar.ok) {
          const ap = await ar.json();
          const prems = (ap.premises || []).map(p => '- ' + String(p.text || '').replace(/\s+/g, ' ').trim().slice(0, 300)).join('\n');
          argBlock = 'Question: ' + String(ap.question || '').replace(/\s+/g, ' ').trim().slice(0, 400)
            + '\nPremises:\n' + (prems || '- (none listed)') + '\nConclusion: '
            + String((ap.conclusion && ap.conclusion.text) || ap.conclusion || '').replace(/\s+/g, ' ').trim().slice(0, 400);
          const un = Array.isArray(ap.unresolved) ? ap.unresolved.join('; ') : String(ap.unresolved || '');
          if (un.trim()) openBlock = un.replace(/\s+/g, ' ').trim().slice(0, 400);
        }
      } catch (e) { /* arguments packet optional — layers packet is the floor */ }
      const trim = (s, n) => String(s || '').replace(/^#+\s*[^\n]*\n/, '').replace(/\s+/g, ' ').trim().slice(0, n);
      // House modes × registers: style may name a mode (precise/hype/prayer) and/or a
      // register (roadman/gen-z). Both are parsed and combined; registers never blend.
      const MODES = {
        precise: 'MODE precise: every proposition must stay checkable against L1. Slang only where mapped, zero decoration. The default for teaching.',
        hype: 'MODE hype: maximum energy, meaning locked. Every Sanskrit term translated in-line, never left standing. No filler transitions. Completed states stay completed (was, never becoming).',
        prayer: 'MODE prayer: devotional tenderness first. Slang softens, never jokes at the verse\'s expense. Rasa forward, claims intact.',
      };
      const REGISTERS = {
        roadman: 'REGISTER roadman (UK): mandem/fam/bruv, wallahi or swear down for oaths (never both), innit/dun know tags, allow it/dead/peak/cook/bless up/lengest. US ballroom terms (ate/no crumbs, bussin as default, clocking as slang) stay OUT. Translate every Sanskrit term in-line.',
        genz: 'REGISTER gen-z (US): no cap/fr, canon event, bussin, giving, delulu, ate/no crumbs, clocked. UK roadman terms (mandem, wallahi, innit, allow it, lengest, bless up, wasteman) stay OUT. Translate every Sanskrit term in-line.',
      };
      const slow = String(st).toLowerCase();
      const modeLine = [MODES.precise && slow.includes('precise') ? MODES.precise : '', MODES.hype && slow.includes('hype') ? MODES.hype : '', MODES.prayer && slow.includes('prayer') ? MODES.prayer : ''].filter(Boolean).join('\n');
      const regLine = [(slow.includes('roadman') ? REGISTERS.roadman : ''), (slow.includes('gen z') || slow.includes('genz')) ? REGISTERS.genz : ''].filter(Boolean).join('\n');
      const styleLine = (modeLine + '\n' + regLine).trim();
      const prompt = 'You render verses into a requested voice. Meaning is FIXED by the canonical packet below — every floor of the translation stack stands behind it. Change diction and rhythm only.\n\n'
        + 'Source (Sanskrit): ' + trim(packet.sanskrit, 600) + '\n'
        + 'Load-bearing propositions, L1 — every one must survive: ' + trim(packet.l1, 800) + '\n'
        + 'Resolved reading, L2: ' + trim(packet.l2, 800) + '\n'
        + 'Commentary — what it means, C1: ' + (trim(packet.c1, 800) || 'none on file — stay inside L1/L2') + '\n'
        + 'Claim skeleton:\n' + (argBlock || trim(packet.argmap, 1200) || 'none') + '\n'
        + 'Open points — hedge in-voice or omit, never close: ' + (openBlock || 'none listed') + '\n'
        + 'Contested readings: none on file for this work — never present uncertain readings as certain.\n\n'
        + 'First, in one silent line, name this verse\'s rasa: what must the reader feel. That line never ships.\n'
        + 'Then render.\n\n'
        + 'Voice: ' + st + '\n'
        + (modeLine ? modeLine + '\n' : '')
        + 'Rules: 2–6 sentences. Same claims, same savor, new voice. NO SANSKRIT except these exact names: Bhairava, Śaṅkara, Maheśa, Abhinavagupta, Pauṣa, samaya, Śiva. Every other Sanskrit word must appear in English — never transliterate-and-leave, never Devanagari script. No new doctrine, no new names, no preaching, no second verse. If a claim won\'t fit the voice, say it plainly. Never output the rasa line or any scaffolding — rendition only, no meta-commentary.\n\nRendition:';
      try {
        let c2 = '', used = '';
        try {
          c2 = await dashscopeChat(env, [{ role: 'user', content: prompt }], 350);
          used = 'qwen3.8-omni-flash';
        } catch (e2) {
          const gen = await env.AI.run(model || '@cf/deepseek-ai/deepseek-v4-flash', {
            messages: [{ role: 'user', content: prompt }],
            max_tokens: 350,
          });
          c2 = gen.response || gen.result?.response || gen.choices?.[0]?.message?.content || '';
          used = model || '@cf/deepseek-ai/deepseek-v4-flash';
        }
        if (!c2.trim()) return json({ error: 'empty rendering' }, 502, cors);
        return json({ c2: c2.trim(), style: st, model: used,
          provenance: { work, chunk, gate: 'PASS', date: new Date().toISOString().slice(0, 10) },
          label: 'machine rendering' }, 200, cors);
      } catch (e) {
        return json({ error: e.message }, 500, cors);
      }
    }

    // POST /api/c2/verify — MIS-style bidirectional entailment + validated-vocabulary check.
    // forward: canonical packet entails C2 (nothing added). backward: C2 entails L1 props (nothing lost).
    // Implements skills/render-c2 § verification; cf. Babakov et al. 2022 (MIS), 2025 meta-eval (style-aware only).
    // Validated voice vocabulary only: slang-glossary USE verdicts + Toronto-shared-with-MLE + MLE core.
    // Anything outside this set in a rendering gets reported (not failed) for curator review.
    const VOICE_WHITELIST = new Set(("locked standing business cap canon cooked ate crumbs bussin giving lore tapped delulu clocked clocking aura mandem fam brudda leng peng lengest allow bare bruv duppy gassed innit dun know bless shook patterned valid lowkey highkey twin unc ghost ghosted chill vibe vibes rizz bet slay period ohio skibidi gyatt fanum kai cenat say wallahi blud wasteman bait long moist rent-free").split(" ").filter(w => w.length > 2));
    if (path === '/api/c2/verify' && request.method === 'POST') {
      const { work, chunk, c2, style } = await request.json();
      if (!work || !chunk || !c2) return json({ error: 'work, chunk and c2 required' }, 400, cors);
      let packet = null;
      try {
        const lr = await fetch('https://ipvv-a8u.pages.dev/data/layers/' + work + '.json');
        if (!lr.ok) return json({ error: 'work not on file: ' + work }, 404, cors);
        const layers = await lr.json();
        packet = (layers.chunks || []).find(c => c.chunk === chunk);
      } catch (e) {
        return json({ error: 'canonical fetch failed: ' + e.message }, 502, cors);
      }
      if (!packet) return json({ error: 'chunk not on file: ' + chunk }, 404, cors);
      const trim = (s, n) => String(s || '').replace(/^#+\s*[^\n]*\n/, '').replace(/\s+/g, ' ').trim().slice(0, 900);
      let argBlock = '';
      try {
        const ar = await fetch('https://ipvv-a8u.pages.dev/data/arguments/' + work + '-' + chunk + '.json');
        if (ar.ok) { const ap = await ar.json();
          argBlock = 'Claim skeleton: ' + trim(ap.question, 300) + ' // ' + trim((ap.conclusion && ap.conclusion.text) || ap.conclusion, 400); }
      } catch (e) {}
      const judgePrompt = 'You audit a styled rendition against its canonical packet. Two entailment checks.\n'
        + 'JUDGING RULES: (1) Sincerity/discourse markers (no cap, fr, innit, wallahi, bet, no crumbs as completion) are voice devices, NOT propositions — never list them as added. (2) A title may ride on the bare name where the referent is unambiguous — list as missing only if lordship/refuge-status is denied or lost. (3) C1 commentary is canon: anything C1 states explicitly may appear in the candidate.\n\n'
        + 'CANON (L1 propositions — every one must survive): ' + trim(packet.l1, 1200) + '\n'
        + 'CANON (L2 resolved reading): ' + trim(packet.l2, 1200) + '\n'
        + 'CANON (C1 commentary — explicit statements are licensed): ' + (trim(packet.c1, 900) || 'none') + '\n'
        + 'CANON (claim skeleton): ' + (argBlock || trim(packet.argmap, 600) || 'none') + '\n'
        + 'CANDIDATE (' + String(style || 'styled') + ' rendition): ' + String(c2).replace(/\s+/g, ' ').trim().slice(0, 1500) + '\n\n'
        + 'Answer ONLY this JSON, no other text: {"forward_pass": true/false (canon entails candidate — nothing added), "backward_pass": true/false (candidate entails every L1 proposition — nothing lost), "added": ["claims in candidate with no canon basis"], "missing": ["L1 propositions absent from candidate"], "note": "one line"}';
      try {
        let raw = '';
        try { raw = await dashscopeChat(env, [{ role: 'user', content: judgePrompt }], 400); }
        catch (e2) {
          const gen = await env.AI.run('@cf/deepseek-ai/deepseek-v4-flash', {
            messages: [{ role: 'user', content: judgePrompt }], max_tokens: 400,
          });
          raw = gen.response || gen.choices?.[0]?.message?.content || '';
        }
        const m = raw.match(/\{[\s\S]*\}/);
        if (!m) throw new Error('no JSON from judge');
        const j = JSON.parse(m[0]);
        const words = String(c2).toLowerCase().replace(/[^a-z0-9' -]/g, ' ').split(/\s+/).filter(w => w.length > 2);
        const NAMES = new Set(['bhairava','śaṅkara','sankara','maheśa','mahesa','śiva','siva','abhinavagupta','pauṣa','pausa','samaya']);
        const deva = /[\u0900-\u097F]/.test(c2);
        const rawToks = String(c2).split(/\s+/).map(t => t.replace(/^["'“‘(\[]+|["'”’).,!?:;\]]+$/g, ''));
        const leaked = [...new Set(rawToks.filter(t => /[āīūṛṝḷēōṃḥṅñṭḍṇśṣĀĪŪṚṜḶĒŌṀḤṄÑṬḌṆŚṢ]/.test(t) && !NAMES.has(t.toLowerCase())))];
        // source-echo check: any long token from the Sanskrit span reappearing in C2
        // (diacritics-insensitive) is untranslated Sanskrit, even in plain ascii.
        const norm = w => String(w).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z]/g, '');
        const STOP = new Set(['that','this','with','from','your','have','what','when','they','them','then','than','about','into','over','under','there','their','been','were','will','would','could','should','mind','heart','still','every','never','always','where','while','which','whom','whose']);
        const srcToks = [...new Set(String(packet.sanskrit || '').split(/\s+/).map(norm).filter(w => w.length >= 5))];
        const c2norm = String(c2).split(/\s+/).map(t => norm(t.replace(/^["'“‘(\[]+|["'”’).,!?:;\]]+$/g, '')));
        const echo = [...new Set(c2norm.filter(w => w.length >= 5 && !STOP.has(w) && !NAMES.has(w) && srcToks.some(st => st.includes(w) || w.includes(st) && Math.min(st.length, w.length) >= 5)))];
        const allLeaked = [...new Set([...leaked, ...echo])];
        const leakFound = deva || allLeaked.length > 0;
        const glossaryHits = [...new Set(words.filter(w => VOICE_WHITELIST.has(w)))];
        const verdict = (j.forward_pass && j.backward_pass && !leakFound) ? 'PASS' : 'FLAG';
        return json({ verdict, forward_entails: !!j.forward_pass, backward_entails: !!j.backward_pass,
          added: j.added || [], missing: j.missing || [], note: j.note || '',
          voice_words: glossaryHits,
          sanskrit_leak: leakFound ? { devanagari: deva, tokens: allLeaked } : null,
          provenance: { work, chunk, gate: packet.gate, date: new Date().toISOString().slice(0, 10) } }, 200, cors);
      } catch (e) {
        return json({ error: e.message }, 500, cors);
      }
    }

    // GET /api/questions/:work — list stored questions for a work
    const qm = path.match(/^\/api\/questions\/([^/]+)$/);
    if (qm && request.method === 'GET') {
      const [, work] = qm;
      const { results } = await env.DB.prepare('SELECT id, message, reply, retrieved_ids, gate_labels, created_at FROM questions WHERE work = ? ORDER BY created_at DESC LIMIT 50')
        .bind(work).all();
      return json({ questions: results }, 200, cors);
    }

    // GET /api/questions — list all questions
    // ---- scholar auth: local signup/login + signed session cookie (phase 1) ----
    const COOKIE = 'svsess=';
    const b64u = b => btoa(String.fromCharCode(...new Uint8Array(b)))
      .replace(/=+$/,'').replace(/\+/g,'-').replace(/\//g,'_');
    const unb64u = s => { s=s.replace(/-/g,'+').replace(/_/g,'/');
      const bin=atob(s.padEnd(s.length+(4-s.length%4)%4,'='));
      return new Uint8Array([...bin].map(c=>c.charCodeAt(0))); };
    const hex = u8 => [...u8].map(b=>b.toString(16).padStart(2,'0')).join('');
    const unhex = h => new Uint8Array((h.match(/../g)||[]).map(x=>parseInt(x,16)));
    async function pwHash(pw, saltHex){
      const salt = saltHex ? unhex(saltHex) : crypto.getRandomValues(new Uint8Array(16));
      const bits = await crypto.subtle.deriveBits(
        {name:'PBKDF2', salt, iterations:100000, hash:'SHA-256'},
        await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveBits']), 256);
      return {hash: b64u(bits), salt: hex(salt)};
    }
    async function signTok(uid, exp){
      const body = btoa(JSON.stringify({u:uid, e:exp}));
      const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(env.SESSION_SECRET||''), {name:'HMAC', hash:'SHA-256'}, false, ['sign']);
      return body + '.' + b64u(await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(body)));
    }
    async function sessUid(request){
      try{
        const ck = request.headers.get('Cookie')||'';
        const tok = ck.split(';').map(x=>x.trim()).find(x=>x.startsWith(COOKIE));
        if(!tok) return null;
        const [body, sig] = tok.slice(COOKIE.length).split('.');
        const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(env.SESSION_SECRET||''), {name:'HMAC', hash:'SHA-256'}, false, ['verify']);
        const ok = await crypto.subtle.verify('HMAC', key, unb64u(sig), new TextEncoder().encode(body));
        if(!ok) return null;
        const p = JSON.parse(atob(body));
        if(p.e < Date.now()) return null;
        return p.u;
      }catch(e){ return null; }
    }

    if (path.startsWith('/api/scholar/')) {
      if (reqOrigin && !allowed.has(reqOrigin)) return json({error:'origin not allowed'},403,cors);
      if (typeof env.SESSION_SECRET !== 'string' || env.SESSION_SECRET.length < 32)
        return json({error:'authentication temporarily unavailable'},503,cors);
      const uid=await sessUid(request);
      if (!uid) return new Response(JSON.stringify({error:'sign in required'}),{status:401,
        headers:{...cors,'Content-Type':'application/json','Cache-Control':'no-store'}});
      return handleScholar(request,env,uid,cors,(messages,maxTokens,signal)=>dashscopeChat(
        {DASHSCOPE_API_KEY:env.SCHOLAR_DASHSCOPE_API_KEY},messages,maxTokens,signal));
    }

    // POST /api/auth/access — join or sign in. Legacy email-only profiles need
    // an ownership-verification flow before a password can be attached.
    if (path === '/api/auth/access' && request.method === 'POST') {
      let b = {}; try { b = await request.json(); } catch(e) {}
      const email = String(b.email||'').trim().toLowerCase();
      const pw = String(b.password||'');
      const name = String(b.name||'').trim().slice(0,80);
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({error:'valid email required'}, 400, cors);
      if(pw.length < 8) return json({error:'password must be at least 8 characters'}, 400, cors);
      let row = (await env.DB.prepare('SELECT * FROM profiles WHERE email = ?').bind(email).first());
      if(row && row.password_hash){
        const {hash} = await pwHash(pw, row.salt);
        if(hash !== row.password_hash) return json({error:'wrong password'}, 401, cors);
      } else {
        if(row) return json({error:'This existing profile requires email verification before it can be claimed.'}, 409, cors);
        const {hash, salt} = await pwHash(pw, null);
        const uid = crypto.randomUUID();
        await env.DB.prepare('INSERT INTO profiles (id, email, password_hash, salt, display_name, provider) VALUES (?,?,?,?,?,?)')
          .bind(uid, email, hash, salt, name || email.split('@')[0], 'local').run();
        row = {id: uid, display_name: name || email.split('@')[0]};
      }
      const exp = Date.now() + 7*24*3600*1000;
      const tok = await signTok(row.id, exp);
      const prof = await env.DB.prepare('SELECT id, email, display_name, orcid, provider FROM profiles WHERE id = ?').bind(row.id).first();
      return new Response(JSON.stringify({profile: prof}), {status: 200, headers: {
        ...cors, 'Content-Type': 'application/json', 'Cache-Control': 'no-store',
        'Set-Cookie': `svsess=${tok}; HttpOnly; Secure; SameSite=None; Path=/; Max-Age=${7*24*3600}`}});
    }

    // POST /api/auth/google — sign in with the shared satsang-auth service.
    // The client never proves identity itself: we verify its bearer token
    // against auth.tantrafiles.xyz/v1/me (server-to-server), then mint our own
    // svsess for the profile keyed by that opaque uid. Pass {link:true} while
    // already signed in to attach Google to the current account instead.
    if (path === '/api/auth/google' && request.method === 'POST') {
      let b = {}; try { b = await request.json(); } catch(e) {}
      const access = String(b.access||'');
      if (access.length < 20 || access.length > 4096) return json({error:'google access token required'}, 400, cors);
      let me = null;
      try {
        const r = await fetch('https://auth.tantrafiles.xyz/v1/me', {
          headers: {authorization: 'Bearer ' + access}, cf: {cacheTtl: 0}});
        if (r.ok) me = await r.json();
      } catch(e) { me = null; }
      if (!me || !/^u_[A-Za-z0-9_-]{8,48}$/.test(String(me.uid||'')))
        return json({error:'that Google session could not be verified'}, 401, cors);
      const gid = String(me.uid);
      const handle = String(me.handle||'').slice(0,40) || 'learner';
      let row = null;
      if (b.link) {
        const cur = await sessUid(request);
        if (!cur) return json({error:'sign in to this account first, then link Google'}, 401, cors);
        const other = await env.DB.prepare('SELECT id FROM profiles WHERE auth_uid = ?').bind(gid).first();
        if (other && other.id !== cur) return json({error:'that Google account is already linked to another profile'}, 409, cors);
        await env.DB.prepare('UPDATE profiles SET auth_uid = ? WHERE id = ?').bind(gid, cur).run();
        row = {id: cur};
      } else {
        row = await env.DB.prepare('SELECT id FROM profiles WHERE auth_uid = ?').bind(gid).first();
        if (!row) {
          const id = crypto.randomUUID();
          try {
            await env.DB.prepare('INSERT INTO profiles (id, email, display_name, provider, auth_uid) VALUES (?,?,?,?,?)')
              .bind(id, null, handle, 'google', gid).run();
            row = {id};
          } catch(e) {
            row = await env.DB.prepare('SELECT id FROM profiles WHERE auth_uid = ?').bind(gid).first();
          }
        }
      }
      if (!row) return json({error:'could not create the profile'}, 500, cors);
      const exp = Date.now() + 7*24*3600*1000;
      const tok = await signTok(row.id, exp);
      const prof = await env.DB.prepare('SELECT id, email, display_name, orcid, provider FROM profiles WHERE id = ?').bind(row.id).first();
      return new Response(JSON.stringify({profile: prof}), {status: 200, headers: {
        ...cors, 'Content-Type': 'application/json', 'Cache-Control': 'no-store',
        'Set-Cookie': `svsess=${tok}; HttpOnly; Secure; SameSite=None; Path=/; Max-Age=${7*24*3600}`}});
    }

    // GET /api/auth/me
    if (path === '/api/auth/me' && request.method === 'GET') {
      const uid = await sessUid(request);
      if(!uid) return new Response(JSON.stringify({profile:null}),{status:200,headers:{...cors,'Content-Type':'application/json','Cache-Control':'no-store'}});
      const prof = await env.DB.prepare('SELECT id, email, display_name, orcid, provider FROM profiles WHERE id = ?').bind(uid).first();
      return new Response(JSON.stringify({profile:prof||null}),{status:200,headers:{...cors,'Content-Type':'application/json','Cache-Control':'no-store'}});
    }

    // ---- Wheel gate: server-scored, anti-cheat ----
    // The pool (data/wheels/gates.json) is public: reading it is studying.
    // The server samples 20 items (half current stage, half earlier),
    // shuffles options per item, holds the key, scores, and writes the unlock.
    // Signed-out users keep local scoring, labelled unverified.
    const GATE_MAX = {word: 4, sentence: 3};
    const GATE_N = 20, GATE_PASS = 18, GATE_TTL_MS = 600*1000;
    let POOL_CACHE = null;
    async function loadGatePool(env){
      const now = Date.now();
      if (POOL_CACHE && now - POOL_CACHE.at < 3600*1000) return POOL_CACHE.data;
      const url = env.GATE_POOLS_URL || 'https://svatantrya.net/data/wheels/gates.json';
      const r = await fetch(url, {cf:{cacheTtl:3600}});
      if(!r.ok) throw new Error('pool unreachable');
      const doc = await r.json();
      if(!doc || doc.format !== 'svatantrya.gate-pools/1' || !doc.curricula) throw new Error('bad pool');
      POOL_CACHE = {data: doc, at: now};
      return doc;
    }
    function gateUid(request){
      try{
        const ck = request.headers.get('Cookie')||'';
        let tok = null;
        const ckTok = ck.split(';').map(x=>x.trim()).find(x=>x.startsWith(COOKIE));
        if(ckTok) tok = ckTok.slice(COOKIE.length);
        else { const ah = request.headers.get('Authorization')||''; const m = /^Bearer\s+(.+)$/.exec(ah); if(m) tok = m[1]; }
        if(!tok) return Promise.resolve(null);
        return sessUid(new Request('https://gate.local/', {headers:{Cookie: COOKIE + tok}}));
      }catch(e){ return Promise.resolve(null); }
    }
    function gateRand(n){
      const b = crypto.getRandomValues(new Uint32Array(1));
      return Number(BigInt(b[0]) % BigInt(Math.max(1, n)));
    }
    function gateShuffle(arr){
      const a = arr.slice();
      for(let i=a.length-1;i>0;i--){ const j = gateRand(i+1); const t=a[i]; a[i]=a[j]; a[j]=t; }
      return a;
    }

    if (path === '/api/wheel/gate/start' && request.method === 'POST') {
      let b = {}; try{ b = await request.json(); }catch(e){}
      const uid = await gateUid(request);
      if(!uid) return json({error:'sign in to take a scored gate; local practice still works on the site'}, 401, cors);
      if(reqOrigin && !allowed.has(reqOrigin)) return json({error:'origin not allowed'}, 403, cors);
      const curriculum = String(b.curriculum||'');
      const stage = Number(b.stage);
      if(!['word','sentence'].includes(curriculum)) return json({error:'curriculum must be word|sentence'}, 400, cors);
      try{
        const pool = await loadGatePool(env);
        const cur = pool.curricula[curriculum];
        if(!cur || !cur.stages[String(stage)]) return json({error:'unknown stage'}, 400, cors);
        let prog = await env.DB.prepare('SELECT stage FROM learner_progress WHERE user_id = ? AND curriculum = ?').bind(uid, curriculum).first();
        if(!prog){ await env.DB.prepare('INSERT INTO learner_progress (user_id, curriculum, stage) VALUES (?,?,1)').bind(uid, curriculum).run(); prog = {stage: 1}; }
        if(curriculum === 'sentence'){
          const wp = await env.DB.prepare('SELECT stage FROM learner_progress WHERE user_id = ? AND curriculum = ?').bind(uid, 'word').first();
          if(!wp || Number(wp.stage) <= GATE_MAX.word) return json({error:'finish the word circle first'}, 403, cors);
        }
        if(stage > Number(prog.stage)) return json({error:'that layer is still locked; pass the current one first', stage: prog.stage}, 403, cors);
        if(stage > GATE_MAX[curriculum]) return json({error:'curriculum complete'}, 400, cors);
        const recent = await env.DB.prepare("SELECT COUNT(*) AS n FROM learner_attempts WHERE user_id = ? AND curriculum = ? AND created_at > datetime('now','-1 hour')").bind(uid, curriculum).first();
        if(recent && Number(recent.n) >= 3) return json({error:'three scored attempts per hour; practice freely and come back'}, 429, cors);
        const cur_items = cur.stages[String(stage)].items;
        const prev_items = [];
        for(const k of Object.keys(cur.stages)){ if(Number(k) < stage) prev_items.push(...cur.stages[k].items); }
        const shuffledCur = gateShuffle(cur_items), shuffledPrev = gateShuffle(prev_items);
        const picked = [];
        const wantCur = Math.ceil(GATE_N/2);
        const poolPrev = shuffledPrev.length ? shuffledPrev : shuffledCur;
        for(let i=0; picked.length < wantCur && shuffledCur.length; i++) picked.push(shuffledCur[i % shuffledCur.length]);
        for(let i=0; picked.length < GATE_N; i++) picked.push(poolPrev[i % poolPrev.length]);
        const items = gateShuffle(picked).slice(0, GATE_N).map((it, idx)=>({
          item_id: it.id, prompt: it.prompt,
          options: gateShuffle(it.options),
        }));
        const key = {};
        for(const it of items){
          const full = [...cur_items, ...prev_items].find(x=>x.id===it.item_id) || cur_items.find(x=>x.id===it.item_id);
          key[it.item_id] = full ? full.answer : null;
        }
        const sid = crypto.randomUUID();
        const now = Date.now();
        await env.DB.prepare('INSERT INTO gate_sessions (id, user_id, curriculum, stage, items_json, key_json, expires_at, created_at) VALUES (?,?,?,?,?,?,?,?)')
          .bind(sid, uid, curriculum, stage, JSON.stringify(items), JSON.stringify(key), now + GATE_TTL_MS, now).run();
        return json({session_id: sid, curriculum, stage, n: items.length, pass_mark: GATE_PASS, items}, 200, cors);
      }catch(e){ return json({error:'gate unavailable right now'}, 503, cors); }
    }

    if (path === '/api/wheel/gate/submit' && request.method === 'POST') {
      let b = {}; try{ b = await request.json(); }catch(e){}
      const uid = await gateUid(request);
      if(!uid) return json({error:'sign in to take a scored gate'}, 401, cors);
      if(reqOrigin && !allowed.has(reqOrigin)) return json({error:'origin not allowed'}, 403, cors);
      const sid = String(b.session_id||'');
      const sess = sid ? await env.DB.prepare('SELECT * FROM gate_sessions WHERE id = ?').bind(sid).first() : null;
      if(!sess || sess.user_id !== uid) return json({error:'unknown session'}, 404, cors);
      if(Number(sess.used)) return json({error:'session already submitted'}, 409, cors);
      if(Date.now() > Number(sess.expires_at)) return json({error:'session expired; start a fresh gate'}, 410, cors);
      await env.DB.prepare('UPDATE gate_sessions SET used = 1 WHERE id = ?').bind(sid).run();
      const items = JSON.parse(sess.items_json||'[]');
      const key = JSON.parse(sess.key_json||'{}');
      const given = {};
      for(const a of (Array.isArray(b.answers)?b.answers:[])){
        if(a && typeof a.item_id==='string' && typeof a.choice==='string') given[a.item_id] = a.choice;
      }
      let correct = 0;
      const detail = items.map(it=>{ const ok = given[it.item_id] === key[it.item_id]; if(ok) correct++; return {item_id: it.item_id, ok}; });
      const passed = correct >= GATE_PASS;
      const curriculum = sess.curriculum, stage = Number(sess.stage);
      await env.DB.prepare('INSERT INTO learner_attempts (id, user_id, curriculum, stage, items_json, answers_json, score, passed) VALUES (?,?,?,?,?,?,?,?)')
        .bind(crypto.randomUUID(), uid, curriculum, stage, sess.items_json, JSON.stringify(given), correct, passed?1:0).run();
      let unlock = null;
      if(passed){
        const prog = await env.DB.prepare('SELECT stage, passed_json, items_json FROM learner_progress WHERE user_id = ? AND curriculum = ?').bind(uid, curriculum).first();
        const cur = prog ? Number(prog.stage) : 1;
        if(stage >= cur && stage <= GATE_MAX[curriculum]){
          const passed = prog ? JSON.parse(prog.passed_json||'[]') : [];
          passed.push({stage, score: correct, at: new Date().toISOString()});
          const agg = prog ? JSON.parse(prog.items_json||'{}') : {};
          for(const d of detail){ const e = agg[d.item_id] || {seen:0, right:0}; e.seen++; if(d.ok) e.right++; agg[d.item_id]=e; }
          await env.DB.prepare('UPDATE learner_progress SET stage = ?, passed_json = ?, items_json = ?, updated_at = datetime("now") WHERE user_id = ? AND curriculum = ?')
            .bind(stage+1, JSON.stringify(passed), JSON.stringify(agg), uid, curriculum).run();
          unlock = {next_stage: stage+1, done: stage+1 > GATE_MAX[curriculum]};
        }
      }
      return json({score: correct, total: items.length, passed, pass_mark: GATE_PASS, unlock, detail}, 200, cors);
    }

    // GET /api/wheel/progress — own progress (for the site + ChatGPT)
    if (path === '/api/wheel/progress' && request.method === 'GET') {
      const uid = await gateUid(request);
      if(!uid) return json({error:'sign in to read progress'}, 401, cors);
      if(reqOrigin && !allowed.has(reqOrigin)) return json({error:'origin not allowed'}, 403, cors);
      const rows = await env.DB.prepare('SELECT curriculum, stage, passed_json FROM learner_progress WHERE user_id = ?').bind(uid).all();
      return json({progress: (rows.results||[]).map(r=>({curriculum:r.curriculum, stage:r.stage, passed:JSON.parse(r.passed_json||'[]')}) )}, 200, cors);
    }

    // POST /api/auth/logout
    if (path === '/api/auth/logout' && request.method === 'POST') {
      return new Response('{}', {status: 200, headers: {...cors, 'Content-Type': 'application/json', 'Cache-Control':'no-store',
        'Set-Cookie': 'svsess=; HttpOnly; Secure; SameSite=None; Path=/; Max-Age=0'}});
    }

    // ---- ORCID phase 2 (AUTH-SETUP.md): sign-in with ORCID, profile autofill ----
    // 503 until ORCID_CLIENT_ID / ORCID_CLIENT_SECRET are set (owner: Developer Tools).
    const ORCID_CB = "https://ipvv-api.tradesprior.workers.dev/api/auth/orcid/callback";
    const orcCreds = () => (env.ORCID_CLIENT_ID && env.ORCID_CLIENT_SECRET)
      ? {id: env.ORCID_CLIENT_ID, sec: env.ORCID_CLIENT_SECRET} : null;

    if (path === '/api/auth/orcid/start' && request.method === 'GET') {
      const creds = orcCreds();
      if(!creds) return json({error:'ORCID not configured — see worker/AUTH-SETUP.md (Developer Tools step)'}, 503, cors);
      const u = new URL(request.url);
      const back = u.searchParams.get('redirect') || '/';
      // Only paths on the reader are valid. In particular reject //host and
      // backslash forms which URL parsers can interpret as external origins.
      if (back.length > 512 || !back.startsWith('/') || back.startsWith('//') || /[\\\x00-\x1f\x7f]/.test(back))
        return json({error:'invalid redirect'}, 400, cors);
      // Remember where the reader lives so the callback can return there
      // instead of a hardcoded host (svatantrya.net vs branch aliases).
      const caller = returnableOrigin(request.headers.get('Referer') || '');
      const st = await (async()=>{
        const nonce = b64u(crypto.getRandomValues(new Uint8Array(32)));
        const body = btoa(JSON.stringify({b: back, o: caller, n: nonce, e: Date.now() + 10*60*1000}));
        const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(env.SESSION_SECRET||''), {name:'HMAC', hash:'SHA-256'}, false, ['sign']);
        const mac = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(body));
        return body + '.' + btoa(String.fromCharCode(...new Uint8Array(mac))).replace(/=+$/,'').replace(/\+/g,'-').replace(/\//g,'_');
      })();
      const authz = 'https://orcid.org/oauth/authorize?' + new URLSearchParams({
        client_id: creds.id, response_type: 'code', scope: '/authenticate',
        redirect_uri: ORCID_CB, state: st}).toString();
      return new Response(null, {status:302,headers:{'Location':authz,'Cache-Control':'no-store',
        'Set-Cookie':`svorcid=${st}; HttpOnly; Secure; SameSite=Lax; Path=/api/auth/orcid/callback; Max-Age=600`}});
    }

    if (path === '/api/auth/orcid/callback' && request.method === 'GET') {
      const creds = orcCreds();
      if(!creds) return json({error:'ORCID not configured'}, 503, cors);
      const u = new URL(request.url);
      const code = u.searchParams.get('code') || '';
      const st = u.searchParams.get('state') || '';
      try {
        const stateCookie = (request.headers.get('Cookie') || '').split(';').map(x=>x.trim())
          .find(x=>x.startsWith('svorcid='))?.slice('svorcid='.length);
        if (!code || !st || !stateCookie || stateCookie !== st)
          return json({error:'bad or expired state'}, 400, cors);
        const [body, sig] = st.split('.');
        const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(env.SESSION_SECRET||''), {name:'HMAC', hash:'SHA-256'}, false, ['verify']);
        const raw = Uint8Array.from(atob(sig.replace(/-/g,'+').replace(/_/g,'/')), c=>c.charCodeAt(0));
        const okSig = await crypto.subtle.verify('HMAC', key, raw, new TextEncoder().encode(body));
        const okExp = okSig && JSON.parse(atob(body)).e > Date.now();
        if(!okExp) return json({error:'bad or expired state'}, 400, cors);
        const back = JSON.parse(atob(body)).b || '/';
        if (typeof back !== 'string' || !back.startsWith('/') || back.startsWith('//') || /[\\\x00-\x1f\x7f]/.test(back))
          return json({error:'bad or expired state'}, 400, cors);
        // Return to the reader host the flow started on (apex, branch alias,
        // or local dev); fall back to the canonical host, never an open URL.
        const retBase = returnableOrigin(JSON.parse(atob(body)).o) || 'https://svatantrya.net';
        const tok = await fetch('https://orcid.org/oauth/token', {method:'POST',
          headers:{'Content-Type':'application/x-www-form-urlencoded','Accept':'application/json'},
          body: new URLSearchParams({grant_type:'authorization_code', code,
            redirect_uri: ORCID_CB, client_id: creds.id, client_secret: creds.sec})}).then(r=>r.json());
        if(!tok.access_token) return json({error:'orcid token exchange failed'}, 502, cors);
        // /authenticate returns the authenticated iD in the token response.
        // The userinfo endpoint instead requires the separate openid scope.
        const sub = String(tok.orcid || '');
        if(!/^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$/.test(sub)) return json({error:'invalid orcid iD'}, 502, cors);
        // link-or-create: identity keyed by ORCID iD (verified via OAuth, never typed)
        let row = await env.DB.prepare('SELECT * FROM profiles WHERE orcid = ?').bind(sub).first();
        const email = `${sub.replace(/-/g,'')}@orcid.svread`;
        if(!row){
          const uid = crypto.randomUUID();
          await env.DB.prepare('INSERT INTO profiles (id, email, display_name, orcid, provider) VALUES (?,?,?,?,?)')
            .bind(uid, email, String(tok.name || sub).slice(0,80), sub, 'orcid').run();
          row = {id: uid};
        }
        const exp = Date.now() + 7*24*3600*1000;
        const sb = btoa(JSON.stringify({u: row.id, e: exp}));
        const skey = await crypto.subtle.importKey('raw', new TextEncoder().encode(env.SESSION_SECRET||''), {name:'HMAC', hash:'SHA-256'}, false, ['sign']);
        const mac = b64u(await crypto.subtle.sign('HMAC', skey, new TextEncoder().encode(sb)));
        const headers = new Headers({...cors, 'Location':new URL(back, retBase).toString(),
          'Cache-Control':'no-store'});
        headers.append('Set-Cookie',`svsess=${sb}.${mac}; HttpOnly; Secure; SameSite=None; Path=/; Max-Age=${7*24*3600}`);
        headers.append('Set-Cookie','svorcid=; HttpOnly; Secure; SameSite=Lax; Path=/api/auth/orcid/callback; Max-Age=0');
        return new Response(null, {status: 302, headers});
      } catch(e) {
        return json({error: 'orcid flow failed'}, 502, cors);
      }
    }

    // POST /api/read — verse-by-verse TTS render (fish s2.1-pro-free, $0),
    // The cache key binds the exact spoken text, voice and model. A revision of
    // a passage must never reuse a recording of an earlier reading.
    if (path === '/api/read' && request.method === 'POST') {
      let b = {}; try { b = await request.json(); } catch (e) {}
      const work = String(b.work || '').replace(/[^a-z0-9_-]/g, '');
      const vid = String(b.verse || '').replace(/[^a-z0-9_.:-]/g, '');
      const lang = ['sa','en','c1'].includes(b.lang) ? b.lang : 'sa';
      const text = String(b.text || '').slice(0, 4000);
      const ref = lang === 'sa'
        ? '4e873c37d4cb439e9bccc4dc1f633290'    // Andlig Sanskrit Rost
        : '614f8afd83f841048c040b2c6234d2c1';   // Granny British (en + commentary)
      if (!work || !vid || !text.trim()) return json({ error: 'work/verse/text required' }, 400, cors);
      const model = 's2.1-pro-free';
      const identity = JSON.stringify({version:2,text,reference_id:ref,model});
      const hash = await crypto.subtle.digest('SHA-256',new TextEncoder().encode(identity));
      const digest = Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,'0')).join('');
      const key = `read-v2/${work}/${vid}_${lang}_${digest}.mp3`;
      const pub = `https://pub-87169194562a44fcb8279a799d626c62.r2.dev/${key}`;
      try {
        const cached = await env.AUDIO.head(key);
        if (cached) return json({ url: pub, cached: true }, 200, cors);
      } catch (e) { /* no cache */ }
      if (!env.FISH_API_KEY) return json({ error: 'FISH_API_KEY not configured' }, 503, cors);
      try {
        const fr = await fetch('https://api.fish.audio/v1/tts', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.FISH_API_KEY}`,
            'model': model,                       // free model; operator must monitor provider quota
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text, reference_id: ref, format: 'mp3' }),
        });
        if (!fr.ok) return json({ error: 'tts http ' + fr.status, detail: (await fr.text()).slice(0, 200) }, 502, cors);
        const buf = await fr.arrayBuffer();
        await env.AUDIO.put(key, buf, { httpMetadata: { contentType: 'audio/mpeg' } });
        return json({ url: pub, cached: false, bytes: buf.byteLength }, 200, cors);
      } catch (e) {
        return json({ error: String(e).slice(0, 200) }, 502, cors);
      }
    }

    if (path === '/api/questions' && request.method === 'GET') {
      const { results } = await env.DB.prepare('SELECT id, work, message, reply, created_at FROM questions ORDER BY created_at DESC LIMIT 100').all();
      return json({ questions: results }, 200, cors);
    }


    // MCP server (JSON-RPC over HTTP)
    if (path === '/mcp' && request.method === 'POST') {
      const body = await request.json();
      const { method, params, id } = body;
      let result = null;

      if (method === 'initialize') {
        result = {
          protocolVersion: '2024-11-05',
          capabilities: { tools: {} },
          serverInfo: { name: 'ipvv-mcp', version: '1.0.0' },
        };
      } else if (method === 'tools/list') {
        result = { tools: [
          { name: 'get_passage', description: 'Get a published IPVV passage (Sanskrit + L2 + C1)', inputSchema: { type: 'object', properties: { chunk: { type: 'string' } }, required: ['chunk'] } },
          { name: 'get_translation', description: 'Get translation records for a work', inputSchema: { type: 'object', properties: { work: { type: 'string' } }, required: ['work'] } },
          { name: 'get_argument', description: 'Get an argument truth-packet', inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] } },
          { name: 'search', description: 'Search across all content', inputSchema: { type: 'object', properties: { query: { type: 'string' }, work: { type: 'string' } } } },
          { name: 'get_scholar', description: 'Get scholar bio + bibliography', inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] } },
          { name: 'list_works', description: 'List all translated works', inputSchema: { type: 'object', properties: {} } },
          { name: 'get_themes', description: 'Get theme proposals', inputSchema: { type: 'object', properties: {} } },
          { name: 'chat', description: 'Chat about a text (RAG)', inputSchema: { type: 'object', properties: { work: { type: 'string' }, message: { type: 'string' } }, required: ['work', 'message'] } },
        ]};
      } else if (method === 'tools/call') {
        const { name, arguments: args } = params;
        if (name === 'get_passage') {
          const id = args.chunk.replace('.md','').replace('chunk','').toLowerCase();
          const resp = await fetch(`https://ipvv-a8u.pages.dev/data/arguments/ipvv-${args.chunk.replace('.md','')}.json`);
          if (!resp.ok) { result = { content: [{ type: 'text', text: JSON.stringify({ error: 'not found' }) }] }; }
          else { const data = await resp.json(); result = { content: [{ type: 'text', text: JSON.stringify(data) }] }; }
        } else if (name === 'get_translation') {
          const resp = await fetch(`https://ipvv-a8u.pages.dev/data/translations/${args.work}.json`);
          if (!resp.ok) { result = { content: [{ type: 'text', text: JSON.stringify({ error: 'work not found' }) }] }; }
          else { const data = await resp.json(); result = { content: [{ type: 'text', text: JSON.stringify(data) }] }; }
        } else if (name === 'get_argument') {
          const id = args.id.startsWith('ipvv-') ? args.id : 'ipvv-' + args.id;
          const resp = await fetch(`https://ipvv-a8u.pages.dev/data/arguments/${id}.json`);
          if (!resp.ok) { result = { content: [{ type: 'text', text: JSON.stringify({ error: 'not found' }) }] }; }
          else { const data = await resp.json(); result = { content: [{ type: 'text', text: JSON.stringify(data) }] }; }
        } else if (name === 'search') {
          const resp = await fetch('https://ipvv-a8u.pages.dev/data/search-index.json');
          const idx = await resp.json();
          const q = (args.query || '').toLowerCase();
          const hits = idx.filter(e => e.t.toLowerCase().includes(q)).slice(0, 20);
          if (args.work) {
            const filtered = hits.filter(e => e.u.includes('/' + args.work + '/'));
            result = { content: [{ type: 'text', text: JSON.stringify(filtered) }] };
          } else {
            result = { content: [{ type: 'text', text: JSON.stringify(hits) }] };
          }
        } else if (name === 'get_scholar') {
          const resp = await fetch('https://ipvv-a8u.pages.dev/data/scholars.json');
          const scholars = await resp.json();
          const s = scholars.find(x => x.id === args.id);
          result = { content: [{ type: 'text', text: JSON.stringify(s || { error: 'not found' }) }] };
        } else if (name === 'list_works') {
          const resp = await fetch('https://ipvv-a8u.pages.dev/data/search-index.json');
          const idx = await resp.json();
          const works = [...new Set(idx.filter(e => e.k === 'work').map(e => e.t))];
          result = { content: [{ type: 'text', text: JSON.stringify(works) }] };
        } else if (name === 'get_themes') {
          const resp = await fetch('https://ipvv-a8u.pages.dev/data/themes/clusters.json');
          const data = await resp.json();
          result = { content: [{ type: 'text', text: JSON.stringify(data) }] };
        } else if (name === 'chat') {
          result = { content: [{ type: 'text', text: 'Use /api/chat/' + (args.work || 'ipvv') + ' directly for RAG chat. MCP chat tool disabled to avoid subrequest errors.' }] };
        } else {
          result = { content: [{ type: 'text', text: JSON.stringify({ error: 'unknown tool: ' + name }) }] };
        }
      } else {
        result = { error: { code: -32601, message: 'Method not found' } };
      }

      return new Response(JSON.stringify({ jsonrpc: '2.0', id, result }), {
        headers: { ...cors, 'Content-Type': 'application/json' },
      });
    }


    // POST /api/screen — analyze a screenshot (vision via Qwen3.8-Omni-Flash)
    if (path === '/api/screen' && request.method === 'POST') {
      const { image, question } = await request.json();
      if (!image) return json({ error: 'image required (base64)' }, 400, cors);
      const q = question || 'Describe what you see on this screen. Be concise and helpful.';
      try {
        const resp = await fetch('https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${env.DASHSCOPE_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: 'qwen3.8-omni-flash',
            messages: [{ role: 'user', content: [
              { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${image}` } },
              { type: 'text', text: q },
            ]}],
            max_tokens: 512,
            reasoning_effort: 'medium',
          }),
        });
        if (!resp.ok) throw new Error(`dashscope ${resp.status}`);
        const data = await resp.json();
        const reply = data.choices?.[0]?.message?.content || '';
        return json({ reply }, 200, cors);
      } catch (e) {
        return json({ error: e.message }, 500, cors);
      }
    }


    // A legacy unauthenticated accept route cannot grant human authority. Keep
    // it closed until it is wired to an authenticated, validated review flow.
    const va = path.match(/^\/api\/variants\/([^/]+)\/accept$/);
    if (va && request.method === 'POST') {
      return json({error:'Variant acceptance requires an authenticated review workflow.'}, 503, cors);
    }

    return json({ error: 'not found' }, 404, cors);
  }
};

function json(data, status, cors) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...cors, 'Content-Type': 'application/json' },
  });
}
