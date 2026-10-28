// Contrôle AST de sources déjà capturées et dont les imports ont été validés.
// Profil fermé de code TRUSTED privilégié ; aucune garantie de sandbox universelle.
// Aucun chargement, aucune évaluation, aucun accès aux fichiers ni décision d’activation.
import { parseAst } from 'vite';
import { types } from 'node:util';

export const SOURCE_PROFILE_SCHEMA='pixs.presentation.source-profile/1.0.0';
export class PresentationSourceError extends Error {
  constructor(code){super(code);this.name='PresentationSourceError';this.code=code;}
}
const fail=code=>{throw new PresentationSourceError(code);};
const GLOBALS=new Set(['undefined','NaN','Infinity','Math','Object','Array','String','Number','Boolean','JSON']);
const REFUSED_NAMES=new Set(['window','document','globalThis','self','navigator','localStorage','sessionStorage','indexedDB','fetch','XMLHttpRequest','WebSocket','Worker','SharedWorker','ServiceWorker','React','ReactDOM','eval','Function','Reflect','Proxy','require','setTimeout','setInterval','queueMicrotask','requestAnimationFrame']);
const REFUSED_MEMBERS=new Set(['constructor','prototype','caller','callee','arguments','getPrototypeOf','setPrototypeOf','defineProperty','defineProperties','getOwnPropertyDescriptor','getOwnPropertyDescriptors','innerHTML','outerHTML','style','cssText','createElement','createElementNS','appendChild','insertAdjacentHTML','attachShadow','setAttribute','write']);
const ALLOWED=new Set([
  'Program','ImportDeclaration','ImportSpecifier','ImportDefaultSpecifier','ImportNamespaceSpecifier',
  'ExportNamedDeclaration','VariableDeclaration','VariableDeclarator','FunctionDeclaration','FunctionExpression','ArrowFunctionExpression',
  'Identifier','Literal','BlockStatement','ExpressionStatement','ReturnStatement','IfStatement','ConditionalExpression',
  'LogicalExpression','BinaryExpression','UnaryExpression','UpdateExpression','AssignmentExpression',
  'CallExpression','MemberExpression','ChainExpression','ArrayExpression','ObjectExpression','Property',
  'ForStatement','ForOfStatement','ForInStatement','WhileStatement','DoWhileStatement','BreakStatement','ContinueStatement',
  'TryStatement','CatchClause','ThrowStatement','EmptyStatement','AwaitExpression','TemplateLiteral','TemplateElement',
  'SwitchStatement','SwitchCase','SequenceExpression',
]);
function limits(value){
  if(value===null||typeof value!=='object'||types.isProxy(value)||![Object.prototype,null].includes(Object.getPrototypeOf(value)))fail('PROFILE_LIMITS_INVALID');
  const names=['maxSourceBytes','maxAstNodes','maxBindings','maxTextLength','maxScopeDepth'],keys=Reflect.ownKeys(value);
  if(keys.length!==names.length)fail('PROFILE_LIMITS_INVALID');
  const out={};
  for(const name of names){
    const d=Object.getOwnPropertyDescriptor(value,name);
    if(!d||!Object.hasOwn(d,'value')||!Number.isSafeInteger(d.value)||d.value<=0)fail('PROFILE_LIMITS_INVALID');
    out[name]=d.value;
  }
  return out;
}
function memberName(node){
  if(!node.computed){if(node.property?.type!=='Identifier')fail('PROFILE_MEMBER_REFUSED');return node.property.name;}
  const p=node.property;
  if(p?.type!=='Literal')fail('PROFILE_MEMBER_REFUSED');
  if(typeof p.value==='number'&&Number.isSafeInteger(p.value)&&p.value>=0)return String(p.value);
  if(typeof p.value==='string'&&p.value.length>0)return p.value;
  fail('PROFILE_MEMBER_REFUSED');
}
function forbiddenMember(name){return name.startsWith('__')||REFUSED_MEMBERS.has(name);}
function children(node,max){
  const result=[];
  for(const field of Object.keys(node)){
    if(['type','start','end','loc','range'].includes(field))continue;
    const v=node[field];
    if(Array.isArray(v)){for(const n of v)if(n&&typeof n.type==='string'){if(result.length>=max)fail('PROFILE_AST_LIMIT');result.push({node:n,parent:node,field});}}
    else if(v&&typeof v.type==='string'){if(result.length>=max)fail('PROFILE_AST_LIMIT');result.push({node:v,parent:node,field});}
  }
  return result;
}
function pureInitializer(root){
  if(!root)return false;
  const pending=[root];
  while(pending.length){
    const node=pending.pop();
    if(node.type==='FunctionExpression'||node.type==='ArrowFunctionExpression')continue;
    if(node.type==='Literal'){
      if(node.regex||node.bigint||!(node.value===null||['string','boolean','number'].includes(typeof node.value))||typeof node.value==='number'&&!Number.isFinite(node.value))return false;
      continue;
    }
    if(node.type==='UnaryExpression'&&['+','-','!'].includes(node.operator)&&node.argument.type==='Literal'){pending.push(node.argument);continue;}
    if(node.type==='ArrayExpression'){
      if(node.elements.some(n=>n===null))return false;
      for(const element of node.elements)pending.push(element);continue;
    }
    if(node.type==='ObjectExpression'){
      const seen=new Set();
      for(const p of node.properties){
        if(p.type!=='Property'||p.kind!=='init'||p.computed||p.method||p.shorthand)return false;
        const name=p.key.type==='Identifier'?p.key.name:p.key.type==='Literal'?String(p.key.value):null;
        if(name===null||forbiddenMember(name)||seen.has(name))return false;
        seen.add(name);pending.push(p.value);
      }
      continue;
    }
    return false;
  }
  return true;
}
function checkTopLevel(program){
  for(const top of program.body){
    if(top.type==='ImportDeclaration')continue;
    const node=top.type==='ExportNamedDeclaration'?top.declaration:top;
    if(!node)fail('PROFILE_TOP_LEVEL_EFFECT');
    if(node.type==='FunctionDeclaration'&&!node.generator)continue;
    if(node.type!=='VariableDeclaration'||node.kind!=='const')fail('PROFILE_TOP_LEVEL_EFFECT');
    for(const d of node.declarations)if(d.id.type!=='Identifier'||!pureInitializer(d.init))fail('PROFILE_TOP_LEVEL_EFFECT');
  }
}

export function analyzePresentationSource(text,inputLimits){
  const b=limits(inputLimits);
  if(typeof text!=='string'||!text.length||text.length>b.maxSourceBytes||text.charCodeAt(0)===0xFEFF||text.includes(String.fromCharCode(13))||text.includes(String.fromCharCode(0)))fail('PROFILE_SOURCE_INVALID');
  for(let i=0;i<text.length;i++){
    const n=text.charCodeAt(i);
    if(n>=0xD800&&n<=0xDBFF){const next=text.charCodeAt(i+1);if(!(next>=0xDC00&&next<=0xDFFF))fail('PROFILE_SOURCE_INVALID');i++;}
    else if(n>=0xDC00&&n<=0xDFFF)fail('PROFILE_SOURCE_INVALID');
  }
  const bytes=new TextEncoder().encode(text).length;
  if(bytes>b.maxSourceBytes)fail('PROFILE_SOURCE_INVALID');
  let program;try{program=parseAst(text);}catch{fail('PROFILE_PARSE_INVALID');}
  const root={parent:null,bindings:new Set(),depth:0};
  let count=0,bindingCount=0,maxDepth=0;
  const records=[],pending=[{node:program,parent:null,field:null,scope:root}];
  const newScope=parent=>{
    const depth=parent.depth+1;
    if(depth>b.maxScopeDepth)fail('PROFILE_SCOPE_LIMIT');
    maxDepth=Math.max(maxDepth,depth);
    return {parent,depth,bindings:new Set()};
  };
  const bind=(scope,node)=>{
    if(node?.type!=='Identifier'||REFUSED_NAMES.has(node.name)||GLOBALS.has(node.name))fail('PROFILE_BINDING_INVALID');
    if(node.name.length>b.maxTextLength)fail('PROFILE_TEXT_LIMIT');
    if(!scope.bindings.has(node.name)){
      if(++bindingCount>b.maxBindings)fail('PROFILE_BINDINGS_LIMIT');
      scope.bindings.add(node.name);
    }
  };
  while(pending.length){
    const frame=pending.pop(),n=frame.node;
    if(++count>b.maxAstNodes)fail('PROFILE_AST_LIMIT');
    if(!ALLOWED.has(n.type))fail('PROFILE_NODE_REFUSED');
    let scope=frame.scope;
    if(['FunctionDeclaration','FunctionExpression','ArrowFunctionExpression'].includes(n.type)){
      if(n.generator)fail('PROFILE_NODE_REFUSED');
      if(n.type==='FunctionDeclaration')bind(scope,n.id);
      scope=newScope(scope);
      if(n.type==='FunctionExpression'&&n.id)bind(scope,n.id);
      for(const param of n.params)bind(scope,param);
    }else if(['BlockStatement','ForStatement','ForOfStatement','ForInStatement','CatchClause','SwitchStatement'].includes(n.type)){
      scope=newScope(scope);
      if(n.type==='CatchClause'&&n.param)bind(scope,n.param);
    }
    if(n.type==='VariableDeclaration'){
      if(!['const','let'].includes(n.kind))fail('PROFILE_BINDING_INVALID');
      for(const d of n.declarations)bind(scope,d.id);
    }
    if(n.type==='ImportDeclaration'){
      if(n.attributes?.length||n.assertions?.length)fail('PROFILE_NODE_REFUSED');
      for(const s of n.specifiers)bind(scope,s.local);
    }
    if(n.type==='Literal'&&(n.regex||n.bigint))fail('PROFILE_NODE_REFUSED');
    if(n.type==='Literal'&&typeof n.value==='string'&&n.value.length>b.maxTextLength)fail('PROFILE_TEXT_LIMIT');
    if(n.type==='TemplateElement'&&((n.value?.raw?.length??0)>b.maxTextLength||(n.value?.cooked?.length??0)>b.maxTextLength))fail('PROFILE_TEXT_LIMIT');
    if(n.type==='Identifier'&&n.name.length>b.maxTextLength)fail('PROFILE_TEXT_LIMIT');
    if(n.type==='Property'){
      if(n.kind!=='init'||n.method||n.computed)fail('PROFILE_MEMBER_REFUSED');
      const name=n.key.type==='Identifier'?n.key.name:n.key.type==='Literal'?String(n.key.value):null;
      if(name===null||forbiddenMember(name))fail('PROFILE_MEMBER_REFUSED');
    }
    if(n.type==='MemberExpression'&&forbiddenMember(memberName(n)))fail('PROFILE_MEMBER_REFUSED');
    records.push({...frame,scope});
    const next=children(n,b.maxAstNodes-count-pending.length);
    for(let i=next.length-1;i>=0;i--)pending.push({...next[i],scope});
  }
  checkTopLevel(program);
  const bound=(scope,name)=>{for(let s=scope;s;s=s.parent)if(s.bindings.has(name))return true;return false;};
  for(const {node:n,parent,field,scope} of records){
    if(n.type==='AssignmentExpression'||n.type==='UpdateExpression'){
      const target=n.type==='AssignmentExpression'?n.left:n.argument;
      if(target.type!=='Identifier'||!bound(scope,target.name))fail('PROFILE_ASSIGNMENT_REFUSED');
    }
    if(n.type==='UnaryExpression'&&n.operator==='delete')fail('PROFILE_ASSIGNMENT_REFUSED');
    if(n.type!=='Identifier')continue;
    const bindingPosition=parent&&(
      parent.type==='VariableDeclarator'&&field==='id'
      ||['FunctionDeclaration','FunctionExpression','ArrowFunctionExpression'].includes(parent.type)&&['id','params'].includes(field)
      ||parent.type==='CatchClause'&&field==='param'
      ||['ImportSpecifier','ImportDefaultSpecifier','ImportNamespaceSpecifier'].includes(parent.type)
      ||parent.type==='MemberExpression'&&field==='property'&&!parent.computed
      ||parent.type==='Property'&&field==='key'&&!parent.computed&&!parent.shorthand
    );
    if(bindingPosition)continue;
    if(REFUSED_NAMES.has(n.name)||!GLOBALS.has(n.name)&&!bound(scope,n.name))fail('PROFILE_FREE_IDENTIFIER');
  }
  return Object.freeze({schema:SOURCE_PROFILE_SCHEMA,source_bytes:bytes,ast_nodes:count,bindings:bindingCount,scope_depth:maxDepth});
}
