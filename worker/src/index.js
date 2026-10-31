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

    // POST /api/profile — create or get profile by email
    if (path === '/api/profile' && request.method === 'POST') {
      const { email } = await request.json();
      if (!email) return json({ error: 'email required' }, 400, cors);
      const id = 'u:' + btoa(email).replace(/=/g, '');
      await env.DB.prepare('INSERT OR IGNORE INTO profiles (id, email) VALUES (?, ?)').bind(id, email).run();
      return json({ id, email }, 200, cors);
    }

    // POST /api/variants — save a variant
    if (path === '/api/variants' && request.method === 'POST') {
      const { user_id, work, chunk, text, style } = await request.json();
      if (!user_id || !work || !chunk || !text) return json({ error: 'missing fields' }, 400, cors);
      const id = 'v:' + crypto.randomUUID();
      await env.DB.prepare('INSERT INTO variants (id, user_id, work, chunk, text, style) VALUES (?, ?, ?, ?, ?, ?)')
        .bind(id, user_id, work, chunk, text, style || 'owner').run();
      return json({ id }, 200, cors);
    }

    // GET /api/variants/:work/:chunk — list variants for a chunk
    const vm = path.match(/^\/api\/variants\/([^/]+)\/([^/]+)$/);
    if (vm && request.method === 'GET') {
      const [, work, chunk] = vm;
      const { results } = await env.DB.prepare('SELECT * FROM variants WHERE work = ? AND chunk = ? ORDER BY created_at DESC')
        .bind(work, chunk).all();
      return json({ variants: results }, 200, cors);
    }

    // POST /api/bookmarks — save a bookmark
    if (path === '/api/bookmarks' && request.method === 'POST') {
      const { user_id, work, chunk } = await request.json();
      if (!user_id || !work || !chunk) return json({ error: 'missing fields' }, 400, cors);
      const id = 'b:' + crypto.randomUUID();
      await env.DB.prepare('INSERT OR IGNORE INTO bookmarks (id, user_id, work, chunk) VALUES (?, ?, ?, ?)')
        .bind(id, user_id, work, chunk).run();
      return json({ id }, 200, cors);
    }

    // GET /api/bookmarks/:user_id — list bookmarks
    const bm = path.match(/^\/api\/bookmarks\/([^/]+)$/);
    if (bm && request.method === 'GET') {
      const [, userId] = bm;
      const { results } = await env.DB.prepare('SELECT * FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC')
        .bind(userId).all();
      return json({ bookmarks: results }, 200, cors);
    }

    // POST /api/chat/:work — chat about a text (stores history, returns placeholder)
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
      // RAG response would go here — for now, echo with work context
      const reply = `Chat about ${work} is live. RAG over corpus.jsonl coming next. Your question: ${message}`;
      await env.DB.prepare('INSERT INTO chat_messages (id, session_id, role, content) VALUES (?, ?, ?, ?)')
        .bind('m:' + crypto.randomUUID(), sid, 'assistant', reply).run();
      return json({ session_id: sid, reply }, 200, cors);
    }

    // GET /api/chat/:session_id/history — chat history
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
