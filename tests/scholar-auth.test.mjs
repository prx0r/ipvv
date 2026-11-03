import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const source = await readFile(new URL('../worker/src/index.js', import.meta.url), 'utf8');
const worker = (await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`)).default;
const origin = 'https://svread.pages.dev';

function database(initial = []) {
  const rows = new Map(initial.map(row => [row.email, {...row}]));
  return {
    rows,
    writes: 0,
    prepare(sql) {
      return {bind: (...args) => ({
        first: async () => {
          if (sql.includes('WHERE email = ?')) return rows.get(args[0]) || null;
          if (sql.includes('WHERE id = ?')) return [...rows.values()].find(row => row.id === args[0]) || null;
          throw new Error(`unexpected query: ${sql}`);
        },
        run: async () => {
          if (!sql.startsWith('INSERT INTO profiles')) throw new Error(`unexpected write: ${sql}`);
          const [id, email, password_hash, salt, display_name, provider] = args;
          rows.set(email, {id, email, password_hash, salt, display_name, provider});
          this.writes++;
        },
      })};
    },
  };
}

function request(path, method = 'GET', body = undefined, extraHeaders = {}) {
  return new Request(`https://worker.example${path}`, {
    method, headers: {Origin: origin, ...(body ? {'Content-Type': 'application/json'} : {}), ...extraHeaders},
    ...(body ? {body: JSON.stringify(body)} : {}),
  });
}

test('authentication rejects an absent session secret', async () => {
  const DB = database();
  const res = await worker.fetch(request('/api/auth/access', 'POST', {email:'a@example.com', password:'password'}), {DB});
  assert.equal(res.status, 503);
  assert.equal(DB.writes, 0);
});

test('an existing email-only profile cannot be claimed', async () => {
  const DB = database([{id:'existing', email:'a@example.com', password_hash:null, orcid:'example'}]);
  const env = {DB, SESSION_SECRET:'s'.repeat(32)};
  const res = await worker.fetch(request('/api/auth/access', 'POST', {email:'a@example.com', password:'password'}), env);
  assert.equal(res.status, 409);
  assert.equal(DB.writes, 0);
  assert.equal(DB.rows.get('a@example.com').password_hash, null);
});

test('new account session is cross-site compatible and rejects untrusted origins', async () => {
  const DB = database();
  const env = {DB, SESSION_SECRET:'s'.repeat(32)};
  const input = {email:'new@example.com', password:'strong-password', name:'A Scholar'};
  const signup = await worker.fetch(request('/api/auth/access', 'POST', input), env);
  assert.equal(signup.status, 200);
  const cookie = signup.headers.get('Set-Cookie');
  assert.match(cookie, /Secure/);
  assert.match(cookie, /SameSite=None/);
  const me = await worker.fetch(request('/api/auth/me', 'GET', undefined, {Cookie: cookie.split(';')[0]}), env);
  assert.equal((await me.json()).profile.display_name, 'A Scholar');
  const bad = await worker.fetch(request('/api/auth/access', 'POST', {...input, password:'wrong-password'}), env);
  assert.equal(bad.status, 401);
  const blocked = await worker.fetch(request('/api/auth/logout', 'POST', undefined, {Origin:'https://untrusted.example'}), env);
  assert.equal(blocked.status, 403);
});
