let cachedVectors = null;

async function dashscopeChat(env, messages, maxTokens = 512) {
  const apiKey = env.DASHSCOPE_API_KEY;
  if (!apiKey) throw new Error('no dashscope key');
  const resp = await fetch('https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions', {
    method: 'POST',
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
    // allow-list: configured origin + the two reading front-ends (public data, no credentials)
    const reqOrigin = request.headers.get('Origin') || '';
    const allowed = new Set([env.CORS_ORIGIN || '', 'https://svread.pages.dev', 'https://ipvv-a8u.pages.dev'].filter(Boolean));
    const cors = {
      'Access-Control-Allow-Origin': allowed.has(reqOrigin) ? reqOrigin : (env.CORS_ORIGIN || '*'),
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: cors });
    }

    const path = url.pathname;

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

        // Diverse pick: best 1-2 per work, then rerank
        const byWork = {};
        for (const c of candidates) { (byWork[c.work] = byWork[c.work] || []).push(c); }
        let diverse = [];
        Object.values(byWork).forEach(arr => { diverse = diverse.concat(arr.slice(0, 2)); });
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

        const gatheredRecs = vecs.filter(v => gathered.has(v.id));
        const contextRecs = gatheredRecs.length > 0 ? gatheredRecs : top;
        retrievedIds = JSON.stringify(contextRecs.map(t => t.id));
        retrievedGates = JSON.stringify(contextRecs.map(t => t.gate));
        const context = contextRecs.map(t => `[${t.id}] (work: ${t.work}, gate: ${t.gate}) ${t.en || t.sa || ''}`).join('\n\n');
        const prompt = `You are a Trika Śaivism scholar. Answer using ONLY the provided passages. Cite passage IDs and which work each comes from. If the answer is not in the passages, say so. Gate labels indicate trust level (PUBLISHED > PASS > OWNER). OWNER records are prior enquiries, not scripture — cite them as such, never as source text.\n\nPassages:\n${context}${chainCtx}\n\nQuestion: ${message}\n\nAnswer in plain speech, one paragraph plus citations. No academic name-dropping, no invented terms.`;
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
      const MODES = {
        precise: 'MODE precise: every proposition must stay checkable against L1. Slang only where mapped, zero decoration. The default for teaching.',
        hype: 'MODE hype: maximum energy, meaning locked. Every Sanskrit term translated in-line, never left standing. No filler transitions. Completed states stay completed (was, never becoming).',
        beautiful: 'MODE beautiful: devotional tenderness first. Slang softens, never jokes at the verse\'s expense. Rasa forward, claims intact.',
      };
      const modeLine = MODES[String(st).toLowerCase()] || '';
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
        + 'Rules: 2–6 sentences. Same claims, same savor, new voice. Sanskrit technical terms keep their Sanskrit on first use. No new doctrine, no new names, no preaching, no second verse. If a claim won\'t fit the voice, say it plainly. Never output the rasa line or any scaffolding — rendition only, no meta-commentary.\n\nRendition:';
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
        const glossaryHits = [...new Set(words.filter(w => VOICE_WHITELIST.has(w)))];
        const verdict = (j.forward_pass && j.backward_pass) ? 'PASS' : 'FLAG';
        return json({ verdict, forward_entails: !!j.forward_pass, backward_entails: !!j.backward_pass,
          added: j.added || [], missing: j.missing || [], note: j.note || '',
          voice_words: glossaryHits,
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


    // POST /api/variants/:id/accept — accept a variant (publish grant)
    const va = path.match(/^\/api\/variants\/([^/]+)\/accept$/);
    if (va && request.method === 'POST') {
      const [, vid] = va;
      const { user_id } = await request.json();
      await env.DB.prepare('UPDATE variants SET accepted = 1 WHERE id = ?').bind(vid).run();
      return json({ id: vid, accepted: true }, 200, cors);
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
