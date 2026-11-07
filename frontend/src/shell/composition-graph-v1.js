// Graphe pur de contributions ; authenticité des entrées portée par le build.
// Pur navigateur : importe uniquement descripteur public 2.1.
// Ne certifie pas authenticité des entrées ; valide structures/versions/quotas.
import { validateCompositionDescriptor, createShellExtensionPoints } from './composition-descriptor-v1.js';

export const GRAPH_VERSION = '1.0.0';
export const GRAPH_SCHEMA_PREFLIGHT = 'pixs.frontend.graph-preflight/1.0.0';
export const GRAPH_SCHEMA = 'pixs.frontend.contribution-graph/1.0.0';
export const POLICY_SCHEMA = 'pixs.frontend.policy/1.0.0';
export const FACTS_SCHEMA = 'pixs.frontend.requirement-facts/1.0.0';
export const RENDERER_CONTRACT = 'pixs.presentation/1.0.0';
export const RENDERER_ADAPTER = 'pixs.dom/v1';
export const PROTECTED_PATHS = Object.freeze([
  '/', '/login', '/platform',
  '/tenants/{tenant_id}',
  '/tenants/{tenant_id}/scopes/{scope_id}',
]);
export const GRAPH_CODES = Object.freeze([
  "GRAPH_CAPTURE_INVALID",
  "GRAPH_CATEGORY_MISMATCH",
  "GRAPH_COLLISION_CATALOG",
  "GRAPH_COLLISION_NAV",
  "GRAPH_COLLISION_PERMISSION",
  "GRAPH_COLLISION_POINT",
  "GRAPH_COLLISION_ROUTE",
  "GRAPH_COLLISION_SLOT",
  "GRAPH_CYCLE_CONTRIBUTION",
  "GRAPH_DEPENDENCY_UNAVAILABLE",
  "GRAPH_DESCRIPTOR_INVALID",
  "GRAPH_DESCRIPTOR_UNDECLARED",
  "GRAPH_DUPLICATE_CONTRIBUTION",
  "GRAPH_ENVELOPE_INVALID",
  "GRAPH_EXPORT_INVALID",
  "GRAPH_FACTS_INVALID",
  "GRAPH_GUARANTEES_INVALID",
  "GRAPH_INVARIANT_FAILED",
  "GRAPH_LIMITS_INVALID",
  "GRAPH_NAMESPACE_RESERVED",
  "GRAPH_OWNER_UNAVAILABLE",
  "GRAPH_POINT_DEPENDENCY_UNDECLARED",
  "GRAPH_POINT_OWNER_UNAVAILABLE",
  "GRAPH_POINT_UNKNOWN",
  "GRAPH_POLICY_INVALID",
  "GRAPH_RENDERER_REFUSED",
  "GRAPH_REQUIREMENT_UNSATISFIED",
  "GRAPH_SCOPE_MISMATCH",
  "GRAPH_TRUST_INVALID"
]);
export class GraphError extends Error {
  constructor(code, options){ super(code, options); this.name='GraphError'; this.code=code; }
}
function fail(code, cause){
  if (cause === undefined) throw new GraphError(code);
  throw new GraphError(code, { cause });
}
function safeInt(v){
  if (typeof v !== 'number' || !Number.isSafeInteger(v) || v <= 0) fail('GRAPH_LIMITS_INVALID');
  return v;
}
function isPlainRecord(v){
  if (v === null || typeof v !== 'object' || Array.isArray(v)) return false;
  const p = Object.getPrototypeOf(v); return p === Object.prototype || p === null;
}
function closedRecord(v, required, code){
  if (!isPlainRecord(v)) fail(code);
  const keys = Reflect.ownKeys(v);
  if (keys.length !== required.length) fail(code);
  for (const k of keys){
    if (typeof k !== 'string' || !required.includes(k)) fail(code);
    const d = Object.getOwnPropertyDescriptor(v, k);
    if (!d || !Object.hasOwn(d, 'value')) fail(code);
  }
  for (const k of required) if (!Object.hasOwn(v, k)) fail(code);
  return v;
}
function denseArray(v, max, code){
  if (!Array.isArray(v) || Object.getPrototypeOf(v) !== Array.prototype || v.length > max) fail(code);
  if (Reflect.ownKeys(v).length !== v.length + 1) fail(code);
  for (let i = 0; i < v.length; i += 1){
    const d = Object.getOwnPropertyDescriptor(v, String(i));
    if (!d || !Object.hasOwn(d, 'value')) fail(code);
  }
  return v;
}
function openRecord(v, max, code){
  if (!isPlainRecord(v)) fail(code);
  const keys = Reflect.ownKeys(v);
  if (keys.length > max) fail(code);
  for (const k of keys){
    const d = Object.getOwnPropertyDescriptor(v, k);
    if (typeof k !== 'string' || !d || !Object.hasOwn(d, 'value')) fail(code);
  }
  return v;
}
function metaText(v, max, code){
  if (typeof v !== 'string' || v.length === 0 || v.length > max) fail(code || 'GRAPH_ENVELOPE_INVALID');
  for (let i = 0; i < v.length; i++){
    const u = v.charCodeAt(i);
    if (u < 32 || u === 127) fail(code || 'GRAPH_ENVELOPE_INVALID');
    if (u >= 0xD800 && u <= 0xDBFF){
      const n = v.charCodeAt(i + 1);
      if (!(n >= 0xDC00 && n <= 0xDFFF)) fail(code || 'GRAPH_ENVELOPE_INVALID');
      i++;
    } else if (u >= 0xDC00 && u <= 0xDFFF) fail(code || 'GRAPH_ENVELOPE_INVALID');
  }
  return v;
}
function deepFreeze(value){
  const seen = new Set(); const stack = [value];
  while (stack.length){
    const item = stack.pop();
    if (item === null || typeof item !== 'object' || seen.has(item)) continue;
    seen.add(item);
    for (const key of Reflect.ownKeys(item)){
      const d = Object.getOwnPropertyDescriptor(item, key);
      if (!d || !Object.hasOwn(d, 'value')) fail('GRAPH_ENVELOPE_INVALID');
      if (d.value !== null && typeof d.value === 'object') stack.push(d.value);
    }
    Object.freeze(item);
  }
  return value;
}
function snapshot(value, budget){
  const holder = {}; const stack = [{ value, parent: holder, key: 'value' }]; const seen = new Set();
  while (stack.length){
    const frame = stack.pop();
    if (frame.finish){ Object.freeze(frame.finish); continue; }
    if (--budget.left < 0) fail('GRAPH_LIMITS_INVALID');
    const source = frame.value;
    if (source === null || typeof source === 'string' || typeof source === 'boolean'
        || typeof source === 'number' && Number.isFinite(source)){
      Object.defineProperty(frame.parent, frame.key, { value: source, enumerable: true });
      continue;
    }
    if (typeof source !== 'object' || seen.has(source)) fail('GRAPH_ENVELOPE_INVALID');
    seen.add(source);
    const array = Array.isArray(source);
    if (array) denseArray(source, Number.MAX_SAFE_INTEGER, 'GRAPH_ENVELOPE_INVALID');
    else openRecord(source, Number.MAX_SAFE_INTEGER, 'GRAPH_ENVELOPE_INVALID');
    if ((array ? source.length : Reflect.ownKeys(source).length) > budget.left) fail('GRAPH_LIMITS_INVALID');
    const target = array ? new Array(source.length) : {};
    Object.defineProperty(frame.parent, frame.key, { value: target, enumerable: true });
    stack.push({ finish: target });
    const keys = array ? Array.from({ length: source.length }, (_, i) => String(i)) : Reflect.ownKeys(source);
    for (let i = keys.length - 1; i >= 0; i -= 1){
      const key = keys[i];
      const d = Object.getOwnPropertyDescriptor(source, key);
      stack.push({ value: d.value, parent: target, key });
    }
  }
  return holder.value;
}
function validateLimits(l){
  closedRecord(l, ['maxContributions','maxFacts','maxEdges','maxInputNodes','descriptorLimits'], 'GRAPH_LIMITS_INVALID');
  safeInt(l.maxContributions); safeInt(l.maxFacts); safeInt(l.maxEdges); safeInt(l.maxInputNodes);
  closedRecord(l.descriptorLimits,
    ['maxTextLength','maxRequires','maxPermissions','maxPoints','maxLocales','maxCatalogKeys'],
    'GRAPH_LIMITS_INVALID');
  for (const k of Object.keys(l.descriptorLimits)) safeInt(l.descriptorLimits[k]);
  return l;
}

const TYPES=Object.freeze(['ROUTE','PAGE','NAVIGATION','COMPONENT','FORM','TRANSLATION','UI_PERMISSION','UI_SLOT']);
const POINT=/^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+$/;
const keyOf=(owner,id)=>JSON.stringify([owner,id]);
const cmp=(a,b)=>a<b?-1:a>b?1:0;
function namespace(id,owner,official){
  return (id===owner||id.startsWith(owner+'.'))&&(!id.startsWith('pixs.')||official.has(owner));
}
function validatePolicy(p,bounds){
  closedRecord(p,['schema','imports','modularPoints','mergeModes','admission','locales','renderer'],'GRAPH_POLICY_INVALID');
  if(p.schema!==POLICY_SCHEMA)fail('GRAPH_POLICY_INVALID');
  closedRecord(p.imports,['shellFacades','foreignFacades'],'GRAPH_POLICY_INVALID');
  denseArray(p.modularPoints,bounds.descriptorLimits.maxPoints,'GRAPH_POLICY_INVALID');
  openRecord(p.mergeModes,bounds.descriptorLimits.maxPoints,'GRAPH_POLICY_INVALID');
  denseArray(p.admission,bounds.maxContributions,'GRAPH_POLICY_INVALID');
  denseArray(p.locales,2,'GRAPH_POLICY_INVALID');
  if(p.locales.length!==2||p.locales[0]!=='en'||p.locales[1]!=='fr')fail('GRAPH_POLICY_INVALID');
  closedRecord(p.renderer,['contract','adapter'],'GRAPH_POLICY_INVALID');
  if(p.renderer.contract!==RENDERER_CONTRACT||p.renderer.adapter!==RENDERER_ADAPTER)fail('GRAPH_RENDERER_REFUSED');
  const points=new Set(), admissions=new Set();
  for(const mp of p.modularPoints){
    closedRecord(mp,['id','owner_version','provider_id','definition'],'GRAPH_POLICY_INVALID');
    metaText(mp.provider_id,bounds.descriptorLimits.maxTextLength,'GRAPH_POLICY_INVALID');
    metaText(mp.id,bounds.descriptorLimits.maxTextLength,'GRAPH_POLICY_INVALID');
    metaText(mp.owner_version,bounds.descriptorLimits.maxTextLength,'GRAPH_POLICY_INVALID');
    if(!POINT.test(mp.id)||points.has(mp.id))fail('GRAPH_POLICY_INVALID');
    points.add(mp.id);
    const d=mp.definition;
    closedRecord(d,['owner','category','version','schema','guarantees'],'GRAPH_POLICY_INVALID');
    metaText(d.owner,bounds.descriptorLimits.maxTextLength,'GRAPH_POLICY_INVALID');
    if(!TYPES.includes(d.category)||d.version!=='1.0.0'||d.schema!=='pixs.frontend.composition-descriptor/1.0.0')fail('GRAPH_POLICY_INVALID');
    denseArray(d.guarantees,2,'GRAPH_POLICY_INVALID');
    if(d.guarantees.length!==2||new Set(d.guarantees).size!==2||!d.guarantees.includes('DATA_ONLY_DESCRIPTOR')||!d.guarantees.includes('EXPLICIT_ENTRY_EXPORTS'))fail('GRAPH_POLICY_INVALID');
  }
  for(const a of p.admission){
    closedRecord(a,['owner','id','mandatory'],'GRAPH_POLICY_INVALID');
    metaText(a.owner,bounds.descriptorLimits.maxTextLength,'GRAPH_POLICY_INVALID');
    metaText(a.id,bounds.descriptorLimits.maxTextLength,'GRAPH_POLICY_INVALID');
    if(!POINT.test(a.id)||typeof a.mandatory!=='boolean'||admissions.has(keyOf(a.owner,a.id)))fail('GRAPH_POLICY_INVALID');
    admissions.add(keyOf(a.owner,a.id));
  }
  for(const [id,mode] of Object.entries(p.mergeModes))if(!POINT.test(id)||!['REJECT','APPEND'].includes(mode))fail('GRAPH_POLICY_INVALID');
  return p;
}
function routeSegments(path){return path==='/'?[]:path.slice(1).split('/');}
function isParam(s){return /^\{[a-z][a-z0-9_]*\}$/.test(s);}
function repeatedParams(path){
  const params=routeSegments(path).filter(isParam);
  return new Set(params).size!==params.length;
}
function routesIntersect(a,b){
  const aa=routeSegments(a),bb=routeSegments(b);
  return aa.length===bb.length&&aa.every((x,i)=>isParam(x)||isParam(bb[i])||x===bb[i]);
}
function catalogParams(text){
  const result=new Set();
  for(let i=0;i<text.length;i++){
    if(text[i]==='}')fail('GRAPH_COLLISION_CATALOG');
    if(text[i]!=='{')continue;
    const end=text.indexOf('}',i+1);
    if(end<0)fail('GRAPH_COLLISION_CATALOG');
    const name=text.slice(i+1,end);
    if(!/^[A-Za-z][A-Za-z0-9_]*$/.test(name))fail('GRAPH_COLLISION_CATALOG');
    result.add(name);i=end;
  }
  return result;
}
function diagnosticSort(a,b){return cmp(a.owner,b.owner)||cmp(a.id,b.id)||cmp(a.code,b.code)||cmp(a.cause??'',b.cause??'');}
function reporter(admission,diagnostics,refused){
  let blocked=false;
  const seen=new Set(diagnostics.map(d=>JSON.stringify(d)));
  return {
    report(owner,id,code,cause=null,forceMandatory=false){
      const key=keyOf(owner,id);
      if(refused)refused.add(key);
      const d={owner,id,code,cause},dk=JSON.stringify(d);
      if(!seen.has(dk)){seen.add(dk);diagnostics.push(d);}
      if(forceMandatory||admission.get(key)?.mandatory===true)blocked=true;
    },
    isBlocked(){return blocked;},
  };
}
function validateComponentContext(envelope,bounds){
  closedRecord(envelope,['schema','capture','plan','ignored_attestation_indices','build_limits','context_checksum','declared_owner_ids'],'GRAPH_ENVELOPE_INVALID');
  if(envelope.schema!=='pixs.frontend.plan-envelope/1.0.0')fail('GRAPH_ENVELOPE_INVALID');
  const cap=envelope.capture,plan=envelope.plan;
  closedRecord(cap,['schema','selection_sha256','environment','provenance_reference','context_fingerprint','composition','owners','errors'],'GRAPH_ENVELOPE_INVALID');
  closedRecord(plan,['schema','order','edges','facets','diagnostics','warnings','evaluation_scope','unevaluated_dimensions','globally_compatible','sources_sha256'],'GRAPH_ENVELOPE_INVALID');
  if(cap.schema!=='pixs.frontend.selection/1.0.0'||plan.schema!=='pixs.frontend.build-plan/1'||plan.globally_compatible!==false||!['DEVELOPMENT','PRODUCTION'].includes(cap.environment))fail('GRAPH_ENVELOPE_INVALID');
  closedRecord(cap.composition,['official_ids','required_ids','configured_providers','attestations'],'GRAPH_ENVELOPE_INVALID');
  denseArray(cap.composition.official_ids,bounds.maxContributions,'GRAPH_ENVELOPE_INVALID');
  denseArray(cap.owners,bounds.maxContributions,'GRAPH_ENVELOPE_INVALID');
  denseArray(cap.errors,bounds.maxContributions,'GRAPH_ENVELOPE_INVALID');
  denseArray(envelope.declared_owner_ids,bounds.maxContributions,'GRAPH_ENVELOPE_INVALID');
  denseArray(plan.order,bounds.maxContributions,'GRAPH_ENVELOPE_INVALID');
  denseArray(plan.edges,bounds.maxEdges,'GRAPH_ENVELOPE_INVALID');
  denseArray(plan.facets,bounds.maxContributions,'GRAPH_ENVELOPE_INVALID');
  for(const id of [...cap.composition.official_ids,...envelope.declared_owner_ids,...plan.order])metaText(id,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
  if(new Set(envelope.declared_owner_ids).size!==envelope.declared_owner_ids.length||new Set(plan.order).size!==plan.order.length)fail('GRAPH_ENVELOPE_INVALID');
  const owners=new Map(),files=new Map(),indices=new Set();
  for(const o of cap.owners){
    closedRecord(o,['index','owner','owner_version','root','trust','manifest','sources'],'GRAPH_CAPTURE_INVALID');
    for(const v of [o.owner,o.owner_version,o.root])metaText(v,bounds.descriptorLimits.maxTextLength,'GRAPH_CAPTURE_INVALID');
    if(!Number.isSafeInteger(o.index)||o.index<0||envelope.declared_owner_ids[o.index]!==o.owner||owners.has(o.owner)||indices.has(o.index)||!['PLATFORM','TRUSTED','SANDBOXED','DEVELOPMENT'].includes(o.trust))fail('GRAPH_CAPTURE_INVALID');
    indices.add(o.index);owners.set(o.owner,o);
    denseArray(o.sources,bounds.maxInputNodes,'GRAPH_CAPTURE_INVALID');
    for(const f of [o.manifest,...o.sources]){
      closedRecord(f,['owner_index','path','sha256','size','data_b64'],'GRAPH_CAPTURE_INVALID');
      metaText(f.path,bounds.descriptorLimits.maxTextLength,'GRAPH_CAPTURE_INVALID');
      if(f.owner_index!==o.index||typeof f.sha256!=='string'||!/^[a-f0-9]{64}$/.test(f.sha256)||files.has(f.path)||!f.path.startsWith(o.root+'/'))fail('GRAPH_CAPTURE_INVALID');
      files.set(f.path,{owner:o.owner,hash:f.sha256});
    }
    if(o.manifest.path!==o.root+'/component.toml')fail('GRAPH_CAPTURE_INVALID');
  }
  if(plan.order.length!==owners.size||plan.order.some(id=>!owners.has(id)))fail('GRAPH_CAPTURE_INVALID');
  const rank=new Map(plan.order.map((id,i)=>[id,i])),edgeKeys=new Set();
  for(const e of plan.edges){
    denseArray(e,2,'GRAPH_ENVELOPE_INVALID');
    if(e.length!==2||!rank.has(e[0])||!rank.has(e[1])||rank.get(e[1])>=rank.get(e[0])||edgeKeys.has(JSON.stringify(e)))fail('GRAPH_ENVELOPE_INVALID');
    edgeKeys.add(JSON.stringify(e));
  }
  const failed=new Map();
  for(const e of cap.errors){
    closedRecord(e,['owner_index','owner','path','code','observed_sha256'],'GRAPH_CAPTURE_INVALID');
    if(!Number.isSafeInteger(e.owner_index)||e.owner_index<0||e.owner_index>=envelope.declared_owner_ids.length||indices.has(e.owner_index))fail('GRAPH_CAPTURE_INVALID');
    metaText(e.code,bounds.descriptorLimits.maxTextLength,'GRAPH_CAPTURE_INVALID');
    const owner=envelope.declared_owner_ids[e.owner_index];
    failed.set(owner,e.code);
  }
  if(new Set([...indices,...cap.errors.map(e=>e.owner_index)]).size!==envelope.declared_owner_ids.length)fail('GRAPH_CAPTURE_INVALID');
  const official=new Set(cap.composition.official_ids);
  const canUsePoint=(from,to)=>{
    if(from===to)return true;
    const pending=[from],seen=new Set();
    while(pending.length){
      const owner=pending.pop();
      if(owner===to)return true;
      if(seen.has(owner))continue;
      seen.add(owner);
      for(const [a,b] of plan.edges)if(a===owner)pending.push(b);
    }
    return false;
  };
  return {cap,plan,owners,files,failed,official,canUsePoint};
}
export function preflightContributions(envelope,imports,policy,limits){
  const bounds=validateLimits(limits),budget={left:bounds.maxInputNodes};
  envelope=snapshot(envelope,budget);imports=snapshot(imports,budget);policy=snapshot(policy,budget);
  const pol=validatePolicy(policy,bounds),ctx=validateComponentContext(envelope,bounds);
  const {cap,plan,owners,files,failed,official,canUsePoint}=ctx;
  closedRecord(imports,['modules','resolutions','diagnostics'],'GRAPH_ENVELOPE_INVALID');
  denseArray(imports.modules,bounds.maxInputNodes,'GRAPH_ENVELOPE_INVALID');
  denseArray(imports.resolutions,bounds.maxInputNodes,'GRAPH_ENVELOPE_INVALID');
  denseArray(imports.diagnostics,bounds.maxInputNodes,'GRAPH_ENVELOPE_INVALID');
  for(const d of imports.diagnostics){
    closedRecord(d,['owner','path','code'],'GRAPH_ENVELOPE_INVALID');
    if(!owners.has(d.owner))fail('GRAPH_CAPTURE_INVALID');
    metaText(d.code,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
    if(!files.has(d.path)||files.get(d.path).owner!==d.owner)fail('GRAPH_CAPTURE_INVALID');
    failed.set(d.owner,d.code);
  }
  const facetGroups=new Map();
  for(const f of plan.facets){
    closedRecord(f,['owner','owner_version','type','id','entry','version','requires','scope'],'GRAPH_ENVELOPE_INVALID');
    for(const v of [f.owner,f.owner_version,f.id,f.entry,f.version,f.scope])metaText(v,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
    denseArray(f.requires,bounds.descriptorLimits.maxRequires,'GRAPH_ENVELOPE_INVALID');
    for(const r of f.requires)metaText(r,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
    if(!owners.has(f.owner)||owners.get(f.owner).owner_version!==f.owner_version||!TYPES.includes(f.type))fail('GRAPH_CAPTURE_INVALID');
    const key=keyOf(f.owner,f.id);
    if(!facetGroups.has(key))facetGroups.set(key,[]);
    facetGroups.get(key).push(f);
  }
  const adm=new Map(pol.admission.map(a=>[keyOf(a.owner,a.id),a]));
  for(const key of facetGroups.keys())if(!adm.has(key))fail('GRAPH_POLICY_INVALID');
  for(const a of pol.admission)if(!facetGroups.has(keyOf(a.owner,a.id))&&!failed.has(a.owner))fail('GRAPH_POLICY_INVALID');
  const diagnostics=[],report=reporter(adm,diagnostics);
  for(const a of pol.admission)if(failed.has(a.owner))report.report(a.owner,a.id,'GRAPH_OWNER_UNAVAILABLE',failed.get(a.owner));
  const shell=createShellExtensionPoints(),pointEntries=Object.entries(shell.points),pointProviders={};
  const pointOwner=new Map(pointEntries.map(([id,d])=>[id,d.owner]));
  for(const mp of pol.modularPoints){
    const owner=owners.get(mp.definition.owner);
    const providerKey=keyOf(mp.definition.owner,mp.provider_id);
    if((!owner&&!failed.has(mp.definition.owner))||(owner&&owner.owner_version!==mp.owner_version)||pointOwner.has(mp.id)||!namespace(mp.id,mp.definition.owner,official)||!adm.has(providerKey))fail('GRAPH_POLICY_INVALID');
    pointEntries.push([mp.id,mp.definition]);pointOwner.set(mp.id,mp.definition.owner);
    Object.defineProperty(pointProviders,mp.id,{value:{owner:mp.definition.owner,id:mp.provider_id},enumerable:true});
  }
  if(pointEntries.length>bounds.descriptorLimits.maxPoints)fail('GRAPH_LIMITS_INVALID');
  const registry={metadata:shell.metadata,points:Object.fromEntries(pointEntries)};
  const modeKeys=Object.keys(pol.mergeModes);
  if(modeKeys.length!==pointEntries.length||modeKeys.some(id=>!pointOwner.has(id)))fail('GRAPH_POLICY_INVALID');
  const modules=new Map(),byDescriptor=new Map(),invalidOwners=new Set();
  for(const m of imports.modules){
    closedRecord(m,['owner','owner_version','root','file','text','hash','isEntry','descriptors','exportedNames','imports'],'GRAPH_ENVELOPE_INVALID');
    const owner=owners.get(m.owner),file=files.get(m.file);
    if(!owner||!file||file.owner!==m.owner||file.hash!==m.hash||owner.owner_version!==m.owner_version||owner.root!==m.root||typeof m.isEntry!=='boolean'||typeof m.text!=='string'||modules.has(m.file))fail('GRAPH_CAPTURE_INVALID');
    denseArray(m.descriptors,bounds.maxContributions,'GRAPH_ENVELOPE_INVALID');
    denseArray(m.exportedNames,bounds.maxInputNodes,'GRAPH_ENVELOPE_INVALID');
    modules.set(m.file,m);
    if(!m.isEntry&&m.descriptors.length)fail('GRAPH_CAPTURE_INVALID');
    for(const d of m.descriptors){
      const validIdentity=isPlainRecord(d)&&typeof d.owner==='string'&&typeof d.id==='string'&&typeof d.entry==='string';
      const key=validIdentity?keyOf(d.owner,d.id):null,group=key===null?null:facetGroups.get(key);
      if(!group||d.owner!==m.owner||!group.some(f=>owner.root+'/'+f.entry===m.file)){
        invalidOwners.add(m.owner);continue;
      }
      if(!byDescriptor.has(key))byDescriptor.set(key,[]);
      byDescriptor.get(key).push({descriptor:d,module:m});
    }
  }
  for(const a of pol.admission)if(invalidOwners.has(a.owner))report.report(a.owner,a.id,'GRAPH_DESCRIPTOR_UNDECLARED');
  const contributions=[],facets=[];
  for(const [key,group] of facetGroups){
    const f=group[0],a=adm.get(key),owner=owners.get(f.owner);
    if(failed.has(f.owner)||invalidOwners.has(f.owner))continue;
    const occurrences=byDescriptor.get(key)??[];
    if(group.length!==1||occurrences.length!==1){report.report(f.owner,f.id,'GRAPH_DUPLICATE_CONTRIBUTION',null,occurrences.some(o=>o.descriptor.mandatory===true));continue;}
    const {descriptor:d,module:m}=occurrences[0];
    const forceMandatory=d.mandatory===true;
    if(!m.isEntry||m.file!==owner.root+'/'+f.entry){report.report(f.owner,f.id,'GRAPH_CAPTURE_INVALID',null,forceMandatory);continue;}
    if(!namespace(f.id,f.owner,official)){report.report(f.owner,f.id,'GRAPH_NAMESPACE_RESERVED',null,forceMandatory);continue;}
    if(d.mandatory!==a.mandatory){report.report(f.owner,f.id,'GRAPH_POLICY_INVALID',null,forceMandatory);continue;}
    if(d.trust!==owner.trust||d.trust==='SANDBOXED'||cap.environment==='PRODUCTION'&&d.trust==='DEVELOPMENT'){report.report(f.owner,f.id,'GRAPH_TRUST_INVALID');continue;}
    if(!pointOwner.has(d.point)){report.report(f.owner,f.id,'GRAPH_POINT_UNKNOWN');continue;}
    const targetOwner=pointOwner.get(d.point);
    if(!Object.hasOwn(shell.points,d.point)&&(failed.has(targetOwner)||invalidOwners.has(targetOwner)||!canUsePoint(f.owner,targetOwner))){report.report(f.owner,f.id,'GRAPH_POINT_OWNER_UNAVAILABLE');continue;}
    let validated;
    try{validated=validateCompositionDescriptor(d,{facet:f,extensionPoints:registry,limits:bounds.descriptorLimits});}
    catch(error){
      if(error?.name!=='CompositionDescriptorError')throw error;
      report.report(f.owner,f.id,'GRAPH_DESCRIPTOR_INVALID',error.code,forceMandatory);continue;
    }
    const exportName=d.type==='ROUTE'?d.payload.page:['PAGE','COMPONENT','FORM','UI_SLOT'].includes(d.type)?d.payload.export:null;
    if(exportName!==null&&!m.exportedNames.some(e=>isPlainRecord(e)&&e.name===exportName&&e.callable===true&&e.from==='local')){report.report(f.owner,f.id,'GRAPH_EXPORT_INVALID');continue;}
    if(d.type==='ROUTE'&&repeatedParams(d.payload.path)||d.type==='NAVIGATION'&&repeatedParams(d.payload.route)){report.report(f.owner,f.id,'GRAPH_COLLISION_ROUTE');continue;}
    if(d.type==='TRANSLATION'&&Object.keys(d.payload.catalog).some(loc=>!pol.locales.includes(loc))){report.report(f.owner,f.id,'GRAPH_COLLISION_CATALOG');continue;}
    if(d.type==='UI_PERMISSION'&&!namespace(d.payload.key,d.owner,official)){report.report(f.owner,f.id,'GRAPH_NAMESPACE_RESERVED');continue;}
    contributions.push(validated);facets.push(f);
  }
  let changed=true;
  const accepted=new Set(contributions.map(c=>keyOf(c.owner,c.id)));
  while(changed){changed=false;for(const c of contributions){
    const provider=pointProviders[c.point],key=keyOf(c.owner,c.id);
    if(accepted.has(key)&&provider&&!accepted.has(keyOf(provider.owner,provider.id))){accepted.delete(key);changed=true;report.report(c.owner,c.id,'GRAPH_POINT_OWNER_UNAVAILABLE');}
  }}
  diagnostics.sort(diagnosticSort);
  return deepFreeze({
    schema:GRAPH_SCHEMA_PREFLIGHT,componentOrder:[...plan.order],componentEdges:plan.edges.map(e=>[...e]),
    facets:facets.filter(f=>accepted.has(keyOf(f.owner,f.id))),contributions:contributions.filter(c=>accepted.has(keyOf(c.owner,c.id))),admission:pol.admission,points:registry,pointProviders,mergeModes:pol.mergeModes,
    locales:pol.locales,diagnostics,blocked:report.isBlocked(),
  });
}

function checkedPreflight(p,bounds){
  closedRecord(p,['schema','componentOrder','componentEdges','facets','contributions','admission','points','pointProviders','mergeModes','locales','diagnostics','blocked'],'GRAPH_ENVELOPE_INVALID');
  if(p.schema!==GRAPH_SCHEMA_PREFLIGHT||typeof p.blocked!=='boolean')fail('GRAPH_ENVELOPE_INVALID');
  for(const key of ['contributions','facets','admission','componentOrder'])denseArray(p[key],bounds.maxContributions,'GRAPH_ENVELOPE_INVALID');
  denseArray(p.locales,2,'GRAPH_ENVELOPE_INVALID');
  if(p.locales.length!==2||p.locales[0]!=='en'||p.locales[1]!=='fr')fail('GRAPH_ENVELOPE_INVALID');
  denseArray(p.componentEdges,bounds.maxEdges,'GRAPH_ENVELOPE_INVALID');
  denseArray(p.diagnostics,bounds.maxInputNodes,'GRAPH_ENVELOPE_INVALID');
  const rank=new Map();
  p.componentOrder.forEach((owner,i)=>{
    metaText(owner,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
    if(rank.has(owner))fail('GRAPH_ENVELOPE_INVALID');
    rank.set(owner,i);
  });
  for(const edge of p.componentEdges){
    denseArray(edge,2,'GRAPH_ENVELOPE_INVALID');
    if(edge.length!==2||!rank.has(edge[0])||!rank.has(edge[1])||rank.get(edge[1])>=rank.get(edge[0]))fail('GRAPH_ENVELOPE_INVALID');
  }
  const admission=new Map(),facets=new Map(),nodes=new Map();
  for(const a of p.admission){
    closedRecord(a,['owner','id','mandatory'],'GRAPH_ENVELOPE_INVALID');
    metaText(a.owner,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
    metaText(a.id,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
    const key=keyOf(a.owner,a.id);
    if(typeof a.mandatory!=='boolean'||admission.has(key))fail('GRAPH_ENVELOPE_INVALID');
    admission.set(key,a);
  }
  for(const f of p.facets){
    const key=keyOf(f.owner,f.id);
    if(facets.has(key))fail('GRAPH_ENVELOPE_INVALID');
    facets.set(key,f);
  }
  for(const c of p.contributions){
    const key=keyOf(c.owner,c.id),a=admission.get(key),f=facets.get(key);
    if(nodes.has(key)||!rank.has(c.owner)||!a||!f||a.mandatory!==c.mandatory)fail('GRAPH_ENVELOPE_INVALID');
    validateCompositionDescriptor(c,{facet:f,extensionPoints:p.points,limits:bounds.descriptorLimits});
    nodes.set(key,c);
  }
  if(nodes.size!==facets.size)fail('GRAPH_ENVELOPE_INVALID');
  for(const d of p.diagnostics){
    closedRecord(d,['owner','id','code','cause'],'GRAPH_ENVELOPE_INVALID');
    for(const v of [d.owner,d.id,d.code])metaText(v,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
    if(d.cause!==null)metaText(d.cause,bounds.descriptorLimits.maxTextLength,'GRAPH_ENVELOPE_INVALID');
  }
  closedRecord(p.points,['metadata','points'],'GRAPH_ENVELOPE_INVALID');
  openRecord(p.mergeModes,bounds.descriptorLimits.maxPoints,'GRAPH_ENVELOPE_INVALID');
  const pointIds=Object.keys(p.points.points);
  if(pointIds.length!==Object.keys(p.mergeModes).length||pointIds.some(id=>!['REJECT','APPEND'].includes(p.mergeModes[id])))fail('GRAPH_ENVELOPE_INVALID');
  openRecord(p.pointProviders,bounds.descriptorLimits.maxPoints,'GRAPH_ENVELOPE_INVALID');
  for(const [point,provider] of Object.entries(p.pointProviders)){
    closedRecord(provider,['owner','id'],'GRAPH_ENVELOPE_INVALID');
    if(!Object.hasOwn(p.points.points,point)||p.points.points[point].owner!==provider.owner||!admission.has(keyOf(provider.owner,provider.id)))fail('GRAPH_ENVELOPE_INVALID');
  }
  return {rank,admission,nodes};
}
function checkedFacts(value,nodes,bounds){
  closedRecord(value,['schema','facts','frontend_edges','all_satisfied'],'GRAPH_FACTS_INVALID');
  if(value.schema!==FACTS_SCHEMA||typeof value.all_satisfied!=='boolean')fail('GRAPH_FACTS_INVALID');
  denseArray(value.facts,bounds.maxFacts,'GRAPH_FACTS_INVALID');
  denseArray(value.frontend_edges,bounds.maxEdges,'GRAPH_FACTS_INVALID');
  const indices=new Set(),expected=new Set();
  const codes=new Set(['SATISFIED','MISSING','AMBIGUOUS','INCOMPATIBLE','OWNER_DEPENDENCY_UNDECLARED']);
  for(const f of value.facts){
    closedRecord(f,['owner','id','index','requirement','target_id','candidates','code'],'GRAPH_FACTS_INVALID');
    const node=nodes.get(keyOf(f.owner,f.id));
    if(!node||!Number.isSafeInteger(f.index)||f.index<0||f.index>=node.requires.length||node.requires[f.index]!==f.requirement||!codes.has(f.code))fail('GRAPH_FACTS_INVALID');
    const ik=JSON.stringify([f.owner,f.id,f.index]);
    if(indices.has(ik))fail('GRAPH_FACTS_INVALID');
    indices.add(ik);
    metaText(f.target_id,bounds.descriptorLimits.maxTextLength,'GRAPH_FACTS_INVALID');
    denseArray(f.candidates,bounds.maxContributions,'GRAPH_FACTS_INVALID');
    const candidates=new Set();
    for(const c of f.candidates){
      closedRecord(c,['owner','id','version'],'GRAPH_FACTS_INVALID');
      const key=keyOf(c.owner,c.id),target=nodes.get(key);
      if(!target||c.id!==f.target_id||target.version!==c.version||candidates.has(key))fail('GRAPH_FACTS_INVALID');
      candidates.add(key);
    }
    if(f.code==='MISSING'?f.candidates.length!==0:f.code==='AMBIGUOUS'?f.candidates.length<2:f.candidates.length!==1)fail('GRAPH_FACTS_INVALID');
    if(f.code==='SATISFIED')expected.add(JSON.stringify([f.owner,f.id,f.candidates[0].owner,f.target_id]));
  }
  let requiredCount=0;
  for(const c of nodes.values()){requiredCount+=c.requires.length;if(!Number.isSafeInteger(requiredCount)||requiredCount>bounds.maxFacts)fail('GRAPH_LIMITS_INVALID');}
  if(requiredCount!==indices.size||value.all_satisfied!==value.facts.every(f=>f.code==='SATISFIED'))fail('GRAPH_FACTS_INVALID');
  const actual=new Set(),edges=[];
  for(const e of value.frontend_edges){
    denseArray(e,4,'GRAPH_FACTS_INVALID');
    if(e.length!==4||!nodes.has(keyOf(e[0],e[1]))||!nodes.has(keyOf(e[2],e[3])))fail('GRAPH_FACTS_INVALID');
    const key=JSON.stringify(e);
    if(actual.has(key)||!expected.has(key))fail('GRAPH_FACTS_INVALID');
    actual.add(key);edges.push(e);
  }
  if(actual.size!==expected.size)fail('GRAPH_FACTS_INVALID');
  return {facts:value.facts,edges};
}
// Kosaraju itératif : les sommets d'un cycle sont distingués de ses dépendants.
function cycleMembers(adj){
  const visited=new Set(),post=[];
  for(const root of adj.keys()){
    if(visited.has(root))continue;
    visited.add(root);
    const stack=[{node:root,index:0}];
    while(stack.length){
      const frame=stack[stack.length-1],targets=adj.get(frame.node);
      if(frame.index>=targets.length){post.push(frame.node);stack.pop();continue;}
      const target=targets[frame.index++];
      if(!visited.has(target)){visited.add(target);stack.push({node:target,index:0});}
    }
  }
  const reverse=new Map([...adj.keys()].map(k=>[k,[]]));
  for(const [from,targets] of adj)for(const to of targets)reverse.get(to).push(from);
  const assigned=new Set(),cyclic=new Set();
  for(let i=post.length-1;i>=0;i--){
    const root=post[i];
    if(assigned.has(root))continue;
    const component=[],pending=[root];assigned.add(root);
    while(pending.length){
      const node=pending.pop();component.push(node);
      for(const target of reverse.get(node))if(!assigned.has(target)){assigned.add(target);pending.push(target);}
    }
    if(component.length>1||adj.get(root).includes(root))for(const node of component)cyclic.add(node);
  }
  return cyclic;
}

export function composeContributionGraph(preflight,requirementFacts,limits){
  const bounds=validateLimits(limits),budget={left:bounds.maxInputNodes};
  preflight=snapshot(preflight,budget);requirementFacts=snapshot(requirementFacts,budget);
  const {rank,admission,nodes}=checkedPreflight(preflight,bounds);
  const {facts,edges}=checkedFacts(requirementFacts,nodes,bounds);
  const diagnostics=preflight.diagnostics.map(d=>({...d})),refused=new Set();
  const report=reporter(admission,diagnostics,refused);
  const adj=new Map([...nodes.keys()].map(key=>[key,[]]));
  for(const [so,si,to,ti] of edges)adj.get(keyOf(so,si)).push(keyOf(to,ti));
  for(const c of nodes.values()){
    const provider=preflight.pointProviders[c.point];
    if(provider&&!adj.get(keyOf(c.owner,c.id)).includes(keyOf(provider.owner,provider.id)))report.report(c.owner,c.id,'GRAPH_POINT_DEPENDENCY_UNDECLARED');
  }
  for(const f of facts)if(f.code!=='SATISFIED')report.report(f.owner,f.id,'GRAPH_REQUIREMENT_UNSATISFIED',f.code);
  for(const key of cycleMembers(adj)){
    const c=nodes.get(key);report.report(c.owner,c.id,'GRAPH_CYCLE_CONTRIBUTION');
  }
  const propagate=()=>{
    let changed=true;
    while(changed){
      changed=false;
      for(const [from,targets] of adj)if(!refused.has(from)&&targets.some(to=>refused.has(to))){
        const c=nodes.get(from);report.report(c.owner,c.id,'GRAPH_DEPENDENCY_UNAVAILABLE');changed=true;
      }
    }
  };
  propagate();
  const available=()=>[...nodes.values()].filter(c=>!refused.has(keyOf(c.owner,c.id)));
  const rejectGroup=(group,code)=>{if(group.length>1)for(const c of group)report.report(c.owner,c.id,code);};
  const groups=(items,value)=>{
    const grouped=new Map();
    for(const c of items){const key=value(c);if(!grouped.has(key))grouped.set(key,[]);grouped.get(key).push(c);}
    return grouped.values();
  };
  const current=available(),routes=current.filter(c=>c.type==='ROUTE');
  for(const c of routes)if(PROTECTED_PATHS.some(p=>routesIntersect(c.payload.path,p)))report.report(c.owner,c.id,'GRAPH_COLLISION_ROUTE','PROTECTED_PATH');
  for(let i=0;i<routes.length;i++)for(let j=i+1;j<routes.length;j++)if(routesIntersect(routes[i].payload.path,routes[j].payload.path)){
    for(const c of [routes[i],routes[j]])report.report(c.owner,c.id,'GRAPH_COLLISION_ROUTE');
  }
  for(const group of groups(current,c=>c.point))if(preflight.mergeModes[group[0].point]==='REJECT')rejectGroup(group,'GRAPH_COLLISION_POINT');
  const navigation=current.filter(c=>c.type==='NAVIGATION');
  for(const group of groups(navigation,c=>c.payload.route))rejectGroup(group,'GRAPH_COLLISION_NAV');
  for(const group of groups(current.filter(c=>c.type==='UI_PERMISSION'),c=>c.payload.key))rejectGroup(group,'GRAPH_COLLISION_PERMISSION');
  const catalogs=current.filter(c=>c.type==='TRANSLATION'),keyOwners=new Map();
  for(const c of catalogs){
    const cat=c.payload.catalog;
    let valid=true;
    if(Object.keys(cat).length!==2||!Object.hasOwn(cat,'en')||!Object.hasOwn(cat,'fr')){
      report.report(c.owner,c.id,'GRAPH_COLLISION_CATALOG','LOCALES');continue;
    }
    const en=Object.keys(cat.en),fr=Object.keys(cat.fr);
    if(en.length!==fr.length||en.some(k=>!Object.hasOwn(cat.fr,k))){
      report.report(c.owner,c.id,'GRAPH_COLLISION_CATALOG','KEYS');continue;
    }
    for(const key of en){
      if(!(key===c.owner||key.startsWith(c.owner+'.'))){
        report.report(c.owner,c.id,'GRAPH_NAMESPACE_RESERVED');valid=false;continue;
      }
      try{
        const a=catalogParams(cat.en[key]),b=catalogParams(cat.fr[key]);
        if(a.size!==b.size||[...a].some(p=>!b.has(p))){
          report.report(c.owner,c.id,'GRAPH_COLLISION_CATALOG','PARAMETERS');valid=false;
        }
      }catch(error){
        if(!(error instanceof GraphError))throw error;
        report.report(c.owner,c.id,error.code,'PARAMETERS');valid=false;
      }
    }
    if(valid)for(const key of en){
      if(!keyOwners.has(key))keyOwners.set(key,[]);
      keyOwners.get(key).push(c);
    }
  }
  for(const group of keyOwners.values())rejectGroup(group,'GRAPH_COLLISION_CATALOG');
  // La perte d'une route ou d'un catalogue invalide aussi ses références UI.
  // Répéter seulement tant que de nouveaux refus apparaissent ; au plus N ajouts.
  let previous=-1;
  while(previous!==refused.size){
    previous=refused.size;propagate();
    const items=available(),paths=new Set(PROTECTED_PATHS),labels=new Map(),labelParams=new Map();
    for(const c of items){
      if(c.type==='ROUTE')paths.add(c.payload.path);
      if(c.type==='TRANSLATION'){
        if(!labels.has(c.owner)){labels.set(c.owner,new Set());labelParams.set(c.owner,new Set());}
        for(const key of Object.keys(c.payload.catalog.en)){labels.get(c.owner).add(key);if(catalogParams(c.payload.catalog.en[key]).size>0)labelParams.get(c.owner).add(key);}
      }
    }
    for(const c of items)if(c.type==='NAVIGATION'){
      if(!paths.has(c.payload.route))report.report(c.owner,c.id,'GRAPH_COLLISION_NAV','ROUTE_UNAVAILABLE');
      if(!labels.get(c.owner)?.has(c.payload.labelKey))report.report(c.owner,c.id,'GRAPH_COLLISION_CATALOG','LABEL_UNAVAILABLE');
      if(labelParams.get(c.owner)?.has(c.payload.labelKey))report.report(c.owner,c.id,'GRAPH_COLLISION_CATALOG','LABEL_PARAMETERS_UNAVAILABLE');
    }
  }
  const survivors=available(),survivorKeys=new Set(survivors.map(c=>keyOf(c.owner,c.id)));
  const pendingCount=new Map(),dependants=new Map([...survivorKeys].map(k=>[k,[]]));
  for(const key of survivorKeys){
    const targets=adj.get(key).filter(t=>survivorKeys.has(t));
    pendingCount.set(key,targets.length);
    for(const target of targets)dependants.get(target).push(key);
  }
  const compareKeys=(a,b)=>{
    const ca=nodes.get(a),cb=nodes.get(b);
    return rank.get(ca.owner)-rank.get(cb.owner)||cmp(ca.id,cb.id);
  };
  const ready=[...survivorKeys].filter(k=>pendingCount.get(k)===0),ordered=[];
  while(ready.length){
    ready.sort(compareKeys);
    const key=ready.shift();ordered.push(key);
    for(const from of dependants.get(key)){
      pendingCount.set(from,pendingCount.get(from)-1);
      if(pendingCount.get(from)===0)ready.push(from);
    }
  }
  if(ordered.length!==survivors.length)fail('GRAPH_INVARIANT_FAILED');
  const orderRank=new Map(ordered.map((key,index)=>[key,index]));
  const finalEdges=edges.filter(e=>survivorKeys.has(keyOf(e[0],e[1]))&&survivorKeys.has(keyOf(e[2],e[3])))
    .map(e=>[...e]).sort((a,b)=>orderRank.get(keyOf(a[0],a[1]))-orderRank.get(keyOf(b[0],b[1]))||orderRank.get(keyOf(a[2],a[3]))-orderRank.get(keyOf(b[2],b[3])));
  diagnostics.sort(diagnosticSort);
  const blocked=preflight.blocked||report.isBlocked();
  return deepFreeze({
    schema:GRAPH_SCHEMA,
    contributions:blocked?[]:ordered.map(key=>nodes.get(key)),
    contributionEdges:blocked?[]:finalEdges,
    order:blocked?[]:ordered.map(key=>({owner:nodes.get(key).owner,id:nodes.get(key).id})),
    diagnostics,blocked,
  });
}
