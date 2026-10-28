import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { validateFrontendImports, collectFrontendImports, SHELL_ALIAS, SHELL_EXPORTS } from '../scripts/composition-imports-v1.mjs';

const ROOT=fileURLToPath(new URL('../../',import.meta.url));
const PYTHON='/home/devops/python/current/bin/python3';
const PY="import sys,json,hashlib\nfrom pathlib import Path\nroot=Path.cwd()\nsys.path[:0]=[str(root/'src'),str(root/'frontend/scripts'),str(root/'frontend/tests')]\nfrom test_build_frontend_plan import PlanTests,manifest_dep,att\nfrom build_frontend_plan import prepare_frontend_plan\nspec=json.load(sys.stdin)\nt=PlanTests()\nt.setUp()\ntry:\n    owners=[]\n    for i,s in enumerate(spec):\n        name=s['owner']\n        raw=manifest_dep(name,kind=s.get('kind','MODULE'),dep_components=s.get('dependencies'))\n        o=t._owner('owner'+str(i),name,raw,js=s['source'].encode('utf-8'))\n        for path,text in s.get('helpers',{}).items():\n            target=root/o['root']/path\n            target.parent.mkdir(parents=True,exist_ok=True)\n            data=text.encode('utf-8')\n            target.write_bytes(data)\n            o['sources'].append({'path':path,'sha256':hashlib.sha256(data).hexdigest()})\n        owners.append(o)\n    # Attestations de fixtures uniquement, sans preuve de production.\n    doc=t._doc(owners,[s['owner'] for s in spec],[s['owner'] for s in spec],None,[att(s['owner'],idx=i) for i,s in enumerate(spec)])\n    blob,pin=t._blob(doc)\n    result=prepare_frontend_plan(blob,expected_sha256=pin,project_root=root,selection_limits=t._limits())\n    print(json.dumps(result.to_dict(),ensure_ascii=False,separators=(',',':')))\nfinally:\n    t.doCleanups()\n";

const ENTRY='export const frontendContributions=[];\nexport const Page=()=>null;\n';
const LIMITS=()=>({maxSourceBytes:32768,maxTotalSourceBytes:262144,maxModules:32,maxImports:64,maxBindings:128,maxResolutions:64,maxInputNodes:20000,syntaxLimits:{maxSourceBytes:32768,maxAstNodes:4096,maxDescriptorCount:32,maxTextLength:4096,maxLiteralItems:4096,maxLiteralDepth:64}});
const POLICY=()=>({shellFacades:{[SHELL_ALIAS]:{exports:[...SHELL_EXPORTS],allowDefault:false,allowNamespace:false}},foreignFacades:{}});
function fixture(spec=[{owner:'acme.one',source:ENTRY}]){
  const p=spawnSync(PYTHON,['-B','-c',PY],{cwd:ROOT,input:JSON.stringify(spec),encoding:'utf8',timeout:15000,maxBuffer:1024*1024});
  assert.ifError(p.error);assert.equal(p.status,0,p.stderr);
  return JSON.parse(p.stdout);
}
function one(source,helpers={}){return fixture([{owner:'acme.one',source,helpers}]);}
function refused(env,code,pol=POLICY(),lim=LIMITS()){
  assert.throws(()=>validateFrontendImports(env,pol,lim),e=>e?.code===code,'refus '+code);
}
function replaceSource(env,raw){
  const f=env.capture.owners[0].sources[0];
  f.data_b64=raw.toString('base64');f.size=raw.length;f.sha256=createHash('sha256').update(raw).digest('hex');
}
test('Kernel réel, façade shell et résultat gelé sans évaluation',()=>{
  const env=one('import { QueryClient as Q } from "pixs-shell/v1";\nglobalThis.C11_IMPORT_EXECUTED=true;\n'+ENTRY);
  delete globalThis.C11_IMPORT_EXECUTED;
  const r=validateFrontendImports(env,POLICY(),LIMITS());
  assert.equal(r.modules.length,1);assert.equal(r.modules[0].isEntry,true);
  assert.equal(r.resolutions[0].target,SHELL_ALIAS);assert.equal(r.resolutions[0].bindings[0].local,'Q');
  assert.equal(globalThis.C11_IMPORT_EXECUTED,undefined);
  assert(Object.isFrozen(r));assert(Object.isFrozen(r.modules[0]));assert(Object.isFrozen(r.resolutions[0].bindings));
});
test('imports relatifs exacts et cycle JS sans nouveau graphe de composants',()=>{
  const env=one('import { a } from "./a.mjs";\n'+ENTRY,{
    'frontend/a.mjs':'import { b } from "./b.mjs";\nexport const a=1;\n',
    'frontend/b.mjs':'import { a } from "./a.mjs";\nexport const b=2;\n'});
  const r=validateFrontendImports(env,POLICY(),LIMITS());
  assert.equal(r.modules.length,3);assert.equal(r.resolutions.length,3);
  assert.equal(r.modules.filter(m=>m.isEntry).length,1);
});
test('aucun suffixe ajouté ni export relatif inventé',()=>{
  refused(one('import { a } from "./a";\n'+ENTRY,{'frontend/a.mjs':'export const a=1;\n'}),'IMPORT_UNLISTED');
  refused(one('import { absent } from "./a.mjs";\n'+ENTRY,{'frontend/a.mjs':'export const a=1;\n'}),'IMPORT_FACADE_UNDECLARED');
});
test('sortie de racine et pseudo-chemin relatif refusés',()=>{
  refused(one('import "../../owner1/frontend/main.mjs";\n'+ENTRY),'IMPORT_PRIVATE_SIBLING');
  refused(one('import ".../other.mjs";\n'+ENTRY),'IMPORT_BARE_REFUSED');
});
test('URI, paquet nu et requête sur chemin refusés',()=>{
  for(const s of ['https://example.invalid/a.js','unknown-package','./a.mjs?raw'])
    refused(one('import "'+s+'";\n'+ENTRY),'IMPORT_BARE_REFUSED');
});
test('moteurs et outils de build directs refusés',()=>{
  for(const s of ['react','react-dom/client','vite','typescript','esbuild'])
    refused(one('import "'+s+'";\n'+ENTRY),'IMPORT_RENDERER_REFUSED');
});
test('import dynamique, require et réexport de helper refusés',()=>{
  refused(one('const p=import("./a.mjs");\n'+ENTRY),'IMPORT_DYNAMIC_REFUSED');
  refused(one('const p=require("./a.mjs");\n'+ENTRY),'IMPORT_REQUIRE_REFUSED');
  refused(one('import "./a.mjs";\n'+ENTRY,{'frontend/a.mjs':'export { q } from "./b.mjs";\n','frontend/b.mjs':'export const q=1;\n'}),'IMPORT_REEXPORT_REFUSED');
});
test('export shell inconnu ou retiré de politique refusé',()=>{
  refused(one('import { translate } from "pixs-shell/v1";\n'+ENTRY),'IMPORT_SHELL_FACADE_UNKNOWN');
  const p=POLICY();p.shellFacades[SHELL_ALIAS].exports=[];
  refused(one('import { QueryClient } from "pixs-shell/v1";\n'+ENTRY),'IMPORT_SHELL_FACADE_UNKNOWN',p);
});
test('default et namespace shell refusés',()=>{
  refused(one('import X from "pixs-shell/v1";\n'+ENTRY),'IMPORT_DEFAULT_REFUSED');
  refused(one('import * as X from "pixs-shell/v1";\n'+ENTRY),'IMPORT_NAMESPACE_REFUSED');
});
function pair(dependency=true){
  return fixture([{owner:'acme.app',kind:'SUBMODULE',dependencies:dependency?['acme.lib >=1.0.0']:[],source:'import { PublicPage as P } from "acme-lib/v1";\n'+ENTRY},
    {owner:'acme.lib',source:ENTRY+'export const PublicPage=()=>null;\n',helpers:{'frontend/private.mjs':'export const Secret=1;\n'}}]);
}
function pairPolicy(){const p=POLICY();p.foreignFacades['acme-lib/v1']={owner:'acme.lib',entry:'frontend/main.mjs',exports:['PublicPage']};return p;}
test('façade explicite et dépendance réelle du Kernel',()=>{
  const r=validateFrontendImports(pair(),pairPolicy(),LIMITS());
  assert(r.resolutions.some(x=>x.target==='acme.lib#frontend/main.mjs'));
});
test('façade sans dépendance commune refusée',()=>refused(pair(false),'IMPORT_FACADE_UNDECLARED',pairPolicy()));
test('helper privé ne devient pas façade même capturé',()=>{
  const p=pairPolicy();p.foreignFacades['acme-lib/v1'].entry='frontend/private.mjs';
  refused(pair(),'IMPORT_FACADE_UNDECLARED',p);
});
test('façade ne peut inventer son export public',()=>{
  const p=pairPolicy();p.foreignFacades['acme-lib/v1'].exports=[];
  refused(pair(),'IMPORT_FACADE_UNDECLARED',p);
});
test('empreinte et taille recoupées avant AST',()=>{
  const e=one(ENTRY);e.capture.owners[0].sources[0].sha256='0'.repeat(64);refused(e,'IMPORT_BYTES_MISMATCH');
  const f=one(ENTRY);f.capture.owners[0].sources[0].size++;refused(f,'IMPORT_BYTES_MISMATCH');
});
test('base64 non canonique refusé',()=>{
  const e=one(ENTRY);e.capture.owners[0].sources[0].data_b64+='\n';refused(e,'IMPORT_BYTES_MISMATCH');
});
test('UTF-8 invalide, BOM et CRLF refusés même avec empreinte concordante',()=>{
  for(const raw of [Buffer.from([255]),Buffer.concat([Buffer.from([239,187,191]),Buffer.from(ENTRY)]),Buffer.from(ENTRY.replaceAll('\n','\r\n'))]){
    const e=one(ENTRY);replaceSource(e,raw);refused(e,'IMPORT_BYTES_MISMATCH');
  }
});
test('checksum, hash manifest et ordre Kernel altérés refusés',()=>{
  const e=one(ENTRY);e.context_checksum='0'.repeat(64);refused(e,'IMPORT_CHECKSUM_MISMATCH');
  const f=one(ENTRY);f.plan.sources_sha256[0].sha256='0'.repeat(64);refused(f,'IMPORT_ENVELOPE_INVALID');
  const g=one(ENTRY);g.plan.order=['acme.absent'];refused(g,'IMPORT_ENVELOPE_INVALID');
});
test('propriétaire de facette absent refusé sans TypeError',()=>{
  const e=one(ENTRY);e.plan.facets[0].owner='acme.absent';refused(e,'IMPORT_CAPTURE_INVALID');
});
test('bornes des octets, modules, imports, bindings et résolutions',()=>{
  const e=one('import { QueryClient, CommandClient } from "pixs-shell/v1";\nimport "pixs-shell/v1";\n'+ENTRY,{'frontend/helper.mjs':'export const x=1;\n'});
  for(const key of ['maxSourceBytes','maxTotalSourceBytes']){
    const l=LIMITS();l[key]=1;assert.throws(()=>validateFrontendImports(e,POLICY(),l),x=>['IMPORT_TOO_LARGE','IMPORT_BYTES_MISMATCH'].includes(x.code));
  }
  for(const key of ['maxModules','maxImports','maxBindings','maxResolutions']){
    const l=LIMITS();l[key]=1;refused(e,'IMPORT_LIMITS_INVALID',POLICY(),l);
  }
});
test('limites et politiques fermées et explicites',()=>{
  const e=one(ENTRY);const l=LIMITS();delete l.maxInputNodes;refused(e,'IMPORT_LIMITS_INVALID',POLICY(),l);
  const p=POLICY();p.extra=true;refused(e,'IMPORT_POLICY_INVALID',p);
  const ns=POLICY();ns.shellFacades[SHELL_ALIAS].allowNamespace=true;refused(e,'IMPORT_POLICY_INVALID',ns);
  const dup=pairPolicy();dup.foreignFacades['acme-lib/v1'].exports=['PublicPage','PublicPage'];refused(e,'IMPORT_POLICY_INVALID',dup);
});
test('getters, proxys, cycles et tableaux creux refusés sans déclenchement',()=>{
  let called=false;const e=one(ENTRY);Object.defineProperty(e,'capture',{get(){called=true;return {};},enumerable:true});
  refused(e,'IMPORT_ENVELOPE_INVALID');assert.equal(called,false);
  const p=new Proxy({}, {get(){throw Error('piège');},ownKeys(){throw Error('piège');}});refused(p,'IMPORT_ENVELOPE_INVALID');
  const c=one(ENTRY);c.loop=c;refused(c,'IMPORT_ENVELOPE_INVALID');
  const s=one(ENTRY);delete s.plan.order[0];refused(s,'IMPORT_ENVELOPE_INVALID');
});
test('budget de copie borné avant parcours',()=>{
  const l=LIMITS();l.maxInputNodes=1;refused(one(ENTRY),'IMPORT_LIMITS_INVALID',POLICY(),l);
});

test('collecteur : même résultat que validation stricte quand tout est valide',()=>{
  const e=one(ENTRY);
  assert.deepEqual(collectFrontendImports(e,POLICY(),LIMITS()),validateFrontendImports(e,POLICY(),LIMITS()));
});
test('collecteur : syntaxe invalide corrélée à son propriétaire, indépendants conservés',()=>{
  const e=fixture([{owner:'acme.bad',source:'export const Broken=;\n'},{owner:'acme.good',source:ENTRY}]);
  const before=JSON.stringify(e);
  const r=collectFrontendImports(e,POLICY(),LIMITS());
  assert.deepEqual(r.modules.map(m=>m.owner),['acme.good']);
  assert.equal(r.diagnostics.length,1);assert.equal(r.diagnostics[0].owner,'acme.bad');
  assert.equal(r.diagnostics[0].code,'SYNTAX_INVALID');
  assert.equal(JSON.stringify(e),before);
  assert.equal(Object.hasOwn(r,'ready'),false);assert.equal(Object.hasOwn(r,'active'),false);
  assert(Object.isFrozen(r.diagnostics[0]));
});
test('collecteur : helper invalide retire toutes les sources du propriétaire',()=>{
  const e=fixture([{owner:'acme.bad',source:ENTRY,helpers:{'frontend/private.mjs':'export const Broken=;\n'}},{owner:'acme.good',source:ENTRY}]);
  const r=collectFrontendImports(e,POLICY(),LIMITS());
  assert.deepEqual(r.modules.map(m=>m.owner),['acme.good']);
  assert.equal(r.diagnostics[0].owner,'acme.bad');
});
test('collecteur : refus import local sans effondrement des indépendants',()=>{
  const e=fixture([{owner:'acme.bad',source:'import "react";\n'+ENTRY},{owner:'acme.good',source:ENTRY}]);
  const r=collectFrontendImports(e,POLICY(),LIMITS());
  assert.deepEqual(r.modules.map(m=>m.owner),['acme.good']);
  assert.equal(r.diagnostics[0].code,'IMPORT_RENDERER_REFUSED');
  assert.equal(r.resolutions.length,0);
});
test('collecteur : propagation vers importeur déjà résolu, pas vers indépendant',()=>{
  const e=fixture([
    {owner:'acme.app',kind:'SUBMODULE',dependencies:['acme.lib >=1.0.0'],source:'import { PublicPage } from "acme-lib/v1";\n'+ENTRY},
    {owner:'acme.lib',source:ENTRY+'export const PublicPage=()=>null;\n',helpers:{'frontend/private.mjs':'import "./absent.mjs";\nexport const p=1;\n'}},
    {owner:'acme.good',source:ENTRY},
  ]);
  const r=collectFrontendImports(e,pairPolicy(),LIMITS());
  assert.deepEqual(r.modules.map(m=>m.owner),['acme.good']);
  assert(r.diagnostics.some(d=>d.owner==='acme.lib'&&d.code==='IMPORT_UNLISTED'));
  assert(r.diagnostics.some(d=>d.owner==='acme.app'&&d.code==='IMPORT_DEPENDENCY_UNAVAILABLE'));
  assert.equal(r.resolutions.length,0);
});
test('collecteur : intégrité de capture reste un refus global',()=>{
  const e=fixture([{owner:'acme.bad',source:'export const Broken=;\n'},{owner:'acme.good',source:ENTRY}]);
  e.capture.owners[0].sources[0].sha256='0'.repeat(64);
  assert.throws(()=>collectFrontendImports(e,POLICY(),LIMITS()),x=>x.code==='IMPORT_BYTES_MISMATCH');
});
test('collecteur : politique et budgets restent globaux même face à une erreur locale',()=>{
  const e=one('import "react";\n'+ENTRY);
  const p=POLICY();p.extra=true;
  assert.throws(()=>collectFrontendImports(e,p,LIMITS()),x=>x.code==='IMPORT_POLICY_INVALID');
  const l=LIMITS();l.maxTotalSourceBytes=1;
  assert.throws(()=>collectFrontendImports(e,POLICY(),l),x=>['IMPORT_TOO_LARGE','IMPORT_BYTES_MISMATCH'].includes(x.code));
  const ast=LIMITS();ast.syntaxLimits.maxAstNodes=1;
  assert.throws(()=>collectFrontendImports(e,POLICY(),ast),x=>x.code==='SYNTAX_AST_TOO_LARGE');
});
test('collecteur : tous refusés donne diagnostics, sans état de disponibilité inventé',()=>{
  const r=collectFrontendImports(one('import "react";\n'+ENTRY),POLICY(),LIMITS());
  assert.deepEqual(r.modules,[]);assert.deepEqual(r.resolutions,[]);
  assert.equal(r.diagnostics.length,1);
  assert.deepEqual(Object.keys(r).sort(),['diagnostics','modules','resolutions']);
});
