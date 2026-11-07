// Doubles structurels pour le consommateur pur ; intégration Kernel/Python testée séparément.
import test from 'node:test';
import assert from 'node:assert/strict';
import { createShellExtensionPoints } from '../src/shell/composition-descriptor-v1.js';
import { preflightContributions, composeContributionGraph } from '../src/shell/composition-graph-v1.js';

const clone=v=>JSON.parse(JSON.stringify(v));
// Ces DTO sont JSON fermés ; comparer leur sérialisation sans élargir l’adapter commun.
const same=(a,b)=>assert.equal(JSON.stringify(a),JSON.stringify(b));
const key=(owner,id)=>JSON.stringify([owner,id]);
const LIMITS=()=>({maxContributions:1024,maxFacts:4096,maxEdges:4096,maxInputNodes:300000,descriptorLimits:{maxTextLength:4096,maxRequires:64,maxPermissions:64,maxPoints:128,maxLocales:8,maxCatalogKeys:512}});
const POINTS={ROUTE:'routes',PAGE:'pages',COMPONENT:'components',FORM:'forms',NAVIGATION:'navigation-items',TRANSLATION:'translations',UI_PERMISSION:'ui-permissions',UI_SLOT:'main'};
function fixture(specs=[{}],options={}){
  const descriptors=specs.map((s,i)=>{
    const owner=s.owner??'acme.one',type=s.type??'PAGE',point=s.point??'pixs.shell.'+POINTS[type];
    const defaults={
      PAGE:{export:'View'},COMPONENT:{export:'View'},FORM:{export:'View'},
      ROUTE:{path:'/apps/'+i,mode:'CSR',page:'View'},
      NAVIGATION:{route:'/apps/'+i,labelKey:owner+'.label'},
      TRANSLATION:{catalog:{en:{[owner+'.label']:'Label'},fr:{[owner+'.label']:'Étiquette'}}},
      UI_PERMISSION:{key:owner+'.read',fallback:'HIDDEN'},UI_SLOT:{slot:point,export:'View'},
    };
    return {descriptor_version:'1.0.0',owner,owner_version:'1.0.0',type,id:s.id??owner+'.page',entry:'ui/main.mjs',
      version:'1.0.0',requires:s.requires??[],scope:'PUBLIC',point,point_version:'1.0.0',display_permissions:[],
      trust:s.trust??'TRUSTED',mandatory:s.mandatory??false,activation_scope:'PUBLIC',payload:s.payload??defaults[type]};
  });
  const ids=[...new Set(descriptors.map(d=>d.owner))],order=options.order??ids;
  const owners=ids.map((owner,index)=>{
    const root='fixtures/'+owner,trust=specs[descriptors.findIndex(d=>d.owner===owner)].ownerTrust??descriptors.find(d=>d.owner===owner).trust;
    return {index,owner,owner_version:'1.0.0',root,trust,
      manifest:{owner_index:index,path:root+'/component.toml',sha256:'0'.repeat(64),size:0,data_b64:''},
      sources:[{owner_index:index,path:root+'/ui/main.mjs',sha256:'1'.repeat(64),size:0,data_b64:''}]};
  });
  const facets=descriptors.map(d=>Object.fromEntries(['owner','owner_version','type','id','entry','version','requires','scope'].map(k=>[k,d[k]])));
  const modules=owners.map(o=>({owner:o.owner,owner_version:o.owner_version,root:o.root,file:o.root+'/ui/main.mjs',
    text:'',hash:'1'.repeat(64),isEntry:true,descriptors:descriptors.filter(d=>d.owner===o.owner),
    exportedNames:[{name:'View',callable:true,from:'local'}],imports:[]}));
  const admission=[...new Map(descriptors.map(d=>[key(d.owner,d.id),{owner:d.owner,id:d.id,mandatory:d.mandatory}])).values()];
  const modularPoints=options.modularPoints??[];
  const mergeModes=Object.fromEntries([...Object.keys(createShellExtensionPoints().points),...modularPoints.map(p=>p.id)].map(id=>[id,'APPEND']));
  const envelope={schema:'pixs.frontend.plan-envelope/1.0.0',
    capture:{schema:'pixs.frontend.selection/1.0.0',selection_sha256:'2'.repeat(64),environment:options.environment??'DEVELOPMENT',
      provenance_reference:'fixture-only:graph-unit',context_fingerprint:'3'.repeat(64),
      composition:{official_ids:options.official??[],required_ids:[],configured_providers:null,attestations:[]},owners,errors:[]},
    plan:{schema:'pixs.frontend.build-plan/1',order,edges:options.edges??[],facets,diagnostics:[],warnings:[],
      evaluation_scope:[],unevaluated_dimensions:[],globally_compatible:false,sources_sha256:owners.map(o=>({owner:o.owner,sha256:o.manifest.sha256}))},
    ignored_attestation_indices:[],build_limits:{max_manifests:1024,max_manifest_bytes:32768,max_total_bytes:262144,allowed_sources:owners.map(o=>o.manifest.path)},
    context_checksum:'4'.repeat(64),declared_owner_ids:ids};
  const policy={schema:'pixs.frontend.policy/1.0.0',imports:{shellFacades:{'pixs-shell/v1':{exports:[],allowDefault:false,allowNamespace:false}},foreignFacades:{}},
    modularPoints,mergeModes,admission,locales:['en','fr'],renderer:{contract:'pixs.presentation/1.0.0',adapter:'pixs.dom/v1'}};
  return clone({envelope,imports:{modules,resolutions:[],diagnostics:[]},policy});
}
function preflight(f,limits=LIMITS()){return preflightContributions(f.envelope,f.imports,f.policy,limits);}
function facts(p,links=[]){
  const fs=[],edges=[],nodes=new Map(p.contributions.map(c=>[key(c.owner,c.id),c]));
  for(const c of p.contributions)c.requires.forEach((requirement,index)=>{
    const link=links.find(e=>e[0]===c.owner&&e[1]===c.id&&e[2]===index);
    const target=link?nodes.get(key(link[3],link[4])):null;
    fs.push({owner:c.owner,id:c.id,index,requirement,target_id:link?link[4]:requirement,
      candidates:target?[{owner:target.owner,id:target.id,version:target.version}]:[],code:target?'SATISFIED':'MISSING'});
    if(target)edges.push([c.owner,c.id,target.owner,target.id]);
  });
  return {schema:'pixs.frontend.requirement-facts/1.0.0',facts:fs,frontend_edges:[...new Map(edges.map(e=>[JSON.stringify(e),e])).values()],all_satisfied:fs.every(f=>f.code==='SATISFIED')};
}
function run(f,links=[],limits=LIMITS()){
  const p=preflight(f,limits);return {p,g:composeContributionGraph(p,facts(p,links),limits)};
}
function refuses(fn,code){
  let caught;try{fn();}catch(error){caught=error;}
  assert.equal(caught?.code,code);
}
function has(g,id,code){return g.diagnostics.some(d=>d.id===id&&d.code===code);}
function catalog(id='acme.one.text',changes={}){
  return {type:'TRANSLATION',id,payload:{catalog:{en:{'acme.one.label':'Hello {name}'},fr:{'acme.one.label':'Bonjour {name}'}}},...changes};
}
function point(){
  return {id:'acme.parent.area',owner_version:'1.0.0',provider_id:'acme.parent.page',
    definition:{owner:'acme.parent',category:'UI_SLOT',version:'1.0.0',schema:'pixs.frontend.composition-descriptor/1.0.0',guarantees:['DATA_ONLY_DESCRIPTOR','EXPLICIT_ENTRY_EXPORTS']}};
}
function parentChild(withRequires=true){
  return fixture([{owner:'acme.parent',id:'acme.parent.page'},
    {owner:'acme.child',id:'acme.child.slot',type:'UI_SLOT',point:'acme.parent.area',requires:withRequires?['acme.parent.page']:[]}],
    {order:['acme.parent','acme.child'],edges:[['acme.child','acme.parent']],modularPoints:[point()]});
}

test('préflight et graphe purs immuables, sans mutation des entrées',()=>{
  const f=fixture([{mandatory:true}]),before=JSON.stringify(f),{p,g}=run(f);
  assert.equal(g.blocked,false);same(g.order,[{owner:'acme.one',id:'acme.one.page'}]);
  assert.ok(Object.isFrozen(p));assert.ok(Object.isFrozen(g.contributions[0].payload));
  assert.equal(JSON.stringify(f),before);
});
test('owner et version du descripteur ne sont jamais réécrits pour concorder',()=>{
  for(const field of ['owner','owner_version']){
    const f=fixture([{mandatory:true}]);f.imports.modules[0].descriptors[0][field]='foreign';
    const p=preflight(f);assert.equal(p.blocked,true);assert.equal(p.contributions.length,0);
  }
});
test('descripteur surnuméraire retire le propriétaire, pas son voisin',()=>{
  const f=fixture([{owner:'acme.one'},{owner:'acme.two'}]);
  f.imports.modules[0].descriptors.push({...clone(f.imports.modules[0].descriptors[0]),id:'acme.one.extra'});
  const {g}=run(f);same(g.order,[{owner:'acme.two',id:'acme.two.page'}]);
  assert.ok(has(g,'acme.one.page','GRAPH_DESCRIPTOR_UNDECLARED'));
});
test('descripteur absent obligatoire bloque même sans contribution conservée',()=>{
  const f=fixture([{mandatory:true}]);f.imports.modules[0].descriptors=[];
  const {p,g}=run(f);assert.equal(p.blocked,true);assert.equal(g.blocked,true);same(g.contributions,[]);
});
test('doublons sans arbitre et mandatory contradictoire ne devient pas optionnel',()=>{
  const f=fixture([{id:'acme.one.x'},{id:'acme.one.x'}]);
  assert.equal(run(f).g.contributions.length,0);
  f.imports.modules[0].descriptors[0].mandatory=true;
  assert.equal(run(f).p.blocked,true);
  const mismatch=fixture();mismatch.imports.modules[0].descriptors[0].mandatory=true;
  assert.equal(run(mismatch).g.blocked,true);
});
test('empreinte module/capture et diagnostic owner sont recoupés',()=>{
  const f=fixture();f.imports.modules[0].hash='9'.repeat(64);
  refuses(()=>preflight(f),'GRAPH_CAPTURE_INVALID');
  const bad=fixture([{mandatory:true}]);bad.imports.diagnostics.push({owner:'acme.one',path:bad.imports.modules[0].file,code:'SYNTAX_INVALID'});bad.imports.modules=[];
  assert.equal(run(bad).g.blocked,true);
});
test('exports réellement callable requis avant graphe',()=>{
  const f=fixture([{mandatory:true}]);f.imports.modules[0].exportedNames[0].callable=false;
  const {g}=run(f);assert.equal(g.blocked,true);assert.ok(has(g,'acme.one.page','GRAPH_EXPORT_INVALID'));
});
test('SANDBOXED sans adapter et DEVELOPMENT en production refusés',()=>{
  const sandbox=fixture([{trust:'SANDBOXED'}]);
  assert.equal(run(sandbox).g.contributions.length,0);
  const dev=fixture([{trust:'DEVELOPMENT',mandatory:true}],{environment:'PRODUCTION'});
  assert.equal(run(dev).g.blocked,true);
});
test('namespace réservé exige owner officiel et propriété concordante',()=>{
  const spoof=fixture([{id:'pixs.fake',mandatory:true}]);assert.equal(run(spoof).g.blocked,true);
  const reserved=fixture([{owner:'pixs.demo',mandatory:true}]);assert.equal(run(reserved).g.blocked,true);
  const accepted=fixture([{owner:'pixs.demo',mandatory:true}],{official:['pixs.demo']});assert.equal(run(accepted).g.blocked,false);
});
test('intersections avec routes protégées refusées, pas uniquement égalité',()=>{
  for(const path of ['/login','/{section}','/tenants/{x}','/tenants/{x}/scopes/{y}']){
    const f=fixture([{type:'ROUTE',mandatory:true,payload:{path,mode:'CSR',page:'View'}}]);
    assert.equal(run(f).g.blocked,true);
  }
});
test('paramètres répétés refusés dans une seule route',()=>{
  const f=fixture([{type:'ROUTE',payload:{path:'/apps/{id}/{id}',mode:'CSR',page:'View'}}]);
  const {g}=run(f);assert.equal(g.contributions.length,0);assert.ok(has(g,'acme.one.page','GRAPH_COLLISION_ROUTE'));
});
test('deux routes en intersection sont toutes deux retirées, indépendant conservé',()=>{
  const f=fixture([{id:'acme.one.a',type:'ROUTE',payload:{path:'/apps/{id}',mode:'CSR',page:'View'}},
    {id:'acme.one.b',type:'ROUTE',payload:{path:'/apps/item',mode:'CSR',page:'View'}},{id:'acme.one.c'}]);
  const {g}=run(f);same(g.order,[{owner:'acme.one',id:'acme.one.c'}]);
  assert.ok(has(g,'acme.one.a','GRAPH_COLLISION_ROUTE'));assert.ok(has(g,'acme.one.b','GRAPH_COLLISION_ROUTE'));
});

test('paramètres de même nom sur deux routes ne provoquent pas erreur globale',()=>{
  const f=fixture([{id:'acme.one.a',type:'ROUTE',payload:{path:'/apps/{id}',mode:'CSR',page:'View'}},
    {id:'acme.one.b',type:'ROUTE',payload:{path:'/apps/{id}',mode:'CSR',page:'View'}}]);
  const {g}=run(f);assert.equal(g.blocked,false);assert.equal(g.contributions.length,0);
});
test('slots APPEND gardés dans ordre déclaré ; REJECT retire toutes les collisions',()=>{
  const f=fixture([{id:'acme.one.b',type:'UI_SLOT'},{id:'acme.one.a',type:'UI_SLOT'}]);
  same(run(f).g.order.map(o=>o.id),['acme.one.a','acme.one.b']);
  f.policy.mergeModes['pixs.shell.main']='REJECT';
  const {g}=run(f);assert.equal(g.contributions.length,0);
  assert.ok(has(g,'acme.one.a','GRAPH_COLLISION_POINT'));assert.ok(has(g,'acme.one.b','GRAPH_COLLISION_POINT'));
});
test('catalogues en/fr complets et mêmes paramètres nommés',()=>{
  const good=fixture([catalog()]);assert.equal(run(good).g.contributions.length,1);
  for(const mode of ['keys','params','braces']){
    const f=fixture([catalog()]);
    const fr=f.imports.modules[0].descriptors[0].payload.catalog.fr;
    if(mode==='keys')fr['acme.one.extra']='Autre';
    if(mode==='params')fr['acme.one.label']='Bonjour {other}';
    if(mode==='braces')fr['acme.one.label']='}{name}{';
    const {g}=run(f);assert.equal(g.contributions.length,0);assert.ok(has(g,'acme.one.text','GRAPH_COLLISION_CATALOG'));
  }
});
test('catalogue appartient au namespace du composant',()=>{
  const f=fixture([catalog('acme.one.text',{payload:{catalog:{en:{'foreign.label':'Hi'},fr:{'foreign.label':'Salut'}}}})]);
  const {g}=run(f);assert.equal(g.contributions.length,0);assert.ok(has(g,'acme.one.text','GRAPH_NAMESPACE_RESERVED'));
});
test('clés de traduction en collision retirent les deux contributions',()=>{
  const f=fixture([catalog('acme.one.a'),catalog('acme.one.b'),{id:'acme.one.independent'}]);
  const {g}=run(f);same(g.order.map(o=>o.id),['acme.one.independent']);
  assert.ok(has(g,'acme.one.a','GRAPH_COLLISION_CATALOG'));assert.ok(has(g,'acme.one.b','GRAPH_COLLISION_CATALOG'));
});
test('navigation exige une route et son libellé de catalogue disponibles',()=>{
  const f=fixture([{id:'acme.one.route',type:'ROUTE',payload:{path:'/apps/one',mode:'CSR',page:'View'}},
    catalog('acme.one.text',{payload:{catalog:{en:{'acme.one.label':'Hello'},fr:{'acme.one.label':'Bonjour'}}}}),{id:'acme.one.nav',type:'NAVIGATION',payload:{route:'/apps/one',labelKey:'acme.one.label'}}]);
  assert.equal(run(f).g.contributions.length,3);
  f.imports.modules[0].descriptors[1].payload.catalog.fr['acme.one.label']='Bonjour {different}';
  const {g}=run(f);assert.ok(has(g,'acme.one.nav','GRAPH_COLLISION_CATALOG'));
  assert.equal(g.order.some(o=>o.id==='acme.one.nav'),false);
});
test('collision des clés UI_PERMISSION refuse les deux, sans créer un droit',()=>{
  const f=fixture([{id:'acme.one.a',type:'UI_PERMISSION'},{id:'acme.one.b',type:'UI_PERMISSION'}]);
  const {g}=run(f);assert.equal(g.contributions.length,0);
  assert.ok(has(g,'acme.one.a','GRAPH_COLLISION_PERMISSION'));assert.ok(has(g,'acme.one.b','GRAPH_COLLISION_PERMISSION'));
});
test('dépendance intra-composant prime sur tri alphabétique des identifiants',()=>{
  const f=fixture([{id:'acme.one.a',requires:['acme.one.z']},{id:'acme.one.z'}]);
  const {g}=run(f,[['acme.one','acme.one.a',0,'acme.one','acme.one.z']]);
  same(g.order.map(o=>o.id),['acme.one.z','acme.one.a']);
});
test('cycles exacts, dépendants diagnostiqués séparément et indépendants gardés',()=>{
  const f=fixture([{id:'acme.one.a',requires:['acme.one.b']},{id:'acme.one.b',requires:['acme.one.a']},
    {id:'acme.one.c',requires:['acme.one.a']},{id:'acme.one.d'}]);
  const links=[['acme.one','acme.one.a',0,'acme.one','acme.one.b'],['acme.one','acme.one.b',0,'acme.one','acme.one.a'],['acme.one','acme.one.c',0,'acme.one','acme.one.a']];
  const {g}=run(f,links);
  same(g.order.map(o=>o.id),['acme.one.d']);
  assert.ok(has(g,'acme.one.a','GRAPH_CYCLE_CONTRIBUTION'));assert.ok(has(g,'acme.one.b','GRAPH_CYCLE_CONTRIBUTION'));
  assert.equal(has(g,'acme.one.c','GRAPH_CYCLE_CONTRIBUTION'),false);assert.ok(has(g,'acme.one.c','GRAPH_DEPENDENCY_UNAVAILABLE'));
});

test('composante cyclique complète avec arête vers sommet déjà visité',()=>{
  const f=fixture([{id:'acme.one.a',requires:['acme.one.b','acme.one.d']},{id:'acme.one.b',requires:['acme.one.c']},
    {id:'acme.one.c',requires:['acme.one.a']},{id:'acme.one.d',requires:['acme.one.c']},{id:'acme.one.e',requires:['acme.one.a']}]);
  const links=[['acme.one','acme.one.a',0,'acme.one','acme.one.b'],['acme.one','acme.one.a',1,'acme.one','acme.one.d'],
    ['acme.one','acme.one.b',0,'acme.one','acme.one.c'],['acme.one','acme.one.c',0,'acme.one','acme.one.a'],
    ['acme.one','acme.one.d',0,'acme.one','acme.one.c'],['acme.one','acme.one.e',0,'acme.one','acme.one.a']];
  const {g}=run(f,links);
  for(const id of ['a','b','c','d'])assert.ok(has(g,'acme.one.'+id,'GRAPH_CYCLE_CONTRIBUTION'));
  assert.equal(has(g,'acme.one.e','GRAPH_CYCLE_CONTRIBUTION'),false);
  assert.ok(has(g,'acme.one.e','GRAPH_DEPENDENCY_UNAVAILABLE'));
});
test('faits incomplets, index, candidats, edges et agrégat falsifiés refusés',()=>{
  const f=fixture([{id:'acme.one.a',requires:['acme.one.b']},{id:'acme.one.b'}]),p=preflight(f);
  const valid=facts(p,[['acme.one','acme.one.a',0,'acme.one','acme.one.b']]);
  const mutations=[
    v=>v.facts.pop(),v=>v.facts[0].index++,v=>v.facts[0].candidates[0].version='9.0.0',
    v=>v.frontend_edges.push(v.frontend_edges[0].slice()),v=>v.frontend_edges[0][3]='acme.one.a',
    v=>{v.all_satisfied=false;},v=>{v.facts[0].code='READY';},
  ];
  for(const mutate of mutations){const v=clone(valid);mutate(v);refuses(()=>composeContributionGraph(p,v,LIMITS()),'GRAPH_FACTS_INVALID');}
});
test('exigence manquante optionnelle isolée, obligatoire bloque',()=>{
  const f=fixture([{id:'acme.one.a',requires:['acme.absent']},{id:'acme.one.b'}]);
  same(run(f).g.order.map(o=>o.id),['acme.one.b']);
  f.policy.admission[0].mandatory=true;f.imports.modules[0].descriptors[0].mandatory=true;
  assert.equal(run(f).g.blocked,true);
});
test('refus après collision propagé vers dépendant obligatoire',()=>{
  const f=fixture([{id:'acme.one.a',type:'ROUTE',payload:{path:'/apps/x',mode:'CSR',page:'View'}},
    {id:'acme.one.b',type:'ROUTE',payload:{path:'/apps/x',mode:'CSR',page:'View'}},
    {id:'acme.one.c',mandatory:true,requires:['acme.one.a']},{id:'acme.one.d'}]);
  const {g}=run(f,[['acme.one','acme.one.c',0,'acme.one','acme.one.a']]);
  assert.equal(g.blocked,true);same(g.contributions,[]);assert.ok(has(g,'acme.one.c','GRAPH_DEPENDENCY_UNAVAILABLE'));
});
test('point public parent consommé avec dépendances commune et contribution prouvées',()=>{
  const {g}=run(parentChild(),[['acme.child','acme.child.slot',0,'acme.parent','acme.parent.page']]);
  assert.equal(g.blocked,false);same(g.order.map(o=>o.id),['acme.parent.page','acme.child.slot']);
});
test('point public sans dépendance frontend vers son fournisseur refusé',()=>{
  const {g}=run(parentChild(false));
  same(g.order.map(o=>o.id),['acme.parent.page']);
  assert.ok(has(g,'acme.child.slot','GRAPH_POINT_DEPENDENCY_UNDECLARED'));
});
test('fournisseur de point invalide retire aussi les consommateurs',()=>{
  const f=parentChild();f.imports.modules[0].exportedNames[0].callable=false;
  const {p,g}=run(f);
  assert.equal(p.contributions.length,0);assert.equal(g.contributions.length,0);
  assert.ok(has(g,'acme.child.slot','GRAPH_POINT_OWNER_UNAVAILABLE'));
});

test('erreur de capture recoupée par owner_index et admission hors capture',()=>{
  for(const mandatory of [false,true]){
    const f=fixture();
    f.envelope.declared_owner_ids.push('acme.absent');
    f.envelope.capture.errors.push({owner_index:1,owner:'',path:'',code:'SOURCE_MISSING',observed_sha256:''});
    f.policy.admission.push({owner:'acme.absent',id:'acme.absent.page',mandatory});
    const {g}=run(f);assert.equal(g.blocked,mandatory);
    assert.ok(has(g,'acme.absent.page','GRAPH_OWNER_UNAVAILABLE'));
    assert.equal(g.contributions.length,mandatory?0:1);
  }
});
test('points privés ou sans relation commune ne sont pas consommables',()=>{
  const f=parentChild();f.envelope.plan.edges=[];
  const {g}=run(f);
  assert.ok(has(g,'acme.child.slot','GRAPH_POINT_OWNER_UNAVAILABLE'));
  const hidden=fixture([{type:'UI_SLOT',point:'acme.private.slot'}]);
  assert.equal(run(hidden).g.contributions.length,0);
});
test('politique, version, budgets et accès de données stricts',()=>{
  const f=fixture(),extra=clone(f);extra.policy.extra=true;
  refuses(()=>preflight(extra),'GRAPH_POLICY_INVALID');
  const v=clone(f);v.envelope.schema='pixs.frontend.plan-envelope/99';
  refuses(()=>preflight(v),'GRAPH_ENVELOPE_INVALID');
  const limits=LIMITS();limits.maxInputNodes=1;
  refuses(()=>preflight(f,limits),'GRAPH_LIMITS_INVALID');
  let called=false;
  Object.defineProperty(f.envelope,'capture',{get(){called=true;return {};},enumerable:true});
  refuses(()=>preflight(f),'GRAPH_ENVELOPE_INVALID');assert.equal(called,false);
});
test('ordre de découverte des facettes et descripteurs sans effet sur résultat',()=>{
  const a=fixture([{id:'acme.one.z'},{id:'acme.one.a'},{id:'acme.one.m'}]),b=clone(a);
  b.envelope.plan.facets.reverse();b.imports.modules[0].descriptors.reverse();b.policy.admission.reverse();
  same(run(a).g,run(b).g);
});
test('chaîne de 512 contributions résolue sans récursion du graphe',()=>{
  const specs=[],links=[];
  for(let i=0;i<512;i++){
    const id='acme.one.n'+i,next='acme.one.n'+(i+1);
    specs.push({id,requires:i<511?[next]:[]});
    if(i<511)links.push(['acme.one',id,0,'acme.one',next]);
  }
  const {g}=run(fixture(specs),links);
  assert.equal(g.order.length,512);assert.equal(g.order[0].id,'acme.one.n511');assert.equal(g.order[511].id,'acme.one.n0');
});

test('navigation sans paramètres explicites ne consomme pas un libellé paramétré',()=>{
  const f=fixture([{id:'acme.one.route',type:'ROUTE',payload:{path:'/apps/one',mode:'CSR',page:'View'}},catalog(),{id:'acme.one.nav',type:'NAVIGATION',payload:{route:'/apps/one',labelKey:'acme.one.label'}}]);
  const {g}=run(f);assert.ok(has(g,'acme.one.nav','GRAPH_COLLISION_CATALOG'));assert.equal(g.order.some(o=>o.id==='acme.one.nav'),false);
});
