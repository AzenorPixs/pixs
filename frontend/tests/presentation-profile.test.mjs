import test from 'node:test';
import assert from 'node:assert/strict';
import {analyzePresentationSource,SOURCE_PROFILE_SCHEMA} from '../scripts/presentation-profile-v1.mjs';
const limits=()=>({maxSourceBytes:32768,maxAstNodes:4096,maxBindings:256,maxTextLength:4096,maxScopeDepth:32});
const accepted=source=>analyzePresentationSource(source,limits());
const refused=(source,code,b=limits())=>assert.throws(()=>analyzePresentationSource(source,b),e=>e.code===code);
const VIEW='export function View(api){return api.present({kind:"text",variant:"body",props:{key:"acme.one.label",params:{}},children:[]});}';

test('profil : fonction publique et constantes JSON, rapport borné sans état ready',()=>{
  const r=accepted('const config={x:1};'+VIEW);
  assert.equal(r.schema,SOURCE_PROFILE_SCHEMA);assert(r.ast_nodes>0);assert(Object.isFrozen(r));
  assert.equal(Object.hasOwn(r,'ready'),false);
});
test('profil : import déjà validé et fonctions asynchrones via façade',()=>{
  accepted('import { QueryClient } from "pixs-shell/v1"; export async function View(api){const data=await api.QueryClient.query("users"); return api.present(data);}');
});
test('profil : fermetures, paramètres et variables locales résolus',()=>{
  accepted('export function View(api){let n=0;const names=["a"];for(let i=0;i<names.length;i++){n+=i;}return names.map(x=>x.toUpperCase()).join(",");}');
  accepted('export function View(api){const f=x=>x;return f(api);}');
});
test('profil : bloc et boucle ne rendent pas leur variable visible au parent',()=>{
  refused('export function View(api){if(true){const inner=1;}return inner;}','PROFILE_FREE_IDENTIFIER');
  refused('export function View(api){for(let i=0;i<1;i++){}return i;}','PROFILE_FREE_IDENTIFIER');
});
test('profil : paramètre catch local et primitives standard',()=>{
  accepted('export function View(api){try{throw 1;}catch(error){return String(error);}}');
});
test('profil : appel ou écriture au chargement refusés avant évaluation',()=>{
  for(const s of ['const x=make();','globalThis.PROFILE_EXECUTED=true;','let x=1;','const x=await Promise.resolve(1);'])
    refused(s,'PROFILE_TOP_LEVEL_EFFECT');
  assert.equal(globalThis.PROFILE_EXECUTED,undefined);
});
test('profil : globals DOM, stockage, réseau et moteur refusés dans une fonction',()=>{
  for(const name of ['window','document','navigator','localStorage','sessionStorage','indexedDB','fetch','ReactDOM','Worker'])
    refused('export const View=api=>'+name+';','PROFILE_FREE_IDENTIFIER');
});
test('profil : noms libres non déclarés et globals masqués refusés',()=>{
  refused('export const View=api=>unknown;','PROFILE_FREE_IDENTIFIER');
  refused('const window={};'+VIEW,'PROFILE_BINDING_INVALID');
});
test('profil : propriétés constructeur, prototype et réflexion refusées',()=>{
  for(const member of ['constructor','prototype','__proto__','getPrototypeOf','defineProperty','innerHTML','style'])
    refused('export const View=api=>api.'+member+';','PROFILE_MEMBER_REFUSED');
});
test('profil : computed non littéral et constructeur échappé refusés',()=>{
  refused('export const View=api=>api["con"+"structor"];','PROFILE_MEMBER_REFUSED');
  refused('export const View=(api,key)=>api[key];','PROFILE_MEMBER_REFUSED');
  const escaped=String.fromCharCode(92)+'u0063onstructor';
  refused('export const View=api=>api["'+escaped+'"];','PROFILE_MEMBER_REFUSED');
  accepted('export function first(items){return items[0].name;}');
});
test('profil : nouvelles instances, this, classes et import dynamique refusés',()=>{
  for(const s of ['export const View=api=>new Date();','export const View=api=>this;','class X{}','export const View=api=>import("x");'])
    refused(s,'PROFILE_NODE_REFUSED');
});
test('profil : mutations membres refusées, compteur local autorisé',()=>{
  refused('export function View(api){api.state=1;}','PROFILE_ASSIGNMENT_REFUSED');
  refused('export function View(api){delete api.state;}','PROFILE_ASSIGNMENT_REFUSED');
  accepted('export function View(api){let n=0;n++;return n;}');
});
test('profil : getters, computed objet et destructuration hors profil refusés',()=>{
  refused('export const View=api=>({get value(){return api;}});','PROFILE_MEMBER_REFUSED');
  refused('export const View=api=>({[api.name]:1});','PROFILE_MEMBER_REFUSED');
  refused('export const View=({api})=>api;','PROFILE_BINDING_INVALID');
});
test('profil : quotas AST, bindings, profondeur et texte explicites',()=>{
  const ast=limits();ast.maxAstNodes=1;refused(VIEW,'PROFILE_AST_LIMIT',ast);
  const bindings=limits();bindings.maxBindings=1;refused(VIEW,'PROFILE_BINDINGS_LIMIT',bindings);
  const depth=limits();depth.maxScopeDepth=1;refused(VIEW,'PROFILE_SCOPE_LIMIT',depth);
  const bytes=limits();bytes.maxSourceBytes=1;refused(VIEW,'PROFILE_SOURCE_INVALID',bytes);
  const text=limits();text.maxTextLength=2;refused('const x="long";','PROFILE_TEXT_LIMIT',text);
});
test('profil : BOM, CR, NUL et surrogate invalide refusés avant parsing',()=>{
  for(const unit of [0xFEFF,13,0,0xD800])refused(String.fromCharCode(unit)+VIEW,'PROFILE_SOURCE_INVALID');
});
test('profil : limites fermées, accesseur jamais invoqué et syntaxe invalide',()=>{
  const b=limits();b.extra=true;refused(VIEW,'PROFILE_LIMITS_INVALID',b);
  let called=false;const getter=limits();Object.defineProperty(getter,'maxAstNodes',{get(){called=true;return 1;},enumerable:true});
  refused(VIEW,'PROFILE_LIMITS_INVALID',getter);assert.equal(called,false);
  refused('export function View(','PROFILE_PARSE_INVALID');
});

test('profil : quotas texte identifiant et template distincts du refus structurel',()=>{
  const b=limits();b.maxTextLength=2;refused('const longname=1;','PROFILE_TEXT_LIMIT',b);
  refused('const x='+String.fromCharCode(96)+'long'+String.fromCharCode(96)+';','PROFILE_TEXT_LIMIT',b);
  refused('const x=/a/;','PROFILE_NODE_REFUSED');
});
