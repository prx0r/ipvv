let cachedVectors = null;

async function getVectors(env) {
  if (cachedVectors) return cachedVectors;
  try {
    const resp = await fetch('https://ipvv-a8u.pages.dev/data/vectors.json');
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
    const cors = {
      'Access-Control-Allow-Origin': env.CORS_ORIGIN || '*',
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

    // POST /api/chat/:work — RAG chat
    const cm = path.match(/^\/api\/chat\/([^/]+)$/);
    if (cm && request.method === 'POST') {
      const [, work] = cm;
      const { session_id, message, user_id } = await request.json();
      if (!message) return json({ error: 'message required' }, 400, cors);

      let sid = session_id;
      if (!sid) {
        sid = 's:' + crypto.randomUUID();
        await env.DB.prepare('INSERT INTO chat_sessions (id, user_id, work) VALUES (?, ?, ?)')
          .bind(sid, user_id || null, work).run();
      }
      await env.DB.prepare('INSERT INTO chat_messages (id, session_id, role, content) VALUES (?, ?, ?, ?)')
        .bind('m:' + crypto.randomUUID(), sid, 'user', message).run();

      let reply = '';
      try {
        const qEmb = await env.AI.run('@cf/baai/bge-m3', { text: ['query: ' + message] });
        const qVec = qEmb.data[0];

        const vecs = await getVectors(env);
        if (!vecs) throw new Error('vectors not loaded');

        const gateWeight = { 'PUBLISHED': 1.0, 'PASS': 0.9, 'OWNER': 0.7, 'BLOCKED': 0.0 };
        const candidates = vecs
          .filter(v => v.work === work && (v.gate === 'PASS' || v.gate === 'PUBLISHED' || v.gate === 'OWNER'))
          .map(v => ({ ...v, score: cosine(qVec, v.vec) * (gateWeight[v.gate] || 0.5) }))
          .sort((a, b) => b.score - a.score)
          .slice(0, 20);

        let top = candidates.slice(0, 5);
        if (candidates.length > 5) {
          const ctxs = candidates.map(c => ({ text: (c.en || c.sa || '').slice(0, 500) || 'passage' }));
          const rerank = await env.AI.run('@cf/baai/bge-reranker-base', {
            query: message,
            contexts: ctxs,
          });
          const scores = rerank.results || rerank.data || [];
          candidates.forEach((c, i) => {
            c.rerank = (scores[i] && (scores[i].score || scores[i])) || c.score;
          });
          top = candidates.sort((a, b) => b.rerank - a.rerank).slice(0, 5);
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
        const context = contextRecs.map(t => `[${t.id}] (gate: ${t.gate}) ${t.en || t.sa || ''}`).join('\n\n');
        const prompt = `You are a Trika Śaivism scholar. Answer using ONLY the provided passages. Cite passage IDs. If the answer is not in the passages, say so. Gate labels indicate trust level (PUBLISHED > PASS > OWNER).\n\nPassages:\n${context}\n\nQuestion: ${message}\n\nAnswer:`;
        const gen = await env.AI.run('@cf/meta/llama-3.1-8b-instruct-fp8', {
          messages: [{ role: 'user', content: prompt }],
          max_tokens: 512,
        });
        reply = gen.response || gen.result?.response || JSON.stringify(gen).slice(0, 500);
      } catch (e) {
        reply = `RAG error: ${e.message}. Vectors: ${cachedVectors ? cachedVectors.length : 'none'}.`;
      }

      await env.DB.prepare('INSERT INTO chat_messages (id, session_id, role, content) VALUES (?, ?, ?, ?)')
        .bind('m:' + crypto.randomUUID(), sid, 'assistant', reply).run();
      return json({ session_id: sid, reply }, 200, cors);
    }

    // GET /api/chat/:session_id/history
    const ch = path.match(/^\/api\/chat\/([^/]+)\/history$/);
    if (ch && request.method === 'GET') {
      const [, sid] = ch;
      const { results } = await env.DB.prepare('SELECT role, content, created_at FROM chat_messages WHERE session_id = ? ORDER BY created_at')
        .bind(sid).all();
      return json({ messages: results }, 200, cors);
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
