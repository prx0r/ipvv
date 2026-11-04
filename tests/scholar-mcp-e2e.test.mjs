import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {existsSync} from 'node:fs';
import {createServer} from 'node:http';
import {createInterface} from 'node:readline';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {createHash} from 'node:crypto';
import {DatabaseSync} from 'node:sqlite';
import {dirname,join} from 'node:path';
import {fileURLToPath} from 'node:url';

const ipvv=dirname(dirname(fileURLToPath(import.meta.url)));
const mcp=process.env.SCHOLAR_MCP_SERVER||join(dirname(ipvv),'svread','mcp','scholar_server.py');
const suite=await readFile(join(ipvv,'worker/src/scholar-workspace.js'),'utf8');
const suiteUrl=`data:text/javascript;base64,${Buffer.from(suite).toString('base64')}`;
const code=(await readFile(join(ipvv,'worker/src/index.js'),'utf8')).replace("'./scholar-workspace.js'",JSON.stringify(suiteUrl));
const worker=(await import(`data:text/javascript;base64,${Buffer.from(code).toString('base64')}`)).default;
function d1(db){return {prepare(sql){return {bind(...args){return {
  first:async()=>db.prepare(sql).get(...args)||null,all:async()=>({results:db.prepare(sql).all(...args)}),
  run:async()=>({meta:{changes:Number(db.prepare(sql).run(...args).changes)}})};}};}};}
const canonical=v=>Array.isArray(v)?'['+v.map(canonical).join(',')+']':v&&typeof v==='object'?'{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}':JSON.stringify(v);
const hash=v=>createHash('sha256').update(canonical(v)).digest('hex');
function fixture(){const originals={t1:{'p-v01':{}},l0:{},argmap:{},l2:{},l3:{},l4:{},c1:{},c2:{}};
  const d={work:'testwork',source_verses:{'p-v01':{text:'śiva'}},originals,withheld_songs:[],
    original_hashes:Object.fromEntries(Object.entries(originals).map(([k,v])=>[k,Object.fromEntries(Object.entries(v).map(([id,x])=>[id,hash(x)]))]))};
  return {...d,projection_sha256:hash(d)};}
function request(path,method='GET',data,cookie){return new Request('https://worker.example'+path,{method,
  headers:{Origin:'https://svread.pages.dev',...(data?{'Content-Type':'application/json'}:{}),...(cookie?{Cookie:cookie}:{})},...(data?{body:JSON.stringify(data)}:{})});}

test('MCP → account Worker → private evidence, review and consented draft', {skip:!existsSync(mcp)}, async()=>{
  const db=new DatabaseSync(':memory:');db.exec(await readFile(join(ipvv,'worker/schema.sql'),'utf8'));
  const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32),SCHOLAR_DASHSCOPE_API_KEY:'mock',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',
    SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'5',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'10'};
  const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
  async function login(email){const res=await call('/api/auth/access','POST',{email,password:'strong-password',name:email.split('@')[0]});
    assert.equal(res.status,200);return {cookie:res.headers.get('Set-Cookie').split(';')[0],profile:(await res.json()).profile};}
  const alice=await login('alice@example.org'),bob=await login('bob@example.org');
  const original=globalThis.fetch;let prompt='';globalThis.fetch=async(url,options)=>{
    if(String(url).includes('/data/scholar/testwork.json'))return Response.json(fixture());
    if(String(url).includes('dashscope')){prompt=JSON.parse(options.body).messages[0].content;return Response.json({choices:[{message:{content:'Grounded agent essay.'}}]});}
    return original(url,options);
  };
  const http=createServer(async(req,res)=>{try{
    const chunks=[];for await(const chunk of req)chunks.push(chunk);const bytes=Buffer.concat(chunks);
    const response=await worker.fetch(new Request('http://localhost'+req.url,{method:req.method,headers:req.headers,...(bytes.length?{body:bytes}:{})}),env);
    res.writeHead(response.status,Object.fromEntries(response.headers));res.end(Buffer.from(await response.arrayBuffer()));
  }catch{res.writeHead(500);res.end('{}');}});
  http.listen(0,'127.0.0.1');await once(http,'listening');let child;
  try{
    child=spawn('python3',[mcp],{stdio:['pipe','pipe','pipe'],env:{...process.env,SCHOLAR_API_ORIGIN:`http://127.0.0.1:${http.address().port}`,SCHOLAR_SESSION_COOKIE:alice.cookie}});
    const rl=createInterface({input:child.stdout});const messages=[];let wake=null;
    rl.on('line',line=>{messages.push(JSON.parse(line));if(wake){wake();wake=null;}});
    let next=0;async function rpc(method,params={}){const id=++next;child.stdin.write(JSON.stringify({jsonrpc:'2.0',id,method,params})+'\n');
      while(!messages.some(x=>x.id===id))await new Promise((resolve,reject)=>{wake=resolve;const timer=setTimeout(()=>reject(new Error('MCP timed out')),10000);timer.unref();});
      const result=messages.splice(messages.findIndex(x=>x.id===id),1)[0];assert.ok(!result.error,JSON.stringify(result));return result.result;}
    async function tool(name,args){const result=await rpc('tools/call',{name,arguments:args});assert.ok(!result.isError,JSON.stringify(result));return JSON.parse(result.content[0].text);}
    assert.equal((await rpc('initialize',{protocolVersion:'2025-06-18'})).serverInfo.name,'svread-scholar');
    assert.ok((await tool('list_works',{})).works.includes('paramarthasara'));
    const real=await tool('passage_evidence',{work:'paramarthasara',target:'param-p01-v01'});assert.match(real.source.text,/śambhuṃ/);
    const doc={expected_revision:0,kind:'essay',work:'testwork',target:'p-v01',layer:'l3',title:'Essay',content:{text:'Śiva is free'}};
    const saved=await tool('save_document',{document_id:'essay:one',document:doc});assert.equal(saved.document.revision,1);
    const decision=await tool('save_decision',{document_id:'essay:one',revision:1,subject:'śiva',before:'lord',after:'Śiva',reason:'Context'});
    const source=await tool('save_source',{work:'testwork',target:'p-v01',note:'Check the source'});
    const review=await tool('request_review',{document_id:'essay:one',reviewer_id:bob.profile.id,revision:1});
    const report=await call('/api/scholar/reviews/'+review.id+'/decision','POST',{decision:'COMMENT',reasoning:'Please check.',ai_consent:true},bob.cookie);assert.equal(report.status,200);
    const comment=await call('/api/scholar/reviews/'+review.id+'/annotations','POST',{start:0,end:4,quote:'Śiva',body:'Clarify'},bob.cookie);assert.equal(comment.status,201);
    const annotations=await tool('list_review_annotations',{review_id:review.id});assert.equal(annotations.annotations[0].quote,'Śiva');
    const draft=await tool('draft_with_qwen',{work:'testwork',target:'p-v01',layer:'l3',kind:'essay',instruction:'',use_style:true,
      decision_ids:[decision.id],source_ids:[source.id],consent_to_ai:true});
    assert.equal(draft.document.content.author_kind,'agent');assert.match(prompt,/Check the source/);assert.match(prompt,/Context/);
    assert.doesNotMatch(prompt,/Clarify/);assert.equal(draft.document.content.source_references[0].projection_sha256,source.projection_sha256);
    const signoff=await call('/api/scholar/signoffs','POST',{document_id:'essay:one',revision:1,rights:'all-rights-reserved',confirmed:true},alice.cookie);assert.equal(signoff.status,201);
  }finally{if(child){child.stdin.end();child.kill();await once(child,'exit').catch(()=>{});}await new Promise(resolve=>http.close(resolve));globalThis.fetch=original;db.close();}
});
