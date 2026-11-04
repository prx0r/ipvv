import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {DatabaseSync} from 'node:sqlite';import {createHash} from 'node:crypto';
import worker from '../worker/src/index.js';
const canonical=v=>Array.isArray(v)?'['+v.map(canonical).join(',')+']':v&&typeof v==='object'?'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}':JSON.stringify(v);
const sha=v=>createHash('sha256').update(canonical(v)).digest('hex');
function database(){const db=new DatabaseSync(':memory:');db.exec(fs.readFileSync(new URL('../worker/schema.sql',import.meta.url),'utf8'));return {db,DB:{prepare(sql){return {bind(...args){return {first:async()=>db.prepare(sql).get(...args)||null,all:async()=>({results:db.prepare(sql).all(...args)}),run:async()=>({meta:{changes:Number(db.prepare(sql).run(...args).changes)}})};}};}}};}
function makeProjection(authorId){
 const work='paramarthasara',target='param-p01-v01',title='A scholar on recognition',text='Recognition is a proposed reading.\n\nA second paragraph gives a careful objection.';
 const snap={kind:'essay',work,target,layer:'l3',title,content:{text}},signoff={id:'signoff:test-1',snapshot_sha256:sha(snap),rights:'all-rights-reserved',created_at:'2026-11-04T00:00:00Z'};
 const essay={format:'scholar-essay/1',work,target,title,text,author:'Alice Scholar',author_id:authorId,identity_state:'SELF_ATTESTED',rights:signoff.rights,signoff,snapshot:snap,assisted:false,model:'',validation_scope:'essay structure and declared source links'};
 essay.essay_id='essay:'+sha(essay);
 const originals={t1:{[target]:{verse_id:target,quick_english:'source gloss'}},c1:{'param-p01':{text:'C1 commentary and its stated limits'}}};
 const d={work,source_verses:{[target]:{text:'Sanskrit source'}},originals,original_hashes:{t1:{[target]:sha(originals.t1[target])},c1:{'param-p01':sha(originals.c1['param-p01'])}},withheld_songs:[],l4_craft:{},essays:[essay]};
 d.projection_sha256=sha(d);return {d,essay,work,target};
}
test('only an author can grant exact-version answer and draft use; revocation and references fail closed',async()=>{
 const {db,DB}=database(),env={DB,SESSION_SECRET:'s'.repeat(32),SCHOLAR_DASHSCOPE_API_KEY:'mock',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'20',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'50'};
 const call=(path,method='GET',body,cookie)=>worker.fetch(new Request('https://worker.example'+path,{method,headers:{Origin:'https://svread.pages.dev',...(body?{'Content-Type':'application/json'}:{}),...(cookie?{Cookie:cookie}:{})},...(body?{body:JSON.stringify(body)}:{})}),env);
 async function login(email){const r=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});return {cookie:r.headers.get('Set-Cookie').split(';')[0],profile:(await r.json()).profile};}
 const alice=await login('alice@example.org'),bob=await login('bob@example.org'),{d,essay,work,target}=makeProjection(alice.profile.id);
 const oldFetch=globalThis.fetch;let modelCalls=0,modelText='The author offers an interpretation [E1:p1].',lastPrompt='';
 globalThis.fetch=async(url,opts)=>{if(String(url).includes('/data/scholar/'))return Response.json(d);if(String(url).includes('dashscope')){modelCalls++;lastPrompt=JSON.parse(opts.body).messages[0].content;return Response.json({choices:[{message:{content:modelText}}]});}return oldFetch(url,opts);};
 try{
  let r=await call('/api/scholar/published-essays?work='+work,'GET',null,bob.cookie),listed=(await r.json()).essays;assert.equal(r.status,200);assert.equal(listed[0].owned,false);assert.equal(listed[0].allow_answers,false);
  const grant={work,essay_id:essay.essay_id,allow_answers:true,allow_drafts:false,confirmed:true};
  assert.equal((await call('/api/scholar/essay-permissions','PUT',grant,bob.cookie)).status,403);
  const query={work,target,layer:'l3',kind:'enquiry',instruction:'How does the author explain recognition?',consent_to_ai:true,scholar_essays:[{work,essay_id:essay.essay_id}]};
  assert.equal((await call('/api/scholar/assist','POST',query,bob.cookie)).status,409);assert.equal(modelCalls,0);
  assert.equal((await call('/api/scholar/essay-permissions','PUT',grant,alice.cookie)).status,200);
  const src=await call('/api/scholar/sources','POST',{work,target,note:'Selected note'},bob.cookie),source=(await src.json()).id;assert.equal(src.status,201);
  r=await call('/api/scholar/assist','POST',{...query,source_ids:[source]},bob.cookie);const answer=await r.json();assert.equal(r.status,200,JSON.stringify(answer));
  assert.equal(answer.document.content.scholar_citations[0].marker,'E1:p1');assert.equal(answer.document.content.scholar_citations[0].essay_id,essay.essay_id);
  assert.match(lastPrompt,/C1 commentary/);assert.match(lastPrompt,/Selected note/);assert.match(lastPrompt,/AUTHOR-PERMITTED SCHOLARSHIP/);assert.doesNotMatch(lastPrompt,new RegExp(alice.profile.id.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
  assert.equal((await call('/api/scholar/assist','POST',{...query,kind:'essay'},bob.cookie)).status,409);
  assert.equal((await call('/api/scholar/essay-permissions','PUT',{...grant,allow_drafts:true},alice.cookie)).status,200);
  r=await call('/api/scholar/assist','POST',{...query,kind:'essay'},bob.cookie);assert.equal(r.status,200);
  modelText='An invented marker [E9:p99].';r=await call('/api/scholar/assist','POST',query,bob.cookie);assert.equal(r.status,502);
  modelText='No source marker.';r=await call('/api/scholar/assist','POST',query,bob.cookie);assert.equal(r.status,502);
  assert.equal((await call('/api/scholar/essay-permissions','PUT',{...grant,allow_answers:false,allow_drafts:false},alice.cookie)).status,200);
  assert.equal((await call('/api/scholar/assist','POST',query,bob.cookie)).status,409);
  // Re-hashing the mutable projection cannot disguise a changed essay under its old content address.
  d.essays[0].text='Tampered';delete d.projection_sha256;d.projection_sha256=sha(d);
  assert.notEqual((await call('/api/scholar/published-essays?work='+work,'GET',null,bob.cookie)).status,200);
 }finally{globalThis.fetch=oldFetch;db.close();}
});

test('permission migration is additive, repeatable, and grants nothing by default',()=>{
 const db=new DatabaseSync(':memory:');db.exec("CREATE TABLE profiles (id TEXT PRIMARY KEY); INSERT INTO profiles VALUES ('alice');");
 for(const name of ['0002_scholar_workspace.sql','0003_scholar_history.sql','0004_scholar_ai_limits.sql','0005_scholar_peer_review.sql','0006_scholar_style_examples.sql','0007_scholar_review_versions.sql','0008_scholar_decisions.sql','0009_scholar_review_annotations.sql','0010_scholar_source_notebook.sql','0011_scholar_source_links.sql'])db.exec(fs.readFileSync(new URL('../worker/migrations/'+name,import.meta.url),'utf8'));
 db.exec("INSERT INTO scholar_documents(user_id,id,kind,work,target,layer,title,content_json,revision,updated_at) VALUES ('alice','essay:one','essay','paramarthasara','','','Essay','{\"text\":\"private\"}',1,'2026-11-04');");
 const migration=fs.readFileSync(new URL('../worker/migrations/0012_scholar_essay_permissions.sql',import.meta.url),'utf8');db.exec(migration);db.exec(migration);
 assert.equal(db.prepare('SELECT COUNT(*) AS n FROM scholar_documents').get().n,1);assert.equal(db.prepare('SELECT COUNT(*) AS n FROM scholar_essay_permissions').get().n,0);db.close();
});
