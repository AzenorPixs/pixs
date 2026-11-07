// Intégration réelle C07/capture/AST/faits Python ; aucune exécution des sources capturées.
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { collectFrontendImports,SHELL_ALIAS,SHELL_EXPORTS } from '../scripts/composition-imports-v1.mjs';
import { createShellExtensionPoints } from '../src/shell/composition-descriptor-v1.js';
import { preflightContributions,composeContributionGraph } from '../src/shell/composition-graph-v1.js';
const ROOT=fileURLToPath(new URL('../../',import.meta.url));
const PYTHON='/home/devops/python/current/bin/python3';
const PY="import sys,json,hashlib\nfrom pathlib import Path\nroot=Path.cwd()\nsys.path[:0]=[str(root/'src'),str(root/'frontend/scripts'),str(root/'frontend/tests')]\nfrom test_build_frontend_plan import PlanTests,manifest_dep,att\nfrom build_frontend_plan import prepare_frontend_plan\nspec=json.load(sys.stdin)\nt=PlanTests()\nt.setUp()\ntry:\n    owners=[]\n    for i,s in enumerate(spec):\n        owner=s['owner']\n        raw=manifest_dep(owner,kind=s.get('kind','MODULE'),requires=s.get('requires',[]),dep_components=s.get('dependencies',[]))\n        if 'contribution_id' in s:\n            raw=raw.replace(('id=\"'+owner+'.page\"').encode(),('id=\"'+s['contribution_id']+'\"').encode())\n        owners.append(t._owner('owner'+str(i),owner,raw,js=s['source'].encode('utf-8')))\n    # Conformité des fixtures seulement, aucune attestation de production.\n    doc=t._doc(owners,[s['owner'] for s in spec],[s['owner'] for s in spec],None,[att(s['owner'],idx=i) for i,s in enumerate(spec)])\n    blob,pin=t._blob(doc)\n    print(json.dumps(prepare_frontend_plan(blob,expected_sha256=pin,project_root=root,selection_limits=t._limits()).to_dict()))\nfinally:\n    if not t.doCleanups():\n        raise RuntimeError('FIXTURE_CLEANUP_FAILED')\n";
const PY_FACTS="import sys,json\nfrom pathlib import Path\nroot=Path.cwd()\nsys.path[:0]=[str(root/'src'),str(root/'frontend/scripts')]\nfrom composition_requirements_v1 import analyze_contribution_requirements,RequirementsLimits\np=json.load(sys.stdin)\nresult=analyze_contribution_requirements(tuple(p['facets']),component_order=tuple(p['componentOrder']),component_edges=tuple(tuple(e) for e in p['componentEdges']),limits=RequirementsLimits(128,64,1024))\nprint(json.dumps(result.to_dict()))\n";

const IMPORT_LIMITS={maxSourceBytes:32768,maxTotalSourceBytes:262144,maxModules:32,maxImports:64,maxBindings:128,maxResolutions:64,maxInputNodes:30000,syntaxLimits:{maxSourceBytes:32768,maxAstNodes:4096,maxDescriptorCount:32,maxTextLength:4096,maxLiteralItems:4096,maxLiteralDepth:64}};
const GRAPH_LIMITS={maxContributions:128,maxFacts:1024,maxEdges:1024,maxInputNodes:100000,descriptorLimits:{maxTextLength:4096,maxRequires:64,maxPermissions:64,maxPoints:128,maxLocales:8,maxCatalogKeys:512}};
function python(program,input){
  const r=spawnSync(PYTHON,['-B','-c',program],{cwd:ROOT,input:JSON.stringify(input),encoding:'utf8',timeout:15000,maxBuffer:1024*1024});
  assert.ifError(r.error);assert.equal(r.status,0,r.stderr);return JSON.parse(r.stdout);
}
function spec(owner,changes={}){
  const requires=changes.requires??[];
  const descriptor={descriptor_version:'1.0.0',owner,owner_version:'1.0.0',type:'PAGE',id:changes.contribution_id??owner+'.page',
    entry:'frontend/main.mjs',version:'1.0.0',requires,scope:'PUBLIC',point:'pixs.shell.pages',point_version:'1.0.0',display_permissions:[],
    trust:'TRUSTED',mandatory:changes.descriptor_mandatory??changes.mandatory??true,activation_scope:'PUBLIC',payload:{export:'View'}};
  return {owner,requires,mandatory:changes.mandatory??true,...changes,source:changes.source??((changes.prefix??'')+'\nexport const frontendContributions='+JSON.stringify([descriptor])+';\nexport const View=()=>null;\n')};
}
function flow(specs,foreignFacades={}){
  const envelope=python(PY,specs);
  const policy={schema:'pixs.frontend.policy/1.0.0',imports:{shellFacades:{[SHELL_ALIAS]:{exports:[...SHELL_EXPORTS],allowDefault:false,allowNamespace:false}},foreignFacades},
    modularPoints:[],mergeModes:Object.fromEntries(Object.keys(createShellExtensionPoints().points).map(id=>[id,'APPEND'])),
    admission:specs.map(s=>({owner:s.owner,id:s.contribution_id??s.owner+'.page',mandatory:s.mandatory})),
    locales:['en','fr'],renderer:{contract:'pixs.presentation/1.0.0',adapter:'pixs.dom/v1'}};
  const imports=collectFrontendImports(envelope,policy.imports,IMPORT_LIMITS);
  const preflight=preflightContributions(envelope,imports,policy,GRAPH_LIMITS);
  const requirementFacts=python(PY_FACTS,preflight);
  const graph=composeContributionGraph(preflight,requirementFacts,GRAPH_LIMITS);
  return {envelope,imports,preflight,requirementFacts,graph};
}

test('vrai Kernel, façade publique, captures AST et faits SemVer cohérents',()=>{
  delete globalThis.GRAPH_INTEGRATION_EXECUTED;
  const result=flow([
    spec('acme.app',{kind:'SUBMODULE',requires:['acme.lib.page >=1.0.0'],dependencies:['acme.lib >=1.0.0'],prefix:'import { View as LibView } from "acme-lib/v1";\nglobalThis.GRAPH_INTEGRATION_EXECUTED=true;'}),
    spec('acme.lib'),
  ],{'acme-lib/v1':{owner:'acme.lib',entry:'frontend/main.mjs',exports:['View']}});
  assert.deepEqual(result.envelope.plan.order,['acme.lib','acme.app']);
  assert.equal(result.imports.diagnostics.length,0);
  assert.equal(result.requirementFacts.facts[0].code,'SATISFIED');
  assert.deepEqual(result.graph.order.map(o=>o.owner),['acme.lib','acme.app']);
  assert.equal(result.graph.blocked,false);
  assert.equal(globalThis.GRAPH_INTEGRATION_EXECUTED,undefined);
  assert.equal(result.envelope.plan.globally_compatible,false);
});
test('vrai matcher SemVer refuse version de contribution incompatible',()=>{
  const r=flow([spec('acme.app',{requires:['acme.lib.page >=2.0.0'],dependencies:['acme.lib >=1.0.0']}),spec('acme.lib')]);
  assert.equal(r.requirementFacts.facts[0].code,'INCOMPATIBLE');
  assert.equal(r.graph.blocked,true);assert.deepEqual(r.graph.contributions,[]);
});
test('source illisible optionnelle selon policy isolée avant faits, indépendant gardé',()=>{
  const r=flow([spec('acme.bad',{mandatory:false,source:'export const broken=;\n'}),spec('acme.good')]);
  assert(r.imports.diagnostics.some(d=>d.owner==='acme.bad'&&d.code==='SYNTAX_INVALID'));
  assert.deepEqual(r.preflight.facets.map(f=>f.owner),['acme.good']);
  assert.equal(r.requirementFacts.facts.length,0);
  assert.deepEqual(r.graph.order.map(o=>o.owner),['acme.good']);
});
test('source illisible obligatoire selon policy bloque sans deviner son descripteur',()=>{
  const r=flow([spec('acme.bad',{source:'export const broken=;\n'}),spec('acme.good')]);
  assert.equal(r.preflight.blocked,true);assert.equal(r.graph.blocked,true);assert.deepEqual(r.graph.contributions,[]);
});
test('désaccord policy/mandatory du vrai descripteur bloque',()=>{
  const r=flow([spec('acme.one',{mandatory:true,descriptor_mandatory:false})]);
  assert.equal(r.preflight.blocked,true);assert.equal(r.graph.blocked,true);
});
test('fait MISSING réel retire optionnel et conserve indépendant',()=>{
  const r=flow([spec('acme.one',{mandatory:false,requires:['acme.absent.page >=1.0.0']}),spec('acme.good')]);
  assert.equal(r.requirementFacts.facts[0].code,'MISSING');
  assert.deepEqual(r.graph.order.map(o=>o.owner),['acme.good']);
});
test('façade sans dépendance commune réelle refuse importeur optionnel',()=>{
  const r=flow([spec('acme.app',{mandatory:false,prefix:'import { View as LibView } from "acme-lib/v1";'}),spec('acme.lib')],
    {'acme-lib/v1':{owner:'acme.lib',entry:'frontend/main.mjs',exports:['View']}});
  assert(r.imports.diagnostics.some(d=>d.owner==='acme.app'&&d.code==='IMPORT_FACADE_UNDECLARED'));
  assert.deepEqual(r.graph.order.map(o=>o.owner),['acme.lib']);
});
test('reconnaissance structurelle pixs.* ne confère pas propriété frontend',()=>{
  const r=flow([spec('acme.one',{contribution_id:'pixs.spoof'})]);
  assert.equal(r.envelope.plan.facets[0].id,'pixs.spoof');
  assert.equal(r.preflight.blocked,true);
  assert(r.graph.diagnostics.some(d=>d.code==='GRAPH_NAMESPACE_RESERVED'));
});
