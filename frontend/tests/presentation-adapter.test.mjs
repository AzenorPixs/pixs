// Tests avec ports moteur/commande doubles ; aucune preuve visuelle ou serveur.
import test from 'node:test';
import assert from 'node:assert/strict';
import {createPresentationAdapter,PresentationAdapterError,PRESENTATION_CLASSES} from '../src/shell/presentation-adapter-v1.js';
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

function setup(changes={}){
  const calls={submit:[],errors:[],reads:[],states:[]},ids=new Map();
  function Link(){}
  const ports={
    h:(type,props,...children)=>({type,props:props??{},children}),
    Link,
    label:(key,params,ctx)=>ctx.catalogs.fr[key].replace(/\{([A-Za-z][A-Za-z0-9_]*)\}/g,(_,name)=>String(params[name])),
    id:local=>{if(!ids.has(local))ids.set(local,'ui-'+ids.size);return ids.get(local);},
    state:id=>{calls.states.push(id);return {state:'IDLE',message:'Prêt',canSubmit:true,fieldsDisabled:false};},
    submit:async(...args)=>{calls.submit.push(args);return {state:'CONFIRMED'};},
    readFields:(element,names)=>{calls.reads.push({element,names});return Object.fromEntries(names.map(name=>[name,'example']));},
    slot:point=>({type:'slot-result',props:{point},children:[]}),
    component:(owner,id)=>({type:'component-result',props:{owner,id},children:[]}),
    onError:(...args)=>{calls.errors.push(args);},
    ...changes,
  };
  return {ports,calls,adapter:createPresentationAdapter(ports),Link};
}
function elements(root){
  const result=[],pending=[root];
  while(pending.length){
    const n=pending.pop();if(n===null||typeof n!=='object'||!Array.isArray(n.children))continue;
    result.push(n);for(let i=n.children.length-1;i>=0;i--)pending.push(n.children[i]);
  }
  return result;
}
const ofType=(root,type)=>elements(root).filter(n=>n.type===type);
const event=()=>({prevented:false,currentTarget:{marker:'private-dom-double'},preventDefault(){this.prevented=true;}});
function bad(fn,code){let e;try{fn();}catch(x){e=x;}assert.ok(e instanceof PresentationAdapterError);assert.equal(e.code,code);}
test('adapter : classes sémantiques et heading associé sans style ou HTML brut',()=>{
  const {adapter}=setup(),view=adapter.render(tree(),context()),heading=ofType(view,'h1')[0];
  assert.equal(view.type,'section');assert.equal(view.props['aria-labelledby'],heading.props.id);
  assert.equal(view.props.className,PRESENTATION_CLASSES['section.panel']);
  assert.equal(ofType(view,'p')[0].children[0],'Bonjour Alice');
  for(const n of elements(view)){assert.equal(Object.hasOwn(n.props,'style'),false);assert.equal(Object.hasOwn(n.props,'dangerouslySetInnerHTML'),false);}
});
test('adapter : headings distincts ne partagent pas une clé objet convertie en chaîne',()=>{
  const {adapter}=setup(),input=node('section','stack',{},[tree(),tree()]),view=adapter.render(input,context()),heads=ofType(view,'h1');
  assert.equal(heads.length,2);assert.ok(heads[0].props.id!==heads[1].props.id);
  const sections=ofType(view,'section').filter(s=>s.props['aria-labelledby']);
  assert.equal(sections[0].props['aria-labelledby'],heads[0].props.id);assert.equal(sections[1].props['aria-labelledby'],heads[1].props.id);
});
test('adapter : Link injecté et segment URI encodé',()=>{
  const {adapter,Link}=setup(),input=node('link','default',{key:'acme.one.title',params:{},route:'/apps/{item}',routeParams:{item:'café'}});
  const view=adapter.render(input,context());assert.equal(view.type,Link);assert.equal(view.props.to,'/apps/caf%C3%A9');
});
test('adapter : tous champs imbriqués rendus et submit hérite du formulaire',()=>{
  const {adapter,calls}=setup(),input=form();input.children=[node('section','stack',{},[node('section','stack',{},input.children)])];
  const view=adapter.render(input,context()),field=ofType(view,'input')[0],label=ofType(view,'label')[0],button=ofType(view,'button')[0];
  assert.equal(field.props.type,'text');assert.equal(field.props.name,'username');assert.equal(label.props.htmlFor,field.props.id);
  assert.equal(button.props.type,'submit');assert.ok(calls.states.every(id=>id==='create'));
  assert.equal(ofType(view,'output').length,1);assert.equal(field.props['aria-describedby'],ofType(view,'output')[0].props.id);
});
test('adapter : submit conserve événement privé, valeurs copiées et gelées',async()=>{
  const {adapter,calls}=setup(),view=adapter.render(form(),context()),evt=event();
  await view.props.onSubmit(evt);
  assert.equal(evt.prevented,true);assert.equal(calls.submit.length,1);
  const [id,intent,values,ctx]=calls.submit[0];
  assert.equal(id,'create');assert.equal(intent.command,'create-user');assert.equal(values.username,'example');
  assert.ok(Object.isFrozen(values));assert.ok(Object.isFrozen(ctx));assert.equal(Object.hasOwn(values,'currentTarget'),false);
  assert.equal(calls.reads[0].element,evt.currentTarget);
});
test('adapter : champ requis vide refusé avant appel commande',async()=>{
  const {adapter,calls}=setup({readFields:()=>({username:'  '})}),view=adapter.render(form(),context());
  await view.props.onSubmit(event());assert.equal(calls.submit.length,0);assert.equal(calls.errors.length,1);
  assert.equal(calls.errors[0][1],'PRESENTATION_SUBMIT_FAILED');
});

function buttonTree(){return node('button','secondary',{id:'run',key:'acme.one.submit',params:{},submit:false,intent:{command:'create-user',body:{payload:{username:'example'}},bindings:[]}});}
test('adapter : bouton autonome a statut automatique sans confirmer retour du port',async()=>{
  const {adapter,calls}=setup(),view=adapter.render(buttonTree(),context()),button=ofType(view,'button')[0],output=ofType(view,'output')[0];
  assert.equal(button.props['aria-describedby'],output.props.id);assert.equal(output.props['data-command-state'],'IDLE');
  await button.props.onClick(event());assert.equal(calls.submit.length,1);
  const after=adapter.render(buttonTree(),context());assert.equal(ofType(after,'output')[0].props['data-command-state'],'IDLE');
});
test('adapter : rejet asynchrone signalé sans recopier le message privé',async()=>{
  const {adapter,calls}=setup({submit:async()=>{throw new Error('synthetic-private-detail');}});
  await ofType(adapter.render(buttonTree(),context()),'button')[0].props.onClick(event());
  assert.equal(calls.errors.length,1);assert.equal(calls.errors[0][1],'PRESENTATION_SUBMIT_FAILED');
  assert.equal(JSON.stringify(calls.errors).includes('synthetic-private-detail'),false);
});
test('adapter : PENDING empêche une deuxième commande même si port incohérent',async()=>{
  const {adapter,calls}=setup({state:()=>({state:'PENDING',message:'En cours',canSubmit:true,fieldsDisabled:true})});
  const button=ofType(adapter.render(buttonTree(),context()),'button')[0];
  assert.equal(button.props.disabled,true);await button.props.onClick(event());assert.equal(calls.submit.length,0);
});
test('adapter : plusieurs statuts explicites ont ids uniques, sans statut auto doublé',()=>{
  const {adapter}=setup(),input=form();input.children.push(node('status','command',{for:'create'}));
  const view=adapter.render(input,context()),outputs=ofType(view,'output'),field=ofType(view,'input')[0];
  assert.equal(outputs.length,2);assert.ok(outputs[0].props.id!==outputs[1].props.id);assert.equal(field.props['aria-describedby'],outputs[0].props.id);
});
test('adapter : slots et composants restent des ports privés injectés',()=>{
  const {adapter}=setup(),input=node('section','stack',{},[node('slot','append',{point:'acme.one.area'}),node('component','public',{owner:'acme.widget',id:'acme.widget.card'})]);
  const view=adapter.render(input,context());
  assert.equal(ofType(view,'slot-result')[0].props.point,'acme.one.area');
  assert.equal(ofType(view,'component-result')[0].props.id,'acme.widget.card');
});
test('adapter : ports fermés, états invalides, ids dupliqués et labels non textuels refusés',()=>{
  const good=setup();bad(()=>createPresentationAdapter({...good.ports,extra:true}),'ADAPTER_PORTS_INVALID');
  bad(()=>setup({state:()=>({state:'ALLOW',message:'x',canSubmit:true,fieldsDisabled:false})}).adapter.render(form(),context()),'ADAPTER_STATE_INVALID');
  bad(()=>setup({id:()=>'same-id'}).adapter.render(form(),context()),'ADAPTER_ID_INVALID');
  bad(()=>setup({label:()=>42}).adapter.render(tree(),context()),'ADAPTER_LABEL_INVALID');
});
