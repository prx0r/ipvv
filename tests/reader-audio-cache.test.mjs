import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const source=await readFile(new URL('../worker/src/index.js',import.meta.url),'utf8');
const worker=(await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`)).default;

test('recordings are keyed to exact text and do not reuse the legacy verse-only cache',async()=>{
  const files=new Map([['read/testwork/p01_en.mp3',new Uint8Array([0])]]),heads=[],calls=[];
  const env={FISH_API_KEY:'test',AUDIO:{head:async key=>{heads.push(key);return files.has(key)?{}:null;},
    put:async(key,value)=>{files.set(key,new Uint8Array(value));}}};
  const original=globalThis.fetch;
  globalThis.fetch=async(url,options)=>{assert.equal(String(url),'https://api.fish.audio/v1/tts');
    assert.equal(options.headers.model,'s2.1-pro-free');calls.push(JSON.parse(options.body));
    return new Response(new Uint8Array([1,2,3]),{status:200});};
  const read=(text,lang='en')=>worker.fetch(new Request('https://worker.example/api/read',{method:'POST',
    headers:{'Content-Type':'application/json'},body:JSON.stringify({work:'testwork',verse:'p01',lang,text})}),env);
  try{
    let response=await read('First reading.');assert.equal(response.status,200);const first=await response.json();
    assert.equal(first.cached,false);assert.match(first.url,/\/read-v2\/testwork\/p01_en_[a-f0-9]{64}\.mp3$/);
    response=await read('First reading.');assert.equal((await response.json()).cached,true);assert.equal(calls.length,1);
    response=await read('A revised reading.');const revised=await response.json();assert.equal(revised.cached,false);
    assert.notEqual(revised.url,first.url);assert.equal(calls.length,2);
    response=await read('First reading.','c1');assert.notEqual((await response.json()).url,first.url);
    assert.equal(heads.includes('read/testwork/p01_en.mp3'),false);assert.equal(calls.length,3);
  }finally{globalThis.fetch=original;}
});
