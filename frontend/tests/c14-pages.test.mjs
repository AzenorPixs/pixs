// Pages propriétaires réelles ; contexte et ports moteur/HTTP de recette explicites.
import test from 'node:test';
import assert from 'node:assert/strict';
import {PztManagementPage,frontendContributions as pzt} from '../../src/pixs/pzt/frontend.mjs';
import {DnsManagementPage,frontendContributions as dns} from '../../src/pixs/dns/frontend.mjs';
import {validatePresentationTree,validatePresentationFieldInput} from '../src/shell/presentation-contract-v1.js';
import {createPresentationAdapter} from '../src/shell/presentation-adapter-v1.js';

const limits=()=>({maxNodes:256,maxDepth:32,maxChildren:128,maxTextLength:4096,maxParams:32,
  maxFields:128,maxBindings:128,maxDataNodes:65536,maxBodyDepth:32,maxBodyNodes:4096});
const owners=[{owner:'pixs.pzt',page:PztManagementPage,descriptors:pzt},
  {owner:'pixs.dns',page:DnsManagementPage,descriptors:dns}];
const context=()=>({state:'ACTIVE',epoch:7,scope:{scope_type:'TENANT',tenant_id:'tenant / opaque',scope_id:'scope % opaque'}});
function ctx(item){
  return {owner:item.owner,id:item.owner+'.management.page',
    catalogs:item.descriptors.find(d=>d.type==='TRANSLATION').payload.catalog,
    routes:[],slots:[],components:[],limits:limits()};
}
function nodes(tree){
  const all=[],pending=[tree];while(pending.length){const n=pending.pop();all.push(n);pending.push(...n.children);}return all;
}
const forms=tree=>nodes(tree).filter(n=>n.kind==='form');
const findForm=(tree,id)=>forms(tree).find(n=>n.props.id===id);
function config(owner){
  const governance={profile_version:'1.0.0',data_asset_id:'actif',owner_component:owner,source_of_truth:'source',
    data_classes:['CONFIGURATION'],confidentiality:'INTERNAL',personal_data:'NONE',purpose_refs:[],
    retention_policy:'retention',deletion_policy:'deletion',residency_constraints:[],authorized_consumers:[],
    processor_refs:[],export_policy:'export',lineage:'lineage'};
  const base={schema_version:'1.0.0',owner_id:owner,config_revision:3,governance,
    secret_refs:[{owner_id:owner,entry_id:'référence / opaque',source:'coffre'}]};
  return owner==='pixs.pzt'?{...base,v6_enabled:false,plan_ref:'plan',budget_ref:'budget'}
    :{...base,suffix:'pzt.test.internal',ttl_positive:30,ttl_negative:5,views:['vue B','vue A','vue B']};
}
function loaded(item,contextValue=context()){
  const data={schema_version:'1.0.0',resource_id:item.owner+'.fixture:profil / opaque',
    config_revision:3,business_state:'DECLARED',persistence_state:'ACTIVE',retention_state:'RETAINED',configuration:config(item.owner)};
  return {actions:{load_profile:{kind:'QUERY',phase:'LOADED',sequence:4,
    response:{data,meta:{context:contextValue.scope},links:{}}}},fields:{}};
}
function page(item,state={},contextValue=context()){
  const result=item.page({context:contextValue,state,api:{},routeParams:{}});
  assert.equal(result.schema,'pixs.presentation/1.0.0');
  return validatePresentationTree(result.root,ctx(item));
}

test('C14 pages : session inactive sans formulaire ni action',()=>{
  for(const item of owners){
    const tree=page(item,{}, {...context(),state:'INACTIVE'});
    assert.equal(forms(tree).length,0);
    assert.equal(nodes(tree).filter(n=>n.kind==='button').length,0);
  }
});
test('C14 pages : creation fermee et declarations sans autorite cliente',()=>{
  for(const item of owners){
    const tree=page(item),form=findForm(tree,'create_profile');
    assert.ok(form);assert.ok(findForm(tree,'load_profile'));
    assert.equal(form.props.intent.body.expected_revision,0);
    assert.equal(form.props.intent.body.configuration.owner_id,item.owner);
    assert.equal(Object.hasOwn(form.props.intent.body,'metadata'),false);
    assert.equal(Object.hasOwn(form.props.intent.body,'subject_id'),false);
    assert.equal(nodes(form).find(n=>n.kind==='field'&&n.props.name==='waive_audit').props.initial,false);
  }
});
test('C14 pages : lecture qualifiee et revision CAS derivee du serveur',()=>{
  for(const item of owners){
    const state=loaded(item),before=JSON.stringify(state),tree=page(item,state);
    const form=findForm(tree,'save_profile');
    assert.ok(form);assert.equal(form.props.intent.body.expected_revision,3);
    assert.equal(form.props.intent.body.configuration.config_revision,4);
    assert.equal(form.props.intent.body.resource_id,state.actions.load_profile.response.data.resource_id);
    assert.equal(JSON.stringify(state),before);
    assert.ok(Object.isFrozen(tree));assert.ok(Object.isFrozen(form.props.intent.body));
    if(item.owner==='pixs.dns'){
      assert.ok(findForm(tree,'declare_name'));assert.ok(findForm(tree,'retire_name'));
      assert.ok(findForm(tree,'resolve_name'));
    }
  }
});
test('C14 pages : reponse dun ancien contexte fermee',()=>{
  for(const item of owners){
    const state=loaded(item);state.actions.load_profile.response.meta.context.tenant_id='autre tenant';
    assert.equal(findForm(page(item,state),'save_profile'),undefined);
  }
});
test('C14 pages : issue UNKNOWN conserve seulement le formulaire concerne',()=>{
  for(const item of owners){
    const state=loaded(item);
    state.actions.save_profile={kind:'COMMAND',phase:'UNKNOWN',sequence:8,response:null};
    const tree=page(item,state);
    assert.deepEqual(forms(tree).map(n=>n.props.id),['save_profile']);
    assert.equal(nodes(tree).filter(n=>n.kind==='button'&&!n.props.submit).length,0);
    assert.ok(nodes(tree).some(n=>n.kind==='text'&&n.props.key===item.owner+'.unknownOutcome'));
  }
});
test('C14 pages : mutation confirmee impose relecture avant nouvelle mutation',()=>{
  for(const item of owners){
    const state=loaded(item),data=state.actions.load_profile.response.data;
    state.actions.save_profile={kind:'COMMAND',phase:'CONFIRMED',sequence:9,
      response:{data:{resource_id:data.resource_id,config_revision:4}}};
    const tree=page(item,state);
    assert.equal(findForm(tree,'save_profile'),undefined);
    assert.ok(nodes(tree).some(n=>n.kind==='text'&&n.props.key===item.owner+'.reloadNeeded'));
  }
});
test('C14 pages : listes ordonnees et references multiligne intactes',()=>{
  for(const item of owners){
    const state=loaded(item),configuration=state.actions.load_profile.response.data.configuration;
    configuration.governance.source_of_truth='ligne un\nligne deux';
    configuration.secret_refs[0].entry_id='secret\nopaque';
    if(item.owner==='pixs.pzt')configuration.plan_ref='plan\nopaque';
    const form=findForm(page(item,state),'save_profile');
    assert.equal(form.props.intent.body.configuration.governance.source_of_truth,'ligne un\nligne deux');
    assert.equal(form.props.intent.bindings.some(b=>b.field==='gov_source_of_truth'),false);
    const refs=nodes(form).find(n=>n.kind==='field'&&n.props.name==='secret_refs');
    assert.equal(JSON.stringify(validatePresentationFieldInput(refs,refs.props.initial,limits())),JSON.stringify(configuration.secret_refs));
    if(item.owner==='pixs.pzt'){
      assert.equal(form.props.intent.body.configuration.plan_ref,'plan\nopaque');
      assert.equal(form.props.intent.bindings.some(b=>b.field==='plan_ref'),false);
    }else{
      const views=nodes(form).find(n=>n.kind==='field'&&n.props.name==='views');
      assert.deepEqual(views.props.initial,['vue B','vue A','vue B']);
      assert.deepEqual(validatePresentationFieldInput(views,views.props.initial,limits()),views.props.initial);
    }
  }
});
test('C14 pages : TTL typés et depassements refuses avant transport',()=>{
  const item=owners[1],form=findForm(page(item,loaded(item)),'save_profile');
  for(const name of ['ttl_positive','ttl_negative']){
    const field=nodes(form).find(n=>n.kind==='field'&&n.props.name===name);
    assert.equal(validatePresentationFieldInput(field,0,limits()),0);
    for(const bad of [-1,field.props.maximum+1,true,'5',1.5]){
      let refused=false;try{validatePresentationFieldInput(field,bad,limits());}catch{refused=true;}assert.equal(refused,true);
    }
  }
});
test('C14 pages : adapter commun rend les champs reels sans HTML brut',()=>{
  for(const item of owners){
    const descriptors=item.descriptors,view=page(item,loaded(item)),catalog=ctx(item).catalogs.fr;
    let sequence=0;
    const adapter=createPresentationAdapter({
      h:(type,props,...children)=>({type,props,children}),Link:()=>null,
      // Le moteur C11 garde la construction DOM des champs typés.
      // Ce double vérifie la délégation par le vrai contrat et le vrai adapter.
      field:(n,args)=>({type:n.variant==='string-list'||n.variant==='record-list'?'textarea':'input',
        props:{id:args.id,name:n.props.name,disabled:args.disabled,
          type:n.variant==='boolean'?'checkbox':n.variant==='integer'?'number':'text'},children:[]}),
      label:(key,params)=>catalog[key].replace(/\{([A-Za-z][A-Za-z0-9_]*)\}/g,(_,k)=>String(params[k])),
      id:()=> 'c14-ui-'+sequence++,state:()=>({state:'IDLE',message:'Prêt',canSubmit:true,fieldsDisabled:false}),
      submit:async()=>({state:'UNKNOWN'}),readFields:()=>({}),slot:()=>null,component:()=>null,onError:()=>{}
    });
    const result=adapter.render(view,ctx(item)),pending=[result],all=[];
    while(pending.length){
      const n=pending.pop();if(Array.isArray(n)){pending.push(...n);continue;}
      if(n&&typeof n==='object'){all.push(n);if(n.children)pending.push(...n.children);}
    }
    assert.ok(all.some(n=>n.type==='form'));assert.ok(all.some(n=>n.type==='input'));
    for(const n of all){
      assert.equal(Object.hasOwn(n.props||{},'dangerouslySetInnerHTML'),false);
      assert.equal(Object.hasOwn(n.props||{},'style'),false);
    }
  }
});

test('C14 pages : retrait et conservation visibles sans actions DNS incompatibles',()=>{
  for(const item of owners){
    const state=loaded(item),data=state.actions.load_profile.response.data;
    data.business_state='RETIRED';
    const tree=page(item,state);
    assert.ok(nodes(tree).some(n=>n.kind==='text'&&n.props.key===item.owner+'.desiredRetired'));
    const lifecycle=nodes(tree).find(n=>n.kind==='text'&&n.props.key===item.owner+'.dataLifecycle');
    assert.equal(lifecycle.props.params.persistence,'ACTIVE');
    assert.equal(lifecycle.props.params.retention,'RETAINED');
    assert.equal(findForm(tree,'retire_profile'),undefined);
    assert.equal(findForm(tree,'save_profile').props.key,item.owner+'.redeclare');
    if(item.owner==='pixs.dns'){
      assert.equal(findForm(tree,'declare_name'),undefined);
      assert.equal(findForm(tree,'retire_name'),undefined);
      assert.equal(findForm(tree,'resolve_name'),undefined);
    }
  }
});
