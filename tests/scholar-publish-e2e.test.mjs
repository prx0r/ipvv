import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile, mkdtemp, cp, symlink, writeFile, chmod, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn,execFileSync} from 'node:child_process';
import {createServer} from 'node:net';
import {once} from 'node:events';
import {createHash} from 'node:crypto';
import {DatabaseSync} from 'node:sqlite';

const here=dirname(fileURLToPath(import.meta.url)),ipvv=dirname(here),translation=process.env.SCHOLAR_TRANSLATION_ROOT||join(dirname(ipvv),'translation-work');
const suite=await readFile(join(ipvv,'worker/src/scholar-workspace.js'),'utf8');
const suiteUrl=`data:text/javascript;base64,${Buffer.from(suite).toString('base64')}`;
const source=(await readFile(join(ipvv,'worker/src/index.js'),'utf8')).replace("'./scholar-workspace.js'",JSON.stringify(suiteUrl));
const worker=(await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`)).default;
const origin='https://svread.pages.dev';
function projectionFixture(data){
  const canonical=value=>Array.isArray(value)?'['+value.map(canonical).join(',')+']':value&&typeof value==='object'?'{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}':JSON.stringify(value);
  const digest=value=>createHash('sha256').update(canonical(value)).digest('hex');
  const {projection_sha256,...body}=data;body.withheld_songs=body.withheld_songs||[];
  body.original_hashes=Object.fromEntries(Object.entries(body.originals).map(([layer,values])=>[layer,Object.fromEntries(Object.entries(values).map(([key,value])=>[key,digest(value)]))]));
  return {...body,projection_sha256:digest(body)};
}

function d1(db){return {prepare(sql){return {bind(...args){return {first:async()=>db.prepare(sql).get(...args)||null,
  all:async()=>({results:db.prepare(sql).all(...args)}),run:async()=>({meta:{changes:Number(db.prepare(sql).run(...args).changes)}})};}};}};}
function canonical(v){if(Array.isArray(v))return '['+v.map(canonical).join(',')+']';
  if(v&&typeof v==='object')return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';return JSON.stringify(v);}
const sha=v=>createHash('sha256').update(canonical(v)).digest('hex');
function git(dir,...args){return execFileSync('git',['-C',dir,...args],{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();}
function request(path,method='GET',data,cookie){return new Request('https://worker.example'+path,{method,
  headers:{Origin:origin,...(data?{'Content-Type':'application/json'}:{}),...(cookie?{Cookie:cookie}:{})},...(data?{body:JSON.stringify(data)}:{})});}

test('account to signed translation and essay on a real local Git remote',async()=>{
  const temp=await mkdtemp(join(tmpdir(),'scholar-chain-')),repo=join(temp,'translation-work'),bare=join(temp,'remote.git');
  let server,db;const oldFetch=globalThis.fetch;
  try{
    for(const folder of ['tools','schemas','paramarthasara'])await cp(join(translation,folder),join(repo,folder),
      {recursive:true,filter:source=>!source.includes('__pycache__')&&!source.endsWith('.pyc')});
    await symlink(ipvv,join(temp,'ipvv'),'dir');git(repo,'init','-b','main');git(repo,'config','user.name','Test');git(repo,'config','user.email','test@example.invalid');
    git(repo,'add','.');git(repo,'commit','-m','Canonical data');git(temp,'init','--bare',bare);git(repo,'remote','add','origin',bare);
    const secret='x'.repeat(40),secretFile=join(temp,'bridge-secret');await writeFile(secretFile,secret);await chmod(secretFile,0o600);
    const listener=createServer();listener.listen(0,'127.0.0.1');await once(listener,'listening');const port=listener.address().port;
    await new Promise(resolve=>listener.close(resolve));
    server=spawn('python3',[join(repo,'tools/scholar_service.py'),'--bridge-secret-file',secretFile,
      '--origin',origin,'--port',String(port),'--push-remote','origin'],{cwd:repo,stdio:['ignore','pipe','pipe']});
    const ready=Promise.race([once(server.stdout,'data'),once(server,'exit').then(([code])=>{throw new Error('bridge exited '+code);}),
      new Promise((_,reject)=>{const timer=setTimeout(()=>reject(new Error('bridge did not start')),10000);timer.unref();})]);
    await ready;
    db=new DatabaseSync(':memory:');db.exec(await readFile(join(ipvv,'worker/schema.sql'),'utf8'));
    const env={DB:d1(db),SESSION_SECRET:'s'.repeat(32),SCHOLAR_DASHSCOPE_API_KEY:'mock',SCHOLAR_QWEN_FREE_TIER_CONFIRMED:'true',
      SCHOLAR_QWEN_DAILY_ACCOUNT_LIMIT:'5',SCHOLAR_QWEN_DAILY_GLOBAL_LIMIT:'10',
      SCHOLAR_BRIDGE_URL:`http://127.0.0.1:${port}`,SCHOLAR_BRIDGE_SECRET:secret};
    const call=(path,method,data,cookie)=>worker.fetch(request(path,method,data,cookie),env);
    let response=await call('/api/auth/access','POST',{email:'scholar@example.org',password:'strong-password',name:'A Scholar'});
    assert.equal(response.status,200);const cookie=response.headers.get('Set-Cookie').split(';')[0];
    const rows=JSON.parse(await readFile(join(repo,'paramarthasara/data/param-p01.l3.json'),'utf8'));
    const target=rows[3].verse_id,t1rows=JSON.parse(await readFile(join(repo,'paramarthasara/data/param-p01.t1.json'),'utf8')),t1=t1rows.find(x=>x.verse_id===target);
    assert.ok(t1);const originals={t1:{[target]:t1},l0:{[target]:[{id:'token'}]},l2:{},l3:{},l4:{},c1:{},c2:{},argmap:{}};
    const projection=projectionFixture({work:'paramarthasara',originals,source_verses:{[target]:{text:'śiva'}},
      l4_craft:{[target]:[{notes:{craft:'Keep the turn'}}]}});
    let lastPrompt='',modelText='A distinct grounded rendering.';globalThis.fetch=async (url,options)=>{
      if(String(url).startsWith('https://svread.pages.dev/'))return Response.json(projection);
      if(String(url).includes('dashscope')){lastPrompt=JSON.parse(options.body).messages[0].content;
        return Response.json({choices:[{message:{content:modelText}}]});}
      return oldFetch(url,options);
    };
    for(let i=0;i<3;i++){
      const doc={expected_revision:0,kind:'translation',work:'paramarthasara',target:rows[i].verse_id,layer:'l3',title:'',content:{text:`Human example ${i}`}};
      assert.equal((await call(`/api/scholar/documents/example-${i}`,'PUT',doc,cookie)).status,200);
    }
    response=await call('/api/scholar/assist','POST',{work:'paramarthasara',target,layer:'l3',kind:'translation',instruction:'',use_style:true,consent_to_ai:true},cookie);
    assert.equal(response.status,200);const agent=(await response.json()).document;assert.equal(agent.content.author_kind,'agent');
    const draft={expected_revision:0,kind:'translation',work:'paramarthasara',target,layer:'l3',title:'',
      content:{text:agent.content.text,base_sha256:sha(rows[3]),parent:null,assisted:true,model:agent.content.model}};
    assert.equal((await call('/api/scholar/documents/draft-1','PUT',draft,cookie)).status,200);
    response=await call('/api/scholar/signoffs','POST',{document_id:'draft-1',revision:1,rights:'all-rights-reserved',confirmed:true},cookie);
    assert.equal(response.status,201);const approval=await response.json();
    response=await call('/api/scholar/submit','POST',{signoff_id:approval.id,confirm_submission:true},cookie);
    const submission=await response.json();assert.equal(response.status,201,JSON.stringify(submission));assert.equal(submission.status,'SUBMITTED_PUBLIC_BRANCH');
    const gitshow=(branch,path)=>execFileSync('git',['--git-dir',bare,'show',branch+':'+path],{encoding:'utf8'});
    const versions=gitshow(submission.branch,'paramarthasara/scholar/versions.jsonl').trim().split('\n').map(JSON.parse);
    const version=versions.at(-1);assert.equal(version.author,'A Scholar');assert.match(version.note,/AI-assisted/);
    const reviews=gitshow(submission.branch,'paramarthasara/scholar/reviews.jsonl').trim().split('\n').map(JSON.parse);
    assert.equal(reviews.at(-1).review_target.object_ref,version.version_id);assert.equal(reviews.at(-1).conflict_of_interest,'AUTHOR');
    response=await call('/api/scholar/sources','POST',{work:'paramarthasara',target,note:'Private source note.'},cookie);
    assert.equal(response.status,201);const sourceId=(await response.json()).id;
    response=await call('/api/scholar/citations/prepare','POST',{source_ids:[sourceId]},cookie);
    assert.equal(response.status,200);const citations=(await response.json()).citations;assert.equal(citations[0].t1_sha256,sha(t1));
    const essay={expected_revision:0,kind:'essay',work:'paramarthasara',target,layer:'l3',title:'My essay',content:{text:'A considered essay.'}};
    assert.equal((await call('/api/scholar/documents/essay-1','PUT',essay,cookie)).status,200);
    assert.equal((await call('/api/scholar/documents/essay-1','PUT',{...essay,expected_revision:1,content:{text:'A carefully revised essay.'}},cookie)).status,200);
    response=await call('/api/scholar/style-examples','POST',{document_id:'essay-1',before_revision:1,after_revision:2,confirmed:true},cookie);
    assert.equal(response.status,201);const style=(await response.json()).id;
    response=await call('/api/auth/access','POST',{email:'reviewer@example.org',password:'strong-password',name:'Reviewer'});
    const reviewerCookie=response.headers.get('Set-Cookie').split(';')[0],reviewer=(await response.json()).profile;
    response=await call('/api/scholar/reviews','POST',{document_id:'essay-1',revision:2,reviewer_id:reviewer.id},cookie);
    assert.equal(response.status,201);const review=await response.json();
    response=await call('/api/scholar/reviews/'+review.id+'/decision','POST',
      {decision:'REQUEST_CHANGES',reasoning:'Private reviewer recommendation.',rubric:{evidence:'Check the Sanskrit.'},ai_consent:true},reviewerCookie);
    assert.equal(response.status,200);
    response=await call('/api/scholar/assist','POST',{kind:'essay_revision',document_id:'essay-1',revision:2,work:'paramarthasara',target,layer:'l3',
      instruction:'Address the evidence.',use_style:true,style_example_ids:[style],review_ids:[review.id],consent_to_ai:true},cookie);
    assert.equal(response.status,200);const essayAgent=(await response.json()).document;
    assert.match(lastPrompt,/Private reviewer recommendation/);assert.match(lastPrompt,/A carefully revised essay/);
    assert.equal((await call('/api/scholar/documents/essay-1','PUT',{...essay,expected_revision:2,
      content:{text:essayAgent.content.text,assisted:true,model:essayAgent.content.model,citations}},cookie)).status,200);
    response=await call('/api/scholar/signoffs','POST',{document_id:'essay-1',revision:3,rights:'cc-by-4.0',confirmed:true},cookie);
    const essayApproval=await response.json();response=await call('/api/scholar/submit','POST',{signoff_id:essayApproval.id,confirm_submission:true},cookie);
    const essayResult=await response.json();assert.equal(response.status,201,JSON.stringify(essayResult));
    assert.match(essayResult.branch,/^scholar\/essay-/);assert.equal(essayResult.status,'SUBMITTED_PUBLIC_BRANCH');
    const digest=essayResult.branch.slice('scholar/essay-'.length);
    const published=gitshow(essayResult.branch,`paramarthasara/scholar/essays/${digest}.json`),paper=JSON.parse(published);
    assert.equal(paper.assisted,true);assert.equal(paper.snapshot.content.text,essayAgent.content.text);
    assert.deepEqual(paper.snapshot.content.citations,citations);assert.equal(paper.source_git_commit,git(repo,'rev-parse','HEAD'));
    assert.doesNotMatch(published,/Private source note/);
    assert.doesNotMatch(published,/Private reviewer recommendation|style:/);
    // Project the exact Git object, then exercise author permission and a reader's cited enquiry.
    Object.assign(projection,projectionFixture({...projection,essays:[paper]}));
    response=await call('/api/scholar/essay-permissions','PUT',{work:'paramarthasara',essay_id:paper.essay_id,allow_answers:true,allow_drafts:false,confirmed:true},cookie);
    assert.equal(response.status,200);
    response=await call('/api/scholar/published-essays?work=paramarthasara','GET',undefined,reviewerCookie);
    const visible=(await response.json()).essays;assert.equal(visible[0].essay_id,paper.essay_id);assert.equal(visible[0].allow_answers,true);
    modelText='The scholar proposes a reading [E1:p1].';
    response=await call('/api/scholar/assist','POST',{work:'paramarthasara',target,layer:'l3',kind:'enquiry',instruction:'Why this reading?',
      consent_to_ai:true,scholar_essays:[{work:'paramarthasara',essay_id:paper.essay_id}]},reviewerCookie);
    const answer=await response.json();assert.equal(response.status,200,JSON.stringify(answer));
    assert.equal(answer.document.content.scholar_citations[0].essay_id,paper.essay_id);assert.match(lastPrompt,/A distinct grounded rendering/);
  }finally{
    globalThis.fetch=oldFetch;if(db)db.close();if(server){server.kill();await once(server,'exit').catch(()=>{});}await rm(temp,{recursive:true,force:true});
  }
});
