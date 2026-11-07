// Gestion propriétaire : arbres de données, sans DOM, moteur, jeton ou store du Shell.
const OWNER = 'pixs.dns';
const MODULE = 'dns';
const GOV_TEXT = ['profile_version','data_asset_id','source_of_truth','confidentiality','personal_data','retention_policy','deletion_policy','export_policy','lineage'];
const GOV_LISTS = ['data_classes','purpose_refs','residency_constraints','authorized_consumers','processor_refs'];
const COMMAND_FORMS = ['create_profile','save_profile','retire_profile','declare_name','retire_name'];

function node(kind, variant, props, children) {
  return {kind, variant, props, children:children || []};
}
function label(suffix, params) { return {key:OWNER+'.'+suffix, params:params || {}}; }
function text(suffix, params) { return node('text','body',label(suffix,params)); }
function heading(suffix) { return node('heading','section',label(suffix)); }
function status(id, kind) { return node('status',kind,{for:id}); }
function record(value) { return value !== null && typeof value === 'object' && !Array.isArray(value); }
function scalar(value) { return typeof value === 'string' && value.length > 0; }
function sameScope(a,b) {
  return record(a) && record(b) && a.scope_type === b.scope_type &&
    a.tenant_id === b.tenant_id && a.scope_id === b.scope_id;
}
function action(state,id) {
  if(!state || !state.actions) return null;
  switch(id) {
    case 'create_profile': return state.actions.create_profile || null;
    case 'save_profile': return state.actions.save_profile || null;
    case 'retire_profile': return state.actions.retire_profile || null;
    case 'declare_name': return state.actions.declare_name || null;
    case 'retire_name': return state.actions.retire_name || null;
    case 'load_profile': return state.actions.load_profile || null;
    case 'load_applied': return state.actions.load_applied || null;
    case 'resolve_name': return state.actions.resolve_name || null;
    default: return null;
  }
}
function responseData(state,id,context) {
  const a = action(state,id);
  if (!a || a.kind !== 'QUERY' || a.phase !== 'LOADED' || !record(a.response) ||
      !record(a.response.meta) || !sameScope(a.response.meta.context,context.scope)) return null;
  return a.response.data;
}
function field(name,suffix,variant,initial,extra) {
  return node('field',variant,Object.assign({name,key:OWNER+'.'+suffix,params:{},required:true,initial},extra || {}));
}
function button(id,suffix) {
  return node('button','primary',{id:id+'_submit',key:OWNER+'.'+suffix,params:{},submit:true,intent:null});
}
function form(id,suffix,intent,children,modelKey,kind) {
  return node('form','stack',{id,key:OWNER+'.'+suffix,params:{},intent,modelKey},
    children.concat([button(id,suffix),status(id,kind || 'command')]));
}
function queryForm(id,suffix,query,params,fields,bindings,key) {
  return form(id,suffix,{query,params,bindings},fields,key,'query');
}
function placeholder(initial) {
  return typeof initial==='string' && initial.includes('\n') ? initial : null;
}
function addField(body,fields,bindings,name,path,suffix,variant,initial,extra) {
  // Le body est construit explicitement ; les références multiligne existantes
  // y restent intactes sans passage par une entrée texte monoligne.
  if(variant==='text' && typeof initial==='string' && initial.includes('\n')) {
    fields.push(text(suffix));
    fields.push(text('preservedValue',{value:initial}));
    return;
  }
  fields.push(field(name,suffix,variant,initial,extra));
  bindings.push({field:name,path});
}
function value(source,name,empty) {
  if(!source) return empty;
  switch(name) {
    case 'profile_version': return Object.hasOwn(source,'profile_version') ? source.profile_version : empty;
    case 'data_asset_id': return Object.hasOwn(source,'data_asset_id') ? source.data_asset_id : empty;
    case 'source_of_truth': return Object.hasOwn(source,'source_of_truth') ? source.source_of_truth : empty;
    case 'confidentiality': return Object.hasOwn(source,'confidentiality') ? source.confidentiality : empty;
    case 'personal_data': return Object.hasOwn(source,'personal_data') ? source.personal_data : empty;
    case 'retention_policy': return Object.hasOwn(source,'retention_policy') ? source.retention_policy : empty;
    case 'deletion_policy': return Object.hasOwn(source,'deletion_policy') ? source.deletion_policy : empty;
    case 'export_policy': return Object.hasOwn(source,'export_policy') ? source.export_policy : empty;
    case 'lineage': return Object.hasOwn(source,'lineage') ? source.lineage : empty;
    case 'data_classes': return Object.hasOwn(source,'data_classes') ? source.data_classes : empty;
    case 'purpose_refs': return Object.hasOwn(source,'purpose_refs') ? source.purpose_refs : empty;
    case 'residency_constraints': return Object.hasOwn(source,'residency_constraints') ? source.residency_constraints : empty;
    case 'authorized_consumers': return Object.hasOwn(source,'authorized_consumers') ? source.authorized_consumers : empty;
    case 'processor_refs': return Object.hasOwn(source,'processor_refs') ? source.processor_refs : empty;
    case 'v6_enabled': return Object.hasOwn(source,'v6_enabled') ? source.v6_enabled : empty;
    case 'plan_ref': return Object.hasOwn(source,'plan_ref') ? source.plan_ref : empty;
    case 'budget_ref': return Object.hasOwn(source,'budget_ref') ? source.budget_ref : empty;
    case 'suffix': return Object.hasOwn(source,'suffix') ? source.suffix : empty;
    case 'ttl_positive': return Object.hasOwn(source,'ttl_positive') ? source.ttl_positive : empty;
    case 'ttl_negative': return Object.hasOwn(source,'ttl_negative') ? source.ttl_negative : empty;
    case 'views': return Object.hasOwn(source,'views') ? source.views : empty;
    case 'secret_refs': return Object.hasOwn(source,'secret_refs') ? source.secret_refs : empty;
    default: return empty;
  }
}
function governanceFields(body,fields,bindings,current) {
  addField(body,fields,bindings,'gov_profile_version',['configuration','governance','profile_version'],'gov_profile_version','text',value(current,'profile_version',''));
  addField(body,fields,bindings,'gov_data_asset_id',['configuration','governance','data_asset_id'],'gov_data_asset_id','text',value(current,'data_asset_id',''));
  addField(body,fields,bindings,'gov_source_of_truth',['configuration','governance','source_of_truth'],'gov_source_of_truth','text',value(current,'source_of_truth',''));
  addField(body,fields,bindings,'gov_confidentiality',['configuration','governance','confidentiality'],'gov_confidentiality','text',value(current,'confidentiality',''));
  addField(body,fields,bindings,'gov_personal_data',['configuration','governance','personal_data'],'gov_personal_data','text',value(current,'personal_data',''));
  addField(body,fields,bindings,'gov_retention_policy',['configuration','governance','retention_policy'],'gov_retention_policy','text',value(current,'retention_policy',''));
  addField(body,fields,bindings,'gov_deletion_policy',['configuration','governance','deletion_policy'],'gov_deletion_policy','text',value(current,'deletion_policy',''));
  addField(body,fields,bindings,'gov_export_policy',['configuration','governance','export_policy'],'gov_export_policy','text',value(current,'export_policy',''));
  addField(body,fields,bindings,'gov_lineage',['configuration','governance','lineage'],'gov_lineage','text',value(current,'lineage',''));
  addField(body,fields,bindings,'gov_data_classes',['configuration','governance','data_classes'],'gov_data_classes','string-list',value(current,'data_classes',[]),{minItems:0,maxItems:null,itemRequired:true});
  addField(body,fields,bindings,'gov_purpose_refs',['configuration','governance','purpose_refs'],'gov_purpose_refs','string-list',value(current,'purpose_refs',[]),{minItems:0,maxItems:null,itemRequired:true});
  addField(body,fields,bindings,'gov_residency_constraints',['configuration','governance','residency_constraints'],'gov_residency_constraints','string-list',value(current,'residency_constraints',[]),{minItems:0,maxItems:null,itemRequired:true});
  addField(body,fields,bindings,'gov_authorized_consumers',['configuration','governance','authorized_consumers'],'gov_authorized_consumers','string-list',value(current,'authorized_consumers',[]),{minItems:0,maxItems:null,itemRequired:true});
  addField(body,fields,bindings,'gov_processor_refs',['configuration','governance','processor_refs'],'gov_processor_refs','string-list',value(current,'processor_refs',[]),{minItems:0,maxItems:null,itemRequired:true});
}
function waiverFields(body,fields,bindings) {
  addField(body,fields,bindings,'waive_audit',['authorization_intent','waive_audit'],
    'waiveAudit','boolean',false);
  addField(body,fields,bindings,'waive_governance',['authorization_intent','waive_governance'],
    'waiveGovernance','boolean',false);
}
function configurationForm(id,current,resource,revision,key,businessState) {
  const existing=current || null;
  const governanceCurrent=existing && existing.governance;
  const governance={owner_component:OWNER,profile_version:placeholder(value(governanceCurrent,'profile_version','')),data_asset_id:placeholder(value(governanceCurrent,'data_asset_id','')),source_of_truth:placeholder(value(governanceCurrent,'source_of_truth','')),confidentiality:placeholder(value(governanceCurrent,'confidentiality','')),personal_data:placeholder(value(governanceCurrent,'personal_data','')),retention_policy:placeholder(value(governanceCurrent,'retention_policy','')),deletion_policy:placeholder(value(governanceCurrent,'deletion_policy','')),export_policy:placeholder(value(governanceCurrent,'export_policy','')),lineage:placeholder(value(governanceCurrent,'lineage','')),data_classes:null,purpose_refs:null,residency_constraints:null,authorized_consumers:null,processor_refs:null};
  const configuration=MODULE==='pzt'
    ? {schema_version:'1.0.0',owner_id:OWNER,config_revision:revision+1,governance,secret_refs:null,
       v6_enabled:null,plan_ref:placeholder(value(existing,'plan_ref','')),
       budget_ref:placeholder(value(existing,'budget_ref',''))}
    : {schema_version:'1.0.0',owner_id:OWNER,config_revision:revision+1,governance,secret_refs:null,
       suffix:placeholder(value(existing,'suffix','')),ttl_positive:null,ttl_negative:null,views:null};
  const body={schema_version:'1.0.0',resource_id:existing?resource:placeholder(resource),
    expected_revision:revision,configuration,authorization_intent:{waive_audit:null,waive_governance:null}};
  const fields=[],bindings=[];
  if(!existing) addField(body,fields,bindings,'resource_id',['resource_id'],'profileRef','text',resource || '');
  fields.push(heading('configuration'));
  if(MODULE==='pzt') {
    addField(body,fields,bindings,'v6_enabled',['configuration','v6_enabled'],'ipv6Desired','boolean',value(existing,'v6_enabled',false));
    addField(body,fields,bindings,'plan_ref',['configuration','plan_ref'],'planRef','text',value(existing,'plan_ref',''));
    addField(body,fields,bindings,'budget_ref',['configuration','budget_ref'],'budgetRef','text',value(existing,'budget_ref',''));
  } else {
    addField(body,fields,bindings,'suffix',['configuration','suffix'],'suffix','text',value(existing,'suffix',''));
    addField(body,fields,bindings,'ttl_positive',['configuration','ttl_positive'],'ttlPositive','integer',
      value(existing,'ttl_positive',null),{minimum:0,maximum:30});
    addField(body,fields,bindings,'ttl_negative',['configuration','ttl_negative'],'ttlNegative','integer',
      value(existing,'ttl_negative',null),{minimum:0,maximum:5});
    addField(body,fields,bindings,'views',['configuration','views'],'views','string-list',
      value(existing,'views',[]),{minItems:1,maxItems:null,itemRequired:true});
  }
  fields.push(heading('governance'));
  governanceFields(body,fields,bindings,existing && existing.governance);
  fields.push(heading('secretReferences'));
  const columns=[
    {name:'owner_id',key:OWNER+'.secretOwner',params:{},required:true},
    {name:'entry_id',key:OWNER+'.secretEntry',params:{},required:true},
    {name:'source',key:OWNER+'.secretSource',params:{},required:true},
  ];
  addField(body,fields,bindings,'secret_refs',['configuration','secret_refs'],'secretReferences','record-list',
    value(existing,'secret_refs',[]),{minItems:0,maxItems:null,columns});
  fields.push(heading('waivers'));
  waiverFields(body,fields,bindings);
  return form(id,existing?(businessState==='RETIRED'?'redeclare':'save'):'create',
    {command:'declare_desired_'+MODULE,body,bindings},fields,key);
}
function retirementForm(data,key) {
  const body={schema_version:'1.0.0',resource_id:data.resource_id,expected_revision:data.config_revision,reason:null,
    authorization_intent:{waive_audit:null,waive_governance:null}};
  const fields=[],bindings=[];
  addField(body,fields,bindings,'reason',['reason'],'reason','text','');
  waiverFields(body,fields,bindings);
  return form('retire_profile','retire',{command:'retire_desired_'+MODULE,body,bindings},fields,key);
}
function nameForm(data,key,retire) {
  const body=retire
    ? {schema_version:'1.0.0',resource_id:data.resource_id,expected_revision:data.config_revision,
       name:null,view:null,authorization_intent:{waive_audit:null,waive_governance:null}}
    : {schema_version:'1.0.0',resource_id:data.resource_id,expected_revision:data.config_revision,
       name:null,view:null,target_ref:null,authorization_intent:{waive_audit:null,waive_governance:null}};
  const fields=[],bindings=[];
  addField(body,fields,bindings,'name',['name'],'dnsName','text','');
  addField(body,fields,bindings,'view',['view'],'dnsView','text','');
  if(!retire) addField(body,fields,bindings,'target_ref',['target_ref'],'targetRef','text','');
  waiverFields(body,fields,bindings);
  const id=retire?'retire_name':'declare_name';
  return form(id,retire?'retireName':'declareName',{command:id,body,bindings},fields,key);
}
function changedAfterRead(state,data) {
  for(const id of COMMAND_FORMS) {
    const a=action(state,id);
    if(a && a.phase==='CONFIRMED' && a.response && a.response.data &&
        a.response.data.resource_id===data.resource_id &&
        Number.isSafeInteger(a.response.data.config_revision) &&
        a.response.data.config_revision>data.config_revision) return true;
  }
  return false;
}
function observation(state,context,resource,key) {
  const intent={query:'get_applied_'+MODULE,params:{resource_id:resource},bindings:[]};
  const nodes=[node('button','secondary',{id:'load_applied',key:OWNER+'.refreshObservation',
    params:{},submit:false,intent}),status('load_applied','query')];
  const data=responseData(state,'load_applied',context);
  if(data && data.resource_id===resource) {
    if(data.application_status==='UNKNOWN' && data.measurement_status==='UNMEASURED' &&
        data.applied_present===null && data.applied_revision===null && data.measurements===null)
      nodes.push(text('observationUnknown'));
    else nodes.push(text('observationUnavailable'));
  }
  return node('section','stack',{},nodes);
}
function policyForm(resource,key) {
  return queryForm('resolve_name','inspectName','resolve_view_policy',
    {resource_id:resource,view:null,name:null},
    [field('view','dnsView','text',''),field('name','dnsName','text','')],
    [{field:'view',path:['view']},{field:'name',path:['name']}],key);
}
function policyView(state,context,resource) {
  const data=responseData(state,'resolve_name',context);
  if(!data || data.resource_id!==resource) return [];
  if(data.target_verification!=='UNVERIFIED' || data.application_status!=='UNKNOWN' ||
      data.measurement_status!=='UNMEASURED' || data.applied_present!==null ||
      data.applied_revision!==null) return [text('observationUnavailable')];
  const out=[text(data.desired_name_present?'nameDeclared':'nameUndeclared')];
  if(data.desired_name_present && scalar(data.desired_target_ref))
    out.push(text('desiredTarget',{target:data.desired_target_ref}));
  if(Number.isSafeInteger(data.ttl_positive_ceiling) && Number.isSafeInteger(data.ttl_negative_ceiling))
    out.push(text('ttlCeilings',{positive:data.ttl_positive_ceiling,negative:data.ttl_negative_ceiling}));
  return out;
}

export function DnsManagementPage(input) {
  const context=input.context,state=input.state || {},children=[
    node('heading','page',label('title')),text('scopeDescription'),
    text(MODULE==='pzt'?'remoteNotSelected':'dnsNotSelected'),
  ];
  if(MODULE==='pzt') children.push(text('localUnqualified'));
  if(!context || context.state!=='ACTIVE') {
    children.push(text('sessionRequired'));
    return {schema:'pixs.presentation/1.0.0',root:node('section','panel',{},children)};
  }
  const unknown=[];
  for(const id of COMMAND_FORMS) if(action(state,id) && action(state,id).phase==='UNKNOWN') unknown.push(id);
  if(unknown.length) children.push(text('unknownOutcome'));
  const created=action(state,'create_profile');
  const createdRef=created && created.phase==='CONFIRMED' && created.response &&
    created.response.data && scalar(created.response.data.resource_id) ? created.response.data.resource_id : '';
  const lookupValue=state.fields && state.fields.load_profile &&
    typeof state.fields.load_profile.profile_ref==='string' ? state.fields.load_profile.profile_ref : createdRef;
  if(!unknown.length) children.push(queryForm('load_profile','load','get_desired_'+MODULE,
    {resource_id:null},[field('profile_ref','profileRef','text',lookupValue)],
    [{field:'profile_ref',path:['resource_id']}],
    'lookup-'+context.epoch+'-'+(created && created.phase==='CONFIRMED'?created.sequence:0)));
  const load=action(state,'load_profile'),data=responseData(state,'load_profile',context);
  const valid=record(data) && data.schema_version==='1.0.0' && scalar(data.resource_id) &&
    Number.isSafeInteger(data.config_revision) && data.config_revision>=1 &&
    data.config_revision<Number.MAX_SAFE_INTEGER && record(data.configuration) &&
    data.configuration.owner_id===OWNER && data.configuration.config_revision===data.config_revision &&
    (data.business_state==='DECLARED'||data.business_state==='RETIRED') &&
    scalar(data.persistence_state) && scalar(data.retention_state);
  if(load && load.phase==='LOADED' && !valid) {
    children.push(text('observationUnavailable'));
    return {schema:'pixs.presentation/1.0.0',root:node('section','panel',{},children)};
  }
  if(!valid || unknown.includes('create_profile')) {
    if(!unknown.length || unknown.includes('create_profile'))
      children.push(configurationForm('create_profile',null,lookupValue,0,'new-'+context.epoch));
  } else {
    const key=MODULE+'-'+context.epoch+'-'+load.sequence+'-'+data.config_revision;
    children.push(text('desiredRevision',{revision:data.config_revision}));
    children.push(text(data.business_state==='RETIRED'?'desiredRetired':'desiredDeclared'));
    children.push(text('dataLifecycle',{persistence:data.persistence_state,retention:data.retention_state}));
    if(!unknown.length && changedAfterRead(state,data)) children.push(text('reloadNeeded'));
    else {
      if(!unknown.length || unknown.includes('save_profile'))
        children.push(configurationForm('save_profile',data.configuration,data.resource_id,data.config_revision,key,data.business_state));
      if(data.business_state==='DECLARED' && (!unknown.length || unknown.includes('retire_profile'))) children.push(retirementForm(data,key));
      if(MODULE==='dns' && data.business_state==='DECLARED') {
        if(!unknown.length || unknown.includes('declare_name')) children.push(nameForm(data,key,false));
        if(!unknown.length || unknown.includes('retire_name')) children.push(nameForm(data,key,true));
      }
    }
    if(!unknown.length) {
      children.push(observation(state,context,data.resource_id,key));
      if(MODULE==='dns' && data.business_state==='DECLARED') {
        children.push(policyForm(data.resource_id,key));
        for(const item of policyView(state,context,data.resource_id)) children.push(item);
      }
    }
  }
  return {schema:'pixs.presentation/1.0.0',root:node('section','panel',{},children)};
}

export const frontendContributions = [
  {
    "descriptor_version": "1.0.0",
    "owner": "pixs.dns",
    "owner_version": "0.1.0",
    "type": "TRANSLATION",
    "id": "pixs.dns.management.translations",
    "entry": "frontend.mjs",
    "version": "1.0.0",
    "requires": [],
    "scope": "AUTHENTICATED",
    "point": "pixs.shell.translations",
    "point_version": "1.0.0",
    "display_permissions": [],
    "trust": "TRUSTED",
    "mandatory": true,
    "activation_scope": "AUTHENTICATED",
    "payload": {
      "catalog": {
        "en": {
          "pixs.dns.title": "DNS management",
          "pixs.dns.scopeDescription": "Manage the desired configuration for the current context.",
          "pixs.dns.remoteNotSelected": "Remote networking is not selected.",
          "pixs.dns.localUnqualified": "Local executor qualification is unavailable.",
          "pixs.dns.dnsNotSelected": "The active DNS service is not selected.",
          "pixs.dns.sessionRequired": "A verified session is required.",
          "pixs.dns.profileRef": "Profile reference",
          "pixs.dns.load": "Load desired configuration",
          "pixs.dns.create": "Declare a new configuration",
          "pixs.dns.save": "Update desired configuration",
          "pixs.dns.retire": "Retire desired configuration",
          "pixs.dns.reason": "Reason for retirement",
          "pixs.dns.configuration": "Desired configuration",
          "pixs.dns.governance": "Data governance",
          "pixs.dns.secretReferences": "Secret references",
          "pixs.dns.secretOwner": "Owning component",
          "pixs.dns.secretEntry": "Entry reference",
          "pixs.dns.secretSource": "Source reference",
          "pixs.dns.waivers": "Explicit requests for exemptions",
          "pixs.dns.waiveAudit": "Request an audit exemption",
          "pixs.dns.waiveGovernance": "Request a governance exemption",
          "pixs.dns.ipv6Desired": "Desired IPv6 setting",
          "pixs.dns.planRef": "Network plan reference",
          "pixs.dns.budgetRef": "Resource budget reference",
          "pixs.dns.suffix": "Private DNS suffix",
          "pixs.dns.ttlPositive": "Positive TTL ceiling in seconds",
          "pixs.dns.ttlNegative": "Negative TTL ceiling in seconds",
          "pixs.dns.views": "Ordered DNS views",
          "pixs.dns.refreshObservation": "Read observed state",
          "pixs.dns.observationUnknown": "Applied state is unknown; measurements are unavailable.",
          "pixs.dns.observationUnavailable": "The response cannot provide a verified management view.",
          "pixs.dns.reloadNeeded": "The change is confirmed. Reload the desired configuration before another mutation.",
          "pixs.dns.desiredRevision": "Desired configuration, revision {revision}.",
          "pixs.dns.unknownOutcome": "The outcome is unknown. Reconcile this command using its retained request; do not start another mutation.",
          "pixs.dns.dnsName": "Full name",
          "pixs.dns.dnsView": "DNS view",
          "pixs.dns.targetRef": "Desired target reference",
          "pixs.dns.declareName": "Declare the desired name",
          "pixs.dns.retireName": "Retire the desired name",
          "pixs.dns.inspectName": "Read the desired naming policy",
          "pixs.dns.nameDeclared": "The name is declared in the desired configuration. Publication is not verified.",
          "pixs.dns.nameUndeclared": "The name is not declared in this view. This does not establish a DNS answer.",
          "pixs.dns.desiredTarget": "Desired target, not verified: {target}.",
          "pixs.dns.ttlCeilings": "Desired TTL ceilings: positive {positive}, negative {negative} seconds.",
          "pixs.dns.preservedValue": "Preserved value: {value}",
          "pixs.dns.gov_profile_version": "Governance schema version",
          "pixs.dns.gov_data_asset_id": "Data asset reference",
          "pixs.dns.gov_source_of_truth": "Source of truth reference",
          "pixs.dns.gov_confidentiality": "Confidentiality classification",
          "pixs.dns.gov_personal_data": "Personal data classification",
          "pixs.dns.gov_retention_policy": "Retention policy reference",
          "pixs.dns.gov_deletion_policy": "Deletion policy reference",
          "pixs.dns.gov_export_policy": "Export policy reference",
          "pixs.dns.gov_lineage": "Lineage reference",
          "pixs.dns.gov_data_classes": "Data classes",
          "pixs.dns.gov_purpose_refs": "Purpose references",
          "pixs.dns.gov_residency_constraints": "Residency constraints",
          "pixs.dns.gov_authorized_consumers": "Authorized consumer references",
          "pixs.dns.gov_processor_refs": "Processor references",
          "pixs.dns.navigationPlatform": "DNS — Platform management",
          "pixs.dns.navigationTenant": "DNS — Tenant management",
          "pixs.dns.navigationScope": "DNS — Scope management",
          "pixs.dns.desiredDeclared": "Desired configuration is declared.",
          "pixs.dns.desiredRetired": "Desired configuration is retired.",
          "pixs.dns.dataLifecycle": "Persistence: {persistence}; retention: {retention}.",
          "pixs.dns.redeclare": "Declare the desired configuration again"
        },
        "fr": {
          "pixs.dns.title": "Gestion DNS",
          "pixs.dns.scopeDescription": "Gérer la configuration souhaitée dans le contexte courant.",
          "pixs.dns.remoteNotSelected": "Le réseau distant n’est pas sélectionné.",
          "pixs.dns.localUnqualified": "La qualification de l’exécutant local est indisponible.",
          "pixs.dns.dnsNotSelected": "Le service DNS actif n’est pas sélectionné.",
          "pixs.dns.sessionRequired": "Une session vérifiée est requise.",
          "pixs.dns.profileRef": "Référence du profil",
          "pixs.dns.load": "Charger la configuration souhaitée",
          "pixs.dns.create": "Déclarer une nouvelle configuration",
          "pixs.dns.save": "Modifier la configuration souhaitée",
          "pixs.dns.retire": "Retirer la configuration souhaitée",
          "pixs.dns.reason": "Motif du retrait",
          "pixs.dns.configuration": "Configuration souhaitée",
          "pixs.dns.governance": "Gouvernance des données",
          "pixs.dns.secretReferences": "Références de secrets",
          "pixs.dns.secretOwner": "Composant propriétaire",
          "pixs.dns.secretEntry": "Référence d’entrée",
          "pixs.dns.secretSource": "Référence de source",
          "pixs.dns.waivers": "Demandes explicites de dispense",
          "pixs.dns.waiveAudit": "Demander une dispense d’audit",
          "pixs.dns.waiveGovernance": "Demander une dispense de gouvernance",
          "pixs.dns.ipv6Desired": "IPv6 souhaité",
          "pixs.dns.planRef": "Référence du plan réseau",
          "pixs.dns.budgetRef": "Référence du budget de ressources",
          "pixs.dns.suffix": "Suffixe DNS privé",
          "pixs.dns.ttlPositive": "Plafond TTL positif en secondes",
          "pixs.dns.ttlNegative": "Plafond TTL négatif en secondes",
          "pixs.dns.views": "Vues DNS ordonnées",
          "pixs.dns.refreshObservation": "Lire l’état observé",
          "pixs.dns.observationUnknown": "L’état appliqué est inconnu ; aucune mesure n’est disponible.",
          "pixs.dns.observationUnavailable": "La réponse ne permet pas une vue de gestion vérifiée.",
          "pixs.dns.reloadNeeded": "La modification est confirmée. Rechargez la configuration souhaitée avant une autre mutation.",
          "pixs.dns.desiredRevision": "Configuration souhaitée, révision {revision}.",
          "pixs.dns.unknownOutcome": "L’issue est inconnue. Rapprochez cette commande avec sa requête conservée ; n’engagez pas une autre mutation.",
          "pixs.dns.dnsName": "Nom complet",
          "pixs.dns.dnsView": "Vue DNS",
          "pixs.dns.targetRef": "Référence de la cible souhaitée",
          "pixs.dns.declareName": "Déclarer le nom souhaité",
          "pixs.dns.retireName": "Retirer le nom souhaité",
          "pixs.dns.inspectName": "Lire la politique de nommage souhaitée",
          "pixs.dns.nameDeclared": "Le nom est déclaré dans la configuration souhaitée. Sa publication n’est pas vérifiée.",
          "pixs.dns.nameUndeclared": "Le nom n’est pas déclaré dans cette vue. Cela ne constitue pas une réponse DNS.",
          "pixs.dns.desiredTarget": "Cible souhaitée, non vérifiée : {target}.",
          "pixs.dns.ttlCeilings": "Plafonds TTL souhaités : positif {positive}, négatif {negative} secondes.",
          "pixs.dns.preservedValue": "Valeur conservée : {value}",
          "pixs.dns.gov_profile_version": "Version du schéma de gouvernance",
          "pixs.dns.gov_data_asset_id": "Référence de l’actif de données",
          "pixs.dns.gov_source_of_truth": "Référence de la source de vérité",
          "pixs.dns.gov_confidentiality": "Classification de confidentialité",
          "pixs.dns.gov_personal_data": "Classification des données personnelles",
          "pixs.dns.gov_retention_policy": "Référence de la politique de rétention",
          "pixs.dns.gov_deletion_policy": "Référence de la politique de suppression",
          "pixs.dns.gov_export_policy": "Référence de la politique d’export",
          "pixs.dns.gov_lineage": "Référence de traçabilité",
          "pixs.dns.gov_data_classes": "Classes de données",
          "pixs.dns.gov_purpose_refs": "Références des finalités",
          "pixs.dns.gov_residency_constraints": "Contraintes de résidence",
          "pixs.dns.gov_authorized_consumers": "Références des consommateurs autorisés",
          "pixs.dns.gov_processor_refs": "Références des sous-traitants",
          "pixs.dns.navigationPlatform": "DNS — Gestion de la plateforme",
          "pixs.dns.navigationTenant": "DNS — Gestion du tenant",
          "pixs.dns.navigationScope": "DNS — Gestion du périmètre",
          "pixs.dns.desiredDeclared": "Configuration souhaitée déclarée.",
          "pixs.dns.desiredRetired": "Configuration souhaitée retirée.",
          "pixs.dns.dataLifecycle": "Persistance : {persistence} ; conservation : {retention}.",
          "pixs.dns.redeclare": "Déclarer à nouveau la configuration souhaitée"
        }
      }
    }
  },
  {
    "descriptor_version": "1.0.0",
    "owner": "pixs.dns",
    "owner_version": "0.1.0",
    "type": "PAGE",
    "id": "pixs.dns.management.page",
    "entry": "frontend.mjs",
    "version": "1.0.0",
    "requires": [
      "pixs.dns.management.translations ==1.0.0"
    ],
    "scope": "AUTHENTICATED",
    "point": "pixs.shell.pages",
    "point_version": "1.0.0",
    "display_permissions": [],
    "trust": "TRUSTED",
    "mandatory": true,
    "activation_scope": "AUTHENTICATED",
    "payload": {
      "export": "DnsManagementPage"
    }
  },
  {
    "descriptor_version": "1.0.0",
    "owner": "pixs.dns",
    "owner_version": "0.1.0",
    "type": "ROUTE",
    "id": "pixs.dns.management.route.platform",
    "entry": "frontend.mjs",
    "version": "1.0.0",
    "requires": [
      "pixs.dns.management.page ==1.0.0"
    ],
    "scope": "PLATFORM_SCOPED",
    "point": "pixs.shell.routes",
    "point_version": "1.0.0",
    "display_permissions": [],
    "trust": "TRUSTED",
    "mandatory": true,
    "activation_scope": "PLATFORM_SCOPED",
    "payload": {
      "path": "/platform/dns",
      "mode": "CSR",
      "page": "DnsManagementPage"
    }
  },
  {
    "descriptor_version": "1.0.0",
    "owner": "pixs.dns",
    "owner_version": "0.1.0",
    "type": "NAVIGATION",
    "id": "pixs.dns.management.navigation.platform",
    "entry": "frontend.mjs",
    "version": "1.0.0",
    "requires": [
      "pixs.dns.management.route.platform ==1.0.0",
      "pixs.dns.management.translations ==1.0.0"
    ],
    "scope": "PLATFORM_SCOPED",
    "point": "pixs.shell.navigation-items",
    "point_version": "1.0.0",
    "display_permissions": [],
    "trust": "TRUSTED",
    "mandatory": false,
    "activation_scope": "PLATFORM_SCOPED",
    "payload": {
      "route": "/platform/dns",
      "labelKey": "pixs.dns.navigationPlatform"
    }
  },
  {
    "descriptor_version": "1.0.0",
    "owner": "pixs.dns",
    "owner_version": "0.1.0",
    "type": "ROUTE",
    "id": "pixs.dns.management.route.tenant",
    "entry": "frontend.mjs",
    "version": "1.0.0",
    "requires": [
      "pixs.dns.management.page ==1.0.0"
    ],
    "scope": "TENANT_SCOPED",
    "point": "pixs.shell.routes",
    "point_version": "1.0.0",
    "display_permissions": [],
    "trust": "TRUSTED",
    "mandatory": true,
    "activation_scope": "TENANT_SCOPED",
    "payload": {
      "path": "/tenants/{tenant_id}/dns",
      "mode": "CSR",
      "page": "DnsManagementPage"
    }
  },
  {
    "descriptor_version": "1.0.0",
    "owner": "pixs.dns",
    "owner_version": "0.1.0",
    "type": "NAVIGATION",
    "id": "pixs.dns.management.navigation.tenant",
    "entry": "frontend.mjs",
    "version": "1.0.0",
    "requires": [
      "pixs.dns.management.route.tenant ==1.0.0",
      "pixs.dns.management.translations ==1.0.0"
    ],
    "scope": "TENANT_SCOPED",
    "point": "pixs.shell.navigation-items",
    "point_version": "1.0.0",
    "display_permissions": [],
    "trust": "TRUSTED",
    "mandatory": false,
    "activation_scope": "TENANT_SCOPED",
    "payload": {
      "route": "/tenants/{tenant_id}/dns",
      "labelKey": "pixs.dns.navigationTenant"
    }
  },
  {
    "descriptor_version": "1.0.0",
    "owner": "pixs.dns",
    "owner_version": "0.1.0",
    "type": "ROUTE",
    "id": "pixs.dns.management.route.scope",
    "entry": "frontend.mjs",
    "version": "1.0.0",
    "requires": [
      "pixs.dns.management.page ==1.0.0"
    ],
    "scope": "TENANT_SCOPED",
    "point": "pixs.shell.routes",
    "point_version": "1.0.0",
    "display_permissions": [],
    "trust": "TRUSTED",
    "mandatory": true,
    "activation_scope": "TENANT_SCOPED",
    "payload": {
      "path": "/tenants/{tenant_id}/scopes/{scope_id}/dns",
      "mode": "CSR",
      "page": "DnsManagementPage"
    }
  },
  {
    "descriptor_version": "1.0.0",
    "owner": "pixs.dns",
    "owner_version": "0.1.0",
    "type": "NAVIGATION",
    "id": "pixs.dns.management.navigation.scope",
    "entry": "frontend.mjs",
    "version": "1.0.0",
    "requires": [
      "pixs.dns.management.route.scope ==1.0.0",
      "pixs.dns.management.translations ==1.0.0"
    ],
    "scope": "TENANT_SCOPED",
    "point": "pixs.shell.navigation-items",
    "point_version": "1.0.0",
    "display_permissions": [],
    "trust": "TRUSTED",
    "mandatory": false,
    "activation_scope": "TENANT_SCOPED",
    "payload": {
      "route": "/tenants/{tenant_id}/scopes/{scope_id}/dns",
      "labelKey": "pixs.dns.navigationScope"
    }
  }
];
