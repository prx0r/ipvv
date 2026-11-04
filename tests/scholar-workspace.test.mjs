import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {DatabaseSync} from 'node:sqlite';
import {createHash,createHmac} from 'node:crypto';

const suite=await readFile(new URL('../worker/src/scholar-workspace.js',import.meta.url),'utf8');
const url=`data:text/javascript;base64,${Buffer.from(suite).toString('base64')}`;
const {handleScholar,voiceInput}=await import(url);
const source=(await readFile(new URL('../worker/src/index.js',import.meta.url),'utf8')).replace("'./scholar-workspace.js'",JSON.stringify(url));
const worker=(await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`)).default;
const origin='https://svread.pages.dev';
const canonicalFixture=value=>Array.isArray(value)?'['+value.map(canonicalFixture).join(',')+']':value&&typeof value==='object'?'{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonicalFixture(value[k])).join(',')+'}':JSON.stringify(value);
const fixtureDigest=value=>createHash('sha256').update(canonicalFixture(value)).digest('hex');
function projectionFixture(data){
  const {projection_sha256,...body}=data;body.withheld_songs=body.withheld_songs||[];
  body.original_hashes=Object.fromEntries(Object.entries(body.originals).map(([layer,values])=>[layer,Object.fromEntries(Object.entries(values).map(([key,value])=>[key,fixtureDigest(value)]))]));
  return {...body,projection_sha256:fixtureDigest(body)};
}

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
  env.SCHOLAR_BRIDGE_URL='https://bridge.example';env.SCHOLAR_BRIDGE_SECRET='x'.repeat(40);
  const oldFetch=globalThis.fetch;
  globalThis.fetch=async (url,options)=>{
    assert.equal(String(url),'https://bridge.example/v1/scholar/account-submissions');
    const raw=options.body,stamp=options.headers['X-Scholar-Time'];
    const hash=createHash('sha256').update(raw).digest('hex');
    assert.equal(options.headers['X-Scholar-Signature'],createHmac('sha256',env.SCHOLAR_BRIDGE_SECRET)
      .update(`scholar-bridge/v1\n${stamp}\n${hash}`).digest('hex'));
    const payload=JSON.parse(raw);assert.equal(payload.account_id,alice.profile.id);
    assert.equal(payload.signoff.snapshot_sha256,signoff.snapshot_sha256);
    return Response.json({branch:'scholar/submission-test',commit:'a'.repeat(40),remote_pushed:true});
  };
  try{
    response=await call('/api/scholar/submit','POST',{signoff_id:signoff.id,confirm_submission:true},alice.cookie);
    assert.equal(response.status,201);assert.equal((await response.json()).status,'SUBMITTED_PUBLIC_BRANCH');
  }finally{globalThis.fetch=oldFetch;}
  assert.equal((await call('/api/scholar/documents/draft:1','PUT',{...data,expected_revision:2,content:{text:'Later edit'}},alice.cookie)).status,200);
  assert.equal((await call('/api/scholar/submit','POST',{signoff_id:signoff.id,confirm_submission:true},alice.cookie)).status,409);
  assert.equal((await call('/api/scholar/documents/draft:1','DELETE',{expected_revision:3},bob.cookie)).status,409);
  assert.equal((await call('/api/scholar/documents/draft:1','DELETE',{expected_revision:3},alice.cookie)).status,200);
  response=await call('/api/scholar/reviews','GET',undefined,bob.cookie);
  assert.equal((await response.json()).reviews[0].snapshot.content.text,'Alice draft');db.close();
});

test('private revision history is atomic, account-scoped, backfilled and deleted with the draft',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  // Simulate an existing deployment before the history migration.
  db.exec('DROP TRIGGER scholar_history_insert; DROP TRIGGER scholar_history_update; DROP TRIGGER scholar_history_delete; DROP TABLE scholar_document_history;');
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32)};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const response=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    return response.headers.get('Set-Cookie').split(';')[0];}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org');
  const path='/api/scholar/documents/private:1';
  const draft={kind:'translation',work:'testwork',target:'test-p01-v01',layer:'l3',title:'',content:{text:'First'},expected_revision:0};
  assert.equal((await call(path,'PUT',draft,alice)).status,200);
  assert.equal((await call(path,'PUT',{...draft,expected_revision:1,content:{text:'Before migration'}},alice)).status,200);
  const migration=await readFile(new URL('../worker/migrations/0003_scholar_history.sql',import.meta.url),'utf8');
  db.exec(migration);db.exec(migration);
  assert.equal((await call(path,'PUT',{...draft,expected_revision:2,content:{text:'New snapshot'}},alice)).status,200);
  assert.equal((await call(path,'PUT',{...draft,expected_revision:2,content:{text:'Conflicting edit'}},alice)).status,409);
  let response=await call(path+'/history','GET',undefined,alice);
  assert.equal(response.status,200);assert.equal(response.headers.get('Cache-Control'),'no-store');
  let history=(await response.json()).revisions;
  assert.deepEqual(history.map(x=>[x.revision,x.content.text]),[[3,'New snapshot'],[2,'Before migration']]);
  response=await call(path+'/history?before=3','GET',undefined,alice);
  assert.deepEqual((await response.json()).revisions.map(x=>x.revision),[2]);
  assert.equal((await call(path+'/history?before=bad','GET',undefined,alice)).status,400);
  assert.equal((await call(path+'/history','GET',undefined,bob)).status,404);
  assert.equal((await call(path,'DELETE',{expected_revision:3},alice)).status,200);
  assert.equal(db.prepare('SELECT COUNT(*) AS n FROM scholar_document_history').get().n,0);
  assert.equal((await call(path+'/history','GET',undefined,alice)).status,404);db.close();
});

test('essay peer reviews have a structured report and participant-only discussion',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const migration=await readFile(new URL('../worker/migrations/0005_scholar_peer_review.sql',import.meta.url),'utf8');db.exec(migration);db.exec(migration);
  const versionMigration=await readFile(new URL('../worker/migrations/0007_scholar_review_versions.sql',import.meta.url),'utf8');db.exec(versionMigration);db.exec(versionMigration);
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32)};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const response=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    return {cookie:response.headers.get('Set-Cookie').split(';')[0],profile:(await response.json()).profile};}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org'),eve=await login('eve@example.org');
  const essay={expected_revision:0,kind:'essay',work:'testwork',target:'test-p01-v01',layer:'l3',title:'My argument',content:{text:'Essay under review.'}};
  assert.equal((await call('/api/scholar/documents/essay:1','PUT',essay,alice.cookie)).status,200);
  const invite=await call('/api/scholar/reviews','POST',{document_id:'essay:1',revision:1,reviewer_id:bob.profile.id},alice.cookie);
  const review=await invite.json(),path='/api/scholar/reviews/'+review.id;
  const report={decision:'REQUEST_CHANGES',reasoning:'Strengthen the evidence.',rubric:{argument:'Claim needs support.',evidence:'Cite the source.'},ai_consent:false};
  assert.equal((await call(path+'/decision','POST',report,eve.cookie)).status,404);
  assert.equal((await call(path+'/decision','POST',{...report,rubric:{evil:'unexpected'}},bob.cookie)).status,400);
  assert.equal((await call(path+'/decision','POST',report,bob.cookie)).status,200);
  let listed=await call('/api/scholar/reviews','GET',undefined,alice.cookie);let visible=(await listed.json()).reviews[0];
  assert.equal(visible.snapshot_sha256,review.snapshot_sha256);assert.equal(visible.rubric.evidence,'Cite the source.');assert.equal(visible.ai_consent,false);
  assert.equal((await call(path+'/ai-consent','POST',{allow:true},alice.cookie)).status,404);
  assert.equal((await call(path+'/ai-consent','POST',{allow:true},bob.cookie)).status,200);
  listed=await call('/api/scholar/reviews','GET',undefined,alice.cookie);assert.equal((await listed.json()).reviews[0].ai_consent,true);
  assert.equal((await call(path+'/messages','POST',{text:'Which source would strengthen it?'},alice.cookie)).status,201);
  assert.equal((await call(path+'/messages','POST',{text:'Check the quoted passage.'},bob.cookie)).status,201);
  assert.equal((await call(path+'/messages','GET',undefined,eve.cookie)).status,404);
  assert.equal((await call(path+'/messages','POST',{text:'Intrusion'},eve.cookie)).status,404);
  const thread=await call(path+'/messages','GET',undefined,bob.cookie);assert.equal((await thread.json()).messages.length,2);
  const revised={expected_revision:1,decision:'ACCEPT',reasoning:'Evidence now clear.',rubric:{evidence:'Source checked.'},ai_consent:true};
  assert.equal((await call(path+'/revise','POST',revised,alice.cookie)).status,409);
  assert.equal((await call(path+'/revise','POST',revised,bob.cookie)).status,200);
  assert.equal((await call(path+'/revise','POST',revised,bob.cookie)).status,409);
  const reports=await call(path+'/report-history','GET',undefined,alice.cookie),versions=(await reports.json()).reports;
  assert.deepEqual(versions.map(v=>v.revision),[2,1]);assert.equal(versions[1].summary,'Strengthen the evidence.');
  assert.equal((await call(path+'/report-history','GET',undefined,eve.cookie)).status,404);
  listed=await call('/api/scholar/reviews','GET',undefined,alice.cookie);visible=(await listed.json()).reviews[0];
  assert.equal(visible.report_revision,2);assert.equal(visible.decision,'ACCEPT');assert.equal(visible.snapshot_sha256,review.snapshot_sha256);
  assert.equal((await call(path+'/ai-consent','POST',{allow:false},bob.cookie)).status,200);
  listed=await call('/api/scholar/reviews','GET',undefined,alice.cookie);assert.equal((await listed.json()).reviews[0].ai_consent,false);
  db.close();
});

test('review annotations bind exact snapshot spans and remain private to participants',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const migration=await readFile(new URL('../worker/migrations/0009_scholar_review_annotations.sql',import.meta.url),'utf8');db.exec(migration);db.exec(migration);
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32)};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const r=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    return {cookie:r.headers.get('Set-Cookie').split(';')[0],profile:(await r.json()).profile};}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org'),eve=await login('eve@example.org');
  const essay={expected_revision:0,kind:'essay',work:'testwork',target:'p-v01',layer:'l3',title:'',content:{text:'🕉 Śiva is free'}};
  assert.equal((await call('/api/scholar/documents/e','PUT',essay,alice.cookie)).status,200);
  const share=await call('/api/scholar/reviews','POST',{document_id:'e',revision:1,reviewer_id:bob.profile.id},alice.cookie);const review=await share.json();
  const url='/api/scholar/reviews/'+review.id+'/annotations';
  assert.equal((await call(url,'GET',undefined,eve.cookie)).status,404);
  const note={start:3,end:7,quote:'Śiva',body:'Explain the source.'};
  assert.equal((await call(url,'POST',{...note,start:2},bob.cookie)).status,400);
  assert.equal((await call(url,'POST',note,eve.cookie)).status,404);
  let response=await call(url,'POST',note,bob.cookie);assert.equal(response.status,201);const annotation=await response.json();
  assert.equal(annotation.snapshot_sha256,review.snapshot_sha256);
  assert.equal((await call('/api/scholar/documents/e','PUT',{...essay,expected_revision:1,content:{text:'Changed essay'}},alice.cookie)).status,200);
  response=await call(url,'GET',undefined,alice.cookie);const rows=(await response.json()).annotations;
  assert.equal(rows[0].quote,'Śiva');assert.equal(rows[0].start_offset,3);assert.equal(rows[0].snapshot_sha256,review.snapshot_sha256);
  assert.equal((await call('/api/scholar/review-annotations/'+annotation.id,'DELETE',{},alice.cookie)).status,404);
  assert.equal((await call('/api/scholar/review-annotations/'+annotation.id,'DELETE',{},bob.cookie)).status,200);
  assert.deepEqual((await (await call(url,'GET',undefined,bob.cookie)).json()).annotations,[]);db.close();
});

test('ordered migrations preserve earlier review decisions without granting AI permission',async()=>{
  const db=new DatabaseSync(':memory:');db.exec("CREATE TABLE profiles (id TEXT PRIMARY KEY); INSERT INTO profiles VALUES ('alice'),('bob');");
  const read=async file=>readFile(new URL('../worker/migrations/'+file,import.meta.url),'utf8');
  const names=['0002_scholar_workspace.sql','0003_scholar_history.sql','0004_scholar_ai_limits.sql',
    '0005_scholar_peer_review.sql','0006_scholar_style_examples.sql','0007_scholar_review_versions.sql'];
  db.exec(await read(names[0]));
  db.exec(`INSERT INTO scholar_reviews (id,owner_id,reviewer_id,work,document_id,revision,snapshot_json,snapshot_sha256,decision,reasoning,created_at,decided_at)
    VALUES ('old-review','alice','bob','testwork','essay',1,'{}','hash','COMMENT','Earlier review','2026-01-01','2026-01-02')`);
  for(const name of names.slice(1))db.exec(await read(name));
  for(const name of names)db.exec(await read(name));
  const report=db.prepare("SELECT * FROM scholar_review_reports WHERE review_id='old-review'").get();
  const versions=db.prepare("SELECT * FROM scholar_review_report_versions WHERE review_id='old-review'").all();
  assert.equal(report.ai_consent,0);assert.equal(report.summary,'Earlier review');
  assert.equal(versions.length,1);assert.equal(versions[0].revision,1);assert.equal(versions[0].summary,'Earlier review');db.close();
});

test('authors can explicitly save and revoke private before-and-after style examples',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const migration=await readFile(new URL('../worker/migrations/0006_scholar_style_examples.sql',import.meta.url),'utf8');db.exec(migration);db.exec(migration);
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32)};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const response=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    return response.headers.get('Set-Cookie').split(';')[0];}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org');
  const essay={expected_revision:0,kind:'essay',work:'testwork',target:'test-p01-v01',layer:'l3',title:'Essay',content:{text:'First wording'}};
  assert.equal((await call('/api/scholar/documents/essay:1','PUT',essay,alice)).status,200);
  assert.equal((await call('/api/scholar/documents/essay:1','PUT',{...essay,expected_revision:1,content:{text:'Revised wording',assisted:true}},alice)).status,200);
  const pair={document_id:'essay:1',before_revision:1,after_revision:2,confirmed:true};
  assert.equal((await call('/api/scholar/style-examples','POST',{...pair,confirmed:false},alice)).status,400);
  assert.equal((await call('/api/scholar/style-examples','POST',pair,bob)).status,404);
  let response=await call('/api/scholar/style-examples','POST',pair,alice);assert.equal(response.status,201);const example=await response.json();
  assert.equal((await call('/api/scholar/style-examples','POST',pair,alice)).status,409);
  response=await call('/api/scholar/style-examples','GET',undefined,bob);assert.deepEqual((await response.json()).examples,[]);
  response=await call('/api/scholar/style-examples','GET',undefined,alice);const examples=(await response.json()).examples;
  assert.equal(examples[0].id,example.id);assert.equal(JSON.stringify(examples).includes('Revised wording'),false);
  assert.equal((await call('/api/scholar/style-examples/'+example.id,'DELETE',undefined,bob)).status,404);
  assert.equal((await call('/api/scholar/documents/essay:1','DELETE',{expected_revision:2},alice)).status,200);
  assert.equal(db.prepare('SELECT COUNT(*) AS n FROM scholar_style_examples').get().n,0);db.close();
});

test('private decisions are revision-bound, account-scoped, revocable and sent only when selected',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const migration=await readFile(new URL('../worker/migrations/0008_scholar_decisions.sql',import.meta.url),'utf8');db.exec(migration);db.exec(migration);
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32),SCHOLAR_DASHSCOPE_API_KEY:'test',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',
    SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'10',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'20'};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const r=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});return r.headers.get('Set-Cookie').split(';')[0];}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org');
  const saved={expected_revision:0,kind:'translation',work:'testwork',target:'test-p01-v01',layer:'l3',title:'',content:{text:'My sovereignty'}};
  assert.equal((await call('/api/scholar/documents/a','PUT',saved,alice)).status,200);
  const choice={document_id:'a',revision:1,subject:'svātantrya',before:'freedom',after:'sovereignty',reason:'Context of agency'};
  assert.equal((await call('/api/scholar/decisions','POST',choice,bob)).status,404);
  const response=await call('/api/scholar/decisions','POST',choice,alice);assert.equal(response.status,201);const decision=await response.json();
  assert.match(decision.snapshot_sha256,/^[a-f0-9]{64}$/);
  assert.deepEqual((await (await call('/api/scholar/decisions','GET',undefined,bob)).json()).decisions,[]);
  assert.equal((await (await call('/api/scholar/decisions?work=testwork','GET',undefined,alice)).json()).decisions[0].subject,'svātantrya');
  let modelCalls=0,prompt='';const original=globalThis.fetch;
  globalThis.fetch=async (url,options)=>{
    if(String(url).startsWith('https://svread.pages.dev/'))return Response.json(projectionFixture({work:'testwork',
      source_verses:{'test-p01-v01':{text:'śiva'}},originals:{t1:{'test-p01-v01':{}},l0:{},l2:{},l3:{},l4:{},c1:{},c2:{},argmap:{}}}));
    if(String(url).includes('dashscope')){modelCalls++;prompt=JSON.parse(options.body).messages[0].content;return Response.json({choices:[{message:{content:'Draft'}}]});}
    throw new Error('Unexpected request');
  };
  const task={work:'testwork',target:'test-p01-v01',layer:'l3',kind:'translation',instruction:'',use_style:true,consent_to_ai:true,decision_ids:[decision.id]};
  try{
    assert.equal((await call('/api/scholar/assist','POST',{...task,consent_to_ai:false},alice)).status,400);
    assert.equal((await call('/api/scholar/assist','POST',{...task,use_style:false},alice)).status,400);
    assert.equal((await call('/api/scholar/assist','POST',task,bob)).status,409);assert.equal(modelCalls,0);
    const generated=await call('/api/scholar/assist','POST',task,alice);assert.equal(generated.status,200);
    assert.match(prompt,/Context of agency/);assert.doesNotMatch(prompt,/My sovereignty/);
    const generatedDoc=(await generated.json()).document;assert.equal(generatedDoc.content.used_style,true);assert.deepEqual(generatedDoc.content.decision_ids,[decision.id]);
    assert.equal((await call('/api/scholar/decisions/'+decision.id,'DELETE',{},bob)).status,404);
    assert.equal((await call('/api/scholar/decisions/'+decision.id,'DELETE',{},alice)).status,200);
    assert.equal((await call('/api/scholar/assist','POST',task,alice)).status,409);assert.equal(modelCalls,1);
    const again=await call('/api/scholar/decisions','POST',choice,alice);assert.equal(again.status,201);
    assert.equal((await call('/api/scholar/documents/a','DELETE',{expected_revision:1},alice)).status,200);
    assert.equal(db.prepare('SELECT COUNT(*) AS n FROM scholar_decisions').get().n,0);
  }finally{globalThis.fetch=original;db.close();}
});

test('essay notebook shares only selected private sources and rejects changed evidence',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const migration=await readFile(new URL('../worker/migrations/0010_scholar_source_notebook.sql',import.meta.url),'utf8');db.exec(migration);db.exec(migration);
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32),SCHOLAR_DASHSCOPE_API_KEY:'test',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',
    SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'10',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'20'};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const r=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});return r.headers.get('Set-Cookie').split(';')[0];}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org');
  const make=(work,text)=>projectionFixture({work,source_verses:{'p-v01':{text}},originals:{t1:{'p-v01':{}},l0:{},argmap:{},l2:{},l3:{},l4:{},c1:{},c2:{}}});
  const base=make('testwork','śiva');let other=make('otherwork','śakti'),prompt='',calls=0;const original=globalThis.fetch;
  globalThis.fetch=async(url,options)=>{
    if(String(url).includes('/data/scholar/testwork.json'))return Response.json(base);
    if(String(url).includes('/data/scholar/otherwork.json'))return Response.json(other);
    if(String(url).includes('dashscope')){calls++;prompt=JSON.parse(options.body).messages[0].content;return Response.json({choices:[{message:{content:'Draft'}}]});}
    throw new Error('Unexpected request');
  };
  try{
    assert.equal((await call('/api/scholar/sources','POST',{work:'ghatakarpara',target:'p-v01',note:''},alice)).status,400);
    let r=await call('/api/scholar/sources','POST',{work:'otherwork',target:'p-v01',note:'Private note'},alice);
    assert.equal(r.status,201);const source=(await r.json()).id;
    assert.deepEqual((await (await call('/api/scholar/sources','GET',undefined,bob)).json()).sources,[]);
    const task={work:'testwork',target:'p-v01',layer:'l3',kind:'essay',instruction:'',use_style:false,consent_to_ai:true,source_ids:[source]};
    assert.equal((await call('/api/scholar/assist','POST',task,bob)).status,409);assert.equal(calls,0);
    assert.equal((await call('/api/scholar/assist','POST',{...task,kind:'translation'},alice)).status,400);
    r=await call('/api/scholar/assist','POST',{...task,source_ids:[]},alice);assert.equal(r.status,200);assert.doesNotMatch(prompt,/Private note/);
    r=await call('/api/scholar/assist','POST',task,alice);assert.equal(r.status,200);assert.match(prompt,/Private note/);assert.match(prompt,/śakti/);
    const draft=(await r.json()).document;assert.equal(draft.content.source_references[0].id,source);
    other=make('otherwork','changed source');assert.equal((await call('/api/scholar/assist','POST',task,alice)).status,409);assert.equal(calls,2);
    assert.equal((await call('/api/scholar/sources/'+source,'DELETE',{},bob)).status,404);
    assert.equal((await call('/api/scholar/sources/'+source,'DELETE',{},alice)).status,200);
  }finally{globalThis.fetch=original;db.close();}
});

test('essay revision uses only selected, permitted feedback and author-owned style edits',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32),SCHOLAR_DASHSCOPE_API_KEY:'test',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',
    SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'10',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'20'};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const response=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    return {cookie:response.headers.get('Set-Cookie').split(';')[0],profile:(await response.json()).profile};}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org');
  const essay={expected_revision:0,kind:'essay',work:'testwork',target:'test-p01-v01',layer:'l3',title:'Essay',content:{text:'My first wording'}};
  assert.equal((await call('/api/scholar/documents/a','PUT',essay,alice.cookie)).status,200);
  assert.equal((await call('/api/scholar/documents/a','PUT',{...essay,expected_revision:1,content:{text:'My edited wording'}},alice.cookie)).status,200);
  let response=await call('/api/scholar/style-examples','POST',{document_id:'a',before_revision:1,after_revision:2,confirmed:true},alice.cookie);
  const own=(await response.json()).id;
  assert.equal((await call('/api/scholar/documents/b','PUT',{...essay,content:{text:'Bob secret first'}},bob.cookie)).status,200);
  assert.equal((await call('/api/scholar/documents/b','PUT',{...essay,expected_revision:1,content:{text:'Bob secret edited'}},bob.cookie)).status,200);
  response=await call('/api/scholar/style-examples','POST',{document_id:'b',before_revision:1,after_revision:2,confirmed:true},bob.cookie);
  const other=(await response.json()).id;
  response=await call('/api/scholar/reviews','POST',{document_id:'a',revision:2,reviewer_id:bob.profile.id},alice.cookie);
  const review=await response.json(),reviewPath='/api/scholar/reviews/'+review.id;
  assert.equal((await call(reviewPath+'/decision','POST',{decision:'REQUEST_CHANGES',reasoning:'Explain the evidence.',rubric:{evidence:'Give a precise source.'},ai_consent:false},bob.cookie)).status,200);
  assert.equal((await call(reviewPath+'/messages','POST',{text:'Private discussion never sent automatically.'},bob.cookie)).status,201);
  const original=globalThis.fetch;let prompt='',modelCalls=0;
  globalThis.fetch=async (url,options)=>{
    if(String(url).startsWith('https://svread.pages.dev/'))return Response.json(projectionFixture({work:'testwork',
      source_verses:{'test-p01-v01':{text:'śiva'}},originals:{t1:{'test-p01-v01':{}},l0:{},l2:{},l3:{},l4:{},c1:{},c2:{},argmap:{}}}));
    if(String(url).includes('dashscope')){modelCalls++;prompt=JSON.parse(options.body).messages[0].content;
      return Response.json({choices:[{message:{content:'Draft with citation gaps.'}}]});}
    throw new Error('Unexpected request');
  };
  const task={kind:'essay_revision',document_id:'a',revision:2,work:'testwork',target:'test-p01-v01',layer:'l3',
    instruction:'Improve the argument',use_style:true,style_example_ids:[own],review_ids:[review.id],consent_to_ai:true};
  try{
    assert.equal((await call('/api/scholar/assist','POST',task,alice.cookie)).status,409);assert.equal(modelCalls,0);
    assert.equal((await call(reviewPath+'/ai-consent','POST',{allow:true},bob.cookie)).status,200);
    assert.equal((await call('/api/scholar/assist','POST',{...task,style_example_ids:[other]},alice.cookie)).status,409);assert.equal(modelCalls,0);
    response=await call('/api/scholar/assist','POST',{...task,use_style:false,style_example_ids:[],review_ids:[]},alice.cookie);
    assert.equal(response.status,200);assert.doesNotMatch(prompt,/Explain the evidence|My first wording|Private discussion/);
    response=await call('/api/scholar/assist','POST',task,alice.cookie);assert.equal(response.status,200);
    const agent=(await response.json()).document;assert.equal(agent.content.task,'essay_revision');assert.equal(agent.content.source_revision,2);
    assert.equal(agent.content.review_versions[0].revision,1);assert.match(agent.content.review_versions[0].sha256,/^[a-f0-9]{64}$/);
    assert.match(prompt,/My first wording/);assert.match(prompt,/My edited wording/);assert.match(prompt,/Explain the evidence/);
    assert.match(prompt,/Give a precise source/);assert.doesNotMatch(prompt,/Bob secret|Private discussion/);
    assert.equal((await call(reviewPath+'/ai-consent','POST',{allow:false},bob.cookie)).status,200);
    assert.equal((await call('/api/scholar/assist','POST',task,alice.cookie)).status,409);
    assert.equal((await call('/api/scholar/documents/a','PUT',{...essay,expected_revision:2,content:{text:'A newer version'}},alice.cookie)).status,200);
    assert.equal((await call('/api/scholar/assist','POST',{...task,review_ids:[]},alice.cookie)).status,409);
  }finally{globalThis.fetch=original;db.close();}
});

test('Qwen needs consent, a free-tier configuration and only the scholar’s own style examples',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32),SCHOLAR_DASHSCOPE_API_KEY:'test',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',
    SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'5',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'10'};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const response=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    return response.headers.get('Set-Cookie').split(';')[0];}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org');
  for(let i=1;i<=3;i++){
    const target=`test-p01-v0${i}`, payload={expected_revision:0,kind:'translation',work:'testwork',target,layer:'l3',title:'',content:{text:`Alice example ${i}`}};
    assert.equal((await call(`/api/scholar/documents/a-${i}`,'PUT',payload,alice)).status,200);
    assert.equal((await call(`/api/scholar/documents/b-${i}`,'PUT',{...payload,content:{text:`Bob secret ${i}`}},bob)).status,200);
  }
  const target='test-p01-v04', originals={t1:{[target]:{}},l0:{[target]:[{id:'token'}],
    'test-p01-v01':[{id:'l0-token',surface:'cit',chosen_index:0,options:[{gloss:'consciousness'},{gloss:'awareness',grounds:'context'}]}]},
    l3:{},l4:{},l2:{},c1:{},c2:{},argmap:{}};
  const lexical={expected_revision:0,kind:'translation',work:'testwork',target:'test-p01-v01',layer:'l0',title:'',
    content:{text:JSON.stringify([{id:'l0-token',surface:'cit',chosen_index:1,options:[{gloss:'consciousness'},{gloss:'awareness',grounds:'context'}]}])}};
  assert.equal((await call('/api/scholar/documents/l0-draft','PUT',lexical,alice)).status,200);
  const projection=projectionFixture({work:'testwork',originals,source_verses:{[target]:{text:'śiva'}},
    l4_craft:{[target]:[{notes:{craft:'Keep the turn'}}]}});
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
    const held=await call('/api/scholar/assist','POST',{...task,work:'ghatakarpara'},alice);
    assert.notEqual(held.status,200);assert.match((await held.json()).error,/withheld/i);assert.equal(prompt,'');
    const response=await call('/api/scholar/assist','POST',task,alice);assert.equal(response.status,200);
    const draft=(await response.json()).document;assert.equal(draft.content.author_kind,'agent');
    assert.match(prompt,/Keep the turn/);assert.match(prompt,/Alice example 1/);assert.doesNotMatch(prompt,/Bob secret/);
    assert.match(prompt,/"chosen":"awareness"/);
    assert.match(prompt,/śiva/);
  }finally{globalThis.fetch=original;db.close();}
});

test('AI evidence rejects changed projection, mismatched layer hashes and withheld passages',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  db.exec("INSERT INTO profiles (id,email,display_name) VALUES ('alice','alice@example.org','Alice')");
  const env={DB:d1(db),SCHOLAR_DASHSCOPE_API_KEY:'test',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'5',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'5'};
  const task={work:'testwork',target:'p-v01',layer:'l3',kind:'readings',instruction:'',use_style:false,consent_to_ai:true};
  const good=projectionFixture({work:'testwork',source_verses:{'p-v01':{text:'śiva'}},originals:{t1:{'p-v01':{text:'test'}},l0:{'p-v01':[{id:'one'}]}}});
  const original=globalThis.fetch;let candidate=good,calls=0;
  globalThis.fetch=async()=>Response.json(candidate);
  const run=()=>handleScholar(request('/api/scholar/assist','POST',task),env,'alice',{},async()=>{calls++;return 'Draft';});
  try{
    candidate=structuredClone(good);candidate.source_verses['p-v01'].text='changed';
    assert.equal((await run()).status,400);assert.equal(calls,0);
    candidate=structuredClone(good);candidate.originals.l0['p-v01'][0].id='changed';
    const {projection_sha256,...modified}=candidate;candidate.projection_sha256=fixtureDigest(modified);
    assert.equal((await run()).status,400);assert.equal(calls,0);
    candidate=structuredClone(good);candidate.withheld_songs=['p'];
    const {projection_sha256:old,...withheld}=candidate;candidate.projection_sha256=fixtureDigest(withheld);
    assert.equal((await run()).status,400);assert.equal(calls,0);
    candidate=good;assert.equal((await run()).status,200);assert.equal(calls,1);
  }finally{globalThis.fetch=original;db.close();}
});

test('voice relay pins server evidence and refuses client instruction overrides',async()=>{
  const req=new Request('https://worker.example/api/scholar/voice?work=testwork&target=p-v01',{headers:{Upgrade:'websocket'}});
  assert.equal((await handleScholar(req,{},'alice',{},async()=>null)).status,503);
  assert.equal(voiceInput({type:'session.update',session:{instructions:'override'}}),null);
  class Socket{constructor(){this.listeners={};this.sent=[];}accept(){}addEventListener(k,f){this.listeners[k]=f;}
    send(v){this.sent.push(v);}close(){}emit(k,e){this.listeners[k]?.(e);}}
  const upstream=new Socket(),server=new Socket(),client=new Socket();
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  const oldFetch=globalThis.fetch,oldPair=globalThis.WebSocketPair,OldResponse=globalThis.Response;
  globalThis.WebSocketPair=class{constructor(){return {0:client,1:server};}};
  globalThis.Response=class extends OldResponse{constructor(body,options={}){
    if(options.status===101){super(null,{status:200});Object.defineProperty(this,'status',{value:101});this.webSocket=options.webSocket;}
    else super(body,options);}};
  globalThis.fetch=async (url,options)=>{
    if(String(url).startsWith('https://svread.pages.dev/'))return OldResponse.json(projectionFixture({work:'testwork',
      source_verses:{'p-v01':{text:'śiva'}},originals:{t1:{'p-v01':{}},l0:{},l2:{},l3:{},l4:{},c1:{},c2:{},argmap:{}},
      l4_craft:{'p-v01':[{notes:{craft:'Keep the turn'}}]}}));
    assert.equal(options.headers.Authorization,'Bearer provider-key');return {webSocket:upstream};
  };
  try{
    const env={DB:d1(db),QWEN_REALTIME_ENABLED:'true',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',SCHOLAR_DASHSCOPE_API_KEY:'provider-key',
      SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'5',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'10',
      QWEN_REALTIME_WS_URL:'wss://workspace.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime'};
    assert.equal((await handleScholar(req,env,'alice',{},async()=>null)).status,101);
    upstream.emit('message',{data:JSON.stringify({type:'session.created'})});assert.match(upstream.sent[0],/Keep the turn/);
    server.emit('message',{data:JSON.stringify({type:'input_audio_buffer.append',audio:'YWJj'})});assert.equal(upstream.sent.length,1);
    upstream.emit('message',{data:JSON.stringify({type:'session.updated'})});
    server.emit('message',{data:JSON.stringify({type:'session.update',session:{instructions:'override'}})});assert.equal(upstream.sent.length,1);
    server.emit('message',{data:JSON.stringify({type:'input_audio_buffer.append',audio:'YWJj'})});assert.equal(JSON.parse(upstream.sent[1]).audio,'YWJj');
    server.emit('close',{});
  }finally{globalThis.fetch=oldFetch;globalThis.WebSocketPair=oldPair;globalThis.Response=OldResponse;db.close();}
});

test('Qwen reservations enforce configured account and global limits before the provider call',async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(new URL('../worker/schema.sql',import.meta.url),'utf8'));
  db.exec("INSERT INTO profiles (id,email,display_name) VALUES ('alice','alice@example.org','Alice'),('bob','bob@example.org','Bob')");
  const env={DB:d1(db),SCHOLAR_DASHSCOPE_API_KEY:'test',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'2',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'2'};
  const task={work:'testwork',target:'p-v01',layer:'l3',kind:'readings',instruction:'',use_style:false,consent_to_ai:true};
  const original=globalThis.fetch;
  globalThis.fetch=async()=>Response.json(projectionFixture({work:'testwork',source_verses:{'p-v01':{text:'śiva'}},
    originals:{t1:{'p-v01':{}},l0:{},l2:{},l3:{},l4:{},c1:{},c2:{},argmap:{}}}));
  let start,finish;const started=new Promise(resolve=>start=resolve),pending=new Promise(resolve=>finish=resolve);
  let calls=0;const slow=async()=>{calls++;start();return pending;};
  const run=(uid,model=async()=>{calls++;return 'A grounded reading';})=>handleScholar(request('/api/scholar/assist','POST',task),env,uid,{},model);
  try{
    delete env.SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT;
    assert.equal((await run('alice')).status,503);assert.equal(calls,0);
    env.SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT='2';
    const first=run('alice',slow);await started;
    assert.equal((await run('alice')).status,429);assert.equal(calls,1);
    assert.equal((await run('bob')).status,200);assert.equal(calls,2);
    finish('A grounded reading');assert.equal((await first).status,200);
    assert.equal((await run('alice')).status,429);assert.equal(calls,2);
    assert.equal(db.prepare('SELECT COUNT(*) AS n FROM scholar_ai_usage').get().n,2);
    db.exec('DELETE FROM scholar_ai_usage');env.SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT='1';env.SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT='10';
    assert.equal((await run('alice')).status,200);assert.equal((await run('alice')).status,429);
    assert.equal((await run('bob')).status,200);assert.equal(calls,4);
  }finally{globalThis.fetch=original;db.close();}
});
