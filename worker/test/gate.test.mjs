// gate.test.mjs — worker-owned functional test for the server-scored gate.
// Runs the REAL worker module with an in-memory D1 stub and a local pool
// fixture — no wrangler, no network, no svread checkout. Run:
//   node --test worker/test/gate.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import worker from '../src/index.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));

// ---- in-memory D1 stub (only the queries the gate + access routes use) ----
function makeDB() {
  const R = { profiles: [], learner_progress: [], learner_attempts: [], gate_sessions: [] };
  return {
    rows: R,
    prepare(sql) {
      const api = {
        _a: [],
        bind(...a) { this._a = a; return this; },
        async first() { return one(sql, this._a); },
        async all() { return { results: many(sql, this._a) }; },
        async run() { mut(sql, this._a); return { success: true }; },
      };
      function one(q, a) {
        if (q.startsWith('SELECT id FROM profiles WHERE auth_uid'))
          return R.profiles.find(r => r.auth_uid === a[0]) || null;
        if (q.startsWith('SELECT * FROM profiles WHERE email'))
          return R.profiles.find(r => r.email === a[0]) || null;
        if (q.startsWith('SELECT id, email, display_name, orcid, provider FROM profiles WHERE id'))
          return R.profiles.find(r => r.id === a[0]) || null;
        if (q.startsWith('SELECT stage FROM learner_progress')) {
          const p = R.learner_progress.find(x => x.user_id === a[0] && x.curriculum === a[1]);
          return p ? { stage: p.stage } : null;
        }
        if (q.startsWith('SELECT COUNT(*) AS n FROM learner_attempts')) {
          const h = Date.now() - 3600 * 1000;
          return { n: R.learner_attempts.filter(x =>
            x.user_id === a[0] && x.curriculum === a[1] && x.created_at_ms > h).length };
        }
        if (q.startsWith('SELECT * FROM gate_sessions WHERE id'))
          return R.gate_sessions.find(x => x.id === a[0]) || null;
        if (q.startsWith('SELECT stage, passed_json, items_json FROM learner_progress')) {
          const p = R.learner_progress.find(x => x.user_id === a[0] && x.curriculum === a[1]);
          return p ? { stage: p.stage, passed_json: p.passed_json, items_json: p.items_json } : null;
        }
        throw new Error('unstubbed SELECT: ' + q.slice(0, 90));
      }
      function many(q, a) {
        if (q.startsWith('SELECT curriculum, stage, passed_json FROM learner_progress'))
          return R.learner_progress.filter(x => x.user_id === a[0])
            .map(x => ({ curriculum: x.curriculum, stage: x.stage, passed_json: x.passed_json }));
        throw new Error('unstubbed SELECT-many: ' + q.slice(0, 90));
      }
      function mut(q, a) {
        if (q.startsWith('INSERT INTO learner_progress')) {
          R.learner_progress.push({ user_id: a[0], curriculum: a[1], stage: 1,
            passed_json: '[]', items_json: '{}' }); return;
        }
        if (q.startsWith('INSERT INTO profiles')) {
          R.profiles.push({ id: a[0], email: a[1], password_hash: a[2], salt: a[3],
            display_name: a[4], provider: a[5], auth_uid: null }); return;
        }
        if (q.startsWith('INSERT INTO gate_sessions')) {
          R.gate_sessions.push({ id: a[0], user_id: a[1], curriculum: a[2], stage: a[3],
            items_json: a[4], key_json: a[5], expires_at: a[6], created_at: a[7], used: 0 });
          return;
        }
        if (q.startsWith('UPDATE gate_sessions SET used')) {
          const s = R.gate_sessions.find(x => x.id === a[0]); if (s) s.used = 1; return;
        }
        if (q.startsWith('INSERT INTO learner_attempts')) {
          R.learner_attempts.push({ id: a[0], user_id: a[1], curriculum: a[2], stage: a[3],
            items_json: a[4], answers_json: a[5], score: a[6], passed: a[7],
            created_at_ms: Date.now() }); return;
        }
        if (q.startsWith('UPDATE learner_progress SET')) {
          const p = R.learner_progress.find(x => x.user_id === a[3] && x.curriculum === a[4]);
          if (p) { p.stage = a[0]; p.passed_json = a[1]; p.items_json = a[2]; } return;
        }
        if (q.startsWith('UPDATE profiles SET auth_uid')) {
          const p = R.profiles.find(x => x.id === a[1]); if (p) p.auth_uid = a[0]; return;
        }
        throw new Error('unstubbed mut: ' + q.slice(0, 90));
      }
      return api;
    },
  };
}

// ---- local pool fixture server (the real gates.json shape, snapshot) ----
const fixture = fs.readFileSync(path.join(HERE, 'fixtures', 'gates.json'), 'utf8');
const poolServer = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(fixture);
});
await new Promise(r => poolServer.listen(0, '127.0.0.1', r));
const poolUrl = `http://127.0.0.1:${poolServer.address().port}/gates.json`;

const DB = makeDB();
const env = {
  DB,
  SESSION_SECRET: 'x'.repeat(40),
  GATE_POOLS_URL: poolUrl,
  CORS_ORIGIN: 'https://svatantrya.net',
};

async function call(pathname, body, cookie) {
  const req = new Request('http://w' + pathname, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(cookie ? { Cookie: cookie } : {}) },
    body: JSON.stringify(body),
  });
  const res = await worker.fetch(req, env);
  const text = await res.text();
  let j; try { j = JSON.parse(text); } catch { j = { _raw: text }; }
  const set = res.headers.get('set-cookie');
  return { status: res.status, json: j, cookie: set ? set.split(';')[0] : null };
}

// answers come from the fixture itself: studying the public pool is allowed;
// what the tests protect is that the SERVER holds the key and writes the unlock
const pool = JSON.parse(fixture);
const ansMap = {};
for (const c of Object.values(pool.curricula.word.stages))
  for (const it of c.items) ansMap[it.id] = it.answer;
for (const c of Object.values(pool.curricula.sentence.stages))
  for (const it of c.items) ansMap[it.id] = it.answer;

test.after(() => poolServer.close());

test('access creates a session cookie', async () => {
  const r = await call('/api/auth/access',
    { email: 't@example.com', password: 'password123', name: 'T' });
  assert.equal(r.status, 200);
  assert.ok(r.cookie && r.cookie.startsWith('svsess='));
  globalThis.__cookie = r.cookie;
});

test('start serves 20 shuffled items and never the key', async () => {
  const r = await call('/api/wheel/gate/start', { curriculum: 'word', stage: 1 }, globalThis.__cookie);
  assert.equal(r.status, 200);
  assert.equal(r.json.items.length, 20);
  assert.ok(!JSON.stringify(r.json).includes('answer'), 'no answer field in start payload');
  globalThis.__sid = r.json.session_id;
  globalThis.__served = r.json.items;
});

test('unknown session is 404', async () => {
  const r = await call('/api/wheel/gate/submit',
    { session_id: 'nope', answers: [] }, globalThis.__cookie);
  assert.equal(r.status, 404);
});

test('perfect submit passes 20/20 and unlocks stage 2', async () => {
  const answers = globalThis.__served.map(it =>
    ({ item_id: it.item_id, choice: ansMap[it.item_id] }));
  const r = await call('/api/wheel/gate/submit',
    { session_id: globalThis.__sid, answers }, globalThis.__cookie);
  assert.equal(r.status, 200);
  assert.equal(r.json.score, 20);
  assert.equal(r.json.passed, true);
  assert.equal(r.json.unlock.next_stage, 2);
});

test('replay of a used session is 409', async () => {
  const answers = globalThis.__served.map(it =>
    ({ item_id: it.item_id, choice: ansMap[it.item_id] }));
  const r = await call('/api/wheel/gate/submit',
    { session_id: globalThis.__sid, answers }, globalThis.__cookie);
  assert.equal(r.status, 409);
});

test('progress endpoint reports word stage 2', async () => {
  const req = new Request('http://w/api/wheel/progress',
    { headers: { Cookie: globalThis.__cookie } });
  const res = await worker.fetch(req, env);
  const j = JSON.parse(await res.text());
  assert.equal(res.status, 200);
  const w = j.progress.find(p => p.curriculum === 'word');
  assert.equal(w.stage, 2);
  assert.equal(w.passed.length, 1);
});

test('skip-ahead to a locked stage is 403', async () => {
  const r = await call('/api/wheel/gate/start', { curriculum: 'word', stage: 3 }, globalThis.__cookie);
  assert.equal(r.status, 403);
});

test('sentence circle stays locked until the word circle is done', async () => {
  const r = await call('/api/wheel/gate/start', { curriculum: 'sentence', stage: 1 }, globalThis.__cookie);
  assert.equal(r.status, 403);
});

test('all-wrong submit fails and writes no unlock', async () => {
  const start = await call('/api/wheel/gate/start', { curriculum: 'word', stage: 2 }, globalThis.__cookie);
  const wrong = start.json.items.map(it => ({ item_id: it.item_id, choice: '___wrong___' }));
  const r = await call('/api/wheel/gate/submit',
    { session_id: start.json.session_id, answers: wrong }, globalThis.__cookie);
  assert.equal(r.status, 200);
  assert.equal(r.json.passed, false);
  assert.equal(r.json.score, 0);
  assert.ok(!r.json.unlock);
});

test('three attempts per hour then 429', async () => {
  // burn two more attempts (the all-wrong one counted as #1)
  for (let i = 0; i < 2; i++) {
    const s = await call('/api/wheel/gate/start', { curriculum: 'word', stage: 2 }, globalThis.__cookie);
    if (s.json.session_id) {
      const wrong = s.json.items.map(it => ({ item_id: it.item_id, choice: '___wrong___' }));
      await call('/api/wheel/gate/submit', { session_id: s.json.session_id, answers: wrong }, globalThis.__cookie);
    }
  }
  const r = await call('/api/wheel/gate/start', { curriculum: 'word', stage: 2 }, globalThis.__cookie);
  assert.equal(r.status, 429);
});

test('unauthenticated start is 401', async () => {
  const r = await call('/api/wheel/gate/start', { curriculum: 'word', stage: 1 });
  assert.equal(r.status, 401);
});

test('cross-origin start is rejected', async () => {
  const req = new Request('http://w/api/wheel/gate/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json',
      Origin: 'https://evil.example',
      Cookie: globalThis.__cookie },
    body: JSON.stringify({ curriculum: 'word', stage: 2 }),
  });
  const res = await worker.fetch(req, env);
  assert.equal(res.status, 403);
});
