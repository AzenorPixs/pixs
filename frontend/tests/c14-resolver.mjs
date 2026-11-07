// Projection réelle du catalogue Python vers les clients publics JavaScript.
// Les ports HTTP sont des doubles explicites ; aucun renderer/TLS n'est qualifié.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {
  validateTransportResolver, defaultTransportResolver, resolveTransport,
  createQueryClient, createCommandClient,
} from '../src/shell/api-v1.js';

const supplied=JSON.parse(readFileSync(0,'utf8'));
const resolver=validateTransportResolver(supplied);
const bindings=resolver.operations.filter(item=>item.owner==='pixs.pzt'||item.owner==='pixs.dns');
const scopes=[
  {scope_type:'PLATFORM',tenant_id:null,scope_id:null},
  {scope_type:'TENANT',tenant_id:'tenant / % opaque',scope_id:null},
  {scope_type:'TENANT',tenant_id:'tenant / % opaque',scope_id:'périmètre / % opaque'},
];
const cases={};
assert.equal(resolver.version,'1.0.0');
assert.equal(resolver.operations.length,48);
assert.equal(bindings.length,11);
assert.equal(bindings.filter(item=>item.owner==='pixs.pzt').length,4);
assert.equal(bindings.filter(item=>item.owner==='pixs.dns').length,7);
assert.ok(Object.isFrozen(resolver)&&Object.isFrozen(resolver.operations));
for(const binding of bindings){
  assert.deepEqual(Object.keys(binding).sort(),
    ['kind','name','owner','contractVersion','scopes','segments'].sort());
  assert.equal(binding.contractVersion,'1.0.0');
  assert.deepEqual(binding.scopes,['P','T','S']);
}
cases.real_python_projection_accepted=true;

let pathCount=0,clientCount=0;
for(const scope of scopes){
  const snapshot={epoch:7,scope};
  const provider={snapshot:()=>snapshot,isCurrent:value=>
    value.epoch===snapshot.epoch&&JSON.stringify(value.scope)===JSON.stringify(scope)};
  const emitted=[];
  const envelope={status:200,body:{data:{fixture:'réponse de port explicite'},
    meta:{correlation_id:'c14-cross-language',context:scope},links:{}}};
  const queries=createQueryClient({resolver,contextProvider:provider,
    fetchJson:async(path,options)=>{emitted.push({kind:'QUERY',path,options});return envelope;}});
  const commands=createCommandClient({resolver,contextProvider:provider,
    postJson:async(path,body,options)=>{emitted.push({kind:'COMMAND',path,body,options});return envelope;}});
  const root=scope.scope_type==='PLATFORM'?'/api/v1/web/platform'
    :scope.scope_id===null?'/api/v1/web/tenants/tenant%20%2F%20%25%20opaque'
    :'/api/v1/web/tenants/tenant%20%2F%20%25%20opaque/scopes/p%C3%A9rim%C3%A8tre%20%2F%20%25%20opaque';
  for(const binding of bindings){
    const path=resolveTransport(resolver,scope,{kind:binding.kind,name:binding.name});
    assert.equal(path,root+'/'+binding.segments.join('/'));
    pathCount+=1;
    const data={resource_id:'profil / %\nopaque',fixture_values:['B','A','B']};
    if(binding.kind==='QUERY'){
      const result=await queries.query(binding.name,{params:data});
      assert.deepEqual(result.data,envelope.body.data);
      assert.deepEqual(emitted.at(-1).options.params,data);
    }else{
      const result=await commands.intent(binding.name,data,{idempotencyKey:'clé-opaque-'+clientCount});
      assert.equal(result.state,'CONFIRMED');
      assert.deepEqual(emitted.at(-1).body,data);
      assert.equal(emitted.at(-1).options.idempotencyKey,'clé-opaque-'+clientCount);
    }
    assert.equal(emitted.at(-1).path,path);
    assert.deepEqual(emitted.at(-1).options.snapshot,snapshot);
    clientCount+=1;
  }
  assert.equal(emitted.length,11);
}
assert.equal(pathCount,33);
assert.equal(clientCount,33);
cases.paths_three_contexts_opaque_identifiers=true;
cases.actual_public_clients_preserve_owner_inputs=true;

let forbiddenSends=0,refusals=0;
const snapshot={epoch:8,scope:scopes[2]};
const provider={snapshot:()=>snapshot,isCurrent:()=>true};
const missing=defaultTransportResolver();
const queries=createQueryClient({resolver:missing,contextProvider:provider,
  fetchJson:async()=>{forbiddenSends+=1;throw new Error('PORT_NE_DOIT_PAS_ETRE_APPELE');}});
const commands=createCommandClient({resolver:missing,contextProvider:provider,
  postJson:async()=>{forbiddenSends+=1;throw new Error('PORT_NE_DOIT_PAS_ETRE_APPELE');}});
for(const binding of bindings){
  const result=binding.kind==='QUERY'
    ?queries.query(binding.name,{params:{resource_id:'profil'}})
    :commands.intent(binding.name,{resource_id:'profil'},{idempotencyKey:'non-envoyée'});
  await assert.rejects(result,error=>error.code==='SHELL_ROUTE_INVALID');
  refusals+=1;
}
assert.equal(refusals,11);
assert.equal(forbiddenSends,0);
cases.missing_c14_binding_closed_before_transport=true;
console.log(JSON.stringify({cases,case_count:Object.keys(cases).length,
  resolved_paths:pathCount,public_client_calls:clientCount,missing_binding_refusals:refusals,
  transport_is_explicit_test_double:true,renderer_qualified:false}));
