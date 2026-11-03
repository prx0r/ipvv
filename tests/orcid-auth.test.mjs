import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {DatabaseSync} from 'node:sqlite';

const source=await readFile(new URL('../worker/src/index.js',import.meta.url),'utf8');
const worker=(await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`)).default;
const origin='https://svread.pages.dev';
function d1(db){return {prepare(sql){return {bind(...args){return {
  first:async()=>db.prepare(sql).get(...args)||null,
  all:async()=>({results:db.prepare(sql).all(...args)}),
  run:async()=>({meta:{changes:Number(db.prepare(sql).run(...args).changes)}}),
};}};}};}
function req(path,cookie){return new Request('https://worker.example'+path,{headers:{Origin:origin,...(cookie?{Cookie:cookie}:{})}});}

test('ORCID rejects off-site redirects and binds callback to the initiating browser',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32),ORCID_CLIENT_ID:'client',ORCID_CLIENT_SECRET:'secret'};
  const invoke=(path,cookie)=>worker.fetch(req(path,cookie),env);
  assert.equal((await invoke('/api/auth/orcid/start?redirect='+encodeURIComponent('https://evil.example/'))).status,400);
  assert.equal((await invoke('/api/auth/orcid/start?redirect='+encodeURIComponent('//evil.example/'))).status,400);
  const start=await invoke('/api/auth/orcid/start?redirect='+encodeURIComponent('/?work=paramarthasara&view=scholar'));
  assert.equal(start.status,302);
  const target=new URL(start.headers.get('Location'));
  assert.equal(target.origin,'https://orcid.org');
  assert.equal(target.searchParams.get('scope'),'/authenticate');
  const state=target.searchParams.get('state');
  const cookie=start.headers.get('Set-Cookie').split(';')[0];
  assert.match(cookie,/^svorcid=/);
  const callback='/api/auth/orcid/callback?code=example&state='+encodeURIComponent(state);
  assert.equal((await invoke(callback)).status,400);
  assert.equal((await invoke(callback,'svorcid=other')).status,400);
  const original=globalThis.fetch;
  let calls=0;
  globalThis.fetch=async (url,options)=>{
    calls++;assert.equal(String(url),'https://orcid.org/oauth/token');
    assert.equal(options.headers.Accept,'application/json');
    return Response.json({access_token:'mock',orcid:'0000-0002-1825-0097',name:'A Scholar'});
  };
  try{
    const result=await invoke(callback,cookie);
    assert.equal(result.status,302);assert.equal(calls,1);
    assert.equal(result.headers.get('Location'),'https://svread.pages.dev/?work=paramarthasara&view=scholar');
    assert.match(result.headers.get('Set-Cookie'),/svsess=/);
    assert.match(result.headers.get('Set-Cookie'),/svorcid=;/);
    assert.equal(db.prepare('SELECT orcid FROM profiles').get().orcid,'0000-0002-1825-0097');
  }finally{globalThis.fetch=original;db.close();}
});
