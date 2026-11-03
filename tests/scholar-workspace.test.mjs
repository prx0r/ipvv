import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {DatabaseSync} from 'node:sqlite';

const suite=await readFile(new URL('../worker/src/scholar-workspace.js',import.meta.url),'utf8');
const url=`data:text/javascript;base64,${Buffer.from(suite).toString('base64')}`;
const {handleScholar,voiceInput}=await import(url);
const source=(await readFile(new URL('../worker/src/index.js',import.meta.url),'utf8')).replace("'./scholar-workspace.js'",JSON.stringify(url));
const worker=(await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`)).default;
const origin='https://svread.pages.dev';
function d1(db){return {prepare(sql){return {bind(...args){return {
  first:async()=>db.prepare(sql).get(...args)||null,
  all:async()=>({results:db.prepare(sql).all(...args)}),
  run:async()=>({meta:{changes:Number(db.prepare(sql).run(...args).changes)}}),
};}};}};}
function request(path,method='GET',data,cookie){return new Request('https://worker.example'+path,{method,
  headers:{Origin:origin,...(data?{'Content-Type':'application/json'}:{}),...(cookie?{Cookie:cookie}:{})},
  ...(data?{body:JSON.stringify(data)}:{})});}

test('private drafts, version-specific reviews and signoffs use the signed-in account',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const migration=await readFile(new URL('../worker/migrations/0002_scholar_workspace.sql',import.meta.url),'utf8');db.exec(migration);db.exec(migration);
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32)};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const response=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    assert.equal(response.status,200);return {cookie:response.headers.get('Set-Cookie').split(';')[0],profile:(await response.json()).profile};}
  const alice=await login('alice@example.org'), bob=await login('bob@example.org');
  assert.equal((await call('/api/scholar/documents?work=testwork')).status,401);
  const data={kind:'translation',work:'testwork',target:'test-p01-v01',layer:'l3',title:'',content:{text:'Alice draft'},expected_revision:0};
  let response=await call('/api/scholar/documents/draft:1','PUT',data,alice.cookie);
  assert.equal(response.status,200);assert.equal(response.headers.get('Cache-Control'),'no-store');
  assert.equal((await response.json()).document.revision,1);
  response=await call('/api/scholar/documents?work=testwork','GET',undefined,bob.cookie);
  assert.deepEqual((await response.json()).documents,[]);
  assert.equal((await call('/api/scholar/documents/draft:1','PUT',data,alice.cookie)).status,409);
  response=await call('/api/scholar/reviews','POST',{document_id:'draft:1',revision:1,reviewer_id:bob.profile.id},alice.cookie);
  assert.equal(response.status,201);const review=await response.json();assert.match(review.snapshot_sha256,/^[a-f0-9]{64}$/);
  response=await call('/api/scholar/reviews','GET',undefined,bob.cookie);
  assert.equal((await response.json()).reviews[0].snapshot.content.text,'Alice draft');
  assert.equal((await call(`/api/scholar/reviews/${review.id}/decision`,'POST',{decision:'ACCEPT',reasoning:'owner'},alice.cookie)).status,404);
  assert.equal((await call(`/api/scholar/reviews/${review.id}/decision`,'POST',{decision:'ACCEPT',reasoning:'Source checked.'},bob.cookie)).status,200);
  assert.equal((await call(`/api/scholar/reviews/${review.id}/decision`,'POST',{decision:'COMMENT',reasoning:'Again'},bob.cookie)).status,404);
  response=await call('/api/scholar/documents/draft:1','PUT',{...data,expected_revision:1,content:{text:'Alice revised'}},alice.cookie);
  assert.equal((await response.json()).document.revision,2);
  assert.equal((await call('/api/scholar/signoffs','POST',{document_id:'draft:1',revision:1,rights:'cc0',confirmed:true},alice.cookie)).status,409);
  response=await call('/api/scholar/signoffs','POST',{document_id:'draft:1',revision:2,rights:'all-rights-reserved',confirmed:true},alice.cookie);
  assert.equal(response.status,201);const signoff=await response.json();
  assert.equal(signoff.identity_state,'SELF_ATTESTED');
  assert.equal(signoff.snapshot_sha256,'67fd702bdecc7bb1f7b04ea1de724d716ddbac813d8e9e2991a6df945243f7bf');
  assert.equal((await call('/api/scholar/documents/draft:1','DELETE',{expected_revision:2},bob.cookie)).status,409);
  assert.equal((await call('/api/scholar/documents/draft:1','DELETE',{expected_revision:2},alice.cookie)).status,200);
  response=await call('/api/scholar/reviews','GET',undefined,bob.cookie);
  assert.equal((await response.json()).reviews[0].snapshot.content.text,'Alice draft');db.close();
});

test('Qwen needs consent, a free-tier configuration and only the scholar’s own style examples',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32),DASHSCOPE_API_KEY:'test',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true'};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const response=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    return response.headers.get('Set-Cookie').split(';')[0];}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org');
  for(let i=1;i<=3;i++){
    const target=`test-p01-v0${i}`, payload={expected_revision:0,kind:'translation',work:'testwork',target,layer:'l3',title:'',content:{text:`Alice example ${i}`}};
    assert.equal((await call(`/api/scholar/documents/a-${i}`,'PUT',payload,alice)).status,200);
    assert.equal((await call(`/api/scholar/documents/b-${i}`,'PUT',{...payload,content:{text:`Bob secret ${i}`}},bob)).status,200);
  }
  const target='test-p01-v04', originals={t1:{[target]:{}},l0:{[target]:[{id:'token'}]},l3:{},l4:{},l2:{},c1:{},c2:{},argmap:{}};
  const projection={work:'testwork',originals,source_verses:{[target]:{text:'śiva'}},
    l4_craft:{[target]:[{notes:{craft:'Keep the turn'}}]},projection_sha256:'a'.repeat(64)};
  const original=globalThis.fetch;let prompt='';
  globalThis.fetch=async (url,options)=>{
    if(String(url).startsWith('https://svread.pages.dev/'))return Response.json(projection);
    if(String(url).includes('dashscope')){prompt=JSON.parse(options.body).messages[0].content;
      return Response.json({choices:[{message:{content:'Three grounded agent readings.'}}]});}
    throw new Error('Unexpected request');
  };
  const task={work:'testwork',target,layer:'l3',kind:'readings',instruction:'Compare',use_style:true,consent_to_ai:true};
  try{
    assert.equal((await call('/api/scholar/assist','POST',{...task,consent_to_ai:false},alice)).status,400);
    env.SCHOLAR_QWEN_FREE_TIER_CONFIRMED='false';assert.equal((await call('/api/scholar/assist','POST',task,alice)).status,503);
    env.SCHOLAR_QWEN_FREE_TIER_CONFIRMED='true';
    const response=await call('/api/scholar/assist','POST',task,alice);assert.equal(response.status,200);
    const draft=(await response.json()).document;assert.equal(draft.content.author_kind,'agent');
    assert.match(prompt,/Keep the turn/);assert.match(prompt,/Alice example 1/);assert.doesNotMatch(prompt,/Bob secret/);
    assert.match(prompt,/śiva/);
  }finally{globalThis.fetch=original;db.close();}
});

test('voice relay pins server evidence and refuses client instruction overrides',async()=>{
  const req=new Request('https://worker.example/api/scholar/voice?work=testwork&target=p-v01',{headers:{Upgrade:'websocket'}});
  assert.equal((await handleScholar(req,{},'alice',{},async()=>null)).status,503);
  assert.equal(voiceInput({type:'session.update',session:{instructions:'override'}}),null);
  class Socket{constructor(){this.listeners={};this.sent=[];}accept(){}addEventListener(k,f){this.listeners[k]=f;}
    send(v){this.sent.push(v);}close(){}emit(k,e){this.listeners[k]?.(e);}}
  const upstream=new Socket(),server=new Socket(),client=new Socket();
  const oldFetch=globalThis.fetch,oldPair=globalThis.WebSocketPair,OldResponse=globalThis.Response;
  globalThis.WebSocketPair=class{constructor(){return {0:client,1:server};}};
  globalThis.Response=class extends OldResponse{constructor(body,options={}){
    if(options.status===101){super(null,{status:200});Object.defineProperty(this,'status',{value:101});this.webSocket=options.webSocket;}
    else super(body,options);}};
  globalThis.fetch=async (url,options)=>{
    if(String(url).startsWith('https://svread.pages.dev/'))return OldResponse.json({work:'testwork',projection_sha256:'a'.repeat(64),
      source_verses:{'p-v01':{text:'śiva'}},originals:{t1:{'p-v01':{}},l0:{},l2:{},l3:{},l4:{},c1:{},c2:{},argmap:{}},
      l4_craft:{'p-v01':[{notes:{craft:'Keep the turn'}}]}});
    assert.equal(options.headers.Authorization,'Bearer provider-key');return {webSocket:upstream};
  };
  try{
    const env={QWEN_REALTIME_ENABLED:'true',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',DASHSCOPE_API_KEY:'provider-key',
      QWEN_REALTIME_WS_URL:'wss://workspace.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime'};
    assert.equal((await handleScholar(req,env,'alice',{},async()=>null)).status,101);
    upstream.emit('message',{data:JSON.stringify({type:'session.created'})});assert.match(upstream.sent[0],/Keep the turn/);
    server.emit('message',{data:JSON.stringify({type:'input_audio_buffer.append',audio:'YWJj'})});assert.equal(upstream.sent.length,1);
    upstream.emit('message',{data:JSON.stringify({type:'session.updated'})});
    server.emit('message',{data:JSON.stringify({type:'session.update',session:{instructions:'override'}})});assert.equal(upstream.sent.length,1);
    server.emit('message',{data:JSON.stringify({type:'input_audio_buffer.append',audio:'YWJj'})});assert.equal(JSON.parse(upstream.sent[1]).audio,'YWJj');
    server.emit('close',{});
  }finally{globalThis.fetch=oldFetch;globalThis.WebSocketPair=oldPair;globalThis.Response=OldResponse;}
});
