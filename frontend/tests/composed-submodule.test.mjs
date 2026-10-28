// C11 2.4 — MODULE acme.parent + SUBMODULE acme.child, dev + bundle, 8 DOM reels.
// Fixture DEV synthetique hors canons. Attestations = DOUBLE de donnee synthetique
// (pattern _att), aucune suite proprietaire executee, aucune Auth reelle. proof_ref
// fixe de fixture. Ni Auth ni PG. Harness router reduit explicite, pas le produit.
// C14 couvre le vrai Shell. Routes statiques PUBLIC /fixture-parent et /fixture-parent/sub.
// Profils Chromium courts sous frontend/tests/c11b-XXXXXX (socket <107), bundles/cache longs sous output.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import http from 'node:http';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { build, createServer } from 'vite';
import { prepareFrontendComposition, isPreparedFrontendComposition } from '../scripts/prepare_frontend_composition.mjs';
import { createFrontendViteConfig } from '../vite.config.js';
const ROOT = fileURLToPath(new URL('../../', import.meta.url));
const PYTHON = '/home/devops/datas/pixs/.venv/bin/python3';
const RUN_WORK = path.join(ROOT, 'output/cismp/cismp3-pixs-c4b2bfe2c6614f3f/composed-pipeline');
const shaHex = (v) => crypto.createHash('sha256').update(v).digest('hex');
const PARENT_TOML = ['schema_version = "1"', 'id = "acme.parent"', 'type = "MODULE"', 'version = "1.0.0"', '', '[frontend]', 'schema_version = "1"', '', '[[frontend.contributions]]', 'type = "TRANSLATION"', 'id = "acme.parent.translations"', 'entry = "frontend.mjs"', 'version = "1.0.0"', 'requires = []', 'scope = "PUBLIC"', '', '[[frontend.contributions]]', 'type = "PAGE"', 'id = "acme.parent.page"', 'entry = "frontend.mjs"', 'version = "1.0.0"', 'requires = ["acme.parent.translations ==1.0.0"]', 'scope = "PUBLIC"', '', '[[frontend.contributions]]', 'type = "ROUTE"', 'id = "acme.parent.route"', 'entry = "frontend.mjs"', 'version = "1.0.0"', 'requires = ["acme.parent.page ==1.0.0"]', 'scope = "PUBLIC"', ''].join('\n') + '\n';
const CHILD_TOML = ['schema_version = "1"', 'id = "acme.child"', 'type = "SUBMODULE"', 'version = "1.0.0"', '', '[dependencies]', 'components = ["acme.parent ==1.0.0"]', '', '[frontend]', 'schema_version = "1"', '', '[[frontend.contributions]]', 'type = "TRANSLATION"', 'id = "acme.child.translations"', 'entry = "frontend.mjs"', 'version = "1.0.0"', 'requires = []', 'scope = "PUBLIC"', '', '[[frontend.contributions]]', 'type = "PAGE"', 'id = "acme.child.page"', 'entry = "frontend.mjs"', 'version = "1.0.0"', 'requires = ["acme.child.translations ==1.0.0", "acme.parent.page ==1.0.0"]', 'scope = "PUBLIC"', '', '[[frontend.contributions]]', 'type = "ROUTE"', 'id = "acme.child.route"', 'entry = "frontend.mjs"', 'version = "1.0.0"', 'requires = ["acme.child.page ==1.0.0"]', 'scope = "PUBLIC"', ''].join('\n') + '\n';
const PARENT_MJS = 'const OWNER = "acme.parent";\nfunction node(kind, variant, props, children) { return {kind: kind, variant: variant, props: props, children: children || []}; }\nfunction label(suffix) { return {key: OWNER + "." + suffix, params: {}}; }\nfunction text(suffix) { return node("text", "body", label(suffix)); }\nfunction heading(suffix) { return node("heading", "section", label(suffix)); }\nexport function ParentPage(input) { const scope = input.context; const keep = scope; return {schema: "pixs.presentation/1.0.0", root: node("section", "panel", {}, [heading("title"), text("scopeDescription"), text("parentMarker")])}; }\nexport const frontendContributions = [\n{descriptor_version: "1.0.0", owner: "acme.parent", owner_version: "1.0.0", type: "TRANSLATION", id: "acme.parent.translations", entry: "frontend.mjs", version: "1.0.0", requires: [], scope: "PUBLIC", point: "pixs.shell.translations", point_version: "1.0.0", display_permissions: [], trust: "TRUSTED", mandatory: true, activation_scope: "PUBLIC", payload: {catalog: {en: {"acme.parent.title": "Parent", "acme.parent.scopeDescription": "Parent scope", "acme.parent.parentMarker": "PARENT_MARKER"}, fr: {"acme.parent.title": "Parent FR", "acme.parent.scopeDescription": "Parent scope FR", "acme.parent.parentMarker": "PARENT_MARKER"}}}},\n{descriptor_version: "1.0.0", owner: "acme.parent", owner_version: "1.0.0", type: "PAGE", id: "acme.parent.page", entry: "frontend.mjs", version: "1.0.0", requires: ["acme.parent.translations ==1.0.0"], scope: "PUBLIC", point: "pixs.shell.pages", point_version: "1.0.0", display_permissions: [], trust: "TRUSTED", mandatory: true, activation_scope: "PUBLIC", payload: {export: "ParentPage"}},\n{descriptor_version: "1.0.0", owner: "acme.parent", owner_version: "1.0.0", type: "ROUTE", id: "acme.parent.route", entry: "frontend.mjs", version: "1.0.0", requires: ["acme.parent.page ==1.0.0"], scope: "PUBLIC", point: "pixs.shell.routes", point_version: "1.0.0", display_permissions: [], trust: "TRUSTED", mandatory: true, activation_scope: "PUBLIC", payload: {path: "/fixture-parent", mode: "CSR", page: "ParentPage"}}\n];\n';
const CHILD_MJS = 'const OWNER = "acme.child";\nfunction node(kind, variant, props, children) { return {kind: kind, variant: variant, props: props, children: children || []}; }\nfunction label(suffix) { return {key: OWNER + "." + suffix, params: {}}; }\nfunction text(suffix) { return node("text", "body", label(suffix)); }\nfunction heading(suffix) { return node("heading", "section", label(suffix)); }\nexport function ChildPage(input) { const scope = input.context; const keep = scope; return {schema: "pixs.presentation/1.0.0", root: node("section", "panel", {}, [heading("title"), text("scopeDescription"), text("childMarker")])}; }\nexport const frontendContributions = [\n{descriptor_version: "1.0.0", owner: "acme.child", owner_version: "1.0.0", type: "TRANSLATION", id: "acme.child.translations", entry: "frontend.mjs", version: "1.0.0", requires: [], scope: "PUBLIC", point: "pixs.shell.translations", point_version: "1.0.0", display_permissions: [], trust: "TRUSTED", mandatory: true, activation_scope: "PUBLIC", payload: {catalog: {en: {"acme.child.title": "Child", "acme.child.scopeDescription": "Child scope", "acme.child.childMarker": "CHILD_MARKER"}, fr: {"acme.child.title": "Child FR", "acme.child.scopeDescription": "Child scope FR", "acme.child.childMarker": "CHILD_MARKER"}}}},\n{descriptor_version: "1.0.0", owner: "acme.child", owner_version: "1.0.0", type: "PAGE", id: "acme.child.page", entry: "frontend.mjs", version: "1.0.0", requires: ["acme.child.translations ==1.0.0", "acme.parent.page ==1.0.0"], scope: "PUBLIC", point: "pixs.shell.pages", point_version: "1.0.0", display_permissions: [], trust: "TRUSTED", mandatory: true, activation_scope: "PUBLIC", payload: {export: "ChildPage"}},\n{descriptor_version: "1.0.0", owner: "acme.child", owner_version: "1.0.0", type: "ROUTE", id: "acme.child.route", entry: "frontend.mjs", version: "1.0.0", requires: ["acme.child.page ==1.0.0"], scope: "PUBLIC", point: "pixs.shell.routes", point_version: "1.0.0", display_permissions: [], trust: "TRUSTED", mandatory: true, activation_scope: "PUBLIC", payload: {path: "/fixture-parent/sub", mode: "CSR", page: "ChildPage"}}\n];\n';
function policyDoc() { return {schema: 'pixs.frontend.build-policy/1.0.0', policy: {schema: 'pixs.frontend.policy/1.0.0', imports: {shellFacades: {'pixs-shell/v1': {exports: [], allowDefault: false, allowNamespace: false}}, foreignFacades: {}}, modularPoints: [], mergeModes: {'pixs.shell.routes': 'APPEND', 'pixs.shell.pages': 'APPEND', 'pixs.shell.navigation-items': 'APPEND', 'pixs.shell.components': 'APPEND', 'pixs.shell.forms': 'APPEND', 'pixs.shell.translations': 'APPEND', 'pixs.shell.ui-permissions': 'APPEND', 'pixs.shell.header': 'APPEND', 'pixs.shell.navigation': 'APPEND', 'pixs.shell.main': 'APPEND', 'pixs.shell.footer': 'APPEND'}, admission: [{owner: 'acme.parent', id: 'acme.parent.translations', mandatory: true}, {owner: 'acme.parent', id: 'acme.parent.page', mandatory: true}, {owner: 'acme.parent', id: 'acme.parent.route', mandatory: true}, {owner: 'acme.child', id: 'acme.child.translations', mandatory: true}, {owner: 'acme.child', id: 'acme.child.page', mandatory: true}, {owner: 'acme.child', id: 'acme.child.route', mandatory: true}], locales: ['en', 'fr'], renderer: {contract: 'pixs.presentation/1.0.0', adapter: 'pixs.dom/v1'}}, limits: {selection: {max_selection_bytes: 65536, max_owners: 4, max_files_per_owner: 2, max_total_files: 6, max_bytes_per_file: 65536, max_total_bytes: 131072}, imports: {maxSourceBytes: 65536, maxTotalSourceBytes: 131072, maxModules: 4, maxImports: 8, maxBindings: 1024, maxResolutions: 8, maxInputNodes: 100000, syntaxLimits: {maxSourceBytes: 65536, maxAstNodes: 16384, maxDescriptorCount: 8, maxTextLength: 4096, maxLiteralItems: 4096, maxLiteralDepth: 32}}, graph: {maxContributions: 16, maxFacts: 32, maxEdges: 64, maxInputNodes: 100000, descriptorLimits: {maxTextLength: 4096, maxRequires: 4, maxPermissions: 4, maxPoints: 16, maxLocales: 2, maxCatalogKeys: 132}}, requirements: {max_contributions: 16, max_requirements_per_contribution: 4, max_total_requirements: 32}, sourceProfile: {maxSourceBytes: 65536, maxAstNodes: 16384, maxBindings: 1024, maxTextLength: 4096, maxScopeDepth: 64}, presentation: {maxNodes: 256, maxDepth: 32, maxChildren: 128, maxTextLength: 4096, maxParams: 32, maxFields: 128, maxBindings: 128, maxDataNodes: 65536, maxBodyDepth: 32, maxBodyNodes: 4096}, wire: {maxPolicyBytes: 65536, maxWireBytes: 1048576, maxPolicyNodes: 65536}}}; }
const ENTRY_SOURCE = "import * as React from 'react';\nimport {createRoot} from 'react-dom/client';\nimport {graph, report, factories, presentationLimits} from 'virtual:pixs-composition/v1';\nimport {createPresentationAdapter} from '/src/shell/presentation-adapter-v1.js';\nconst trial = new URLSearchParams(location.search).get('trial');\nasync function post(data) {\n  const response = await fetch('/__c11_result', {method:'POST', headers:{'Content-Type':'application/json'},\n    body:JSON.stringify({trial,...data}), signal:AbortSignal.timeout(5000)});\n  if (response.status !== 204) throw new Error('REPORT_REJECTED');\n}\nasync function run() {\n  const route=graph.contributions.find(c=>c.type==='ROUTE' && c.payload.path===location.pathname);\n  if (!route) throw new Error('ROUTE_ABSENT');\n  const factory=factories[JSON.stringify([route.owner,route.id])];\n  if (typeof factory!=='function') throw new Error('FACTORY_ABSENT');\n  const translated=graph.contributions.find(c=>c.type==='TRANSLATION' && c.owner===route.owner);\n  if (!translated) throw new Error('CATALOG_ABSENT');\n  const model=factory({context:{state:'ACTIVE'},state:{},params:{}});\n  if (model.schema!=='pixs.presentation/1.0.0') throw new Error('MODEL_SCHEMA_INVALID');\n  const catalogs=translated.payload.catalog;\n  let counter=0;\n  const unexpected=()=>{throw new Error('UNEXPECTED_INTERACTIVE_PORT');};\n  const adapter=createPresentationAdapter({\n    h:React.createElement, Link:p=>React.createElement('a',{href:p.to},p.children),\n    label:key=>{if(!Object.hasOwn(catalogs.en,key))throw new Error('LABEL_ABSENT');return catalogs.en[key];},\n    id:()=> 'fixture-'+(++counter), state:unexpected, submit:unexpected, readFields:unexpected,\n    slot:unexpected, component:unexpected, onError:unexpected\n  });\n  const ctx={owner:route.owner,id:route.id,catalogs,routes:graph.contributions.filter(c=>c.type==='ROUTE').map(c=>c.payload.path),\n    slots:[],components:[],limits:presentationLimits};\n  const mount=document.getElementById('root');\n  createRoot(mount).render(adapter.render(model.root,ctx));\n  for(let i=0;i<100 && !mount.querySelector('h2');i++) await new Promise(r=>setTimeout(r,20));\n  const heading=mount.querySelector('h2')?.textContent || '';\n  const text=mount.textContent || '';\n  const marker=text.includes('CHILD_MARKER')?'CHILD_MARKER':text.includes('PARENT_MARKER')?'PARENT_MARKER':'';\n  await post({phase:'dom',owner:route.owner,id:route.id,path:location.pathname,heading,marker,\n    selection_sha256:report.selection_sha256,policy_sha256:report.policy_sha256,order:report.order});\n}\nrun().catch(async error=>{\n  document.documentElement.dataset.fixtureFailure=String(error.message);\n  try {await post({phase:'failure',error:String(error.message)});}\n  catch(reportError){console.error('Fixture report failed: '+reportError.message);}\n});\n";

const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
function groupAlive(pid) {
  try { process.kill(-pid,0); return true; }
  catch(error) { if(error.code==='ESRCH')return false; throw error; }
}
async function stopBrowser(child,closed) {
  if (!child.pid) return;
  for(const signal of ['SIGTERM','SIGKILL']) {
    try {process.kill(-child.pid,signal);}
    catch(error){if(error.code!=='ESRCH')throw error;}
    await Promise.race([closed,wait(1500)]);
    for(let n=0;n<30 && groupAlive(child.pid);n++)await wait(50);
    if(!groupAlive(child.pid))return;
  }
  throw new Error('BROWSER_GROUP_NOT_QUIESCENT');
}
function html(script) {
  return '<!doctype html><html><head><meta charset="utf-8"></head><body><div id="root"></div>'
    +'<script type="module" src="'+script+'"></script></body></html>';
}
async function bodyBytes(req) {
  req.setTimeout(4000,()=>req.destroy(new Error('BODY_TIMEOUT')));
  const chunks=[];let size=0;
  try {for await(const chunk of req){size+=chunk.length;if(size>16384)throw new Error('BODY_LIMIT');chunks.push(chunk);}}
  finally {req.setTimeout(0);}
  return Buffer.concat(chunks);
}
test('MODULE et SUBMODULE : huit rendus React dev et bundle', {timeout:175000}, async () => {
  const errors=[],observations=[],profiles=[];
  const expected=new Map(),arrivals=new Map();
  let fixture=null,work=null,dev=null,server=null;
  const main=path.join(ROOT,'frontend/src/main.js');
  const mainHash=shaHex(await fsp.readFile(main));
  const paths=['/fixture-parent','/fixture-parent/sub'];
  const handlerErrors=[];
  function respondError(res,error) {
    handlerErrors.push(error);
    if(!res.destroyed){res.statusCode=500;res.end('FIXTURE_SERVER_ERROR');}
  }
  async function receive(req,res) {
    assert.equal(req.method,'POST');
    const body=JSON.parse((await bodyBytes(req)).toString('utf8'));
    assert.equal(typeof body.trial,'string');
    assert.ok(expected.has(body.trial),'unknown trial');
    assert.ok(!arrivals.has(body.trial),'duplicate trial');
    assert.ok(body.phase==='dom'||body.phase==='failure');
    arrivals.set(body.trial,body);
    res.statusCode=204;res.end();
  }
  try {
    fixture=await fsp.mkdtemp(path.join(ROOT,'frontend/tests/c11s-'));
    const parent=path.join(fixture,'parent'),child=path.join(parent,'sub');
    await fsp.mkdir(child,{recursive:true});
    await fsp.writeFile(path.join(parent,'component.toml'),PARENT_TOML);
    await fsp.writeFile(path.join(parent,'frontend.mjs'),PARENT_MJS);
    await fsp.writeFile(path.join(child,'component.toml'),CHILD_TOML);
    await fsp.writeFile(path.join(child,'frontend.mjs'),CHILD_MJS);
    const entryPath=path.join(fixture,'entry.mjs');
    await fsp.writeFile(entryPath,ENTRY_SOURCE);
    const components=[];
    for(const [owner,dir] of [['acme.parent',parent],['acme.child',child]]) {
      components.push({owner,owner_version:'1.0.0',root:path.relative(ROOT,dir).split(path.sep).join('/'),trust:'TRUSTED',
        manifest:{path:'component.toml',sha256:shaHex(await fsp.readFile(path.join(dir,'component.toml')))},
        sources:[{path:'frontend.mjs',sha256:shaHex(await fsp.readFile(path.join(dir,'frontend.mjs')))}]});
    }
    const attestation=owner=>({component_id:owner,component_version:'1.0.0',scope:'COMPONENT',
      target_id:owner,target_version:'1.0.0',suite_id:'c11.synthetic-manifest.test',suite_version:'1.0.0',
      verdict:'PASS',proof_ref:'c11-fixture:acme-parent-child-manifests-v1'});
    const selection={schema:'pixs.frontend.selection/1.0.0',environment:'DEVELOPMENT',
      provenance:{kind:'LOCAL_OPERATOR_SELECTION',reference:'c11-synthetic-submodule-fixture-only'},components,
      composition:{official_ids:['acme.parent','acme.child'],required_ids:['acme.parent','acme.child'],
        configured_providers:null,attestations:['acme.parent','acme.child'].map(attestation)}};
    const selectionBytes=Buffer.from(JSON.stringify(selection)),policyBytes=Buffer.from(JSON.stringify(policyDoc()));
    const options={selectionBytes,policyBytes,expectedSelectionSha256:shaHex(selectionBytes),
      expectedPolicySha256:shaHex(policyBytes),maxPolicyBytes:65536,maxWireBytes:1048576,pythonExecutable:PYTHON};
    const bad=Buffer.from(selectionBytes);bad[0]^=1;
    assert.throws(()=>prepareFrontendComposition({...options,selectionBytes:bad}),/BUILD_PIN_MISMATCH/);
    const prepared=prepareFrontendComposition(options);
    assert.equal(isPreparedFrontendComposition(prepared),true);
    assert.equal(prepared.graph.blocked,false);
    assert.equal(prepared.graph.contributions.length,6);
    assert.deepEqual(prepared.envelope.capture.owners.map(o=>o.owner).sort(),['acme.child','acme.parent']);
    const order=prepared.graph.order.map(v=>v.owner+'/'+v.id);
    assert.ok(order.indexOf('acme.parent/acme.parent.page')>=0);
    assert.ok(order.indexOf('acme.child/acme.child.page')>order.indexOf('acme.parent/acme.parent.page'));
    assert.equal(prepared.verifyBeforePublish().verified,true);
    await fsp.mkdir(RUN_WORK,{recursive:true});
    work=await fsp.mkdtemp(path.join(RUN_WORK,'submod-'));
    const outDir=path.join(work,'bundle'),cacheDir=path.join(work,'vite-cache');
    const config=createFrontendViteConfig({mode:'COMPOSED',composition:prepared});
    const middlewarePlugin={name:'c11-test-page',configureServer(s){
      s.middlewares.use((req,res,next)=>{
        let url;
        try{url=new URL(req.url,'http://127.0.0.1');}
        catch(error){respondError(res,error);return;}
        if(url.pathname==='/__c11_result'){receive(req,res).catch(e=>respondError(res,e));return;}
        if(paths.includes(url.pathname)){res.setHeader('Content-Type','text/html; charset=utf-8');res.end(html('/@fs/'+entryPath));return;}
        next();
      });
    }};
    dev=await createServer({...config,configFile:false,cacheDir,logLevel:'error',
      plugins:[...config.plugins,middlewarePlugin],
      server:{...config.server,host:'127.0.0.1',port:0,strictPort:false}});
    await dev.listen();
    const devBase='http://127.0.0.1:'+dev.httpServer.address().port;
    const resolved=await dev.pluginContainer.resolveId('virtual:pixs-composition/v1');
    const loaded=await dev.pluginContainer.load(resolved.id);
    const raw=typeof loaded==='string'?loaded:loaded.code;
    const reportLine=raw.split('\n').find(line=>line.startsWith('export const report = __freeze('));
    assert.ok(reportLine);
    const devReport=JSON.parse(reportLine.slice('export const report = __freeze('.length,-2));
    assert.deepEqual(devReport,JSON.parse(JSON.stringify(prepared.report)));
    await build({...createFrontendViteConfig({mode:'COMPOSED',composition:prepared}),configFile:false,
      define:{'process.env.NODE_ENV':JSON.stringify('production')},
      cacheDir,logLevel:'error',build:{outDir,emptyOutDir:true,
        lib:{entry:entryPath,formats:['es'],fileName:()=> 'fixture.js'}}});
    const bundleReport=JSON.parse(await fsp.readFile(path.join(outDir,'composition.json'),'utf8'));
    assert.deepEqual(bundleReport,devReport);
    assert.ok((await fsp.stat(path.join(outDir,'fixture.js'))).size>0);
    server=http.createServer((req,res)=>{
      (async()=>{
        const url=new URL(req.url,'http://127.0.0.1');
        if(url.pathname==='/__c11_result'){await receive(req,res);return;}
        if(paths.includes(url.pathname)){res.setHeader('Content-Type','text/html; charset=utf-8');res.end(html('/fixture.js'));return;}
        if(url.pathname==='/fixture.js'){res.setHeader('Content-Type','text/javascript; charset=utf-8');res.end(await fsp.readFile(path.join(outDir,'fixture.js')));return;}
        if(url.pathname==='/favicon.ico'){res.statusCode=204;res.end();return;}
        res.statusCode=404;res.end('NOT_FOUND');
      })().catch(error=>respondError(res,error));
    });
    server.requestTimeout=5000;server.headersTimeout=5000;
    await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
    const bundleBase='http://127.0.0.1:'+server.address().port;
    for(const mode of ['dev','bundle'])for(const route of paths)for(const engine of ['chromium','firefox']) {
      const trial=crypto.randomUUID(),owner=route===paths[0]?'acme.parent':'acme.child';
      expected.set(trial,{mode,route,engine,owner});
      const profile=await fsp.mkdtemp(path.join(ROOT,'frontend/tests/c11b-'));
      profiles.push(profile);
      const env={PATH:'/usr/bin:/bin',LANG:'C.UTF-8',HOME:profile,TMPDIR:profile,
        XDG_CACHE_HOME:profile,XDG_CONFIG_HOME:profile,XDG_DATA_HOME:profile};
      const url=(mode==='dev'?devBase:bundleBase)+route+'?trial='+trial;
      const args=engine==='chromium'?['--headless','--disable-gpu','--no-first-run','--no-default-browser-check',
        '--disable-background-networking','--disable-crash-reporter','--user-data-dir='+profile,url]:
        ['-headless','-no-remote','-profile',profile,url];
      const child=spawn('/usr/bin/'+engine,args,{env,detached:true,stdio:'ignore'});
      let spawnError=null;
      const closed=new Promise(resolve=>{child.once('error',e=>{spawnError=e;});child.once('close',resolve);});
      try {
        const end=Date.now()+15000;
        while(!arrivals.has(trial)){
          if(spawnError)throw spawnError;
          if(child.exitCode!==null)throw new Error('BROWSER_EARLY_EXIT:'+engine);
          if(Date.now()>end)throw new Error('DOM_REPORT_TIMEOUT:'+engine+':'+mode+':'+route);
          await wait(50);
        }
        const result=arrivals.get(trial);
        assert.equal(result.phase,'dom',JSON.stringify(result));
        assert.equal(result.owner,owner);
        assert.equal(result.path,route);
        assert.equal(result.marker,owner==='acme.child'?'CHILD_MARKER':'PARENT_MARKER');
        assert.equal(result.heading,owner==='acme.child'?'Child':'Parent');
        assert.equal(result.selection_sha256,options.expectedSelectionSha256);
        assert.equal(result.policy_sha256,options.expectedPolicySha256);
        assert.deepEqual(result.order,prepared.report.order);
        observations.push({engine,mode,route,...result});
      } finally {
        await stopBrowser(child,closed);
        await fsp.rm(profile,{recursive:true,force:true});
        assert.equal(fs.existsSync(profile),false);
      }
    }
    assert.equal(arrivals.size,8);
    assert.equal(observations.length,8);
    assert.equal(prepared.verifyBeforePublish().verified,true);
    assert.equal(shaHex(await fsp.readFile(main)),mainHash);
  } catch(error){errors.push(error);}
  finally{
    if(dev)try{await dev.close();}catch(error){errors.push(error);}
    if(server)try{await new Promise((resolve,reject)=>server.close(error=>error?reject(error):resolve()));}catch(error){errors.push(error);}
    for(const profile of profiles)if(fs.existsSync(profile))errors.push(new Error('PROFILE_RETAINED:'+profile));
    if(work)try{await fsp.rm(work,{recursive:true,force:true});assert.equal(fs.existsSync(work),false);}catch(error){errors.push(error);}
    if(fixture)try{await fsp.rm(fixture,{recursive:true,force:true});assert.equal(fs.existsSync(fixture),false);}catch(error){errors.push(error);}
  }
  errors.push(...handlerErrors);
  if(errors.length)throw new AggregateError(errors,'C11_SUBMODULE_RECIPE_FAILED');
  console.log(JSON.stringify({schema:'c11-submodule-browser/1',status:'PASS',observations,
    fixtures_removed:true,profiles_removed:true,browser_groups_quiescent:true,servers_closed:true,
    source_unchanged:true,limits:'Fixture DEV, attestations et contexte doubles ; routage de harnais, vrai Kernel/Vite/React/adapter/DOM. Aucune qualification Auth/PG/accessibilite manuelle.'}));
});
