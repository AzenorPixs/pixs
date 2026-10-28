import { types as utilTypes } from 'node:util';
import { createHash } from 'node:crypto';
import { analyzeModuleSource, parseEntrySource, CompositionSyntaxError } from './composition-syntax-v1.mjs';

export const IMPORTS_VERSION = '1.0.0';
export const SHELL_ALIAS = 'pixs-shell/v1';
export const SHELL_EXPORTS = Object.freeze([
  'SHELL_API_VERSION','ShellContextProvider','useShellContext','QueryClient',
  'CommandClient','navigate','invalidateScope','shellSlots','bindShellApi',
]);
export const IMPORT_CODES = Object.freeze([
  'IMPORT_LIMITS_INVALID','IMPORT_ENVELOPE_INVALID','IMPORT_POLICY_INVALID',
  'IMPORT_BYTES_MISMATCH','IMPORT_TOO_LARGE','IMPORT_UNLISTED','IMPORT_PRIVATE_SIBLING',
  'IMPORT_SHELL_FACADE_UNKNOWN','IMPORT_FACADE_UNDECLARED','IMPORT_REEXPORT_REFUSED',
  'IMPORT_DYNAMIC_REFUSED','IMPORT_REQUIRE_REFUSED','IMPORT_BARE_REFUSED',
  'IMPORT_RENDERER_REFUSED','IMPORT_NAMESPACE_REFUSED','IMPORT_DEFAULT_REFUSED',
  'IMPORT_CHECKSUM_MISMATCH','IMPORT_CAPTURE_INVALID','IMPORT_DEPENDENCY_UNAVAILABLE',
]);
export class ImportValidationError extends Error {
  constructor(code, options){ super(code, options); this.name='ImportValidationError'; this.code=code; }
}
function fail(code, cause){
  if(cause===undefined) throw new ImportValidationError(code);
  throw new ImportValidationError(code, { cause });
}
function safeInt(v){
  if(typeof v!=='number'||!Number.isSafeInteger(v)||v<=0) fail('IMPORT_LIMITS_INVALID');
  return v;
}
function isPlainRecord(v){
  if(v===null||typeof v!=='object'||Array.isArray(v)||utilTypes.isProxy(v)) return false;
  const p=Object.getPrototypeOf(v); return p===Object.prototype||p===null;
}
function closedRecord(v, required, code) {
  if (!isPlainRecord(v)) fail(code);
  const keys = Reflect.ownKeys(v);
  if (keys.length !== required.length) fail(code);
  for (const k of keys) {
    if (typeof k !== 'string' || !required.includes(k)) fail(code);
    const d = Object.getOwnPropertyDescriptor(v, k);
    if (!d || !Object.hasOwn(d, 'value')) fail(code);
  }
  for (const k of required) if (!Object.hasOwn(v, k)) fail(code);
  return v;
}
function denseArray(v, max, code) {
  if (!Array.isArray(v) || utilTypes.isProxy(v) || Object.getPrototypeOf(v) !== Array.prototype || v.length > max) fail(code);
  if (Reflect.ownKeys(v).length !== v.length + 1) fail(code);
  for (let i = 0; i < v.length; i += 1) {
    const d = Object.getOwnPropertyDescriptor(v, String(i));
    if (!d || !Object.hasOwn(d, 'value')) fail(code);
  }
  return v;
}
function openRecord(v, max, code) {
  if (!isPlainRecord(v)) fail(code);
  const keys = Reflect.ownKeys(v);
  if (keys.length > max) fail(code);
  for (const k of keys) {
    const d = Object.getOwnPropertyDescriptor(v, k);
    if (typeof k !== 'string' || !d || !Object.hasOwn(d, 'value')) fail(code);
  }
  return v;
}
function metaText(v, max, code){
  if(typeof v!=='string'||v.length===0||v.length>max) fail(code);
  for(let i=0;i<v.length;i++){
    const u=v.charCodeAt(i);
    if(u<32||u===127) fail(code);
    if(u>=0xD800&&u<=0xDBFF){
      const n=v.charCodeAt(i+1);
      if(!(n>=0xDC00&&n<=0xDFFF)) fail(code);
      i++;
    } else if(u>=0xDC00&&u<=0xDFFF) fail(code);
  }
  return v;
}
function canonical(v){
  if(v===null||typeof v!=='object'){
    if(typeof v==='number'&&!Number.isFinite(v)) fail('IMPORT_ENVELOPE_INVALID');
    return JSON.stringify(v);
  }
  if(Array.isArray(v)) return '['+v.map(canonical).join(',')+']';
  const ks=Object.keys(v).sort();
  return '{'+ks.map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
}
function deepFreeze(value) {
  const seen = new Set();
  const stack = [value];
  while (stack.length) {
    const item = stack.pop();
    if (item === null || typeof item !== 'object' || seen.has(item)) continue;
    seen.add(item);
    for (const key of Reflect.ownKeys(item)) {
      const d = Object.getOwnPropertyDescriptor(item, key);
      if (!d || !Object.hasOwn(d, 'value')) fail('IMPORT_ENVELOPE_INVALID');
      if (d.value !== null && typeof d.value === 'object') stack.push(d.value);
    }
    Object.freeze(item);
  }
  return value;
}
function jsonDataSnapshot(value, budget) {
  const holder = {};
  const stack = [{ value, parent: holder, key: 'value' }];
  const seen = new Set();
  while (stack.length) {
    const frame = stack.pop();
    if (frame.finish) { Object.freeze(frame.finish); continue; }
    if (--budget.left < 0) fail('IMPORT_LIMITS_INVALID');
    const source = frame.value;
    if (source === null || typeof source === 'string' || typeof source === 'boolean'
        || typeof source === 'number' && Number.isFinite(source)) {
      Object.defineProperty(frame.parent, frame.key, { value: source, enumerable: true });
      continue;
    }
    if (typeof source !== 'object' || utilTypes.isProxy(source) || seen.has(source)) fail('IMPORT_ENVELOPE_INVALID');
    seen.add(source);
    const array = Array.isArray(source);
    if (array) denseArray(source, Number.MAX_SAFE_INTEGER, 'IMPORT_ENVELOPE_INVALID');
    else openRecord(source, Number.MAX_SAFE_INTEGER, 'IMPORT_ENVELOPE_INVALID');
    if ((array ? source.length : Reflect.ownKeys(source).length) > budget.left) fail('IMPORT_LIMITS_INVALID');
    const target = array ? new Array(source.length) : {};
    Object.defineProperty(frame.parent, frame.key, { value: target, enumerable: true });
    stack.push({ finish: target });
    const keys = array ? Array.from({ length: source.length }, (_, i) => String(i)) : Reflect.ownKeys(source);
    for (let i = keys.length - 1; i >= 0; i -= 1) {
      const key = keys[i];
      const d = Object.getOwnPropertyDescriptor(source, key);
      stack.push({ value: d.value, parent: target, key });
    }
  }
  return holder.value;
}

function validateSyntaxLimits(s){
  closedRecord(s,['maxSourceBytes','maxAstNodes','maxDescriptorCount','maxTextLength','maxLiteralItems','maxLiteralDepth'],'IMPORT_LIMITS_INVALID');
  for(const k of Object.keys(s)) safeInt(s[k]);
  return s;
}
function validateLimits(l){
  closedRecord(l,['maxSourceBytes','maxTotalSourceBytes','maxModules','maxImports','maxBindings','maxResolutions','maxInputNodes','syntaxLimits'],'IMPORT_LIMITS_INVALID');
  safeInt(l.maxInputNodes);
  safeInt(l.maxSourceBytes); safeInt(l.maxTotalSourceBytes);
  safeInt(l.maxModules); safeInt(l.maxImports); safeInt(l.maxBindings); safeInt(l.maxResolutions);
  validateSyntaxLimits(l.syntaxLimits);
  return l;
}
function validatePolicy(p, bounds){
  closedRecord(p,['shellFacades','foreignFacades'],'IMPORT_POLICY_INVALID');
  if(!isPlainRecord(p.shellFacades)||!isPlainRecord(p.foreignFacades)) fail('IMPORT_POLICY_INVALID');
  const sk=Object.keys(p.shellFacades);
  if(sk.length!==1||sk[0]!==SHELL_ALIAS) fail('IMPORT_POLICY_INVALID');
  const s=p.shellFacades[SHELL_ALIAS];
  closedRecord(s,['exports','allowDefault','allowNamespace'],'IMPORT_POLICY_INVALID');
  if(!Array.isArray(s.exports)) fail('IMPORT_POLICY_INVALID');
  denseArray(s.exports,SHELL_EXPORTS.length,'IMPORT_POLICY_INVALID');
  if(new Set(s.exports).size!==s.exports.length) fail('IMPORT_POLICY_INVALID');
  openRecord(p.foreignFacades,bounds.maxModules,'IMPORT_POLICY_INVALID');
  for(const e of s.exports){ if(typeof e!=='string'||!SHELL_EXPORTS.includes(e)) fail('IMPORT_POLICY_INVALID'); }
  if(s.allowDefault!==false||s.allowNamespace!==false) fail('IMPORT_POLICY_INVALID');
  for(const alias of Object.keys(p.foreignFacades)){
    metaText(alias,bounds.syntaxLimits.maxTextLength,'IMPORT_POLICY_INVALID');
    if(alias===SHELL_ALIAS||alias.startsWith('.')||alias.startsWith('/')||/[\\:%?#]/.test(alias)||['react','react-dom','vite','typescript','esbuild'].includes(alias.split('/')[0])) fail('IMPORT_POLICY_INVALID');
    const f=p.foreignFacades[alias];
    closedRecord(f,['owner','entry','exports'],'IMPORT_POLICY_INVALID');
    metaText(f.owner,bounds.syntaxLimits.maxTextLength,'IMPORT_POLICY_INVALID');
    metaText(f.entry,bounds.syntaxLimits.maxTextLength,'IMPORT_POLICY_INVALID');
    denseArray(f.exports,bounds.maxBindings,'IMPORT_POLICY_INVALID');
    if(new Set(f.exports).size!==f.exports.length) fail('IMPORT_POLICY_INVALID');
    for(const e of f.exports) metaText(e,bounds.syntaxLimits.maxTextLength,'IMPORT_POLICY_INVALID');
  }
  return p;
}
function b64Bounded(b64, maxBytes){
  if(typeof b64!=='string') fail('IMPORT_BYTES_MISMATCH');
  if(b64.length>Math.ceil(maxBytes/3)*4+8) fail('IMPORT_TOO_LARGE');
  let raw;
  try{ raw=Buffer.from(b64,'base64'); }catch{ fail('IMPORT_BYTES_MISMATCH'); }
  if(raw.toString('base64')!==b64) fail('IMPORT_BYTES_MISMATCH');
  return raw;
}
function checkBytes(raw, expectSha, expectSize, maxBytes){
  if(raw.length!==expectSize||raw.length>maxBytes) fail('IMPORT_BYTES_MISMATCH');
  const h=createHash('sha256').update(raw).digest('hex');
  if(h!==expectSha) fail('IMPORT_BYTES_MISMATCH');
  if(raw.length>=3&&raw[0]===239&&raw[1]===187&&raw[2]===191) fail('IMPORT_BYTES_MISMATCH');
  let text;
  try{ text=new TextDecoder('utf-8',{fatal:true}).decode(raw); }
  catch{ fail('IMPORT_BYTES_MISMATCH'); }
  if(text.startsWith('﻿')||text.includes('\r')) fail('IMPORT_BYTES_MISMATCH');
  return text;
}
function posixResolve(dir, spec){
  if(spec.includes('\\')||spec.includes(':')||spec.includes('\0')||spec.includes('%')||spec.includes('?')||spec.includes('#')) fail('IMPORT_BARE_REFUSED');
  for(let i=0;i<spec.length;i++){ const u=spec.charCodeAt(i); if(u<32||u===127) fail('IMPORT_BARE_REFUSED'); }
  const out=dir?dir.split('/').filter(x=>x!==''):[];
  for(const seg of spec.split('/')){
    if(seg===''||seg==='.') continue;
    if(seg==='..'){ out.pop(); continue; }
    out.push(seg);
  }
  return out.join('/');
}
function dirOf(full){ const i=full.lastIndexOf('/'); return i<0?'':full.slice(0,i); }

function inspectFrontendImports(envelope, policy, limits, collectErrors){
  const bounds=validateLimits(limits);
  const inputBudget={left:bounds.maxInputNodes};
  envelope=jsonDataSnapshot(envelope,inputBudget);
  policy=jsonDataSnapshot(policy,inputBudget);
  const pol=validatePolicy(policy,bounds);
  const diagnostics=[]; const failedOwners=new Set();
  const ownerCodes=new Set([
    'IMPORT_UNLISTED','IMPORT_PRIVATE_SIBLING','IMPORT_SHELL_FACADE_UNKNOWN',
    'IMPORT_FACADE_UNDECLARED','IMPORT_REEXPORT_REFUSED','IMPORT_DYNAMIC_REFUSED',
    'IMPORT_REQUIRE_REFUSED','IMPORT_BARE_REFUSED','IMPORT_RENDERER_REFUSED',
    'IMPORT_NAMESPACE_REFUSED','IMPORT_DEFAULT_REFUSED','IMPORT_DEPENDENCY_UNAVAILABLE',
    'SYNTAX_TEXT_INVALID','SYNTAX_INVALID','SYNTAX_EXPORT_INVALID','SYNTAX_IMPORT_INVALID',
  ]);
  const collect=(error,file)=>{
    if(!collectErrors||!(error instanceof ImportValidationError||error instanceof CompositionSyntaxError)||!ownerCodes.has(error.code)) throw error;
    failedOwners.add(file.owner);
    diagnostics.push({owner:file.owner,path:file.path,code:error.code});
  };
  closedRecord(envelope,['schema','capture','plan','ignored_attestation_indices','build_limits','context_checksum','declared_owner_ids'],'IMPORT_ENVELOPE_INVALID');
  if(envelope.schema!=='pixs.frontend.plan-envelope/1.0.0') fail('IMPORT_ENVELOPE_INVALID');
  const cap=envelope.capture; const plan=envelope.plan;
  closedRecord(cap,['schema','selection_sha256','environment','provenance_reference','context_fingerprint','composition','owners','errors'],'IMPORT_ENVELOPE_INVALID');
  if(cap.schema!=='pixs.frontend.selection/1.0.0') fail('IMPORT_ENVELOPE_INVALID');
  closedRecord(plan,['schema','order','edges','facets','diagnostics','warnings','evaluation_scope','unevaluated_dimensions','globally_compatible','sources_sha256'],'IMPORT_ENVELOPE_INVALID');
  if(plan.schema!=='pixs.frontend.build-plan/1') fail('IMPORT_ENVELOPE_INVALID');
  closedRecord(envelope.build_limits,['max_manifests','max_manifest_bytes','max_total_bytes','allowed_sources'],'IMPORT_ENVELOPE_INVALID');
  for(const key of ['max_manifests','max_manifest_bytes','max_total_bytes']) safeInt(envelope.build_limits[key]);
  denseArray(envelope.build_limits.allowed_sources,envelope.build_limits.max_manifests,'IMPORT_ENVELOPE_INVALID');
  denseArray(envelope.declared_owner_ids,envelope.build_limits.max_manifests,'IMPORT_ENVELOPE_INVALID');
  for(const value of [...envelope.build_limits.allowed_sources,...envelope.declared_owner_ids]) metaText(value,bounds.syntaxLimits.maxTextLength,'IMPORT_ENVELOPE_INVALID');
  if(typeof cap.context_fingerprint!=='string'||!/^[0-9a-f]{64}$/.test(cap.context_fingerprint)||typeof envelope.context_checksum!=='string'||!/^[0-9a-f]{64}$/.test(envelope.context_checksum)) fail('IMPORT_ENVELOPE_INVALID');
  denseArray(plan.order,envelope.build_limits.max_manifests,'IMPORT_ENVELOPE_INVALID');
  denseArray(plan.sources_sha256,envelope.build_limits.max_manifests,'IMPORT_ENVELOPE_INVALID');
  denseArray(plan.edges,bounds.maxResolutions,'IMPORT_ENVELOPE_INVALID');
  denseArray(plan.facets,bounds.maxBindings,'IMPORT_ENVELOPE_INVALID');
  if(plan.globally_compatible!==false) fail('IMPORT_ENVELOPE_INVALID');
  const payload={
    allowed_sources:envelope.build_limits.allowed_sources,
    context_fingerprint:cap.context_fingerprint,
    max_manifest_bytes:envelope.build_limits.max_manifest_bytes,
    max_manifests:envelope.build_limits.max_manifests,
    max_total_bytes:envelope.build_limits.max_total_bytes,
    schema:'pixs.frontend.plan-envelope/1.0.0',
    declared_owner_ids:envelope.declared_owner_ids,
  };
  const expect=createHash('sha256').update(Buffer.from(canonical(payload),'utf-8')).digest('hex');
  if(expect!==envelope.context_checksum) fail('IMPORT_CHECKSUM_MISMATCH');
  const owners=cap.owners;
  denseArray(owners,bounds.maxModules,'IMPORT_ENVELOPE_INVALID');
  if(owners.length===0) fail('IMPORT_ENVELOPE_INVALID');
  const seenFull=new Set(); const ownerByName=new Map();
  for(const o of owners){
    closedRecord(o,['index','owner','owner_version','root','trust','manifest','sources'],'IMPORT_ENVELOPE_INVALID');
    metaText(o.owner,bounds.syntaxLimits.maxTextLength,'IMPORT_ENVELOPE_INVALID'); metaText(o.root,bounds.syntaxLimits.maxTextLength,'IMPORT_ENVELOPE_INVALID');
    if(!Number.isSafeInteger(o.index)||o.index<0||envelope.declared_owner_ids[o.index]!==o.owner) fail('IMPORT_CAPTURE_INVALID');
    metaText(o.owner_version,bounds.syntaxLimits.maxTextLength,'IMPORT_CAPTURE_INVALID');
    closedRecord(o.manifest,['owner_index','path','sha256','size','data_b64'],'IMPORT_ENVELOPE_INVALID');
    if(o.manifest.path!==o.root+'/component.toml') fail('IMPORT_CAPTURE_INVALID');
    denseArray(o.sources,Number.MAX_SAFE_INTEGER,'IMPORT_CAPTURE_INVALID');
    if(o.sources.length>bounds.maxModules) fail('IMPORT_LIMITS_INVALID');
    if(ownerByName.has(o.owner)) fail('IMPORT_CAPTURE_INVALID');
    ownerByName.set(o.owner,o);
    for(const f of [o.manifest,...o.sources]){
      closedRecord(f,['owner_index','path','sha256','size','data_b64'],'IMPORT_ENVELOPE_INVALID');
      metaText(f.path,bounds.syntaxLimits.maxTextLength,'IMPORT_CAPTURE_INVALID');
      if(!f.path.startsWith(o.root+'/')||typeof f.sha256!=='string'||!/^[0-9a-f]{64}$/.test(f.sha256)||!Number.isSafeInteger(f.size)||f.size<0) fail('IMPORT_CAPTURE_INVALID');
      if(f.owner_index!==o.index) fail('IMPORT_CAPTURE_INVALID');
      if(seenFull.has(f.path)) fail('IMPORT_CAPTURE_INVALID');
      seenFull.add(f.path);
    }
  }
  if(new Set(plan.order).size!==plan.order.length) fail('IMPORT_ENVELOPE_INVALID');
  if(plan.order.length!==owners.length) fail('IMPORT_ENVELOPE_INVALID');
  for(const id of plan.order){ if(!ownerByName.has(id)) fail('IMPORT_ENVELOPE_INVALID'); }
  const hashByOwner=new Map(owners.map(o=>[o.owner,o.manifest.sha256]));
  if(plan.sources_sha256.length!==owners.length) fail('IMPORT_ENVELOPE_INVALID');
  const seenManifestHashes=new Set();
  if(envelope.build_limits.allowed_sources.length!==owners.length||envelope.build_limits.allowed_sources.some((p,i)=>p!==owners[i].manifest.path)) fail('IMPORT_ENVELOPE_INVALID');
  for(const pair of plan.sources_sha256){
    closedRecord(pair,['owner','sha256'],'IMPORT_ENVELOPE_INVALID');
    if(typeof pair.owner!=='string'||typeof pair.sha256!=='string'||seenManifestHashes.has(pair.owner)||hashByOwner.get(pair.owner)!==pair.sha256) fail('IMPORT_ENVELOPE_INVALID');
    seenManifestHashes.add(pair.owner);
  }
  const facetKeys=new Set();
  for(const f of plan.facets){
    closedRecord(f,['owner','owner_version','type','id','entry','version','requires','scope'],'IMPORT_ENVELOPE_INVALID');
    for(const key of ['owner','owner_version','type','id','entry','version','scope']) metaText(f[key],bounds.syntaxLimits.maxTextLength,'IMPORT_ENVELOPE_INVALID');
    denseArray(f.requires,bounds.maxBindings,'IMPORT_ENVELOPE_INVALID');
    for(const requirement of f.requires) metaText(requirement,bounds.syntaxLimits.maxTextLength,'IMPORT_ENVELOPE_INVALID');
    if(!ownerByName.has(f.owner)||ownerByName.get(f.owner).owner_version!==f.owner_version) fail('IMPORT_CAPTURE_INVALID');
    facetKeys.add(f.owner+' '+f.entry);
  }
  const selected=new Map();
  let total=0;
  const files=[];
  for(const o of owners){
    for(const f of [o.manifest,...o.sources]){
      const remaining=bounds.maxTotalSourceBytes-total;
      const raw=b64Bounded(f.data_b64,Math.min(bounds.maxSourceBytes,remaining));
      total+=raw.length;
      if(total>bounds.maxTotalSourceBytes) fail('IMPORT_TOO_LARGE');
      const text=checkBytes(raw,f.sha256,f.size,bounds.maxSourceBytes);
      if(f.path.endsWith('.js')||f.path.endsWith('.mjs')){
        if(files.length>=bounds.maxModules) fail('IMPORT_LIMITS_INVALID');
        files.push({owner:o.owner,owner_version:o.owner_version,root:o.root,path:f.path,text,hash:f.sha256});
      }
      selected.set(f.path,{owner:o.owner,text});
    }
  }
  for(const f of plan.facets){ const path=ownerByName.get(f.owner).root+'/'+f.entry; if(!selected.has(path)||selected.get(path).owner!==f.owner) fail('IMPORT_CAPTURE_INVALID'); }
  const adj=new Map(plan.order.map(id=>[id,[]]));
  for(const e of plan.edges){
    if(!Array.isArray(e)||e.length!==2) fail('IMPORT_ENVELOPE_INVALID');
    if(!adj.has(e[0])||!adj.has(e[1])||plan.order.indexOf(e[1])>=plan.order.indexOf(e[0])) fail('IMPORT_ENVELOPE_INVALID');
    adj.get(e[0]).push(e[1]);
  }
  const reach=(from,target)=>{
    const seen=new Set(); const st=[from];
    while(st.length){ const c=st.pop(); if(c===target) return true; if(seen.has(c)) continue; seen.add(c); for(const n of (adj.get(c)??[])) st.push(n); }
    return false;
  };
  const parsedAll=[];
  for(const file of files){
    const rel=file.path.startsWith(file.root+'/')?file.path.slice(file.root.length+1):null;
    const isEntry=rel!==null&&facetKeys.has(file.owner+' '+rel);
    try {
      const parsed=isEntry
        ? parseEntrySource(file.text,bounds.syntaxLimits)
        : analyzeModuleSource(file.text,bounds.syntaxLimits);
      parsedAll.push({file,parsed,isEntry});
    } catch(error) { collect(error,file); }
  }
  const modules=[]; const resolutions=[]; let nI=0; let nB=0;
  for(const {file,parsed,isEntry} of parsedAll){
    nI+=parsed.imports.length;
    if(nI>bounds.maxImports) fail('IMPORT_LIMITS_INVALID');
    for(const im of parsed.imports){ nB+=(im.bindings?.length??0); }
    if(nB>bounds.maxBindings) fail('IMPORT_LIMITS_INVALID');
    if(failedOwners.has(file.owner)) continue;
    try {
    if(resolutions.length>bounds.maxResolutions) fail('IMPORT_LIMITS_INVALID');
    const recs=[];
    for(const im of parsed.imports){
      if(im.kind==='ExportAlias'||im.kind==='ExportAllFrom'||im.kind==='ExportNamedFrom') fail('IMPORT_REEXPORT_REFUSED');
      if(im.kind==='requireCall') fail('IMPORT_REQUIRE_REFUSED');
      if(im.kind==='ImportExpression') fail('IMPORT_DYNAMIC_REFUSED');
      if(resolutions.length>=bounds.maxResolutions) fail('IMPORT_LIMITS_INVALID');
      const src=im.source;
      if(src.startsWith('.')){
        if(!(src.startsWith('./')||src.startsWith('../'))) fail('IMPORT_BARE_REFUSED');
        const full=posixResolve(dirOf(file.path),src);
        const hit=selected.get(full);
        if(!full.startsWith(file.root+'/')) fail('IMPORT_PRIVATE_SIBLING');
        if(!hit) fail('IMPORT_UNLISTED');
        if(hit.owner!==file.owner) fail('IMPORT_PRIVATE_SIBLING');
        const target=parsedAll.find(p=>p.file.path===full);
        if(!target) fail('IMPORT_UNLISTED');
        const targetNames=new Set(target.parsed.exportedNames.map(e=>e.name));
        for(const binding of im.bindings) if(binding.imported!=='*'&&!targetNames.has(binding.imported)) fail('IMPORT_FACADE_UNDECLARED');
        const r={from:file.path,source:src,target:full,kind:im.kind,bindings:im.bindings.map(b=>({imported:b.imported,local:b.local,exported:b.exported}))};
        recs.push(r); resolutions.push(r);
      } else if(src===SHELL_ALIAS){
        for(const b of im.bindings){
          if(b.imported==='default') fail('IMPORT_DEFAULT_REFUSED');
          if(b.imported==='*') fail('IMPORT_NAMESPACE_REFUSED');
          if(!SHELL_EXPORTS.includes(b.imported)||!pol.shellFacades[SHELL_ALIAS].exports.includes(b.imported)) fail('IMPORT_SHELL_FACADE_UNKNOWN');
        }
        const r={from:file.path,source:src,target:src,kind:im.kind,bindings:im.bindings.map(b=>({imported:b.imported,local:b.local,exported:b.exported}))};
        recs.push(r); resolutions.push(r);
      } else if(Object.hasOwn(pol.foreignFacades,src)){
        const fac=pol.foreignFacades[src];
        if(!ownerByName.has(fac.owner)) fail('IMPORT_FACADE_UNDECLARED');
        const hit=selected.get(fac.owner==null? '':ownerByName.get(fac.owner).root+'/'+fac.entry);
        if(!hit) fail('IMPORT_FACADE_UNDECLARED');
        const targetOwner=fac.owner;
        const targetFile=ownerByName.get(targetOwner).root+'/'+fac.entry;
        const targetParsed=parsedAll.find(p=>p.file.path===targetFile);
        if(!targetParsed||!targetParsed.isEntry||targetParsed.file.owner!==targetOwner) fail('IMPORT_FACADE_UNDECLARED');
        const names=new Set(targetParsed.parsed.exportedNames.map(e=>e.name));
        for(const b of im.bindings){
          if(b.imported==='default') fail('IMPORT_DEFAULT_REFUSED');
          if(b.imported==='*') fail('IMPORT_NAMESPACE_REFUSED');
          if(!fac.exports.includes(b.imported)) fail('IMPORT_FACADE_UNDECLARED');
          if(!names.has(b.imported)) fail('IMPORT_FACADE_UNDECLARED');
        }
        if(!reach(file.owner,targetOwner)) fail('IMPORT_FACADE_UNDECLARED');
        const r={from:file.path,source:src,target:targetOwner+'#'+fac.entry,kind:im.kind,bindings:im.bindings.map(b=>({imported:b.imported,local:b.local,exported:b.exported}))};
        recs.push(r); resolutions.push(r);
      } else {
        const head=src.split('/')[0];
        if(['react','react-dom','vite','typescript','esbuild'].includes(head)) fail('IMPORT_RENDERER_REFUSED');
        fail('IMPORT_BARE_REFUSED');
      }
    }
    modules.push({
      owner:file.owner,owner_version:file.owner_version,root:file.root,file:file.path,
      text:file.text,hash:file.hash,isEntry,
      descriptors:parsed.descriptors??[],
      exportedNames:parsed.exportedNames.map(e=>({...e})),
      imports:recs.map(r=>JSON.parse(JSON.stringify(r))),
    });
    } catch(error) { collect(error,file); }
  }
  if(resolutions.length>bounds.maxResolutions) fail('IMPORT_LIMITS_INVALID');
  let changed=true;
  while(changed){
    changed=false;
    for(const r of resolutions){
      const from=selected.get(r.from).owner;
      const target=selected.get(r.target)?.owner??(r.target.includes('#')?r.target.split('#')[0]:null);
      if(!failedOwners.has(from)&&target!==null&&failedOwners.has(target)){
        failedOwners.add(from); changed=true;
        diagnostics.push({owner:from,path:r.from,code:'IMPORT_DEPENDENCY_UNAVAILABLE'});
      }
    }
  }
  const survivors=modules.filter(m=>!failedOwners.has(m.owner));
  const usable=resolutions.filter(r=>!failedOwners.has(selected.get(r.from).owner));
  return deepFreeze({modules:survivors,resolutions:usable,diagnostics});
}

export function validateFrontendImports(envelope,policy,limits){
  return inspectFrontendImports(envelope,policy,limits,false);
}

// Collecte pure de refus, sans décision obligatoire/optionnel ni activation.
// Le préflight propriétaire applique ensuite la politique épinglée et les descripteurs.
// Intégrité de capture, schéma, politique et quotas restent des refus globaux.
export function collectFrontendImports(envelope,policy,limits){
  return inspectFrontendImports(envelope,policy,limits,true);
}
