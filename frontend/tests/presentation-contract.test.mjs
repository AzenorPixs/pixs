// Tests du contrat pur de présentation ; contexte fourni par un double explicite.
import test from 'node:test';
import assert from 'node:assert/strict';
import {PRESENTATION_SCHEMA,PresentationContractError,validatePresentationTree} from '../src/shell/presentation-contract-v1.js';
const clone=v=>JSON.parse(JSON.stringify(v));
const limits=()=>({maxNodes:128,maxDepth:16,maxChildren:32,maxTextLength:1024,maxParams:16,maxFields:16,maxBindings:16,maxDataNodes:4096,maxBodyDepth:16,maxBodyNodes:512});
function context(){
  return {owner:'acme.one',id:'acme.one.page',catalogs:{
    en:{'acme.one.title':'Title','acme.one.message':'Hello {name}','acme.one.form':'Create user','acme.one.username':'Username','acme.one.submit':'Create'},
    fr:{'acme.one.title':'Titre','acme.one.message':'Bonjour {name}','acme.one.form':'Créer un utilisateur','acme.one.username':'Identifiant','acme.one.submit':'Créer'}},
    routes:['/login','/apps/{item}'],slots:['acme.one.area'],components:[{owner:'acme.widget',id:'acme.widget.card'}],limits:limits()};
}
const node=(kind,variant,props,children=[])=>({kind,variant,props,children});
const text=()=>node('text','body',{key:'acme.one.message',params:{name:'Alice'}});
const tree=()=>node('section','panel',{},[node('heading','page',{key:'acme.one.title',params:{}}),text()]);
function intent(){return {command:'create-user',body:{payload:{username:null}},bindings:[{field:'username',path:['payload','username']}]};}
function form(){
  return node('form','stack',{id:'create',key:'acme.one.form',params:{},intent:intent()},[
    node('field','text',{name:'username',key:'acme.one.username',params:{},required:true,initial:''}),
    node('button','primary',{id:'submit',key:'acme.one.submit',params:{},submit:true,intent:null}),
    node('status','command',{for:'create'}),
  ]);
}
function refused(value,ctx=context()){
  let error;try{validatePresentationTree(value,ctx);}catch(cause){error=cause;}
  assert.ok(error instanceof PresentationContractError);
  assert.equal(typeof error.code,'string');assert.ok(error.code.length>0);
}
test('présentation : arbre fermé copié, profondément gelé et sans mutation',()=>{
  const input=tree(),before=JSON.stringify(input),result=validatePresentationTree(input,context());
  assert.equal(PRESENTATION_SCHEMA,'pixs.presentation/1.0.0');
  assert.equal(JSON.stringify(result),before);assert.equal(JSON.stringify(input),before);
  assert.ok(result!==input);assert.ok(Object.isFrozen(result.children[1].props.params));assert.equal(Object.isFrozen(input),false);
});
test('présentation : alias autorisés copiés sans partager, cycles refusés',()=>{
  const child=text(),input=node('section','stack',{},[child,child]);
  const result=validatePresentationTree(input,context());
  assert.ok(result.children[0]!==result.children[1]);
  const cyclic=node('section','stack',{},[]);cyclic.children.push(cyclic);refused(cyclic);
});
test('présentation : styles, HTML, composants bruts et variantes inconnues refusés',()=>{
  for(const key of ['style','className','html','dangerouslySetInnerHTML']){
    const input=text();input.props[key]='raw';refused(input);
  }
  const unknown=text();unknown.variant='custom';refused(unknown);
  refused({type:'div',props:{children:'raw'}});
  refused(node('text','body',{key:'acme.one.message',params:{name:()=>null}}));
});
test('présentation : catalogue propriétaire et paramètres exacts des deux langues',()=>{
  const missing=text();missing.props.params={};refused(missing);
  const extra=text();extra.props.params.other='extra';refused(extra);
  const foreign=text();foreign.props.key='foreign.message';refused(foreign);
  const ctx=context();ctx.catalogs.fr['acme.one.message']='Bonjour {other}';refused(text(),ctx);
});
test('présentation : liens déclarés avec paramètres URL complets et sûrs',()=>{
  validatePresentationTree(node('link','default',{key:'acme.one.title',params:{},route:'/apps/{item}',routeParams:{item:'example'}}),context());
  for(const item of ['.','..','../x','a/b','a%2fb','https:evil']){
    refused(node('link','default',{key:'acme.one.title',params:{},route:'/apps/{item}',routeParams:{item}}));
  }
  refused(node('link','default',{key:'acme.one.title',params:{},route:'https://example.invalid',routeParams:{}}));
});
test('présentation : seuls slots et composants publics admis par le contexte',()=>{
  validatePresentationTree(node('slot','append',{point:'acme.one.area'}),context());
  validatePresentationTree(node('component','public',{owner:'acme.widget',id:'acme.widget.card'}),context());
  refused(node('slot','append',{point:'acme.private.area'}));
  refused(node('component','public',{owner:'acme.widget',id:'acme.widget.private'}));
});
test('présentation : formulaire, liaison de champ et statut de commande sans exécution',()=>{
  const input=form(),result=validatePresentationTree(input,context());
  assert.equal(JSON.stringify(result),JSON.stringify(input));
  assert.equal(Object.hasOwn(result.props.intent,'idempotencyKey'),false);
  const forged=form();forged.children[2].props.state='CONFIRMED';refused(forged);
  const success=form();success.children[2].props.tone='success';refused(success);
});
test('présentation : statut ne référence pas un id action absent',()=>{
  const input=form();input.children[2].props.for='absent';refused(input);
  refused(node('status','command',{for:'absent'}));
});
test('présentation : champs ou cibles de liaison dupliqués refusés',()=>{
  const duplicate=form();duplicate.children.unshift(clone(duplicate.children[0]));refused(duplicate);
  const binding=form();binding.props.intent.bindings.push(clone(binding.props.intent.bindings[0]));refused(binding);
  const absent=form();absent.props.intent.bindings[0].field='absent';refused(absent);
});
test('présentation : chemins de corps déclarés, pas prototype ni cible arbitraire',()=>{
  for(const path of [['missing'],['payload','missing'],['__proto__','x'],['payload',0]]){
    const input=form();input.props.intent.bindings[0].path=path;refused(input);
  }
  const key=form();key.props.intent.idempotencyKey='module-key';refused(key);
});
test('présentation : formulaire imbriqué et champs ou submit sans formulaire refusés',()=>{
  const nested=form();nested.children.push(form());refused(nested);
  refused(node('field','text',{name:'username',key:'acme.one.username',params:{},required:true,initial:''}));
  refused(node('button','primary',{id:'submit',key:'acme.one.submit',params:{},submit:true,intent:null}));
});
test('présentation : accesseurs jamais invoqués et tableaux creux refusés',()=>{
  let called=false;const input=text();Object.defineProperty(input.props,'key',{get(){called=true;return 'acme.one.message';},enumerable:true});
  refused(input);assert.equal(called,false);
  const sparse=node('section','stack',{},new Array(3));refused(sparse);
});
test('présentation : quotas explicites de nœuds, profondeur, données et corps',()=>{
  for(const [key,value] of [['maxNodes',1],['maxDepth',1],['maxDataNodes',1]]){
    const ctx=context();ctx.limits[key]=value;refused(key==='maxDepth'?node('section','stack',{},[tree()]):tree(),ctx);
  }
  const body=context();body.limits.maxBodyNodes=1;refused(form(),body);
  const bindings=context();bindings.limits.maxBindings=1;
  const two=form();two.children.splice(1,0,node('field','text',{name:'second',key:'acme.one.username',params:{},required:false,initial:''}));
  two.props.intent.body.payload.second=null;two.props.intent.bindings.push({field:'second',path:['payload','second']});refused(two,bindings);
});

test('présentation : bouton autonome et statut avant déclaration d’action',()=>{
  const input=node('section','stack',{},[
    node('status','command',{for:'run'}),
    node('button','secondary',{id:'run',key:'acme.one.submit',params:{},submit:false,intent:{command:'create-user',body:{payload:{username:'example'}},bindings:[]}}),
  ]);
  validatePresentationTree(input,context());
});
test('présentation : bouton submit ne crée pas un faux id de résultat autonome',()=>{
  const input=form();input.children[2].props.for='submit';refused(input);
});
test('présentation : section de formulaire conserve portée des champs et liaisons',()=>{
  const input=form();input.children=[node('section','stack',{},input.children)];
  validatePresentationTree(input,context());
});
